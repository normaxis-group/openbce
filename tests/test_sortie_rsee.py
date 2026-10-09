# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
import xml.etree.ElementTree as ET

import pytest

from openbce import rsee, sortie_rsee


def _calcul():
    g1 = dict(index=1, name="G1", sref=100.0, shab=100.0, su=0.0, climatise=False,
              b_ch_mois=[1.0] * 12, b_fr_mois=[0.5] * 12, b_ecl_mois=[0.1] * 12,
              c_b_ch_mois=[1.2] * 12, c_b_fr_mois=[0.0] * 12, c_b_ecs=20.0,
              cef=dict(ch=5.0, fr=0.0, ecs=10.0, ecl=1.5, aux_vent=0.8, aux_dist=0.2),
              cef_energie={("ch", "elec"): 5.0, ("ecs", "elec"): 10.0}, dh=300.0, nb_h_inconf=(10, 5, 2), dh_max=1250.0)
    g2 = dict(g1, index=2, name="G2", sref=300.0, shab=300.0, b_ch_mois=[2.0] * 12, cef=dict(g1["cef"], ch=7.0))
    return dict(name="essai", batiments=[dict(index=1, name="B1", zones=[dict(index=1, name="Z1", usage=2, nb_logements=4, bbio_max=dict(bbio_max=80.0, mbgeo=0.1),
                                                                               groupes=[g1, g2])],
                                              cep=dict(cef_annuel=17.5, cep_annuel=40.0, cep_nr_annuel=38.0, imp=dict(ch=6.5, ecs=10.0), par_energie=dict(elec=17.5)))])


def test_construction_et_relecture(tmp_path):
    el = sortie_rsee.construire(_calcul(), version="essai", departement="13", altitude=10.0)
    racine = ET.Element("projet")
    rset = ET.SubElement(racine, "RSET")
    ET.SubElement(rset, "Entree_Projet")
    rset.append(el)
    chemin = tmp_path / "x.xml"
    ET.ElementTree(racine).write(chemin, encoding="utf-8", xml_declaration=True)
    p = rsee.lire(chemin)
    b = p.sortie.un("Sortie_Batiment_B")
    assert b.nombre("O_B_Ch_annuel") == pytest.approx(0.25 * 12 + 0.75 * 24, abs=0.05)     # moyenne pondérée 100 / 300 m²
    assert b.nombre("O_Bbio_pts_annuel") == pytest.approx(2 * 21 + 2 * 6 + 5 * 1.2, abs=0.2)
    z = p.sortie.un("Sortie_Zone_B")
    assert z.nombre("O_Bbio_Max") == 80.0 and z.entier("Usage") == 2 and len(z.mensuel("O_B_Ch_mois")) == 12
    c = p.sortie.un("Sortie_Batiment_C")
    assert c.nombre("O_Cep_annuel") == 40.0 and c.nombre("O_Cef_imp_ecs_annuel") == 10.0
    gc = [g for g in p.sortie.tous("Sortie_Groupe_C") if g.entier("Index") == 2][0]
    assert gc.nombre("O_Cef_ch_annuel") == 7.0 and gc.nombre("O_Cef_ch_elec_annuel") == 5.0 and gc.nombre("O_B_Ch_annuel") == pytest.approx(14.4)
    d = p.sortie.un("Sortie_Groupe_D")
    assert d.nombre("O_NbDegresHeures") == 300.0 and d.entier("O_Nb_h_inconf_1") == 5


def test_ecriture_remplace_le_bloc_sortie(tmp_path):
    entree = tmp_path / "e.xml"
    entree.write_text('<?xml version="1.0" encoding="UTF-8"?><projet><Datas_Comp version="1"/><RSET><Entree_Projet><Version>v</Version></Entree_Projet>'
                      '<Sortie_Projet HashKey="x"><Index>1</Index></Sortie_Projet></RSET></projet>', encoding="utf-8")
    el = sortie_rsee.construire(_calcul())
    s = sortie_rsee.ecrire(entree, el, tmp_path / "s.xml")
    p = rsee.lire(s)
    assert p.entree.texte("Version") == "v" and p.sortie.tous("Sortie_Batiment_B")
