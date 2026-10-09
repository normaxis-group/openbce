# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import climat, rayonnement


def meteo(gamma, psi, idn=800.0, idi=100.0):
    n = 48
    return {"te0": np.full(n, 10.0), "we0": np.full(n, 6.0), "dirN": np.full(n, idn), "diff": np.full(n, idi), "teciel": np.full(n, 0.0),
            "vent": np.full(n, 3.0), "teau": np.full(n, 12.0), "gamma": np.full(n, gamma), "psi": np.full(n, psi)}


def test_correction_d_altitude():
    c = climat.du_site(meteo(30, 0), "83", 600)
    assert c.te[0] == pytest.approx(10 - 0.005 * 500)
    assert c.we[0] == pytest.approx((6 - 0.0025 * 500) / 1000)
    assert c.base_ext == pytest.approx(-3 - 2.5)
    assert climat.du_site(meteo(30, 0), 1, 0).base_ext == pytest.approx(-9.5)


def test_rayonnement_sur_paroi():
    c = climat.du_site(meteo(30, 0), "83", 0)           # soleil plein sud, 30° au-dessus de l'horizon
    sud, _ = rayonnement.sur_paroi(c, 0, 90)
    nord, _ = rayonnement.sur_paroi(c, 180, 90)
    toit, _ = rayonnement.sur_paroi(c, 0, 0)
    assert sud.direct[0] == pytest.approx(800 * np.cos(np.radians(30)))
    assert nord.direct[0] == 0
    assert toit.direct[0] == pytest.approx(400) and toit.diffus[0] == pytest.approx(100) and toit.reflechi[0] == 0
    assert sud.diffus[0] == pytest.approx(50) and sud.reflechi[0] == pytest.approx((400 + 100) * 0.2 * 0.5)


def test_masque_azimutal():
    c = climat.du_site(meteo(30, 0), "83", 0)           # soleil plein sud, à 30°
    devant = [0.0] * 18 + [40.0] + [0.0] * 17           # obstacle de 40° dans la tranche qui part de la normale
    assert rayonnement.masque_azimutal(c, devant, 0)[0] == 0        # paroi sud : le soleil est derrière l'obstacle
    assert rayonnement.masque_azimutal(c, devant, 90)[0] == 1       # paroi ouest : le soleil est 90° à gauche de la normale
    assert rayonnement.masque_azimutal(c, [20.0 if k == 18 else 0.0 for k in range(36)], 0)[0] == 1   # obstacle plus bas que le soleil
    a_gauche = [0.0] * 9 + [40.0] + [0.0] * 26          # tranche des azimuts relatifs de -90° à -80°
    assert rayonnement.masque_azimutal(c, a_gauche, 90)[0] == 0


def test_masques_proches():
    c = climat.du_site(meteo(45, 0), "83", 0)          # soleil plein sud, à 45°
    casquette = rayonnement.MasquesProches(dhm=1.0, dhp=0.0, hauteur=2.0)
    direct, diffus = casquette.facteurs(c, 0, 90)
    assert direct[0] == pytest.approx(0.5)             # l'ombre descend d'un mètre sur une baie de deux mètres
    assert diffus == pytest.approx(0.5)                # le centre de la baie voit le ciel sous 45° : 45 / 90
    assert casquette.facteurs(c, 0, 0) == (1.0, 1.0)   # sans effet sur une paroi non verticale
    joue = rayonnement.MasquesProches(dvg=1.0, largeur=2.0)
    assert joue.facteurs(c, -45, 90)[0][0] == pytest.approx(0.5)   # soleil à 45° sur la gauche de la normale
    assert joue.facteurs(c, 45, 90)[0][0] == pytest.approx(1.0)
