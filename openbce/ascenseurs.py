# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Consommation des ascenseurs (fiche 10.1 C_Bat_Ascenseurs), poste « déplacement des occupants ».

Le calcul est annuel par cabine (2275 à 2305). La répartition entre les zones desservies suit (2310).
Les équations (2300) et (2301) sont imprimées avec des signes incohérents d'un terme à l'autre ; elles sont
reprises ici sous leur forme physique : frottement toujours résistant, travail de la pesanteur (G - F).g compté
positif à la descente et négatif à la montée, énergie cinétique fournie au démarrage et rendue au freinage.

Deux points sont déduits des RSEE sans parking (banc/ascenseurs.py), le texte ne les donnant pas lisiblement :
- le nombre de personnes NB de la zone (2281) est le nombre d'adultes équivalents conventionnel, pas le Nocc saisi ;
- l'énergie Emoy de (2302) est la moyenne d'une montée et d'une descente, pas leur somme.
Avec ces deux lectures l'écart est inférieur à 4 % de la consommation des cabines. Dans les RSEE, le poste
« déplacement » contient aussi l'éclairage et la ventilation des parkings (fiches 10.3 et 10.4).
"""
from __future__ import annotations

G = 9.81                # m/s²
E_PORTE = 1188.0        # J par cycle d'ouverture et de fermeture
DECO = 1.2              # masse de la cabine vide rapportée à la charge utile
M_PASS = 75.0           # kg par passager (10.1.3.2)
P_VEILLE_PORTE = 13.0   # W
CF = 0.45               # m/s²
COR_CH = 1.1
COR_EMOBCAB = 0.9

BV = {2: 1600.0, 3: 1700.0}                      # voyages par personne et par an (tableau 311), par usage des RSEE
RG = (0.6, 0.8, 0.29, 0.6)                       # rendement global par TechMac (tableau 312)
ALPHA = (6.0, 0.0, 0.0, 6.0)                     # coefficient d'inertie (tableau 314)
SPECTRE = ((1.0, 0.0), (0.75, 0.1), (0.5, 0.1), (0.25, 0.3), (0.0, 0.5))   # (X, S), identique à la montée et à la descente (tableau 318)
P_MAN, P_BOUTON_PAL, P_IND_PAL, P_IND_CAB, P_FREIN, P_ALARME = 75.0, 0.0, 2.0, 5.0, 0.0, 10.0   # W, cabine immobile (tableau 317)
T_NUIT = {True: 8 * 365 * 3600.0, False: (12 * 365 + 52 * 48 + 9 * 24) * 3600.0}                 # habitation ou non (2295, 2296)
AN = 24 * 365 * 3600.0


def acceleration(v: float) -> float:
    return 0.5 if v <= 1 else (0.8 if v <= 2 else 1.2)                    # tableau 313


def eclairage_cabine(q: float) -> float:
    return 140.0 if q <= 630 else (210.0 if q <= 1275 else 280.0)         # tableau 316


def veille_par_defaut(q: float, netage: int) -> float:
    """Puissance de veille par défaut, W (2275)."""
    return P_MAN + (netage + 1) * (P_BOUTON_PAL + P_IND_PAL) + P_FREIN + P_VEILLE_PORTE + P_IND_CAB + eclairage_cabine(q) + P_ALARME


def _trajet(sens: int, x: float, z: float, q: float, v: float, a: float, cp: float, techmac: int) -> float:
    """Énergie mécanique d'un trajet de longueur z avec la charge x.q, J. sens = +1 à la descente, -1 à la montée."""
    p = DECO * q
    g_ = p + cp * q                                 # contrepoids (2290)
    f = p + x * q                                   # cabine en charge (2299)
    mi = ALPHA[techmac] * (g_ + p)                  # masse d'inertie (2291)
    d = v * v / (2 * a)                             # distance de démarrage ou de freinage
    frott, pes, cin = (g_ + f) * CF, sens * (g_ - f) * G, (g_ + f + mi) * v * v / 2
    return max(0.0, (frott + pes) * d + cin) + max(0.0, (frott + pes) * (z - d)) + max(0.0, (frott + pes) * d - cin)


def cabine(asc, personnes_voyages: float, habitation: bool) -> float:
    """Consommation annuelle d'une cabine, Wh (2305). `personnes_voyages` est le besoin de voyages BVNB (2283)."""
    q, v, h, netage, techmac = asc.nombre("Q"), asc.nombre("V"), asc.nombre("H"), asc.entier("Netage"), asc.entier("TechMac")
    cp = -1.2 if techmac == 2 else asc.nombre("Cp", 0.5)
    if asc.entier("ScVeille", 0) == 1:
        pti, dp1, t1, dp2, t2 = (asc.nombre(k) for k in ("Pti", "dP1", "T1", "dP2", "T2"))
    else:
        pti, dp1, t1, dp2, t2 = veille_par_defaut(q, netage), 0.0, 86400.0, 0.0, 86400.0       # (2275 à 2279)
    ndem = personnes_voyages * M_PASS / (q * 0.2)                                              # (2284)
    a = acceleration(v)
    ch = (netage + 1) / (netage + 2) * COR_CH                                                  # (2287)
    tmob = (ch * h / v + v / a) * ndem                                                         # (2292)
    t_nuit = T_NUIT[habitation]
    t_jour = max(0.0, AN - tmob - t_nuit)                                                      # (2294, 2298)
    emoy = sum(s * (_trajet(-1, x, ch * h, q, v, a, cp, techmac) + _trajet(+1, x, ch * h, q, v, a, cp, techmac)) / 2 for x, s in SPECTRE) / RG[techmac]   # (2302)
    etm = (emoy * COR_EMOBCAB * ndem / 2 + E_PORTE * ndem + pti * tmob) / 3600                 # (2303)

    def veille(duree, arrets):
        if duree <= 0:
            return 0.0
        pause = duree / arrets if arrets > 0 else float("inf")
        return (dp1 * min(1.0, t1 / pause) + dp2 * min(1.0, (t1 + t2) / pause) + (pti - dp1 - dp2)) * duree / 3600

    return etm + veille(t_jour, ndem) + veille(t_nuit, 365)                                    # (2304, 2305)


def occupants_conventionnels(batiment) -> dict[int, float]:
    """Nombre de personnes de chaque zone pour le besoin de voyages : adultes équivalents en habitation, Nocc sinon."""
    from .calendrier import adultes_equivalents
    r = {}
    for z in batiment.directs("Zone"):
        shab = sum(g.nombre("SHAB", 0.0) for g in z.directs("Groupe"))
        if z.entier("Usage") in (1, 2) and shab > 0:
            r[z.entier("Index")] = adultes_equivalents(z.entier("Usage"), shab, max(z.entier("NB_logement", 1), 1))
        else:
            r[z.entier("Index")] = z.nombre("Nocc", 0.0)
    return r


def du_batiment(batiment, occupants: dict[int, float]) -> dict[int, float]:
    """Consommation annuelle des ascenseurs attribuée à chaque zone, Wh, par Index de zone.

    `occupants` donne le nombre d'adultes équivalents de chaque zone (2281), voir `occupants_conventionnels`.
    """
    usages = {z.entier("Index"): z.entier("Usage") for z in batiment.directs("Zone")}
    cabines = [(a, [int(i) for i in a.texte("C").split()]) for a in batiment.directs("Ascenseur")]
    q_zone = {z: sum(a.nombre("Q") for a, zones in cabines if z in zones) for z in usages}                    # (2280)
    conso = dict.fromkeys(usages, 0.0)
    for a, zones in cabines:
        if any(usages[z] not in BV for z in zones):
            raise NotImplementedError("ascenseur desservant un usage sans besoin de voyages tabulé")
        bvnb = sum(a.nombre("Q") / q_zone[z] * BV[usages[z]] * occupants[z] for z in zones)                   # (2283)
        e = cabine(a, bvnb, all(usages[z] in (1, 2) for z in zones))
        total = sum(q_zone[z] for z in zones)
        for z in zones:
            conso[z] += e * q_zone[z] / total                                                                 # (2310)
    return conso
