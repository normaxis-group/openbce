# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Exigences de l'annexe à l'article R. 172-4 du CCH (chapitres II et III, version consolidée après le décret
n° 2024-1258 du 30 décembre 2024) : Bbio_max et ses coefficients de modulation.

    Bbio_max = Bbio_maxmoyen x (1 + Mbgeo + Mbcombles + Mbsurf_moy + Mbsurf_tot + Mbbruit)

Mbsurf_moy se calcule par partie de bâtiment (surface moyenne des logements de la zone), Mbsurf_tot sur la somme des
surfaces de référence des parties de même usage (chapitre II, I). Le banc (banc/exigences.py) le vérifie sur les
sorties O_Mb* et O_Bbio_Max des RSEE.
"""
from __future__ import annotations

ZONES = ("H1a", "H1b", "H1c", "H2a", "H2b", "H2c", "H2d", "H3")
USAGES = {1: "maison", 2: "collectif", 3: "bureaux", 4: "enseignement primaire", 5: "enseignement secondaire"}
BBIO_MAX_MOYEN = {1: 63.0, 2: 65.0, 3: 95.0, 4: 68.0, 5: 68.0}

# Mbgeo par usage : trois lignes d'altitude (< 400 m, 400 à 800 m, > 800 m), huit zones climatiques.
MBGEO = {
    1: ((0.15, 0.2, 0.2, -0.05, 0.0, -0.1, 0.05, -0.1), (0.4, 0.5, 0.45, 0.15, 0.3, 0.05, 0.1, -0.05), (0.75, 0.85, 0.75, 0.55, 0.65, 0.35, 0.25, 0.1)),
    2: ((0.1, 0.2, 0.15, -0.1, 0.0, -0.1, 0.0, -0.1), (0.4, 0.5, 0.45, 0.2, 0.3, 0.1, 0.2, -0.05), (0.8, 0.85, 0.75, 0.6, 0.65, 0.4, 0.4, 0.15)),
    3: ((0.05, 0.10, 0.20, -0.05, 0.0, 0.10, 0.30, 0.25), (0.25, 0.25, 0.20, 0.20, 0.20, 0.10, 0.10, -0.05), (0.45, 0.45, 0.40, 0.40, 0.35, 0.25, 0.30, 0.10)),
    4: ((0.10, 0.20, 0.25, -0.10, 0.0, 0.05, 0.50, 0.50), (0.25, 0.30, 0.25, 0.05, 0.10, 0.0, 0.35, 0.25), (0.45, 0.45, 0.40, 0.30, 0.35, 0.20, 0.30, 0.20)),
}
MBGEO[5] = MBGEO[4]
# Mbbruit en zones de bruit BR2 et BR3, par zone climatique (BR1 : 0 partout).
MBBRUIT_BR23 = {1: (0, 0, 0, 0, 0, 0, 0.1, 0.1), 2: (0, 0, 0.1, 0, 0, 0.1, 0.2, 0.2)}
MBBRUIT_BUREAUX_CAT3 = 0.4     # bureaux : 0 en BR1, BR2 et BR3 ; 0,4 en catégorie de contraintes extérieures 3


def mbgeo(usage: int, zone: str, altitude: float) -> float:
    ligne = 0 if altitude < 400 else (1 if altitude <= 800 else 2)
    return MBGEO[usage][ligne][ZONES.index(zone)]


def mbcombles(usage: int, s_combles: float, sref: float) -> float:
    return 0.4 * s_combles / sref if usage == 1 and sref > 0 else 0.0


def mbsurf_moy(usage: int, sref: float, nb_logements: int) -> float:
    """Formules du chapitre III. Banc : exactes en logement collectif et sur un projet de maisons (cas 27) ; sur les
    autres projets de maisons, les RSEE donnent une valeur calculée comme si la surface moyenne valait 1,02 fois Sref/NL
    (écart de 0,01 sur Mbsurf_moy, 0,7 point de Bbio_max), sans explication dans le texte : on garde le texte."""
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
    if usage == 1:
        return 0.0
    if usage == 2:
        return (19.5 - 0.015 * s) / ref if s <= 1300 else 0.0
    if usage == 3:
        if s <= 500:
            return (24 - 0.06 * s) / ref
        periode = 0 if annee_permis <= 2024 else (1 if annee_permis <= 2027 else 2)
        if s <= 4000:
            return ((-5.55 - 0.0009 * s), (-4.9 - 0.0022 * s), (-3.8 - 0.0044 * s))[periode] / ref
        if s <= 10000:
            return ((-5.55 - 0.0009 * s), (-9.7 - 0.001 * s), -21.4)[periode] / ref
        return (-14.55, -19.7, -21.4)[periode] / ref
    if usage == 4:
        return (35 - 0.05 * s) / ref if s <= 500 else ((20 - 0.02 * s) / ref if s <= 1000 else 0.0)
    return (45 - 0.045 * s) / ref if s <= 1000 else 0.0


def mbbruit(usage: int, zone: str, exposition_bruit: int, categorie_ce: int = 1) -> float:
    """exposition_bruit : classe BR du groupe (1, 2 ou 3 ; un Exp_BR_Groupe à 0 dans les RSEE est traité comme BR3, c'est ce
    que donne le banc) ; categorie_ce : catégorie de contraintes extérieures."""
    if usage == 3:
        return MBBRUIT_BUREAUX_CAT3 if categorie_ce >= 3 else 0.0
    if usage in (4, 5) or exposition_bruit <= 1:
        return 0.0
    return MBBRUIT_BR23[usage][ZONES.index(zone)]


def bbio_max(usage: int, zone: str, altitude: float, sref: float, nb_logements: int, sref_usage: float, s_combles: float = 0.0,
             exposition_bruit: int = 1, categorie_ce: int = 1, annee_permis: int = 2026) -> dict[str, float]:
    m = dict(mbgeo=mbgeo(usage, zone, altitude), mbcombles=mbcombles(usage, s_combles, sref), mbsurf_moy=mbsurf_moy(usage, sref, nb_logements),
             mbsurf_tot=mbsurf_tot(usage, sref_usage, annee_permis), mbbruit=mbbruit(usage, zone, exposition_bruit, categorie_ce))
    m["bbio_max"] = BBIO_MAX_MOYEN[usage] * (1 + sum(m.values()))
    return m


# DH_max par catégorie de contraintes extérieures (chapitre III, IV). « Climatisé en H2d ou H3 » relève la limite.
def dh_max(usage: int, zone: str, categorie_ce: int = 1, climatise: bool = False, smoy_logement: float = 0.0) -> float | None:
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
    if usage == 3:
        if categorie_ce >= 3:
            return None                                        # pas de seuil
        return 2600.0 if categorie_ce == 2 else (2400.0 if chaud else 1150.0)
    return 2200.0 if categorie_ce >= 2 else (1800.0 if chaud else 900.0)
