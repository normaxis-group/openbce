# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des exigences sur les données ouvertes de l'observatoire OPEE (data.gouv.fr, table « zone ») : pour chaque zone,
les coefficients de modulation et les seuils publiés sont confrontés à `openbce.exigences`.

    python -m banc.opee_exigences <zone_open_data.csv> <projet_open_data.csv>

Vérifié par zone : Mbgeo, Mcgeo, Mccat, Mbbruit (usages 3 et plus, où il ne dépend que de la catégorie de contraintes
extérieures), Mbsurf_tot et Mcsurf_tot quand la surface de référence de l'usage dans le bâtiment est connue (sommes des
zones de même usage, toutes à surface publiée), Bbio_maxmoyen, Cep,nr_maxmoyen et Cep_maxmoyen retrouvés en divisant le
seuil publié par (1 + somme des modulations publiées, Mccat calculé), et DH_max. La classe d'altitude de l'OPEE est ramenée à 200,
600 ou 1 000 m. Les surfaces moyennes des logements ne sont pas publiées : Mbsurf_moy et Mcsurf_moy ne sont pas testés,
et DH_max du logement collectif n'est testé qu'en catégorie 1 hors climatisation en H2d et H3.
"""
import collections
import csv
import statistics
import sys

from openbce import exigences

ALTITUDE = {"0 à 400m": 200.0, "400 à 800m": 600.0, "> à 800m": 1000.0}
TOL = 0.0051


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main(zone_csv: str, projet_csv: str) -> None:
    annee = {}
    with open(projet_csv, encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            a = _f(r.get("annee_depot_pc"))
            if a:
                annee[r["projet_id"]] = int(a)
    zones = []
    with open(zone_csv, encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            u = _f(r.get("usage"))
            if u is None or int(u) not in exigences.BBIO_MAX_MOYEN or r.get("zone_climatique") not in exigences.ZONES:
                continue
            zones.append(r)
    # surface de référence par usage et par bâtiment, quand toutes les zones de l'usage ont une surface publiée
    sref_usage = {}
    par_bat = collections.defaultdict(list)
    for r in zones:
        par_bat[(r["projet_id"], r["batiment_index"], r["usage"])].append(_f(r.get("sref")))
    for cle, srefs in par_bat.items():
        if all(s is not None for s in srefs):
            sref_usage[cle] = sum(srefs)

    bilan = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, []]))   # usage -> test -> [ok, total, exemples]
    bases = collections.defaultdict(lambda: collections.defaultdict(list))

    def test(u, nom, ok, exemple):
        b = bilan[u][nom]
        b[1] += 1
        if ok:
            b[0] += 1
        elif len(b[2]) < 3:
            b[2].append(exemple)

    for r in zones:
        u, zc, alt = int(float(r["usage"])), r["zone_climatique"], ALTITUDE.get(r.get("altitude"), 200.0)
        cat = int(_f(r.get("categorie_ce")) or 1) or 1
        clim = r.get("is_climatise") == "true"
        an = annee.get(r["projet_id"], 2026)
        mb = {k: _f(r.get(k)) for k in ("mbgeo", "mbcombles", "mbsurf_moy", "mbsurf_tot", "mbbruit")}
        mc = {k: _f(r.get(k)) for k in ("mcgeo", "mccombles", "mcsurf_moy", "mcsurf_tot", "mccat")}
        if mb["mbgeo"] is not None:
            v = exigences.mbgeo(u, zc, alt)
            test(u, "Mbgeo", abs(v - mb["mbgeo"]) <= TOL, f"{zc} {r.get('altitude')} : OPEE {mb['mbgeo']}, calculé {v:.3f}")
        if mc["mcgeo"] is not None:
            v = exigences.mcgeo(u, zc, alt, an)
            test(u, "Mcgeo", abs(v - mc["mcgeo"]) <= TOL, f"{zc} {r.get('altitude')} : OPEE {mc['mcgeo']}, calculé {v:.3f}")
        if mc["mccat"] is not None:
            v = exigences.mccat(u, zc, cat)
            test(u, "Mccat", abs(v - mc["mccat"]) <= TOL, f"{zc} CE{cat} : OPEE {mc['mccat']}, calculé {v:.3f}")
        if u >= 3 and mb["mbbruit"] is not None:
            v = exigences.mbbruit(u, zc, 1, cat)
            test(u, "Mbbruit", abs(v - mb["mbbruit"]) <= TOL, f"{zc} CE{cat} : OPEE {mb['mbbruit']}, calculé {v:.3f}")
        s = sref_usage.get((r["projet_id"], r["batiment_index"], r["usage"]))
        if s is not None and mb["mbsurf_tot"] is not None and u != 1:
            v = exigences.mbsurf_tot(u, s, an)
            test(u, "Mbsurf_tot", abs(v - mb["mbsurf_tot"]) <= TOL, f"S {s:.0f} m², permis {an} : OPEE {mb['mbsurf_tot']}, calculé {v:.3f}")
        if s is not None and mc["mcsurf_tot"] is not None and u != 1:
            v = exigences.mcsurf_tot(u, s, an, r.get("is_reseau_urbain") == "true")
            test(u, "Mcsurf_tot", abs(v - mc["mcsurf_tot"]) <= TOL, f"S {s:.0f} m², permis {an} : OPEE {mc['mcsurf_tot']}, calculé {v:.3f}")
        bbio_max, cep_max, cep_nr_max = _f(r.get("bbio_max")), _f(r.get("cep_max")), _f(r.get("cep_nr_max"))
        if bbio_max and all(x is not None for x in mb.values()):
            base = bbio_max / (1 + sum(mb.values()))
            bases[u]["Bbio_maxmoyen"].append(base)
            test(u, "Bbio_maxmoyen", abs(base / exigences.BBIO_MAX_MOYEN[u] - 1) <= 0.005, f"retrouvé {base:.1f} pour {exigences.BBIO_MAX_MOYEN[u]}")
        if cep_nr_max and all(x is not None for x in mc.values()):
            # la colonne mccat de l'OPEE est vide (0) sur quelques zones CE2 dont le seuil contient pourtant la modulation :
            # le seuil est divisé par les modulations publiées, Mccat remplacé par la valeur calculée
            mc = dict(mc, mccat=exigences.mccat(u, zc, cat))
            base = cep_nr_max / (1 + sum(mc.values()))
            bases[u]["Cep,nr_maxmoyen"].append(base)
            test(u, "Cep,nr_maxmoyen", abs(base / exigences.CEP_NR_MAX_MOYEN[u] - 1) <= 0.005, f"retrouvé {base:.1f} pour {exigences.CEP_NR_MAX_MOYEN[u]}")
        if cep_max and all(x is not None for x in mc.values()):
            base = cep_max / (1 + sum(mc.values()))
            bases[u]["Cep_maxmoyen"].append(base)
            test(u, "Cep_maxmoyen", abs(base / exigences.CEP_MAX_MOYEN[u] - 1) <= 0.005, f"retrouvé {base:.1f} pour {exigences.CEP_MAX_MOYEN[u]}")
        dh = _f(r.get("dh_max"))
        if dh is not None and not (u == 2 and (cat >= 2 or (clim and zc in ("H2d", "H3")))):
            v = exigences.dh_max(u, zc, cat, clim)
            test(u, "DH_max", (v is None and dh >= 9999990) or (v is not None and abs(v - dh) <= 0.5), f"{zc} CE{cat} {'climatisé' if clim else ''} : OPEE {dh:.0f}, calculé {v}")

    for u in sorted(bilan):
        print(f"\n=== usage {u} ({exigences.USAGES[u]}) : {sum(1 for r in zones if int(float(r['usage'])) == u)} zones")
        for nom, (ok, total, ex) in bilan[u].items():
            ligne = f"  {nom:16} {ok:6}/{total:<6} ({100 * ok / total:5.1f} %)"
            if nom in bases[u]:
                ligne += f"  médiane retrouvée {statistics.median(bases[u][nom]):.1f}"
            print(ligne)
            for e in ex:
                print("      écart :", e)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], sys.argv[2])
