# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Essai des stores enroulables sur quelques projets : python -m banc.essai_stores <dossier de RSEE> [nombre]"""
import json
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, limite = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 4
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus = set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus or len(vus) >= limite:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        types = {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")}
        if not (types & {4, 5, 6}) or not types <= {0, 1, 2, 3, 4, 5, 6} or not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            continue
        vus.add(x["projet"])
        for l in besoins.comparer(str(dossier / x["fichier"])):
            b = 2 * l[4].sum() + 2 * l[6].sum() + 5 * l[8].sum()
            print(x["projet"], l[1][:22], sorted(types), f"chauffage {l[4].sum():.1f}/{l[11][0]}, froid {l[6].sum():.1f}/{l[11][1]}, "
                  f"éclairage {l[8].sum():.2f}/{l[11][2]}, Bbio {b:.1f}/{l[10]} ({b / l[10] - 1:+.1%})")
