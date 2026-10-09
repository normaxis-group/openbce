# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Agrège un relevé par zone (banc.zones) par caractère traversant et famille de protections mobiles.

    python -m banc.agreger <zones.json> [<zones.json de comparaison>]
"""
import json
import statistics as st
import sys


def famille(x):
    pm = set(x.get("pm", [])) - {0}
    if pm & {4, 5, 6}:
        return "store"
    return "auto" if pm & {1} else "manuel"


def ligne(l, nom):
    if not l:
        return
    d = [x["fr"] - x["fr_ref"] for x in l]
    b = [x["bbio"] / x["bbio_ref"] - 1 for x in l]
    print(f"{nom:24s} n {len(l):3d} | froid médian {st.median(d):+.2f} moyen {st.mean(d):+.2f} | >+1 : {sum(v > 1 for v in d):2d} <-1 : {sum(v < -1 for v in d):2d}"
          f" | Bbio médian {st.median(b):+.1%} |écart| {st.median(abs(v) for v in b):.1%} | ±1 % : {sum(abs(v) <= 0.01 for v in b)} ±2 % : {sum(abs(v) <= 0.02 for v in b)} ±5 % : {sum(abs(v) <= 0.05 for v in b)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for chemin in sys.argv[1:]:
        z = json.load(open(chemin, encoding="utf-8"))
        print(chemin)
        ligne(z, "toutes")
        for t in (1, 0):
            for f in ("manuel", "auto", "store"):
                ligne([x for x in z if x.get("traversant") == t and famille(x) == f], f"trav={t} {f}")
        print()
