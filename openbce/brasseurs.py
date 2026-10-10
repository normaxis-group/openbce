# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Brasseurs d'air (annexe III, fiche 8.32) : gestion de la vitesse sur la température opérative et correction de la
température de confort ressentie, Δθop_BA (1647 à 1662). Ne jouent qu'en période de refroidissement propre au groupe
et en occupation. PREMIER JET : gestion manuelle pour tous les modes de gestion (consignes conventionnelles du
tableau 259), usage jour (6 h à 22 h), nuit ou jour et nuit. La consommation électrique (1662 à 1665 : puissance
intermédiaire ou maximale corrigée selon le débit, par brasseur) est rendue par `puissance` ; les RSEE la comptent avec
les auxiliaires de ventilation (O_Cef_aux_ventilateur). Le flux thermique associé (1664, 1666) n'est pas encore rendu
au groupe."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from openbce import usages as mod_usages

from .rsee import Noeud

D_OP_1, D_OP_2, D_OP_3 = 2.0, 4.0, 1.0        # tableau 259, gestion manuelle
RAT_US = {1: (0.6, 0.4), 2: (0.54, 0.36), 3: (0.7, 0.0), 4: (0.85, 0.0), 5: (0.75, 0.0)}   # tableau 258 : (jour, nuit)
SURFACE_MAX_PAR_BRASSEUR = 15.0
VITESSE_MIN = 0.2                              # m/s : en dessous, aucun effet (1660)


@dataclass
class TypeBrasseur:
    nombre: int
    rat_surf: float          # part de la surface du groupe desservie
    usage: int               # 0 nuit, 1 jour, 2 jour et nuit
    q_max_corr: float        # m³/h par brasseur, débit maximal corrigé
    p_max_corr: float = 0.0  # W par brasseur, puissance maximale corrigée (1,2 déclarée, 1,1 justifiée, p. 992)
    debit: float = 0.0       # état : débit courant par brasseur

    @property
    def q_int(self) -> float:
        return 0.6 * self.q_max_corr

    @property
    def p_int(self) -> float:
        return 0.6 * self.p_max_corr


def lire(groupe: Noeud, usage: int, surface: float) -> list[TypeBrasseur]:
    types = []
    for b in groupe.directs("Brasseur_Air"):
        nb = b.entier("Nb", 0)
        if nb <= 0:
            continue
        q_max = b.nombre("Qv_air_max", 0.0) * (0.9 if b.entier("Type_Qv_air_max", 0) >= 1 else 0.8)   # certifié ou justifié / déclaré
        rat = min(SURFACE_MAX_PAR_BRASSEUR * nb / surface if surface > 0 else 0.0, b.nombre("Rat_surf", 0.0))
        p_max = b.nombre("P_elec_max", 0.0) * (1.2 if b.entier("Type_P_elec_max", 0) == 0 else 1.1)   # déclarée / justifiée (certifiée lue comme justifiée, cf. débit)
        types.append(TypeBrasseur(nb, rat, b.entier("Us", 1), q_max, p_max))
    return types


def puissance(types: list[TypeBrasseur]) -> float:
    """Électricité de l'heure de tous les brasseurs du groupe, Wh (1662 à 1665) : nulle à l'arrêt, intermédiaire au débit
    intermédiaire, maximale corrigée au débit maximal ; l'état des débits est celui laissé par `delta_theta_op`."""
    w = 0.0
    for t in types:
        if t.debit <= 0:
            continue
        w += t.nombre * (t.p_max_corr if t.debit >= t.q_max_corr - 1e-9 else t.p_int)
    return w


def actif(usage_brasseur: int, heure_legale: int) -> bool:
    nuit = heure_legale > 22 or heure_legale <= 6
    return usage_brasseur == 2 or (usage_brasseur == 1 and not nuit) or (usage_brasseur == 0 and nuit)


def delta_theta_op(types: list[TypeBrasseur], usage: int, occupe: bool, froid_autorise: bool, heure_legale: int, top_prec: float,
                   consigne_fr: float, d_conf_adapt: float, theta_rm: float, theta_i: float, volume: float) -> float:
    """Δθop_BA du groupe à cette heure : met à jour l'état des brasseurs (1652 à 1655) puis combine les types au
    prorata des surfaces (1657 à 1662)."""
    if not types or not occupe or not froid_autorise:
        for t in types:
            t.debit = 0.0
        return 0.0
    dec = consigne_fr + d_conf_adapt + D_OP_3                                    # (1647)
    v1, v2, arret = dec, dec + D_OP_2, dec - D_OP_1                              # (1649)
    nuit = heure_legale > 22 or heure_legale <= 6
    jour_total = nuit_total = 0.0
    for t in types:
        if not actif(t.usage, heure_legale):
            t.debit = 0.0
            continue
        if top_prec < arret:
            t.debit = 0.0
        elif top_prec < v1:
            pass
        elif top_prec < v2:
            t.debit = max(t.q_int, t.debit)
        else:
            t.debit = t.q_max_corr
        if usage in mod_usages.IHEBERGEMENT and nuit:                           # fiche 8.32, p. 1000
            t.debit = min(t.debit, t.q_int)                                      # acoustique la nuit en habitation
        if t.debit <= 0 or t.rat_surf <= 0 or volume <= 0:
            continue
        taux = t.debit * t.nombre / (volume * t.rat_surf)                        # (1658)
        v = 0.0032 * taux                                                        # (1659)
        if v <= VITESSE_MIN:
            continue
        d = (1.8322 * np.exp(0.0361 * (theta_rm - theta_i))) * np.log(v) + 3.0498 * np.exp(0.0368 * (theta_rm - theta_i))
        d = max(float(d), 0.0)
        if t.usage == 1:
            jour_total += t.rat_surf * d
        elif t.usage == 0:
            nuit_total += t.rat_surf * d
        else:
            jour_total += t.rat_surf * d
            nuit_total += t.rat_surf * d
    rat_jour, rat_nuit = RAT_US.get(usage, (0.7, 0.0))
    if any(t.usage == 2 for t in types):
        rat_jour = rat_nuit = 1.0
    if nuit:
        return nuit_total / rat_nuit if rat_nuit > 0 else 0.0
    return jour_total / rat_jour if rat_jour > 0 else 0.0
