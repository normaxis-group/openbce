# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Calendrier conventionnel de la simulation (annexe III, fiches 3.1 et 4.1.3.1).

La simulation parcourt 8 760 pas d'une heure, comptés en temps UTC à partir de 0. Les scénarios d'usage sont décrits
en heure légale, sur une année qui commence un lundi et dont les mois comptent 4 ou 5 semaines entières.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

HEURES = 8760
SEMAINES_PAR_MOIS = (4, 4, 5, 4, 5, 4, 4, 5, 4, 4, 5, 4)
JOURS_PAR_MOIS_CIVIL = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
# heure d'été : du pas 1896 au pas 7031 inclus (tableau de la fiche 4.1.3.1)
ETE_DEBUT, ETE_FIN = 1896, 7031


@dataclass(frozen=True)
class Calendrier:
    ehlo: np.ndarray           # décalage entre l'heure légale et l'heure UTC : 1 en hiver, 2 en été
    case: np.ndarray           # case horaire du scénario, de 1 à 24 (heure légale de début + 1)
    jour_semaine: np.ndarray   # 1 = lundi ... 7 = dimanche, en heure légale
    semaine: np.ndarray        # semaine du mois, de 1 à 4 ou 5
    mois: np.ndarray           # mois conventionnel des scénarios, de 1 à 12
    mois_civil: np.ndarray     # mois du calendrier civil (31, 28, 31... jours), en temps UTC, pour les bilans mensuels


def construire() -> Calendrier:
    h = np.arange(HEURES)
    ehlo = np.where((h >= ETE_DEBUT) & (h <= ETE_FIN), 2, 1)
    legal = h + ehlo                                   # heure légale de début du pas, comptée depuis le 1er janvier 0 h
    case = legal % 24 + 1
    # 52 semaines entières font 364 jours ; le 365e reprend au lundi de la première semaine. Le texte ne le dit pas :
    # les RSEE comptent 8 heures d'éclairage autorisé de plus que si ce jour prolongeait la semaine de vacances,
    # soit exactement un lundi ordinaire.
    jour = (legal // 24) % 364
    jour_semaine = jour % 7 + 1
    semaine_annee = jour // 7                          # 0 à 51
    bornes = np.cumsum(SEMAINES_PAR_MOIS)
    mois = np.searchsorted(bornes, semaine_annee, side="right") + 1
    semaine = semaine_annee - np.concatenate(([0], bornes))[mois - 1] + 1
    mois_civil = np.searchsorted(np.cumsum(JOURS_PAR_MOIS_CIVIL) * 24, h, side="right") + 1
    return Calendrier(ehlo, case, jour_semaine, semaine, mois, mois_civil)


def adultes_equivalents(usage: int, surface: float, nb_logements: int) -> float:
    """Nombre d'adultes équivalents d'une zone d'habitation (équations 32, 35 et 36).

    `surface` est la surface utile de la zone en maison (usage 1), la surface du local d'habitation en collectif (usage 2).
    """
    a = surface / nb_logements
    if usage == 1:
        nmax = 1.0 if a < 30 else (1.75 - 0.01875 * (70 - a) if a <= 70 else 0.025 * a)
    elif usage == 2:
        nmax = 1.0 if a < 10 else (1.75 - 0.01875 * (50 - a) if a <= 50 else 0.035 * a)
    else:
        raise ValueError("usage d'habitation attendu (1 ou 2)")
    return nb_logements * (nmax if nmax < 1.75 else 1.75 + 0.3 * (nmax - 1.75))
