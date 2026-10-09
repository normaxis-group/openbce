# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import ascenseurs


class Cabine:
    def __init__(self, **v):
        self.v = v

    def nombre(self, cle, defaut=None):
        return self.v.get(cle, defaut)

    entier = nombre


def test_veille_par_defaut():
    # 75 + 7 paliers x 2 + 13 + 5 + 140 + 10 (2275)
    assert ascenseurs.veille_par_defaut(400, 6) == 257
    assert ascenseurs.veille_par_defaut(650, 4) == 75 + 5 * 2 + 13 + 5 + 210 + 10


def test_cabine_a_l_arret():
    # sans voyage, la cabine ne consomme que sa veille sur l'année
    c = Cabine(Q=400.0, V=1.0, H=10.0, Netage=6, TechMac=0, Cp=0.5, ScVeille=0)
    assert ascenseurs.cabine(c, 0.0, True) == pytest.approx(257 * 8760)


def test_les_voyages_ajoutent_de_l_energie():
    c = Cabine(Q=400.0, V=1.0, H=10.0, Netage=6, TechMac=0, Cp=0.5, ScVeille=0)
    e = ascenseurs.cabine(c, 28 * 1600.0, True)
    assert 257 * 8760 < e < 1.2 * 257 * 8760
