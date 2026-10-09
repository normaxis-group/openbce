# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Générateurs pour ballon d'ECS (annexe III, fiches 9.13, 9.14, 8.23 partie ECS, 8.18) : pompe à chaleur électrique
en mode ECS (air extérieur, air extrait, air ambiant), appoint à effet joule, et assemblage horaire avec le ballon.

Technologies air (Sys_thermo_Ecs 1 air extérieur, 2 air extrait, 3 air ambiant) ; sources eau, sol et glycolée non
traitées. Température amont (8.26, 1406 à 1408) : air extérieur, air repris du système de ventilation d'extraction
(Tair_extrait, 654), air d'un espace tampon. Pour l'air extrait, la puissance est plafonnée par l'échange à la source
(1292, 1454 à 1456), avec le débit massique de tout le système d'extraction (654) divisé par Rdim.

Charge partielle des CET ECS seule (8.23.3.7.4) : compresseur tout ou rien (Fonc_compr 2, 1301 à 1305) ou à puissance
variable (Fonc_compr 1, 1306 à 1319, LRcontmin et CcpLRcontmin 1281, 1282 par défaut 0,4 et 1). PAC double et triple
service : le mode ECS tourne à pleine charge une fraction du pas (1320 à 1324) ; les auxiliaires à charge nulle ne sont
imputés à l'ECS qu'en dehors des saisons de chauffage et de refroidissement (iECS_seule, p. 796), le mode chauffage ou
froid les portant sinon.

Arbitrages (texte muet, choix de l'implémenteur de référence) :
- Sys_Thermo_ts 5 (triple service « air extérieur avec production ECS ») est lu comme ECS air extérieur/eau (tableau 150) ;
- auxiliaires à charge nulle d'une PAC double ou triple service : Taux_Ch x Pabs pivot du mode chauffage (Val_Pabs_Ch) ;
- le débit d'air extrait n'est pas partagé entre les nb_assembl assemblages identiques de la génération : le banc cas 28
  (Aquacosy sur VMC, 242 m³/h pour 5 CET) le confirme, un partage plafonnerait la machine sous la puissance observée ;
- Tair_Lim lu tel quel dans Source_Amont (0 °C dans les RSEE vus) ;
- pertes du ballon retranchées dans le premier appel (base), pas dans le second (appoint) ;
- température d'ambiance du ballon hors volume chauffé : température extérieure ; air extrait à défaut de simulation : 20 °C.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .ballon import Ballon, RHO_CW, uas_util
from .rsee import Noeud

THETA_AVAL = (5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0)                   # lignes des matrices ECS (tableau 178)
# technologies ECS : colonnes de températures amont, pivot (ligne, colonne), Val_util_max du COP, Cnnam COP et Pabs
TECHNO = {
    1: dict(amont=(-7.0, 2.0, 7.0, 20.0, 35.0), pivot=(4, 2), cop_max=2.7,
            cnnam_cop={0: 0.50, 1: 0.80, 3: 1.25, 4: 1.50}, cnnam_pabs={0: 0.86, 1: 0.95, 3: 1.13, 4: 1.28}),          # tableaux 179, 180
    2: dict(amont=(5.0, 10.0, 15.0, 20.0, 25.0, 30.0), pivot=(4, 3), cop_max=3.2,
            cnnam_cop={0: 0.7, 1: 0.8, 2: 0.9, 4: 1.1, 5: 1.2}, cnnam_pabs={0: 0.85, 1: 0.90, 2: 0.95, 4: 1.05, 5: 1.10}),   # 182, 183
    3: dict(amont=(5.0, 10.0, 15.0, 20.0, 25.0, 30.0), pivot=(4, 2), cop_max=3.1,
            cnnam_cop={0: 0.8, 1: 0.9, 3: 1.1, 4: 1.2, 5: 1.3}, cnnam_pabs={0: 0.85, 1: 0.90, 3: 1.05, 4: 1.10, 5: 1.15}),   # 185 ; 186 : par analogie avec 183
}
CNNAV_COP = {0: 1.8, 1: 1.6, 2: 1.4, 3: 1.2, 5: 0.8, 6: 0.6}             # tableau 179, par ligne (θaval 5 à 65), pivot ligne 4 (45 °C)
CNNAV_PABS = {0: 1.40, 1: 1.30, 2: 1.20, 3: 1.10, 5: 0.90, 6: 0.80}
SYS_TRIPLE = {1: 1, 2: 4, 3: 6, 5: 1}                                     # tableau 150 : Sys_Thermo_ts -> Sys_thermo_Ecs
SYS_DOUBLE = {1: 1, 2: 4, 3: 6, 4: 5, 5: 1}                               # tableau 149
TAUX_DEFAUT = 0.02
DEQ, DFOU0_ECS = 0.5, 26.0                                                # minutes : durée équivalente de démarrage, durée de référence (p. 785, 786)
LRCONTMIN_DEFAUT, CCP_DEFAUT = 0.4, 1.0                                   # (1281), (1282)
CPA, RHO_AIR = 1006.0, 1.2                                                # J/(kg.K), kg/m³ (tableau 244)
AIR_EXTRAIT_DEFAUT = 20.0                                                 # °C, air repris sans simulation thermique


def _matrice(texte: str, lignes: int, colonnes: int) -> np.ndarray:
    m = np.zeros((lignes, colonnes))
    for i, ligne in enumerate(t for t in texte.split(";") if t.strip()):
        vals = [float(v) for v in ligne.split()]
        for j, v in enumerate(vals[:colonnes]):
            if i < lignes:
                m[i, j] = v
    return m


def _completer(m: np.ndarray, pivot: tuple[int, int], cnnav: dict[int, float], cnnam: dict[int, float]) -> np.ndarray:
    """Remplit les cases nulles : colonne du pivot par les Cnnav (1257), puis chaque ligne depuis la colonne du pivot
    par les Cnnam (1258 à 1263) ; les cases saisies sont conservées."""
    m = m.copy()
    ip, jp = pivot
    for i, c in cnnav.items():
        if m[i, jp] == 0:
            m[i, jp] = m[ip, jp] * c
    for i in range(m.shape[0]):
        for j, c in cnnam.items():
            if m[i, j] == 0:
                m[i, j] = m[i, jp] * c
    return m


def _encadrer(grille, x):
    """Indices et poids pour l'interpolation linéaire, bornée aux extrémités de la grille (1284 à 1286)."""
    if x <= grille[0]:
        return 0, 0, 0.0
    if x >= grille[-1]:
        return len(grille) - 1, len(grille) - 1, 0.0
    j = int(np.searchsorted(grille, x)) - 1
    return j, j + 1, (x - grille[j]) / (grille[j + 1] - grille[j])


@dataclass
class PacEcs:
    cop: np.ndarray            # COP utile par (θaval, θamont)
    pabs: np.ndarray           # puissance absorbée à pleine charge, W
    amont: tuple               # grille des températures amont
    sys: int                   # 1 air extérieur, 2 air extrait, 3 air ambiant
    rdim: int
    waux0: float               # auxiliaires à charge nulle, W
    lim: int
    t_max_aval: float
    t_min_amont: float
    tout_ou_rien: bool = False      # charge partielle par cyclage (1301 à 1305), CET ECS seule
    multiservice: bool = False      # double ou triple service : mode ECS à pleine charge une fraction du pas (1320 à 1324)
    lr_contmin: float = LRCONTMIN_DEFAUT
    ccp: float = CCP_DEFAUT
    qm_air_extrait: float = 0.0     # kg/s, machines sur air extrait (654, 1454)
    t_air_lim: float = 0.0          # °C, température minimale de l'air en sortie de source (1455)
    dernier_lr: float = 0.0         # taux de charge du dernier appel : Rfonct_ecs transmis aux modes chauffage et froid (1294, 1295)

    @classmethod
    def depuis(cls, src: Noeud, categorie: str, qm_air_extrait: float = 0.0, t_air_lim: float = 0.0) -> "PacEcs":
        if categorie == "triple":
            sys = SYS_TRIPLE.get(src.entier("Sys_Thermo_ts", 1), 1)
        elif categorie == "double":
            sys = SYS_DOUBLE.get(src.entier("Sys_Thermo_ds", 1), 1)
        else:
            sys = src.entier("Sys_Thermo_Ecs", 1)
        if sys not in TECHNO:
            raise NotImplementedError(f"PAC ECS de technologie {sys} (sources eau, sol, glycolée)")
        t = TECHNO[sys]
        n = len(t["amont"])
        # Les RSEE nomment les champs avec le suffixe _Ecs dans les PAC double et triple service, sans suffixe dans les
        # chauffe-eau thermodynamiques ECS seule (Performance, Pabs, COR, Val_Cop, Lim_Theta, Statut_Donnee...).
        sfx = "" if categorie == "ecs" else "_Ecs"
        perf, pabs, cor = (_matrice(src.texte(k + sfx), 7, n) for k in ("Performance", "Pabs", "COR"))
        ip, jp = t["pivot"]
        cop = np.zeros_like(perf)
        if src.entier("Statut_Donnee" + sfx, 1) == 1:                                           # (1239)
            cop[cor == 1] = perf[cor == 1]
            cop[cor == 2] = 0.9 * perf[cor == 2]
        else:
            pivot = src.nombre("Val_Cop" + sfx, 0.0)
            cop[ip, jp] = min(0.8 * pivot, t["cop_max"]) if src.entier("Statut_Val_Pivot" + sfx, 2) == 1 else 0.8 * t["cop_max"]
            pabs[ip, jp] = src.nombre("Val_Pabs" + sfx, 0.0)
        if cop[ip, jp] == 0 and src.nombre("Val_Cop" + sfx, 0.0):
            cop[ip, jp] = src.nombre("Val_Cop" + sfx)
        if pabs[ip, jp] == 0 and src.nombre("Val_Pabs" + sfx, 0.0):
            pabs[ip, jp] = src.nombre("Val_Pabs" + sfx)
        cop = _completer(cop, (ip, jp), CNNAV_COP, t["cnnam_cop"])
        pabs = _completer(pabs, (ip, jp), CNNAV_PABS, t["cnnam_pabs"]) * 1000.0                # kW -> W
        lr_contmin, ccp = LRCONTMIN_DEFAUT, CCP_DEFAUT
        if categorie == "ecs":
            taux, statut = src.nombre("Taux", TAUX_DEFAUT), src.entier("Statut_Taux", 2)
            pabs_ref = pabs[ip, jp]
            tout_ou_rien = src.entier("Fonctionnement_Compresseur", 2) == 2
            statut_cont = src.entier("Statut_Fonctionnement_Continu", 2)
            if statut_cont == 0:                                                                 # certifié : tel quel
                lr_contmin, ccp = src.nombre("LRcontmin", LRCONTMIN_DEFAUT), src.nombre("CCP_LRcontmin", CCP_DEFAUT)
            elif statut_cont == 1:                                                               # justifié : +0,05 et x0,9
                lr_contmin, ccp = src.nombre("LRcontmin", LRCONTMIN_DEFAUT) + 0.05, 0.9 * src.nombre("CCP_LRcontmin", CCP_DEFAUT)
        else:
            taux, statut = src.nombre("Taux_Ch", TAUX_DEFAUT), src.entier("Statut_Taux_Ch", 2)
            pabs_ref = 1000.0 * (src.nombre("Val_Pabs_Ch", 0.0) or pabs[ip, jp] / 1000.0)
            tout_ou_rien = False
        taux = {0: taux, 1: 1.1 * taux}.get(statut, TAUX_DEFAUT)                                # (1278 à 1280)
        return cls(cop, pabs, t["amont"], sys, max(src.entier("Rdim", 1), 1), taux * pabs_ref, src.entier("Lim_Theta" + sfx, 0),
                   src.nombre("Theta_Max_Av" + sfx, 0.0) or 90.0, src.nombre("Theta_Min_Am" + sfx, 0.0) or -99.0, tout_ou_rien,
                   categorie != "ecs", min(max(lr_contmin, 1e-3), 1.0), ccp, qm_air_extrait, t_air_lim)

    def pleine_charge(self, t_amont: float, t_aval: float) -> tuple[float, float]:
        """(Pabs, COP) à pleine charge aux températures de fonctionnement, interpolation bilinéaire bornée (1284 à 1288)."""
        j1, j2, cam = _encadrer(self.amont, t_amont)
        i1, i2, cav = _encadrer(THETA_AVAL, t_aval)

        def bilin(m):
            return ((1 - cav) * ((1 - cam) * m[i1, j1] + cam * m[i1, j2]) + cav * ((1 - cam) * m[i2, j1] + cam * m[i2, j2]))
        return bilin(self.pabs), bilin(self.cop)

    def heure(self, qreq: float, t_amont: float, t_aval: float, ecs_seule: bool = True) -> tuple[float, float]:
        """Mode ECS d'une PAC (1296 à 1328) : rend (énergie fournie, électricité), Wh. `ecs_seule` : hors saisons de
        chauffage et de refroidissement (iECS_seule), seules heures où une PAC multiservice impute ses auxiliaires à
        charge nulle à l'ECS (p. 796)."""
        qreq_act = qreq / self.rdim                                                                # (1296)
        pabs_pc, cop_pc = self.pleine_charge(t_amont, t_aval)
        bloque = (self.lim == 1 and (t_amont < self.t_min_amont or t_aval > self.t_max_aval)) or \
                 (self.lim == 2 and t_amont < self.t_min_amont and t_aval > self.t_max_aval)        # (1297)
        pfou_pc = 0.0 if bloque else pabs_pc * cop_pc                                              # (1290)
        if pfou_pc > 0 and self.sys == 2 and self.qm_air_extrait > 0 and pfou_pc > pabs_pc:
            pech = self.qm_air_extrait / self.rdim * CPA * max(0.0, t_amont - self.t_air_lim)      # (1454), (1455)
            pfou_pc = min(pfou_pc, pech * pfou_pc / (pfou_pc - pabs_pc))                           # (1456), (1292)
        waux0 = self.waux0 if (ecs_seule or not self.multiservice) else 0.0
        self.dernier_lr = 0.0
        if qreq_act <= 0 or pfou_pc <= 0:
            return 0.0, waux0 * self.rdim                                                          # (1325)
        pfou = min(qreq_act, pfou_pc)                                                              # (1299)
        lr = pfou / pfou_pc                                                                        # (1300)
        self.dernier_lr = lr
        pcomp_pc = max(pabs_pc - self.waux0, 1e-9)                                                 # (1301), (1306)
        if self.multiservice:
            pabs = pabs_pc * lr + (1 - lr) * waux0                                                 # (1320 à 1324) : pleine charge une fraction du pas
        elif self.tout_ou_rien:                                                                    # (1301 à 1305)
            pabs = pcomp_pc * lr + pcomp_pc * DEQ * lr * (1 - lr) / DFOU0_ECS + self.waux0
        else:                                                                                      # puissance variable (1306 à 1319)
            lrm = self.lr_contmin
            cop_net = pfou_pc / pcomp_pc                                                           # (1307)
            ccp_net = lrm * pcomp_pc * self.ccp / max(lrm * pabs_pc - self.ccp * self.waux0, 1e-9)  # (1308)
            if lr >= lrm:
                cop_lr_net = cop_net * (1 + (ccp_net - 1) * (1 - lr) / max(1 - lrm, 1e-9))         # (1309)
                pabs = pfou / cop_lr_net + self.waux0                                              # (1310), (1311)
            else:
                pcomp_min = pfou_pc * lrm / (cop_net * ccp_net)                                    # (1313), (1314)
                lr_cycl = lr / lrm                                                                 # (1316)
                pabs = pcomp_min * lr_cycl + pcomp_min * DEQ * lr_cycl * (1 - lr_cycl) / DFOU0_ECS + self.waux0   # (1315), (1317), (1318)
        return pfou * self.rdim, pabs * self.rdim                                                  # (1328)


@dataclass
class Joule:
    pmax: float               # W

    def heure(self, qreq: float, *_) -> tuple[float, float]:
        qfou = min(qreq, self.pmax)                                                                # (1068)
        return qfou, qfou


@dataclass
class ChaudiereBallon:
    """Chaudière gaz ou fioul en base ou appoint d'un ballon (Source_Ballon_Base_Combustion, _Appoint_Combustion) : fiche
    8.19 en mode ECS seule, à la température de la zone d'échange ; le gaz est rendu à part de l'électricité."""
    chaudiere: object
    dernier_gaz: float = 0.0

    @classmethod
    def depuis(cls, n: Noeud, pos_gen: int) -> "ChaudiereBallon":
        from .chaudiere import Chaudiere
        from .reseau_fourniture import ReseauFourniture
        if "Reseau_Fourniture" in n.nom:
            obj = cls(ReseauFourniture.depuis(n))
            obj.chaudiere.pos_gen = pos_gen
            return obj
        return cls(Chaudiere.depuis(n, pos_gen))

    def heure(self, qreq: float, t_amont: float = 0.0, t_aval: float = 55.0, ecs_seule: bool = True) -> tuple[float, float]:
        r = self.chaudiere.appeler(qreq, 0.0, t_aval, t_aval, 20.0 if self.chaudiere.pos_gen == 1 else t_amont, ecs_seule)
        self.dernier_gaz = float(r.qcef[:, [1, 3, 0]].sum()) if False else float(r.qcef.sum() - r.waux)   # énergies hors électricité
        return r.qfou, r.waux


@dataclass
class AssemblageECS:
    """Un ballon et ses générateurs (base, appoint), répété nb fois (9.14)."""
    ballon: Ballon
    base: PacEcs | Joule
    appoint: object | None      # Joule ou ChaudiereBallon
    nb: int
    pos_gen: int
    ballon_base: Ballon | None = None   # Type_prod_stockage 2 : ballon principal (base) en amont du ballon d'appoint (9.14)

    @classmethod
    def depuis(cls, ps: Noeud, pos_gen: int, qm_air_extrait: float = 0.0, t_air_lim: float = 0.0) -> "AssemblageECS":
        base = appoint = None
        for c in ps.enfants:
            if c.nom.startswith("Source_Ballon_Base_Thermodynamique_Elec"):
                cat = "triple" if c.nom.endswith("TripleService") else ("double" if c.nom.endswith("DoubleService") else "ecs")
                base = PacEcs.depuis(c, cat, qm_air_extrait, t_air_lim)
            elif c.nom == "Source_Ballon_Base_Effet_Joule":
                base = Joule(1000.0 * c.nombre("Pmax", 0.0) * max(c.entier("Rdim", 1), 1))
            elif c.nom == "Source_Ballon_Appoint_Effet_Joule":
                appoint = Joule(1000.0 * c.nombre("Pmax", 0.0) * max(c.entier("Rdim", 1), 1))
            elif c.nom in ("Source_Ballon_Base_Combustion", "Source_Ballon_Base_Reseau_Fourniture"):
                base = ChaudiereBallon.depuis(c, pos_gen)
            elif c.nom == "Source_Ballon_Appoint_Combustion":
                appoint = ChaudiereBallon.depuis(c, pos_gen)
            elif c.nom.startswith("Source_Ballon"):
                raise NotImplementedError(f"source de ballon {c.nom}")
        if base is None:
            raise NotImplementedError("ballon sans générateur de base reconnu")
        ballon_base = None
        if ps.entier("Type_prod_stockage", 0) == 2 and ps.nombre("V_tot_appoint", 0.0) > 0:
            # deux ballons en série : le principal (V_tot, chauffé par la base) alimente le secondaire (V_tot_appoint, chauffé
            # par l'appoint) d'où l'eau est puisée ; le secondaire est décrit par les champs *_appoint
            ballon_base = Ballon.depuis(ps, pos_gen)
            ballon_base.v = [ps.nombre("V_tot") / 4] * 4
            ballon_base.u = [uas_util(ps) / 4] * 4
            secondaire = Noeud(ps.nom, dict(ps.valeurs), [])
            secondaire.valeurs.update({"V_tot": ps.texte("V_tot_appoint"), "UA_S": ps.texte("UA_S_appoint"), "Nature_Ballon": ps.texte("Nature_Ballon_Appoint") or ps.texte("Nature_Ballon"),
                                       "Valeur_Certifiee_Justifiee_Defaut": ps.texte("Valeur_Certifiee_Justifiee_Defaut_Appoint") or ps.texte("Valeur_Certifiee_Justifiee_Defaut"),
                                       "Theta_Max": ps.texte("Theta_Max_appoint") or ps.texte("Theta_Max"), "Type_prod_stockage": "0"})
            ballon = Ballon.depuis(secondaire, pos_gen)
            return cls(ballon, base, appoint, max(ps.entier("nb_assembl", 1), 1), pos_gen, ballon_base)
        return cls(Ballon.depuis(ps, pos_gen), base, appoint, max(ps.entier("nb_assembl", 1), 1), pos_gen)

    def _heure_deux_ballons(self, qreq_ecs, t_eau_froide, t_depart, t_ext, heure_legale, ecs_seule, t_air_extrait, t_tampon) -> dict:
        """Type_prod_stockage 2 : puisage dans le ballon d'appoint, alimenté par le haut du ballon principal, lui-même
        alimenté en eau froide ; la base chauffe le principal, l'appoint le secondaire."""
        bb, ba = self.ballon_base, self.ballon
        t_amb = 20.0 if self.pos_gen == 1 else t_ext
        t_amont = t_ext
        if isinstance(self.base, PacEcs) and self.base.sys == 2:
            t_amont = AIR_EXTRAIT_DEFAUT if t_air_extrait is None else t_air_extrait
        elif isinstance(self.base, PacEcs) and self.base.sys == 3:
            t_amont = t_ext if t_tampon is None else t_tampon
        pertes_b, pertes_a = bb.pertes(t_amb), ba.pertes(t_amb)
        # puisage en série (1794 à 1800 sur l'ensemble) : l'énergie utile se compte depuis l'eau froide, le volume puisé
        # traverse les deux ballons (le principal reçoit l'eau froide, le secondaire le haut du principal)
        from .ballon import NB_ITER
        restant, vp, fourni = qreq_ecs / self.nb + ba.report, 0.0, 0.0
        vmin = min(ba.v)                                                        # le secondaire, d'où l'on puise, fixe la tranche
        for _ in range(NB_ITER):
            if restant <= 0:
                break
            haut = ba.theta[-1]
            if haut <= t_depart or haut - t_eau_froide <= 1e-6:
                break
            v = min(restant / (RHO_CW * (haut - t_eau_froide)), vmin)
            energie = RHO_CW * v * (haut - t_eau_froide)
            fourni += energie; restant -= energie; vp += v
            entrant = bb.theta[-1]
            ba.decaler(v, entrant)
            bb.decaler(v, t_eau_froide)
        ba.report = max(restant, 0.0)
        ba.nbh_report = ba.nbh_report + 1 if ba.report > 0 else ba.nbh_report
        gaz = 0.0
        q_base = bb.demande_chauffe(bb.z_base, bb.z_reg_base, bb.d_theta_base, bb.gestion_base, heure_legale, vp > 0, pertes_b)
        t_aval = 0.5 * (bb.theta[bb.z_base - 1] + bb.theta_prec[bb.z_base - 1])
        if isinstance(self.base, PacEcs):
            qfou_b, elec_b = self.base.heure(q_base, t_amont, t_aval, ecs_seule)
        elif isinstance(self.base, ChaudiereBallon):
            qfou_b, elec_b = self.base.heure(q_base, t_ext, t_aval, ecs_seule); gaz += self.base.dernier_gaz
        else:
            qfou_b, elec_b = self.base.heure(q_base)
        bb.injecter(bb.z_base, qfou_b, pertes_b)
        elec_a = 0.0
        if self.appoint is not None:
            q_ap = ba.demande_chauffe(ba.z_base, ba.z_reg_base, ba.d_theta_ap, ba.gestion_ap, heure_legale, vp > 0, pertes_a)
            if isinstance(self.appoint, ChaudiereBallon):
                qfou_a, elec_a = self.appoint.heure(q_ap, t_ext, ba.theta[0], ecs_seule); gaz += self.appoint.dernier_gaz
            else:
                qfou_a, elec_a = self.appoint.heure(q_ap)
            ba.injecter(ba.z_base, qfou_a, pertes_a)
        else:
            ba.injecter(1, 0.0, pertes_a)
        bb.cloturer(); ba.cloturer()
        return dict(fourni=fourni * self.nb, non_fourni=ba.report * self.nb, elec=(elec_b + elec_a) * self.nb,
                    pertes=(sum(pertes_b) + sum(pertes_a)) * self.nb, theta_haut=ba.theta[-1], gaz=gaz * self.nb)

    def heure(self, qreq_ecs: float, t_eau_froide: float, t_depart: float, t_ext: float, heure_legale: int,
              ecs_seule: bool = True, t_air_extrait: float | None = None, t_tampon: float | None = None) -> dict:
        """Une heure de l'assemblage : puisage, base, appoint ; rend fourni, non fourni, électricité (Wh, tous ballons).
        Température amont selon la source (1406 à 1408) : air extérieur, air repris du système d'extraction, espace tampon."""
        if self.ballon_base is not None:
            return self._heure_deux_ballons(qreq_ecs, t_eau_froide, t_depart, t_ext, heure_legale, ecs_seule, t_air_extrait, t_tampon)
        b = self.ballon
        t_amb = 20.0 if self.pos_gen == 1 else t_ext
        t_amont = t_ext
        if isinstance(self.base, PacEcs) and self.base.sys == 2:
            t_amont = AIR_EXTRAIT_DEFAUT if t_air_extrait is None else t_air_extrait
        elif isinstance(self.base, PacEcs) and self.base.sys == 3:
            t_amont = t_ext if t_tampon is None else t_tampon
        pertes = b.pertes(t_amb)
        fourni, vp = b.puiser(qreq_ecs / self.nb, t_eau_froide, t_depart)
        puise = vp > 0
        # base (1811 à 1816, 1946, 1947)
        q_base = b.demande_chauffe(b.z_base, b.z_reg_base, b.d_theta_base, b.gestion_base, heure_legale, puise, pertes)
        t_aval = b.theta[b.z_base - 1] if b.theta else 50.0                                        # (1784) : θ moyenne de la zone d'échange
        gaz = 0.0
        if isinstance(self.base, PacEcs):
            qfou_b, elec_b = self.base.heure(q_base, t_amont, 0.5 * (t_aval + b.theta_prec[b.z_base - 1]), ecs_seule)
        elif isinstance(self.base, ChaudiereBallon):
            qfou_b, elec_b = self.base.heure(q_base, t_ext, 0.5 * (t_aval + b.theta_prec[b.z_base - 1]), ecs_seule)
            gaz += self.base.dernier_gaz
        else:
            qfou_b, elec_b = self.base.heure(q_base)
        b.injecter(b.z_base, qfou_b, pertes)
        elec_a = 0.0
        if self.appoint is not None:
            q_ap = b.demande_chauffe(b.z_ap, b.z_reg_ap, b.d_theta_ap, b.gestion_ap, heure_legale, puise, [0.0] * 4)
            if isinstance(self.appoint, ChaudiereBallon):
                qfou_a, elec_a = self.appoint.heure(q_ap, t_ext, b.theta[b.z_ap - 1], ecs_seule)
                gaz += self.appoint.dernier_gaz
            else:
                qfou_a, elec_a = self.appoint.heure(q_ap)
            b.injecter(b.z_ap, qfou_a, None)
        b.cloturer()
        return dict(fourni=fourni * self.nb, non_fourni=b.report * self.nb, elec=(elec_b + elec_a) * self.nb,
                    pertes=sum(pertes) * self.nb, theta_haut=b.theta[-1], gaz=gaz * self.nb)


def debit_air_extrait(entree: Noeud, gen: Noeud) -> tuple[float, float]:
    """(débit massique d'air extrait en kg/s, Tair_Lim) du système d'extraction raccordé à la source amont de la
    génération (Source_Amont_Air 3, Id_SF_Extraction) : somme des débits repris de base des bouches rattachées au
    système (654, débit conventionnel de base faute de simulation de la ventilation) ; (0, 0) sans source air extrait."""
    for sa in gen.tous("Source_Amont"):
        if sa.entier("Source_Amont_Air", 0) == 3 and sa.entier("Id_SF_Extraction", 0) > 0:
            id_sf = sa.entier("Id_SF_Extraction")
            qv = sum(bc.nombre("Qv_rep_base", 0.0) for bc in entree.tous("Bouche_Conduit") if bc.entier("Id_Systeme_Mecanique", 0) == id_sf)
            return qv / 3600.0 * RHO_AIR, sa.nombre("Tair_Lim", 0.0)
    return 0.0, 0.0

