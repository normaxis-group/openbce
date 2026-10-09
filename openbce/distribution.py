# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Distribution hydraulique de chauffage et de refroidissement (annexe III, fiches 8.7 à 8.10) : régulation du réseau du
groupe (débit, chute de température dans l'émetteur, température de départ à départ constant, retour constant ou loi
d'eau, retour, circulateur ; 855 à 872), pertes du réseau du groupe (875 à 881), puis réseau intergroupes (température
de départ, retour pondéré par les débits, pertes, circulateur primaire ; 905 à 929) dont la température moyenne est
celle que voit la génération (θmoy_dp, 1011).

Froid : mêmes équations avec le signe inversé (864 à 872, 882 à 888, 930 à 937) ; les pertes des réseaux froids sont
comptées positives dans la demande (point ouvert 2 de la spécification, tranché dans le sens physique).

Arbitrages (texte en image ou muet, choix de l'implémenteur de référence) :
- loi d'eau (862, figure 97) : θdép = θdép_dim sous la température de base, interpolation linéaire jusqu'à 20 °C à
  15 °C extérieurs, bornée à θi + Δθem ; limite extérieure 15 °C, départ minimal 20 °C ;
- circulateur à vitesse variable (863) : Modcirc = Modpertes x (qeff/qnom)^(2/3) pour idcirc 2, 0,5 x² + 0,5 x³ pour
  idcirc 3 ; Modpertes du réseau intergroupes = max des réseaux du groupe (idtype 1), 0 pour un réseau sans pertes (idtype 2) ;
- Delta_Theta_Em_Dim_Fr saisi négatif dans les RSEE : valeur absolue ;
- θi,moy du groupe : température d'air de fin de pas de groupe.calculer (écart de 20 à 40 K avec l'eau, impact faible).
"""
from __future__ import annotations

from dataclasses import dataclass

from .rsee import Noeud

CHAUD, FROID = 1, 2
RHO_CP = 998.0 * 1.163                 # Wh/(m³.K)
THETA_EXT_LIM_CH, THETA_DEP_CH_MIN = 15.0, 20.0        # p. 550
THETA_AMB = {CHAUD: 20.0, FROID: 26.0}                 # ambiance conventionnelle des réseaux intergroupes (p. 571, 584)
PCIRC_VC_GROUPE = 0.5                                  # part du circulateur du groupe rendue à l'ambiance (p. 562)


@dataclass(frozen=True)
class ReseauGroupe:
    fonction: int
    idtype: int                 # Type_2nd : 0 fictif, 1 hydraulique avec pertes, 2 hydraulique sans perte
    id_dp: int                  # Id_Dist_1re : réseau intergroupes parent
    lvc: float
    lhvc: float
    u_vc: float
    u_hvc: float
    paux: float                 # W, circulateur
    iddebit: int                # Mode_Reg_Debit : 1 constant continu, 2 constant intermittent, 3 variable
    idgest: int                 # Gest_2nd : 1 départ constant, 2 retour constant, 3 loi d'eau
    idcirc: int                 # Gest_Circ_2nd : 0 aucun, 1 tout ou rien, 2 et 3 vitesse variable
    theta_dep_dim: float
    theta_ret_dim: float
    d_theta_dim: float          # |Δθem_dim|
    qnom: float                 # m³/h
    qresid: float               # m³/h, débit de décharge
    b_tampon: float = 1.0

    @classmethod
    def depuis(cls, n: Noeud, fonction: int, b_tampons: dict[int, float] | None = None) -> "ReseauGroupe":
        sfx = "_Ch" if fonction == CHAUD else "_Fr"
        d_theta = abs(n.nombre("Delta_Theta_Em_Dim" + sfx, 0.0))
        theta_dep = n.nombre("Theta_Dep_Dim" + sfx, 0.0)
        theta_ret = n.nombre("Theta_Ret_Dim" + sfx, 0.0) or (theta_dep - d_theta if fonction == CHAUD else theta_dep + d_theta)
        return cls(fonction, n.entier("Type_2nd", 0), n.entier("Id_Dist_1re", 0), n.nombre("Lvc", 0.0), n.nombre("Lhvc", 0.0),
                   n.nombre("Umoyen_Vc" + sfx, 0.0), n.nombre("Umoyen_Hvc" + sfx, 0.0), n.nombre("Pcirculateur" + sfx, 0.0),
                   n.entier("Mode_Reg_Debit" + sfx, 0), n.entier("Gest_2nd" + sfx, 0), n.entier("Gest_Circ_2nd" + sfx, 0),
                   theta_dep, theta_ret, d_theta or 10.0, n.nombre("Qnom" + sfx, 0.0), n.nombre("Q2nd_Resid", 0.0),
                   (b_tampons or {}).get(n.entier("Id_Et", 0), 1.0))


@dataclass
class EtatReseau:
    fonct: int = 0
    qeff: float = 0.0
    d_theta: float = 0.0
    theta_dep: float = 0.0
    theta_ret: float = 0.0
    modpertes: float = 0.0
    modcirc: float = 0.0
    qsys: float = 0.0           # Wh, demande augmentée des pertes
    waux: float = 0.0
    phi_vc: float = 0.0
    phi_hvc: float = 0.0


def _modcirc(idcirc: int, modpertes: float, qeff: float, qnom: float) -> float:
    if idcirc == 0 or qnom <= 0:
        return 0.0
    x = min(qeff / qnom, 1.0)
    if idcirc == 1:
        return modpertes
    if idcirc == 2:
        return modpertes * x ** (2.0 / 3.0)                                                   # (863), lecture retenue
    return modpertes * (0.5 * x ** 2 + 0.5 * x ** 3)


def reseau_groupe(r: ReseauGroupe, qsys_em: float, theta_i: float, te: float, te_base: float) -> EtatReseau:
    """Régulation (855 à 872) et pertes (875 à 881) du réseau du groupe pour une heure ; qsys_em en Wh."""
    e = EtatReseau()
    if r.idtype == 0:                                                                       # (854), (873), (874)
        e.qsys = qsys_em
        return e
    e.fonct = 1 if qsys_em > 0 else 0                                                       # (855), (864)
    signe = 1.0 if r.fonction == CHAUD else -1.0
    if e.fonct:
        if r.iddebit == 3:                                                                  # (856), (865)
            qreq = qsys_em / (RHO_CP * r.d_theta_dim)
            e.qeff = max(qreq, r.qresid)
            e.d_theta = qsys_em / (RHO_CP * e.qeff) if e.qeff > 0 else r.d_theta_dim
            e.modpertes = 1.0
        elif r.iddebit == 2 and r.qnom > 0:                                                 # (857), (866)
            e.qeff = r.qnom
            e.modpertes = min(1.0, qsys_em / (RHO_CP * r.qnom * r.d_theta_dim))
            e.d_theta = r.d_theta_dim
        elif r.qnom > 0:                                                                    # (858), (867)
            e.qeff = r.qnom
            e.modpertes = 1.0
            e.d_theta = qsys_em / (RHO_CP * r.qnom)
        else:                                                                               # débit nominal absent : débit variable
            e.qeff = qsys_em / (RHO_CP * r.d_theta_dim)
            e.d_theta, e.modpertes = r.d_theta_dim, 1.0
    if r.idgest == 1:
        e.theta_dep = r.theta_dep_dim if e.fonct else theta_i                                # (860), (869)
    elif r.idgest == 2:
        e.theta_dep = (r.theta_ret_dim + signe * e.d_theta) if e.fonct else theta_i          # (861), (870)
    else:                                                                                   # loi d'eau (862), chauffage
        if not e.fonct:
            e.theta_dep = theta_i
        elif te >= THETA_EXT_LIM_CH:
            e.theta_dep = max(THETA_DEP_CH_MIN, theta_i + e.d_theta)
        elif te <= te_base:
            e.theta_dep = r.theta_dep_dim
        else:
            pente = (THETA_DEP_CH_MIN - r.theta_dep_dim) * (te - te_base) / (THETA_EXT_LIM_CH - te_base)
            e.theta_dep = max(theta_i + e.d_theta, r.theta_dep_dim + pente)
    e.theta_ret = e.theta_dep - signe * e.d_theta if e.fonct else e.theta_dep                # (872)
    e.modcirc = _modcirc(r.idcirc, e.modpertes, e.qeff, r.qnom)                             # (863), (871)
    # pertes du réseau du groupe (875 à 881)
    theta_moy = 0.5 * (e.theta_dep + e.theta_ret)
    theta_hvc = r.b_tampon * te + (1 - r.b_tampon) * theta_i
    ecart_vc, ecart_hvc = signe * (theta_moy - theta_i), signe * (theta_moy - theta_hvc)
    if r.idtype == 1:
        e.phi_vc = e.modpertes * r.u_vc * r.lvc * max(0.0, ecart_vc)
        e.phi_hvc = e.modpertes * r.u_hvc * r.lhvc * max(0.0, ecart_hvc)
    e.waux = e.modcirc * r.paux
    e.qsys = qsys_em + e.phi_vc + e.phi_hvc                                                  # (881), (888)
    return e


@dataclass(frozen=True)
class ReseauInter:
    fonction: int
    idtype: int                 # Type_Prim : 0 fictif, 1 hydraulique avec pertes, 2 sans perte
    id_gen: int
    lvc: float
    lhvc: float
    u_vc: float
    u_hvc: float
    paux: float
    idcirc: int
    b_tampon: float = 1.0

    @classmethod
    def depuis(cls, n: Noeud, fonction: int, b_tampons: dict[int, float] | None = None) -> "ReseauInter":
        sfx = "_Ch" if fonction == CHAUD else "_Fr"
        return cls(fonction, n.entier("Type_Prim", 0), n.entier("Id_Gen", 0), n.nombre("Lvc_Prim", 0.0), n.nombre("Lhvc_Prim", 0.0),
                   n.nombre("Umoyen_Vc_Prim" + sfx, 0.0), n.nombre("Umoyen_Hvc_Prim" + sfx, 0.0), n.nombre("Pcirc_Prim" + sfx, 0.0),
                   n.entier("Gest_Circ_Prim" + sfx, 0), (b_tampons or {}).get(n.entier("Id_Et", 0), 1.0))


def reseau_intergroupe(dp: ReseauInter, etats: list[EtatReseau], qnom: float, qresid: float, te: float) -> EtatReseau:
    """Réseau intergroupes pour une heure (905 à 929) : départ = extrême des réseaux du groupe, retour pondéré par les
    débits, pertes à l'ambiance conventionnelle ; `qsys` est la demande aux bornes de la génération."""
    e = EtatReseau()
    qsys_req = sum(x.qsys for x in etats)                                                   # (890)
    if dp.idtype == 0:
        e.qsys = qsys_req
        return e
    signe = 1.0 if dp.fonction == CHAUD else -1.0
    e.fonct = max((x.fonct for x in etats), default=0)
    if e.fonct:
        actifs = [x for x in etats if x.fonct]
        e.theta_dep = max(x.theta_dep for x in actifs) if dp.fonction == CHAUD else min(x.theta_dep for x in actifs)   # (906), (915)
        e.modpertes = max(x.modpertes for x in actifs) if dp.idtype == 1 else 0.0           # (908), (917)
        qtot = sum(x.qeff for x in actifs)
        e.qeff = max(qtot, qresid)
        if e.qeff > 0:
            e.theta_ret = (sum(x.qeff * x.theta_ret for x in actifs) + max(0.0, qresid - qtot) * e.theta_dep) / e.qeff   # (919)
        else:
            e.theta_ret = e.theta_dep
    else:
        e.theta_dep = e.theta_ret = THETA_AMB[dp.fonction]
    e.modcirc = 0.0 if dp.idtype == 2 else _modcirc(dp.idcirc, e.modpertes, e.qeff, qnom)  # (909), (918)
    theta_moy = 0.5 * (e.theta_dep + e.theta_ret)                                           # (922), (930)
    theta_vc = THETA_AMB[dp.fonction]
    theta_hvc = dp.b_tampon * te + (1 - dp.b_tampon) * theta_vc
    if dp.idtype == 1:
        e.phi_vc = e.modpertes * dp.u_vc * dp.lvc * max(0.0, signe * (theta_moy - theta_vc))      # (924), (932)
        e.phi_hvc = e.modpertes * dp.u_hvc * dp.lhvc * max(0.0, signe * (theta_moy - theta_hvc))  # (926), (934)
    e.waux = e.modcirc * dp.paux                                                             # (927), (935)
    e.qsys = qsys_req + e.phi_vc + e.phi_hvc                                                 # (929), (937)
    return e
