# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Comportement thermique d'un groupe (annexe III, fiche 5.21 C_BAT_comportement thermique d'un groupe).

Réseau à trois nœuds : air intérieur θi, nœud de résolution θs (surfaces légères et baies), masse θmq (parois lourdes,
inertie quotidienne). Le bilan est résolu à chaque heure par un schéma de Crank-Nicolson sur θmq (équation 365).

En mode Th-B (calcul des besoins), les inerties séquentielle et annuelle ne sont pas prises en compte (5.21.3.2). En
mode Th-D elles le sont, par superposition (5.21.3.10, figure 66) : la classe `InertieLente` porte les nœuds θms et
θma et rend le flux φmq_seq + φmq_ann injecté dans le bilan de la masse (365). Les échanges entre groupes (φmig,
Hs,ig,eq) sont nuls.
"""
from __future__ import annotations

from dataclasses import dataclass

# constantes conventionnelles (équations 311 à 314, 324, 325 et tableau 52)
HCI = 2.5            # échange convectif intérieur, W/(m².K)
HRI = 5.5            # échange radiatif intérieur, W/(m².K)
HRS = 1.2 * HRI
HIS = HCI + HRS
PTOP = 0.5           # poids de la température radiante dans la température opérative
PTRM = 1 + HCI / HRS
FSA = 0.1            # part du flux solaire transmise directement à l'air
CA, CV, HFG = 1006.0, 1830.0, 2.5e6   # J/(kg.K), J/(kg.K), J/kg
# classes d'inertie quotidienne (tableau 53) : Amq_surf (m²/m²), Cmq_surf (kJ/(K.m²))
INERTIE_QUOTIDIENNE = {1: (2.5, 80.0), 2: (2.5, 110.0), 3: (2.5, 165.0), 4: (3.0, 260.0), 5: (3.5, 370.0)}


@dataclass(frozen=True)
class Groupe:
    """Grandeurs fixes du groupe."""

    surface: float      # Agr, m²
    a_baies: float      # surface des baies, m²
    amq_surf: float     # m²/m²
    cmq_surf: float     # kJ/(K.m²)

    @property
    def at_parois(self) -> float:
        return 4.5 * self.surface                                   # (313)

    @property
    def amq(self) -> float:
        return self.amq_surf * self.surface                         # (317)

    @property
    def cmq(self) -> float:
        return self.cmq_surf * self.surface / 3.6                   # (320), ramené en Wh/K

    @property
    def hgis(self) -> float:
        return self.at_parois / (1 / HCI - 1 / HIS)                 # (323)

    @property
    def hgmqs(self) -> float:
        return HIS * self.amq                                       # (326)

    @property
    def frl_baies(self) -> float:
        return self.a_baies / self.at_parois                        # (349)

    @property
    def frm(self) -> float:
        return self.amq / self.at_parois                            # (350)

    @property
    def frmd(self) -> float:
        return self.amq / (self.at_parois - self.a_baies)           # (352)

    @property
    def frld(self) -> float:
        return (self.at_parois - self.amq - self.a_baies) / (self.at_parois - self.a_baies)   # (351)

    @property
    def frs(self) -> float:
        # Le texte ne donne pas la formule de frs. On prend le complément de frm et de la part des baies,
        # par cohérence avec (349) à (351). À CONFIRMER au banc.
        return (self.at_parois - self.amq - self.a_baies) / self.at_parois


@dataclass(frozen=True)
class Sollicitations:
    """Ce que le groupe reçoit pendant une heure."""

    hgei: float          # échange par renouvellement d'air, W/K (333)
    theta_ei: float      # température équivalente de l'air entrant, °C (338)
    h_opaque: float      # HTH,k+pt : transmission des parois opaques et des ponts thermiques, W/K (340)
    hges: float          # HTH,b : transmission des baies, W/K (341)
    theta_es: float      # température extérieure équivalente vue par les baies, °C (342)
    theta_em: float      # température extérieure équivalente vue par les parois opaques, °C (344)
    phi_i: float         # flux convectif au nœud d'air, W (346)
    phi_l: float         # flux radiatif reçu par les baies, W (347)
    phi_mq: float        # flux radiatif reçu par la masse, W (348)
    # Flux radiatif reçu par les parois légères, W. Les équations imprimées (346 à 348) répartissent les apports
    # radiatifs entre l'air, les baies et la masse, et la nomenclature cite frs et frsd sans équation : la part des
    # parois légères, frs x (apports radiatifs) + frld x (1 - fsa) x Fs1, est reconstituée ici pour que le bilan
    # ferme. À CONFIRMER au banc.
    phi_s_leger: float = 0.0


@dataclass(frozen=True)
class Temperatures:
    mq: float            # masse, fin du pas de temps
    mq_moy: float        # masse, moyenne sur le pas de temps
    s: float
    i: float

    @property
    def rm(self) -> float:
        return PTRM * self.s + (1 - PTRM) * self.i                  # (369)

    @property
    def op(self) -> float:
        return PTOP * self.rm + (1 - PTOP) * self.i                 # (371)


def hgemq(g: Groupe, h_opaque: float) -> float:
    """Échange entre le nœud de masse et l'extérieur (339)."""
    if h_opaque <= 0:
        return 0.0
    return 1 / (1 / h_opaque - 1 / g.hgmqs)


def _noeuds(g: Groupe, x: Sollicitations, sys_conv: float, sys_rad: float):
    hgei = max(x.hgei, 1e-9)
    phi_s = ((1 - x.hges / (g.a_baies * HIS)) * x.phi_l if g.a_baies > 0 else 0.0) + x.phi_s_leger   # (361)
    u1 = 1 / (1 / hgei + 1 / g.hgis)                                # (362)
    air = (x.phi_i + sys_conv) / hgei + x.theta_ei
    return hgei, phi_s + g.frs * sys_rad, u1, air                   # (372) pour la part radiative vers θs


def temperatures(g: Groupe, x: Sollicitations, mq: float, sys_conv: float = 0.0, sys_rad: float = 0.0) -> tuple[float, float]:
    """Températures θs et θi pour une température de masse donnée (367, 368)."""
    hgei, phi_s, u1, air = _noeuds(g, x, sys_conv, sys_rad)
    s = (g.hgmqs * mq + x.hges * x.theta_es + phi_s + u1 * air) / (g.hgmqs + x.hges + u1)
    i = (g.hgis * s + hgei * x.theta_ei + x.phi_i + sys_conv) / (g.hgis + hgei)
    return s, i


NB_JOURS_SEQUENCE = 14          # (315)


class InertieLente:
    """Inerties séquentielle et annuelle du groupe (353 à 360). `avancer` est appelée une fois par heure avec la
    température de masse de l'heure écoulée et rend le flux à injecter dans le bilan de la masse de l'heure suivante."""

    def __init__(self, g: Groupe, ams_surf: float, cms_surf: float, ama_surf: float, cma_surf: float):
        hgmqs, hgms, hgma = HIS * (g.amq_surf * g.surface), HIS * (ams_surf * g.surface), HIS * (ama_surf * g.surface)   # (326 à 328)
        d_r_sq, d_r_aq = (1 / hgms - 1 / hgmqs) if hgms > 0 else 0.0, (1 / hgma - 1 / hgmqs) if hgma > 0 else 0.0
        # (329), (330) : ΔR nul, ΔH nul. Un ΔR négatif (surface d'échange lente plus grande que la quotidienne) donnerait
        # une conductance négative et un calcul instable : il est traité comme nul.
        self.dh_sq = 1 / d_r_sq if d_r_sq > 1e-12 else 0.0
        self.dh_aq = 1 / d_r_aq if d_r_aq > 1e-12 else 0.0
        self.dc_sq = max(cms_surf - g.cmq_surf, 0.0) * g.surface / 3.6              # (331), Wh/K
        self.dc_as = max(cma_surf - cms_surf, 0.0) * g.surface / 3.6                # (332)
        self.ms = self.ma = 18.0
        self.histo: list[float] = []

    def avancer(self, mq: float) -> float:
        self.histo.append(mq)
        if len(self.histo) > 24 * NB_JOURS_SEQUENCE:
            del self.histo[0]
        mq_24 = sum(self.histo[-24:]) / 24 if len(self.histo) >= 24 else 18.0                                  # (353)
        mq_seq = sum(self.histo) / len(self.histo) if len(self.histo) >= 24 * NB_JOURS_SEQUENCE else 19.0        # (357)
        flux = 0.0
        if self.dh_sq and self.dc_sq:
            ms = ((self.dc_sq - 0.5 * self.dh_sq) * self.ms + self.dh_sq * mq_24) / (self.dc_sq + 0.5 * self.dh_sq)   # (354)
            flux += self.dh_sq * (0.5 * (ms + self.ms) - mq_24)                                                   # (355)
            self.ms = ms
        if self.dh_aq and self.dc_as:
            ma = ((self.dc_as - 0.5 * self.dh_aq) * self.ma + self.dh_aq * mq_seq) / (self.dc_as + 0.5 * self.dh_aq)  # (358)
            flux += self.dh_aq * (0.5 * (ma + self.ma) - mq_seq)                                                  # (359)
            self.ma = ma
        return flux


def pas(g: Groupe, x: Sollicitations, mq_precedent: float, sys_conv: float = 0.0, sys_rad: float = 0.0, phi_lent: float = 0.0) -> Temperatures:
    """Avance d'une heure. Les températures rendues (s, i) sont des moyennes sur le pas de temps (cas 1 de 5.21.3.13).
    `phi_lent` : flux des inerties séquentielle et annuelle, φmq_seq + φmq_ann (365), nul en Th-B."""
    hgem = hgemq(g, x.h_opaque)
    _, phi_s, u1, air = _noeuds(g, x, sys_conv, sys_rad)
    u2 = u1 + x.hges                                                # (363)
    u3 = 1 / (1 / u2 + 1 / g.hgmqs)                                 # (364)
    # (366). L'apport des baies Hges.θes ne figure pas dans l'équation imprimée, mais il figure dans (367) et le
    # bilan du nœud θs l'impose : on l'ajoute. À CONFIRMER au banc.
    phi_mtot = x.phi_mq + g.frm * sys_rad + hgem * x.theta_em + u3 / u2 * (phi_s + x.hges * x.theta_es + u1 * air) + phi_lent
    c = g.cmq
    mq = (mq_precedent * (c - 0.5 * (u3 + hgem)) + phi_mtot) / (c + 0.5 * (u3 + hgem))   # (365)
    mq_moy = 0.5 * (mq + mq_precedent)
    return Temperatures(mq, mq_moy, *temperatures(g, x, mq_moy, sys_conv, sys_rad))
