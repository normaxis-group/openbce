# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Saisons propres d'un groupe (annexe III, fiche 4.6) et écarts d'inconfort qui les déclenchent (fiche 4.5).

Chaque jour à 9 h légales, l'automate décide si le chauffage et le refroidissement sont autorisés. Un démarrage se
décide sur les degrés-heures d'inconfort cumulés sur les quatre semaines précédentes au plus ; un arrêt, sur la
moyenne des besoins bruts (calculés sans tenir compte des saisons) sur quatre semaines. En mode Th-B, les
autorisations effectives sont les autorisations propres du groupe (91).
"""
from __future__ import annotations

from collections import deque

# Seuils de la nomenclature 4.6.2 : 40 °C.h d'inconfort pour démarrer une saison, 2 Wh/m² de besoin moyen pour l'arrêter.
SEUIL_DEBUT, SEUIL_FIN = 40.0, 2.0
# Écart d'inconfort chaud (61) : il s'écrit  i_chaud x (i_froid + 1) / 2 x |écart|, où i_froid est l'indicateur
# d'inconfort FROID. En occupation sans inconfort froid, i_froid vaut 0 : l'écart chaud est donc compté pour moitié.
# L'écart d'inconfort froid (60), lui, vaut i_froid x (i_froid + 1) / 2 x |écart|, soit l'écart entier.
# Le banc le confirme : sans ce facteur, la saison de refroidissement démarre 3 à 4 jours trop tôt (froid de juin
# surestimé de 0,5 kWh/m² sur 14 zones) ; avec lui, l'écart de juin tombe à 0,04 kWh/m².
POIDS_INCONFORT_CHAUD = 0.5
# Mode Th-C : poids de l'écart d'inconfort chaud propre aux consommations (None : le même qu'en Th-B). Essai du 08/10 :
# avec 1,0, la saison de froid de cas 03 démarre début juin comme sa référence (5,9 pour 6,9 en juin, contre 1,3) sans
# toucher cas 04 (démarrage forcé au 1er juillet) ; à confirmer sur les bureaux avant adoption.
POIDS_INCONFORT_CHAUD_THC = None
REDEMARRAGES_MAX = 1
D_OP_INC_C1 = 2.0                      # catégorie d'ambiance 1, retenue pour tous les usages (tableau 10)
CHAUFFAGE, MI_SAISON, REFROIDISSEMENT, MIXTE = 3, 2, 1, 4   # valeurs de Saison_gr (tableau 11)
FENETRE = 28                           # jours


def seuil_inconfort_chaud(consigne_fr: float, theta_rm: float) -> float:
    """Température opérative au-delà de laquelle l'occupant est en inconfort chaud, catégorie 1 (58)."""
    return max(consigne_fr, 0.33 * theta_rm + 18.8 + D_OP_INC_C1)


class Saisons:
    def __init__(self, heures_occupation_reference: float, surface: float, poids_inconfort_chaud: float | None = None):
        self.ref, self.surface = heures_occupation_reference, surface
        self.poids_chaud = POIDS_INCONFORT_CHAUD if poids_inconfort_chaud is None else poids_inconfort_chaud
        self.chauffage, self.refroidissement = True, False
        self.jours_chauffage_consecutifs = 56
        self.redemarrages = 0
        self._jour = [0.0] * 5                   # cumuls depuis 9 h : inconfort froid, inconfort chaud, occupation, besoins bruts
        self.dh_ch, self.dh_fr, self.occ = deque(maxlen=FENETRE), deque(maxlen=FENETRE), deque(maxlen=FENETRE)
        self.q_ch, self.q_fr = deque(maxlen=FENETRE), deque(maxlen=FENETRE)
        self._attente_ch = 0                     # jours écoulés depuis l'arrêt du chauffage

    @property
    def saison(self) -> int:
        if self.chauffage:
            return MIXTE if self.refroidissement else CHAUFFAGE
        return REFROIDISSEMENT if self.refroidissement else MI_SAISON

    def heure(self, occupe: bool, top_libre: float, consigne_ch: float, seuil_chaud: float, besoin_ch: float, besoin_fr: float) -> None:
        """Enregistre une heure : écarts d'inconfort en occupation (60, 61) et besoins bruts en Wh."""
        if occupe:
            self._jour[0] += max(consigne_ch - top_libre, 0.0)
            if top_libre >= consigne_ch:                 # pas d'inconfort froid
                self._jour[1] += self.poids_chaud * max(top_libre - seuil_chaud, 0.0)
            self._jour[2] += 1
        self._jour[3] += besoin_ch
        self._jour[4] += besoin_fr

    def _seuil(self, occupation: float) -> float:
        return SEUIL_DEBUT * max(0.5, occupation / (4 * self.ref))

    def nouveau_jour(self, jour: int) -> None:
        """À 9 h légales du jour `jour` (compté à partir de 0) : clôt la journée écoulée et met à jour les autorisations."""
        froid, chaud, occ, qch, qfr = self._jour
        self._jour = [0.0] * 5
        self.q_ch.append(qch)
        self.q_fr.append(qfr)
        # --- chauffage (76 à 81) ------------------------------------------------------------------------------------
        if self.chauffage:
            self.dh_ch.clear()
        else:
            self._attente_ch += 1
            if (jour >= 252 or self._attente_ch >= 2) and not 182 <= jour < 252:
                self.dh_ch.append((froid, occ))
        if jour < 56:
            nouveau = True
        elif jour < 182:
            if self.chauffage:
                jours = min(len(self.q_ch), FENETRE)
                mgb = sum(list(self.q_ch)[-jours:]) / (24 * jours) / self.surface
                nouveau = not (mgb <= SEUIL_FIN and self.jours_chauffage_consecutifs >= 7)
            else:
                nouveau = (self.redemarrages < REDEMARRAGES_MAX and self._attente_ch >= 2
                           and sum(d for d, _ in self.dh_ch) >= self._seuil(sum(o for _, o in self.dh_ch)))
                if nouveau:
                    self.redemarrages += 1
                    self.q_ch.clear()            # la moyenne des besoins repart du redémarrage (73)
        elif jour < 252:
            nouveau = False
        else:
            nouveau = self.chauffage or sum(d for d, _ in self.dh_ch) >= self._seuil(sum(o for _, o in self.dh_ch))
        if self.chauffage and not nouveau:
            self._attente_ch = 0
        self.jours_chauffage_consecutifs = self.jours_chauffage_consecutifs + 1 if nouveau else 0
        self.chauffage = nouveau
        # --- refroidissement (87 à 90) -------------------------------------------------------------------------------
        if 7 <= jour < 182:
            self.dh_fr.append(chaud)
            self.occ.append(occ)
        if jour < 7:
            self.refroidissement = False
        elif jour < 182:
            if not self.refroidissement:
                self.refroidissement = sum(self.dh_fr) >= self._seuil(sum(self.occ))
        elif jour < 245:
            self.refroidissement = True
        elif self.refroidissement:
            jours = min(len(self.q_fr), FENETRE)
            self.refroidissement = sum(list(self.q_fr)[-jours:]) / (24 * jours) / self.surface > SEUIL_FIN
