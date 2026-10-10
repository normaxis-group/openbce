# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Écriture du bloc Sortie_Projet d'un RSEE à partir des résultats du moteur.

Le bloc est construit avec les noms de champs des RSEE des logiciels évalués (Sortie_Batiment_B/C/D, Sortie_Zone_*,
Sortie_Groupe_*, séries mensuelles sous <X_mois><Sortie_Mensuelle><Index/><Mois/><Valeur/>). Première version : besoins
Th-B et Bbio (B), besoins et consommations Th-C par poste et par énergie (C), degrés-heures d'inconfort (D). Les
agrégats de zone et de bâtiment sont des moyennes pondérées par la surface de référence des groupes. Les champs non
calculés sont absents du fichier (pas de valeur inventée) ; aucun schéma XSD n'est disponible dans le corpus pour
valider la structure, qui reprend celle des RSEE lus.

Entrée : un dictionnaire `calcul` :
    {"batiments": [{"index", "name", "zones": [{"index", "name", "usage", "nb_logements", "bbio_max" (dict ou None),
                     "groupes": [{"index", "name", "sref", "shab", "su", "climatise",
                                  "b_ch_mois", "b_fr_mois", "b_ecl_mois"   (Th-B, 12 valeurs kWh/m²),
                                  "c_b_ch_mois", "c_b_fr_mois"            (Th-C, besoins),
                                  "c_b_ecs", "cef" {ch, fr, ecs, ecl, aux_vent, aux_dist} (kWh/m²),
                                  "cef_energie" {(poste, énergie): kWh/m²}, "dh", "nb_h_inconf" (3), "dh_max"}]}]},
                   "cep": {"cef_annuel", "cep_annuel", "cep_nr_annuel", "imp" {poste: kWh/m²}, "par_energie" {énergie: kWh/m²}}}]}
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

POSTES = ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist", "deplacement", "mobilier")
ENERGIES = ("gaz", "fioul", "bois", "elec", "reseau")
POINTS = {"ch": 2.0, "fr": 2.0, "ecl": 5.0}        # Bbio (2.1)


def _val(parent: ET.Element, nom: str, valeur) -> ET.Element:
    e = ET.SubElement(parent, nom)
    if isinstance(valeur, float):
        e.text = f"{valeur:.10g}" if abs(valeur) < 1e-3 and valeur != 0 else f"{round(valeur, 4):g}"
    else:
        e.text = str(valeur)
    return e


def _mois(parent: ET.Element, nom: str, serie) -> None:
    bloc = ET.SubElement(parent, nom)
    for i, v in enumerate(serie):
        m = ET.SubElement(bloc, "Sortie_Mensuelle")
        _val(m, "Index", i + 1)
        _val(m, "Mois", i + 1)
        _val(m, "Valeur", round(float(v), 2))


def _surface(g: dict) -> float:
    return float(g.get("sref") or g.get("shab") or g.get("su") or 0.0)


def _moyenne(groupes: list[dict], cle, defaut=0.0):
    """Moyenne pondérée par la surface d'une grandeur par m² ; `cle` : nom ou fonction d'extraction."""
    f = cle if callable(cle) else (lambda g: g.get(cle, defaut))
    total = sum(_surface(g) for g in groupes)
    if total <= 0:
        return defaut
    return sum(_surface(g) * (f(g) if f(g) is not None else defaut) for g in groupes) / total


def _moyenne_mois(groupes: list[dict], cle: str) -> list[float]:
    return [_moyenne(groupes, lambda g, m=m: (g.get(cle) or [0.0] * 12)[m]) for m in range(12)]


def _bbio_pts(ch, fr, ecl) -> float:
    return POINTS["ch"] * ch + POINTS["fr"] * fr + POINTS["ecl"] * ecl


def _bloc_b(parent: ET.Element, nom: str, index: int, name: str, groupes: list[dict], usage: int | None = None, bbio_max: dict | None = None) -> ET.Element:
    e = ET.SubElement(parent, nom)
    _val(e, "Index", index)
    _val(e, "Name", name)
    _val(e, "O_SREF", round(sum(_surface(g) for g in groupes), 2))
    if nom != "Sortie_Batiment_B":
        _val(e, "O_SHAB", round(sum(float(g.get("shab") or 0.0) for g in groupes), 2))
        _val(e, "O_SU", round(sum(float(g.get("su") or 0.0) for g in groupes), 2))
    if usage is not None and nom == "Sortie_Zone_B":
        _val(e, "Usage", usage)
    if nom == "Sortie_Groupe_B":
        _val(e, "Is_Climatise", int(bool(groupes[0].get("climatise"))))
    ch, fr, ecl = (_moyenne_mois(groupes, k) for k in ("b_ch_mois", "b_fr_mois", "b_ecl_mois"))
    if bbio_max:
        _val(e, "O_Bbio_Max", round(bbio_max["bbio_max"], 1))
        if nom == "Sortie_Groupe_B":
            for k, nom_rsee in (("mbgeo", "O_Mbgeo"), ("mbcombles", "O_Mbcombles"), ("mbsurf_moy", "O_Mbsurf_moy"), ("mbsurf_tot", "O_Mbsurf_tot"), ("mbbruit", "O_Mbbruit")):
                _val(e, nom_rsee, round(bbio_max.get(k, 0.0), 4))
    _val(e, "O_B_Ch_annuel", round(sum(ch), 1))
    _val(e, "O_B_Fr_annuel", round(sum(fr), 1))
    _val(e, "O_B_Ecl_annuel", round(sum(ecl), 1))
    _val(e, "O_Bbio_pts_annuel", round(_bbio_pts(sum(ch), sum(fr), sum(ecl)), 1))
    _mois(e, "O_B_Ch_mois", ch)
    _mois(e, "O_B_Fr_mois", fr)
    _mois(e, "O_B_Ecl_mois", ecl)
    _mois(e, "O_Bbio_pts_mois", [_bbio_pts(a, b, c) for a, b, c in zip(ch, fr, ecl)])
    return e


def _cef(g: dict, poste: str) -> float:
    return float((g.get("cef") or {}).get(poste, 0.0))


def _cef_energie(g: dict, poste: str, energie: str) -> float:
    return float((g.get("cef_energie") or {}).get((poste, energie), 0.0))


def _bloc_c_groupe(parent: ET.Element, g: dict) -> ET.Element:
    e = ET.SubElement(parent, "Sortie_Groupe_C")
    _val(e, "Index", g["index"])
    _val(e, "Name", g["name"])
    _val(e, "O_SREF", round(_surface(g), 2))
    _val(e, "O_SHAB", round(float(g.get("shab") or 0.0), 2))
    _val(e, "O_SU", round(float(g.get("su") or 0.0), 2))
    cef = sum(_cef(g, p) for p in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist"))
    _val(e, "O_Cef_annuel", round(cef, 1))
    for poste, nom in (("ch", "O_Cef_ch_annuel"), ("fr", "O_Cef_fr_annuel"), ("ecs", "O_Cef_ecs_annuel"), ("ecl", "O_Cef_ecl_annuel"),
                       ("aux_vent", "O_Cef_aux_ventilateur_annuel"), ("aux_dist", "O_Cef_aux_distribution_annuel")):
        _val(e, nom, round(_cef(g, poste), 1))
    for poste in ("ch", "fr", "ecs"):
        for energie in ENERGIES:
            _val(e, f"O_Cef_{poste}_{energie}_annuel", round(_cef_energie(g, poste, energie), 1))
    _val(e, "O_Cef_ecl_elec_annuel", round(_cef(g, "ecl"), 1))
    _val(e, "O_Cef_auxv_elec_annuel", round(_cef(g, "aux_vent"), 1))
    _val(e, "O_Cef_auxs_elec_annuel", round(_cef(g, "aux_dist"), 1))
    for energie in ENERGIES:
        total = sum(_cef_energie(g, p, energie) for p in ("ch", "fr", "ecs"))
        if energie == "elec":
            total += sum(_cef(g, p) for p in ("ecl", "aux_vent", "aux_dist"))
        _val(e, f"O_Cef_{energie}_annuel", round(total, 1))
    _val(e, "O_B_Ecs_annuel", round(float(g.get("c_b_ecs") or 0.0), 1))
    ch, fr = _moyenne_mois([g], "c_b_ch_mois"), _moyenne_mois([g], "c_b_fr_mois")
    _val(e, "O_B_Ch_annuel", round(sum(ch), 1))
    _val(e, "O_B_Fr_annuel", round(sum(fr), 1))
    _val(e, "O_B_Ecl_annuel", round(sum(g.get("b_ecl_mois") or [0.0] * 12), 1))
    _mois(e, "O_B_Ch_mois", ch)
    _mois(e, "O_B_Fr_mois", fr)
    return e


def _bloc_d_groupe(parent: ET.Element, g: dict) -> ET.Element:
    e = ET.SubElement(parent, "Sortie_Groupe_D")
    _val(e, "Index", g["index"])
    _val(e, "Name", g["name"])
    _val(e, "O_SREF", round(_surface(g), 2))
    _val(e, "O_SHAB", round(float(g.get("shab") or 0.0), 2))
    _val(e, "O_SU", round(float(g.get("su") or 0.0), 2))
    if g.get("dh") is not None:
        _val(e, "O_NbDegresHeures", round(float(g["dh"]), 1))
        if g.get("dh_max") is not None:
            _val(e, "O_NbDegresHeures_max", round(float(g["dh_max"]), 1))
        nb = g.get("nb_h_inconf") or (0, 0, 0)
        for k, nom in enumerate(("O_Nb_h_inconf", "O_Nb_h_inconf_1", "O_Nb_h_inconf_2")):
            _val(e, nom, int(nb[k]))
    return e


def construire(calcul: dict, version: str = "", departement: str = "", altitude: float = 0.0) -> ET.Element:
    """Élément Sortie_Projet."""
    racine = ET.Element("Sortie_Projet")
    _val(racine, "Index", 1)
    _val(racine, "Name", calcul.get("name", "openbce"))
    _val(racine, "Version", version)
    _val(racine, "Departement", departement)
    _val(racine, "Altitude", altitude)
    coll_b, coll_c, coll_d = (ET.SubElement(racine, n) for n in ("Sortie_Batiment_B_Collection", "Sortie_Batiment_C_Collection", "Sortie_Batiment_D_Collection"))
    for bat in calcul["batiments"]:
        groupes_bat = [g for z in bat["zones"] for g in z["groupes"]]
        # ---- Th-B
        eb = _bloc_b(coll_b, "Sortie_Batiment_B", bat["index"], bat["name"], groupes_bat)
        zb = ET.SubElement(eb, "Sortie_Zone_B_Collection")
        for z in bat["zones"]:
            ez = _bloc_b(zb, "Sortie_Zone_B", z["index"], z["name"], z["groupes"], z.get("usage"), z.get("bbio_max"))
            gb = ET.SubElement(ez, "Sortie_Groupe_B_Collection")
            for g in z["groupes"]:
                _bloc_b(gb, "Sortie_Groupe_B", g["index"], g["name"], [g], None, z.get("bbio_max"))
        # ---- Th-C
        ec = ET.SubElement(coll_c, "Sortie_Batiment_C")
        _val(ec, "Index", bat["index"])
        _val(ec, "Name", bat["name"])
        _val(ec, "O_SREF", round(sum(_surface(g) for g in groupes_bat), 2))
        cep = bat.get("cep") or {}
        for k, nom in (("cef_annuel", "O_Cef_annuel"), ("cep_annuel", "O_Cep_annuel"), ("cep_nr_annuel", "O_Cep_nr_annuel"), ("cep_max", "O_Cep_Max"), ("cep_nr_max", "O_Cep_nr_Max")):
            if cep.get(k) is not None:
                _val(ec, nom, round(float(cep[k]), 1))
        for poste in POSTES:
            v = (cep.get("imp") or {}).get(poste)
            if v is not None:
                _val(ec, f"O_Cef_imp_{poste.replace('aux_vent', 'auxvent').replace('aux_dist', 'auxdist')}_annuel", round(float(v), 1))
        for energie in ENERGIES:
            v = (cep.get("par_energie") or {}).get(energie)
            if v is not None:
                _val(ec, f"O_Cef_{energie}_imp_annuel", round(float(v), 1))
        pv = bat.get("pv")
        if pv:
            _val(ec, "O_Eef_Prod_PV_annuel", round(float(pv["prod"]), 1))
            _val(ec, "O_Eef_Prod_PV_AC_annuel", round(float(pv["ac"]), 1))
            _val(ec, "O_TAC_elec_PV_annuel", round(float(pv["tac"]), 1))
            _val(ec, "O_Eef_Elec_Exportee_annuel", round(float(pv["exportee"]), 1))
        zc = ET.SubElement(ec, "Sortie_Zone_C_Collection")
        for z in bat["zones"]:
            ez = ET.SubElement(zc, "Sortie_Zone_C")
            _val(ez, "Index", z["index"])
            _val(ez, "Name", z["name"])
            _val(ez, "O_SREF", round(sum(_surface(g) for g in z["groupes"]), 2))
            _val(ez, "O_SHAB", round(sum(float(g.get("shab") or 0.0) for g in z["groupes"]), 2))
            _val(ez, "O_SU", round(sum(float(g.get("su") or 0.0) for g in z["groupes"]), 2))
            if z.get("usage") is not None:
                _val(ez, "Usage", z["usage"])
            _val(ez, "O_Cef_annuel", round(_moyenne(z["groupes"], lambda g: sum(_cef(g, p) for p in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist"))), 1))
            for poste in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist"):
                _val(ez, f"O_Cef_imp_{poste.replace('aux_vent', 'auxvent').replace('aux_dist', 'auxdist')}_annuel", round(_moyenne(z["groupes"], lambda g, p=poste: _cef(g, p)), 1))
            gc = ET.SubElement(ez, "Sortie_Groupe_C_Collection")
            for g in z["groupes"]:
                _bloc_c_groupe(gc, g)
        # ---- Th-D
        ed = ET.SubElement(coll_d, "Sortie_Batiment_D")
        _val(ed, "Index", bat["index"])
        _val(ed, "Name", bat["name"])
        zd = ET.SubElement(ed, "Sortie_Zone_D_Collection")
        for z in bat["zones"]:
            ez = ET.SubElement(zd, "Sortie_Zone_D")
            _val(ez, "Index", z["index"])
            _val(ez, "Name", z["name"])
            _val(ez, "O_SREF", round(sum(_surface(g) for g in z["groupes"]), 2))
            gd = ET.SubElement(ez, "Sortie_Groupe_D_Collection")
            for g in z["groupes"]:
                _bloc_d_groupe(gd, g)
    return racine


def ecrire(chemin_entree: str | Path, sortie: ET.Element, chemin_sortie: str | Path) -> Path:
    """Recopie le RSEE d'entrée (Datas_Comp et Entree_Projet intacts) en remplaçant son bloc Sortie_Projet."""
    arbre = ET.parse(chemin_entree)
    racine = arbre.getroot()
    parent_de = {c: p for p in racine.iter() for c in p}
    ancien = next((e for e in racine.iter() if e.tag.split("}")[-1] == "Sortie_Projet"), None)
    if ancien is not None:
        parent = parent_de[ancien]
        i = list(parent).index(ancien)
        parent.remove(ancien)
        parent.insert(i, sortie)
    else:
        rset = next((e for e in racine.iter() if e.tag.split("}")[-1] == "RSET"), racine)
        rset.append(sortie)
    ET.indent(arbre, space=" ")
    chemin_sortie = Path(chemin_sortie)
    arbre.write(chemin_sortie, encoding="utf-8", xml_declaration=True)
    return chemin_sortie
