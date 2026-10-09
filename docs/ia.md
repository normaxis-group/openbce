# OpenBCE et les assistants d'IA

OpenBCE est prévu pour être employé par un assistant (Claude ou tout modèle compatible MCP) autant que par une
personne : un assistant peut lire un RSEE, le recalculer, le comparer à sa référence et étudier des variantes, en
citant ses sources et en rappelant les réserves. Quatre points d'entrée.

| Point d'entrée | Fichier | Pour qui |
|---|---|---|
| Index de la documentation pour les modèles | [`llms.txt`](../llms.txt) | tout modèle qui doit comprendre le projet avant d'y travailler |
| Serveur MCP en stdio | `openbce/serveur_mcp.py` | assistants de bureau ou de code (Claude Desktop, Claude Code, autres clients MCP) |
| API HTTP décrite en OpenAPI 3.1 | [`openapi.yaml`](openapi.yaml), `openbce/api.py` | intégration dans une application ou un agent par HTTP |
| Schéma JSON des résultats | [`schemas/resume.schema.json`](schemas/resume.schema.json) | validation des réponses de l'API et du serveur MCP |

## Le serveur MCP

Il ne dépend que de la bibliothèque standard et de numpy, comme le reste du moteur. Il lit les RSEE sur le disque
local, par leur chemin : aucun fichier ne quitte la machine.

| Outil | Ce qu'il fait | Durée |
|---|---|---|
| `version` | version, texte suivi, couverture de la méthode, réserves | immédiate |
| `lire_rsee` | résumé des entrées (site, zone climatique, zones, usages, surfaces, composition) et sorties de référence du fichier | immédiate |
| `calculer` | recalcul : Bbio, Cep, Cef, DH, Bbio_max par bâtiment ; RSEE recalculé écrit sur disque | 30 s à 40 min |
| `comparer` | recalcul puis écarts champ par champ avec les sorties de référence du fichier | celle d'un calcul |
| `variante` | modifie des champs de `Entree_Projet` sur une copie, recalcule, rend les écarts avec le projet initial | deux calculs |

Pendant un calcul, si le client fournit un `progressToken`, le serveur envoie une notification de progression toutes
les 15 secondes. Certains clients limitent la durée d'un appel d'outil : la relever pour les gros projets (avec Claude
Code, variable d'environnement `MCP_TOOL_TIMEOUT`, en millisecondes).

Désignation d'un champ pour `variante` : chemin sous `Entree_Projet`, noms d'éléments séparés par « / », sans les
niveaux `_Collection`, avec un rang facultatif entre crochets à partir de 1. Exemples :

- `Batiment/Zone/Groupe/Permeabilite/Q4PaSurf` : perméabilité à l'air de tous les groupes ;
- `Batiment/Zone[2]/Groupe[1]/Baie[3]/Uw` : coefficient d'une baie précise.

Essai sur un projet de bureaux de 241 m² : `comparer` en 36 s (Bbio +0,1 %, Cep -1,0 % par rapport à la référence) ;
`variante` avec une perméabilité ramenée de 1,7 à 0,5 m³/(h.m²) sous 4 Pa : Bbio -16,9 points, Cep -4,3 kWh/(m².an),
en deux calculs de 30 et 34 s.

### Installation

Prérequis : le dépôt cloné, `pip install -e .`, puis la météo (`python outils/meteo_officielle.py`).

Claude Code :

    claude mcp add openbce -- python /chemin/vers/openbce/openbce/serveur_mcp.py

Claude Desktop, dans `claude_desktop_config.json` :

    {
      "mcpServers": {
        "openbce": {
          "command": "python",
          "args": ["/chemin/vers/openbce/openbce/serveur_mcp.py"]
        }
      }
    }

Autre client MCP : commande `python -m openbce.serveur_mcp` lancée depuis la racine du dépôt, ou le chemin du fichier
comme ci-dessus.

## Ce qu'un assistant doit dire de ces résultats

Le serveur transmet ses consignes au client à l'initialisation. L'assistant doit rappeler que les résultats ne sont pas
opposables (logiciel non évalué), citer les écarts connus quand le projet en relève (froid Th-C des logements
climatisés, PAC multiservices) et ne jamais présenter un recalcul comme une attestation. Voir [validation.md](validation.md).
