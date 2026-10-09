# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import generateurs_ballon as gb


def _pac(**kw):
    cop = np.full((7, 6), 4.0)
    pabs = np.full((7, 6), 150.0)
    base = dict(cop=cop, pabs=pabs, amont=gb.TECHNO[2]["amont"], sys=2, rdim=1, waux0=3.0, lim=0, t_max_aval=90.0, t_min_amont=-99.0)
    base.update(kw)
    return gb.PacEcs(**base)


def test_puissance_variable_rejoint_la_pleine_charge():
    """Fonc_compr 1 : à LR = 1, Pabs = Pabs_pc ; à LR = LRcontmin, le COP net est majoré de CcpLRcontmin (1308, 1309)."""
    pac = _pac(lr_contmin=0.4, ccp=1.2)
    pfou, pabs = pac.heure(600.0, 20.0, 45.0)
    assert pfou == pytest.approx(600.0) and pabs == pytest.approx(150.0)
    pfou, pabs = pac.heure(240.0, 20.0, 45.0)                       # LR = 0,4
    cop_net_pc = 600.0 / 147.0
    ccp_net = 0.4 * 147.0 * 1.2 / (0.4 * 150.0 - 1.2 * 3.0)
    assert pabs == pytest.approx(240.0 / (cop_net_pc * ccp_net) + 3.0)


def test_puissance_variable_cycle_sous_lrcontmin():
    """Sous LRcontmin le compresseur cycle : Pabs croît avec LR et porte la pénalité d'irréversibilité (1313 à 1318)."""
    pac = _pac(lr_contmin=0.4, ccp=1.0)
    _, p_bas = pac.heure(60.0, 20.0, 45.0)
    _, p_haut = pac.heure(180.0, 20.0, 45.0)
    _, p_min = pac.heure(240.0, 20.0, 45.0)
    assert 3.0 < p_bas < p_haut < p_min == pytest.approx(0.4 * 150.0)   # (1308) : à LR = LRcontmin, Pabs = LRcontmin x Pabs_pc


def test_plafond_air_extrait():
    """Machine sur air extrait : la puissance fournie est bornée par l'échange à la source (1455, 1456)."""
    pac = _pac(qm_air_extrait=50.0 / 3600 * 1.2, t_air_lim=0.0)
    pfou, _ = pac.heure(5000.0, 20.0, 45.0)
    pech = 50.0 / 3600 * 1.2 * 1006.0 * 20.0
    assert pfou == pytest.approx(pech * 600.0 / 450.0)
    assert pfou < 600.0


def test_auxiliaires_multiservice_hors_ecs_seule():
    """PAC triple service : les auxiliaires à charge nulle ne vont à l'ECS qu'en dehors des saisons (p. 796)."""
    pac = _pac(multiservice=True, waux0=12.0)
    assert pac.heure(0.0, 7.0, 45.0, ecs_seule=True) == (0.0, 12.0)
    assert pac.heure(0.0, 7.0, 45.0, ecs_seule=False) == (0.0, 0.0)
    _, p_seule = pac.heure(300.0, 7.0, 45.0, ecs_seule=True)        # LR = 0,5
    _, p_saison = pac.heure(300.0, 7.0, 45.0, ecs_seule=False)
    assert p_seule == pytest.approx(75.0 + 6.0) and p_saison == pytest.approx(75.0)


def test_temperature_amont_selon_la_source():
    """Air extrait : l'air repris remplace l'air extérieur comme température amont (1408)."""
    cop = np.full((7, 6), 1.0)
    cop[:, 3] = 5.0                                                   # colonne 20 °C
    pac = _pac(cop=cop)
    _, p_ext = pac.heure(300.0, 5.0, 45.0)
    _, p_extrait = pac.heure(300.0, 20.0, 45.0)
    assert p_extrait < p_ext
