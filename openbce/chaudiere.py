# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Chaudières gaz et fioul (annexe III, fiche 8.19, équations 1073 à 1119, tableaux 116 à 123) : rendements à pleine
charge et à charge intermédiaire corrigés de la température aval, pertes à l'arrêt, auxiliaires, ECS instantanée puis
chauffage sur le même pas (Rpuis_dispo), pertes récupérables vers l'ambiance.

Nœud RSEE Generateur_Combustion (champs relevés sur cas 24 et cas 09) : Generateur (type, tableau 116 : 0 gaz
classique, 1 gaz condensation, 2 fioul classique, 3 fioul condensation, 4 bois), Combustible_Gaz (0 gaz naturel,
1 GPL), Ventilation (ventilateur de combustion), Evac_Fumee (clapet), Pn_gen et Pint (kW), R_pn et R_Pint (%, sur PCI),
Q_po_30 (W), Q_veille (W), Q_aux_nom (W), Theta_Fonc_Min, Id_Fou_Gen_1 (1 chauffage, 3 ECS, 4 chauffage + ECS), Rdim.

Arbitrages (texte muet ou en image, choix de l'implémenteur de référence) :
- codes des statuts Valeur_Certifiee_Defaut_R_pn / R_Pint : 3 certifié (tel quel), 2 justifié (x 0,9), 1 déclaré
  (x 0,8), 0 par défaut (tableau 119) ; Valeur_Mesuree_Defaut_* : 1 mesuré, 0 par défaut ;
- le type de chaudière n'est pas porté par un code lisible : condensation si R_Pint > 100 % ou si le champ Generateur
  vaut 1 ou 3, classique sinon ; combustible gaz sauf Generateur 2 ou 3 (fioul) ;
- idpertes_parois (tableau 122) : 3 si clapet sur le conduit (Evac_Fumee 1), 2 si ventilateur de combustion, 1 sinon ;
- Waux_int à défaut de champ : Q_aux_nom x (Pint / Pn_gen)^n avec n = 0,48 (tableau 120) ;
- état « dernier fonctionnement » (1090, 1105 à 1108) tenu par mode avec Rfonct de l'heure précédente.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .generateurs import CH, COL, ECS, Resultat
from .rsee import Noeud

PCSI = {10: 1.11, 11: 1.09, 20: 1.07, 40: 1.08}          # gaz naturel, GPL, fioul, bois (tableau 117)
THETA_MIN = {"classique": 40.0, "condensation": 30.0, "bois": 70.0}    # p. 677
THETA_MAX = 100.0
# tableau 119 (défauts) : c1..c6 ; tableau 120 : c7..c10, n ; tableau 121 : alpha et theta de référence
DEFAUT_GAZ_FIOUL = dict(c1=94.0, c2=1.0, c3=103.0, c4=1.0, c5=4.0, c6=-0.4, c7=0.0, c8=45.0, c9=0.0, c10=15.0, n=0.48)
ALPHA = {"classique": (0.04, 70.0, 0.05, 40.0), "condensation": (0.2, 70.0, 0.2, 33.0), "bois": (0.0, 70.0, 0.0, 70.0)}   # tableau 121
P_ARRET = {1: 0.50, 2: 0.75, 3: 1.0}                      # tableau 122, part des pertes à l'arrêt par les parois
P_FONCT = 0.30                                            # tableau 123 (0,25 pour le bois)
WVEILLE_DEFAUT = 20.0                                     # (1076)
STATUT = {3: 1.0, 2: 0.9, 1: 0.8}                         # correction des rendements selon le statut


@dataclass
class Chaudiere:
    pn: float                    # kW
    pint: float                  # kW
    r_pn: float                  # fraction, sur PCI, à θ de référence
    r_pint: float
    q_po_30: float               # W, pertes à l'arrêt pour un écart de 30 K
    w_veille: float              # W
    w_aux_nom: float             # W
    w_aux_int: float             # W
    theta_min: float
    famille: str                 # classique, condensation, bois
    energie: int                 # 10 gaz, 20 fioul, 40 bois
    pcsi: float
    idpertes_parois: int
    fonction: int                # 1 chauffage, 3 ECS, 4 les deux
    rdim: int = 1
    pos_gen: int = 0
    # états
    rfonct_ecs_prec: float = 0.0
    theta_cr_ecs_prec: float = 0.0
    qfou_ch_prec: float = 0.0
    theta_cr_ch_prec: float = 0.0

    @classmethod
    def depuis(cls, n: Noeud, pos_gen: int = 0) -> "Chaudiere":
        type_gen = n.entier("Generateur", 0)
        pn = n.nombre("Pn_gen", 0.0)
        pint = n.nombre("Pint", 0.0) or 0.3 * pn
        r_pint_saisi = n.nombre("R_Pint", 0.0)
        if type_gen == 4:
            famille, energie = "bois", 40
        else:
            energie = 20 if type_gen in (2, 3) else (11 if n.entier("Combustible_Gaz", 0) == 1 else 10)
            famille = "condensation" if (type_gen in (1, 3) or r_pint_saisi > 100.0) else "classique"
        pcsi = PCSI[energie]
        d = DEFAUT_GAZ_FIOUL
        log_pn = math.log10(max(pn, 1e-3))
        statut_pn, statut_pint = n.entier("Valeur_Certifiee_Defaut_R_pn", 0), n.entier("Valeur_Certifiee_Defaut_R_Pint", 0)
        # Rendements ramenés au PCS (p. 678 : les rendements saisis sont sur PCI, divisés par PCSI ; les défauts 1073 et 1074
        # le sont déjà) ; (1099) ramène ensuite la consommation au PCI : Qcons = Qfou / R_PCI au total.
        r_pn = (n.nombre("R_pn", 0.0) / 100.0 * STATUT[statut_pn] if statut_pn in STATUT and n.nombre("R_pn", 0.0) > 0 else (d["c1"] + d["c2"] * log_pn) / 100.0) / pcsi   # (1073)
        r_pint = (r_pint_saisi / 100.0 * STATUT[statut_pint] if statut_pint in STATUT and r_pint_saisi > 0 else (d["c3"] + d["c4"] * log_pn) / 100.0) / pcsi   # (1074)
        if max(r_pn, r_pint) >= 1.0:
            raise ValueError("rendement sur PCS supérieur ou égal à 1")                                                # (1121)
        q_po_30 = n.nombre("Q_po_30", 0.0) if n.entier("Valeur_Mesuree_Defaut_Q_po_30", 0) == 1 and n.nombre("Q_po_30", 0.0) > 0 else 1000.0 * d["c5"] * pn ** d["c6"] * pn   # (1075)
        w_veille = n.nombre("Q_veille", 0.0) or WVEILLE_DEFAUT                                                        # (1076)
        w_aux_nom = n.nombre("Q_aux_nom", 0.0) if n.entier("Valeur_Mesuree_Defaut_Q_aux_nom", 0) == 1 and n.nombre("Q_aux_nom", 0.0) > 0 else d["c7"] + d["c8"] * pn ** d["n"]   # (1077)
        w_aux_int = n.nombre("Q_aux_int", 0.0) or (d["c9"] + d["c10"] * pint ** d["n"] if n.entier("Valeur_Mesuree_Defaut_Q_aux_nom", 0) != 1 else w_aux_nom * (pint / pn) ** d["n"])   # (1078)
        theta_min = n.nombre("Theta_Fonc_Min", 0.0) if n.entier("Valeur_Mesuree_Defaut_Theta_Min", 0) == 1 and n.nombre("Theta_Fonc_Min", 0.0) > 0 else THETA_MIN[famille]
        idp = 3 if n.entier("Evac_Fumee", 0) == 1 else (2 if n.entier("Ventilation", 0) == 1 else 1)
        return cls(pn, pint, r_pn, r_pint, q_po_30, w_veille, w_aux_nom, w_aux_int, theta_min, famille, energie, pcsi, idp,
                   n.entier("Id_Fou_Gen_1", 1), max(n.entier("Rdim", 1), 1), pos_gen)

    # --- rendements et pertes ---------------------------------------------------------------------------------------
    def _r_pn(self, theta_aval: float) -> float:
        a, t_ref, _, _ = ALPHA[self.famille]
        return self.r_pn + a * (t_ref - theta_aval) / 100.0                                                         # (1079)

    def _r_pint(self, theta_aval: float) -> float:
        _, _, a, t_ref = ALPHA[self.famille]
        return self.r_pint + a * (t_ref - theta_aval) / 100.0                                                       # (1080)

    def _phi_stab(self, theta_aval: float, theta_amb: float) -> float:
        return max(0.0, self.q_po_30 * (max(0.0, theta_aval - theta_amb) / 30.0) ** 1.25)                          # (1081)

    def _fonctionnement(self, qfou: float, theta_cr: float, theta_amb: float) -> tuple[float, float, float, float]:
        """Pertes et auxiliaires d'un mode qui fournit qfou (Wh) ; rend (pertes, waux, pth_nom, pth_int) en Wh et W."""
        r_pn, r_pint = self._r_pn(theta_cr), self._r_pint(theta_cr)
        pth_nom = 1000.0 * r_pn / self.r_pn * self.pn                                                                # (1083)
        pth_int = 1000.0 * r_pint / self.r_pint * self.pint                                                         # (1087)
        phi_int = (1.0 / r_pint - 1.0) * pth_int                                                                    # (1088)
        phi_nom = (1.0 / r_pn - 1.0) * pth_nom                                                                      # (1089)
        if qfou <= pth_int:                                                                                         # (1093 à 1095) : cycles tout ou rien
            fx = qfou / pth_int if pth_int > 0 else 0.0
            pertes = fx * phi_int + (1 - fx) * self._phi_stab(theta_cr, theta_amb)
            waux = fx * self.w_aux_int + (1 - fx) * self.w_veille
        else:                                                                                                       # (1096 à 1098) : modulation
            fx = (qfou - pth_int) / max(pth_nom - pth_int, 1e-9)
            pertes = fx * phi_nom + (1 - fx) * phi_int
            waux = fx * self.w_aux_nom + (1 - fx) * self.w_aux_int
        return pertes, waux, pth_nom, pth_int

    def appeler(self, qreq_ecs: float, qreq_ch: float, theta_aval_ecs: float, theta_aval_ch: float, theta_amb: float, iecs_seule: bool) -> Resultat:
        """Un pas : ECS instantanée d'abord (1082 à 1099), chauffage ensuite sur le temps restant (1100 à 1119). Les
        demandes sont celles de la génération (Wh), les résultats valent pour les Rdim appareils."""
        r = Resultat()
        qreq_ecs_act, qreq_ch_act = qreq_ecs / self.rdim, qreq_ch / self.rdim
        # ECS
        theta_cr_ecs = max(theta_aval_ecs, self.theta_min)                                                          # (1084)
        pth_nom_ecs = 1000.0 * self._r_pn(theta_cr_ecs) / self.r_pn * self.pn
        qfou_ecs = min(pth_nom_ecs, qreq_ecs_act) if self.fonction in (3, 4) else 0.0                               # (1082)
        rfonct = qfou_ecs / pth_nom_ecs if pth_nom_ecs > 0 and qfou_ecs > 0 else 0.0                                # (1085)
        if qfou_ecs > 0:
            pertes_ecs, waux_ecs, _, _ = self._fonctionnement(qfou_ecs, theta_cr_ecs, theta_amb)
            qcons_ecs = (qfou_ecs + pertes_ecs) / self.pcsi                                                         # (1099)
        elif iecs_seule and self.fonction in (3, 4):
            pertes_ecs = self.rfonct_ecs_prec * self._phi_stab(self.theta_cr_ecs_prec, theta_amb)                   # (1090)
            qcons_ecs, waux_ecs = pertes_ecs, self.w_veille                                                         # (1091), (1092)
        else:
            pertes_ecs = qcons_ecs = waux_ecs = 0.0
        # chauffage
        rpuis = 1.0 - rfonct                                                                                        # (1102)
        theta_cr_ch = max(theta_aval_ch, self.theta_min)
        pth_nom_ch = 1000.0 * self._r_pn(theta_cr_ch) / self.r_pn * self.pn
        qfou_ch = min(rpuis * pth_nom_ch, qreq_ch_act) if self.fonction in (1, 4) else 0.0                          # (1100)
        if qfou_ch > 0:
            pertes_ch, waux_ch, _, _ = self._fonctionnement(qfou_ch / max(rpuis, 1e-9), theta_cr_ch, theta_amb)
            pertes_ch, waux_ch = rpuis * pertes_ch, rpuis * waux_ch
            qcons_ch = (qfou_ch + pertes_ch) / self.pcsi
        else:
            if rpuis < 1.0:
                pertes_ch = rpuis * self._phi_stab(theta_cr_ecs, theta_amb)                                          # (1105)
            elif self.qfou_ch_prec > 0:
                pertes_ch = rpuis * self._phi_stab(self.theta_cr_ch_prec, theta_amb)                                 # (1106)
            elif self.rfonct_ecs_prec > 0:
                pertes_ch = self.rfonct_ecs_prec * self._phi_stab(self.theta_cr_ecs_prec, theta_amb)                 # (1107)
            else:
                pertes_ch = 0.0                                                                                     # (1108)
            qcons_ch = pertes_ch if self.fonction in (1, 4) else 0.0                                                # (1109)
            waux_ch = self.w_veille if self.fonction in (1, 4) else 0.0                                             # (1110)
        # sorties (1111 à 1119)
        r.qfou = (qfou_ch + qfou_ecs) * self.rdim
        r.qcons = (qcons_ch + qcons_ecs) * self.rdim
        r.waux = (waux_ch + waux_ecs) * self.rdim
        r.qrest = (qreq_ecs_act - qfou_ecs + qreq_ch_act - qfou_ch) * self.rdim
        r.rfonct_ecs = rfonct
        r.tau = rfonct + (rpuis * qfou_ch / max(rpuis * pth_nom_ch, 1e-9) if qfou_ch > 0 else 0.0)                  # (1115)
        r.eta = r.qfou / r.qcons if r.qcons > 0 else 0.0                                                            # (1117)
        r.qcef[ECS, COL[10 if self.energie == 11 else self.energie]] = qcons_ecs * self.rdim                        # (1118)
        r.qcef[ECS, COL[50]] = waux_ecs * self.rdim
        r.qcef[CH, COL[10 if self.energie == 11 else self.energie]] = qcons_ch * self.rdim
        r.qcef[CH, COL[50]] = waux_ch * self.rdim
        pertes = (pertes_ch + pertes_ecs) * self.rdim
        part = (P_FONCT if self.famille != "bois" else 0.25) if r.qfou > 0 else P_ARRET[self.idpertes_parois]
        r.phi_vc = self.pos_gen * (part * pertes + r.waux)                                                          # (1119)
        # états
        self.rfonct_ecs_prec, self.theta_cr_ecs_prec = rfonct, theta_cr_ecs
        self.qfou_ch_prec, self.theta_cr_ch_prec = qfou_ch, theta_cr_ch
        return r
