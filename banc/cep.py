# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des consommations (mode Th-C) par groupe, poste par poste, contre Sortie_Groupe_C des RSEE.

    python -m banc.cep <fichier RSEE | dossier> [nombre de projets]

Postes couverts : auxiliaires de ventilation (O_Cef_aux_ventilateur_annuel), éclairage (O_Cef_ecl_annuel), besoins
de chauffage et de refroidissement au niveau des émetteurs (O_B_Ch_annuel, O_B_Fr_annuel), en kWh par m².
"""
import dataclasses
import json
import statistics
import sys
from pathlib import Path

from banc.besoins import METEO, zone_climatique
import numpy as np

from openbce import aeraulique, brasseurs, calendrier, climat, consommation, distribution, ecs, ecs_distribution, emission, enveloppe, groupe, meteo, rsee, scenarios, ventilation
from openbce import usages as mod_usages


def reseaux_chaud(g, b_tampons=None):
    """Réseaux hydrauliques de chauffage du groupe avec la part de leur émetteur (Rat_s x Rat_t normalisé, 797, 798)."""
    ems = [(em, em.nombre("Rat_s_ch", 1.0) * em.nombre("Rat_t_ch", 1.0)) for em in g.directs("Emetteur") if em.entier("Is_emetteur_chaud", 1) == 1]
    total = sum(r for _, r in ems) or 1.0
    out = []
    for em, r in ems:
        for x in em.tous("Distribution_Groupe_Chaud"):
            if x.entier("Type_2nd", 0) in (1, 2):
                out.append((distribution.ReseauGroupe.depuis(x, distribution.CHAUD, b_tampons), r / total))
    return tuple(out)


def _thc(zone, g, usage, sc_g, cl, ch_impose=None, fr_impose=None, b_tampons=None):
    vent = ventilation.du_groupe(zone, g, usage, sc_g.ventilation)
    surface = g.nombre("SHAB") if usage in (1, 2) else g.nombre("SU")
    return groupe.ThC(vent, aeraulique.entrees_air(zone, g), emission.equivalent(g, True), emission.equivalent(g, False),
                      emission.relance(sc_g.consigne_ch, g.entier("Type_Pgrm_Ch", 1), cl.te, float(np.min(cl.base_ext)), True, sc_g.etat_ch),
                      emission.relance(sc_g.consigne_fr, g.entier("Type_Pgrm_Fr", 1), cl.te, float(np.min(cl.base_ext)), False, sc_g.etat_fr),
                      g.entier("Is_Climatise", 0) == 1, ch_impose, fr_impose, reseaux_chaud(g, b_tampons),
                      brasseurs.lire(g, usage, surface), g.nombre("V", 2.5 * surface))


def saisons_batiment(bat, cl, cal, b_tampons=None):
    """Première passe du Th-C : saisons propres de chaque groupe, puis union sur le bâtiment (8.4, raccordement
    permanent). Rend (chauffage, refroidissement) autorisés par jour, ou (None, None) sans groupe d'usage traité."""
    b_tampons = enveloppe.coefficients_b(bat) if b_tampons is None else b_tampons
    union_ch, union_fr = None, None
    for zone in bat.directs("Zone"):
        usage = zone.entier("Usage")
        if usage not in mod_usages.NOMS:
            continue
        groupes = zone.directs("Groupe")
        cle = "SHAB" if usage in (1, 2) else "SU"
        surface_zone = sum(g.nombre(cle) for g in groupes)
        sc = scenarios.habitation(cal, usage, surface_zone, max(zone.entier("NB_logement", 1), 1)) if usage in (1, 2) else scenarios.tertiaire(cal, usage, surface_zone)
        for g in groupes:
            part = g.nombre(cle) / surface_zone
            sc_g = dataclasses.replace(sc, occupants=sc.occupants * part, apports_occupants=sc.apports_occupants * part,
                                       apports_usages=sc.apports_usages * part, nadeq=sc.nadeq * part)
            b0 = groupe.calculer(g, usage, cl, cal, sc_g, b_tampons, aeraulique.du_groupe(zone, g), thc=_thc(zone, g, usage, sc_g, cl))
            ch = np.isin(b0.saison, (3, 4)); fr = np.isin(b0.saison, (1, 4))
            union_ch = ch if union_ch is None else (union_ch | ch)
            union_fr = fr if union_fr is None else (union_fr | fr)
    return union_ch, union_fr


def generateurs_chauffage(projet, groupe) -> set[str]:
    """Noms des nœuds générateurs (Generateur_Effet_Joule, Generateur_Thermodynamique_*, Production_Stockage...) des
    générations qui chauffent le groupe, par la chaîne Emetteur > Distribution_Groupe_Chaud > Distribution_Intergroupe_Chaud > Generation."""
    gens = {g.entier("Index"): g for g in projet.entree.directs("Generation")}
    dch = {d.entier("Index"): d.entier("Id_Gen") for d in projet.entree.tous("Distribution_Intergroupe_Chaud")}
    ids = {dch.get(d.entier("Id_Dist_1re", 0), 0) for em in groupe.directs("Emetteur") for d in em.tous("Distribution_Groupe_Chaud")}
    return {c.nom for i in ids if i in gens for c in gens[i].enfants if c.nom.startswith(("Generateur", "Production"))}


def comparer(chemin: str):
    projet = rsee.lire(chemin)
    simu = projet.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(projet)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    sorties = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g
               for b in projet.sortie.tous("Sortie_Batiment_C") for z in b.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C")}
    lignes = []
    for bat in projet.entree.directs("Batiment"):
        b_tampons = enveloppe.coefficients_b(bat)
        union_ch, union_fr = saisons_batiment(bat, cl, cal, b_tampons)
        for zone in bat.directs("Zone"):
            usage = zone.entier("Usage")
            if usage not in mod_usages.NOMS:
                continue
            groupes = zone.directs("Groupe")
            cle = "SHAB" if usage in (1, 2) else "SU"
            surface_zone = sum(g.nombre(cle) for g in groupes)
            sc = scenarios.habitation(cal, usage, surface_zone, max(zone.entier("NB_logement", 1), 1)) if usage in (1, 2) else scenarios.tertiaire(cal, usage, surface_zone)
            for g in groupes:
                surface = g.nombre(cle)
                part = surface / surface_zone
                sc_g = dataclasses.replace(sc, occupants=sc.occupants * part, apports_occupants=sc.apports_occupants * part,
                                           apports_usages=sc.apports_usages * part, nadeq=sc.nadeq * part)
                s = sorties.get((bat.entier("Index"), zone.entier("Index"), g.entier("Index")))
                thc = _thc(zone, g, usage, sc_g, cl, union_ch, union_fr, b_tampons)
                b = groupe.calculer(g, usage, cl, cal, sc_g, b_tampons, aeraulique.du_groupe(zone, g), thc=thc)
                aux_h = consommation.puissance_ventilateurs(zone, g, usage, sc_g.ventilation)
                if b.brasseurs_w is not None:                                         # brasseurs d'air (8.32) : avec les auxiliaires de ventilation
                    aux_h = aux_h + b.brasseurs_w
                aux = aux_h.sum() / 1000 / surface
                ecl = b.eclairage.sum() / 1000 / surface
                ref = lambda k: s.nombre(k, float("nan")) if s else float("nan")
                try:
                    qw = ecs.besoins(g, usage, cal, cl.teau)
                    pertes_ecs = ecs_distribution.pertes(ecs_distribution.troncons(g, usage, surface), qw, b.theta_i, cl.te)
                    ecs_tot = (qw.sum() + pertes_ecs.sum()) / 1000 / surface
                except NotImplementedError:
                    ecs_tot = float("nan")
                mois = np.array([b.chauffage[cal.mois_civil == m].sum() / 1000 / surface for m in range(1, 13)])
                lignes.append((zone.texte("Name"), usage, surface, aux, ref("O_Cef_aux_ventilateur_annuel"), ecl, ref("O_Cef_ecl_annuel"),
                               b.chauffage.sum() / 1000 / surface, ref("O_B_Ch_annuel"), b.refroidissement.sum() / 1000 / surface, ref("O_B_Fr_annuel"),
                               ecs_tot, ref("O_B_Ecs_annuel"), ref("O_Cef_ecs_annuel"),
                               dict(mois=mois, mois_ref=np.array(s.mensuel("O_Cef_ch_mois")) if s else None, generateurs=generateurs_chauffage(projet, g),
                                    fr_mois=np.array([b.refroidissement[cal.mois_civil == m].sum() / 1000 / surface for m in range(1, 13)]),
                                    fr_mois_ref=np.array(s.mensuel("O_Cef_fr_mois")) if s else None, groupe=g.entier("Index"),
                                    bat=bat.entier("Index"), zone_index=zone.entier("Index"), noeud=g, usage=usage,
                                    ch_h=b.chauffage, fr_h=b.refroidissement, theta_i=b.theta_i, saison=b.saison,
                                    ecl_h=b.eclairage, aux_h=aux_h, mob_h=sc_g.apports_usages,          # Wh par heure (4.7 : mobilier = apports hors occupants)
                                    etats_reseau=b.etats_reseau, recup_reseau=b.recup_reseau, reseaux=thc.reseaux_chaud,
                                    cef_ch_ref=s.nombre("O_Cef_ch_annuel", float("nan")) if s else float("nan"),
                                    cef_fr_ref=s.nombre("O_Cef_fr_annuel", float("nan")) if s else float("nan"))))
    return lignes


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cible = Path(sys.argv[1])
    if cible.is_file():
        fichiers = [cible]
    else:
        lot = json.loads((cible / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
        limite = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        fichiers, vus = [], set()
        for x in sorted(lot, key=lambda x: x["octets"]):
            if x["projet"] in vus or len(vus) >= limite:
                continue
            try:
                rsee.lire(cible / x["fichier"])
            except Exception:
                continue
            vus.add(x["projet"])
            fichiers.append(cible / x["fichier"])
    e_aux, e_ecl, e_ch, e_fr = [], [], [], []
    for f in fichiers:
        for zone, usage, surface, aux, aux_ref, ecl, ecl_ref, ch, ch_ref, fr, fr_ref, ecs_tot, ecs_b, ecs_cef, _ in comparer(str(f)):
            e_aux.append(aux - aux_ref)
            e_ch.append(ch / ch_ref - 1 if ch_ref else float("nan"))
            e_fr.append(fr - fr_ref)
            texte = (f"{f.name[:12]} {zone[:18]:18s} usage {usage} {surface:6.0f} m² | aux. {aux:5.2f} / {aux_ref:4.1f} | ch {ch:5.1f} / {ch_ref:5.1f} | fr {fr:5.1f} / {fr_ref:5.1f}"
                     f" | ECS besoins+pertes {ecs_tot:5.1f} (besoins RSEE {ecs_b:4.1f}) / Cef {ecs_cef:4.1f}")
            if ecl is not None:
                e_ecl.append(ecl - ecl_ref)
                texte += f" | éclairage {ecl:5.2f} / {ecl_ref:4.1f}"
            print(texte, flush=True)
    ch_valides = [e for e in e_ch if e == e]
    if ch_valides:
        print(f"chauffage Th-C : {len(ch_valides)} groupes, écart médian {statistics.median(ch_valides):+.1%}, |écart| médian {statistics.median(abs(e) for e in ch_valides):.1%}")
        print(f"froid Th-C : écart médian {statistics.median(e_fr):+.2f} kWh/m², |écart| médian {statistics.median(abs(e) for e in e_fr):.2f}")
    if e_aux:
        print(f"auxiliaires : {len(e_aux)} groupes, écart médian {statistics.median(e_aux):+.2f} kWh/m², |écart| médian {statistics.median(abs(e) for e in e_aux):.2f}")
    if e_ecl:
        print(f"éclairage : {len(e_ecl)} groupes, écart médian {statistics.median(e_ecl):+.2f} kWh/m², |écart| médian {statistics.median(abs(e) for e in e_ecl):.2f}")
