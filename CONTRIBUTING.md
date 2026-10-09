# Contribuer à OpenBCE

Les contributions sont bienvenues : signalements, relectures du texte, cas de test, code. Le projet est en français,
comme la méthode qu'il met en œuvre.

## Signaler une lecture du texte

C'est la contribution la plus utile. Ouvrir un ticket qui donne :

- la fiche, l'équation ou le tableau de l'annexe III concerné (numéros de la version consolidée, avec la date de la
  version) ;
- la lecture actuelle d'OpenBCE (voir [docs/lectures.md](docs/lectures.md) et le commentaire du module) ;
- la lecture proposée et ce qui la fonde : le texte, une fiche d'application, ou les sorties d'un RSEE produit par un
  logiciel évalué.

Un RSEE joint doit être anonymisé : retirer la branche `DATAS_COMP` et les libellés, ne garder que ce qui sert au cas.

## Proposer du code

- Un module par fiche ou famille de fiches, avec en tête la fiche suivie ; les numéros d'équation et de tableau en
  commentaire, à côté de la ligne qui les applique.
- Suivre la lettre du texte. S'en écarter seulement sur une mesure, écrite dans le commentaire avec ses chiffres, et
  ajouter le point au registre des lectures.
- Aucun coefficient de calage. Une hypothèse à tester devient une option d'étude, inactive par défaut.
- Des tests sans données réelles : RSEE fabriqués dans le test (voir `tests/test_socle.py`).
- `python -m pytest` doit passer avant toute proposition.

## Licence des contributions

OpenBCE est distribué sous AGPL-3.0-or-later ; les contributions le sont aux mêmes conditions. ARKEMEP, titulaire des
droits, peut aussi proposer le moteur sous une autre licence à des éditeurs ; pour qu'une contribution importante
puisse y être incluse, un accord de contribution sera proposé à son auteur avant intégration.

## Échanges

Les questions, propositions de sujets d'étude et signalements passent par les tickets du dépôt.
