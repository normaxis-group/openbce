# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Contrôle des données d'entrée d'un RSEE : situe chaque zone par rapport au corpus de référence.

    python -m banc.controle_saisie <dossier de RSEE de référence> <rsee à contrôler.xml>

Pour une dizaine de grandeurs qui pèsent sur le Bbio, donne la valeur de la zone et son rang dans le corpus (centile).
Un rang extrême ne prouve rien : il désigne une donnée à justifier par les pièces du projet (plans, CCTP, fiches
produits, rapport d'étanchéité). Le sens favorable est indiqué pour chaque grandeur.
"""
from __future__ import annotations

import bisect
import json
import sys
from pathlib import Path

from openbce import rsee

# nom, sens favorable au Bbio (-1 : plus c'est bas, mieux c'est ; +1 : l'inverse ; 0 : selon le cas)
GRANDEURS = [
    ("perméabilité saisie, m³/(h.m²)", -1), ("U moyen des parois verticales", -1), ("U moyen des planchers hauts", -1), ("U moyen des planchers bas", -1),
    ("Uw moyen des baies", -1), ("facteur solaire moyen des baies", 0), ("psi moyen des ponts thermiques, W/(m.K)", -1),
    ("longueur de ponts thermiques par m² habitable", -1), ("surface de baies par m² habitable", 0), ("inertie quotidienne, kJ/(K.m²)", 1),
    ("débit d'air du Bbio, m³/h par m² habitable", -1), ("part des baies à protection automatique", 1), ("part des baies avec masque lointain", 0),
    ("hauteur moyenne des masques lointains, degrés", 0), ("ratio d'ouverture moyen des baies", 1), ("Bbio rapporté au Bbio max", -1),
]


def _moyenne(couples):
    s = sum(a for a, _ in couples)
    return sum(a * v for a, v in couples) / s if s > 0 else None


def indicateurs(zone, sortie):
    g = zone.directs("Groupe")
    shab = sum(x.nombre("SHAB", 0) or x.nombre("SU", 0) for x in g)
    parois = [p for x in g for p in x.directs("Paroi_Opaque") if p.entier("Id_Et", 0) == 0]
    baies = [b for x in g for b in x.directs("Baie")]
    lin = [l for x in g for l in x.directs("Lineaire")]
    a_baies = sum(b.nombre("Ab") for b in baies)
    lointains = [max(m.serie("Gamma") or [0]) for b in baies for m in b.directs("Masque_Lointain_Azimutal")]
    moyennes_lointains = [sum(m.serie("Gamma")) / 36 for b in baies for m in b.directs("Masque_Lointain_Azimutal") if len(m.serie("Gamma")) == 36]
    bbio, bmax = sortie.nombre("O_Bbio_pts_annuel", 0), sortie.nombre("O_Bbio_Max", 0)
    return [
        _moyenne([(x.nombre("SHAB", 0) or 1, x.un("Permeabilite").nombre("Q4PaSurf")) for x in g]),
        _moyenne([(p.nombre("Ak"), p.nombre("Uk")) for p in parois if 60 <= p.nombre("Beta") <= 120]),
        _moyenne([(p.nombre("Ak"), p.nombre("Uk")) for p in parois if p.nombre("Beta") < 60]),
        _moyenne([(p.nombre("Ak"), p.nombre("Uk")) for p in parois if p.nombre("Beta") > 120]),
        _moyenne([(b.nombre("Ab"), b.nombre("Usp_Vert")) for b in baies]),
        _moyenne([(b.nombre("Ab"), b.nombre("Sw1_sp_c") + b.nombre("Sw2_sp_c") + b.nombre("Sw3_sp_c")) for b in baies]),
        _moyenne([(l.nombre("Ll"), l.nombre("Psil")) for l in lin]),
        sum(l.nombre("Ll") for l in lin) / shab if shab else None,
        a_baies / shab if shab else None,
        _moyenne([(x.nombre("SHAB", 0) or 1, x.un("Inertie").nombre("Cmq_surf")) for x in g]),
        sum(x.nombre("Qv_occ_BBIO", 0) for x in g) / shab if shab else None,
        sum(b.nombre("Ab") for b in baies if b.entier("Choix_PM_GPM", 0) in (1, 4, 7)) / a_baies if a_baies else None,
        sum(b.nombre("Ab") for b in baies if b.directs("Masque_Lointain_Azimutal")) / a_baies if a_baies else None,
        sum(moyennes_lointains) / len(moyennes_lointains) if moyennes_lointains else 0.0,
        _moyenne([(b.nombre("Ab"), b.nombre("Rouv_Max", 0)) for b in baies]),
        bbio / bmax if bmax else None,
    ]


def zones(chemin):
    p = rsee.lire(chemin)
    for b in p.entree.directs("Batiment"):
        sorties = {z.entier("Index"): z for sb in p.sortie.tous("Sortie_Batiment_B") if sb.entier("Index") == b.entier("Index") for z in sb.tous("Sortie_Zone_B")}
        for z in b.directs("Zone"):
            s = sorties.get(z.entier("Index"))
            if s is not None and z.entier("Usage") in (1, 2):
                yield z, s


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, cible = Path(sys.argv[1]), sys.argv[2]
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    corpus, projets = [], set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in projets:
            continue
        try:
            for z, s in zones(dossier / x["fichier"]):
                corpus.append(indicateurs(z, s))
            projets.add(x["projet"])
        except Exception:
            continue
    print(f"corpus : {len(corpus)} zones de logement, {len(projets)} projets")
    colonnes = [sorted(v[k] for v in corpus if v[k] is not None) for k in range(len(GRANDEURS))]
    for z, s in zones(cible):
        v = indicateurs(z, s)
        print(f"\n{z.texte('Name')} (usage {z.texte('Usage')}, {z.texte('NB_logement')} logements) - Bbio {s.texte('O_Bbio_pts_annuel')} pour un maximum de {s.texte('O_Bbio_Max')}")
        for k, (nom, sens) in enumerate(GRANDEURS):
            if v[k] is None or not colonnes[k]:
                continue
            rang = 100 * (bisect.bisect_left(colonnes[k], v[k]) + bisect.bisect_right(colonnes[k], v[k])) / 2 / len(colonnes[k])
            med = colonnes[k][len(colonnes[k]) // 2]
            favorable = (sens < 0 and rang <= 10) or (sens > 0 and rang >= 90)
            defavorable = (sens < 0 and rang >= 90) or (sens > 0 and rang <= 10)
            marque = "  << très favorable" if favorable else ("  >> très défavorable" if defavorable else ("  (extrême)" if sens == 0 and (rang <= 5 or rang >= 95) else ""))
            print(f"   {nom:<48} {v[k]:8.3f}   médiane du corpus {med:8.3f}   centile {rang:3.0f}{marque}")
