# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Éclairage (annexe III, fiche 7.1) : éclairement naturel intérieur et consommation d'éclairage du groupe.

État : logement en mode Th-B, où le calcul est entièrement conventionnel (7.1.3, « cas de l'habitation ») : 1 W/m²,
interrupteur manuel (C1 = 0,9), tout le groupe ayant accès à la lumière naturelle.
"""
from __future__ import annotations

import functools

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


# --- tertiaire, mode Th-B (781, 782) et Th-C : tableau 78 de l'annexe III 2026 (p. 488 à 491) ----------------------
# Par usage et type de local conventionnel : C1 pour Gest_ecl = 1 (interrupteur), 2 (interrupteur et horloge), 3 (marche
# et arrêt automatiques), 4 (marche manuelle et arrêt automatique), et éclairement intérieur de référence Eiref en lux.
# Th-B : C1 = colonne Gest_ecl = 2, Pecl_tot = 2 x Eiref / 100 (782). Les noms sont ceux du tableur officiel des
# scénarios ; le code Locaux_Bureau du récapitulatif est lu comme le rang du local dans la feuille du tableur de l'usage
# (_locaux_usage). Hors bureaux, ce rang est un choix non validé : l'ordre du tableau 78 diffère de celui du tableur
# pour vingt usages et aucun récapitulatif ne le montre.
# Bureaux : valeurs relevées sur l'image du tableau de 2022 et validées au banc (salle de réunion 500 lux ; le texte 2026
# imprime « 50 » ; circulation 0,75 en Gest_ecl = 1 et 0,5 en 3). Usage 7, local service : absent du tableau 78, valeur
# des autres lignes « Local service » (déduction).
TABLEAU_78 = {
    3: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.70, 0.65, 0.60, 0.50), 500),
        "Circulation Accueil": ((0.75, 0.75, 0.50, 0.60), 100), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    4: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
        "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300), "Salle de repos": ((0.60, 0.75, 0.70, 0.60), 300),
        "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    5: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300),
        "Salle d'enseignement informatique": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de conférence Salle polyvalente": ((0.80, 0.75, 0.70, 0.60), 300),
        "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Salle des professeurs": ((0.80, 0.75, 0.70, 0.60), 300), "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100),
        "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    6: {"Salle multi-fonctions": ((0.80, 0.75, 0.70, 0.60), 300), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
        "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300), "Circulation accueil": ((0.80, 0.75, 0.70, 0.60), 100),
        "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    7: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de conférence Amphithéâtre": ((0.80, 0.75, 0.70, 0.60), 300),
        "Salle d'enseignement informatique": ((0.95, 0.90, 0.85, 0.75), 300), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300),
        "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    8: {"Chambre sans cuisine avec salle de bain": ((0.60, 0.55, 0.50, 0.40), 70), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100)},
    9: {"Chambre sans cuisine avec salle de bain": ((0.60, 0.55, 0.50, 0.40), 70), "Sanitaires collectifs": ((1.00, 0.95, 0.90, 0.80), 150),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100)},
    10: {"Bureau standard": ((0.80, 0.75, 0.70, 0.60), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Salle petits déjeuners": ((1.00, 1.00, 1.00, 1.00), 200)},
    11: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Bar": ((1.00, 1.00, 1.00, 1.00), 200),
         "Salle petits déjeuners": ((1.00, 1.00, 1.00, 1.00), 200), "salle de séminaires réunion": ((0.80, 0.75, 0.70, 0.60), 500)},
    12: {"Salle de jeux": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de repos": ((0.80, 0.75, 0.70, 0.60), 300),
         "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 500),
         "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    13: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    14: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    15: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    16: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    17: {"Aire de vente (inférieure à 300m²)": ((1.00, 1.00, 1.00, 1.00), 300), "Aire de vente (supérieure à 300m²)": ((1.00, 1.00, 1.00, 1.00), 300),
         "Circulation Accueil": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    18: {"Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200)},
    19: {"Chambre sans cuisine avec salle de bain": ((1.00, 1.00, 1.00, 1.00), 70), "Circulation Accueil": ((1.00, 1.00, 1.00, 1.00), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Salle commune": ((0.80, 0.75, 0.70, 0.60), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500)},
    20: {"Chambre sans cuisine avec salle de bain": ((1.00, 1.00, 1.00, 1.00), 70), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200), "Circulation Accueil": ((1.00, 1.00, 1.00, 1.00), 200),
         "Locaux soins et offices": ((1.00, 1.00, 1.00, 1.00), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Salle d'attente et de consulation (urgences)": ((1.00, 1.00, 1.00, 1.00), 500), "Aire de production": ((1.00, 0.95, 0.90, 0.80), 500)},
    21: {"Aire de production": ((1.00, 0.95, 0.90, 0.80), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation Accueil": ((1.00, 1.00, 1.00, 1.00), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Salle d'attente et de consultation": ((1.00, 1.00, 1.00, 1.00), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Salle de réunion": ((0.70, 0.65, 0.60, 0.50), 500)},
    22: {"Espace voyageurs": ((1.00, 1.00, 1.00, 1.00), 200), "Circulation Accueil": ((1.00, 0.75, 0.70, 0.60), 150),
         "Commerces": ((1.00, 1.00, 1.00, 1.00), 300), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Inspection filtrage": ((1.00, 1.00, 1.00, 1.00), 500), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    23: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Aire de production": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    24: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Aire de production": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    25: {"Salle de sport": ((0.90, 0.85, 0.80, 0.70), 300), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    26: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    27: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    28: {"Salle de sport": ((0.90, 0.85, 0.80, 0.70), 300), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
}
_C2_MANUEL = ((0.0, 100.0, 700.0, 2800.0), (1.0, 1.0, 0.3, 0.0))                                # Grad_ecl = 1 (tableau 79)


def _normaliser(nom: str) -> str:
    return " ".join(nom.casefold().replace("m²", "m2").replace("( ", "(").replace(" )", ")").split())


@functools.lru_cache(maxsize=None)
def _locaux_usage(usage: int) -> tuple:
    """Types de locaux de l'usage, dans l'ordre du tableur officiel (rang = code Locaux_Bureau) : (nom, C1 par Gest_ecl, Eiref)."""
    from openbce import scenarios
    table = TABLEAU_78.get(usage)
    if table is None:
        raise NotImplementedError(f"éclairage conventionnel : pas de locaux au tableau 78 pour l'usage {usage}")
    cle = {_normaliser(k): v for k, v in table.items()}
    locaux = []
    for l in scenarios._locaux(usage):
        v = cle.get(_normaliser(l["nom"]))
        if v is None:
            raise NotImplementedError(f"éclairage conventionnel : local « {l['nom']} » de l'usage {usage} absent du tableau 78")
        locaux.append((l["nom"], v[0], float(v[1])))
    return tuple(locaux)


def _type_local(usage: int, code: int) -> tuple:
    types = _locaux_usage(usage)
    if not 0 <= code < len(types):
        raise ValueError(f"Locaux_Bureau = {code} hors des {len(types)} locaux conventionnels de l'usage {usage}")
    return types[code]


# Déduction du banc, contraire à la lettre du texte. La fiche 7.1 donne C2 = 1 à un local sans aucun accès à la lumière
# naturelle (Ratio_ecl_nat = 0) : il consommerait à pleine puissance pendant toute l'occupation. Les RSEE disent autre
# chose pour les circulations et les sanitaires : leur consommation est absente du Bbio. Sur deux projets de bureaux
# (35 % de la surface en circulations et sanitaires aveugles sur l'un), le calcul selon le texte excède le RSEE d'un
# montant égal chaque mois, et le calcul sans ces locaux le retrouve (docs/lectures.md). Un troisième reste inexpliqué
# dans les deux sens ; son seul bureau aveugle est donc laissé à C2 = 1, comme le veut le texte. La règle est étendue
# telle quelle aux circulations et sanitaires des usages 4 à 28, sans preuve.
def _non_compte(nom: str) -> bool:
    n = _normaliser(nom)
    return n.startswith("circulation") or n.startswith("sanitaires")


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


def locaux_tertiaires_saisis(groupe, usage: int = 3) -> list[tuple]:
    """Locaux du groupe avec leurs caractéristiques saisies (mode Th-C) : (part de surface, part ayant accès à la
    lumière naturelle, C1, éclairement de référence, Pecl_tot, Pecl_aux, points de C2, fractionné ?)."""
    locaux = []
    for e in groupe.directs("Eclairage"):
        genre, nat = e.entier("Locaux_Bureau", 0), e.nombre("Ratio_ecl_nat", 0.0)
        gest, grad = e.entier("Gest_Ecl", 1), e.entier("Grad_Ecl", 1)
        nom, c1s, eiref = _type_local(usage, genre)
        c1 = 1.0 if gest == 0 else (c1s[gest - 1] if 1 <= gest <= 4 else 0.9)
        if nat <= 0 and _non_compte(nom):
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


def locaux_tertiaires(groupe, usage: int = 3) -> list[tuple[float, float, float, float]]:
    """(part de surface, part ayant accès à la lumière naturelle, C1, éclairement de référence) par local du groupe."""
    locaux = []
    for e in groupe.directs("Eclairage"):
        genre, nat = e.entier("Locaux_Bureau", 0), e.nombre("Ratio_ecl_nat", 0.0)
        nom, c1s, eiref = _type_local(usage, genre)
        c1 = c1s[1]                                                       # Gest_ecl = 2 (782)
        if nat <= 0 and _non_compte(nom):
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
