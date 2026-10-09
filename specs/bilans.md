# Spécification : Sorties Th-C, bilans, postes forfaitaires, Cep et Cep_max

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

FAMILLE : sorties du mode Th-C, bilans d'énergie consommée, produite et importée, postes forfaitaires (refroidissement fictif, déplacements, mobilier, parkings), Cef, Cep, Cep,nr. Fiches lues en entier : 13.2 (pages 1329 à 1342), 13.3 (1343 à 1348), 13.4 (1349 à 1358), 4.7 (89 et 90), 10.1 (1261 à 1273), 10.3 (1283 à 1290), 10.4 (1291 à 1298), 13.6 (1367 à 1369). Modules OpenBCE lus : README, groupe.py, emission.py, ventilation.py, consommation.py, rsee.py, ascenseurs.py, parkings.py, banc/cep.py. RSEE lus : rsee_a.xml (logement collectif, 2 bâtiments, 4 zones, 4 groupes tous Is_Climatise = 1, un ascenseur, un parking intérieur habitat) et rsee_b.xml (bureaux, 1 zone, 1 groupe Is_Climatise = 0, sans ascenseur ni parking).

CE QUE COUVRE LA FAMILLE
1. Le bilan horaire du groupe (13.4) : matrice Qcef[poste ; énergie] (postes 1 chauffage, 2 refroidissement, 3 ECS ; énergies 10 gaz, 20 fioul, 30 charbon, 40 bois, 50 électricité, 60 réseau) par somme des générations reliées au groupe ; vecteur Welec_cons[poste] du groupe pour ch, fr, ecs, ecl, auxvent, auxdist ; besoins Qreq_ch, Qreq_fr aux bornes des émetteurs et Qreq_gen_ch, Qreq_gen_fr en entrée des générations.
2. Le bilan de la zone : somme des groupes, plus parkings (éclairage dans ecl, ventilation dans auxvent), plus éclairage des parties communes (ecl), plus poste déplacement (ascenseurs, escalators), plus usages mobiliers hors périmètre RE2020.
3. Le bilan du bâtiment : somme des zones ; production d'électricité locale (PV intégré, PV de parcelle au prorata des consommations horaires tous usages, cogénération) ; autoconsommation Eelec_prod_AC = min(production, consommation tous usages mobilier compris) ; taux TAC et TAP horaires ; énergie importée par poste Welec_IMP = Welec_cons x (1 - TAP) au bâtiment et dans chaque zone ; taux d'autoconsommation global de la cogénération.
4. Les sorties (13.2) : surfaces de référence (SHAB en usages 1 et 2, SU sinon), sorties mensuelles et annuelles du groupe (énergie consommée), de la zone et du bâtiment (énergie importée, et consommée pour l'électricité), coefficients CoefEP et CoefEPnr (tableau 337 : électricité 2,3 et 2,3 ; bois 1 et 0 ; réseau de chaleur 1 et 1 - RatENR_rdch ; réseau de froid 1 et 1 ; fossiles 1 et 1), Cef, Cep, Cep,nr, besoins annuels, sous-décomposition bois (bûche, plaquette, granulés ; poêle ou chaudière), productions, taux d'autoconsommation, électricité exportée.
5. Le forfait de refroidissement des groupes non climatisés (13.3) : ajouté en post-traitement aux cumuls annuels Fr, élec et Fr_élec, aux trois niveaux, pondéré par les surfaces.
6. Les postes forfaitaires annexes : usages mobiliers (4.7, égal aux apports internes hors occupants), ascenseurs (10.1), ventilation des parkings fermés (10.3), éclairage des parkings (10.4).
7. L'indicateur Cep par occupant (13.6).

Le texte dit explicitement que les calculs de 13.2 « consistent à sommer ou cumuler les données de sortie du calcul mené au pas de temps horaire » (page 1335) : la famille est une couche d'agrégation, sans modèle physique propre hormis les quatre postes forfaitaires.

HORS CHAMP ET POURQUOI
- Les matrices Qcef[poste ; énergie]_gen,gr et Qef_prelec (électricité produite par cogénération) sont des ENTRÉES fournies par la fiche C_GEN (chapitre 8, générateurs 8.18 à 8.23, assemblage génération) : hors de ce lot, qui ne fait que les sommer (2498).
- Les consommations d'auxiliaires de distribution (W_aux dp-e, dp, ds, dCTA, équation 2506), les ventilateurs locaux des émetteurs (W_vent-loc-tot) et les brasseurs d'air (W_abs-GA, fiche 8.32) sont des entrées venant des fiches distribution et émission ; seul le cumul est ici.
- Les ventilateurs des centrales (W_ventmoy, fiche 6.5) existent déjà dans consommation.puissance_ventilateurs.
- La production photovoltaïque Pond_PV(h) (fiche PV, chapitre 12) et la cogénération (Is_cogeneration, Cef_comb) : les deux RSEE lus n'ont ni PV ni cogénération (sorties toutes nulles) ; les équations 2524 à 2542 sont spécifiées mais ne pourront être bancées sur ces fichiers.
- Les escalators (fiche 10.2, page 1274 et suivantes) : non listés dans le lot ; W_cef_escalators est traité comme une entrée nulle en l'absence d'objet Escalator (aucun dans les deux RSEE).
- L'éclairage des parties communes des logements collectifs (fiche 7.2, page 483, W_cef_ecl_parties_communes) : non listé dans le lot ; entrée à fournir par le lot éclairage.
- Cep_max et Cep,nr_max (sorties O_Cep_Max, O_Cep_nr_Max, modulations O_Mcgeo, O_Mccombles, O_Mcsurf_moy, O_Mcsurf_tot, O_Mccat, O_ProdRef, O_BilanBEPOS_max_1 à 4, O_McbilanBEPOS_1 à 3, O_Bilan_BEPOS_annuel_niv_1_2 et niv_3_4) : ils ne sont PAS dans l'annexe III (seules les fiches d'application 4.2 et 4.3 mentionnent « Cepmax » comme pondéré par les SRT des zones). Ils relèvent du corps de l'arrêté (articles et annexes I et II). Nommés ici pour mémoire dans sorties_rsee, non spécifiés.
- Le seuil haut de degrés-heures (O_NbDegresHeures_max : 1 400 à 1 485,6 en logement collectif, 1 150 en bureaux dans les RSEE lus) est un paramètre d'entrée de 13.3 fixé par l'arrêté, non calculé ici ; pour un banc, le lire dans Sortie_Groupe_D.
- Les DH par groupe (O_NbDegresHeures) viennent du mode Th-D déjà codé (Besoins.dh, équation 2552) ; ce lot les consomme.

NOMENCLATURE RELEVÉE DANS LES RSEE ET REPRODUCTIBILITÉ
Sortie_Groupe_C : O_SREF, O_SHAB, O_SU, O_Cef_annuel, O_Cep_annuel, O_Cef_[ch|fr|ecs|ecl]_annuel, O_Cef_aux_ventilateur_annuel, O_Cef_aux_distribution_annuel, O_Cef_[ch|fr|ecs]_[gaz|fioul|bois|reseau|elec]_annuel (fr absent pour fioul et bois), O_Cef_ecl_elec_annuel, O_Cef_auxv_elec_annuel, O_Cef_auxs_elec_annuel, O_Cef_[gaz|fioul|bois|elec|reseau]_annuel, O_B_[Ch|Fr|Ecs|Ecl]_annuel, O_Cef_[ch|fr|ecs|ecl]_mois, O_Cef_aux_ventilateur_mois, O_Cef_aux_distribution_mois, O_B_[Ch|Fr|Ecs|Ecl]_mois (douze Sortie_Mensuelle avec Mois et Valeur), plus les champs Cep_max hors champ.
Sortie_Zone_C : O_SREF, O_SHAB, O_SU, Usage, Nocc, O_Cef_annuel, O_Cep_annuel, O_Cep_nr_annuel, O_Cef_imp_[ch|fr|ecs|ecl|auxvent|auxdist|deplacement|mobilier]_annuel, O_Cef_[gaz|fioul|bois|elec|reseau]_imp_annuel, O_Cef_[gaz|fioul|bois|reseau]_imp_[ch|fr|ecs]_annuel, O_Cef_bois[gran|buch|plaq][chaud|poel]_imp_[ch|ecs]_annuel, O_Cef_elec_cons_[poste]_annuel, O_Cef_elec_imp_[poste]_annuel, O_Eef_Prod_PV_annuel, O_Eef_Prod_PV_AC_annuel, O_Eef_Prod_Coge_annuel, O_Eef_Prod_Coge_AC_annuel, O_TAC_elec_annuel, O_TAC_elec_PV_annuel, O_TAC_elec_Coge_annuel, O_Eef_Elec_Exportee_annuel, séries mensuelles O_Cef_[energie]_imp_[poste]_mois, O_Cef_elec_cons_[poste]_mois, O_Eef_Prod_*_mois, O_B_[Ch|Fr|Ecs]_annuel et _mois, O_E_Sol_zone, O_E_ef_aux_zone.
Sortie_Batiment_C : mêmes familles qu'en zone avec en plus O_Cep_annuel_occ, O_Type_Reseau, O_RatENR_rdch, vecteur_energie_principal_[ch|ecs|fr], generateur_principal_[ch|ecs|fr], O_Cef_elec_AC_[poste]_annuel (au lieu de elec_cons), O_TAC_Global_coge_annuel, O_Eelec_Exportee_ef_mois (nom différent de la zone), O_Cef_Ch_comb_bat, O_Cef_ECS_comb_bat, O_E_Sol_bat, O_E_ef_aux_bat.
Attention : l'ordre des segments des noms XML diffère du texte : le texte écrit O_Cef_imp_[poste]_[energie]_annuel, le RSEE écrit O_Cef_[energie]_imp_[poste]_annuel ; au groupe le texte écrit O_Cef_[poste]_[energie]_annuel et le RSEE suit cet ordre (O_Cef_ch_elec_annuel) mais abrège auxvent en auxv et auxdist en auxs.

Reproductibles sans systèmes complexes (avec les modules existants : groupe Th-C, ventilateurs, éclairage, ascenseurs, parkings, scénarios) : O_SREF, O_SHAB, O_SU ; O_B_Ch, O_B_Fr, O_B_Ecl (annuel et mois) à tous niveaux ; O_B_Ecs (ecs.py, +0,35 %) ; O_Cef_ecl_annuel, O_Cef_ecl_elec_annuel, O_Cef_ecl_mois (logement et bureaux saisis) ; O_Cef_aux_ventilateur_annuel et _mois (simple flux résidentiel) ; O_Cef_imp_deplacement_annuel et O_Cef_elec_imp_deplacement_mois (ascenseurs + parkings) ; O_Cef_imp_mobilier_annuel et O_Cef_elec_cons_mobilier_mois (scénarios) ; O_Cep_annuel_occ dès que O_Cep_annuel est connu (vérifié : 51,2 x 731,2 / 33 = 1 134 contre 1 133,8 ; 62,2 x 241,2 / 19 = 790 contre 790,3) ; les agrégations Cef, Cep, Cep,nr elles-mêmes (vérifié : 16,6 x 2,3 = 38,2 ; 22,2 x 2,3 = 51,1 contre 51,2 ; zone 21,3 = groupe 16,6 + déplacement 4,6 ; mobilier 24,8 bien exclu). Les postes ch, fr, ecs, auxdist et le forfait de refroidissement exigent le chapitre 8 et 9 (générations), sauf le forfait 13.3 lui-même qui ne demande que les DH du Th-D. Dans un bâtiment tout électrique sans PV, TAP = 0, donc imp = cons : les deux RSEE lus sont dans ce cas, ce qui rend les sorties zone et bâtiment égales aux sommes des groupes plus postes forfaitaires.

## Entrées (RSEE)

- `Entree_Projet/Simu` / `Avec_Clim_Fictive` : Activation de la procédure forfait de refroidissement (13.3, conditions page 1343) ; nom non cité dans le texte, déduit ; entier 0/1 ; valeurs vues : 1 dans les deux RSEE
- `Entree_Projet/Simu` / `Mode` : Simu.Mode (13.3 tableau 338 : 0 Th-B, 4 Th-D, 5 Th-DBC ; la valeur 3 n'y figure pas) ; entier ; valeurs vues : 3 dans les deux RSEE
- `Entree_Projet/Simu` / `Departement` : département, zone climatique (tableau 340) ; entier ; valeurs vues : 6 ; 83
- `Entree_Projet/Simu` / `Altitude` : Alt (tableau 340 : 0 à 400, 400 à 800, 800 et plus) ; réel m ; valeurs vues : 0
- `Batiment` / `Type_Reseau` : O_Type_Reseau_bat ; entier ; valeurs vues : 0
- `Batiment` / `RatENR_rdch` : RatENR_rdch_bat (tableau 337, CoefEPnr réseau chaleur = 1 - RatENR_rdch) ; réel 0 à 1 ; valeurs vues : 0
- `Batiment` / `RatENR_rdfr` : O_RatENR_rdfr_bat (tableau 337 donne pourtant CoefEPnr réseau froid = 1 : point ouvert) ; réel 0 à 1 ; valeurs vues : absent des deux RSEE
- `Zone` / `Usage` : Usage_zn (2413, 2414 ; tableaux 311, 322, 325, 339) ; entier ; valeurs vues : 2 ; 3
- `Zone` / `Nocc` : Nocc_zn (2553, 2554) ; aussi NB_z candidat de (2281), mais le banc existant retient les adultes équivalents ; réel ; valeurs vues : 21, 12, 12, 35 (logements) ; 19 (bureaux)
- `Zone` / `NB_logement` : nombre de logements (adultes équivalents, scénarios) ; entier ; valeurs vues : 7, 4, 4, 13 ; 1
- `Groupe` / `SHAB` : SHAB_gr, SREF_gr si usage 1 ou 2 (2413) ; réel m² ; valeurs vues : 410,27 ; 320,97 ; 171,56 ; 774,76 ; 0
- `Groupe` / `SU` : SU_gr, SREF_gr sinon (2414) ; réel m² ; valeurs vues : 0 ; 241,242
- `Groupe` / `Is_Climatise` : Groupe_is_climatisé (13.3, page 1347) ; entier 0/1 ; valeurs vues : 1 (4 groupes logement) ; 0 (bureaux)
- `Sortie_Groupe_D (sortie, lue par le banc)` / `O_NbDegresHeures` : DH_g (2494) ; OpenBCE le calcule : Besoins.dh (2552) ; réel °C.h ; valeurs vues : 1153,6 ; 735,3 ; 1236 ; 1039,6 ; 15,3
- `Sortie_Groupe_D (sortie, lue par le banc)` / `O_NbDegresHeures_max` : Seuil haut (13.3), fixé par l'arrêté, hors annexe III ; réel °C.h ; valeurs vues : 1407 ; 1400 ; 1485,6 ; 1402 ; 1150
- `Batiment/Ascenseur` / `H, Netage, C, Q, V, TechMac, Cp, ScVeille, Pti, dP1, T1, dP2, T2` : H, netage, C(i,z), Q, V, TechMac, Cp, ScVeille, Pti, dP1, T1, dP2, T2 (tableau 310) ; réels, entiers, C = liste d'Index de zones séparés par des espaces ; valeurs vues : H 7,5 ; Netage 3 ; C « 1 2 » ; Q 500 ; V 1 ; TechMac 0 ; Cp 0,5 ; ScVeille 0 ; Pti 1000 ; dP1 50 ; T1 100 ; dP2 500 ; T2 100 (ignorés car ScVeille = 0)
- `Entree_Projet/Parking (niveau projet)` / `Net, Npl, Type_Parking, Type_Usage, IsParamEclHdDefaut, Type_PlagDse, PlagDse, Type_PlagDwe, PlagDwe, Ex, IsParamEclPuisDefaut, Pec_ins, Vent, IsParamVentilationDefaut, Dvent1, Dvent2, Pvent1, Pvent2, IsParamVentilationHabDefaut, Pvent600, Reg` : Net, Npl, Type, Typeusage, PlagDse_j, PlagDwe_j, Ex, Pecins, Vent, IsParamVentilationDefaut, Dvent1, Dvent2, Pvent1, Pvent2, Pvent600, Reg (tableaux 323 et 326) ; entiers, réels ; Pec_ins en kW ; PlagDse « début fin » en heures légales ; valeurs vues : Net 1 ; Npl 58 ; Type_Parking 0 (intérieur) ; Type_Usage 2 (habitat) ; PlagDse « 0 24 » ; Ex 1 ; Pec_ins 1,74 ; Vent 0 ; Pvent600 150 ; Reg 1
- `Scénarios conventionnels (chapitre 15, scenarios.py)` / `apports de chaleur hors occupants (Qmax_proc_loc, tach, tsch), Aloc` : Cef_us_mob_loc(h) = Aloc x Qmax_proc x tach x tsch (93) ; séries horaires W ; valeurs vues : Scenario.apports_usages
- `Sortie_Groupe_C / Sortie_Zone_C / Sortie_Batiment_C` / `Sortie_Mensuelle/Mois, Sortie_Mensuelle/Valeur` : O_*_mois ; lu par Noeud.mensuel() ; 12 couples (entier, réel) ; valeurs vues : séries mensuelles de toutes les sorties _mois

## Paramètres conventionnels

- CoefEP électricité = 2,3 (p. 1335 (tableau 337) et 1346 (tableau 338))
- CoefEPnr électricité = 2,3 (p. 1335)
- CoefEP et CoefEPnr bois = 1 et 0 (p. 1335)
- CoefEP et CoefEPnr réseau urbain chauffage = 1 et 1 - RatENR_rdch_bat (p. 1335)
- CoefEP et CoefEPnr réseau urbain froid = 1 et 1 (p. 1335)
- CoefEP et CoefEPnr énergies fossiles (gaz, fioul, charbon) = 1 et 1 (p. 1335)
- Codes énergie de la matrice Qcef = 10 gaz, 20 fioul, 30 charbon, 40 bois, 50 électricité, 60 réseau de chaleur ; postes 1 chauffage, 2 refroidissement, 3 ECS (p. 1352 (tableau 342))
- Seuil bas DH (forfait refroidissement) = 350 °C.h (p. 1346)
- Coef_kWh_fr_par_DH = maison individuelle 0,011 ; logement collectif 0,011 ; bureaux 0,009 ; enseignement primaire ou secondaire jour 0,016 kWhep/m²/an/(°C.h) (p. 1347 (tableau 339))
- Coef_zone_clim_et_alt (altitude 0 à 400 / 400 à 800 / 800 et plus) = H1a 0,8 0,6 0,4 ; H1b 1 0,8 0,6 ; H1c 1 0,8 0,6 ; H2a 0,7 0,5 0,3 ; H2b 1 0,8 0,6 ; H2c 1,1 0,9 0,7 ; H2d 1,2 1 0,8 ; H3 1,2 1 0,8 (p. 1347 (tableau 340))
- Borne nomenclature Cef_fr_elec_refroidissement = 0 à 97,2 kWhef/m²/an (p. 1346)
- Ascenseurs : g, Eporte, deco, Mpass, Pveilleporte, Cf, Cor_Ch, Cor_Emobcab = 9,81 m/s² ; 1188 J ; 1,2 ; 75 kg (le tableau 310 page 1264 imprime 120, le texte page 1266 dit 75) ; 13 W (le tableau 310 page 1265 imprime 75, le texte page 1266 dit 13) ; 0,45 m/s² ; 1,1 ; 0,9 (p. 1266)
- Tempec (temporisation éclairage cabine) = 120 s page 1266 (13 s dans le tableau 310 page 1264) ; non utilisée dans les équations (p. 1266)
- Bv(k) voyages par personne et par an = logement collectif 1600 ; bureaux 1700 ; enseignement primaire 800 ; enseignement secondaire jour 1200 ; maison individuelle absente (p. 1266 (tableau 311))
- Rg(TechMac) = 0,6 ; 0,8 ; 0,29 ; 0,6 pour TechMac 0, 1, 2, 3 (p. 1267 (tableau 312))
- Ac(V) = 0,5 si V <= 1 ; 0,8 si 1 < V <= 2 ; 1,2 si 2 < V <= 2,5 (identique électrique et hydraulique) (p. 1267 (tableau 313))
- alpha(TechMac) coefficient d'inertie = 6 ; 0 ; 0 ; 6 (p. 1267 (tableau 314))
- Cp(TechMac) par défaut = 0,5 ; 0,5 ; -1,2 (obligatoire si hydraulique) ; 0,5 (p. 1267 (tableau 315))
- Pec(Q) éclairage cabine = 140 W si Q <= 630 ; 210 W si 630 < Q <= 1275 ; 280 W au-delà (p. 1268 (tableau 316))
- Puissances d'auxiliaires cabine immobile = Pman 75 ; Pboutonpal 0 ; Pindpal 2 ; Pindcab 5 ; Pfrein 0 ; Palarm 10 W (p. 1268 (tableau 317))
- Spectre de charge S(direction, X) = X = 1 : 0 ; 0,75 : 0,1 ; 0,5 : 0,1 ; 0,25 : 0,3 ; 0 : 0,5 ; identique haut et bas ; somme X.S = 0,2 (2285) (p. 1268 et 1269 (tableau 318))
- Ascenseurs : valeurs par défaut de veille = dP1 = 0 W ; T1 = 86 400 s ; dP2 = 0 W ; T2 = 86 400 s (p. 1269 (2276 à 2279))
- Durées d'immobilité nocturne = habitation 8 x 365 x 3600 s ; autres (12 x 365 + 52 x 48 + 9 x 24) x 3600 s (p. 1271 (2295, 2296))
- Parkings ventilation : Effvent, CCOlim, ProdCOveh, Rutil, Dfix, Vmoy, Rl, Spl = 0,5 ; 5e-5 m³CO/m³ ; 0,35 m³CO/h ; 1 ; 0,01 h ; 10 000 m/h ; 2 ; 12 m² (p. 1286 (tableau 323))
- Parkings ventilation : défauts = Dvent2 = 900 Npl m³/h ; Dvent1 = 450 Npl ; Pvent2 = 40 Npl W ; Pvent1 = 5 Npl W ; Pvent600 = 40 W/place (p. 1288 (2327))
- Rmvtpl(h) mouvements par place selon l'heure légale de fin de pas = nul de 0 à 8 h ; bureaux 0,308 (9 à 11 h), 0,154, 0, 0,154, 0,154, 0, 0,308, 0,308 ; habitation 0,19, 0,095, 0,19, 0,095 ; commerce 0,278, 0,556, 0,278 (cellules fusionnées, lecture de parkings.py RMVTPL à conserver) (p. 1288 (tableau 324, image))
- Places de parking = deux-roues motorisé 0,33 place arrondi à l'entier supérieur ; deux-roues non motorisé 0 ; autre 1 ; Npl réel admis (p. 1287 et 1295)
- Passerelle usage zone vers Typeusage parking = usages 1 et 2 : habitat ; usages 3 à 6 : bureaux (p. 1284 (tableau 322) et 1291 (tableau 325))
- Parkings éclairage : Fhint, TauDet = 1 ; 0,2 (abattement 80 % en détection) (p. 1295 (2348, 2349))
- Fhext(h) par heure légale 1 à 24 = 1, 1, 1, 1, 1, 1, 0,79, 0,48, 0,15, 0, 0, 0, 0, 0, 0, 0, 0,03, 0,2, 0,36, 0,5, 0,65, 0,84, 1, 1 (p. 1295 (tableau 327))
- Plages d'ouverture par défaut des parkings = habitat 0 à 23 h semaine et week-end ; bureau 9 à 18 h semaine, jamais le week-end ; commerce 7 à 21 h semaine et samedi, fermé le dimanche ; NbjO = 1 tous les jours ; détection PlagDse = PlagDwe = {0 ; 0} (p. 1296)
- Puissance d'éclairage de parking par défaut = intérieur 75 W par place ; extérieur 8 W par place (p. 1296 (2350, 2351))
- Occupants pour Cep par occupant = résidentiel : nombre de pièces principales (1 à 7 occupants pour 1 à 7 pièces) saisi dans Nocc de la zone ; tertiaire : scénarios conventionnels ; enseignement : effectif programmé (p. 1368 (tableau 346))

## Équations

- (2413, p. 1335) SREF_gr = SHAB_gr ; SHAB_gr ; Usage_gr = 1 ou 2
- (2414, p. 1335) SREF_gr = SU_gr ; SU_gr ; autres usages
- (2415, p. 1335) SREF_zn = somme_{gr in zn} SREF_gr ;  ; 
- (2416, p. 1335) SREF_bat = somme_{zn in bat} SREF_zn ;  ; 
- (2417, p. 1335) O_Cef_[poste]_mois (gr) = somme_{h in mois} somme_{energie} Qcef[poste;energie]_gr(h) / SREF_gr ; Wh vers kWh/m² (diviser par 1000 implicite) ; postes ch, fr, ecs ; niveau groupe
- (2418, p. 1336) O_Cef_[poste]_mois (gr) = somme_{h in mois} Welec_cons[poste]_gr(h) / SREF_gr ;  ; postes ecl, auxvent, auxdist (électricité seule)
- (2419, p. 1336) O_B_Ch_mois (gr) = somme_{h in mois} Qreq_ch_gr(h) / SREF_gr ; Qreq_ch_gr (2499) ; 
- (2420, p. 1336) O_B_Fr_mois (gr) = somme_{h in mois} Qreq_fr_gr(h) / SREF_gr ;  ; 
- (2421, p. 1336) O_B_Ecs_mois (gr) = somme_{h in mois} Qw_brut_gr(h) / SREF_gr ; besoins ECS bruts (ecs.py, 1695) ; 
- (2422, p. 1336) O_Cef_[poste]_[energie]_annuel (gr) = somme_h Qcef[poste;energie]_gr(h) / SREF_gr ;  ; postes ch, fr, ecs
- (2423, p. 1336) O_Cef_[poste]_elec_annuel (gr) = somme_h Welec_cons[poste]_gr(h) / SREF_gr ;  ; postes ecl, auxvent, auxdist
- (2424, p. 1336) O_Cef_[poste]_annuel (gr) = somme_mois O_Cef_[poste]_mois ;  ; 
- (2425, p. 1336) O_Cef_[energie]_annuel (gr) = somme_poste O_Cef_[poste]_[energie]_annuel ;  ; 
- (2426, p. 1336) O_Cef_annuel (gr) = somme_energie O_Cef_[energie]_annuel ;  ; hors mobilier et déplacement, non définis au groupe
- (2427, p. 1336) O_Cep_annuel (gr) = somme_energie O_Cef_[energie]_annuel x CoefEP[energie] ; tableau 337 ; 
- (2428 à 2430, p. 1336) O_B_Ch_annuel = somme_mois O_B_Ch_mois ; idem Fr, Ecs ;  ; groupe
- (2431, p. 1337) O_Cef_imp_[poste]_[energie]_mois (zn) = somme_{h in mois} Qcef[poste;energie]_zn(h) / SREF_zn ;  ; postes ch, fr, ecs, énergies hors électricité
- (2432, p. 1337) O_Cef_imp_[poste]_elec_mois (zn) = somme_{h in mois} Welec_imp[poste]_zn(h) / SREF_zn ; Welec_imp (2537) ; tous postes, électricité
- (2433, p. 1337) O_Cef_cons_[poste]_elec_mois (zn) = somme_{h in mois} Welec_cons[poste]_zn(h) / SREF_zn ;  ; tous postes, électricité
- (2434 à 2437, p. 1337) O_Eef_prod_PV_mois, O_Eef_prod_coge_mois, O_Eef_prod_PV_AC_mois, O_Eef_prod_coge_AC_mois (zn) = somme_{h in mois} E correspondant_zn(h) / SREF_zn ; E_elec_prod_PV_zn, E_elec_prod_coge_zn, E_elec_prod_PV_AC_zn, E_elec_prod_coge_AC_zn ; 
- (2438, p. 1337) O_Eef_Elec_Exportee_mois = O_Eef_prod_PV_mois + O_Eef_prod_coge_mois - O_Eef_prod_PV_AC_mois - O_Eef_prod_coge_AC_mois ;  ; zone
- (2439 à 2441, p. 1337) O_B_Ch_mois (zn) = somme_{gr in zn} O_B_Ch_mois_gr x SREF_gr / SREF_zn ; idem Fr, Ecs ;  ; 
- (2442, p. 1338) O_Cef_imp_[poste]_[energie]_annuel (zn) = somme_mois O_Cef_imp_[poste]_[energie]_mois ;  ; hors électricité
- (2443, p. 1338) O_Cef_imp_[poste]_elec_annuel (zn) = somme_mois O_Cef_imp_[poste]_elec_mois ;  ; 
- (2444, p. 1338) O_Cef_cons_[poste]_elec_annuel (zn) = somme_mois O_Cef_cons_[poste]_elec_mois ;  ; 
- (2445, p. 1338) O_Cef_imp_ch_boisbuchpoel_annuel = somme_{gnr -> zn} Qcef[ch;bois]_gnr(h) sommé sur h ; O_Cef_imp_ecs_boisbuchpoel_annuel = somme Qcef[ecs;bois]_gnr(h) ; pour chaque combinaison (poêle ou chaudière) x (bûche, plaquette, granulés) x (ch, ecs) ; Is_Generateur_Poele_gnr, Type_Combustible_Bois_gnr ; générateurs bois reliés à la zone ; le texte omet la division par SREF_zn que l'unité kWhef/m² impose
- (2446, p. 1338) O_Cef_imp_[poste]_annuel (zn) = somme_mois somme_energie O_Cef_imp_[poste]_[energie]_mois ;  ; 
- (2447, p. 1338) O_Cef_[energie]_annuel (zn) = somme_mois somme_{poste hors mobilier} O_Cef_imp_[poste]_[energie]_mois ;  ; le poste mobilier est exclu
- (2448 à 2452, p. 1338 et 1339) O_Eef_prod_PV_annuel, O_Eef_prod_coge_annuel, O_Eef_prod_PV_AC_annuel, O_Eef_prod_coge_AC_annuel, O_Eef_Elec_Exportee_annuel = somme_mois des valeurs mensuelles ;  ; zone
- (2453, p. 1339) O_TAC_elec_annuel = 100 x (O_Eef_prod_PV_AC_annuel + O_Eef_prod_coge_AC_annuel) / (O_Eef_prod_PV_annuel + O_Eef_prod_coge_annuel) ;  ; 0 si dénominateur nul (déduit de la note page 1357)
- (2454, p. 1339) O_TAC_elec_PV_annuel = 100 x O_Eef_prod_PV_AC_annuel / O_Eef_prod_PV_annuel ;  ; 
- (2455, p. 1339) O_TAC_elec_coge_annuel = 100 x O_Eef_prod_coge_AC_annuel / O_Eef_prod_coge_annuel ;  ; 
- (2456, p. 1339) O_TAC_coge_global_annuel = 100 x (Cef_tot_comb_cogé,bat + O_Eef_prod_coge_AC_annuel) / (Cef_tot_comb_cogé,bat + O_Eef_prod_coge_annuel) ; Cef_tot_comb (2540, 2541) ; bâtiment
- (2457, p. 1339) O_Cef_annuel (zn) = somme_energie O_Cef_[energie]_annuel ;  ; 
- (2458, p. 1339) O_Cep_annuel (zn) = somme_energie O_Cef_[energie]_annuel x CoefEP[energie] ;  ; 
- (2459, p. 1339) O_Cepnr_annuel (zn) = somme_energie O_Cef_[energie]_annuel x CoefEPnr[energie] ;  ; 
- (2460 à 2462, p. 1339) O_B_Ch_annuel, O_B_Fr_annuel, O_B_Ecs_annuel (zn) = somme_mois ;  ; 
- (2463, p. 1339) O_Cef_imp_[poste]_[energie]_mois (bat) = somme_{h in mois} Qcef[poste;energie]_bat(h) / SREF_bat ;  ; ch, fr, ecs hors électricité
- (2464, p. 1339) O_Cef_imp_[poste]_elec_mois (bat) = somme_{h in mois} Welec_imp[poste]_bat(h) / SREF_bat ; Welec_IMP (2536) ; 
- (2465, p. 1340) O_Cef_cons_[poste]_elec_mois (bat) = somme_{h in mois} Welec_cons[poste]_bat(h) / SREF_bat ;  ; dans le RSEE le bâtiment publie O_Cef_elec_AC_[poste]_annuel plutôt que cons
- (2466 à 2469, p. 1340) productions mensuelles du bâtiment : somme_{h in mois} E_elec_prod_PV_bat, E_elec_prod_coge_bat, E_elec_prod_PV_AC_bat, E_elec_prod_coge_AC_bat / SREF_bat ;  ; 
- (2470, p. 1340) O_Eef_Elec_Exportee_mois (bat) = prod_PV + prod_coge - prod_PV_AC - prod_coge_AC ;  ; 
- (2471 à 2473, p. 1340) O_B_Ch_mois (bat) = somme_{zn in bat} O_B_Ch_mois_zn x SREF_zn / SREF_bat ; idem Fr, Ecs ;  ; 
- (2474 à 2476, p. 1340) annuels du bâtiment par somme des mensuels : O_Cef_imp_[poste]_[energie]_annuel, O_Cef_imp_[poste]_elec_annuel, O_Cef_cons_[poste]_elec_annuel ;  ; 
- (2477, p. 1340 et 1341) sous-décomposition bois du bâtiment, même règle que (2445) sur les générateurs reliés au bâtiment ;  ; 
- (2478, p. 1341) O_Cef_imp_[poste]_annuel (bat) = somme_mois somme_energie O_Cef_imp_[poste]_[energie]_mois ;  ; 
- (2479, p. 1341) O_Cef_[energie]_annuel (bat) = somme_mois somme_{poste hors mobilier} O_Cef_imp_[poste]_[energie]_mois ;  ; 
- (2480 à 2484, p. 1341) productions et export annuels du bâtiment par somme des mensuels ;  ; 
- (2485 à 2487, p. 1341) O_TAC_elec_annuel, O_TAC_elec_PV_annuel, O_TAC_elec_coge_annuel du bâtiment, mêmes formules que 2453 à 2455 ;  ; 
- (2488, p. 1341) O_Cef_annuel (bat) = somme_energie O_Cef_[energie]_annuel ;  ; 
- (2489, p. 1341) O_Cep_annuel (bat) = somme_energie O_Cef_[energie]_annuel x CoefEP[energie] ;  ; 
- (2490, p. 1341) O_Cepnr_annuel (bat) = somme_energie O_Cef_[energie]_annuel x CoefEPnr[energie] ;  ; 
- (2491 à 2493, p. 1341) O_B_Ch_annuel, O_B_Fr_annuel, O_B_Ecs_annuel (bat) = somme_mois ;  ; 
- (2494, p. 1347) Cef_fr_elec_refroidissement,g = Coef_kWh_fr_par_DH(Usage) x max(0 ; min(DH_g ; seuil_haut) - seuil_bas) x Coef_zone_clim_et_alt / CoefEP[elec] ; tableaux 339, 340 ; seuil_bas 350 ; CoefEP 2,3 ; résultat en kWhef/m²/an ; Th-C présent (Th-C ou Th-DBC), au moins un groupe non climatisé dans le bâtiment, Groupe_is_climatisé = 0, DH_g > seuil_bas ; sinon 0
- (2495, p. 1348) groupe : O_Cef_imp_[poste]_[energie]_annuel = somme_mois O_Cef_imp_[poste]_[energie]_mois + Cef_fr_elec_refroidissement,g ;  ; [poste]_[energie] vaut Fr, élec et Fr_élec seulement ; aussi O_Cef_annuel et donc O_Cep_annuel ; les mensuels ne sont pas modifiés
- (2496, p. 1348) zone : O_Cef_imp_[poste]_[energie]_annuel = somme_mois ... + somme_{g in zn} Cef_fr_elec_refroidissement,g x SREF_gr / SREF_zn ;  ; s'applique aux imp et aux cons
- (2497, p. 1348) bâtiment : O_Cef_imp_[poste]_[energie]_annuel = somme_mois ... + somme_{g in bat} Cef_fr_elec_refroidissement,g x SREF_zn / SREF_bat (lire SREF_gr / SREF_bat, le texte imprime SREF_zn) ;  ; 
- (2498, p. 1352) Qcef(poste;energie)_gr(h) = somme_{gen -> gr} Qcef(poste;energie)_gen,gr(h) ; matrice 3 x 6 (tableau 342) ; 
- (2499, p. 1352) Qreq_ch_gr(h) = somme_{em in gr} Qreq_ch_em(h) ; Qreq_fr_gr(h) = somme_{em in gr} Qreq_fr_em(h) ;  ; besoins aux bornes des émetteurs (Besoins.chauffage, Besoins.refroidissement, en Wh)
- (2500, p. 1352) Qreq_gen_ch_gr(h) = somme_{gen -> gr} Qreq_ch_gen,gr(h) ; idem fr ;  ; pertes de distribution incluses ; référence des saisons par groupe (28 jours)
- (2501, p. 1353) Qcef(poste;energie)_gr(h) = somme_{gen in gr} somme_{en = 10..60} Qcef(poste;energie)_gen,gr(h) ;  ; redite de 2498 ligne par ligne
- (2502 à 2504, p. 1353) Welec_cons[ch]_gr(h) = somme_{gen} Qcef(ch;elec)_gen,gr(h) ; idem [fr] et [ecs] ; colonne 50 ; 
- (2505, p. 1353) Welec_cons[auxvent]_gr(h) = W_ventmoy_s,gr(h) + W_vent-loc-tot_gr(h) + W_abs-GA_gr(h) ; ventilateurs des centrales (consommation.puissance_ventilateurs), ventilateurs locaux des émetteurs, brasseurs d'air ; 
- (2506, p. 1353) Welec_cons[auxdist]_gr(h) = somme W_aux_prim-e_dp-e,gr + somme W_aux_dp,gr + somme_{ds in gr} W_aux_ds + somme W_aux_dCTA,gr ; distributions primaire, de groupe, intergroupe, de CTA ; entrées du lot distribution
- (2507, p. 1353) Qcef(poste;energie)_zn(h) = somme_{gr in zn} Qcef(poste;energie)_gr(h) ;  ; 
- (2508 à 2510, p. 1353 et 1354) Welec_cons[ch|fr|ecs]_zn(h) = somme_{gr in zn} Welec_cons[...]_gr(h) ;  ; 
- (2511, p. 1354) Welec_cons[ecl]_zn(h) = somme_gr Welec_cons[ecl]_gr(h) + W_cef_ecl_park_z(h) + W_cef_ecl_parties_communes_z(h) ; Wecl_gr = Besoins.eclairage ; parkings (2354 réparti) ; fiche 7.2 ; 
- (2512, p. 1354) Welec_cons[auxvent]_zn(h) = somme_gr Welec_cons[auxvent]_gr(h) + W_cef_vent_park_z(h) ; ventilation des parkings (2340 à 2346 réparti) ; 
- (2513, p. 1354) Welec_cons[auxdist]_zn(h) = somme_gr Welec_cons[auxdist]_gr(h) ;  ; 
- (2514, p. 1354) Welec_cons[depl]_zn(h) = W_cef_ascenseurs_z(h) + W_cef_escalators_z(h) ; (2311) ; escalators fiche 10.2 ; le banc constate que les RSEE y mettent aussi les parkings (voir points ouverts)
- (2515, p. 1354) Welec_hors_mobilier_zn(h) = somme_poste Welec_cons[poste]_zn(h) ;  ; périmètre RE2020
- (2516, p. 1354) Welec_tous_usages_zn(h) = Welec_hors_mobilier_zn(h) + W_cef_mobilier_zn(h) ; W_cef_mobilier = Cef_us_mob_z (94) ; 
- (2517, p. 1354) Qcef(poste;energie)_bat(h) = somme_{zn in bat} Qcef(poste;energie)_zn(h) ;  ; 
- (2518, p. 1354) Welec_cons[poste]_bat(h) = somme_{zn in bat} Welec_cons[poste]_zn(h) ;  ; tous postes
- (2519, p. 1355) Welec_hors_mobilier_bat(h) = somme_poste Welec_cons[poste]_bat(h) ;  ; 
- (2520, p. 1355) Welec_tous_usages_bat(h) = Welec_hors_mobilier_bat(h) + W_cef_mobilier_bat(h) ;  ; 
- (2521, p. 1355) E_elec_prod_coge_gr(h) = somme_{gen -> gr} Qef_prelec_gen,gr(h) ;  ; 
- (2522, 2523, p. 1355) E_elec_prod_coge_zn(h) = somme_gr ; E_elec_prod_coge_bat(h) = somme_zn ;  ; 
- (2524, p. 1355) E_elec_prod_PV_bat(h) = E_elec_prod_PV_integre_bat(h) + E_elec_prod_PV_parcelle_bat(h) ;  ; 
- (2525, p. 1355) E_elec_prod_PV_integre_bat(h) = somme_{PV in bat} Pond_PV(h) ; fiche PV ; 
- (2526, p. 1355 et 1356) E_elec_prod_PV_parcelle_bat(h) = somme_{PV_projet} Pond_PV_projet(h) x Welec_tous_usages_bat(h) / somme_bat Welec_tous_usages_bat(h) ;  ; répartition au prorata des consommations horaires tous usages du projet
- (2527, p. 1356) E_elec_prod_tot_bat(h) = E_elec_prod_PV_bat(h) + E_elec_prod_coge_bat(h) ;  ; 
- (2528, p. 1357) E_elec_prod_AC_bat(h) = min(E_elec_prod_tot_bat(h) ; Welec_tous_usages_bat(h)) ;  ; mobilier compris dans la consommation
- (2529, p. 1357) TAC_bat(h) = E_elec_prod_AC_bat(h) / E_elec_prod_tot_bat(h) ;  ; 0 si production nulle (note page 1357)
- (2530, p. 1357) TAP_bat(h) = E_elec_prod_AC_bat(h) / Welec_tous_usages_bat(h) ;  ; 0 si consommation nulle (déduit)
- (2531, 2532, p. 1357) E_elec_prod_PV_AC_bat(h) = TAC_bat(h) x E_elec_prod_PV_bat(h) ; E_elec_prod_coge_AC_bat(h) = TAC_bat(h) x E_elec_prod_coge_bat(h) ;  ; 
- (2533 à 2535, p. 1357) E_elec_prod_AC_zn(h) = TAC_bat(h) x E_elec_prod_tot_zn(h) ; E_elec_prod_PV_AC_zn(h) = TAC_bat x E_elec_prod_PV_zn ; E_elec_prod_coge_AC_zn(h) = TAC_bat x E_elec_prod_coge_zn ; E_elec_prod_PV_zn non défini par le texte (voir points ouverts) ; 
- (2536, p. 1357) Welec_IMP[poste]_bat(h) = Welec_cons[poste]_bat(h) x (1 - TAP_bat(h)) ;  ; tous postes, mobilier compris
- (2537, p. 1357) Welec_IMP[poste]_zn(h) = Welec_cons[poste]_zn(h) x (1 - TAP_bat(h)) ; TAP du bâtiment appliqué à chaque zone ; 
- (2538, 2539, p. 1357) Welec_tous_usages_IMP_bat(h) = somme_poste Welec_IMP[poste]_bat(h) ; idem zone ;  ; 
- (2540, p. 1358) Cef_comb_tot_cogé(h) = (Cef_ch_comb_coge,bat(h) + Cef_ECS_comb_coge,bat(h)) / SREF_bat ;  ; générateurs à combustion avec Is_cogénération = 1
- (2541, p. 1358) Cef_comb_tot_coge,bat(h) = somme_{coge in bat} C_comb_tot_coge,bat(h) ;  ; 
- (2542, p. 1358) TAC_coge_global_bat(h) = (Cef_comb_tot_coge,bat(h) + E_elec_prod_coge_AC_bat(h)) / (Cef_comb_tot_coge,bat(h) + E_elec_prod_coge_bat(h)) ;  ; chaleur supposée autoconsommée à 100 %
- (93, p. 90) Cef_us_mob_loc(h) = Aloc x Qmax_proc_loc x tach(m,s) x tsch(j,h) ; apports internes hors occupants du local (scénarios conventionnels), Wh ; 
- (94, p. 90) Cef_us_mob_z(h) = somme_{loc in z} Cef_us_mob_loc(h) ;  ; 
- (95, p. 90) Cef_us_mob_annuel_z = somme_{h=1..8760} Cef_us_mob_z(h) ; kWh/m² SREF (division par SREF_zn et 1000 implicite) ; 
- (2275, p. 1269) Pti_i = Pman + (netage + 1) x (Pboutonpal + Pindpal) + Pfrein + Pveilleporte + Pindcab + Pec(Q_i) + Palarm ; tableaux 316, 317 ; si Pti non connu (ScVeille = 0)
- (2276 à 2279, p. 1269) dP1 = 0 ; T1 = 86400 ; dP2 = 0 ; T2 = 86400 ;  ; défauts en cascade (page 1269)
- (2280, p. 1270) Q_z = somme_i Q_i x C(i,z) ;  ; 
- (2281, p. 1270) NB_z = max_année(somme_{l in z} Nocc_l) ; occupants conventionnels des locaux ; le banc existant lit les adultes équivalents (ascenseurs.occupants_conventionnels)
- (2282, p. 1270) BV_z = Bv(k) ; tableau 311 ; 
- (2283, p. 1270) BVNB_i = somme_z C(i,z) x Q_i / Q_z x BV_z x NB_z ;  ; 
- (2284, 2285, p. 1270) Ndem_i = BVNB_i x Mpass / (Q_i x 0,2) ; somme X.S(direction,X) = 0,2 ;  ; 
- (2286, p. 1270) a_i = Ac(V_i) ; tableau 313 ; 
- (2287, p. 1270) Ch_i = (netage_i + 1) / (netage_i + 2) x Cor_Ch ;  ; 
- (2288 à 2291, p. 1270) rg_i = Rg(TechMac) ; P_i = deco x Q_i ; G_i = P_i + Cp_i x Q_i ; Mi_i = alpha(TechMac) x (G_i + P_i) ;  ; 
- (2292, p. 1271) Tmob_i = (Ch_i x H_i / V_i + V_i / a_i) x Ndem_i ; s ; 
- (2293, p. 1271) Tmobh_i = Tmob_i / (365 x 3600) ; h par jour ; 
- (2294, p. 1271) Timmob_i = 24 x 365 x 3600 - Tmob_i ;  ; 
- (2295, 2296, p. 1271) Timmob_n_z = 8 x 365 x 3600 (habitation) ; (12 x 365 + 52 x 48 + 9 x 24) x 3600 (autres) ;  ; 
- (2297, p. 1271) Timmob_n_i = somme_z C(i,z) x Q_i / Q_z x Timmob_n_z ;  ; cabines multizones ; ascenseurs.py prend habitation si toutes les zones sont d'habitation (écart à corriger)
- (2298, p. 1271) Timmob_j_i = max(0 ; Timmob_i - Timmob_n_i) ;  ; 
- (2299, p. 1271) F_i(X) = P_i + X x Q_i ;  ; 
- (2300, p. 1271) Emoy_bas(X,Z) = max(0 ; (G+F)Cf V²/2a + (G - F) g V²/2a + (G+F+Mi) V²/2) + max(0 ; (G+F) Cf (Z - V²/2a) + (G - F) g (Z - V²/2a)) + max(0 ; (G+F) Cf V²/2a + (G - F) g V²/2a - (G+F+Mi) V²/2) ; forme physique retenue par ascenseurs._trajet ; le texte imprime (G + F) g au premier terme ; 
- (2301, p. 1272) Emoy_haut(X,Z) = même expression avec le travail de la pesanteur de signe opposé : -(G - F) g ;  ; 
- (2302, p. 1272) Emoy_i = somme_{X in 0, 0.25, 0.5, 0.75, 1} [S(haut,X) Emoy_haut(X, Ch_i H_i) + S(bas,X) Emoy_bas(X, Ch_i H_i)] / rg_i ;  ; le banc retient la moyenne (division par 2) et non la somme des deux sens
- (2303, p. 1272) Etm_i = (Emoy_i x Cor_Emobcab x Ndem_i / 2 + Eporte x Ndem_i + Pti_i x Tmob_i) / 3600 ; Wh ; 
- (2304, p. 1272) Eti_i = [dP1 min(1 ; T1 / (Timmob_j/Ndem)) + dP2 min(1 ; (T1+T2) / (Timmob_j/Ndem)) + (Pti - dP1 - dP2)] x Timmob_j / 3600 + [dP1 min(1 ; T1 / (Timmob_n/365)) + dP2 min(1 ; (T1+T2) / (Timmob_n/365)) + (Pti - dP1 - dP2)] x Timmob_n / 3600 ; lecture de ascenseurs.veille ; l'impression du texte est ambiguë sur ce que multiplie Timmob ; 
- (2305, p. 1272) Etot_i = Etm_i + Eti_i ;  ; 
- (2306, p. 1273) U_i(h) = somme_z C(i,z) x Q_i / Q_z x U_z(h) ; U_z : scénario de mobilité de la zone (chapitre 15, lignes « mobilité » jour x heure) ; 
- (2307, p. 1273) Fmob_i(h) = U_i(h) / somme_t U_i(t) ;  ; 
- (2308, p. 1273) Fimob_i(h) = (1/365 - Fmob_i(h) x Tmobh_i) / (24 - Tmobh_i) [lecture ; texte imprimé : « 1/365 . Tmobh - Fmob(h) » sur « 24 Tmobh - 1 »] ;  ; somme sur l'année égale à 1 ; voir points ouverts
- (2309, p. 1273) Pcab_i(h) = Fimob_i(h) x Eti_i + Fmob_i(h) x Etm_i ; W (pas de 1 h) ; 
- (2310, p. 1273) Pcab_z(h) = somme_i Pcab_i(h) x C(i,z) Q_z / somme_j C(i,j) Q_j ;  ; 
- (2311, p. 1273) W_ef_ascenseurs_z(h) = Pcab_z(h) x 1 h ; Wh ; 
- (2327, p. 1288) Dvent2 = 900 Npl ; Dvent1 = 450 Npl ; Pvent2 = 40 Npl ; Pvent1 = 5 Npl ; Pvent600 = 40 ;  ; IsParamVentilationDefaut (le texte dit « = 0 », le RSEE semble coder 1 = défaut : parkings.py lit 1)
- (2328 à 2330, p. 1288) Larg = (Spl Npl / Net / Rl)^0,5 ; Long = Rl Larg ; Peri = 2 Long + 2 Larg ;  ; 
- (2331 à 2333, p. 1288) Lmoytraj = Peri (Net/4 + 1/4) ; Dtraj = Lmoytraj / Vmoy ; Dmvmt = Dfix + Dtraj ; h ; 
- (2334, p. 1288) Pvent(h) = 0 ;  ; Type = ext
- (2335, p. 1289) Pvent(h) = 0 ;  ; Vent = non
- (2336 à 2338, p. 1289) Nveh(h) = Npl Rutil Rmvtpl(h) ; ProdCO(h) = ProdCOveh Nveh(h) Dmvmt ; Dreq(h) = ProdCO(h) / (CCOlim Effvent) ;  ; Type int, usage bureau ou commerce, NbjO(j) = 1
- (2339, p. 1289) Dreq(h) = 0 ;  ; NbjO(j) = 0
- (2340 à 2343, p. 1289) Pvent(h) = 0 si Dreq = 0 ; Dreq Pvent1 / Dvent1 si Dvent1 > Dreq ; sinon Dreq Pvent2 / Dvent2 ;  ; 
- (2344, 2345, p. 1290) Pvent(h) = Pvent600 Npl Rutil Rmvtpl(h) si NbjO(j) = 1, sinon 0 ;  ; habitat, Type int, Reg = 1
- (2346, p. 1290) Pvent(h) = Pvent600 Npl Rutil ;  ; habitat, Reg = 0
- (2347, p. 1290) Event = somme_{h=1..8760} Pvent(h) ; réparti au prorata des surfaces SRT des zones du bâtiment, ajouté à Cef_park_z(h) ;  ; 
- (2348, 2349, p. 1295) Fhint(h) = 1 ; TauDet(h) = 0,2 ;  ; 
- (2350, 2351, p. 1296) Pecins = 75 Npl (int) ; 8 Npl (ext) ; W ; défaut
- (Ouv(h) (sans numéro), p. 1297) Ouv(h) = 1 si NbjO(j) = 1 et [jsem 1 à 5 et Hleg dans PlagOse] ou [jsem 6 ou 7, sauf dimanche en commerce, et Hleg dans PlagOwe] ; sinon 0 ;  ; 
- (2352, p. 1297) Det(h) = 1 si NbjO(j) = 1 et Hleg dans l'union des PlagDse_j (semaine) ou PlagDwe_j (week-end) ; sinon 0 ; jusqu'à 3 plages ; 
- (2353, p. 1298) Fh(h) = Fhint(h) si Type int, sinon Fhext(h) ; tableau 327 ; 
- (2354, p. 1298) Pecapp(h) = Pecins x [Ouv(h) Fh(h) (1 - Det(h) + Det(h) TauDet) + (1 - Ouv(h)) Ex] ; W ; 
- (2355, p. 1298) Eec = somme_{h=1..8760} Pecapp(h) ; Pecapp réparti au prorata des SREF des zones, ajouté à Cef_park_z(h) ;  ; 
- (2553, p. 1368) Nocc_bat = somme_{zn in bat} Nocc_zn ;  ; 
- (2554, p. 1369) Cep_annuel_par_occ_bat = Cep_annuel_bat x SREF_bat / Nocc_bat ; 0 si Nocc_bat = 0 ; kWhep/occ/an ; sortie O_Cep_annuel_occ ; 

## Algorithme

```
Structure proposée : module openbce/bilans.py (classes et fonctions ci-dessous), module openbce/forfait_froid.py (2494 à 2497), fonction mobilier dans scenarios.py ou bilans.py (93 à 95), et banc/sorties_c.py. Les tableaux horaires sont des np.ndarray de longueur 8760 en Wh. POSTES = ("ch", "fr", "ecs", "ecl", "auxvent", "auxdist", "depl", "mobilier") ; ENERGIES = {10: "gaz", 20: "fioul", 30: "charbon", 40: "bois", 50: "elec", 60: "reseau"}.

# ---------- constantes ----------
COEF_EP = {"gaz": 1, "fioul": 1, "charbon": 1, "bois": 1, "elec": 2.3, "reseau": 1}            # tableau 337
def coef_ep_nr(energie, bat, poste):                                                             # tableau 337
    if energie == "elec": return 2.3
    if energie == "bois": return 0.0
    if energie == "reseau": return 1.0 if poste == "fr" else 1.0 - bat.nombre("RatENR_rdch", 0.0)
    return 1.0
SEUIL_BAS_DH = 350.0 ; COEF_KWH_FR_PAR_DH = {1: 0.011, 2: 0.011, 3: 0.009, 4: 0.016, 5: 0.016}   # tableau 339
COEF_ZONE_ALT = {"H1a": (0.8, 0.6, 0.4), "H1b": (1, 0.8, 0.6), "H1c": (1, 0.8, 0.6), "H2a": (0.7, 0.5, 0.3),
                 "H2b": (1, 0.8, 0.6), "H2c": (1.1, 0.9, 0.7), "H2d": (1.2, 1, 0.8), "H3": (1.2, 1, 0.8)}  # tableau 340

# ---------- états portés d'une heure à l'autre ----------
# Aucun état interne propre à cette famille : tout est somme ou cumul (page 1335). Les seuls états
# horaires sont ceux des modules amont (modèle thermique du groupe, saisons sur 28 jours alimentées
# par Qreq_gen_ch/fr de (2500), relances). Les cumuls mensuels et annuels se font a posteriori sur les
# tableaux 8760 ; le calendrier (calendrier.construire) donne le mois de chaque heure, l'heure légale
# cal.case et le jour de semaine cal.jour_semaine.

@dataclass
class BilanGroupe:
    sref: float
    qcef: dict[tuple[str, str], np.ndarray]      # (poste in ch, fr, ecs ; energie) -> Wh/h   (2498)
    welec: dict[str, np.ndarray]                 # poste -> Wh/h, postes ch, fr, ecs, ecl, auxvent, auxdist (2502 à 2506)
    qreq_ch: np.ndarray ; qreq_fr: np.ndarray    # (2499)
    qw_brut: np.ndarray                          # besoins ECS bruts
    qreq_gen_ch: np.ndarray ; qreq_gen_fr: np.ndarray   # (2500), pour les saisons
    e_prod_coge: np.ndarray                      # (2521)
    forfait_fr: float = 0.0                      # kWhef/m²/an (2494)

def bilan_groupe(groupe, usage, besoins: Besoins, generations: list[SortieGenerationGroupe], w_ventmoy, w_vent_loc, w_brasseurs, w_auxdist) -> BilanGroupe:
    sref = groupe.nombre("SHAB") if usage in (1, 2) else groupe.nombre("SU")                 # (2413), (2414)
    qcef = {(p, e): zeros(8760) for p in ("ch", "fr", "ecs") for e in ENERGIES.values()}
    e_coge = zeros(8760)
    for gen in generations:                                                                 # (2498), (2501)
        for (p, e), serie in gen.qcef.items(): qcef[(p, e)] += serie
        e_coge += gen.qef_prelec                                                            # (2521)
    welec = {"ch": qcef[("ch", "elec")], "fr": qcef[("fr", "elec")], "ecs": qcef[("ecs", "elec")],    # (2502) à (2504)
             "ecl": besoins.eclairage,                                                                # Wecl_gr
             "auxvent": w_ventmoy + w_vent_loc + w_brasseurs,                                         # (2505)
             "auxdist": w_auxdist}                                                                     # (2506)
    return BilanGroupe(sref, qcef, welec, besoins.chauffage, besoins.refroidissement, qw_brut, qreq_gen_ch, qreq_gen_fr, e_coge)

@dataclass
class BilanZone:
    sref: float ; usage: int ; nocc: float
    qcef: dict ; welec_cons: dict[str, np.ndarray]     # 8 postes dont depl et mobilier
    welec_imp: dict[str, np.ndarray]                   # rempli après le bâtiment (2537)
    e_prod_coge: np.ndarray ; e_prod_pv: np.ndarray    # PV attribué à la zone : voir points ouverts
    groupes: list[BilanGroupe]

def bilan_zone(zone, groupes: list[BilanGroupe], park_ecl_z, park_vent_z, ecl_parties_communes_z, ascenseurs_z, escalators_z, mobilier_z) -> BilanZone:
    sref = sum(g.sref for g in groupes)                                                      # (2415)
    qcef = {k: sum(g.qcef[k] for g in groupes) for k in groupes[0].qcef}                     # (2507)
    w = {p: sum(g.welec[p] for g in groupes) for p in ("ch", "fr", "ecs", "auxdist")}        # (2508) à (2510), (2513)
    w["ecl"] = sum(g.welec["ecl"] for g in groupes) + park_ecl_z + ecl_parties_communes_z    # (2511)
    w["auxvent"] = sum(g.welec["auxvent"] for g in groupes) + park_vent_z                    # (2512)
    w["depl"] = ascenseurs_z + escalators_z                                                  # (2514)  [RSEE : + parkings, voir points ouverts]
    w["mobilier"] = mobilier_z                                                               # (2516), (94)
    return BilanZone(sref, zone.entier("Usage"), zone.nombre("Nocc", 0.0), qcef, w, {}, sum(g.e_prod_coge for g in groupes), zeros(8760), groupes)

def mobilier_zone(sc: Scenario) -> np.ndarray:
    return sc.apports_usages.copy()           # W sur un pas de 1 h = Wh : Cef_us_mob_z(h) = somme_loc Aloc Qmax_proc tach tsch (93), (94)

def bilan_batiment(bat, zones: list[BilanZone], pv_integre_bat, pv_parcelle_projet, part_parcelle) -> BilanBatiment:
    sref = sum(z.sref for z in zones)                                                        # (2416)
    qcef = {k: sum(z.qcef[k] for z in zones) for k in zones[0].qcef}                         # (2517)
    w_cons = {p: sum(z.welec_cons[p] for z in zones) for p in POSTES}                        # (2518)
    hors_mob = sum(w_cons[p] for p in POSTES if p != "mobilier")                             # (2519)
    tous_usages = hors_mob + w_cons["mobilier"]                                              # (2520)
    e_coge = sum(z.e_prod_coge for z in zones)                                               # (2523)
    # part_parcelle(h) = tous_usages_bat(h) / somme_bat tous_usages_bat(h) : exige un passage préalable sur tous les bâtiments du projet
    e_pv = pv_integre_bat + pv_parcelle_projet * part_parcelle                               # (2524) à (2526)
    e_tot = e_pv + e_coge                                                                    # (2527)
    e_ac = np.minimum(e_tot, tous_usages)                                                    # (2528)
    tac = np.where(e_tot > 0, e_ac / e_tot, 0.0)                                             # (2529)
    tap = np.where(tous_usages > 0, e_ac / tous_usages, 0.0)                                 # (2530)
    e_pv_ac, e_coge_ac = tac * e_pv, tac * e_coge                                            # (2531), (2532)
    w_imp = {p: w_cons[p] * (1 - tap) for p in POSTES}                                       # (2536)
    for z in zones:
        z.welec_imp = {p: z.welec_cons[p] * (1 - tap) for p in POSTES}                       # (2537)
        z.e_prod_ac = tac * (z.e_prod_pv + z.e_prod_coge) ; z.e_pv_ac = tac * z.e_prod_pv ; z.e_coge_ac = tac * z.e_prod_coge   # (2533) à (2535)
    tous_imp = sum(w_imp.values())                                                           # (2538) ; zone : (2539)
    cef_comb = (cef_ch_comb_coge + cef_ecs_comb_coge) / sref                                 # (2540), (2541) : entrée du lot génération
    tac_coge_global = np.where(cef_comb + e_coge > 0, (cef_comb + e_coge_ac) / (cef_comb + e_coge), 0.0)   # (2542)
    return BilanBatiment(...)

# ---------- forfait de refroidissement (13.3), post-traitement annuel ----------
def forfait_froid(groupe, usage, dh: float, seuil_haut: float, zone_climatique: str, altitude: float, mode_thc: bool, un_groupe_non_climatise: bool) -> float:
    if not (mode_thc and un_groupe_non_climatise) or groupe.entier("Is_Climatise", 0) == 1 or dh <= SEUIL_BAS_DH:
        return 0.0                                                                           # conditions pages 1343 et 1347
    col = 0 if altitude < 400 else (1 if altitude < 800 else 2)
    return COEF_KWH_FR_PAR_DH[usage] * max(0.0, min(dh, seuil_haut) - SEUIL_BAS_DH) * COEF_ZONE_ALT[zone_climatique][col] / COEF_EP["elec"]   # (2494)
# dh = Besoins.dh du calcul Th-D du même groupe (13.5, 2552) ; seuil_haut = DH_max de l'arrêté (lu dans Sortie_Groupe_D.O_NbDegresHeures_max pour le banc).

# ---------- sorties (13.2) ----------
def mensuel(serie_wh, cal, sref) -> list[float]:          # 12 valeurs kWh/m²
    return [serie_wh[cal.mois == m].sum() / 1000 / sref for m in range(1, 13)]

def sorties_groupe(b: BilanGroupe, cal) -> dict:
    s = {}
    for p in ("ch", "fr", "ecs"):
        s[f"O_Cef_{p}_mois"] = mensuel(sum(b.qcef[(p, e)] for e in ENERGIES.values()), cal, b.sref)      # (2417)
        for e in ENERGIES.values(): s[f"O_Cef_{p}_{e}_annuel"] = b.qcef[(p, e)].sum() / 1000 / b.sref      # (2422)
    for p, nom in (("ecl", "ecl"), ("auxvent", "aux_ventilateur"), ("auxdist", "aux_distribution")):
        s[f"O_Cef_{nom}_mois"] = mensuel(b.welec[p], cal, b.sref)                                            # (2418)
        s[f"O_Cef_{ {'ecl':'ecl','auxvent':'auxv','auxdist':'auxs'}[p] }_elec_annuel"] = b.welec[p].sum() / 1000 / b.sref   # (2423)
    s["O_B_Ch_mois"], s["O_B_Fr_mois"], s["O_B_Ecs_mois"] = (mensuel(x, cal, b.sref) for x in (b.qreq_ch, b.qreq_fr, b.qw_brut))   # (2419) à (2421)
    for p in POSTES_GROUPE: s[f"O_Cef_{p}_annuel"] = sum(s[f"O_Cef_{p}_mois"])                               # (2424)
    s["O_Cef_fr_annuel"] += b.forfait_fr ; s["O_Cef_fr_elec_annuel"] += b.forfait_fr                        # (2495) : Fr et Fr_élec ; mensuels inchangés
    for e in ENERGIES.values(): s[f"O_Cef_{e}_annuel"] = sum(s.get(f"O_Cef_{p}_{e}_annuel", 0) for p in POSTES_GROUPE)   # (2425)
    s["O_Cef_elec_annuel"] += b.forfait_fr                                                                   # (2495) : élec
    s["O_Cef_annuel"] = sum(s[f"O_Cef_{e}_annuel"] for e in ENERGIES.values())                               # (2426)
    s["O_Cep_annuel"] = sum(s[f"O_Cef_{e}_annuel"] * COEF_EP[e] for e in ENERGIES.values())                  # (2427)
    s["O_B_Ch_annuel"], s["O_B_Fr_annuel"], s["O_B_Ecs_annuel"] = (sum(s[k]) for k in ("O_B_Ch_mois", "O_B_Fr_mois", "O_B_Ecs_mois"))   # (2428) à (2430)
    return s

def sorties_zone(z: BilanZone, bat, cal) -> dict:
    s = {}
    for p in ("ch", "fr", "ecs"):
        for e in ENERGIES.values():
            if e != "elec": s[f"O_Cef_{e}_imp_{p}_mois"] = mensuel(z.qcef[(p, e)], cal, z.sref)             # (2431) (nom RSEE : énergie avant imp)
    for p in POSTES:
        s[f"O_Cef_elec_imp_{p}_mois"] = mensuel(z.welec_imp[p], cal, z.sref)                                 # (2432)
        s[f"O_Cef_elec_cons_{p}_mois"] = mensuel(z.welec_cons[p], cal, z.sref)                               # (2433)
    s["O_Eef_Prod_PV_mois"], s["O_Eef_Prod_Coge_mois"], s["O_Eef_Prod_PV_AC_mois"], s["O_Eef_Prod_Coge_AC_mois"] = ...   # (2434) à (2437)
    s["O_Eef_Elec_Exportee_mois"] = PV + coge - PV_AC - coge_AC (mois par mois)                              # (2438)
    s["O_B_Ch_mois"] = [sum(g_s["O_B_Ch_mois"][m] * g.sref for g, g_s in groupes) / z.sref for m in range(12)]   # (2439) ; idem Fr, Ecs (2440), (2441)
    annuels = somme des mensuels pour toutes les séries ci-dessus                                            # (2442) à (2444), (2448) à (2452)
    forfait_zn = sum(g.forfait_fr * g.sref for g in z.groupes) / z.sref                                      # (2496)
    s["O_Cef_imp_fr_annuel"] += forfait_zn ; s["O_Cef_elec_imp_fr_annuel"] += forfait_zn ; s["O_Cef_elec_cons_fr_annuel"] += forfait_zn ; s["O_Cef_elec_imp_annuel"] += forfait_zn
    # sous-décomposition bois (2445) : à partir des Qcef par générateur bois relié à la zone, par (poêle | chaudière) x (buch | plaq | gran) x (ch | ecs), / SREF_zn
    for p in POSTES: s[f"O_Cef_imp_{p}_annuel"] = somme sur énergies et mois                                 # (2446)
    for e in ENERGIES.values(): s[f"O_Cef_{e}_imp_annuel"] = somme sur postes HORS mobilier et mois          # (2447)
    s["O_TAC_elec_annuel"], s["O_TAC_elec_PV_annuel"], s["O_TAC_elec_Coge_annuel"] = (2453) à (2455), 0 si dénominateur nul
    s["O_Cef_annuel"] = sum(s[f"O_Cef_{e}_imp_annuel"])                                                      # (2457)
    s["O_Cep_annuel"] = sum(s[f"O_Cef_{e}_imp_annuel"] * COEF_EP[e])                                         # (2458)
    s["O_Cep_nr_annuel"] = sum(s[f"O_Cef_{e}_imp_{p}_annuel"] * coef_ep_nr(e, bat, p) pour e, p hors mobilier)   # (2459), réseau distingué ch/ecs et fr
    s["O_B_Ch_annuel"], ... = somme des mensuels                                                              # (2460) à (2462)
    s["O_SREF"], s["O_SHAB"], s["O_SU"], s["Usage"], s["Nocc"] = ...
    return s

def sorties_batiment(b: BilanBatiment, bat, cal) -> dict:
    mêmes séries qu'en zone sur les tableaux du bâtiment : (2463) à (2470) mensuels, (2471) à (2473) besoins pondérés par SREF_zn, (2474) à (2476) annuels,
    (2477) bois, (2478) par poste, (2479) par énergie hors mobilier, (2480) à (2484) productions et export, (2485) à (2487) TAC,
    forfait_bat = sum(g.forfait_fr * g.sref for g in tous les groupes) / sref_bat ajouté à imp_fr, elec_imp_fr, elec_AC/cons_fr, elec_imp   # (2497)
    s["O_Cef_annuel"] (2488) ; s["O_Cep_annuel"] (2489) ; s["O_Cep_nr_annuel"] (2490) ; s["O_B_*_annuel"] (2491) à (2493)
    s["O_TAC_Global_coge_annuel"] = 100 x (Cef_tot_comb + coge_AC_annuel) / (Cef_tot_comb + coge_annuel), 0 si nul   # (2456)
    nocc_bat = sum(z.nocc for z in b.zones)                                                                   # (2553)
    s["O_Cep_annuel_occ"] = s["O_Cep_annuel"] * b.sref / nocc_bat if nocc_bat > 0 else 0.0                    # (2554)
    s["O_Type_Reseau"], s["O_RatENR_rdch"] = bat.entier("Type_Reseau", 0), bat.nombre("RatENR_rdch", 0.0)
    return s

# ---------- ordre d'appel sur un projet (13.4 page 1349 : groupe, zone, bâtiment, production, imports bâtiment puis zone) ----------
def calculer_projet(projet):
    cal = calendrier.construire() ; sref_zones = {(b, z): ...}
    park = parkings.du_projet(...)  # à scinder en deux séries horaires ecl et vent par zone, réparties au prorata des SREF (2347, 2355)
    for bat in projet.entree.directs("Batiment"):
        occupants = ascenseurs.occupants_conventionnels(bat) ; asc = ascenseurs.du_batiment(bat, occupants)   # (2280) à (2305), (2310) ; distribution horaire (2306) à (2311) à ajouter
        zones = []
        for zone in bat.directs("Zone"):
            sc = scenarios.habitation(...) ou tertiaire(...)
            groupes = []
            for g in zone.directs("Groupe"):
                besoins_c = groupe.calculer(g, ..., thc=ThC(...))          # Th-C : Qreq_ch, Qreq_fr, Wecl
                besoins_d = groupe.calculer(g, ..., thd=ThD(...))          # Th-D : DH (2552)
                gens = generation.pour_groupe(...)                         # lot génération : Qcef matrices, Qef_prelec, Qreq_gen
                bg = bilan_groupe(g, usage, besoins_c, gens, consommation.puissance_ventilateurs(...), w_vent_loc, w_brasseurs, w_auxdist)
                bg.forfait_fr = forfait_froid(g, usage, besoins_d.dh, seuil_haut, zone_clim, altitude, True, any_non_climatise(bat))
                groupes.append(bg)
            zones.append(bilan_zone(zone, groupes, park_ecl[z], park_vent[z], ecl_pc[z], asc_horaire[z], zeros, mobilier_zone(sc)))
        bb = bilan_batiment(bat, zones, pv_integre, pv_parcelle, part_parcelle)          # part_parcelle exige une première passe sur tous les bâtiments (2526)
        sorties = {"bat": sorties_batiment(bb, bat, cal), "zones": [sorties_zone(z, bat, cal) for z in zones], "groupes": [sorties_groupe(g, cal) for z in zones for g in z.groupes]}

# ---------- banc (banc/sorties_c.py) ----------
# Compare, par Index (bâtiment, zone, groupe), chaque clé calculée à la clé homonyme de Sortie_*_C (Noeud.nombre, Noeud.mensuel), et
# d'abord les identités internes du RSEE lui-même (Cep = 2,3 x Cef_elec + ..., zone = groupes + depl, Cep_occ = Cep x SREF / somme Nocc), qui
# valident la lecture des formules sans dépendre des lots amont.
```

## Sorties RSEE pour le banc

- `O_SREF, O_SHAB, O_SU` (Sortie_Groupe_C, Sortie_Zone_C (et O_SREF seul en Sortie_Batiment_C), m²)
- `O_Cef_annuel` (Sortie_Groupe_C (2426), Sortie_Zone_C (2457), Sortie_Batiment_C (2488), kWhef/m²/an)
- `O_Cep_annuel` (Sortie_Groupe_C (2427), Sortie_Zone_C (2458), Sortie_Batiment_C (2489), kWhep/m²/an)
- `O_Cep_nr_annuel` (Sortie_Zone_C (2459), Sortie_Batiment_C (2490), kWhep/m²/an)
- `O_Cep_annuel_occ` (Sortie_Batiment_C (2554), kWhep/occupant/an)
- `O_Cef_ch_annuel, O_Cef_fr_annuel, O_Cef_ecs_annuel, O_Cef_ecl_annuel, O_Cef_aux_ventilateur_annuel, O_Cef_aux_distribution_annuel` (Sortie_Groupe_C (2424) ; fr contient le forfait 13.3 (2495), kWhef/m²/an)
- `O_Cef_[ch|fr|ecs]_[gaz|fioul|bois|reseau|elec]_annuel, O_Cef_ecl_elec_annuel, O_Cef_auxv_elec_annuel, O_Cef_auxs_elec_annuel` (Sortie_Groupe_C (2422, 2423), kWhef/m²/an)
- `O_Cef_[gaz|fioul|bois|elec|reseau]_annuel` (Sortie_Groupe_C (2425), kWhef/m²/an)
- `O_Cef_[ch|fr|ecs|ecl]_mois, O_Cef_aux_ventilateur_mois, O_Cef_aux_distribution_mois` (Sortie_Groupe_C (2417, 2418), 12 Sortie_Mensuelle (Mois, Valeur), kWhef/m²)
- `O_B_Ch_annuel, O_B_Fr_annuel, O_B_Ecs_annuel, O_B_Ecl_annuel et les _mois` (Sortie_Groupe_C (2419 à 2421, 2428 à 2430), Sortie_Zone_C (2439 à 2441, 2460 à 2462), Sortie_Batiment_C (2471 à 2473, 2491 à 2493) ; O_B_Ecl n'est pas dans le texte, kWh/m²/an et kWh/m²)
- `O_Cef_imp_[ch|fr|ecs|ecl|auxvent|auxdist|deplacement|mobilier]_annuel` (Sortie_Zone_C et Sortie_Batiment_C (2446, 2478), kWhef/m²/an)
- `O_Cef_[gaz|fioul|bois|elec|reseau]_imp_annuel` (Sortie_Zone_C et Sortie_Batiment_C (2447, 2479), hors mobilier, kWhef/m²/an)
- `O_Cef_[gaz|fioul|bois|reseau]_imp_[ch|fr|ecs]_annuel et _mois` (Sortie_Zone_C et Sortie_Batiment_C (2431, 2442, 2463, 2474), kWhef/m²/an et kWhef/m²)
- `O_Cef_elec_imp_[poste]_annuel et _mois (8 postes)` (Sortie_Zone_C et Sortie_Batiment_C (2432, 2443, 2464, 2475), kWhef/m²/an et kWhef/m²)
- `O_Cef_elec_cons_[poste]_annuel et _mois` (Sortie_Zone_C (2433, 2444), kWhef/m²/an et kWhef/m²)
- `O_Cef_elec_AC_[poste]_annuel` (Sortie_Batiment_C (nom RSEE ; le texte prévoit O_Cef_cons_[poste]_elec, 2465, 2476), kWhef/m²/an)
- `O_Cef_bois[buch|plaq|gran][poel|chaud]_imp_[ch|ecs]_annuel` (Sortie_Zone_C et Sortie_Batiment_C (2445, 2477), kWhef/m²/an)
- `O_Eef_Prod_PV_annuel, O_Eef_Prod_PV_AC_annuel, O_Eef_Prod_Coge_annuel, O_Eef_Prod_Coge_AC_annuel et _mois` (Sortie_Zone_C et Sortie_Batiment_C (2434 à 2437, 2448 à 2451, 2466 à 2469, 2480 à 2483), kWhef/m²/an et kWhef/m²)
- `O_Eef_Elec_Exportee_annuel ; O_Eef_Elec_Exportee_mois (zone) ; O_Eelec_Exportee_ef_mois (bâtiment)` (Sortie_Zone_C et Sortie_Batiment_C (2438, 2452, 2470, 2484), kWhef/m²/an et kWhef/m²)
- `O_TAC_elec_annuel, O_TAC_elec_PV_annuel, O_TAC_elec_Coge_annuel` (Sortie_Zone_C et Sortie_Batiment_C (2453 à 2455, 2485 à 2487), %)
- `O_TAC_Global_coge_annuel` (Sortie_Batiment_C (2456), %)
- `O_Type_Reseau, O_RatENR_rdch` (Sortie_Batiment_C (tableau 337), menu ; 0 à 1)
- `Usage, Nocc` (Sortie_Zone_C (entrées recopiées ; Nocc sert à 2553), menu ; occupants)
- `O_NbDegresHeures, O_NbDegresHeures_max` (Sortie_Groupe_D (entrée du forfait 2494 : DH_g et seuil haut), °C.h)
- `O_Cef_Ch_comb_bat, O_Cef_ECS_comb_bat` (Sortie_Batiment_C (Cef_ch_comb et Cef_ecs_comb de la cogénération, 2540), kWhef/m²/an)
- `O_E_Sol_bat, O_E_ef_aux_bat, O_E_Sol_zone, O_E_ef_aux_zone` (Sortie_Batiment_C, Sortie_Zone_C (solaire thermique, hors texte lu), kWh/m²/an)
- `vecteur_energie_principal_[ch|ecs|fr], generateur_principal_[ch|ecs|fr]` (Sortie_Batiment_C (hors texte lu ; valeurs 11, 0, 513, 510, 1502), codes)
- `O_Cep_Max, O_Cep_nr_Max, O_Mcgeo, O_Mccombles, O_Mcsurf_moy, O_Mcsurf_tot, O_Mccat, O_ProdRef, O_BilanBEPOS_max_1 à 4, O_McbilanBEPOS_1 à 3, O_Bilan_BEPOS_annuel_niv_1_2, O_Bilan_BEPOS_annuel_niv_3_4` (Sortie_Groupe_C, Sortie_Zone_C, Sortie_Batiment_C (hors annexe III : arrêté), kWhep/m²/an et coefficients)

## Points ouverts (à trancher au codage)

- Poste déplacement et parkings : le texte range l'éclairage des parkings dans ecl (2511) et leur ventilation dans auxvent (2512), le poste déplacement ne contenant que ascenseurs et escalators (2514). Le banc existant (README, parkings.py) constate que les RSEE les mettent dans O_Cef_imp_deplacement_annuel. À confirmer sur le RSEE 912ea : zone 1 déplacement 4,6 kWh/m², zone 4 3,4 kWh/m² alors que O_Cef_imp_ecl_annuel (1,8) égale O_Cef_ecl_annuel du groupe (1,8) : l'éclairage du parking (Pec_ins 1,74 kW, Ex = 1, 24 h/24, environ 15 200 kWh/an sur le projet) n'est pas dans ecl, donc bien dans déplacement. Banc : O_Cef_imp_deplacement_annuel - ascenseurs calculés = part parking de la zone.
- Répartition des parkings : le texte dit « au prorata des surfaces SRT des zones du bâtiment » (10.3.3.7, 10.4.1 « chaque zone des bâtiments »), parkings.du_projet répartit sur toutes les zones du projet. Deux bâtiments dans 912ea : comparer les deux lectures sur O_Cef_imp_deplacement_annuel des 4 zones après soustraction des ascenseurs (zone 3 : 8,8 kWh/m², zone 4 : 3,4).
- Forfait de refroidissement : les deux RSEE lus ne permettent pas de le bancer (groupes du logement tous Is_Climatise = 1 avec DH 735 à 1 236 ; bureaux Is_Climatise = 0 mais DH = 15,3 < 350). Banc à faire sur un RSEE avec Is_Climatise = 0 et O_NbDegresHeures > 350 : O_Cef_fr_annuel (groupe) doit valoir Coef x (min(DH, O_NbDegresHeures_max) - 350) x Coef_zone_alt / 2,3, et O_Cef_fr_mois doit rester nul. Vérifier aussi si le forfait entre dans O_Cef_elec_annuel du groupe (le texte dit oui, « élec tous postes »).
- Avec_Clim_Fictive (Simu) : le texte ne nomme pas ce champ. Il vaut 1 dans les deux RSEE, dont un sans groupe non climatisé. Hypothèse : il active la procédure 13.3 ; à vérifier sur un RSEE où il vaut 0 avec un groupe non climatisé et DH > 350 (O_Cef_fr_annuel devrait alors être nul).
- Simu.Mode vaut 3 dans les RSEE alors que le tableau 338 ne liste que 0 (Th-B), 4 (Th-D), 5 (Th-DBC) : la correspondance des codes de mode n'est pas dans le texte lu. Sans conséquence sur le calcul si l'on suppose un calcul complet Th-BCD.
- Groupe climatisé et DH : la fiche 13.5 calcule les DH des groupes climatisés comme s'ils ne l'étaient pas ; 912ea le confirme (DH 1 153 pour un groupe climatisé). Le forfait ne s'applique qu'aux non climatisés (page 1347).
- Qreq_gen_ch, Qreq_gen_fr (2500) servent de référence aux saisons par groupe sur 28 jours : OpenBCE décide aujourd'hui les saisons sur les besoins bruts aux bornes des émetteurs (saisons.Saisons). L'écart (pertes de distribution incluses) n'est pas mesurable sans le lot génération ; banc indirect : O_B_Ch_annuel et O_B_Fr_annuel du groupe.
- Besoins ECS : O_B_Ecs_annuel du groupe est à +0,35 % constant (README) ; (2421) dit « Qw_brut », donc besoins bruts : l'écart vient du lot ECS, pas de ce lot.
- Sous-décomposition bois (2445, 2477) : le texte somme des Wh sans diviser par SREF alors que l'unité est kWhef/m² ; retenir la division. Non bancable sur les deux RSEE (bois nul).
- E_elec_prod_PV_zn (2533 à 2535) : le texte définit la production PV au bâtiment seulement ; la clé de répartition vers les zones (prorata des consommations ou des surfaces) n'est pas écrite. Banc : O_Eef_Prod_PV_annuel des Sortie_Zone_C d'un RSEE avec PV, comparé à la valeur bâtiment x SREF_zn / SREF_bat et à un prorata des O_Cef_elec_cons.
- Production PV de parcelle (2526) : prorata des consommations horaires tous usages des bâtiments du projet ; impose une première passe sur tous les bâtiments avant les bilans. Non bancable ici (PV absent).
- Nom des sorties : le bâtiment publie O_Cef_elec_AC_[poste]_annuel et non O_Cef_cons_[poste]_elec (2465) ; dans un RSEE sans production ces champs valent 0 alors que cons = imp. Hypothèse : AC = cons - imp (autoconsommé). Banc : RSEE avec PV, comparer O_Cef_elec_AC_fr + O_Cef_elec_imp_fr à la zone O_Cef_elec_cons_fr.
- RatENR_rdfr : le tableau 337 fixe CoefEPnr réseau froid à 1, mais la nomenclature (page 1331) nomme O_RatENR_rdfr ; le champ est absent des deux RSEE (O_RatENR_rdch seul). Retenir 1 ; banc sur un RSEE raccordé à un réseau de froid : O_Cep_nr_annuel.
- Occupants pour O_Cep_annuel_occ : Nocc de la zone (entrée) ; vérifié sur les deux RSEE à 0,1 % près (1 134 contre 1 133,8 ; 790 contre 790,3), l'écart venant de l'arrondi de O_Cep_annuel. Pour un bâtiment, somme des Nocc de ses zones seulement.
- Ascenseurs, NB_z (2281) : le texte dit « nombre d'occupants conventionnels des locaux » (Nocc_l, max annuel), le banc existant retient les adultes équivalents, pas Zone.Nocc (21, 12, 12, 35) ; incohérence des constantes imprimées (Mpass 120 contre 75, Pveilleporte 75 contre 13, Tempec 13 contre 120) tranchée en faveur du texte de la page 1266. Cas non expliqués listés dans le README.
- Ascenseurs, cabines multizones (2297) : Timmob_n doit être la moyenne pondérée par Q_i / Q_z des durées de nuit des zones ; ascenseurs.cabine prend « habitation » si toutes les zones le sont. À corriger quand un ascenseur dessert logement et tertiaire ; sans effet sur les RSEE lus (C = « 1 2 », deux zones d'habitation).
- Ascenseurs, profil horaire (2306 à 2311) : non codé (ascenseurs.py donne l'annuel). La lecture de (2308) est incertaine (impression « 1/365 . Tmobh - Fmob(h) » sur « 24 Tmobh - 1 ») ; retenir la forme qui somme à 1 sur l'année : Fimob(h) = (1/365 - Fmob(h) Tmobh) / (24 - Tmobh) par jour. Nécessaire seulement pour O_Cef_elec_imp_deplacement_mois et pour l'autoconsommation PV ; banc : les douze valeurs de O_Cef_elec_imp_deplacement_mois.
- Escalators (fiche 10.2) et éclairage des parties communes (fiche 7.2, page 483) : entrées de (2511) et (2514) hors du lot ; aucun objet dans les RSEE lus. En logement collectif, O_Cef_imp_ecl_annuel de la zone (1,8) égale celui du groupe : l'éclairage des parties communes ne semble pas ajouté dans ce RSEE, ou vaut 0 ; à examiner sur d'autres RSEE (champ d'entrée à identifier).
- Parkings : IsParamVentilationDefaut « = 0 » active les défauts selon le texte (page 1287), parkings.py lit 1 ; de même IsParamEclPuisDefaut et IsParamEclHdDefaut. Le RSEE 912ea a IsParamEclPuisDefaut = 0 avec Pec_ins saisi 1,74 kW, cohérent avec « 1 = défaut ». Banc : O_Cef_imp_deplacement_annuel avec les deux lectures.
- Parkings : Pec_ins est en kW dans le RSEE (1,74 pour 58 places, soit 30 W/place) alors que le texte le donne en W ; parkings.py multiplie par 1000.
- Parkings, PlagDse « 0 24 » avec IsParamEclHdDefaut = 0 : lecture de parkings.py (détection sur toute la journée, abattement 0,2). Si la lecture inverse (0 = défaut, pas de détection) était la bonne, l'éclairage serait 5 fois plus élevé : le banc sur O_Cef_imp_deplacement_annuel tranche.
- Tableau 324 (Rmvtpl, page 1288) : image à cellules fusionnées, valeurs reconstituées dans parkings.RMVTPL ; non bancable sur 912ea (Vent = 0).
- Mobilier (4.7) : « égal aux apports internes de chaleur non dus aux occupants » ; en logement les scénarios donnent des apports par m² de surface habitable ; vérifier sur O_Cef_imp_mobilier_annuel (24,8 en logement collectif, 28,7 en bureaux) que la série Scenario.apports_usages sommée et divisée par SREF les reproduit.
- O_B_Ecl_annuel et O_B_Ecl_mois existent au groupe dans les RSEE sans figurer dans le texte de 13.2 : égaux à O_Cef_ecl_annuel (1,8 et 7,2) dans les deux RSEE.
- Unités : les équations (2417) et suivantes divisent des Wh par des m² et annoncent des kWh/m² ; la division par 1000 est implicite partout.
- Page 1342 de la fiche 13.2 est vide dans le texte (fin de fiche ou figure non extraite) ; Figure 214 (page 1344, schéma de la procédure forfait) et Figure 211 (page 1297, séquence de saisie des parkings) sont des images sans contenu calculatoire. Tableau 342 (page 1352) est partiellement lisible (en-têtes seuls). Tableau 327 (page 1295) et tableau 318 (pages 1268 et 1269) sont lisibles mais éclatés sur plusieurs lignes.

## Tableaux en image dans le PDF

- Tableau 324 (page 1288) : Rmvtpl par heure légale et typeusage, cellules fusionnées, colonnes 8 à 24 illisibles sans l'image ; valeurs reconstituées dans parkings.RMVTPL
- Figure 214 (page 1344) : schéma de principe de la procédure forfait de refroidissement (image, texte épars)
- Figure 211 (page 1297) : séquence logique de saisie des paramètres parkings (image)
- Tableau 342 (page 1352) : matrice Qcef(poste ; énergie), seuls les en-têtes 10 à 60 et 1 à 3 sont lisibles
- Page 1342 (fiche 13.2) : page sans texte extrait
- Tableau 318 (pages 1268 et 1269) : spectre de charge, lisible mais éclaté sur deux pages
- Tableau 327 (page 1295) : Fhext(h), lisible mais chiffres coupés (« 0,7 9 » pour 0,79)
- Tableau 310 (pages 1262 à 1265) : nomenclature des ascenseurs avec constantes contredites par le texte (Mpass 120, Pveilleporte 75, Tempec 13)

## Estimation

Environ 500 lignes de Python : bilans.py 220 lignes (BilanGroupe, BilanZone, BilanBatiment, production et imports, 2498 à 2542), sorties_c.py 180 lignes (2413 à 2493 avec les noms XML des RSEE et les séries mensuelles), forfait_froid.py 40 lignes (2494 à 2497, tableaux 339 et 340, zone climatique depuis le département via meteo ou banc.besoins.zone_climatique), mobilier 15 lignes (93 à 95), ascenseurs : 40 lignes à ajouter pour le profil horaire (2306 à 2311) et la correction (2297), banc/sorties_c.py 100 lignes. Difficulté faible pour l'agrégation (sommes, prorata, coefficients fixes) ; les contrôles internes des RSEE (Cep = 2,3 x Cef élec, zone = groupes + déplacement, Cep_occ) passent déjà à l'arrondi près. Difficulté moyenne sur trois points : l'ordre des segments des noms XML qui diffère du texte et entre niveaux (imp avant ou après l'énergie, auxv et auxs, elec_AC au bâtiment), la double passe projet pour le PV de parcelle, et le forfait de refroidissement qui exige un RSEE de banc avec un groupe non climatisé en inconfort (aucun des deux lus). La valeur des sorties ch, fr, ecs et auxdist dépend entièrement des lots génération et distribution (chapitres 8 et 9) : sans eux, le banc de ce lot se limite aux postes ecl, auxvent, déplacement, mobilier, aux besoins et aux identités d'agrégation, ce qui suffit à valider toute la couche 13.2 et 13.4.
