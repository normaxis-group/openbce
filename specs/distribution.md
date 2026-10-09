# Spécification : Distribution de chauffage et de refroidissement

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

Famille « Distribution de chauffage et de refroidissement » : tout ce qui se passe entre la demande d'énergie des émetteurs d'un groupe (Qsys_ch_em(h), Qsys_fr_em(h), sorties de la fiche 8.1 C_Emi, équation 825 p. 506) et la demande transmise à la génération (Qsys_ch_dp(h), Qsys_fr_dp(h), θmoy_dp(h), θdep_dp(h), irelance_dp(h), entrées de la fiche 8.14 S1_Syst_Assemblage de la génération, p. 608, qui les transforme en Qreq,ch gen,gr(h)).

Couvert, dans l'ordre de l'arborescence (fiche 8.6, p. 545 et 546) :
1. Gestion/régulation de la distribution du groupe (fiche 8.7, p. 548 à 559, équations 851 à 872) : indicateur de fonctionnement, débit requis et effectif, chute de température dans les émetteurs, température de départ selon trois modes (constante, retour constant, loi d'eau sur l'extérieur), température de retour, coefficients Modpertes et Modcirc, relance.
2. Distribution du groupe (fiche 8.8, p. 560 à 566, équations 873 à 888) : température moyenne, pertes en volume chauffé (récupérables) et hors volume chauffé (vers un espace tampon ou l'extérieur), énergie du circulateur, part récupérable, demande augmentée Qsys_ch_ds.
3. Gestion/régulation de la distribution intergroupes (fiche 8.9, p. 567 à 581, équations 889 à 919 : cette fiche n'était pas dans la liste fournie mais elle est indispensable, c'est elle qui porte l'héritage départ = max, débit = somme, retour = moyenne pondérée, intermittence = max, ainsi que les ratios de surface et de besoin utilisés par la génération et par la fiche 11.1).
4. Distribution intergroupes (fiche 8.10, p. 582 à 588, équations 920 à 937) : mêmes pertes avec ambiance conventionnelle 20 °C en chaud, 26 °C en froid, circulateur primaire non récupérable, demande Qsys_ch_dp.
5. Classement en ou hors volume chauffé (fiche 8.13, p. 602 à 604) : règle de saisie uniquement, aucune équation ; elle justifie la répartition Lvc / Lhvc saisie dans le RSEE et exclut les planchers chauffants.
6. Attribution des pertes et consommations récupérables aux groupes (fiche 11.1 C_PER, p. 1298 à 1304, équations 2357, 2359, 2361, 2364 à 2366), pour la seule part issue des distributions de chaud et de froid : nécessaire pour boucler sur le groupe au pas suivant.

Hors champ, et pourquoi :
- Réseaux de distribution de CTA (fiches 8.11 et 8.12, équations 938 à 957, nœud Distribution_CTA_Chaud sous Ventilation_Mecanique) : ils partent du composant CTA (préchauffage, antigel, humidification), pas des émetteurs ; les processus horaires sont « exactement similaires » à la fiche 8.7 (p. 596) donc le code écrit ici est réutilisable, mais la demande d'entrée vient d'un module CTA qui n'existe pas encore.
- Distribution d'ECS (Distribution_Groupe_ECS, Distribution_Intergroupe_ECS, chapitre 9) : autre famille, bouclage sur le ballon et pertes à 60 % (p. 1303).
- Distribution_Rafraichissement_Direct (sous Generation) et Emission_Rafraichissement_Direct : géocooling, fiche propre.
- Génération (8.14 et suivantes) : consomme Qsys_ch_dp, θmoy_dp, θdep_dp, irelance_dp, Adess, Ratbes_prim ; la présente spécification s'arrête à la production de ces sorties.
- Ventilateurs locaux des émetteurs (Wvent_loc, Φvent_loc, fiche 8.1) : cités dans l'assemblage 8.6 mais calculés dans l'émission.
- Émetteurs à batterie sur air soufflé (idv_air_ds = 1, équation 900) : la température d'air soufflé vient du module ventilation double flux ; on code le cas idv_air = 0 et on laisse le branchement.
- Vérifications de cohérence de montage (851, 852, 896, 897, 901, 902, 910, 911 : θmax_ch, θmin_fr, idfonction = idfonction_dp) : à coder en contrôle de saisie, sans effet sur les flux.

## Entrées (RSEE)

- `Distribution_Groupe_Chaud (sous Groupe/Emetteur_Collection/Emetteur ; un seul par émetteur chaud)` / `Index` : identifiant ds ; entier ; valeurs vues : 1 à 12
- `Distribution_Groupe_Chaud` / `Type_2nd` : idtype (8.7 p. 549, 8.8 p. 562) ; entier 0/1 ; valeurs vues : 0 (fictif) dans les deux RSEE lus ; 1 attendu pour un réseau hydraulique
- `Distribution_Groupe_Chaud` / `Lvc` : Lvc longueur en volume chauffé (8.8 p. 561) ; réel, m ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Lhvc` : Lhvc longueur hors volume chauffé (8.8 p. 561) ; réel, m ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Q2nd_Resid` : qresid débit résiduel (8.7 p. 550) ; réel, m³/h ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Id_Et` : espace tampon qui fournit btherm(h) (8.8 p. 561) ; 0 : réseau hors volume chauffé donnant sur l'extérieur, btherm = 1 (même convention que parois.py et enveloppe.coefficients_b) ; entier ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Id_Dist_1re` : Index du Distribution_Intergroupe_Chaud parent (lien ds -> dp, cohérence 851, 852) ; entier ; valeurs vues : 1, 4, 5, 6, 7, 8
- `Distribution_Groupe_Chaud` / `Id_Ballon` : hors champ (ECS) ; absent du nœud Froid ; entier ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Gest_2nd_Ch` : idgest_ch mode de régulation de température : 1 départ constant, 2 retour constant, 3 loi d'eau (8.7 p. 550, équations 860 à 862) ; entier 1 à 3 ; valeurs vues : 0 (fictif)
- `Distribution_Groupe_Chaud` / `Mode_Reg_Debit_Ch` : iddebit_ch : 1 débit constant continu, 2 débit constant intermittent, 3 débit variable (8.7 p. 549, équations 856 à 858) ; entier 1 à 3 ; valeurs vues : 0 (fictif)
- `Distribution_Groupe_Chaud` / `Theta_Dep_Dim_Ch` : θdep_dim_ch (8.7 p. 550) ; réel, °C ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Theta_Ret_Dim_Ch` : θret_dim_ch ; réel, °C ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Delta_Theta_Em_Dim_Ch` : Δθem_dim_ch (positif en chaud) ; réel, K ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Qnom_Ch` : qnom_ch ; réel, m³/h ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Umoyen_Vc_Ch` : Umoyen_vc_ch (8.8 p. 562) ; réel, W/(m.K) ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Umoyen_Hvc_Ch` : Umoyen_hvc_ch ; réel, W/(m.K) ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Gest_Circ_2nd_Ch` : idcirc_ch : 0 pas de circulateur, 1 vitesse constante, 2 Δp constante, 3 Δp réduite (8.7 p. 550, équation 863) ; entier 0 à 3 ; valeurs vues : 0
- `Distribution_Groupe_Chaud` / `Pcirculateur_Ch` : Paux_ch puissance du circulateur du groupe (8.8 p. 562) ; réel, W ; valeurs vues : 0
- `Distribution_Groupe_Froid (sous Emetteur ; un seul par émetteur froid)` / `Type_2nd, Lvc, Lhvc, Q2nd_Resid, Id_Et, Id_Dist_1re, Gest_2nd_Fr, Mode_Reg_Debit_Fr, Theta_Dep_Dim_Fr, Theta_Ret_Dim_Fr, Delta_Theta_Em_Dim_Fr, Qnom_Fr, Umoyen_Vc_Fr, Umoyen_Hvc_Fr, Gest_Circ_2nd_Fr, Pcirculateur_Fr` : idtype, Lvc, Lhvc, qresid, btherm, lien dp, idgest_fr, iddebit_fr, θdep_dim_fr, θret_dim_fr, Δθem_dim_fr, qnom_fr, Umoyen_vc_fr, Umoyen_hvc_fr, idcirc_fr, Paux_fr ; mêmes types que le nœud Chaud ; valeurs vues : tout à 0 sauf Delta_Theta_Em_Dim_Fr = -1 et Id_Dist_1re = 2 : la convention RSEE donne Δθem_dim_fr négatif, cohérente avec la note p. 579 « a une valeur négative »
- `Distribution_Intergroupe_Chaud (racine Entree_Projet/Distribution_Intergroupe_Chaud_Collection)` / `Index` : identifiant dp, cible des Id_Dist_1re ; entier ; valeurs vues : 1, 4, 5, 6, 7, 8
- `Distribution_Intergroupe_Chaud` / `Type_Prim` : idtype : 0 fictif, 1 hydraulique collectif, 2 réseaux hydrauliques individuels uniquement (8.9 p. 569) ; entier 0 à 2 ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Lvc_Prim` : Lvc (8.10 p. 583) ; réel, m ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Lhvc_Prim` : Lhvc ; réel, m ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Id_Gen` : Index de la Generation desservie (8.10 p. 582 : une et une seule génération) ; entier ; valeurs vues : 1 à 6
- `Distribution_Intergroupe_Chaud` / `Id_Et` : espace tampon pour btherm(h) (8.10 p. 583) ; entier ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Umoyen_Vc_Prim_Ch` : Umoy_vc_ch (8.10 p. 584) ; réel, W/(m.K) ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Umoyen_Hvc_Prim_Ch` : Umoy_hvc_ch ; réel, W/(m.K) ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Gest_Circ_Prim_Ch` : idcirc_ch du réseau intergroupes (8.9 p. 569, équation 909) ; entier 0 à 3 ; valeurs vues : 0
- `Distribution_Intergroupe_Chaud` / `Pcirc_Prim_Ch` : Paux_ch intergroupes (8.10 p. 584) ; réel, W ; valeurs vues : 0
- `Distribution_Intergroupe_Froid (racine)` / `Type_Prim, Lvc_Prim, Lhvc_Prim, Id_Gen, Id_Et, Umoyen_Vc_Prim_Fr, Umoyen_Hvc_Prim_Fr, Gest_Circ_Prim_Fr, Pcirc_Prim_Fr` : idem Chaud en froid ; aucun champ de gestion de température ni de débit au niveau intergroupes : tout est hérité des réseaux du groupe (8.9 p. 567) ; idem Chaud ; valeurs vues : tout à 0, Id_Gen = 1
- `Emetteur (sous Groupe)` / `Is_emetteur_chaud, Is_emetteur_froid` : présence du couple réseau chaud / réseau froid (8.7 p. 548 : un émetteur réversible porte les deux nœuds) ; entier 0/1 ; valeurs vues : 1/0, 1/1
- `Emetteur` / `Rat_s_ch, Rat_t_ch, Rat_s_fr, Rat_t_fr` : Rateff_ch_gr,em = Rat_s x Rat_t (8.1, équations 797, 798) : part de la demande du groupe portée par l'émetteur, donc par son réseau ds, et surface desservie Rateff x Agr (891, 892) ; réels 0 à 1 ; valeurs vues : déjà lus par emission.py
- `Emetteur` / `Per_dos` : Pper, pertes au dos, déjà incluses dans Qsys_ch_em amont (8.1 p. 1356) ; réel ; valeurs vues : lu par emission.py
- `Groupe` / `SU ou SHAB` : Agr surface utile du groupe (8.6 p. 543, 8.9 équations 891 à 893) ; réel, m² ; valeurs vues : -
- `Groupe` / `Type_Pgrm_Ch, Type_Pgrm_Fr` : source de irelance_gr(h) (consigne de relance de emission.relance ; irelance = 1 quand la consigne de relance dépasse la consigne programmée), équation 853 ; entier ; valeurs vues : 1
- `Batiment/Espace_Tampon_Non_Solarise` / `coefficient b (déjà lu par enveloppe.coefficients_b)` : btherm(h) (8.8 p. 561) ; constant dans l'année dans openBCE ; réel ; valeurs vues : -
- `Météo (climat.du_site)` / `te[h], base_ext` : θext(h), θext_base (8.7 p. 549) ; réels, °C ; valeurs vues : -
- `Sortie du modèle thermique du groupe (groupe.calculer, variable ti_fin / fin.i)` / `-` : θi,moy_gr(h) température d'air moyenne du groupe après croisement (8.7 p. 549) ; le texte prend la moyenne sur le pas, openBCE expose la valeur de fin de pas : prendre t.i moyen si disponible, sinon fin.i ; réel, °C ; valeurs vues : -

## Paramètres conventionnels

- ρeau masse volumique de l'eau = 998 kg/m³ (p. 551 (tableau 96) et 593)
- Cp_eau capacité thermique massique = 1,163 Wh/(kg.K) ; produit ρ.Cp = 1160,7 Wh/(m³.K) (p. 551 et 593)
- θext_lim_ch limite extérieure de la loi d'eau = 15 °C (non saisi dans le RSEE) (p. 550 et 591)
- θdep_ch_min température de départ minimale en loi d'eau = 20 °C (non saisi dans le RSEE) (p. 550 et 591)
- Pcirc_vc part de l'énergie du circulateur du groupe transmise à l'ambiance = 0,5 (p. 562, confirmé 565 et 566 (« Pcirc_amb = 50 % »))
- Pcirc_vc part de l'énergie du circulateur intergroupes transmise à l'ambiance = 0 (p. 584, confirmé 587 et 588)
- θvc_ch = θamb_ch ambiance équivalente du réseau intergroupes en chauffage = 20 °C (p. 584 et 571)
- θvc_fr = θamb_fr ambiance équivalente du réseau intergroupes en refroidissement = 26 °C (p. 584 et 571)
- θdep à l'arrêt du réseau intergroupes = θamb_ch (20 °C) en chaud, θamb_fr (26 °C) en froid (p. 576 (906) et 580 (917))
- Partrecup_dgr_chfr part récupérable des pertes des distributions du groupe = 1,0 (p. 1301 et 1303)
- Partrecup_dintgr_chfr part récupérable des pertes des distributions intergroupes = 0,6 (p. 1301 et 1303)
- Partrecup_circ_chfr part récupérable du flux des circulateurs (groupe et intergroupes) = 0,6 (p. 1301 et 1303)
- Partconv_autres part convective des flux récupérés = 0,5 (le reste radiatif) (p. 1301 et 1304)
- θmax_ch / θmin_fr d'un réseau fictif (contrôle de montage) = 0 °C / 100 °C (p. 574 (896, 897) et 596 (950, 951))
- Réseau fictif : toutes sorties horaires nulles = θdep = θret = 0 °C, Modpertes = Modcirc = 0, qeff = 0, fonct = 0 (p. 553 (854) et 574 (898))
- Émetteurs sans by-pass (retour = départ moins chute) = convention (p. 559)
- Puissance des émetteurs considérée infinie quelle que soit la température d'eau = convention (p. 555)

## Équations

- (851, p. 552) idfonction_ch(ds) = idfonction_ch(dp) ou idfonction_fr(ds) = idfonction_fr(dp) ; fonction du réseau du groupe et du réseau intergroupes parent (Id_Dist_1re) ; contrôle de saisie : un Distribution_Groupe_Chaud pointe un Distribution_Intergroupe_Chaud
- (852, p. 552) idtype(ds) = idtype(dp) ; Type_2nd, Type_Prim ; contrôle de saisie ; nuance 8.9 p. 574 : réseau hydraulique sans branche intergroupes = intergroupes hydraulique de longueur nulle sans circulateur (Type_Prim = 2)
- (853, p. 552) irelance_ds(h) = irelance_gr(h) ; indicateur de relance du groupe ; toujours
- (854, p. 553) θdep(h) = 0 ; θret(h) = 0 ; Modpertes(h) = 0 ; Modcirc(h) = 0 ; qeff(h) = 0 ; fonct(h) = 0 ; sorties du réseau du groupe ; idtype = 0 (réseau fictif : effet joule, générateurs d'air chaud, poêles, PAC à détente directe)
- (855, p. 554) fonct(h) = 1 si Qsys_ch_em(h) > 0, sinon 0 ; demande de l'émetteur associé ; idtype = 1, idfonction = 1
- (856, p. 554) qreq(h) = Qsys_ch_em(h) / (ρeau . Cp_eau . Δθem_dim_ch) ; qeff(h) = MAX(qreq(h) ; qresid) ; Δθem(h) = Qsys_ch_em(h) / (ρeau . Cp_eau . qeff(h)) ; Modpertes(h) = 1 ; Qsys en Wh sur 1 h, débits en m³/h, ρ.Cp = 1160,7 Wh/(m³.K) ; fonct(h) = 1 et iddebit_ch = 3 (débit variable)
- (857, p. 554) qreq(h) = qnom_ch ; qeff(h) = qnom_ch ; Modpertes(h) = MIN(1 ; Qsys_ch_em(h) / (ρeau . Cp_eau . qnom_ch . Δθem_dim_ch)) ; Δθem(h) = Δθem_dim_ch ;  ; fonct(h) = 1 et iddebit_ch = 2 (débit constant, fonctionnement intermittent)
- (858, p. 554) qreq(h) = qnom_ch ; qeff(h) = qnom_ch ; Modpertes(h) = 1 ; Δθem(h) = Qsys_ch_em(h) / (ρeau . Cp_eau . qnom_ch) ;  ; fonct(h) = 1 et iddebit_ch = 1 (débit constant, fonctionnement continu)
- (859, p. 554) qreq(h) = 0 ; qeff(h) = 0 ; Δθem(h) = 0 ; Modpertes(h) = 0 ;  ; fonct(h) = 0 (réseau à l'arrêt)
- (860, p. 555) θdep(h) = fonct(h) . θdep_dim_ch + (1 - fonct(h)) . θi,moy_gr(h) ;  ; idgest_ch = 1 (départ constant)
- (861, p. 555) θdep(h) = fonct(h) . (θret_dim_ch + Δθem(h)) + (1 - fonct(h)) . θi,moy_gr(h) ;  ; idgest_ch = 2 (retour constant)
- (862, p. 555 et 556 (figure 97)) Si fonct(h) = 1 : si θext(h) ≥ θext_lim_ch : θdep(h) = MAX(θdep_ch_min ; θi,moy_gr(h) + Δθem(h)) ; si θext(h) ≤ θext_base : θdep(h) = θdep_dim_ch ; sinon : θdep(h) = MAX(θi,moy_gr(h) + Δθem(h) ; θdep_dim_ch + (θdep_ch_min - θdep_dim_ch) . (θext(h) - θext_base) / (θext_lim_ch - θext_base)). Si fonct(h) = 0 : θdep(h) = θi,moy_gr(h) ; θext_lim_ch = 15, θdep_ch_min = 20, θext_base du site ; idgest_ch = 3 (loi d'eau, chauffage seulement) ; lecture reconstruite depuis les jetons, la borne MAX(.. ; θi + Δθem) garantit que l'eau est plus chaude que l'ambiance
- (863, p. 556) idcirc_ch = 0 : Modcirc(h) = 0 ; idcirc_ch = 1 : Modcirc(h) = Modpertes(h) ; idcirc_ch = 2 : Modcirc(h) = Modpertes(h) . (qeff(h) / qnom_ch)^(2/3) [lecture incertaine, exposant lu « 3 2 »] ; idcirc_ch = 3 : Modcirc(h) = Modpertes(h) . (0,5 . (qeff(h) / qnom_ch)^2 + 0,5 . (qeff(h) / qnom_ch)^3) [lecture incertaine, jetons « 3 2 2 0,5 0,5 »] ; note p. 556 : les circulateurs à vitesse variable ne sont pris en compte qu'avec un réseau à débit variable (iddebit = 3) ; sinon qeff = qnom et le facteur vaut 1 ; idtype = 1 ; voir point ouvert 1
- (864, p. 557) fonct(h) = 1 si Qsys_fr_em(h) > 0, sinon 0 ;  ; idtype = 1, idfonction = 2
- (865, p. 557) qreq(h) = Qsys_fr_em(h) / (ρeau . Cp_eau . |Δθem_dim_fr|) ; qeff(h) = MAX(qreq(h) ; qresid) ; Δθem(h) = Qsys_fr_em(h) / (ρeau . Cp_eau . qeff(h)) ; Modpertes(h) = 1 ; Δθem_dim_fr saisi négatif dans les RSEE (-1 vu) : prendre la valeur absolue pour les débits, voir point ouvert 3 ; fonct(h) = 1 et iddebit_fr = 3
- (866, p. 557) qreq(h) = qeff(h) = qnom_fr ; Modpertes(h) = MIN(1 ; Qsys_fr_em(h) / (ρeau . Cp_eau . qnom_fr . |Δθem_dim_fr|)) ; Δθem(h) = Δθem_dim_fr ;  ; fonct(h) = 1 et iddebit_fr = 2
- (867, p. 557) qreq(h) = qeff(h) = qnom_fr ; Modpertes(h) = 1 ; Δθem(h) = Qsys_fr_em(h) / (ρeau . Cp_eau . qnom_fr) ;  ; fonct(h) = 1 et iddebit_fr = 1
- (868, p. 558) qreq(h) = 0 ; qeff(h) = 0 ; Δθem(h) = 0 ; Modpertes(h) = 0 ;  ; fonct(h) = 0
- (869, p. 558) θdep(h) = fonct(h) . θdep_dim_fr + (1 - fonct(h)) . θi,moy_gr(h) ;  ; idgest_fr = 1
- (870, p. 558) θdep(h) = fonct(h) . (θret_dim_fr - Δθem(h)) + (1 - fonct(h)) . θi,moy_gr(h) ; Δθem(h) pris positif (échauffement de l'eau dans l'émetteur) ; pas de mode 3 en froid ; idgest_fr = 2
- (871, p. 558) identique à (863) avec idcirc_fr et qnom_fr ;  ; idtype = 1, idfonction = 2
- (872, p. 559) Si fonct(h) = 0 : θret(h) = θdep(h) (= θi,moy_gr(h), réseau sans débit). Sinon : θret(h) = θdep(h) - Δθem(h) en chauffage ; θret(h) = θdep(h) + Δθem(h) en refroidissement ; convention : émetteurs sans by-pass ; le texte n'écrit que le signe moins ; le signe plus en froid est déduit du sens physique, voir point ouvert 3
- (873, p. 564) idfonction = 1 : Qsys_ch_ds(h) = Qsys_ch_em(h), Qsys_fr_ds(h) = 0 ; idfonction = 2 : Qsys_ch_ds(h) = 0, Qsys_fr_ds(h) = Qsys_fr_em(h) ;  ; idtype = 0 (réseau du groupe fictif)
- (874, p. 564) Waux(h) = 0 ; Φpertes_vc(h) = 0 ; Φpertes_hvc(h) = 0 (et Φaux_vc(h) = 0) ;  ; idtype = 0
- (875, p. 565) θmoy(h) = (θdep(h) + θret(h)) / 2 ; longueurs départ et retour supposées égales ; idtype = 1, idfonction = 1 (le titre du paragraphe dit « idtype = 0 », coquille du texte)
- (876, p. 565) Φpertes_vc(h) = Modpertes(h) . Umoyen_vc_ch . Lvc . MAX(0 ; θmoy(h) - θi,moy_gr(h)) ; Wh sur 1 h, U en W/(m.K), L en m ; chauffage
- (877, p. 565) θhvc(h) = btherm(h) . θext(h) + (1 - btherm(h)) . θi,moy_gr(h) ; btherm du Id_Et, 1 si Id_Et = 0 ; chauffage et refroidissement (idem 884)
- (878, p. 565) Φpertes_hvc(h) = Modpertes(h) . Umoyen_hvc_ch . Lhvc . MAX(0 ; θmoy(h) - θhvc(h)) ;  ; chauffage
- (879, p. 565) Waux(h) = Modcirc(h) . Paux_ch . 1 h ; Paux_ch = Pcirculateur_Ch en W, résultat en Wh ; chauffage
- (880, p. 565) Φaux_vc(h) = Pcirc_vc . Waux(h), Pcirc_vc = 0,5 ;  ; chauffage (idem 887 en froid)
- (881, p. 565) Qsys_ch_ds(h) = Qsys_ch_em(h) + Φpertes_vc(h) + Φpertes_hvc(h) ; Qsys_fr_ds(h) = 0 ;  ; chauffage
- (882, p. 566) θmoy(h) = (θdep(h) + θret(h)) / 2 ;  ; idtype = 1, idfonction = 2
- (883, p. 566) Φpertes_vc(h) = Modpertes(h) . Umoyen_vc_fr . Lvc . MIN(0 ; θmoy(h) - θi,moy_gr(h)) ; valeur négative ou nulle telle qu'écrite (gain de chaleur par le réseau froid) ; refroidissement ; signe à trancher, voir point ouvert 2
- (884, p. 566) θhvc(h) = btherm(h) . θext(h) + (1 - btherm(h)) . θi,moy_gr(h) ;  ; refroidissement
- (885, p. 566) Φpertes_hvc(h) = Modpertes(h) . Umoyen_hvc_fr . Lhvc . MIN(0 ; θmoy(h) - θhvc(h)) ;  ; refroidissement
- (886, p. 566) Waux(h) = Modcirc(h) . Paux_fr . 1 h ;  ; refroidissement
- (887, p. 566) Φaux_vc(h) = Pcirc_vc . Waux(h), Pcirc_vc = 0,5 ;  ; refroidissement
- (888, p. 566) Qsys_ch_ds(h) = 0 ; Qsys_fr_ds(h) = Qsys_fr_em(h) + Φpertes_vc(h) + Φpertes_hvc(h) ; pour que la demande de froid augmente avec les apports parasites, les Φpertes doivent être comptés en valeur absolue ici ; refroidissement ; point ouvert 2
- (889, p. 572) irelance_dp(h) = MAX_{ds ∈ dp} irelance_ds(h) ;  ; toujours
- (890, p. 572) Qsys_ds_req_ch(h) = Σ_{ds ∈ dp} Qsys_ch_ds(h) ; Qsys_ds_req_fr(h) = Σ_{ds ∈ dp} Qsys_fr_ds(h) ; somme des demandes augmentées des réseaux du groupe rattachés (Id_Dist_1re) ; toujours
- (891, p. 572) Adess_ch_dp = Σ_{gr} Σ_{em ∈ dp} Rateff_ch_gr,em . Agr si idfonction = 1 (sinon 0) ; Adess_fr_dp = Σ_{gr} Σ_{em ∈ dp} Rateff_fr_gr,em . Agr si idfonction = 2 (sinon 0) ; Rateff = Rat_s x Rat_t de l'émetteur, Agr = SU ou SHAB ; une fois par simulation
- (892, p. 572) Ratsurf_dess_ch_dp,gr = Σ_{em ∈ dp, em ∈ gr} Rateff_ch_gr,em . Agr / Adess_ch_dp ; Ratsurf_dess_fr_dp,gr = 0 ; Ratsurf_dp,gr = Ratsurf_dess_ch_dp,gr ;  ; idfonction = 1
- (893, p. 572) Ratsurf_dess_fr_dp,gr = Σ_{em ∈ dp, em ∈ gr} Rateff_fr_gr,em . Agr / Adess_fr_dp ; Ratsurf_dess_ch_dp,gr = 0 ; Ratsurf_dp,gr = Ratsurf_dess_fr_dp,gr ;  ; idfonction = 2
- (894, p. 573) Ratbes_prim_fr_dp,gr(h) = 0 ; si Qsys_ds_req_ch(h) > 0 : Ratbes_prim_ch_dp,gr(h) = Σ_{ds ∈ dp, ds ∈ gr} Qsys_ch_ds(h) / Qsys_ds_req_ch(h) ; sinon Ratbes_prim_ch_dp,gr(h) = Ratsurf_dess_ch_dp,gr ; sert à la génération pour ventiler Qreq et les consommations par groupe ; idfonction = 1
- (895, p. 573) symétrique de (894) en froid ;  ; idfonction = 2
- (896, 897, p. 574) θmax_ch = 0 °C ; θmin_fr = 100 °C ; contrôle de montage ; idtype_dp = 0
- (898, p. 574) θdep(h) = θret(h) = 0 ; Modpertes(h) = Modcirc(h) = 0 ; qeff(h) = 0 ; fonct(h) = 0 ;  ; idtype_dp = 0
- (899, p. 574) θi,aval,eq_dp(h) = Σ_{gr} Ratsurf_dp,gr . θi,moy_gr(h) ; température d'air vue par les générateurs sur air (PAC air/air, effet joule) ; idtype_dp = 0 et idv_air_ds = 0 (batteries sur air du local)
- (900, p. 575) θi,aval,eq_dp(h) = Σ qm,spec_souffle_gr,s(h) . θair_souffle_gr,s(h) / Σ qm,spec_souffle_gr,s(h) ; si la somme des débits est nulle, reprendre (899) ; débits et températures de soufflage du système de ventilation ; idtype_dp = 0 et idv_air_ds = 1 ; hors champ immédiat (dépend du module double flux)
- (901, p. 576) θmax_ch_dp = MAX_{ds ∈ dp}(θdep_dim_ch_ds + Δθem_dim_ch_ds / 2 ; θret_dim_ch_ds - Δθem_dim_ch_ds / 2) [signes reconstruits par symétrie avec 911] ; contrôle de compatibilité avec la génération ; idtype_dp = 1 ou 2, chauffage
- (902, p. 576) θmin_fr = 100 °C ;  ; réseau intergroupes de chauffage
- (903, 904, p. 576) qnom_ch_dp = Σ_{ds ∈ dp} qnom_ch_ds ; qresid_dp = Σ_{ds ∈ dp} qresid_ds ;  ; idtype_dp = 1 ou 2
- (905, p. 576) fonct(h) = MAX_{ds ∈ dp} fonct_ds(h) ;  ; toujours (hydraulique)
- (906 (première rédaction), p. 576) Si fonct(h) > 0 : θdep(h) = MAX_{ds} θdep_ds(h) ; qtot_req(h) = Σ_{ds} qeff_ds(h) ; qeff(h) = MAX(qtot_req(h) ; qresid_dp) ; Modpertes(h) = 1 si idtype = 1, 0 si idtype = 2. Sinon (arrêt) : θdep(h) = θamb_ch (20 °C) ; qtot_req(h) = 0 ; qeff(h) = 0 ; Modpertes(h) = 0 ;  ; chauffage
- (907, 908 (seconde rédaction), p. 577) Si fonct(h) > 0 : θdep(h) = MAX_{ds} θdep_ds(h) ; Modpertes(h) = MAX_{ds} Modpertes_ds(h) ; qtot_req(h) = Σ qeff_ds(h) ; qeff(h) = MAX(qtot_req(h) ; qresid_dp). Sinon : θdep(h) = θamb_ch ; qtot_req = qeff = 0 ; Modpertes(h) = 0 ; doublon du texte avec (906) ; la seconde rédaction suit l'introduction p. 567 (« coefficient d'intermittence pris égal au maximum ») : retenir Modpertes = MAX_ds Modpertes_ds pour idtype = 1 et Modpertes = 0 pour idtype = 2 ; chauffage ; point ouvert 4
- (909, p. 578) idcirc_ch = 0 : Modcirc(h) = 0 ; 1 : Modcirc(h) = Modpertes(h) ; 2 : Modcirc(h) = Modpertes(h) . (qeff(h) / qnom_ch_dp)^(2/3) ; 3 : Modcirc(h) = Modpertes(h) . (0,5 . (qeff / qnom)^2 + 0,5 . (qeff / qnom)^3) ; et Modcirc(h) = 0 si idtype = 2 (p. 581) ; mêmes réserves de lecture que (863) ; réseau intergroupes de chauffage
- (910, p. 579) θmax_ch = 0 °C ;  ; réseau intergroupes de refroidissement
- (911, p. 579) θmin_fr = MIN_{ds ∈ dp}(θdep_dim_fr_ds + Δθem_dim_fr_ds / 2 ; θret_dim_fr_ds - Δθem_dim_fr_ds / 2), Δθem_dim_fr négatif ; seule équation de la fiche lisible en clair (unicode) ; refroidissement
- (912, 913, p. 579) qnom_fr_dp = Σ qnom_fr_ds ; qresid_dp = Σ qresid_ds ;  ; refroidissement
- (914 à 917, p. 579 et 580) fonct(h) = MAX_ds fonct_ds(h) ; si fonct > 0 : θdep(h) = MIN_{ds} θdep_ds(h) ; Modpertes(h) = MAX_ds Modpertes_ds(h) (ou 1 / 0 selon idtype dans la première rédaction) ; qtot_req(h) = Σ qeff_ds(h) ; qeff(h) = MAX(qtot_req(h) ; qresid_dp). Sinon : θdep(h) = θamb_fr (26 °C) ; qtot_req = qeff = 0 ; Modpertes = 0 ; MIN au lieu de MAX pour le départ en froid ; refroidissement
- (918, p. 581) idtype = 2 : Modcirc(h) = 0 ; idtype = 1 : mêmes quatre cas que (909) avec idcirc_fr, qnom_fr_dp ;  ; refroidissement
- (919, p. 581) Si fonct(h) = 0 : θret(h) = θdep(h). Sinon : θret(h) = (Σ_{ds ∈ dp} qeff_ds(h) . θret_ds(h) + MAX(0 ; qresid_dp - qtot_req(h)) . θdep(h)) / qeff(h) ; moyenne pondérée par les débits, le débit de décharge revenant à θdep ; chauffage et refroidissement
- (920, p. 586) idfonction = 1 : Qsys_ch_dp(h) = Qsys_ds_req_ch(h), Qsys_fr_dp(h) = 0 ; idfonction = 2 : Qsys_ch_dp(h) = 0, Qsys_fr_dp(h) = Qsys_ds_req_fr(h) ;  ; idtype_dp = 0
- (921, p. 586) Waux(h) = 0 ; Φpertes_vc(h) = 0 ; Φpertes_hvc(h) = 0 ; θmoy(h) = 0 °C ; Φaux_vc(h) = 0 ;  ; idtype_dp = 0
- (922, p. 587) θmoy(h) = (θdep(h) + θret(h)) / 2 ; transmis à la génération ; idtype_dp = 1 ou 2, chauffage
- (923, p. 587) θvc(h) = θvc_ch = 20 °C ;  ; chauffage
- (924, p. 587) Φpertes_vc(h) = Modpertes(h) . Umoy_vc_ch . Lvc . MAX(0 ; θmoy(h) - θvc(h)) ;  ; chauffage
- (925, p. 587) θhvc(h) = btherm(h) . θext(h) + (1 - btherm(h)) . θvc(h) ; btherm de Id_Et du nœud intergroupes ; chauffage
- (926, p. 587) Φpertes_hvc(h) = Modpertes(h) . Umoy_hvc_ch . Lhvc . MAX(0 ; θmoy(h) - θhvc(h)) ;  ; chauffage
- (927, p. 587) Waux(h) = Modcirc(h) . Paux_ch . 1 h ; Paux_ch = Pcirc_Prim_Ch ; chauffage
- (928, p. 587) Φaux_vc(h) = Pcirc_vc . Waux(h) avec Pcirc_vc = 0, donc 0 ;  ; chauffage
- (929, p. 587) Qsys_ch_dp(h) = Qsys_ds_req_ch(h) + Φpertes_vc(h) + Φpertes_hvc(h) ; Qsys_fr_dp(h) = 0 ; demande transmise à la génération Id_Gen ; chauffage
- (930 à 937, p. 588) θmoy = (θdep + θret) / 2 ; θvc(h) = θvc_fr = 26 °C ; Φpertes_vc = Modpertes . Umoy_vc_fr . Lvc . MIN(0 ; θmoy - θvc) ; θhvc = btherm . θext + (1 - btherm) . θvc ; Φpertes_hvc = Modpertes . Umoy_hvc_fr . Lhvc . MIN(0 ; θmoy - θhvc) ; Waux = Modcirc . Paux_fr ; Φaux_vc = 0 ; Qsys_ch_dp = 0 ; Qsys_fr_dp = Qsys_ds_req_fr + Φpertes_vc + Φpertes_hvc ; même question de signe qu'en (883) à (888) ; refroidissement
- (2357, p. 1303) Φpertes_dgr_recup_gr(h) = Partrecup_dgr_chfr . Σ_{ds ∈ gr} Φpertes_vc_ds(h), Partrecup_dgr_chfr = 1 ; pertes des réseaux du groupe en volume chauffé ; chaud et froid confondus (en froid le flux est un apport négatif de chaleur)
- (2359, p. 1303) Φaux_dgr_recup_gr(h) = Partrecup_circ_chfr . Σ_{ds ∈ gr} Φaux_vc_ds(h), Partrecup_circ_chfr = 0,6 ; soit 0,6 x 0,5 = 30 % de Waux du circulateur du groupe ; 
- (2361, p. 1303) Φaux_dintgr_recup_gr(h) = Partrecup_circ_chfr . Σ_{dp -> gr} Ratsurf_dp,gr . Φaux_vc_dp(h) (= 0 puisque Pcirc_vc = 0) ; Φpertes_dintgr_recup_gr(h) = Partrecup_dintgr_chfr . Σ_{dp -> gr} Ratsurf_dp,gr . Φpertes_vc_dp(h), Partrecup_dintgr_chfr = 0,6 ; répartition au prorata des surfaces desservies (892, 893) ; 
- (2364 à 2366, p. 1304) Φrecup_gr(h) = somme des flux récupérables (dont les quatre termes ci-dessus) ; Φrecup_conv_gr(h) = Partconv_autres . (Φaux_dgr + Φaux_dintgr + Φpertes_dgr + Φpertes_dintgr + ...) avec Partconv_autres = 0,5 ; Φrecup_rad_gr(h) = Φrecup_gr(h) - Φrecup_conv_gr(h) ; injectés comme apports internes du groupe au pas h + 1 (p. 1304) ; la part des ventilateurs locaux est à 100 % convective, hors famille

## Algorithme

```
Structures proposées (module openbce/distribution.py) :

RHO_CP = 998 * 1.163            # Wh/(m³.K)
THETA_EXT_LIM_CH, THETA_DEP_CH_MIN = 15.0, 20.0        # p. 550
PCIRC_VC_GROUPE, PCIRC_VC_INTER = 0.5, 0.0             # p. 562, 584
THETA_AMB = {CHAUD: 20.0, FROID: 26.0}                 # p. 571, 584
PART_RECUP = dict(dgr=1.0, dintgr=0.6, circ=0.6, conv=0.5)   # p. 1301

@dataclass(frozen=True)
class ReseauGroupe:        # un Distribution_Groupe_Chaud ou _Froid, lu sous l'Emetteur
    fonction: int           # 1 chaud, 2 froid
    emetteur: Noeud ; rateff: float          # Rat_s x Rat_t de l'émetteur porteur
    idtype: int (Type_2nd) ; id_dp: int (Id_Dist_1re) ; b_tampon: float (b de Id_Et, 1.0 si 0)
    lvc, lhvc, u_vc, u_hvc, paux: float
    iddebit (Mode_Reg_Debit), idgest (Gest_2nd), idcirc (Gest_Circ_2nd): int
    theta_dep_dim, theta_ret_dim, d_theta_dim (valeur absolue), qnom, qresid: float

@dataclass(frozen=True)
class ReseauInter:         # un Distribution_Intergroupe_Chaud ou _Froid, à la racine
    fonction, idtype (Type_Prim), id_gen (Id_Gen), b_tampon, lvc, lhvc, u_vc, u_hvc, paux, idcirc
    reseaux: list[ReseauGroupe]            # ceux dont Id_Dist_1re == Index
    qnom = Σ qnom_ds ; qresid = Σ qresid_ds                                   # (903, 904, 912, 913)
    adess, ratsurf: dict[groupe -> float]                                    # (891 à 893)

@dataclass
class EtatGroupeH:         # résultat horaire d'un réseau du groupe
    fonct: int ; qeff, d_theta, theta_dep, theta_ret, modpertes, modcirc: float
    qsys: float (demande augmentée) ; waux, phi_aux_vc, phi_pertes_vc, phi_pertes_hvc: float

def regulation_groupe(r, qsys_em, theta_i, te, te_base) -> (fonct, qreq, qeff, d_theta, modpertes, theta_dep, theta_ret, modcirc):
    if r.idtype == 0: return zéros                                              # (854)
    fonct = 1 if qsys_em > 0 else 0                                             # (855, 864)
    if not fonct: qreq = qeff = d_theta = modpertes = 0                         # (859, 868)
    elif r.iddebit == 3:                                                        # (856, 865)
        qreq = qsys_em / (RHO_CP * r.d_theta_dim) ; qeff = max(qreq, r.qresid)
        d_theta = qsys_em / (RHO_CP * qeff) ; modpertes = 1
    elif r.iddebit == 2:                                                        # (857, 866)
        qreq = qeff = r.qnom ; modpertes = min(1, qsys_em / (RHO_CP * r.qnom * r.d_theta_dim)) ; d_theta = r.d_theta_dim
    else:                                                                       # (858, 867)
        qreq = qeff = r.qnom ; modpertes = 1 ; d_theta = qsys_em / (RHO_CP * r.qnom)
    signe = +1 if r.fonction == 1 else -1                                       # chaud : eau plus chaude que l'ambiance
    if r.idgest == 1: theta_dep = fonct * r.theta_dep_dim + (1 - fonct) * theta_i            # (860, 869)
    elif r.idgest == 2: theta_dep = fonct * (r.theta_ret_dim + signe * d_theta) + (1 - fonct) * theta_i   # (861, 870)
    else:   # loi d'eau, chauffage seulement                                                   (862)
        if not fonct: theta_dep = theta_i
        elif te >= THETA_EXT_LIM_CH: theta_dep = max(THETA_DEP_CH_MIN, theta_i + d_theta)
        elif te <= te_base: theta_dep = r.theta_dep_dim
        else: theta_dep = max(theta_i + d_theta, r.theta_dep_dim + (THETA_DEP_CH_MIN - r.theta_dep_dim) * (te - te_base) / (THETA_EXT_LIM_CH - te_base))
    theta_ret = theta_dep if not fonct else theta_dep - signe * d_theta        # (872)
    modcirc = _modcirc(r.idcirc, modpertes, qeff, r.qnom)                       # (863, 871)
    return ...

def _modcirc(idcirc, modpertes, qeff, qnom):                                    # (863, 871, 909, 918)
    if idcirc == 0 or qnom <= 0: return 0.0
    x = qeff / qnom
    if idcirc == 1: return modpertes
    if idcirc == 2: return modpertes * x ** (2/3)          # lecture à confirmer au banc (point ouvert 1)
    return modpertes * (0.5 * x ** 2 + 0.5 * x ** 3)       # idem

def pertes_groupe(r, etat, qsys_em, theta_i, te) -> EtatGroupeH:                 # fiche 8.8
    if r.idtype == 0: qsys = qsys_em ; pertes et waux nuls                      # (873, 874)
    else:
        theta_moy = (etat.theta_dep + etat.theta_ret) / 2                       # (875, 882)
        theta_hvc = r.b_tampon * te + (1 - r.b_tampon) * theta_i                # (877, 884)
        ecart_vc, ecart_hvc = theta_moy - theta_i, theta_moy - theta_hvc
        if r.fonction == 1: p_vc, p_hvc = max(0, ecart_vc), max(0, ecart_hvc)   # (876, 878)
        else: p_vc, p_hvc = -min(0, ecart_vc), -min(0, ecart_hvc)               # (883, 885) comptées positives, point ouvert 2
        phi_vc = etat.modpertes * r.u_vc * r.lvc * p_vc ; phi_hvc = etat.modpertes * r.u_hvc * r.lhvc * p_hvc
        waux = etat.modcirc * r.paux                                            # (879, 886)
        phi_aux_vc = PCIRC_VC_GROUPE * waux                                     # (880, 887)
        qsys = qsys_em + phi_vc + phi_hvc                                       # (881, 888)
    return EtatGroupeH(...)

def intergroupe_heure(dp, etats: list[EtatGroupeH], te) -> (qsys_dp, theta_dep, theta_ret, theta_moy, waux, phi_pertes_vc, phi_pertes_hvc, fonct, irelance, ratbes):
    qsys_req = Σ e.qsys                                                          # (890)
    irelance = max(irelance_ds)                                                  # (889)
    ratbes[gr] = Σ_{ds ∈ gr} e.qsys / qsys_req si qsys_req > 0 sinon dp.ratsurf[gr]    # (894, 895)
    if dp.idtype == 0: return qsys_req, 0, 0, 0, zéros, ... ; θi,aval,eq = Σ ratsurf . θi_gr   # (920, 921, 899)
    fonct = max(e.fonct)                                                         # (905, 914)
    if fonct:
        theta_dep = max(e.theta_dep) en chaud, min en froid                      # (906, 915)
        modpertes = max(e.modpertes) si idtype == 1 sinon 0                      # (908, 917) lecture retenue, point ouvert 4
        qtot = Σ e.qeff ; qeff = max(qtot, dp.qresid)
        theta_ret = (Σ e.qeff * e.theta_ret + max(0, dp.qresid - qtot) * theta_dep) / qeff      # (919)
    else: theta_dep = theta_ret = THETA_AMB[fonction] ; qeff = qtot = 0 ; modpertes = 0         # (906, 917, 919)
    modcirc = 0 si idtype == 2 sinon _modcirc(dp.idcirc, modpertes, qeff, dp.qnom)              # (909, 918)
    theta_moy = (theta_dep + theta_ret) / 2                                      # (922, 930)
    theta_vc = THETA_AMB[fonction] ; theta_hvc = dp.b_tampon * te + (1 - dp.b_tampon) * theta_vc   # (923, 925, 931, 933)
    phi_vc, phi_hvc : mêmes formules que pertes_groupe avec Umoy_Prim, Lvc_Prim, Lhvc_Prim    # (924, 926, 932, 934)
    waux = modcirc * dp.paux ; phi_aux_vc = PCIRC_VC_INTER * waux = 0            # (927, 928, 935, 936)
    qsys_dp = qsys_req + phi_vc + phi_hvc                                        # (929, 937)
    return ...

Ordre d'appel dans la boucle horaire du mode Th-C (à insérer dans groupe.calculer après le calcul de la puissance p et des températures fin, ligne 278, ou dans une boucle maître qui fait avancer tous les groupes d'un bâtiment heure par heure, voir point ouvert 7) :
pour h dans 0..n-1 :
    1. apports internes du groupe : conv += Φrecup_conv_gr(h-1), rad += Φrecup_rad_gr(h-1) (état conservé de l'heure précédente, 0 à h = 0)   # p. 1304
    2. modèle thermique du groupe (existant) : besoin bch[h] / bfr[h] et θi,moy_gr(h) ; irelance_gr(h) = 1 si consigne de relance > consigne programmée (emission.relance)
    3. demande par émetteur : Qsys_ch_em(h) = Rateff_em . bch[h] (corrigée des pertes au dos dans la fiche 8.1, module emission.py à compléter ; point ouvert 6) ; idem froid
    4. pour chaque ReseauGroupe du groupe (chaud puis froid, un réseau par émetteur et par fonction) : regulation_groupe puis pertes_groupe ; cumuls du groupe : Waux_ds_gr(h) = Σ waux, Φaux_vc_ds_gr(h) = Σ phi_aux_vc, Φpertes_vc_ds_gr(h) = Σ phi_pertes_vc
    5. pour chaque ReseauInter du bâtiment : intergroupe_heure sur les EtatGroupeH de tous les groupes rattachés à la même heure ; sorties vers la génération Id_Gen : Qsys_ch_dp(h), Qsys_fr_dp(h), θmoy_dp(h), θdep_dp(h), irelance_dp(h), Adess, Ratsurf_dp,gr, Ratbes_prim_dp,gr(h), θi,aval,eq_dp(h)
    6. pertes récupérables pour h + 1 (fiche 11.1) :
       Φpertes_dgr = 1.0 . Φpertes_vc_ds_gr(h) ; Φaux_dgr = 0.6 . Φaux_vc_ds_gr(h)                                # (2357, 2359)
       Φpertes_dintgr = 0.6 . Σ_dp Ratsurf_dp,gr . Φpertes_vc_dp(h) ; Φaux_dintgr = 0                            # (2361)
       Φrecup = somme ; Φrecup_conv = 0.5 . Φrecup ; Φrecup_rad = Φrecup - Φrecup_conv                            # (2364 à 2366)
       en froid, les Φpertes_vc comptés positifs en (888) deviennent des apports négatifs ici (signe à trancher, point ouvert 2)
    7. consommation d'auxiliaires de distribution du groupe : Waux_dist_gr(h) = Σ_ds waux_ds(h) + Σ_dp Ratsurf_dp,gr . waux_dp(h) (répartition du circulateur primaire au prorata des surfaces : convention à confirmer au banc, point ouvert 5) ; cumul annuel / 1000 / surface -> à comparer à O_Cef_aux_distribution_annuel (électricité, coefficient 2,3 pour le Cep dans consommation.py)

États conservés d'une heure à l'autre : Φrecup_conv_gr et Φrecup_rad_gr (une valeur par groupe, injectée à h + 1) ; rien d'autre, la distribution est sans inertie (pas de variable mémoire dans les fiches 8.7 à 8.10). Les grandeurs annuelles fixes (Adess, Ratsurf, qnom_dp, qresid_dp, θmax_ch, θmin_fr) sont calculées une fois à la construction des objets.

Interface aval : la génération (fiche 8.14) reçoit par réseau intergroupes Qsys_ch_dp(h), Qsys_fr_dp(h), θmoy_dp(h), θdep_dp(h), irelance_dp(h), Adess_ch/fr, Ratbes_prim et renvoie Qreq,ch gen,gr(h) ventilé par groupe ; cette conversion est hors famille.
```

## Sorties RSEE pour le banc

- `O_Cef_aux_distribution_annuel` (Sortie_Groupe_C (Sortie_Batiment_C/Sortie_Zone_C/Sortie_Groupe_C), kWhef/m² (surface O_SREF du groupe), vu 0 sur réseaux fictifs ; cible principale du banc pour Σ Waux)
- `O_Cef_aux_distribution_mois` (Sortie_Groupe_C (Sortie_Mensuelle Mois/Valeur), kWhef/m² par mois : utile pour distinguer circulateur chaud (hiver) et froid (été))
- `O_Cef_auxs_elec_annuel` (Sortie_Groupe_C, kWhef/m² ; auxiliaires « systèmes » en électricité, à comparer à O_Cef_aux_distribution_annuel pour vérifier s'il inclut d'autres auxiliaires (génération))
- `O_Cef_elec_cons_auxdist_annuel et O_Cef_elec_cons_auxdist_mois` (Sortie_Zone_C, kWhef/m² ; somme des groupes de la zone pondérée par les surfaces)
- `O_Cef_imp_auxdist_annuel, O_Cef_elec_imp_auxdist_annuel, O_Cef_elec_imp_auxdist_mois, O_Cef_elec_AC_auxdist_annuel` (Sortie_Zone_C et Sortie_Batiment_C, kWhef/m² ; part importée et part autoconsommée (PV) : la somme imp + AC doit retrouver cons)
- `O_E_ef_aux_zone, O_E_ef_aux_bat` (Sortie_Zone_C, Sortie_Batiment_C, énergie finale des auxiliaires (ventilation + distribution), unité à vérifier (probablement kWhef) ; sert de contrôle de cohérence avec O_Cef_aux_ventilateur_annuel + O_Cef_aux_distribution_annuel)
- `O_Cef_ch_annuel, O_Cef_fr_annuel (et par énergie : O_Cef_ch_gaz_annuel, O_Cef_ch_elec_annuel, ...)` (Sortie_Groupe_C, kWhef/m² ; seule trace de Qsys_ch_dp : pour une génération dont le rendement est connu (chaudière à rendement constant, effet joule à 100 %), Cef_ch x rendement - O_B_Ch_annuel donne les pertes de distribution)
- `O_B_Ch_annuel, O_B_Fr_annuel, O_B_Ch_mois, O_B_Fr_mois` (Sortie_Groupe_C (et Sortie_Batiment_C), kWh/m² ; besoins au niveau des émetteurs, point de départ (Qsys_em) déjà bancé par banc/cep.py)
- `Q_fou_3_postes` (Sortie_Generation/Sortie_Generateur_Collection/Sortie_Generateur, Wh (ou kWh) fournis par le générateur sur les trois postes chauffage, froid, ECS : pour un bâtiment sans ECS sur ce générateur, Q_fou_3_postes = Σ_h (Qsys_ch_dp + Qsys_fr_dp), c'est le meilleur banc direct des pertes de distribution)
- `Nbhcharge_0_ch ... Nbhcharge_90_100_ch, Nbhcharge_HF_ch (idem _fr)` (Sortie_Generateur, heures par classe de taux de charge : la distribution des Qsys_ch_dp(h) / Pn du générateur doit reproduire l'histogramme ; sensible à Modpertes et aux pertes intergroupes à faible charge)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch, O_Idsousdim_Court_Fr, O_Idsousdim_Long_Fr` (Sortie_Generation, booléens de sous-dimensionnement : dépendent des pointes de Qsys_ch_dp(h))
- `aucune sortie pour θdep, θret, θmoy, Modpertes, Φpertes_vc, Φrecup` (-, ces grandeurs ne peuvent être bancées qu'indirectement (consommation de génération dépendant de θmoy pour les PAC))

## Points ouverts (à trancher au codage)

- 1. Facteur de modulation des circulateurs à vitesse variable (863, 871, 909, 918) : les équations sont des images illisibles, les jetons donnent seulement « 3 2 » pour idcirc = 2 et « 3 2 2 0,5 0,5 » pour idcirc = 3. Lectures candidates : idcirc = 2 : (qeff/qnom)^(2/3) ou 0,25 + 0,75 . qeff/qnom ; idcirc = 3 : 0,5 . x² + 0,5 . x³ ou 0,5 . x + 0,5 . x^(2/3). Tranché par un banc sur O_Cef_aux_distribution_annuel et _mois des RSEE dont un Distribution_Groupe_* a Mode_Reg_Debit = 3 et Gest_Circ_2nd = 2 ou 3 (planchers chauffants collectifs, ventilo-convecteurs) ; avec iddebit 1 ou 2 le facteur vaut 1 et le banc ne discrimine pas.
- 2. Signe des pertes des réseaux de refroidissement (883, 885, 888, 931 à 934, 937) : écrites avec MIN(0 ; θmoy - θi), donc négatives, puis ajoutées à Qsys_fr, ce qui réduirait la demande de froid alors qu'un réseau froid qui se réchauffe doit en augmenter. Hypothèse retenue : valeur absolue dans Qsys_fr et apport négatif (refroidissement de l'ambiance) dans la fiche 11.1. Banc : O_Cef_fr_annuel et Q_fou_3_postes d'un RSEE à réseau froid hydraulique avec Lvc ou Lhvc non nuls, comparés à O_B_Fr_annuel.
- 3. Convention de signe de Delta_Theta_Em_Dim_Fr : les RSEE le saisissent négatif (-1 même pour un réseau fictif) et la note p. 579 confirme ; les équations 865 à 867 et 870 ne précisent pas si la valeur absolue est prise. Hypothèse : valeur absolue pour les débits, θret = θdep + |Δθem| en froid. Banc : identique au point 2 (le débit conditionne Modpertes et Modcirc en débit variable).
- 4. Modpertes du réseau intergroupes : deux rédactions contradictoires p. 576 et 577 (idem p. 579 et 580 en froid), l'une fixe Modpertes = 1 si idtype = 1 et 0 si idtype = 2, l'autre Modpertes = MAX_ds Modpertes_ds. Retenu : MAX_ds pour idtype = 1 (cohérent avec l'introduction p. 567), 0 pour idtype = 2. Banc : O_Cef_aux_distribution_annuel des RSEE dont Type_Prim = 1 avec Pcirc_Prim non nul et des réseaux du groupe en fonctionnement intermittent (Mode_Reg_Debit = 2) ; l'écart entre les deux lectures est la différence entre heures de fonctionnement et heures à pleine charge.
- 5. Attribution de Waux du circulateur intergroupes aux groupes pour O_Cef_aux_distribution_annuel : la fiche 8.6 (p. 546) dit seulement que les consommations sont « regroupées et sommées dans la fiche Calculs groupe » ; la clé de répartition n'est pas dans les fiches lues (Ratsurf_dp,gr ou Ratbes_prim_ch_dp,gr(h)). Hypothèse : Ratsurf_dp,gr comme pour les pertes (2361). Banc : RSEE à plusieurs groupes sur un même Distribution_Intergroupe avec Pcirc_Prim non nul, comparer la répartition de O_Cef_aux_distribution_annuel entre groupes aux surfaces desservies.
- 6. Demande par émetteur Qsys_ch_em(h) : la fiche 8.1 la produit (Rateff, pertes au dos Pper, part latente 829) et emission.py ne la calcule pas encore (seulement l'émetteur équivalent) ; les équations 809 à 824 de la fiche 8.1 n'ont pas été lues ici. À spécifier dans la famille émission ; en attendant Qsys_ch_em = Rateff_em . bch[h] / (1 - Pper_em) comme approximation à vérifier.
- 7. Architecture : groupe.calculer boucle sur toute l'année pour un groupe ; le réseau intergroupes a besoin, à la même heure, des états de tous les groupes qu'il dessert, et les pertes récupérées reviennent à h + 1. Deux voies : (a) boucle maître heure par heure sur tous les groupes du bâtiment (refonte de groupe.calculer en générateur ou en objet à méthode pas(h)) ; (b) deux passes : groupes sans récupération, puis distribution et récupération, puis nouvelle passe des groupes avec Φrecup en série fixe. La voie (b) converge vite car les flux récupérés sont petits devant les besoins, mais l'intergroupes doit alors être calculé entre les deux passes. Banc : O_B_Ch_annuel après injection des pertes récupérées (déjà bancé sans elles à +1 % médian).
- 8. θi,moy_gr(h) : le texte veut la moyenne sur le pas « après croisement » ; groupe.py expose la température de fin de pas (fin.i) et la moyenne t.i. Prendre t.i (moyenne). Impact faible sur les pertes (écart θmoy - θi de 20 à 40 K).
- 9. btherm(h) : la fiche attend une valeur horaire ; openBCE a un b constant par espace tampon (enveloppe.coefficients_b). Suffisant pour la distribution. Pour Id_Et = 0 on prend btherm = 1 (réseau hors volume chauffé donnant sur l'extérieur), convention déjà en usage dans parois.py.
- 10. irelance_gr(h) : non défini explicitement dans les fiches lues ; déduit de la fiche 8.5 (relances, emission.relance) comme l'indicateur des heures où la consigne de relance diffère de la consigne programmée. Il ne pèse sur aucune équation de la distribution, seulement transmis à la génération (889).
- 11. Loi d'eau (862) : l'équation est une image ; la reconstruction MAX(θdep_ch_min ; θi + Δθem) / θdep_dim / interpolation linéaire suit la figure 97 (p. 555). Banc : consommation d'une PAC air/eau (O_Cef_ch_elec_annuel) dont le COP dépend de θmoy, sur un RSEE avec Gest_2nd_Ch = 3.
- 12. Réseau 2 tubes réversible : la conduite unique est décrite deux fois (nœuds Chaud et Froid, p. 548) ; les pertes sont donc calculées par le réseau en fonctionnement seulement, l'autre ayant Qsys_em = 0 et Modpertes = 0. Pas d'ambiguïté mais un contrôle à poser : Lvc et Lhvc identiques sur les deux nœuds du même émetteur.
- 13. Tableaux et équations illisibles en texte (images dans le PDF) : toutes les équations 851 à 872 (p. 552 à 559), 875 à 878 et 882 à 885 (p. 565, 566), 889 à 909 et 912 à 919 (p. 572 à 581, sauf 911 lisible), 922 à 926 et 930 à 934 (p. 587, 588), 938 à 957 (p. 594 à 597) ; figures 94 à 97 (assemblages et loi d'eau, p. 541, 545, 547, 555) et figures 98 à 102 de la fiche 8.13 (p. 602 à 604). Les tableaux 95 à 103 (nomenclatures) sont lisibles.

## Tableaux en image dans le PDF

- Figure 94 Assemblages des systèmes de chauffage et de refroidissement, p. 541 (schéma, texte partiel)
- Figure 95 Assemblage des composants des systèmes de chauffage et de refroidissement, p. 545 (schéma d'interface, flux Qsys/θdep/θret/Waux entre sous-assemblages)
- Figure 96 Assemblage des composants des systèmes associés à une CTA, p. 547
- Équations 851 à 853, p. 552 (cohérence et relance) : images, jetons dispersés
- Équations 855 à 859, p. 554 (fonctionnement, débits, Modpertes du groupe) : images
- Équations 860 à 863 et figure 97 (loi d'eau), p. 555 et 556 : images
- Équations 864 à 871, p. 557 et 558 : images
- Équation 872, p. 559 : image
- Équations 875 à 878, p. 565 et 882 à 885, p. 566 : images
- Équations 889 à 895, p. 572 et 573 (ratios de surface et de besoin) : images
- Équations 896 à 900, p. 574 et 575 : images
- Équations 901 à 909, p. 576 à 578 : images
- Équations 910 et 912 à 919, p. 579 à 581 : images (911 lisible en unicode)
- Équations 920 à 921, p. 586 et 922 à 937, p. 587 et 588 : images
- Fiche 8.11 : équations 938 à 957, p. 594 à 597 : images (hors champ)
- Fiche 8.13 : figures 98 à 102 (schémas de position des réseaux par rapport à l'isolant, gaines palières et logements), p. 602 à 604 : images, le texte seul suffit à la règle
- Tableau 99 (p. 564), tableau 101 (p. 574), tableau 103 (p. 586) : récapitulatifs d'appel des procédures, lisibles ; attention le titre du paragraphe hydraulique de la fiche 8.8 (p. 565, 566) écrit « idtype = 0 » au lieu de 1

## Estimation

Volume : module distribution.py d'environ 300 à 380 lignes (lecture des nœuds et constitution de l'arborescence émetteur -> réseau du groupe -> réseau intergroupes -> génération : 80 lignes ; régulation du groupe : 70 ; pertes du groupe : 40 ; intergroupes : 90 ; récupération fiche 11.1 : 30 ; constantes et docstrings : 40). Banc banc/distribution.py d'environ 80 lignes sur O_Cef_aux_distribution_annuel et _mois, Q_fou_3_postes et Nbhcharge. Tests d'environ 120 lignes (réseau fictif, les trois modes de débit, les trois modes de température, retour pondéré avec débit de décharge, pertes nulles quand θmoy < θi).

Difficulté : moyenne pour les équations elles-mêmes (elles sont algébriques, sans inertie, et la plupart se reconstruisent sans ambiguïté depuis les jetons), élevée pour deux raisons : (1) la refonte de la boucle horaire (point 7) pour faire avancer plusieurs groupes en parallèle et réinjecter les pertes récupérées à h + 1, qui touche groupe.calculer ; (2) trois lectures incertaines d'images (facteurs Modcirc, signe des pertes en froid, Modpertes intergroupes) qui ne se tranchent qu'au banc, et les deux RSEE lus ici n'ont que des réseaux fictifs : il faudra choisir parmi les autres RSEE du lot ceux dont Type_2nd = 1 ou Type_Prim = 1 avec Pcirculateur non nul (planchers chauffants, radiateurs à eau sur chaudière ou PAC air/eau, bureaux à ventilo-convecteurs) avant de lancer le banc. Prérequis amont : Qsys_ch_em par émetteur (fiche 8.1, point 6). Ordre de grandeur de deux à trois jours de travail, dont une journée de banc.
