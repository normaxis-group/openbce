# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Bilans du mode Th-C (annexe III, fiches 13.2, 13.3, 13.4 et 4.7) : énergie finale par poste et par énergie, forfait de
refroidissement des groupes non climatisés, usages mobiliers, énergie primaire.

Coefficients d'énergie primaire (tableau 337) : électricité 2,3 ; gaz, fioul, charbon, réseau 1 ; bois 1 en énergie
primaire totale et 0 en non renouvelable ; réseau de chaleur 1 - RatENR en non renouvelable. Le Cep ne compte pas les
usages mobiliers (2488 à 2490).

Forfait de refroidissement (13.3, 2494 à 2497) : pour un groupe non climatisé d'un calcul Th-C, consommation
d'électricité fictive proportionnelle aux degrés-heures d'inconfort du Th-D au-delà de 350 °C.h et jusqu'à DH_max,
par un coefficient d'usage (tableau 339) et un coefficient de zone climatique et d'altitude (tableau 340), le tout
ramené en énergie finale (division par 2,3). Elle s'ajoute aux valeurs annuelles de froid et d'électricité du groupe,
de la zone et du bâtiment, pas aux mensuels.
"""
from __future__ import annotations

import numpy as np

ENERGIES = {10: "gaz", 20: "fioul", 30: "charbon", 40: "bois", 50: "elec", 60: "reseau"}
COEF_EP = {"gaz": 1.0, "fioul": 1.0, "charbon": 1.0, "bois": 1.0, "elec": 2.3, "reseau": 1.0}
POSTES = ("ch", "fr", "ecs", "ecl", "auxvent", "auxdist", "depl", "mobilier")

SEUIL_BAS_DH = 350.0                                                              # °C.h (13.3)
COEF_FR_PAR_DH = {1: 0.011, 2: 0.011, 3: 0.009, 4: 0.016, 5: 0.016}             # kWhep/(m².an.°C.h), tableau 339
COEF_ZONE_ALT = {"H1a": (0.8, 0.6, 0.4), "H1b": (1.0, 0.8, 0.6), "H1c": (1.0, 0.8, 0.6), "H2a": (0.7, 0.5, 0.3),
                 "H2b": (1.0, 0.8, 0.6), "H2c": (1.1, 0.9, 0.7), "H2d": (1.2, 1.0, 0.8), "H3": (1.2, 1.0, 0.8)}   # tableau 340


def coef_ep_nr(energie: str, rat_enr_reseau: float = 0.0, poste: str = "ch") -> float:
    if energie == "elec":
        return 2.3
    if energie == "bois":
        return 0.0
    if energie == "reseau":
        return 1.0 if poste == "fr" else 1.0 - rat_enr_reseau
    return 1.0


def forfait_froid(usage: int, climatise: bool, dh: float, dh_max: float | None, zone: str, altitude: float) -> float:
    """Électricité fictive de refroidissement d'un groupe non climatisé, kWhef/m².an (2494). Nulle si le groupe est
    climatisé, si DH ≤ 350 °C.h ou si l'usage n'a pas de seuil (bureaux en catégorie 3)."""
    if climatise or dh <= SEUIL_BAS_DH or usage not in COEF_FR_PAR_DH:
        return 0.0
    colonne = 0 if altitude < 400 else (1 if altitude < 800 else 2)
    plafond = min(dh, dh_max) if dh_max else dh
    return COEF_FR_PAR_DH[usage] * max(0.0, plafond - SEUIL_BAS_DH) * COEF_ZONE_ALT[zone][colonne] / COEF_EP["elec"]


def mobilier(apports_usages: np.ndarray, surface: float) -> float:
    """Consommation des usages mobiliers de la zone, kWhef/m².an (4.7, 93 à 95) : égale aux apports internes de chaleur
    non dus aux occupants, en Wh sur un pas d'une heure."""
    return float(np.sum(apports_usages)) / 1000.0 / surface if surface > 0 else 0.0


def cep(cef_par_energie: dict[str, float]) -> float:
    """Énergie primaire totale, kWhep/m².an, à partir des énergies finales importées par énergie (hors mobilier)."""
    return sum(v * COEF_EP[e] for e, v in cef_par_energie.items())


def cep_nr(cef_par_energie_et_poste: dict[tuple[str, str], float], rat_enr_reseau: float = 0.0) -> float:
    return sum(v * coef_ep_nr(e, rat_enr_reseau, p) for (e, p), v in cef_par_energie_et_poste.items())
