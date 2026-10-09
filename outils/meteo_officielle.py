# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Télécharge les données météorologiques conventionnelles de la RE2020 à leur source et les convertit pour OpenBCE.

    python outils/meteo_officielle.py [sortie.npz]          # par défaut : donnees/meteo_re2020.npz

Le classeur est publié par le ministère sur rt-re-batiment.developpement-durable.gouv.fr (rubrique « Documents
complémentaires »). Il n'est pas copié dans ce dépôt : chacun le récupère à la source, puis `meteo.convertir` en tire
le fichier .npz que lisent le banc et l'API.
"""
from __future__ import annotations

import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openbce import meteo  # noqa: E402

URL = "https://rt-re-batiment.developpement-durable.gouv.fr/IMG/xlsx/4_scenarios_meteorologiques_th-bc_th-d_re2020.xlsx"


def main() -> None:
    sortie = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "donnees" / "meteo_re2020.npz"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        classeur = Path(d) / "meteo_re2020.xlsx"
        requete = urllib.request.Request(URL, headers={"User-Agent": "OpenBCE"})
        with urllib.request.urlopen(requete, timeout=300) as r, open(classeur, "wb") as f:
            f.write(r.read())
        formes = meteo.convertir(classeur, sortie)
    print(f"{len(formes)} feuilles converties dans {sortie}")


if __name__ == "__main__":
    main()
