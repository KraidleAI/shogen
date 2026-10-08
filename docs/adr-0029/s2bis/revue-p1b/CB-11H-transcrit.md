# CB-11h : rapport du worker et contre-contrôle bref (transcrits)

> Transcription par l'orchestrateur le 2026-10-05 03:18:37 UTC des deux rapports rendus par message (worker a1b943cc864fefbc9 ; réviseur a89713614f46e2240) ; contrôle FM-1.1 des deux transcripts : fragments_l51_l14 = 0. Textes ci-dessous, sans retouche.

## 1. Rapport du worker

**Gate 0** : je tourne sous `claude-opus-5-5`. Lu par `date -u` : début le 2026-10-05 à 02:55:48 UTC, fin à 03:14:34 UTC.

CB-11h est produit. Il ne touche que du texte, dans deux fichiers (+4 −3). CC-1 et CC-2 sont faits. Le facultatif RFC 7301 n'est pas fait : il ne tient pas sur la ligne (138 caractères, la borne est 120). Tous les contrôles demandés passent.

## Livrables
- `<scratchpad>/s2bis/p1b/cb11h/CB-11h.diff` : 32 lignes, 2 291 octets, sha256 `accd8bf7fa5edce206a042173066d37c34008c18093d3b9bcf185d614b62ebec`.
- `…/cb11h/SHA256SUMS` : 1 ligne, `sha256sum -c` OK.
- `…/cb11h/arbre/` : la copie de travail.
- `…/cb11h/preuves/` et `…/cb11h/outils/` : sorties et outils, indexés par `…/cb11h/SHA256SUMS-preuves` (23 lignes, `2b734b3d…0eb4`).

## Base
- **Diffs** : `rebase-784ebd2/SHA256SUMS` vérifié, 13 sur 13 OK.
- **Archive** : `git archive 784ebd2` sur les 4 chemins donne un tar `1665486a…9d0bd` de 52 entrées.
- **Application** : les 13 diffs passent dans l'ordre du brief, `--check` puis `apply`, tous en sortie 0.
- **Index local** : un index git local, sans commit (`init` puis `add -A`), sert seulement à produire `git diff` avec les préfixes a/ b/.
- **Pré-images** : FORMAT `5a9fa6f` et test `5ceb4a0`, soit les post-images de CB-11g ; j'ai vérifié la chaîne des lignes `index`.
- **HEAD du dépôt** : `784ebd2` au début, puis `408a534` à 03:09 (tes commits CB-3a à CB-10a), puis `4b358a2` à 03:14. À `408a534`, les deux fichiers valent `fb46681` et `d317b9f`. CB-11h ne s'applique donc qu'après CB-11g.

## Avant / après

**CC-1**, `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`, §12, dernier paragraphe (l.265-271 avant, l.265-272 après) :
- l.267 avant : `si la suite est mal formée. Tout autre datagramme (écho de la requête, réponse à une autre question, datagramme trop`
- l.267-268 après :
  - `si la suite est mal formée (RFC 1035 §4.1.1-4.1.2).`
  - `Tout autre datagramme (écho de la requête, réponse à une autre question, datagramme trop`
- l.271 avant : `résolution et sans envoi (RFC 1035 §4.1 ; ADR-0029 l.109).`
- l.272 après : `résolution et sans envoi (ADR-0029 l.109).`

La citation est placée à la fin de la phrase d'appariement, comme le dit la liste. Elle ne tenait pas dans la l.267 (116 + 24 = 140 caractères). J'ai donc coupé la ligne à la fin de la phrase, sans reformater le paragraphe : la nouvelle l.268 reprend mot pour mot la fin de l'ancienne l.267. Autre forme possible, à toi de choisir : remplir la ligne jusqu'à 120 et renvoyer « question, datagramme trop » à la ligne suivante. Le diff a le même nombre de lignes.

**CC-2**, `s2bis/tests/test_http_reseau.py`, docstring de `test_contexte_tls_d_urllib` (la l.228 ne change pas, elle finit par « (RFC 8446 ») :
- l.229 avant : `        §4.2.6, extension 49, vide) ; le nom de la requête part en SNI."""`
- l.229 après : `        §4.2 (numéro 49), §4.2.6 (données vides)) ; le nom de la requête part en SNI."""`

La citation se lit donc « (RFC 8446 §4.2 (numéro 49), §4.2.6 (données vides)) ». La première ligne de la docstring, celle que `-v` affiche, ne change pas.

**Facultatif RFC 7301** : non fait. La l.228 passerait de 110 à 138 caractères, alors que ce fichier ne dépasse jamais 120. Si l'on reporte « et l'authentification après poignée (RFC 8446 » sur la l.229, celle-ci monte à 134 et il faut une ligne de plus.

## Contrôles

Tous les contrôles sont lancés depuis la racine de la copie.

**1. Ligne du job `s2bis-unittest`.**
- Elle est extraite octet pour octet des l.217-218 de `gates.yml` (`job-s2bis.sh`, `8834ffd3…c23e`).
- Je la lance par `bash --noprofile --norc -eo pipefail`, sous `unshare -n`, avec `lo` allumée par ioctl.
- Isolement vérifié : la boucle locale répond, 1.1.1.1:53 renvoie Errno 101.

| état | python3 | Ran | verdict |
|---|---|---|---|
| avant | 3.11.15 (tel qu'écrit) | 114 | conforme |
| après | 3.11.15 (tel qu'écrit) | 114 | conforme (code 0, résumé final, aucun saut, Ran = 114) |
| après | 3.12.3 (version de l'image ubuntu-24.04) | 114 | conforme |
| après | 3.10.20 | 114 | conforme |
| après | 3.13.14 | 114 | conforme |

Le plancher reste à 114 : `gates.yml` n'est pas dans le diff.

**2. Runner.** `python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py` sort en 0 avec `verdict-suite-s2 : 33 ok, 0 échec`, avant (3.11) comme après (3.11 et 3.12).

**3. R-13.**
- Le motif est extrait octet pour octet de la l.71 de `gates.yml` : 67 octets, dont 4 octets 92. Son sha256 (avec le LF final) est `a1a6e684…ba71`, et je l'ai contrôlé par `od -c`.
- Le témoin positif trouve ses 2 lignes sur 2.
- Sur les deux fichiers, avant et après, `git grep -nE -f` sort en 1 : 0 marqueur. `grep -c` donne aussi 0 et 0, et 0 sur le diff lui-même.

**4. Octets 92.** FORMAT en a 1 avant et 1 après ; le test, 25 avant et 25 après. Le diff n'en contient aucun.

**5. Hygiène.**
- `git diff --check` sort en 0 ; aucun changement de mode, aucun CR, aucune tabulation.
- Les lignes ajoutées font 51, 88, 42 et 88 caractères.
- Les lignes de FORMAT de plus de 120 caractères sont les mêmes qu'avant (des tableaux, hors du diff).

**6. Reproduction.** J'ai rebâti un arbre neuf (le tar, les 13 diffs, puis `git apply CB-11h.diff`). Il est identique à la copie (`diff -r -x .git` sort en 0), et `--numstat` donne 3/2 et 1/1.

## Points à décider
- **I-1, procédure.** Avec un `unshare -n` seul, `lo` reste éteinte et la ligne du job échoue : `FAILED (failures=21, errors=4)` en 217 s, Errno 101.
  - Je l'ai constaté sur l'état de base, avant toute retouche, puis après : ce sont les mêmes 25 tests (listes normalisées identiques).
  - « Sous unshare -n » doit donc vouloir dire « unshare -n avec lo allumée », comme le fait `isole.sh` du réviseur. Je propose d'en faire une consigne de gabarit.
- **I-2, citation (hors liste fermée, rien modifié).**
  - RFC 1035 §4.1.1-4.1.2 décrit les champs : ID (l.1423-1426), QR (l.1428-1429), QDCOUNT (l.1517-1518) et la question (l.1532-1534).
  - La règle d'appariement elle-même est au §7.3 : l.2543-2546 (l'ID, puis la section question) et l.2531-2532 (écarter les requêtes quand on attend des réponses). On pourrait resserrer en « RFC 1035 §4.1.1-4.1.2, §7.3 ».
  - Placée en fin de phrase, la citation couvre aussi « vient de l'adresse et du port interrogés ». Or le §7.3 (l.2550-2554) note que des serveurs répondent depuis une autre adresse : c'est un choix du lot, pas une règle de la RFC 1035.
  - « Casse ignorée » relève du §2.3.3 (l.480-482).
- **I-3, convention du document.** L'en-tête « Corrections » de FORMAT (l.10-14) liste chaque diff de correction, de CB-11c à CB-11g. CB-11h n'y figure pas, à cause de la consigne de changer le minimum. À toi de dire s'il faut ajouter « CB-11h, CC-1 (§12) ».
- **I-4, couverture.** Je n'ai pas lancé la suite s2-harness : elle n'est pas dans la copie demandée, et le diff ne touche aucun de ses chemins.

## Journal G1

**[lu]**
- le brief ;
- `p1b/rfc/RFC-CITATIONS.md` ;
- `p1b/g2/CONTRE-CONTROLE-P1B-transcrit.md` ;
- dans la copie : FORMAT l.249-273, test l.220-261, `gates.yml` l.55-79 et l.160-221 ;
- RFC 1035 (`d14ae809…fdfb`) : l.478-486, 1349-1356, 1399-1445, 1470-1480, 1515-1571, 2526-2560 ;
- RFC 8446 (`47871bc8…b3bd`) : l.1909-1914, 1923-1946 (`post_handshake_auth(49)` à la l.1941, dans le §4.2 qui commence l.1911 ; le §4.2.1 commence l.2135) et l.2581-2596 (« zero length » aux l.2593-2594) ;
- RFC 7301 (`ba122aee…3222`) : l.139-160, 366-376, avec le §6 qui commence l.343 ;
- ADR-0029 à `784ebd2` (`git show`, `b908842d…cbef`), l.105-112. La l.109 est la ligne D-4, « adresse IPv4 littérale (aucune résolution…) » : elle suffit à soutenir la phrase conservée ;
- `lo_up.py` et `isole.sh` du réviseur (sha256 égaux à ceux de `SHA256SUMS-reviseur`) ;
- `faire_diff.sh`, `mini.sh`, `longueurs.py` ;
- les blocs FORMAT de CB-11f et CB-11g, et les lignes `index` des 13 diffs.

**[2nd]** : aucun.

**[abs]** :
- RFC 5452 : non lue, et non citée.
- RFC 5737 et 2606, citées dans `test_garde.py` : non vérifiées. Ce fichier est hors de la tranche B : il est déjà dans `784ebd2` et absent des 13 diffs.

**Commandes et sorties** : toutes dans `…/cb11h/preuves/` :
- `application-13-diffs.txt` ;
- `avant-*` et `apres-*` (job, runner, mesures) ;
- `*.ensemble.txt` ;
- `temoin-r13.txt`.

J'ai recompté moi-même 114, 33, les octets 92, les longueurs de ligne et les ensembles d'échecs.

**Exposition** : aucun dossier interdit, aucun `*.jsonl`, aucune pièce de D.2. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (`isole.sh` la retire). Aucun accès réseau : toutes les suites tournent sous `unshare -n`. Je n'ai fait aucune recherche récursive : seulement des fichiers nommés ou des globs d'un seul niveau, et un `ls-tree` non récursif sur `docs/adr-0029/`.

**Incidents**
- (a) Mon premier lancement chronométré est sorti en 127 avant tout test, car `/usr/bin/time` est absent. Je l'ai relancé et ne l'ai pas compté.
- (b) J'ai lancé deux fois `git status --short` sur le dépôt, à 02:55 et 03:10. Cette commande peut prendre le verrou optionnel de l'index pour le rafraîchir. Aucune erreur constatée, et je ne l'ai plus utilisée ; la bonne forme est `git --no-optional-locks status`.
- (c) Un `sha256sum -c` lancé depuis le mauvais répertoire (celui du dépôt) a renvoyé « No such file » ; refait dans `cb11h/`, il est OK.

Je n'ai rien écrit dans le dépôt. Les seules commandes git que j'y ai lancées sont `archive`, `show`, `ls-tree`, `rev-parse`, `log`, `cat-file`, `config --get` et `status` (voir b).

## 2. Contre-contrôle bref du réviseur

**Contre-contrôle bref de CB-11h : CONFORME.** CC-1 et CC-2 sont faits exactement, rien n'a été touché hors de ma liste, et aucun des trois points ouverts par le worker ne justifie un CB-11i.

- **Gate 0** : je tourne sous `claude-opus-5-5`.
- **Horloge** : de 03:15:38 à 03:18:08 UTC, le 2026-10-05.
- **Diff** : sha256 `accd8bf7…ebec`, égal à l'annoncé. Il touche deux fichiers, +4 −3 (FORMAT +3 −2, test +1 −1).

## CC-1 et CC-2
- **CC-1, FORMAT §12** :
  - « (RFC 1035 §4.1.1-4.1.2) » suit maintenant la phrase d'appariement.
  - Après la phrase sur l'IPv4 littérale ne reste que « (ADR-0029 l.109) ».
  - La coupure de ligne ajoutée reste dans le même paragraphe Markdown.
- **CC-2, docstring de `test_contexte_tls_d_urllib`** : elle porte « RFC 8446 §4.2 (numéro 49), §4.2.6 (données vides) », mot pour mot.
- **Sur pièce** :
  - RFC 1035 : §4.1.1 commence l.1401, avec ID et QR ; l.1423-1426 dit que l'ID sert « to match up replies » ; §4.1.2 commence l.1530.
  - RFC 8446 : `post_handshake_auth(49)` est l.1941, dans le §4.2 (l.1911) ; « zero length » est l.2593-2594, dans le §4.2.6.
- **Reste des citations** : plus aucune occurrence de l'ancien texte ; les autres citations RFC du lot sont inchangées.

## Contrôles sur 784ebd2 + les 13 diffs recalés + CB-11h
Tout tourne en réseau isolé, `lo` allumée par mon outil.
- **Ligne du job** telle qu'écrite (`--egal --plancher 114`), sous 3.10, 3.12 et 3.13 : conforme, Ran = 114.
- **Runner** : 33 cas, OK.
- **R-13** : le motif est lu dans `gates.yml` ; il a la même empreinte que `motif-r13.txt` du worker (`ce8609f6…`). Sur les 14 fichiers du lot, `git grep` sort en 1 avec 0 ligne. Sur les lignes ajoutées du diff : 0.
- **Octet 92** : 0 dans les lignes ajoutées et 0 dans tout le diff. Avant et après, le FORMAT en compte 1 et `test_http_reseau.py` 25.
- `xtask` n'a pas été relancé : la demande ne le comprenait pas, et le diff ne touche que du texte.

## Avis sur les trois points ouverts par le worker
- **I-2 : moins précis, pas faux.**
  - La citation renvoie aux sections qui définissent les champs de l'appariement (ID, QR, nombre de questions, question). §4.1.1 l.1423-1426 donne en outre le rôle d'appariement de l'ID.
  - La clause « vient de l'adresse et du port interrogés » est un choix du lot. RFC 1035 §7.3 (l.2550-2554) avertit d'ailleurs qu'un serveur peut répondre depuis une autre adresse. Avec la règle du lot, ce cas donne `delai`, c'est-à-dire un échec D-4 ou D-5, que le rodage mesurerait.
  - Proposition, au prochain diff qui touche le FORMAT (CB-18) : citer aussi §7.3 et marquer la règle de source comme choix du lot.
- **I-3 : incomplet, pas faux.** L'en-tête « Corrections » liste les diffs de correction de la G2 ; CB-11h applique une correction du contre-contrôle. Il suffit de l'ajouter au prochain diff qui touche le FORMAT.
- **I-1** : sans effet sur mes contrôles. L'item HARNAIS-UNSHARE-LO-1 est déjà formé.

## Exposition et état
- Aucune opération git en écriture, aucun dossier interdit ouvert.
- Mes arbres temporaires sont supprimés.
- À 03:18 UTC, `git status` du dépôt montre 7 entrées : ce sont les commits de l'orchestrateur en cours, pas mon fait.

Preuves dans `…/p1b/g2/travail/preuves/` :
- `h-job-python3.12.txt` (`0ab3949d…`)
- `h-job-python3.10.txt` (`e0034a42…`)
- `h-job-python3.13.txt` (`1a977e32…`)
- `h-runner.txt` (`994ba82f…`)
- `h-r13.txt` (vide)
