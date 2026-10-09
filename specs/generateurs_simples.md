# Spécification : Générateurs à effet joule, chaudières, réseaux de chaleur

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille « générateurs sans cycle thermodynamique » du chapitre 8 : effet joule direct (fiche 8.18, type 500, pages 668 à 671), chaudières gaz, fioul et bois (fiche 8.19, types 0 à 4 du tableau 116, pages 672 à 686), autres générateurs gaz à combustion (fiche 8.20, types 103 à 109 : radiateurs et poêles gaz, chauffe-eau gaz, accumulateurs gaz, générateurs d'air chaud, tubes et panneaux radiants, pages 687 à 703), poêles et inserts bois (fiche 8.22, type 401, pages 721 à 724), sous-stations de réseaux de chaleur et de froid (fiche 8.28, types 600 et 601, pages 912 à 917). Pour chaque type la spécification couvre : puissance maximale, rendement ou efficacité selon la charge et la température aval, auxiliaires propres, pertes récupérables vers l'ambiance (Φvc), énergie non fournie reportée (Qrest), et l'écriture dans la matrice {poste ; énergie} Qcef (tableaux 114, 134, 143, 250 : postes 1 chauffage, 2 refroidissement, 3 ECS ; énergies 10 gaz, 20 fioul, 30 charbon, 40 bois, 50 électricité, 60 réseau).

Le contrat d'interface est le même pour les cinq fiches : à chaque heure h le composant reçoit Qreq (Wh) par poste, l'indicateur de fonction idfonction, la température aval θaval (°C) par poste, la température d'ambiance θamb du local de la génération, l'indicateur iECS_seule et, pour les générateurs double service, le ratio Rpuis_dispo ; il rend Qfou, Qcons, Waux,pro, Φvc, Qrest, τcharge, ηeff, Rfonctecs et la matrice Qcef. Ce contrat correspond à ce que le moteur openBCE devra brancher sous une future classe « Generation » (fiches 8.29 calculs génération et 8.30 gestion/régulation, hors lot).

Hors champ, et pourquoi : la gestion/régulation de la génération qui produit Qreq, θaval, Rpuis_dispo et iECS_seule et répartit entre générateurs selon Type_Priorite et Idpriorite_Ch/Ecs (fiches 8.29 et 8.30, autre lot) ; les générateurs thermodynamiques (8.23 à 8.27, autre famille) ; la cogénération (8.21, type différent et production d'électricité) ; les pertes de distribution primaire et secondaire et les ballons (chapitres 8.6 à 8.17 et 9) qui gonflent Qreq en amont ; l'agrégation de Qcef en Cef et Cep (2488 à 2490, déjà dans consommation.py) ; la température θamb d'un local hors volume chauffé (définie par la fiche de la génération, non par celles-ci). L'effet joule est traité en premier : il est le générateur de chauffage de 18 projets du banc (47 fichiers portent la balise Generateur_Effet_Joule dans brut/rsee_entetes.json), devant Generateur_Combustion (84 fichiers) et Reseau_Chaleur (3 fichiers).

## Entrées (RSEE)

- `Entree_Projet/Generation_Collection/Generation` / `Index, Type_Priorite, Idraccord_Gnr, Idraccord_Reseau_Gen, Pos_Gen, Id_Bat, Id_Et, Type_Gestion_Chaud_Gen, Theta_Wm_Ch, Type_Gestion_Froid_Gen, Theta_Wm_Fr, Theta_Wm_Ecs` : idraccord_gnr (8.19 et 8.20, 0 permanent, 1 avec isolement) ; idpos_gen = Pos_Gen (1 en volume chauffé) ; Theta_Wm_* : température moyenne de l'eau qui alimente θaval,CH / θaval,ECS via la gestion/régulation (hors lot) ; Type_Gestion_*_Gen : loi d'eau (hors lot) ; entiers et réels ; valeurs vues : Type_Priorite 1 ou 2 ; Idraccord_Gnr 1 (avec isolement) ; Pos_Gen 0 (hors volume chauffé) ou 1 ; Theta_Wm_Ch 70 ; Theta_Wm_Fr 7 ; Theta_Wm_Ecs 50 ou 54 (RSEE rsee_a et rsee_b)
- `Generation/Generateur_Collection/Generateur_Effet_Joule` / `Index, Rdim, Pmax, Id_Fou_Gen, Idpriorite_Ch, Idpriorite_Ecs` : Rdim ; Pngen = 1000 x Pmax (W) ; idfougen = Id_Fou_Gen (1 chauffage ou 3 ECS, jamais 4, page 670) ; idengen = 50 fixé par le type ; Idpriorite_* : rang dans la cascade de la génération (fiche 8.30, hors lot) ; Rdim entier, Pmax réel, autres entiers ; valeurs vues : Rdim 1 ; Pmax 100 (appoints des PAC du RSEE rsee_a) et 2 (sèche-serviettes, arbre_4b62.txt) : l'unité est le kW, la fiche donne Pngen en W (page 668) ; Id_Fou_Gen 1 (chauffage) ; Idpriorite 0
- `Generation/Generateur_Collection/Generateur_Combustion` / `balise vue dans les en-têtes de 84 RSEE (rsee_entetes.json) ; champs relevés dans les en-têtes : Pn_gen, Pint, Alim_Chaudiere_Bois, Id_Fou_Gen_1 / Id_Fou_Gen_4 / Id_Fou_Gen_5 ; les autres noms n'ont pas pu être lus (limite de deux RSEE, aucun des deux ne porte de chaudière)` : Pn_gen (kW), Pint (kW), Alim_Chaudiere_Bois (0 à 3), idtype (tableau 116 : 0 gaz classique, 1 gaz condensation, 2 fioul classique, 3 fioul condensation, 4 bois ; tableau 125 : 103 à 109), TypeCombustibleBois (1 bûches, 2 granulés, 3 plaquettes), R_pn, R_pint, Waux_nom, Waux_int, Wveille, Q_po_30, statuts (certifié, justifié, déclaré, défaut) des rendements et des pertes à l'arrêt, idpertes_parois (1 à 3), Rdim, et pour 8.20 : A à H, fmaj (présence de ventilateur de combustion, évacuation des fumées), veilleuse ; à relever sur un RSEE à chaudière ; valeurs vues : aucune
- `Generation/Generateur_Collection/Reseau_Chaleur` / `balise vue dans 3 RSEE ; champ Type_Reseau vu dans 2 en-têtes ; autres noms non lus` : idtype 600 ou 601 ; Type_Reseau : type de réseau (eau chaude BT, eau chaude HT, vapeur BP, vapeur HP) qui fixe θprs et Dss (tableau 249) et la ligne de Bss (tableau 248) ; classes d'isolation primaire et secondaire (colonne de Bss) ; PEss (kW) ; Rdim ; Id_Fou_Gen (1, 3 ou 4 pour 600 ; 2 pour 601) ; à relever ; valeurs vues : aucune
- `Zone/Groupe/Emetteur/Distribution_Groupe_Chaud et Distribution_Groupe_Froid` / `Id_Dist_1re, Id_Ballon, Theta_Dep_Dim_Ch, Theta_Ret_Dim_Ch, Qnom_Ch, Pcirculateur_Ch` : chaîne groupe -> distribution secondaire -> distribution intergroupe -> génération : sert à retrouver quelle génération reçoit le Qreq du groupe (hors lot, nécessaire au banc par groupe) ; entiers et réels ; valeurs vues : Id_Dist_1re 4 (chaud), 2 (froid) dans rsee_a
- `Entree_Projet/Distribution_Intergroupe_Chaud, _Froid, _ECS` / `Index, Id_Gen, Type_Prim, Lvc_Prim, Lhvc_Prim, Umoyen_Vc_Prim_Ch, Pcirc_Prim_Ch` : Id_Gen : lien vers Generation.Index ; pertes de distribution primaire ajoutées à Qreq (fiches 8.6 à 8.9, hors lot) ; entiers et réels ; valeurs vues : Id_Gen 1 vers la génération d'index 1
- `Zone/Groupe/Emetteur_ECS/Distribution_Groupe_ECS` / `Id_Dist_Primaire, Id_Ballon, Type_Dist_Primaire` : lien ECS groupe -> distribution intergroupe ECS -> génération ; détermine Qreq,ECS et iECS_seule ; entiers ; valeurs vues : Id_Dist_Primaire 3 ; Id_Ballon 0
- `Sortie_Projet/Sortie_Generation_Collection/Sortie_Generation` / `Index, O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch, O_Idsousdim_Court_Fr, O_Idsousdim_Long_Fr (et variantes _BE)` : indicateurs de sous-dimensionnement issus de Qrest (fiche 8.29) : utiles au banc pour vérifier Pmax ; entiers 0/1 ; valeurs vues : O_Idsousdim_Court_Ch 1 sur la génération PAC + joule de rsee_a

## Paramètres conventionnels

- Effet joule : ηgnr = 1, Waux,pro = 0, Φthrecact = 0, Φvc = 0, type 500, idengen 50, idfougen 1 ou 3 seulement = 1 ; 0 Wh ; 0 Wh ; 0 Wh (p. 670, équations 1066 et 1071)
- PCSI (ratio PCS/PCI) par combustible = gaz naturel 1,11 ; GPL 1,09 ; FOD 1,07 ; bois 1,08 (idengen 10, 10, 20, 40) (p. 677 tableau 117 ; 692 tableau 126 (sans bois))
- Température maximale de fonctionnement des générateurs à combustion = 100 °C (p. 677 et 693)
- Température minimale de fonctionnement θaval,min = 40 °C gaz ou fioul classique ; 30 °C gaz ou fioul condensation ; 70 °C bois ; 20 °C par défaut pour les accumulateurs et chauffe-eau gaz (8.20) (p. 677 ; 693)
- Correction des rendements selon le statut de la donnée = certifié : aucune ; justifié : -10 % ; déclaré : -20 % ; par défaut : valeurs imposées (1073, 1074). Pas de pénalité sur les valeurs par défaut (p. 678 ; 693)
- Tableau 119 : c1 à c6 (défauts chaudières) = gaz/fioul Pn <= 400 kW : c1 94,0 ; c2 1,0 ; c3 103,0 ; c4 1,0 ; c5 4,0 ; c6 -0,4. Gaz/fioul Pn > 400 kW : 96,6 ; 0 ; 105,6 ; 0 ; 4,0 ; 0. Bois bûche : 89 ; 2,0 ; 84 ; 2,0 ; 14,0 ; -0,28. Bois granulés/plaquettes : 91 ; 2,0 ; 88 ; 2,0 ; 14,0 ; -0,28 (p. 679)
- Wveille par défaut = 20 W (p. 679, équation 1076)
- Tableau 120 : c7 à c10 et n (défauts auxiliaires) = gaz/fioul : c7 0 ; c8 45 ; c9 0 ; c10 15 ; n 0,48. Bois manuel tirage naturel : 0 ; 0 ; 0 ; 0 ; 1. Bois manuel air pulsé : 74 ; 0,5 ; 74 ; 0,5 ; 1. Bois automatique tirage naturel : 0 ; 10 ; 0 ; 10 ; 1. Bois automatique air pulsé : 74 ; 10,5 ; 74 ; 10,5 ; 1 (p. 679 et 680)
- Tableau 121 : pente αth et température de référence des rendements = gaz/fioul classique : αth,nom 0,04, θav,ref,nom 70, αth,int 0,05, θav,ref,int 40 ; condensation : 0,2 ; 70 ; 0,2 ; 33 ; bois : 0 ; 70 ; 0 ; 70 (p. 681)
- Exposant des pertes à l'arrêt ramenées à l'écart de température = ((θaval - θamb)/30)^1,25 (p. 681 équation 1081 ; 695 équation 1128)
- Tableau 122 / 132 : part des pertes par les parois à l'arrêt p_Qp.g_arret = idpertes_parois 1 (pas de ventilateur dans le circuit de combustion) 0,50 ; 2 (ventilateur) 0,75 ; 3 (clapet sur conduit de fumées) 1,0 (p. 686 ; 701)
- Tableau 123 / 133 : part des pertes par les parois en fonctionnement p_Qp.g_fonct = chaudière bois 0,25 ; tout autre générateur 0,30 ; flux nul si hors volume chauffé (p. 686 ; 702)
- Tableau 127 (8.20) : rendements par défaut A (Rpn) et C (Rpint), B et D nuls = radiateur/poêle gaz Pn < 5 kW A 80 ; >= 5 kW sans ventilateur 82 ; avec ventilateur 84 ; chauffe-eau gaz < 10 kW 82 ; > 10 kW 84 ; accumulateur gaz 84 ; accumulateur condensation 98 ; générateur d'air chaud standard A 84, C 77 ; condensation A 90, C 83 ; tube radiant 85 ; panneau radiant 90 (p. 694)
- Tableau 128 (8.20) : pertes à charge nulle par défaut E, F = générateur d'air chaud 1,75 / -0,55 ; accumulateur > 200 l et montée en température < 45 mn 1,7 / 0 ; autres accumulateurs 1,5 / 0 ; chauffe-eau gaz 1,5 / 0 (p. 694)
- Tableau 129 (8.20) : auxiliaires par défaut G, H = générateur d'air chaud sans ventilateur côté émission 0 / 4 ; avec 0 / 54 ; tube radiant avec ventilateur 0 / 54 ; radiateur/poêle gaz 40 / 0 par ventilateur (combustion et émission comptés séparément) ; chauffe-eau 0 / 0 ; accumulateur 0 / 0. Veilleuse : Wveille + consommation de la veilleuse / 2,58 (p. 694)
- Plafonds des valeurs déclarées (8.20) = Rpn = min(0,8 Rpn,decl ; 86 %) ; Rpint = min(0,8 Rpint,decl ; 81 %) ; générateurs d'air chaud : formules valables jusqu'à Pn = 300 kW, valeurs figées au-delà (p. 693, 696)
- Tableau 130 / 131 : fmaj = radiateurs gaz : ventilateur de combustion 1,02 ; sans, micro-ventouse 1,04 ; sans, cheminée 1,06 ; panneaux radiants 1,00 ; tubes radiants 1,06 (p. 697)
- Poêles et inserts bois : type 401, chauffage seul, pertes à charge nulle nulles, Φvc = 0, énergie 40 bois + auxiliaires 50 = QH,sys,ls,0 = 0 ; Φvc = 0 (p. 723, 724)
- Tableau 248 : Bss selon le type de réseau et les classes d'isolation (secondaire 4/3/2/1, primaire 5/4/3/2) = eau chaude BT 3,5 ; 4 ; 4,4 ; 4,9 ; eau chaude HT 3,1 ; 3,5 ; 3,9 ; 4,3 ; vapeur BP 2,8 ; 3,2 ; 3,5 ; 3,9 ; vapeur HP 2,6 ; 3 ; 3,3 ; 3,7 (p. 915)
- Tableau 249 : θprs et Dss = eau chaude BT 105 °C, 0,6 ; eau chaude HT 150 °C, 0,4 ; vapeur BP 110 °C, 0,5 ; vapeur HP 180 °C, 0,4 (p. 916)
- Réseaux : Waux,pro = 0, Φvc = 0 (pertes hors volume chauffé), réseau de froid Qssact = 0 = 0 Wh (p. 916 (1480, 1481), 917 (1484))
- th, durée du pas de temps = 1 h (les puissances en W valent des Wh) (p. 676)

## Équations

- (1066, p. 670) ηgnr = 1 ; Waux,pro = 0 ; Φthrecact = 0 ; effet joule ; type 500, toujours
- (1067, p. 670) Pmax = Pngen ; Pngen en W (RSEE : 1000 x Pmax) ; indépendant des conditions extérieures
- (1068, p. 670) Qfou = MIN(Qreq ; Pmax x th) ; Qcons = Qfou ; Wh ; chauffage ou ECS
- (1069, p. 670) Qrest = Qreq - Qcons ; Wh ; reporté au générateur suivant ou à l'heure suivante par la gestion
- (1070, p. 670) τcharge = Qfou / Pmax ; formule en image, reconstruite des fragments « Qfou / Pmax » ; 
- (1071, p. 670) Φvc = 0 ;  ; 
- (1072, p. 670) Rfonctecs = τcharge ;  ; fonction ECS (idfougen = 3)
- (tableau 114, p. 671) Qcef(idfougen ; 50) = Qcons ; poste 1 ou 3, énergie 50 électricité ; 
- (1073, p. 679) R_pn = (c1 + c2 x log(Pn_gen)) / (100 x PCSI) ; Pn_gen kW ; c1, c2 tableau 119 ; log décimal (déduit du 1,0 x log Pn) ; R_pn par défaut seulement
- (1074, p. 679) R_pint = (c3 + c4 x log(Pn_gen)) / (100 x PCSI) ;  ; R_pint par défaut
- (1075, p. 679) Q_po_30 = 1000 x c5 x Pn_gen^c6 x Pn_gen  (W) ; c5, c6 tableau 119 ; pertes à l'arrêt par défaut
- (1076, p. 679) Wveille = 20 W ;  ; par défaut
- (1077, p. 679) Waux_nom = c7 + c8 x Pn_gen^n ; tableau 120 ; sous-catégorie Alim_Chaudiere_Bois pour le bois ; par défaut
- (1078, p. 679) Waux_int = c9 + c10 x Pint^n ;  ; par défaut
- (statuts (texte), p. 678) R = R_saisi x {1 ; 0,9 ; 0,8} selon certifié / justifié / déclaré ; erreur si R_pn ou R_pint ramené au PCS >= 1 ;  ; avant toute correction
- (1079, p. 681) R_pn(θaval) = R_pn + αth,nom x (θav,ref,nom - θaval)  (%) ; tableau 121 ; chaque heure, par poste
- (1080, p. 681) R_pint(θaval) = R_pint + αth,int x (θav,ref,int - θaval)  (%) ;  ; 
- (1081, p. 681) φthstab(θaval) = MAX(0 ; Q_po_30 x ((θaval - θamb(h)) / 30)^1,25)  (W) ;  ; 
- (1082, p. 682) Qfou,ECS(h) = MIN(Pth,nom,ecs(h) x th ; Qreq,ECS(h) / Rdim) ;  ; ECS calculée en premier
- (1083, p. 682) Pth,nom,ecs(h) = 1000 x R_pn(θaval,cr_ecs(h)) / R_pn x Pn_gen ; W ; 
- (1084, p. 682) θaval,cr_ecs(h) = MAX(θaval,ecs(h) ; θaval,min) ; θaval,min par type (page 677) ; 
- (1085, p. 682) Rfonct,ECS(h) = Qfou,ECS(h) / (Pth,nom,ecs(h) x th) ; 0 si Qfou,ECS = 0 ;  ; 
- (1086, p. 682) Qrest,ECS(h) = Qreq,ECS(h) - Qfou,ECS(h) ;  ; 
- (1087, p. 683) Pth,int,ecs(h) = 1000 x R_pint(θaval,cr_ecs(h)) / R_pint x Pint ;  ; 
- (1088, p. 683) φpertes,int,ecs(h) = (100 % / R_pint(θaval,cr_ecs(h)) - 1) x Pth,int,ecs(h) ; W ; 
- (1089, p. 683) φpertes,nom,ecs(h) = (100 % / R_pn(θaval,cr_ecs(h)) - 1) x Pth,nom,ecs(h) ;  ; 
- (1090, p. 683) Qpertes,ecs(h) = Rfonct,ECS(h-1) x φthstab(θaval,cr_ecs(h-1)) x th ;  ; Qfou,ecs(h) = 0 et iECS_seule(h) = 1 (chaudière à l'arrêt, dernier état = ECS de h-1)
- (1091, p. 683) Qcons,ecs(h) = Qpertes,ecs(h) ;  ; même cas
- (1092, p. 683) Waux,ecs(h) = Wveille x th ;  ; même cas
- (1093, p. 683) Qpertes,ecs(h) = (fx x φpertes,int(h) + (1 - fx) x φthstab(θaval,cr_ecs(h))) x th ;  ; 0 < Qfou,ecs <= Pth,int,ecs x th (cycles tout ou rien)
- (1094, p. 683) Waux,ecs(h) = (fx x Waux_int + (1 - fx) x Wveille) x th ; le texte écrit Waux_min, lu Waux_int ; même plage
- (1095, p. 683) fx = Qfou,ecs(h) / (Pth,int,ecs(h) x th) ;  ; même plage
- (1096, p. 684) Qpertes,ecs(h) = (fx x φpertes,nom(h) + (1 - fx) x φpertes,int(h)) x th ;  ; Pth,int x th < Qfou,ecs <= Pth,nom x th (modulation du brûleur)
- (1097, p. 684) Waux,ecs(h) = (fx x Waux_nom + (1 - fx) x Waux_int) x th ; le texte écrit Waux_min et Wveille ; par continuité avec 1094 on lit Waux_nom et Waux_int (point ouvert) ; même plage
- (1098, p. 684) fx = (Qfou,ecs(h) - Pth,int,ecs(h) x th) / ((Pth,nom,ecs(h) - Pth,int,ecs(h)) x th) ;  ; 
- (1099, p. 684) Qcons,ecs(h) = (Qfou,ecs(h) + Qpertes,ecs(h)) / PCSI ; énergie finale sur PCI ; 
- (1100, p. 684) Qfou,CH(h) = MIN(Rpuisdispo(h) x Pth,nom,ch(h) x th ; Qreq,CH(h) / Rdim) ;  ; chauffage après l'ECS
- (1101, p. 684) Pth,nom,ch(h) = 1000 x R_pn(θaval,cr_ch(h)) / R_pn x Pn_gen ; avec θaval,cr_ch = MAX(θaval,ch ; θaval,min) par analogie avec 1084 ;  ; 
- (1102, p. 684) Rpuisdispo(h) = 1 - Rfonct,ecs(h) ;  ; 
- (1103, p. 684) τcharge_ch(h) = Qfou,CH(h) / (Rpuisdispo(h) x Pmax,ch(h)) ; Pmax,ch = Pth,nom,ch x th ; 
- (1104, p. 684) Qrest,CH(h) = Qreq,CH(h) - Qfou,CH(h) ;  ; 
- (1105, p. 685) Qpertes,ch(h) = Rpuisdispo(h) x φthstab(θaval,cr_ecs(h)) x th ;  ; Qfou,ch(h) = 0 et Rpuisdispo(h) < 1 (ECS produite cette heure)
- (1106, p. 685) Qpertes,ch(h) = Rpuisdispo(h) x φthstab(θaval,cr_ch(h-1)) x th ;  ; sinon si Qfou,ch(h-1) > 0
- (1107, p. 685) Qpertes,ch(h) = Rfonct,ecs(h-1) x φthstab(θaval,cr_ecs(h-1)) x th ;  ; sinon si Qfou,ecs(h-1) > 0
- (1108, p. 685) Qpertes,ch(h) = 0 ;  ; sinon (pas de fonctionnement en h ni h-1)
- (1109, p. 685) Qcons,ch(h) = Qpertes,ch(h) ;  ; Qfou,ch = 0
- (1110, p. 685) Waux,ch(h) = Wveille x th ;  ; Qfou,ch = 0
- (1093 à 1099 (ch), p. 685) mêmes formules avec l'indice ch quand Qfou,ch > 0 ;  ; 
- (1111, p. 685) Qfou(h) = Qfou,CH + Qfou,ECS ;  ; 
- (1112, p. 685) Qcons(h) = Qcons,CH + Qcons,ECS ;  ; 
- (1113, p. 685) Wauxpro(h) = Waux,ecs + Waux,ch ;  ; 
- (1114, p. 685) Qpertes(h) = Qpertes,ch + Qpertes,ecs ;  ; 
- (1115, p. 685) τcharge(h) = Rfonctecs(h) + Rpuisdispo(h) x τcharge_ch(h) ;  ; 
- (1116, p. 685) Pmax(h) = Rfonctecs(h) x Pmax,ecs(h) + Rpuisdispo(h) x Pmax,ch(h) ;  ; 
- (1117, p. 686) ηeff(h) = Qfou(h) / Qcons(h) ; 0 si Qcons = 0 ;  ; 
- (1118, p. 686) Qcef(3 ; idengen) = Qcons,ecs ; Qcef(3 ; 50) = Waux,ecs ; Qcef(1 ; idengen) = Qcons,ch ; Qcef(1 ; 50) = Waux,ch ; puis toutes les énergies (Wh) sont multipliées par Rdim ;  ; 
- (1119, p. 686) si Qfou(h) > 0 : φvc = idposgen x (p_Qp.g_fonct x Qpertes + Waux,pro) ; sinon φvc = idposgen x (p_Qp.g_arret x Qpertes + Waux,pro) ; x Rdim ; tableaux 122, 123 ; 
- (1120, p. 693) θaval_corr = MAX(θaval ; θfonct_min) ; 8.20 ; générateurs sur eau (accumulateurs, chauffe-eau)
- (1121, p. 693) si MAX(Rpn ; Rpint) / PCSI >= 1 : erreur « rendements sur PCS >= 1 » ;  ; préalable
- (1122, p. 693) RPn = A + B x log(Pn)  (%) ; tableau 127 ; par défaut ; Pn figé à 300 kW au-delà pour les générateurs d'air chaud
- (1123, p. 693) RPint = C + D x log(Pn)  (%) ;  ; 
- (1124, p. 693) Qp0 = Pn x (E + F x log(Pn)) / 100  (kW) ; tableau 128 ; sert de Qpo30 par défaut ; 
- (1125, p. 693) Paux = G + H x Pn  (W) ; tableau 129 ; hors chaudières gaz/fioul ; 
- (1126, p. 695) ida_fonctionne(h) = 0 ;  ; début de chaque pas
- (1127, p. 695) si Qreq != 0 : ida_fonctionne(h) = idfonction ;  ; 
- (1128, p. 695) QP0 = 100 x QPO30 / Rpn x (MAX(0 ; θaval_corr - θamb(h)) / 30)^1,25  (Wh) ; générateurs sur eau ; 
- (1129, p. 695) QP0 = 0 ;  ; générateurs sur air (103, 106 à 109)
- (1130, p. 696) Rpn = MIN(0,8 x Rpn,decl ; 86 %) ; générateur d'air chaud, valeur déclarée ; 
- (1131, p. 696) Rpint = MIN(0,8 x Rpint,decl ; 81 %) ;  ; 
- (1132, p. 696) Pmax = Pngen x 1000  (W) ; générateur d'air chaud ; énergie fournie et pertes comme la chaudière gaz (1082 à 1099, sans correction de température) ; 
- (1133, p. 696) Rpn = MIN(0,8 x Rpn,decl ; 86 %) ; radiateurs, poêles gaz, tubes et panneaux radiants ; Rpn seul connu, non corrigé en température ; 
- (1134, p. 697) Pmax = Pngen x 1000  (W) ;  ; 
- (1135, p. 697) QPx = fmaj x (100 - RPn / PCSI) x Qfouact x PCSI / RPn ; fmaj tableaux 130, 131 ; chauffage, radiateurs et radiants
- (1136, p. 697) ηeff_% = Qfouact / (Qfouact + QPx) x 100 x PCSI ;  ; 
- (1137, p. 697) Qconsact = Qfouact / ηeff_% x 100 ; tous les générateurs 8.20 en chauffage ; 
- (1138, p. 698) Wauxact = Rpuis_dispo x [τcharge x (Waux,nom - Wveille) + Wveille] ;  ; chauffage
- (1139, p. 698) ηeff_% = Rpn ; ECS (accumulateurs, chauffe-eau) ; fonctionnement intermittent à pleine charge
- (1140, p. 698) Pmax = Pngen  (W) ; ECS ; 
- (1141, p. 698) Qreqact = Qreq / Rdim ;  ; 
- (1142, p. 699) Qfouact = MIN(Qreqact ; Pmax) ;  ; 
- (1143, p. 699) τcharge = Qfouact / Pmax ;  ; 
- (1144, p. 699) Rfonctecs = τcharge ;  ; 
- (1145, p. 699) QPX = (100 - ηeff_% / PCSI) x Qfouact x PCSI / ηeff_% + idECS_seule x (1 - Rfonctecs) x QP0 ;  ; ECS
- (1146, p. 699) Qconsact = Qfouact / ηeff_% + idECS_seule x (1 - Rfonctecs) x QP0 ; ηeff_% en fraction ici (x100 attendu) ; ECS
- (1147, p. 699) Wauxact = Rfonctecs x Waux,nom + idECS_seule x (1 - Rfonctecs) x Wveille ;  ; ECS
- (1148 à 1150, p. 699) Qfouact = 0 ; Qrest = 0 ; τcharge = 0 ;  ; Qreq = 0
- (1151, p. 700) si ida_fonctionne(h-1) > 0 ou Rpuis_dispo < 1 : QPX = Rpuis_dispo x MAX(QP0 ; QP0prev) ; sinon QPX = Rpuis_dispo x QP0 ;  ; arrêt, chauffage, idraccord_gnr = 0
- (1152, 1153, p. 700) Qconsact = QPX ; ηeff_% = 0 ;  ; 
- (1154, p. 700) si ida_fonctionne(h-1) = 1 ou Rpuis_dispo < 1 : QPX = Rpuis_dispo x QP0prev ; sinon si ida_fonctionne(h-1) = 3 : QPX = Rfonctecs(h-1) x QP0prev ; sinon 0 ;  ; arrêt, chauffage, idraccord_gnr = 1
- (1155, 1156, p. 700) Qconsact = QPX ; ηeff_% = 0 ;  ; 
- (1157, p. 700) Wauxact = Rpuis_dispo x Wveille ;  ; arrêt, chauffage
- (1158, 1159, 1160, p. 700, 701) si iECS_seule = 1 : (si ida_fonctionne(h-1) > 0 : QPX = MAX(QP0 ; QP0prev) sinon QPX = QP0) ; Qconsact = QPX ; ηeff_% = 0 ;  ; arrêt, ECS, idraccord_gnr = 0
- (1161 à 1163, p. 701) si iECS_seule = 1 : (si ida_fonctionne(h-1) > 0 : QPX = Rfonctecs(h-1) x QP0prev sinon 0) ; Qconsact = QPX ; ηeff_% = 0 ;  ; arrêt, ECS, idraccord_gnr = 1
- (1164, p. 701) si iECS_seule = 1 : Wauxact = Wveille ;  ; arrêt, ECS seule ou mixte hors saison de chauffe
- (1165, p. 702) si ida_fonctionne(h) > 0 : φthreact = idpos_gen x (QPX x p_Qp_g_fonct + Wauxact) ; sinon φthreact = idpos_gen x (QPX x p_Qp_g_arret + Wauxact) ;  ; 
- (1166, p. 702) si Qreq > 0 : QP0prev = QP0 ; mémoire ; 
- (1167, p. 702) Qcons = Qconsact x Rdim ;  ; 
- (1168, p. 702) Waux,pro = Wauxact x Rdim ;  ; 
- (1169, p. 702) Qcef(idfonction ; idengen) = Qcons ; Qcef(idfonction ; 50) += Waux,pro ;  ; 
- (1170, p. 702) Qfou = Qfouact x Rdim ;  ; 
- (1171, p. 703) Φvc = Rdim x Φthreact ;  ; 
- (1172, p. 703) Qrest = Qreq - Qfou ;  ; 
- (1173, p. 703) ηeff = ηeff_% / 100 ;  ; 
- (1226, p. 723) Qreqact = Qreq / Rdim ; poêles et inserts ; formule en image, reconstruite des fragments ; 
- (1227, p. 723) Qfouact = MIN(Qreqact ; 1000 x Pngen) ; Pngen kW ; 
- (1228, p. 723) τcharge = Qfouact / (1000 x Pngen) ;  ; 
- (1229, p. 723) QH,sys,ls,100 = 1000 x Pngen x (100 / ηH,sys,n - 1) ; pertes à 100 % de charge, Wh ; calculé une fois
- (1230, p. 723) QH,sys,ls,0 = 0 ;  ; 
- (1231, p. 723) Φthreact = τcharge x QH,sys,ls,100 + (1 - τcharge) x QH,sys,ls,0 ;  ; 
- (1232, p. 723) Qconsact = Qfouact + Φthreact ;  ; 
- (1233, p. 724) Qfou = Rdim x Qfouact ;  ; 
- (1234, p. 724) Qcons = Rdim x Qconsact ;  ; 
- (1235, p. 724) Waux,pro = Rdim x τcharge x Paux,vent ; aucune consommation hors fonctionnement ; 
- (1236, p. 724) Φvc = 0 ; pertes Φthreact entièrement perdues ; 
- (1237, p. 724) ηeff = Qfouact / Qconsact ;  ; 
- (1238, p. 724) Qrest = Qreq - Qfou ;  ; 
- (tableau 143, p. 724) Qcef(1 ; 40) = Qcons ; Qcef(1 ; 50) = Waux,pro ;  ; 
- (1468, p. 914) Qreqact = Qreq / Rdim ; réseau de chaleur ; formules en image, reconstruites des fragments ; 
- (1469, p. 914) Qfouact = MIN(Qreqact ; Rpuisdispo x PEss x 1000) ; PEss kW ; 
- (1470, p. 914) Qfou = Rdim x Qfouact ;  ; 
- (1471, p. 914) τcharge = Qfouact / (Rpuisdispo x PEss x 1000) ;  ; 
- (1472, p. 915) Qssact = Rpuisdispo x Hss x (θss - θamb) ; Wh ; chauffage
- (1473, p. 915) Qss = Rdim x Qssact ;  ; 
- (1474, p. 915) Hss = Bss x (1000 x PEss)^(1/3)  (W/K) ; Bss tableau 248 ; 
- (1475, p. 915) θwh,ss = θaval ;  ; 
- (1476, p. 915) θss = Dss x θprs + (1 - Dss) x θwh,ss ; tableau 249 ; 
- (1477, p. 916) Qcons = Qfou + Qss ;  ; 
- (1478, p. 916) ηeff = Qfou / Qcons ;  ; 
- (1479, p. 916) Qrest = Qreq - Qfou ;  ; 
- (1480, p. 916) Waux,pro = 0 ;  ; 
- (1481, p. 916) Φvc = 0 ;  ; 
- (1482, p. 916) Rfonct_ecs = τcharge_ecs ;  ; ECS
- (1483, p. 917) si idECS_seule = 1 : Qssact = Hss x (θss - θamb) ; sinon Qssact = Rfonct_ecs x Hss x (θss - θamb) ; Hss et θss comme en chauffage ; ECS
- (1484, p. 917) Qssact = 0 ; réseau de froid (601) ; 
- (tableau 250, p. 917) Qcef(idfonction ; 60) = Qcons ; énergie 60 réseau ; 

## Algorithme

```
Structure commune (module openbce/generateurs.py proposé) :

    POSTES = {1: "ch", 2: "fr", 3: "ecs"} ; ENERGIES = (10, 20, 30, 40, 50, 60)
    @dataclass
    class Resultat: qfou, qcons, waux, phivc, qrest, tau, eta, rfonct_ecs, qcef: dict[(poste, energie)] -> Wh

    class Generateur:              # contrat des fiches 8.18 à 8.28
        def pas(self, h, qreq: dict[poste -> Wh], theta_aval: dict[poste -> °C], theta_amb, iecs_seule, rpuis_dispo=1.0) -> Resultat

1. Effet joule (8.18), classe EffetJoule(pmax_w = 1000 x Pmax, rdim, fonction) ; aucun état :
    pas(): for poste in qreq (1 ou 3 seulement) :
        qfou = min(qreq[poste], pmax_w x rdim x th)          # (1068), Rdim : Rdim générateurs identiques
        qcons = qfou ; qrest = qreq - qcons                  # (1068), (1069)
        tau = qfou / (pmax_w x rdim) ; rfonct_ecs = tau si poste == 3     # (1070), (1072)
        waux = 0 ; phivc = 0 ; eta = 1                       # (1066), (1071)
        qcef[(poste, 50)] = qcons                            # tableau 114

2. Chaudière (8.19), classe Chaudiere ; préprocesseur :
    pcsi = PCSI[idengen] (gaz : GPL si saisi) ; theta_min = {classique 40, condensation 30, bois 70}
    statut -> r_pn, r_pint = saisis x {1, 0,9, 0,8} ou (1073), (1074) par défaut ; contrôle « sur PCS >= 1 »
    q_po_30 = saisi ou (1075) ; wveille = saisi ou 20 ; waux_nom, waux_int = saisis ou (1077), (1078) (bois : colonne Alim_Chaudiere_Bois)
    alpha_nom, t_ref_nom, alpha_int, t_ref_int = tableau 121 ; p_arret = tableau 122[idpertes_parois] ; p_fonct = 0,25 bois sinon 0,30
    états conservés d'une heure à l'autre : qfou_ch_prev, qfou_ecs_prev, rfonct_ecs_prev, theta_cr_ch_prev, theta_cr_ecs_prev
    pas():
        def r_pn_t(t): r_pn + alpha_nom x (t_ref_nom - t)   ; def r_pint_t(t): r_pint + alpha_int x (t_ref_int - t)      # (1079), (1080)
        def stab(t): max(0, q_po_30 x ((t - theta_amb)/30) ** 1,25)                                                       # (1081)
        def service(poste, qreq_p, theta_p, plafond):       # plafond = 1 en ECS, rpuis_dispo en chauffage
            t_cr = max(theta_p, theta_min)                                                     # (1084)
            p_nom = 1000 x r_pn_t(t_cr) / r_pn x pn_gen ; p_int = 1000 x r_pint_t(t_cr) / r_pint x p_int_kw      # (1083), (1087)
            qfou = min(plafond x p_nom x th, qreq_p / rdim)                                    # (1082), (1100)
            phi_int = (100 / r_pint_t(t_cr) - 1) x p_int ; phi_nom = (100 / r_pn_t(t_cr) - 1) x p_nom     # (1088), (1089)
            if qfou == 0: pertes, waux selon les cas d'arrêt (1090 à 1092 en ECS si iecs_seule ; 1105 à 1110 en chauffage)
            elif qfou <= p_int x th: fx = qfou / (p_int x th) ; pertes = (fx x phi_int + (1 - fx) x stab(t_cr)) x th ; waux = (fx x waux_int + (1 - fx) x wveille) x th   # (1093 à 1095)
            else: fx = (qfou - p_int x th) / ((p_nom - p_int) x th) ; pertes = (fx x phi_nom + (1 - fx) x phi_int) x th ; waux = (fx x waux_nom + (1 - fx) x waux_int) x th   # (1096 à 1098)
            qcons = (qfou + pertes) / pcsi si qfou > 0 sinon pertes                            # (1099), (1091), (1109)
            return qfou, pertes, qcons, waux, p_nom, t_cr
        # ordre imposé : ECS d'abord
        ecs = service(3, qreq[3], theta_aval[3], 1.0) ; rfonct_ecs = ecs.qfou / (ecs.p_nom x th) si ecs.qfou > 0 sinon 0   # (1085)
        rpuis = 1 - rfonct_ecs                                                                  # (1102)
        ch = service(1, qreq[1], theta_aval[1], rpuis)
        tau_ch = ch.qfou / (rpuis x ch.p_nom x th) si rpuis > 0 sinon 0                        # (1103)
        qfou = ch.qfou + ecs.qfou ; qcons = ... ; waux = ... ; pertes = ...                     # (1111 à 1114)
        tau = rfonct_ecs + rpuis x tau_ch ; eta = qfou / qcons si qcons > 0 sinon 0            # (1115), (1117)
        qcef[(3, idengen)] = ecs.qcons ; qcef[(3, 50)] = ecs.waux ; qcef[(1, idengen)] = ch.qcons ; qcef[(1, 50)] = ch.waux   # (1118)
        phivc = pos_gen x ((p_fonct si qfou > 0 sinon p_arret) x pertes + waux)                # (1119)
        toutes les énergies x rdim ; qrest par poste = qreq - qfou x rdim                       # (1086), (1104)
        mémoriser qfou_ch_prev, qfou_ecs_prev, rfonct_ecs_prev, t_cr_ch_prev, t_cr_ecs_prev

3. Autres générateurs gaz (8.20), classe CombustionGaz(idtype 103 à 109) ; préprocesseur : theta_min (20 par défaut, eau seulement), pcsi, rpn/rpint (statut : certifié, justifié -10 %, déclaré min(0,8 x, 86 / 81 %), défaut (1122), (1123)), qpo30 = saisi ou (1124) x 1000, waux_nom = saisi ou (1125), wveille (+ veilleuse / 2,58), fmaj (tableaux 130, 131), p_arret, p_fonct = 0,30 ;
    états : ida_prev (0, 1, 3), rfonct_ecs_prev, qp0_prev
    pas():
        ida = 0 ; idfonction = poste demandé (ECS d'abord, puis chauffage)                      # (1126)
        t_corr = max(theta_aval, theta_min) si fluide eau                                        # (1120)
        qp0 = 100 x qpo30 / rpn x (max(0, t_corr - theta_amb)/30) ** 1,25 si eau sinon 0        # (1128), (1129)
        qreqact = qreq / rdim                                                                    # (1141)
        if qreq > 0: ida = idfonction                                                            # (1127)
            if idfonction == 3 (104, 105): pmax = pngen_w ; qfouact = min(qreqact, pmax) ; tau = qfouact / pmax ; rfonct_ecs = tau ; eta_pct = rpn   # (1139 à 1144)
                qpx = (100 - eta_pct / pcsi) x qfouact x pcsi / eta_pct + iecs_seule x (1 - rfonct_ecs) x qp0        # (1145)
                qconsact = qfouact / (eta_pct / 100) + iecs_seule x (1 - rfonct_ecs) x qp0                             # (1146), % lu en fraction
                wauxact = rfonct_ecs x waux_nom + iecs_seule x (1 - rfonct_ecs) x wveille                             # (1147)
            elif idtype in (106, 107): calcul chaudière gaz (bloc 2) avec rpn, rpint constants, pmax = pngen_w            # (1130 à 1132)
            else (103, 108, 109): pmax = pngen_w ; qfouact = min(rpuis_dispo x pmax, qreqact) ; tau = qfouact / (rpuis_dispo x pmax)
                qpx = fmaj x (100 - rpn / pcsi) x qfouact x pcsi / rpn ; eta_pct = qfouact / (qfouact + qpx) x 100 x pcsi ; qconsact = qfouact / eta_pct x 100   # (1135 à 1137)
                wauxact = rpuis_dispo x (tau x (waux_nom - wveille) + wveille)                                           # (1138)
            qp0_prev = qp0                                                                       # (1166)
        else (arrêt): qfouact = tau = 0 ; eta_pct = 0                                            # (1148 à 1150)
            chauffage : idraccord 0 -> (1151) ; idraccord 1 -> (1154) ; wauxact = rpuis_dispo x wveille (1157)
            ECS (iecs_seule) : idraccord 0 -> (1158), (1159) ; idraccord 1 -> (1161) ; wauxact = wveille (1164)
            qconsact = qpx                                                                       # (1152), (1155), (1159), (1162)
        phithreact = pos_gen x (qpx x (p_fonct si ida > 0 sinon p_arret) + wauxact)              # (1165)
        qcons = qconsact x rdim ; waux = wauxact x rdim ; qfou = qfouact x rdim ; phivc = phithreact x rdim ; qrest = qreq - qfou ; eta = eta_pct / 100   # (1167 à 1173)
        qcef[(idfonction, 10)] = qcons ; qcef[(idfonction, 50)] += waux                         # (1169)
        ida_prev = ida ; rfonct_ecs_prev = rfonct_ecs

4. Poêle ou insert bois (8.22), classe Poele(pngen_kw, eta_n_pct, paux_vent, rdim) ; sans état :
    q_ls_100 = 1000 x pngen x (100 / eta_n - 1)                                                  # (1229), une fois
    pas(): qreqact = qreq[1] / rdim ; qfouact = min(qreqact, 1000 x pngen) ; tau = qfouact / (1000 x pngen)    # (1226 à 1228)
        phith = tau x q_ls_100 ; qconsact = qfouact + phith                                       # (1231), (1232)
        qfou = rdim x qfouact ; qcons = rdim x qconsact ; waux = rdim x tau x paux_vent ; phivc = 0 ; eta = qfouact / qconsact ; qrest = qreq - qfou   # (1233 à 1238)
        qcef[(1, 40)] = qcons ; qcef[(1, 50)] = waux                                              # tableau 143

5. Réseau de chaleur ou de froid (8.28), classe SousStation(idtype, pess_kw, bss, dss, theta_prs, rdim) ; sans état :
    hss = bss x (1000 x pess) ** (1/3)                                                            # (1474), une fois
    pas(): pour chaque poste demandé (ECS puis chauffage, Rpuisdispo = 1 - rfonct_ecs comme en 8.19 ; froid pour 601) :
        qreqact = qreq / rdim ; qfouact = min(qreqact, rpuis x pess x 1000) ; qfou = rdim x qfouact ; tau = qfouact / (rpuis x pess x 1000)   # (1468 à 1471)
        theta_ss = dss x theta_prs + (1 - dss) x theta_aval                                       # (1475), (1476)
        pertes = 0 si idtype == 601 ; sinon chauffage : rpuis x hss x (theta_ss - theta_amb) ; ECS : hss x (theta_ss - theta_amb) x (1 si iecs_seule sinon rfonct_ecs)   # (1472), (1483), (1484)
        qcons = qfou + rdim x pertes ; eta = qfou / qcons ; qrest = qreq - qfou ; waux = 0 ; phivc = 0   # (1473), (1477) à (1481)
        qcef[(poste, 60)] = qcons                                                                 # tableau 250

6. Après la boucle horaire : sommes par (poste, énergie) -> kWh/m² SREF pour le banc ; histogramme de tau en 10 classes plus « charge nulle » et « hors fonctionnement » pour reproduire Nbhcharge_* de Sortie_Generateur ; compteur des heures où qrest > 0 en ECS (NbReports_ECS).
```

## Sorties RSEE pour le banc

- `O_Cef_ch_elec_annuel, O_Cef_ch_gaz_annuel, O_Cef_ch_fioul_annuel, O_Cef_ch_bois_annuel, O_Cef_ch_reseau_annuel` (Sortie_Groupe_C, kWh ef / m² SREF par an (vérifié : O_Cef_ch_elec_annuel = O_Cef_ch_annuel = 4,0 pour un groupe tout électrique))
- `O_Cef_ecs_elec_annuel, O_Cef_ecs_gaz_annuel, O_Cef_ecs_fioul_annuel, O_Cef_ecs_bois_annuel, O_Cef_ecs_reseau_annuel` (Sortie_Groupe_C, kWh ef / m² par an)
- `O_Cef_fr_elec_annuel, O_Cef_fr_gaz_annuel, O_Cef_fr_reseau_annuel` (Sortie_Groupe_C, kWh ef / m² par an (réseau de froid 601))
- `O_Cef_ch_mois, O_Cef_ecs_mois, O_Cef_fr_mois` (Sortie_Groupe_C (Sortie_Mensuelle), kWh ef / m² par mois, pour contrôler la saisonnalité des pertes à l'arrêt)
- `O_B_Ch_annuel, O_B_Ecs_annuel, O_B_Fr_annuel` (Sortie_Groupe_C, kWh / m² : besoins aux émetteurs, pour isoler rendement + pertes de distribution (ratio Cef/B = 0,30 sur le groupe PAC + joule observé))
- `O_Cef_aux_distribution_annuel` (Sortie_Groupe_C, kWh ef / m² : auxiliaires de distribution, hors Waux,pro des générateurs (à vérifier au banc : Waux,pro des chaudières devrait tomber dans O_Cef_ch_elec_annuel selon 1118))
- `O_Cef_elec_cons_ch_annuel, O_Cef_elec_cons_ecs_annuel, O_Cef_gaz_imp_ch_annuel, O_Cef_gaz_imp_ecs_annuel, O_Cef_fioul_imp_*, O_Cef_bois_imp_*, O_Cef_reseau_imp_ch_annuel, O_Cef_reseau_imp_ecs_annuel, O_Cef_reseau_imp_fr_annuel` (Sortie_Zone_C, kWh ef / m² par an (et _mois))
- `O_Cef_elec_imp_ch_annuel, O_Cef_elec_imp_ecs_annuel, O_Cef_gaz_imp_ch_annuel, O_Cef_reseau_imp_ch_annuel, O_Cef_boisbuchchaud_imp_ch_annuel, O_Cef_boisgranchaud_imp_ch_annuel, O_Cef_boisplaqchaud_imp_ch_annuel, O_Cef_boisbuchpoel_imp_ch_annuel, O_Cef_boisgranpoel_imp_ch_annuel, O_Cef_boisplaqpoel_imp_ch_annuel` (Sortie_Batiment_C, kWh ef / m² par an ; les six sorties bois distinguent chaudière (chaud) et poêle (poel) par combustible : banc direct des fiches 8.19 bois et 8.22)
- `O_Cef_Ch_comb_bat, O_Cef_ECS_comb_bat` (Sortie_Batiment_C, kWh ef (combustibles, à confirmer) ; 0 sur le bâtiment tout électrique)
- `generateur_principal_ch, generateur_principal_ecs, generateur_principal_fr, vecteur_energie_principal_ch` (Sortie_Batiment_C, codes (vus : generateur_principal_ecs 513, vecteur_energie_principal_ch 11) : filtre du banc par type de générateur)
- `O_Type_Reseau, O_RatENR_rdch` (Sortie_Batiment_C, code du réseau et part ENR du réseau de chaleur (pour le Cep nr, 2488 à 2490))
- `Nbhcharge_0_ch, Nbhcharge_0_10_ch ... Nbhcharge_90_100_ch, Nbhcharge_HF_ch (idem _fr et _ECS)` (Sortie_Generation/Sortie_Generateur, heures (somme 8760) : histogramme de τcharge en classes de 10 %, charge nulle et hors fonctionnement ; banc direct de Pmax et de τcharge (1070, 1115, 1143))
- `Q_fou_3_postes` (Sortie_Generateur, énergie fournie Qfou cumulée sur les trois postes, kWh (unité déduite des ordres de grandeur : 3801 pour une PAC de logement collectif, 24,7 pour son appoint joule))
- `NbReports_ECS` (Sortie_Generateur, nombre d'heures avec Qrest,ECS > 0 reporté (6472 vu sur une PAC ECS) : banc de 1069, 1086, 1172)
- `IsChaudiereGaz, IsReliePrechauffageCW` (Sortie_Generateur, booléens : repérage des chaudières gaz dans le banc)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch, O_Idsousdim_Court_Fr, O_Idsousdim_Long_Fr` (Sortie_Generation, 0/1 : sous-dimensionnement déduit de Qrest par la fiche 8.29)

## Points ouverts (à trancher au codage)

- Unité et sens de Pmax dans Generateur_Effet_Joule : la fiche donne Pngen en W (page 668), le RSEE porte 100 (appoints de PAC) et 2 (sèche-serviettes) : lecture kW retenue. Les appoints à 100 kW sont peut-être une valeur « illimitée » saisie par le logiciel. Banc : Nbhcharge_90_100_ch du Sortie_Generateur du générateur joule (12 heures à pleine charge pour l'appoint de rsee_a, donc Pmax n'est pas illimité) et O_Idsousdim_Court_Ch.
- Les RSEE du banc portent les balises Generateur_Combustion (84 fichiers) et Reseau_Chaleur (3 fichiers) : leurs champs n'ont pas été lus (limite de deux RSEE, aucun des deux n'en contient). Il faut relever sur un RSEE à chaudière les noms correspondant à idtype, R_pn, R_pint, Waux_nom, Waux_int, Wveille, Q_po_30, statuts, idpertes_parois, TypeCombustibleBois, et sur un RSEE à réseau ceux de PEss, Type_Reseau, classes d'isolation. Les poêles (type 401) sont peut-être aussi portés par Generateur_Combustion.
- Rendements sur PCS ou sur PCI : la nomenclature 8.19 (page 673) dit « rendement sur PCS », les formules 1073 et 1074 divisent par PCSI et par 100, 1099 divise (Qfou + Qpertes) par PCSI, et la fiche 8.20 parle de rendement PCI avec le test MAX(Rpn ; Rpint)/PCSI >= 1. Lecture retenue : R saisi sur PCI en %, pertes calculées sur PCI, puis 1099 divise par PCSI (ce qui suppose en fait R sur PCS). Banc : O_Cef_gaz_imp_ch_annuel d'un bâtiment à chaudière gaz condensation, écart attendu de 11 % entre les deux lectures.
- Formule 1073 : le rendu « c1 + c2.log(Pn) / 100.PCSI » peut se lire (c1 + c2 log Pn)/(100 PCSI) (fraction) ou c1 + c2 log(Pn)/(100 PCSI) (pourcentage). La première donne 0,85 pour une chaudière gaz de 20 kW, cohérent avec un rendement sur PCS en fraction, mais 1079 attend des %. Banc : même sortie, cas d'une chaudière aux valeurs par défaut.
- 1094 et 1097 écrivent Waux_min et Wveille pour les deux plages de charge ; lecture retenue par continuité : Waux_int et Wveille sur la plage tout ou rien, Waux_nom et Waux_int sur la plage de modulation. Effet au banc : O_Cef_ch_elec_annuel d'un bâtiment à chaudière (auxiliaires seuls en électricité).
- 1105 : à l'arrêt en chauffage avec Rpuisdispo < 1, la perte est Rpuisdispo x φthstab(θaval,cr_ecs(h)) alors que 1107 utilise Rfonct,ecs(h-1) ; la convention « la chaudière est chaude pendant la part d'heure restante » est retenue telle quelle.
- 1103 et 1116 emploient Pmax,ch et Pmax,ecs non définis dans la fiche ; lus comme Pth,nom,ch(h) x th et Pth,nom,ecs(h) x th.
- 1146 : Qconsact = Qfouact / ηeff_% avec ηeff_% en pourcentage donnerait une consommation 100 fois trop faible ; lu comme Qfouact x 100 / ηeff_%, cohérent avec 1137.
- Les équations des fiches 8.22 (1226 à 1238) et 8.28 (1468 à 1484) sont des images dans le PDF ; elles ont été reconstruites à partir des fragments de texte (variables dans l'ordre) et de la norme EN 15316-4-5 citée. À confirmer sur O_Cef_boisbuchpoel_imp_ch_annuel (poêle bûches) et O_Cef_reseau_imp_ch_annuel (3 fichiers réseau du banc).
- Réseau de chaleur : la fiche ne dit pas comment la colonne de Bss (classes d'isolation 4/5, 3/4, 2/3, 1/2) et la ligne (type de réseau) sont saisies ; le champ Type_Reseau vu dans deux en-têtes et la sortie O_Type_Reseau devraient porter le type. θamb de la sous-station hors volume chauffé (Pos_Gen = 0) vient de la fiche de la génération (hors lot).
- Température aval θaval,CH et θaval,ECS : fournies par la gestion/régulation de la génération (fiche 8.30, hors lot) à partir de Theta_Wm_Ch (70 °C vu), Theta_Wm_Ecs (50 ou 54) et Type_Gestion_Chaud_Gen (loi d'eau 2) ; sans cette fiche, le banc des chaudières ne peut être mené qu'avec θaval = Theta_Wm_* constant, ce qui surestime les pertes des chaudières à condensation.
- Qreq reçu par le générateur inclut les pertes de distribution primaire et secondaire, les ballons et les priorités entre générateurs (Idpriorite_Ch/Ecs, Type_Priorite 1 ou 2) : hors lot. Le banc par groupe de l'effet joule n'est possible que sur les bâtiments où la distribution est à pertes nulles (O_Cef_aux_distribution_annuel = 0 et émetteurs directs), comme les 18 projets joule ciblés.
- Le texte ne dit pas si Qrest d'un générateur effet joule reporté « au pas de temps suivant » s'ajoute au Qreq de h+1 ou est perdu : c'est la fiche 8.29 qui tranche ; NbReports_ECS et O_Idsousdim_* permettent de le voir au banc.
- Tableaux illisibles ou partiellement lisibles en texte : équation 1070 (page 670), figure 113 (page 681), tableau 127 (page 694, cases grisées sans valeur), équations 1226 à 1238 (pages 723 et 724), équations 1468 à 1484 (pages 914 à 917). Les tableaux 114, 134, 143, 250 (matrices Qcef) sont lisibles mais vides par construction.
- Sortie_Generateur ne porte pas Qcons ni Waux par générateur : le banc des rendements ne peut se faire qu'au niveau groupe/zone/bâtiment par énergie, donc sur des bâtiments à générateur unique par poste.

## Tableaux en image dans le PDF


## Estimation

Environ 750 lignes de Python dans un module openbce/generateurs.py, plus 150 lignes de banc (banc/generation.py) : effet joule 40 lignes (difficulté nulle, aucune ambiguïté de texte, à livrer en premier avec un banc sur O_Cef_ch_elec_annuel des 18 projets) ; chaudières 8.19 environ 250 lignes (difficulté moyenne : double service avec ECS prioritaire, cinq états à conserver d'une heure à l'autre, statuts et valeurs par défaut, trois ambiguïtés de texte dont PCS/PCI qui pèse 11 % sur le gaz) ; autres générateurs gaz 8.20 environ 200 lignes (difficulté moyenne : six sous-types, états ida_fonctionne et Qp0prev, deux modes de raccordement) ; poêles 8.22 environ 60 lignes (faible) ; réseaux 8.28 environ 120 lignes (faible, formules reconstruites à confirmer sur 3 fichiers). Tables conventionnelles 117 à 131, 248, 249 : 80 lignes de constantes. La difficulté principale n'est pas dans ces fiches mais en amont : sans la fiche 8.30 (gestion/régulation : Qreq, θaval, Rpuis_dispo, iECS_seule, priorités) et les distributions, seul l'effet joule à distribution directe est bancable immédiatement ; chaudières et réseaux attendent le lot génération. Compter 2 jours pour le code et les tests unitaires de la famille, 1 jour de banc effet joule, le banc des chaudières étant conditionné par le lot amont et par la lecture des champs de Generateur_Combustion sur un RSEE autorisé.
