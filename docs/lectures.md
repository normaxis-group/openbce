# Registre des lectures du texte

L'annexe III ne suffit pas toujours à reproduire le calcul : des valeurs y manquent, des tableaux et des formules ne
sont publiés qu'en image, des champs du RSEE ne sont pas documentés, et sur quelques points les sorties des logiciels
évalués s'écartent de la lettre du texte. Ce registre recense les lectures qu'OpenBCE a dû trancher. Chacune est écrite
aussi dans le module concerné, avec les chiffres qui l'ont décidée.

Trois catégories :

- **Muet** : le texte ne donne pas la valeur ou la règle ; la lecture retenue est celle qu'un implémenteur de la
  méthode retiendrait, vérifiée au banc quand c'est possible.
- **Déduit** : un code ou un champ du RSEE n'est pas documenté ; son sens est déduit des RSEE de référence.
- **Contre la lettre** : le banc montre que les logiciels évalués ne suivent pas la lettre du texte ; OpenBCE reproduit
  la référence et le signale. Ces points intéressent au premier chef quiconque veut comparer le texte publié et le
  moteur de référence.

Les « cas » cités sont des projets réels du banc de validation, désignés par un repère neutre (voir
[validation.md](validation.md)).

## Points où la référence ne suit pas la lettre du texte

| Fiche | Question | Lecture retenue | Mesure | Module |
|---|---|---|---|---|
| 7.1 éclairage | Un local sans accès à la lumière naturelle prend C2 = 1 : il consomme à pleine puissance toute l'occupation | les circulations et sanitaires sans accès à la lumière naturelle ne sont pas comptés dans le Bbio | bureaux cas 11 : 8,14 kWh/m² selon le texte, 6,68 sans ces locaux, 6,6 au RSEE ; cas 23 : 17,27, 16,61, 16,5 | `eclairage.py` |
| 8.1 émission | Correction des consignes par la variation temporelle (θvt) et spatiale (θvs) des émetteurs | θvt appliqué seulement aux émetteurs dont le statut vaut 2 (valeur par défaut écrite), avec la valeur saisie, sans majoration de 0,5 K ; θvs non appliqué | sur 1 772 émetteurs, θvt vaut 1,8 ou 2,0 exactement quand le statut vaut 2 ; bureaux cas 11 : chauffage 36,4 pour 36,2 ainsi, 48,6 avec le θvs saisi, 62,8 avec le défaut de θvt | `emission.py` |
| 8.1 émission (803, 808) | Cible de la puissance d'émission : consigne brute (lettre de 803) ou consigne corrigée | consigne corrigée, en chaud et en froid | les références Th-C dépassent leur Th-B de 15 à 57 % exactement sur les groupes à θvt de 1,8 K | `groupe.py` |
| 5.6 (138) débits d'air | En habitation, pas de tirage thermique entre niveaux (hauteur limitée à 3 m) | hauteur de la zone plafonnée à 15 m dès qu'elle atteint 3 m | avec 3 m, l'indicateur d'infiltration hivernale des RSEE est sous-estimé de 24 à 72 % selon le caractère traversant ; avec 15 m, l'écart tombe dans une bande de 0 à -28 % indépendante de ce caractère | `aeraulique.py` |

## Valeurs et règles absentes du texte

| Fiche | Question | Lecture retenue | Justification | Module |
|---|---|---|---|---|
| 5.9 protections mobiles | Limites de température opérative de la gestion automatique (« - » en valeur conventionnelle) | 24 et 26 °C | grille sur 10 projets à volets automatiques : 24/26 donne un Bbio à -0,4 % (écart médian 1,2 %) ; 25/27 +1,4 % ; 26/28 +1,8 % ; valeur provisoire | `protections.py` |
| 5.13 ouverture des baies | L'hystérésis vaut-elle la nuit ? | à toute heure d'occupation | fenêtres fermées la nuit : froid surestimé de 7 kWh/m² ; ratio figé la nuit : sous-estimé de 1,8 | `ouverture.py` |
| 5.13 (Th-B) | Le mode Th-B reprend la gestion manuelle « avec quelques différences » | hors période de refroidissement, les baies à ouverture automatique restent pilotées en inoccupation | sans cette aération, la saison de froid des bureaux démarre le 1er juin, ce qu'aucun RSEE ne montre | `groupe.py` |
| 5.21 comportement thermique | Formule de la part frs non donnée | complément de frm et de la part des baies, par cohérence avec (349) à (351) | à confirmer | `thermique.py` |
| 5.6 perméabilité | Majoration de 1,2 d'une perméabilité mesurée par échantillonnage : s'applique-t-elle à la valeur par défaut ? | non, seulement aux valeurs mesurées | rapport de 1,20 à 1,23 entre groupes échantillonnés et non échantillonnés ; aucun RSEE ne tranche le cas par défaut | `aeraulique.py` |
| 8.7 distribution | Loi d'eau (figure 97, en image) | départ de dimensionnement sous la température de base, interpolation jusqu'à 20 °C à 15 °C extérieurs | relevé sur la figure | `distribution.py` |
| 8.7 à 8.10 | Signe des pertes des réseaux froids | comptées positives dans la demande | sens physique | `distribution.py` |
| 9.7 distribution ECS | Température de l'eau au secondaire : 53 °C (tableau 279) ou 48 °C (tableau 272) | 53 °C, la valeur de la fiche de la distribution elle-même | | `ecs_distribution.py` |
| 9.8 bouclage | Débit de bouclage non défini | même énergie, volume puisé majoré | | `ecs_distribution.py` |
| 9.13, 9.14 | Pertes du ballon : premier ou second appel de générateur | premier appel (base) | | `generateurs_ballon.py` |
| 9.13, 9.14 | Débit d'air extrait d'un chauffe-eau thermodynamique : partagé entre assemblages identiques ? | non | un partage plafonnerait la machine sous la puissance observée (cas 28) | `generateurs_ballon.py` |
| 10.1 ascenseurs | Équations 2300 et 2301 imprimées avec des signes incohérents | forme physique : frottement résistant, pesanteur comptée selon le sens | | `ascenseurs.py` |
| 10.1 ascenseurs | Nombre de personnes NB (2281) ; énergie moyenne Emoy (2302) | NB = adultes équivalents conventionnels ; Emoy = moyenne d'une montée et d'une descente | écart inférieur à 4 % sur les zones sans parking | `ascenseurs.py` |

## Champs du RSEE non documentés

| Champ | Lecture retenue | Justification | Module |
|---|---|---|---|
| `Type_Regul_Res` (ventilation résidentielle) | 0 : gestion manuelle (14 h de grand débit par semaine) ; 1 : temporisation (7 h) | banc des auxiliaires : 151 groupes sur 181 dans ±0,05 kWh/m² | `ventilation.py`, `ventilateurs.py` |
| `Cdep` (coefficient de dépassement) | 0 : 1,30 par défaut ; 1 : pas de dépassement (1,0) ; 2 : valeur saisie | lu 1,15, le chauffage Th-C de 18 groupes sort à +23,6 % ; lu 1,0, à +12,6 % puis dans ±4 % avec les autres lectures | `ventilation.py` |
| `Classe_Etancheite` (réseaux de ventilation) | 3 lu « par défaut », 0 aussi ; 1 et 2 : classes A et B | lue classe C, des collectifs sortent à -38/-58 % ; lue par défaut, dans ±4 % | `ventilation.py` |
| Statut d'efficacité d'échangeur double flux | 2 : certifié (ε tel quel) ; 1 : justifié (0,9 ε) ; 0 : déclaré | ordre du texte (6.3.3.4.2) ; le lot ne porte que le code 2 | `ventilation.py` |
| `Valeur_Saisie_Defaut_Q4PaSurf` | 0 : valeur par défaut du tableau 30 | les zones à 0 ont une perméabilité saisie nulle et une forte déperdition par infiltration | `aeraulique.py` |
| `Reseau_Chaleur` | index du type de réseau des tableaux 248 et 249 (0 eau chaude basse température ... 3 vapeur haute pression) | un réseau nommé « chaud » porte 0, ce qui exclut une lecture booléenne | `reseau_fourniture.py` |
| `Isolation_Du_Reseau` | index de colonne du tableau 248 | | `reseau_fourniture.py` |
| `Sys_Thermo_ts` = 5 | triple service « air extérieur avec production d'ECS » lu comme ECS air extérieur/eau (tableau 150) | | `generateurs_ballon.py` |

## Hypothèses essayées puis écartées

Elles restent dans le code comme options d'étude, inactives par défaut, pour que chacun puisse refaire la mesure.

| Option | Hypothèse | Pourquoi elle est écartée |
|---|---|---|
| `thermodynamique.MULTISERVICE_PABS_REDUIT` | PAC double et triple service (1294) : réduire aussi la puissance absorbée du temps passé en ECS | corrige deux projets (+25 à +5 %, +20 à 0 %) mais en dégrade six autres, dont un exact à la lettre (0 à -17 %) |
| `saisons.POIDS_INCONFORT_CHAUD_THC` | poids 1,0 de l'inconfort chaud dans le déclenchement des saisons en Th-C | deux projets gagnent, un perd, les bureaux prennent du froid en juin |
| `groupe.OUVERTURE_CLIMATISE_JAMAIS` | un groupe climatisé n'ouvre jamais ses baies en Th-C | la saison de froid démarre trop tôt partout |
| `groupe.RECUP_RESEAU` | récupération partielle des pertes des réseaux rebouclées | à 0,5, un projet passe à +66 % ; la valeur du texte (1,0) est gardée |

## Écarts connus entre les références et le texte, non reproduits

- Annexe R. 172-4 : sur la plupart des projets de maisons, les RSEE calculent la modulation Mbsurf_moy comme si la
  surface moyenne valait 1,02 fois Sref/NL (0,7 point de Bbio_max). Le texte ne le justifie pas : OpenBCE garde le texte
  (`exigences.py`).
