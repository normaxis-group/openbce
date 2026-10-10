# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Réseau intergroupe mixte à modules thermiques d'appartement (MTA), fiche 16.8 (Titre V Cardonnel, nœud RSEE
T5_Cardonnel_ModuleAppartement_Mixte), configuration n° 1 : modules ECS et chauffage « direct » (idfonction 2), avec ou
sans maintien en température de l'échangeur ECS, production alternée ou simultanée ; et le circuit primaire (16.8.4).

Chaque heure, le module équivalent reçoit les besoins d'ECS des groupes (majorés des pertes de distribution interne) et
l'état des réseaux de chauffage des groupes (débit, départ, retour, demande, modulation des pertes) ; il rend l'énergie à
fournir par le réseau primaire (besoins + maintien + pertes des modules, 2688), le débit moyen (2689), la température de
retour (2690), les auxiliaires des cartes (2691, 2692) et la part récupérable (2693, 2694). Le circuit primaire ajoute
ses pertes de colonnes et de gaines (2812 à 2820), son circulateur (2821) et rend la demande à la génération (2823), avec
la température moyenne du réseau comme température aval du générateur (2812). Quand il y a un besoin de chauffage,
cette demande va au mode chauffage de la génération, sinon à son mode ECS (p. 1525).

Lectures retenues là où le texte est ambigu :
- échangeur ECS : les coefficients a, b, c saisis sont utilisés tels quels quand ils ne sont pas tous nuls, sinon les
  valeurs par défaut de la p. 1491 ; le statut « justifié » (Statut_Donnees_Echangeur_ECS = 1) pénalise UA de 10 % ;
- (2649) : le débit de maintien de tous les modules (2645) n'est pas multiplié une seconde fois par Nbmod ;
- (2667) : le temps statique vaut 1 − temps ECS seule − temps chauffage seul − temps mixte (le texte retranche deux fois
  le temps mixte, sans effet en production alternée où il est nul) ;
- (2646) : si la température de sortie de maintien saisie est nulle, on prend θin − Δreseau_mixte (2647) ;
- maintien en température de l'échangeur ECS : effectif seulement si un débit de maintien est saisi (sinon ni énergie
  de maintien ni pertes statiques des modules) ;
- pertes du circuit primaire (colonnes comme gaines) seulement aux heures où un débit circule : sans débit, le réseau
  n'est pas en fonction, comme un réseau intergroupe ordinaire (905 à 929). Lecture calée sur une opération de référence
  (35 modules, 24 logements) : l'été, hors chauffage, sa consommation d'ECS laisse moins de 1 kW de pertes en moyenne,
  ce qu'un primaire maintenu à 75 °C en permanence (9 kW) ne permet pas ;
- espace tampon : sans Id_Et, b = 1 (modules et tubes hors volume chauffé vus à la température extérieure).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .rsee import Noeud

RHO_CP = 1160.0                 # Wh/(m³.K) : ρeau × Cpeau (1000 kg/m³ × 1,16 Wh/kg/K)
Q_MOD_ECS = 0.72                # m³/h, débit de puisage ECS par module (2619)
S_ECH = 0.3                     # m², surface extérieure d'un échangeur (2651)
R_SI = 0.13                     # m².K/W (2653)
S_MODULE = 0.8                  # m² (2658)
THETA_VC = 20.0                 # °C (2670), (2814)
A_DEF, B_DEF, C_DEF = -9.5502e-07, 0.07943663, -407.54714      # coefficients par défaut de l'échangeur ECS (p. 1491)


def dtlm_sortie(p_mod: float, ua: float, d_te: float) -> float:
    """ΔTs tel que (ΔTe − ΔTs) / ln(ΔTe / ΔTs) = P/UA (2625 à 2632) : la DTLM croît avec ΔTs, résolu par dichotomie sur
    ]0, ΔTe] ; si la cible dépasse ΔTe (échangeur trop petit), ΔTs = ΔTe."""
    cible = p_mod / ua if ua > 0 else d_te
    if d_te <= 0 or cible >= d_te:
        return max(d_te, 0.0)

    def f(d_ts: float) -> float:
        if abs(d_te - d_ts) < 1e-9:
            return d_te
        return (d_te - d_ts) / math.log(d_te / d_ts)

    lo, hi = 1e-6, d_te
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < cible:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-4:
            break
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class ModulesMixtes:
    """Un réseau intergroupe mixte et ses Nbmod modules identiques (configuration 1) avec son circuit primaire."""
    id_gen: int
    nb_mod: int
    maintien_ecs: int           # δM_ech_ECS_temp (2615, 2616)
    simultanee: int             # δprod_ECS_CH (2617, 2618)
    en_volume_chauffe: int      # Id_Position : 1 dans le volume chauffé, 0 hors
    idcirc: int                 # mode de régulation du circulateur (2696 à 2699)
    a: float
    b: float
    c: float
    theta_in_nom: float
    q_maintien: float           # m³/h par module
    theta_out_maintien: float   # °C, 0 = non saisie
    h_ech_ecs: float            # W/K (2654)
    h_ecs: float                # W/K (2656)
    h_mixte: float              # W/K (2655)
    h_ch: float                 # W/K (2657)
    h_module: float             # W/K (2658)
    paux_fct: float             # W par module
    paux_arret: float
    q_nom: float                # m³/h
    q_resid: float
    delta_maintien: float       # K, chute de température du réseau mixte maintenu hors utilisation
    # circuit primaire (16.8.4)
    lvc: float
    lhvc: float
    lvc_gaines: float
    lhvc_gaines: float
    u_vc: float
    u_hvc: float
    u_vc_gaines: float
    u_hvc_gaines: float
    paux_prim: float            # W
    b_tampon: float = 1.0

    @classmethod
    def depuis(cls, n: Noeud, b_tampons: dict[int, float] | None = None) -> "ModulesMixtes":
        if n.entier("Id_Fonction", 2) != 2:
            raise NotImplementedError(f"réseau mixte MTA de fonction {n.entier('Id_Fonction', 0)} (seule la configuration directe est codée)")
        a, b, c = n.nombre("a", 0.0), n.nombre("b", 0.0), n.nombre("c", 0.0)
        if a == 0.0 and b == 0.0 and c == 0.0:
            a, b, c = A_DEF, B_DEF, C_DEF
        if n.entier("Statut_Donnees_Echangeur_ECS", 0) == 1:
            a, b, c = 0.9 * a, 0.9 * b, 0.9 * c
        ep, lam = n.nombre("Ep_Iso_Echangeur_ECS", 0.0), n.nombre("Lambda_Iso_Echangeur_ECS", 0.0)
        r_ech = ep / lam if ep > 0 and lam > 0 else 0.0                                              # (2652)
        return cls(n.entier("Id_Gen", 0), max(n.entier("Nb_Mod", 1), 1), n.entier("Is_Maintenir_Temp_ECS", 0), n.entier("Is_prod_ECS_CH", 0),
                   n.entier("Id_Position", 0), n.entier("Id_Regulation_Circ", 0), a, b, c, n.nombre("Theta_In_Prim_Nom", 75.0),
                   n.nombre("q_Maintien_Echangeur_ECS", 0.0), n.nombre("Theta_Out_Prim_Maintien_Echangeur_ECS", 0.0),
                   S_ECH / (R_SI + r_ech), n.nombre("U_ECS", 0.0) * n.nombre("L_ECS", 0.0), n.nombre("U_Mixte", 0.0) * n.nombre("L_Mixte", 0.0),
                   n.nombre("U_Chauffage", 0.0) * n.nombre("L_Chauffage", 0.0), S_MODULE / (2 * R_SI + n.nombre("R_Module", 0.0)),
                   n.nombre("P_Aux_Fct", 0.0), n.nombre("P_Aux_Arret", 0.0), n.nombre("q_Nom", 0.0), n.nombre("q_Resid", 0.0),
                   n.nombre("Delta_reseau_mixte_maintien_temperature", 5.0) or 5.0,
                   n.nombre("L_Vc", 0.0), n.nombre("L_H_Vc", 0.0), n.nombre("L_Vc_gaine_MTA", 0.0), n.nombre("L_H_Vc_gaine_MTA", 0.0),
                   n.nombre("U_Moy_Vc", 0.0), n.nombre("U_Moy_H_Vc", 0.0), n.nombre("U_Moy_Vc_Gaines_Modules", 0.0), n.nombre("U_Moy_H_Vc_Gaines_Modules", 0.0),
                   n.nombre("P_Aux", 0.0), (b_tampons or {}).get(n.entier("Id_Et", 0), 1.0))

    def heure(self, qw: float, theta_2nd: float, theta_cw: float, reseaux_ch: list, te: float) -> dict:
        """Un pas de temps. `qw` : besoins d'ECS des groupes majorés de leurs pertes internes (Wh) ; `theta_2nd` :
        température de puisage (°C) ; `reseaux_ch` : états des réseaux de chauffage des groupes (distribution.EtatReseau,
        un par groupe desservi). Rend qsys (Wh, demande à la génération), theta_aval (°C), chauffage (bool), waux (Wh,
        circulateur du primaire + cartes des modules), phi_recup (Wh), pertes (Wh, modules + primaire), q_moyen (m³/h)."""
        theta_in = self.theta_in_nom
        theta_hvc = self.b_tampon * te + (1 - self.b_tampon) * THETA_VC                                  # (2672)
        theta_amb = THETA_VC if self.en_volume_chauffe else theta_hvc                                     # (2669), (2671)
        # ECS (2619 à 2640, 2659, 2660)
        q_ecs = Q_MOD_ECS * self.nb_mod
        p_ecs = RHO_CP * q_ecs * max(theta_2nd - theta_cw, 0.0)                                           # W
        if qw > 0 and p_ecs > 0:
            p_mod = p_ecs / self.nb_mod
            ua = max(self.a * p_mod ** 2 + self.b * p_mod + self.c, 1e-6)                                  # (2624)
            d_ts = dtlm_sortie(p_mod, ua, theta_in - theta_2nd)
            theta_out_ecs = d_ts + theta_cw                                                                # (2633)
            q_prim_ecs = p_ecs / (RHO_CP * max(theta_in - theta_out_ecs, 1e-6))                           # (2638)
            t_ecs = min(qw / p_ecs, 1.0)                                                                   # (2640), (2659)
            q_prim_ecs_wh = p_ecs * t_ecs                                                                  # (2639)
        else:
            theta_out_ecs = theta_in - 5.0                                                                 # (2635)
            q_prim_ecs = t_ecs = q_prim_ecs_wh = 0.0
        # chauffage direct (2641 à 2644)
        actifs = [x for x in reseaux_ch if x.fonct and x.qeff > 0]
        q_prim_ch_wh = sum(x.qsys for x in reseaux_ch)
        if actifs and q_prim_ch_wh > 0:
            q_prim_ch = sum(x.qeff * (x.theta_dep - x.theta_ret) / max(theta_in - x.theta_ret, 1e-6) for x in actifs)   # (2642)
            theta_out_ch = sum(x.qeff * x.theta_ret for x in actifs) / sum(x.qeff for x in actifs)        # (2643)
            t_ch = sum(x.modpertes for x in reseaux_ch) / len(reseaux_ch)                                 # (2661), (2664)
            if not self.simultanee:
                t_ch = max(t_ch - t_ecs, 0.0)
        else:
            q_prim_ch = q_prim_ch_wh = t_ch = 0.0
            theta_out_ch = theta_in
        t_ecs_ch = min(t_ecs, t_ch) if self.simultanee else 0.0                                            # (2663), (2666)
        t_ecs_seule = max(0.0, t_ecs - t_ecs_ch)                                                           # (2667)
        t_ch_seul = max(0.0, t_ch - t_ecs_ch)
        t_statique = max(0.0, 1.0 - t_ecs_seule - t_ch_seul - t_ecs_ch)
        # maintien en température de l'échangeur ECS (2645 à 2650) : sans débit de maintien saisi, pas de maintien
        dm = 1 if (self.maintien_ecs and self.q_maintien > 0) else 0
        q_statique = self.q_maintien * dm * self.nb_mod
        theta_out_stat = self.theta_out_maintien if (dm and self.theta_out_maintien > 0) else theta_in - self.delta_maintien
        q_statique_wh = RHO_CP * q_statique * max(theta_in - theta_out_stat, 0.0) * t_statique if dm else 0.0
        # pertes des modules (2668 à 2687)
        theta_moy_ecs = 0.5 * (theta_in + theta_out_ecs)
        theta_moy_ch = 0.5 * (theta_in + theta_out_ch)
        theta_moy_stat = 0.5 * (theta_in + theta_out_stat)
        h_e = self.h_ech_ecs + self.h_ecs
        phi_ecs_ch = self.nb_mod * t_ecs_ch * (h_e * (theta_moy_ecs - theta_amb) + self.h_mixte * (max(theta_moy_ecs, theta_moy_ch) - theta_amb)
                                                + self.h_ch * (theta_moy_ch - theta_amb)) / (1 + (h_e + self.h_mixte) / self.h_module)          # (2676)
        phi_ecs = self.nb_mod * t_ecs_seule * (h_e * (theta_moy_ecs - theta_amb) + self.h_mixte * (theta_moy_ecs - theta_amb)) / (1 + (h_e + self.h_mixte) / self.h_module)   # (2679)
        phi_ch = self.nb_mod * t_ch_seul * (h_e * dm * (theta_moy_stat - theta_amb) + self.h_mixte * (max(theta_moy_stat if dm else theta_moy_ch, theta_moy_ch) - theta_amb)
                                             + self.h_ch * (theta_moy_ch - theta_amb)) / (1 + (h_e * dm + self.h_mixte + self.h_ch) / self.h_module)   # (2683)
        phi_stat = self.nb_mod * t_statique * (h_e * (theta_moy_stat - theta_amb) + self.h_mixte * (theta_moy_stat - theta_amb)) / (1 + (h_e + self.h_mixte) / self.h_module) if dm else 0.0   # (2686), (2687)
        phi_module = max(phi_ecs_ch, 0.0) + max(phi_ecs, 0.0) + max(phi_ch, 0.0) + max(phi_stat, 0.0)      # (2668)
        q_totale = q_prim_ecs_wh + q_prim_ch_wh + q_statique_wh + phi_module                                # (2688)
        q_moyen = max((q_prim_ecs + q_prim_ch) * t_ecs_ch + q_prim_ecs * t_ecs_seule + (q_statique + q_prim_ch) * t_ch_seul + q_statique * t_statique, self.q_resid)   # (2689)
        poids = q_prim_ecs + q_prim_ch + q_statique
        if poids > 0:
            theta_out = (q_prim_ecs * theta_out_ecs + q_prim_ch * theta_out_ch + q_statique * theta_out_stat) / poids    # (2690)
        else:
            theta_out = theta_in - self.delta_maintien
        caux_mod = self.paux_fct * (t_ecs_ch + t_ecs_seule + t_ch_seul) + self.paux_arret * t_statique     # (2692)
        caux = self.nb_mod * caux_mod                                                                       # (2691)
        phi_recup = self.nb_mod * 0.5 * (phi_module / self.nb_mod + caux_mod) if self.en_volume_chauffe else 0.0   # (2693), (2694)
        modpertes = 1.0                                                                                    # (2695)
        x = min(q_moyen / self.q_nom, 1.0) if self.q_nom > 0 else 0.0
        modcirc = {0: 0.0, 1: modpertes, 2: modpertes * x ** (2.0 / 3.0), 3: modpertes * (0.5 * x + 0.5 * x ** 2) ** (2.0 / 3.0)}.get(self.idcirc, 0.0)   # (2696 à 2699)
        # circuit primaire (2812 à 2823) : pertes des colonnes et des gaines seulement quand un débit circule (2816 à 2820,
        # étendu aux colonnes : sans débit, le réseau n'est pas en fonction, comme un réseau intergroupe ordinaire, 905 à 929)
        theta_moy = 0.5 * (theta_in + theta_out)
        if q_moyen > 0:
            phi_vc = modpertes * (self.u_vc * self.lvc + self.u_vc_gaines * self.lvc_gaines) * max(0.0, theta_moy - THETA_VC)            # (2815), (2816)
            phi_hvc = modpertes * (self.u_hvc * self.lhvc + self.u_hvc_gaines * self.lhvc_gaines) * max(0.0, theta_moy - theta_hvc)      # (2819)
        else:
            phi_vc = phi_hvc = 0.0                                                                                                 # (2817), (2820)
        waux_prim = modcirc * self.paux_prim                                                                                 # (2821)
        return dict(qsys=q_totale + phi_vc + phi_hvc, theta_aval=theta_moy, chauffage=q_prim_ch_wh > 0, waux=waux_prim + caux, phi_recup=phi_recup,
                    pertes=phi_module + phi_vc + phi_hvc, pertes_modules=phi_module, pertes_primaire=phi_vc + phi_hvc, q_moyen=q_moyen, theta_out=theta_out,
                    q_ecs=q_prim_ecs_wh, q_ch=q_prim_ch_wh, q_statique=q_statique_wh, temps=(t_ecs_ch, t_ecs_seule, t_ch_seul, t_statique))
