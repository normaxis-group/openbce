# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Dump par zone (logement) : caractère traversant, protections, hauteur, besoins calculés et RSEE.

    python -m banc.zones <dossier de RSEE> [fichiers par projet]   -> <dossier>/../zones.json
"""
import json
import sys
from pathlib import Path

from banc import besoins
from openbce import rsee

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier, par_projet = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 1
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    vus, zones = {}, []
    for x in sorted(lot, key=lambda x: x["octets"]):
        if vus.get(x["projet"], 0) >= par_projet:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        if not all(z.entier("Usage") in (1, 2) for z in p.entree.tous("Zone")):
            continue
        vus[x["projet"]] = vus.get(x["projet"], 0) + 1
        infos = {}
        for z in p.entree.tous("Zone"):
            g = z.directs("Groupe")[0]
            pm = sorted({b.entier("Choix_PM_GPM", 0) for b in g.tous("Baie")})
            infos[z.texte("Name")] = dict(traversant=z.entier("Is_Traversant", 1), hauteur=z.nombre("Hauteur_Zone", 0), pm=pm,
                                          ouvrables=sum(b.nombre("Ab") * b.nombre("Rouv_Max", 0) for b in g.tous("Baie") if b.entier("Baie_ouvrable", 0)),
                                          a_baies=sum(b.nombre("Ab") for b in g.tous("Baie")), httf=g.nombre("Httf", 1.5), auto_ouv=sum(b.entier("Has_Gestion_Auto_Ouverture", 0) for b in g.tous("Baie")))
        try:
            for nom, zone, usage, surface, ch, _, fr, _, ecl, _, bbio_ref, (ch_an, fr_an, ecl_an) in besoins.comparer(str(dossier / x["fichier"])):
                b = 2 * ch.sum() + 2 * fr.sum() + 5 * ecl.sum()
                zones.append(dict(projet=x["projet"], zone=zone, usage=usage, surface=surface, ch=float(ch.sum()), ch_ref=ch_an, fr=float(fr.sum()), fr_ref=fr_an,
                                  ecl=float(ecl.sum()), ecl_ref=ecl_an, bbio=float(b), bbio_ref=bbio_ref, **infos.get(zone, {})))
        except Exception as e:
            print(x["projet"], "échec", type(e).__name__, flush=True)
        print(x["projet"], len(zones), flush=True)
    (dossier.parent / "zones.json").write_text(json.dumps(zones, ensure_ascii=False, indent=0), encoding="utf-8")
