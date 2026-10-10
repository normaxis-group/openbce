# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du refroidissement par PAC électrique (8.23 mode froid) des groupes climatisés : la demande horaire est la somme des
besoins de froid Th-C des groupes desservis (émetteurs froids, parts Rat_s_fr x Rat_t_fr, distribution fictive), la PAC
est appelée après le mode ECS du même pas (triple service, 1295), et l'électricité est comparée à O_Cef_fr_annuel des
groupes desservis.

    python -m banc.pac_froid <fichier RSEE>

Température aval : air du groupe (émetteurs à air, sys 2) ou Theta_Wm_Fr de la génération (sys 1, eau glacée).
Auxiliaires à charge nulle : au froid en saison de refroidissement (p. 796).
"""
import sys

import numpy as np

from banc.besoins import METEO, zone_climatique
from banc.cep import comparer as cep_comparer
from openbce import calendrier, climat, ecs, ecs_distribution, enveloppe, generateurs_ballon, meteo, rsee, thermodynamique as th


def comparer(chemin: str):
    p = rsee.lire(chemin)
    simu = p.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(p)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    n = len(cl.te)
    lignes = cep_comparer(chemin)
    groupes = {(d["bat"], d["zone_index"], d["groupe"]): (d, surface) for *_, surface, _a, _ar, _e, _er, _ch, _chr, _fr, _frr, _e1, _e2, _e3, d in lignes}
    gens = {g.entier("Index"): g for g in p.entree.directs("Generation")}
    dfr = {d.entier("Index"): d.entier("Id_Gen") for d in p.entree.tous("Distribution_Intergroupe_Froid")}
    decs = {d.entier("Index"): d.entier("Id_Gen") for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    b_tampons = {}
    for bat in p.entree.directs("Batiment"):
        b_tampons.update(enveloppe.coefficients_b(bat))
    reseaux = {d.entier("Index"): ecs_distribution.Intergroupe.depuis(d, b_tampons) for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    qfr, qecs_dp, desservis, saison_fr = {}, {}, {}, {}
    for cle, (d, surface) in groupes.items():
        g = d["noeud"]
        if g.entier("Is_Climatise", 0) != 1:
            continue
        ems = [(em, em.nombre("Rat_s_fr", 0.0) * em.nombre("Rat_t_fr", 0.0)) for em in g.directs("Emetteur") if em.entier("Is_emetteur_froid", 0) == 1]
        total = sum(r for _, r in ems) or 1.0
        parts = {}
        for em, r in ems:
            for x in em.tous("Distribution_Groupe_Froid"):
                i = dfr.get(x.entier("Id_Dist_1re", 0), 0)
                parts[i] = parts.get(i, 0.0) + r / total
        for i, part in parts.items():
            qfr[i] = qfr.get(i, np.zeros(n)) + np.abs(d["fr_h"]) * part
            desservis.setdefault(i, []).append((cle, d, surface * part))
            fr_j = np.isin(d["saison"], (1, 4))
            saison_fr[i] = fr_j if i not in saison_fr else (saison_fr[i] | fr_j)
    for cle, (d, surface) in groupes.items():
        g = d["noeud"]
        try:
            qw = ecs.besoins(g, d["usage"], cal, cl.teau)
            dem = qw + ecs_distribution.pertes(ecs_distribution.troncons(g, d["usage"], surface), qw, d["theta_i"] if d["theta_i"] is not None else np.full(n, 20.0), cl.te)
            for em in g.directs("Emetteur_ECS"):
                for ds in em.directs("Distribution_Groupe_ECS"):
                    i = ds.entier("Id_Dist_Primaire", 0)
                    qecs_dp[i] = qecs_dp.get(i, np.zeros(n)) + dem * em.nombre("Rat_em_e", 1.0)
        except NotImplementedError:
            pass
    qecs = {}
    for i, qw in qecs_dp.items():
        r = reseaux[i].heure(qw, cl.te) if i in reseaux else dict(qw_prim=qw)
        qecs[decs.get(i, 0)] = qecs.get(decs.get(i, 0), np.zeros(n)) + r["qw_prim"]
    resultats = []
    jours = np.arange(n) // 24
    for id_gen, gen in gens.items():
        if id_gen not in qfr:
            continue
        pac_noeud = assemblage = None
        for ps in gen.directs("Production_Stockage"):
            for c in ps.enfants:
                if c.nom.startswith("Source_Ballon_Base_Thermodynamique_Elec_") and c.nom.endswith("Service"):
                    pac_noeud = c
            if pac_noeud is not None:
                qm, t_lim = generateurs_ballon.debit_air_extrait(p.entree, gen)
                assemblage = generateurs_ballon.AssemblageECS.depuis(ps, gen.entier("Pos_Gen", 0), qm, t_lim)
        for c in gen.enfants:
            if c.nom.startswith("Generateur_Thermodynamique"):
                pac_noeud = c
        reseau_froid = next((c for c in gen.enfants if c.nom == "Generateur_Reseau_Fourniture" and c.entier("Id_Fou_Gen", 1) == 2), None)
        if reseau_froid is not None:
            # réseau de froid (8.28, type 601) : fourniture bornée par PEss, pertes de sous-station nulles (1484), énergie « réseau »
            from openbce import reseau_fourniture
            rf = reseau_fourniture.ReseauFourniture.depuis(reseau_froid)
            fr_j = saison_fr[id_gen]
            fourni = report = heures = 0.0
            for h in range(n):
                q = (float(qfr[id_gen][h]) + report) if bool(fr_j[min(jours[h], len(fr_j) - 1)]) else 0.0
                fou = min(q, rf.rdim * 1000.0 * rf.p_ess)                            # (1469), (1470)
                fourni += fou; report = q - fou; heures += fou > 0
            surface = sum(s for _, _, s in desservis[id_gen])
            ref = sum(d["cef_fr_ref"] * s for _, d, s in desservis[id_gen] if d["cef_fr_ref"] == d["cef_fr_ref"])
            resultats.append((id_gen, "réseau de froid", dict(sys=0, demande=float(qfr[id_gen].sum()), fourni=fourni, elec=0.0, reseau=fourni, heures=heures,
                                                             surface=surface, ref=ref, report=report, groupes=[d["zone_index"] for _, d, _ in desservis[id_gen]])))
            continue
        if pac_noeud is None:
            resultats.append((id_gen, "pas de générateur thermodynamique de froid", None))
            continue
        try:
            pac = th.Pac.depuis(pac_noeud)
        except NotImplementedError as e:
            resultats.append((id_gen, f"non traité : {e}", None))
            continue
        if th.FR not in pac.modes:
            resultats.append((id_gen, "PAC sans mode froid lisible", None))
            continue
        sys_fr = pac.modes[th.FR].sys
        t_wm = gen.nombre("Theta_Wm_Fr", 7.0) or 7.0
        theta_groupes = [d["theta_i"] for _, d, _ in desservis[id_gen] if d["theta_i"] is not None]
        t_air = np.mean(theta_groupes, axis=0) if theta_groupes else np.full(n, 26.0)
        fr_j = saison_fr[id_gen]
        demande_ecs = qecs.get(id_gen, np.zeros(n))
        elec = fourni = heures = 0.0
        report = 0.0
        elec_h = np.zeros(n)
        for h in range(n):
            en_saison = bool(fr_j[min(jours[h], len(fr_j) - 1)])
            rfonct = 0.0
            if assemblage is not None:
                assemblage.heure(float(demande_ecs[h]), float(cl.teau[h]), ecs_distribution.THETA_2ND, float(cl.te[h]), int(cal.case[h]) - 1, False)
                rfonct = getattr(assemblage.base, "dernier_lr", 0.0)
            q = (float(qfr[id_gen][h]) + report) if en_saison else 0.0
            t_aval = float(t_air[h]) if sys_fr == 2 else t_wm
            r = pac.heure(th.FR, q, float(cl.te[h]), t_aval, rfonct_ecs=rfonct, part_waux0=(1.0 - rfonct) if en_saison else 0.0)
            elec += r["elec"]; fourni += r["fourni"]; heures += r["lr"] > 0
            report = r["rest"]
            elec_h[h] = r["elec"]
        surface = sum(s for _, _, s in desservis[id_gen])
        ref = sum(d["cef_fr_ref"] * s for _, d, s in desservis[id_gen] if d["cef_fr_ref"] == d["cef_fr_ref"])
        resultats.append((id_gen, pac_noeud.nom.replace("Source_Ballon_Base_Thermodynamique_Elec_", "ballon ").replace("Generateur_Thermodynamique_Elec_", "PAC "),
                          dict(sys=sys_fr, demande=float(qfr[id_gen].sum()), fourni=fourni, elec=elec, heures=heures, surface=surface, ref=ref, report=report,
                               groupes=[d["zone_index"] for _, d, _ in desservis[id_gen]], elec_h=elec_h)))
    return resultats


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tot = ref_tot = 0.0
    for id_gen, nom, r in comparer(sys.argv[1]):
        if r is None:
            print(f"génération {id_gen} : {nom}")
            continue
        s = r["surface"]
        print(f"génération {id_gen} : {nom} sys {r['sys']} | zones {r['groupes']} | demande {r['demande'] / 1000:6.0f} kWh | fournie {r['fourni'] / 1000:6.0f}"
              f" | élec {r['elec'] / 1000 / s:5.2f} / RSEE {r['ref'] / s:5.2f} kWh/m² ({r['elec'] / 1000 / r['ref'] - 1 if r['ref'] else 0:+.0%}) | EER {r['fourni'] / max(r['elec'], 1):.2f} | {r['heures']:.0f} h | report final {r['report'] / 1000:.0f} kWh")
        tot += r["elec"]; ref_tot += r["ref"]
    if ref_tot:
        print(f"PROJET : froid {tot / 1000:.0f} / RSEE {ref_tot:.0f} kWh ({tot / 1000 / ref_tot - 1:+.0%})")
