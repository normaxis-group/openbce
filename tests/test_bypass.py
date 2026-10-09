# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import numpy as np

from openbce import ventilation as v


def test_bypass_selon_les_trois_conditions():
    q = np.zeros(3)
    sans = v.Ventilation(q, q, 0.72)
    avec = v.Ventilation(q, q, 0.72, (12.0, 20.0, 12.0, 20.0))
    assert sans.epsilon_h(15.0, 24.0, True) == 0.72
    assert avec.epsilon_h(15.0, 24.0, True) == 0.0            # θext < θi, θext > 12, θi > 20 : bypass (494)
    assert avec.epsilon_h(10.0, 24.0, True) == 0.72           # θext trop basse
    assert avec.epsilon_h(15.0, 19.0, True) == 0.72           # intérieur trop frais
    assert avec.epsilon_h(26.0, 24.0, False) == 0.72          # air neuf plus chaud que l'intérieur
