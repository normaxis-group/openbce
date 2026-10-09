# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Cherche les seuils de la gestion automatique des volets que le texte ne donne pas (éclairement Eclim_auto,
limites de température opérative), en balayant une grille et en mesurant l'écart sur le froid et sur le Bbio des
zones à volets automatiques. C'est une déduction à partir des RSEE.

    python -m banc.seuils_auto <dossier de RSEE> [nombre de projets]
"""
import json
import statistics
import sys
from pathlib import Path

from banc import besoins
from openbce import protections, rsee

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, limite = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 10
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    fichiers, projets = [], set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in projets or len(fichiers) >= limite:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        types = {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")}
        if 1 in types and types <= {0, 1, 2, 3} and all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            fichiers.append(x["fichier"])
            projets.add(x["projet"])
    print(len(fichiers), "projets à volets automatiques")
    for eclim in (3000.0, 10000.0, 30000.0):
        for bas, haut in ((22.0, 24.0), (23.0, 25.0), (24.0, 26.0), (25.0, 27.0)):
            protections.ECLIM_AUTO, protections.TOP_LIM_BAS, protections.TOP_LIM_HAUT = eclim, bas, haut
            froid, bbio, chauffage = [], [], []
            for f in fichiers:
                try:
                    for _, zone, usage, surface, ch, _a, fr, _b, ecl, _c, bbio_ref, (ch_an, fr_an, ecl_an) in besoins.comparer(str(dossier / f)):
                        froid.append(fr.sum() - fr_an)
                        chauffage.append(ch.sum() / max(ch_an, 1e-9) - 1)
                        bbio.append((2 * ch.sum() + 2 * fr.sum() + 5 * ecl.sum()) / max(bbio_ref, 1e-9) - 1)
                except Exception:
                    pass
            print(f"Eclim {eclim:>6.0f} lux, limites {bas:.0f}/{haut:.0f} °C : froid {statistics.median(froid):+.2f} kWh/m² (|écart| médian {statistics.median(map(abs, froid)):.2f}), "
                  f"chauffage {statistics.median(chauffage):+.1%}, Bbio {statistics.median(bbio):+.1%} (|écart| médian {statistics.median(map(abs, bbio)):.1%})", flush=True)
