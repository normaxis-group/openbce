# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import baies, climat


def test_u_selon_l_inclinaison():
    assert baies._u(2.0, 1.0, 90) == 1.0 and baies._u(2.0, 1.0, 10) == 2.0
    assert baies._u(2.0, 1.0, 45) == pytest.approx(1.5)


def test_flux_d_une_baie_sud():
    n = 24
    m = {"te0": np.full(n, 5.0), "we0": np.full(n, 5.0), "dirN": np.full(n, 600.0), "diff": np.full(n, 100.0), "teciel": np.full(n, 5.0),
         "vent": np.full(n, 2.0), "teau": np.full(n, 10.0), "gamma": np.full(n, 30.0), "psi": np.full(n, 0.0)}
    c = climat.du_site(m, "13", 0)
    b = baies.Baie(surface=2.0, alpha=0, beta=90, u_sp=1.2, u_ap=1.0, sw_sp=(0.4, 0.05, 0.0), sw_ap=(0.05, 0.02, 0.0))
    incident = 600 * np.cos(np.radians(30)) + 50 + (300 + 100) * 0.2 * 0.5
    ouvert, ferme = baies.flux(b, c, 0.0), baies.flux(b, c, 1.0)
    assert ouvert.fs1[0] == pytest.approx(2 * 0.4 * incident) and ouvert.fs2[0] == pytest.approx(2 * 0.05 * incident)
    assert ferme.fs1[0] == pytest.approx(2 * 0.05 * incident)
    assert (ouvert.hges[0], ferme.hges[0]) == pytest.approx((2.4, 2.0))
    assert ouvert.ftvc[0] == 0                      # paroi verticale : pas de rayonnement vers la voûte céleste
