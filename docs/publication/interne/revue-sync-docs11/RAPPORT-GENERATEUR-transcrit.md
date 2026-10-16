# Rapport du générateur du lot SYNC-DOCS11 (phases 1 et 2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 20:36:18 UTC du fichier sync-docs11/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (238 occurrences). Texte ci-dessous avec 2 retouche(s) (E38) : le mot anglais cité comme locution de la gate S-G4 est mis entre guillemets français, sans autre changement ; sans autre retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — lot SYNC-DOCS11 (SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort `high` (fiche `shogen-worker`, générateur G1 ; réviseur G2 à nommer,
  distinct).
- **Rattachement (G0)** : item SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1, `docs/adr-0028/ANNEXE-B-items.md` l.1854 (ligne lue) ;
  décision de l'investisseur du 2026-10-16 (préparer le diff et l'appliquer), consignée par l'orchestrateur ; ADR-0028 §4
  pt 4 (la publication reste la décision de l'investisseur). Brief : `BRIEF.md` de ce dossier (2026-10-16 18:05:30 UTC).
- **Base** : dépôt `/home/user/shogen` à `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (`git rev-parse HEAD`, 2026-10-16
  18:05 UTC) ; fichiers cibles inchangés depuis `3c64e6a`. Empreintes à la base : docs/11 `10f368da…52c9` (1120 l.),
  version française publique `5de6e716…08b6` (1081 l.), version anglaise publique `34d5b233…c10d` (760 l.). Copie
  creuse par `git archive HEAD` (chemins explicites) dans `copie/` ; aucune écriture dans le dépôt, aucune commande git
  en écriture.
- **Heure de l'ajout daté** : `2026-10-16 18:11:04 UTC`, lue par `date -u` avant l'écriture.

## 1. Livrables

| fichier | contenu | sha256 |
|---|---|---|
| `diffs/SYNC-FR.diff` | `docs/publication/11-mesures-pilotes-public.md` : 49 lignes ajoutées en fin (l.1082-1130), 0 retirée ; 1081 → 1130 l. | `4fdede21e94ab67c333d0d7e73f6b028837d75a30fedc86fabb7f55bb1e43543` |
| `diffs/SYNC-EN.diff` | `docs/publication/11-pilot-measurements-public-en.md` : 11 lignes ajoutées en fin (l.761-771), 0 retirée ; 760 → 771 l. | `197955fc2739d5bee7dabe606fa5956d1b437e7a7b8e766ad8ad69d457c66c92` |

Diffs unifiés, chemins `a/` `b/`, saut de ligne final ; appliqués par `git apply` sur une copie de la base : fichiers
égaux à l'octet aux versions construites (FR `fe02a202…959f`, EN `edd47c9f…4f81`).

## 2. Forme retenue

- **Lieu** : en fin de document dans les deux langues, comme dans docs/11 : aucune ligne existante ne bouge ni ne
  change (contrôle V1/V2, préfixe exact). En anglais, la fin du document suit le glossaire (l.641-760) : la section est
  écrite après lui, pour ne décaler aucune des lignes du glossaire citées par numéro (annexe B l.1704 : l.672, 714, 715).
- **Français** : les 49 lignes de docs/11 (l.1072-1120) sont recopiées une à une (l.1082-1130 = l.1072-1120 + 10), à
  deux retouches près, déclarées :
  - **E-29** (l.1075 → l.1085) : l'ajout daté du portage, `*Ajout daté du 2026-10-16 18:11:04 UTC (`date -u`) ;
    portage dans la version publique* : …`, est placé en tête de la ligne, le texte source suit intact. Motif : une
    ligne qui commencerait par l'entrée datée du 2026-10-10 serait refusée par `avant_acte.py` (contrôle C4,
    `heure-passee` : antérieure à la dernière entrée datée du fichier, 2026-10-15 20:37:28).
  - **E-30** (l.1096 → l.1106) : `pas garanti,` devient `pas tenu,` (registre du doc 09 : `garanti` est dans la liste
    LOCUTIONS_09 de `controle_public` ; l'anglais `guaranteed` est une des 15 locutions de la gate S-G4). Le mot vient
    de la même phrase source (`son niveau ne serait pas tenu`) ; même sens, aucun nombre. L'ajout daté du portage le
    dit (`sauf une formule mise au registre du vocabulaire du projet`).
- **Anglais** : traduction fidèle, une ligne par paragraphe ou élément de liste (usage du fichier anglais) ; mêmes
  conventions que le corps (lot = `work package`, `[inféré]` = `[inferred]`, `« de type Manski »` = `“Manski-type”`
  comme au §11.1 anglais, nombres à l'anglaise, dates ISO gardées) ; les citations anglaises d'origine (gardées entre
  « » dans le français, presg5 : 0 fragment) sont rendues entre guillemets anglais.
- **Filtrage** (règle de la table de correspondance) : aucun passage retiré. Aucun chemin de poste local, nom de
  dépôt privé, identifiant de session ou d'agent, pièce de D.2 ni dossier interdit dans les 49 lignes (contrôle 2 de
  `controle_public` : 0 motif) ; aucun acteur mesuré nommé (relevé par script des 24 alias des acteurs d'`ACTEURS-NOMMES.md`, bornes de lettre : 0 mention,
  `sorties/acteurs.sortie.txt` ;
  les auteurs et NIST/SEMATECH sont des sources de méthode, comme Künsch et Kiefer-Vogelsang au §1 de cette pièce).
  Examinés et gardés : les décisions Q-B et Q-C de l'adjudication du procurement (l.1080, l.1119), renvois internes
  traités comme les renvois aux décisions et au JOURNAL (G-05, G-06) et comme P-05 et P-08, déjà publics au §11.1 ;
  les chemins relatifs au dépôt `biblio/INDEX.md` et `scripts/post-s2/contenu.py` (précédent G-14).

## 3. Table ligne par ligne (49 lignes : 49 portées, dont 2 retouchées ; 0 non portée)

FR : ligne de la version française après le diff ; EN : ligne de la version anglaise qui porte la traduction.

| docs/11 | FR | EN | état | motif |
|---|---|---|---|---|
| l.1072 | l.1082 | l.761 | portée | ligne vide |
| l.1073 | l.1083 | l.762 | portée | portée à l'identique |
| l.1074 | l.1084 | l.763 | portée | ligne vide |
| l.1075 | l.1085 | l.764 | portée, retouchée | portée avec retouche E-29 : ajout daté du portage (2026-10-16 18:11:04 UTC) placé en tête, texte source intact à la suite |
| l.1076 | l.1086 | l.764 | portée | portée à l'identique |
| l.1077 | l.1087 | l.764 | portée | portée à l'identique |
| l.1078 | l.1088 | l.765 | portée | ligne vide |
| l.1079 | l.1089 | l.766 | portée | portée ; référence interne (décisions Q-B et Q-C, adjudication du procurement) examinée et gardée, comme les renvois aux décisions et au JOURNAL (G-05, G-06) |
| l.1080 | l.1090 | l.766 | portée | idem l.1079 |
| l.1081 | l.1091 | l.766 | portée | portée ; chemin relatif au dépôt `biblio/INDEX.md` gardé (précédent G-14) |
| l.1082 | l.1092 | l.767 | portée | ligne vide |
| l.1083 | l.1093 | l.768 | portée | portée à l'identique |
| l.1084 | l.1094 | l.768 | portée | portée ; chemin relatif au dépôt `scripts/post-s2/contenu.py` gardé (précédent G-14) |
| l.1085 | l.1095 | l.768 | portée | portée à l'identique |
| l.1086 | l.1096 | l.768 | portée | portée à l'identique |
| l.1087 | l.1097 | l.768 | portée | portée ; citation anglaise d'origine gardée en FR (presg5 : 0 fragment), entre guillemets anglais en EN |
| l.1088 | l.1098 | l.768 | portée | portée à l'identique |
| l.1089 | l.1099 | l.768 | portée | portée à l'identique |
| l.1090 | l.1100 | l.769 | portée | portée à l'identique |
| l.1091 | l.1101 | l.769 | portée | portée à l'identique |
| l.1092 | l.1102 | l.769 | portée | portée à l'identique |
| l.1093 | l.1103 | l.769 | portée | portée à l'identique |
| l.1094 | l.1104 | l.769 | portée | portée à l'identique |
| l.1095 | l.1105 | l.769 | portée | portée à l'identique |
| l.1096 | l.1106 | l.769 | portée, retouchée | portée avec retouche E-30 : garanti devient tenu (registre du doc 09, liste LOCUTIONS_09 ; EN : held, S-G4 interdit « guaranteed ») |
| l.1097 | l.1107 | l.769 | portée | portée ; citation anglaise d'origine (voir l.1087) |
| l.1098 | l.1108 | l.769 | portée | idem l.1097 |
| l.1099 | l.1109 | l.769 | portée | portée à l'identique |
| l.1100 | l.1110 | l.769 | portée | portée à l'identique |
| l.1101 | l.1111 | l.769 | portée | portée à l'identique |
| l.1102 | l.1112 | l.769 | portée | portée à l'identique |
| l.1103 | l.1113 | l.769 | portée | portée à l'identique |
| l.1104 | l.1114 | l.770 | portée | portée à l'identique |
| l.1105 | l.1115 | l.770 | portée | portée à l'identique |
| l.1106 | l.1116 | l.770 | portée | portée à l'identique |
| l.1107 | l.1117 | l.770 | portée | portée à l'identique |
| l.1108 | l.1118 | l.770 | portée | portée à l'identique |
| l.1109 | l.1119 | l.770 | portée | portée à l'identique |
| l.1110 | l.1120 | l.770 | portée | portée à l'identique |
| l.1111 | l.1121 | l.770 | portée | portée à l'identique |
| l.1112 | l.1122 | l.770 | portée | portée à l'identique |
| l.1113 | l.1123 | l.771 | portée | portée ; « de type Manski » traduit “Manski-type” comme au §11.1 de la version anglaise |
| l.1114 | l.1124 | l.771 | portée | portée ; citation anglaise d'origine (voir l.1087) |
| l.1115 | l.1125 | l.771 | portée | idem l.1114 |
| l.1116 | l.1126 | l.771 | portée | idem l.1114 |
| l.1117 | l.1127 | l.771 | portée | portée à l'identique |
| l.1118 | l.1128 | l.771 | portée | portée à l'identique |
| l.1119 | l.1129 | l.771 | portée | portée ; « Aucun achat (décision Q-B) » : référence interne gardée (voir l.1079) |
| l.1120 | l.1130 | l.771 | portée | portée à l'identique |

## 4. Une citation, un grep (partie française ajoutée contre partie anglaise ajoutée)

Produite par `outils/verifier_sync.py` (contrôle V4) : chaque nombre (virgule décimale ramenée au point) et chaque
identifiant (majuscules à trait d'union) de la partie française ajoutée, compté dans la partie anglaise ajoutée, et
réciproquement. 52 jetons, 0 écart.

| genre | jeton | compte FR | compte EN | état |
|---|---|---|---|---|
| nombre | 0.02 | 2 | 2 | OK |
| nombre | 0.04 | 1 | 1 | OK |
| nombre | 0266466605050565 | 1 | 1 | OK |
| nombre | 04:56:09 | 2 | 2 | OK |
| nombre | 05-08 | 1 | 1 | OK |
| nombre | 1 | 9 | 9 | OK |
| nombre | 1.3.5.15 | 1 | 1 | OK |
| nombre | 10.1017 | 1 | 1 | OK |
| nombre | 11.1 | 4 | 4 | OK |
| nombre | 1130-1164 | 1 | 1 | OK |
| nombre | 13 | 2 | 2 | OK |
| nombre | 14 | 5 | 5 | OK |
| nombre | 18:11:04 | 1 | 1 | OK |
| nombre | 1975 | 1 | 1 | OK |
| nombre | 1989 | 2 | 2 | OK |
| nombre | 1997 | 1 | 1 | OK |
| nombre | 1999 | 1 | 1 | OK |
| nombre | 2 | 6 | 6 | OK |
| nombre | 2.2 | 1 | 1 | OK |
| nombre | 2.377 | 1 | 1 | OK |
| nombre | 2.459 | 1 | 1 | OK |
| nombre | 2010 | 1 | 1 | OK |
| nombre | 2010-40 | 1 | 1 | OK |
| nombre | 2019 | 1 | 1 | OK |
| nombre | 2024-04-01 | 1 | 1 | OK |
| nombre | 2026-10-09 | 2 | 2 | OK |
| nombre | 2026-10-10 | 2 | 2 | OK |
| nombre | 2026-10-16 | 1 | 1 | OK |
| nombre | 21 | 1 | 1 | OK |
| nombre | 240 | 2 | 2 | OK |
| nombre | 26 | 1 | 1 | OK |
| nombre | 28 | 1 | 1 | OK |
| nombre | 3 | 3 | 3 | OK |
| nombre | 31 | 1 | 1 | OK |
| nombre | 4 | 1 | 1 | OK |
| nombre | 449 | 1 | 1 | OK |
| nombre | 5 | 2 | 2 | OK |
| nombre | 5.4 | 1 | 1 | OK |
| nombre | 6 | 3 | 3 | OK |
| nombre | 7 | 1 | 1 | OK |
| nombre | 77-84 | 1 | 1 | OK |
| nombre | 875 | 1 | 1 | OK |
| nombre | 95 | 1 | 1 | OK |
| nombre | 99 | 1 | 1 | OK |
| identifiant | DETTES-T14 | 4 | 4 | OK |
| identifiant | Q-B | 2 | 2 | OK |
| identifiant | Q-C | 1 | 1 | OK |
| identifiant | SHOGEN-CENSURE-INFO-2 | 1 | 1 | OK |
| identifiant | SHOGEN-CENSURE-ZBLOC-1 | 1 | 1 | OK |
| identifiant | SHOGEN-DEP-FENETRES-2 | 2 | 2 | OK |
| identifiant | SHOGEN-PEARSON-IF-SOURCE-1 | 1 | 1 | OK |
| identifiant | SHOGEN-R1-PLUGIN-1 | 2 | 2 | OK |

## 5. Contrôles rejoués (sorties dans `sorties/`, rejeu complet : `bash outils/rejouer.sh`)

| contrôle | entrée | résultat |
|---|---|---|
| `outils/verifier_sync.py` (spécification écrite à la main, indépendante du constructeur : V1 FR, V2 EN, V3 registre des deux outils, V4 une citation un grep, V5 dates) | état d'avant | NON CONFORME, 6 écarts, sortie 1 (étape rouge) |
| idem | état d'après | CONFORME, 52 jetons, 0 écart, sortie 0 |
| `outils/mutants_verifier.py` (une mutation par cas, groupe de processus neuf, borne 120 s) | 8 mutants | 8 tués, 0 vivant, 0 FATAL ; relevé `ps` de fin : 0 processus restant |
| `scripts/controle/presg5.py` (racine : dépôt, pour les octets de `biblio/`) | deux fichiers après diff | 0 fragment, sortie 0 |
| R-13 (`TODO`, `FIXME`, `XXX` sur les lignes ajoutées) | deux diffs | 0 |
| `avant_acte.py --lecture-seule diff --fichier … --rapport RAPPORT-GENERATEUR.md` | `SYNC-FR.diff`, `SYNC-EN.diff` | sortie 0 chacun (rejoué sur ce rapport final, `sorties/avant_acte.*.sortie.txt`) |
| `controle_public` (copie amendée `44265e7f…5be4`, non versée), configuration versée : source docs/11 à `2db4f40` (`fcf93b87…53b7`), table versée (`ee8f87a4…b5e2`) | brouillon de base | CONFORME 7/7 (référence) |
| idem | brouillon après diff | NON CONFORME : 1. nombres (44 inventés, 101 ajoutés : ceux des 49 lignes, absentes de la source à `2db4f40`) ; 5. section « Ajouts datés en fin de document » non déclarée ; 6. titres 58 / 59. Contrôles 2, 3, 4, 7 : OK |
| idem, configuration de travail : source docs/11 à la tête (`10f368da…52c9`), table versée + E-29 et E-30 (`work/cpB/`, pièce de travail) | brouillon après diff | NON CONFORME sur **1. nombres seulement** : 2 inventés et 8 ajoutés, tous jetons de `2026-10-16 18:11:04` (E-29) ; 2 à 7 OK (rejeu des 30 retouches identique à l'octet, titres 59 / 59, citations 152 / 152) |
| `controle_en` versé (`b42777db…bb4c`, glossaire `d909935c…328f`) | paire de base | CONFORME 11/11 (référence) |
| idem | paire après diffs | FATAL, sortie 3 : source française non épinglée (`SOURCE_SHA256`) |
| idem, données de travail (`work/en-travail/glossaire_en.py` : épingle `fe02a202…959f`, titre de la section, citations C-43 à C-47 des cinq citations anglaises d'origine) | paire après diffs | NON CONFORME : 1. alignement (source 417 unités, corps 410) et 11. glossaire (7 unités après les deux tables) : la section suit le glossaire, que l'outil veut dernier |
| idem, section déplacée avant le glossaire (traduction de travail, alignement seul) | paire de travail | **CONFORME 11/11** : nombres identiques par unité et dans l'ordre (composites 1070 / 1070 distincts), citations, gloses, registre anglais (S-G4 compris), résidus français, convention des nombres |

Constats en cours de lot, tous corrigés avant les sorties finales (journal `NOTES.md`) : `garanti` / `guaranteed`
(E-30) ; entrée datée du 2026-10-10 en tête de ligne (E-29) ; une date 2026-10-10 de trop dans l'ajout daté du portage
(retirée) ; `zero means` compté comme nombre en lettres par `controle_en` (rendu `vanishing means`).

## 6. Limites, rendues comme items à former

- **L-1 — en-têtes.** La l.13 française (`hors les dates des ajouts datés du 2026-10-15`) et la l.7 anglaise
  (`except the dates of the dated additions of 2026-10-15`) ne nomment pas la date du portage (2026-10-16 18:11:04,
  seuls nombres ajoutés par rapport à docs/11 à la tête, config. B) ; la l.7 française et la l.7 anglaise
  disent `une formule` / `one wording` mise au registre, il y en a désormais deux (E-03, E-30) ; l'en-tête anglais
  l.5 dit le glossaire `at the end of this document`, la section portée le suit. Aucune ligne existante ne pouvant
  changer (brief), rien n'est fait : proposition, mention `hors les dates des ajouts datés` sans date, et `des
  formules`, par un lot qui touche l'en-tête.
- **L-2 — contrat de `controle_public`.** Sa source est docs/11 à `2db4f40` ; sur elle, le brouillon porté ne peut
  pas être conforme. Pour un vert : source docs/11 à la tête, rangées E-29 et E-30 versées à la table (forme dans
  `work/cpB/TABLE-CORRESPONDANCE.travail.md`), et admission de la date d'un ajout daté placé en tête de ligne (le
  contrat du 2026-10-15 n'admet que la forme suffixe, `AJOUTS_DATES`). Non desserré. L'outil n'est toujours pas versé
  (item SHOGEN-PUBLICATION-OUTILS-PUBLIC-VERSES-1).
- **L-3 — contrat de `controle_en`.** Épingle à reporter dans `glossaire_en.py` (`SOURCE_SHA256` = `fe02a202…959f`),
  avec le titre de la section et les citations C-43 à C-47 (forme dans `work/en-travail/glossaire_en.py`) ; et le
  contrôle 11 refuse toute unité après le glossaire. Trois voies : (a) admettre une section d'ajouts datés après le
  glossaire ; (b) placer la section avant le glossaire, ce qui décale ses lignes (l.641-760, citées par numéro) ;
  (c) adjudication écrite. Le brief ne demande que deux diffs : le diff de données n'est pas produit.
- **L-4 — sorties versées.** `interne/controle_public.sortie.txt`, `interne/controle_en.sortie.txt`,
  `interne/TABLE-CORRESPONDANCE.md` et `TABLE-CORRESPONDANCE-EN.md` décrivent l'état d'avant ; leur régénération suit
  L-2 et L-3.
- **L-5 — renvois internes gardés.** Q-B, Q-C (l.1080, l.1119) : gardés par cohérence avec G-05 et G-06 ; si
  l'orchestrateur les juge gouvernance interne sans objet pour un lecteur extérieur, une retouche E-31 (phrase neutre)
  est possible ; à adjuger.
- **L-6 — PDF.** Le PDF anglais n'est pas reconstruit (hors mandat) ; son pied de page porte l'empreinte de
  l'anglais d'avant.
- **L-7 — `ACTEURS-NOMMES.md`.** Aucun acteur mesuré nouveau ; le relevé reste périmé (item ouvert
  SHOGEN-PUBLICATION-ACTEURS-RELEVE-1).

## 7. Phrase de fermeture proposée (annexe B)

« SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1 : fermé le <date> (commit `<…>`, G2 neuve <verdict>). Les 49 lignes ajoutées à
docs/11 par `6c04e91` (l.1072-1120) sont portées en fin des deux versions publiques, sous un ajout daté du
2026-10-16 18:11:04 UTC : français l.1082-1130, recopie ligne à ligne à deux retouches déclarées près (E-29 : ajout
daté du portage en tête de la l.1085 ; E-30 : `garanti` devient `tenu`, registre du doc 09) ; anglais l.761-771,
après le glossaire, traduction contrôlée (52 jetons, 0 écart ; `controle_en` 11/11 avec données de travail et section
avant le glossaire). Aucune ligne existante changée ni décalée ; aucune ligne non portée. Restent L-1 (en-têtes),
L-2 et L-3 (contrats des deux contrôles), L-4 (sorties à régénérer) ; L-5 à adjuger. »

## 8. Journal de provenance (G1)

Journal horodaté : `NOTES.md` (même dossier ; heures du 2026-10-16, UTC). Sources [lu] : brief (en entier) ;
annexe B l.1845-1856 ; `git show 6c04e91 -- docs/11-mesures-pilotes.md` (entier) ; les cinq pièces internes et le
rapport transcrit du lot d'amendements (en entier) ; versions publiques (en-têtes, fins, §11.1) ; `presg5.py` (entier) ;
`controle_en.py`, `glossaire_en.py`, `controle_public.py` amendé, `avant_acte.py`, `garde_commun.py` (parties citées
au journal). [2nd] : aucun chiffre de seconde main ; chaque compte de ce rapport est affiché par un outil dans
`sorties/` ou au journal.

Écarts : E-1, une liste par motif (`docs/publication/*.md`) dans une copie de ce dossier ; E-2, une chaîne Python
tapée avec séquences d'échappement, résultat recompté sans barre (détail : `NOTES.md`).

Outils du lot (`outils/`, bibliothèque standard) : `construire_sync.py`, `verifier_sync.py`, `mutants_verifier.py`,
`table_travail.py`, `donnees_en_travail.py`, `table_lignes.py`, `rejouer.sh` ; copies des contrôles :
`controle_public.py`, `controle_en.py`, `glossaire_en.py`. Empreintes : `SHA256SUMS`.

## Phase 2 (2026-10-16, après l'adjudication de L-1 à L-6 par l'orchestrateur)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort `high` (même générateur).
- **Rattachement** : message du coordinateur (adjudication : décisions 1 à 6 sur L-1 à L-6) ; même item, même base
  `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (relue à la fin, inchangée) ; même règles (dépôt en lecture seule, copie
  creuse, diffs à l'octet). Horodatage de l'amendement A-10 du glossaire : `2026-10-16T18:30:32Z` (`date -u`).
- **Ordre d'application** : SYNC-FR, SYNC-EN (phase 1, inchangés), puis SYNC-ENTETES, SYNC-CONTROLE-EN, SYNC-TESTS-EN,
  SYNC-GLOSSAIRE-EN, SYNC-TABLE, SYNC-TABLE-EN, SYNC-SORTIE-PUBLIC, SYNC-SORTIE-EN. Chacun s'applique seul sur la base
  (`git apply --check`) ; les dix appliqués dans cet ordre sur une copie de la base redonnent `final/` à l'octet.
  Un commit par diff : entre SYNC-ENTETES et SYNC-GLOSSAIRE-EN, `controle_en` versé sort en FATAL (épingle) ; à commiter à
  la suite.

### Diffs de la phase 2 (un par cible, au plus 200 lignes ajoutées chacun)

| diff | cible | ajoutées / retirées | sha256 |
|---|---|---|---|
| `diffs/SYNC-ENTETES.diff` | FR l.7 et l.13, EN l.5 et l.7 | 4 / 4 | `65b5f28c46b3434ff5c939c9c32736e01307b731716a4da3a7adfef159d3ed70` |
| `diffs/SYNC-CONTROLE-EN.diff` | `scripts/publication/en/outils/controle_en.py` | 15 / 4 | `7e33586b0403202b2da1bfd97e2e175a64cdc4d10a99671d48a1d1140bf801ba` |
| `diffs/SYNC-TESTS-EN.diff` | `scripts/publication/en/tests/test_controle_en.py` | 65 / 0 | `b4ae87f20c7623e7701e9edb64f6dc89f91440d48e1b9d511cb5e470476d6f44` |
| `diffs/SYNC-GLOSSAIRE-EN.diff` | `scripts/publication/en/outils/glossaire_en.py` (l.7, 40, 42 ; 18 lignes en fin) | 21 / 3 | `b31deb7ef99d08215baab63e45cf31818e9dc4671eb6ed10f23d84650f9371a1` |
| `diffs/SYNC-TABLE.diff` | `docs/publication/interne/TABLE-CORRESPONDANCE.md` (l.3, 5, 6, 7 ; 9 lignes en fin) | 13 / 4 | `f63102093348b623a0f6dcde60dc3079f5149ccdeacff68d2724e46e9b25c296` |
| `diffs/SYNC-TABLE-EN.diff` | `docs/publication/interne/TABLE-CORRESPONDANCE-EN.md` (régénérée) | 3 / 2 | `1085fc61e122bcdd67ac7b2decae8ff79f26570dfd8c3c332409485874a17982` |
| `diffs/SYNC-SORTIE-PUBLIC.diff` | `docs/publication/interne/controle_public.sortie.txt` (régénérée) | 20 / 19 | `00a4bf2f99bd8338fecc3d210c6932c7092609fe64119ed37589d3ae42161577` |
| `diffs/SYNC-SORTIE-EN.diff` | `docs/publication/interne/controle_en.sortie.txt` (régénérée) | 9 / 9 | `c58d2c213d61b6b80147384134178c4dc7704b1f92f909a4eb7fc1b768799d22` |

Hors dépôt (l'outil n'est pas versé, item SHOGEN-PUBLICATION-OUTILS-PUBLIC-VERSES-1) : `diffs/revue-controle_public.diff`
(31 / 4) et `diffs/revue-test_controle_public.diff` (93 / 3), du lot d'amendements (`44265e7f…5be4`, `dbf9a523…8f15`) à
`outils-public/controle_public.py` (`92636b3b…aec`) et `tests-public/test_controle_public.py` (`b4dcae21…2c07`).

État final : FR `3ca9f599ef8d6ace69163c9c1d3e2ee8fa3effb118d75b181185f2eb54ee6a8b` (1130 l.), EN
`6db435db6215c65623d6b8dea9a5f381a7aae173fca76018dd263afde7dcc8dd` (771 l.), table `aba4d0f5…5646`, table anglaise
`aa2f5e7c…3646`, `controle_public.sortie.txt` `5a649b5f…7886`, `controle_en.sortie.txt` `ee17e7e6…67d4`,
`controle_en.py` `fea95d3e…bb0f`, `glossaire_en.py` `13f280c3…4fc2`, `test_controle_en.py` `87c427fe…268b`.

### L-1 — en-têtes (SYNC-ENTETES ; table E-31, E-32)

- FR l.7 : `une formule est mise au registre` devient `deux formules sont mises au registre` (E-31, second ordre sur E-01).
- FR l.13 : `hors les dates des ajouts datés du 2026-10-15.` devient `… du 2026-10-15 et du 2026-10-16.` (E-32, second ordre
  sur E-28 ; liste MENTIONS_DE_DATE).
- EN l.5 : `the glossary at the end of this document lists the glosses` devient `the glossary that follows the body of the
  report, before the dated additions carried over at the end of this document, lists the glosses` (sans chiffre :
  contrôle 10 de `controle_en`).
- EN l.7 : `one wording is` devient `two wordings are` ; `of 2026-10-15.` devient `of 2026-10-15 and 2026-10-16.`
- Les retouches anglaises n'entrent pas dans la table française (`controle_public` la rejoue sur le français) ; elles sont
  déclarées à l'amendement A-10 de `glossaire_en.py` et ici. `outils/verifier_p2.py` : seules les lignes FR 7 et 13 et EN 5
  et 7 changent, plus les lignes de fin ; le seul nombre ajouté aux en-têtes est `2026-10-16`.

### L-2 — contrat de `controle_public` (amendé le 2026-10-16)

- (a) Ajout daté en tête de ligne admis : `après = préfixe + avant`. Le préfixe s'ouvre par `*Ajout daté du AAAA-MM-JJ
  hh:mm:ss UTC[ libellé sans chiffre ni astérisque]* : `, tient sur une ligne, se trouve une seule fois dans le brouillon,
  au début d'une ligne. Il est exclu du compte comme un suffixe. E-29 entre dans AJOUTS_DATES, E-32 dans MENTIONS_DE_DATE.
- (b) Épingle : la ligne de la table qui commence par `- Source :` et porte un sha256 entre accents graves épingle la source ; une autre source est FATAL (3). La l.5
  de la table épingle docs/11 à la tête (`10f368da…52c9`, blob `6708185f`, dernier commit `6c04e91`, base `fe9a72b`).
- Rangées E-29 à E-32 versées en fin de table (section « Retouches E-29 à E-32 »).
- **Tests d'abord** : outil d'origine, suite de 104 tests verte (référence) ; 12 tests ajoutés et 2 retouchés (E-29 entre
  dans la liste : le test du n° hors liste passe à E-90 ; liste fermée) : rouge, 4 échecs, sortie 1 ; outil amendé :
  117 tests OK, sortie 0.
- **Mutants** (`outils/mutants_public_p2.py`, une mutation par cas) : 10 tués, 0 vivant, 0 FATAL. Un premier tour a laissé MQ10
  vivant (ancre en fin non exigée) : test `test_prefixe_dont_l_ancre_change_sans_nombre` ajouté, MQ10 tué ; MQ1 refait sur
  la marque (FATAL au premier tour : mutant mal formé). Les 7 mutants MP du lot d'amendements, rejoués : 7 tués.
- **Sortie versée régénérée** (`SYNC-SORTIE-PUBLIC`) : **CONFORME, sept contrôles sur sept** ; 0 inventé, 0 ajouté,
  0 retouche qui ajoute un nombre ; ajouts datés exclus : E-24, E-25, E-26 (2026-10-15), E-29 (2026-10-16) ; rejeu des 32
  retouches identique à l'octet ; titres 59 / 59 ; citations 152 / 152. Recette contrôlée : sur la base, la même commande
  redonne à l'octet les trois sorties versées (`work/recette/`).

### L-3 — contrat de `controle_en` (amendé le 2026-10-16)

- La section anglaise reste après le glossaire (lignes 641-760 non décalées). Une section d'ajouts datés peut suivre le
  glossaire final si son titre est AJOUTS_FIN_TITRE des données ; elle n'est pas du glossaire (contrôle 11), elle est alignée
  sur la fin de la source et soumise aux contrôles 1 à 9. Sans titre déclaré, toute unité après les deux tables reste
  refusée.
- `glossaire_en.py` (A-10) : épingle `3ca9f599…6a8b` (l.42 ; l.7 et l.40 mises au courant), AJOUTS_FIN_TITRE, titre de la
  section, citations C-43 à C-47.
- **Tests d'abord** : suite d'origine, 101 tests OK ; 7 tests ajoutés, rouges sur l'outil d'origine (5 échecs, sortie 1) ;
  outil amendé : 108 tests OK. Les 69 mutants MC du lot DOCS11-EN rejoués sur l'outil amendé : 69 tués (ancres intactes).
- Mutants du code ajouté (`outils/mutants_en_p2.py`), un mutant tué par test ajouté au moins :
  - `test_section_apres_glossaire_conforme` : mutants ME3, ME4 et ME7 tués ;
  - `test_sans_titre_declare_refusee` : mutant ME5 tué ;
  - `test_autre_titre_apres_glossaire_refuse` : mutant ME5 tué ;
  - `test_nombres_de_la_section_controles` : mutant ME3 tué ;
  - `test_registre_de_la_section_controle` : mutants ME1 et ME2 tués ;
  - `test_corps_comprend_la_section_sans_le_glossaire` : mutants ME1, ME2 et ME7 tués ;
  - `test_separer_section_hors_glossaire` : mutants ME3 et ME4 tués.
  Bilan : 6 mutants, 6 tués. Un mutant d'un premier tour (ME6, `queue and` retiré) était équivalent : la condition
  redondante est retirée du code de `separer`, et le mutant de la liste. ME5 a été refait (FATAL au premier tour).
- **Sortie versée régénérée** (`SYNC-SORTIE-EN`, `SYNC-TABLE-EN`) : **CONFORME, onze contrôles sur onze** ; unités 417 / 417,
  glossaire final 116 ; titres alignés 59 ; nombres identiques par unité (composites 1070 / 1070 distincts) ; table
  anglaise : une rangée 59 de plus (« Ajouts datés en fin de document », 75 = 75 nombres).

### L-4 — sorties et tables internes

Régénérées sur l'état final par la recette contrôlée ci-dessus : `TABLE-CORRESPONDANCE.md` (l.5 et l.6 : sha256 de la
source et du brouillon), `TABLE-CORRESPONDANCE-EN.md`, `controle_public.sortie.txt`, `controle_en.sortie.txt`.

### L-5 — renvois Q-B et Q-C : gardés (décision 5), rien à faire.

### L-6 — PDF

- Outil : `publication-amendements/outils/md2pdf_pa.py` (`7ba84a6b…4652`, inchangé), lancé sous `python3 -I` par
  `outils/lancer_md2pdf.py` (Markdown 3.9 de `outils-pdf/lib` : 40 fichiers de RECORD égaux ; Chromium hors réseau,
  `--disable-background-networking`, `--proxy-server=127.0.0.1:9`, TMPDIR retiré par l'outil).
- Équivalence : l'anglais de base redonne le HTML du lot précédent à l'octet (`5f039799…3c67`) ; son PDF ne diffère de
  `aa3e5802…bfd7` que par 10 octets, tous dans les deux dates PDF (`zones_pdf.py`, sortie 0).
- **PDF final** : `sorties/pdf/Shogen-S2-pilot-measurements-DRAFT.pdf`, sha256
  `66ef2d80c1daf1dafe279909bb09553fd6e7c73e9a54c29a95f3f929278adf62`, **18 pages**, 877524 octets ; HTML `902c2c7e…6e0e`.
  Lecture par `pdftotext` : `Draft — not published` présent ; la section portée, l'ajout daté du 2026-10-16 18:11:04 et les
  en-têtes retouchés présents ; pied de page = sha256 de l'anglais final (`6db435db…dcc8dd`) ; `failed reading` 8, `outage` 3
  (inchangés).

### Contrôles rejoués de la phase 2 (`bash outils/rejouer_p2.sh` ; sorties dans `sorties/p2/`)

| contrôle | résultat |
|---|---|
| composition des dix diffs sur une copie de la base | égale à `final/` à l'octet ; chaque diff s'applique seul sur la base |
| `outils/verifier_p2.py` (lignes changées = lignes déclarées ; nombres des en-têtes) | CONFORME, sortie 0 |
| `presg5` (FR, EN, deux tables, état final) | 0 fragment, sortie 0 |
| R-13 sur les dix diffs | 0 |
| `controle_public` amendé, état final | CONFORME 7/7, sortie 0 |
| `controle_en` amendé, état final | CONFORME 11/11, sortie 0 |
| tests EN (état final) / tests de `controle_public` | 108 OK / 117 OK |
| `avant_acte.py --lecture-seule diff --fichier … --rapport RAPPORT-GENERATEUR.md`, dix diffs | sortie 0 chacun (`sorties/p2/avant_acte.*.sortie.txt`) |

### Écarts de la phase 2

- E-4 : premier tour des mutants de chaque outil avec un mutant mal formé (MQ1, ME5 : FATAL, non comptés) et un mutant
  équivalent (ME6) ; refaits, chiffres ci-dessus du dernier tour.
- E-5 : premier jet de `SourceEpinglee` sans fixture (erreur d'attribut, sortie 3) : corrigé avant l'étape rouge comptée.

### Limite restante (item à former)

- L-7 (inchangée) : relevé d'`ACTEURS-NOMMES.md` périmé (SHOGEN-PUBLICATION-ACTEURS-RELEVE-1) ; `controle_public.py` et ses
  tests restent hors dépôt (SHOGEN-PUBLICATION-OUTILS-PUBLIC-VERSES-1 ; la ligne 40 du glossaire est désormais à jour).

### Phrase de fermeture proposée (remplace celle du §7)

« SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1 : fermé le <date> (commits <…> ; G2 neuve <verdict> ; adjudication du 2026-10-16).
Les 49 lignes ajoutées à docs/11 par `6c04e91` sont portées en fin des deux versions publiques sous un ajout daté du
2026-10-16 18:11:04 UTC : français l.1082-1130 (retouches E-29 et E-30), anglais l.761-771, après le glossaire. En-têtes FR
l.7 et l.13, EN l.5 et l.7 : deux formules, dates 2026-10-15 et 2026-10-16, place du glossaire (E-31, E-32, A-10). Contrats
amendés : `controle_public` (ajout daté en tête de ligne, épingle de la source), conforme 7/7 ; `controle_en` (section
d'ajouts datés après le glossaire), conforme 11/11. Sorties et tables internes régénérées. PDF reconstruit hors réseau,
sha256 `66ef2d80…df62`, 18 pages, « Draft — not published ». Aucune valeur mesurée changée ; aucune ligne décalée. »

## Correction S-G4 (2026-10-16, demande du coordinateur, tête `816cad0`)

- **Cause** : la gate S-G4 lit les 15 locutions de `xtask/src/sg4.rs` ; `garanti` n'en est pas. La rangée E-30 portait en clair
  `guaranteed` dans sa colonne motif (`anglais held (« guaranteed » est une locution …)`) : c'est l'occurrence relevée.
- **Correction** : le motif de E-30 met le mot en code. Les cellules avant et après de E-30 sont inchangées (`garanti` n'est
  pas lu par S-G4) ; controle_public lit les cellules avant et après à l'octet, et pas le motif : il n'est pas modifié.
- **Contrôles** : émulation de S-G4 (`outils/sg4_emule.py`) sur la table, la table anglaise et les deux versions publiques :
  0 locution ; E-31, E-32 et la table anglaise : 0. controle_public CONFORME 7/7, controle_en CONFORME 11/11 (anglais de la
  tête) ; presg5 0 ; R-13 0 ; avant_acte `--lecture-seule diff` 0 sur chacun des quatre diffs.
- **Diffs corrigés** (`diffs/corriges-sg4/`, base `816cad0`, ordre SYNC-TABLE, SYNC-TABLE-EN, SYNC-SORTIE-PUBLIC,
  SYNC-SORTIE-EN ; chacun s'applique seul sur la tête, et en séquence) :
  - `SYNC-TABLE.diff` `075319e6bbe0c49487102a6091d2542bf135e753a297c085a26b83392a589694` (13 / 4) ;
  - `SYNC-TABLE-EN.diff` `2845be87e5134e164f446626544ca4a61c1137c7d8edbfe2493ca66ba44397e7` (3 / 2) ;
  - `SYNC-SORTIE-PUBLIC.diff` `6ce5b8f38672374510ce2d087bb4742de177a274854286e90158aa62e8e376d1` (20 / 19) ;
  - `SYNC-SORTIE-EN.diff` `05db924f411b7dc44cc8d93b75bc7d513d2280d8f2c84153a4ce90887fcc956a` (9 / 9).
