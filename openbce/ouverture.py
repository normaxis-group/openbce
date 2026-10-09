# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Surventilation naturelle par ouverture des baies (annexe III, fiche 5.13), gestion manuelle en mode Th-B.

Les profils des figures 61 et 62 (images du PDF) ont été relevés à la lecture. Points non couverts par le texte et
tranchés ici : l'hystérésis s'applique à toute heure d'occupation, de jour comme de nuit (le banc écarte les deux
autres lectures : fenêtres fermées la nuit, froid surestimé de 7 kWh/m² ; ratio figé la nuit, froid sous-estimé
de 1,8 kWh/m² en zone calme) ;
l'écart de confort adaptatif Δθconf_adapt est nul en mode Th-B.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SEUIL_BAS, SEUIL_HAUT, D_EXT_INT = 10.0, 18.0, -3.0      # °C (241)
D_EXT_INT_AUTO = 2.0                                       # °C : écart extérieur-intérieur en gestion automatique (5.13.3.1.3)
P_DEROG_OUV = 0.5                                          # part des occupants dérogeant à l'ouverture automatique (247)
CW, CST = 0.001, 0.0035                                    # vent, tirage thermique (nomenclature 5.13.2)
CD_GO, D_CP, VENT_MAX = 0.6, 0.75, 3.0
RHO_REF, THETA_REF = 1.2, 19.0
CVENT = 0.9
# taux de passage de l'air à travers une protection mobile baissée, selon sa typologie (tableau 40)
TAUX_PASSAGE = {0: 0.0, 1: 0.10, 2: 0.25, 3: 0.50, 4: 0.75}


def moderation_exterieure(theta_ext: float, theta_op_prec: float, consigne_fr: float, refroidissement_autorise: bool, d_ext_int: float = D_EXT_INT) -> float:
    """Mod_ext_man : pas d'ouverture s'il fait trop froid dehors, ni trop chaud par rapport à l'intérieur (figure 61).
    `d_ext_int` : -3 °C en gestion manuelle (241), +2 °C pour la part automatique (5.13.3.1.3)."""
    haut, limite = SEUIL_HAUT, theta_op_prec - d_ext_int
    if refroidissement_autorise:                           # mode Th-B, 5.13.3.1.2
        haut, limite = min(consigne_fr - 1, haut), min(consigne_fr - 1, limite)
    if theta_ext <= SEUIL_BAS or theta_ext > limite:
        return 0.0
    return 1.0 if theta_ext >= haut else (theta_ext - SEUIL_BAS) / (haut - SEUIL_BAS)


def contrainte(exposition_bruit: int, heure_legale: int, saison_chauffage: bool) -> float:
    """Cpr en occupation (tableau 42). `heure_legale` de 0 à 23."""
    if saison_chauffage:
        return 0.3
    if exposition_bruit <= 1:
        return 1.0
    return 0.7 if 7 <= heure_legale <= 21 else 0.3


def ratio_thermique(theta_op_prec: float, precedent: float, consigne_fr: float, saison_chauffage: bool) -> float:
    """Rouv_θop_man : hystérésis sur la température opérative du pas précédent (figure 62, 242 et 243)."""
    ouv2 = consigne_fr + (1.0 if saison_chauffage else -1.0)
    ouv1, fer1, fer2 = ouv2 - 2, ouv2 - 2, ouv2 - 3
    monte = min(max((theta_op_prec - ouv1) / (ouv2 - ouv1), 0.0), 1.0)
    descend = min(max((theta_op_prec - fer2) / (fer1 - fer2), 0.0), 1.0)
    return max(monte, min(precedent, descend))


@dataclass(frozen=True)
class Ouvrants:
    """Baies ouvrables d'un groupe : surface maximale d'ouverture, azimut, inclinaison, exposition au bruit."""

    baies: tuple[tuple[float, float, float, int], ...]
    traversant: bool
    httf: float
    rang: tuple[int, ...] = ()          # rang de chaque baie ouvrable parmi les baies du groupe
    passage: tuple[float, ...] = ()     # taux de passage de l'air à travers la protection baissée (fiche 5.12)
    automatique: tuple[bool, ...] = ()  # ouverture pilotée par un automatisme (Has_Gestion_Auto_Ouverture)

    def sections(self, ratios: list[float], rprot: list[float]) -> list[float]:
        """Ratios d'ouverture ramenés à la section laissée libre par les protections mobiles (239, 248, 249)."""
        corriges = []
        for k, r in enumerate(ratios):
            fermeture = rprot[self.rang[k]]
            libre = fermeture * self.passage[k] + (1 - fermeture)
            corriges.append(min(r, libre))
        return corriges

    def debit(self, ratios: list[float], vent_meteo: float, theta_ext: float, theta_int_prec: float) -> float:
        """Débit massique d'air entrant par les baies ouvertes, en kg/s (250 à 255)."""
        aires = [r * b[0] for r, b in zip(ratios, self.baies)]
        total = sum(aires)
        if total <= 0:
            return 0.0
        vent = CVENT * vent_meteo
        tirage = total / 2 * (CST * self.httf * abs(theta_ext - theta_int_prec)) ** 0.5
        if not self.traversant:
            q = total / 2 * max(CW * vent * vent, CST * self.httf * abs(theta_ext - theta_int_prec)) ** 0.5   # (251)
        else:
            sors = []
            for k in range(2):                              # deux roses des vents décalées de 45° (253)
                par_orientation = [0.0] * 4
                for a, (_, alpha, beta, _) in zip(aires, self.baies):
                    if beta >= 60:
                        par_orientation[int(((alpha - k * 45 + 45) % 360) // 90)] += a
                s = sum(1 / (1 / (x * x) + 1 / ((total - x) ** 2)) ** 0.5 for x in par_orientation if 0 < x < total)
                sors.append(s / 4)
            q = max(CD_GO * min(sors) * min(vent, VENT_MAX) * D_CP ** 0.5, tirage)                             # (254)
        return q * RHO_REF * (273 + THETA_REF) / (273 + theta_ext)                                             # (255)


def du_groupe(groupe, usage: int) -> Ouvrants:
    ouvrables = [(k, b) for k, b in enumerate(groupe.directs("Baie")) if b.entier("Baie_ouvrable", 0) == 1 and b.entier("Id_Et", 0) == 0]
    baies = tuple((b.nombre("Ab") * b.nombre("Rouv_Max", 0.0), b.nombre("Alpha"), b.nombre("Beta"), b.entier("Exp_BR", 1)) for _, b in ouvrables)
    passage = tuple(1.0 if b.entier("Choix_PM_GPM", 0) == 0 else TAUX_PASSAGE.get(b.entier("Typo_Permea_PM", 0), 0.0) for _, b in ouvrables)
    traversant = usage == 1 or groupe.entier("Delta_trav_surv", 0) == 1      # tableau 43
    return Ouvrants(baies, traversant, groupe.nombre("Httf", 1.5) or 1.5, tuple(k for k, _ in ouvrables), passage,
                    tuple(b.entier("Has_Gestion_Auto_Ouverture", 0) == 1 for _, b in ouvrables))
