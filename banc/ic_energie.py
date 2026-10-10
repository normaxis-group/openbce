# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Banc de l'indicateur Ic énergie : à partir des énergies importées du récapitulatif énergétique (RSET, Sortie_Batiment_C),
recalcule Ic énergie et le compare à la partie environnementale du même fichier (RSEnv, sortie_projet/batiment/ic_energie),
quand elle existe. Valide la formule, les coefficients de pondération et les DE, indépendamment des consommations calculées.

    python -m banc.ic_energie <dossier de RSEE | fichiers>

Pour chaque sous-contributeur « énergie » du RSEnv, l'impact du module B divisé par Cef × 50 / Sref redonne la DE que la
référence a employée : affichée pour contrôle. Le seuil : rapport ic_energie_max / Ic énergie_maxmoyen comparé au rapport
O_Cep_nr_Max / Cep,nr_maxmoyen du RSET (même facteur de modulation attendu).
"""
import json
import re
import sys
from pathlib import Path

from openbce import carbone, exigences, rsee

CHAMPS_ELEC = {"ch": "ch", "fr": "fr", "ecs": "ecs", "ecl": "ecl", "aux_vent": "auxvent", "aux_dist": "auxdist", "dep": "deplacement"}
ENERGIES_COMBUSTIBLES = {"gaz": ("gaz",), "fioul": ("fioul",), "bois": ("bois", "boisgranchaud", "boisbuchchaud", "boisplaqchaud", "boisplaqpoel", "boisbuchpoel", "boisgranpoel"),
                         "reseau": ("reseau",)}


def imports_rset(b) -> dict[tuple[str, str], float]:
    """Énergies importées par (énergie, poste), kWh/m²/an, lues dans Sortie_Batiment_C."""
    imp = {}
    for poste, c in CHAMPS_ELEC.items():
        imp[("elec", poste)] = b.nombre(f"O_Cef_elec_imp_{c}_annuel", 0.0)
    for energie, prefixes in ENERGIES_COMBUSTIBLES.items():
        for poste in ("ch", "fr", "ecs"):
            imp[(energie, poste)] = sum(b.nombre(f"O_Cef_{p}_imp_{poste}_annuel", 0.0) for p in prefixes)
    return imp


def rsenv(chemin: str) -> list[dict]:
    """Par bâtiment du RSEnv : sref, ic_energie, ic_energie_max, ic_energie_maxmoyen et impacts B des sous-contributeurs énergie."""
    s = open(chemin, encoding="utf-8", errors="replace").read()
    i = s.find("<RSEnv")
    if i < 0:
        return []
    env = s[i:]
    j = env.find("<sortie_projet>")
    entree, sortie = env[:j], env[j:]
    bats = []
    for bi, bo in zip(re.findall(r"<batiment>(.*?)</batiment>", entree, re.S), re.findall(r"<batiment>(.*?)</batiment>", sortie, re.S)):
        d = dict(sref=float((re.search(r"<sref>([^<]*)<", bi) or [0, "0"])[1]))
        for k in ("ic_energie", "ic_energie_max", "ic_energie_maxmoyen"):
            m = re.search(rf"<{k}>\s*([^<\s]+)", bo)
            d[k] = float(m.group(1)) if m else None
        m_in, m_out = re.search(r"<energie>(.*?)</energie>", bi, re.S), re.search(r"<energie>(.*?)</energie>", bo, re.S)
        d["sous"] = []
        if m_in and m_out:
            noms = {m.group(1): dict(re.findall(r"<([a-z_]+)>([^<]*)<", m.group(2))) for m in re.finditer(r"<sous_contributeur ref=\"(\d+)\">(.*?)</sous_contributeur>", m_in.group(1), re.S)}
            for m in re.finditer(r"<sous_contributeur ref=\"(\d+)\">(.*?)</sous_contributeur>", m_out.group(1), re.S):
                ind = re.search(r"<indicateur ref=\"101\">(.*?)</indicateur>", m.group(2), re.S)
                b = float((re.search(r'ref="B">([^<]*)<', ind.group(1)) or [0, "0"])[1]) if ind else 0.0
                d["sous"].append((noms.get(m.group(1), {}).get("nom", ""), b))
        bats.append(d)
    return bats


def _poste_du_nom(nom: str) -> tuple[str, str] | None:
    n = nom.lower()
    energie = "gaz" if "gaz" in n else ("elec" if ("lectricit" in n or "électr" in n) else None)
    if energie is None:
        return None
    for cle, mots in (("ch", ("chauffage",)), ("fr", ("refroidissement", "climatisation")), ("ecs", ("ecs",)), ("ecl", ("clairage",)),
                      ("aux_vent", ("ventilation",)), ("dep", ("placement", "ascenseur"))):
        if any(w in n for w in mots):
            return energie, cle
    return energie, "autres"


def comparer(chemin: str) -> list[dict]:
    p = rsee.lire(chemin)
    env = rsenv(chemin)
    if not env:
        return []
    out = []
    bats = p.sortie.tous("Sortie_Batiment_C")
    for b, e in zip(bats, env):
        imp = imports_rset(b)
        r = carbone.ic_energie(imp)
        usage = next((z.entier("Usage") for bat in p.entree.directs("Batiment") if bat.entier("Index") == b.entier("Index") for z in bat.directs("Zone")), 2)
        de_obs = []
        for nom, bval in e["sous"]:
            k = _poste_du_nom(nom)
            cef = imp.get(k, 0.0) if k else 0.0
            if cef > 0 and bval > 0:
                de_obs.append((nom[:40], round(bval * e["sref"] / (cef * e["sref"]) / carbone.PER, 4) if False else round(bval / (cef * carbone.PER), 4)))
        fact_cep = b.nombre("O_Cep_nr_Max", 0.0) / exigences.CEP_NR_MAX_MOYEN.get(usage, 1.0) if usage in exigences.CEP_NR_MAX_MOYEN else None
        fact_ic = e["ic_energie_max"] / e["ic_energie_maxmoyen"] if e["ic_energie_max"] and e["ic_energie_maxmoyen"] else None
        out.append(dict(index=b.entier("Index"), sref=b.nombre("O_SREF", 0.0), sref_env=e["sref"], usage=usage, calc=r["ic_energie"], ref=e["ic_energie"],
                        annuel=r["ic_energie_annuel"], de_obs=de_obs, ignores=r["energies_ignorees"], fact_cep=fact_cep, fact_ic=fact_ic,
                        max_ref=e["ic_energie_max"], max_moyen=e["ic_energie_maxmoyen"]))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cibles = []
    for a in sys.argv[1:]:
        pth = Path(a)
        if pth.is_dir():
            lot = json.loads((pth / "_lot.json").read_text(encoding="utf-8"))["fichiers"]
            cibles += [pth / x["fichier"] for x in lot if "<RSEnv" in (pth / x["fichier"]).read_text(encoding="utf-8", errors="replace")]
        else:
            cibles.append(pth)
    rapports = []
    for chemin in cibles:
        for r in comparer(str(chemin)):
            if not r["ref"]:
                continue
            rapports.append(r["calc"] / r["ref"])
            print(f"{chemin.stem} bât {r['index']} usage {r['usage']} {r['sref']:6.0f} m² | Ic énergie {r['calc']:7.2f} / RSEnv {r['ref']:7.2f} kg/m² ({r['calc'] / r['ref'] - 1:+.1%}) ; annuel statique {r['annuel']:5.2f}"
                  f" | seuil : facteur Cep {r['fact_cep'] if r['fact_cep'] is None else round(r['fact_cep'], 4)} / facteur Ic {r['fact_ic'] if r['fact_ic'] is None else round(r['fact_ic'], 4)} (max RSEnv {r['max_ref']:.1f}, moyen {r['max_moyen']:.0f})"
                  + (f" | énergies sans DE {r['ignores']}" if r["ignores"] else ""))
            print("   DE observées (B / (Cef x 50)) :", r["de_obs"])
    if rapports:
        import statistics
        print(f"\n{len(rapports)} bâtiments : rapport médian {statistics.median(rapports):.4f}, min {min(rapports):.4f}, max {max(rapports):.4f}")
