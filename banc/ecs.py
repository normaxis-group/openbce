# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des besoins d'ECS : compare le besoin annuel calculé à la sortie O_B_Ecs_annuel de chaque groupe.

    python -m banc.ecs <dossier de RSEE>            # un fichier par projet
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

from openbce import calendrier, climat, ecs, meteo, rsee

from .besoins import METEO, zone_climatique


def comparer(chemin):
    projet = rsee.lire(chemin)
    simu = projet.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(projet)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    for bat in projet.entree.directs("Batiment"):
        sorties = {(z.entier("Index"), g.entier("Index")): g for sb in projet.sortie.tous("Sortie_Batiment_C") if sb.entier("Index") == bat.entier("Index")
                   for z in sb.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C")}
        for zone in bat.directs("Zone"):
            usage = zone.entier("Usage")
            for g in zone.directs("Groupe"):
                s = sorties.get((zone.entier("Index"), g.entier("Index")))
                if s is None or usage not in (1, 2) or not g.directs("Emetteur_ECS"):
                    continue
                surface = g.nombre("SHAB")
                em = g.directs("Emetteur_ECS")
                try:
                    q = ecs.besoins(g, usage, cal, cl.teau).sum() / 1000 / surface
                    brut = ecs.besoins(g, usage, cal, cl.teau, corrige=False).sum() / 1000 / surface
                except (NotImplementedError, ValueError) as e:
                    print(Path(chemin).name, zone.texte("Name"), "non traité :", e)
                    continue
                yield (Path(chemin).name, zone.texte("Name"), usage, surface, q, brut, s.nombre("O_B_Ecs_annuel", 0.0),
                       tuple(e.entier("app_ecs", -1) for e in em), tuple(e.nombre("part_em_e_mitigeur_thermo", 0) for e in em))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, ecarts, par_code = set(), [], collections.defaultdict(list)
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            lignes = list(comparer(dossier / x["fichier"]))
        except Exception as e:
            print(x["projet"], "illisible :", type(e).__name__, e)
            continue
        vus.add(x["projet"])
        for nom, zone, usage, surface, q, brut, ref, app, mitig in lignes:
            if ref <= 0:
                continue
            ecarts.append(q / ref - 1)
            par_code[app].append(brut / ref)
            print(f"{x['projet']:<10} {zone[:28]:<28} usage {usage} {surface:7.0f} m²  calculé {q:5.2f}  brut {brut:5.2f}  RSEE {ref:5.1f}  écart {q / ref - 1:+.1%}  app {app} mitigeurs {mitig}")
    if ecarts:
        a = sorted(abs(e) for e in ecarts)
        print(f"\n{len(ecarts)} groupes ; écart médian {statistics.median(ecarts):+.2%} ; écart absolu médian {statistics.median(a):.2%} ; "
              f"dans ±1 % : {sum(e <= 0.01 for e in a)} ; dans ±2 % : {sum(e <= 0.02 for e in a)} ; maximum {a[-1]:.1%}")
        for code, v in sorted(par_code.items()):
            print(f"   app_ecs {code} : {len(v)} groupes, brut / RSEE médian {statistics.median(v):.4f}")
