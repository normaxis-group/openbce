# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Étude de sensibilité : effet de quelques leviers de conception sur le Bbio des projets de logement.

    python -m banc.variantes <dossier de RSEE> <sortie.csv> [processus]

Pour chaque projet (un fichier), le Bbio est recalculé par OpenBCE avec les données du RSEE puis avec une donnée
modifiée à la fois. L'écart est pris entre deux calculs d'OpenBCE, jamais avec le RSEE : le biais du moteur s'annule
en grande partie. Les leviers ne sont pas chiffrés : c'est un classement par points de Bbio, à croiser avec des coûts.
"""
from __future__ import annotations

import csv
import json
import multiprocessing
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee

_LIRE = rsee.lire


def _chaque(projet, nom):
    return projet.entree.tous(nom)


def _facteur(noeud, cle, f, plancher=0.0):
    if noeud.valeurs.get(cle) not in (None, ""):
        noeud.valeurs[cle] = repr(max(noeud.nombre(cle) * f, plancher))


def _decalage(noeud, cle, d, plancher):
    if noeud.valeurs.get(cle) not in (None, "") and noeud.nombre(cle) > 0:
        noeud.valeurs[cle] = repr(max(noeud.nombre(cle) + d, plancher))


def etancheite_mesuree(p):
    """Perméabilité justifiée sans échantillonnage : la majoration de 20 % disparaît."""
    for n in _chaque(p, "Permeabilite"):
        n.valeurs["id_echantillonnage_permea"] = "1"


def etancheite_moins_02(p):
    """Perméabilité abaissée de 0,2 m³/(h.m²)."""
    for n in _chaque(p, "Permeabilite"):
        _decalage(n, "Q4PaSurf", -0.2, 0.1)


def baies_uw_moins_02(p):
    """Uw des baies abaissé de 0,2 W/(m².K), protection relevée ou baissée."""
    for n in _chaque(p, "Baie"):
        for cle in ("Usp_Vert", "Usp_Horiz", "Uap_Vert", "Uap_Horiz"):
            _decalage(n, cle, -0.2, 0.5)


def baies_sw_plus_10(p):
    """Facteur solaire des baies sans protection augmenté de 10 % (vitrage plus transparent)."""
    for n in _chaque(p, "Baie"):
        for cle in ("Sw1_sp_c", "Sw2_sp_c", "Sw3_sp_c"):
            _facteur(n, cle, 1.1)


def baies_sw_moins_10(p):
    """Facteur solaire des baies sans protection réduit de 10 % (vitrage plus sélectif)."""
    for n in _chaque(p, "Baie"):
        for cle in ("Sw1_sp_c", "Sw2_sp_c", "Sw3_sp_c"):
            _facteur(n, cle, 0.9)


def parois_u_moins_20(p):
    """U des parois opaques réduit de 20 % (isolation renforcée)."""
    for n in _chaque(p, "Paroi_Opaque"):
        _facteur(n, "Uk", 0.8)


def ponts_moins_30(p):
    """Coefficients linéiques des ponts thermiques réduits de 30 %."""
    for n in _chaque(p, "Lineaire"):
        _facteur(n, "Psil", 0.7)


def _gestion(p, cible):
    for n in _chaque(p, "Baie"):
        choix = n.entier("Choix_PM_GPM", 0)
        if 1 <= choix <= 6:
            n.valeurs["Choix_PM_GPM"] = str((3 if choix >= 4 else 0) + cible)


def protections_automatiques(p):
    """Toutes les protections mobiles en gestion automatique."""
    _gestion(p, 1)


def protections_manuelles(p):
    """Toutes les protections mobiles en gestion manuelle non motorisée."""
    _gestion(p, 2)


def protections_motorisees(p):
    """Toutes les protections mobiles en gestion manuelle motorisée."""
    _gestion(p, 3)


VARIANTES = [None, etancheite_mesuree, etancheite_moins_02, baies_uw_moins_02, baies_sw_plus_10, baies_sw_moins_10, parois_u_moins_20, ponts_moins_30,
             protections_automatiques, protections_manuelles, protections_motorisees]


def calcul(tache):
    projet, fichier, k = tache
    variante = VARIANTES[k]

    def lire(chemin):
        p = _LIRE(chemin)
        if variante is not None:
            variante(p)
        return p

    besoins.rsee.lire = lire
    try:
        lignes = besoins.comparer(fichier)
    except Exception as e:
        return [(projet, variante.__name__ if variante else "base", "", "", "", "", "", "", type(e).__name__)]
    finally:
        besoins.rsee.lire = _LIRE
    return [(projet, variante.__name__ if variante else "base", zone, usage, round(surface, 1), round(ch.sum(), 3), round(fr.sum(), 3), round(ecl.sum(), 3), bbio_ref)
            for _, zone, usage, surface, ch, _a, fr, _b, ecl, _c, bbio_ref, _annuel in lignes]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, sortie = Path(sys.argv[1]), Path(sys.argv[2])
    processus = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    fichiers, projets = [], set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in projets:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        types = {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")}
        if types <= {0, 1, 2, 3, 4, 5, 6} and all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            fichiers.append((x["projet"], str(dossier / x["fichier"])))
            projets.add(x["projet"])
    taches = [(projet, f, k) for projet, f in fichiers for k in range(len(VARIANTES))]
    print(len(fichiers), "projets,", len(taches), "calculs,", processus, "processus", flush=True)
    with multiprocessing.Pool(processus) as pool, open(sortie, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["projet", "variante", "zone", "usage", "surface", "chauffage", "froid", "eclairage", "bbio_rsee"])
        for n, lignes in enumerate(pool.imap_unordered(calcul, taches), 1):
            w.writerows(lignes)
            if n % 50 == 0:
                f.flush()
                print(n, "calculs faits", flush=True)
    print("terminé")
