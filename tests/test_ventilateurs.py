# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import ventilateurs


class N:
    def __init__(self, enfants=(), **v):
        self.v, self.e = v, dict(enfants)

    def nombre(self, cle, defaut=None):
        return self.v.get(cle, defaut)

    entier = nombre

    def directs(self, nom):
        return self.e.get(nom, [])


def test_repartition_entre_groupes():
    g1 = N({"Bouche_Conduit": [N(Id_Systeme_Mecanique=1, Type_Regul_Res=1, Qv_rep_pointe=300.0, Qv_rep_base=300.0)]}, Index=1)
    g2 = N({"Bouche_Conduit": [N(Id_Systeme_Mecanique=1, Type_Regul_Res=1, Qv_rep_pointe=100.0, Qv_rep_base=100.0)]}, Index=2)
    zone = N({"Groupe": [g1, g2], "Ventilation_Mecanique": [N(Index=1, Type_Ventilation_Mecanique=0, Pvent_pointe_rep=80.0, Pvent_base_rep=40.0)]}, Usage=2)
    p = ventilateurs.de_la_zone(zone)
    moyenne = (80 * 7 + 40 * 161) / 168                       # (641)
    assert p[1] == pytest.approx(0.75 * moyenne) and p[2] == pytest.approx(0.25 * moyenne)
