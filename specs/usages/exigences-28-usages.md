# Spécification : exigences de résultat des 28 usages (annexe de l'article R. 172-4, chapitres I à III)

Date : 09/10/2026, corrections de la contre-lecture du 09/10/2026 appliquées (§ 1, 2, 4.2, 5.2, 6.1, 8, 10, 11). Décision de Cédric PLANTAZ (ARKEMEP) du 09/10/2026 : « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Les valeurs ci-dessous sont recopiées du texte ; seuls les usages 1, 2 et 3 ont été confrontés à des RSEE (banc/exigences.py). Rien n'est demandé au CSTB.

## Sources lues

- Annexe à l'article R. 172-4 du CCH, chapitres I à III, version consolidée après les décrets n° 2022-305 du 1er mars 2022, n° 2024-1258 du 30 décembre 2024 et n° 2026-16 du 15 janvier 2026 (`corpus/site_2026-10-09/chapitre1a3_annexe_r172-4_post-gtm2.txt`, 93 pages) : définitions p. 1-2, formules p. 2-5, Bbio_max p. 6-28, Cep,nr_max / Cep_max / Icénergie_max p. 28-56, Icconstruction_max p. 56-87, DH_max p. 87-93. Les chapitres IV (zones climatiques) et V (catégories de contraintes extérieures, zones de bruit) ne sont pas dans ce fichier.
- Arrêté du 4 août 2021 consolidé (`corpus/textes/arrete-040821-...txt`) : articles 1, 2, 3, 4, 5, 8, 9, 17, 19, 45, 50-1 à 50-4, 51.
- Arrêté du 22 décembre 2022 (constructions temporaires, petites surfaces : articles 50-1 à 50-4), arrêté du 14 août 2024 (HLL, « surface de référence »), arrêté du 18 mars 2026 (surélévations, en vigueur le 1er juillet 2026), arrêté du 19 mars 2026 (usages 6 à 28, en vigueur le 1er mai 2026 : articles 1 à 3, 5 II tableau 4, 5 VI A tableau 278, 8, 9).
- Annexe II de l'arrêté (`corpus/site_2026-10-09/annexeii_arrete_4_aout_2021.txt`) : 2.3.3 La surface de référence, p. 32.
- Annexe III (`corpus/texte_annexe3_2026-07/annexe3.txt`) : fiche 5.11 classement au bruit d'une baie p. 245-247 ; nomenclature Categorie_CE1_CE2 et Isclimatise du groupe p. 990 et p. 1356 ; fiche 13.1 sommation des Bbio par zone et bâtiment, équations 2386 et 2387, p. 1360.
- Fiches d'application FA05 v2 du 01/10/2026 (identification de l'usage, p. 2-12) et FA09 v1 du 01/10/2026 (exclusions process, p. 2-8).
- Tableur des scénarios officiels du 29/04/2026 (`openbce/tables/scenarios_officiels.json`) : seulement pour la numérotation 1 à 28 des usages.

Convention de ce document : un coefficient « par zone climatique » est un tuple de huit valeurs dans l'ordre H1a, H1b, H1c, H2a, H2b, H2c, H2d, H3 (ordre de `exigences.ZONES`). Les tableaux à trois lignes d'altitude sont dans l'ordre < 400 m, 400 à 800 m, > 800 m (le texte écrit « 400m-800m », le moteur prend 400 ≤ alt ≤ 800 dans la ligne du milieu, convention conservée). Les formules par morceaux sont écrites comme des segments `(borne_sup, a, b)` : la valeur vaut `(a + b * S) / ref` tant que `S <= borne_sup` ; `None` en borne signifie « au-delà ».

## 1. Dates d'application et usages sans exigence

- Usages 1 et 2 (habitation) : permis ou déclaration préalable déposés à compter du 1er janvier 2022 (R. 172-1 I, cité FA05 p. 2). Résidences de tourisme avec local de sommeil, cuisine et sanitaires : règles de l'habitation (R. 172-1 I, FA05 p. 2).
- Usages 3, 4, 5 (bureaux, enseignement primaire et secondaire) : à compter du 1er juillet 2022 (R. 172-1 I, décret n° 2022-305, FA05 p. 2).
- Constructions temporaires et HLL des usages 1 à 5 : deux dates dans les sources. R. 172-1 II (cité FA05 p. 2) dit « à compter du 1er juillet 2023 » ; l'art. 3 I de l'arrêté du 4 août 2021 consolidé dit « à compter du 1er janvier 2023 » pour les habitations légères de loisir (R.* 421-2 b) et les constructions provisoires (R.* 421-5), et l'art. 51 (III et IV, rédaction de l'arrêté du 22 décembre 2022 art. 5) fait entrer les art. 50-2 à 50-4 au 1er janvier 2023 et le seul art. 50-1 au 1er juillet 2023. Écart entre le décret et l'arrêté, sans effet sur le moteur.
- Usages 6 à 28 (tertiaires spécifiques, industriel et artisanal) : permis ou déclaration préalable déposés à compter du 1er mai 2026 (R. 172-1 III, décret n° 2026-16 du 15 janvier 2026, FA05 p. 2-3 ; arrêté du 19 mars 2026 art. 9 : entrée en vigueur le 1er mai 2026). Avant cette date, ces usages n'avaient aucune exigence RE2020. Qu'ils aient relevé de la RT2012 n'est écrit dans aucun passage lu (l'art. 2 de l'arrêté du 4 août 2021 cite les arrêtés du 26 octobre 2010 et du 28 décembre 2012 ; FA05 p. 5 ne maintient en RT2012 que les tribunaux et palais de justice) : non démontré, hors moteur.
- Pour les usages 6 à 28, R. 172-1 III exclut (FA05 p. 3, FA09 p. 2 et 8) : les locaux à conditions particulières de température, d'hygrométrie ou de qualité d'air (process), les constructions temporaires (R.* 421-5 ou durée ≤ 2 ans), les constructions ou extensions de surface < 50 m², les extensions cumulativement < 150 m² et < 30 % de la surface des locaux existants. Un local à usage de process est exclu du Bbio, du Cep, du Cep,nr et du DH et ne compte pas dans la Sref (FA09 p. 5).
- Dans la liste des 28 usages du texte en vigueur, **aucun usage n'est sans exigence** : les 28 ont Bbio_maxmoyen (p. 6), Cep,nr_maxmoyen et Cep_maxmoyen (p. 28-29), Icénergie_maxmoyen (p. 29-32), Icconstruction_maxmoyen (p. 56-57) et DH_maxcat (p. 87-93). Les colonnes « 2022 à 2024 » des usages 6 à 28 ne portent aucune valeur pour Icénergie « autres cas » ni pour Icconstruction : un tiret « - » pour Icénergie « autres cas » des usages 6 à 16 et 18 à 28 (p. 30-32) et pour Icconstruction des usages 6 à 17 (p. 56-57) ; cellule simplement absente, sans tiret, pour Icénergie « autres cas » de l'usage 17 (p. 31) et pour Icconstruction des usages 18 à 28 (p. 57). Le texte ne motive pas ces cellules vides. La colonne « 2022 à 2024, raccordés » de ces usages est, elle, renseignée ; la règle des réseaux classés qui y renvoie est au § 5.2.
- Hors champ de la méthode (aucun des 28 usages, FA05 p. 5) : lieux de culte, salles de spectacle, musées et salles d'exposition, piscines municipales, saunas, hammams, patinoires, établissements pénitentiaires, salles polyvalentes et salles des fêtes, datacenters ; les tribunaux et palais de justice restent en RT2012 (FA05 p. 5).
- Exigences alternatives (hors moteur) : constructions temporaires art. 50-1 (arrêté du 22 décembre 2022 art. 3) ; petites surfaces et extensions art. 50-2 et 50-3 (art. 4), modifiés par l'arrêté du 18 mars 2026 (surélévations, en vigueur le 1er juillet 2026) : les surélévations de maison individuelle climatisées en H2d ou H3 gardent les 1°, 4° et 5° de R. 172-4 avec DH_maxcat porté à 1 400 DH (art. 50-3 II 1, rédaction du 18 mars 2026) ; HLL < 50 m² art. 50-4 (arrêté du 14 août 2024). Bâtiment livré sans chauffage et sans système par défaut : seules les exigences 1°, 4° et 5° (Bbio, Icconstruction, DH) s'appliquent (art. 45).

## 2. Surface de référence par usage

- Chapitre I, X (p. 2) : Sref = surface habitable (SHAB) pour un bâtiment ou une partie de bâtiment à usage d'habitation, surface utile (SU) dans les autres cas. Smoylgt = Sref / NL (chapitre I, XI, p. 2).
- Arrêté du 4 août 2021 art. 2 : la Sref du chapitre I est la surface utilisée dans tout l'arrêté sauf mention contraire ; l'arrêté du 14 août 2024 (art. 2) a remplacé « surface utile » par « surface de référence » aux articles 50-1 à 50-4.
- Arrêté du 19 mars 2026 art. 5 VI A, tableau 278 : l'unité des besoins d'ECS est « m² de surface utile » pour chacun des usages 3 à 28, hôtels (8 à 11) et établissements sanitaires avec hébergement (19) compris. Aucun texte lu ne qualifie l'usage des hôtels (8 à 11) au regard du X du chapitre I : les ranger dans « les autres cas » (SU) est une déduction de l'unité du tableau 278, cohérente avec FA05 p. 9 (résidences étudiantes sans cuisine rangées en usage 8, avec cuisine en usage 2) mais non écrite (point ouvert 13). Seules les résidences de tourisme équipées (R. 172-1 I) et les résidences étudiantes avec cuisine (FA05 p. 9, usage 2) sont explicitement en habitation, donc en SHAB.
- Annexe II 2.3.3 (p. 32) : la Sref ne se confond pas avec les surfaces de parois ou de baies des algorithmes.

```python
SURFACE_REFERENCE = {u: ("SHAB" if u in (1, 2) else "SU") for u in range(1, 29)}   # chapitre I, X, p. 2 ; SU des hôtels 8 à 11 déduite du tableau 278, non écrite (point ouvert 13)
```

Dans le RSEE, le banc lit `Groupe/SHAB` pour les usages 1 et 2 et `Groupe/SU` sinon (banc/exigences.py L43, banc/sortie_rsee.py L54) : règle inchangée, étendue telle quelle aux usages 4 à 28.

## 3. Formules (chapitre II, p. 2-5)

- Bbio_max = Bbio_maxmoyen × (1 + Mbgéo + Mbcombles + Mbsurf_moy + Mbsurf_tot + Mbbruit) (chapitre II, I, p. 3). Mbsurf_tot est déterminé, pour chaque usage, sur la somme des surfaces des parties de bâtiment de l'usage considéré (p. 3).
- Cep,nr_max = Cep,nr_maxmoyen × (1 + Mcgéo + Mccombles + Mcsurf_moy + Mcsurf_tot + Mccat) ; Cep_max = Cep_maxmoyen × (même parenthèse) ; Icénergie_max = Icénergie_maxmoyen × (même parenthèse) (chapitre II, II, p. 3-4). Mcsurf_tot est pris sur la somme des surfaces des parties de même usage (p. 4). Les formules de Mcsurf_moy et Mcsurf_tot divisent toujours par Cep,nr_maxmoyen, y compris quand la modulation s'applique à Cep_max ou Icénergie_max (p. 33, 34, 35, 36, 39, 46, 50, 51, 52).
- Icconstruction_max = Icconstruction_maxmoyen × (1 + Micombles + Misurf_moy + Misurf_tot) + Migéo + Miinfra + Mivrd + Mipv + Mided (chapitre II, III, p. 4) : Migéo, Miinfra, Mivrd, Mipv et Mided sont additifs, en kg éq. CO2/m².
- DH_max = DH_maxcat, par partie de bâtiment thermiquement homogène (chapitre II, IV, p. 4-5) : au groupe dans le RSEE.
- Bâtiments à plusieurs zones : § 9.

## 4. Bbio_max (chapitre III, I, p. 6-28)

### 4.1 Bbio_maxmoyen (p. 6)

```python
BBIO_MAX_MOYEN = {   # points, annexe R. 172-4 chapitre III, I, p. 6
    1: 63.0, 2: 65.0, 3: 95.0, 4: 68.0, 5: 68.0, 6: 117.0, 7: 122.0, 8: 76.0, 9: 76.0, 10: 134.0, 11: 163.0, 12: 139.0,
    13: 245.0, 14: 100.0, 15: 206.0, 16: 177.0, 17: 170.0, 18: 225.0, 19: 174.0, 20: 164.0, 21: 133.0, 22: 248.0,
    23: 257.0, 24: 69.0, 25: 94.0, 26: 76.0, 27: 116.0, 28: 94.0,
}
```

### 4.2 Mbgéo (trois lignes d'altitude, huit zones)

```python
MBGEO = {
    1: ((0.15, 0.2, 0.2, -0.05, 0.0, -0.1, 0.05, -0.1), (0.4, 0.5, 0.45, 0.15, 0.3, 0.05, 0.1, -0.05), (0.75, 0.85, 0.75, 0.55, 0.65, 0.35, 0.25, 0.1)),        # p. 7
    2: ((0.1, 0.2, 0.15, -0.1, 0.0, -0.1, 0.0, -0.1), (0.4, 0.5, 0.45, 0.2, 0.3, 0.1, 0.2, -0.05), (0.8, 0.85, 0.75, 0.6, 0.65, 0.4, 0.4, 0.15)),              # p. 8
    3: ((0.05, 0.10, 0.20, -0.05, 0.0, 0.10, 0.30, 0.25), (0.25, 0.25, 0.20, 0.20, 0.20, 0.10, 0.10, -0.05), (0.45, 0.45, 0.40, 0.40, 0.35, 0.25, 0.30, 0.10)),  # p. 9
    4: ((0.10, 0.20, 0.25, -0.10, 0.0, 0.05, 0.50, 0.50), (0.25, 0.30, 0.25, 0.05, 0.10, 0.0, 0.35, 0.25), (0.45, 0.45, 0.40, 0.30, 0.35, 0.20, 0.30, 0.20)),   # p. 10, primaire et secondaire
    6: ((0.05, 0.2, 0.25, -0.1, 0.0, 0.0, 0.3, 0.2), (0.2, 0.3, 0.3, 0.0, 0.1, 0.0, 0.25, 0.15), (0.4, 0.5, 0.40, 0.15, 0.3, 0.1, 0.25, 0.15)),                  # p. 11
    7: ((0.1, 0.2, 0.2, -0.05, 0.0, 0.0, 0.2, 0.2), (0.3, 0.35, 0.35, 0.1, 0.2, 0.05, 0.25, 0.15), (0.5, 0.6, 0.5, 0.3, 0.4, 0.2, 0.25, 0.15)),                  # p. 11
    8: ((0.15, 0.2, 0.2, 0.0, 0.0, -0.1, 0.0, -0.15), (0.45, 0.45, 0.4, 0.25, 0.3, 0.15, 0.15, -0.05), (0.75, 0.8, 0.7, 0.6, 0.6, 0.4, 0.4, 0.15)),              # p. 12
    9: ((0.15, 0.2, 0.2, 0.0, 0.0, -0.1, 0.0, -0.15), (0.45, 0.45, 0.4, 0.25, 0.3, 0.15, 0.15, -0.05), (0.75, 0.75, 0.65, 0.6, 0.6, 0.4, 0.4, 0.15)),            # p. 13
    10: ((0.1, 0.15, 0.25, -0.1, 0.0, 0.0, 0.35, 0.25), (0.25, 0.3, 0.35, 0.05, 0.15, 0.05, 0.3, 0.15), (0.45, 0.55, 0.5, 0.3, 0.35, 0.2, 0.35, 0.15)),          # p. 14
    11: ((0.05, 0.15, 0.2, -0.1, 0.0, -0.05, 0.25, 0.1), (0.25, 0.3, 0.3, 0.1, 0.15, 0.05, 0.25, 0.1), (0.45, 0.5, 0.45, 0.3, 0.35, 0.20, 0.3, 0.15)),           # p. 15
    12: ((0.1, 0.15, 0.1, 0.0, 0.0, -0.1, 0.1, 0.0), (0.25, 0.3, 0.25, 0.15, 0.2, 0.05, 0.1, 0.05), (0.45, 0.5, 0.4, 0.4, 0.4, 0.25, 0.25, 0.15)),               # p. 16
    13: ((0.05, 0.1, 0.2, -0.05, 0.0, 0.05, 0.25, 0.15), (0.15, 0.2, 0.25, 0.05, 0.1, 0.05, 0.25, 0.15), (0.3, 0.35, 0.35, 0.2, 0.25, 0.15, 0.30, 0.15)),        # p. 16
    14: ((0.1, 0.15, 0.2, 0.0, 0.0, -0.05, 0.2, 0.1), (0.3, 0.35, 0.3, 0.2, 0.2, 0.05, 0.2, 0.15), (0.55, 0.55, 0.5, 0.45, 0.45, 0.25, 0.3, 0.2)),               # p. 17
    15: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.0, 0.15, 0.1), (0.20, 0.25, 0.25, 0.1, 0.15, 0.05, 0.2, 0.1), (0.35, 0.4, 0.35, 0.25, 0.3, 0.15, 0.25, 0.15)),          # p. 18
    16: ((0.05, 0.15, 0.15, -0.05, 0.0, 0.0, 0.2, 0.1), (0.2, 0.25, 0.25, 0.05, 0.15, 0.05, 0.2, 0.15), (0.35, 0.4, 0.35, 0.25, 0.3, 0.15, 0.3, 0.2)),           # p. 19
    17: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.05, 0.3, 0.25), (0.1, 0.2, 0.2, 0.0, 0.1, 0.0, 0.25, 0.2), (0.2, 0.3, 0.25, 0.15, 0.2, 0.1, 0.25, 0.2)),                # p. 19-20
    18: ((0.05, 0.1, 0.1, -0.05, 0.0, -0.1, 0.0, -0.1), (0.3, 0.3, 0.25, 0.2, 0.25, 0.05, 0.1, 0.0), (0.55, 0.55, 0.5, 0.45, 0.5, 0.3, 0.25, 0.15)),             # p. 20
    19: ((0.1, 0.15, 0.15, -0.05, 0.0, -0.05, 0.05, -0.05), (0.25, 0.3, 0.25, 0.15, 0.15, 0.1, 0.1, -0.05), (0.45, 0.5, 0.45, 0.3, 0.35, 0.25, 0.2, 0.05)),      # p. 21
    20: ((0.05, 0.15, 0.2, -0.05, 0.0, 0.0, 0.2, 0.1), (0.25, 0.3, 0.3, 0.15, 0.2, 0.1, 0.25, 0.1), (0.45, 0.5, 0.45, 0.35, 0.4, 0.25, 0.35, 0.2)),              # p. 22
    21: ((0.05, 0.15, 0.2, -0.05, 0.0, 0.0, 0.25, 0.2), (0.15, 0.2, 0.2, 0.05, 0.05, 0.0, 0.2, 0.1), (0.25, 0.3, 0.25, 0.15, 0.2, 0.1, 0.15, 0.1)),              # p. 23
    22: ((0.05, 0.1, 0.15, -0.05, 0.0, 0.05, 0.2, 0.2), (0.1, 0.15, 0.2, 0.0, 0.1, 0.05, 0.2, 0.15), (0.05, 0.15, -0.05, 0.0, 0.1, 0.25, 0.25, 0.05)),           # p. 23 (ligne > 800 m telle quelle)
    23: ((0.05, 0.05, 0.1, -0.05, 0.0, 0.05, 0.25, 0.25), (0.05, 0.1, 0.1, 0.0, 0.05, 0.05, 0.2, 0.15), (0.1, 0.15, 0.15, 0.05, 0.1, 0.05, 0.2, 0.1)),           # p. 24
    24: ((0.1, 0.15, 0.25, -0.05, 0.0, 0.05, 0.4, 0.35), (0.2, 0.25, 0.3, 0.05, 0.1, 0.05, 0.4, 0.3), (0.35, 0.4, 0.45, 0.2, 0.25, 0.15, 0.35, 0.25)),           # p. 25
    25: ((0.0, 0.1, 0.25, -0.15, 0.0, 0.1, 0.55, 0.55), (0.0, 0.05, 0.15, -0.15, -0.05, -0.05, 0.4, 0.3), (0.05, 0.1, 0.15, -0.05, 0.0, -0.05, 0.25, 0.15)),      # p. 26, municipaux et privés
    26: ((0.15, 0.2, 0.15, -0.05, 0.0, -0.05, 0.1, 0.1), (0.35, 0.4, 0.35, 0.2, 0.25, 0.1, 0.2, 0.1), (0.65, 0.65, 0.6, 0.5, 0.55, 0.35, 0.35, 0.25)),           # p. 27
    27: ((0.1, 0.15, 0.15, -0.05, 0.0, -0.05, 0.1, 0.1), (0.3, 0.35, 0.3, 0.15, 0.2, 0.1, 0.2, 0.1), (0.55, 0.55, 0.5, 0.45, 0.45, 0.3, 0.35, 0.2)),             # p. 27
}
MBGEO[5] = MBGEO[4]      # « enseignement primaire ou secondaire », p. 10
MBGEO[28] = MBGEO[25]    # « 25. et 28. », p. 26
```

### 4.3 Mbcombles et Mbsurf_moy

- Mbcombles = 0,4 × Scombles / Sref pour l'usage 1 seul (p. 7 ; Scombles = plancher des combles aménagés de hauteur sous plafond < 1,8 m) ; 0 pour les usages 2 à 28 (p. 8 à 28). Fonction `mbcombles` inchangée.
- Mbsurf_moy : usage 1 (p. 7) et usage 2 (p. 8) selon les formules déjà codées (`mbsurf_moy` L40-50) ; 0 pour les usages 3 à 28 (p. 9 à 28). Fonction inchangée.

### 4.4 Mbsurf_tot

Segments `(borne_sup, a, b)` : Mbsurf_tot = (a + b × S) / Bbio_maxmoyen pour S ≤ borne_sup, S = somme des Sref des parties de même usage (chapitre II, I, p. 3). Pour les bureaux, la formule dépend de l'année de dépôt du permis (p. 9), déjà codée (`mbsurf_tot` L60-68) ; elle est rappelée en clair.

```python
MBSURF_TOT = {   # (borne_sup, a, b) : (a + b*S)/Bbio_maxmoyen ; None : 0 partout
    1: None,                                                          # p. 7
    2: ((1300, 19.5, -0.015), (None, 0.0, 0.0)),                      # p. 8
    3: "selon l'année du permis, voir ci-dessous",                     # p. 9
    4: ((500, 35.0, -0.05), (1000, 20.0, -0.02), (None, 0.0, 0.0)),   # p. 10, primaire
    5: ((1000, 45.0, -0.045), (None, 0.0, 0.0)),                      # p. 10, secondaire
    6: None, 7: None, 8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None,   # p. 11 à 19
    17: ((500, 47.5, -0.095), (None, 0.0, 0.0)),                      # p. 20, commerces
    18: None, 19: None, 20: None,                                     # p. 21, 21, 22
    21: ((2000, 22.0, -0.008), (None, 0.0, 0.0)),                     # p. 23, santé partie jour
    22: None,                                                         # p. 24
    23: ((5000, 50.0, -0.01), (None, 0.0, 0.0)),                      # p. 25, industrie 3x8
    24: ((5000, 65.0, -0.013), (None, 0.0, 0.0)),                     # p. 25, industrie 8h à 18h
    25: None, 26: None, 27: None, 28: None,                           # p. 26, 27, 28, 26
}
# Bureaux (p. 9), années 2022-2024 / 2025-2027 / à partir de 2028 :
#   S <= 500 : (24 - 0,06 S) dans les trois cas
#   500 < S <= 4000 : (-5,55 - 0,0009 S) / (-4,9 - 0,0022 S) / (-3,8 - 0,0044 S)
#   4000 < S <= 10000 : (-5,55 - 0,0009 S) / (-9,7 - 0,001 S) / -21,4
#   S > 10000 : -14,55 / -19,7 / -21,4          (le tout divisé par Bbio_maxmoyen = 95)
```

### 4.5 Mbbruit

Trois formes dans le texte : par zone climatique et classe BR (usages 1 et 2), par zone climatique en catégorie 3 avec 0 en BR1/BR2/BR3 (usages 6, 7, 12), scalaire en catégorie 3 avec 0 en BR1/BR2/BR3 (usages 3, 8, 9, 10, 11, 17), nul partout (4, 5, 13 à 16, 18 à 28).

```python
MBBRUIT_BR23 = {1: (0, 0, 0, 0, 0, 0, 0.1, 0.1),            # p. 7, BR2 et BR3 (BR1 : 0)
                2: (0, 0, 0.1, 0, 0, 0.1, 0.2, 0.2)}        # p. 8
MBBRUIT_CAT3 = {                                            # 0 en BR1, BR2 et BR3 ; valeur en catégorie 3
    3: 0.4,                                                 # p. 9
    6: (0.15, 0.1, 0.1, 0.15, 0.15, 0.2, 0.1, 0.15),        # p. 11
    7: (0.1, 0.05, 0.1, 0.1, 0.15, 0.2, 0.1, 0.15),         # p. 12
    8: 0.05, 9: 0.05,                                       # p. 13, 14
    10: 0.3, 11: 0.3,                                       # p. 14, 15
    12: (0.05, 0.1, 0.15, 0.1, 0.15, 0.2, 0.25, 0.3),       # p. 16
    17: 0.2,                                                # p. 20
}
# Mbbruit = 0 pour 4 et 5 (p. 10), 13 (p. 17), 14 et 15 (p. 18), 16 (p. 19), 18 (p. 21), 19 (p. 22), 20 (p. 22),
# 21 (p. 23), 22 (p. 24), 23 (p. 25), 24 (p. 26), 25 et 28 (p. 26), 26 (p. 27), 27 (p. 28).
```

## 5. Cep,nr_max, Cep_max et Icénergie_max (chapitre III, II, p. 28-56)

### 5.1 Cep,nr_maxmoyen et Cep_maxmoyen (p. 28-29), kWhep/(m².an)

```python
CEP_NR_MAX_MOYEN = {1: 55.0, 2: 70.0, 3: 75.0, 4: 65.0, 5: 63.0, 6: 93.0, 7: 102.0, 8: 121.0, 9: 118.0, 10: 235.0, 11: 234.0,
                    12: 150.0, 13: 282.0, 14: 132.0, 15: 219.0, 16: 214.0, 17: 163.0, 18: 242.0, 19: 190.0, 20: 274.0, 21: 165.0,
                    22: 191.0, 23: 290.0, 24: 94.0, 25: 94.0, 26: 119.0, 27: 153.0, 28: 112.0}
CEP_MAX_MOYEN = {1: 75.0, 2: 85.0, 3: 85.0, 4: 72.0, 5: 72.0, 6: 105.0, 7: 112.0, 8: 144.0, 9: 138.0, 10: 252.0, 11: 281.0,
                 12: 182.0, 13: 578.0, 14: 275.0, 15: 446.0, 16: 412.0, 17: 182.0, 18: 306.0, 19: 252.0, 20: 302.0, 21: 180.0,
                 22: 253.0, 23: 365.0, 24: 116.0, 25: 116.0, 26: 251.0, 27: 329.0, 28: 148.0}
```

### 5.2 Icénergie_maxmoyen (p. 29-32), kg éq. CO2/m², par usage, raccordement à un réseau de chaleur urbain, et année de dépôt du permis (2022 à 2024, 2025 à 2027, à partir de 2028)

```python
IC_ENERGIE_MAX_MOYEN = {   # usage: {"rcu": (2022-2024, 2025-2027, 2028+), "autres": (...)} ; None = « - » dans le texte ; "non spécifié" = cellule sans valeur ni tiret
    1: {"rcu": (200, 200, 160), "autres": (160, 160, 160)},      # p. 29-30
    2: {"rcu": (560, 320, 260), "autres": (560, 260, 260)},
    3: {"rcu": (280, 200, 200), "autres": (200, 200, 200)},
    4: {"rcu": (240, 200, 140), "autres": (240, 140, 140)}, 5: {"rcu": (240, 200, 140), "autres": (240, 140, 140)},
    6: {"rcu": (360, 285, 285), "autres": (None, 285, 285)},     # p. 30
    7: {"rcu": (225, 190, 190), "autres": (None, 190, 190)},
    8: {"rcu": (490, 390, 390), "autres": (None, 390, 390)},
    9: {"rcu": (485, 350, 350), "autres": (None, 350, 350)},
    10: {"rcu": (595, 495, 495), "autres": (None, 495, 495)},
    11: {"rcu": (630, 520, 520), "autres": (None, 520, 520)},
    12: {"rcu": (895, 680, 680), "autres": (None, 680, 680)},    # p. 31
    13: {"rcu": (670, 570, 570), "autres": (None, 570, 570)},
    14: {"rcu": (605, 470, 470), "autres": (None, 470, 470)},
    15: {"rcu": (705, 570, 570), "autres": (None, 570, 570)},
    16: {"rcu": (675, 545, 545), "autres": (None, 545, 545)},
    17: {"rcu": (315, 315, 315), "autres": ("non spécifié", 315, 315)},   # p. 31 : la ligne « autres cas » ne porte que deux cellules « 315 », sans tiret ; la colonne vide n'est pas identifiable dans l'extraction, sa lecture en « 2022 à 2024 » n'est qu'une analogie avec les usages 6 à 16 et 18 à 28 (point ouvert 14)
    18: {"rcu": (1460, 1120, 1120), "autres": (None, 585, 585)},
    19: {"rcu": (1155, 890, 890), "autres": (None, 330, 330)},
    20: {"rcu": (575, 490, 490), "autres": (None, 320, 320)},
    21: {"rcu": (615, 365, 365), "autres": (None, 230, 230)},
    22: {"rcu": (290, 260, 260), "autres": (None, 260, 260)},
    23: {"rcu": None, "autres": (None, 315, 315)},               # une seule ligne, sans distinction RCU, p. 31
    24: {"rcu": None, "autres": (None, 110, 110)},               # p. 32
    25: {"rcu": (330, 265, 265), "autres": (None, 150, 150)},
    26: {"rcu": (570, 445, 445), "autres": (None, 445, 445)},
    27: {"rcu": (615, 485, 485), "autres": (None, 485, 485)},
    28: {"rcu": (535, 420, 420), "autres": (None, 190, 190)},
}
```

Règles complémentaires (p. 32) : maisons individuelles, Icénergie_maxmoyen = 280 kg CO2/m² si permis déposé avant le 31 décembre 2023 et parcelle sous permis d'aménager (avant le 1er janvier 2022) ou ZAC prévoyant le gaz ; parties raccordées à un réseau de chaleur et de froid **classé** (L. 712-1 du code de l'énergie) avec permis déposé avant le 31 décembre 2027 : valeur de la colonne « 2022 à 2024, raccordé » de l'usage. Le texte ne motive pas la présence de la colonne « 2022 à 2024, raccordés » pour les usages 6 à 28, qui n'étaient pas soumis avant le 1er mai 2026 ; la rattacher à cette règle est une interprétation, sans conséquence sur les tables.

### 5.3 Mcgéo (trois lignes d'altitude, huit zones)

```python
MCGEO = {
    1: ((0.1, 0.15, 0.1, -0.05, 0.0, -0.1, -0.10, -0.15), (0.4, 0.5, 0.4, 0.15, 0.3, 0.05, 0.0, -0.1), (0.75, 0.85, 0.75, 0.55, 0.6, 0.35, 0.25, 0.15)),     # p. 32-33
    2: ((0.05, 0.05, 0.05, -0.1, 0.0, -0.15, -0.1, -0.15), (0.35, 0.4, 0.35, 0.2, 0.2, 0.05, 0.05, -0.1), (0.55, 0.65, 0.55, 0.45, 0.5, 0.3, 0.3, 0.15)),    # p. 34
    3: ((0.05, 0.10, 0.10, 0.0, 0.0, 0.0, 0.15, 0.15), (0.20, 0.25, 0.20, 0.15, 0.15, 0.05, 0.10, -0.05), (0.35, 0.40, 0.35, 0.35, 0.30, 0.20, 0.25, 0.10)),  # p. 35
    4: ((0.05, 0.15, 0.10, -0.05, 0.0, -0.05, 0.40, 0.30), (0.30, 0.30, 0.30, 0.15, 0.20, 0.10, 0.30, 0.10), (0.60, 0.60, 0.60, 0.45, 0.50, 0.35, 0.35, 0.15)),  # p. 36, primaire et secondaire
    6: ((0.1, 0.15, 0.1, -0.05, 0.0, -0.05, 0.15, 0.05), (0.25, 0.3, 0.2, 0.1, 0.15, 0.05, 0.1, 0.0), (0.5, 0.45, 0.4, 0.35, 0.35, 0.2, 0.2, 0.05)),          # p. 36
    7: ((0.05, 0.10, 0.10, -0.05, 0.0, 0.0, 0.2, 0.15), (0.1, 0.15, 0.15, 0.0, 0.05, 0.0, 0.1, 0.05), (0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0)),              # p. 37
    8: ((0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.05, 0.0), (0.2, 0.25, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05), (0.35, 0.35, 0.35, 0.25, 0.25, 0.2, 0.25, 0.1)),             # p. 38
    9: ((0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.05, 0.0), (0.2, 0.25, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05), (0.35, 0.35, 0.35, 0.25, 0.25, 0.2, 0.25, 0.1)),             # p. 39
    10: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.05, 0.15, 0.1), (0.1, 0.15, 0.15, 0.0, 0.05, 0.05, 0.15, 0.1), (0.2, 0.2, 0.2, 0.1, 0.15, 0.1, 0.15, 0.05)),          # p. 40
    11: ((0.05, 0.1, 0.1, 0.0, 0.0, 0.0, 0.1, 0.1), (0.1, 0.15, 0.15, 0.05, 0.05, 0.05, 0.1, 0.05), (0.2, 0.25, 0.2, 0.15, 0.15, 0.1, 0.15, 0.05)),           # p. 41
    12: ((0.1, 0.1, 0.1, 0.0, 0.0, -0.05, 0.05, -0.05), (0.25, 0.25, 0.25, 0.2, 0.20, 0.1, 0.1, 0.0), (0.45, 0.4, 0.4, 0.35, 0.35, 0.25, 0.25, 0.15)),        # p. 42
    13: ((0.0, 0.05, 0.1, -0.05, 0.0, 0.05, 0.2, 0.15), (0.1, 0.1, 0.1, 0.0, 0.05, 0.05, 0.15, 0.05), (0.2, 0.2, 0.15, 0.10, 0.15, 0.10, 0.15, 0.05)),        # p. 42
    14: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, 0.05, -0.05), (0.25, 0.25, 0.2, 0.15, 0.2, 0.05, 0.1, 0.0), (0.4, 0.4, 0.35, 0.35, 0.35, 0.2, 0.2, 0.05)),         # p. 43
    15: ((0.05, 0.1, 0.05, -0.05, 0.0, 0.0, 0.15, 0.1), (0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05), (0.15, 0.2, 0.15, 0.1, 0.15, 0.05, 0.1, 0.05)),         # p. 44
    16: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.0, 0.1, 0.05), (0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.1, 0.0), (0.3, 0.3, 0.25, 0.2, 0.25, 0.15, 0.15, 0.05)),           # p. 45
    17: ((0.0, 0.05, 0.1, -0.05, 0.0, 0.05, 0.2, 0.2), (0.0, 0.1, 0.1, -0.05, 0.05, 0.05, 0.15, 0.15), (0.05, 0.1, 0.1, 0.0, 0.05, 0.05, 0.1, 0.1)),          # p. 46
    18: ((0.05, 0.1, 0.05, 0.0, 0.0, -0.05, 0.0, -0.05), (0.15, 0.15, 0.15, 0.1, 0.15, 0.05, 0.05, -0.05), (0.3, 0.3, 0.3, 0.25, 0.25, 0.15, 0.15, 0.05)),    # p. 47
    19: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, 0.0, -0.05), (0.25, 0.25, 0.2, 0.15, 0.15, 0.1, 0.1, -0.05), (0.4, 0.4, 0.35, 0.3, 0.35, 0.2, 0.25, 0.1)),         # p. 48
    20: ((0.05, 0.05, 0.1, 0.0, 0.0, 0.05, 0.1, 0.1), (0.05, 0.1, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05), (0.1, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05)),            # p. 48
    21: ((0.05, 0.1, 0.1, -0.05, 0.0, -0.05, 0.1, 0.1), (0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.15, 0.1), (0.3, 0.35, 0.3, 0.25, 0.25, 0.15, 0.2, 0.2)),         # p. 49
    22: ((-0.05, 0.0, 0.05, -0.05, 0.0, 0.0, 0.1, 0.1), (-0.05, 0.0, 0.05, -0.1, 0.1, 0.2, 0.25, 0.0), (0.05, 0.1, -0.05, 0.0, 0.05, 0.15, 0.15, 0.0)),       # p. 50
    23: ((0.05, 0.05, 0.1, -0.05, 0.0, 0.05, 0.15, 0.15), (0.05, 0.05, 0.1, 0.0, 0.05, 0.05, 0.1, 0.1), (0.1, 0.15, 0.15, 0.05, 0.1, 0.05, 0.1, 0.05)),       # p. 51
    24: ((0.05, 0.1, 0.1, -0.05, 0.0, 0.0, 0.2, 0.15), (0.15, 0.15, 0.2, 0.05, 0.1, 0.05, 0.15, 0.1), (0.25, 0.3, 0.3, 0.2, 0.2, 0.1, 0.2, 0.1)),             # p. 52
    25: ((0.0, 0.1, 0.1, -0.1, 0.0, 0.0, 0.4, 0.25), (0.05, 0.1, 0.05, -0.05, 0.0, -0.05, 0.2, 0.05), (0.1, 0.15, 0.1, 0.05, 0.1, 0.0, 0.1, 0.0)),            # p. 53
    26: ((0.1, 0.1, 0.05, 0.0, 0.0, -0.05, -0.05, -0.15), (0.25, 0.25, 0.2, 0.2, 0.2, 0.1, 0.05, -0.05), (0.45, 0.45, 0.4, 0.35, 0.4, 0.25, 0.20, 0.1)),      # p. 54
    27: ((0.05, 0.1, 0.05, 0.0, 0.0, 0.0, 0.0, -0.05), (0.2, 0.2, 0.15, 0.1, 0.15, 0.05, 0.05, 0.0), (0.3, 0.35, 0.3, 0.25, 0.25, 0.2, 0.15, 0.1)),           # p. 54
    28: ((0.0, 0.1, 0.05, -0.1, 0.0, 0.05, 0.35, 0.25), (0.0, 0.05, 0.05, -0.05, 0.0, -0.05, 0.15, 0.05), (0.05, 0.1, 0.05, 0.0, 0.05, 0.0, 0.1, -0.05)),     # p. 55
}
MCGEO[5] = MCGEO[4]   # p. 36
```

Les établissements sportifs privés (28) ont leur propre Mcgéo (p. 55), différent de celui des municipaux (25, p. 53), alors qu'ils partagent le Mbgéo (p. 26).

### 5.4 Mccombles et Mcsurf_moy

- Mccombles = 0,4 × Scombles / Sref pour l'usage 1 (p. 33) ; 0 pour les usages 2 à 28 (p. 34 à 55).
- Mcsurf_moy (diviseur Cep,nr_maxmoyen de l'usage) :

```python
MCSURF_MOY = {   # (borne_sup, a, b) sur Smoylgt : (a + b*S)/Cep,nr_maxmoyen
    1: ((100, 49.5, -0.55), (150, 14.5, -0.2), (None, -15.5, 0.0)),               # p. 33
    2: ((40, 45.0, -1.0), (80, 15.0, -0.25), (120, 3.0, -0.1), (None, -9.0, 0.0)),  # p. 34
}
# 0 pour les usages 3 à 28 (p. 35 à 56).
```

### 5.5 Mcsurf_tot (diviseur Cep,nr_maxmoyen, S = somme des Sref des parties de même usage, chapitre II, II, p. 4)

```python
MCSURF_TOT = {
    1: None,                                                                   # p. 33
    2: ((1300, 13.0, -0.01), (None, 0.0, 0.0)),                                # p. 34
    3: ((500, 18.0, -0.032), (1500, 6.0, -0.008), (None, -6.0, 0.0)),          # p. 35
    4: ((500, 12.5, -0.025), (None, 0.0, 0.0)), 5: ((500, 12.5, -0.025), (None, 0.0, 0.0)),   # p. 36
    6: None, 7: None, 8: None,                                                 # p. 37, 38, 39
    9: ((1000, 81.0, -0.081), (None, 0.0, 0.0)),                               # p. 39, hôtels 3 à 5 étoiles partie nuit
    10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None,      # p. 40 à 45
    17: ((500, 113.0, -0.226), (None, 0.0, 0.0)),                              # p. 46, commerces
    18: None, 19: None, 20: None,                                              # p. 47, 48, 49
    21: ((2000, 0.0, 0.0), (5000, 49.0, -0.026), (None, -78.0, 0.0)),          # p. 50, santé partie jour
    22: None,                                                                  # p. 50
    23: ((5000, 15.0, -0.003), (None, 0.0, 0.0)),                              # p. 51, industrie 3x8
    24: "selon réseau de chaleur et année, voir ci-dessous",                    # p. 52
    25: None, 26: None, 27: None, 28: None,                                    # p. 53, 54, 55, 56
}
# Industrie 8h à 18h (24), p. 52, pour S <= 5000 m² (0 au-delà) :
#   raccordé à un réseau de chaleur urbain classé, « année 2025 à 2028 » : (365 - 0,073 S) / Cep,nr_maxmoyen
#   raccordé à un réseau classé, « à partir de l'année 2028 » : (265 - 0,053 S) / Cep,nr_maxmoyen
#   raccordé à un réseau non classé : (265 - 0,053 S) / Cep,nr_maxmoyen
#   autre cas : (265 - 0,053 S) / Cep,nr_maxmoyen
```

### 5.6 Mccat (catégorie de contraintes extérieures, chapitre V)

```python
MCCAT = {   # par catégorie ; tuple de huit = par zone climatique ; scalaire = toutes zones ; absent = 0
    1: {2: (0, 0, 0, 0, 0, 0, 0.1, 0.1)},                        # p. 33 (catégorie 1 : 0)
    2: {2: (0, 0, 0, 0, 0, 0, 0.1, 0.1)},                        # p. 34
    3: {},                                                        # p. 35, Mccat = 0
    4: {2: 0.05}, 5: {2: 0.05},                                   # p. 36 (cat 1 : 0)
    6: {3: (0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.2, 0.3)},        # p. 37 (cat 1 et 2 : 0)
    7: {3: (0, 0, 0, 0, 0, 0, 0.05, 0.05)},                       # p. 38
    8: {}, 9: {}, 10: {}, 11: {},                                 # p. 39, 40, 40, 41
    12: {3: (0, 0.05, 0.05, 0, 0.05, 0.05, 0.2, 0.25)},           # p. 42
    13: {}, 14: {}, 15: {}, 16: {},                               # p. 43, 44, 45, 45
    17: {3: 0.05},                                                # p. 46 (tableau libellé BR1 / BR2-BR3 / Cat 3 : 0 / 0 / 0,05)
    18: {}, 19: {}, 20: {}, 21: {}, 22: {}, 23: {}, 24: {}, 25: {}, 26: {}, 27: {}, 28: {},   # p. 47 à 56
}
```

## 6. Icconstruction_max (chapitre III, III, p. 56-87), pour mémoire : indicateur ACV, hors moteur Th-BCE

### 6.1 Icconstruction_maxmoyen (p. 56-57), kg éq. CO2/m², années 2022-2024 / 2025-2027 / 2028-2030 / à partir de 2031

```python
IC_CONSTRUCTION_MAX_MOYEN = {   # None = colonne 2022 à 2024 sans valeur : tiret « - » pour 6 à 17 (p. 56-57), cellule absente sans tiret pour 18 à 28 (p. 57) ; valeurs inchangées, tables pour mémoire
    1: (640, 530, 475, 415), 2: (740, 650, 580, 490), 3: (980, 810, 710, 600), 4: (900, 770, 680, 590), 5: (900, 770, 680, 590),
    6: (None, 940, 785, 630), 7: (None, 940, 790, 640),
    8: (None, 820, 680, 540), 9: (None, 820, 680, 540), 10: (None, 820, 680, 540), 11: (None, 820, 680, 540),
    12: (None, 950, 780, 630),
    13: (None, 800, 670, 540), 14: (None, 800, 670, 540), 15: (None, 800, 670, 540), 16: (None, 800, 670, 540),
    26: (None, 800, 670, 540), 27: (None, 800, 670, 540), 17: (None, 800, 670, 540),
    18: (None, 1050, 900, 750), 19: (None, 880, 760, 620), 20: (None, 880, 760, 620), 21: (None, 880, 760, 620),
    22: (None, 1120, 950, 780), 23: (None, 840, 695, 550), 24: (None, 840, 695, 550), 25: (None, 900, 760, 620), 28: (None, 900, 760, 620),
}
```

### 6.2 Coefficients Mi (p. 57-87)

Micombles = 0,4 × Scombles / Sref pour l'usage 1 (p. 57), 0 ailleurs. Misurf_moy : usage 1, 0,36 − 3,6 × Smoylgt / 1000 si Smoylgt ≤ 120 m², −0,072 au-delà (p. 58) ; usage 2, (100 − 2,5 × Smoylgt) / Icconstruction_maxmoyen si Smoylgt ≤ 40 m², 0 au-delà (p. 60) ; 0 pour 3 à 28. Les seuils Miinfra (lot 2), Mivrd (lot 1), Mipv (lot 13) donnent max(0, Iclot − seuil) ; Mided vaut 0,3 × (Icded − seuil) en 2022-2024 (usages 1 à 5 seulement), 0 en 2025-2027 et −0,3 × (Icded − seuil) à partir de 2028.

```python
MI = {   # usage: (Misurf_tot, Migéo H2d/H3 si alt < 400 m, seuil Miinfra, seuil Mivrd, seuil Mipv, seuil Mided)
    1: (None, 30, 40, 20, 20, 370),                                                       # p. 58-59 ; Misurf_tot = 0
    2: (((1300, -0.104, 0.8e-4), (3999.99, 0.0455, -0.350e-4), (None, -0.0945, 0.0)), 30, 40, 10, 20, 250),   # p. 60-61 (formules sans diviseur)
    3: (((2500, 0.034, -0.86e-4), (None, -0.181, 0.0)), 50, 40, 10, 20, 275),              # p. 62-63
    4: (((10000, 0.084, -0.21e-4), (None, -0.126, 0.0)), 0, 60, 20, 20, 300), 5: "idem 4",  # p. 64-65
    6: (None, 30, 60, 20, 20, 440),                                                       # p. 65-67
    7: (None, 30, 60, 20, 20, 320),                                                       # p. 67-69
    8: (None, 20, 40, 10, 20, 300), 9: "idem 8", 10: "idem 8", 11: "idem 8",              # p. 69-71
    12: (None, 0, 60, 20, 20, 530),                                                       # p. 71-73
    13: (None, 0, 40, 10, 20, 480), 14: "idem 13", 15: "idem 13", 16: "idem 13", 26: "idem 13", 27: "idem 13",   # p. 73-75
    17: (None, 0, 40, 10, 20, 280),                                                       # p. 75-77
    18: (None, 0, 40, 10, 20, 480),                                                       # p. 77-79
    19: (None, 0, 40, 10, 20, 580), 20: "idem 19", 21: "idem 19",                         # p. 79-81
    22: (None, 0, 100, 10, 20, 665),                                                      # p. 81-83
    23: (((5000, 0.035, -0.00007), (None, -0.315, 0.0)), 0, 40, 10, 20, 500), 24: "idem 23",   # p. 83-85
    25: (((2000, 0.3, -0.00015), (None, 0.0, 0.0)), 0, 60, 20, 20, 480), 28: "idem 25",   # p. 85-87
}
```

Le texte écrit la borne des logements collectifs « 1300 < Sref < 4000 » puis « Sref ≥ 4000 » (p. 60) : la borne 3999,99 ci-dessus traduit le strict.

## 7. DH_max (chapitre III, IV, p. 87-93)

Colonnes du texte : catégorie 1 « sauf parties climatisées en H2d et H3 », catégorie 1 climatisé en H2d ou H3, catégorie 2, catégorie 3 (quand la colonne existe : « Pas de seuil »).

```python
DH_MAX = {   # usage: (cat1, cat1 climatisé en H2d/H3, cat2, cat3) ; None = pas de seuil ; "non spécifié" = colonne absente
    1: (1250, 1250, 1850, "non spécifié"),       # p. 87 (deux colonnes seulement : catégorie 1, catégorie 2)
    2: "formule par Smoylgt, voir ci-dessous",    # p. 87
    3: (1150, 2400, 2600, None),                  # p. 88
    4: (900, 1800, 2200, "non spécifié"), 5: (900, 1800, 2200, "non spécifié"),   # p. 88
    6: (900, 2200, 2400, None),                   # p. 88
    7: (900, 2200, 2400, None),                   # p. 88
    8: (300, 700, 1000, None), 9: (300, 700, 1000, None),        # p. 88-89
    10: (1300, 3300, 3400, None), 11: (1300, 3300, 3400, None),  # p. 89
    12: (550, 1600, 1600, None),                  # p. 89
    13: (2500, 5000, 5000, None),                 # p. 89
    14: (250, 650, 650, None),                    # p. 90
    15: (1600, 3500, 3500, None),                 # p. 90
    16: (1250, 2500, 2500, None),                 # p. 90
    17: (3300, 8000, 9500, None),                 # p. 90
    18: (1000, 2200, 2200, "non spécifié"),       # p. 90
    19: (900, 2400, 2600, "non spécifié"),        # p. 91
    20: (900, 2400, 2600, "non spécifié"),        # p. 91
    21: (1250, 3000, 3300, None),                 # p. 91
    22: (12100, 21500, 21500, None),              # p. 91
    23: (3200, 8000, 8000, "non spécifié"),       # p. 92
    24: (900, 2200, 2200, "non spécifié"),        # p. 92
    25: (2000, 4600, 5000, "non spécifié"),       # p. 92
    26: (40, 170, 170, None),                     # p. 92
    27: (260, 650, 650, None),                    # p. 93
    28: (2000, 4600, 5000, "non spécifié"),       # p. 93
}
# Logements collectifs (p. 87), S = Smoylgt :
#   catégorie 1 hors climatisé H2d/H3 : 1250
#   catégorie 1 climatisé H2d/H3 : 1600 si S <= 20 ; 1700 - 5 S si 20 < S <= 60 ; 1400 si S > 60
#   catégorie 2 : 2600 si S <= 20 ; 2850 - 12,5 S si 20 < S <= 60 ; 2100 si S > 60
# Déjà codé (dh_max L97-103). Pour l'usage 1 : 1250 en catégorie 1, 1850 en catégorie 2 (dh_max L95-96).
```

Les usages 4, 5, 18, 19, 20, 23, 24, 25, 28 n'ont pas de colonne catégorie 3 : le texte ne donne rien pour une partie de bâtiment de catégorie 3 de ces usages (non spécifié ; le moteur ne doit pas inventer « pas de seuil »).

## 8. Catégories de contraintes extérieures et classes de bruit

- Le chapitre III renvoie pour les catégories de contraintes extérieures et les zones de bruit au chapitre V de l'annexe (p. 4, 7, 33, 87), **absent du corpus lu** (le fichier s'arrête au chapitre III). Les catégories utilisées par le chapitre III sont trois : 1, 2 et 3. Le périmètre de la catégorie 3 diffère selon le coefficient : Mbbruit non nul en catégorie 3 pour les usages 3, 6, 7, 8 à 12 et 17 (§ 4.5, p. 9 à 20) ; Mccat non nul en catégorie 3 pour les usages 6, 7, 12 et 17 seulement (§ 5.6, p. 37, 38, 42, 46) ; colonne DH « Pas de seuil » en catégorie 3 pour les usages 3, 6 à 17, 21, 22, 26 et 27 (§ 7, p. 88-93).
- Annexe III : `Categorie_CE1_CE2` est une donnée d'entrée du groupe, « 1 = CE1 / 2 = CE2 » (nomenclature de la fiche brasseurs d'air, p. 990) et « 0 ou 1 » (nomenclature de la fiche 13.1, p. 1356) ; la fiche 13.1 cumule les Sref des groupes CE1 et CE2 de la zone pour les usages 1 et 2 (équation 2387, p. 1360). `Isclimatise` est l'indicateur de climatisation du groupe (p. 990). La méthode ne calcule donc pas la catégorie : elle la reçoit.
- Classes BR1, BR2, BR3 : fiche 5.11 de l'annexe III (p. 245-247), baie par baie, d'après le classement sonore des infrastructures (arrêté préfectoral, L. 571-10 du code de l'environnement), la distance et la vue de l'infrastructure, et les zones A à D du plan d'exposition au bruit (zone A, B, C : BR3 ; zone D : BR2 ; hors zone : BR1, p. 246). Le RSEE porte en plus une classe de groupe `Exp_BR_Groupe` que le banc lit avec « 0 traité comme BR3 » (banc/exigences.py L55).
- Dans le moteur : `categorie_ce` (1, 2 ou 3) et `exposition_bruit` (1, 2, 3) restent des entrées, lues du RSEE (`Groupe/Categorie_CE`, `Groupe/Exp_BR_Groupe`, `Groupe/Is_Climatise`). Le codage de la catégorie 3 dans le RSEE est un point ouvert (§ 10).

## 9. Bâtiments à plusieurs usages

- Chapitre II, V (p. 5) : pour un bâtiment à plusieurs zones définies par leur usage, Bbio_max, Cep,nr_max, Cep_max, Icénergie_max et Icconstruction_max du bâtiment sont calculés au prorata des Sref de chaque zone, à partir des valeurs de chaque zone. DH_max reste par partie thermiquement homogène (chapitre II, IV, p. 4-5 ; FA05 p. 12 : « par groupe et donc par usage et type Cat1/Cat2, climatisés ou non, traversant ou non »).
- Mbsurf_tot et Mcsurf_tot se calculent, pour chaque usage, sur la somme des Sref des parties de bâtiment de cet usage (chapitre II, I et II, p. 3-4) : le banc le fait déjà par `sref_usage` (banc/exigences.py L40-43).
- Assimilation à l'usage principal (arrêté du 4 août 2021 art. 2, FA05 p. 3 et 7-8) : une partie de Sref < 150 m² **et** < 10 % de la Sref de l'usage principal peut prendre l'usage principal (scénarios et exigences de l'usage principal, systèmes propres décrits) ; la partie principale doit être soumise à l'arrêté ou à la RT2012 ; une partie à usage de maison individuelle n'est jamais assimilée ; la règle ne joue pas si les autres locaux ne sont soumis ni à la RT2012 ni à la RE2020 (FA05 p. 8).
- Bâtiments accolés : un seul bâtiment si parois mitoyennes d'au moins 15 m² (maisons) ou 50 m² (autres) (FA05 p. 6, annexe I de l'arrêté).
- Vestiaires des établissements sportifs : compris dans les scénarios des usages 25 et 28, pas de zone « vestiaires seuls » (FA05 p. 4).

```python
def ponderation_sref(valeurs: list[tuple[float, float]]) -> float:
    """Chapitre II, V, p. 5 : valeurs [(Sref_zone, X_max_zone), ...] -> X_max du bâtiment au prorata des Sref."""
    s = sum(sref for sref, _ in valeurs)
    return sum(sref * x for sref, x in valeurs) / s if s > 0 else 0.0
```

## 10. Points ouverts

1. Chapitre V (définition des catégories 1, 2, 3 et des zones de bruit) absent du corpus : les catégories restent des entrées. Le texte lu ne dit pas si une catégorie 3 existe pour les usages 4, 5, 18 à 20, 23 à 25, 28 (colonne absente des tableaux DH, Mbbruit = 0, Mccat = 0) : on code « non spécifié » (erreur explicite) pour DH_max si categorie_ce = 3 sur ces usages.
2. Codage de la catégorie 3 dans le RSEE : la nomenclature de l'annexe III ne connaît que CE1 et CE2 (p. 990, p. 1356). Le moteur garde sa convention actuelle (`Categorie_CE >= 3`, exigences.py L78 et L105) ; seul le banc des bureaux (usage 3, les seuls RSEE tertiaires disponibles) peut la confirmer.
3. `Exp_BR_Groupe` = 0 traité comme BR3 (banc/exigences.py L55) : convention déduite du banc des logements, à maintenir pour les usages 6, 7, 12 dont Mbbruit dépend de la catégorie 3 et non de la classe BR ; sans effet sur les usages où Mbbruit = 0.
4. Mcsurf_tot de l'industrie 8h à 18h (p. 52) : les colonnes « réseau classé, année 2025 à 2028 » et « réseau classé, à partir de l'année 2028 » se recouvrent sur 2028. On code 2025 à 2027 pour la première (par analogie avec les autres tableaux du chapitre, tous bornés 2025 à 2027) et 2028 et au-delà pour la seconde ; les trois autres colonnes sont identiques entre elles. Le cas « classé » suppose une donnée d'entrée que le RSEE ne porte peut-être pas (réseau classé L. 712-1) : à lire au banc.
5. Mcsurf_tot des établissements de santé partie jour (p. 50) : 0 jusqu'à 2 000 m² puis (49 − 0,026 S)/165 = −0,018 juste au-dessus : discontinuité du texte, reproduite telle quelle.
6. Mbgéo des aérogares (p. 23) : la ligne > 800 m (0,05, 0,15, −0,05, 0, 0,1, 0,25, 0,25, 0,05) est inférieure à la ligne 400-800 m en H1a-H2a ; reproduite telle quelle, sans correction.
7. Mccat de l'usage 17 (p. 46) et Mbbruit des usages 3, 8 à 11, 17 : les tableaux sont libellés « BR1 / BR2-3 / Cat 3 », mélange de classe de bruit et de catégorie ; on lit « 0 sauf en catégorie 3 ».
8. Borne « 400m-800m » : le texte ne dit pas si 400 m et 800 m exacts vont à la ligne du milieu ; la convention actuelle (`mbgeo` L32 : alt < 400 ligne 1, 400 ≤ alt ≤ 800 ligne 2) est conservée, déjà conforme au banc des usages 1 à 3.
9. Diviseur Cep,nr_maxmoyen pour les modulations appliquées à Cep_max et Icénergie_max (p. 33 et suivantes) : lu littéralement. Les sorties O_Mcgeo, O_Mccombles, O_Mcsurf_moy, O_Mcsurf_tot, O_Mccat, O_Cep_Max, O_Cep_nr_Max (specs/bilans.md L27 et L458) permettront de le vérifier sur les usages 1 à 3 seulement.
10. Icénergie_max : la règle des réseaux classés (p. 32, permis avant le 31 décembre 2027) et la règle du gaz pour les maisons (280 kg, p. 32) demandent deux entrées (réseau classé, permis d'aménager gaz) que le moteur n'a pas ; tables fournies, fonction à n'écrire que si une sortie RSEE existe (aucune O_Icenergie_max connue du banc).
11. Icconstruction_max et coefficients Mi : indicateur ACV, hors Th-BCE ; tables données pour mémoire, pas de code prévu dans exigences.py.
12. Année du permis : le banc la déduit de `date_depot_PC`, sinon du millésime du RSEE (banc/exigences.py L29-32) ; utilisée pour Mbsurf_tot des bureaux, Mcsurf_tot de l'usage 24, Icénergie et Icconstruction. Pour les usages 6 à 28 un permis antérieur au 1er mai 2026 n'est pas soumis : le moteur signale l'usage comme non validé sans refuser le calcul.
13. Surface de référence des hôtels (usages 8 à 11) : aucun texte lu ne dit si un hôtel est « à usage d'habitation » au sens du X du chapitre I (p. 2). La SU est déduite de l'unité « m² de surface utile » du tableau 278 (arrêté du 19 mars 2026 art. 5 VI A) et de FA05 p. 9 : déduction non écrite, `SURFACE_REFERENCE` la porte avec ce commentaire.
14. Icénergie_maxmoyen de l'usage 17 « autres cas » (p. 31) : cellule « 2022 à 2024 » sans valeur ni tiret, codée « non spécifié » ; sans effet pratique, l'usage n'étant pas soumis avant le 1er mai 2026. Même situation pour Icconstruction des usages 18 à 28 (p. 57), tables pour mémoire, `None` conservé.

## 11. Où coder

Fichier `openbce/exigences.py` (109 lignes aujourd'hui) :

- L15 `USAGES` : remplacer le dict de 5 entrées par `usages.NOMS` (openbce/usages.py L11-40, déjà 28 noms) ou l'étendre à 28 ; L16 `BBIO_MAX_MOYEN` : § 4.1.
- L19-25 `MBGEO` : § 4.2 (28 clés, alias 5 → 4 et 28 → 25).
- L27 `MBBRUIT_BR23` : inchangé ; L28 `MBBRUIT_BUREAUX_CAT3` : remplacer par `MBBRUIT_CAT3` (§ 4.5).
- L31-33 `mbgeo` : inchangé. L36-37 `mbcombles` : inchangé. L40-50 `mbsurf_moy` : inchangé (0 hors usages 1 et 2).
- L53-71 `mbsurf_tot` : garder les branches 1 à 5, ajouter les segments du § 4.4 pour 17, 21, 23, 24, 0 pour les autres (table `MBSURF_TOT` + fonction générique `_segments(table, S, ref)`).
- L74-81 `mbbruit` : usages 1 et 2 par `MBBRUIT_BR23` (BR ≥ 2), usages de `MBBRUIT_CAT3` par `categorie_ce >= 3` (scalaire ou tuple indexé par `ZONES.index(zone)`), 0 sinon.
- L84-89 `bbio_max` : signature inchangée ; les appelants (banc/exigences.py L54, banc/sortie_rsee.py L83) n'ont rien à changer.
- L93-108 `dh_max` : garder les branches 1 et 2, remplacer la branche finale (L108, qui applique 900/1800/2200 à tout usage > 3) par la table `DH_MAX` du § 7 ; lever `ValueError("DH_max non spécifié")` pour categorie_ce = 3 sur un usage sans colonne 3 ; `None` pour « pas de seuil ».
- Nouveau bloc Cep (après L108) : constantes `CEP_NR_MAX_MOYEN`, `CEP_MAX_MOYEN`, `IC_ENERGIE_MAX_MOYEN`, `MCGEO`, `MCSURF_MOY`, `MCSURF_TOT`, `MCCAT` ; fonctions `mcgeo(usage, zone, altitude)` (même indexation que `mbgeo`), `mccombles(usage, s_combles, sref)` (usage 1), `mcsurf_moy(usage, sref, nb_logements)`, `mcsurf_tot(usage, sref_usage, annee_permis=2026, reseau_classe=False)`, `mccat(usage, zone, categorie_ce)`, et `cep_max(usage, zone, altitude, sref, nb_logements, sref_usage, s_combles=0.0, categorie_ce=1, annee_permis=2026, reseau_classe=False) -> dict` renvoyant mcgeo, mccombles, mcsurf_moy, mcsurf_tot, mccat, cep_nr_max, cep_max (et ic_energie_max si demandé).
- Nouveau : `ponderation_sref` (§ 9) et `SURFACE_REFERENCE` (§ 2).
- En-tête du module (L3-10) : citer les pages 6 à 93 et la mention « usages 4 à 28 non validés ».

Fichier `banc/exigences.py` :

- L51 et L80 : le filtre `usage not in exigences.BBIO_MAX_MOYEN` laisse passer les 28 usages dès que la table est étendue ; ajouter un compteur par usage des groupes rencontrés (les RSEE du lot n'en ont que 1, 2 et 3 : le banc doit dire « 0 groupe » pour 4 à 28, pas « écart »).
- L14-15 `CLES` : ajouter les sorties Cep quand `cep_max` existe : (« mcgeo », « O_Mcgeo »), (« mccombles », « O_Mccombles »), (« mcsurf_moy », « O_Mcsurf_moy »), (« mcsurf_tot », « O_Mcsurf_tot »), (« mccat », « O_Mccat »), (« cep_max », « O_Cep_Max »), (« cep_nr_max », « O_Cep_nr_Max ») lues dans `Sortie_Groupe_C` ou `Sortie_Zone_C` (specs/bilans.md L458).
- L86 : accepter `m is None` comme « pas de seuil » sans compter d'écart si `O_NbDegresHeures_max` est absent ou nul.

Autres fichiers touchés (lecture seule ici, à modifier au codage) :

- `openbce/usages.py` L42 `VALIDES = frozenset({1, 2, 3})` : inchangé, c'est lui qui porte l'avertissement « non validé » (fonctions `nom`, `non_valides` et `avertissement`, L45-60 ; `avertissement` L54-60).
- `banc/sortie_rsee.py` (fichier du 09/10/2026 20:21) L50 `if usage not in (1, 2, 3)` : lever la restriction une fois scénarios et exigences étendus ; L54 `cle_s` : inchangé (§ 2) ; L81 (`dh_max`) et L83 (`bbio_max`) : inchangés ; alimenter `cep_max` et `cep_nr_max` du dict `cep` pour `openbce/sortie_rsee.py` L182 (O_Cep_Max, O_Cep_nr_Max, aujourd'hui non renseignés).
- `openbce/sortie_rsee.py` L83-87 (`if bbio_max:` L83, O_Bbio_Max L84, O_Mb* L86-87) : écrit O_Bbio_Max et O_Mb* ; ajouter O_Mc* au même endroit dans `Sortie_Groupe_C`.
- `openbce/api.py` L47 et `openbce/serveur_mcp.py` L255 : remontent `bbio_max` et `dh_max_groupes`, à compléter par `cep_max`.
