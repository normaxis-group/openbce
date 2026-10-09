# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Ventilation mécanique réelle d'un groupe (annexe III, fiches 6.2 et 6.5) : débits spécifiques repris et soufflés,
heure par heure, pour les modes Th-C et Th-D. Le Bbio (mode Th-B) ignore ces systèmes au profit de la ventilation
conventionnelle de la fiche 6.1.

PREMIER JET, périmètre : bouches de reprise et de soufflage des systèmes « Ventilation_Mecanique » (simple flux par
extraction ou insufflation, double flux). Non traités : CTA, ventilation naturelle ou hybride par conduit, puits
climatique et hydraulique, fuites des réseaux (430, 431 : prises nulles), pertes des conduits hors volume chauffé
(647, 664), chaleur des ventilateurs (653, 663 : prise nulle, elle ne compte que pour le Cep).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rsee import Noeud

# Durée d'utilisation du grand débit en résidentiel, h par semaine (tableau 58) : dispositif à gestion manuelle 14 h,
# dispositif avec temporisation 7 h. L'ordre des codes de Type_Regul_Res n'est pas dans le texte : le banc des
# auxiliaires de ventilation (banc/ventilateurs.py, 151 groupes sur 181 dans ±0,05 kWh/m²) a tranché 0 manuel, 1
# temporisation ; même table dans ventilateurs.py.
DUGD = {0: 14.0, 1: 7.0}
# Coefficient de dépassement (tableau 59) : valeur par défaut 1,30 ; composants autoréglables certifiés 1,15 ;
# hygroréglables certifiés : valeur issue de l'évaluation (champ Cdep_Value). Le champ Cdep vaut 0, 1 ou 2 dans
# les RSEE. Déduction du banc (cas 17, 18 groupes effet joule, 10/10/2026) : avec Cdep = 1 lu comme 1,15 le besoin
# de chauffage Th-C est à +23,6 %, avec 1,0 à +12,6 % : le code 1 est donc lu comme « pas de dépassement » (1,0) et
# le code 2 comme la valeur du champ Cdep_Value ; le code 0 reste la valeur par défaut 1,30.
CDEP = {0: 1.30, 1: 1.0}
# Efficacité d'échangeur retenue selon le statut du certificat (396 à 398) : certifié 1,0 ; justifié 0,9 ; déclaré 0,8
# plafonné à EPS_UTILE_MAX.
# codes du texte (6.3.3.4.2) : 2 certifié (ε saisi), 1 justifié (0,9 ε), 0 déclaré (0,8 ε plafonné). Le lot ne porte que
# le code 2 ; lu 0,9 jusqu'au 08/10/2026, cas 13 (double flux ε 0,8) sortait à +25 % de besoin Th-C.
CERTIFICAT = {2: 1.0, 1: 0.9, 0: 0.8}
EPS_UTILE_MAX = 0.9
# Fuites des réseaux (430, 431, tableaux 60 et 61) : Kres en m³/(s.m²) sous 1 Pa par classe d'étanchéité, dP en haute
# pression par usage, ratio de fuites en volume chauffé. Lecture du champ Classe_Etancheite tranchée au banc mensuel des
# 47 groupes chauffés par effet joule (banc/chauffage_mois.py, 07/10/2026) : la valeur 3 (92 % des bouches) lue comme la
# classe C donne un écart médian de -1,6 % mais |écart| médian 8,1 %, avec les collectifs de cas 17 à -38/-58 % et
# cas 16 à -15 % ; lue comme « par défaut » (0,0675), ces mêmes groupes tombent dans ±4 % (PRI collectifs -14 à +13 %,
# cas 16 -2 %). Le code 0 (cas 28) colle aussi avec « par défaut ». Codes 1 et 2 (deux projets) : classes A et B.
KRES = {0: 0.0675e-3, 1: 0.027e-3, 2: 0.009e-3, 3: 0.0675e-3}
DP_HP = {1: 80.0, 2: 160.0}
DP_HP_DEFAUT = 250.0
RATFUITEVC = {1: 0.25, 2: 0.5}
RATSURFCOND, RATDEBCOND = 0.05, 0.05
FUITES_RESEAU = True


@dataclass(frozen=True)
class Ventilation:
    repris: np.ndarray     # débit volumique repris (extrait) du groupe, m³/h, positif
    souffle: np.ndarray    # débit volumique soufflé dans le groupe, m³/h
    epsilon: float         # efficacité de l'échangeur du double flux (0 en simple flux)
    # bypass de l'échangeur (6.3.3.4.6.2, équations 494, 495) : (θext,bypass,hiver ; θint,bypass,hiver ; θext,bypass,été ;
    # θint,bypass,été), None sans fonction de bypass (Is_ByPass = 0) ; activé quand θext < θi(h-1), θext > θext,bypass et
    # θi(h-1) > θint,bypass : l'échangeur n'est alors pas pris en compte, ε(h) = 0 (496)
    bypass: tuple | None = None

    def epsilon_h(self, te: float, ti_prec: float, saison_chauffage: bool) -> float:
        if self.bypass is None:
            return self.epsilon
        t_ext, t_int = (self.bypass[0], self.bypass[1]) if saison_chauffage else (self.bypass[2], self.bypass[3])
        return 0.0 if (te < ti_prec and te > t_ext and ti_prec > t_int) else self.epsilon

    @property
    def desequilibre(self) -> np.ndarray:
        """Débit net extrait mécaniquement (repris - soufflé), m³/h : compensé par l'enveloppe dans le bilan de pression."""
        return self.repris - self.souffle


def _debit_bouche(b: Noeud, usage: int, sens: str, ventilation: np.ndarray) -> np.ndarray:
    """Débit régulé puis majoré du dépassement d'une bouche (383 à 390, 411 à 414, 423, 424), m³/h, par heure."""
    cdep = CDEP.get(b.entier("Cdep", 0), b.nombre("Cdep_Value", 1.0) or 1.0)
    if usage in (1, 2):
        pointe, base = b.nombre(f"Qv_{sens}_pointe", 0.0), b.nombre(f"Qv_{sens}_base", 0.0)
        dugd = DUGD.get(b.entier("Type_Regul_Res", 1), 14.0)
        q = (pointe * dugd + base * (168.0 - dugd)) / 168.0                              # (414)
        return np.full(len(ventilation), cdep * q)
    occ, inocc = b.nombre(f"Qv_{sens}_occ", 0.0), b.nombre(f"Qv_{sens}_inocc", 0.0)
    crdbnr = b.nombre("Cndbnr_Value", 1.0) or 1.0                                        # réduction en occupation (411, 412)
    return cdep * np.where(ventilation > 0, crdbnr * occ, inocc)


def _fuites(b: Noeud, usage: int, sens: str, q: np.ndarray, surface: float) -> np.ndarray:
    """Part des fuites du réseau prélevée dans le volume chauffé, m³/h (430 à 438) : elle s'ajoute au débit extrait
    du groupe (reprise) ou s'en retranche (soufflage)."""
    if not FUITES_RESEAU:
        return np.zeros_like(q)
    if b.entier(f"valeur_surface_conduit_{sens}", 0) == 1 and b.nombre(f"A_cond_{sens}", 0.0) > 0:
        a_cond = b.nombre(f"A_cond_{sens}", 0.0)
        rat_vc = b.nombre("Ratfuitevc", RATFUITEVC.get(usage, 0.75))
    else:
        a_cond = surface * RATSURFCOND if usage == 1 else float(np.max(q)) * RATDEBCOND
        rat_vc = RATFUITEVC.get(usage, 0.75)
    kres = KRES.get(b.entier("Classe_Etancheite", 3), KRES[3])
    dp = DP_HP.get(usage, DP_HP_DEFAUT)
    fuites = 3600.0 * kres * a_cond * dp ** 0.667
    return np.where(q > 0, rat_vc * fuites, 0.0)


def du_groupe(zone: Noeud, groupe: Noeud, usage: int, ventilation: np.ndarray) -> Ventilation:
    """`ventilation` : indicateur horaire Ivent de la zone (scénario conventionnel)."""
    n = len(ventilation)
    repris, souffle = np.zeros(n), np.zeros(n)
    surface = groupe.nombre("SHAB") if usage in (1, 2) else groupe.nombre("SU")
    systemes = {v.entier("Index"): v for v in zone.directs("Ventilation_Mecanique")}
    epsilon, bypass = 0.0, None
    for b in groupe.directs("Bouche_Conduit"):
        if b.entier("Type_Bouche_Conduit", 0) == 1:                                     # soufflage
            q = _debit_bouche(b, usage, "souf", ventilation)
            souffle += q - _fuites(b, usage, "souf", q, surface)
        else:
            q = _debit_bouche(b, usage, "rep", ventilation)
            repris += q + _fuites(b, usage, "rep", q, surface)
        vm = systemes.get(b.entier("Id_Systeme_Mecanique", 0))
        if vm is not None and vm.entier("Type_Ventilation_Mecanique", 0) == 1 and vm.entier("Type_Echangeur", 0) >= 1:
            eps = vm.nombre("Epsilon", 0.0) * CERTIFICAT.get(vm.entier("Certificat_Efficacite_Echangeur", 0), 0.8)
            epsilon = max(epsilon, min(eps, EPS_UTILE_MAX) if vm.entier("Certificat_Efficacite_Echangeur", 0) == 0 else eps)
            if vm.entier("Is_ByPass", 0) == 1:
                bypass = (vm.nombre("T_ext_bp_hiver", 0.0), vm.nombre("T_int_bp_hiver", 0.0), vm.nombre("T_ext_bp_ete", 0.0), vm.nombre("T_int_bp_ete", 0.0))
    return Ventilation(repris, souffle, epsilon, bypass)
