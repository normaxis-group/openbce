# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Lecture d'un RSEE (récapitulatif standardisé d'étude énergétique et environnementale).

Un RSEE porte trois blocs : Datas_Comp (données administratives), RSET/Entree_Projet (les données d'entrée du moteur,
au format réglementaire) et RSET/Sortie_Projet (les résultats). Le format pivot du moteur est calqué sur Entree_Projet :
un arbre de nœuds dont les noms sont ceux du format réglementaire.

    projet = lire("fichier.xml")
    for groupe in projet.entree.tous("Groupe"): ...
    projet.sortie.un("Sortie_Batiment_B").nombre("O_Bbio_pts_annuel")
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


def _nu(tag: str) -> str:
    return tag.split("}")[-1]


@dataclass
class Noeud:
    """Un élément du fichier : ses valeurs simples (texte) et ses enfants. Les « X_Collection » sont aplaties."""

    nom: str
    valeurs: dict[str, str] = field(default_factory=dict)
    enfants: list["Noeud"] = field(default_factory=list)

    def nombre(self, cle: str, defaut: float | None = None) -> float:
        v = self.valeurs.get(cle)
        if v is None or v == "":
            if defaut is None:
                raise KeyError(f"{self.nom}.{cle} absent")
            return defaut
        return float(v.replace(",", "."))

    def entier(self, cle: str, defaut: int | None = None) -> int:
        return int(self.nombre(cle, defaut))

    def texte(self, cle: str, defaut: str = "") -> str:
        return self.valeurs.get(cle, defaut)

    def serie(self, cle: str) -> list[float]:
        """Valeur faite de nombres séparés par des espaces ou des points-virgules (masques, paramètres horaires)."""
        return [float(x) for x in self.valeurs.get(cle, "").replace(";", " ").split()]

    def directs(self, nom: str) -> list["Noeud"]:
        return [e for e in self.enfants if e.nom == nom]

    def tous(self, nom: str) -> list["Noeud"]:
        trouves = []
        for e in self.enfants:
            if e.nom == nom:
                trouves.append(e)
            trouves.extend(e.tous(nom))
        return trouves

    def un(self, nom: str) -> "Noeud":
        trouves = self.tous(nom)
        if not trouves:
            raise KeyError(f"{nom} absent sous {self.nom}")
        return trouves[0]

    def mensuel(self, cle: str) -> list[float]:
        """Série de douze valeurs rangées sous <cle><Sortie_Mensuelle><Mois/><Valeur/>."""
        bloc = next((e for e in self.enfants if e.nom == cle), None)
        if bloc is None:
            return []
        mois = sorted(bloc.directs("Sortie_Mensuelle"), key=lambda m: m.entier("Mois"))
        return [m.nombre("Valeur", 0.0) for m in mois]


def _noeud(el: ET.Element) -> Noeud:
    n = Noeud(_nu(el.tag))
    for e in el:
        nom = _nu(e.tag)
        if len(e) == 0:
            n.valeurs[nom] = (e.text or "").strip()
        elif nom.endswith("_Collection") or nom.endswith("_collection"):
            n.enfants.extend(_noeud(x) for x in e)
        else:
            n.enfants.append(_noeud(e))
    return n


@dataclass
class Projet:
    chemin: Path
    version_rsee: str
    administratif: Noeud
    entree: Noeud
    sortie: Noeud

    @property
    def version_moteur(self) -> str:
        return self.entree.texte("Version")


def lire(chemin: str | Path) -> Projet:
    racine = ET.parse(chemin).getroot()
    blocs = {}
    for el in racine.iter():
        nom = _nu(el.tag)
        if nom in ("Datas_Comp", "Entree_Projet", "Sortie_Projet") and nom not in blocs:
            blocs[nom] = el
    manque = {"Entree_Projet", "Sortie_Projet"} - set(blocs)
    if manque:
        raise ValueError(f"{chemin} : bloc(s) absent(s) {sorted(manque)}")
    datas = blocs.get("Datas_Comp")
    return Projet(Path(chemin), (datas.get("version", "") if datas is not None else "") or racine.get("version", ""),
                  _noeud(datas) if datas is not None else Noeud("Datas_Comp"), _noeud(blocs["Entree_Projet"]), _noeud(blocs["Sortie_Projet"]))
