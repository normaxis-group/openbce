# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import calendrier, ecs


def test_adultes_equivalents():
    # collectif, 15 logements de 60,25 m² : Nmax = 0,035 x 60,25 = 2,109, plafonné à 1,75 + 0,3 x 0,359 (1689, 1690)
    assert ecs.adultes_equivalents(2, 903.8, 15) == pytest.approx(15 * (1.75 + 0.3 * (0.035 * 903.8 / 15 - 1.75)))
    # maison de 50 m² : interpolation entre 30 et 70 m² (1685)
    assert ecs.adultes_equivalents(1, 50.0, 1) == pytest.approx(1.75 - 0.01875 * 20)
    assert ecs.adultes_equivalents(1, 20.0, 1) == 1.0


def test_cle_de_puisage():
    cal = calendrier.construire()
    for usage in (1, 2):
        cle = ecs.cle_horaire(cal, usage)
        # 52 semaines dont une sans puisage ; les facteurs de semaine valent 0,95 ou 1,05
        assert 48 < cle.sum() < 53
        assert cle[(cal.case >= 10) & (cal.case <= 17)].sum() == 0


def test_volume_plafonne_par_la_surface():
    class Emetteur:
        def nombre(self, cle, defaut=None):
            return {"Rat_em_e": 1.0}.get(cle, defaut)

        def entier(self, cle, defaut=None):
            return {"nb_lgt_gr_em_e": 10}.get(cle, defaut)

    # 10 logements de 9 m² : 40 L/m² l'emporte sur 392 L par adulte équivalent (1691)
    assert ecs.volume_hebdomadaire(2, 90.0, Emetteur()) == pytest.approx(40 * 90.0)
