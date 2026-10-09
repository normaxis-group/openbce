# Spécification : besoins d'eau chaude sanitaire des usages non résidentiels (usages 3 à 28)

Date : 09/10/2026. Décision de Cédric PLANTAZ (ARKEMEP) : « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Le NAS ne contient aucun RSEE RE2020 d'usage 4 à 28 ; ces usages sont codés sur la foi du texte. Le seul usage non résidentiel observé dans un récapitulatif est l'usage 3 (bureaux, voir `specs/ecs.md` l. 16 ; aucune valeur de projet n'est reprise ici).

## Sources lues

Texte de référence : annexe III en vigueur, `corpus/texte_annexe3_2026-07/annexe3.txt` (1 854 pages).

- Chapitre 2.1.1, synthèse des scénarios, p. 18 à 27 : texte d'introduction des besoins d'ECS (p. 19) et tableau de synthèse par usage avec la colonne « Besoin unitaire hebdomadaire en ECS à 40 °C (L/m² de surface utile) » (p. 24 à 26 ; tableau en image, colonnes mélangées à l'extraction, valeurs lisibles).
- Fiche 4.1 C_EIN_Scénarios conventionnels : nomenclature `ihebergement` et `ienseignement` (p. 54), tableau 4 « liste des usages de la zone » avec les deux indicateurs par usage (p. 57), équation (46) clé de répartition ah, (47) iecs(j), (49) Iocc_zone (p. 62).
- Fiche 9.5 C_EMI_Emission_ECS, p. 1042 à 1048 : tableau 271 nomenclature (p. 1043 et 1044), tableau 272 paramètres d'intégration par usage (p. 1045), équations (1673) à (1679), tableau 273 gains émetteurs (p. 1046), tableau 274 ratio douches-bains (p. 1047), tableau 275 gains appareils (p. 1047).
- Fiche 9.6 C_EIN_besoins_ECS, p. 1049 à 1066 : tableau 276 nomenclature (p. 1050 à 1052), équations (1680) à (1694) (p. 1053 à 1057), tableau 277 besoins unitaires hebdomadaires pour les 28 usages (p. 1053 à 1055), récupérateurs sur eaux grises, section ouverte en bas de p. 1057 après (1694), équations (1695), p. 1059, à (1728), p. 1065 (hors champ ; la fiche 9.7 ouvre p. 1067).
- Fiche 9.24 FA_Bâtiments non équipés de production d'eau chaude sanitaire, p. 1294 (une page, sans équation numérotée ni tableau).
- Chapitre 15 Scénarios conventionnels, p. 1409 : une seule page, qui renvoie au tableur `2026-04-29_scenarios_conventionnels.xlsx` (note 14). Le texte en vigueur ne contient plus les matrices de clé ECS : le tableur fait foi pour ah.
- Tableur converti : `openbce/openbce/tables/scenarios_officiels.json` (source 2026-04-29_scenarios_conventionnels.xlsx), scalaire « nombre de litres d'eau à 40°C puisés par semaine et par unité » (unité L/semaine/unité, absent des feuilles MI et LC) et tableau « ECS facteur correctif de la semaine » (hebdo 7 × 24, annuel 5 × 12) pour les 28 feuilles.
- Version 2022 découpée, `corpus/texte_annexe3/009_6_C_EIN_besoins_ECS.txt` et `009_5_C_EMI_Emission_ECS.txt` : uniquement pour établir la correspondance des numéros (le tableau 278 de 2022 ne donnait que bureaux, enseignement primaire et secondaire partie jour ; il est devenu le tableau 277 à 28 lignes).
- Fiches d'application du site, `corpus/site_2026-10-09/` : FA05 « Comment identifier l'usage d'un bâtiment » v2 du 01/10/2026 (liste des 28 usages p. 4, N.B. vestiaires p. 4, conventions d'usage p. 5 « Besoin unitaire hebdomadaire en ECS à 40°C l/m² Sref », usages de groupe p. 9 à 11) ; FA09 « Exclusions tertiaires spécifiques et industrie » v1 du 01/10/2026 (locaux de process, p. 3 à 7 ; rien sur l'ECS).
- Moteur : `openbce/openbce/ecs.py` (82 lignes, lu en entier), `scenarios.py` l. 22 à 45, `calendrier.py` l. 49 à 61, `groupe.py` l. 108, `ballon.py` l. 35 à 53 et 97 à 105, `banc/ecs.py` (lu en entier), `specs/ecs.md` (entrées RSEE et points ouverts).

Correspondance des numéros entre les commentaires du moteur (numérotation 2022) et le texte en vigueur : tableau 274 (gains émetteurs) devient 273 ; 275 (ratio douches-bains) devient 274 ; 276 (gains appareils) devient 275 ; 277 (nomenclature 9.6) devient 276 ; 278 (besoins unitaires) devient 277. Équations : (1675) devient (1674) ; (1677) à (1679) deviennent (1676) à (1678) ; (1684) à (1692) deviennent (1683) à (1691) ; (1694) et (1695) deviennent (1693) et (1694).

## 1. Chaîne de calcul (fiche 9.6, p. 1053 à 1057)

Pour chaque émetteur ECS équivalent em-e d'un groupe gr :

- (1680), p. 1053 : Qw = ρw · cw · Vuw · (θuw - θcw), avec ρw = 1 kg/L, cw = 1,163 Wh/(kg.K), θuw = 40 °C (constantes du tableau 276, p. 1052) et θcw(h) la température d'eau froide du fichier météo.
- (1681), p. 1053 : Vuw = a · ah · Nu ; a besoins unitaires hebdomadaires de l'usage, ah coefficient horaire de la clé de répartition de l'usage, Nu nombre d'unités de l'émetteur.
- (1682), p. 1055 : A_gr,em-e = Rat_em^gr,em-e × A_gr (même formule que (1674), p. 1046, fiche 9.5 ; contrôle (1673), p. 1046 : la somme des Rat_em des émetteurs du groupe vaut 1, message d'erreur sinon, p. 1045).
- § 9.6.3.2.2.1, p. 1055 : « Si Usage_zone ≠ {1, 2}, le nombre d'unités caractéristiques Nu_gr,em-e est un paramètre d'intégration » (saisi, pas calculé). a est « figé dans les scénarios conventionnels (il sera donc le même pour tous les émetteurs d'une zone) », p. 1055.
- (1683) à (1690), p. 1055 et 1056 : usages 1 et 2 seulement (adultes équivalents, a = min(392 ; 40 × A/Nadeq)), déjà codés dans `ecs.adultes_equivalents` et `ecs.volume_hebdomadaire`.
- (1691), p. 1056 : Vuw_hebdo^gr,em-e = a_gr,em-e · Nu_gr,em-e, « quel que soit l'usage ».
- (1692), p. 1057 : Vuw_hebdo_corr^gr,em-e = Vuw_hebdo^gr,em-e × corr^gr,em-e, corr calculé par la fiche 9.5 (voir § 4). Aucune variante de (1692) dans le texte : la correction a la même forme pour tous les usages, seule la valeur de Rat_douches-bains change avec l'usage.
- § 9.6.3.4, p. 1057 : la clé ah répartit Vuw_hebdo_corr sur chaque pas de temps de la semaine ; « définie par zone », « calculée dans la fiche scénarios conventionnels », fonction du mois, du jour de la semaine et de l'heure ; « les matrices de répartition des besoins d'ECS sont détaillées dans les scénarios » (donc dans le tableur, p. 1409). Note 1, p. 1057 : la variation saisonnière traduit seulement le comportement des occupants.
- (1693), p. 1057 : Qw^gr,em-e = ρw · cw · (Vuw_hebdo_corr^gr,em-e · ah) · (θuw - θcw) ; Qw^gr = ρw · cw · (Σ_em-e Vuw_hebdo_corr) · ah · (θuw - θcw).
- (1694), p. 1057 : Qw_bruts^gr, même formule sans la correction, indicateur pédagogique seulement.
- (1695), p. 1059, à (1728), p. 1065 (section ouverte en bas de p. 1057, après (1694)) : récupérateurs de chaleur sur eaux grises, inchangés par l'usage, hors champ (le moteur lève NotImplementedError, `ecs.py` l. 79 et 80). Seule équation utile ici : (1700), p. 1060, Rat = (100 - Rat_douches-bains)/100, qui confirme que Rat_douches-bains est un pourcentage conventionnel propre à l'usage.

Entrées du tableau 276 (p. 1050) non utilisées par les équations : Usage_zone (ne sert qu'à choisir a, Rat et ah) et Iocc_zone (l'occupation est déjà portée par ah). Le texte ne donne aucune formule qui annule Qw hors occupation : ne pas multiplier par Iocc_zone.

## 2. Tableau 277 : a et Nu pour les 28 usages (p. 1053 à 1055)

Le tableau 277 donne, pour chaque usage de 3 à 28, a_gr,em-e en « L d'eau à θuw par unité » et Nu_gr,em-e en « m² de surface utile ». Les usages 1 et 2 renvoient aux équations (1683) à (1690). La colonne « Besoin unitaire hebdomadaire en ECS à 40 °C (L/m² de surface utile) » de la synthèse du chapitre 2 (p. 24 à 26) redonne les mêmes valeurs, et le tableur (scalaire « nombre de litres d'eau à 40°C puisés par semaine et par unité », L/semaine/unité) aussi, sauf pour l'usage 16.

| Usage | Libellé (tableau 277) | a (L/semaine/unité), page | Nu | Tableur 29/04/2026 |
|---|---|---|---|---|
| 1 | Maisons individuelles ou accolées | voir (1686), p. 1056 : min(392 ; 40 × A/Nadeq) | adultes équivalents (1685) | feuille MI, pas de scalaire |
| 2 | Logements collectifs | voir (1690), p. 1056 | adultes équivalents (1689) | feuille LC, pas de scalaire |
| 3 | Bureaux | 1,25, p. 1053 | m² de surface utile | 1,25 |
| 4 | Enseignement primaire | 0,2, p. 1053 | m² de surface utile | 0,2 |
| 5 | Enseignement secondaire | 0,2, p. 1053 | m² de surface utile | 0,2 |
| 6 | Médiathèques et bibliothèques | 0,2, p. 1053 | m² de surface utile | 0,2 |
| 7 | Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques | 0,2, p. 1054 | m² de surface utile | 0,2 |
| 8 | Hôtels 0, 1 et 2 étoiles (partie nuit) | 22,873, p. 1054 | m² de surface utile | 22,873 |
| 9 | Hôtels 3, 4 et 5 étoiles (partie nuit) | 18,98, p. 1054 | m² de surface utile | 18,98 |
| 10 | Hôtels 0, 1 et 2 étoiles (partie jour) | 5,694, p. 1054 | m² de surface utile | 5,694 |
| 11 | Hôtels 3, 4 et 5 étoiles (partie jour) | 4,76, p. 1054 | m² de surface utile | 4,76 |
| 12 | Établissements d'accueil de la petite enfance | 0,714, p. 1054 | m² de surface utile | 0,714 |
| 13 | Restaurants - en continu, 18 heures par jour, 7 jours sur 7 | 19,5, p. 1054 | m² de surface utile | 19,5 |
| 14 | Restaurants - 1 repas par jour, 5 jours sur 7 | 2,2, p. 1054 | m² de surface utile | 2,2 |
| 15 | Restaurants - 2 repas par jour, 7 jours sur 7 | 5,3, p. 1054 | m² de surface utile | 5,3 |
| 16 | Restaurants - 2 repas par jour, 6 jours sur 7 | 19,5, p. 1054 (et p. 25) | m² de surface utile | **4,7** (écart, point ouvert 1) |
| 17 | Commerces | 0,24, p. 1054 | m² de surface utile | 0,24 |
| 18 | Vestiaires seuls | 79, p. 1054 | m² de surface utile | 79 |
| 19 | Établissements sanitaires avec hébergement | 2,8, p. 1054 | m² de surface utile | 2,8 |
| 20 | Établissements de santé (partie nuit) | 1,68, p. 1054 | m² de surface utile | 1,68 |
| 21 | Établissements de santé (partie jour) | 25,2, p. 1054 | m² de surface utile | 25,2 |
| 22 | Aérogares | 0,24, p. 1054 | m² de surface utile | 0,24 |
| 23 | Industries ou artisanats 3x8h | 0,24, p. 1054 | m² de surface utile | 0,24 |
| 24 | Industries ou artisanats 8h à 18h | 0,24, p. 1054 | m² de surface utile | 0,24 |
| 25 | Établissements sportifs municipaux ou scolaires | 13,2, p. 1054 | m² de surface utile | 13,2 |
| 26 | Restaurants scolaires - 1 repas par jour, 5 jours sur 7 | 4,5, p. 1054 | m² de surface utile | 4,5 |
| 27 | Restaurants scolaires - 3 repas par jour, 5 jours sur 7 | 9,8, p. 1054 | m² de surface utile | 9,8 |
| 28 | Établissements sportifs privés | 33,9, p. 1054 | m² de surface utile | 33,9 |

Aucun usage n'a un a nul : le texte ne prévoit pas d'usage « à ECS nulle ». Les plus forts besoins par m² sont les vestiaires seuls (79), les établissements sportifs privés (33,9), les établissements de santé partie jour (25,2) et les hôtels partie nuit (22,873 et 18,98).

Dict prêt à copier (valeurs du texte en vigueur ; aucune case « non spécifié » car le tableau 277 est complet) :

```python
# Tableau 277, p. 1053 à 1055 : litres d'eau à 40 °C par semaine et par unité, usages 3 à 28.
# Usages 1 et 2 : a = min(392 ; 40 × A_gr,em-e / Nadeq) (1686, 1690), calculé, pas tabulé.
A_TERTIAIRE = {
    3: 1.25, 4: 0.2, 5: 0.2, 6: 0.2, 7: 0.2,
    8: 22.873, 9: 18.98, 10: 5.694, 11: 4.76,
    12: 0.714,
    13: 19.5, 14: 2.2, 15: 5.3, 16: 19.5,      # 16 : le tableur du 29/04/2026 dit 4,7 (point ouvert 1)
    17: 0.24, 18: 79.0, 19: 2.8, 20: 1.68, 21: 25.2,
    22: 0.24, 23: 0.24, 24: 0.24,
    25: 13.2, 26: 4.5, 27: 9.8, 28: 33.9,
}
# Même scalaire lu dans le tableur (scenarios_officiels.json, « nombre de litres d'eau à 40°C puisés par
# semaine et par unité ») : identique sauf l'usage 16.
A_TERTIAIRE_TABLEUR = {**A_TERTIAIRE, 16: 4.7}

# Tableau 277 : unité de Nu_gr,em-e. Le texte écrit « m² de surface utile » pour chacun des usages 3 à 28 ;
# aucun usage n'est compté en lits, repas, chambres, occupants ou douches.
UNITE_NU = {1: "adulte équivalent (1685)", 2: "adulte équivalent (1689)", **{u: "m² de surface utile" for u in range(3, 29)}}
```

### Ce que compte le champ `nu_gr_em_e` du récapitulatif

Le champ XML `Emetteur_ECS/nu_gr_em_e` porte Nu_gr,em-e, « nombre d'unités caractéristiques desservies par un émetteur ECS équivalent (pour les usages autres que maison individuelle ou accolée et logements collectifs) », paramètre d'intégration, réel de 0 à +∞ (tableau 276, p. 1050 ; tableau 271, p. 1043 ; tableau 272, p. 1045 : « Autres usages : Rat_em et Nu, le nombre d'unités concernées »). Comme le tableau 277 définit l'unité comme le m² de surface utile pour tous les usages 3 à 28, `nu_gr_em_e` compte des **m² de surface utile desservis par l'émetteur**, pour chacun des 26 usages non résidentiels, hôtels et établissements d'hébergement compris. La valeur observée en bureaux (un émetteur à Rat_em_e = 1, `specs/ecs.md` l. 16, chiffre non repris ici) est cohérente avec Nu = Rat_em^gr,em-e × A_gr (1682). Le texte ne dit pas que Nu doit être égal à A_gr,em-e ; il dit seulement que la somme des Rat_em vaut 1 (1673). Voir point ouvert 2.

La phrase de la p. 19 (« ces besoins sont calculés en fonction du nombre d'équipements, par exemple le nombre de chambres pour un hôtel ») est un reste d'une version antérieure : le tableau 277 en vigueur compte les hôtels en m² de surface utile, et c'est lui qui s'applique (point ouvert 3).

## 3. Tableau 274 : ratio douches-bains pour les 28 usages (p. 1047)

Tableau 274 « Valeurs conventionnelles de ratio de besoins dédiés aux douches et/ou aux bains », p. 1047 : « Maison individuelle et accolée, logement collectif : 80 % ; Bureaux : 50 % ; Autres usages : 0 % ». Paramètre intrinsèque Rat_douches-bains, borné 0 à 0,9 (tableau 271, p. 1043). Le texte tranche donc explicitement les usages 4 à 28 : 0 %.

```python
# Tableau 274, p. 1047.
RAT_DOUCHES_BAINS = {1: 0.8, 2: 0.8, 3: 0.5, **{u: 0.0 for u in range(4, 29)}}
```

Conséquence, (1677) p. 1047 : corr_app = 1 - Rat_douches-bains × gain_app = 1 pour les usages 4 à 28, quel que soit `app_ecs` (tableau 275, p. 1047 : douches seules 5 %, baignoire sabot 2,5 %, standard 0 %, grande baignoire -2,5 %). Le type d'appareil sanitaire n'a d'effet qu'en habitation et en bureaux. Le moteur continue de lire `app_ecs` (défaut 2) sans erreur pour ces usages.

## 4. Tableaux 273 et 275, équations (1676) à (1678) : correction, inchangée par l'usage (p. 1046 à 1048)

- Tableau 273, p. 1046, gain_em : mélangeurs, mitigeurs mécaniques et autres 0 % ; mitigeurs thermostatiques et mitigeurs mécaniques économes (position médiane sur l'eau froide, C3 ou CH3) 5 % ; temporisateurs et robinets électroniques 7 %. (1675), p. 1046 : M_part_em = [part_melangeur ; part_mitigeur ; part_temporisateur], somme 1. (1676), p. 1047 : corr_em = 1 - Σ part(i) × gain_em(i).
- Tableau 275, p. 1047, gain_app (ci-dessus) ; note p. 1047 : « s'il y a plusieurs appareils d'ECS de nature différente, l'appareil le plus défavorable sera retenu ». (1677), p. 1047 : corr_app = 1 - Rat_douches-bains × gain_app.
- (1678), p. 1048 : corr^gr,em-e = corr_app × corr_em. Déjà codé (`ecs.correction`, l. 53 à 58) ; seule la table RAT_DOUCHES_BAINS doit être étendue.
- (1679), p. 1048 : θec^gr,em-e = θ2nd-e^gr (48 °C, tableau 271, p. 1044), erreur si θec < θuw ; hors besoins, relève de la distribution (`specs/ecs.md`).

Aucune variante par usage dans la fiche 9.5 : les gains des tableaux 273 et 275 sont les mêmes pour les 28 usages.

## 5. Clé de répartition horaire ah par usage

### Définition dans le texte

- (46), p. 62 : ah(m, s, j, h) = p_ECS^a(m, s) × p_ECS^s(j, h), décidée au niveau de la zone (p_a : profil annuel par mois m et semaine s du mois ; p_s : profil hebdomadaire par jour j et heure h).
- (47), p. 62 : si ienseignement = 1 et ivac = 0, iecs(j) = 0, sinon iecs(j) = 1 : pendant les vacances des zones d'enseignement, « l'éventuel réseau primaire d'ECS est arrêté ». Cet indicateur agit sur la distribution intergroupe ((1737), `specs/ecs.md`), pas sur les besoins Qw.
- Tableau 4, p. 57 : ienseignement = 1 pour les usages 4, 5, 7, 26 et 27, 0 pour les autres ; ihebergement = 1 pour 1, 2, 8, 9, 19 et 20.
- Chapitre 15, p. 1409 : les matrices sont dans le tableur 2026-04-29 ; le texte ne contient plus de valeurs horaires.
- Fiche 9.6, § 9.6.1, p. 1049 : la clé est « propre à chaque usage », « définie au niveau de la zone, et est commune à tous les émetteurs ECS équivalents situés dans la zone » ; § 9.6.3.4, p. 1057 : « définie par zone », « cohérente avec le scénario d'occupation ». Le texte ne demande aucune normalisation de la somme hebdomadaire.

```python
# Tableau 4, p. 57 : indicateurs d'usage de la fiche 4.1.
IENSEIGNEMENT = {u: (1 if u in (4, 5, 7, 26, 27) else 0) for u in range(1, 29)}
IHEBERGEMENT = {u: (1 if u in (1, 2, 8, 9, 19, 20) else 0) for u in range(1, 29)}
```

### Tableau « ECS facteur correctif de la semaine » du tableur (les 28 feuilles)

Le moteur (`ecs.cle_horaire`, l. 61 à 71) lit déjà, pour tout usage, le premier tableau dont le nom commence par « ECS » dans la feuille de l'usage, et calcule hebdo[jour, case] × annuel[semaine, mois] (None lu comme 0). Les 28 feuilles ont ce tableau, nommé à l'identique, 7 × 24 et 5 × 12 ; aucune extension du code n'est nécessaire, seulement des tests. Motifs horaires lus dans `scenarios_officiels.json` (heure légale = numéro de case 1 à 24, valeur = part du volume hebdomadaire ; les jours non cités sont nuls) :

| Usage | Feuille | Profil hebdomadaire (jours : case = part) | Somme hebdo | Profil annuel (min à max, 5 semaines × 12 mois) |
|---|---|---|---|---|
| 1 | MI | lun à ven : 8 = 0,028, 9 = 0,029, 18 = 0,0072, 19 à 21 = 0,0215, 22 = 0,014 ; sam, dim : 8 = 0,028, 9 = 0,029, 18 et 19 = 0,0115, 20 = 0,0287, 21 = 0,022, 22 = 0,0115 | 0,99747 | 0,95 (avril à septembre) à 1,05 ; 0 la 4e semaine de décembre |
| 2 | LC | lun à ven : 8 = 0,028, 9 = 0,029, 18 = 0,0072, 19 à 21 = 0,0215, 22 et 23 = 0,0072 ; sam, dim : 8 = 0,028, 9 = 0,029, 18 et 19 = 0,0115, 20 = 0,0287, 21 à 23 = 0,0115 | 1,001 | 0,95 à 1,05 ; 0 la 4e semaine de décembre |
| 3 | BUR | lun à ven : 9 = 0,012, 10 à 12 = 0,0253, 13 et 14 = 0,012, 15 à 17 = 0,0253, 18 = 0,012 ; sam, dim nuls | 1,0 | 0,5 (juillet, août, 2e semaine d'avril, 4e de décembre) à 1,0 |
| 4 | ENS_PRI | lun, mar, jeu, ven : 9 = 0,0139, 10 à 16 = 0,0317, 17 = 0,0139 ; mer, sam, dim nuls | 1,0 | 0 (vacances scolaires), 0,5 (juillet, août), 1,0 |
| 5 | ENS_SEC | lun à ven : 17 et 18 = 0,0833 ; sam : 11 et 12 = 0,0833 ; dim nul | 1,0 | 0 (vacances), 0,5 (juillet, août), 1,0 |
| 6 | MED | lun à ven : 10 à 12 et 15 à 18 = 0,0208, 19 = 0,0417 ; sam : 10 à 12 = 0,0208 ; dim nul | 1,0 | 1,0 à 1,1 ; 0 la 4e semaine de décembre |
| 7 | ENS_SUP | lun à ven : 8 à 18 = 0,0138, 19 = 0,0305 ; sam : 8 à 11 = 0,0138, 12 = 0,0305 ; dim nul | 0,9972 | 0,5 (juillet, août) à 1,2 (novembre à mars) ; jamais 0 |
| 8 | HOT012_N | lun à jeu : 7 à 9 = 0,022, 19 à 21 = 0,033 ; ven à dim : 7 à 9 = 0,015, 19 à 21 = 0,023 | 1,002 | 1,0 partout |
| 9 | HOT345_N | lun à jeu : 7 à 9 = 0,017, 19 à 21 = 0,0113 ; ven à dim : 7 à 9 = 0,044, 19 à 21 = 0,0293 | 0,9993 | 0,9 (novembre à février) à 1,2 (juillet, août) |
| 10 | HOT012_J | tous les jours : 10 à 14 = 0,0189, 15 à 18 = 0,0121 | 1,0003 | 1,0 partout |
| 11 | HOT345_J | tous les jours : 10 à 14 = 0,0189, 15 à 18 = 0,0121 | 1,0003 | 0,9 à 1,2 |
| 12 | CRE | lun à ven : 7 = 0,005, 8 = 0,0083, 9 à 18 = 0,0187 ; sam, dim nuls | 1,0 | 0,5 (vacances, juillet, août) à 1,0 |
| 13 | RES_CON | tous les jours : 9 = 0,0286, 13 = 0,0429, 22 = 0,0714 | 1,0 | 1,0 partout |
| 14 | RES_1RJ-5J7 | lun à ven : 9 = 0,08, 13 = 0,12 ; sam, dim nuls | 1,0 | 1,0 ; 0 la 4e semaine de décembre |
| 15 | RES_2RJ-7J7 | tous les jours : 9 = 0,0571, 13 = 0,0857 | 1,0 | 1,0 partout |
| 16 | RES_2RJ-6J7 | lun à sam : 9 = 0,0667, 13 = 0,1 ; dim nul | 1,0 | 1,0 partout |
| 17 | COM | lun à sam : 7 = 0,1667 ; dim nul | 1,0 | 1,0 partout |
| 18 | VES | lun à sam : 10, 12, 15, 18 = 0,028, 21 = 0,035 ; dim : 10, 12, 15 = 0,028, 18 = 0,035 | 1,001 | 0,5 (3e et 4e semaines d'août) à 1,2 (décembre à février) ; 0 la 1re semaine de janvier et la 4e de décembre |
| 19 | EHPAD | tous les jours : 6 et 7 = 0,0071, 8 à 10 = 0,014, 11 à 16 = 0,0071, 17 à 19 = 0,01, 20 et 21 = 0,0071 | 1,001 | 0,95 (juillet, août) à 1,05 (janvier, décembre) |
| 20 | SAN_N | tous les jours, cases 6 à 22, en cloche : 0,0007 à 6, maximum 0,0146 à 12, 0,0077 à 22 | 1,00093 | 1,0 partout |
| 21 | SAN_J | lun à sam : 7 à 12 et 17 à 19 = 0,0185 ; dim nul | 1,0 | 1,0 partout |
| 22 | AER | tous les jours : 7 à 24 = 0,0079 | 1,0 | 1,0 partout |
| 23 | IND_3x8 | tous les jours : 8, 9, 16, 17 = 0,0357 | 1,0 | 1,0 ; 0,5 la 4e semaine de décembre |
| 24 | IND_8_18h | lun à ven : 18 à 20 = 0,0667 ; sam, dim nuls | 1,0 | 1,0 ; 0,5 la 4e semaine de décembre |
| 25 | GYM_MUN | identique à l'usage 18 | 1,001 | identique à l'usage 18 |
| 26 | RES_SCO_1RJ_5J7 | lun à ven : 10 = 0,08, 14 = 0,12 ; sam, dim nuls | 1,0 | 0 (vacances scolaires, juillet, août) ou 1,0 |
| 27 | RES_SCO_3RJ_5J7 | lun à ven : 9 = 0,04, 13 = 0,06, 22 = 0,1 ; sam, dim nuls | 1,0 | 0 (vacances scolaires, juillet, août) ou 1,0 |
| 28 | GYM_PRI | lun à sam : 9 à 20 = 0,0113, 21 = 0,0124 ; dim : 9 à 17 = 0,0113, 18 = 0,0124 | 1,0 | identique à l'usage 18 |

Valeurs de contrôle pour les tests (somme hebdomadaire du tableur, nombre de jours actifs, minimum et maximum du facteur annuel) :

```python
# Lu dans scenarios_officiels.json (tableur 2026-04-29), tableau « ECS facteur correctif de la semaine ».
CLE_ECS_CONTROLE = {
    #  usage: (somme hebdo, jours actifs, annuel min, annuel max)
    #  annuel min et max calculés sur les cellules non None du tableau 5 × 12 (8 cellules None par feuille, semaines
    #  inexistantes) ; `cle_horaire` lit None comme 0, et un minimum calculé avec None = 0 vaudrait 0 pour les 28 usages.
    1: (0.99747, 7, 0.0, 1.05),  2: (1.001, 7, 0.0, 1.05),   3: (1.0, 5, 0.5, 1.0),      4: (1.0, 4, 0.0, 1.0),
    5: (1.0, 6, 0.0, 1.0),       6: (1.0, 6, 0.0, 1.1),      7: (0.9972, 6, 0.5, 1.2),   8: (1.002, 7, 1.0, 1.0),
    9: (0.9993, 7, 0.9, 1.2),    10: (1.0003, 7, 1.0, 1.0),  11: (1.0003, 7, 0.9, 1.2),  12: (1.0, 5, 0.5, 1.0),
    13: (1.0, 7, 1.0, 1.0),      14: (1.0, 5, 0.0, 1.0),     15: (1.0, 7, 1.0, 1.0),     16: (1.0, 6, 1.0, 1.0),
    17: (1.0, 6, 1.0, 1.0),      18: (1.001, 7, 0.0, 1.2),   19: (1.001, 7, 0.95, 1.05), 20: (1.00093, 7, 1.0, 1.0),
    21: (1.0, 6, 1.0, 1.0),      22: (1.0, 7, 1.0, 1.0),     23: (1.0, 7, 0.5, 1.0),     24: (1.0, 5, 0.5, 1.0),
    25: (1.001, 7, 0.0, 1.2),    26: (1.0, 5, 0.0, 1.0),     27: (1.0, 5, 0.0, 1.0),     28: (1.0, 7, 0.0, 1.2),
}
```

Remarques de lecture : la somme hebdomadaire n'est pas exactement 1 pour onze usages, 1, 2, 7, 8, 9, 10, 11, 18, 19, 20 et 25 (de 0,9972 à 1,002) ; le texte ne demande pas de la normaliser et les usages 1 et 2 ont été validés avec les valeurs brutes, donc on garde les valeurs brutes (point ouvert 4). Les usages 18, 25 et 28 partagent le même profil annuel (fermeture 1re semaine de janvier et 4e de décembre, demi-activité fin août) ; 18 et 25 ont le même profil hebdomadaire.

## 6. Usages à ECS particulière

- Vestiaires seuls (18) : 79 L/m² de SU par semaine (p. 1054), la plus forte valeur. FA05 v2, p. 4, N.B. : « les vestiaires des établissements sportifs (municipaux, scolaires ou privés) sont compris dans les scénarios conventionnels des usages n° 25 et n° 28. Il ne doit donc pas être saisi un bâtiment multi-usages avec une zone vestiaires seuls pour ces établissements sportifs ». L'usage 18 vise les vestiaires de stade et les vestiaires d'un bâtiment industriel dont l'aire de production est hors RE2020 (FA05 p. 11). Les douches collectives sont déjà dans les locaux conventionnels de 25 et 28 (synthèse p. 26 : « Douches collectives 0,05 »).
- Gymnases (25 et 28) : 13,2 et 33,9 L/m² ; FA09 p. 7 : les tribunes à occupation ponctuelle sont à exclure des débits de ventilation, rien n'est dit sur l'ECS.
- Restaurants (13 à 16, 26, 27) : de 2,2 à 19,5 L/m² ; clé concentrée sur deux ou trois heures de la journée (cases 9, 13 et 22). FA05 p. 10 : une salle de restauration sans cuisine prend le local « salle de restauration » de l'un de ces usages ; un restaurant sans salle (dark kitchen) prend l'usage 13, 15 ou 16. FA09 p. 6 : les cuisines centrales sans service sont hors RE2020 (process) ; le local cuisine d'un restaurant reste soumis.
- Hôtels partie jour (10, 11) et partie nuit (8, 9) : deux zones distinctes avec chacune son a et sa clé ; la partie jour (salle des petits déjeuners, bar) a 5,694 et 4,76 L/m², la partie nuit 22,873 et 18,98.
- Enseignement (4, 5, 7, 26, 27) : iecs(j) = 0 en vacances (47), ce qui arrête le réseau primaire ; la clé annuelle ECS est déjà nulle les semaines de vacances scolaires pour 4, 5, 26 et 27, mais pas pour 7 (minimum 0,5, « 52 s/an » dans la synthèse p. 24).
- Industries (23, 24), commerces (17), aérogares (22) : 0,24 L/m², la plus faible valeur avec 0,2 (enseignement, médiathèques).
- Aucun usage à ECS nulle. Le texte ne dit pas comment traiter une zone d'un usage 8 à 16, 18 à 21, 25 à 28 ou 12 qui n'aurait pas de production d'ECS (point ouvert 7).

## 7. Fiche 9.24 : bâtiments non équipés de production d'ECS (p. 1294)

Champ d'application (§ 9.24.2, p. 1294) : usages 3 (bureaux), 4 (enseignement primaire), 5 (enseignement secondaire), 6 (médiathèques et bibliothèques), 7 (universitaires et atypiques), 17 (commerces), 22 (aérogares), 23 (industries 3x8h), 24 (industries 8h à 18h). « Cette fiche ne s'applique pas aux extensions. » La version 2022 (p. 1260) ne couvrait que bureaux, enseignement primaire et secondaire partie jour.

```python
# Fiche 9.24, § 9.24.2, p. 1294 : usages pour lesquels un bâtiment sans production d'ECS reçoit le système conventionnel.
SANS_ECS_FA924 = {u: (u in (3, 4, 5, 6, 7, 17, 22, 23, 24)) for u in range(1, 29)}
```

Prise en compte (§ 9.24.3, p. 1294), génération conventionnelle : chauffe-eau électriques ; nombre : 1 si SREF < 750 m² « quel que soit le nombre d'étages », sinon « 1 chauffe-eau par niveau et par tranche de 750 m² à l'intérieur d'un niveau » ; capacité 15 L ; pertes par défaut d'un chauffe-eau électrique vertical de moins de 75 L, Qpr = 0,1474 + 0,0719 · V^(2/3) (même formule que le tableau 283 de la fiche 9.9, codée `ballon.py` l. 50) ; température maximale du ballon « par défaut » (valeur non donnée dans la fiche) ; hystérésis 5 °C ; hauteur de l'échangeur 0,3 ; chauffage permanent. Émission : appareils sanitaires de type « douche » ; émetteurs du projet s'il y en a, sinon « mitigeur mécanique économe ».

Effet sur les besoins : avec Rat_douches-bains = 0 pour les usages 4 à 7, 17, 22 à 24, l'appareil « douche » ne change rien (corr_app = 1) ; en bureaux, corr_app = 1 - 0,5 × 0,05 = 0,975. Le « mitigeur mécanique économe » donne part_mitigeur = 1 et corr_em = 0,95 (tableau 273). Rien d'autre ne change dans la fiche 9.6 : a et Nu restent ceux du tableau 277. Les paramètres de génération (nombre, volume, pertes, hystérésis, hauteur d'échangeur, régulation permanente) relèvent de `ballon.py` et de l'assemblage 9.14 ; ce qui manque pour les coder est au point ouvert 6.

## Points ouverts

1. Usage 16, valeur de a : 19,5 dans le texte en vigueur (tableau 277, p. 1054, et synthèse p. 25) contre 4,7 dans le tableur du 29/04/2026. La valeur 19,5 est aussi celle de l'usage 13 (restaurant en continu 18 h/j, 7 j/7) alors que l'usage 15 (2 repas, 7 j/7) vaut 5,3 ; rien ne permet de trancher sans récapitulatif. Le cadre impose le texte : coder 19,5 dans A_TERTIAIRE, garder 4,7 dans A_TERTIAIRE_TABLEUR, faire signaler l'écart par un test de cohérence texte/tableur (sans le faire échouer) et marquer l'usage 16 « doublement non validé ». Se tranchera au banc dès qu'un RSEE d'usage 16 existera (O_B_Ecs_annuel).
2. Nature exacte de `nu_gr_em_e` : le texte en fait un paramètre d'intégration saisi (p. 1055), en m² de surface utile (tableau 277), sans imposer Nu = Rat_em × A_gr. Si un logiciel de saisie remplit Nu avec la SREF ou une surface autre que la SU du groupe, le résultat diffère. Proposition : lire `nu_gr_em_e` tel quel, comparer à Rat_em_e × SU et journaliser un avertissement si l'écart dépasse 1 % ; si `nu_gr_em_e` = 0 pour un usage 3 à 28 avec un émetteur ECS déclaré, lever ValueError (comme pour nb_lgt = 0 en habitation) plutôt que de deviner. À confirmer au banc des bureaux (seul usage non résidentiel disponible).
3. Phrase de la p. 19 (« en fonction du nombre d'équipements, par exemple le nombre de chambres pour un hôtel ») contradictoire avec le tableau 277 (hôtels en m² SU). Le tableau 277 est la fiche algorithmique, il s'applique. Un RSEE d'hôtel confirmerait que `nu_gr_em_e` y est bien en m².
4. Sommes hebdomadaires de la clé différentes de 1 pour onze usages, 1, 2, 7, 8, 9, 10, 11, 18, 19, 20 et 25 (0,9972 à 1,002) : aucune règle de normalisation dans le texte ; garder les valeurs brutes, comme pour les usages 1 et 2 validés. Un écart systématique au banc de l'ordre de la somme signalerait que le moteur CSTB normalise.
5. Fiche 9.6 : entrée Iocc_zone listée au tableau 276 mais absente des équations ; ne pas s'en servir. Entrée « Usage_zone » : sert uniquement à choisir a, Rat_douches-bains et la feuille de clé.
6. Fiche 9.24, ce qui manque pour coder la génération conventionnelle : (a) le texte ne dit pas comment un récapitulatif signale un bâtiment « non équipé » (champ XML inconnu : le modélisateur saisit-il lui-même le chauffe-eau conventionnel, ou le moteur le crée-t-il ?) ; (b) le nombre de chauffe-eau dépend de la surface par niveau, que le RSEE ne porte pas au niveau du groupe ; (c) le cas SREF = 750 m² exactement n'est pas tranché (« moins de » et « plus de ») ; (d) la température maximale « par défaut » n'est pas chiffrée dans la fiche ; (e) rien sur la distribution (longueurs par défaut de (1729), p. 1071 : si δlvc = 0, Lvc_2nd-e = 6 × A_gr,em-e / 80 en habitation et 0,05 × A_gr,em-e pour les autres usages, (1730), p. 1071, donnant ensuite les volumes Vvc_2nd-e et Vhvc_2nd-e ; ou réseau nul) ni sur la position du ballon (volume chauffé ou non). Sans RSEE de ce type, coder une fonction qui construit les paramètres conventionnels à partir de (usage, SREF, nombre de niveaux) et la brancher plus tard.
7. Zone sans production d'ECS dans un usage hors liste 9.24 (8 à 16, 18 à 21, 25 à 28, 12) : le texte ne le prévoit pas. Comportement actuel du moteur (aucun Emetteur_ECS, donc Qw = 0) à conserver, avec un avertissement.
8. Vestiaires d'un établissement sportif saisis en zone 18 en plus d'une zone 25 ou 28 (interdit par FA05 p. 4) : le moteur ne peut pas le détecter avec certitude ; un contrôle de saisie qui avertit quand un même bâtiment porte une zone 18 et une zone 25 ou 28 est une proposition, pas une règle du texte.
9. Usage 7 et iecs(j) : ienseignement = 1 (tableau 4) mais la synthèse p. 24 donne « 52 s/an » et la clé annuelle ECS ne descend jamais à 0 ; l'arrêt du réseau primaire (47) dépend de ivac, lu dans le scénario d'occupation du tableur ; à vérifier dans `ecs_distribution` quand un RSEE d'usage 7 existera.
10. Numérotation : les commentaires de `ecs.py` citent les numéros de 2022 (tableaux 274 à 278, équations 1675, 1677 à 1679, 1684 à 1695) ; à réaligner sur 2026-07 lors du codage (correspondance donnée en tête de ce document).

## Où coder

Fichiers sous ``.

- `openbce/ecs.py` l. 3 à 8 (docstring) : remplacer « (1694) », « (1684 à 1692) », « (1677 à 1679) » par (1693), (1683 à 1691), (1676 à 1678) ; citer la fiche 9.24.
- `openbce/ecs.py` l. 19 : commentaire « tableau 277 » devient « tableau 276 (p. 1052) ». L. 21 et 22 : « (1687, 1691) » devient « (1686, 1690) ».
- `openbce/ecs.py` l. 23, `A_TERTIAIRE = {3: 1.25}` : remplacer par le dict A_TERTIAIRE du § 2 (26 clés, tableau 277, p. 1053 à 1055) ; ajouter `A_TERTIAIRE_TABLEUR` et un test (`banc/` ou tests unitaires) qui compare les deux à `scenarios._scalaire(usage, "nombre de litres")` (`openbce/scenarios.py` l. 41 à 45) et signale l'usage 16.
- `openbce/ecs.py` l. 25 : commentaire « tableau 274 » devient « tableau 273 (p. 1046) ». L. 26, `RAT_DOUCHES_BAINS = {1: 0.8, 2: 0.8, 3: 0.5}` : remplacer par le dict du § 3 (28 clés, tableau 274, p. 1047). L. 27 à 29 : commentaire « tableau 276 » devient « tableau 275 (p. 1047) ».
- `openbce/ecs.py` l. 42 à 50, `volume_hebdomadaire` : l. 43 docstring « (1692) » devient « (1691) » ; l. 44 « (1675) » devient « (1674), (1682) » ; l. 50 garder `A_TERTIAIRE[usage] * emetteur.nombre("nu_gr_em_e", 0.0)` et ajouter le contrôle du point ouvert 2 (ValueError si `nu_gr_em_e` = 0, avertissement si écart à Rat_em_e × surface > 1 %). Les usages 1 et 2 (l. 45 à 49) ne changent pas.
- `openbce/ecs.py` l. 53 à 58, `correction` : aucun changement de code, `RAT_DOUCHES_BAINS[usage]` devient défini pour 28 usages ; docstring « (1677 à 1679) » devient « (1676 à 1678) ».
- `openbce/ecs.py` l. 61 à 71, `cle_horaire` : aucun changement de code (le tableau « ECS facteur correctif de la semaine » existe dans les 28 feuilles) ; ajouter un test sur CLE_ECS_CONTROLE (§ 5) : somme hebdomadaire, jours actifs, bornes annuelles calculées en excluant les cellules None du tableur (sinon le minimum vaut 0 pour les 28 usages), et somme annuelle de la clé sur le calendrier construit par `calendrier.construire()`.
- `openbce/ecs.py` l. 74 à 82, `besoins` : docstring « (1694) », « (1695) » deviennent « (1693) », « (1694) » ; l. 76 (`"SHAB" if usage in (1, 2) else "SU"`) reste, cohérent avec `openbce/groupe.py` l. 108.
- `openbce/ecs.py`, nouvelle fonction proposée `generation_conventionnelle_sans_ecs(usage, sref, nb_niveaux)` (fiche 9.24, p. 1294) : retourne None si `SANS_ECS_FA924[usage]` est faux, sinon un dict exprimé avec les clés que le moteur lit déjà : {nb_chauffe_eau, V_tot = 15 (`openbce/ballon.py` l. 37), Nature_Ballon = 3 (vertical < 75 L, l. 42, 49 et 50), Delta_Theta_base = 5 (hystérésis, l. 104), Theta_Max = non spécifié (la fiche dit « par défaut » sans chiffre, p. 1294 ; le moteur prend 90 °C à défaut, l. 101), type_gest_th_base = 0 (chauffage permanent, l. 105), part_mitigeur = 1 si le projet n'a pas d'émetteur, app_ecs = code « douche(s) seule(s) »}. La hauteur d'échangeur 0,3 de la fiche n'a aucun champ dans le moteur (« hech » n'existe nulle part ; le ballon à quatre zones de `ballon.py` l. 97 à 105 ne positionne qu'un repère `z_reg_base`) : à traduire au codage. Code de l'appareil : le tableau 271, p. 1044, numérote 1 = douche(s) seule(s), 2 = baignoire standard, 3 = grande baignoire, alors que `GAIN_APPAREIL` (`openbce/ecs.py` l. 27 à 29, ordre déduit du banc) place le gain douche 5 % sous le code 0 ; la fiche 9.24 ne donne aucun nom de champ, donc noms et code sont à fixer au codage, pas dans cette spécification. Branchement sur le RSEE différé (point ouvert 6).
- `openbce/scenarios.py` l. 22 (`USAGES`) : déjà 1 à 28, rien à faire ; l. 34 à 38 `_tableau` et l. 41 à 45 `_scalaire` : réutilisables pour les tests ci-dessus.
- `banc/ecs.py` l. 32 (`usage not in (1, 2)`) et l. 34 (`g.nombre("SHAB")`) : étendre au moins à l'usage 3 (SU) pour banquer les bureaux, puis à tout usage dès qu'un RSEE existe ; la ligne de sortie l. 65 doit afficher `nu_gr_em_e` à côté de la surface pour éclairer le point ouvert 2.
- `specs/ecs.md` l. 14 à 20 (entrées RSEE de l'émetteur) : compléter la ligne `nu_gr_em_e` (m² de SU pour les 26 usages non résidentiels) et renvoyer à ce document.
