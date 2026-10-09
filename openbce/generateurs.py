# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Générateurs instantanés de la génération (annexe III, chapitre 8) : contrat d'appel commun (figure 112, p. 652) et
générateur à effet joule direct (fiche 8.18, type 500, équations 1066 à 1072, tableau 114).

Contrat : à chaque heure le générateur reçoit la demande Qreq (Wh) d'un poste (1 chauffage, 2 froid, 3 ECS), les
températures amont et aval, le ratio de puissance disponible Rpui_dispo et l'indicateur iECS_seule ; il rend l'énergie
fournie, la consommation par énergie (matrice Qcef poste x énergie), les auxiliaires, les pertes récupérables Φvc, le
reste non fourni Qrest et le taux de charge. Les générateurs thermodynamiques pour ballon sont dans generateurs_ballon.

Banc : pour les groupes chauffés par effet joule seul (distribution fictive), les RSEE donnent O_Cef_ch_annuel égal à
O_B_Ch_annuel au dixième près sur 46 groupes du lot (07/10/2026) : la génération est bien une identité, et le besoin de
chauffage Th-C au niveau des émetteurs est directement bancable sur ces groupes.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .rsee import Noeud

CH, FR, ECS = 0, 1, 2                                            # lignes de la matrice Qcef (codes du texte 1, 2, 3)
ENERGIES = (10, 20, 30, 40, 50, 60)                              # gaz, fioul, charbon, bois, électricité, réseau (tableau 253)
COL = {e: i for i, e in enumerate(ENERGIES)}
COEF_EP = {10: 1.0, 20: 1.0, 30: 1.0, 40: 1.0, 50: 2.3, 60: 1.0}  # tableau 252


@dataclass
class Resultat:
    qfou: float = 0.0            # Wh fournis
    qcons: float = 0.0           # Wh consommés (énergie finale, hors auxiliaires)
    waux: float = 0.0            # Wh d'auxiliaires propres
    phi_vc: float = 0.0          # Wh de pertes récupérables vers l'ambiance
    qrest: float = 0.0           # Wh non fournis, reportés par la gestion
    tau: float = 0.0             # taux de charge
    eta: float = 0.0             # rendement ou COP effectif
    rfonct_ecs: float = 0.0      # fraction du pas consacrée à l'ECS (générateurs chauffage + ECS)
    qcef: np.ndarray = field(default_factory=lambda: np.zeros((3, len(ENERGIES))))


@dataclass
class EffetJoule:
    """Fiche 8.18 : rendement 1, pas d'auxiliaire ni de perte récupérable (1066, 1071) ; Pmax indépendant des conditions (1067)."""
    pmax: float                  # W, pour l'ensemble des Rdim appareils
    fonction: int = 1            # Id_Fou_Gen : 1 chauffage, 3 ECS (jamais 4, p. 670)
    rdim: int = 1

    @classmethod
    def depuis(cls, n: Noeud) -> "EffetJoule":
        rdim = max(n.entier("Rdim", 1), 1)
        return cls(1000.0 * n.nombre("Pmax", 0.0) * rdim, n.entier("Id_Fou_Gen", 1), rdim)   # Pmax en kW dans les RSEE

    def appeler(self, qreq: float, poste: int, rpui_dispo: float = 1.0, **_) -> Resultat:
        r = Resultat()
        if qreq <= 0 or self.pmax <= 0:
            return r
        pmax = self.pmax * rpui_dispo
        r.qfou = r.qcons = min(qreq, pmax)                                                 # (1068)
        r.qrest = qreq - r.qcons                                                           # (1069)
        r.tau = r.qfou / pmax                                                              # (1070)
        r.eta = 1.0                                                                        # (1066)
        if poste == ECS:
            r.rfonct_ecs = r.tau                                                           # (1072)
        r.qcef[poste, COL[50]] = r.qcons                                                   # tableau 114
        return r
