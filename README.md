<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/openbce-logo-fond-sombre.svg">
    <img alt="OpenBCE, moteur RE2020 open source" src="docs/images/openbce-logo.svg" width="460">
  </picture>
</p>

# OpenBCE

**Moteur de calcul libre de la méthode Th-BCE 2020 de la RE2020**, écrit depuis le texte publié de l'annexe III de
l'arrêté du 4 août 2021 modifié. Droits : ARKEMEP. Licence : AGPL-3.0-or-later.

> **Avertissement.** OpenBCE n'est pas un logiciel évalué au sens du règlement d'évaluation des logiciels RE2020. Ses
> résultats ne sont pas opposables : il ne produit pas d'attestation, ne peut pas fonder une étude réglementaire et ne
> remplace pas un logiciel approuvé. Sa précision est mesurée et publiée ([docs/validation.md](docs/validation.md)) ;
> elle n'atteint pas encore 1 % sur les consommations. Le code est fourni sans garantie (articles 15 et 16 de la
> licence).

## Pourquoi ce projet

La méthode de calcul de la RE2020 est un texte réglementaire public de plus de 1 800 pages. Le moteur qui l'applique
dans tous les logiciels du marché est une bibliothèque compilée, distribuée aux seuls éditeurs. Personne ne peut donc
lire comment un résultat réglementaire est calculé, ni vérifier que le moteur suit le texte.

OpenBCE met en œuvre la méthode à partir du seul texte publié, dans un code lisible qui suit l'ordre et la numérotation
des fiches. Chaque fois que le texte ne suffit pas (valeur absente, tableau publié en image, champ du RSEE non
documenté) ou que les logiciels évalués s'en écartent, la lecture retenue est écrite dans le code avec la mesure qui
l'a décidée, et recensée dans un registre public ([docs/lectures.md](docs/lectures.md)).

Il sert à relire et contrôler un calcul réglementaire, à étudier la sensibilité d'un projet, à enseigner la méthode et
à mener des travaux de recherche qui supposaient jusqu'ici l'accès à un moteur fermé ([docs/recherche.md](docs/recherche.md)).

## Ce que fait OpenBCE aujourd'hui

- Lit un RSEE (le fichier XML de toute étude RE2020) et en recalcule les sorties : besoins (Bbio), consommations (Cep),
  confort d'été (DH), seuils Bbio_max et DH_max avec leurs modulations ; écrit un RSEE dont le bloc des sorties est
  remplacé.
- Couvre le logement individuel et collectif, les bureaux en partie, l'effet joule, les PAC électriques à source air,
  les chaudières gaz et fioul, les réseaux de chaleur et de froid, les ballons et chauffe-eau thermodynamiques, la
  ventilation simple et double flux, l'éclairage, les ascenseurs et parkings.
- Ne couvre pas encore : indicateurs carbone (Ic), photovoltaïque, solaire thermique, espaces tampons, ventilation
  naturelle et puits climatiques, PAC à sources eau et sol, bois et cogénération, systèmes sous Titre V, usages
  tertiaires autres que les bureaux.

Résultats de validation au 08/10/2026, sur 50 opérations réelles : Cep à -0,1 % en médiane, écart absolu médian 1,5 %,
48 opérations dans ±10 % ; Bbio du logement à +0,1 % en médiane sur 167 zones. Détail, protocole et écarts connus :
[docs/validation.md](docs/validation.md).

## Documentation

| Document | Contenu |
|---|---|
| [docs/methode.md](docs/methode.md) | la méthode Th-BCE 2020 et sa correspondance fiche par fiche avec les modules |
| [docs/lectures.md](docs/lectures.md) | registre des lectures du texte tranchées par OpenBCE, dont les écarts entre le texte et la référence |
| [docs/validation.md](docs/validation.md) | réserves, protocole, résultats et écarts connus |
| [docs/sources.md](docs/sources.md) | textes réglementaires, annexes, données conventionnelles et données ouvertes, avec leurs liens |
| [docs/rsee.md](docs/rsee.md) | le format RSEE, ses versions, ce qu'OpenBCE en lit et en écrit |
| [docs/recherche.md](docs/recherche.md) | pistes de travail pour la recherche et l'enseignement |
| [docs/ia.md](docs/ia.md) | emploi par un assistant d'IA : serveur MCP, API OpenAPI, schéma des résultats, [`llms.txt`](llms.txt) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | comment contribuer |
| `specs/` | spécifications des fiches des consommations, avec les lectures envisagées |

## Installation et emploi

Python 3.11 ou plus et numpy ; openpyxl et pytest pour les outils et les tests.

    git clone https://github.com/normaxis-group/openbce.git
    cd openbce
    pip install -e ".[dev]"
    python outils/meteo_officielle.py                        # météo conventionnelle, téléchargée à la source
    python -m pytest
    python -m banc.sortie_rsee <rsee.xml> [sortie.xml]      # RSEE recalculé et comparaison champ à champ
    python -m banc.cep_total <rsee.xml>                      # Cep d'un projet, poste par poste
    python -m openbce.api --port 8765                        # API HTTP : GET /version, POST /calcul
    python -m openbce.serveur_mcp                            # serveur MCP en stdio, pour un assistant d'IA

API : `POST /calcul` avec le RSEE en corps ; la réponse est le RSEE recalculé, avec l'en-tête `X-Openbce-Resume`
(Bbio, Cep, DH par bâtiment) ; `POST /calcul?format=json` renvoie le résumé seul. Le fichier reçu est effacé après le
calcul. Description complète : [docs/openapi.yaml](docs/openapi.yaml). Un `Dockerfile` est fourni (python:3.12-slim et
numpy, données météo montées en volume).

Assistant d'IA : le serveur MCP expose les outils `version`, `lire_rsee`, `calculer`, `comparer` et `variante` (étude
d'une modification des entrées). Installation dans Claude Code :
`claude mcp add openbce -- python /chemin/vers/openbce/openbce/serveur_mcp.py`. Détails : [docs/ia.md](docs/ia.md).

## Organisation du code

- `openbce/` : le moteur, un module par fiche ou famille de fiches de l'annexe III ; numéros d'équation et de tableau
  en commentaire.
- `banc/` : comparaison aux sorties de RSEE de référence, poste par poste. Il ne contient aucun RSEE : chacun
  l'emploie avec les siens.
- `outils/` : conversion des données publiées (scénarios conventionnels, météo).
- `tests/` : tests unitaires, sur des RSEE fabriqués.

## Données

Textes, scénarios et météo viennent du portail du ministère chargé de la construction
(rt-re-batiment.developpement-durable.gouv.fr, Licence Ouverte etalab-2.0 sauf mention contraire). Les scénarios
convertis sont dans le dépôt (`openbce/tables/scenarios_officiels.json`) ; la météo est téléchargée à la source.
Aucune donnée de la base INIES ni aucun RSEE réel n'est inclus. Liste complète : [docs/sources.md](docs/sources.md).

## Citer, contribuer, licence

- Citation : voir [CITATION.cff](CITATION.cff).
- Contributions, questions et propositions de sujets d'étude : par les tickets du dépôt ; voir
  [CONTRIBUTING.md](CONTRIBUTING.md).
- Licence : GNU Affero General Public License v3.0 ou ultérieure ([LICENSE](LICENSE)). Toute version modifiée
  distribuée ou mise à disposition par réseau doit l'être avec son code source. Pour un autre régime de licence,
  s'adresser à ARKEMEP par un ticket.

---

*English summary.* OpenBCE is an open-source (AGPL-3.0) implementation of Th-BCE 2020, the French regulatory
building energy calculation method (RE2020), written solely from the published text. It reads a RSEE file, recomputes
the regulatory indicators (Bbio, Cep, DH) and documents every interpretation of the text, including the points where
certified software departs from it. It is not a certified tool and its results have no regulatory value. Validation
against 50 real projects is published in `docs/validation.md`.
