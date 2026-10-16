# Relecture G2 neuve du groupe B (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2b/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# GARDE-FOUS-ORCH, phase 2, groupe B : relecture G2 neuve

Réviseur : `claude-opus-5-5` (Gate 0 : identifiant système de la session ; je n'ai pas généré le lot). Brief :
`g2/BRIEF-G2.md` (orchestrateur, 2026-10-16 01:10:25 UTC). Début de la relecture : 2026-10-16 01:11:09 UTC (`date -u`).
Rattachement : ADR-0028 annexe B, B.102 (SHOGEN-GARDE-OUTIL-E18-E20-1, SHOGEN-GARDE-OUTIL-E26-E27-E28-1,
SHOGEN-GARDE-CROCHET-ACTE-1). Journal G1 de la relecture : `g2/NOTES.md`.

Base : tête du dépôt `88da219e2bc0ab5272d6fca8caf80b9c65923d96` (le générateur partait de `8499309` ; E29 est à la tête
par `5cccd33`), copie creuse `g2/tete/` par l'outil `copie.py` du générateur, relu (`git archive HEAD`, interdits exclus
par pathspec, filtre `chemin_interdit` : 0 écarté). Pièces du générateur : `sha256sum -c SHA256SUMS` : toutes OK.
Empreinte des huit diffs relus, concaténés dans l'ordre de la série (GFB-1, 2, 2t, 3 à 7) :
`9ea2e22ffc57df1146a742d31d0d95dafb12fcdf8ba3f34ebe34986c5f41b3e1`. Enregistrement `oracle_record.py --role G2` : sans
objet (lot hors du chemin S2, rien n'est soumis au cp-2).

## Verdict : ACCEPTE-AVEC-CORRECTIONS, C-1 à C-8 (liste fermée)

La série fait ce qu'elle annonce sur les cas réels (les deux faux refus de LN-6 passent, `sleep 60`, `pgrep -f` non
ancré, PR sans forge, workflow de dix agents, CoinGecko rattaché à Pocket, livre sans rangée et versement pendant une
chaîne sont refusés), elle est verte sur la tête à 136 et ses 21 mutants rejoués sont tués. Elle a quatre régressions de
LN-6 (des actes réels refusés avant et permis après), deux écarts à des décisions de l'orchestrateur (L-3, liste des
dossiers), une preuve de forge qui n'en est pas une (marqueur écrit à la main), un jeton accordé par une défense, le
défaut des tests hors CI (L-7), et huit mutants neufs vivants. Les diffs C-2 à C-8 sont dans `g2/diffs/`, à appliquer
après GFB-7 ; C-1 est un recalage de texte.

| C-n | point | diff | lignes ajoutées | plancher |
|---|---|---|---|---|
| C-1 | 1, 11 | aucun (recalage à la chaîne) | – | – |
| C-2 | 2 (LN-6) | `C-2.diff` | 39 | 137 |
| C-3 | 3 (L-3) | `C-3.diff` | 43 | 138 |
| C-4 | 4 (E20) | `C-4.diff` | 68 | 138 |
| C-5 | 6 (E26) | `C-5.diff` | 37 | 139 |
| C-6 | 8 (L-7) | `C-6.diff` | 11 | 139 |
| C-7 | 5 (E27) | `C-7.diff` | 27 | 140 |
| C-8 | 9 (mutants) | `C-8.diff` | 26 | 140 |

Chaque diff : sous 200 lignes ajoutées (R-25), aucune ligne ajoutée de plus de 120 caractères, aucun marqueur de dette
nu (R-13), README en fin seulement (ajouts datés, dates lues par `date -u` au pas), plancher changé en place. Série C-2
à C-8 appliquée par `git apply` sur la série recalée (`g2/serie/`) : sept OK, résultat égal octet pour octet à
`g2/corr/`. Ligne du job `controle-unittest` à chaque pas : `conforme`, Ran 137, 138, 138, 139, 139, 140, 140. Matrice
sur l'état final, `-X dev -W error` : python3.11, 3.12, 3.13 : sortie 0, Ran 140, OK, aucune ligne Warning ni
Exception ignored. Rouge avant : chaque cas neuf échoue sur le crochet du pas d'avant (sortie au journal).

## Checklist

1. **Application sur la tête** : GFB-1 s'applique ; GFB-2 à GFB-7 échouent sur `scripts/controle/README.md` seul (la fin
   du README a avancé : 470 lignes à la tête, 449 à la base) ; hors README, les huit s'appliquent dans l'ordre, E29
   compris. README recalé en fin : la ligne du job est `conforme`, `Ran = 136`. Plancher de la tête : 117 ; 117 + 19
   = 136 : conforme. Aucune ligne décalée hors fin du README (`gates.yml` : une ligne remplacée par diff ;
   `lignes-citees.txt` cite le README seul parmi les fichiers touchés ; `docs/RENVOIS-LIGNES.tsv` ne cite aucun d'eux).
   Défaut de recalage : **C-1**.
2. **LN-6** : sonde du contre-contrôle : tête R3 puis R5, série 0 et 0 (verts). Vrais refus rouges : commit, push, R5 du
   message, `bash -c`, `eval` littéral, `xargs git commit`, affectation, chemin absolu de git ; gains : `env GIT_DIR=…
   git commit` et `git -c … commit` (permis avant, refusés après). Cinq contournements demandés : `bash -c` : refusé ;
   `eval` : refusé s'il est littéral, **permis s'il porte une variable** (`C='git commit -m x'; eval "$C"`, refusé
   avant : régression) ; `xargs` : `xargs git commit` refusé, `printf 'commit -m x' | xargs git` permis (avant aussi :
   limite) ; variable : `C='…'; $C` **permis (refusé avant : régression)**, `G=commit; git $G` et `g=git; $g commit`
   permis (avant aussi : limite) ; chemin avec `..` : résolu (`rm -rf d/../d/clone` refusé R1), sauf après un `cd`
   (`cd w && rm -rf ../d/clone`, permis avant aussi : limite). Deux régressions de plus : un code python qui lance git
   (`os.system('git commit -m x')` en `-c` ou en heredoc) est permis après GFB-2, refusé avant. L-5 ne déclare aucune
   des quatre : **C-2**. Les limites d'avant restent des items (§ Limites).
3. **E18, E28 (R7)** : `sleep 60` refusé ; `pgrep -f`/`pkill -f` non ancrés refusés sous leurs formes (`--full`, `-af`,
   `-HUP`, `--`). La règle livrée refuse toute boucle while (`while ! test -f fin; do sleep 5; done` : R7) et admet
   `until false` (sans fin) : elle ne dit pas la décision de l'orchestrateur (while ou until à condition de sortie admis
   au même titre). Le moniteur de l'orchestrateur relevé sur l'hôte (`while true; do …; break; …; sleep 5; done`)
   serait refusé : **C-3**. Faux refus mineurs, sens sûr : `pgrep -f '[c]haine_gf.sh'`, `pgrep -x -f 'bash chaine.sh'`.
4. **E20 (R8)** : personne n'écrit `garde/forge-actions.txt` (ni le crochet, ni une skill, ni un outil) ; la ligne
   `owner/repo AAAA-MM-JJ` se pose à la main, sans preuve, et R5 ne juge pas un nombre décimal. Une preuve est possible
   hors ligne : les journaux de la session (principal et `subagents/agent-*`) sont des fichiers locaux que le crochet
   lit déjà. **C-4** : la ligne porte l'identifiant du run lu (`owner/repo AAAA-MM-JJ <id>`) et ne vaut que si cet
   identifiant figure dans une preuve du même dépôt d'un journal de la session. D'une autre session, la preuve n'est
   pas vérifiable sans réseau : le marqueur ne vaut alors rien (une lecture de `actions_list` de plus suffit).
   Remarque : le marqueur est un fichier versé, chaque ligne du jour modifie l'arbre de travail.
5. **E27 (R9)** : seuil et jeton conformes au brief ; `fan out` vaut jeton (adjudication). Défaut : `non, pas de fan out,
   fais en direct` et `fan-out interdit ici` valent jeton (sortie 0 sur un workflow de dix agents) : une défense de
   l'investisseur autorise le fan-out : **C-7** (les mots ne valent que dans une phrase sans négation ;
   `FANOUT-AUTORISE` vaut toujours). L-2 : acceptable comme limite, mais incomplète : un agent fini depuis moins de
   300 s compte vivant (quatre journaux touchés il y a 290 s : le cinquième agent est refusé) ; faux refus d'au plus
   cinq minutes, levé par le jeton : à écrire en limite (L-G4).
6. **E26 (R10)** : CoinGecko au message, réponse qui dit `Pocket` sans relevé : refusée (`R10 (E26) : la réponse nomme Pocket
   sans relevé du tour`) ; après le relevé (UserPromptSubmit), la réponse au préavis passe et la réponse Pocket reste
   refusée. Mais la liste des six dossiers est codée (`DOSSIERS`, constante du crochet) : **C-5** (lue dans
   `scripts/controle/garde/dossiers.txt`, versé). Faux positif mesuré : un mot commun (`publication`) avec un nom
   propre au message : refus, une fois par tour (L-4, à garder).
7. **E28 (`verser` V6, V7)** : rejoués dans la ligne du job (verts). Le vrai refus V7 est testé contre une chaîne
   vivante : `test_e28_versement_pendant_une_chaine` lance `bash chaine_essai_<pid>.sh` (processus factice), le voit par
   le vrai `pgrep` et refuse V7 ; un shell qui nomme la chaîne sans la lancer n'est pas vu. Conforme, sans C-n. Le faux
   `pgrep` des autres cas : acceptable (une vraie chaîne tournait sur l'hôte pendant ma relecture :
   `bash …/scratchpad/chaine_d15.sh`).
8. **L-7** : reproduit sur la tête et sur la série : `Ran 26`, 2 FAIL (`test_permis_apres_read`,
   `test_permis_apres_tail`), `R5 : l'identifiant « 7ba84933 » n'a été affiché par aucun outil` ; OK sous un TMPDIR
   sans segment hexadécimal. Cause : le cas écrit dans `NOTES.md` par son chemin absolu ; écrire un `.md` par le shell
   fait de la commande entière un texte que R5 parcourt, chemin compris, et le segment `7ba84933` du dossier de session
   (7 à 40 hexadécimaux, chiffres et lettres mêlés) y est pris pour un identifiant. Sous `/tmp`, un nom de tempfile de
   huit caractères tout hexadécimaux mêlés donne le même échec (rare). **C-6** (nom relatif au cwd du cas : 26 OK sous
   le TMPDIR du lot). La cause est aussi dans le crochet (R5 lit le chemin cible) : item L-G6, pas corrigé ici (ce
   serait desserrer R5).
9. **Mutants** : `tete/scripts/controle/mutants.py` (arbre relu = tête) sur une copie de la série, job
   `controle-unittest`, borne 300 s, lancement détaché ; témoin vivant ; 34 mutants : 21 rejoués du générateur (C01 à
   C09 des sites d'appel, S14, S15, H17, H36, H37, A10, H09, H10, H13, H15, H21, A07) : tous tués ; 13 neufs (G01 à
   G13) : 5 tués, 8 vivants (G04 refus du crochet cité dans un résultat de forge, G05 gh run d'un autre dépôt, G06
   entrée isMeta porteuse du jeton, G07 fichiers autres que agent-* comptés vivants, G10 dossier en casse différente,
   G11 gh pr create hors de R5, G12 forme `--message=` hors de R5, G13 boucle until englobante) ; aucun FATAL ; relevé
   `ps` de fin vide. **C-8** porte leurs cas. Campagne 2 sur l'état corrigé : voir § Mutants des corrections.
10. **Écarts E-1 à E-7** : relus ; aucune pièce interdite ouverte (E-1 : noms de sous-dossiers seuls, déjà au brief) ;
    E-4 (`sleep 2` d'avant-plan, l'acte même que R7 refuse) et E-7 (heredoc non cité, substitution exécutée, arrêtée
    par un motif ancré) sont consignés au NOTES du générateur. Absence dans ses copies de `docs/pocket-report`,
    `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution` : contrôlée par
    `test -e` ; `docs/15-*` et `docs/16-*` ne se contrôlent que par une liste à motif (interdite) : non contrôlés,
    exclus par le pathspec de `copie.py` (relu).
11. **Groupes A et C** : au-delà du plancher et de la fin du README, la série dépend d'autres lignes (essais sur copies
    de la tête, README et `gates.yml` exclus) : C puis B : GFB-7 échoue (`avant_acte.py`, docstring, l.66). A puis B :
    GFB-2 échoue (`garde_faits.py:235`, corps de `pre_tool_use`), GFB-3 à GFB-6 (docstring du crochet), GFB-7
    (`shogen-avant-committer/SKILL.md:8`, `avant_acte.py:66`). Deux dépendances de sens : P2A-4 lit la variable `cibles`
    dans la branche Bash, que GFB-2 retire (`fc["ecrit"]`) : sans recalage, `NameError`, rattrapée par
    `except Exception` du crochet : **toute commande Bash permise sans contrôle**, sans refus visible ; P2A-3 nomme R7
    la règle des briefs, GFB-3 nomme R7 la règle sleep et pkill : collision de numéros à trancher. Et les sha256 du
    crochet cités par les ajouts du README changent avec l'ordre (C-1).

## Corrections

- **C-1 (recalage, sans diff)** : les ajouts README de GFB-2 à GFB-6 citent le sha256 de `garde_faits.py` sur la base
  sans E29 ; sur la tête, les états du crochet sont : GFB-2 `fa444fd52d2e0990b198a2b707bc6d0f1ed2078440df805e8df774a0d314c450`,
  GFB-3 `a9cad0e7a379da9ea4fa02662dca90413b246efcfebc08d6f9f9849ca5425a9d`, GFB-4
  `7a84eb09e57de13204c9aff267fd874488efb7192a2aa71e96f688e931e7d4f5`, GFB-5
  `c68d50445587d70b4445934a02ed398a3576afcde57040d7ccbe33c6e09dced5`, GFB-6 et GFB-7
  `773bee0ac647c62b154fbdb3a2dc543df2f81ef65928a0e2d98f5400199e016a`. Les autres sha256 cités (`acte_shell.py`,
  `settings.json`, `avant_acte.py`, SKILL, `forge-actions.txt`) sont justes sur la tête. Si un diff du groupe A passe
  avant, ils se recalculent au pas. Les ajouts du README se posent en fin, après ceux de A et de C.
- **C-2 (LN-6)** : `garde_faits.py` : un acte dont le programme ou l'argument d'eval porte `$` ou un accent grave, ou un
  code python qui lance un processus (`PY_PROCESSUS` : subprocess, os.system, os.popen, os.exec*, os.spawn*,
  pty.spawn), est jugé aussi par les motifs d'avant (union, sens sûr). Les quatre régressions et `R='rm -rf clone'; $R`
  sont refusés ; la sonde, `print('git commit -m x')` et `F=neuf.txt; echo x > $F` passent. Cas
  `test_ln6_actes_non_litteraux`.
- **C-3 (L-3)** : `acte_shell.py` marque `while-sans-fin` ou `until-sans-fin` une boucle à condition constante (true,
  `:`, false, et leurs négations) ; R7 admet le sleep d'une boucle while ou until à condition, et d'une boucle sans fin
  si la commande porte break, exit ou return ; for reste refusé ; message et docstring disent la règle. Cas
  `test_e18_boucle_a_condition_de_sortie`.
- **C-4 (E20)** : `preuves_forge` ; `forge_lance(entrees, owner, repo, entree)` : marqueur `owner/repo AAAA-MM-JJ <id>`,
  identifiant cherché dans les preuves du même dépôt des journaux de la session ; en-tête du marqueur et message de
  refus récrits. Cas `test_e20_marqueur_du_jour` récrit (sans identifiant, autre jour, autre dépôt, identifiant absent
  ou lu dans un échec : refus ; preuve au journal principal pour un sous-agent, ou au journal d'un sous-agent : permis).
- **C-5 (E26)** : `dossiers()` lit `scripts/controle/garde/dossiers.txt` (neuf, les six noms) ; l'aide `arbre()` des cas
  copie ce fichier. Cas `test_e26_dossiers_lus_au_fichier`.
- **C-6 (L-7)** : `.claude/hooks/tests/test_garde_faits.py`, deux commandes écrites par nom relatif. Hors CI.
- **C-7 (E27)** : `jeton()` ; `NEGATION`. Cas `test_e27_fan_out_dans_une_phrase_niee`.
- **C-8 (mutants vivants)** : cas seuls, dans les tests existants (comptes inchangés).

## Mutants des corrections

Même outil, état corrigé (`corr/`), borne 300 s, détaché ; 19 mutants : K01 à K11 (un par correction : PY_PROCESSUS
retiré, programme non littéral ignoré, marque sans fin retirée, break ignoré, date du marqueur ignorée, identifiant
non cherché, preuves ignorées, liste codée rétablie, négation ignorée, FANOUT-AUTORISE ignoré, négation de la boucle
ignorée) et les huit vivants de la campagne 1 (G04, G06, G07, G10, G11, G12, G05b et G13b adaptés au code corrigé).
Une première campagne a été coupée par le redémarrage du conteneur (lot interrompu : non compté, copie mutée refaite
depuis `corr/`) ; refaite en deux lots (`tmp/mutants-run-3.txt`, `tmp/mutants-run-4.txt`) : témoin vivant, 19 tués,
aucun vivant, aucun FATAL ; relevés `ps` de fin vides (22 et 20 groupes).

Tête avancée pendant la relecture : `520bb2afa8116ecd3229cda0e8685eb19a4e0e4f` (DETTES-T15 : deux lignes de
commentaire avant le job, plancher 118). Sur une copie de cette tête (`tete2/`), GFB-1 à GFB-7 puis C-2 à C-8
s'appliquent hors README et `gates.yml` (fichiers égaux à `corr/`) ; seul le bloc du plancher échoue (contexte 117).
Plancher recalé : 118 + 19 = 137 pour la série, 141 avec C-2 à C-8 ; ligne du job sur `tete2/` (README recalé en
fin, plancher 141) : `conforme`, `Ran = 141`.

## Limites (items à former, règle PAROXYSME)

- L-G1 R1 et R2 ne voient pas : un chemin relatif après un `cd` de la même commande, une cible portée par une variable
  (`X=d/clone; rm -rf $X`), `find … -delete`, `cp`, `mv`, `dd of=`, `install` sur un fichier existant. Avant comme après
  la série.
- L-G2 R3 ne voit pas : la sous-commande venue d'un tube (`… | xargs git`), une sous-commande ou un programme en
  variable (`git $G`, `$g commit`), un code python qui lance git par une liste (`subprocess.run(['git', 'commit'])` :
  C-2 le voit par PY_PROCESSUS, mais le motif d'avant ne lit pas la liste), un script lancé par son nom (L-5).
- L-G3 E18 a des formes déguisées que R7 ne voit pas : `sleep 60 & wait`, `timeout 60 tail -f /dev/null`,
  `time.sleep` d'un code python, `read -t 60`, `S=sleep; $S 60` ; E28 : `ps -ef | grep chaine_gf.sh` se reconnaît
  comme `pgrep -f`, non refusé.
  C-3 cherche break, exit ou return dans toute la commande, non dans la boucle : `while true; do sleep 5; done; exit 0`
  est admis (forme grossière, à affiner si elle sert de contournement).
- L-G4 R9 compte vivant un agent fini depuis moins de 300 s (complément de L-2).
- L-G5 R10 : chaque message à nom propre injecte en contexte jusqu'à douze noms de cinq lignes (coût) ; faux positifs
  sur les mots communs (L-4).
- L-G6 R5 parcourt la commande entière d'une écriture `.md` par le shell, chemin cible compris : un segment
  hexadécimal du chemin (dossier de session) non affiché fait refuser l'écriture (cause de L-7 côté crochet).
  Décision à prendre : ôter les cibles du texte jugé desserrerait R5.
- L-G7 V7 voit toute commande `bash …/chaine.sh`, y compris la chaîne d'essai d'une suite de tests d'un autre lot
  (vue sur l'hôte : `bash …/tmp/…/chaine.sh` d'une autre relecture) : refus passager, sens sûr.
- L-G8 Conflits de sens avec le groupe A (point 11) : `cibles` et numéro R7 ; un cas qui lance le crochet sur une
  commande Bash quelconque et exige une sortie sans `erreur interne` attraperait le premier.

## Écarts de la relecture

- E-1 Une fois, TMPDIR hors du dossier du lot (`/tmp/g2b-sanshex-tmp`, créé puis retiré) pour montrer L-7 vert sans
  segment hexadécimal : tout chemin du scratchpad porte le segment de la session.
- E-2 Listes par motif sur le scratchpad : `ls -d …/p2a/diffs/P2A-*.diff` et `…/p2c/diffs/P2C-*.diff` (diffs des
  groupes A et C, point 11), `grep -c '' …/diffs/*.diff` et `glob` python sur `diffs/` (le mien et celui du
  générateur) ; aucun emplacement interdit dans ces dossiers. J'ai lu les en-têtes des diffs de A et de C et les blocs
  de A sur `garde_faits.py` et la SKILL (travail d'un autre groupe, non interdit).
- E-3 Un `ps -eo pid,args` filtré a affiché les lignes de commande de processus de l'hôte (chaîne de l'orchestrateur,
  son moniteur, une chaîne d'essai d'une autre relecture) ; aucun contenu de pièce.
- E-4 `avant_acte.py diff` non joué sur mes diffs : sortie 3 (`git read-tree : sortie 128`), il exige un dépôt git et je
  n'en crée pas ; contrôle de l'orchestrateur à la réception. presg5 sur le README final : 0 fragment introuvable.
- E-5 Disque de l'hôte : 4,8 G libres au relevé (`df -h /`), sous le seuil d'avertissement de 6 Go ; mes copies sont
  petites.

## Provenance

[lu] `g2/BRIEF-G2.md`, `BRIEF.md`, `RAPPORT-GENERATEUR.md`, `NOTES.md`, `SHA256SUMS`, les huit diffs ; crochet de la
tête et de la série (`garde_faits.py` en entier), `settings.json`, `acte_shell.py`, `avant_acte.py` (hunks de GFB-7),
`gabarits/chaine.sh` (en-tête), `tests/test_garde_faits.py` (cas R2), `mutants.py` (docstring) ;
`docs/adr-0028/revue-garde-fous/CONTRE-CONTROLE-transcrit.md` l.284-304 (LN-6) ; `ERREURS-ORCHESTRATEUR.md`
(E18 à E31) ; `ADJUDICATION.md` l.1-80 ; `lignes-citees.txt`. Commandes, sorties et comptes : `g2/NOTES.md`, sorties
dans `g2/tmp/`. Outils de la relecture : `g2/outils/`.
