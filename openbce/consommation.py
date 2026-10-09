# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Consommations du mode Th-C (Cep), premier bloc : auxiliaires de ventilation (fiche 6.5, 636 à 646) et conversion
en énergie primaire (annexe à l'article R. 172-4, chapitre III : électricité 2,3, autres énergies 1).

Les puissances des ventilateurs sont des données des systèmes « Ventilation_Mecanique » : en résidentiel, la
puissance est moyennée sur la semaine avec la durée d'utilisation du grand débit (641, 643) et s'applique à toutes
les heures ; en non résidentiel, elle suit l'indicateur de ventilation Ivent (636 à 639). Elle est répartie entre les
groupes desservis au prorata de leurs débits spécifiques (642, 644).
"""
from __future__ import annotations

import numpy as np

from . import ventilation
from .rsee import Noeud

COEF_EP_ELEC = 2.3        # kWhep par kWhef d'électricité
COEF_EP_AUTRE = 1.0


def puissance_ventilateurs(zone: Noeud, groupe: Noeud, usage: int, ivent: np.ndarray) -> np.ndarray:
    """Puissance électrique des ventilateurs attribuée au groupe, en W, par heure."""
    n = len(ivent)
    total = np.zeros(n)
    systemes = {v.entier("Index"): v for v in zone.directs("Ventilation_Mecanique")}
    # débits spécifiques par (système, groupe) pour la répartition (642, 644)
    debits: dict[int, dict[int, float]] = {}
    for g in zone.directs("Groupe"):
        for b in g.directs("Bouche_Conduit"):
            sens = "souf" if b.entier("Type_Bouche_Conduit", 0) == 1 else "rep"
            q = float(ventilation._debit_bouche(b, usage, sens, ivent).mean())
            debits.setdefault(b.entier("Id_Systeme_Mecanique", 0), {}).setdefault(g.entier("Index"), 0.0)
            debits[b.entier("Id_Systeme_Mecanique", 0)][g.entier("Index")] += q
    for id_sys, par_groupe in debits.items():
        vm = systemes.get(id_sys)
        if vm is None:
            continue
        part = par_groupe.get(groupe.entier("Index"), 0.0) / max(sum(par_groupe.values()), 1e-9)
        if part <= 0:
            continue
        if usage in (1, 2):
            codes = [b.entier("Type_Regul_Res", 0) for g in zone.directs("Groupe") for b in g.directs("Bouche_Conduit") if b.entier("Id_Systeme_Mecanique", 0) == id_sys]
            dugd = ventilation.DUGD.get(max(set(codes), key=codes.count) if codes else 0, 14.0)   # tableau 58 (voir ventilation.DUGD)
            for sens in ("rep", "souf"):
                pointe, base = vm.nombre(f"Pvent_pointe_{sens}", 0.0), vm.nombre(f"Pvent_base_{sens}", 0.0)
                total += part * (pointe * dugd + base * (168.0 - dugd)) / 168.0            # (641), (643)
        else:
            for sens in ("rep", "souf"):
                occ, inocc = vm.nombre(f"Pvent_{sens}_occ", 0.0), vm.nombre(f"Pvent_{sens}_inocc", 0.0)
                total += part * np.where(ivent > 0, occ, inocc)                             # (636) à (639)
    return total
