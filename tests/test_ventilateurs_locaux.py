# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Ventilateurs locaux des émetteurs à recyclage d'air (fiche 8.1, 811 à 813)."""
from openbce import emission
from openbce.rsee import Noeud


def _vcv(gest, spv=False):
    return emission.VentilateurLocal(gest, spv, 270.0, 180.0, 90.0, 30.0, True, True, 1.0, 1.0)


def test_arret_sans_besoin_en_gestion_3():
    v = _vcv(3)
    assert v.heure(0.0, 0.0, 100.0, True, True, False, True, True) == 0.0
    assert v.heure(500.0, 0.0, 100.0, True, True, False, True, True) == 90.0        # besoin faible : petite vitesse
    assert v.heure(5000.0, 0.0, 100.0, True, True, False, True, True) == 180.0      # 50 Wh/m² > 20 : moyenne vitesse
    assert v.heure(0.0, 5000.0, 100.0, True, True, True, True, True) == 270.0       # relance : grande vitesse


def test_hors_saison_rien():
    v = _vcv(3)
    assert v.heure(5000.0, 0.0, 100.0, True, True, False, False, False) == 0.0


def test_marche_permanente_gestion_2_et_manuelle():
    v2 = _vcv(2, spv=True)
    assert v2.heure(0.0, 0.0, 100.0, True, True, False, True, True) == 30.0         # super petite vitesse sans besoin
    v1 = _vcv(1)
    assert v1.heure(5000.0, 0.0, 100.0, True, False, False, True, True) == 180.0    # premier pas d'occupation : régime choisi
    assert v1.heure(0.0, 0.0, 100.0, True, True, False, True, True) == 180.0        # puis conservé
    assert v1.heure(0.0, 0.0, 100.0, False, True, False, True, True) == 180.0       # marche permanente, même inoccupé


def test_lecture_des_emetteurs():
    e1 = Noeud("Emetteur", {"Is_emetteur_chaud": "1", "Is_emetteur_froid": "1", "Rat_s_ch": "0.6", "Rat_s_fr": "0.6", "Gest_vcv": "3", "P_VCV_gv": "270", "P_VCV_mv": "180", "P_VCV_pv": "90"}, [])
    e2 = Noeud("Emetteur", {"Is_emetteur_chaud": "1", "Rat_s_ch": "0.4", "Gest_vcv": "0"}, [])
    vs = emission.ventilateurs_locaux(Noeud("Groupe", {}, [e1, e2]))
    assert len(vs) == 1 and abs(vs[0].w_ch - 0.6) < 1e-9 and abs(vs[0].w_fr - 1.0) < 1e-9
