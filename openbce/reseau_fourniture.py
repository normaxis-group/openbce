# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Sous-stations de réseaux de chaleur et de froid (annexe III, fiche 8.28, équations 1468 à 1484, tableaux 248 à 250) :
puissance d'échange PEss, pertes de la sous-station Hss (θss - θamb) avec θss combinaison de la température du
réseau primaire et de l'eau aval, ECS puis chauffage sur le même pas, énergie comptée en réseau (code 60).

Nœuds RSEE : Generateur_Reseau_Fourniture (génération) ou Source_Ballon_Base_Reseau_Fourniture (base de ballon) :
P_Ess (kW), Id_Fou_Gen (1 chauffage, 2 froid, 3 ECS, 4 chauffage + ECS), Reseau_Chaleur, Isolation_Du_Reseau, Rdim.

Arbitrages (champs non documentés, tranchés au banc sur cas 12) :
- Reseau_Chaleur est lu comme l'index du type de réseau des tableaux 248 et 249 (0 eau chaude basse température,
  1 eau chaude haute température, 2 vapeur basse pression, 3 vapeur haute pression) ; cas 12 porte 0 pour un réseau
  nommé « CHAUD », ce qui exclut une lecture booléenne ;
- Isolation_Du_Reseau est lu comme l'index de la colonne du tableau 248 (1 : classes 4/5, les meilleures ; 4 : classes 1/2) ;
- réseau de froid (Id_Fou_Gen 2) : Qss = 0 (1484).
"""
from __future__ import annotations

from dataclasses import dataclass

from .generateurs import CH, COL, ECS, Resultat
from .rsee import Noeud

# tableau 248 : Bss par type de réseau et colonne d'isolation (classe secondaire 4, 3, 2, 1)
BSS = {0: (3.5, 4.0, 4.4, 4.9), 1: (3.1, 3.5, 3.9, 4.3), 2: (2.8, 3.2, 3.5, 3.9), 3: (2.6, 3.0, 3.3, 3.7)}
# tableau 249 : température primaire et Dss par type de réseau
THETA_PRS = {0: 105.0, 1: 150.0, 2: 110.0, 3: 180.0}
DSS = {0: 0.6, 1: 0.4, 2: 0.5, 3: 0.4}


@dataclass
class ReseauFourniture:
    p_ess: float            # kW
    fonction: int
    bss: float
    theta_prs: float = 105.0
    dss: float = 0.6
    rdim: int = 1
    froid: bool = False

    @classmethod
    def depuis(cls, n: Noeud) -> "ReseauFourniture":
        fonction = n.entier("Id_Fou_Gen", 1)
        type_reseau = n.entier("Reseau_Chaleur", 0) if n.entier("Reseau_Chaleur", 0) in BSS else 0
        col = min(max(n.entier("Isolation_Du_Reseau", 1), 1), 4) - 1
        return cls(n.nombre("P_Ess", 0.0), fonction, BSS[type_reseau][col], THETA_PRS[type_reseau], DSS[type_reseau],
                   max(n.entier("Rdim", 1), 1), fonction == 2)

    def _hss(self) -> float:
        # (1474) Hss = Bss x (PEss / 1000)^(1/3), PEss en kW. Le texte extrait ne laisse pas lire la place du facteur 1000 ;
        # cas 12 (PEss 690 kW, O_Cef_ch_reseau 16,4 pour O_B_Ch 17) exclut les lectures 1000 x PEss (309 W/K, 17 kWh/m²)
        # et PEss seul (31 W/K, 1,7 kWh/m²) ; PEss / 1000 donne 3,1 W/K, soit 0,2 kW de pertes, compatible.
        return self.bss * (self.p_ess / 1000.0) ** (1.0 / 3.0)

    def appeler(self, qreq_ecs: float, qreq_ch: float, theta_aval_ecs: float, theta_aval_ch: float, theta_amb: float, iecs_seule: bool) -> Resultat:
        r = Resultat()
        pmax = 1000.0 * self.p_ess
        qreq_ecs_act, qreq_ch_act = qreq_ecs / self.rdim, qreq_ch / self.rdim
        hss = self._hss() if not self.froid else 0.0
        # ECS (1468 à 1471, 1482, 1483)
        qfou_ecs = min(qreq_ecs_act, pmax) if self.fonction in (3, 4) else 0.0
        rfonct = qfou_ecs / pmax if pmax > 0 else 0.0
        theta_ss_ecs = self.dss * self.theta_prs + (1 - self.dss) * theta_aval_ecs                              # (1476)
        if self.fonction in (3, 4):
            qss_ecs = hss * (theta_ss_ecs - theta_amb) * (1.0 if iecs_seule else rfonct)                         # (1483)
        else:
            qss_ecs = 0.0
        # chauffage (1468 à 1479)
        rpuis = 1.0 - rfonct
        qfou_ch = min(qreq_ch_act, rpuis * pmax) if self.fonction in (1, 4) else 0.0
        theta_ss_ch = self.dss * self.theta_prs + (1 - self.dss) * theta_aval_ch
        qss_ch = rpuis * hss * (theta_ss_ch - theta_amb) if (self.fonction in (1, 4) and not iecs_seule) else 0.0   # (1472)
        r.qfou = (qfou_ch + qfou_ecs) * self.rdim
        r.qcons = (qfou_ch + qss_ch + qfou_ecs + qss_ecs) * self.rdim                                           # (1477)
        r.qrest = (qreq_ecs_act - qfou_ecs + qreq_ch_act - qfou_ch) * self.rdim
        r.rfonct_ecs = rfonct
        r.tau = rfonct + (qfou_ch / (rpuis * pmax) if rpuis * pmax > 0 else 0.0)
        r.eta = r.qfou / r.qcons if r.qcons > 0 else 0.0
        r.qcef[ECS, COL[60]] = (qfou_ecs + qss_ecs) * self.rdim                                                 # tableau 250
        r.qcef[CH, COL[60]] = (qfou_ch + qss_ch) * self.rdim
        return r
