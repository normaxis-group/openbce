# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import calendrier


def test_cases_horaires_du_tableau_de_la_fiche():
    c = calendrier.construire()
    # itération -> case du scénario, d'après le tableau de la fiche 4.1.3.1
    for iteration, case in ((0, 2), (1, 3), (1895, 1), (1896, 3), (7031, 2), (7032, 2)):
        assert c.case[iteration] == case
    # Le tableau donne la case 2 pour le dernier pas (8759, 23 h UTC en hiver), ce qui contredit sa propre ligne 1895
    # (23 h UTC en hiver, case 1). On garde la règle générale. À CONFIRMER au banc.
    assert c.case[8759] == 1


def test_annee_conventionnelle():
    c = calendrier.construire()
    assert c.jour_semaine[0] == 1 and c.mois[0] == 1 and c.semaine[0] == 1
    assert c.mois[4 * 7 * 24] == 2                       # le mois 1 compte 4 semaines
    assert (c.mois.max(), c.semaine.max(), c.mois_civil.max()) == (12, 5, 12)
    assert (c.mois_civil == 2).sum() == 28 * 24
    midi = 364 * 24 + 12
    assert (c.jour_semaine[midi], c.semaine[midi], c.mois[midi]) == (1, 1, 1)      # le 365e jour est un lundi ordinaire


def test_adultes_equivalents():
    assert calendrier.adultes_equivalents(1, 76, 1) == pytest.approx(1.75 + 0.3 * (0.025 * 76 - 1.75))
    assert calendrier.adultes_equivalents(1, 20, 1) == 1
    assert calendrier.adultes_equivalents(2, 400, 10) == pytest.approx(10 * (1.75 - 0.01875 * 10))
