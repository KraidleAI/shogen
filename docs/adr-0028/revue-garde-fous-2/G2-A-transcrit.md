# Relecture G2 neuve du groupe A (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2a/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve — GARDE-FOUS-ORCH, phase 2, groupe A (briefs et comptes)

- **Gate 0** : réviseur `claude-opus-5-5` (identifiant déclaré par l'environnement) ; générateur distinct.
- **Pièces relues** (série) : `../diffs/P2A-1.diff` … `P2A-7.diff`, sha256 de leur concaténation dans l'ordre
  `fb36bf5a8e14f45c20ea9b28daaca44fefba9ae722bbff5d4bcccac6e2bbebfa` (chaque sha256 égal à `../SHA256SUMS`) ;
  `../BRIEF.md`, `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, `../outils/recaler.py` ; outils versés après la série ;
  `docs/adr-0028/revue-garde-fous/ADJUDICATION.md` ; registre des erreurs (E6, E7, E12, E13, E22, E23, E24).
- **Bases** : relecture faite sur `ec5d0eb` ; la tête a avancé à `520bb2a` pendant la relecture (voir point 1).
- Enregistrement `oracle_record.py --role G2` : sans objet (lot hors du chemin S2, aucun dossier soumis au cp-2).
- Journal : `NOTES.md` ; mesures : `outils/*.txt` ; mutants : `mut/`, `mut2/`.

## Verdict : ACCEPTE-AVEC-CORRECTIONS, C-1 à C-8 (liste fermée)

Diffs byte-exacts dans `diffs/`, à appliquer après P2A-7, dans l'ordre ; sha256 de leur concaténation
`559195c5979929d91d4a04dc7d3b65f242b6fd26e2d1b874cdd770075c128166`. Chacun : `git apply` sur la série (seule et
cumulée), autocontrôle `avant_acte.py diff` de l'outil final : sortie 0 pour les huit (`outils/autocontrole-c.txt`) ;
aucune fonction de test neuve, plancher inchangé (129) ; ajout daté en fin de README ; sha256 cités contrôlés égaux au
fichier de leur pas ; aucun TODO ni FIXME ; lignes ajoutées 19, 33, 21, 17, 27, 46, 38, 21.

| C-n | point | objet | rouge avant / vert après |
|---|---|---|---|
| C-1 | 2 (E6) | `CLOS` lit aussi soldé et sans objet ; tranché non (une question tranchée laisse l'item ouvert) | 1 échec / OK |
| C-2 | 3 (E24) | décision de l'orchestrateur : B4 exige la règle dans le brief lui-même, quelle que soit la fiche ; le refus le dit et nomme la fiche ; options globales de git (`-C`, `-c`, `--no-pager`, `--git-dir=`, `--work-tree=`) vues | 2 échecs / OK |
| C-3 | 4 (E22) | B2 : sujets au pluriel, contre-contrôleur, verbes au pluriel, participes accordés, `d'après` | 1 échec / OK |
| C-4 | 4 (E23) | B3 lit aussi `chemin l.N` (forme de référence admise par B2, jamais vérifiée) | 1 échec / OK |
| C-5 | 5 (R7) | consigne `prompt` de plus de 1500 caractères sans `BRIEF*.md` : refus (brief manquant) | 1 échec / OK |
| C-6 | 6 (E7) | compte lu sans unité par `wc` ou `grep -c` (résultat apparié à sa commande par l'id) : permis | 1 échec / OK |
| C-7 | 7 (E12) | IGNORECASE : jeux de caractères clos par la casse | 1 échec / OK |
| C-8 | 9 | tests seuls : Workflow et champ hors `prompt` (R7), compte tapé par l'humain (E7) | mutants G02, G03, G04 tués |

Suite du job `controle-unittest` (ligne exacte de `gates.yml`, `TMPDIR` du lot) : tête `ec5d0eb` 153 ok + Ran = 117 ;
série 153 ok + Ran = 129 ; série + C-1…C-8 153 ok + Ran = 129 ; conformes, 0 ligne Warning ni Exception
(`suites.txt`). `test_garde_*` sous 3.11, 3.12, 3.13, `-X dev -W error` : 30 tests OK, série et corrigé
(`outils/versions.txt`). Crochet, `.claude/hooks/tests/test_garde_faits.py` : 2 échecs identiques sur tête, série et
corrigé (artefact du TMPDIR à segment hexadécimal, déjà relevé par le générateur).

## Checklist

1. **Application** — sur `ec5d0eb` : sept `git apply --check` à 0 ; fichiers du lot égaux à l'octet à `../etape3-G` ;
   plancher 117 → 129 (= 117 + 12) ; README : 470 premières lignes inchangées, ajouts en fin ; seule la l.365 de
   `gates.yml` change, en place (renvois du registre `docs/RENVOIS-LIGNES.tsv` vers `gates.yml` : l.35, 54-92,
   144-192). Sur `520bb2a` (DT15-e à DT15-j, lue à la reprise) : **P2A-1 ne s'applique plus** (`patch failed:
   scripts/controle/README.md:468` ; plancher de la tête 118 avec une ligne de commentaire ajoutée au job), et la suite
   tombe en cascade ; hors README et `gates.yml`, les sept P2A et les huit C s'appliquent sur `520bb2a` et donnent les
   mêmes `garde_commun.py`, `avant_acte.py`, `garde_faits.py`. Recalage : README en fin, plancher final 130 (118 + 12),
   les nombres `plancher … 120` à `129` des ajouts décalés de un. Observation O-1 : le job porte une ligne de
   commentaire par lot qui change son plancher (DT15-f l'a suivie) ; la série n'en ajoute pas.
2. **E6** — `ANNEXE-B-items.md` à la tête : 502 items, 222 fermés. SHOGEN-E1-XTASK-REFS-1 (fermé l.1583) et
   SHOGEN-CI-RUNNERS-1 (fermé l.1564) cités ouverts : REFUS B1 ; items de B.102 : conforme. Faux verts réels :
   SHOGEN-SCEAU-OTS-1 (l.1500, `sans objet`) et SHOGEN-RENDU-ETIQUETTE-1 (l.405, `soldés`) : sortie 0. Amendements
   datés `X fermé` : déjà lus (fenêtre après l'item, cas l.1564). Colonne statut : **non**, les tables d'items n'en ont
   pas (en-têtes `item | constat | propriétaire | déclencheur | prix | origine` et deux variantes, relevés par grep) ;
   la fermeture vit dans les amendements. C-1 : 222 → 230 fermés, huit changements relus un à un, justes.
3. **E24** — à la série, B4 se satisfait de la fiche : contraire à la décision. C-2 ; refus :
   `le brief nomme une commande git sans porter lui-même la règle … ; elle vaut pour tout brief, quelle que soit la
   fiche (fiche-regle) : une fiche qui la porte ne suffit pas (E24)`. Conséquence mesurée : 5 briefs réels sur 8 du
   lot GARDE-FOUS-ORCH (p2b, p2c, p2b/g2, gf1, gf1/g2/cc) seraient refusés (`outils/briefs-reels-C3.txt`). Limite
   gardée : la règle se lit comme texte (un brief qui la cite passe, le mien et celui du générateur).
4. **E22/E23** — faux et vrai pour chacun (`outils/essais-b2-b3.txt`) : constat sans référence REFUS / avec
   `chemin:N` 0 ; `selon la G2` REFUS ; fichier absent REFUS / présent 0 ; ligne `:99999` REFUS (`810 lignes`) / `:100`
   0 ; commit `abc1234` REFUS / `ec5d0eb` 0 ; sous-commande `verifier` REFUS / `diff` 0. Faux verts adverses : pluriels,
   contre-contrôleur, `d'après` (C-3) ; `inexistant.py l.3` (C-4) ; `Le CC note` (verbe hors liste) et un chemin absent
   sur une ligne qui dit `écrire` ailleurs (PRODUIRE juge toute la ligne) : limites, items ci-dessous. Connecteur non
   vérifiable (`mcp__Google_Drive__upload`) : sortie 0, limite admise. Mon propre brief (`BRIEF-G2.md`) est refusé
   B2 l.9 (`le générateur dit` sans référence) : vrai positif au sens de E22.
5. **R7** — consigne en ligne sans fichier : permise à la série. Avis : oui, une consigne longue sans brief est un
   brief manquant ; C-5 (seuil 1500 caractères, constante `CONSIGNE_MAX`, à adjuger) ; une consigne courte qui renvoie
   au brief reste permise (la mienne). Limite : le texte en ligne d'une consigne qui nomme aussi un brief.
6. **E7** — compte tapé : REFUS ; `printf` avec unité : permis ; `echo` : permis (limite admise). **Compte lu par
   `grep -c` (sortie `12`) ou `wc -l` (`42 x.py`) : REFUS à la série** (unité absente de la sortie) : C-6. Après C-6 :
   permis ; le même nombre affiché par `cat` : refus. Hors règle : nombres en lettres au-delà de douze, `brief-a.md` en
   minuscules, copie `cp` vers un `BRIEF*.md`.
7. **E12** — `git log -n 5 --format=%h -- enforcement/runners-epingles.py` : d49df1b e7ffd12 ae7ffe3 17172ce
   ba03914. VIDE et BLOC de `e7ffd12` (l.25-26) : `quantificateurs-imbriques` (ast et `motifs_ajoutes`) ; `d49df1b` :
   rien. Motifs actuels de `scripts/controle/*.py`, `.claude/hooks/*.py`, `enforcement/*.py` (13 fichiers) :
   72 littéraux, 68 lus par `motifs_ajoutes`, 55 motifs de module (concaténations comprises) : **aucun faux positif**.
   Motifs adverses (13, temps réel mesuré en sous-processus borné à 5 s, `outils/adverses_e12.txt`) : vrais positifs
   `(\w+\s?)*$`, `(?:x+x+)+y`, `(?:[0-9]+\.?)+$`, `(?:.*?,){11}x`, `(?:\d|\d\d)+$`, courriel OWASP,
   `(?:a(?=a)|a)+$` ; sûrs non signalés `(?>a+)*$`, `(?:a+)*+$`, guillemets CSV ; faux positif prudent `(?:a|b?)+$`
   (0,0 s) ; **faux vert `(?i)(?:A+a+)+$`** (0,002 s, 0,043 s, 0,224 s à 16, 20, 22 caractères) : C-7 ; après C-7,
   signalé, et la mesure sur le dépôt reste à 0.
8. **E13** — diff ajoutant un test, sans `--rapport` : REFUS D4 ; rapport `vivant` : REFUS ; rapport `tué` : 0 ;
   fonction publique sans README : REFUS D3 ; avec README au même diff : 0 (`outils/essais-e13.txt`). Limites vues :
   une ligne `non tué` passe (TUE sans négation) ; le nom du test est cherché comme sous-chaîne.
9. **Mutants** — outil `scripts/controle/mutants.py` de `ec5d0eb`, job `controle-unittest`, borne 300 s, détaché.
   Campagne 1 (copie de la série) : témoin vivant ; 21 mutants du générateur rejoués (M01 M04 M07 M10 M12 M13 M16 M18
   M21 M22 M23 M24 M25 M26 M30 M41 M45 M50 M51 M57 M59 ; c1 et c4) : **tous tués, M24 compris** ; mes mutants de
   sites d'appel et de sources : G01 G05 G06 G08 G09 G10 G11 tués, **G02 (R7 limité à Agent), G03 (consigne lue dans
   `prompt` seul), G04 (humain retiré des sources de comptes), G07 (base et dépôt permutés dans B3) vivants** ; la
   campagne a été coupée par le redémarrage du conteneur avant G12 (run sans résultat, non compté) et avant son relevé
   `ps`. G07 est tué par le cas de C-4 (rejeu à la main, test en échec) ; G02, G03, G04 par C-8 (idem). Campagne 2
   (copie corrigée, `mut2/`) : témoin vivant ; K01-K15, K17, K18 et G12 tués ; K16 vivant (un résultat sans
   `tool_use_id` lu comme compteur : forme absente des journaux Claude Code, aucun cas ajouté) ; K19 vivant,
   **équivalent** (`_CASSE[0]` est reposé à chaque appel de `motifs_suspects`, seul appelant de `_jeu`) ; relevé de
   fin : `aucun processus des 42 groupes de la campagne`.
10. **Écarts du générateur** — E-1 (git dans un dépôt jetable) admis ; E-2 à E-7 admis ; aucune pièce interdite
    ouverte d'après NOTES et rapport (listes explicites, journaux sans interdit : grep 0 sur `outils/journaux.txt`).
11. **Conflits B et C, dépendances** — lignes partagées : plancher, fin du README, docstrings de module (ajouts en
    fin), `COMMANDES` et `parseur()` d'`avant_acte.py`, en-tête des règles et `pre_tool_use` du crochet. La série dépend
    aussi : (a) des **sha256 cités dans ses ajouts au README** (11 du générateur, 7 des miennes), faux dès que B ou C
    changent les mêmes fichiers ; (b) de l'**ordre des dates** des ajouts du README : l'ajout DT15-f de la tête est daté
    `2026-10-15 23:45:31 UTC`, après ceux de P2A-1 à P2A-7 ; DATE-PASSEE du groupe C (refus d'une date-heure antérieure
    au dernier ajout daté du même fichier) refuserait la série posée derrière ; (c) des internes de `diff` (index
    temporaire `env` lu par D3) que LECTURE-SEULE (C) remplace ; (d) de la variable `cibles` de R2 (E7, écritures par
    le shell) que LN-6 (B) refait par `shlex` ; (e) des autres règles du crochet sur Agent et Write (E27 de B) que les
    tests R7 et E7 lancent sur le crochet réel ; (f) des aides partagées (`chemin_interdit`, `MASQUE`, `plier`,
    `analyser_diff`, `contenus`, `resoudre`). **`outils/recaler.py` n'est pas sûr en réemploi** : rejoué dans
    `recal/` depuis `../etape-*` sur la tête, il rend un `garde_commun.py`, un README et un `test_garde_regex.py`
    différents de la série livrée (les étapes `etape-*` précèdent la correction du nœud `.` et `_absorbe`, faites sur
    `etape3-*`) : il réintroduirait le `TypeError` ; il ne recalcule pas les sha256 du README, ne relance aucune suite,
    garde de `gates.yml` la seule ligne du plancher. Il échoue fermé sur un conflit vrai. Le recalage se fait depuis les
    diffs livrés (plus C-1 à C-8), suite rejouée, sha256 et dates relus.

## Items à former (règle PAROXYSME)

| item proposé | constat |
|---|---|
| SHOGEN-GARDE-FERMETURE-MOTS-1 (du générateur, réduit par C-1) | tranché et les fermetures sans mot de clôture restent hors de l'outil |
| SHOGEN-GARDE-BRIEF-EN-LIGNE-1 (réduit par C-5) | texte en ligne d'une consigne qui nomme aussi un brief ; seuil à adjuger |
| SHOGEN-GARDE-B3-PRODUIRE-LIGNE-1 | PRODUIRE exempte toute la ligne : un chemin absent passe si la ligne dit `écrire` ailleurs |
| SHOGEN-GARDE-B2-VERBES-1 | relais par un autre verbe (`note`, `voit`) ou sans sujet nommé |
| SHOGEN-GARDE-E7-LETTRES-CASSE-1 | nombres en lettres au-delà de douze, brief nommé en minuscules, `cp` vers un `BRIEF*.md` |
| SHOGEN-GARDE-D4-NEGATION-1 | D4 lit `non tué` comme tué ; nom de test cherché comme sous-chaîne |
| SHOGEN-CROCHET-HUMAIN-CHAINE-1 (hors lot) | `faits_et_appels` découpe en caractères un message humain dont le contenu est une chaîne (mesuré : 14 éléments pour `tape 4 mutants`) : R5 ne voit ni identifiant ni compte tapé par l'humain sous cette forme |
| SHOGEN-GARDE-RECALER-REEMPLOI-1 | `recaler.py` part d'étapes périmées ; sha256 et dates des ajouts du README non recalculés |
| SHOGEN-GARDE-ORDRE-DATES-README-1 | ordre de la chaîne contre dates des ajouts du README (DATE-PASSEE du groupe C) |

SHOGEN-GARDE-REGLE-GIT-FICHES-1 (du générateur) tombe avec C-2 ; SHOGEN-GARDE-CAPACITE-OUTIL-1,
SHOGEN-GARDE-VALEUR-INERTE-1, SHOGEN-GARDE-COMPTE-PROVENANCE-1, SHOGEN-GARDE-REDOS-POLY-1, SHOGEN-CROCHET-TESTS-JOB-1
confirmés.

## Écarts du réviseur
- E-1 : git en écriture dans le scratchpad seulement (`jetable/`, `corr/`, `tmpdir/jetable2`, configuration isolée) ;
  objets du projet lus par `GIT_ALTERNATE_OBJECT_DIRECTORIES` (lecture seule) pour résoudre les commits dans B3.
- E-2 : `grep -rn` sur ma copie `tete/` (dossier `docs/` compris, réduit aux fichiers archivés par liste explicite)
  pour chercher des renvois par ligne ; aucun interdit n'y est.
- E-3 : la mesure des motifs de module a chargé les modules, ce qui a exécuté le haut de `render_fixture.py`
  (FileExistsError ; rien écrit, `find -newer` vide).
- E-4 : `__pycache__` écrits dans `corr/` par un `python3 -I -c` sans -B, entrés dans deux révisions ; historique de
  `corr/` refait depuis les diffs, aucun pyc dans les diffs livrés.
- E-5 : campagne 1 coupée par le redémarrage (G12 rejoué en campagne 2 ; relevé `ps` de fin perdu, aucun processus
  de mes copies vivant au relevé de reprise).
- E-6 : lecture des briefs voisins (p2b, p2c, gf1) par chemin nommé, pour la mesure de faux refus ; aucune liste par motif.
