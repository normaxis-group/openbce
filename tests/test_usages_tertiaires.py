# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Les 28 usages traversent le moteur : tables complètes, scénarios et locaux résolus, exigences calculables.
Usages 4 à 28 non validés (aucun récapitulatif de référence) : ces tests vérifient la cohérence, pas l'exactitude."""
import numpy as np

from openbce import ascenseurs, calendrier, ecs, eclairage, exigences, groupe, ouverture, scenarios, usages


def test_tables_couvrent_les_usages_non_residentiels():
    for u in range(3, 29):
        assert u in groupe.DEBIT_CONVENTIONNEL and u in groupe.DEBIT_INOCCUPATION
        assert groupe.DEBIT_INOCCUPATION[u][0] == 60.0
        assert u in ecs.A_TERTIAIRE and u in ecs.RAT_DOUCHES_BAINS and u in ascenseurs.BV
    for u in range(1, 29):
        assert u in exigences.BBIO_MAX_MOYEN and u in exigences.MBGEO and u in exigences.CEP_MAX_MOYEN and u in exigences.MCGEO
        assert len(exigences.MBGEO[u]) == 3 and all(len(l) == 8 for l in exigences.MBGEO[u])


def test_locaux_d_eclairage_resolus_pour_les_26_usages_non_residentiels():
    for u in range(3, 29):
        types = eclairage._locaux_usage(u)
        assert len(types) == len(scenarios._locaux(u))
        assert all(len(c1) == 4 and 50 <= eiref <= 500 for _, c1, eiref in types)
    assert eclairage._locaux_usage(3)[1] == ("Salle de réunion", (0.70, 0.65, 0.60, 0.50), 500.0)


def test_scenarios_des_28_usages():
    cal = calendrier.construire()
    for u in range(3, 29):
        sc = scenarios.tertiaire(cal, u, 1000.0)
        assert sc.nbh_occ_ref > 0
        assert set(np.unique(sc.etat_ch)) <= {-1.0, 0.0, 1.0} and set(np.unique(sc.etat_fr)) <= {-1.0, 0.0, 1.0}
        assert np.isfinite(sc.occupants).all() and sc.apports_occupants.max() > 0
    assert scenarios.tertiaire(cal, 11, 1000.0).apports_usages.max() > 0          # cellule vide du tableur, valeur du texte
    assert scenarios.tertiaire(cal, 23, 1000.0).consigne_ch.max() == 15.0


def test_exigences_des_28_usages():
    for u in range(1, 29):
        m = exigences.bbio_max(u, "H2d", 100.0, 1000.0, 10, 1000.0)
        assert m["bbio_max"] > 0
        c = exigences.cep_max(u, "H1a", 50.0, 1000.0, 10, 1000.0)
        assert c["cep_nr_max"] > 0 and c["cep_max"] >= c["cep_nr_max"]
        for cat in (1, 2, 3):
            d = exigences.dh_max(u, "H3", cat, True, 60.0)
            assert d is None or d > 0
    assert exigences.dh_max(3, "H3", 3) is None and exigences.dh_max(4, "H3", 3) == 2200.0
    assert exigences.mbbruit(3, "H1a", 1, 3) == 0.4 and exigences.mbbruit(6, "H3", 3, 3) == 0.15
    assert exigences.mbsurf_tot(17, 300.0) == (47.5 - 0.095 * 300) / 170.0 and exigences.mbsurf_tot(17, 600.0) == 0.0
    assert exigences.mcsurf_tot(24, 1000.0, 2026, True) == (365 - 73) / 94.0


def test_indicateurs_d_usage():
    assert usages.IHEBERGEMENT == {1, 2, 8, 9, 19, 20} and usages.IENSEIGNEMENT == {4, 5, 7, 26, 27}
    assert ouverture.TRAVERSANT_SURV[17] == 1 and 3 not in ouverture.TRAVERSANT_SURV
    assert usages.surface_reference(2) == "SHAB" and usages.surface_reference(17) == "SU"
