# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des exigences : Bbio_max et ses modulations contre O_Bbio_Max et O_Mb* des RSEE (sans simulation).

    python -m banc.exigences <dossier de RSEE>
"""
import collections
import json
import sys
from pathlib import Path

from openbce import climat, exigences, rsee

CLES = (("mbgeo", "O_Mbgeo"), ("mbcombles", "O_Mbcombles"), ("mbsurf_moy", "O_Mbsurf_moy"), ("mbsurf_tot", "O_Mbsurf_tot"),
        ("mbbruit", "O_Mbbruit"), ("bbio_max", "O_Bbio_Max"))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dossier = Path(sys.argv[1])
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    ecarts, n, pires = collections.Counter(), 0, []
    for x in sorted(lot, key=lambda x: x["octets"]):
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        simu = p.entree.un("Simu")
        dep, alt = climat.departement(simu.texte("Departement")), simu.nombre("Altitude", 0)
        dates = [d.texte("date_depot_PC") for d in [p.administratif] + list(p.administratif.tous("Datas_Comp")) if d.texte("date_depot_PC")]
        depot = dates[0] if dates else ""
        # année du permis : date_depot_PC, sinon le millésime du format RSEE (année de l'étude), sinon l'année courante
        annee = int(depot[:4]) if depot[:4].isdigit() else (int(p.version_rsee[:4]) if p.version_rsee[:4].isdigit() else 2026)
        zone = climat.ZONE_CLIMATIQUE.get(dep)
        if zone is None:
            ecarts["zone inconnue"] += 1
            continue
        sorties = {(b.entier("Index"), z.entier("Index")): z for b in p.sortie.tous("Sortie_Batiment_B") for z in b.tous("Sortie_Zone_B")}
        for b in p.entree.directs("Batiment"):
            zones = b.directs("Zone")
            sref_usage = collections.Counter()
            for z in zones:
                for g in z.directs("Groupe"):
                    sref_usage[z.entier("Usage")] += g.nombre("SHAB") if z.entier("Usage") in (1, 2) else g.nombre("SU")
            for z in zones:
                s = sorties.get((b.entier("Index"), z.entier("Index")))
                if s is None:
                    continue
                g = z.directs("Groupe")[0]
                sg = s.tous("Sortie_Groupe_B")[0]
                usage = z.entier("Usage")
                if usage not in exigences.BBIO_MAX_MOYEN:
                    ecarts[f"usage {usage} non traité"] += 1
                    continue
                m = exigences.bbio_max(usage, zone, alt, s.nombre("O_SREF"), z.entier("NB_logement", 1), sref_usage[usage],
                                       g.nombre("S_combles", 0), g.entier("Exp_BR_Groupe", 1) or 3, g.entier("Categorie_CE", 1), annee)
                n += 1
                for cle, attendu in CLES:
                    ref = sg.nombre(attendu, 0.0)
                    if abs(m[cle] - ref) > (0.06 if cle == "bbio_max" else 0.0015):
                        ecarts[cle] += 1
                        if len(pires) < 40:
                            pires.append((x["projet"], z.texte("Name")[:18], usage, cle, round(m[cle], 4), ref,
                                          dict(dep=dep, zone=zone, alt=alt, sref=s.nombre("O_SREF"), nl=z.texte("NB_logement"),
                                               tot=round(sref_usage[usage], 1), br=g.texte("Exp_BR_Groupe"), ce=g.texte("Categorie_CE"))))
    # DH_max contre O_NbDegresHeures_max (Sortie_Groupe_D)
    n_dh, ecarts_dh, pires_dh = 0, 0, []
    for x in sorted(lot, key=lambda x: x["octets"]):
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        zone = climat.ZONE_CLIMATIQUE.get(climat.departement(p.entree.un("Simu").texte("Departement")))
        sd = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g for b in p.sortie.tous("Sortie_Batiment_D")
              for z in b.tous("Sortie_Zone_D") for g in z.tous("Sortie_Groupe_D")}
        for b in p.entree.directs("Batiment"):
            for z in b.directs("Zone"):
                for g in z.directs("Groupe"):
                    s = sd.get((b.entier("Index"), z.entier("Index"), g.entier("Index")))
                    usage = z.entier("Usage")
                    if s is None or usage not in exigences.BBIO_MAX_MOYEN or zone is None:
                        continue
                    smoy = sum(gg.nombre("SHAB") for gg in z.directs("Groupe")) / max(z.entier("NB_logement", 1), 1)
                    m = exigences.dh_max(usage, zone, g.entier("Categorie_CE", 1), g.entier("Is_Climatise", 0) == 1, smoy)
                    ref = s.nombre("O_NbDegresHeures_max", 0.0)
                    n_dh += 1
                    if m is None or abs(m - ref) > 0.6:
                        ecarts_dh += 1
                        if len(pires_dh) < 12:
                            pires_dh.append((x["projet"], z.texte("Name")[:16], usage, m, ref, zone, g.texte("Categorie_CE"), g.texte("Is_Climatise"), round(smoy, 1)))
    print(n, "groupes ; écarts :", dict(ecarts))
    print(n_dh, "groupes Th-D ; écarts DH_max :", ecarts_dh)
    for ligne in pires_dh:
        print("  ", ligne)
    for ligne in pires:
        print("  ", ligne)
