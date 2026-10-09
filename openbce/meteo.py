# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Données météorologiques conventionnelles de la RE2020.

Source : classeur publié par le ministère (« Données météorologiques conventionnelles de la RE2020 »), 16 feuilles :
8 zones climatiques (H1a, H1b, H1c, H2a, H2b, H2c, H2d, H3) en deux jeux, Th-BC (calcul des besoins et des
consommations) et Th-D (confort d'été, avec séquence caniculaire). 8 760 heures par feuille.

Le classeur n'est pas copié dans le dépôt : `outils/meteo_officielle.py` le télécharge à sa source, `convertir()` le
transforme une fois en fichier .npz, que `charger()` relit.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

ZONES = ("H1a", "H1b", "H1c", "H2a", "H2b", "H2c", "H2d", "H3")
JEUX = ("Th-BC", "Th-D")
# colonnes du classeur, dans l'ordre : heure, température extérieure (°C), humidité spécifique, rayonnement direct
# normal (W/m²), rayonnement diffus horizontal (W/m²), température du ciel (°C), vent (m/s), température de l'eau
# froide (°C), hauteur du soleil gamma (°), puis une dernière colonne quand elle existe (azimut psi)
GRANDEURS = ("h", "te0", "we0", "dirN", "diff", "teciel", "vent", "teau", "gamma", "psi")


def convertir(classeur: str | Path, sortie: str | Path) -> dict[str, tuple[int, int]]:
    import openpyxl

    wb = openpyxl.load_workbook(classeur, read_only=True, data_only=True)
    tables, formes = {}, {}
    for ws in wb.worksheets:
        zone, _, jeu = ws.title.partition("_")
        if zone not in ZONES or jeu not in JEUX:
            continue
        lignes = [r for r in ws.iter_rows(min_row=2, values_only=True) if r and isinstance(r[0], (int, float))]
        t = np.array([[float(x) if isinstance(x, (int, float)) else np.nan for x in r[:len(GRANDEURS)]] for r in lignes])
        tables[f"{zone}|{jeu}"] = t
        formes[ws.title] = t.shape
    wb.close()                                   # en lecture seule, openpyxl garde le fichier ouvert (verrou sous Windows)
    np.savez_compressed(sortie, **tables)
    return formes


def charger(fichier: str | Path, zone: str, jeu: str = "Th-BC") -> dict[str, np.ndarray]:
    """Renvoie les séries horaires de la zone, une par grandeur (8 760 valeurs)."""
    if zone not in ZONES or jeu not in JEUX:
        raise ValueError(f"zone {zone!r} ou jeu {jeu!r} inconnu")
    with np.load(fichier) as z:
        t = z[f"{zone}|{jeu}"]
    return {g: t[:, i] for i, g in enumerate(GRANDEURS[:t.shape[1]])}
