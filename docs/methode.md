# La méthode Th-BCE 2020 et son découpage dans OpenBCE

## Ce que calcule la méthode

La RE2020 juge un bâtiment neuf sur des indicateurs calculés par une simulation thermique horaire sur une année
conventionnelle (8 760 heures, météo et occupation conventionnelles). La méthode est fixée par l'annexe III de
l'arrêté du 4 août 2021 ; les seuils par l'annexe à l'article R. 172-4 du code de la construction et de l'habitation.
Trois modes de calcul se partagent le même modèle de bâtiment :

| Mode | Ce qu'il calcule | Indicateur réglementaire |
|---|---|---|
| Th-B | besoins de chauffage, de refroidissement et d'éclairage, à consignes et systèmes conventionnels | Bbio = 2 x (Bch + Bfr) + 5 x Becl, en points |
| Th-C | consommations réelles des systèmes : émission, distribution, stockage, génération, auxiliaires, eau chaude sanitaire, éclairage, déplacements | Cep et Cep,nr (kWh d'énergie primaire par m² et par an) |
| Th-D | température intérieure sans système de refroidissement, avec une séquence caniculaire | DH, degrés-heures d'inconfort estival |

S'y ajoutent les indicateurs carbone (Ic énergie, Ic construction), qui relèvent de l'analyse de cycle de vie et ne
sont pas encore traités par OpenBCE.

## Le modèle de bâtiment

Le RSEE (voir [rsee.md](rsee.md)) décrit le projet par niveaux emboîtés : projet, bâtiment, zone (un usage : maison,
logement collectif, bureaux, enseignement...), groupe (l'unité thermique, avec ses parois, ses baies, ses ponts
thermiques, ses émetteurs et sa ventilation), puis les systèmes partagés : générations, distributions intergroupes,
ballons d'eau chaude. La simulation tourne heure par heure au niveau du groupe ; les résultats sont agrégés à la zone
puis au bâtiment, pondérés par les surfaces.

## Organisation de l'annexe III et modules correspondants

Les numéros sont ceux des fiches de l'annexe III (version de mai 2025). Chaque module cite dans ses commentaires les
numéros d'équation et de tableau qu'il applique.

| Fiches | Objet | Module | État |
|---|---|---|---|
| 3.1 | climat extérieur, calendrier | `climat.py`, `calendrier.py`, `meteo.py` | fait |
| 3.2 | rayonnement, masques lointains et proches, éclairement | `rayonnement.py` | fait |
| 4.1, chapitre 15 | scénarios conventionnels (28 usages) | `scenarios.py` | fait |
| 4.5, 4.6 | indicateurs de confort, saisons propres d'un groupe | `saisons.py` | fait |
| 5.6 | débits d'air par les défauts d'étanchéité | `aeraulique.py` | fait |
| 5.7, 5.21, 13.1 | assemblage du groupe, comportement thermique, sorties Th-B | `groupe.py`, `thermique.py` | fait |
| 5.9 | gestion des protections mobiles | `protections.py` | fait (volets, stores enroulables) ; stores vénitiens à faire |
| 5.10 | baies vitrées | `baies.py` | fait |
| 5.13 | surventilation par ouverture des baies | `ouverture.py` | fait |
| 5.17, 5.19 | parois opaques, ponts thermiques | `parois.py`, `enveloppe.py` | fait |
| 5.2 à 5.4 | espaces tampons | | à faire |
| 6.2, 6.3, 6.5 | ventilation mécanique : bouches, double flux, simple flux | `ventilation.py`, `ventilateurs.py` | fait en résidentiel ; tertiaire partiel |
| 6.6 à 6.11 | ventilation naturelle et hybride, puits climatiques | | à faire |
| 7.1 | éclairage | `eclairage.py` | fait |
| 8.1, 8.5 | émission en chaud et en froid, relances | `emission.py` | fait |
| 8.4 | saisons de fonctionnement des systèmes | `banc/cep.py` (saisons du bâtiment) | fait, à intégrer au moteur |
| 8.7 à 8.10 | distribution hydraulique du groupe et intergroupe | `distribution.py` | fait |
| 8.17, 8.18 | génération : contrat d'appel, effet joule direct | `generateurs.py` | fait |
| 8.19 | chaudières gaz et fioul | `chaudiere.py` | fait |
| 8.23, 8.26 | PAC électriques (chauffage, froid, multiservice), sources amont air | `thermodynamique.py` | fait pour les sources air |
| 8.28 | réseaux de chaleur et de froid | `reseau_fourniture.py` | fait |
| 8.32 | brasseurs d'air | `brasseurs.py` | partiel |
| 8.20 à 8.22, 8.24, 8.25, 8.30, 8.31 | autres générateurs (bois, cogénération, PAC gaz, géocooling) | | à faire |
| 9.5 à 9.8 | eau chaude sanitaire : besoins, émission, distribution | `ecs.py`, `ecs_distribution.py` | fait |
| 9.9 à 9.14 | ballons, régulation, générateurs pour ballon (CET, appoints) | `ballon.py`, `generateurs_ballon.py` | fait pour les sources air |
| 9.15 à 9.21 | solaire thermique, récupération sur eaux grises | | à faire |
| 10.1, 10.3, 10.4 | ascenseurs, ventilation et éclairage des parkings | `ascenseurs.py`, `parkings.py` | fait |
| 11.1 | pertes récupérables | `groupe.py` | fait pour les réseaux |
| 12.1 à 12.4 | photovoltaïque | | à faire |
| 13.2 à 13.4, 4.7 | sorties Th-C, bilans, Cep | `bilans.py`, `consommation.py` | fait |
| 13.5 | confort d'été (Th-D) | `groupe.py` | fait, à fiabiliser |
| 16.x | systèmes sous Titre V | | à faire |
| annexe R. 172-4 | Bbio_max, DH_max et modulations | `exigences.py` | fait |
| annexe VI | lecture et écriture du RSEE | `rsee.py`, `sortie_rsee.py` | fait, sans validation contre un schéma |

## Principes d'écriture

- Le code suit la lettre du texte. Quand le texte est muet, illisible (tableaux ou formules publiés en image) ou
  contredit par les sorties des logiciels évalués, la lecture retenue est écrite dans le code avec sa justification et
  les mesures qui l'ont décidée. Ces lectures sont recensées dans [lectures.md](lectures.md).
- Aucun coefficient n'est ajusté pour coller à un résultat. Une hypothèse qu'on veut tester devient une option
  d'étude, inactive par défaut, avec la mesure qui l'a fait écarter.
- Le calcul est en Python avec numpy, sans autre dépendance. Les performances ne sont pas l'objectif de cette
  version : un projet de logement collectif se calcule en une à quelques minutes.
