# Spécification : Eau chaude sanitaire : émission, distribution, stockage

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille couverte : la chaîne ECS du besoin horaire (déjà codé, ecs.py, équations 1694 et 1695) jusqu'à la demande transmise aux générateurs, soit : (1) fiche 9.5 C_EMI_Emission_ECS, coefficient correctif corr_gr,em-e (déjà codé dans ecs.correction, à conserver) et température aux émetteurs ; (2) fiche 9.7 C_DIS_Distribution_ECS_du_groupe, pertes des tuyauteries internes au groupe par la méthode des bouchons d'eau froide, besoin majoré Qw_2nd-e ; (3) fiche 9.8 C_DIS_Distribution_ECS_intergroupe, réseau bouclé (pertes, réchauffeur, circulateurs) ou tracé (traceur électrique), besoin aux bornes de la génération Qw_prim-e, répartitions Ratsurfaces et Ratbesoins ; (4) fiche 9.9 C_STO_Ballon_de_stockage, ballon à 4 zones, UA_S selon statut (certifié, justifié, défaut tableaux 283 et 284), pertes par zone, effet piston, mélange, injection par échangeur ou par piquages, température vue par l'échangeur ; (5) fiche 9.10 C_STO_gestion_régulation_ballon, boucle itérative de puisage (Vp, report), programmation fp, enclenchement avec hystérésis, énergie requise Qreq_sto_base/ap, variante appoint séparé instantané, régulation optimisée de l'appoint (titre V, CET) ; (6) fiche 9.11 C_STO_échangeur_ballon, échangeur externe à plaques (NUT, efficacité) et échangeur interne (serpentin) ; (7) fiche 9.12 C_STO_Accumulateur_ECS_en_eau_technique (Type_accumulateur_ECS = 1 ou 2), débit de puisage conventionnel, UA_ech par inversion NUT (Brent), réchauffage de boucle, circulateur primaire ; (8) fiches 9.13 et 9.14 pour la couture ballon vers générateurs (Qreq_sto -> générateur, Qfou_sto, matrice Qcef de l'assemblage, Nbiter_vp, Vz,min, pertes récupérables Φvc_sto) ; (9) fiches 9.1 à 9.4 (assemblages), qui ne contiennent aucune équation : elles fixent seulement l'ordre d'appel émission -> besoins -> distribution du groupe -> distribution intergroupe -> gestion-régulation de la génération -> générateurs (instantanés, ballons, CESCI/CESCAI, mixte).

Hors champ et pourquoi : les modèles de générateurs eux-mêmes (effet Joule 8.18 ou Source_Ballon_Base_Effet_Joule, thermodynamique 8.23 et triple service T.ONE 8.23/9.22, chaudières), qui produisent la matrice {Qcef(poste;énergie)} à partir de Qreq_sto et θb_moy_ech : famille génération ; la gestion-régulation de la génération (8.17 : priorités, cascade, idencl_gen, θaval, Qrep_tot_ar_ecs) et les calculs génération (8.29 : Ratbes_ecs_gen,gr, Cef_ecs_gen,gr, qui fabriquent O_Cef_ecs_annuel par groupe) : seules les équations d'interface sont citées ; la boucle solaire (9.15), CESCI (9.16), CESCAI (9.17), SSC (9.18 à 9.20) : la fiche 9.3 renvoie à ces assemblages, ils relèvent d'un autre lot ; les récupérateurs de chaleur sur eaux grises (9.6.3.5, 9.21) : ecs.py lève déjà NotImplementedError, et le texte des fiches 9.9 (1775, 1776) ne fait que modifier θentrant ; le service chauffage du ballon (zp,ch, zinj,ch, Qreq_CH, deuxième boucle itérative de 9.14 étape 2) : Id_Fou_Sto = 3 dans les deux RSEE lus, la spécification garde les crochets pour Id_Fou_Sto = 4 mais ne les détaille pas ; les pertes récupérables dans le bilan thermique du groupe (11.1, Φvc_sto, Φpertes_vc_2nd-e, Φaux_vc) : elles alimentent le mode Th-C du groupe, pas O_Cef_ecs ; elles sont calculées ici et exposées comme sorties pour le lot chauffage.

## Entrées (RSEE)

- `Groupe/Emetteur_ECS_Collection/Emetteur_ECS` / `Rat_em_e` : Rat_em^gr,em-e (1674, 1675) ; réel 0..1 ; valeurs vues : 1
- `Emetteur_ECS` / `nb_lgt_gr_em_e` : Nb_logement^gr,em-e (tableau 273) ; entier ; valeurs vues : 7 ; 4 ; 0 (bureaux)
- `Emetteur_ECS` / `nb_maison_gr_e` : Nb_maison^gr,em-e ; entier ; valeurs vues : 0
- `Emetteur_ECS` / `nu_gr_em_e` : Nu^gr,em-e ; réel ; valeurs vues : 0 ; 241,24 (bureaux, m² SU)
- `Emetteur_ECS` / `part_em_e_melangeurs` : part_melangeur (1676) ; réel 0..1 ; valeurs vues : 0
- `Emetteur_ECS` / `part_em_e_mitigeur_thermo` : part_mitigeur (1676) ; réel 0..1 ; valeurs vues : 1
- `Emetteur_ECS` / `part_em_e_temporisateur` : part_temporisateur (1676) ; réel 0..1 ; valeurs vues : 0
- `Emetteur_ECS` / `app_ecs` : App_ecs, gain_app (tableau 276) ; code entier ; valeurs vues : 3 (logement) ; 1 (bureaux) ; correspondance 0:douches 5 %, 1:sabot 2,5 %, 2:standard 0, 3:grande -2,5 % déduite du banc (ecs.py GAIN_APPAREIL)
- `Emetteur_ECS` / `Nb_douches_bains_relies, Nb_douches_bains_non_relies, Nb_total_douches_bains, NB_rat_eviers_lavabos` : récupérateurs eaux grises (9.6.3.5, hors champ ; >0 lève NotImplementedError) ; entiers ; valeurs vues : 0
- `Emetteur_ECS/Distribution_Groupe_ECS` / `nb_dist_2nd_e` : nb_dist_2nd-e (1733, 1734) ; entier ; valeurs vues : 1
- `Distribution_Groupe_ECS` / `delta_lvc` : δlvc (1730) : texte 0 = valeur par défaut, 1 = saisie ; sens du code RSEE à trancher au banc ; booléen 0/1 ; valeurs vues : 1 (avec l_vc_2nd_e = 0)
- `Distribution_Groupe_ECS` / `l_vc_2nd_e` : Lvc_2nd-e ; réel m ; valeurs vues : 0
- `Distribution_Groupe_ECS` / `l_hvc_2nd_e` : Lhvc_2nd-e ; réel m ; valeurs vues : 0
- `Distribution_Groupe_ECS` / `d_int_2nd_e` : Dint_2nd-e (1731) : diviser par 1000 ; réel, mm dans le RSEE (12), m dans le texte ; valeurs vues : 12
- `Distribution_Groupe_ECS` / `Type_Dist_Primaire` : nature du réseau amont (0 = distribution intergroupe ECS ?) ; code ; valeurs vues : 0
- `Distribution_Groupe_ECS` / `Id_Dist_Primaire` : lien ds-e -> dp-e (clé vers Distribution_Intergroupe_ECS.Index) ; entier (Index) ; valeurs vues : 3 ; 7
- `Distribution_Groupe_ECS` / `Id_Ballon` : ballon décentralisé (CESCI/CESCAI), hors champ ; entier ; valeurs vues : 0
- `Entree_Projet/Distribution_Intergroupe_ECS_Collection/Distribution_Intergroupe_ECS` / `Type_Reseau_Intergroupe_ECS` : Type_reseau_intergroupe-e (0 aucun, 1 bouclé, 2 tracé) ; code 0/1/2 ; valeurs vues : 0 (pas de réseau) dans les deux RSEE
- `Distribution_Intergroupe_ECS` / `l_vc_prim_bcl_e, l_hvc_prim_bcl_e, l_vc_prim_trac_e, l_hvc_prim_trac_e` : Lvc_prim_bcl-e, Lhvc_prim_bcl-e, Lvc_prim_trac-e, Lhvc_prim_trac-e (1746, 1758) ; réels m ; valeurs vues : 0
- `Distribution_Intergroupe_ECS` / `u_prim_e` : Uprim-e (1745, 1757) ; réel W/(m.K) ; valeurs vues : 0
- `Distribution_Intergroupe_ECS` / `Is_Rechauf_Bcl_e` : Isrechauf_bcl-e (1747, 1753) ; booléen ; valeurs vues : 0
- `Distribution_Intergroupe_ECS` / `type_gest_circ_e` : Typegest_circ-e (1748, 1749) ; code 0/1 ; valeurs vues : 0
- `Distribution_Intergroupe_ECS` / `p_circ_prim_e` : Pcirc-e ; réel W ; valeurs vues : 0
- `Distribution_Intergroupe_ECS` / `Id_Gen` : lien dp-e -> gen (clé vers Generation.Index) ; entier (Index) ; valeurs vues : 1 ; 5
- `Distribution_Intergroupe_ECS` / `Id_PCAD` : production centralisée à appoints décentralisés (1742), hors champ ; entier ; valeurs vues : 0
- `Generation` / `Pos_Gen` : Idpos_gen (1962) ; détermine θamb du ballon ; booléen ; valeurs vues : 0 (hors volume chauffé)
- `Generation` / `Theta_Wm_Ecs` : θwm_ecs^gen (1010) ; candidat pour θdepart,aval,ECS et pour θ2nd-e (point ouvert) ; réel °C ; valeurs vues : 50 ; 54
- `Generation` / `Type_Priorite` : idtype_priorite^gen ; code ; valeurs vues : 2 (cascade, obligatoire avec stockage, 8.17)
- `Generation/Production_Stockage_ECS_Collection/Production_Stockage` / `Id_Fou_Sto` : id_fou_sto ; code 1/3/4 ; valeurs vues : 3
- `Production_Stockage` / `Type_prod_stockage` : Typeprod_stockage (tableau 292, 1951) ; code 0..3 ; valeurs vues : 1 (base + appoint intégré, CET T.ONE) ; 0 (base seule, effet Joule bureaux)
- `Production_Stockage` / `Type_accumulateur_ECS` : Type_Accumulateur_ECS (9.12) ; 1 et 2 déclenchent la fiche 9.12 ; code 0/1/2 ; valeurs vues : 0 (ballon ECS direct) dans les deux RSEE
- `Production_Stockage` / `nb_assembl` : nb_assembl (1953, 1961, 1962) ; entier ; valeurs vues : 28 (un CET par logement) ; 1
- `Production_Stockage` / `V_tot` : Vtot (1770, 1776 et suivantes) ; réel L ; valeurs vues : 175 ; 100
- `Production_Stockage` / `Statut_faux` : Statut_faux (texte : 1 saisie, 2 défaut 0,5) ; code 0 du RSEE à trancher ; code ; valeurs vues : 0
- `Production_Stockage` / `f_aux` : faux (V3 = V4 = faux·Vtot/2) ; réel 0..1 ; valeurs vues : 0,5 ; 0
- `Production_Stockage` / `Valeur_Certifiee_Justifiee_Defaut` : Statut_UA (1767 à 1769) ; la correspondance des codes est incohérente avec le texte dans les deux fichiers, à trancher au banc ; code 0/1/2 ; valeurs vues : 2 avec UA_S = 2,94 ; 0 avec UA_S = 0
- `Production_Stockage` / `Nature_Ballon` : ligne du tableau 283/284 (effet Joule horizontal, vertical >= 75 L, vertical < 75 L, autres, solaire) ; correspondance à déduire ; code ; valeurs vues : 1 ; 2
- `Production_Stockage` / `UA_S` : UAS (1767, 1768) ; réel W/K ; valeurs vues : 2,94 ; 0
- `Production_Stockage` / `Theta_Cons` : θc_base = θc_ap (1949 : 55 °C imposé si Id_Fou_Sto = 3) ; réel °C ; valeurs vues : 55
- `Production_Stockage` / `Theta_Max` : θmax (1780) ; réel °C ; valeurs vues : 90 ; 55
- `Production_Stockage` / `b_sto_e` : bsto-e, coefficient d'espace tampon du ballon (figure 198) ; usage non décrit dans les fiches lues ; réel ; valeurs vues : 0
- `Production_Stockage` / `V_tot_appoint, UA_S_appoint, Nature_Ballon_Appoint, Valeur_Certifiee_Justifiee_Defaut_Appoint, Theta_Max_appoint` : ballon secondaire (Type_prod_stockage = 2, 1950, 1951) ; réels / codes ; valeurs vues : 0
- `Production_Stockage` / `type_gest_th_base` : typegest_base (1811 à 1813 : 0 permanent, 1 nuit, 2 jour) ; code 0/1/2 ; valeurs vues : 2 (CET) ; 0 (effet Joule)
- `Production_Stockage` / `Statut_Delta_Theta_Base, Delta_Theta_base` : Statut_Δθbase, Δθbase (1814 ; défaut 2 K) ; code, réel K ; valeurs vues : 1 et 2 ; 2 et 2
- `Production_Stockage` / `hech_base` : hrelech_base (1782 à 1785) ; réel 0..1 ; valeurs vues : 0 ; 0,2
- `Production_Stockage` / `z_reg_base` : zreg_base (1814, 1815) ; entier 1..4 ; valeurs vues : 1
- `Production_Stockage` / `type_gest_th_appoint, Statut_Delta_Theta_Appoint, Delta_Theta_appoint, hech_appoint` : typegest_ap, Statut_Δθap, Δθap, hrelech_ap ; code, code, réel K, réel ; valeurs vues : 2, 1, 5, 0 ; 0, 2, 2, 0
- `Production_Stockage` / `z_appoint` : zap (zone basse de l'échangeur d'appoint, 1816) ; entier 1..4 ; valeurs vues : 1 (CET) ; 3
- `Production_Stockage` / `z_reg_appoint` : zreg_ap ; entier ; valeurs vues : 2 ; 0
- `Production_Stockage` / `Is_Retour_Boucle_Separe` : IsRetour,boucle,separe (tableau 288) ; booléen ; valeurs vues : 0
- `Production_Stockage` / `Pech_ECS, qv_prim_ECS, Type_Circulateur_Prep_ECS, Pw_circ_prim_ECS, Pw_circ_prim_RB` : PechECS, qv_prim_nom, Type_Circulateur_Prep_ECS, Pw_circ_prim_nom, Pw_circ_prim_RB (9.12) ; kW, m3/h, code, W, W ; valeurs vues : 0
- `Production_Stockage` / `Idpriorite_Ecs, Idpriorite_Ch, delta_reg_bcl_ch` : priorités de la génération (8.17), hors champ ; entiers ; valeurs vues : 1, 1, 2
- `Production_Stockage/Source_Ballon_Base_Collection/Source_Ballon_Base_*` / `Id_Fou_Gen, Pmax, Rdim, Val_Cop_Ecs, Performance_Ecs, Pabs_Ecs, COR_Ecs, Lim_Theta_Ecs, Theta_Max_Av_Ecs, Theta_Min_Am_Ecs` : générateur pour ballon (9.13) : reçoit Qreq_sto_base et θb_moy_ech ; modèle hors champ ; générateur de base (Effet_Joule : Pmax kW ; Thermodynamique_Elec_TripleService : matrices) ; valeurs vues : Pmax = 2 ; COP 3,5, Pabs 0,79, Theta_Max_Av_Ecs 25, Theta_Min_Am_Ecs -5
- `Production_Stockage/Source_Ballon_Appoint_Collection/Source_Ballon_Appoint_Effet_Joule` / `Pmax, Id_Fou_Gen` : générateur d'appoint (Qreq_sto_ap) ; kW, code ; valeurs vues : 1,5 ; 3
- `Zone` / `Usage` : Type_usage_z (tableaux 275, 280) et iecs(j) (47) ; code ; valeurs vues : 1, 2, 3
- `Groupe` / `SHAB ou SU` : Agr (1675) ; réel m² ; valeurs vues : 
- `Climat (meteo)` / `teau, te` : θcw(h) (1755, 1763), θext(h) (1734, 1745, 1757) ; séries horaires ; valeurs vues : 
- `Besoins du groupe (groupe.calculer, Th-C)` / `θi(h) = Temperatures.i` : θi(h) (1733, 1734) ; à exposer depuis groupe.py ; série horaire ; valeurs vues : 
- `Enveloppe / espaces tampons` / `b_tampons` : btherm(h) (1734, 1745, 1757) ; aucun champ b2nd-e / bprim-e vu dans les RSEE : prendre 1 hors volume chauffé ; réel ; valeurs vues : 

## Paramètres conventionnels

- θuw température de l'eau mitigée = 40 °C (p. 1019 (tableau 272), 1043 (tableau 279))
- θ2nd-e température de la distribution ECS du groupe = 48 °C selon tableau 272 ; 53 °C selon tableau 279 (contradiction, point ouvert) (p. 1019 et 1043)
- ρw·cw = 1 kg/L × 1,163 Wh/(kg.K) ; 998 kg/m3 dans les fiches 9.11 et 9.12 (volumes en m3) (p. 1043, 1062, 1075, 1087, 1099)
- gain_em par catégorie d'émetteur = 0 ; 0,05 ; 0,07 (tableau 274) (p. 1021)
- Rat_douches-bains = 80 % habitation, 50 % bureaux, 0 % autres (tableau 275) (p. 1022)
- gain_app = douches 5 %, sabot 2,5 %, standard 0, grande baignoire -2,5 % (tableau 276) (p. 1022)
- Lvc_2nd-e par défaut = 6 × A_gr,em-e / 80 en habitation ; 0,05 × A_gr,em-e autres usages (1730) (p. 1045)
- nb_bouchons = 3 (maison), 3 (collectif), 2 (enseignement primaire), 3 (secondaire jour), 2 (bureaux) ; tableau 280, autres usages non donnés (p. 1046)
- Fonction_prim ECS = 3 (1736) (p. 1051)
- θretour boucle = θdépart - 5 K (1743) (p. 1052)
- θamb des réseaux intergroupes en volume chauffé = 20 °C (1746, 1758) (p. 1053, 1056)
- Pcirc_vc-e part récupérable des circulateurs = 0 (1752, 1761) (p. 1050, 1054, 1056)
- Nzone = 4 (p. 1059, 1063)
- faux par défaut (Statut_faux = 2) = 0,5 (p. 1063)
- UAS justifié = 1,1 × UAS (1768) (p. 1063)
- Qpr par défaut (tableau 283) = effet Joule horizontal 0,939 + 0,0104·Vtot ; vertical >= 75 L 0,224 + 0,0663·Vtot^(2/3) ; vertical < 75 L 0,1474 + 0,0719·Vtot^(2/3) ; autres 0,189·Vtot^0,55 (kWh/jour, Vtot en L) (p. 1063)
- UAS_util depuis Qpr = Qpr × 1000 / (45 × 24) (1769) (p. 1064)
- UAS_util ballon solaire (tableau 284) = 0,16 × Vtot^0,5 (p. 1064)
- θbz initiale = 50 °C au premier pas de temps (p. 1064)
- zp,ecs / zinj,ecs = 4 / 1 (1773) (p. 1065)
- zp,base / zinj,base = 1 / 4 (piquages haut et bas) (p. 1061)
- zbase = 1 (1948) (p. 1127)
- θc_base = θc_ap si Id_Fou_Sto = 3 = 55 °C (1949) (p. 1127)
- Δθbase par défaut (statut 2) = 2 K (p. 1082)
- θc_base/ap valeur conventionnelle de la nomenclature = 55 °C (p. 1074)
- Période nuit (gestion 1) = hleg > 23 h ou < 5 h ; période jour (gestion 2) : 10 h < hleg < 17 h (p. 1081)
- Réinitialisation des booléens de la régulation optimisée = chaque jour à hleg = 6 h (p. 1084)
- Débit secondaire d'un échangeur ECS (9.10) = qv_boucle,ecs + 12 × Vef_ECS (1810) (p. 1080)
- h_haut,ech,rel / h_bas,ech,rel échangeur interne (9.11) = 100 % / 25 % par défaut (p. 1092)
- Pas d'itération énergétique échangeur interne = Qiter = Vtot·ρ·c·2 °C (1854, 1932) (p. 1093, 1115)
- Puisage significatif (9.12) = 6 L/min pendant 8 min à 40 °C ; 0,13 h par puisage ; Y = 0,8/√(N-1) (p. 1101, 1102)
- θcons eau technique = 55 °C individuel (Vtot < 500 L ou un ballon par logement), 60 °C collectif (tableau 289) (p. 1104)
- Conditions nominales de PechECS = primaire θcons, eau froide 15 °C, ECS θcons - 5 (p. 1104, 1114)
- UAech initial (Brent) = 50 × PechECS (W/K), critère |Δε| < 0,01 (p. 1105)
- Modmin = 0,3 (p. 1097)
- zretour,ech,ext / zretour,ech_boucle / z_bas,ech / z_haut,ech (tableau 288) = 1 / 1 ou 3 selon Is_Retour_Boucle_Separe / 1 / 4 (p. 1104)
- Alerte report = 24 h (1781, 9.9) ; 12 h erreur bloquante (9.12) ; 168 h sans atteinte de consigne (1960) (p. 1067, 1111, 1132)
- Nbiter_vp = 4 (base seule, appoint instantané ; valeur illisible dans le texte, déduite) ; arrondi inférieur de 2/min(faux, 1-faux) (appoint intégré) ; arrondi inférieur de (Vtot_princ + Vtot_sec)/Vz,min (ballon séparé) (1951) (p. 1128)

## Équations

- (1674, p. 1021) Σ_{em-e ∈ gr} Rat_em^gr,em-e = 1 ; Rat_em_e ; contrôle de saisie ; erreur sinon
- (1675, p. 1021) A_gr,em-e = Rat_em^gr,em-e × A_gr ; A_gr = SHAB (usages 1, 2) ou SU ; 
- (1676, p. 1021) M_part_em = [part_melangeur ; part_mitigeur ; part_temporisateur], somme = 1 ; part_em_e_* ; 
- (1677, p. 1022) corr_em = 1 - Σ_i M_part_em(i) × gain_em(i) ; gain_em = (0 ; 0,05 ; 0,07) ; déjà codé (ecs.correction)
- (1678, p. 1022) corr_app = 1 - Rat_douches-bains(usage) × gain_app(App_ecs) ; tableaux 275, 276 ; déjà codé
- (1679, p. 1023) corr_gr,em-e = corr_app × corr_em ;  ; multiplie les besoins 1694
- (1680, p. 1023) θec^gr,em-e = θ2nd-e^gr ; erreur si θec < θuw ; θ2nd-e ; 
- (1730, p. 1045) si δlvc = 0 : Lvc_2nd-e = 6 × A_gr,em-e / 80 (habitation) ou 0,05 × A_gr,em-e (autres) ; sinon Lvc_2nd-e saisi (seule la valeur saisie est multipliée par nb_dist_2nd-e) ; delta_lvc, l_vc_2nd_e ; 
- (1731, p. 1045) Vvc_2nd-e = Lvc_2nd-e × π·Dint² / 4 × 1000 ; Vhvc_2nd-e = Lhvc_2nd-e × π·Dint² / 4 × 1000 (L, Dint en m) ; d_int_2nd_e / 1000 ; 
- (1732, p. 1046) Is_successif(h) = 1 si Qw(h-1) = 0 et Qw(h) ≠ 0 ; = (nb_bouchons - 1)/nb_bouchons si Qw(h-1) ≠ 0 et Qw(h) ≠ 0 ; = 0 sinon ; Qw^gr,em-e besoins horaires 1694 ; la condition du second cas est partiellement illisible (image), reconstituée
- (1733, p. 1046) Φpertes_vc_2nd-e(h) = ρw·cw·Vvc_2nd-e × (θ2nd-e - θi(h)) × nb_bouchons × Is_successif(h) × nb_dist_2nd-e ; θi(h) du groupe ; 
- (1734, p. 1046) Φpertes_hvc_2nd-e(h) = ρw·cw·Vhvc_2nd-e × max(0 ; θ2nd-e - (btherm·θext + (1 - btherm)·θi)) × nb_bouchons × Is_successif × nb_dist_2nd-e ; btherm, θext ; 
- (1735, p. 1046) Qw_2nd-e(h) = Qw^gr,em-e(h) + Φpertes_vc_2nd-e(h) + Φpertes_hvc_2nd-e(h) ;  ; 
- (1736, p. 1051) Fonction_prim = 3 ;  ; 
- (1737, p. 1051) idencl-e(j) = 1 s'il existe ds-e ∈ dp-e avec iecs^ds-e(j) = 1, sinon 0 ; iecs(j) de (47) : 0 si enseignement en vacances, 1 sinon ; équation en image, reconstituée
- (1738, p. 1051) Ratsurfaces_prim_e^gr = Σ_{em-e ∈ gr, em-e ∈ dp-e} A_gr,em-e / Adess_e ;  ; 
- (1739, p. 1052) Adess_e = Σ_{em-e ∈ dp-e} A_gr,em-e ;  ; 
- (1740, p. 1052) Ratbesoins_prim_e^gr(h) = Σ_{ds-e ∈ gr} Qw_2nd-e(h) / Σ_{ds-e ∈ dp-e} Qw_2nd-e(h) ; si dénominateur nul : = Ratsurfaces_prim_e^gr ;  ; 
- (1741, p. 1052) θdépart_prim-e = max_{ds-e}(θ2nd-e^ds-e) ;  ; bouclé
- (1742, p. 1052) θdépart_prim-e(h) = θb4^centr(h-1) ;  ; PCAD seulement (Id_PCAD ≠ 0), hors champ
- (1743, p. 1052) θretour_prim-e = θdépart_prim-e - 5 ;  ; bouclé
- (1744, p. 1052) θmoy_prim-e = (θdépart + θretour)/2 ;  ; bouclé
- (1745, p. 1053) φpertes_vc_prim-e(h) = Uprim-e × Lvc_prim-e × (θmoy - θamb) × idencl-e(j) ; φpertes_hvc_prim-e(h) = Uprim-e × Lhvc_prim-e × idencl-e(j) × (θmoy - (θamb + btherm(h)·(θext(h) - θamb))) ; Wh par heure (W × 1 h) ; bouclé
- (1746, p. 1053) θamb = 20 °C ; Lvc_prim-e = Lvc_prim_bcl-e ; Lhvc_prim-e = Lhvc_prim_bcl-e ;  ; bouclé
- (1747, p. 1053) Wrechauf_prim-e(h) = 0 si Isrechauf = 0 ; = φpertes_vc_prim-e + φpertes_hvc_prim-e si Isrechauf = 1 ; électricité, auxiliaire ; bouclé
- (1748, p. 1053) si typegest_circ = 1 : Wcirc_prim-e(h) = Pcirc-e × 1 h si idencl-e(j) = 1, sinon 0 ;  ; bouclé
- (1749, p. 1054) si typegest_circ = 0 : Wcirc_prim-e(h) = Pcirc-e × 1 h ;  ; bouclé
- (1750, p. 1054) Waux_prim-e^dp-e(h) = Wcirc_prim-e(h) ;  ; bouclé
- (1751, p. 1054) Waux_prim-e^dp-e,gr(h) = Waux_prim-e^dp-e(h) × Ratsurfaces_prim_e^gr ;  ; bouclé
- (1752, p. 1054) Φaux_vc(h) = Pcirc_vc-e × Waux_prim-e^dp-e(h) = 0 ; Pcirc_vc-e = 0 ; 
- (1753, p. 1054) Qw_prim-e(h) = Σ_{ds-e} Qw_2nd-e(h) + φpertes_vc_prim-e + φpertes_hvc_prim-e si Isrechauf = 0 ; = Σ Qw_2nd-e si Isrechauf = 1 ;  ; bouclé
- (1754, p. 1055) θdépart_prim-e = max_{ds-e}(θ2nd-e) ;  ; tracé
- (1755, p. 1055) θretour_prim-e = θcw(h) ;  ; tracé
- (1756, p. 1055) θmoy_prim-e = θdépart_prim-e ;  ; tracé
- (1757, p. 1055) φpertes_vc_prim-e = Uprim-e × Lvc_prim-e × (θdépart - θamb) × idencl ; φpertes_hvc_prim-e = Uprim-e × Lhvc_prim-e × idencl × (θdépart - (θamb + btherm·(θext - θamb))) ;  ; tracé
- (1758, p. 1056) θamb = 20 °C ; Lvc_prim-e = Lvc_prim_trac-e ; Lhvc_prim-e = Lhvc_prim_trac-e ;  ; tracé
- (1759, p. 1056) Waux_prim-e^dp-e(h) = Wtrac_prim-e(h) = φpertes_vc_prim-e + φpertes_hvc_prim-e ; électricité, auxiliaire ; non ajouté à Qw_prim ; tracé
- (1760, p. 1056) Waux_prim-e^dp-e,gr(h) = Waux_prim-e^dp-e(h) × Ratsurfaces_prim_e^gr ;  ; tracé
- (1761, p. 1056) Φaux_vc(h) = Pcirc_vc-e × Waux = 0 ;  ; tracé
- (1762, p. 1056) Qw_prim-e(h) = Σ_{ds-e} Qw_2nd-e(h) ;  ; tracé
- (1763, p. 1057) θdépart_prim-e = max(θ2nd-e) ; θretour_prim-e = θcw(h) ; θmoy_prim-e = θdépart_prim-e ;  ; Type_Reseau_Intergroupe_ECS = 0
- (1764, p. 1057) φpertes_vc_prim-e = φpertes_hvc_prim-e = 0 ;  ; type 0
- (1765, p. 1057) Qw_prim-e(h) = Σ_{ds-e} Qw_2nd-e(h) ;  ; type 0
- (1766, p. 1057) Waux_prim-e^dp-e = Waux_prim-e^dp-e,gr = 0 ; Φaux_vc = 0 ;  ; type 0
- (1767, p. 1063) UAS_util = UAS ;  ; statut certifié
- (1768, p. 1063) UAS_util = 1,1 × UAS ;  ; statut justifié
- (1769, p. 1064) UAS_util = Qpr × 1000 / (45 × 24), Qpr du tableau 283 selon Nature_Ballon ; ballon solaire : UAS_util = 0,16·Vtot^0,5 (tableau 284) ; Vtot en L ; statut par défaut
- (1770, p. 1064) Uz = UAS_util × Vz / Vtot ;  ; 
- (répartition des zones (texte 9.9.3.1), p. 1063, 1103, 1113) sans appoint : Vz = Vtot/4 ; avec appoint : V4 = V3 = faux·Vtot/2 = Vap/2, V1 = V2 = (1 - faux)·Vtot/2 ; eau technique (1875, 1876, 1922, 1923) : Vz = Vtot/4 quel que soit faux ; faux (défaut 0,5) ; 
- (1771, p. 1064) Φpertes,z(h) = Uz × (θbz(h-1) - θamb(h)) ; W ; calculé avec les températures de fin du pas précédent
- (1772, p. 1064) Φpertes(h) = Σ_z Φpertes,z(h) ; récupérable si génération en volume chauffé ; 
- (1773, p. 1065) zp,ecs = 4 ; zinj,ecs = 1 ;  ; 
- (1774, p. 1065) θb_zinj(i) = (θb_zinj(i-1)·(V_zinj - Vp) + θentrant(h)·Vp) / V_zinj ; Vp = Vp(i) de la gestion-régulation ; puisage direct ou échangeur externe
- (1775, p. 1066) θentrant(h) = θpréchauffée,ecs(h) ;  ; récupérateur eaux grises position 0 ou 1, hors champ
- (1776, p. 1066) θentrant(h) = θentrant,ecs(h) ;  ; pas de récupérateur ou position 2
- (1777, p. 1066) pour z de zinj+1 à zp : θbz(i) = (θbz(i-1)·(Vz - Vp) + θb(z-1)(i-1)·Vp) / Vz ; effet piston ; 
- (1778, p. 1066) pour z de z_bas,ech à z_haut,ech : θb[z](i) = θb[z](i-1) - Qprel[z](i) / (V[z]·ρw·cw) (le facteur 1/3600 du texte vaut pour des unités SI ; en Wh et L il disparaît) ; Qprel de 9.11 (1861 ou 1939) ; échangeur interne
- (1779, p. 1066, 1067) mélange : a = 1 ; tant que θb_a ≤ θb_(a+1) ≤ ... n'est pas vérifié : si θb_a(i) > θb_(a+1)(i) : si moyenne volumique des zones a..a+1 > θb_(a+2) : si moyenne a..a+2 > θb_(a+3) : égaliser a..a+3 à la moyenne volumique, a = 1 ; sinon égaliser a..a+2, a = 1 ; sinon égaliser a..a+1, a = 1 ; sinon a = a + 1 ; moyenne volumique = Σ Vj·θbj / Σ Vj ; bornes a+k ≤ Nzone ; algorithme partiellement en image, reconstitué
- (1780, p. 1067) θbz(i) = min(θbz(i), θmax) pour z = 1..4 ; Theta_Max ; 
- (1781, p. 1067) nbh_report(h) = nbh_report(h-1) + 1 si Qw_sto_unit_report(h) ≠ 0, sinon inchangé ; alerte si > 24 ;  ; 
- (1782, p. 1068) zech = zbase, hrelech = hrelech_base (base) ou zech = zap, hrelech = hrelech_ap (appoint) ; hrel_z = Vz/Vtot ; si hrelech = 0 (ou ≤ hrel_zech) : zmax_ech = zech, hrelrest = hrelech ; hech_base, hech_appoint ; 
- (1783, p. 1068) sinon pour j = 1..Nzone - zech : si hrelech ≤ Σ_{z=zech}^{zech+j} hrel_z : zmax_ech = zech + j, hrelrest = hrelech - Σ_{z=zech}^{zmax_ech-1} hrel_z, sortie ; sinon j += 1, erreur si j dépasse (échangeur trop haut) ;  ; 
- (1784, p. 1068) θb_moy_ech(h) = θ̄b(zech) ;  ; hrelech = 0
- (1785, p. 1069) θb_moy_ech(h) = (Σ_{z=zech}^{zmax_ech-1} hrel_z·θ̄bz + hrelrest·θ̄b(zmax_ech)) / hrelech ;  ; hrelech ≠ 0
- (1786, p. 1069) θ̄bz = (θbz(h-1) + θbz(i-1)) / 2, où i-1 est l'état après puisage et avant injection ;  ; 
- (1787, p. 1069) pour i ≥ Nbiter_vp + 1 : θbz(i) = θbz(i-1) + (Qinj,z - Φpertes,z) / (ρw·cw·Vz) ; Qinj,z = énergie fournie par le générateur dans la zone zbase (ou zap) ; Φpertes,z en Wh (× 1 h) ; apport par échangeur intégré ; Φpertes,z mis à 0 si déjà comptées (voir assemblage)
- (1788, p. 1070) v_inj = Qfou,sto,base(h) / (ρw·cw·(θinjecte,base(h) - θb[zp,base](i-1))) ; L (facteur 1/3600 du texte en unités SI) ; TypeRaccordement_Base_Ballon = 1 (piquages), interdit si Typeprod_stockage = 2 ; appliquer d'abord 1787 sans Qinj
- (1789, p. 1070) n = k = Nzone ; tant que v_inj ≥ V[n] : θb[n](i) = θinjecte ; pour k = n-1..1 : θb[k](i) = θb[k+1](i-1) ; si θb[zp,base](i) < θinjecte : v_inj -= V[n], n -= 1 ; sinon v_inj = 0 et arrêt ; θb(i-1) ← θb(i) ;  ; piquages haut et bas
- (1790, p. 1071) k = n : θb[k](i) = (v_inj·θinjecte + (V[k] - v_inj)·θb[k](i-1)) / V[k] ; puis pour k décroissant : θb[k](i) = (v_inj·θb[k+1](i-1) + (V[k] - v_inj)·θb[k](i-1)) / V[k] ; reste de volume injecté ; piquages haut et bas
- (1791, p. 1071) θbz(h) = θbz(i_fin) après mélange (1779) ;  ; 
- (1792, p. 1077) puisage ECS : zp(i) = zp,ecs = 4 ; θentrant(i) = θentrant,ecs(h) ; θcons,sortie(i) = θdepart,aval,ecs(h) ;  ; 
- (1793, p. 1077) puisage chauffage : zp(i) = zp,ch ; θentrant(i) = θentrant,ch(h) ; θcons,sortie(i) = θdepart,aval,ch(h) ;  ; Id_Fou_Sto = 1 ou 4, hors champ
- (1794, p. 1077) i = 1 : Qw_sto_unit(1) = Qw_sto_unit(h) ; Qw_sto_unit(h) = Qreq,ECS(h)/nb_assembl (1953), report compris ; 
- (1795, p. 1077) si θb,zp(h-1) > θcons,sortie(i) : Vp(i) = min(Qw_sto_unit(i) / (ρw·cw·(θb,zp(h-1) - θentrant(i))) ; min_z Vz) ; Qw_sto_unit_report(i) = Qw_sto_unit(i) - ρw·cw·Vp(i)·(θb,zp(h-1) - θentrant(i)) ;  ; ballon ECS direct, première itération
- (1796, p. 1077) sinon Vp(i) = 0 ; Qw_sto_unit_report(i) = Qw_sto_unit(i) ;  ; 
- (1797, p. 1077) tant que 1 < i ≤ Nbiter_vp et report(i-1) ≠ 0 : Qw_sto_unit(i) = Qw_sto_unit_report(i-1) ;  ; 
- (1798, p. 1078) si θb,zp(i-1) > θcons,sortie : Vp(i) = min(Qw_sto_unit(i)/(ρw·cw·(θb,zp(i-1) - θentrant)) ; min Vz) ; report(i) = Qw_sto_unit(i) - ρw·cw·Vp(i)·(θb,zp(i-1) - θentrant) ;  ; itérations suivantes ; recalcul 1774, 1777, 1779, 1780 après chaque itération
- (1799, p. 1078) sinon Vp(i) = 0 ; report(i) = Qw_sto_unit(i) ;  ; 
- (1800, p. 1078) Vp(h) = Σ_{i=1}^{Nbiter_vp} Vp(i) ; report(Nbiter_vp) est reporté au pas suivant ;  ; 
- (1801 à 1808, p. 1078, 1079) appoint séparé instantané : i = 1, Qw_sto_unit(1) = Qw_sto_unit(h) (1801) ; si θb,zp ≥ θcons,sortie : comme 1795 (1802, 1806) ; sinon si θb,zp > θentrant : Vp(i) = min(Qw_sto_unit(i)/(ρw·cw·(θcons,sortie - θentrant)) ; min Vz), report(i) = Qw_sto_unit(i) - ρw·cw·Vp(i)·(θb,zp - θentrant), puis arrêt de la boucle (1803, 1807) ; sinon Vp = 0, report = Qw_sto_unit (1804, 1808) ; 1805 identique à 1797 ;  ; Typeprod_stockage = 3
- (1809, p. 1080) qv_aval(h) = qv_ch(h) ;  ; échangeur chauffage, hors champ
- (1810, p. 1080) qv_aval(h) = qv_boucle,ecs(h) + 12 × Vef_ECS(h) ; m3/h ; en cas de report avec débit nul, garder les dernières valeurs non nulles de qv_boucle, Vef, θentrant, θdepart,aval ; échangeur ECS (9.11)
- (1811, p. 1081) typegest = 0 : fp(h) = 1 ;  ; 
- (1812, p. 1081) typegest = 1 (nuit) : fp(h) = 1 si hleg > 23 ou hleg < 5, sinon 0 ; hleg heure légale (cal.case - 1 dans openBCE) ; 
- (1813, p. 1081) typegest = 2 (jour) : fp(h) = 1 si 10 < hleg < 17, sinon 0 ;  ; 
- (1814, p. 1081) enclenchement : Vp(h) > 0 ou θb(zreg)(h-1) < θc - Δθ ou (θc - Δθ ≤ θb(zreg)(h-1) < θc et θb(zreg)(h-2) < θb(zreg)(h-1)) ; si fp(h) = 0 : Qreq_sto = 0 ; Δθ = 2 K par défaut ; base solaire : toujours enclenchée ; 
- (1815, p. 1082) base seule : condition supplémentaire θb(zreg_base)(h-1) < θc_base + Φpertes,zreg_base(h-1) / (ρw·cw·V(zreg_base)) ;  ; Typeprod_stockage = 0
- (1816, p. 1082) si iactive : Qreq_sto_base(h) = max[ρw·cw·Σ_{z=zbase}^{Nzone} Vz × (θc_base - Σ_{z=zbase}^{Nzone} Vz·θbz(i-1) / Σ Vz) + Σ_{z=zbase}^{Nzone} Φpertes,z ; 0] ; θbz(i-1) : dernière itération de puisage ; pour l'appoint remplacer zbase par zap, θc_ap ; 
- (1817, p. 1083) régulation optimisée : fp_ap(h) = 1 si hleg > 23 ou < 5, sinon 0 ;  ; CET titre V (certifié NF EN 16147, Vtot < 400 L)
- (1818, 1819, p. 1083) fp_base(h) = 1 (permanent) ou 1 la nuit seulement ;  ; régulation optimisée
- (1820, p. 1083) si hleg = 0 : Iactive,base = 1, Iactive,ap = 0 ;  ; régulation optimisée
- (1821, p. 1084) Qrequis(h) = ρw·cw·Σ_{z=1}^{4} Vz·(θc - θz(h-1)) ;  ; 
- (1822, p. 1084) PPAC(h) = ρw·cw·Σ_z Vz·(θz(h-1) - θz(h-2)) / 1 h ;  ; 
- (1823, p. 1084) Nhrestant(h) = 5 - hleg si hleg < 5, sinon 0 ;  ; 
- (1824, p. 1084) Qdisponible(h) = Nhrestant(h) × PPAC(h) ;  ; 
- (1825, p. 1084) si Vp(h) > 0 : Iactive,ap = 1 ; si Qrequis = 0 : Icons_atteinte = 1 ; si Icons_atteinte = 0 : Iactive,ap = 1 si (Qdisponible < Qrequis ou Iactive,ap(h-1) = 1 ou (hleg = 4 et Qrequis > 0)) sinon 0 ; sinon 0 ; remise à 0 des booléens à hleg = 6 ; le texte dit aussi que l'appoint est désactivé l'heure suivant son activation pour remesurer PPAC ; 
- (1826, p. 1088) NUT(h) = 3600·UAech / (ρe·ce·min(qv_aval ; qv_prim)) ; ρe = 998 kg/m3, débits m3/h ; échangeur externe
- (1827, p. 1089) Rd(h) = min(qv_aval ; qv_prim) / max(qv_aval ; qv_prim) ;  ; 
- (1828, p. 1089) εeff = NUT / (NUT + 1) ;  ; Rd = 1
- (1829, p. 1089) εeff = (1 - e^{-NUT(1-Rd)}) / (1 - Rd·e^{-NUT(1-Rd)}) ;  ; Rd ≠ 1
- (1830, p. 1089) θentree_ech(i) = θretour,aval(h) + qv_aval / (εeff·min(qv_aval ; qv_prim)) × (θdepart,aval(h) - θentrant(h)) ;  ; 
- (1831, p. 1089) θsortie,ballon(i) = θb[zp](i-1) ;  ; 
- (1832, p. 1089) θsortie_ech(i) = θentree_ech + Qw_sto_unit(i) / (qv_prim·ρw·cw) (signe à vérifier : physiquement θsortie_ech < θentree_ech) ;  ; θsortie,ballon ≥ θentree_ech
- (1833, p. 1089) θretour,ballon(i) = θsortie_ech(i) ;  ; 
- (1834, p. 1089) Vpuisage(i) = qv_prim × (θentree_ech - θsortie_ech) / (θsortie,ballon - θsortie_ech) ;  ; 
- (1835, p. 1089) Vp(i) = min(Vpuisage(i) ; Vzmin) ;  ; 
- (1836, p. 1089) Qrest(i) = Qreq(i) - Vp(i)·ρw·cw·(θsortie,ballon - θsortie_ech) ;  ; 
- (1837, p. 1089) Wcirc,prim(h) = Pw_circ_prim × th ;  ; puisage assuré
- (1838 à 1843, p. 1090) sinon : θsortie_ech = θamb (1838) ; Vpuisage = 0 (1839) ; Vp = 0 (1840) ; Qrest = Qreq(h) (1841) ; ArretPuisage = vrai (1842) ; Wcirc,prim = 0 (1843) ;  ; θsortie,ballon < θentree_ech
- (1844 à 1851, p. 1090, 1091) appoint séparé instantané, préchauffage si θentree_ech > θsortie,ballon > θretour,aval : θentree_ech = θsortie,ballon (1844) ; θsortie_ech = θentree_ech - εeff·min(qv_aval ; qv_prim)/qv_prim × (θentree_ech - θentrant) (1845) ; θretour,ballon = θsortie_ech (1846) ; Vpuisage = qv_prim (1847) ; Vp = min(Vpuisage ; Vzmin) (1848) ; report = Qw_sto_unit - Vp·ρw·cw·(θsortie,ballon - θsortie_ech) (1849) ; ArretPuisage (1850) ; Wcirc = Pw·th (1851) ;  ; Typeprod_stockage = 3, échangeur externe
- (1852, p. 1092, 1093) UAech[z] = UAech / (h_haut - h_bas) × min(V[z]/Vtot ; hzsup - h_bas ; h_haut - hzinf) pour les zones traversées (hzinf = cumul des V/Vtot) ; z_bas,ech et z_haut,ech par encadrement ; h_bas = 25 % par défaut, h_haut = 100 % ; échangeur interne 9.11
- (1853, p. 1093) NUTech[z](h) = UAech[z] / (qv_aval·ρw·cw) ;  ; 
- (1854, p. 1093) Qiter = Vtot·ρw·cw·2 °C ;  ; 
- (1855, p. 1093) Qw(i) = min(Qw_sto_unit(i) ; Qiter) ;  ; 
- (1856, p. 1093) Qmax[1](i) = V[1]·ρw·cw·max(0 ; θb[1](i-1) - θentrant) ;  ; 
- (1857, p. 1093) Δθdeb[1](i) = max(0 ; (θb[1](i-1) - θentrant) / (1/NUTech[1] + 0,5)) ;  ; 
- (1858, p. 1093) Qmax[z](i) = V[z]·ρw·cw·max(0 ; θb[z](i-1) - θentrant) ;  ; z > 1
- (1859, p. 1094) Δθdeb[z](i) = max(0 ; (θb[z](i-1) - θentrant - Σ_{k<z} Δθdeb[k]) / (1/NUTech[z] + 0,5)) ;  ; z > 1
- (1860, p. 1094) θsortie,ballon(i) = θentrant + Σ_z Δθdeb[z](i) ;  ; 
- (1861, p. 1094) si θsortie,ballon ≥ θdepart,aval : Qprelevee[z](i) = min(Qmax[z] ; Δθdeb[z] / (θsortie,ballon - θentrant) × Qw(i)) ;  ; 
- (1862, p. 1094) sinon Qprelevee[z](i) = 0 ;  ; 
- (1863, p. 1094) Qw_sto_unit_report(i+1) = Qw_sto_unit(i) - Σ_z Qprelevee[z](i) ;  ; 
- (1864 à 1866, p. 1094) appoint instantané, échangeur interne : si θentrant < θsortie,ballon < θdepart,aval : Qprelevee[z] = min(Qmax[z] ; Δθdeb[z]/(θdepart,aval - θentrant) × Qw(i)) (1864) ; si θsortie,ballon ≤ θentrant : 0 (1865) ; report(i+1) = Qw(i) - Σ Qprelevee (1866) ;  ; Typeprod_stockage = 3
- (1867, p. 1101) Rtemp(h) = (40 - θef(h)) / (θdepart,aval - θef(h)) ;  ; 9.12, Type_accumulateur_ECS ≠ 0
- (1868, p. 1101) Veq-un-puisage(h) = 8 × 6 × Rtemp(h) (L) ;  ; 
- (1869, p. 1101) Npuisage(h) = max(1 ; ENTIER(Vef,ecs(h) / Veq-un-puisage(h))) (le texte dit « entier directement supérieur ») ; Vef en L ici ; 
- (1870, p. 1101) N = 1 : qvef,ecs(h) = 0,06 × N × 6 × Rtemp (m3/h) ;  ; 
- (1871, p. 1101) N > 1 : qvef,ecs(h) = 0,06 × N × 6 × Rtemp × Y(h) ;  ; 
- (1872, p. 1102) Y(h) = 0,8 / √(Npuisage - 1) ;  ; N > 1
- (1873, p. 1102) N = 1 : t_puis(h) = 2 × 0,13 h ;  ; 
- (1874, p. 1102) N > 1 : t_puis(h) = min(1 ; N × Y × 0,13) ;  ; 
- (1875, 1876, p. 1103) Nzone = 4 ; Vzone = V/4 ;  ; eau technique, échangeur externe
- (1877, p. 1105) qv,ECS,nom = 1000·PechECS / (ρe·ce·(θcons - 5 - 15)) ; PechECS en kW ; 
- (1878, p. 1105) εeff,nom = (θcons - 20) / (θcons - 15) × min(qv,ECS,nom ; qv_prim_nom) / qv,ECS,nom ;  ; 
- (1879, p. 1105) Rd,nom = min(qv,ECS,nom ; qv_prim_nom) / max(...) ;  ; 
- (1880, p. 1105) UAech(0) = 50 × PechECS ; W/K ; initialisation Brent
- (1881 à 1883, p. 1105) NUT(i) = 3600·UAech(i)/(ρe·ce·min(qv,ECS,nom ; qv_prim_nom)) ; εeff(i) = (1 - e^{-NUT(1-Rd,nom)})/(1 - Rd,nom·e^{-NUT(1-Rd,nom)}) ; Δε(i) = εeff,nom - εeff(i), arrêt si |Δε| < 0,01 ;  ; résolution de Brent sur UAech ; cas Rd,nom = 1 non écrit, prendre 1891
- (1884, p. 1106) Qw_sto_unit(i=1) = Qw_sto_unit(h) - Qw_rechauboucle(h) ;  ; réseau bouclé seulement
- (1885, 1886, p. 1106) qv_aval(h) = qvef,ecs(h) ; θretour,aval(h) = θef(h) ;  ; 
- (1887, p. 1106) qv_prim(h) = qv_prim_nom ;  ; Type_Circulateur_Prep_ECS = 0
- (1888, p. 1106) qv_prim(h) = max(qv_aval/qv,ECS,nom ; Modmin) × qv_prim_nom ;  ; Type_Circulateur_Prep_ECS = 1
- (1889 à 1892, p. 1106, 1107) NUT(h), Rd(h), εeff(h) : mêmes formes que 1826 à 1829 avec qv_prim(h) ;  ; 
- (1893, p. 1107) θentree_ech(h) = θretour,aval + qv_aval/(εeff·min(qv_aval ; qv_prim)) × (θdepart,aval - θretour,aval) ;  ; 
- (1894, p. 1107) θsortie,ballon(i) = θb[zp](i-1) ;  ; 
- (1895, p. 1107) vitesse constante : θsortie_ech(i) = θsortie,ballon(i) - εeff·min(qv_aval ; qv_prim)/qv_aval × (θentree_ech - θretour,aval) ;  ; θsortie,ballon ≥ θentree_ech
- (1896, p. 1107) vitesse variable : θsortie_ech(i) = θsortie,ballon(i) - εeff·min(qv_aval ; qv_prim)/qv_aval × (θsortie,ballon - θretour,aval) ;  ; 
- (1897, p. 1107) θretour,ballon(i) = θsortie_ech(i) ;  ; 
- (1898, p. 1108) Vpuisage(i) = Qw_sto_unit(i) / (ρe·ce·(θsortie,ballon(i) - θsortie_ech(i))) ;  ; 
- (1899, p. 1108) Vp(i) = min(Vpuisage(i) ; Vzmin) ;  ; 
- (1900, p. 1108) report(i) = Qw_sto_unit(i) - Vp(i)·ρw·cw·(θsortie,ballon - θsortie_ech) ;  ; 
- (1901 à 1905, p. 1108) sinon θsortie_ech = θamb ; Vpuisage = 0 ; Vp = 0 ; report(i) = Qreq(h) ; ArretPuisage = vrai ;  ; θsortie,ballon < θentree_ech
- (1906, p. 1108) fin de boucle si ArretPuisage ou report(i) = 0 ou Vp(i) = 0 ;  ; 
- (1907, p. 1108) Qw_sto_unit_report(h) = report(i) ;  ; sans bouclage
- (1908, p. 1109) Wcirc,prim,puis(h) = Pw_circ_prim × t_puis(h) ;  ; vitesse constante
- (1909, p. 1109) Wcirc,prim,puis(h) = min[1 ; (qv_prim(h)/qv_prim_nom)^(2/3)] × Pw_circ_prim × t_puis(h) ;  ; vitesse variable
- (1910, p. 1110) réchauffage de boucle : θsortie,ballon(i) = θb[zp](i-1) ;  ; qv_boucle,ecs > 0, dernière itération, retour en zone 1 ou 3
- (1911, p. 1110) Vpuisage(i) = Qw_rechauboucle(h) / (ρe·ce·(θsortie,ballon(i) - θsortie_ech(h))) ;  ; pas de prélèvement si énergie insuffisante
- (1912, p. 1110) Qw_sto_unit_report(h) = report(i_RB) + report(i-1) ;  ; 
- (1913, p. 1110) Wcirc,prim,RB(h) = Pw_circ_prim_RB × (1 - t_puis(h)) ;  ; 
- (1914, p. 1110) Wcirc,prim(h) = Wcirc,prim,puis + Wcirc,prim,RB ;  ; 
- (1915 à 1921, p. 1112) appoint instantané, échangeur externe eau technique : mêmes formes que 1844 à 1850 ;  ; Type_Assemblage = 3 ; alerte 12 h non applicable
- (1922, 1923, p. 1113) Nzone = 4 ; Vzone = V/4 ;  ; eau technique, échangeur interne
- (1924, p. 1114) qv,ECS,nom = 1000·PechECS / (ρe·ce·(θcons - 20)) ;  ; 
- (1925, p. 1114) εeff,nom = (50 - 15) / (θcons - 15) (le texte écrit 50 °C, cohérent avec θcons - 5 seulement pour θcons = 55) ;  ; 
- (1926, p. 1114) NUTnom = -ln(1 - εeff,nom) ;  ; 
- (1927, p. 1114) UAech = ρe·ce·qv,ECS,nom·NUTnom ;  ; 
- (1928, p. 1114) UAech[z] = Vzone/V × UAech ; h_bas = 0 %, h_haut = 100 % ; 
- (1929 à 1941, p. 1114 à 1116) identiques à 1853 à 1863 avec θretour,aval = θef (1930), NUTech (1931), Qiter (1932), Qw(i) (1933), Qmax (1934, 1936), Δθdeb (1935, 1937), θsortie,ballon (1938), Qprelevee (1939, 1940), report(i) (1941) ;  ; eau technique, échangeur interne
- (1942 à 1945, p. 1116, 1117) appoint instantané : Qprelevee[z] = min(Qmax[z] ; Δθdeb[z]/(θdepart,aval - θretour,aval) × Qw(i)) (1942) ; Qnon-assurée(i) = Qnon-assurée(i-1) + Qw(i) - Σ Qprelevee (1943) ; report(i) = Qw_sto_unit(i) - Qw(i) (1944) ; Qw_sto_unit_report(h) = report(i) + Qnon-assurée(i) (1945) ;  ; 
- (1946, p. 1120) Qreq_sto = Qreq_sto_base (base) ou Qreq_sto_ap (appoint) ; l'échangeur du générateur relève θaval sans changer Qreq ; UAhx du générateur ; 
- (1947, p. 1122) Qfou_sto = Qfou_sto_base ou Qfou_sto_ap ; {Qcef} de l'assemblage = {Qcef} du générateur ; pertes de l'échangeur vers le volume chauffé nulles ;  ; 
- (1948, p. 1127) zbase = 1 ;  ; 
- (1949, p. 1127) θc_base = θc_ap = 55 °C ;  ; Id_Fou_Sto = 3 ; sinon θc_base ≥ θc_ap ≥ max(55 ; θmax,ECS^gen)
- (1950, p. 1127) Vz,min = min(Vz,min^principal ; Vz,min^secondaire) ;  ; Typeprod_stockage = 2
- (1951, p. 1128) Nbiter_vp = 4 (types 0 et 3, valeur en image) ; arrondi inférieur de 2/min(faux ; 1 - faux) (type 1) ; arrondi inférieur de (Vtot_princ + Vtot_sec)/Vz,min (type 2) ;  ; 
- (1952, p. 1129) θentrant,ECS(h) = (Vsoutire,ECS·θcw + qv_boucle,ECS·θretour,aval,ECS) / (Vsoutire,ECS + qv_boucle,ECS) ; Vsoutire en m3, qv_boucle en m3/h sur 1 h ; réseau bouclé ; sinon θentrant,ECS = θcw
- (1953, p. 1129) Qw_sto_unit(h) = Qreq,ECS(h) / nb_assembl ;  ; 
- (1954, p. 1129) Qrest,ECS(h) = Qw_sto_unit_report(i-1) (dernière itération) ;  ; 
- (1955, p. 1129) Qfou,ECS(h) = Qreq,ECS(h) - Qrest,ECS(h) ;  ; 
- (1956 à 1959, p. 1130) chauffage : θentrant,CH = θretour,aval,CH ; Qw_sto_unit = Qreq,CH/nb_assembl ; Qrest,CH ; Qfou,CH ;  ; Id_Fou_Sto = 1 ou 4, hors champ
- (1960, p. 1132) nbh_temp_sto_insuff(h) = nbh(h-1) + 1 si θb4(h) < θc (base seule : θc_base ; sinon θc_ap), sinon 0 ; erreur si > 168 ; condition en image, reconstituée ; sauf Typeprod_stockage = 3
- (1961, p. 1133) {Qcef^assemblage(po ; énergie)}(h) = nb_assembl × [Qcons_gnr_base × (Qreq_ch·E(1;én) + Qreq_ecs·E(3;én))/(Qreq_ecs + Qreq_ch) + Qcons_gnr_ap × (idem) + (Waux_pro_base + Waux_pro_ap) × (Qreq_ch·E(1;50) + Qreq_ecs·E(3;50))/(Qreq_ecs + Qreq_ch)] ; si les deux Qreq sont nuls, tout sur le chauffage si Id_Fou_Sto = 1, sur l'ECS si 3 ; E(po;én) matrice unitaire, énergie 50 = électricité des auxiliaires ; 
- (1962, p. 1133) Φvc_sto(h) = nb_assembl × Idpos_gen × (Φpertes^principal(h) + Φpertes^secondaire(h)) ;  ; 
- (1963, p. 1133) Φvc_gnr(h) = nb_assembl × Φvc_gnr_base + nb_assembl × Φvc_gnr_ap ;  ; 
- (47 (fiche 4.1), p. fiche scénarios conventionnels) iecs(j) = 0 si ienseignement = 1 et ivac = 0, sinon 1 ;  ; 
- (1008 (fiche 8.17), p. fiche 8.17) idencl^gen(j) = max_{dp-e → gen, idfonction = 3} idencl^dp-e(j) ;  ; interface vers la génération

## Algorithme

```
Organisation proposée : nouveau module openbce/ecs_distribution.py (9.5, 9.7, 9.8), openbce/ballon.py (9.9, 9.10, 9.11), openbce/ballon_eau_technique.py (9.12), openbce/production_ecs.py (9.13, 9.14, couture vers les générateurs), banc/ecs_cef.py. Toutes les grandeurs horaires en Wh, volumes en L sauf 9.11/9.12 (m3 dans le texte ; convertir en entrée et garder ρ·c = 1,163 Wh/(L.K)).

PRÉPROCESSEUR (une fois par projet)
  pour chaque Groupe gr, chaque Emetteur_ECS em :
      A_em = Rat_em_e × A_gr                                  # (1675) ; vérifier Σ Rat_em_e = 1 (1674)
      Qw_em[h] = ecs.besoins(...) par émetteur (1694 avec corr 1679)   # existant ; le découper par émetteur
      ds = em.un("Distribution_Groupe_ECS")
      L_vc = l_vc_2nd_e si delta_lvc = saisie sinon (6·A_em/80 si usage in (1,2) sinon 0,05·A_em)   # (1730)
      L_hvc = l_hvc_2nd_e
      D = d_int_2nd_e / 1000
      V_vc, V_hvc = L·π·D²/4·1000                              # (1731)
      nb_bouchons = {1:3, 2:3, 3:2, 4:2, 5:3}[usage]           # tableau 280 ; autres usages : point ouvert
      θ2nd = 53 (ou 48 ; point ouvert) ; erreur si θ2nd < 40    # (1680)
      rattacher ds à dp = Distribution_Intergroupe_ECS[Index == Id_Dist_Primaire], et dp à gen = Generation[Index == Id_Gen]
  pour chaque dp : Adess = Σ A_em (1739) ; Ratsurf[gr] = Σ_{em ∈ gr} A_em / Adess (1738) ; θdep = max θ2nd (1741/1754/1763)
  pour chaque Production_Stockage ps de la génération :
      Vtot ; faux = f_aux si Statut_faux = saisie sinon 0,5
      si Type_prod_stockage in (1, 2) et Type_accumulateur_ECS = 0 : V = [(1-faux)Vtot/2]*2 + [faux·Vtot/2]*2  sinon V = [Vtot/4]*4
      UAS_util selon Valeur_Certifiee_Justifiee_Defaut : UA_S (1767) | 1,1·UA_S (1768) | tableau 283/284 via Nature_Ballon puis (1769)
      Uz = UAS_util·Vz/Vtot                                     # (1770)
      Vzmin = min(V) ; Nbiter = 4 | floor(2/min(faux,1-faux)) | floor((Vp+Vs)/Vzmin)    # (1951)
      θc = 55 si Id_Fou_Sto = 3 sinon Theta_Cons (1949) ; Δθ_base, Δθ_ap (défaut 2)
      zbase = 1 (1948) ; zap = z_appoint ; zreg_base, zreg_ap ; (zmax_ech, hrelrest) pour base et appoint par (1782, 1783)
      si Type_accumulateur_ECS = 2 : UAech par Brent (1877 à 1883) ; si = 1 : UAech par (1924 à 1928)
  état initial : θb = [50]*4 (h-1 et h-2), report = 0, Qw_prev = 0 par émetteur, nbh_report = 0, nbh_insuff = 0, I_ap_prev = 0, I_cons_atteinte = 0

BOUCLE HORAIRE h = 0..8759 (hleg = cal.case[h] - 1 ; jour j)
  1. Émission + distribution du groupe, pour chaque émetteur em :
       Qw = Qw_em[h]
       Is = 1 si Qw_prev = 0 and Qw ≠ 0 ; (nb-1)/nb si Qw_prev ≠ 0 and Qw ≠ 0 ; 0 sinon          # (1732)
       Φvc_2nd = ρc·V_vc·(θ2nd - θi[h])·nb·Is·nb_dist                                               # (1733)
       Φhvc_2nd = ρc·V_hvc·max(0, θ2nd - (b·θext[h] + (1-b)·θi[h]))·nb·Is·nb_dist                  # (1734)
       Qw_2nd[em] = Qw + Φvc_2nd + Φhvc_2nd                                                        # (1735)
       Qw_prev = Qw
  2. Distribution intergroupe, pour chaque dp :
       idencl = max(iecs[j] des ds-e reliés)                                                       # (1737), iecs par (47)
       S = Σ Qw_2nd ; Ratbes[gr] = Σ_{gr} Qw_2nd / S si S > 0 sinon Ratsurf[gr]                    # (1740)
       si type = 0 : φvc = φhvc = 0 ; Qw_prim = S ; Waux = 0 ; θret = θcw[h] ; θmoy = θdep        # (1763 à 1766)
       si type = 1 : θret = θdep - 5 ; θmoy = (θdep+θret)/2                                       # (1743, 1744)
                     φvc = U·Lvc_bcl·(θmoy - 20)·idencl ; φhvc = U·Lhvc_bcl·idencl·(θmoy - (20 + b·(θext-20)))   # (1745, 1746)
                     Wrech = (φvc+φhvc) si Is_Rechauf else 0                                        # (1747)
                     Wcirc = Pcirc·(idencl si type_gest_circ = 1 else 1)                            # (1748, 1749)
                     Waux = Wcirc ; Qw_prim = S + (0 si Is_Rechauf else φvc+φhvc)                   # (1750, 1753)
       si type = 2 : θret = θcw[h] ; θmoy = θdep ; φ par (1757, 1758) ; Waux = φvc+φhvc (traceur) ; Qw_prim = S   # (1759, 1762)
       Waux_gr[gr] = Waux·Ratsurf[gr] (1751, 1760) ; Φaux_vc = 0 (1752, 1761)
       qv_boucle = débit du bouclage (point ouvert, voir ci-dessous) ; Qw_rechauboucle = φvc + φhvc (déduction)
  3. Vers la génération (interface 8.17, hors champ) : Qreq_ecs^gen = Σ_{dp} Qw_prim + report génération ; θdepart,aval,ECS = θdep (ou Theta_Wm_Ecs : point ouvert) ; Vef_ECS = Qreq_ecs / (ρc·(θdepart,aval - θcw)) (déduction) ; idencl_gen (1008). Si idencl_gen = 0 : rien n'est fourni.
  4. Assemblage ballon (9.14, par Production_Stockage), ordre impératif :
       θentrant = θcw[h] si qv_boucle = 0 sinon (1952)
       Qw_sto_unit = Qreq_ecs/nb_assembl (1953) ; (le report du pas précédent est déjà dans Qreq via la génération ; sinon l'ajouter ici)
       Φpertes_z = Uz·(θb[z](h-1) - θamb) pour z = 1..4 (1771) ; θamb = 20/23/26 si Pos_Gen = 1 (8.17), sinon θext (déduction)
       # 4a boucle itérative de puisage (9.10) : θ_i = copie de θb(h-1) ; Vp_tot = 0 ; i = 1
       tant que i ≤ Nbiter et (i == 1 ou report ≠ 0) :
           θ_zp = θ_i[3]
           si Type_accumulateur_ECS = 0 :
               si Type_prod_stockage ≠ 3 :
                   si θ_zp > θdepart,aval : Vp = min(Qw_sto_unit/(ρc·(θ_zp - θentrant)), Vzmin) ; report = Qw_sto_unit - ρc·Vp·(θ_zp - θentrant)   # (1795, 1798)
                   sinon Vp = 0 ; report = Qw_sto_unit                                                                                   # (1796, 1799)
               sinon (appoint instantané) : (1802 à 1808), avec arrêt de boucle après le cas « préchauffage »
           si Type_accumulateur_ECS = 2 : (1885 à 1906) ; si = 1 : (1929 à 1941) ; appoint instantané : (1915 à 1921) ou (1942 à 1945)
           # mise à jour des températures après puisage (9.9), sans pertes ni apports
           si Vp > 0 : θ_i[0] = (θ_i[0]·(V1 - Vp) + θentrant·Vp)/V1 (1774) ; pour z = 2..4 : θ_i[z] = (θ_i[z]·(Vz - Vp) + θ_i[z-1]_avant·Vp)/Vz (1777) [utiliser les valeurs de l'itération précédente à droite]
           si échangeur interne : θ_i[z] -= Qprel[z]/(ρc·Vz) (1778)
           melanger(θ_i, V) (1779) ; θ_i = min(θ_i, θmax) (1780)
           Vp_tot += Vp ; Qw_sto_unit = report ; i += 1
       Vp_h = Vp_tot (1800) ; Qrest = report (1954) ; Qfou_ECS = Qreq_ecs - Qrest (1955) ; report au pas suivant (à renvoyer à la génération) ; nbh_report (1781) ; Qw_rechauboucle : itération finale (1910 à 1912) si bouclage
       θ_apres_puisage = θ_i ; θ̄ = (θb(h-1) + θ_apres_puisage)/2 (1786)
       # 4b générateur de base (9.10 + 9.13)
       fp_base = (1811..1813)[type_gest_th_base](hleg) ; (régulation optimisée : 1818 à 1820)
       actif_base = fp_base and ((Vp_h > 0) or θb[zreg_b](h-1) < θc - Δθb or (θc - Δθb ≤ θb[zreg_b](h-1) < θc and θb[zreg_b](h-2) < θb[zreg_b](h-1)))   # (1814)
       si Type_prod_stockage = 0 : actif_base = actif_base and θb[zreg_b](h-1) < θc + Φpertes_zreg/(ρc·V[zreg_b])   # (1815)
       Qreq_base = max(ρc·ΣV[zbase:]·(θc - ΣVθ_i[zbase:]/ΣV[zbase:]) + ΣΦpertes[zbase:], 0) si actif_base sinon 0   # (1816)
       θb_moy_ech_base = (1784) ou (1785) sur θ̄
       Qfou_base, Qcef_base, Φvc_gnr_base = generateur_base(Qreq_base, θb_moy_ech_base, ...)      # hors champ (9.13 : 1946, 1947)
       si raccordement par échangeur : θ_i[z] += (Qinj_z - Φpertes_z)/(ρc·Vz) avec Qinj = Qfou_base en zone zbase, Φpertes appliquées une seule fois (1787)
       si piquages haut et bas (Type_prod_stockage ≠ 2) : (1787 sans Qinj) puis (1788 à 1790)
       melanger ; min(θmax)
       # 4c générateur d'appoint (Type_prod_stockage in (1, 2))
       fp_ap = (1811..1813)[type_gest_th_appoint](hleg) ; régulation optimisée : (1817), (1821 à 1825) avec PPAC sur θb(h-1), θb(h-2)
       actif_ap par (1814) avec zreg_ap, Δθ_ap, θc_ap (pas de condition 1815)
       Qreq_ap = (1816) avec zap ; θb_moy_ech_ap = (1784/1785) avec zap, hech_appoint
       Qfou_ap, Qcef_ap, Φvc_gnr_ap = generateur_appoint(Qreq_ap, θb_moy_ech_ap)        # effet Joule : Qfou = min(Qreq, Pmax·1000), Qcef = Qfou
       θ_i[z] += Qinj_z/(ρc·Vz) en zone zap (1787, pertes déjà comptées) ; melanger ; min(θmax)
       θb(h-2) = θb(h-1) ; θb(h-1) = θ_i (1791)
       nbh_insuff (1960) ; Φvc_sto = nb_assembl·Pos_Gen·ΣΦpertes (1962) ; Φvc_gnr (1963)
       Qcef_assemblage = nb_assembl × (Qcef_base + Qcef_ap + Waux_pro) réparti sur ECS puisque Qreq_ch = 0 (1961)
  5. Consommations ECS du pas : Cef_ecs_gen = Σ générateurs ECS (Qcef) + Wrech (8.17 ligne 5028 : le réchauffeur est ajouté dans la matrice génération) ; auxiliaires de distribution : Waux_gr (circulateurs, traceurs) et Wcirc_prim (9.12) vers le poste auxiliaires de distribution
  6. Répartition par groupe (8.29, interface) : Cef_ecs_gen,gr = Cef_ecs_gen × Ratbes_ecs_gen,gr, Ratbes = Qw_prim du groupe / Σ (par analogie avec 1740) ; cumul annuel / 1000 / surface -> O_Cef_ecs_annuel

ÉTATS CONSERVÉS D'UNE HEURE À L'AUTRE : Qw_prev par émetteur (1732) ; θb(h-1) et θb(h-2) par ballon (1814, 1822) ; report Qw_sto_unit_report (1797, 1912) ; nbh_report ; nbh_temp_sto_insuff ; Iactive,ap(h-1), Icons_atteinte (remis à 0 à hleg = 6) ; dernières valeurs non nulles de qv_boucle, Vef, θentrant, θdepart,aval (9.10 p. 1080) ; côté génération, Qrep_tot_ar_ecs (report de la demande non assurée, 8.17).

FONCTION melanger(θ, V) : implémenter (1779) littéralement : a = 0 ; tant que θ n'est pas croissante : si θ[a] > θ[a+1] : chercher le plus grand k ∈ {1,2,3} (borné par 4) tel que la moyenne volumique de a..a+k-1 dépasse θ[a+k] ; égaliser a..a+k à la moyenne volumique ; a = 0 ; sinon a += 1.
```

## Sorties RSEE pour le banc

- `O_Cef_ecs_annuel` (Sortie_Batiment_C/Sortie_Zone_C/Sortie_Groupe_C, kWh ef/m² (SHAB ou SU) ; cible principale du banc ; 7,9 (CET collectif, besoins 17,4) et 4,3 (effet Joule bureaux, besoins 1,6) dans les deux RSEE lus)
- `O_Cef_ecs_mois` (Sortie_Groupe_C (Sortie_Mensuelle), kWh ef/m² par mois ; permet de tester la dynamique du ballon et les pertes (hiver vs été))
- `O_Cef_ecs_elec_annuel, O_Cef_ecs_gaz_annuel, O_Cef_ecs_fioul_annuel, O_Cef_ecs_bois_annuel, O_Cef_ecs_reseau_annuel` (Sortie_Groupe_C, kWh ef/m² par vecteur ; vérifie la ventilation de (1961) par énergie)
- `O_B_Ecs_annuel, O_B_Ecs_mois` (Sortie_Groupe_C, Sortie_Zone_C, Sortie_Batiment_C, kWh/m² ; déjà validé (+0,35 %) ; sert de dénominateur pour isoler pertes + rendement)
- `O_Cef_aux_distribution_annuel, O_Cef_auxs_elec_annuel` (Sortie_Groupe_C, kWh ef/m² ; circulateurs de bouclage (1750), traceurs (1759), circulateur primaire (1914) ; à comparer sur des projets à réseau bouclé)
- `O_Cef_imp_ecs_annuel, O_Cef_elec_imp_ecs_annuel, O_Cef_elec_cons_ecs_annuel` (Sortie_Zone_C, Sortie_Batiment_C, kWh ef/m² ; agrégats ; O_Cef_elec_AC_ecs_annuel (autoconsommation) à écarter)
- `O_Cef_ECS_comb_bat` (Sortie_Batiment_C, kWh ; ECS par combustion, 0 dans les RSEE lus)
- `generateur_principal_ecs, vecteur_energie_principal_ecs` (Sortie_Batiment_C, codes (513 et 1502 ; 11 = électricité) ; contrôle de la correspondance Source_Ballon_Base_* -> type de générateur)
- `NbReports_ECS` (Sortie_Generation/Sortie_Production_Stockage/Sortie_Generateur_Collection/Sortie_Generateur, heures ; nombre d'heures avec Qw_sto_unit_report ≠ 0 (1781) : 6472 pour le CET de nuit, 84 pour l'effet Joule ; test direct de la boucle de puisage et de la programmation fp)
- `Nbhcharge_0_ECS, Nbhcharge_0_10_ECS ... Nbhcharge_90_100_ECS, Nbhcharge_HF_ECS` (Sortie_Generateur, heures par classe de taux de charge en ECS (8.29) ; histogramme de Qfou/Pn du générateur de base ; test de Qreq_sto_base (1816) et de fp (1811 à 1813))
- `Q_fou_3_postes` (Sortie_Generateur, kWh fournis tous postes (3801,2 et 1025,8) ; pour un générateur ECS seul : Σ Qfou_sto = besoins + pertes distribution + pertes ballon : isole UAS_util)
- `IsReliePrechauffageCW` (Sortie_Generateur, booléen ; récupérateur eaux grises, doit rester 0)
- `Reseau_ECS_Cep, ECS_Perte_UAs_Cep` (Sortie_Sensibilite_Batiment, kWh ep/m² ; NaN dans les RSEE lus ; s'ils sont renseignés ailleurs, ils donnent directement l'effet des pertes de réseau et du UA_S)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch` (Sortie_Generation, booléens de sous-dimensionnement (chauffage seulement ; pas d'équivalent ECS exposé))

## Points ouverts (à trancher au codage)

- θ2nd-e : 48 °C (tableau 272, p. 1019) contre 53 °C (tableau 279, p. 1043) ; aucun champ XML ne la porte (Distribution_Groupe_ECS n'a que des longueurs et un diamètre) ; Generation.Theta_Wm_Ecs vaut 50 ou 54 selon la génération. Banc : sur des groupes à l_vc_2nd_e = l_hvc_2nd_e = 0 et réseau intergroupe de type 0, O_Cef_ecs_annuel ne dépend de θ2nd que par θdepart,aval du ballon (Vp via 1795) ; comparer les trois hypothèses (48, 53, Theta_Wm_Ecs) sur O_Cef_ecs_mois et NbReports_ECS.
- Sens du code delta_lvc : le texte dit δlvc = 0 valeur par défaut, 1 valeur saisie ; les deux RSEE ont delta_lvc = 1 avec l_vc_2nd_e = 0 (distribution sans pertes) et non la valeur par défaut 6·A/80. Banc : si delta_lvc = 1 signifie « défaut », les pertes 1733 sur 80 m² et 12 mm donnent environ 0,7 L × 1,163 × 30 K × 3 bouchons par heure de puisage ; l'écart sur O_Cef_ecs_annuel (effet Joule, rendement 1) tranche.
- Unité de d_int_2nd_e : 12 dans le RSEE, m dans le texte ; lire en mm (12 mm est un diamètre intérieur plausible).
- nb_bouchons des usages absents du tableau 280 (p. 1046 : seuls les codes 1, 2, 4, 5 et 16 sont donnés, et le code bureaux y est 16 alors que l'usage RSEE bureaux est 3) : proposer 2 pour les usages tertiaires, 3 pour l'hébergement ; banc sur O_Cef_ecs_mois de projets tertiaires à distribution non nulle.
- Codes RSEE de Valeur_Certifiee_Justifiee_Defaut : le texte (p. 1060) donne 0 certifié, 1 justifié, 2 défaut ; le CET T.ONE porte 2 avec UA_S = 2,94 W/K (valeur plausible certifiée pour 175 L), le ballon effet Joule porte 0 avec UA_S = 0 (impossible en certifié). Hypothèse : correspondance inversée dans le RSEE (0 = défaut, 2 = certifié). Banc : Q_fou_3_postes du générateur de base moins besoins moins pertes de distribution = pertes de ballon annuelles ; pour 1025,8 kWh fournis et 1,6 kWh/m² de besoins on peut remonter à UAS_util et le comparer à 2,94, à 0,189·V^0,55 ou aux formules effet Joule du tableau 283.
- Correspondance des codes Nature_Ballon (1 pour le CET, 2 pour l'effet Joule bureaux) avec les lignes des tableaux 283 et 284 (effet Joule horizontal, vertical ≥ 75 L, vertical < 75 L, autres ballons, ballon solaire) : à déduire du même banc sur Q_fou_3_postes.
- Statut_faux : texte 1 saisie, 2 défaut ; RSEE 0 avec f_aux = 0,5 et 0 avec f_aux = 0 (base seule). Lire f_aux tel quel quand Type_prod_stockage = 1 ; banc sur NbReports_ECS (le nombre d'itérations et la taille de la zone 4 pilotent les reports).
- type_gest_th_base = 2 pour le CET T.ONE : selon le texte 2 = « de jour seulement » (10 h à 17 h), ce qui est surprenant pour un chauffe-eau thermodynamique ; NbReports_ECS = 6472 h (74 % de l'année) est cohérent avec une plage de fonctionnement très réduite. Banc : simuler 0, 1 et 2 et comparer NbReports_ECS et l'histogramme Nbhcharge_*_ECS.
- Programmation fp et heure légale : le texte dit « hleg > 23 h ou hleg < 5 h » (jamais vrai pour > 23 si hleg ∈ 0..23) : lire comme hleg ∈ {0,1,2,3,4} ; vérifier avec openBCE cal.case (case 10 = 9 h).
- θamb du ballon hors volume chauffé (Pos_Gen = 0 dans les deux RSEE) : la fiche 8.17 (eq. 1009) ne donne que le cas en volume chauffé (20/23/26 °C) ; hypothèse θamb = θext(h) ou température conventionnelle d'un local non chauffé. Banc : O_Cef_ecs_mois d'un effet Joule hors volume chauffé est sensible à θamb hiver/été ; comparer θext et 20 °C constant.
- Grandeurs d'interface non définies dans les fiches lues ni dans 8.17 (grep négatif) : qv_boucle,ECS(h), Vef_ECS(h) = V_soutire,ECS(h), θretour,aval,ECS(h), Qw_rechauboucle(h), θdepart,aval,ECS(h). Déductions proposées : Vef = Qw_prim/(ρc·(θdepart,aval - θcw)) ; θretour,aval = θdépart - 5 (1743) ; Qw_rechauboucle = φpertes_vc_prim + φpertes_hvc_prim ; qv_boucle = Qw_rechauboucle/(ρc·5 K) ; θdepart,aval = max θ2nd-e (= θmax,ECS^gen de 9.14). Les RSEE lus n'ont pas de bouclage (type 0) : ces déductions ne sont testables que sur un projet à Type_Reseau_Intergroupe_ECS = 1 via O_Cef_aux_distribution_annuel (circulateur Pcirc) et O_Cef_ecs_annuel.
- Nbiter_vp pour Type_prod_stockage 0 et 3 : la valeur est une image (p. 1128), seul un « 4 » est lisible ; retenir 4 (= Vtot/Vzmin pour quatre zones égales).
- Équation (1779) mélange et (1960) : partiellement en image (p. 1066, 1067, 1132) ; la reconstitution est donnée dans l'algorithme ; (1737) idem (p. 1051).
- Équation (1832) : θsortie_ech = θentree_ech + Qw/(qv_prim·ρc) donne une sortie plus chaude que l'entrée côté primaire, incohérent avec (1834) ; la fiche 9.12 (1895, 1896) écrit le signe négatif. Appliquer le signe négatif.
- Équation (1925) : εeff,nom = (50 - 15)/(θcons - 15) ; pour θcons = 60 (collectif), le numérateur devrait être θcons - 5 - 15 = 40 par cohérence avec (1878) et (1924) ; retenir (θcons - 20)/(θcons - 15).
- Équation (1869) : le texte dit « entier directement supérieur » mais écrit ENTIER() ; retenir plafond (ceil) avec max 1.
- Facteur 1/3600 dans (1778) et (1788) : il correspond à des volumes en m3 et des énergies en Wh avec ρ en kg/m3 ; en L et Wh il disparaît. Vérifier la cohérence d'unités dans chaque module (9.11 et 9.12 travaillent en m3).
- Pertes du ballon dans (1787) : « dans certains cas les pertes pourront être mises à zéro » ; l'assemblage 9.14 ne le précise pas explicitement pour base + appoint intégré. Hypothèse : pertes appliquées une seule fois lors de l'injection de la base (ou seule injection), pas lors de celle de l'appoint.
- Report Qw_sto_unit_report : porté par le ballon (9.10) ou par la génération (8.17 Qrep_tot_ar_ecs, eq. 1040, 1041) ; les deux mécanismes existent, risque de double comptage. Hypothèse : le ballon renvoie Qrest à la génération, qui le réinjecte dans Qreq du pas suivant. NbReports_ECS tranche le comportement.
- b_sto_e (coefficient d'espace tampon du ballon, figure 198) : aucune équation ne l'utilise dans les fiches lues ; ignoré (0 dans les RSEE).
- Régulation optimisée de l'appoint (1817 à 1825) : le déclencheur n'est pas un champ XML vu ; probablement lié à un titre V porté par Source_Ballon_Base_Thermodynamique_* (Statut_Donnee certifié) ; non activée par défaut ; banc : NbReports_ECS et O_Cef_ecs_elec_annuel du CET.
- Répartition de Cef_ecs par groupe (8.29, Ratbes_ecs_gen,gr) : O_Cef_ecs_annuel du groupe (7,9) égale celui du bâtiment (7,9) alors que O_B_Ecs diffère (17,4 vs 16,1), ce qui suggère une répartition au prorata des besoins (même ratio Cef/B par groupe) ; à confirmer sur un bâtiment à plusieurs groupes de besoins différents.
- Tableaux et figures illisibles en texte : figure 182 (découpage émetteurs, p. 1020), figure 183 (ballon 4 zones, p. 1058), figure 184 (chronologie, p. 1076), figure 185 (appoint séparé, p. 1080), figures 186 à 199 (schémas), figure 191 et 192 (Y et t_puis, p. 1102, redondantes avec 1872 à 1874), figure 194 (p. 1109). Tous les tableaux numérotés (272 à 292) sont lisibles en texte.

## Tableaux en image dans le PDF

- Figure 182 (p. 1020) : exemples de découpage en émetteurs ECS équivalents (schéma, sans valeur)
- Équation (1732) second cas (p. 1046) : condition illisible, reconstituée
- Équation (1737) (p. 1051) : condition d'existence illisible, reconstituée
- Figure 183 (p. 1058) : schéma du ballon à quatre zones
- Équation (1779) (p. 1066, 1067) : algorithme de mélange partiellement en image (branche à trois zones)
- Figure 184 (p. 1076) : chronologie des étapes du ballon
- Figure 185 (p. 1080) : logique de puisage avec appoint séparé
- Figures 186, 187, 188, 189, 193, 195, 196 : schémas d'échangeurs et d'accumulateurs (sans valeur numérique)
- Figures 191 et 192 (p. 1102) : courbes Y(N) et t_puis(N), redondantes avec (1872) à (1874)
- Figure 194 (p. 1109) : rapport de puissance du circulateur à vitesse variable, redondante avec (1909)
- Équation (1951) premier cas (p. 1128) : Nbiter_vp pour types 0 et 3, seul un « 4 » est lisible
- Équation (1960) (p. 1132) : condition θb4(h) < θc illisible, reconstituée
- Figures 197, 198, 199 : schémas d'assemblage (9.13, 9.14)
- Tableaux 272 à 292 : tous lisibles en texte (aucun tableau en image dans la famille)

## Estimation

Lignes de code Python estimées : émission (déjà fait, 0 à 20 lignes pour exposer corr et A_em par émetteur) ; distribution du groupe (1730 à 1735) 60 lignes ; distribution intergroupe (1736 à 1766) 120 lignes ; ballon 9.9 (zones, UAS, pertes, piston, mélange, injection, température vue par l'échangeur) 220 lignes ; gestion-régulation 9.10 (boucle de puisage, fp, enclenchement, Qreq, appoint instantané, régulation optimisée) 180 lignes ; échangeur 9.11 (externe et interne) 160 lignes ; accumulateur eau technique 9.12 (débit conventionnel, Brent, réchauffage de boucle, circulateur) 220 lignes ; assemblage 9.13/9.14 et couture génération (Qw_sto_unit, nb_assembl, matrice 1961, Φvc) 150 lignes ; banc banc/ecs_cef.py (O_Cef_ecs_annuel, O_Cef_ecs_mois, NbReports_ECS, Nbhcharge, Q_fou_3_postes) 100 lignes ; tests unitaires (mélange, piston, enclenchement, cas limites) 150 lignes. Total 1 300 à 1 400 lignes.

Difficulté : élevée. Les fiches 9.5, 9.7 et 9.8 sont simples et sans ambiguïté (hors θ2nd-e et delta_lvc). Le ballon est le cœur du risque : trois boucles imbriquées (itérations de puisage, mélange, injection), deux états mémoire (h-1, h-2), dépendance forte à des codes RSEE dont la correspondance au texte est incertaine (statut UA, Nature_Ballon, type_gest_th, Statut_faux), et quatre équations en image à reconstituer. Le résultat O_Cef_ecs_annuel ne peut être atteint sans le générateur de base (effet Joule trivial, thermodynamique 8.23 non trivial) : prévoir d'abord le banc sur les ballons à effet Joule (Source_Ballon_Base_Effet_Joule, rendement 1), où Cef = besoins + pertes de distribution + pertes de ballon, pour caler UAS_util, θamb et la programmation avant d'attaquer les CET. La fiche 9.12 (eau technique) peut être livrée en second temps : Type_accumulateur_ECS = 0 dans les deux RSEE lus.
