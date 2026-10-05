**Gate 0 :** je tourne sous `claude-opus-5-5` (identifiant exact fourni par l'environnement).

# Contre-contrôle des corrections de la G2 de CB-18 (diffs CB-18g à CB-18q) : **NON-CONFORME**, liste fermée **CC-1 et CC-2**

Heures lues par `date -u` : début à 11:17:52 UTC, reprise après compactage à 11:28:27 (depuis `NOTES-CC.md`), fin à 12:11:46.

**Base.** Copie de 3164348 par `git archive`, avec les sept exclusions habituelles. La recette est vérifiée : `read-tree` puis `rm --cached` redonnent 44283521. J'ai appliqué ensuite les 9 diffs (SHA256SUMS : 232 OK), puis les 11 diffs (235 OK), par `git apply` sans décalage. L'arbre final vaut **199454e1**, comme attendu.

Les deux points relevés sont petits. Ils ne remettent en cause ni C-1 à C-3, ni les lettres du FORMAT, ni `--egal` sur S2, ni le recalage.

## Résumé, point par point

**1. C-1 à C-3 et adjudications : fermées.** Chacune a un test qui échoue sans elle. Méthode : les tests de l'état N lancés sur le code de N−1.
- **g :** 22 échecs et 2 erreurs, dont `test_budget_de_l_adr_a_la_borne`.
- **h :** 16 échecs (`test_regles_de_configuration_a_la_borne`).
- **i** (tests seuls) : avec un numéro de segment à un chiffre, `test_onze_redemarrages…` échoue ; les tests de h laissaient passer ce mutant.
- **j :** `test_convention_des_citations_et_run_params…` échoue.
- **k** (tests seuls) : sous MR-24, 2 échecs ; les tests de j laissaient passer ce mutant.
- **l :** `test_oracle_record` échoue 3 fois sur le code de k ; le runner de l plante sur le vérificateur de k (`etapes` absent).
- **m :** K-01 échoue sur le `gates.yml` de l.
- **n :** 3 échecs (64 et 65 niveaux).
- **o :** `test_paragraphe_7_1…` échoue.
- **p** (tests seuls, code inchangé, R-1) : sous le mutant `append`, 2 échecs.
- **q :** 7 échecs et 1 erreur.

Chaque état repasse au vert. Autres vérifications :
- **Jobs** (python3.12, borne de 300 s, réseau isolé) : job s2bis VIVANT au plancher exact à chaque état (e9 133, g 134, h 135, i 136, j 137, k 137, l 137, m 137, n 139, o 139, p 140, q 141). Job S2 : Ran 406 à e9, k, l, m et q. Job sim-bis : 93.
- **`sonde_budget.py` telle quelle :** `CONFIG/champ-absent` (tolerance).
- **Copie avec tolerance = 5 s :** délai 10 s admis (5+4+10+1 = 20). Délais 14, 15 et 16 refusés en `CONFIG/incoherent : budget`. À e9, 14 et 15 étaient admis.
- **`contournement_role.py`, copie avec `shell: bash`** :
  - C0 est enregistré en exit 0, avec K-02 ok.
  - C1 à C6 sont refusés par l'enregistreur et par K-02.
  - C7 est enregistré en exit 1 (plancher faux), avec K-02 ok.
  - L'outil tel quel voit tout refusé, puisqu'il écrit ses étapes sans `shell: bash`.
- **Mes mutants, classés par la commande du job :** MR-01 à MR-07, MR-10 à MR-23, MR-25 et MR-12b : 23 sur 23 tués. Portages MP-08, MP-09, MP-24 et MP-26 (cibles déplacées) : 4 sur 4 tués. Aucun FATAL.
- **C-3 :** `boucle.py` fait bien 132 lignes ; METRIQUES l.371 est corrigée.
- **Test du disque :** `statvfs` est injecté, avec des valeurs écrites à la main. Le test est déterministe.

**2. LIGNE-JOB-LEURRE-1.**
- **Analyseur unique :** la ligne est lue par un seul analyseur. `etapes` et `lignes_du_job` du vérificateur sont partagés par `cable()` (K-01 à K-03) et par `ligne_du_job`. L'enregistreur charge le vérificateur de l'arbre de l'outil. Mais K garde un second lecteur local, `job()`, qui contrôle par présence de texte : voir CC-1.
- **Runner :** 33 cas à e9, 57 à l, **58 à m** (L-22). Le « 33 → 57 » du rapport du worker est le compte de l. Les sections V, E et C sont identiques octet pour octet, aucun cas n'est retiré, 25 sont ajoutés, et K est plus strict.
- **20 leurres neufs** (`leurres_cc.py`, lancés sur le vrai `cable` et le vrai analyseur de sq) :
  - 10 sont refusés : `|-`, `|2`, `run: | # c`, scalaire continué par `|| true`, `run:` dont la valeur passe à la ligne suivante, étape en flux, séquence compacte, tabulation suivie de `set +e`, second document `---`, commentaire sur la clé du job. N-08 et N-09 sont toutefois lus par l'enregistreur (ENREG-FORME-JOB-1, déjà déclaré).
  - 2 relèvent du résidu « validité » : N-12, clé de job répétée entre guillemets (PyYAML garde la dernière ; comportement de la forge non vérifiable [abs]) ; N-14, U+001F (YAML invalide).
  - **8 sont admis : c'est CC-1.**
- **Analyseur, mutants CA :** **3 sur 12 survivent, et ne sont pas équivalents : c'est CC-2.**

**3. `--egal` sur le job S2 : le raisonnement est juste.**
- Les deux tests de `test_exclusion` (l.270-273 et 297-300) lèvent `SkipTest` dans leur corps : ils comptent dans Ran, variable posée ou non. `lancer` retire d'ailleurs la variable.
- Ran vaut 406 sous 3.10, 3.11, 3.12 et 3.13. Sous 3.10, la suite échoue (77 échecs, 3 erreurs), exactement comme à e0 et e9 (PY310-1).
- Le motif de l'inégalité (G1-DETTES-B1 §9) tenait à « ajouter des tests ne casse jamais le job ». Le couplage au test de comptes visait l'option du manifeste. L'ajout daté du G0 (l.38) fait suivre le compte au plancher, et `--egal` mécanise ce suivi.
- MR-25 est tué et L-22 refuse la ligne sans `--egal`.

**4. Lettres C-1 à C-5 du FORMAT : conformes.**
- **§7.1 :** il reproduit mot pour mot l'AVIS l.49-55 (comparaison à espaces normalisés : égalité). Le paragraphe qui suit type le `ws` des types non réservés, selon l'adjudication C-2 (« tous les champs du §1.3 et du §2 typés »). Les autres renvois (§1.2, §7.2 à §7.7, §8.3) pointent vers le §7.1 : c'est le seul lieu de la définition.
- **`_lire` applique exactement le §7.1.** Mon vérificateur indépendant, écrit d'après le seul FORMAT, a été comparé à `_lire` sur 1 795 fichiers altérés, tirés d'un journal à deux fichiers (ouverture, point, clôture, reprise avec queue, trous) : **0 désaccord**. Les issues sont celles attendues :
  - entiers de 640 chiffres admis, 641 refusés, signes compris ;
  - niveaux 64 admis et 65 refusés, en listes comme en objets ; un partage à 64 niveaux est admis ;
  - lignes de LIMITE octets admises, LIMITE+1 refusées ;
  - `queue` à `[]` ou null intègre, `queue` objet traité en queue ;
  - booléens refusés partout.
- **Ordre de `queue` :** quatre queues (04-0, 04-2, 04-10, 05-0) sont déclarées dans cet ordre, alors que `ls` place 04-10 avant 04-2. Le segment neuf est 05-1.
- **Imbrication :** une structure partagée `[a, a]` de 63, 100 ou 2 000 niveaux est refusée en `JOURNAL/imbrication` en 7 ms au plus ; un cycle est refusé en `JOURNAL/type`.
- **Noms :** 8 noms hors grammaire (00, 01, +1, espace, chiffre arabe-indien, mois sur un chiffre, double tiret, double extension) sont refusés à l'ouverture en `JOURNAL/nom`. L'écrivain est fermé, rien n'est écrit, le verrou est rendu.
- **§6.1 et §7.7 :** conformes à l'AVIS l.123-124, plus `JOURNAL/nom` chez l'écrivain.
- **§8.3 :** conforme à l'AVIS l.104, plus M = 4. J'ai vérifié qu'une `sante` SOA ou TXT atteint 6 niveaux.
- **§7.4 :** lettre C-3 (G2-RB18 l.199), plus l'ordre (jour, k), l'ordre d'écriture de l'écrivain, le test et le classement de l'avis (l.75).
- **Mes mutants neufs CM :** 18 sur 18 tués.

**5. Avis sur les observations du worker.**
- **O-1 :** juste. Le point (d) rend non intègre une `reprise` dont `queue` est un objet (je l'ai vérifié, et CM-04 est tué). L'incise au §7.4 lève l'ambiguïté sans toucher à la lettre ; elle est à adjuger avant RB-1 et RB-18 (appliquer le §7.1 avant le §7.4).
- **O-2 :** juste et sans effet en S2-bis. Je l'ai reproduit : `pool` est refusé à cause de `pool-x-2026-10-05-0.jsonl`, et le refus est asymétrique. L'item est utile, ou bien on écrit « un dossier par journal » au FORMAT.
- **O-3 :** juste pour 3164348. Mais RUPTURE-PORTEE-1 est inscrit à B.65 depuis 72aa806 et figure à 5f99ab5 : la citation se résout après recalage. LIRE-BOOLEENS-1 n'est inscrit nulle part. Plus largement, 7 items cités dans les ajouts ne sont pas inscrits à l'annexe B à 5f99ab5 (CITATIONS-ADR-DECALEES-1, CONFIG-REGLES-1, ENTIER-ECRIVAIN-1, LIGNE-JOB-LEURRE-1, LIRE-BOOLEENS-1, SEGMENTS-10-1, TEST-DISQUE-INSTABLE-1) : ils sont à inscrire, ouverts puis clos, au versement.

**6. Recalage sur 5f99ab5 : vérifié, avec une nuance pour xtask.**
- **Lignes +/- :** j'ai comparé chaque diff recalé à son original, fichier par fichier et dans l'ordre (pas seulement en multiensemble) : 0 écart. Seul le plancher s2bis change, N devient N+42. La base passe de 114 à 156 et 141 + 42 = 183.
- **SHA256SUMS** des 20 diffs recalés : 20 OK.
- **Arbre final :** recalculé dans mon propre clone nu partagé (index temporaire, `git apply --cached` exact). Il vaut **f342a14b**, comme annoncé.
- **Fichiers :** 21 des 23 fichiers touchés sont identiques à sq octet pour octet.
  - `gates.yml` ne diffère de la tête que par CB-18m et 156 → 183 ; le plancher sim-bis 129 est intact.
  - METRIQUES : les 406 lignes ajoutées sont identiques et dans le même ordre, placées après les sections RB.
- **Jobs sur f342a14b** (extraction contrôlée, f1aa47a0) : s2bis Ran **183**, sim-bis 129, S2 406 avec `--egal` ; runner à 58 ok. Témoin 5f99ab5 : 156, 129 et 405.
- **États intermédiaires :** j'ai lancé le job s2bis sur les **20 états recalés** : tous VIVANT à leur plancher, de 159 à 183.
- **xtask, sur f342a14b, 5f99ab5, sq et e9 :** S-G1 à S-G8, fmt, no_std et clippy sont VERT. S-G9 est ROUGE pour `docs/17-modele-de-menace.md:70` seul (connu). Le verdict global est donc ROUGE pour cette seule raison, identique aux témoins. « VERT » ne vaut qu'au sens du brief, S-G9 connu mis à part.

## CC-1 : runs-on et checkout ne sont contrôlés que par présence de texte (la classe du leurre C1)

Ces leurres sont acceptés par K-01, K-02 et K-03. Le docstring de `cable()` (CB-18l) affirme pourtant que l'analyseur contrôle « trois étapes, le checkout, le runner seul ». En réalité :
- l'étape 1 doit seulement être non admise ;
- `runs-on: ubuntu-24.04` et le checkout épinglé ne sont vérifiés que par `e in l[:k[0]]`, sur des lignes dépouillées de leur indentation.

Une ligne cachée dans un `name: >` ou dans le `with:` du checkout suffit donc. Preuve : `preuves/leurres-sq.txt`, avec la lecture de PyYAML. Sur le runner réel de sq, ces leurres donnent 58 ok (`preuves/leurres-runner-reel.txt`).
- **N-01, N-04, N-17 :** `runs-on` vaut réellement ubuntu-latest, macos-15 ou windows-latest.
- **N-02, N-18, N-20 :** checkout réel en `@v4`, `tiers/action@main` ou `@main`.
- **N-03 :** l'étape 1 est un `run` en `shell: sh` qui clone le dépôt et réécrit `verdict-suite-s2.py` : la suite est neutralisée.
- **N-19 :** même leurre que N-01, sur K-01.

Cette classe est antérieure au lot : à e9, K-02 et K-03 admettent déjà ces leurres. L'enregistreur n'est pas trompé, car il lance lui-même la ligne.

**Remède, au choix de l'orchestrateur :**
- **(a)** contrôler les ETAPES sur les lignes brutes, à indentation exacte. Ma preuve de faisabilité tient en 5 lignes (`preuves/poc-remede-cc1.diff`) : le runner reste à 58 ok, et les 8 leurres sont refusés (`poc-remede-cc1.txt`). On y ajoute N-01 et N-02 comme cas L.
- **(b)** corriger le docstring de `cable()` et former l'item SHOGEN-S2BIS-K-ETAPES-LEURRE-1, avec pour déclencheur le moment où la forge lancera les jobs.

## CC-2 : trois refus de l'analyseur ne sont figés par aucun cas

Trois mutants de l'analyseur survivent à la commande du job : la sortie est 0, et le runner comme la suite passent.
- **CA-01 :** `env` ajouté à PREMIER. L-19 ne teste que la forme `env :`, avec une espace.
- **CA-07 :** clé de job répétée admise.
- **CA-12 :** des étapes sont lues hors de `steps`.

Aucun n'est équivalent :
- un `env:` simple de premier niveau est refusé à sq et admis sous CA-01 (`preuves/ca01-env-premier-niveau.txt`) ;
- un `runs-on` répété est refusé à sq et admis sous CA-07 (PyYAML retient macos-15) ;
- sous CA-12, un `name: >` à l'indentation 6 qui imite une étape fait lire à `lignes_du_job` la ligne leurre pendant que la vraie étape lance `--plancher 0` : le leurre de type C1 contre l'enregistreur revient (`preuves/ca07-ca12-non-equivalents.txt`).

**Remède :** trois cas. Ma preuve (`preuves/poc-remede-cc2.diff`) ajoute L-23 (`env: {PATH: leurre}`), L-24 (`runs-on` répété) et A-03 (`etapes` égal à `[]` sur les étapes imitées). Le runner passe à 61 ok, et chaque cas tue son mutant (`poc-remede-cc2.txt`).

Bilan des mutants neufs : CM 18 sur 18 tués, CA 9 sur 12, MP 4 sur 4. Au total, 31 tués, 3 vivants, 0 FATAL (`preuves/mutants-CC-sq.txt`).

## Items à former (PAROXYSME), propriétaire : l'orchestrateur
- SHOGEN-S2BIS-K-ETAPES-LEURRE-1, si le remède (b) de CC-1 est retenu.
- Étendre ANALYSEUR-RESIDUS-1 à N-12 (clé de job répétée entre guillemets ; refus de la forge [abs]) et à N-14.
- O-3 : inscrire les 7 items cités.

## Écarts déclarés
- **E-1 :** mes outils (`verif71_cc.py`, scénarios d'ordre, O-2 et noms) ont lu des `pool-….jsonl` synthétiques, écrits par l'écrivain dans mon TMPDIR. La lettre « tout *.jsonl » les couvre. Aucun journal d'exemple de RB-18, aucune pièce D.2, aucun journal de session n'a été lu.
- **E-2 :** mon outil de leurres importe PyYAML 6.0.1, déjà installé au système (dist-packages), en lecture seule et hors dépôt. Rien n'a été installé.
- **E-3 :** les arbres recalés contiennent `recalc/lecteur.py`. Je ne l'ai jamais ouvert ; il n'a tourné que par la suite s2bis, lancée par la commande du job.
- **E-4 :** j'ai listé à un seul niveau, sans récursion, `docs/` et `docs/adr-0028` de ma copie pour retrouver les exclusions. J'ai aussi lancé un `grep -r --include=*.py` sur `s2bis/` de la copie (sans `recalc/`). Aucune recherche récursive n'a porté sur `docs/`, sur le dépôt ou sur le scratchpad.
- **E-5 :** mon premier leurre CA-12 affaiblissait la mauvaise ligne. Je l'ai corrigé et relancé ; seule la sortie corrigée est versée.

## Journal G1
- **[lu] :**
  - pièces du lot : brief du contre-contrôle 64f702a4 (entier) ; brief des corrections bfca4aff (entier) ; rapport du worker 06114b41 (entier, §1, §3, §4 et §9 relus) ; AVIS-FORMAT 6daf4065 (entier) ; ADJUDICATION e6528325 (entier) ; G2-RB18 1ddabaee (l.68-202) ; ma G2 ce9e2a11 ; `rebaser_p1c.py` 0d4431f3 (entier) ; SHA256SUMS : cb18 3641e431, corr ddd515b5, rebase eb39992b ;
  - code de sq : `journal.py`, `verdict-suite-s2.py` et le runner (entiers) ; `oracle_record.py` (l.1-54, 101-124, 151-212) ; `gates.yml` (l.39-77, 146-244) ; `test_exclusion` 89c6d894 (l.264-310) ; `test_sante` (l.63-87) ; FORMAT e459f6f9 (l.1-82, 109-262, 378-477) ; runner de e9 (l.100-146) ;
  - documents : G1-DETTES-B1 61c9b86d (l.205-235) ; G1-B-SEG-1 49ccdc79 (par grep) ; G0-D8a a5d70848 (l.436) ; G0-DETTES 868f9fff (l.38) ; G2-P1A 736455ae (l.290-310) ;
  - ADR-0029 : titres à e16956b, eb518b3, b9ba2b4, 435fa12 et 3164348 ; lignes 107, 109, 233, 234 et 238-240 à e16956b ; diff b9ba2b4 ;
  - annexe B à 3164348, 72aa806 et 5f99ab5 (f7cf4cd5, B.60).
- **[abs] :** `lecteur.py` et la contre-épreuve de RB-18, les `*.jsonl` d'exemple, les pièces D.2, les dossiers exclus, les dossiers `preuves/` et `mutants/` du worker (non lus : tout a été rejoué), le comportement de la forge.
- **[2nd] :** aucun ; tous les chiffres sont recomptés.
- **PID réels, tous terminés :** 4424, 4440, 22122, 22274, 30788, 3671, 9376, 11855, 23574 et 1146.
- **Après tous les runs :** empreintes inchangées (sq 199454e1, fin f1aa47a0).
- **R-13 :** 0 occurrence sur 908 lignes ajoutées, avec le motif lu dans les octets de `gates.yml` (a1a6e684) ; contrôle positif 2 sur 2.
- **Octets 92 :** 0 ajouté dans les 11 diffs ; 2 retirés dans l, où `\.` devient `[.]`.
- **Dépendances (R-8) :** seulement `importlib.util` et des modules de test internes.
- **Nettoyage :** copies, clone, cible cargo et TMP supprimés ; le dossier `cc` fait 2,4 Mo.

## Fichiers
- `<scratchpad>/s2bis/cb18/cc/SHA256SUMS` (143 entrées, 143 OK, sha256 a0e80745…)
- `<scratchpad>/s2bis/cb18/cc/travail/NOTES-CC.md`
- `<scratchpad>/s2bis/cb18/cc/travail/outils/` (`leurres_cc.py`, `verif71_cc.py`, `mutants_cc.py`, `compare_rebase.py`, `rouges_cc.py`…)
- `<scratchpad>/s2bis/cb18/cc/travail/preuves/` (dont `poc-remede-cc1.diff`, `poc-remede-cc2.diff`, `rebase-*.txt` et `.log`, `xtask-*-verdicts.txt`)
- `<scratchpad>/s2bis/cb18/cc/travail/leurres/` (les 20 `gates.yml` leurres)
