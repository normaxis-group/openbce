# openBCE

Moteur de calcul libre de la méthode Th-BCE 2020 (RE2020), écrit à partir de l'annexe III de l'arrêté du 4 août 2021
modifié, telle qu'elle est publiée. Droits : ARKEMEP. Licence : AGPL-3.0-or-later (voir `LICENSE`).

openBCE n'est pas un logiciel évalué au sens du règlement d'évaluation des logiciels RE2020 : ses résultats ne sont pas
opposables, il ne produit pas d'attestation et ne remplace pas un logiciel approuvé. Il sert à relire, contrôler et
comprendre un calcul réglementaire. Le code est fourni sans garantie (articles 15 et 16 de la licence).

Le moteur est écrit depuis le texte publié, sans accès au moteur de référence. Chaque valeur que le texte ne donne pas,
et chaque point où la lettre du texte et les sorties des logiciels évalués divergent, est signalé dans le code avec la
mesure qui a conduit à la lecture retenue.

## État

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
| Bbio du logement à volets | en cours | 159 zones, écart médian +0,7 %, écart absolu médian 1,1 % ; 69 dans ±1 %, 124 dans ±2 %, 152 dans ±5 % |
| Stores enroulables | fait | essai sur 4 projets, Bbio entre -4,3 % et +3,9 % |
| Stores vénitiens, espaces tampons vitrés, tertiaire | à faire | - |
| Confort d'été (DH, mode Th-DC) | en cours | `groupe.calculer(thd=...)`, `banc.confort` : 12 groupes de 8 projets, écart médian nul, écart absolu médian 77 °C.h, 8 dans ±10 % |
| Bbio_max, DH_max (annexe R. 172-4) | fait | `exigences.py`, `banc.exigences` : Mbgeo juste sur 732 groupes, DH_max juste sur 761 |
| Consommations (Cep) | en cours | voir ci-dessous ; spécifications du lot 2 dans `specs/` |
| Carbone | à faire | - |

Mesure faite sur un fichier par projet (46 projets de logement). Les valeurs que le texte réglementaire ne donne pas
sont déduites des RSEE par le banc et consignées comme telles dans le code.

### Cep (en cours)

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
| Cep complet d'un projet (chauffage, froid, ECS, éclairage, auxiliaires, forfait froid, déplacements lus) | tous | `banc.cep_total`, `banc.cep_lot` | lot de 50 projets (électricité, gaz, réseaux) au 08/10/2026 : écart médian -0,1 %, |écart| médian 1,5 %, 34 dans ±5 %, 48 dans ±10 % ; hors : cas 16 (ECS d'un ballon sans source dans le RSEE, prise de la référence et signalée) et cas 15 (RSEE incohérent) |
| Génération : contrat d'appel, effet joule direct (8.18) | `generateurs.py` | `banc.chauffage_mois` | identité vérifiée : O_Cef_ch = O_B_Ch sur 46 groupes effet joule du lot |
| Besoin de chauffage Th-C (ventilation réelle, fuites de conduits, émission, relance) | `groupe.py`, `ventilation.py` | `banc.chauffage_mois` | 47 groupes effet joule : collectifs dans ±4 % après lecture « par défaut » de la classe d'étanchéité 3 ; restent les maisons de cas 17 (+9 à +13 %), cas 18 (+16 à +29 %) et cas 13 (+16 %) |
| Consignes corrigées Th-C (8.1) : θvt appliqué seulement aux émetteurs de statut 2 (valeur par défaut écrite), θvs non appliqué, cibles de puissance corrigées en chaud et en froid | `emission.py`, `groupe.py` | `banc.cep` | tranché au banc contre la lettre du texte : bureaux cas 11 36,4/36,2, cas 19 +6 %, cas 04 +4 à +11 %, cas 03 +2 %, effet joule cas 20 +0/-3 % ; froid des logements climatisés encore -13 à -33 % |
| Sortie RSEE : bloc Sortie_Projet (B, C, D) écrit depuis les résultats, RSEE d'entrée recopié | `sortie_rsee.py` | `banc.sortie_rsee` | première version ; pas de XSD dans le corpus, validation tierce à faire |
| Chauffage et froid : distribution, génération | à faire | | `specs/distribution.md`, `specs/generation.md`, `specs/pac_elec.md`, `specs/generateurs_simples.md` |

Lectures déduites des RSEE, que le texte ne donne pas : le poste « déplacement » contient les parkings ; le nombre
de personnes des ascenseurs est le nombre d'adultes équivalents ; l'énergie d'un aller-retour d'ascenseur est la
moyenne d'une montée et d'une descente. Cas non expliqués : ascenseurs de cas 21 et du bâtiment A de cas 22 (sous leur
veille par défaut), cas 23, bâtiment D de cas 18, cas 08.

## Installation et emploi

Python 3.11 ou plus, numpy ; openpyxl et pytest pour les outils et les tests.

    pip install -e ".[dev]"
    python outils/meteo_officielle.py                        # météo conventionnelle : téléchargée à la source, convertie
    python -m pytest
    python -m banc.sortie_rsee <rsee.xml> [sortie.xml]      # RSEE recalculé (Sortie_Projet remplacé) et comparaison
    python -m banc.cep_total <rsee.xml>                      # Cep d'un projet, poste par poste, face aux sorties du RSEE
    python -m openbce.api --port 8765                        # API HTTP : GET /version, POST /calcul (RSEE en corps)

API : `POST /calcul` avec le RSEE d'entrée en corps ; la réponse est le RSEE recalculé (XML) avec l'en-tête
`X-Openbce-Resume` (Bbio, Cep, DH par bâtiment) ; `POST /calcul?format=json` renvoie le résumé seul. Le RSEE reçu est
écrit dans un dossier temporaire le temps du calcul puis effacé. Conteneur : `Dockerfile` (python:3.12-slim + numpy,
données météo montées en volume).

Le banc d'essai (`banc/`) compare le calcul aux sorties de RSEE produits par un logiciel évalué. Il ne contient aucun
RSEE : chacun l'emploie avec les siens. Les cas cités dans ce fichier et dans le code (« cas 01 », « cas 02 »...) sont
des projets réels désignés par un repère neutre.

## Données

- Annexe III de l'arrêté du 4 août 2021 modifié et scénarios conventionnels : publiés par le ministère chargé de la
  construction sur rt-re-batiment.developpement-durable.gouv.fr, sous Licence Ouverte (etalab-2.0) sauf mention
  contraire. `openbce/tables/scenarios_officiels.json` est la conversion du tableur « Scénarios conventionnels » du
  29/04/2026 par `outils/scenarios_xlsx.py`.
- Données météorologiques conventionnelles : même source, non copiées dans le dépôt (`outils/meteo_officielle.py`).
- Aucune donnée de la base INIES n'est incluse.

## Organisation

- `openbce/rsee.py` : lecture d'un RSEE ; le format pivot reprend les noms du bloc `Entree_Projet`.
- `openbce/` : un module par fiche ou famille de fiches de l'annexe III, numéros d'équation en commentaire.
- `banc/` : comparaison aux RSEE de référence, poste par poste.
- `specs/` : spécifications des fiches du Cep, avec les lectures retenues et leurs justifications.
- `outils/` : conversion des données publiées.

## Contribuer

Les signalements les plus utiles portent sur une lecture du texte : citer la fiche, l'équation ou le tableau, la lecture
proposée et, si possible, un RSEE (anonymisé) dont les sorties la confirment. Toute modification distribuée ou mise à
disposition par réseau reste sous AGPL-3.0-or-later. Pour un autre régime de licence, s'adresser à ARKEMEP.
