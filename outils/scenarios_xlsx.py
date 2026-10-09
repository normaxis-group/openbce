# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Convertit le tableur officiel des scénarios conventionnels en `openbce/tables/scenarios_officiels.json`.

    python outils/scenarios_xlsx.py <2026-04-29_scenarios_conventionnels.xlsx> [sortie.json]

Source : « Scénarios conventionnels », publié avec les textes consolidés sur rt-re-batiment.developpement-durable.gouv.fr
(fichier du 29/04/2026, une feuille par usage, 28 usages). Il remplace l'extraction du chapitre 15 de l'annexe III
faite sur le PDF (outil retiré le 09/10/2026) : 5 usages seulement, valeurs arrondies, tableaux des locaux
d'enseignement illisibles.

Le schéma de sortie est celui que lit `openbce.scenarios` : par usage, une liste de scalaires (consignes, puis pour
chaque local : nom, part de surface, occupants, chaleur et humidité par occupant, apports par unité) et une liste de
tableaux {nom, hebdo 7 x 24, annuel 5 x 12}. Dans le profil annuel, une case vide (mois sans cinquième semaine) vaut null.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import openpyxl

JOUR, SEMAINE = "jour V / heure >", "semaine V / mois >"
ENTETES_JOUR = (JOUR, "jour/heure")          # les feuilles 6, 7 et 11 emploient la seconde forme dans certains locaux
TITRES = {                                   # titre de bloc du tableur -> début du nom lu par openbce.scenarios
    "mobilité": "mobilité", "occupation": "occupation", "chauffage": "Chauffage", "refroidissement": "Refroidissement",
    "ventilation": "ventilation", "eclairage": "éclairage", "éclairage": "éclairage", "besoins d'ecs": "ECS facteur correctif de la semaine",
}


def _nombre(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", ".").strip())
    except ValueError:
        return None


def _texte(v) -> str:
    return "" if v is None else " ".join(str(v).split())     # espaces normalisés : « semaine V / mois  > » existe aussi


def _entete_jour(r) -> bool:
    """Ligne d'en-tête d'un profil hebdomadaire : libellé connu, ou heures 1 à 24 (le local 5 de l'usage 11 porte « 0 »)."""
    return _texte(r[1]) in ENTETES_JOUR or (_nombre(r[2]) == 1 and _nombre(r[25]) == 24 and _nombre(r[1]) == 0)


def feuille(ws) -> tuple[int, str, dict]:
    lignes = [list(r) + [None] * (30 - len(r)) for r in ws.iter_rows(values_only=True)]
    titre = next(_texte(r[0]) for r in lignes if _texte(r[0]).startswith("RE 2020 Description"))
    m = re.search(r"usage\s+(\d+)\.\s*(.+)$", titre)
    numero, nom = int(m.group(1)), f"{m.group(1)}. {m.group(2).strip()}"
    scalaires, tableaux = [], []
    local = None
    i = 0
    while i < len(lignes):
        r = lignes[i]
        c1, c2, c3 = _texte(r[1]), r[2], _texte(r[3])
        b = c1.lower()
        if b in ("normal", "arrêt moins de 48 h", "arrêt plus de 48 h") and local is None:
            scalaires.append({"nom": f"consigne {b}", "chauffage": _nombre(r[3]), "refroidissement": _nombre(r[4])})
        elif b.startswith("local n°"):
            local = {}
        elif b == "nom du local":
            local = {"nom": _texte(c2)}
            scalaires.append({"nom": "local", "local": local["nom"]})
        elif b in ("rat_l", "ratel"):
            scalaires.append({"nom": "ratio du local", "valeur": _nombre(c2)})
        elif b == "occupant":
            local["occupant"] = (_nombre(c2), c3)            # Noccnom par m² en tertiaire ; « * » (Nadeq calculé) en résidentiel
            if c3.lower().startswith("noccnom"):
                scalaires.append({"nom": "occupants par m²", "valeur": _nombre(c2)})
        elif c3 in ("W/Nocc", "W/Nadeq", "W/Noccnom"):
            scalaires.append({"nom": "Chaleur moyenne dégagée par un occupant", "valeur": _nombre(c2), "unite": c3})
        elif c3.lower().startswith("kg/h/n"):
            scalaires.append({"nom": "Humidité dégagée par un occupant", "valeur": _nombre(c2), "unite": c3})
        elif c3 == "Watts/unité":
            scalaires.append({"nom": "Apports de chaleur hors occupants et éclairage, par unité", "valeur": _nombre(c2), "unite": c3})
        elif c3 == "kg/h/unité":
            scalaires.append({"nom": "production d'humidité hors occupants et éclairage, par unité", "valeur": _nombre(c2), "unite": c3})
        elif c3 == "L/semaine/unité" and _nombre(c2) is not None:
            scalaires.append({"nom": "nombre de litres d'eau à 40°C puisés par semaine et par unité", "valeur": _nombre(c2), "unite": c3})
        elif _entete_jour(r):
            hebdo = [[_nombre(v) for v in lignes[i + k][2:26]] for k in range(1, 8)]
            # titre du bloc : la dernière cellule de la colonne B au-dessus qui n'est ni un nombre ni un en-tête
            j = i - 1
            while j > 0 and (not _texte(lignes[j][1]) or _nombre(lignes[j][1]) is not None or _texte(lignes[j][1]) in (*ENTETES_JOUR, SEMAINE)):
                j -= 1
            bloc = _texte(lignes[j][1])
            k = i + 8
            while k < len(lignes) and _texte(lignes[k][1]) != SEMAINE and not _entete_jour(lignes[k]):
                k += 1
            annuel = [[_nombre(v) for v in lignes[k + s][2:14]] for s in range(1, 6)] if k < len(lignes) and _texte(lignes[k][1]) == SEMAINE else None
            cle = bloc.lower()
            if local is not None and cle == "occupant":
                v, u = local.get("occupant", (None, ""))
                t_nom = f"occupant {'' if v is None else str(v).replace('.', ',')} {u}".strip()
            elif local is not None and cle.startswith("apports de chaleur"):
                t_nom = "Apports de chaleur hors occupants et éclairage"
            elif local is not None and cle.startswith("apports d'humidité"):
                t_nom = "Apports d'humidité hors occupants et éclairage"
            else:
                t_nom = next((v for c, v in TITRES.items() if cle.startswith(c)), bloc)
            tableaux.append({"nom": t_nom, "hebdo": hebdo, "annuel": annuel, "ligne": i + 1})
            i = k + 6 if annuel is not None else i + 8
            continue
        i += 1
    return numero, nom, {"feuille": ws.title, "scalaires": scalaires, "tableaux": tableaux}


def convertir(xlsx: Path) -> dict:
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    usages = {}
    for ws in wb.worksheets:
        numero, nom, d = feuille(ws)
        usages[str(numero)] = {"nom": nom, **d}
    return {"source": f"{xlsx.name} (rt-re-batiment.developpement-durable.gouv.fr, textes consolidés)", "usages": usages}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    entree = Path(sys.argv[1])
    sortie = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "openbce" / "tables" / "scenarios_officiels.json"
    d = convertir(entree)
    sortie.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    for n, u in d["usages"].items():
        locaux = [s["local"] for s in u["scalaires"] if s["nom"] == "local"]
        print(f"{n:>3} {u['feuille']:16} {len(u['tableaux']):3} tableaux, {len(locaux)} locaux : {', '.join(locaux)[:90]}")
