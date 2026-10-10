# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc de la consommation d'ECS (Th-C) : besoins (9.6) + pertes de distribution du groupe (9.7) alimentent, par
génération, l'assemblage ballon + générateurs (9.9, 9.10, 9.13, 9.14, 8.23 ECS, 8.18) ; la consommation électrique est
comparée à O_Cef_ecs_annuel des groupes (Sortie_Groupe_C).

    python -m banc.ecs_cef <fichier RSEE> [--rapide]

La comparaison se fait au niveau du projet (somme des générations contre somme des groupes) : un groupe peut être
desservi par plusieurs générations (émetteurs ECS à Rat_em_e partiel), ce qui rend la comparaison par génération
invalide. Les saisons effectives du bâtiment (8.4) donnent iECS_seule, qui conditionne l'imputation des auxiliaires à
charge nulle des PAC multiservices à l'ECS ; `--rapide` saute cette première passe (tout est alors « ECS seule »).

La température d'air des groupes est prise à 20 °C pour les pertes de distribution et l'air extrait (banc rapide, sans
simulation thermique) ; la distribution intergroupe est supposée sans perte (type 0).
"""
import sys

import numpy as np

from banc.besoins import METEO, zone_climatique
from banc.cep import saisons_batiment
from openbce import calendrier, climat, ecs, ecs_distribution, enveloppe, generateurs_ballon, meteo, rsee
from openbce import usages as mod_usages


class _Defaut(dict):
    """Dictionnaire dont les clés absentes renvoient une génération par défaut."""

    def __init__(self, d, defaut):
        super().__init__(d)
        self.defaut = defaut

    def get(self, k, d=None):
        return super().get(k, self.defaut)

    def __missing__(self, k):
        return self.defaut


def comparer(chemin: str, rapide: bool = False):
    p = rsee.lire(chemin)
    simu = p.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(p)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    n = len(cl.te)
    dps = {d.entier("Index"): d.entier("Id_Gen") for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    gens_mta = set()                                                     # réseaux mixtes MTA (16.8) : ECS comptée avec le chauffage (banc.pac_chauffage)
    for m in p.entree.tous("T5_Cardonnel_ModuleAppartement_Mixte"):
        dps[m.entier("Index")] = m.entier("Id_Gen", 0)
        gens_mta.add(m.entier("Id_Gen", 0))
    # RSEE sans nœud Distribution_Intergroupe_ECS (cas 15) : les émetteurs ECS sont rattachés à l'unique génération à ballon
    _gens_ballon = [g.entier("Index") for g in p.entree.directs("Generation") if g.directs("Production_Stockage")]
    if not dps and len(_gens_ballon) == 1:
        dps = _Defaut(dps, _gens_ballon[0])
    b_tampons = {}
    for bat in p.entree.directs("Batiment"):
        b_tampons.update(enveloppe.coefficients_b(bat))
    reseaux = {d.entier("Index"): ecs_distribution.Intergroupe.depuis(d, b_tampons) for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    demandes_dp = {}
    sorties = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g for b in p.sortie.tous("Sortie_Batiment_C")
               for z in b.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C")}
    demandes, ecs_seule = {}, {}
    ref = surface_tot = 0.0
    for bat in p.entree.directs("Batiment"):
        if rapide:
            seule = np.ones(n, dtype=bool)
        else:
            ch, fr = saisons_batiment(bat, cl, cal)
            jours = np.arange(n) // 24
            seule = np.ones(n, dtype=bool) if ch is None else ~(ch[jours] | fr[jours])
        for zone in bat.directs("Zone"):
            usage = zone.entier("Usage")
            if usage not in mod_usages.NOMS:
                continue
            for g in zone.directs("Groupe"):
                surface = g.nombre("SHAB" if usage in (1, 2) else "SU")
                try:
                    qw = ecs.besoins(g, usage, cal, cl.teau)
                except NotImplementedError:
                    continue
                pertes = ecs_distribution.pertes(ecs_distribution.troncons(g, usage, surface), qw, np.full(n, 20.0), cl.te)
                demande = qw + pertes
                s = sorties.get((bat.entier("Index"), zone.entier("Index"), g.entier("Index")))
                if s is not None:
                    ref += s.nombre("O_Cef_ecs_annuel", 0.0) * surface
                    surface_tot += surface
                for em in g.directs("Emetteur_ECS"):
                    for ds in em.directs("Distribution_Groupe_ECS"):
                        id_dp = ds.entier("Id_Dist_Primaire", 0)
                        demandes_dp[id_dp] = demandes_dp.get(id_dp, np.zeros(n)) + demande * em.nombre("Rat_em_e", 1.0)
                        ecs_seule[dps.get(id_dp, 0)] = seule
    # distribution intergroupe (9.8) : demande aux bornes de chaque génération, électricité des réchauffeurs et traceurs, circulateurs
    elec_reseau, circulateurs = {}, {}
    elec_reseau_h, circulateurs_h = {}, {}
    for id_dp, qw in demandes_dp.items():
        id_gen = dps.get(id_dp, 0)
        r = reseaux[id_dp].heure(qw, cl.te) if id_dp in reseaux else dict(qw_prim=qw, elec_ecs=np.zeros(n), circulateur=np.zeros(n))
        demandes[id_gen] = demandes.get(id_gen, np.zeros(n)) + r["qw_prim"]
        elec_reseau[id_gen] = elec_reseau.get(id_gen, 0.0) + float(r["elec_ecs"].sum())
        circulateurs[id_gen] = circulateurs.get(id_gen, 0.0) + float(r["circulateur"].sum())
        elec_reseau_h[id_gen] = elec_reseau_h.get(id_gen, np.zeros(n)) + np.asarray(r["elec_ecs"], dtype=float)
        circulateurs_h[id_gen] = circulateurs_h.get(id_gen, np.zeros(n)) + np.asarray(r["circulateur"], dtype=float)
    resultats = []
    for gen in p.entree.directs("Generation"):
        id_gen = gen.entier("Index")
        if id_gen not in demandes:
            continue
        if id_gen in gens_mta:
            resultats.append((id_gen, "MTA : ECS comptée avec le chauffage (16.8)", demandes[id_gen].sum(), None))
            continue
        ps_list = gen.directs("Production_Stockage")
        if not ps_list:
            resultats.append((id_gen, "sans ballon", demandes[id_gen].sum(), None))
            continue
        try:
            qm, t_lim = generateurs_ballon.debit_air_extrait(p.entree, gen)
            assemblage = generateurs_ballon.AssemblageECS.depuis(ps_list[0], gen.entier("Pos_Gen", 0), qm, t_lim)
        except NotImplementedError as e:
            resultats.append((id_gen, f"non traité : {e}", demandes[id_gen].sum(), None))
            continue
        t_depart = ecs_distribution.THETA_2ND                         # θdépart,aval = θdépart_prim-e = max θ2nd-e (1741, 1754, 1763), pas Theta_Wm_Ecs (ECS instantanée, 1010)
        elec = fourni = pertes_sto = gaz = 0.0
        heures = 0
        elec_h = np.zeros(n)
        seule = ecs_seule[id_gen]
        for h in range(n):
            r = assemblage.heure(float(demandes[id_gen][h]), float(cl.teau[h]), t_depart, float(cl.te[h]), int(cal.case[h]) - 1, bool(seule[h]))
            elec += r["elec"]; fourni += r["fourni"]; pertes_sto += r["pertes"]; gaz += r.get("gaz", 0.0)
            elec_h[h] = r["elec"]
            heures += r["elec"] > assemblage.nb * 50.0
        resultats.append((id_gen, assemblage, demandes[id_gen].sum(),
                          dict(elec=elec + elec_reseau.get(id_gen, 0.0), fourni=fourni, pertes=pertes_sto, nbh_report=assemblage.ballon.nbh_report, heures=heures,
                               h_seule=int(seule.sum()), elec_reseau=elec_reseau.get(id_gen, 0.0), circulateur=circulateurs.get(id_gen, 0.0), gaz=gaz,
                               elec_h=elec_h + elec_reseau_h.get(id_gen, np.zeros(n)), circulateur_h=circulateurs_h.get(id_gen, np.zeros(n)))))
    return resultats, ref, surface_tot


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    resultats, ref, surface = comparer(sys.argv[1], "--rapide" in sys.argv)
    total = 0.0
    for id_gen, asm, demande, r in resultats:
        if r is None:
            print(f"génération {id_gen} : {asm} | demande {demande / 1000:6.0f} kWh")
            continue
        total += r["elec"]
        print(f"génération {id_gen} : {type(asm.base).__name__} x{asm.nb}, appoint {type(asm.appoint).__name__ if asm.appoint else '-'} | demande {demande / 1000:6.0f} kWh | "
              f"fournie {r['fourni'] / 1000:6.0f} | pertes ballon {r['pertes'] / 1000:5.0f} | élec {r['elec'] / 1000:6.0f} kWh | COP apparent {(r['fourni'] + r['pertes']) / max(r['elec'], 1):.2f}"
              f" | {r['heures']} h de PAC, {r['nbh_report']} h de report, {r['h_seule']} h ECS seule | réseau : réchauffeur/traceur {r['elec_reseau'] / 1000:.0f} kWh, circulateur {r['circulateur'] / 1000:.0f} kWh")
    gaz_total = sum(r.get("gaz", 0.0) for _, _, _, r in resultats if r)
    if ref:
        print(f"PROJET : élec {total / 1000 / surface:5.2f} + gaz {gaz_total / 1000 / surface:5.2f} / RSEE {ref / surface:5.2f} kWh/m² ({(total + gaz_total) / 1000 / ref - 1:+.0%}) sur {surface:.0f} m²")
