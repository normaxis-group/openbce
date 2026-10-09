# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Gestion des protections mobiles (annexe III, fiche 5.9) : taux de fermeture Rprot d'un volet, heure par heure.

État : volets (Choix_PM_GPM 1 à 3) et stores enroulables (4 à 6), familles « habitation » et « bureau », en gestion manuelle et en
gestion automatique avec dérogation. Les valeurs conventionnelles viennent des figures 34 à 36, 38, 39, 44 et 45 de
l'annexe III (pages 186 à 191), qui sont des IMAGES dans le PDF : elles ont été relevées à la lecture, À RELIRE par un
thermicien. Les seuils de la gestion automatique (Eclim_auto, Toph-1limb, Toph-1limh) ne sont donnés nulle part
dans le texte : les valeurs ci-dessous sont PROVISOIRES. Restent à écrire : l'horloge personnalisable, les stores
vénitiens, la seconde protection mobile.
"""
from __future__ import annotations

HIVER, MI_SAISON, ETE = 1, 2, 3
TOP_LIM_MANU = 26.5          # °C, limite sur la température opérative maximale de la veille (nomenclature 5.9.2)
P_OCC = {1: 0.5, 2: 0.7, 3: 0.5}     # part des baies en locaux occupés, par usage (figure 34) ; 3 = bureaux
P_DEROG = {1: 0.25, 2: 0.25, 3: 0.25}
FAMILLE = {1: "habitation", 2: "habitation", 3: "bureau"}

# Figure 35, volets. Par type de gestion (3 = manuelle non motorisée, 4 = manuelle motorisée, 2 et 1 = dérogation
# manuelle sans et avec détecteur de présence), quatre situations : hiver, mi-saison, été frais, été chaud
# (Topj-1max >= 26,5 °C). En occupation : (Rprot à éclairement nul, éclairement de fermeture complète en lux, Rprot de nuit).
OCCUPATION = {
    2: ((0.10, 100000, 0.80), (0.10, 100000, 0.80), (0.20, 60000, 0.80), (0.30, 40000, 0.80)),
    1: ((0.10, 100000, 0.90), (0.10, 100000, 0.90), (0.20, 50000, 0.90), (0.30, 30000, 0.90)),
    3: ((0.15, 100000, 0.80), (0.15, 100000, 0.80), (0.20, 80000, 0.80), (0.25, 60000, 0.80)),
    4: ((0.10, 100000, 0.90), (0.10, 100000, 0.90), (0.20, 60000, 0.90), (0.30, 40000, 0.90)),
}
# En inoccupation : (Rprot de jour, Rprot de nuit).
INOCCUPATION = {
    3: ((0.20, 0.70), (0.20, 0.70), (0.20, 0.70), (0.40, 0.70)),
    4: ((0.10, 0.80), (0.10, 0.80), (0.20, 0.80), (0.50, 0.80)),
}


# Figure 38, stores enroulables : mêmes lectures que la figure 35.
OCCUPATION_STORE = {
    2: ((0.10, 100000, 0.10), (0.10, 60000, 0.10), (0.20, 50000, 0.10), (0.30, 30000, 0.10)),
    1: ((0.10, 60000, 0.10), (0.10, 60000, 0.10), (0.20, 40000, 0.10), (0.30, 30000, 0.10)),
    3: ((0.10, 100000, 0.10), (0.10, 80000, 0.10), (0.15, 60000, 0.10), (0.20, 40000, 0.10)),
    4: ((0.10, 100000, 0.10), (0.10, 60000, 0.10), (0.20, 50000, 0.10), (0.30, 30000, 0.10)),
}
INOCCUPATION_STORE = {
    3: ((0.10, 0.20), (0.20, 0.20), (0.30, 0.20), (0.40, 0.20)),
    4: ((0.10, 0.10), (0.20, 0.10), (0.30, 0.10), (0.60, 0.10)),
}
# Figure 39, stores enroulables, famille « bureau ».
OCCUPATION_STORE_BUREAU = {
    2: ((0.10, 60000, 0.15), (0.10, 80000, 0.15), (0.25, 30000, 0.20), (0.30, 30000, 0.20)),
    1: ((0.10, 60000, 0.10), (0.10, 80000, 0.10), (0.25, 20000, 0.15), (0.30, 20000, 0.15)),
    3: ((0.15, 60000, 0.10), (0.15, 80000, 0.10), (0.20, 40000, 0.10), (0.25, 40000, 0.10)),
    4: ((0.10, 60000, 0.10), (0.10, 80000, 0.10), (0.25, 30000, 0.10), (0.30, 30000, 0.10)),
}
INOCCUPATION_STORE_BUREAU = {
    3: ((0.15, 0.15), (0.15, 0.15), (0.25, 0.20), (0.30, 0.20)),
    4: ((0.10, 0.10), (0.10, 0.10), (0.30, 0.15), (0.40, 0.15)),
}


# Figure 36, volets, famille « bureau ».
OCCUPATION_BUREAU = {
    2: ((0.05, 80000, 0.90), (0.05, 100000, 0.90), (0.15, 80000, 0.90), (0.20, 60000, 0.90)),
    1: ((0.05, 80000, 0.90), (0.05, 100000, 0.90), (0.15, 70000, 0.90), (0.20, 50000, 0.90)),
    3: ((0.10, 80000, 0.30), (0.10, 100000, 0.30), (0.10, 80000, 0.30), (0.15, 60000, 0.30)),
    4: ((0.05, 80000, 0.70), (0.05, 100000, 0.70), (0.15, 80000, 0.70), (0.20, 60000, 0.70)),
}
INOCCUPATION_BUREAU = {
    3: ((0.10, 0.30), (0.10, 0.30), (0.20, 0.30), (0.30, 0.30)),
    4: ((0.10, 0.70), (0.10, 0.70), (0.30, 0.70), (0.40, 0.70)),
}


def _matrices(usage: int, store: bool):
    """Matrices conventionnelles de gestion manuelle (occupation, inoccupation) selon la famille d'usage et le type."""
    if FAMILLE[usage] == "habitation":
        return (OCCUPATION_STORE, INOCCUPATION_STORE) if store else (OCCUPATION, INOCCUPATION)
    return (OCCUPATION_STORE_BUREAU, INOCCUPATION_STORE_BUREAU) if store else (OCCUPATION_BUREAU, INOCCUPATION_BUREAU)


VENT_LIMITE_STORE = 10.0     # m/s : au-delà, un store extérieur est remonté (nomenclature 5.9.2, équations 190 et 191)
CVENT = 0.9                  # correction locale de la vitesse du vent (fiche 3.2)


def decoder(choix_pm_gpm: int) -> tuple[bool, int]:
    """Champ Choix_PM_GPM d'une baie -> (store enroulable ?, type de gestion 1 automatique, 2 manuelle, 3 motorisée)."""
    if not 1 <= choix_pm_gpm <= 6:
        raise NotImplementedError(f"protection mobile de type {choix_pm_gpm} non traitée")
    return choix_pm_gpm >= 4, (choix_pm_gpm - 1) % 3 + 1


def store_remonte(store: bool, exterieur: bool, vent_meteo: float) -> bool:
    return store and exterieur and CVENT * vent_meteo >= VENT_LIMITE_STORE


def type_gpm_manu(choix_pm_gpm: int, detecteur: bool = False) -> int:
    """Type de gestion (180) à partir du champ Choix_PM_GPM d'une baie à volet (1 automatique, 2 et 3 manuelles)."""
    return {1: 1 if detecteur else 2, 2: 3, 3: 4}[choix_pm_gpm]


def _situation(saison: int, top_max_veille: float) -> int:
    if saison == HIVER:
        return 0
    if saison == MI_SAISON:
        return 1
    return 3 if top_max_veille >= TOP_LIM_MANU else 2


# Tableau 34 (5.9.3.6) : en mode Th-D, en période de confort adaptatif et quand la température opérative maximale de la
# veille dépasse TOP_LIM_MANU, les Rprot0 de la gestion manuelle sont forcés : de jour sous le seuil d'éclairement,
# au moins 80 % (gestion motorisée) ou 70 % (autres) ; de nuit, au plus 70 % en résidentiel et 50 % ailleurs (volets),
# 50 % partout pour les stores enroulables. Les seuils d'éclairement sont conservés.
THD_JOUR = {4: 0.8}
THD_JOUR_DEFAUT = 0.7
THD_NUIT_VOLET = {"habitation": 0.7, "bureau": 0.5}
THD_NUIT_STORE = 0.5


def volet_manuel_thd(gpm_manu: int, usage: int, occupe: bool, eclairement: float, iocc_gpm: int = 1, store: bool = False) -> float:
    """Gestion manuelle en Th-D, confort adaptatif et veille chaude (203, 204) : matrices d'été forcées par le tableau 34."""
    occupation, inoccupation = _matrices(usage, store)
    plancher = THD_JOUR.get(gpm_manu, THD_JOUR_DEFAUT)
    r0, ecl_man, nuit = occupation[gpm_manu][3]
    r0 = max(plancher, r0)
    nuit = min(THD_NUIT_STORE if store else THD_NUIT_VOLET[FAMILLE[usage]], nuit)
    jour = eclairement > 0 if iocc_gpm == 1 else iocc_gpm == 0
    r_inocc = inoccupation[gpm_manu][3][0 if jour else 1]
    r_inocc = max(plancher, r_inocc) if jour else min(THD_NUIT_STORE if store else THD_NUIT_VOLET[FAMILLE[usage]], r_inocc)
    if not occupe:
        return r_inocc
    r_occ = (1.0 if eclairement >= ecl_man else r0 + (1 - r0) * eclairement / ecl_man) if jour else nuit
    part = P_OCC[usage]
    return part * r_occ + (1 - part) * r_inocc


def volet_manuel(gpm_manu: int, usage: int, occupe: bool, eclairement: float, saison: int, top_max_veille: float, iocc_gpm: int = 1, store: bool = False) -> float:
    """Taux de fermeture moyen de la baie en gestion manuelle (177, 178, 183, 188, 189, 209).

    `eclairement` : éclairement total incident sur la baie, en lux. `iocc_gpm` : 1 occupation, 0 inoccupation de
    jour, -1 inoccupation de nuit ou de vacances.
    """
    k = _situation(saison, top_max_veille)
    jour = eclairement > 0 if iocc_gpm == 1 else iocc_gpm == 0          # (183)
    occupation, inoccupation = _matrices(usage, store)
    r_inocc = inoccupation[gpm_manu][k][0 if jour else 1]
    if not occupe:
        return r_inocc                                                 # (189) : partGPM = 0
    r0, ecl_man, nuit = occupation[gpm_manu][k]
    r_occ = (1.0 if eclairement >= ecl_man else r0 + (1 - r0) * eclairement / ecl_man) if jour else nuit   # (177)
    part = P_OCC[usage]                                                # (178)
    return part * r_occ + (1 - part) * r_inocc                         # (209)


# --- gestion automatique (figure 44, résidentiel, volets et stores enroulables) -------------------------------------
# Par occupation puis par situation (hiver, mi-saison, été), trois couples (Rprot si θop > limite haute, Rprot si
# θop < limite basse) : de jour sous le seuil d'éclairement, de jour au-dessus, de nuit.
AUTO = {
    True: (((0.0, 0.0), (0.0, 0.0), (1.0, 1.0)), ((0.0, 0.0), (0.5, 0.0), (1.0, 1.0)), ((0.5, 0.0), (1.0, 0.75), (0.5, 0.9))),
    False: (((0.0, 0.0), (0.0, 0.0), (1.0, 1.0)), ((0.0, 0.0), (0.5, 0.0), (1.0, 1.0)), ((1.0, 0.75), (1.0, 0.75), (0.5, 0.5))),
}
# Figure 45, tertiaire : ne diffère de la figure 44 que par la nuit d'été (protections relevées).
AUTO_TERTIAIRE = {
    True: (((0.0, 0.0), (0.0, 0.0), (1.0, 1.0)), ((0.0, 0.0), (0.5, 0.0), (1.0, 1.0)), ((0.5, 0.0), (1.0, 0.75), (0.0, 0.0))),
    False: (((0.0, 0.0), (0.0, 0.0), (1.0, 1.0)), ((0.0, 0.0), (0.5, 0.0), (1.0, 1.0)), ((1.0, 0.75), (1.0, 0.75), (0.0, 0.0))),
}
# Seuils absents du texte. Un balayage sur dix projets à volets automatiques (banc/seuils_auto.py) ne les identifie
# pas un par un : plusieurs couples donnent le même froid (3 000 ou 10 000 lux avec 24/26 °C, 30 000 lux avec
# 23/25 °C, 10 000 lux avec 25/27 °C). On retient 10 000 lux et 25/27 °C, encadrant la consigne de 26 °C.
# PROVISOIRE : à resserrer par le banc sur davantage de projets.
ECLIM_AUTO = 10000.0
TOP_LIM_BAS, TOP_LIM_HAUT = 24.0, 26.0   # °C ; le texte ne donne pas ces limites (fiche 5.9 : « - » en valeur conventionnelle) et les RSEE
# ne les portent pas. Grille du banc (banc/seuils_auto, 10 projets à volets automatiques, 10/10/2026) : 24/26 donne Bbio -0,4 %
# (écart médian 1,2 %), 25/27 +1,4 % (2,0 %), 24/27 +0,9 %, 26/28 +1,8 %.


def volet_auto(detecteur: bool, usage: int, occupe: bool, eclairement: float, saison: int, top_max_veille: float, top_prec: float,
               chaud_precedent: bool, type_horloge: int = 0, store: bool = False) -> tuple[float, bool]:
    """Taux de fermeture moyen de la baie en gestion automatique avec dérogation (179, 182, 186, 187) et état de
    l'hystérésis sur la température opérative (vrai : au-dessus de la limite haute)."""
    chaud = True if top_prec > TOP_LIM_HAUT else (False if top_prec < TOP_LIM_BAS else chaud_precedent)   # figure 31
    jour = True if type_horloge == 0 else eclairement > 0                                             # (182)
    colonne = 2 if not jour else (1 if eclairement >= ECLIM_AUTO else 0)
    situation = {HIVER: 0, MI_SAISON: 1, ETE: 2}[saison]
    r_auto = (AUTO if FAMILLE[usage] == "habitation" else AUTO_TERTIAIRE)[occupe][situation][colonne][0 if chaud else 1]
    if not occupe:
        return r_auto, chaud
    gpm_manu = type_gpm_manu(1, detecteur)
    r0, ecl_man, nuit = _matrices(usage, store)[0][gpm_manu][_situation(saison, top_max_veille)]
    r_derog = (1.0 if eclairement >= ecl_man else r0 + (1 - r0) * eclairement / ecl_man) if eclairement > 0 else nuit
    part = P_OCC[usage] * P_DEROG[usage]                                                              # (179)
    return part * r_derog + (1 - part) * r_auto, chaud
