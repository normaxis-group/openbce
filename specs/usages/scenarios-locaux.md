# Scénarios conventionnels et locaux des 28 usages

Spécification OpenBCE, thème « scenarios ». Date : 09/10/2026, corrigée le même jour après contre-lecture (références des tableaux 77 à 79 et de ihebergement, vacances scolaires des usages 5, 26 et 27, ventilation de l'usage 18, unités de la feuille 22, chambres des hôtels 8 et 9, décompte 129 sur 135, débits conventionnels du Bbio, lignes du moteur, tests, coquille de FA05 p. 11). Décision de Cédric PLANTAZ (ARKEMEP) du 09/10/2026 : « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Le NAS ne contient aucun RSEE RE2020 d'usage 4 à 28. Les usages 1 à 3 sont validés au banc ; les usages 4 à 28 sont codés sur la foi du texte de l'annexe III et du tableur officiel du 29/04/2026, et doivent rester signalés comme tels dans les sorties (`openbce/usages.py` : `VALIDES = frozenset({1, 2, 3})`, `non_valides()`, `avertissement()` ; `openbce/api.py` l. 50 ; `docs/schemas/resume.schema.json` l. 88, champ `usages_non_valides`). Rien n'est demandé au CSTB.

## Sources lues

- Annexe III en vigueur, texte consolidé juillet 2026 (`corpus/texte_annexe3_2026-07/annexe3.txt`, 1 854 pages) : chapitre 2.1 « Données conventionnelles d'occupation et d'usage », p. 17 à 27, dont la synthèse des scénarios p. 23 à 26 (tableau en format paysage ; l'extraction texte en mélange les lignes, la synthèse a donc été relue avec la position des mots dans le PDF `corpus/site_2026-10-09/annexeiii_arrete_4_aout_2021_complet_compresse.pdf`, pages 24 à 26) ; fiche 4.1 C_EIN_Scénarios conventionnels, p. 52 à 63 (tableau 3 nomenclature p. 52 à 55, calendrier p. 56, tableau 4 p. 57, tableaux 5 et 6 p. 58, équations 27 à 55 p. 58 à 63) ; fiche 4.3 FA « Comment identifier l'usage d'un bâtiment et l'exigence associée », p. 69 ; fiche 4.4 extension, p. 70 ; fiche 6.2 C_VEN_Bouche_conduit, débits conventionnels du Bbio p. 334 et 335 (équations 399, 402, 405 et 408 ; tableau 56-1 p. 335) et débits régulés, p. 336 (équations 400 à 402) ; fiche 6.3 CTA, p. 355 et 356 ; fiche 6.5 ventilateurs, p. 407 (équations 636 à 639) ; fiche 7.1 éclairage : liste des types de locaux p. 474 et 475 (sans numéro de tableau, « en entrée du Tableau 78 »), tableau 77 nomenclature p. 475 à 480, tableau 78 valeurs de C1 et de l'éclairement de référence par usage et type de local p. 488 à 491 (le corps du texte p. 488 l'appelle « tableau 79 », la légende p. 491 « Tableau 78 »), tableau 79 points de référence de C2 p. 497 ; fiche 7.2 éclairage des locaux communs, p. 503 (équation 791) ; fiche 8.5 programmation des relances, p. 556 à 559 (tableaux 91 à 93) ; fiche 9.6 besoins d'ECS, p. 1049 à 1056 (équations 1680 à 1691, tableau 277 p. 1053 à 1055) ; fiche 10.1 ascenseurs, p. 1300 à 1303 (tableau 310, tableau Uk) ; fiche 10.2 escalators, p. 1313 ; fiche 13.6 indicateurs par occupant, p. 1404 à 1406 (tableau 342, équations 2552 et 2553) ; chapitre 15, p. 1409 ; lectures de ihebergement p. 112 (équation 97), 256 et 462 ; fiche 9.5 émission d'ECS, tableau 275 p. 1047 ; Rat_douches_bains p. 1610 (équation 2982).
- Tableur officiel « Scénarios conventionnels » du 29/04/2026 (`corpus/site_2026-10-09/2026-04-29_scenarios_conventionnels.xlsx`, 28 feuilles), converti en `openbce/tables/scenarios_officiels.json` par `outils/scenarios_xlsx.py` ; les cellules vides signalées plus bas ont été vérifiées à la source avec openpyxl (feuilles HOT345_J, CRE, EHPAD, RES_2RJ-6J7).
- Fiches d'application : FA05 « Comment identifier l'usage d'un bâtiment et l'exigence associée » v2 du 01/10/2026, 12 pages ; FA09 « Exclusions d'application pour les bâtiments dits tertiaires spécifiques et industriels/artisanaux » v1 du 01/10/2026, 8 pages.
- Moteur : `openbce/scenarios.py`, `openbce/usages.py`, `openbce/api.py`, `openbce/calendrier.py`, `openbce/groupe.py`, `openbce/ecs.py`, `openbce/eclairage.py`, `openbce/ventilation.py`, `openbce/consommation.py`, `banc/besoins.py`, `banc/cep.py`, `outils/scenarios_xlsx.py`, `tests/test_scenarios.py`, `tests/test_calendrier.py`.

Convention de citation : « p. n » renvoie à la pagination de l'annexe III (n/1854) ; « FA05 p. n » et « FA09 p. n » aux fiches d'application ; « tableur » au fichier du 29/04/2026, feuille indiquée dans la table USAGES.

## 1. Ce que le texte définit, et à quel niveau

Le chapitre 2.1 (p. 17) pose le principe : les conditions d'occupation sont conventionnelles, décrites en scénarios horaires dont l'unité de base est la semaine, avec des modifications liées aux périodes de vacances ; certains scénarios sont définis au niveau de la zone, d'autres au niveau du local. La fiche 4.1 (p. 52) le reprend : « le scénario d'occupation à proprement parler se définit au niveau de la zone, indépendamment du bâtiment. La zone est divisée en locaux. Les apports internes sont définis au niveau des locaux. »

Au niveau de la zone (p. 18 et 19, p. 58) : présence, mobilité, consignes de chauffage et de refroidissement (trois jeux), ventilation, éclairage, clé horaire d'ECS. Au niveau du local (p. 20 à 22, p. 59) : ratio de surface, occupants par m², apports de chaleur et d'humidité des occupants, apports de chaleur et d'humidité des équipements.

Le chapitre 15 (p. 1409) ne contient plus les tableaux : « les scénarios conventionnels sont approuvés », avec en note le lien vers le tableur du 29/04/2026. Le tableur est donc la source numérique de référence ; la synthèse p. 24 à 26 et le tableau 277 p. 1053 à 1054 sont les seules valeurs chiffrées du texte, et servent ici de contrôle (section 8).

Le texte donne les équations pour tous les usages avec les mêmes formules : seules les valeurs changent. Le moteur traite donc les usages 4 à 28 par les fonctions existantes `scenarios.tertiaire` et `scenarios._locaux`, qui lisent le tableur ; ce qui manque est listé en section 10.

## 2. Calendrier conventionnel

- Pas de temps : 8 760 itérations d'une heure, comptées en temps UTC à partir de 0 (tableau des itérations, p. 56). Les scénarios sont écrits en heure légale ; la case horaire du scénario (1 à 24) est l'heure légale de début du pas plus 1. Passage à l'heure d'été à l'itération 1896, retour à l'heure d'hiver à l'itération 7032 (p. 56) ; l'heure légale vaut l'heure solaire plus 1 h en hiver, plus 2 h en été (p. 17). Codé : `calendrier.py` l. 14 à 46.
- Date des scénarios (p. 56) : mois m de 1 à 12, semaine du mois s de 1 à 4 ou 5 selon le mois (4 4 5 4 5 4 4 5 4 4 5 4 semaines, soit 52 semaines), jour de la semaine j de 1 à 7, heure h de 1 à 24 ; « on suppose que l'année commence un lundi ». Les 52 semaines font 364 jours ; le texte ne dit rien du 365e jour. `calendrier.py` l. 36 à 39 le traite comme un lundi de la semaine 1 du mois 1, déduit des RSEE d'habitation : à garder pour tous les usages, non validé au-delà des usages 1 à 3.
- Jours fériés : le texte n'en connaît aucun (le mot n'apparaît nulle part dans les 1 854 pages) ; aucun usage n'en a. Ne rien coder.
- Semaines de fermeture et semaines partielles : uniquement par le profil annuel (semaine du mois x mois, 5 x 12) de chaque tableau du tableur. Le texte les décrit en clair dans la synthèse p. 24 à 26 : « Inoccupé 1 semaine en décembre » (1, 2, 6, 14, 18, 25, 28), « Arrêt 1 semaine en décembre » (éclairage de 1, 2 et 14), « Inoccupé en vacances scolaires hors été, Juillet-août : occupé à 50 % » (4, 5), « Inoccupé en vacances scolaires » (26, 27), « 52s/an » (tous les autres), « 52s/an (dernière semaine de l'année occupée à 50 %) » (23, 24). La table ZONES de la section 7 donne, pour chaque usage, les semaines (m, s) fermées ou partielles de chaque profil, telles que le tableur les code ; les écarts entre profils d'un même usage sont en section 8.
- Vacances scolaires conventionnelles (semaines à 0 du profil annuel d'occupation de la zone, tableur) : usage 4, 9 semaines, m1s1 (fin de Noël), m2s1 et m2s2 (hiver), m4s2 et m4s3 (printemps), m10s4 et m11s1 (Toussaint), m12s3 et m12s4 (Noël) ; usage 5, 8 semaines, les mêmes sans m12s3 (qui reste à -1 dans les seules consignes, section 8.4) ; usages 26 et 27, 16 semaines, m1s1, m2s1, m2s2, m4s2, m4s3, m10s4, m12s4 et l'été m7s1 à m8s5 (feuilles RES_SCO_*), sans m11s1 ni m12s3. Ces semaines sont une convention du tableur, le texte ne les date pas.

## 3. Usages, indicateurs et découpage en zones

### 3.1 Liste des usages et indicateurs d'usage

Le tableau 4 (p. 57) donne les 28 usages avec deux indicateurs de sortie (nomenclature p. 54) : `ihebergement` (1 pour 1, 2, 8, 9, 19, 20 ; 0 sinon) et `ienseignement` (1 pour 4, 5, 7, 26, 27 ; 0 sinon). `ienseignement` commande l'arrêt de la génération d'ECS pendant les vacances (équation 47, p. 62) ; `ihebergement` (indicateur d'usage habitation ou hébergement, p. 54) est lu par la fiche des espaces tampons solarisés, ihebergement_et = MIN(ihebergement_gr) (équation 97, p. 112), et figure en entrée de zone p. 256 et p. 462 ; p. 1610 (Rat_douches_bains, équation 2982) nomme les usages (hôtels partie nuit, hébergement, établissements sportifs) sans lire l'indicateur. Table USAGES en section 7. FA05 p. 4 reprend la même liste avec les mêmes numéros.

### 3.2 Comment on constitue les zones

Annexe III 4.3.3 (p. 69) et FA05 p. 6 et 7 donnent la même démarche : 1) identifier les bâtiments, les bâtiments accolés formant un bâtiment unique (parois mitoyennes d'au moins 15 m² pour les maisons, 50 m² pour les autres) ; 2) écarter les parties hors RE2020 ; 3) choisir le ou les usages de la liste qui caractérisent au mieux la destination ; 4) identifier les types de locaux présents, « lorsqu'un local associé ne figure pas dans la liste, on utilise un local ayant le niveau d'apports internes le plus proche » (p. 69) ; 5) constituer les zones : tous les groupes ayant le même usage « et, pour certains usages, les groupes ayant le même fonctionnement (partie jour ou partie nuit, catégorie d'hôtel, ...). Les zones peuvent être constituées de locaux non contigus » (p. 69 ; FA05 p. 6 ajoute traversant ou non pour les logements collectifs) ; 6) séparer en groupes les parties climatisées ou non et les classes d'exposition au bruit (FA05 p. 6) ; 7) facultatif, redécouper selon les transferts thermiques (FA05 p. 7). L'usage est une donnée saisie (balise `Usage` de la zone du RSEE, lue par `banc/besoins.py` l. 35) : le moteur ne le déduit pas.

Partie de bâtiment de petite taille (arrêté du 4 août 2021 article 2, cité FA05 p. 3) : surface de référence inférieure à 150 m² et à 10 % de celle de l'usage principal, elle prend l'usage de la zone majoritaire, avec ses propres systèmes (FA05 p. 7 et 8) ; une maison individuelle ne peut jamais être assimilée (FA05 p. 3).

### 3.3 Hôtels : partie nuit, partie jour, catégorie

Quatre usages (tableau 4, p. 57) : 8 et 9 « partie nuit » (0 à 2 étoiles ; 3 à 5 étoiles), 10 et 11 « partie jour ». Le texte ne définit la partie nuit et la partie jour que par leurs locaux (synthèse p. 24) : partie nuit = circulation accueil 0,233, chambre sans cuisine avec salle de bain 0,728, sanitaires collectifs 0,007, local service 0,032 ; partie jour 0 à 2 étoiles = bureau standard 0,1161, circulation accueil 0,4308, sanitaires collectifs 0,0512, salle petits déjeuners 0,4019 ; partie jour 3 à 5 étoiles = bureau standard 0,105, circulation accueil 0,173, sanitaires collectifs 0,037, salle petits déjeuners 0,17, salle de séminaires réunion 0,4276, bar 0,0874. La partie nuit est occupée de 0 h à 9 h et de 18 h à 0 h, la partie jour de 6 h à 20 h, 7 jours sur 7, 52 semaines (p. 24). La répartition des surfaces entre les deux zones et la catégorie d'étoiles sont des données saisies ; le texte ne donne aucune règle de partage. Le système d'éclairage des chambres de la partie nuit est entièrement conventionnel (p. 18 ; fiche 7.1 p. 473). Rattachements (FA05 p. 9 et 10) : résidences étudiantes sans cuisine, établissements de placement éducatif la nuit, auberges de jeunesse (8 à 11), internats d'établissement d'enseignement (10, partie jour), salles communes d'hébergements hors logements collectifs (10, local « salle petits déjeuners »).

### 3.4 Établissements sanitaires et de santé

19 « établissements sanitaires avec hébergement » (EHPAD, FAM, MAS, foyers de vie, FA05 p. 11), 20 « établissements de santé (partie nuit) » (parties d'hôpitaux et cliniques à occupation continue 24 h/24 et 7 j/7, FA05 p. 11), 21 « établissements de santé (partie jour) » (occupation diurne, cabinets médicaux, cliniques vétérinaires, accueil de jour sans hébergement, FA05 p. 11). Structures d'éducation adaptée (IME, ITEP) : 21 sans hébergement, 20 et 21 avec hébergement (FA05 p. 11). Coquille de FA05 p. 11 : son tableau numérote 22 la ligne « Établissement de santé (partie nuit) » (parties d'hôpitaux et cliniques à occupation continue), alors que le tableau 4 (p. 57) donne 20, que 22 est l'usage des aérogares et que la même page écrit « 20 et 21 » pour les structures avec hébergement ; lire 20. Les locaux des deux parties sont listés p. 25 (voir LOCAUX) ; l'affectation des surfaces à la partie nuit ou à la partie jour est saisie, comme pour les hôtels. Les plateaux techniques hospitaliers sont des locaux de process, hors RE2020 (FA09 p. 7).

### 3.5 Restaurants : quatre variantes, plus deux scolaires

Les usages 13 à 16 ne diffèrent que par le rythme de service inscrit dans leur nom (tableau 4, p. 57) : 13 en continu 18 heures par jour, 7 jours sur 7 (occupation 6 h à 0 h) ; 14 un repas par jour, 5 jours sur 7 (9 h à 15 h, inoccupé une semaine en décembre) ; 15 deux repas par jour, 7 jours sur 7 (10 h à 15 h et 17 h à 23 h) ; 16 deux repas par jour, 6 jours sur 7 (idem, lundi à samedi). Les trois locaux sont les mêmes (salle restaurant 0,7, cuisine 0,2, local service 0,1 ; p. 25). Les restaurants scolaires 26 (un repas, 5 jours sur 7, 9 h à 15 h) et 27 (trois repas, 5 jours sur 7, 6 h à 15 h et 16 h à 20 h) sont « affiliés à l'enseignement » (ienseignement = 1, p. 57) et fermés en vacances scolaires (p. 26). Le texte ne donne aucune règle de choix entre les variantes autre que ce rythme : l'usage est saisi. FA05 p. 10 : une salle de restauration sans cuisine est le local « salle de restauration » d'un des usages 13 à 16, 26 ou 27 ; un restaurant sans salle (dark kitchen) prend l'usage 13, 15 ou 16. FA09 p. 6 : les cuisines centrales sont des locaux de process hors RE2020 ; dans une cuisine professionnelle, les hottes de cuisson sont des équipements de process à écarter, le local « cuisine » restant soumis.

### 3.6 Autres rattachements utiles

Vestiaires : les vestiaires des établissements sportifs sont compris dans les scénarios des usages 25 et 28, il ne faut pas créer de zone « vestiaires seuls » pour eux (FA05 p. 4) ; vestiaires de stade et vestiaires d'un bâtiment industriel dont l'aire de production est hors périmètre : usage 18 (FA05 p. 11). Industrie et artisanat (23 en 3x8, 24 de 8 h à 18 h) : seuls les locaux chauffés ou refroidis pour le confort des occupants sont dans le calcul, les locaux et équipements de process sont exclus (FA09 p. 5 et 6 ; FA05 p. 11 pour centres techniques et entrepôts). Tableau complet des destinations rattachées : FA05 p. 9 à 11 (maisons témoins et gîtes 1, logements de fonction 2, mairies et banques 3, écoles maternelles et centres de loisirs 4, CFA 5, ludothèques et bibliothèques universitaires indépendantes 6, conservatoires et écoles d'ingénieurs 7, concessions, bars, casinos et aires de service 17, centres de fitness 28). Hors champ (FA05 p. 5) : lieux de culte, salles de spectacle, musées, piscines, patinoires, établissements pénitentiaires, salles polyvalentes, datacenters. Les tribunaux restent en RT 2012 (FA05 p. 5).

## 4. Profils de zone

### 4.1 Algèbre des profils (p. 58, tableaux 5 et 6)

Chaque grandeur de zone p(m, s, j, h) est le produit d'un profil hebdomadaire p^s(j, h) (7 jours x 24 cases) et d'un profil annuel p^a(m, s) (semaine du mois x mois). Deux algèbres : pour le chauffage et le refroidissement, le tableau 5 (p. 58) combine les états -1, 0, 1 en gardant le plus petit (-1 l'emporte, puis 0) ; pour les autres grandeurs, le tableau 6 (p. 58) est le ET logique, c'est-à-dire le produit. `scenarios.py` l. 88 et 89 code le tableau 5 par `np.minimum`, l. 83 à 85 et 128 à 130 le tableau 6 par le produit : c'est juste pour des valeurs entières. Le tableur contient des valeurs fractionnaires dans les profils de zone (0,5 pour la ventilation et l'éclairage de 17 de 6 h à 7 h, 0,35 pour l'éclairage de 20 hors plage, 0,5 pour toutes les grandeurs de 23 et 24 la dernière semaine) que le texte ne prévoit pas : section 9.

### 4.2 Consignes de température et arrêts de moins ou de plus de 48 h

Trois jeux par zone (nomenclature p. 52 et 53) : θ+ en occupation normale (confort), θ0 en réduit de moins de 48 h, θ- en réduit de plus de 48 h, pour le chauffage et pour le refroidissement. L'équation 30 (p. 59) choisit la consigne selon l'état p = p^a ⊗ p^s : -1 donne θ-, 0 donne θ0, 1 donne θ+. Valeurs par usage dans ZONES (`consigne_ch`, `consigne_fr`), toutes confirmées par la synthèse p. 24 à 26 : 19/16/16 et 26/30/30 pour 1, 2 et 22 ; 19/16/7 et 26/30/30 pour 3 à 11, 13 à 18, 26 et 27 ; 21/18/7 pour 12, 19, 20 et 21 ; 15/7/7 pour 23, 24, 25 et 28. Le refroidissement vaut 26/30/30 pour les 28 usages.

L'indicateur de consigne de chauffage p^s_ch(j, h) est un entier -1, 0 ou 1 (p. 53). Le tableur porte la règle des 48 h dans le profil hebdomadaire : pour les usages fermés le week-end dont l'absence dépasse 48 h (3, 4, 12, 14, 24, 26, 27), le lundi de 0 h à l'ouverture, le vendredi après la fermeture et tout le week-end valent -1, les nuits de semaine 0 ; pour les usages dont la fermeture hebdomadaire est plus courte que 48 h (5 et 6 samedi midi à lundi matin, 7, 15, 16, 17, 21 ; 18, 25, 28 dimanche soir à lundi matin), toutes les périodes d'inoccupation valent 0 et -1 ne vient que du profil annuel (semaines fermées) ; pour les usages occupés en continu (19, 20, 23) l'état est 1 en permanence ; pour les hôtels et les usages 13 et 22 l'inoccupation quotidienne vaut 0. Les durées ont été vérifiées sur les horaires du tableur : aucun usage ne contredit le seuil de 48 h. Le profil annuel de chauffage vaut -1 sur les semaines fermées (vacances, semaine de décembre), ce qui donne θ- (7 °C en tertiaire, 16 °C en habitation et pour 22) pendant ces semaines.

La fiche 8.5 (p. 556 à 559) consomme ces états : la relance anticipe le retour à θ+ de 2 h ou 6 h en chauffage à horloge fixe selon que l'inoccupation est courte (pch = 0) ou prolongée (pch = -1), 2 h ou 4 h avec contrôle d'ambiance, 1 h ou 0 à 3 h linéaire en θext avec optimiseur (tableau 92, p. 559) ; 1 h ou 3 h, 1 h ou 2 h, 0 h en refroidissement (tableau 93, p. 559) ; elle lit pch(t) et pfr(t) de h à h+6 (tableau 91, p. 557). L'équation 55 (p. 63) expose pch_s(h) et pfr_s(h). Le moteur porte déjà `etat_ch` et `etat_fr` dans `Scenario` (`scenarios.py` l. 71 et 72) ; rien à changer pour 4 à 28.

### 4.3 Ventilation : sens de l'indicateur

Ivent(m, s, j, h) = p^a_vent x p^s_vent (équation 45, p. 61), « indicateur d'utilisation de la ventilation en occupation ou inoccupation » (p. 53). Le chapitre 2.1 (p. 18) le décrit comme proche du scénario de présence « mais qui permet une remise en route de la ventilation avant l'occupation, conformément aux réglementations en vigueur pour les usages autres que d'habitation » : dans le tableur, la ventilation précède l'occupation d'une heure pour 12, 13, 14, 15, 16, 17, 22 et 27 (synthèse p. 25 et 26, colonne « Horaire ventilation zone », « Idem éclairage »), est égale à l'occupation pour 3 à 11, 19, 20, 21, 23 à 26 et 28 (« Idem occupation »), et vaut 1 en permanence pour 1 et 2 (p. 24 : 24h/24, 7j/7, 52s/an) ; pour 18 le texte dit aussi « Idem occupation » (p. 25) mais le tableur (feuille VES) prolonge la ventilation d'une heure, 8 h à 22 h et dimanche 8 h à 19 h, pour une occupation 8 h à 21 h et dimanche 8 h à 18 h (section 8.4), et le moteur lit le tableur. Sens dans les fiches qui le lisent : fiche 6.2 (p. 336), Ivent vrai donne les débits régulés au débit maximal (équations 400 et 401, avec Crdbnr), Ivent faux donne les débits minimaux (402) ; pour 1 et 2, Crdbnr = 1 quelle que soit l'occupation ; fiche 6.3 CTA (p. 355 et 356), « occupation au sens de la ventilation (ivent(h) = 1) » commande le débit de zone neutre en occupation ; fiche 6.5 (p. 407), Ivent vrai donne la puissance de ventilateur en occupation (636, 638), faux celle d'inoccupation (637, 639). Donc 1 = débit et puissance d'occupation, 0 = débit et puissance d'inoccupation ; c'est ce que codent `groupe.py` l. 223 et `ventilation.py` l. 83, qui testent `> 0`.

### 4.4 Éclairage

Iecl(m, s, j, h) = p^a_light x p^s_light (équation 54, p. 63). Le scénario d'éclairage est « basé sur les scénarios de présence en prenant en compte les périodes de sommeil » (p. 18) ; il n'autorise l'éclairage que si l'éclairement naturel est insuffisant, la consommation n'est pas systématique (p. 18 et 19). Pour les chambres des usages 5 (partie nuit), 19 et hôtels partie nuit, le système d'éclairage est entièrement conventionnel (p. 18 ; fiche 7.1 p. 473). Profils dans ZONES ; particularité de l'usage 20 : « Lun-Dim 5h-21h (réduit sinon) » (p. 25), codé 0,35 hors plage dans le tableur.

### 4.5 Mobilité

Uk(m, s, j, h) = p^a_mob x p^s_mob (équation 31, p. 60), « indice de mobilité nécessaire aux calculs liés aux ascenseurs, aux escalators et également utilisé pour l'éclairage des locaux communs » (p. 58). Fiche 10.1 (p. 1303) : « Tableau Uk de mobilité des cabines par type de zone k : le tableau est obtenu via les éléments fournis dans la fiche dédiée aux scénarios conventionnels » ; fiche 10.2 (p. 1313), même renvoi pour les escalators ; tableau 310 (p. 1300 et 1301) donne le besoin de voyages Bv par an et par personne selon l'usage de la zone (par exemple 2920 pour 8 à 11 et 21, 4380 pour 20, 7665 pour 22, 402 pour 18 et 26). Fiche 7.2 (p. 503) : l'éclairage des locaux communs des logements collectifs suit la mobilité des ascenseurs, à 2,19 W/m² SREF (équation 791). La mobilité n'entre pas dans le bilan thermique du groupe ; elle n'est pas lue aujourd'hui par `ascenseurs.py` ni `bilans.py`. Valeurs dans ZONES (`mobilite`) ; l'usage 18 n'a aucune mobilité (profil nul).

### 4.6 ECS, vacances, occupation de la zone, protections mobiles

- Clé horaire d'ECS ah(m, s, j, h) = p^a_ECS x p^s_ECS (équation 46, p. 62), définie au niveau de la zone et commune à tous les émetteurs de la zone (p. 1049) ; tableau « ECS facteur correctif de la semaine » du tableur ; `ecs.cle_horaire` l. 61 à 71 la lit déjà pour tout usage.
- Besoin hebdomadaire (fiche 9.6, p. 1053 à 1056) : Vuw = a x ah x Nu (1681), Qw = ρw cw Vuw (θuw - θcw) (1680), θuw = 40 °C (p. 1052). Pour les usages 3 à 28, a est « figé dans les scénarios conventionnels » et Nu est le nombre d'unités caractéristiques, un paramètre d'intégration de l'émetteur ECS, en m² de surface utile pour les 26 usages (tableau 277, p. 1053 et 1054 ; p. 1055). Valeurs de a dans ZONES (`ecs_a`) ; pour 1 et 2, a = min(392 ; 40 x A / Nadeq) litres par semaine et par adulte équivalent (1686, 1690, p. 1056). Le tableur et le tableau 277 concordent pour 25 usages sur 26 ; écart sur l'usage 16, section 8.
- Génération d'ECS en vacances (équation 47, p. 62) : si ienseignement = 1 et Ivac = 0 alors iecs(j) = 0, sinon 1 ; Ivac(m, s, j, h) = p^a_occ(m, s) (équation 48). Concerne 4, 5, 7, 26, 27 ; pour 7 le profil annuel d'occupation vaut 1 toute l'année, donc iecs = 1 toujours.
- Iocc_zone = p^a_occ x p^s_occ (équation 49, p. 62) : c'est `Scenario.occupation`.
- Iocc_gpm (équations 50 à 53, p. 62) : -1 en inoccupation de nuit ou de vacances, 0 en inoccupation de jour (les creux d'inoccupation compris entre 7 h et 22 h, encadrés d'heures occupées), 1 en occupation ; combiné par le tableau 5. Sert à la gestion des protections mobiles (fiche 5.9). Non produit aujourd'hui (`groupe.py` l. 180 ne distingue que occupé ou non).

## 5. Locaux : occupants et apports

### 5.1 Surfaces et ratio des locaux

Rat_gr = A_gr / A_z (27), A_z = Σ A_gr (28), A_l = A_z x Rat_loc^l (29) (p. 58). Rat_loc^l est un paramètre intrinsèque entre 0 et 1 sans valeur conventionnelle (tableau 3, p. 52) ; la synthèse p. 24 l'appelle « Ratio par défaut surface utile du local / surface utile du groupe », la fiche 4.3 (p. 69) « Ratio de surface utile du local sur la surface utile du groupe (%) (Ratel) », avec la consigne d'identifier les types de locaux présents et de prendre, pour un local absent de la liste, celui dont les apports sont les plus proches. Lecture : les ratios sont saisis par groupe, les valeurs du tableur sont les valeurs par défaut. Le moteur (`scenarios._locaux` l. 101 à 123, `tertiaire` l. 138 à 146) n'utilise que les défauts, le RSEE n'ayant pas pu être lu pour cette spécification ; `eclairage.py` l. 82 à 95 et 121 à 130 lit déjà `Rat_local` et un type de local (`Locaux_Bureau`) sur les entrées `Eclairage` du groupe, pour les bureaux seulement. Les types de locaux de l'éclairage (liste p. 474 et 475 ; tableau 78 des valeurs de C1 et de l'éclairement de référence, p. 488 à 491) portent les mêmes noms que ceux des scénarios (bureau standard, salle de classe, chambre sans cuisine avec salle de bains, aire de production, salle de sport, ...) : un même jeu de ratios saisis devrait servir aux deux, à confirmer sur un RSEE.

La somme des ratios vaut 1 pour 27 usages et 0,999 pour l'usage 22, dans le texte (p. 25) comme dans le tableur.

### 5.2 Nombre d'occupants

Usages 1 et 2 (p. 60) : Nmax selon la surface moyenne du logement (équations 32 et 35), Nadeq = Nblgt x (Nmax si Nmax < 1,75, sinon 1,75 + 0,3 (Nmax - 1,75)) (32, 36), Ahab = Rat_hab x A_z (33), Algt = Ahab / Nblgt (34), N_occ_hab = Nadeq x (p^a_occ x p^s_occ) x (t^a_occ x t^s_occ) (37), nul pour le local de circulation. Codé : `calendrier.adultes_equivalents` l. 49 à 61, `scenarios.habitation` l. 80 à 98, `RATIO_HABITATION` l. 25 (0,9 et 0,1 en collectif, synthèse p. 24).

Usages 3 à 28 (équation 38, p. 61) : N_occ^l(m, s, j, h) = A_l x N_occ_nom^l x (p^a_occ x p^s_occ) x (t^a_occ x t^s_occ), avec N_occ_nom^l l'« occupation surfacique maximale » (tableau 3, p. 52), c'est-à-dire la colonne « Nombre occupants nominal /m² utile par local » de la synthèse p. 24 à 26 et la ligne « occupant x Noccnom » de chaque local du tableur, et t_occ le « facteur correctif du taux d'occupation du local » (p. 53), réel de 0 à 1, tableau « occupant » du local (hebdomadaire et annuel). Le produit avec p_occ fait que les locaux n'ont jamais d'occupant quand la zone est inoccupée, quel que soit leur propre profil. Codé : `scenarios.tertiaire` l. 139 à 143.

### 5.3 Chaleur et humidité des occupants

Équation 39 (p. 61) : φ_int_occ,conv^g = Rat_gr^g x α_conv x Σ_l N_occ^l x Q_max_occ^l, et la part radiative avec (1 - α_conv) ; α_conv = 0,5 (p. 53, `ALPHA_CONV` l. 26, `groupe.py` l. 139 et 140). Équation 40 : ω_int_occ^g = Rat_gr^g x Σ_l N_occ^l x ω_max_occ^l. Q_max_occ^l est l'« apport maximal de chaleur interne dû aux occupants, par occupant, du local l », en W/occ (tableau 3, p. 52) ; ω_max_occ^l en kg/h/occ. Le texte chiffre un adulte à 90 W au repos et 63 W en sommeil (p. 20), 0,055 kg/h au repos et 0,0385 kg/h en sommeil (p. 21), et renvoie pour les autres usages au taux d'occupation conventionnel « ce qui permet d'en déduire directement les niveaux d'apports » (p. 20 et 21), sans autre chiffre.

Tableur, par local : Q_max_occ = 90 W pour 1 et 2 (W/Nadeq), 3 à 11, 18, 19, 25 et 28 (sauf la salle de sport), 26 ; 105 W pour 12 à 17, 20 à 24 et 27 ; 300 W pour la salle de sport de 25 et 28. ω_max_occ = 0,055 kg/h partout. Le sommeil est porté par le profil t_occ (0,7 de 22 h à 6 h en habitation, 0,7 de 0 h à 6 h et 23 h à 24 h dans les chambres d'hôtel, 0,7 de 21 h à 5 h dans les chambres de 19), ce qui redonne 63 W et 0,0385 kg/h. Les valeurs 105 W et 300 W n'apparaissent nulle part dans le texte : elles sont « tableur seul », approuvées par le chapitre 15 (p. 1409) et non validées.

Unités du tableur : « W/Nadeq » (usages 1 et 2) et « W/Noccnom » (4 à 28) ; « W/Nocc » sur la feuille des bureaux (usage 3, feuille datant de l'arrêté de 2022), sur le seul bureau standard de la feuille 22 (circulation accueil et sanitaires vestiaires y sont en W/Noccnom) et sur les locaux bureau standard, circulation accueil et sanitaires vestiaires des feuilles 23 et 24, copiés de la feuille des bureaux. Dans l'équation 39 la chaleur est multipliée par N_occ^l(m, s, j, h), le nombre d'occupants présents calculé par (38) : W/Nocc et W/Noccnom désignent la même grandeur, des watts par occupant présent ; « Noccnom » ne fait que rappeler que ce nombre dérive de la densité nominale. Aucun effet numérique ; `scenarios._locaux` l. 115 lit déjà les trois libellés de la même façon.

### 5.4 Apports de chaleur et d'humidité hors occupants (« par unité »)

Équation 41 (p. 61) : φ_int,conv^l = A_l x α_conv x Q_max_proc^l x (t^a_ch x t^s_ch), part radiative avec (1 - α_conv) ; équation 42 : somme sur les locaux pondérée par Rat_gr^g. Équations 43 et 44 : idem pour l'humidité avec ω_max_proc^l et t_ω. Q_max_proc^l est l'« apport maximal de chaleur interne du local l » en W/m² et ω_max_proc^l en kg/h/m² (tableau 3, p. 52) ; A_l est en m² de surface utile (29). L'unité du tableur « Watts/unité » et « kg/h/unité » est donc le mètre carré de surface utile du local, comme la colonne « W/m² utile » de la synthèse p. 24 et le tableau 277 pour l'ECS (« m² de surface utile »). t_ch est le « ratio d'apports internes de chaleur du local », réel de 0 à 1 (p. 53), tableau « Apports de chaleur hors occupants et éclairage » du local.

La synthèse p. 24 à 26 donne deux colonnes, « en période d'occupation » et « hors période d'occupation » : la seconde est Q_max_proc x la valeur de t_ch hors occupation, soit 1/9 (0,11111) pour les bureaux standard, centres de documentation et salles informatiques (16 x 0,11111 = 1,77776 ; 5 x 0,11111 = 0,55555 ; 25,795 x 0,1111 = 2,8658), 0,2 en habitation (5,7 x 0,2 = 1,14 ; le texte p. 21 dit 5,7 W/m² en occupation et 1,1 W/m² en sommeil et inoccupation), 0,15 et 0,34 dans les chambres d'hôtel (4 x 0,15 = 0,6 ; 4,625 x 0,34 = 1,5725), 0,1 dans les salles de petits déjeuners (88,8 x 0,1 = 8,88 ; 44,3 x 0,1 = 4,43), 0,12 au bar (34,4 x 0,12 = 4,128), 1 dans les aires de production occupées en continu (20 : 5 et 5 ; 23 : 2 et 2). Le moteur n'a besoin que de Q_max_proc et du profil (`scenarios.tertiaire` l. 145 et 146) ; cette colonne sert de contrôle (section 8).

Apports à 0 W : le tableur donne Q_max_proc = 0 pour tous les locaux des restaurants 13 à 16, des vestiaires 18, des établissements sportifs 25 et 28 et des restaurants scolaires 26 et 27. Le texte le confirme, colonne par colonne, p. 25 et 26 (salle restaurant, cuisine, local service : 0 et 0 ; douches collectives, sanitaires vestiaires, circulation accueil : 0 et 0 ; salle de sport, local service : 0 et 0). C'est cohérent avec FA09 p. 6 : les postes de cuisson professionnels sont des équipements de process écartés du calcul. Les apports de ces usages se réduisent donc à la chaleur des occupants (105 W dans les salles de restaurant à 0,59 ou 0,77 occupant par m², 300 W dans les salles de sport à 0,1 occupant par m²).

Humidité hors occupants : le chapitre 2.1 (p. 22) dit que les bâtiments d'habitation ont des apports d'humidité nuls et que, pour les autres usages, ils « sont dépendants du type de bâtiments et des périodes d'occupation/inoccupation » ; mais le tableur donne 0 kg/h/unité à tous les locaux de tous les usages (une cellule vide, salle commune de l'usage 19). Valeur à coder : 0 ; le texte ne donne aucune valeur non nulle (non spécifié).

### 5.5 Apports des équipements de l'habitation, pour mémoire

5,7 W/m² en occupation, 1,1 W/m² en sommeil et inoccupation (p. 21 ; tableau p. 22 : 26,3 kWh/(m².an) dont froid 8,0, audiovisuel 6,8, informatique 5,0, cuisson 3,7, appareils ménagers 2,2, lavage 0,6). Déjà codé et validé.

## 6. Nocc du récapitulatif contre Noccnom conventionnel

La fiche 13.6 (p. 1404 à 1406) introduit Nocc_zn, « nombre total d'occupants de la zone », saisi dans une balise de la zone pour le seul indicateur pédagogique Cep_annuel_par_occ = Cep_annuel x SREF / Nocc_bat (équations 2552 et 2553, p. 1405 et 1406). En résidentiel il vaut le nombre de pièces principales du logement (tableau 342, p. 1405) ; en tertiaire « les valeurs d'occupation issues des scénarios conventionnels peuvent être utilisées » ; en enseignement, le nombre d'élèves prévu à la programmation (p. 1405). Ce Nocc saisi n'entre dans aucun calcul thermique : les occupants du bilan sont toujours N_occ^l(m, s, j, h) de l'équation 38, à partir de N_occ_nom^l du tableur. Le moteur n'écrit pas cet indicateur (`sortie_rsee.py` ne porte pas de balise Nocc) ; le nom de la balise RSEE n'a pas pu être vérifié (lecture des RSEE interdite pour cette spécification) : point ouvert, hors du thème.

## 7. Tables des 28 usages

Les trois dicts suivants sont générés depuis `openbce/tables/scenarios_officiels.json` (tableur du 29/04/2026) par un script de contrôle, sans retouche manuelle (une exception : la colonne « hors occupation » des chambres des usages 8 et 9 porte la valeur de nuit du texte, voir l'en-tête de LOCAUX), et annotés avec les pages du texte. Ils sont la référence de relecture ; le moteur continue de lire le JSON. Clé = numéro d'usage. « None » ou « vide » = non spécifié par la source indiquée ; rien n'a été complété par vraisemblance.

```python
# Tableau 4 (p. 57) : numéro d'usage -> (nom, feuille du tableur du 29/04/2026, ihebergement, ienseignement)
USAGES = {
    1: ('Maisons individuelles ou accolées', 'MI', 1, 0),
    2: ('Logements collectifs', 'LC', 1, 0),
    3: ('Bureaux', 'BUR', 0, 0),
    4: ('Enseignement primaire', 'ENS_PRI', 0, 1),
    5: ('Enseignement secondaire', 'ENS_SEC', 0, 1),
    6: ('Médiathèques et bibliothèques', 'MED', 0, 0),
    7: ("Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques", 'ENS_SUP', 0, 1),
    8: ('Hôtels 0, 1 et 2 étoiles (partie nuit)', 'HOT012_N', 1, 0),
    9: ('Hôtels 3, 4 et 5 étoiles (partie nuit)', 'HOT345_N', 1, 0),
    10: ('Hôtels 0, 1 et 2 étoiles (partie jour)', 'HOT012_J', 0, 0),
    11: ('Hôtels 3, 4 et 5 étoiles (partie jour)', 'HOT345_J', 0, 0),
    12: ("Établissements d'accueil de la petite enfance", 'CRE', 0, 0),
    13: ('Restaurants - en continu, 18 heures par jour, 7 jours sur 7', 'RES_CON', 0, 0),
    14: ('Restaurants - 1 repas par jour, 5 jours sur 7', 'RES_1RJ-5J7', 0, 0),
    15: ('Restaurants - 2 repas par jour, 7 jours sur 7', 'RES_2RJ-7J7', 0, 0),
    16: ('Restaurants - 2 repas par jour, 6 jours sur 7', 'RES_2RJ-6J7', 0, 0),
    17: ('Commerces', 'COM', 0, 0),
    18: ('Vestiaires seuls', 'VES', 0, 0),
    19: ('Établissements sanitaires avec hébergement', 'EHPAD', 1, 0),
    20: ('Établissements de santé (partie nuit)', 'SAN_N', 1, 0),
    21: ('Établissements de santé (partie jour)', 'SAN_J', 0, 0),
    22: ('Aérogares', 'AER', 0, 0),
    23: ('Industries ou artisanats 3x8h', 'IND_3x8', 0, 0),
    24: ('Industries ou artisanats 8h à 18h', 'IND_8_18h', 0, 0),
    25: ('Établissements sportifs municipaux ou scolaires', 'GYM_MUN', 0, 0),
    26: ('Restaurants scolaires - 1 repas par jour, 5 jours sur 7', 'RES_SCO_1RJ_5J7', 0, 1),
    27: ('Restaurants scolaires - 3 repas par jour, 5 jours sur 7', 'RES_SCO_3RJ_5J7', 0, 1),
    28: ('Établissements sportifs privés', 'GYM_PRI', 0, 0),
}
```

```python
# Scénarios de zone. Horaires en heure légale : "8-18h" = cases 9 à 18, zone occupée de 8 h à 18 h ; "x0,5" = valeur du profil.
# Chauffage et refroidissement : états horaires 1 confort, 0 arrêt de moins de 48 h, -1 arrêt de plus de 48 h (p. 53, équation 30 p. 59) ;
# l'état combiné au profil annuel suit le tableau 5 (p. 58), soit min(hebdo, annuel).
# 'semaines_fermees' : (mois m, semaine s) où le profil annuel d'occupation vaut 0 ; 'semaines_partielles_*' : valeur du profil annuel.
# 'ecs_a' : besoin unitaire hebdomadaire, litres d'eau à 40 °C par semaine et par m² de surface utile (tableau 277, p. 1053-1054).
# Sources : tableur 29/04/2026 (feuille indiquée dans USAGES) ; synthèse de l'annexe III p. 24-26 ; chapitre 15 p. 1409.
ZONES = {
    1: {  # Maisons individuelles ou accolées
        'consigne_ch': (19, 16, 16), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': None,  # habitation : a = min(392 ; 40 x A / Nadeq) litres par semaine et par adulte équivalent (1686, 1690, p. 1056)
        'occupation': 'Lu/Ma/Je/Ve: 0-9h 17-24h | Me: 0-9h 13-24h | Sa/Di: 0-24h',
        'chauffage': 'Lu/Ma/Je/Ve: 0-9h=1 9-17h=0 17-24h=1 | Me: 0-9h=1 9-13h=0 13-24h=1 | Sa/Di: 0-24h=1',
        'refroidissement': 'Lu/Ma/Je/Ve: 0-9h=1 9-17h=0 17-24h=1 | Me: 0-9h=1 9-13h=0 13-24h=1 | Sa/Di: 0-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'eclairage': 'Lu/Ma/Je/Ve: 6-9h 17-22h | Me: 6-9h 13-22h | Sa/Di: 6-22h',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 7-8hx0.3 8-9hx0.1 9-11hx0.05 11-12hx0.1 12-13hx0.15 13-16hx0.05 16-17hx0.1 17-18hx0.2 18-19hx0.1 19-22hx0.05 | Sa/Di: 7-9hx0.2 9-12hx0.1 12-13hx0.15 13-16hx0.05 16-20hx0.1 20-22hx0.05',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 7-8hx0.028 8-9hx0.029 17-18hx0.00716667 18-21hx0.0215 21-22hx0.014 | Sa/Di: 7-8hx0.028 8-9hx0.029 17-19hx0.0114667 19-20hx0.0286667 20-21hx0.022 21-22hx0.0114667',
        'semaines_fermees': ['m12s4'],
        'semaines_fermees_ventilation': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': (['m12s4'], ['m1s1=1.05', 'm2s1=1.05', 'm3s1=1.05', 'm5s1=0.95', 'm6s1=0.95', 'm7s1=0.95', 'm8s1=0.95', 'm9s1=0.95', 'm10s1=1.05', 'm11s1=1.05', 'm12s1=1.05', 'm1s2=1.05', 'm2s2=1.05', 'm3s2=1.05', 'm4s2=0.95', 'm5s2=0.95', 'm6s2=0.95', 'm7s2=0.95', 'm8s2=0.95', 'm9s2=0.95', 'm10s2=1.05', 'm11s2=1.05', 'm12s2=1.05', 'm1s3=1.05', 'm2s3=1.05', 'm3s3=1.05', 'm4s3=0.95', 'm5s3=0.95', 'm6s3=0.95', 'm7s3=0.95', 'm8s3=0.95', 'm9s3=0.95', 'm10s3=1.05', 'm11s3=1.05', 'm12s3=1.05', 'm1s4=1.05', 'm2s4=1.05', 'm3s4=1.05', 'm4s4=0.95', 'm5s4=0.95', 'm6s4=0.95', 'm7s4=0.95', 'm8s4=0.95', 'm9s4=0.95', 'm10s4=1.05', 'm11s4=1.05', 'm3s5=1.05', 'm5s5=0.95', 'm8s5=0.95', 'm11s5=1.05']),
    },
    2: {  # Logements collectifs
        'consigne_ch': (19, 16, 16), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': None,  # habitation : a = min(392 ; 40 x A / Nadeq) litres par semaine et par adulte équivalent (1686, 1690, p. 1056)
        'occupation': 'Lu/Ma/Je/Ve: 0-9h 17-24h | Me: 0-9h 13-24h | Sa/Di: 0-24h',
        'chauffage': 'Lu/Ma/Je/Ve: 0-9h=1 9-17h=0 17-24h=1 | Me: 0-9h=1 9-13h=0 13-24h=1 | Sa/Di: 0-24h=1',
        'refroidissement': 'Lu/Ma/Je/Ve: 0-9h=1 9-17h=0 17-24h=1 | Me: 0-9h=1 9-13h=0 13-24h=1 | Sa/Di: 0-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'eclairage': 'Lu/Ma/Je/Ve: 6-9h 17-22h | Me: 6-9h 13-22h | Sa/Di: 6-22h',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 7-8hx0.3 8-9hx0.1 9-11hx0.05 11-12hx0.1 12-13hx0.15 13-16hx0.05 16-17hx0.1 17-18hx0.2 18-19hx0.1 19-22hx0.05 | Sa/Di: 7-9hx0.2 9-12hx0.1 12-13hx0.15 13-16hx0.05 16-20hx0.1 20-22hx0.05',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 7-8hx0.028 8-9hx0.029 17-18hx0.00716667 18-21hx0.0215 21-23hx0.00716667 | Sa/Di: 7-8hx0.028 8-9hx0.029 17-19hx0.0114667 19-20hx0.0286667 20-23hx0.0114667',
        'semaines_fermees': ['m12s4'],
        'semaines_fermees_ventilation': [],
        'semaines_mobilite': (['m12s4'], []),
        'semaines_ecs': (['m12s4'], ['m1s1=1.05', 'm2s1=1.05', 'm3s1=1.05', 'm4s1=1.05', 'm5s1=0.95', 'm6s1=0.95', 'm7s1=0.95', 'm8s1=0.95', 'm9s1=0.95', 'm10s1=1.05', 'm11s1=1.05', 'm12s1=1.05', 'm1s2=1.05', 'm2s2=1.05', 'm3s2=1.05', 'm4s2=0.95', 'm5s2=0.95', 'm6s2=0.95', 'm7s2=0.95', 'm8s2=0.95', 'm9s2=0.95', 'm10s2=1.05', 'm11s2=1.05', 'm12s2=1.05', 'm1s3=1.05', 'm2s3=1.05', 'm3s3=1.05', 'm4s3=0.95', 'm5s3=0.95', 'm6s3=0.95', 'm7s3=0.95', 'm8s3=0.95', 'm9s3=0.95', 'm10s3=1.05', 'm11s3=1.05', 'm12s3=1.05', 'm1s4=1.05', 'm2s4=1.05', 'm3s4=1.05', 'm4s4=0.95', 'm5s4=0.95', 'm6s4=0.95', 'm7s4=0.95', 'm8s4=0.95', 'm9s4=0.95', 'm10s4=1.05', 'm11s4=1.05', 'm3s5=1.05', 'm5s5=0.95', 'm8s5=0.95', 'm11s5=1.05']),
    },
    3: {  # Bureaux
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 1.25,
        'occupation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'chauffage': 'Lu: 0-8h=-1 8-18h=1 18-24h=0 | Ma/Me/Je: 0-8h=0 8-18h=1 18-24h=0 | Ve: 0-8h=0 8-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-8h=-1 8-18h=1 18-24h=0 | Ma/Me/Je: 0-8h=0 8-18h=1 18-24h=0 | Ve: 0-8h=0 8-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 7-8hx0.2 8-9hx0.5 9-10hx0.4 10-12hx0.2 12-13hx0.5 13-14hx0.4 14-17hx0.2 17-18hx0.3 18-19hx0.1 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 8-9hx0.012 9-12hx0.0253333 12-14hx0.012 14-17hx0.0253333 17-18hx0.012 | Sa/Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
        'semaines_ecs': ([], ['m7s1=0.5', 'm8s1=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
    },
    4: {  # Enseignement primaire
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.2,
        'occupation': 'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
        'chauffage': 'Lu: 0-8h=-1 8-17h=1 17-24h=0 | Ma/Me/Je: 0-8h=0 8-17h=1 17-24h=0 | Ve: 0-8h=0 8-16h=1 16-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-8h=-1 8-17h=1 17-24h=0 | Ma/Me/Je: 0-8h=0 8-17h=1 17-24h=0 | Ve: 0-8h=0 8-17h=1 17-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 8-9hx0.3 12-13hx0.05 16-17hx0.3 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Je/Ve: 8-9hx0.0138889 9-15hx0.031746 15-16hx0.031746 16-17hx0.0138889 | Me/Sa/Di: 0',
        'semaines_fermees': ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm12s3', 'm10s4', 'm12s4'],
        'semaines_fermees_ventilation': ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'],
        'semaines_fermees_eclairage': ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'],
        'semaines_mobilite': (['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        'semaines_ecs': (['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
    },
    5: {  # Enseignement secondaire
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.2,
        'occupation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je/Ve: 0-8h=0 8-18h=1 18-24h=0 | Sa: 0-8h=0 8-12h=1 12-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve: 0-8h=0 8-18h=1 18-24h=0 | Sa: 0-8h=0 8-12h=1 12-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
        'mobilite': 'Lu: 8-9hx0.3 9-13hx0.05 13-14hx0.3 14-15hx0.1 15-17hx0.05 17-18hx0.3 | Ma/Me/Je/Ve: 8-9hx0.3 10-13hx0.05 13-14hx0.3 14-15hx0.1 15-17hx0.05 17-18hx0.3 | Sa: 8-9hx0.3 10-12hx0.05 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 16-18hx0.0833333 | Sa: 10-12hx0.0833333 | Di: 0',
        'semaines_fermees': ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'],
        'semaines_arret_long_chauffage': ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm12s3', 'm10s4', 'm12s4'],
        'semaines_mobilite': (['m1s1', 'm2s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        'semaines_ecs': (['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
    },
    6: {  # Médiathèques et bibliothèques
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.2,
        'occupation': 'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je: 0-9h=0 9-12h=1 12-14h=0 14-19h=1 19-24h=0 | Ve: 0-9h=0 9-12h=1 12-14h=0 14-23h=1 23-24h=0 | Sa: 0-9h=0 9-12h=1 12-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je: 0-9h=0 9-12h=1 12-14h=0 14-19h=1 19-24h=0 | Ve: 0-9h=0 9-12h=1 12-14h=0 14-23h=1 23-24h=0 | Sa: 0-9h=0 9-12h=1 12-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
        'mobilite': 'Lu/Ma/Me/Je: 9-12hx0.45 14-19hx0.45 | Ve: 9-12hx0.45 14-23hx0.45 | Sa: 9-12hx0.45 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 9-12hx0.0208333 14-18hx0.0208333 18-19hx0.0416667 | Sa: 9-12hx0.0208333 | Di: 0',
        'semaines_fermees': ['m12s4'],
        'semaines_mobilite': (['m12s4'], []),
        'semaines_ecs': (['m12s4'], ['m1s1=1.1', 'm2s1=1.1', 'm1s2=1.1', 'm2s2=1.1', 'm12s2=1.1', 'm1s3=1.1', 'm2s3=1.1', 'm12s3=1.1', 'm1s4=1.1', 'm2s4=1.1']),
    },
    7: {  # Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.2,
        'occupation': 'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je/Ve: 0-7h=0 7-19h=1 19-24h=0 | Sa: 0-7h=0 7-12h=1 12-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve: 0-7h=0 7-19h=1 19-24h=0 | Sa: 0-7h=0 7-12h=1 12-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 7-19hx0.507692 | Sa: 7-12hx0.507692 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 7-18hx0.0138 18-19hx0.0305 | Sa: 7-11hx0.0138 11-12hx0.0305 | Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], ['m1s1=1.2', 'm2s1=1.2', 'm3s1=1.2', 'm7s1=0.5', 'm8s1=0.5', 'm11s1=1.2', 'm12s1=1.2', 'm1s2=1.2', 'm2s2=1.2', 'm3s2=1.2', 'm7s2=0.5', 'm8s2=0.5', 'm11s2=1.2', 'm12s2=1.2', 'm1s3=1.2', 'm2s3=1.2', 'm3s3=1.2', 'm7s3=0.5', 'm8s3=0.5', 'm11s3=1.2', 'm12s3=1.2', 'm1s4=1.2', 'm2s4=1.2', 'm7s4=0.5', 'm8s4=0.5', 'm11s4=1.2', 'm12s4=1.2', 'm11s5=1.2']),
    },
    8: {  # Hôtels 0, 1 et 2 étoiles (partie nuit)
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 22.873,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h=1 9-18h=0 18-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h=1 9-18h=0 18-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-9h 18-23h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-9h 18-23h',
        'ecs_cle': 'Lu/Ma/Me/Je: 6-9hx0.022 18-21hx0.033 | Ve/Sa/Di: 6-9hx0.015 18-21hx0.023',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    9: {  # Hôtels 3, 4 et 5 étoiles (partie nuit)
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 18.98,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h=1 9-18h=0 18-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h=1 9-18h=0 18-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-9h 18-23h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-9h 18-23h',
        'ecs_cle': 'Lu/Ma/Me/Je: 6-9hx0.017 18-21hx0.0113 | Ve/Sa/Di: 6-9hx0.044 18-21hx0.0293',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], ['m1s1=0.9', 'm2s1=0.9', 'm7s1=1.2', 'm8s1=1.2', 'm11s1=0.9', 'm12s1=0.9', 'm1s2=0.9', 'm2s2=0.9', 'm7s2=1.2', 'm8s2=1.2', 'm11s2=0.9', 'm12s2=0.9', 'm1s3=0.9', 'm2s3=0.9', 'm7s3=1.2', 'm8s3=1.2', 'm11s3=0.9', 'm12s3=0.9', 'm1s4=0.9', 'm2s4=0.9', 'm7s4=1.2', 'm8s4=1.2', 'm11s4=0.9', 'm12s4=0.9', 'm8s5=1.1', 'm11s5=0.9']),
    },
    10: {  # Hôtels 0, 1 et 2 étoiles (partie jour)
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 5.694,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6h=0 6-20h=1 20-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6h=0 6-20h=1 20-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 9-18hx0.444444',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 9-14hx0.0189 14-18hx0.0121',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    11: {  # Hôtels 3, 4 et 5 étoiles (partie jour)
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 4.76,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6h=0 6-20h=1 20-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6h=0 6-20h=1 20-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 9-18hx0.444444',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 9-14hx0.0189 14-18hx0.0121',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], ['m1s1=0.9', 'm2s1=0.9', 'm7s1=1.2', 'm8s1=1.2', 'm11s1=0.9', 'm12s1=0.9', 'm1s2=0.9', 'm2s2=0.9', 'm7s2=1.2', 'm8s2=1.2', 'm11s2=0.9', 'm12s2=0.9', 'm1s3=0.9', 'm2s3=0.9', 'm7s3=1.2', 'm8s3=1.2', 'm11s3=0.9', 'm12s3=0.9', 'm1s4=0.9', 'm2s4=0.9', 'm7s4=1.2', 'm8s4=1.2', 'm11s4=0.9', 'm12s4=0.9', 'm8s5=1.1', 'm11s5=0.9']),
    },
    12: {  # Établissements d'accueil de la petite enfance
        'consigne_ch': (21, 18, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.714,
        'occupation': 'Lu/Ma/Me/Je/Ve: 7-19h | Sa/Di: 0',
        'chauffage': 'Lu: 0-6h=-1 6-18h=1 18-24h=0 | Ma/Me/Je: 0-6h=0 6-18h=1 18-24h=0 | Ve: 0-6h=0 6-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-6h=-1 6-18h=1 18-24h=0 | Ma/Me/Je: 0-6h=0 6-18h=1 18-24h=0 | Ve: 0-6h=0 6-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 7-8hx0.3 11-13hx0.05 16-17hx0.05 17-18hx0.2 18-19hx0.05 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 6-7hx0.005 7-8hx0.00833333 8-18hx0.0186667 | Sa/Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        'semaines_ecs': ([], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
    },
    13: {  # Restaurants - en continu, 18 heures par jour, 7 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 19.5,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5h=0 5-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5h=0 5-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-7hx0.05 7-9hx0.4 9-12hx0.1 12-14hx0.4 14-18hx0.1 18-20hx0.4 20-21hx0.2 21-22hx0.1 22-24hx0.05',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 8-9hx0.0285714 12-13hx0.0428571 21-22hx0.0714286',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    14: {  # Restaurants - 1 repas par jour, 5 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 2.2,
        'occupation': 'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
        'chauffage': 'Lu: 0-8h=-1 8-14h=1 14-24h=0 | Ma/Me/Je: 0-8h=0 8-14h=1 14-24h=0 | Ve: 0-8h=0 8-14h=1 14-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-8h=-1 8-14h=1 14-24h=0 | Ma/Me/Je: 0-8h=0 8-14h=1 14-24h=0 | Ve: 0-8h=0 8-14h=1 14-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 8-11hx0.05 11-14hx0.4 14-15hx0.05 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 8-9hx0.08 12-13hx0.12 | Sa/Di: 0',
        'semaines_fermees': ['m12s4'],
        'semaines_mobilite': (['m12s4'], []),
        'semaines_ecs': (['m12s4'], []),
    },
    15: {  # Restaurants - 2 repas par jour, 7 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 5.3,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 10-15h 17-23h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-8h=0 8-14h=1 14-16h=0 16-22h=1 22-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-8h=0 8-14h=1 14-16h=0 16-22h=1 22-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 8-14h 16-22h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 8-14h 16-22h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 8-11hx0.05 11-14hx0.4 14-17hx0.05 17-18hx0.1 18-19hx0.4 19-20hx0.3 20-21hx0.1 21-22hx0.05',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 8-9hx0.0571429 12-13hx0.0857143',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    16: {  # Restaurants - 2 repas par jour, 6 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 4.7,  # ÉCART : tableau 277 p. 1054 et synthèse p. 25 donnent 19.5
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 10-15h 17-23h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-9h=0 9-14h=1 14-16h=0 16-22h=1 22-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-9h=0 9-14h=1 14-16h=0 16-22h=1 22-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa: 8-11hx0.05 11-14hx0.4 14-17hx0.05 17-18hx0.1 18-19hx0.4 19-20hx0.3 20-21hx0.1 21-22hx0.05 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 8-9hx0.0666667 12-13hx0.1 | Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    17: {  # Commerces
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.24,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 7-22h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-6h=0 6-21h=1 21-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-6h=0 6-21h=1 21-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 6-7hx0.5 7-21h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 6-7hx0.5 7-21h | Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa: 7-9hx0.15 9-10hx0.2 10-11hx0.25 11-12hx0.3 12-14hx0.35 14-15hx0.4 15-17hx0.45 17-18hx0.4 18-19hx0.2 19-20hx0.1 20-21hx0.05 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 6-7hx0.166667 | Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    18: {  # Vestiaires seuls
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 79,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 8-22h | Di: 8-19h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 9-10hx0.028 11-12hx0.028 14-15hx0.028 17-18hx0.028 20-21hx0.035 | Di: 9-10hx0.028 11-12hx0.028 14-15hx0.028 17-18hx0.035',
        'semaines_fermees': ['m1s1', 'm12s4'],
        'semaines_mobilite': (['m1s1', 'm12s4'], []),
        'semaines_ecs': (['m1s1', 'm12s4'], ['m2s1=1.2', 'm3s1=1.1', 'm11s1=1.1', 'm12s1=1.2', 'm1s2=1.2', 'm2s2=1.2', 'm3s2=1.1', 'm11s2=1.1', 'm12s2=1.2', 'm1s3=1.2', 'm2s3=1.1', 'm3s3=1.1', 'm8s3=0.5', 'm10s3=1.1', 'm11s3=1.1', 'm12s3=1.2', 'm1s4=1.2', 'm2s4=1.1', 'm3s4=1.1', 'm8s4=0.5', 'm10s4=1.1', 'm11s4=1.1', 'm3s5=1.1', 'm11s5=1.1']),
    },
    19: {  # Établissements sanitaires avec hébergement
        'consigne_ch': (21, 18, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 2.8,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-21h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.25 6-8hx0.5 8-10hx0.25 10-12hx0.5 12-13hx0.25 13-15hx0.5 15-18hx0.25 18-20hx0.5 20-21hx0.25',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-7hx0.0071 7-10hx0.014 10-16hx0.0071 16-19hx0.01 19-21hx0.0071',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], ['m1s1=1.05', 'm7s1=0.95', 'm8s1=0.95', 'm12s1=1.05', 'm1s2=1.05', 'm7s2=0.95', 'm8s2=0.95', 'm12s2=1.05', 'm1s3=1.05', 'm7s3=0.95', 'm8s3=0.95', 'm12s3=1.05', 'm1s4=1.05', 'm7s4=0.95', 'm8s4=0.95', 'm12s4=1.05', 'm8s5=0.95', 'm11s5=1.05']),
    },
    20: {  # Établissements de santé (partie nuit)
        'consigne_ch': (21, 18, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 1.68,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5hx0.35 5-21h 21-24hx0.35',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-7hx0.1 7-8hx0.15 8-12hx0.1 12-13hx0.15 13-17hx0.1 17-18hx0.15 18-24hx0.1',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.00066 6-7hx0.00153 7-8hx0.00351 8-9hx0.0068 9-10hx0.01006 10-11hx0.01292 11-12hx0.01458 12-13hx0.0144 13-14hx0.01253 14-15hx0.01099 15-16hx0.00904 16-17hx0.00713 17-18hx0.00655 18-19hx0.00722 19-20hx0.00838 20-21hx0.00898 21-22hx0.00771',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    21: {  # Établissements de santé (partie jour)
        'consigne_ch': (21, 18, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 25.2,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 7-18h | Di: 0',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-7h=0 7-18h=1 18-24h=0 | Di: 0-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-7h=0 7-18h=1 18-24h=0 | Di: 0-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 7-18h | Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 7-18h | Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa: 7-8hx0.3 8-18hx0.4 18-19hx0.3 19-20hx0.05 | Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 6-12hx0.0185185 16-19hx0.0185185 | Di: 0',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    22: {  # Aérogares
        'consigne_ch': (19, 16, 16), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.24,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5h=0 5-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5h=0 5-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 3-5hx0.05 5-6hx0.1 6-7hx0.15 7-19hx0.2 19-21hx0.15 21-23hx0.1 23-24hx0.05',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 6-24hx0.00793651',
        'semaines_fermees': [],
        'semaines_mobilite': ([], []),
        'semaines_ecs': ([], []),
    },
    23: {  # Industries ou artisanats 3x8h
        'consigne_ch': (15, 7, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.24,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h=1',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24hx0.1',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa/Di: 7-9hx0.0357143 15-17hx0.0357143',
        'semaines_fermees': [],
        'semaines_partielles_occupation': ['m12s4=0.5'],
        'semaines_partielles_chauffage': ['m12s4=0.5'],
        'semaines_mobilite': ([], ['m12s4=0.5']),
        'semaines_ecs': ([], ['m12s4=0.5']),
    },
    24: {  # Industries ou artisanats 8h à 18h
        'consigne_ch': (15, 7, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 0.24,
        'occupation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'chauffage': 'Lu: 0-8h=-1 8-18h=1 18-24h=0 | Ma/Me/Je: 0-8h=0 8-18h=1 18-24h=0 | Ve: 0-8h=0 8-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-8h=-1 8-18h=1 18-24h=0 | Ma/Me/Je: 0-8h=0 8-18h=1 18-24h=0 | Ve: 0-8h=0 8-18h=1 18-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 8-9hx0.5 9-10hx0.4 10-12hx0.2 12-14hx0.4 14-16hx0.2 16-17hx0.4 17-18hx0.5 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 17-20hx0.0666667 | Sa/Di: 0',
        'semaines_fermees': [],
        'semaines_partielles_occupation': ['m12s4=0.5'],
        'semaines_partielles_chauffage': ['m12s4=0.5'],
        'semaines_mobilite': ([], ['m12s4=0.5']),
        'semaines_ecs': ([], ['m12s4=0.5']),
    },
    25: {  # Établissements sportifs municipaux ou scolaires
        'consigne_ch': (15, 7, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 13.2,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa: 8-21hx0.363636 | Di: 8-18hx0.363636',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 9-10hx0.028 11-12hx0.028 14-15hx0.028 17-18hx0.028 20-21hx0.035 | Di: 9-10hx0.028 11-12hx0.028 14-15hx0.028 17-18hx0.035',
        'semaines_fermees': ['m1s1', 'm12s4'],
        'semaines_mobilite': (['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        'semaines_ecs': (['m1s1', 'm12s4'], ['m2s1=1.2', 'm3s1=1.1', 'm11s1=1.1', 'm12s1=1.2', 'm1s2=1.2', 'm2s2=1.2', 'm3s2=1.1', 'm11s2=1.1', 'm12s2=1.2', 'm1s3=1.2', 'm2s3=1.1', 'm3s3=1.1', 'm8s3=0.5', 'm10s3=1.1', 'm11s3=1.1', 'm12s3=1.2', 'm1s4=1.2', 'm2s4=1.1', 'm3s4=1.1', 'm8s4=0.5', 'm10s4=1.1', 'm11s4=1.1', 'm3s5=1.1', 'm11s5=1.1']),
    },
    26: {  # Restaurants scolaires - 1 repas par jour, 5 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 4.5,
        'occupation': 'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
        'chauffage': 'Lu: 0-9h=-1 9-15h=1 15-24h=0 | Ma/Me/Je: 0-9h=0 9-15h=1 15-24h=0 | Ve: 0-9h=0 9-15h=1 15-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-9h=-1 9-15h=1 15-24h=0 | Ma/Me/Je: 0-9h=0 9-15h=1 15-24h=0 | Ve: 0-9h=0 9-15h=1 15-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 8-11hx0.05 11-14hx0.4 14-15hx0.05 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 9-10hx0.08 13-14hx0.12 | Sa/Di: 0',
        'semaines_fermees': ['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'],
        'semaines_mobilite': (['m12s4'], []),
        'semaines_ecs': (['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'], []),
    },
    27: {  # Restaurants scolaires - 3 repas par jour, 5 jours sur 7
        'consigne_ch': (19, 16, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 9.8,
        'occupation': 'Lu/Ma/Me/Je/Ve: 6-15h 16-20h | Sa/Di: 0',
        'chauffage': 'Lu: 0-5h=-1 5-14h=1 14-15h=0 15-19h=1 19-24h=0 | Ma/Me/Je: 0-5h=0 5-14h=1 14-15h=0 15-19h=1 19-24h=0 | Ve: 0-5h=0 5-14h=1 14-15h=0 15-19h=1 19-24h=-1 | Sa/Di: 0-24h=-1',
        'refroidissement': 'Lu: 0-5h=-1 5-14h=1 14-15h=0 15-19h=1 19-24h=0 | Ma/Me/Je: 0-5h=0 5-14h=1 14-15h=0 15-19h=1 19-24h=0 | Ve: 0-5h=0 5-14h=1 14-15h=0 15-19h=1 19-24h=-1 | Sa/Di: 0-24h=-1',
        'ventilation': 'Lu/Ma/Me/Je/Ve: 5-14h 15-19h | Sa/Di: 0',
        'eclairage': 'Lu/Ma/Me/Je/Ve: 5-14h 15-19h | Sa/Di: 0',
        'mobilite': 'Lu/Ma/Me/Je/Ve: 6-7hx0.05 7-8hx0.3 8-11hx0.05 11-14hx0.4 14-17hx0.05 17-18hx0.1 18-19hx0.4 19-20hx0.3 20-21hx0.1 21-22hx0.05 | Sa/Di: 0',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve: 8-9hx0.04 12-13hx0.06 21-22hx0.1 | Sa/Di: 0',
        'semaines_fermees': ['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'],
        'semaines_mobilite': ([], []),
        'semaines_ecs': (['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'], []),
    },
    28: {  # Établissements sportifs privés
        'consigne_ch': (15, 7, 7), 'consigne_fr': (26, 30, 30),  # confort, arrêt < 48 h, arrêt > 48 h, °C
        'ecs_a': 33.9,
        'occupation': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'chauffage': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'refroidissement': 'Lu/Ma/Me/Je/Ve/Sa: 0-8h=0 8-21h=1 21-24h=0 | Di: 0-8h=0 8-18h=1 18-24h=0',
        'ventilation': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'eclairage': 'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
        'mobilite': 'Lu/Ma/Me/Je/Ve/Sa: 8-21hx0.363636 | Di: 8-18hx0.363636',
        'ecs_cle': 'Lu/Ma/Me/Je/Ve/Sa: 8-20hx0.011274 20-21hx0.0124014 | Di: 8-17hx0.011274 17-18hx0.0124014',
        'semaines_fermees': ['m1s1', 'm12s4'],
        'semaines_mobilite': (['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        'semaines_ecs': (['m1s1', 'm12s4'], ['m2s1=1.2', 'm3s1=1.1', 'm11s1=1.1', 'm12s1=1.2', 'm1s2=1.2', 'm2s2=1.2', 'm3s2=1.1', 'm11s2=1.1', 'm12s2=1.2', 'm1s3=1.2', 'm2s3=1.1', 'm3s3=1.1', 'm8s3=0.5', 'm10s3=1.1', 'm11s3=1.1', 'm12s3=1.2', 'm1s4=1.2', 'm2s4=1.1', 'm3s4=1.1', 'm8s4=0.5', 'm10s4=1.1', 'm11s4=1.1', 'm3s5=1.1', 'm11s5=1.1']),
    },
}
```

```python
# Locaux conventionnels, dans l'ordre du tableur : (nom, Rat_loc, Nocc_nom par m² utile, Qmax_occ en W par occupant,
#  omega_max_occ en kg/h par occupant, Qmax_proc en W par m² utile en occupation, Qmax_proc x valeur de t_ch hors occupation
#  (colonne « hors période d'occupation » de la synthèse p. 24-26 : minimum du profil hebdomadaire, sauf chambres des hôtels 8 et 9,
#  où ce minimum vaut 0 de 9 h à 18 h et où le texte retient la valeur de nuit de t_ch, 0,15 et 0,34), omega_max_proc en kg/h par m²,
#  profil hebdomadaire 'occupant' (t_occ), profil hebdomadaire 'apports' (t_ch), semaines à 0 puis semaines partielles du profil annuel du local).
# Usages 1 et 2 : Nocc_nom = None, le nombre d'occupants est Nadeq (équations 32 à 37) ; Qmax_occ en W par adulte équivalent.
# 'vide' : cellule vide du tableur, lue 0 par openbce.scenarios._locaux ; la valeur de la synthèse p. 24-25 est rappelée.
LOCAUX = {
    1: [  # Maisons individuelles ou accolées ; feuille MI ; somme des ratios 1
        ('Maison individuelle', 1, None, 90, 0.055, 5.7, 1.14, 0,  # unité du tableur : W/Nadeq
         'Lu/Ma/Je/Ve: 0-6hx0.7 6-9h 9-11hx0.05 11-12hx0.1 12-13hx0.15 13-16hx0.05 16-17hx0.1 17-22h 22-24hx0.7 | Me: 0-6hx0.7 6-9h 9-11hx0.05 11-12hx0.1 12-13hx0.15 13-22h 22-24hx0.7 | Sa/Di: 0-6hx0.7 6-22h 22-24hx0.7',
         'Lu/Ma/Je/Ve: 0-6hx0.2 6-9h 9-17hx0.2 17-22h 22-24hx0.2 | Me: 0-6hx0.2 6-9h 9-13hx0.2 13-22h 22-24hx0.2 | Sa/Di: 0-6hx0.2 6-22h 22-24hx0.2',
         ['m12s4'], []),
    ],
    2: [  # Logements collectifs ; feuille LC ; somme des ratios 1
        ('Logements', 0.9, None, 90, 0.055, 5.7, 1.14, 0,  # unité du tableur : W/Nadeq
         'Lu/Ma/Je/Ve: 0-6hx0.7 6-9h 17-22h 22-24hx0.7 | Me: 0-6hx0.7 6-9h 13-22h 22-24hx0.7 | Sa/Di: 0-6hx0.7 6-22h 22-24hx0.7',
         'Lu/Ma/Je/Ve: 0-6hx0.2 6-9h 9-17hx0.2 17-22h 22-24hx0.2 | Me: 0-6hx0.2 6-9h 9-13hx0.2 13-22h 22-24hx0.2 | Sa/Di: 0-6hx0.2 6-22h 22-24hx0.2',
         ['m12s4'], []),
        ('Circulation', 0.1, None, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Nadeq
         'Lu/Ma/Je/Ve: 0-9h 17-24h | Me: 0-9h 13-24h | Sa/Di: 0-24h',
         'Lu/Ma/Je/Ve: 0-9h 17-24h | Me: 0-9h 13-24h | Sa/Di: 0-24h',
         ['m12s4'], []),
    ],
    3: [  # Bureaux ; feuille BUR ; somme des ratios 1
        ('Bureau standard', 0.6047, 0.1, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-12h 12-14hx0.57 14-17h 17-18hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-17h 17-18hx0.55 18-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
        ('Salle de réunion', 0.1047, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Sa/Di: 0',
         ['m8s1', 'm4s2', 'm8s2', 'm8s3', 'm8s4', 'm12s4'], []),
        ('Circulation Accueil', 0.2558, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
        ('Sanitaires collectifs', 0.0348, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
    ],
    4: [  # Enseignement primaire ; feuille ENS_PRI ; somme des ratios 1
        ('Bureau standard', 0.1, 0.067, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-12h 12-14hx0.57 14-16h 16-17hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-16h 16-17hx0.55 17-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Circulation Accueil', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de classe', 0.55, 0.66, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Je/Ve: 8-9hx0.5 9-16h 16-17hx0.5 | Me/Sa/Di: 0',
         'Lu/Ma/Je/Ve: 8-17h | Me/Sa/Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de réunion', 0.05, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Me/Sa/Di: 0',
         'Lu/Ma/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Me/Sa/Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de repos', 0.15, 0.66, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Je/Ve: 13-16h | Me/Sa/Di: 0',
         'Lu/Ma/Je/Ve: 13-16h | Me/Sa/Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Sanitaires vestiaires', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-17h | Sa/Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
    ],
    5: [  # Enseignement secondaire ; feuille ENS_SEC ; somme des ratios 1
        ('Bureau standard', 0.1, 0.1, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-12h 12-14hx0.57 14-17h 17-18hx0.57 | Sa: 8-9hx0.57 9-12h 12-13hx0.57 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-17h 17-18hx0.55 18-24hx0.11111 | Sa: 0-8hx0.11111 8-9hx0.55 9-11h 11-12hx0.55 12-24hx0.11111 | Di: 0-24hx0.11111',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Circulation Accueil', 0.2, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de classe', 0.25, 0.67, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.5 9-17h 17-18hx0.5 | Sa: 8-9hx0.25 9-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de réunion', 0.1, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Sa: 9-10hx0.25 10-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Sa: 9-10hx0.25 10-11hx0.5 11-12hx0.25 | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Centre de documentation', 0.05, 0.1, 90, 0.055, 5, 0.55555, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-10hx0.5 10-15h 15-17hx0.5 17-18hx0.25 | Sa: 8-9hx0.25 9-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-17h 17-18hx0.55 18-24hx0.11111 | Sa: 0-8hx0.11111 8-9hx0.55 9-11h 11-12hx0.55 12-24hx0.11111 | Di: 0-24hx0.11111',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle des professeurs', 0.05, 0.67, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18hx0.5 | Sa: 8-12hx0.5 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ("Salle d'enseignement informatique", 0.05, 0.335, 90, 0.055, 25.795, 2.86582, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-10hx0.5 10-15h 15-17hx0.5 17-18hx0.25 | Sa: 8-9hx0.25 9-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.1111 8-9hx0.25 9-10hx0.5 10-15h 15-17hx0.5 17-18hx0.25 18-24hx0.1111 | Sa: 0-8hx0.1111 8-9hx0.25 9-11hx0.5 11-12hx0.25 12-24hx0.1111 | Di: 0-24hx0.1111',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de conférence Salle polyvalente', 0.15, 0.33, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5 | Sa: 9-10hx0.25 10-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-18h | Sa: 9-12h | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Sanitaires collectifs', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa: 8-12h | Di: 0',
         ['m1s1', 'm2s1', 'm11s1', 'm2s2', 'm4s2', 'm4s3', 'm10s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
    ],
    6: [  # Médiathèques et bibliothèques ; feuille MED ; somme des ratios 1
        ('Circulation accueil', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
         'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
         ['m12s4'], []),
        ('Bureau standard', 0.05, 0.1, 90, 0.055, 16, 1.76, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-10hx0.57 10-11h 11-12hx0.57 14-15hx0.57 15-17h 17-18hx0.57 | Sa: 9-12hx0.57 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-9hx0.11111 9-10hx0.55 10-12h 12-14hx0.55 14-17h 17-18hx0.55 18-24hx0.11111 | Sa: 0-9hx0.11111 9-12hx0.55 12-13hx0.11 13-24hx0.11111 | Di: 0-24hx0.11111',
         ['m12s4'], []),
        ('Sanitaires collectifs', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
         'Lu/Ma/Me/Je: 9-12h 14-19h | Ve: 9-12h 14-23h | Sa: 9-12h | Di: 0',
         ['m12s4'], []),
        ('Local service', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-12h 14-19h | Sa: 9-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-12h 14-19h | Sa: 9-12h | Di: 0',
         ['m12s4'], []),
        ('Salle de réunion', 0.1, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 14-19hx0.5 | Sa: 9-10hx0.25 10-12hx0.5 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-10hx0.25 10-12hx0.5 14-19hx0.5 | Sa: 9-10hx0.25 10-12hx0.5 | Di: 0',
         ['m12s4'], []),
        ('Centre de documentation', 0.6, 0.1, 90, 0.055, 5, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-10hx0.5 10-12h 14-18h 18-19hx0.5 | Sa: 9-10hx0.5 10-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-9hx0.111 9-10hx0.5 10-12h 12-14hx0.111 14-18h 18-19hx0.5 19-24hx0.111 | Sa: 0-9hx0.111 9-10hx0.5 10-12h 13-24hx0.111 | Di: 0-24hx0.111',
         ['m12s4'], []),
        ('Salle multi-fonctions', 0.05, 0.26, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je: 9-10hx0.5 10-12h 14-18h 18-19hx0.5 | Ve: 9-10hx0.5 10-12h 14-22h 22-23hx0.5 | Sa: 9-10hx0.5 10-12h | Di: 0',
         'Lu/Ma/Me/Je: 9-10hx0.5 10-12h 14-18h 18-19hx0.5 | Ve: 9-10hx0.5 10-12h 14-22h 22-23hx0.5 | Sa: 9-10hx0.5 10-12h | Di: 0',
         ['m12s4'], []),
    ],
    7: [  # Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques ; feuille ENS_SUP ; somme des ratios 1
        ('Bureau standard', 0.1, 0.1, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-11h 11-13hx0.57 13-16h 16-17hx0.57 | Sa: 7-12hx0.57 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.11111 7-8hx0.55 8-11h 11-13hx0.55 13-16h 16-17hx0.55 17-24hx0.11111 | Sa: 0-7hx0.11111 7-12hx0.55 12-24hx0.11111 | Di: 0-24hx0.11111',
         [], ['m7s1=0.5', 'm8s1=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Circulation Accueil', 0.15, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
         [], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de classe', 0.25, 0.67, 90, 0.055, 0.5, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-18h 18-19hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-18h 18-19hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         ['m1s1', 'm9s1', 'm2s2', 'm4s2', 'm9s2', 'm4s3', 'm6s3', 'm6s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Centre de documentation', 0.05, 0.1, 90, 0.055, 5, 0.55555, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-18h 18-19hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.11111 7-8hx0.55 8-18h 18-19hx0.55 19-24hx0.11111 | Sa: 0-7hx0.11111 7-8hx0.25 8-11hx0.5 11-12hx0.25 12-24hx0.11111 | Di: 0-24hx0.11111',
         [], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de conférence Amphithéâtre', 0.15, 0.33, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-11h 11-13hx0.57 13-18h 18-19hx0.57 | Sa: 7-8hx0.57 8-11h 11-12hx0.57 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-11h 11-13hx0.57 13-18h 18-19hx0.57 | Sa: 7-8hx0.57 8-11h 11-12hx0.57 | Di: 0',
         ['m1s1', 'm9s1', 'm2s2', 'm4s2', 'm9s2', 'm4s3', 'm6s3', 'm6s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ("Salle d'enseignement informatique", 0.05, 0.335, 90, 0.055, 25.795, 2.86325, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-16h 16-17hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.111 7-8hx0.5 8-16h 16-17hx0.5 17-24hx0.111 | Sa: 0-7hx0.111 7-8hx0.25 8-11hx0.5 11-12hx0.25 12-24hx0.111 | Di: 0-24hx0.111',
         ['m1s1', 'm9s1', 'm2s2', 'm4s2', 'm9s2', 'm4s3', 'm6s3', 'm6s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Salle de réunion', 0.05, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-11hx0.5 11-13hx0.25 13-18hx0.5 18-19hx0.25 | Sa: 8-9hx0.25 9-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-11hx0.5 11-13hx0.25 13-18hx0.5 18-19hx0.25 | Sa: 8-9hx0.25 9-11hx0.5 11-12hx0.25 | Di: 0',
         [], ['m7s1=0.5', 'm8s1=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Sanitaires collectifs', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
         'Lu/Ma/Me/Je/Ve: 7-19h | Sa: 7-12h | Di: 0',
         [], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
        ('Local service', 0.15, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-18h 18-19hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve: 7-8hx0.5 8-18h 18-19hx0.5 | Sa: 7-8hx0.25 8-11hx0.5 11-12hx0.25 | Di: 0',
         ['m1s1', 'm9s1', 'm2s2', 'm4s2', 'm9s2', 'm4s3', 'm6s3', 'm6s4', 'm12s4'], ['m7s1=0.5', 'm8s1=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm8s5=0.5']),
    ],
    8: [  # Hôtels 0, 1 et 2 étoiles (partie nuit) ; feuille HOT012_N ; somme des ratios 1
        ('Circulation Accueil', 0.233, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
        ('Chambre sans cuisine avec salle de bain', 0.728, 0.05, 90, 0.055, 4, 0.6, 0,  # unité du tableur : W/Noccnom ; 0,6 = 4 x 0,15, valeur de nuit (synthèse p. 24), minimum hebdomadaire 0
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.7 6-9hx0.8 18-20hx0.8 20-23h 23-24hx0.7',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.15 6-9hx0.8 18-20hx0.8 20-23h 23-24hx0.15',
         [], []),
        ('Sanitaires collectifs', 0.007, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
        ('Local service', 0.032, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
    ],
    9: [  # Hôtels 3, 4 et 5 étoiles (partie nuit) ; feuille HOT345_N ; somme des ratios 1
        ('Circulation Accueil', 0.233, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
        ('Chambre sans cuisine avec salle de bain', 0.728, 0.0375, 90, 0.055, 4.625, 1.5725, 0,  # unité du tableur : W/Noccnom ; 1,5725 = 4,625 x 0,34, valeur de nuit (synthèse p. 24), minimum hebdomadaire 0
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.7 6-9hx0.8 18-20hx0.8 20-23h 23-24hx0.7',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.34 6-9hx0.8 18-20hx0.8 20-23h 23-24hx0.34',
         [], []),
        ('Sanitaires collectifs', 0.007, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
        ('Local service', 0.032, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-9h 18-24h',
         [], []),
    ],
    10: [  # Hôtels 0, 1 et 2 étoiles (partie jour) ; feuille HOT012_J ; somme des ratios 1
        ('Bureau standard', 0.1161, 0.067, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.11111 6-20h 20-24hx0.11111',
         [], []),
        ('Circulation Accueil', 0.4308, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         [], []),
        ('Sanitaires collectifs', 0.0512, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         [], []),
        ('Salle petits déjeuners', 0.4019, 0.5, 90, 0.055, 88.8, 8.88, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-7hx0.5 7-9h 9-10hx0.5',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.1 6-7hx0.5 7-9h 9-10hx0.5 10-24hx0.1',
         [], []),
    ],
    11: [  # Hôtels 3, 4 et 5 étoiles (partie jour) ; feuille HOT345_J ; somme des ratios 1
        ('Bureau standard', 0.105, 0.067, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.11111 6-20h 20-24hx0.11111',
         [], []),
        ('Circulation Accueil', 0.173, 0, 90, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         [], []),
        ('Sanitaires collectifs', 0.037, 0, 90, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-20h',
         [], []),
        ('Salle petits déjeuners', 0.17, 0.5, 90, 0.055, 'vide (synthèse p. 24-25 : 44.3)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-7hx0.5 7-9h 9-10hx0.5',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-6hx0.1 6-7hx0.5 7-9h 9-10hx0.5 10-24hx0.1',
         [], []),
        ('salle de séminaires réunion', 0.4276, 0.42, 90, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 9-10hx0.25 10-12hx0.5 12-14hx0.25 14-17hx0.5',
         [], []),
        ('Bar', 0.0874, 0.1, 90, 0.055, 34.4, 4.128, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 12-15hx0.2 17-19hx0.5',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-12hx0.12 12-15hx0.2 15-17hx0.12 17-19hx0.5 19-24hx0.12',
         [], []),
    ],
    12: [  # Établissements d'accueil de la petite enfance ; feuille CRE ; somme des ratios 1
        ('Bureau standard', 0.15, 0.067, 105, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-11h 11-13hx0.57 13-17h 17-18hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.11111 7-8hx0.55 8-17h 17-18hx0.55 18-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Circulation Accueil', 0.15, 0, 105, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Salle de réunion', 0.1, 0.42, 105, 0.055, 'vide (synthèse p. 24-25 : 10)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-11hx0.5 11-13hx0.25 13-16hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-11hx0.5 11-13hx0.25 13-16hx0.5 | Sa/Di: 0',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Salle de jeux', 0.3, 0.25, 105, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 6-7hx0.25 7-8hx0.5 8-16h 16-18hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Salle de repos', 0.2, 0.66, 105, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 12-15h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 12-15h | Sa/Di: 0',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
        ('Sanitaires vestiaires', 0.1, 0, 105, 0.055, 'vide (synthèse p. 24-25 : 0)', None, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 6-18h | Sa/Di: 0',
         [], ['m1s1=0.5', 'm2s1=0.5', 'm7s1=0.5', 'm8s1=0.5', 'm2s2=0.5', 'm4s2=0.5', 'm7s2=0.5', 'm8s2=0.5', 'm4s3=0.5', 'm7s3=0.5', 'm8s3=0.5', 'm7s4=0.5', 'm8s4=0.5', 'm10s4=0.5', 'm12s4=0.5', 'm8s5=0.5']),
    ],
    13: [  # Restaurants - en continu, 18 heures par jour, 7 jours sur 7 ; feuille RES_CON ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.59, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-7hx0.25 7-9hx0.8 9-11hx0.25 11-13hx0.8 13-19hx0.25 19-21hx0.8 21-24hx0.25',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
         [], []),
        ('Cuisine', 0.2, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-24h',
         [], []),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-14h',
         ['m12s4'], []),
    ],
    14: [  # Restaurants - 1 repas par jour, 5 jours sur 7 ; feuille RES_1RJ-5J7 ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.77, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 10-11hx0.5 11-12h 12-13hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 10-13h | Sa/Di: 0',
         ['m12s4'], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5']),
        ('Cuisine', 0.2, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
         ['m12s4'], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5']),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-14h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-14h',
         ['m12s4'], []),
    ],
    15: [  # Restaurants - 2 repas par jour, 7 jours sur 7 ; feuille RES_2RJ-7J7 ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.59, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 11-13hx0.8 13-14hx0.25 18-19hx0.25 19-21hx0.8 21-22hx0.25',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 11-14h 18-22h',
         [], []),
        ('Cuisine', 0.2, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 9-14h 16-22h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 9-14h 16-22h',
         [], []),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         [], []),
    ],
    16: [  # Restaurants - 2 repas par jour, 6 jours sur 7 ; feuille RES_2RJ-6J7 ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.59, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 11-13hx0.8 13-14hx0.25 18-19hx0.25 19-21hx0.8 21-22hx0.25 | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 11-14h 18-22h | Di: 0',
         [], []),
        ('Cuisine', 0.2, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         [], []),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 9-14h 16-22h | Di: 0',
         [], []),
    ],
    17: [  # Commerces ; feuille COM ; somme des ratios 1
        ('Sanitaires collectifs', 0.01, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 6-21h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 6-21h | Di: 0',
         [], []),
        ('Douches collectives', 0.01, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 6-21h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 6-21h | Di: 0',
         [], []),
        ('Aire de vente (supérieure à 300m²)', 0.25, 0.15, 105, 0.055, 8, 0, 0,  # unité du tableur : W/Noccnom
         'Lu: 7-8hx0.12 8-9hx0.25 9-10hx0.35 10-11hx0.27 11-12hx0.53 12-13hx0.41 13-14hx0.43 14-15hx0.57 15-16hx0.56 16-17hx0.59 17-18hx0.47 18-19hx0.22 19-20hx0.01 20-21hx0.03 | Ma: 7-8hx0.14 8-9hx0.26 9-10hx0.36 10-11hx0.27 11-12hx0.54 12-13hx0.42 13-14hx0.43 14-16hx0.56 16-17hx0.58 17-18hx0.5 18-19hx0.26 19-20hx0.04 20-21hx0.03 | Me: 7-8hx0.13 8-9hx0.25 9-10hx0.37 10-11hx0.28 11-12hx0.54 12-13hx0.45 13-14hx0.53 14-15hx0.7 15-17hx0.69 17-18hx0.53 18-19hx0.28 19-20hx0.05 20-21hx0.04 | Je: 7-8hx0.15 8-9hx0.29 9-10hx0.4 10-11hx0.3 11-12hx0.56 12-13hx0.45 13-14hx0.49 14-15hx0.61 15-16hx0.59 16-17hx0.6 17-18hx0.49 18-19hx0.27 19-20hx0.05 20-21hx0.04 | Ve: 7-8hx0.13 8-9hx0.27 9-10hx0.39 10-11hx0.31 11-12hx0.53 12-13hx0.47 13-14hx0.53 14-15hx0.68 15-16hx0.7 16-17hx0.71 17-18hx0.56 18-19hx0.33 19-20hx0.09 20-21hx0.06 | Sa: 7-8hx0.07 8-9hx0.26 9-10hx0.54 10-11hx0.48 11-12hx0.47 12-13hx0.52 13-14hx0.78 14-17h 17-18hx0.71 18-19hx0.36 19-20hx0.07 20-21hx0.06 | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-12h 12-21hx0.25 | Di: 0',
         [], []),
        ('Aire de vente (inférieure à 300m²)', 0.4, 0.25, 105, 0.055, 8, 0, 0,  # unité du tableur : W/Noccnom
         'Lu: 7-8hx0.12 8-9hx0.25 9-10hx0.35 10-11hx0.27 11-12hx0.53 12-13hx0.41 13-14hx0.43 14-15hx0.57 15-16hx0.56 16-17hx0.59 17-18hx0.47 18-19hx0.22 19-20hx0.01 20-21hx0.03 | Ma: 7-8hx0.14 8-9hx0.26 9-10hx0.36 10-11hx0.27 11-12hx0.54 12-13hx0.42 13-14hx0.43 14-16hx0.56 16-17hx0.58 17-18hx0.5 18-19hx0.26 19-20hx0.04 20-21hx0.03 | Me: 7-8hx0.13 8-9hx0.25 9-10hx0.37 10-11hx0.28 11-12hx0.54 12-13hx0.45 13-14hx0.53 14-15hx0.7 15-17hx0.69 17-18hx0.53 18-19hx0.28 19-20hx0.05 20-21hx0.04 | Je: 7-8hx0.15 8-9hx0.29 9-10hx0.4 10-11hx0.3 11-12hx0.56 12-13hx0.45 13-14hx0.49 14-15hx0.61 15-16hx0.59 16-17hx0.6 17-18hx0.49 18-19hx0.27 19-20hx0.05 20-21hx0.04 | Ve: 7-8hx0.13 8-9hx0.27 9-10hx0.39 10-11hx0.31 11-12hx0.53 12-13hx0.47 13-14hx0.53 14-15hx0.68 15-16hx0.7 16-17hx0.71 17-18hx0.56 18-19hx0.33 19-20hx0.09 20-21hx0.06 | Sa: 7-8hx0.07 8-9hx0.26 9-10hx0.54 10-11hx0.48 11-12hx0.47 12-13hx0.52 13-14hx0.78 14-17h 17-18hx0.71 18-19hx0.36 19-20hx0.07 20-21hx0.06 | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-21h | Di: 0',
         [], []),
        ('Circulation Accueil', 0.28, 0.2, 105, 0.055, 8, 0, 0,  # unité du tableur : W/Noccnom
         'Lu: 7-8hx0.12 8-9hx0.25 9-10hx0.35 10-11hx0.27 11-12hx0.53 12-13hx0.41 13-14hx0.43 14-15hx0.57 15-16hx0.56 16-17hx0.59 17-18hx0.47 18-19hx0.22 19-20hx0.01 20-21hx0.03 | Ma: 7-8hx0.14 8-9hx0.26 9-10hx0.36 10-11hx0.27 11-12hx0.54 12-13hx0.42 13-14hx0.43 14-16hx0.56 16-17hx0.58 17-18hx0.5 18-19hx0.26 19-20hx0.04 20-21hx0.03 | Me: 7-8hx0.13 8-9hx0.25 9-10hx0.37 10-11hx0.28 11-12hx0.54 12-13hx0.45 13-14hx0.53 14-15hx0.7 15-17hx0.69 17-18hx0.53 18-19hx0.28 19-20hx0.05 20-21hx0.04 | Je: 7-8hx0.15 8-9hx0.29 9-10hx0.4 10-11hx0.3 11-12hx0.56 12-13hx0.45 13-14hx0.49 14-15hx0.61 15-16hx0.59 16-17hx0.6 17-18hx0.49 18-19hx0.27 19-20hx0.05 20-21hx0.04 | Ve: 7-8hx0.13 8-9hx0.27 9-10hx0.39 10-11hx0.31 11-12hx0.53 12-13hx0.47 13-14hx0.53 14-15hx0.68 15-16hx0.7 16-17hx0.71 17-18hx0.56 18-19hx0.33 19-20hx0.09 20-21hx0.06 | Sa: 7-8hx0.07 8-9hx0.26 9-10hx0.54 10-11hx0.48 11-12hx0.47 12-13hx0.52 13-14hx0.78 14-17h 17-18hx0.71 18-19hx0.36 19-20hx0.07 20-21hx0.06 | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-21h | Di: 0',
         [], []),
        ('Local service', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-20h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 8-20h | Di: 0',
         [], []),
    ],
    18: [  # Vestiaires seuls ; feuille VES ; somme des ratios 1
        ('Douches collectives', 0.3, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h 18-20hx0.5 20-21h | Di: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h 18-20hx0.5 20-21h | Di: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Sanitaires vestiaires', 0.5, 0.1, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Circulation Accueil', 0.2, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
    ],
    19: [  # Établissements sanitaires avec hébergement ; feuille EHPAD ; somme des ratios 1
        ('Bureau standard', 0.1, 0.1, 90, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-11h 11-13hx0.57 13-18h 18-19hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-18h 18-19hx0.55 19-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
        ('Circulation Accueil', 0.15, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ('Chambre sans cuisine avec salle de bain', 0.5, 0.063, 90, 0.055, 6.8, 1.02, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5hx0.7 5-6h 6-7hx0.75 7-8hx0.9 8-9h 9-10hx0.9 10-16hx0.75 16-17hx0.85 17-18hx0.9 18-19hx0.95 19-21h 21-24hx0.7',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-5hx0.15 5-21hx0.75 21-24hx0.15',
         [], []),
        ('Sanitaires collectifs', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ('Local service', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ('Salle commune', 0.1, 0.1, 90, 0.055, 6, 0, 'vide',  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-7hx0.35 7-19hx0.8 19-21hx0.35',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-7hx0.35 7-19hx0.8 19-21hx0.35',
         [], []),
    ],
    20: [  # Établissements de santé (partie nuit) ; feuille SAN_N ; somme des ratios 1
        ('Chambre sans cuisine avec salle de bain', 0.2, 0.08, 105, 0.055, 6.8, 1.02, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-7hx0.15 7-22hx0.75 22-24hx0.15',
         [], []),
        ('Douches collectives', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 6-8hx0.5 8-9hx0.25 18-20hx0.5 20-21hx0.25',
         [], []),
        ('Sanitaires collectifs', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ('Circulation Accueil', 0.15, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ('Locaux soins et offices', 0.2, 0.06, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24hx0.5',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24hx0.5',
         [], []),
        ('Bureau standard', 0.15, 0.57, 105, 0.055, 16, 1.7776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-9hx0.57 9-12h 12-14hx0.57 14-18h 18-19hx0.57',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-8hx0.1111 8-9hx0.55 9-18h 18-19hx0.55 19-24hx0.1111',
         [], []),
        ('Aire de production', 0.05, 0.14, 105, 0.055, 5, 5, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], []),
        ("Salle d'attente et de consulation (urgences)", 0.15, 0.4, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 8-9hx0.57 9-12h 12-14hx0.57 14-18h 18-19hx0.57',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-8hx0.1111 8-9hx0.55 9-18h 18-19hx0.55 19-24hx0.1111',
         [], []),
    ],
    21: [  # Établissements de santé (partie jour) ; feuille SAN_J ; somme des ratios 1
        ('Salle de réunion', 0.15, 0.42, 105, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-12hx0.5 12-14hx0.25 14-16hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-9hx0.25 9-12hx0.5 12-14hx0.25 14-16hx0.5 | Sa/Di: 0',
         [], []),
        ('Douches collectives', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         [], []),
        ('Sanitaires collectifs', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         [], []),
        ('Circulation Accueil', 0.25, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 7-17h | Di: 0',
         [], []),
        ('Bureau standard', 0.2, 0.57, 105, 0.055, 16, 1.7776, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-12h 12-14hx0.57 14-16h 16-17hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.1111 7-8hx0.55 8-16h 16-17hx0.55 17-24hx0.1111 | Sa/Di: 0-24hx0.1111',
         [], []),
        ('Aire de production', 0.05, 0.14, 105, 0.055, 5, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-12h 12-14hx0.5 14-18h | Di: 0',
         'Lu/Ma/Me/Je/Ve/Sa: 8-12h 12-14hx0.5 14-18h | Di: 0',
         [], []),
        ("Salle d'attente et de consultation", 0.25, 0.4, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-12h 12-14hx0.57 14-16h 16-17hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.1111 7-8hx0.55 8-16h 16-17hx0.55 17-24hx0.1111 | Sa/Di: 0-24hx0.1111',
         [], []),
    ],
    22: [  # Aérogares ; feuille AER ; somme des ratios 0.999
        ('Espace voyageurs', 0.42, 0.25, 105, 0.055, 5, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.7 6-10hx0.6 10-12hx0.3 12-13hx0.8 13-14hx0.6 14-16hx0.3 16-19hx0.8 19-21hx0.7 21-24hx0.3',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
         [], []),
        ('Circulation Accueil', 0.179, 0.08, 105, 0.055, 2, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.1 6-7hx0.5 7-10hx0.7 10-11hx0.4 11-12hx0.5 12-13hx0.4 13-14hx0.7 14-19hx0.4 19-21hx0.7 21-24hx0.4',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 4-24h',
         ['m1s1', 'm2s1', 'm3s1', 'm4s1', 'm5s1', 'm6s1', 'm7s1', 'm8s1', 'm9s1', 'm10s1', 'm11s1', 'm12s1', 'm1s2', 'm2s2', 'm3s2', 'm4s2', 'm5s2', 'm6s2', 'm7s2', 'm8s2', 'm9s2', 'm10s2', 'm11s2', 'm12s2', 'm1s3', 'm2s3', 'm3s3', 'm4s3', 'm5s3', 'm6s3', 'm7s3', 'm8s3', 'm9s3', 'm10s3', 'm11s3', 'm12s3', 'm1s4', 'm2s4', 'm3s4', 'm4s4', 'm5s4', 'm6s4', 'm7s4', 'm8s4', 'm9s4', 'm10s4', 'm11s4', 'm12s4', 'm3s5', 'm5s5', 'm8s5', 'm11s5'], []),
        ('Commerces', 0.109, 0.12, 105, 0.055, 5, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.1 6-10hx0.7 10-12hx0.4 12-13hx0.8 13-14hx0.7 14-16hx0.4 16-19hx0.8 19-21hx0.7 21-24hx0.4',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-24h',
         [], []),
        ('Bureau standard', 0.143, 0.1, 105, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 7-8hx0.57 8-11h 11-13hx0.57 13-16h 16-17hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-7hx0.11111 7-8hx0.55 8-16h 16-17hx0.55 17-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5', 'm12s4=0.5']),
        ('Sanitaires vestiaires', 0.105, 0.2, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-10hx0.7 10-11hx0.4 11-13hx0.3 13-14hx0.7 14-19hx0.4 19-21hx0.7 21-24hx0.4',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0',
         [], []),
        ('Inspection filtrage', 0.043, 0.33, 105, 0.055, 10, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.7 6-10hx0.6 10-12hx0.3 12-13hx0.8 13-14hx0.6 14-16hx0.3 16-19hx0.8 19-21hx0.7 21-24hx0.3',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 5-6hx0.5 6-19h 19-24hx0.5',
         [], []),
    ],
    23: [  # Industries ou artisanats 3x8h ; feuille IND_3x8 ; somme des ratios 1
        ('Bureau standard', 0.1, 0.1, 105, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-12h 12-14hx0.57 14-17h 17-18hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-17h 17-18hx0.55 18-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m12s4=0.5']),
        ('Aire de production', 0.6, 0.14, 105, 0.055, 2, 2, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], ['m12s4=0.5']),
        ('Circulation Accueil', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], ['m12s4=0.5']),
        ('Sanitaires vestiaires', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], ['m12s4=0.5']),
        ('Douches collectives', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], ['m12s4=0.5']),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         'Lu/Ma/Me/Je/Ve/Sa/Di: 0-24h',
         [], ['m12s4=0.5']),
    ],
    24: [  # Industries ou artisanats 8h à 18h ; feuille IND_8_18h ; somme des ratios 1
        ('Bureau standard', 0.1, 0.1, 105, 0.055, 16, 1.77776, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-9hx0.57 9-12h 12-14hx0.57 14-17h 17-18hx0.57 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 0-8hx0.11111 8-9hx0.55 9-17h 17-18hx0.55 18-24hx0.11111 | Sa/Di: 0-24hx0.11111',
         [], ['m12s4=0.5']),
        ('Aire de production', 0.6, 0.14, 105, 0.055, 2, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m12s4=0.5']),
        ('Circulation Accueil', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m12s4=0.5']),
        ('Sanitaires vestiaires', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Nocc
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m12s4=0.5']),
        ('Douches collectives', 0.05, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m12s4=0.5']),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-18h | Sa/Di: 0',
         [], ['m12s4=0.5']),
    ],
    25: [  # Établissements sportifs municipaux ou scolaires ; feuille GYM_MUN ; somme des ratios 1
        ('Circulation Accueil', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Salle de sport', 0.65, 0.1, 300, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Local service', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Sanitaires vestiaires', 0.15, 0.1, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Douches collectives', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h 18-20hx0.5 20-21h | Di: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h 18-20hx0.5 20-21h | Di: 8-9hx0.5 9-10h 10-11hx0.5 11-12h 12-14hx0.5 14-15h 15-17hx0.5 17-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
    ],
    26: [  # Restaurants scolaires - 1 repas par jour, 5 jours sur 7 ; feuille RES_SCO_1RJ_5J7 ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.77, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 11-12hx0.5 12-13h 13-14hx0.5 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 11-14h | Sa/Di: 0',
         ['m12s4'], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5']),
        ('Cuisine', 0.2, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
         ['m12s4'], ['m8s1=0.5', 'm4s2=0.5', 'm8s2=0.5', 'm8s3=0.5', 'm8s4=0.5']),
        ('Local service', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 9-15h | Sa/Di: 0',
         ['m12s4'], []),
    ],
    27: [  # Restaurants scolaires - 3 repas par jour, 5 jours sur 7 ; feuille RES_SCO_3RJ_5J7 ; somme des ratios 1
        ('Salle restaurant', 0.7, 0.77, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 5-7hx0.25 10-11hx0.25 11-12hx0.8 12-13hx0.5 15-19hx0.25 | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 5-8h 10-13h 15-19h | Sa/Di: 0',
         ['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'], []),
        ('Cuisine', 0.2, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 8-14h 16-19h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 8-14h 16-19h | Sa/Di: 0',
         ['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'], []),
        ('Local service', 0.1, 0, 105, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve: 5-14h 16-22h | Sa/Di: 0',
         'Lu/Ma/Me/Je/Ve: 5-14h 16-22h | Sa/Di: 0',
         ['m1s1', 'm2s1', 'm7s1', 'm8s1', 'm2s2', 'm4s2', 'm7s2', 'm8s2', 'm4s3', 'm7s3', 'm8s3', 'm7s4', 'm8s4', 'm10s4', 'm12s4', 'm8s5'], []),
    ],
    28: [  # Établissements sportifs privés ; feuille GYM_PRI ; somme des ratios 1
        ('Circulation Accueil', 0.1, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Salle de sport', 0.65, 0.1, 300, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Local service', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Sanitaires vestiaires', 0.15, 0.1, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
        ('Douches collectives', 0.05, 0, 90, 0.055, 0, 0, 0,  # unité du tableur : W/Noccnom
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         'Lu/Ma/Me/Je/Ve/Sa: 8-21h | Di: 8-18h',
         ['m1s1', 'm12s4'], ['m8s3=0.5', 'm8s4=0.5']),
    ],
}
```

## 8. Comparaison du tableur converti (JSON) avec le texte

Méthode : les 135 lignes de locaux de la synthèse p. 24 à 26 (usages 3 à 28) ont été relues par position des mots dans le PDF et alignées une à une sur les 135 locaux du JSON, dans l'ordre ; les quatre colonnes (ratio, Noccnom, W/m² en occupation, W/m² hors occupation) ont été comparées à la tolérance de 0,0005, la colonne « hors occupation » étant reconstituée par Q_max_proc x minimum du profil hebdomadaire ; cette reconstitution ne redonne pas la colonne du texte pour les chambres des hôtels 8 et 9, dont le minimum vaut 0 (9 h à 18 h) alors que le texte retient la valeur de nuit (section 8.4). Les consignes et les horaires ont été comparés usage par usage sur la relecture du PDF ; les besoins d'ECS sur le tableau 277 (p. 1053 et 1054), dont les valeurs sont nettes, la colonne ECS de la synthèse étant décalée d'une ligne par l'extraction.

### 8.1 Usage 4, enseignement primaire (p. 24 ; tableau 277 p. 1053 ; feuille ENS_PRI)

Concordant : les six locaux (bureau standard 0,1 / 0,067 / 16 / 1,77776 ; circulation accueil 0,1 / 0 / 0 / 0 ; salle de classe 0,55 / 0,66 / 0 / 0 ; salle de réunion 0,05 / 0,42 / 10 / 0 ; salle de repos 0,15 / 0,66 / 0 / 0 ; sanitaires vestiaires 0,05 / 0 / 0 / 0) ; consignes 19/16/7 et 26/30/30 ; occupation lundi à vendredi 8 h à 17 h ; éclairage et ventilation « idem occupation » ; ECS 0,2 L/semaine/m².
Nuances propres au tableur : « Juillet-août : occupé à 50 % » (p. 24) est porté par les profils annuels des locaux (occupants et apports à 0,5 de m7s1 à m8s5), de la mobilité et de l'ECS, mais pas par l'occupation, la ventilation, l'éclairage ni les consignes de la zone, qui restent à 1 ; « Inoccupé en vacances scolaires hors été » couvre 9 semaines pour l'occupation et les consignes (m1s1, m2s1, m2s2, m4s2, m4s3, m10s4, m11s1, m12s3, m12s4) mais 8 pour la ventilation, l'éclairage et tous les locaux (m12s3 absent) ; le profil de chauffage du vendredi s'arrête à 16 h quand l'occupation et le refroidissement vont à 17 h. Sans incidence sur les occupants (annulés par p_occ) ; incidence sur Ivent, Iecl et les apports des équipements la troisième semaine de décembre.

### 8.2 Usage 13, restaurant en continu (p. 25 ; tableau 277 p. 1054 ; feuille RES_CON)

Concordant en tout : trois locaux (salle restaurant 0,7 / 0,59 / 0 / 0 ; cuisine 0,2 / 0 / 0 / 0 ; local service 0,1 / 0 / 0 / 0) ; consignes 19/16/7 et 26/30/30 ; occupation lundi à dimanche 6 h à 0 h, 52 semaines ; éclairage 5 h à 0 h ; ventilation « idem éclairage » ; ECS 19,5. Le texte ne donne pas la chaleur par occupant (105 W dans le tableur). Particularité sans effet : les tableaux du local service (lundi à vendredi 8 h à 14 h, fermé m12s4) sont ceux d'un restaurant à un repas, alors que la zone ouvre 7 jours sur 7 ; ce local n'a ni occupant ni apport.

### 8.3 Usage 22, aérogares (p. 25 ; tableau 277 p. 1054 ; feuille AER)

Concordant : six locaux (espace voyageurs 0,42 / 0,25 / 5 / 0 ; circulation accueil 0,179 / 0,08 / 2 / 0 ; commerces 0,109 / 0,12 / 5 / 0 ; bureau standard 0,143 / 0,1 / 16 / 1,77776 ; sanitaires vestiaires 0,105 / 0,2 / 0 / 0 ; inspection filtrage 0,043 / 0,33 / 10 / 0 ; somme 0,999 des deux côtés) ; consignes 19/16/16 et 26/30/30 ; occupation lundi à dimanche 6 h à 0 h, 52 semaines ; éclairage 5 h à 0 h ; ventilation « idem éclairage » ; ECS 0,24. Écart interne au tableur : le profil annuel « occupant » de la circulation accueil vaut 0 sur les 52 semaines, de sorte que ses 0,08 occupant par m² ne sont jamais présents alors que la synthèse les prévoit ; les tableaux « apports d'humidité » de cinq locaux valent 0 partout, celui du bureau standard est non nul (hebdomadaire à 1 au maximum, annuel à 1, copie de la feuille des bureaux), sans effet puisque la production d'humidité hors occupants vaut 0 kg/h/m² pour les six locaux. Le libellé « W/Nocc » du bureau standard, copié des bureaux, est sans effet (section 5.3).

### 8.4 Écarts sur les 28 usages

Locaux (quatre colonnes) : 129 locaux sur 135 concordent exactement, la colonne « hors occupation » étant reconstituée par Q_max_proc x minimum du profil hebdomadaire. Six écarts : usage 6, bureau standard (1,76 contre 1,77776) et centre de documentation (0 contre 0,555) ; usage 8, chambre (0 contre 0,6) ; usage 9, chambre (0 contre 1,5725) ; usage 11, salle petits déjeuners (cellule vide contre 44,3 et 4,43) ; usage 12, salle de réunion (cellule vide contre 10). Les six autres cellules vides des usages 11 et 12, lues 0, concordent avec le texte. Détail :
- usage 11, feuille HOT345_J : la cellule « Apports de chaleur hors occupants et éclairage, par unité » est vide pour trois locaux ; le texte (p. 24) donne 0 pour circulation accueil et sanitaires collectifs, et 44,3 W/m² en occupation et 4,43 hors occupation pour la salle petits déjeuners. Le profil t_ch de ce local (0,1 hors plage, 0,5 de 6 h à 7 h et de 9 h à 10 h, 1 de 7 h à 9 h) est celui qui redonne 4,43 à partir de 44,3 : la cellule vide est un oubli du tableur. `_locaux` lit 0 ;
- usage 12, feuille CRE : cellule vide pour cinq locaux ; le texte (p. 25) donne 0 pour circulation accueil, salle de jeux, salle de repos et sanitaires vestiaires, et 10 W/m² pour la salle de réunion (profil 0,25 / 0,5 identique aux autres salles de réunion à 10 W/m²). `_locaux` lit 0 ;
- usage 6, bureau standard : une case à 0,11 au lieu de 0,11111 le samedi de 12 h à 13 h (1,76 au lieu de 1,77776) et une case à 0 dans le centre de documentation au même créneau (0 au lieu de 0,555) : coquilles du tableur, sans incidence mesurable ;
- usages 8 et 9, chambres : la colonne « hors période d'occupation » du texte (p. 24) vaut 0,6 et 1,5725, soit Q_max_proc x la valeur de nuit de t_ch (4 x 0,15 ; 4,625 x 0,34, de 0 h à 6 h et de 23 h à 24 h), alors que le minimum hebdomadaire de t_ch vaut 0 (9 h à 18 h, zone inoccupée). Aucun écart de valeur entre le tableur et le texte, seule la définition de la colonne change pour ces deux locaux ; le dict LOCAUX porte 0,6 et 1,5725.

Besoins d'ECS : 25 usages sur 26 concordent avec le tableau 277. Écart : usage 16, restaurants 2 repas par jour 6 jours sur 7, 4,7 L/semaine/m² dans le tableur, 19,5 dans le tableau 277 (p. 1054) et dans la synthèse (p. 25). La valeur 19,5 est celle de l'usage 13 ; 4,7 est proche de 5,3 x 6/7 = 4,54 (usage 15 ramené à six jours). Le texte et le tableur se contredisent ; aucun des deux n'est validable.

Consignes : les 28 usages concordent avec la synthèse.

Horaires et semaines : écarts entre la synthèse (p. 24 à 26) et le tableur, ou entre tableaux d'une même feuille :
- usages 18, 25 et 28 : « Inoccupé 1 semaine en décembre » dans le texte ; le tableur ferme m12s4 et aussi m1s1 (deux semaines) sur tous les profils de zone et de locaux ;
- usage 18 : ventilation « idem occupation » dans le texte (8 h à 21 h, dimanche 8 h à 18 h) ; le tableur la prolonge d'une heure (8 h à 22 h, dimanche 8 h à 19 h) ;
- usage 5 : l'occupation ferme 8 semaines, les consignes passent à -1 sur 9 (m12s3 en plus) ; même mécanique que l'usage 4 inversée ;
- usage 7 : zone « 52s/an » dans le texte et dans les profils de zone du tableur, mais les locaux d'enseignement (salle de classe, amphithéâtre, salle informatique, local service) sont fermés 9 semaines (m1s1, m2s2, m4s2, m4s3, m6s3, m6s4, m9s1, m9s2, m12s4) et à 0,5 en juillet et août, les bureaux et salles de réunion à 0,5 sur 11 semaines : tableur seul ;
- usage 12 : zone « 52s/an », mais locaux, mobilité et ECS à 0,5 pendant les 16 semaines de vacances scolaires (été compris) : tableur seul ;
- usage 26 : la zone ferme 16 semaines, les locaux seulement m12s4 ; sans effet (p_occ annule les occupants, apports à 0 W) ;
- usages 23 et 24 : « dernière semaine de l'année occupée à 50 % » codé 0,5 sur tous les profils annuels, y compris chauffage et refroidissement (section 9).

## 9. Points ouverts

Ce que le texte ne tranche pas, ou que le tableur et le texte tranchent différemment. Se décidera au banc des bureaux pour ce qui touche l'usage 3, et restera non validé pour 4 à 28.

1. Usage 16, besoin d'ECS : 4,7 (tableur) ou 19,5 (tableau 277 p. 1054 et synthèse p. 25). Proposition : coder la valeur du tableur, qui est la source approuvée (p. 1409), et conserver 19,5 en commentaire avec la référence.
2. Cellules vides des usages 11 et 12 : coder les valeurs du texte (44,3 W/m² pour la salle petits déjeuners de 11, 10 W/m² pour la salle de réunion de 12, 0 pour les six autres), puisque la synthèse les donne explicitement et que les profils du tableur sont construits pour elles ; marquer la surcharge dans le code. Le moteur lit 0 aujourd'hui.
3. État 0,5 des consignes (usages 23 et 24, m12s4) : le tableau 5 (p. 58) ne connaît que -1, 0 et 1. `_consignes` (l. 75 à 77) envoie 0,5 sur la consigne d'arrêt de plus de 48 h (7 °C) toute la dernière semaine, alors que la zone est occupée à 50 % (occupation 0,5 > 0). Proposition : ramener à 1 (confort) toute valeur strictement comprise entre 0 et 1 des profils annuels de chauffage et de refroidissement.
4. Valeurs fractionnaires de ventilation et d'éclairage (0,5 pour 17 de 6 h à 7 h, 0,35 pour 20 hors 5 h à 21 h, 0,5 pour 23 et 24 la dernière semaine) : le texte définit Ivent et Iecl comme des booléens (p. 53 et 54). Le moteur teste `> 0` (`groupe.py` l. 223, `eclairage.py` l. 107 et 138, `ventilation.py` l. 83), donc 0,35 vaut 1. Rien dans le texte ne dit si l'éclairage « réduit » de l'usage 20 doit pondérer la consommation ; garder le booléen.
5. Chaleur par occupant 105 W (12 à 17, 20 à 24, 27) et 300 W (salles de sport de 25 et 28) : tableur seul ; le texte ne chiffre que 90 W et 63 W (p. 20). Coder le tableur.
6. Humidité hors occupants : annoncée non nulle en tertiaire (p. 22), 0 partout dans le tableur. Coder 0 ; le bilan hydrique (fiche 8.3) n'est pas dans le moteur.
7. Semaines fermées discordantes (usages 4, 5, 18, 25, 28) et semaines des locaux (7, 12, 26) : coder le tableur tel quel, tableau par tableau, sans harmoniser ; noter les écarts avec le texte dans `docs/lectures.md`.
8. Circulation accueil des aérogares sans occupant toute l'année (profil annuel nul) alors que la synthèse donne 0,08 occupant par m² : coder le tableur ; signaler.
9. Ratios des locaux saisis : la fiche 4.1 en fait un paramètre d'intégration, le tableur et la synthèse des valeurs par défaut. Le champ du RSEE qui les porte pour les usages 4 à 28 n'a pas été vu ; `eclairage.py` lit `Rat_local` et `Locaux_Bureau` sur les entrées `Eclairage` des groupes de bureaux. À trancher sur un RSEE : si ces entrées existent pour tous les usages avec un code de type de local (liste des types de locaux p. 474 et 475 ; tableau 78 p. 488 à 491), `tertiaire` doit accepter des ratios saisis en place des défauts.
10. Groupes multiples dans une zone : les équations 39 et 42 pondèrent par Rat_gr ; le banc le fait (`banc/besoins.py` l. 47 à 49, `banc/cep.py` l. 56 à 58) avec le scénario construit sur la surface de la zone. Juste si tous les groupes ont les mêmes ratios de locaux ; à revoir avec le point 9.
11. 365e jour : lundi ordinaire de la semaine 1 (`calendrier.py` l. 36 à 39, déduit des RSEE d'habitation) ; valable pour tous les usages faute de texte.
12. Nocc_zn du récapitulatif (fiche 13.6) : balise à identifier dans le RSEE pour écrire Cep_annuel_par_occ ; hors thème.
13. Partie nuit et partie jour des hôtels et établissements de santé : le texte ne dit pas comment répartir les surfaces ni les systèmes entre les deux zones ; c'est une saisie. Rien à coder, à documenter dans l'aide à la saisie.
14. Iocc_gpm (équations 50 à 53) non produit : nécessaire à la fiche 5.9 pour distinguer l'inoccupation de jour (0) de la nuit et des vacances (-1) ; thème protections mobiles, mais la sortie relève de `scenarios`.
15. Débits conventionnels du Bbio : le texte les donne pour les usages 3 à 28, fiche 6.2 C_VEN_Bouche_conduit, § 6.2.3, p. 334 et 335, « cas des usages hors maison individuelle ou accolée et hors logement collectif » : en occupation q_max = Param_occupation x SREF_gr (équations 399 reprise et 402 soufflage), en inoccupation q_min = max(60 ; Param_inoccupation x SREF_gr) (équations 405 et 408), avec le tableau 56-1 (p. 335) ci-dessous ; Crdbnr = 1 pour le Bbio (p. 335). `groupe.py` l. 27 et 28 (`DEBIT_CONVENTIONNEL`, `DEBIT_INOCCUPATION`) ne connaît que les bureaux : seul le codage manque, le Bbio tertiaire est calculable dès que la table y est. Usages 1 et 2 : cas distinct p. 335, par renvoi aux équations des débits d'hygiène (le texte cite le § 6.2.3.2.2.1 sous « Cas des usages maison individuelle ou accolée et logement collectif », puis le § 6.2.3.2.2.2 dans le paragraphe sur le Bbio), déjà codé et validé. Thème ventilation.

    ```python
    # Tableau 56-1 (p. 335) : usage -> (Param_occupation, Param_inoccupation), m³/h par m² de SREF du groupe ;
    # équations 399 et 402 (occupation), 405 et 408 (inoccupation, plancher 60 m³/h), p. 334. Usages 1 et 2 : non spécifié ici (cas distinct p. 335).
    PARAM_DEBITS_BBIO = {
        3: (4, 0.42), 4: (7.2, 0.38), 5: (4.7, 0.38), 6: (5.6, 0.46), 7: (7.4, 0.6),
        8: (3, 3), 9: (2, 2.2), 10: (8, 0), 11: (7, 0), 12: (4.7, 0.75),
        13: (10, 0.5), 14: (10, 0.5), 15: (10, 0.5), 16: (10, 0.5), 17: (3.7, 0),
        18: (6.7, 6.7), 19: (4.5, 4.5), 20: (4.5, 4.5), 21: (4.5, 0), 22: (4, 0.3),
        23: (3.1, 0), 24: (3.1, 0), 25: (3, 0), 26: (8, 0.3), 27: (8, 0.3), 28: (3, 0),
    }
    ```
16. Exigences : `exigences.py` l. 16 n'a Bbio_max moyen que pour 1 à 5 ; thème exigences.
17. Éclairage des locaux des usages 4 à 28 : `eclairage.py` l. 45 ne porte que les quatre locaux des bureaux (tableau 78 p. 488 à 491, C1 et Eiref par usage et type de local ; liste des types de locaux p. 474 et 475 ; tableau 79 p. 497, points de référence de C2) ; thème éclairage.

## 10. Où coder

Fichiers sous `openbce/openbce/` sauf mention ; lignes du 09/10/2026.

- `scenarios.py` l. 22, `USAGES` : inchangé (1 à 28).
- `usages.py` l. 11 à 42 (`NOMS`, `VALIDES`), qui porte déjà la table des 28 usages du moteur : ajouter à côté de `NOMS` les deux constantes du tableau 4 (p. 57), `USAGES_HEBERGEMENT = frozenset({1, 2, 8, 9, 19, 20})` et `USAGES_ENSEIGNEMENT = frozenset({4, 5, 7, 26, 27})`, avec deux fonctions `ihebergement(usage)` et `ienseignement(usage)` ; `scenarios.py` importe `ienseignement` pour `iecs` (`usages.py` n'importe rien, pas de cycle).
- `scenarios.py` l. 55 à 72, `Scenario` : ajouter `humidite_occupants` (kg/h, équation 40), `humidite_usages` (kg/h, équations 43 et 44), `mobilite` (équation 31), `ivac` (équation 48, profil annuel d'occupation étalé sur l'année), `iecs` (équation 47, booléen par heure : 0 si ienseignement et ivac = 0), `iocc_gpm` (équations 50 à 53, entier -1, 0, 1). Tous sont des séries de 8 760 valeurs, à défaut `None` pour ne pas casser `habitation`.
- `scenarios.py` l. 75 à 77, `_consignes` : ramener à 1 les états strictement entre 0 et 1 avant la sélection (point 3), ou le faire dans `tertiaire` sur `ch` et `fr` (l. 132 et 133) : `ch = np.where((ch > 0) & (ch < 1), 1.0, ch)`.
- `scenarios.py` l. 101 à 123, `_locaux` : (a) distinguer la cellule vide de la valeur 0 : le scalaire « Apports de chaleur hors occupants et éclairage, par unité » est absent de la liste pour les locaux à cellule vide (le convertisseur, `outils/scenarios_xlsx.py` l. 82 et 83, ne l'émet pas) ; lever un avertissement ou appliquer une table de surcharges `SURCHARGES_TEXTE = {(11, "Salle petits déjeuners"): 44.3, (12, "Salle de réunion"): 10.0}` documentée avec la page (p. 24 et 25), les six autres restant à 0 (point 2) ; (b) lire aussi le scalaire « Humidité dégagée par un occupant » (kg/h/occ) et « production d'humidité hors occupants et éclairage, par unité » (kg/h/m²), et le troisième tableau du local (« Apports d'humidité ») dans `t_humidite` ; (c) accepter un paramètre optionnel `ratios: dict[str, float] | None` pour remplacer `ratio` par les valeurs saisies quand le RSEE les porte (point 9), sans changer le défaut.
- `scenarios.py` l. 126 à 150, `tertiaire` : calculer en plus `humidite_occupants += n * l["kg_h_occupant"]` et `humidite_usages += aire * l["kg_h_usages"] * h * a` (équations 40, 43 et 44, avec Rat_gr appliqué par l'appelant comme aujourd'hui pour les apports) ; produire `mobilite` par `produit("mobilit")` ; `ivac` à partir du profil annuel d'occupation seul (deuxième élément de `_horaire(cal, _tableau(usage, "occupation"))`) ; `iecs = 1 - ((ivac == 0) & ienseignement)` ; `iocc_gpm` selon les équations 50 à 53 (creux d'inoccupation encadrés entre 7 h et 22 h en heure légale, `cal.case`, à 0 ; le reste de l'inoccupation à -1 ; combiné par `np.minimum` avec le profil annuel codé -1 quand p^a_occ = 0). Les usages 1 et 2 passent par `habitation` (l. 80 à 98) : y ajouter les mêmes sorties avec les tableaux « Apports d'humidité » du local d'habitation (0 kg/h) et la mobilité.
- `scenarios.py` l. 3 à 10, docstring : dire que les usages 4 à 28 sont codés sur le tableur sans RSEE de référence, et renvoyer à `specs/usages/scenarios-locaux.md`.
- `calendrier.py` : rien d'obligatoire. Utile : une fonction `semaine_annee(cal)` (0 à 51) et `jour_annee(cal)` pour exprimer `iecs(j)` par jour (équation 47 est indexée par j) ; `construire` l. 31 à 46 et `adultes_equivalents` l. 49 à 61 inchangés ; conserver le commentaire des l. 36 à 38 sur le 365e jour et l'étendre aux usages 4 à 28 (point 11).
- `ecs.py` l. 23, `A_TERTIAIRE = {3: 1.25}` : compléter avec le tableau 277 (p. 1053 et 1054) ou lire le scalaire « nombre de litres d'eau à 40°C puisés par semaine et par unité » du JSON via `scenarios._scalaire(usage, "nombre de litres")` ; usage 16 : valeur du tableur 4,7 avec le commentaire « texte 19,5 » (point 1) ; l. 26, `RAT_DOUCHES_BAINS` : valeurs conventionnelles p. 1610 (équation 2982 : 80 % maisons et logements collectifs, 90 % hôtels partie nuit, hébergement et établissements sportifs, 50 % petite enfance et bureaux ; non spécifié pour les autres usages) ; le commentaire « tableau 275 » du code renvoie au tableau des gains selon le type d'appareil sanitaire (p. 1047, fiche 9.5), à rectifier ; hors thème, à compléter par le thème ECS avant tout calcul de corr. `cle_horaire` l. 61 à 71 fonctionne déjà pour 1 à 28.
- `groupe.py` l. 27 et 28, `DEBIT_CONVENTIONNEL = {3: 4.0}` et `DEBIT_INOCCUPATION = {3: (60.0, 0.42)}`, lus l. 136 à 138 : étendre aux usages 3 à 28 avec le tableau 56-1 (p. 335, dict `PARAM_DEBITS_BBIO` du point 15), `DEBIT_CONVENTIONNEL[u] = Param_occupation` et `DEBIT_INOCCUPATION[u] = (60.0, Param_inoccupation)` ; thème ventilation (point 15). L. 180, `occupe = sc.occupation[h] > 0` : lire `sc.iocc_gpm` quand les protections mobiles en auront besoin (point 14). L. 223, `sc.ventilation[h] > 0` : inchangé.
- `banc/besoins.py` l. 36 et `banc/cep.py` l. 49 et 88 (`if usage not in (1, 2, 3):`) : lever le filtre et marquer les lignes des usages 4 à 28 « non validé » dans les sorties avec `usages.non_valides()` ; le mécanisme existe dans `usages.py` (`VALIDES = frozenset({1, 2, 3})` l. 42, `non_valides()` l. 49, `avertissement()` l. 54), `api.py` l. 50 (`usages_non_valides`, `avertissement`) et `docs/schemas/resume.schema.json` l. 88 ; `sortie_rsee.py` ne porte rien sur les usages non validés.
- `outils/scenarios_xlsx.py` l. 82 à 85 : émettre le scalaire avec `"valeur": None` quand la cellule « Watts/unité » ou « kg/h/unité » est vide, au lieu de l'omettre, pour que `_locaux` voie la différence (point 2) ; puis régénérer `tables/scenarios_officiels.json`.
- `tests/test_scenarios.py` : ajouter, pour chaque usage 4 à 28, un test de forme (8 760 valeurs, somme des ratios 1 ou 0,999, occupants nuls hors occupation de zone, consignes dans l'ensemble des trois valeurs) et trois tests de valeurs tirés de la section 8 : usage 4 (479,20 occupants au maximum pour 1 000 m², atteints de 14 h à 16 h les lundi, mardi, jeudi et vendredi : 0,55 x 0,66 + 0,15 x 0,66 + 0,05 x 0,42 x 0,5 + 0,1 x 0,067 par m² ; 471,07 de 13 h à 14 h, la salle de réunion étant à 0,25 et le bureau standard à 0,57 ; 1 850,0 W d'équipements au maximum, de 10 h à 12 h et de 14 h à 16 h, soit 0,1 x 16 + 0,05 x 10 x 0,5 par m²), usage 13 (330,40 occupants au maximum, 0 W d'équipements), usage 22 (122,37 occupants au maximum, de 16 h à 17 h en semaine ; 5 721,0 W d'équipements au maximum, de 8 h à 16 h) ; valeurs recalculées avec `scenarios.tertiaire` le 09/10/2026 ; marquer ces tests « non validés, tableur seul ».
- `docs/lectures.md` : une ligne par point ouvert de la section 9 retenu au codage.
