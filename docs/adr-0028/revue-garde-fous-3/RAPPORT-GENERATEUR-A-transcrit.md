# Rapport du générateur du groupe A (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/p3a/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (387 occurrences, aucune autre). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT DU GÉNÉRATEUR — GARDE-FOUS phase 3, groupe A

Générateur G1 : `claude-opus-5-5` (Gate 0). Base : dépôt à `fddedcfe6c64c43c5c25aa1477f1b8fe1d6f9933` (lu, jamais
écrit) ; copie `copie/` par `git archive HEAD` hors interdits. Rattachement : ADR-0028, annexe B l.1872, 1875, 1876,
1877 (bloc B.108). Journal G1 : `NOTES.md`. Diffs : `diffs/`, série à appliquer dans l'ordre GF3A-1, GF3A-2, GF3A-3a,
GF3A-3b, GF3A-4, GF3A-5 (chacun vérifié par `git apply --check` sur la tête qui porte les précédents, par
`avant_acte.py chaine --blanc` lui-même et par `avant_acte.py diff --rapport` de ce rapport).

Écart déclaré au brief (un diff par item) : l'item SHOGEN-GARDE-RECALAGE-CHECK-1 tient en trois diffs (GF3A-3a,
GF3A-3b, GF3A-4), parce qu'un seul passait 200 lignes ajoutées (R-25).

## GF3A-1 — SHOGEN-FM11-MOTIF-ATTRIBUTION-1 (annexe B l.1876)

Outil : `scripts/controle/fm11.py` (motifs de D.2, l.23 ; aussi lus par `garde_commun.interdits` pour les chemins
sous un scratchpad). Ce qu'il refuse ou compte désormais :
- le pied `Claude-Session: https://claude.ai/code/session_…` d'un message de commit n'est plus compté comme fragment
  de session (lookbehind sur la clé et l'URL) ; la même session nommée ailleurs (URL sans la clé, texte libre) l'est ;
- un chemin qui ressort du scratchpad par un composant `..` (juste après `scratchpad` ou plus loin dans le chemin,
  jusqu'au premier blanc) est compté ; `..x` et `a..b` ne sont pas des composants `..`.
Preuve rouge puis verte : `tests/test_fm11.py` rejoué avant le changement du motif : 2 échecs
(`{'session_013dvmub': [[0, 1]]}` au lieu de `{}`, `[]` au lieu des comptes) ; après : `Ran 12 tests`, `OK`.
Empreinte de `fm11.py` reportée (SHA256SUMS, `SHA_FM11`, README l.11, remplacement à nombre de lignes égal ; la ligne 4,
seule empreinte de `garde/lignes-citees.txt` sur ce fichier, ne bouge pas).
Limites : un `..` qui revient dans le scratchpad est compté (sens sûr, faux positif admis) ; un chemin écrit par une
variable du shell (`$S/../x`) n'est pas vu.
Phrase de fermeture proposée : SHOGEN-FM11-MOTIF-ATTRIBUTION-1 fermé par GF3A-1 : pied `Claude-Session:` non compté,
sortie du scratchpad par `..` comptée ; deux tests, mutants tués.

## GF3A-2 — SHOGEN-GARDE-ATTRIBUTION-PLAGE-LETTRES-1 (annexe B l.1877)

Outil : `avant_acte.py commit`, C3 (L-3), fonctions `nommes`, `attribuer` et `rang` (neuve). Ce qu'il ne refuse plus :
un mot du message porté par un passage qui nomme une plage à bornes en lettres couvrant le Diff-Id (`DT15-a à DT15-m`
pour `DT15-j`, bornes comprises, `DT15-b2` compris). Ce qu'il refuse toujours : un Diff-Id hors de la plage (`DT15-n`,
`DT15-aa`, rangé après `z`, `INT-26`). Rang : nombre de tête (0, n), ou lettres de tête (1, longueur, lettres) ; deux
bornes de sortes différentes ne forment pas de plage.
Preuve rouge puis verte : le cas mesuré par la G2 du groupe C (Diff-Id `DT15-j`, source `Série DT15-a à DT15-m : G2
neuve ACCEPTE-AVEC-CORRECTIONS, C-1 à C-10 reprises.`) donnait trois refus C3 (verdict, C-1, C-10) avant ; admis après.
Limites : suffixes en capitales non rangés ; une plage écrite autrement qu'avec `à`, `a`, `au`, `…`, `..` n'est pas lue.
Phrase de fermeture proposée : SHOGEN-GARDE-ATTRIBUTION-PLAGE-LETTRES-1 fermé par GF3A-2 : plage à bornes en lettres
lue (rang z avant aa) ; un test sur les deux formes, mutants tués.

## GF3A-3a, GF3A-3b, GF3A-4 — SHOGEN-GARDE-RECALAGE-CHECK-1 (annexe B l.1872)

Outil : `avant_acte.py chaine --blanc --script <chaîne.sh> [--diffs <d1> <d2>…]` (diffs du plan à défaut, pas déjà
commis sautés ; `--plan` et `--cc` ensemble gardent G1 à G4) et `avant_acte.py verser --blanc --script <versement.py>`,
appelés par les skills `shogen-avant-lancer` (point 2) et `shogen-avant-committer` (point 5). Ce qu'ils refusent :
- K0 : diff qui touche un interdit (ni lu ni nommé) ; K5 : diff qui ne passe pas `git apply --check` sur une copie
  creuse de HEAD (`git archive`, interdits exclus) qui porte déjà les diffs précédents, chacun appliqué avant le suivant
  (E30 : sans saut de ligne final ; E31 : chemins absolus ; diff qui suppose un pas absent ou dans le désordre) ;
- K6 : marqueur de dette nu sur une ligne ajoutée (motif R-13 lu dans l'étape du job g5, avec ses exclusions, E35) ;
  G5 : fragment anglais entre guillemets français sur une ligne ajoutée d'un `.md` (presg5, E33) ; jamais un fichier
  entier (E36) ;
- K1 : `bash -n` ; K2 : aucun `trap … ERR` ou pas de `set -E` (E36) ; K3 : `sleep` d'avant-plan (E18) ; K4 : sous
  `set -u`, `$N` lu sans protection par une fonction appelée avec moins de N arguments, aussi dans un `$( )` entre
  guillemets, ou hors de toute fonction (E34) ;
- V8 : script de versement qui ne lit pas `SHOGEN_DEPOT` (jamais lancé), qui sort hors de 0 (écriture avant contrôle
  nommée, E32), ou qui écrit dans le dépôt ; V9 : rangée de tableau ajoutée dont le compte de cellules diffère de
  l'en-tête de son tableau (compte lu par `garde_commun.rangees_fautives`, E32) ; K6 et G5 sur ce qu'il écrit.
Gabarit de versement : `scripts/controle/gabarits/versement.py` (aucun n'existait) : actes `ACTES`, toutes les cibles
vérifiées avant la première écriture, ajouts en fin, compte des cellules par la même fonction que V9.
Preuves : tests rouges sur le code d'avant (option inconnue, sortie 3 ; puis `'' != 'REFUS K1 '` pour 3b ; gabarit
absent pour 4), verts après ; sonde des messages (`patches/sonde_blanc.py`, `patches/sonde_verser.py`) : E30 `corrupt
patch at line 7`, E31 chemin absolu, E34 `un appelée avec 2 argument(s), lit $3`, E32 `8 cellules, en-tête de 7`.
Sur les chaînes réelles de la session (lecture seule) : `chaine_int.sh`, `chaine_fus.sh`, `chaine_e29.sh`,
`chaine_d7.sh` donnent K2 et K7, aucun K3 ni K4 (pas de faux refus sur leurs fonctions à arguments protégés).
Dogfooding : `chaine --blanc --script gabarits/chaine-modele.sh --diffs` des six diffs de cette série sur la base :
sortie 0 ; GF3A-3b placé avant GF3A-3a : `REFUS K5`.
Limites : K4 est une lecture statique, non un pas à vide (E34 demandait un pas à vide ou shellcheck, absent de
l'hôte) : `shift`, `eval`, appels par variable, variables nommées non liées non vus ; la copie creuse exclut les
préfixes INTERDITS et `*.jsonl`, pas les noms de D.2 hors de ces préfixes ; `verser --blanc` ne voit pas une écriture
du script hors du dépôt et de la copie (autre dossier) ; le compte des cellules suppose une barre de bord cohérente
entre en-tête et rangée.
Non-desserrement : `--plan` et `--cc` de `chaine`, `--pieces` de `verser` ne sont plus exigés par argparse (forme
`--blanc`) ; `tests/test_skills.py` garde leur présence au skill par `EXIGES` (rouge mesuré : `['--cc'] != []` quand
le skill les perd).
Phrase de fermeture proposée : SHOGEN-GARDE-RECALAGE-CHECK-1 fermé par GF3A-3a, GF3A-3b et GF3A-4 : chaîne et
versement joués à blanc sur copie creuse, lancement conditionné à la sortie 0 par les skills.

## GF3A-5 — SHOGEN-GARDE-CHAINE-ORCH-MODELE-1 (annexe B l.1875)

Outil : `scripts/controle/gabarits/chaine-modele.sh` (neuf), `verif` de `gabarits/chaine.sh` (diff relu, Q-2) et K7
de `avant_acte.py chaine --blanc` (`sceau_de_chaine`). Choix écrit au README : fichier neuf plutôt que `chaine.sh` étendu
ou remplacé, parce que `chaine.sh` porte la `verif` scellée (référence de C1, `MODELE`) et que ses copies déjà faites
tournent encore. Le modèle tire `verif` par `source` de `$OUTILS/gabarits/chaine.sh` (le fichier que `avant_acte.py` de
`$OUTILS` scelle), porte `set -Eeuo pipefail`, `trap … ERR`, `chaine --blanc` avant tout pas ; `verif` lance ses portes
Python sous `unshare -n` (`lo` allumée par ioctl) sans variables de mandataire. K7 refuse une chaîne dont la `verif` est
écrite ou recopiée, ou non tirée par `source` de `$OUTILS/gabarits/chaine.sh`, et un `git commit` sans `acte commit`.
Preuves : tests rouges sur le code d'avant (10 erreurs de `ChaineModele`, `test_k7_verif_du_sceau` et
`Chaine.test_modele` en échec ; `test_c1_verif_reelle` serré rouge sur la `verif` d'avant), verts après ; isolement
mesuré en root sur l'hôte (boucle locale joignable, `HTTPS_PROXY` absent, sous `unshare -n`).
Conséquence à porter par l'orchestrateur (C-4 de la G2 du groupe C) : l'empreinte de `verif` change ; la chaîne qui
commet GF3A-5 doit prendre `OUTILS` sur une copie des outils d'après GF3A-5, sinon C1 refuse le commit.
Limites : un `source` d'un autre `$OUTILS` que celui d'`acte` n'est pas vu ; `unshare -n` exige les droits de l'hôte.
Phrase de fermeture proposée : SHOGEN-GARDE-CHAINE-ORCH-MODELE-1 fermé par GF3A-5 : modèle versionné qui tire la
`verif` scellée par `source`, isolement et mandataire portés à la `verif`, K7 à `chaine --blanc`.

## Mutants (campagne `scripts/controle/mutants.py` du dépôt, job `controle-unittest`, borne 300 s)

Outil relu du dépôt (lecture seule), copie mutée à part (`mut/`), classement par la sortie de la commande du job (1 :
tué ; 0 : vivant ; borne ou hors contrat : FATAL, aucun). Témoin vivant à chaque lot ; relevé `ps` de fin vide à chaque
lot (`aucun processus des … groupes de la campagne, aucun descendant vivant de l'outil (moissonneur)`). Lots 1 et 2 sur
l'état final de la série 3, lot 3 (M5j) et lot 4 (M5a à M5i rejoués après le cas ajouté) sur la série 4 ; la série
5 livrée ne diffère de la série 4 que par `tests/test_skills.py` (`EXIGES`) et une ligne du README (aucun code muté). Tests en
échec de chaque mutant lus dans sa sortie (`patches/attribuer_kills.py`) : `preuves/mutants-attribution.txt`.
Run écarté : M1d du lot 1 (texte après mal écrit, motif illisible : il tuait toute la suite, sans valeur) ; refait en
M1d-bis au lot 2. M5j : vivant au lot 2 (aucun cas d'un fichier suivi sous une règle d'ignorance), cas ajouté à
`VersementABlanc.setUp` (série 4), tué au lot 3.

Ligne par test ajouté (forme exigée par D4 : nom du test et mutant tué sur la même ligne ; sens des mutants plus bas) :
- `test_attribution_claude_session` : mutants tués M1a, M1b.
- `test_sortie_du_scratchpad_comptee` : mutants tués M1c, M1e, M1d-bis.
- `test_plage_a_bornes_en_lettres` : mutants tués M2a, M2b, M2d.
- `test_e30_e31_diffs_a_blanc` : mutants tués M3a, M3b, M3c, M3h.
- `test_e35_e36_portes_sur_lignes_ajoutees` : mutants tués M3d, M3e, M3f, M3g, M3i.
- `test_e34_e36_script` : mutants tués M4a, M4b, M4c, M4d, M4e, M4f, M4g, M4h, M4i.
- `test_e32_rangee_lue_et_ordre` : mutants tués M5a, M5b, M5c, M5f, M5h, M5i, M5j.
- `test_e33_e35_portes_et_contrat` : mutants tués M5d, M5e, M5g, M5h, M5j.
- `test_k7_verif_du_sceau` : mutants tués M6a, M6b, M6c, M6d, M6k.
- `test_l4_verif_versionnee` (classe `ChaineModele`) : mutants tués M6a, M6d, M6f.
- `test_modele` (classe `ChaineModele`) : mutants tués M6g, M6j.
- `test_modele_a_blanc_avant_tout_pas` : mutants tués M6f, M3b.
- `test_c1_verif_reelle` (serré, non ajouté) : mutants tués M6h, M6i ; `Chaine.test_modele` (serré) : M6h tué.
- M6e : tué par `ChaineModele.test_verte_puis_reprise` (hérité de `Chaine`, rejoué sur le modèle).

Sens des mutants : M1a lookbehind retiré ; M1b lookbehind sans la clé ; M1c garde du `..` retirée ; M1d-bis `..x`
pris pour `..` ; M1e `..` juste après scratchpad seulement ; M2a plages de nombres seules ; M2b rang sans la longueur
(`aa` avant `m`) ; M2c borne basse exclue (tuée par `test_l3_attribution_au_diff`, existant) ; M2d rang d'un nombre
par sa longueur ; M3a diffs jamais appliqués à la copie ; M3b patch corrompu admis ; M3c chemin absent admis ; M3d
portes sur le fichier entier (E36) ; M3e exclusions du job g5 ignorées ; M3f presg5 retiré ; M3g K0 retiré ; M3h
`--blanc` jamais joué ; M3i motif R-13 remplacé ; M4a K1 retiré ; M4b `set -E` non exigé ; M4c sleep en fin de ligne
admis ; M4d redirection prise pour un séparateur ; M4e arité moins un ; M4f documents en ligne non sautés ; M4g K4
hors fonction retiré ; M4h `$( )` entre guillemets non relu ; M4i ligne de définition lue comme un appel ; M5a
gabarit sans compte des cellules ; M5b en-tête mal trouvé ; M5c V9 retiré ; M5d contrat SHOGEN_DEPOT non lu ; M5e
écriture dans le dépôt non vue ; M5f écriture avant contrôle non nommée ; M5g portes du versement retirées ; M5h
fichiers neufs non vus ; M5i gabarit qui écrit malgré ses refus ; M5j copie qui n'indexe pas les fichiers suivis
ignorés ; M6a verif écrite admise ; M6b git commit sans acte admis ; M6c source d'un autre fichier admise ; M6d K7
non appelé ; M6e pas déjà commis non sautés à blanc ; M6f `--blanc` retiré du modèle ; M6g trap ERR retiré du
modèle ; M6h `unshare -n` retiré de la verif ; M6i `$mand` retiré ; M6j verif écrite au modèle ; M6k `git -c …
commit` non vu. Diff et sortie de chacun : `mutants/lot*/<id>.diff` et `.out`.

Bilan : 48 mutants, 48 tués (M5j après le cas ajouté) ; aucun FATAL ; aucun équivalent déclaré.

## Validation de la série

- Suite du job `controle-unittest` (ligne lue dans `gates.yml` de chaque état, `--egal`) à chaque état : base Ran 177,
  GF3A-1 Ran 179, GF3A-2 Ran 180, GF3A-3a Ran 182, GF3A-3b Ran 183, GF3A-4 Ran 185, GF3A-5 Ran 196 ; toutes
  `verdict-suite-s2 : conforme`, sortie 0 (`preuves/etats-serie2.txt` pour les trois premiers états, communs,
  `preuves/etats-serie5.txt` pour les quatre derniers de la série livrée). Plancher recalé par diff : 177 → 179 → 180
  → 182 → 183 → 185 → 196.
- `avant_acte.py chaine --blanc --script gabarits/chaine-modele.sh --diffs` des six diffs sur la base : sortie 0 ;
  motif R-13 du job g5 et presg5 sur les lignes ajoutées : aucun ; série dans le désordre : `REFUS K5`.
- `avant_acte.py diff --fichier <diff> --rapport RAPPORT-GENERATEUR.md`, chaque diff sur la tête qui porte les
  précédents : voir `preuves/juger-diffs.txt` (sortie 0 exigée).

## Limites rendues à l'orchestrateur (items à former, règle PAROXYSME)

- SHOGEN-GARDE-CHAINE-PAS-A-VIDE-1 (proposé) : K4 lit le script, il ne le rejoue pas ; E34 demandait un pas à vide (ou
  shellcheck, absent de l'hôte, dépendance neuve sous R-8) : `shift`, `eval`, appels par variable, variables nommées
  non liées restent hors de vue.
- SHOGEN-GARDE-VERSER-HORS-COPIE-1 (proposé) : `verser --blanc` voit une écriture du script dans le dépôt (état relu)
  et dans la copie, pas ailleurs (autre dossier) ; un bac à sable de fichiers (espace de noms de montage) le fermerait.
- Transition C-4 à la charge de la chaîne qui commettra GF3A-5 : `OUTILS` sur une copie des outils d'après GF3A-5
  (sinon C1 refuse le sceau, l'empreinte de `verif` ayant changé) ; `unshare -n` exige les droits de l'hôte.
- `rangees_fautives` suppose une barre de bord cohérente entre en-tête et rangée ; barre échappée comptée à part, sans
  cas.
- Écart de forme, sans effet : deux commandes git sans liste de chemins (`git diff --cached --name-only` et
  `git diff --cached`) lancées dans la copie lors de la reconstruction de la série 5 ; la copie ne porte aucun interdit
  (archive faite sans eux, 0 relevé), aucun nom interdit n'a pu s'afficher.

## Empreintes à la tête de la série (copie, branche serie5, `sha256sum`)

| fichier | sha256 |
|---|---|
| `scripts/controle/avant_acte.py` | `db98fb16da8672eecf49b9f2c66d69ba0ef4fad07c384e2a3ed58d0e3b4d9c33` |
| `scripts/controle/garde_commun.py` | `5488d9639f7f72375eab1509563388549cc8bbac3c313f96ff79be4a659e53ab` |
| `scripts/controle/fm11.py` | `b78a19e9303ab4675309cabb3d28f26f4c9b415c093f7be4d93a0bab6e8631b1` |
| `scripts/controle/SHA256SUMS` | `f13cbe6cdfc1f3007ec72c3cd81a09505f8777bdeea8aa897e66d3147935e4d8` |
| `scripts/controle/gabarits/chaine.sh` | `a2b3640a451138952e407a78281ea7f077868e0c3a77f9f406493e077ec4ee76` |
| `scripts/controle/gabarits/chaine-modele.sh` | `3c78d1110985a5678dbc4c6ede2c9d7cc099d4b7b597cff5d0e906de33ca890b` |
| `scripts/controle/gabarits/versement.py` | `8b18ebed6f41bf98b425651320374365bec0c9b6b6f5361ac381b67935a93f29` |
| `.claude/skills/shogen-avant-lancer/SKILL.md` | `cd32dde276b80551d34e0580244b38b02914cee8e5b1aa181a44fc11a44ea93d` |
| `.claude/skills/shogen-avant-committer/SKILL.md` | `1d9dbb620dbc80025a72612be69a54d5fc1ed70d674c16a51788c54ed6854da6` |

Empreinte de `verif` (sha256 de `declare -f verif`, `empreinte_verif`) : avant `8fa5ee9f55f6994dd266b4ae7cb72dcbc6478b4b8c7e80cdd117277d818a05dc`
(celle que la G2 du groupe C a mesurée en C1), après `e0254878d0c18fadd8ac53269891ede6a982e67fd9fb85ad9989d90f3068e976`.

Base : la tête du dépôt est passée à `fe9a72b` pendant le travail (commit `FORGE-PR12` de l'orchestrateur : JOURNAL.md
et annexe B, ajouts en fin) ; aucun chemin touché par la série n'a changé entre `fddedcfe` et `fe9a72b`
(`git diff --quiet`) : les diffs s'appliquent à l'identique. sha256 de la concaténation des six diffs, dans l'ordre :
`689669bf6d5c06bef95466f666c1802769db38bd732493b41638c34c361e0374`.
