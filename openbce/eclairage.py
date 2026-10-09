# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Éclairage (annexe III, fiche 7.1) : éclairement naturel intérieur et consommation d'éclairage du groupe.

État : logement en mode Th-B, où le calcul est entièrement conventionnel (7.1.3, « cas de l'habitation ») : 1 W/m²,
interrupteur manuel (C1 = 0,9), tout le groupe ayant accès à la lumière naturelle.
"""
from __future__ import annotations

import numpy as np

# locaux de volume normal éclairés par des baies de type 2 (nomenclature 7.1.2)
RO_PLAFOND, RO_MURS, RO_SOL, R_MURS_SOL = 0.7, 0.5, 0.2, 2.5
FF_BAIE, FF_PLAFOND = 0.4, 0.8
RGR = 4.5
_RO_MOYEN = (RO_SOL + R_MURS_SOL * RO_MURS + RO_PLAFOND) / (2 + R_MURS_SOL)
_INTER = _RO_MOYEN / (1 - _RO_MOYEN) / RGR
K1, K2, K3 = RO_SOL * _INTER, FF_BAIE + _INTER, RO_PLAFOND * FF_PLAFOND + RO_PLAFOND * _INTER

P_ECL_LOGEMENT = 1.0      # W/m² (781)
C1_LOGEMENT = 0.9
# points de référence de C2 en résidentiel (page 482) : éclairement naturel intérieur en lux, C2
_C2_LOGEMENT = ((0.0, 100.0, 200.0, 2800.0), (1.0, 1.0, 0.05, 0.0))
PART_CONVECTIVE = 0.5     # Crec_ecl_conv ; le reste est radiatif, rien n'est perdu


def eclairement_interieur(flt1, flt2, flt3, surface: float):
    """Éclairement naturel du plan utile, en lux (785 et expression de Einat(2))."""
    return (K1 * flt1 + K2 * flt2 + K3 * flt3) / surface


def c2_logement(einat):
    return np.interp(einat, *_C2_LOGEMENT)


def consommation_logement(einat, autorise, surface: float):
    """Consommation d'éclairage du groupe, en Wh par heure (790)."""
    return P_ECL_LOGEMENT * C1_LOGEMENT * c2_logement(einat) * surface * (np.asarray(autorise) > 0)


# --- tertiaire, mode Th-B (781, 782, tableau 79, tableau 80) ----------------------------------------------------------
# Par type de local de bureaux (champ Locaux_Bureau de l'entrée « Eclairage ») : coefficient C1 pour un interrupteur
# manuel avec programmation horaire (Gest_ecl = 2), éclairement intérieur de référence en lux. Le tableau 79 est une
# image du PDF, relevée à la lecture. Correspondance des codes déduite des noms de locaux des RSEE.
LOCAUX_BUREAU = {0: (0.85, 500.0), 1: (0.65, 500.0), 2: (0.75, 100.0), 3: (0.65, 200.0)}   # bureau, réunion, circulation, sanitaires
_C2_MANUEL = ((0.0, 100.0, 700.0, 2800.0), (1.0, 1.0, 0.3, 0.0))                                # Grad_ecl = 1 (tableau 80)


# Déduction du banc, contraire à la lettre du texte. La fiche 7.1 donne C2 = 1 à un local sans aucun accès à la lumière
# naturelle (Ratio_ecl_nat = 0) : il consommerait à pleine puissance pendant toute l'occupation. Les RSEE disent autre
# chose pour les circulations et les sanitaires : leur consommation est absente du Bbio. Sur cas 11 (35 % de la surface
# en circulations et sanitaires aveugles), le calcul selon le texte donne 8,14 kWh/m² pour 6,6 au RSEE, avec un excès
# égal chaque mois (0,12 kWh/m²) ; sans ces locaux, 6,68. Sur cas 23 : 17,27 selon le texte, 16,61 sans eux, 16,5 au
# RSEE. cas 01 reste inexpliqué dans les deux sens (7,59 selon le texte, 6,90 sans eux, 7,2 au RSEE) ; son seul bureau
# aveugle est donc laissé à C2 = 1, comme le veut le texte.
TYPES_SANS_ACCES_NON_COMPTES = (2, 3)      # circulation, sanitaires


# --- tertiaire, mode Th-C : caractéristiques saisies (tableau 79 complet, tableau 80) ---------------------------------
# C1 par type de local de bureaux et mode de commande Gest_ecl (1 interrupteur, 2 interrupteur et horloge, 3 marche et
# arrêt automatiques, 4 marche manuelle et arrêt automatique) ; Gest_ecl = 0 : C1 = 1.
C1_BUREAU = {0: {1: 0.9, 2: 0.85, 3: 0.8, 4: 0.7}, 1: {1: 0.7, 2: 0.65, 3: 0.6, 4: 0.5},
             2: {1: 0.75, 2: 0.75, 3: 0.5, 4: 0.6}, 3: {1: 0.7, 2: 0.65, 3: 0.6, 4: 0.5}}
PART_RESID_GRAD = 0.15


def c2_points(grad: int, eiref: float):
    """Points de référence de C2 selon le mode de gestion de la lumière naturelle (tableau 80)."""
    if grad == 1:
        return (0.0, 100.0, 700.0, 2800.0), (1.0, 1.0, 0.3, 0.0)
    if grad == 2:
        return (0.0, 100.0, eiref, 2 * eiref, 2 * eiref + 1e-6), (1.0, 1.0, PART_RESID_GRAD, PART_RESID_GRAD, 0.0)
    if grad == 3:
        return (0.0, eiref, eiref + 1e-6), (1.0, 1.0, 0.0)
    if grad == 4:
        if eiref < 700:
            return (0.0, 100.0, eiref, eiref + 1e-6), (1.0, 1.0, (6.7 - 7 * eiref / 1000) / 6, 0.0)
        return (0.0, 100.0, 700.0, eiref, eiref + 1e-6), (1.0, 1.0, 0.3, 0.4 - eiref / 7000, 0.0)
    return (0.0, 1.0), (1.0, 1.0)                                      # Grad_ecl = 0 : C2 = 1


def locaux_tertiaires_saisis(groupe) -> list[tuple]:
    """Locaux du groupe avec leurs caractéristiques saisies (mode Th-C) : (part de surface, part ayant accès à la
    lumière naturelle, C1, éclairement de référence, Pecl_tot, Pecl_aux, points de C2, fractionné ?)."""
    locaux = []
    for e in groupe.directs("Eclairage"):
        genre, nat = e.entier("Locaux_Bureau", 0), e.nombre("Ratio_ecl_nat", 0.0)
        gest, grad = e.entier("Gest_Ecl", 1), e.entier("Grad_Ecl", 1)
        eiref = LOCAUX_BUREAU[genre][1]
        c1 = 1.0 if gest == 0 else C1_BUREAU[genre].get(gest, 0.9)
        if nat <= 0 and genre in TYPES_SANS_ACCES_NON_COMPTES:
            c1 = 0.0                      # même déduction du banc qu'en Th-B (bureaux cas 11 en Th-C : 8,55 pour 7,0 avec eux)
        pecl = e.nombre("Pecl_tot", 0.0) or 2.0 * eiref / 100.0
        locaux.append((e.nombre("Rat_local", 0.0), nat, c1, eiref, pecl, e.nombre("Pecl_aux", 0.0), c2_points(grad, eiref), e.entier("Fr_Grad_Ecl", 1) != 1))
    return locaux


def consommation_tertiaire_saisie(flt1: float, flt2: float, flt3: float, autorise: float, surface: float, locaux) -> tuple[float, float]:
    """Consommation d'éclairage du groupe en Wh par heure avec les caractéristiques saisies (787, 788) et
    éclairement naturel des parties éclairées. Fractionnement : C2 de la partie éclairée sur Einat, de l'autre sur
    l'éclairement réduit (7.1.3, locaux de volume normal)."""
    aire_eclairee = surface * sum(l[0] * l[1] for l in locaux)
    einat = (K1 * flt1 + K2 * flt2 + K3 * flt3) / aire_eclairee if aire_eclairee > 0 else 0.0
    total = 0.0
    for rat, nat, c1, eiref, pecl, paux, pts, fractionne in locaux:
        a_local = surface * rat
        if not autorise > 0:
            total += paux * a_local
            continue
        reduit = einat * (2.5 * nat - 1.5) if nat > 0.7 else (einat * (0.5 * nat - 0.1) if nat > 0.2 else 0.0)
        if nat <= 0:
            ctrl = 1.0
        elif fractionne:
            ctrl = nat * float(np.interp(einat, *pts)) + (1 - nat) * float(np.interp(reduit, *pts))
        else:
            ctrl = float(np.interp(reduit, *pts))
        total += max(pecl * c1 * ctrl, paux) * a_local                                     # (788)
    return total, einat


def locaux_tertiaires(groupe) -> list[tuple[float, float, float, float]]:
    """(part de surface, part ayant accès à la lumière naturelle, C1, éclairement de référence) par local du groupe."""
    locaux = []
    for e in groupe.directs("Eclairage"):
        genre, nat = e.entier("Locaux_Bureau", 0), e.nombre("Ratio_ecl_nat", 0.0)
        c1, eiref = LOCAUX_BUREAU[genre]
        if nat <= 0 and genre in TYPES_SANS_ACCES_NON_COMPTES:
            c1 = 0.0
        locaux.append((e.nombre("Rat_local", 0.0), nat, c1, eiref))
    return locaux


def consommation_tertiaire(flt1: float, flt2: float, flt3: float, autorise: float, surface: float, locaux) -> tuple[float, float]:
    """Consommation d'éclairage du groupe en Wh par heure et éclairement naturel des parties éclairées, en lux.
    Système conventionnel du Bbio : 2 W/m² par tranche de 100 lux de référence, gestion non fractionnée (782)."""
    aire_eclairee = surface * sum(rat * nat for rat, nat, _, _ in locaux)
    einat = (K1 * flt1 + K2 * flt2 + K3 * flt3) / aire_eclairee if aire_eclairee > 0 else 0.0
    if not autorise > 0:
        return 0.0, einat
    total = 0.0
    for rat, nat, c1, eiref in locaux:
        if nat <= 0:
            c2 = 1.0
        else:
            effectif = einat * (2.5 * nat - 1.5) if nat > 0.7 else (einat * (0.5 * nat - 0.1) if nat > 0.2 else 0.0)
            c2 = float(np.interp(effectif, *_C2_MANUEL))
        total += 2.0 * eiref / 100.0 * c1 * c2 * surface * rat
    return total, einat
