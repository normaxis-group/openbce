# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import brasseurs, thermique, ventilation
from openbce.rsee import Noeud


def noeud(nom, **valeurs):
    n = Noeud(nom)
    n.valeurs.update({k: str(v) for k, v in valeurs.items()})
    return n


def test_debit_bouche_logement():
    b = noeud("Bouche_Conduit", Qv_rep_pointe=300, Qv_rep_base=100, Type_Regul_Res=1, Cdep=0)
    q = ventilation._debit_bouche(b, 2, "rep", np.ones(3))
    assert q[0] == pytest.approx(1.30 * (300 * 7 + 100 * 161) / 168)        # (414), (423), tableau 59 : Type_Regul_Res 1 = temporisation, 7 h


def test_debit_bouche_tertiaire():
    b = noeud("Bouche_Conduit", Qv_rep_occ=400, Qv_rep_inocc=40, Cdep=2, Cdep_Value=1.05, Cndbnr_Value=0.8)
    q = ventilation._debit_bouche(b, 3, "rep", np.array([1.0, 0.0]))
    assert q.tolist() == pytest.approx([1.05 * 0.8 * 400, 1.05 * 40])


def test_inertie_lente_sans_ecart_de_surface():
    g = thermique.Groupe(100.0, 10.0, 3.0, 260.0)
    lente = thermique.InertieLente(g, 3.0, 500.0, 3.0, 500.0)
    assert lente.dh_sq == 0 and lente.avancer(20.0) == 0.0                   # (329) : ΔR nul, ΔH nul


def test_inertie_lente_converge():
    g = thermique.Groupe(100.0, 10.0, 3.5, 370.0)
    lente = thermique.InertieLente(g, 3.0, 500.0, 3.0, 500.0)
    for _ in range(24 * 30):
        flux = lente.avancer(22.0)
    assert abs(flux) < 1e-6 and lente.ms == pytest.approx(22.0, abs=1e-6)


def test_brasseur_delta_theta_op():
    t = [brasseurs.TypeBrasseur(nombre=2, rat_surf=0.3, usage=2, q_max_corr=10000.0)]
    # au-dessus de V2 : plein débit, vitesse 0,0032 x 20000 / (300 x 0,3) = 0,71 m/s, correction positive
    d = brasseurs.delta_theta_op(t, 2, True, True, 15, 32.0, 26.0, 0.0, 28.0, 28.0, 300.0)
    assert d > 0.5 and t[0].debit == 10000.0
    # inoccupation : arrêt
    assert brasseurs.delta_theta_op(t, 2, False, True, 15, 32.0, 26.0, 0.0, 28.0, 28.0, 300.0) == 0.0 and t[0].debit == 0.0
