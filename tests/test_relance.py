# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np

from openbce import emission


def _journee(consigne_nuit, consigne_jour, debut=8, fin=18, jours=3):
    c = np.full(24 * jours, consigne_nuit, dtype=float)
    etat = np.zeros(24 * jours)
    for j in range(jours):
        c[24 * j + debut:24 * j + fin] = consigne_jour
        etat[24 * j + debut:24 * j + fin] = 1
    return c, etat


def test_relance_froid_courte_une_heure_avec_indicateur():
    # bureaux : consignes réduites courte et prolongée toutes deux à 30 °C ; sans l'indicateur, chaque nuit passait pour
    # une inoccupation prolongée (2 h de relance au lieu de 1 h, tableau 94, horloge avec contrôle d'ambiance)
    c, etat = _journee(30.0, 26.0)
    te = np.full(len(c), 25.0)
    r = emission.relance(c, 2, te, -5.0, False, etat)
    assert r[24 + 7] == 26.0 and r[24 + 6] == 30.0
    r_sans = emission.relance(c, 2, te, -5.0, False)
    assert r_sans[24 + 6] == 26.0


def test_relance_froid_prolongee_deux_heures():
    c, etat = _journee(30.0, 26.0)
    etat[:24 + 8] = np.where(etat[:24 + 8] == 1, 1, -1)          # absence de plus de 48 h avant la 2e journée
    r = emission.relance(c, 2, np.full(len(c), 25.0), -5.0, False, etat)
    assert r[24 + 6] == 26.0 and r[24 + 5] == 30.0


def test_relance_chaud_identique_avec_ou_sans_indicateur():
    c, etat = _journee(16.0, 19.0)
    te = np.full(len(c), 5.0)
    assert np.array_equal(emission.relance(c, 2, te, -5.0, True, etat), emission.relance(c, 2, te, -5.0, True))
