# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import generateurs as g


def test_effet_joule_identite_sous_pmax():
    ej = g.EffetJoule(pmax=2000.0)
    r = ej.appeler(1500.0, g.CH)
    assert r.qfou == r.qcons == 1500.0 and r.qrest == 0.0 and r.tau == pytest.approx(0.75) and r.eta == 1.0
    assert r.qcef[g.CH, g.COL[50]] == 1500.0 and r.qcef.sum() == 1500.0 and r.waux == 0.0 and r.phi_vc == 0.0


def test_effet_joule_reporte_au_dela_de_pmax():
    ej = g.EffetJoule(pmax=2000.0)
    r = ej.appeler(5000.0, g.ECS, rpui_dispo=0.5)
    assert r.qfou == 1000.0 and r.qrest == 4000.0 and r.tau == 1.0 and r.rfonct_ecs == 1.0
    assert r.qcef[g.ECS, g.COL[50]] == 1000.0


def test_effet_joule_depuis_rsee_kw_et_rdim():
    class N:
        def entier(self, k, d=0): return {"Rdim": 3, "Id_Fou_Gen": 1}.get(k, d)
        def nombre(self, k, d=0.0): return {"Pmax": 1.5}.get(k, d)
    ej = g.EffetJoule.depuis(N())
    assert ej.pmax == 4500.0 and ej.rdim == 3
