# Contre-contrôle neuf de GARDE-FOUS-ORCH phase 1 (R-1 à R-10) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 20:10:04 UTC du fichier garde-fous/gf1/g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle du lot GARDE-FOUS-ORCH, phase 1 (gabarit du lot, GF-9b)

Modèle résolu : `claude-opus-5-5` (identifiant déclaré par l'environnement), effort max (fiche) ; base de la copie :
`8d19a0e53536f186c16986ad50434363b0efeb97` (`git rev-parse`, tête de `claude/compassionate-noether-szmdyj` à 10:58:50
UTC), relue à la fin : `6409d90` (§8) ; heures lues par `date -u`. Rédigé le 2026-10-15 à partir de 12:00:11 UTC.
Contre-contrôleur neuf : je n'ai ni écrit ni relu ce lot. Brief `cc/BRIEF-CC.md` (sha256 `ea705e7f…`).

Pièces (sha256, huit caractères) : `ADJUDICATION.md` `c4dd2ebb` (ajout du 2026-10-15 10:57:57 compris) ;
`ERREURS-ORCHESTRATEUR.md` `216ce860` (E1 à E27) ; `g2/RAPPORT-G2.md` `a5809e40` ; `g2/NOTES.md` `04412ffd` ;
`gf1/RAPPORT-GENERATEUR.md` `1c511b88` ; `g2/BRIEF-G2.md` `2f723718` ; `gf1/bloc-commun-brouillon.md` `ff3c02b7` ;
`g2/SHA256SUMS` `298478f4` et `gf1/SHA256SUMS` `f49f733b`, rejoués par `sha256sum -c` : conformes (129 et 21 lignes).

Copie : `git archive` de la base avec les exclusions des interdits et de `*.jsonl`, dépôt jetable à moi, un commit de
base puis un commit et une étiquette par diff, dans l'ordre de la chaîne : GF-0 à GF-10b, C-1 à C-12, C-14 à C-18
(36 commits ; tête jetable `e9c2074`), puis mes réserves R-1 à R-10. Aucune écriture dans le dépôt du projet, aucun
réseau (outils sous `isole.sh`, sans variables de mandataire), `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucun
emplacement interdit ouvert ni listé. Journal de la passe : `cc/NOTES.md` ; scripts : `cc/outils/`, `cc/sondes/`,
`cc/ecrire/` ; sorties : `cc/tmp/` ; mutants : `cc/mutants/` ; réserves : `cc/propose/`.

## Verdict

**CONFORME-AVEC-RÉSERVES (R-1 à R-10).** Les dix-huit corrections sont justes : chaque correction de code a son test
rouge d'assertion (FAIL, jamais ERROR) sur l'état d'avant et vert sur le sien (19 rouges, §1) ; le bout en bout de C-1
et les rejeux réels de C-3 et C-16 donnent ce que la G2 annonce ; aucune ne porte de défaut neuf qui casse un acte
juste. Chaque état de la série et des corrections est vert seul à la ligne exacte du job `controle-unittest`, `Ran`
égal au plancher (36 états, tableau de la série). 25 mutants joués sur l'état final (K-28 à K-30 de la G2, M-01 à
M-22 à moi) : 25 tués, 0 vivant, 0 FATAL. Gates de la copie finale vertes, S-G9 rouge attendu sur copie creuse (§5).

Réserves : dix formes voisines des cas réels passent encore ; chacune a sa forme exacte, éprouvée (rouge sur l'état
d'avant, vert après, ligne du job au plancher exact, `avant_acte.py diff` en sortie 0) : `propose/R-n.diff`, à poser
après C-18 dans l'ordre R-1 à R-10 (§3). Les plus lourdes : R-2 (un `docs/15-*` passe au distant par l'historique de
la plage), R-5 (un pas du plan sauté sans rien dire, chaîne en sortie 0), R-6 (une étape rouge de `gates.yml` écrite
`- run:` laisse sceller et commettre), R-8 (le crochet GARDE-FAITS du dépôt refuse les commandes des skills telles
qu'écrites), R-1 (GF-0 contredit l'adjudication du 2026-10-10 14:09:16 et la liste E1 à E27).

## Série rejouée diff par diff

Ligne exacte du job `controle-unittest`, lue dans le `gates.yml` de chaque état, sous `isole.sh` (`outils/etats.sh` ;
`tmp/etats-tous.txt`, `tmp/etats-r.txt`) ; `avant_acte.py diff` (outil C-18) sur chaque diff, dans un dépôt jetable
dont la tête est la base du diff (`outils/rejeu_diff.sh`) ; cargo et gates complètes sur l'état C-18 (§5).

| diff | appliqué sur le précédent | vérification (lignes de `gates.yml`, cible cargo par défaut) | verdict |
|---|---|---|---|
| base `8d19a0e` | — | Ran 37 = plancher | vert |
| GF-0 | oui | Ran 37 = 37 ; `diff` 0 | vert seul |
| GF-1 | oui | Ran 43 = 43 ; `diff` 0 | vert seul |
| GF-4 | oui | Ran 48 = 48 ; `diff` 0 | vert seul |
| GF-2 | oui | Ran 49 = 49 ; `diff` 0 | vert seul |
| GF-2b | oui | Ran 53 = 53 ; `diff` 0 | vert seul |
| GF-3 | oui | Ran 56 = 56 ; `diff` 0 | vert seul |
| GF-4b | oui | Ran 57 = 57 ; `diff` 0 | vert seul |
| GF-5 | oui | Ran 60 = 60 ; `diff` 0 | vert seul |
| GF-5b | oui | Ran 63 = 63 ; `diff` 0 | vert seul |
| GF-6 | oui | Ran 67 = 67 ; `diff` 0 | vert seul |
| GF-6b | oui | Ran 70 = 70 ; `diff` 0 | vert seul |
| GF-7 | oui | Ran 72 = 72 ; `diff` 0 | vert seul |
| GF-8 | oui | Ran 75 = 75 ; `diff` 0 | vert seul |
| GF-8b | oui | Ran 77 = 77 ; `diff` 0 | vert seul |
| GF-9 | oui | Ran 82 = 82 ; `diff` 0 | vert seul |
| GF-9b | oui | Ran 86 = 86 ; `diff` 0 | vert seul |
| GF-10 | oui | Ran 88 = 88 ; `diff` 0 | vert seul |
| GF-10b | oui | Ran 89 = 89 ; `diff` 0 | vert seul |
| C-1 | oui | Ran 90 = 90 ; `diff` 0 ; bout en bout (§1) | vert seul |
| C-2 | oui | Ran 91 = 91 ; `diff` 0 | vert seul |
| C-3 | oui | Ran 94 = 94 ; `diff` 0 ; rejeux DT14, DT6-d (§1) | vert seul |
| C-4 | oui | Ran 95 = 95 ; `diff` 0 | vert seul |
| C-5 | oui | Ran 96 = 96 ; `diff` 0 | vert seul |
| C-6 | oui | Ran 97 = 97 ; `diff` 0 | vert seul |
| C-7 | oui | Ran 98 = 98 ; `diff` 0 | vert seul |
| C-8 | oui | Ran 99 = 99 ; `diff` 0 | vert seul |
| C-9 | oui | Ran 100 = 100 ; `diff` 0 | vert seul |
| C-10 | oui | Ran 101 = 101 ; `diff` 0 | vert seul |
| C-11 | oui | Ran 102 = 102 ; `diff` 0 | vert seul |
| C-12 | oui | Ran 103 = 103 ; `diff` 0 | vert seul |
| C-14 | oui | Ran 103 = 103 ; `diff` 0 | vert seul (réserve R-1) |
| C-15 | oui | Ran 103 = 103 ; `diff` 0 | vert seul |
| C-16 | oui | Ran 104 = 104 ; `diff` 0 ; rejeux DT6-d, DT5-22 (§1) | vert seul |
| C-17 | oui | Ran 105 = 105 ; `diff` 0 | vert seul |
| C-18 | oui | Ran 107 = 107 ; `diff` 0 ; 16 étapes de gates, matrice, cargo (§5) | vert seul |
| R-1 | oui | Ran 107 = 107 ; `diff` 0 (outils C-18 et R-10) | vert seul |
| R-2 | oui | Ran 108 = 108 ; `diff` 0 | vert seul |
| R-3 | oui | Ran 109 = 109 ; `diff` 0 | vert seul |
| R-4 | oui | Ran 110 = 110 ; `diff` 0 | vert seul |
| R-5 | oui | Ran 111 = 111 ; `diff` 0 | vert seul |
| R-6 | oui | Ran 111 = 111 ; `diff` 0 | vert seul |
| R-7 | oui | Ran 112 = 112 ; `diff` 0 | vert seul |
| R-8 | oui | Ran 113 = 113 ; `diff` 0 | vert seul |
| R-9 | oui | Ran 114 = 114 ; `diff` 0 | vert seul |
| R-10 | oui | Ran 115 = 115 ; `diff` 0 ; matrice, 12 étapes de gates (§5) | vert seul |

Ajouts datés du README recomptés à chaque état (`outils/recompte.py`, `tmp/recompte.txt`) : chaque sha256 cité égale
le fichier nommé à cet état, chaque compte de tests égale les `def test_` du fichier, chaque plancher égale la ligne
du job : 0 écart, de GF-1 à R-10.

## Groupes de commit

Un diff rouge seul, vert avec un autre, forme un groupe avec lui : la chaîne commet le groupe en un seul pas. Ligne
fixe, lue par `avant_acte.py chaine` avant tout pas (erreur E11), une seule par rapport : `aucun` si chaque diff est
vert seul, sinon les groupes. Ici chaque diff de la série, des corrections et des réserves est vert seul (tableau
ci-dessus).

Ligne lue par l'outil lui-même : `avant_acte.py chaine --plan <45 pas : série, corrections, réserves> --cc
RAPPORT-CC.md --detache` : sortie 0 avec l'outil C-18 et avec l'outil R-10 (`tmp/plan-45.txt`) ; en lancement lié :
`REFUS G3 : durée estimée 270 min (45 pas × 6 min)` : la chaîne se lance détachée, délai que l'outil donne (32400 s).
Ce rapport passé à `avant_acte.py publier` (outils C-18 et R-10) et à `presg5.py` : sorties 0.

GROUPES : aucun

## 1. Corrections C-1 à C-18

Rouge et vert (`outils/rouges.sh`, `tmp/rouges.txt`) : les tests de l'état C-n posés sur le code de l'état d'avant,
seuls les tests nouveaux (ou changés) de C-n lancés : 19 FAIL d'assertion sur 16 corrections de code, jamais
ERROR ; 19 verts sur leur état (18 tests distincts : `test_c1_verif_reelle` sert C-1 et C-15).

| C-n | test(s) | rouge sur l'état d'avant | vert | défaut neuf |
|---|---|---|---|---|
| C-1 | `test_c1_verif_reelle` | FAIL sur GF-10b | oui | aucun ; R-6 (étape `- run:`, antérieure) |
| C-2 | `test_c2_branche_autre_que_la_tete` | FAIL sur C-1 | oui | aucun ; R-2 (historique, antérieure) |
| C-3 | `test_c3_prefixes_de_la_configuration`, `test_c3_etat_d_apres_le_diff`, `test_c3_format_du_diff` | 3 FAIL sur C-2 | oui | aucun (limite LN-3) |
| C-4 | `test_c4_actes_voisins_et_sources` | FAIL sur C-3 | oui | aucun ; R-3 (formes voisines restantes) |
| C-5 | `test_c5_reference_en_code` | FAIL sur C-4 | oui | aucun |
| C-6 | `test_c6_casse_et_dossiers` | FAIL sur C-5 | oui | aucun |
| C-7 | `test_c7_noms_du_plan_et_gabarit` | FAIL sur C-6 | oui | aucun ; R-5 (doublon, antérieure) |
| C-8 | `test_c8_racine_et_parcours` | FAIL sur C-7 | oui | aucun ; R-7 (racines voisines) |
| C-9 | `test_c9_journal_en_erreur` | FAIL sur C-8 | oui | aucun |
| C-10 | `test_c10_racine_interdite` | FAIL sur C-9 | oui | aucun |
| C-11 | `test_c11_plages` | FAIL sur C-10 | oui | aucun ; R-9 (date en code) |
| C-12 | `test_c12_documents_cites_par_docs17` | FAIL sur C-11 | oui | aucun ; R-4 (retrait d'un cité) |
| C-13 | texte (brouillon GF-20) | — | — | aucun (ci-dessous) |
| C-14 | aucun (texte de GF-0) | — | — | **R-1** : texte périmé |
| C-15 | `test_c1_verif_reelle` (changé) | FAIL sur C-14 | oui | aucun |
| C-16 | `test_c16_passe_n_des_sources` | FAIL sur C-15 | oui | aucun (L-3 demeure) |
| C-17 | `test_c17_diff_id_deja_porte` | FAIL sur C-16 | oui | aucun ; R-5 |
| C-18 | `test_c18_chargement_et_sortie`, `test_c18_installation_abimee` | 2 FAIL sur C-17 | oui | aucun |

**Bout en bout de C-1** (`outils/essai_c1.sh`, `tmp/essai-c1.txt`) : modèle `gabarits/chaine.sh` de l'état donné,
projet jetable, cargo factice, ligne de `gates.yml` factice au format réel (`- name:` puis `run:`). GF-10b : xtask
ROUGE, cargo test rouge, ligne rouge : chaîne en sortie 0 et un commit `Diff-Id: X-1` chaque fois (défaut reproduit).
C-1 et C-18 : sortie 1, `vérification rouge avant X-1 : arrêt, rien de commis`, aucun commit ; tout vert : sortie 0,
un commit. Mon premier essai portait une ligne `      - run: python3 -B enforcement/porte.py` : jamais lancée par
`verif` (d'où R-6).

**Rejeux réels de C-3** (`outils/rejeu_diff.sh` ; `tmp/rejeu-dt14-c3.txt`, `tmp/rejeu-dt14-origine-dt6.txt`) :
DT14 commis (a à m) sur `dda4bbc` : outil GF-10b, DT14-a sortie 1 (56 `REFUS G5`), DT14-b sortie 1 (9 `REFUS G5`),
65 faux refus ; outil C-18 : 0 partout. DT14 d'origine (a à l) sur `dda4bbc`, outils GF-10b et C-18 : DT14-e sortie 1
(`REFUS C7`, `docs/adr-0028/ADR-0028-decisions-sortie-S2.md`, ligne 36), DT14-g sortie 1 (`REFUS C7`,
`docs/17-modele-de-menace.md`, ligne 8) : E21 réel tenu. DT6-d sur `a59eaa2` : 0 avec les deux outils.

**Rejeux réels de C-16** (`outils/rejeu_commit.sh`, `tmp/rejeu-commits.txt`) : commit DT6-d (`8575186`, source
`s2bis/dettes6/ADJUDICATION.md`, `f3f60996…`) : outil C-15, sortie 1, `REFUS C3 : nombre de passes du message absent
des sources : 2 (E8)` (faux) ; outils C-16 et C-18 : sortie 0. Commit DT5-22 (`0838597`, message `en trois passes`,
source `534204fe…`) : sortie 1 avec C-15, C-16 et C-18 (E8 réel tenu).

**C-13** (texte de GF-20, `git apply` sur une copie du brouillon : `37081729…`) : la phrase de
`.claude/agents/shogen-orchestrator.md` §4 (l.84 à 86) est reprise mot pour mot, minuscule initiale comprise ; mutants
bornés, `git archive` avec exclusions, ligne g3 adjugée le 2026-10-10 à 08:19:22 avec sa source, taille du diff
(25 lignes de bloc, 6 fiches) et retrait du point 4 de `shogen-avant-lancer` : justes.

**C-14** : juste à sa date, périmé aujourd'hui (réserve R-1).

## 2. Contournements, règle par règle

Sondes sur l'état C-18 (`sondes/sonde1.py`, `sonde2.py`, `sonde3.py`, `essai_chaine.sh`, `sonde_crochet.py` ;
`tmp/sonde1.txt`, `sonde2.txt`, `sonde3.txt`, `essai-chaine.txt`, `sonde-crochet.txt`).

| règle | formes voisines éprouvées | issue |
|---|---|---|
| heures (C4) | `AAAA-MM-JJTHH:MM:SSZ` : refus ; date du jour en code et heure hors du code : **0** ; heure en code : 0 (masque voulu : extraits de journal) | **R-9** ; lendemain, sans date, autres écritures : L-1 |
| citations (C5) | forme stricte à chemin introuvable (faute de frappe, casse) : avertissement seul, sortie 0 ; citation d'un fichier que le même diff retire : lue dans l'arbre d'avant | limites LN-2, LN-3 (conception GF-3) |
| lignes citées (C7) | fichier cité retiré : `commit` 0, `diff` 0 ; renommé : `commit` 0, `diff` 0 | **R-4** ; remplacement à nombre égal : L-13 |
| commit (C1 à C9) | verdict `CONFORME-AVEC-RÉSERVES` (celui du gabarit de contre-contrôle) au message contre des sources `NON-CONFORME` : 0 | **R-10** ; `passe 3`, `troisième passe`, minuscules : L-3 |
| poussée (P2) | `docs/15-*` ajouté puis retiré dans la plage, tête scellée sans lui : 0 (référence distante, et branche neuve) | **R-2** |
| poussée (P4) | `git -C … push origin -d b`, `git -C … push origin --delete b`, `':b'`, `+:b`, `":refs/heads/b"`, `-X  DELETE`, `-X 'DELETE'`, `--method "PUT"`, DELETE et POST sur la protection : 0 (dix formes) ; `curl -X DELETE …/git/refs/…` : refus | **R-3** ; outils MCP, alias : L-7 |
| chaîne | `Diff-Id` en double au plan : `chaine` 0, modèle 0 et `FIN`, second pas `déjà commis` et jamais commis ; étape `- run: python3 -B enforcement/rouge.py` : non lancée, commit fait | **R-5**, **R-6** ; disque contrôlé au seul départ : LN-1 |
| verser | `--pieces /root`, `/usr` (os.walk remplacé par un témoin, rien de lu) : parcours lancé ; `/tmp` refusé ici parce que mes dépôts y étaient | **R-7** ; copie retouchée : L-14 |
| interdits | 16 formes interdites (casse, `//`, `..`, lien, `*.JSONL`, composant `.jsonl`, copie sous un autre dossier) : interdites ; 6 admis sur 7 admis : le septième, `journal.jsonl.txt`, jugé interdit (motif de D.2, sens sûr, jamais affiché) | aucune forme qui passe ; LN-5 |
| crochet du dépôt | voir §6 | **R-8** |

## 3. Réserves R-1 à R-10 (forme exacte)

Diffs de l'état d'avant à l'état R-n (R-1 depuis C-18), écrits par `ecrire/reserves.py` (remplacements exacts, heure
lue par `date -u`, sha256 relus, tests comptés), `git diff` limité à une liste explicite de chemins ; C-18 puis R-1 à
R-10 appliqués dans un index temporaire donnent l'arbre de R-10 (`a9d7998f…`). Rouge d'assertion sur l'état d'avant,
vert sur le sien (`outils/rouges_r.sh`, `tmp/rouges-r.txt`) ; ligne du job au plancher exact (`tmp/etats-r.txt`) ;
`avant_acte.py diff` en sortie 0 avec l'outil C-18 et l'outil R-10 (`tmp/verif-r.txt`) ; aucune ligne neuve de plus
de 120 caractères. Concaténation des dix diffs, dans l'ordre :
`e30fa54cf96d31b2fd7989b7aba347d4490464a612ba7f3a57c96cf254626693`.

| R-n | forme voisine qui passait (cas réel) | forme exacte | test (rouge → vert) | lignes | plancher | sha256 |
|---|---|---|---|---|---|---|
| R-1 | GF-0 (C-14) écrit `E1 à E25` (la liste versée porte E26, E27) et décrit la phase 2 « non engagée », sous accord de l'investisseur, que l'ajout du 2026-10-10 14:09:16 décide (E8 dans le lot) | `docs/adr-0028/G0-lots-DETTES.md` : `E1 à E27`, puce Phase 2 récrite d'après l'ajout de 14:09:16, heure relue ; six lignes à nombre égal (C7 admis) | — (texte) | 6 | 107 | `c1122ba8` |
| R-2 | `docs/15-*` ajouté puis retiré dans la plage poussée (ADR-0028 l.293 : préfixes sans ces fichiers) | P2 juge aussi `git rev-list -n 1 HEAD --not --remotes=NOM -- <chemins>` | `test_r2_historique_de_la_plage` | 34 | 108 | `711230b6` |
| R-3 | dix écritures voisines des actes de B.92 et B.95 (`git -C … push -d`, guillemets, blancs, `+:b`, DELETE et POST de la protection) | guillemets et blancs ramenés, options de git ôtées avant les motifs ; cinq motifs ajoutés à `garde/hors-distant.txt`, en fin | `test_r3_actes_ecrits_autrement` | 43 | 109 | `6928c3f3` |
| R-4 | fichier cité par numéro retiré ou renommé (E21 : renvois qui ne mènent plus nulle part) | C7 refuse ; voulu : `Décalage admis : <chemin>` | `test_r4_fichier_cite_retire_ou_renomme` | 36 | 110 | `436c784d` |
| R-5 | deux pas du plan au même `Diff-Id` : le second sauté, chaîne en sortie 0 (LA-N04, E11) | `chaine` G4 refuse un `Diff-Id` porté par plus d'un pas | `test_r5_diff_id_en_double_au_plan` | 27 | 111 | `8d65556d` |
| R-6 | étape rouge écrite `- run: python3 -B enforcement/…` non lancée par `verif` : sceau et commit (LA-N05) | motif et `sed` de `verif` étendus à `- ` | `test_c1_verif_reelle` (pas `tiret`) | 14 | 111 | `dca44971` |
| R-7 | `verser --pieces /root` ou `/usr` (voisine de `/`, C-8) : parcours et lecture entiers, extraits de `.md` imprimés aux refus (E19) | fichiers et octets comptés avant toute lecture ; erreur 3 au-delà de 5000 fichiers ou 512 Mio | `test_r7_dossier_trop_grand` | 31 | 112 | `d2ac5576` |
| R-8 | commandes des skills refusées par le crochet GARDE-FAITS (R3) telles qu'écrites (§6) | `git diff --cached --stat`, `git log --oneline origin/<b>..HEAD`, `git status --short` en tête des points concernés | `test_r8_crochet_garde_faits` (vrai crochet, journal synthétique) | 57 | 113 | `beb237b0` |
| R-9 | date du jour en code, heure future hors du code (E14) | dates lues sur la ligne écrite, heures sur la ligne masquée ; extrait de la ligne écrite | `test_r9_date_en_code` | 21 | 114 | `efd64eaf` |
| R-10 | verdict `CONFORME-AVEC-RÉSERVES` jamais lu par C3 (message ni sources) (E8) | verdict ajouté, accentué ou non, comparé sous une forme | `test_r10_verdict_avec_reserves` | 27 | 115 | `9c691222` |

Total : 296 lignes ajoutées, chaque diff sous 200 (R-25). L'outil R-10 ne change aucune sortie juste : les 45 diffs
(série, corrections, réserves) sur `67061e7` (`tmp/tete-outil-R-10.txt`), DT14 commis (a à m) sur `dda4bbc`, DT6-d
sur `a59eaa2` : sortie 0 ; commit DT6-d : 0 ; commit DT5-22 : refusé, E8 réel (`tmp/rejeux-r10.txt` ; mêmes sorties
avec l'outil R-9, `tmp/rejeux-r9.txt`). R-1 se rattache à C-14 (même ajout daté de GF-0) ; si l'orchestrateur préfère
refaire C-14, la forme est la même.

## 4. Mutants

Banc `outils/banc_cc.py` (remplacement exact présent une fois, base verte exigée, ligne exacte du job lue dans le
`gates.yml` de la copie, groupe de processus tué au délai, fichier relu par sha256 après restauration, `isole.sh`,
sans mandataire, relevé `ps`) ; sortie 1 tué, 0 vivant, toute autre FATAL ; copie tirée de l'étiquette C-18 ;
`mutants/mutants_cc.py`, journal `mutants/cc.log`. Aucun mutant ne touche une racine de parcours ni un contrôle
d'interdit éprouvé sur un vrai chemin (le test de C-8 remplace `os.walk` par un témoin).

| mutant | cible | issue | test qui tue |
|---|---|---|---|
| K-28 (G2) | C-16, négation ignorée | tué | `test_c16_passe_n_des_sources` |
| K-29 (G2) | C-16, `passe N` des sources ignoré | tué | `test_c16_passe_n_des_sources` |
| K-30 (G2) | C-17, G4 retiré | tué | `test_c17_diff_id_deja_porte` |
| M-01 à M-04 | C-1 : verdict de xtask, `< /dev/null`, `done || exit 1`, cargo test rouge | 4 tués | `test_c1_verif_reelle` |
| M-05 | C-15 : `CARGO_TARGET_DIR` hérité | tué | `test_c1_verif_reelle` |
| M-06 | C-2 : P3 retiré | tué | `test_c2_branche_autre_que_la_tete` |
| M-07, M-08 | C-3 : corpus de HEAD, citations sans surcouche | 2 tués | `test_c3_etat_d_apres_le_diff` |
| M-09 | C-4 : actes non ramenés | tué | `test_c4_actes_voisins_et_sources` |
| M-10 | C-6 : casse et dossiers | tué | `test_c6_casse_et_dossiers` |
| M-11 | C-7 : noms de GROUPES | tué | `test_c7_noms_du_plan_et_gabarit` |
| M-12 | C-8 : ancêtres admis | tué | `test_c8_racine_et_parcours` |
| M-13 | C-9 : journal en erreur rendu 1 | tué | `test_c9_journal_en_erreur` |
| M-14, M-15 | C-18 : module frère en 1, vidage final retiré | 2 tués | `test_c18_chargement_et_sortie` |
| M-16 | C-18 : `presg5`, erreurs hors `OSError` | tué | `test_c18_installation_abimee` |
| M-17 | C-10 : racine non jugée | tué | `test_c10_racine_interdite` |
| M-18 | C-5 : référence en code | tué | `test_c5_reference_en_code` |
| M-19, M-20, M-22 | C-11 : fenêtre de 25 caractères, `X` majuscule, tolérance | 3 tués | `test_c11_plages` et d'autres |
| M-21 | C-12 : `CLAUDE.md` retiré de la liste | tué | `test_c12_documents_cites_par_docs17` |

Bilan : base `Ran 107`, 25 joués, 25 tués, 0 vivant, 0 FATAL, 0 non appliqué, 0 processus restant. Aucun équivalent
déclaré. Plancher exact (`--egal`) : tableau de la série, 36 états de la série et des corrections, dix états des réserves.

## 5. Gates de la copie finale (état C-18)

Copie de gates : archive de l'étiquette C-18 avec exclusions, un commit, `objects/info/alternates` vers les objets du
projet en lecture (sim-bis lit `f35a70c` et `f458980`) ; sous `isole.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL` et
sans variables de mandataire, `TMPDIR` de mon dossier (`outils/gates.sh`, `tmp/gates-c18.txt`). Toutes les étapes
`run:` de `gates.yml`, g3 `--history` et `--tree` exceptés : 16 en sortie 0 : hooks 57 ok ; aucun marqueur de dette
nu ; runners épinglés (7 workflows, 22 clés) ; `workflows-yaml` 16 cas et conforme (PyYAML 6.0.1) ; `model-pinning`
227 cas, lint R-1 sur 12 fichiers ; `journaux-modele` conforme ; `docs-sha256sums` conforme (42 SHA256SUMS, 324
lignes) ; secrets 147 cas ; runner 137 ok ; S2 `Ran = 419` ; s2bis 358 ; sim-bis 279 ; calib-actifs 77 ; controle 107.

Matrice `scripts/controle`, Python 3.10 à 3.13, `-X dev -W error -B` (`outils/matrice.sh`) : `Ran 107`, OK sous les
quatre ; la ligne du job relancée ensuite reste conforme (aucun fichier compilé laissé). Même matrice sur R-10 :
`Ran 115`, OK sous les quatre. Sur R-10, les 12 étapes que les réserves touchent (hooks, marqueurs, g1, secrets,
runner, controle) : sortie 0 (`tmp/gates-r10.txt`).

Cargo, à la cible par défaut de la copie de gates (I-1 ; `CARGO_TARGET_DIR` retirée ; garde de disque à 3,1 Gio ;
journaux bruts jamais affichés, effacés après extraction ; `tmp/*.garde` gardés) : `cargo --locked xtask verify` (`outils/verdicts.py`, lignes VERDICT seules) : huit
VERT, un ROUGE (1 violation), verdict global ROUGE : S-G9, `docs/17-modele-de-menace.md:70`, chemin exclu de la copie
creuse (attendu ; 7 autres jetons `chemin:ligne` comptés, non affichés) ; `cargo --locked test -p xtask` : sortie 0,
100 passés, 0 échec ; `cargo test --locked --workspace` (forme de la forge) : sortie 0, 269 passés, 0 échec, 0 ignoré.
Espace libre minimal : 4250 Mio.

## 6. Crochet GARDE-FAITS du dépôt et `avant_acte.py`

Lu : `.claude/hooks/garde_faits.py` (`3a2df6d8…`, commis par `a45f363`) et `.claude/settings.json` (`debfbe17…`).
Sonde : copie du crochet lancée sur des journaux synthétiques (nom en `.txt`) bâtis avec les commandes des skills
(`sondes/sonde_crochet.py`, `tmp/sonde-crochet.txt`), que l'appel courant soit ou non au journal (mêmes sorties).

Recouvrement :
- commit : R3 du crochet (un `git status` ou `git diff` lu dans les 60 derniers appels, quel que soit l'arbre) et C1
  (sceau après vérification), C6 (index égal aux diffs nommés) de l'outil : même intention, l'outil est le plus fort ;
  R5 (identifiant écrit déjà affiché) et C3 (sha court présent aux sources ou résolu par git) : le crochet ne lit que
  le texte de la commande (un identifiant jamais affiché dans le fichier de `git commit -F` passe), l'outil lit le
  message ; un `git commit -m` à identifiant résolu mais jamais affiché est refusé par le crochet, admis par C3 ;
- poussée : R3 (ce qui part lu : `git log …origin`, `git status`, `ls-remote`) et P1, P2, P3 de l'outil ;
- chaîne détachée : le crochet ne voit pas les commits du script (`bash chaine.sh`) ; seuls l'outil et `verif` jugent.

Contradictions (refus du crochet sur un acte que l'outil admet), éprouvées : la commande du point 4 de
`shogen-avant-committer` (`avant_acte.py commit … && git commit -q -F <m>`) est refusée (R3) sans lecture préalable ;
celle du point 2 de `shogen-avant-pousser` (`avant_acte.py pousser … && git push origin <b>`) aussi ; le contrôle du
point 3 (`avant_acte.py pousser --acte "git push origin --delete …"`), qui ne pousse rien, est pris pour une poussée
et refusé : le crochet bloque le contrôle même qui évite E17. Avec la lecture en tête du point, les trois passent.
Forme exacte : réserve R-8 (skills complétés ; test qui lance le vrai crochet). Vécu dans cette passe : le crochet a
refusé deux de mes commandes de sonde qui ne poussaient ni ne commettaient rien (R3, puis R5 sur un identifiant fictif
d'un journal synthétique) : il juge le texte de la commande (item LN-6, hors de ce lot).

## 7. Limites (items à former)

- LN-1 `chaine.sh` contrôle le disque au départ seulement ; une chaîne longue peut passer sous 3 Go en route (E4) ;
  une forme testable demande un disque factice : item.
- LN-2 Citation de forme stricte dont le chemin n'existe pas (faute de frappe, casse) : avertissement seul, sortie 0
  (conception de GF-3 : les pièces versées citent des fichiers hors du dépôt) ; à durcir après mesure du journal.
- LN-3 `diff` : citation d'un fichier que le même diff retire, lue dans l'arbre de travail d'avant.
- LN-4 `verif` ne lance ni `cargo test --workspace` (forge) ni les cas des hooks et des secrets ; le pre-commit
  versionné installé couvre R-13, R-1 et G3 au commit (L-9 : `verif` à relire par lot).
- LN-5 `chemin_interdit` juge `journal.jsonl.txt` interdit (motif de D.2) : faux interdit possible, sens sûr.
- LN-6 Crochet GARDE-FAITS (hors lot) : il juge le texte de la commande, non l'acte ; R5 ne lit pas le fichier de
  `git commit -F`.
- LN-7 Les tests cargo du workspace laissent 34 dossiers temporaires (`shogen-canonique-*`, `-coquille-*`, `-e2e-*`,
  `-reel-*`) dans `TMPDIR` (effacés du mien) : hygiène des tests Rust, hors lot.
- L-1, L-2, L-3, L-7, L-11, L-13, L-14 de la G2 : rejugées, justes ; les formes que j'en ai fermées sont R-9, R-10,
  R-3 (le reste demande un jugement de sens ou expose à des faux refus).

## 8. Tête du moment

Relue à 11:57:17 : `67061e7` (DEPLOI-BIS DB1-d). Entre `8d19a0e` et elle, sur la liste explicite des chemins de la
série et des réserves et sur les fichiers que lisent outils et gates : `gates.yml` seul (planchers s2bis 358 → 367,
calib-actifs 77 → 78, hors des blocs de la série). Copie de `67061e7` : les 45 diffs (série, corrections, réserves)
s'appliquent dans l'ordre ; ligne du job : GF-10b `Ran 89`, C-18 `Ran 107`, R-10 `Ran 115` (plancher exact) ;
`avant_acte.py diff` sur les 45, outils C-18 et R-10 : 45 sorties 0 chacun. Relue encore à 12:05:23 : `6409d90`
(DEPLOI-BIS DB1-e) ; depuis `67061e7`, sur la même liste : `gates.yml` seul (plancher s2bis 367 → 369) ; les 45 diffs
s'y appliquent, ligne du job : C-18 `Ran 107`, R-10 `Ran 115`.

## 9. Écarts

- E-1 `du -sh` lancé une fois sur ma copie creuse (total seul affiché) ; non refait.
- E-2 Étiquette et branche nommées `base` dans ma copie (avertissement d'ambiguïté de git ; l'étiquette, commit de
  base, a été prise : `Ran 37`) ; ensuite étiquettes en `refs/tags/`.
- E-3 Crochet GARDE-FAITS : deux refus de mes commandes (R3, R5) ; j'ai lu le `git status` de ma copie jetable, puis
  écrit la sonde du crochet par l'outil d'écriture (fichier `.py`), le texte de la commande portant `git commit`.
- E-4 Commits, étiquettes, `checkout` de fichiers et `reset --hard` dans ma copie jetable seulement, jamais dans le
  dépôt du projet : R-2, R-3, R-4 récrits avant leur commit (ligne de plus de 120 caractères, garde du script,
  docstring) ; R-6 et R-7 retouchés avant commit (docstring) ; R-7 à R-9 refaits après commit (`reset --hard` sur
  R-6) parce que le test de R-7 donnait ERROR, non FAIL, sur l'état d'avant.
- E-5 Cargo écrit son verrou et son cache dans `CARGO_HOME` (`~/.cargo`), hors de mon dossier ; cible dans ma copie.
- E-6 Deux `sed -i` à barre oblique inverse (`recompte.py`, `verif_r.sh`) : octets relus après écriture, justes.
- E-7 `objects/info/alternates` de ma copie de gates vers les objets du projet, en lecture (sim-bis).
- E-8 Les étapes `g5-todo` (`git grep`) et `g3-cas` ont cherché dans mes copies, comme le point 4 le demande.
- E-9 Le harnais a refusé un `sleep` d'avant-plan : attente par la notification de fin des tâches de fond.
- E-10 `GIT_INDEX_FILE` temporaire de mon dossier pour rebâtir l'arbre de R-10 depuis les diffs (dans ma copie).

## 10. Journal de provenance

Sources lues, niveau [lu] : le brief ; les pièces (empreintes en tête), dont les ajouts de l'adjudication du
2026-10-10 (05:05:23, 08:13:53, 08:19:22, 14:09:16) et du 2026-10-15 (10:57:57) ; les dix-huit diffs de correction en
entier (C-13 appliqué au brouillon) ; la série GF-0 à GF-10b lue par son effet, non diff par diff (état final des
outils et des tests, appliquée et jugée état par état) ; dans ma copie, à l'état final : `scripts/controle/avant_acte.py`,
`garde_commun.py`, `presg5.py`, `gabarits/chaine.sh`, `gabarits/rapport-cc.md`, `garde/hors-distant.txt`,
`garde/lignes-citees.txt`, les en-têtes et aides des tests, `test_skills.py`, les quatre skills, la fin de
`docs/adr-0028/G0-lots-DETTES.md`, `.github/workflows/gates.yml`, l'en-tête de `enforcement/verdict-suite-s2.py` ;
la l.293 d'ADR-0028 ; `.claude/hooks/garde_faits.py`, `.claude/settings.json`, l'en-tête de son test ;
`.claude/agents/shogen-orchestrator.md` l.80 à 90 ; `.cargo/config.toml` ; `enforcement/hooks/pre-commit` (en-tête) ;
les outils `isole.sh`, `lo_up.py` ; les scripts de la G2 (copie, états, gates, rejeux, banc, mutants) pour la forme,
non leurs résultats. `fm11.py` lu par `ast` (structure seule, aucun motif affiché). Niveau [2nd] : aucun chiffre
repris : lignes, sommes, comptes, planchers, bilans de mutants, de gates et de cargo recomptés par mes scripts
(`cc/tmp/`). Commandes, heures et sorties : `cc/NOTES.md`. Commandes git sur le dépôt du projet : lecture seule,
`archive` avec exclusions, `log`, `rev-parse`, `config --get`, `diff` limité à une liste explicite de chemins ;
`.git/hooks/pre-commit` relu par sha256 (égal au versionné). Aucune variable de clé lue, rien sur Pocket.
