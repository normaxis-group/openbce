# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Le modèle thermique du groupe doit conserver l'énergie : en régime permanent, ce qui entre égale ce qui sort."""
import pytest

from openbce.thermique import Groupe, Sollicitations, hgemq, pas

G = Groupe(surface=76, a_baies=17.9, amq_surf=3.0, cmq_surf=260)


def permanent(x, **sys):
    t = 18.0
    for _ in range(4000):
        r = pas(G, x, t, **sys)
        t = r.mq
    return r


def test_evolution_libre_rejoint_l_exterieur():
    x = Sollicitations(hgei=30, theta_ei=10, h_opaque=60, hges=25, theta_es=10, theta_em=10, phi_i=0, phi_l=0, phi_mq=0)
    r = permanent(x)
    assert (r.i, r.s, r.mq) == pytest.approx((10, 10, 10), abs=1e-6)


# une émission radiative n'atteint que les parois (372) : la part qui vise les baies, Abaies / Atparois, n'est pas injectée
@pytest.mark.parametrize("sys, recu", [({"sys_conv": 2000}, 2000), ({"sys_rad": 2000}, 2000 * (G.frs + G.frm))])
def test_bilan_en_regime_permanent(sys, recu):
    x = Sollicitations(hgei=30, theta_ei=2, h_opaque=60, hges=25, theta_es=5, theta_em=3, phi_i=150, phi_l=0, phi_mq=80)
    r = permanent(x, **sys)
    pertes = 30 * (r.i - 2) + 25 * (r.s - 5) + hgemq(G, 60) * (r.mq - 3)
    assert pertes == pytest.approx(recu + 150 + 80, rel=1e-6)
