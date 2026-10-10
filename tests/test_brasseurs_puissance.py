# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Électricité des brasseurs d'air (fiche 8.32, 1662 à 1665)."""
from openbce import brasseurs


def test_puissance_selon_le_debit():
    t = brasseurs.TypeBrasseur(nombre=10, rat_surf=0.5, usage=2, q_max_corr=8000.0, p_max_corr=48.0)
    assert brasseurs.puissance([t]) == 0.0                              # à l'arrêt
    t.debit = t.q_int
    assert abs(brasseurs.puissance([t]) - 10 * 0.6 * 48.0) < 1e-9        # débit intermédiaire : 60 % de la puissance corrigée
    t.debit = t.q_max_corr
    assert abs(brasseurs.puissance([t]) - 10 * 48.0) < 1e-9              # débit maximal


def test_puissance_corrigee_selon_le_statut():
    """1,2 fois la puissance déclarée, 1,1 fois la puissance justifiée (p. 992)."""
    from openbce.rsee import Noeud
    decl = Noeud("Brasseur_Air", {"Nb": "4", "Rat_surf": "0.5", "Us": "1", "Type_Qv_air_max": "0", "Qv_air_max": "10000", "Type_P_elec_max": "0", "P_elec_max": "40"}, [])
    just = Noeud("Brasseur_Air", {"Nb": "4", "Rat_surf": "0.5", "Us": "1", "Type_Qv_air_max": "1", "Qv_air_max": "10000", "Type_P_elec_max": "1", "P_elec_max": "40"}, [])
    g = Noeud("Groupe", {}, [decl, just])
    types = brasseurs.lire(g, 2, 100.0)
    assert abs(types[0].p_max_corr - 48.0) < 1e-9 and abs(types[1].p_max_corr - 44.0) < 1e-9
