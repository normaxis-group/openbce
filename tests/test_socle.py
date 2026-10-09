# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 ARKEMEP
"""Tests du socle : lecteur de RSEE et indicateurs d'enveloppe, sur un RSEE fabriqué (aucune donnée de client)."""
from pathlib import Path

import pytest

from openbce import enveloppe, rsee

RSEE = """<?xml version="1.0" encoding="utf-8"?>
<projet version="2022.D1.0.0">
 <Datas_Comp version="2022.D1.0.0"><donnees_generales><operation>essai</operation></donnees_generales></Datas_Comp>
 <RSET>
  <Entree_Projet><Version>2022.E3.0.0</Version>
   <Batiment_Collection><Batiment><Index>1</Index>
    <Espace_Tampon_Collection><Espace_Tampon_Non_Solarise><Index>7</Index><b_et_ns>0.5</b_et_ns></Espace_Tampon_Non_Solarise></Espace_Tampon_Collection>
    <Zone_Collection><Zone><Index>1</Index><Usage>1</Usage>
     <Groupe_Collection><Groupe><Index>1</Index><SHAB>80</SHAB>
      <Paroi_opaque_Collection>
       <Paroi_Opaque><Ak>50</Ak><Uk>0.2</Uk><Beta>90</Beta><Id_Et>0</Id_Et></Paroi_Opaque>
       <Paroi_Opaque><Ak>10</Ak><Uk>0.4</Uk><Beta>90</Beta><Id_Et>7</Id_Et></Paroi_Opaque>
       <Paroi_Opaque><Ak>80</Ak><Uk>0.1</Uk><Beta>0</Beta><Id_Et>0</Id_Et></Paroi_Opaque>
       <Paroi_Opaque><Ak>80</Ak><Uk>0.25</Uk><Beta>180</Beta><Id_Et>0</Id_Et></Paroi_Opaque>
      </Paroi_opaque_Collection>
      <Baie_Collection><Baie><Ab>12</Ab></Baie></Baie_Collection>
      <Lineaire_Collection><Lineaire><Ll>30</Ll><Psil>0.1</Psil></Lineaire></Lineaire_Collection>
     </Groupe></Groupe_Collection>
    </Zone></Zone_Collection>
   </Batiment></Batiment_Collection>
  </Entree_Projet>
  <Sortie_Projet><Sortie_Batiment_B_Collection><Sortie_Batiment_B><Index>1</Index><O_Bbio_pts_annuel>70.5</O_Bbio_pts_annuel>
   <O_B_Ch_mois><Sortie_Mensuelle><Mois>2</Mois><Valeur>5</Valeur></Sortie_Mensuelle><Sortie_Mensuelle><Mois>1</Mois><Valeur>6.8</Valeur></Sortie_Mensuelle></O_B_Ch_mois>
  </Sortie_Batiment_B></Sortie_Batiment_B_Collection></Sortie_Projet>
 </RSET>
</projet>"""


@pytest.fixture
def projet(tmp_path: Path):
    f = tmp_path / "essai.xml"
    f.write_text(RSEE, encoding="utf-8")
    return rsee.lire(f)


def test_lecture(projet):
    assert projet.version_rsee == "2022.D1.0.0"
    assert projet.version_moteur == "2022.E3.0.0"
    assert len(projet.entree.tous("Paroi_Opaque")) == 4
    sortie = projet.sortie.un("Sortie_Batiment_B")
    assert sortie.nombre("O_Bbio_pts_annuel") == 70.5
    assert sortie.mensuel("O_B_Ch_mois") == [6.8, 5.0]


def test_enveloppe(projet):
    batiment = projet.entree.directs("Batiment")[0]
    e = enveloppe.de_zone(batiment.directs("Zone")[0], enveloppe.coefficients_b(batiment))
    assert (e.a_opv, e.a_ophh, e.a_ophb, e.a_baies, e.a_t) == (60, 80, 80, 12, 232)
    assert e.h_opv == pytest.approx(50 * 0.2 + 10 * 0.4 * 0.5)
    assert e.h_ophh == pytest.approx(8) and e.h_ophb == pytest.approx(20)
    assert e.h_pt == pytest.approx(3) and e.l_pt == 30


def test_bloc_manquant(tmp_path: Path):
    f = tmp_path / "vide.xml"
    f.write_text("<projet><Datas_Comp/></projet>", encoding="utf-8")
    with pytest.raises(ValueError):
        rsee.lire(f)
