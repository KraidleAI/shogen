# G1 — lot SIM-NIVEAU d'ADR-0028 (item SHOGEN-SIM-NIVEAU-1 ; sous-lots a1, a2 et b), Shōgen S2 — journal

- **Modèle** : `claude-opus-5-5` (identifiant déclaré par le harnais), effort max, contexte frais ; worker G1 (R-1 déclaré en tête de session). Aucun commit, aucun workflow déclenché (R-20). **Aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree`.** Git en lecture seule sur `F:\Shogen` : `rev-parse`, `status --porcelain`, `show <sha>:<chemin>`, `ls-tree`, `config --get`, `log`, `diff --stat`, `diff --quiet`, et `git -C F:/Shogen archive f5b8269 s2-harness/shogen_s2 | tar -x` vers `F:\tmp` (§0). `git status --porcelain` = `?? .claude/worktrees/` avant et après (préexistant).
- **Horloge** (`date -u`) : voir §1 bis (chronologie complète).
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`), HEAD `f5b8269` : implémenter le G0 `F:\tmp\shogen-lots\SIM-NIVEAU\G0-lot-SIM-NIVEAU.md` (sha256 `4e4dcf13e99c9b7ec394ae24a853fd65203e0e3bfd809600f91764f8ac55f948`, recalculé à 07:39Z, égal à celui de C-1) avec les corrections C-1 à C-9 de son cp-1 (`F:\tmp\cp1-SIM-NIVEAU\CP1-SIM-NIVEAU.md`, sha256 `ece81297a0f16945b15ff58728c7538fd4ba1633f3b043d9c73b02d2b6386303`, recalculé). Cadre : ADR-0028 §1 bis.1 pts 3, 5 et 7, §1 bis.2 ; annexe A l.41 ; CRITIQUE v2 §4.1 et §4.3 ; AVIS-advisor-defi Q1 (v) ; RECONCILIATION-Q2-advisor-defi §3.
- **Classification** : bounded. Scripts hors harnais, bibliothèque standard seule, aucune dépendance nouvelle (R-8 sans objet). Rien d'écrit dans `F:\Shogen` ni sur `C:` : le versement au dépôt est un acte de l'orchestrateur (lot PAQUET).
- **Résultat** : lot livré en trois sous-lots sous le seuil R-25 (a1 148, a2 190, b 74 lignes [mesuré]) ; exécution complète (R = 10⁵, 8 cas, 12 processus) faite deux fois, A et B identiques à l'octet (JSON `d17c5121…350e`, texte `7173a9ce…00eb`) ; (1b) identique entre 1 et 12 processus, 12 PID par cas (C-6) ; (2) et (2b) 100000/100000 dans chaque cas ; (3) 24/24 erreurs-types recalculées ; (4a) 1 363 égalités exactes contre r1 à `f5b8269` ; (4) en attente de B-DEP-1 (ORACLE4-1) ; (5) étendu (C-4) : 24 contrôles, max 2,34 SE ; mutants 10/10. Un défaut de conception de l'oracle (5), constaté par le banc de mutants (E-3), est corrigé avant toute exécution à l'échelle (gel 2). Taux au §6, sans critère (C-6).
- **Répartition des corrections du cp-1** : C-4 et C-6 relèvent du G1 et sont appliquées ici (§3 c, §3 e). C-5 (rédacteur du G0) exige un comportement du script : le G1 en implémente un et le soumet à ratification (§3 b, Q-G1-2). C-3, C-7 et C-8 (rédacteur du G0) et C-1, C-2, C-9 (orchestrateur) ne sont pas exécutées ici ; le G1 fournit leurs entrées mesurées (lignes datées de C-2 au §1, table des mutants de C-4 au §5). Le G0 n'est pas modifié (son sha est cité par C-1).

## 0. Préconditions mesurées avant code

- **Base** : `git rev-parse HEAD` = `f5b82693b8f1a99d6cc2fb53a5e3edd35b4e0a78`.
- **HEAD a avancé pendant le G1**, sans acte de ce worker : `cf696bd` (commit de l'orchestrateur, 2026-09-30T07:41:49Z, `JOURNAL.md` seul, +2 lignes ; contenu non ouvert, seul `git diff --stat` lu). `git diff --quiet f5b8269 HEAD -- s2-harness/shogen_s2/r1.py docs/adr-0028/ADR-0028-decisions-sortie-S2.md` : rc 0 ; blob de r1.py à HEAD = `1d6a908c…` (inchangé). L'oracle (4a) reste épinglé sur `f5b8269`, comme le G0 le prescrit.
- **Interpréteur** : Python 3.14.5 (`C:\Users\KACIMI\AppData\Local\Python\pythoncore-3.14-64\python.exe`, lu, jamais écrit), Windows 10 build 19045 ; 24 processeurs logiques, 12 cœurs (`wmic cpu`). Toutes les commandes : `python -B`, `PYTHONDONTWRITEBYTECODE=1`, `TMP`, `TEMP` et `TMPDIR` sur `F:/tmp/shogen-tests-tmp`.
- **Fins de ligne et règle du sha (G0 §7)** : `.gitattributes` à `f5b8269` porte `* text=auto eol=lf` ; `core.autocrlf=true` (configuration système de Git). Les trois scripts sont écrits en LF (`grep -c $'\r'` = 0 sur chacun) et les sorties en octets UTF-8 (mode `xb`). Le blob commis doit donc être égal, à l'octet, au fichier exécuté ici ; contrôle dû au commit : `git show <C>:scripts/sim/<fichier> | sha256sum`.
- **r1 de référence** : `git -C F:/Shogen archive f5b8269 s2-harness/shogen_s2 | tar -x -C F:/tmp/shogen-lots/SIM-NIVEAU/oracle-r1-f5b8269/` (07:57Z). SHA-1 de blob recalculé sur l'export : `1d6a908cb2872ae261e09f1870bbaba5afca174c` = `git rev-parse f5b8269:s2-harness/shogen_s2/r1.py`. Export restreint au paquet `shogen_s2` (le G0 écrit `s2-harness` ; seul le paquet est importé, les autres fichiers de `s2-harness` ne sont ni exportés ni ouverts). Import sans effet de bord constaté (`records`, `window` : aucune ouverture de fichier au niveau module).
- **Fonction absente** : `block_long_run_variance` n'existe pas dans r1 à `f5b8269` (constaté par l'adaptateur, `hasattr`) : oracle (4) non exécutable, item ORACLE4-1.
- **Chaîne de graine** : `repr(0.02)` = `'0.02'`, donc la chaîne `SHOGEN-SIM-NIVEAU-1|20260930|p={p!r}|L={L}|n={n}|r={r}` rend, à p = 0,02, le littéral du G0 §4 (exemple écrit dans chaque JSON : `SHOGEN-SIM-NIVEAU-1|20260930|p=0.02|L=1|n=10000|r=0`).
- **Arithmétique entière** : `math.sumprod` rend un entier exact sur des entiers (contrôle : `sumprod([10**30, 2], [3, 4])` = 3·10³⁰ + 8).

## 1. Coupe R-25 (C-2)

- **Estimation du G0** : ≈ 200 (script) + 60 (adaptateur) = 260 lignes.
- **Mesure au G1** : le premier fichier unique atteignait 89 lignes au seul générateur et aux répliques de r1 ; la suite (σ̂² en deux formes, réplication, agrégation, sorties, CLI) le portait au-delà de 200. Coupe appliquée selon le G0 §7 (« générateur et statistiques, puis sorties et CLI ») : trois fichiers neufs, `wc -l` (méthode du lot B0) :

| sous-lot | fichier | lignes | contenu | oracles |
|---|---|---|---|---|
| **SIM-NIVEAU-a1** | `scripts/sim/sim_niveau_calc.py` | **148** | graine, chaîne (a, b), générateur, répliques r1 (`poisson_binomial`, `gate_value`, `z_score`), σ̂² en deux formes entières, z_bloc, valeur de la règle, diagnostics, tâche du Pool | (2), (2b) (drapeaux par réplication, exigés par a2) ; (4a) par b |
| **SIM-NIVEAU-a2** | `scripts/sim/sim_niveau.py` | **190** | CLI, Pool ordonné, agrégation, taux et SE, oracle (5) étendu, JSON, texte, journal d'exécution | (1), (1b), (3), (5) |
| **SIM-NIVEAU-b** | `scripts/sim/sim_niveau_oracle_r1.py` | **74** | adaptateur (4a) contre r1 à `f5b8269` ; (4) déclaré en attente | (4a) ; (4) après B-DEP-1 |

- **Lignes datées proposées pour l'annexe A** (acte de l'orchestrateur, C-2 ; non écrit ici) :
  - **SIM-NIVEAU-a1** (2026-09-30, coupe R-25 du G1 de SIM-NIVEAU) : générateur markovien des 11 flux simulés, répliques de r1, σ̂²_bloc (ℓ = 240) en forme par lags et en sommes de blocs, z_bloc, valeur de la règle (§1 bis.1 pt 5). Véhicule : `scripts/sim/sim_niveau_calc.py`. Oracles : (2) et (2b) à chaque réplication ; (4a). Taille 148 [mesuré]. Tuyau : consommé par a2 et b. cp-1 bref.
  - **SIM-NIVEAU-a2** (2026-09-30, même coupe) : exécution ordonnée, agrégation, taux avec erreur-type, oracle (5) étendu (C-4), sorties `sim_niveau.json`, `sim_niveau.txt`, `sim_niveau.log.txt`. Véhicule : `scripts/sim/sim_niveau.py`. Oracles (1), (1b), (3), (5). Taille 190 [mesuré]. Tuyau : générateur → taux de rejet → paquet ; consommateurs §1 bis.1 pt 7 et cp-1 de PAQUET. cp-1 bref.
  - **SIM-NIVEAU-b** (2026-09-30, même coupe) : adaptateur d'oracle contre r1. Véhicule : `scripts/sim/sim_niveau_oracle_r1.py`. Oracle (4a) aujourd'hui ; (4) au commit de B-DEP-1 (ORACLE4-1). Taille 74 [mesuré]. cp-1 bref.
- **Ordre de commit** : a1, puis a2 (qui importe a1), puis b (qui importe a1 et a2). a1 seul est une bibliothèque sans pilote : ses oracles ne s'exécutent que par a2. Remplacer « ≈ 120 » (annexe A l.41, annexe B l.104) par « 148 + 190 + 74 = 412 [mesuré] » relève de l'orchestrateur (C-2).

## 1 bis. Chronologie (`date -u`, 2026-09-30)

- 07:39:25Z : début ; orientation (G0, cp-1, ADR §1 bis, annexes, consultations, r1 à `f5b8269`, format du G1 de B0).
- Avant toute écriture : **consultation de l'outil advisor intégré** (canal 1, R-26) sur l'approche ; avis suivi sur quatre points : cible à n fini pour (5) étendu, noms de sorties du G0 avec correspondance déclarée, octets LF et règle du sha, aucun chemin de D.2 dans les entrées d'outils. Conseil, jamais verdict.
- 07:52:00Z : première ligne de code ; 07:53Z : coupe en a1/a2 (§1) ; 07:55Z : incident E-1 ; 07:57Z : export de r1.
- 07:59:09Z : **gel 1** ; 07:59:16Z : (4a) sur gel 1 ; 07:59:29Z-08:00:17Z : (1b) à 12 processus sur gel 1 ; 07:59:30Z : (1b) à 1 processus sur gel 1.
- 08:00:30Z-08:00:47Z : banc de mutants, essai 1 (pilote défectueux, E-4) ; 08:01:39Z-08:01:54Z : essai 2 sur gel 1, constat E-3 (M9).
- 08:02:37Z : (1b) à 1 processus du gel 1 arrêté (`taskkill`) ; sorties du gel 1 archivées.
- 08:03:31Z : **gel 2** (correctif E-3) ; 08:03:40Z-08:03:42Z : (4a) ; 08:03:50Z-08:09:10Z : (1b) à 1 processus ; 08:03:52Z-08:04:39Z : (1b) à 12 processus ; 08:03:59Z-08:04:23Z : banc de mutants (10/10).
- 08:09:25Z-08:39:42Z : **exécution A** (R = 10⁵, 8 cas, 12 processus), sortie 0.
- 08:39:53Z-09:07:55Z : **exécution B** (mêmes paramètres, `sortie\execution-B\`), sortie 0 ; 09:08Z : oracle (1), `cmp` et `oracles/controles_g1.py`.
- 09:10:57Z : journal final ; `SHA256SUMS` du dossier `sortie\`.

## 2. Fichiers du lot (gel 2, 2026-09-30T08:03:31Z ; `F:\tmp\shogen-lots\SIM-NIVEAU\scripts\sim\`)

| fichier | lignes | sha256 (gel 2) | chemin fixé au dépôt (G0 §7) |
|---|---|---|---|
| `sim_niveau_calc.py` | 148 | `815ffd6d98603929ead4d3f4b6ee520a82f3e1340e4b8a728b4512e53e8eacbf` | `scripts/sim/sim_niveau_calc.py` (ajout de la coupe) |
| `sim_niveau.py` | 190 | `4fe7ea29248744dac59a3cebad665ab1977e8fa602f96b233b28d80519ffff88` | `scripts/sim/sim_niveau.py` |
| `sim_niveau_oracle_r1.py` | 74 | `f960c48d04bee2d031ebfc691aedf28a8b54866444faa98a47b7d911b297770d` | `scripts/sim/sim_niveau_oracle_r1.py` |

- Relevé du gel : `GEL-2-scripts.sha256`. Le gel 1 (07:59:09Z, `sim_niveau.py` sha256 `914c8838…45bb`) est remplacé par le gel 2 à la suite du constat E-3 (§9) ; ses sorties sont archivées sous `essais\avant-correctif-oracle5\` et ne servent à rien.
- Bibliothèque standard seule : `argparse`, `contextlib`, `hashlib`, `json`, `math`, `multiprocessing`, `os`, `platform`, `random`, `sys`, `time`, `collections`, `decimal`, `fractions`, `itertools`, `operator`, `statistics`.

## 3. Décisions du G1 — ce que le G0 fixe, ce qu'il laisse ouvert

- **(a) Noms des sorties.** La commande de mission écrit `sortie/sim-niveau.json` et `sim-niveau.txt` (tiret) ; le G0 §6 fixe `sim_niveau.json`, `sim_niveau.txt` et `sim_niveau.log.txt` (souligné). Retenu : les noms du G0, que le G2 relit contre le code ; le dossier de l'exécution A est `F:\tmp\shogen-lots\SIM-NIVEAU\sortie\`. Correspondance : `sortie/sim-niveau.json` ↔ `sortie/sim_niveau.json`, `sortie/sim-niveau.txt` ↔ `sortie/sim_niveau.txt`. Changer de convention coûte une ligne (`sim_niveau.py`, liste `noms`) : Q-G1-1.
- **(b) C-5, comportement de `--p`.** Chaîne retenue : `SHOGEN-SIM-NIVEAU-1|20260930|p={p!r}|L={L}|n={n}|r={r}`. À p = 0,02 elle est identique au littéral du G0 §4 (`repr(0.02)` = `'0.02'`) ; pour tout autre `--p` (item P-1), les flux sont distincts par p (pas de nombres aléatoires communs entre p). Chaque JSON écrit le gabarit (`chaine_graine`) et la chaîne effective de r = 0 du premier cas (`chaine_effective_r0`). C-5 appartient au rédacteur du G0 : ligne proposée pour le G0 §4, « `--p` : la chaîne porte p={p!r} ; à p = 0,02 elle est celle ci-dessus ; à un autre p, flux distincts par p » (Q-G1-2).
- **(c) C-4, oracle (5) étendu : cible à n fini.** Longueur moyenne des runs d'écart des flux, estimée par le rapport de sommes Σ_{r,i} e_i / Σ_{r,i} runs_i (11 flux et R réplications ; runs comptés sur chaque série D_{i,·}), contre sa valeur exacte sur une grille de n fenêtres, tirée du G0 §2 :
  - E[Σ_t D_{i,t}] = n·p (stationnarité) ; E[runs_i] = P(D_{i,1} = 1) + Σ_{t≥2} P(D_{i,t−1} = 0, D_{i,t} = 1) = p + (n − 1)(1 − p)·b ;
  - pour L > 1, (1 − p)·b = p/L, d'où **L_n = nL/(n + L − 1)** ; pour L = 1 (b = p), **L_n = n/(1 + (n − 1)(1 − p))** ;
  - L_n → L (et 1/(1 − p) = 1,0204 pour L = 1) quand n → ∞ : c'est la cible écrite par C-4, imprimée à côté (`limite_n_infini`). Écart relatif L_n/L − 1 ≈ −(L − 1)/n : −0,59 % à L = 60, n = 10⁴ (L_n = 59,648).
  - Erreur-type par linéarisation du rapport : SE = √(Var(X_r − ρ̂·Y_r)/R) / Ȳ, X_r = Σ_i e_i, Y_r = Σ_i runs_i, ρ̂ = ΣX/ΣY, moments en `Fraction` exacte.
  - Motif mesuré : contre L lui-même, le biais de bord vaut plusieurs erreurs-types à R = 10⁵ aux L longs (chiffres au §4, ligne (5)) ; l'oracle, fail-closed, refuserait alors d'écrire une sortie juste. Le mutant 9 est tué par la cible à n fini (§5).
- **(d) Théories de l'oracle (5) indépendantes du code sous test.** P_more(p), p et L_n sont calculés par a2 à partir de p, L, n et d'une constante propre `N_FLUX = 11` (G0 §2), jamais à partir de `sim_niveau_calc` (`chaine`, `NSRC`). Correctif du gel 2 (constat E-3, §9).
- **(e) C-6, processus distincts.** Chaque enregistrement porte le PID qui l'a servi (hors empreinte, hors JSON et texte) ; le `.log.txt` écrit le nombre de PID distincts par cas et sur l'exécution. `--processus 1` s'exécute sans Pool (`map` dans le processus principal) : l'invariance (1b) compare deux chemins de code distincts.
- **(f) `script_sha256`.** Du fait de la coupe, le JSON et le texte portent le sha256 des deux fichiers exécutés (`sim_niveau.py`, `sim_niveau_calc.py`), lus à l'exécution (`__file__` de chacun) ; le G0 §6 et §7 écrivent un seul sha : la règle du sha s'applique aux deux blobs (Q-G1-3).
- **(g) Libellés de la valeur de la règle** (§1 bis.1 pt 5), sous-cause entre parenthèses : `REJETTE` ; `NE REJETTE PAS (z < 2,33)` ; `NE REJETTE PAS (discordance)` ; `NON ÉVALUABLE (garde §5.4)` ; `NON ÉVALUABLE (rejet non qualifiable)`. La valeur au sens du pt 5 est le libellé sans parenthèse ; « NE REJETTE PAS » total = somme des deux sous-causes.
- **(h) Oracles (2) et (2b) par contrôle explicite**, pas par `assert` (retiré par `python -O`). (2) compare n²·γ̂₀, calculé à partir des comptes du lag 0 de la forme par lags (C₀, S₀, S′₀ sur masques de bits, M₀ = n), à n·K(n − K) ; (2b) compare N_lag et N_bloc en entiers. La réplication rend deux drapeaux ; a2 arrête l'exécution (sortie ≠ 0, aucun fichier) au premier drapeau faux.
- **(i) Oracle (4) de la commande de mission (« égalité Python/Rust si Rust »)** : sans objet. Le G0 §7 écarte Rust sur mesure (0,029 à 0,034 s par réplication à n = 2,5·10⁴ contre le seuil de 2 s) ; aucun crate, `CARGO_HOME` non utilisé. Mesure du G1 : durées par cas au `.log.txt` des exécutions (§6).
- **(j) Colonne « temps » de la commande de mission** : le G0 §6 interdit toute durée dans le JSON et le texte (oracle 1) ; les durées murales par cas sont au `.log.txt`, et le tableau du §6 assemble texte et journal d'exécution.
- **(k) Parallélisme** : `multiprocessing.Pool(k).imap(tâche, r = 0..R−1, chunksize = 20)`, ordre conservé, agrégation dans le processus principal dans l'ordre des r ; la graine ne dépend que de (p, L, n, r).
- **(l) Fail-closed** : refus au démarrage si l'un des trois fichiers de sortie existe ; écriture en mode exclusif (`xb`) à la fin, seulement si les oracles (2), (2b) et (5) ont passé sur tous les cas ; sinon sortie ≠ 0, message sur la sortie d'erreur, aucun fichier.
- **(m) Limite déclarée de la bit-identité entre plates-formes** *(complétée le 2026-09-30 par la correction C-2 du G2, worker G1 de correction ; texte d'origine : `essais/avant-correction-C1/G1-lot-SIM-NIVEAU.avant-C2-C3.md`, §15)*. Cinq champs flottants du JSON passent par la bibliothèque mathématique C de la plate-forme (libm) et peuvent différer au dernier ulp sur une autre plate-forme :
  - `alpha_nominal` (`NormalDist().cdf`, fonction d'erreur) ;
  - `rho_puissance_ell` (puissance `**`) ;
  - `borne95_si_x_nul` (`0.05 ** (1/R)`) ;
  - **`z_sd` et `z_bloc_sd`** (diagnostics ; ajout de C-2) : `moy_sd` calcule `(x − mu) ** 2` (a2 l.47), puissance flottante de la même classe que `rho_puissance_ell`.
  - Mécanisme [lu] : `**` entre flottants appelle le `pow` de la plate-forme, après des cas spéciaux dont aucun ne vise l'exposant 2 (CPython, `Objects/floatobject.c`, `float_pow`, branche 3.14 : (paraphrase, source non versée à biblio/ : CPython float_pow délègue la puissance à la libm de la plate-forme), lu le 2026-09-30 vers 14:45Z) ; (paraphrase, source non versée à biblio/ : le module math enveloppe les fonctions de la libm C) (docs.python.org/3.14/library/math.html, même jour).
  - **Complément du correcteur, même source [lu]** : pour `math.fsum`, (paraphrase, source non versée à biblio/ : certaines libm non Windows arrondissent deux fois une somme intermédiaire, au dernier bit). Sur de telles plates-formes, `z_moyenne` et `z_bloc_moyenne` (`math.fsum(v)/len(v)`, a2 l.46) peuvent donc aussi différer au dernier bit, comme les sommes de `z_sd` et `z_bloc_sd`. `math.fsum` sort ainsi de la liste des opérations correctement arrondies qu'écrivait ce point.
  - Tous les autres flottants sont des conversions ou opérations correctement arrondies (`Decimal` → `float`, `float(Fraction)`, `math.sqrt`, + − × ÷ ; déclaration d'origine du G1, non re-sourcée par C-2).
  - La bit-identité exigée (même machine) n'est pas touchée : a1 et a2 sont inchangés par la correction (gel 3, §15) et la sortie A garde son sha. Un rejeu tiers sur une autre plate-forme peut voir un autre sha du JSON sans qu'aucun compte ni taux ne change.
  - Le texte imprime `alpha_nominal` à 8 décimales, `rho_puissance_ell` et la borne à 3 chiffres significatifs, `z_sd` et `z_bloc_sd` à 4 décimales. Un écart d'un ulp ne change un chiffre imprimé que si la valeur tombe sur une frontière d'arrondi [inféré] ; le sha du texte n'est donc exposé que dans ce cas.

## 4. Oracles non-LLM — résultats (gel 2)

| oracle | exécution | résultat |
|---|---|---|
| **(1) bit-identité** | A (`sortie\`, 08:09:25Z-08:39:42Z) contre B (`sortie\execution-B\`) ; R = 10⁵, 8 cas, 12 processus chacune | JSON identiques (sha256 `d17c51219751d24738127e6f8a99de06e3f7f00c0e29f659c2028e4d54d9350e`), textes identiques (`7173a9cecc5118390022aad00471d7f7de07d22403055f1def548ec0e57000eb`), `cmp` sans différence ; 8 empreintes par cas identiques ; 12 PID distincts par cas dans A et dans B ; journaux d'exécution différents (horloges), hors bit-identité |
| **(1b) invariance au parallélisme** (précondition du (1)) | R = 2 000, 8 cas : `--processus 1` (sans Pool, 08:03:50Z-08:09:10Z) contre `--processus 12` (08:03:52Z-08:04:39Z) | JSON identiques (sha256 `3a5b91ce114bb85ae4039406078690aa8cefc13f0c57e0858dedc465d88c69df`), textes identiques (`c241cb155d0d79b1b48a21388623fb4ddce0643c53800e9dd2f56df0aade1b8c`) ; **C-6 : 12 PID distincts dans chacun des 8 cas** à 12 processus (1 PID à 1 processus), au `.log.txt` |
| **(2) n²γ̂₀ = n·K(n − K)** | A, à chaque réplication | 100000/100000 dans chacun des 8 cas (800 000 réplications) ; idem en (1b) (2000/2000 × 8, deux fois) |
| **(2b) N_lag = N_bloc** (entiers) | A, à chaque réplication | 100000/100000 dans chacun des 8 cas |
| **(3) erreur-type imprimée** | A | chaque taux porte x, r, SE et, à x = 0, la borne 1 − 0,05^(1/R) = 2,996·10⁻⁵ ; recalcul indépendant depuis x et R (`oracles/controles_g1.py`, `Fraction`) : **24/24 taux égaux** (r exact, SE à 10⁻¹⁵ relatif, borne égale à x = 0) |
| **(4) σ̂² = `r1.block_long_run_variance`** | — | non exécutable à `f5b8269` (fonction absente) ; item SHOGEN-SIM-NIVEAU-ORACLE4-1, déclencheur : commit de B-DEP-1 |
| **(4a) plug-in, garde et z = r1 à `f5b8269`** | 08:03:40Z, `sortie\oracle-4a\oracle_4a.json` | **1 363 égalités exactes** (== et `str`) : 3 constantes + 8 cas × 10 réplications × 17 valeurs (11 p̂_i, P̂₀, P̂₁, P̂_more, garde, garde tenue, z) ; sortie 0 |
| **(5) générateur contre la théorie** (étendu, C-4) | A, 3 contrôles × 8 cas = 24 | tous sous 5 SE ; **max |écart| = 2,34 SE** (run moyen, L = 1, n = 10⁴) ; détail par cas au `sim_niveau.txt` |
| (4) de la commande de mission, Python/Rust | — | sans objet (§3 i) |

- **Motif chiffré de la cible L_n (C-4, §3 c)**, sortie A : écart du run moyen à la limite L, en erreurs-types, de −2,55 / −0,04 (L = 1), −4,03 / −1,17 (L = 5), **−7,33** / −4,67 (L = 20), **−11,43 / −7,36** (L = 60), pour n = 10⁴ / 2,5·10⁴ ; contre L_n : −2,34 / +0,10, −1,07 / +0,71, −0,85 / −0,58, +0,01 / −0,10. Contre L, trois cas sur huit dépasseraient 5 SE et le script, fail-closed, n'aurait rien écrit.
- **Mutants** : 10 tués sur 10 (§5).

## 5. Mutants de programme (registre ADR-0011 ; copies sous `F:\tmp\shogen-lots\SIM-NIVEAU\mutants\`, jamais sur les fichiers gelés)

Pilote `mutants/mutants.py` (sha256 `9c2df38db23f1a81864269685e43a47a6a1f85fd238461ac2b950db3c5470448`) : une substitution textuelle par mutant (occurrence unique exigée), exécution courte, critère = l'oracle nommé échoue. Exécution sur le gel 2 : 08:03:59Z-08:04:23Z, `mutants/sortie-banc.txt`, `mutants/resultats.json`. **10 tués sur 10.**

| # (G0 §8) | mutant | oracle qui le tue | preuve (message de sortie ≠ 0, ou comparaison) |
|---|---|---|---|
| 1 | poids 2(ℓ − k) → 2(ℓ − k − 1), forme par lags | (2b) | `oracle (2) ou (2b) en echec : L=5 n=10000 r=0` (R = 3) |
| 2 | forme en blocs appelée avec ⌊n·P̂_more⌋ à la place de K (centrage et complément du préfixe) | (2b) | idem, r = 0 |
| 3 | lag 0 compté deux fois (W₀ = 2ℓ) | (2b) | idem, r = 0 |
| 4 | a et b inversés | (5), K/n | moyenne 0,98495 contre 0,019513, +9 134 SE (R = 200) |
| 5 | K = fenêtres à ≥ 1 écart | (5), K/n | 0,200641 contre 0,019513, +230 SE (R = 200) |
| 6 | graine tirée d'un compteur de tâches propre à chaque processus, au lieu de (L, n, r) | (1b) | `--processus 1` : sortie 0 ; `--processus 12` : sortie ≠ 0 (graines répétées d'un processus à l'autre, (5) K/n à −5,75 SE) ; les deux exécutions ne rendent donc pas la même sortie |
| 7 | plug-in en flottants (`Decimal(x / n)`) | (4a) | p̂₁ : r1 `0.0219`, script `0.02189999999999999932…` |
| 8a | p̂_i = e_i/(n − 1) | (4a) | p̂₁ : r1 `0.0219`, script `0.0219021902…` |
| 8b | P̂₁ sans le facteur Π_{j≠i}(1 − p̂_j) | (4a) | P̂₁ : r1 `0.18106522867…`, script `0.2220` |
| 9 | L = 1 codé en chaîne à ρ = −p/(1 − p) (a = 0, b = p/(1 − p)) | **(5) étendu (C-4)** | run moyen 1,0 contre L_n = 1,0204061 ; tous les runs valent 1, l'erreur-type est nulle, écart infini (R = 200) |
| 10 | « ≥ 2,33 » → « > 2,33 » | aucun | mutant équivalent en probabilité (égalité exacte à 2,33 de mesure nulle), déclaré au G0, non exécuté |

- **Table du G0 à mettre à jour (C-4, rédacteur du G0)** : mutant 9, « (5) étendu » au lieu de « aucun oracle » ; mutant 4, « (5) : K/n et run moyen » ; mutant 6, « (1b) ; à 12 processus, (5) peut aussi refuser d'écrire ».
- **Deux essais antérieurs du banc, déclarés et conservés** : `mutants/essai-1-pilote-defectueux/` (le pilote plantait à l'impression, encodage cp1252 de la console, et le critère de M6 exigeait deux sorties écrites) ; `mutants/essai-2-gel-1/` (même banc sur le gel 1, 10 sur 10, mais M9 n'y était tué que par un arrondi : constat E-3, §9).

## 6. Résultats de l'exécution A (`sortie\sim_niveau.txt` ; R = 10⁵ par cas, p = 0,02, ℓ = 240)

Taux de rejet à tort sous le modèle nul synthétique : x/R, puis r (SE = √(r(1 − r)/R)) ; à x = 0, borne unilatérale à 95 % 2,996·10⁻⁵. α nominal = 1 − Φ(2,33) = 0,00990308, imprimé pour comparaison ; **aucun critère n'en est tiré (C-6)** ; rien n'est établi sur des sources réelles (doc 09). Durées : `sortie\sim_niveau.log.txt` (horloge murale, 12 processus), hors bit-identité.

| L | n | r_z (z ≥ 2,33, garde tenue) | r_bloc (z_bloc publiée ≥ 2,33) | r_règle (REJETTE) | discordances | σ̂² = 0 | SD(z) | SD(z_bloc) | FIV médian | run max de I ≥ ℓ | durée |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 10 000 | 265 → 0,002650 (0,000163) | 208 → 0,002080 (0,000144) | 159 → 0,001590 (0,000126) | 106 | 0 | 0,828 | 0,855 | 0,96 | 0 | 146,7 s |
| 1 | 25 000 | 257 → 0,002570 (0,000160) | 206 → 0,002060 (0,000143) | 181 → 0,001810 (0,000134) | 76 | 0 | 0,830 | 0,841 | 0,98 | 0 | 306,5 s |
| 5 | 10 000 | 8 374 → 0,083740 (0,000876) | 6 → 0,000060 (0,000024) | 6 → 0,000060 (0,000024) | 8 368 | 0 | 1,670 | 0,766 | 5,11 | 0 | 110,9 s |
| 5 | 25 000 | 8 205 → 0,082050 (0,000868) | 7 → 0,000070 (0,000026) | 7 → 0,000070 (0,000026) | 8 198 | 0 | 1,673 | 0,736 | 5,33 | 0 | 371,4 s |
| 20 | 10 000 | 24 234 → 0,242340 (0,001355) | 0 (borne 2,996·10⁻⁵) | 0 (borne 2,996·10⁻⁵) | 24 234 | 0 | 3,446 | 0,938 | 19,53 | 0 | 120,3 s |
| 20 | 25 000 | 24 627 → 0,246270 (0,001362) | 3 → 0,000030 (0,000017) | 3 → 0,000030 (0,000017) | 24 624 | 0 | 3,456 | 0,795 | 21,24 | 0 | 341,9 s |
| 60 | 10 000 | 32 717 → 0,327170 (0,001484) | 0 (borne 2,996·10⁻⁵) | 0 (borne 2,996·10⁻⁵) | 32 717 | 437 | 5,964 | 3,358 | 45,58 | 489 | 129,4 s |
| 60 | 25 000 | 33 730 → 0,337300 (0,001495) | 0 (borne 2,996·10⁻⁵) | 0 (borne 2,996·10⁻⁵) | 33 730 | 0 | 6,000 | 1,031 | 53,97 | 1 237 | 289,1 s |

- **Comptes communs aux 8 cas** : garde §5.4 non tenue 0 ; NON ÉVALUABLE (garde) 0 ; NON ÉVALUABLE (rejet non qualifiable) 0 (les 437 réplications à σ̂² = 0 ont K = 0, donc z < 2,33). Comptes « hors famille, sans conclusion » (pt 8) : z ≤ −2,33 de 216 (L = 1, n = 10⁴) à 37 939 (L = 60, n = 10⁴) ; z_bloc ≤ −2,33 de 283 à 8 855 (JSON, `comptes`).
- **Portée de la dépendance** (G0 §2) : ρ^ℓ = 1,630·10⁻² à L = 60, imprimé par cas ; le niveau mesuré à L = 60 inclut le biais de troncature du noyau au-delà de ℓ ; le drapeau « run maximal de I ≥ ℓ » est levé dans 489 et 1 237 réplications sur 10⁵ à L = 60 (pt 9, sans effet sur la valeur).
- **Durée totale** : A 30 min 17 s (08:09:25Z-08:39:42Z) pour 8·10⁵ réplications sur 12 processus, soit ≈ 0,027 s de processus par réplication en moyenne (machine partagée, charge d'autres processus non contrôlée) ; B 28 min 02 s (08:39:53Z-09:07:55Z).
- **Chiffres cités par l'ADR** : §1 bis.1 pt 7 et §1 bis.3 citent « 10 à 34 % de rejets à tort pour des runs de 5 à 60 fenêtres » (R ≤ 150, RECONCILIATION §3, CRITIQUE v2 §4.3). Mesure de ce lot au même p, R = 10⁵ : r_z de 8,21 % (0,087 % d'erreur-type) à 33,73 % (0,15 %) pour L ∈ {5, 20, 60}. La reprise de la citation au paquet relève de l'orchestrateur (Q-G1-7) ; C-6 : sans effet sur ℓ, le seuil ni la règle.

## 7. Tuyaux (règle Branchement, CA-11)

- **Entrée** : constantes du G0 (p, L, n, R, GRAINE et sa dérivation, ℓ, seuils), codées dans a1 (`NSRC`, `ELL`, `PREC`, `GRAINE`, `SEUIL_Z`, `SEUIL_HIST`, `N_MIN_BLOCS`, `CHAINE`) et a2 (`P_DEFAUT`, `R_DEFAUT`, `CAS`, `N_FLUX`).
- **Sortie** : `sim_niveau.json` et `sim_niveau.txt`, identiques à l'octet sur 2 exécutions complètes (A, B) et sur 2 exécutions à R = 2 000 (1 et 12 processus), même machine, Python 3.14.5 ; `sim_niveau.log.txt` hors bit-identité ; sha256 au `SHA256SUMS` du dossier `sortie\`.
- **État** : dossier `F:\tmp\shogen-lots\SIM-NIVEAU\sortie\` ; au dépôt, emplacement fixé par le lot PAQUET (proposition du G0 : `docs/adr-0028/sim-niveau/`) ; sha au JOURNAL par l'orchestrateur, avec le commit C et le sha des deux scripts.
- **Consommateurs** : texte scellé §1 bis.1 pt 7 (niveau) ; cp-1 du lot PAQUET ; lecteur tiers qui rejoue au commit C.
- **Valeur attendue du test de composition** : le JSON porte le sha256 des deux scripts et aucune horloge ; si les blobs commis sont égaux, à l'octet, aux fichiers du gel 2 (§2), l'exécution du paquet depuis `git archive <C> scripts/sim` avec la commande du G0 §7 doit rendre `sim_niveau.json` sha256 `d17c51219751d24738127e6f8a99de06e3f7f00c0e29f659c2028e4d54d9350e` et `sim_niveau.txt` sha256 `7173a9cecc5118390022aad00471d7f7de07d22403055f1def548ec0e57000eb`, sur cette machine ; tout autre sha est un écart.
- **Tests de composition** : oracle (1), rejoué ici sur deux exécutions complètes (§4) et à rejouer par l'orchestrateur depuis le blob commis ; oracle (4a) aujourd'hui (script contre r1), (4) après B-DEP-1 ; garde (1) de D.4 b au RENDU-1 (sha du paquet). Tuyau conditionnel déclaré : (4), déclencheur écrit (commit de B-DEP-1, item ORACLE4-1).

## 8. Risques MAST (libellés de l'annexe C ; ligne SIM-NIVEAU, annexe C l.27) et contre-mesures du G1

- **FM-1.1 Disobey task specification** (paramètres synthétiques) : p, R, graine, cas et définitions des taux sont ceux du G0 ; aucune valeur de source ; L = 1 codé en tirages indépendants (mutant 9, tué par (5) étendu). Contrôle non-LLM des chemins de D.2 dans les appels d'outils : acte de l'orchestrateur (C-1 pour le G0 ; même contrôle applicable à ce G1). Ce journal ne recopie aucun chemin de la liste D.2, pour que la recherche par motifs (regex C-3 de la CRITIQUE v2 §7) ne lève pas de faux positif ; la liste figure dans la sortie structurée du worker.
- **FM-2.4 (exposition retenue)** : exposition du G1 déclarée au §14 ; aucune pièce de D.2 ouverte.
- **FM-3.3 (vérification incorrecte)**, réplique qui diverge de r1 : (4a), 1 363 égalités exactes ; mutants 7, 8a, 8b tués. Oracle qui dérive du code sous test : constat E-3, corrigé (§3 d). Lecture de la sortie comme un verdict : C-6 recopiée dans le JSON et dans le texte ; §6 sans critère.
- **Non-déterminisme caché** : graine par (p, L, n, r), agrégation ordonnée, `math.fsum`, aucune horloge dans JSON et texte ; oracles (1) et (1b) ; mutant 6 tué.

## 9. Écarts et incidents déclarés ; `error_origin` proposés (à assigner au G7)

- **E-1 (incident, sans effet)** : 07:55Z, `python -B -m py_compile sim_niveau.py` a écrit `scripts\sim\__pycache__\sim_niveau.cpython-314.pyc` (py_compile écrit son `.pyc` quel que soit `-B`) sous `F:\tmp` ; supprimé à 07:55:44Z ; rien sur `C:` ni dans `F:\Shogen`. Contrôle final : `find F:/tmp/shogen-lots/SIM-NIVEAU -name __pycache__` vide (§12). `error_origin` proposé : G1 (outillage du worker).
- **E-2 (défaut attrapé avant gel)** : la première version de l'adaptateur déclarait les trois constantes (`DECIMAL_PREC`, `SEUIL_HIST`, `SEUIL_Z`) sans les comparer (le contrôle ne parcourait que les paires ajoutées par cas). Corrigé à la relecture, avant le gel 1. `error_origin` : G1.
- **E-3 (défaut de conception d'oracle, attrapé par le banc de mutants)** : au gel 1, la cible de l'oracle (5) pour le run moyen était calculée avec `C.chaine(p, L)`, c'est-à-dire avec le code sous test. Sur le mutant 9, la cible suivait donc le mutant (b = p/(1 − p) ⇒ L_n = 0,9999999999999999) et le mutant n'était tué que par un arrondi (moyenne 1,0 contre 0,9999999999999999, erreur-type nulle). Correctif du gel 2 (08:03:31Z) : cibles tirées du G0 §2 (formules fermées en p, L, n) et constante `N_FLUX = 11` propre à a2 (§3 d). Les exécutions faites sur le gel 1 — (4a) à 07:59Z, (1b) à 12 processus terminée à 08:00Z, (1b) à 1 processus arrêtée volontairement à 08:02Z (`taskkill`, sortie ≠ 0, aucun fichier) — sont archivées sous `essais\avant-correctif-oracle5\` et remplacées ; aucun paramètre du G0 (p, R, graine, cas, définitions des taux) n'a changé. `error_origin` proposé : G1 (conception de l'oracle).
- **E-4 (pilote de banc)** : premier essai du banc de mutants planté à l'impression (console cp1252) et critère de M6 trop étroit ; corrigé, essais conservés (§5). `error_origin` : G1 (outillage).
- **E-5 (écart au G0, déclaré)** : trois fichiers au lieu de deux (coupe R-25, §1) ; `script_sha256` en dictionnaire (§3 f) ; export de r1 restreint à `shogen_s2` (§0) ; libellés à sous-cause (§3 g). Aucun ne touche p, R, la graine, les cas ni les définitions des taux.
- **Exécutions d'essai déclarées** (`essais\`, toutes antérieures au gel 2 ou sur copies) : e1 à e4 (R = 30 à 60, deux cas chacune, contrôles de fonctionnement), `o4a-essai.json`, `m9-apres\` (contrôle du correctif E-3 sur M9). Aucune n'a conduit à changer un paramètre du G0.

## 10. Review Focus (pour le G2)

1. Répliques de r1 (a1, l.49-81) contre r1.py l.199-238 à `f5b8269`, ligne à ligne ; p̂_i de la réplication contre `compute_r1` l.450-452.
2. `num_blocs` : préfixe complété, `pre[v]` = somme des I_t sur les min(max(v − ℓ + 1, 0), n) premières fenêtres ; c_j = pre[u + ℓ] − pre[u], u = j + ℓ − 1.
3. `num_lags` : masques C_k = |X ∧ (X ≫ k)|, S_k = |X ∧ (2^{n−k} − 1)|, S′_k = |X ≫ k|, M_k = n − k ; poids W₀ = ℓ, W_k = 2(ℓ − k) ; (2) calculé sur les comptes du lag 0.
4. Valeur de la règle : ordre des branches contre §1 bis.1 pt 5 (garde, puis z, puis publication de z_bloc, puis z_bloc).
5. Oracle (5) : cibles tirées du G0 §2 et indépendantes de a1 ; linéarisation du rapport ; L_n contre L (§3 c).
6. Dénominateurs des taux (R sans conditionnement) ; borne 1 − 0,05^(1/R) à x = 0.
7. Mutant 10 et sens de la garde (« < 10 » pour « non tenue ») : relecture seulement.

## 11. Questions ouvertes Q-G1-n (pour l'orchestrateur)

- **Q-G1-1** : noms des sorties, `sim_niveau.*` (G0 §6, retenus) ou `sim-niveau.*` (commande de mission) ; une ligne à changer si la commande prévaut (§3 a).
- **Q-G1-2** : ratification de C-5 telle qu'implémentée (`p={p!r}`, flux distincts par p) et ligne à poser au G0 §4 par son rédacteur (§3 b).
- **Q-G1-3** : la règle du sha du G0 §7 porte sur deux blobs (`sim_niveau.py`, `sim_niveau_calc.py`) ; l'export `git archive <C> scripts/sim` les emporte tous deux, avec l'adaptateur (§3 f).
- **Q-G1-4** : ratification de la cible à n fini L_n de l'oracle (5) étendu, au lieu de la limite L écrite par C-4 (§3 c) ; motif chiffré au §4.
- **Q-G1-5** : C-3, C-7, C-8 et la mise à jour de la table des mutants (C-4) restent au rédacteur du G0 ; les lignes datées de C-2 sont au §1.
- **Q-G1-6** : l'annexe C l.27 place la contre-mesure (3) (contrôle non-LLM des chemins de D.2 dans les appels d'outils) sur les missions du G0 **et du G1** : le contrôle de C-1 est à étendre aux appels d'outils de ce worker G1 ; ce journal n'en recopie aucun chemin pour ne pas créer de faux positif. Contrôle mécanique fait par le G1 sur ses propres fichiers (`oracles/controle_c3.py`, motifs lus dans la CRITIQUE v2 l.411-413, jamais recopiés) : 0 occurrence dans ce journal, les trois scripts, `mutants.py`, `controles_g1.py` et `controle_c3.py` ; témoin positif : 21 occurrences dans le G0 lui-même (sa liste §0 des pièces non ouvertes), que le contrôle de C-1 relèvera donc sur l'écriture du G0, à distinguer d'une lecture.
- **Q-G1-7** : la citation « 10 à 34 % » (§1 bis.1 pt 7, §1 bis.3 ; R ≤ 150) et la sortie de ce lot (r_z de 8,21 % à 33,73 % pour L ∈ {5, 20, 60}, R = 10⁵, §6) portent sur le même p ; le G0 §3 prévoit que le paquet ne porte qu'un jeu de chiffres. Reprise au paquet : acte de l'orchestrateur (lot PAQUET), sans effet sur ℓ, le seuil ni la règle (C-6).
- **Q-G1-8** : prix mesuré pour l'item SHOGEN-SIM-NIVEAU-P-1 : ≈ 30 min murales par valeur de p sur 12 processus (exécution A), soit ≈ 2 h pour les quatre valeurs de sa grille [inféré : même machine, même charge ; le G0 écrivait ≈ 1,8 h].

## 12. Livrables (`F:\tmp\shogen-lots\SIM-NIVEAU\`)

| chemin | rôle | sha256 |
|---|---|---|
| `scripts\sim\sim_niveau_calc.py` | sous-lot a1 | `815ffd6d98603929ead4d3f4b6ee520a82f3e1340e4b8a728b4512e53e8eacbf` |
| `scripts\sim\sim_niveau.py` | sous-lot a2 | `4fe7ea29248744dac59a3cebad665ab1977e8fa602f96b233b28d80519ffff88` |
| `scripts\sim\sim_niveau_oracle_r1.py` | sous-lot b | `f960c48d04bee2d031ebfc691aedf28a8b54866444faa98a47b7d911b297770d` |
| `GEL-2-scripts.sha256` | relevé du gel 2 | `ae7b396046e15c3ac9508bc96c58cc96ce748e62df091a115817072f5ebda819` |
| `sortie\sim_niveau.json` | **sortie A** (« sortie/sim-niveau.json » de la commande, §3 a) | `d17c51219751d24738127e6f8a99de06e3f7f00c0e29f659c2028e4d54d9350e` |
| `sortie\sim_niveau.txt` | **sortie A** (« sim-niveau.txt ») | `7173a9cecc5118390022aad00471d7f7de07d22403055f1def548ec0e57000eb` |
| `sortie\sim_niveau.log.txt` | journal d'exécution A (durées, PID) | `058fb1f4a668b9ddc69ca078c8608cd2ae88cfed0aab72148c803f024d640c93` |
| `sortie\execution-B\` | sortie B, oracle (1) (JSON et texte = A) | journal `02e6fa72…e89c` |
| `sortie\oracle-1b\processus-1\`, `processus-12\` | oracle (1b) | JSON `3a5b91ce…69df`, texte `c241cb15…b8c` |
| `sortie\oracle-4a\oracle_4a.json` | oracle (4a) | `653b78295b6bb8e7f9e46510b115559faa69dc8372175e635213977e23bd0af2` |
| `sortie\SHA256SUMS` | 13 fichiers du dossier `sortie\` (chemins relatifs ; `sha256sum -c` : 13 OK) | `b541b4f73e37376aebed03393db4b231ca0733702265816353320b1887f3a9ee` |
| `oracles\controles_g1.py`, `controles_g1.out.txt` | contrôles (1), (3), (5), tableau | `d5c573b7…6636`, `3ee80360…d20c` |
| `oracles\controle_c3.py`, `motifs-c3.txt` | contrôle mécanique C-3 (§8, §11) | `59dc2ae2…6483`, `191df2af…abfc` |
| `mutants\mutants.py`, `resultats.json`, `sortie-banc.txt` | banc de mutants (§5) | `9c2df38d…0448`, `b2c9ec46…f6f2a`, `f0b82971…6461` |
| `oracle-r1-f5b8269\s2-harness\shogen_s2\` | export de r1 à `f5b8269` | `r1.py` : `992f841c018185b3031bbbdcc44a68fd6147c85f9b2e306af1e886a806ca07b9` (blob `1d6a908c…`) |
| `essais\` | essais déclarés (§9) et sorties du gel 1 archivées | — |
| `G1-lot-SIM-NIVEAU.md` | ce journal | sha256 dans la sortie structurée du worker |

- **Contrôles de clôture** : `find F:/tmp/shogen-lots/SIM-NIVEAU -name __pycache__` : 0 ; `git -C F:/Shogen status --porcelain` : `?? .claude/worktrees/` (inchangé) ; aucun fichier neuf sous `C:\Users\KACIMI\AppData\Local\Python` depuis 07:26Z (`find -newer`, 0) ; `TMP`, `TEMP` et `TMPDIR` sur `F:` pour toutes les commandes.
- **Versement** : acte de l'orchestrateur (lot PAQUET) ; les trois scripts vont à `scripts/sim/` (chemin du G0 §7), les sorties à l'emplacement que fixe PAQUET, avec le `SHA256SUMS`.

## 13. Commandes rejouables (Git Bash ; aucune écriture hors de `F:\tmp`)

```
export TMP=F:/tmp/shogen-tests-tmp TEMP=F:/tmp/shogen-tests-tmp TMPDIR=F:/tmp/shogen-tests-tmp PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
cd /f/tmp/shogen-lots/SIM-NIVEAU
(cd scripts/sim && sha256sum -c ../../GEL-2-scripts.sha256)                       # gel 2 : 3 OK
(cd sortie && sha256sum -c SHA256SUMS)                                             # sorties du lot
python -B scripts/sim/sim_niveau_oracle_r1.py --r1 oracle-r1-f5b8269/s2-harness --sortie F:/tmp/shogen-tests-tmp/o4a.json   # (4a), ~2 s
python -B scripts/sim/sim_niveau.py --sortie F:/tmp/shogen-tests-tmp/p1 --R 2000 --processus 1     # (1b), ~6 min
python -B scripts/sim/sim_niveau.py --sortie F:/tmp/shogen-tests-tmp/p12 --R 2000 --processus 12   # (1b), ~50 s
cmp F:/tmp/shogen-tests-tmp/p1/sim_niveau.json sortie/oracle-1b/processus-1/sim_niveau.json        # rejeu identique attendu
python -B scripts/sim/sim_niveau.py --sortie F:/tmp/shogen-tests-tmp/C --processus 12             # (1), exécution complète
cmp F:/tmp/shogen-tests-tmp/C/sim_niveau.json sortie/sim_niveau.json && cmp F:/tmp/shogen-tests-tmp/C/sim_niveau.txt sortie/sim_niveau.txt
python -B oracles/controles_g1.py sortie sortie/execution-B                        # (1), (3), (5), tableau
git -C /f/Shogen rev-parse f5b8269:s2-harness/shogen_s2/r1.py                      # 1d6a908c…
```

Rejeu du banc de mutants : copier `mutants/mutants.py` dans un dossier vide voisin de `scripts\` et de `oracle-r1-f5b8269\` (chemins relatifs du pilote), puis `python -B mutants.py` (≈ 30 s) ; attendu : `tues 10 sur 10`.

## 14. Attestation d'exposition (forme de l'annexe D.3, précisée par C-8)

**Je n'ai vu ni z, ni K, ni P̂_more, ni φ des journaux de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne, hors les comptes de classe M repris par ADR-0028/D.1 et les avis (Pyth 0 ok / 40 804, DNS du harnais). Aucune statistique S2 n'a été calculée.** Les z, K et P̂_more de ce lot portent sur des données synthétiques seules.

- **Non ouverts** : les pièces D.2 n° 1 à 9 de l'annexe D d'ADR-0028, toutes, et les chemins interdits nommément par la commande de mission (liste recopiée dans la sortie structurée du worker, pas ici, §8) ; aucun journal de campagne ni copie ; aucune transcription de session ; `JOURNAL.md` non ouvert.
- **Pièces lues** (lecture seule) :
  - le G0 du lot, entier ; le cp-1 (`CP1-SIM-NIVEAU.md`, sha256 `ece81297…6303` : l.18-57 à la déclaration d'origine, **corrigées en l.18-70** par la correction C-3 du G2 le 2026-09-30, note datée en fin de section) ; `g0-mesure\` : `proto_temps.py`, `proto_pool.py`, `calc_constantes.py` et sa sortie ;
  - ADR-0028 : liste des titres (`grep`), l.88-124 (§1 bis.1 et §1 bis.2) ; annexe A l.11 et l.41, annexe B l.104, annexe C l.22 et l.27 (par `grep` du nom du lot) ; annexe D l.29-120 (D.2, D.3, début de D.4) ;
  - consultations du 2026-09-30 (`sha256sum -c SHA256SUMS.txt` : 11/11 OK) : CRITIQUE v2 (titres par `grep`, qui affichent aussi les l.405-416 de son §7, puis l.215-236 et l.294-312) ; AVIS-advisor-defi l.30-47 ; RECONCILIATION-Q2-advisor-defi (titres, l.87-102, l.150-153) ;
  - `r1.py` à `f5b8269` (l.1-80, l.190-245, l.370-524) ; lignes d'import de `records.py` et `window.py` ; `shogen_s2/__init__.py` ; noms de fichiers de `s2-harness` (`git ls-tree`) ;
  - Git : `.gitattributes` à `f5b8269` (l.1-20) ; `core.autocrlf` ; à la clôture, le sujet du commit `cf696bd` (`git log`, une ligne tronquée à 220 caractères) et `git diff --stat f5b8269 HEAD` (`JOURNAL.md`, +2), contenu de `JOURNAL.md` non ouvert ;
  - doc 09 entier ; `docs/G1-lot-B0-pool-analyse.md` (l.1-60, titres, l.200-238) ; corpus doc 02 (ligne R-25, par `grep`) ; noms des dossiers `docs\` et `docs\adr-0028\`.
- **Exposé à** (classe M, constantes de conception, résultats synthétiques) : les comptes opérationnels que recopient le §0 du G0, l'ADR §1 bis.2 et l'avis advisor-defi (comptes de fenêtres, bornes de calendrier, Pyth, `resolve_failed`) ; σ_classe maximal (10 695 s) ; les résultats synthétiques antérieurs à p = 0,02 (RECONCILIATION §3, CRITIQUE v2 §4.3, AVIS Q1 (v)) ; le nom d'une source dans l'attestation D.3 (a), valeurs masquées, et les noms des fixtures de `s2-harness/tests` (noms de fichiers seulement).
- Aucune de ces valeurs n'entre dans le code ni dans les paramètres de ce lot : p, R, graine, cas et définitions viennent du G0.
- **Correction C-3 du G2 (2026-09-30, worker G1 de correction `claude-opus-5-5`, contexte frais) : source du texte des corrections C-1 à C-9 appliquées.**
  - *Faits mesurés par le correcteur* : `CP1-SIM-NIVEAU.md`, sha256 `ece81297…6303` recalculé à 15:03:32Z, égal à celui du Mandat ; 78 lignes (`wc -l` et `awk`, fin de ligne finale présente ; le G2 écrit 79, §0 de son rapport, sans effet sur les plages) ; le texte des corrections forme le §4 du cp-1, l.58-70 (titre l.58, C-1 à C-9 l.60-68, phrase de clôture l.70) ; les l.18-57 ne portent que les libellés « correction C-4, C-6 », « précision C-5 » et « précision C-8 » (tableau, l.39-48), sans leur texte.
  - *Ce que montrent ce journal et le code du G1* : trois formulations propres au §4 du cp-1, que `grep` ne trouve nulle part dans ses l.1-57, y sont reprises : « nombres aléatoires communs entre p » de C-5 (cp-1 l.64 ; §3 b de ce journal, qui écrit aussi « flux sont distincts par p » pour « flux distincts par p ») ; « PID distincts ayant servi des réplications » de C-6 (cp-1 l.65 ; ligne du journal d'exécution écrite par `sim_niveau.py`, l.180) ; la phrase de C-8 « … (Pyth 0 ok / 40 804, DNS du harnais) » (cp-1 l.67 ; en tête de ce §14). Le G1 disposait donc du texte des l.58-70.
  - *Source nommée* : le cp-1, l.58-70 (§4, liste fermée C-1 à C-9), que la ligne « Mandat » de ce journal désigne, avec son sha256, comme source des corrections. La plage déclarée est corrigée en l.18-70 ; les l.1-17 et l.71-78 restent non déclarées pour le G1 d'origine.
  - *Non établi par le correcteur* : si la commande de mission du G1 recopiait aussi ces textes. Le correcteur n'a ni cette commande ni la transcription du G1 (non ouverte, par règle). **Question formée Q-C3-1**, à l'orchestrateur, détenteur de la commande : la commande de mission du G1 porte-t-elle, mot pour mot, la phrase de C-8 ci-dessus ? Une recherche de chaîne suffit. Si oui, la source est double (commande et cp-1), et la ligne JOURNAL du lot le dit.
  - *Sans effet d'exposition* : les l.58-78 du cp-1 ne portent aucune pièce de D.2 (G2 §6, relu par le correcteur) ; la l.67 ne porte que des comptes de classe M, déjà déclarés dans « Exposé à ».

## 15. Correction du G2 (C-1 à C-3), 2026-09-30 — amendement daté, ajouté en fin de journal

- **Correcteur** : worker G1 de correction, modèle résolu `claude-opus-5-5` (R-1), effort max, contexte frais. Commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`), HEAD `7425a49`. Liste fermée : `G2-rapport.md` §12 (sha256 `94175e57…1d7c`). Aucun commit, aucun workflow (R-20).
- **Rapport de correction** (correction → changement → preuve) : `correction-rapport.md`, à côté de ce journal. Texte d'origine de ce journal : `essais/avant-correction-C1/G1-lot-SIM-NIVEAU.avant-C2-C3.md` (sha256 `8d72c475…9779`, celui que cite le G2).
- **Corrections en place** : §3 m (C-2) et §14 (C-3), marquées et datées. Le reste du journal est le texte d'origine du G1. Ses valeurs remplacées par la correction C-1 sont listées ci-dessous et restent lisibles à leur place.

| cellule d'origine | valeur d'origine (gel 2) | valeur au gel 3 (C-1) |
|---|---|---|
| en-tête « Résultat » ; §1, table et ligne datée SIM-NIVEAU-b ; §2 | b : 74 lignes, sha256 `f960c48d…770d` | b : **196** lignes, sha256 `cb844d5b724223def91cd2d3397b4deebef9f6a7353d9aa41e30b3361ca2c11d` ; a1 (148) et a2 (190) inchangés |
| §2, « Relevé du gel » ; §12 | `GEL-2-scripts.sha256` (`ae7b3960…a819`) | `GEL-3-scripts.sha256` (sha256 `632dedf9ca8533a48b17b9843c20f03b21908ba767401018f285d6e6c20516d0`, 14:56:18Z) |
| en-tête « Résultat » ; §4, ligne (4a) ; §12 | `sortie/oracle-4a/oracle_4a.json` (`653b7829…0af2`), 1 363 égalités | `sortie/oracle-4a-4b/oracle_4a_4b.json` (sha256 `bd3cc31125ec83ad349f1a130574ff563d9f32f1aeb7dfbdc912d8fcacf63e5e`) : (4a) 1 363 égalités, inchangé ; (4b) (i) 2 280 égalités ; (4b) (ii) 64 invariants sur chacun des JSON A, B, (1b) processus 1 et 12. L'ancien enregistrement est archivé sous `essais/avant-correction-C1/oracle-4a/` |
| §4 | pas de ligne (4b) | (4b) (i) recalcul indépendant de chaque enregistrement, égalité exacte ; (ii) invariants de comptes (`--json`) |
| en-tête « Résultat » ; §5 | banc `mutants/`, 10 tués sur 10 | banc `mutants/banc-C1/` : **17 tués sur 17** (M1 à M9 avec M8a et M8b, MG2-1 à MG2-7), témoin passant tout ; M10 et le sens de la garde restent déclarés équivalents |
| §12, `sortie/SHA256SUMS` | `b541b4f7…a9ee` | sha256 `eafde65e9233762f60d5cdaede2175cfd665bbee3833249680c5f88840eaadf7` (13 fichiers, 13 OK ; ancien archivé sous `essais/avant-correction-C1/`) |
| §7, tests de composition ; §13 | (4a) seul | (4a) et (4b) : `sim_niveau_oracle_r1.py --r1 … --sortie … --json <sim_niveau.json …>` sur toute sortie produite, dont celle de l'exécution du paquet |

- **Sortie A inchangée** : `sim_niveau.json` `d17c5121…350e` et `sim_niveau.txt` `7173a9ce…00eb` restent valides. a1 et a2 ont le sha du gel 2, que la sortie A porte dans `script_sha256`. `sim_niveau.py` n'importe que `sim_niveau_calc`, jamais l'adaptateur. Rejeu (1b) à 12 processus depuis une copie du gel 3 : JSON et texte identiques, à l'octet, à `sortie/oracle-1b/processus-12/` (`correction-C1/rejeu-1b-p12-gel3/`).
- **Ligne datée proposée pour l'annexe A, en remplacement de celle du §1** (acte de l'orchestrateur, C-2 du cp-1) : SIM-NIVEAU-b (2026-09-30, coupe R-25 du G1, correction C-1 du G2) : adaptateur d'oracle contre r1 et oracle (4b) (recalcul indépendant de chaque enregistrement ; invariants de comptes des sorties). Véhicule : `scripts/sim/sim_niveau_oracle_r1.py`. Oracles (4a) et (4b) aujourd'hui ; (4) au commit de B-DEP-1 (ORACLE4-1). Taille 196 [mesuré] ; lot : 148 + 190 + 196 = 534 lignes. cp-1 bref.
