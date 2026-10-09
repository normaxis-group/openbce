# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import ballon


def test_uas_defaut_vertical():
    class N:
        def entier(self, k, d=0): return {"Valeur_Certifiee_Justifiee_Defaut": 2, "Nature_Ballon": 1}.get(k, d)
        def nombre(self, k, d=0.0): return {"V_tot": 200.0, "UA_S": 0.0}.get(k, d)
    qpr = 0.224 + 0.0663 * 200 ** (2 / 3)
    assert ballon.uas_util(N()) == pytest.approx(qpr * 1000 / (45 * 24))


def test_melange():
    t, v = [60.0, 50.0, 55.0, 58.0], [50.0] * 4
    ballon.melanger(t, v)
    assert t == pytest.approx([55.0, 55.0, 55.0, 58.0]) and t == sorted(t)


def test_puisage_conserve_l_energie():
    b = ballon.Ballon(v=[50.0] * 4, u=[0.0] * 4, theta=[55.0] * 4, theta_prec=[55.0] * 4)
    fourni, vp = b.puiser(2000.0, 10.0, 40.0)
    assert fourni == pytest.approx(2000.0) and vp == pytest.approx(2000 / (1.163 * 45))
    contenu_avant, contenu_apres = 1.163 * 200 * 55, sum(1.163 * 50 * t for t in b.theta)
    assert contenu_avant - contenu_apres == pytest.approx(fourni, rel=1e-6)   # l'énergie puisée est comptée au-dessus de l'eau froide entrée
    assert b.theta == sorted(b.theta) and b.report == 0.0


def test_report_quand_le_haut_est_froid():
    b = ballon.Ballon(v=[50.0] * 4, u=[0.0] * 4, theta=[35.0] * 4, theta_prec=[35.0] * 4)
    fourni, vp = b.puiser(1000.0, 10.0, 40.0)
    assert fourni == 0.0 and b.report == 1000.0 and b.nbh_report == 1


def test_demande_chauffe_et_injection():
    b = ballon.Ballon(v=[50.0] * 4, u=[1.0] * 4, theta=[45.0] * 4, theta_prec=[45.0] * 4)
    pertes = b.pertes(20.0)
    q = b.demande_chauffe(1, 1, 2.0, 0, 12, False, pertes)
    assert q == pytest.approx(1.163 * 200 * 10 + sum(pertes))
    b.injecter(1, q, pertes)
    assert all(t == pytest.approx(55.0, abs=1e-6) for t in b.theta)
