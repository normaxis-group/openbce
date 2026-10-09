# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Exigences de l'annexe à l'article R. 172-4 du CCH (chapitres I à IV, version consolidée après le décret n° 2024-1258
du 30 décembre 2024 et l'extension aux usages 6 à 28 pour les permis déposés à compter du 1er mai 2026) : Bbio_max,
Cep,nr_max, Cep_max et DH_max, avec leurs coefficients de modulation.

    Bbio_max = Bbio_maxmoyen x (1 + Mbgeo + Mbcombles + Mbsurf_moy + Mbsurf_tot + Mbbruit)
    Cep,nr_max = Cep,nr_maxmoyen x (1 + Mcgeo + Mccombles + Mcsurf_moy + Mcsurf_tot + Mccat), Cep_max de même avec Cep_maxmoyen

Mbsurf_moy et Mcsurf_moy se calculent par partie de bâtiment (surface moyenne des logements de la zone), Mbsurf_tot et
Mcsurf_tot sur la somme des surfaces de référence des parties de même usage (chapitre II). Usages 1 à 3 : vérifiés au
banc (banc/exigences.py) sur les sorties O_Mb* et O_Bbio_Max des RSEE. Usages 4 à 28 : tables lues dans le texte
(specs/usages/exigences-28-usages.md, pages de l'annexe R. 172-4 chapitres I à III), sans récapitulatif de référence.
"""
from __future__ import annotations

from openbce import usages as mod_usages

ZONES = ("H1a", "H1b", "H1c", "H2a", "H2b", "H2c", "H2d", "H3")
USAGES = dict(mod_usages.NOMS)

# ------------------------------------------------------------------ Bbio (chapitre III, I, p. 6 à 28)
BBIO_MAX_MOYEN = {1: 63.0, 2: 65.0, 3: 95.0, 4: 68.0, 5: 68.0, 6: 117.0, 7: 122.0, 8: 76.0, 9: 76.0, 10: 134.0, 11: 163.0, 12: 139.0,
                  13: 245.0, 14: 100.0, 15: 206.0, 16: 177.0, 17: 170.0, 18: 225.0, 19: 174.0, 20: 164.0, 21: 133.0, 22: 248.0,
                  23: 257.0, 24: 69.0, 25: 94.0, 26: 76.0, 27: 116.0, 28: 94.0}     # points, p. 6

# Mbgeo par usage : trois lignes d'altitude (< 400 m, 400 à 800 m, > 800 m), huit zones climatiques (p. 7 à 28).
MBGEO = {
    1: ((0.15, 0.2, 0.2, -0.05, 0.0, -0.1, 0.05, -0.1), (0.4, 0.5, 0.45, 0.15, 0.3, 0.05, 0.1, -0.05), (0.75, 0.85, 0.75, 0.55, 0.65, 0.35, 0.25, 0.1)),
    2: ((0.1, 0.2, 0.15, -0.1, 0.0, -0.1, 0.0, -0.1), (0.4, 0.5, 0.45, 0.2, 0.3, 0.1, 0.2, -0.05), (0.8, 0.85, 0.75, 0.6, 0.65, 0.4, 0.4, 0.15)),
    3: ((0.05, 0.10, 0.20, -0.05, 0.0, 0.10, 0.30, 0.25), (0.25, 0.25, 0.20, 0.20, 0.20, 0.10, 0.10, -0.05), (0.45, 0.45, 0.40, 0.40, 0.35, 0.25, 0.30, 0.10)),
    4: ((0.10, 0.20, 0.25, -0.10, 0.0, 0.05, 0.50, 0.50), (0.25, 0.30, 0.25, 0.05, 0.10, 0.0, 0.35, 0.25), (0.45, 0.45, 0.40, 0.30, 0.35, 0.20, 0.30, 0.20)),
    6: ((0.05, 0.2, 0.25, -0.1, 0.0, 0.0, 0.3, 0.2), (0.2, 0.3, 0.3, 0.0, 0.1, 0.0, 0.25, 0.15), (0.4, 0.5, 0.40, 0.15, 0.3, 0.1, 0.25, 0.15)),
    7: ((0.1, 0.2, 0.2, -0.05, 0.0, 0.0, 0.2, 0.2), (0.3, 0.35, 0.35, 0.1, 0.2, 0.05, 0.25, 0.15), (0.5, 0.6, 0.5, 0.3, 0.4, 0.2, 0.25, 0.15)),
    8: ((0.15, 0.2, 0.2, 0.0, 0.0, -0.1, 0.0, -0.15), (0.45, 0.45, 0.4, 0.25, 0.3, 0.15, 0.15, -0.05), (0.75, 0.8, 0.7, 0.6, 0.6, 0.4, 0.4, 0.15)),
    9: ((0.15, 0.2, 0.2, 0.0, 0.0, -0.1, 0.0, -0.15), (0.45, 0.45, 0.4, 0.25, 0.3, 0.15, 0.15, -0.05), (0.75, 0.75, 0.65, 0.6, 0.6, 0.4, 0.4, 0.15)),
    10: ((0.1, 0.15, 0.25, -0.1, 0.0, 0.0, 0.35, 0.25), (0.25, 0.3, 0.35, 0.05, 0.15, 0.05, 0.3, 0.15), (0.45, 0.55, 0.5, 0.3, 0.35, 0.2, 0.35, 0.15)),
    11: ((0.05, 0.15, 0.2, -0.1, 0.0, -0.05, 0.25, 0.1), (0.25, 0.3, 0.3, 0.1, 0.15, 0.05, 0.25, 0.1), (0.45, 0.5, 0.45, 0.3, 0.35, 0.20, 0.3, 0.15)),
    12: ((0.1, 0.15, 0.1, 0.0, 0.0, -0.1, 0.1, 0.0), (0.25, 0.3, 0.25, 0.15, 0.2, 0.05, 0.1, 0.05), (0.45, 0.5, 0.4, 0.4, 0.4, 0.25, 0.25, 0.15)),
    13: ((0.05, 0.1, 0.2, -0.05, 0.0, 0.05, 0.25, 0.15), (0.15, 0.2, 0.25, 0.05, 0.1, 0.05, 0.25, 0.15), (0.3, 0.35, 0.35, 0.2, 0.25, 0.15, 0.30, 0.15)),
    14: ((0.1, 0.15, 0.2, 0.0, 0.0, -0.05, 0.2, 0.1), (0.3, 0.35, 0.3, 0.2, 0.2, 0.05, 0.2, 0.15), (0.55, 0.55, 0.5, 0.45, 0.45, 0.25, 0.3, 0.2)),
    15: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.0, 0.15, 0.1), (0.20, 0.25, 0.25, 0.1, 0.15, 0.05, 0.2, 0.1), (0.35, 0.4, 0.35, 0.25, 0.3, 0.15, 0.25, 0.15)),
    16: ((0.05, 0.15, 0.15, -0.05, 0.0, 0.0, 0.2, 0.1), (0.2, 0.25, 0.25, 0.05, 0.15, 0.05, 0.2, 0.15), (0.35, 0.4, 0.35, 0.25, 0.3, 0.15, 0.3, 0.2)),
    17: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.05, 0.3, 0.25), (0.1, 0.2, 0.2, 0.0, 0.1, 0.0, 0.25, 0.2), (0.2, 0.3, 0.25, 0.15, 0.2, 0.1, 0.25, 0.2)),
    18: ((0.05, 0.1, 0.1, -0.05, 0.0, -0.1, 0.0, -0.1), (0.3, 0.3, 0.25, 0.2, 0.25, 0.05, 0.1, 0.0), (0.55, 0.55, 0.5, 0.45, 0.5, 0.3, 0.25, 0.15)),
    19: ((0.1, 0.15, 0.15, -0.05, 0.0, -0.05, 0.05, -0.05), (0.25, 0.3, 0.25, 0.15, 0.15, 0.1, 0.1, -0.05), (0.45, 0.5, 0.45, 0.3, 0.35, 0.25, 0.2, 0.05)),
    20: ((0.05, 0.15, 0.2, -0.05, 0.0, 0.0, 0.2, 0.1), (0.25, 0.3, 0.3, 0.15, 0.2, 0.1, 0.25, 0.1), (0.45, 0.5, 0.45, 0.35, 0.4, 0.25, 0.35, 0.2)),
    21: ((0.05, 0.15, 0.2, -0.05, 0.0, 0.0, 0.25, 0.2), (0.15, 0.2, 0.2, 0.05, 0.05, 0.0, 0.2, 0.1), (0.25, 0.3, 0.25, 0.15, 0.2, 0.1, 0.15, 0.1)),
    22: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.05, 0.2, 0.2), (0.1, 0.15, 0.2, 0.0, 0.1, 0.05, 0.2, 0.15), (0.05, 0.15, -0.05, 0.0, 0.1, 0.25, 0.25, 0.05)),   # ligne > 800 m telle quelle (p. 23)
    23: ((0.05, 0.05, 0.1, -0.05, 0.0, 0.05, 0.25, 0.25), (0.05, 0.1, 0.1, 0.0, 0.05, 0.05, 0.2, 0.15), (0.1, 0.15, 0.15, 0.05, 0.1, 0.05, 0.2, 0.1)),
    24: ((0.1, 0.15, 0.25, -0.05, 0.0, 0.05, 0.4, 0.35), (0.2, 0.25, 0.3, 0.05, 0.1, 0.05, 0.4, 0.3), (0.35, 0.4, 0.45, 0.2, 0.25, 0.15, 0.35, 0.25)),
    25: ((0.0, 0.1, 0.25, -0.15, 0.0, 0.1, 0.55, 0.55), (0.0, 0.05, 0.15, -0.15, -0.05, -0.05, 0.4, 0.3), (0.05, 0.1, 0.15, -0.05, 0.0, -0.05, 0.25, 0.15)),
    26: ((0.15, 0.2, 0.15, -0.05, 0.0, -0.05, 0.1, 0.1), (0.35, 0.4, 0.35, 0.2, 0.25, 0.1, 0.2, 0.1), (0.65, 0.65, 0.6, 0.5, 0.55, 0.35, 0.35, 0.25)),
    27: ((0.1, 0.15, 0.15, -0.05, 0.0, -0.05, 0.1, 0.1), (0.3, 0.35, 0.3, 0.15, 0.2, 0.1, 0.2, 0.1), (0.55, 0.55, 0.5, 0.45, 0.45, 0.3, 0.35, 0.2)),
}
MBGEO[5] = MBGEO[4]      # « enseignement primaire ou secondaire », p. 10
MBGEO[28] = MBGEO[25]    # « 25. et 28. », p. 26

# Mbsurf_tot : morceaux (borne supérieure de S, a, b), valeur (a + b x S) / Bbio_maxmoyen tant que S <= borne, 0 au-delà du
# dernier morceau ; None = pas de borne. Usages absents : 0 partout (valeurs nulles explicites du texte). Bureaux : fonction à part.
MBSURF_TOT = {2: ((1300, 19.5, -0.015),), 4: ((500, 35.0, -0.05), (1000, 20.0, -0.02)), 5: ((1000, 45.0, -0.045),),
              17: ((500, 47.5, -0.095),), 21: ((2000, 22.0, -0.008),), 23: ((5000, 50.0, -0.01),), 24: ((5000, 65.0, -0.013),)}
# Mbbruit : habitation en zones de bruit BR2 et BR3 par zone climatique (BR1 : 0) ; autres usages : 0 en BR1 à BR3, valeur en
# catégorie de contraintes extérieures 3 (scalaire, ou tuple par zone climatique). Usages absents : 0.
MBBRUIT_BR23 = {1: (0, 0, 0, 0, 0, 0, 0.1, 0.1), 2: (0, 0, 0.1, 0, 0, 0.1, 0.2, 0.2)}
MBBRUIT_CAT3 = {3: 0.4, 6: (0.15, 0.1, 0.1, 0.15, 0.15, 0.2, 0.1, 0.15), 7: (0.1, 0.05, 0.1, 0.1, 0.15, 0.2, 0.1, 0.15), 8: 0.05, 9: 0.05,
                10: 0.3, 11: 0.3, 12: (0.05, 0.1, 0.15, 0.1, 0.15, 0.2, 0.25, 0.3), 17: 0.2}


def _par_morceaux(table, s: float) -> float:
    for borne, a, b in table:
        if borne is None or s <= borne:
            return a + b * s
    return 0.0


def mbgeo(usage: int, zone: str, altitude: float) -> float:
    ligne = 0 if altitude < 400 else (1 if altitude <= 800 else 2)
    return MBGEO[usage][ligne][ZONES.index(zone)]


def mbcombles(usage: int, s_combles: float, sref: float) -> float:
    return 0.4 * s_combles / sref if usage == 1 and sref > 0 else 0.0


def mbsurf_moy(usage: int, sref: float, nb_logements: int) -> float:
    """Formules du chapitre III. Banc : exactes en logement collectif et sur un projet de maisons ; sur les autres projets
    de maisons, les RSEE donnent une valeur calculée comme si la surface moyenne valait 1,02 fois Sref/NL (écart de 0,01
    sur Mbsurf_moy, 0,7 point de Bbio_max), sans explication dans le texte : on garde le texte."""
    if usage not in (1, 2) or nb_logements <= 0:
        return 0.0
    s = sref / nb_logements
    ref = BBIO_MAX_MOYEN[usage]
    if usage == 1:
        return (49 - 0.49 * s) / ref if s <= 100 else ((18 - 0.18 * s) / ref if s <= 150 else -9 / ref)
    return (-6 + 0.1 * s) / ref if s <= 80 else ((-2 + 0.05 * s) / ref if s <= 120 else 4 / ref)


def mbsurf_tot(usage: int, sref_usage: float, annee_permis: int = 2026) -> float:
    ref = BBIO_MAX_MOYEN[usage]
    s = sref_usage
    if usage == 3:                                                     # p. 9, selon l'année du permis
        if s <= 500:
            return (24 - 0.06 * s) / ref
        periode = 0 if annee_permis <= 2024 else (1 if annee_permis <= 2027 else 2)
        if s <= 4000:
            return ((-5.55 - 0.0009 * s), (-4.9 - 0.0022 * s), (-3.8 - 0.0044 * s))[periode] / ref
        if s <= 10000:
            return ((-5.55 - 0.0009 * s), (-9.7 - 0.001 * s), -21.4)[periode] / ref
        return (-14.55, -19.7, -21.4)[periode] / ref
    return _par_morceaux(MBSURF_TOT.get(usage, ()), s) / ref


def mbbruit(usage: int, zone: str, exposition_bruit: int, categorie_ce: int = 1) -> float:
    """exposition_bruit : classe BR du groupe (1, 2 ou 3 ; un Exp_BR_Groupe à 0 dans les RSEE est traité comme BR3, c'est ce
    que donne le banc) ; categorie_ce : catégorie de contraintes extérieures."""
    if usage in (1, 2):
        return 0.0 if exposition_bruit <= 1 else MBBRUIT_BR23[usage][ZONES.index(zone)]
    v = MBBRUIT_CAT3.get(usage)
    if v is None or categorie_ce < 3:
        return 0.0
    return v[ZONES.index(zone)] if isinstance(v, tuple) else v


def bbio_max(usage: int, zone: str, altitude: float, sref: float, nb_logements: int, sref_usage: float, s_combles: float = 0.0,
             exposition_bruit: int = 1, categorie_ce: int = 1, annee_permis: int = 2026) -> dict[str, float]:
    m = dict(mbgeo=mbgeo(usage, zone, altitude), mbcombles=mbcombles(usage, s_combles, sref), mbsurf_moy=mbsurf_moy(usage, sref, nb_logements),
             mbsurf_tot=mbsurf_tot(usage, sref_usage, annee_permis), mbbruit=mbbruit(usage, zone, exposition_bruit, categorie_ce))
    m["bbio_max"] = BBIO_MAX_MOYEN[usage] * (1 + sum(m.values()))
    return m


# ------------------------------------------------------------------ Cep,nr et Cep (chapitre III, II, p. 28 à 56)
CEP_NR_MAX_MOYEN = {1: 55.0, 2: 70.0, 3: 75.0, 4: 65.0, 5: 63.0, 6: 93.0, 7: 102.0, 8: 121.0, 9: 118.0, 10: 235.0, 11: 234.0, 12: 150.0,
                    13: 282.0, 14: 132.0, 15: 219.0, 16: 214.0, 17: 163.0, 18: 242.0, 19: 190.0, 20: 274.0, 21: 165.0, 22: 191.0,
                    23: 290.0, 24: 94.0, 25: 94.0, 26: 119.0, 27: 153.0, 28: 112.0}       # kWhep/(m².an), p. 28 et 29
CEP_MAX_MOYEN = {1: 75.0, 2: 85.0, 3: 85.0, 4: 72.0, 5: 72.0, 6: 105.0, 7: 112.0, 8: 144.0, 9: 138.0, 10: 252.0, 11: 281.0, 12: 182.0,
                 13: 578.0, 14: 275.0, 15: 446.0, 16: 412.0, 17: 182.0, 18: 306.0, 19: 252.0, 20: 302.0, 21: 180.0, 22: 253.0,
                 23: 365.0, 24: 116.0, 25: 116.0, 26: 251.0, 27: 329.0, 28: 148.0}
MCGEO = {
    1: ((0.1, 0.15, 0.1, -0.05, 0.0, -0.1, -0.10, -0.15), (0.4, 0.5, 0.4, 0.15, 0.3, 0.05, 0.0, -0.1), (0.75, 0.85, 0.75, 0.55, 0.6, 0.35, 0.25, 0.15)),
    2: ((0.05, 0.05, 0.05, -0.1, 0.0, -0.15, -0.1, -0.15), (0.35, 0.4, 0.35, 0.2, 0.2, 0.05, 0.05, -0.1), (0.55, 0.65, 0.55, 0.45, 0.5, 0.3, 0.3, 0.15)),
    3: ((0.05, 0.10, 0.10, 0.0, 0.0, 0.0, 0.15, 0.15), (0.20, 0.25, 0.20, 0.15, 0.15, 0.05, 0.10, -0.05), (0.35, 0.40, 0.35, 0.35, 0.30, 0.20, 0.25, 0.10)),
    4: ((0.05, 0.15, 0.10, -0.05, 0.0, -0.05, 0.40, 0.30), (0.30, 0.30, 0.30, 0.15, 0.20, 0.10, 0.30, 0.10), (0.60, 0.60, 0.60, 0.45, 0.50, 0.35, 0.35, 0.15)),
    6: ((0.1, 0.15, 0.1, -0.05, 0.0, -0.05, 0.15, 0.05), (0.25, 0.3, 0.2, 0.1, 0.15, 0.05, 0.1, 0.0), (0.5, 0.45, 0.4, 0.35, 0.35, 0.2, 0.2, 0.05)),
    7: ((0.05, 0.10, 0.10, -0.05, 0.0, 0.0, 0.2, 0.15), (0.1, 0.15, 0.15, 0.0, 0.05, 0.0, 0.1, 0.05), (0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0)),
    8: ((0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.05, 0.0), (0.2, 0.25, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05), (0.35, 0.35, 0.35, 0.25, 0.25, 0.2, 0.25, 0.1)),
    9: ((0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.05, 0.0), (0.2, 0.25, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05), (0.35, 0.35, 0.35, 0.25, 0.25, 0.2, 0.25, 0.1)),
    10: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.05, 0.15, 0.1), (0.1, 0.15, 0.15, 0.0, 0.05, 0.05, 0.15, 0.1), (0.2, 0.2, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05)),
    11: ((0.05, 0.1, 0.1, 0.0, 0.0, 0.0, 0.1, 0.1), (0.1, 0.15, 0.15, 0.05, 0.05, 0.05, 0.1, 0.05), (0.2, 0.25, 0.2, 0.15, 0.15, 0.1, 0.15, 0.05)),
    12: ((0.1, 0.1, 0.1, 0.0, 0.0, -0.05, 0.05, -0.05), (0.25, 0.25, 0.25, 0.2, 0.20, 0.1, 0.1, 0.0), (0.45, 0.4, 0.4, 0.35, 0.35, 0.25, 0.25, 0.15)),
    13: ((0.0, 0.05, 0.1, -0.05, 0.0, 0.05, 0.2, 0.15), (0.1, 0.1, 0.1, 0.0, 0.05, 0.05, 0.15, 0.05), (0.2, 0.2, 0.15, 0.10, 0.15, 0.10, 0.15, 0.05)),
    14: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, 0.05, -0.05), (0.25, 0.25, 0.2, 0.15, 0.2, 0.05, 0.1, 0.0), (0.4, 0.4, 0.35, 0.35, 0.35, 0.2, 0.2, 0.05)),
    15: ((0.05, 0.1, 0.05, -0.05, 0.0, 0.0, 0.15, 0.1), (0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05), (0.15, 0.2, 0.15, 0.1, 0.15, 0.05, 0.1, 0.05)),
    16: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.0, 0.1, 0.05), (0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.1, 0.0), (0.3, 0.3, 0.25, 0.2, 0.25, 0.15, 0.15, 0.05)),
    17: ((0.0, 0.05, 0.1, -0.05, 0.0, 0.05, 0.2, 0.2), (0.0, 0.1, 0.1, -0.05, 0.05, 0.05, 0.15, 0.15), (0.05, 0.1, 0.1, 0.0, 0.05, 0.05, 0.1, 0.1)),
    18: ((0.05, 0.1, 0.05, 0.0, 0.0, -0.05, 0.0, -0.05), (0.15, 0.15, 0.15, 0.1, 0.15, 0.05, 0.05, -0.05), (0.3, 0.3, 0.3, 0.25, 0.25, 0.15, 0.15, 0.05)),
    19: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, 0.0, -0.05), (0.25, 0.25, 0.2, 0.15, 0.15, 0.1, 0.1, -0.05), (0.4, 0.4, 0.35, 0.3, 0.35, 0.2, 0.25, 0.1)),
    20: ((0.05, 0.05, 0.1, 0.0, 0.0, 0.05, 0.1, 0.1), (0.05, 0.1, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05), (0.1, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05)),
    21: ((0.05, 0.1, 0.1, -0.05, 0.0, -0.05, 0.1, 0.1), (0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.15, 0.1), (0.3, 0.35, 0.3, 0.25, 0.25, 0.15, 0.2, 0.2)),
    22: ((-0.05, 0.0, 0.05, -0.05, 0.0, 0.0, 0.1, 0.1), (-0.05, 0.0, 0.05, -0.1, 0.1, 0.2, 0.25, 0.0), (0.05, 0.1, -0.05, 0.0, 0.05, 0.15, 0.15, 0.0)),
    23: ((0.05, 0.05, 0.1, -0.05, 0.0, 0.05, 0.15, 0.15), (0.05, 0.05, 0.1, 0.0, 0.05, 0.05, 0.1, 0.1), (0.1, 0.15, 0.15, 0.05, 0.1, 0.05, 0.1, 0.05)),
    24: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.0, 0.2, 0.15), (0.15, 0.15, 0.2, 0.05, 0.1, 0.05, 0.15, 0.1), (0.25, 0.3, 0.3, 0.2, 0.2, 0.1, 0.2, 0.1)),
    25: ((0.0, 0.1, 0.1, -0.1, 0.0, 0.0, 0.4, 0.25), (0.05, 0.1, 0.05, -0.05, 0.0, -0.05, 0.2, 0.05), (0.1, 0.15, 0.1, 0.05, 0.1, 0.0, 0.1, 0.0)),
    26: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, -0.05, -0.15), (0.25, 0.25, 0.2, 0.2, 0.2, 0.1, 0.05, -0.05), (0.45, 0.45, 0.4, 0.35, 0.4, 0.25, 0.20, 0.1)),
    27: ((0.05, 0.1, 0.05, 0.0, 0.0, 0.0, 0.0, -0.05), (0.2, 0.2, 0.15, 0.1, 0.15, 0.05, 0.05, 0.0), (0.3, 0.35, 0.3, 0.25, 0.25, 0.2, 0.15, 0.1)),
    28: ((0.0, 0.1, 0.05, -0.1, 0.0, 0.05, 0.35, 0.25), (0.0, 0.05, 0.05, -0.05, 0.0, -0.05, 0.15, 0.05), (0.05, 0.1, 0.05, 0.0, 0.05, 0.0, 0.1, -0.05)),
}
MCGEO[5] = MCGEO[4]      # p. 36
# Mcsurf_moy sur la surface moyenne des logements (p. 33 et 34), Mcsurf_tot sur la somme des Sref de même usage (p. 33 à 56) :
# mêmes morceaux que Mbsurf_tot, diviseur Cep,nr_maxmoyen. Usages absents : 0. Industrie 8 h à 18 h (24) : fonction à part.
MCSURF_MOY = {1: ((100, 49.5, -0.55), (150, 14.5, -0.2), (None, -15.5, 0.0)), 2: ((40, 45.0, -1.0), (80, 15.0, -0.25), (120, 3.0, -0.1), (None, -9.0, 0.0))}
MCSURF_TOT = {2: ((1300, 13.0, -0.01),), 3: ((500, 18.0, -0.032), (1500, 6.0, -0.008), (None, -6.0, 0.0)), 4: ((500, 12.5, -0.025),),
              5: ((500, 12.5, -0.025),), 9: ((1000, 81.0, -0.081),), 17: ((500, 113.0, -0.226),),
              21: ((2000, 0.0, 0.0), (5000, 49.0, -0.026), (None, -78.0, 0.0)), 23: ((5000, 15.0, -0.003),)}
# Mccat par catégorie de contraintes extérieures (p. 33 à 56) : tuple par zone climatique ou scalaire ; absent = 0.
MCCAT = {1: {2: (0, 0, 0, 0, 0, 0, 0.1, 0.1)}, 2: {2: (0, 0, 0, 0, 0, 0, 0.1, 0.1)}, 4: {2: 0.05}, 5: {2: 0.05},
         6: {3: (0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.2, 0.3)}, 7: {3: (0, 0, 0, 0, 0, 0, 0.05, 0.05)},
         12: {3: (0, 0.05, 0.05, 0, 0.05, 0.05, 0.2, 0.25)}, 17: {3: 0.05}}


def mcgeo(usage: int, zone: str, altitude: float) -> float:
    ligne = 0 if altitude < 400 else (1 if altitude <= 800 else 2)
    return MCGEO[usage][ligne][ZONES.index(zone)]


def mcsurf_moy(usage: int, sref: float, nb_logements: int) -> float:
    if usage not in MCSURF_MOY or nb_logements <= 0:
        return 0.0
    return _par_morceaux(MCSURF_MOY[usage], sref / nb_logements) / CEP_NR_MAX_MOYEN[usage]


def mcsurf_tot(usage: int, sref_usage: float, annee_permis: int = 2026, reseau_classe: bool = False) -> float:
    ref = CEP_NR_MAX_MOYEN[usage]
    s = sref_usage
    if usage == 24:                                                    # p. 52 : S <= 5 000 m², 0 au-delà
        if s > 5000:
            return 0.0
        return ((365 - 0.073 * s) if reseau_classe and annee_permis <= 2027 else (265 - 0.053 * s)) / ref
    return _par_morceaux(MCSURF_TOT.get(usage, ()), s) / ref


def mccat(usage: int, zone: str, categorie_ce: int = 1) -> float:
    v = MCCAT.get(usage, {}).get(min(categorie_ce, 3))
    if v is None:
        return 0.0
    return v[ZONES.index(zone)] if isinstance(v, tuple) else v


def cep_max(usage: int, zone: str, altitude: float, sref: float, nb_logements: int, sref_usage: float, categorie_ce: int = 1,
            annee_permis: int = 2026, reseau_classe: bool = False) -> dict[str, float]:
    """Cep,nr_max et Cep_max de la zone (chapitre II, II). Mccombles n'est pas codé (0) : le texte le réserve à l'usage 1 et le
    banc ne l'a pas encore mesuré. Aucune de ces valeurs n'est confrontée aux RSEE à ce jour."""
    m = dict(mcgeo=mcgeo(usage, zone, altitude), mccombles=0.0, mcsurf_moy=mcsurf_moy(usage, sref, nb_logements),
             mcsurf_tot=mcsurf_tot(usage, sref_usage, annee_permis, reseau_classe), mccat=mccat(usage, zone, categorie_ce))
    facteur = 1 + sum(m.values())
    m["cep_nr_max"] = CEP_NR_MAX_MOYEN[usage] * facteur
    m["cep_max"] = CEP_MAX_MOYEN[usage] * facteur
    return m


# ------------------------------------------------------------------ DH_max (chapitre III, IV, p. 87 à 93)
# Par usage : (catégorie 1, catégorie 1 climatisé en H2d ou H3, catégorie 2, catégorie 3) ; None = pas de seuil ; "ns" = colonne
# absente du texte (non spécifié : la valeur de catégorie 2 est reprise, ces usages n'ayant pas de catégorie 3 au texte).
DH_MAX = {3: (1150, 2400, 2600, None), 4: (900, 1800, 2200, "ns"), 5: (900, 1800, 2200, "ns"), 6: (900, 2200, 2400, None), 7: (900, 2200, 2400, None),
          8: (300, 700, 1000, None), 9: (300, 700, 1000, None), 10: (1300, 3300, 3400, None), 11: (1300, 3300, 3400, None), 12: (550, 1600, 1600, None),
          13: (2500, 5000, 5000, None), 14: (250, 650, 650, None), 15: (1600, 3500, 3500, None), 16: (1250, 2500, 2500, None), 17: (3300, 8000, 9500, None),
          18: (1000, 2200, 2200, "ns"), 19: (900, 2400, 2600, "ns"), 20: (900, 2400, 2600, "ns"), 21: (1250, 3000, 3300, None), 22: (12100, 21500, 21500, None),
          23: (3200, 8000, 8000, "ns"), 24: (900, 2200, 2200, "ns"), 25: (2000, 4600, 5000, "ns"), 26: (40, 170, 170, None), 27: (260, 650, 650, None),
          28: (2000, 4600, 5000, "ns")}


def dh_max(usage: int, zone: str, categorie_ce: int = 1, climatise: bool = False, smoy_logement: float = 0.0) -> float | None:
    """DH_max par catégorie de contraintes extérieures ; None = pas de seuil. « Climatisé en H2d ou H3 » relève la limite."""
    chaud = climatise and zone in ("H2d", "H3")
    if usage == 1:
        return 1850.0 if categorie_ce >= 2 else 1250.0
    if usage == 2:
        s = smoy_logement
        if categorie_ce >= 2:
            return 2600.0 if s <= 20 else (2850.0 - 12.5 * s if s <= 60 else 2100.0)
        if chaud:
            return 1600.0 if s <= 20 else (1700.0 - 5.0 * s if s <= 60 else 1400.0)
        return 1250.0
    cat1, cat1_chaud, cat2, cat3 = DH_MAX[usage]
    if categorie_ce >= 3:
        v = cat2 if cat3 == "ns" else cat3
        return None if v is None else float(v)
    if categorie_ce == 2:
        return float(cat2)
    return float(cat1_chaud if chaud else cat1)
