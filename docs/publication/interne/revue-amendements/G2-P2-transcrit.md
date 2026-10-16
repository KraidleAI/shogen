# Relecture G2 des amendements, phase 2 (ACCEPTE-AVEC-CORRECTIONS, C-1 hors dépôt) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:39:39 UTC du fichier publication-amendements/g2/RAPPORT-G2-P2.md ; contrôle FM-1.1 des transcripts du générateur et du réviseur G2 (deux relectures) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 — phase 2 du lot PUBLICATION-S2-AMENDEMENTS (SHOGEN-PUBLICATION-S2-AMENDEMENTS-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max. Même réviseur G2 qu'en phase 1, distinct du générateur ; je n'ai écrit ni
  PA-e, ni PA-f, ni PA-g, ni l'outil modifié.
- **Rattachement** : demande du coordinateur ; `ADJUDICATION.md` de l'orchestrateur (sha256 `64be462a…24fd`, lue en entier),
  décisions 2 et 3 ; section « Phase 2 » de `RAPPORT-GENERATEUR.md` (l.229-365 ; les l.1-227 sont inchangées).
- **Heures** (`date -u`) : ouverture 21:43:11 UTC ; rédaction après 21:57:54 UTC (2026-10-15).
- **Base** : tête `364f43f1a959996aa3a6d664fab7f1d11e712df2`, puis `bfd88fa6903072cb6bc5c33783f4e5fab162d346` (deux commits DETTES-T7,
  dont `894ef46`). `git log` entre les deux têtes, limité aux huit fichiers touchés, est vide ; PA-a à PA-d n'y sont pas encore commis.
- **Pièces relues** :
  - `diffs/PA-e.diff`, `PA-f.diff`, `PA-g.diff` ;
  - les diffs de revue de l'outil et des tests ;
  - `outils-public/`, `tests-public/` ;
  - le PDF `sorties/pdf-p2/`.
  `SHA256SUMS` du générateur : 114 lignes, 114 OK. Empreintes de concaténation :
  - série de la phase 2 (e, f, g) : `d1eda681bd4a792a3c1abb20393a77fcedae36bce6f7d6fbb2abaf9e30f00574` ;
  - série complète (a, c, b, d, e, f, g) : `08f49e911b599a5a0ecd59b5e7f49a21c191a4d473a1e4fbfb194c47456d7420`.
- **Règles** : tout est vérifié sur des copies hors dépôt. Aucune commande git en écriture, pas de `cargo xtask verify`, pas de réseau,
  un seul processus à la fois.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée : C-1)

- **PA-e, PA-f et PA-g sont acceptés à l'octet** : aucune correction ne touche un fichier du dépôt.
- **C-1** ajoute cinq tests au fichier de tests de `controle_public`, qui est hors dépôt (L-8).
  - Diff : `g2/diffs/C-1.diff`, sha256 `9274d1d7395bf24a42b605ac5945503cf2b23b1fe640101d129ea76a865cf5bb`, 37 lignes ajoutées,
    0 retirée. Il s'applique avec `git apply` depuis le dossier du lot, sur `tests-public/test_controle_public.py`.
  - Fichier obtenu : `dbf9a523…`.
  - C-1 est à appliquer avant tout versement de l'outil.

## 1. Points demandés

**(1) Application et lignes : OK.**
- Copie bâtie avec `git show` de la tête. Les sept diffs ont été appliqués un à un, dans l'ordre a, c, b, d, e, f, g, avec
  `git apply --check` puis `git apply` à chaque pas : sortie 0 sept fois, `cleanly`, aucun décalage de bloc.
- État final égal à l'octet aux huit fichiers finaux du générateur (`sha256sum -c` : 8 OK).
- Lignes (`outils/lignes_g2.py`) :
  - anglais : 760 lignes, toujours 760 ; seules les lignes déclarées changent, plus la l.7 ;
  - français : 1081, toujours 1081 ; lignes déclarées, plus la l.13 ;
  - `ACTEURS-NOMMES.md` : 104, toujours 104 ; seule la l.52 change ;
  - `TABLE-CORRESPONDANCE.md` : 59 devient 72 ; les l.3, 6 et 7 changent sur place, les l.60-72 sont ajoutées en fin ;
  - `glossaire_en.py` : 514 devient 525 ; les l.7, 40, 42, 186, 450 et 453 changent sur place, les l.515-525 sont ajoutées en fin.
- La sortie régénérée `controle_public.sortie.txt` passe de 158 à 159 lignes (ligne du contrat insérée à la l.10). Aucun renvoi par
  numéro vers elle dans les G1/G2 de DOCS11-PUBLIC et DOCS11-EN, `JOURNAL.md`, l'annexe B et les pièces d'envoi (recherche ciblée).

**(2) Substitutions de PA-e : exactes.** Mon outil `outils/pae_g2.py` vérifie chaque ligne : ancre trouvée une fois, et la ligne finale
est l'ancienne avec le seul remplacement prévu.
- FR l.13 : la clause est le texte de la décision 2, mot pour mot.
- EN l.7 : `no number is changed or added, except the dates of the dated additions of 2026-10-15`, même sens.
- `ACTEURS-NOMMES.md` l.52 : `une panne` devient `une lecture en échec` (décision 3).
- Effets :
  - citations inchangées (EN 151, FR 146, ACTEURS 25) ;
  - seul nombre ajouté : la date 2026-10-15, une fois par en-tête ;
  - aucun nombre retiré ; comptes des mots de verdict inchangés.

**(3) `controle_en` : OK.**
- CONFORME 11/11 après PA-d, après PA-f et sur l'état final (sortie 0, sans Warning, glossaire `d909935c…`).
- FATAL (sortie 3, épingle `5de6e716…` contre `f5eddc6a…`) entre PA-e et PA-f. C'est L-9, consigné.

**(4) Contrat L-2 de `controle_public` : OK sur le code ; tests incomplets, d'où C-1.**
- Outil : l'original est `35ba9a6c…`, celui épinglé par `docs/G1-lot-DOCS11-PUBLIC.md` l.401 ; la copie modifiée est `44265e7f…`. Le diff
  de revue égale `diff -u` entre les deux.
- Seul le contrôle 1 change. Les exclusions sont bornées dans le code :
  - liste fermée par numéro ;
  - `après = avant + suffixe` ;
  - marque ` *Ajout daté du AAAA-MM-JJ hh:mm:ss UTC* : ` en tête du suffixe ;
  - une seule ligne ;
  - suffixe trouvé une seule fois dans le brouillon ;
  - mention limitée aux jetons des dates retenues, chaque date une fois.
  Sans ajout déclaré, les nouveaux calculs reviennent aux fonctions d'origine.
- Tests (copies dans `g2/work/p2/public`) :
  - outil modifié : 99 OK ;
  - outil d'origine : 99 lancés, 4 FAIL (exclusion, ajout mal formé sans nombre, liste fermée, mention) ;
  - suite d'origine : 87 OK, sur l'outil d'origine comme sur l'outil modifié.
- Mutants du générateur : 7 sur 7 tués, d'après sa sortie. Son lanceur ne pose ni groupe de processus ni borne de temps.
- Ma campagne (`outils/mutants_public_g2.py`) : groupe de processus neuf, borne de 300 s, `os.killpg` au dépassement ; elle mute aussi les
  sites d'appel et les données passées sous étiquette.
  - Résultat : 18 mutants, 11 tués, 7 vivants, 0 FATAL.
  - G10 (ajout sur plusieurs lignes), G11 (marque cherchée hors de la tête du suffixe), G12 (heure non exigée), G13 (date permise
    plusieurs fois) et G15 (heure permise dans une mention) ne sont tués par aucun test. La table convertit ` ⏎ ` en saut de ligne, donc
    G10 est atteignable.
  - G14 et G17 sont équivalents pour la sortie : `outils/equivalents_g2.py` montre que l'outil complet rend la même sortie, muté ou non.
    Sous G14, le contrôle 5 garde le verdict NON CONFORME ; sous G17, la sortie est identique.
- Avec C-1 : 104 tests OK sur l'outil modifié ; l'outil d'origine garde les mêmes 4 FAIL ; ma campagne rejouée donne 16 tués sur 18.
  Chacun des cinq nouveaux tests tue exactement son mutant ; il reste les deux équivalents. Aucun processus de mes groupes ne reste
  (`ps` filtré par groupe : vide).
- Sur l'état final : CONFORME 7/7. Les comptes après exclusion égalent ceux de la sortie d'origine (0 inventé, 0 ajouté, 11 retirés) ;
  rejeu des 28 retouches identique à l'octet.

**(5) PA-g : OK.** J'ai régénéré les trois sorties sur l'état final, avec les chemins relatifs de PA-g, dans l'arbre
`work/p2/regen`, avec `docs/11` à `2db4f40` (`fcf93b87…`). Les trois sont identiques à l'octet à celles de PA-g :
- `controle_en.sortie.txt` `165223a7…` ;
- `TABLE-CORRESPONDANCE-EN.md` `ddb4a5b0…` ;
- `controle_public.sortie.txt` `df05cdb9…`.

**(6) PDF : OK.**
- Sha256 `aa3e580225c5de10fbbc688ba0904561cd01c4cfc7f0a06b118bfdcb43e2bfd7`, égal à celui du coordinateur ; 851608 octets.
- 17 pages selon `pdfinfo`, selon les objets `/Type /Page` et selon les sauts de page.
- `pdftotext` :
  - la clause d'en-tête est présente ;
  - `outage` 3 ; `failed reading` 8 ; `failed-reading` 1 ;
  - trois ajouts datés ; mention `Draft — not published` présente ;
  - dernière ligne `Source file sha256: 34d5b233…`, l'anglais final.

**(7) Items L-7 à L-10 : tous fondés.**
- L-7 fondé. L'outil de relevé, sur le brouillon final, compte Binance 32 et CoinGecko 24, avec la l.370 en plus. `ACTEURS-NOMMES.md`
  §1 dit encore 26 et 18, et sa l.7 vise `c101998b…`. C'est hors du mandat de la décision 3 : à former en item. Les deux notes
  datées nomment justement Binance et CoinGecko.
- L-8 fondé. `git ls-files` sous `scripts/publication/` : 7 fichiers, aucun outil public.
- L-9 fondé, et plus large que déclaré. La série de la phase 1, adoptée en quatre commits, laisse déjà `controle_en` NON CONFORME après PA-a
  et PA-c, et FATAL après PA-b, jusqu'à PA-d. `controle_public` est NON CONFORME de PA-b à PA-e et CONFORME après PA-f. Recommandation :
  commiter les sept diffs à la suite, sans commit intercalé. Aucun de ces deux outils n'est une gate de CI.
- L-10 fondé, traité par PA-f l.3.

## 2. C-1 — les cinq tests (ajoutés à la fin de la classe `ContratAjoutsDates`)

Chaque test a une valeur attendue posée à la main (sortie 1) ; il passe sur l'outil modifié et tue son mutant :

| test | mutant tué | ce qu'il fixe |
|---|---|---|
| `test_ajout_date_dont_la_marque_n_ouvre_pas_le_suffixe` | G11 | la marque ouvre le suffixe ; un nombre écrit avant elle reste compté |
| `test_ajout_date_sur_deux_lignes` | G10 | un ajout daté tient sur une ligne |
| `test_ajout_date_sans_heure` | G12 | la marque porte l'heure `hh:mm:ss` |
| `test_mention_de_la_date_deux_fois` | G13 | chaque date n'est permise qu'une fois dans une mention |
| `test_mention_qui_ajoute_l_heure` | G15 | une mention n'ajoute que les jetons de la date |

## 3. Observations (non bloquantes)

- **O-P2-1 — portée de la clause d'en-tête.** Les ajouts datés portent, en plus de leur date, l'heure, des renvois de section, `ed479c5`
  et un chemin. Le contrat de l'outil les exclut en entier, alors que la clause ne nomme que les dates.
  - Au sens ordinaire (nombre = valeur), la clause est exacte.
  - La phrase de fermeture proposée, `les dates des ajouts datés du 2026-10-15 sont les seuls nombres ajoutés`, va plus loin. À
    nuancer, par exemple : hors des ajouts datés, l'en-tête n'ajoute que leur date.
  - Le libellé est fixé par l'adjudication : je ne le corrige pas.
- **O-P2-2.** `glossaire_en.py` l.40 dit encore `(amendements A-7 et A-8)`, alors qu'A-9 a réépinglé la source. Corriger cette ligne
  changerait l'empreinte du glossaire, qui est imprimée dans PA-g.
- **O-P2-3.** `ACTEURS-NOMMES.md` l.52-53 se lit `une lecture en échec, … de la lecture faite par le harnais` (redondance). Ce libellé
  est fixé par la décision 3.
- **O-P2-4.** `controle_public.sortie.txt` nomme `../../11-mesures-pilotes.2db4f40.md`, fichier absent du dépôt. Écrire la recette de
  rejeu dans le message de commit ou au JOURNAL : extraction de `docs/11` à `2db4f40` sous ce nom, dossier courant
  `docs/publication/interne`, outil `44265e7f…`. Sans elle, et tant que L-8 reste ouvert, la sortie ne se rejoue pas depuis le dépôt seul.
- **O-P2-5.** Le lanceur de mutants du générateur n'a ni groupe de processus ni borne de temps. Rien n'en résulte ici : les runs sont
  courts, et ma campagne bornée ne laisse aucun reste.

## 4. Exposition du réviseur (phase 2)

- **E-3** : le contexte de PA-f a affiché les dernières lignes G-16 à G-18 de la table interne : identifiants d'items, renvois aux
  numéros de D.2, désignation générique du poste. Ce sont des noms seulement ; aucun contenu de pièce D.2 n'a été affiché.
- La section 2 (motifs) de `controle_public.sortie.txt` n'a pas été affichée.

## 5. Journal de provenance (détail horodaté dans `NOTES-P2.md`)

Sources [lu], sha256 recomptés par outil :
- `ADJUDICATION.md` ; section Phase 2 du rapport et des NOTES du générateur ;
- PA-e, PA-f, PA-g ; les deux diffs de revue ;
- `controle_public.py`, original et modifié (fonctions du contrôle 1, `table_retouches`, `main`) ;
- `test_controle_public.py` (aide `Contrat.lancer`, classe ajoutée) ; `lancer_tests.py` ;
- `ACTEURS-NOMMES.md` l.1-22 ;
- G1/G2 de DOCS11-PUBLIC et DOCS11-EN (lignes qui citent les sorties).

[2nd] : aucun chiffre de seconde main.

Commandes, avec leur sortie :
- `git apply` pas à pas ;
- `lignes_g2.py`, `pae_g2.py`, `citations_g2.py`, `invariants_g2.py` ;
- `controle_en`, sur sept états ;
- `controle_public`, sur quatre états intermédiaires et sur l'arbre de rejeu ;
- tests, sur quatre combinaisons, puis deux avec C-1 ;
- mutants, deux campagnes ; `equivalents_g2.py` ;
- `pdfinfo`, `pdftotext` ;
- `acteurs_nommes.py` ;
- `git log`, `git ls-files`, `git show`, chacun sur une liste explicite de chemins.

## 6. Livrables (`g2/`)

- `RAPPORT-G2-P2.md` ; `NOTES-P2.md` ;
- `diffs/C-1.diff` ;
- `outils/pae_g2.py`, `outils/mutants_public_g2.py`, `outils/equivalents_g2.py`, `outils/inserer_c1.py` ;
- `sorties/p2/` ;
- `work/p2/` : copies, états successifs, arbre de rejeu, tests corrigés ;
- `SHA256SUMS`, réécrit en dernier pour les deux phases. Les fichiers de la phase 1 sont inchangés.
