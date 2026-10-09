# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Serveur MCP (Model Context Protocol) d'OpenBCE, en stdio, sans dépendance hors bibliothèque standard.

    python -m openbce.serveur_mcp

Il expose le moteur à un assistant (Claude, ou tout client MCP) sous forme d'outils :

- `version` : version du moteur, texte suivi, couverture et réserves ;
- `lire_rsee` : résumé des entrées d'un RSEE et des sorties de référence qu'il porte (rapide, sans calcul) ;
- `calculer` : recalcul d'un RSEE (Bbio, Cep, DH par bâtiment), RSEE recalculé écrit sur disque ;
- `comparer` : recalcul puis comparaison champ à champ aux sorties de référence du même RSEE ;
- `variante` : modification de champs de `Entree_Projet`, recalcul, écarts avec le projet initial.

Un calcul dure de 30 secondes à 40 minutes selon la taille du projet. Quand le client fournit un `progressToken`, le
serveur envoie une notification de progression toutes les 15 secondes pendant le calcul, ce qui permet aux clients qui
le gèrent de ne pas abandonner la requête. Les RSEE sont lus sur le disque local, par leur chemin ; rien ne sort de la
machine. Les résultats ne sont pas opposables (voir docs/validation.md).

Le protocole est celui de MCP sur stdio : un message JSON-RPC 2.0 par ligne, en UTF-8. Les journaux vont sur stderr ;
stdout est réservé au protocole.
"""
from __future__ import annotations

import contextlib
import json
import shutil
import sys
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))          # le pilote d'assemblage vit dans banc/, comme pour l'API

from openbce import api, rsee  # noqa: E402

VERSIONS_PROTOCOLE = ("2025-06-18", "2025-03-26", "2024-11-05")
PERIODE_PROGRESSION = 15.0                    # secondes
RESERVES = ("OpenBCE n'est pas un logiciel évalué au sens du règlement d'évaluation des logiciels RE2020 : ses "
            "résultats ne sont pas opposables, ne valent ni attestation ni étude réglementaire. Précision mesurée sur "
            "50 opérations réelles : Cep à -0,2 % en médiane, écart absolu médian 1,5 %, 49 dans ±10 % ; écarts connus "
            "sur le froid Th-C des logements climatisés et les PAC multiservices (docs/validation.md).")
INSTRUCTIONS = ("Outils de recalcul d'études RE2020 à partir de leur RSEE (fichier XML). Commencer par lire_rsee pour "
                "connaître le projet. calculer, comparer et variante lancent la simulation horaire : compter de 30 s à "
                "40 min par calcul (variante en fait deux). Toujours rappeler à l'utilisateur que les résultats ne sont "
                "pas opposables. " + RESERVES)

_CHEMIN = {"type": "string", "description": "chemin absolu d'un RSEE (XML) sur la machine du serveur"}
OUTILS = [
    dict(name="version", title="Version d'OpenBCE",
         description="Version du moteur, texte réglementaire suivi, couverture de la méthode et réserves d'usage.",
         inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
         annotations={"readOnlyHint": True, "openWorldHint": False}),
    dict(name="lire_rsee", title="Lire un RSEE",
         description="Résume un RSEE sans calcul : versions, site, zone climatique, bâtiments, zones (usage, surfaces, "
                     "nombre de groupes et de logements), composition (parois, baies, émetteurs, générations), et sorties "
                     "de référence portées par le fichier (Bbio, Cep, DH). Rapide.",
         inputSchema={"type": "object", "properties": {"chemin": _CHEMIN}, "required": ["chemin"], "additionalProperties": False},
         annotations={"readOnlyHint": True, "openWorldHint": False}),
    dict(name="calculer", title="Recalculer un RSEE",
         description="Recalcule le RSEE avec OpenBCE : Bbio, Cep, Cef, DH et Bbio_max par bâtiment. Écrit le RSEE recalculé "
                     "(bloc Sortie_Projet remplacé) et en rend le chemin. Durée : 30 s à 40 min. Résultats non opposables.",
         inputSchema={"type": "object", "properties": {
             "chemin": _CHEMIN,
             "sortie": {"type": "string", "description": "chemin du RSEE recalculé à écrire (par défaut : dossier temporaire)"}},
             "required": ["chemin"], "additionalProperties": False},
         annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}),
    dict(name="comparer", title="Comparer au calcul de référence",
         description="Recalcule le RSEE puis compare, champ par champ, les sorties d'OpenBCE à celles que porte le fichier "
                     "(calculées par le logiciel évalué qui l'a produit) : besoins, Bbio, Bbio_max, consommations par poste, "
                     "Cep, degrés-heures. Durée : celle d'un calcul.",
         inputSchema={"type": "object", "properties": {"chemin": _CHEMIN}, "required": ["chemin"], "additionalProperties": False},
         annotations={"readOnlyHint": True, "openWorldHint": False}),
    dict(name="variante", title="Étudier une variante",
         description="Modifie un ou plusieurs champs de Entree_Projet (copie du fichier, l'original n'est pas touché), "
                     "recalcule et rend les écarts de Bbio, Cep et DH avec le projet initial. Un champ se désigne par son "
                     "chemin sous Entree_Projet, noms des éléments séparés par « / », sans les niveaux « _Collection », "
                     "avec un rang facultatif entre crochets (à partir de 1) : « Batiment/Zone[2]/Groupe/Permeabilite/Q4PaSurf ». "
                     "Sans rang, toutes les occurrences sont modifiées. Durée : deux calculs.",
         inputSchema={"type": "object", "properties": {
             "chemin": _CHEMIN,
             "modifications": {"type": "array", "minItems": 1, "items": {"type": "object", "properties": {
                 "champ": {"type": "string", "description": "chemin du champ sous Entree_Projet"},
                 "valeur": {"type": "string", "description": "nouvelle valeur, telle qu'écrite dans le XML"}},
                 "required": ["champ", "valeur"], "additionalProperties": False}},
             "calculer_base": {"type": "boolean", "default": True,
                               "description": "recalculer aussi le projet initial pour donner les écarts (sinon, la variante seule)"}},
             "required": ["chemin", "modifications"], "additionalProperties": False},
         annotations={"readOnlyHint": True, "openWorldHint": False}),
]


class ErreurOutil(Exception):
    """Erreur d'usage d'un outil : rendue au client comme résultat en erreur, pas comme erreur de protocole."""


# --- outils ----------------------------------------------------------------------------------------------------------

def _fichier(arguments: dict) -> Path:
    chemin = Path(str(arguments.get("chemin", ""))).expanduser()
    if not chemin.is_file():
        raise ErreurOutil(f"RSEE introuvable : {chemin}")
    return chemin


def _usage(code: int) -> str:
    from openbce import scenarios
    return scenarios._tables().get(str(code), {}).get("nom", f"usage {code}")


def outil_version(_arguments: dict) -> dict:
    return dict(moteur="OpenBCE", version=api.VERSION, texte=api.CORPUS,
                couverture=("logement individuel et collectif, bureaux en partie ; effet joule, PAC électriques à source air, "
                            "chaudières gaz et fioul, réseaux de chaleur et de froid, ballons et chauffe-eau thermodynamiques, "
                            "ventilation simple et double flux, éclairage, ascenseurs et parkings. Non couverts : Ic, "
                            "photovoltaïque, solaire thermique, espaces tampons, Titre V, tertiaire hors bureaux."),
                reserves=RESERVES)


def outil_lire_rsee(arguments: dict) -> dict:
    projet = rsee.lire(_fichier(arguments))
    e, s = projet.entree, projet.sortie
    simu = next(iter(e.tous("Simu")), None)
    try:
        from banc.besoins import zone_climatique
        zone_clim = zone_climatique(projet)
    except Exception:                                                  # département absent ou inconnu
        zone_clim = None
    batiments = []
    for bat in e.directs("Batiment"):
        zones = []
        for z in bat.directs("Zone"):
            u = z.entier("Usage", 0)
            groupes = z.directs("Groupe")
            cle = "SHAB" if u in (1, 2) else "SU"
            zones.append(dict(index=z.entier("Index", 0), nom=z.texte("Name"), usage=u, usage_txt=_usage(u),
                              surface=round(sum(g.nombre(cle, 0.0) for g in groupes), 1), surface_type=cle,
                              groupes=len(groupes), logements=z.entier("NB_logement", 0) if u in (1, 2) else None,
                              climatise=any(g.entier("Is_Climatise", 0) == 1 for g in groupes)))
        ref_b = next((x for x in s.tous("Sortie_Batiment_B") if x.entier("Index", 0) == bat.entier("Index", 0)), None)
        ref_c = next((x for x in s.tous("Sortie_Batiment_C") if x.entier("Index", 0) == bat.entier("Index", 0)), None)
        batiments.append(dict(index=bat.entier("Index", 0), nom=bat.texte("Name"), zones=zones,
                              composition={k: len(bat.tous(k)) for k in ("Paroi_Opaque", "Baie", "Lineaire", "Emetteur", "Emetteur_ECS")},
                              reference=dict(bbio_pts=ref_b.nombre("O_Bbio_pts_annuel", None) if ref_b and "O_Bbio_pts_annuel" in ref_b.valeurs else None,
                                             cep=ref_c.nombre("O_Cep_annuel") if ref_c and "O_Cep_annuel" in ref_c.valeurs else None)))
    return dict(fichier=str(projet.chemin), version_rsee=projet.version_rsee, version_moteur_reference=projet.version_moteur,
                departement=simu.texte("Departement") if simu else None, altitude=simu.nombre("Altitude", 0.0) if simu else None,
                zone_climatique=zone_clim, generations=len(e.tous("Generation")), batiments=batiments)


def _calculer(entree: Path, sortie: Path) -> dict:
    debut = time.monotonic()
    resume = api.calculer_rsee(entree, sortie)
    resume["duree_s"] = round(time.monotonic() - debut, 1)
    return resume


def _sortie_temporaire(entree: Path, suffixe: str) -> Path:
    return Path(tempfile.mkdtemp(prefix="openbce_mcp_")) / f"{entree.stem}_{suffixe}.xml"


def outil_calculer(arguments: dict) -> dict:
    entree = _fichier(arguments)
    sortie = Path(arguments["sortie"]).expanduser() if arguments.get("sortie") else _sortie_temporaire(entree, "openbce")
    if sortie.resolve() == entree.resolve():
        raise ErreurOutil("la sortie ne peut pas remplacer le RSEE d'entrée")
    resume = _calculer(entree, sortie)
    return dict(resume, rsee_recalcule=str(sortie), reserves=RESERVES)


def outil_comparer(arguments: dict) -> dict:
    entree = _fichier(arguments)
    sortie = _sortie_temporaire(entree, "openbce")
    resume = _calculer(entree, sortie)
    from banc import sortie_rsee as pilote
    lignes = [{k: (None if isinstance(v, float) and v != v else v) for k, v in e.items()}       # NaN : champ absent
              for e in pilote.ecarts(rsee.lire(entree), rsee.lire(sortie))]
    return dict(resume=resume, comparaison=lignes, rsee_recalcule=str(sortie), reserves=RESERVES)


def _pas(texte: str) -> tuple[str, int | None]:
    if texte.endswith("]") and "[" in texte:
        nom, rang = texte[:-1].split("[", 1)
        if not rang.isdigit() or int(rang) < 1:
            raise ErreurOutil(f"rang invalide dans « {texte} »")
        return nom, int(rang)
    return texte, None


def _enfants(el: ET.Element, nom: str) -> list[ET.Element]:
    """Enfants de nom donné, en traversant les niveaux « _Collection » (aplatis comme dans openbce.rsee)."""
    trouves = []
    for e in el:
        local = e.tag.split("}")[-1]
        if local == nom:
            trouves.append(e)
        elif local.lower().endswith("_collection"):
            trouves.extend(_enfants(e, nom))
    return trouves


def appliquer_modifications(racine: ET.Element, modifications: list[dict]) -> list[dict]:
    """Applique les modifications sous Entree_Projet ; rend, pour chacune, le nombre de champs modifiés."""
    entree = next((e for e in racine.iter() if e.tag.split("}")[-1] == "Entree_Projet"), None)
    if entree is None:
        raise ErreurOutil("bloc Entree_Projet absent")
    bilan = []
    for m in modifications:
        champ, valeur = str(m.get("champ", "")).strip("/"), str(m.get("valeur", ""))
        if not champ:
            raise ErreurOutil("modification sans champ")
        noeuds = [entree]
        for pas in champ.split("/"):
            nom, rang = _pas(pas)
            suivants = []
            for n in noeuds:
                trouves = _enfants(n, nom)
                suivants.extend(trouves if rang is None else trouves[rang - 1:rang])
            noeuds = suivants
        if not noeuds:
            raise ErreurOutil(f"champ introuvable : {champ}")
        if any(len(n) for n in noeuds):
            raise ErreurOutil(f"« {champ} » désigne un élément composé, pas un champ")
        anciennes = sorted({(n.text or "").strip() for n in noeuds})
        for n in noeuds:
            n.text = valeur
        bilan.append(dict(champ=champ, valeur=valeur, occurrences=len(noeuds), anciennes_valeurs=anciennes[:10]))
    return bilan


def outil_variante(arguments: dict) -> dict:
    entree = _fichier(arguments)
    modifications = arguments.get("modifications") or []
    if not modifications:
        raise ErreurOutil("aucune modification")
    dossier = Path(tempfile.mkdtemp(prefix="openbce_mcp_"))
    arbre = ET.parse(entree)
    bilan = appliquer_modifications(arbre.getroot(), modifications)
    fichier_variante = dossier / f"{entree.stem}_variante_entree.xml"
    arbre.write(fichier_variante, encoding="utf-8", xml_declaration=True)
    variante = _calculer(fichier_variante, dossier / f"{entree.stem}_variante_openbce.xml")
    resultat = dict(modifications=bilan, variante=variante, rsee_variante=str(fichier_variante), reserves=RESERVES)
    if arguments.get("calculer_base", True):
        base = _calculer(entree, dossier / f"{entree.stem}_base_openbce.xml")
        ecarts = []
        for b0, b1 in zip(base["batiments"], variante["batiments"]):
            ecarts.append({k: round(b1[k] - b0[k], 2) for k in ("bbio_pts", "cep", "cef", "dh_max_groupes")} | {"batiment": b0["batiment"]})
        resultat.update(base=base, ecarts=ecarts)
    return resultat


EXECUTEURS = dict(version=outil_version, lire_rsee=outil_lire_rsee, calculer=outil_calculer, comparer=outil_comparer,
                  variante=outil_variante)


# --- protocole -------------------------------------------------------------------------------------------------------

class Serveur:
    def __init__(self, sortie=None):
        self._sortie = sortie or sys.stdout
        self._verrou = threading.Lock()

    def envoyer(self, message: dict) -> None:
        with self._verrou:
            self._sortie.write(json.dumps(message, ensure_ascii=False) + "\n")
            self._sortie.flush()

    def _appeler(self, nom: str, arguments: dict, jeton) -> dict:
        resultat: dict = {}

        def travail():
            try:
                with contextlib.redirect_stdout(sys.stderr):          # aucun affichage du moteur ne doit polluer le protocole
                    resultat["donnees"] = EXECUTEURS[nom](arguments)
            except ErreurOutil as e:
                resultat["erreur"] = str(e)
            except Exception as e:                                       # erreur de calcul : rendue, jamais masquée
                resultat["erreur"] = f"{type(e).__name__} : {e}"

        fil = threading.Thread(target=travail, daemon=True)
        debut = time.monotonic()
        fil.start()
        n = 0
        while fil.is_alive():
            fil.join(PERIODE_PROGRESSION)
            if fil.is_alive() and jeton is not None:
                n += 1
                self.envoyer({"jsonrpc": "2.0", "method": "notifications/progress",
                              "params": {"progressToken": jeton, "progress": n,
                                         "message": f"calcul en cours depuis {int(time.monotonic() - debut)} s"}})
        if "erreur" in resultat:
            return {"content": [{"type": "text", "text": resultat["erreur"]}], "isError": True}
        donnees = resultat["donnees"]
        return {"content": [{"type": "text", "text": json.dumps(donnees, ensure_ascii=False, indent=1)}],
                "structuredContent": donnees, "isError": False}

    def traiter(self, message: dict) -> dict | None:
        """Traite un message JSON-RPC ; rend la réponse, ou None pour une notification."""
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or "method" not in message:
            return {"jsonrpc": "2.0", "id": message.get("id") if isinstance(message, dict) else None,
                    "error": {"code": -32600, "message": "requête invalide"}}
        methode, ident, params = message["method"], message.get("id"), message.get("params") or {}
        if ident is None:                                                 # notification (initialized, cancelled...)
            return None
        reponse = {"jsonrpc": "2.0", "id": ident}
        if methode == "initialize":
            demandee = params.get("protocolVersion")
            reponse["result"] = {
                "protocolVersion": demandee if demandee in VERSIONS_PROTOCOLE else VERSIONS_PROTOCOLE[0],
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "openbce", "title": "OpenBCE, moteur RE2020 libre", "version": api.VERSION},
                "instructions": INSTRUCTIONS}
        elif methode == "ping":
            reponse["result"] = {}
        elif methode == "tools/list":
            reponse["result"] = {"tools": OUTILS}
        elif methode == "tools/call":
            nom = params.get("name")
            if nom not in EXECUTEURS:
                reponse["error"] = {"code": -32602, "message": f"outil inconnu : {nom}"}
            else:
                jeton = (params.get("_meta") or {}).get("progressToken")
                reponse["result"] = self._appeler(nom, params.get("arguments") or {}, jeton)
        else:
            reponse["error"] = {"code": -32601, "message": f"méthode non prise en charge : {methode}"}
        return reponse

    def servir(self, entree=None) -> None:
        for ligne in entree or sys.stdin:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                message = json.loads(ligne)
            except json.JSONDecodeError as e:
                self.envoyer({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"JSON invalide : {e}"}})
                continue
            for m in message if isinstance(message, list) else [message]:
                reponse = self.traiter(m)
                if reponse is not None:
                    self.envoyer(reponse)


def main() -> None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    print(f"OpenBCE {api.VERSION} : serveur MCP sur stdio", file=sys.stderr, flush=True)
    Serveur().servir()


if __name__ == "__main__":
    main()
