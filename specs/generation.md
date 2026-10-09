# Spécification : Assemblage, gestion et calculs de la génération

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille « assemblage, gestion et calculs de la génération » : fiches 8.14 (S1_Syst_Assemblage de la génération, pages 605 à 610), 8.17 (C_GEN_Gestion/régulation de la génération, pages 631 à 667), 8.29 (C_GEN_Calculs génération, pages 918 à 939) et 8.4 (C_Ein_Détermination des saisons de fonctionnement des systèmes, pages 530 à 534).

Couvert :
- Saisons effectives de la génération, des groupes desservis, des réseaux intergroupes et des CTA (8.4, équations 840 à 844), calcul journalier à IHJ(h) = 1, mode Th-C seulement.
- Contrôles de cohérence du montage (981 à 988), liste des types de générateurs (tableau 112), ratios surfaciques de répartition des pertes (989 à 993).
- Calculs préliminaires horaires : demandes totales sans report (994 à 996), ratios de besoins par distribution et par groupe (997 à 1005), indicateurs de relance et d'activation ECS (1006 à 1008), température d'ambiance de la génération (règle non numérotée page 648), température amont (1009), températures de fonctionnement aval (1010 à 1014), demandes avec report (1015 à 1017).
- Les trois modes de régulation des générateurs instantanés : sans priorité (1018 à 1029), cascade (1030 à 1035), alternance monoposte froid, ECS, chauffage et biposte chauffage + ECS (1036 à 1053), avec le report Qrest d'un générateur au suivant et le report Qrep d'une heure à l'autre, le ratio de puissance disponible Rpui_dispo, les indicateurs ia_refroidi, iecs_seule, iecs_fonction, Rfonct_ecs, le compteur de basculement Nbasculement.
- Imputation des auxiliaires amont à la matrice Qcef (1054 à 1056), post-traitement (1057 à 1059 : matrice Qcef de la génération, réchauffeur de boucle ECS, pertes récupérables Φvc_tot, production électrique), indicateurs de sous-dimensionnement (1060 à 1065).
- Fiche 8.29 : coefficients d'énergie primaire (tableau 252), structure 3 x 6 de la matrice Qcef (tableau 253), répartition par groupe (1485 à 1492), électricité produite (1493 à 1494, 1516 à 1520), cumuls mensuels et annuels par poste, par générateur, par génération et par groupe en énergie finale et primaire (1495 à 1515), bilan solaire (1521), Qfou_3postes (1522), histogrammes d'heures par taux de charge Nbhcharge (1523 à 1525), rendements annuels (1526 à 1527), auxiliaires (1528 à 1529), cumuls par énergie (1530 à 1569).

Hors champ, et pourquoi :
- Le comportement interne de chaque générateur (fonction AppelGenerateur : fiches 8.18 effet joule, 8.19 chaudières, 8.20 et suivantes PAC, réseaux, cogénération) : la gestion ne fait qu'appeler ce composant et agréger ses sorties. La spécification définit seulement l'interface d'appel (entrées : θamont, θaval, Qreq, idfonction, Rpui_dispo, iecs_seule ; sorties : Qcef(po;en), Qcons, Qfou, τcharge, Φvc, Waux,pro, Qrest, ηeff, Qprelec, Φrejet, Rfonct_ecs).
- Les sous-assemblages à ballon(s) de stockage (fiches S2_GEN_ballon, nœuds Production_Stockage et leurs Source_Ballon_Base / Appoint) : ils sont vus par la gestion comme le premier générateur d'une cascade et pilotent eux-mêmes base et appoint ; seule leur place dans la cascade et l'ajout de Φvc_sto sont spécifiés ici.
- Les sources amont (fiche C_Gen_Sources amont, nœud Source_Amont) : seules les fonctions CalculTempAmont (1009) et CalculAuxAmont (1054) sont appelées ; leur contenu est une autre famille.
- Transferts sur boucle d'eau (8.15) et transferts entre locaux par DRV et thermofrigopompes (8.16) : seuls les points d'insertion dans l'algorithme (ensemble GBE, note de la page 655) sont relevés.
- Les distributions intergroupes (8.10 à 8.12) qui fournissent Qsys, θmoy, θmax, Adess, idrelance, idencl : traitées comme des entrées.
- Les conditions d'exigence (Cep, Cep,nr) et la conversion finale en kWh/m² : chapitre Calculs groupe / bâtiment, déjà amorcé dans consommation.py.

## Entrées (RSEE)

- `Generation (Batiment > ... > Generation_Collection)` / `Index` : indice gen ; cible des Id_Gen des distributions ; entier ; valeurs vues : 1 à 6
- `Generation` / `Type_Priorite` : idtype_priorite_gen (tableau 111 p.636) ; entier 1 à 3 ; valeurs vues : 1 (sans priorité : sèche-serviettes, PAC seule) ; 2 (cascade : génération avec Production_Stockage)
- `Generation` / `Idraccord_Gnr` : idraccord_gnr_gen (0 permanent, 1 avec isolement, p.636) ; aucune équation ne l'exploite dans 8.17 ; entier 0/1 ; valeurs vues : 1 partout
- `Generation` / `Idraccord_Reseau_Gen` : idraccord_reseau_gen de la fiche 8.4 (0 avec isolement, 1 permanent, p.531). Attention : le code 0 vaut « isolement » ici alors que banc/cep.py applique l'union (raccordement permanent) ; voir points ouverts ; entier 0/1 ; valeurs vues : 0 partout
- `Generation` / `Pos_Gen` : idpos_gen (p.636) ; entier 0/1 ; valeurs vues : 0 (hors volume chauffé) ; 1 (sèche-serviettes en volume chauffé)
- `Generation` / `Id_Bat` : indice bat du bâtiment où se trouve la génération (989) ; entier ; valeurs vues : 0 si hors volume ; 1 ou 2 sinon
- `Generation` / `Id_Et` : espace tampon abritant la génération, donne btherm(h) (p.648) ; entier ; valeurs vues : 0
- `Generation` / `Type_Gestion_Chaud_Gen` : idgestion_ch_gen (1 température constante, 2 température des réseaux) ; entier 1/2 ; valeurs vues : 2
- `Generation` / `Theta_Wm_Ch` : θwm_ch_gen (1010, 1011) ; réel °C ; valeurs vues : 70
- `Generation` / `Type_Gestion_Froid_Gen` : idgestion_fr_gen ; entier 1/2 ; valeurs vues : 2
- `Generation` / `Theta_Wm_Fr` : θwm_fr_gen (1012) ; réel °C ; valeurs vues : 7
- `Generation` / `Theta_Wm_Ecs` : θwm_ecs_gen (1010, 986) ; réel °C ; valeurs vues : 50, 54
- `Generation > Generateur_Collection > Generateur_Effet_Joule / Generateur_Thermodynamique_Elec_NonReversible / ...` / `Index, Rdim, Pmax (effet joule), Id_Fou_Gen ou Id_FouGen_Mod, Idpriorite_Ch, Idpriorite_Fr, Idpriorite_Ecs, Id_Source_Amont, Id_Groupe, Sys_Thermo_Ch/Fr/Ecs, Theta_Max_Av, Theta_Min_Av, Theta_Min_Am, Theta_Max_Am` : Ratdim_gnr (Rdim), Pngen_ch_gnr et Pngen_fr_gnr (Pmax ou matrices Performance des PAC), idfougen_gnr (Id_Fou_Gen), idpriorite_ch/fr/ecs_gnr, idtype_gnr (déduit du nom du nœud : Generateur_Effet_Joule = 500, Generateur_Thermodynamique_Elec_* = 503), θmin_gnr et θmax_gnr (Theta_Min_Av, Theta_Max_Av) ; idfluide_aval_gnr non lu dans les RSEE, à déduire du type ; entiers et réels ; valeurs vues : Rdim = 1 ; Pmax = 100 W (sèche-serviettes) ; Id_Fou_Gen = 1 ; Idpriorite_* = 0 en mode sans priorité ; Id_Groupe = 0 ; Theta_Max_Av = 32
- `Generation > Production_Stockage_ECS_Collection > Production_Stockage` / `Index, Id_Fou_Sto, Idpriorite_Ch, Idpriorite_Ecs, nb_assembl, V_tot, Theta_Cons, Pw_circ_prim_ECS, Pw_circ_prim_RB, Source_Ballon_Base_Collection, Source_Ballon_Appoint_Collection` : sous-assemblage ballon placé en tête de cascade (p.651) ; idfou_sto_BS (8.29 p.920) ; Φvc_sto (1059) ; entiers et réels ; valeurs vues : Id_Fou_Sto = 3 ; Idpriorite_Ecs = 1 ; Idpriorite_Ch = 1 ; nb_assembl = 28 (un ballon par logement) ou 1
- `Production_Stockage > Source_Ballon_Base_Collection > Source_Ballon_Base_Thermodynamique_Elec_TripleService (ou _Effet_Joule)` / `Index, Rdim, Id_Source_Amont, Idpriorite_Ch/Fr/Ecs, Sys_Thermo_ts, Val_Cop_Ch/Fr/Ecs, Val_Pabs_Ch/Fr/Ecs, Theta_Max_Av_Ch/Ecs, Theta_Min_Am_Ch/Ecs, LRcontmin_Ch, Pmax (effet joule), Id_Fou_Gen` : générateur base du ballon : Pngen = Val_Pabs x Val_Cop (en kW, à convertir en W) ; type 503 ; participe aussi au chauffage instantané si idfougen = 4 (p.645) ; réels et entiers ; valeurs vues : Val_Cop_Ch 4,15 ; Val_Pabs_Ch 1,42 kW ; Val_Cop_Ecs 3,5 ; Theta_Max_Av_Ch 20 ; Pmax 2 kW (base effet joule) ou 1,5 kW (appoint)
- `Production_Stockage > Source_Ballon_Appoint_Collection > Source_Ballon_Appoint_Effet_Joule` / `Index, Rdim, Pmax, Idpriorite_Ch, Idpriorite_Ecs, Id_Fou_Gen` : générateur appoint du ballon, type 500/502, idfougen = 3 ; réels et entiers ; valeurs vues : Pmax 1,5 ; Id_Fou_Gen 3
- `Generation > Source_Amont_Collection > Source_Amont` / `Index, Id_Fl_Amont, Source_Amont_Air, Source_Amont_Eau, Id_Et, Tair_Lim, Ppompes_*, Pvent_Tour, Theta_Min_Boucle, Theta_Max_Boucle, Theta_Min_Source, Theta_Max_Source` : SA : θamont_SA(h) (1009), Waux,am (1054), θboucle_min et θboucle_max (987, 988) ; entiers et réels ; valeurs vues : Id_Fl_Amont 2 ; Source_Amont_Air 1 ; tout le reste 0 (PAC air)
- `Zone > Distribution_Intergroupe_Chaud / _Froid` / `Index, Id_Gen, Type_Prim, Id_Et, Umoyen_Vc_Prim_Ch, Lvc_Prim, Lhvc_Prim, Gest_Circ_Prim_Ch, Pcirc_Prim_Ch` : dp → gen par Id_Gen ; idfonction_dp = 1 (Chaud) ou 2 (Froid) selon le nœud ; idtype_dp (0 fictif, 1 hydraulique) non lu directement : à déduire de Type_Prim ou du fluide aval des générateurs (point ouvert) ; θmax_ch_dp, θmoy_dp(h), Qsys_ch_dp(h), Adess_ch_dp, idrelance_dp, Ratbes_ch_dp,gr(h), θi,aval,eq_dp(h) sont des sorties de la fiche 8.10 et 8.11 ; entiers et réels ; valeurs vues : Id_Gen 1 ou 6 ; Type_Prim 0 ; longueurs 0 (réseau fictif ou très court)
- `Zone > Distribution_Intergroupe_ECS` / `Index, Id_Gen, Type_Reseau_Intergroupe_ECS, Is_Rechauf_Bcl_e, p_circ_prim_e, type_gest_circ_e, l_vc_prim_bcl_e, l_hvc_prim_bcl_e, u_prim_e, Id_PCAD, Id_Et` : dp-e → gen ; idfonction_dp = 3 ; Wrechauff-e_dp-e(h) (1058, nul si Is_Rechauf_Bcl_e = 0) ; Qsys_ecs_dp-e(h), θmoy_dp-e, Adess_ecs_dp-e, idencl_dp-e(j) issus du chapitre 9 ; entiers et réels ; valeurs vues : Id_Gen 1 ou 5 ; Is_Rechauf_Bcl_e 0 ; type réseau 0
- `Groupe` / `SHAB ou SU, Index, Is_Climatise` : Agr (989), iclim_gr (840) ; réels et entiers ; valeurs vues : déjà lus par groupe.py
- `Groupe (par l'intermédiaire de ses distributions Distribution_Chaud / Distribution_ECS raccordées aux intergroupes)` / `liaison groupe → dp (Id de la distribution intergroupe dans le nœud de distribution du groupe)` : iddesservi_ch_gen,gr, iddesservi_fr_gen,gr (8.4, variables internes p.531) : 1 si une chaîne groupe → distribution → intergroupe → génération existe ; entier ; valeurs vues : non relevé dans cette lecture
- `Batiment > Espace_Tampon` / `b (coefficient de réduction)` : btherm(h) pour θamb hors volume chauffé (p.648) ; réel ; valeurs vues : déjà calculé par enveloppe.coefficients_b
- `Climat` / `te` : θext(h) ; série horaire ; valeurs vues : climat.te
- `Calendrier` / `case (heure légale), mois` : IHJ(h) = 1 (début de jour, 8.4 p.533), Imois (iecs_fonction p.653) ; série horaire ; valeurs vues : cal.case

## Paramètres conventionnels

- θamb_ch, température d'ambiance intérieure conventionnelle quand un générateur est sollicité en chauffage = 20 °C (p. 641 (tableau 111, constantes))
- θamb_fr, température d'ambiance conventionnelle en refroidissement = 26 °C (p. 641)
- θamb en période mixte (Autch = Autfr) en volume chauffé = (20 + 26) / 2 = 23 °C (p. 648)
- Nbasculement_init_gen, nombre d'heures de non-utilisation provoquant la coupure d'un générateur en mode alterné = 20 h (valeur conventionnelle du tableau 111) (p. 636)
- Seuil de sous-dimensionnement court terme = Nbsousdim > 6 heures successives (p. 666, 667 (1061, 1064))
- Seuil de sous-dimensionnement long terme (critique) = Nbsousdim > 72 heures successives (p. 666, 667 (1062, 1065))
- Mois de fonctionnement d'un générateur ECS hivernal (ihivernal = 1) = Imois dans {1, 2, 3, 4, 5, 10, 11, 12} (p. 653, 656, 661)
- Mois de fonctionnement d'un générateur ECS estival (ihivernal = 2) = Imois dans {5, 6, 7, 8, 9, 10} (mai et octobre communs aux deux) (p. 653)
- Coefep(10 gaz), Coefep(20 fioul), Coefep(40 bois) = 1 (ef → ep) ; colonne 2 du tableau 252 également 1 (p. 925 (tableau 252))
- Coefep(50 électricité) = 2,3 (p. 925)
- Coefep(60 réseau) = 1 ; seconde colonne : 1 - RatENR_rdch pour les réseaux de chaleur, 1 pour les réseaux de froid (p. 925)
- Codes énergie de la matrice Qcef (colonnes) = 10 gaz, 20 fioul, 30 charbon, 40 bois, 50 électricité, 60 réseau (p. 925 (tableau 253))
- Codes poste de la matrice Qcef (lignes) = 1 chauffage, 2 refroidissement, 3 ECS (p. 925)
- Codes idfougen = 1 chauffage, 2 refroidissement, 3 ECS, 4 chauffage + ECS, 5 chauffage + refroidissement (p. 635)
- Codes idtype_gnr (tableau 112) = 100 à 109 gaz, 200 et 201 fioul, 400 bois, 403 poêle, 404 insert, 500 effet joule, 501 ECS élec. direct, 502 ballon élec., 503 PAC compression, 504 PAC absorption, 507 PAC boucle d'eau, 508 thermofrigopompe, 509 DRV, 600 réseau de chaleur, 601 réseau de froid, 700 cogénération ; générateurs thermodynamiques : 503 à 509 (p. 643, 644)
- Classes de taux de charge des sorties pédagogiques = HF (hors plage de fonctionnement), 0, ]0 ; 10 %], ]10 ; 20 %] ... ]90 ; 100 %] (p. 921, 922, 933 à 935)

## Équations

- (840, p. 533) Aut_ch_gen(j) = MAX_gr( iddesservi_ch_gen,gr x Aut_ch,pro_gr(j) ) ; Aut_fr_gen(j) = MAX_gr( iddesservi_fr_gen,gr x iclim_gr x Aut_fr,pro_gr(j) ) ; Aut_pro_gr : saisons propres du groupe (fiche 4.6, Besoins.saison) ; iddesservi : 1 si le groupe est relié à la génération par une distribution intergroupe (émission ou CTA) ; Calcul journalier à IHJ(h) = 1, Th-C seulement. Les groupes non climatisés ne comptent pas en froid. Équation reconstituée : le texte extrait est illisible (symboles dispersés), page 533
- (841, p. 533) Si MAX_gen( iddesservi_gen,gr x idraccord_reseau_gen ) > 0 : Aut_ch,eff_gr(j) = MAX_gen( iddesservi_ch_gen,gr x idraccord_reseau_gen x Aut_ch_gen(j) ) ; Aut_fr,eff_gr(j) = MAX_gen( iddesservi_fr_gen,gr x idraccord_reseau_gen x Aut_fr_gen(j) ) ; idraccord_reseau_gen : 1 raccordement permanent, 0 isolement (Idraccord_Reseau_Gen) ; Groupe desservi par au moins une génération à raccordement permanent. Reconstituée (page 533)
- (842, p. 534) Sinon : Aut_ch,eff_gr(j) = Aut_ch,pro_gr(j) ; Aut_fr,eff_gr(j) = Aut_fr,pro_gr(j) ;  ; Groupe indépendant (toutes ses générations sont avec isolement)
- (843, p. 534) Aut_ch,eff_dp(j) = MAX_{gr ∈ dp}( Aut_ch,eff_gr(j) ) ; Aut_fr,eff_dp(j) = MAX_{gr ∈ dp}( Aut_fr,eff_gr(j) ) ; dp : réseau intergroupe ; Reconstituée (page 534)
- (844, p. 534) Aut_ch,eff_CTA(j) = MAX_{gr ∈ CTA}( Aut_ch,eff_gr(j) ) ; Aut_fr,eff_CTA(j) = MAX_{gr ∈ CTA}( Aut_fr,eff_gr(j) ) ;  ; Reconstituée (page 534)
- (981, p. 642) θdist_ch_max_gen = max_{dp → gen, idfonction_dp = 1}( θmax_ch_dp ) ; θmax_ch_dp : température maximale de la distribution intergroupe de chauffage ; Distributions hydrauliques seulement ; calcul unique
- (982, p. 643) θdist_fr_max_gen = max_{dp → gen, idfonction_dp = 2}( θmax_fr_dp ) ; la nomenclature nomme la même grandeur θdist_fr_min_gen (p.1340) : il s'agit de la température minimale des réseaux de froid ; 
- (983, p. 643) θdist_ecs_max_gen = max_{dp-e → gen, idfonction_dp = 3}( θmax_ecs_dp-e ) ;  ; 
- (984, p. 643) Pour chaque générateur de chauffage (idfougen ∈ {1, 4, 5}) sur fluide aval eau (idfluide_aval ≠ 2) : si idgestion_ch_gen = 1 : θmax_gnr ≥ θwm_ch_gen et θdist_ch_max_gen ≤ θwm_ch_gen ; si idgestion_ch_gen = 2 : θmax_gnr ≥ θdist_ch_max_gen ; θmax_gnr : Theta_Max_Av ; Contrôle de cohérence, pas de calcul
- (985, p. 643) Pour chaque générateur de refroidissement (idfougen ∈ {2, 5}), fluide aval eau : si idgestion_fr_gen = 1 : θmax_gnr ≥ θwm_fr_gen et θdist_fr_max_gen ≤ θwm_fr_gen ; si idgestion = 2 : θmax_gnr ≥ θdist_fr_max_gen ;  ; Le texte écrit « idgestion_ch » dans la seconde branche : lire idgestion_fr. En froid, la logique physique voudrait θmin_gnr ≤ θdist_fr_min ; le texte est recopié tel quel
- (986, p. 643) Pour chaque générateur d'ECS (idfougen ∈ {3, 4}) : θmax_gnr ≥ θwm_ecs_gen et θdist_ecs_max_gen ≤ θwm_ecs_gen ;  ; 
- (987, p. 643) Boucle d'eau, générateur de chauffage desservant la boucle : θmin_gnr ≥ θboucle_max ; θboucle_max : Theta_Max_Boucle de la Source_Amont ; Génération contenant une boucle d'eau
- (988, p. 643) Boucle d'eau, générateur de refroidissement desservant la boucle : θmin_gnr ≤ θboucle_min ;  ; 
- (989, p. 644) Ratsurf_gen,gr = A_gr / Σ_{gr* → gen, gr* ∈ bat} A_gr* ; A_gr : surface du groupe (SHAB ou SU) ; bat : bâtiment où est la génération (Id_Bat) ; Si le groupe gr appartient au bâtiment bat et que la génération est en volume chauffé ; calcul unique
- (990, p. 644) Sinon Ratsurf_gen,gr = 0 ;  ; 
- (991, p. 644) Ratsurf_dess_ch_dp = Adess_ch_dp / Σ_{dp ← gen} Adess_ch_dp ; Adess_ch_dp : surface desservie par la distribution intergroupe en chauffage ; Calcul unique
- (992, p. 644) Ratsurf_dess_fr_dp = Adess_fr_dp / Σ_{dp ← gen} Adess_fr_dp ;  ; 
- (993, p. 645) Ratsurf_dess_ecs_dp-e = Adess_ecs_dp-e / Σ_{dp-e ← gen} Adess_ecs_dp-e ;  ; 
- (994, p. 646) Qreq_tot_sr_ch_gen(h) = Σ_{dp ∈ gen} Qsys_ch_dp(h) ; Qsys_ch_dp : besoins de chauffage augmentés des pertes de distribution intergroupe (et des CTA) ; Chaque heure, après remise à zéro du jeu de données de chaque générateur (figure 111 p.646)
- (995, p. 646) Qreq_tot_sr_fr_gen(h) = - Σ_{dp ∈ gen} Qsys_fr_dp(h) ; Qsys_fr_dp négatif en froid ; la demande de froid de la génération est positive ; 
- (996, p. 646) Qreq_tot_sr_ecs_gen(h) = Σ_{dp-e ∈ gen} Qsys_ecs_dp-e(h) ;  ; 
- (997, p. 646, 647) Si Qreq_tot_sr_ch_gen(h) > 0 : Ratbes_ch_gen,dp(h) = Qsys_ch_dp(h) / Qreq_tot_sr_ch_gen(h) ; sinon Ratbes_ch_gen,dp(h) = Ratsurf_dess_ch_dp ;  ; 
- (998, p. 647) Si Qreq_tot_sr_fr_gen(h) > 0 : Ratbes_fr_gen,dp(h) = - Qsys_fr_dp(h) / Qreq_tot_sr_fr_gen(h) ; sinon Ratsurf_dess_fr_dp ;  ; 
- (999, p. 647) Si Qreq_tot_sr_ecs_gen(h) > 0 : Ratbes_ecs_gen,dp-e(h) = Qsys_ecs_dp-e(h) / Qreq_tot_sr_ecs_gen(h) ; sinon Ratsurf_dess_ecs_dp-e ;  ; 
- (1000, p. 647) Ratbes_ch_gen,gr(h) = Σ_{dp → gr} Ratbes_ch_gen,dp(h) x Ratbes_ch_dp,gr(h) ; Ratbes_ch_dp,gr : part du groupe dans les besoins du réseau (sortie de la distribution intergroupe) ; 
- (1001, p. 647) Ratbes_fr_gen,gr(h) = Σ_{dp → gr} Ratbes_fr_gen,dp(h) x Ratbes_fr_dp,gr(h) ;  ; 
- (1002, p. 647) Ratbes_ecs_gen,gr(h) = Σ_{dp-e → gr} Ratbes_ecs_gen,dp-e(h) x Ratbes_ecs_dp-e,gr(h) ;  ; 
- (1003, p. 647) Qreq,ch_gen,gr(h) = Qreq_tot_sr_ch_gen(h) x Ratbes_ch_gen,gr(h) ;  ; Demande sans report, transmise aux calculs groupe et aux transferts boucle d'eau
- (1004, p. 647) Qreq,fr_gen,gr(h) = Qreq_tot_sr_fr_gen(h) x Ratbes_fr_gen,gr(h) ;  ; 
- (1005, p. 647) Qreq,ecs_gen,gr(h) = Qreq_tot_sr_ecs_gen(h) x Ratbes_ecs_gen,gr(h) ;  ; 
- (1006, p. 647) idrelance_ch_gen(h) = max_{dp → gen, idfonction_dp = 1}( idrelance_dp(h) ) ; idrelance_dp : période de relance du réseau (fiche 8.11, issue de 8.5) ; 
- (1007, p. 648) idrelance_fr_gen(h) = max_{dp → gen, idfonction_dp = 2}( idrelance_dp(h) ) ;  ; 
- (règle p.648 (non numérotée), p. 648) Si idtype_priorite_gen = 2 (cascade) et idrelance_ch_gen(h) = vrai : la chaleur fournie Qfou et la consommation Qcef(1;en) du générateur dont idpriorite_ch_gnr est le plus élevé ne sont pas prises en compte au pas h ;  ; Formulation ambiguë (« le générateur avec idrelance le plus élevé »). Voir points ouverts
- (1008, p. 648) idencl_gen(j) = max_{dp-e → gen, idfonction_dp = 3}( idencl_dp-e(j) ) ; idencl_dp-e : jour inclus dans la période de fonctionnement du réseau ECS ; 
- (θamb (p.648, non numérotée), p. 648) Si idpos_gen = 1 : θamb(h) = θamb_ch si Autch_gen(j) = 1 et Autfr_gen(j) = 0 ; θamb_fr si Autch = 0 et Autfr = 1 ; (θamb_ch + θamb_fr)/2 sinon. Si idpos_gen = 0 : θamb(h) = btherm(h) x θext(h) + (1 - btherm(h)) x [même valeur conventionnelle que ci-dessus] ; btherm : coefficient b de l'espace tampon (1 si à l'extérieur) ; Sert aux pertes des générateurs à combustion
- (1009, p. 648, 649) θamont_SA(h) = CalculTempAmont( Φrejet_gnr(h-1) ) ; pour tout gnr relié à SA : θamont_gnr(h) = θamont_SA(h) ; Φrejet(h-1) : rejets des générateurs au pas précédent (état conservé) ; Générateurs thermodynamiques (types 503 à 509) ; une fois par source amont
- (1010, p. 649) θaval_ecs_gen(h) = θwm_ecs_gen ; le texte écrit θaval_ch = θwm_ch sous le titre ECS instantanée : lire θaval_ecs = θwm_ecs ; Production ECS instantanée
- (1011, p. 649, 650) Chauffage, réseaux hydrauliques : si idgestion_ch_gen = 1 : θaval_ch_gen(h) = θwm_ch_gen ; sinon si idrelance_ch_gen(h) = 1 : θaval_ch_gen(h) = θdist_ch_max_gen ; sinon si Qreq_tot_sr_ch(h) = 0 et Qreq_tot_ar_ch(h) > 0 : θaval_ch_gen(h) = θaval_ch_gen(h-1) ; sinon θaval_ch_gen(h) = max_{dp → gen, idfonction_dp = 1}( θmoy_dp(h) ) ; θmoy_dp(h) : température moyenne du réseau (fiche 8.11) ; idtype_dp = 1 ; θaval_ch(h-1) est un état conservé
- (1012, p. 650) Refroidissement, réseaux hydrauliques : si idgestion_fr_gen = 1 : θaval_fr_gen(h) = θwm_fr_gen ; sinon si idrelance_fr_gen(h) = 1 : θaval_fr_gen(h) = θdist_fr_max_gen ; sinon si Qreq_tot_sr_fr = 0 et Qreq_tot_ar_fr > 0 : θaval_fr_gen(h-1) ; sinon max_{dp → gen, idfonction_dp = 2}( θmoy_dp(h) ) ;  ; Le texte écrit idfonction_dp = 1 dans la dernière branche : lire 2. En froid un max de températures moyennes est contre-intuitif (voir points ouverts)
- (1013, p. 650) Chauffage, réseaux fictifs (idtype_dp = 0) : θaval_ch_gen(h) = Σ_{dp → gen, idfonction_dp = 1} Ratbes_ch_gen,dp(h) x θi,aval,eq_dp(h) ; θi,aval,eq_dp : température d'air équivalente vue par la distribution (air ambiant ou batterie de CTA) ; Génération sur air
- (1014, p. 650) Refroidissement, réseaux fictifs : θaval_fr_gen(h) = Σ_{dp → gen, idfonction_dp = 2} Ratbes_fr_gen,dp(h) x θi,aval,eq_dp(h) ;  ; 
- (1015, p. 651) Qreq_tot_ar_ch_gen(h) = Qreq_tot_sr_ch_gen(h) + Qrep_ch_gen(h-1) ; Qrep_ch(h-1) : énergie reportée de l'heure précédente (état) ; 
- (1016, p. 651) Qreq_tot_ar_fr_gen(h) = Qreq_tot_sr_fr_gen(h) + Qrep_fr_gen(h-1) ;  ; 
- (1017, p. 651) Qreq_tot_ar_ecs_gen(h) = Qreq_tot_sr_ecs_gen(h) + Qrep_ecs_gen(h-1) ; Report ECS seulement pour un générateur instantané ; 
- (1018, p. 652) Pngen_tot_[po] = Σ_{gnr ∈ G[po]} Rdim_gnr x Pngen_[po]_gnr ; Rdim : nombre de générateurs identiques ; G[po] : ensemble des générateurs instantanés du poste ; Mode sans priorité (idtype_priorite_gen = 1), début de simulation
- (1019, p. 652) Ratpngen_[po]_gnr = Rdim_gnr x Pngen_[po]_gnr / Pngen_tot_[po] ;  ; 
- (1020, p. 652) ETAPE 2 ECS : idfonction_gnr = 3 ; générateurs désactivés si idencl_gen(j) ≠ 1 ;  ; Sans priorité
- (1021, p. 653) Qreq = [1 - ia_refroidi_gnr(h)] x Ratpngen_ecs_gnr / Σ_{gnrk ∈ Gecs} ([1 - ia_refroidi_gnrk(h)] x Ratpngen_ecs_gnrk) x Qreq_tot_ar_ecs_gen(h) ; ia_refroidi : générateur déjà appelé en froid au pas h (ordre d'appel : froid, ECS, chauffage, figure 110) ; Pour chaque gnr ∈ Gecs
- (1022, p. 653) Qrest = 0 ;  ; 
- (règle ECS p.653 (non numérotée), p. 653) Si ia_refroidi_gnr(h) ≠ 1 : iecs_seule = 1 si idfougen_gnr = 3 ou Autch_gen(j) = 0, sinon 0 ; iecs_fonction_gnr = 1 si ihivernal_gnr = 0, ou (ihivernal = 1 et Imois ∈ {1..5, 10..12}), ou (ihivernal = 2 et Imois ∈ {5..10}) ; si (Qreq_ecs_gen,gr(h) > 0 ou iecs_seule = 1) et iecs_fonction = 1 : Rpui_dispo = 1 ; [Qcef(3;en), Qcons, Qfou, τcharge, Φvc, Waux,pro, Qrest, ηeff, Qprelec, Φrejet, Rfonct_ecs] = AppelGenerateur(θamont_gnr(h), θaval_ecs_gen(h), Qreq, Rpui_dispo, idfonction = 3, iecs_seule) ; puis Qcef(3;en)_gnr(h) += Qcef(3;en) ; Qcons_gnr += Qcons ; Qfou_ecs_gnr += Qfou ; Qprelec_gnr += Qprelec ; τcharge_gnr += Rpui_dispo x τcharge ; Φrejet_gnr += Φrejet ; Φvc_gnr += Φvc ; Waux,pro_gnr += Waux,pro ; Waux_gnr += Waux ; ηeff_ecs_gnr += ηeff ; Rfonct_ecs_gnr += Rfonct_ecs ; ihivernal : codé 1 hivernal/estival, 2 hivernal, 3 estival dans la nomenclature (p.635) mais 0, 1, 2 dans l'algorithme ; le test « Qreq_ecs_gen,gr > 0 » vise la demande du générateur Qreq (coquille d'indice) ; Mise à jour par += du jeu de données horaire
- (1023, p. 653, 654) ETAPE 3 froid : idfonction_gnr = 2 ; désactivé si Autfr_gen(j) ≠ 1 ;  ; Sans priorité
- (1024, p. 654) Qreq = Ratpngen_fr_gnr / Σ_{gnrk ∈ Gfr} Ratpngen_fr_gnrk x Qreq_tot_ar_fr_gen(h) ;  ; 
- (1025, p. 654) Qrest = 0 ; si (Qreq > 0 ou idfougen_gnr ≠ 5 ou Autch_gen(j) ≠ 1) : si Qreq > 0 alors ia_refroidi_gnr(h) = 1 ; Rpui_dispo = 1 - Rfonct_ecs_gnr(h) ; si Rpui_dispo > 0 : [Qcef(2;en), Qcons, Qfou, τcharge, Φvc, Waux,pro, Qrest, ηeff, Qprelec, Φrejet] = AppelGenerateur(θamont_gnr, θaval_fr_gen, Qreq, idfonction = 2, Rpui_dispo) ; mises à jour += (Qcef(2;en), Qcons, Qfou_fr, Qprelec, τcharge x Rpui_dispo, Φrejet, Φvc, Waux,pro, Waux, ηeff_fr) ; La condition « ou idfougen ≠ 5 ou Autch ≠ 1 » fait appeler un générateur réversible à charge nulle hors saison de chauffage pour imputer ses consommations résiduelles au froid ; 
- (1026, p. 654, 655) ETAPE 4 chauffage : idfonction_gnr = 1 ; désactivé si Autch_gen(j) ≠ 1 ;  ; Sans priorité
- (1027, p. 655) Qreq = [1 - ia_refroidi_gnr(h)] x Ratpngen_ch_gnr / Σ_{gnrk ∈ Gch} ([1 - ia_refroidi_gnrk(h)] x Ratpngen_ch_gnrk) x Qreq_tot_ar_ch_gen(h) ;  ; Pour les types 508 et 509, l'algorithme de boucle est celui de la fiche 8.16
- (1028, p. 655) Qrest = 0 ; si ia_refroidi_gnr(h) ≠ 1 : Rpui_dispo = 1 - Rfonct_ecs_gnr ; si Rpui_dispo > 0 : AppelGenerateur(θamont, θaval_ch_gen, Qreq, idfonction = 1, Rpui_dispo) ; mises à jour += (Qcef(1;en), Qcons, Qfou_ch, Qprelec, τcharge x Rpui_dispo, Φrejet, Φvc, Waux,pro, Waux, ηeff_ch) ; Le texte écrit Qfou_fr += Qfou et ηeff_fr dans cette étape chauffage : coquilles, lire Qfou_ch et ηeff_ch ; 
- (1029, p. 655) Qrep_[po]_gen,gr(h) = Qreq_tot_ar_[po]_gen(h) - Σ_{gnr ∈ G[po]} Qfou_[po]_gnr(h) ;  ; Sans priorité, ETAPE 5, pour chaque poste
- (1030, p. 656) Cascade (idtype_priorite_gen = 2), ETAPE 1 : Qreq = Qreq_tot_ar_[po]_gen(h) ; Le texte écrit Qrep_tot_ar : lire Qreq_tot_ar ; 
- (1031, p. 656) Qrest = Qreq_tot_ar_[po]_gen(h) ;  ; 
- (1032, p. 656, 657) ETAPE 2 ECS en cascade : idfonction_gnr = 3 ; désactivé si idencl_gen(j) ≠ 1 ; boucle sur gnr ∈ Gecs par idpriorite_ecs croissant à partir de 1 (le sous-assemblage ballon est toujours premier) : si ia_refroidi ≠ 1 : iecs_seule et iecs_fonction comme p.653 ; si (Qreq > 0 ou iecs_seule = 1) et iecs_fonction = 1 : Rpui_dispo = 1 ; AppelGenerateur(θamont, θaval_ecs, Qreq, Rpui_dispo, 3, iecs_seule) ; report Qreq = Qrest ; mises à jour += du jeu de données (3;en) ; « Rreq = Rrest » dans le texte : lire Qreq = Qrest ; Générateur suivant : premier idpriorite_ecs strictement supérieur
- (1033, p. 657, 658) ETAPE 3 froid en cascade : idfonction_gnr = 2 ; désactivé si Autfr_gen(j) ≠ 1 ; boucle par idpriorite_fr croissant : si (Qreq > 0 ou idfougen ≠ 5 ou Autch_gen(j) ≠ 1) : si Qreq > 0 alors ia_refroidi = 1 ; Rpui_dispo = 1 - Rfonct_ecs_gnr(h) ; si Rpui_dispo > 0 : AppelGenerateur(..., idfonction = 2, ...) ; Qreq = Qrest ; mises à jour += (2;en) ;  ; 
- (1034, p. 658) ETAPE 4 chauffage en cascade : idfonction_gnr = 1 ; désactivé si Autch_gen(j) ≠ 1 ; boucle par idpriorite_ch croissant : si ia_refroidi ≠ 1 : Rpui_dispo = 1 - Rfonct_ecs_gnr(h) ; si Rpui_dispo > 0 : AppelGenerateur(..., idfonction = 1, ...) ; Qreq = Qrest ; mises à jour += (1;en) (lire Qfou_ch, ηeff_ch) ;  ; 
- (1035, p. 659) Qrep_[po]_gen,gr(h) = Qrest (énergie restant à fournir après le dernier générateur de la cascade) ;  ; Cascade, ETAPE 5
- (1036, p. 659) Alternance (idtype_priorite_gen = 3), monoposte froid, ETAPE 1 : Qreq = Qreq_tot_ar_fr_gen(h) ; Tous les générateurs ont le même idfougen, différent de 4 (lire : le mode est interdit aux générateurs chauffage + refroidissement, idfougen = 5, selon le sens ; le texte écrit 4 puis le décrit comme « chauffage et refroidissement ») ; tri préalable par Pngen décroissant, gnr = 1 le plus puissant ; 
- (1037, p. 659) Qrest = Qreq_tot_ar_fr_gen(h) ;  ; 
- (1038, p. 659, 660) ETAPE 2 : idfonction_gnr = 2 ; désactivé si Autfr_gen(j) ≠ 1 ; boucle du plus puissant au moins puissant : compteur : si Qreq ≤ Rdim_{gnr+1} x Pngen_fr_{gnr+1} (le suivant suffit) : Nbasculement_gnr(h) = max(0 ; Nbasculement_gnr(h-1) - 1) ; sinon Nbasculement_gnr(h) = Nbasculement_init_gen ; si Nbasculement_gnr(h) > 0 : Rpui_dispo = 1 ; ia_refroidi = 1 ; AppelGenerateur(θamont, θaval_fr (le texte écrit θaval_ch), Qreq, 2, Rpui_dispo) ; Qreq = Qrest ; mises à jour += (2;en) (le texte écrit Qfou_ecs et ηeff_ecs : lire Qfou_fr, ηeff_fr) ; Qrest = Qreq ; Nbasculement_gnr(h-1) : état conservé par générateur ; 
- (1039, p. 660) Qrep_fr_gen,gr(h) = Qrest ;  ; 
- (1040, p. 660) Alternance monoposte ECS, ETAPE 1 : Qreq = Qreq_tot_ar_ecs_gen(h) ;  ; 
- (1041, p. 660) Qrest = Qreq_tot_ar_ecs_gen(h) ;  ; 
- (1042, p. 660, 661) ETAPE 2 : idfonction = 3 ; désactivé si idencl_gen(j) ≠ 1 ; boucle par puissance décroissante : compteur avec Pngen_ecs_{gnr+1} comme en 1038 ; iecs_fonction comme p.653 ; si Nbasculement_gnr(h) > 0 et iecs_fonction = 1 : Rpui_dispo = 1 ; iecs_seule = 1 ; AppelGenerateur(θamont, θaval_ecs, Qreq, Rpui_dispo, 3, iecs_seule) ; Qreq = Qrest ; mises à jour += (3;en) y compris Rfonct_ecs ; Qrest = Qreq ;  ; 
- (1043, p. 661) Qrep_ecs_gen,gr(h) = Qrest ;  ; 
- (1044, p. 662) Alternance monoposte chauffage, ETAPE 1 : Qreq = Qreq_tot_ar_ch_gen(h) ;  ; 
- (1045, p. 662) Qrest = Qreq_tot_ar_ch_gen(h) ;  ; 
- (1046, p. 662) ETAPE 2 : idfonction = 1 ; désactivé si Autch_gen(j) ≠ 1 ; boucle par puissance décroissante : compteur avec Pngen_ch_{gnr+1} ; si Nbasculement_gnr(h) > 0 : Rpui_dispo = 1 ; AppelGenerateur(θamont, θaval_ch, Qreq, 1, Rpui_dispo) ; Qreq = Qrest ; mises à jour += (1;en) (lire Qfou_ch, ηeff_ch) ; Qrest = Qreq ;  ; 
- (1047, p. 663) Qrep_ch_gen,gr(h) = Qrest ;  ; 
- (1048, p. 663) Alternance biposte chauffage + ECS (idfougen = 4), ETAPE 1 : Qreq_ecs = Qreq_tot_ar_ecs_gen(h) ;  ; 
- (1049, p. 663) Qrest_ecs = Qreq_tot_ar_ecs_gen(h) ;  ; 
- (1050, p. 663) Qreq_ch = Qreq_tot_ar_ch_gen(h) ;  ; 
- (1051, p. 663) Qrest_ch = Qreq_tot_ar_ch_gen(h) ;  ; 
- (1052, p. 663, 664) ETAPE 2 : idfonction = 1 ; désactivé si Autch_gen(j) ≠ 1 et idencl_gen(j) ≠ 1 ; boucle par puissance décroissante : compteur : si Qreq_ch + Qreq_ecs ≤ Rdim_{gnr+1} x Pngen_ch_{gnr+1} : Nbasculement(h) = max(0 ; Nbasculement(h-1) - 1), sinon Nbasculement_init ; si Nbasculement(h) > 0 : iecs_seule = 1 si Autch_gen(j) = 0 sinon 0 ; partie ECS : Rpui_dispo = 1 ; AppelGenerateur(θamont, θaval_ecs, Qreq_ecs, 1, 3, iecs_seule) ; post-traitement += (3;en) avec Rfonct_ecs ; Qreq_ecs = Qrest_ecs ; partie chauffage : Rpui_dispo = 1 - Rfonct_ecs_gnr(h) ; si Rpui_dispo > 0 et iecs_seule = 0 : AppelGenerateur(θamont, θaval_ch, Qreq_ch, Rpui_dispo, 1, iecs_seule) ; post-traitement += (1;en) (lire Qfou_ch) ; Qreq_ch = Qrest_ch ; Qrest_ch = Qreq_ch ; Qrest_ecs = Qreq_ecs ;  ; C'est la demande totale chauffage + ECS qui choisit la configuration
- (1053, p. 665) Qrep_ch_gen,gr(h) = Qrest_ch ; Qrep_ecs_gen,gr(h) = Qrest_ecs ;  ; 
- (1054, p. 665) [Waux,am_gnr(h)]_{gnr = 1..N} = CalculAuxAmont_SA( [τcharge_gnr(h)]_{gnr = 1..N} ) ; N générateurs reliés à la source amont SA, avec idsource_amont_gnr = 1 ; Après les algorithmes de priorité, pendant les périodes de fonctionnement
- (1055, p. 665) Waux_gnr(h) += Waux,am_gnr(h) ;  ; 
- (1056, p. 665) Si ia_refroidi_gnr(h) = 1 : Qcef(2;50)_gnr(h) += Waux,am ; sinon si τcharge_gnr(h) > 0 : Qcef(2;50) += [1 - Rfonct_ecs_gnr(h)/τcharge_gnr(h)] x Waux,am et Qcef(3;50) += Rfonct_ecs_gnr(h)/τcharge_gnr(h) x Waux,am ; sinon (charge nulle) : si idfougen = 3 ou Autch_gen(j) = 0 (iecs_seule = 1) : Qcef(3;50) += Waux,am ; sinon Qcef(1;50) += Waux,am ;  ; La branche « τcharge > 0 sans refroidissement » impute la part non ECS à la ligne 2 (froid) dans le texte ; un générateur de chauffage y verrait ses auxiliaires amont comptés en froid : lire ligne 1 (voir points ouverts)
- (1057, p. 666) Qcef(po;en)_gen(h) = Σ_{gnr ∈ gen} Qcef(po;en)_gnr(h) ; Somme des matrices 3 x 6 de tous les générateurs et ballons ; Post-traitement
- (1058, p. 666) Qcef(3;50)_gen(h) += Σ_{dp-e ∈ gen} Wrechauff-e_dp-e(h) ; Réchauffeur de boucle ECS ; 
- (1059, p. 666) Φvc_tot_gen(h) = Σ_{gnr ∈ gen} Φvc_gnr(h) + Σ_{sto ∈ gen} Φvc_sto(h) ; Qprelec_tot_gen(h) = Σ_{gnr ∈ gen} Qprelec_gnr(h) ; Pertes transmises aux groupes du bâtiment bat au prorata de Ratsurf_gen,gr, au pas h+1 (fiche 8.14 p.610) ; Φvc_sto seulement si la génération est en volume chauffé (p.651)
- (1060, p. 666) Si (Qrep_ch(h) > 0 ou Qrep_ecs(h) > 0) et idrelance_ch_gen(h) = faux : Nbsousdim_ch(h) = Nbsousdim_ch(h-1) + 1 ; sinon 0 ; État conservé ; Générateurs seulement, ballons évalués à part
- (1061, p. 666) Si Nbsousdim_ch(h) > 6 : idsousdim_court_ch_gnr = 1 ; Indicateur fixé pour toute la simulation ; 
- (1062, p. 666) Si Nbsousdim_ch(h) > 72 : idsousdim_long_ch_gnr = 1 ;  ; 
- (1063, p. 666) Si Qrep_fr(h) > 0 : Nbsousdim_fr(h) = Nbsousdim_fr(h-1) + 1 ; sinon 0 ;  ; 
- (1064, p. 667) Si Nbsousdim_fr(h) > 6 : idsousdim_court_fr_gnr = 1 ;  ; 
- (1065, p. 667) Si Nbsousdim_fr(h) > 72 : idsousdim_long_fr_gnr = 1 ;  ; 
- (1485, p. 925) Qcef(1;en)_gen,gr(h) = Ratbes_ch_gen,gr(h) x [Qcef(1;en)_gen(h) - Σ_{gnr ∈ GBE} Qcef(1;en)_gnr(h)] + Σ_{gnr ∈ GBE, gnr → gr} Qcef(1;en)_gnr(h) ; GBE : générateurs sur boucle d'eau (type 507), rattachés à un groupe (Id_Groupe) ; Fiche 8.29 ; équation reconstituée depuis les symboles dispersés (pages 925 à 926)
- (1486, p. 925) Qcef(2;en)_gen,gr(h) = Ratbes_fr_gen,gr(h) x [Qcef(2;en)_gen(h) - Σ_{GBE} Qcef(2;en)_gnr(h)] + Σ_{GBE → gr} Qcef(2;en)_gnr(h) ;  ; Reconstituée
- (1487, p. 926) Qcef(3;en)_gen,gr(h) = Ratbes_ecs_gen,gr(h) x Qcef(3;en)_gen(h) ;  ; Reconstituée
- (1488, p. 927) Qcef(1;en)_gnr,gr(h) = Qcef(1;en)_gnr(h) x Ratbes_ch_gen,gr(h) ;  ; Générateurs thermodynamiques 503 à 509 hors boucle d'eau ; sert à Cep_ch_gnr,gr (1497)
- (1489, p. 927) Qcef(2;en)_gnr,gr(h) = Qcef(2;en)_gnr(h) x Ratbes_fr_gen,gr(h) ;  ; 
- (1490, p. 927) Qcef(3;en)_gnr,gr(h) = Qcef(3;en)_gnr(h) x Ratbes_ecs_gen,gr(h) ;  ; 
- (1491, p. 927) Qcef(1;en)_gnr,gr(h) = Qcef(1;en)_gnr(h) ;  ; Générateur de boucle d'eau (507) lié directement au groupe
- (1492, p. 927) Qcef(2;en)_gnr,gr(h) = Qcef(2;en)_gnr(h) ;  ; 
- (1493, p. 927) Si Qreq_tot_sr_ch_gen(h) + Qreq_tot_sr_ecs_gen(h) > 0 : Ratpelec_gen,gr(h) = [Qreq,ch_gen,gr(h) + Qreq,ecs_gen,gr(h)] / [Qreq_tot_sr_ch_gen(h) + Qreq_tot_sr_ecs_gen(h)] ; sinon Ratpelec_gen,gr(h) = [Σ_dp Ratbes_ch_dp,gr(h) x Adess_ch_dp + Σ_dp-e Ratbes_ecs_dp-e,gr(h) x Adess_ecs_dp-e] / [Σ_dp Adess_ch_dp + Σ_dp-e Adess_ecs_dp-e] ; Ratpelec = Ratbes_ch+ecs_gen,gr de la nomenclature ; Reconstituée (page 927)
- (1494, p. 927) Qef_prelec_gen,gr(h) = Qprelec_tot_gen(h) x Ratpelec_gen,gr(h) ;  ; Cogénération
- (1495, p. 928) Cef_ch_m_gnr = Σ_{h ∈ mois} Σ_{en = 10..60} Qcef(1;en)_gnr(h) ; Cep_ch_m_gnr = Σ_{h ∈ mois} Σ_en Coefep(en) x Qcef(1;en)_gnr(h) ;  ; Mensuel, par générateur
- (1496, p. 928) Cef_ch_gnr = Σ_{mois = 1..12} Cef_ch_m_gnr ; Cep_ch_gnr = Σ_mois Cep_ch_m_gnr ;  ; Annuel
- (1497, p. 928) Cep_ch_gnr,gr = Σ_{h = 1..8760} Σ_{en = 10..60} Coefep(en) x Qcef(1;en)_gnr,gr(h) ;  ; Thermodynamiques seulement, annuel, énergie primaire
- (1498, p. 928) Cef_ch_m_gen = Σ_{h ∈ mois} Σ_en Qcef(1;en)_gen(h) ; Cep_ch_m_gen = Σ Σ Coefep(en) x Qcef(1;en)_gen(h) ;  ; 
- (1499, p. 928) Cef_ch_gen = Σ_mois Cef_ch_m_gen ; Cep_ch_gen = Σ_mois Cep_ch_m_gen ;  ; 
- (1500, p. 929) Cef_ch_m_gen,gr = Σ_{h ∈ mois} Σ_en Qcef(1;en)_gen,gr(h) ; Cep_ch_m_gen,gr = Σ Σ Coefep(en) x Qcef(1;en)_gen,gr(h) ;  ; Par groupe
- (1501, p. 929) Cef_ch_gen,gr = Σ_mois Cef_ch_m_gen,gr ; Cep_ch_gen,gr = Σ_mois Cep_ch_m_gen,gr ;  ; 
- (1502, p. 929) Cef_fr_m_gnr = Σ_{h ∈ mois} Σ_en Qcef(2;en)_gnr(h) ; Cep_fr_m_gnr = Σ Σ Coefep(en) x Qcef(2;en)_gnr(h) ;  ; 
- (1503, p. 929) Cef_fr_gnr = Σ_mois Cef_fr_m_gnr ; Cep_fr_gnr = Σ_mois Cep_fr_m_gnr ;  ; 
- (1504, p. 929) Cep_fr_gnr,gr = Σ_{h = 1..8760} Σ_en Coefep(en) x Qcef(2;en)_gnr,gr(h) ;  ; Thermodynamiques
- (1505, p. 930) Cef_fr_m_gen = Σ_{h ∈ mois} Σ_en Qcef(2;en)_gen(h) ; Cep_fr_m_gen idem avec Coefep ;  ; 
- (1506, p. 930) Cef_fr_gen = Σ_mois Cef_fr_m_gen ; Cep_fr_gen = Σ_mois Cep_fr_m_gen ;  ; 
- (1507, p. 930) Cef_fr_m_gen,gr = Σ_{h ∈ mois} Σ_en Qcef(2;en)_gen,gr(h) ; Cep_fr_m_gen,gr idem avec Coefep ;  ; 
- (1508, p. 930) Cef_fr_gen,gr = Σ_mois Cef_fr_m_gen,gr ; Cep_fr_gen,gr = Σ_mois Cep_fr_m_gen,gr ;  ; 
- (1509, p. 930) Cef_ecs_m_gnr = Σ_{h ∈ mois} Σ_en Qcef(3;en)_gnr(h) ; Cep_ecs_m_gnr idem avec Coefep ;  ; 
- (1510, p. 930) Cef_ecs_gnr = Σ_mois Cef_ecs_m_gnr ; Cep_ecs_gnr = Σ_mois Cep_ecs_m_gnr ;  ; 
- (1511, p. 931) Cep_ecs_gnr,gr = Σ_{h = 1..8760} Σ_en Coefep(en) x Qcef(3;en)_gnr,gr(h) ;  ; Thermodynamiques
- (1512, p. 931) Cef_ecs_m_gen = Σ_{h ∈ mois} Σ_en Qcef(3;en)_gen(h) ; Cep_ecs_m_gen idem avec Coefep ;  ; 
- (1513, p. 931) Cef_ecs_gen = Σ_mois Cef_ecs_m_gen ; Cep_ecs_gen = Σ_mois Cep_ecs_m_gen ;  ; 
- (1514, p. 931) Cef_ecs_m_gen,gr = Σ_{h ∈ mois} Σ_en Qcef(3;en)_gen,gr(h) ; Cep_ecs_m_gen,gr idem avec Coefep ;  ; 
- (1515, p. 932) Cef_ecs_gen,gr = Σ_mois Cef_ecs_m_gen,gr ; Cep_ecs_gen,gr = Σ_mois Cep_ecs_m_gen,gr ;  ; 
- (1516, p. 932) Eef_prelec_m_gnr = Σ_{h ∈ mois} Qprelec_gnr(h) ; Eep_prelec_m_gnr = Coefep(50) x Eef_prelec_m_gnr ;  ; Cogénération
- (1517, p. 932) Eef_prelec_gnr = Σ_mois Eef_prelec_m_gnr ; Eep_prelec_gnr = Coefep(50) x Eef_prelec_gnr ;  ; 
- (1518, p. 932) Eef_prelec_m_gen = Σ_{gnr ∈ gen} Eef_prelec_m_gnr ; Eep_prelec_m_gen = Coefep(50) x Eef_prelec_m_gen ;  ; 
- (1519, p. 932) Eef_prelec_gen = Σ_{gnr ∈ gen} Eef_prelec_gnr ; Eep_prelec_gen = Coefep(50) x Eef_prelec_gen ;  ; 
- (1520, p. 932) Eef_prelec_gen,gr = Σ_{h = 1..8760} Qef_prelec_gen,gr(h) ; Eep_prelec_gen,gr = Coefep(50) x Eef_prelec_gen,gr ;  ; 
- (1521, p. 932) Eep_sol_tot_gen,gr = Σ_h Σ_{BS ∈ gen} Qsol_BS(h) x Rat_BS,gr(h) ; Eep_aux_tot_gen,gr = Coefep(50) x Σ_h Σ_BS Pp_BS(h) x Rat_BS,gr(h), avec Rat_BS,gr = Ratbes_ch_gen,gr si idfou_sto_BS = 1, Ratbes_ecs_gen,gr si 3, Ratbes_ch+ecs_gen,gr (Ratpelec) si 4 ; Qsol_BS, Pp_BS : énergie solaire transmise et pompe de la boucle solaire (chapitre stockage) ; Reconstituée (page 932) ; bilan ENR
- (1522, p. 933) Qfou_3postes_gnr = Σ_{h = 1..8760} [Qfou_ch_gnr(h) + Qfou_fr_gnr(h) + Qfou_ecs_gnr(h)] ;  ; Sortie XML Q_fou_3_postes
- (1523, p. 933, 934) Générateurs de chauffage (idfonction = 1), chaque heure : si Autch_gen(j) ≠ 1 : Nbhcharge_HF_ch_gnr += 1 ; sinon : si τcharge_ch_gnr(h) = 0 % : Nbhcharge_0_ch += 1 ; si 0 % < τ ≤ 10 % : Nbhcharge_0_10_ch += 1 ; ... si 90 % < τ : Nbhcharge_90_100_ch += 1. Avec τcharge_ch_gnr(h) = τcharge_gnr(h) si idfougen = 1 ; (τcharge_gnr(h) - Rfonct_ecs_gnr(h)) x 100 % si idfougen = 4 ; τcharge_gnr(h) si idfougen = 5 et ia_refroidi = 0 ; 0 si idfougen = 5 et ia_refroidi = 1 ; Compteurs nuls au premier pas ; Reconstituée depuis les fragments (pages 933 à 934) ; les bornes exactes (inclusives ou non) ne sont pas lisibles
- (1524, p. 934) Générateurs de refroidissement (idfonction = 2) : si Autfr_gen(j) ≠ 1 : Nbhcharge_HF_fr += 1 ; sinon classes 0, ]0;10], ... ]90;100] sur τcharge_fr_gnr(h) = τcharge_gnr(h) si idfougen = 2 ; τcharge_gnr(h) si idfougen = 5 et ia_refroidi = 1 ; 0 si idfougen = 5 et ia_refroidi = 0 ;  ; Reconstituée
- (1525, p. 935) Générateurs d'ECS (idfonction = 3) : si Idencl_gen(j) ≠ 1 : Nbhcharge_HF_ecs += 1 ; sinon classes sur τcharge_ecs_gnr(h) = τcharge_gnr(h) si idfougen = 3 ; Rfonct_ecs_gnr(h) si idfougen = 4 ;  ; Reconstituée
- (1526, p. 935, 936) Eef_fou_ch_gnr = Σ_{h = 1..8760} Qfou_ch_gnr(h) ; Eef_fou_fr_gnr = Σ_h Qfou_fr_gnr(h) ; Eef_fou_ecs_gnr = Σ_h Qfou_ecs_gnr(h) ;  ; 
- (1527, p. 936) ηeff_ch_an_gnr = Eef_fou_ch_gnr / Cef_ch_gnr ; ηeff_fr_an_gnr = Eef_fou_fr_gnr / Cef_fr_gnr ; ηeff_ecs_an_gnr = Eef_fou_ecs_gnr / Cef_ecs_gnr ; COP ou EER annuel pour les thermodynamiques, rendement pour les autres ; Division protégée si Cef = 0
- (1528, p. 936) Cef_aux_m_gnr = Σ_{h ∈ mois} Waux_gnr(h) ; Cep_aux_m_gnr = Coefep(50) x Cef_aux_m_gnr ; Waux inclut les auxiliaires amont (1055) ; 
- (1529, p. 936) Cef_aux_gnr = Σ_mois Cef_aux_m_gnr ; Cep_aux_gnr = Coefep(50) x Cef_aux_gnr ;  ; 
- (1530 à 1535, p. 937) Cef_gaz_gnr = Σ_{po = 1..3} Σ_{h = 0..8760} Qcef(po;10)_gnr(h) ; Cef_fod_gnr avec en = 20 ; Cef_cha_gnr avec 30 ; Cef_boi_gnr avec 40 ; Cef_ele_gnr avec 50 ; Cef_rdc_gnr avec 60 ;  ; Annuel, par générateur
- (1536 à 1541, p. 937) Cep_gaz_gnr = Coefep(10;1) x Cef_gaz_gnr ; Cep_fod_gnr = Coefep(20;1) x Cef_fod_gnr ; Cep_cha_gnr = Coefep(30;1) x Cef_cha ; Cep_boi_gnr = Coefep(40;1) x Cef_boi ; Cep_ele_gnr = Coefep(50;1) x Cef_ele ; Cep_rdc_gnr = Coefep(60;1) x Cef_rdc ;  ; 
- (1542 à 1547, p. 937, 938) Cef_gaz_gen, Cef_fod_gen, Cef_cha_gen, Cef_boi_gen, Cef_ele_gen, Cef_rdc_gen = Σ_{po = 1..3} Σ_h Qcef(po;en)_gen(h) ;  ; Par génération
- (1548 à 1553, p. 938) Cep_x_gen = Coefep(x;1) x Cef_x_gen pour x dans {gaz 10, fod 20, cha 30, boi 40, ele 50, rdc 60} ;  ; 
- (1554 à 1559, p. 938) Cef_gaz_gen,gr ... Cef_rdc_gen,gr = Σ_{po = 1..3} Σ_h Qcef(po;en)_gen,gr(h) ;  ; Par génération et par groupe ; alimente Sortie_Groupe_C O_Cef_ch_gaz_annuel etc.
- (1560 à 1565, p. 938, 939) Cep_x_gen,gr = Coefep(x;1) x Cef_x_gen,gr ;  ; 
- (1566, p. 939) Cef_rdch_gen,gr = Σ_h [Qcef(1;60)_gen,gr(h) + Qcef(3;60)_gen,gr(h)] ; Réseau de chaleur : chauffage + ECS ; 
- (1567, p. 939) Cef_rdfr_gen,gr = Σ_h Qcef(2;60)_gen,gr(h) ;  ; 
- (1568, p. 939) Cep_rdch_gen,gr = Coefep(60;1) x Cef_rdch_gen,gr ;  ; 
- (1569, p. 939) Cep_rdfr_gen,gr = Coefep(60;1) x Cef_rdfr_gen,gr ;  ; 

## Algorithme

```
Structures proposées (module openbce/generation.py, en lecture des Noeud) :

```
POSTE = {CH: 0, FR: 1, ECS: 2}            # lignes de la matrice Qcef (codes texte 1, 2, 3)
ENERGIE = {10: 0, 20: 1, 30: 2, 40: 3, 50: 4, 60: 5}   # colonnes (tableau 253)
COEF_EP = {10: 1.0, 20: 1.0, 30: 1.0, 40: 1.0, 50: 2.3, 60: 1.0}   # tableau 252 ; 60 : 1 - RatENR pour Cep,nr
THETA_AMB_CH, THETA_AMB_FR = 20.0, 26.0
N_BASCULEMENT_INIT = 20

@dataclass
class EtatGenerateur:            # jeu de données de la figure 111, remis à zéro chaque heure
    qcef: np.ndarray  (3 x 6)    # Wh
    qcons, qfou_ch, qfou_fr, qfou_ecs, qprelec: float
    theta_amont: float
    phi_rejet, phi_vc, waux_pro, waux, tau_charge: float
    eta_ch, eta_fr, eta_ecs: float
    ia_refroidi: bool
    rfonct_ecs: float
    # états persistants d'une heure à l'autre
    phi_rejet_prec: float        # (1009)
    n_basculement: int           # mode alterné, initialisé à N_BASCULEMENT_INIT
    nbh_charge: dict[str, int]   # compteurs (1523 à 1525), 12 classes x 3 postes
    cumul_qcef_mois: np.ndarray  (12 x 3 x 6), cumul_qfou (3), cumul_waux_mois (12), cumul_qprelec_mois (12)

class Generation:
    noeud: Noeud                                   # Generation
    type_priorite, pos_gen, id_bat, id_et: int
    gestion_ch, gestion_fr: int ; theta_wm_ch, theta_wm_fr, theta_wm_ecs: float
    gnrs: list[Generateur]                          # objets fournissant appeler(...) (fiches 8.18 et suivantes)
    ballons: list[SousAssemblageBallon]             # premiers en cascade, exposent leur propre jeu de données
    dps_ch, dps_fr, dps_ecs: list[DistributionIntergroupe]   # Qsys(h), theta_moy(h), theta_max, adess, idrelance(h), idencl(j), ratbes_dp_gr(h), theta_i_aval_eq(h), type_fictif
    sources_amont: list[SourceAmont]
    # états
    qrep: np.ndarray (3)         # Qrep_ch, Qrep_fr, Qrep_ecs de h-1
    theta_aval_prec: np.ndarray (2)   # θaval_ch(h-1), θaval_fr(h-1)
    nb_sousdim_ch, nb_sousdim_fr: int
    sousdim: dict[str, bool]      # court/long x ch/fr
    ratsurf_gr: dict[int, float] ; ratsurf_dess: dict[(poste, dp), float]
    pngen_tot, ratpngen: dict      # mode sans priorité (1018, 1019)
```

Appel AppelGenerateur (interface commune à tous les générateurs, figure 112 p.652) :
```
def appeler(gnr, theta_amont, theta_aval, qreq, idfonction, rpui_dispo, iecs_seule=0) -> Resultat:
    # retourne qcef (3x6 Wh), qcons, qfou, tau_charge, phi_vc, waux_pro, qrest, eta, qprelec, phi_rejet, rfonct_ecs
```

Phase 0 : saisons effectives (fiche 8.4), une fois par jour avant les systèmes, après le calcul des saisons propres :
```
def saisons_effectives(projet, saisons_propres: dict[gr, (aut_ch_pro[j], aut_fr_pro[j])]):
    for gen in generations:
        desservis_ch = {gr : relié à gen par une dp de chauffage ou une CTA}
        desservis_fr = {gr : relié par une dp de froid ou CTA}
        gen.aut_ch[j] = max(aut_ch_pro[gr][j] for gr in desservis_ch)                       # (840)
        gen.aut_fr[j] = max(aut_fr_pro[gr][j] for gr in desservis_fr if gr.is_climatise)     # (840)
    for gr in groupes:
        gens_perm = [gen for gen in generations if gr desservi par gen and gen.idraccord_reseau == 1]
        if gens_perm:                                                                        # (841)
            aut_ch_eff[gr][j] = max(gen.aut_ch[j] for gen in gens_perm desservant gr en chaud)
            aut_fr_eff[gr][j] = max(gen.aut_fr[j] for gen in gens_perm desservant gr en froid)
        else:                                                                                # (842)
            aut_ch_eff[gr][j], aut_fr_eff[gr][j] = aut_ch_pro[gr][j], aut_fr_pro[gr][j]
    for dp in distributions: aut_ch_eff[dp][j] = max(aut_ch_eff[gr][j] for gr in dp)        # (843)
    for cta in ctas: idem                                                                    # (844)
    # aut_ch_eff[gr] alimente ThC.chauffage_impose / refroidissement_impose de groupe.py
```
Remarque de mise en œuvre : le groupe a besoin de sa saison effective pour son calcul horaire, et la génération a besoin des saisons propres de tous ses groupes. En Th-C le calcul se fait par jour (IHJ(h) = 1), donc deux passes par jour ou, comme banc/cep.py aujourd'hui, une première passe annuelle en saisons propres puis une seconde en saisons effectives.

Phase 1 : initialisation (une fois) :
```
def initialiser(gen):
    verifier_coherence(gen)                     # (981) à (988), lève un avertissement, pas une erreur bloquante
    for gr in groupes desservis:
        gen.ratsurf_gr[gr] = A_gr / sum(A_gr* for gr* desservis and dans Id_Bat) if gen.pos_gen == 1 and gr dans Id_Bat else 0.0   # (989), (990)
    for poste, dps in ((CH, dps_ch), (FR, dps_fr), (ECS, dps_ecs)):
        total = sum(dp.adess for dp in dps)
        gen.ratsurf_dess[(poste, dp)] = dp.adess / total                                     # (991) à (993)
    if gen.type_priorite == 1:
        for poste: G = generateurs instantanes du poste
            gen.pngen_tot[poste] = sum(g.rdim * g.pngen[poste] for g in G)                 # (1018)
            gen.ratpngen[(poste, g)] = g.rdim * g.pngen[poste] / gen.pngen_tot[poste]     # (1019)
    if gen.type_priorite == 3:
        trier G par rdim x pngen décroissant ; n_basculement = N_BASCULEMENT_INIT pour chaque gnr
    theta_dist_ch_max = max(dp.theta_max for dp in dps_ch hydrauliques)                     # (981)
    theta_dist_fr_max = max(dp.theta_max for dp in dps_fr hydrauliques)                     # (982)
    theta_dist_ecs_max = max(dp.theta_max for dp in dps_ecs)                                # (983)
    gen.qrep[:] = 0 ; gen.theta_aval_prec[:] = (theta_wm_ch, theta_wm_fr) ; nb_sousdim = 0
```

Phase 2 : pas horaire, dans l'ordre d'appel de la figure 110 (p.645) :
```
def pas(gen, h, j, te, b_therm, mois):
    for g in gen.gnrs: g.etat.remise_a_zero()                                    # figure 111
    # --- calculs préliminaires (8.17.3.5) ---
    qsr = [sum(dp.qsys[h] for dp in dps_ch), -sum(dp.qsys[h] for dp in dps_fr), sum(dp.qsys[h] for dp in dps_ecs)]   # (994) à (996)
    ratbes_dp = {}
    for poste, dps in ...:
        for dp in dps:
            ratbes_dp[(poste, dp)] = (abs(dp.qsys[h]) / qsr[poste]) if qsr[poste] > 0 else gen.ratsurf_dess[(poste, dp)]   # (997) à (999)
    ratbes_gr = {(poste, gr): sum(ratbes_dp[(poste, dp)] * dp.ratbes_gr[gr][h] for dp in dps[poste] if gr in dp)}         # (1000) à (1002)
    qreq_gr = {(poste, gr): qsr[poste] * ratbes_gr[(poste, gr)]}                                                           # (1003) à (1005), sortie vers calculs groupe
    idrelance_ch = max(dp.idrelance[h] for dp in dps_ch) ; idrelance_fr = max(dp.idrelance[h] for dp in dps_fr)          # (1006), (1007)
    idencl = max(dp.idencl[j] for dp in dps_ecs)                                                                           # (1008)
    conv = THETA_AMB_CH if (aut_ch[j] and not aut_fr[j]) else THETA_AMB_FR if (aut_fr[j] and not aut_ch[j]) else 23.0
    theta_amb = conv if gen.pos_gen == 1 else b_therm[h] * te[h] + (1 - b_therm[h]) * conv                                # p.648
    for sa in gen.sources_amont:
        theta_sa = sa.temperature_amont(h, [g.etat.phi_rejet_prec for g in sa.gnrs])                                       # (1009)
        for g in sa.gnrs: g.etat.theta_amont = theta_sa
    qar = qsr + gen.qrep                                                                                                   # (1015) à (1017)
    theta_aval_ecs = gen.theta_wm_ecs                                                                                      # (1010)
    theta_aval_ch = _theta_aval(gen, CH, h, qsr, qar, idrelance_ch, ratbes_dp)                                             # (1011) ou (1013)
    theta_aval_fr = _theta_aval(gen, FR, h, qsr, qar, idrelance_fr, ratbes_dp)                                             # (1012) ou (1014)
    gen.theta_aval_prec = (theta_aval_ch, theta_aval_fr)
    # --- sous-assemblages ballons : appelés en premier (cascade), mettent à jour base/appoint et Φvc_sto ---
    # --- algorithme principal selon type_priorite ; ordre des postes : froid, ECS, chauffage ---
    if gen.type_priorite == 1: qrest = _sans_priorite(gen, h, j, qar, mois, theta_amont, theta_aval_*)        # (1020) à (1029)
    elif gen.type_priorite == 2: qrest = _cascade(gen, h, j, qar, mois, ...)                                  # (1030) à (1035)
    else: qrest = _alternance(gen, h, j, qar, mois, ...)                                                       # (1036) à (1053)
    gen.qrep = qrest                                                                                           # report vers h+1
    # --- auxiliaires amont ---
    for sa in gen.sources_amont:
        waux_am = sa.auxiliaires_amont(h, [g.etat.tau_charge for g in sa.gnrs])                                # (1054)
        for g, w in zip(sa.gnrs, waux_am):
            g.etat.waux += w                                                                                   # (1055)
            _imputer_aux_amont(g, w, aut_ch[j])                                                                # (1056)
    # --- post-traitement ---
    qcef_gen = sum(g.etat.qcef for g in gen.gnrs) + sum(b.qcef for b in gen.ballons)                           # (1057)
    qcef_gen[ECS, ENERGIE[50]] += sum(dp.w_rechauffeur[h] for dp in dps_ecs)                                   # (1058)
    phi_vc_tot = sum(g.etat.phi_vc for g in gen.gnrs) + (sum(b.phi_vc_sto for b in gen.ballons) if gen.pos_gen == 1 else 0)   # (1059)
    qprelec_tot = sum(g.etat.qprelec for g in gen.gnrs)
    # sous-dimensionnement
    gen.nb_sousdim_ch = gen.nb_sousdim_ch + 1 if ((qrest[CH] > 0 or qrest[ECS] > 0) and not idrelance_ch) else 0        # (1060)
    gen.sousdim['court_ch'] |= gen.nb_sousdim_ch > 6 ; gen.sousdim['long_ch'] |= gen.nb_sousdim_ch > 72                  # (1061), (1062)
    gen.nb_sousdim_fr = gen.nb_sousdim_fr + 1 if qrest[FR] > 0 else 0                                                    # (1063)
    gen.sousdim['court_fr'] |= gen.nb_sousdim_fr > 6 ; gen.sousdim['long_fr'] |= gen.nb_sousdim_fr > 72                  # (1064), (1065)
    # fiche 8.29 : répartition par groupe et cumuls
    for gr in groupes desservis:
        gbe = [g for g in gen.gnrs if g.type == 507]
        for poste in (CH, FR):
            hors_be = qcef_gen[poste] - sum(g.etat.qcef[poste] for g in gbe)
            qcef_gr[gr][poste] = ratbes_gr[(poste, gr)] * hors_be + sum(g.etat.qcef[poste] for g in gbe if g.id_groupe == gr)   # (1485), (1486)
        qcef_gr[gr][ECS] = ratbes_gr[(ECS, gr)] * qcef_gen[ECS]                                                                   # (1487)
        if qsr[CH] + qsr[ECS] > 0: ratpelec = (qreq_gr[(CH, gr)] + qreq_gr[(ECS, gr)]) / (qsr[CH] + qsr[ECS])                    # (1493)
        else: ratpelec = (sum(dp.ratbes_gr[gr][h] * dp.adess for dp in dps_ch + dps_ecs if gr in dp)) / sum(dp.adess for dp in dps_ch + dps_ecs)
        qef_prelec_gr[gr] = qprelec_tot * ratpelec                                                                                 # (1494)
        cumuls mensuels et annuels (1495 à 1515, 1520, 1554 à 1569) : cumul[mois][gr] += qcef_gr[gr] ; ep = qcef x COEF_EP par colonne
    for g in gen.gnrs:                                                                                                             # cumuls par générateur
        g.cumul_qcef_mois[mois] += g.etat.qcef ; g.cumul_qfou += (qfou_ch, qfou_fr, qfou_ecs) ; g.cumul_waux_mois[mois] += g.etat.waux ; g.cumul_qprelec_mois[mois] += g.etat.qprelec   # (1495), (1502), (1509), (1516), (1522), (1526), (1528)
        _histogramme_charge(g, aut_ch[j], aut_fr[j], idencl)                                                                      # (1523) à (1525)
        g.etat.phi_rejet_prec = g.etat.phi_rejet
    return qreq_gr, qcef_gr, phi_vc_tot (réparti par ratsurf_gr aux groupes au pas h+1), qef_prelec_gr
```

Température aval (1011 à 1014) :
```
def _theta_aval(gen, poste, h, qsr, qar, idrelance, ratbes_dp):
    dps = gen.dps[poste] ; gestion = gen.gestion_ch if poste == CH else gen.gestion_fr
    if dps fictifs:                                                                 # (1013), (1014)
        return sum(ratbes_dp[(poste, dp)] * dp.theta_i_aval_eq[h] for dp in dps)
    if gestion == 1: return gen.theta_wm[poste]
    if idrelance: return gen.theta_dist_max[poste]
    if qsr[poste] == 0 and qar[poste] > 0: return gen.theta_aval_prec[poste]
    return max(dp.theta_moy[h] for dp in dps)
```

Mode sans priorité (1020 à 1029), ordre froid, ECS, chauffage :
```
def _sans_priorite(gen, h, j, qar, mois, ...):
    G = {FR: gen.G_fr, ECS: gen.G_ecs, CH: gen.G_ch}
    if gen.aut_fr[j]:
        for g in G[FR]:
            qreq = gen.ratpngen[(FR, g)] / sum(gen.ratpngen[(FR, k)] for k in G[FR]) * qar[FR]                     # (1024)
            if qreq > 0 or g.idfougen != 5 or not gen.aut_ch[j]:
                if qreq > 0: g.etat.ia_refroidi = True
                rpui = 1 - g.etat.rfonct_ecs
                if rpui > 0: _appliquer(g, FR, appeler(g, g.etat.theta_amont, theta_aval_fr, qreq, 2, rpui), rpui)
    if idencl:
        for g in G[ECS]:
            poids = [(1 - k.etat.ia_refroidi) * gen.ratpngen[(ECS, k)] for k in G[ECS]]
            qreq = (1 - g.etat.ia_refroidi) * gen.ratpngen[(ECS, g)] / sum(poids) * qar[ECS]                       # (1021)
            if not g.etat.ia_refroidi:
                iecs_seule = int(g.idfougen == 3 or not gen.aut_ch[j])
                iecs_fonction = _ecs_fonction(g.ihivernal, mois)
                if (qreq > 0 or iecs_seule) and iecs_fonction:
                    _appliquer(g, ECS, appeler(g, θamont, theta_aval_ecs, qreq, 3, 1.0, iecs_seule), 1.0)
    if gen.aut_ch[j]:
        for g in G[CH]:
            poids = [(1 - k.etat.ia_refroidi) * gen.ratpngen[(CH, k)] for k in G[CH]]
            qreq = (1 - g.etat.ia_refroidi) * gen.ratpngen[(CH, g)] / sum(poids) * qar[CH]                         # (1027)
            if not g.etat.ia_refroidi:
                rpui = 1 - g.etat.rfonct_ecs
                if rpui > 0: _appliquer(g, CH, appeler(g, θamont, theta_aval_ch, qreq, 1, rpui), rpui)
    return [qar[p] - sum(g.etat.qfou[p] for g in G[p]) for p in (CH, FR, ECS)]                                        # (1029)
```
Le texte ne dit pas ce que fait le mode sans priorité des générateurs d'un poste quand la saison est fermée : ils sont « désactivés », leur jeu de données reste à zéro.

Mise à jour du jeu de données (bloc « += » répété pages 653 à 664) :
```
def _appliquer(g, poste, r, rpui):
    g.etat.qcef[poste] += r.qcef[poste] ; g.etat.qcons += r.qcons ; g.etat.qfou[poste] += r.qfou
    g.etat.qprelec += r.qprelec ; g.etat.tau_charge += rpui * r.tau_charge ; g.etat.phi_rejet += r.phi_rejet
    g.etat.phi_vc += r.phi_vc ; g.etat.waux_pro += r.waux_pro ; g.etat.waux += r.waux ; g.etat.eta[poste] += r.eta
    if poste == ECS: g.etat.rfonct_ecs += r.rfonct_ecs
```

Cascade (1030 à 1035) : même structure, mais la boucle parcourt G[poste] trié par idpriorite croissant (ballons d'abord), qreq démarre à qar[poste] et devient r.qrest après chaque appel ; le report du poste est le dernier qrest. Si idrelance_ch et cascade : ignorer Qfou et Qcef(1;en) du générateur d'idpriorite_ch le plus élevé (règle p.648, voir points ouverts).

Alternance (1036 à 1053) : boucle sur G trié par puissance décroissante ; pour chaque gnr, seuil = rdim[gnr+1] x pngen[gnr+1] (0 pour le dernier) ; n_basculement = max(0, n_basculement - 1) si qreq ≤ seuil sinon N_BASCULEMENT_INIT ; appel si n_basculement > 0 ; en froid ia_refroidi = 1 ; en ECS iecs_seule = 1 et appel seulement si iecs_fonction ; en biposte (idfougen = 4) le test de seuil porte sur qreq_ch + qreq_ecs, l'ECS est servie d'abord (rpui = 1) puis le chauffage avec rpui = 1 - rfonct_ecs si iecs_seule = 0.

Imputation des auxiliaires amont (1056) :
```
def _imputer_aux_amont(g, w, aut_ch):
    e = g.etat ; col = ENERGIE[50]
    if e.ia_refroidi: e.qcef[FR, col] += w
    elif e.tau_charge > 0:
        part_ecs = e.rfonct_ecs / e.tau_charge
        e.qcef[FR, col] += (1 - part_ecs) * w        # texte : ligne 2 ; lecture physique : ligne CH (point ouvert)
        e.qcef[ECS, col] += part_ecs * w
    elif g.idfougen == 3 or not aut_ch: e.qcef[ECS, col] += w
    else: e.qcef[CH, col] += w
```

Histogramme (1523 à 1525) :
```
def _histogramme_charge(g, aut_ch, aut_fr, idencl):
    e = g.etat
    tau_ch = e.tau_charge if g.idfougen == 1 else (e.tau_charge - e.rfonct_ecs) if g.idfougen == 4 else (0.0 if e.ia_refroidi else e.tau_charge) if g.idfougen == 5 else None
    tau_fr = e.tau_charge if g.idfougen == 2 else (e.tau_charge if e.ia_refroidi else 0.0) if g.idfougen == 5 else None
    tau_ecs = e.tau_charge if g.idfougen == 3 else e.rfonct_ecs if g.idfougen == 4 else None
    for poste, tau, aut in ((CH, tau_ch, aut_ch), (FR, tau_fr, aut_fr), (ECS, tau_ecs, idencl)):
        if tau is None: continue
        if not aut: g.nbh[poste]['HF'] += 1
        elif tau <= 0: g.nbh[poste]['0'] += 1
        else: g.nbh[poste][classe(min(tau, 1.0))] += 1      # ]0;0,1], ]0,1;0,2] ... ]0,9;1]
```

Fin d'année (8.29) : Cef_po_gnr = somme des 12 mois (1496, 1503, 1510) ; Cep = même somme pondérée par COEF_EP ; ηeff_an = cumul_qfou / Cef (1527) ; Cef_x par énergie = somme sur les 3 postes (1530 à 1565) ; Cef_rdch, Cef_rdfr (1566 à 1569) ; Q_fou_3_postes = somme des trois cumuls (1522).

États conservés d'une heure à l'autre : gen.qrep (3), gen.theta_aval_prec (2), gen.nb_sousdim_ch et _fr, gen.sousdim (4 booléens définitifs), par générateur phi_rejet_prec, n_basculement, et tous les cumuls. États journaliers : aut_ch[j], aut_fr[j], idencl[j].
```

## Sorties RSEE pour le banc

- `O_Cef_ch_annuel` (Sortie_Groupe_C, kWh/m² (Cef_ch_gen,gr sommé sur les générations, 1501, divisé par la surface du groupe))
- `O_Cef_ch_elec_annuel, O_Cef_ch_gaz_annuel, O_Cef_ch_fioul_annuel, O_Cef_ch_bois_annuel, O_Cef_ch_reseau_annuel` (Sortie_Groupe_C, kWh/m² ; banc direct de la matrice Qcef(1;en)_gen,gr (1485) cumulée (1554 à 1559 restreintes au poste 1))
- `O_Cef_fr_annuel, O_Cef_fr_elec_annuel, O_Cef_fr_gaz_annuel, O_Cef_fr_reseau_annuel` (Sortie_Groupe_C, kWh/m² ; ligne 2 de la matrice (1486, 1508))
- `O_Cef_ecs_annuel, O_Cef_ecs_elec_annuel, O_Cef_ecs_gaz_annuel, O_Cef_ecs_fioul_annuel, O_Cef_ecs_bois_annuel, O_Cef_ecs_reseau_annuel` (Sortie_Groupe_C, kWh/m² ; ligne 3 (1487, 1515), inclut le réchauffeur de boucle (1058))
- `O_Cef_auxs_elec_annuel` (Sortie_Groupe_C, kWh/m² ; auxiliaires des systèmes (génération et sources amont, Waux_gnr réparti par groupe) ; à distinguer de O_Cef_aux_distribution_annuel et O_Cef_aux_ventilateur_annuel ; le périmètre exact est un point ouvert)
- `O_Cef_elec_annuel, O_Cef_gaz_annuel, O_Cef_fioul_annuel, O_Cef_bois_annuel, O_Cef_reseau_annuel` (Sortie_Groupe_C, kWh/m² ; Cef_x_gen,gr (1554 à 1559) plus les autres postes)
- `O_Cep_annuel, O_Cep_nr_Max, O_Cep_Max` (Sortie_Groupe_C, kWhep/m² ; Cep_x_gen,gr (1560 à 1565) avec Coefep)
- `O_Cef_elec_cons_ch_annuel, O_Cef_elec_cons_fr_annuel, O_Cef_elec_cons_ecs_annuel, O_Cef_gaz_imp_ch_annuel, O_Cef_gaz_imp_ecs_annuel, O_Cef_gaz_imp_fr_annuel, O_Cef_fioul_imp_ch_annuel, O_Cef_fioul_imp_ecs_annuel, O_Cef_reseau_imp_ch_annuel, O_Cef_reseau_imp_ecs_annuel, O_Cef_reseau_imp_fr_annuel, O_Cef_bois_imp_ch_annuel, O_Cef_bois_imp_ecs_annuel` (Sortie_Zone_C, kWh/m² ; matrice Qcef par poste et énergie agrégée à la zone (cons = consommée, imp = importée après autoconsommation))
- `O_Cef_elec_cons_auxdist_annuel, O_E_ef_aux_zone` (Sortie_Zone_C, kWh/m² et kWh ; auxiliaires (contrôle de Waux))
- `O_Cef_boisbuchchaud_imp_ch_annuel, O_Cef_boisgranchaud_imp_ecs_annuel, etc.` (Sortie_Zone_C et Sortie_Batiment_C, kWh/m² ; ventilation du bois par type de combustible et de générateur (chaudière, poêle) : au-delà du texte 8.29, à alimenter par idtype_gnr)
- `O_Cef_imp_ch_annuel, O_Cef_imp_fr_annuel, O_Cef_imp_ecs_annuel, O_Cef_elec_imp_ch_annuel, O_Cef_elec_AC_ch_annuel, O_Cef_Ch_comb_bat, O_Cef_ECS_comb_bat` (Sortie_Batiment_C, kWh/m² ; totaux bâtiment par poste ; _comb_bat : part combustible (gaz, fioul, bois) du chauffage et de l'ECS)
- `generateur_principal_ch, generateur_principal_ecs, generateur_principal_fr` (Sortie_Batiment_C, code ou libellé du générateur principal ; permet de vérifier le tri par Qfou_3postes ou par Pngen)
- `O_E_ef_aux_bat` (Sortie_Batiment_C, kWh)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch, O_Idsousdim_Court_Fr, O_Idsousdim_Long_Fr` (Sortie_Generation, booléen (0/1) ; équations 1061, 1062, 1064, 1065)
- `O_Idsousdim_Court_Ch_BE, O_Idsousdim_Long_Ch_BE, O_Idsousdim_Court_Fr_BE, O_Idsousdim_Long_Fr_BE` (Sortie_Generation, booléen ; variante boucle d'eau (fiche 8.15), hors champ)
- `Nbhcharge_HF_ch, Nbhcharge_0_ch, Nbhcharge_0_10_ch ... Nbhcharge_90_100_ch` (Sortie_Generation > Sortie_Generateur_Collection > Sortie_Generateur (aussi sous Sortie_Production_Stockage > Sortie_Generateur_Collection pour les générateurs des ballons), heures (entier) ; équation 1523 ; leur somme vaut 8760, ce qui contrôle Autch_gen(j) jour par jour)
- `Nbhcharge_HF_fr, Nbhcharge_0_fr ... Nbhcharge_90_100_fr` (Sortie_Generateur, heures ; équation 1524 ; Nbhcharge_HF_fr contrôle Autfr_gen(j))
- `Nbhcharge_HF_ECS, Nbhcharge_0_ECS ... Nbhcharge_90_100_ECS` (Sortie_Generateur, heures ; équation 1525 ; Nbhcharge_HF_ECS contrôle idencl_gen(j))
- `Q_fou_3_postes` (Sortie_Generateur, Wh ou kWh (unité à vérifier sur un RSEE : équation 1522 donne des Wh))
- `NbReports_ECS` (Sortie_Generateur, nombre d'heures (entier) où Qrep_ecs > 0 : contrôle direct du mécanisme de report (1017, 1035, 1043, 1053))
- `IsChaudiereGaz, IsReliePrechauffageCW` (Sortie_Generateur, booléens descriptifs (type 100 à 102 ; préchauffage))

## Points ouverts (à trancher au codage)

- Lecture de Idraccord_Reseau_Gen : le texte (p.531) code 0 = avec possibilité d'isolement, 1 = permanent ; les deux RSEE lus portent 0, or banc/cep.py applique aujourd'hui l'union des saisons du bâtiment (comportement « permanent ») et le README le présente comme fondé sur le banc. Déduction à faire sur Nbhcharge_HF_ch de Sortie_Generateur (= nombre d'heures où Autch_gen(j) = 0) comparé aux saisons propres recalculées : si HF_ch correspond à l'union des groupes, le logiciel évalué traite 0 comme permanent (ou ignore le champ).
- Les équations 840 à 844, 1485 à 1494, 1521, 1523 à 1527 sont des images ou des formules éclatées en symboles dans le texte extrait : elles ont été reconstituées depuis la nomenclature et les fragments. Les bornes des classes de taux de charge (1523) sont illisibles (0 < τ ≤ 10 % ou 0 ≤ τ < 10 %) ; trancher en sommant Nbhcharge_0_ch et Nbhcharge_0_10_ch d'un générateur effet joule dont la charge horaire est reconstituable.
- Règle de relance en cascade (p.648, non numérotée) : « la chaleur fournie et la consommation du générateur avec idpriorite_ch le plus élevé n'est pas prise en compte » quand idrelance_ch_gen(h) = vrai. On ne sait pas si le générateur est appelé (et son Qrest propagé) puis effacé, ou s'il est sauté ; ni si « le plus élevé » désigne le dernier de la cascade (appoint) ou le premier. Banc : NbReports_ECS et O_Idsousdim_Court_Ch (1060 exclut explicitement les heures de relance) sur un projet chaudière + appoint en cascade.
- Équation 1056, branche « τcharge > 0 sans ia_refroidi » : le texte impute la part non ECS des auxiliaires amont à Qcef(2;50) (froid) alors que le générateur n'a pas refroidi ; la logique de l'alinéa voisin (charge nulle : Qcef(1;50)) suggère la ligne 1. Banc : O_Cef_fr_elec_annuel d'un groupe à PAC chauffage seule non réversible (rsee_b, PAC CH bureaux) doit être nul si la ligne 1 est la bonne.
- Condition de l'appel en froid « Qreq > 0 ou idfougen ≠ 5 ou Autch_gen(j) ≠ 1 » (1025, 1033) : telle quelle, tout générateur de froid non réversible est appelé même à charge nulle en saison de froid (consommations résiduelles comptées en froid) ; un réversible à charge nulle n'est appelé en froid que hors saison de chauffage, sinon ses résiduelles vont au chauffage (p.645). Banc : Nbhcharge_0_fr d'une PAC réversible comparé aux heures de saison de froid sans demande.
- Température aval en refroidissement à la température des réseaux (1012) : le texte prend max(θmoy_dp) alors qu'en froid la contrainte est la température la plus basse ; et la dernière branche écrit idfonction_dp = 1. Appliquer max sur les réseaux de froid comme écrit, et tester sur les sorties de la famille générateurs (COP horaire non disponible dans les RSEE : seul O_Cef_fr_elec_annuel permet un contrôle indirect).
- Coquilles du texte à ne pas reproduire : Qfou_fr += Qfou et ηeff_fr dans les étapes chauffage (p.655, 658), Qfou_ecs dans l'alternance froid et chauffage (p.660, 662, 664), Qrep_tot_ar pour Qreq_tot_ar (1030, 1031, 1036 à 1051), Rreq = Rrest pour Qreq = Qrest (p.656 à 658), θaval_ch pour θaval_ecs (1010) et pour θaval_fr (p.660), idfougen = 4 décrit comme « chauffage et refroidissement » dans l'interdiction du mode alterné (p.659) alors que 4 = chauffage et ECS et que le paragraphe 8.17.3.7.2.3.4 traite justement idfougen = 4 : l'interdiction vise idfougen = 5.
- Codage de ihivernal : la nomenclature donne 1 toute l'année, 2 hivernal, 3 estival (p.635) ; l'algorithme teste 0, 1 et 2 (p.653). Aucun champ XML correspondant n'a été vu dans les deux RSEE (générateurs ECS des ballons) : la valeur par défaut « toute l'année » est retenue. Banc : Nbhcharge_HF_ECS doit alors ne compter que les jours où idencl_gen(j) = 0.
- Type de réseau idtype_dp (fictif ou hydraulique) : les nœuds Distribution_Intergroupe_Chaud lus ne portent que Type_Prim (0) et des longueurs nulles ; la nature fictive est à déduire de Type_Prim ou du fluide aval des générateurs (idfluide_aval, lui non plus pas lu directement : Sys_Thermo_Ch = 2 pour une PAC air/air recyclé, Theta_Aval_Air_Exterieur_Air_Recycle = 1). Règle proposée : réseau fictif si tous les générateurs du poste sont sur air ; à confirmer avec la famille distribution.
- Puissance nominale Pngen des PAC : Pmax existe pour l'effet joule (W) ; pour les PAC les RSEE donnent Val_Pabs et Val_Cop (kW, valeur pivot) ou des matrices Performance et Pabs par couple de températures : Pngen = Pabs x COP au point pivot, en W. À confirmer avec la famille générateurs thermodynamiques ; le mode alterné et le mode sans priorité en dépendent directement, la cascade non.
- Périmètre de O_Cef_auxs_elec_annuel (Sortie_Groupe_C) : auxiliaires des systèmes (génération + sources amont, Waux_gnr) ou tous auxiliaires hors ventilateurs et distribution ? Banc : comparer à Σ Waux_gnr x Ratbes sur un projet à PAC avec Ppompes nulles (seul l'auxiliaire propre reste).
- Répartition de Φvc_tot aux groupes : la fiche 8.14 (p.610) la renvoie à la fiche « Calcul des pertes et consommations récupérables », transmise au pas h+1 au prorata de Ratsurf_gen,gr ; le facteur de récupération n'est pas dans cette famille. Les RSEE n'ont pas de sortie directe ; l'effet se voit dans O_B_Ch_annuel (besoins) des groupes du bâtiment Id_Bat quand Pos_Gen = 1.
- Fiche 8.4 : le calcul des saisons effectives suppose connues les saisons propres de tous les groupes du jour j à IHJ(h) = 1, alors que le calcul horaire du groupe du même jour en dépend : ordre d'exécution à fixer (passe journalière avant les groupes, comme le fait déjà banc/cep.py par deux passes annuelles).
- Unités des sorties Sortie_Generateur (Q_fou_3_postes en Wh ou kWh) et des O_Cef (kWh/m² de SHAB ou de SU selon l'usage, comme pour O_B_Ch_annuel) : à vérifier sur un RSEE avant d'écrire le banc.

## Tableaux en image dans le PDF

- Fiche 8.4, page 533 : équations 840 et 841 rendues en symboles dispersés (illisibles en texte, reconstituées) ; page 534 : équations 842 à 844 idem ; figure 92 (p.530) et figure 93 (p.533) : schémas.
- Fiche 8.14, page 609 : figure 103 « Assemblage de la génération » (schéma, légendes mélangées au texte).
- Fiche 8.17, pages 632 et 633 : figures 107, 108, 109 (schémas des trois modes de régulation) ; page 645 : figure 110 « Ordre des calculs dans la génération » ; page 646 : figure 111 « Jeu de données » (lisible partiellement) ; page 652 : figure 112 « Fonction AppelGenerateur ». Les équations 981 à 1065 sont lisibles. Tableau 111 (nomenclature, p.634 à 641) et tableau 112 (types de générateurs, p.643 et 644) lisibles.
- Fiche 8.29, page 925 : tableau 252 (coefficients Coefep) et tableau 253 (matrice Qcef) lisibles mais mis en page en colonnes ; équations 1485 à 1487 (p.925 et 926), 1488 à 1494 (p.927), 1495 à 1515 (p.928 à 931), 1516 à 1521 (p.932), 1522 (p.933), 1523 (p.933 et 934), 1524 (p.934), 1525 (p.935), 1526 à 1529 (p.936), 1530 à 1569 (p.937 à 939) : toutes sous forme d'images ou de formules éclatées en symboles sur plusieurs lignes ; seules les légendes (« Sous forme de résultats mensuels », « annuel total », « ne concerne que les générateurs thermodynamiques ») sont en texte. Les formules ont été reconstituées à partir des symboles et de la nomenclature du tableau 251 (p.919 à 924, lisible).

## Estimation

Volume : environ 650 à 850 lignes de Python pour la famille, réparties ainsi : saisons_effectives (fiche 8.4) 60 à 80 lignes, en remplacement de la boucle d'union de banc/cep.py ; classe Generation avec lecture des nœuds, contrôles de cohérence et ratios surfaciques 120 lignes ; calculs préliminaires horaires 100 lignes ; les trois modes de régulation 200 à 250 lignes (la cascade et le sans priorité se factorisent, l'alternance biposte reste à part) ; auxiliaires amont et post-traitement 60 lignes ; fiche 8.29 (répartition par groupe, cumuls, histogrammes, rendements annuels, sorties par énergie) 120 à 150 lignes ; banc banc/generation.py contre Sortie_Groupe_C (O_Cef_ch_*, O_Cef_ecs_*, O_Cef_fr_*) et Sortie_Generateur (Nbhcharge_*, Q_fou_3_postes, NbReports_ECS) 100 lignes.

Difficulté : élevée, non pas par les équations (sommes, ratios, boucles) mais par les dépendances : la famille n'est testable qu'avec au moins un générateur réel (8.18 effet joule, 30 lignes, suffit pour les sèche-serviettes de rsee_a et pour la base effet joule du ballon ECS de rsee_b), les distributions intergroupes (Qsys, θmoy, Adess, idrelance, idencl) et les besoins d'ECS horaires (ecs.py existe). Le premier banc raisonnable est la génération « effet joule sans priorité sur réseau fictif » : Qcef(1;50) = Qreq, Nbhcharge_HF_ch = heures hors saison, ce qui valide 8.4, 994 à 1005, 1018 à 1029, 1057, 1485, 1523 et les cumuls. Le second est la cascade ballon ECS + appoint. Les parties les plus incertaines (relance en cascade, imputation 1056, θaval froid, Pngen des PAC) touchent peu ces deux cas. Compter deux à trois jours de travail pour le cœur et le banc, hors fiches générateurs et distributions.
