# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Climat extérieur du site (annexe III, fiche 3.1 C_EEX_Climat extérieur).

Part des séries météo conventionnelles de la zone (au niveau de la mer) et rend les séries du site : correction
d'altitude, éclairements, température de base, période de confort adaptatif.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# température de base au niveau de la mer, par département (fiche 3.1.3)
_BASE = {
    -9.0: "01 02 03 05 08 10 14 15 19 21 23 25 27 28 38 39 42 43 45 51 52 54 55 57 58 59 60 61 62 63 67 68 69 70 71 73 74 75 76 77 78 80 87 88 89 90 91 92 93 94 95",
    -6.0: "04 07 09 12 16 17 18 22 24 26 29 31 32 33 35 36 37 40 41 44 46 47 48 49 50 53 56 64 65 72 79 82 81 84 85 86",
    -3.0: "06 11 13 2A 2B 30 34 66 83",
}
BASE_EXT_0 = {d: t for t, liste in _BASE.items() for d in liste.split()}
# Zone climatique par département. Répartition saisie de mémoire d'après le découpage réglementaire en huit zones :
# À VÉRIFIER sur l'annexe de l'article R.172-4 du code de la construction.
_ZONES = {
    "H1a": "02 14 27 28 59 60 61 62 75 76 77 78 80 91 92 93 94 95",
    "H1b": "08 10 45 51 52 54 55 57 58 67 68 70 88 89 90",
    "H1c": "01 03 05 15 19 21 23 25 38 39 42 43 63 69 71 73 74 87",
    "H2a": "22 29 35 50 56",
    "H2b": "16 17 18 36 37 41 44 49 53 72 79 85 86",
    "H2c": "09 12 24 31 32 33 40 46 47 64 65 81 82",
    "H2d": "04 07 26 48 84",
    "H3": "06 11 13 2A 2B 30 34 66 83",
}
# Vérifié par le banc des exigences (O_Mbgeo des RSEE) pour les départements 04, 06, 13, 31, 33, 83 et 84 ; les autres
# restent à relire sur le chapitre IV de l'annexe à l'article R. 172-4.
ZONE_CLIMATIQUE = {d: z for z, liste in _ZONES.items() for d in liste.split()}
# rendement lumineux du rayonnement direct : polynôme de degré 6 (fiche 3.1.3). Le texte ne nomme pas la variable x ;
# on prend la hauteur du soleil en degrés, comme dans la méthode Th-BCE 2012. À CONFIRMER par le banc (éclairage).
_POLY_EDN = (-1.03753210e-08, 2.90312257e-06, -3.31804423e-04, 1.99283162e-02, -6.72171072e-01, 1.24650445e01, 2.38954889e00)


def altitude_corrigee(altitude: float) -> float:
    """Le site est ramené à 100, 500 ou 900 m."""
    if altitude <= 400:
        return 100.0
    return 500.0 if altitude <= 800 else 900.0


def departement(code: str | int) -> str:
    c = str(code).strip().upper()
    return c if c in ("2A", "2B") else c.zfill(2)


@dataclass
class Climat:
    """Séries horaires du site (8 760 valeurs) ; angles en radians."""

    te: np.ndarray          # température extérieure, °C
    we: np.ndarray          # poids d'eau, kg/kg d'air sec
    idn: np.ndarray         # rayonnement direct normal, W/m²
    idi: np.ndarray         # rayonnement diffus horizontal, W/m²
    edn: np.ndarray         # éclairement direct normal, lux
    edi: np.ndarray         # éclairement diffus horizontal, lux
    teciel: np.ndarray      # température du ciel, °C
    vent: np.ndarray        # vitesse du vent à 10 m, m/s
    teau: np.ndarray        # température d'eau froide, °C
    gamma: np.ndarray       # hauteur du soleil, rad
    psi: np.ndarray         # azimut du soleil par rapport au sud, négatif au lever, rad
    base_ext: float         # température extérieure de base, °C
    theta_rm: np.ndarray    # moyenne glissante journalière de la température extérieure, °C (par heure)
    confort_adaptatif: np.ndarray   # 1 en période de confort adaptatif


def du_site(meteo: dict[str, np.ndarray], code_departement: str | int, altitude: float) -> Climat:
    alt = altitude_corrigee(altitude)
    te = meteo["te0"] - 0.005 * alt
    idn, idi = meteo["dirN"], meteo["diff"]
    gamma_deg = np.maximum(meteo["gamma"], 0.0)
    edn = idn * np.polyval(_POLY_EDN, gamma_deg)
    edi = np.where(idn < 1, 124.0, np.where(idn > 120, 128.0, 116.0)) * idi
    # moyenne glissante : calculée au premier pas de temps du jour sur les 24 heures de la veille (équation 1)
    jours = te.reshape(-1, 24).mean(axis=1)
    rm = np.zeros(len(jours))
    for j in range(1, len(jours)):
        rm[j] = 0.8 * rm[j - 1] + 0.2 * jours[j - 1]
    chauds = np.nonzero(rm >= 16.0)[0]
    adaptatif = np.zeros(len(jours))
    if len(chauds):
        adaptatif[chauds[0]:chauds[-1] + 1] = 1
    return Climat(
        te=te, we=(meteo["we0"] - 0.0025 * alt) / 1000.0, idn=idn, idi=idi, edn=edn, edi=edi, teciel=meteo["teciel"],
        vent=meteo["vent"], teau=meteo["teau"] - 0.005 * alt, gamma=np.radians(gamma_deg), psi=np.radians(meteo["psi"]),
        base_ext=BASE_EXT_0[departement(code_departement)] - 0.005 * alt, theta_rm=np.repeat(rm, 24), confort_adaptatif=np.repeat(adaptatif, 24))
