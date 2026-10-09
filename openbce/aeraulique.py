# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Bilan aéraulique d'une zone (annexe III, fiche 5.6) : débits d'air par les défauts d'étanchéité de l'enveloppe.

La pression intérieure au niveau du plancher, Pib, est celle qui annule la somme des débits massiques. En mode Th-B la
ventilation conventionnelle est équilibrée (débit soufflé = débit repris) : seuls les défauts d'étanchéité entrent
dans le bilan et les entrées d'air du projet n'y sont pas (banc du Bbio : H_V_Def_Hiver reproduit sans elles). En modes
Th-C et Th-D, le débit net extrait par la ventilation mécanique et les entrées d'air entrent dans le bilan (167).

Limites actuelles : un bilan par groupe (pas d'échange entre groupes par le hall) ; zones d'habitation, donc sans
tirage thermique entre niveaux (138).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rsee import Noeud

RHO_REF, THETA_REF = 1.2, 19.0     # kg/m³ à 19 °C
MA_SUR_MW = 28.976 / 18.0
G = 9.81
CVENT = 0.9                        # correction locale de la vitesse du vent (fiche 3.2)
CPA = 1006.0                       # J/(kg.K)
Q4PA_DEFAUT = {1: 0.6, 2: 1.0, 3: 1.7}   # m³/(h.m²) : maison, collectif, bureaux (tableau 30)


def masse_volumique(theta: float, omega: float) -> float:
    return RHO_REF * (273 + THETA_REF) / (273 + theta) * (1 + omega) / (1 + omega * MA_SUR_MW)   # (131), (132)


def coefficients_pression(traversante: bool, h_moy: float) -> tuple[float, float, float]:
    """Cp des façades au vent, sous le vent et du toit (tableaux 23 et 24, écrantage « normal »)."""
    if not traversante:
        return 0.05, -0.05, 0.0
    return (0.25 if h_moy < 15 else 0.45), -0.50, -0.60


@dataclass(frozen=True)
class Fuites:
    """Défauts d'étanchéité d'un groupe : (coefficient en m³/(h.Pa^2/3), Cp, altitude en m) par point de fuite."""

    points: tuple[tuple[float, float, float], ...]
    anti_retour: float = 1.0      # entrées d'air : coefficient de réduction du débit sortant (146)

    def debits(self, pib: float, vent: float, rho_ext: float, rho_int: float) -> list[float]:
        """Débits volumiques par point de fuite, en m³/h, positifs en entrée (135 à 137, 151)."""
        q = []
        for c, cp, z in self.points:
            dp = 0.5 * cp * rho_ext * vent * vent - G * z * rho_ext - (pib - rho_int * G * z)
            q.append(c * abs(dp) ** (2 / 3) * (1 if dp > 0 else -1))
        return q

    def equilibre(self, vent_meteo: float, theta_ext: float, omega_ext: float, theta_int: float, omega_int: float) -> tuple[float, float]:
        """Débit massique d'air neuf entrant (kg/s) et pression Pib (Pa), à l'équilibre des masses (167, 171)."""
        if not self.points:
            return 0.0, 0.0
        vent = CVENT * vent_meteo
        rho_e, rho_i = masse_volumique(theta_ext, omega_ext), masse_volumique(theta_int, omega_int)

        def bilan(pib):
            return sum(q * (rho_e if q > 0 else rho_i) for q in self.debits(pib, vent, rho_e, rho_i))

        bas, haut = -200.0, 200.0          # le bilan décroît quand Pib augmente
        for _ in range(50):
            milieu = 0.5 * (bas + haut)
            if bilan(milieu) > 0:
                bas = milieu
            else:
                haut = milieu
        pib = 0.5 * (bas + haut)
        entrant = sum(q * rho_e for q in self.debits(pib, vent, rho_e, rho_i) if q > 0) / 3600.0
        return entrant, pib


def air_neuf(f: Fuites, vent_meteo: np.ndarray, theta_ext: np.ndarray, omega_ext: np.ndarray, theta_int: np.ndarray | float,
             entrees: Fuites | None = None, extraction: np.ndarray | float = 0.0) -> np.ndarray:
    """Débit massique d'air neuf entrant (kg/s) pour toutes les heures à la fois : même équilibre que
    `Fuites.equilibre`, résolu par dichotomie vectorisée. L'humidité intérieure est prise égale à l'extérieure.

    `entrees` : entrées d'air du groupe, mêmes conventions que les défauts d'étanchéité mais en exposant 1/2 (141,
    146) ; `extraction` : débit net extrait mécaniquement (repris - soufflé), en m³/h, qui entre dans le bilan (167)
    comme un terme constant à la masse volumique intérieure (154). L'air neuf est la somme des débits entrants par
    les défauts et les entrées d'air (171)."""
    n = len(theta_ext)
    extraction = np.broadcast_to(np.asarray(extraction, dtype=float), (n,))
    if not f.points and not (entrees and entrees.points):
        return np.zeros(n)
    vent = CVENT * vent_meteo
    rho_e = RHO_REF * (273 + THETA_REF) / (273 + theta_ext) * (1 + omega_ext) / (1 + omega_ext * MA_SUR_MW)
    rho_i = RHO_REF * (273 + THETA_REF) / (273 + np.broadcast_to(theta_int, (n,))) * (1 + omega_ext) / (1 + omega_ext * MA_SUR_MW)

    def debits(pib):
        for c, cp, z in f.points:
            dp = 0.5 * cp * rho_e * vent * vent - G * z * rho_e - (pib - rho_i * G * z)
            yield c * np.cbrt(dp * dp) * np.sign(dp)
        if entrees:
            for c, cp, z in entrees.points:
                dp = 0.5 * cp * rho_e * vent * vent - G * z * rho_e - (pib - rho_i * G * z)
                yield c * np.sqrt(np.abs(dp)) * np.sign(dp) * np.where(dp < 0, entrees.anti_retour, 1.0)

    bas, haut = np.full(n, -400.0), np.full(n, 400.0)
    for _ in range(50):
        milieu = 0.5 * (bas + haut)
        bilan = sum(q * np.where(q > 0, rho_e, rho_i) for q in debits(milieu)) - rho_i * extraction
        positif = bilan > 0
        bas, haut = np.where(positif, milieu, bas), np.where(positif, haut, milieu)
    return sum(np.maximum(q, 0.0) for q in debits(0.5 * (bas + haut))) * rho_e / 3600.0


def entrees_air(zone: Noeud, groupe: Noeud, tirage_si_haut: bool = True) -> Fuites:
    """Entrées d'air du groupe (fiche 5.6, 141 à 147, tableaux 25 et 26) : le module M (m³/h sous 20 Pa) donne la
    caractéristique q = C |dP|^0,5 avec C = M / 20^0,5 ; un quart du module à chaque point (au vent ou sous le vent,
    en bas ou en haut), aux mêmes hauteurs que les défauts d'étanchéité. PREMIER JET : entrée fixe (Type_entree_air
    0) ; l'autorégulabilité (143 à 145, 1 % des entrées du banc) est ignorée ; l'anti-retour r est lu (R_f)."""
    module = sum(e.nombre("Module", 0.0) for e in groupe.directs("Entree_Air"))
    if module <= 0:
        return Fuites(())
    r = min((e.nombre("R_f", 1.0) for e in groupe.directs("Entree_Air")), default=1.0)
    z0, h_zone = zone.nombre("Hauteur", 0.0), zone.nombre("Hauteur_Zone", 2.5)
    traversante = zone.entier("Usage") != 2 or zone.entier("Is_Traversant", 1) == 1
    cp_v, cp_s, _ = coefficients_pression(traversante, z0 + 0.5 * h_zone)
    h = min(h_zone, 15.0) if tirage_si_haut and h_zone >= 3 else min(h_zone, 3.0)
    zb, zh = z0 + 0.25 * h, z0 + 0.75 * h
    c = module / 20.0 ** 0.5 / 4
    return Fuites(tuple((c, cp, z) for cp in (cp_v, cp_s) for z in (zb, zh)), anti_retour=r)


def du_groupe(zone: Noeud, groupe: Noeud, tirage_si_haut: bool = True) -> Fuites:
    """Répartition conventionnelle de la perméabilité : un quart de la façade à chaque point (au vent ou sous le vent,
    en bas ou en haut), et le toit à part (150, tableaux 27 à 29)."""
    permea = groupe.un("Permeabilite")
    q4 = permea.nombre("Q4PaSurf")
    # Valeur par défaut de la perméabilité selon l'usage (tableau 30), quand le champ Valeur_Saisie_Defaut_Q4PaSurf
    # vaut 0. Sens du champ déduit des RSEE : les zones qui le portent à 0 ont une perméabilité saisie nulle et une
    # déperdition par infiltration H_V_Def_Hiver importante.
    if permea.entier("Valeur_Saisie_Defaut_Q4PaSurf", 1) == 0:
        q4 = Q4PA_DEFAUT.get(zone.entier("Usage"), 1.7)
    # Une perméabilité mesurée par échantillonnage est multipliée par 1,2 : fiche 5.6 p. 145 et article 17 de l'arrêté
    # du 4 août 2021. Le champ id_echantillonnage_permea la signale par la valeur 0 (banc : rapport de 1,20 à 1,23 entre
    # les groupes à 0 et à 1, indépendant de Q4). La majoration ne vise que les valeurs mesurées : une valeur par défaut
    # du tableau 30 n'est pas majorée (aucun RSEE ne tranche ce cas, décision du 10/10/2026).
    if permea.entier("id_echantillonnage_permea", 1) == 0 and permea.entier("Valeur_Saisie_Defaut_Q4PaSurf", 1) == 1:
        q4 *= 1.2
    a_facade = a_toit = 0.0
    for n, cle in [(p, "Ak") for p in groupe.directs("Paroi_Opaque")] + [(b, "Ab") for b in groupe.directs("Baie")]:
        beta = n.nombre("Beta")
        if beta > 120:
            continue                         # plancher bas : hors perméabilité
        if beta >= 60:
            a_facade += n.nombre(cle)        # façade : moins de 30° par rapport à la verticale
        else:
            a_toit += n.nombre(cle)
    c_facade, c_toit = a_facade * q4 / 4 ** (2 / 3), a_toit * q4 / 4 ** (2 / 3)
    z0, h_zone = zone.nombre("Hauteur", 0.0), zone.nombre("Hauteur_Zone", 2.5)
    traversante = zone.entier("Usage") != 2 or zone.entier("Is_Traversant", 1) == 1      # conventionnel hors collectif (tableau 22)
    cp_v, cp_s, cp_t = coefficients_pression(traversante, z0 + 0.5 * h_zone)
    # (138) dit qu'en habitation il n'y a pas de tirage thermique entre niveaux (hauteur limitée à 3 m). Le banc dit
    # le contraire : avec 3 m, l'indicateur H_V_Def_Hiver des RSEE est sous-estimé de 24 à 72 % et l'écart dépend du
    # caractère traversant ; avec la hauteur de la zone plafonnée à 15 m dès qu'elle atteint 3 m, l'écart tombe dans
    # une bande de 0 à -28 % qui n'en dépend plus. On retient donc cette lecture, déduite du banc.
    h = min(h_zone, 15.0) if tirage_si_haut and h_zone >= 3 else min(h_zone, 3.0)
    zb, zh, zt = z0 + 0.25 * h, z0 + 0.75 * h, z0 + h
    points = [(c_facade / 4, cp, z) for cp in (cp_v, cp_s) for z in (zb, zh)] if c_facade > 0 else []
    if c_toit > 0:
        points.append((c_toit, cp_t, zt))
    return Fuites(tuple(points))
