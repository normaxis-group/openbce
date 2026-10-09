# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import eclairage


def test_c2_du_logement():
    assert eclairage.c2_logement(50) == 1 and eclairage.c2_logement(3000) == 0
    assert eclairage.c2_logement(150) == pytest.approx(0.525)


def test_consommation():
    # 100 m², nuit, éclairage autorisé : 1 W/m² x 0,9
    assert eclairage.consommation_logement(0.0, 1, 100.0) == pytest.approx(90.0)
    assert eclairage.consommation_logement(0.0, 0, 100.0) == 0


def test_coefficients_d_eclairement():
    ro = (0.2 + 2.5 * 0.5 + 0.7) / 4.5
    assert eclairage.K2 == pytest.approx(0.4 + ro / (1 - ro) / 4.5)


def test_circulations_et_sanitaires_aveugles_non_comptes():
    class Local:
        def __init__(self, genre, part, nat):
            self.v = {"Locaux_Bureau": genre, "Rat_local": part, "Ratio_ecl_nat": nat}

        def entier(self, cle, defaut=0):
            return int(self.v.get(cle, defaut))

        def nombre(self, cle, defaut=0.0):
            return float(self.v.get(cle, defaut))

    class Groupe:
        def directs(self, nom):
            return [Local(0, 0.5, 0.0), Local(2, 0.3, 0.0), Local(3, 0.1, 0.0), Local(2, 0.1, 1.0)]

    locaux = eclairage.locaux_tertiaires(Groupe())
    assert [c1 for _, _, c1, _ in locaux] == [0.85, 0.0, 0.0, 0.75]
    conso, _ = eclairage.consommation_tertiaire(0.0, 0.0, 0.0, 1.0, 100.0, locaux)
    assert conso == pytest.approx(100.0 * (0.5 * 10.0 * 0.85 + 0.1 * 2.0 * 0.75))     # nuit : C2 = 1 partout
