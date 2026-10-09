# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc du poste « déplacement » : ascenseurs et parkings, comparés à O_Cef_imp_deplacement_annuel de chaque zone.

    python -m banc.deplacement <dossier de RSEE>            # un fichier par projet
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from openbce import ascenseurs, calendrier, parkings, rsee


def comparer(chemin):
    projet = rsee.lire(chemin)
    cal = calendrier.construire()
    sorties = {(sb.entier("Index"), z.entier("Index")): z for sb in projet.sortie.tous("Sortie_Batiment_C") for z in sb.tous("Sortie_Zone_C")}
    sref = {cle: z.nombre("O_SREF", 0.0) for cle, z in sorties.items()}
    park = parkings.du_projet(projet.entree, cal, sref)
    for bat in projet.entree.directs("Batiment"):
        if bat.directs("Escalator"):
            print(Path(chemin).name, "escalator non traité")
            continue
        asc = ascenseurs.du_batiment(bat, ascenseurs.occupants_conventionnels(bat))
        for z in bat.directs("Zone"):
            cle = (bat.entier("Index"), z.entier("Index"))
            if cle not in sorties or sref[cle] <= 0:
                continue
            yield (z.texte("Name"), sref[cle], asc[cle[1]] / 1000 / sref[cle], park[cle] / 1000 / sref[cle], sorties[cle].nombre("O_Cef_imp_deplacement_annuel", 0.0),
                   len(bat.directs("Ascenseur")), len(projet.entree.tous("Parking")))


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
            print(x["projet"], "non traité :", type(e).__name__, e)
            continue
        vus.add(x["projet"])
        for zone, sref, a, p, ref, na, np_ in lignes:
            if na or np_:
                ecarts.append(a + p - ref)
            print(f"{x['projet']:<10} {zone[:28]:<28} {sref:6.0f} m²  {na} asc. {np_} park.  ascenseurs {a:5.2f} + parkings {p:5.2f} = {a + p:5.2f}  RSEE {ref:4.1f}  écart {a + p - ref:+.2f}")
    if ecarts:
        a = sorted(abs(e) for e in ecarts)
        print(f"\n{len(ecarts)} zones ; écart médian {statistics.median(ecarts):+.2f} kWh/m² ; dans ±0,05 : {sum(e <= 0.0501 for e in a)} ; dans ±0,1 : {sum(e <= 0.1001 for e in a)} ; "
              f"dans ±0,3 : {sum(e <= 0.3001 for e in a)} ; maximum {a[-1]:.2f}")
