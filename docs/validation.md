# Validation : protocole, résultats, limites

## Réserves, à lire avant tout usage des résultats

- OpenBCE n'est pas un logiciel évalué au sens du règlement d'évaluation des logiciels RE2020. Ses résultats ne sont
  pas opposables, ne peuvent fonder ni une attestation ni une étude réglementaire, et ne remplacent pas le calcul d'un
  logiciel approuvé.
- L'objectif de recette fixé au départ (moins de 1 % d'écart par indicateur, par bâtiment et par zone) n'est pas
  atteint sur les consommations. Il l'est sur une partie des besoins.
- Les références de comparaison sont des sorties de logiciels évalués, pas des mesures : un accord avec elles montre
  qu'OpenBCE reproduit le moteur de référence, pas que le bâtiment consommera ce qui est calculé.
- Plusieurs lectures du texte ont été tranchées au banc ([lectures.md](lectures.md)). Elles peuvent être fausses sur
  des cas que le banc ne contient pas.
- Des pans de la méthode ne sont pas codés (voir [methode.md](methode.md)) : un projet qui en relève est soit refusé,
  soit calculé avec la valeur de la référence prise au prorata et signalée comme telle.

## Protocole

Le banc compare, poste par poste, ce que calcule OpenBCE aux sorties que porte le même RSEE, calculées par le logiciel
évalué qui l'a produit. Les entrées sont identiques ; seul le moteur change.

- **Corpus** : 223 RSEE de 54 opérations réelles (222 lisibles), produits entre 2022 et 2025 par des logiciels évalués
  dans le cadre d'études réglementaires d'un bureau d'études. Logement individuel et collectif en majorité, quelques
  bureaux. Ces fichiers sont des données de projets : ils ne sont pas publiés. Dans la documentation et le code, chaque
  opération est désignée par un repère neutre (« cas 01 », « cas 02 »...).
- **Grandeurs comparées** : sorties annuelles et mensuelles par groupe, zone et bâtiment (besoins Th-B, consommations
  Th-C par poste et par énergie, Cep, DH, seuils et modulations).
- **Mesure de l'écart** : écart relatif au résultat de référence, résumé par la médiane, la médiane des écarts absolus
  et le nombre de cas dans ±1 %, ±5 % et ±10 %.
- **Limites du protocole** : les RSEE ne donnent que des valeurs annuelles et mensuelles ; quand deux explications d'un
  écart donnent les mêmes totaux, le banc ne peut pas les départager. Les références proviennent de plusieurs versions
  du moteur de référence (voir [rsee.md](rsee.md)).

## Résultats au 09/10/2026

| Indicateur | Périmètre | Résultat |
|---|---|---|
| Surfaces et déperditions par transmission | 732 zones | 99 à 100 % dans la tolérance de 1 % |
| Bbio, logement | 167 zones | écart médian +0,1 % ; 160 zones dans ±5 % |
| Bbio, bureaux | 3 opérations | dans ±1 % |
| Bbio_max et modulations | 732 groupes | Mbgeo exact partout ; DH_max exact sur 761 groupes |
| Besoins d'eau chaude sanitaire | 182 groupes | rapport médian 1,002 à 1,003 |
| DH, confort d'été | 12 groupes de 8 opérations | 8 dans ±10 %, biais de +10 à +15 % ; rafraîchissement adiabatique non modélisé |
| Cep | 50 opérations (électricité, gaz, réseaux) | hors production locale : écart médian -0,2 %, écart absolu médian 1,5 %, 34 dans ±5 %, 49 dans ±10 % ; avec l'autoconsommation photovoltaïque, contre O_Cep_annuel (valeur réglementaire) : écart médian -0,1 %, écart absolu médian 2,4 %, 49 dans ±10 % (10/10/2026) ; seule hors de ±10 % : une opération dont le RSEE est incohérent (mensuels sans rapport avec l'annuel) |

Le bilan du Cep est reproductible avec `python -m banc.cep_lot <dossier de RSEE>`.

## Écarts connus et non expliqués

- **Froid des logements climatisés en mode Th-C** : -13 à -33 % alors que le besoin Th-B est exact. Deux composantes :
  le démarrage de la saison de froid (certaines références démarrent au 1er juillet sans déclenchement préalable, le
  critère n'est pas identifié) et un niveau d'été trop bas de 14 à 17 %, probablement lié au débit d'air neuf des
  zones traversantes (flux du vent au travers des entrées d'air).
- **Chauffage en mode Th-C** : excès de demi-saison sur certaines opérations (+16 à +32 %), saison de chauffage plus
  courte sur une autre (-23 %).
- **PAC double et triple service** : +20 à +25 % de chauffage sur deux opérations à la lettre du texte (équation 1294).
- **Auxiliaires de ventilation** : la référence semble majorer la puissance des ventilateurs d'un facteur proche de
  (débit + fuites) / débit ; non codé.
- **RSEE de sortie** : consommations réparties entre groupes au prorata des besoins, gaz imputé au chauffage ; pas de
  validation contre un schéma officiel.

Ces écarts sont détaillés dans le tableau ci-dessous et dans les commentaires des modules.

## Détail par brique

| Brique | État | Mesure |
|---|---|---|
| Lecture d'un RSEE (entrées, sorties) | fait | 222 RSEE lus sur 223 |
| Surfaces et déperditions par transmission | fait | 732 zones, 99 à 100 % dans la tolérance de 1 % |
| Climat, rayonnement, masques lointains et proches | fait | - |
| Scénarios conventionnels (28 usages) | fait | tableur officiel du 29/04/2026 converti par `outils/scenarios_xlsx.py` |
| Infiltrations (bilan de pression de la zone) | fait | 86 zones, écart médian de 3 % sur l'indicateur hivernal |
| Besoin de chauffage du logement | fait | 159 zones, écart médian +1 %, 150 dans ±5 %, 158 dans ±10 % |
| Éclairage du logement | fait | 159 zones, écart médian -1 %, 148 dans ±5 % ; compteurs d'heures identiques à ceux des RSEE |
| Besoin de froid (saisons, ouverture des baies) | fait | 159 zones, écart médian +0,1 kWh/m², écart absolu médian 0,2 |
| Bbio du logement | fait | 167 zones : écart médian +0,1 %, 160 dans ±5 % (mesure du 08/10/2026, voir le résumé) |
| Stores enroulables | fait | essai sur 4 projets, Bbio entre -4,3 % et +3,9 % |
| Stores vénitiens, espaces tampons vitrés | à faire | - |
| Usages 4 à 28 (enseignement, hôtels, restauration, commerces, santé, industrie, sport...) | codé, non validé (sauf les seuils des usages 4 et 5, validés sur l'OPEE) | tables de l'annexe III lues et contre-lues (`specs/usages/`) : débits conventionnels (tableau 56-1), éclairage par local (tableau 78), ECS (tableau 277), ouverture des baies (tableau 43), exigences (annexe R. 172-4) ; aucun récapitulatif de référence, le résumé porte un avertissement |
| Confort d'été (DH, mode Th-DC) | en cours | `groupe.calculer(thd=...)`, `banc.confort` : 12 groupes de 8 projets, écart médian nul, écart absolu médian 77 °C.h, 8 dans ±10 % |
| Bbio_max, Cep,nr_max, Cep_max, DH_max (annexe R. 172-4) | fait pour les usages 1 à 5 | `exigences.py` ; `banc.exigences` sur les RSEE du lot (Mbgeo juste sur 732 groupes, DH_max sur 761) ; `banc.opee_exigences` sur les données ouvertes de l'observatoire OPEE (113 016 zones, août 2026) : Mbgeo et Mcgeo 100 %, Bbio_maxmoyen, Cep,nr_maxmoyen et Cep_maxmoyen retrouvés à 100 % (99,8 % en collectif), Mbsurf_tot et Mcsurf_tot 100 % en enseignement, DH_max 100 % ; usages 6 à 28 : tables lues dans le texte, aucun RSEE déposé avant août 2026 |
| Consommations (Cep) | en cours | voir ci-dessous ; spécifications du lot 2 dans `specs/` |
| Poêles et inserts à bois (fiche 8.22) | fait | `banc.pac_chauffage` : deux projets, bois +4 % et -11 % contre O_Cef_ch_bois_annuel (la part du besoin confiée au poêle suit Rat_s_ch, sans variation temporelle propre à l'émetteur) |
| Production photovoltaïque (fiches 12.1 à 12.4) | fait | `photovoltaique.py`, `banc.pv` : 17 bâtiments de 11 opérations, rapport calcul/RSEE médian 1,002, 15 dans ±2,1 % ; deux toitures ouest et nord à face arrière confinée à +11 %, cause non trouvée (`brut/pv_lot1.txt`) ; autoconsommation (13.4, minimum horaire par bâtiment de la production et de la consommation électrique tous usages) : part autoconsommée 2,29/2,28 et 5,00/4,98 kWh/m² sur deux opérations à plusieurs bâtiments |
| Carbone | à faire | - |

Mesure faite sur un fichier par projet (46 projets de logement). Les valeurs que le texte réglementaire ne donne pas
sont déduites des RSEE par le banc et consignées comme telles dans le code.

Les seuils et modulations sont aussi confrontés aux données ouvertes de l'observatoire de la performance énergétique et
environnementale (OPEE, data.gouv.fr, table « zone » de l'archive d'août 2026, 113 016 zones d'usages 1 à 5) par
`python -m banc.opee_exigences zone.csv projet.csv`. Deux enseignements : la modulation Mcgeo des maisons en H2d et H3
sous 400 m valait -0,15 et -0,20 pour les permis déposés avant 2025 (`MCGEO_AVANT_2025`), et la colonne Mccat de l'OPEE est
vide sur quelques zones de catégorie 2 dont le seuil publié contient pourtant la modulation du texte. Reste ouvert : dix zones
de bureaux en catégorie 3 portent un Mbbruit compris entre 0,05 et 0,38, sans doute un prorata des surfaces de groupe en
catégorie 3 que le moteur ne fait pas (il applique 0,4 à la zone).

### Consommations (Cep), poste par poste

Le Cep se construit poste par poste, chacun confronté à la sortie correspondante des RSEE (`Sortie_Batiment_C`).
Cep = somme des énergies finales importées x coefficient d'énergie primaire (électricité 2,3 ; bois 1 et 0 en non
renouvelable ; réseau 1 et 1 - RatENR ; fossiles 1), hors usages mobiliers (équations 2488 à 2490).

| Poste | Module | Banc | État |
|---|---|---|---|
| Besoins d'ECS | `ecs.py` | `banc.ecs` | 182 groupes, rapport médian 1,002 à 1,003 sur `O_B_Ecs_annuel` (besoins bruts, équation 1695 ; clé de puisage du tableur officiel) |
| Éclairage | `eclairage.py` | `banc.besoins` | logement fait avec le Bbio |
| Déplacement : ascenseurs | `ascenseurs.py` | `banc.ascenseurs` | 9 zones sans parking dans ±0,1 kWh/m² |
| Déplacement : parkings | `parkings.py` | `banc.deplacement` | 157 zones : 123 dans ±0,1 kWh/m², 143 dans ±0,3 |
| Auxiliaires de ventilation | `ventilateurs.py` | `banc.ventilateurs` | simple flux résidentiel : 151 groupes sur 181 dans ±0,05 kWh/m² ; l'écart restant vient des brasseurs d'air (fiche 8.32), à faire avec la boucle thermique du mode Th-C ; double flux et tertiaire à faire |
| Auxiliaires de ventilation (tous usages) | `consommation.py` | `banc.cep` | 20 groupes à ±0,1 kWh/m² |
| Éclairage tertiaire avec saisies | `eclairage.py` | `banc.cep` | cas 01 7,15 / 7,2 |
| Besoins Th-C aux émetteurs (chauffage, froid) | `emission.py`, `ventilation.py`, `groupe.calculer(thc=...)` | `banc.cep` | chauffage : 43 groupes effet joule, médiane +5 %, écart absolu médian 19 % (débits de ventilation réels mal lus) ; froid sous-estimé |
| Bilans, Cep, usages mobiliers, forfait de refroidissement | `bilans.py` | `banc.bilans` | identités Cep sur 267 nœuds, mobilier 169 zones, forfait 138 groupes : justes |
| ECS : distribution du groupe et intergroupe (bouclage, traceur, circulateur), ballon, PAC d'ECS, appoint joule | `ecs_distribution.py`, `ballon.py`, `generateurs_ballon.py` | `banc.ecs_cef`, `banc.ecs_lot` | lot de 33 projets : écart médian -1,1 %, |écart| médian 2,3 %, 32 dans ±10 % (cas 02 -50 % à expliquer) |
| PAC électriques chauffage et froid (8.23) : air ext/eau, air ext/air recyclé, multiservices | `thermodynamique.py` | `banc.pac_chauffage` | air/air : cas 01 +7 %, cas 03 +7 %, cas 04 -18 % (besoins) ; air/eau avec réseaux : cas 05 +0 %, cas 06 +8 %, cas 07 +11 %, cas 08 +29 % |
| Distribution hydraulique (8.7 à 8.10) et pertes récupérables rebouclées heure par heure dans le modèle thermique (11.1) | `distribution.py`, `groupe.py` | `banc.pac_chauffage` | cas 05 +0 %, cas 09 -2 %, cas 10 +1 %, cas 08 +0 % |
| PAC double et triple service (8.23, 1294) : le temps d'ECS réduit la puissance fournie, lettre du texte (le COP de chauffage baisse au prorata) | `thermodynamique.py` | `banc.pac_chauffage` | cas 05 -0 %, T.ONE triple service -7 à -9 % ; cas 06 +25 % et cas 08 +20 % (la réduction de Pabs, option `MULTISERVICE_PABS_REDUIT`, les ramène à +5 et 0 % mais casse les autres) |
| Froid réel des groupes climatisés : besoins Th-C (pas d'ouverture des baies, cible brute (803)), PAC mode froid | `groupe.py`, `thermodynamique.py` | `banc.pac_froid` | bureaux cas 11 : besoin 17,1 pour 18,7 ; cas 03 et cas 04 (PAC air/air) à remesurer |
| Réseaux de chaleur et de froid (8.28) : sous-station en génération ou en base de ballon, énergie « réseau » | `reseau_fourniture.py` | `banc.cep_total` | cas 11 bureaux (réseau de froid) : froid 17,1/18,7 ; cas 12 (réseau de chaleur en base de ballon, 3 bâtiments) : Cep -1 % (chauffage -10 %, ECS +5 %) |
| Relances (8.5) : durées selon Type_Pgrm et l'indicateur de consigne du scénario | `emission.py`, `scenarios.py` | `banc.cep` | tests unitaires |
| Double flux : statut de l'efficacité d'échangeur (certifié 2, justifié 1, déclaré 0), bypass selon θext et θi (6.3) | `ventilation.py`, `groupe.py` | `banc.cep` | cas 13 (ε 0,8) : besoin Th-C 8,1 -> 7,4 pour 6,4 |
| Chaudières gaz et fioul (8.19) : rendements, pertes à l'arrêt, auxiliaires, ECS instantanée + chauffage, base ou appoint de ballon | `chaudiere.py`, `generateurs_ballon.py` | `banc.pac_chauffage`, `banc.ecs_cef` | 12 projets gaz (chauffage + ECS) : tous dans ±7 % ; ballon à base chaudière cas 14 -0 % ; assemblage à deux ballons (type 2) : cas 15 ECS -11 % |
| Cep complet d'un projet (chauffage, froid, ECS, éclairage, auxiliaires, forfait froid, déplacements lus) | tous | `banc.cep_total`, `banc.cep_lot` | lot de 50 projets (électricité, gaz, réseaux) au 09/10/2026 : écart médian -0,2 %, \|écart\| médian 1,5 %, 34 dans ±5 %, 49 dans ±10 % ; hors : cas 15 (RSEE incohérent) ; cas 16 (ECS d'un ballon sans source dans le RSEE) prise de la référence et signalée, à -3 % |
| Génération : contrat d'appel, effet joule direct (8.18) | `generateurs.py` | `banc.chauffage_mois` | identité vérifiée : O_Cef_ch = O_B_Ch sur 46 groupes effet joule du lot |
| Besoin de chauffage Th-C (ventilation réelle, fuites de conduits, émission, relance) | `groupe.py`, `ventilation.py` | `banc.chauffage_mois` | 47 groupes effet joule : collectifs dans ±4 % après lecture « par défaut » de la classe d'étanchéité 3 ; restent les maisons de cas 17 (+9 à +13 %), cas 18 (+16 à +29 %) et cas 13 (+16 %) |
| Consignes corrigées Th-C (8.1) : θvt appliqué seulement aux émetteurs de statut 2 (valeur par défaut écrite), θvs non appliqué, cibles de puissance corrigées en chaud et en froid | `emission.py`, `groupe.py` | `banc.cep` | tranché au banc contre la lettre du texte : bureaux cas 11 36,4/36,2, cas 19 +6 %, cas 04 +4 à +11 %, cas 03 +2 %, effet joule cas 20 +0/-3 % ; froid des logements climatisés encore -13 à -33 % |
| Sortie RSEE : bloc Sortie_Projet (B, C, D) écrit depuis les résultats, RSEE d'entrée recopié | `sortie_rsee.py` | `banc.sortie_rsee` | première version ; pas de XSD dans le corpus, validation tierce à faire |
| Chauffage et froid : distribution, génération | à faire | | `specs/distribution.md`, `specs/generation.md`, `specs/pac_elec.md`, `specs/generateurs_simples.md` |

Lectures déduites des RSEE, que le texte ne donne pas : le poste « déplacement » contient les parkings ; le nombre
de personnes des ascenseurs est le nombre d'adultes équivalents ; l'énergie d'un aller-retour d'ascenseur est la
moyenne d'une montée et d'une descente. Cas non expliqués : ascenseurs de cas 21 et du bâtiment A de cas 22 (sous leur
veille par défaut), cas 23, bâtiment D de cas 18, cas 08.

