# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Les 28 usages de la méthode Th-BCE 2020 (chapitre 15 de l'annexe III, tableur officiel des scénarios du 29/04/2026)
et leur état de validation dans OpenBCE.

Un usage est dit validé quand ses résultats ont été mesurés au banc contre des récapitulatifs de référence
(docs/validation.md). Les usages 4 à 28 sont codés d'après le texte, sans récapitulatif de référence : tout calcul qui
en contient est rendu avec un avertissement, dans le résumé de l'API et du serveur MCP.
"""

NOMS = {
    1: "Maisons individuelles ou accolées",
    2: "Logements collectifs",
    3: "Bureaux",
    4: "Enseignement primaire",
    5: "Enseignement secondaire",
    6: "Médiathèques et bibliothèques",
    7: "Bâtiments universitaires d'enseignement et de recherche et bâtiments d'enseignements atypiques",
    8: "Hôtels 0, 1 et 2 étoiles (partie nuit)",
    9: "Hôtels 3, 4 et 5 étoiles (partie nuit)",
    10: "Hôtels 0, 1 et 2 étoiles (partie jour)",
    11: "Hôtels 3, 4 et 5 étoiles (partie jour)",
    12: "Établissements d'accueil de la petite enfance",
    13: "Restaurants - en continu, 18 heures par jour, 7 jours sur 7",
    14: "Restaurants - 1 repas par jour, 5 jours sur 7",
    15: "Restaurants - 2 repas par jour, 7 jours sur 7",
    16: "Restaurants - 2 repas par jour, 6 jours sur 7",
    17: "Commerces",
    18: "Vestiaires",
    19: "Établissements sanitaires avec hébergement",
    20: "Établissements de santé (partie nuit)",
    21: "Établissements de santé (partie jour)",
    22: "Aérogares",
    23: "Industries ou artisanats 3x8h",
    24: "Industries ou artisanats 8h à 18h",
    25: "Établissements sportifs municipaux ou scolaires",
    26: "Restaurants scolaires - 1 repas par jour, 5 jours sur 7",
    27: "Restaurants scolaires - 3 repas par jour, 5 jours sur 7",
    28: "Établissements sportifs privés",
}

VALIDES = frozenset({1, 2, 3})
IHEBERGEMENT = frozenset({1, 2, 8, 9, 19, 20})   # tableau 4 (fiche 4.1, p. 57) : habitation ou hébergement
IENSEIGNEMENT = frozenset({4, 5, 7, 26, 27})     # tableau 4 : enseignement


def surface_reference(usage: int) -> str:
    """Balise de la surface de référence du groupe : SHAB en habitation, SU ailleurs (annexe R. 172-4, chapitre I)."""
    return "SHAB" if usage in (1, 2) else "SU"


def nom(usage: int) -> str:
    return NOMS.get(usage, f"usage {usage} inconnu")


def non_valides(usages) -> list[int]:
    """Usages présents dans le calcul qui n'ont pas de validation au banc, triés."""
    return sorted({int(u) for u in usages if int(u) not in VALIDES})


def avertissement(usages) -> str | None:
    """Phrase à joindre au résultat quand le calcul contient un usage non validé, sinon None."""
    nv = non_valides(usages)
    if not nv:
        return None
    return ("Usages non validés : " + ", ".join(f"{u} ({nom(u)})" for u in nv)
            + " ; codés d'après le texte de l'annexe III, sans récapitulatif de référence (voir docs/validation.md).")
