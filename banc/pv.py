# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc de la production photovoltaïque : par bâtiment, production annuelle et mensuelle calculée contre O_Eef_Prod_PV
(kWh par m² de SREF) des RSEE.

    python -m banc.pv <dossier de RSEE | fichiers> [--tous]

Sur un dossier, un seul RSEE (le plus petit) par opération ; `--tous` les garde tous, variantes comprises.
"""
import json
import statistics
import sys
from pathlib import Path

import numpy as np

from banc.besoins import METEO, zone_climatique
from openbce import climat, meteo, photovoltaique, rsee

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cibles = []
    tous = "--tous" in sys.argv
    for a in (x for x in sys.argv[1:] if x != "--tous"):
        p = Path(a)
        if p.is_dir():
            lot = json.loads((p / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
            vus = set()
            for x in sorted(lot, key=lambda x: x["octets"]):
                if (tous or x["projet"] not in vus) and "<PV_install>" in (p / x["fichier"]).read_text(encoding="utf-8", errors="replace"):
                    vus.add(x["projet"])
                    cibles.append(p / x["fichier"])
        else:
            cibles.append(p)
    rapports, mensuels = [], []
    for chemin in cibles:
        try:
            projet = rsee.lire(str(chemin))
        except Exception as e:
            print(chemin.name, "illisible", type(e).__name__)
            continue
        simu = projet.entree.un("Simu")
        cl = climat.du_site(meteo.charger(METEO, zone_climatique(projet)), simu.texte("Departement"), simu.nombre("Altitude"))
        sorties = {b.entier("Index"): b for b in projet.sortie.tous("Sortie_Batiment_C")}
        for bat in projet.entree.directs("Batiment"):
            if not bat.tous("PV_install"):
                continue
            s = sorties.get(bat.entier("Index"))
            sref = s.nombre("O_SREF", 0.0) if s else 0.0
            if not s or sref <= 0:
                continue
            prod = photovoltaique.du_batiment(bat, cl) / 1000.0 / sref                          # kWh/m²
            ref = s.nombre("O_Eef_Prod_PV_annuel", 0.0)
            calc = float(prod.sum())
            capteurs = [c for i in bat.tous("PV_install") for o in i.directs("Onduleur_PV") for c in o.directs("Capteur_PV")]
            codes = sorted({(c.entier("Valeur_Declaree_Defaut", -1), c.entier("Type_Confinement", -1), c.entier("Type_Techno_Capteur", -1)) for c in capteurs})
            masques = sum(1 for c in capteurs if c.directs("Masque_Lointain_Azimutal"))
            ref_mois = np.array(s.mensuel("O_Eef_Prod_PV_mois")) if s.tous("O_Eef_Prod_PV_mois") else None
            from openbce import calendrier
            cal = calendrier.construire()
            calc_mois = np.array([prod[cal.mois_civil == m + 1].sum() for m in range(12)])
            ecart_mois = ""
            if ref_mois is not None and ref_mois.sum() > 0:
                ecart_mois = " | mois " + " ".join(f"{c / r:4.2f}" if r > 0 else "  - " for c, r in zip(calc_mois, ref_mois))
                mensuels.append((calc_mois, ref_mois))
            ratio = calc / ref if ref > 0 else float("nan")
            rapports.append((chemin.stem, bat.texte("Name"), calc, ref, ratio, codes, masques))
            print(f"{chemin.stem} {bat.texte('Name')[:18]:18} calc {calc:6.2f} / RSEE {ref:6.2f} kWh/m² ({ratio:5.2f}) codes {codes} masques {masques}{ecart_mois}", flush=True)
    valides = [r for r in rapports if r[3] > 0]
    if valides:
        ratios = [r[4] for r in valides]
        print(f"\n{len(valides)} bâtiments : rapport médian {statistics.median(ratios):.3f}, min {min(ratios):.3f}, max {max(ratios):.3f}, "
              f"dans ±5 % : {sum(1 for r in ratios if abs(r - 1) <= 0.05)}, dans ±10 % : {sum(1 for r in ratios if abs(r - 1) <= 0.10)}")
        for cle in ("statut", "confinement"):
            groupes = {}
            for r in valides:
                for code in r[5]:
                    k = code[0] if cle == "statut" else code[1]
                    groupes.setdefault(k, []).append(r[4])
            print(f"  par {cle} :", {k: f"{statistics.median(v):.3f} ({len(v)})" for k, v in sorted(groupes.items())})
