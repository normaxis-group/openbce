# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Parois opaques et ponts thermiques (annexe III, fiches 5.17 et 5.19) : transmission et flux transmis au groupe."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .baies import HE
from .climat import Climat
from .rayonnement import masque_azimutal, rayonnement_froid, sur_paroi
from .rsee import Noeud

# résistances superficielles cumulées selon le sens du flux : paroi verticale, flux ascendant, flux descendant
_RS = {1: 0.17, 2: 0.14, 3: 0.21}
# Bornes d'inclinaison de la figure 64, qui est une image : valeurs prises par analogie avec les baies (30° et 60°)
# et leur symétrique. À RELIRE sur la figure.
_B1, _B2, _B3, _B4 = 30.0, 60.0, 120.0, 150.0


def u_incline(uk: float, type_incl: int, beta: float) -> float:
    """Coefficient U ramené à l'inclinaison réelle de la paroi (294)."""
    rth = 1 / uk - _RS.get(type_incl, 0.17)
    vert, asc, des = 1 / (rth + 0.17), 1 / (rth + 0.14), 1 / (rth + 0.21)
    if beta < _B1:
        return asc
    if beta < _B2:
        return ((vert - asc) * beta + _B2 * asc - _B1 * vert) / (_B2 - _B1)
    if beta <= _B3:
        return vert
    if beta < _B4:
        return ((des - vert) * beta + _B4 * vert - _B3 * des) / (_B4 - _B3)
    return des


@dataclass
class FluxOpaques:
    h: float               # HTH,k+pt : transmission des parois opaques et des ponts thermiques, W/K (295, 340)
    phi_sh: np.ndarray     # flux solaire absorbé et rayonnement froid transmis au groupe, W (289, 297, 345)


def _masque(n: Noeud, climat: Climat):
    m = n.directs("Masque_Lointain_Azimutal")
    return masque_azimutal(climat, m[0].serie("Gamma"), n.nombre("Alpha")) if m else None


def du_groupe(groupe: Noeud, climat: Climat, b_tampons: dict[int, float], ete: bool = False) -> FluxOpaques:
    """`ete` : facteur de transmission solaire Sf_e des conditions « e » (Th-D en confort adaptatif, 291, 292)."""
    h, phi = 0.0, np.zeros_like(climat.te)
    for p in groupe.directs("Paroi_Opaque"):
        a, beta = p.nombre("Ak"), p.nombre("Beta")
        u = u_incline(p.nombre("Uk"), p.entier("Type_Paroi_Inclk", 1), beta)
        id_et = p.entier("Id_Et", 0)
        h += a * u * b_tampons.get(id_et, 1.0)
        if id_et:
            continue      # derrière un espace tampon non solarisé : ni soleil ni voûte céleste. Provisoire.
        ray, _ = sur_paroi(climat, p.nombre("Alpha"), beta, _masque(p, climat))
        sf = p.nombre("Sf_ek", p.nombre("Sf_ck", 0.0)) if ete else p.nombre("Sf_ck", 0.0)
        phi += a * sf * ray.total + a * u / HE * rayonnement_froid(climat, beta)
    for l in groupe.directs("Lineaire"):
        longueur = l.nombre("Ll")
        h += longueur * l.nombre("Psil") * b_tampons.get(l.entier("Id_Et", 0), 1.0)
        if not l.entier("Id_Et", 0):
            ray, _ = sur_paroi(climat, l.nombre("Alpha"), l.nombre("Beta"), _masque(l, climat))
            phi += longueur * l.nombre("Sf_cl", 0.0) * ray.total
    return FluxOpaques(h, phi)
