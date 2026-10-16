# Relecture G2 neuve des amendements, phase 1 (ACCEPTE) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:39:39 UTC du fichier publication-amendements/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur et du réviseur G2 (deux relectures) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve — lot PUBLICATION-S2-AMENDEMENTS (SHOGEN-PUBLICATION-S2-AMENDEMENTS-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max. Réviseur G2 distinct du générateur : je n'ai écrit aucun des quatre diffs.
- **Rattachement (G0)** : annexe B d'ADR-0028, §B.98, item SHOGEN-PUBLICATION-S2-AMENDEMENTS-1 (`ANNEXE-B-items.md` l.1704, fichier
  `677a8e51…e035`) ; engagements de `docs/publication/envoi-preavis/reponses/COINGECKO-2026-10-10.md` §4 (l.97-104, fichier
  `2f4669ad…3514`, lu en entier) ; brief G2 de l'orchestrateur (24 l., lu en entier).
- **Heures** (`date -u`) : ouverture Thu Oct 15 20:59:48 UTC 2026 ; rédaction Thu Oct 15 21:19:41 UTC 2026.
- **Base** : tête `0dd5fe5710d969130a3092b8ee6b03b0333050b5` à l'ouverture. La tête a avancé pendant la relecture, jusqu'à
  `d48818f40d0413d26ba2665167f9119df0188a4c` (commits DETTES-T7 `3f30dc1`, `7b8f999`, `d48818f`). `git diff --stat` entre les deux
  têtes, limité à la liste explicite des pièces relues, est vide ; les trois fichiers cibles ont les mêmes sha256 aux deux têtes.
- **Pièces relues** : `diffs/PA-a.diff`, `PA-c.diff`, `PA-b.diff`, `PA-d.diff`. `sha256sum -c` du `SHA256SUMS` du générateur : 53 OK.
  Empreinte de la série relue (concaténation PA-a, PA-c, PA-b, PA-d) :
  `58ba49e43d14f5dfd8ec71f0f7cd339b6f62ceba1f8a0e752fb7edcd92f899d4`.
- **Règles tenues** : dépôt en lecture seule, aucune commande git en écriture, aucune liste par motif sur `docs/`, `cargo xtask verify`
  non lancé, pas de réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. TMPDIR sous `g2/tmp` pour les tests.

## Verdict : ACCEPTE

Aucune correction (liste C vide, `g2/diffs/` vide). Cinq observations non bloquantes (O-1 à O-5). Les six items L-1 à L-6 du générateur
sont fondés ; L-1, L-2 et L-3 sont à trancher par l'orchestrateur avant la publication (échéance 2026-10-25). Ils ne sont pas dans
le mandat du lot.

## 1. Checklist, verdict par point

**1. Application et lignes : OK.**
- Copie de base = `git show HEAD:<chemin>` des trois fichiers, hors dépôt. Sha256 de base égaux à l'arbre : EN `60f7dc7a…21d6`
  (760 l.), FR `c101998b…6561` (1081 l.), `glossaire_en.py` `4beaf064…d76c` (514 l.).
- `git apply --check -v`, chaque diff seul sur la base : sortie 0, quatre fois. Application en série (a, c, b, d) : sortie 0, quatre fois,
  `Applied patch … cleanly`, aucun décalage de bloc.
- Fichiers amendés égaux à l'octet aux finaux du générateur : EN `284acb3e…50e5` (760 l.), FR `f5eddc6a…9d11` (1081 l.),
  glossaire `86d44bbb…3d83` (521 l.).
- Mon outil `outils/lignes_g2.py` : lignes changées EN [23, 62, 90, 202, 244, 253, 437, 547, 672, 714, 715] ; FR [51, 120, 161, 370,
  393, 681, 883] ; glossaire [7, 40, 42, 186, 450, 453] et 515-521 ajoutées en fin. Ce sont les lignes déclarées ; aucune ligne
  numérotée ne se décale.

**2. Valeurs, verdicts, blocs copiés, citations : OK.**
- Mon outil `outils/invariants_g2.py` (aucune barre oblique inverse, contrôlé par `od -c`) :
  - aucune ligne changée dans un bloc de code (EN : bloc 6 aux l.222-242 ; FR : l.343-363) ;
  - chaque ajout garde la ligne d'origine en préfixe exact ;
  - substitutions : nombres identiques et dans l'ordre, sauf EN l.714 (renvoi `§9.3 pt 8` ajouté à la note) ;
  - nombres retirés : aucun, en EN comme en FR ; nombres ajoutés : ceux des trois ajouts datés seulement (date, heure, renvois,
    chemin `r2.py`, `ed479c5`) ;
  - comptes des mots de verdict inchangés.
- Mon outil `outils/citations_g2.py`, sur le texte entier : citations entre guillemets français EN 151 = 151, FR 146 = 146 (dont 27 sur
  plusieurs lignes), identiques et dans le même ordre. S-G5 voit donc les mêmes fragments.
- Étiquettes scellées inchangées : `(panne / stale / horsE / nonÉv)` (EN l.202 et l.672, FR l.323) et `panne_transport` ; seul ajout,
  `panne_transport` une fois par langue, dans l'ajout du §7.5.

**3. Engagements de la section 4 : tenus.**
- (i) `grep -n -i outage` sur l'anglais amendé : l.553 et l.714 seulement, trois occurrences. Dans la base : neuf lignes (l.23, 62, 90,
  202, 547, 553, 672, 714, 715). La l.553 (`nothing shows an outage of Pyth`, §9.3 pt 8) reste. La note de la l.714 garde le sens
  ordinaire, comme l'a décidé l'orchestrateur ; son renvoi au §9.3 pt 8 est exact. `failed-reading` (l.23) est la forme épithète, comme
  `out-of-envelope` dans la même ligne. Les autres mots en `fail` sont l'énoncé scellé (`co-failure of the sources`) ou des statuts
  du harnais (`resolve_failed`), hors engagement.
- (ii) Note exacte sur le fond. `ed479c5:s2-harness/shogen_s2/r2.py` (sha256 `8c42f336…`), arête `"kind": "upstream"`, binance vers
  coingecko : champ `relation` = `intégration (table des marchés spot, … — chiffre daté) ; granularité « intégration », pas
  « ticker-set » (§3.2)`, `doc_url` = `coingecko.com/en/exchanges/binance`. `METHOD_EDGES` est identique à `f35a70c`, le commit
  d'analyse (52 l., sha256 `546aba37…` aux deux commits, `cmp` 0).
  - Effets de l'arête relevés par `git grep` sur la liste explicite des modules : `basis_doc_triggered` (une étiquette
    `basis:doc→(b)` dans `report.py`), la ligne `amont déclaré (basis:doc, ne fusionne pas)` et la ligne du (c) AXE MÉTHODE.
    `compute_content` calcule toutes les paires ; `compute_partition` n'utilise jamais `basis:doc` seul. L'arête ne change donc aucune
    valeur et aucun verdict : la phrase `no effect on any result` est exacte.
  - Le rapport nomme déjà `ed479c5` `collection commit` (EN l.630, FR l.1062).
  - Le bloc 6 copié n'a pas changé.
  - Le mot `nombreuses` de l'engagement n'est pas repris (O-1).
- (iii) Phrase conforme (EN l.437, FR l.681) : un φ élevé décrit des lectures que le harnais n'a pas obtenues dans les mêmes fenêtres ;
  il n'établit pas une dépendance entre fournisseurs. Renvois relus sur la copie amendée :
  - §9.3 pt 2 = l.547 / l.883 (anomalies presque toutes des lectures en échec) ;
  - §2.7 (un hôte de collecte, un résolveur par relevé ASN) ;
  - §5.2 (`it describes the composition of K`) ;
  - §11.1 (concentration de K dans les démarrages à `resolve_failed` ; `compatible with a common mode of the observer, without
    establishing it`).
  Les quatre renvois sont exacts dans les deux langues.

**4. Cohérence EN/FR : OK.** Selon `interne/TABLE-CORRESPONDANCE-EN.md` (`74bf3680…`) :
- EN l.23/FR l.51 (§1) ;
- l.62/l.120 (lexique) ;
- l.90/l.161 (§2.1) ;
- l.244/l.370 (§4.1) ;
- l.253/l.393 (§4.2) ;
- l.437/l.681 (§7.5) ;
- l.547/l.883 (§9.3 pt 2).

Les ajouts portent le même contenu et la même marque datée (2026-10-15 20:37:28 UTC). EN l.202 n'a pas de pendant à changer : FR l.323
porte l'étiquette scellée sans glose. Une différence de forme reste, sans effet sur le sens (O-2).

**5. PA-d et `controle_en` : OK.**
- Nouvel état de `glossaire_en.py` :
  - l.7, empreinte courte `f5eddc6a…9d11` ;
  - l.42, `SOURCE_SHA256` = sha256 du français amendé ;
  - l.186, glose G-26 `failed reading / stale / out-of-envelope / not evaluable` ;
  - l.450 et l.453, égales aux l.714 et 715 du glossaire final ;
  - note A-8 en fin de fichier (l.515-521) ;
  - l.40 garde 120 caractères ; aucun octet 0x5C ; syntaxe Python 3.11 valide.
- `controle_en.py` de la tête (`b42777db…bb4c`, inchangé), sous `-X dev -W error` :
  - base : CONFORME 11/11, sortie 0 ;
  - textes amendés avec le glossaire d'origine : FATAL, sortie 3 (épingle). C'est l'étape rouge ;
  - copie amendée : CONFORME, onze contrôles sur onze, sortie 0, aucune ligne Warning. Même sortie que le générateur, aux chemins près.
- Tests (`lancer_tests.py`, sur la copie amendée) : 101 tests OK sous Python 3.11.15, 3.12.3 et 3.13.14, sortie 0, aucune ligne
  Warning. Ces tests utilisent des données réduites, pas le glossaire réel.
- Table de correspondance régénérée (`--table`) : sha256 `5647f44f…`, égale à celle du générateur. Elle ne diffère de la table versée
  que par les empreintes et par les comptes des sections 4.1 (84 devient 88), 4.2 (35 devient 38) et 7.5 (51 devient 58).
- `verifier_pa.py` du générateur, lu en entier (235 l.) et rejoué sur mes copies : base vers amendée CONFORME, sortie 0 ; base vers
  base NON CONFORME (23 écarts), sortie 1.

**6. Items L-1 à L-6 : tous fondés.**
- L-1 fondé. EN l.7 dit `no number is changed or added`, FR l.13 dit `aucun nombre n'est changé ni ajouté` (lus sur la copie amendée).
  Les ajouts datés y ajoutent une date, une heure, des renvois et un chemin. EN l.3 (`numbers, verdicts and sealed labels are
  identical to the original`, épinglée par `ENTETE_PHRASE`) reste exacte face à l'original français traduit (contrôle 2 de
  `controle_en` conforme). Le correctif touche l'en-tête des deux langues, donc l'épingle de PA-d et le contrat de L-2 : à trancher
  avec L-2, avant la publication.
- L-2 fondé. Sortie `controle_public` du générateur avec la table étendue : NON CONFORME sur le contrôle 1 seul
  (`aucun inventé, aucun ajouté`) ; les nombres inventés sont la date, l'heure et le chemin `r2.py` des ajouts. Décision de
  l'orchestrateur. L'outil est au scratchpad, il n'est pas versé.
- L-3 fondé. `docs/11` vaut `fcf93b87…53b7` à `2db4f40` et `10f368da…52c9` à la tête. `6c04e91` (2026-10-10, DETTES-T14) y ajoute
  49 lignes en fin (`@@ -1069,3 +1069,52 @@`), absentes des versions publiques.
- L-4 fondé. `interne/ACTEURS-NOMMES.md` (`ac4d6f6a…`) l.52-53 paraphrase la définition par `une panne`. Pièce interne : à aligner
  dans un lot à venir.
- L-5 fondé. `ed479c5:s2-harness/shogen_s2/sources.py` lit par `urllib.request.urlopen`, donc par la résolution du système de l'hôte ;
  le résolveur du §2.7 est celui des relevés ASN. La même formule figure déjà au §9.3 pt 5 du rapport, qui précède le lot : ce n'est
  pas un défaut du lot.
- L-6 fondé. Les sorties versées décrivent l'état d'avant (exemple : la table versée porte les sources `c101998b…` et `60f7dc7a…`).

**7. Écarts E-1 à E-5 du générateur : rien d'une pièce interdite n'a été lu.** Contrôle fait sur `RAPPORT-GENERATEUR.md` et
`NOTES.md` seulement, contre la liste fermée D.2 (annexe D l.32-47, lue sans rien ouvrir).
- Les lectures du générateur sont toutes hors D.2 et hors des dossiers interdits.
- E-1 : des noms ont été affichés depuis des pièces internes autorisées. Pour un fichier de `docs/rapports/`, seul un `test -e` a été
  fait, sans ouverture.
- E-2 n'est pas une lecture : c'est un écart à la règle sans réseau. Chromium, lancé sans TMPDIR, a tenté des connexions HTTPS de
  fond, en échec TLS. L'écart est déclaré ; l'orchestrateur l'adjuge.
- E-3 et E-4 : aucun effet sur les pièces.

**8. PDF : OK.**
- `sorties/pdf/Shogen-S2-pilot-measurements-DRAFT.pdf` : sha256 recalculé
  `fcea115a9af288440bcdf59b1840ca1538fe5b0d86bbf4b307159683f6569726`, égal au rapport ; 851624 octets.
- `pdfinfo` : 17 pages ; recompte indépendant des objets `/Type /Page` : 17.
- `pdftotext` :
  - `outage` 3 ; `failed reading` 8 ; `failed-reading` 1 ;
  - trois `Addition dated 2026-10-15` ; mention `Draft — not published` présente ;
  - dernière ligne `Source file sha256: 284acb3e…`, l'anglais amendé.

## 2. Observations (non bloquantes, aucune correction demandée)

- **O-1 — engagement (ii), mot `nombreuses`.** COINGECKO §4 l.101 et B.98 l.1704 disent `une source parmi les nombreuses que
  CoinGecko agrège` ; le courriel (l.56) dit `one of the many sources CoinGecko aggregates`.
  - La note dit `one of the exchanges whose markets CoinGecko integrates`, ni source unique ni principale : le sens est tenu, le
    quantificateur ne l'est pas.
  - Elle reprend mot pour mot le brief du générateur et le point 3 du courriel.
  - Je ne corrige pas : `many` n'a pour source détenue que le message de CoinGecko (correspondance privée). À l'orchestrateur de dire
    si le mot doit figurer.
- **O-2 — FR l.120.** L'anglais insère `is` (`has a failed reading (…), is stale (…)`). Le français garde `s'il a une lecture en échec (…),
  en staleness (…) ou hors enveloppe (…)`. Cette phrase se lit `une lecture en échec, en staleness ou hors enveloppe` : même sens,
  construction différente.
- **O-3 — étiquette `panne` en français.** Le texte courant français ne dit plus `panne`. L'étiquette scellée (l.323, bloc l.576,
  `panne_transport`) ne s'y relie que par l'ordre des colonnes et la précédence de la l.161 ; l'anglais a le glossaire (l.714).
  Une glose française éventuelle relève d'un lot à venir.
- **O-4 — style de `glossaire_en.py`.** Deux lignes dépassent la largeur du fichier : l.7 (147 caractères) et l.450 (132). La base en
  avait une seule, l.79 (123). Aucune gate ne couvre ce dossier : aucun job de `gates.yml` ne porte sur `scripts/publication/en`.
- **O-5 — nom A-8.** Dans `glossaire_en.py`, `A-8` désigne déjà l'amendement d'ADR-0028 du titre §10.3 (l.133-134). Dans la phrase de
  fermeture, écrire `amendement A-8 du glossaire`.

Enregistrement du rôle G2 par `oracle_record.py` : je ne l'ai pas fait. Ce lot de publication vient après le cp-2 de S2
(`docs/adr-0028/CP2-S2.md`, 2026-10-04) et le brief n'en parle pas ; l'outil aurait aussi lancé la suite `s2-harness`, processus lourd
pendant la chaîne. À adjuger par l'orchestrateur.

## 3. Expositions et écarts du réviseur

- **E-1** : `git show ed479c5:s2-harness/shogen_s2/sources.py | sed -n '30,60p'` a affiché la constante User-Agent du harnais, qui
  porte l'adresse d'un dépôt (nom retiré du public). C'est du code, pas une pièce D.2. L'adresse n'est recopiée ni dans NOTES ni ici.
- **E-2** : un `grep` des titres et de `D.2` dans `ANNEXE-D-preenregistrement.md` a affiché des lignes de D.1 et D.3 : noms de dépôts
  privés, chemins locaux, sujets de lectures. Ce sont des noms seulement ; aucun contenu de pièce D.2 n'a été ouvert.
- Les sorties de `controle_public` du générateur n'ont été lues que pour leurs verdicts et leur contrôle 1. Les libellés de motifs
  n'ont pas été affichés.

## 4. Journal de provenance (G1 du réviseur ; détail horodaté dans `NOTES.md`)

Sources [lu], sha256 recomptés par outil :
- brief G2 et brief du générateur ;
- `RAPPORT-GENERATEUR.md` et `NOTES.md` du générateur ;
- les quatre diffs ; `verifier_pa.py` ; `mutants_pa.sortie.txt` ;
- `COINGECKO-2026-10-10.md` en entier ;
- B.98 ; annexe D l.32-47 ;
- les deux rapports aux lignes et sections touchées et renvoyées (§1, lexique, §2.1, §2.7, §3.5, §4.1, §4.2, §5.2, §7.5, §9.3, §11.1,
  glossaire) ;
- `TABLE-CORRESPONDANCE-EN.md` ; `ACTEURS-NOMMES.md` l.48-56 ;
- `controle_en.py` (en-tête, `main`, `controle_entete`) ; `test_controle_en.py` (en-tête) ; `lancer_tests.py` ;
- `r2.py` à `ed479c5` et `f35a70c` ; `report.py` aux deux commits (lignes de l'arête) ; `sources.py` à `ed479c5` l.30-60 ;
- `xtask/src/sg4.rs`, `sg9.rs` (en-tête) ; `gates.yml` (noms des jobs) ; `CP2-S2.md` l.1-45.

[2nd] : aucun chiffre de seconde main ; chaque compte cité ci-dessus est affiché par un outil dans ce journal.

Commandes principales, avec leur sortie (toutes dans `NOTES.md`) :
- `git apply --check` et `git apply` ;
- `lignes_g2.py`, `invariants_g2.py`, `citations_g2.py` ;
- `controle_en.py`, trois cas, et sa table ;
- `lancer_tests.py` sous trois versions de Python ;
- `verifier_pa.py`, deux cas ;
- `pdfinfo`, `pdftotext`, recompte des pages ;
- `git diff --stat`, `git log`, `git grep`, chacun sur une liste explicite de chemins.

## 5. Livrables (`g2/`)

- `RAPPORT-G2.md` ; `NOTES.md` ;
- `outils/lignes_g2.py`, `outils/invariants_g2.py`, `outils/citations_g2.py` ;
- `sorties/` : sorties de `controle_en`, des tests et de la table régénérée ;
- `work/` : copies de base, amendée et rouge, texte du PDF, résultats des invariants ;
- `diffs/` : vide, aucune correction ;
- `SHA256SUMS`, écrit en dernier.
