# Le RSEE, format d'entrée et de sortie

Le récapitulatif standardisé d'étude énergétique et environnementale (RSEE) est le fichier XML que tout logiciel
évalué produit pour une étude RE2020 (article 18 de l'arrêté du 4 août 2021, contenu fixé par l'annexe VI). Il est
déposé sur le service de génération des attestations ; c'est aussi la matière première de l'observatoire OPEE.

OpenBCE lit un RSEE, recalcule ses sorties et écrit un RSEE dont seul le bloc des sorties est remplacé.

## Structure

| Branche | Contenu | Emploi par OpenBCE |
|---|---|---|
| `DATAS_COMP` | données administratives (opération, permis, maître d'ouvrage) | recopiée telle quelle ; l'année de dépôt du permis sert aux exigences |
| `RSET` / `Entree_Projet` | entrées du moteur de calcul : projet, bâtiments, zones, groupes, parois, baies, ponts thermiques, émetteurs, ventilation, générations, distributions, ballons | lue intégralement ; c'est le format pivot du moteur (`openbce/rsee.py`) |
| `RSET` / `Sortie_Projet` | sorties du moteur : Bbio, Cep, Cep,nr, DH et leurs seuils, besoins et consommations par poste, annuels et mensuels, par bâtiment, zone et groupe | lue par le banc de validation ; réécrite par `openbce/sortie_rsee.py` |
| `RSEnv` | analyse de cycle de vie : lots, composants, données environnementales | non lue pour l'instant |

Un RSEE est donc à la fois un jeu d'entrées complet et la réponse du moteur de référence sur ces entrées : c'est ce
qui en fait un cas de test.

## Versions

Le moteur de référence et le RSEE évoluent ensemble. Versions publiées par le ministère
([source](https://rt-re-batiment.developpement-durable.gouv.fr/gestion-des-versions-du-moteur-de-calcul-th-bce-a688.html)) :

| Version du moteur et du RSET | Application obligatoire (permis déposés à partir du) |
|---|---|
| 2021.E1.0.0 | 01/01/2022 |
| 2022.E1.0.0 | 25/07/2022 |
| 2022.E1.0.1 | 11/09/2022 |
| 2022.E2.1.0 | 29/11/2022 |
| 2022.E3.0.0 | 07/04/2023 |
| 2024.E1.0.0 | 01/01/2025 |
| 2025.E1.0.0 | 01/05/2026 |
| 2026.E1.0.0 | 01/07/2026 |

Les RSEE du banc de validation ont été produits entre 2022 et 2025 par plusieurs versions du moteur. Un écart entre
OpenBCE et une référence peut donc venir aussi d'une évolution du moteur de référence entre deux versions.

## Ce qui manque

Aucun schéma XSD du RSEE n'est publié sur le portail du ministère. La structure lue par OpenBCE est celle des RSEE
rencontrés ; le RSEE écrit par OpenBCE reprend les noms de champs des RSEE lus mais n'a pas été validé contre un schéma
officiel ni par un vérificateur tiers.

## Données personnelles

Un RSEE réel contient des données d'opération et souvent de maîtres d'ouvrage. Le dépôt n'en contient aucun.
L'API efface le fichier reçu après le calcul. Pour partager un cas de test, retirer au minimum la branche
`DATAS_COMP` et les libellés des entrées.
