# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du Cep complet d'un projet tout électrique : chauffage (PAC et effet joule, banc.pac_chauffage), ECS (banc.ecs_cef),
éclairage et auxiliaires de ventilation (banc.cep), circulateurs des réseaux ECS, forfait de refroidissement des groupes
non climatisés (13.3, avec les degrés-heures du RSEE faute de Th-D dans ce banc), contre O_Cep_annuel du bâtiment.

    python -m banc.cep_total <fichier RSEE>

Les groupes climatisés (froid réel) et les générateurs à combustion ou réseau ne sont pas modélisés : le projet est
alors signalé et la part manquante lue dans le RSEE pour que le reste soit comparable.
"""
import collections
import sys

import numpy as np

from banc import ecs_cef, pac_chauffage, pac_froid
from banc.besoins import METEO, zone_climatique
from banc.cep import comparer as cep_comparer
from openbce import bilans, climat, meteo, photovoltaique, rsee

COEF_EP_ELEC = 2.3


def comparer(chemin: str) -> dict:
    p = rsee.lire(chemin)
    simu = p.entree.un("Simu")
    zone_clim = climat.ZONE_CLIMATIQUE.get(climat.departement(simu.texte("Departement")))
    alt = simu.nombre("Altitude", 0.0)
    lignes = cep_comparer(chemin)
    sref = sum(b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C"))
    cep_ref = sum(b.nombre("O_Cep_annuel", 0.0) * b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C")) / sref
    dh = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g for b in p.sortie.tous("Sortie_Batiment_D") for z in b.tous("Sortie_Zone_D") for g in z.tous("Sortie_Groupe_D")}
    postes = dict(ch=0.0, ecs=0.0, ecl=0.0, aux_vent=0.0, aux_dist=0.0, fr=0.0)
    ref = dict(ch=0.0, ecs=0.0, ecl=0.0, aux_vent=0.0, aux_dist=0.0, fr=0.0)
    non_modelise = []
    n = 8760
    w_elec = collections.defaultdict(lambda: np.zeros(n))     # par bâtiment : électricité consommée par heure, postes hors mobilier, Wh (13.4)
    w_mob = collections.defaultdict(lambda: np.zeros(n))      # par bâtiment : usages mobiliers, Wh (4.7)
    zone_bat = {}                                             # index de zone -> (index de bâtiment, surface)
    sref_bat = {b.entier("Index"): b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C")}

    def repartir(serie, groupes=None):
        """Ajoute une série horaire aux bâtiments : selon les zones desservies si on les connaît, sinon au prorata des SREF."""
        poids = {}
        for z in groupes or ():
            if z in zone_bat:
                b, surf = zone_bat[z]
                poids[b] = poids.get(b, 0.0) + surf
        if not poids:
            poids = dict(sref_bat)
        total = sum(poids.values()) or 1.0
        for b, x in poids.items():
            w_elec[b] += serie * (x / total)
    for *_, surface, aux, aux_ref, ecl, ecl_ref, ch, ch_ref, fr, fr_ref, e1, e2, e3, d in lignes:
        postes["aux_vent"] += aux * surface; ref["aux_vent"] += aux_ref * surface
        zone_bat.setdefault(d["zone_index"], (d["bat"], 0.0))
        zone_bat[d["zone_index"]] = (d["bat"], zone_bat[d["zone_index"]][1] + surface)
        w_elec[d["bat"]] += d["aux_h"]
        w_mob[d["bat"]] += d["mob_h"]
        if ecl is not None:
            postes["ecl"] += ecl * surface; ref["ecl"] += ecl_ref * surface
            w_elec[d["bat"]] += d["ecl_h"]
        s = next((g for (b, z, gi), g in dh.items() if (b, z, gi) == (d["bat"], d["zone_index"], d["groupe"])), None)
        g = d["noeud"]
        fr_ref_g = d["cef_fr_ref"] if d["cef_fr_ref"] == d["cef_fr_ref"] else 0.0
        ref["fr"] += fr_ref_g * surface
        if g.entier("Is_Climatise", 0) == 0 and s is not None and zone_clim is not None and d["usage"] in bilans.COEF_FR_PAR_DH:
            # forfait de froid (13.3) : étalé sur les heures de refroidissement du groupe, à défaut uniformément
            forfait = bilans.forfait_froid(d["usage"], False, s.nombre("O_NbDegresHeures", 0.0), s.nombre("O_NbDegresHeures_max", 0.0) or None, zone_clim, alt) * surface
            postes["fr"] += forfait
            poids = np.asarray(d["fr_h"], dtype=float)
            w_elec[d["bat"]] += forfait * 1000 * (poids / poids.sum() if poids.sum() > 0 else np.full(n, 1.0 / n))
        else:
            postes["fr"] += fr_ref_g * surface
            w_elec[d["bat"]] += fr_ref_g * surface * 1000 / n
            if g.entier("Is_Climatise", 0) == 1:
                non_modelise.append(f"froid réel groupe {d['zone_index']}.{d['groupe']}")
        ref["ch"] += (d["cef_ch_ref"] if d["cef_ch_ref"] == d["cef_ch_ref"] else 0.0) * surface
    # chauffage (et ECS des chaudières, comptée dans le poste ECS)
    gaz = 0.0
    ecs_chaudieres = 0.0
    for id_gen, nom, r in pac_chauffage.comparer(chemin):
        if r is None:
            non_modelise.append(f"chauffage génération {id_gen} ({nom})")
            continue
        postes["ch"] += (r["elec_pac"] + r["elec_joule"]) / 1000
        repartir(r.get("elec_h", np.zeros(n)), r.get("groupes"))
        if "gaz" in r:
            postes["ch"] += (r["gaz"] - r["gaz_ecs"]) / 1000
            postes["ecs"] += r["gaz_ecs"] / 1000
            ecs_chaudieres += r["gaz_ecs"]
            gaz += r["gaz"] / 1000
    # froid réel des groupes climatisés : la PAC remplace la valeur lue dans le RSEE
    for id_gen, nom, r in pac_froid.comparer(chemin):
        if r is not None and r["ref"] == r["ref"]:
            postes["fr"] += (r["elec"] + r.get("reseau", 0.0)) / 1000 - r["ref"]
            repartir(r.get("elec_h", np.zeros(n)) - r["ref"] * 1000 / n, r.get("groupes"))
            gaz += r.get("reseau", 0.0) / 1000                                   # énergie réseau : coefficient 1 comme le gaz
            non_modelise = [x for x in non_modelise if not x.startswith("froid réel")]
    # ECS
    resultats, ref_ecs, surf_ecs = ecs_cef.comparer(chemin)
    demande_ecs_tot = sum(d for _, _, d, _ in resultats) or 1.0
    for id_gen, asm, demande, r in resultats:
        if r is None:
            if asm == "sans ballon" and ecs_chaudieres > 0:
                # production instantanée par une chaudière double service : son ECS est déjà comptée avec le chauffage
                # (gaz_ecs). Sans ce test, cas 24, cas 09 et cas 25 la comptaient deux fois (cas 24 : Cep 58,8 -> 102,2).
                continue
            # génération non modélisée (ballon sans source dans le RSEE, assemblage non traité) : la valeur de la référence
            # est prise au prorata de la demande, comme pour le froid réel, et le cas est signalé
            non_modelise.append(f"ECS génération {id_gen} ({asm})")
            postes["ecs"] += ref_ecs * demande / demande_ecs_tot
            repartir(np.full(n, ref_ecs * demande / demande_ecs_tot * 1000 / n))
            continue
        postes["ecs"] += (r["elec"] + r.get("gaz", 0.0)) / 1000
        gaz += r.get("gaz", 0.0) / 1000
        postes["aux_dist"] += r["circulateur"] / 1000
        repartir(r.get("elec_h", np.zeros(n)) + r.get("circulateur_h", np.zeros(n)))
    ref["ecs"] = ref_ecs
    for b in p.sortie.tous("Sortie_Batiment_C"):
        for z in b.tous("Sortie_Zone_C"):
            for g in z.tous("Sortie_Groupe_C"):
                ref["aux_dist"] += g.nombre("O_Cef_aux_distribution_annuel", 0.0) * (g.nombre("O_SHAB", 0.0) or g.nombre("O_SU", 0.0))
        # déplacements (ascenseurs, parkings) : pris du RSEE, hors de ce banc
        dep = b.nombre("O_Cef_imp_deplacement_annuel", 0.0) * b.nombre("O_SREF", 0.0)
        postes["dep"] = postes.get("dep", 0.0) + dep; ref["dep"] = ref.get("dep", 0.0) + dep
        w_elec[b.entier("Index")] += dep * 1000 / n                          # profil horaire non calculé : uniforme
    cef = sum(postes.values())
    pv = sum(b.nombre("O_Cef_elec_AC_ecs_annuel", 0.0) * b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C")) / sref
    # production photovoltaïque et autoconsommation (13.4, 2525 à 2534) : minimum horaire de la production et de la consommation
    # électrique tous usages, mobilier compris ; la part autoconsommée réduit les imports de chaque poste au prorata (2531), donc
    # l'import hors mobilier vaut (W hors mobilier) x (1 - taux d'autoproduction). Projet pris en bloc (2526 : la production
    # du projet est répartie entre bâtiments au prorata de leurs consommations, ce qui revient au même).
    pv_prod, pv_ac = np.zeros(n), np.zeros(n)
    ac_hors_mob = 0.0                                                        # kWh autoconsommés par les postes du Cep
    pv_par_bat = {}                                                          # index de bâtiment -> (production, autoconsommée, dont postes du Cep), kWh
    pv_projet = [i for i in p.entree.tous("PV_install") if not any(i is j for bat in p.entree.directs("Batiment") for j in bat.tous("PV_install"))]
    if pv_projet or any(bat.tous("PV_install") for bat in p.entree.directs("Batiment")):
        cl = climat.du_site(meteo.charger(METEO, zone_climatique(p)), simu.texte("Departement"), alt)
        # installations déclarées au niveau du projet (2525, 2526) : réparties entre bâtiments au prorata des consommations horaires
        prod_projet = np.zeros(n)
        for inst in pv_projet:
            for o in inst.directs("Onduleur_PV"):
                prod_projet += photovoltaique._onduleur(cl, o)
        w_projet = sum((w_elec[b.entier("Index")] + w_mob[b.entier("Index")]) for b in p.entree.directs("Batiment"))
        for bat in p.entree.directs("Batiment"):
            w_e, w_m = w_elec[bat.entier("Index")], w_mob[bat.entier("Index")]
            prod = photovoltaique.du_batiment(bat, cl) + prod_projet * np.divide(w_e + w_m, w_projet, out=np.zeros(n), where=w_projet > 0)
            w_tous = w_e + w_m
            ac = np.minimum(prod, w_tous)
            tap = np.divide(ac, w_tous, out=np.zeros(n), where=w_tous > 0)
            ac_hors_mob += float((w_e * tap).sum()) / 1000
            pv_prod += prod
            pv_ac += ac
            pv_par_bat[bat.entier("Index")] = (float(prod.sum()) / 1000, float(ac.sum()) / 1000, float((w_e * tap).sum()) / 1000)
    w_elec_total = sum(w_elec.values()) if w_elec else np.zeros(n)
    pv_ref = sum(b.nombre("O_Eef_Prod_PV_annuel", 0.0) * b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C")) / sref
    pv_ac_ref = sum(b.nombre("O_Eef_Prod_PV_AC_annuel", 0.0) * b.nombre("O_SREF", 0.0) for b in p.sortie.tous("Sortie_Batiment_C")) / sref
    # énergie primaire : 2,3 pour l'électricité, 1 pour le gaz (tableau 252) ; la référence par poste est séparée de même
    ref_gaz = sum((g.nombre("O_Cef_ch_gaz_annuel", 0.0) + g.nombre("O_Cef_ecs_gaz_annuel", 0.0) + g.nombre("O_Cef_ch_reseau_annuel", 0.0) + g.nombre("O_Cef_ecs_reseau_annuel", 0.0)
                   + g.nombre("O_Cef_fr_reseau_annuel", 0.0)) * (g.nombre("O_SHAB", 0.0) or g.nombre("O_SU", 0.0))
                  for b in p.sortie.tous("Sortie_Batiment_C") for z in b.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C"))
    return dict(sref=sref, postes=postes, ref=ref, cep=(COEF_EP_ELEC * (cef - gaz) + gaz) / sref, cep_ref=cep_ref,
                cep_pv=(COEF_EP_ELEC * (cef - gaz - ac_hors_mob) + gaz) / sref,
                pv_prod=float(pv_prod.sum()) / 1000 / sref, pv_ac_calc=float(pv_ac.sum()) / 1000 / sref, pv_ref=pv_ref, pv_ac_ref=pv_ac_ref, pv_par_bat=pv_par_bat,
                w_elec_annuel=float(w_elec_total.sum()) / 1000 / sref, cef_elec_annuel=(cef - gaz) / sref,
                cep_ref_postes=(COEF_EP_ELEC * (sum(ref.values()) - ref_gaz) + ref_gaz) / sref, pv_ac=pv, non_modelise=non_modelise, gaz=gaz / sref, ref_gaz=ref_gaz / sref)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r = comparer(sys.argv[1])
    s = r["sref"]
    for k in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist", "dep"):
        print(f"  {k:9s} Cef {r['postes'][k] / s:6.2f} / RSEE {r['ref'][k] / s:6.2f} kWh/m²")
    print(f"  Cep {r['cep']:6.1f} / RSEE hors PV {r['cep_ref_postes']:6.1f} kWhep/m² ({r['cep'] / r['cep_ref_postes'] - 1:+.0%}) ; avec autoconsommation PV : {r['cep_pv']:6.1f} / O_Cep_annuel {r['cep_ref']:6.1f} ({r['cep_pv'] / r['cep_ref'] - 1:+.0%})"
          f" | non modélisé : {sorted(set(r['non_modelise'])) or 'rien'}")
    print(f"  PV production {r['pv_prod']:5.2f} / RSEE {r['pv_ref']:5.2f} ; autoconsommée {r['pv_ac_calc']:5.2f} / RSEE {r['pv_ac_ref']:5.2f} kWh/m² ; électricité horaire sommée {r['w_elec_annuel']:6.2f} pour Cef élec {r['cef_elec_annuel']:6.2f}")
