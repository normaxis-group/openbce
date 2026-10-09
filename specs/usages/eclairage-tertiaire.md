# Spécification : éclairage des usages non résidentiels (fiche 7.1 C_ECL_éclairage)

Date : 09/10/2026. Décision de Cédric PLANTAZ (ARKEMEP) : « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Le NAS ne contient aucun RSEE RE2020 d'usage 4 à 28 ; tout ce qui suit pour ces usages est codé sur la foi du texte, sans banc. Seul l'usage 3 (bureaux) a un banc (docs/lectures.md, ligne 24 ; docs/validation.md, lignes 96 à 101).

## Sources lues

- Annexe III en vigueur, `corpus/texte_annexe3_2026-07/annexe3.txt` (1 854 pages) : fiche 7.1 C_ECL_éclairage, p. 470 à 501 (introduction p. 470 à 474, nomenclature tableau 77 p. 475 à 480, description mathématique p. 481 à 501 : équations 781 à 790, tableaux 76, 78 et 79, figures 82 à 86) ; chapitre 2.1.1 p. 18 (systèmes d'éclairage conventionnels) ; synthèse des scénarios p. 23 à 26 (locaux conventionnels, horaires d'éclairage par zone) ; tableau 4 p. 57 (liste des 28 usages) ; figure 23 p. 169 (entrées du composant éclairage en Bbio) ; fiche 5.10 p. 229 et 230 (type de baie selon le volume du local) ; chapitre 15 p. 1409 (renvoi au tableur des scénarios).
- Version 2022 découpée, `corpus/texte_annexe3/007_1_C_ECL_clairage.txt` : le tableau des C1 et des éclairements y est une image (ligne 1892, vide) ; la version 2026 le donne en texte, c'est elle qui fait foi ici. La numérotation des tableaux a glissé d'une unité : le tableau 79 de 2022 (C1 et Eiref) est le tableau 78 de 2026, le tableau 80 de 2022 (points de C2) est le tableau 79 de 2026. Les commentaires actuels de `eclairage.py` (« tableau 79 », « tableau 80 ») suivent la numérotation 2022.
- Tableur officiel des scénarios (29/04/2026) converti : `openbce/tables/scenarios_officiels.json` (noms des locaux, parts de surface, tableaux « éclairage » des 28 usages).
- Fiches d'application `corpus/site_2026-10-09/re2020-fa05_usage-batiment_v2.txt` (p. 4 : numéros d'usage ; p. 9 à 11 : rattachement des destinations) et `re2020-fa09_exclusion-application-tertiaire-specifique-industrie_v1.txt` (p. 5 : équipements de process exclus des puissances et consommations).
- Moteur : `openbce/eclairage.py` (en entier), `openbce/groupe.py` l. 105 à 125 et 195 à 225, `openbce/scenarios.py` (en entier), `openbce/baies.py` l. 106 à 114, `tests/test_eclairage.py`, `banc/essai_bureaux.py`, `docs/lectures.md` l. 24.

## 1. Ce que le texte fixe pour tout usage non résidentiel

### 1.1 Mode Th-B (Bbio) : système conventionnel, équation 782 (p. 481)

Si Type_bat n'est ni maison individuelle ni logement collectif :

- Pecl_tot,l = 2 x Eiref / 100 W/m² (782), Eiref lu au tableau 78 pour le type de local ;
- Pecl_aux,l = 0 W/m² ;
- Gest_ecl = 2 (interrupteur manuel et programmation horaire) : C1 est la deuxième colonne du tableau 78 ;
- Grad_ecl = 1 (gestion manuelle de la lumière du jour) : C2 suit les points A (0 ; 1), B (100 ; 1), G (700 ; 0,3), J (2 800 ; 0), C2 = 0 au-delà de 2 800 lux (tableau 79, p. 496) ;
- fr_Grad_Ecl = 1 : gestion non fractionnée, C2ae = C2pae calculés sur l'éclairement réduit du local (p. 494 et 495).

Les paramètres d'intégration restent des entrées, même en Th-B (tableau 77, p. 476, et figure 23, p. 169, qui liste type_local, Alocal, Agr, Ratio_ecl_nat, Fr_grad_ecl, seuil_auto_lumi parmi les entrées du composant éclairage du Bbio) : type_local,l, Ratio_local,l (part de la surface du local dans celle du groupe, 0 à 1), Ratio_ecl_nat,l (part du local ayant accès à la lumière naturelle, 0 à 1, égale à 1 pour les locaux éclairés par des baies de type 1), Seuil_auto_lumi (conventionnel 300 lux). Le texte ne donne aucune valeur conventionnelle de Ratio_ecl_nat par usage ni par local : c'est une saisie, déterminée par la règle d'accès effectif, réduit ou impossible (p. 491 et 492, voir 1.6).

Pour les maisons individuelles et les logements collectifs : Pecl_tot = 1 W/m², Pecl_aux = 0, Gest_ecl = 1, Grad_ecl = 1, fr_Grad_Ecl = 0 (781, p. 481) ; C1 = 0,9, Ratio_ecl_nat = 1, points de C2 A (0 ; 1), B (100 ; 1), G (200 ; 0,05), J (2 800 ; 0) (p. 500 et 501, équations 789 et 790). Déjà codé (`eclairage.py` l. 20 à 38).

### 1.2 Mode Th-C (Cep) : caractéristiques saisies (p. 481 et 482)

« Les caractéristiques des systèmes d'éclairage des autres locaux sont des données d'entrée » (p. 482) : Pecl_tot,l, Pecl_aux,l, Gest_ecl,l (0 à 4), Grad_ecl,l (0 à 4), Fr_Grad_ecl,l (1 ou 2) sont lus par local (tableau 77, p. 476 et 477). Deux corrections, à mener une seule fois en début de simulation (p. 481) :

- Type_bat = commerces, Type_local = petit magasin de vente ou aire de vente : Pecl_tot,l = max {4,5 ; Pecl_tot,l} (p. 481). Valeurs conventionnelles associées, p. 474 : efficacité lumineuse conventionnelle 80 lm/W, puissance conventionnelle 20 W/m² « au-dessous de laquelle un éclairage mobilier est nécessaire » pour les aires de vente, puissance de l'éclairage mobilier 50 W/m² pour les petits magasins ; Eff_immo_projet par famille de lampes (halogène 20, fluocompacte 70, fluorescente 80, halogénures métalliques 90, sodium haute pression 110 lm/W, tableau 77, p. 476). Aucune équation de 7.1.3 n'emploie ces valeurs de la p. 474 ni Eff_immo_projet : seul le plancher de 4,5 W/m² est écrit.
- Type_bat = bureaux, Type_local = bureaux : Pecl_immo_projet = Pecl_tot,l ; si Pecl_immo_projet < 10 W/m² : Ecl_immo_projet = 100 x Pecl_immo_projet / Eff_ecl_immo_projet ; si Ecl_immo_projet < Eiproj : Pecl_mob = (Eiproj - Ecl_immo_projet) / 100 x Eff_ecl_mob, avec Eff_ecl_mob = 1 W/m²/100 lux (p. 477 et 481) ; sinon Pecl_mob = 0 ; Pecl_tot,l = Pecl_immo_projet + Pecl_mob (p. 482). Eff_ecl_immo_projet (W/m²/100 lux) et Eiproj (lux) sont des paramètres intrinsèques (p. 477). Non codé aujourd'hui (`locaux_tertiaires_saisis` prend Pecl_tot tel quel) ; les champs du RSEE qui les portent n'ont pas été vus.

Pecl_aux est nul dès que (Gest_ecl = 0, 1 ou 2) et (Grad_ecl = 0 ou 1) (p. 486) : à forcer, quelle que soit la saisie.

La différence Th-B / Th-C tient donc aux seuls paramètres intrinsèques (Pecl_tot, Pecl_aux, Gest_ecl, Grad_ecl, Fr_Grad_ecl) : la liste des locaux, leurs parts de surface et leur accès à la lumière naturelle sont les mêmes entrées dans les deux modes.

### 1.3 Consommation horaire (786 à 788, p. 486 et 487)

CECL_GR = Σ CECL_local,l (786). CECL_local,l = max (Pecl_tot,l x CTRL_ecl_occ,l x CTRL_ecl_einat,l ; Pecl_aux,l) x Alocal,l / 1000 (787, Wh, Alocal,l = Agr x Ratio_local,l). CTRL_ecl_occ = 0 si IEcl = 0, C1 si IEcl = 1 (788, p. 487). IEcl est l'indice de fonctionnement de l'éclairage de la zone, 0 ou 1, « correspond aux plages d'occupation données par les scénarios conventionnels » (tableau 77, p. 475). Si Gest_ecl = 0 : C1 = 1 (p. 487) ; sinon C1 est lu au tableau 78 selon l'usage, le local et Gest_ecl. Apports récupérables : FeclC = 0,5 x CECL_GR, FeclR = 0,5 x CECL_GR, FeclNE = 0 (p. 501 ; constantes p. 479).

### 1.4 Coefficient C2 et gestion selon la lumière du jour (tableau 79, p. 496 et 497)

CTRL_ecl_einat = Ratio_ecl_nat,l x C2ae,l + (1 - Ratio_ecl_nat,l) x C2pae,l (p. 491). Points de référence, interpolation linéaire (p. 496) :

- Grad_ecl = 0 : C2 = 1 ;
- Grad_ecl = 1 : A (0 ; 1), B (100 ; 1), G (700 ; 0,3), J (2 800 ; 0), 0 au-delà ;
- Grad_ecl = 2 : A (0 ; 1), B (100 ; 1), E (Eiref ; 0,15), H (2 x Eiref ; 0,15), I (2 x Eiref ; 0), 0 au-delà ; Eimax_grad = 2 x Eiref, Part_resid_grad = 0,15 (p. 478, 493, 496) ;
- Grad_ecl = 3 : A (0 ; 1), C (Eiref ; 1), F (Eiref ; 0), 0 au-delà ;
- Grad_ecl = 4, Eiref < 700 : A (0 ; 1), B (100 ; 1), D (Eiref ; (1/6) x (6,7 - 7 x Eiref / 1 000)), F (Eiref ; 0) ; Eiref ≥ 700 : A, B, G (700 ; 0,3), D (Eiref ; 0,4 - Eiref / 7 000), F (Eiref ; 0) (p. 497).

Eimin = 100 lux : éclairement naturel minimum en deçà duquel l'éclairage artificiel est indispensable (p. 479 et 497). Déjà codé (`c2_points`, l. 67 à 79) : rien à changer.

### 1.5 Éclairement naturel réduit, fractionnement, locaux aveugles (p. 494 et 495)

Pour un local de volume normal (baies de type 2), avec Einat(2) l'éclairement des parties du groupe ayant accès à la lumière naturelle (784) :

- Fr_Grad_ecl = 1 (non fractionné, cas du Th-B) : C2ae = C2pae calculés avec Einat = Einat(2) x (2,5 x Ratio_ecl_nat - 1,5) si 1 ≥ Ratio > 0,7 ; Einat(2) x (0,5 x Ratio - 0,1) si 0,7 ≥ Ratio > 0,2 ; 0 si 0,2 ≥ Ratio ;
- Fr_Grad_ecl = 2 (fractionné) : C2pae sur l'éclairement réduit ci-dessus, C2ae sur Einat(2) ;
- **Ratio_ecl_nat,l = 0 (tout le local n'a pas accès à la lumière naturelle) : C2ae = C2pae = 1** (p. 495). Le local aveugle consomme donc Pecl_tot x C1 pendant toute l'occupation. Mêmes règles pour les grands volumes non uniformément éclairés (baies de type 0) avec Einat(0) (p. 494 et 495). Pour les grands volumes uniformément éclairés par la toiture (type 1, avec ou sans baies verticales) : pas de fractionnement (Fr_Grad_ecl = 1), C2ae = C2pae avec Einat = Einat(0) + Einat(1) (p. 494).

L'exception du moteur `TYPES_SANS_ACCES_NON_COMPTES = (2, 3)` (circulations et sanitaires aveugles non comptés, `eclairage.py` l. 48 à 56 et 94 à 96) est contraire à cette lettre ; elle est une déduction du banc des bureaux (docs/lectures.md l. 24 ; docs/validation.md l. 101). Rien dans le texte ne permet de l'étendre aux usages 4 à 28 ni de la limiter : voir points ouverts.

### 1.6 Accès à la lumière naturelle, Ratio_ecl_nat (p. 491 et 492)

Accès effectif : groupes à baies non horizontales de profondeur ≤ 2,5 x (hLi - hTa) (hauteur de linteau moins hauteur du plan de travail) ; pour les groupes plus profonds, les parties à moins de 2,5 x (hLi - hTa) d'une baie non horizontale si leurs luminaires sont commandés indépendamment ; les parties munies de parties vitrées uniformément réparties en toiture ; les locaux à éclairants uniformément répartis en toiture (type 1) ; les parties de locaux à moins de 2,5 fois l'écart de hauteur de la verticale d'un éclairant de toiture non uniformément réparti. Accès réduit : les parties au-delà de cette distance, ou en deçà mais commandées par un dispositif commun à tout le local. Accès impossible : locaux sans baies. Le texte ne convertit pas cette typologie en valeur numérique autrement que par Ratio_ecl_nat saisi par local ; aucune valeur par usage.

Seuil de 300 lux : Seuil_auto_lumi (conventionnel 300 lux, p. 476) sert uniquement aux indicateurs d'autonomie (785, p. 485 : Nbh_occ_Einat_sup, Nbh_occ_Einat_inf, Nbh_occ_nuit, Taux_occ_einat_sup, Taux_eclnat, Taux_fond_local, Taux_pas_eclnat, Grp_sans_accès, Grp_accès_mixte, Grp_accès_total), jamais à la consommation. Il n'a rien à voir avec les 300 lux d'Eiref des salles de classe ou des aires de vente (tableau 78).

### 1.7 Grands volumes et éclairement naturel (p. 482 à 484, p. 229 et 230)

Locaux de grand volume, « donnés dans le tableau 78 » (p. 482) : salle de sport des établissements sportifs scolaires ou municipaux (25) et privés (28), aire de production des industries 3x8 (23) et 8 à 18 h (24), aire de vente supérieure à 300 m² des commerces (17). La fiche 5.10 (p. 229) dit « zone à usage de commerces et que le local a une aire de vente » sans la borne de 300 m² : divergence entre les deux fiches, voir points ouverts. L'aire de production des établissements de santé (20, 21) n'est pas citée : volume normal.

Surfaces (p. 482) : Aeclnat01 = Σ Agr x Ratio_local x Ratio_ecl_nat sur les locaux de grand volume éclairés par des baies de type 1 et/ou 0 (Ratio_ecl_nat = 1 pour le type 1) ; Aeclnat0 pour les grands volumes éclairés par des baies de type 0 seules ; Aeclnat2 pour les locaux de volume normal (type 2). Remarque p. 485 : Aeclnat01 et Aeclnat0 ne peuvent être non nuls ensemble dans un même groupe. Les expressions de la p. 483 écrivent Einatbaiedif(0) = Flt2(0) x FFbpu_h / Aeclnat01 (et non Aeclnat0) : incohérence de notation du texte.

Éclairement (783 et 784, p. 483) : grand volume Einat = Einat(1) + Einat(0) ; volume normal Einat = Einat(2). Si Aeclnat = 0 pour tout le groupe, Einat = 0 (note p. 483). Chaque terme vaut Einat(n) = [K1 x Flt1(n) + K2 x Flt2(n) + K3 x Flt3(n)] / Aeclnat avec, pour Romoyen = (Rosol + Rmursol x Romurs + Roplafond) / (2 + Rmursol) et I = Romoyen / (1 - Romoyen) / RgrA,AT (RgrA,AT = 4,5) : K1 = Rosol x I, K2 = FFbpu + I, K3 = Roplafond x FFplpu + Roplafond x I (p. 483 et 484). Constantes p. 479 :

| Type de baie | Roplafond | Romurs | Rosol | Rmursol | FFbpu | FFplpu | K1 | K2 | K3 |
|---|---|---|---|---|---|---|---|---|---|
| 2, volume normal (vn) | 0,7 | 0,5 | 0,2 | 2,5 | 0,4 (FFbpu_h) | 0,8 (FFplpu_h) | 0,04066 | 0,60331 | 0,70232 |
| 1, grand volume uniforme (gvu) | 0,5 | 0,5 | 0,2 | 0,5 | 0,8 | 0,9 | 0,02724 | 0,93620 | 0,51810 |
| 0, grand volume non uniforme (gv) | 0,5 | 0,5 | 0,2 | 0,5 | 0,4 (FFbpu_h) | 0,8 (FFplpu_h) | 0,02724 | 0,53620 | 0,46810 |

Les K sont calculés ici depuis les constantes de la p. 479 (Romoyen_pv = 0,47778, Romoyen_gv = 0,38) ; le texte n'en donne pas la valeur numérique. La ligne « type 2 » est déjà codée (`eclairage.py` l. 13 à 18) ; les deux autres manquent. Le type de baie se décide à la baie selon le local qu'elle éclaire (p. 229 et 230) : horizontale (βb = 0) sur un grand volume, uniformément répartie (distance entre éclairants inférieure à la hauteur du local, distance à la périphérie inférieure à la moitié de la hauteur) : type 1 ; autre baie d'un grand volume : type 0 ; baie d'un volume normal : type 2. C'est la numérotation de la p. 230 et de la p. 479 (Type_baie = 2 locaux divisés, 0 et 1 grands volumes) ; le tableau 76 (p. 471 et 472) et la p. 492 en emploient une autre, voir points ouverts 17 et 18. Le groupe ne peut mêler grands volumes uniformément éclairés et grands volumes non uniformément éclairés (p. 472).

### 1.8 Ce que l'éclairage saisi ne comprend pas (p. 473, Th-C)

Exclus de Pecl_tot : éclairage extérieur, éclairage de sécurité, éclairage de mise en valeur d'objets ou de marchandises (dont l'éclairage localisé des tables de restaurant), éclairage spécialisé de process (scène, sous conditions). Les équipements de process d'un local soumis sont exclus des puissances et consommations (FA09, p. 5). Ce sont des règles de saisie, pas de calcul.

### 1.9 Systèmes conventionnels en Th-C aussi (p. 473 et p. 18)

« Pour les chambres des usages d'enseignement secondaire (partie nuit), bâtiment à usage d'habitation - établissement sanitaire avec hébergement et hôtel partie nuit, le système d'éclairage est conventionnel pour le calcul des coefficients Bbio et C » (p. 473 ; même phrase p. 18). Usages concernés par leur nom : 8 et 9 (hôtels partie nuit), 19 (établissements sanitaires avec hébergement) ; « enseignement secondaire (partie nuit) » n'est pas un usage du tableau 4 (p. 57) ; la FA05 rattache les internats à l'usage 10 et les résidences étudiantes sans cuisine à l'usage 8 (p. 9). L'usage 20 (santé partie nuit) n'est pas nommé. Le texte ne dit pas quelle convention s'applique à ces chambres en Th-C (782 avec Gest_ecl = 2, ou 781 avec les points résidentiels) : point ouvert.

## 2. Tableau 78 : C1 et Eiref des 28 usages (p. 488 à 491)

Transcription littérale, sans correction. Clé = numéro d'usage ; sous-clé = nom du local **tel que le tableur l'écrit** (feuille de l'usage dans `scenarios_officiels.json`), parce que `scenarios.tertiaire` fournit déjà ces noms ; valeur = (C1 pour Gest_ecl = 1, 2, 3, 4, puis Eiref en lux). `None` = non spécifié par le texte. Les différences d'orthographe entre le tableur et le tableau 78 sont en commentaire ; les deux locaux dont le nom diffère vraiment (18 et 25) sont signalés.

```python
# Tableau 78 (annexe III 2026, p. 488 à 491) : C1 par mode de commande Gest_ecl = 1, 2, 3, 4 et éclairement
# intérieur de référence Eiref (lux, NF EN 12464-1). Th-B : C1 = colonne Gest_ecl = 2, Pecl_tot = 2 x Eiref / 100 (782).
# Lecture littérale du texte ; None = non spécifié. Usages 4 à 28 non validés (aucun RSEE de référence).
TABLEAU_78 = {
    1: None,   # habitation : convention 781 (p. 481, 500, 501), pas de local
    2: None,   # idem
    3: {"Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
        "Salle de réunion": (0.70, 0.65, 0.60, 0.50, 50),     # texte : « 50 » ; moteur actuel : 500 (relevé sur l'image de 2022, banc des bureaux) ; voir points ouverts
        "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
        "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200)},
    4: {"Salle de classe": (0.95, 0.90, 0.85, 0.75, 300),
        "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
        "Salle de réunion": (0.80, 0.75, 0.70, 0.60, 300),
        "Salle de repos": (0.60, 0.75, 0.70, 0.60, 300),       # texte : 0,60 en Gest_ecl = 1, hors motif des autres lignes ; transcrit tel quel
        "Circulation Accueil": (0.60, 0.55, 0.50, 0.40, 100),
        "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200)},
    5: {"Salle de classe": (0.95, 0.90, 0.85, 0.75, 300),      # texte : « Salle de classes »
        "Salle de réunion": (0.80, 0.75, 0.70, 0.60, 300),
        "Salle d'enseignement informatique": (0.95, 0.90, 0.85, 0.75, 300),
        "Salle de conférence Salle polyvalente": (0.80, 0.75, 0.70, 0.60, 300),   # texte : « Sallepolyvalente »
        "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
        "Centre de documentation": (0.80, 0.75, 0.70, 0.60, 500),
        "Salle des professeurs": (0.80, 0.75, 0.70, 0.60, 300),
        "Circulation Accueil": (0.60, 0.55, 0.50, 0.40, 100),
        "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200)},   # texte : « Sanitaire collectifs »
    6: {"Salle multi-fonctions": (0.80, 0.75, 0.70, 0.60, 300),
        "Centre de documentation": (0.80, 0.75, 0.70, 0.60, 500),
        "Local service": (0.06, 0.05, 0.04, 0.02, 200),
        "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
        "Salle de réunion": (0.80, 0.75, 0.70, 0.60, 300),
        "Circulation accueil": (0.80, 0.75, 0.70, 0.60, 100),  # texte : « CirculationAccueil »
        "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200)},
    7: {"Salle de classe": (0.95, 0.90, 0.85, 0.75, 300),
        "Salle de conférence Amphithéâtre": (0.80, 0.75, 0.70, 0.60, 300),   # texte : « Amphithéatre »
        "Salle d'enseignement informatique": (0.95, 0.90, 0.85, 0.75, 300),  # texte : « 0,9 » en Gest_ecl = 2
        "Centre de documentation": (0.80, 0.75, 0.70, 0.60, 500),
        "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
        "Salle de réunion": (0.80, 0.75, 0.70, 0.60, 300),
        "Circulation Accueil": (0.60, 0.55, 0.50, 0.40, 100),
        "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
        "Local service": None},                                 # 15 % de la surface au tableur, absent du tableau 78 : non spécifié
    8: {"Chambre sans cuisine avec salle de bain": (0.60, 0.55, 0.50, 0.40, 70),   # texte : « salle de bains »
        "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
        "Local service": (0.06, 0.05, 0.04, 0.02, 200),
        "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100)},
    9: {"Chambre sans cuisine avec salle de bain": (0.60, 0.55, 0.50, 0.40, 70),
        "Sanitaires collectifs": (1.00, 0.95, 0.90, 0.80, 150),   # texte : seule ligne de sanitaires à 1,00 et 150 lux
        "Local service": (0.06, 0.05, 0.04, 0.02, 200),
        "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100)},
    10: {"Bureau standard": (0.80, 0.75, 0.70, 0.60, 500),       # texte : 0,80 (0,90 partout ailleurs) ; transcrit tel quel
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Salle petits déjeuners": (1.00, 1.00, 1.00, 1.00, 200)},
    11: {"Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Bar": (1.00, 1.00, 1.00, 1.00, 200),
         "Salle petits déjeuners": (1.00, 1.00, 1.00, 1.00, 200),
         "salle de séminaires réunion": (0.80, 0.75, 0.70, 0.60, 500)},
    12: {"Salle de jeux": (0.95, 0.90, 0.85, 0.75, 300),
         "Salle de repos": (0.80, 0.75, 0.70, 0.60, 300),
         "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Salle de réunion": (0.80, 0.75, 0.70, 0.60, 500),
         "Circulation Accueil": (0.60, 0.55, 0.50, 0.40, 100),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200)},
    13: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    14: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    15: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    16: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    17: {"Aire de vente (inférieure à 300m²)": (1.00, 1.00, 1.00, 1.00, 300),
         "Aire de vente (supérieure à 300m²)": (1.00, 1.00, 1.00, 1.00, 300),
         "Circulation Accueil": (1.00, 1.00, 1.00, 1.00, 300),
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    18: {"Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),   # texte : « 0,80 0?75 0?7 0,60 100 », séparateurs décimaux corrompus
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200),  # texte : ligne « Sanitaires collectifs » ; le tableur nomme ce local « Sanitaires vestiaires »
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200)},
    19: {"Chambre sans cuisine avec salle de bain": (1.00, 1.00, 1.00, 1.00, 70),   # texte : « Chambres »
         "Circulation Accueil": (1.00, 1.00, 1.00, 1.00, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200),
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Salle commune": (0.80, 0.75, 0.70, 0.60, 500),
         "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500)},
    20: {"Chambre sans cuisine avec salle de bain": (1.00, 1.00, 1.00, 1.00, 70),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Circulation Accueil": (1.00, 1.00, 1.00, 1.00, 200),
         "Locaux soins et offices": (1.00, 1.00, 1.00, 1.00, 500),
         "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Salle d'attente et de consulation (urgences)": (1.00, 1.00, 1.00, 1.00, 500),   # orthographe du tableur ; texte : « consultation »
         "Aire de production": (1.00, 0.95, 0.90, 0.80, 500)},
    21: {"Aire de production": (1.00, 0.95, 0.90, 0.80, 500),
         "Sanitaires collectifs": (0.70, 0.65, 0.60, 0.50, 200),
         "Circulation Accueil": (1.00, 1.00, 1.00, 1.00, 200),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Salle d'attente et de consultation": (1.00, 1.00, 1.00, 1.00, 500),
         "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Salle de réunion": (0.70, 0.65, 0.60, 0.50, 500)},
    22: {"Espace voyageurs": (1.00, 1.00, 1.00, 1.00, 200),
         "Circulation Accueil": (1.00, 0.75, 0.70, 0.60, 150),   # texte : 1,00 en Gest_ecl = 1 puis 0,75 ; transcrit tel quel
         "Commerces": (1.00, 1.00, 1.00, 1.00, 300),
         "Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Inspection filtrage": (1.00, 1.00, 1.00, 1.00, 500),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200)},
    23: {"Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Aire de production": (1.00, 1.00, 1.00, 1.00, 300),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    24: {"Bureau standard": (0.90, 0.85, 0.80, 0.70, 500),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Aire de production": (1.00, 1.00, 1.00, 1.00, 300),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    25: {"Salle de sport": (0.90, 0.85, 0.80, 0.70, 300),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200),  # texte : ligne « Sanitaires collectifs » ; le tableur nomme ce local « Sanitaires vestiaires »
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    26: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    27: {"Salle restaurant": (1.00, 1.00, 1.00, 1.00, 200), "Cuisine": (1.00, 1.00, 1.00, 1.00, 200), "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
    28: {"Salle de sport": (0.90, 0.85, 0.80, 0.70, 300),
         "Circulation Accueil": (0.80, 0.75, 0.70, 0.60, 100),
         "Sanitaires vestiaires": (0.70, 0.65, 0.60, 0.50, 200),
         "Douches collectives": (0.70, 0.65, 0.60, 0.50, 200),
         "Local service": (0.06, 0.05, 0.04, 0.02, 200)},
}

# Locaux de grand volume (p. 482 ; liste reprise p. 229 sans la borne de 300 m²). Tous les autres locaux sont de volume normal.
GRANDS_VOLUMES = {
    17: ("Aire de vente (supérieure à 300m²)",),
    23: ("Aire de production",),
    24: ("Aire de production",),
    25: ("Salle de sport",),
    28: ("Salle de sport",),
}

# Th-B, puissance conventionnelle par local : 2 x Eiref / 100 (782, p. 481), soit 500 lux : 10 W/m² ; 300 : 6 ; 200 : 4 ;
# 150 : 3 ; 100 : 2 ; 70 : 1,4 ; 50 : 1. Valeur calculée, pas une donnée distincte du texte.
def pecl_conventionnelle(eiref: float) -> float:
    return 2.0 * eiref / 100.0

# Th-C, commerces (p. 481) : plancher de puissance des aires de vente.
PECL_MIN_AIRE_DE_VENTE = 4.5   # W/m², Type_bat = commerces, Type_local = aire de vente ou petit magasin de vente
EFF_ECL_MOB = 1.0              # W/m²/100 lux, bureaux (p. 477, 481)
```

Vérification de cohérence tableur / tableau 78 : pour 27 usages sur 28 (hors 7), chaque local du tableur a une ligne au tableau 78, et réciproquement ; la somme des parts de surface du tableur vaut 1 (0,999 pour l'usage 22). L'usage 7 a un neuvième local, « Local service » (ratio 0,15, p. 24 et tableur), sans ligne au tableau 78.

## 3. Correspondance entre les noms du tableur et les types de la fiche 7.1

Le tableau 78 est indexé par « N° type de zone (usage) » et « type de local » : les types de la fiche 7.1 **sont** les noms de locaux du tableur, usage par usage, aux variantes d'orthographe près listées en commentaire ci-dessus. Il n'existe pas de nomenclature de types de local indépendante des usages (type_local,l « voir tableau 78 », p. 476 ; type_bat « renseigné automatiquement d'après l'usage défini au niveau de la zone », p. 474). Un même nom prend des valeurs différentes selon l'usage : « Salle de réunion » vaut 300 lux en 4, 5, 6, 7 et 500 en 11 (séminaires), 12, 21 ; « Circulation Accueil » vaut C1 (Gest_ecl = 2) 0,75 en 3, 6, 8, 9, 10, 11, 18, 23, 24, 25, 28, 0,55 en 4, 5, 7, 12, 1,00 en 17, 19, 20, 21 et 0,75 en 22, avec 100, 150, 200 ou 300 lux. La clé de la table doit donc être (usage, nom du local), jamais le seul nom.

Codes du RSEE : le champ `Locaux_Bureau` des entrées « Eclairage » n'est documenté nulle part (ni dans le texte, ni dans docs/rsee.md : aucun XSD publié). Pour l'usage 3 le moteur a déduit 0 bureau, 1 réunion, 2 circulation, 3 sanitaires (`eclairage.py` l. 45) des noms de locaux des RSEE de bureaux. Cet ordre est à la fois celui de la feuille BUR du tableur et celui du tableau 78 (p. 488) : l'usage 3 ne départage donc rien. Vérification faite sur `scenarios_officiels.json` contre les p. 488 à 491 : les deux ordres coïncident pour 7 usages seulement (3, 13 à 16, 26, 27) et diffèrent pour les 19 autres (4 à 12, 17 à 25, 28). Usage 4 : tableur Bureau standard, Circulation Accueil, Salle de classe, Salle de réunion, Salle de repos, Sanitaires vestiaires ; tableau 78 Salle de classe, Bureau standard, Salle de réunion, Salle de repos, Circulation Accueil, Sanitaires vestiaires. Usage 25 : tableur Circulation Accueil, Salle de sport, Local service, Sanitaires vestiaires, Douches collectives ; tableau 78 Salle de sport, Circulation Accueil, Sanitaires collectifs, Douches collectives, Local service. Le texte ne tranche pas (le champ n'y figure pas) et aucun RSEE d'usage 4 à 28 ne peut trancher. Deux candidats : A, code = indice du local dans la feuille de l'usage au tableur (ordre de `scenarios._locaux(usage)`) ; B, code = indice de la ligne de l'usage au tableau 78 (p. 488 à 491). Choix codé, marqué non validé : A, parce que `scenarios._locaux` fournit déjà cette liste et que le tableur porte aussi les parts de surface ; B reste à portée par une table des noms dans l'ordre du tableau 78, et le code doit pouvoir basculer de l'un à l'autre. Voir point ouvert 15.

Noms de locaux qui reviennent dans plusieurs usages (pour mémoire, pas de table à part) : Bureau standard (3, 4, 5, 6, 7, 10, 11, 12, 19, 20, 21, 22, 23, 24), Circulation Accueil (tous sauf 13 à 16, 26, 27), Sanitaires collectifs (3, 5, 6, 7, 8, 9, 10, 11, 17, 19, 20, 21), Sanitaires vestiaires (4, 12, 18, 22, 23, 24, 25, 28), Douches collectives (17, 18, 20, 21, 23, 24, 25, 28), Local service (6, 7, 8, 9, 13 à 17, 19, 23 à 28), Salle de réunion (3, 4, 5, 6, 7, 12, 21), Salle de classe (4, 5, 7), Chambre sans cuisine avec salle de bain (8, 9, 19, 20), Salle restaurant et Cuisine (13 à 16, 26, 27), Aire de production (20, 21, 23, 24), Salle de sport (25, 28).

## 4. Part de surface avec accès à la lumière naturelle, par usage

Non spécifié pour les 28 usages : le texte ne donne aucune valeur conventionnelle de Ratio_ecl_nat ; c'est un paramètre d'intégration saisi par local (p. 476, règle p. 491 et 492), égal à 1 pour les locaux éclairés par des baies de type 1 (p. 476 et 482). Le tableau 78 ne contient pas cette colonne. La description de `LOCAUX_BUREAU` dans la consigne (« dict {type: (part avec accès lumière, lux)} ») ne correspond pas au code : le dict porte (C1 pour Gest_ecl = 2, Eiref), la part avec accès vient de `Ratio_ecl_nat` du RSEE (`eclairage.py` l. 87 et 125).

Les parts de surface des locaux (Ratio_local,l) sont elles aussi lues dans le RSEE (`Rat_local`, l. 94 et 129) ; le tableur et la synthèse p. 24 à 26 en donnent une valeur « par défaut ». Le texte ne dit pas si l'éclairage doit suivre les parts saisies ou les parts par défaut quand elles diffèrent ; le moteur suit les parts saisies (banc des bureaux).

## 5. Horaires d'éclairage et usages 5, 7, 20, 22

La consigne annonce que les usages 5, 7, 20 et 22 n'ont pas de tableau « éclairage » au tableur. Ce n'est pas ce que contient `scenarios_officiels.json` (converti le 09/10/2026) : les 28 usages ont un tableau « éclairage » hebdomadaire (ligne 102 de chaque feuille) et annuel, et `scenarios.tertiaire` le lit déjà (`produit("éclairage")`, `scenarios.py` l. 149). Le texte dit la même chose, colonne « Horaire éclairage zone » de la synthèse (p. 24 et 25) : 5 et 7 « Idem occupation » (le tableur donne un tableau identique à celui de l'occupation) ; 20 « Lun - Dim : 5h-21h (réduit sinon), 52s/an » ; 22 « Lun - Dim : 5h-0h, 52s/an ». Le chapitre 15 (p. 1409) renvoie entièrement au tableur du 29/04/2026, il n'y a pas d'autre texte.

Valeurs non binaires du tableau « éclairage » du tableur : usage 17, 0,5 à 6 h ; usage 20, 0,35 de 21 h à 5 h (le « réduit sinon » de la p. 25, sans valeur dans le texte) ; usages 23 et 24, 0,5 sur la dernière semaine de l'année (profil annuel). IEcl est défini à 0 ou 1 (p. 475) ; le texte ne dit pas comment lire 0,35 ou 0,5. Le moteur teste `autorise > 0` (`eclairage.py` l. 107 et 138) : 0,35 vaut 1. Point ouvert.

## 6. Points ouverts

Ce que le texte ne tranche pas, ou qui ne se tranchera qu'au banc des bureaux (seul banc disponible) :

1. Eiref de la salle de réunion des bureaux : le texte 2026 écrit 50 lux (p. 488) ; le moteur a 500 (relevé sur l'image du PDF de 2022, l. 45) et le banc des bureaux a été calé avec 500 (banc des bureaux, docs/lectures.md l. 24 ; docs/validation.md l. 101). Une salle de réunion à 50 lux ferait Pecl_tot = 1 W/m² au lieu de 10, soit environ 12 % de consommation en moins sur un groupe de bureaux au tableur. Seul le banc des bureaux tranche : garder 500 pour l'usage 3 tant qu'il reproduit la référence, et consigner la lettre du texte dans docs/lectures.md.
2. Locaux aveugles : la lettre (C2 = 1, p. 495) contre l'exception du banc des bureaux (circulations et sanitaires aveugles non comptés, l. 48 à 56). Pour les usages 4 à 28, choisir entre appliquer la lettre, ou étendre l'exception aux mêmes natures de locaux (circulations, sanitaires, et par analogie douches et locaux de service, qui n'ont pas d'occupant au tableur) : rien dans le texte ne le dit, aucun banc ne le mesure. Recommandation : lettre du texte pour 4 à 28, exception maintenue pour le seul usage 3, les deux écrits dans docs/lectures.md.
3. Lignes du tableau 78 hors motif, transcrites telles quelles : usage 4 salle de repos (0,60 ; 0,75 ; 0,70 ; 0,60), usage 10 bureau standard (0,80 au lieu de 0,90), usage 22 circulation accueil (1,00 ; 0,75 ; 0,70 ; 0,60 à 150 lux), usage 9 sanitaires collectifs (1,00 ; 0,95 ; 0,90 ; 0,80 à 150 lux). Seule la colonne Gest_ecl = 2 compte en Th-B ; les autres n'interviennent qu'en Th-C sur saisie.
4. Usage 7, « Local service » (15 % de la surface) : aucune ligne au tableau 78. Lever une NotImplementedError pour ce local tant qu'un texte ne le complète pas, ou laisser le choix de la lecture (toutes les autres lignes « Local service » du tableau 78 valent 0,06 ; 0,05 ; 0,04 ; 0,02 ; 200) explicitement marquée non spécifiée.
5. Usages 18 et 25 : le tableau 78 écrit « Sanitaires collectifs », le tableur « Sanitaires vestiaires ». Les valeurs (0,70 ; 0,65 ; 0,60 ; 0,50 ; 200) sont les mêmes pour les deux noms partout ailleurs ; la correspondance retenue ici est par position, à confirmer.
6. Usage 18, circulation accueil : « 0?75 0?7 » dans le texte (p. 489), lu 0,75 et 0,70.
7. IEcl non binaire (17 : 0,5 ; 20 : 0,35 ; 23 et 24 : 0,5 annuel) : lecture en seuil (> 0 vaut 1, comportement actuel), ou en facteur multiplicatif de la consommation horaire (P x C1 x C2 x 0,35), ou en facteur de C1. Le texte ne le dit pas (p. 475 définit IEcl à 0 ou 1).
8. Chambres conventionnelles en Th-C (p. 473, p. 18) pour les usages 8, 9, 19 : la convention à appliquer en Th-C n'est pas écrite (782 avec Gest_ecl = 2 et C1 du tableau 78, ou 781 avec C1 = 0,9 et les points résidentiels). L'usage 20 n'est pas nommé. La chambre est 72,8 % de la surface des usages 8 et 9, 50 % de 19.
9. Grand volume des commerces : « aire de vente supérieure à 300 m² » (7.1, p. 482) contre « le local a une aire de vente » (5.10, p. 229). Retenir la fiche 7.1, qui porte le calcul, et le noter. Les baies horizontales d'un volume normal sont « automatiquement non réparties uniformément » (p. 230).
10. Typage des baies par local (0, 1, 2 ; p. 229 et 230) : le champ du RSEE qui rattache une baie à un local, ou qui porte Type_volume et la répartition uniforme, n'a pas été vu. Sans lui, les flux ne peuvent pas être séparés par type et les usages 17, 23, 24, 25, 28 ne peuvent être calculés qu'en volume normal (type 2), ce qui est faux pour la salle de sport (65 % de la surface) et l'aire de production (60 %).
11. Th-C bureaux : Eff_ecl_immo_projet et Eiproj (p. 477, équations p. 481 et 482) : champs du RSEE non vus ; le mode bureaux ne les applique pas aujourd'hui (banc des bureaux, docs/lectures.md l. 24 ; docs/validation.md l. 101). À mesurer au banc des bureaux en Th-C avant de les coder.
12. Th-C commerces : « petit magasin de vente » n'est pas un local du tableur (usage 17 n'a que deux aires de vente) ; la règle max{4,5 ; Pecl_tot} vise aussi « aire de vente », donc les deux locaux. Les valeurs 80 lm/W, 20 W/m², 50 W/m² (p. 474) n'ont pas d'équation.
13. Aeclnat01 contre Aeclnat0 (p. 482 et 483) : les expressions de Einat(0) divisent par Aeclnat01 ; retenir Aeclnat0 pour les groupes à baies de type 0 seules, puisque les deux ne coexistent jamais (p. 485).
14. Parts de surface des locaux : saisies (`Rat_local`) ou par défaut (tableur) ; le moteur suit les saisies pour l'éclairage et le tableur pour les occupants et apports (`scenarios._locaux`). Cohérence à vérifier au banc des bureaux.
15. Correspondance code `Locaux_Bureau` / local pour les usages 4 à 28 (section 3) : deux candidats, A ordre de la feuille du tableur, B ordre du tableau 78 (p. 488 à 491), identiques pour 3, 13 à 16, 26 et 27 seulement, différents pour les 19 autres. Le texte ne dit rien du champ, aucun RSEE ne peut trancher. Codé : A, non validé ; une table `ORDRE_TABLEAU_78` (noms dans l'ordre des p. 488 à 491) permet de basculer sur B sans toucher au calcul.
16. La prose de la p. 488 (« Les valeurs de C1 pour les autres types de commande sont données dans le tableau 79 ») garde la numérotation de 2022 : le tableau des C1 et des Eiref est légendé « Tableau 78 » (p. 491) et le tableau 79 de 2026 est celui des points de C2 (p. 496). La spécification suit les légendes.
17. Le tableau 76 (p. 471 et 472) numérote les types de baie à l'envers de la fiche 5.10 : « volumes normaux : type 1 », « grands volumes non uniformément éclairés : type 2 », « uniformément éclairés : type 0 », là où la p. 230 donne GV = type 0, GVU = type 1, VN = type 2 et où la p. 479 rattache Type_baie = 2 aux locaux divisés, 0 et 1 aux grands volumes. La spécification suit les p. 230 et 479, qui portent le calcul des flux (indice b(n)) et les constantes (section 1.7).
18. La p. 492 appelle « baie type 2 » les éclairants de toiture non uniformément répartis (accès effectif et accès réduit), qui sont le type 0 de la p. 230 ; la p. 491 appelle bien « type baie 1 » les éclairants uniformément répartis. La spécification suit la p. 230 (section 1.6).

## 7. Où coder

Constantes et fonctions à étendre, avec fichier et ligne (état du 09/10/2026) :

- `openbce/eclairage.py` l. 13 à 18 (`RO_PLAFOND … K1, K2, K3`) : ajouter les constantes des grands volumes (p. 479 : Roplafond_gv 0,5, Romurs_gv 0,5, Rosol_gv 0,2, Rmursol_gv 0,5 ; FFbpu 0,8 et FFplpu 0,9 pour le type 1 ; FFbpu_h 0,4 et FFplpu_h 0,8 pour le type 0) et les triplets `K_GVU = (0.02724, 0.93620, 0.51810)`, `K_GV = (0.02724, 0.53620, 0.46810)` (section 1.7) ; renommer le triplet actuel `K_VN`.
- `openbce/eclairage.py` l. 45 (`LOCAUX_BUREAU`) : remplacer par `TABLEAU_78` (section 2) indexé par usage puis nom de local, plus `GRANDS_VOLUMES`, `pecl_conventionnelle`, `PECL_MIN_AIRE_DE_VENTE`, `EFF_ECL_MOB`. Garder la valeur 500 de la salle de réunion de l'usage 3 tant que le banc des bureaux la soutient (point ouvert 1), avec la lettre du texte en commentaire.
- `openbce/eclairage.py` l. 46 (`_C2_MANUEL`) et l. 67 à 79 (`c2_points`) : inchangés ; corriger les commentaires « tableau 80 » en « tableau 79 (2026) ».
- `openbce/eclairage.py` l. 48 à 56 (`TYPES_SANS_ACCES_NON_COMPTES`) : passer d'un tuple de codes à un dict par usage, `{3: ("Circulation Accueil", "Sanitaires collectifs")}`, vide pour 4 à 28 (point ouvert 2) ; mettre à jour docs/lectures.md l. 24.
- `openbce/eclairage.py` l. 62 et 63 (`C1_BUREAU`) : supprimer, les quatre colonnes sont dans `TABLEAU_78`.
- `openbce/eclairage.py` l. 82 à 96 (`locaux_tertiaires_saisis(groupe)`) : ajouter le paramètre `usage` ; résoudre le local par `(usage, nom)` avec le candidat A (code = indice de la feuille du tableur, section 3 et point ouvert 15, non validé) via `scenarios._locaux(usage)`, et une table `ORDRE_TABLEAU_78` des noms dans l'ordre des p. 488 à 491 pour basculer sur le candidat B ; `None` dans la table lève `NotImplementedError("local non spécifié par le tableau 78")` ; C1 = `TABLEAU_78[usage][nom][gest - 1]` pour Gest_ecl 1 à 4, 1,0 pour Gest_ecl = 0 (p. 487) ; Pecl_aux forcé à 0 si Gest_ecl ≤ 2 et Grad_ecl ≤ 1 (p. 486) ; plancher 4,5 W/m² sur les deux aires de vente de l'usage 17 (p. 481) ; marquer le local grand volume (`GRANDS_VOLUMES`) et son type de baie (0 ou 1) dans le tuple retourné ; complément mobilier des bureaux (p. 481 et 482) seulement après le point ouvert 11.
- `openbce/eclairage.py` l. 98 à 118 (`consommation_tertiaire_saisie`) : recevoir les flux par type de baie, `(flt1, flt2, flt3)` x 3, au lieu d'un seul triplet ; calculer Aeclnat2 (type 2), Aeclnat01 (types 0 et 1) séparément (p. 482) ; Einat(2) avec `K_VN`, Einat(1) avec `K_GVU`, Einat(0) avec `K_GV` (p. 483 et 484) ; pour un local grand volume uniformément éclairé : C2ae = C2pae sur Einat(0) + Einat(1), sans fractionnement (p. 494) ; pour un grand volume non uniforme : règles de Ratio sur Einat(0) (p. 494 et 495) ; retourner Einat par type pour les indicateurs d'autonomie (785, seuil 300 lux, p. 485), si les sorties RSEE les demandent.
- `openbce/eclairage.py` l. 121 à 131 (`locaux_tertiaires(groupe)`) : même signature `(groupe, usage)` et même résolution ; C1 = colonne Gest_ecl = 2 (782), Eiref de `TABLEAU_78` ; Pecl = `pecl_conventionnelle(eiref)`.
- `openbce/eclairage.py` l. 133 à 149 (`consommation_tertiaire`) : même découpage par type de baie que la version saisie ; la formule 2 x Eiref / 100 x C1 x C2 x surface x rat reste (782, 787).
- `openbce/groupe.py` l. 114 (`locaux_ecl = …`) : passer `usage` aux deux fonctions ; l. 209 à 211 (sommes `flt1 += …`, `flt2 += …`, `flt3 += …`) : sommer par type de baie (0, 1, 2) d'après le local que la baie éclaire (p. 229 et 230), champ RSEE à identifier (point ouvert 10) ; l. 217 et 219 : passer les trois triplets.
- `openbce/baies.py` l. 106 à 114 (`flux_lumineux`) : inchangé par baie ; le type de baie est une propriété à lire sur la baie (`Baie`, l. 36 à 73) ou à déduire de β et du volume du local (p. 230).
- `openbce/scenarios.py` l. 126 à 150 (`tertiaire`, `eclairage=produit("éclairage")`) : décider la lecture des valeurs 0,35 et 0,5 (point ouvert 7) ; aujourd'hui transmise telle quelle et seuillée dans `eclairage.py` l. 107 et 138. `_locaux` (l. 101 à 124) fournit déjà les noms du tableur dans l'ordre de la feuille : c'est la source du candidat A (point ouvert 15), non validé.
- `tests/test_eclairage.py` l. 24 à 43 : adapter le faux groupe (codes → usage + noms), ajouter un test par usage sur `TABLEAU_78` (nombre de locaux = nombre de locaux de `scenarios._locaux(usage)`, sauf 7), un test du plancher 4,5 W/m² (17), un test grand volume (25 : Einat = Einat(0) + Einat(1) et absence de fractionnement).
- `docs/lectures.md` l. 24 et `docs/validation.md` l. 96 à 101 : inscrire « usages 4 à 28 codés sur le texte, non validés », la lettre du 50 lux (point ouvert 1), l'exception limitée à l'usage 3 (point ouvert 2).
