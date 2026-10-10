# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Émission équivalente du groupe en mode Th-C (annexe III, fiche 8.1) et relances (fiche 8.5).

L'émetteur équivalent de chaud (et de froid) est la moyenne, pondérée par les parts Rat = Rat_s x Rat_t (797, 798),
des caractéristiques des émetteurs du groupe (799) : part convective Pem (tableaux 86, 87), sonde Psd (0,5), variation
spatiale θvs (tableaux 83, 85 selon la classe et la hauteur sous plafond), variation temporelle θvt (saisie ou tableau
88), détection de présence (800 : -0,15 K). Les consignes corrigées (801) sont : chauffage = max(consigne, consigne de
relance) + θvs + θvt + θprésence ; refroidissement = min(consigne, relance) + θvs + θvt (θvt négatif en froid).

Correspondances des codes des RSEE, déduites des noms d'émetteurs du banc (le texte ne les donne pas) :
Typologie_Emetteur_Chaud 1 soufflage d'air, 2 émetteur mural rayonnant, 3 plancher chauffant, 4 mur ou plafond
rayonnant, 5 plafond chauffant ; Classe_Variation_Spatiale_Chaud 1 A, 2 B1, 3 B2, 4 B3, 5 C ; Carac_Haut_Plafond 0 à 3
pour les quatre colonnes de hauteur. PREMIER JET : pertes au dos lues (Per_dos), ventilateurs locaux ignorés.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rsee import Noeud

PEM_CHAUD = {0: 0.0, 1: 0.95, 2: 0.70, 3: 0.50, 4: 0.35, 5: 0.20}            # tableau 86
PEM_FROID = {0: 0.0, 1: 0.95, 2: 0.80, 3: 0.50, 4: 0.35, 5: 0.20}            # tableau 87
# tableau 83 : θvs en chauffage par classe (A, B1, B2, B3, C) et hauteur sous plafond (< 4, 4 à 6, 6 à 8, > 8 m)
VS_CHAUD = {1: (0.0, 0.0, 0.0, 0.0), 2: (0.0, 0.0, 0.5, 1.0), 3: (0.0, 0.6, 1.7, 2.8), 4: (0.2, 0.8, 1.2, 1.6), 5: (0.4, 1.2, 2.0, 2.8)}
VS_FROID = {1: (0.0, 0.4, 0.8, 1.2), 2: (0.0, 0.2, 0.4, 0.6), 3: (0.0, 0.0, 0.0, 0.0)}   # tableau 85 : A, B, C
VT_DEFAUT_CHAUD = {0: 2.0, 1: 1.8}            # tableau 88 : sans arrêt total, avec arrêt total
VT_DEFAUT_FROID = {0: -2.0, 1: -1.8}
D_PRESENCE = -0.15                            # θpresence_ch (nomenclature 8.1)
PSD = 0.5
# relances (tableaux 93, 94) : durées en heures (inoccupation courte, prolongée) ; optimiseur : 0 à 3 h selon θext
RELANCE_CHAUD = {1: (2, 6), 2: (2, 4), 3: (1, None)}
RELANCE_FROID = {1: (1, 3), 2: (1, 2), 3: (0, 0)}
THETA_EXT_REG_SUP = 15.0


@dataclass(frozen=True)
class EmetteurEquivalent:
    rat: float            # somme des parts (≤ 1 ; 0 : pas d'émetteur)
    pem: float            # part convective
    psd: float
    d_vs: float
    d_vt: float
    d_presence: float
    pertes_dos: float     # Pper de l'émetteur équivalent (moyenne pondérée, premier jet)

    @property
    def correction(self) -> float:
        return self.d_vs + self.d_vt + self.d_presence


# Lecture des variations tranchée au banc (08/10/2026), contraire à la lettre du texte : θvt est la valeur saisie
# Delta_Temp_vt_* telle quelle (pas de + 0,5 K de statut justifié, pas de défaut du tableau 88 quand elle vaut 0) et
# θvs vient des tableaux 83/85 par classe (le champ Delta_Temp_vs_* saisi est ignoré), les cibles de puissance étant
# les consignes corrigées (groupe.CIBLE_*_CORRIGEE). Mesures : bureaux cas 11 (vs saisi 1,8, vt 0 statut 2) chauffage
# 36,4/36,2 ainsi, 48,6 avec le vs saisi, 62,8 avec le défaut de vt ; cas 19 (vt 1,8 sur 6 émetteurs) 26,9/25,2 ainsi,
# 20,5 avec la cible brute, 29,0 avec + 0,5 K ; cas 04 : 39,7 attendu, -13 % en brute, +13 % avec + 0,5 K.
# Précision du même jour sur le lot (1 772 émetteurs de chauffage) : Delta_Temp_vt_ch vaut 1,8 ou 2,0 (les défauts du
# tableau 88) exactement quand Statut_Variation_Temporelle vaut 2, et 0,1 à 1,4 avec le statut 0 ; les groupes à
# émetteurs de statut 0 (effet joule 0,2 K, cas 18, cas 03) sont justes avec la cible brute et passent à +7/+13 % dès
# qu'on leur applique 0,2 à 0,4 K. Lecture retenue : la correction θvt n'est appliquée que pour le statut 2 (valeur
# par défaut), avec la valeur écrite ; θvs n'est pas appliqué (bureaux : +1 % sans, +34 % avec le 1,8 saisi).
VT_SAISIE_SEULE = True
VS_IGNORE = True


def _vt(e: Noeud, chaud: bool) -> float:
    cle = "Delta_Temp_vt_ch" if chaud else "Delta_Temp_vt_fr"
    statut = e.entier("Statut_Variation_Temporelle_Chaud" if chaud else "Statut_Variation_Temporelle_Froid", 0)
    saisie = e.nombre(cle, 0.0)
    if VT_SAISIE_SEULE:
        return saisie if statut == 2 else 0.0
    if saisie:
        return saisie + (0.5 if statut == 2 else 0.0) * (1 if chaud else -1)      # valeur justifiée : + 0,5 K
    arret = e.entier("Couple_Regulateur_Emetteur_Chaud" if chaud else "Couple_Regulateur_Emetteur_Froid", 0)
    return (VT_DEFAUT_CHAUD if chaud else VT_DEFAUT_FROID).get(arret, 2.0 if chaud else -2.0)


def equivalent(groupe: Noeud, chaud: bool = True) -> EmetteurEquivalent:
    suffixe = "ch" if chaud else "fr"
    emetteurs = [e for e in groupe.directs("Emetteur") if e.entier("Is_emetteur_chaud" if chaud else "Is_emetteur_froid", 0) == 1]
    rats = [e.nombre(f"Rat_s_{suffixe}", 0.0) * e.nombre(f"Rat_t_{suffixe}", 1.0) for e in emetteurs]
    total = sum(rats)
    if total <= 0:
        return EmetteurEquivalent(0.0, 0.5, PSD, 0.0, 0.0, 0.0, 0.0)
    pem = d_vs = d_vt = d_pres = pper = 0.0
    for e, r in zip(emetteurs, rats):
        w = r / total                                                              # (798)
        typo = e.entier("Typologie_Emetteur_Chaud" if chaud else "Typologie_Emetteur_Froid", 1)
        p = e.nombre(f"Pem_conv_{suffixe}", 0.0) or (PEM_CHAUD if chaud else PEM_FROID).get(typo, 0.5)
        vs = e.nombre(f"Delta_Temp_vs_{suffixe}", 0.0)
        if VS_IGNORE:
            vs = 0.0
        elif not vs:
            classe = e.entier("Classe_Variation_Spatiale_Chaud" if chaud else "Classe_Variation_Spatiale_Froid", 5 if chaud else 3)
            colonne = min(max(e.entier("Carac_Haut_Plafond", 0), 0), 3)
            vs = (VS_CHAUD if chaud else VS_FROID).get(classe, (0.0,) * 4)[colonne]
        pem += w * p
        d_vs += w * vs
        d_vt += w * _vt(e, chaud)
        d_pres += w * (D_PRESENCE if (chaud and e.entier("detection_presence", 0) == 1) else 0.0)
        pper += w * e.nombre("Per_dos", 0.0)
    return EmetteurEquivalent(min(total, 1.0), pem, PSD, d_vs, d_vt, d_pres, pper)


SEUIL_VCV_CH = 20.0           # Wh/m², besoin de chauffage à partir duquel le ventilo-convecteur passe en moyenne vitesse (p. 507)
SEUIL_VCV_FR = 20.0           # Wh/m², idem en froid (seuil écrit -20 sur un besoin négatif)


@dataclass
class VentilateurLocal:
    """Ventilateurs d'un émetteur à recyclage d'air (ventilo-convecteur, split) : fiche 8.1, 811 à 813, Th-C seulement.
    `gest` : 1 manuelle (marche permanente, régime choisi au premier pas d'occupation), 2 automatique à marche permanente
    (super petite vitesse sans besoin si l'appareil en dispose), 3 automatique avec arrêt sans besoin. En relance, grande
    vitesse. Actifs seulement pendant les saisons de fonctionnement de l'émetteur (811)."""
    gest: int
    spv: bool
    p_gv: float
    p_mv: float
    p_pv: float
    p_spv: float
    chaud: bool
    froid: bool
    w_ch: float               # part de l'émetteur dans la demande de chauffage du groupe (798)
    w_fr: float
    etat: float = 0.0         # W : dernier régime (gestion manuelle)

    def heure(self, bch: float, bfr: float, surface: float, occupe: bool, occupe_prec: bool, relance: bool, aut_ch: bool, aut_fr: bool) -> float:
        """Puissance des ventilateurs locaux à cette heure, W (= Wh). `bch`, `bfr` : besoins du groupe de l'heure, Wh."""
        if self.gest <= 0 or not ((self.chaud and aut_ch) or (self.froid and aut_fr)):                     # (811)
            self.etat = 0.0
            return 0.0
        q_ch = bch * self.w_ch if (self.chaud and aut_ch) else 0.0
        q_fr = bfr * self.w_fr if (self.froid and aut_fr) else 0.0
        besoin = q_ch > 0 or q_fr > 0
        moyenne = q_ch > self.w_ch * surface * SEUIL_VCV_CH or q_fr > self.w_fr * surface * SEUIL_VCV_FR
        if relance:
            self.etat = self.p_gv
        elif self.gest == 1:                                                                               # (812) manuelle
            if occupe and not occupe_prec:
                self.etat = self.p_mv if moyenne else self.p_pv
            elif self.etat <= 0:
                self.etat = self.p_pv
        elif self.gest == 2:
            self.etat = (self.p_spv if self.spv else self.p_pv) if not besoin else (self.p_mv if moyenne else self.p_pv)
        else:
            self.etat = 0.0 if not besoin else (self.p_mv if moyenne else self.p_pv)
        return self.etat


def ventilateurs_locaux(groupe: Noeud) -> list[VentilateurLocal]:
    """Ventilateurs locaux des émetteurs du groupe (Gest_vcv > 0), avec leur part dans les demandes de chaud et de froid."""
    ems = groupe.directs("Emetteur")
    tot_ch = sum(e.nombre("Rat_s_ch", 0.0) * e.nombre("Rat_t_ch", 1.0) for e in ems if e.entier("Is_emetteur_chaud", 0) == 1) or 1.0
    tot_fr = sum(e.nombre("Rat_s_fr", 0.0) * e.nombre("Rat_t_fr", 1.0) for e in ems if e.entier("Is_emetteur_froid", 0) == 1) or 1.0
    out = []
    for e in ems:
        gest = e.entier("Gest_vcv", 0)
        if gest <= 0:
            continue
        chaud, froid = e.entier("Is_emetteur_chaud", 0) == 1, e.entier("Is_emetteur_froid", 0) == 1
        out.append(VentilateurLocal(gest, e.entier("I_spv", 0) == 1, e.nombre("P_VCV_gv", 0.0), e.nombre("P_VCV_mv", 0.0), e.nombre("P_VCV_pv", 0.0),
                                    e.nombre("P_VCV_spv", 0.0), chaud, froid,
                                    e.nombre("Rat_s_ch", 0.0) * e.nombre("Rat_t_ch", 1.0) / tot_ch if chaud else 0.0,
                                    e.nombre("Rat_s_fr", 0.0) * e.nombre("Rat_t_fr", 1.0) / tot_fr if froid else 0.0))
    return out


def relance(consigne: np.ndarray, type_programmation: int, te: np.ndarray, base_ext: float, chaud: bool = True,
            etat: np.ndarray | None = None) -> np.ndarray:
    """Consigne de relance (845 à 848) : la consigne de confort est anticipée de la durée de relance avant chaque
    retour en occupation ; max(consigne, relance) en chaud, min en froid (801). Sans horloge en froid : confort permanent.
    `etat` : indicateur de consigne du scénario (1, 0, -1) ; l'inoccupation prolongée (tableaux 93, 94) est celle où il
    vaut -1. Sans lui, elle est devinée sur la valeur de la consigne réduite (7 °C en chaud), ce qui ne marche pas en
    froid où les deux consignes réduites valent 30 °C."""
    durees = (RELANCE_CHAUD if chaud else RELANCE_FROID).get(type_programmation, (0, 0))
    confort = consigne.max() if chaud else consigne.min()
    sortie = consigne.copy()
    if not chaud and type_programmation == 3:
        return np.full_like(consigne, confort)
    debuts = np.flatnonzero((consigne[1:] == confort) & (consigne[:-1] != confort)) + 1
    for t0 in debuts:
        if etat is not None:
            prolongee = etat[t0 - 1] == -1
        else:
            prolongee = (consigne[t0 - 1] < 10) if chaud else (consigne[t0 - 1] > 29)
        courte, longue = durees
        if not prolongee:
            d = courte
        elif longue is not None:
            d = longue
        else:                                                                      # optimiseur : 0 à 3 h selon θext
            d = 0
            for k in (3, 2, 1):
                x = int(round(min(3.0, max(0.0, 3.0 * (THETA_EXT_REG_SUP - te[t0 - k]) / (THETA_EXT_REG_SUP - base_ext)))))
                if x >= k:
                    d = k
                    break
        sortie[max(t0 - d, 0):t0] = confort
    return sortie
