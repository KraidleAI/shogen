# Relecture G2 neuve — SIM-BIS tranche 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 07:43:22 UTC du rapport rendu par message par le réviseur G2 (agent a388ef21916294a7b) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

claude-opus-5-5

# Relecture G2 neuve : SIM-BIS, tranche 3 (SB-4I, SB-6A à SB-8C)

- **Gate 0** : je tourne sous `claude-opus-5-5`, effort max. Je suis réviseur G2 neuf et je n'ai rien généré de ce lot.
- **Horloge** (`date -u`) : 2026-10-05, de 06:45:43 à 07:40:32 UTC.
- **Dépôt** : tête `31643485cf90…` (3164348) au début et à la fin, `git status --short` vide. Aucune opération git en écriture dans /home/user/shogen.
- **Preuves** : `<scratchpad>/s2bis/sim3/g2/rev/`, avec `outils/` (26 fichiers), `sorties/` (56 fichiers) et `SHA256SUMS` (82 entrées, sha256 `db37d015…`, 82 sur 82 OK).
- **Nettoyage** : copies, arbres, cible cargo et TMPDIR supprimés ; 9,4 Go libres à la fin.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-3, liste fermée)

## Résumé
- **Série** : les neuf diffs s'appliquent sur la tête 3164348, 194 lignes de code au plus par diff, 1 314 au total. Chaque état est vert seul à son plancher exact : 93, 94, 98, 101, 105, 108, 112, 115, 117, 119. Aucune gate n'est affaiblie.
- **Code** : il est juste. Mes oracles, écrits depuis le G0 et l'ADR sans réutiliser le calcul du lot, ne trouvent aucun écart, sur plusieurs milliers d'instances. Le Monte Carlo des processus d'observateurs s'accorde aux paramètres.
- **Identité bit à bit** : toutes les empreintes déclarées sont reproduites, 16 fois sur 16. SB-4I tient la stabilité des dérives demandée par O-A. O-B est fermé.
- **Trois défauts** :
  1. `oracle()` ne contrôle pas la classification de C_S quand S est suivie (E-S-29) : une faute d'arrêt anticipé qui ne touche que C_S passe sans refus ;
  2. quatre mutants vivants de ma campagne montrent des trous de tests : les artefacts n'ont aucun effet testé sur la consolidation, le compte des unités sur des séries nulles et la loi des absences des paramètres ne sont pas exercés ;
  3. le compte des octets 92 de l'écart E-1 est faux dans le rapport.

## Contrôles

**1. Série**
- **Application** : copie `git archive 3164348` avec les 7 exclusions. Les neuf diffs passent `git apply --check` puis `git apply`, aucun .orig ni .rej. Sha256 des diffs égaux à `sim3/SHA256SUMS` (77f3268d…, 319 sur 319 OK).
- **Égalité avec les étapes du worker** : chaque état est égal à la photo e0…c8c du worker sur ses 17 à 21 fichiers. La tête est égale à e0, ce qui confirme l'écart de base déclaré.
- **Tailles, recomptées par mon script** (code ajouté / retiré) : +99/−34, +186/−2, +155/−3, +170/−3, +141/−1, +194/−4, +155/−11, +92/−4, +122/−18. Aucun octet 92. Ligne Python ajoutée la plus longue : 120 caractères.
- **Commande du job** : runner d'abord (33 ok), puis la ligne lue dans le `gates.yml` de l'état, borne 300 s. Sortie 0 sur les dix états, Ran égal au plancher (`sorties/etapes.txt`).

**2. Conformité, exigence par exigence**

| exigences | constat |
|---|---|
| E-S-17, E-S-18 | Conformes : absences D-1, dégradations, paires, perte, repli avec O4 absent, M_j. Les valeurs non fixées par le G0 sont posées en Q-T3-2, 3, 6 et 7. Loi des absences non testée : C-2 c. |
| E-S-19, E-S-20 | Conformes : vote tout axe, manque β, cache régional, ε par (o, u, t), défaut local sur toutes les séries. Q-T3-5, 8, 10 et 11. |
| E-S-21 | Le code est conforme : un seul processus pour O1 à O3 sur les 7 hôtes AS13335. Mais son effet sur D et sur ok n'est testé nulle part (V-02 et V-25 vivants) : C-2 a. |
| E-S-22 | Conforme : 3 500 instances contre mon oracle fenêtre par fenêtre, et trois cas à la main. |
| E-S-24, E-S-26, E-S-27 | Conformes : 3 000 cas de retraits ; vecteurs de décalage ; 5 000 décalages et rotations. |
| E-S-28 | Le code est conforme. Le compte des unités sur une série nulle n'est pas testé (V-22 vivant) : C-2 b. |
| E-S-29 | L'arrêt anticipé est exact (172 instances), mais l'oracle d'équivalence ne couvre pas C_S : C-1. |
| E-S-30, E-S-31, E-S-32, E-S-34, E-S-35 | Conformes : 36 cas construits ; 4 000 suites et 30 lois d'événements ; 3 000 pools d'absorption. |
| E-S-01, 03, 06, 41, 42, 43, 44, 53, 54, 55 | Tenues. |
| O-A, O-B | Tenues (contrôle 4, et K-05 tué). |

**3. Justesse, par des calculs indépendants**

*Consolidation et quorum*
- Oracle naïf, fenêtre par fenêtre, depuis E-S-19 à E-S-22 : 3 000 instances à M = 4 et 500 à M = 2 ou 3, aucun écart.
- Trois cas à la main, tous OK (`sorties/cas_main.txt`) : H1, quorum 3 sur 4 ; H2, quorum 2 sur 3 avec manque d'écart ; H3, quorum 2 sur 2 et M_j = 1.

*Rotation, K, S, C, K_crit et seuil*
- Les six vecteurs de RB-6, par `sha256sum` et `bc` seuls : 107527, 24225, 39743, 0, 6, 52807. La graine est le sha256 de « SHOGEN-RB6-VECTEURS ».
- Les cinq vecteurs de T-ROT-1, de même : 38692, 21459, 4167, 0, 18. La graine 26455ac1… est recalculée.
- Contrat RB-6 lu, reconstruit depuis RB-6a et RB-6b (ROTATION-S2BIS.md, sha256 d0078046…). Les onze points du §7 du worker sont exacts. K_crit de SIM-BIS égale le `tri[seuil] + 1` de RB-6 [calc].
- Cas à la main : K = 1 et S = 3, puis 1 et 1 après rotation ; R = 9, seuil 4 : REJETTE, C 4, C1 7, K_crit 2, moyenne 14/9 ; seuils 99, 9 et 4.

*Arrêt anticipé contre R complet, par mon propre oracle*
- 160 instances aléatoires à R = 999 et 12 à R = 9 999, dont une partie avec S suivie, aucun écart.
- Couvert : REJETTE, NE REJETTE PAS, NON ÉVALUABLE, les 4 causes, des arrêts et des passes complètes.
- Comparé : valeur et causes ; arrêt au premier r possible ; C, C1 et C_S sans arrêt ; loi, K_crit et moyenne du mode complet.

*Séquence d'ETH, F3, événements, absorption* : tous conformes, sur cas construits et aléatoires.

*Monte Carlo indépendant à graine fixe* (cellules G2-REV-T3-MC-*, espérances exactes calculées depuis les paramètres)

| processus | résultats, premier passage |
|---|---|
| absences (a = 1/50) | part z = −1,99 ; O1 et O2 ensemble z = +1,18 ; débuts z = −0,72 ; longueurs 1:1:1, χ² = 2,21 (2 ddl) |
| dégradations | \|z\| ≤ 0,25, indépendance par fenêtre et par observateur |
| défauts locaux | part z = +0,52 ; débuts z = +0,24 ; longueur moyenne 2,006 |
| paires (1/7 par jour) | couverture exacte z = −0,96 et −0,25 au repli ; paires uniformes, χ² = 3,23 (5 ddl) et 2,22 (2 ddl) |
| artefacts (1/20 par jour) | masques identiques pour O1 à O3 sur les 7 hôtes AS13335, rien ailleurs ; couverture z = +1,53 |
| régionales (π = 1/5) | z = +1,06, −0,69 (π/2), +0,40 (3π/14), +1,40 (π², hôtes indépendants) ; sous-ensembles χ² = 12,58 (13 ddl) |
| manques β | \|z\| ≤ 1,44 |
| chemins ε | z = −0,65 et +0,22 ; ε = 0 en stress donne 0 fenêtre |
| perte | instant z = +0,06 ; jours χ² = 5,86 (6 ddl) |

Quatre écarts du premier passage, entre 2 et 2,8 erreurs-types, disparaissent sur des cellules neuves avec plus de réplications :
- absences : P(absent en t) aux cinq instants testés, N = 20 000, \|z\| ≤ 0,56 ;
- chemins O2 et O3 ensemble : z = +0,56 ;
- observateur perdu : χ² = 1,58 et 1,67 sur 20 000 ;
- longueurs des défauts locaux : χ² = 0,80 sur 197 450 épisodes.

**4. Identité bit à bit** (Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242, aléatoire)

| sonde | état | empreinte | résultat |
|---|---|---|---|
| tranche 2, worker | SB-4I | 8d97a9dc… | 16 sur 16 |
| tranche 2, réviseur de T2 | SB-4I | d3ba1eb6… | 16 sur 16 |
| les deux précédentes | SB-8C | inchangées | 2 sur 2 chacune |
| tranche 3, worker | SB-8C | 42e935b0… | 16 sur 16, égale sur SB-8B |
| ma sonde propre (repli, perte, manques, régionales, artefacts, unité faible d'écart, R = 9 999 avec S) | SB-8C | a7cf3bab… | 16 sur 16, égale sur SB-8B |

Mode strict `-X dev -W error` : 119 tests OK, 8 fois sur 8.

**Stabilité de SB-4I** (ma sonde `sonde_4i.py` : calme et stress présents, 5 760 fenêtres, 7 genres de dérive, 3 réplications)
- **Pool à rebours** : 0 fenêtre différente, pour tous les genres.
- **Pool réduit** (sans coinbase, okx ou chainlink) : 0 fenêtre de calme différente ; dérives des autres hôtes identiques ; panne initiale gardée, ou absente si l'hôte tiré est retiré.
- **Sans binance** (l'unité non décalée) : l'hôte de la panne initiale change, soit 21 445 fenêtres de calme différentes. C'est la limite déclarée en Q-T3-1.
- **En stress, toute réduction change l'état de tous les hôtes, même sans dérive** : de 745 à 10 862 fenêtres selon la variante. Les comptes sont identiques sur t2, l'effet est donc antérieur à SB-4I : voir O-1.
- **Sur t2, avant SB-4I** : différences en calme sous « tendances », « sauts » et « initiale ». O-A est donc confirmé, puis corrigé par SB-4I.

**5. Rouge, vert et mutants**

*Rouge puis vert, rejoués sur cinq pas*

| pas | rouge rejoué | vert |
|---|---|---|
| SB-4I | tests sur le `sources.py` de t2 : 3 FAIL, 0 ERROR | 94 |
| SB-6A | sur l'ébauche du worker : 4 FAIL, 0 ERROR | 98 |
| SB-7A | sur l'ébauche du worker : 3 FAIL, 0 ERROR | 108 |
| SB-8B | sur l'ébauche du worker : 2 FAIL, 0 ERROR | 117 |
| SB-8C | sur le `regle.py` de SB-8B : 22 FAIL et 1 ERROR (attribut `STRATES` absent) | 119 |

*Campagnes, classées par la commande du job* (runner d'abord, puis la ligne de `gates.yml` ; borne 300 s par étape ; chaque fichier muté compilé avant ; témoin vert)
- **Mes 28 mutants V-01 à V-28** : 24 tués, 4 vivants (V-02, V-20, V-22, V-25), 0 FATAL. Ils comprennent le mutant de spécification « C1 contre K_crit » (V-18, tué) et trois mutants de la garde `ast` sur les modules neufs (V-26 à V-28, tués).
- **Échantillon de 32 mutants du worker**, définitions versées chargées telles quelles : 31 tués, R-28 vivant (déclaré), 0 FATAL.

**6. CI** : aucune gate affaiblie.
- `gates.yml` ne change que le plancher, de 93 à 119 ; `--aucun-saut --egal` et l'étape du runner sont gardés.
- Suite s2bis : 114 OK. Suite s2-harness : 405 OK (skipped=2, sauts nommant la variable). Toutes deux sous `unshare -n`, lo allumée par `isole.sh` (ebaa1c78…).
- Cas des hooks 54/54, de l'épinglage des modèles 95/95, des secrets 147/147.
- `gate-secrets --tree` dans un dépôt jetable : OK, 20 fichiers dans la portée.

**7. Règles et vérification**
- **R-13** : motif lu dans `gates.yml`, aucun constat sur 19 fichiers ni dans les lignes ajoutées.
- **R-8** : bibliothèque standard et modules du lot seuls.
- **Octets 92** : 0 dans le lot et dans les diffs.
- **Garde `ast`** : les quatre gardes rendent [] sur `observateurs.py`, `regle.py` et `sources.py`, que le moteur couvre.
- **`cargo --locked xtask verify`** (unshare -n, sur la série et sur la tête témoin) : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation. Une seule mention de `17-modele-de-menace.md:70`, section S-G9 identique sur le témoin.

## Corrections demandées (liste fermée)

**C-1 — E-S-29 : `regle.oracle()` doit couvrir C_S quand S est suivie.**
- Aujourd'hui, il ne compare que la valeur et les causes.
- Preuve (`sorties/oracle_cs.txt`) : un arrêt simulé sans la condition sur C_S donne C_S = 6 en mode anticipé et 207 en mode complet, à R = 999, valeur égale ; `oracle()` passe.
- Attendu :
  - avec S suivie, refus REGLE/oracle si `C_S ≤ seuil` diffère entre les deux modes ;
  - un cas rouge montré avant le code (`mock` sur le C_S de `complet`, prototype dans `outils/proto_corrections.py`) ;
  - T-REG-2 étendu à des instances où S est suivie.

**C-2 — Trous de tests : un cas écrit à la main par mutant vivant, rouge sous le mutant, vert sur le code.** Prototypes vérifiés dans `sorties/proto_corrections.txt` : verts sur le code livré, chacun rouge sous son mutant.
- **(a) E-S-21 et E-S-22, tue V-02 et V-25.** Artefacts de O1 à O3 sur un hôte AS13335 en fenêtres 1 et 2 :
  - à M_j = 4, D = {1, 2} et ok = {0, 3} ;
  - au repli, même résultat ;
  - par `Couche.consolidation`, D sur les seuls hôtes AS13335.
- **(b) E-S-28, tue V-22.** `tester` avec une seule série non nulle parmi trois : unites = 1 et cause « unites ».
- **(c) E-S-17, tue V-20.** La loi des absences de `parametres.json` est effectivement tirée : longueurs entières observées = {5, 180, 4 320}.

**C-3 — Rapport, E-1.**
- Le décompte des octets 92 des outils omet 20 octets : `mutants_6b.py` 10, `mutants_6c.py` 2, `mutants_7b.py` 4, `mutants_8a.py` 4.
- Ce sont des échappements `\"` voulus et fonctionnels (M-6C-08, rejoué, est tué), mais l'affirmation « tous les chiffres recomptés » est à corriger.

## Observations (non bloquantes ; limites rendues pour être formées)
- **O-1** : en stress, la loi regroupée somme les histogrammes sur le pool opérationnel (`sources.loi_longueurs` l.151). Retirer un hôte change donc l'état en stress de tous les autres.
  - C'est antérieur à SB-4I et hors de la lettre d'O-A. Le test de SB-4I, comme la mesure du contre-contrôle de T2, n'a que du calme.
  - Item à former avant E0 : ancrer cette loi sur le pool opérationnel ou sur la liste scellée de calibration (un retrait avant le sceau fait rejouer SIM-BIS, ADR l.175).
- **O-2** : Q-T3-1 est confirmée et chiffrée par ma sonde.
- **O-3** : la panne initiale est tirée hors du premier hôte du pool, avant les retraits. Si D1-bis retire binance d'une strate, l'unité non décalée de cette strate peut la porter, ce qui contredit E-S-13 (c). À trancher avec Q-T3-15.
- **O-4** : le schéma n'impose à `observateurs.ue` et `repli` que d'être des entiers naturels. Une valeur ≥ M est ignorée sans refus. Un refus nommé est à ajouter avant E0.
- **O-5** : la grille de la couche d'observateurs (Q-S-11 modifiée par l'AVIS : 0,5 %, 2 %, point large 5 %, paires par mois et par semaine, perte) n'est pas encore dans `parametres.json`. Elle est à écrire avec les cellules de SB-11, avant E0.
- **O-6** : l'hôte est partagé ; j'ai vu tourner le `campagne.py` d'un autre lot. Une recherche de processus par motif (`pgrep -f`) peut viser un processus étranger : consigner le PID réel et lire `/proc/PID/cmdline`.

## Écarts E-1 à E-9 du worker
- **E-1** : accepté, sous C-3. Le lot et les diffs n'ont aucun octet 92, vérifié.
- **E-2** : accepté. J'ai eu le même cas de PID (3450 et 3452 contre 3454 et 3455).
- **E-3** : accepté ; voir O-6.
- **E-4** : accepté ; rien n'a tourné, rien n'est compté.
- **E-5** : accepté. Chemin et sha256 cités (55e3e4e5…, l.81 = O-A) vérifiés, et les dix états rejoués verts par moi.
- **E-6** : accepté tel que déclaré, sans exposition à une pièce D.2 au vu de ce qui en a été extrait.
  - Un journal de session ne contient que ce que l'agent a lui-même lu ou produit sous son brief, et il atteste n'avoir ouvert aucune pièce D.2.
  - Il n'en a extrait que ses propres contextes « Q-T3- ». Les meta.json ne portent que des descriptions de tâches.
  - La commande exacte n'est pas versée au journal : rien ne permet de vérifier qu'elle s'est bornée à son propre fichier. À verser ou à attester.
  - La lettre de l'interdit est enfreinte, et lire les meta.json d'autres agents sort du brief. Item à former : après un compactage, reprendre depuis un fichier de notes tenu dans le scratchpad, jamais depuis le .jsonl.
- **E-7** : accepté. Le `find` sur la copie n'a lu que des noms, et les dossiers interdits étaient absents. Rappel : borner aux dossiers du lot.
- **E-8** : accepté. Rouge remontré ; je le rejoue (22 FAIL et 1 ERROR, puis vert).
- **E-9** : accepté. Le pouvoir de détection est montré par les mutants ; M-8C-01 et M-7A-01, rejoués, sont tués.

## Items P-1 à P-9

| item | avis | déclencheur |
|---|---|---|
| P-1 | à former, en y joignant O-1 et O-3 | tout retrait du pool avant le sceau |
| P-2 | à former | adjudication des Q-T3, avant E0 |
| P-3 | à former | G2 de SB-11 |
| P-4 | à rattacher à SHOGEN-SIM-BIS-INDICES-IDENTIFIANTS-1 (B.64) plutôt qu'à un item neuf | gel des identifiants |
| P-5 | à former | brief de SB-13 |
| P-6 | à former ; tenu aujourd'hui à R = 9 999 (99) et R = 999 (9) | SB-13 |
| P-7 | à former : SB-8C se rejoue si la G2 de RB-6 change le contrat | verdict de la G2 de RB-6 |
| P-8 | pas d'item neuf : la limite de R-28 couvre déjà tout le moteur | — |
| P-9 | à former : T-DET-1 de SB-11 doit exercer un retrait | SB-11 |

## Questions Q-T3 (fidélité seulement)
Les seize questions décrivent fidèlement le code et portent chacune sur une valeur que le G0 ne fixe pas. Je n'ai trouvé aucun choix silencieux, hors O-1 (antérieur à la tranche) et O-3 (croisement de Q-T3-1 et Q-T3-15).

## Mes écarts
1. Un `du -sh` sur ma copie filtrée du dépôt : taille seule, dossiers exclus absents.
2. Barres obliques inverses tapées dans cinq cas. Résultats recoupés autrement ou contrôlés sur les octets :
   - un `grep` sur une sortie `od`, sans usage ;
   - un `"\n"` dans un heredoc qui éditait `mc_observateurs.py` (fichier contrôlé, 0 octet 92) ;
   - un `r"\s"` dans le contrôle R-13 (recoupé par le motif lu dans `gates.yml` : 0) ;
   - un `tr` de lecture de `/proc/PID/environ` ;
   - une continuation de ligne dans `outils/xtask.sh` : 1 octet voulu, effet vérifié sur l'environnement du processus cargo.
3. Exécutions invalides refaites, jamais comptées :
   - premier Monte Carlo arrêté par un formatage ;
   - seconde partie des oracles arrêtée sur mon propre contrôle (R = 1 invalide), puis rejouée entière ;
   - syntaxe de `bc` ;
   - arbre léger sans `window.py`, rouge et vert rejoués entiers.
4. Lu `BRIEF-AVIS-SIM-T3.md` (présent dans mon dossier). `AVIS-SIM-T2.md` non ouvert (sha256 seul).

## Journal G1
**[lu]** :
- mon brief ; BRIEF-SIM-T3 (eaeb1937…) ; rapport du worker ; G0 (d9cffc0a…), PROPOSITION (0e78afab…) et AVIS (aaf70a4f…) en entier ;
- ADR-0029 (b908842d…) l.78, 81, 90-98, 139, 164, 168-175, 196-205, 212 ;
- G2 de T2 (4633f17a…) et contre-contrôle (55e3e4e5…) ; SHA256SUMS de revue-t2, égaux ;
- diffs RB-6a (15de17a0…) et RB-6b (89e4c806…), d'où ROTATION-S2BIS.md et rotation.py ;
- code final et tests de la série ;
- outils et journal du worker cités ; outils du réviseur de T2 (identite.sh, ordre_derives.py, xtask.sh) ; isole.sh et lo_up.py (b532be4b…) ;
- verdict-suite-s2.py l.1-80 ; gate-secrets.sh l.1-40 ; `gates.yml` l.215-242 et ligne R-13.

**[abs]** :
- texte des deux ajouts au brief du worker (décrits seulement dans son rapport) ;
- AVIS-SIM-T3 (pas encore rendu) ; AVIS-SIM-T2 ;
- G2 de RB-6 ;
- contenus de l'E-6 (non ouverts).

**[2nd]** : la garantie de stabilité de `random()` d'une version de Python à l'autre (E-S-42), recoupée ici par les sondes, 16 fois sur 16.

**Exposition** : aucune pièce D.2, aucun `*.jsonl`, aucun dossier exclu. SHOGEN_S2_CAMPAGNE_CONTROL jamais posée (`env -u` partout). Aucune recherche récursive sur docs/, sur le dépôt ou sur le scratchpad.

**Commandes et sorties** : toutes dans `rev/sorties/`.
- `serie.txt`, `tailles.txt`, `etapes.txt`, `job-*.txt` ;
- `vecteurs_rb6_bc.txt`, `vecteurs_trot1.txt` ;
- `oracles-1.txt`, `oracles-2.txt`, `cas_main.txt`, `oracle_cs.txt` ;
- `mc_*.txt`, `sonde_4i.txt`, `identite-A.txt`, `identite-B.txt`, `strict.txt` ;
- `rouge_vert.txt`, `rv-*.txt`, `mutants-rev.txt`, `mutants-rev2.txt`, `mutants-worker-echantillon.txt` ;
- `portes.txt`, `xtask-verdicts.txt`, `proto_corrections.txt`.

Tous les chiffres de ce rapport sont recomptés par mes propres commandes.
