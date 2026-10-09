# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np
import pytest

from openbce import thermodynamique as th


class N:
    """Nœud minimal : PAC air extérieur / air recyclé non réversible, pivot 3,54 / 3,05 kW (bureaux cas 01)."""
    nom = "Generateur_Thermodynamique_Elec_NonReversible"

    def __init__(self, **kw):
        self.valeurs = {"Sys_Thermo_Ch": "2", "Statut_Donnee": "1", "Rdim": "1",
                        "Performance": "0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 3.54 0 ;0 0 0 0 0",
                        "Pabs": "0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 3.05 0 ;0 0 0 0 0",
                        "COR": "0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 1 0 ;0 0 0 0 0",
                        "Lim_Theta": "2", "Theta_Max_Av": "32", "Theta_Min_Am": "-15", "Fonctionnement_Compresseur": "1",
                        "Statut_Fonctionnement_Continu": "2", "Statut_Taux": "2", "Typo_Emetteur": "3"}
        self.valeurs.update(kw)

    def texte(self, k, d=""): return self.valeurs.get(k, d)
    def nombre(self, k, d=0.0): return float(self.valeurs.get(k, d) or d)
    def entier(self, k, d=0): return int(float(self.valeurs.get(k, d) or d))


def test_matrices_completees_depuis_le_pivot():
    pac = th.Pac.depuis(N())
    m = pac.modes[th.CH]
    assert m.cop[3, 3] == pytest.approx(3.54) and m.pabs[3, 3] == pytest.approx(3050.0)
    assert m.cop[3, 4] == pytest.approx(3.54 * 1.25) and m.cop[3, 1] == pytest.approx(3.54 * 0.5) and m.cop[3, 0] == pytest.approx(3.54 * 0.5 * 0.8)
    assert m.cop[0, 3] == pytest.approx(3.54 * 1.3) and m.pabs[4, 3] == pytest.approx(3050.0 * 0.95)
    assert pac.waux0 == pytest.approx(0.02 * 3050.0) and pac.lr_contmin == 0.4 and pac.ccp == 1.0 and th.FR not in pac.modes


def test_pleine_charge_au_pivot_et_charge_partielle():
    pac = th.Pac.depuis(N())
    pfou_pc = 3050.0 * 3.54
    r = pac.heure(th.CH, 100000.0, 7.0, 20.0)
    assert r["fourni"] == pytest.approx(pfou_pc) and r["elec"] == pytest.approx(3050.0) and r["lr"] == 1.0
    r2 = pac.heure(th.CH, 0.5 * pfou_pc, 7.0, 20.0)                   # LR = 0,5 ≥ LRcontmin : continu, pas d'irréversibilité
    assert r2["lr"] == pytest.approx(0.5) and r2["cop"] > 3.54 * 0.9
    r3 = pac.heure(th.CH, 0.1 * pfou_pc, 7.0, 20.0)                   # LR = 0,1 < LRcontmin : cyclage, COP dégradé par rapport au continu
    assert r3["cop"] < r2["cop"]
    assert r3["rejet"] < 0


def test_limite_de_source_et_auxiliaires_a_vide():
    pac = th.Pac.depuis(N(Lim_Theta="1"))
    r = pac.heure(th.CH, 5000.0, -20.0, 20.0)                          # θamont < -15 : bloquée
    assert r["fourni"] == 0.0 and r["rest"] == 5000.0 and r["elec"] == pytest.approx(pac.waux0)
    assert pac.heure(th.CH, 0.0, 7.0, 20.0, part_waux0=0.0)["elec"] == 0.0


def test_interpolation_bornee():
    pac = th.Pac.depuis(N())
    m = pac.modes[th.CH]
    assert m.pleine_charge(-30.0, 20.0) == m.pleine_charge(-15.0, 20.0)
    p7, c7 = m.pleine_charge(7.0, 20.0)
    p13, c13 = m.pleine_charge(13.5, 20.0)
    assert c7 < c13 < m.cop[3, 4]


def test_multiservice_partage_le_pas_avec_l_ecs():
    n = N(); n.nom = "Source_Ballon_Base_Thermodynamique_Elec_TripleService"
    n.valeurs.update({"Sys_Thermo_ts": "5", "Performance_Ch": n.valeurs["Performance"], "Pabs_Ch": n.valeurs["Pabs"], "COR_Ch": n.valeurs["COR"]})
    pac = th.Pac.depuis(n)
    plein = pac.heure(th.CH, 1e6, 7.0, 20.0)["fourni"]
    moitie = pac.heure(th.CH, 1e6, 7.0, 20.0, rfonct_ecs=0.5)["fourni"]
    assert moitie == pytest.approx(0.5 * plein)
    assert pac.heure(th.CH, 1e6, 7.0, 20.0, froid_demande=True)["fourni"] == 0.0


def test_part_ecs_selon_la_lecture_retenue():
    """(1294) pris à la lettre : le temps d'ECS réduit la puissance fournie, pas la puissance absorbée, donc le COP de
    chauffage baisse au prorata (lecture exacte sur cas 05) ; MULTISERVICE_PABS_REDUIT = True rend le COP invariant."""
    from openbce import rsee as _r
    import glob
    chemins = glob.glob("../brut/rsee/rsee_c.xml")
    if not chemins:
        pytest.skip("RSEE de référence absent")
    p = _r.lire(chemins[0])
    pac = th.Pac.depuis(p.entree.tous("Source_Ballon_Base_Thermodynamique_Elec_DoubleService")[0])
    sans = pac.heure(th.CH, 1000.0, 7.0, 28.0, rfonct_ecs=0.0, part_waux0=1.0)
    avec = pac.heure(th.CH, 1000.0, 7.0, 28.0, rfonct_ecs=0.5, part_waux0=0.5)
    assert avec["fourni"] == pytest.approx(1000.0)
    if th.MULTISERVICE_PABS_REDUIT:
        assert avec["cop"] == pytest.approx(sans["cop"], rel=0.15)
    else:
        assert avec["cop"] < 0.7 * sans["cop"]
