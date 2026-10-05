# Lettre de l'ajout daté au G0 de SIM-BIS (lot PLAN-S2BIS-2), consolidée

- **Statut** : pièce finale, sans code. Texte à inscrire tel quel par l'orchestrateur à la fin de
  `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, après adjudication ; l'en-tête garde `<date>`, que l'orchestrateur remplace par l'heure.
- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (fiche `shogen-worker`).
- **Date** (`date -u`) : rédaction le 2026-10-05 à partir de 14:21 UTC.
- **Sources** : proposition `scratchpad/s2bis/plan2/PROPOSITION-PLAN2.md` (sha256 `4b3107a7…1749`, version remise et lue par
  l'avis ; « PP l.n ») ; avis de l'advisor `scratchpad/s2bis/plan2/AVIS-PLAN2.md` (sha256 `33ac8d31…92a4`, adopté tel qu'écrit
  par l'orchestrateur, y compris ses trois modifications ; « AV l.n ») ; relecture G2 de la tranche 4
  `scratchpad/s2bis/sim4/g2/G2-SIM-T4-transcrit.md` (sha256 `4663486e…86d6` ; « G2-T4 l.n ») ; G0 de SIM-BIS (`d9cffc0a…` ;
  « G0-SIM l.n »), son avis (`aaf70a4f…` ; « AVIS-G0 l.n ») et sa proposition (`0e78afab…` ; « PROP l.n ») ; ADR-0029
  (`b908842d…` ; « l.n »).
- **Écart au §3.2 de la proposition** (PP l.234-261) : retouches des points (1), (2), (4), (5) et (7) (AV l.120-124) ; ajout au
  point (6) (AV l.106) ; point (3) précisé (AV l.103, l.46) ; point (8) recopié mot pour mot du critère de bord (AV l.117) ;
  point (9), le filet. L'option (c) d'encadrement de la mise à jour non retenue disparaît.

## Lettre

> *Ajout daté du <date> (lot PLAN-S2BIS-2 : G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md`, proposition, avis de l'advisor,
> périmètre réduit et cp-1 de cet ajout dans le même dossier ; option B de l'avis de la tranche 4 ; motif : constat du point 9
> du rapport de la tranche 4, vu à la mesure de mise au point E-4 du 2026-10-05 et recompté par la relecture G2 de la tranche 4
> (`docs/adr-0029/g0-sim/revue-t4/`), et §3.2 de l'avis de la tranche 4)* :
> (1) **C1** : dans chaque strate, point p de la grille d'E1 qui minimise Q₁(p) = Σ_u Σ_ℓ (ln F̄_u,p(ℓ) − ln F_u(ℓ))², somme
> sur les hôtes u du pool d'E1 (D1-bis) dont F_u(ℓ) est défini, sans garde sur leur nombre de cellules d'écart, et sur les ℓ de
> la grille de calibration où la garde de `fiv_unites.txt` est tenue. Même type de série des deux côtés : série d'écart
> (`r1.ECARTS`) côté S2 ; D*(u) = H(u) ∪ F(u, BTC) côté modèle, sans hors-enveloppe (Q-T4-13). F_u(ℓ) = FIV_série de
> `fiv_unites.txt`, chaîne de r1 prise en rationnel exact depuis son écriture décimale, comme EP (E-S-37). F̄_u,p(ℓ) = moyenne
> exacte, sur les réplications définies parmi les 200 du point p (celles de C2), du FIV exact de la série D*(u) sur le masque
> mesuré. Logarithmes par `Decimal.ln` sous le contexte de r1 ; égalités au plus petit κ, puis τ_D, puis φ ; un point dont un
> F̄_u,p(ℓ) retenu est indéfini est écarté. La convention « milieu des logs de C0 et de C2 à ℓ = 240 » est retirée.
> (2) **C2** : critère sur ln FIV_série de I_t contre la courbe D1-bis d'EP (EP l.128-161), inchangé. **C0** : inchangé (aucun
> régime).
> (3) **Calendrier d'E1** : positions présentes = masque des fenêtres évaluables de J28 versé par PLAN-S2BIS-2
> (`masque_j28.txt`), empreinte contrôlée, au lieu des positions de la portée hors D5, pour C0, C1 et C2. Le masque s'applique
> après génération (à vérifier par la G2 du diff d'intégration) ; il ne touche qu'E1 : E2 et E3 gardent le calendrier de S2-bis.
> (4) **Nature** : C1 : groupement propre mesuré par hôte, déclaré borne haute du groupement propre, par hypothèse : les
> absences de l'observateur unique ajoutent de la dépendance sérielle aux séries d'écart (ADR l.38 ; §5 de l'avis du G0 de
> PLAN-S2BIS-2) ; la troncature par le masque joue en sens inverse aux grands ℓ ; la sensibilité au voisinage des lacunes
> (PLAN-S2BIS-2, Q-P2-10) en chiffre la part. Ce sens n'est pas démontré pour la durée, d'où les trois W* de (5) ; au bord de la
> grille, (8) s'applique. C2 : point de la grille le plus proche de la courbe de I_t ; garde-fou imprimé, plus « cas le plus
> défavorable plausible » depuis le constat de la tranche 4
> (relecture G2 de la tranche 4, `revue-t4/`, constat du point 9, pt 4).
> (5) **Durée** : la règle du §3 de la proposition de SIM-BIS se lit au niveau C1 pour l'acte A-2 : W retenue = max(16,
> W*(C1)). Le fond de référence de la cible (§3 pt 1 de la proposition de SIM-BIS ; ADR l.399 pt 2, « groupement au niveau C2 »)
> passe au niveau C1 : la confirmation à 10⁴ réplications à la durée retenue et le bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` (§3
> pts 3 et 6) s'y calculent ; l'échelle des durées tourne toujours aux trois niveaux (AVIS-G0 Q-S-03, modification 1) et P-cible
> à C2 (N3) reste imprimée. A-2 est posé si, et seulement si, W*(C1) > 16 ou W*(C0) > 16, ou si aucune durée de l'échelle ne
> tient (a) à (c) à l'un de ces deux niveaux (§3 pt 4 de la proposition de SIM-BIS) ; jamais sur W*(C2) seul. Si
> W*(C0) > 16 ≥ W*(C1), A-2 est posé sans détour, comme le prévoyait l'avis du G0 (Q-S-03), W retenue reste 16 et la question
> dit que le seul niveau mesuré, C1, n'exige pas l'allongement. Si A-2 n'est pas posé, et en particulier si W*(C1) ≤ 16 < W*(C2)
> avec W*(C0) ≤ 16, aucune question n'est posée : la durée écrite au paquet reste 16 semaines, la puissance à la cible y est
> imprimée aux trois niveaux et une phrase de limite nomme C2. La question A-2, si elle est posée, porte W*(C0), W*(C1), W*(C2),
> la phrase de (4), le 20 % sous H0 (adjudication 5) et, le cas échéant, la phrase de (8). Ce point remplace « la durée déclarée
> est celle de C2 » (adjudication 2) ; l'ajout daté du même jour à l'ADR-0029 porte le même changement à l'ajout daté du
> 2026-10-04 23:02:56 UTC (l.399, pts 2 et 5). Dans (8)(iii), « sans question » s'entend au titre de (8) seul ; si A-2 est posé
> par la règle ci-dessus, il porte la phrase de (8).
> (6) **Contrôles et impressions** : SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 sur C1 dès son épinglage. SB-11 imprime, par strate et
> par hôte, les résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) aux ℓ retenus, le point qui minimiserait Q₁ pour cet hôte seul (diagnostic,
> jamais candidat), le nombre de réplications à FIV indéfini, et la loi des pauses du modèle à C1 sur le masque, à côté de
> `intervalles.txt` ; et, par point et par ℓ, l'écart-type exact (racine par `Decimal.sqrt` sous le contexte de r1, à
> l'impression seulement) des FIV définis parmi les 200 réplications, pour la série de I_t.
> (7) **Ordre** : cet ajout est inscrit au G0 de SIM-BIS avant l'exécution de PLAN-S2BIS-2 et avant l'inscription au JOURNAL du
> sha256 du code de PLAN-S2BIS-2 ; cette antériorité est consignée par deux heures `date -u`. Un cp-1 bref de cet ajout, par un
> validateur frais, passe avant cette inscription (Q-P2-13 ; rapport `docs/adr-0029/g0-plan2/CP1-AJOUT.md`). `e1.ell_c1` est
> retiré de `parametres.json` de SIM-BIS (sans objet). E0 attend le versement de PLAN-S2BIS-2 et le diff de SIM-BIS qui lit ses
> sorties ; aucune exécution provisoire avec la C1 de la lettre d'E-S-38. RB-7 attend aussi : l'exécution provisoire du § Suite
> de ce G0 (« pour clore la conception et débloquer RB-7 ») se fait avec la C1 de cet ajout, donc après E0. Le texte d'E-S-38
> reste tel quel.
> **(8) Bord de la grille.** Dans une strate, C1 est « au bord » si l'une de ses trois coordonnées est la valeur extrême de sa grille (φ = 0,1, κ = 50 ou τ_D = 4 320 ; E-S-38) **ou** si, aux ℓ retenus ≥ 60, le résidu ln F̄_u,C1(ℓ) − ln F_u(ℓ) est négatif pour au moins six des dix hôtes du format. Alors : (i) C1 reste le point retenu (aucun point hors grille, aucune seconde sélection) ; (ii) la limite de SHOGEN-SIM-BIS-FIV-IDENTIF-1 s'écrit « dans la strate s, la famille E1 n'atteint pas les FIV_u mesurés ; C1 y est une borne basse de la mesure, et « borne haute » ne s'applique pas » ; (iii) les trois W* sont imprimés et, si W*(C1) ≤ 16 et que C1-calme est au bord, le paquet dit que les 16 semaines reposent sur un niveau que la famille ne peut pas dépasser : information à l'investisseur à l'accord A-1 de S-2, sans question ; si W*(C1) > 16, A-2 porte la même phrase. (iv) Le bord est constaté par le script, par une ligne nommée, jamais par une lecture humaine.
> Précision d'adjudication à (8) : la seconde condition se lit « pour au moins six des dix hôtes du format, le résidu ln
> F̄_u,C1(ℓ) − ln F_u(ℓ) est négatif à chacun des ℓ retenus ≥ 60 » ; la ligne nommée de (8)(iv) imprime, par strate, le nombre
> d'hôtes qui satisfont cette condition et la liste des ℓ retenus ≥ 60.
> (9) **Filet** : le déclencheur « W* différente entre C0 et C2 » de SHOGEN-SIM-BIS-FIV-IDENTIF-1 est retiré ; PLAN-S2BIS-2
> précède E0 dans tous les cas, que W*(C0) et W*(C2) diffèrent ou non. Le cas où C1 n'atteint pas les FIV_u mesurés relève de
> (8), jamais d'un déclencheur nouveau ; l'item reste ouvert jusqu'à la sortie d'E1 épinglée, où sa limite s'écrit selon (4)
> et (8).

## Tableau des sources

| pt | contenu | avis (AV) | proposition (PP) | G2-T4 | autres pièces |
|---|---|---|---|---|---|
| en-tête | `<date>` laissé ; motif | l.16 ; §3.3 l.115-124 | l.239-241 | l.27, l.172-183 | T4 l.111, l.114 ; RW-T4 point 9 |
| (1) | C1 = argmin Q₁ ; même type de série des deux côtés ; F_u = chaîne de r1 en rationnel exact ; pas de garde sur K ; milieu des logs retiré | §3.1 l.101 ; §3.3 l.120 ; Q-P2-02 l.34 ; Q-P2-05 l.49-53 ; §4.1 l.131 | l.242-247 ; Q-P2-05 | — | PROP l.196-197 (E-S-37, E-S-38) ; T4 l.47-63 (Q-T4-6, 7, 9) ; Q-T4-13 (T4 l.77-80) |
| (2) | C2 contre la courbe D1-bis d'EP | §3.1 l.102 ; §3.3 l.121 ; §9 obs. 1 l.194 | l.248 | — | EP l.128 (D1-bis) et l.94-127 (S2) |
| (3) | masque mesuré pour C0, C1, C2 ; après génération, à vérifier ; E1 seule | §3.1 l.103 ; Q-P2-04 l.42-46 | l.249-250 ; Q-P2-04 | l.71-75 (calendrier recompté) | T4 l.45 (Q-T4-5) ; ADR l.31 |
| (4) | C1 borne haute par hypothèse ; durée non démontrée ; bord : (8) ; C2 garde-fou imprimé | §3.1 l.104 ; §3.3 l.122 ; §5 l.165-166 | l.251-252 | l.189 (pt 4) | ADR l.38 ; PROP l.329-330 ; T4 l.120 |
| (5) | W retenue = max(16, W*(C1)) ; A-2 jamais sur C2 seul ; C0 > 16 : sans détour ; contenu de A-2 ; ajout daté à l'ADR | §3.1 l.105 ; §3.3 l.123 ; Q-P2-06 l.55-61 ; §1 l.16 | l.253-255 ; Q-P2-06 l.470-477 | l.149, l.176-183, l.189 | G0-SIM l.13-15, l.20-22 ; AVIS-G0 l.22-23 ; ADR l.399 pts 2 et 5 |
| (6) | impressions ; écart-type des 200 FIV ; réplications à FIV indéfini | §3.1 l.106 ; Q-P2-05 l.52 | l.256-258 | — | T4 l.50 ; B.64 l.1067, l.1069 |
| (7) | antériorité sur le sha256 du code au JOURNAL, deux heures ; cp-1 bref ; `e1.ell_c1` retiré ; E0 attend ; pas de provisoire | §3.1 l.107 ; §3.3 l.124 ; Q-P2-07 l.63-66 ; Q-P2-13 l.91-93 ; §6 l.178 | l.259-261 ; Q-P2-07, Q-P2-13 | — | T4 l.116, l.148 ; SB-10C l.113-136 (`ell_c1`) |
| (8) | critère de bord, mot pour mot | §3.3 l.117 ; §3.2 l.111-113 ; §8 risque 2 l.189 | — | l.189 (le point 4, déplacé à C1) | B.64 l.1067 ; T4 l.101 |
| (9) | filet : déclencheur retiré, PLAN-S2BIS-2 avant E0 dans tous les cas | §3.2 l.111 ; §6 l.178 ; Q-P2-06 l.57 | l.562 (déclencheur de FIV-IDENTIF-1) ; ancien point (8) de la mise à jour non retenue | l.187, l.189 | B.61 l.1022 ; G0-SIM l.13-15 |

## Contrôles de cohérence de la lettre

1. **(9) et l'avis** : l'avis ferme le cas pour C2 en faisant porter la durée par C1 (AV l.111), et pour C1 par le critère de
   bord (AV l.112-113) ; il refuse tout élargissement de grille (AV l.113) et fixe l'ordre « ajout daté, cp-1 bref, épinglage du
   lot, lancement, versement, diff d'intégration, E0, E1 » (AV l.178). Retirer le déclencheur et faire passer PLAN-S2BIS-2
   avant E0 dans tous les cas en est la conséquence ; (9) ne crée aucun déclencheur et renvoie le cas du bord à (8).
2. **(5) et (8)** : la dernière phrase de (5) (C-1) lit « sans question » de (8)(iii) au titre de (8) seul ; quand A-2 est posé
   par (5), y compris si W*(C0) > 16 ≥ W*(C1), il porte la phrase de (8).
3. **(4) et (8)** : au bord, « borne haute » ne s'applique pas (8)(ii) ; (4) y renvoie.
4. **(1) et (7)** : C1 ne lit plus `ell_c1` ; son retrait de `parametres.json` est sans effet sur C2.
5. **Cas tranché** : W*(C0) > 16 ≥ W*(C1) relève de C-1, adjugée par l'orchestrateur (cp-1 §4 et §6) : A-2 est posé sans détour,
   W retenue reste 16, et la question dit que le seul niveau mesuré, C1, n'exige pas l'allongement ; elle montre les trois W*.

## Version 2 : corrections du cp-1 (correction → lignes changées)

- **v2** : écrite le 2026-10-05 à 15:04:18 UTC (`date -u`), par programme (`brouillons/lettre_v2.py`), depuis la v1 (sha256
  `01ce4551…fcd00`, gardée dans `brouillons/LETTRE-AJOUT-G0-SIM-v1.md`). Corrections C-1 à C-6 du cp-1 bref `CP1-AJOUT.md`
  (sha256 `7f497ab2…02cc`, §6), lettres exactes recopiées par programme, adjugées par l'orchestrateur avec ses choix (C-1 :
  lettre du cp-1 ; C-2 : lecture « à chacun des ℓ retenus ≥ 60 » et ligne nommée du compte ; C-5 : chemins de versement) ;
  observations O-7 et O-4 du cp-1 (§7) portées au point (7), à sa demande.
- **C-4** : « et pour chaque série D*(u) » est retiré, comme la lettre de C-4 le prévoit : T4 l.50 (`AVIS-SIM-T4.md`, sha256
  `6dfc13e7…`) ne vise que la série de I_t (« C2 est-il distinguable de ses voisins »).

| correction | point | changement | lignes v1 | lignes v2 |
|---|---|---|---|---|
| C-5 (a), (b), (c) | en-tête de la lettre | G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md` ; proposition, avis, périmètre réduit et cp-1 dans ce dossier ; relecture G2 de la tranche 4 à `docs/adr-0029/g0-sim/revue-t4/` | 19-21 | 19-22 |
| C-6 | (2) | « (EP l.128-161) » | 30 | 31 |
| C-5 (c) | (4) | « `revue-t4/` » ; ligne coupée en deux | 40 | 41-42 |
| C-3 ; C-1 | (5) | fond de référence au niveau C1 (C-3) ; règle de A-2 fermée, cas W*(C0) > 16 ≥ W*(C1) écrit, lecture de (8)(iii) (C-1) | 42-47 | 44-56 |
| C-4 | (6) | écart-type exact des FIV définis, série de I_t | 51 | 60-61 |
| O-7 ; O-4 (observation (7)) | (7) | `CP1-AJOUT.md` nommé ; RB-7 attend | 54-56 | 64-68 |
| C-2 | après (8) | précision d'adjudication et ligne nommée du compte ; (8) inchangé | aucune (insertion après 57) | 70-72 |
| C-1, hors lettre | contrôles 2 et 5 | relus après C-1 ; cas tranché | 84-85 ; 88-91 | 99-100 ; 103-104 |
| aucune | cette section | version, tableau, vérification | aucune | 105-132 |

- **Vérification** [mesuré, par le programme] : les 70 autres lignes de la v1 (sur 91) se retrouvent à l'identique,
  dans le même ordre, dans la v2 ; `difflib` ne rend aucun bloc hors du tableau ; (8) reste identique à AV l.117 ; aucun octet
  92, aucune tabulation ; aucune ligne de la lettre ne commence par « > > » ; lignes nouvelles de la lettre et des contrôles de
  128 caractères au plus ; `diff -U0` de la v1 à la v2 : neuf blocs, ceux du tableau (le dernier joint les contrôles et cette
  section).
