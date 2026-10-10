# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Réseau intergroupe mixte à modules thermiques d'appartement (fiche 16.8, configuration directe)."""
import math

from openbce import mta
from openbce.distribution import EtatReseau


def _module(**kw):
    base = dict(id_gen=1, nb_mod=10, maintien_ecs=1, simultanee=0, en_volume_chauffe=0, idcirc=2, a=0.0, b=0.0683, c=587.65, theta_in_nom=75.0,
                q_maintien=0.0, theta_out_maintien=0.0, h_ech_ecs=mta.S_ECH / mta.R_SI, h_ecs=0.0, h_mixte=0.2 * 0.98, h_ch=0.2 * 0.71,
                h_module=mta.S_MODULE / (2 * mta.R_SI + 0.625), paux_fct=1.0, paux_arret=0.0, q_nom=7.0, q_resid=0.0, delta_maintien=1.0,
                lvc=100.0, lhvc=50.0, lvc_gaines=100.0, lhvc_gaines=0.0, u_vc=0.6, u_hvc=0.25, u_vc_gaines=0.4, u_hvc_gaines=0.0, paux_prim=300.0)
    base.update(kw)
    return mta.ModulesMixtes(**base)


def test_dtlm_resolue_sur_la_definition():
    """ΔTs vérifie (ΔTe − ΔTs) / ln(ΔTe / ΔTs) = P / UA (2625) ; un échangeur trop petit sort à ΔTe."""
    d_te, p, ua = 22.0, 35900.0, 3040.0
    d_ts = mta.dtlm_sortie(p, ua, d_te)
    assert 0 < d_ts < d_te
    assert abs((d_te - d_ts) / math.log(d_te / d_ts) - p / ua) < 1e-2
    assert mta.dtlm_sortie(p, 10.0, d_te) == d_te


def test_heure_sans_demande_ni_debit():
    """Sans puisage, sans chauffage et sans débit de maintien : rien à fournir, pas de pertes du primaire (réseau hors fonction)."""
    r = _module().heure(0.0, 53.0, 10.0, [EtatReseau(), EtatReseau()], 5.0)
    assert r["qsys"] == 0.0 and r["pertes"] == 0.0 and r["q_moyen"] == 0.0 and r["waux"] == 0.0
    assert r["chauffage"] is False
    assert r["temps"] == (0.0, 0.0, 0.0, 1.0)


def test_heure_de_puisage():
    """Un puisage : l'énergie primaire vaut le besoin, le retour est froid (ΔTs + θcw), le primaire perd à sa température moyenne."""
    m = _module()
    r = m.heure(6000.0, 53.0, 10.0, [EtatReseau()], 5.0)
    assert abs(r["q_ecs"] - 6000.0) < 1e-6 and r["chauffage"] is False
    assert 10.0 < r["theta_out"] < 30.0
    theta_moy = 0.5 * (75.0 + r["theta_out"])
    assert abs(r["theta_aval"] - theta_moy) < 1e-9
    attendu_vc = (0.6 * 100 + 0.4 * 100) * (theta_moy - 20.0)
    attendu_hvc = 0.25 * 50 * (theta_moy - 5.0)
    assert abs(r["pertes_primaire"] - attendu_vc - attendu_hvc) < 1e-6
    assert r["pertes_modules"] > 0 and r["qsys"] > 6000.0
    assert r["waux"] > 0                                              # circulateur à vitesse variable et cartes des modules


def test_heure_de_chauffage_direct():
    """Chauffage direct : la demande des réseaux de groupe passe au primaire, débit primaire réduit par l'écart 75 − retour."""
    m = _module(simultanee=0)
    e = EtatReseau(fonct=1, qeff=0.8, d_theta=10.0, theta_dep=50.0, theta_ret=40.0, modpertes=0.8, qsys=9000.0)
    r = m.heure(0.0, 53.0, 10.0, [e, e], 0.0)
    assert r["chauffage"] is True and abs(r["q_ch"] - 18000.0) < 1e-6
    attendu_q = 2 * 0.8 * (50.0 - 40.0) / (75.0 - 40.0)                  # (2642)
    assert abs(r["q_moyen"] - attendu_q * 0.8) < 1e-6                      # temps de chauffage seul = modulation moyenne (2664)
    assert abs(r["theta_out"] - 40.0) < 1e-9
    assert r["temps"] == (0.0, 0.0, 0.8, 0.2 - 0.0) or abs(r["temps"][3] - 0.2) < 1e-9


def test_maintien_sans_debit_ne_coute_rien():
    """Maintien demandé mais débit de maintien nul : ni énergie de maintien ni pertes statiques."""
    sans = _module(maintien_ecs=1, q_maintien=0.0).heure(0.0, 53.0, 10.0, [], 5.0)
    avec = _module(maintien_ecs=1, q_maintien=0.05, theta_out_maintien=70.0).heure(0.0, 53.0, 10.0, [], 5.0)
    assert sans["qsys"] == 0.0
    assert avec["q_statique"] > 0 and avec["pertes_modules"] > 0 and avec["q_moyen"] == 0.05 * 10


def test_recuperation_en_volume_chauffe():
    """En volume chauffé, la moitié des pertes des modules et des cartes est récupérable ; hors volume, rien."""
    hors = _module(en_volume_chauffe=0).heure(6000.0, 53.0, 10.0, [], 5.0)
    dans = _module(en_volume_chauffe=1).heure(6000.0, 53.0, 10.0, [], 5.0)
    assert hors["phi_recup"] == 0.0
    assert abs(dans["phi_recup"] - 0.5 * (dans["pertes_modules"] + 10 * 1.0 * dans["temps"][1])) < 1e-6
