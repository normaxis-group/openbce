# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import reseau_fourniture as rf
from openbce.generateurs import CH, COL, ECS


class N:
    nom = "Source_Ballon_Base_Reseau_Fourniture"

    def __init__(self, **kw):
        self.valeurs = {"Rdim": "1", "Id_Fou_Gen": "4", "P_Ess": "690", "Reseau_Chaleur": "0", "Isolation_Du_Reseau": "1"}
        self.valeurs.update(kw)

    def texte(self, k, d=""): return self.valeurs.get(k, d)
    def nombre(self, k, d=0.0): return float(self.valeurs.get(k, d) or d)
    def entier(self, k, d=0): return int(float(self.valeurs.get(k, d) or d))


def test_lecture_tableaux_248_249():
    r = rf.ReseauFourniture.depuis(N())
    assert r.bss == 3.5 and r.theta_prs == 105.0 and r.dss == 0.6 and not r.froid
    assert rf.ReseauFourniture.depuis(N(Reseau_Chaleur="1", Isolation_Du_Reseau="4")).bss == 4.3


def test_fourniture_bornee_et_pertes_de_sous_station():
    r = rf.ReseauFourniture.depuis(N())
    x = r.appeler(0.0, 1e9, 55.0, 45.0, 20.0, False)
    assert x.qfou == pytest.approx(690_000.0) and x.qrest == pytest.approx(1e9 - 690_000.0)        # (1469), (1470)
    hss = 3.5 * 0.69 ** (1 / 3)                                                                          # (1474)
    theta_ss = 0.6 * 105.0 + 0.4 * 45.0                                                                  # (1476)
    assert x.qcons - x.qfou == pytest.approx(hss * (theta_ss - 20.0))                                    # (1472), (1477)
    assert x.qcef[CH, COL[60]] == pytest.approx(x.qcons) and x.waux == 0.0


def test_ecs_seule_pertes_entieres_puis_partage():
    r = rf.ReseauFourniture.depuis(N())
    seule = r.appeler(10_000.0, 0.0, 55.0, 45.0, 20.0, True)
    hss = 3.5 * 0.69 ** (1 / 3)
    assert seule.qcef[ECS, COL[60]] == pytest.approx(10_000.0 + hss * (0.6 * 105.0 + 0.4 * 55.0 - 20.0))   # (1483) ECS seule
    assert seule.qcef[CH, COL[60]] == 0.0
    mixte = r.appeler(10_000.0, 1e9, 55.0, 45.0, 20.0, False)
    assert mixte.qcef[ECS, COL[60]] < seule.qcef[ECS, COL[60]]                                           # pertes ECS au prorata du temps


def test_reseau_de_froid_sans_pertes():
    r = rf.ReseauFourniture.depuis(N(Id_Fou_Gen="2"))
    x = r.appeler(0.0, 0.0, 55.0, 45.0, 20.0, False)
    assert r.froid and x.qcons == 0.0 and x.qfou == 0.0                                                  # (1484)
