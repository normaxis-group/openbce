# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import calendrier, parkings


class Parking:
    def __init__(self, **v):
        self.v = v

    def nombre(self, cle, defaut=None):
        return self.v.get(cle, defaut)

    entier = texte = nombre


CAL = calendrier.construire()


def test_parking_interieur_d_habitation_en_marche_forcee():
    p = Parking(Type_Parking=0, Type_Usage=2, Npl=10.0, IsParamEclPuisDefaut=1, IsParamEclHdDefaut=1, Ex=1)
    assert parkings.eclairage(p, CAL).sum() == pytest.approx(75 * 10 * 8760)


def test_detection_de_presence():
    p = Parking(Type_Parking=0, Type_Usage=2, Npl=10.0, IsParamEclPuisDefaut=0, Pec_ins=0.5, IsParamEclHdDefaut=0, PlagDse="0 24", PlagDwe="0 24", Ex=1)
    assert parkings.eclairage(p, CAL).sum() == pytest.approx(500 * 0.2 * 8760)
    # une plage de 20 h à 6 h couvre 10 heures par jour
    p.v.update(PlagDse="20 6", PlagDwe="20 6")
    assert parkings.eclairage(p, CAL).sum() == pytest.approx(500 * (14 + 10 * 0.2) * 365)


def test_parking_exterieur():
    p = Parking(Type_Parking=1, Type_Usage=2, Npl=15.0, IsParamEclPuisDefaut=1, IsParamEclHdDefaut=1, Ex=1, Vent=1)
    assert parkings.eclairage(p, CAL).sum() == pytest.approx(8 * 15 * parkings.FH_EXT.sum() * 365)
    assert parkings.ventilation(p, CAL).sum() == 0


def test_ventilation_d_habitation():
    p = Parking(Type_Parking=0, Type_Usage=2, Npl=20.0, Vent=1, IsParamVentilationHabDefaut=0, Pvent600=150.0, Reg=1)
    assert parkings.ventilation(p, CAL).sum() == pytest.approx(150 * 20 * parkings.RMVTPL[2].sum() * 365)
    p.v["Reg"] = 0
    assert parkings.ventilation(p, CAL).sum() == pytest.approx(150 * 20 * 8760)
    assert np.isclose(parkings.RMVTPL[2].sum(), 1.995)
