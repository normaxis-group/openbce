# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import bilans


def test_forfait_froid():
    # P8813 Groupe-T : logement collectif H3 (dép. 13), DH 1160, DH_max 1250 : 0,011 x (1160 - 350) x 1,2 / 2,3 = 4,65 (RSEE : 4,6)
    assert bilans.forfait_froid(2, False, 1160.0, 1250.0, "H3", 0.0) == pytest.approx(4.65, abs=0.01)
    assert bilans.forfait_froid(2, True, 1160.0, 1250.0, "H3", 0.0) == 0.0
    assert bilans.forfait_froid(2, False, 300.0, 1250.0, "H3", 0.0) == 0.0
    assert bilans.forfait_froid(2, False, 2000.0, 1250.0, "H1a", 500.0) == pytest.approx(0.011 * 900 * 0.6 / 2.3)


def test_cep():
    assert bilans.cep({"elec": 10.0, "gaz": 5.0, "bois": 2.0}) == pytest.approx(30.0)
    assert bilans.cep_nr({("elec", "ch"): 10.0, ("bois", "ch"): 2.0, ("reseau", "ch"): 4.0}, rat_enr_reseau=0.5) == pytest.approx(25.0)
