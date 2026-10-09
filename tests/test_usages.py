# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
from openbce import usages


def test_les_28_usages_ont_un_nom():
    assert sorted(usages.NOMS) == list(range(1, 29))
    assert usages.nom(3) == "Bureaux" and usages.nom(99).endswith("inconnu")


def test_usages_non_valides_et_avertissement():
    assert usages.non_valides([2, 3, 2]) == []
    assert usages.non_valides([3, 17, 4, 17]) == [4, 17]
    assert usages.avertissement([1, 2]) is None
    a = usages.avertissement([2, 17])
    assert a.startswith("Usages non validés : 17 (Commerces)") and "annexe III" in a
