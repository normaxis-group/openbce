# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Synthèse de l'étude de sensibilité : gain de Bbio par levier, par projet et sur l'ensemble.

    python -m banc.variantes_synthese <variantes.csv> [synthese.json]
"""
from __future__ import annotations

import collections
import csv
import json
import statistics
import sys

LIBELLES = {
    "etancheite_mesuree": "Étanchéité justifiée sans échantillonnage",
    "etancheite_moins_02": "Perméabilité abaissée de 0,2 m³/(h.m²)",
    "baies_uw_moins_02": "Uw des baies abaissé de 0,2 W/(m².K)",
    "baies_sw_plus_10": "Facteur solaire des vitrages + 10 %",
    "baies_sw_moins_10": "Facteur solaire des vitrages - 10 %",
    "parois_u_moins_20": "U des parois opaques - 20 %",
    "ponts_moins_30": "Ponts thermiques - 30 %",
    "protections_automatiques": "Protections mobiles en gestion automatique",
    "protections_manuelles": "Protections mobiles manuelles non motorisées",
    "protections_motorisees": "Protections mobiles manuelles motorisées",
}


def lire(chemin):
    """Bbio par (projet, variante), pondéré par la surface des zones, et ses trois composantes."""
    cumul = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    echecs = collections.Counter()
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        for l in csv.DictReader(f, delimiter=";"):
            if not l["surface"]:
                echecs[l["variante"]] += 1
                continue
            s = float(l["surface"])
            c = cumul[(l["projet"], l["variante"])]
            c[0] += s
            c[1] += s * float(l["chauffage"])
            c[2] += s * float(l["froid"])
            c[3] += s * float(l["eclairage"])
    projets = collections.defaultdict(dict)
    for (projet, variante), (s, ch, fr, ecl) in cumul.items():
        ch, fr, ecl = ch / s, fr / s, ecl / s
        projets[projet][variante] = {"surface": s, "chauffage": ch, "froid": fr, "eclairage": ecl, "bbio": 2 * ch + 2 * fr + 5 * ecl}
    return projets, echecs


def synthese(projets):
    lignes = []
    for variante, libelle in LIBELLES.items():
        d = [(p, v[variante], v["base"]) for p, v in projets.items() if variante in v and "base" in v]
        if not d:
            continue
        gains = [x["bbio"] - b["bbio"] for _, x, b in d]
        rel = [x["bbio"] / b["bbio"] - 1 for _, x, b in d]
        lignes.append({
            "variante": variante, "libelle": libelle, "projets": len(d),
            "bbio_median": statistics.median(gains), "bbio_min": min(gains), "bbio_max": max(gains), "bbio_rel_median": statistics.median(rel),
            "chauffage_median": statistics.median(x["chauffage"] - b["chauffage"] for _, x, b in d),
            "froid_median": statistics.median(x["froid"] - b["froid"] for _, x, b in d),
            "eclairage_median": statistics.median(x["eclairage"] - b["eclairage"] for _, x, b in d),
            "projets_gagnants": sum(g < -0.05 for g in gains), "projets_perdants": sum(g > 0.05 for g in gains)})
    return sorted(lignes, key=lambda l: l["bbio_median"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    projets, echecs = lire(sys.argv[1])
    complets = {p: v for p, v in projets.items() if "base" in v}
    print(len(complets), "projets ; échecs :", dict(echecs))
    print(f"{'levier':<46}{'projets':>8}{'Bbio médian':>13}{'min':>8}{'max':>8}{'%':>8}{'chauff.':>9}{'froid':>8}{'écl.':>7}{'gagnants':>10}{'perdants':>9}")
    s = synthese(complets)
    for l in s:
        print(f"{l['libelle']:<46}{l['projets']:>8}{l['bbio_median']:>+13.2f}{l['bbio_min']:>+8.1f}{l['bbio_max']:>+8.1f}{l['bbio_rel_median']:>+8.1%}"
              f"{l['chauffage_median']:>+9.2f}{l['froid_median']:>+8.2f}{l['eclairage_median']:>+7.2f}{l['projets_gagnants']:>10}{l['projets_perdants']:>9}")
    if len(sys.argv) > 2:
        json.dump({"leviers": s, "projets": complets}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
