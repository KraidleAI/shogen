# Journal de provenance G1 — lot DOCS11-PUBLIC (brouillon de la version publique filtrée de `docs/11`)

Worker du lot (fiche `shogen-worker`), instance neuve. Ouvert le 2026-10-04, horloge lue `date -u` →
`Sun Oct  4 13:23:42 UTC 2026` ; fermé à 14:1x UTC. Rien n'est publié ; aucune opération git en écriture.

## Gate 0

Identifiant de modèle déclaré par l'environnement : `claude-opus-5-5` (préfixe attendu `claude-opus-5-5` : conforme).
Effort `max` demandé par le brief ; non observable de l'intérieur de la session.

## Brief et rattachement (G0)

- Brief `…/scratchpad/s2bis/docs11pub/BRIEF-DOCS11-PUBLIC.md` [lu, 27 lignes] ; sha256 recompté
  `f086b6636d133f0ade2cfd229942996571b2810baba4bd9406f26da91eff300e`, égal à la valeur donnée.
- G0 : `docs/adr-0029/G0-lots-S2BIS.md` [lu, 23 lignes, sha256 `25a82120…a130`], **l.13**, ligne DOCS11-PUBLIC :
  sortie `docs/publication/11-mesures-pilotes-public.md` (brouillon), « non (rapport validé seul) », « rien n'est publié
  sans le feu vert écrit de l'investisseur après lecture ». Rattachement du G0 : ADR-0029 révision 3, ADR-0028.
- Décision : JOURNAL l.382 (2026-10-04 13:18:44 UTC, verbatim) [lu dans le diff du commit `8fada28`], dont q. 15
  « acteurs mesurés nommés avec préavis privé » ; JOURNAL l.384 (G0 de la vague) [lu dans le diff de `75bf258`].
- Écart E-1 : le brief cite la décision et la source, pas la ligne de G0 ; trouvée à l.13 (même objet). Le G0 nomme la
  sortie `docs/publication/…` ; le brief borne mes écritures au dossier du lot : le brouillon y est livré, le
  versement est un acte de l'orchestrateur.

## État du dépôt (lecture seule)

- Départ : `git rev-parse HEAD` → `75bf25862c12332bc8aba2dcd0b78d161ee1fa5b` ; branche `claude/compassionate-noether-szmdyj`
  (celle du brief) ; `git status --short` vide.
- Écart E-2 : pendant le lot, l'orchestrateur a commis `2c2fbe9` (2026-10-04T13:42:52Z, lot CALIB-ACTIFS-G0 : JOURNAL.md,
  `docs/adr-0029/calib/` ×2, `scripts/controle/sorties-fm11/calib-sources.json`). Aucune de mes entrées n'est touchée ;
  `docs/11` garde son sha256 `fcf93b87…53b7` (recompté à 14:09 UTC) ; la construction refuse toute autre empreinte.
- Fin : tête `2c2fbe9`, `git status --short` vide, `git status --short --ignored` identique avant et après la suite
  (190 entrées ignorées, 0 non suivie, sha256 du relevé `2281800a…f8a` avant comme après ; relevés supprimés ensuite).

## Pièces interdites et périmètre de lecture

- Liste fermée D.2 lue à l'annexe D l.32-48 [lu] ; aucune pièce de D.2 ouverte. Rien ouvert sous `docs/15-*`,
  `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` ; aucun `*.jsonl`.
  Les recherches récursives portaient `--exclude-dir` (rapports, adr-0025, monark-m009a, pocket-report, .git) et
  `--exclude` (`*.jsonl`, `15-*`, `16-*`) ; `find` élaguait ces dossiers.
- Écart E-3 : un `grep -rl` (noms de fichiers seuls) a parcouru les octets des trois rendus J14p, J14s et J28 de
  `docs/adr-0028/execution/rendu-2026-10-04/` pour la chaîne « AVIS-advisor-defi » ; un `grep -rIl` hors `docs/` a
  parcouru `JOURNAL.md` et `scratch/`. Aucune ligne affichée, aucune valeur vue ; c'est au-delà du « rapport validé
  seul » du G0. Le contrôle FM-1.1 de ma transcription est un acte de l'orchestrateur.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -u` pour la suite). `cargo xtask verify` jamais lancé ; le binaire
  `target/debug/xtask` (construit 09:45:20Z, après le dernier commit de `xtask/`, 08:24:53Z [inféré : à jour]) a tourné
  en mode `gates` sur une copie réduite de mon dossier, jamais sur l'arbre réel ; aucune gate n'écrit (recherche de
  `fs::write`, `File::create`, `create_dir`, `remove_*` dans `xtask/src/` : seuls `fuzz`, `reproductible`, `mutation`,
  `exemple`, que `gates` n'appelle pas).

## Sources lues

| source | niveau | portée |
|---|---|---|
| `docs/11-mesures-pilotes.md` (sha256 `fcf93b87…53b7`, blob `95044daf`, dernier commit `2db4f40`) | [lu] | l.1-1071, en entier |
| `docs/09-vocabulaire.md` (sha256 `001b9606…2f831`) | [lu] | en entier (63 l.) |
| `docs/adr-0028/CP2-S2.md` (sha256 `eb00a2e3…83a0`) | [lu] | en entier (206 l.) |
| `docs/adr-0029/G0-lots-S2BIS.md` | [lu] | en entier |
| JOURNAL l.380-384 | [lu] | par `git show 8fada28` et `git show 75bf258` (diffs) |
| `docs/adr-0029/ADR-0029-campagne-S2-bis.md` | [lu] | ligne Statut seule (diff de `8fada28`) |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` (sha256 `deb64179…5eaf`) | [lu] | l.32-48 ; titres et lignes qui citent « D.2 » (grep) |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` | [lu] partiel | titres ; l.51-56 (D4) ; l.252-262 (§4) ; lignes citant AVIS-advisor-defi |
| `xtask/src/sg4.rs`, `xtask/src/sg5.rs` | [lu] | en entier |
| `xtask/src/main.rs`, `lib.rs`, `sg2.rs`, `sg8.rs`, `sg9.rs` | [lu] partiel | dispatch, `verifier_tout`, garde cargo, en-têtes |
| `docs/G1-rapport-docs11.md` | [lu] | l.1-40 (format) |
| docs 00-14, 17 et README | comptes seuls | occurrences de « MONARK » et « Kraidle » (doc 08 : 2 et 2 ; doc 17 : 22 ; README : 10 Kraidle) |
| rendus, paquet, sceau, autres annexes, JOURNAL hors l.380-384, DECISIONS, PASSATION | [abs] | non lus (hors « rapport validé seul ») |
| contenu des rendus (chemin F: en J28 l.7, « ADR-0025 » en J28 l.435801) | [2nd] | connu par `docs/11` §2.7 et §7.4 seulement |
| état G3 (JOURNAL l.374) | [2nd] | par `CP2-S2.md` §5 |
| corpus qualité (doc 02, doc 03) | [abs] | hors dépôt |

## Méthode

1. Inventaire des motifs du point 1 dans la source (`grep -c`, puis contextes) ; contrôle de registre (doc 09) ;
   relevé du texte exact de chaque passage à retoucher.
2. Treize retouches, liste fermée dans `outils/construire_public.py`, appliquées dans l'ordre, chacune exactement une
   fois, sur la source à l'empreinte attendue ; la table de correspondance et le diff sont générés depuis la même liste.
   Principe déclaré : les chemins, noms de fichier, noms de dépôt, identifiants de session ou d'agent et le commit de
   D.2 n° 12 sont retirés ; les étiquettes (identifiants d'items, noms de lots, de gates, de relectures) restent, comme
   marques de provenance ; 16 passages examinés et gardés sont listés avec leur motif (G-01 à G-16).
3. Contrôle indépendant (`outils/controle_public.py`), sept contrôles bloquants : nombres (aucun inventé, aucun ajouté,
   même par répétition, aucun ajouté par une retouche) ; 36 motifs du point 1 à 0 ; registre (15 locutions S-G4, 46
   formules du doc 09, « N sources ») hors 3 exceptions motivées ; 30 passages protégés ; sections modifiées =
   sections déclarées, et rejeu de la table sur la source égal au brouillon à l'octet ; structure ; citations.
4. Tests d'abord, pour chaque module : module factice, échec montré, puis implémentation ; campagne de mutants.

## Commandes et sorties (chronologie, heures `date -u`)

| heure | commande | sortie |
|---|---|---|
| 13:23:42 | `sha256sum` du brief | `f086b663…300e` (égal) |
| 13:2x | `git rev-parse HEAD`, `status`, `log` | `75bf258`, arbre propre |
| 13:2x | `grep -c` des motifs sur `docs/11` | `F:` 1 ; `ADR-0025` 2 ; `Kraidle` 2 ; `90684fb2` 1 ; `aa04924` 1 ; `shogen-campagne` 1 ; `Drive` 1 ; `shogen-worker` 1 ; Pocket 0 ; `/tmp` 0 ; `docs/15`, `docs/16`, `monark-m009a` 0 |
| 13:3x | registre sur `docs/11` | une seule formule fautive : « rapport validé » (l.70-71) ; « validé » l.866 et « 10 sources » l.162-163 admissibles |
| 13:3x | barres obliques inverses de `docs/11` (`chr(92)`) | 2, toutes en l.211 |
| 13:45:46 | tests du contrôle sur module factice | 32 tests, 27 échecs, 0 erreur, sortie 1 |
| 13:49:04 | mêmes tests, module réel | 32 OK, sortie 0 |
| 13:49:42 | tests de la construction sur module factice | 44 tests, 12 échecs, sortie 1 |
| 13:52:03 | mêmes tests, module réel | 44 OK |
| 13:52:08 | construction | 13 retouches ; brouillon `903d6d0c…5433` (98 546 octets, 1 077 lignes) |
| 13:52:14 | contrôle | CONFORME, sortie 0 |
| 13:5x | relecture du contrôle | faille trouvée : un échange de nombres vers « 1 » ou « 2 », qui ont du jeu après les retraits, passerait le contrôle global |
| 13:54:46 | tests du rejeu sur fonctions factices | 51 tests, 7 échecs (dont l'échange de nombres), sortie 1 |
| 13:55:38 | rejeu implémenté | 51 OK ; brouillon inchangé, rejeu égal à l'octet |
| 13:56-13:58 | tests de câblage ajoutés (nombre déplacé, source modifiée d'un octet, registre seul, protégé seul, citation seule, titre supprimé, structure) | 58 OK |
| 13:59:50 | campagne de mutants | 52 tués sur 52 ; témoins T-0 sortie 0 |
| 14:00:19 | branche redondante retirée de `main` | 58 OK ; CONFORME ; 52 sur 52 |
| 14:01:31 | motif de recherche ajouté à G-02 | brouillon inchangé ; table `6af200f7…6d46d` ; CONFORME |
| 14:02:39 / 14:02:54 | `xtask gates` sur copie réduite, A (source) puis B (brouillon sous `docs/publication/`) | S-G4 VERT (0 violation) ; S-G5 VERT (4 fragments contrôlés, 257 écartés, corpus 155 sur 155) ; sorties A et B identiques à l'octet (sha256 `35980c4d…26f9`) ; verdict global ROUGE des autres gates, sans objet sur une copie réduite |
| 14:03:20-14:04:05 | suite `s2-harness` (`env -u SHOGEN_S2_CAMPAGNE_CONTROL`, `TMPDIR` dans le dossier du lot, `-B`) | `Ran 405 tests in 43.947s`, `OK (skipped=2)`, sortie 0 ; aucun fichier du dépôt plus récent que le repère |
| 14:04:39 | tests du relevé des acteurs, module factice | 3 échecs, sortie 1 |
| 14:05:04 | module réel ; relevé | 61 OK ; 22 noms relevés |
| 14:0x | nombres de `ACTEURS-NOMMES.md` contre le brouillon | 111 jetons absents du brouillon, tous des numéros de ligne, l'empreinte, l'heure ou des identifiants du lot ; aucune valeur de mesure |
| 14:09:37 | campagne finale (mutants MA et MC-27 à MC-31 ajoutés) | 60 tués sur 60, 0 vivant, 0 FATAL ; chacun des 60 noms de tests a échoué au moins une fois (étape rouge ou mutant) |
| 14:09:54 | contrôle final ; tests | CONFORME (sortie 0) ; 61 OK |

## Chiffres recomptés (sortie du contrôle final)

- Nombres : jetons composites 1 051 distincts dans la source, 1 047 dans le brouillon ; 0 inventé, 0 ajouté, 0 ajouté
  par une retouche ; 11 retraits, tous expliqués par la table : `ADR-0025` ×2 (E-05, E-07), `1` de « déc. 1 » (E-05),
  `D.2` et `2` de « n° 2 » (E-10), `aa04924` (E-10), `90684fb2` (E-11), et leurs suites de chiffres.
- Motifs : dans la source, 15 motifs présents sur 12 lignes (l.3, 14, 71, 178, 211, 624, 729, 914, 915, 933, 934,
  1064) ; pour les huit motifs comptés aussi par `grep -c` (F:, ADR-0025, Kraidle, 90684fb2, aa04924, shogen-campagne,
  Drive, shogen-worker), les comptes sont égaux ; dans le brouillon, 0.
- Sections : 58 dans chaque texte ; 49 identiques à l'octet ; 9 modifiées (titre, 1, 2.4, 2.7, 7.4, 8.3, 10.1, 10.2,
  12) = 9 déclarées ; rejeu des 13 retouches égal au brouillon à l'octet.
- Passages protégés : 30 sur 30 au même compte (verdict, énoncé de discordance, étiquette du §11.1, « hors décision »
  29 = 29, « NE REJETTE PAS » 9 = 9, empreintes du paquet, du manifeste, du jeton et du premier sceau, genTime, FreeTSA,
  commit `f35a70c…`, sha256 du script, Python 3.11.15, sha256 des journaux et tailles).
- Structure : 18 clôtures de code et 134 lignes de table de chaque côté ; citations 146 → 145 (la citation retirée par
  E-04), une modifiée (française, E-07).

## Écarts déclarés

- E-1 et E-2 : ci-dessus (rattachement, avance de la tête).
- E-3 : parcours mécanique des rendus et de JOURNAL.md par `grep -l`, ci-dessus.
- E-4 : deux commandes ont porté des séquences d'échappement de saut de ligne tapées (mise à jour des tests par Python, fichier factice par `printf`) ;
  octets contrôlés (`od -c`, 0 octet 0x5C dans tous les scripts, le brouillon et les listes) ; ensuite, toute barre
  est produite par `chr(92)`.
- E-5 : la consigne système « pas de fichier de rapport » et le brief (journal G1, table, liste) divergent ; j'ai écrit
  les seuls livrables du brief, dans le dossier du lot.
- E-6 : les scripts, le brouillon et les listes sont de moi ; leur relecture G2 par une instance distincte est due.

## Limites rendues comme items à former (règle PAROXYSME)

1. **Périmètre de publication** (proposé SHOGEN-PUBLIC-PERIMETRE-1) : le brouillon renvoie à des pièces du dépôt privé
   (rendus, paquet, sceau, ADR-0028 et annexes, docs 04/08/09/10, AVIS-SEUIL, journal G1 de POST-PREREG, scripts du
   rédacteur, sorties PP/, JOURNAL l.x, décision 270). Certaines portent des motifs du point 1 : annexe D l.34-45
   (chemins F:, `KraidleAI/monark-governance`, un identifiant de session) [lu] ; rendu J28 l.7 et l.435801 [2nd]. Les
   pièces scellées ou hachées ne se filtrent pas sans casser leur sha256 : les publier telles quelles, ou non.
2. **J14** (proposé SHOGEN-PUBLIC-J14-1) : valeurs gardées (§7.1, §7.2) ; ADR-0028 D4 en fait une décision de
   l'investisseur, que le feu vert doit couvrir explicitement.
3. **Libellé « Pyth est mort »** (§9.3 pt 8 ; proposé SHOGEN-PUBLIC-PYTH-LIBELLE-1) : gardé (limite déclarée) ; risque
   de lecture comme une panne de Pyth ; une précision serait un ajout daté au rapport validé.
4. **Mention de brouillon** (proposé SHOGEN-PUBLIC-MENTION-FEU-VERT-1) : au feu vert, la remplacer par la trace du feu
   vert ajoute des nombres (une date) ; déclarer une retouche E-14 et rejouer le contrôle.
5. **Liste de motifs fermée** (proposé SHOGEN-PUBLIC-MOTIFS-OUVERTS-1) : un nom privé non connu de moi échapperait au
   contrôle ; à compléter par l'investisseur et la relecture G2.

## Ajout daté du 2026-10-04 (14:46 à 14:5x UTC, `date -u`) : corrections de la relecture G2

Commande de l'orchestrateur : appliquer la liste fermée C-1 à C-3 et les observations adoptées O-1 et O-2 du rapport G2,
puis régénérer brouillon, table et diff, rejouer contrôle, tests et mutants, et mettre à jour les renvois de ligne de
`ACTEURS-NOMMES.md`. Ne pas anticiper les réponses de l'investisseur (J14, Pyth, MONARK, pièces jointes) : le texte du
brouillon reste tel quel sur ces points. Gate 0 : `claude-opus-5-5`. Rien de ce qui précède n'est réécrit ; cet ajout le
complète.

**Entrées.** Rapport G2 `g2/G2-DOCS11-PUBLIC.md` [lu, en entier, 388 lignes], sha256 recompté
`c58bba93b1cc7bc65814fe4a35c4702fd246205250c69405f3c591a037d97c2a`, égal à la valeur donnée ; verdict
ACCEPTE-AVEC-CORRECTIONS. Base : tête `6d463fa` (lots SG5-INTERDITS, `c4cf982` et `6d463fa`), arbre propre à 14:46:37 ;
`docs/11` garde son sha256 `fcf93b87…53b7` (recompté à 14:46:37 et 14:53:07). À 14:53, l'arbre porte `JOURNAL.md` modifié
par l'orchestrateur, pas par moi.

**Faits revérifiés pour les textes.**
- `docs/17-modele-de-menace.md` l.1-12 [lu] : l.5, « **Classification** : interne. Son inclusion dans un export public est
  une décision de l'investisseur (ADR-0028 §4.10 b) ». Comptes de « MONARK » (insensibles à la casse) : README 0, docs 00
  à 07 : 0 chacun, `docs/pitch-plates.html` 0, doc 08 : 2, doc 17 : 22. Mon motif G-08 de la première passe (« déjà
  présent dans des documents destinés au public (doc 08, doc 17) ») était faux : il reposait sur des comptes seuls, sans
  lecture des en-têtes.
- ADR-0028 l.1 (titre : « séquence PAROXYSME ») et §4 pt 7 (« Mesure de l'envergure : position institutionnelle
  (citations, recalculs) ou revenu ») [lu] ; annexe D l.173 et l.185, lignes coupées, qui citent PX-Shogen-13 (D.5) [lu].
- JOURNAL l.322 [lu partiel] : la clause « priorité : « Position d'abord (Recommandé) » (ADR-0028 §4.7 : benchmark gratuit
  et recalculable ; rapports de concentration vendus après un recalcul externe) ». Le motif de E-04 était exact.

**Corrections appliquées** (`outils/construire_public.py`, liste fermée) :
- C-1 : motif de G-08 réécrit : projet absent des documents d'allure publique, présent au doc 08 et au doc 17 classé
  interne, gardé en attente de la décision de l'investisseur (ADR-0028 §4 pt 5).
- C-2 : statut de E-01 réécrit sur le texte du réviseur, avec « paquet scellé » ajouté à la liste des pièces (consigne de
  l'orchestrateur) ; les autres pièces citées restent, au dépôt privé, et leur diffusion n'est pas décidée ; aucun chiffre
  ajouté (test : multiset des chiffres de E-01 égal avant et après). L'en-tête compte deux lignes de plus.
- C-3 : G-17 (« M009 ») et G-18 (« PX-Shogen-13 ») ajoutés ; la table des passages gardés porte désormais, pour chacun,
  les lignes de la source **et** celles du brouillon, calculées par le script (un passage gardé absent de l'un ou de
  l'autre arrête la construction).
- O-1 : E-04 dit l'omission : « une réponse de stratégie commerciale n'est pas reprise ».
- O-2 : E-06 écrit « chemin à lettre de lecteur (J28 l.7) ».

**Commandes et sorties.**

| heure | commande | sortie |
|---|---|---|
| 14:46:37 | `date -u` ; `sha256sum` du rapport G2 ; `git rev-parse`, `status` | `c58bba93…7c2a` égal ; `6d463fa` ; arbre propre |
| 14:4x | lectures et comptes ci-dessus | voir « Faits revérifiés » |
| 14:49:50 | sept tests nouveaux (C-1, C-2, C-3, O-1, O-2, deux pour la table des passages gardés), `table_gardes` factice | 68 tests, 7 échecs, 0 erreur, sortie 1 |
| 14:50:50 | corrections appliquées | 68 OK, sortie 0 ; 0 octet 0x5C dans scripts et tests |
| 14:50:56 | construction | 13 retouches, 18 passages gardés ; brouillon `89d659c8…97bd` (98 860 octets, 1 079 lignes) |
| 14:5x | contrôle | CONFORME, sept sur sept, sortie 0 ; aucune exception nouvelle |
| 14:51:33 | campagne (MD-03 et MD-08 aux nouvelles chaînes ; MB-08 à MB-15 ajoutés) | 68 mutants, 68 tués, 0 vivant, 0 FATAL ; témoins T-0 sortie 0 |
| 14:52 | relevé des acteurs régénéré ; comparaison à l'ancien | mentions et sections inchangées ; chaque numéro de ligne décalé de deux (30 lignes, 0 écart) |
| 14:52:14 | `ACTEURS-NOMMES.md` : empreinte, table du §1, renvois « b. l. » décalés de deux, mention datée | 18 renvois décalés ; un renvoi sans préfixe (« l.380-383 ») corrigé à part en « l.382-385 » ; 17 renvois vérifiés contre le texte du brouillon |

**Contrôle final (sortie `controle_public.sortie.txt`).** Nombres : 0 inventé, 0 ajouté, 0 ajouté par une retouche ;
mêmes 11 retraits d'identifiants. Motifs : 0 sur 36. Registre : 0 formule interdite, les 3 mêmes exceptions motivées.
Passages protégés : 30 sur 30. Sections : 49 sur 58 identiques, 9 modifiées = 9 déclarées ; rejeu de la table égal au
brouillon à l'octet. Structure : 18 clôtures de code et 134 lignes de table de chaque côté. Citations : 146 → 147
(« Position d'abord (Recommandé) » retirée par E-04 ; « Reproduire » et « Ce qui n'est pas public » ajoutées par E-01,
françaises).

**Empreintes après corrections.**

| pièce | sha256 |
|---|---|
| `11-mesures-pilotes-public.md` | `89d659c8c7c65d7526ee40534e7894dc809b68361c7e76172e245e9590d397bd` |
| `TABLE-CORRESPONDANCE.md` | `35e3cb69d2d8d713e46b12b4a08373ab1f57a295040e835cb2e3eb7c8d328c48` |
| `diff-source-brouillon.txt` | `df8478108381abe052a02745c01550d55a4cf6d684b93bc9b3b37457230a57e1` |
| `controle_public.sortie.txt` | `4b20f816f1695dc56380f40a7284a8730654ac08530c17f69bf193ce7fd5b4b5` |
| `ACTEURS-NOMMES.md` | `6c36f0b61b89cee23bce4c37006caa11fcd76854590330aca011ec118dec1574` |
| `acteurs_nommes.sortie.txt` | `187872089ea11b062f730fd1d4ce7fe11d0396c5a123b4680469ae6f0818a1dc` |
| `outils/construire_public.py` | `a9a8227693f01081fc9ac37f0223108debfac8d744cee9ac182bd31feb8f4003` |
| `outils/controle_public.py` (inchangé) | `311a734ff3dfc20b984a3688d2e70d22b88da08815e1845551dbd572ee260236` |
| `tests/test_construire_public.py` | `10a1d53889b9855c650f008901c3511e019c31c154ae4f3804bed598e1fa18d9` |
| `mutants/campagne_mutants.py` | `c2838ffe0517b0f3fae1a21b9f2bb631f8946d0c24c2821e71e7ca2162366f91` |
| `mutants/campagne.sortie.txt` | `a15b73e5def16f12ca3c548132adc743b6a8cf933abad2e3774d3259d9714bed` |

**Écarts de cette passe.**
- E-7 : ma première extraction de JOURNAL l.322 (fragment de 260 caractères) a affiché, avant la clause visée, une
  incise de la réponse « publication » qui porte le mot « Pocket ». C'est une mention, pas une pièce ; le brouillon n'en
  porte aucune (motif « pocket » : 0). Le contrôle FM-1.1 de ma transcription vous revient.
- E-8 : un `grep -o` en lecture seule, sur `ACTEURS-NOMMES.md`, portait des barres obliques inverses tapées ; son
  résultat a été refait et vérifié en Python, sans barre (expressions à classes de caractères).
- E-9 : S-G4 et S-G5 n'ont pas été rejouées après les corrections. Le binaire de 09:45 précède la modification de
  `xtask/src/sg5.rs` par le lot SG5-INTERDITS ; reconstruire `xtask` écrirait dans `target/` du dépôt. Le contrôle des
  citations (parité S-G5) et du registre (dont les 15 locutions de S-G4) est vert ; la gate au versement fera foi.
- La suite `s2-harness` n'a pas été rejouée dans cette passe : aucun fichier du dépôt n'a été touché.

## Ajout daté du 2026-10-04 (14:56 à 15:04 UTC, `date -u`) : décisions de l'investisseur intégrées

Commande de l'orchestrateur (trois messages concordants) : intégrer au brouillon, dans la même passe que C-1 à C-3, les
décisions de l'investisseur du JOURNAL, entrée de 14:52:24 UTC, verbatim, au dépôt depuis le commit `8a1e642`. Gate 0 :
`claude-opus-5-5`. Rien de ce qui précède n'est réécrit.

**Rattachement.** JOURNAL l.390 [lu, en entier, dans l'arbre puis contrôlé au commit : `git show 8a1e642:JOURNAL.md`, même
ligne]. Réponses verbatim : J14, « Oui, tout montrer (Recommandé) » ; Pyth, « Phrase factuelle (Recommandé) » ; MONARK,
« Nommer MONARK (Recommandé) » ; pièces, « Rapport seul (Recommandé) » ; défauts annoncés sans objection : la consigne
« pas sur mon PC » remplacée par une phrase neutre (la limite reste écrite), aucun nom privé signalé. Conséquences
écrites : J14 publié avec son étiquette (SHOGEN-PUBLIC-J14-1 tranché) ; libellé factuel pour Pyth ; MONARK nommé ;
rapport publié seul, pièces (sceau, rendus, enregistrements) remises sur demande sous accord ; publication toujours
soumise au feu vert écrit de l'investisseur après lecture du brouillon corrigé. Base : `8a1e642`, puis `2aa4d6b` (G0 du lot
PLAN-S2BIS : JOURNAL.md et `docs/adr-0029/G0-lot-PLAN-S2BIS.md`) ; aucune entrée du lot touchée, `docs/11` à `fcf93b87…53b7`.

**Recensement dans le brouillon `89d659c8…`** (script, mots « mort », « remis », « joint », « publi », « versé », « VPS »,
« mon PC ») : un seul écho de « Pyth est mort » (§9.3 pt 8 ; les « flux quasi morts » des §11 et §11.1 sont un item
générique) ; « remis avec ce rapport » aux §6 et §8.9 (scripts du rédacteur) ; §12 « Ce qui n'est pas public » ; en-tête
(« leur diffusion n'est pas décidée ») ; consigne verbatim au §2.7. Les quatre scripts du §8.9 sont au dépôt, aux empreintes
citées (`8f91474c…`, `11779f79…`, `4e61cea8…`, `4d210cb6…`, recomptées).

**Retouches et passages gardés.**
- E-01 (en-tête) : la publication porte sur ce rapport seul ; les autres pièces citées sont au dépôt privé et ne sont pas
  publiées ; le sceau, les rendus et les enregistrements sont remis sur demande, sous accord ; le constat sur Pyth et une
  consigne de l'investisseur sont reformulés sur sa décision ; mêmes chiffres qu'avant (test).
- E-14 (§9.3 pt 8, Pyth) : « Aucune donnée de prix n'a été reçue de Pyth sur toute la campagne : l'accès au service
  interrogé a été refusé (HTTP 401) dès le premier jour (ADR l.25), et rien ne montre une panne de Pyth ; … » ; mêmes
  nombres que la phrase source (8, 401, 25) : aucun nombre repris d'ailleurs, donc aucune adaptation du contrôle des
  nombres n'est nécessaire.
- E-15 (§2.7) : consigne verbatim remplacée par « … sur le poste personnel de l'investisseur, qui demande pour S2-bis une
  collecte sur un serveur privé virtuel (JOURNAL l.324) » ; la limite reste (§2.7 et §9.3 pt 5).
- E-16 (§12) : « Les rendus, le sceau et les enregistrements sont au même dépôt privé et ne sont pas publiés : pièces
  remises sur demande, sous accord ; … ».
- E-17 (§6) et E-18 (§8.9) : « remis avec ce rapport » devient « versé(s) au dépôt du projet avec ce rapport ». Les scripts
  ne sont pas dans la liste de la réponse (sceau, rendus, enregistrements) : seule leur place est dite, pas leur remise.
- G-02 : la limite est gardée, la citation remplacée (E-15). G-08 : MONARK nommé par décision (« Nommer MONARK »). G-12 :
  J14 publié avec son étiquette (« Oui, tout montrer »). G-17 : même décision que G-08.
- Contrôle resserré : trois motifs « décision de l'investisseur » (« Pyth est mort », la consigne verbatim, « remis avec
  ce »), à 0 exigé dans le brouillon.

**Commandes et sorties.**

| heure | commande | sortie |
|---|---|---|
| 14:56:45 | `date -u` ; `git status` ; lecture de JOURNAL l.390 | tête `8a1e642` ; `JOURNAL.md` modifié dans l'arbre (orchestrateur) |
| 14:57:14 | `git show 8a1e642:JOURNAL.md` ; entrées du lot | l'entrée est au commit, l.390 ; 0 entrée du lot changée |
| 14:5x | recensement ; empreintes des scripts au dépôt | voir ci-dessus |
| 14:59:09 | tests nouveaux (une par décision, compte des retouches 13 → 18, spécification de E-01, motifs du contrôle) | 75 tests, 8 échecs, 0 erreur, sortie 1 |
| 15:00:40 | décisions appliquées | 74 OK, 1 échec : le test de E-14 cherchait « décision » en minuscule dans un motif qui commence par une capitale ; test rendu insensible à la casse, exigence inchangée |
| 15:00:58 | tests ; construction ; contrôle | 75 OK ; 18 retouches, 18 passages gardés ; brouillon `4de98654…7688` (99 352 octets, 1 081 lignes) ; CONFORME, sept sur sept, sortie 0 |
| 15:02:11 | campagne (MB-11 et MD-09 mis à jour ; MB-16 à MB-23, MC-35 à MC-37, MD-19 à MD-21 ajoutés) | 82 mutants, 82 tués, 0 vivant, 0 FATAL ; témoins T-0 sortie 0 ; chacun des 74 noms de tests a échoué au moins une fois |
| 15:03 | relevé des acteurs ; `ACTEURS-NOMMES.md` | Pyth 19 → 21 mentions (§9.3 pt 8, en-tête), autres acteurs décalés de deux lignes ; 18 renvois décalés, 17 vérifiés contre le brouillon |

**Contrôle final (`controle_public.sortie.txt`).** Nombres : 0 inventé, 0 ajouté, 0 ajouté par une retouche ; mêmes 11
retraits d'identifiants. Motifs : 0 sur 39 (36 du point 1, 3 des décisions). Registre : 0 formule interdite, 3 exceptions
motivées. Passages protégés : 30 sur 30. Sections : 46 sur 58 identiques, 12 modifiées = 12 déclarées (titre, 1, 2.4, 2.7,
6, 7.4, 8.3, 8.9, 9.3, 10.1, 10.2, 12) ; rejeu des 18 retouches égal au brouillon à l'octet. Structure : 18 clôtures et 134
lignes de table de chaque côté. Citations : 146 → 146 (deux retirées, la priorité et la consigne ; deux ajoutées, françaises).

**Empreintes.**

| pièce | sha256 |
|---|---|
| `11-mesures-pilotes-public.md` | `4de986544cee9622a0848f585103cea594352df65d02e8f51e6ef4c593fc7688` |
| `TABLE-CORRESPONDANCE.md` | `2b3a34ebb19467905c0e9f6de6a17fb7bf8715e9b99c08f9fcc1ca29ad97b689` |
| `diff-source-brouillon.txt` | `ef85aa08b0f5c2725b947d50e9533fca6046d904aa733ea3f1b9b63084519ce2` |
| `controle_public.sortie.txt` | `935cf1c1deaf797d4003e0f66a707e12077f9909f00bc11178b2f565bdf1ce3b` |
| `ACTEURS-NOMMES.md` | `b8ac4acd0322b0909ed5d7f198558ba73ec6858791dade1d3beb5a01e5d79356` |
| `acteurs_nommes.sortie.txt` | `5fe978378aeb6637b87b9c0605e8fe52fd2c70bdb19aa67363ee6ef1e3ce3678` |
| `outils/construire_public.py` | `1a974a5d79dec6d308c1425fff3268d2b93c5e726fb7c3782e83bf6826c24ada` |
| `outils/controle_public.py` | `467e13ee5f66531f95d162293c7a1dddb678d3423525ededbb83336d67d41b8e` |
| `tests/test_construire_public.py` | `ce616f1264a407118fbe6f0d76fc4eedb2d2accc2a0ec0ed6e586730c7820a80` |
| `tests/test_controle_public.py` | `5b75a76db6d5231620cc7fb889c20f23cb999edcd16ab4da6f41cebfefc3189f` |
| `mutants/campagne_mutants.py` | `78f045f31bd0c770f0657ddd02e54fac31226abec58b0f3f5fdcefc7c37c7a19` |
| `mutants/campagne.sortie.txt` | `78bf9affd38aafd211e4b554cc5773b998f8323b613908088bef1ca73a971178` |

**Items.** SHOGEN-PUBLIC-J14-1 : tranché (publié avec son étiquette). SHOGEN-PUBLIC-PYTH-LIBELLE-1 : tranché, appliqué par
E-14. SHOGEN-PUBLIC-MOTIFS-OUVERTS-1 : fermé par la réponse de l'investisseur (aucun nom privé). MONARK : tranché (nommé).
SHOGEN-PUBLIC-PERIMETRE-1 : tranché (rapport seul ; pièces remises sur demande, sous accord). Reste
SHOGEN-PUBLIC-MENTION-FEU-VERT-1 : la mention de brouillon de l'en-tête attend le feu vert écrit.

**Écarts de cette passe.**
- E-10 : un pilote de mutants a reçu une apostrophe échappée (octet 0x5C) ; ligne réécrite avec des triples guillemets,
  syntaxe contrôlée, 0 octet 0x5C ensuite.
- E-11 : les scripts du rédacteur (§6, §8.9) ne figurent pas dans la liste des pièces remises sur demande (sceau, rendus,
  enregistrements) ; le brouillon dit seulement qu'ils sont versés au dépôt du projet. Question ouverte : sont-ils remis
  sur demande comme les autres pièces ? De même, « sceau » couvre-t-il le paquet scellé, nécessaire pour contrôler le
  sceau ? Le brouillon ne tranche aucun des deux points.
- S-G4 et S-G5 n'ont pas été rejouées (même motif que E-9) ; la suite `s2-harness` non plus (dépôt non touché).
