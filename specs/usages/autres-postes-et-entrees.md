# Autres postes et données d'entrée dépendant de l'usage : déplacements, parkings, parties communes, usages mobiliers, auxiliaires de ventilation, entrées et sorties du récapitulatif pour les zones non résidentielles

Date : 09/10/2026. Décision de Cédric PLANTAZ (ARKEMEP) : « go code les 28 usages, marqués non validés ».

Contre-lecture du 09/10/2026 appliquée (12 corrections, chacune relue à la source avant d'être portée) : FA05 p. 11 (occupation hospitalière continue), mobilité des usages 20 et 23 (tableur), équations (2315) à (2317) p. 1315, tableaux 315 et 316 p. 1303, (783) et (784) p. 483 et constantes p. 479, numéros de ligne de `groupe.py`, `eclairage.py`, `ecs.py` et `banc/sortie_rsee.py` ; l'affectation horaire du tableau 321 et le contexte de P5 sont ramenés à « non spécifié ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Le NAS ne contient aucun RSEE RE2020 d'usage 4 à 28 ; tout ce qui suit pour ces usages est écrit sur la foi du texte et devra porter la marque « non validé » dans le code. Rien n'est demandé au CSTB.

## Sources lues

| Source | Pages ou lignes lues |
|---|---|
| Annexe III en vigueur (arrêté du 4 août 2021 modifié jusqu'au 19 mars 2026), `corpus/texte_annexe3_2026-07/annexe3.txt`, 1 854 pages | sommaire p. 1 à 14 ; 1.3.2 surfaces p. 16 ; 2.1 données conventionnelles p. 17 à 26 (synthèse des scénarios p. 24 à 26) ; 4.1 scénarios conventionnels p. 52 à 63 ; 4.7 usages mobiliers p. 95 et 96 ; 6.5 ventilateurs p. 407 et 408 ; 7.1 éclairage p. 475 à 492 ; 7.2 parties communes p. 502 et 503 ; 8.32 brasseurs (Type_UsageZ) p. 990 ; 9.6 besoins d'ECS p. 1049 à 1057 ; 10.1 ascenseurs p. 1295 à 1308 ; 10.2 escalators p. 1309 à 1315 ; 10.3 ventilation des parkings p. 1318 à 1326 ; 10.4 éclairage des parkings p. 1327 à 1333 ; 13.1 sorties Th-B p. 1355 à 1364 ; 13.2 sorties Th-C p. 1365 à 1377 ; 13.4 bilans p. 1386 à 1395 ; 13.6 indicateur par occupant p. 1404 à 1406 ; chapitre 15 p. 1409 |
| Version 2022 découpée, `corpus/texte_annexe3/010_1_C_Bat_Ascenseurs.txt` | lignes 584 à 812 (tableau Bv, constantes) |
| Tableur officiel des scénarios du 29/04/2026, converti : `openbce/tables/scenarios_officiels.json` | feuilles MI à GYM_PRI (usages 1 à 28), scalaires et tableaux « mobilité », « occupation », « occupant », « apports de chaleur », « ECS » |
| Fiche d'application FA05 « Comment identifier l'usage d'un bâtiment » v2 (01/10/2026), `corpus/site_2026-10-09/re2020-fa05_usage-batiment_v2.txt` | p. 1 à 12 |
| Fiche d'application FA09 « Exclusions tertiaire spécifique et industrie » v1 (01/10/2026), `re2020-fa09_...txt` | p. 1 à 8 |
| Fiche d'application FA08 « Ascenseurs partagés » v1.1 (05/10/2026), `re2020-fa08_ascenseurs_partages_v1_1.pdf` (texte extrait) | p. 1 à 6 |
| Moteur : `openbce/ascenseurs.py`, `parkings.py`, `consommation.py`, `scenarios.py`, `calendrier.py`, `eclairage.py`, `ecs.py`, `bilans.py`, `sortie_rsee.py`, `rsee.py`, `groupe.py` (l. 1 à 60, 105 à 140) ; bancs `banc/sortie_rsee.py`, `banc/deplacement.py`, `banc/ascenseurs.py`, `banc/cep_total.py`, `banc/bilans.py` (grep) ; `docs/rsee.md`, `docs/lectures.md`, `specs/00-plan-cep.md` | intégralement sauf mention |

Schéma XSD du récapitulatif : **aucun fichier `*.xsd` dans le corpus** (`find` sur `octane-thbce/` : 0 résultat) ; `docs/rsee.md` le confirme (« Aucun schéma XSD du RSEE n'est publié sur le portail du ministère »). Les noms de champs cités ci-dessous sont ceux que le moteur lit déjà dans les RSEE d'usage 1 à 3 ; pour les objets propres aux usages 4 à 28 ils sont « non spécifiés ».

Numérotation : les numéros d'équation et de tableau sont ceux du texte 2026. Ils diffèrent d'une unité de ceux que le moteur porte en commentaire (version 2022) : par exemple le tableau Bv est le **tableau 310** p. 1300 (le moteur écrit « tableau 311 »), la veille par défaut est **(2274)** p. 1304 (le moteur écrit 2275), les sorties horaires des ascenseurs sont **(2305) à (2310)** p. 1308.

## 1. Ce qui dépend de l'usage dans ce thème

| Poste ou donnée | Fiche | Ce qui dépend de l'usage | Usages concernés |
|---|---|---|---|
| Surface de référence SREF | 1.3.2 p. 16, 13.1 (2375 à 2378) p. 1359, 13.2 (2412 à 2415) p. 1371 | SHAB pour 1 et 2, SU pour 3 à 28 | tous |
| Occupants conventionnels Nocc_l, NB_z | 4.1 (38) p. 61, 10.1 (2280) p. 1305 | locaux conventionnels (ratio, Nocc_nom), profils d'occupation | 3 à 28 (1 et 2 : adultes équivalents (32) à (37)) |
| Nombre d'occupants saisi Nocc_zn | 13.6 p. 1404 à 1406 | règle de saisie (pièces principales, scénarios, élèves) | tous |
| Mobilité Uk | 4.1 (31) p. 60 | tableau « mobilité » du tableur | tous |
| Ascenseurs | 10.1 p. 1295 à 1308 | Bv(k) tableau 310, NB_z, Timmob_n (habitation ou non), Uk | 2 à 28 (1 : Bv absent) |
| Escalators | 10.2 p. 1309 à 1315 | mêmes Bv(k), NB_z, Uk | 2 à 28 |
| Éclairage des parties communes | 7.2 p. 502 et 503 | calculé pour l'usage 2 seulement | 2 |
| Parkings, éclairage et ventilation | 10.3 p. 1318 à 1326, 10.4 p. 1327 à 1333 | Typeusage du parking (bureau, commerce, habitat) déduit de l'usage de la zone ; plages d'ouverture ; mouvements Rmvtpl | tous |
| Auxiliaires de ventilation | 6.5 (636) à (646) p. 407 et 408 | résidentiel (Dugd) ou non (Ivent) ; aucune constante par usage | tous |
| Usages mobiliers | 4.7 (93) à (95) p. 96 | apports des équipements des locaux conventionnels | tous |
| Éclairage, entrées par local | 7.1 tableau 78 p. 488 à 491, (781), (782) p. 481 | C1 et Eiref par type de local de chaque usage, locaux de grand volume | 3 à 28 |
| Besoins d'ECS, unité Nu | 9.6 tableau 277 p. 1053 à 1055 | a par m² de surface utile | 3 à 28 |
| Sorties par zone | 13.1, 13.2, 13.4, 13.6 | O_SHAB et O_SU, postes déplacement et mobilier, O_Cep_annuel_occ | tous |

L'énergie de mobilité d'une cabine Emoy (2301) p. 1307 ne dépend pas de l'usage : elle ne dépend que de la cabine (Q, V, H, netage, TechMac, Cp). Pour le poste déplacement, l'usage n'entre que par Bv(k), NB_z, Timmob_n et Uk.

## 2. Liste des usages et indicateurs d'usage (fiche 4.1, tableau 4, p. 57)

```python
# tableau 4, p. 57 : numéro d'usage -> (ihebergement, ienseignement)
INDICATEURS_USAGE = {
    1: (1, 0), 2: (1, 0), 3: (0, 0), 4: (0, 1), 5: (0, 1), 6: (0, 0), 7: (0, 1),
    8: (1, 0), 9: (1, 0), 10: (0, 0), 11: (0, 0), 12: (0, 0), 13: (0, 0), 14: (0, 0),
    15: (0, 0), 16: (0, 0), 17: (0, 0), 18: (0, 0), 19: (1, 0), 20: (1, 0), 21: (0, 0),
    22: (0, 0), 23: (0, 0), 24: (0, 0), 25: (0, 0), 26: (0, 1), 27: (0, 1), 28: (0, 0),
}
```

- ihebergement sert aux fiches qui distinguent « habitation ou hébergement » (nomenclature p. 54) ; ienseignement coupe le réseau primaire d'ECS pendant les vacances, (47) p. 62.
- Le texte emploie trois vocables qu'il ne définit pas l'un par rapport à l'autre : « habitation » (10.1, (2294) p. 1306 : « zones de typologie habitation »), « résidentiel » (6.5, 13.1), « habitation ou hébergement » (ihebergement). La lecture retenue par le moteur pour « résidentiel » et « habitation » est : usages 1 et 2 (`groupe.py` l. 108, `consommation.py` l. 42, `ascenseurs.py` l. 112). Voir point ouvert P1.
- FA05 (p. 4, 9 à 11) rattache les destinations non listées à l'un des 28 usages (résidences étudiantes avec cuisine : 2, sans cuisine : 8 ; internats : 10 ; centres de loisirs : 4 ; CFA : 5 ; bibliothèques universitaires indépendantes : 6 ; conservatoires et écoles d'ingénieurs : 7 ; auberges de jeunesse : 8 à 11 ; bars, concessions, casinos, aires de service, espaces de vente des gares : 17 ; EHPAD, FAM, MAS : 19 ; cabinets médicaux, cliniques vétérinaires, accueil de jour : 21 ; parties d'hôpitaux et cliniques à occupation continue (H24, 7j/7) : « Établissement de santé (partie nuit) », numéro imprimé « 22 » p. 11, coquille pour 20 (au tableau 4 p. 57, 22 est l'aérogare) ; IME, IEM, ITEP sans hébergement : 21, avec hébergement « partie jour et nuit » : 20 et 21 ; vestiaires de stade : 18 ; centres de fitness : 28 ; entrepôts et centres techniques chauffés pour le confort : 23 ou 24). Les vestiaires des établissements sportifs sont compris dans les usages 25 et 28 et ne font pas une zone 18 (FA05 p. 4). Le moteur n'a rien à coder ici : c'est l'applicateur qui choisit l'usage de la zone ; le moteur lit le champ `Usage`.
- FA09 (p. 5) : les locaux de process sont exclus du calcul et de la SREF ; les équipements de process ne sont pas saisis. Rien à coder : les données d'entrée arrivent déjà épurées.

## 3. Surfaces, locaux, occupants

### 3.1 Surfaces (p. 16, p. 58, p. 1359, p. 1371)

- SREF_gr = SHAB_gr si Usage_gr ∈ {1, 2}, sinon SU_gr : (2375), (2376) p. 1359 et (2412), (2413) p. 1371. SREF_zn = Σ SREF_gr (2377), (2414) ; SREF_bat = Σ SREF_zn (2378), (2415).
- Surface utile de la zone A_z = Σ_g A_gr (28) p. 58 ; part d'un groupe Rat_gr = A_gr / A_z (27) ; surface d'un local A_l = A_z × Rat_loc_l (29) p. 58. En usage 2 la zone n'a que deux locaux, habitation et circulation, (33) p. 60 (le moteur : `scenarios.RATIO_HABITATION`, l. 25).
- Dans le RSEE lu par le moteur, le groupe porte `SHAB` (usages 1 et 2) ou `SU` (usage 3) : `groupe.py` l. 108, `banc/sortie_rsee.py` l. 54. Pour les usages 4 à 28, la même lecture `SU` est la seule compatible avec (2413) ; aucun RSEE ne permet de vérifier que les logiciels écrivent `SU` et non `SHAB` pour ces usages (point ouvert P8).

### 3.2 Locaux conventionnels des usages 3 à 28

Source : synthèse des scénarios p. 24 à 26 (colonnes « ratio par défaut surface utile du local », « nombre d'occupants nominal par m² utile », « apports internes des équipements en occupation » et « hors occupation », W/m² utile) et tableur du 29/04/2026, approuvé par le chapitre 15 p. 1409. La chaleur dégagée par occupant (90, 105 ou 300 W) n'est que dans le tableur (scalaire « Chaleur moyenne dégagée par un occupant ») ; le texte p. 20 ne donne que 90 W au repos et 63 W en sommeil pour l'habitation.

Chaque entrée : (nom du local, ratio de surface, Nocc_nom en occupants par m², W par occupant, apports des équipements en occupation en W/m², apports des équipements hors occupation en W/m²). Les deux dernières colonnes sont celles de la synthèse p. 24 à 26.

```python
LOCAUX = {
    3: [  # Bureaux, p. 24
        ("Bureau standard", 0.6047, 0.1, 90, 16, 1.77776),
        ("Salle de réunion", 0.1047, 0.42, 90, 10, 0),
        ("Circulation Accueil", 0.2558, 0, 90, 0, 0),
        ("Sanitaires collectifs", 0.0348, 0, 90, 0, 0),
    ],
    4: [  # Enseignement primaire, p. 24
        ("Bureau standard", 0.1, 0.067, 90, 16, 1.77776),
        ("Circulation Accueil", 0.1, 0, 90, 0, 0),
        ("Salle de classe", 0.55, 0.66, 90, 0, 0),
        ("Salle de réunion", 0.05, 0.42, 90, 10, 0),
        ("Salle de repos", 0.15, 0.66, 90, 0, 0),
        ("Sanitaires vestiaires", 0.05, 0, 90, 0, 0),
    ],
    5: [  # Enseignement secondaire, p. 24
        ("Bureau standard", 0.1, 0.1, 90, 16, 1.77776),
        ("Circulation Accueil", 0.2, 0, 90, 0, 0),
        ("Salle de classe", 0.25, 0.67, 90, 0, 0),
        ("Salle de réunion", 0.1, 0.42, 90, 10, 0),
        ("Centre de documentation", 0.05, 0.1, 90, 5, 0.55555),
        ("Salle des professeurs", 0.05, 0.67, 90, 0, 0),
        ("Salle d'enseignement informatique", 0.05, 0.335, 90, 25.795, 2.8658245),
        ("Salle de conférence Salle polyvalente", 0.15, 0.33, 90, 10, 0),
        ("Sanitaires collectifs", 0.05, 0, 90, 0, 0),
    ],
    6: [  # Médiathèques et bibliothèques, p. 24
        ("Circulation accueil", 0.1, 0, 90, 0, 0),
        ("Bureau standard", 0.05, 0.1, 90, 16, 1.77776),
        ("Sanitaires collectifs", 0.05, 0, 90, 0, 0),
        ("Local service", 0.05, 0, 90, 0, 0),
        ("Salle de réunion", 0.1, 0.42, 90, 10, 0),
        ("Centre de documentation", 0.6, 0.1, 90, 5, 0.555),
        ("Salle multi-fonctions", 0.05, 0.26, 90, 10, 0),
    ],
    7: [  # Bâtiments universitaires et enseignements atypiques, p. 24
        ("Bureau standard", 0.1, 0.1, 90, 16, 1.77776),
        ("Circulation Accueil", 0.15, 0, 90, 0, 0),
        ("Salle de classe", 0.25, 0.67, 90, 0.5, 0),
        ("Centre de documentation", 0.05, 0.1, 90, 5, 0.55555),
        ("Salle de conférence Amphithéâtre", 0.15, 0.33, 90, 10, 0),
        ("Salle d'enseignement informatique", 0.05, 0.335, 90, 25.795, 2.863245),
        ("Salle de réunion", 0.05, 0.42, 90, 10, 0),
        ("Sanitaires collectifs", 0.05, 0, 90, 0, 0),
        ("Local service", 0.15, 0, 90, 0, 0),
    ],
    8: [  # Hôtels 0, 1 et 2 étoiles, partie nuit, p. 24
        ("Circulation Accueil", 0.233, 0, 90, 0, 0),
        ("Chambre sans cuisine avec salle de bain", 0.728, 0.05, 90, 4, 0.6),
        ("Sanitaires collectifs", 0.007, 0, 90, 0, 0),
        ("Local service", 0.032, 0, 90, 0, 0),
    ],
    9: [  # Hôtels 3, 4 et 5 étoiles, partie nuit, p. 24
        ("Circulation Accueil", 0.233, 0, 90, 0, 0),
        ("Chambre sans cuisine avec salle de bain", 0.728, 0.0375, 90, 4.625, 1.5725),
        ("Sanitaires collectifs", 0.007, 0, 90, 0, 0),
        ("Local service", 0.032, 0, 90, 0, 0),
    ],
    10: [  # Hôtels 0, 1 et 2 étoiles, partie jour, p. 24
        ("Bureau standard", 0.1161, 0.067, 90, 16, 1.77776),
        ("Circulation Accueil", 0.4308, 0, 90, 0, 0),
        ("Sanitaires collectifs", 0.0512, 0, 90, 0, 0),
        ("Salle petits déjeuners", 0.4019, 0.5, 90, 88.8, 8.88),
    ],
    11: [  # Hôtels 3, 4 et 5 étoiles, partie jour, p. 24 (voir point ouvert P11 pour la salle petits déjeuners)
        ("Bureau standard", 0.105, 0.067, 90, 16, 1.77776),
        ("Circulation Accueil", 0.173, 0, 90, 0, 0),
        ("Sanitaires collectifs", 0.037, 0, 90, 0, 0),
        ("Salle petits déjeuners", 0.17, 0.5, 90, 44.3, 4.43),
        ("Salle de séminaires réunion", 0.4276, 0.42, 90, 10, 0),
        ("Bar", 0.0874, 0.1, 90, 34.4, 4.128),
    ],
    12: [  # Établissements d'accueil de la petite enfance, p. 25 (voir P11 pour la salle de réunion)
        ("Bureau standard", 0.15, 0.067, 105, 16, 1.77776),
        ("Circulation Accueil", 0.15, 0, 105, 0, 0),
        ("Salle de réunion", 0.1, 0.42, 105, 10, 0),
        ("Salle de jeux", 0.3, 0.25, 105, 0, 0),
        ("Salle de repos", 0.2, 0.66, 105, 0, 0),
        ("Sanitaires vestiaires", 0.1, 0, 105, 0, 0),
    ],
    13: [  # Restaurants en continu, p. 25
        ("Salle restaurant", 0.7, 0.59, 105, 0, 0),
        ("Cuisine", 0.2, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    14: [  # Restaurants 1 repas, 5 j/7, p. 25
        ("Salle restaurant", 0.7, 0.77, 105, 0, 0),
        ("Cuisine", 0.2, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    15: [  # Restaurants 2 repas, 7 j/7, p. 25
        ("Salle restaurant", 0.7, 0.59, 105, 0, 0),
        ("Cuisine", 0.2, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    16: [  # Restaurants 2 repas, 6 j/7, p. 25
        ("Salle restaurant", 0.7, 0.59, 105, 0, 0),
        ("Cuisine", 0.2, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    17: [  # Commerces, p. 25
        ("Sanitaires collectifs", 0.01, 0, 105, 0, 0),
        ("Douches collectives", 0.01, 0, 105, 0, 0),
        ("Aire de vente (supérieure à 300m²)", 0.25, 0.15, 105, 8, 0),
        ("Aire de vente (inférieure à 300m²)", 0.4, 0.25, 105, 8, 0),
        ("Circulation Accueil", 0.28, 0.2, 105, 8, 0),
        ("Local service", 0.05, 0, 105, 0, 0),
    ],
    18: [  # Vestiaires seuls, p. 25
        ("Douches collectives", 0.3, 0, 90, 0, 0),
        ("Sanitaires vestiaires", 0.5, 0.1, 90, 0, 0),
        ("Circulation Accueil", 0.2, 0, 90, 0, 0),
    ],
    19: [  # Établissements sanitaires avec hébergement, p. 25
        ("Bureau standard", 0.1, 0.1, 90, 16, 1.77776),
        ("Circulation Accueil", 0.15, 0, 90, 0, 0),
        ("Chambre sans cuisine avec salle de bain", 0.5, 0.063, 90, 6.8, 1.02),
        ("Sanitaires collectifs", 0.05, 0, 90, 0, 0),
        ("Local service", 0.1, 0, 90, 0, 0),
        ("Salle commune", 0.1, 0.1, 90, 6, 0),
    ],
    20: [  # Établissements de santé, partie nuit, p. 25
        ("Chambre sans cuisine avec salle de bain", 0.2, 0.08, 105, 6.8, 1.02),
        ("Douches collectives", 0.05, 0, 105, 0, 0),
        ("Sanitaires collectifs", 0.05, 0, 105, 0, 0),
        ("Circulation Accueil", 0.15, 0, 105, 0, 0),
        ("Locaux soins et offices", 0.2, 0.06, 105, 0, 0),
        ("Bureau standard", 0.15, 0.57, 105, 16, 1.7776),
        ("Aire de production", 0.05, 0.14, 105, 5, 5),
        ("Salle d'attente et de consultation (urgences)", 0.15, 0.4, 105, 0, 0),
    ],
    21: [  # Établissements de santé, partie jour, p. 25
        ("Salle de réunion", 0.15, 0.42, 105, 10, 0),
        ("Douches collectives", 0.05, 0, 105, 0, 0),
        ("Sanitaires collectifs", 0.05, 0, 105, 0, 0),
        ("Circulation Accueil", 0.25, 0, 105, 0, 0),
        ("Bureau standard", 0.2, 0.57, 105, 16, 1.7776),
        ("Aire de production", 0.05, 0.14, 105, 5, 0),
        ("Salle d'attente et de consultation", 0.25, 0.4, 105, 0, 0),
    ],
    22: [  # Aérogares, p. 25
        ("Espace voyageurs", 0.42, 0.25, 105, 5, 0),
        ("Circulation Accueil", 0.179, 0.08, 105, 2, 0),
        ("Commerces", 0.109, 0.12, 105, 5, 0),
        ("Bureau standard", 0.143, 0.1, 105, 16, 1.77776),
        ("Sanitaires vestiaires", 0.105, 0.2, 105, 0, 0),
        ("Inspection filtrage", 0.043, 0.33, 105, 10, 0),
    ],
    23: [  # Industries ou artisanats 3x8, p. 25
        ("Bureau standard", 0.1, 0.1, 105, 16, 1.77776),
        ("Aire de production", 0.6, 0.14, 105, 2, 2),
        ("Circulation Accueil", 0.1, 0, 105, 0, 0),
        ("Sanitaires vestiaires", 0.05, 0, 105, 0, 0),
        ("Douches collectives", 0.05, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    24: [  # Industries ou artisanats 8 h à 18 h, p. 25
        ("Bureau standard", 0.1, 0.1, 105, 16, 1.77776),
        ("Aire de production", 0.6, 0.14, 105, 2, 0),
        ("Circulation Accueil", 0.1, 0, 105, 0, 0),
        ("Sanitaires vestiaires", 0.05, 0, 105, 0, 0),
        ("Douches collectives", 0.05, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    25: [  # Établissements sportifs municipaux ou scolaires, p. 26
        ("Circulation Accueil", 0.1, 0, 90, 0, 0),
        ("Salle de sport", 0.65, 0.1, 300, 0, 0),
        ("Local service", 0.05, 0, 90, 0, 0),
        ("Sanitaires vestiaires", 0.15, 0.1, 90, 0, 0),
        ("Douches collectives", 0.05, 0, 90, 0, 0),
    ],
    26: [  # Restaurants scolaires 1 repas, p. 26
        ("Salle restaurant", 0.7, 0.77, 90, 0, 0),
        ("Cuisine", 0.2, 0, 90, 0, 0),
        ("Local service", 0.1, 0, 90, 0, 0),
    ],
    27: [  # Restaurants scolaires 3 repas, p. 26
        ("Salle restaurant", 0.7, 0.77, 105, 0, 0),
        ("Cuisine", 0.2, 0, 105, 0, 0),
        ("Local service", 0.1, 0, 105, 0, 0),
    ],
    28: [  # Établissements sportifs privés, p. 26
        ("Circulation Accueil", 0.1, 0, 90, 0, 0),
        ("Salle de sport", 0.65, 0.1, 300, 0, 0),
        ("Local service", 0.05, 0, 90, 0, 0),
        ("Sanitaires vestiaires", 0.15, 0.1, 90, 0, 0),
        ("Douches collectives", 0.05, 0, 90, 0, 0),
    ],
}
```

Le moteur ne doit pas recopier ce dict : `scenarios._locaux(usage)` (l. 101 à 123) le lit déjà dans le tableur, profils horaires compris. Le dict sert de contrôle et de référence de page. Deux écarts entre la synthèse p. 24 et 25 et le tableur (point ouvert P11) : usage 11, salle petits déjeuners, 44,3 et 4,43 W/m² dans le texte, 0 dans le tableur ; usage 12, salle de réunion, 10 W/m² dans le texte, 0 dans le tableur.

### 3.3 Nombre d'occupants d'un local et de la zone

- Usages autres que 1 et 2 : Nocc_l(m,s,j,h) = A_l × Nocc_nom_l × (p_occ_a(m,s) × p_occ_s(j,h)) × (t_occ_a(m,s) × t_occ_s(j,h)), (38) p. 61. Le moteur le fait dans `scenarios.tertiaire` l. 139 à 144 (`n = aire * l["occupants"] * occupation * h * a`), et `Scenario.occupants` en est la somme sur les locaux.
- Usages 1 et 2 : adultes équivalents (32) à (37) p. 60 et 61 (`calendrier.adultes_equivalents` l. 49 à 61).
- Nombre de personnes de la zone pour les déplacements : NB_z = Max_année(Σ_l Nocc_l), (2280) p. 1305, « avec Nocc_l nombre d'occupants conventionnels calculé dans le chapitre C_EIN_Scénarios conventionnels ». C'est donc `max(sc.occupants)` pour une zone tertiaire, pas le champ `Nocc` saisi. Le moteur lit aujourd'hui `z.nombre("Nocc")` pour les usages autres que 1 et 2 (`ascenseurs.occupants_conventionnels`, l. 95) : lecture à confronter au texte sur le banc des bureaux (point ouvert P2).
- Valeur de contrôle, calculée avec (38) et (2280) sur le tableur, en occupants par m² de surface utile de la zone (nombre d'heures de l'année où ce maximum est atteint en commentaire) :

```python
# densité maximale d'occupants de la zone, occ/m² SU : max sur l'année de somme_l Nocc_l, (38) p. 61 et (2280) p. 1305,
# tableur du 29/04/2026. Valeur de contrôle : le moteur recalcule max(sc.occupants) et ne recopie pas ce dict.
DENSITE_MAX = {
    3: 0.08246,   # 1 155 h
    4: 0.47920,   # 272 h
    5: 0.26175,   # 525 h
    6: 0.09900,   # 768 h
    7: 0.25925,   # 850 h
    8: 0.03640,   # 1 095 h
    9: 0.02730,   # 1 095 h
    10: 0.20873,  # 730 h
    11: 0.09858,  # 365 h
    12: 0.23805,  # 360 h
    13: 0.33040,  # 2 190 h
    14: 0.53900,  # 231 h
    15: 0.33040,  # 1 460 h
    16: 0.33040,  # 1 252 h
    17: 0.19350,  # 156 h
    18: 0.05000,  # 4 224 h
    19: 0.04635,  # 462 h
    20: 0.17450,  # 2 555 h
    21: 0.25250,  # 1 305 h
    22: 0.12237,  # 231 h
    23: 0.09400,  # 1 536 h
    24: 0.09400,  # 1 536 h
    25: 0.08000,  # 4 224 h
    26: 0.53900,  # 180 h
    27: 0.43120,  # 180 h
    28: 0.08000,  # 4 224 h
}
```

### 3.4 Nombre d'occupants saisi pour l'indicateur par occupant (fiche 13.6)

- Nocc_zn est une « balise ajoutée au niveau de la zone » (p. 1405). Champ lu par le moteur dans les RSEE : `Nocc` sur `Zone` (`ascenseurs.py` l. 95). Nocc_bat = Σ Nocc_zn (2552) p. 1405 ; Cep_annuel_par_occ_bat = Cep_annuel_bat × SREF_bat / Nocc_bat, 0 si Nocc_bat = 0, (2553) p. 1406.
- Règle de saisie (p. 1405) : résidentiel, nombre d'occupants égal au nombre de pièces principales du logement, tableau 342 (1 pièce : 1 ... 7 pièces : 7) ; tertiaire, « les valeurs d'occupation issues des scénarios conventionnels peuvent être utilisées », sans dire laquelle (maximum, moyenne, Nocc_nom) ; enseignement, « nombre d'élèves prévu lors de la programmation ». Rien n'est à calculer par le moteur pour les usages 4 à 28 : Nocc est une saisie. Point ouvert P3 : valeur par défaut quand la balise est vide ou nulle.

## 4. Mobilité Uk (fiche 4.1, (31) p. 60)

U_k(m,s,j,h) = p_mob_a(m,s) × p_mob_s(j,h), (31) p. 60. Les profils sont le tableau « mobilité » de chaque feuille du tableur (hebdomadaire 7 jours × 24 cases, annuel 5 semaines × 12 mois), présent pour les 28 usages. La fiche 10.1 (p. 1303) et la fiche 10.2 (p. 1313) renvoient à ce tableau ; la fiche 7.2 (p. 503) s'en sert pour les parties communes. Rien à transcrire : `scenarios._tableau(usage, "mobilit")` le lit (l. 34 à 38) ; il manque seulement une fonction qui en fasse la série horaire (voir « Où coder »).

Pour contrôle, somme des poids hebdomadaires et heures équivalentes de pleine mobilité par an (produit hebdomadaire × annuel sur les 8 760 heures, calendrier `calendrier.construire()`) :

| Usage | Σ hebdo | h-équivalentes/an | Usage | Σ hebdo | h-équivalentes/an |
|---|---|---|---|---|---|
| 1 | 10,25 | 534,5 | 15 | 17,15 | 894,3 |
| 2 | 10,25 | 524,2 | 16 | 14,70 | 766,9 |
| 3 | 17,00 | 836,4 | 17 | 22,80 | 1 189,4 |
| 4 | 3,25 | 128,4 | 18 | 0,00 | 0,0 |
| 5 | 6,70 | 271,4 | 19 | 42,00 | 2 190,0 |
| 6 | 21,15 | 1 082,2 | 20 | 17,85 | 930,7 |
| 7 | 33,00 | 1 722,1 | 21 | 27,90 | 1 455,5 |
| 8 | 56,00 | 2 920,0 | 22 | 23,10 | 1 204,5 |
| 9 | 56,00 | 2 920,0 | 23 | 16,80 | 867,6 |
| 10 | 28,00 | 1 460,0 | 24 | 17,00 | 878,9 |
| 11 | 28,00 | 1 460,0 | 25 | 32,00 | 1 568,0 |
| 12 | 3,50 | 154,4 | 26 | 7,00 | 358,4 |
| 13 | 25,20 | 1 314,0 | 27 | 14,00 | 730,8 |
| 14 | 7,00 | 358,4 | 28 | 32,00 | 1 568,0 |

L'usage 18 (vestiaires seuls) a une mobilité identiquement nulle (tableur, feuille VES : les 168 cases hebdomadaires à 0) : (2306) divise par Σ_h U_i(h) = 0 pour une cabine qui ne dessert que des zones 18 (point ouvert P4). Les usages 20 et 23 n'ont jamais de mobilité nulle : usage 20 (feuille SAN_N), U_k de 0,1 à 0,15 toutes les heures (profil annuel constant à 1) ; usage 23 (feuille IND_3x8), U_k de 0,05 à 0,1 (hebdomadaire constant à 0,1, annuel de 0,5 à 1).

## 5. Ascenseurs (fiche 10.1) et escalators (fiche 10.2)

### 5.1 Besoin de voyages par personne et par an, tableau 310 p. 1300 et 1301

```python
# tableau 310, p. 1300 et 1301 : voyages par personne et par an, par usage de la zone. L'usage 1 n'y figure pas.
BV = {
    2: 1582.4, 3: 1731.9, 4: 804.0, 5: 1206.0, 6: 1608.0, 7: 1608.0,
    8: 2920.0, 9: 2920.0, 10: 2920.0, 11: 2920.0, 12: 924.0,
    13: 2190.0, 14: 510.0, 15: 1460.0, 16: 1248.0, 17: 4158.0, 18: 402.0,
    19: 2190.0, 20: 4380.0, 21: 2920.0, 22: 7665.0, 23: 2190.0, 24: 1040.0,
    25: 2680.0, 26: 402.0, 27: 1206.0, 28: 2680.0,
}
# usage 1 : non spécifié (absent du tableau 310)
```

Le moteur porte `BV = {2: 1600.0, 3: 1700.0}` (`ascenseurs.py` l. 27), valeurs de la version 2022 (`texte_annexe3/010_1_C_Bat_Ascenseurs.txt` l. 808 à 812 : 1600 et 1700). Le texte 2026 écrit 1582,4 et 1731,9. Les usages 2 et 3 ont été validés au banc avec 1600 et 1700 ; la version du moteur qui a produit les RSEE du banc n'est établie par aucune des sources lues ici (point ouvert P5). La fiche 10.2 (p. 1313) renvoie au « tableau 311 » pour les escalators : c'est le même tableau Bv.

### 5.2 Chaîne de calcul dépendant de l'usage (p. 1304 à 1308)

1. Q_z = Σ_i Q_i C(i,z) (2279) ; NB_z = Max_année(Σ_l Nocc_l) (2280) (section 3.3) ; BV_z = BV(k) (2281).
2. BVNB_i = Σ_z C(i,z) × Q_i / Q_z × BV_z × NB_z (2282) ; Ndem_i = BVNB_i × Mpass / (Q_i × 0,2) (2283), avec Σ X × S(direction, X) = 0,2 (2284).
3. Durées d'immobilité de nuit, (2294) à (2297) p. 1306 : Timmob_n_z = 8 × 365 × 3600 s « pour les zones de typologie habitation » (2294) ; Timmob_n_z = (12 × 365 + 52 × 48 + 9 × 24) × 3600 s « pour toutes les zones qui ne sont pas des zones d'habitation » (2295) ; pour une cabine desservant plusieurs zones, Timmob_n_i = Σ_z C(i,z) × Q_i / Q_z × Timmob_n_z (2296) ; Timmob_j_i = max(0, Timmob_i − Timmob_n_i) (2297).

```python
# (2294), (2295) p. 1306 : durée d'immobilité de nuit, s par an, selon que la zone est « habitation » ou non.
# Lecture « habitation » = usages 1 et 2 (celle du moteur, ascenseurs.py l. 112) ; voir point ouvert P1.
T_NUIT_HABITATION = 8 * 365 * 3600.0
T_NUIT_AUTRE = (12 * 365 + 52 * 48 + 9 * 24) * 3600.0
HABITATION = {u: (u in (1, 2)) for u in range(1, 29)}
```

   La formule (2296) ne se réduit pas à une moyenne pondérée : pour une cabine qui dessert seule deux zones (Q_i = Q_z1 = Q_z2), elle donne Timmob_n_z1 + Timmob_n_z2, soit plus d'un an pour deux zones non résidentielles. Le moteur prend aujourd'hui un seul booléen pour la cabine (toutes les zones desservies en 1 ou 2, sinon « non habitation », l. 112). Point ouvert P6.

4. Énergie de mobilité Emoy_i (2299) à (2301) p. 1306 et 1307, consommations Etm_i (2302), Eti_i (2303), Etot_i (2304) : indépendantes de l'usage. Rien à changer dans `ascenseurs.cabine` (l. 60 à 83) ; le texte 2026 reprend les signes incohérents de (2299) et (2300) déjà relevés dans `docs/lectures.md`.
5. Sorties horaires (p. 1307 et 1308), nécessaires aux sorties mensuelles de la zone et à l'autoconsommation (13.4) : U_i = Σ_z C(i,z) × Q_i / Q_z × U_z (2305) ; Fmob_i(h) = U_i(h) / Σ_t U_i(t) (2306) ; Fimob_i(h) selon (2307), dont l'impression est brouillée (« 1/365 · Tmobh − Fmob(h) / 24 Tmobh − 1 ») ; Pcab_i(h) = Fimob_i(h) × Eti_i + Fmob_i(h) × Etm_i (2308) ; Pcab_z(h) = Σ_i Pcab_i(h) × C(i,z) Q_z / Σ_j C(i,j) Q_j (2309) ; Wef_ascenseurs_z(h) = Pcab_z(h) × 1 h (2310). Lecture proposée pour (2307), qui rend Σ_h Fimob_i(h) = 1 et Fimob nul aux heures de pleine mobilité : Fimob_i(h) = (1/365 − Tmobh_i × Fmob_i(h)) / (24 − Tmobh_i), avec Tmobh_i en heures par jour (2292). Point ouvert P7.

### 5.3 Constantes : deux jeux dans le texte

La nomenclature (tableau 309, p. 1298 et 1299) écrit Tempec = 13 s, Mpass = 120 kg, Pveilleporte = 75 W ; le paragraphe des constantes (p. 1300) écrit Tempec = 120 s, Mpass = 75 kg, Pveilleporte = 13 W. Le moteur suit le paragraphe des constantes (`M_PASS = 75`, `P_VEILLE_PORTE = 13`, l. 21 et 22). FA08 (p. 3) confirme cette lecture : ses puissances de veille par défaut 243, 313 et 383 W + 2 W par palier valent Pman 75 + Pindcab 5 + Palarm 10 (tableau 316 p. 1303) + Pveilleporte 13 (paragraphe des constantes p. 1300) + Pec 140, 210 ou 280 selon Q (tableau 315 p. 1303), les 2 W par palier étant Pindpal (tableau 316 p. 1303) × (netage + 1). Rien à changer.

### 5.4 Ascenseurs partagés (FA08, p. 3 et 4)

Un ascenseur desservant plusieurs bâtiments ou un bâtiment mixte est saisi dans chaque bâtiment avec ScVeille = 1 et Pti, dP1, dP2 au prorata de la SREF desservie dans le bâtiment (Pti_bat = Pti_tot × Sref_bat / Σ Sref ; par défaut Pti_tot = {243, 313, 383 selon Q} + (netage + 1) × 2), T1 et T2 inchangés (86 400 s par défaut), netage propre au bâtiment. C'est une règle de saisie : le moteur lit les valeurs saisies ; rien à coder, sauf à vérifier qu'avec ScVeille = 1 les cinq champs `Pti`, `dP1`, `T1`, `dP2`, `T2` sont lus (`ascenseurs.cabine` l. 64 et 65 : oui).

### 5.5 Escalators (fiche 10.2, p. 1309 à 1315)

Même dépendance à l'usage : Bv(k) du tableau 310 (p. 1313 « tableau 311 ») ; NB_z = Max_année(Σ_l Nocc_l), identique à (2280), équation (2315) p. 1315 ; BV_z = BV(k) (2316) p. 1315 ; BVNB = Σ_z C(z) × BV_z × NB_z (2317) p. 1315, la p. 1314 n'en portant que l'annonce (vecteur de connexion C(z)) ; tableau Uk de mobilité (p. 1313). Constantes propres : R_m = R_d = 0,8 (tableau 319 p. 1313), Mpass = 75 kg, g = 9,81. Le moteur n'a pas de module escalators (`banc/deplacement.py` l. 24 et 25 : « escalator non traité ») ; cette spécification ne couvre que la part de la fiche qui dépend de l'usage.

## 6. Éclairage des parties communes (fiche 7.2, p. 502 et 503)

- P_ef_ecl_parties_communes = 2,19 W/m² SREF (791) p. 503 (tableau 80 p. 502 : constante).
- Si Usage_zone = 2 : W_cef_ecl_parties_communes_z(h) = 2,19 × p_mob_a × p_mob_s × SREF_zn (792) ; sinon 0 (793), p. 503. « Cette consommation n'est calculée que pour l'usage logement collectif » (p. 503). Réponse à la question posée : oui, logement collectif seulement.
- Profil : « calqué sur celui de la mobilité des ascenseurs pour les logements collectifs » (p. 503), soit U_k de l'usage 2 (section 4), 524,2 heures équivalentes par an, ce qui donne 2,19 × 524,2 / 1000 = 1,148 kWh/m² SREF par an pour une zone d'usage 2.
- Annuel : Cef_circ_ecl_annuel_z = Σ_h W(h) / SREF_bat (794) p. 503 : la division se fait par la SREF du bâtiment, pas celle de la zone, alors que (792) multiplie par SREF_zn. Le poste est ajouté au poste éclairage de la zone, (2510) p. 1391.

```python
# fiche 7.2, (791) à (793) p. 503 : puissance surfacique de l'éclairage des circulations, par usage
P_ECL_PARTIES_COMMUNES = {u: (2.19 if u == 2 else 0.0) for u in range(1, 29)}   # W/m² SREF
```

Le moteur n'a pas ce poste (grep « parties_communes », « 2.19 » : rien). Le constat du banc écrit dans `ascenseurs.py` l. 13 et 14 (« dans les RSEE, le poste déplacement contient aussi l'éclairage et la ventilation des parkings ») laisse ouverte la question du poste où les logiciels rangent les parties communes (point ouvert P9).

## 7. Parkings (fiches 10.3 et 10.4)

### 7.1 Typeusage du parking selon l'usage de la zone (p. 1319 et 1320)

« La valeur à adopter pour Typeusage est déterminée à partir de l'usage de la zone de bâtiment associée au parking » (p. 1319). Codes : 0 bureau, 1 commerce, 2 habitat (nomenclature p. 1321 et 1328 ; mêmes codes dans le champ `Type_Usage` des RSEE, `parkings.py` l. 9).

```python
# fiche 10.3, tableau sans numéro p. 1319 et 1320 : Typeusage du parking (0 bureau, 1 commerce, 2 habitat) par usage de la zone
TYPE_USAGE_PARKING = {
    1: 2, 2: 2, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 2, 9: 2, 10: 2, 11: 2, 12: 0,
    13: 1, 14: 0, 15: 1, 16: 1, 17: 1, 18: 0, 19: 0, 20: 1, 21: 1, 22: 1,
    23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 1,
}
```

Dans le RSEE, `Type_Usage` est un paramètre d'intégration saisi (p. 1321, p. 1328). Le dict sert de valeur par défaut quand le champ manque et de contrôle de cohérence quand il est présent ; la fiche 10.4 (p. 1327) renvoie au « Tableau 322 » pour cette passerelle, mais le tableau 322 est la nomenclature (p. 1329) : la passerelle est le tableau sans numéro de la fiche 10.3.

### 7.2 Règles qui dépendent de Typeusage

- Plages d'ouverture par défaut (p. 1331) : habitat, NbjO(j) = 1 tous les jours, PlagOse = PlagOwe = {0 ; 23} (24 h/24) ; bureau, NbjO = 1, PlagOse = {9 ; 18} « (9h, 19h) », PlagOwe = {0 ; 0} (jamais ouvert le week-end) ; commerce, NbjO = 1, PlagOse = PlagOwe = {7 ; 21} « (7h à 22h) », fermé le dimanche par l'algorithme de Ouv(h) (p. 1332 : « si typeusage = commerce et jsem = 7 alors Ouv(h) = 0 »). Le moteur : `OUVERTURE` l. 21 (9 à 19, 7 à 22, 0 à 24) et l. 54 et 55 (dimanche). L'écriture « {9 ; 18} (9h, 19h) » avec Hleg ∈ [PlagOse[ laisse une ambiguïté d'une heure que le moteur a tranchée à 19 h (point ouvert P10).
- Détection de présence par défaut : PlagDse = PlagDwe = {0 ; 0}, aucune (p. 1331) ; TauDet = 0,2 (2348) p. 1330 ; Ex (extinction à la fermeture) saisi.
- Puissance d'éclairage par défaut : Pecins = Npl × 75 W en intérieur (2349), Npl × 8 W en extérieur (2350), p. 1331. Fhext tableau 323 p. 1330 ; Fhint = 1 (2347).
- Mouvements par place Rmvtpl(h), tableau 321 p. 1324, par Typeusage et heure légale de fin de pas (8 à 24), nul de 0 h à 8 h quel que soit l'usage (p. 1324). Ce que le texte 2026 imprime, cellules fusionnées sans les heures : bureaux « 0 0,308 0,154 0 0,154 0 0,308 0 », usage d'habitation « 0,19 0,095 0,19 0,095 0 », commerce « 0,278 0,556 0,278 0 ». L'affectation heure par heure est **non spécifiée** par le texte 2026 : elle vient de l'image de la version 2022 relevée par le moteur (`parkings.RMVTPL` l. 26 à 30 : bureau 0,308 de 9 h à 11 h, 0,154 à 12 h, 0 à 13 h, 0,154 à 14 h et 15 h, 0 à 16 h, 0,308 à 17 h et 18 h ; habitat 0,19 de 8 h à 10 h, 0,095 de 11 h à 16 h, 0,19 de 17 h à 19 h, 0,095 de 20 h à 22 h ; commerce 0,278 à 8 h, 0,556 de 9 h à 20 h, 0,278 à 21 h et 22 h), cohérente avec les séquences imprimées mais non vérifiable sur le texte 2026 ; à garder « non validé » dans le code (point ouvert P15).
- Ventilation (p. 1323 à 1326) : hors habitat, débit requis par le CO, (2335) à (2342), constantes tableau 320 p. 1322 ; habitat, Pvent600 × Npl × Rutil × Rmvtpl(h) si régulé (2343), permanent sinon (2345). Valeurs par défaut (2326) p. 1324 : Dvent2 = 900 Npl, Dvent1 = 450 Npl, Pvent2 = 40 Npl, Pvent1 = 5 Npl, Pvent600 = 40 W/place.

### 7.3 Règles communes qui ne dépendent pas de l'usage mais que les usages 4 à 28 rendent fréquentes

- Nombre de places Npl (p. 1323 et 1330) : deux-roues motorisés 0,33 place (arrondi à l'entier supérieur sur leur total), deux-roues non motorisés 0, autres 1 ; Npl réel admis.
- Parking associé à des zones de Typeusage différents : « créer un objet parking pour chaque typologie d'usage », places affectées selon le programme ou réparties au prorata des SREF des zones regroupées par type (p. 1323 et 1330). C'est une règle de saisie ; le moteur peut la contrôler (Σ Npl des parkings par type contre les SREF par type) mais n'a pas à la faire.
- Répartition de la consommation : la fiche 10.4 la définit « au niveau du projet », « entre chaque zone des bâtiments, au prorata de sa surface SREF » (p. 1327, 1333) ; la fiche 10.3 écrit « au prorata des surfaces S_RT des différentes zones du bâtiment » (p. 1326). Le moteur répartit au niveau du projet (`parkings.du_projet` l. 87 à 94). La consommation est ajoutée au poste éclairage (2510) et au poste auxiliaires de ventilation (2511) de la zone, p. 1391 ; le banc a constaté qu'elle est dans le poste déplacement des RSEE (`parkings.py` l. 5 à 7).

## 8. Auxiliaires de ventilation des usages non résidentiels (fiche 6.5)

- Simple flux par extraction ou insufflation, non résidentiel : Pvent = Pvent_occ si Ivent vrai, Pvent_inocc sinon, (636) à (639) p. 407 ; résidentiel : moyenne hebdomadaire par Dugd, (640), (641), (643) ; répartition par groupe au prorata des débits spécifiques repris (642) ou soufflés (644) « en résidentiel et en non résidentiel » ; Cvent = Pvent (645), (646) p. 408.
- Ivent(m,s,j,h) = p_vent_a × p_vent_s (45) p. 61, tableau « ventilation » du tableur, présent pour les 28 usages. Les plages de ventilation de chaque usage sont dans la synthèse p. 24 à 26 (colonne « horaire ventilation zone » : « idem occupation », « idem éclairage », ou plage propre, par exemple usage 22 « 5 h à 0 h »).
- Aucune constante par usage dans la fiche 6.5 : `consommation.puissance_ventilateurs` (l. 22 à 52) s'applique tel quel aux usages 4 à 28 dès lors que `usage in (1, 2)` reste le test du résidentiel (l. 42) et que `ivent` vient de `scenarios.tertiaire(cal, usage, surface).ventilation`. Les consommations d'auxiliaires de ventilation du groupe ajoutent les ventilateurs locaux des émetteurs et les auxiliaires de la génération d'air, (2504) p. 1390.
- Les débits eux-mêmes (fiche 5.6, (399) à (408) ; `groupe.DEBIT_CONVENTIONNEL = {3: 4.0}` l. 27 et `DEBIT_INOCCUPATION` l. 28 ; `ventilation._debit_bouche` l. 73) relèvent du thème ventilation : non traités ici.

## 9. Usages mobiliers (fiche 4.7, p. 95 et 96)

- Cef_us_mob_loc(h) = A_loc × Qmax_proc_loc × t_a_ch(m,s) × t_s_ch(j,h) (93) ; Cef_us_mob_z(h) = Σ_loc (94) ; annuel Σ_h, en kWh/m² SREF (95). « Par convention, les consommations électriques des équipements mobiliers sont considérées égales aux valeurs d'apports internes de chaleur non dus aux occupants » (p. 95).
- C'est exactement `Scenario.apports_usages` (41) et (42) calculé par `scenarios.tertiaire` l. 145 et 146 (usages 3 à 28) et `scenarios.habitation` l. 97 (usages 1 et 2 : 5,7 W/m² en occupation, 1,1 W/m² sinon, p. 21). Le moteur l'a déjà : `bilans.mobilier(apports_usages, surface)` l. 50 ; `banc/bilans.py` le compare à `O_Cef_imp_mobilier_annuel` par usage. Les valeurs par local sont les deux dernières colonnes de `LOCAUX` (section 3.2).
- Le poste mobilier n'entre ni dans O_Cef_[energie]_annuel ni dans Cep, (2446) p. 1374, (2478) p. 1377 ; il figure dans O_Cef_imp_mobilier_annuel de la zone et du bâtiment et dans W_elec_tous_usages pour l'autoconsommation, (2515), (2519), (2527) p. 1391 à 1394.

## 10. Éclairage des locaux (fiche 7.1) : entrées par type de local de chaque usage

### 10.1 Règles

- Mode Th-B, usages autres que 1 et 2 : Pecl_tot = 2 × Eiref / 100 W/m², Pecl_aux = 0, Gest_ecl = 2, Grad_ecl = 1, fr_Grad_Ecl = 1 (782) p. 481 ; usages 1 et 2 : 1 W/m², Gest_ecl = 1, Grad_ecl = 1, fr_Grad_Ecl = 0 (781).
- Mode Th-C : les caractéristiques saisies par local (Pecl_tot, Pecl_aux, Gest_ecl, Grad_ecl, Ratio_ecl_nat, Fr_Grad_ecl) ; commerces, local aire de vente ou petit magasin : Pecl_tot = max(4,5 ; Pecl_tot) (p. 481) ; bureaux, local bureaux : complément mobilier Pecl_mob = (Eiproj − Ecl_immo_projet)/100 × Eff_ecl_mob si Pecl_immo < 10 W/m² et Ecl_immo_projet < Eiproj (p. 481 et 482).
- C1 : 1 si Gest_ecl = 0 (p. 487) ; sinon tableau 78 (p. 488 à 491, appelé « tableau 79 » dans le corps du texte p. 488) par type de zone et de local. Eiref du même tableau sert à C2 (tableau p. 493 et suivantes, déjà codé : `eclairage.c2_points` l. 67 à 79) et à (782).
- Locaux de grand volume (liste p. 482) : salle de sport des usages 25 et 28, aire de production des usages 23 et 24, aire de vente supérieure à 300 m² de l'usage 17 ; ils prennent Einat = Einat(1) + Einat(0), (783) p. 483, avec les constantes « gv » du tableau 77 (p. 479), les autres locaux Einat(2), (784) p. 483, avec les constantes « pv ».

```python
# fiche 7.1, liste p. 482, (783) et (784) p. 483 : locaux de grand volume (baies de type 0 ou 1, constantes « gv » du tableau 77 p. 479)
GRAND_VOLUME = {
    17: ("Aire de vente (supérieure à 300 m2)",),
    23: ("Aire de production",), 24: ("Aire de production",),
    25: ("Salle de sport",), 28: ("Salle de sport",),
}   # autres usages : aucun
```

### 10.2 Tableau 78 (p. 488 à 491) : C1 selon Gest_ecl = 1, 2, 3, 4 et Eiref (lux), par usage et type de local

```python
# tableau 78, p. 488 à 491. Clé : usage -> {type de local: ((C1 Gest_ecl=1, =2, =3, =4), Eiref lux)}.
# Transcription littérale, fautes d'impression comprises (usage 3 salle de réunion « 50 » lux ; usage 18 « 0?75 0?7 » lu 0,75 et 0,70).
C1_EIREF = {
    3: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.70, 0.65, 0.60, 0.50), 50),
        "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    4: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
        "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300), "Salle de repos": ((0.60, 0.75, 0.70, 0.60), 300),
        "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    5: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300),
        "Salle d'enseignement informatique": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de conférence Salle polyvalente": ((0.80, 0.75, 0.70, 0.60), 300),
        "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Salle des professeurs": ((0.80, 0.75, 0.70, 0.60), 300), "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100),
        "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    6: {"Salle multi-fonctions": ((0.80, 0.75, 0.70, 0.60), 300), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
        "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
        "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200)},
    7: {"Salle de classe": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de conférence Amphithéâtre": ((0.80, 0.75, 0.70, 0.60), 300),
        "Salle d'enseignement informatique": ((0.95, 0.90, 0.85, 0.75), 300), "Centre de documentation": ((0.80, 0.75, 0.70, 0.60), 500),
        "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 300),
        "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
        "Local service": None},   # non spécifié : local présent dans les scénarios (ratio 0,15), absent du tableau 78 pour cet usage
    8: {"Chambre sans cuisine avec salle de bain": ((0.60, 0.55, 0.50, 0.40), 70), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100)},
    9: {"Chambre sans cuisine avec salle de bain": ((0.60, 0.55, 0.50, 0.40), 70), "Sanitaires collectifs": ((1.00, 0.95, 0.90, 0.80), 150),
        "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100)},
    10: {"Bureau standard": ((0.80, 0.75, 0.70, 0.60), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Salle petits déjeuners": ((1.00, 1.00, 1.00, 1.00), 200)},
    11: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Bar": ((1.00, 1.00, 1.00, 1.00), 200),
         "Salle petits déjeuners": ((1.00, 1.00, 1.00, 1.00), 200), "Salle de séminaires réunion": ((0.80, 0.75, 0.70, 0.60), 500)},
    12: {"Salle de jeux": ((0.95, 0.90, 0.85, 0.75), 300), "Salle de repos": ((0.80, 0.75, 0.70, 0.60), 300),
         "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Salle de réunion": ((0.80, 0.75, 0.70, 0.60), 500),
         "Circulation Accueil": ((0.60, 0.55, 0.50, 0.40), 100), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    13: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    14: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    15: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    16: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    17: {"Aire de vente (inférieure à 300 m2)": ((1.00, 1.00, 1.00, 1.00), 300), "Aire de vente (supérieure à 300 m2)": ((1.00, 1.00, 1.00, 1.00), 300),
         "Circulation Accueil": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    18: {"Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200)},   # le scénario nomme le second local « Sanitaires vestiaires »
    19: {"Chambres sans cuisine avec salle de bain": ((1.00, 1.00, 1.00, 1.00), 70), "Circulation accueil": ((1.00, 1.00, 1.00, 1.00), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Salle commune": ((0.80, 0.75, 0.70, 0.60), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500)},
    20: {"Chambres sans cuisine avec salle de bain": ((1.00, 1.00, 1.00, 1.00), 70), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200), "Circulation accueil": ((1.00, 1.00, 1.00, 1.00), 200),
         "Locaux soins et offices": ((1.00, 1.00, 1.00, 1.00), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Salle d'attente et de consultation (urgences)": ((1.00, 1.00, 1.00, 1.00), 500), "Aire de production": ((1.00, 0.95, 0.90, 0.80), 500)},
    21: {"Aire de production": ((1.00, 0.95, 0.90, 0.80), 500), "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200),
         "Circulation accueil": ((1.00, 1.00, 1.00, 1.00), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Salle d'attente et de consultation": ((1.00, 1.00, 1.00, 1.00), 500), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Salle de réunion": ((0.70, 0.65, 0.60, 0.50), 500)},
    22: {"Espace voyageurs": ((1.00, 1.00, 1.00, 1.00), 200), "Circulation Accueil": ((1.00, 0.75, 0.70, 0.60), 150),
         "Commerces": ((1.00, 1.00, 1.00, 1.00), 300), "Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500),
         "Inspection filtrage": ((1.00, 1.00, 1.00, 1.00), 500), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200)},
    23: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Aire de production": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    24: {"Bureau standard": ((0.90, 0.85, 0.80, 0.70), 500), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Aire de production": ((1.00, 1.00, 1.00, 1.00), 300), "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200),
         "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    25: {"Salle de sport": ((0.90, 0.85, 0.80, 0.70), 300), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Sanitaires collectifs": ((0.70, 0.65, 0.60, 0.50), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},   # le scénario nomme les sanitaires « Sanitaires vestiaires »
    26: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    27: {"Salle restaurant": ((1.00, 1.00, 1.00, 1.00), 200), "Cuisine": ((1.00, 1.00, 1.00, 1.00), 200), "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
    28: {"Salle de sport": ((0.90, 0.85, 0.80, 0.70), 300), "Circulation Accueil": ((0.80, 0.75, 0.70, 0.60), 100),
         "Sanitaires vestiaires": ((0.70, 0.65, 0.60, 0.50), 200), "Douches collectives": ((0.70, 0.65, 0.60, 0.50), 200),
         "Local service": ((0.06, 0.05, 0.04, 0.02), 200)},
}
# usages 1 et 2 : éclairage entièrement conventionnel (781) p. 481, pas de type de local
```

Le moteur code l'usage 3 par les codes 0 à 3 du champ `Locaux_Bureau` de l'entrée `Eclairage` (`eclairage.LOCAUX_BUREAU` l. 45, `C1_BUREAU` l. 62 et 63, avec Eiref = 500 lux pour la salle de réunion là où le texte 2026 imprime 50). Pour les usages 4 à 28, le code numérique qui désigne chaque type de local dans le RSEE est **non spécifié** (aucun schéma, aucun RSEE) ; le moteur ne peut lire ces locaux que par leur nom ou par un code dont la correspondance sera à déduire au premier RSEE disponible.

## 11. Besoins d'ECS : unité Nu et besoin unitaire a (fiche 9.6, tableau 277, p. 1053 à 1055)

Pour mémoire (le thème ECS détaille la fiche 9.6) : pour les usages 3 à 28, Nu est un paramètre d'intégration (p. 1055) dont l'unité est « m² de surface utile » pour tous (tableau 277), et a est fixé par usage. Champ lu par le moteur : `nu_gr_em_e` de l'émetteur ECS équivalent (`ecs.volume_hebdomadaire` l. 50) ; sa cohérence avec A_gr,em-e = Rat_em-e × A_gr (1682) n'est pas imposée par le texte (point ouvert P12).

```python
# tableau 277, p. 1053 et 1054 : litres d'eau à 40 °C par semaine et par m² de surface utile (Nu = m² de surface utile)
A_TERTIAIRE = {
    3: 1.25, 4: 0.2, 5: 0.2, 6: 0.2, 7: 0.2, 8: 22.873, 9: 18.98, 10: 5.694, 11: 4.76, 12: 0.714,
    13: 19.5, 14: 2.2, 15: 5.3, 16: 19.5, 17: 0.24, 18: 79.0, 19: 2.8, 20: 1.68, 21: 25.2, 22: 0.24,
    23: 0.24, 24: 0.24, 25: 13.2, 26: 4.5, 27: 9.8, 28: 33.9,
}   # usages 1 et 2 : adultes équivalents, (1683) à (1690) p. 1055 et 1056
```

Usage 16 : 19,5 dans le texte (tableau 277 p. 1054 et synthèse p. 25), 4,7 dans le tableur (feuille RES_2RJ-6J7). Point ouvert P11.

## 12. Données d'entrée du récapitulatif propres aux zones et groupes non résidentiels

Sans schéma XSD, la seule liste disponible est celle des champs que le moteur lit déjà. Pour les usages 4 à 28, tout ce qui est marqué « non spécifié » devra être lu au premier RSEE d'un logiciel évalué.

| Nœud | Champ lu par le moteur | Sens, fiche | Usages 4 à 28 |
|---|---|---|---|
| Zone | `Usage` | numéro d'usage, tableau 4 p. 57 | identique ; valeurs 4 à 28 attendues |
| Zone | `Nocc` | nombre d'occupants saisi, 13.6 p. 1405 | identique (section 3.4) |
| Zone | `NB_logement` | nombre de logements, (32) à (36) | sans objet hors 1 et 2 |
| Zone | `Is_Traversant`, `Hauteur_Zone` | aéraulique 5.6 | identiques (thème ventilation) |
| Zone | `Ventilation_Mecanique` (`Index`, `Pvent_rep_occ`, `Pvent_rep_inocc`, `Pvent_souf_occ`, `Pvent_souf_inocc`) | 6.5 (636) à (639) | identiques ; noms des champs tertiaires déjà lus sur les bureaux (`consommation.py` l. 50) |
| Groupe | `SU` (3 à 28) ou `SHAB` (1 et 2) | SREF (2412), (2413) | `SU` attendu ; non vérifié (P8) |
| Groupe | `Is_Climatise`, `Categorie_CE`, `Exp_BR_Groupe`, `S_combles` | exigences, confort | identiques |
| Groupe / Eclairage | `Locaux_Bureau`, `Rat_local`, `Ratio_ecl_nat`, `Gest_Ecl`, `Grad_Ecl`, `Pecl_tot`, `Pecl_aux`, `Fr_Grad_Ecl` | 7.1, tableau 77 p. 476 et 477 | codes des types de locaux non spécifiés hors usage 3 ; les autres champs sont identiques |
| Groupe / émetteur ECS | `Rat_em_e`, `nu_gr_em_e`, `app_ecs`, `part_em_e_melangeurs`, `part_em_e_mitigeur_thermo`, `part_em_e_temporisateur` | 9.5, 9.6 | `nu_gr_em_e` en m² SU (section 11) |
| Groupe / Bouche_Conduit | `Type_Bouche_Conduit`, `Id_Systeme_Mecanique`, `Type_Regul_Res` (résidentiel), débits | 6.2, 6.5 | identiques (thème ventilation) |
| Batiment / Ascenseur | `TechMac`, `Q`, `V`, `H`, `Netage`, `Cp`, `ScVeille`, `Pti`, `dP1`, `T1`, `dP2`, `T2`, `C` (liste d'index de zones) | 10.1, tableau 309 p. 1296 et 1297 | identiques ; `C` doit pouvoir citer des zones d'usage 4 à 28 |
| Batiment / Escalator | non lus (`banc/deplacement.py` l. 24) | 10.2 | non spécifiés |
| Projet / Parking | `Type_Parking`, `Type_Usage`, `Npl`, `Net`, `Pec_ins`, `IsParamEclPuisDefaut`, `IsParamEclHdDefaut`, `PlagDse`, `PlagDwe`, `Ex`, `Vent`, `Reg`, `IsParamVentilationDefaut`, `IsParamVentilationHabDefaut`, `Dvent1`, `Dvent2`, `Pvent1`, `Pvent2`, `Pvent600` | 10.3, 10.4 | identiques ; `Type_Usage` à contrôler avec `TYPE_USAGE_PARKING` |

Le texte ne nomme aucun champ propre aux usages 4 à 28 dans les listes d'entrées des fiches 4.1 (p. 52 à 55), 7.1 (p. 475 à 477), 9.6 (p. 1050), 13.1 (p. 1356 et 1357) et 13.2 (p. 1366 et 1367) : les entrées sont les mêmes que pour les bureaux, seules leurs valeurs conventionnelles changent.

## 13. Sorties des fiches 13.1, 13.2, 13.4 et 13.6 pour une zone non résidentielle

### 13.1 Sortie_Zone_B et Sortie_Groupe_B (13.1, p. 1357)

- Par groupe, zone et bâtiment : B_Ch_mois, B_Fr_mois, B_Ecl_mois (12 valeurs), B_Ch_annuel, B_Fr_annuel, B_Ecl_annuel, Bbio_pts_mois, Bbio_pts_annuel, (2379) à (2386) p. 1359 et 1360, rapportés à SREF (SU pour 3 à 28). Noms observés dans les RSEE et écrits par le moteur : `O_B_Ch_mois`, `O_B_Fr_mois`, `O_B_Ecl_mois`, `O_B_Ch_annuel`, `O_B_Fr_annuel`, `O_B_Ecl_annuel`, `O_Bbio_pts_mois`, `O_Bbio_pts_annuel`, `O_SREF`, `O_SHAB`, `O_SU`, `Usage` (zone), `Is_Climatise` (groupe), `O_Bbio_Max` et ses modulations (`sortie_rsee._bloc_b` l. 70 à 96).
- Pour un groupe d'usage 3 à 28 : O_SREF = O_SU = SU_gr et O_SHAB = 0 (lecture du banc, `banc/sortie_rsee.py` l. 77 : `shab = s if usage in (1, 2) else 0.0`). Le texte ne dit pas si SHAB est écrit 0 ou omis (P8).
- Sorties de zone propres au 13.1 sans équation d'usage : surfaces d'enveloppe par m² SREF (2388) à (2399), perméabilité (2400), (2401), déperditions (2402) à (2408), débits moyens en occupation (2409) à (2411), p. 1360 à 1364. Leurs noms de champ ne sont pas dans le texte et le moteur ne les écrit pas : non spécifiés.

### 13.2 Sortie_Zone_C (13.2, p. 1368 et 1369 ; formules (2430) à (2461) p. 1373 à 1375)

- En-tête : SREF_zn, SHAB_zn, SU_zn, Usage.
- Annuels : O_Cef_annuel (2456), O_Cep_annuel (2457), O_Cep_annuel_occ (sans formule de zone, voir P3), O_Cep_nr_annuel (2458), O_Cef_imp_[poste]_annuel pour les huit postes ch, fr, ecs, ecl, auxvent, auxdist, déplacement, mobilier (2445), O_Cef_[energie]_imp_annuel hors mobilier (2446), O_Cef_imp_[poste]_[energie]_annuel (2441), (2442), O_Cef_cons_[poste]_elec_annuel (2443), sous-décompositions bois (2444), productions et autoconsommation PV et cogénération (2447) à (2455).
- Mensuels : O_Cef_imp_[poste]_[energie]_mois (2430), (2431), O_Cef_cons_[poste]_elec_mois (2432), productions (2433) à (2437), O_B_Ch_mois, O_B_Fr_mois, O_B_Ecs_mois (2438) à (2440) ; annuels des besoins (2459) à (2461).
- Les postes déplacement et mobilier n'existent qu'à partir de la zone : « au niveau groupe, les auxiliaires de déplacement et les consommations associées aux usages mobiliers ne sont pas définies » (p. 1371, 13.2.3.3) ; O_Cef_annuel et O_Cep_annuel du groupe sont « hors usages mobiliers et déplacement » (p. 1370). Bilans (13.4) : W_elec_cons[ecl]_zn = Σ_gr + parkings + parties communes (2510), W_elec_cons[auxvent]_zn = Σ_gr + ventilation des parkings (2511), W_elec_cons[depl]_zn = ascenseurs + escalators (2513), p. 1391.
- Noms observés dans les RSEE pour ces postes (lus par les bancs) : `O_Cef_imp_deplacement_annuel` (`banc/deplacement.py` l. 32, `banc/cep_total.py` l. 92), `O_Cef_imp_mobilier_annuel` (`banc/bilans.py` l. 68), `O_Cef_imp_auxvent_annuel`, `O_Cef_imp_auxdist_annuel` (`sortie_rsee.py` l. 188 et 205). Le moteur n'écrit pas encore, pour la zone : O_Cep_annuel, O_Cep_nr_annuel, O_Cep_annuel_occ, O_Cef_imp_deplacement_annuel, O_Cef_imp_mobilier_annuel, les O_Cef_cons_*, les mensuels par poste et énergie.
- Sortie_Batiment_C (p. 1367 et 1368, (2462) à (2492)) : mêmes grandeurs sommées sur les zones, plus O_Cep_annuel_occ = (2553) p. 1406 et O_Type_Reseau, O_RatENR_rdch, O_RatENR_rdfr.

### 13.3 Indicateur par occupant (13.6)

Au bâtiment : (2552), (2553) (section 3.4). À la zone : O_Cep_annuel_occ est listé p. 1368 (« ramenée au nombre d'occupant ») sans formule ; lecture par analogie, non spécifiée par le texte : O_Cep_annuel_zn × SREF_zn / Nocc_zn, 0 si Nocc_zn = 0 (P3).

## Points ouverts

Ce que le texte ne tranche pas ; ce qui se déduira au banc des bureaux seulement (B) ou restera non validé (NV).

- **P1 (NV)** « Habitation » de (2294) p. 1306 : usages 1 et 2 seulement (lecture du moteur l. 112), ou toute zone à ihebergement = 1 (8, 9, 19, 20, tableau 4 p. 57) ? La durée d'immobilité de nuit passe de 8 h à 12 h et plus selon la lecture. Même question pour « résidentiel » dans 6.5 et 13.1.
- **P2 (B)** NB_z des zones tertiaires, (2280) : maximum annuel de Σ Nocc_l calculé (lettre du texte, section 3.3 et `DENSITE_MAX`) ou champ `Nocc` saisi (lecture actuelle, `ascenseurs.py` l. 95, validée à moins de 4 % sur les zones sans parking). À trancher sur les RSEE de bureaux à ascenseur.
- **P3 (NV)** Nocc_zn vide ou nul en tertiaire : le texte dit « peuvent être utilisées » pour les scénarios (p. 1405) sans dire quelle valeur ; formule de O_Cep_annuel_occ à la zone absente (p. 1368). Proposition : max(sc.occupants) comme défaut et la formule du bâtiment transposée, les deux marquées non spécifiées.
- **P4 (NV)** Mobilité nulle de l'usage 18 : (2306) et la répartition (2305) à (2309) divisent par zéro pour une cabine ne desservant que des vestiaires. Le texte ne prévoit rien ; proposition : Fmob = 0, Fimob = 1/8760.
- **P5 (B)** Bv des usages 2 et 3 : 1582,4 et 1731,9 (tableau 310, 2026) contre 1600 et 1700 (2022, moteur l. 27, banc validé). Les versions de moteur qui ont produit les RSEE du banc et la date à partir de laquelle les logiciels appliquent les valeurs 2026 ne sont établies par aucune des sources lues ici (texte, tableur, fiches d'application, moteur, docs) : non spécifiées, à lire dans les en-têtes des RSEE eux-mêmes (`projet.version_moteur`, `projet.version_rsee`, `banc/sortie_rsee.py` l. 32 et 92). Garder 1600 et 1700 comme valeurs validées au banc ; passer aux valeurs 2026 par une option d'étude, à mesurer sur des RSEE dont l'en-tête montre un moteur postérieur à la publication du tableau 310 en vigueur.
- **P6 (NV)** (2296) ne donne pas une moyenne pondérée des Timmob_n_z (section 5.2). Lecture à retenir pour les cabines mixtes : moyenne pondérée par C(i,z) Q_z / Σ_j C(i,j) Q_j, cohérente avec (2309), ou lettre du texte.
- **P7 (NV)** Formule (2307) de Fimob brouillée à l'impression ; lecture proposée section 5.2. À vérifier dès qu'un RSEE porte des sorties mensuelles du poste déplacement.
- **P8 (NV)** Champ de surface des groupes d'usage 4 à 28 (`SU` attendu) et écriture de O_SHAB (0 ou absent) dans les sorties : aucun RSEE ne le montre.
- **P9 (B)** Poste des parties communes (7.2) et des parkings dans les RSEE : le texte les met dans éclairage et auxiliaires de ventilation ((2510), (2511)), le banc a vu les parkings dans le poste déplacement (`parkings.py` l. 5 à 7). À vérifier pour les parties communes sur les RSEE de logements collectifs (écart attendu de 1,15 kWh/m² sur le poste éclairage ou déplacement).
- **P10 (B)** Plage d'ouverture des parkings de bureau : « {9 ; 18} (9h, 19h) » p. 1331 ; le moteur prend 9 h à 19 h (l. 21). Mesurable sur les RSEE de bureaux à parking.
- **P11 (NV)** Trois écarts entre la synthèse du texte (p. 24 à 26, tableau 277 p. 1054) et le tableur approuvé par le chapitre 15 (p. 1409) : usage 11 salle petits déjeuners (44,3 et 4,43 W/m² contre 0), usage 12 salle de réunion (10 W/m² contre 0), usage 16 besoin d'ECS (19,5 contre 4,7 L/m²). Le moteur lit le tableur ; signaler l'écart dans `docs/lectures.md`.
- **P12 (NV)** `nu_gr_em_e` : le texte fait de Nu un paramètre d'intégration en m² SU sans lier sa valeur à Rat_em-e × A_gr (1682). Contrôle de cohérence seulement.
- **P13 (NV)** Tableau 78 : Eiref de la salle de réunion des bureaux imprimé « 50 » (le moteur a 500, banc validé) ; local service de l'usage 7 absent ; noms des sanitaires des usages 18 et 25 différents entre scénarios et tableau 78 ; codes numériques des types de locaux dans le RSEE inconnus hors usage 3.
- **P14 (NV)** Répartition des parkings au niveau du projet (10.4 p. 1327) ou du bâtiment (10.3 p. 1326) ; le moteur fait projet. Ne se tranche qu'avec un RSEE à plusieurs bâtiments et un parking.
- **P15 (NV)** Tableau 321 p. 1324 : le texte 2026 n'imprime que les trois séquences de Rmvtpl sans leurs heures (cellules fusionnées) ; l'affectation horaire de `parkings.RMVTPL` l. 26 à 30 vient de l'image de la version 2022 et n'est pas vérifiable sur le texte en vigueur. À garder « non validé » tant qu'un RSEE à parking ne confirme pas le profil horaire.

## Où coder

Lignes de la version du 09/10/2026 des fichiers.

**`openbce/scenarios.py`**
- l. 34 à 38 `_tableau` : rien à changer ; ajouter après `tertiaire` (l. 150) une fonction `mobilite(cal, usage) -> np.ndarray` qui renvoie U_k = hebdo × annuel du tableau « mobilité » (31), par `_horaire(cal, _tableau(usage, "mobilit"))`, NaN remplacés par 0. Sert à 7.2, 10.1 (2305) et 10.2.
- l. 55 à 72 `Scenario` : ajouter le champ `mobilite: np.ndarray | None = None`, rempli par `habitation` (l. 80 à 98) et `tertiaire` (l. 126 à 150).
- l. 126 à 150 `tertiaire` : déjà conforme à (38) pour les 28 usages ; NB_z = `float(sc.occupants.max())` (2280) n'a pas besoin d'un nouveau code, seulement d'un appel.

**`openbce/ascenseurs.py`**
- l. 27 `BV` : passer aux 27 valeurs du tableau 310 (section 5.1) sous une constante `BV_2026`, garder `BV_2022 = {2: 1600.0, 3: 1700.0}` et une option de module (P5) ; marquer 4 à 28 « non validé ».
- l. 32 `T_NUIT` : conserver ; ajouter `HABITATION` (section 5.2) et l'employer l. 112 à la place de `usages[z] in (1, 2)` (P1, P6).
- l. 86 à 96 `occupants_conventionnels` : pour `usage not in (1, 2)`, calculer `scenarios.tertiaire(cal, usage, surface_zone).occupants.max()` (2280) ; garder la lecture `Nocc` sous une option de module jusqu'au banc (P2). La fonction a besoin du calendrier : signature `occupants_conventionnels(batiment, cal)`.
- l. 99 à 116 `du_batiment` : supprimer le `NotImplementedError` des l. 109 et 110 une fois `BV` complet ; usage 1 : lever une erreur explicite (Bv non spécifié) ; garder (2282), (2283), (2309).
- Nouvelle fonction `profil_horaire(batiment, cal, conso_par_cabine) -> dict[int, np.ndarray]` : (2305) à (2310) avec `scenarios.mobilite` et la lecture de (2307) de la section 5.2 ; retourne Wef_ascenseurs_z(h). Point d'entrée pour les sorties mensuelles et pour (2513).
- Docstring l. 10 à 14 : la mention « nombre de personnes NB = adultes équivalents, pas le Nocc saisi » reste vraie pour 1 et 2 ; compléter pour 3 à 28 selon P2.

**`openbce/parkings.py`**
- l. 9 (docstring) et l. 21 `OUVERTURE` : conserver ; l. 26 à 30 `RMVTPL` : conserver avec la marque « non validé » (P15) ; ajouter `TYPE_USAGE_PARKING` (section 7.1) et une fonction `type_usage(zone_usage) -> int`.
- l. 47 à 61 `eclairage` et l. 64 à 84 `ventilation` : lire `Type_Usage` avec repli sur `type_usage(usage de la zone associée)` quand le champ manque ; les l. 54 et 55 (dimanche des commerces) et 71 à 73 (habitat) restent écrites sur le code 0, 1, 2 et n'ont pas à changer.
- l. 87 à 94 `du_projet` : conserver la répartition au prorata des SREF (P14) ; ajouter un contrôle facultatif « un objet parking par Typeusage » (p. 1323) qui compare les `Type_Usage` saisis aux usages des zones du projet.

**`openbce/eclairage.py` (nouvelle fonction, fiche 7.2)**
- Après `consommation_logement` (l. 36 à 38) : `parties_communes(usage, mobilite, sref_zone) -> np.ndarray` = `P_ECL_PARTIES_COMMUNES[usage] * mobilite * sref_zone` en Wh par heure (792), (793) ; annuel par (794). Constante `P_ECL_PARTIES_COMMUNES` de la section 6.
- l. 45 `LOCAUX_BUREAU` et l. 62 et 63 `C1_BUREAU` : remplacer par `C1_EIREF` indexé par usage et nom de local (section 10.2) ; conserver les codes 0 à 3 de l'usage 3 dans une table de correspondance `CODES_LOCAUX = {3: {0: "Bureau standard", 1: "Salle de réunion", 2: "Circulation Accueil", 3: "Sanitaires collectifs"}}`, les autres usages « non spécifiés » (P13). Ajouter `GRAND_VOLUME` (section 10.1) et les constantes « gv » du tableau 77 p. 479 (Roplafond 0,5, Romurs 0,5, Rosol 0,2, Rmursol 0,5, FFbpu 0,8 et FFplpu 0,9 pour les éclairants répartis uniformément, type 1 ; FFbpu_h 0,4 et FFplpu_h 0,8 « pour les autres éclairants : type baie = 0 et/ou 2 », p. 479, déjà portés pour le type 2 par `FF_BAIE, FF_PLAFOND` l. 14) à côté des « pv » des l. 13 à 18.
- l. 82 à 95 `locaux_tertiaires_saisis` et l. 121 à 130 `locaux_tertiaires` : prendre `usage` en argument et lire `C1_EIREF[usage]` ; l. 56 `TYPES_SANS_ACCES_NON_COMPTES` (déduction du banc des bureaux) : à n'appliquer qu'aux circulations et sanitaires, par nom de local, et à laisser « non validé » hors usage 3.

**`openbce/consommation.py`**
- l. 22 à 52 `puissance_ventilateurs` : rien à changer pour 4 à 28 ; le test `usage in (1, 2)` l. 42 suit la lecture P1 (`HABITATION`) si elle change.

**`openbce/ecs.py`** (thème ECS, pour mémoire)
- l. 23 `A_TERTIAIRE` : 26 valeurs du tableau 277 (section 11, P11 pour l'usage 16) ; l. 26 `RAT_DOUCHES_BAINS` : non lu dans ce thème (tableau 275).

**`openbce/bilans.py`**
- l. 50 `mobilier` : déjà conforme à (93) à (95) ; appeler avec `sc.apports_usages` des 28 usages.

**`openbce/sortie_rsee.py`**
- l. 26 `POSTES` : déjà les huit postes.
- l. 70 à 96 `_bloc_b` (l. 75 à 77) : O_SHAB = 0 et O_SU = SREF pour les usages 3 à 28 (P8) ; `Usage` écrit pour toute zone (l. 78 et 79, déjà).
- l. 107 à 137 `_bloc_c_groupe` : rester sans déplacement ni mobilier (p. 1371).
- l. 193 à 208 Sortie_Zone_C : ajouter `O_Cef_imp_deplacement_annuel` (ascenseurs + escalators, (2513)), `O_Cef_imp_mobilier_annuel`, `O_Cep_annuel` (2457), `O_Cep_nr_annuel` (2458), `O_Cep_annuel_occ` (P3), les `O_Cef_cons_[poste]_elec_annuel` (2443) et les mensuels (2430) à (2432) ; ajouter parkings et parties communes aux postes ecl et auxvent de la zone selon (2510) et (2511), avec l'option de les ranger dans déplacement comme le banc l'a vu (P9).
- l. 177 à 192 Sortie_Batiment_C : ajouter `O_Cep_annuel_occ` (2553) à partir de Σ `Nocc` des zones (2552), `O_Cef_imp_mobilier_annuel`, `O_Cep_nr_annuel`.
- Dictionnaire d'entrée (docstring l. 12 à 19) : ajouter par zone `nocc`, `deplacement` (kWh/m²), `mobilier`, `parties_communes`, `parkings_ecl`, `parkings_vent`.

**`banc/sortie_rsee.py`**
- l. 50 et 51 : remplacer `if usage not in (1, 2, 3): continue` par la boucle sur 1 à 28 ; l. 54 à 57 : `cle_s = "SHAB" if usage in (1, 2) else "SU"` et `scenarios.tertiaire` pour 3 à 28, déjà écrits ainsi.
- l. 81 (`exigences.dh_max`) et l. 83 et 84 (`exigences.bbio_max`) : `exigences.USAGES` (l. 15) ne connaît que 1 à 5 ; protéger l'appel (`None` au-delà) en attendant le thème exigences.
- l. 87 et 88 : `imp` et `imp["deplacement"]` ; ce dernier vient de `total["postes"]["dep"]`, lu dans le RSEE par `banc/cep_total.py` l. 91 à 93 ; le remplacer par `ascenseurs.du_batiment` + `parkings.du_projet` (déjà assemblés dans `banc/deplacement.py` l. 22 et 27), puis ajouter `mobilier` et `parties_communes`.
- l. 33 à 36 `sref_usage` : déjà sur `SU` hors 1 et 2.

**`banc/deplacement.py`**
- l. 24 et 25 : garder l'avertissement escalators ; l. 27 : passer `cal` à `occupants_conventionnels` ; ajouter une colonne « parties communes » pour l'usage 2 (P9).

**`banc/cep_total.py`**
- l. 91 à 93 : même remplacement que ci-dessus ; `ref["dep"]` reste lu dans le RSEE.

**`docs/lectures.md`**
- Ajouter P1, P2, P5, P7, P9, P11 et P13 au registre, catégorie « muet » ou « contre la lettre » selon le résultat du banc.
