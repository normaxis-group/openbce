# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du chauffage par PAC électrique (8.23 modes chauffage) : pour chaque génération dont le générateur de chauffage
est thermodynamique (base de ballon double ou triple service, Generateur_Thermodynamique_Elec_*), la demande horaire
est la somme des besoins Th-C des groupes desservis (distribution fictive sans perte), la PAC est appelée après le mode
ECS du même pas (Rfonct_ecs, 1294), le reste va à l'appoint à effet joule de la génération (cascade), et l'électricité
du chauffage (PAC + appoint) est comparée à O_Cef_ch_annuel des groupes desservis.

    python -m banc.pac_chauffage <fichier RSEE>

Températures : amont = air extérieur ; aval = air du groupe (sys 2, air recyclé) ou Theta_Wm_Ch de la génération
(sys 1 air/eau, en attendant la distribution hydraulique). Auxiliaires à charge nulle : à l'ECS hors saisons, au
chauffage en saison de chauffage (p. 796).
"""
import sys

import numpy as np

from banc.besoins import METEO, zone_climatique
from banc.cep import comparer as cep_comparer
from openbce import calendrier, chaudiere, climat, distribution, ecs, ecs_distribution, enveloppe, generateurs, generateurs_ballon, meteo, reseau_fourniture, rsee, thermodynamique as th


# Récupération des pertes de réseau (11.1) dans ce banc sans rebouclage thermique : « net » = besoin diminué des pertes
# récupérées pour tous les émetteurs, génération chargée des pertes brutes ; « brut » = besoin brut, génération chargée
# des seules pertes non récupérées (hors volume, 40 % de l'intergroupe).
MODE_RECUP = "net"
ITERATIONS_RECUP = 2          # nombre d'itérations de la pré-passe des réseaux
AMORTISSEMENT = 0.0           # part de l'itération précédente conservée dans les pertes récupérées


class _Defaut(dict):
    """Dictionnaire dont les clés absentes renvoient une génération par défaut."""

    def __init__(self, d, defaut):
        super().__init__(d)
        self.defaut = defaut

    def get(self, k, d=None):
        return super().get(k, self.defaut)

    def __missing__(self, k):
        return self.defaut


def comparer(chemin: str):
    p = rsee.lire(chemin)
    simu = p.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(p)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    n = len(cl.te)
    lignes = cep_comparer(chemin)                                    # besoins Th-C horaires par groupe, avec saisons effectives
    groupes = {(d["bat"], d["zone_index"], d["groupe"]): (d, surface) for *_, surface, _a, _ar, _e, _er, _ch, _chr, _fr, _frr, _e1, _e2, _e3, d in lignes}
    gens = {g.entier("Index"): g for g in p.entree.directs("Generation")}
    dch = {d.entier("Index"): d.entier("Id_Gen") for d in p.entree.tous("Distribution_Intergroupe_Chaud")}
    # RSEE dont certains réseaux intergroupes manquent (cas 15 : Id_Dist_1re 3 absent) : rattachés à l'unique génération à ballon
    _gens_ballon = [g.entier("Index") for g in p.entree.directs("Generation") if g.directs("Production_Stockage")]
    _ids_dist = {x.entier("Id_Dist_1re", 0) for g in p.entree.tous("Groupe") for em in g.directs("Emetteur") for x in em.tous("Distribution_Groupe_Chaud")}
    if len(_gens_ballon) == 1 and any(i not in dch for i in _ids_dist if i):
        dch = _Defaut(dch, _gens_ballon[0])
    decs = {d.entier("Index"): d.entier("Id_Gen") for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    # RSEE sans nœud Distribution_Intergroupe_ECS (cas 15) : les émetteurs ECS sont rattachés à l'unique génération à ballon
    _gens_ballon = [g.entier("Index") for g in p.entree.directs("Generation") if g.directs("Production_Stockage")]
    if not decs and len(_gens_ballon) == 1:
        decs = _Defaut(decs, _gens_ballon[0])
    b_tampons = {}
    for bat in p.entree.directs("Batiment"):
        b_tampons.update(enveloppe.coefficients_b(bat))
    reseaux = {d.entier("Index"): ecs_distribution.Intergroupe.depuis(d, b_tampons) for d in p.entree.tous("Distribution_Intergroupe_ECS")}
    # demandes par génération : chauffage (groupes desservis), ECS (par les réseaux intergroupes)
    qch, qecs_dp, desservis, saison_ch, t_reseau, reseaux_gen = {}, {}, {}, {}, {}, {}
    dp_ch = {d.entier("Index"): distribution.ReseauInter.depuis(d, distribution.CHAUD, b_tampons) for d in p.entree.tous("Distribution_Intergroupe_Chaud")}
    for cle, (d, surface) in groupes.items():
        g = d["noeud"]
        # part de chaque émetteur dans la demande du groupe : Rat_s x Rat_t normalisé (797, 798, 811)
        ems = [(em, em.nombre("Rat_s_ch", 1.0) * em.nombre("Rat_t_ch", 1.0)) for em in g.directs("Emetteur") if em.entier("Is_emetteur_chaud", 1) == 1]
        total = sum(r for _, r in ems) or 1.0
        parts = {}
        for em, r in ems:
            for x in em.tous("Distribution_Groupe_Chaud"):
                i = dch.get(x.entier("Id_Dist_1re", 0), 0)
                parts[i] = parts.get(i, 0.0) + r / total
        for i, part in parts.items():
            qch[i] = qch.get(i, np.zeros(n)) + d["ch_h"] * part
            desservis.setdefault(i, []).append((cle, d, surface * part))
        # température moyenne de dimensionnement des réseaux hydrauliques (θdép - Δθ/2), par génération, pondérée par la part
        for em, r in ems:
            for x in em.tous("Distribution_Groupe_Chaud"):
                i = dch.get(x.entier("Id_Dist_1re", 0), 0)
                if x.entier("Type_2nd", 0) in (1, 2):                                  # réseau hydraulique : régulation et pertes (8.7, 8.8)
                    reseaux_gen.setdefault(i, []).append((distribution.ReseauGroupe.depuis(x, distribution.CHAUD, b_tampons), r / total, d, x.entier("Id_Dist_1re", 0)))
                if x.nombre("Theta_Dep_Dim_Ch", 0.0) > 0:
                    i = dch.get(x.entier("Id_Dist_1re", 0), 0)
                    t_reseau.setdefault(i, []).append((x.nombre("Theta_Dep_Dim_Ch") - 0.5 * x.nombre("Delta_Theta_Em_Dim_Ch", 10.0), r / total * surface))
            ch_j = np.isin(d["saison"], (3, 4))
            saison_ch[i] = ch_j if i not in saison_ch else (saison_ch[i] | ch_j)
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
    # Réseaux hydrauliques : les états horaires des réseaux du groupe viennent du modèle thermique (groupe.calculer, qui
    # rend déjà leurs pertes en volume chauffé au groupe à l'heure suivante : le besoin ch_h est net). Ici on assemble le
    # réseau intergroupes de chaque génération ; la génération fournit le besoin net plus les pertes brutes des réseaux
    # du groupe et du réseau intergroupes, moins la part récupérée de ce dernier (60 %, non rebouclée).
    etats_gen = {}
    for id_gen, hyd in reseaux_gen.items():
        dp = next((dp_ch[k] for *_, k in hyd if k in dp_ch), None)
        if dp is None:
            continue
        qnom_dp, qresid_dp = sum(r.qnom for r, *_ in hyd), sum(r.qresid for r, *_ in hyd)
        liste = []
        for h in range(n):
            etats = []
            for r, part, d, _ in hyd:
                src = d.get("etats_reseau")
                if src is not None and d.get("reseaux"):
                    idx = next((i for i, (rr, _p) in enumerate(d["reseaux"]) if rr == r), None)
                    etats.append(src[h][idx] if idx is not None else distribution.EtatReseau())
                else:
                    etats.append(distribution.reseau_groupe(r, float(d["ch_h"][h]) * part, float(d["theta_i"][h]) if d["theta_i"] is not None else 20.0, float(cl.te[h]), cl.base_ext))
            inter = distribution.reseau_intergroupe(dp, etats, qnom_dp, qresid_dp, float(cl.te[h]))
            liste.append((etats, inter))
        etats_gen[id_gen] = liste
    sorties = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g for b in p.sortie.tous("Sortie_Batiment_C")
               for z in b.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C")}
    resultats = []
    jours = np.arange(n) // 24
    for id_gen, gen in gens.items():
        if id_gen not in qch:
            continue
        combustion = next((c for c in gen.enfants if c.nom in ("Generateur_Combustion", "Generateur_Reseau_Fourniture")), None)
        ballon_combustion = combustion is None and any(c.nom in ("Source_Ballon_Base_Combustion", "Source_Ballon_Base_Reseau_Fourniture")
                                                       and c.entier("Id_Fou_Gen_1", c.entier("Id_Fou_Gen", 3)) in (1, 4)
                                                       for ps in gen.directs("Production_Stockage") for c in ps.enfants)
        if ballon_combustion:                                            # générateur en base de ballon qui chauffe aussi : l'ECS est portée par le ballon (banc ECS)
            combustion = next(c for ps in gen.directs("Production_Stockage") for c in ps.enfants if c.nom in ("Source_Ballon_Base_Combustion", "Source_Ballon_Base_Reseau_Fourniture"))
        if combustion is not None and combustion.nom.endswith("Reseau_Fourniture") and combustion.entier("Id_Fou_Gen", 1) == 2:
            combustion = None                                            # réseau de froid : hors chauffage
        if combustion is not None:
            # chaudière (8.19) ou sous-station (8.28) : ECS instantanée à Theta_Wm_Ecs puis chauffage sur les réseaux hydrauliques, le reste reporté
            if "Reseau_Fourniture" in combustion.nom:
                ch_ = reseau_fourniture.ReseauFourniture.depuis(combustion)
                ch_.famille = "réseau de chaleur"
            else:
                ch_ = chaudiere.Chaudiere.depuis(combustion, gen.entier("Pos_Gen", 0))
            hyd = etats_gen.get(id_gen)
            ch_j = saison_ch[id_gen]
            demande_ecs = np.zeros(n) if ballon_combustion else qecs.get(id_gen, np.zeros(n))
            t_ecs = gen.nombre("Theta_Wm_Ecs", 54.0) or 54.0
            t_wm = gen.nombre("Theta_Wm_Ch", 70.0) or 70.0
            gaz = aux = fourni = pertes_reseau = gaz_ecs = 0.0
            report = 0.0
            mois = np.zeros(12)
            elec_h = np.zeros(n)
            for h in range(n):
                en_saison = bool(ch_j[min(jours[h], len(ch_j) - 1)])
                q = (float(qch[id_gen][h]) + report) if en_saison else 0.0
                t_aval = t_wm
                if hyd and en_saison:
                    etats, inter = hyd[h]
                    pertes = sum(x.phi_vc + x.phi_hvc for x in etats) + 0.4 * inter.phi_vc + inter.phi_hvc
                    pertes_reseau += pertes
                    q += pertes
                    if inter.fonct:
                        t_aval = 0.5 * (inter.theta_dep + inter.theta_ret)
                r = ch_.appeler(float(demande_ecs[h]), q, t_ecs, t_aval, 20.0 if gen.entier("Pos_Gen", 0) == 1 else float(cl.te[h]), not en_saison)
                gaz += r.qcef.sum() - r.qcef[:, generateurs.COL[50]].sum()                 # énergies non électriques : gaz, fioul, bois, réseau
                gaz_ecs += r.qcef[generateurs.ECS, :].sum() - r.qcef[generateurs.ECS, generateurs.COL[50]]
                aux += r.waux; fourni += r.qfou
                elec_h[h] += r.waux + r.qcef[:, generateurs.COL[50]].sum()
                mois[int(cal.mois_civil[h]) - 1] += r.qcef[generateurs.CH, :].sum()
                report = max(0.0, r.qrest - max(0.0, float(demande_ecs[h]) - (r.qfou - min(r.qfou, q))))   # seul le reste de chauffage est reporté
            surface = sum(x for _, _, x in desservis[id_gen])
            ref_ch = sum(d["cef_ch_ref"] * x for _, d, x in desservis[id_gen] if d["cef_ch_ref"] == d["cef_ch_ref"])
            # référence ECS : les groupes dont les émetteurs ECS aboutissent à cette génération (Rat_em_e), pas ceux qu'elle chauffe
            ref_ecs = 0.0
            for c, (d, surf) in groupes.items():
                if c not in sorties or ballon_combustion:
                    continue
                for em in d["noeud"].directs("Emetteur_ECS"):
                    for ds in em.directs("Distribution_Groupe_ECS"):
                        if decs.get(ds.entier("Id_Dist_Primaire", 0), 0) == id_gen:
                            ref_ecs += sorties[c].nombre("O_Cef_ecs_annuel", 0.0) * surf * em.nombre("Rat_em_e", 1.0)
            resultats.append((id_gen, "chaudière " + ch_.famille, dict(sys=0, demande=float(qch[id_gen].sum()) + pertes_reseau, fourni=fourni, elec_pac=aux, elec_joule=0.0,
                                                                     reste=report, heures=0, surface=surface, ref=ref_ch + ref_ecs, gaz=gaz, ref_ecs=ref_ecs, gaz_ecs=gaz_ecs, ref_ch=ref_ch, mois=mois,
                                                                     mois_ref=sum((d["mois_ref"] if d["mois_ref"] is not None and len(d["mois_ref"]) == 12 else np.zeros(12)) * x for _, d, x in desservis[id_gen]),
                                                                     groupes=[d["zone_index"] for _, d, _ in desservis[id_gen]], pertes_reseau=pertes_reseau, waux_reseau=0.0, elec_h=elec_h)))
            continue
        pac_noeud = None
        assemblage = None
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
        if pac_noeud is None:
            joules = [generateurs.EffetJoule.depuis(c) for c in gen.enfants if c.nom == "Generateur_Effet_Joule"]
            if joules:                                                   # génération à effet joule seul : identité (8.18)
                s = sum(x for _, _, x in desservis[id_gen])
                resultats.append((id_gen, "effet joule", dict(sys=0, demande=float(qch[id_gen].sum()), fourni=float(qch[id_gen].sum()), elec_pac=0.0,
                                                               elec_joule=float(qch[id_gen].sum()), reste=0.0, heures=0, surface=s,
                                                               ref=sum(d["cef_ch_ref"] * x for _, d, x in desservis[id_gen] if d["cef_ch_ref"] == d["cef_ch_ref"]),
                                                               groupes=[d["zone_index"] for _, d, _ in desservis[id_gen]], elec_h=np.asarray(qch[id_gen], dtype=float).copy())))
            continue
        try:
            pac = th.Pac.depuis(pac_noeud)
        except NotImplementedError as e:
            resultats.append((id_gen, f"non traité : {e}", None))
            continue
        joules = [generateurs.EffetJoule.depuis(c) for c in gen.enfants if c.nom == "Generateur_Effet_Joule"]
        # appoint à combustion du ballon qui chauffe aussi (Id_Fou 1 ou 4) : reçoit le reste du chauffage après la PAC (cascade)
        appoint_comb = next((chaudiere.Chaudiere.depuis(c, gen.entier("Pos_Gen", 0)) for ps in gen.directs("Production_Stockage") for c in ps.enfants
                             if c.nom == "Source_Ballon_Appoint_Combustion" and c.entier("Id_Fou_Gen_1", 3) in (1, 4)), None)
        gaz_appoint = 0.0
        sys_ch = pac.modes[th.CH].sys
        # réseau hydraulique (sys 1) : Theta_Wm_Ch si gestion à température constante, sinon moyenne de dimensionnement des
        # réseaux desservis (premier jet : pas de loi d'eau, θmoy_dp(h) de la fiche 8.11 viendra avec la distribution)
        if gen.entier("Type_Gestion_Chaud_Gen", 2) == 1 or id_gen not in t_reseau:
            t_wm = gen.nombre("Theta_Wm_Ch", 35.0) or 35.0
        else:
            t_wm = sum(t * w for t, w in t_reseau[id_gen]) / sum(w for _, w in t_reseau[id_gen])
        theta_groupes = [d["theta_i"] for _, d, _ in desservis[id_gen] if d["theta_i"] is not None]
        t_air = np.mean(theta_groupes, axis=0) if theta_groupes else np.full(n, 20.0)
        ch_j = saison_ch[id_gen]
        demande_ecs = qecs.get(id_gen, np.zeros(n))
        elec_pac = elec_joule = fourni = reste = heures = 0.0
        report = 0.0                                                     # énergie non fournie reportée au pas suivant (1015, 1029)
        mois = np.zeros(12)
        elec_h = np.zeros(n)
        hydraulique = etats_gen.get(id_gen)
        pertes_reseau = waux_reseau = 0.0
        for h in range(n):
            en_saison = bool(ch_j[min(jours[h], len(ch_j) - 1)])
            rfonct = 0.0
            if assemblage is not None:
                assemblage.heure(float(demande_ecs[h]), float(cl.teau[h]), ecs_distribution.THETA_2ND, float(cl.te[h]), int(cal.case[h]) - 1, not en_saison)
                rfonct = getattr(assemblage.base, "dernier_lr", 0.0)
            q = (float(qch[id_gen][h]) + report) if en_saison else 0.0
            t_aval = float(t_air[h]) if sys_ch == 2 else t_wm
            if hydraulique and en_saison:                                   # réseaux hydrauliques : demande nette + pertes brutes, θmoy vue par la génération (1011)
                etats, inter = hydraulique[h]
                pertes = sum(x.phi_vc + x.phi_hvc for x in etats) + 0.4 * inter.phi_vc + inter.phi_hvc
                pertes_reseau += pertes
                waux_reseau += inter.waux + sum(x.waux for x in etats)
                q = float(qch[id_gen][h]) + pertes + report
                if inter.fonct:
                    t_aval = 0.5 * (inter.theta_dep + inter.theta_ret)
            r = pac.heure(th.CH, q, float(cl.te[h]), t_aval, rfonct_ecs=rfonct, part_waux0=(1.0 - rfonct) if en_saison else 0.0)
            elec_pac += r["elec"]; fourni += r["fourni"]; heures += r["lr"] > 0
            rest = r["rest"]
            mois[int(cal.mois_civil[h]) - 1] += r["elec"]
            elec_h[h] += r["elec"]
            for j in joules:
                rj = j.appeler(rest, generateurs.CH)
                elec_joule += rj.qcons; rest = rj.qrest
                mois[int(cal.mois_civil[h]) - 1] += rj.qcons
                elec_h[h] += rj.qcons
            if appoint_comb is not None and rest > 0:
                rc = appoint_comb.appeler(0.0, rest, t_wm, t_aval, 20.0 if gen.entier("Pos_Gen", 0) == 1 else float(cl.te[h]), False)
                gaz_appoint += rc.qcons; elec_pac += rc.waux; rest = rc.qrest
                elec_h[h] += rc.waux
                mois[int(cal.mois_civil[h]) - 1] += rc.qcons
            report = rest
        reste = report
        surface = sum(s for _, _, s in desservis[id_gen])
        ref = sum(d["cef_ch_ref"] * s for _, d, s in desservis[id_gen] if d["cef_ch_ref"] == d["cef_ch_ref"])
        resultats.append((id_gen, pac_noeud.nom.replace("Source_Ballon_Base_Thermodynamique_Elec_", "ballon ").replace("Generateur_Thermodynamique_Elec_", "PAC "),
                          dict(sys=sys_ch, demande=float(qch[id_gen].sum()) + pertes_reseau, fourni=fourni, elec_pac=elec_pac, elec_joule=elec_joule, reste=reste, heures=heures,
                               surface=surface, ref=ref, groupes=[d["zone_index"] for _, d, _ in desservis[id_gen]], pertes_reseau=pertes_reseau, waux_reseau=waux_reseau,
                               mois=mois, mois_ref=sum((d["mois_ref"] if d["mois_ref"] is not None and len(d["mois_ref"]) == 12 else np.zeros(12)) * x for _, d, x in desservis[id_gen]),
                               elec_h=elec_h, **(dict(gaz=gaz_appoint, gaz_ecs=0.0, ref_ch=ref, ref_ecs=0.0) if appoint_comb is not None else {}))))
    return resultats


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tot = ref_tot = 0.0
    for id_gen, nom, r in comparer(sys.argv[1]):
        if r is None:
            print(f"génération {id_gen} : {nom}")
            continue
        s = r["surface"]
        if "gaz" in r:
            print(f"génération {id_gen} : {nom} | zones {r['groupes']} | demande ch {r['demande'] / 1000:6.0f} kWh (dont pertes réseaux {r['pertes_reseau'] / 1000:.0f}) | fournie ch+ECS {r['fourni'] / 1000:6.0f}"
                  f" | gaz ch {(r['gaz'] - r['gaz_ecs']) / 1000 / s:5.2f} / RSEE ch {r['ref_ch'] / s:5.2f} ; gaz ECS {r['gaz_ecs'] / 1000 / s:5.2f} / RSEE ECS {r['ref_ecs'] / s:5.2f} ; aux élec {r['elec_pac'] / 1000 / s:4.2f} kWh/m²"
                  f" | total ({(r['gaz'] + r['elec_pac']) / 1000 / r['ref'] - 1:+.0%}) | report final {r['reste'] / 1000:.0f} kWh")
            tot += r["gaz"] + r["elec_pac"]; ref_tot += r["ref"]
            continue
        print(f"génération {id_gen} : {nom} sys {r['sys']} | zones {r['groupes']} | demande {r['demande'] / 1000:6.0f} kWh | fournie PAC {r['fourni'] / 1000:6.0f}"
              f" | élec PAC {r['elec_pac'] / 1000 / s:5.2f} + joule {r['elec_joule'] / 1000 / s:4.2f} = {(r['elec_pac'] + r['elec_joule']) / 1000 / s:5.2f} / RSEE {r['ref'] / s:5.2f} kWh/m²"
              f" ({(r['elec_pac'] + r['elec_joule']) / 1000 / r['ref'] - 1:+.0%}) | COP PAC {r['fourni'] / max(r['elec_pac'], 1):.2f} | {r['heures']:.0f} h | report final {r['reste'] / 1000:.0f} kWh"
              + (f" | pertes réseaux {r['pertes_reseau'] / 1000:.0f} kWh, circulateurs {r['waux_reseau'] / 1000:.0f} kWh" if r.get('pertes_reseau') else ""))
        tot += r["elec_pac"] + r["elec_joule"]; ref_tot += r["ref"]
    if ref_tot:
        print(f"PROJET : chauffage {tot / 1000:.0f} / RSEE {ref_tot:.0f} kWh ({tot / 1000 / ref_tot - 1:+.0%})")
    if "--mois" in sys.argv:
        for id_gen, nom, r in comparer(sys.argv[1]):
            if r is None or "mois" not in r or r["surface"] <= 0:
                continue
            print(f"génération {id_gen} chauffage mensuel (kWh/m²) :")
            print("   calcul " + " ".join(f"{v / 1000 / r['surface']:5.1f}" for v in r["mois"]))
            print("   RSEE   " + " ".join(f"{v / r['surface']:5.1f}" for v in r["mois_ref"]))
