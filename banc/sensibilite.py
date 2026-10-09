# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Essai de sensibilité : quelle correction des infiltrations et de la ventilation rapproche le mieux le chauffage
calculé de celui des RSEE ? Trois passes (base, infiltrations doublées, échangeur sans récupération), puis ajustement
linéaire par moindres carrés. Sert à trancher entre des lectures du texte, pas à caler le moteur.

    python -m banc.sensibilite <dossier de RSEE>
"""
import json
import sys
from pathlib import Path

import numpy as np

from banc import besoins
from openbce import groupe, rsee


def passe(dossier, fichiers):
    r = {}
    for f in fichiers:
        try:
            for _, zone, usage, surface, ch, ch_ref, *_ in besoins.comparer(str(dossier / f)):
                r[(f, zone)] = (ch, ch_ref)
        except Exception:
            pass
    return r


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    fichiers, projets = [], set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        if x["projet"] in projets or not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            continue
        if {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")} <= {0, 2, 3}:
            fichiers.append(x["fichier"])
            projets.add(x["projet"])
    base = passe(dossier, fichiers)
    groupe.FACTEUR_INFILTRATION = 2.0
    double = passe(dossier, fichiers)
    groupe.FACTEUR_INFILTRATION, groupe.EPSILON_BBIO = 1.0, 0.0
    sans = passe(dossier, fichiers)
    cles = [k for k in base if k in double and k in sans and base[k][1].sum() >= 3]
    for nom, sel in (("année", slice(0, 12)), ("décembre à février", [0, 1, 11])):
        y = np.array([base[k][1][sel].sum() for k in cles])
        c0 = np.array([base[k][0][sel].sum() for k in cles])
        d_inf = np.array([double[k][0][sel].sum() for k in cles]) - c0
        d_vent = np.array([sans[k][0][sel].sum() for k in cles]) - c0
        print(f"{nom} : {len(cles)} zones de {len(fichiers)} projets")
        for titre, X in (("base", None), ("infiltrations seules", d_inf[:, None]), ("ventilation seule", d_vent[:, None]), ("les deux", np.c_[d_inf, d_vent])):
            if X is None:
                coef, calc = [], c0
            else:
                coef, *_ = np.linalg.lstsq(X / y[:, None], (y - c0) / y, rcond=None)
                calc = c0 + X @ coef
            e = calc / y - 1
            print(f"   {titre:<22} coefficients {np.round(coef, 2)}  écart médian {np.median(e):+.0%}, |écart| médian {np.median(abs(e)):.0%}, de {e.min():+.0%} à {e.max():+.0%}")
    print("lecture : infiltrations x(1 + coefficient) ; efficacité de l'échangeur 0,5 x (1 - coefficient)")
