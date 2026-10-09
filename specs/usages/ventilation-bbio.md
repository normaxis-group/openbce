# Ventilation conventionnelle du Bbio et débits par usage (fiches 6.1, 6.2, 6.3 et 6.5)

Date : 09/10/2026. Thème « ventilation » de la décision « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Tout ce qui suit pour ces usages est lu dans le texte de l'annexe III en vigueur et dans le tableur officiel des scénarios ; rien n'a été confronté à un RSEE.

## Sources lues

| Source | Pages ou lignes lues |
|---|---|
| Annexe III en vigueur (`corpus/texte_annexe3_2026-07/annexe3.txt`, 1 854 pages) : chapitre 2.1 données conventionnelles | p. 17 à 24 |
| Fiche 4.1 C_EIN_Scénarios conventionnels (indicateur de ventilation) | p. 53, 54, 58 |
| Fiche 5.6 C_VEN_Débits_d'air_Cep : entrée booléenne `ihergement` (« indicateur d'usage résidentiel ou hébergement », nomenclature p. 138, sans tableau par usage) ; tableau 22 p. 143 et 144, qui donne le caractère traversant `trav_zone` par usage et non l'hébergement | p. 138, 143, 144 |
| Fiche 6.1 C_VEN_BBIO | p. 321 à 325 (intégrale) |
| Fiche 6.2 C_VEN_Bouche_conduit | p. 326 à 341 (intégrale) ; tableau 56-1 p. 334 et 335 |
| Fiche 6.3 C_VEN_CTA et Double_flux | p. 344 à 346, 352, 354, 355, 360 à 362, 372 à 374, 379 |
| Fiche 6.5 C_VEN_Mécanique_SF | p. 401 à 410 |
| Fiche des fenêtres pariétodynamiques, qui renvoie aux débits conventionnels du tableau 56 | p. 1412 (équations 2557 à 2559), pour mémoire |
| Version 2022 découpée (`corpus/texte_annexe3/006_2_C_VEN_Bouche_conduit.txt`) | p. 316 à 318 de cette version, pour comparer la numérotation |
| Annexe de l'article R. 172-4, chapitre I, X (`corpus/site_2026-10-09/chapitre1a3_annexe_r172-4_post-gtm2.txt`) | lignes 91 à 96 (définition de Sref) |
| Fiche d'application FA05 « usage du bâtiment » v2 du 01/10/2026 | p. 4 à 11 |
| Fiche d'application FA09 « exclusions tertiaire spécifique et industrie » v1 du 01/10/2026 | p. 5 à 7 |
| Tableur officiel des scénarios du 29/04/2026, converti (`openbce/tables/scenarios_officiels.json`) | tableau « ventilation » des 28 feuilles |
| Moteur : `openbce/groupe.py`, `openbce/ventilation.py`, `openbce/consommation.py`, `openbce/ventilateurs.py`, `openbce/scenarios.py`, `openbce/usages.py` ; banc `banc/ventilateurs.py` | intégrale |

Convention de citation : « p. n » renvoie à la pagination « n/1854 » du texte en vigueur ; les numéros d'équations sont ceux imprimés dans ce texte. Attention, la fiche 6.2 réutilise des numéros : la p. 334 ne porte que (399), (402), (405) et (408) ; (402) sert deux fois (p. 334 et p. 336), (405) et (408) aussi (p. 334 et p. 337), et la p. 341 reprend (383) à (385) de la p. 331. (400) et (401) n'apparaissent qu'une fois, p. 336. Les équations sont donc toujours citées avec leur page.

## 1. Le système conventionnel du Bbio (fiche 6.1)

Le texte ne distingue aucun usage dans la fiche 6.1 : « pour tous les usages » (p. 324).

- Le système de ventilation du Bbio est « une VMC à débit soufflé et extrait constant avec efficacité d'échangeur de 50 % » (p. 324, 6.1.3). Paramètre ε « fixée à 0.5 pour le calcul du BBIO », bornes 0 à 1, conventionnelle 0,5 (tableau 55 p. 322).
- Puissance des ventilateurs nulle quel que soit Ivent : Pvent_rep = 0 (374, p. 324), Pvent_souf = 0 (375, p. 324). L'impact des pertes de conduit est nul (376, p. 324).
- Température de l'air repris après ventilateur : T_extr2 = T_extr1 + pel × Pvent_rep / (0,34 × |q_rep,cond|) (377, p. 324), donc T_extr2 = T_extr1 puisque Pvent_rep = 0. Constantes : Cpa = 1006 J/(kg.K), pel = 0,8 (tableau 55 p. 322).
- Air soufflé après l'échangeur : T_souf1 = θext + ε × (T_extr2 − θext) (378, p. 325) ; après ventilateur T_souf2 = T_souf1 (379, p. 325) ; T_air_soufflé = T_souf2 (380, p. 325) ; humidité ω_air_soufflé = ω_ext (381, p. 325).
- Déperditions : Hvent = q_soufflé,cond × Cpa × (1 − ε) (382, p. 325).

Entrées du composant (tableau 55 p. 322) : Ivent (indicateur de ventilation de la zone), débits spécifiques repris et soufflés du groupe, θi,fin(h−1), θext, ωext, Dugd (h/semaine). Les débits eux-mêmes viennent de la fiche 6.2.

Le moteur fait déjà cela pour tout usage : `EPSILON_BBIO = 0.5` (groupe.py l. 24) et `hgei = CPA_VOL * q * (1 - EPSILON_BBIO) + infiltration` (groupe.py l. 230, équation 382). Rien à changer pour les usages 4 à 28.

## 2. Débits conventionnels du Bbio (fiche 6.2)

### 2.1 Règle générale

« Pour le calcul du Bbio, les débits correspondent au débit d'hygiène pour le résidentiel, alors que les débits sont conventionnels en non résidentiel. Pour le calcul des consommations, en résidentiel les débits sont des débits d'hygiène, alors qu'en non résidentiel ce sont des débits totaux soufflés ou extraits. » (p. 331, 6.2.3)

L'indicateur Ivent « est vrai quand la zone est occupée du point de vue de la ventilation et est faux sinon » (p. 331). Il vient du scénario conventionnel de la zone : « la ventilation : arrêt ou marche des systèmes spécifiques de ventilation », produit d'un profil hebdomadaire jour × heure et d'un profil annuel mois × semaine (fiche 4.1, p. 53 et 58 ; sortie Ivent p. 54). Le moteur le lit dans le tableur officiel (`scenarios.py`, tableau « ventilation » de chaque feuille) : conforme, à la réserve près des valeurs 0,5 que porte le tableur pour trois feuilles (point ouvert 10).

### 2.2 Usages hors maison individuelle ou accolée et hors logement collectif (p. 333 à 335)

Débit maximal (occupation) :

- bouche-conduit de reprise (Isouf = 0) : q_rep,max = −Param_occupation × SREF_gr, q_soufflé,max = 0 (399, p. 334) ;
- bouche-conduit de soufflage (Isouf = 1) : q_rep,max = 0, q_soufflé,max = Param_occupation × SREF_gr (402, p. 334).

Débit minimal (inoccupation) :

- reprise : q_rep,min = −max(60 ; Param_inoccupation × SREF_gr), q_soufflé,min = 0 (405, p. 334) ;
- soufflage : q_rep,min = 0, q_soufflé,min = max(60 ; Param_inoccupation × SREF_gr) (408, p. 334).

Le plancher de 60 m³/h est écrit dans l'équation, sans unité explicite ; les paramètres sont en m³/h par m² de SREF_gr (p. 334 ; la version 2022 écrivait « 4 m3/h/m² » et « max(60 m3/h ; 0.42 m3/h/m² × SREF) », p. 317 de cette version).

« Les paramètres Param_occupation et Param_inoccupation sont définis selon le type d'usage réglementaire » (p. 334) par le **tableau 56-1** (p. 334 et 335), reproduit ici sans modification :

| N° | Type d'usage | Param_occupation | Param_inoccupation |
|---|---|---|---|
| 3 | Bureaux | 4 | 0,42 |
| 4 | Enseignement primaire | 7,2 | 0,38 |
| 5 | Enseignement secondaire | 4,7 | 0,38 |
| 6 | Médiathèques et bibliothèques | 5,6 | 0,46 |
| 7 | Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques | 7,4 | 0,6 |
| 8 | Hôtels 0, 1 et 2 étoiles (partie nuit) | 3 | 3 |
| 9 | Hôtels 3, 4 et 5 étoiles (partie nuit) | 2 | 2,2 |
| 10 | Hôtels 0, 1 et 2 étoiles (partie jour) | 8 | 0 |
| 11 | Hôtels 3, 4 et 5 étoiles (partie jour) | 7 | 0 |
| 12 | Établissements d'accueil de la petite enfance | 4,7 | 0,75 |
| 13 | Restaurants, en continu, 18 heures par jour, 7 jours sur 7 | 10 | 0,5 |
| 14 | Restaurants, 1 repas par jour, 5 jours sur 7 | 10 | 0,5 |
| 15 | Restaurants, 2 repas par jour, 7 jours sur 7 | 10 | 0,5 |
| 16 | Restaurants, 2 repas par jour, 6 jours sur 7 | 10 | 0,5 |
| 17 | Commerces | 3,7 | 0 |
| 18 | Vestiaires seuls | 6,7 | 6,7 |
| 19 | Établissements sanitaires avec hébergement | 4,5 | 4,5 |
| 20 | Établissements de santé (partie nuit) | 4,5 | 4,5 |
| 21 | Établissements de santé (partie jour) | 4,5 | 0 |
| 22 | Aérogares | 4 | 0,3 |
| 23 | Industries ou artisanats 3x8h | 3,1 | 0 |
| 24 | Industries ou artisanats 8h à 18h | 3,1 | 0 |
| 25 | Établissements sportifs municipaux ou scolaires | 3 | 0 |
| 26 | Restaurants scolaires, 1 repas par jour, 5 jours sur 7 | 8 | 0,3 |
| 27 | Restaurants scolaires, 3 repas par jour, 5 jours sur 7 | 8 | 0,3 |
| 28 | Établissements sportifs privés | 3 | 0 |

Les usages 1 et 2 ne figurent pas dans ce tableau : « cas des usages maison individuelle ou accolée et logement collectif : on utilise les équations du § 6.2.3.2.2.1 » (p. 335), c'est-à-dire les débits d'hygiène saisis (voir 2.4).

Les valeurs des usages 3, 4 et 5 sont celles de la version 2022, qui ne connaissait que ces trois typologies (bureaux 4 et 0,42 ; enseignement primaire 7,2 et 0,38 ; enseignement secondaire 4,7 et 0,38, équations 399 à 410 p. 317 et 318 de cette version). Le moteur n'avait codé que les bureaux.

Les débits sont donnés **par usage et au niveau du groupe**, rapportés à SREF_gr ; aucun débit conventionnel de Bbio n'est défini par local dans la fiche 6.2. Les locaux conventionnels du chapitre 15 ne portent que les occupants et les apports (FA05 p. 6).

### 2.3 Chaîne de calcul jusqu'au débit utile, en Bbio

1. Débits régulés (6.2.3.2.2.1, p. 336) : en occupation q_regul = Crdbnr × q_max (400 et 401, p. 336) ; en inoccupation Crdbnr = 1 et q_regul = q_min (402, p. 336). « Dans le cas particulier du Bbio, Crdbnr = 1 quelle que soit l'occupation et l'usage du groupe » (p. 335).
2. Coefficient de dépassement : « pour le calcul conventionnel du BBIO, Cdep_BBio = 1 » (414, p. 338) ; q_dep = Cdep × q_regul (412 et 413, p. 338).
3. Fuites de réseau : Kres = 0 « cas de l'aération et du BBio » (tableau 59, p. 339), donc q_fuites = 0 (419 et 420, p. 339) et q_spec = q_dep (428 et 429, p. 341), q_cond = q_dep (430 et 431, p. 341).

Au total, pour un groupe d'usage u (3 à 28), de surface SREF_gr, à l'heure h :

- Ivent(h) = 1 : q(h) = Param_occupation[u] × SREF_gr ;
- Ivent(h) = 0 : q(h) = max(60 ; Param_inoccupation[u] × SREF_gr) ;
- Hvent(h) = 0,34 × q(h) × (1 − 0,5) en Wh/(h.K), soit l'équation (382) avec Cpa volumique (groupe.py l. 25, CPA_VOL = 0,34).

Le plancher de 60 m³/h est écrit par bouche-conduit g,s ; le système conventionnel du Bbio est une VMC unique par groupe (p. 324), le plancher s'applique donc une fois par groupe. C'est ce que fait déjà groupe.py l. 138.

### 2.4 Usages 1 et 2, pour mémoire (validés, hors périmètre de cette spécification)

Débits d'hygiène saisis : q_rep,max = −q_spec,rep,conv_pointe, q_rep,min = −q_spec,rep,conv_base (387 à 390, p. 332) ; débit régulé constant quelle que soit l'occupation q_regul = Crdbnr × (q_max × Dugd + q_min × (168 − Dugd)) / 168 (403, p. 336) avec Dugd = 14 h/semaine en mode Bbio (tableau 57 p. 336, note 1 p. 337), Crdbnr = 1, Cdep = 1, Kres = 0. Le moteur lit les champs `Qv_occ_BBIO` et `Qv_inocc_BBIO` du groupe (groupe.py l. 135) ; le scénario de ventilation du tableur vaut 1 à toute heure pour les feuilles MI et LC, donc seul `Qv_occ_BBIO` sert. Non modifié ici.

### 2.5 Surface de référence

SREF_gr est « la surface de référence du groupe » (tableau 56, p. 327). La surface de référence est définie par l'annexe de l'article R. 172-4, chapitre I, X : « pour un bâtiment ou une partie de bâtiment à usage d'habitation, la surface habitable ; pour les autres cas, la surface utile » (lignes 91 à 96 du fichier cité). FA05 le rappelle p. 7 (« surface habitable, SHAB, ou surface utile, SU, suivant usage »). Le moteur prend SHAB pour les usages 1 et 2 et SU pour les autres (groupe.py l. 108) : conforme pour les usages 3 à 28.

### 2.6 Usages à occupation continue (hôtels nuit, santé nuit, industrie 3x8)

Le texte ne prévoit aucun traitement particulier : la fiche 6.1 vaut « pour tous les usages » (p. 324) et la fiche 6.2 ne distingue que résidentiel et non résidentiel (p. 331). Ce qui change d'un usage à l'autre, c'est le scénario Ivent du tableur et le couple du tableau 56-1. Heures de ventilation par semaine lues dans le tableur du 29/04/2026 (tableau « ventilation », profil hebdomadaire ; donnée du tableur, pas du texte) :

| Usage | Feuille | Ivent = 1, h/semaine | Par jour (lun à dim) | Conséquence en Bbio |
|---|---|---|---|---|
| 8 | HOT012_N | 105 | 15 × 7 | inoccupation 9 h par jour au débit max(60 ; 3 × SREF), identique à l'occupation |
| 9 | HOT345_N | 105 | 15 × 7 | inoccupation 9 h par jour au débit max(60 ; 2,2 × SREF), supérieur à l'occupation (2 × SREF) |
| 13 | RES_CON | 133 | 19 × 7 | inoccupation 5 h par jour à max(60 ; 0,5 × SREF) |
| 15 | RES_2RJ-7J7 | 84 | 12 × 7 | inoccupation 12 h par jour |
| 18 | VES | 95 | 14 × 6 + 11 | inoccupation à 6,7 × SREF, identique à l'occupation |
| 19 | EHPAD | 168 | 24 × 7 | jamais d'inoccupation : Param_inoccupation (4,5) sans effet |
| 20 | SAN_N | 168 | 24 × 7 | jamais d'inoccupation : Param_inoccupation (4,5) sans effet |
| 22 | AER | 133 | 19 × 7 | inoccupation 5 h par jour à max(60 ; 0,3 × SREF) |
| 23 | IND_3x8 | 168 | 24 × 7 | jamais d'inoccupation : Param_inoccupation (0) sans effet |

Pour les autres usages non résidentiels (3 à 7, 10 à 12, 14, 16, 17, 21, 24 à 28), Ivent vaut 0 une partie de la semaine et le débit d'inoccupation s'applique ; avec Param_inoccupation = 0 (10, 11, 17, 21, 23, 24, 25, 28) il vaut 60 m³/h pour le groupe. Les usages 4, 5, 6, 14, 18, 25, 26, 27, 28 ont aussi des semaines à Ivent = 0 dans le profil annuel (vacances), où seul le débit d'inoccupation s'applique. L'usage 17 (COM) compte 87 h par semaine : six jours (lundi à samedi) à 14,5 h chacun, la 7e heure du jour à 0,5 et les 8e à 21e heures à 1, dimanche à 0 (point ouvert 10 pour la valeur 0,5).

## 3. Efficacité d'échangeur

- Bbio : ε = 0,5 pour tous les usages (p. 322 et 324). Aucune valeur par usage.
- Th-C (fiche 6.3, prétraitement selon le statut de la donnée, p. 360 et 361) : statut certifié (idstatut_echangeur = 2) ε = ε_saisi (396, p. 360) ; justifié (1) ε_t = 0,9 × ε_saisi (397, p. 361) ; déclaré (0) ε_t = MIN(0,8 × ε_saisi ; ε_utile_max) (398, p. 361). La constante ε_utile_max, « efficacité maximale de l'échangeur en l'absence de valeurs certifiées ou justifiées », vaut **0,5** (tableau 61, p. 352). Le moteur porte `EPS_UTILE_MAX = 0.9` (ventilation.py l. 36) : écart au texte, indépendant de l'usage, signalé en point ouvert. Le texte précise aussi que « l'efficacité ε_t définie en paramètre doit être mesurée pour des débits correspondant à la zone neutre en occupation » (p. 360).
- Antigel (Th-C, fiche 6.3, tableau 62 p. 379) : θsech_LIM par défaut −5 °C pour les échangeurs rotatifs en bâtiment non résidentiel, 0 °C pour les échangeurs à plaques en non résidentiel, 5 °C « autres cas » (dont le résidentiel). Seule dépendance à l'usage de la fiche 6.3 ; la fonction antigel n'est pas traitée dans ventilation.py.

## 4. Débits conventionnels en Th-C

Il n'existe aucun débit conventionnel Th-C par usage dans la fiche 6.2 : en non résidentiel les débits de consommation sont « des débits totaux soufflés ou extraits » saisis (p. 331 ; champs Qv_rep_occ, Qv_rep_inocc, Qv_souf_occ, Qv_souf_inocc des bouches, ventilation.py l. 81), en résidentiel les débits d'hygiène saisis (pointe et base). Ce qui dépend de la typologie en Th-C :

| Grandeur | Valeurs | Source |
|---|---|---|
| Crdbnr, coefficient de réduction des débits en non résidentiel | aucune régulation 1 ; détection d'utilisation du local 0,9 ; comptage d'occupants ou sondes CO2 0,8 ; en inoccupation Crdbnr = 1 (402 p. 336) ; aération Crdbnr = 1 | tableau 57, p. 335 |
| Dugd, durée d'utilisation du grand débit (résidentiel seulement) | ventilation mécanique : gestion manuelle (par défaut) 14 h/semaine, temporisation 7 ; ventilation naturelle par conduit et hybride : maison individuelle 14, logement collectif 28 ; mode Bbio 14 | tableau 57 (deuxième tableau portant ce numéro), p. 336 ; note 1 p. 337 |
| Cdep, coefficient de dépassement | par défaut 1,30 ; composants autoréglables certifiés 1,15 ; hygroréglables certifiés : valeur de l'évaluation ; aération Cdep = Cfenb = 1,7 (p. 328, p. 338) ; Bbio 1 (414) | tableau 58, p. 338 |
| Kres, fuite de réseau | classe A 0,027·10⁻³ ; B 0,009·10⁻³ ; C 0,003·10⁻³ ; défaut 0,0675·10⁻³ m³/(s.m²) sous 1 Pa ; aération et Bbio 0 | tableau 59, p. 339 |
| Ratfuitevc, Ratsurfcond, Ratdebcond, dP | maison individuelle 0,25 ; Ratsurfcond 0,05 m² par m² de SHAB ; 80 Pa haute pression, 20 Pa basse pression. Bâtiment collectif 0,5 ; Ratdebcond 0,05 m² par m³/h ; 160 Pa HP, 20 Pa BP. Bâtiment non résidentiel 0,75 ; Ratdebcond 0,05 ; 250 Pa HP (case BP vide) | tableau 60, p. 340 |
| Surface de conduit par défaut | maison individuelle A_cond = SHAB × Ratsurfcond (421, p. 339) ; non résidentiel ou collectif A_cond = abs(q_max) × Ratdebcond (424 et 425, p. 340 ; CTA et double flux 426 et 427 avec q_CH,max) | p. 339 et 340 |

Le texte ne connaît en Th-C que trois typologies pour ces paramètres (maison individuelle, bâtiment collectif, bâtiment non résidentiel) : les usages 3 à 28 partagent les valeurs « non résidentiel ». Le moteur les applique déjà par défaut à tout usage autre que 1 et 2 (`RATFUITEVC.get(usage, 0.75)`, `DP_HP.get(usage, DP_HP_DEFAUT)` avec 250, ventilation.py l. 43 à 47 et 93 à 98 ; `surface * RATSURFCOND if usage == 1 else max(q) * RATDEBCOND`, l. 95). Rien à ajouter pour les usages 4 à 28.

Deux règles de saisie, pas de code, viennent de FA09 (p. 5 à 7) : les débits exclusivement liés au process (postes de cuisson professionnels, plateaux techniques hospitaliers) sont exclus ; pour un gymnase avec tribunes, les débits des tribunes sont exclus et les puissances de ventilateur adaptées.

## 5. Ventilateurs (fiches 6.5 et 6.3)

### 5.1 Simple flux, fiche 6.5 (p. 407 et 408)

- Non résidentiel : extraction Pvent = Pvent_occ si Ivent vrai (636), Pvent_inocc sinon (637) ; insufflation idem (638, 639) ; p. 407. Pas de notion de pointe et de base en non résidentiel : la « répartition » se fait entre occupation et inoccupation par Ivent, puis entre groupes au prorata des débits spécifiques repris Pvent_g = Pvent × q_spec_repris(g,s) / Σ_s q_spec_repris (642, p. 407) ou soufflés (644, p. 407). Consommation Cvent = Pvent (645), Cvent_g = Pvent_g (646), p. 408.
- Résidentiel : Dugd_equ = max(Dugd_s) sur les bouches du système (640, p. 407) ; Pvent = (Pvent_pointe × Dugd_equ + Pvent_base × (168 − Dugd_equ)) / 168 quel que soit Ivent (641 extraction, 643 insufflation, p. 407).

Le moteur traite les deux branches dans `consommation.puissance_ventilateurs` (consommation.py l. 42 à 47 résidentiel, l. 48 à 51 non résidentiel) avec `usage in (1, 2)` comme critère : conforme pour les usages 3 à 28, Ivent venant du tableur. `ventilateurs.de_la_zone` (ventilateurs.py l. 23 et 24) refuse encore le non résidentiel.

### 5.2 Double flux et CTA, fiche 6.3

- Résidentiel (double flux) : Dugd = MAX_g,s(Dugd) (390, p. 360) ; Pvent,occ,sou = ((168 − Dugd) × Pvent,base,sou + Dugd × Pvent,pointe,sou) / 168 (391), Pvent,inocc,sou = Pvent,occ,sou (392), idem reprise (393, 394), p. 360. Les CTA ne sont pas prévues en résidentiel (p. 354) ; en résidentiel seul le double flux (Type_ventilation_mecaniq = 1) est compatible (p. 354 et 355).
- Non résidentiel, double flux (Type_ventilation_mecaniq = 1) : Pvent_rep(h) = Pvent_rep_occ et Pvent_sou(h) = Pvent_sou_occ si isvent(h) = 1 (458), sinon les valeurs inocc (459), p. 372.
- CTA à débit constant (type 2) : CH en occupation, en relance, ou si un besoin a été détecté au pas précédent en inoccupation (460), sinon ZN_inocc (461), p. 372 ; type 3 régulé selon la charge : mêmes règles (462, 463, p. 373) ; débit variable (type 4) : ZN_occ (464) ou ZN_inocc (465), p. 373, avec rafraîchissement adiabatique actif : interpolation cubique entre ZN_occ et CH (466 à 468, p. 373 et 374) ; surventilation mécanique : Pvent_rep_raf,noc (457, p. 372). Les trois débits des CTA (ZN_inocc, ZN_occ, CH) sont décrits p. 355.

Aucune de ces règles ne dépend du numéro d'usage au-delà de la distinction résidentiel (1, 2) et non résidentiel (3 à 28).

## 6. Tables prêtes à copier

```python
# Fiche 6.2, tableau 56-1 (p. 334 et 335) : débits conventionnels du Bbio en non résidentiel, m³/h par m² de SREF_gr.
# Occupation : q = Param_occupation × SREF_gr (399 reprise, 402 soufflage, p. 334).
# Inoccupation : q = max(60 ; Param_inoccupation × SREF_gr) (405 reprise, 408 soufflage, p. 334).
# Usages 1 et 2 : non spécifié dans ce tableau ; débits d'hygiène saisis (387 à 390 p. 332, 403 p. 336, Dugd = 14 p. 336).
PARAM_OCCUPATION = {
    1: None,    # non spécifié : résidentiel, débits d'hygiène saisis (p. 331, 335)
    2: None,    # non spécifié : résidentiel, débits d'hygiène saisis (p. 331, 335)
    3: 4.0,
    4: 7.2,
    5: 4.7,
    6: 5.6,
    7: 7.4,
    8: 3.0,
    9: 2.0,
    10: 8.0,
    11: 7.0,
    12: 4.7,
    13: 10.0,
    14: 10.0,
    15: 10.0,
    16: 10.0,
    17: 3.7,
    18: 6.7,
    19: 4.5,
    20: 4.5,
    21: 4.5,
    22: 4.0,
    23: 3.1,
    24: 3.1,
    25: 3.0,
    26: 8.0,
    27: 8.0,
    28: 3.0,
}

PARAM_INOCCUPATION = {
    1: None,    # non spécifié (voir ci-dessus)
    2: None,    # non spécifié (voir ci-dessus)
    3: 0.42,
    4: 0.38,
    5: 0.38,
    6: 0.46,
    7: 0.6,
    8: 3.0,
    9: 2.2,
    10: 0.0,
    11: 0.0,
    12: 0.75,
    13: 0.5,
    14: 0.5,
    15: 0.5,
    16: 0.5,
    17: 0.0,
    18: 6.7,
    19: 4.5,
    20: 4.5,
    21: 0.0,
    22: 0.3,
    23: 0.0,
    24: 0.0,
    25: 0.0,
    26: 0.3,
    27: 0.3,
    28: 0.0,
}

PLANCHER_INOCCUPATION = 60.0    # m³/h par groupe, « max(60 ; ...) » (405, 408, p. 334)

# Forme directement compatible avec groupe.py l. 27 et 28 (même structure que les constantes actuelles) :
DEBIT_CONVENTIONNEL = {u: v for u, v in PARAM_OCCUPATION.items() if v is not None}
DEBIT_INOCCUPATION = {u: (PLANCHER_INOCCUPATION, v) for u, v in PARAM_INOCCUPATION.items() if v is not None}

# Fiche 6.1 (p. 322, 324) : efficacité d'échangeur du système conventionnel du Bbio, tous usages.
EPSILON_BBIO = 0.5

# Fiche 6.2, tableau 57 (second du nom, p. 336) : durée d'utilisation du grand débit, h/semaine, résidentiel seulement.
DUGD_MECANIQUE = {"manuel": 14.0, "temporisation": 7.0}      # dispositifs à gestion manuelle (par défaut), avec temporisation
DUGD_NATURELLE_HYBRIDE = {1: 14.0, 2: 28.0}                   # maison individuelle 14, logement collectif 28
DUGD_BBIO = 14.0                                              # mode Bbio (p. 336 ; note 1 p. 337)
# Usages 3 à 28 : non spécifié (Dugd ne sert qu'aux usages 1 et 2).

# Fiche 6.2, tableau 57 (p. 335) : Crdbnr en non résidentiel, Th-C ; Bbio = 1 pour tout usage (p. 335).
CRDBNR = {"aucune": 1.0, "detection_local": 0.9, "comptage_ou_co2": 0.8}

# Fiche 6.2, tableau 58 (p. 338) : Cdep ; Bbio = 1 (414, p. 338) ; aération = Cfenb = 1,7 (p. 328, 338).
CDEP = {"defaut": 1.30, "autoreglable_certifie": 1.15}       # hygroréglable certifié : valeur de l'évaluation

# Fiche 6.2, tableau 59 (p. 339) : Kres, m³/(s.m²) sous 1 Pa ; aération et Bbio : 0.
KRES = {"A": 0.027e-3, "B": 0.009e-3, "C": 0.003e-3, "defaut": 0.0675e-3}

# Fiche 6.2, tableau 60 (p. 340), par typologie : (Ratfuitevc, Ratsurfcond, Ratdebcond, dP haute pression, dP basse pression).
# Les usages 3 à 28 relèvent tous de la ligne « bâtiment non résidentiel » (le texte ne distingue pas plus finement).
TABLEAU_60 = {
    "maison_individuelle": (0.25, 0.05, None, 80.0, 20.0),
    "batiment_collectif": (0.5, None, 0.05, 160.0, 20.0),
    "batiment_non_residentiel": (0.75, None, 0.05, 250.0, None),   # dP basse pression : non spécifié (case vide)
}

# Fiche 6.3, tableau 61 (p. 352) et équations 396 à 398 (p. 360, 361) : efficacité d'échangeur retenue en Th-C.
CERTIFICAT = {2: 1.0, 1: 0.9, 0: 0.8}     # certifié ε saisi ; justifié 0,9 ε ; déclaré min(0,8 ε ; ε_utile_max)
EPS_UTILE_MAX_TEXTE = 0.5                 # p. 352 (le moteur porte 0,9 : point ouvert)

# Fiche 6.3, tableau 62 (p. 379) : seuil antigel θsech_LIM par défaut, °C.
TSECH_LIM = {"rotatif_non_residentiel": -5.0, "plaques_non_residentiel": 0.0, "autres": 5.0}

# Tableur officiel du 29/04/2026 (donnée du tableur, pas du texte) : somme du profil hebdomadaire « ventilation » (7 jours × 24 h),
# sans le profil annuel. Usage 17 : 6 × 14,5 = 87, dont six valeurs 0,5 comptées pour 0,5 (point ouvert 10).
IVENT_HEURES_SEMAINE = {
    1: 168, 2: 168, 3: 50, 4: 45, 5: 54, 6: 47, 7: 65, 8: 105, 9: 105, 10: 98, 11: 98, 12: 60, 13: 133, 14: 30,
    15: 84, 16: 66, 17: 87, 18: 95, 19: 168, 20: 168, 21: 66, 22: 133, 23: 168, 24: 50, 25: 88, 26: 30, 27: 65, 28: 88,
}
```

## 7. Points ouverts

1. **Usage 9, Param_inoccupation (2,2) supérieur à Param_occupation (2)** (tableau 56-1 p. 334). Le texte est codé tel quel ; seul un récapitulatif d'hôtel 3 à 5 étoiles dirait si c'est une coquille.
2. **Plancher de 60 m³/h par groupe ou par bouche-conduit.** L'équation est écrite par composant g,s ; en Bbio le système est unique par groupe (p. 324), donc une fois par groupe. Si un jour le Bbio était calculé par bouche saisie, le plancher se multiplierait. Lecture retenue : une fois par groupe, comme aujourd'hui pour les bureaux.
3. **Groupes à plusieurs usages dans une zone.** Le texte rapporte le débit à SREF_gr et le paramètre au « type d'usage réglementaire » ; un groupe porte un seul usage dans les RSEE. Rien à trancher tant que l'usage est porté par la zone.
4. **ε_utile_max = 0,5** (tableau 61 p. 352) contre `EPS_UTILE_MAX = 0.9` dans ventilation.py l. 36. Indépendant de l'usage, inactif sur le lot (seul le code 2 y figure, commentaire l. 33 et 34). À trancher au banc des bureaux ou sur un RSEE à échangeur de statut déclaré.
5. **Numérotation des tableaux de la fiche 6.2** : le texte en vigueur porte deux « Tableau 57 » (Crdbnr p. 335, Dugd p. 336) puis 58 (Cdep), 59 (Kres), 60 (ratios) ; la version 2022 numérotait 57, 58, 59, 60, 61. Les commentaires du moteur (« tableau 58 » pour Dugd, « tableau 59 » pour Cdep, « tableaux 60 et 61 » pour les fuites) suivent la version 2022 : à mettre à jour avec la page.
6. **Numérotation des équations** : le moteur cite (399 à 401) pour l'occupation et (405, 408) pour l'inoccupation, numérotation 2022 où 400 et 401 étaient les deux enseignements. Dans le texte en vigueur, l'occupation est (399) et (402), l'inoccupation (405) et (408), p. 334 ; (402) est réutilisé p. 336, (405) et (408) p. 337, et (400), (401) n'existent qu'à la p. 336. Citer avec la page.
7. **Ivent des usages à ventilation continue** (19, 20, 23) : le débit d'inoccupation n'est jamais sollicité en Bbio ; Param_inoccupation reste codé pour la cohérence du tableau. Si un futur tableur change le profil, aucune modification du moteur n'est nécessaire.
8. **Ventilateurs des CTA non résidentielles** (fiche 6.3, 457 à 468 p. 372 à 374) : hors du périmètre de consommation.py (simple flux occ/inocc seulement) ; aucun paramètre n'y dépend du numéro d'usage, mais les trois régimes CH, ZN_occ, ZN_inocc restent à coder pour tout usage, y compris les bureaux. Se déduira au banc des bureaux seulement (seuls RSEE disponibles).
9. **Th-D** (confort d'été) et **Th-C** utilisent la ventilation réelle, pas le système conventionnel ; les débits saisis des bouches en non résidentiel (occ, inocc) valent pour les usages 4 à 28 comme pour les bureaux. Pas de donnée conventionnelle à ajouter, mais pas de validation possible non plus.
10. **Valeurs 0,5 d'Ivent dans le tableur.** Le texte définit Ivent comme un booléen : « Indicateur de ventilation de la zone (Occ / Inocc) Bool » (tableau 55 p. 322 ; tableau 56 p. 327) et « est vrai quand la zone est occupée du point de vue de la ventilation et est faux sinon » (p. 331). Le tableur du 29/04/2026 porte pourtant des 0,5 dans trois feuilles : COM (usage 17), 7e heure du jour du lundi au samedi dans le profil hebdomadaire ; IND_3x8 (23) et IND_8_18h (24), semaine 4 de décembre dans le profil annuel. Le moteur multiplie les deux profils sans arrondi (scenarios.py l. 83 à 85 et 95, `produit("ventilation")`) et les trois lecteurs testent `> 0` : groupe.py l. 223 (débit du Bbio), ventilation.py l. 83 (débits réels des bouches) et consommation.py l. 51 (puissance des ventilateurs en non résidentiel) ; un 0,5 est donc lu comme une heure d'occupation. Le texte ne prévoit pas cette valeur (demi-débit, demi-heure ou arrondi) : lecture retenue par défaut, celle du moteur, sans fondement dans le texte ; à trancher sur un RSEE de commerce ou d'industrie seulement, aucun n'étant disponible. Sans effet sur les bureaux.

## 8. Où coder

| Fichier, ligne | État actuel | Modification |
|---|---|---|
| `openbce/groupe.py` l. 27 `DEBIT_CONVENTIONNEL = {3: 4.0}` | bureaux seuls | remplacer par le dict `DEBIT_CONVENTIONNEL` du § 6 (usages 3 à 28, tableau 56-1 p. 334 et 335 ; équations 399 et 402 p. 334) |
| `openbce/groupe.py` l. 28 `DEBIT_INOCCUPATION = {3: (60.0, 0.42)}` | bureaux seuls | remplacer par le dict `DEBIT_INOCCUPATION` du § 6, même structure `(plancher 60, paramètre)` (équations 405 et 408 p. 334) |
| `openbce/groupe.py` l. 24 `EPSILON_BBIO = 0.5` | conforme | inchangé (p. 322, 324) ; mettre la page dans le commentaire |
| `openbce/groupe.py` l. 108 `surface = SHAB si usage in (1, 2) sinon SU` | conforme | inchangé (SREF, annexe R. 172-4 chap. I, X ; FA05 p. 7) |
| `openbce/groupe.py` l. 135 à 138 (`if usage in DEBIT_CONVENTIONNEL`) | la logique vaut pour tout usage présent dans le dict | inchangé : avec les dicts étendus, les usages 3 à 28 prennent le débit conventionnel, 1 et 2 gardent `Qv_occ_BBIO` et `Qv_inocc_BBIO` ; ajouter un `assert` ou un message si un usage non résidentiel manque au dict |
| `openbce/groupe.py` l. 223 (`q = q_occ if sc.ventilation[h] > 0 else q_inocc`) et l. 230 (équation 382) | conformes | inchangés ; commentaire : (382) p. 325 |
| `openbce/groupe.py` l. 136 commentaire « (399 à 401) » | numérotation 2022 | remplacer par « (399, 402, 405, 408) p. 334, tableau 56-1 p. 334 et 335 » |
| `openbce/ventilation.py` l. 20 à 24 `DUGD` (commentaire « tableau 58 ») | résidentiel seul, conforme | commentaire : tableau 57 p. 336, note 1 p. 337 ; ajouter si besoin les lignes naturelle/hybride (MI 14, LC 28) non lues aujourd'hui |
| `openbce/ventilation.py` l. 25 à 30 `CDEP` (commentaire « tableau 59 ») | `CDEP = {0: 1.30, 1: 1.0}` (l. 30) : lecture des codes 0, 1, 2 des RSEE tranchée au banc (commentaire l. 25 à 29 : code 1 lu 1,0, code 2 = champ Cdep_Value) ; la valeur 1,15 des autoréglables certifiés (tableau 58 p. 338) n'y figure pas | inchangé ; commentaire : tableau 58 p. 338 ; aération Cfenb 1,7 non traitée ; 1,15 absent du moteur, à ne coder que si un banc le demande |
| `openbce/ventilation.py` l. 31 à 36 `CERTIFICAT`, `EPS_UTILE_MAX = 0.9` | valeurs 396 à 398 conformes ; plafond 0,9 contre 0,5 au texte | point ouvert 4 ; si tranché, `EPS_UTILE_MAX = 0.5` (tableau 61 p. 352) |
| `openbce/ventilation.py` l. 37 à 47 `KRES`, `DP_HP`, `RATFUITEVC`, `RATSURFCOND`, `RATDEBCOND` | les valeurs par défaut couvrent déjà tout usage autre que 1 et 2 | inchangé ; commentaire : tableaux 59 p. 339 et 60 p. 340 |
| `openbce/ventilation.py` l. 73 à 83 `_debit_bouche` | `usage in (1, 2)` sépare résidentiel et non résidentiel | inchangé pour 4 à 28 (p. 331 ; 383 à 386 p. 331 ; 400 à 402 p. 336 ; 412, 413 p. 338) |
| `openbce/ventilation.py` l. 86 à 100 `_fuites` | `usage == 1` pour Ratsurfcond, sinon Ratdebcond | inchangé (421 p. 339 ; 424 à 427 p. 340) |
| `openbce/consommation.py` l. 42 à 47 (résidentiel, Dugd) | conforme (640, 641, 643 p. 407) | inchangé ; commentaire « tableau 58 » l. 44 à remplacer par « tableau 57 p. 336 » |
| `openbce/consommation.py` l. 48 à 51 (non résidentiel, occ/inocc) | conforme (636 à 639 p. 407), vaut pour 3 à 28 | inchangé ; répartition (642, 644 p. 407) déjà faite l. 39 |
| `openbce/ventilateurs.py` l. 12 à 14 `DUGD` (commentaire l. 12 et 13, dict l. 14) et l. 23 et 24 (test `usage not in (1, 2)` l. 23, `NotImplementedError` l. 24 ; la l. 22 est la docstring) | résidentiel seul | si le module doit couvrir 3 à 28 : même branche occ/inocc que consommation.py l. 48 à 51 ; commentaire « tableau 58 » à corriger |
| `openbce/usages.py` l. 42 `VALIDES = frozenset({1, 2, 3})` (la l. 39 porte l'entrée 28 du dict `NOMS`) | avertissement sur 4 à 28 | inchangé : les usages 4 à 28 restent non validés |
| `openbce/scenarios.py` (`ventilation=produit("ventilation")`) | Ivent du tableur pour les 28 feuilles | inchangé |
