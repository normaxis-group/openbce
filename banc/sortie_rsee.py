# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Produit le RSEE de sortie d'un projet (Datas_Comp et Entree_Projet recopiés, Sortie_Projet recalculé) et le compare
au RSEE de référence : python -m banc.sortie_rsee <rsee.xml> [chemin de sortie]

Première version : Th-B par groupe, besoins Th-C par groupe, Cep du bâtiment (banc.cep_total), consommations par poste
réparties entre les groupes au prorata de leurs besoins (les générations sont partagées), degrés-heures (banc.confort).
"""
import dataclasses
import sys
from pathlib import Path

import numpy as np

from banc import cep as banc_cep, cep_total, confort
from banc.besoins import METEO, zone_climatique
from openbce import aeraulique, calendrier, climat, enveloppe, exigences, groupe, meteo, rsee, scenarios, sortie_rsee
from openbce import usages as mod_usages


def calculer(chemin: str) -> dict:
    projet = rsee.lire(chemin)
    simu = projet.entree.un("Simu")
    zone_clim = zone_climatique(projet)
    cl = climat.du_site(meteo.charger(METEO, zone_clim), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    # Th-C par groupe et Cep du projet
    thc = {(d["bat"], d["zone_index"], d["groupe"]): (aux, ecl, ecs_tot, d) for *_, aux, _ar, ecl, _er, _ch, _chr, _fr, _frr, ecs_tot, _b, _c, d in banc_cep.comparer(chemin)}
    total = cep_total.comparer(chemin)
    dh = {(zn, gn): (b_dh, nb) for zn, gn, _u, _s, b_dh, _ref, nb, *_ in confort.comparer(chemin)}
    dates = [d.texte("date_depot_PC") for d in [projet.administratif] + list(projet.administratif.tous("Datas_Comp")) if d.texte("date_depot_PC")]
    depot = dates[0] if dates else ""
    annee = int(depot[:4]) if depot[:4].isdigit() else (int(projet.version_rsee[:4]) if projet.version_rsee[:4].isdigit() else 2026)
    sref_usage = {}
    for zone in projet.entree.tous("Zone"):
        u = zone.entier("Usage")
        sref_usage[u] = sref_usage.get(u, 0.0) + sum(g.nombre("SHAB") if u in (1, 2) else g.nombre("SU") for g in zone.directs("Groupe"))
    # poids pour répartir les consommations du projet entre les groupes : besoin x surface
    poids = {}
    for cle, (aux, ecl, ecs_tot, d) in thc.items():
        s = d["noeud"].nombre("SHAB") if d["usage"] in (1, 2) else d["noeud"].nombre("SU")
        poids[cle] = dict(ch=float(np.sum(d["mois"])) * s, fr=float(np.sum(d["fr_mois"])) * s, ecs=(ecs_tot or 0.0) * s, s=s)
    somme = {k: sum(p[k] for p in poids.values()) or 1.0 for k in ("ch", "fr", "ecs")}
    gaz_ch = max(total.get("gaz", 0.0) * total["sref"] - (total["postes"].get("ecs_gaz", 0.0)), 0.0)
    batiments, zones_ignorees = [], []
    for bat in projet.entree.directs("Batiment"):
        b_tampons = enveloppe.coefficients_b(bat)
        zones = []
        for zone in bat.directs("Zone"):
            usage = zone.entier("Usage")
            if usage not in mod_usages.NOMS:
                zones_ignorees.append(dict(batiment=bat.texte("Name"), zone=zone.texte("Name"), usage=usage, motif="usage non pris en charge par le moteur"))
                continue
            groupes = zone.directs("Groupe")
            cle_s = "SHAB" if usage in (1, 2) else "SU"
            surface_zone = sum(g.nombre(cle_s) for g in groupes)
            nb_log = max(zone.entier("NB_logement", 1), 1)
            sc = scenarios.habitation(cal, usage, surface_zone, nb_log) if usage in (1, 2) else scenarios.tertiaire(cal, usage, surface_zone)
            gs = []
            for g in groupes:
                s = g.nombre(cle_s)
                part = s / surface_zone
                sc_g = dataclasses.replace(sc, occupants=sc.occupants * part, apports_occupants=sc.apports_occupants * part,
                                           apports_usages=sc.apports_usages * part, nadeq=sc.nadeq * part)
                b = groupe.calculer(g, usage, cl, cal, sc_g, b_tampons, aeraulique.du_groupe(zone, g))
                mois = lambda x: [float(x[cal.mois_civil == m].sum()) / 1000 / s for m in range(1, 13)]
                cle = (bat.entier("Index"), zone.entier("Index"), g.entier("Index"))
                aux, ecl, ecs_tot, d = thc.get(cle, (0.0, None, 0.0, None))
                p = poids.get(cle, dict(ch=0.0, fr=0.0, ecs=0.0, s=s))
                cef = dict(ch=total["postes"]["ch"] * p["ch"] / somme["ch"] / s, fr=total["postes"]["fr"] * p["fr"] / somme["fr"] / s,
                           ecs=total["postes"]["ecs"] * p["ecs"] / somme["ecs"] / s, ecl=ecl or 0.0, aux_vent=aux or 0.0,
                           aux_dist=total["postes"]["aux_dist"] * p["s"] / total["sref"] / s)
                gaz_ch_g = gaz_ch * p["ch"] / somme["ch"] / s
                gaz_ecs_g = total["postes"].get("ecs_gaz", 0.0) * p["ecs"] / somme["ecs"] / s
                cef_energie = {("ch", "elec"): cef["ch"] - gaz_ch_g, ("ch", "gaz"): gaz_ch_g, ("fr", "elec"): cef["fr"],
                               ("ecs", "elec"): cef["ecs"] - gaz_ecs_g, ("ecs", "gaz"): gaz_ecs_g}
                b_dh, nb = dh.get((zone.texte("Name"), g.texte("Name")), (None, None))
                gs.append(dict(index=g.entier("Index"), name=g.texte("Name"), sref=s, shab=s if usage in (1, 2) else 0.0, su=s if usage >= 3 else 0.0,
                               climatise=g.entier("Is_Climatise", 0) == 1, b_ch_mois=mois(b.chauffage), b_fr_mois=mois(b.refroidissement), b_ecl_mois=mois(b.eclairage),
                               c_b_ch_mois=list(d["mois"]) if d is not None else [0.0] * 12, c_b_fr_mois=list(d["fr_mois"]) if d is not None else [0.0] * 12,
                               c_b_ecs=ecs_tot or 0.0, cef=cef, cef_energie=cef_energie, dh=b_dh, nb_h_inconf=nb,
                               dh_max=exigences.dh_max(usage, zone_clim, g.entier("Categorie_CE", 1), g.entier("Is_Climatise", 0) == 1, surface_zone / nb_log)))
            g0 = groupes[0]
            bbio_max = exigences.bbio_max(usage, zone_clim, simu.nombre("Altitude"), surface_zone, nb_log, sref_usage[usage],
                                          g0.nombre("S_combles", 0), g0.entier("Exp_BR_Groupe", 1) or 3, g0.entier("Categorie_CE", 1), annee)
            zones.append(dict(index=zone.entier("Index"), name=zone.texte("Name"), usage=usage, nb_logements=nb_log, bbio_max=bbio_max, groupes=gs))
        s_bat = sum(g["sref"] for z in zones for g in z["groupes"])
        imp = {k: total["postes"][k] / total["sref"] for k in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist")}
        imp["deplacement"] = total["postes"].get("dep", 0.0) / total["sref"]
        batiments.append(dict(index=bat.entier("Index"), name=bat.texte("Name"), zones=zones,
                              cep=dict(cef_annuel=sum(imp.values()), cep_annuel=total["cep"], imp=imp,
                                       par_energie=dict(elec=sum(imp.values()) - total.get("gaz", 0.0), gaz=total.get("gaz", 0.0)))))
    return dict(name=Path(chemin).stem, batiments=batiments, zones_ignorees=zones_ignorees, version=projet.version_moteur, departement=simu.texte("Departement"), altitude=simu.nombre("Altitude"))


CHAMPS_COMPARES = (("Sortie_Batiment_B", ("O_B_Ch_annuel", "O_B_Fr_annuel", "O_B_Ecl_annuel", "O_Bbio_pts_annuel")),
                   ("Sortie_Zone_B", ("O_Bbio_Max",)),
                   ("Sortie_Batiment_C", ("O_Cef_annuel", "O_Cep_annuel", "O_Cef_imp_ch_annuel", "O_Cef_imp_fr_annuel", "O_Cef_imp_ecs_annuel", "O_Cef_imp_ecl_annuel", "O_Cef_imp_auxvent_annuel")),
                   ("Sortie_Groupe_C", ("O_B_Ch_annuel", "O_B_Fr_annuel", "O_Cef_ch_annuel", "O_Cef_ecs_annuel")),
                   ("Sortie_Groupe_D", ("O_NbDegresHeures", "O_NbDegresHeures_max")))


def ecarts(ref: rsee.Projet, calc: rsee.Projet) -> list[dict]:
    """Écarts champ par champ entre les sorties de référence et celles d'OpenBCE (écart relatif None si référence nulle)."""
    lignes = []
    for bloc, champs in CHAMPS_COMPARES:
        for r, c in zip(ref.sortie.tous(bloc), calc.sortie.tous(bloc)):
            for ch in champs:
                a, b = r.nombre(ch, float("nan")), c.nombre(ch, float("nan"))
                lignes.append(dict(bloc=bloc, nom=r.texte("Name"), champ=ch, openbce=b, reference=a,
                                   ecart=round(b / a - 1, 4) if a and a == a and b == b else None))
    return lignes


def comparer(ref: rsee.Projet, calc: rsee.Projet) -> list[str]:
    return [f"{e['bloc']:18s} {e['nom'][:24]:24s} {e['champ']:28s} calc {e['openbce']:8.1f}  ref {e['reference']:8.1f}  {(e['ecart'] or 0):+.1%}"
            for e in ecarts(ref, calc)]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    chemin = sys.argv[1]
    sortie = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(chemin).with_name(Path(chemin).stem + "_openbce.xml")
    calcul = calculer(chemin)
    el = sortie_rsee.construire(calcul, calcul["version"], calcul["departement"], calcul["altitude"])
    sortie_rsee.ecrire(chemin, el, sortie)
    print("écrit :", sortie)
    for l in comparer(rsee.lire(chemin), rsee.lire(sortie)):
        print(l)
