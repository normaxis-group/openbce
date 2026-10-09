# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des ascenseurs : compare la consommation annuelle calculée à O_Cef_imp_deplacement_annuel de chaque zone.
Le poste des RSEE contient aussi les parkings : la statistique ne porte que sur les projets qui n'en ont pas.

    python -m banc.ascenseurs <dossier de RSEE>            # un fichier par projet
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from openbce import ascenseurs, rsee


def comparer(chemin):
    projet = rsee.lire(chemin)
    for bat in projet.entree.directs("Batiment"):
        if not bat.directs("Ascenseur"):
            continue
        sorties = {z.entier("Index"): z for sb in projet.sortie.tous("Sortie_Batiment_C") if sb.entier("Index") == bat.entier("Index") for z in sb.tous("Sortie_Zone_C")}
        try:
            conso = ascenseurs.du_batiment(bat, ascenseurs.occupants_conventionnels(bat))
        except NotImplementedError as e:
            print(Path(chemin).name, "non traité :", e)
            continue
        for z in bat.directs("Zone"):
            s = sorties.get(z.entier("Index"))
            if s is None or s.nombre("O_SREF", 0) <= 0:
                continue
            yield z.texte("Name"), s.nombre("O_SREF"), conso[z.entier("Index")] / 1000 / s.nombre("O_SREF"), s.nombre("O_Cef_imp_deplacement_annuel", 0.0), len(projet.entree.tous("Parking"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, ecarts = set(), []
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            lignes = list(comparer(dossier / x["fichier"]))
        except Exception as e:
            print(x["projet"], "illisible :", type(e).__name__, e)
            continue
        vus.add(x["projet"])
        for zone, sref, q, ref, n in lignes:
            if ref > 0 and n == 0:
                ecarts.append(q - ref)
            print(f"{x['projet']:<10} {zone[:30]:<30} {sref:7.0f} m²  {n} parking(s)  calculé {q:5.2f}  RSEE {ref:4.1f}  écart {q - ref:+.2f}")
    if ecarts:
        a = sorted(abs(e) for e in ecarts)
        print(f"\n{len(ecarts)} zones ; écart médian {statistics.median(ecarts):+.2f} kWh/m² ; dans ±0,05 : {sum(e <= 0.0501 for e in a)} ; dans ±0,1 : {sum(e <= 0.1001 for e in a)} ; maximum {a[-1]:.2f}")
