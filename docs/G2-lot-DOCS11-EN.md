# Relecture G2 — lot DOCS11-EN (version anglaise du brouillon public du rapport de S2)

Réviseur G2 neuf (fiche `shogen-worker`), lecteur du français et de l'anglais ; je n'ai rien écrit de ce lot. Relecture
faite le 2026-10-04 de 16:56:16 à 17:2x UTC (`date -u`) ; rapport écrit à partir de 17:25:12 UTC. Rien n'est publié.
Aucune opération git en écriture. Écritures limitées au dossier
`/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/en/g2/` (noté `g2/` ; le dossier
du lot est noté `en/`).

## 0. Gate 0, rattachement, base

- Modèle : identifiant exact déclaré par l'environnement, `claude-opus-5-5` (préfixe attendu `claude-opus-5-5` :
  conforme). Effort `max` demandé par l'orchestrateur ; il n'est pas observable de l'intérieur de la session.
- Brief `g2/BRIEF-G2-DOCS11-EN.md` : sha256 recompté
  `03ff54983812024c836e1828d7b0a8a7e02c05f33c530cfc1aed133eb1b792c2`, égal à la valeur donnée (début et fin).
- Rattachement (G0) :
  - JOURNAL l.396, entrée du 2026-10-04 15:16:03 UTC : lot DOCS11-EN lancé, « suivront […] les relectures » ;
  - ADR-0028, annexe B.57 (`ANNEXE-B-items.md` l.937 à 955) : brouillon source versé, non publié ;
  - `docs/adr-0029/G0-lots-S2BIS.md` n'a toujours pas de ligne DOCS11-EN (E-7 du traducteur, constaté de nouveau à
    `665898a`) : item I-G2-1.
- Base :
  - début : `10e860a35a1b93473254887f81aa025bdefa8802` ; fin : `665898a2238df8085ac7cb60f75bced0fff8bc3b` (commits de
    l'orchestrateur : PLAN-S2BIS, G0 de collecte, JOURNAL) ;
  - `git diff --quiet 10e860a HEAD -- docs/publication docs/09-vocabulaire.md xtask
    docs/adr-0028/ANNEXE-D-preenregistrement.md docs/adr-0029/G0-lots-S2BIS.md s2-harness biblio` : sortie 0, les
    entrées du lot sont inchangées ;
  - `git status --short` : 0 ligne à la fin.
- Pièces relues :
  - traduction `en/11-pilot-measurements-public-en.md`, sha256
    `ad5289a9bf0e917adae37ba1589dbb77b265a21fe283f49d1435fec8d692e36d` (égal au brief), 760 lignes ;
  - source `docs/publication/11-mesures-pilotes-public.md`, sha256
    `4de986544cee9622a0848f585103cea594352df65d02e8f51e6ef4c593fc7688` (égal au brief), 1081 lignes.
- Interdits respectés : aucune pièce de D.2 ouverte (noms seulement, ANNEXE-D l.28 à 50) ; aucun `*.jsonl` ouvert ;
  aucun dossier interdit lu ; aucune recherche récursive sur `docs/` ; `SHOGEN_S2_CAMPAGNE_CONTROL` non posée
  (`printenv`, sortie 1) et retirée par `env -u` à chaque lancement.

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1 à C-10 (section 2).

- La traduction est fidèle. Les 58 sections sont lues en entier dans les deux langues : aucun contresens sur le
  verdict, les nombres, les limites ou les déviations ; aucune omission ; aucun ajout dans le corps.
- Les contrôles rejoués rendent les mêmes sorties, à l'octet, que celles du traducteur (section 3).
- Les corrections portent sur :
  - l'adjudication de l'en-tête, non appliquée dans la version livrée (C-1) ;
  - une phrase inexacte du paragraphe de conventions (C-2) ;
  - un renforcement léger (C-3) et un risque de contresens pour un lecteur anglais (C-4) ;
  - deux gloses (C-5, C-6) et trois faux amis (C-7 à C-9) ;
  - une affirmation inexacte du journal G1 du traducteur (C-10).
- Preuve d'applicabilité : C-1 à C-9 appliquées sur une copie (`g2/essai/`) donnent un contrôle CONFORME (onze sur
  onze), 97 tests verts, 97 mutants tués sur 97, S-G4, S-G5 et S-G6 vertes, et des nombres identiques à la source.

## 2. Liste fermée des corrections (textes exacts)

Chaque texte se remplace tel quel, une seule occurrence. Les numéros de ligne sont ceux de la traduction `ad5289a9…`.
La traduction est assemblée depuis `en/parties/` : chaque correction du corps se porte dans la partie indiquée, puis la
traduction se réassemble (section 2.2).

### C-1 — En-tête : adjudication de l'orchestrateur (point 6 du brief ; E-2 du traducteur)

Traduction l.3 et `parties/p1.md` :

```text
avant : English translation of the report as accepted at validation;
après : English translation of the accepted report;
```

Module `outils/glossaire_en.py` l.37 (le contrôle 10 compare l'en-tête à `ENTETE_PHRASE`) :

```text
avant : ENTETE_PHRASE = ("English translation of the report as accepted at validation; numbers, verdicts and sealed labels "
après : ENTETE_PHRASE = ("English translation of the accepted report; numbers, verdicts and sealed labels "
```

Commentaire du module, l.34 et l.36 (texte proposé ; il n'agit pas sur la traduction) :

```text
avant : # Phrase du brief, point 6, à un mot près : « validated » est remplacé par « as accepted at validation », parce que
après : # Phrase du brief, point 6, à un mot près : « the validated report » devient « the accepted report », parce que
avant : # qualificatif d'assurance). Écart déclaré au rapport du lot, à adjuger par l'orchestrateur.
après : # qualificatif d'assurance). Écart E-2, adjugé par l'orchestrateur le 2026-10-04 (brief de la relecture G2).
```

Motif : la version livrée n'applique pas l'adjudication. Le mot `accepted` n'est pas une locution de S-G4 ; la gate est
verte après correction.

### C-2 — Paragraphe `Translation conventions` (gardé par adjudication) : exactitude

Traduction l.5 et `parties/p1.md` :

```text
avant : At its first occurrence, each such passage carries an English gloss, in italics between square brackets, unless it is already legible in English (symbols, English terms); the glossary at the end of this document lists the glosses.
après : At its first occurrence in the running text, each such passage carries an English gloss, in italics between square brackets, unless it is already legible in English (symbols, English terms); code blocks are not glossed; the glossary at the end of this document lists the glosses.
```

Motif : la phrase qui précède range les blocs de code parmi les passages gardés en français ; la phrase actuelle leur
promet donc une glose. Or les 9 blocs de code n'en portent aucune (I-3 du traducteur ; vérifié). Le paragraphe ajouté
décrit plus que ce qui est fait.

### C-3 — Fidélité : « des mentions de gouvernance interne sans objet pour un lecteur extérieur » (source l.6)

Traduction l.7 et `parties/p1.md` :

```text
avant : and the mentions of internal governance with no purpose for an outside reader are removed
après : and mentions of internal governance that are of no relevance to an outside reader are removed
```

Motif : la source écrit « les » pour les quatre premières catégories retirées et « des » pour celle-ci. L'article
défini anglais fait dire que toutes ces mentions sont retirées : c'est plus fort que la source. « sans objet pour » se
rend par `of no relevance to`.

### C-4 — « sous veto » (source l.289-290)

Traduction l.182 et `parties/p2.md` :

```text
avant : ratified by the orchestrator on 2026-09-30, under veto, before the sealing
après : ratified by the orchestrator on 2026-09-30, subject to veto, before the sealing
```

Motif : le paquet scellé donne le sens (l.108 : veto A-8 ; l.112 : « ratifiée par l'orchestrateur le 2026-09-30, sous
veto ») : ratifiée sous réserve du veto. En anglais, `under veto` se lit « frappée de veto » : risque de contresens.

### C-5 — Glose de « gardes levées »

Traduction l.457 et `parties/p4.md` :

```text
avant : « gardes levées » [*guards lifted*]
après : « gardes levées » [*guards cleared*]
```

Module, ligne G-47 (la ligne l.693 du glossaire final en sort au réassemblage) :

```text
avant : ("G-47", "« gardes levées »", "guards lifted", "sortie imprimée"),
après : ("G-47", "« gardes levées »", "guards cleared", "sortie imprimée"),
```

Campagne `mutants/campagne_mutants.py`, ancrage de MT-23 (sans ce report, MT-23 devient FATAL) :

```text
avant : ("MT-23", "« gardes levées » [*guards lifted*]", "“guards lifted”",
après : ("MT-23", "« gardes levées » [*guards cleared*]", "“guards cleared”",
```

Motif : `rendu_unique.py` au commit d'analyse `f35a70c` (sha256 `06d189cf…9050`, égal à `sha256_script`) imprime
« gardes levées » à la l.502 quand aucune garde ne refuse ; l'outil est en refus par défaut. `guards lifted` peut se
lire « gardes désactivées » ; `guards cleared` dit « gardes franchies ». Le sens est le même.

### C-6 — Glose de « conforme »

Traduction l.468 et `parties/p4.md` :

```text
avant : « conforme » [*compliant*]
après : « conforme » [*conformant*]
```

Module, ligne G-48 (la ligne l.694 du glossaire final en sort au réassemblage) :

```text
avant : ("G-48", "« conforme »", "compliant", "sortie imprimée"),
après : ("G-48", "« conforme »", "conformant", "sortie imprimée"),
```

Motif : `oracle_record.py --verifier` (l.261 à `f35a70c`) imprime « conforme » quand l'enregistrement passe ses
contrôles. Pour une banque ou un régulateur, `compliant` évoque une conformité réglementaire : la glose en dit plus
que la sortie. `conformant` garde le sens technique.

### C-7 — Faux ami : « la précision (i) du paquet » (source l.966)

Traduction l.579 et `parties/p4.md` :

```text
avant : whereas precision (i) of the package provides for one
après : whereas clarification (i) of the package provides for one
```

Motif : le paquet, l.8, écrit « Précisions, sans effet sur ces valeurs : (i) un prix qui n'est pas un nombre fini
[…] ». En anglais, `precision` veut dire exactitude.

### C-8 — « leur publication conditionne le test de composition » (source l.1075)

Traduction l.635 et `parties/p5.md` :

```text
avant : and their publication conditions the composition test
après : and their publication is a precondition for the composition test
```

Motif : en anglais, le verbe `to condition` se lit d'abord « préparer, façonner » ; la source dit « est une condition
préalable du test ».

### C-9 — « ferme l'appel accidentel de --produire » (source l.851)

Traduction l.529 et `parties/p4.md` :

```text
avant : closes the accidental call of `--produire`, not the deliberate call
après : blocks the accidental call of `--produire`, not the deliberate call
```

Motif : `closes a call` n'a pas de sens clair en anglais ; « fermer » vaut ici « bloquer ».

### C-10 — Journal G1 du traducteur (`en/G1-lot-DOCS11-EN.md`), l.347-348 : affirmation inexacte

```text
avant : Octets 0x5c : 0 dans chacun des fichiers écrits du lot (scripts, tests, parties, traduction, table, relevés, ce
journal), compte fait sur les octets écrits. Aucun marqueur de tâche ouverte (R-13).
après : Octets 0x5c : 0 dans les livrables du lot (traduction, table, `outils/`, `outils-factice/`, `tests/*.py`,
`mutants/`, `parties/`, ce journal), compte fait sur les octets écrits. En portent sept scripts d'exploration
(`explo/ctx.py`, `distinctes.py`, `mots.py`, `premiers.py`, `quotes.py`, `survey.py`, `verif_glossaire.py` : de 3 à
16 octets chacun, échappements Python écrits sans gabarit) et deux sorties (`tests/etape-rouge.sortie.txt`,
`explo/factice-final.txt` : 2 chacune) ; les comptes du journal qui venaient de ces scripts sont refaits par le
contrôle (contrôle 3 : 120 citations, 96 distinctes). Aucun marqueur de tâche ouverte (R-13).
```

Motif : compte fait sur les octets (`od`), 9 fichiers du lot portent l'octet 0x5c (échappements de fin de ligne et
d'espaces dans des chaînes et des expressions régulières Python, écrits directement). Les livrables en ont 0. Aucun résultat du lot n'en dépend : les comptes concernés sont refaits
par le contrôle, qui n'en porte pas.

### 2.2 Application et valeurs attendues

1. Appliquer C-1 à C-9 au lot : parties, module, campagne. Le script `g2/appliquer_corrections.py` fait les 15
   remplacements exacts ; il refuse et n'écrit rien si un texte d'origine n'apparaît pas exactement une fois. Appliquer
   C-10 à la main dans le G1, et y consigner l'adjudication de E-2 et de E-3.
2. Réassembler : `python3 -B outils/assembler_en.py SOURCE parties 11-pilot-measurements-public-en.md`.
3. Rejouer le contrôle avec `--table`, les tests, la campagne de mutants et les gates.
4. Valeurs obtenues sur ma copie `g2/essai/` :
   - traduction `f8865abe003189a382c0fe22366a72fbc6614442b4273f99630326cbc31a1b3f` ; seules les l.3, 5, 7, 182, 457,
     468, 529, 579, 635, 693 et 694 changent ;
   - table de correspondance `9aedd60d0cbe2b024f2c6ea59f2d4c0c58258229ba2a67af5607f4d482107d0c` (seule l'empreinte de la
     traduction y change) ;
   - module `65591349695c757d54ea3367ccb521c10fde49b7ef00ca27565e7d7424c9985a` (avec les commentaires proposés en C-1 ;
     un autre texte de commentaire ne change que cette empreinte) ;
   - campagne `32615ccbfc88f0d5663f0261541a9491d40b120d85091d87d8defd3724225f52` ;
   - parties : p1 `396f0648a7918adbbec95b1800ad664df606cb43f8828a3c5450f1cffec25b99`, p2
     `03ed057e4f9ce31b2fd046bfb87be92e9544427233e60c1807aa4c1662655946`, p3 inchangée
     (`3a434421f3a44831c05b6818a4553c66e7d5a53d0939f9bd144002a6d8d27f85`), p4
     `a7d4b623515ff988825687aa72402083e9fc2b67f6f4b6d9a483c0d147ca1b00`, p5
     `39a8e3abcde09b975103f0bdd9c629d36c84440202da104bf03b161f0ea6b35d` ;
   - contrôle : CONFORME, onze contrôles sur onze, sortie 0 ;
   - tests : `Ran 97 tests`, `OK` ; mutants : 97 tués, 0 vivant, 0 FATAL, témoins OK ;
   - S-G4, S-G5 et S-G6 vertes (sortie identique à celle d'avant correction) ;
   - nombres : 3 384 occurrences de chaque côté, 0 inventé, 0 perdu ; relevé des termes : 22 manques, sortie
     identique.
5. Diff unifié de référence : `g2/corrections-G2.diff` (195 lignes, sha256
   `09a641ba1f351c75582dcb163406c845d9cb8883f9fbfb614ed8789d1b1bd1a9`).

## 3. Contrôles rejoués (point 1 du brief)

Chaque rejeu porte sur une copie dans `g2/rejeu/`. Ses fichiers ont les empreintes déclarées au G1 du traducteur,
vérifiées une à une. `TMPDIR` pointe dans `g2/`.

| heure UTC | contrôle | résultat | comparaison |
|---|---|---|---|
| 17:06:41 | `outils/controle_en.py SOURCE TRADUCTION --table` | CONFORME, onze sur onze, sortie 0 | sortie identique à `en/controle_en.sortie.txt` hors chemins ; table régénérée identique à l'octet (`a647b9b3…f2d`) |
| 17:06:48 | `tests/lancer_tests.py outils` | `Ran 97 tests`, `OK`, sortie 0 | comme au G1 |
| 17:06:48 | `tests/lancer_tests.py outils-factice` | `FAILED (failures=79)`, sortie 1 | comme au G1 (79 sur 97) |
| 17:06:55 à 17:07:31 | `mutants/campagne_mutants.py` | 97 mutants : 97 tués, 0 vivant, 0 FATAL ; témoins OK ; 97 tests vus en échec | sortie identique à l'octet (`f966a888…f203`) |
| entre 17:07:31 et 17:12:44 | réassemblage depuis `parties/` | `ad5289a9…e36d` | identique à l'octet au livrable |
| 17:12:44 | `target/debug/xtask gates` sur une copie réduite construite par moi | S-G4 VERT (0 violation, 4 fichiers) ; S-G5 VERT (4 fragments contrôlés, 474 sous le seuil, corpus 155 sur 155) ; S-G6 VERT ; autres gates rouges par couverture (copie réduite) | sortie identique à celle du traducteur, hors racine |
| 17:12:59 à 17:13:46 | suite `s2-harness`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL` | `Ran 405 tests in 45.784s`, `OK (skipped=2)`, sortie 0 | comme au G1 |
| entre 17:17:27 et 17:21:25 | `explo/termes_survey.py` (copie) | 22 manques | sortie identique (`d02685d3…e236`) |

## 4. Fidélité du sens (point 2)

- Lecture parallèle intégrale, phrase par phrase : en-tête, §1, conventions et lexique, §2.1 à §2.7, §3 à §3.5, §4.1 à
  §4.4, §5 à §5.4, §6, §7 à §7.6, §8.1 à §8.9, §9.1 à §9.3, §10.1 à §10.5, §11, §11.1, §12 et ses deux ajouts datés,
  glossaire final. Cela fait 58 sections sur 58 ; le brief en exige au moins 15.
- §1 et §3 (verdict) : NE REJETTE PAS dans les deux strates, « R1 discrimine » = FAUX, énoncé scellé de la discordance,
  EMD_s, k_eff = 4 pour k nominal = 10, drapeaux. Tout est rendu sans écart ; les libellés scellés restent en français,
  glosés.
- §8 (sceau, exécution) : empreintes, genTime, délai, voie (a), gardes, journaux, enregistrement et ce que le sceau
  n'atteste pas sont fidèles. Voir C-4 (§3.2) et les gloses C-5, C-6.
- §9.3 (limites) : les 14 constats sont rendus sans adoucissement ni renforcement. Les 24 occurrences de `only`,
  relues une à une, rendent toutes un « seul » ou un « ne … que » de la source.
- §11.1 : « ce que ces analyses permettent de dire » et « ce qu'elles ne permettent pas de dire » sont fidèles.
- §12 : fidèle, au faux ami C-8 près.
- Bilan :
  - contresens : aucun sur le fond ; un risque de contresens de lecture (C-4) ;
  - ajouts : aucun dans le corps ; les ajouts déclarés sont l'en-tête (C-1, C-2) et le glossaire final ;
  - omissions : aucune (alignement des 410 unités contrôlé ; aucun rapport de longueur par unité hors [0,6 ; 1,5] ;
    lecture) ;
  - renforcement : un, léger (C-3) ; aucun modal ajouté (`may`, `might`, `could`, `likely`, `clearly`, `strongly` :
    0 occurrence ; `can` ×3, `appear` ×3, `shows` ×1, `significan…` ×6 ont chacun leur équivalent dans la source).

Contrôles indépendants (`g2/verif_g2.py`, `g2/verif_g2_registre.py`, écrits par moi sans réutiliser le code du
traducteur ; 0 octet 0x5c dans chacun) :
- blocs de code : 9 et 9, identiques à l'octet et dans le même ordre ;
- nombres : corps anglais sans en-tête ajouté ni glossaire, gloses retirées ; virgule décimale et espace de milliers
  françaises normalisées ; citations gardées lues à la française. Résultat : 3 384 occurrences et 901 valeurs
  distinctes de chaque côté, 0 inventé, 0 perdu ;
- exposants et indices : 39 de chaque côté, identiques ; en-tête ajouté : 0 chiffre ;
- octets : 0 octet 0x5c dans la source et dans la traduction ; 0 CR ; pas de BOM ;
- typographie : aucune espace française avant `;`, `:`, `?`, `!` ou `%` dans les zones anglaises du corps (hors
  libellés scellés gardés et `:=`) ; aucune espace insécable.

## 5. Registre anglais (point 3)

Aucune surclamation. J'ai relevé 57 racines de mots d'assurance en zone anglaise (hors code et citations gardées,
gloses comprises) : 214 occurrences, relues contre la source.
- `independent` et `independence` (18) : modèle à fenêtres indépendantes, paires indépendantes, négations
  (`does not establish the independence of the sources`, `not an independent implementation`), `independent oracle`
  et `code independent of r1` rendus de la source. Aucune forme proscrite par le doc 09 (« sources indépendantes »).
- `verifier` (1) : nom de calcul ; `validator` : nom de rôle ; `validation` (1) : l'en-tête, retiré par C-1.
- `proof` (1) : `not a proof`. `demonstrated` (2) : négations. `trust` (2) : `under trust in FreeTSA`.
- `accuracy` (1) : `Nothing is said about the accuracy of a price`. `authoritative` (1) : rend « fait foi ».
- `compliant` (2) : corrigé par C-6.
- Absents : `guarantee`, `secure`, `safe`, `ensure`, `proves`, `correct price`, `true price`, `trustless`,
  `reproducible`.

Le contrôle 7 du lot (15 locutions de S-G4, 52 locutions anglaises) admet 2 occurrences : la glose `10 sources / 11
feeds` du libellé imprimé « 10 sources / 11 flux ». C'est l'exception déclarée, la même qu'au lot DOCS11-PUBLIC.

## 6. Ton institutionnel et clarté (point 4)

- Ton : registre de rapport méthodologique, phrases déclaratives, sans marketing.
- Corrections de clarté retenues, sans changement de sens : C-4, C-5, C-7, C-8, C-9.
- Les autres gallicismes sont compréhensibles et ne demandent pas de correction. Je les donne en observation O-1
  (section 11).

## 7. Libellés scellés et glossaire (point 5)

- Les 55 gloses sont vérifiées de façon indépendante, à partir des paires du glossaire A de la traduction. Chacune
  apparaît une seule fois, juste après la première occurrence de sa forme française dans le corps (hors blocs de
  code) : 0 défaut.
- J'ai relu le sens de chaque glose : C-5 et C-6 sont à corriger ; les 53 autres sont justes.
- Glossaire B : l'emploi est cohérent dans le corps. Sondage :
  - `déviation` ×8 / `deviation` ×8 ; `divergence` ×9 / ×9 ;
  - « écart » au sens du doc 10 est rendu `anomaly` ; `stream` n'apparaît que dans `upstream`.
- Relevé informatif des termes, rejoué : 22 manques, sortie identique à celle du traducteur ; 0 nouveau manque après
  correction.
- La note `Littlewood and Miller (L&M)` du glossaire B est absente de la source, mais exacte : `biblio/INDEX.md` l.27
  porte Littlewood et Miller, IEEE TSE 15(12), 1989, éq. 28.

## 8. Adjudications de l'orchestrateur (point 6)

- En-tête : l'adjudication n'est pas appliquée dans `ad5289a9…` ; C-1 l'applique. Après correction, le contrôle 10 et
  S-G4 sont verts.
- Paragraphe `Translation conventions` : présent (l.5) et gardé ; une phrase inexacte, corrigée par C-2.

## 9. Motifs interdits (point 7)

- Contrôle 6 du lot, rejoué : 46 motifs, 0 occurrence dans la traduction.
- Mon relevé indépendant (80 motifs et l'expression des lecteurs Windows, insensible à la casse, glossaire compris) :
  0 motif interdit. Trois occurrences examinées et jugées légitimes :
  - `drive letter` (l.131) rend « lettre de lecteur » : ce n'est pas Google Drive ;
  - `filed in the project repository with this report` (l.320 et l.497) rend « versé au dépôt du projet avec ce
    rapport » : c'est le dépôt privé, pas une remise de pièces.
- Pocket, chemins locaux, noms de dépôts privés, identifiants de session, dossiers interdits, pièces de D.2 : 0.

## 10. Limites rendues comme items à former (règle PAROXYSME)

| item proposé | constat | propriétaire | déclencheur |
|---|---|---|---|
| I-G2-1 | pas de ligne DOCS11-EN dans `G0-lots-S2BIS.md` (E-7 du traducteur, toujours vrai à `665898a`) | orch. | avant le versement du lot |
| I-G2-2, confirme I-6 et I-7 du traducteur (SHOGEN-SG5-GUILLEMETS-ANGLAIS-1, SHOGEN-SG4-CITATIONS-TRADUITES-1) | S-G4 exclut les citations entre guillemets anglais (note imprimée par la gate) et S-G5 n'extrait que les « … » : les 43 citations traduites du document anglais échappent aux deux gates ; seul le contrôle du lot leur applique le registre | orch. | versement du document anglais sous `docs/` |
| I-G2-3, confirme I-12 (SHOGEN-PUBLIC-EN-TERMES-1) | l'emploi des termes du glossaire dans le corps n'est mesuré que par un relevé informatif, sans tests ni mutants ; rejoué : 22 manques, tous expliqués par le traducteur | orch. | prochaine retouche du contrôle |
| I-G2-4, nouveau (proposé : SHOGEN-G1-OCTETS-5C-PERIMETRE-1) | un G1 a affirmé « 0 octet 0x5c dans chacun des fichiers écrits » alors que 9 fichiers d'exploration et de sortie en portent ; la consigne B.16 (gabarit) n'a pas été suivie pour `explo/` | orch. (fiche worker, gabarit du G1) | prochain brief de lot |
| I-G2-5, nouveau (source française) | la source ne range que « le sceau, les rendus et les enregistrements » parmi les pièces « remises sur demande, sous accord » (l.10-11 et l.1076). L'annexe B.57 y range aussi les scripts du rédacteur et le paquet scellé, et précise : « sans le paquet, le sceau ne se contrôle pas ». Or le §12 dit qu'un tiers qui reçoit les rendus et le sceau, sans les journaux, « peut contrôler le sceau ». La traduction suit la source ; seule la mention générale de l'en-tête anglais (`supporting documents are provided on request`) s'accorde avec B.57 | orch. (source) ; retouche de l'anglais par I-9 | prochaine retouche du brouillon français, ou feu vert |

## 11. Observations (aucune correction exigée)

- O-1 — Gallicismes compréhensibles, à reprendre si l'orchestrateur le souhaite (sens inchangé) :
  - `Reservation already written` (l.283) → `Caveat already recorded` ;
  - `By pre-declared consequence` (l.196) → `As a pre-declared consequence` ;
  - `has no object on J28` (l.254, l.554) → `does not apply to J28` ;
  - `**Object**` (l.476) → `**Scope**` ;
  - `recounted equal` (l.447, l.448) → `recomputed and found equal` ;
  - `The configured pool counts 12 feeds` (l.60) → `comprises 12 feeds` ;
  - `exclusion of a range of degraded harness` (l.71) → `exclusion of a period of degraded harness operation` ;
  - `go of the investor` (l.451) → `go-ahead of the investor` ;
  - `two witness imputations` (l.615) → `two illustrative imputations`.
  Les titres restent tels quels : ils sont fixés au module.
- O-2 — `English translation of the accepted report` (adjugé) : le paragraphe suivant (l.7) dit aussitôt qu'il s'agit
  de la version publique filtrée. Aucune ambiguïté ne reste.
- O-3 — E-1 du traducteur : la sortie FM-1.1 existe (`en/fm11-traducteur.json`, identique à
  `scripts/controle/sorties-fm11/docs11en-worker.json` à `665898a`). Elle compte 0 fragment de la cartographie l.51 et
  0 de l'ADR-0025 l.14. Je n'en ai lu que la structure (clés et comptes), aucun extrait. L'adjudication revient à
  l'orchestrateur.
- O-4 — `third-party recomputation` rend fidèlement « recalcul tiers » ; le rapport dit lui-même qu'il ne s'agit pas
  d'une implémentation indépendante (§8.6, §9.3 pt 12).
- O-5 — La campagne de mutants écrit dans `mutants/tmp` du lot : un réviseur en lecture seule doit copier le lot (fait
  dans `g2/rejeu/`).
- O-6 — La date `18/09` (§10.1) reste telle quelle, à cause du contrôle des nombres ; elle se lit sans ambiguïté.

## 12. Journal de provenance (G1 du réviseur)

### Sources lues

| source | niveau | empreinte | usage |
|---|---|---|---|
| `g2/BRIEF-G2-DOCS11-EN.md` | [lu], intégral | `03ff5498…92c2` | brief |
| `en/BRIEF-DOCS11-EN.md` | [lu], intégral | `cfe6c0d5…0e69` | règles de traduction |
| `en/G1-lot-DOCS11-EN.md` | [lu], intégral | `5a738619…9836` | journal du traducteur |
| `docs/publication/11-mesures-pilotes-public.md` | [lu], intégral | `4de98654…7688` | source |
| `en/11-pilot-measurements-public-en.md` | [lu], intégral | `ad5289a9…e36d` | traduction |
| `en/TABLE-CORRESPONDANCE-EN.md` | [lu], partiel (tête et comptes) ; régénérée et comparée à l'octet | `a647b9b3…f2d` | table |
| `docs/09-vocabulaire.md` | [lu], intégral | `001b9606…2f31` | registre |
| `en/outils/controle_en.py`, `glossaire_en.py`, `assembler_en.py` | [lu], intégral | `f4eb2fb3…ea8c`, `9a44cda6…5d9c`, `07f8d40d…77a6d0` | contrôle, données, assemblage |
| `en/tests/lancer_tests.py` ; `en/tests/test_controle_en.py` | [lu], intégral ; [lu], partiel (l.1-45, l.505-540, recherches) | `a21bbddf…0b4f` ; `18501634…74be` | contrat du runner ; données des tests |
| `en/mutants/campagne_mutants.py` | [lu], intégral | `9cab5460…0e3c` | campagne |
| `en/explo/termes_survey.py` ; `explo/ctx.py`, `distinctes.py`, `premiers.py` ; `tests/etape-rouge.sortie.txt` | [lu], partiel (l.1-20) ; lignes portant l'octet 0x5c seulement | — | relevé ; C-10 |
| `docs/adr-0029/G0-lots-S2BIS.md` | [lu], intégral | `25a82120…a130` | rattachement |
| `JOURNAL.md` (à `10e860a`) | [lu], partiel : l.382, 384, 396 ; l.118 et l.125 tronquées à 400 caractères (recherche de « sous veto ») | `1213c10d…0814` | rattachement ; C-4 |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | [lu], partiel (l.28-50 : noms des pièces de D.2) | `deb64179…0eaf` | liste interdite |
| `docs/adr-0028/ANNEXE-B-items.md` (à `665898a`) | [lu], partiel (B.57, l.937-955) | `a59f753e…3b27` | rattachement ; I-G2-5 |
| `docs/adr-0028/PAQUET-PREREG-S2.md` | [lu], partiel (l.8 : fragment « Précisions… (i) » ; l.108, 112, 125 par recherche de « veto ») | `4d2a8276…f528` | C-4, C-7 |
| `s2-harness/tools/rendu_unique.py` (tête et `f35a70c`) | [lu], partiel (l.1-12, l.470-506 ; recherche à `f35a70c`) | tête `5ee95dbf…f4b8` ; `f35a70c` `06d189cf…9050` | C-5 |
| `s2-harness/tools/oracle_record.py` (tête et `f35a70c`) | [lu], partiel (l.185-200, l.240-265) | tête `9be02e6b…824f` | C-6 |
| `xtask/src/sg4.rs` ; `xtask/src/sg5.rs` | [lu], partiel (recherche) ; [abs] (empreinte seule) | `b0f7f125…9bdb` ; `e2629451…3f1d` | I-G2-2 |
| `biblio/INDEX.md` | [lu], partiel (l.27, par recherche) | `0fb86390…3dd8` | note L&M |
| `docs/10-mesures-pilotes-design.md`, `docs/04-certificat-diversite.md` | [lu], recherche de « Littlewood » et « L&M » (aucune ligne affichée) | `b306224f…9a44`, `b282f09f…2f8a` | note L&M |
| `en/fm11-traducteur.json` | [lu], structure seule (clés et comptes) | `be512256…a659` | O-3 |
| `docs/publication/interne/TABLE-CORRESPONDANCE.md` ; pièces de D.2 ; `*.jsonl` | [abs] | — | non ouverts |

### Commandes et sorties (heures `date -u`)

| heure UTC | commande | sortie |
|---|---|---|
| 16:56:16 | `sha256sum` du brief ; inventaire de `en/` | brief `03ff5498…92c2`, égal |
| vers 16:57 | `sha256sum` de la source, du registre et des pièces du lot | `4de98654…7688`, `001b9606…2f31`, `ad5289a9…e36d` : égaux |
| vers 16:58 | `git rev-parse HEAD` ; `git log` et `git diff --name-status 4a31685..HEAD` | `10e860a…` ; seuls `scripts/plan-s2bis/*` ajoutés |
| 17:06:41 à 17:13:46 | rejeux du tableau de la section 3 | voir section 3 |
| entre 17:07:31 et 17:12:44 | `verif_g2.py`, `verif_g2_registre.py`, contrôle indépendant des gloses, typographie | voir sections 4, 5, 7 et 9 |
| après 17:13:46 | `git log 10e860a..HEAD` ; `git diff --quiet` sur les entrées du lot | 5 commits de l'orchestrateur ; sortie 0 |
| avant 17:16:51 | `appliquer_corrections.py g2/essai` ; `assembler_en.py` ; contrôle avec `--table` ; tests | 15 remplacements, 6 fichiers ; `f8865abe…1a1b3f` ; CONFORME, sortie 0 ; `Ran 97 tests`, `OK` |
| 17:16:51 à 17:17:27 | campagne de mutants sur `g2/essai/` | 97 tués, 0 vivant, 0 FATAL, témoins OK, MT-23 tué |
| après 17:17:27 | gates sur la copie avec la traduction corrigée ; scripts indépendants sur la version corrigée | S-G4, S-G5, S-G6 vertes ; 3 384 nombres identiques |
| vers 17:20 | `od` sur les fichiers du lot (octet 0x5c) | 9 fichiers hors livrables (C-10) |
| 17:21:25 | empreinte de la table corrigée ; G1 l.347-348 | `9aedd60d…7d0c` |
| 17:22:05 | `git rev-parse HEAD` ; `git status --short` ; empreintes de `en/` | `665898a…` ; 0 ligne ; 452 fichiers de `en/` hors `g2/` aux empreintes inchangées |

### Chiffres recomptés

- Nombres : 3 384 occurrences, 901 valeurs distinctes, de chaque côté (mon script) ; contrôle du lot : composites 2 491
  et suites de chiffres 3 785, de chaque côté (rejoué).
- Blocs de code 9 ; titres 58 ; unités alignées 410 ; gloses 55 ; citations de premier niveau 120 (96 distinctes) ;
  citations gardées 78, traduites 43 (rejoué).
- Tests 97 ; mutants 97 tués sur 97 ; module factice : 79 échecs sur 97 ; suite `s2-harness` : 405 tests.
- Fichiers du lot portant l'octet 0x5c : 9 (C-10) ; livrables : 0.

### Exposition

Aucune pièce de D.2, aucun `*.jsonl` et aucun dossier interdit ouvert. Ce qui a été affiché hors du lot :
- les noms des pièces de D.2 (ANNEXE-D l.28-50), sans valeur ;
- deux lignes du JOURNAL tronquées à 400 caractères (l.118 et l.125), qui citent des chemins du poste local et un
  identifiant de flux de travail : ni pièce de D.2, ni valeur de campagne ;
- des lignes du paquet scellé (l.8, l.108, l.112, l.125), dont des taux de simulations synthétiques déjà publiés au §3.4
  du rapport ;
- la structure de la sortie FM-1.1 (noms de motifs et comptes, aucun extrait).

### Fichiers écrits dans `g2/`

| fichier | sha256 |
|---|---|
| `verif_g2.py` | `8da8a4f8dc2864e7b651e367e647cfa3ab2e1d1b7bb18d483a686894259d1f1b` |
| `verif_g2_registre.py` | `8896ee69f9fe417cd3476dc0fbf57947ef05b1b31602a596e799f3648de2ff45` |
| `appliquer_corrections.py` | `26e3e0c94f0a7974dc7c52ae26457213eaaf75a00bfcf0d32b4c62f7aac7fcb0` |
| `corrections-G2.diff` | `09a641ba1f351c75582dcb163406c845d9cb8883f9fbfb614ed8789d1b1bd1a9` |
| `controle-rejoue.sortie.txt` | `552c6a9436395a630db94d79423870061e4f61e54ca18320f31e0c65d677f079` |
| `tests-reel.sortie.txt` ; `tests-factice.sortie.txt` | `4ac7a30e167e5ddf93ee0356a312b41e81dffe214e14c68f23d1641d45b9c11f` ; `365b16f2391042cd0b65f2351204d471ef6f2e40d4600222125e0972d5e01bb6` |
| `mutants-rejoues.sortie.txt` (identique à `essai-mutants.sortie.txt`) | `f966a888e73e7e199ace89fd99bb20f08ec16147b87f42189cc9a7c4854af203` |
| `gates-rejouees.sortie.txt` (identique à `essai-gates.sortie.txt`) | `138fbb09cb1d59cf585da6afe69e23c64e62d6c3dd7d1bd2410e0586d0ffc627` |
| `suite-s2-harness.sortie.txt` | `f460eeab8d822e88377636e627d9cf0294db6faca93571bf3a83dca47be22e9a` |
| `registre.sortie.txt` ; `essai-registre.sortie.txt` | `0cca7749c9f4b260872f665e161ffd94baed122762cccb9df746d5183641e529` ; `14347eef520b89299494cf38ee838d951666a73d1a3925f51b2f0396d3efcd41` |
| `termes-rejoue.sortie.txt` (identique à `essai-termes.sortie.txt`) | `d02685d3880ad305b0e8347fb31e8cfe480b0c773965197d0ed8d8b1fcd3e236` |
| `essai-controle.sortie.txt` ; `essai-tests.sortie.txt` | `09c04be99195c776d6c6fdf5d115e526b2a0a00097cf15d5b235a6da01ba2f96` ; `81b509bc7c8eda441476b04398a1c9130131acb9d8cab9a693440c8b87f41121` |
| dossiers `rejeu/`, `essai/`, `gates/`, `tmp/`, `tmp-suite/` | copies de travail (contenus décrits plus haut) |

## 13. Résumé court

La traduction anglaise est fidèle. J'ai lu les 58 sections dans les deux langues : verdict, nombres, limites et
déviations sont rendus sans écart, sans ajout ni omission. J'ai rejoué tous les contrôles : ils redonnent, à l'octet,
les sorties du traducteur. Le contrôle passe onze points sur onze ; 97 tests sont verts, 97 mutants sur 97 sont tués ;
les gates S-G4, S-G5 et S-G6 sont vertes ; la suite `s2-harness` passe ses 405 tests. Mes propres scripts confirment
3 384 nombres identiques et 0 motif interdit.

Verdict : **ACCEPTE-AVEC-CORRECTIONS**, dix corrections :
- l'en-tête adjugé, non appliqué dans la version livrée (C-1) ;
- une phrase inexacte des conventions (C-2) ;
- un article qui renforce la source (C-3) ;
- `under veto`, à lire `subject to veto` (C-4) ;
- deux gloses (C-5, C-6) et trois faux amis (C-7 à C-9) ;
- une affirmation inexacte du G1 sur les octets 0x5c (C-10).

Appliquées sur une copie, ces corrections passent tous les contrôles. Cinq items sont rendus à l'orchestrateur, dont
deux nouveaux : I-G2-4 (périmètre du compte d'octets 0x5c dans un G1) et I-G2-5 (régime « sur demande » de la source,
à harmoniser avec l'annexe B.57).
