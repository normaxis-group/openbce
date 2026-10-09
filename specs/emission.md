# Spécification : Émission et relance : compléments

Lot 2 du 10/10/2026, lecture seule des fiches de l'annexe III. Les « points ouverts » sont tranchés au codage.

## Périmètre

FAMILLE « Émission et relance : compléments » (fiches 8.1 C_Emi_Systèmes d'émission, 8.2 FA_Émissions mixte et composite, 8.3 C_Emi_Bilan hydrique, 8.5 C_Ein_Programmation des relances).

COUVERT par cette spécification (ce qui manque dans emission.py et groupe.py) :
1. Répartition de la puissance utile du groupe entre les émetteurs et pertes au dos par émetteur : Qsys_ch_em, Qsys_fr_em (811, p. 503), totaux (825, p. 506-507), Pper (796, p. 497). Aujourd'hui groupe.calculer rend un besoin global (bch, bfr) et emission.equivalent porte une moyenne pondérée de Per_dos qui n'est appliquée nulle part.
2. Températures finales et moyennes corrigées des dérives (826 à 828, p. 507) : le code ne retranche pas idbch x (δθvt + δθvs) de θop,fin.
3. Ventilateurs locaux des émetteurs à recyclage d'air (ventilo-convecteurs, cassettes) : conditions d'activation (812), régimes et puissances (813), chaleur restituée (814), débit massique (815), totaux (816, 817), p. 503-505 ; indicateur de relance irelance (849, p. 540) dont ils dépendent. Th-C seulement.
4. Batterie froide et déshumidification des émetteurs à recyclage : θbatt_dim (818, 819, p. 506), Qm_recirc_eff et θbatt (820 à 823), ωsat (824), énergie latente ajoutée aux besoins de froid (829, p. 507).
5. Bilan hydrique du groupe (8.3) : nécessaire au Cep uniquement s'il existe un émetteur de froid à recyclage d'air sollicité (Gest_vcv > 0 et Is_emetteur_froid = 1), ou pour alimenter une CTA (hors famille). Sans cela, ω_i,g n'intervient dans aucune consommation : on peut le coder plus tard ; la spécification donne la version complète (830 à 839) reconstituée, car toutes ces équations sont des images dans le PDF.
6. Vérification mot à mot des équations déjà codées (797 à 810, 845 à 848) : liste des divergences dans points_ouverts.
7. Émissions mixtes et composites (8.2) : règles de SAISIE uniquement (valeurs de Rat_t par configuration et zone climatique, variations à retenir). Aucune équation de calcul : le moteur lit Rat_s_ch, Rat_t_ch tels que saisis et applique (797). Les tableaux de la fiche servent au plus à un contrôle de saisie (banc/controle_saisie.py), pas au moteur.

HORS CHAMP et pourquoi :
- Comportement thermique du groupe (fiche 5.21, matrice 10 W/m²) : déjà dans thermique.py.
- Brasseurs d'air en Th-C (δθcons_fr_BA, p. 500, fiche 8.32) : famille brasseurs ; signalé comme manque dans ThC.
- Saisons effectives (8.4) : déjà traitées par chauffage_impose/refroidissement_impose.
- Distribution du groupe (8.7, 8.8) et génération : familles suivantes ; on s'arrête à Qsys_ch_em / Qsys_fr_em transmis au réseau de distribution du groupe (Distribution_Groupe_Chaud / Froid de l'émetteur).
- Relance des CTA (850, p. 540) : image, dépend de la fiche CTA.
- Humidité des scénarios (A_int_occ, A_int_hors_occ) et débits d'air sec Qmaj avec ωmaj : entrées du bilan hydrique à fournir par les fiches scénarios et C_VEN_Débits d'air ; non spécifiées ici.
- Bbio : la fiche 8.1 dit que l'émetteur conventionnel du Bbio n'a ni pertes au dos ni ventilateurs (p. 494) ; rien à changer dans le mode Th-B.

## Entrées (RSEE)

- `Groupe/Emetteur` / `Index` : em ; entier ; valeurs vues : 1 à 8
- `Groupe/Emetteur` / `Is_emetteur_chaud` : idem_chaud_em ; booléen 0/1 ; valeurs vues : 1
- `Groupe/Emetteur` / `Is_emetteur_froid` : idem_froid_em ; booléen 0/1 ; valeurs vues : 0, 1 (plenums du T.ONE)
- `Groupe/Emetteur` / `Per_dos` : Pper_em (796) ; valeur déjà calculée par le logiciel de saisie, lue telle quelle ; réel 0 à 1 ; valeurs vues : 0 partout dans les deux fichiers
- `Groupe/Emetteur` / `Rat_s_ch` : Rats_ch_em ; réel 0 à 1 ; valeurs vues : 0,1 (sèche-serviettes), 0,9 (plenum), 1
- `Groupe/Emetteur` / `Rat_t_ch` : Ratt_ch_em ; réel 0 à 1 ; valeurs vues : 1
- `Groupe/Emetteur` / `Rat_s_fr` : Rats_fr_em ; réel 0 à 1 ; valeurs vues : 0, 1
- `Groupe/Emetteur` / `Rat_t_fr` : Ratt_fr_em ; réel 0 à 1 ; valeurs vues : 0, 1
- `Groupe/Emetteur` / `Typologie_Emetteur_Chaud` : ligne du tableau 86 (Pemconv_ch) ; entier code ; valeurs vues : 1 (soufflage), 2 (mural rayonnant)
- `Groupe/Emetteur` / `Pem_conv_ch` : Pemconv_ch_em saisi ; réel ; valeurs vues : 0 (donc valeur du tableau 86)
- `Groupe/Emetteur` / `Typologie_Emetteur_Froid` : ligne du tableau 87 (Pemconv_fr) ; entier code ; valeurs vues : 0, 1
- `Groupe/Emetteur` / `Pem_conv_fr` : Pemconv_fr_em saisi ; réel ; valeurs vues : 0
- `Groupe/Emetteur` / `Classe_Variation_Spatiale_Chaud` : classe A, B1, B2, B3, C du tableau 83 ; entier 1 à 5 ; valeurs vues : 3 (B2), 4 (B3)
- `Groupe/Emetteur` / `Classe_Variation_Spatiale_Froid` : classe A, B, C du tableau 85 ; entier 0 à 3 ; valeurs vues : 0, 2 (B)
- `Groupe/Emetteur` / `Carac_Haut_Plafond` : colonne de hauteur sous plafond des tableaux 83 et 85 ; entier 0 à 3 ; valeurs vues : 0 (< 4 m)
- `Groupe/Emetteur` / `Delta_Temp_vs_ch / Delta_Temp_vs_fr` : θvs_ch_em, θvs_fr_em saisis (valeur justifiée) ; réel K ; valeurs vues : 0 (donc tableau)
- `Groupe/Emetteur` / `Nombre_niveaux_desservis` : colonne du tableau 84 (poêles et inserts : 1 niveau 0,9 ; 2 niveaux 1,4) ; NON lu par le code ; entier ; valeurs vues : 0
- `Groupe/Emetteur` / `Regulation_Poele_Ou_Insert` : ligne du tableau 89 (thermostat d'ambiance 2 ; manuelle 2,5) ; NON lu par le code ; entier code ; valeurs vues : 0
- `Groupe/Emetteur` / `Delta_Temp_vt_ch` : θvt_ch_em saisi (bornes : 0,2 effet joule, 0,4 autres) ; réel K ; valeurs vues : 0,2 (sèche-serviettes effet joule), 0,4 (plenum, cassette)
- `Groupe/Emetteur` / `Delta_Temp_vt_fr` : θvt_fr_em saisi (borne haute -0,4) ; réel K négatif ; valeurs vues : 0, -0,4
- `Groupe/Emetteur` / `Statut_Variation_Temporelle_Chaud / _Froid` : certifiée / justifiée (+0,5 K) / défaut ; correspondance des codes non donnée par le texte (le code lit 2 = justifiée) ; entier code ; valeurs vues : 0
- `Groupe/Emetteur` / `Couple_Regulateur_Emetteur_Chaud / _Froid` : tableau 88 : arrêt total possible ou non (le code lit 0 = sans arrêt total 2,0 K ; 1 = avec 1,8 K) ; entier code ; valeurs vues : 0
- `Groupe/Emetteur` / `detection_presence` : Id_detection_presence_em (800) ; booléen 0/1 ; valeurs vues : 0
- `Groupe/Emetteur` / `Gest_vcv` : GestVCV_em ; entier 0 à 3 ; valeurs vues : 0 (T.ONE) ; 3 (cassette bureaux : arrêt total possible)
- `Groupe/Emetteur` / `I_spv` : ispv_em ; booléen 0/1 ; valeurs vues : 0
- `Groupe/Emetteur` / `P_VCV_gv / P_VCV_mv / P_VCV_pv / P_VCV_spv` : PVCV_GV, PVCV_MV, PVCV_PV, PVCV_SPV ; réel W ; valeurs vues : 13 / 8 / 6 / 0 (cassette) ; 0 ailleurs
- `Groupe/Emetteur` / `Q_v_recirc_GV / Q_v_recirc_MV / Q_v_recirc_PV` : Qv_recirc_GV, Qv_recirc_MV, Qv_recirc_PV ; réel m³/h ; valeurs vues : 510 / 420 / 390 (cassette) ; 0 ailleurs
- `Groupe/Emetteur` / `Id_Regul_Batt` : idregul_batt (0 débit d'eau progressif, 1 batterie à température constante) ; entier 0/1 ; valeurs vues : 0
- `Groupe/Emetteur` / `SeuilVCV_pvmv_ch / _fr` : SeuilVCV_pvmv_ch = 20 Wh/m², SeuilVCV_pvmv_fr = -20 Wh/m² (conventionnels, p. 488) ; absent du RSEE ; valeurs vues : aucun champ trouvé
- `Groupe/Emetteur/Distribution_Groupe_Froid` / `Type_2nd` : idtype (0 fictif : θbatt_dim = 9 °C ; 1 hydraulique) ; entier 0/1 ; valeurs vues : 0 (réseau fictif)
- `Groupe/Emetteur/Distribution_Groupe_Froid` / `Gest_2nd_Fr` : idgest_fr (1 départ constant, 2 retour constant, 3 non précisé) ; entier 1 à 3 ; valeurs vues : 0
- `Groupe/Emetteur/Distribution_Groupe_Froid` / `Theta_Dep_Dim_Fr` : θdep_dim_fr ; réel °C ; valeurs vues : 0
- `Groupe/Emetteur/Distribution_Groupe_Froid` / `Theta_Ret_Dim_Fr` : θret_dim_fr ; réel °C ; valeurs vues : 0
- `Groupe/Emetteur/Distribution_Groupe_Froid` / `Delta_Theta_Em_Dim_Fr` : Δθem_dim_fr ; réel K ; valeurs vues : -1 (négatif en froid)
- `Groupe/Emetteur/Distribution_Groupe_Chaud` / `Index, Id_Dist_1re` : réseau de distribution du groupe destinataire de Qsys_ch_em (famille distribution) ; entiers ; valeurs vues : 1 à 11 ; 1, 4, 5, 6, 7, 8
- `Groupe` / `Is_Climatise` : iclim (808) ; booléen 0/1 ; valeurs vues : 1 (T.ONE), 0 (bureaux)
- `Groupe` / `SHAB / SU` : Agr (SHAB en usages 1 et 2, SU sinon) ; réel m² ; valeurs vues : 410,27 / 241,24
- `Groupe` / `Type_Pgrm_Ch` : Typepgrm_ch (tableau 93) ; entier 1 à 3 ; valeurs vues : 2 (horloge + ambiance), 3 (optimiseur, bureaux)
- `Groupe` / `Type_Pgrm_Fr` : Typepgrm_fr (tableau 94) ; 0 hors texte, à lire comme « sans objet » ; entier 0 à 3 ; valeurs vues : 2 ; 0 quand le groupe n'est pas climatisé
- `Groupe` / `volume du groupe` : V (bilan hydrique, 830) ; réel m³ ; valeurs vues : pas de champ Volume direct repéré sous Groupe dans les deux fichiers ; le ThD d'openbce porte déjà un `volume`
- `Simu / zone climatique` / `Departement, Altitude (déjà lus par banc/cep.py)` : θext_base (845), zone H1/H2/H3 pour les tableaux de la fiche 8.2 ; texte, réel ; valeurs vues : -

## Paramètres conventionnels

- Ca, chaleur massique de l'air sec = 1006 J/(kg.K) (p. 493 (tableau 82))
- Lv_eau, chaleur latente de vaporisation = 2500 kJ/kg (p. 524 (tableau 90))
- SeuilVCV_pvmv_ch = 20 Wh/m² (passage petite vitesse à moyenne vitesse en chaud) (p. 488)
- SeuilVCV_pvmv_fr = -20 Wh/m² (p. 488)
- FBbatt, facteur de by-pass de la batterie (idregul_batt = 0) = 0,8 (p. 489 et 506)
- θbatt_dim si réseau fictif (détente directe) = 9 °C (p. 505-506 (818))
- HRsat = 100 % (p. 506 (824))
- θpresence_ch = -0,15 K (p. 489)
- Psd_ch, Psd_fr = 0,5 quelle que soit la régulation (p. 489 et 498)
- θvt par défaut chaud = 2,0 K sans arrêt total ; 1,8 K avec arrêt total (p. 498 (tableau 88))
- θvt par défaut froid = -2,0 K ; -1,8 K (p. 498 (tableau 88))
- θvt poêles et inserts = 2 K avec thermostat d'ambiance ; 2,5 K régulation manuelle (p. 498 (tableau 89))
- θvs poêles et inserts = 0,9 K un niveau desservi ; 1,4 K deux niveaux (p. 495 (tableau 84))
- Bornes de θvt saisi = chaud : ≥ 0,2 K effet joule, ≥ 0,4 K autres ; froid : ≤ -0,4 K ; valeur justifiée (non certifiée) : +0,5 K en chaud, -0,5 K en froid (p. 497)
- Puissance d'essai de la droite du groupe = 10 W/m² x Agr, répartie Pemconv convectif et (1 - Pemconv) radiatif (p. 501 (805))
- θext_reg_sup (relance, optimiseur) = 15 °C (p. 536)
- Durées de relance chaud (courte / prolongée) = type 1 : 2 h / 6 h ; type 2 : 2 h / 4 h ; type 3 : 1 h / 0 à 3 h linéaire en θext (p. 538 (tableau 93))
- Durées de relance froid = type 1 : 1 h / 3 h ; type 2 : 1 h / 2 h ; type 3 : 0 h, consigne de confort permanente (p. 538 (tableau 94))
- Valeurs initiales des consignes de relance = θiich_relance(0) = 0 °C ; θiifr_relance(0) = 100 °C ; hors saison : 0 °C en chaud, 100 °C en froid (p. 539-540 (846))
- Rat_t émetteur à air non gainé en partie B (fiche 8.2.3) = H1 : 0,40 ; H2a-b-c : 0,45 ; H2d et H3 : 0,55 ; complémentaire : 0,60 / 0,55 / 0,45 ; partie A et SDB : 1,0 (p. 511)
- Rat_t appareil bois régulé automatiquement (8.2.4) = partie A 1,0 ; partie B bois 0,5 et complément 0,5 ; SDB 1,0 (p. 512)
- Rat_t appareil bois sans régulation automatique (8.2.4) = bois : 0,5 en A, 0,25 en B ; principal : 0,5 en A, 0,75 en B ; SDB 1,0 (p. 513)
- Rat_t poêle ou insert gaz en appoint (8.2.5) = appoint : 0,10 en A, 0,05 en B ; principal : 0,90 en A, 0,95 en B ; SDB 1,0 ; SA + SB ≤ 100 m² (p. 514-515)
- Rat_t émission composite base + appoint, selon P1 / Prequise (0,9 ; 0,7 ; 0,5 ; 0,3) = base hors H3 : 0,76 ; 0,75 ; 0,69 ; 0,50. base H3 : 0,67 ; 0,67 ; 0,59 ; 0,39. appoint hors H3 : 0,24 ; 0,25 ; 0,31 ; 0,50. appoint H3 : 0,33 ; 0,33 ; 0,41 ; 0,61. Colonne la plus proche, sans interpolation ; base admise si P1 ≥ 30 % de Prequise ; les deux émetteurs prennent θvs et θvt de l'appoint (p. 519-520)
- Rat_t complément par temps froid, selon P1 / Prequise (0,9 ; 0,7 ; 0,5) = base hors H3 : 0,99 ; 0,99 ; 0,97. base H3 : 0,99 ; 0,98 ; 0,95. complément hors H3 : 0,01 ; 0,01 ; 0,03. complément H3 : 0,01 ; 0,02 ; 0,05. Base admise si P1 ≥ 50 % ; les deux émetteurs prennent θvs et θvt de l'émetteur 1 (p. 520)
- Rat_t systèmes alternés = hors mi-saison : 0,77 (hors H3), 0,64 (H3) ; mi-saison : 0,23 ; 0,36 ; chaque émetteur garde ses propres θvs et θvt (p. 521)
- Surface maximale chauffée par un système à air non gainé ou un appareil indépendant = 100 m² (SDB exclues), un niveau au-dessus au plus ; le système à air doit couvrir 1,3 fois les besoins de la partie A à la température de base (p. 510, 511, 515)

## Équations

- (796, p. 497) Pper = Ri x Ue ; Ri résistance entre le plancher chauffant et l'intérieur, Rsi inclus (m².K/W) ; Ue coefficient équivalent du plancher (W/m².K) ; plancher sur extérieur, vide sanitaire, sol ou local non chauffé. Dans les RSEE la valeur est déjà dans Per_dos : à lire, pas à recalculer
- (797, p. 498) Rat_ch_em = Rats_ch_em x Ratt_ch_em ; Rat_fr_em = Rats_fr_em x Ratt_fr_em ; Rat_s_*, Rat_t_* de l'émetteur ; déjà codé (emission.equivalent, variable rats)
- (798, p. 499) Rateff_ch_em = Rat_ch_em / Σ_em Rat_ch_em ; Rateff_fr_em = Rat_fr_em / Σ_em Rat_fr_em ; Σ Rat ≤ 1 ; si Σ = 0, l'émetteur équivalent est nul ; déjà codé (w = r / total). À conserver par émetteur pour (811) et (813) : aujourd'hui w n'est pas rendu
- (799, p. 499) Ratem_eq = Σ Rat_em ; Psd_eq = Σ Rateff_em x Psd_em ; Pem_eq = Σ Rateff_em x Pem_em ; δθvt_eq = Σ Rateff_em x δθvt_em ; δθvs_eq = Σ Rateff_em x δθvs_em (chaud et froid séparément) ; Psd_em = 0,5 ; Pem_em tableaux 86-87 ou saisi ; θvs tableaux 83-85 ou saisi, tableau 84 pour poêles ; θvt saisi, tableau 88 par défaut, tableau 89 pour poêles ; déjà codé sauf les cas poêles et inserts (tableaux 84 et 89) et les bornes de θvt saisi
- (800, p. 499) δθpresence_eq_ch = Σ Rateff_ch_em x θpresence_ch_em x Id_detection_presence_em ; θpresence_ch = -0,15 K ; chaud seulement ; déjà codé
- (801, p. 500) θi_eq_ch(h) = MAX(θiich(h) ; θiich_relance(h)) + δθvs_eq_ch + δθvt_eq_ch + δθpresence_eq_ch ; θi_eq_fr(h) = MIN(θiifr(h) ; θiifr_relance(h)) + δθvs_eq_fr + δθvt_eq_fr ; consignes de scénario et de relance (847, 848) ; déjà codé. En présence de brasseurs d'air, le texte ajoute δθcons_fr_BA(h) (fiche brasseurs) : non codé en Th-C
- (802, p. 500) θsd_eq_ch(h) = Psd_eq_ch x θi,moy(0,0)(h) + (1 - Psd_eq_ch) x θrm,moy(0,0)(h) ; idem froid avec Psd_eq_fr ; températures MOYENNES du pas à puissance nulle ; déjà codé (_sonde sur le résultat de thermique.pas, qui rend des moyennes)
- (803, p. 500 et 493) Si θsd_eq_ch < θi_eq_ch : Psd = Psd_eq_ch, Pem = Pem_eq_ch, θic = θi_eq_ch. Sinon si θsd_eq_fr > θi_eq_fr : Psd = Psd_eq_fr, Pem = Pem_eq_fr, θic = θi_eq_fr. Sinon aucune émission ; chaud prioritaire sur froid ; DIVERGENCE : le code vise la consigne non corrigée (thc.consigne_ch[h]) alors que la nomenclature définit θic comme la « température de consigne équivalente », c'est-à-dire θi_eq (corrigée des variations) ; la soustraction de (826) n'a de sens que dans ce cas. Voir points ouverts
- (804, p. 501) φcrois = a0 + a1 x θsd ; droite du groupe ; déjà codé sous forme pente / ordonnée
- (805, p. 501) θi,moy_0 = θi,moy(0,0) ; θrm,moy_0 = θrm,moy(0,0) ; θi,moy_10 = Pem x θi,moy(10,0) + (1 - Pem) x θi,moy(0,10) ; θrm,moy_10 = Pem x θrm,moy(10,0) + (1 - Pem) x θrm,moy(0,10) ; φconv = Pem x 10 x Agr, φrad = (1 - Pem) x 10 x Agr ; le code fait un seul essai à (Pem x 10 Agr ; (1 - Pem) x 10 Agr) : équivalent par linéarité du modèle
- (806, p. 501) θsd_0 = Psd x θi,moy_0 + (1 - Psd) x θrm,moy_0 ; θsd_10 = Psd x θi,moy_10 + (1 - Psd) x θrm,moy_10 ;  ; déjà codé
- (807, p. 501) a1 = 10 x Agr / (θsd_10 - θsd_0) (W/K) ; a0 = -a1 x θsd_0 ; le texte imprime 10 / (θsd_10 - θsd_0) : le facteur Agr est implicite puisque les 10 W/m² s'appliquent à Agr ; déjà codé (pente = Δθ / p_test)
- (808, p. 502) Si iclim : φcrois = a0 + a1 x θic ; sinon φcrois = MAX(a0 + a1 x θic ; 0) ; θic de (803) ; déjà codé (brut_fr seulement si climatise)
- (809, p. 502) φcrois_ch = MAX(0 ; φcrois) ; φcrois_fr = MIN(0 ; φcrois) ;  ; déjà codé (brut_ch, brut_fr)
- (810, p. 503) Si (θsd_fr > θi_fr et Autfr,eff(j) = 1) ou (θsd_ch < θi_ch et Autch,eff(j) = 1) : φutil = φcrois ; si φcrois ≠ 0 : idbch = φcrois_ch / φcrois, idbfr = φcrois_fr / φcrois ; sinon idbch = idbfr = 0. Sinon φutil = 0, idbch = idbfr = 0 ; Autch,eff, Autfr,eff saisons effectives (8.4) ; en Th-C celles de la génération ; déjà codé ; idbch, idbfr à exposer pour (813), (826), (836)
- (811, p. 503) Qsys_ch_em(h) = idem_chaud_em x Rateff_ch_em x MAX(0 ; φutil(h)) / (1 - Pper_em) ; Qsys_fr_em(h) = idem_froid_em x Rateff_fr_em x MIN(0 ; φutil(h)) / (1 - Pper_em) ; Wh sur le pas d'une heure (φutil en W) ; Qsys_fr_em négatif ; À CODER par émetteur. Le code actuel porte une moyenne pondérée de Pper non appliquée ; Σ Rateff / (1 - Pper_em) n'est pas 1 / (1 - Pper moyen)
- (812, p. 504) Ventilateurs locaux actifs si GestVCV_em > 0 et [(idem_chaud_em = 1 et Autch,eff(j) = 1) ou (idem_froid_em = 1 et Autfr,eff(j) = 1)] ;  ; Th-C uniquement. Hors de ces conditions : Qv_recirc_em = 0, Wvent_loc_em = 0
- (813, p. 504-505) Si irelance(h) = 1 : Qv = Qv_GV, W = PVCV_GV. Sinon si GestVCV = 1 : si iocc(h) = 1 et iocc(h-1) = 0 : [si Qsys_ch_em > Rateff_ch_em x Agr x SeuilVCV_pvmv_ch ou Qsys_fr_em < Rateff_fr_em x Agr x SeuilVCV_pvmv_fr : Qv = Qv_MV, W = PVCV_MV ; sinon Qv = Qv_PV, W = PVCV_PV] ; sinon Qv(h) = Qv(h-1), W(h) = W(h-1). Sinon si GestVCV = 2 : si ispv = 1 et idbch = 0 et idbfr = 0 : Qv = 0, W = PVCV_SPV ; sinon même test de seuil → MV ou PV. Sinon si GestVCV = 3 : si idbch = 0 et idbfr = 0 : Qv = 0, W = 0 ; sinon même test de seuil → MV ou PV ; Qv en m³/h, W en Wh (puissance sur une heure) ; iocc indicateur d'occupation de la zone ; seuils 20 et -20 Wh/m² ; état à conserver en gestion manuelle : (Qv, W) du pas précédent ; valeur initiale non donnée (point ouvert)
- (814, p. 505) Φvent_loc_vc_em(h) = Wvent_loc_em(h) ; toute la consommation est restituée à l'ambiance en chaleur ; l'heure d'injection dans le bilan thermique n'est pas dite ici (point ouvert) ; injecter en apport convectif au pas suivant
- (815, p. 505) Qm_recirc_em(h) = ρ_i,g(h-1) x Qv_recirc_em(h) / 3600 ; ρ masse volumique de l'air intérieur au pas précédent (fiche débits d'air) ; kg/s ; 
- (816, p. 505) Wvent_loc_tot(h) = Σ_em Wvent_loc_em(h) ; Wh ; consommation électrique du groupe à verser au Cep
- (817, p. 505) Φvent_loc_vc(h) = Σ_em Φvent_loc_vc_em(h) ; Wh ; 
- (818, p. 506) Si idtype2nd = 0 : θbatt_dim_em = 9 °C ; Type_2nd de la Distribution_Groupe_Froid de l'émetteur ; réseau fictif, détente directe
- (819, p. 506) Si idtype2nd = 1 : si idgest_fr = 1 : θbatt_dim = θdep_dim_fr - Δθem_dim_fr / 2 ; si idgest_fr = 2 : θbatt_dim = θret_dim_fr - Δθem_dim_fr / 2 ; Theta_Dep_Dim_Fr, Theta_Ret_Dim_Fr, Delta_Theta_Em_Dim_Fr (négatif dans les RSEE) ; idgest_fr = 3 non traité par le texte ; signe de Δθ à trancher (point ouvert)
- (820, p. 506) Qm_recirc_eff_em(h) = FBbatt x Qm_recirc_em(h) ; FBbatt = 0,8 ; idregul_batt = 0 (débit d'eau régulé progressivement)
- (821, p. 506) θbatt_em(h) = MAX(θbatt_dim_em ; θi,moy(h) + Qsys_fr_em(h) / (Ca x Qm_recirc_eff_em(h))) ; Qsys_fr_em négatif, en W (= Wh sur une heure) ; Ca = 1006 ; Qm en kg/s ; idregul_batt = 0 ; si Qm_recirc_eff = 0, θbatt = θbatt_dim (à protéger)
- (822, p. 506) θbatt_em(h) = θbatt_dim_em ;  ; idregul_batt = 1 (température de batterie constante)
- (823, p. 506) Qm_recirc_eff_em(h) = -Qsys_fr_em(h) / (Ca x (θi,moy(h) - θbatt_em(h))) ;  ; idregul_batt = 1 ; dénominateur à protéger si θi,moy ≤ θbatt
- (824, p. 506) ωsat_em(h) = 1e-3 x (HRsat / 100) x exp(18,8161 - 4110,34 / (θbatt_em(h) + 235,00)) ; HRsat = 100 ; kg/kg d'air sec ; émetteurs à ventilateurs locaux seulement
- (825, p. 506-507) Qsys_ch(h) = Σ_em Qsys_ch_em(h) ; Qsys_fr(h) = Σ_em Qsys_fr_em(h) ;  ; besoins effectifs totaux du groupe (c'est ce que le banc compare à O_B_Ch_annuel / O_B_Fr_annuel, sous réserve du point ouvert sur les pertes au dos)
- (826, p. 507) θx,fin = θx,fin(0,0) + (φutil_conv / 10) x (θx,fin(10,0) - θx,fin(0,0)) + (φutil_rad / 10) x (θx,fin(0,10) - θx,fin(0,0)) pour x = i, s, m, rm, op ; puis θop,fin -= idbch x (δθvt_eq_ch + δθvs_eq_ch) + idbfr x (δθvs_eq_fr + δθvt_eq_fr) ; les 10 sont des W/m² : φutil_conv / (10 x Agr) en toute rigueur ; la soustraction est imprimée sur la dernière ligne de l'accolade (θop,fin), le paragraphe précédent ne parle que de θop,fin ; DIVERGENCE : le code ne retranche pas les dérives. Le θop,fin corrigé alimente les protections mobiles, l'ouverture des baies et l'automate des saisons
- (827, p. 507) même interpolation pour les températures moyennes θi,moy, θs,moy, θm,moy, θrm,moy, θop,moy, avec la même soustraction sur θop,moy ;  ; θi,moy sert à (821), (823)
- (828, p. 507) φutil_conv(h) = Pemconv x φutil(h) ; φutil_rad(h) = (1 - Pemconv) x φutil(h) ; Pemconv de l'émetteur équivalent sollicité ; déjà codé (p_conv x p)
- (829, p. 507) Qsys_fr_em(h) += Qsys_lat_em(h) ; Qsys_fr(h) += Qsys_lat(h) ; après le bilan hydrique ; Th-C uniquement ; énergie latente négative comme Qsys_fr (convention de signe à fixer : (837) donne une valeur positive, à retrancher)
- (830, p. 525) ρ x V x dω_i,g/dt = Σ_j Qmaj_j(h) x (ωmaj_j(h) - ω_i,g) + A_int(h) - Σ_em Qm_recirc_eff_em(h) x MAX(0 ; ω_i,g - ωsat_em(h)) ; Qmaj débits d'air sec entrants (kg/s), ωmaj leur humidité, A_int apports internes (kg/s), V volume du groupe ; IMAGE dans le PDF, reconstituée d'après la nomenclature et les fragments ; débits entrants = débits sortants ; inertie hygroscopique négligée
- (831, p. 525) A_int(h) = A_int_occ(h) + A_int_hors_occ(h) ; scénarios ; IMAGE, reconstituée
- (832, p. 526) CalculHumiditeSpeFin(Rat, Qm, ωsat, T, ωini) : B = (Rat x Σ Qmaj + Rat x Qm) / (Rat x ρ_i,g(h-1) x V) ; A = (Rat x A_int + Rat x Σ Qmaj x ωmaj + Rat x Qm x ωsat) / (Rat x ρ x V) ; ωfin = A/B + (ωini - A/B) x exp(-B x T) ; Rat = Rateff_fr_em du local, Qm = débit de recirculation effectif (0 hors déshumidification), T en s ; IMAGE, reconstituée : solution exacte de l'ODE linéaire (830) sur un local de volume Rat x V. Le facteur Rat sur Qm est incertain (point ouvert) ; s'il porte sur tous les termes il se simplifie
- (833, p. 526) CalculHumiditeSpeMoy(Rat, Qm, ωsat, T, ωini) : ωmoy = A/B + (ωini - A/B) x (1 - exp(-B x T)) / (B x T) ; mêmes A et B ; IMAGE, reconstituée (moyenne temporelle de (832))
- (834, p. 527) CalculTemps(Rat, Qm, ωsat, ωini, ωfin) : T = -ln((ωfin - A/B) / (ωini - A/B)) / B ;  ; IMAGE, reconstituée (inversion de (832))
- (835, p. 527) Bbio : ω_i,g,fin(h) = CalculHumiditeSpeFin(1, 0, 0, 3600, ω_i,g,fin(h-1)) ; pas de déshumidification en Th-B ; IMAGE, reconstituée ; ρ_i,g(h-1) calculée dans la fiche débits d'air
- (836, p. 528-529) Th-C, pour chaque émetteur de froid em : si idbfr = 0 : ωfin_em = Fin(Rat, 0, 0, 3600, ω(h-1)), dt_deshu = 0. Sinon si ω(h-1) > ωsat_em : ωperm = Fin(Rat, Qm_eff, ωsat, 3600, ω(h-1)) ; si ωperm > ωsat : dt_deshu = 3600, ωfin = ωperm, ωmoy_deshu = Moy(Rat, Qm_eff, ωsat, 3600, ω(h-1)) ; sinon dt_deshu = Temps(Rat, Qm_eff, ωsat, ω(h-1), ωsat), ωmoy_deshu = Moy(Rat, Qm_eff, ωsat, dt_deshu, ω(h-1)), ωfin = Fin(Rat, 0, ωsat, 3600 - dt_deshu, ωsat). Sinon (ω(h-1) ≤ ωsat) : ωsans = Fin(Rat, 0, ωsat, 3600, ω(h-1)) ; si ωsans ≤ ωsat : dt_deshu = 0, ωfin = ωsans ; sinon dt_sec = Temps(Rat, 0, ωsat, ω(h-1), ωsat), dt_deshu = 3600 - dt_sec, ωfin = Fin(Rat, Qm_eff, ωsat, dt_deshu, ωsat), ωmoy_deshu = Moy(Rat, Qm_eff, ωsat, dt_deshu, ωsat) ; Fin, Moy, Temps = fonctions (832) à (834) ; IMAGE sur deux pages, reconstituée d'après les commentaires en clair du texte (« la déshumidification a lieu dès le début du pas », « s'est arrêtée au bout d'un temps dt_deshu », « se déclenche au bout d'un temps dt_sec »)
- (837, p. 529) Qsys_lat_em(h) = Lv_eau x dt_deshu(h) x Qm_recirc_eff_em(h) x MAX(0 ; ωmoy_deshu_em(h) - ωsat_em(h)) / 3,6 ; kJ/kg x s x kg/s = kJ ; / 3,6 → Wh ; valeur positive ; IMAGE, reconstituée
- (838, p. 529) ω_i,g,fin(h) = Σ_em Rateff_fr_em x ωfin_em(h) ; moyenne pondérée des locaux ; IMAGE, reconstituée ; si aucun émetteur de froid, un seul local avec Rat = 1
- (839, p. 529) Qsys_lat(h) = Σ_em Qsys_lat_em(h) ;  ; IMAGE, reconstituée
- (845, p. 539) Optimiseur, inoccupation prolongée : Δt_relance_ch(h) = ARRONDI(3 x (θext_reg_sup - θext(h)) / (θext_reg_sup - θext_base)) borné à [0 ; 3] h ; inoccupation courte : 1 h ; θext_reg_sup = 15 °C, θext_base température de base du site ; IMAGE, reconstituée ; durées fixes des tableaux 93 et 94 pour les types 1 et 2 ; calculée seulement en saison effective (Autch,eff(j) = 1)
- (846, p. 539) θiich_relance(0) = 0 °C ; θiifr_relance(0) = 100 °C ;  ; 
- (847, p. 539) Chaud, si Autch,eff(j) = 1 : si pch(h) < 1 : [si θiich_relance(h-1) < θiich_+ : (si pch(h + Δt(h)) = 1 et pch(h + Δt(h) - 1) < 1 : θiich_relance(h) = θiich_+ ; sinon 0) ; sinon θiich_relance(h) = θiich_relance(h-1)] ; sinon (pch(h) = 1) : 0. Hors saison : 0 ; pch indicateur de consigne (-1 absence > 48 h, 0 absence < 48 h, 1 présence) ; codé en équivalent (fenêtre [t0 - d ; t0[ avant chaque retour en occupation) avec trois écarts : voir points ouverts (optimiseur, arrondi, saison)
- (848, p. 540) Froid, si Autfr,eff(j) = 1 : si pfr(h) < 1 : [si Typepgrm_fr < 3 : (si θiifr_relance(h-1) > θiifr_+ : (si pfr(h + Δt) = 1 et pfr(h + Δt - 1) < 1 : θiifr_+ ; sinon 100) ; sinon θiifr_relance(h-1)) ; sinon (type 3) : θiifr_+] ; sinon (pfr = 1) : 100. Hors saison : 100 °C ;  ; déjà codé ; hors saison la valeur 100 °C est sans effet via MIN
- (849, p. 540) irelance_gr(h) = 1 si θiich_relance(h) > 0 ou θiifr_relance(h) < 100 ; sinon 0 ;  ; À CODER : emission.relance ne rend que la consigne fusionnée ; il faut aussi la fenêtre de relance (vrai pendant [t0 - d ; t0[, faux en occupation)
- (850, p. 540) irelance_CTA(h) = MAX sur les groupes desservis de irelance_gr(h) ;  ; IMAGE ; hors famille (CTA)

## Algorithme

```
PRÉPARATION (une fois par groupe, module emission.py)

    @dataclass
    class Emetteur:                      # un émetteur du RSEE (nœud Groupe/Emetteur)
        index: int
        chaud: bool; froid: bool          # Is_emetteur_chaud / _froid
        rat_eff_ch: float; rat_eff_fr: float   # (798), 0 si la fonction est absente
        pper: float                       # Per_dos (796)
        gest_vcv: int; ispv: bool
        p_gv, p_mv, p_pv, p_spv: float    # W
        qv_gv, qv_mv, qv_pv: float        # m³/h
        idregul_batt: int
        theta_batt_dim: float             # (818), (819) ; nan si pas d'émetteur de froid à recyclage
        id_dist_ch: int | None; id_dist_fr: int | None   # Distribution_Groupe_Chaud/Froid.Index

    def emetteurs(groupe) -> list[Emetteur]:
        # (797), (798) : rat_ch = Rat_s_ch x Rat_t_ch ; rat_eff_ch = rat_ch / Σ rat_ch (0 si Σ = 0) ; idem froid
        # θbatt_dim : dist = premier Distribution_Groupe_Froid de l'émetteur ;
        #   Type_2nd == 0 → 9 ; Gest_2nd_Fr == 1 → Theta_Dep_Dim_Fr - Delta_Theta_Em_Dim_Fr / 2 ;
        #   Gest_2nd_Fr == 2 → Theta_Ret_Dim_Fr - Delta_Theta_Em_Dim_Fr / 2 ; autre → 9 (point ouvert)

    equivalent(groupe, chaud) : inchangé, plus : tableau 84 (θvs poêles : Nombre_niveaux_desservis 1 → 0,9 ; 2 → 1,4)
    et tableau 89 (θvt poêles : Regulation_Poele_Ou_Insert thermostat → 2,0 ; manuelle → 2,5) quand la typologie
    est un poêle ou insert ; bornes de θvt saisi (max(saisie, 0,2 ou 0,4) en chaud ; min(saisie, -0,4) en froid).
    Retirer pertes_dos de EmetteurEquivalent (sans objet : l'équivalent n'a pas de pertes au dos, p. 498).

    relance(...) rend désormais (consigne_relance: ndarray, irelance: ndarray[bool]) :
      consigne_relance[h] = θ+ dans la fenêtre, 0 (chaud) ou 100 (froid) sinon ; irelance = fenêtre (849).
      Optimiseur (type 3 chaud, inoccupation prolongée) : à chaque h hors occupation en saison,
        d = min(3, max(0, floor(3 (15 - te[h]) / (15 - te_base) + 0,5)))      # (845), arrondi au plus proche
        relance si pch[h + d] == 1 and pch[h + d - 1] < 1 (égalité stricte de d, pas « ≥ »).
      Les relances ne sont calculées que si Autch,eff(j) = 1 (resp. Autfr,eff) : passer la saison effective
      par jour en argument (chauffage_impose) ou appliquer le masque après coup.

BOUCLE HORAIRE (groupe.calculer, mode thc), pour chaque heure h

    1. Besoins d'air, apports, sollicitations x : comme aujourd'hui, plus
         conv += phi_vent_loc_prec             # (814) : chaleur des ventilateurs locaux de l'heure précédente (état)
    2. libre = thermique.pas(g, x, mq)        # θ(0,0) moyennes
       cons_ch = consigne_ch_relancee[h] + chaud.correction        # (801)
       cons_fr = consigne_fr_relancee[h] + froid.correction        # (801) (+ δθ_BA si brasseurs, hors famille)
       sd_ch = psd x libre.i + (1 - psd) x libre.rm                # (802)
       sollicite = 'ch' if (chaud.rat > 0 and sd_ch < cons_ch) else ('fr' if (froid.rat > 0 and sd_fr > cons_fr) else None)   # (803)
    3. Si sollicite : essai à 10 W/m² x Agr réparti Pem / (1 - Pem) → sd0, sd10 ; a1 = 10 Agr / (sd10 - sd0) ; a0 = -a1 sd0   # (805) à (807)
       theta_ic = cons_ch si 'ch' sinon cons_fr                    # θic = consigne ÉQUIVALENTE corrigée (803) ; divergence avec le code actuel
       phi_crois = a0 + a1 x theta_ic ; si not climatise : max(., 0)          # (808)
       phi_crois_ch, phi_crois_fr = max(0, .), min(0, .)                       # (809)
    4. Saisons (810) : autorise = (sollicite == 'ch' and Autch_eff[j]) or (sollicite == 'fr' and Autfr_eff[j])
       phi_util = phi_crois si autorise sinon 0
       idbch = 1 si phi_util > 0 ; idbfr = 1 si phi_util < 0
    5. Répartition par émetteur (811), pour em dans emetteurs :
         qsys_ch[em] = em.chaud x em.rat_eff_ch x max(0, phi_util) / (1 - em.pper)
         qsys_fr[em] = em.froid x em.rat_eff_fr x min(0, phi_util) / (1 - em.pper)
       Qsys_ch = Σ qsys_ch ; Qsys_fr = Σ qsys_fr                             # (825)
    6. Températures finales et moyennes (826) à (828) : t = thermique.pas(g, x, mq, Pem x phi_util, (1 - Pem) x phi_util) ;
       fin = thermique.temperatures(g, x, t.mq, ...) ;
       top_fin = fin.op - idbch x (chaud.d_vt + chaud.d_vs) - idbfr x (froid.d_vs + froid.d_vt)   # (826), dernière ligne
       top_moy = t.op - (même soustraction)                                                      # (827)
       (point ouvert : appliquer ou non la soustraction à θi, θs, θm, θrm ; ne jamais corriger l'état mq)
       automate.heure(...), protections et ouverture utilisent top_fin corrigé.
    7. Ventilateurs locaux (812) à (817), pour em avec em.gest_vcv > 0 et ((em.chaud and Autch_eff[j]) or (em.froid and Autfr_eff[j])) :
         seuil = (qsys_ch[em] > em.rat_eff_ch x Agr x 20) or (qsys_fr[em] < em.rat_eff_fr x Agr x (-20))
         if irelance[h]:                      qv, w = em.qv_gv, em.p_gv
         elif em.gest_vcv == 1:
             if occ[h] and not occ[h-1]:      qv, w = (qv_mv, p_mv) if seuil else (qv_pv, p_pv)
             else:                            qv, w = etat_vcv[em]            # état (h-1) ; initial : (qv_pv, p_pv), point ouvert
         elif em.gest_vcv == 2:
             if em.ispv and not idbch and not idbfr: qv, w = 0, em.p_spv
             else:                            qv, w = (qv_mv, p_mv) if seuil else (qv_pv, p_pv)
         else:  # 3
             if not idbch and not idbfr:      qv, w = 0, 0
             else:                            qv, w = (qv_mv, p_mv) if seuil else (qv_pv, p_pv)
         etat_vcv[em] = (qv, w)
         qm_recirc[em] = rho_prec x qv / 3600                                  # (815), rho_prec = ρ_i,g(h-1), état
       sinon qv = w = 0.
       Wvent_loc_tot[h] = Σ w ; phi_vent_loc_prec = Σ w                        # (816), (817), réinjecté à l'étape 1 de h+1
    8. Batterie froide (818) à (824), pour em.froid et em.gest_vcv > 0 et idbfr :
         if em.idregul_batt == 0: qm_eff = 0,8 x qm_recirc[em] ; theta_batt = max(em.theta_batt_dim, top_moy_i + qsys_fr[em] / (1006 x qm_eff)) si qm_eff > 0 sinon theta_batt_dim
         else: theta_batt = em.theta_batt_dim ; qm_eff = -qsys_fr[em] / (1006 x (theta_i_moy - theta_batt)) si theta_i_moy > theta_batt sinon 0
         omega_sat[em] = 1e-3 x exp(18,8161 - 4110,34 / (theta_batt + 235))     # (824)
    9. Bilan hydrique (830) à (839) (seulement si un émetteur de froid à recyclage existe, sinon (835) pour tenir ω_i,g) :
         locaux = émetteurs de froid (Rat = rat_eff_fr) ou un seul local Rat = 1
         pour chaque local : algorithme (836) avec Fin/Moy/Temps (832) à (834), entrées Qmaj, ωmaj (fiche débits), A_int (scénarios), ρ_prec, V
           → omega_fin[em], dt_deshu[em], omega_moy_deshu[em]
         qsys_lat[em] = 2500 x dt_deshu x qm_eff x max(0, omega_moy_deshu - omega_sat[em]) / 3,6    # (837), Wh > 0
         omega_fin = Σ Rat x omega_fin[em]  (état ω_i,g,fin(h) pour h+1)                              # (838)
         qsys_fr[em] -= qsys_lat[em] ; Qsys_fr -= Σ qsys_lat                                          # (829), (839), signe à confirmer
    10. Sorties horaires du groupe : Qsys_ch (Wh), Qsys_fr (Wh, négatif), par émetteur qsys_ch[em], qsys_fr[em] vers id_dist_ch / id_dist_fr,
        Wvent_loc_tot (Wh électrique), top_fin corrigé, mq.

ÉTATS D'UNE HEURE À L'AUTRE : mq (déjà), top_fin, ti_fin (déjà), phi_vent_loc_prec, etat_vcv[em] (gestion manuelle), rho_prec, omega_i_g_fin, occ[h-1], θiich_relance(h-1) / θiifr_relance(h-1) si la relance est calculée au fil de l'eau plutôt que vectorisée.

RÉSULTAT (Besoins) : ajouter chauffage_em / refroidissement_em (dict index émetteur → ndarray Wh), ventilateurs_locaux (ndarray Wh), latent (ndarray Wh). Le banc compare Σ chauffage (= Qsys_ch avec pertes au dos) à O_B_Ch_annuel, et Wvent_loc_tot au résidu O_Cef_aux_ventilateur_annuel - ventilateurs.py.
```

## Sorties RSEE pour le banc

- `O_B_Ch_annuel` (Sortie_Groupe_C (aussi Sortie_Zone_C, Sortie_Batiment_C), kWh/m² (Agr) par an ; besoins de chauffage au niveau des émetteurs (Qsys_ch, 825) ; tranche θic corrigée ou non, pertes au dos, θop,fin corrigé)
- `O_B_Ch_mois` (Sortie_Groupe_C / Sortie_Mensuelle (Mois, Valeur), kWh/m² par mois ; localise les écarts de relance et de saison)
- `O_B_Fr_annuel` (Sortie_Groupe_C, Sortie_Zone_C, Sortie_Batiment_C, kWh/m² par an ; besoins de froid, latent inclus ou non (point ouvert) ; groupes Is_Climatise = 1)
- `O_B_Fr_mois` (Sortie_Groupe_C / Sortie_Mensuelle, kWh/m² par mois)
- `O_Cef_aux_ventilateur_annuel` (Sortie_Groupe_C, kWhef/m² par an ; auxiliaires de ventilation : le résidu par rapport à ventilateurs.py sur un groupe à Gest_vcv > 0 (cassette des bureaux : 13 / 8 / 6 W) mesure Wvent_loc_tot (816) si le poste l'inclut)
- `O_Cef_aux_ventilateur_mois` (Sortie_Groupe_C / Sortie_Mensuelle, kWhef/m² par mois ; en bureaux non climatisés, nul hors saison de chauffage si les ventilateurs locaux y sont (812))
- `O_Cef_auxv_elec_annuel` (Sortie_Groupe_C, kWhef/m² ; variante électrique du même poste)
- `O_Cef_elec_imp_auxvent_annuel / O_Cef_elec_cons_auxvent_annuel` (Sortie_Zone_C, kWhef/m² ; même poste au niveau zone, pour localiser où le moteur range Wvent_loc_tot)
- `O_Cef_ch_annuel, O_Cef_fr_annuel` (Sortie_Groupe_C, kWhef/m² ; alternative si Wvent_loc_tot est rangé dans le chauffage ou le froid plutôt que dans les auxiliaires)
- `O_Cef_fr_elec_annuel` (Sortie_Groupe_C, kWhef/m² ; sensible au latent via la génération froid)
- `Nbhcharge_0_fr, Nbhcharge_0_10_fr ... Nbhcharge_HF_fr (idem _ch)` (Sortie_Generation / Sortie_Generateur, heures par classe de taux de charge ; Nbhcharge_0_ch compte les heures sans besoin : valide le découpage saisons / relance / idbch sans passer par la génération)
- `O_Idsousdim_Court_Ch, O_Idsousdim_Long_Ch (et _Fr)` (Sortie_Generation, indicateurs de sous-dimensionnement ; sensibles à la pointe de besoin (relance, θic corrigée))
- `O_SHAB, O_SU` (Sortie_Groupe_C, m² ; Agr de normalisation)

## Points ouverts (à trancher au codage)

- DIVERGENCE PROBABLE, forte incidence : cible de la puissance (803, 808). Le code vise la consigne non corrigée (thc.consigne_ch[h]) ; la nomenclature (p. 493) définit θic comme « température de consigne équivalente », nom donné à θi_eq_ch = MAX(consigne, relance) + δθvs + δθvt + δθpresence (p. 492 et 500), et (826) retranche ensuite ces dérives de θop,fin, ce qui n'a de sens que si la puissance les a produites. Banc : O_B_Ch_annuel sur les 18 groupes effet joule de cas 17 déjà à +12,6 % (ventilation.py) : viser θi_eq (environ +2,4 K) devrait augmenter le besoin calculé ; si l'écart se creuse, la lecture inverse est la bonne.
- DIVERGENCE : (826) et (827) non appliquées. θop,fin et θop,moy doivent être diminués de idbch x (δθvt_eq_ch + δθvs_eq_ch) + idbfr x (δθvs_eq_fr + δθvt_eq_fr). Incertitude : l'accolade imprimée porte la soustraction sur la ligne θop seulement, le texte au-dessus ne parle que de θop,fin ; appliquer à θi, θs, θm, θrm aussi ? Jamais à l'état mq (sinon la dynamique change). Banc : O_B_Fr_annuel et dates de saison (la soustraction retarde les seuils d'inconfort de l'automate des saisons et des protections mobiles).
- DIVERGENCE : pertes au dos (811). emission.equivalent porte une moyenne pondérée Per_dos jamais appliquée ; le texte divise la part de chaque émetteur par (1 - Pper_em). Dans les deux RSEE lus Per_dos = 0 ; chercher au banc un projet à plancher chauffant sur vide sanitaire (Per_dos > 0) et comparer O_B_Ch_annuel avec et sans division (le texte dit « demande transmise au réseau de distribution » : O_B_Ch inclut probablement les pertes au dos).
- DIVERGENCE : poêles et inserts. Tableaux 84 (θvs 0,9 / 1,4 selon Nombre_niveaux_desservis) et 89 (θvt 2 / 2,5 selon Regulation_Poele_Ou_Insert) non codés ; les champs existent dans le RSEE. La typologie RSEE qui désigne un poêle n'est pas connue (Typologie_Emetteur_Chaud 3 = plancher d'après le code ; les poêles sont dans la ligne 0,50 du tableau 86 avec les planchers). Banc : maisons individuelles à poêle bois (O_Cef_bois_annuel > 0), O_B_Ch_annuel.
- Variation temporelle saisie : les bornes (0,2 K effet joule, 0,4 K autres, -0,4 K froid) et le +0,5 K des valeurs justifiées ne sont pas appliqués ; le code lit Statut_Variation_Temporelle = 2 comme « justifiée » sans que le texte donne les codes. Les deux RSEE ont Statut 0 avec 0,2 et 0,4 : cohérent avec « certifiée aux bornes ». Banc : projets à Statut 1 ou 2, O_B_Ch_annuel.
- Couple_Regulateur_Emetteur_Chaud : correspondance 0 → sans arrêt total (2,0 K), 1 → avec (1,8 K) déduite, non donnée par le texte. Banc : groupes à Delta_Temp_vt_ch = 0 (valeur par défaut) ; écart de 0,2 K sur O_B_Ch_annuel.
- Relance (847) : trois écarts du code. a) Optimiseur : le code démarre si Δt(t0 - k) ≥ k ; le texte exige pch(h + Δt(h)) = 1 et pch(h + Δt(h) - 1) < 1, soit Δt(h) = k exactement, ce qui peut donner aucune relance certains matins. Le groupe des bureaux (Type_Pgrm_Ch = 3) est le cas test : O_B_Ch_mois. b) round() de Python arrondit au pair (round(2,5) = 2) : utiliser floor(x + 0,5). c) La relance n'est calculée qu'en saison effective ; le code la calcule toute l'année et la consigne relancée entre dans automate.heure, donc dans la détermination des saisons : masquer par Autch,eff(j).
- Relance : indicateur irelance (849) à produire, préalable aux ventilateurs locaux (813, régime GV). Vérifier au banc que le résidu O_Cef_aux_ventilateur_annuel du groupe cassette (Gest_vcv = 3, bureaux) est positif : 13 W x heures de relance + 6 ou 8 W x heures avec besoin ≈ 10 à 20 kWh par an sur 241 m², soit 0,04 à 0,08 kWh/m².
- Où est rangée Wvent_loc_tot dans le Cep ? La fiche ne le dit pas. Candidats : O_Cef_aux_ventilateur_annuel (auxiliaires de ventilation), O_Cef_ch_annuel. Banc : groupe cassette des bureaux (seul émetteur, Gest_vcv = 3) : comparer ventilateurs.py + Wvent_loc_tot à O_Cef_aux_ventilateur_annuel, et le profil O_Cef_aux_ventilateur_mois (nul hors saison de chauffage si les ventilateurs locaux y sont, puisque le groupe n'est pas climatisé).
- Heure d'injection de Φvent_loc_vc (814) dans le bilan thermique : la fiche 8.1 ne dit pas si la chaleur entre au pas h (ce qui créerait une boucle avec φutil) ou h + 1. Proposition : apport convectif à h + 1. Incidence faible (6 à 13 W). Banc : O_B_Ch_annuel du groupe cassette.
- Valeur initiale de l'état des ventilateurs en gestion manuelle (Gest_vcv = 1) avant le premier passage en occupation : non donnée ; proposer petite vitesse. Le texte dit aussi « permanent en occupation et en inoccupation », donc en inoccupation hors relance on garde (h - 1), y compris la nuit.
- Masse volumique ρ_i,g(h - 1) (815) et débits d'air sec Qmaj avec ωmaj (830) : viennent de la fiche C_VEN_Débits d'air, non lue ici ; aeraulique.py ne rend pas ρ. Prendre ρ = 1,2 kg/m³ en première approche, à confirmer.
- θbatt_dim (819) : signe de Delta_Theta_Em_Dim_Fr. Les RSEE portent -1 (négatif en froid). Avec Δθ = départ - retour (négatif), θdep - Δθ/2 est bien la moyenne départ/retour pour idgest_fr = 1, mais θret - Δθ/2 ne l'est pas pour idgest_fr = 2. Cas idgest_fr = 3 non traité. Les deux RSEE ont Type_2nd = 0 (9 °C), donc sans incidence ici. Banc : groupe climatisé à ventilo-convecteurs sur réseau hydraulique (Type_2nd = 1), O_B_Fr_annuel.
- O_B_Fr_annuel inclut-il l'énergie latente (829) ? Et signe : (837) donne une valeur positive alors que Qsys_fr est négatif ; le « += » de (829) suppose Qsys_lat négatif ou une convention de valeur absolue. Banc : groupes climatisés à émetteur de froid Gest_vcv > 0 (VCV) contre groupes à plafond rafraîchissant (sans recyclage, donc sans latent) : écart O_B_Fr_annuel au-delà du sensible.
- Toutes les équations de la fiche 8.3 (830 à 839) et (845), (850) sont des IMAGES : la spécification les reconstitue d'après la nomenclature, les commentaires en clair et la physique (ODE linéaire du premier ordre). Doute résiduel sur (832) : Rateff multiplie-t-il aussi Qm_recirc_eff (auquel cas il se simplifie partout) ou seulement les termes du groupe ? Les fragments de texte montrent « Rat » devant chaque terme. Banc : seul O_B_Fr_annuel d'un groupe à VCV peut trancher, faiblement.
- Émetteur équivalent nul : si Σ Rat_ch = 0 (groupe sans émetteur de chaud) mais θsd < θi_eq_ch, le code choisit tout de même le chaud (em = thc.chaud) et n'évalue pas le froid ce pas-là. Le texte dit seulement que l'équivalent est nul ; traiter « pas d'émetteur » comme condition fausse dans (803) de sorte que le froid puisse être sollicité.
- Brasseurs d'air en Th-C : δθcons_fr_BA(h) de la fiche 8.32 doit s'ajouter à θi_eq_fr (p. 500) ; ThC ne porte pas de brasseurs alors que ThD les a. Banc : O_B_Fr_annuel des logements à brasseurs.
- Fiche 8.2 : les tableaux de Rat_s (p. 511, 512, 513, 515) sont des IMAGES (formules S_A / (S_A + S_B + S_SDB) etc. illisibles) ; seuls les Rat_t sont lisibles et donnés dans parametres_conventionnels. Rien à coder dans le moteur : contrôle de saisie éventuel (Σ Rat_s_ch x Rat_t_ch ≤ 1, Rat_t conformes aux tableaux par zone climatique, surface d'un système à air non gainé ≤ 100 m²). Le code 1 à 5 de Typologie_Emetteur_Chaud reste une déduction du banc (docstring d'emission.py).
- Type_Pgrm_Fr = 0 (groupe non climatisé) n'existe pas dans le texte (1 à 3) : lire comme « sans objet », pas de relance froid.

## Tableaux en image dans le PDF

- Fiche 8.1, p. 499 : fragments de (798) et des notations Rat_eff en fin de page (lisible par ailleurs)
- Fiche 8.1, p. 500 : conditions de (803) en caractères éclatés (reconstituées : θsd_eq_fr > θi_eq_fr ; θsd_eq_ch < θi_eq_ch)
- Fiche 8.1, p. 501 : Figure 87 (droite du groupe) ; p. 502 : Figure 88 (intersection) : images sans équation perdue
- Fiche 8.1, p. 504 : condition de (813) pour GestVCV = 2 en caractères éclatés (reconstituée : ispv = 1 et idbch = 0 et idbfr = 0)
- Fiche 8.1, p. 507 : (826) et (827) tronquées en fin de ligne (fin des termes θx,fin(0,10) - θx,fin(0,0))
- Fiche 8.2, p. 510 et 519 : formule Rat_em = Rat_s_em x Rat_t_em en caractères éclatés
- Fiche 8.2, p. 511, 512, 513, 515 : tableaux des ratios spatiaux Rat_s (formules S_A / (S_A + S_B + S_SDB) etc.) illisibles ; lignes Rat_t lisibles
- Fiche 8.2, p. 516 à 518 : Figures 89, 90, 91 (puissances base / appoint selon θext)
- Fiche 8.3, p. 525 : équation (830) et (831) entièrement en caractères éclatés
- Fiche 8.3, p. 526 à 527 : fonctions (832), (833), (834) entièrement illisibles
- Fiche 8.3, p. 527 : (835) et notes associées illisibles
- Fiche 8.3, p. 528 à 529 : algorithme (836) sur deux pages, seuls les commentaires entre parenthèses sont lisibles
- Fiche 8.3, p. 529 : (837), (838), (839) illisibles
- Fiche 8.5, p. 539 : équation (845) de la durée de relance de l'optimiseur illisible ; (847) lisible
- Fiche 8.5, p. 540 : (850) relance CTA illisible
- Fiche 8.4 (hors famille), p. 530 : Figure 92

## Estimation

Lignes de code (hors tests) :
- emission.py : Emetteur + emetteurs() (lecture, 797, 798, 818, 819, poêles tableaux 84 et 89, bornes θvt) : 60 à 80 lignes ; relance() rendant aussi irelance, optimiseur conforme, masque de saison : 30 lignes modifiées.
- groupe.py (boucle Th-C) : θic corrigée (1 ligne), (826)/(827) sur θop (5 lignes), répartition (811)/(825) et nouveaux champs de Besoins (25 lignes), ventilateurs locaux (813) à (817) avec états (50 lignes), batterie froide (820) à (824) (25 lignes).
- Nouveau module hydrique.py : fonctions Fin/Moy/Temps (832 à 834), algorithme (836), (837) à (839), (835) pour le Bbio : 90 à 120 lignes ; dépend d'entrées non encore disponibles (A_int des scénarios, Qmaj/ωmaj des débits d'air, ρ).
- banc/cep.py : colonnes ventilateurs locaux et latent, résidu auxiliaires : 20 lignes.
Total : 300 à 350 lignes.

Difficulté : moyenne pour la répartition, les pertes au dos, θic, (826) et les ventilateurs locaux (texte lisible, algorithme explicite, deux RSEE de test dont un avec cassette Gest_vcv = 3) ; élevée pour le bilan hydrique (toutes les équations sont des images, entrées amont absentes, effet sur le Cep limité aux groupes climatisés à ventilo-convecteurs). Risque principal : la lecture de θic (corrigée ou non) change le besoin de chauffage de plusieurs pourcents ; à trancher en premier au banc sur O_B_Ch_annuel avant tout le reste. Ordre conseillé : 1) θic et (826) ; 2) répartition et pertes au dos ; 3) relance conforme + irelance ; 4) ventilateurs locaux et poste Cep ; 5) batterie froide et hydrique quand les débits d'air sec et l'humidité des scénarios seront disponibles.
