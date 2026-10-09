# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import ecs_distribution as d


def _reseau(**kw):
    base = dict(type_reseau=1, u=0.25, l_vc=400.0, l_hvc=150.0, rechauffeur=False, gestion_circ=1, p_circ=150.0, b_et=1.0)
    base.update(kw)
    return d.Intergroupe(**base)


def test_boucle_pertes_et_circulateur():
    """Bouclé sans réchauffeur : pertes à θmoy = θdépart - 2,5 ajoutées à la demande (1745, 1753), circulateur en auxiliaire."""
    r = _reseau().heure(np.array([1000.0, 0.0]), np.array([10.0, 20.0]))
    attendu_h0 = 0.25 * 400 * (50.5 - 20) + 0.25 * 150 * (50.5 - 10)
    assert r["pertes"][0] == pytest.approx(attendu_h0)
    assert r["qw_prim"][0] == pytest.approx(1000.0 + attendu_h0) and r["qw_prim"][1] == pytest.approx(r["pertes"][1])
    assert r["elec_ecs"].sum() == 0.0 and r["circulateur"].tolist() == [150.0, 150.0]


def test_boucle_avec_rechauffeur():
    """Réchauffeur : les pertes passent en électricité ECS et la demande n'est pas majorée (1747, 1753)."""
    r = _reseau(rechauffeur=True).heure(np.array([1000.0]), np.array([10.0]))
    assert r["qw_prim"][0] == 1000.0 and r["elec_ecs"][0] == pytest.approx(r["pertes"][0]) and r["pertes"][0] > 0


def test_trace_et_sans_reseau():
    """Tracé : pertes à θdépart en électricité (traceur), pas de circulateur (1757, 1759) ; type 0 : identité."""
    r = _reseau(type_reseau=2).heure(np.array([1000.0]), np.array([10.0]))
    assert r["qw_prim"][0] == 1000.0 and r["elec_ecs"][0] == pytest.approx(0.25 * 400 * 33 + 0.25 * 150 * 43) and r["circulateur"][0] == 0.0
    r0 = _reseau(type_reseau=0).heure(np.array([1000.0]), np.array([10.0]))
    assert r0["qw_prim"][0] == 1000.0 and r0["pertes"][0] == 0.0


def test_espace_tampon_reduit_les_pertes_hvc():
    chaud = _reseau(b_et=0.5).heure(np.array([0.0]), np.array([0.0]))["pertes"][0]
    froid = _reseau(b_et=1.0).heure(np.array([0.0]), np.array([0.0]))["pertes"][0]
    assert chaud < froid
