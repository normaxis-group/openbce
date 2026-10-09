# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des auxiliaires de ventilation : compare à O_Cef_aux_ventilateur_annuel de chaque groupe.

    python -m banc.ventilateurs <dossier de RSEE>            # un fichier par projet
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

from openbce import rsee, ventilateurs


def comparer(chemin):
    projet = rsee.lire(chemin)
    for bat in projet.entree.directs("Batiment"):
        sorties = {(z.entier("Index"), g.entier("Index")): g for sb in projet.sortie.tous("Sortie_Batiment_C") if sb.entier("Index") == bat.entier("Index")
                   for z in sb.tous("Sortie_Zone_C") for g in z.tous("Sortie_Groupe_C")}
        for zone in bat.directs("Zone"):
            try:
                p = ventilateurs.de_la_zone(zone)
            except NotImplementedError as e:
                print(Path(chemin).name, zone.texte("Name"), "non traité :", e)
                continue
            for g in zone.directs("Groupe"):
                s = sorties.get((zone.entier("Index"), g.entier("Index")))
                if s is None or s.nombre("O_SREF", 0) <= 0:
                    continue
                vm = zone.directs("Ventilation_Mecanique")
                yield (zone.texte("Name"), s.nombre("O_SREF"), p[g.entier("Index")] * 8.76 / s.nombre("O_SREF"), s.nombre("O_Cef_aux_ventilateur_annuel", 0.0),
                       tuple(b.entier("Type_Regul_Res", 0) for b in g.directs("Bouche_Conduit")), any(v.texte("Pvent_base_rep") != v.texte("Pvent_pointe_rep") for v in vm))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, ecarts, par = set(), [], collections.defaultdict(list)
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            lignes = list(comparer(dossier / x["fichier"]))
        except Exception as e:
            print(x["projet"], "illisible :", type(e).__name__, e)
            continue
        vus.add(x["projet"])
        for zone, sref, q, ref, regul, deux in lignes:
            ecarts.append(q - ref)
            par[(regul, deux)].append(q - ref)
            print(f"{x['projet']:<10} {zone[:28]:<28} {sref:6.0f} m²  calculé {q:5.2f}  RSEE {ref:4.1f}  écart {q - ref:+.2f}  régulation {regul} deux vitesses {deux}")
    if ecarts:
        a = sorted(abs(e) for e in ecarts)
        print(f"\n{len(ecarts)} groupes ; écart médian {statistics.median(ecarts):+.2f} kWh/m² ; dans ±0,05 : {sum(e <= 0.0501 for e in a)} ; dans ±0,1 : {sum(e <= 0.1001 for e in a)} ; maximum {a[-1]:.2f}")
        for k, v in sorted(par.items(), key=str):
            print("  ", k, len(v), f"médiane {statistics.median(v):+.3f}  min {min(v):+.2f}  max {max(v):+.2f}")
