# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np

from openbce import photovoltaique as pv


def test_perte_optique_par_reflexion():
    assert pv.fopt(0.0) == 1.0
    assert 0.9 < pv.fopt(60.0) < 1.0
    assert np.isclose(pv.fopt(89.0), pv.fopt(87.0))                      # plafonné à 87°


def test_valeurs_de_calcul_selon_le_statut():
    assert pv.parametres_capteur(0, "certifiee", 400.0, 0.004, 45.0) == (400.0, 0.004, 45.0)
    assert np.allclose(pv.parametres_capteur(0, "justifiee", 400.0, 0.004, 45.0), (360.0, 0.0044, 49.5))
    assert np.allclose(pv.parametres_capteur(0, "declaree", 400.0, 0.003, 30.0), (320.0, 0.00425, 40.0))   # planchers μ_util_min, NOCT_util_min
    assert np.allclose(pv.parametres_capteur(2, "defaut", 400.0, 0.0, 0.0), (320.0, 1.2 * 0.00208, 48.0))


def test_onduleur_courbe_par_defaut_et_extinction():
    ppv = np.array([0.0, 100.0, 200.0, 1000.0, 1100.0, 1200.0])
    pond = pv.onduleur(ppv, 1000.0)
    assert pond[0] == 0.0 and np.isclose(pond[1], 100.0 * 0.45) and np.isclose(pond[2], 180.0)   # 0 à vide, 0,9 dès 20 %
    assert np.isclose(pond[3], 900.0) and np.isclose(pond[4], 990.0) and pond[5] == 0.0          # extinction au-delà de 115 %
    assert np.isclose(pv.onduleur(np.array([500.0]), 1000.0, rendement=0.95)[0], 475.0)
    assert pv.onduleur(np.array([500.0]), 0.0)[0] == 0.0
