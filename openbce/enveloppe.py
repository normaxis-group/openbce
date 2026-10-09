# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Indicateurs d'enveloppe d'une zone : surfaces et déperditions par transmission.

Ce sont les grandeurs que le RSEE restitue par zone (Sortie_Zone_B) sans simulation horaire ; elles servent de premier
contrôle du lecteur et des conventions de classement des parois.
"""
from __future__ import annotations

from dataclasses import dataclass

from .rsee import Noeud

# Inclinaison Beta en degrés par rapport à l'horizontale : 0 = paroi horizontale vue du dessus (plancher haut),
# 90 = verticale, 180 = plancher bas. Bornes de classement à confirmer sur le texte de l'annexe III.
BETA_VERTICAL_MIN, BETA_VERTICAL_MAX = 60.0, 120.0


def classe(beta: float) -> str:
    if beta < BETA_VERTICAL_MIN:
        return "ophh"
    if beta > BETA_VERTICAL_MAX:
        return "ophb"
    return "opv"


@dataclass
class Enveloppe:
    a_opv: float = 0.0
    a_ophh: float = 0.0
    a_ophb: float = 0.0
    a_baies: float = 0.0
    h_opv: float = 0.0
    h_ophh: float = 0.0
    h_ophb: float = 0.0
    h_pt: float = 0.0
    l_pt: float = 0.0

    @property
    def h_op(self) -> float:
        return self.h_opv + self.h_ophh + self.h_ophb

    @property
    def a_t(self) -> float:
        return self.a_opv + self.a_ophh + self.a_ophb + self.a_baies


def coefficients_b(batiment: Noeud) -> dict[int, float]:
    """Coefficient de réduction b des espaces tampons du bâtiment, par Index (référencé par Id_Et des parois)."""
    b = {}
    for et in batiment.directs("Espace_Tampon_Non_Solarise"):
        b[et.entier("Index")] = et.nombre("b_et_ns")
    return b


def de_zone(zone: Noeud, b_tampons: dict[int, float] | None = None) -> Enveloppe:
    """Une paroi donnant sur un espace tampon (Id_Et non nul) voit sa déperdition multipliée par le b de cet espace."""
    b_tampons = b_tampons or {}
    e = Enveloppe()
    for p in zone.tous("Paroi_Opaque"):
        c = classe(p.nombre("Beta"))
        a, u = p.nombre("Ak"), p.nombre("Uk")
        b = b_tampons.get(p.entier("Id_Et", 0), 1.0)
        setattr(e, "a_" + c, getattr(e, "a_" + c) + a)
        setattr(e, "h_" + c, getattr(e, "h_" + c) + a * u * b)
    for b in zone.tous("Baie"):
        e.a_baies += b.nombre("Ab")
    for l in zone.tous("Lineaire"):
        e.l_pt += l.nombre("Ll")
        e.h_pt += l.nombre("Ll") * l.nombre("Psil")
    return e
