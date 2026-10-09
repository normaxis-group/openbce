# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc ECS sur tout un lot de RSEE : un fichier par projet, résultat au niveau du projet (voir banc.ecs_cef).

    python -m banc.ecs_lot <dossier de RSEE> [--rapide]
"""
import json
import sys
from pathlib import Path

from banc.ecs_cef import comparer
from openbce import rsee


def main(dossier: Path, rapide: bool) -> None:
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, ecarts = set(), []
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        vus.add(x["projet"])
        try:
            resultats, ref, surface = comparer(str(dossier / x["fichier"]), rapide)
        except Exception as e:
            print(f"{x['projet']:10s} erreur : {e}", flush=True)
            continue
        traites = [(g, a, d, r) for g, a, d, r in resultats if r is not None]
        if not traites or not ref:
            continue
        total = sum(r["elec"] for _, _, _, r in traites)
        for id_gen, asm, demande, r in traites:
            print(f"{x['projet']:10s} gén. {id_gen} : {type(asm.base).__name__} x{asm.nb} | demande {demande / 1000:6.0f} kWh | pertes ballon {r['pertes'] / 1000:5.0f}"
                  f" | élec {r['elec'] / 1000:6.0f} kWh | COP apparent {(r['fourni'] + r['pertes']) / max(r['elec'], 1):.2f} | {r['heures']} h de PAC, {r['nbh_report']} h de report, {r['h_seule']} h ECS seule", flush=True)
        ecart = total / 1000 / ref - 1
        ecarts.append(ecart)
        print(f"{x['projet']:10s} PROJET : élec {total / 1000 / surface:5.2f} / RSEE {ref / surface:5.2f} kWh/m² ({ecart:+.0%}) sur {surface:.0f} m²", flush=True)
    if ecarts:
        import statistics
        print(f"{len(ecarts)} projets, écart médian {statistics.median(ecarts):+.1%}, |écart| médian {statistics.median(abs(e) for e in ecarts):.1%}, "
              f"dans ±10 % : {sum(abs(e) <= 0.10 for e in ecarts)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(Path(sys.argv[1]), "--rapide" in sys.argv)
