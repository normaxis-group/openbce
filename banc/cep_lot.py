# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du Cep complet sur un lot de RSEE : un fichier par projet tout électrique (sans générateur à combustion ni réseau).

    python -m banc.cep_lot <dossier de RSEE>
"""
import json
import statistics
import sys
from pathlib import Path

from banc.cep_total import comparer
from openbce import rsee


def main(dossier: Path) -> None:
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, ecarts = set(), []
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        vus.add(x["projet"])
        if not p.sortie.tous("Sortie_Batiment_C"):
            continue
        try:
            r = comparer(str(dossier / x["fichier"]))
        except Exception as e:
            print(f"{x['projet']:10s} erreur : {e!r}", flush=True)
            continue
        s = r["sref"]
        if not s or not r["cep_ref_postes"]:
            continue
        e = r["cep"] / r["cep_ref_postes"] - 1
        ecarts.append(e)
        postes = " | ".join(f"{k} {r['postes'][k] / s:5.2f}/{r['ref'][k] / s:5.2f}" for k in ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist")) + (f" | gaz {r['gaz']:5.2f}/{r['ref_gaz']:5.2f}" if r.get("gaz") else "")
        print(f"{x['projet']:10s} Cep {r['cep']:6.1f} / RSEE hors PV {r['cep_ref_postes']:6.1f} ({e:+.0%}) [O_Cep_annuel {r['cep_ref']:5.1f}] | {postes} | {sorted(set(r['non_modelise'])) or ''}", flush=True)
    if ecarts:
        print(f"{len(ecarts)} projets : écart médian {statistics.median(ecarts):+.1%}, |écart| médian {statistics.median(abs(e) for e in ecarts):.1%}, dans ±10 % : {sum(abs(e) <= 0.1 for e in ecarts)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(Path(sys.argv[1]))
