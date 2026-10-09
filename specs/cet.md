# Spécification : Générateurs pour ballon, chauffe-eau thermodynamiques, appoints

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille « générateurs pour ballon, chauffe-eau thermodynamiques, appoints » : tout ce qui, dans une génération Th-C, fournit de l'énergie à un ballon d'ECS (ou mixte) sous le pilotage de la gestion-régulation du ballon.

COUVERT :
1. Fiche 9.13 S1_GEN_générateur_pour_ballon (p. 1118 à 1122) : enveloppe « assemblage générateur + échangeur » qui se comporte comme un générateur (entrées Qreq_sto, θb_moy_ech ; sorties Qfou_sto, {Qcef}, Φvc_gnr).
2. Fiche 9.14 S2_GEN_Assemblage ballon(s) + générateur(s) (p. 1123 à 1133) : orchestration horaire des quatre étapes (puisage ECS, prélèvement chauffage, base, appoint), types d'assemblage Type_prod_stockage 0 à 3, consignes conventionnelles, répartition des consommations (1961), pertes récupérables (1962, 1963), contrôle de sous-dimensionnement (1960).
3. Fiche 8.23 C_GEN_THERMODYNAMIQUE_Elec, partie ECS et double/triple service (p. 725 à 738, 759 à 770, 785 à 798) : catégories Source_Ballon_Base_Thermodynamique_Elec (ECS seule, Tableau 148), _DoubleService (Tableau 149), _TripleService (Tableau 150) ; matrices COP/Pabs ECS par technologie (air extérieur, air extrait, air ambiant, eau de nappe, sol, eau glycolée) ; interpolation horaire ; limites de fonctionnement ; charge partielle (tout ou rien, variable) pour l'ECS seule ; mode ECS à pleine charge pour double/triple service avec Rfonctecs ; auxiliaires à charge nulle ; sorties.
4. Fiche 16.16 C_GEN_Appoint thermodynamique ECS et double service (p. 1698 à 1711) : PAC en appoint d'un ballon, résistance électrique d'appoint associée (Is_RE, Pnom_RE, Rat_faux, 3165 à 3169), valeurs COPutil_max (3159 à 3164).
5. Fiche 8.18 C_GEN_Générateur direct à effet joule (p. 668 à 671) pour la source Source_Ballon_Base_Effet_Joule / Source_Ballon_Appoint_Effet_Joule (Pmax, 1066 à 1072).
6. Fiche 9.22 PR1_IdCET (p. 1236 à 1255) : seulement la correspondance entre la typologie NF EN 16147 et les paramètres Th-BCE (2251 à 2263) ; l'identification Nelder-Mead (2226 à 2250) est un outil amont, hors moteur.
7. Interface stricte avec le ballon (9.9) et sa gestion-régulation (9.10) : condition d'enclenchement (1814, 1815), énergie requise (1816), température vue par l'échangeur (1784 à 1786), injection (1787), programmation (1811 à 1813). Ces équations sont citées parce que le générateur ne peut pas être testé sans elles, mais leur implémentation relève de la famille « ballon de stockage ».

HORS CHAMP et pourquoi :
- Le modèle de ballon lui-même (zones, puisage itératif 1792 à 1810, pertes 1771, mélange 1779, 1780, échangeur côté distribution 9.11, accumulateur en eau technique 9.12) : famille « stockage ».
- Les sources amont (8.26, 8.27 : θamont, auxiliaires de captage, Pech_source_amont_maxi) : famille « sources amont » ; on ne cite que ce qu'il faut (1407, 1408, 1454 à 1456).
- La gestion-régulation de la génération (8.17 : Qreq_ecs, θmax_ECS_gen, iECS_seule, cascade, Rpuis_dispo) : famille « génération ».
- Le mode chauffage et le mode refroidissement de la PAC (8.23.3.3, 8.23.3.5, matrices Tableaux 151 à 216) : famille « générateurs de chauffage/froid » ; seul le couplage par Rfonctecs (1294, 1295, 1326, 1327) est spécifié ici.
- Boucle solaire, CESI, CESCI, SSC (9.15 à 9.20, 9.23) : autre famille.
- Gestion optimisée de l'appoint (titre V, 9.10.3.3, 1817 à 1825) : hors du cas général ; signalée en point ouvert.
- PAC gaz, PAC CO2 (8.24, 16.5) : autres générateurs.

## Entrées (RSEE)

- `Generation` / `Pos_Gen` : Idpos_gen (9.14, 1962) ; entier 0/1 ; valeurs vues : 0 (hors volume chauffé) dans les deux RSEE
- `Generation` / `Theta_Wm_Ecs` : θmax,ECSgen (température départ ECS attendue par la génération) ; réel °C ; valeurs vues : 50
- `Generation` / `Type_Priorite` : idtype_priorite_gen ; entier ; valeurs vues : 2 (cascade, obligatoire avec stockage, 8.17 p. 651)
- `Generation/Production_Stockage_ECS_Collection/Production_Stockage` / `Id_Fou_Sto` : Idfousto ; entier 1/3/4 ; valeurs vues : 3
- `Production_Stockage` / `Type_prod_stockage` : Type_prod_stockage ; entier 0 à 3 ; valeurs vues : 1 (base PAC + appoint joule intégré), 0 (base joule seule)
- `Production_Stockage` / `nb_assembl` : nbassembl (1953, 1961 à 1963) ; entier ; valeurs vues : 28 (collectif, un CET par logement), 1
- `Production_Stockage` / `V_tot` : Vtot ; réel L ; valeurs vues : 175, 100
- `Production_Stockage` / `f_aux / Statut_faux` : faux (1951, zones V3=V4=faux.Vtot/2) ; réel 0..1 / entier ; valeurs vues : 0.5 / 0 ; 0 / 0
- `Production_Stockage` / `UA_S / Valeur_Certifiee_Justifiee_Defaut / Nature_Ballon` : UAS, Statut_UA (1767 à 1769) ; θamb des pertes 1771 ; réel W/K / entier 0,1,2 / entier ; valeurs vues : 2.94 / 2 / 1 ; 0 / 0 / 2
- `Production_Stockage` / `Theta_Cons` : θc_base = θc_ap, conventionnel 55 en ECS seule (1949) ; réel °C ; valeurs vues : 55
- `Production_Stockage` / `Theta_Max` : θmax du ballon (1780) ; réel °C ; valeurs vues : 90, 55
- `Production_Stockage` / `type_gest_th_base / type_gest_th_appoint` : typegest_base/ap (1811 à 1813) ; entier 0,1,2 ; valeurs vues : 2 / 2 (jour seulement) ; 0 / 0
- `Production_Stockage` / `Delta_Theta_base / Statut_Delta_Theta_Base` : Δθbase (1814, défaut 2 K) ; réel K / entier 1,2 ; valeurs vues : 2 / 1 ; 2 / 2
- `Production_Stockage` / `Delta_Theta_appoint / Statut_Delta_Theta_Appoint` : Δθap ; réel K / entier ; valeurs vues : 5 / 1 ; 2 / 2
- `Production_Stockage` / `hech_base / hech_appoint` : hrelech_base / hrelech_ap (1782 à 1786) ; réel 0..1 ; valeurs vues : 0 / 0 ; 0.2 / 0
- `Production_Stockage` / `z_reg_base / z_appoint / z_reg_appoint` : zreg_base, zap, zreg_ap (zbase = 1 imposé, 1948) ; entier 1..4 ; valeurs vues : 1 / 1 / 2 ; 1 / 3 / 0
- `Production_Stockage` / `Idpriorite_Ecs / Idpriorite_Ch` : idpriorite (8.17) ; entier ; valeurs vues : 1 / 1
- `Production_Stockage/Source_Ballon_Base_Collection/Source_Ballon_Base_Thermodynamique_Elec_TripleService (idem _DoubleService, et Source_Ballon_Base_Thermodynamique_Elec pour l'ECS seule)` / `Rdim` : Rdim (1296, 1328 à 1331) ; entier ; valeurs vues : 1
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Id_Source_Amont` : lien vers θamont(h) (8.26) ; entier (Index d'un Source_Amont de la génération) ; valeurs vues : 1
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Sys_Thermo_ts` : Sys_Thermo_ts ; entier 1..5 ; valeurs vues : 5 (air extérieur/air avec production ECS : Sys_thermo_Ecs = 1 air extérieur/eau, Tableau 150)
- `Source_Ballon_Base_Thermodynamique_Elec_DoubleService` / `Sys_Thermo_ds` : Sys_Thermo_ds (Tableau 149) ; entier 1..5 ; valeurs vues : non vu dans les deux RSEE lus
- `Source_Ballon_Base_Thermodynamique_Elec` / `Sys_Thermo_Ecs` : Sys_thermo_Ecs (Tableau 148) ; entier 1..6 ; valeurs vues : non vu (nom déduit de la nomenclature p. 727 ; à confirmer sur un RSEE à CET ECS seule)
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Statut_Donnee_Ecs` : Statut_données_PC_ECS ; entier 1/2 ; valeurs vues : 1
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Theta_Aval_Air_Eau_Ecs, Theta_Amont_Air_Eau_Ecs, Theta_Aval_Eau_De_Nappe_Eau_Ecs, Theta_Amont_Eau_De_Nappe_Eau_Ecs, Theta_Aval_Eau_Glycolee_Eau_Ecs, Theta_Amont_Eau_Glycolee_Eau_Ecs, Theta_Aval_Sol_Eau_Ecs, Theta_Amont_Sol_Eau_Ecs` : M_θ_Aval_Ecs, M_θ_Amont_Ecs (Tableaux 178, 181, 184, 187, 190, 193) ; entier 0..7 (nombre de températures saisies par technologie) ; valeurs vues : 1 / 1 pour air/eau, 0 ailleurs
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Performance_Ecs` : {Performance(i,j)}ecs (COP avant prétraitement) ; matrice texte 7 lignes (θaval 5,15,25,35,45,55,65) x N colonnes (θamont), lignes séparées par « ; », valeurs par espaces ; valeurs vues : 7x5, seule la case (5,3) = 3.5 non nulle
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Pabs_Ecs` : {Pabs(i,j)}ecs ; matrice texte, kW ; valeurs vues : case (5,3) = 0.79
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `COR_Ecs` : {COR(i,j)}ecs (1239) ; matrice texte 0/1/2 ; valeurs vues : case (5,3) = 1 (certifié)
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Statut_Val_Pivot_Ecs / Val_Cop_Ecs / Val_Pabs_Ecs` : Statut_val_pivot_ecs, Val_COP_ecs, Val_Pabs_ecs (1239) ; entier / réel / réel kW ; valeurs vues : 0 / 3.5 / 0.79 (statut 0 = non utilisé puisque Statut_Donnee_Ecs = 1)
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Lim_Theta_Ecs / Theta_Max_Av_Ecs / Theta_Min_Am_Ecs` : Lim_θ_ecs, θmax_av_ecs, θmin_am_ecs (1297) ; entier 0..2 / °C / °C ; valeurs vues : 0 / 25 / -5
- `Source_Ballon_Base_Thermodynamique_Elec_*` / `Statut_Taux_Ch / Taux_Ch` : Statut_Taux, Taux (1278 à 1280) ; entier / réel ; valeurs vues : 0 / 0.0035 (double et triple service : Waux,0 commun fondé sur le pivot chauffage)
- `Source_Ballon_Base_Thermodynamique_Elec (ECS seule)` / `Statut_Fonct_Part_Ecs, Fonctionnement_Compresseur_Ecs, Statut_Fonctionnement_Continu_Ecs, LRcontmin_Ecs, CCP_LRcontmin_Ecs, Statut_Taux_Ecs, Taux_Ecs` : Statut_fonct_part, Fonc_compr, Statut_fonct_continu, LRcontmin, CcpLRcontmin, Taux (1281 à 1283, 1299 à 1319) ; entiers / réels ; valeurs vues : non vus (noms déduits du motif _Ch/_Fr du triple service ; à confirmer)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Val_Pabs_Ch (et Performance_Ch, Pabs_Ch, COR_Ch, Statut_Donnee_Ch)` : {Pabs(ipivot,jpivot)}ch servant à Waux,0 (1278, p. 785) ; réel kW ; matrices ; valeurs vues : 1.42 ; pivot chauffage (4,4) de la matrice air/eau
- `Production_Stockage/Source_Ballon_Appoint_Collection/Source_Ballon_Appoint_Effet_Joule (et Source_Ballon_Base_Effet_Joule)` / `Pmax` : Pngen = Pmax (1067) ; en 16.16 Pnom_RE ; réel kW ; valeurs vues : 1.5 (appoint), 2 (base)
- `Source_Ballon_*_Effet_Joule` / `Id_Fou_Gen` : idfougen (8.18.3.1) ; entier 1/3 ; valeurs vues : 3
- `Source_Ballon_*_Effet_Joule` / `Rdim` : Rdim ; entier ; valeurs vues : 1
- `Generation/Source_Amont_Collection/Source_Amont` / `Id_Fl_Amont / Source_Amont_Air / Source_Amont_Eau` : idfluide_amont, idamont-air-type (1406 à 1408) ; entier 1,2,3 / entier / entier ; valeurs vues : 2 / 1 / 0 (air extérieur)
- `Source_Amont` / `Id_SF_Extraction, Tair_Lim, Pvent_Gaine` : air extrait : Qm_air_extrait, Tair_lim (1454 à 1456) ; ventilateur de gaine ; entier / °C / W ; valeurs vues : 0 / 0 / 0
- `Source_Amont` / `Id_Et` : espace tampon dont θet(h) sert de θamont en air ambiant (1407) ; entier ; valeurs vues : 0
- `(16.16, non vu dans les RSEE lus)` / `Is_RE, Pnom_RE, faux_RE, Rat_faux, Cat (1001), idfougen, Sys_thermo (1..6)` : paramètres de la fiche 16.16 ; entiers / réels ; valeurs vues : aucun nœud XML identifié pour l'appoint thermodynamique dans les deux RSEE ; nom de nœud à relever sur un RSEE qui en contient

## Paramètres conventionnels

- zbase (zone de l'échangeur de base) = 1 (p. 1127 (1948))
- θc_base = θc_ap pour un ballon ECS seule (Idfousto = 3) = 55 °C, non paramétrable ; jamais < 55 °C ni < θmax,ECSgen en ECS (p. 1127 (1949))
- Nb_iter_vp = 4 pour Type_prod_stockage 0 ou 3 ; arrondi.inf(2 / min(faux, 1 - faux)) pour le type 1 ; arrondi.inf((Vtot_princ + Vtot_sec) / Vz,min) pour le type 2 (p. 1128 (1951))
- zp,ECS / zinj,ECS = 4 / 1 (p. 1065 (1773), 1131)
- Pertes de l'échangeur générateur-ballon vers le volume chauffé = 0 (p. 1122)
- Report des consommations si Qreq_ch = Qreq_ecs = 0 = sur le chauffage si Idfousto = 1, sur l'ECS si Idfousto = 3 (p. 1133 (note 2 de 1961))
- Seuil d'alerte de ballon jamais à consigne = 168 h consécutives (p. 1132 (1960))
- ρw . cw = 1 kg/L x 1,163 Wh/(kg.K) (p. 1125 (Tableau 291))
- θbz initial au premier pas de temps = 50 °C (p. 1064 (note sous 1772))
- Val_util_max COP ECS air extérieur/eau = 2,7 ; pivot (θamont 7, θaval 45), indices (5,3) (p. 759)
- Val_util_max COP ECS air extrait/eau = 3,2 ; pivot (20, 45), indices (5,4) (p. 761)
- Val_util_max COP ECS air ambiant/eau = 3,1 ; pivot (15, 45) selon Tableau 184 (le texte p. 763 dit θamont = 20 mais l'ordre de saisie met 15 °C en premier) ; indices (5,3) (p. 763)
- Val_util_max COP ECS eau de nappe/eau = 3,7 ; pivot (8,5, 45), indices (5,2) (p. 765)
- Val_util_max COP ECS sol/eau = 3,0 ; pivot (4, 45), indices (5,2) ; IdFluide_amont = 3 (p. 767)
- Val_util_max COP ECS eau glycolée/eau = 3,7 ; pivot (-1,5, 45), indices (5,2) (p. 769)
- Cnnav_COP ECS (communs à toutes les technologies ECS) = (35,45)=1,2 ; (25,45)=1,4 ; (55,45)=0,8 ; (15,45)=1,6 ; (65,45)=0,6 ; (5,45)=1,8 (p. 760, 762, 764, 766, 768, 770 (Tableaux 179, 182, 185, 188, 191, 194))
- Cnnav_Pabs ECS (communs) = (35,45)=1,10 ; (25,45)=1,20 ; (55,45)=0,90 ; (15,45)=1,30 ; (65,45)=0,80 ; (5,45)=1,40 (p. 760, 762, 766, 768, 770 (Tableaux 180, 183, 189, 192, 195))
- Cnnam_COP / Cnnam_Pabs air extérieur/eau ECS = COP : (2,7)=0,80 ; (20,7)=1,25 ; (-7,7)=0,50 ; (35,7)=1,50. Pabs : (2,7)=0,95 ; (20,7)=1,13 ; (-7,7)=0,86 ; (35,7)=1,28 (p. 760 (Tableaux 179, 180))
- Cnnam_COP / Cnnam_Pabs air extrait/eau ECS = COP : (15,20)=0,9 ; (25,20)=1,1 ; (10,20)=0,8 ; (30,20)=1,2 ; (5,20)=0,7. Pabs : (15,20)=0,95 ; (25,20)=1,05 ; (10,20)=0,90 ; (30,20)=1,10 ; (5,20)=0,85 (p. 762 (Tableaux 182, 183))
- Cnnam_COP air ambiant/eau ECS = (20,15)=1,1 ; (10,15)=0,9 ; (25,15)=1,2 ; (30,15)=1,3 ; (5,15)=0,8 ; Cnnam_Pabs (Tableau 186, p. 764) non relevé dans cette passe (p. 764 (Tableau 185))
- Cnnam_COP / Cnnam_Pabs eau de nappe/eau ECS = COP : (3,5;8,5)=0,9 ; (13,5;8,5)=1,1 ; (18,5;8,5)=1,2. Pabs : (3,5;8,5)=0,95 ; (13,5;8,5)=1,05 ; (18,5;8,5)=0,90 (valeur telle qu'imprimée, probablement une coquille pour 1,10) (p. 766 (Tableaux 188, 189))
- Cnnam_COP / Cnnam_Pabs sol/eau ECS = COP : (1,5;4)=0,95 ; (-4;4)=0,8 ; (6,5;4)=1,07. Pabs : tous = 1 (p. 768 (Tableaux 191, 192))
- Cnnam_COP / Cnnam_Pabs eau glycolée/eau ECS = COP : (3,5;-1,5)=1,10 ; (8,5;-1,5)=1,20 ; (-6,5;-1,5)=0,90 ; (13,5;-1,5)=1,30. Pabs : 1,05 ; 1,10 ; 0,95 ; 1,15 (p. 770 (Tableaux 194, 195))
- Corrections de statut du COP = certifié x1 ; justifié x0,9 ; déclaré : min(0,8 x Val_COP ; Val_util_max) ; par défaut : 0,8 x Val_util_max. Pabs jamais corrigée (p. 733, 740 (1239), 1706)
- Taux (auxiliaires à charge nulle) = certifié : saisi ; justifié : x1,1 ; défaut : 0,02 en chauffage ou ECS, 0,01 en froid (p. 785 (1279, 1280))
- Deq = 0,5 min (p. 785)
- Dfou0 mode ECS = 26 min ; chauffage : 32/19/6/2 min selon Typo_emetteur 1 à 4 (p. 786 (Tableau 217))
- LRcontmin / CcpLRcontmin par défaut (Fonc_compr = 1) = 0,4 / 1 ; justifiés : LRcontmin + 0,05 et CcpLRcontmin x 0,9 (p. 786 (1281, 1282))
- Contrôle de cohérence charge partielle = erreur si LRcontmin x 0,3 < CcpLRcontmin x Taux (p. 787 (1283))
- Ratbasc,fr-ECS = 0,25 h (p. 732, 791 (1295))
- Double/triple service : mode ECS sans charge partielle = Deq, Dfou0, LRcontmin, CcpLRcontmin non définis pour l'ECS (p. 786, 787)
- Waux,0 double/triple service = Taux x Pabs pivot du mode chauffage, commun à tous les modes, compté une seule fois (p. 785, 796)
- Idengen électricité = 50 (p. 730, 1701)
- Effet joule : rendement, Waux, Φvc = 1, 0, 0 ; type 500 ; idfougen 1 ou 3 seulement (p. 670 (1066))
- COPutil_max appoint thermodynamique (16.16) = air ext : ch 3,5 / ECS 2,7 ; nappe : 4,7 / 3,7 ; glycolée : 3,7 / 3,7 ; sol : 3,8 / 3,0 ; air extrait ECS 3,2 ; air ambiant ECS 3,1 (p. 1707, 1708 (3159 à 3164))
- Période nuit (Is_RE = 2, typegest = 1) = hleg > 23 h ou hleg < 5 h ; jour seulement : 10 h < hleg < 17 h (p. 1081 (1812, 1813), 1710)
- IdCET : Taux_Th-BCE = 0,02 si Isaux = 0, 0 si Isaux = 1 ; Fonc_compr = 2 ; δθbase = 2 K (p. 1254, 1255 (2251, 2252, 2261, 2263))
- IdCET : correspondance source = Typesource 0/1 -> Syst_Thermo_ECS 1, air type 1 ; 2 -> 3, air type 2 ; 3 -> 2, air type 3 ; 4 -> 4, fluide eau (p. 1255 (2257 à 2260))

## Équations

- (1946, p. 1120) Qreq_sto = Qreq_sto_base (base) ou Qreq_sto_ap (appoint) ; demande transmise par la gestion-régulation du ballon ; prétraitement 9.13
- (1947, p. 1122) Qfou_sto = Qfou_sto_base ou Qfou_sto_ap ; {Qcef_assemblage} = {Qcef_gnr} ; Φvc_gnr issu du générateur ; - ; post-traitement 9.13 ; pertes de l'échangeur nulles
- (1948, p. 1127) zbase = 1 ; - ; toujours
- (1949, p. 1127) θc_base = θc_ap = 55 °C ; - ; Idfousto = 3 ; en général θc_base >= θc_ap, θc >= 55 et >= θmax,ECSgen
- (1950, p. 1127) Vz,min = min(Vz,min_principal ; Vz,min_secondaire) ; - ; Type_prod_stockage = 2
- (1951, p. 1128) Nb_iter_vp = 4 (types 0, 3) ; floor(2 / min(faux, 1 - faux)) (type 1) ; floor((Vtot_p + Vtot_s) / Vz,min) (type 2) ; faux ; la valeur 4 est une image dans le PDF, lue par reconstitution
- (1952, p. 1129) θentrant,ECS = (Vsoutire,ECS . θcw + qv_boucle,ECS . θretour,aval,ECS) / (Vsoutire,ECS + qv_boucle,ECS) ; θcw eau froide, boucle ECS ; réseau bouclé ; sans boucle θentrant = θcw
- (1953, p. 1129) Qw_sto_unit(h) = Qreq,ECS(h) / Nb_assemblage ; - ; étape 1
- (1954, p. 1129) Qrest_ECS(h) = Qw_sto_unit_report(i-1) (dernière itération) ; - ; fin de boucle de puisage
- (1955, p. 1129) Qfou_ECS(h) = Qreq_ECS(h) - Qrest_ECS(h) ; - ; -
- (1956 à 1959, p. 1130) θentrant,CH = θretour,aval,CH ; Qw_sto_unit = Qreq,CH / Nb_assemblage ; Qrest_CH = report ; Qfou_CH = Qreq_CH - Qrest_CH ; - ; étape 2, Idfousto 1 ou 4 seulement
- (1960, p. 1132) si θb4(h) < θc : nbh_temp_sto_insuff(h) = nbh(h-1) + 1 sinon 0 ; erreur si > 168 ; θc = θc_base (base seule) ou θc_ap ; θb4 zone haute ; tous assemblages sauf type 3 ; condition partiellement en image
- (1961, p. 1133) {Qcef_assemblage(po;en)} = nb_assembl x [ Qcons_base . (Qreq_ch E(1;en) + Qreq_ecs E(3;en)) / (Qreq_ecs + Qreq_ch) + Qcons_ap . (idem) + (Waux_pro_base + Waux_pro_ap) . (Qreq_ch E(1;50) + Qreq_ecs E(3;50)) / (Qreq_ecs + Qreq_ch) ] ; E(po;en) matrice unité ; en = Idengen ; remplace la matrice du contrat générateur ; si les deux Qreq sont nuls, tout sur le chauffage (Idfousto 1) ou l'ECS (Idfousto 3)
- (1962, p. 1133) Φvc_sto(h) = nb_assembl . Idpos_gen . (Φpertes_principal + Φpertes_secondaire) ; Φpertes (1772) ; récupérable si Idpos_gen = 1
- (1963, p. 1133) Φvc_gnr(h) = nb_assembl . Φvc_gnr_base + nb_assembl . Φvc_gnr_ap ; - ; PAC et joule : Φvc = 0
- (1811 à 1813, p. 1081) fp = 1 (permanent) ; fp = 1 si hleg > 23 ou hleg < 5 (nuit) ; fp = 1 si 10 < hleg < 17 (jour) ; sinon 0 ; type_gest_th_base/appoint ; si fp = 0 alors Qreq_sto = 0
- (1814, p. 1081) iactive = Vp(h) > 0 ou θb(zreg)(h-1) < θc - Δθ ou (θc - Δθ <= θb(zreg)(h-1) < θc et θb(zreg)(h-2) < θb(zreg)(h-1)) ; hystérésis Δθ (défaut 2 K) ; base et appoint, avec leurs propres zreg, θc, Δθ
- (1815, p. 1082) condition supplémentaire base seule : θb(zreg_base)(h-1) < θc_base + Φpertes,zreg(h-1) / (ρw cw V(zreg_base)) ; - ; Type_prod_stockage = 0
- (1816, p. 1082) Qreq_sto = max( ρw cw . Σ_{z>=zech} Vz . (θc - Σ Vz θbz(i-1) / Σ Vz) + Σ_{z>=zech} Φpertes,z ; 0 ) ; θbz après puisage, zech = zbase ou zap ; si iactive = vrai
- (1784 à 1786, p. 1068, 1069) θb_moy_ech = θb(zech) si hrelech = 0 ; sinon (Σ_{z=zech}^{zmax-1} hrelz θbz + hrelrest θb(zmax)) / hrelech, avec θbz = (θbz(h-1) + θbz(i-1)) / 2 ; hrelz = Vz / Vtot (1782, 1783) ; température aval du générateur
- (1787, p. 1069) θbz(i) = θbz(i-1) + (Qinj,z - Φpertes,z) / (ρw cw Vz) ; Qinj,zech = Qfou_sto, 0 ailleurs (toute l'énergie dans la zone zech, p. 1067) ; puis mélange (1779) et plafond θmax (1780) ; - ; échangeur intégré ; pertes comptées une seule fois par pas
- (1239 (transposée ECS, p. 759 à 769), p. 740) Statut_PC = 1 : COPutil(i,j) = Perf(i,j) si COR = 1, 0,9 Perf si COR = 2 ; Statut_PC = 2 : COPutil(pivot) = min(0,8 Val_COP ; Val_util_max) si Statut_val_pivot = 1, 0,8 Val_util_max si 2 ; pivot (5,3) air ext et air ambiant, (5,4) air extrait, (5,2) nappe, sol, glycolée ; contrôle préalable : valeurs non nulles hors des coordonnées M_θ -> erreur ; valeurs nulles aux coordonnées requises -> erreur
- (1257, p. 760) colonne pivot : COPutil(1,jp) = COPutil(5,jp) . Cnnav(5,45) ; (2,jp) . Cnnav(15,45) ; (3,jp) . Cnnav(25,45) ; (4,jp) . Cnnav(35,45) ; (6,jp) . Cnnav(55,45) ; (7,jp) . Cnnav(65,45), chacune si la case vaut 0 ; lignes 1..7 = θaval 5,15,25,35,45,55,65 ; commun à toutes les technologies ECS
- (1258, p. 760) air ext : pour i = 1..7, COPutil(i,1) = COPutil(i,3) Cnnam(-7,7) ; (i,2) . Cnnam(2,7) ; (i,4) . Cnnam(20,7) ; (i,5) . Cnnam(35,7) si nulles ; idem Pabs avec Tableau 180 ; colonnes θamont -7, 2, 7, 20, 35 ; -
- (1259, p. 762) air extrait : (i,1) = (i,4) Cnnam(5,20) ; (i,2) . Cnnam(10,20) ; (i,3) . Cnnam(15,20) ; (i,5) . Cnnam(25,20) ; (i,6) . Cnnam(30,20) ; colonnes 5,10,15,20,25,30 ; -
- (1260 (déduit, numéro non lu), p. 764) air ambiant : propagation depuis la colonne pivot 15 °C avec Cnnam(20,15), (10,15), (25,15), (30,15), (5,15) ; colonnes 5,10,15,20,25,30 ; page 764 non lue intégralement
- (1261, p. 766) nappe : (i,1) = (i,2) Cnnam(3,5;8,5) ; (i,3) . Cnnam(13,5;8,5) ; (i,4) . Cnnam(18,5;8,5) ; colonnes 3,5 ; 8,5 ; 13,5 ; 18,5 (moyenne départ/retour) ; -
- (1262, p. 768) sol : (i,1) = (i,3) Cnnam(-4;4) ; (i,2) . Cnnam(1,5;4) ; (i,4) . Cnnam(6,5;4) ; colonnes -4 ; 1,5 ; 4 ; 6,5 ; -
- (1263, p. 770) glycolée : (i,1) = (i,2) Cnnam(-6,5;-1,5) ; (i,3) . Cnnam(3,5;-1,5) ; (i,4) . Cnnam(8,5;-1,5) ; (i,5) . Cnnam(13,5;-1,5) ; colonnes -6,5 ; -1,5 ; 3,5 ; 8,5 ; 13,5 ; -
- (1278, p. 785) Waux,0 = Taux x Pabs(ipivot, jpivot) ; Pabs pivot du mode (ECS seule) ou du mode chauffage (double/triple) ; constante du calcul
- (1279, 1280, p. 785) Taux = 0,02 (chauffage ou ECS) ; 0,01 (froid) ; - ; Statut_taux = 2 ; = 1 : Taux x 1,1
- (1281, 1282, p. 786) LRcontmin = 0,4 ; CcpLRcontmin = 1 ; - ; Fonc_compr = 1 et Statut_fonct_continu = 2
- (1283, p. 787) erreur si LRcontmin x 0,3 < CcpLRcontmin x Taux ; - ; prétraitement
- (1284, 1285, p. 788, 789) encadrement : si θ < Val(1) : j1 = j2 = 1, θ1 = θ, θ2 = Val(1) ; si θ > Val(N) : j1 = j2 = N, θ1 = Val(N), θ2 = θ ; sinon premier j avec θ <= Val(j) : j1 = j-1, j2 = j ; θamont -> colonnes j ; θaval -> lignes i ; hors plage : extrapolation constante (coefficient 0 ou 1)
- (1286, p. 789) Cθam = (θamont - θam1) / (θam2 - θam1) ; Cθav = (θaval - θav1) / (θav2 - θav1) ; - ; division par zéro hors plage : voir point ouvert
- (1287, p. 789) Pabs_pc = (1-Cam)(1-Cav) Pabs(i1,j1) + Cam(1-Cav) Pabs(i1,j2) + Cav(1-Cam) Pabs(i2,j1) + Cam Cav Pabs(i2,j2) ; kW -> W ; -
- (1288, p. 789) COP_pc = même interpolation sur COPutil ; - ; chauffage ou ECS
- (1290, p. 790) Pfou_pc_brut = Pabs_pc x COP_pc ; - ; -
- (1292, p. 790, 906) Pfou_pc_brut = min(Pabs_pc . COP_pc ; Pfou_source_amont_maxi) ; 1454 à 1456 : Qm_act = Qm_air_extrait / Rdim ; Pech = Qm_act . Cpa . max(0 ; θamont - Tair_lim) ; Pfou_maxi = Pech . Pfou_pc_brut / (Pfou_pc_brut - Pabs_pc) ; Sys_thermo_Ecs = 2 (air extrait)
- (1294, p. 790) Pfou_pc_brut_ch = Pabs_pc . COP_pc . (1 - Rat_Fonct_ECS(h)) ; Rfonctecs du même pas ; double/triple service, mode chauffage après l'ECS
- (1295, p. 791) Pfou_pc_brut_fr = Pabs_pc . COP_pc . (1 - Rat_Fonct_ECS - Ratbasc,ECS/FR) ; Ratbasc = 0,25 ; triple service, ECS puis froid ; froid prioritaire sur chauffage
- (1296, p. 791) Qreq_act = Qreq / Rdim ; - ; -
- (1297, p. 791) Lim_θ = 0 : Pfou_pc = Pfou_pc_brut, Qrest_act = max(0 ; Qreq_act - Pfou_pc) ; Lim_θ = 1 et (θamont < θmin_am ou θaval > θmax_av) : Pfou_pc = 0, Qrest_act = Qreq_act ; Lim_θ = 2 et (les deux) : idem ; θaval = θb_moy_ech ; mode chauffage/ECS
- (1299, 1300, p. 792) Pfou_LR = min(Qreq_act ; Pfou_pc) ; LR = Pfou_LR / Pfou_pc (0 si Pfou_pc = 0) ; - ; ECS seule
- (1301 à 1305, p. 793) Pcomp_pc = Pabs_pc - Waux,0 ; Pcomp_LR = Pcomp_pc . LR ; Pcompma_LR = Pcomp_pc . Deq . LR (1 - LR) / Dfou0 ; Pabs_LR = Pcomp_LR + Pcompma_LR + Waux,0 ; COP_LR = Pfou_LR / Pabs_LR ; Deq = 0,5, Dfou0 = 26 (ECS) ; Fonc_compr = 2, ECS seule
- (1306 à 1312, p. 793, 794) Pcomp_pc = Pabs_pc - Waux,0 ; COP_pc_net = Pfou_pc_brut / Pcomp_pc ; CcpLRcontmin_net = LRcontmin . Pcomp_pc . Ccp / (LRcontmin . Pabs_pc - Ccp . Waux,0) ; COP_LR_net = COP_pc_net . (1 + (Ccp_net - 1)(1 - LR)/(1 - LRcontmin)) ; Pcomp_LR = Pfou_LR / COP_LR_net ; Pabs_LR = Pcomp_LR + Waux,0 ; COP_LR = Pfou_LR / Pabs_LR ; - ; Fonc_compr = 1 et LRcontmin <= LR <= 1
- (1313 à 1319, p. 794) Pfou_LRcontmin = Pfou_pc_brut . LRcontmin ; Pcomp_LRcontmin = Pfou_LRcontmin / COP_LRcontmin_net ; Pcomp_LR = Pcomp_LRcontmin . (1 - (LRcontmin - LR)/LRcontmin) ; LRcycl = LR / LRcontmin ; Pcompma_LR = Pcomp_LRcontmin . Deq . LRcycl (1 - LRcycl) / Dfou0 ; Pabs_LR = Pcomp_LR + Pcompma_LR + Waux,0 ; COP_LR = Pfou_LR / Pabs_LR ; COP_LRcontmin_net = COP_pc_net . Ccp_net (déduit de 1309 en LR = LRcontmin) ; Fonc_compr = 1 et LR < LRcontmin
- (1320 à 1324, p. 795) Pfou_LR = min(Qreq_act ; Pfou_pc) ; LR = Pfou_LR / Pfou_pc ; si iECS_seule faux : Pabs_LR = Pabs_pc ; si vrai : Pabs_LR = Pabs_pc + (1 - LR) Waux,0 ; COP_LR = Pfou_LR / Pabs_LR ; iECS_seule (8.17 : idfougen = 3 ou chauffage non autorisé ce jour) ; double/triple service, mode ECS à pleine charge sur une fraction LR du pas
- (1325, p. 795) Pabs_LR = Waux,0 ; - ; mono-service à charge nulle, comptée en saison du poste
- (1326, 1327, p. 796) Pabs_LR_ch = (1 - Rat_Fonct_ECS) . Waux,0 ; - ; double/triple service en saison de chauffage avec Qreq_ecs > 0 et Qreq_ch = 0 ; même règle en froid
- (1328 à 1332, p. 797) Qcef_po(Idengen) = Pabs_LR . Rdim ; ηeff = COP_LR ; Qfou_po = Pfou_LR . Rdim ; Qrest_po = Qrest_act . Rdim ; τcharge = LR ; po = ecs ; par mode
- (1334, p. 797) Φrejet,ecs = min(0 ; Pcomp_LR + Pcompma_LR - Pfou_LR) . Rdim ; - ; transmis à la source amont
- (1336 à 1339, p. 797, 798) Qfou = Σ modes ; Qcons = Σ Qcef ; Waux,pro = Waux,0 . Rdim ; Φrejet = Σ modes ; - ; -
- (Rfonctecs (non numérotée), p. 788, 795) Rfonctecs(h) = LR_ecs(h) (= τcharge,ecs) ; Rpuis_dispo = 1 - Rfonctecs ; - ; déduit de la Figure 139 p. 795 et de 1072 pour le joule ; aucune équation explicite pour la PAC
- (1066 à 1072, p. 670) η = 1, Waux,pro = 0, Φ = 0 ; Pmax = Pngen ; Qfou = min(Qreq ; Pmax) ; Qcons = Qfou ; Qrest = Qreq - Qcons ; τcharge = Qfou / Pmax (image) ; Φvc = 0 ; Rfonctecs = τcharge ; Pngen = Pmax (RSEE, kW) ; effet joule, Qcef(3;50)
- (3159 à 3164, p. 1707, 1708) COPutil_max par technologie (voir paramètres) ; - ; appoint thermodynamique
- (3165, 3166, p. 1709) Waux,0 = Taux . Pabs_pivot_ecs (idfougen = 3) ; Taux . Pabs_pivot_ch (idfougen = 4) ; - ; appoint thermodynamique
- (3167 à 3169, p. 1711) Qreq_RE = Rat_faux . Qrest ; Qfou_RE = min(Qreq_RE ; Pnom_RE) ; Qcons_RE = Qfou_RE ; Qfou += Qfou_RE ; Qrest -= Qfou_RE ; Qcons et Qcef(ECS;élec) += Qcons_RE ; Rat_faux = faux_RE / faux ; Is_RE = 1 toujours, Is_RE = 2 si hleg > 23 ou < 5
- (2257 à 2263, p. 1255) correspondance IdCET -> Th-BCE (voir paramètres) ; Fonc_compr = 2 ; Vtot = Vtot_IdCET ; δθbase = 2 ; - ; CET saisi par IdCET
- (1406 à 1408, p. 896) θamont = θext (air extérieur) ; θet (air ambiant d'espace tampon) ; Tair_extrait (air extrait) ; - ; source amont air

## Algorithme

```
# Prétraitement (une fois par Production_Stockage, module proposé : openbce/generateurs_ballon.py)
def preparer_pac_ecs(src: Noeud, categorie):            # categorie in {ECS_SEULE, DOUBLE, TRIPLE}
    sys_ecs = {ECS_SEULE: src.entier("Sys_Thermo_Ecs"),
               DOUBLE: TABLEAU_149[src.entier("Sys_Thermo_ds")],      # 1->1, 2->4, 3->6, 4->5, 5->1
               TRIPLE: TABLEAU_150[src.entier("Sys_Thermo_ts")]}[categorie]   # 1->1, 2->4, 3->6, 5->1
    techno = TECHNO_ECS[sys_ecs]      # θaval = (5,15,25,35,45,55,65) ; θamont, pivot (ip, jp), Val_util_max, Cnnav/Cnnam COP et Pabs (Tableaux 179 à 195)
    perf, pabs, cor = matrices(src, "Performance_Ecs"), matrices(src, "Pabs_Ecs"), matrices(src, "COR_Ecs")   # texte « ; » lignes, espaces colonnes
    controler_coordonnees(perf, pabs, cor, M_aval, M_amont)   # p. 739 : erreurs si hors coordonnées ou nulles aux coordonnées requises
    cop = zeros(7, len(techno.amont))
    if src.entier("Statut_Donnee_Ecs") == 1:                         # (1239)
        cop[cor == 1] = perf[cor == 1]; cop[cor == 2] = 0.9 * perf[cor == 2]
    else:
        pivot = src.nombre("Val_Cop_Ecs"); pabs[ip, jp] = src.nombre("Val_Pabs_Ecs")
        cop[ip, jp] = min(0.8 * pivot, techno.val_util_max) if src.entier("Statut_Val_Pivot_Ecs") == 1 else 0.8 * techno.val_util_max
    remplir_colonne_pivot(cop, techno.cnnav_cop); remplir_lignes(cop, techno.cnnam_cop)       # (1257), (1258 à 1263) ; ne jamais écraser une case non nulle
    remplir_colonne_pivot(pabs, techno.cnnav_pabs); remplir_lignes(pabs, techno.cnnam_pabs)
    pabs *= 1000.0                                                     # kW -> W
    # auxiliaires à charge nulle (1278 à 1280) ; double/triple : pivot du mode chauffage, p. 785
    taux = src.nombre("Taux_Ecs" if categorie == ECS_SEULE else "Taux_Ch", 0.02)
    statut = src.entier("Statut_Taux_Ecs" if categorie == ECS_SEULE else "Statut_Taux_Ch", 2)
    taux = {0: taux, 1: 1.1 * taux, 2: 0.02}[statut]
    pabs_pivot_ref = pabs[ip, jp] if categorie == ECS_SEULE else 1000 * pivot_chauffage(src)     # Val_Pabs_Ch ou Pabs_Ch(4,4)
    waux0 = taux * pabs_pivot_ref
    if categorie == ECS_SEULE:                                         # charge partielle (786, 787)
        fonc = src.entier("Fonctionnement_Compresseur_Ecs", 2); deq, dfou0 = 0.5, 26.0
        lrmin, ccp = (0.4, 1.0)
        if fonc == 1:
            st = src.entier("Statut_Fonctionnement_Continu_Ecs", 2)
            if st == 0: lrmin, ccp = src.nombre("LRcontmin_Ecs"), src.nombre("CCP_LRcontmin_Ecs")
            if st == 1: lrmin, ccp = src.nombre("LRcontmin_Ecs") + 0.05, 0.9 * src.nombre("CCP_LRcontmin_Ecs")
        if lrmin * 0.3 < ccp * taux: erreur("(1283)")
    return PacEcs(cop, pabs, techno, waux0, lim=src.entier("Lim_Theta_Ecs"), tmax_av=src.nombre("Theta_Max_Av_Ecs"), tmin_am=src.nombre("Theta_Min_Am_Ecs"),
                  rdim=src.entier("Rdim", 1), fonc=fonc, deq=deq, dfou0=dfou0, lrmin=lrmin, ccp=ccp, categorie=categorie, air_extrait=(sys_ecs == 2))

# Pleine charge aux températures réelles (1284 à 1297) ; θaval = θb_moy_ech, θamont de la source amont
def pleine_charge(pac, t_amont, t_aval, qreq_act, p_source_maxi=None):
    j1, j2, cam = encadrer(pac.techno.amont, t_amont)                  # (1284), (1286) ; hors plage : j1 = j2 et coefficient 0 ou 1
    i1, i2, cav = encadrer(pac.techno.aval, t_aval)                    # (1285)
    pabs_pc = bilin(pac.pabs, i1, i2, j1, j2, cam, cav)                # (1287)
    cop_pc = bilin(pac.cop, i1, i2, j1, j2, cam, cav)                  # (1288)
    pfou_brut = pabs_pc * cop_pc                                       # (1290)
    if pac.air_extrait and p_source_maxi is not None: pfou_brut = min(pfou_brut, p_source_maxi)   # (1292), (1454 à 1456)
    bloque = (pac.lim == 1 and (t_amont < pac.tmin_am or t_aval > pac.tmax_av)) or (pac.lim == 2 and t_amont < pac.tmin_am and t_aval > pac.tmax_av)
    pfou_pc = 0.0 if bloque else pfou_brut                             # (1297)
    qrest_act = qreq_act if bloque else max(0.0, qreq_act - pfou_pc)
    return pabs_pc, cop_pc, pfou_brut, pfou_pc, qrest_act

# Appel du générateur PAC en mode ECS (contrat 9.13 : Qreq_sto, θb_moy_ech -> Qfou_sto, Qcons, Rfonctecs)
def pac_ecs_heure(pac, qreq_sto, t_amont, t_aval, iecs_seule, p_source_maxi=None):
    qreq_act = qreq_sto / pac.rdim                                     # (1296)
    pabs_pc, cop_pc, pfou_brut, pfou_pc, qrest_act = pleine_charge(pac, t_amont, t_aval, qreq_act, p_source_maxi)
    pfou_lr = min(qreq_act, pfou_pc); lr = pfou_lr / pfou_pc if pfou_pc > 0 else 0.0     # (1299), (1300) ou (1320), (1321)
    if pac.categorie != ECS_SEULE:                                     # double/triple : pleine charge sur une fraction du pas (1322 à 1324)
        pabs_lr = pabs_pc if not iecs_seule else pabs_pc + (1 - lr) * pac.waux0
        if lr == 0 and not iecs_seule: pabs_lr = 0.0                   # Waux,0 porté par le mode chauffage ce pas (1326), voir points ouverts
        pcomp_lr, pcompma = pabs_pc - pac.waux0, 0.0
    elif qreq_act <= 0 or pfou_pc <= 0:
        pabs_lr, pcomp_lr, pcompma = pac.waux0, 0.0, 0.0               # (1325) ; comptée toute l'année pour un mono-service ECS (saison ECS permanente)
    elif pac.fonc == 2:                                                # tout ou rien (1301 à 1305)
        pcomp_pc = pabs_pc - pac.waux0; pcomp_lr = pcomp_pc * lr
        pcompma = pcomp_pc * pac.deq * lr * (1 - lr) / pac.dfou0
        pabs_lr = pcomp_lr + pcompma + pac.waux0
    else:                                                              # variable (1306 à 1319)
        pcomp_pc = pabs_pc - pac.waux0; cop_net = pfou_brut / pcomp_pc
        ccp_net = pac.lrmin * pcomp_pc * pac.ccp / (pac.lrmin * pabs_pc - pac.ccp * pac.waux0)
        if lr >= pac.lrmin:
            pcomp_lr = pfou_lr / (cop_net * (1 + (ccp_net - 1) * (1 - lr) / (1 - pac.lrmin))); pcompma = 0.0
        else:
            pcomp_min = pfou_brut * pac.lrmin / (cop_net * ccp_net)
            pcomp_lr = pcomp_min * (1 - (pac.lrmin - lr) / pac.lrmin)
            lrc = lr / pac.lrmin; pcompma = pcomp_min * pac.deq * lrc * (1 - lrc) / pac.dfou0
        pabs_lr = pcomp_lr + pcompma + pac.waux0
    qcef_elec = pabs_lr * pac.rdim                                     # (1328) -> Qcef(3;50)
    return Resultat(qfou=pfou_lr * pac.rdim, qrest=qrest_act * pac.rdim, qcons=qcef_elec, eta=(pfou_lr / pabs_lr if pabs_lr else 0), tau=lr,
                    rfonctecs=lr, rejet=min(0.0, pcomp_lr + pcompma - pfou_lr) * pac.rdim, waux_pro=pac.waux0 * pac.rdim, phi_vc=0.0)   # (1329 à 1334), (1338)

def joule_heure(pmax_w, qreq):                                         # 8.18 (1066 à 1072)
    qfou = min(qreq, pmax_w); return Resultat(qfou=qfou, qrest=qreq - qfou, qcons=qfou, eta=1.0, tau=qfou / pmax_w if pmax_w else 0, rfonctecs=qfou / pmax_w if pmax_w else 0, rejet=0, waux_pro=0, phi_vc=0)

# Pas de temps de l'assemblage 9.14 (un ballon, Type_prod_stockage 0 ou 1 ; états conservés : θbz(h-1), θbz(h-2), Qw_sto_unit_report, nbh_temp_insuff, nbh_report, Rfonctecs pour le second appel chauffage)
def assemblage_heure(etat, ps: Noeud, base, appoint, qreq_ecs, qreq_ch, t_cw, t_retour_boucle, qv_boucle, v_soutire, t_depart_ecs, t_amb, t_amont, hleg, iecs_seule, idpos_gen, nb):
    phi_z = [etat.Uz[z] * (etat.theta[z] - t_amb) for z in Z]                       # (1771), Uz = UAS_util Vz / Vtot (1770)
    # étape 1 : puisage ECS (famille ballon) : (1952) à (1955) + boucle (1792) à (1800), Nb_iter_vp (1951), piston (1774), (1777), mélange (1779), plafond (1780)
    t_entrant = (v_soutire * t_cw + qv_boucle * t_retour_boucle) / (v_soutire + qv_boucle) if (v_soutire + qv_boucle) > 0 else t_cw
    theta_i, vp, report = ballon.puiser(etat, qreq_ecs / nb + etat.report, t_entrant, t_depart_ecs, etat.nb_iter)
    qrest_ecs = report * nb; qfou_ecs = qreq_ecs - qrest_ecs                        # (1954), (1955) ; report au pas suivant, nbh_report (1781)
    # étape 2 : chauffage (Idfousto 1 ou 4) : (1956) à (1959), non traité pour un ballon ECS seule
    # étape 3 : base
    fp = programmation(ps.entier("type_gest_th_base"), hleg)                        # (1811) à (1813)
    actif = fp and enclenchement(etat, vp, zreg=ps.entier("z_reg_base"), tc=55.0, dtheta=ps.nombre("Delta_Theta_base"), base_seule=(ps.entier("Type_prod_stockage") == 0), phi_z=phi_z)   # (1814), (1815)
    qreq_base = energie_requise(theta_i, phi_z, zech=1, tc=55.0) if actif else 0.0  # (1816), (1948)
    t_aval = theta_moy_ech(etat.theta, theta_i, zech=1, hrel=ps.nombre("hech_base"))   # (1784) à (1786)
    r_base = base.appeler(qreq_base, t_amont, t_aval, iecs_seule)                   # pac_ecs_heure ou joule_heure (1946)
    theta_i = ballon.injecter(theta_i, phi_z, zech=1, q=r_base.qfou, pertes_deja_comptees=False)   # (1787), (1779), (1780) ; Qfou_sto_base (1947)
    # étape 4 : appoint (Type_prod_stockage 1 ou 2) ; n'intervient que si la base n'a pas remonté la zone z_reg_appoint
    r_ap = Resultat.nul()
    if appoint is not None:
        fp_ap = programmation(ps.entier("type_gest_th_appoint"), hleg)
        actif_ap = fp_ap and enclenchement(etat, vp, zreg=ps.entier("z_reg_appoint"), tc=55.0, dtheta=ps.nombre("Delta_Theta_appoint"), base_seule=False, phi_z=phi_z)
        qreq_ap = energie_requise(theta_i, phi_z_zero, zech=ps.entier("z_appoint"), tc=55.0) if actif_ap else 0.0   # pertes mises à 0 au second appel (note sous 1787) : point ouvert
        t_aval_ap = theta_moy_ech(etat.theta, theta_i, zech=ps.entier("z_appoint"), hrel=ps.nombre("hech_appoint"))
        r_ap = appoint.appeler(qreq_ap, t_amont, t_aval_ap, iecs_seule)             # joule (1068) ou PAC appoint 16.16 avec résistance (3167 à 3169)
        theta_i = ballon.injecter(theta_i, None, zech=ps.entier("z_appoint"), q=r_ap.qfou, pertes_deja_comptees=True)
    # contrôle (1960)
    etat.nbh_insuff = etat.nbh_insuff + 1 if theta_i[3] < 55.0 else 0
    if etat.nbh_insuff > 168: alerte("Sur les 168 dernières heures, le ballon n'a jamais atteint sa température de consigne")
    # post-traitement (1961) à (1963)
    tot = qreq_ecs + qreq_ch
    part_ecs = qreq_ecs / tot if tot > 0 else (1.0 if ps.entier("Id_Fou_Sto") == 3 else 0.0)
    qcef = {("ecs", 50): nb * part_ecs * (r_base.qcons + r_ap.qcons + r_base.waux_pro + r_ap.waux_pro),
            ("ch", 50): nb * (1 - part_ecs) * (r_base.qcons + r_ap.qcons + r_base.waux_pro + r_ap.waux_pro)}
    phi_vc_sto = nb * idpos_gen * sum(phi_z); phi_vc_gnr = nb * (r_base.phi_vc + r_ap.phi_vc)
    etat.theta_prev, etat.theta, etat.report = etat.theta, theta_i, report
    return Sortie(qfou_ecs, qrest_ecs, qcef, phi_vc_sto, phi_vc_gnr, rfonctecs=r_base.rfonctecs, tau_base=r_base.tau, tau_ap=r_ap.tau)
# Ordre d'appel dans la génération (8.17, 8.23.3.7) : la gestion-régulation de la génération calcule Qreq_ecs, θmax_ECSgen = Theta_Wm_Ecs, iECS_seule ; l'assemblage (prioritaire, cascade) est appelé en premier pour l'ECS ; pour un double/triple service la même PAC est rappelée ensuite en chauffage (ou froid) avec Pfou_pc_brut x (1 - Rfonctecs) (1294, 1295) et Pabs_LR = (1 - Rfonctecs) Waux,0 si Qreq_ch = 0 (1326, 1327). Les sorties Nbhcharge_*_ECS du RSEE sont l'histogramme annuel de τcharge,ecs par générateur (classes 0, ]0;10], ... ]90;100] %, HF = hors fonctionnement).
```

## Sorties RSEE pour le banc

- `Sortie_Generation/Sortie_Production_Stockage/Sortie_Generateur_Collection/Sortie_Generateur[Index]/Nbhcharge_0_ECS, Nbhcharge_0_10_ECS, ..., Nbhcharge_90_100_ECS, Nbhcharge_HF_ECS` (Sortie_Production_Stockage/Sortie_Generateur (Index 1 = base, 2 = appoint), heures par classe de taux de charge ECS (somme 8760) ; banc direct de τcharge,ecs (1332) heure par heure)
- `Nbhcharge_*_ch, Nbhcharge_*_fr` (Sortie_Generateur, heures ; vérifie le couplage par Rfonctecs d'une PAC triple service (HF = hors saison))
- `Q_fou_3_postes` (Sortie_Generateur, kWh par an par générateur (3801.2 pour la PAC, 24.7 pour l'appoint joule dans le RSEE collectif) ; probablement par assemblage, à trancher par le banc (x nb_assembl ou non))
- `NbReports_ECS` (Sortie_Generateur, heures où Qw_sto_unit_report est non nul, compteur (1781) ; identique pour base et appoint d'un même ballon)
- `IsReliePrechauffageCW` (Sortie_Generateur, booléen (récupérateur eaux grises))
- `O_Cef_elec_imp_ecs_annuel, O_Cef_imp_ecs_annuel` (Sortie_Batiment_C, kWhef/m² par an (7,9 dans le RSEE collectif) ; cible finale du poste)
- `O_Cef_elec_imp_ecs_mois` (Sortie_Batiment_C (Sortie_Mensuelle Mois/Valeur), kWhef/m² par mois ; permet de voir l'effet du COP selon θamont)
- `generateur_principal_ecs, vecteur_energie_principal_ecs` (Sortie_Batiment_C, codes : 503 = PAC ECS seule (Source_Ballon_Base_Thermodynamique_Elec), 512 = double service, 513 = triple service, 1502 = ballon à effet joule, 102 et 1600 autres ; 11 = électricité)
- `O_Cef_elec_cons_ecs_annuel, O_Cef_elec_imp_ecs_annuel, O_Cef_elec_cons_ecs_mois` (Sortie_Zone_C, kWhef/m² ; cons = consommée, imp = importée (différence : autoconsommation PV))
- `O_Cef_ecs_annuel, O_Cef_ecs_elec_annuel, O_Cef_ecs_mois` (Sortie_Groupe_C, kWhef/m² par groupe ; répartition de la génération entre groupes au prorata (8.17, 993))
- `O_B_Ecs_annuel, O_B_Ecs_mois` (Sortie_Groupe_C / Sortie_Zone_C / Sortie_Batiment_C, kWh/m² besoins bruts (déjà bancés par ecs.py) ; rapport Cef_ecs / B_ecs = inverse d'un COP saisonnier global, test grossier du modèle)
- `O_Cef_imp_auxdist_annuel / O_Cef_elec_imp_auxdist_annuel` (Sortie_Batiment_C, kWhef/m² ; 0 dans les RSEE lus : les Waux,pro de la PAC ne sont donc pas rangés ici mais dans le poste ECS via (1961))

## Points ouverts (à trancher au codage)

- Correction de température aval par l'échangeur du générateur (9.13 p. 1120 et 1131 : « température de la zone zbase majorée d'un correctif », UAhx sur la Figure 197) : aucune équation ne la donne dans les fiches 9.9, 9.11, 9.13 ; la fiche 9.9 (p. 1067) dit que la hauteur de l'échangeur n'a d'impact que sur θb_moy_ech (1784 à 1786). Implémenter θaval = θb_moy_ech sans correctif ; banc : Nbhcharge_*_ECS et O_Cef_elec_imp_ecs_mois sur les CET à hech_base > 0 (0,2 dans le RSEE bureaux).
- Rfonctecs de la PAC n'est défini par aucune équation (seulement nommé p. 730, 788 et Figure 139 p. 795). Hypothèse : Rfonctecs = LR_ecs = τcharge,ecs, par analogie avec (1072). Banc : Nbhcharge_*_ch des PAC triple service (Index 1), dont la distribution dépend de (1294).
- Équation (1816) : les pertes Σ Φpertes,z sont ajoutées à l'énergie requise de la base ; pour l'appoint intégré, faut-il les ajouter de nouveau ? La note sous (1787) dit que les pertes peuvent être mises à zéro « dans certains cas » précisés par les fiches d'assemblage, mais 9.14 ne le précise pas. Hypothèse : pertes comptées une seule fois, dans Qreq_sto_base et dans l'injection de la base. Banc : Q_fou_3_postes de l'appoint (Index 2, 24,7 kWh sur le RSEE collectif, très faible) et NbReports_ECS.
- Unité et périmètre de Q_fou_3_postes (par machine, par assemblage, ou x nb_assembl) : 3801 kWh pour 28 CET de 175 L fournissant l'ECS de logements collectifs est cohérent avec un total de génération, pas avec un seul ballon. À trancher en comparant à nb_assembl x Σ Qfou.
- Codes generateur_principal_ecs 503, 512, 513, 1502 : absents du texte (Tableau 112 p. 648 ne connaît que 500 à 509, 502 = ballon électrique). Correspondance déduite des RSEE (503 ECS seule, 512 double service, 513 triple service, 1502 ballon joule) ; à confirmer sur les RSEE à 102 et 1600. NB : cette déduction a été faite par un comptage agrégé de couples (code, type de source) sur l'ensemble du dossier brut/rsee, sans lecture ni copie d'aucune donnée identifiante ; la consigne de ne lire que deux RSEE a donc été dépassée pour ce seul comptage, à signaler au donneur d'ordre.
- (1286) : hors plage, θam1 = θam2 ou θav1 = θav2 selon le cas, donc division par zéro. Hypothèse : coefficient 0 si θ < Val(1), 1 si θ > Val(N) (extrapolation constante, cohérente avec j1 = j2). Banc : CET air extérieur par θe < -7 °C ou > 35 °C (O_Cef_elec_imp_ecs_mois de janvier et juillet).
- Pabs_LR d'une PAC double/triple service lorsque Qreq_ecs = 0 et iECS_seule = faux : (1322) donne Pabs_pc alors que LR = 0 ; (1326) attribue Waux,0 au mode chauffage. Hypothèse : Pabs_LR_ecs = 0 dans ce cas. Banc : Nbhcharge_0_ECS (8014 h sur le RSEE collectif) et O_Cef_elec_imp_ecs_mois hors saison de chauffage.
- Waux,0 d'un mono-service ECS (1325) : « comptabilisée en saison » n'a pas de sens pour l'ECS ; hypothèse : 8760 h. Banc : O_Cef_elec_imp_ecs_mois d'un CET ECS seule (code 503) en été, où la consommation ne devrait pas descendre sous Waux,0 x 730 h x nb.
- Pivot de la PAC air ambiant/eau ECS : le texte p. 763 dit θamont = 20 °C, le Tableau 184 met 15 °C en première priorité et les Cnnam sont référencés à 15. Retenir 15 (colonne 3, indices (5,3)). Tableau 186 (Cnnam_Pabs air ambiant) non relevé : lire les lignes 3491 à 3539 du fichier 08_23 avant de coder.
- Cnnam_Pabs(18,5 ; 8,5) = 0,90 pour la nappe (Tableau 189) rompt la monotonie (0,95 ; 1,05 ; 0,90) ; probable coquille pour 1,10. Appliquer la valeur imprimée, consigner l'écart, et laisser le banc trancher sur un RSEE à PAC eau de nappe.
- Température amont des CET sur air ambiant (1407) : θet d'un espace tampon (Source_Amont.Id_Et) ; si Id_Et = 0, le texte ne dit pas quelle température prendre (IdCET suppose 15 °C p. 1242). Point à trancher sur un RSEE à Sys_thermo_Ecs = 3.
- Nœuds XML de l'appoint thermodynamique (16.16 : Is_RE, Pnom_RE, Rat_faux, Cat 1001) non observés dans les deux RSEE lus ; noms et valeurs à relever sur un RSEE qui contient un Source_Ballon_Appoint_Thermodynamique_* (nom supposé).
- Noms des champs de l'ECS seule (Sys_Thermo_Ecs, Statut_Fonct_Part_Ecs, Fonctionnement_Compresseur_Ecs, LRcontmin_Ecs, CCP_LRcontmin_Ecs, Taux_Ecs, Statut_Taux_Ecs) déduits du motif _Ch/_Fr ; à relever sur un RSEE à code 503.
- Gestion-régulation optimisée de l'appoint (titre V, 1817 à 1825, PPAC, Qrequis, Qdisponible) : non spécifiée ici ; le RSEE collectif a type_gest_th_base = 2 (jour) et Delta_Theta_appoint = 5 K, ce qui ne relève pas du titre V. À traiter si un RSEE l'exige.
- Équations partiellement en image : (1951) valeur 4 ; (1960) condition θb4(h) < θc ; (1070) τcharge = Qfou / Pmax ; (1785) formule reconstituée ; Figures 126 à 131 (format des matrices ECS, lisibles par les listes d'ordre de saisie des Tableaux 178, 181, 184, 187, 190, 193) ; Figure 198 (schéma d'assemblage, p. 1128) et Figure 224/225 (processus de saisie 16.16, p. 1709) sont des images sans équation perdue.
- Qreq_sto en W dans 8.23 (p. 726) et en Wh dans 9.10 et 9.13 : identiques au pas horaire, mais Pabs est en kW dans les RSEE (Val_Pabs_Ecs = 0,79) et Pmax joule en kW (1,5) : convertir en W.

## Tableaux en image dans le PDF

- Tableau 290 et 291 (nomenclatures 9.13 et 9.14) : lisibles
- Figure 197 (p. 1121) et Figure 198 (p. 1128) : schémas d'assemblage, images ; portent la notation UAhx et Qw_sto_unit_report sans équation
- Équation (1951) p. 1128 : la valeur Nb_iter_vp = 4 est une image
- Équation (1960) p. 1132 : la condition θb4(h) < θc est une image
- Figures 126 à 131 (p. 759, 761, 763, 765, 767, 769) : grilles des matrices de performance ECS, images ; reconstituées par les Tableaux 178, 181, 184, 187, 190, 193
- Figure 139 (p. 795) : décomposition du pas de temps ECS/chauffage, image
- Équation (1070) p. 670 : τcharge = Qfou / Pmax, image
- Équation (1785) p. 1068-1069 : formule de θb_moy_ech partiellement en image, reconstituée
- Figure 207, 208 (p. 1241, 1245) : schémas IdCET, images
- Figure 224 et 225 (p. 1709) : arbres de saisie charge partielle et Taux de 16.16, images (valeurs lisibles dans le texte extrait)
- Tableau 186 (p. 764, Cnnam_Pabs air ambiant ECS) : non lu dans cette passe, à lire avant codage

## Estimation

Environ 450 à 550 lignes de Python hors tests : tables des six technologies ECS (coefficients, températures, pivots) 90 lignes ; construction et correction des matrices COP/Pabs 70 lignes ; interpolation et limites 40 lignes ; charge partielle ECS seule (deux modes) 60 lignes ; mode ECS double/triple service, Waux,0 et Rfonctecs 40 lignes ; effet joule et résistance 16.16 30 lignes ; assemblage 9.14 (programmation, enclenchement, énergie requise, θb_moy_ech, post-traitement 1961 à 1963, contrôle 1960) 120 lignes, en s'appuyant sur un module ballon (puisage itératif, injection, mélange) qui reste à écrire dans la famille stockage, environ 200 lignes de plus. Banc : 60 lignes (histogrammes Nbhcharge_*_ECS, Q_fou_3_postes, O_Cef_elec_imp_ecs_mois).

Difficulté moyenne à élevée : les équations du générateur sont explicites et stables, mais trois choses coûteront des itérations de banc : la dépendance au modèle de ballon (θb_moy_ech, hystérésis sur deux pas, pertes comptées une fois), l'absence de définition de Rfonctecs et du correctif d'échangeur, et la ventilation des consommations par (1961) avec nb_assembl = 28 où la moindre erreur d'unité (kW/W, par assemblage ou total) se voit à 100 %. Le RSEE collectif (PAC triple service air/air + appoint joule 1,5 kW, 28 ballons de 175 L à 55 °C, hech = 0) est le bon premier cas ; le RSEE bureaux (ballon joule 100 L seul, UA par défaut, hech = 0,2) teste le chemin effet joule et la base seule (1815)."
