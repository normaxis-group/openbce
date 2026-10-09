# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import distribution as d


def _reseau(**kw):
    base = dict(fonction=d.CHAUD, idtype=1, id_dp=1, lvc=60.0, lhvc=0.0, u_vc=0.6, u_hvc=0.0, paux=50.0, iddebit=3, idgest=3, idcirc=2,
                theta_dep_dim=35.0, theta_ret_dim=30.0, d_theta_dim=5.0, qnom=1.0, qresid=0.0)
    base.update(kw)
    return d.ReseauGroupe(**base)


def test_loi_d_eau_suit_la_figure_97():
    r = _reseau()
    q = d.RHO_CP * 1.0 * 5.0                                     # demande qui donne le débit nominal et Δθ = 5 K
    assert d.reseau_groupe(r, q, 20.0, -5.0, -5.0).theta_dep == 35.0              # à la température de base : départ de dimensionnement
    milieu = d.reseau_groupe(r, q, 20.0, 5.0, -5.0).theta_dep                     # à mi-chemin entre -5 et 15 : 27,5 °C
    assert milieu == pytest.approx(27.5)
    doux = d.reseau_groupe(r, q, 20.0, 16.0, -5.0).theta_dep                      # au-delà de 15 °C : max(20 ; θi + Δθ)
    assert doux == pytest.approx(25.0)
    assert d.reseau_groupe(r, 0.0, 19.0, 0.0, -5.0).theta_dep == 19.0             # réseau à l'arrêt : θi


def test_retour_pertes_et_circulateur():
    r = _reseau(idgest=1)
    e = d.reseau_groupe(r, d.RHO_CP * 0.5 * 5.0, 20.0, 0.0, -5.0)                  # débit variable : qeff = 0,5 m³/h, Δθ = 5 K
    assert e.qeff == pytest.approx(0.5) and e.d_theta == pytest.approx(5.0) and e.theta_ret == pytest.approx(30.0)
    assert e.phi_vc == pytest.approx(0.6 * 60 * (32.5 - 20.0)) and e.qsys == pytest.approx(d.RHO_CP * 2.5 + e.phi_vc)
    assert e.waux == pytest.approx(50.0 * 0.5 ** (2.0 / 3.0))
    assert d.reseau_groupe(_reseau(idtype=0), 1000.0, 20.0, 0.0, -5.0).qsys == 1000.0


def test_debit_constant_intermittent_module_les_pertes():
    r = _reseau(iddebit=2, idgest=1, idcirc=1)
    e = d.reseau_groupe(r, 0.25 * d.RHO_CP * 1.0 * 5.0, 20.0, 0.0, -5.0)
    assert e.modpertes == pytest.approx(0.25) and e.waux == pytest.approx(12.5) and e.d_theta == 5.0


def test_intergroupe_retour_pondere_et_pertes():
    dp = d.ReseauInter(d.CHAUD, 1, 1, 100.0, 0.0, 0.25, 0.0, 300.0, 1)
    a = d.EtatReseau(fonct=1, qeff=1.0, theta_dep=60.0, theta_ret=40.0, modpertes=1.0, qsys=1000.0)
    b = d.EtatReseau(fonct=1, qeff=3.0, theta_dep=50.0, theta_ret=45.0, modpertes=0.5, qsys=3000.0)
    e = d.reseau_intergroupe(dp, [a, b], 4.0, 0.0, 0.0)
    assert e.theta_dep == 60.0 and e.theta_ret == pytest.approx((40.0 + 135.0) / 4.0)
    assert e.phi_vc == pytest.approx(0.25 * 100 * (0.5 * (60 + e.theta_ret) - 20.0)) and e.qsys == pytest.approx(4000.0 + e.phi_vc)
    assert e.waux == 300.0
    arret = d.reseau_intergroupe(dp, [d.EtatReseau()], 4.0, 0.0, 0.0)
    assert arret.theta_dep == 20.0 and arret.qsys == 0.0 and arret.waux == 0.0
