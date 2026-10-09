# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Synthèse du banc des besoins, pour toutes les zones de logement calculables.

Les écarts sont pris sur les sorties annuelles des RSEE (une décimale), et non sur la somme de leurs valeurs
mensuelles, elles-mêmes arrondies : cette somme porte jusqu'à 0,6 kWh/m² d'erreur d'arrondi.

    python -m banc.synthese <dossier de RSEE>
"""
import collections
import json
import statistics
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee


TYPES = {0, 1, 2, 3, 4, 5, 6}      # protections mobiles traitées (Choix_PM_GPM) : volets et stores enroulables


def mesurer(dossier: Path, par_projet: int = 2):
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    ecarts, vus, echecs, pris = [], set(), collections.Counter(), collections.Counter()
    for x in sorted(lot, key=lambda x: x["octets"]):
        f = dossier / x["fichier"]
        try:
            p = rsee.lire(f)
            if not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
                continue
            types = {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")}
            if not types <= TYPES:
                continue
            if pris[x["projet"]] >= par_projet:      # les variantes d'un même projet se ressemblent : on en garde quelques-unes
                continue
            pris[x["projet"]] += 1
            famille = "store" if types & {4, 5, 6} else ("automatique" if 1 in types else "manuel")
            for _, zone, usage, surface, ch, _m1, fr, _m2, ecl, _m3, bbio_ref, (ch_an, fr_an, ecl_an) in besoins.comparer(str(f)):
                cle = (x["projet"], zone, ch_an, bbio_ref)
                if cle in vus or ch_an < 3:
                    continue
                vus.add(cle)
                ecarts.append((ch.sum() / ch_an - 1, x["projet"], zone[:24], famille, ch_an, ecl.sum() / max(ecl_an, 1e-9) - 1, fr.sum(), fr_an, (2 * ch.sum() + 2 * fr.sum() + 5 * ecl.sum()) / max(bbio_ref, 1e-9) - 1))
        except Exception as e:
            echecs[type(e).__name__] += 1
    return ecarts, echecs


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ecarts, echecs = mesurer(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    e = [a for a, *_ in ecarts]
    print(len(e), "zones ; échecs :", dict(echecs))
    print("chauffage annuel : écart médian %+.0f %%, |écart| médian %.0f %%, de %+.0f %% à %+.0f %%" % (100 * statistics.median(e), 100 * statistics.median(map(abs, e)), 100 * min(e), 100 * max(e)))
    print("dans ±5 % :", sum(abs(v) <= 0.05 for v in e), "| ±10 % :", sum(abs(v) <= 0.10 for v in e), "| ±25 % :", sum(abs(v) <= 0.25 for v in e))
    for nom in ("manuel", "automatique", "store"):
        v = [x[0] for x in ecarts if x[3] == nom]
        if v:
            f2 = [x[6] - x[7] for x in ecarts if x[3] == nom]
            b2 = [x[8] for x in ecarts if x[3] == nom]
            print("  ", nom, ":", len(v), "zones, chauffage médian %+.1f %%, froid %+.1f kWh/m², Bbio %+.1f %% (|écart| médian %.1f %%, dans ±5 %% : %d)" % (
                100 * statistics.median(v), statistics.median(f2), 100 * statistics.median(b2), 100 * statistics.median(map(abs, b2)), sum(abs(q) <= 0.05 for q in b2)))
    l = [x[5] for x in ecarts]
    print("éclairage annuel : écart médian %+.0f %%, |écart| médian %.0f %%, de %+.0f %% à %+.0f %% ; dans ±5 %% : %d" % (100 * statistics.median(l), 100 * statistics.median(map(abs, l)), 100 * min(l), 100 * max(l), sum(abs(v) <= 0.05 for v in l)))
    print("froid annuel, médianes en kWh/m² : calculé %.1f, RSEE %.1f" % (statistics.median(x[6] for x in ecarts), statistics.median(x[7] for x in ecarts)))
    f = [x[6] - x[7] for x in ecarts]
    print("froid annuel : écart médian %+.1f kWh/m², |écart| médian %.1f kWh/m², de %+.1f à %+.1f" % (statistics.median(f), statistics.median(map(abs, f)), min(f), max(f)))
    b = [x[8] for x in ecarts]
    print("Bbio : écart médian %+.1f %%, |écart| médian %.1f %%, de %+.0f %% à %+.0f %% ; dans ±1 %% : %d, ±2 %% : %d, ±5 %% : %d, ±10 %% : %d" % (
        100 * statistics.median(b), 100 * statistics.median(map(abs, b)), 100 * min(b), 100 * max(b),
        sum(abs(v) <= 0.01 for v in b), sum(abs(v) <= 0.02 for v in b), sum(abs(v) <= 0.05 for v in b), sum(abs(v) <= 0.10 for v in b)))
    print("zones les plus en écart sur le Bbio :")
    for x in sorted(ecarts, key=lambda x: x[8])[:3] + sorted(ecarts, key=lambda x: x[8])[-3:]:
        print("   %+.0f %%" % (100 * x[8]), x[1:3], "chauffage %+.0f %%" % (100 * x[0]), "froid %.1f / %.1f" % (x[6], x[7]))
    print("zones les plus en écart sur le chauffage :")
    for x in sorted(ecarts)[:4] + sorted(ecarts)[-2:]:
        print("   %+.0f %%" % (100 * x[0]), x[1:5])
