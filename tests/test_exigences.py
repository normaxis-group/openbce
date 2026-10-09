# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import exigences


def test_bbio_max_bureaux():
    # cas 01 : H3, 241,2 m² de SU, permis 2023 : 95 x (1 + 0,25 + 0,1) = 128,3 (RSEE : 128,3)
    m = exigences.bbio_max(3, "H3", 0.0, 241.2, 0, 241.2, annee_permis=2023)
    assert m["mbgeo"] == 0.25 and m["mbsurf_tot"] == pytest.approx(0.1, abs=0.001)
    assert m["bbio_max"] == pytest.approx(128.3, abs=0.06)


def test_bbio_max_collectif():
    # cas 29 : H3, 903,8 m², 15 logements, BR3 : 65 x (1 - 0,1 + 0 + 0,091 + 0,2) = 77,5 (RSEE : 77,5)
    m = exigences.bbio_max(2, "H3", 0.0, 903.8, 15, 903.8, exposition_bruit=3)
    assert m["mbsurf_moy"] == pytest.approx(0.0004, abs=0.001)
    assert m["mbsurf_tot"] == pytest.approx(0.091, abs=0.001)
    assert m["mbbruit"] == 0.2
    assert m["bbio_max"] == pytest.approx(77.5, abs=0.06)


def test_mbsurf_tot_bureaux_par_periode():
    assert exigences.mbsurf_tot(3, 1562.0, 2023) == pytest.approx((-5.55 - 0.0009 * 1562) / 95)
    assert exigences.mbsurf_tot(3, 1562.0, 2026) == pytest.approx((-4.9 - 0.0022 * 1562) / 95)
    assert exigences.mbsurf_tot(3, 12000.0, 2028) == pytest.approx(-21.4 / 95)


def test_maison_et_altitude():
    assert exigences.mbgeo(1, "H1b", 600.0) == 0.5
    assert exigences.mbcombles(1, 20.0, 100.0) == pytest.approx(0.08)
    assert exigences.mbsurf_moy(1, 358.2, 5) == pytest.approx(0.221, abs=0.001)     # cas 27
    assert exigences.mbbruit(3, "H3", 3, categorie_ce=3) == 0.4


def test_dh_max():
    assert exigences.dh_max(1, "H2b") == 1250 and exigences.dh_max(1, "H3", 2) == 1850
    assert exigences.dh_max(2, "H3", 1, True, 58.6) == pytest.approx(1407.0)      # cas 26 : 1700 - 5 x 58,6
    assert exigences.dh_max(2, "H1a", 2, False, 70.0) == 2100 and exigences.dh_max(3, "H3", 3) is None
