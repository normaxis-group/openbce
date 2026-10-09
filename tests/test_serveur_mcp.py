# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Tests du serveur MCP : protocole, lecture d'un RSEE fabriqué, modification de champs pour les variantes."""
import io
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from openbce import serveur_mcp
from tests.test_socle import RSEE


@pytest.fixture
def serveur():
    return serveur_mcp.Serveur(sortie=io.StringIO())


@pytest.fixture
def fichier(tmp_path: Path) -> Path:
    f = tmp_path / "essai.xml"
    f.write_text(RSEE, encoding="utf-8")
    return f


def appel(serveur, methode, params=None, ident=1):
    return serveur.traiter({"jsonrpc": "2.0", "id": ident, "method": methode, "params": params or {}})


def test_initialisation(serveur):
    r = appel(serveur, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test"}})
    assert r["result"]["protocolVersion"] == "2025-06-18"
    assert "tools" in r["result"]["capabilities"]
    assert r["result"]["serverInfo"]["name"] == "openbce"
    assert "opposables" in r["result"]["instructions"]
    inconnue = appel(serveur, "initialize", {"protocolVersion": "1999-01-01"})
    assert inconnue["result"]["protocolVersion"] == serveur_mcp.VERSIONS_PROTOCOLE[0]


def test_liste_des_outils(serveur):
    outils = appel(serveur, "tools/list")["result"]["tools"]
    assert [o["name"] for o in outils] == ["version", "lire_rsee", "calculer", "comparer", "variante"]
    for o in outils:
        assert o["inputSchema"]["type"] == "object" and o["description"]


def test_erreurs_de_protocole(serveur):
    assert appel(serveur, "methode/inconnue")["error"]["code"] == -32601
    assert appel(serveur, "tools/call", {"name": "absent"})["error"]["code"] == -32602
    assert serveur.traiter({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    assert serveur.traiter({"id": 3})["error"]["code"] == -32600


def test_outil_version(serveur):
    r = appel(serveur, "tools/call", {"name": "version", "arguments": {}})["result"]
    assert r["isError"] is False
    assert r["structuredContent"]["moteur"] == "OpenBCE"
    assert json.loads(r["content"][0]["text"])["version"] == r["structuredContent"]["version"]


def test_lire_rsee(serveur, fichier):
    r = appel(serveur, "tools/call", {"name": "lire_rsee", "arguments": {"chemin": str(fichier)}})["result"]
    assert r["isError"] is False
    d = r["structuredContent"]
    assert d["version_moteur_reference"] == "2022.E3.0.0"
    zone = d["batiments"][0]["zones"][0]
    assert zone["usage"] == 1 and zone["surface"] == 80 and zone["groupes"] == 1
    assert d["batiments"][0]["composition"]["Paroi_Opaque"] == 4
    assert d["batiments"][0]["reference"]["bbio_pts"] == 70.5


def test_fichier_absent_rendu_en_erreur_d_outil(serveur, tmp_path):
    r = appel(serveur, "tools/call", {"name": "lire_rsee", "arguments": {"chemin": str(tmp_path / "absent.xml")}})["result"]
    assert r["isError"] is True and "introuvable" in r["content"][0]["text"]


def test_modifications(fichier):
    racine = ET.parse(fichier).getroot()
    bilan = serveur_mcp.appliquer_modifications(racine, [
        {"champ": "Batiment/Zone/Groupe/Paroi_Opaque[2]/Uk", "valeur": "0.3"},
        {"champ": "Batiment/Zone/Groupe/Paroi_Opaque/Beta", "valeur": "90"}])
    assert bilan[0]["occurrences"] == 1 and bilan[0]["anciennes_valeurs"] == ["0.4"]
    assert bilan[1]["occurrences"] == 4
    parois = [e for e in racine.iter() if e.tag == "Paroi_Opaque"]
    assert parois[1].find("Uk").text == "0.3" and parois[0].find("Uk").text == "0.2"
    assert all(p.find("Beta").text == "90" for p in parois)
    with pytest.raises(serveur_mcp.ErreurOutil):
        serveur_mcp.appliquer_modifications(racine, [{"champ": "Batiment/Zone/Inexistant", "valeur": "1"}])
    with pytest.raises(serveur_mcp.ErreurOutil):
        serveur_mcp.appliquer_modifications(racine, [{"champ": "Batiment/Zone/Groupe", "valeur": "1"}])


def test_echange_complet_sur_stdio():
    sortie = io.StringIO()
    entree = io.StringIO("\n".join(json.dumps(m) for m in [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]) + "\npas du json\n")
    serveur_mcp.Serveur(sortie=sortie).servir(entree)
    reponses = [json.loads(l) for l in sortie.getvalue().splitlines()]
    assert [r.get("id") for r in reponses] == [1, 2, None]
    assert reponses[0]["result"]["protocolVersion"] == "2025-03-26"
    assert reponses[2]["error"]["code"] == -32700
