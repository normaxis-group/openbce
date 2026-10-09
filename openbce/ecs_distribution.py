# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Distribution d'ECS du groupe (annexe III, fiche 9.7, équations 1730 à 1735) : pertes des tronçons terminaux à chaque
reprise de puisage, qui s'ajoutent aux besoins (1694) pour former la demande transmise à la distribution intergroupe ;
et distribution intergroupe (fiche 9.8, 1736 à 1766) : réseau bouclé (pertes du bouclage, réchauffeur électrique,
circulateur), réseau tracé (traceur électrique), ou sans réseau.

Arbitrages (le texte ne tranche pas, choix de l'implémenteur de référence) :
- θ2nd-e : 53 °C (tableau 279, fiche 9.7, la fiche de la distribution elle-même) plutôt que 48 °C (tableau 272, fiche 9.5) ;
- delta_lvc : 0 = longueur par défaut (6 x A_em / 80 en habitation, 0,05 x A_em ailleurs), 1 = longueur saisie ; une longueur
  saisie nulle avec delta_lvc = 1 (cas vu dans les RSEE) est lue comme « par défaut » ;
- btherm des tronçons hors volume chauffé : 1 (pas de champ dans les RSEE) ;
- nb_bouchons des usages non listés au tableau 280 : 2 ;
- bouclage : la demande transmise à la génération est Σ Qw_2nd + pertes du bouclage (1753), l'eau entrant dans le
  ballon restant à la température d'eau froide (le débit de bouclage qv_boucle n'est défini nulle part : même énergie,
  volume puisé majoré) ; idencl = 1 toute l'année hors enseignement (1737, 47).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rsee import Noeud

RHO_CW = 1.163            # Wh/(L.K)
THETA_2ND = 53.0          # °C, tableau 279
THETA_AMB = 20.0          # °C, ambiance des réseaux intergroupes en volume chauffé (1746, 1758)
NB_BOUCHONS = {1: 3, 2: 3, 3: 2, 4: 2, 5: 3}


@dataclass(frozen=True)
class TronconECS:
    rat: float            # part des besoins du groupe portée par l'émetteur (Rat_em_e)
    v_vc: float           # volume du tronçon en volume chauffé, L (1731)
    v_hvc: float          # hors volume chauffé, L
    nb_bouchons: int
    nb_dist: int


def troncons(groupe: Noeud, usage: int, surface: float) -> list[TronconECS]:
    out = []
    for em in groupe.directs("Emetteur_ECS"):
        rat = em.nombre("Rat_em_e", 1.0)
        a_em = rat * surface                                                            # (1675)
        ds = em.directs("Distribution_Groupe_ECS")
        d = ds[0] if ds else None
        l_saisie = d.nombre("l_vc_2nd_e", 0.0) if d else 0.0
        if d is not None and d.entier("delta_lvc", 0) == 1 and l_saisie > 0:
            l_vc = l_saisie
        else:
            l_vc = 6.0 * a_em / 80.0 if usage in (1, 2) else 0.05 * a_em                 # (1730)
        l_hvc = d.nombre("l_hvc_2nd_e", 0.0) if d else 0.0
        d_int = (d.nombre("d_int_2nd_e", 12.0) if d else 12.0) / 1000.0
        section = np.pi * d_int ** 2 / 4 * 1000.0                                       # L par m (1731)
        out.append(TronconECS(rat, l_vc * section, l_hvc * section, NB_BOUCHONS.get(usage, 2), d.entier("nb_dist_2nd_e", 1) if d else 1))
    return out


def pertes(troncons_: list[TronconECS], besoins: np.ndarray, theta_i: np.ndarray, theta_ext: np.ndarray) -> np.ndarray:
    """Pertes de distribution du groupe, Wh par heure (1732 à 1734), pour les besoins horaires du groupe."""
    total = np.zeros_like(besoins)
    for t in troncons_:
        qw = besoins * t.rat
        prec = np.concatenate(([0.0], qw[:-1]))
        succ = np.where((prec == 0) & (qw != 0), 1.0, np.where((prec != 0) & (qw != 0), (t.nb_bouchons - 1) / t.nb_bouchons, 0.0))   # (1732)
        facteur = t.nb_bouchons * succ * t.nb_dist
        total += RHO_CW * t.v_vc * (THETA_2ND - theta_i) * facteur                                             # (1733)
        total += RHO_CW * t.v_hvc * np.maximum(0.0, THETA_2ND - theta_ext) * facteur                          # (1734), btherm = 1
    return total


@dataclass(frozen=True)
class Intergroupe:
    type_reseau: int          # 0 aucun, 1 bouclé, 2 tracé
    u: float                  # W/(m.K)
    l_vc: float               # m, en volume chauffé
    l_hvc: float              # m, hors volume chauffé
    rechauffeur: bool         # Is_Rechauf_Bcl_e : pertes du bouclage compensées par un réchauffeur électrique (1747)
    gestion_circ: int         # 0 permanent, 1 asservi à idencl (1748, 1749)
    p_circ: float             # W
    b_et: float               # coefficient b de l'espace tampon qui abrite la partie hors volume chauffé (1 = extérieur)

    @classmethod
    def depuis(cls, dp: Noeud, b_tampons: dict[int, float] | None = None) -> "Intergroupe":
        t = dp.entier("Type_Reseau_Intergroupe_ECS", 0)
        sfx = "bcl" if t == 1 else "trac"
        return cls(t, dp.nombre("u_prim_e", 0.0), dp.nombre(f"l_vc_prim_{sfx}_e", 0.0), dp.nombre(f"l_hvc_prim_{sfx}_e", 0.0),
                   dp.entier("Is_Rechauf_Bcl_e", 0) == 1, dp.entier("type_gest_circ_e", 0), dp.nombre("p_circ_prim_e", 0.0),
                   (b_tampons or {}).get(dp.entier("Id_Et", 0), 1.0))

    def heure(self, qw_2nd: np.ndarray, theta_ext: np.ndarray, idencl: np.ndarray | float = 1.0, theta_depart: float = THETA_2ND) -> dict:
        """Séries horaires (Wh) : demande aux bornes de la génération, pertes du réseau, réchauffeur et traceur
        (électricité imputée à l'ECS, 1058), circulateur (auxiliaire de distribution)."""
        n = len(qw_2nd)
        zeros = np.zeros(n)
        if self.type_reseau == 0 or self.u <= 0:                                                     # (1763 à 1766)
            return dict(qw_prim=qw_2nd, pertes=zeros, elec_ecs=zeros, circulateur=zeros)
        amb_hvc = THETA_AMB + self.b_et * (theta_ext - THETA_AMB)                                     # (1745), (1757)
        if self.type_reseau == 1:
            theta_moy = theta_depart - 2.5                                                           # (1743), (1744)
            pertes = (self.u * self.l_vc * (theta_moy - THETA_AMB) + self.u * self.l_hvc * (theta_moy - amb_hvc)) * idencl   # (1745)
            circ = self.p_circ * (idencl if self.gestion_circ == 1 else 1.0) * np.ones(n)             # (1748), (1749)
            if self.rechauffeur:
                return dict(qw_prim=qw_2nd, pertes=pertes, elec_ecs=pertes, circulateur=circ)          # (1747), (1753)
            return dict(qw_prim=qw_2nd + pertes, pertes=pertes, elec_ecs=zeros, circulateur=circ)
        pertes = (self.u * self.l_vc * (theta_depart - THETA_AMB) + self.u * self.l_hvc * (theta_depart - amb_hvc)) * idencl   # (1757)
        return dict(qw_prim=qw_2nd, pertes=pertes, elec_ecs=pertes, circulateur=zeros)                 # traceur (1759), (1762)
