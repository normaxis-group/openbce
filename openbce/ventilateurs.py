# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Consommation des ventilateurs (auxiliaires de ventilation), fiche 6.5 C_VEN_Mécanique_SF.

En résidentiel, un caisson simple flux appelle une puissance constante, moyenne de la pointe et de la base pondérée
par la durée d'utilisation du grand débit (641, 643) ; elle est répartie entre les groupes au prorata des débits
repris (642). Les centrales double flux et le non résidentiel ne sont pas encore traités.
"""
from __future__ import annotations

HEURES_SEMAINE = 168.0
# Durée d'utilisation du grand débit, h/semaine (tableau 58), selon Type_Regul_Res des RSEE. L'ordre des codes n'est
# pas donné par le texte : il est déduit du banc (banc/ventilateurs.py).
DUGD = {0: 14.0, 1: 7.0}


def _moyenne(pointe: float, base: float, dugd: float) -> float:
    return (pointe * dugd + base * (HEURES_SEMAINE - dugd)) / HEURES_SEMAINE


def de_la_zone(zone) -> dict[int, float]:
    """Puissance moyenne des ventilateurs attribuée à chaque groupe de la zone, W, par Index de groupe."""
    if zone.entier("Usage") not in (1, 2):
        raise NotImplementedError("ventilateurs en non résidentiel")
    groupes = zone.directs("Groupe")
    r = {g.entier("Index"): 0.0 for g in groupes}
    for vm in zone.directs("Ventilation_Mecanique"):
        if vm.entier("Type_Ventilation_Mecanique", 0) != 0:
            raise NotImplementedError("centrale double flux")
        bouches = [(g.entier("Index"), b) for g in groupes for b in g.directs("Bouche_Conduit") if b.entier("Id_Systeme_Mecanique") == vm.entier("Index")]
        if not bouches:
            continue
        dugd = max(DUGD[b.entier("Type_Regul_Res", 0)] for _, b in bouches)                                    # (640)
        p = _moyenne(vm.nombre("Pvent_pointe_rep", 0.0) + vm.nombre("Pvent_pointe_souf", 0.0),
                     vm.nombre("Pvent_base_rep", 0.0) + vm.nombre("Pvent_base_souf", 0.0), dugd)               # (641, 643)
        debits = [(i, _moyenne(b.nombre("Qv_rep_pointe", 0.0) + b.nombre("Qv_souf_pointe", 0.0), b.nombre("Qv_rep_base", 0.0) + b.nombre("Qv_souf_base", 0.0), dugd)) for i, b in bouches]
        total = sum(q for _, q in debits)
        for i, q in debits:
            r[i] += p * (q / total if total > 0 else 1 / len(debits))                                          # (642)
    return r
