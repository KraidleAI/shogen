# Relecture G2 neuve de SB-11 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:33:41 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur (deux reprises), du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 de la série SIM-BIS SB-11a … SB-11u (executer.py, e1.py, câblage d'E1)

**Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact de l'environnement de ce réviseur). Rôle : réviseur G2
neuf. Je n'ai écrit aucun des 21 diffs relus.

**Verdict : ACCEPTE-AVEC-CORRECTIONS.** La liste des corrections est fermée : C-1 à C-9, au §5. Le code de la série tient
le brief et le G0 dans chacun des cas que j'ai contrôlés. Une seule correction touche le code : C-1, la formule de
`executer.plan`, qui dépasse la borne de 90 min. Les huit autres sont des tests de site d'appel qui manquent : 12 de
mes 21 mutants ont survécu à la suite. Pour chaque correction, le test qui la prouve est écrit et exécuté : il est rouge
sous le mutant qu'il vise et vert sur la série. Seul P-1 est rouge sur la série, parce qu'il montre le défaut.

Dossier : `<scratchpad>/s2bis/sb11/g2/`. `NOTES.md` permet la reprise. La sonde a été écrite avant la lecture du code
(`sonde/SONDE.md`). Les outils sont dans `outils/`, les tests de preuve dans `preuves/`, les mutants dans `mut/` et les
contrôles dans `journal/`. Le tout est couvert par `SHA256SUMS`.

## 1. Base, copies, horloge

- **Horloge** : début à 05:21:06 UTC et rapport à 06:34:15 UTC, le 2026-10-09. Chaque heure a été lue par `date -u`.
- **Base** : `5e386c4`. Copie `g2/copie` faite par `git --no-optional-locks archive`, avec les exclusions du brief.
  - Les 21 diffs s'appliquent en série avec `-p1`, sans aucun rejet.
  - `scripts/sim-bis` et `gates.yml` sont égaux à `etapes/e11u` du générateur (`diff -rq` vide).
  - Chaque étape reconstruite (base + a…X) est égale à `etapes/e11X` pour X = a…u.
- **Tête** :
  - relue à 05:38:30 : `d10f6c2`. Copie neuve `g2/tete`, puis `g2/tete-serie` = tête + série (§9) ;
  - relue à 06:34:15 : `1a388e1`. Seul changement sur les chemins de la série : le plancher s2bis de `gates.yml`
    (289 → 340). Rejeu à sec sur `1a388e1` : mêmes rejets, rien d'autre.
- **Dépôt réel** : lecture seule (`--no-optional-locks`), aucune écriture git.
  - Les index git servent `oracle_r1` et les gates à index. Ils vivent seulement dans mes copies `g2/` (`git init`,
    alternates vers les objets du dépôt, `git add`).
  - Le dépôt réel porte des changements indexés d'un autre agent (s2bis). Je ne les ai pas touchés.
- **Interdits tenus** :
  - `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (retirée des environnements, `isole.sh`) ;
  - aucun `*.jsonl`, aucune pièce de D.2, aucun dossier interdit ouvert ;
  - aucune recherche récursive sur `docs/`, ni sur le dépôt, ni sur le scratchpad entier ;
  - aucun réseau : tout a tourné sous `unshare -n`.

## 2. Sonde du réviseur, écrite avant le code, et son résultat

La sonde a été écrite entre 05:21:06 et 05:29:38 UTC, avant la lecture des diffs et du rapport du générateur. Résultats :

| item de la sonde | résultat (preuve) |
|---|---|
| A1, A2, A6 : comptes en entiers et en `Fraction`, SE en `Decimal` sous le contexte de r1 | tenu (`executer.py:45-58`). SE de 121/10⁴ égale au calcul de `bc` à 50 chiffres. SE et borne inchangées sous un contexte ambiant modifié (précision 5, ROUND_DOWN) : script, `NOTES.md` |
| A3 : borne 1 − 0,05^(1/R) | tenu, par `Decimal.ln` et `Decimal.exp` sous le contexte. Valeurs de 10⁴ et de 2 000 recalculées par `bc` (scale 80) : égales aux attendus des tests |
| A4 : aucune fonction de libm | tenu. La garde `ast` couvre `executer.py` et `e1.py`, parce que `test_fitness` énumère les modules du dossier |
| B1, B2 : un fichier par lot ; chaque i une fois | tenu sur les noms et les plages. Le contrôle des i **dans** les enregistrements n'est pas testé : G-03 vit, d'où **C-3** |
| B3 : lot perdu refait à l'octet | tenu (`test_lot_octets`, `test_lots_par_point_et_reprise`) |
| B4, B5 : écriture atomique, refus nommé sans lien dur, fsync du dossier | tenu (`commun.py:202-231`, `test_ecrire_sans_lien_dur`). Un `.partiel` resté après un arrêt n'est vu qu'au moment de l'écriture : O-7 |
| B6 : lots de 90 min au plus | **non tenu**. La plage vaut `borne·processus // ns`, si bien qu'un lot dure ⌈(b − a)/processus⌉·ns, au-delà de la borne quand le compte n'est pas un multiple du nombre de processus. Exemple au coût mesuré de N1 : 41 s × 4 processus, lot (0, 526), 132 tours, 5 412 s > 5 400 s. `test_budget` entérine ce dépassement : 5 réplications de 12 ns sur 2 processus, borne 30 ns, durée réelle 36 ns. D'où **C-1** |
| C-a, C-e : I_t et D*(u) d'un même appel `replication` | tenu (`e1.py:36-44`, `test_courbes_d_un_seul_appel`, compte d'appels égal à 1) |
| C-b : `charger_unites`, jamais `analyser_unites` | tenu (`e1.py:121`). M-11K-01 est tué par le masque retouché (CALIB/croisement) |
| C-c : `ligne_bord` par strate, phrases (8)(ii) et (iii) | tenu (`e1.py:77-81`, `:127`). Le texte de (ii) est mot pour mot celui du G0 ; (iii) garde sa condition (Q-SB11-11) |
| C-d : réplications à FIV indéfini par hôte | tenu (`_par_hote`, par point de la grille) |
| C-f, C-g, C-k : C0, C1, C2 par strate ; masque ; 200 réplications | tenu par `calib_fiv` (SB-10, SB-15) et câblé (`calibrer`, `calculer_e1`) |
| C-h : impressions du point (6) | tenu : résidus, point de Q₁ par hôte, indéfinies, pauses à C1, écart-type. Les définitions d'EP sont vérifiées contre `episodes.episodes` et `regles.quantile` (rang ⌈q·N/100⌉ ; censure sur une position voisine absente) |
| C-i : REGIME-FAISABILITE-1 | tenu (`e1.py:84-95`, `:129-136`). La formule de l'attendu, écrite à la main dans le test, vérifiée par algèbre : r′ < 1 ⇔ p_A < φ + (1 − φ)/κ |
| C-j : sorties et première ligne (E-S-05, E-S-48) | tenu. Le texte commence par l'étiquette ; dans le JSON, l'étiquette est le premier élément de `entete`, qui est la première clé triée |
| D : [BORD E1] | la règle est celle de `calib_fiv.bord` (SB-15, hors série) ; le câblage est tenu (`test_bord_et_phrases_q_si_8_c`) |
| E1 à E4 : T-DET-1 | tenu à échelle réduite : 3 cellules × 6 réplications, W = 1, R = 99 ; 1 processus contre 4 ; PYTHONHASHSEED 0 contre 1 ; retrait « presque mort » de bitfinex exigé (P-9) ; M-DET-1 et M-DET-2 tués. Aucune réplication n'y passe par le chemin i ≥ 200 : O-5 |
| F1, F2 : schéma fermé, surcharges | tenu dans le code. Trois refus du schéma ne sont pas testés : G-07, G-08 et G-19 vivent, d'où **C-5** |
| F3 : W de la cellule passé à la couche (L-2) | tenu dans la fonction (`couche`). Le site d'appel dans `cellule` n'est pas testé : G-06 vit, d'où **C-4** |
| F5 : « g sur la grille » (P-3) | M-11G-03 tué (journal du générateur [2nd]) |
| F6 : NON ÉVALUABLE par strate et par cause (E-S-52) | tenu. Une combinaison mixte (n_prime avec une cause d'information insuffisante) n'est pas testée : G-01 vit, d'où **C-2** |
| F8 : R par cellule (Q-S-06, complément 1) | tenu dans le code (`rg["R"]`). Jamais testé avec un R de cellule différent de celui de `parametres` : G-11 vit, d'où **C-8** |

## 3. Pièces du générateur et forme

- **`SHA256SUMS` du générateur** : `sha256sum -c` donne 1 199 OK et 0 échec. Le fichier lui-même a pour sha256 `ff92f2e8…`.
  `RAPPORT-GENERATEUR.md` (sha256 `37a0cea7…`) a été lu en entier, comme une donnée.
- **Diffs** : sha256 égaux à ceux du rapport, 0 octet 92 chacun, aucune ligne `.py` de plus de 120 caractères. Mon
  recompte des lignes ajoutées (hors `.md`) :

| diff | lignes | plancher | diff | lignes | plancher | diff | lignes | plancher |
|---|---|---|---|---|---|---|---|---|
| a `22a3565b…` | 179 | 200 | h `b368dca6…` | 109 | 219 | o `0e037c40…` | 144 | 233 |
| b `480a2055…` | 163 | 204 | i `59813014…` | 134 | 221 | p `4770d1c8…` | 177 | 235 |
| c `0c770aeb…` | 67 | 206 | j `996aa088…` | 145 | 223 | q `941d7e8f…` | 139 | 237 |
| d `d15e4f31…` | 114 | 208 | k `7e390933…` | 167 | 226 | r `adf57dfd…` | 193 | 241 |
| e `dddb3d3f…` | 195 | 211 | l `cc57ea66…` | 68 | 228 | s `f2c647b8…` | 130 | 243 |
| f `482acc23…` | 186 | 215 | m `ddfd4263…` | 58 | 229 | t `7c2bdbc5…` | 66 | 245 |
| g `2e1b361e…` | 104 | 217 | n `b8baf771…` | 188 | 231 | u `f179c55c…` | 67 | 246 |

- **Lignes ajoutées** : total 2 793, maximum 195. R-25 est tenu.
- **Planchers** : à chaque étape, le compte de `TestLoader.discover`, sans aucune erreur de chargement, est égal au
  plancher du diff (194 à la base, puis 200 … 246). Le plancher est donc exact à chaque pas.
- **Suite verte à chaque pas** : les témoins du générateur sur chaque instantané sont conformes à leur plancher [2nd].
  Ces instantanés sont égaux aux étapes reconstruites par moi.
- **R-13** : motif du job écrit par `chr(92)`, témoin positif détecté. Aucun marqueur dans `scripts/sim-bis` de la
  tête + série.
- **Octets 92** : 0 dans toute la série et dans toute la copie finale de `scripts/sim-bis`.
- **Modifications de fichiers existants** : aucun desserrement. L'espion de `test_commun` devient plus strict (deux
  fsync ordonnés au lieu d'un) ; `test_sources` reçoit le composant « debut ».

## 4. Exigences du brief et lignes de LIGNES-BRIEF-SB11 (contrôle du réviseur)

| exigence | état | preuve |
|---|---|---|
| Périmètre 1 : cellules | tenu ; schéma fermé testé en partie | `executer.py:193-329` ; C-4 et C-5 |
| Périmètre 2 : réplications, processus | tenu | `appliquer` (`:168-180`, spawn, starmap ordonné) ; T-DET-1 |
| Périmètre 3 : lots | tenu, sauf la borne | `:108-165` ; C-1, C-3 ; O-6, O-7 |
| Périmètre 4 : agrégation exacte | tenu sur ce qui est agrégé | `:416-443` ; agrégats manquants pour SB-12 : O-4 |
| Périmètre 5 : E1 câblé | tenu | `e1.py` en entier ; C-9 |
| Périmètre 6 : toute cellule par la même mécanique | tenu pour l'expression et la validation | test_table. Chaque cellule du §5.1 a tourné une fois dans la sonde de budget du générateur [2nd : `journal/budget.txt`, 18 lignes] |
| Périmètre 7 : budget | mesuré, majorant | §10 |
| L-2 | fonction tenue, site d'appel non testé | **C-4** (G-06) |
| O-5 | tenu | `cellules.couches`, test_couches_o_5 |
| P-3 | tenu | M-11G-03 |
| P-9 | tenu | test_t_det_1 (`["bitfinex", "presque mort"]`) |
| SB11-IMPRESSIONS-1, point (6) | tenu | §2, C-h |
| Q-SI-8 (a) à (e) | tenu | §2, C-a à C-e ; même point de C1 dans les deux strates non testé : **C-9** (G-16) |
| Mutant « analyser_unites » | tué | M-11K-01 [2nd], mécanisme relu |
| Q-SI-7 | phrase proposée (Q-SB11-15) | acte de l'orchestrateur |
| C1-COUT-1, TABLES-CACHE-1 | mesurés ; cache par processus, par contenu (`sources.py:33-40`, `lru_cache` sur la table) | §10 |
| ECRITURE-LIEN-1 | tenu | SB-11a |

E-S réalisées : la liste du générateur (§5 de son rapport) est juste au regard du §2 de la PROPOSITION. Trois réserves :
- E-S-23 (distribution des dates d'atteinte), E-S-24 (retraits comptés), E-S-32 (taux de C_S ≤ 99) et E-S-34
  (puissance par g) sont enregistrés par réplication mais **pas agrégés** (O-4) ;
- E-S-46 n'est mesuré qu'en majorant ;
- E-S-48 ne vaut que pour E1.

## 5. Corrections exigées (liste fermée)

Chaque correction a son test de preuve dans `preuves/test_preuves_g2.py`. Les sorties sont dans `journal/preuves.txt`,
dont le troisième passage est seul compté. Chaque test est rouge d'assertion sous le mutant visé et vert sur la série,
sauf P-1.

- **C-1, code, mineure (adjudication 6)** : dans `executer.plan`, remplacer `t = borne * processus // ns` par
  `t = borne // ns * processus`. Ainsi chaque lot dure ⌈(b − a)/processus⌉·ns ≤ borne.
  - Mettre à jour `test_budget` : durées dans l'ordre (12, 5), coût retenu 12, lots de 4 sous la borne de 30 ns. Les
    attendus sont recalculés à la main.
  - Mettre à jour `test_plan_90_min` en ajoutant un cas non multiple : 41 s × 4 processus donne des lots de 524, soit
    131 tours et 5 371 s.
  - Preuve : P-1. Il est rouge sur la série (5 412 s > 5 400 s) et vert sous le remède, que j'ai fait tourner comme le
    mutant G-05. Mutants qui le prouveront : l'ancienne formule, et G-22 (« dernière durée au lieu du maximum »), déjà
    rouge sous P-1.
- **C-2, test** : ajouter à `test_frequences_e_s_52` une NON ÉVALUABLE de causes [unites, k_crit, runs, n_prime]. Elle
  compte en information insuffisante. Ce cas se produit dans la règle : `regle.tester` à n′_s = 1 le rend.
  Preuve P-2 ; mutant G-01 (`any` → `all`).
- **C-3, test** : un lot dont les i sont permutés, l'empreinte étant recalculée, doit donner LOT/forme
  (`test_lot_forme`). C'est le mécanisme de contenu d'E-S-45. Preuve P-3 ; mutant G-03 (contrôle des i retiré).
- **C-4, test, L-2 au site d'appel** : `executer.cellule(..., grille dégradée, W)["couche"]["perte"] == W`, pour W = 16
  et W = 2. Preuve P-4 ; mutant G-06 (`couche(p, ep, cel, (W + 1) // 2)` dans `cellule`).
- **C-5, test, schéma fermé** : CELLULE/schema pour trois cas, chacun sous un `prm` où la cellule de base passe le
  schéma :
  - un incident « parmi » dont les imposés sont « faibles » sans unité faible ;
  - des classes sans BTC en tête (`["ETH"]`) ou hors de l'ordre (`["ETH", "BTC"]`) ;
  - f nul.

  Preuve P-5 ; mutants G-07, G-08, G-19.
- **C-6, test, n′_s au site d'appel (E-S-24, E-S-35)** : dans le cas n′_s < n_s (fixture de `test_chaine_a_la_main` :
  n_s de calme 12 000, couche dégradée au repli, critère collectif actif), `regle.retraits` et `regle.filtrer` reçoivent
  les n retenus. Preuve P-6 (espions `wraps`) ; mutants G-09 (n_s aux retraits) et G-12 (n_s au critère).
- **C-7, test, source des données** : une surcharge `{"longues": [60], "poids_longues": [1]}` atteint
  `sources.Replication` lors d'une réplication. Preuve P-7 ; mutant G-10 (`Replication(prm, …)` au lieu du prm de la
  cellule).
- **C-8, test, R de la cellule (Q-S-06, complément 1)** : une cellule à R = 999 sous un `parametres` à R = 99 transmet
  999 à `regle.oracle`, à `variante.deux_modes` et à `regle.loi_evenements`. Preuve P-8 ; mutant G-11 (`p["regle"]["R"]`
  au lieu de `rg["R"]`).
- **C-9, test** : quand C1 est le même point en calme et en stress, `pauses_c1` rend les deux strates, chacune égale
  à l'appel où le point n'est C1 que de cette strate. Preuve P-9 ; mutant G-16 (première strate seule).

Ces corrections font environ 90 à 120 lignes, et tiennent en un diff SB-11v. Leurs attendus sont écrits à la main. Il
faut ensuite recaler le plancher exactement et mener une campagne de 10 mutants au moins, dont G-01, G-03, G-06 à G-12,
G-16, G-19, G-22 et l'ancienne formule de `plan`.

## 6. Mutants du réviseur

Commande : celle du job `sim-bis-unittest`, sur la base + série, avec `--plancher 246`. Chaque arbre de mutant est fait
de liens vers la copie, avec `scripts/sim-bis` copié et muté. Les runs tournent sous `isole.sh` et `timeout 300`.

Classement : sortie 1, tué ; sortie 0, vivant ; toute autre sortie, FATAL.

La campagne a tourné de 05:37:10 à 06:16:17 UTC, en PAR=2. La chaîne avait le PID 22105 ; `/proc/PID/cmdline` a été lu.
Témoins : 133 s au début, 130 s à la fin, VIVANT (sortie 0). Le mutant le plus long a pris 209 s.

**Bilan** : 21 mutants, 5 tués, 16 vivants, 0 FATAL, 0 inapplicable. Tous les tués le sont par un AssertionError.

| id | diff | mutation | issue | classement |
|---|---|---|---|---|
| G-01 | a | `any` → `all` (information insuffisante) | VIVANT | lacune de test → C-2 |
| G-03 | b | contrôle des i des enregistrements retiré (`_lot`) | VIVANT | lacune de test → C-3 |
| G-04 | o | site d'appel : `plan(R, ns, 1, borne)` dans `calculer_e1` | VIVANT | équivalent pour les sorties : seuls la taille et le nombre des lots changent, toujours sous la borne |
| G-05 | c | `borne // ns * processus` (remède de C-1) | TUÉ (test_budget) | montre que le test entérine le dépassement |
| G-06 | d | site d'appel : W → (W + 1) // 2 dans `cellule` → `couche` | VIVANT | lacune (L-2) → C-4 |
| G-07 | e | imposés « faibles » admis sans unité faible | VIVANT | lacune → C-5 |
| G-08 | e | `cl[0] == "BTC"` retiré | VIVANT | lacune → C-5 |
| G-09 | f | site d'appel : `regle.retraits(…, e["n"])` (n_s au lieu de n′_s) | VIVANT | lacune (fixture n′_s = n_s) → C-6 |
| G-10 | f | source des données : `sources.Replication(prm, …)` | VIVANT | lacune (aucune surcharge exercée) → C-7 |
| G-11 | g | `p["regle"]["R"]` au lieu de `rg["R"]` | VIVANT | lacune (R cellule = R prm partout) → C-8 |
| G-12 | g | `regle.filtrer(series, n_s, p)` | VIVANT | lacune → C-6 |
| G-13 | k | `_par_hote` sans le filtre « F_u défini » | VIVANT | équivalent sous les données épinglées : aucun (u, ℓ) de `fiv_unites.txt` n'a sa garde tenue avec F_u indéfini ; sinon le mutant lève TypeError |
| G-14 | m | `bord` si g **et** f | TUÉ | — |
| G-15 | m | `vides += bool(g)` | TUÉ | — |
| G-16 | n | `pauses_c1` : première strate seule pour un point partagé | VIVANT | lacune → C-9 |
| G-17 | r | `_par_duree` sur la première fenêtre seule | TUÉ | — |
| G-18 | s | donnée : ε de N0 = 10⁻³ | TUÉ (test_table) | — |
| G-19 | e | f = 0 admis | VIVANT | lacune → C-5 |
| G-20 | i | site d'appel : `appliquer(…, 1)` dans `calculer_lot` | VIVANT | équivalent : E-S-42 rend la sortie indépendante du nombre de processus |
| G-21 | l | égalité de r′ : dernier maximum au lieu du premier | VIVANT | équivalent sur EP : aucune égalité de r′ ; le docstring dit « premier » |
| G-22 | t | coût retenu = dernière durée au lieu du maximum | VIVANT | lacune (durées données en ordre croissant) → C-1 |

**Couverture exigée** :
- SB-11m : G-14 et G-15, tués. SB-11s : G-18, tué.
- Mutants de site d'appel : G-04, G-06, G-09, G-12, G-20. Mutants de source des données : G-10, G-11, G-18.

**Constat de méthode** : les 12 vivants qui ne sont pas équivalents relèvent tous du même motif. La fixture donne au
paramètre passé « sous étiquette » la valeur de son concurrent : W = 1, n′_s = n_s, R de la cellule = R de `prm`,
surcharges vides, points de C1 distincts. C'est SHOGEN-MUTANTS-SITE-APPEL-1 joint à SHOGEN-SIM-BIS-MUT-EQUIV-FIXTURE-1 :
voir le §12.

## 7. Constats

- **O-1, mineure** : la garantie de 90 min de `plan` est fausse dès que le nombre de réplications d'un lot n'est pas un
  multiple du nombre de processus, et `test_budget` entérine ce dépassement → C-1.
- **O-2, majeure en somme** : 12 mutants du réviseur vivent, tous à un site d'appel ou sous une fixture équivalente.
  Le tableau du générateur reconnaît des diffs sans mutant de site d'appel (c, d, g, i, k, m, r, s) → C-2 à C-9.
- **O-3, moyenne, bloque E0** : à n′_s = 0, `regle.tester` refuse (REGLE/entier). Mesuré : à n = 0, refus ; à n = 1,
  NON ÉVALUABLE [unites, k_crit, runs, n_prime]. Q-SB11-7, item NPRIME-NUL-1.
- **O-4, moyenne, brief de SB-12** : `agreger` ne compte ni le taux de C_S ≤ 99 (E-S-32), ni la puissance par g
  (E-S-34), ni la distribution des dates d'atteinte (E-S-23), ni les retraits (E-S-24). Les enregistrements les portent.
- **O-5, mineure** : T-DET-1 ne passe jamais par le chemin i ≥ 200 (`regle.tester`, `variante.tester`, sans
  impressions). Les 3 × 200 de la PROPOSITION ne le feraient pas non plus.
- **O-6, mineure** : la reprise d'E1 exige les mêmes (ns, processus, borne). Avec un autre plan, on obtient LOT/double,
  un refus nommé et sûr. À consigner au journal d'exécution (E1-LANCEUR-1).
- **O-7, mineure** : un `.partiel` laissé par un lot tué fait échouer la reprise à l'écriture (SORTIE/partiel-present),
  après tout le calcul. Le README prescrit de le retirer à la main. Je suggère un contrôle avant le calcul.
- **O-8, mineure** : `ecrire_e1` écrit le JSON puis le texte. Si le second échoue, le premier reste seul : c'est sûr,
  mais la paire n'est pas atomique.
- **O-9, mineure** : `lignes_pauses` saute en silence une strate absente de `pz` (`if s in pz`).
- **O-10, mineure** : l'ε de N10 suit la formule (1 − f)·p̂, soit 0,9·p̂. Or le §5.1 écrit ε = 0,7·p̂ pour N1, et N10 ne
  change que f. Cette lecture est à joindre à Q-SB11-9.
- **O-11, info** : la grille « large » n'est employée par aucune cellule de `cellules.nulles`. Son usage est à fixer
  avec Q-SB11-3 ou FAMILLES-1.
- **O-12, info** : les rouges d'E-26 ont été montrés après coup, sur des ébauches à fonctions vides : ce sont des rouges
  d'existence. La discrimination est prouvée par M-11F-03, M-11I-04 à 06, M-DET-1 et M-DET-2, tués [2nd, journaux
  relus]. Je l'accepte comme écart déclaré, non comme « test d'abord ».
- **O-13, info** : E-15 et E-21, des passages sans PID consigné, sont acceptés comme écarts déclarés. Ma campagne porte
  sur l'état final.

## 8. Matrice, portes, xtask

Tous les contrôles portent sur la **tête `d10f6c2` + série résolue** (`g2/tete-serie`). Ils ont tourné l'un après
l'autre, par `outils/apres.sh` (PID 25332), de 06:16:45 à 06:32:47 UTC.

| contrôle | résultat |
|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | code 0, 136 ok, 0 échec |
| sim-bis `--plancher 262` | conforme, Ran = 262 (145 s) |
| sim-bis `--plancher 246` (base + série) | conforme, Ran = 246 (129 s, 05:29:48–05:31:57) |
| s2bis `--plancher 289` (plancher de `d10f6c2`) | conforme, Ran = 289 |
| S2 `--egal` | conforme, Ran = 415, deux sauts qui nomment la variable scellée |
| hooks | 54 ok, 0 échec |
| secrets | fixtures : 147 ok ; `--tree` : 971 fichiers, OK |
| R-1 | fixtures : 227 ok ; arbre : OK, liste blanche exacte |
| matrice `-X dev -W error` | 3.10 : code 0, 262 OK (193 s) ; 3.11 : 170 s ; 3.12 : 162 s ; 3.13 : 151 s ; 0 « Exception ignored », 0 « Warning » |
| `cargo --locked xtask verify` (lignes VERDICT seules) | tête + série : 8 VERT, 1 ROUGE (1 violation), global ROUGE ; tête neuve `d10f6c2` : **mêmes dix lignes** (`diff` vide). La violation précède la série ; la série n'en ajoute aucune |

## 9. Application sur la tête

- **Rejets** : série appliquée diff par diff sur `git archive d10f6c2`. Chaque diff a pour seuls rejets la ligne du
  plancher sim-bis de `gates.yml` et, pour 20 diffs sur 21 (pas s), la ligne du README voisine d'`oracle_recalc.py`.
  Tout le reste s'applique, `commun.py` avec un décalage de 6 lignes.
- **Résolution indépendante** :
  - plancher 210 + (246 − 194) = **262** ;
  - les lignes `executer.py` et `e1.py` insérées après celle d'`oracle_recalc.py` ; les deux lignes sont gardées.
- **Comparaison** :
  - `scripts/sim-bis` est identique à `fusion/` du générateur ;
  - `gates.yml` ne diffère de `fusion/` que par le plancher s2bis, passé de 255 à 289 par la tête.
- **Verdict** : la résolution du générateur est **juste**, et le job sim-bis est conforme à 262 sur la tête + série.
- **Sur `1a388e1`** (relue à 06:34) : mêmes rejets. Le plancher s2bis est maintenant à 340 ; ce n'est pas un conflit
  de la série.

## 10. Budget mesuré (avis)

- **Mesure** : une réplication par type, à i = 0, sous une charge de 4,1 à 7,1. Elle inclut l'oracle à R complet, la
  variante à deux modes et les impressions. C'est donc un **majorant**, comme le déclare le générateur.
- **Le majorant pour les 17 cellules du §5.1 à 10⁴** : environ 163 h de mur sur 4 processus. Il dépasse de plus de
  deux fois le seuil de 72 h de Q-S-16 (A-3).
- **Il ne doit pas fonder la question A-3** : le coût des réplications i ≥ 200 (98 % d'une cellule) n'est pas mesuré.
- **Coût fixe de l'oracle** : l'oracle d'E-S-29 coûte à lui seul de l'ordre de 200 × 234 s ≈ 13 h de CPU pour les
  17 cellules [calc sur la mesure à i = 0]. Il est à garder distinct dans le plan.
- **E1** : environ 109 min au coût du point (2 s, à froid et sous charge), contre environ 70 min dans C1-COUT-1.
  L'ordre de grandeur est cohérent.
- **Le plan devra** :
  - appliquer C-1 ;
  - prendre le maximum mesuré, avec une marge déclarée pour la charge ;
  - reposer sur une mesure à i ≥ 200 et sur une réplication chaude d'E1 (BUDGET-SERRE-1).

## 11. Avis sur les questions Q-SB11-1 à Q-SB11-19

- **Q-SB11-1** : accord. La frontière d'E-S-01 couvre les deux modules (`test_fitness` énumère le dossier).
- **Q-SB11-2** : accord, à adjuger avant E0. Ajouter un composant ne change aucun autre flux : la clé SHA-256 nomme le
  composant (E-S-41).
- **Q-SB11-3** : accord, à adjuger avant E0. Aucune cellule n'emploie encore la grille « large » (O-11).
- **Q-SB11-4** : accord sur m − 1. Je suggère que l'en-tête [ÉCART-TYPE I_t] nomme le dénominateur.
- **Q-SB11-5** : accord. D*(u) = H ∪ F correspond au type « ecart » d'EP, qui comprend la panne, et c'est la série de Q₁.
- **Q-SB11-6** : accord. Le sous-ensemble est le même que celui de l'oracle, et le paquet devra le dire.
- **Q-SB11-7** : c'est un défaut au regard d'E-S-28 et d'E-S-52. À n′_s = 0 < n_s/2, la règle définit NON ÉVALUABLE
  (cause n_prime), et à n′_s = 1 le moteur rend [unites, k_crit, runs, n_prime]. Je ne le corrige **pas dans ce lot** :
  - le défaut est dans `regle.tester` (SB-7) et change une sortie de la règle ; la liste des causes au cas dégénéré
    demande une ligne d'adjudication, que je recommande égale à celle de n′_s = 1 ;
  - le refus nommé est un défaut sûr : aucun chiffre faux n'est produit ;
  - je ne l'ai pas reproduit à W = 1 sous ma cellule (n′ de stress de 2 434 à 2 736 pour i = 0 à 3).

  En revanche, il **bloque E0** : un lot qui le rencontre échouerait à chaque reprise (E-S-45). L'item NPRIME-NUL-1 doit
  porter un test qui reproduit le cas, puisque E-14 a déplacé la fixture pour l'éviter.
- **Q-SB11-8** : accord. ETH sans condition dans toutes les cellules est un sur-ensemble de « N1 et N3 », ce qui a un
  coût.
- **Q-SB11-9** : accord. J'y ajoute l'ε de N10 (O-10).
- **Q-SB11-10** : accord avec E1-LANCEUR-1. Je recommande que `lancer_e1` calcule lui-même ses oracles internes, dont
  E-S-39 contre r1, au lieu de recevoir un dictionnaire de booléens.
- **Q-SB11-11** : accord.
- **Q-SB11-12** : accord. P-L20-1 est à régler avant E0 : un schéma changé après E0 serait une déviation.
- **Q-SB11-13** : accord, comme majorant. Le plan réel suit le §10.
- **Q-SB11-14** : accord. L'O-3 de l'item reste comme limite écrite.
- **Q-SB11-15** : accord avec la phrase, conforme au refus de `calib_fiv.selection`. L'orchestrateur la date.
- **Q-SB11-16** : j'accepte 3 × 6 dans la suite. Je demande avant E0 un passage hors suite : 3 cellules × au moins
  202 réplications, pour couvrir i ≥ 200 (O-5), 1 contre 4 processus, PYTHONHASHSEED 0 contre 1, W réduit déclaré.
- **Q-SB11-17** : accord, FAMILLES-1 avant E0.
- **Q-SB11-18** : accord. J'admets une seconde mesure par type (i = 200 ; E1 à i = 1), sur une machine moins chargée,
  avant l'approbation du plan.
- **Q-SB11-19** : je ne le corrige pas dans ce lot. Le JSON fait foi, et le renfort d'E-17 l'exige. VALS-STRICT-1 est à
  régler avant E0, au brief de SB-12, par `zip(…, strict=True)` (la matrice commence à 3.10) ou par un refus nommé, en
  y joignant O-9.

## 12. Items

- **Proposés par le générateur** :
  - BUDGET-SERRE-1 : accord, avant E0. J'y ajoute C-1, une marge déclarée et le coût de l'oracle compté à part.
  - VALS-STRICT-1 : accord, avant E0. J'y ajoute O-9.
  - MUT-EQUIV-FIXTURE-1 : accord, avec une portée plus large. Les 12 vivants de cette G2 sont des fixtures équivalentes
    à des sites d'appel. La règle à inscrire au prochain brief de campagne : « pour chaque paramètre passé sous étiquette
    (W, n′_s, R, prm de la cellule, point par strate), une fixture où sa valeur diffère de toute source concurrente ».
    Elle est à joindre à SHOGEN-MUTANTS-SITE-APPEL-1.
- **Autres items du générateur** :
  - NPRIME-NUL-1 : bloque E0, avec un test qui reproduit le cas ;
  - P-L20-1, FAMILLES-1, E1-LANCEUR-1 (avec O-6), TDET-ECHELLE-1 (avec i ≥ 200) : accord ;
  - MUT-DUREE-1 : accord. Je l'ai mesuré : mutants jusqu'à 209 s en PAR=2 sous une charge d'environ 5, témoin seul
    130 s, borne 300 s.
- **Item à former** : SHOGEN-SIM-BIS-AGREGATS-SB12-1 (O-4). Les agrégats d'E-S-23, E-S-24, E-S-32 et E-S-34 sont à
  écrire par SB-12 depuis les lots, avec les tests.

## 13. Écarts du réviseur

- **E-R1** : le premier et le deuxième passage de P-4 et P-5 étaient invalides. La cellule de test (R = 99) était hors
  schéma sous `PRM` (R = 9 999 ou 999), de sorte que le refus était obtenu pour une autre raison. Je l'ai vu, corrigé
  (`P99`) et refait. Seul le troisième passage est compté.
- **E-R2** : la première ligne de la sonde portait une heure estimée (« vers 05:35 »). Je l'ai corrigée, avant tout
  autre usage, par les bornes lues : 05:21:06 et 05:29:38.
- **E-R3** : les preuves, des tests courts de 12 s au plus, ont tourné de 06:18 à 06:21 en même temps que `apres.sh`.
  Il y avait donc deux processus, dont un lourd.
- **E-R4** : il n'y a pas de G-02 dans mes mutants. Je l'ai écarté avant le lancement, comme équivalent.
- **E-R5** : des index git existent dans mes copies `g2/` (§1). Aucune écriture n'a touché le dépôt réel.

## 14. Journal de provenance (G1)

**Lu [lu]**
- `BRIEF-SB11.md`, `LIGNES-BRIEF-SB11.md`, `G0-SIM-BIS.md` : en entier.
- `PROPOSITION.md` : §2, §5 à §7 (l.129-448).
- `AVIS.md` : grep ciblé, et Q-S-06 (l.34-45).
- Annexe B : l.1022-1261, items du brief par leur nom.
- `revue-integ/` : G2, CORRECTIONS-G2, CONTRE-CONTROLE-1 et 2, CORRECTIONS-CC, par grep ciblé ;
  RAPPORT-GENERATEUR-transcrit l.9-112.
- `RAPPORT-GENERATEUR.md` : en entier.
- Les 21 diffs : fichiers neufs lus à l'état final, lignes retirées de tous les diffs listées.
- Code : `executer.py`, `e1.py`, tous les tests ajoutés ; `calib_fiv.py` l.32-72 et 148-321 ; parties de `commun.py`,
  `sources.py`, `observateurs.py` et `regle.py`.
- `scripts/plan-s2bis-2/intervalles.py` l.1-80 ; `plan-s2bis/regles.quantile` et `episodes.episodes`.
- `gates.yml` (jobs) ; `verdict-suite-s2.py` (codes de sortie et AMORCE) ; `isole.sh`.

**Seconde main [2nd]** : journaux du générateur (campagnes, témoins par étape, rouges, `budget.txt`, `final.txt`), lus
comme des données.

**Commandes, toutes consignées dans `NOTES.md` et `journal/`** :
- `sha256sum -c` : 1 199 OK ;
- application de la série et reconstruction des étapes ; recomptes de lignes, d'octets 92, de longueurs et de planchers ;
- valeurs de référence recalculées par `bc` ;
- campagne de mutants (`mut/campagne.txt`) ; preuves (`journal/preuves.txt`) ;
- `apres.sh` (`journal/resume.txt`) ; xtask (`journal/xtask-*.txt`, VERDICT seuls) ; R-13 (`outils/r13.py`).

**Chiffres recomptés par moi** : lignes et planchers par diff, total 2 793, 0 octet 92, mutants (21 / 5 / 16), durées de
`plan` (5 412 s), Ran de chaque job.
