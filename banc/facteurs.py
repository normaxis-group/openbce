# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Cherche ce qui distingue les zones en écart : écarts de chauffage et de froid selon quelques champs d'entrée.

    python -m banc.facteurs <dossier de RSEE>
"""
import collections
import json
import statistics
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee

def classe(valeur: float, bornes: tuple[float, float]) -> str:
    return "faible" if valeur < bornes[0] else ("moyen" if valeur < bornes[1] else "fort")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    lignes, projets = [], set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        if x["projet"] in projets or not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            continue
        if not {b.entier("Choix_PM_GPM", 0) for b in p.entree.tous("Baie")} <= {0, 1, 2, 3, 4, 5, 6}:
            continue
        projets.add(x["projet"])
        zones = {z.texte("Name"): z for z in p.entree.tous("Zone")}
        for _, zone, usage, surface, ch, _a, fr, _b, ecl, _c, bbio_ref, (ch_an, fr_an, ecl_an) in besoins.comparer(str(dossier / x["fichier"])):
            z = zones[zone]
            g = z.directs("Groupe")[0]
            baies = g.directs("Baie")
            lignes.append({
                "projet": x["projet"], "ch": ch.sum() / max(ch_an, 1e-9) - 1, "fr": fr.sum() - fr_an, "ecl": ecl.sum() - ecl_an, "ecl_ref": ecl_an, "ecl_calc": ecl.sum(),
                "CE": g.texte("Categorie_CE"), "hall": g.texte("Is_Hall"), "inertie": g.un("Inertie").texte("Type_Inertie_Quotidienne"),
                "traversant": z.texte("Is_Traversant"), "usage": str(usage), "brasseur": str(len(g.directs("Brasseur_Air"))),
                "dept": p.entree.un("Simu").texte("Departement"), "PM": "/".join(sorted({b.texte("Choix_PM_GPM") for b in baies})),
                "BR": "/".join(sorted({b.texte("Exp_BR") for b in baies})), "tampons": str(min(sum(q.entier("Id_Et", 0) != 0 for q in g.directs("Paroi_Opaque")), 1)),
                "echant": g.un("Permeabilite").texte("id_echantillonnage_permea"), "moteur": p.version_moteur,
                "volet opaque": str(int(any(b.entier("Choix_PM_GPM", 0) and b.nombre("Sw1_ap", 0) + b.nombre("Sw2_ap", 0) == 0 for b in baies))),
                "sans PM": classe(sum(b.nombre("Ab") for b in baies if b.entier("Choix_PM_GPM", 0) == 0) / max(sum(b.nombre("Ab") for b in baies), 1e-9), (0.05, 0.3)),
                "vitrage": classe(sum(b.nombre("Ab") for b in baies) / g.nombre("SHAB"), (0.17, 0.25)),
                "casquette": classe(max([m.nombre("Dhm", 0) for b in baies for m in b.directs("Masque_Horizontal")] or [0]), (0.5, 1.5)),
                "joue": classe(max([m.nombre(k, 0) for b in baies for n, k in (("Masque_Vert_Gauche", "Dvg"), ("Masque_Vert_Droite", "Dvd")) for m in b.directs(n)] or [0]), (0.5, 1.5)),
                "bbio": (2 * ch.sum() + 2 * fr.sum() + 5 * ecl.sum()) / max(bbio_ref, 1e-9) - 1})
    print(len(lignes), "zones de", len(projets), "projets")
    for cle in ("CE", "inertie", "traversant", "usage", "brasseur", "dept", "PM", "BR", "echant", "moteur", "volet opaque", "sans PM", "vitrage", "casquette", "joue"):
        groupes = collections.defaultdict(list)
        for l in lignes:
            groupes[l[cle]].append(l)
        print(f"{cle:<11}", " | ".join(f"{k or '-'} : n={len(v)}, chauffage {statistics.median(x['ch'] for x in v):+.0%}, froid {statistics.median(x['fr'] for x in v):+.1f}, Bbio {statistics.median(x['bbio'] for x in v):+.1%} (|.| {statistics.median(abs(x['bbio']) for x in v):.1%})" for k, v in sorted(groupes.items())))
    print("éclairage calculé selon la valeur du RSEE :", {k: round(statistics.median(l["ecl_calc"] for l in lignes if round(l["ecl_ref"], 1) == k), 3) for k in sorted({round(l["ecl_ref"], 1) for l in lignes})})
