# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc des bilans Th-C (fiches 13.2 à 13.4, 4.7), sans simulation : identités internes des RSEE et postes forfaitaires.

    python -m banc.bilans <dossier de RSEE>

Vérifie, à partir des sorties des RSEE eux-mêmes : O_Cep_annuel = somme des O_Cef_<énergie>_imp_annuel x coefficient
d'énergie primaire (zone et bâtiment) ; O_Cep_annuel_occ = O_Cep_annuel x SREF / somme des Nocc ; le forfait de
refroidissement des groupes non climatisés (O_Cef_fr_annuel du groupe contre 2494 avec O_NbDegresHeures et
O_NbDegresHeures_max du Th-D) ; les usages mobiliers de la zone contre les apports internes du scénario conventionnel.
"""
import collections
import json
import statistics
import sys
from pathlib import Path

from openbce import bilans, calendrier, climat, rsee, scenarios


def main(dossier: Path) -> None:
    lot = json.loads((dossier / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
    cal = calendrier.construire()
    cep_ecarts, occ_ecarts, forf, mob = [], [], [], collections.defaultdict(list)
    vus = set()
    for x in sorted(lot, key=lambda x: x["octets"]):
        if x["projet"] in vus:
            continue
        try:
            p = rsee.lire(dossier / x["fichier"])
        except Exception:
            continue
        vus.add(x["projet"])
        simu = p.entree.un("Simu")
        zone_clim = climat.ZONE_CLIMATIQUE.get(climat.departement(simu.texte("Departement")))
        alt = simu.nombre("Altitude", 0.0)
        dh_groupes = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): g for b in p.sortie.tous("Sortie_Batiment_D")
                      for z in b.tous("Sortie_Zone_D") for g in z.tous("Sortie_Groupe_D")}
        entrees = {(b.entier("Index"), z.entier("Index"), g.entier("Index")): (b, z, g) for b in p.entree.directs("Batiment")
                   for z in b.directs("Zone") for g in z.directs("Groupe")}
        for sb in p.sortie.tous("Sortie_Batiment_C"):
            for noeud in [sb] + list(sb.tous("Sortie_Zone_C")):
                cef = {e: noeud.nombre(f"O_Cef_{e}_imp_annuel", 0.0) for e in bilans.ENERGIES.values()}
                if any(cef.values()):
                    cep_ecarts.append(bilans.cep(cef) - noeud.nombre("O_Cep_annuel", 0.0))
            nocc = sum(z.nombre("Nocc", 0.0) for z in sb.tous("Sortie_Zone_C"))
            if nocc > 0 and sb.nombre("O_Cep_annuel_occ", 0.0):
                occ_ecarts.append(sb.nombre("O_Cep_annuel", 0.0) * sb.nombre("O_SREF", 0.0) / nocc / sb.nombre("O_Cep_annuel_occ") - 1)
            for sz in sb.tous("Sortie_Zone_C"):
                for sg in sz.tous("Sortie_Groupe_C"):
                    cle = (sb.entier("Index"), sz.entier("Index"), sg.entier("Index"))
                    d = dh_groupes.get(cle)
                    e = entrees.get(cle)
                    if d is None or e is None or zone_clim is None:
                        continue
                    bat, zone, g = e
                    usage = zone.entier("Usage")
                    if g.entier("Is_Climatise", 0) == 0 and usage in bilans.COEF_FR_PAR_DH:
                        f = bilans.forfait_froid(usage, False, d.nombre("O_NbDegresHeures", 0.0), d.nombre("O_NbDegresHeures_max", 0.0) or None, zone_clim, alt)
                        forf.append((x["projet"], sg.texte("Name")[:14], round(f, 2), sg.nombre("O_Cef_fr_annuel", 0.0), round(d.nombre("O_NbDegresHeures", 0.0))))
                # usages mobiliers de la zone
                z_e = next((z for b in p.entree.directs("Batiment") if b.entier("Index") == sb.entier("Index") for z in b.directs("Zone") if z.entier("Index") == sz.entier("Index")), None)
                if z_e is not None and z_e.entier("Usage") in (1, 2, 3):
                    usage = z_e.entier("Usage")
                    surface = sum(g.nombre("SHAB" if usage in (1, 2) else "SU") for g in z_e.directs("Groupe"))
                    if surface > 0:
                        sc = scenarios.habitation(cal, usage, surface, max(z_e.entier("NB_logement", 1), 1)) if usage in (1, 2) else scenarios.tertiaire(cal, usage, surface)
                        mob[usage].append((bilans.mobilier(sc.apports_usages, surface), sz.nombre("O_Cef_imp_mobilier_annuel", 0.0)))
    print(f"Cep = somme Cef x coefficient : {len(cep_ecarts)} nœuds, |écart| max {max(abs(e) for e in cep_ecarts):.2f} kWhep/m², médian {statistics.median(abs(e) for e in cep_ecarts):.3f}")
    print(f"Cep par occupant : {len(occ_ecarts)} bâtiments, |écart| max {max(abs(e) for e in occ_ecarts):.2%}")
    for u, l in sorted(mob.items()):
        print(f"mobilier usage {u} : {len(l)} zones, calculé {statistics.median(a for a, _ in l):.2f} / RSEE {statistics.median(b for _, b in l):.2f} kWh/m² (médianes), |écart| médian {statistics.median(abs(a - b) for a, b in l):.2f}")
    if forf:
        ecarts = [a - b for _, _, a, b, _ in forf]
        print(f"forfait de refroidissement : {len(forf)} groupes non climatisés, |écart| médian {statistics.median(abs(e) for e in ecarts):.2f} kWh/m², max {max(abs(e) for e in ecarts):.2f}")
        for ligne in sorted(forf, key=lambda t: -abs(t[2] - t[3]))[:8]:
            print("  ", ligne)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(Path(sys.argv[1]))
