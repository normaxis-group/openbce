# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Ballon de stockage d'ECS à quatre zones (annexe III, fiches 9.9 ballon, 9.10 gestion-régulation, 9.14 assemblage).

Un ballon est découpé en quatre zones de volume Vz, du bas (zone 1, entrée d'eau froide, injection de la base) au haut
(zone 4, puisage). À chaque heure : pertes vers l'ambiance (1771), puisage par itérations avec report (1794 à 1800)
et effet piston (1774, 1777), mélange des inversions de température (1779), plafond θmax (1780), puis chauffe par la
base et par l'appoint (1811 à 1816, 1787), chacune suivie du mélange.

Arbitrages (texte muet, choix de l'implémenteur de référence) :
- Valeur_Certifiee_Justifiee_Defaut : 2 certifié (UAS tel quel), 1 justifié (1,1 UAS), 0 par défaut (tableau 283 par
  Nature_Ballon) ; un UA_S nul force le défaut. Banc cas 26 (28 CET de 175 L, UA_S 2,94, code 2) : UAS tel quel donne
  -15 % sur O_Cef_ecs, le défaut du tableau 283 (2,12 W/K) -22 % ;
- Nature_Ballon : 1 effet Joule vertical ≥ 75 L, 2 effet Joule horizontal, 3 vertical < 75 L, 4 autres, 5 solaire ;
  codes non vus : « autres » ;
- température d'ambiance du ballon : 20 °C en volume chauffé (Pos_Gen = 1), température extérieure sinon ;
- nombre d'itérations de puisage : 4 (valeur illisible du texte).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .rsee import Noeud

RHO_CW = 1.163          # Wh/(L.K)
N_ZONES = 4
NB_ITER = 4
THETA_INIT = 50.0
THETA_CONS_DEFAUT = 55.0
D_THETA_DEFAUT = 2.0


def uas_util(ps: Noeud) -> float:
    """Coefficient de pertes du ballon, W/K (1767 à 1769, tableaux 283 et 284)."""
    statut, uas, vtot = ps.entier("Valeur_Certifiee_Justifiee_Defaut", 2), ps.nombre("UA_S", 0.0), ps.nombre("V_tot", 0.0)
    if uas > 0 and statut == 2:
        return uas                                                                       # (1767)
    if uas > 0 and statut == 1:
        return 1.1 * uas                                                                 # (1768)
    nature = ps.entier("Nature_Ballon", 4)
    if nature == 5:
        return 0.16 * vtot ** 0.5                                                        # tableau 284
    if nature == 2:
        qpr = 0.939 + 0.0104 * vtot
    elif nature == 1 or (nature == 3 and vtot >= 75):
        qpr = 0.224 + 0.0663 * vtot ** (2 / 3)
    elif nature == 3:
        qpr = 0.1474 + 0.0719 * vtot ** (2 / 3)
    else:
        qpr = 0.189 * vtot ** 0.55
    return qpr * 1000.0 / (45.0 * 24.0)                                                 # (1769), kWh/jour -> W/K


def melanger(theta: list[float], v: list[float]) -> None:
    """Supprime les inversions de stratification en égalisant les zones concernées à leur moyenne volumique (1779)."""
    a = 0
    while a < N_ZONES - 1:
        if theta[a] > theta[a + 1] + 1e-9:
            k = a + 1
            while k + 1 < N_ZONES and sum(theta[j] * v[j] for j in range(a, k + 1)) / sum(v[a:k + 1]) > theta[k + 1] + 1e-9:
                k += 1
            moy = sum(theta[j] * v[j] for j in range(a, k + 1)) / sum(v[a:k + 1])
            for j in range(a, k + 1):
                theta[j] = moy
            a = 0
        else:
            a += 1


@dataclass
class Ballon:
    v: list[float]                      # volumes des zones, L, du bas vers le haut
    u: list[float]                      # pertes par zone, W/K (1770)
    theta_cons: float = THETA_CONS_DEFAUT
    theta_max: float = 90.0
    z_reg_base: int = 1                 # zone de la sonde de la base (1 à 4)
    z_base: int = 1                     # zone d'injection de la base (1948)
    z_ap: int = 1                       # zone d'injection de l'appoint
    z_reg_ap: int = 1
    d_theta_base: float = D_THETA_DEFAUT
    d_theta_ap: float = D_THETA_DEFAUT
    gestion_base: int = 0               # 0 permanent, 1 nuit, 2 jour (1811 à 1813)
    gestion_ap: int = 0
    theta: list[float] = field(default_factory=lambda: [THETA_INIT] * N_ZONES)
    theta_prec: list[float] = field(default_factory=lambda: [THETA_INIT] * N_ZONES)
    report: float = 0.0                 # Wh non fournis au pas précédent (1797)
    nbh_report: int = 0

    @classmethod
    def depuis(cls, ps: Noeud, pos_gen: int = 1) -> "Ballon":
        vtot = ps.nombre("V_tot", 0.0)
        faux = ps.nombre("f_aux", 0.5) if ps.entier("Statut_faux", 2) != 2 else 0.5
        if ps.entier("Type_prod_stockage", 0) in (1, 2) and ps.entier("Type_accumulateur_ECS", 0) == 0:
            v = [(1 - faux) * vtot / 2] * 2 + [faux * vtot / 2] * 2                    # base en bas, appoint en haut
        else:
            v = [vtot / 4] * 4
        ua = uas_util(ps)
        return cls(v=v, u=[ua * vz / vtot if vtot > 0 else 0.0 for vz in v],         # (1770)
                   theta_cons=THETA_CONS_DEFAUT if ps.entier("Id_Fou_Sto", 3) == 3 else (ps.nombre("Theta_Cons", 0.0) or THETA_CONS_DEFAUT),
                   theta_max=ps.nombre("Theta_Max", 90.0) or 90.0,
                   z_reg_base=max(1, ps.entier("z_reg_base", 1)), z_ap=max(1, ps.entier("z_appoint", 3)), z_reg_ap=max(1, ps.entier("z_reg_appoint", 3)),
                   d_theta_base=ps.nombre("Delta_Theta_base", 0.0) or D_THETA_DEFAUT, d_theta_ap=ps.nombre("Delta_Theta_appoint", 0.0) or D_THETA_DEFAUT,
                   gestion_base=ps.entier("type_gest_th_base", 0), gestion_ap=ps.entier("type_gest_th_appoint", 0))

    # --- une heure ---------------------------------------------------------------------------------------------------
    def pertes(self, theta_amb: float) -> list[float]:
        return [u * (t - theta_amb) for u, t in zip(self.u, self.theta)]               # (1771), Wh sur une heure

    def puiser(self, demande_wh: float, theta_entrant: float, theta_depart: float) -> tuple[float, float]:
        """Puisage en haut du ballon avec entrée d'eau froide en bas (1794 à 1800) ; rend (énergie fournie, volume puisé)."""
        restant, vp_total, fourni = demande_wh + self.report, 0.0, 0.0
        vmin = min(self.v)
        for _ in range(NB_ITER):
            if restant <= 0:
                break
            haut = self.theta[-1]
            if haut <= theta_depart:
                break                                                                    # (1796), (1799)
            vp = min(restant / (RHO_CW * (haut - theta_entrant)), vmin)                  # (1795), (1798)
            energie = RHO_CW * vp * (haut - theta_entrant)
            fourni += energie
            restant -= energie
            vp_total += vp
            avant = list(self.theta)
            self.theta[0] = (avant[0] * (self.v[0] - vp) + theta_entrant * vp) / self.v[0]   # (1774)
            for z in range(1, N_ZONES):
                self.theta[z] = (avant[z] * (self.v[z] - vp) + avant[z - 1] * vp) / self.v[z]   # (1777)
            melanger(self.theta, self.v)
            self.theta = [min(t, self.theta_max) for t in self.theta]                    # (1780)
        self.report = max(restant, 0.0)
        self.nbh_report = self.nbh_report + 1 if self.report > 0 else self.nbh_report
        return fourni, vp_total

    def decaler(self, vp: float, theta_entrant: float) -> None:
        """Effet piston d'un volume vp entrant par le bas (1774, 1777), par tranches d'au plus une zone, puis mélange et
        plafond ; sert aux ballons en série, où le volume puisé peut dépasser une zone du petit ballon."""
        restant = vp
        while restant > 1e-9:
            v = min(restant, min(self.v))
            avant = list(self.theta)
            self.theta[0] = (avant[0] * (self.v[0] - v) + theta_entrant * v) / self.v[0]
            for z in range(1, N_ZONES):
                self.theta[z] = (avant[z] * (self.v[z] - v) + avant[z - 1] * v) / self.v[z]
            restant -= v
        melanger(self.theta, self.v)
        self.theta = [min(t, self.theta_max) for t in self.theta]

    @staticmethod
    def plage(gestion: int, heure_legale: int) -> bool:
        if gestion == 1:
            return heure_legale > 23 or heure_legale < 5                                  # (1812)
        if gestion == 2:
            return 10 < heure_legale < 17                                                # (1813)
        return True                                                                      # (1811)

    def demande_chauffe(self, zone_inj: int, zone_reg: int, d_theta: float, gestion: int, heure_legale: int, puise: bool, pertes: list[float]) -> float:
        """Énergie demandée au générateur (base ou appoint) pour ramener à la consigne les zones au-dessus de l'injection
        (1814, 1816), Wh ; nulle si la plage horaire ou la sonde ne le demandent pas."""
        if not self.plage(gestion, heure_legale):
            return 0.0
        t_reg, t_reg_prec = self.theta[zone_reg - 1], self.theta_prec[zone_reg - 1]
        actif = puise or t_reg < self.theta_cons - d_theta or (self.theta_cons - d_theta <= t_reg < self.theta_cons and t_reg_prec < t_reg)   # (1814)
        if not actif:
            return 0.0
        zones = range(zone_inj - 1, N_ZONES)
        v_tot = sum(self.v[z] for z in zones)
        t_moy = sum(self.v[z] * self.theta[z] for z in zones) / v_tot
        return max(RHO_CW * v_tot * (self.theta_cons - t_moy) + sum(pertes[z] for z in zones), 0.0)   # (1816)

    def injecter(self, zone_inj: int, energie_wh: float, pertes: list[float] | None = None) -> None:
        """Apport du générateur dans la zone d'injection, pertes retranchées zone par zone si fournies (1787), puis mélange."""
        for z in range(N_ZONES):
            apport = energie_wh if z == zone_inj - 1 else 0.0
            perte = pertes[z] if pertes else 0.0
            self.theta[z] += (apport - perte) / (RHO_CW * self.v[z])
        melanger(self.theta, self.v)
        self.theta = [min(t, self.theta_max) for t in self.theta]

    def cloturer(self) -> None:
        self.theta_prec = list(self.theta)                                                # (1791)
