# Spécification « confort » pour les 28 usages : ouverture des baies, confort d'été, saisons, brasseurs d'air, relance et intermittence

Date : 09/10/2026. Décision de Cédric PLANTAZ (ARKEMEP) du 09/10/2026 : « go code les 28 usages, marqués non validés ».

**Usages 4 à 28 non validés : aucun récapitulatif de référence.** Le NAS ne contient aucun RSEE RE2020 d'usage 4 à 28 ; ce qui suit est codé sur la foi du texte, rien n'a été demandé au CSTB, et `openbce.usages.VALIDES` reste `{1, 2, 3}`.

Périmètre : règles de Th-B et Th-D qui dépendent de l'usage, hors ventilation, éclairage et ECS. Thèmes : fiche 5.13 (ouverture des baies), fiche 13.5 (confort d'été), fiche 4.6 (saisons), fiche 8.32 (brasseurs d'air), fiches 8.1 et 8.5 (variation temporelle, relance, arrêt de plus de 48 h), ligne 187 de `groupe.py`.

## Sources lues

Texte de référence : annexe III consolidée (`corpus/texte_annexe3_2026-07/annexe3.txt`, 1 854 pages, arrêté du 19 mars 2026 inclus). Pages lues :

- fiche 4.1 : tableau 4 « liste des usages de la zone » avec les indicateurs `ihebergement` et `ienseignement`, p. 57 ; synthèse des scénarios (consignes confort / réduit court / réduit long, plages d'occupation), p. 23 à 26 ;
- fiche 4.5 indicateurs de confort, p. 71 à 79 (équations 56 à 65) ;
- fiche 4.6 détermination des saisons, p. 80 à 94 (équations 66 à 91, tableaux 8 à 11) ;
- fiche 5.9 gestion des protections mobiles : équations 178 et 179, p. 188 ; figure 34 (familles d'usages, Pocc, Pderog), p. 195 et 196 ; légendes des figures 35 à 47 (matrices conventionnelles par famille et par type de protection), p. 197 à 206 ;
- fiche 5.13 surventilation par ouverture des baies, p. 255 à 271 (tableaux 41 à 44, équations 240 à 256) ;
- fiche 8.1 émission : nomenclature p. 507 et 508, variation temporelle p. 517 à 519 (tableaux 87 et 88), saisons de fonctionnement p. 523 et 524 ;
- fiche 8.4 saisons de fonctionnement des systèmes, p. 551 à 555 ;
- fiche 8.5 programmation des relances, p. 556 à 561 (tableaux 91 à 93, équations 844 à 849) ;
- fiche 8.32 brasseurs d'air, p. 989 à 1002 (tableaux 256 à 258, équations 1646 à 1666) ;
- fiche 13.1 sorties du mode Th-B : nomenclature p. 1356, équation 2387 p. 1360 (catégorie CE1/CE2) ;
- fiche 13.5 confort d'été, p. 1396 à 1403 (tableaux 339 et 340, équations 2542 à 2551).

Autres sources : tableur officiel des scénarios du 29/04/2026 converti en `openbce/tables/scenarios_officiels.json` (consignes, matrices hebdomadaires d'occupation et de consigne, profils annuels) ; fiche d'application FA05 v2 du 01/10/2026 (identification de l'usage, rattachement des destinations) ; FA09 v1 du 01/10/2026 (exclusions tertiaire spécifique et industrie). Moteur lu : `ouverture.py`, `brasseurs.py`, `groupe.py`, `saisons.py`, `emission.py`, `scenarios.py`, `protections.py`, `calendrier.py`, `usages.py`, `exigences.py`, `banc/confort.py`, `tests/test_thd.py`, `tests/test_ouverture.py`.

Numérotation : les numéros d'équations et de tableaux cités sont ceux du texte consolidé de 2026. Ils sont décalés d'une unité par rapport aux commentaires du moteur sur quatre fiches :

- fiche 13.5 : le moteur cite 2544 à 2552, le texte numérote 2543 à 2551 ;
- fiche 8.32 : le moteur cite 1647 à 1662, le texte 1646 à 1666 ; `brasseurs.py` ligne 15 cite « tableau 259 » pour les paramètres de gestion manuelle et ligne 16 « tableau 258 » pour RatUs, que le texte numérote 258 (p. 998) et 257 (p. 996) ;
- fiche 8.5 : le moteur cite les tableaux 93 et 94, le texte les numérote 92 et 93 ;
- fiche 8.1 : `emission.py` lignes 24, 25 et 29 et `groupe.py` ligne 35 citent les tableaux 86, 87 et 88 pour les parts convectives en chauffage, en refroidissement et pour θvt par défaut, que le texte numérote 85 (Pem_conv_ch, p. 516), 86 (Pem_conv_fr, p. 517) et 87 (θvt par défaut, p. 518), le tableau 88 (p. 518) étant celui des poêles et inserts ; même décalage aux lignes 26 et 28 d'`emission.py`, qui citent les tableaux 83 et 85 pour θvs en chauffage et en refroidissement, numérotés 82 (p. 514) et 84 (p. 515) dans le texte.

## 1. Indicateurs d'usage transverses (fiche 4.1, tableau 4, p. 57)

Le texte définit deux indicateurs par usage de zone, que plusieurs fiches reprennent. Ils sont à coder une fois (`usages.py`) et à importer partout.

```python
# Tableau 4, p. 57 : « Indicateur d'usage habitation ou hébergement » (ihebergement)
IHEBERGEMENT = {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                15: 0, 16: 0, 17: 0, 18: 0, 19: 1, 20: 1, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0}
# Tableau 4, p. 57 : « Indicateur d'usage associé à l'enseignement » (ienseignement)
IENSEIGNEMENT = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 1, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 1, 27: 1, 28: 0}
```

Attention : le texte emploie trois périmètres différents pour « habitation » selon la fiche. Ils ne se recouvrent pas, et le moteur ne doit pas en déduire un des autres :

| Périmètre | Usages | Où il sert |
|---|---|---|
| `ihebergement = 1` (tableau 4, p. 57) | 1, 2, 8, 9, 19, 20 | brasseurs d'air la nuit (p. 1000) ; déclaré en entrée de la fiche 5.13 (p. 256) mais inutilisé dans son algorithme |
| « usage de type habitation (maison individuelle, logement collectif, établissement sanitaire avec hébergement) » (fiche 13.5, p. 1401) | 1, 2, 19 | température d'inconfort chaud la nuit, équation 2544 |
| famille « habitation, hôtellerie et hébergement » (figure 34, p. 195 et 196) | 1, 2, 8, 9, 19 | matrices conventionnelles des protections mobiles ; l'usage 20 est dans la famille « hôpitaux (24h/24) » |

## 2. Fiche 5.13 : surventilation par ouverture des baies

### 2.1 Caractère traversant au sens de la surventilation (tableau 43, p. 265 et 266)

« Le caractère traversant du groupe au sens de la surventilation par ouverture des baies est conventionnel (voir tableau 43). La seule exception est le cas d'un groupe associé à l'usage d'habitation - logement collectif. Pour ce dernier, δtrav_surv est pris égal à 1 (traversant), ou 0 (non traversant) selon le caractère (traversant ou non traversant) du groupe » (p. 265). Il est distinct du caractère traversant au sens des conditions d'hiver (tableau 22, p. 143 et 144, fiche 5.6), qui vaut 1 pour presque tous les usages.

```python
# Tableau 43, p. 265 et 266 : δtrav_surv conventionnel ; None = non conventionnel, lu sur le groupe (Delta_trav_surv)
TRAVERSANT_SURV = {1: 1, 2: None, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                   15: 0, 16: 0, 17: 1, 18: 1, 19: 0, 20: 0, 21: 0, 22: 1, 23: 1, 24: 1, 25: 1, 26: 0, 27: 0, 28: 1}
```

Conséquence pour le débit : en traversant, équations 252 à 254 (p. 269 et 270) avec Sors calculé sur deux roses des vents, `Cd_go = 0,6` et `dCp = 0,75` (nomenclature p. 259, texte p. 270), `Vvent_max = 3 m/s` (nomenclature p. 259, texte p. 271) ; en non traversant, équation 251 (p. 269). Le texte note qu'en traversant « par hypothèse, il en existe au moins 2 » orientations ouvertes (p. 269) : pour un groupe d'usage 17, 18, 22 à 25 ou 28 dont toutes les baies ouvrables sont sur une seule façade, Sors est nul et l'équation 254 retombe sur le seul tirage thermique ; le moteur le fait déjà (`ouverture.Ouvrants.debit`, somme sur `0 < x < total`).

Httf (p. 266) : 1,5 m dans le cas général ; saisi (au plus 15 m) pour les groupes d'usage 1 dont la différence d'altitude entre ouvrants dépasse 4 m pour chaque logement, et pour les groupes de locaux de grande hauteur (`Is_grandvolume`, p. 257). Aucune autre dépendance à l'usage.

### 2.2 Part des baies accessibles aux occupants, Pocc (figure 34, p. 195 et 196 ; équations 178 et 179, p. 188)

La fiche 5.13 renvoie à la fiche 5.9 pour Pocc (p. 259 : « Voir C_BAT_Gestion_protections_mobiles »). La figure 34 fixe Pocc et Pderog pour chacun des 28 usages et range les usages en six familles de matrices conventionnelles. Pour l'ouverture des baies, seul Pocc sert (équations 240 et 246) ; la part dérogeante de l'ouverture automatique est une constante propre à la fiche 5.13, `Pderog_ouv = 0,5` pour tous les usages (p. 259 et 264), distincte du Pderog des protections mobiles.

```python
# Figure 34, p. 195 et 196 : Pocc, part des baies en locaux occupés sur lesquelles un occupant peut agir (178)
P_OCC = {1: 0.5, 2: 0.7, 3: 0.5, 4: 0.7, 5: 0.7, 6: 0.7, 7: 0.7, 8: 0.8, 9: 0.8, 10: 0.8, 11: 0.8, 12: 0.7, 13: 0.9, 14: 0.9,
         15: 0.9, 16: 0.9, 17: 0.7, 18: 0.9, 19: 0.8, 20: 0.8, 21: 0.5, 22: 0.9, 23: 0.7, 24: 0.7, 25: 0.9, 26: 0.9, 27: 0.9, 28: 0.9}
# Figure 34, p. 195 et 196 : Pderog, part des baies en locaux occupés dont la gestion des PROTECTIONS MOBILES est la
# dérogation manuelle (179). Ne sert pas à l'ouverture des baies (Pderog_ouv = 0,5, p. 259).
P_DEROG = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.4, 5: 0.4, 6: 0.4, 7: 0.4, 8: 0.25, 9: 0.25, 10: 0.25, 11: 0.25, 12: 0.4, 13: 0.1,
           14: 0.1, 15: 0.1, 16: 0.1, 17: 0.1, 18: 0.0, 19: 0.25, 20: 0.25, 21: 0.25, 22: 0.0, 23: 0.1, 24: 0.1, 25: 0.0,
           26: 0.1, 27: 0.1, 28: 0.0}
# Figure 34, p. 195 et 196 : famille de matrices conventionnelles des protections mobiles (six familles)
FAMILLE_GPM = {1: "habitation", 2: "habitation", 3: "bureaux", 4: "enseignement", 5: "enseignement", 6: "bureaux",
               7: "enseignement", 8: "habitation", 9: "habitation", 10: "bureaux", 11: "bureaux", 12: "enseignement",
               13: "restauration", 14: "restauration", 15: "restauration", 16: "restauration", 17: "autre", 18: "autre",
               19: "habitation", 20: "hopitaux", 21: "bureaux", 22: "autre", 23: "autre", 24: "autre", 25: "autre",
               26: "restauration", 27: "restauration", 28: "autre"}
# Fiche 5.13, p. 259 et 264 : part des occupants dérogeant à l'ouverture automatique, tous usages
P_DEROG_OUV = 0.5
```

`FAMILLE_GPM` est donné parce que `protections.FAMILLE` ne couvre que les usages 1 à 3 et que `groupe.calculer` passe par `protections.P_OCC[usage]` pour l'ouverture (lignes 245 et 254). Les matrices des familles « enseignement », « restauration », « hôpitaux » et « autre » relèvent du thème protections mobiles, pas de celui-ci. Le texte les donne, en gestion manuelle, pour les six familles et les trois types de protection (légendes relues, images du PDF non relevées) : volets, figures 35 à 37-3 (p. 197 à 199) ; stores enroulables, figures 38 à 40-3 (p. 200 à 202) ; stores vénitiens, figures 41 à 43-3 (p. 203 et 204). Dans chaque série, « enseignement » est la figure 37, 40 ou 43, « restauration » la figure 37-1, 40-1 ou 43-1, « hôpitaux » la figure 37-2, 40-2 ou 43-2 (famille nommée « hôpitaux (24h/24) » dans la figure 34 et « hôpitaux-nuit » dans les légendes des matrices), « autres usages » la figure 37-3, 40-3 ou 43-3. En gestion automatique, le texte ne définit que deux familles (p. 205) : « habitation, hôtellerie et hébergement », figures 44 et 46, et « tertiaire » pour tous les autres usages, figures 45 et 47 (p. 205 et 206). `protections.py` ne cite que les figures 34 à 36, 38, 39, 44 et 45.

### 2.3 Ouverture en inoccupation et la nuit

Rien dans l'algorithme ne dépend de l'usage : tout passe par l'indicateur d'occupation `iocc_zone(h)` du scénario, la saison propre du groupe, l'heure légale et la classe de bruit de la baie. Règles, dans l'ordre du texte :

- Gestion manuelle (`Has_Gestion_Auto_Ouverture = 0`) : « on considère que l'occupant ferme l'ensemble des ouvrants en période d'inoccupation » (p. 260). Équation 240 (p. 260) : `Rouv = iocc . Pocc . Cpr . Mod_ext_man . Rouv_θop_man`. En inoccupation, `Cpr = 0` (p. 261).
- Gestion automatique (`= 1`) : « autorise la surventilation en période d'inoccupation, et donc la surventilation nocturne régulée » (p. 260). Équation 246 (p. 264) : part dérogée en manuel, part non dérogée `Pauto_nonderog . Mod_ext_auto . Rouv_θop_auto` ; équation 247 : `Pauto_nonderog = (1 - Pocc) + Pocc . (1 - Pderog_ouv)` en occupation, 1 en inoccupation. `Rouv_θop_auto` n'intègre pas `Δθconf_adapt` ; `Δθext_int = 2 °C` en automatique contre -3 °C en manuel (p. 259, 264).
- Modération extérieure (figure 61, équation 241, p. 261) : `θei_seuil_bas = 10 °C`, `θei_seuil_haut = 18 °C`, `Δθext_int = -3 °C`, tous usages.
- Contrainte Cpr en occupation (tableau 42, p. 261) : hors saison de chauffage, BR1 = 1 jour et nuit, BR2 et BR3 = 0,7 en journée (hlég de 7 h à 21 h) et 0,3 la nuit (hlég de 22 h à 6 h) ; en saison de chauffage (Saison = chauffage sans refroidissement), 0,3 pour toutes les classes. Tous usages.
- Hystérésis sur la température opérative (figure 62, p. 262) : énoncée « en occupation et en période journée (hleg > 7 h et hleg < 23 h) ». Seuils, équation 242 (hors saison de chauffage) : `ouv2 = θiifr+ + Δθconf_adapt - 1 °C`, `ouv1 = fer1 = ouv2 - 2`, `fer2 = ouv2 - 3` ; équation 243 (saison de chauffage) : `ouv2 = θiifr+ + Δθconf_adapt + 1 °C`, mêmes écarts. Le texte ne dit pas ce que vaut `Rouv_θop_man` aux heures d'occupation de nuit (voir points ouverts).
- Mode Th-B (p. 262 et 263) : `Rouv_θop_man = 0` en inoccupation (245) ; en période d'autorisation de refroidissement, `θop(h-1) - Δθext_int` remplacé par `min(θiifr - 1 ; θop(h-1) - Δθext_int)` et `θei_seuil_haut` par `min(θiifr - 1 ; θei_seuil_haut)` ; hors période, `Mod_ext_man = 0` (244). Tous usages.
- Groupes rafraîchis : « on ne fait pas appel à la surventilation naturelle au cours de la saison de refroidissement », exception faite du Th-B (p. 255). Tous usages.

Les seules entrées par usage sont donc `TRAVERSANT_SURV`, `P_OCC`, la consigne de refroidissement en occupation `θiifr+` (26 °C pour les 28 usages, synthèse p. 24 à 26) et les scénarios d'occupation. Les usages occupés la nuit (hlég 23 h à 6 h) d'après la matrice hebdomadaire du tableur sont 1, 2, 8, 9, 19, 20, 23 (56 h par semaine), 13 et 22 (14 h), 10 et 11 (7 h), 27 (5 h) : pour eux, l'absence de règle de nuit dans la fiche 5.13 n'est pas neutre.

## 3. Fiche 13.5 : confort d'été (mode Th-D)

### 3.1 Heures comptées dans DH et Nbh

Équation 2551 (p. 1403) : `DH = Σ max(0 ; θop(h) - θop_conf_ch_corr(h))` sur les heures telles que `Is_occ_zone(h) = 1` et `Is_conf_adapt(h) = 1`. Même condition pour `Nbh_inconf`, `+1 °C`, `+2 °C` (équations 2548 à 2550, p. 1403). Le texte ne distingue aucun usage : ce sont les heures d'occupation du scénario de la zone, pas « toutes les heures », pour les 28 usages. La période de confort adaptatif vient du climat seul (θrm(j) > 16 °C, p. 1402). Groupe climatisé : passé en non climatisé, système désactivé (p. 1399), tous usages.

### 3.2 Catégorie d'ambiance et seuils

Tableau 340 (p. 1401) : `Cat_amb = 1` pour « bâtiments à usage d'habitation » et pour « autres usages ». `Δθop_inc_C1 = 2 °C` (tableau 339, p. 1398 ; identique fiche 4.5, p. 72), `Δθop_min_max = 2 °C` (p. 1398 et 1401). Équation 2543 (p. 1401) : `θop_inc_max_C1(j) = max(θiifr+ ; 0,33 θrm(j) + 18,8 + Δθop_inc_C1)`.

```python
# Tableau 340, p. 1401 (et tableau 10, p. 91) : catégorie d'ambiance, tous usages
CAT_AMB = {u: 1 for u in range(1, 29)}
```

### 3.3 Température d'inconfort chaud la nuit : la règle de la ligne 187 de groupe.py

Texte, p. 1401 : « Pour les usages d'habitation, la température d'inconfort chaud aux heures de la nuit est donc supposée égale à la température de consigne de refroidissement en occupation normale, sans effet du confort adaptatif. Si le groupe appartient à une zone dont l'usage est de type « habitation » (maison individuelle, logement collectif, établissement sanitaire avec hébergement) : si 6 < hleg ≤ 22, `θop_conf_ch(h) = min(θiifr+ + Δθop_min_max ; θop_inc_max_C1)` ; sinon (période de sommeil), `θop_conf_ch(h) = θiifr+` » (équation 2544). « Pour les autres types d'usage : `θop_conf_ch(h) = min(θiifr+ + Δθop_min_max ; θop_inc_max_C1)` » à toute heure (équation 2545).

La version pour les autres usages est donc l'absence de règle de nuit. Le moteur applique la règle de nuit à `usage in (1, 2)` ; le texte la donne pour trois usages.

Réserve de lecture, à inscrire dans le docstring de la règle : l'équation 2544 est typographiquement brouillée dans le texte consolidé (p. 1401, la ligne de jour se lit « θop_conf_ch(h) = min(θiifr+ + Δθop_inc_max_C1 op_min_max()) », et l'équation 2545 est brouillée de la même façon). La forme `min(θiifr+ + Δθop_min_max ; θop_inc_max_C1)` retenue ci-dessus est reconstituée depuis le paragraphe « Valeur maximale » de la même page (« quel que soit l'usage, nous limiterons la température d'inconfort chaud à 2 °C au-dessus de la température de consigne de refroidissement (Δθop_min_max = 2 °C) ») et depuis l'équation 2543, qui définit `θop_inc_max_C1(j)`. La branche de nuit (« sinon (période de sommeil), θop_conf_ch(h) = θiifr+ ») est lisible telle quelle.

```python
# Fiche 13.5, équation 2544, p. 1401 : usages où la température d'inconfort chaud vaut θiifr+ hors de 6 h < hlég <= 22 h
NUIT_INCONFORT_CONSIGNE = {1: True, 2: True, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
                           11: False, 12: False, 13: False, 14: False, 15: False, 16: False, 17: False, 18: False, 19: True,
                           20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False}
```

Suite inchangée pour tous les usages : `Δθconf_adapt = max(0 ; θop_conf_ch - θiifr+)` en Th-D (équation 2546, p. 1402), `θop_conf_ch_corr = θop_conf_ch + Δθcorr_syst` (équation 2547, p. 1403, où `Δθcorr_syst` est le `Δθop_BA` des brasseurs).

### 3.4 Catégories CE1 et CE2

La fiche 13.5 ne contient pas les mots CE1 ni CE2 ; son tableau 340 ne connaît que Cat_amb. Dans l'annexe III, `Categorie_CE1_CE2gr` est un paramètre saisi au niveau du groupe (fiche 13.1, p. 1356 : « 0 ou 1 » ; fiche 8.32, p. 990 : « 1 = CE1 / 2 = CE2 ») et sert une seule fois : la fiche 13.1 cumule les surfaces de référence des groupes CE1 et CE2 de la zone, « si Usagezn = 1 ou 2 » (équation 2387, p. 1360). Les seuils DHmax par catégorie sont dans l'annexe à l'article R. 172-4 du CCH, hors annexe III (`exigences.dh_max`, ligne 93 : branches explicites pour les usages 1, 2 et 3, puis un repli de 900, 1 800 ou 2 200 °C.h selon la catégorie et le climat appliqué à tout autre usage, 4 à 28 compris, sans que ce repli ait été vérifié pour eux ; seuls `USAGES` et `BBIO_MAX_MOYEN`, lignes 15 et 16 du module, sont bornés à 1 à 5).

```python
# Catégorie CE1/CE2 : aucune attribution par usage dans l'annexe III (saisie par groupe, fiche 13.1 p. 1356)
CATEGORIE_CE = {u: "non spécifié" for u in range(1, 29)}
```

## 4. Fiche 4.6 : saisons propres

Tout l'algorithme est commun aux 28 usages : seuils `Seuil_debut = 40 °C.h` et `Seuil_fin = 2 Wh/m²` (tableau 8, p. 82 et 83) ; un seul redémarrage (équation 67, p. 85) ; chauffage autorisé les 8 premières semaines, arrêt testé du 57e au 182e jour, interdit du 183e au 252e, démarrage testé à partir du 253e (p. 85, équations 76 à 81, p. 88 et 89) ; refroidissement nul la première semaine, démarrage testé du 8e au 182e jour, autorisé du 183e au 245e, arrêt testé à partir du 246e (p. 90, équations 87 à 90, p. 92 et 93). En Th-D : chauffage interdit en période de confort adaptatif (équations 76, 77, 80), refroidissement déclenché au premier jour de confort adaptatif (équation 88, p. 93) et arrêt interdit tant que la période dure (équation 90). Tableau 11 (p. 93) pour `Saison_gr`.

Deux grandeurs dépendent de l'usage :

1. `Cat_amb`, tableaux 9 et 10 (p. 91) : 1 pour « bâtiments à usage d'habitation » et pour « autres usages », soit `Δθop_inc_C1,fr` de la fiche 4.5 (équation 61, p. 77) pour les 28 usages. `saisons.D_OP_INC_C1 = 2.0` est juste.
2. `Nbh_occ_ref`, équation 66 (p. 85) : « nombre d'heures d'occupation de référence correspondant à une semaine d'occupation type pour l'usage considéré. Il est calculé par sommation de l'ensemble des valeurs du tableau des indicateurs d'occupation de la zone par jour (1 à 7) / heure (1 à 24). Le calcul est réalisé en début de simulation. » C'est la somme de la matrice hebdomadaire `poccs(J, H)` du scénario (tableau 8, p. 82), sans le profil annuel. Il entre dans le seuil de démarrage `Seuil_debut x max(0,5 ; Nbh_occ_somme / (4 x Nbh_occ_ref))` (équations 78, 81, 88).

Valeurs de `Nbh_occ_ref` calculées depuis la matrice hebdomadaire d'occupation du tableur officiel (feuilles MI à GYM_PRI, `scenarios_officiels.json`) ; elles ne figurent pas en clair dans le texte, le moteur doit les recalculer depuis la matrice et non les figer :

```python
# Équation 66, p. 85 : somme de la matrice hebdomadaire d'occupation du tableur du 29/04/2026 (valeur dérivée, à recalculer)
NBH_OCC_REF = {1: 132, 2: 132, 3: 50, 4: 45, 5: 54, 6: 47, 7: 65, 8: 105, 9: 105, 10: 98, 11: 98, 12: 60, 13: 126, 14: 30,
               15: 77, 16: 66, 17: 90, 18: 88, 19: 168, 20: 168, 21: 66, 22: 126, 23: 168, 24: 50, 25: 88, 26: 30, 27: 65, 28: 88}
```

Défaut du moteur mis au jour : `groupe.calculer` prend `hebdo = sc.occupation[:168]` (ligne 162), c'est-à-dire la première semaine simulée, profil annuel compris. Le profil annuel d'occupation du tableur vaut 0 en semaine 1 de janvier (vacances) pour les usages 4, 5, 18, 25, 26, 27 et 28 : `Nbh_occ_ref = 0`, puis `saisons.Saisons._seuil` (ligne 66) divise par `4 x 0` et lève `ZeroDivisionError`. Pour les usages 1 à 3 et les autres, le facteur annuel vaut 1 cette semaine-là et le résultat coïncide avec l'équation 66.

Hors usage, à signaler sans le trancher ici : « dans le cas où le groupe ne dispose pas de système de refroidissement (iclim = 0), la variable `Aut_fr,pro` est nulle toute l'année » (p. 90) ; le moteur calcule une saison de refroidissement propre pour tout groupe, climatisé ou non (`groupe.py`, lignes 301 à 304).

## 5. Fiche 8.32 : brasseurs d'air

### 5.1 Conditions (p. 993 et 999)

Groupes non climatisés seulement (`Is_climatise = 0`) ; modélisés en Th-D et Th-C ; en Th-D utilisables « durant l'ensemble de la période de confort adaptatif », en Th-C « restreinte à la période de refroidissement du groupe (`Aut_fr,pro = 1`) » (p. 993) ; désactivés en inoccupation (équation 1651, p. 999) et hors de leur plage jour/nuit (équations 1652 et 1653 : jour = `6 < hlég ≤ 22`, nuit = complément). Tous usages.

### 5.2 Ratio de surface occupée par usage jour/nuit, RatUs_BA_p (tableau 257, p. 994 à 997)

```python
# Tableau 257, p. 994 à 997 : RatUs_BA_p par usage de zone, (Us = jour, Us = nuit) ; Us = 2 (jour et nuit) : RatUs = 1 (p. 996)
RAT_US = {1: (0.6, 0.4), 2: (0.54, 0.36), 3: (0.7, 0.0), 4: (0.85, 0.0), 5: (0.75, 0.0), 6: (0.75, 0.0), 7: (0.75, 0.0),
          8: (0.728, 0.728), 9: (0.728, 0.728), 10: (0.5179, 0.0), 11: (0.79, 0.0), 12: (0.728, 0.0), 13: (0.7, 0.7),
          14: (0.7, 0.0), 15: (0.7, 0.0), 16: (0.7, 0.0), 17: (0.93, 0.0), 18: (0.75, 0.0), 19: (0.6, 0.5), 20: (0.75, 0.45),
          21: (0.65, 0.0), 22: (1.0, 0.0), 23: (0.7, 0.6), 24: (0.7, 0.0), 25: (0.75, 0.0), 26: (0.7, 0.0), 27: (0.7, 0.0),
          28: (0.75, 0.0)}
```

Un brasseur d'usage nuit (`Us = 0`) dans un usage dont `RatUs` de nuit vaut 0 (par exemple 3 ou 17) viole le test de cohérence `Σ Ratbr_p < min(RatUs)` (p. 997) : « une erreur apparaît ». Le moteur rend 0 (`rat_nuit = 0`), ce qui revient au même sur le résultat ; il peut en plus refuser la saisie.

### 5.3 Paramètres de gestion manuelle (tableau 258, p. 998)

`Δop_1_br_man = 2 °C`, `Δop_2_br_man = 4 °C`, `Δop_3_br_man = 1 °C` ; « elles sont les mêmes pour tous les usages » (p. 997). Le tableau imprime une seule valeur pour `Δop_3` sur deux colonnes jour/nuit. Équations 1646 et 1648 (p. 998) : `θop_dec = θiifr+ + Δθconf_adapt + Δop_3`, `V1 = θop_dec`, `V2 = θop_dec + Δop_2`, `arr = θop_dec - Δop_1`. Hystérésis à deux paliers, équation 1654 (p. 1000). Modes automatiques (thermostat, tout automatique) : consignes saisies par l'utilisateur, pas de valeur par usage (p. 998).

### 5.4 Règle de nuit (p. 1000)

« Pour toute la durée de la période nuit, une distinction est faite en fonction du type d'usage de la zone : zones à caractère résidentiel ou d'hébergement d'une part, zones à autres usages de l'autre. En résidentiel et hébergement, on considère d'une part que la vitesse maximale du brasseur ne peut être appliquée pour des raisons acoustiques, et d'autre part, en cas de gestion manuelle, que le débit du brasseur d'air est bloqué sur la position qu'il avait à 23 h. »

Pour `Us = 0` (nuit) ou `Us = 2` (jour et nuit) : si `ihebergement = 1` et (`hlég > 22` ou `hlég ≤ 6`), `Qv(h) = min(Qv(h) ; Qv_int)` ; si gestion manuelle et (`hlég > 23` ou `hlég ≤ 6`), `Qv(h) = Qv(h - 1)`. Le critère est `ihebergement` du tableau 4, donc les usages 1, 2, 8, 9, 19 et 20, et non `usage in (1, 2)` comme à la ligne 75 de `brasseurs.py`. Le blocage sur la position de 23 h n'est pas codé (le moteur recalcule l'hystérésis chaque heure).

Réserve de lecture, à inscrire dans le docstring de la règle : le texte écrit « ihergement » (p. 1000 : « Si ihergement =1 et (h_leg(h) > 22h ou h_leg(h) ≤ 6h) »), variable absente de la nomenclature de la fiche 8.32 (tableau 256, p. 992) et de tout le reste de la fiche (p. 989 à 1002). Elle est rattachée à `ihebergement` du tableau 4 (p. 57), seul indicateur de ce nom dans l'annexe III ; le paragraphe qui précède (« zones à caractère résidentiel ou d'hébergement d'une part, zones à autres usages de l'autre », p. 1000) va dans ce sens, mais le rattachement reste une lecture, pas une lettre du texte.

```python
# Fiche 8.32, p. 1000 : usages soumis au plafond Qv_int la nuit et, en gestion manuelle, au blocage à 23 h (= IHEBERGEMENT)
BRASSEUR_NUIT_BRIDE = {u: bool(v) for u, v in IHEBERGEMENT.items()}
```

Combinaison jour/nuit, équations 1660 et 1661 (p. 1001) : `Δθop_BA_jour` et `Δθop_BA_nuit`, chacun normé par `min(RatUs)` des brasseurs de l'usage considéré ; `Δθop_BA = jour` si `6 < hlég ≤ 22`, `nuit` sinon. Vitesse : `v = 0,0032 τ` (1658), aucun effet sous 0,2 m/s, formule empirique (1659). Consommation électrique (1662 à 1666, p. 1001 et 1002), `P_int = 0,6 P_max_corr`, correctifs 1,1 / 1,2 en puissance et 0,9 / 0,8 en débit selon le statut justifié ou déclaré (p. 993) : identiques pour tous les usages, non codés en Cep (premier jet).

## 6. Relance et intermittence des émetteurs (fiches 8.5 et 8.1)

### 6.1 Durées de relance (fiche 8.5)

Calcul des consommations seulement (p. 556), pendant la saison effective de chauffage ou de refroidissement (p. 560 et 561). Durées, tableau 92 (chauffage, p. 559) : type 1 horloge 2 h / 6 h, type 2 horloge et contrôle d'ambiance 2 h / 4 h, type 3 optimiseur 1 h / linéaire entre 0 et 3 h selon θext (équation 844, p. 560, arrondi à l'entier, `θext_reg_sup = 15 °C`). Tableau 93 (refroidissement, p. 559) : type 1 1 h / 3 h, type 2 1 h / 2 h, type 3 sans horloge 0 h / 0 h, consigne de confort permanente (p. 561). La première durée vaut après une inoccupation courte (`pch(t) = 0`, moins de 48 h), la seconde après une inoccupation prolongée (`pch(t) = -1`, plus de 48 h). Algorithme 845 à 849 (p. 560 et 561). Le type de programmation est saisi par groupe (`Typepgrm_ch`, `Typepgrm_fr`, tableau 91, p. 557) : aucune valeur par usage.

Ce qui dépend de l'usage passe entièrement par les scénarios : l'indicateur de consigne `pch`, `pfr` (1 présence, 0 absence de moins de 48 h, -1 absence de plus de 48 h, p. 557) et les trois niveaux de consigne, synthèse p. 24 à 26 (colonnes « confort / réduit court / réduit long »), confirmés par le tableur :

```python
# Synthèse des scénarios, p. 24 à 26 : consignes (confort, réduit de moins de 48 h, réduit de plus de 48 h), °C
CONSIGNES_CHAUD = {1: (19, 16, 16), 2: (19, 16, 16), 3: (19, 16, 7), 4: (19, 16, 7), 5: (19, 16, 7), 6: (19, 16, 7),
                   7: (19, 16, 7), 8: (19, 16, 7), 9: (19, 16, 7), 10: (19, 16, 7), 11: (19, 16, 7), 12: (21, 18, 7),
                   13: (19, 16, 7), 14: (19, 16, 7), 15: (19, 16, 7), 16: (19, 16, 7), 17: (19, 16, 7), 18: (19, 16, 7),
                   19: (21, 18, 7), 20: (21, 18, 7), 21: (21, 18, 7), 22: (19, 16, 16), 23: (15, 7, 7), 24: (15, 7, 7),
                   25: (15, 7, 7), 26: (19, 16, 7), 27: (19, 16, 7), 28: (15, 7, 7)}
CONSIGNES_FROID = {u: (26, 30, 30) for u in range(1, 29)}
```

Le moteur lit déjà ces valeurs dans le tableur (`scenarios._consignes`) et l'indicateur `etat_ch` pour distinguer les deux absences (`emission.relance`, paramètre `etat`). D'après la matrice hebdomadaire du tableur, l'absence de plus de 48 h apparaît chaque semaine (week-end) pour les usages 3, 4, 12, 14, 24, 26 et 27, par le profil annuel (vacances) pour 1, 2, 4, 5, 6, 14, 18, 25, 26, 27 et 28, et jamais pour 7 à 11, 13, 15 à 17, 19 à 23 ; les usages 19 et 20 ont `pch = 1` en permanence, donc aucune relance. Ce sont des constats sur le tableur, pas des règles du texte.

### 6.2 Variation temporelle et arrêt de l'émission (fiche 8.1)

La fiche 8.1 ne contient aucune règle par usage. La variation temporelle `θvt` est certifiée (plancher 0,2 K pour l'effet joule, 0,4 K pour les autres émetteurs de chauffage, plafond -0,4 K en froid, p. 517), justifiée (+ 0,5 K en chaud, - 0,5 K en froid, p. 517), ou par défaut selon que le couple régulateur/émetteur permet ou non « un arrêt total de l'émission » : 2,0 K sinon, 1,8 K si oui en chauffage ; -2,0 K et -1,8 K en refroidissement (tableau 87, p. 518) ; poêles et inserts 2 K avec thermostat d'ambiance, 2,5 K en régulation manuelle (tableau 88, p. 518). Cet « arrêt total » qualifie la régulation terminale, pas une absence de 48 h. L'intermittence proprement dite est portée par les consignes réduites des scénarios (6.1) et par les saisons effectives (p. 523 et 524, fiche 8.4), qui dépendent de la génération et des groupes raccordés, pas de l'usage. La fiche d'application FA07 (variation temporelle des émetteurs électriques directs) n'a pas été relue ici : hors thème usage.

```python
# Fiche 8.1 : aucune règle de variation temporelle ou d'intermittence propre à un usage
VARIATION_TEMPORELLE_PAR_USAGE = {u: "non spécifié" for u in range(1, 29)}
```

## 7. Tables complètes, dict Python

Récapitulatif des tables ci-dessus, toutes à clé = numéro d'usage (1 à 28), prêtes à copier ; les sources sont rappelées dans les sections correspondantes.

```python
IHEBERGEMENT = {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                15: 0, 16: 0, 17: 0, 18: 0, 19: 1, 20: 1, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0}   # tableau 4, p. 57
IENSEIGNEMENT = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 1, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 1, 27: 1, 28: 0}  # tableau 4, p. 57
TRAVERSANT_SURV = {1: 1, 2: None, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                   15: 0, 16: 0, 17: 1, 18: 1, 19: 0, 20: 0, 21: 0, 22: 1, 23: 1, 24: 1, 25: 1, 26: 0, 27: 0, 28: 1}  # tableau 43, p. 265-266
P_OCC = {1: 0.5, 2: 0.7, 3: 0.5, 4: 0.7, 5: 0.7, 6: 0.7, 7: 0.7, 8: 0.8, 9: 0.8, 10: 0.8, 11: 0.8, 12: 0.7, 13: 0.9, 14: 0.9,
         15: 0.9, 16: 0.9, 17: 0.7, 18: 0.9, 19: 0.8, 20: 0.8, 21: 0.5, 22: 0.9, 23: 0.7, 24: 0.7, 25: 0.9, 26: 0.9, 27: 0.9, 28: 0.9}  # figure 34, p. 195-196
P_DEROG = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.4, 5: 0.4, 6: 0.4, 7: 0.4, 8: 0.25, 9: 0.25, 10: 0.25, 11: 0.25, 12: 0.4, 13: 0.1,
           14: 0.1, 15: 0.1, 16: 0.1, 17: 0.1, 18: 0.0, 19: 0.25, 20: 0.25, 21: 0.25, 22: 0.0, 23: 0.1, 24: 0.1, 25: 0.0,
           26: 0.1, 27: 0.1, 28: 0.0}  # figure 34, p. 195-196 (protections mobiles)
P_DEROG_OUV = 0.5  # p. 259 et 264, tous usages
FAMILLE_GPM = {1: "habitation", 2: "habitation", 3: "bureaux", 4: "enseignement", 5: "enseignement", 6: "bureaux",
               7: "enseignement", 8: "habitation", 9: "habitation", 10: "bureaux", 11: "bureaux", 12: "enseignement",
               13: "restauration", 14: "restauration", 15: "restauration", 16: "restauration", 17: "autre", 18: "autre",
               19: "habitation", 20: "hopitaux", 21: "bureaux", 22: "autre", 23: "autre", 24: "autre", 25: "autre",
               26: "restauration", 27: "restauration", 28: "autre"}  # figure 34, p. 195-196
CAT_AMB = {u: 1 for u in range(1, 29)}  # tableau 10, p. 91 ; tableau 340, p. 1401
NUIT_INCONFORT_CONSIGNE = {1: True, 2: True, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
                           11: False, 12: False, 13: False, 14: False, 15: False, 16: False, 17: False, 18: False, 19: True,
                           20: False, 21: False, 22: False, 23: False, 24: False, 25: False, 26: False, 27: False, 28: False}  # équation 2544, p. 1401
CATEGORIE_CE = {u: "non spécifié" for u in range(1, 29)}  # aucune attribution par usage dans l'annexe III
RAT_US = {1: (0.6, 0.4), 2: (0.54, 0.36), 3: (0.7, 0.0), 4: (0.85, 0.0), 5: (0.75, 0.0), 6: (0.75, 0.0), 7: (0.75, 0.0),
          8: (0.728, 0.728), 9: (0.728, 0.728), 10: (0.5179, 0.0), 11: (0.79, 0.0), 12: (0.728, 0.0), 13: (0.7, 0.7),
          14: (0.7, 0.0), 15: (0.7, 0.0), 16: (0.7, 0.0), 17: (0.93, 0.0), 18: (0.75, 0.0), 19: (0.6, 0.5), 20: (0.75, 0.45),
          21: (0.65, 0.0), 22: (1.0, 0.0), 23: (0.7, 0.6), 24: (0.7, 0.0), 25: (0.75, 0.0), 26: (0.7, 0.0), 27: (0.7, 0.0),
          28: (0.75, 0.0)}  # tableau 257, p. 994-997
BRASSEUR_NUIT_BRIDE = {u: bool(v) for u, v in IHEBERGEMENT.items()}  # p. 1000
BRASSEUR_MANUEL = {u: (2.0, 4.0, 1.0) for u in range(1, 29)}  # tableau 258, p. 998 : Δop_1, Δop_2, Δop_3, tous usages
NBH_OCC_REF = {1: 132, 2: 132, 3: 50, 4: 45, 5: 54, 6: 47, 7: 65, 8: 105, 9: 105, 10: 98, 11: 98, 12: 60, 13: 126, 14: 30,
               15: 77, 16: 66, 17: 90, 18: 88, 19: 168, 20: 168, 21: 66, 22: 126, 23: 168, 24: 50, 25: 88, 26: 30, 27: 65, 28: 88}  # équation 66, p. 85, valeur dérivée du tableur
CONSIGNES_CHAUD = {1: (19, 16, 16), 2: (19, 16, 16), 3: (19, 16, 7), 4: (19, 16, 7), 5: (19, 16, 7), 6: (19, 16, 7),
                   7: (19, 16, 7), 8: (19, 16, 7), 9: (19, 16, 7), 10: (19, 16, 7), 11: (19, 16, 7), 12: (21, 18, 7),
                   13: (19, 16, 7), 14: (19, 16, 7), 15: (19, 16, 7), 16: (19, 16, 7), 17: (19, 16, 7), 18: (19, 16, 7),
                   19: (21, 18, 7), 20: (21, 18, 7), 21: (21, 18, 7), 22: (19, 16, 16), 23: (15, 7, 7), 24: (15, 7, 7),
                   25: (15, 7, 7), 26: (19, 16, 7), 27: (19, 16, 7), 28: (15, 7, 7)}  # synthèse, p. 24-26
CONSIGNES_FROID = {u: (26, 30, 30) for u in range(1, 29)}  # synthèse, p. 24-26
RELANCE_PAR_USAGE = {u: "non spécifié" for u in range(1, 29)}  # tableaux 92-93, p. 559 : par type de programmation, pas par usage
VARIATION_TEMPORELLE_PAR_USAGE = {u: "non spécifié" for u in range(1, 29)}  # tableaux 87-88, p. 518
```

## Points ouverts

Ce que le texte ne tranche pas, ou ne tranche que par la lettre, et qui ne se mesurera qu'au banc, c'est-à-dire sur les bureaux seuls tant qu'aucun RSEE d'usage 4 à 28 n'existe :

1. **Nuit du confort d'été, usages 8, 9 et 20.** La fiche 13.5 (p. 1401) réserve la température d'inconfort de nuit égale à la consigne aux usages 1, 2 et 19, alors que le tableau 4 (p. 57) classe aussi 8, 9 et 20 en hébergement et que la fiche 8.32 (p. 1000) bride leurs brasseurs la nuit pour « période de sommeil ». Lecture retenue : la lettre de 13.5, pas de règle de nuit pour 8, 9 et 20. Aucun banc possible.
2. **Nbh_occ_ref des usages en vacances la première semaine** (4, 5, 18, 25 à 28) : le texte dit « semaine d'occupation type » (équation 66, p. 85) et non première semaine simulée ; le moteur doit sommer la matrice hebdomadaire. Mesurable sur les bureaux (aucun changement attendu : facteur annuel 1).
3. **Indicateur de consigne à 0,5** (usages 23 et 24, dernière semaine de décembre « occupée à 50 % », p. 25) : le tableur met 0,5 dans les profils annuels de chauffage et de refroidissement ; le texte ne définit l'indicateur qu'à 1, 0 et -1 (p. 557). `scenarios._consignes` (lignes 75 à 77) traite 0,5 comme -1 et applique 7 °C au lieu de 15 °C toute la semaine. Lecture à décider : consigne de confort (occupation à 50 %), ou réduit court.
4. **Hystérésis d'ouverture aux heures d'occupation de nuit** : la fiche 5.13 (p. 262) n'énonce `Rouv_θop_man` qu'en « période journée (hleg > 7 h et < 23 h) » ; `ouverture.py` l'applique à toute heure d'occupation, tranché au banc sur les usages 1 et 2. Pour 8, 9, 13, 19, 20, 22, 23 (occupés la nuit), aucun banc ; la lecture de 1 et 2 est reconduite.
5. **`ihebergement` en entrée de la fiche 5.13** (p. 256) sans emploi dans l'algorithme (p. 260 à 271) : rien n'autorise une règle d'ouverture propre aux usages d'hébergement.
6. **`Has_Gestion_Auto_Ouverture = 2`** (régulation automatique sans dérogation, p. 257, borne max 1 dans la même ligne) : l'algorithme (p. 264) ne traite que la valeur 1. `Pauto_nonderog = 1` serait la lecture naturelle ; non codée, non tranchée.
7. **Blocage des brasseurs sur la position de 23 h** en gestion manuelle et hébergement (p. 1000) : non codé ; le mode de gestion des brasseurs (`mode_gestion_br_p`) n'est pas lu par le moteur, qui suppose la gestion manuelle partout.
8. **`Δop_3_br_man` de nuit** : le tableau 258 (p. 998) n'imprime qu'une valeur (1 °C) à cheval sur les colonnes jour et nuit ; retenue pour les deux.
9. **Catégorie CE1/CE2** : saisie par groupe, cumulée seulement pour les usages 1 et 2 (équation 2387, p. 1360) ; seuils DHmax des usages 4 à 28 hors annexe III, à chercher dans l'annexe à l'article R. 172-4 (hors de cette spécification).
10. **Saison de refroidissement d'un groupe non climatisé** (p. 90, `Aut_fr,pro = 0` si `iclim = 0`) : hors thème usage, mais la règle contredit le calcul actuel du besoin de froid du Bbio pour tout groupe ; à traiter dans la spécification des saisons, avec le banc des bureaux.

## Où coder

| Règle | Fichier, ligne | Changement |
|---|---|---|
| Indicateurs `ihebergement`, `ienseignement` (tableau 4, p. 57) | `openbce/usages.py` (nouveau, après `NOMS`) | ajouter `IHEBERGEMENT`, `IENSEIGNEMENT` ; les importer dans `brasseurs.py` et `groupe.py` |
| Caractère traversant (tableau 43, p. 265-266) | `openbce/ouverture.py`, ligne 104 : `traversant = usage == 1 or groupe.entier("Delta_trav_surv", 0) == 1` | `t = TRAVERSANT_SURV[usage]` ; `traversant = (groupe.entier("Delta_trav_surv", 0) == 1) if t is None else bool(t)` ; `Delta_trav_surv` n'est lu que pour l'usage 2 |
| Pocc, Pderog, famille (figure 34, p. 195-196) | `openbce/protections.py`, lignes 16 à 18 (`P_OCC`, `P_DEROG`, `FAMILLE`) | étendre aux 28 usages ; `FAMILLE` prend les six familles ; `_matrices` (ligne 73) doit lever une erreur explicite pour les familles sans matrice relevée (enseignement, restauration, hôpitaux, autre ; matrices présentes dans le texte aux figures 37 à 43-3, p. 198 à 204, images du PDF) tant que le thème protections mobiles n'est pas spécifié |
| Pocc dans l'ouverture | `openbce/groupe.py`, lignes 245 et 254 (`protections.P_OCC[usage]`) | inchangé une fois `P_OCC` étendu |
| Température d'inconfort chaud la nuit (équation 2544, p. 1401) | `openbce/groupe.py`, ligne 187 : `if usage in (1, 2) and not 6 < heure_legale <= 22` | `if NUIT_INCONFORT_CONSIGNE[usage] and not 6 < heure_legale <= 22`, soit `usage in (1, 2, 19)` ; renuméroter les commentaires (2543 à 2551) ; docstring : équation 2544 typographiquement brouillée p. 1401, forme `min(θiifr+ + Δθop_min_max ; θop_inc_max_C1)` reconstituée depuis le paragraphe « Valeur maximale » de la même page (section 3.3) |
| Nbh_occ_ref (équation 66, p. 85) | `openbce/groupe.py`, lignes 162 et 163 : `hebdo = sc.occupation[:168]` ; `saisons.Saisons(float(hebdo.sum()), ...)` | passer la somme de la matrice hebdomadaire du tableur : ajouter dans `scenarios.py` une fonction `heures_occupation_semaine_type(usage)` qui renvoie `sum(sum(ligne) for ligne in _tableau(usage, "occupation")["hebdo"])`, et l'appeler ici ; `saisons.Saisons.__init__` (ligne 38) refuse `heures_occupation_reference <= 0` |
| Seuil de démarrage | `openbce/saisons.py`, ligne 66 (`_seuil`) | inchangé après correction ci-dessus ; commentaire ligne 27 (`D_OP_INC_C1`) : citer tableau 10, p. 91, et tableau 340, p. 1401 |
| RatUs des brasseurs (tableau 257, p. 994-997) | `openbce/brasseurs.py`, ligne 16 (`RAT_US`, usages 1 à 5) et ligne 92 (`RAT_US.get(usage, (0.7, 0.0))`) | table des 28 usages ; supprimer le défaut `(0.7, 0.0)`, qui est une vraisemblance ; commentaires : ligne 16 « tableau 258 » devient « tableau 257 » (p. 996), ligne 15 (`D_OP_1, D_OP_2, D_OP_3`) « tableau 259 » devient « tableau 258 » (p. 998) |
| Nuit des brasseurs en hébergement (p. 1000) | `openbce/brasseurs.py`, lignes 75 et 76 : `if usage in (1, 2) and nuit: t.debit = min(t.debit, t.q_int)` | `if IHEBERGEMENT[usage] and nuit and t.usage in (0, 2)` ; ajouter, en gestion manuelle, le gel `t.debit = debit_precedent` pour `heure_legale > 23 or heure_legale <= 6` (lire `mode_gestion_br_p` si le RSEE le porte, sinon rester en manuel et le dire dans le docstring) ; renuméroter les commentaires (1646 à 1666) ; docstring : le texte écrit « ihergement » p. 1000, variable absente de la nomenclature 8.32 (tableau 256, p. 992), rattachée à `ihebergement` du tableau 4 (p. 57) par lecture (section 5.4) |
| Th-D et Th-C des brasseurs (p. 993) | `openbce/brasseurs.py`, ligne 55 (`froid_autorise`) et `groupe.py`, lignes 177-178 et 325 | inchangé : en Th-D `automate.refroidissement` est forcé à vrai en confort adaptatif, ce qui couvre « l'ensemble de la période de confort adaptatif » |
| Heures comptées dans DH (équation 2551, p. 1403) | `openbce/groupe.py`, lignes 327 à 331 (`if occupe and adaptatif`) | inchangé pour les 28 usages |
| Durées de relance (tableaux 92-93, p. 559) | `openbce/emission.py`, lignes 34-35 (`RELANCE_CHAUD`, `RELANCE_FROID`) et 108 (`relance`) | inchangé ; corriger les commentaires (« tableaux 93, 94 » devient « tableaux 92, 93 », équations 844 à 848) |
| Numérotation des tableaux de la fiche 8.1 | `openbce/emission.py`, lignes 24, 25, 26, 28 et 29 (`PEM_CHAUD`, `PEM_FROID`, `VS_CHAUD`, `VS_FROID`, `VT_DEFAUT_CHAUD`) ; `openbce/groupe.py`, ligne 35 (commentaire « tableau 88 » pour θvt par défaut) | commentaires seulement : « tableau 86 » devient « tableau 85 » (Pem_conv_ch, p. 516), « 87 » devient « 86 » (Pem_conv_fr, p. 517), « 83 » devient « 82 » (θvs chauffage, p. 514), « 85 » devient « 84 » (θvs refroidissement, p. 515), « 88 » devient « 87 » (θvt par défaut, p. 518) dans les deux fichiers ; le tableau 88 du texte (p. 518) est celui des poêles et inserts |
| Indicateur de consigne à 0,5 (usages 23, 24) | `openbce/scenarios.py`, lignes 75 à 77 (`_consignes`, `np.select`) | décider la lecture (point ouvert 3) ; au minimum, traiter `0 < etat < 1` comme 1 plutôt que comme -1, et le documenter comme lecture non tranchée |
| Catégorie CE1/CE2 | `openbce/exigences.py`, ligne 93 (`dh_max` : branches explicites 1, 2 et 3, puis repli 900 / 1 800 / 2 200 °C.h selon catégorie et climat pour tout autre usage) ; lignes 15 et 16 (`USAGES`, `BBIO_MAX_MOYEN`, bornés à 1 à 5) | rien dans l'annexe III ; le repli de `dh_max` s'applique déjà aux usages 4 à 28 sans avoir été vérifié contre l'annexe à l'article R. 172-4 : renvoi à la spécification des exigences |
| Avertissement « usage non validé » | `openbce/usages.py`, ligne 42 (`VALIDES = frozenset({1, 2, 3})`) | inchangé : aucun des points ci-dessus n'est validé pour 4 à 28 |
