# Rapport du générateur de SB-11x, y et z, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:27:52 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts de l'advisor (claude-fable-5-1), du générateur-correcteur, du réviseur et du contre-contrôleur (claude-opus-5-5), par le fm11.py versé et par celui de DETTES-T3 : fragments_l51_l14 = 0. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : SB-11x (SHOGEN-SIM-BIS-NPRIME-NUL-1), 2026-10-09, écrit à partir de 12:36:25 UTC

## 0. Gate 0
Modèle résolu : `claude-opus-5-5` (identifiant de l'environnement de l'agent), worker G1, générateur. Je n'ai écrit ni
l'avis, ni l'adjudication, ni SB-11a … w. La G2 qui suit doit être neuve (réviseur ≠ générateur).

## 1. Rattachement (G0)
- ADJUDICATION.md (sha256 28ff0c90…1849), option (b) : lieu `executer.replication`, `regle` intact, enregistrement
  dégénéré champ par champ, six tests.
- AVIS.md (sha256 2024f275…2ef2) : constat, tests 1 à 6, mutants.
- PROPOSITION.md (sha256 0e78afab…9dd6) l.182 (E-S-28), l.209 (E-S-45), l.221 (E-S-52) [lu].
- RAPPORT-CC.md, section NPRIME (l.231-246), et `journal/nprime.txt` du contre-contrôle de SB-11 [lu].

## 2. Diff SB-11x (à appliquer après SB-11w)
`SB-11x.diff`, sha256 `c86a4d9b994922013f899e29acf4266c166049dfc855f26e19f3417126ea73a1`, 246 lignes. Il ajoute 176
lignes et en retire 8 (borne R-25 : 200). Il contient 0 octet 92, 0 TODO et 0 FIXME. Les lignes Python font au plus
120 caractères (118 dans executer.py, 119 dans test_nprime.py).

| fichier | + | − | objet |
|---|---|---|---|
| scripts/sim-bis/executer.py | 26 | 6 | `_vide(p, rg)` ; dans `replication`, `vide = n[s] == 0` par strate, `_vide` à la place de `_tester`, compte d'événements sauté si `vide` ; docstrings |
| scripts/sim-bis/tests/test_nprime.py | 148 | 0 | les tests 1 à 5 de l'avis (le test 6 est la campagne de mutants) |
| scripts/sim-bis/README.md | 1 | 1 | ligne `executer.py` : SB-11x. La ligne est une rangée de tableau : 4 606 caractères, contre 4 240 avant |
| .github/workflows/gates.yml | 1 | 1 | plancher sim-bis 268 → 273 (`--egal`) |

Fichiers inchangés (sha256 égaux avant et après) : regle.py 5875ccbd…, variante.py 3906f1f6…, calendrier.py
9fecdca0…, oracle_recalc.py a5805ffa…, tests/test_regle.py 3cf99c66…, tests/test_oracle_recalc.py 48732980….

Enregistrement dégénéré (`_vide`), par classe de la strate :
- champs de tête : valeur `VALEURS[2]` (NON ÉVALUABLE), causes `list(regle.CAUSES)`, C = R de la cellule, C1 = 0,
  C_S = R si S est suivie (sinon None), r = R, K = 0, runs = 0, unites = 0, S = 0 si S est suivie (sinon None) ;
- « avec » : les mêmes champs, plus retirees = [] et indice = Fraction(0) ;
- variante[d] : les mêmes champs sans S, avec C_S = None et N = `variante.demi(0, d, p)` = 0 ;
- ni clé « evenements », ni appel à regle ou à variante.tester ou deux_modes pour cette strate.

## 3. Rouges : les tests d'abord
- 11:44:45, avant tout code, `tests.test_nprime` donne Ran 5, FAILED (failures=4). Les quatre tests rouges sont
  test_reproduction, test_forme_et_agreger, test_equivalence_regle et test_determinisme. Chacun échoue sur
  « AssertionError: refus REGLE/entier : … n = 0 : entier ≥ 1 attendu », et le refus est converti en échec nommé.
  test_contrat_regle_inchange est vert, comme attendu. Pièce : journal/rouge-avant.txt.
- 11:45:24, après le correctif : Ran 5, OK (journal/vert-apres.txt).

## 4. Tests de l'avis
1. **test_reproduction** : la recette `replication(P99, EP, cel(grille large, repli), POINTS, 1, 1)` passe. La garde
   de fixture vérifie n′ de stress = 0 et n′ de calme > 0. Pour chaque classe : NON ÉVALUABLE, les quatre causes
   écrites à la main, premiere None, retraits non vides.
2. **test_forme_et_agreger** :
   - fixture : quatre classes, S suivie, critère collectif, variante 4 et 8, événements 2 ; R de la cellule 99 sous
     un prm à R = 199 (R_approche = 99) [phrase retirée le 2026-10-09, C-6 de la G2 de SB-11x : l'affirmation
     d'étiquettes toutes distinctes de leurs sources concurrentes était inexacte (S égale à absorption, R de la
     cellule égal au R_approche du prm) ; voir la section datée « SB-11y et SB-11z »] ;
   - espions : regle.oracle (8 appels), variante.deux_modes (8) et loi_evenements (4), tous en calme seulement ;
   - stress : enregistrement égal à un attendu écrit à la main ;
   - clés : les mêmes qu'en calme, « evenements » à part ;
   - `agreger` sur trois copies donne NON ÉVALUABLE 3, insuffisante 3, chaque cause 3 et une seule combinaison, dans
     les blocs « sans », « avec », variante 4 et variante 8.
3. **test_equivalence_regle** :
   - deux cellules : S non suivie (sans critère ni variante), puis la cellule riche ;
   - chaque classe de stress égale, champ par champ, la sortie de `regle.tester`, de `regle.filtrer` et de
     `variante.tester` sur séries vides, à n = 1 et n_s = 2 736 ;
   - la référence est la même à n_s = 3 ;
   - avec `regle.CAUSES` permutée (mock), l'enregistrement suit la permutation.
4. **test_contrat_regle_inchange** : à n = 0 et sur séries vides, tester, oracle, deux_modes, loi_evenements, filtrer
   et variante.tester lèvent REGLE/entier. test_regle.py et test_oracle_recalc.py ne sont pas touchés et restent verts
   (Ran 273).
5. **test_determinisme** : dans la suite, deux réplications donnent la même empreinte, et deux `ecrire_lot` les mêmes
   octets et le même sha256. Le passage hors suite est consigné dans journal/determinisme.txt :
   - lot [0, 4) de la cellule riche, en 1 processus sous PYTHONHASHSEED=0, puis en 4 processus sous
     PYTHONHASHSEED=1 ;
   - même sha256 (e4d5fecc…6fd7), même empreinte (8827bce2…0bfc), `cmp` sans écart ;
   - n′ de stress [2736, 0, 2736, 2736].
6. **Mutants** : voir §5.

## 5. Mutants (test 6)
Commande exacte du job : `verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher 273`. Le réseau est
isolé et les variables de mandataire retirées par `env -u`. La borne est de 300 s, avec `os.killpg` de la session au
dépassement. Deux mutants tournent en parallèle (PAR=2). Classement : sortie 1 = tué, 0 = vivant, toute autre = FATAL.
Pièces : mut/campagne.txt et mut/<id>.txt.

| id | mutation | classement | tests rouges |
|---|---|---|---|
| TEMOIN-debut / TEMOIN-fin | aucune | VIVANT, Ran 273 (145 s / 134 s) | — |
| M-NP-01 | `n[s] == 0` → `n[s] < 0` (jamais pris) | TUÉ | reproduction, forme, équivalence, déterminisme |
| M-NP-02 | causes écrites en littéral au lieu de `regle.CAUSES` | TUÉ | équivalence (CAUSES permutée) |
| M-NP-03 | compte d'événements non sauté | TUÉ | forme, équivalence, déterminisme |
| M-NP-04 | C = 0 au lieu de R | TUÉ | forme, équivalence |
| M-NP-05 | n′ de stress lu pour toutes les strates (une strate pour l'autre) | TUÉ | forme (espions) |
| M-NP-06 | n′ de calme lu pour toutes les strates (une strate pour l'autre) | TUÉ | reproduction, forme, équivalence, déterminisme |
| M-NP-07 | R du prm au lieu du R de la cellule | TUÉ | forme, équivalence |
| M-NP-08 | « avec » omis | TUÉ | forme, équivalence |
| M-NP-09 | variante omise | TUÉ | forme, équivalence |
| M-NP-10 | C_S sans S | TUÉ | forme, équivalence |
| M-NP-11 | S None quand S est suivie | TUÉ | forme, équivalence |
| M-NP-12 | C_S de la variante = R | TUÉ | forme, équivalence |
| M-NP-13 | N = diviseur | TUÉ | forme, équivalence |
| M-NP-14 | indice None | TUÉ | forme, équivalence |
| M-NP-15 | S omis de « avec » | TUÉ | forme, équivalence |

Bilan : 15 mutants sur 15 tués, par AssertionError seules (0 ERROR, 0 FATAL, 0 dépassement de borne). Les runs ont
duré de 134 à 172 s. Les rouges ciblés préalables (journal/rouges.txt) concordent.

## 6. Gates sur une copie neuve
Copie f : git archive de 19a0c7e (tête relue à 12:18:43), puis SB-11a … w (rebase-sb11/diffs), puis SB-11x. Les 24
diffs passent en code 0, sans rejet ni décalage. La copie fn est 19a0c7e seule, pour comparer xtask. Pièce :
journal/gates.txt.

| étape | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis (plancher 273) | conforme, Ran = 273, 140 s |
| s2bis (plancher 340) | conforme, Ran = 340 |
| S2 | conforme, Ran = 415, 2 sauts nommant la variable |
| matrice 3.10, 3.11, 3.12, 3.13 (`-X dev -W error`) | code 0, Ran 273, OK ; 0 « Exception ignored », 0 « Warning » |
| xtask, f et fn | code 0 ; 10 lignes VERDICT identiques (9 VERT + global VERT) ; seules les lignes VERDICT ont été gardées |

## 7. Écarts
- **E-1, incident sans effet sur les preuves.** La première suite, lancée par `setsid nohup &`, a été sondée sur le
  PID de setsid (1519) et non sur celui de l'enfant. Un second run a donc tourné 8 s en même temps et tronqué le
  fichier de sortie. Les deux runs ont été tués, aucun n'est compté, et la suite a été relancée seule (conforme,
  Ran 273).
- **E-2, forme du test 2.** Le test 2 de l'avis demande des clés égales entre stress et calme sur une cellule à
  événements ≥ 2. L'adjudication fait sauter la branche des événements : l'égalité est donc tenue hors
  « evenements », et l'absence de la clé est vérifiée. Aucun consommateur de cette clé n'existe dans scripts/sim-bis
  (grep), et sa présence varie déjà avec i.
- **E-3, valeurs de référence.** La référence du test 3 est prise à n = 1, car n = 0 est refusé par le contrat. n_s
  vaut 2 736 dans l'enregistrement (W = 1). L'identité de la référence à n_s = 3 est vérifiée à part.
- **E-4, mutants équivalents.** Les champs nuls (K, runs, unites, C1, S, N) valent tous 0 par construction : un
  mutant qui en échange deux est équivalent. Je n'en ai compté aucun.
- **E-5, écritures git dans des copies seulement.** J'ai fait `git init` avec alternates vers
  /home/user/shogen/.git/objects dans les copies dev, f et fn, pour oracle_r1 et oracle_recalc, et `git add -N` dans
  la copie x, pour former le diff. Le dépôt réel n'a rien reçu.
- **E-6, machine partagée.** Pendant la campagne et les gates, un autre agent faisait tourner des suites s2bis. Les
  durées restent sous la borne.

## 8. Items à former (PAROXYSME)
- **I-1, empreinte du G0.** L'ajout daté au G0 change le sha256 de docs/adr-0029/g0-sim/G0-SIM-BIS.md. Or
  `parametres.json` (rattachement) et tests/test_commun.py l.61-62 épinglent `a216a953…`. Le versement du texte doit
  porter les nouvelles épingles, sinon test_commun rougit (fil d'alarme de SB-14H). C'est hors de mon diff, car le
  texte n'est pas le mien.
- **I-2, oracle d'E-S-29.** Les comparaisons effectives de l'oracle baissent pour les strates à n′ = 0. C'est écrit
  dans le README et dans les docstrings, et c'est à écrire au G0.
- **I-3, taux d'information insuffisante.** Chaque réplication à n′ = 0 y compte, sous la combinaison
  « unites+k_crit+runs+n_prime ». C'est à signaler au paquet (E-S-52).

## 9. Proposition de texte pour l'ajout daté au G0 (sous E-S-28 et E-S-52)
Proposition ; la rédaction revient à l'orchestrateur.

> **Ajout daté du 2026-10-09 (SHOGEN-SIM-BIS-NPRIME-NUL-1 ; sous-lot SB-11x ; adjudication de l'orchestrateur,
> option (b), sur l'avis de l'advisor).**
>
> **Strate sans fenêtre retenue (n′_s = 0).** Il arrive qu'à T_max aucune fenêtre évaluable ne soit retenue dans une
> strate s : `calendrier.retenues` rend alors n = 0. Pour cette strate, `executer.replication` n'appelle ni `regle`
> (tester, oracle, loi_evenements, filtrer), ni `variante` (tester, deux_modes). `regle` garde son contrat : n ≥ 1,
> sinon REGLE/entier (contrat RB-6 §4, SHOGEN-SIM-BIS-CONTRAT-RB6-1).
>
> Chaque classe de la strate reçoit l'enregistrement que `regle.tester` rend sur des séries vides :
> - valeur NON ÉVALUABLE ;
> - causes = `list(regle.CAUSES)` = [unites, k_crit, runs, n_prime] : 0 unité en écart, moins de 2 ; C1 = 0, au plus
>   le seuil ; 0 run, moins de 2 ; 2·0 < n_s ;
> - K = 0, runs = 0, unites = 0, et S = 0 si S est suivie (sinon None) ;
> - aucun arrêt anticipé : C = R (R de la cellule), C1 = 0, C_S = R si S est suivie (sinon None), r = R ;
> - « avec » (critère collectif actif) : les mêmes champs, plus retirees = [] et indice = 0 ;
> - variante[d], pour chaque diviseur de la cellule : les mêmes champs sans S, avec C_S = None et N = ⌊0/d⌋ = 0.
>
> L'égalité de cet enregistrement avec `regle.tester` et `variante.tester` est vérifiée champ par champ, sur séries
> vides à n = 1 et n_s ≥ 3.
>
> **Ce que la strate n'a pas.** Elle n'a pas de compte d'événements (E-S-34) ni de clé « evenements ». Aucune
> comparaison d'oracle d'E-S-29 n'y est faite. Le sous-ensemble pré-déclaré reste les 200 premières réplications, mais
> le nombre de comparaisons effectives baisse d'autant ; il n'existe là aucune rotation à comparer.
>
> **Comptage.** La réplication n'est pas refusée : elle est comptée (E-S-45). Au comptage d'E-S-52, chaque réplication
> à n′_s = 0 ajoute 1 à chacun de ces comptes : NON ÉVALUABLE, chacune des quatre causes, information insuffisante, et
> la combinaison « unites+k_crit+runs+n_prime ». L'axe « n′_s < n_s/2 seul » reste lisible par la combinaison
> « n_prime ». Le taux d'information insuffisante des cellules qui produisent n′_s = 0 inclut ces réplications ; ce
> point est à signaler au paquet.
>
> **Recette et tests.** Recette de reproduction : cellule T-imp, grille « large », repli, W = 1, i = 1, P99 ; n′ de
> stress = 0 pour n_s = 2 736. Tests : `scripts/sim-bis/tests/test_nprime.py`.

Ligne d'item proposée : « SHOGEN-SIM-BIS-NPRIME-NUL-1 : fermé par SB-11x ; causes [unites, k_crit, runs, n_prime] ;
recette T-imp large repli W = 1 i = 1 ; lieu executer.replication, regle intacte. »

## 10. SB-11y et SB-11z — section datée du 2026-10-09, écrite à partir de 14:52:03 UTC
Gate 0 : modèle résolu `claude-opus-5-5`, générateur. Entrées : g2/RAPPORT-G2.md (ACCEPTE-AVEC-CORRECTIONS ;
g2/SHA256SUMS 57/57 OK), ajout daté d'ADJUDICATION.md (après 13:49:50 UTC), G0-AJOUT.md (sha256 2341498a…42c3),
g2/outils/mutants_g2.py et epingles_g0.py ; g2/propositions/test_nprime_g2.py lu comme donnée, non recopié. SB-11x
n'est pas touché (sha256 c86a4d9b…a73a1).

### Diffs (dans l'ordre : SB-11x, puis SB-11y, puis SB-11z)
| diff | sha256 | lignes | + / − | plancher sim-bis |
|---|---|---|---|---|
| SB-11y.diff | 185db61bdda8e94fa2db745f7dea4396636f669356d085e0b842bd23c54a4c0d | 206 | 85 / 26 | 273 → 277 |
| SB-11z.diff | dbc916030e5a66dcac96cdd127e8afc32d8ae3c486914a9e616bd8c50d44bc32 | 55 | 15 / 4 | 277 (aucun test ajouté) |

Contrôles des deux diffs : 0 octet 92, 0 TODO ou FIXME, lignes Python de 119 caractères au plus. Lignes plus longues :
la rangée README (4 842 caractères ; O-4 de la G2, format préexistant), le paragraphe du G0 (texte de l'orchestrateur,
recopié tel quel) et la ligne `rattachement` de parametres.json (préexistante, une seule ligne JSON).
Application : sur 2229e15 (tête, SB-11w commis), SB-11x, y et z passent par patch -p1 en code 0, sans rejet ni décalage.
Sur 798176f (tête relue à 14:51:47 ; seul changement sur nos chemins : plancher s2bis 340 → 341 par DETTES-T1), les trois
diffs passent aussi (dry-run puis application, sur scripts/sim-bis, g0-sim et gates.yml).

### Corrections
| id | fait | test | mutants (rouge d'assertion, puis tués par la commande du job) |
|---|---|---|---|
| C-1 | fixtures à S et absorption opposés : (S, critère absent, variante 8) puis (S absente, critère, variante 4) | test_etiquettes_croisees_et_octets | G2-M04, G2-M05, G2-M06 ; neufs M-NP-16 (S de « avec » lu sur absorption), M-NP-17 (« avec » sous critère ou S) |
| C-2 | R de la cellule égal au R_approche (99), puis au R (199) d'un prm où ils diffèrent ; C et r comparés à R | même test | G2-M08 ; neufs M-NP-18 (r = R_approche), M-NP-19 (C_S = R_approche) |
| C-3 | source de « vide » : 0 < n′ < n_s/2 (i = 65, n′ 650, suffisant faux) passe par la règle ; `regle.premiere` rendue None à n′ > 0 : règle appelée dans les deux strates | test_n_prime_partiel, test_premiere_absente | G2-M01, G2-M03 ; neufs M-NP-22 (vide si n′ < n_s/4), M-NP-23 (vide si n′ nul ou première absente) |
| C-4 | égalité en octets du JSON canonique (`commun.json_canonique(executer.jsonable(·))`) avec la référence regle/variante sur séries vides à n = 1 ; la référence est passée en fonction de module (`reference`), réemployée par test_equivalence_regle | test_etiquettes_croisees_et_octets | G2-M12, G2-M13 ; neufs M-NP-20 (C1 = Fraction(0)), M-NP-21 (K = False) |
| C-5 | plancher exact 277 (`--egal`) | job : conforme, Ran = 277 | témoin sous 276 : sortie 1 (« Ran 277 > plancher 276 ») ; sous 278 : sortie 1 (« Ran 277 < plancher 278 ») |
| C-6 | §4 point 2 de ce rapport : phrase retirée (marque datée en place) | — | sans objet (texte) |
| C-7 | `agreger` : par strate, « n_prime_nul » (réplications à n′_s = 0) et « oracle » (comparaisons effectives de l'oracle d'E-S-29 : réplications i < ORACLE à n′_s > 0) ; par cellule, « oracle » (somme). test_agreger complété (n′ = i % 3 : 2 et 3 ; clés de l'agrégat) | test_compte_n_prime_et_oracle, test_agreger | neufs M-NP-24 (n′ nul lu sur « suffisant »), M-NP-25 (i ignoré), M-NP-26 (n′ ignoré), M-NP-27 (somme de cellule = dernière strate) |

Rouges : à 13:52:56, sous le code de SB-11x, tests.test_nprime et tests.test_executer donnaient Ran 22, FAILED
(failures=2) : test_compte_n_prime_et_oracle (« [[None, None], [None, None], None] != [[0, 2], [2, 1], 3] ») et
test_agreger (clés sans « oracle ») ; vert à 13:53:12, après C-7 (journal/y-rouge-avant.txt, y-vert-apres.txt). Les
tests de C-1 à C-4 passent sur le code livré, qui est correct : leur rouge se montre sous chaque mutant visé (rouges
ciblés, journal/rouges-y.txt : 20 mutants, chacun par AssertionError du test visé).

### Campagne (mut-y/campagne.txt ; 13:57:49 → 14:35:03 ; PID 26207)
Commande exacte du job (`verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher 277`), arbre z, réseau
isolé, `env -u` des mandataires, borne 300 s, `os.killpg`, PAR=2. Témoins de début et de fin : VIVANT, Ran 277 (143 s,
139 s). 20 mutants sur 20 tués (sortie 1), les 8 de la G2 et 12 neufs, par AssertionError ; M-NP-24 donne en plus une
ERROR (KeyError « suffisant » dans test_agreger, dont les enregistrements écrits à la main n'ont pas ce champ), et son
AssertionError est dans test_compte_n_prime_et_oracle. 0 FATAL, 0 borne, 154 à 186 s.

### SB-11z (G0 et épingles, un seul diff)
- G0 : G0-AJOUT.md ajouté octet pour octet à la fin de docs/adr-0029/g0-sim/G0-SIM-BIS.md (cmp de la fin = G0-AJOUT ;
  tête inchangée) ; sha256 neuf c6c8e692645a59b0d9c67452157c0b46303cb8b9646738d8c232684e545a6210.
- Épingles : `python3 -B g2/outils/epingles_g0.py <arbre> "NPRIME-NUL-1 du 2026-10-09 13:49:50 UTC"` (heure de
  G0-AJOUT.md) : parametres.json, une ligne remplacée en texte (JSON relu sans erreur) ; test_commun.py,
  test_provenance_c_5 : préfixe c6c8e692…, maillon « avant l'ajout daté NPRIME-NUL-1 … : a216a953… », [True, True, True] ;
  docstring complétée (SB-11z, mutant M-Z-01 « épingle a216a953… remise »).
- Preuves (outils/preuves_z.py, journal/preuves-z.txt, 13:54:08) : témoin, tests.test_commun Ran 22 OK ; preuve 1,
  ancienne épingle remise dans parametres.json : FAILED (failures=2 : test_g0_mesure, test_provenance_c_5) ; preuve 2,
  G0 augmenté d'un octet : FAILED (failures=1 : test_g0_mesure) ; preuve 3 : suite entière verte (gates ci-dessous).

### Gates (journal/gates-y.txt ; 14:35:38 → 14:51:30 ; PID 20693)
Copie f2 = git archive 2229e15 + SB-11x + SB-11y + SB-11z ; fn2 = 2229e15 seule.
| étape | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis (277) | conforme, Ran = 277 (147 s) |
| s2bis (340, plancher de 2229e15) | conforme, Ran = 340 |
| S2 | conforme, Ran = 415, 2 sauts nommant la variable |
| matrice 3.10 / 3.11 / 3.12 / 3.13, `-X dev -W error` | code 0, Ran 277, OK ; 0 « Exception ignored », 0 « Warning » |
| xtask f2 et fn2 | code 0 ; 10 lignes VERDICT identiques (9 VERT + global VERT), lignes VERDICT seules gardées |
Fichiers inchangés (cmp f2 contre fn2) : regle.py, variante.py, calendrier.py, oracle_recalc.py, test_regle.py,
test_oracle_recalc.py.

### Écarts
- E-7 : la rouge de C-1 à C-4 n'existe que sous mutant (le code de SB-11x est correct) ; seule C-7 a un rouge sur le
  code d'avant.
- E-8 : test_agreger (test_executer.py, SB-11h) est modifié : champ « n » ajouté aux enregistrements écrits à la main
  (n′ = i % 3), clés de l'agrégat et assertion des deux comptes ajoutées ; aucune assertion retirée.
- E-9 : copie de travail « base » avec git init, alternates et commits locaux (base, x, y, z) pour former les diffs ;
  copies seulement. Le dépôt réel n'a reçu aucune écriture ; à 14:51:47 son index portait gates.yml, posé par un autre
  acteur.
- E-10 : la tête a avancé pendant les gates (2229e15 → 798176f ; plancher s2bis 341, DETTES-T1). Les gates ont tourné
  sur 2229e15 ; sur 798176f, seule l'applicabilité des trois diffs a été vérifiée, pas la suite s2bis à 341.
- E-11 : M-NP-24 mêle une ERROR à son AssertionError (voir la campagne) ; il reste classé tué par sa sortie 1, et
  l'assertion du test visé est présente.

### Items
- I-1, I-2 et I-3 du §8 sont fermés : I-1 par SB-11z, I-2 et I-3 par C-7 (comptes imprimés dans l'agrégat). La forme
  de leur impression au paquet reste celle de l'agrégat ; le paquet lui-même n'existe pas encore.
- [phrase retirée le 2026-10-09, C-10 (R-3 du contre-contrôle de SB-11y et SB-11z)] O-4 : aucun défaut (format
  préexistant, aucune règle enfreinte) ; ni item ni réserve.
- Le texte proposé au §9 est remplacé par G0-AJOUT.md, qui lève l'ambiguïté O-3 (S entier 0, indice Fraction(0),
  sérialisé « "0" »).

## 11. Corrections du contre-contrôle (C-8 à C-12) — section datée du 2026-10-09, écrite à partir de 16:24:50 UTC
Gate 0 : modèle résolu `claude-opus-5-5`, générateur. Entrées : ajout daté 15:26:10 UTC d'ADJUDICATION.md ;
g2/cc/RAPPORT-CC.md (CONFORME-AVEC-RÉSERVES, R-1 à R-5 ; g2/cc/SHA256SUMS sans échec) ; g2/cc/outils/mutants_cc.py ;
g2/cc/propositions/test_nprime_cc.py lu comme donnée. Base : tête 0cfbe3e (SB-11a … w commis ; sim-bis = w recalé).
SB-11x inchangé (c86a4d9b…a73a1). Anciennes versions : travail/avant-cc/SB-11y.diff (185db61b…), SB-11z.diff
(dbc91603…).

### Diffs corrigés (mêmes noms)
| diff | sha256 | lignes | + / − | plancher sim-bis |
|---|---|---|---|---|
| SB-11y.diff | f24a64a74c8a40a69db3178d5afa69b3bcbb9b9dfd2347f240968015f56ac7ac | 239 | 116 / 28 | 273 → 279 |
| SB-11z.diff | 0888a978644f87c609bfbff2afa2a574eae94df119d2dde1cbe5acdb601a823d | 66 | 16 / 5 | 279 |
0 octet 92, 0 TODO ou FIXME ; Python ≤ 120 caractères. Sur 0cfbe3e, x, y et z passent par `patch -p1 -F0` en code 0.

### Corrections
| id | fait | preuve |
|---|---|---|
| C-8 (R-1) | SB-11z : ligne de G0-SIM-BIS.md de docs/adr-0029/g0-sim/SHA256SUMS → c6c8e692…6210 | avant : `sha256sum -c` FAILED sur G0-SIM-BIS.md (journal/c8-avant.txt) ; après : 5/5 OK (c8-apres.txt) ; aucun test ni outil ne lit ce fichier (grep : seuls des commentaires nomment le dossier), donc pas de rouge de test |
| C-9 (R-2) | test_equivalence_regle : égalité en octets du JSON canonique avec la référence à n_s = 3, 4, 7 et 2 736 (l'égalité Python reste) | G2-M12, G2-M13, M-NP-20, M-NP-21, M-CC-02 rougissent désormais aussi ce test (AssertionError) |
| C-10 (R-3) | §10 : phrase sur la refonte du tableau retirée, marque datée : « O-4 : aucun défaut … ; ni item ni réserve » | — |
| C-11 (R-4) | test_n_prime_partiel_resultat (espion sur executer._tester, i = 65) | M-CC-01 tué par AssertionError |
| C-12 (R-5) | test_compte_premiere_absente (premiere None, i = 0 et 1 : n′ nul [0, 1], oracle [2, 1], cellule 3) | M-CC-03 et M-CC-04 tués par AssertionError (plus une ERROR KeyError dans test_agreger) |

Preuves de z′ (journal/preuves-z-cc.txt) : témoin test_commun Ran 22 OK ; ancienne épingle : FAILED (2) ; G0 + 1 octet :
FAILED (1).

### Campagne (mut-cc/campagne.txt ; 15:31:45 → 16:08:45 ; PID 12150 ; ps de fin vide)
Commande du job, `--plancher 279`, réseau isolé, `env -u` des mandataires, borne 300 s, killpg, PAR=2. Témoins VIVANT,
Ran 279. 25 sur 25 tués : les 20 de SB-11y (dont les 8 de la G2) et M-CC-01 à M-CC-05, chacun avec AssertionError ;
0 FATAL, 0 borne ; 130 à 166 s. Rouges ciblés préalables : journal/rouges-cc.txt.

### Gates (journal/gates-cc.txt ; 16:09:05 → 16:24:41 ; PID 32418) sur f3 = 0cfbe3e + x + y + z
| étape | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis (279) | conforme, Ran = 279 |
| s2bis (341) | conforme, Ran = 341 |
| S2 | conforme, Ran = 415 (2 sauts nommant la variable) |
| calib-actifs (65) | conforme, Ran = 65 |
| matrice 3.10 à 3.13, `-X dev -W error` | code 0, Ran 279 ; 0 « Exception ignored », 0 « Warning » |
| xtask f3 et fn3 (0cfbe3e seule) | code 0 ; 10 lignes VERDICT identiques, toutes VERT (archive complète ; lignes VERDICT seules gardées) |

### Écarts
- E-12 : C-8 n'a pas de rouge de test, aucun test ne lisant docs/adr-0029/g0-sim/SHA256SUMS ; la preuve est
  `sha256sum -c` avant et après.
- E-13 : SB-11y passe de 85 à 116 lignes ajoutées (sous 200) ; le README n'est pas retouché pour C-9, C-11, C-12.
- E-14 : copie b3 avec git init, alternates et commits locaux (dont un `reset --hard` sur y et un `commit --amend`),
  copie seule ; dépôt réel sans écriture (index vide sur nos chemins à 16:24:50).

## 12. Correction C-13 (R-6 de la passe 2 du contre-contrôle) — section datée du 2026-10-09, écrite à partir de 17:52:56 UTC
Gate 0 : modèle résolu `claude-opus-5-5`, générateur. Entrées : ajout daté 16:48:15 UTC d'ADJUDICATION.md ; section
« Passe 2 » de g2/cc/RAPPORT-CC.md et g2/cc/journal/r6.txt ; g2/cc/outils/mutants_cc.py (M-CC-06 à M-CC-09). Base :
0cfbe3e. Anciennes versions : travail/avant-c13/SB-11y.diff (f24a64a7…) et SB-11z.diff (0888a978…).

### Diffs
| diff | sha256 | lignes | + / − | plancher |
|---|---|---|---|---|
| SB-11x.diff | c86a4d9b994922013f899e29acf4266c166049dfc855f26e19f3417126ea73a1 (inchangé) | 246 | 176 / 8 | 273 |
| SB-11y.diff | d9f7329935a51b1682cd9e62cb92d556aeb27cd4c14fcb0ab7ec7a0b62d6e2ad | 242 | 119 / 28 | 279 (inchangé) |
| SB-11z.diff | 0888a978644f87c609bfbff2afa2a574eae94df119d2dde1cbe5acdb601a823d (inchangé) | 66 | 16 / 5 | 279 |
SB-11y ne change que dans test_n_prime_partiel_resultat : l'espion fige `octets(r)` à l'appel ; l'assertion compare
`octets(r["classes"]["BTC"])` à ces octets ; docstring : C-13, M-CC-06. 0 octet 92, 0 TODO ou FIXME, Python ≤ 120.
Application : sur 0cfbe3e, x, y et z en `patch -p1 -F0`, code 0 ; aussi sur 0781a68 (tête relue à 17:52:29 ; DETTES-T3
ajoute un job à gates.yml, plancher sim-bis toujours 279 après z).

### Preuves
- Rouges ciblés (journal/rouges-c13.txt, 16:49:05 → 16:52:32) : M-CC-01 et M-CC-06 rouges par AssertionError dans
  test_n_prime_partiel_resultat, 0 ERROR ; les 29 mutants sortent en 1.
- Campagne (mut-c13/campagne.txt ; 16:52:48 → 17:35:27 ; PID 18318) : commande du job `--plancher 279`, réseau isolé,
  `env -u` des mandataires, borne 300 s, killpg, PAR=2 ; témoins VIVANT, Ran 279 (131 s, 143 s) ; 29 sur 29 tués (les
  25 de la passe précédente et M-CC-06 à M-CC-09), chacun avec AssertionError ; 0 FATAL, 0 borne ; 135 à 190 s ; ps de
  fin vide.
- Gates (journal/gates-c13.txt ; 17:35:43 → 17:52:17 ; PID 27533) sur 0cfbe3e + x + y + z : runner 136 ok ; sim-bis
  conforme Ran = 279 ; s2bis conforme Ran = 341 ; S2 conforme Ran = 415 ; calib-actifs conforme Ran = 65 ; matrice 3.10
  à 3.13 `-X dev -W error` : Ran 279, OK, 0 « Exception ignored », 0 « Warning » ; xtask (archive complète) : 10 lignes
  VERDICT VERT, identiques à 0cfbe3e seule.

### Écarts
- E-15 : copie b4 avec git init, alternates et commits locaux (dont un `commit --amend`), copie seule ; le dépôt réel
  n'a reçu aucune écriture (son index porte gates.yml, posé par DETTES-T3).
- E-16 : la tête a avancé pendant les gates (0cfbe3e → 0781a68) ; gates jouées sur 0cfbe3e, comme demandé ; sur 0781a68,
  seule l'applicabilité des trois diffs est vérifiée.
