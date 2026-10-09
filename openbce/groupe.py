# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Calcul des besoins d'un groupe en mode Th-B (annexe III, fiches 5.7, 5.21, 6.1, 8.1 et 13.1).

PREMIER ASSEMBLAGE, incomplet. Ce qui est conforme au texte : climat, rayonnement, baies, parois, scénarios, modèle
thermique, ventilation conventionnelle du Bbio, émetteur conventionnel. Ce qui est provisoire et marqué comme tel :
  - bilan aéraulique par groupe, sans échange entre groupes ni entrées d'air (fiche 5.6) ;
  - ouverture des baies en gestion manuelle seulement (fiche 5.13) ;
  - volets et stores enroulables seulement ; en gestion automatique, seuils provisoires (voir protections.py).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import baies as mod_baies
from . import aeraulique, brasseurs, distribution, eclairage, emission, ouverture, parois, protections, saisons, thermique, ventilation
from .calendrier import Calendrier
from .climat import Climat
from .rsee import Noeud
from .scenarios import ALPHA_CONV, Scenario

EPSILON_BBIO = 0.5        # efficacité de l'échangeur de la ventilation conventionnelle du Bbio (6.1.3)
CPA_VOL = 0.34            # chaleur volumique de l'air, Wh/(m³.K)
P_CONV = 0.5              # part convective de l'émetteur conventionnel du Bbio (8.1.3)
DEBIT_CONVENTIONNEL = {3: 4.0}     # m³/h par m² de surface de référence, en occupation : bureaux (399)
DEBIT_INOCCUPATION = {3: (60.0, 0.42)}   # en inoccupation : max(60 m³/h ; 0,42 m³/h par m²) (405, 408)
PAS_T = 3.0
T_INTERIEURES = tuple(13.0 + PAS_T * k for k in range(8))     # 13 à 34 °C
FACTEUR_INFILTRATION = 1.0   # sert aux essais de sensibilité du banc
# Cible de la puissance d'émission (803, 808) : la consigne corrigée des dérives θi_eq, ou la consigne brute. Tranché au
# banc (07/10/2026) : en froid la cible corrigée ramène cas 04 de -45 % à -2/-10 % et cas 03 de -33 % à -26 % ; en chaud
# elle dégrade 27 groupes effet joule de ±4 % à +4/+17 %. Revu le 08/10 sur les bureaux de cas 11 (émetteur froid à
# θvt = -2 K par défaut, tableau 88) : cible corrigée 25,7 pour 18,7 au RSEE (+38 %), cible brute 17,1 (-9 %), alors que
# le Th-B du même groupe est juste (17,5 pour 17,3). Le texte (803) écrit θic = θifr, la consigne brute : lecture
# retenue en chaud comme en froid ; le déficit de froid de cas 04 et cas 03 (PAC air/air) a une autre cause.
# Revu encore le 08/10 (voir emission.VT_SAISIE_SEULE) : avec θvt = valeur saisie seule et θvs des tableaux, la cible
# corrigée convient en chaud comme en froid (bureaux +1 %, cas 19 +7 %, cas 04 ≈ 0 attendu) ; les références Th-C
# dépassent leur Th-B de 15 à 57 % exactement sur les groupes dont les émetteurs portent un θvt saisi de 1,8 K.
CIBLE_FROID_CORRIGEE = True
# Essai (08/10) : en Th-C, un groupe climatisé n'ouvre jamais ses baies (et pas seulement en saison de refroidissement) ;
# avant la saison, l'ouverture rafraîchit le groupe et retarde le démarrage de la saison (cas 03 : juin 1,3 pour 6,9).
OUVERTURE_CLIMATISE_JAMAIS = False
# Part des pertes des réseaux du groupe rendue au groupe à l'heure suivante (11.1 : 1,0) ; sert aux essais du banc.
RECUP_RESEAU = 1.0
CIBLE_CHAUD_CORRIGEE = True
P_SD = 0.5                # poids de la température d'air dans la mesure du régulateur (8.1.3)


@dataclass
class ThD:
    """Ce que le mode Th-D (confort d'été, fiche 13.5) ajoute au calcul : la ventilation réelle, les entrées d'air et
    les brasseurs d'air du groupe. Le climat passé à `calculer` doit être celui du jeu Th-D."""
    ventilation: ventilation.Ventilation
    entrees: aeraulique.Fuites
    brasseurs: list[brasseurs.TypeBrasseur]
    volume: float


D_OP_MIN_MAX = 2.0            # °C : la température d'inconfort chaud est plafonnée à consigne + 2 (13.5.3)


@dataclass
class ThC:
    """Mode Th-C (consommations) : ventilation réelle et entrées d'air comme en Th-D, émetteurs équivalents de la
    fiche 8.1, consignes de relance de la fiche 8.5, groupe climatisé ou non (Is_Climatise)."""
    ventilation: ventilation.Ventilation
    entrees: aeraulique.Fuites
    chaud: emission.EmetteurEquivalent
    froid: emission.EmetteurEquivalent
    consigne_ch: np.ndarray       # consigne de chauffage avec relance (max(consigne, relance))
    consigne_fr: np.ndarray
    climatise: bool
    # saisons effectives (fiche 8.4) : autorisations par jour imposées par la génération (union des saisons propres des
    # groupes qu'elle dessert, raccordement permanent) ; None : saisons propres du groupe
    chauffage_impose: np.ndarray | None = None
    refroidissement_impose: np.ndarray | None = None
    # réseaux hydrauliques de chauffage du groupe (fiches 8.7, 8.8) : (ReseauGroupe, part de l'émetteur dans la demande) ;
    # leurs pertes en volume chauffé reviennent en apports internes à l'heure suivante (fiche 11.1, dgr = 1, moitié
    # convective, moitié radiative), de sorte que le besoin calculé est net de ces pertes, comme O_B_Ch des RSEE
    reseaux_chaud: tuple = ()


@dataclass
class Besoins:
    chauffage: np.ndarray       # Wh par heure
    refroidissement: np.ndarray
    eclairage: np.ndarray       # consommation d'éclairage, Wh par heure
    theta_op: np.ndarray
    rprot_moyen: np.ndarray
    saison: np.ndarray          # saison propre du groupe, par jour (tableau 11)
    einat: np.ndarray           # éclairement naturel intérieur, lux
    dh: float = 0.0             # mode Th-D : degrés-heures d'inconfort (2552)
    nb_h_inconfort: tuple[int, int, int] = (0, 0, 0)   # heures au-dessus du seuil, du seuil + 1, du seuil + 2 (2549 à 2551)
    theta_i: np.ndarray | None = None   # température d'air de fin de pas, °C (sert à la distribution d'ECS, 1733)
    etats_reseau: list | None = None    # Th-C : par heure, états des réseaux hydrauliques du groupe (distribution.EtatReseau)
    recup_reseau: np.ndarray | None = None   # Wh : pertes des réseaux rendues au groupe à l'heure suivante


_SAISON_GPM = {saisons.CHAUFFAGE: protections.HIVER, saisons.MI_SAISON: protections.MI_SAISON, saisons.MIXTE: protections.MI_SAISON,
               saisons.REFROIDISSEMENT: protections.ETE}                    # (181)


def calculer(groupe: Noeud, usage: int, climat: Climat, cal: Calendrier, sc: Scenario, b_tampons: dict[int, float], fuites: aeraulique.Fuites,
             thd: ThD | None = None, thc: ThC | None = None) -> Besoins:
    """`thc` : mode Th-C (voir ThC) ; l'éclairage tertiaire y prend les caractéristiques saisies (7.1, Th-C)."""
    surface = groupe.nombre("SHAB") if usage in (1, 2) else groupe.nombre("SU")
    inertie = groupe.un("Inertie")
    lot = [(n, mod_baies.lire(n)) for n in groupe.directs("Baie")]
    g = thermique.Groupe(surface, sum(b.surface for _, b in lot), inertie.nombre("Amq_surf"), inertie.nombre("Cmq_surf"))
    opaques = parois.du_groupe(groupe, climat, b_tampons)
    opaques_e = parois.du_groupe(groupe, climat, b_tampons, ete=True) if thd else opaques
    locaux_ecl = None if usage in (1, 2) else (eclairage.locaux_tertiaires_saisis(groupe) if thc else eclairage.locaux_tertiaires(groupe))
    hgem, n = thermique.hgemq(g, opaques.h), len(climat.te)

    # baies : flux pour la protection relevée et baissée, puis interpolation par Rprot à chaque heure
    ouvert = [mod_baies.flux(b, climat, 0.0) for _, b in lot]
    ferme = [mod_baies.flux(b, climat, 1.0) for _, b in lot]
    ouvert_e = [mod_baies.flux(b, climat, 0.0, ete=True) for _, b in lot] if thd else ouvert
    eclairement = [mod_baies.eclairement(b, climat) for _, b in lot]
    lum_ouvert = [mod_baies.flux_lumineux(b, climat, False) for _, b in lot]
    lum_ferme = [mod_baies.flux_lumineux(b, climat, True) for _, b in lot]
    gpm = []
    for noeud, _ in lot:
        choix = noeud.entier("Choix_PM_GPM", 0)
        store, gestion = protections.decoder(choix) if choix else (False, 0)
        gpm.append((gestion, protections.type_gpm_manu(gestion) if gestion else 0, noeud.entier("Detec_Pres", 0) == 1, noeud.entier("Type_Horl", 0),
                    store, noeud.entier("Prot_Ext", 1) == 1))
    chaud_auto = [False] * len(gpm)

    ouvrants = ouverture.du_groupe(groupe, usage)
    r_ouv = [0.0] * len(ouvrants.baies)
    r_ouv_auto = [0.0] * len(ouvrants.baies)                      # Th-D : hystérésis de la part automatique (246)
    q_occ, q_inocc = groupe.nombre("Qv_occ_BBIO"), groupe.nombre("Qv_inocc_BBIO")
    if usage in DEBIT_CONVENTIONNEL:                                   # non résidentiel : débit d'occupation conventionnel (399 à 401)
        q_occ = DEBIT_CONVENTIONNEL[usage] * surface
        q_inocc = max(DEBIT_INOCCUPATION[usage][0], DEBIT_INOCCUPATION[usage][1] * surface)
    rad_interne = (1 - ALPHA_CONV) * (sc.apports_occupants + sc.apports_usages)
    conv_interne = ALPHA_CONV * (sc.apports_occupants + sc.apports_usages)
    p_test = 10.0 * surface
    # Infiltrations (167, 171, 333). Le bilan de pression dépend de la température intérieure du pas précédent : il
    # est résolu d'avance pour quelques températures intérieures, puis interpolé à chaque heure.
    reel = thd or thc                                                 # ventilation réelle et entrées d'air (Th-C, Th-D)
    if reel:
        h_infiltration = np.array([aeraulique.CPA * aeraulique.air_neuf(fuites, climat.vent, climat.te, climat.we, t, reel.entrees, reel.ventilation.desequilibre)
                                   for t in T_INTERIEURES])
    else:
        h_infiltration = np.array([FACTEUR_INFILTRATION * aeraulique.CPA * aeraulique.air_neuf(fuites, climat.vent, climat.te, climat.we, t) for t in T_INTERIEURES])
    dh, nb_inconf, delta_ba, phi_lent = 0.0, [0, 0, 0], 0.0, 0.0
    lente = None
    if thd:                                                           # inerties séquentielle et annuelle, Th-D seulement (5.21.3.2)
        cms = inertie.nombre("Cms_surf", 0.0) or inertie.nombre("Cmq_surf")
        cma = inertie.nombre("Cma_surf", 0.0) or cms
        lente = thermique.InertieLente(g, inertie.nombre("Ams_surf", inertie.nombre("Amq_surf")), cms, inertie.nombre("Ama_surf", inertie.nombre("Amq_surf")), cma)
    bch, bfr, becl, top, rmoy, einat = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    t_air = np.zeros(n)
    etats_reseau = [] if (thc and thc.reseaux_chaud) else None
    recup_reseau = np.zeros(n) if etats_reseau is not None else None
    recup_prec = 0.0
    mq, top_fin, ti_fin, top_max_jour, top_max_veille = 18.0, 18.0, 18.0, 0.0, 0.0
    hebdo = sc.occupation[:168]                                       # première semaine : semaine type d'occupation (66)
    automate = saisons.Saisons(float(hebdo.sum()), surface, saisons.POIDS_INCONFORT_CHAUD_THC if thc else None)
    jours_saison = np.zeros(n // 24 + 1, dtype=int)
    for h in range(n):
        jour = h // 24
        if h % 24 == 0:                                               # (175)
            top_max_veille, top_max_jour = top_max_jour, 0.0
        top_max_jour = max(top_max_jour, top_fin)
        if cal.case[h] == 10 and h >= 24:                             # 9 h légales : décision des saisons
            automate.nouveau_jour(jour)
            if thc and thc.chauffage_impose is not None:              # saisons effectives (8.4)
                automate.chauffage = bool(thc.chauffage_impose[min(jour, len(thc.chauffage_impose) - 1)])
                automate.refroidissement = bool(thc.refroidissement_impose[min(jour, len(thc.refroidissement_impose) - 1)])
        jours_saison[jour] = automate.saison
        adaptatif = bool(thd) and climat.confort_adaptatif[h] > 0
        if adaptatif:                                                 # Th-D : refroidissement dès le premier jour de confort adaptatif (4.6)
            automate.refroidissement = True
        saison = _SAISON_GPM[automate.saison]
        occupe = sc.occupation[h] > 0
        veille_chaude = adaptatif and top_max_veille >= protections.TOP_LIM_MANU
        d_adapt, conf = 0.0, 0.0
        if thd:
            consigne_fr = float(sc.consigne_fr.min())
            heure_legale = int(cal.case[h]) - 1                       # heure légale de 0 à 23 (case 10 = 9 h, voir saisons)
            inc_max = max(consigne_fr, 0.33 * climat.theta_rm[h] + 18.8 + saisons.D_OP_INC_C1)                  # (2544)
            if usage in (1, 2) and not 6 < heure_legale <= 22:
                conf = consigne_fr                                                                               # (2545) nuit
            else:
                conf = min(consigne_fr + D_OP_MIN_MAX, inc_max)                                                  # (2545), (2546)
            d_adapt = max(0.0, conf - consigne_fr) if adaptatif else 0.0                                         # (2547)
        hges = fs1 = fs2 = fs3 = ftvc = flt1 = flt2 = flt3 = 0.0
        rprot = [0.0] * len(gpm)
        for k, (gestion, r_gpm, detecteur, horloge, store, exterieur) in enumerate(gpm):
            if gestion == 0 or protections.store_remonte(store, exterieur, climat.vent[h]):
                r = 0.0
            elif gestion == 1:
                r, chaud_auto[k] = protections.volet_auto(detecteur, usage, occupe, eclairement[k][h], saison, top_max_veille, top_fin, chaud_auto[k], horloge, store)
            else:
                r = (protections.volet_manuel_thd(r_gpm, usage, occupe, eclairement[k][h], store=store) if veille_chaude
                     else protections.volet_manuel(r_gpm, usage, occupe, eclairement[k][h], saison, top_max_veille, store=store))
            rprot[k] = r
            o, f = (ouvert_e[k] if adaptatif else ouvert[k]), ferme[k]
            hges += (1 - r) * o.hges[h] + r * f.hges[h]
            fs1 += (1 - r) * o.fs1[h] + r * f.fs1[h]
            fs2 += (1 - r) * o.fs2[h] + r * f.fs2[h]
            fs3 += (1 - r) * o.fs3[h] + r * f.fs3[h]
            ftvc += (1 - r) * o.ftvc[h] + r * f.ftvc[h]
            flt1 += (1 - r) * lum_ouvert[k][0][h] + r * lum_ferme[k][0][h]
            flt2 += (1 - r) * lum_ouvert[k][1][h] + r * lum_ferme[k][1][h]
            flt3 += (1 - r) * lum_ouvert[k][2][h] + r * lum_ferme[k][2][h]
            rmoy[h] += r / max(len(gpm), 1)
        if locaux_ecl is None:
            einat[h] = eclairage.eclairement_interieur(flt1, flt2, flt3, surface)
            becl[h] = eclairage.consommation_logement(einat[h], sc.eclairage[h], surface)   # (790)
        elif thc:
            becl[h], einat[h] = eclairage.consommation_tertiaire_saisie(flt1, flt2, flt3, sc.eclairage[h], surface, locaux_ecl)   # (788)
        else:
            becl[h], einat[h] = eclairage.consommation_tertiaire(flt1, flt2, flt3, sc.eclairage[h], surface, locaux_ecl)   # (788)
        conv = conv_interne[h] + eclairage.PART_CONVECTIVE * becl[h] + 0.5 * recup_prec     # (11.1) pertes de réseau de h-1
        rad = rad_interne[h] + (1 - eclairage.PART_CONVECTIVE) * becl[h] + 0.5 * recup_prec
        te = climat.te[h]
        q = q_occ if sc.ventilation[h] > 0 else q_inocc
        k_t = min(max((ti_fin - T_INTERIEURES[0]) / PAS_T, 0.0), len(T_INTERIEURES) - 1.001)
        infiltration = h_infiltration[int(k_t), h] * (1 - k_t % 1) + h_infiltration[int(k_t) + 1, h] * (k_t % 1)
        if reel:                                                      # ventilation réelle : air soufflé après échangeur (378), air neuf par l'enveloppe
            eps_h = reel.ventilation.epsilon_h(te, ti_fin, automate.saison == saisons.CHAUFFAGE)        # bypass (494 à 496)
            hgei = CPA_VOL * reel.ventilation.souffle[h] * (1 - eps_h) + infiltration
        else:
            hgei = CPA_VOL * q * (1 - EPSILON_BBIO) + infiltration                                # (382)
        phi_sh = opaques_e.phi_sh[h] if adaptatif else opaques.phi_sh[h]
        if ouvrants.baies:                                             # surventilation par ouverture des baies (240)
            chauffe = automate.saison == saisons.CHAUFFAGE
            froid_autorise = automate.refroidissement
            heure = int(cal.case[h]) - 1
            consigne_confort = float(sc.consigne_fr.min())             # consigne de refroidissement en occupation
            if thd or thc:
                # Gestion générale (246, 247) en Th-C et Th-D ; le Th-B garde ses règles propres (244, 245). : part dérogée en gestion manuelle (seuils relevés de l'écart de confort
                # adaptatif, 242, 243), part non dérogée en gestion automatique (sans cet écart, écart extérieur-intérieur
                # de 2 °C, ni part d'occupation ni contrainte de bruit) ; en inoccupation, tout est automatique.
                r_ouv = [ouverture.ratio_thermique(top_fin, r, consigne_confort + d_adapt, chauffe) for r in r_ouv]
                r_ouv_auto = [ouverture.ratio_thermique(top_fin, r, consigne_confort, chauffe) for r in r_ouv_auto]
                mod_man = ouverture.moderation_exterieure(te, top_fin, consigne_confort, False) if occupe else 0.0
                mod_auto = ouverture.moderation_exterieure(te, top_fin, consigne_confort, False, ouverture.D_EXT_INT_AUTO)
                p_occ = protections.P_OCC[usage]
                p_nd = ((1 - p_occ) + p_occ * (1 - ouverture.P_DEROG_OUV)) if occupe else 1.0
                ratios = []
                for r_m, r_a, b, auto in zip(r_ouv, r_ouv_auto, ouvrants.baies, ouvrants.automatique):
                    manuel = (1.0 if occupe else 0.0) * p_occ * ouverture.contrainte(b[3], heure, chauffe) * mod_man * r_m
                    ratios.append((1 - p_nd) * manuel + p_nd * mod_auto * r_a if auto else manuel)
            elif occupe:                                               # voir ouverture.py : l'hystérésis vaut jour et nuit
                r_ouv = [ouverture.ratio_thermique(top_fin, r, consigne_confort, chauffe) for r in r_ouv]
                mod = ouverture.moderation_exterieure(te, top_fin, consigne_confort, froid_autorise)
                ratios = [protections.P_OCC[usage] * ouverture.contrainte(b[3], heure, chauffe) * mod * r for r, b in zip(r_ouv, ouvrants.baies)]
            elif not froid_autorise and any(ouvrants.automatique):
                # Hors période de refroidissement, les baies à ouverture automatique restent pilotées en inoccupation
                # (246, 247) : même hystérésis, ouverture si l'air extérieur est plus frais que l'intérieur de
                # D_EXT_INT_AUTO. Le texte dit seulement que le mode Th-B reprend la gestion manuelle « avec quelques
                # différences » ; le banc tranche : sans cette aération, la saison de froid des bureaux démarre le
                # 1er juin (6 kWh/m² de froid en juin, aucun dans les RSEE) ; avec elle, plus aucun froid avant
                # juillet et un besoin annuel à 0,2 à 1,1 kWh/m² des RSEE. En logement, le résultat ne bouge pas.
                r_ouv = [ouverture.ratio_thermique(top_fin, r, consigne_confort, chauffe) for r in r_ouv]
                air_frais = ouverture.SEUIL_BAS < te < top_fin - ouverture.D_EXT_INT_AUTO
                ratios = [r if (air_frais and auto) else 0.0 for r, auto in zip(r_ouv, ouvrants.automatique)]
            else:
                r_ouv = [0.0] * len(r_ouv)                             # (245)
                ratios = r_ouv
            if thc and thc.climatise and (froid_autorise or OUVERTURE_CLIMATISE_JAMAIS):
                # Fiche 5.13 : l'ouverture des baies est incompatible avec le refroidissement ; dans les bâtiments
                # rafraîchis, pas de surventilation naturelle en saison de refroidissement (le Th-B fait exception).
                ratios = [0.0] * len(ratios)
            hgei += aeraulique.CPA * ouvrants.debit(ouvrants.sections(ratios, rprot), climat.vent[h], te, ti_fin)
        x = thermique.Sollicitations(
            hgei=hgei, theta_ei=te, h_opaque=opaques.h, hges=hges,
            theta_es=te + (fs2 + ftvc) / hges if hges > 0 else te,                                   # (342), (343)
            theta_em=te + phi_sh * (1 / hgem + 1 / g.hgmqs) if hgem > 0 else te,                    # (344)
            phi_i=thermique.FSA * fs1 + fs3 + conv,                                       # (346)
            phi_l=g.frl_baies * rad,                                                      # (347)
            phi_mq=g.frmd * (1 - thermique.FSA) * fs1 + g.frm * rad,                      # (348)
            phi_s_leger=g.frs * rad + g.frld * (1 - thermique.FSA) * fs1)
        libre = thermique.pas(g, x, mq, phi_lent=phi_lent)
        if thc:
            # Th-C (8.1) : droite du groupe avec la part convective et la sonde de l'émetteur équivalent sollicité
            # (803 à 808), consignes corrigées des variations et de la relance (801).
            cons_ch = thc.consigne_ch[h] + thc.chaud.correction
            cons_fr = thc.consigne_fr[h] + thc.froid.correction
            em = thc.chaud if _sonde(libre, thc.chaud.psd) < cons_ch else thc.froid
            essai = thermique.pas(g, x, mq, sys_conv=em.pem * p_test, sys_rad=(1 - em.pem) * p_test, phi_lent=phi_lent)
            sd0, sd1 = _sonde(libre, em.psd), _sonde(essai, em.psd)
            pente = (sd1 - sd0) / p_test
            # (803), (808) : la consigne corrigée décide s'il y a besoin ; la puissance vise la consigne non corrigée θic.
            cible_ch = cons_ch if CIBLE_CHAUD_CORRIGEE else thc.consigne_ch[h]
            brut_ch = max((cible_ch - sd0) / pente, 0.0) if (thc.chaud.rat > 0 and sd0 < cons_ch) else 0.0
            cible_fr = cons_fr if CIBLE_FROID_CORRIGEE else thc.consigne_fr[h]
            brut_fr = max((sd0 - cible_fr) / pente, 0.0) if (thc.climatise and thc.froid.rat > 0 and sd0 > cons_fr) else 0.0
            p_conv = em.pem
        else:
            essai = thermique.pas(g, x, mq, sys_conv=P_CONV * p_test, sys_rad=(1 - P_CONV) * p_test, phi_lent=phi_lent)
            sd0, sd1 = _sonde(libre), _sonde(essai)
            pente = (sd1 - sd0) / p_test
            # besoins bruts, sans tenir compte des saisons ; le besoin de froid du Bbio se calcule que le groupe soit
            # climatisé ou non. Ils ne sont fournis au groupe que si la saison l'autorise.
            brut_ch = max((sc.consigne_ch[h] - sd0) / pente, 0.0)
            brut_fr = max((sd0 - sc.consigne_fr[h]) / pente, 0.0)
            p_conv = P_CONV
        c_ch, c_fr = (cons_ch, cons_fr) if thc else (sc.consigne_ch[h], sc.consigne_fr[h])   # Th-C : consignes corrigées (801)
        automate.heure(occupe, libre.op, c_ch, saisons.seuil_inconfort_chaud(c_fr, climat.theta_rm[h]), brut_ch, brut_fr)
        if thd:                                                       # Th-D : groupe non climatisé, chauffage interdit en confort adaptatif (77, 80)
            p = brut_ch if (brut_ch and automate.chauffage and not adaptatif) else 0.0
        else:
            p = brut_ch if (brut_ch and automate.chauffage) else (-brut_fr if (brut_fr and automate.refroidissement) else 0.0)
        t = thermique.pas(g, x, mq, sys_conv=p_conv * p, sys_rad=(1 - p_conv) * p, phi_lent=phi_lent) if p else libre
        fin = thermique.Temperatures(t.mq, t.mq, *thermique.temperatures(g, x, t.mq, p_conv * p, (1 - p_conv) * p))
        mq, top_fin, ti_fin = t.mq, fin.op, fin.i
        if lente is not None:
            phi_lent = lente.avancer(t.mq)
        bch[h], bfr[h], top[h] = max(p, 0.0), max(-p, 0.0), t.op
        t_air[h] = fin.i
        if etats_reseau is not None:                                   # réseaux hydrauliques du groupe sur la demande de l'heure (855 à 881)
            etats = [distribution.reseau_groupe(r, bch[h] * part, fin.i, te, climat.base_ext) for r, part in thc.reseaux_chaud]
            etats_reseau.append(etats)
            recup_prec = RECUP_RESEAU * sum(e.phi_vc for e in etats)
            recup_reseau[h] = recup_prec
        if thd:
            delta_ba = brasseurs.delta_theta_op(thd.brasseurs, usage, occupe, automate.refroidissement, heure_legale, top_fin,
                                                consigne_fr, d_adapt, fin.rm, fin.i, thd.volume)
            if occupe and adaptatif:
                seuil = conf + delta_ba                                                                          # (2548)
                dh += max(0.0, t.op - seuil)                                                                     # (2552)
                for k, marge in enumerate((0.0, 1.0, 2.0)):
                    nb_inconf[k] += int(t.op >= seuil + marge)                                                        # (2549 à 2551)
    return Besoins(bch, bfr, becl, top, rmoy, jours_saison[:n // 24], einat, dh, tuple(nb_inconf), t_air, etats_reseau, recup_reseau)


def _sonde(t: thermique.Temperatures, psd: float = P_SD) -> float:
    """Température vue par le régulateur : moyenne de l'air et de la température radiante, pondérée par Psd (802)."""
    return psd * t.i + (1 - psd) * t.rm
