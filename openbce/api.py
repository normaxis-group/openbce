# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""API HTTP du moteur, sans dépendance hors bibliothèque standard (cahier des charges §4 : un conteneur exposant une API).

    python -m openbce.api [--hote 0.0.0.0] [--port 8765]

Points d'accès :
    GET  /version            -> {"moteur": "openbce", "version": ..., "corpus": ...}
    POST /calcul             corps : le RSEE d'entrée (XML) ; réponse : le RSEE recalculé (XML), bloc Sortie_Projet
                             remplacé ; en-tête X-Openbce-Resume : résumé JSON (Bbio, Cep, DH par bâtiment)
    POST /calcul?format=json corps : le RSEE d'entrée ; réponse : le résumé JSON seul

Le calcul est synchrone et déterministe ; il dure de quelques dizaines de secondes à quelques minutes par projet selon
le nombre de groupes (objectif du cahier des charges : moins de 10 s, non atteint en Python pur). Le RSEE reçu est
écrit dans un dossier temporaire le temps du calcul puis effacé : rien n'est conservé côté moteur.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VERSION = "0.1.0"
CORPUS = "annexe III de l'arrêté du 4 août 2021 modifié, méthode Th-BCE 2020 (texte du corpus local)"


def calculer_rsee(chemin_entree: Path, chemin_sortie: Path) -> dict:
    """Recalcule un RSEE et écrit le fichier de sortie ; rend le résumé par bâtiment."""
    from banc import sortie_rsee as pilote          # le pilote d'assemblage vit dans le banc tant que l'API n'a pas son propre orchestrateur
    from openbce import sortie_rsee
    calcul = pilote.calculer(str(chemin_entree))
    el = sortie_rsee.construire(calcul, calcul["version"], calcul["departement"], calcul["altitude"])
    sortie_rsee.ecrire(chemin_entree, el, chemin_sortie)
    resume = []
    for bat in calcul["batiments"]:
        groupes = [g for z in bat["zones"] for g in z["groupes"]]
        sref = sum(g["sref"] for g in groupes) or 1.0
        bbio = sum(g["sref"] * (2 * sum(g["b_ch_mois"]) + 2 * sum(g["b_fr_mois"]) + 5 * sum(g["b_ecl_mois"])) for g in groupes) / sref
        dh = max((g["dh"] or 0.0) for g in groupes) if groupes else 0.0
        resume.append(dict(batiment=bat["name"], sref=round(sref, 1), bbio_pts=round(bbio, 1), cep=round(bat["cep"]["cep_annuel"], 1),
                           cef=round(bat["cep"]["cef_annuel"], 1), dh_max_groupes=round(dh, 0),
                           bbio_max=[round(z["bbio_max"]["bbio_max"], 1) for z in bat["zones"] if z.get("bbio_max")]))
    return dict(moteur="openbce", version=VERSION, batiments=resume)


class _Handler(BaseHTTPRequestHandler):
    def _repondre(self, code: int, corps: bytes, type_mime: str, entetes: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", type_mime)
        self.send_header("Content-Length", str(len(corps)))
        for k, v in (entetes or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(corps)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/version":
            self._repondre(200, json.dumps(dict(moteur="openbce", version=VERSION, corpus=CORPUS)).encode("utf-8"), "application/json; charset=utf-8")
        else:
            self._repondre(404, b"", "text/plain")

    def do_POST(self) -> None:
        url = urlparse(self.path)
        if url.path != "/calcul":
            self._repondre(404, b"", "text/plain")
            return
        taille = int(self.headers.get("Content-Length", "0"))
        corps = self.rfile.read(taille)
        try:
            ET.fromstring(corps)
        except ET.ParseError as e:
            self._repondre(400, json.dumps(dict(erreur=f"XML invalide : {e}")).encode("utf-8"), "application/json; charset=utf-8")
            return
        format_json = parse_qs(url.query).get("format", [""])[0] == "json"
        with tempfile.TemporaryDirectory(prefix="openbce_") as d:
            entree, sortie = Path(d) / "entree.xml", Path(d) / "sortie.xml"
            entree.write_bytes(corps)
            try:
                resume = calculer_rsee(entree, sortie)
            except Exception as e:                                           # erreur de calcul : rendue au client, jamais masquée
                self._repondre(422, json.dumps(dict(erreur=f"{type(e).__name__} : {e}")).encode("utf-8"), "application/json; charset=utf-8")
                return
            if format_json:
                self._repondre(200, json.dumps(resume, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            else:
                self._repondre(200, sortie.read_bytes(), "application/xml; charset=utf-8", {"X-Openbce-Resume": json.dumps(resume, ensure_ascii=True)})

    def log_message(self, fmt, *args):                                       # journal sobre, sans contenu de requête
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def servir(hote: str = "0.0.0.0", port: int = 8765) -> None:
    serveur = ThreadingHTTPServer((hote, port), _Handler)
    print(f"openbce {VERSION} : API sur http://{hote}:{port} (GET /version, POST /calcul)", flush=True)
    serveur.serve_forever()


if __name__ == "__main__":
    args = sys.argv[1:]
    hote = args[args.index("--hote") + 1] if "--hote" in args else os.environ.get("OPENBCE_HOTE", "0.0.0.0")
    port = int(args[args.index("--port") + 1] if "--port" in args else os.environ.get("OPENBCE_PORT", "8765"))
    servir(hote, port)
