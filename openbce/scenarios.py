# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Scénarios conventionnels d'usage, heure par heure (annexe III, fiche 4.1 et chapitre 15).

Les tableaux viennent de `tables/scenarios_officiels.json`, converti par `outils/scenarios_xlsx.py` depuis le tableur
officiel des scénarios conventionnels (29/04/2026, 28 usages). Il remplace l'extraction du chapitre 15 sur le texte du
PDF (`outils/extraire_scenarios.py`), identique là où elle avait lu quelque chose, mais qui arrondissait 1/9 à 0,111,
les parts de surface au millième, et manquait les tableaux des locaux d'enseignement. Chaque grandeur est le produit
d'un profil hebdomadaire (jour x heure légale) et d'un profil annuel (semaine x mois).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from .calendrier import Calendrier, adultes_equivalents

USAGES = {n: str(n) for n in range(1, 29)}    # numérotation des RSEE, identique à celle du tableur (1 maison ... 28)
# Part de la surface utile de la zone occupée par le local d'habitation (33) : en collectif, 10 % vont aux
# circulations, sans occupant ni apport (synthèse des scénarios, annexe I de l'arrêté du 19 mars 2026).
RATIO_HABITATION = {1: 1.0, 2: 0.9}
ALPHA_CONV = 0.5   # part convective des apports internes (valeur conventionnelle, nomenclature de la fiche 4.1)


@lru_cache
def _tables() -> dict:
    return json.loads((Path(__file__).parent / "tables" / "scenarios_officiels.json").read_text(encoding="utf-8"))["usages"]


def _tableau(usage: int, debut: str) -> dict:
    for t in _tables()[USAGES[usage]]["tableaux"]:
        if t["hebdo"] and t["nom"].lower().startswith(debut):
            return t
    raise KeyError(f"tableau {debut!r} absent pour l'usage {usage}")


def _scalaire(usage: int, debut: str) -> dict:
    for s in _tables()[USAGES[usage]]["scalaires"]:
        if s["nom"].lower().startswith(debut):
            return s
    raise KeyError(f"valeur {debut!r} absente pour l'usage {usage}")


def _horaire(cal: Calendrier, t: dict) -> tuple[np.ndarray, np.ndarray]:
    """Profils hebdomadaire et annuel étalés sur les 8 760 heures."""
    hebdo = np.asarray(t["hebdo"], dtype=float)[cal.jour_semaine - 1, cal.case - 1]
    annuel = np.array([[np.nan if v is None else v for v in ligne] for ligne in t["annuel"]], dtype=float)[cal.semaine - 1, cal.mois - 1]
    return hebdo, annuel


@dataclass(frozen=True)
class Scenario:
    """Séries horaires d'une zone d'habitation."""

    occupation: np.ndarray        # 1 si la zone est occupée
    consigne_ch: np.ndarray       # température de consigne de chauffage, °C
    consigne_fr: np.ndarray       # température de consigne de refroidissement, °C
    ventilation: np.ndarray       # 1 = débit d'occupation, 0 = débit d'inoccupation
    eclairage: np.ndarray         # 1 si l'éclairage peut fonctionner
    occupants: np.ndarray         # nombre d'adultes équivalents présents (37)
    apports_occupants: np.ndarray # chaleur dégagée par les occupants, W (39)
    apports_usages: np.ndarray    # chaleur des usages hors occupants et éclairage, W (41)
    nadeq: float
    locaux: tuple = ()            # (nom, part de surface) des locaux conventionnels de la zone
    # indicateurs de consigne (fiche 8.5, pch et pfr) : 1 présence, 0 absence de moins de 48 h, -1 absence de plus de 48 h ;
    # la relance les lit, car les consignes réduites courte et prolongée peuvent avoir la même valeur (froid : 30 °C)
    etat_ch: np.ndarray | None = None
    etat_fr: np.ndarray | None = None


def _consignes(usage: int, etat: np.ndarray, cle: str) -> np.ndarray:
    v = {1: _scalaire(usage, "consigne normal")[cle], 0: _scalaire(usage, "consigne arrêt moins")[cle], -1: _scalaire(usage, "consigne arrêt plus")[cle]}
    return np.select([etat == 1, etat == 0], [v[1], v[0]], v[-1])


def habitation(cal: Calendrier, usage: int, surface: float, nb_logements: int) -> Scenario:
    """`surface` : surface utile de la zone. Les occupants et les apports portent sur le local d'habitation."""
    surface = surface * RATIO_HABITATION[usage]
    def produit(nom):
        h, a = _horaire(cal, _tableau(usage, nom))
        return h * a

    # consignes : tableau 5, le résultat est le plus petit des deux états (-1 l'emporte, puis 0)
    ch = np.minimum(*_horaire(cal, _tableau(usage, "chauffage")))
    fr = np.minimum(*_horaire(cal, _tableau(usage, "refroidissement")))
    occupation = produit("occupation")
    nadeq = adultes_equivalents(usage, surface, nb_logements)
    occupants = nadeq * occupation * produit("occupant")
    return Scenario(
        occupation=occupation, consigne_ch=_consignes(usage, ch, "chauffage"), consigne_fr=_consignes(usage, fr, "refroidissement"),
        ventilation=produit("ventilation"), eclairage=produit("éclairage"), occupants=occupants,
        apports_occupants=occupants * _scalaire(usage, "chaleur moyenne")["valeur"],
        apports_usages=surface * _scalaire(usage, "apports de chaleur hors occupants")["valeur"] * produit("apports de chaleur"), nadeq=nadeq,
        etat_ch=ch, etat_fr=fr)


def _locaux(usage: int) -> list[dict]:
    """Locaux conventionnels de l'usage, dans l'ordre du chapitre 15 : nom, part de surface, occupants par m²,
    chaleur par occupant, apports des équipements par m², et leurs deux tableaux (occupation, apports)."""
    donnees = _tables()[USAGES[usage]]
    locaux = []
    for s in donnees["scalaires"]:
        if s["nom"] == "local":
            locaux.append({"nom": s["local"], "ratio": 0.0, "occupants": 0.0, "w_occupant": 0.0, "w_usages": 0.0})
        elif not locaux:
            continue
        elif s["nom"] == "ratio du local":
            locaux[-1]["ratio"] = s["valeur"]
        elif s["nom"] == "occupants par m²":
            locaux[-1]["occupants"] = s["valeur"]
        elif s.get("unite") in ("W/Nocc", "W/Nadeq"):
            locaux[-1]["w_occupant"] = s["valeur"]
        elif s.get("unite") == "Watts/unité":
            locaux[-1]["w_usages"] = s["valeur"]
    occupation = [t for t in donnees["tableaux"] if t["hebdo"] and t["nom"].lower().startswith("occupant")]
    apports = [t for t in donnees["tableaux"] if t["hebdo"] and t["nom"].lower().startswith("apports de chaleur")]
    for k, l in enumerate(locaux):
        l["t_occupation"], l["t_apports"] = occupation[k], apports[k]
    return locaux


def tertiaire(cal: Calendrier, usage: int, surface: float) -> Scenario:
    """Scénarios d'une zone non résidentielle : occupants et apports sommés sur ses locaux conventionnels (38, 39, 41)."""
    def produit(nom):
        h, a = _horaire(cal, _tableau(usage, nom))
        return h * a

    ch = np.minimum(*_horaire(cal, _tableau(usage, "chauffage")))
    fr = np.minimum(*_horaire(cal, _tableau(usage, "refroidissement")))
    occupation = produit("occupation")
    occupants = np.zeros(len(occupation))
    w_occupants = np.zeros(len(occupation))
    w_usages = np.zeros(len(occupation))
    locaux = _locaux(usage)
    for l in locaux:
        aire = surface * l["ratio"]
        h, a = _horaire(cal, l["t_occupation"])
        n = aire * l["occupants"] * occupation * h * a
        occupants += n
        w_occupants += n * l["w_occupant"]
        h, a = _horaire(cal, l["t_apports"])
        w_usages += aire * l["w_usages"] * h * a
    return Scenario(
        occupation=occupation, consigne_ch=_consignes(usage, ch, "chauffage"), consigne_fr=_consignes(usage, fr, "refroidissement"),
        ventilation=produit("ventilation"), eclairage=produit("éclairage"), occupants=occupants, apports_occupants=w_occupants,
        apports_usages=w_usages, nadeq=0.0, locaux=tuple((l["nom"], l["ratio"]) for l in locaux), etat_ch=ch, etat_fr=fr)
