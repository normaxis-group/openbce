# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
from openbce import saisons as s


def automate():
    return s.Saisons(heures_occupation_reference=128, surface=100.0)


def test_chauffage_autorise_les_huit_premieres_semaines_puis_arret_sur_besoins_faibles():
    a = automate()
    for jour in range(1, 70):
        for _ in range(24):
            a.heure(True, 20.0, 19.0, 26.0, 0.0, 0.0)      # aucun besoin
        a.nouveau_jour(jour)
        assert a.chauffage == (jour < 56)
    assert a.saison == s.MI_SAISON


def test_refroidissement_demarre_sur_inconfort_puis_est_impose_en_ete():
    a = automate()
    for jour in range(1, 30):
        for _ in range(24):
            a.heure(True, 29.0, 19.0, 26.0, 0.0, 500.0)    # 3 °C d'inconfort chaud à chaque heure
        a.nouveau_jour(jour)
    assert a.refroidissement                                # 24 h x 3 °C x 0,5 = 36 °C.h par jour : seuil franchi le deuxième jour compté
    b = automate()
    for jour in range(1, 190):
        b.nouveau_jour(jour)
    assert b.refroidissement and not b.chauffage and b.saison == s.REFROIDISSEMENT


def test_seuil_d_inconfort_chaud():
    assert s.seuil_inconfort_chaud(26, 10) == 26
    assert s.seuil_inconfort_chaud(26, 25) == 0.33 * 25 + 20.8
