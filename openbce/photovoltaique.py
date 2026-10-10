# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Production photovoltaïque d'un bâtiment (fiches 12.1 à 12.4 de l'annexe III 2026, équations 2366 à 2374).

Un champ est un ensemble de N modules identiques reliés à un onduleur ; une installation (PV_install) porte un ou
plusieurs onduleurs. La puissance d'un module au point de puissance maximale dépend du rayonnement efficace dans son
plan (direct, diffus de ciel et réfléchi par le sol, chacun affecté d'une perte optique par réflexion) et de sa
température, calculée par un bilan entre l'air, la voûte céleste et le rayonnement absorbé (2373). L'onduleur applique
sa courbe de rendement et s'éteint au-delà de 115 % de sa puissance nominale (2374).

Codes du récapitulatif : Type_Techno_Capteur 0 à 5 (mono-Si, multi-Si, CdTe, CIS, amorphe, autre, tableau 328) ;
Valeur_Declaree_Defaut (statut de Pc, Mu et NOCT) et Type_Confinement (face arrière libre, confinée, autre) sont lus
selon les correspondances STATUT et CONFINEMENT, déduites du banc (banc/pv.py) faute d'une table dans le texte.
"""
from __future__ import annotations

import numpy as np

from .climat import Climat
from .rayonnement import cos_incidence, masque_azimutal, sur_paroi
from .rsee import Noeud

TAU_ALPHA = 0.9                 # coefficient de transmission-absorption solaire des modules (tableau 327)
FM = 0.97                       # pertes par connectique et mismatch (tableau 327)
U2 = 5.0                        # échange vers la voûte céleste, W/(m².K) (2368)
DT_CIEL_REF = -13.0             # écart de référence air - voûte céleste, °C (tableau 327)
NOCT_UTIL_MIN = 40.0            # °C
MU_UTIL_MIN = {0: 0.00425, 1: 0.00433, 2: 0.00208, 3: 0.00325, 4: 0.00175, 5: 0.00433}   # par technologie, °C-1
GAMMA_BASSE_LUMIERE = {0: 0.07, 1: 0.07, 2: 0.0, 3: 0.07, 4: 0.0, 5: 0.07}              # tableau 329
# Type_Confinement du récapitulatif -> coefficient CT (1 face arrière libre, 2 confinée, 1,5 autre) ; lecture du banc.
CONFINEMENT = {0: 1.0, 1: 2.0, 2: 1.5}
# Valeur_Declaree_Defaut du récapitulatif -> statut : "defaut", "declaree", "justifiee", "certifiee" ; lecture du banc.
STATUT = {0: "defaut", 1: "declaree", 2: "justifiee", 3: "certifiee"}
RENDEMENT_ONDULEUR_DEFAUT = 0.9


def parametres_capteur(techno: int, statut: str, pc: float, mu: float, noct: float) -> tuple[float, float, float]:
    """Valeurs de calcul de Pc, μ et NOCT selon le statut de la donnée (12.3.3)."""
    mu_min = MU_UTIL_MIN.get(techno, 0.00433)
    if statut == "certifiee":
        return pc, mu, noct
    if statut == "justifiee":
        return 0.9 * pc, 1.1 * mu, 1.1 * noct
    if statut == "declaree":
        return 0.8 * pc, max(1.2 * mu, mu_min), max(1.2 * noct, NOCT_UTIL_MIN)
    return 0.8 * pc, 1.2 * mu_min, 1.2 * NOCT_UTIL_MIN


def fopt(theta_deg) -> np.ndarray:
    """Perte optique par réflexion selon l'angle à la normale, en degrés (12.3.3)."""
    return 1.0 - 0.05 * (1.0 / np.cos(np.radians(np.minimum(87.0, theta_deg))) - 1.0)


def champ(climat: Climat, n: int, pc: float, mu: float, noct: float, techno: int, ct: float, alpha: float, beta: float, s: float,
          masque: np.ndarray | None = None) -> np.ndarray:
    """Puissance MPPT horaire du champ absorbée par l'onduleur, W (2371 à 2373)."""
    ray, _ = sur_paroi(climat, alpha, beta, masque)
    cos_t = cos_incidence(climat, alpha, beta)
    theta = np.degrees(np.arccos(np.clip(cos_t, 0.0, 1.0)))
    theta1 = 59.7 - 0.13888 * beta + 0.001497 * beta ** 2
    theta2 = 90.0 - 0.5788 * beta + 0.002693 * beta ** 2
    g = fopt(theta) * ray.direct + fopt(theta1) * ray.diffus + fopt(theta2) * ray.reflechi
    eta_stc = pc / (s * 1000.0)                                                                          # (2366)
    fr = (1 + np.cos(np.radians(30.0))) / 2                                                              # (2369)
    f = (1 + np.cos(np.radians(beta))) / 2                                                               # (2370)
    u1 = (TAU_ALPHA * 800.0 / (noct - 20.0) - fr * U2 * (noct - DT_CIEL_REF - 20.0) / (noct - 20.0)) / ct   # (2367)
    tm = (u1 * climat.te + f * U2 * climat.teciel + g * (TAU_ALPHA - eta_stc)) / (u1 + f * U2)           # (2373)
    gamma = GAMMA_BASSE_LUMIERE.get(techno, 0.07)
    pmpp = pc * g / 1000.0 * np.maximum(0.0, 1.0 + gamma * np.log(np.maximum(1e-4, g) / 1000.0)) * (1.0 - mu * (tm - 25.0))   # (2372)
    return np.maximum(pmpp, 0.0) * n * FM


def onduleur(ppv: np.ndarray, pac_nom: float, rendement: float | None = None, courbe: tuple | None = None) -> np.ndarray:
    """Puissance délivrée au réseau, W (2374) : rendement par défaut 0,9 (nul à vide, atteint à 20 % de charge), rendement
    européen saisi, ou courbe (X_i, η_i) ; extinction au-delà de 115 % de la puissance nominale."""
    if pac_nom <= 0:
        return np.zeros_like(ppv)
    x = ppv / pac_nom
    if courbe:
        xs, ys = (0.0,) + tuple(courbe[0]), (0.0,) + tuple(courbe[1])
    else:
        e = rendement if rendement else RENDEMENT_ONDULEUR_DEFAUT
        xs, ys = (0.0, 0.2, 1.0), (0.0, e, e)
    eta = np.interp(x, xs, ys)
    return ppv * eta * (x <= 1.15)


def _capteur(climat: Climat, c: Noeud) -> tuple[np.ndarray, float, float]:
    """Puissance MPPT du champ décrit par un Capteur_PV, et (N, Pc saisie) pour la puissance par défaut de l'onduleur."""
    n = c.entier("Nb_capteurs_PV", 1)
    techno = c.entier("Type_Techno_Capteur", 5)
    statut = STATUT.get(c.entier("Valeur_Declaree_Defaut", 0), "defaut")
    pc, mu, noct = parametres_capteur(techno, statut, c.nombre("Pc", 0.0), c.nombre("Mu", 0.0), c.nombre("NOCT", 0.0))
    ct = CONFINEMENT.get(c.entier("Type_Confinement", 1), 2.0)
    masques = c.directs("Masque_Lointain_Azimutal")
    masque = masque_azimutal(climat, list(masques[0].serie("Gamma")), c.nombre("Alpha", 0.0)) if masques else None
    s = c.nombre("S", 0.0)
    if pc <= 0 or s <= 0 or n <= 0:
        return np.zeros_like(climat.te), float(n), c.nombre("Pc", 0.0)
    return champ(climat, n, pc, mu, noct, techno, ct, c.nombre("Alpha", 0.0), c.nombre("Beta", 0.0), s, masque), float(n), c.nombre("Pc", 0.0)


def _onduleur(climat: Climat, o: Noeud) -> np.ndarray:
    ppv = np.zeros_like(climat.te)
    n_pc = 0.0
    for c in o.directs("Capteur_PV"):
        p, n, pc = _capteur(climat, c)
        ppv += p
        n_pc += n * pc
    pac = o.nombre("Pac_Onduleur", 0.0) if o.entier("Valeur_Declaree_Defaut_Pac_Onduleur", 2) != 2 else 0.0
    if pac <= 0:
        pac = 0.8 * n_pc                                                                                 # PAC NOM par défaut (12.4.3)
    type_courbe = o.entier("Type_CourbeRend", 0)
    rendement = o.nombre("n_EU", 0.0) if type_courbe == 1 else None
    return onduleur(ppv, pac, rendement)


def du_batiment(batiment: Noeud, climat: Climat) -> np.ndarray:
    """Production horaire de toutes les installations du bâtiment, Wh (puissance moyenne sur l'heure)."""
    total = np.zeros_like(climat.te)
    for inst in batiment.tous("PV_install"):
        for o in inst.directs("Onduleur_PV"):
            total += _onduleur(climat, o)
    return total
