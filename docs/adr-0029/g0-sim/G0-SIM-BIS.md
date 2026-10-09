# G0 du lot SIM-BIS (SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS, S2-bis)

Adjugé par l'orchestrateur le 2026-10-04 23:02:56 UTC (heure produite par le script). Rattachement : ADR-0029 révision 3, acceptée (§2.4, §2.7, §6
lot 4, §8 ; ajout daté après l.141 sur les sources de la méthode des rotations) ; G0 de vague `docs/adr-0029/G0-lots-S2BIS.md` ;
sorties du lot PLAN-S2BIS (`docs/adr-0029/plan-s2bis/`). Pièces : proposition du rédacteur (`PROPOSITION.md`, worker
`claude-opus-5-5`, sha256 `0e78afab…`, 55 exigences E-S-01 à E-S-55, 22 questions Q-S-01 à Q-S-22) ; avis de l'advisor (`AVIS.md`,
`claude-fable-5-1` effort medium, sha256 `aaf70a4f…` : 15 recommandations adoptées, 7 modifiées, aucune rejetée).

## Adjudications
1. **La proposition est le contenu de ce G0** (périmètre, exigences, règle de n_s et T_max, règle de niveau, cellules, sous-lots,
   tests, critères de sortie, actes de l'investisseur), **corrigée par l'avis** : pour chacune des 22 questions, la recommandation de
   l'avis s'applique telle qu'écrite, y compris ses sept modifications (Q-S-03, Q-S-04, Q-S-06, Q-S-09, Q-S-11, Q-S-13, Q-S-21).
2. **Q-S-03** : l'échelle des durées tourne aux trois niveaux de calibration C0, C1, C2 ; la durée déclarée est celle de C2 ; si
   W*(C2) > 16 semaines ≥ W*(C0), le lot PLAN-S2BIS-2 (identification du groupement par source) passe **avant** toute question de durée
   à l'investisseur (acte A-2) : aucun allongement n'est demandé sur un artefact de calibration.
3. **Les sept écarts à la lettre de l'ADR** (§11 de la proposition, §4 de l'avis) sont adoptés et portés par l'ajout daté du même jour
   à l'ADR-0029 (après l'ajout du G0 de COLLECTE-BIS) ; SHOGEN-S2BIS-SIM-1 n'est pas fermé : sa portée est réduite et re-datée.
4. **Items** : les huit items du §12 sont formés (annexe B.61), avec les précisions de l'avis ; la portée de SHOGEN-S2BIS-ENREG-ROLE-1
   s'étend à `scripts/sim-bis` et SHOGEN-S2BIS-P1-ESTIMATION-1 s'applique à l'estimation du §6.1.
5. **Décisions réservées à l'investisseur** [INV] : durée au-delà de 16 semaines (A-2) ; serveur de calcul au-delà de 72 h de mur
   (A-3) ; information, dans A-2, que 20 % de NON ÉVALUABLE sous H0 est la probabilité acceptée qu'une campagne sans incident ne
   tranche pas. Aucune dépense sans acte écrit.
6. **Lieu du calcul** : hôte de session, lots détachés de 90 min au plus, versement par phase, graines par réplication ; bibliothèque
   standard seule (R-8 sans objet tant qu'aucune dépendance n'est proposée).
7. **Écarts du rédacteur** E-1 à E-6 (§14 de la proposition) : acceptés ; E-2 (sondes de temps hors dépôt, aucun taux de rejet
   imprimé) et E-6 (barres obliques inverses dans des heredocs, contrôlées) déclarés.

## Suite
Sous-lots SB-1 à SB-15 (§6 de la proposition) par un worker `claude-opus-5-5` effort max, tranche par tranche, G2 neuve à 100 %,
chaque diff ≤ 200 lignes de code ; exécution provisoire sur le pool de l'ADR pour clore la conception et débloquer RB-7 ; exécution
finale épinglée après le gel des pools.

*Ajout daté du 2026-10-05 01:45:03 UTC (relecture G2 de la tranche 1, `revue-t1/`)* : (1) **numérotation** : les sous-lots sont **SB-0 à SB-14** (proposition §6.1) ; « SB-1 à SB-15 » au § Suite ci-dessus est une erreur de compte de l'orchestrateur. (2) **E-S-10** n'est pas réalisable à la lettre : l'histogramme des épisodes d'EP compte tous les épisodes, censurés compris (`scripts/plan-s2bis/episodes.py` l.47-50 ; EP l.13-14 : 332 épisodes dont 51 censurés) ; SB-3 emploie la loi « tous épisodes » d'EP avec une limite écrite (écart des moyennes complets / tous : −0,035 à +0,134 fenêtre en calme, −0,023 à +0,015 en stress, mesuré par le réviseur) ; recours : PLAN-S2BIS-2, selon l'adjudication 2. (3) Questions de la tranche 1 adjugées : `Fraction(cellules, n_s)` ; indice de réplication à 0 ; composants des flux en liste fermée sous schéma avant E0 ; `math.nextafter` admis au sens d'E-S-43 (nextUp IEEE 754, vérifié par le réviseur) ; pas de garde réseau dans les tests ; lundi de référence, table géométrique de 4 096 rangs et garde de 128 bits scellés tels quels à E0.

*Ajout daté du 2026-10-05 15:05:43 UTC (heure produite par le script d'écriture) (lot PLAN-S2BIS-2 : G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md`, proposition, avis de l'advisor,
périmètre réduit et cp-1 de cet ajout dans le même dossier ; option B de l'avis de la tranche 4 ; motif : constat du point 9
du rapport de la tranche 4, vu à la mesure de mise au point E-4 du 2026-10-05 et recompté par la relecture G2 de la tranche 4
(`docs/adr-0029/g0-sim/revue-t4/`), et §3.2 de l'avis de la tranche 4)* :
(1) **C1** : dans chaque strate, point p de la grille d'E1 qui minimise Q₁(p) = Σ_u Σ_ℓ (ln F̄_u,p(ℓ) − ln F_u(ℓ))², somme
sur les hôtes u du pool d'E1 (D1-bis) dont F_u(ℓ) est défini, sans garde sur leur nombre de cellules d'écart, et sur les ℓ de
la grille de calibration où la garde de `fiv_unites.txt` est tenue. Même type de série des deux côtés : série d'écart
(`r1.ECARTS`) côté S2 ; D*(u) = H(u) ∪ F(u, BTC) côté modèle, sans hors-enveloppe (Q-T4-13). F_u(ℓ) = FIV_série de
`fiv_unites.txt`, chaîne de r1 prise en rationnel exact depuis son écriture décimale, comme EP (E-S-37). F̄_u,p(ℓ) = moyenne
exacte, sur les réplications définies parmi les 200 du point p (celles de C2), du FIV exact de la série D*(u) sur le masque
mesuré. Logarithmes par `Decimal.ln` sous le contexte de r1 ; égalités au plus petit κ, puis τ_D, puis φ ; un point dont un
F̄_u,p(ℓ) retenu est indéfini est écarté. La convention « milieu des logs de C0 et de C2 à ℓ = 240 » est retirée.
(2) **C2** : critère sur ln FIV_série de I_t contre la courbe D1-bis d'EP (EP l.128-161), inchangé. **C0** : inchangé (aucun
régime).
(3) **Calendrier d'E1** : positions présentes = masque des fenêtres évaluables de J28 versé par PLAN-S2BIS-2
(`masque_j28.txt`), empreinte contrôlée, au lieu des positions de la portée hors D5, pour C0, C1 et C2. Le masque s'applique
après génération (à vérifier par la G2 du diff d'intégration) ; il ne touche qu'E1 : E2 et E3 gardent le calendrier de S2-bis.
(4) **Nature** : C1 : groupement propre mesuré par hôte, déclaré borne haute du groupement propre, par hypothèse : les
absences de l'observateur unique ajoutent de la dépendance sérielle aux séries d'écart (ADR l.38 ; §5 de l'avis du G0 de
PLAN-S2BIS-2) ; la troncature par le masque joue en sens inverse aux grands ℓ ; la sensibilité au voisinage des lacunes
(PLAN-S2BIS-2, Q-P2-10) en chiffre la part. Ce sens n'est pas démontré pour la durée, d'où les trois W* de (5) ; au bord de la
grille, (8) s'applique. C2 : point de la grille le plus proche de la courbe de I_t ; garde-fou imprimé, plus « cas le plus
défavorable plausible » depuis le constat de la tranche 4
(relecture G2 de la tranche 4, `revue-t4/`, constat du point 9, pt 4).
(5) **Durée** : la règle du §3 de la proposition de SIM-BIS se lit au niveau C1 pour l'acte A-2 : W retenue = max(16,
W*(C1)). Le fond de référence de la cible (§3 pt 1 de la proposition de SIM-BIS ; ADR l.399 pt 2, « groupement au niveau C2 »)
passe au niveau C1 : la confirmation à 10⁴ réplications à la durée retenue et le bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` (§3
pts 3 et 6) s'y calculent ; l'échelle des durées tourne toujours aux trois niveaux (AVIS-G0 Q-S-03, modification 1) et P-cible
à C2 (N3) reste imprimée. A-2 est posé si, et seulement si, W*(C1) > 16 ou W*(C0) > 16, ou si aucune durée de l'échelle ne
tient (a) à (c) à l'un de ces deux niveaux (§3 pt 4 de la proposition de SIM-BIS) ; jamais sur W*(C2) seul. Si
W*(C0) > 16 ≥ W*(C1), A-2 est posé sans détour, comme le prévoyait l'avis du G0 (Q-S-03), W retenue reste 16 et la question
dit que le seul niveau mesuré, C1, n'exige pas l'allongement. Si A-2 n'est pas posé, et en particulier si W*(C1) ≤ 16 < W*(C2)
avec W*(C0) ≤ 16, aucune question n'est posée : la durée écrite au paquet reste 16 semaines, la puissance à la cible y est
imprimée aux trois niveaux et une phrase de limite nomme C2. La question A-2, si elle est posée, porte W*(C0), W*(C1), W*(C2),
la phrase de (4), le 20 % sous H0 (adjudication 5) et, le cas échéant, la phrase de (8). Ce point remplace « la durée déclarée
est celle de C2 » (adjudication 2) ; l'ajout daté du même jour à l'ADR-0029 porte le même changement à l'ajout daté du
2026-10-04 23:02:56 UTC (l.399, pts 2 et 5). Dans (8)(iii), « sans question » s'entend au titre de (8) seul ; si A-2 est posé
par la règle ci-dessus, il porte la phrase de (8).
(6) **Contrôles et impressions** : SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 sur C1 dès son épinglage. SB-11 imprime, par strate et
par hôte, les résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) aux ℓ retenus, le point qui minimiserait Q₁ pour cet hôte seul (diagnostic,
jamais candidat), le nombre de réplications à FIV indéfini, et la loi des pauses du modèle à C1 sur le masque, à côté de
`intervalles.txt` ; et, par point et par ℓ, l'écart-type exact (racine par `Decimal.sqrt` sous le contexte de r1, à
l'impression seulement) des FIV définis parmi les 200 réplications, pour la série de I_t.
(7) **Ordre** : cet ajout est inscrit au G0 de SIM-BIS avant l'exécution de PLAN-S2BIS-2 et avant l'inscription au JOURNAL du
sha256 du code de PLAN-S2BIS-2 ; cette antériorité est consignée par deux heures `date -u`. Un cp-1 bref de cet ajout, par un
validateur frais, passe avant cette inscription (Q-P2-13 ; rapport `docs/adr-0029/g0-plan2/CP1-AJOUT.md`). `e1.ell_c1` est
retiré de `parametres.json` de SIM-BIS (sans objet). E0 attend le versement de PLAN-S2BIS-2 et le diff de SIM-BIS qui lit ses
sorties ; aucune exécution provisoire avec la C1 de la lettre d'E-S-38. RB-7 attend aussi : l'exécution provisoire du § Suite
de ce G0 (« pour clore la conception et débloquer RB-7 ») se fait avec la C1 de cet ajout, donc après E0. Le texte d'E-S-38
reste tel quel.
**(8) Bord de la grille.** Dans une strate, C1 est « au bord » si l'une de ses trois coordonnées est la valeur extrême de sa grille (φ = 0,1, κ = 50 ou τ_D = 4 320 ; E-S-38) **ou** si, aux ℓ retenus ≥ 60, le résidu ln F̄_u,C1(ℓ) − ln F_u(ℓ) est négatif pour au moins six des dix hôtes du format. Alors : (i) C1 reste le point retenu (aucun point hors grille, aucune seconde sélection) ; (ii) la limite de SHOGEN-SIM-BIS-FIV-IDENTIF-1 s'écrit « dans la strate s, la famille E1 n'atteint pas les FIV_u mesurés ; C1 y est une borne basse de la mesure, et « borne haute » ne s'applique pas » ; (iii) les trois W* sont imprimés et, si W*(C1) ≤ 16 et que C1-calme est au bord, le paquet dit que les 16 semaines reposent sur un niveau que la famille ne peut pas dépasser : information à l'investisseur à l'accord A-1 de S-2, sans question ; si W*(C1) > 16, A-2 porte la même phrase. (iv) Le bord est constaté par le script, par une ligne nommée, jamais par une lecture humaine.
Précision d'adjudication à (8) : la seconde condition se lit « pour au moins six des dix hôtes du format, le résidu ln
F̄_u,C1(ℓ) − ln F_u(ℓ) est négatif à chacun des ℓ retenus ≥ 60 » ; la ligne nommée de (8)(iv) imprime, par strate, le nombre
d'hôtes qui satisfont cette condition et la liste des ℓ retenus ≥ 60.
(9) **Filet** : le déclencheur « W* différente entre C0 et C2 » de SHOGEN-SIM-BIS-FIV-IDENTIF-1 est retiré ; PLAN-S2BIS-2
précède E0 dans tous les cas, que W*(C0) et W*(C2) diffèrent ou non. Le cas où C1 n'atteint pas les FIV_u mesurés relève de
(8), jamais d'un déclencheur nouveau ; l'item reste ouvert jusqu'à la sortie d'E1 épinglée, où sa limite s'écrit selon (4)
et (8).

**Ajout daté du 2026-10-09 13:49:50 UTC (heure produite par `date -u`) : strate sans fenêtre retenue (SHOGEN-SIM-BIS-NPRIME-NUL-1 ; SB-11x, SB-11y ; adjudication de l'orchestrateur, option (b), sur l'avis de l'advisor ; G2 neuve de SB-11x).** Sous E-S-28 et E-S-52 de la proposition.
(1) **Cas.** À T_max, `calendrier.retenues` peut ne retenir aucune fenêtre évaluable dans une strate s (n′_s = 0). Pour cette strate, `executer.replication` n'appelle ni `regle` (tester, oracle, loi_evenements, filtrer) ni `variante` (tester, deux_modes). `regle` garde son contrat : n ≥ 1, sinon REGLE/entier (contrat RB-6 §4 ; SHOGEN-SIM-BIS-CONTRAT-RB6-1).
(2) **Enregistrement.** Chaque classe de la strate reçoit l'enregistrement que `regle.tester` rend sur des séries vides : valeur NON ÉVALUABLE ; causes = `list(regle.CAUSES)` = [unites, k_crit, runs, n_prime] ; K = 0, runs = 0, unites = 0 ; S = 0 (l'entier) si S est suivie, sinon None ; aucun arrêt anticipé : C = R (R de la cellule), C1 = 0, C_S = R si S est suivie, sinon None, r = R. Sous-bloc « avec » (critère collectif actif) : les mêmes champs, plus retirees = [] et indice = Fraction(0), sérialisé « "0" » dans le JSON canonique. Sous-bloc variante[d], pour chaque diviseur de la cellule : les mêmes champs sans S, C_S = None et N = ⌊0/d⌋ = 0. L'égalité avec `regle.tester`, `regle.filtrer` et `variante.tester` sur séries vides est vérifiée en octets du JSON canonique, à n = 1 et à plusieurs n_s.
(3) **Ce que la strate n'a pas.** Ni compte d'événements (E-S-34) ni clé « evenements » ; aucune comparaison d'oracle d'E-S-29 : le sous-ensemble pré-déclaré reste les 200 premières réplications, et le nombre de comparaisons effectives par cellule est imprimé au paquet.
(4) **Comptage.** La réplication est comptée (E-S-45), jamais refusée. Au comptage d'E-S-52, elle ajoute 1 à NON ÉVALUABLE, à chacune des quatre causes, à l'information insuffisante et à la combinaison « unites+k_crit+runs+n_prime ». Le nombre de réplications à n′_s = 0 est imprimé par cellule et par strate, pour que le taux d'information insuffisante se lise avec sa part due à ce cas.
(5) **Recette.** Cellule T-imp, grille « large », repli, W = 1, i = 1, P99 : n′ de stress = 0 pour n_s = 2 736. Une strate à 0 < n′ < n_s/2 (même cellule, i = 65 : n′ = 650) passe par la règle comme toute autre. Tests : `scripts/sim-bis/tests/test_nprime.py`.
