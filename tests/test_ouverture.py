# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import ouverture as o


def test_moderation_exterieure():
    assert o.moderation_exterieure(8, 27, 26, False) == 0
    assert o.moderation_exterieure(14, 27, 26, False) == pytest.approx(0.5)
    assert o.moderation_exterieure(22, 27, 26, False) == 1
    assert o.moderation_exterieure(31, 27, 26, False) == 0        # plus de 3 °C au-dessus de l'intérieur
    assert o.moderation_exterieure(26, 27, 26, True) == 0         # en période de refroidissement : fermé dès 25 °C dehors


def test_hysteresis():
    # hors saison de chauffage, consigne 26 : ouverture entre 23 et 25 °C, fermeture entre 23 et 22 °C
    assert o.ratio_thermique(22.5, 0.0, 26, False) == 0
    assert o.ratio_thermique(24.0, 0.0, 26, False) == pytest.approx(0.5)
    assert o.ratio_thermique(22.5, 1.0, 26, False) == pytest.approx(0.5)
    assert o.ratio_thermique(21.0, 1.0, 26, False) == 0


def test_debit_non_traversant():
    g = o.Ouvrants(((2.0, 0, 90, 1),), False, 1.5)
    q = g.debit([1.0], 0.0, 20, 26)
    assert q == pytest.approx(2.0 / 2 * (0.0035 * 1.5 * 6) ** 0.5 * 1.2 * 292 / 293)
    assert g.debit([0.0], 3.0, 20, 26) == 0


def test_section_limitee_par_le_volet_baisse():
    g = o.Ouvrants(((2.0, 0, 90, 1),), False, 1.5, rang=(0,), passage=(0.10,))
    assert g.sections([1.0], [0.0]) == [1.0]
    assert g.sections([1.0], [1.0]) == [0.10]
    assert g.sections([0.3], [0.5]) == [0.3]            # la section libre (0,55) dépasse l'ouverture demandée
