# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import sys, json, statistics
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from openbce import rsee, aeraulique, meteo, climat
TIRAGE, FACTEUR = sys.argv[1] == '1', float(sys.argv[2])
lot = json.load(open("../brut/rsee/_lot.json", encoding="utf-8"))["fichiers"]
res, vus = [], set()
for x in sorted(lot, key=lambda x: x["octets"])[:70]:
    try: p = rsee.lire("../brut/rsee/" + x["fichier"])
    except Exception: continue
    simu = p.entree.un("Simu")
    d = climat.departement(simu.texte("Departement"))
    c = climat.du_site(meteo.charger("donnees/meteo_re2020.npz", climat.ZONE_CLIMATIQUE[d]), d, simu.nombre("Altitude"))
    hiver = np.r_[0:59 * 24, 334 * 24:8760]            # décembre à février
    for b in p.entree.directs("Batiment"):
        sz = {z.entier("Index"): z for sb in p.sortie.tous("Sortie_Batiment_B") if sb.entier("Index") == b.entier("Index") for z in sb.tous("Sortie_Zone_B")}
        for z in b.directs("Zone"):
            s = sz.get(z.entier("Index"))
            if z.entier("Usage") not in (1, 2) or s is None: continue
            ref = s.nombre("H_V_Def_Hiver", 0)
            cle = (x["projet"], z.texte("Name"), ref)
            if cle in vus or ref <= 0: continue
            vus.add(cle)
            h = 0.0
            for g in z.directs("Groupe"):
                f = aeraulique.du_groupe(z, g, tirage_si_haut=TIRAGE)
                h += FACTEUR * np.mean([aeraulique.CPA * f.equilibre(c.vent[k], c.te[k], c.we[k], 19.0, 0.006)[0] for k in hiver[::7]])
            res.append((h / ref - 1, x["projet"], z.texte("Name")[:24], z.entier("Usage"), z.directs("Groupe")[0].un("Permeabilite").entier("id_echantillonnage_permea", 0), z.nombre("Hauteur_Zone"), round(h, 1), ref))
e = [r[0] for r in res]
print(len(res), "zones ; écart médian %+.0f %%, |écart| médian %.0f %%, de %+.0f %% à %+.0f %%" % (100 * statistics.median(e), 100 * statistics.median(map(abs, e)), 100 * min(e), 100 * max(e)))
for t in (0, 1):
    v = [r[0] for r in res if r[4] == t]
    if v: print("  id_echantillonnage_permea =", t, ":", len(v), "zones, médiane %+.0f %%" % (100 * statistics.median(v)))
for r in sorted(res)[:2] + sorted(res)[-2:]: print("   %+.0f %%" % (100 * r[0]), r[1:])
