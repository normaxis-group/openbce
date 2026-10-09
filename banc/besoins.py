# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc d'essai des besoins : compare les besoins mensuels calculés à ceux du RSEE, groupe par groupe.

    python -m banc.besoins <rsee.xml> [<rsee.xml> ...]

"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np

from openbce import aeraulique, calendrier, climat, enveloppe, groupe, meteo, rsee, scenarios

METEO = Path(__file__).resolve().parent.parent / "donnees" / "meteo_re2020.npz"


def zone_climatique(projet) -> str:
    return climat.ZONE_CLIMATIQUE[climat.departement(projet.entree.un("Simu").texte("Departement"))]


def comparer(chemin: str) -> list[tuple]:
    projet = rsee.lire(chemin)
    simu = projet.entree.un("Simu")
    cl = climat.du_site(meteo.charger(METEO, zone_climatique(projet)), simu.texte("Departement"), simu.nombre("Altitude"))
    cal = calendrier.construire()
    lignes = []
    for bat in projet.entree.directs("Batiment"):
        b_tampons = enveloppe.coefficients_b(bat)
        sorties = {z.entier("Index"): z for sb in projet.sortie.tous("Sortie_Batiment_B") if sb.entier("Index") == bat.entier("Index") for z in sb.tous("Sortie_Zone_B")}
        for zone in bat.directs("Zone"):
            usage, sortie = zone.entier("Usage"), sorties.get(zone.entier("Index"))
            if usage not in (1, 2, 3) or sortie is None:
                continue
            groupes = zone.directs("Groupe")
            cle = "SHAB" if usage in (1, 2) else "SU"
            surface_zone = sum(g.nombre(cle) for g in groupes)
            if usage in (1, 2):
                sc = scenarios.habitation(cal, usage, surface_zone, max(zone.entier("NB_logement", 1), 1))
            else:
                sc = scenarios.tertiaire(cal, usage, surface_zone)
            ch, fr, ecl = np.zeros(12), np.zeros(12), np.zeros(12)
            for g in groupes:
                part = g.nombre(cle) / surface_zone
                sc_g = dataclasses.replace(sc, occupants=sc.occupants * part, apports_occupants=sc.apports_occupants * part,
                                           apports_usages=sc.apports_usages * part, nadeq=sc.nadeq * part)
                b = groupe.calculer(g, usage, cl, cal, sc_g, b_tampons, aeraulique.du_groupe(zone, g))
                for m in range(12):
                    ch[m] += b.chauffage[cal.mois_civil == m + 1].sum() / 1000 / surface_zone
                    fr[m] += b.refroidissement[cal.mois_civil == m + 1].sum() / 1000 / surface_zone
                    ecl[m] += b.eclairage[cal.mois_civil == m + 1].sum() / 1000 / surface_zone
            lignes.append((Path(chemin).name, zone.texte("Name"), usage, surface_zone, ch, np.array(sortie.mensuel("O_B_Ch_mois")), fr, np.array(sortie.mensuel("O_B_Fr_mois")), ecl, np.array(sortie.mensuel("O_B_Ecl_mois")), sortie.nombre("O_Bbio_pts_annuel", 0.0),
                           (sortie.nombre("O_B_Ch_annuel", 0.0), sortie.nombre("O_B_Fr_annuel", 0.0), sortie.nombre("O_B_Ecl_annuel", 0.0))))
    return lignes


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for chemin in sys.argv[1:]:
        try:
            lignes = comparer(chemin)
        except NotImplementedError as e:
            print(Path(chemin).name, "non traité :", e)
            continue
        for nom, zone, usage, surface, ch, ch_ref, fr, fr_ref, ecl, ecl_ref, bbio_ref, annuel in lignes:
            print(f"{nom} | {zone} | usage {usage} | {surface:.0f} m²")
            print("  chauffage calculé :", " ".join(f"{v:5.1f}" for v in ch), f"| an {ch.sum():6.1f}")
            print("  chauffage RSEE    :", " ".join(f"{v:5.1f}" for v in ch_ref), f"| an {ch_ref.sum():6.1f}  écart {ch.sum() / max(ch_ref.sum(), 1e-9) - 1:+.0%}")
            print("  froid calculé     :", " ".join(f"{v:5.1f}" for v in fr), f"| an {fr.sum():6.1f}")
            print("  éclairage calculé :", " ".join(f"{v:5.2f}" for v in ecl), f"| an {ecl.sum():6.2f}")
            print("  éclairage RSEE    :", " ".join(f"{v:5.2f}" for v in ecl_ref), f"| an {ecl_ref.sum():6.2f}  écart {ecl.sum() / max(ecl_ref.sum(), 1e-9) - 1:+.0%}")
            print("  froid RSEE        :", " ".join(f"{v:5.1f}" for v in fr_ref), f"| an {fr_ref.sum():6.1f}")
            bbio = 2 * ch.sum() + 2 * fr.sum() + 5 * ecl.sum()                # (2386)
            print(f"  Bbio calculé {bbio:.1f} points, RSEE {bbio_ref:.1f}, écart {bbio / max(bbio_ref, 1e-9) - 1:+.1%}")
