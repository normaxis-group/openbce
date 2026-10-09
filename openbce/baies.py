# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Baie vitrée (annexe III, fiche 5.10 C_BAT_Baie vitrée) : déperdition et flux solaires transmis au groupe.

Traite les protections mobiles autres que les stores vénitiens (volets, stores enroulables) : leurs facteurs solaires
sont les mêmes pour le direct, le diffus et le réfléchi (214). Les baies sur espace tampon vitré (coefficients
b_therm, b_solaire) et les flux lumineux (231 à 237) restent à écrire.

Le taux de fermeture Rprot (0 = protection relevée, 1 = baissée) vient de la gestion des protections mobiles (fiche 5.9).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .climat import Climat
from .rayonnement import Incident, MasquesProches, masque_azimutal, rayonnement_froid, sur_paroi
from .rsee import Noeud

HE = 25.0                 # échange global extérieur, W/(m².K)
BETA1, BETA2 = 30.0, 60.0  # en dessous de BETA1 la baie est horizontale, au-dessus de BETA2 verticale


def _u(horizontal: float, vertical: float, beta: float) -> float:
    """Coefficient U selon l'inclinaison (207, 208). Beta est ramené entre 0 et 90°."""
    b = min(beta, 180.0 - beta)
    if b < BETA1:
        return horizontal
    if b >= BETA2:
        return vertical
    return ((vertical - horizontal) * b + BETA2 * horizontal - BETA1 * vertical) / (BETA2 - BETA1)


@dataclass(frozen=True)
class Baie:
    surface: float
    alpha: float
    beta: float
    u_sp: float            # sans protection mobile
    u_ap: float            # avec protection mobile
    sw_sp: tuple[float, float, float]   # Sw1, Sw2, Sw3 sans protection, conditions Th-BC (indice c)
    sw_ap: tuple[float, float, float]   # Sw1, Sw2, Sw3 avec protection
    sw_sp_e: tuple[float, float, float] = (0.0, 0.0, 0.0)   # sans protection, conditions Th-D « e » (224) ; (215) : Sw_c = Sw_e - 0,1
    masque: tuple[float, ...] = ()      # masque lointain : 36 hauteurs d'horizon, en degrés
    sur_tampon: bool = False
    proches: MasquesProches | None = None
    tl_sp: tuple[float, float] = (0.0, 0.0)   # transmission lumineuse sans protection : globale (Tli), part diffusée (Tlid)
    tl_ap: tuple[float, float] = (0.0, 0.0)   # avec protection


def lire(n: Noeud) -> Baie:
    """Construit la baie à partir du nœud « Baie » du format réglementaire."""
    beta = n.nombre("Beta")
    masques = n.directs("Masque_Lointain_Azimutal")
    g, d, h = n.directs("Masque_Vert_Gauche"), n.directs("Masque_Vert_Droite"), n.directs("Masque_Horizontal")
    proches = None
    if g or d or h:
        proches = MasquesProches(
            dvg=g[0].nombre("Dvg", 0) if g else 0, dpg=g[0].nombre("Dpg", 0) if g else 0,
            dvd=d[0].nombre("Dvd", 0) if d else 0, dpd=d[0].nombre("Dpd", 0) if d else 0,
            largeur=(g or d)[0].nombre("lp_b", 1) if (g or d) else 1.0,
            dhm=h[0].nombre("Dhm", 0) if h else 0, dhp=h[0].nombre("Dhp", 0) if h else 0, hauteur=h[0].nombre("hp_b", 1) if h else 1.0)
    return Baie(
        surface=n.nombre("Ab"), alpha=n.nombre("Alpha"), beta=beta,
        u_sp=_u(n.nombre("Usp_Horiz"), n.nombre("Usp_Vert"), beta), u_ap=_u(n.nombre("Uap_Horiz"), n.nombre("Uap_Vert"), beta),
        sw_sp=(n.nombre("Sw1_sp_c"), n.nombre("Sw2_sp_c"), n.nombre("Sw3_sp_c")),
        sw_ap=(n.nombre("Sw1_ap"), n.nombre("Sw2_ap"), n.nombre("Sw3_ap")),
        sw_sp_e=(n.nombre("Sw1_sp_e", n.nombre("Sw1_sp_c")), n.nombre("Sw2_sp_e", n.nombre("Sw2_sp_c")), n.nombre("Sw3_sp_e", n.nombre("Sw3_sp_c"))),
        masque=tuple(masques[0].serie("Gamma")) if masques else (), sur_tampon=n.entier("Id_Et", 0) != 0, proches=proches,
        tl_sp=(n.nombre("Tli_sp", 0.0), n.nombre("Tlid_sp", 0.0)), tl_ap=(n.nombre("Tli_ap", 0.0), n.nombre("Tlid_ap", 0.0)))


@dataclass
class FluxBaie:
    hges: np.ndarray   # déperdition, W/K (210)
    fs1: np.ndarray    # flux transmis en courte longueur d'onde, W (219)
    fs2: np.ndarray    # flux réémis en grande longueur d'onde et convection, W (220)
    fs3: np.ndarray    # flux de la lame d'air intérieure ventilée, W (221)
    ftvc: np.ndarray   # rayonnement froid vers la voûte céleste, W (222)
    incident: Incident


def flux(b: Baie, climat: Climat, rprot: np.ndarray | float, ete: bool = False) -> FluxBaie:
    """`ete` : conditions « e » de Th-D en période de confort adaptatif (224) ; avec protection, Sw_ap est le même (216)."""
    r = np.broadcast_to(np.asarray(rprot, dtype=float), climat.te.shape)
    masque = masque_azimutal(climat, list(b.masque), b.alpha) if b.masque else None
    ray, _ = sur_paroi(climat, b.alpha, b.beta, masque, b.proches)
    total = ray.total                                                  # (206)
    hges = b.surface * ((1 - r) * b.u_sp + r * b.u_ap)                 # (210), b_therm = 1 hors espace tampon

    def composante(k: int) -> np.ndarray:
        # (214) : avec protection, même facteur pour le direct, le diffus et le réfléchi ; facteur de pertes f_lf nul
        return b.surface * ((1 - r) * (b.sw_sp_e if ete else b.sw_sp)[k] + r * b.sw_ap[k]) * total

    ftvc = np.zeros_like(total) if b.sur_tampon else b.surface * ((1 - r) * b.u_sp + r * b.u_ap) / HE * rayonnement_froid(climat, b.beta)
    return FluxBaie(hges, composante(0), composante(1), composante(2), ftvc, ray)


def eclairement(b: Baie, climat: Climat) -> np.ndarray:
    """Éclairement total incident sur la baie, en lux, masque lointain compris (sert à la gestion des protections)."""
    masque = masque_azimutal(climat, list(b.masque), b.alpha) if b.masque else None
    return sur_paroi(climat, b.alpha, b.beta, masque, b.proches)[1].total


def flux_lumineux(b: Baie, climat: Climat, ferme: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Flux lumineux transmis au groupe, en lumens : direct (Flt1), diffus (Flt2), réfléchi vers le plafond (Flt3),
    pour la protection relevée ou baissée (231 à 233, avec les conventions 214, 225 à 229)."""
    masque = masque_azimutal(climat, list(b.masque), b.alpha) if b.masque else None
    ecl = sur_paroi(climat, b.alpha, b.beta, masque, b.proches)[1]
    tli, tlid = b.tl_ap if ferme else b.tl_sp
    tlii = tli - tlid
    return b.surface * tlii * ecl.direct, b.surface * (tlid * ecl.direct + tli * ecl.diffus + tlid * ecl.reflechi), b.surface * tlii * ecl.reflechi
