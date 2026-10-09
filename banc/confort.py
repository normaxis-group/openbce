# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du confort d'été (mode Th-D, fiche 13.5) : degrés-heures DH par groupe contre O_NbDegresHeures des RSEE
(Sortie_Groupe_D, valeur Th-DC).

    python -m banc.confort <dossier de RSEE> [nombre de projets]     (logement seulement, un fichier par projet)
    python -m banc.confort <fichier RSEE>
"""
import dataclasses
import json
import statistics
import sys
from pathlib import Path

from banc.besoins import METEO, zone_climatique
from openbce import aeraulique, brasseurs, calendrier, climat, enveloppe, groupe, meteo, rsee, scenarios, ventilation


def comparer(chemin: str):
    projet = rsee.lire(chemin)
    simu = projet.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(projet), "Th-D"), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    sorties = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g
               for b in projet.sortie.tous("Sortie_Batiment_D") for z in b.tous("Sortie_Zone_D") for g in z.tous("Sortie_Groupe_D")}
    lignes = []
    for bat in projet.entree.directs("Batiment"):
        b_tampons = enveloppe.coefficients_b(bat)
        for zone in bat.directs("Zone"):
            usage = zone.entier("Usage")
            groupes = zone.directs("Groupe")
            surface_zone = sum(g.nombre("SHAB") if usage in (1, 2) else g.nombre("SU") for g in groupes)
            if usage in (1, 2):
                sc = scenarios.habitation(cal, usage, surface_zone, max(zone.entier("NB_logement", 1), 1))
            else:
                sc = scenarios.tertiaire(cal, usage, surface_zone)
            for g in groupes:
                surface = g.nombre("SHAB") if usage in (1, 2) else g.nombre("SU")
                part = surface / surface_zone
                sc_g = dataclasses.replace(sc, occupants=sc.occupants * part, apports_occupants=sc.apports_occupants * part,
                                           apports_usages=sc.apports_usages * part, nadeq=sc.nadeq * part)
                thd = groupe.ThD(ventilation.du_groupe(zone, g, usage, sc_g.ventilation), aeraulique.entrees_air(zone, g),
                                 brasseurs.lire(g, usage, surface), g.nombre("V", 2.5 * surface))
                b = groupe.calculer(g, usage, cl, cal, sc_g, b_tampons, aeraulique.du_groupe(zone, g), thd)
                s = sorties.get((bat.entier("Index"), zone.entier("Index"), g.entier("Index")))
                ref = s.nombre("O_NbDegresHeures", 0.0) if s else float("nan")
                ref_h = tuple(s.entier(k, 0) for k in ("O_Nb_h_inconf", "O_Nb_h_inconf_1", "O_Nb_h_inconf_2")) if s else ()
                lignes.append((zone.texte("Name"), g.texte("Name"), usage, surface, b.dh, ref, b.nb_h_inconfort, ref_h,
                               float(thd.ventilation.repris.mean()), float(thd.ventilation.souffle.mean()), thd.ventilation.epsilon, len(thd.brasseurs)))
    return lignes


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cible = Path(sys.argv[1])
    if cible.is_file():
        fichiers = [cible]
    else:
        lot = json.loads((cible / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
        limite = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        fichiers, vus = [], set()
        for x in sorted(lot, key=lambda x: x["octets"]):
            if x["projet"] in vus or len(vus) >= limite:
                continue
            try:
                p = rsee.lire(cible / x["fichier"])
            except Exception:
                continue
            if not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")) or not p.sortie.tous("Sortie_Groupe_D"):
                continue
            vus.add(x["projet"])
            fichiers.append(cible / x["fichier"])
    ecarts = []
    for f in fichiers:
        for zone, nom, usage, surface, dh, ref, nb, ref_h, q_rep, q_souf, eps, n_br in comparer(str(f)):
            ecarts.append(dh - ref)
            print(f"{f.name[:12]} {zone[:18]:18s} usage {usage} {surface:6.0f} m² | DH {dh:7.1f} / {ref:7.1f} | heures {nb} / {ref_h} | "
                  f"repris {q_rep:6.0f} soufflé {q_souf:6.0f} m³/h ε {eps:.2f} | brasseurs {n_br}", flush=True)
    if ecarts:
        print(f"{len(ecarts)} groupes : écart médian {statistics.median(ecarts):+.1f} °C.h, |écart| médian {statistics.median(abs(e) for e in ecarts):.1f}")
