# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc mensuel du besoin de chauffage Th-C des groupes chauffés uniquement par effet joule direct.

    python -m banc.chauffage_mois <fichier RSEE | dossier> [nombre de projets]

Pour ces groupes la génération est une identité (8.18 : rendement 1, pas d'auxiliaire, distribution fictive sans
perte) : O_Cef_ch_mois est le besoin de chauffage mensuel au niveau des émetteurs, directement comparable à la
sortie de groupe.calculer en mode Th-C. Le profil mensuel sépare un écart de ventilation (proportionnel au froid)
d'un écart d'apports ou d'inertie (demi-saisons).
"""
import json
import statistics
import sys
from pathlib import Path

import numpy as np

from banc.cep import comparer
from openbce import rsee

MOIS = "J F M A M J J A S O N D".split()


def main(cible: Path, limite: int) -> None:
    if cible.is_file():
        fichiers = [cible]
    else:
        lot = json.loads((cible / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
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
    ecarts = []
    for f in fichiers:
        for zone, usage, surface, *_, ch, ch_ref, fr, fr_ref, _e1, _e2, _e3, d in comparer(str(f)):
            if d["generateurs"] != {"Generateur_Effet_Joule"} or d["mois_ref"] is None or len(d["mois_ref"]) != 12:
                continue
            ref = d["mois_ref"]
            ecarts.append(ch / ch_ref - 1 if ch_ref else float("nan"))
            print(f"{f.name[:12]} {zone[:16]:16s} g{d['groupe']} u{usage} {surface:5.0f} m² | annuel {ch:5.1f} / {ch_ref:5.1f} ({ch / ch_ref - 1 if ch_ref else 0:+.0%})", flush=True)
            print("   mois   " + " ".join(f"{m:>5s}" for m in MOIS))
            print("   calcul " + " ".join(f"{v:5.1f}" for v in d["mois"]))
            print("   RSEE   " + " ".join(f"{v:5.1f}" for v in ref))
            print("   écart  " + " ".join(f"{a - b:+5.1f}" for a, b in zip(d["mois"], ref)), flush=True)
    valides = [e for e in ecarts if e == e]
    if valides:
        print(f"{len(valides)} groupes effet joule : écart médian {statistics.median(valides):+.1%}, |écart| médian {statistics.median(abs(e) for e in valides):.1%}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 60)
