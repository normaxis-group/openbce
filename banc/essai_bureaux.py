# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Essai des zones de bureaux : python -m banc.essai_bureaux <dossier de RSEE> [nombre de projets]"""
import json
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, limite = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 3
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus = set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus or len(vus) >= limite:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        if not any(z.entier("Usage") == 3 for z in p.entree.tous("Zone")):
            continue
        vus.add(x["projet"])
        try:
            lignes = besoins.comparer(str(dossier / x["fichier"]))
        except NotImplementedError as e:
            print(x["projet"], "non traité :", e)
            continue
        for l in lignes:
            if l[2] != 3:
                continue
            b = 2 * l[4].sum() + 2 * l[6].sum() + 5 * l[8].sum()
            print(x["projet"], l[1][:22], f"{l[3]:.0f} m² | chauffage {l[4].sum():.1f}/{l[11][0]}, froid {l[6].sum():.1f}/{l[11][1]}, "
                  f"éclairage {l[8].sum():.2f}/{l[11][2]}, Bbio {b:.1f}/{l[10]} ({b / l[10] - 1:+.1%})")
            print("   chauffage par mois :", " ".join(f"{v:.1f}" for v in l[4]), "| RSEE", " ".join(f"{v:.1f}" for v in l[5]))
            print("   froid par mois     :", " ".join(f"{v:.1f}" for v in l[6]), "| RSEE", " ".join(f"{v:.1f}" for v in l[7]))
            print("   éclairage par mois :", " ".join(f"{v:.2f}" for v in l[8]), "| RSEE", " ".join(f"{v:.2f}" for v in l[9]))
