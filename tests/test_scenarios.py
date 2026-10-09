# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import calendrier, scenarios


def test_maison_individuelle():
    cal = calendrier.construire()
    s = scenarios.habitation(cal, 1, 76, 1)
    assert set(s.consigne_ch) == {16.0, 19.0} and set(s.consigne_fr) == {26.0, 30.0}
    # lundi de la première semaine : inoccupé de 9 h à 17 h légales (cases 10 à 17), soit 8 heures
    lundi = slice(0, 23)
    assert (s.occupation[lundi] == 0).sum() == 8
    # dernière semaine de décembre : vacances, consigne réduite et aucun occupant
    vacances = 360 * 24 + 12
    assert s.consigne_ch[vacances] == 16.0 and s.occupants[vacances] == 0
    assert s.apports_usages.max() == pytest.approx(76 * 5.7)
    assert s.apports_occupants.max() == pytest.approx(s.nadeq * 90)


def test_collectif_les_apports_portent_sur_le_local_d_habitation():
    cal = calendrier.construire()
    s = scenarios.habitation(cal, 2, 1000, 20)
    assert s.apports_usages.max() == pytest.approx(900 * 5.7)
    assert s.nadeq == pytest.approx(calendrier.adultes_equivalents(2, 900, 20))
