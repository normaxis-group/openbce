# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Indicateur d'impact sur le changement climatique des consommations d'énergie, Ic énergie (arrêté du 4 août 2021,
annexe II, § 4.3.2, équations 74 et 75), et son seuil Ic énergie_max (annexe de l'article R. 172-4, chapitre II).

Ic énergie = (1 / Sref) × Σ_énergie Σ_usage [Cef_imp(énergie, usage) × DE(énergie, usage) × Σ_{a=1..50} f_CO2(a)]
en kg CO2 eq/m² sur la période d'étude de référence de 50 ans ; Cef_imp est l'énergie importée annuelle (déduction faite de
l'autoconsommation, p. 1393 de l'annexe III), DE la donnée environnementale conventionnelle de mise à disposition de
l'énergie (base INIES, kg CO2 eq/kWh), f_CO2 les coefficients de pondération dynamique de l'article 11 de l'arrêté.

Les DE retenues sont déduites des récapitulatifs environnementaux de référence (partie RSEnv des RSEE, contributeur
« énergie » : impact du module B = Cef × DE × 50 / Sref) et recoupées avec les valeurs publiques de la RE2020 :
électricité 0,079 pour le chauffage, 0,069 pour l'éclairage et 0,064 pour les autres usages, gaz naturel 0,227. Fioul et bois sont les valeurs
publiées (0,324 et 0,030), non confrontées à un récapitulatif ; les réseaux de chaleur ont une DE propre à chaque réseau,
à fournir (`DE_RESEAU`), sinon leur contribution est ignorée et signalée.
"""
from __future__ import annotations

# coefficients de pondération dynamique f_CO2(a), a = 0 à 50 (article 11 de l'arrêté du 4 août 2021, cas général)
F_CO2 = (1.000, 0.992, 0.984, 0.976, 0.969, 0.961, 0.953, 0.945, 0.937, 0.929, 0.921, 0.913, 0.905, 0.897, 0.889, 0.880, 0.872,
         0.864, 0.856, 0.848, 0.840, 0.831, 0.823, 0.815, 0.806, 0.798, 0.790, 0.781, 0.773, 0.764, 0.756, 0.747, 0.739, 0.730,
         0.721, 0.713, 0.704, 0.695, 0.686, 0.678, 0.669, 0.660, 0.651, 0.642, 0.633, 0.624, 0.615, 0.606, 0.597, 0.587, 0.578)
PER = 50                                            # période d'étude de référence, ans
SOMME_F = sum(F_CO2[1:PER + 1])                     # 39,543 : les émissions de l'année a sont pondérées par f(a), a = 1 à 50

# données environnementales conventionnelles, kg CO2 eq/kWh d'énergie finale importée
DE_ELEC_CHAUFFAGE = 0.079
DE_ELEC_AUTRES = 0.064
DE_ELEC_ECLAIRAGE = 0.069                           # lu sur cinq bâtiments de référence (0,069 à chaque fois), contre 0,064 attendu
DE = {"gaz": 0.227, "fioul": 0.324, "bois": 0.030}
DE_RESEAU: float | None = None                      # réseau de chaleur : DE propre au réseau (arrêté DPE), à renseigner
POSTES = ("ch", "fr", "ecs", "ecl", "aux_vent", "aux_dist", "dep")


def de(energie: str, poste: str) -> float | None:
    if energie == "elec":
        return DE_ELEC_CHAUFFAGE if poste == "ch" else (DE_ELEC_ECLAIRAGE if poste == "ecl" else DE_ELEC_AUTRES)
    if energie == "reseau":
        return DE_RESEAU
    return DE.get(energie)


def ic_energie(imports: dict[tuple[str, str], float]) -> dict:
    """`imports` : énergie importée annuelle par (énergie, poste), kWh/m² de Sref et par an (hors usages mobiliers). Rend
    Ic énergie (kg CO2 eq/m², 50 ans pondérés), Ic énergie annuel statique (kg CO2 eq/m²/an, équation 75 à f = 1), le
    détail par (énergie, poste) et la liste des énergies sans DE (ignorées)."""
    detail, ignores, annuel = {}, [], 0.0
    for (energie, poste), cef in imports.items():
        if cef <= 0:
            continue
        d = de(energie, poste)
        if d is None:
            ignores.append(energie)
            continue
        detail[(energie, poste)] = cef * d * SOMME_F
        annuel += cef * d
    return dict(ic_energie=sum(detail.values()), ic_energie_annuel=annuel, detail=detail, energies_ignorees=sorted(set(ignores)))


# Ic énergie_maxmoyen, kg CO2 eq/m², par usage : (permis 2022 à 2024, 2025 à 2027, 2028 et après), colonne « raccordé à un
# réseau de chaleur urbain » puis « autres cas » (annexe de l'article R. 172-4, chapitre II, p. 29 et 30). Usages 4 et 5 :
# enseignement primaire ou secondaire ; les autres usages n'ont pas de seuil Ic énergie dans le texte disponible. Sur les
# 113 016 zones de l'observatoire OPEE, la colonne « autres cas » est retrouvée à 97 à 99,5 % même pour les zones déclarées
# raccordées à un réseau urbain (maisons 160, bureaux 200) : la colonne « réseau » ne s'applique qu'à un réseau classé
# (L. 712-1), que le RSEE ne distingue pas ; elle n'est utilisée que sur demande explicite (`reseau_chaleur=True`).
IC_ENERGIE_MAX_MOYEN = {1: ((200, 200, 160), (160, 160, 160)), 2: ((560, 320, 260), (560, 260, 260)), 3: ((280, 200, 200), (200, 200, 200)),
                        4: ((240, 200, 140), (240, 140, 140)), 5: ((240, 200, 140), (240, 140, 140))}
IC_ENERGIE_MAX_MAISON_GAZ = 280.0                   # maisons : permis avant le 31/12/2023 sur une parcelle prévue pour le gaz (p. 30)


def ic_energie_max_moyen(usage: int, annee_permis: int = 2026, reseau_chaleur: bool = False, derogation_gaz: bool = False) -> float | None:
    if usage == 1 and derogation_gaz and annee_permis <= 2023:
        return IC_ENERGIE_MAX_MAISON_GAZ
    t = IC_ENERGIE_MAX_MOYEN.get(usage)
    if t is None:
        return None
    periode = 0 if annee_permis <= 2024 else (1 if annee_permis <= 2027 else 2)
    return float(t[0 if reseau_chaleur else 1][periode])


def ic_energie_max(usage: int, facteur_modulation: float, annee_permis: int = 2026, reseau_chaleur: bool = False, derogation_gaz: bool = False) -> float | None:
    """Ic énergie_max = Ic énergie_maxmoyen × (1 + Mcgéo + Mccombles + Mcsurf_moy + Mcsurf_tot + Mccat) : le facteur est celui des
    seuils Cep (exigences.cep_max), identique pour les trois exigences (chapitre II, II)."""
    moyen = ic_energie_max_moyen(usage, annee_permis, reseau_chaleur, derogation_gaz)
    return None if moyen is None else moyen * facteur_modulation
