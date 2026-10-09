# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import pytest

from openbce import parois, protections as p


def test_volet_manuel_motorise_en_hiver():
    # occupation, de jour, éclairement nul : 10 % en locaux occupés (part 0,5 en maison), 10 % en locaux inoccupés
    assert p.volet_manuel(4, 1, True, 1.0, p.HIVER, 20.0) == pytest.approx(0.5 * (0.10 + 0.9 * 1 / 100000) + 0.5 * 0.10)
    # occupation, de nuit : 90 % en locaux occupés, 80 % ailleurs
    assert p.volet_manuel(4, 1, True, 0.0, p.HIVER, 20.0) == pytest.approx(0.5 * 0.90 + 0.5 * 0.80)
    # inoccupation de jour
    assert p.volet_manuel(4, 1, False, 5000.0, p.HIVER, 20.0, iocc_gpm=0) == 0.10


def test_volet_ferme_au_dela_du_seuil_d_eclairement_en_ete_chaud():
    assert p.volet_manuel(4, 2, True, 50000.0, p.ETE, 28.0) == pytest.approx(0.7 * 1.0 + 0.3 * 0.50)


def test_u_d_une_paroi_selon_son_inclinaison():
    assert parois.u_incline(0.25, 1, 90) == pytest.approx(0.25)
    assert parois.u_incline(0.25, 3, 180) == pytest.approx(0.25)
    assert parois.u_incline(0.25, 1, 0) == pytest.approx(1 / (1 / 0.25 - 0.17 + 0.14))


def test_volet_automatique():
    # hiver, sans horloge : la part automatique reste ouverte jour et nuit ; seule la dérogation manuelle ferme
    r, chaud = p.volet_auto(False, 2, True, 0.0, p.HIVER, 20.0, 19.0, False, type_horloge=0)
    assert not chaud and r == pytest.approx(0.7 * 0.25 * 0.80)
    # inoccupation : pas de dérogation ; avec horloge crépusculaire, fermé la nuit en hiver
    assert p.volet_auto(False, 2, False, 0.0, p.HIVER, 20.0, 19.0, False, type_horloge=1)[0] == 1.0
    # été, inoccupation, de jour, local chaud : fermé
    r, chaud = p.volet_auto(False, 2, False, 30000.0, p.ETE, 27.0, 28.0, False)
    assert chaud and r == 1.0
    # entre les deux limites de température, l'état précédent est conservé
    assert p.volet_auto(False, 2, False, 30000.0, p.ETE, 27.0, 26.0, True)[1] is True
    assert p.volet_auto(False, 2, False, 30000.0, p.ETE, 27.0, 26.0, False)[1] is False


def test_store_enroulable():
    assert p.decoder(5) == (True, 2) and p.decoder(1) == (False, 1)
    # store manuel non motorisé, hiver, occupation de nuit : 10 % en locaux occupés, 20 % ailleurs
    assert p.volet_manuel(3, 2, True, 0.0, p.HIVER, 20.0, store=True) == pytest.approx(0.7 * 0.10 + 0.3 * 0.20)
    assert p.store_remonte(True, True, 12.0) and not p.store_remonte(True, False, 12.0) and not p.store_remonte(False, True, 12.0)
