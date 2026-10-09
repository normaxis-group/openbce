# Pistes de travail pour la recherche et l'enseignement

OpenBCE est la première mise en œuvre lisible de la méthode Th-BCE 2020. Il ouvre des travaux qui supposaient jusqu'ici
l'accès à un moteur fermé. Les sujets ci-dessous sont à la portée d'un stage, d'un projet de fin d'études ou d'une
thèse ; ils sont classés du plus immédiat au plus long.

## 1. Construire un jeu de cas de test ouvert

Le banc de validation repose sur des RSEE réels qui ne peuvent pas être publiés. Un jeu de cas synthétiques, chacun
isolant un phénomène (une paroi, une baie avec masque, un émetteur, une PAC, un ballon), calculé par des logiciels
évalués et publié avec ses sorties, permettrait à chacun de vérifier OpenBCE et de trancher les lectures du registre
([lectures.md](lectures.md)). C'est le travail le plus utile à court terme.

## 2. Écarts entre le texte publié et le moteur de référence

Le registre identifie des points où les logiciels évalués s'écartent de la lettre de l'annexe III. Un travail
méthodique (cas synthétiques, variation d'un paramètre à la fois) permettrait de les recenser tous et de proposer une
rédaction du texte qui suffise à reproduire le calcul.

## 3. Sensibilité et incertitudes

Le moteur se prête aux études de sensibilité : un premier essai sur 49 projets de logement a chiffré l'effet de
quelques choix de conception sur le Bbio (ponts thermiques, isolation, perméabilité, menuiseries, protections
solaires ; `banc/variantes.py`). Une analyse globale (indices de Sobol, plans d'expériences) donnerait la hiérarchie des
paramètres par usage et par zone climatique.

## 4. Lecture statistique de la RE2020

Les données ouvertes de l'observatoire OPEE (plus de 100 000 opérations) donnent la distribution nationale des
indicateurs, des seuils et des modulations, et le détail de l'analyse de cycle de vie par lot. Croisées avec OpenBCE,
elles permettent de situer une étude dans sa population, de repérer les saisies atypiques et d'étudier les marges
réelles par rapport aux seuils.

## 5. Indicateurs carbone

Ic construction et Ic énergie ne sont pas encore codés. La méthode (annexe II, annexe XI pour les forfaits) et la
table des composants de l'OPEE fournissent la matière d'une mise en œuvre et de sa validation.

## 6. Performance numérique

Un projet se calcule en une à quelques minutes en Python ; le cahier des charges initial visait moins de dix secondes.
Vectorisation, compilation (Numba, Cython, Rust) ou parallélisation par groupe sont des sujets d'ingénierie logicielle
bien délimités, vérifiables au banc.

## 7. Méthode conventionnelle et consommations réelles

Un moteur ouvert permet de remplacer un à un les scénarios conventionnels (occupation, météo réelle, consignes) et de
confronter le calcul aux consommations mesurées de bâtiments livrés.

## 8. Enseignement

Le code suit l'ordre et la numérotation des fiches de l'annexe III. Il peut servir de support à un cours de thermique
réglementaire : chaque module se lit à côté de sa fiche, et le banc montre l'effet chiffré de chaque choix.

Pour engager un travail, ouvrir un ticket sur le dépôt en décrivant le sujet ; voir aussi
[CONTRIBUTING.md](../CONTRIBUTING.md).
