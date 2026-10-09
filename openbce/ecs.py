# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Besoins d'eau chaude sanitaire (fiches 9.5 C_EMI_Emission_ECS et 9.6 C_EIN_besoins_ECS).

Le besoin horaire d'un émetteur ECS équivalent est l'énergie qui porte de la température d'eau froide à 40 °C le
volume puisé dans l'heure (1694). Le volume hebdomadaire vient du nombre d'adultes équivalents de l'émetteur
(1684 à 1692), corrigé des émetteurs et des appareils sanitaires (1677 à 1679), puis réparti par la clé horaire
ah = facteur de la semaine × profil du jour (équation 46 de la fiche des scénarios).

Les récupérateurs de chaleur sur eaux grises (9.6.3.5) ne sont pas traités : `besoins` lève NotImplementedError.
"""
from __future__ import annotations

import numpy as np

from . import scenarios
from .calendrier import Calendrier

RHO_CW = 1.163          # ρw.cw, Wh/(L.K) (tableau 277)
THETA_UW = 40.0         # température de l'eau mitigée au puisage, °C
A_MAX = 392.0           # litres à 40 °C par semaine et par adulte équivalent (1687, 1691)
A_SURFACE = 40.0        # litres à 40 °C par semaine et par m² (1687, 1691)
A_TERTIAIRE = {3: 1.25} # litres par semaine et par m² de surface utile (tableau 278)

GAIN_EMETTEUR = (0.0, 0.05, 0.07)                 # mélangeurs, mitigeurs thermostatiques, temporisateurs (tableau 274)
RAT_DOUCHES_BAINS = {1: 0.8, 2: 0.8, 3: 0.5}      # tableau 275
# Tableau 276, rangé selon le code app_ecs des RSEE. L'ordre des codes n'est pas donné par le texte : il est déduit du
# banc (voir banc/ecs.py).
GAIN_APPAREIL = {0: 0.05, 1: 0.025, 2: 0.0, 3: -0.025}


def adultes_equivalents(usage: int, surface: float, nombre: int) -> float:
    """Nombre d'adultes équivalents d'un émetteur ECS desservant `nombre` maisons ou logements (1684 à 1690)."""
    a = surface / nombre
    if usage == 1:
        nmax = 1.0 if a < 30 else (1.75 - 0.01875 * (70 - a) if a < 70 else 0.025 * a)
    else:
        nmax = 1.0 if a < 10 else (1.75 - 0.01875 * (50 - a) if a < 50 else 0.035 * a)
    return nombre * (nmax if nmax < 1.75 else 1.75 + 0.3 * (nmax - 1.75))


def volume_hebdomadaire(usage: int, surface: float, emetteur) -> float:
    """Litres d'eau à 40 °C puisés par semaine par un émetteur ECS équivalent, avant correction (1692)."""
    a_em = emetteur.nombre("Rat_em_e", 1.0) * surface                                   # (1675)
    if usage in (1, 2):
        nombre = emetteur.entier("nb_maison_gr_e" if usage == 1 else "nb_lgt_gr_em_e", 0)
        if nombre <= 0:
            raise ValueError("émetteur ECS sans nombre de logements")
        return min(A_MAX * adultes_equivalents(usage, a_em, nombre), A_SURFACE * a_em)  # a × Nu
    return A_TERTIAIRE[usage] * emetteur.nombre("nu_gr_em_e", 0.0)


def correction(usage: int, emetteur) -> float:
    """Coefficient correctif des émetteurs et des appareils sanitaires (1677 à 1679)."""
    parts = (emetteur.nombre("part_em_e_melangeurs", 0.0), emetteur.nombre("part_em_e_mitigeur_thermo", 0.0), emetteur.nombre("part_em_e_temporisateur", 0.0))
    corr_em = 1 - sum(p * g for p, g in zip(parts, GAIN_EMETTEUR))
    corr_app = 1 - RAT_DOUCHES_BAINS[usage] * GAIN_APPAREIL[emetteur.entier("app_ecs", 2)]
    return corr_em * corr_app


def cle_horaire(cal: Calendrier, usage: int) -> np.ndarray:
    """Part du volume hebdomadaire puisée à chaque heure de l'année (équation 46).

    La clé hebdomadaire est celle du tableur officiel des scénarios. Elle était recopiée ici depuis le PDF, arrondie
    (0,022 pour 0,0215, 0,025 pour 0,0253) : sa somme valait 1,002 en logement et 0,99 en bureaux, et le banc des
    besoins d'ECS portait un biais constant de +0,35 % sur 182 groupes.
    """
    t = next(t for t in scenarios._tables()[scenarios.USAGES[usage]]["tableaux"] if t["nom"].startswith("ECS"))
    hebdo = np.array(t["hebdo"], dtype=float)
    annuel = np.array([[0.0 if v is None else v for v in ligne] for ligne in t["annuel"]])[cal.semaine - 1, cal.mois - 1]
    return hebdo[cal.jour_semaine - 1, cal.case - 1] * annuel


def besoins(groupe, usage: int, cal: Calendrier, teau: np.ndarray, corrige: bool = True) -> np.ndarray:
    """Besoins horaires d'ECS du groupe, en Wh (1694), ou besoins bruts sans correction (1695)."""
    surface = groupe.nombre("SHAB" if usage in (1, 2) else "SU")
    volume = 0.0
    for em in groupe.directs("Emetteur_ECS"):
        if em.entier("Nb_douches_bains_relies", 0) > 0:
            raise NotImplementedError("récupérateur de chaleur sur eaux grises")
        volume += volume_hebdomadaire(usage, surface, em) * (correction(usage, em) if corrige else 1.0)
    return RHO_CW * volume * cle_horaire(cal, usage) * (THETA_UW - teau)
