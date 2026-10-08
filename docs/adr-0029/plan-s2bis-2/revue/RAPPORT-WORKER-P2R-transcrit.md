# Rapport du worker — lot PLAN-S2BIS-2, sous-lots P2R-0 à P2R-5 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 18:29:25 UTC du rapport rendu par message par le worker (agent a29a7540445f89261) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`). Reçu pendant la pause demandée par l'investisseur : transcrit seulement, G2 neuve et adjudications à la reprise.

**Gate 0 : modèle résolu `claude-opus-5-5`** (worker `shogen-worker`, effort max). Horloge (`date -u`) : début 17:10:19, fin 18:26:26 UTC, le 2026-10-05.

# Rapport du worker : lot PLAN-S2BIS-2, sous-lots P2R-0 à P2R-5

## 1. Résumé

1. **Livré.** Le lot complet se trouve sous `scripts/plan-s2bis-2/`. Ce sont les 13 fichiers du §1 du périmètre, et rien d'autre.
   - Il y a **9 diffs en série**, chacun de **200 lignes ajoutées au plus**.
   - La règle de coupe du §1 est appliquée et déclarée trois fois :
     - P2R-0 faisait +335 lignes à l'écriture : coupé en 0a et 0b ;
     - P2R-1 a été coupé d'emblée en 1a (socle II) et 1b (masque) ;
     - P2R-4 faisait +234 lignes à l'écriture : coupé en 4a et 4b.
   - Le lot n'a jamais été écrit dans le dépôt. `git status` y est vide à 18:26.
2. **Tests.** 28 tests, verts à chaque diff (2, 6, 7, 11, 14, 18, 20, 23, puis 28), sous python3.11, 3.12 et 3.13 avec `-X dev -W error`, sans aucune ligne d'avertissement. La suite tourne isolée du réseau (`unshare -n`, `lo` allumée), avec un `TMPDIR` dédié.
   - Un rouge d'assertion a été montré avant chaque code : 8 journaux, 0 erreur.
   - Exceptions déclarées en E-2 : quelques tests ont été écrits après leur code.
3. **Mutants : 71, tous tués sur l'état final.**
   - Ce sont les 36 du §2 (M-P2-01 à 08, 10, 13 à 16, 18 à 30, 32 à 41) et 35 neufs (au moins 2 par sous-lot).
   - 70 sont tués par leur test nommé. M-P2R0-5 est tué au chargement de `tests/__init__`.
   - Aucun vivant, aucun FATAL. Les témoins sont verts au début et à la fin, et la restauration est contrôlée par sha256.
   - Les campagnes ont aussi été lancées diff par diff.
4. **Identité T-P2-DET-1.** Les sha256 des trois sorties sont égaux sous 3.11, 3.12 et 3.13, avec les graines 0 et 1.
   - Empreintes, pour la fixture de MAS-1 (préfixes) : `fiv_unites` 6c22291d…, `intervalles` 7bea20d8…, `masque_j28` 66ec2d1f…
   - **3.10 est impossible** (Q-P2R-1, mesuré) : le `commun.py` épinglé appelle `hashlib.file_digest`, qui n'existe qu'à partir de 3.11.
5. **Mesure à l'échelle, scripts seuls.** Journaux synthétiques de 38 569 fenêtres (95 Mo). Le lanceur n'a pas été lancé : le brief l'interdit (voir l'item sur E-P2-20).
   - `masque_fiv` prend 27 à 30 s et `intervalles` 20 s ; mémoire maximale 909 Mo ; A = B à l'échelle.
   - Sur la portée réelle, le masque donne 46 468 positions, D5 de j = 41718 à 44408 (2 691 positions), calendrier hors D5 de 30 286 et 13 491 positions : ces valeurs égalent celles de PROPOSITION §2.2.
   - Une passe dure donc environ 50 s ; le lancement entier environ 2 min.
6. **Autres suites et gates.**
   - Suite de PLAN-S2BIS : 37 tests OK.
   - s2-harness (`verdict-suite-s2.py --egal`) : 406 tests, OK (2 sauts), « conforme ».
   - Gate des secrets (`--tree` et index, dans un dépôt jetable) : OK sur 13 fichiers.
   - `cargo --locked xtask verify` : S-G1 à S-G8 VERT ; S-G9 ROUGE, 1 violation, `docs/17:70` (connue) ; fmt, no_std et clippy VERT.
   - La suite sim-bis n'a pas été rejouée (voir E-P2-28).
7. **Interdits respectés.**
   - Aucun journal réel lu, listé ni haché ; aucun `*.jsonl` réel ; aucune pièce de D.2.
   - Rien d'ouvert dans les dossiers exclus.
   - `lancer.sh` lancé dans les seuls tests, avec de faux scripts.
   - `SHOGEN_S2_CAMPAGNE_CONTROL` posée seulement par l'exception A-3 / E-P2-05 exigée par T-P2-LAN-6 : valeur fictive, dans le seul sous-processus du lanceur.
   - `f35a70c` extrait par `git archive` avec les 7 exclusions. L'absence de `docs/adr-0028/execution` et des 6 autres dossiers exclus a été vérifiée chemin par chemin (`test -e`), dans la copie comme dans l'extraction.
8. **Base.** 12ce67f relevée au début. La tête du dépôt est passée à 47b2177 pendant la passe : 3 commits COLLECTE-BIS du runner. `git diff --quiet 12ce67f HEAD` sur tout mon périmètre sort 0, et P2R-0a s'applique sur la tête (`git apply --check`).
9. **Épingle avant la G2** : sha256 de `scripts/plan-s2bis-2/SHA256SUMS` = `a8bb826d2c8dc67f14aca13a722345ff974d72b876b7fe1c103db5a1aab40e08`. Elle change si la G2 corrige.

## 2. Diffs

Les diffs sont dans `<scratchpad>/s2bis/plan2/code/diffs/`, à appliquer dans l'ordre (`git apply`).
- Appliqués en série sur une copie neuve de 12ce67f, ils reconstruisent l'instantané final octet pour octet (`diff -r`). Hors du dossier du lot, rien ne diffère.
- Les diffs ne contiennent aucun octet 92, aucune tabulation ni aucun retour chariot. Tous les fichiers sont en mode 100644.

| diff | contenu | +/− | tests | mutants | sha256 |
|---|---|---|---|---|---|
| P2R-0a | `parametres.json` ; socle : Refus, garde, schéma, `lire` ; `tests/__init__` minimal ; SOC-2, SOC-5 | +176 | 2 | 5/5 | e3d7ab9a…2223 |
| P2R-0b | socle : `piece`, `charger_module`, `charger`, (c), (d) ; SOC-1, SOC-3, SOC-4, POOL-1 | +166 | 6 | 14/14 | c9bf9b3b…7d96 |
| P2R-1a | socle II : `executer`, `provenance`, ETIQUETTE ; banc de fixtures ; SOC-6 étendu | +129 | 7 | 8/8 | 6dc6e591…0d01 |
| P2R-1b | `masque_fiv` I : portée, masque, (b), sortie ; MAS-1 à 3, OUT-1 | +200 | 11 | 10/10 | d8210e5d…835b |
| P2R-2 | `masque_fiv` II : D_u, (f), FIV_u, sensibilité au voisinage ; FIV-5, FIV-6, VOI-1 | +152 −11 | 14 | 7/7 | 68fc6498…e772 |
| P2R-3 | `intervalles.py` ; EPI-1 à 3, INT-1, INT-2 | +169 | 18 | 8/8 | cbedaf09…f642 |
| P2R-4a | lanceur I : usage, variable, journaux, sortie, épingle, `parametres.json` de PS2 ; LAN-3, LAN-6 (début) | +171 | 20 | 6/6 | 210948c1…cc8d |
| P2R-4b | lanceur I : paquet, bloc, journaux, commit, extraction déjà présente ; LAN-4, LAN-5, LAN-6 (fin) | +83 | 23 | 15/15 | dcbea54c…3b8f |
| P2R-5 | lanceur II : 7 épingles, extraction (+ `execution`), passes A et B ; LAN-1, 2, 7, 8, 9 ; DET-1 ; README ; SHA256SUMS | +196 −6 | 28 | 9/9 | 00b64986…5237 |

- Total : 1 425 lignes nettes (1 413 lignes de code et de tests, plus les 12 de SHA256SUMS).
- Les lanceurs intermédiaires (4a, 4b) finissent par « REFUS P2/usage : lanceur incomplet », code 5. Aucun état commis avant P2R-5 ne peut donc sortir en succès.
- **sha256 des fichiers** (SHA256SUMS du lot) :
  - `README.md` ccbe488b… ; `intervalles.py` a684d113… ; `lancer.sh` 61c54ac8… ; `masque_fiv.py` 7845d5ed… ; `parametres.json` 7a6a7112… ; `socle.py` 130c21aa…
  - `tests/__init__.py` 834e6661… ; `tests/test_identite.py` a14a4ea8… ; `tests/test_intervalles.py` 031d5da3… ; `tests/test_lancer.py` a815c093… ; `tests/test_masque_fiv.py` ef3dfdee… ; `tests/test_socle.py` a432583e…
  - Le fichier complet est dans `code/snap/P2R-5/scripts/plan-s2bis-2/SHA256SUMS`.

## 3. Exigences E-P2 (état du périmètre réduit, et ce qui les fixe)

| E-P2 | où | fixé par |
|---|---|---|
| 01 (modifiée) | 13 fichiers du §1 ; chaque diff ne touche que `scripts/plan-s2bis-2/` | numstat de chaque diff ; chaîne reconstruite (contrôle outillé, pas de test unitaire) |
| 02 (modifiée) | lecture par `commun.charger` et `commun.controle` seuls ; `--harnais` = extraction ; exception écrite au README | LAN-1 (M-P2-38), LAN-2, SOC-6 |
| 03 (précisée) | 8 épingles, au socle et au lanceur | SOC-1, SOC-3, LAN-3, LAN-9 |
| 04 | EP et rendu sous épingle ; rendu lu par `commun.controle` seul | SOC-1, SOC-6 (P2/coherence) |
| 05 | garde sur l'environnement passé ; exception A-3 | SOC-2, SOC-6, LAN-6 |
| 06 (modifiée) | en-tête étendu (P-3, provenance, bloc 3) | OUT-1 (M-P2-19), SOC-6 |
| 07 | `.partiel` puis renommage ; 0 octet 92 ; lignes de 120 caractères au plus ; 0 TODO ou FIXME | OUT-1, M-P2R1-6 ; outil `controle_octets.py` |
| 08 | `masque_j28.txt` dans la forme de PROPOSITION §2.2 | MAS-1, MAS-2 |
| 09 (modifiée) | 340 lignes FIV_u, forme d'EP l.94 (P-6), plus `[SENSIBILITÉ VOISINAGE]` (680 lignes à l'échelle, mesuré) | FIV-6, VOI-1 |
| 10 (précisée) | 40 entrées ; pauses complètes imprimées en premier | EPI-1, EPI-2, EPI-3, INT-1, INT-2 |
| 11 (modifiée) | (a) à (f) ; (f) serré par n et K (P-5) | (a) SOC-6 ; (b) MAS-3 ; (c) POOL-1 ; (d) SOC-4 ; (e) EPI-2 ; (f) FIV-5 (M-P2-32 tué) |
| 12 | refus nommé, sans valeur | MAS-3, FIV-5, EPI-2 : une ligne REFUS, aucune section de valeurs |
| 13 (modifiée) | voisinage pré-déclaré, d = 1, bords comptés | VOI-1 (M-P2-33) |
| 14 | aucune autre sortie | par construction ; à relire en G2 |
| 15 (modifiée) | chaînes de r1 (`commun.dec`), `resume` | FIV-6, INT-2 |
| 16, 17 | déterminisme, identité 3.11 à 3.13 | DET-1 (M-P2-20) ; A = B à l'échelle |
| 18 (modifiée) | lettre de Q-P2-08 | LAN-1, LAN-7 (P-7), LAN-8 (P-8) ; README |
| 19 (modifiée) | refus du §4 | table du §4 ci-dessous |
| 20 | répétition à l'échelle | **partielle** : scripts seuls ; lanceur non lancé (brief) → item |
| 21 (précisée) | épingle passée en argument | LAN-3 ; inscription au JOURNAL : orchestrateur |
| 22, 23 | lancement détaché ; écran fait de noms, codes et sha256 ; relance = déviation | LAN-1 (écran) ; README |
| 24, 25 | versement, exposition | orchestrateur |
| 26 (modifiée) | tests d'abord ; références indépendantes (à la main, `printf \| sha256sum`, `date -u`, `episodes.py` épinglé, calc_p2 et SB-10B) | journaux rouges ; chaque test nomme sa mutation |
| 27 | mutants classés par la sortie | `outils/mutants.py` (0 vivant, 1 tué, sinon FATAL ; compilation contrôlée) |
| 28 (modifiée) | suites | voir le détail sous la table |
| 29 | tombe | — |

Détail de E-P2-28 :
- Le lot est vert à chaque diff ; la suite de PLAN-S2BIS donne 37 tests OK et s2-harness 406.
- **La suite sim-bis n'a pas été rejouée** : `oracle_r1` exige l'historique git, et la copie produite par `git archive` n'en a pas. Elle est inchangée par construction : seul le dossier du lot diffère.

## 4. Refus du §4

| code | où | test |
|---|---|---|
| P2/usage | lanceur | LAN-6, `test_variable_journaux_sortie_usage` |
| P2/variable | lanceur ; `socle.garde` | SOC-2, SOC-6, LAN-6 |
| P2/sortie | lanceur : sortie non vide ; extraction déjà présente | LAN-6 (début), `test_commit_extraction` |
| P2/epingle | lanceur | LAN-3, `test_epingle` |
| P2/plan-s2bis | `socle.piece`, `charger_module`, `charger` ; lanceur | SOC-1 (y compris « module chargé hors de son chemin »), LAN-3, LAN-9 |
| P2/paquet | lanceur | LAN-4 |
| P2/journal | lanceur : dossier absent, journal absent, sha256 différent, ligne malformée, journal non nommé au bloc | LAN-5, LAN-6 |
| P2/commit | lanceur | `test_commit_extraction` |
| P2/harnais, P2/coherence | `socle.executer` | SOC-6, `test_executer_refus` |
| P2/parametres | `socle.lire` | SOC-5 |
| P2/masque | `masque_fiv.controle_b` | MAS-3 |
| P2/pool | `socle.controle_c` | POOL-1, SOC-6 |
| P2/ecarts | `socle.controle_d` | SOC-4, SOC-6 |
| P2/ep | (f) dans `masque_fiv.fiv` ; (e) dans `intervalles.analyse` | FIV-5, EPI-2 |
| P2/identite | lanceur | LAN-8 |
| code 4 ; code 5 (script en échec) | lanceur | LAN-7 |

## 5. Questions Q-P2R (périmètre muet, ou en contradiction avec le code) : mon choix et sa raison

- **Q-P2R-1 : Python 3.10.** Le brief le demande, mais le `commun.py` épinglé ne tourne pas sous 3.10.
  - Mesuré : sous 3.10, `tests` échoue à l'import (AttributeError) et les scripts sortent en code 1 sans sortie.
  - Choix : identité et `-X dev` sous 3.11 à 3.13 (T-P2-DET-1 et E-P2-17 nomment ces versions). Je n'ai ni modifié PLAN-S2BIS ni rien rapiécé.
- **Q-P2R-2 : `--parametres` désigne le `parametres.json` du lot**, racine de toutes les épingles ; le `parametres.json` de PLAN-S2BIS est atteint par son épingle.
  - Les chemins des pièces sont relatifs à la racine du dépôt.
  - Une fixture peut épingler un chemin absolu (règle de `os.path.join`) ; cela n'arrive que dans les tests.
- **Q-P2R-3 : refus précoce.** La sortie porte l'en-tête déjà calculé, puis la ligne REFUS.
  - Les ValueError de `commun.charger` n'ont pas de code au §4 : strates journalisées incohérentes, classe divergente, segment.
  - Elles terminent donc le script sans sortie (code 1, échec fermé). À adjuger : faut-il leur donner un refus nommé ?
- **Q-P2R-4 : `pauses complètes = p` en premier** (AV l.39). Le compte des épisodes complets vient de `episodes.resume`.
- **Q-P2R-5 : MAS-3.** Au script, « retenues différentes du n du bloc 3 » est pris d'abord par (a), car le n de `compute_r1` égale le nombre de fenêtres retenues. Le contrôle (b) est donc éprouvé sur la fonction, et au script par « sautées attendues fausses ».
- **Q-P2R-6 : forme des lignes FIV_u.** `« st » f (hôte h) ℓ = … : n = … ; K = … ; FIV_série = … ; σ̂²_bloc = … ; γ̂₀ = … ; cv théorique = … ; garde : …`
- **Q-P2R-7 : rattachement de trois refus.**
  - P2/journal couvre aussi « dossier des journaux absent » et « control.jsonl ou journal.jsonl non nommé au bloc ».
  - P2/sortie couvre « extraction déjà présente ».
  - P2/plan-s2bis couvre « commit malformé ».
- **Q-P2R-8 : texte de la ligne « contrôle » de (b).** Repris mot pour mot de PROPOSITION §2.2. Le contrôle vérifie en plus le calendrier hors D5, l'absence de position D5 retenue et l'absence de retenue hors grille.
- **Q-P2R-9 : clés des comptes du masque.** Elles sont libres au schéma et comparées aux strates de PLAN-S2BIS dans (b). Aucun nom de strate n'est écrit dans le code.
- **Q-P2R-10 : lanceurs intermédiaires** (4a, 4b) : refus final « lanceur incomplet », code 5.
- **Q-P2R-11 : forme de la section `[SENSIBILITÉ VOISINAGE]`.** Elle est de mon choix : une ligne par strate (positions retirées, n′, K − K′ par hôte), puis les lignes des séries réduites ; la règle généralise d (distance au plus d).
- **Q-P2R-12 : E-P2-20.** Le lanceur n'a pas été lancé (interdit du brief) ; seuls les scripts ont été mesurés.

## 6. Écarts

- **E-1.** Un `git status --short` a été lancé sans `--no-optional-locks` à 17:10 ; il a pu rafraîchir l'index, sans changer de contenu. Ensuite, `--no-optional-locks` partout.
- **E-2. Tests écrits après leur code.** Leur pouvoir de détection est montré par les mutants nommés.
  - OUT-1 porte sur l'en-tête de P2R-1a (M-P2-19) ; DET-1 sur les scripts de P2R-1 à 3 (M-P2-20).
  - Les 3 cas ajoutés à SOC-6 ont leur rouge montré contre un executer naïf (`P2R-1a-rouge-etendu.txt`) ; mutants M-P2R1-3 à 5.
  - Les 2 cas de couverture ajoutés à 18:13 : M-P2R0-8 et M-P2R4-8.
- **E-3. Avertissement masqué.** Sous `-W error`, un ResourceWarning est sorti en « Exception ignored » et la suite est restée à 0. Je l'ai vu et corrigé ; mon critère de vert exige désormais 0 ligne de ce type, et les instantanés antérieurs ont été revérifiés : 0.
- **E-4. Barres obliques inverses tapées dans des commandes et des outils hors lot** : une continuation dans `suite.sh` (retirée), un `\n` dans le `printf` de `outils/vert.sh` (1 octet, laissé), des guillemets échappés dans des heredocs, un `grep "D\.2"`, et la première version de `mutants_P2R-4.py` (réécrite). Le lot et les diffs ne contiennent aucun octet 92 (compte Python).
- **E-5. Heures écrites dans NOTES avant la lecture de l'horloge** (P2R-1a, 1b, 2). Corrigées depuis `date -u` et l'heure des fichiers.
- **E-6. Annexe D.**
  - J'ai listé un niveau de `docs/adr-0028` (noms) ; `execution` et `monark-m009a` étaient dans le flux de `git ls-tree` et ont été filtrés avant affichage.
  - J'ai lu l'annexe D, l.32-48 (liste D.2, noms seuls).
- **E-7.** La tête du dépôt a avancé pendant la passe (voir §1, point 8).
- **E-8. Dépôts git jetables** pour les tests du lanceur, le suivi des diffs et la gate des secrets : `init`, `add`, `write-tree`, aucun commit.
- **E-9. `*.jsonl` synthétiques.**
  - Écrits sous mon `TMPDIR`.
  - Une fixture restante (`tmp/p2_banc_88bl3oc3`, 17:52:29) venait d'un script de débogage coupé par `head`.
  - Tout est retiré.
- **E-10. Sortie de xtask.** J'ai affiché le bloc de notes de S-G9, et pas seulement les lignes de verdict, pour confirmer `docs/17:70` (renvoi vers `docs/rapports/`, exclu de la copie).
- **E-11. Opérations récursives sur mes propres copies du dépôt**, d'où les dossiers interdits sont absents : `du -sh` (tailles), `cp -a` ou `copytree`, `diff -rq` (seul le dossier du lot y diffère).
- **E-12. PID de la campagne finale.** `setsid` a fourché ; le PID réel, 25086, a été relevé par une liste `ps` filtrée sur la ligne de commande exacte (25084 était l'enveloppe).
  - Autres PID : campagne v1 19524 ; cargo 28901 ; mesure à l'échelle 30727 (`timeout` 30726).

## 7. Items à former (règle PAROXYSME)

- **SHOGEN-PLAN-S2BIS-2-PY310-1** (neuf). Constat : Q-P2R-1. Construction : retirer 3.10 des briefs des lots qui réemploient PLAN-S2BIS, ou écrire la limite. Prix : nul. Déclencheur : prochain brief.
- **SHOGEN-WORKER-WERROR-IGNORE-1** (neuf). Constat : E-3. Construction : critère de vert = code 0 et aucune ligne « Exception ignored » ou « Warning ». Prix : une ligne de fiche.
- **SHOGEN-PLAN-S2BIS-2-REPETITION-1** (neuf). Constat : E-P2-20 demande le lanceur entier, avec l'extraction réelle de `f35a70c`, et le brief l'interdit au worker. Construction : décider qui le lance, et comment (dépôt jetable portant `f35a70c`), avant l'épinglage. Prix : environ 10 min.
- **SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1** (neuf). Constat : Q-P2R-3.
- **SHOGEN-S2BIS-P1-ESTIMATION-1** (précisé) : 1 425 lignes mesurées, contre environ 980 au périmètre (× 1,45) ; 9 diffs au lieu de 6.
- **SHOGEN-PLAN-S2BIS-VARIABLE-TEST-1** (précisé) : la règle 3 de la fiche contredit l'exception A-3 exigée par LAN-6. Je l'ai appliquée telle que le G0 l'écrit ; la fiche devrait la nommer.
- **SHOGEN-PLAN-S2BIS-CI-1** (précisé) : la suite sim-bis ne se rejoue pas dans une copie produite par `git archive`.

## 8. Journal G1 (provenance)

**Lu [lu]**, avec le sha256 tronqué de chaque pièce :
- Brief `BRIEF-P2R.md` (16fc3e81…), en entier.
- Dossier `g0-plan2` : `G0-PLAN-S2BIS-2.md` (bc8dba70…), `PERIMETRE-REDUIT.md` (b48989f3…), `AVIS.md` (33ac8d31…) et `PROPOSITION.md` (4b3107a7…), en entier. Le `SHA256SUMS` du dossier passe `sha256sum -c`.
- ADR-0029 (35563d8f…), l.395-403. `G0-SIM-BIS.md` (a216a953…), l.35-92. Annexe D (deb64179…), l.32-48.
- PLAN-S2BIS, en entier : `commun.py`, `episodes.py`, `regles.py`, `parametres.json`, `README.md`, `lancer.sh`, `SHA256SUMS`, `tests/__init__.py`, `tests/fixtures.py`, `test_lancer.py`, `test_episodes.py`, `test_regles.py`, `test_commun.py`. Les 16 sha256 sont égaux au `SHA256SUMS`, et les 8 épingles à celles du §1.
- EP (c0371ca5…), l.1-20, l.88-96, l.125-130 et l.159-161 ; son `SHA256SUMS` (f21f9293…).
- `G1-lot-PLAN-S2BIS.md` (cb9d1be0…), l.1-140. `oracle_r1.py` (84703863…), en entier.
- Harnais extrait de `f35a70c` : `r1.py` (0a16e5de…) l.55-700 par plages ; `window.py` (f8c3b79f…) en entier ; `records.py` (a2e9a774…) l.295-423.
- Scratchpad : `calc_p2.out.txt` (eace3fe5…) l.1-12 ; `SB-10B.diff` (847fae13…) l.140-165 ; `isole.sh` et `lo_up.py`.
- Copie du dépôt : `gates.yml` (f116753c…) l.180-260 ; `gate-secrets.sh` (f89abf0f…) l.1-60 ; `xtask/src/lib.rs` (002e2cdd…) l.56-96.

**Non lus [abs]** :
- Dans `g0-plan2` : `LETTRE-AJOUT-G0-SIM.md`, `CP1-AJOUT*.md` et les briefs.
- Pièces de la tranche 4 (T4, G2-T4, RW-T4) ; `calc_p2.py` ; SB-10A et SB-10C.
- Annexe B ; JOURNAL ; paquet de S2 ; rendu J28.
- Le reste d'EP.
- Les autres fichiers de `sim-bis`.

**Recomptes [calc]** :
- Empreinte de la chaîne de MAS-1 par `printf | sha256sum` : b262f67f…
- Dates des fixtures par `date -u`.
- Calendrier de MAS-2 : calme 300 + 2 880 + 4 × 7 200 + 88 = 32 068 ; stress 5 × 2 880 = 14 400. Plage D5 : 342 + 1 440 = 1 782 positions de calme et 909 de stress.
- Valeurs à la main :
  - FIV-6 : 3/2 ;
  - INT-2 : rangs 2, 4 et 4 ; moyenne 12/4 = 3, contre 42/5 avec les pauses de bord ;
  - VOI-1 : positions retirées {0, 4, 6, 9}, n′ = 5 ;
  - FIV-5 : 5 cellules d'écart contre 4 de panne.

**Attestation, forme D.3** : aucune pièce de D.2 ouverte ; aucun `*.jsonl` réel ; rien des dossiers interdits ; aucune recherche récursive sur `docs/`, sur le dépôt ni sur le scratchpad ; seul `…/plan2/code/` a été écrit. Exposition : valeurs de S2 post-rendu portées par EP l.1-20, l.88-96, l.125-130 et l.159-161 ; aucune donnée de S2-bis n'existe.

## 9. Fichiers (chemins absolus)

Racine : `<scratchpad>/s2bis/plan2/code/`
- `diffs/P2R-{0a,0b,1a,1b,2,3,4a,4b,5}.diff`
- `snap/P2R-5/scripts/plan-s2bis-2/` : état final du lot ; les 9 instantanés sont dans `snap/`.
- `journal/` : journaux rouges, `mutants-*.json`, `mutants-final.json` (71/71), `det1.txt`, `repetition.txt`, `s2-harness-verdict.txt`, `suite-py310.txt`, `xtask-verify.txt`.
- `outils/` : scripts de suite, de mutants, de coupe et de mesure.
- `NOTES.md`
- `SHA256SUMS` du dossier (121 lignes, `sha256sum -c` OK), dont le sha256 est `9c6e4cb26c7542bf4cbc1ae112c14686aafce1bf252d835f45cdd7e5e04bf08c`.

Les copies lourdes ont été retirées : copie, extraction de `f35a70c`, arbres de vérification, `target` de cargo et données d'échelle. Les outils les recréent par les commandes consignées dans NOTES.md, à la section « Mise en place ».
