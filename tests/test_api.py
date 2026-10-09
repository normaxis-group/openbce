# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from openbce import api


def test_version_et_xml_invalide():
    serveur = ThreadingHTTPServer(("127.0.0.1", 0), api._Handler)
    port = serveur.server_address[1]
    t = threading.Thread(target=serveur.serve_forever, daemon=True)
    t.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/version") as r:
            assert json.loads(r.read())["moteur"] == "openbce"
        req = urllib.request.Request(f"http://127.0.0.1:{port}/calcul", data=b"<pas du xml", method="POST")
        try:
            urllib.request.urlopen(req)
            assert False, "un XML invalide doit être refusé"
        except urllib.error.HTTPError as e:
            assert e.code == 400
    finally:
        serveur.shutdown()
