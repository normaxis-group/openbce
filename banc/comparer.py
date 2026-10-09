# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc d'essai : compare ce que calcule le moteur aux sorties des RSEE de référence.

    python -m banc.comparer enveloppe [dossier_rsee]

Les RSEE de référence sont des données de clients : ils ne sont jamais dans le dépôt. Le dossier est donné en argument
ou par la variable OPENBCE_RSEE.
"""
from __future__ import annotations

import collections
import json
import os
import statistics
import sys
from pathlib import Path

from openbce import enveloppe, rsee

TOLERANCE = 0.01   # 1 %, tolérance du règlement d'évaluation
# sortie du RSEE -> attribut calculé
ENVELOPPE = {"A_opv": "a_opv", "A_ophh": "a_ophh", "A_ophb": "a_ophb", "A_baies": "a_baies", "A_T": "a_t", "L_PT": "l_pt",
             "H_Th_opv": "h_opv", "H_Th_ophh": "h_ophh", "H_Th_ophb": "h_ophb", "H_Th_op": "h_op", "H_Th_PT": "h_pt"}


def ecart(calcule: float, attendu: float, decimales: int) -> float:
    """Écart relatif, nul si la différence tient dans l'arrondi d'affichage de la valeur attendue."""
    if abs(calcule - attendu) <= 0.5 * 10 ** -decimales + 1e-9:
        return 0.0
    return abs(calcule - attendu) / max(abs(attendu), 1e-9)


def decimales(texte: str) -> int:
    return len(texte.split(".")[1]) if "." in texte else 0


def zones(projet):
    """Couples (zone d'entrée, zone de sortie), appariés par bâtiment et par Index."""
    sorties = {(b.entier("Index"), z.entier("Index")): z for b in projet.sortie.tous("Sortie_Batiment_B") for z in b.tous("Sortie_Zone_B")}
    for b in projet.entree.directs("Batiment"):
        for z in b.directs("Zone"):
            s = sorties.get((b.entier("Index"), z.entier("Index")))
            if s is not None:
                yield b, z, s


def enveloppe_tous(dossier: Path):
    lot = {x["fichier"]: x for x in json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]}
    bilan = collections.defaultdict(list)   # indicateur -> écarts
    pires = collections.defaultdict(list)
    n_zones = illisibles = 0
    for nom, info in sorted(lot.items()):
        try:
            projet = rsee.lire(dossier / nom)
        except Exception:
            illisibles += 1
            continue
        for batiment, zone, sortie in zones(projet):
            n_zones += 1
            e = enveloppe.de_zone(zone, enveloppe.coefficients_b(batiment))
            for cle, attribut in ENVELOPPE.items():
                brut = sortie.texte(cle)
                if not brut:
                    continue
                x = ecart(getattr(e, attribut), float(brut), decimales(brut))
                bilan[cle].append(x)
                if x > TOLERANCE:
                    pires[cle].append((round(x, 3), info["projet"], nom, zone.texte("Name")[:20], round(getattr(e, attribut), 2), float(brut)))
    print(f"{len(lot) - illisibles} RSEE lus ({illisibles} illisibles), {n_zones} zones")
    print(f"{'indicateur':<11}{'zones':>6}{'dans 1 %':>10}{'médiane':>9}{'max':>8}")
    for cle in ENVELOPPE:
        v = bilan[cle]
        if v:
            print(f"{cle:<11}{len(v):>6}{sum(x <= TOLERANCE for x in v) / len(v):>10.0%}{statistics.median(v):>9.1%}{max(v):>8.0%}")
    return pires


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[2] if len(sys.argv) > 2 else os.environ.get("OPENBCE_RSEE", "."))
    pires = enveloppe_tous(dossier)
    for cle, liste in pires.items():
        print(f"\n{cle} : {len(liste)} zones hors tolérance ; les plus fortes :")
        for x in sorted(liste, reverse=True)[:5]:
            print("   ", x)
