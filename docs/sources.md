# Sources officielles

Toutes les sources ci-dessous sont publiques. OpenBCE est écrit depuis ces textes et rien d'autre : il n'utilise ni le
moteur de calcul de référence, ni sa documentation interne, ni aucune donnée qui ne soit publiée.

Le portail de référence est celui du ministère chargé de la construction :
<https://rt-re-batiment.developpement-durable.gouv.fr/>. Ses contenus sont sous Licence Ouverte (etalab-2.0) sauf
mention contraire.

## Textes réglementaires

| Texte | Objet | Lien |
|---|---|---|
| Code de la construction et de l'habitation, articles R. 172-1 à R. 172-9 | exigences de performance énergétique et environnementale des constructions neuves | [Légifrance](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074096/LEGISCTA000043882854/) |
| Annexe à l'article R. 172-4 du CCH | seuils (Bbio_max, Cep_max, Cep,nr_max, DH_max, Ic) et modulations | [Légifrance, hors chapitres I à III](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045292850) ; chapitres I à III en PDF ci-dessous |
| Décret n° 2021-1004 du 29 juillet 2021 | exigences de la RE2020 | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043877196) |
| Arrêté du 4 août 2021 | exigences et approbation de la méthode de calcul (annexes I à XII) | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043936431) |
| Décret n° 2022-305 du 1er mars 2022 | extension aux bureaux et à l'enseignement | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045288020) |
| Arrêté du 6 avril 2022 | modification de l'arrêté du 4 août 2021 | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045571217) |
| Décret n° 2022-1516 du 3 décembre 2022 | modification | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046678439) |
| Arrêté du 22 décembre 2022 | modification | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046829490) |
| Arrêté du 14 août 2024 | modification | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050145618) |
| Décret n° 2024-1258 du 30 décembre 2024 | retour d'expérience RE2020 | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050873122) |
| Décret n° 2026-16 du 15 janvier 2026 | extension aux bâtiments tertiaires spécifiques et industriels | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053378848) |
| Décret n° 2026-200 du 18 mars 2026 | ajustements | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053703809) |
| Arrêté du 18 mars 2026 | modification | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053703826) |
| Arrêté du 19 mars 2026 | modification | [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053975637) |

Légifrance ne reproduit pas les annexes consolidées de l'arrêté : elles sont publiées en PDF sur le portail.
Récapitulatif officiel : [textes en version consolidée](https://rt-re-batiment.developpement-durable.gouv.fr/textes-en-version-consolidee-a617.html)
et [textes « Exigences et méthode »](https://rt-re-batiment.developpement-durable.gouv.fr/textes-exigences-et-methode-a703.html).

## Annexes de l'arrêté du 4 août 2021 (versions consolidées)

| Annexe | Contenu | Lien |
|---|---|---|
| I | définitions | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexei_arrete_4_aout_2021.pdf) |
| II | méthode de calcul énergie et environnement (cadre, coefficients) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexeii_arrete_4_aout_2021.pdf) |
| III | **méthode de calcul détaillée « Th-BCE 2020 »**, la source principale d'OpenBCE (1 854 pages) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexeiii_arrete_4_aout_2021_complet_compresse.pdf) |
| IV | règles Th-Bat 2020 : données d'entrée du calcul (publiées à part, voir plus bas) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexeiv_arrete_4_aout_2021_new.pdf) |
| V | procédure d'autocontrôle et d'approbation des logiciels | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexev_arrete_4_aout_2021.pdf) |
| VI | contenu du récapitulatif standardisé d'étude énergétique et environnementale (RSEE) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexevi_arrete_4_aout_2021.pdf) |
| VII | calcul optionnel : impact de différents paramètres sur Bbio, Cep,nr, Cep et DH (information des concepteurs et des occupants) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexevii_arrete_4_aout_2021.pdf) |
| VIII | modalités de vérification des systèmes de ventilation | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexeviii_arrete_4_aout_2021.pdf) |
| IX | dossier d'études pour la proposition de modes d'application simplifiés | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexeix_arrete_4_aout_2021.pdf) |
| X | dossier d'études pour les cas particuliers (Titre V) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexex_arrete_4_aout_2021.pdf) |
| XI | performances forfaitaires de certains lots (analyse de cycle de vie) | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexexi_arrete_4_aout_2021.pdf) |
| XII | performances par défaut des isolants biosourcés | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/annexexii_arrete_4_aout_2021.pdf) |

Chapitres I à III de l'annexe à l'article R. 172-4 (seuils et modulations), versions successives :
[avant le retour d'expérience 2024](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/chapitre1a3_annexe_r172-4_avant-retex2024.pdf),
[après le retour d'expérience 2024](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/chapitre1a3_annexe_r172-4_post-retex2024.pdf),
[extension aux tertiaires spécifiques](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/chapitre1a3_annexe_r172-4_post-gtm2.pdf),
[ajustements de 2026](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/chapitre1a3_annexe_r172-4_post-rivaton-i.pdf).

**Version de l'annexe III suivie par le code.** Le code a été écrit sur la version de mai 2025 (1 872 pages) et
comparé fiche par fiche, le 09/10/2026, à la version consolidée du 21/07/2026 (1 854 pages, moteur de référence
2026.E1). Les fiches codées n'ont pas changé sur le fond ; les écarts portent surtout sur l'extension aux 28 usages et
sur des fiches nouvelles (PAC au CO2, systèmes sous Titre V).

## Données conventionnelles

| Donnée | Emploi dans OpenBCE | Lien |
|---|---|---|
| Scénarios conventionnels, 28 usages (tableur du 29/04/2026) | `openbce/tables/scenarios_officiels.json`, converti par `outils/scenarios_xlsx.py` | [XLSX](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/xlsx/2026-04-29_scenarios_conventionnels.xlsx) |
| Données météorologiques conventionnelles (8 zones, jeux Th-BC et Th-D, 8 760 h) | téléchargées et converties par `outils/meteo_officielle.py` | [XLSX](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/xlsx/4_scenarios_meteorologiques_th-bc_th-d_re2020.xlsx), [page](https://rt-re-batiment.developpement-durable.gouv.fr/documents-complementaires-a706.html) |
| Règles Th-Bat 2020 (coefficients de l'enveloppe) | non utilisées par le calcul : les RSEE portent déjà les U et ψ | [PDF](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/2026-04-29_regles_th-bat.pdf) |

## Documents d'application et cadre des logiciels

- [Fiches d'application de la RE2020](https://rt-re-batiment.developpement-durable.gouv.fr/documents-d-application-a618.html)
  (protections mobiles, variation temporelle des émetteurs électriques, ascenseurs partagés, usages, etc.).
- [Gestion des versions du moteur Th-BCE 2020 et du RSEE](https://rt-re-batiment.developpement-durable.gouv.fr/gestion-des-versions-du-moteur-de-calcul-th-bce-a688.html) :
  le moteur de référence est développé par le CSTB à la demande des pouvoirs publics et distribué aux éditeurs sous
  forme de bibliothèque compilée ; dates des versions et combinaisons autorisées du RSEE.
- [Évaluation des logiciels](https://rt-re-batiment.developpement-durable.gouv.fr/evaluation-des-logiciels-a619.html)
  et son [règlement](https://rt-re-batiment.developpement-durable.gouv.fr/IMG/pdf/reglement_evaluation_logiciels_re2020.pdf) :
  seuls les logiciels approuvés peuvent servir à une étude réglementaire. OpenBCE n'en fait pas partie.

## Données ouvertes

- [Observatoire des performances énergétiques et environnementales des bâtiments neufs (OPEE)](https://www.data.gouv.fr/datasets/opee-observatoire-des-performances-energetiques-et-environnementales-des-batiments-neufs),
  data.gouv.fr, Licence Ouverte 2.0 : indicateurs et seuils de plus de 100 000 opérations achevées (extraction au
  01/01/2026), par projet, bâtiment, zone et groupe, et composants de l'analyse de cycle de vie. Les données d'entrée
  détaillées (parois, systèmes) n'y sont pas : elles ne permettent pas de recalculer un projet, mais de situer un
  résultat dans la distribution nationale.
