# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Éclairage et ventilation des parkings (fiches 10.4 et 10.3).

Un parking est décrit au niveau du projet ; sa consommation est répartie entre les zones au prorata de leur surface
de référence. Dans les RSEE elle est comptée dans le poste « déplacement » (constat du banc : le texte l'annonce
dans les postes éclairage et auxiliaires de ventilation).

Codes des RSEE : Type_Parking 0 = intérieur, 1 = extérieur ; Type_Usage 0 = bureau, 1 = commerce, 2 = habitat ;
Pec_ins en kW. Le tableau 324 est relevé sur l'image de la page 1288 (cellules fusionnées).
"""
from __future__ import annotations

import numpy as np

from .calendrier import Calendrier

TAU_DET = 0.2                                   # part de la puissance appelée en détection de présence (2349)
P_DEFAUT = {0: 75.0, 1: 8.0}                    # W par place, intérieur et extérieur (2350, 2351)
PVENT600_DEFAUT = 40.0                          # W par place (2327)
OUVERTURE = {0: ((9, 19), (0, 0)), 1: ((7, 22), (7, 22)), 2: ((0, 24), (0, 24))}   # semaine, week-end, par Type_Usage (10.4.3.2)

# Tableau 327 : besoin d'éclairage d'un parking extérieur selon l'heure légale de fin de pas (1 à 24)
FH_EXT = np.array([1, 1, 1, 1, 1, 1, 0.79, 0.48, 0.15, 0, 0, 0, 0, 0, 0, 0, 0.03, 0.2, 0.36, 0.5, 0.65, 0.84, 1, 1])
# Tableau 324 : mouvements par place selon l'heure légale de fin de pas (1 à 24)
RMVTPL = {
    0: np.array([0] * 8 + [0.308] * 3 + [0.154, 0, 0.154, 0.154, 0, 0.308, 0.308] + [0] * 6),
    1: np.array([0] * 7 + [0.278] + [0.556] * 12 + [0.278] * 2 + [0] * 2),
    2: np.array([0] * 7 + [0.19] * 3 + [0.095] * 6 + [0.19] * 3 + [0.095] * 3 + [0] * 2),
}
# Constantes de la ventilation hors habitation (tableau 323)
EFF_VENT, CCO_LIM, PROD_CO_VEH, R_UTIL, D_FIX, V_MOY, RL, S_PL = 0.5, 5e-5, 0.35, 1.0, 0.01, 10000.0, 2.0, 12.0


def _dans(heure: np.ndarray, plages) -> np.ndarray:
    r = np.zeros(heure.shape, dtype=bool)
    for a, b in plages:
        r |= ((heure >= a) & (heure < b)) if a <= b else ((heure >= a) | (heure < b))      # une plage peut passer minuit
    return r


def _plages(texte: str) -> list[tuple[float, float]]:
    v = [float(x) for x in (texte or "").split()]
    return list(zip(v[0::2], v[1::2]))


def eclairage(parking, cal: Calendrier) -> np.ndarray:
    """Puissance horaire appelée par l'éclairage du parking, W (2354)."""
    type_, usage, npl = parking.entier("Type_Parking"), parking.entier("Type_Usage"), parking.nombre("Npl")
    pec = P_DEFAUT[type_] * npl if parking.entier("IsParamEclPuisDefaut", 0) == 1 else 1000 * parking.nombre("Pec_ins")
    heure, semaine = cal.case - 1, cal.jour_semaine <= 5
    ouv_se, ouv_we = OUVERTURE[usage]
    ouv = np.where(semaine, _dans(heure, [ouv_se]), _dans(heure, [ouv_we]))
    if usage == 1:
        ouv &= cal.jour_semaine != 7                                    # commerces fermés le dimanche
    if parking.entier("IsParamEclHdDefaut", 0) == 1:
        det = np.zeros(heure.shape, dtype=bool)                         # pas de détection par défaut
    else:
        det = np.where(semaine, _dans(heure, _plages(parking.texte("PlagDse"))), _dans(heure, _plages(parking.texte("PlagDwe"))))
    fh = FH_EXT[cal.case - 1] if type_ == 1 else 1.0
    return pec * (ouv * fh * np.where(det, TAU_DET, 1.0) + (~ouv) * parking.entier("Ex", 0))


def ventilation(parking, cal: Calendrier) -> np.ndarray:
    """Puissance horaire des ventilateurs du parking, W (2334 à 2346)."""
    n = len(cal.case)
    type_, usage, npl = parking.entier("Type_Parking"), parking.entier("Type_Usage"), parking.nombre("Npl")
    if type_ == 1 or parking.entier("Vent", 0) == 0:
        return np.zeros(n)
    mouvements = RMVTPL[usage][cal.case - 1]
    if usage == 2:
        p600 = PVENT600_DEFAUT if parking.entier("IsParamVentilationHabDefaut", 0) == 1 else parking.nombre("Pvent600")
        return p600 * npl * R_UTIL * (mouvements if parking.entier("Reg", 0) == 1 else np.ones(n))        # (2344, 2346)
    if parking.entier("IsParamVentilationDefaut", 0) == 1:
        d1, d2, p1, p2 = 450 * npl, 900 * npl, 5 * npl, 40 * npl                                         # (2327)
    else:
        d1, d2, p1, p2 = (parking.nombre(k) for k in ("Dvent1", "Dvent2", "Pvent1", "Pvent2"))
    net = max(parking.entier("Net", 1), 1)
    larg = (S_PL * npl / net / RL) ** 0.5                                                                # (2328)
    peri = 2 * RL * larg + 2 * larg
    duree = D_FIX + peri * (net / 4 + 0.25) / V_MOY                                                      # (2331 à 2333)
    dreq = PROD_CO_VEH * npl * R_UTIL * mouvements * duree / (CCO_LIM * EFF_VENT)                        # (2336 à 2338)
    # le parking est ouvert tous les jours (NbjO = 1) : pas de mise à zéro du débit
    return np.where(dreq < d1, dreq * p1 / d1, dreq * p2 / d2)                                           # (2340 à 2343)


def du_projet_horaire(entree, cal: Calendrier) -> np.ndarray:
    """Consommation horaire de tous les parkings du projet (éclairage et ventilation), Wh."""
    total = np.zeros(len(cal.case))
    for p in entree.tous("Parking"):
        total += eclairage(p, cal) + ventilation(p, cal)
    return total


def du_projet(entree, cal: Calendrier, sref: dict[tuple[int, int], float]) -> dict[tuple[int, int], float]:
    """Consommation annuelle des parkings attribuée à chaque zone, Wh, par (Index de bâtiment, Index de zone).

    `sref` donne la surface de référence de chaque zone du projet.
    """
    total = sum((eclairage(p, cal) + ventilation(p, cal)).sum() for p in entree.tous("Parking"))
    surface = sum(sref.values())
    return {cle: total * s / surface for cle, s in sref.items()} if surface > 0 else dict.fromkeys(sref, 0.0)
