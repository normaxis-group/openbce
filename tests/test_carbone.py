# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Ic énergie (annexe II, équations 74 et 75) et Ic énergie_max."""
from openbce import carbone


def test_coefficients_de_ponderation():
    assert len(carbone.F_CO2) == 51 and carbone.F_CO2[0] == 1.0 and carbone.F_CO2[50] == 0.578
    assert abs(carbone.SOMME_F - 39.543) < 1e-6


def test_ic_energie_par_energie_et_usage():
    r = carbone.ic_energie({("elec", "ch"): 10.0, ("elec", "ecs"): 5.0, ("elec", "ecl"): 2.0, ("gaz", "ch"): 20.0, ("reseau", "ch"): 7.0})
    attendu = (10.0 * 0.079 + 5.0 * 0.064 + 2.0 * 0.069 + 20.0 * 0.227) * carbone.SOMME_F
    assert abs(r["ic_energie"] - attendu) < 1e-9
    assert abs(r["ic_energie_annuel"] - (10.0 * 0.079 + 5.0 * 0.064 + 2.0 * 0.069 + 20.0 * 0.227)) < 1e-9
    assert r["energies_ignorees"] == ["reseau"]                      # réseau de chaleur sans DE renseignée


def test_seuil_par_usage_et_periode():
    assert carbone.ic_energie_max_moyen(2, 2023) == 560.0 and carbone.ic_energie_max_moyen(2, 2026) == 260.0 and carbone.ic_energie_max_moyen(2, 2026, reseau_chaleur=True) == 320.0
    assert carbone.ic_energie_max_moyen(1, 2023, derogation_gaz=True) == 280.0 and carbone.ic_energie_max_moyen(1, 2028) == 160.0
    assert carbone.ic_energie_max_moyen(12, 2026) is None
    assert abs(carbone.ic_energie_max(2, 0.8585, 2023) - 560.0 * 0.8585) < 1e-9
