# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Générateurs thermodynamiques électriques en chauffage et en refroidissement (annexe III, fiche 8.23, 1239 à 1339).

Couvert : PAC air extérieur / eau (Sys_thermo 1) et air extérieur / air recyclé (2), modes chauffage et froid, lues
dans Generateur_Thermodynamique_Elec_NonReversible, _Reversible, _Autre et dans les bases de ballon double et triple
service (tableaux 147, 149, 150 pour la correspondance Sys_Thermo_Rev / _ds / _ts). Matrices de performance complétées
par les Cnn des tableaux 152 à 156 et 197 à 201, interpolation bilinéaire bornée (1284 à 1289), limites de source
(1297, 1298), charge partielle à puissance variable ou tout ou rien (1301 à 1319), auxiliaires à charge nulle (1278
à 1280, 1325 à 1327), partage du pas avec l'ECS d'un multiservice (1294, 1295), rejets à la source (1333, 1335).

Hors champ : sources eau, sol, boucle d'eau, nappe et air extrait (NotImplementedError), machines réversibles autres
que air/eau et air/air. Le mode ECS des PAC est dans generateurs_ballon.

Arbitrages (texte muet, choix de l'implémenteur de référence) :
- Generateur_Thermodynamique_Elec_Autre (Cat_Gen 503) : lu comme une PAC réversible dont Sys_Thermo donne la technologie
  des deux modes (tableau 147), matrices COP / Pabs_Ch / COR_Ch et EER / Pabs_Fr / COR_Fr ;
- limite déclarée mais non atteinte (1297) : branche Lim_θ = 0 ;
- Cnnam(-7 ; 7) du COP air extérieur : 0,50 (Pnom au pivot < 100 kW) ou 0,60 au-delà, Pnom = Pabs x COP au pivot ;
- Typo_Emetteur absent : 3 (émission légère, Dfou0 = 6 min).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .generateurs_ballon import DEQ, _encadrer, _matrice
from .rsee import Noeud

CH, FR = "ch", "fr"
TAUX_DEFAUT = {CH: 0.02, FR: 0.01}                               # (1279), (1280)
LRCONTMIN_DEFAUT, CCP_DEFAUT = 0.4, 1.0                          # (1281), (1282)
DFOU0 = {1: 32.0, 2: 19.0, 3: 6.0, 4: 2.0}                       # minutes, tableau 217 par Typo_Emetteur
PNOM_SEUIL = 100_000.0
MULTISERVICE_PABS_REDUIT = False                                  # voir Pac.heure (1294)                                           # W, bascule du Cnnam(-7 ; 7) air extérieur

# Chaînes de complétion : liste (cible, source, coefficient) ; `av` agit sur la colonne du pivot, `am` sur chaque ligne.
TECHNOS = {
    (CH, 1): dict(aval=(23.5, 32.5, 42.5, 51.0, 60.0), amont=(-15.0, -7.0, 2.0, 7.0, 20.0), pivot=(1, 3), cop_max=3.5,     # air ext / eau, tableaux 152, 153
                  av_cop=[(0, 1, 1.10), (2, 1, 0.8), (3, 2, 0.8), (4, 3, 0.8)], am_cop=[(1, 3, 0.50), (2, 3, 0.80), (4, 3, 1.25), (0, 1, 0.80)],
                  av_pabs=[(0, 1, 1.09), (2, 1, 0.9), (3, 2, 0.915), (4, 3, 0.91)], am_pabs=[(1, 3, 0.86), (2, 3, 0.95), (4, 3, 1.13), (0, 1, 0.92)]),
    (CH, 2): dict(aval=(5.0, 10.0, 15.0, 20.0, 25.0), amont=(-15.0, -7.0, 2.0, 7.0, 20.0), pivot=(3, 3), cop_max=3.5,         # air ext / air recyclé, 155, 156
                  av_cop=[(0, 3, 1.3), (1, 3, 1.20), (2, 3, 1.10), (4, 3, 0.9)], am_cop=[(1, 3, 0.50), (2, 3, 0.80), (4, 3, 1.25), (0, 1, 0.80)],
                  av_pabs=[(0, 3, 1.15), (1, 3, 1.10), (2, 3, 1.05), (4, 3, 0.95)], am_pabs=[(1, 3, 0.86), (2, 3, 0.95), (4, 3, 1.13), (0, 1, 0.92)]),
    (FR, 1): dict(aval=(4.0, 9.5, 15.0, 20.5, 26.0), amont=(5.0, 15.0, 25.0, 35.0, 45.0), pivot=(1, 3), cop_max=2.7,          # air ext / eau, 197, 198
                  av_cop=[(0, 1, 0.9), (2, 1, 1.075), (3, 1, 1.15), (4, 1, 1.225)], am_cop=[(1, 3, 1.4), (2, 3, 1.2), (4, 3, 0.8), (0, 3, 1.6)],
                  av_pabs=[(0, 1, 0.945), (2, 1, 1.055), (3, 1, 1.11), (4, 1, 1.165)], am_pabs=[(1, 3, 1.2), (2, 3, 1.1), (4, 3, 0.9), (0, 3, 1.3)]),
    (FR, 2): dict(aval=(22.0, 27.0, 32.0, 37.0), amont=(5.0, 15.0, 25.0, 35.0, 45.0), pivot=(1, 3), cop_max=2.7,              # air ext / air recyclé, 200, 201
                  av_cop=[(0, 1, 0.9), (2, 1, 1.075), (3, 1, 1.15)], am_cop=[(1, 3, 1.4), (2, 3, 1.2), (4, 3, 0.8), (0, 3, 1.6)],
                  av_pabs=[(0, 1, 0.95), (2, 1, 1.05), (3, 1, 1.1)], am_pabs=[(1, 3, 1.2), (2, 3, 1.1), (4, 3, 0.9), (0, 3, 1.3)]),
}
# correspondances des multiservices et réversibles vers (Sys_thermo_Ch, Sys_thermo_Fr) : tableaux 147, 149, 150
SYS_REV = {1: (1, 1), 2: (2, 2), 3: (3, 3), 4: (5, 4), 5: (7, 5), 6: (6, 6), 7: (4, 7)}
SYS_DOUBLE = {1: (1, None), 2: (4, None), 3: (5, None), 4: (8, None), 5: (2, None)}
SYS_TRIPLE = {1: (1, 1), 2: (4, 7), 3: (5, 4), 5: (2, 2)}


def _completer(m: np.ndarray, techno: dict, cle: str, pivot: tuple[int, int]) -> np.ndarray:
    """Colonne du pivot par les Cnnav (chaîne), puis chaque ligne par les Cnnam ; les valeurs saisies sont gardées (1240 à 1243)."""
    m = m.copy()
    jp = pivot[1]
    for cible, source, c in techno["av_" + cle]:
        if m[cible, jp] == 0:
            m[cible, jp] = m[source, jp] * c
    for i in range(m.shape[0]):
        for cible, source, c in techno["am_" + cle]:
            if m[i, cible] == 0:
                m[i, cible] = m[i, source] * c
    return m


@dataclass
class Mode:
    sys: int
    cop: np.ndarray
    pabs: np.ndarray            # W
    aval: tuple
    amont: tuple
    lim: int
    t_max_aval: float           # chauffage : θaval maximale ; froid : θamont maximale (1298)
    t_min_amont: float          # chauffage : θamont minimale ; froid : θaval minimale
    dfou0: float

    def pleine_charge(self, t_amont: float, t_aval: float) -> tuple[float, float]:
        j1, j2, cam = _encadrer(self.amont, t_amont)
        i1, i2, cav = _encadrer(self.aval, t_aval)

        def bilin(m):
            return (1 - cav) * ((1 - cam) * m[i1, j1] + cam * m[i1, j2]) + cav * ((1 - cam) * m[i2, j1] + cam * m[i2, j2])   # (1287), (1288)
        return bilin(self.pabs), bilin(self.cop)

    def bloque(self, t_amont: float, t_aval: float, mode: str) -> bool:
        if mode == CH:
            a, b = t_amont < self.t_min_amont, t_aval > self.t_max_aval                                            # (1297)
        else:
            a, b = t_amont > self.t_max_aval, t_aval < self.t_min_amont                                            # (1298)
        return (self.lim == 1 and (a or b)) or (self.lim == 2 and a and b)


def _champ(n: Noeud, base: str, sfx: str, defaut):
    """Valeur du champ avec suffixe de mode (_Ch, _Fr) s'il existe, sinon sans suffixe."""
    for k in (base + sfx, base):
        if k in n.valeurs and n.valeurs[k] != "":
            return float(n.valeurs[k]) if not isinstance(defaut, str) else n.valeurs[k]
    return defaut


def _mode(n: Noeud, mode: str, sys: int, sfx: str, perf_cle: str) -> Mode:
    if (mode, sys) not in TECHNOS:
        raise NotImplementedError(f"PAC {mode} de technologie {sys}")
    t = TECHNOS[(mode, sys)]
    nav, nam = len(t["aval"]), len(t["amont"])
    perf = _matrice(n.texte(perf_cle + sfx, n.texte(perf_cle, "")), nav, nam)
    pabs = _matrice(n.texte("Pabs" + sfx, n.texte("Pabs", "")), nav, nam)
    cor = _matrice(n.texte("COR" + sfx, n.texte("COR", "")), nav, nam)
    ip, jp = t["pivot"]
    cop = np.zeros_like(perf)
    if int(_champ(n, "Statut_Donnee", sfx, 1)) == 1:                                                                # (1239)
        cop[cor == 1] = perf[cor == 1]
        cop[cor == 2] = 0.9 * perf[cor == 2]
    else:
        val = _champ(n, "Val_Cop" if mode == CH else "Val_EER", sfx, 0.0)
        cop[ip, jp] = min(0.8 * val, t["cop_max"]) if int(_champ(n, "Statut_Val_Pivot", sfx, 2)) == 1 else 0.8 * t["cop_max"]
        pabs[ip, jp] = _champ(n, "Val_Pabs", sfx, 0.0)
    if cop[ip, jp] == 0:
        cop[ip, jp] = _champ(n, "Val_Cop" if mode == CH else "Val_EER", sfx, 0.0)
    if pabs[ip, jp] == 0:
        pabs[ip, jp] = _champ(n, "Val_Pabs", sfx, 0.0)
    if cop[ip, jp] <= 0 or pabs[ip, jp] <= 0:
        raise NotImplementedError(f"PAC {mode} sans valeur pivot")
    techno = dict(t)
    if mode == CH and sys in (1, 2) and 1000.0 * pabs[ip, jp] * cop[ip, jp] > PNOM_SEUIL:
        techno["am_cop"] = [(1, 3, 0.60) if (c == 1 and s == 3) else (c, s, k) for c, s, k in t["am_cop"]]
    cop = _completer(cop, techno, "cop", (ip, jp))
    pabs = _completer(pabs, techno, "pabs", (ip, jp)) * 1000.0
    typo = int(_champ(n, "Typo_Emetteur", sfx, 3) or 3)
    if mode == CH:
        tmax, tmin = _champ(n, "Theta_Max_Av", sfx, 0.0) or 99.0, _champ(n, "Theta_Min_Am", sfx, 0.0) or -99.0
    else:
        tmax, tmin = _champ(n, "Theta_Max_Am", sfx, 0.0) or 99.0, _champ(n, "Theta_Min_Av", sfx, 0.0) or -99.0
    return Mode(sys, cop, pabs, t["aval"], t["amont"], int(_champ(n, "Lim_Theta", sfx, 0)), tmax, tmin, DFOU0.get(typo, 6.0))


@dataclass
class Pac:
    """Une machine (Rdim exemplaires) et ses modes ; états partagés avec l'ECS d'un multiservice fournis à l'appel."""
    modes: dict
    rdim: int
    waux0: float                # W, auxiliaires à charge nulle (1278)
    fonc_compr: int             # 1 puissance variable, 2 tout ou rien (mode chauffage)
    lr_contmin: float           # mode chauffage
    ccp: float
    multiservice: bool          # double ou triple service : ECS prioritaire (1294, 1295)
    reversible: bool            # froid prioritaire sur le chauffage au même pas (p. 790)
    charge_fr: tuple = (2, LRCONTMIN_DEFAUT, CCP_DEFAUT)   # (Fonc_compr, LRcontmin, Ccp) du mode froid, lus avec le suffixe _Fr

    @classmethod
    def depuis(cls, n: Noeud) -> "Pac":
        nom = n.nom
        if nom.endswith("TripleService"):
            sys_ch, sys_fr = SYS_TRIPLE.get(n.entier("Sys_Thermo_ts", 1), (1, 1)); multi, rev = True, True
        elif nom.endswith("DoubleService"):
            sys_ch, sys_fr = SYS_DOUBLE.get(n.entier("Sys_Thermo_ds", 1), (1, None)); multi, rev = True, False
        elif nom.endswith("Reversible") and "Non" not in nom or nom.endswith("Autre"):
            sys_ch, sys_fr = SYS_REV.get(n.entier("Sys_Thermo_Rev", n.entier("Sys_Thermo", 1)), (1, 1)); multi, rev = False, True
        else:
            sys_ch, sys_fr = n.entier("Sys_Thermo_Ch", n.entier("Sys_Thermo", 1)), None; multi, rev = False, False
        modes = {}
        perf_ch = "COP" if nom.endswith("Autre") else "Performance"
        perf_fr = "EER" if nom.endswith("Autre") else "Performance"
        modes[CH] = _mode(n, CH, sys_ch, "_Ch", perf_ch)
        if sys_fr is not None and (n.texte("Performance_Fr") or n.texte("EER") or n.texte("Pabs_Fr")):
            try:
                modes[FR] = _mode(n, FR, sys_fr, "_Fr", perf_fr)
            except NotImplementedError:
                pass
        sfx = "_Ch"
        taux, statut = _champ(n, "Taux", sfx, TAUX_DEFAUT[CH]), int(_champ(n, "Statut_Taux", sfx, 2))
        taux = {0: taux, 1: 1.1 * taux}.get(statut, TAUX_DEFAUT[CH])                                                # (1278 à 1280)
        ip, jp = TECHNOS[(CH, sys_ch)]["pivot"]
        waux0 = taux * modes[CH].pabs[ip, jp]

        def charge_partielle(sfx):                                                                                   # (1281), (1282) par mode
            fonc = int(_champ(n, "Fonctionnement_Compresseur", sfx, 2) or 2)
            lrm, ccp = LRCONTMIN_DEFAUT, CCP_DEFAUT
            statut_cont = int(_champ(n, "Statut_Fonctionnement_Continu", sfx, 2))
            if statut_cont == 0:
                lrm, ccp = _champ(n, "LRcontmin", sfx, LRCONTMIN_DEFAUT) or LRCONTMIN_DEFAUT, _champ(n, "CCP_LRcontmin", sfx, CCP_DEFAUT) or CCP_DEFAUT
            elif statut_cont == 1:
                lrm, ccp = (_champ(n, "LRcontmin", sfx, LRCONTMIN_DEFAUT) or LRCONTMIN_DEFAUT) + 0.05, 0.9 * (_champ(n, "CCP_LRcontmin", sfx, CCP_DEFAUT) or CCP_DEFAUT)
            return fonc, min(max(lrm, 1e-3), 1.0), ccp
        fonc, lrm, ccp = charge_partielle("_Ch")
        return cls(modes, max(n.entier("Rdim", 1), 1), waux0, fonc, lrm, ccp, multi, rev, charge_partielle("_Fr") if FR in modes else (2, LRCONTMIN_DEFAUT, CCP_DEFAUT))

    def heure(self, mode: str, qreq: float, t_amont: float, t_aval: float, rfonct_ecs: float = 0.0, froid_demande: bool = False,
              part_waux0: float = 1.0) -> dict:
        """Un pas d'un mode : rend fourni, électricité, reste, taux de charge, rejet à la source (Wh, tous exemplaires).
        `part_waux0` : fraction des auxiliaires à charge nulle imputée à ce mode quand la demande est nulle (1325 à 1327)."""
        m = self.modes.get(mode)
        vide = dict(fourni=0.0, elec=0.0, rest=qreq, lr=0.0, rejet=0.0, cop=0.0)
        if m is None:
            return vide
        pabs_pc, cop_pc = m.pleine_charge(t_amont, t_aval)
        pfou_brut = pabs_pc * cop_pc                                                                                 # (1290), (1291)
        if mode == CH and self.reversible and froid_demande:
            pfou_brut = 0.0                                                                                          # froid prioritaire (p. 790)
        if self.multiservice:
            # (1294), (1295) : le temps restant après l'ECS limite la puissance fournie. Le texte ne réduit que Pfou ;
            # pris à la lettre, Pcomp_pc = Pabs_pc - Waux0 (1301, 1306) reste entier et le COP net (1307) tombe au
            # prorata du temps d'ECS (COP 4,86 -> 2,48 à Rfonct 0,5 sur la Loria Duo de cas 06), ce qu'aucune
            # référence ne montre (cas 06 : COP implicite ≈ 4,1 pour 3,5 calculé). Arbitrage : la puissance
            # absorbée à pleine charge est réduite du même facteur, le rendement du compresseur est inchangé.
            # Banc (08/10) : la lettre du texte est exacte sur cas 05 (COP 2,47 = référence, ECS 14,8 pour 10,9 kWh/m²
            # de chauffage) et sur les cinq projets T.ONE triple service (-7 à -9 % avec la lettre, -9 à -12 % avec
            # Pabs réduit) ; la réduction de Pabs n'arrange que cas 06 (+23 -> +2 %) et cas 08 (+20 -> 0 %), dont
            # l'écart a donc une autre cause. Lettre du texte gardée ; MULTISERVICE_PABS_REDUIT reste pour l'étude.
            facteur = max(0.0, 1 - rfonct_ecs) if mode == CH else max(0.0, 1 - rfonct_ecs - 0.25)
            pfou_brut *= facteur
            if MULTISERVICE_PABS_REDUIT:
                pabs_pc *= facteur
        qreq_act = qreq / self.rdim                                                                                  # (1296)
        pfou_pc = 0.0 if m.bloque(t_amont, t_aval, mode) else pfou_brut                                              # (1297), (1298)
        if qreq_act <= 0 or pfou_pc <= 0:
            waux = self.waux0 * part_waux0 * self.rdim                                                               # (1325 à 1327)
            return dict(fourni=0.0, elec=waux, rest=qreq, lr=0.0, rejet=0.0, cop=0.0)
        pfou = min(qreq_act, pfou_pc)                                                                                # (1299)
        lr = pfou / pfou_pc                                                                                          # (1300)
        pcomp_pc = max(pabs_pc - self.waux0, 1e-9)                                                                   # (1301), (1306)
        fonc_compr, lr_contmin, ccp_mode = (self.fonc_compr, self.lr_contmin, self.ccp) if mode == CH else self.charge_fr
        if fonc_compr == 2:
            pcomp = pcomp_pc * lr                                                                                    # (1302)
            pma = pcomp_pc * DEQ * lr * (1 - lr) / m.dfou0                                                           # (1303)
        else:
            lrm = lr_contmin
            cop_net = pfou_brut / pcomp_pc                                                                           # (1307)
            ccp_net = lrm * pcomp_pc * ccp_mode / max(lrm * pabs_pc - ccp_mode * self.waux0, 1e-9)                   # (1308)
            if lr >= lrm:
                pcomp = pfou / (cop_net * (1 + (ccp_net - 1) * (1 - lr) / max(1 - lrm, 1e-9)))                       # (1309), (1310)
                pma = 0.0
            else:
                pcomp_min = pfou_brut * lrm / (cop_net * ccp_net)                                                    # (1313), (1314)
                lrc = lr / lrm                                                                                       # (1316)
                pcomp = pcomp_min * lrc                                                                              # (1315)
                pma = pcomp_min * DEQ * lrc * (1 - lrc) / m.dfou0                                                    # (1317)
        pabs = pcomp + pma + self.waux0                                                                              # (1304), (1311), (1318)
        rejet = min(0.0, pcomp + pma - pfou) if mode == CH else pcomp + pma + pfou                                   # (1333), (1335)
        return dict(fourni=pfou * self.rdim, elec=pabs * self.rdim, rest=(qreq_act - pfou) * self.rdim, lr=lr, rejet=rejet * self.rdim, cop=pfou / pabs)
