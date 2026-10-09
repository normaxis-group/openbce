# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Rayonnement solaire et éclairement naturel sur une paroi (annexe III, fiche 3.2 C_EEX_environnement_proche).

Angles d'entrée en degrés comme dans le format réglementaire : Alpha = azimut de la paroi par rapport au sud
(0 sud, 90 ouest, 180 nord, 270 est), Beta = inclinaison (0 horizontale vers le haut, 90 verticale, 180 vers le bas).

Masques traités : masque lointain par tranches azimutales, masques proches verticaux et horizontal (19 à 21).
Restent à écrire : le plan vertical lointain (22) et les arbres à feuilles caduques.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .climat import Climat

ALBEDO = 0.2          # albédo conventionnel du sol, rayonnement et éclairement
HRE = 5.5             # coefficient d'échange radiatif extérieur, W/(m².K)
CVENT = 0.9           # correction locale de la vitesse du vent


@dataclass
class Incident:
    """Flux incidents sur la paroi, par heure : direct, diffus, réfléchi par le sol (W/m² ou lux)."""

    direct: np.ndarray
    diffus: np.ndarray
    reflechi: np.ndarray

    @property
    def total(self) -> np.ndarray:
        return self.direct + self.diffus + self.reflechi


def cos_incidence(climat: Climat, alpha: float, beta: float) -> np.ndarray:
    """Cosinus de l'angle entre le soleil et la normale à la paroi (équation 7), nul quand le soleil est derrière."""
    a, b = np.radians(alpha), np.radians(beta)
    c = np.cos(climat.gamma) * np.sin(b) * np.cos(climat.psi - a) + np.sin(climat.gamma) * np.cos(b)
    return np.clip(c, 0.0, 1.0)


def masque_azimutal(climat: Climat, hauteurs: list[float], alpha: float) -> np.ndarray:
    """Facteur d'affaiblissement du direct (0 ou 1) pour un masque lointain décrit par 36 tranches de 10°.

    Les tranches sont comptées par rapport à la paroi : la tranche 19 (indice 18) commence dans l'axe de la normale,
    les tranches 10 à 27 couvrent le demi-espace devant la paroi, et l'indice croît dans le sens des azimuts
    (sud, ouest, nord, est). C'est ce que dit la fiche 3.2 (p. 44, § 3.2.3.14.1 et figure 10 : azimut du soleil par
    rapport à la normale à la paroi, normale sur la frontière des tranches 18 et 19) ; les RSEE le confirment, les
    6 617 masques lus occupant les tranches 10 à 27 quelle que soit l'orientation.
    """
    if len(hauteurs) != 36 or not any(hauteurs):
        return np.ones_like(climat.gamma)
    relatif = (np.degrees(climat.psi) - alpha + 180.0) % 360.0
    tranche = np.minimum((relatif // 10).astype(int), 35)
    return (np.degrees(climat.gamma) > np.asarray(hauteurs)[tranche]).astype(float)


@dataclass(frozen=True)
class MasquesProches:
    """Masques proches d'une paroi verticale. Longueurs en mètres ; une profondeur nulle signifie « pas de masque »."""

    dvg: float = 0.0     # profondeur du masque vertical gauche
    dpg: float = 0.0     # distance du masque gauche au bord de la paroi
    dvd: float = 0.0
    dpd: float = 0.0
    largeur: float = 1.0  # largeur de la paroi protégée (lp)
    dhm: float = 0.0     # débord du masque horizontal
    dhp: float = 0.0     # distance du masque horizontal au haut de la paroi
    hauteur: float = 1.0  # hauteur de la paroi protégée (hp)

    def facteurs(self, climat: Climat, alpha: float, beta: float) -> tuple[np.ndarray | float, float]:
        """Facteurs d'affaiblissement du direct (par heure) et du diffus (constant)."""
        if abs(beta - 90.0) > 1e-6 or not (self.dvg > 0 or self.dvd > 0 or self.dhm > 0):
            return 1.0, 1.0
        phi = climat.psi - np.radians(alpha)
        cos_phi = np.cos(phi)
        face = cos_phi >= 1e-5
        tan_phi = np.where(face, np.tan(phi), 0.0)
        direct = np.ones_like(phi)
        if self.dvg > 0:                                              # (19)
            direct *= np.clip(1 - (np.maximum(0.0, self.dvg * tan_phi) - self.dpg) / self.largeur, 0, 1)
        if self.dvd > 0:
            direct *= np.clip(1 - (np.maximum(0.0, -self.dvd * tan_phi) - self.dpd) / self.largeur, 0, 1)
        diffus = 1.0
        if self.dhm > 0:                                              # (20), (21)
            dh = np.maximum(0.0, self.dhm * np.tan(climat.gamma) / np.where(face, cos_phi, 1.0))
            direct *= np.clip(1 - (dh - self.dhp) / self.hauteur, 0, 1)
            diffus = float(np.degrees(np.arctan((self.dhp + self.hauteur / 2) / self.dhm)) / 90.0)
        return np.where(face, direct, 1.0), diffus


def sur_paroi(climat: Climat, alpha: float, beta: float, masque: np.ndarray | None = None, proches: MasquesProches | None = None) -> tuple[Incident, Incident]:
    """Rayonnement (W/m²) et éclairement (lux) incidents sur la paroi, masque lointain compris (équations 8 à 16, 23 à 25)."""
    cos_t = cos_incidence(climat, alpha, beta)
    f_dir = masque if masque is not None else 1.0
    f_dif = 1.0
    if proches is not None:
        p_dir, f_dif = proches.facteurs(climat, alpha, beta)
        f_dir = f_dir * p_dir                                          # (23), (24)
    cb = np.cos(np.radians(beta))
    vue_ciel, vue_sol = 0.5 * (1 + cb), 0.5 * (1 - abs(cb))
    sin_g = np.sin(climat.gamma)
    ray = Incident(cos_t * climat.idn * f_dir, climat.idi * vue_ciel * f_dif, (climat.idn * sin_g + climat.idi) * ALBEDO * vue_sol)
    ecl = Incident(cos_t * climat.edn * f_dir, climat.edi * vue_ciel * f_dif, (climat.edn * sin_g + climat.edi) * ALBEDO * vue_sol)
    return ray, ecl


def rayonnement_froid(climat: Climat, beta: float) -> np.ndarray:
    """Échange radiatif vers la voûte céleste, W/m² (équation 17) : négatif quand le ciel est plus froid que l'air."""
    vue = np.cos(np.radians(beta))
    return HRE * (climat.teciel - climat.te) * (vue if vue > 1e-12 else 0.0)
