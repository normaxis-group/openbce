# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import chaudiere as c
from openbce.generateurs import CH, COL, ECS


class N:
    nom = "Generateur_Combustion"

    def __init__(self, **kw):
        self.valeurs = {"Rdim": "1", "Generateur": "0", "Ventilation": "1", "Evac_Fumee": "0", "Combustible_Gaz": "0", "Id_Fou_Gen_1": "4",
                        "Valeur_Mesuree_Defaut_Theta_Min": "1", "Theta_Fonc_Min": "20", "Pn_gen": "26", "Valeur_Certifiee_Defaut_R_pn": "3", "R_pn": "98.16",
                        "Pint": "6.26", "Valeur_Certifiee_Defaut_R_Pint": "3", "R_Pint": "110.28", "Valeur_Mesuree_Defaut_Q_po_30": "1", "Q_po_30": "35",
                        "Q_veille": "3.6", "Valeur_Mesuree_Defaut_Q_aux_nom": "1", "Q_aux_nom": "40.8"}
        self.valeurs.update(kw)

    def texte(self, k, d=""): return self.valeurs.get(k, d)
    def nombre(self, k, d=0.0): return float(self.valeurs.get(k, d) or d)
    def entier(self, k, d=0): return int(float(self.valeurs.get(k, d) or d))


def test_lecture_condensation_gaz():
    ch = c.Chaudiere.depuis(N(), pos_gen=1)
    assert ch.famille == "condensation" and ch.energie == 10 and ch.pcsi == 1.11 and ch.idpertes_parois == 2
    assert ch.r_pn == pytest.approx(0.9816 / 1.11) and ch.r_pint == pytest.approx(1.1028 / 1.11) and ch.theta_min == 20.0


def test_pleine_charge_chauffage_sur_pci_pcs():
    ch = c.Chaudiere.depuis(N(), pos_gen=1)
    r = ch.appeler(0.0, 1e6, 54.0, 70.0, 20.0, False)
    assert r.qfou == pytest.approx(26000.0)                                      # Pth,nom à θ de référence 70 °C
    assert r.qcons == pytest.approx(26000.0 / 0.9816)                            # (1099) : au total Qfou / R_PCI
    assert r.waux == pytest.approx(40.8) and r.qcef[CH, COL[10]] == pytest.approx(r.qcons) and r.qcef[CH, COL[50]] == pytest.approx(40.8)
    assert r.qrest == pytest.approx(1e6 - 26000.0)


def test_condensation_meilleure_a_basse_temperature_et_charge_partielle():
    ch = c.Chaudiere.depuis(N(), pos_gen=1)
    haut = ch.appeler(0.0, 5000.0, 54.0, 70.0, 20.0, False)
    bas = c.Chaudiere.depuis(N(), pos_gen=1).appeler(0.0, 5000.0, 54.0, 35.0, 20.0, False)
    assert bas.qcons < haut.qcons                                                 # (1079) : αth = 0,2 %/K en condensation
    assert bas.eta > haut.eta


def test_ecs_puis_chauffage_sur_le_meme_pas():
    ch = c.Chaudiere.depuis(N(), pos_gen=1)
    r = ch.appeler(13000.0, 1e6, 54.0, 70.0, 20.0, False)
    assert 0 < r.rfonct_ecs < 1 and r.qfou == pytest.approx(13000.0 + (1 - r.rfonct_ecs) * 26000.0, rel=1e-3)
    assert r.qcef[ECS, COL[10]] > 0 and r.qcef[CH, COL[10]] > 0


def test_arret_pertes_et_veille():
    ch = c.Chaudiere.depuis(N(), pos_gen=1)
    ch.appeler(0.0, 5000.0, 54.0, 70.0, 20.0, False)                              # dernier fonctionnement : chauffage à 70 °C
    r = ch.appeler(0.0, 0.0, 54.0, 70.0, 20.0, False)
    assert r.qfou == 0.0 and r.qcons == pytest.approx(35.0 * (50.0 / 30.0) ** 1.25) and r.waux == pytest.approx(3.6)   # (1106), (1110)
    assert r.phi_vc == pytest.approx(0.75 * r.qcons + 3.6)                       # (1119) à l'arrêt, ventilateur de combustion
