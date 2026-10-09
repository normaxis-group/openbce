# Spécification : Générateurs thermodynamiques électriques (chauffage, refroidissement)

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille : générateurs thermodynamiques à compression électrique (fiche 8.23 C_GEN_THERMODYNAMIQUE_Elec, pages 725 à 798 de l'annexe III) en mode chauffage et en mode refroidissement, avec leurs sources amont (fiche 8.26 C_Gen_Sources amont, pages 889 à 906 ; fiche 8.27 sources amont de type sol, pages 907 à 911).

Couvert :
- les cinq catégories XML : Generateur_Thermodynamique_Elec_NonReversible (Id_FouGen_Mod 1 chauffage ou 2 refroidissement), Generateur_Thermodynamique_Elec_Reversible (Sys_Thermo_Rev, tableau 147 p. 736), et les parts chauffage et refroidissement des Source_Ballon_Base_Thermodynamique_Elec_DoubleService (Sys_Thermo_ds, tableau 149 p. 737) et _TripleService (Sys_Thermo_ts, tableau 150 p. 738) ;
- les 9 technologies de chauffage (Sys_thermo_Ch 1 à 9 : air ext/eau, air ext/air recyclé, air extrait/air neuf, eau de nappe/eau, eau glycolée/eau, eau de nappe/air, eau de boucle/air, sol/eau, sol/sol) et les 7 technologies de refroidissement (Sys_thermo_Fr 1 à 7 : air ext/eau, air ext/air recyclé, air extrait/air neuf, eau ou eau glycolée/eau, eau ou eau de boucle/air, eau de nappe/air, eau de nappe/eau) ;
- le prétraitement des matrices COP/EER et Pabs (statuts certifié, justifié, déclaré, par défaut ; coefficients Cnn par technologie ; pivot et ordre de saisie M_θ_Aval, M_θ_Amont) ;
- le calcul horaire : interpolation bilinéaire sur θamont(h) et θaval(h), puissance pleine charge, limites de fonctionnement Lim_Theta, taux de charge LR, correction de charge partielle (tout ou rien Fonc_compr = 2 ; puissance variable Fonc_compr = 1 avec LRcontmin et CcpLRcontmin), irréversibilités Deq/Dfou0, auxiliaires à charge nulle Waux,0 (Taux), consommation Qcef, énergie fournie Qfou, reste Qrest, rejet à la source amont φrejet ;
- la température amont θamont(h) et les auxiliaires amont Waux,am selon la source : air extérieur, air d'espace tampon, air extrait (avec plafond Pfou_source_amont_maxi), captage sonde, nappe avec ou sans échangeur de barrage, boucle d'eau, tour humide ou sèche, sol (table de correspondance tableau 246).

Hors champ et pourquoi :
- le mode ECS : matrices ECS (8.23.3.4, pages 759 à 770, équations 1257 à 1263, figures 126 à 131, tableaux 178 à 195) et le traitement des assemblages production-stockage ; traité dans la spécification cet.md. Il commence page 759 (ligne 2955 du fichier texte) à l'intitulé « Création des matrices de performance à pleine charge en mode production ECS ». Les règles de couplage ECS/chauffage et ECS/froid d'un double ou triple service (priorité ECS, Rfonct_ecs, iECS_seule, équations 1294, 1295, 1320 à 1327) sont citées ici seulement pour ce qu'elles imposent aux modes chauffage et froid ; Rfonct_ecs(h) et iECS_seule(h) sont des entrées fournies par le calcul ECS.
- les entrées θaval,ch(h), θaval,fr(h), Qreq,ch(h), Qreq,fr(h), les saisons effectives et le report de Qrest vers un appoint ou le pas suivant : ils relèvent de la fiche de gestion-régulation de la génération et de l'assemblage de la génération (8.14, 8.15), pas de cette famille ; ils sont pris comme entrées.
- les générateurs thermodynamiques gaz (8.24), PAC à moteur gaz (8.25), PAC CO2 et Titre V (16.x) ; les émetteurs et distributions.
- le dégivrage : aucune occurrence du mot dans les trois fiches ; le texte ne contient pas de modèle de dégivrage, l'effet du givre est porté implicitement par les points de matrice à -7 °C et 2 °C (Cnnam(2, 7) = 0,80 inférieur à ce que donnerait une interpolation entre -7 et 7). Rien à coder à ce titre.

## Entrées (RSEE)

- `Entree_Projet/Batiment/Generation/Generateur_Collection/Generateur_Thermodynamique_Elec_NonReversible` / `Index, Name, Rdim` : Rdim (nombre de machines identiques, p. 729) ; Ent, texte, Ent ; valeurs vues : Rdim = 1 (bureaux double flux, PAC air ext/air recyclé)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Id_Source_Amont` : lien vers C_Gen_Source_Amont (θamont, Waux,am) ; Ent (Index de la Source_Amont de la Generation) ; valeurs vues : 1
- `Generateur_Thermodynamique_Elec_NonReversible` / `Id_FouGen_Mod` : Id_Fougen_Mod (p. 726) ; Ent 1 ou 2 ; valeurs vues : 1 (chauffage seul)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Idpriorite_Ch, Idpriorite_Fr, Idpriorite_Ecs` : ordre de priorité du générateur dans l'assemblage (fiche 8.14, hors fiche 8.23) ; Ent ; valeurs vues : 0, 0, 0 (mono) ; 1, 1, 1 (triple service)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Sys_Thermo_Ch, Sys_Thermo_Fr, Sys_Thermo_Ecs` : Sys_thermo_Ch / Fr / Ecs (p. 726-727, tableau 146) ; Ent 0 à 9 ; valeurs vues : 2, 0, 0
- `Generateur_Thermodynamique_Elec_NonReversible` / `Id_Groupe` : groupe desservi en détente directe (air recyclé) ; hors fiche 8.23 ; Ent ; valeurs vues : 0
- `Generateur_Thermodynamique_Elec_NonReversible` / `Statut_Donnee` : Statut_données_PC_ch (1 : valeurs certifiées ou justifiées ; 2 : aucune) p. 727 ; Ent 1 ou 2 ; valeurs vues : 1
- `Generateur_Thermodynamique_Elec_NonReversible` / `Theta_Aval_<techno> et Theta_Amont_<techno> (Air_Eau_Ch, Air_Exterieur_Air_Recycle, Air_Extrait_Air_Neuf, Eau_De_Nappe_Eau, Eau_Glycolee_Eau, Eau_De_Nappe_Air, Eau_De_Boucle_Air, Sol_Eau_Ch, Sol_Sol_Ch, puis suffixes _Fr : Air_Eau_Fr, Air_Exterieur_Air_Recycle_Fr, Eau_De_Nappe_Air_Fr, Eau_De_Nappe_Eau_Fr, Air_Extrait_Air_Neuf_Fr, Eau_Eau_Fr, Eau_Air_Fr ; et _Ecs)` : M_θ_Aval_Ch / M_θ_Amont_Ch (ordre de saisie, tableaux 151, 154, 157, 160, 163, 166, 169, 172, 175 ; froid : 196, 199, 202, 205, 208, 211, 214) ; Ent 0 à 7 ; un seul couple non nul, celui de la technologie retenue ; valeurs vues : Theta_Aval_Air_Exterieur_Air_Recycle = 1, Theta_Amont_Air_Exterieur_Air_Recycle = 1 ; tous les autres 0
- `Generateur_Thermodynamique_Elec_NonReversible` / `Performance` : {Performance(i,j)}ch (COP avant prétraitement, p. 727) ; matrice texte : lignes séparées par « ; », valeurs par espace ; ligne i = température aval, colonne j = température amont ; 5 x 5 en chauffage ; valeurs vues : 0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 0 0 ;0 0 0 3.54 0 ;0 0 0 0 0 (pivot (4,4) = 20 °C / 7 °C de l'air ext/air recyclé)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Pabs` : {Pabs(i,j)}ch (kW, p. 727) ; matrice texte, kW ; valeurs vues : ... ;0 0 0 3.05 0 ;...
- `Generateur_Thermodynamique_Elec_NonReversible` / `COR` : {COR(i,j)}ch (1 certifié, 2 justifié, p. 727) ; matrice texte d'entiers 0, 1, 2 ; valeurs vues : ... ;0 0 0 1 0 ;... (pivot certifié)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Statut_Val_Pivot, Val_Cop, Val_Pabs` : Statut_val_pivot_ch (1 déclarée, 2 par défaut), Val_COP_ch, Val_Pabs_ch (p. 727) ; Ent, réel, réel (kW) ; valeurs vues : 0, 0, 0 quand Statut_Donnee = 1
- `Generateur_Thermodynamique_Elec_NonReversible` / `Lim_Theta, Theta_Max_Av, Theta_Min_Am, Theta_Max_Am, Theta_Min_Av` : Lim_θ_ch / Lim_θ_fr, θmax_av_ch, θmin_am_ch, θmax_am_fr, θmin_av_fr (p. 728) ; Ent 0 à 2 ; réels °C ; valeurs vues : 2, 32, -15, -15, 32 (les deux dernières valeurs, limites du mode froid, sont inutilisées en chauffage seul)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Valeur_Declaree_Defaut` : sans équivalent nommé dans la fiche ; vraisemblablement Statut_fonct_part (0 par défaut, 1 déclarée) : point ouvert ; Ent ; valeurs vues : 1
- `Generateur_Thermodynamique_Elec_NonReversible` / `Fonctionnement_Compresseur` : Fonc_compr (p. 728) ; Ent 1 ou 2 ; valeurs vues : 1 (puissance variable)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Statut_Fonctionnement_Continu, LRcontmin, CCP_LRcontmin` : Statut_fonct_continu (0 certifié, 1 justifié, 2 par défaut), LRcontmin, CcpLRcontmin (p. 728, 786) ; Ent 0 à 2 ; réels ; valeurs vues : 2, 0, 0 (par défaut : LRcontmin 0,4 et Ccp 1)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Statut_Taux, Taux` : Statut_Taux, Taux (p. 729, codage effectif p. 785 : 0 certifié, 1 justifié, 2 par défaut) ; Ent 0 à 2 ; réel ; valeurs vues : 2, 0 (par défaut)
- `Generateur_Thermodynamique_Elec_NonReversible` / `Typo_Emetteur` : Typo_emetteur_ch (Dfou0, tableau 217 p. 786) ; Ent 1 à 4 ; valeurs vues : 3 (VCV, systèmes à eau par défaut)
- `Generation/Generateur_Collection/Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Index, Name, Rdim, Id_Source_Amont, Idpriorite_Ch, Idpriorite_Ecs, Idpriorite_Fr` : Rdim ; lien source amont ; priorités d'assemblage ; Ent, texte, Ent, Ent, Ent, Ent, Ent ; valeurs vues : Rdim 1 ; Id_Source_Amont 1 ; priorités 1, 1, 1 (PAC triple service air ext/air avec ECS, logement collectif)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Sys_Thermo_ts` : Sys_Thermo_ts (tableau 150 p. 738) ; Ent 1 à 5 ; valeurs vues : 5 (air ext/air avec production ECS : Sys_thermo_Ch = 2, Ecs = 1, Fr = 2)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Donnee_Ch ; Theta_Aval_Air_Eau_Ch, Theta_Amont_Air_Eau_Ch, Theta_Aval_Air_Extrait_Air_Recycle_Ch, Theta_Amont_Air_Extrait_Air_Recycle_Ch, Theta_Aval_Eau_De_Nappe_Eau_Ch, Theta_Amont_Eau_De_Nappe_Eau_Ch, Theta_Aval_Eau_Glycolee_Eau_Ch, Theta_Amont_Eau_Glycolee_Eau_Ch, Theta_Amont_Sol_Eau_Ch, Theta_Aval_Sol_Eau_Ch` : Statut_données_PC_ch ; M_θ_Aval_Ch, M_θ_Amont_Ch du mode chauffage ; Ent ; valeurs vues : Statut_Donnee_Ch 1 ; Theta_Aval_Air_Extrait_Air_Recycle_Ch 1, Theta_Amont_Air_Extrait_Air_Recycle_Ch 2 (le champ nommé « Air_Extrait_Air_Recycle » porte ici la techno air ext/air recyclé) ; plusieurs couples non nuls à 1 (valeurs résiduelles de saisie)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Performance_Ch, Pabs_Ch, COR_Ch` : {Performance(i,j)}ch, {Pabs(i,j)}ch, {COR(i,j)}ch ; matrices 5 x 5 texte ; valeurs vues : Performance_Ch ligne 4 : 0 2.6 0 4.15 0 (aval 20 °C ; amont -7 °C et 7 °C) ; Pabs_Ch ligne 4 : 0 2.12 0 1.42 0 ; COR_Ch ligne 4 : 0 1 0 1 0
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Val_Pivot_Ch, Val_Cop_Ch, Val_Pabs_Ch` : Statut_val_pivot_ch, Val_COP_ch, Val_Pabs_ch ; Ent, réel, réel ; valeurs vues : 0, 4.15, 1.42 (recopie du pivot bien que Statut_Donnee_Ch = 1)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Lim_Theta_Ch, Theta_Max_Av_Ch, Theta_Min_Am_Ch` : Lim_θ_ch, θmax_av_ch, θmin_am_ch ; Ent ; °C ; °C ; valeurs vues : 0, 20, -15
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Donnee_Fr ; Theta_Aval_Air_Eau_Fr, Theta_Amont_Air_Eau_Fr, Theta_Aval_Air_Exterieur_Air_Recycle_Fr, Theta_Amont_Air_Exterieur_Air_Recycle_Fr, Theta_Aval_Eau_De_Nappe_Air_Fr, Theta_Amont_Eau_De_Nappe_Air_Fr, Theta_Aval_Eau_De_Nappe_Eau_Fr, Theta_Amont_Eau_De_Nappe_Eau_Fr, Theta_Aval_Eau_Air_Fr, Theta_Amont_Eau_Air_Fr, Theta_Aval_Air_Extrait_Air_Neuf_Fr, Theta_Amont_Air_Extrait_Air_Neuf_Fr, Theta_Aval_Eau_Eau_Fr, Theta_Amont_Eau_Eau_Fr` : Statut_données_PC_fr ; M_θ_Aval_Fr, M_θ_Amont_Fr ; Ent ; valeurs vues : Statut_Donnee_Fr 1 ; Air_Exterieur_Air_Recycle_Fr 1 / 1
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Performance_Fr, Pabs_Fr, COR_Fr` : {Performance(i,j)}fr (EER), {Pabs(i,j)}fr, {COR(i,j)}fr ; matrices 4 lignes (aval 22, 27, 32, 37 °C) x 5 colonnes (amont 5, 15, 25, 35, 45 °C) pour l'air ext/air recyclé ; valeurs vues : Performance_Fr ligne 2 : 0 0 0 3.8 0 (pivot (2,4) = 27 °C / 35 °C) ; Pabs_Fr ligne 2 : 0 0 0 1.32 0 ; COR_Fr ligne 2 : 0 0 0 1 0
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Val_Pivot_Fr, Val_Cop_Fr, Val_Pabs_Fr, Lim_Theta_Fr, Theta_Max_Av_Fr, Theta_Min_Am_Fr` : Statut_val_pivot_fr, Val_EER, Val_Pabs_fr, Lim_θ_fr, θmax_am_fr, θmin_av_fr ; Ent, réel, réel, Ent, °C, °C ; valeurs vues : 0, 3.8, 1.32, 0, 0, 0 (noter : pas de champ Theta_Max_Am_Fr / Theta_Min_Av_Fr dans ce nœud, les noms sont ceux du chauffage)
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Donnee_Ecs, Theta_*_Ecs, Performance_Ecs, Pabs_Ecs, COR_Ecs, Statut_Val_Pivot_Ecs, Val_Cop_Ecs, Val_Pabs_Ecs, Lim_Theta_Ecs, Theta_Max_Av_Ecs, Theta_Min_Am_Ecs` : mode ECS : hors champ (spécifications ecs.md et cet.md) ; idem mode ECS (matrice 7 lignes) ; valeurs vues : 1 ; pivot 3.5 / 0.79 ; Lim 0 ; 25 ; -5
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Fonct_Part_Ch, Fonctionnement_Compresseur_Ch, Statut_Fonctionnement_Continu_Ch, LRcontmin_Ch, CCP_LRcontmin_Ch, Statut_Taux_Ch, Taux_Ch, Typo_Emetteur_Ch` : Statut_fonct_part, Fonc_compr, Statut_fonct_continu (0 certifié), LRcontmin, CcpLRcontmin, Statut_Taux (0 certifié), Taux, Typo_emetteur_ch ; Ent, Ent, Ent, réel, réel, Ent, réel, Ent ; valeurs vues : 1, 1, 0, 0.27, 1.33, 0, 0.0035, 3
- `Source_Ballon_Base_Thermodynamique_Elec_TripleService` / `Statut_Fonct_Part_Fr, Fonctionnement_Compresseur_Fr, Statut_Fonctionnement_Continu_Fr, LRcontmin_Fr, CCP_LRcontmin_Fr, Typo_Emetteur_Fr` : idem mode froid ; Ent, Ent, Ent, réel, réel, Ent ; valeurs vues : 1, 1, 0, 0.34, 1.66, 3 (pas de Statut_Taux_Fr ni Taux_Fr : Waux,0 commun, pris sur le mode chauffage, p. 785)
- `Generation/Source_Amont_Collection/Source_Amont` / `Index, Name, Id_Fl_Amont, Source_Amont_Eau, Source_Amont_Air, Id_Et, Id_SF_Extraction, Tair_Lim` : idfluide-amont, idamont-eau-type, idamont-air-type, espace tampon pour θet(h), système d'extraction pour Tair_extrait et Qmair_extrait, Tair_lim (p. 891-893) ; Ent, texte, Ent 1 eau 2 air 3 sol, Ent (idamont-eau-type 1 à 5), Ent (idamont-air-type 1 à 3), Ent, Ent, °C ; valeurs vues : Id_Fl_Amont 2, Source_Amont_Eau 0, Source_Amont_Air 1 (air extérieur), Id_Et 0, Id_SF_Extraction 0, Tair_Lim 0
- `Source_Amont` / `Idgestion_Captage, Idgestion_Pompe_Captage, Type_Echangeur, Type_Generateur_Fr` : idgest_captage (1 permanent, 2 sur demande), idgest_pompe_captage_cont_var (1 tout ou rien, 2 vitesse variable), type_echangeur (1 contre-courant, 2 parallèle, 3 croisé), idtour (1 humide, 2 sèche) ; Ent ; valeurs vues : 0, 0, 0, 0
- `Source_Amont` / `Pvent_Gaine, Delta_Theta_Evap_Ch, Delta_Theta_Cond_Fr` : Pvent_gaine, θEvap_CH, θCond_FR ; W, K, K ; valeurs vues : 0, 0, 0 (défaut 5 K pour les deux écarts, p. 900)
- `Source_Amont` / `Ppompes_Tour, Pvent_Tour, Delta_Theta_Tour, Theta_Es_Tour_Consigne, Qv_nom_tour` : Ppompes_tour, Pvent_tour, θtour, θes_tour_consigne (p. 892) ; W, W, K, °C, m3/h ; valeurs vues : 0
- `Source_Amont` / `Ppompes_Cap, Ppompes_Nappe, Ppompes_Inter, Ppompes_Boucle_Eau` : Ppompes_captage (sonde, nappe, boucle selon le type), Ppompes_inter ; W ; valeurs vues : 0
- `Source_Amont` / `Idmois_Mini, Theta_Min_Source, Theta_Max_Source, Theta_Min_Boucle, Theta_Max_Boucle, Theta_Max_Rech_BE, Theta_Min_Fr_BE` : idmois_mini, θmin_source, θmax_source, θmin_boucle, θmax_boucle (p. 892-893) ; les deux derniers (boucle d'eau, recharge) ne sont pas dans la fiche 8.26 ; Ent 1 à 12, °C ; valeurs vues : 0
- `Source_Amont` / `Rb, L, Qv_nappe_nom, Qv_inter_nom, Rho_inter, UA, Cpe_inter` : Rb, L, Qv_nappe_nom, Qv_inter_nom, ρinter, UA, Cpeinter (p. 893) ; K.m/W, m, m3/h, m3/h, kg/m3, W/K, J/(kg.K) ; valeurs vues : 0
- `Source_Amont` / `Idmois_Mini_sol, Theta_min_sol, Theta_max_sol` : idmois_mini_sol, θmin_sol, θmax_sol (fiche 8.27 p. 908) ; Ent, °C, °C ; valeurs vues : 0
- `Generation (champs directs)` / `Type_Priorite, Idraccord_Gnr, Idraccord_Reseau_Gen, Pos_Gen, Id_Bat, Id_Et, Type_Gestion_Chaud_Gen, Theta_Wm_Ch, Type_Gestion_Froid_Gen, Theta_Wm_Fr, Theta_Wm_Ecs` : gestion-régulation de la génération (fiche 8.15) : donne θaval,ch(h), θaval,fr(h) et Qreq ; entrées de la fiche 8.23, hors champ ici ; Ent ; °C ; valeurs vues : 2, 1, 0, 0, 0, 0, 2, 70, 2, 7, 50 (identiques dans les deux RSEE)
- `Entrées horaires venant d'autres modules` / `θamont(h) (8.26/8.27), θaval,ch(h), θaval,fr(h), Qreq,ch(h), Qreq,fr(h), Rpuis_dispo(h) = 1 - Rfonct_ecs(h), iECS_seule(h), Pfou_source_amont_maxi(h), hleg(h), θext(h), ωext(h), θet(h), Tair_extrait(h), Qmair_extrait(h), idMois(j)` : tableau 144 p. 726 et tableau 244 p. 891 ; séries horaires ; valeurs vues : calculées, pas dans le RSEE

## Paramètres conventionnels

- Correction des valeurs selon statut : certifiée x 1,0 ; justifiée x 0,9 ; déclarée x 0,8 puis plafond Val_util_max ; par défaut 0,8 x Val_util_max (pivot) = 1,0 / 0,9 / 0,8 / 0,8 x Val_util_max (p. 733-734, 740 (1239))
- Val_util_max chauffage par technologie : air ext/eau 3,5 ; air ext/air recyclé 3,5 ; air extrait/air neuf 2,5 ; eau de nappe/eau 4,7 ; eau glycolée/eau 3,7 ; eau de nappe/air 3,5 ; eau de boucle/air 4 ; sol/eau 3,8 ; sol/sol 3,8 = voir liste (p. 739, 743, 745, 747, 749, 751, 753, 755, 757)
- Val_util_max refroidissement par technologie : air ext/eau 2,7 ; air ext/air recyclé 2,7 ; air extrait/air neuf 2,7 ; eau ou eau glycolée/eau 3,7 ; eau ou eau de boucle/air 2,7 ; eau de nappe/air 3,7 ; eau de nappe/eau 3,7 = voir liste (p. 771, 773, 775, 777, 779, 781, 783)
- Températures de référence et pivot, chauffage. Air ext/eau : aval 23,5 / 32,5 / 42,5 / 51 / 60 (moyenne départ-retour), amont -15 / -7 / 2 / 7 / 20, pivot (2,4) = 32,5 / 7. Air ext/air recyclé : aval 5 / 10 / 15 / 20 / 25, amont -15 / -7 / 2 / 7 / 20, pivot (4,4) = 20 / 7. Air extrait/air neuf : aval (air neuf) -15 / -7 / 2 / 7 / 20, amont (air extrait) 5 / 10 / 15 / 20 / 25, pivot (4,4) = 7 / 20. Eau de nappe/eau : aval 23,5 / 32,5 / 42,5 / 51 / 60, amont 3,5 / 8,5 / 13,5 / 18,5, pivot (2,2) = 32,5 / 8,5. Eau glycolée/eau : aval idem, amont -6,5 / -1,5 / 3,5 / 8,5 / 13,5, pivot (2,2) = 32,5 / -1,5. Eau de nappe/air : aval 5 / 10 / 15 / 20 / 25, amont 3,5 / 8,5 / 13,5 / 18,5, pivot aval 20 / amont 8,5 (texte : « (2,4) », lire (4,2)). Eau de boucle/air : aval 5 / 10 / 15 / 20 / 25, amont 8,5 / 13,5 / 18,5 / 23,5 / 28,5, pivot (4,3) = 20 / 18,5. Sol/eau : aval 23,5 / 32,5 / 42,5 / 51 / 60, amont (bain d'essai) -4 / 1,5 / 4 / 6,5, pivot (2,3) = 32,5 / 4 (texte p. 755 écrit « θaval = 20 », coquille). Sol/sol : aval 35 seul, amont -4 / 1,5 / 4 / 6,5, pivot (1,3) = voir liste (p. 739, 743, 745, 747, 749, 751, 753, 755, 757 (figures 117 à 125))
- Températures de référence et pivot, refroidissement. Air ext/eau : aval 4 / 9,5 / 15 / 20,5 / 26, amont 5 / 15 / 25 / 35 / 45, pivot (2,4) = 9,5 / 35. Air ext/air recyclé : aval 22 / 27 / 32 / 37, amont 5 / 15 / 25 / 35 / 45, pivot (2,4) = 27 / 35. Air extrait/air neuf : aval (air neuf) 5 / 15 / 25 / 35 / 45, amont (air extrait) 22 / 27 / 32 / 37, pivot (4,2) = 35 / 27. Eau ou eau glycolée/eau : aval 4 / 9,5 / 15 / 20,5 / 26, amont 2,5 / 12,5 / 22,5 / 32,5 / 42,5, pivot (2,4) = 9,5 / 32,5. Eau ou eau de boucle/air : aval 22 / 27 / 32 / 37, amont 2,5 / 12,5 / 22,5 / 32,5 / 42,5, pivot (2,4) = 27 / 32,5. Eau de nappe/air : aval 22 / 27 / 32 / 37, amont 7,5 / 12,5 / 17,5 / 22,5, pivot (2,2) = 27 / 12,5. Eau de nappe/eau : aval 4 / 9,5 / 15 / 20,5 / 26, amont 7,5 / 12,5 / 17,5 / 22,5, pivot (2,2) = 9,5 / 12,5 = voir liste (p. 771 à 784 (figures 132 à 138))
- Ordre de saisie M_θ_Aval_Ch (eau) : 1 : 32,5 ; 2 : + 42,5 ; 3 : + 51 ; 4 : + 23,5 ; 5 : + 60. M_θ_Aval_Ch (air recyclé) : 1 : 20 ; 2 : + 15 ; 3 : + 25 ; 4 : + 10 ; 5 : + 5. M_θ_Aval_Ch (air neuf) : 1 : 7 ; 2 : + -7 ; 3 : + 2 ; 4 : + 20 ; 5 : + -15. M_θ_Amont_Ch (air ext) : 1 : 7 ; 2 : + -7 ; 3 : + 2 ; 4 : + 20 ; 5 : + -15. M_θ_Amont_Ch (air extrait) : 1 : 20 ; 2 : + 15 ; 3 : + 25 ; 4 : + 10 ; 5 et 6 : + 5. M_θ_Amont_Ch (nappe) : 1 : 8,5 ; 2 : + 3,5 ; 3 : + 13,5 ; 4 : + 18,5. M_θ_Amont_Ch (glycolée) : 1 : -1,5 ; 2 : + 3,5 ; 3 : + 8,5 ; 4 : + -6,5 ; 5 : + 13,5. M_θ_Amont_Ch (boucle) : 1 : 18,5 ; 2 : + 13,5 ; 3 : + 23,5 ; 4 : + 8,5 ; 5 : + 28,5. M_θ_Amont_Ch (sol) : 1 : 4 ; 2 : + 1,5 ; 3 : + -4 ; 4 : + 6,5 = voir liste (p. 739, 743, 745, 747, 749, 751, 753, 755, 757 (tableaux 151 à 175))
- Ordre de saisie froid. M_θ_Aval_Fr (eau) : 1 : 9,5 ; 2 : + 20,5 ; 3 : + 15 ; 4 : + 26 ; 5 : + 4. M_θ_Aval_Fr (air) : 1 : 27 ; 2 : + 22 ; 3 : + 32 ; 4 : + 37. M_θ_Aval_Fr (air neuf) : 1 : 35 ; 2 : + 25 ; 3 : + 15 ; 4 : + 5 ; 5 : + 45. M_θ_Amont_Fr (air ext) : 1 : 35 ; 2 : + 25 ; 3 : + 15 ; 4 : + 5 ; 5 : + 45. M_θ_Amont_Fr (air extrait) : 1 : 27 ; 2 : + 22 ; 3 : + 32 ; 4 : + 37. M_θ_Amont_Fr (eau) : 1 : 32,5 ; 2 : + 22,5 ; 3 : + 12,5 ; 4 : + 2,5 ; 5 : + 42,5. M_θ_Amont_Fr (nappe) : 1 : 12,5 ; 2 : + 17,5 ; 3 : + 7,5 ; 4 : + 22,5 = voir liste (p. 771 à 784 (tableaux 196 à 214))
- Cnn COP chauffage, aval (eau) : Cnnav(42,5 ; 32,5) 0,8 ; (51 ; 42,5) 0,8 ; (23,5 ; 32,5) 1,10 ; (60 ; 51) 0,8. Aval (air recyclé) : (15 ; 20) 1,10 ; (25 ; 20) 0,9 ; (10 ; 20) 1,20 ; (5 ; 20) 1,3. Aval (air neuf, air extrait) : (-7 ; 7) 1,20 ; (2 ; 7) 1,1 ; (20 ; 7) 0,80 ; (-15 ; 7) 1,30 = voir liste (p. 740, 743-744, 746, 748, 750, 752, 754, 756 (tableaux 152, 155, 158, 161, 164, 167, 170, 173))
- Cnn COP chauffage, amont. Air ext (Pnom à 7 °C < 100 kW) : Cnnam(-7 ; 7) 0,50 ; (2 ; 7) 0,80 ; (20 ; 7) 1,25 ; (-15 ; -7) 0,80 ; si Pnom > 100 kW : (-7 ; 7) 0,60, le reste identique. Air extrait : (15 ; 20) 0,90 ; (25 ; 20) 1,10 ; (10 ; 20) 0,80 ; (5 ; 20) 0,70. Nappe : (3,5 ; 8,5) 0,9 ; (13,5 ; 8,5) 1,1 ; (18,5 ; 8,5) 1,2. Glycolée : (3,5 ; -1,5) 1,10 ; (8,5 ; -1,5) 1,20 ; (-6,5 ; -1,5) 0,90 ; (13,5 ; -1,5) 1,30. Boucle : (13,5 ; 18,5) 0,9 ; (23,5 ; 18,5) 1,1 ; (8,5 ; 18,5) 0,8 ; (28,5 ; 18,5) 1,2. Sol : (1,5 ; 4) 0,95 ; (-4 ; 4) 0,8 ; (6,5 ; 4) 1,07 = voir liste (p. 740, 744, 746, 748, 750, 752, 754, 756, 757)
- Cnn Pabs chauffage (indépendants de la puissance). Aval eau : (42,5 ; 32,5) 0,9 ; (51 ; 42,5) 0,915 ; (23,5 ; 32,5) 1,09 ; (60 ; 51) 0,91. Aval air recyclé : (15 ; 20) 1,05 ; (25 ; 20) 0,95 ; (10 ; 20) 1,10 ; (5 ; 20) 1,15. Aval air neuf : (-7 ; 7) 1,14 ; (2 ; 7) 1,05 ; (20 ; 7) 0,87 ; (-15 ; 7) 1,22. Amont air ext : (-7 ; 7) 0,86 ; (2 ; 7) 0,95 ; (20 ; 7) 1,13 ; (-15 ; -7) 0,92. Amont air extrait : (15 ; 20) 0,95 ; (25 ; 20) 1,05 ; (10 ; 20) 0,90 ; (5 ; 20) 0,85. Amont nappe : (3,5 ; 8,5) 0,95 ; (13,5 ; 8,5) 1,05 ; (18,5 ; 8,5) 1,10. Amont glycolée : (3,5 ; -1,5) 1,05 ; (8,5 ; -1,5) 1,10 ; (-6,5 ; -1,5) 0,95 ; (13,5 ; -1,5) 1,15. Amont boucle : (13,5 ; 18,5) 0,95 ; (23,5 ; 18,5) 1,05 ; (8,5 ; 18,5) 0,9 ; (28,5 ; 18,5) 1,10. Amont sol : tous 1 = voir liste (p. 742, 744, 746, 748, 750, 752, 754, 756, 758 (tableaux 153, 156, 159, 162, 165, 168, 171, 174, 177))
- Cnn EER refroidissement. Aval eau : (20,5 ; 9,5) 1,15 ; (15 ; 9,5) 1,075 ; (26 ; 9,5) 1,225 ; (4 ; 9,5) 0,9. Aval air : (22 ; 27) 0,9 ; (32 ; 27) 1,075 ; (37 ; 27) 1,15. Aval air neuf : (25 ; 35) 0,9 ; (45 ; 35) 1,2 ; (15 ; 35) 0,8 ; (5 ; 35) 0,7. Amont air ext : (25 ; 35) 1,2 ; (15 ; 35) 1,4 ; (5 ; 35) 1,6 ; (45 ; 35) 0,8. Amont air extrait : (32 ; 27) 0,9 ; (22 ; 27) 1,075 ; (37 ; 27) 0,8. Amont eau : (22,5 ; 32,5) 1,2 ; (12,5 ; 32,5) 1,4 ; (2,5 ; 32,5) 1,6 ; (42,5 ; 32,5) 0,8. Amont nappe : (17,5 ; 12,5) 0,90 ; (7,5 ; 12,5) 1,10 ; (22,5 ; 12,5) 0,80 = voir liste (p. 772, 774, 776, 778, 780, 782, 784 (tableaux 197, 200, 203, 206, 209, 212, 215))
- Cnn Pabs refroidissement. Aval eau : (20,5 ; 9,5) 1,11 ; (15 ; 9,5) 1,055 ; (26 ; 9,5) 1,165 ; (4 ; 9,5) 0,945. Aval air : (22 ; 27) 0,95 ; (32 ; 27) 1,05 ; (37 ; 27) 1,1. Aval air neuf : (25 ; 35) 0,9 ; (45 ; 35) 1,2 ; (15 ; 35) 0,8 ; (5 ; 35) 0,7. Amont air ext : (25 ; 35) 1,1 ; (15 ; 35) 1,2 ; (5 ; 35) 1,3 ; (45 ; 35) 0,9. Amont air extrait : (32 ; 27) 0,95 ; (22 ; 27) 1,05 ; (37 ; 27) 0,9. Amont eau : (22,5 ; 32,5) 1,10 ; (12,5 ; 32,5) 1,20 ; (2,5 ; 32,5) 1,30 ; (42,5 ; 32,5) 0,90. Amont nappe : (17,5 ; 12,5) 0,95 ; (7,5 ; 12,5) 1,05 ; (22,5 ; 12,5) 1,10 = voir liste (p. 772, 774, 776, 778, 780, 782, 784-785 (tableaux 198, 201, 204, 207, 210, 213, 216))
- Taux (auxiliaires à charge nulle) par défaut : chauffage ou ECS 0,02 ; refroidissement 0,01 ; justifié x 1,1 ; certifié sans correction. Réversible, double et triple service : Waux,0 unique, calculé sur le Pabs pivot du mode chauffage avec le Taux du chauffage = 0,02 / 0,01 / x 1,1 (p. 785 (1278 à 1280))
- Deq (durée équivalente des irréversibilités) = 0,5 min (p. 729, 785)
- Dfou0 selon Typo_emetteur : 1 forte inertie 32 min ; 2 moyenne 19 min ; 3 légère (VCV, défaut eau) 6 min ; 4 systèmes à air 2 min ; mode ECS 26 min = 32 / 19 / 6 / 2 (ECS 26) (p. 786 (tableau 217))
- LRcontmin et CcpLRcontmin par défaut (Statut_fonct_continu = 2) ; justifié : LRcontmin + 0,05 et Ccp x 0,9 ; certifié sans correction = LRcontmin 0,4 ; CcpLRcontmin 1 (p. 786 (1281, 1282))
- Contrôle de cohérence : erreur si LRcontmin x 0,3 < CcpLRcontmin x Taux = 0,3 (p. 787 (1283))
- Ratbasc,fr-ECS (délai de basculement ECS vers froid, triple service) = 0,25 h (p. 732, 791 (1295))
- Idengen électricité = 50 (p. 730)
- Statut par défaut de Pabs : variation de 1 % par degré d'écart θaval - θamont (principe énoncé, remplacé en pratique par les Cnn Pabs) = 1 %/K (p. 735)
- θEvap_CH et θCond_FR par défaut (écart aux bornes de l'échangeur amont, sources eau) = 5 K (p. 900, 902)
- Débit minimal des pompes de captage à vitesse variable = max(0,3 ; τcharge) (p. 898, 904 (1414, 1446, 1448))
- Tdépart_amont au premier pas d'une saison (nappe avec échangeur) ; rejets nuls = 12 °C (p. 899)
- Constantes 8.26 : Cv 1830 J/(kg.K) ; Cpe 4180 ; ρeau 1000 kg/m3 ; Ca 1006 ; Hfg 2,5 x 10^6 J/kg = voir liste (p. 895)
- Correspondance sol (fiche 8.27) : θf -5 / 0 / 5 / 10 °C donne θamont (bain d'essai) -4 / 1,5 / 4 / 6,5 °C, interpolation linéaire = tableau 246 (p. 911)
- Normes de référence (tableau 145) : NF EN 14511-2 chauffage et froid, NF EN 15879-1 sol/eau, NF EN 16147 ECS = informatif (p. 734)

## Équations

- (1239, p. 739-740) Si Statut_données_PC = 1 : COPutil(i,j) = Performance(i,j) si COR(i,j) = 1 ; = 0,9 x Performance(i,j) si COR(i,j) = 2. Si Statut_données_PC = 2 : si Statut_val_pivot = 1 : COPutil(pivot) = MIN(0,8 x Val_COP ; Val_util_max) ; si Statut_val_pivot = 2 : COPutil(pivot) = 0,8 x Val_util_max ; COR, Performance, Val_COP, Val_util_max ; pivot (2,4) pour air ext/eau, indices du pivot selon technologie ; contrôle préalable : toute valeur non nulle hors des coordonnées M_θ_Aval x M_θ_Amont est une erreur ; toute valeur nulle dans ces coordonnées est une erreur (p. 739). Pabs : valeurs saisies prises sans correction (statut 1), pivot Val_Pabs seul (statut 2), p. 735. Même procédure pour EER_util (p. 771)
- (1240, p. 740) Air ext/eau, colonne pivot j = 4 : si COPutil(1,4) = 0 : = COPutil(2,4) x Cnnav(23,5 ; 32,5) ; si COPutil(3,4) = 0 : = COPutil(2,4) x Cnnav(42,5 ; 32,5) ; si COPutil(4,4) = 0 : = COPutil(3,4) x Cnnav(51 ; 42,5) ; si COPutil(5,4) = 0 : = COPutil(4,4) x Cnnav(60 ; 51) ; Cnnav_COP tableau 152 ; on ne remplace jamais une valeur saisie non nulle ; chaîne séquentielle
- (1241, p. 740-742) Air ext/eau, pour chaque ligne i : si COPutil(i,2) = 0 : = COPutil(i,4) x Cnnam(-7 ; 7) ; si COPutil(i,3) = 0 : = COPutil(i,4) x Cnnam(2 ; 7) ; si COPutil(i,5) = 0 : = COPutil(i,4) x Cnnam(20 ; 7) ; si COPutil(i,1) = 0 : = COPutil(i,2) x Cnnam(-15 ; -7) ; Cnnam_COP tableau 152 (0,50 ou 0,60 selon Pnom à 7 °C < ou > 100 kW) ; Pabs : même procédure avec tableau 153
- (1242, p. 743-744) Air ext/air recyclé, colonne pivot j = 4 : COPutil(1,4) = COPutil(4,4) x Cnnav(5 ; 20) ; (2,4) = (4,4) x Cnnav(10 ; 20) ; (3,4) = (4,4) x Cnnav(15 ; 20) ; (5,4) = (4,4) x Cnnav(25 ; 20) (chacun si nul) ; tableau 155 ; pivot (4,4)
- (1243, p. 744) Air ext/air recyclé, lignes : (i,2) = (i,4) x Cnnam(-7 ; 7) ; (i,3) = (i,4) x Cnnam(2 ; 7) ; (i,5) = (i,4) x Cnnam(20 ; 7) ; (i,1) = (i,2) x Cnnam(-15 ; -7) ; tableau 155 ; Pabs tableau 156 ; si nul
- (1244, p. 746) Air extrait/air neuf, colonne pivot j = 4 : (1,4) = (4,4) x Cnnav(-15 ; 7) ; (2,4) = (4,4) x Cnnav(-7 ; 7) ; (3,4) = (4,4) x Cnnav(2 ; 7) ; (5,4) = (4,4) x Cnnav(20 ; 7) ; tableau 158 ; lignes = θaval air neuf -15, -7, 2, 7, 20 ; colonnes = θamont air extrait 5, 10, 15, 20, 25 ; pivot (4,4) = aval 7 / amont 20
- (1245, p. 746) Air extrait/air neuf, lignes : (i,1) = (i,4) x Cnnam(5 ; 20) ; (i,2) = (i,4) x Cnnam(10 ; 20) ; (i,3) = (i,4) x Cnnam(15 ; 20) ; (i,5) = (i,4) x Cnnam(25 ; 20) ; tableau 158 ; Pabs tableau 159 ; si nul
- (1246, p. 748) Eau de nappe/eau, colonne pivot j = 2 : (1,2) = (2,2) x Cnnav(23,5 ; 32,5) ; (3,2) = (2,2) x Cnnav(42,5 ; 32,5) ; (4,2) = (3,2) x Cnnav(51 ; 42,5) ; (5,2) = (4,2) x Cnnav(60 ; 51) ; tableau 161 ; pivot (2,2) ; 4 colonnes amont
- (1247, p. 748) Eau de nappe/eau, lignes : (i,1) = (i,2) x Cnnam(3,5 ; 8,5) ; (i,3) = (i,2) x Cnnam(13,5 ; 8,5) ; (i,4) = (i,2) x Cnnam(18,5 ; 8,5) ; tableau 161 ; Pabs tableau 162 ; si nul
- (1248, p. 750) Eau glycolée/eau, colonne pivot j = 2 : identique à 1246 (chaîne 23,5 / 42,5 / 51 / 60 depuis (2,2)) ; tableau 164 ; pivot (2,2) ; 5 colonnes amont
- (1249, p. 750) Eau glycolée/eau, lignes : (i,1) = (i,2) x Cnnam(-6,5 ; -1,5) ; (i,3) = (i,2) x Cnnam(3,5 ; -1,5) ; (i,4) = (i,2) x Cnnam(8,5 ; -1,5) ; (i,5) = (i,2) x Cnnam(13,5 ; -1,5) ; tableau 164 ; Pabs tableau 165 ; si nul
- (1250, p. 752) Eau de nappe/air, colonne pivot (texte garbled : « (1,2) = (2,4) x Cnnav(5 ; 20) ; (2,2) = (2,4) x Cnnav(10 ; 20) ; (2,3) = (2,4) x Cnnav(15 ; 20) ; (5,2) = (2,4) x Cnnav(25 ; 20) »). Lecture retenue : colonne j = 2 (amont 8,5), pivot (4,2) : (1,2) = (4,2) x Cnnav(5 ; 20) ; (2,2) = (4,2) x Cnnav(10 ; 20) ; (3,2) = (4,2) x Cnnav(15 ; 20) ; (5,2) = (4,2) x Cnnav(25 ; 20) ; tableau 167 ; point ouvert sur les indices ; structure identique à 1252
- (1251, p. 752) Eau de nappe/air, lignes : (i,1) = (i,2) x Cnnam(3,5 ; 8,5) ; (i,3) = (i,2) x Cnnam(13,5 ; 8,5) ; (i,4) = (i,2) x Cnnam(18,5 ; 8,5) ; tableau 167 ; Pabs tableau 168 ; si nul
- (1252, p. 754) Eau de boucle/air, colonne pivot j = 3 : (1,3) = (4,3) x Cnnav(5 ; 20) ; (2,3) = (4,3) x Cnnav(10 ; 20) ; (3,3) = (4,3) x Cnnav(15 ; 20) ; (5,3) = (4,3) x Cnnav(25 ; 20) ; tableau 170 ; pivot (4,3)
- (1253, p. 754) Eau de boucle/air, lignes : (i,1) = (i,3) x Cnnam(8,5 ; 18,5) ; (i,2) = (i,3) x Cnnam(13,5 ; 18,5) ; (i,4) = (i,3) x Cnnam(23,5 ; 18,5) ; (i,5) = (i,3) x Cnnam(28,5 ; 18,5) ; tableau 170 ; Pabs tableau 171 ; si nul
- (1254, p. 756) Sol/eau, colonne pivot j = 3 : (1,3) = (2,3) x Cnnav(23,5 ; 32,5) ; (3,3) = (2,3) x Cnnav(42,5 ; 32,5) ; (4,3) = (3,3) x Cnnav(51 ; 42,5) ; (5,3) = (4,3) x Cnnav(60 ; 51) ; tableau 173 ; pivot (2,3) ; amont = température de bain d'essai (fiche 8.27)
- (1255, p. 756) Sol/eau, lignes : (i,1) = (i,3) x Cnnam(-4 ; 4) ; (i,2) = (i,3) x Cnnam(1,5 ; 4) ; (i,4) = (i,3) x Cnnam(6,5 ; 4) ; tableau 173 ; Pabs tableau 174 (tous à 1) ; si nul
- (1256, p. 757-758) Sol/sol, une seule ligne aval 35 °C : (1,1) = (1,3) x Cnnam(-4 ; 4) ; (1,2) = (1,3) x Cnnam(1,5 ; 4) ; (1,4) = (1,3) x Cnnam(6,5 ; 4) ; tableau 176 ; Pabs tableau 177 (tous à 1) ; pivot (1,3) ; pas de propagation aval
- (1257 à 1263, p. 759-770) matrices ECS (air ext/eau, air extrait/eau, air ambiant/eau, nappe/eau, sol/eau, glycolée/eau) ; hors champ (spécifications ecs.md et cet.md) ; section 8.23.3.4
- (1264, p. 772) Froid air ext/eau, colonne pivot j = 4 : (1,4) = (2,4) x Cnnav_EER(4 ; 9,5) ; (3,4) = (2,4) x Cnnav(15 ; 9,5) ; (4,4) = (2,4) x Cnnav(20,5 ; 9,5) ; (5,4) = (2,4) x Cnnav(26 ; 9,5) ; tableau 197 ; toutes depuis le pivot (pas de chaîne) ; pivot (2,4)
- (1265, p. 772) Froid air ext/eau, lignes : (i,2) = (i,4) x Cnnam(15 ; 35) ; (i,3) = (i,4) x Cnnam(25 ; 35) ; (i,5) = (i,4) x Cnnam(45 ; 35) ; (i,1) = (i,4) x Cnnam(5 ; 35) ; tableau 197 ; Pabs tableau 198 ; si nul
- (1266, p. 774) Froid air ext/air recyclé, colonne pivot j = 4 (texte garbled « (1,4), (4,3), (4,4) »). Lecture retenue : (1,4) = (2,4) x Cnnav(22 ; 27) ; (3,4) = (2,4) x Cnnav(32 ; 27) ; (4,4) = (2,4) x Cnnav(37 ; 27) ; tableau 200 ; 4 lignes aval ; pivot (2,4) ; point ouvert indices
- (1267, p. 774) Froid air ext/air recyclé, lignes : (i,2) = (i,4) x Cnnam(15 ; 35) ; (i,3) = (i,4) x Cnnam(25 ; 35) ; (i,5) = (i,4) x Cnnam(45 ; 35) ; (i,1) = (i,4) x Cnnam(5 ; 35) ; tableau 200 ; Pabs tableau 201 ; si nul
- (1268, p. 776) Froid air extrait/air neuf, colonne pivot (texte écrit avec (2,4) alors que le pivot annoncé est (4,2)). Lecture retenue : colonne j = 2 (amont 27) : (1,2) = (4,2) x Cnnav(5 ; 35) ; (2,2) = (4,2) x Cnnav(15 ; 35) ; (3,2) = (4,2) x Cnnav(25 ; 35) ; (5,2) = (4,2) x Cnnav(45 ; 35) ; tableau 203 ; lignes aval air neuf 5, 15, 25, 35, 45 ; colonnes amont air extrait 22, 27, 32, 37 ; point ouvert indices
- (1269, p. 776) Froid air extrait/air neuf, lignes : (i,1) = (i,2) x Cnnam(22 ; 27) ; (i,3) = (i,2) x Cnnam(32 ; 27) ; (i,4) = (i,2) x Cnnam(37 ; 27) ; tableau 203 ; Pabs tableau 204 ; si nul
- (1270, p. 778) Froid eau ou glycolée/eau, colonne pivot j = 4 : (1,4) = (2,4) x Cnnav(4 ; 9,5) ; (3,4) = (2,4) x Cnnav(15 ; 9,5) ; (4,4) = (2,4) x Cnnav(20,5 ; 9,5) ; (5,4) = (2,4) x Cnnav(26 ; 9,5) ; tableau 206 ; pivot (2,4)
- (1271, p. 778) Froid eau/eau, lignes : (i,1) = (i,4) x Cnnam(2,5 ; 32,5) ; (i,2) = (i,4) x Cnnam(12,5 ; 32,5) ; (i,3) = (i,4) x Cnnam(22,5 ; 32,5) ; (i,5) = (i,4) x Cnnam(42,5 ; 32,5) ; tableau 206 ; Pabs tableau 207 (le tableau nomme à tort Cnnav les coefficients amont) ; si nul
- (1272, p. 780) Froid eau ou boucle/air, colonne pivot j = 4 : (1,4) = (2,4) x Cnnav(22 ; 27) ; (3,4) = (2,4) x Cnnav(32 ; 27) ; (4,4) = (2,4) x Cnnav(37 ; 27) (même garbling que 1266) ; tableau 209 ; pivot (2,4)
- (1273, p. 780) Froid eau/air, lignes : (i,1) = (i,4) x Cnnam(2,5 ; 32,5) ; (i,2) = (i,4) x Cnnam(12,5 ; 32,5) ; (i,3) = (i,4) x Cnnam(22,5 ; 32,5) ; (i,5) = (i,4) x Cnnam(42,5 ; 32,5) ; tableau 209 ; Pabs tableau 210 ; si nul
- (1274, p. 782) Froid eau de nappe/air, colonne pivot j = 2 : (1,2) = (2,2) x Cnnav(22 ; 27) ; (3,2) = (2,2) x Cnnav(32 ; 27) ; (4,2) = (2,2) x Cnnav(37 ; 27) (texte : (2,3), (2,4), lire (3,2), (4,2)) ; tableau 212 ; pivot (2,2)
- (1275, p. 782) Froid eau de nappe/air, lignes : (i,1) = (i,2) x Cnnam(7,5 ; 12,5) ; (i,3) = (i,2) x Cnnam(17,5 ; 12,5) ; (i,4) = (i,2) x Cnnam(22,5 ; 12,5) ; tableau 212 ; Pabs tableau 213 ; si nul
- (1276, p. 784) Froid eau de nappe/eau, colonne pivot j = 2 : (1,2) = (2,2) x Cnnav(4 ; 9,5) ; (3,2) = (2,2) x Cnnav(15 ; 9,5) ; (4,2) = (2,2) x Cnnav(20,5 ; 9,5) ; (5,2) = (2,2) x Cnnav(26 ; 9,5) (texte écrit (i,4) et (2,4), le pivot annoncé est (2,2)) ; tableau 215 ; pivot (2,2)
- (1277, p. 784-785) Froid eau de nappe/eau, lignes : (i,1) = (i,2) x Cnnam(7,5 ; 12,5) ; (i,3) = (i,2) x Cnnam(17,5 ; 12,5) ; (i,4) = (i,2) x Cnnam(22,5 ; 12,5) ; tableau 215 ; Pabs tableau 216 ; si nul
- (1278, p. 785) Waux,0 = Taux x Pabs(ipivot, jpivot) ; Pabs pivot en W (saisi en kW : x 1000) ; Taux corrigé selon Statut_taux (0 : tel quel ; 1 : x 1,1 ; 2 : défaut) ; constante du calcul ; réversible, double et triple service : Pabs pivot du mode chauffage
- (1279, p. 785) Taux = 0,02 ;  ; Statut_taux = 2, mode chauffage ou ECS
- (1280, p. 785) Taux = 0,01 ;  ; Statut_taux = 2, mode refroidissement (mono-service froid)
- (1281, p. 786) LRcontmin = 0,4 ;  ; Statut_fonct_continu = 2 ; justifié : LRcontmin saisi + 0,05
- (1282, p. 786) CcpLRcontmin = 1 ;  ; Statut_fonct_continu = 2 ; justifié : Ccp saisi x 0,9
- (1283, p. 787) Erreur si LRcontmin x 0,3 < CcpLRcontmin x Taux ;  ; contrôle de saisie ; en double/triple service LRcontmin, Ccp, Deq, Dfou0 ne sont pas définis pour l'ECS
- (1284, p. 788) Encadrement amont : si θamont(h) < Valθam(1) : j1 = j2 = 1, θam1 = θamont(h), θam2 = Valθam(1). Si θamont(h) > Valθam(Nam) : j1 = j2 = Nam, θam1 = Valθam(Nam), θam2 = θamont(h). Sinon premier j de 2 à Nam tel que θamont(h) <= Valθam(j) : j1 = j - 1, j2 = j, θam1 = Valθam(j1), θam2 = Valθam(j2) ; Valθam liste croissante des températures amont de la technologie ; hors plage : j1 = j2 donc Cθam vaut 0 ou 1 et la valeur de bord est reconduite (pas d'extrapolation)
- (1285, p. 788-789) Encadrement aval, même algorithme avec Valθav, i1, i2, θav1, θav2 ; Valθav liste croissante des températures aval ; 
- (1286, p. 789) Cθam(h) = (θamont(h) - θam1) / (θam2 - θam1) ; Cθav(h) = (θaval(h) - θav1) / (θav2 - θav1) ;  ; dénominateur nul hors plage : prendre Cθ = 0 (valeur de bord)
- (1287, p. 789) Pabs_pc(h) = (1 - Cθam)(1 - Cθav) Pabs(i1,j1) + Cθam (1 - Cθav) Pabs(i1,j2) + Cθav (1 - Cθam) Pabs(i2,j1) + Cθam Cθav Pabs(i2,j2) ; W (matrice en kW x 1000) ; 
- (1288, p. 789) COP_pc(h) = même interpolation bilinéaire sur COP_util ;  ; mode chauffage (ou ECS)
- (1289, p. 789) EER_pc(h) = même interpolation bilinéaire sur EER_util ;  ; mode refroidissement
- (1290, p. 790) Pfou_pc_brut(h) = Pabs_pc(h) x COP_pc(h) ; W ; chauffage
- (1291, p. 790) Pfou_pc_brut(h) = Pabs_pc(h) x EER_pc(h) ; W ; refroidissement
- (1292, p. 790) Pfou_pc_brut(h) = MIN(Pabs_pc x COP_pc ; Pfou_source_amont_maxi(h)) ; Pfou_source_amont_maxi de 8.26 (1456) ; Sys_Thermo_Ch = 3 (air extrait/air neuf) ou Sys_Thermo_Ecs = 2
- (1293, p. 790) Pfou_pc_brut(h) = MIN(Pabs_pc x EER_pc ; Pfou_source_amont_maxi(h)) ; (1458) ; Sys_Thermo_Fr = 3
- (règle réversible (sans numéro), p. 790-791) Si Qreq,fr(h) > 0 : Pfou_pc_brut,ch(h) = 0 (le froid est prioritaire, pas de chauffage et froid au même pas) ;  ; Generateur_Thermodynamique_Elec_Reversible et triple service
- (1294, p. 790) Pfou_pc_brut,ch(h) = Pabs_pc(h) x COP_pc(h) x (1 - Rat_Fonct_ECS(h)) ; Rat_Fonct_ECS = Rfonct_ecs du calcul ECS ; double et triple service, mode chauffage (ECS prioritaire traitée avant)
- (1295, p. 791) Pfou_pc_brut,fr(h) = Pabs_pc(h) x EER_pc(h) x (1 - Rat_Fonct_ECS(h) - Ratbasc,ECS/FR) (le texte écrit COP_pc ; en froid c'est l'EER) ; Ratbasc = 0,25 ; triple service, mode froid, pas de temps avec ECS puis froid ; borner à 0
- (1296, p. 791) Qreq_act(h) = Qreq(h) / Rdim ; Wh par machine ; 
- (1297, p. 791) Chauffage : si Lim_θ = 0 : Pfou_pc = Pfou_pc_brut, Qrest_act = MAX(0 ; Qreq_act - Pfou_pc). Sinon si Lim_θ = 1 et (θamont < θmin_am ou θaval > θmax_av) : Qrest_act = Qreq_act, Pfou_pc = 0. Sinon si Lim_θ = 2 et (θamont < θmin_am et θaval > θmax_av) : Qrest_act = Qreq_act, Pfou_pc = 0. Dans les autres cas (limite non atteinte) : comme Lim_θ = 0 ; Theta_Min_Am, Theta_Max_Av ; le cas « limite déclarée mais non atteinte » n'est pas écrit : déduction, appliquer la branche Lim_θ = 0
- (1298, p. 792) Refroidissement : idem avec (θamont > θmax_am ou θaval < θmin_av) pour Lim_θ = 1, et (et) pour Lim_θ = 2 ; Theta_Max_Am, Theta_Min_Av ; 
- (1299, p. 792) Pfou_LR(h) = MIN(Qreq_act(h) ; Pfou_pc(h)) ; W (pas horaire : Wh = W) ; 
- (1300, p. 792) LR(h) = Pfou_LR(h) / Pfou_pc(h) ; LR = 0 si Pfou_pc = 0 ;  ; 
- (1301, p. 793) Pcomp_pc(h) = Pabs_pc(h) - Waux,0 ;  ; Fonc_compr = 2 (tout ou rien)
- (1302, p. 793) Pcomp_LR(h) = Pcomp_pc(h) x LR(h) ;  ; Fonc_compr = 2
- (1303, p. 793) Pcompma_LR(h) = Pcomp_pc(h) x Deq x LR(h) x (1 - LR(h)) / Dfou0 ; Deq 0,5 min ; Dfou0 tableau 217 (min) ; Fonc_compr = 2
- (1304, p. 793) Pabs_LR(h) = Pcomp_LR(h) + Pcompma_LR(h) + Waux,0 ;  ; Fonc_compr = 2 ; LR > 0
- (1305, p. 793) COP_LR(h) = Pfou_LR(h) / Pabs_LR(h) (EER_LR en froid) ;  ; Fonc_compr = 2
- (1306, p. 793) Pcomp_pc(h) = Pabs_pc(h) - Waux,0 ;  ; Fonc_compr = 1 (puissance variable)
- (1307, p. 793) COP_pc_net(h) = Pfou_pc_brut(h) / Pcomp_pc(h) ;  ; Fonc_compr = 1
- (1308, p. 793) CcpLRcontmin_net(h) = LRcontmin x Pcomp_pc(h) x CcpLRcontmin / (LRcontmin x Pabs_pc(h) - CcpLRcontmin x Waux,0) ;  ; Fonc_compr = 1 ; le contrôle 1283 garantit un dénominateur positif
- (1309, p. 793) COP_LR_net(h) = COP_pc_net(h) x (1 + (CcpLRcontmin_net - 1) x (1 - LR(h)) / (1 - LRcontmin)) ;  ; LRcontmin <= LR(h) <= 1
- (1310, p. 793) Pcomp_LR(h) = Pfou_LR(h) / COP_LR_net(h) ;  ; LR >= LRcontmin
- (1311, p. 794) Pabs_LR(h) = Pcomp_LR(h) + Waux,0 ;  ; LR >= LRcontmin (pas d'irréversibilités en continu)
- (1312, p. 794) COP_LR(h) = Pfou_LR(h) / Pabs_LR(h) ;  ; LR >= LRcontmin
- (1313, p. 794) Pfou_LRcontmin(h) = Pfou_pc_brut(h) x LRcontmin ;  ; 0 < LR(h) < LRcontmin
- (1314, p. 794) Pcomp_LRcontmin(h) = Pfou_LRcontmin(h) / COP_LRcontmin_net(h), avec COP_LRcontmin_net = COP_pc_net x CcpLRcontmin_net (valeur de 1309 à LR = LRcontmin) ;  ; LR < LRcontmin
- (1315, p. 794) Pcomp_LR(h) = Pcomp_LRcontmin(h) x (1 - (LRcontmin - LR(h)) / LRcontmin) = Pcomp_LRcontmin x LR / LRcontmin ;  ; LR < LRcontmin
- (1316, p. 794) LRcycl(h) = LR(h) / LRcontmin ;  ; LR < LRcontmin
- (1317, p. 794) Pcompma_LR(h) = Pcomp_LRcontmin(h) x Deq x LRcycl(h) x (1 - LRcycl(h)) / Dfou0 ;  ; LR < LRcontmin
- (1318, p. 794) Pabs_LR(h) = Pcomp_LR(h) + Pcompma_LR(h) + Waux,0 ;  ; LR < LRcontmin
- (1319, p. 794) COP_LR(h) = Pfou_LR(h) / Pabs_LR(h) (EER_LR en froid) ;  ; LR < LRcontmin
- (1320 à 1324, p. 795) Mode ECS d'un double ou triple service : Pfou_LR = MIN(Qreq_act ; Pfou_pc) ; LR = Pfou_LR / Pfou_pc ; Pabs_LR = Pabs_pc si iECS_seule = faux, = Pabs_pc + (1 - LR) x Waux,0 si vrai ; COP_LR = Pfou_LR / Pabs_LR ; hors champ (ECS), cité pour la cohérence de Waux,0 ; double et triple service
- (1325, p. 795-796) Pabs_LR(h) = Waux,0 quand la demande du mode est nulle (LR = 0) ;  ; mono-service : comptée seulement en saison de chauffage (mono chauffage) ou de refroidissement (mono froid). Réversible : comptée pour le chauffage en saison de chauffage ou mixte, pour le froid en saison de refroidissement, une seule fois
- (1326, p. 796) Pabs_LR,ch(h) = (1 - Rat_Fonct_ECS(h)) x Waux,0 ;  ; double service, saison de chauffage, Qreq,ecs > 0 et Qreq,ch = 0 ; hors saison de chauffage (iECS_seule vrai) Waux,0 est porté par l'ECS (1323)
- (1327, p. 796) Pabs_LR,ch ou fr(h) = (1 - Rat_Fonct_ECS(h)) x Waux,0 ;  ; triple service : chauffage en saison de chauffage (Qreq,ecs > 0, Qreq,ch = 0) ; refroidissement en saison de refroidissement (Qreq,ecs > 0, Qreq,fr = 0) ; Waux,0 compté une seule fois par pas
- (1328, p. 797) Qcef_ch(id_engen = 50)(h) = Pabs_LR(h) x Rdim ; Wh, vecteur de 6 énergies, électricité seule ; par mode
- (1329, p. 797) ηeff,ch(h) = COP_LR(h) (EER_LR en froid) ;  ; 
- (1330, p. 797) Qfou_ch(h) = Pfou_LR(h) x Rdim ; Wh ; 
- (1331, p. 797) Qrest_ch(h) = Qrest_act(h) x Rdim ; Wh, reporté à l'appoint ou au pas suivant par la gestion de la génération ; 
- (1332, p. 797) τcharge,ch(h) = LR(h) ; transmis à C_Gen_Source_Amont ; 
- (1333, p. 797) φrejet,ch(h) = MIN(0 ; Pcomp_LR + Pcompma_LR - Pfou_LR) x Rdim ; Wh, négatif (prélèvement à la source) ; chauffage
- (1334, p. 797) φrejet,ecs(h) = MIN(0 ; Pcomp_LR + Pcompma_LR - Pfou_LR) x Rdim ;  ; ECS (hors champ)
- (1335, p. 797) φrejet,fr(h) = (Pcomp_LR + Pcompma_LR + Pfou_LR) x Rdim ; Wh, positif ; refroidissement
- (1336, p. 797) Qfou(h) = Qfou_ch + Qfou_ecs + Qfou_fr ;  ; 
- (1337, p. 797) Qcons(h) = somme sur id_engen de (Qcef_ch + Qcef_ecs + Qcef_fr) ;  ; 
- (1338, p. 797) Waux,pro(h) = Waux,0 x Rdim ; sortie informative ; 
- (1339, p. 798) φrejet(h) = φrejet,ch + φrejet,ecs + φrejet,fr ; transmis à la source amont pour le pas suivant ; 
- (1403, p. 896) RatPngen_gnr = Pngen_gnr / somme des Pngen_gnr des générateurs raccordés à la source amont ; Pngen = puissance nominale du générateur ; début de simulation
- (1404, p. 896) RatPhirejet_gnr = φrejet_gnr(h-1) / φrejet(h-1) ;  ; si φrejet(h-1) différent de 0
- (1405, p. 896) φrejet(h-1) = somme des φrejet_gnr(h-1) ;  ; 
- (1406, p. 896) θamont(h) = θext(h) ;  ; idamont-air-type = 1 (air extérieur)
- (1407, p. 896) θamont(h) = θet(h) ; température de l'espace tampon Id_Et ; idamont-air-type = 2
- (1408, p. 896) θamont(h) = Tair_extrait(h) ; air repris après ventilateur d'extraction ; idamont-air-type = 3
- (1409, p. 897) θb(j) = A + B sin(2π idmois(j)/12 + φ) ;  ; captage sonde, nappe (idamont-eau-type 1, 4, 5)
- (1410, p. 897) A = (θmin_source + θmax_source)/2 ; B = (θmax_source - θmin_source)/2 ; φ = π (3/2 - idmois_mini/6) ;  ; θmin = θmax pour une source constante
- (1411, p. 897) θf(h) = θb(j) + φrejet(h-1) x Rb / L ; φrejet en W, Rb en K.m/W, L en m ; sonde (type 1)
- (1412, p. 898) Qm_nappe_reel = Qv_nappe_nom x ρeau / 3600 ; Qm_inter_reel = Qv_inter_nom x ρinter / 3600 ; kg/s ; nappe avec échangeur (type 4), idgest_captage = 1
- (1413, p. 898) si τcharge = 0 : débits nuls ; sinon si idgest_pompe = 1 : débits nominaux (1412) ;  ; type 4, idgest_captage = 2
- (1414, p. 898) débits nominaux x MAX(0,3 ; τcharge) ;  ; type 4, idgest_captage = 2, idgest_pompe = 2
- (1415, p. 898) si un débit est nul : Tdépart_amont = Tdépart_amont,prev ; état conservé ; type 4
- (1416, p. 898) Cnappe = Qm_nappe_reel x Cpe ; Cinter = Qm_inter_reel x Cpe_inter ; W/K ; type 4
- (1417, p. 898) C = MIN(Cnappe, Cinter) / MAX(Cnappe, Cinter) ;  ; 
- (1418, p. 898) NUT = UA / MIN(Cnappe, Cinter) ;  ; 
- (1419, p. 899) ε = NUT / (NUT + 1) ;  ; type_echangeur = 1 et C = 1
- (1420, p. 899) ε = (1 - exp(-NUT (1 - C))) / (1 - C exp(-NUT (1 - C))) ;  ; type_echangeur = 1, C différent de 1
- (1421, p. 899) ε = (1 - exp(-NUT (1 + C))) / (1 + C) ;  ; type_echangeur = 2
- (1422, p. 899) ε = 1 / (1/(1 - exp(-NUT)) + C/(1 - exp(-NUT C)) - 1/NUT) ;  ; type_echangeur = 3
- (1423, p. 899) Tretour_amont = Tdépart_amont(h-1) + ε (θb(j) - Tdépart_amont(h-1)) x MIN(Cnappe, Cinter) / Cinter ;  ; type 4
- (1424, p. 899) θf(h) = Tretour_amont ;  ; type 4
- (1425, p. 899) Tdépart_amont = Tretour_amont + φrejet(h-1) / (Qm_inter_reel x Cpe_inter) ; état pour le pas suivant ; 12 °C et rejets nuls au premier pas d'une saison ; type 4
- (1426, p. 900) Tretour_amont = θb(j) ;  ; nappe sans échangeur (type 5)
- (1427, p. 900) θf(h) = Tretour_amont ;  ; type 5
- (1428, p. 900) θamont(h) = θf(h) + Δθcond/2, avec Δθcond = -θEvap_CH si φrejet(h-1) < 0, = θCond_FR si φrejet(h-1) > 0 (5 K par défaut) ; 0 si rejet nul (déduction) ;  ; types 1, 4, 5
- (1429 à 1432, p. 901) Tour humide : ωsat = 10^-3 exp(18,8161 - 4110,34/(θ'as + 235)) ; hsat = Ca θ'as + ωsat (Hfg + Cv θ'as) ; relation implicite (1430) résolue par itération sur ωsat ; hext = Ca θext + ωext (Hfg + Cv θext) ; θ'as = (ωsat Hfg - hext) / (Ce (ωsat - ωext) - Ca - Cv ωsat) ; Ce = Cpe ; ω en kg/kg ; idtour = 1
- (1433 / 1434, p. 901) θes_tour_cont = θ'as + Δθtour ; θes_tour = MAX(θes_tour_cont ; θes_tour_consigne) ;  ; tour humide
- (1435 / 1436, p. 902) θes_tour_cont = θext + Δθtour ; θes_tour = MAX(θes_tour_cont ; θes_tour_consigne) ;  ; tour sèche (idtour = 2)
- (1437, p. 902) θamont(h) = θes_tour + Δθcond_FR/2 (même convention de signe que 1428) ;  ; tour (type 2) ; froid seulement
- (1438 / 1439, p. 902) Boucle d'eau : θbe(j) = A + B sin(2π idmois/12 + φ) avec A, B, φ sur θmin_boucle, θmax_boucle, idmois_mini ;  ; type 3
- (1440, p. 902) θamont(h) = θbe(j) + Δθcond/2 ;  ; type 3
- (1441, p. 903) θamont_gnr(h) = θamont(h) pour tous les générateurs raccordés ;  ; 
- (1442, p. 903) τcharge = somme des τcharge_gnr x RatPngen_gnr ;  ; 
- (1443, p. 903, 911) Waux,am = 0 ;  ; source air non gainée (Pvent_gaine = 0) ; sol (1466)
- (1444, p. 903) Waux,am = Pvent_gaine x τcharge ; Wh ; source air gainée
- (1445, p. 903) Wpompes_captage = Ppompes_captage ;  ; types 1, 3, 4, 5, idgest_captage = 1 (permanent en saison)
- (1446, p. 903-904) si τcharge = 0 : 0 ; sinon idgest_pompe = 1 : Ppompes_captage ; idgest_pompe = 2 : Ppompes_captage x MAX(τcharge ; 0,3) ;  ; idgest_captage = 2
- (1447 / 1448, p. 904) Wpompes_inter : mêmes règles avec Ppompes_inter ;  ; type 4 (circuit intermédiaire)
- (1449, p. 904) Waux,am = Wpompes_captage + Wpompes_inter ; pas de test de saison : le composant n'est appelé qu'en saison ; types 1, 3, 4, 5
- (1450 / 1451 / 1452, p. 905) Wpompes_tour = Ppompes_tour x τcharge ; Wvent_tour = Pvent_tour x τcharge ; Waux,am = somme ;  ; tour (type 2)
- (1453, p. 905) Waux,am_gnr = Waux,am x RatPhirejet_gnr si φrejet(h-1) différent de 0, sinon Waux,am x RatPngen_gnr ; répartition entre générateurs ; 
- (1454, p. 906) Qmair_extrait_act = Qmair_extrait(h) / Rdim ; kg/s ; air extrait
- (1455, p. 906) Pech_source_amont_maxi = Qmair_extrait_act x Cpa x MAX(0 ; θamont(h) - Tair_lim) ; Cpa = Ca 1006 ; Sys_Thermo_Ch = 3, idfougen = 1 (idem ECS Sys_Thermo_Ecs = 2)
- (1456, p. 906) Pfou_source_amont_maxi = Pech_source_amont_maxi x Pfou_pc_brut / (Pfou_pc_brut - Pabs_pc) ;  ; chauffage sur air extrait
- (1457, p. 906) Pech_source_amont_maxi = Qmair_extrait_act x Cpa x MAX(0 ; Tair_lim - θamont(h)) ;  ; Sys_Thermo_Fr = 3
- (1458, p. 906) Pfou_source_amont_maxi = Pech_source_amont_maxi x Pfou_pc_brut / (Pfou_pc_brut + Pabs_pc) ;  ; froid sur air extrait
- (1459 à 1461, p. 910) Sol : mêmes ratios que 1403 à 1405 ;  ; fiche 8.27
- (1462 / 1463, p. 910) θb(j) = A + B sin(2π idmois/12 + φ) sur θmin_sol, θmax_sol, idmois_mini_sol ;  ; sol/eau et sol/sol
- (1464, p. 911) θf(h) = θb(j) + φrejet(h-1) x Rb / L ;  ; 
- (tableau 246 (sans numéro), p. 911) θamont(h) = interpolation linéaire de θf(h) sur les couples (-5 ; -4), (0 ; 1,5), (5 ; 4), (10 ; 6,5) ;  ; hors plage : point ouvert (bord ou prolongement)
- (1465, p. 911) θamont_gnr(h) = θamont(h) ;  ; 
- (1466, p. 911) Waux,am = 0 ;  ; sol
- (1467, p. 911) répartition identique à 1453 ;  ; 

## Algorithme

```
# Module proposé : openbce/thermodynamique.py (PAC) + openbce/source_amont.py, appelés par la future gestion de la génération (8.14/8.15).

TECHNOS_CH = {  # Sys_thermo_Ch -> (Valθav, Valθam, (i_piv, j_piv), Val_util_max, cnnav_cop, cnnam_cop, cnnav_pabs, cnnam_pabs, id_fluide_aval, id_fluide_amont)
    1: ((23.5, 32.5, 42.5, 51, 60), (-15, -7, 2, 7, 20), (2, 4), 3.5, ...),   # chaînes de propagation codées comme listes d'arêtes (cible, source, coef)
    ...  # 9 technologies, tableaux 152 à 177 ; TECHNOS_FR idem, 7 technologies, tableaux 197 à 216
}
# Lecture RSEE : Sys_Thermo_Rev / _ds / _ts -> (Sys_Ch, Sys_Fr) par tableaux 147, 149, 150. Matrice Performance « a b c ; d e f » :
# ligne i = aval, colonne j = amont, dans l'ordre croissant des températures (vérifié sur le pivot (4,4) = 3,54 air ext/air recyclé
# et (2,4) = 3,8 en froid). Les Cnn à 100 kW : Pnom = 1000 x Pabs(pivot) x COP(pivot).

def pretraiter(mode, techno, statut_pc, perf, pabs, cor, statut_pivot, val_cop, val_pabs):
    T = TECHNOS[mode][techno]; cop = zeros(Nav, Nam); pab = zeros(Nav, Nam)
    verifier_coordonnees(perf, pabs, cor, M_aval, M_amont)                        # erreurs p. 739
    if statut_pc == 1:                                                              # (1239)
        cop = where(cor == 1, perf, where(cor == 2, 0.9 * perf, 0)); pab = pabs
    else:
        cop[piv] = min(0.8 * val_cop, T.vmax) if statut_pivot == 1 else 0.8 * T.vmax
        pab[piv] = val_pabs                                                         # p. 735
    for (cible, source, c) in T.chaine_colonne_cop: cop[cible] = cop[cible] or cop[source] * c   # (1240, 1242, ...)
    for i in range(Nav):
        for (jc, js, c) in T.chaine_lignes_cop: cop[i, jc] = cop[i, jc] or cop[i, js] * c        # (1241, 1243, ...)
    idem pour pab avec les Cnn Pabs
    return Matrices(cop, pab * 1000.0)                                              # W

def parametres_charge_partielle(noeud, mode):
    taux = {0: t, 1: 1.1 * t, 2: 0.02 if mode != FR else 0.01}[statut_taux]         # (1278 à 1280) ; multi-service : mode chauffage
    waux0 = taux * pabs_ch[piv_ch]                                                  # (1278)
    if fonc_compr == 1:
        lrmin, ccp = {0: (lr, ccp), 1: (lr + 0.05, 0.9 * ccp), 2: (0.4, 1.0)}[statut_continu]   # (1281, 1282)
        assert lrmin * 0.3 >= ccp * taux                                            # (1283)
    dfou0 = {1: 32, 2: 19, 3: 6, 4: 2}[typo_emetteur]; deq = 0.5                    # tableau 217

def encadrer(x, vals):                                                              # (1284, 1285, 1286)
    if x < vals[0]: return 0, 0, 0.0
    if x > vals[-1]: return N-1, N-1, 0.0
    j = premier indice >= 1 tel que x <= vals[j]; return j-1, j, (x - vals[j-1]) / (vals[j] - vals[j-1])

def pleine_charge(mat, th_amont, th_aval):
    j1, j2, cam = encadrer(th_amont, Valθam); i1, i2, cav = encadrer(th_aval, Valθav)
    pabs_pc = bilin(mat.pabs, i1, i2, j1, j2, cam, cav)                             # (1287)
    cop_pc = bilin(mat.cop, ...)                                                    # (1288 / 1289)
    return pabs_pc, cop_pc

def pas(gen, mode, h, th_amont, th_aval, qreq, rfonct_ecs=0.0, qreq_fr=0.0, pfou_source_maxi=None, saison, iecs_seule):
    # Entrées : Qreq en Wh par pas, températures amont (source_amont.pas) et aval (gestion de la génération)
    pabs_pc, cop_pc = pleine_charge(gen.mat[mode], th_amont, th_aval)
    pfou_brut = pabs_pc * cop_pc                                                    # (1290 / 1291)
    if gen.sys[mode] est air extrait: pfou_brut = min(pfou_brut, pfou_source_maxi)  # (1292 / 1293) via (1455 à 1458)
    if mode == CH and gen.multi and qreq_fr > 0: pfou_brut = 0.0                    # froid prioritaire (p. 790-791)
    if gen.double_ou_triple:
        pfou_brut *= (1 - rfonct_ecs) if mode == CH else max(0.0, 1 - rfonct_ecs - 0.25)   # (1294, 1295)
    qreq_act = qreq / gen.rdim                                                      # (1296)
    bloque = limite_atteinte(gen.lim[mode], th_amont, th_aval, mode)               # (1297 / 1298)
    pfou_pc = 0.0 if bloque else pfou_brut
    qrest_act = qreq_act if bloque else max(0.0, qreq_act - pfou_pc)
    pfou_lr = min(qreq_act, pfou_pc); lr = pfou_lr / pfou_pc if pfou_pc > 0 else 0.0            # (1299, 1300)
    pcomp_pc = pabs_pc - gen.waux0                                                  # (1301 / 1306)
    if lr == 0:
        # auxiliaires à charge nulle : une seule fois par pas, selon le type et la saison (1325 à 1327)
        pabs_lr = gen.waux0 * part_waux0(gen, mode, saison, iecs_seule, rfonct_ecs); pcomp_lr = pcompma = 0.0
    elif gen.fonc_compr == 2:
        pcomp_lr = pcomp_pc * lr                                                    # (1302)
        pcompma = pcomp_pc * gen.deq * lr * (1 - lr) / gen.dfou0[mode]              # (1303)
        pabs_lr = pcomp_lr + pcompma + gen.waux0                                    # (1304)
    else:
        cop_net = pfou_brut / pcomp_pc                                              # (1307)
        ccp_net = lrmin * pcomp_pc * ccp / (lrmin * pabs_pc - ccp * gen.waux0)      # (1308)
        if lr >= lrmin:
            cop_lr_net = cop_net * (1 + (ccp_net - 1) * (1 - lr) / (1 - lrmin))     # (1309)
            pcomp_lr = pfou_lr / cop_lr_net; pcompma = 0.0; pabs_lr = pcomp_lr + gen.waux0   # (1310, 1311)
        else:
            pcomp_min = pfou_brut * lrmin / (cop_net * ccp_net)                     # (1313, 1314)
            pcomp_lr = pcomp_min * lr / lrmin                                       # (1315)
            lrc = lr / lrmin; pcompma = pcomp_min * gen.deq * lrc * (1 - lrc) / gen.dfou0[mode]   # (1316, 1317)
            pabs_lr = pcomp_lr + pcompma + gen.waux0                                # (1318)
    cop_lr = pfou_lr / pabs_lr if pabs_lr > 0 else 0.0                              # (1305 / 1312 / 1319)
    rejet = min(0.0, pcomp_lr + pcompma - pfou_lr) if mode == CH else (pcomp_lr + pcompma + pfou_lr)   # (1333 / 1335)
    return Sortie(qcef_elec=pabs_lr * gen.rdim, qfou=pfou_lr * gen.rdim, qrest=qrest_act * gen.rdim,
                  eta=cop_lr, tau=lr, rejet=rejet * gen.rdim, cop_pc=cop_pc)      # (1328 à 1333)

# Ordre d'appel à chaque heure, pour une génération :
#   1. source_amont.pas(h) : θamont(h) à partir de θext, θet, Tair_extrait, ou de l'état (θb(j), Tdépart_amont(h-1), φrejet(h-1)) ; (1406 à 1441)
#   2. mode ECS (spécification ecs.md et cet.md) -> rfonct_ecs(h), iecs_seule(h), φrejet,ecs ;
#   3. mode froid si Qreq,fr > 0 et saison le permet ; 4. mode chauffage sinon ; chaque appel = pas(...) ci-dessus ;
#   5. agrégats (1336 à 1339) ; φrejet(h) et τcharge(h) renvoyés à source_amont pour h+1 ;
#   6. source_amont.auxiliaires(τcharge) : Waux,am (1443 à 1453) ajouté aux auxiliaires de génération (hors Qcef du générateur).

# États conservés d'une heure à l'autre : φrejet_gnr(h-1) par générateur et leur somme ; Tdépart_amont (nappe avec échangeur,
# réinitialisé à 12 °C au premier pas de chaque saison) ; θb(j) recalculé au changement de mois ; côté PAC aucun état
# (Qrest est repris par la gestion de la génération). Waux,0, LRcontmin, Ccp, Dfou0, matrices : calculés une fois au prétraitement.

def part_waux0(gen, mode, saison, iecs_seule, rfonct_ecs):
    # mono : 1 si saison du mode ; réversible : chauffage en saison chauffage ou mixte, froid en saison froid ;
    # double/triple : 0 si iecs_seule (porté par l'ECS, 1323), sinon (1 - rfonct_ecs) si Qreq,ecs > 0 (1326, 1327), sinon 1.

def source_amont_pas(sa, h, etat):                                                  # 8.26, 8.27
    if sa.fluide == AIR: θ = {1: θext[h], 2: θet[h], 3: Tair_extrait[h]}[sa.type_air]          # (1406 à 1408)
    elif sa.fluide == SOL: θf = θb(j) + φrejet_prev * Rb / L ; θ = interp(θf, (-5, 0, 5, 10), (-4, 1.5, 4, 6.5))   # (1462 à 1464, tableau 246)
    elif type_eau in (1, 4, 5):
        θf = θb(j) + φrejet_prev * Rb / L (sonde) | échangeur NUT-ε avec état Tdépart (1412 à 1425) | θb(j) (1426)
        θ = θf + Δθcond(φrejet_prev) / 2                                            # (1428)
    elif type_eau == 2: θ = θes_tour(θext, ωext) + Δθcond_FR / 2                      # (1429 à 1437)
    elif type_eau == 3: θ = θbe(j) + Δθcond / 2                                     # (1438 à 1440)
    return θ
```

## Sorties RSEE pour le banc

- `O_Cef_ch_annuel` (Sortie_Groupe_C, kWh/m² (SREF) par an, énergie finale chauffage (générateur + auxiliaires imputés))
- `O_Cef_fr_annuel` (Sortie_Groupe_C, kWh/m² par an, énergie finale refroidissement)
- `O_Cef_ch_elec_annuel` (Sortie_Groupe_C, kWh/m² par an, part électrique du chauffage (= Qcef_ch id_engen 50 pour une PAC seule))
- `O_Cef_fr_elec_annuel` (Sortie_Groupe_C, kWh/m² par an)
- `O_Cef_ch_mois, O_Cef_fr_mois` (Sortie_Groupe_C (Sortie_Mensuelle, Noeud.mensuel), kWh/m² par mois ; permet de tester la dépendance à θext (COP d'hiver))
- `O_B_Ch_annuel, O_B_Fr_annuel, O_B_Ch_mois, O_B_Fr_mois` (Sortie_Groupe_C, kWh/m², besoins aux émetteurs (déjà au banc) ; O_Cef / O_B donne un SCOP de contrôle)
- `O_Cef_aux_distribution_annuel, O_Cef_auxs_elec_annuel` (Sortie_Groupe_C, kWh/m² ; à vérifier au banc si Waux,am (pompes de captage, Pvent_gaine) y est imputé)
- `O_Cef_elec_cons_ch_annuel, O_Cef_elec_cons_fr_annuel, O_Cef_elec_cons_ch_mois, O_Cef_elec_cons_fr_mois` (Sortie_Zone_C, kWh/m² (consommée, avant déduction du photovoltaïque))
- `O_Cef_elec_imp_ch_annuel, O_Cef_elec_imp_fr_annuel, O_Cef_elec_imp_ch_mois, O_Cef_elec_imp_fr_mois` (Sortie_Zone_C et Sortie_Batiment_C, kWh/m² importée)
- `O_Cef_elec_AC_ch_annuel, O_Cef_elec_AC_fr_annuel` (Sortie_Batiment_C, kWh/m² (autoconsommée))
- `generateur_principal_ch, generateur_principal_fr, vecteur_energie_principal_ch, vecteur_energie_principal_fr` (Sortie_Batiment_C, codes (identification du générateur et du vecteur ; filtre du banc))
- `Nbhcharge_0_ch, Nbhcharge_0_10_ch ... Nbhcharge_90_100_ch, Nbhcharge_HF_ch (idem _fr, _ECS)` (Sortie_Generation/Sortie_Generateur_Collection/Sortie_Generateur (aussi sous Sortie_Production_Stockage pour les ballons), heures : histogramme de τcharge(h) = LR par tranche de 10 % ; Nbhcharge_0 = heures à charge nulle, HF = hors fonctionnement (vu : 8760 h à 0 pour la PAC bureaux sans besoin ; 1891 / 4968 pour le T.ONE). Banc direct sur LR(h), équation (1332))
- `Q_fou_3_postes` (Sortie_Generateur, kWh par an (déduit des ordres de grandeur : 1025,8 et 3801,2) ; somme de Qfou (1336) sur l'année, tous modes)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch, O_Idsousdim_Court_Fr, O_Idsousdim_Long_Fr (et _BE)` (Sortie_Generation, indicateurs de sous-dimensionnement (Qrest non couvert, équation 1331) ; banc qualitatif)
- `IsChaudiereGaz, IsReliePrechauffageCW, NbReports_ECS` (Sortie_Generateur, booléens / compte ; NbReports_ECS relève de la spécification cet.md)

## Points ouverts (à trancher au codage)

- Codage de Statut_Taux : la nomenclature (p. 729) dit 0 par défaut / 1 déclarée, le corps (p. 785) dit 0 certifié / 1 justifié / 2 par défaut. Les RSEE montrent Statut_Taux = 2 avec Taux = 0 (bureaux) et Statut_Taux_Ch = 0 avec Taux_Ch = 0,0035 (T.ONE) : le codage p. 785 est le bon. À confirmer au banc sur O_Cef_ch_elec_annuel (le Waux,0 est de l'ordre de 1 à 2 % de Pabs pivot sur toutes les heures de saison).
- Pivot et indices garbled dans le texte pour les technologies eau de nappe/air (1250, pivot écrit (2,4), matrice 5 x 4 où le pivot est (4,2)), air ext/air recyclé froid (1266, 1272 : indices (4,3), (4,4) incohérents), air extrait/air neuf froid (1268 : pivot annoncé (4,2) mais équations en (2,4)), eau de nappe/air froid (1274 : (2,3), (2,4) au lieu de (3,2), (4,2)), eau de nappe/eau froid (1276 : (i,4) au lieu de (i,2)). Lecture retenue : la colonne pivot est toujours celle de la température amont pivot et les lignes sont propagées depuis cette colonne. Un banc sur un RSEE équipé de ces technologies (chercher Theta_Aval_Eau_De_Nappe_Air ou _Fr non nuls) tranchera sur O_Cef_fr_elec_annuel ; aucune des deux RSEE lues n'en a.
- Seuil « puissance nominale à 7 °C < ou > 100 kW » (tableaux 152, 155) : la puissance n'est pas définie ; déduction : Pabs(pivot) x COP(pivot) en kW. Le cas égal à 100 kW n'est pas tranché (prendre < 100). Banc : O_Cef_ch_elec_annuel sur un RSEE avec Statut_Donnee = 2 ou matrice incomplète et PAC air extérieur de plus de 100 kW.
- Air extrait/air neuf, chauffage : le texte intervertit « aval » et « amont » dans le tableau 157 et la figure 119 ; retenu : lignes = θaval air neuf (-15, -7, 2, 7, 20), colonnes = θamont air extrait (5, 10, 15, 20, 25), pivot (4,4) = 7 / 20. M_θ_Amont_Ch a 6 niveaux dont le 5 et le 6 identiques. Banc sur une PAC sur air extrait (Sys_Thermo_Ch = 3) : O_Cef_ch_elec_annuel.
- Limites de fonctionnement (1297, 1298) : le cas « Lim_θ = 1 ou 2 avec limite non atteinte » n'est pas écrit ; retenu : traitement comme Lim_θ = 0. Le RSEE bureaux a Lim_Theta = 2, Theta_Max_Av = 32 (aval air recyclé 20 °C, jamais atteint), Theta_Min_Am = -15 : la machine n'est jamais bloquée. Banc : O_Idsousdim_Court_Ch et Nbhcharge_HF_ch.
- Sens de Nbhcharge_HF_ch (4968 h pour le T.ONE, 0 pour la PAC bureaux à besoin nul) : hors fonctionnement, hors saison, ou heures où le générateur n'est pas sollicité ; la somme Nbhcharge_0 + tranches + HF = 8760 à vérifier. Banc : recomposer l'histogramme de LR(h) et comparer tranche par tranche.
- Interpolation hors plage : (1284) donne j1 = j2 et un dénominateur nul dans (1286) ; retenu Cθ = 0 (valeur de bord, pas d'extrapolation). Impact réel sur les heures à θext < -15 °C ou > 20 °C en chauffage. Banc : O_Cef_ch_mois en janvier et O_Cef_fr_mois en juillet.
- Table de correspondance sol (tableau 246) hors de -5 à 10 °C : bord ou prolongement linéaire non dit ; retenu bord. Pas de RSEE sol dans les deux lus.
- Δθcond (1428, 1437, 1440) quand φrejet(h-1) = 0 : non défini ; retenu 0. Et la convention (-θEvap_CH en chauffage) suppose que le signe de φrejet du pas précédent dit le mode courant, ce qui est faux au changement de mode : accepter l'erreur d'une heure.
- Tdépart_amont initial « au premier pas de temps d'une saison » : la saison est celle de la génération (union des groupes, fiche 8.4) ; retenu l'union déjà calculée dans banc/cep.py.
- Waux,am (pompes de captage, Pvent_gaine, tour) : la fiche 8.26 ne dit pas à quel poste du Cep ces consommations sont imputées (chauffage, froid ou auxiliaires de distribution). Déduction : poste du mode servi, au prorata (1453). Banc : O_Cef_aux_distribution_annuel contre O_Cef_ch_elec_annuel sur un RSEE à PAC géothermique avec Ppompes_Cap non nul.
- Champ Valeur_Declaree_Defaut (= 1) du nœud NonReversible : sans correspondant nommé ; hypothèse Statut_fonct_part (0 par défaut, 1 déclarée) alors que le triple service porte explicitement Statut_Fonct_Part_Ch. Sans effet sur le calcul si LRcontmin et CCP sont lus via Statut_Fonctionnement_Continu.
- Champ Theta_Max_Rech_BE, Theta_Min_Fr_BE, Ppompes_Boucle_Eau, Qv_nom_tour, Id_SF_Extraction, Type_Generateur_Fr de Source_Amont : absents de la fiche 8.26 (boucle d'eau avec recharge, fiche 8.10 ou Titre V). À ignorer en première passe.
- Le nœud TripleService nomme le couple M_θ du chauffage air ext/air recyclé « Theta_Aval_Air_Extrait_Air_Recycle_Ch » : la correspondance nom de champ / technologie doit être prise par position (Sys_Thermo_ts) et non par le nom. Plusieurs couples sont à 1 simultanément (valeurs résiduelles) : ne lire que celui de la technologie retenue.
- Double et triple service : Rfonct_ecs(h) et iECS_seule(h) viennent du calcul ECS (spécifications ecs.md et cet.md) ; la saison qui décide la part de Waux,0 (1325 à 1327) et la priorité froid sur chaud dépendent de la gestion de la génération (8.15), non spécifiée ici. Le banc sur le T.ONE (O_Cef_ch_elec_annuel, O_Cef_fr_elec_annuel, O_Cef_ecs_elec_annuel) ne sera possible qu'avec les deux spécifications assemblées.
- Dégivrage : aucun modèle dans le texte (0 occurrence dans 8.23, 8.26, 8.27). Si le banc montre un écart hivernal systématique sur O_Cef_ch_mois pour les PAC air extérieur, chercher ailleurs (fiche 8.15 ou Titre V), pas dans cette famille.
- Les équations (1297) et (1298) comparent θaval(h) à une « température départ aval » alors que la matrice utilise la moyenne départ-retour pour l'eau (p. 735) : retenu θaval(h) tel que fourni par la gestion de la génération dans les deux cas.

## Tableaux en image dans le PDF

- Figure (sans numéro) p. 735 « La figure ci-dessous montre l'organisation des données de performance » : image non rendue en texte.
- Figures 117 à 125 (p. 739, 743, 745, 747, 749, 751, 753, 755, 757) : grilles de matrices de performance en chauffage, rendues comme suites de nombres mélangés (températures départ/retour/aval et ordres de priorité) ; reconstituées ici à partir des tableaux 151 à 175 et des équations.
- Figures 126 à 131 (p. 759 à 770) : matrices ECS, même rendu, hors champ.
- Figures 132 à 138 (p. 771, 773, 775, 777, 779, 781, 783) : grilles de matrices en refroidissement, même rendu, reconstituées à partir des tableaux 196 à 214.
- Figure 139 (p. 795) : schéma de sous-décomposition d'un pas de temps d'un double service (Rfonct_ecs, Rpuis_dispo), lisible seulement par ses légendes.
- Tableaux 152 à 177 et 197 à 216 (coefficients Cnn) : rendus en texte en deux colonnes désordonnées (aval puis amont) mais complets ; le tableau 207 (p. 778) et le tableau 210 (p. 780) nomment Cnnav des coefficients amont, le tableau 159 (p. 746) titre « air extérieur / air recyclé » pour l'air extrait / air neuf, les tableaux 167, 168, 170 (p. 752, 754) titrent « eau glycolée / air » pour eau de nappe/air et eau de boucle/air.
- Tableau 144 (nomenclature, p. 726 à 732) et tableau 244 (p. 891 à 895) : rendus en colonnes éclatées mais lisibles.
- Équations 1429 à 1432 (p. 901, tour humide) et 1419 à 1423 (p. 899) : fractions rendues sur plusieurs lignes, reconstituées ; l'équation implicite 1430 est confirmée par 1429.

## Estimation

Environ 850 lignes de Python : 250 lignes de tables (16 technologies : températures, pivot, Val_util_max, Cnn COP/EER et Pabs, chaînes de propagation, correspondances Sys_Thermo_Rev/ds/ts), 120 lignes de lecture RSEE et de prétraitement des matrices (contrôles, statuts, propagation), 150 lignes de calcul horaire (interpolation, limites, charge partielle deux régimes, Waux,0 selon catégorie et saison, sorties), 230 lignes pour les sources amont (air, sonde, nappe avec échangeur NUT-ε et état Tdépart, nappe sans échangeur, boucle, tour humide avec itération sur ωsat, tour sèche, sol avec table 246, auxiliaires et répartition), 100 lignes de banc (Sortie_Groupe_C O_Cef_ch_elec_annuel et O_Cef_fr_elec_annuel, histogramme Nbhcharge, Q_fou_3_postes). Difficulté moyenne pour la PAC seule (modèle algébrique sans état, bien numéroté) ; difficulté élevée pour l'intégration : θaval et Qreq viennent de la gestion de la génération et des distributions qui n'existent pas encore dans openBCE, les saisons qui conditionnent Waux,0 et la priorité froid/chaud sont celles de la fiche 8.15, et le banc sur le T.ONE dépend du module ECS (spécification cet.md). Le premier banc réaliste est la PAC air extérieur/air recyclé mono-service des bureaux (rsee_b : Rdim 1, pivot certifié 3,54 / 3,05 kW, Fonc_compr 1 par défaut, Typo_Emetteur 3), qui ne demande que θaval = température d'air du groupe et Qreq = besoin aux émetteurs déjà calculé par groupe.calculer en mode Th-C.
