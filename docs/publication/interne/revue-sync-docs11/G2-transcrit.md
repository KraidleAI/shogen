# Relecture G2 neuve bilingue du lot SYNC-DOCS11 (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 20:36:18 UTC du fichier sync-docs11/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (185 occurrences). Texte ci-dessous avec 2 retouche(s) (E38) : le mot anglais cité comme locution de la gate S-G4 est mis entre guillemets français, sans autre changement ; sans autre retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve bilingue — lot SYNC-DOCS11 (SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort `high`, fiche `shogen-worker` ; réviseur distinct du générateur
  (je n'ai produit aucun des dix diffs ni des deux diffs de revue).
- **Rattachement (G0)** : brief `g2/BRIEF-G2.md` (orchestrateur, 2026-10-16 18:37:15 UTC), lu en entier ; item
  SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1, `docs/adr-0028/ANNEXE-B-items.md` l.1854 (ligne lue) ; décision de l'investisseur du
  2026-10-16 18:04:49 UTC, point 1 (lue dans `DECISIONS-INVESTISSEUR.md`).
- **Base** : `git rev-parse HEAD` = `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (tête attendue `fe9a72b`), relue à la fin ;
  `git status --short` vide sur les dix chemins du lot. Copie creuse `g2/copie/` par `git archive HEAD`.
- **Série relue** : dix diffs du générateur dans l'ordre de son rapport, sha256 de leur concaténation
  `a70315f23e29fc8816e9d21971c37d6f68d791d6e3f8681822fbbd022d0dc424` ; diffs de revue hors dépôt (concaténés)
  `9ecec744ecf11e52d8e728c95be7c1f093df81300f43e11efe9c060a9f08ea05`. `sha256sum -c ../SHA256SUMS` : 97 lignes, 97 OK.
- Heures : 2026-10-16, UTC, lues par `date -u` (journal `NOTES.md`).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée : C-1, C-2)

Le portage est fidèle : 43 lignes non vides retrouvées à l'octet, 4 vides, et les 2 retouches déclarées (E-29, E-30)
vérifiées. Aucune ligne existante ne change hors FR l.7, l.13 et EN l.5, l.7, et aucune valeur mesurée ne change. Le
filtrage tient ; les deux contrôles sont conformes et reproduits à l'octet. Deux corrections :

- **C-1 (traduction, version anglaise publique)** : `held` rend à la fois `détenu` (l.766, l.770) et `tenu` (l.769, deux
  fois) ; pour un niveau de test, `is not held` peut se lire `n'est pas détenu`. Le corps anglais rend `tient` par
  `holds` (l.516 `whereas the rule holds`, l.517 `the bound 0.02 holds under`). Texte exact proposé ci-dessous.
- **C-2 (contrat de `controle_public`, hors dépôt)** : la forme en tête admise le 2026-10-16 exclut du compte tout le corps
  du préfixe, et pas seulement la date de sa marque. Une valeur ajoutée dans ce corps passe (démonstration ci-dessous).
  Serrage : le corps qui suit la marque ne porte aucun nombre. E-29 n'en porte aucun, donc la sortie versée reste
  inchangée à l'octet. S'y ajoutent deux tests pour deux mutants survivants du code ajouté (MG2, MG4).

Les fichiers versés au dépôt ne changent que par C-1 (cinq diffs remplacés, une ligne chacun) ; C-2 ne touche que les
diffs de revue hors dépôt et ne change aucune sortie versée.

## C-1 — `held` / `hold` (EN l.769 ; table E-30)

Version anglaise publique, l.769 (unité `SHOGEN-R1-PLUGIN-1 (b)`), deux remplacements, rien d'autre :

| avant | après |
|---|---|
| `the nominal level is not held, and the correction` | `the nominal level does not hold, and the correction` |
| `its level would not be held; the distribution` | `its level would not hold; the distribution` |

Par suite, `docs/publication/interne/TABLE-CORRESPONDANCE.md` l.79 (rangée E-30), motif : `; anglais held (« guaranteed » est
une locution de la gate S-G4) ; aucun nombre |` devient `; anglais does not hold (« guaranteed » est une locution de la gate
S-G4) ; aucun nombre |`. Les deux sorties versées et la table anglaise sont régénérées par les commandes de la recette du
générateur. Seules les empreintes changent : traduction `36133b08a39cb63d4d4114261ada085b1b8750ae513d367a61bb1dd7068a3d0a`,
table `cbfac9fe94aa9e39abd3af3cf414e84ec42b0e7f15326daa434a19d582bd171f`.

Diffs byte-exacts, à substituer aux diffs du générateur de même nom (chacun n'en diffère que d'une ligne) :

| diff corrigé | sha256 |
|---|---|
| `diffs/corriges/SYNC-EN.diff` | `ba0604771ec5263d24880af823cfebeb5d96531061ffdc1430d13055ed6b1a2c` |
| `diffs/corriges/SYNC-TABLE.diff` | `8ec4ded1fe651b625aab70ff273fe330f47178da0875575ea71c6a356a917253` |
| `diffs/corriges/SYNC-TABLE-EN.diff` | `2845be87e5134e164f446626544ca4a61c1137c7d8edbfe2493ca66ba44397e7` |
| `diffs/corriges/SYNC-SORTIE-PUBLIC.diff` | `7938fe8fb0f9ba15bdb40ade317c5e7f3a4085863c6100fe39d32c7576e7b78f` |
| `diffs/corriges/SYNC-SORTIE-EN.diff` | `05db924f411b7dc44cc8d93b75bc7d513d2280d8f2c84153a4ce90887fcc956a` |

Delta de lecture (état final du générateur vers état corrigé, 8 lignes changées) : `diffs/C-1-delta.diff`
(`7f365f715826ac2bb678d59cbddcbc55ca4d563e5459dba1945166b96e18911b`). Série corrigée, dans le même ordre (cinq diffs
corrigés, cinq inchangés) : `e9fd1e26427811192538c8daf88aabc97164c79715e2c42babb1acb986ec6dee`.

Contrôles de la série corrigée (`outils/verifier_corriges.sh`, `preuves/verifier_corriges.sortie.txt`) :

- les dix diffs appliqués dans l'ordre sortent en 0, et chacun s'applique seul sur la base ;
- `controle_public` : CONFORME 7/7 avec l'outil du générateur comme avec l'outil C-2 ; sa sortie est égale à l'octet à la
  sortie versée corrigée ;
- `controle_en` : CONFORME 11/11 ; tests anglais : 108 OK ;
- presg5 : 0 fragment ; R-13 : 0 ;
- `avant_acte.py --lecture-seule diff` : sortie 0 sur les cinq diffs corrigés.

PDF reconstruit sur l'anglais corrigé : `pdf/corrige/Shogen-S2-pilot-measurements-DRAFT.pdf`, sha256
`1d645017d1fa3bd48984a837a5c33042c3a9d613cbc79a4320aae8c67bb1209a`, 18 pages. `Draft — not published` y est présent, et le
pied de page porte `36133b08a39cb63d4d4114261ada085b1b8750ae513d367a61bb1dd7068a3d0a`. Si C-1 est retenue, la phrase de
fermeture du générateur (empreinte `66ef2d80…df62`) est à mettre au courant.

## C-2 — corps du préfixe exclu du compte (`controle_public`, hors dépôt)

Démonstration (`demo-e29/`, `preuves/demo-e29-valeur.sortie.txt`) : sur l'état final, j'insère `seuil 42,7` dans le corps
du préfixe E-29, au brouillon et à la rangée de la table. L'outil du générateur (`92636b3b…aec`) sort `VERDICT : CONFORME —
sept contrôles sur sept (sortie 0)`. La limite L-2 du générateur ne demandait que l'admission de la date d'un ajout daté
placé en tête ; la forme livrée admet aussi tout nombre écrit après la marque. Le contrôle anglais, lui, tient :
`threshold 42.7` ajouté dans la section anglaise donne `VERDICT : NON CONFORME — 2. nombres (sortie 1)`
(`preuves/demo-en-valeur.sortie.txt`).

Correction (tests d'abord) :

- outil, dans la branche de la forme en tête de `ajouts_dates`, après le refus multi-ligne :
  `elif jetons(prefixe[RE_MARQUE_EN_TETE.match(apres).end():]):` puis le refus `nombre dans le corps de l'ajout daté en
  tête (seule la date de sa marque sort du compte)` ; la docstring du contrat du 2026-10-16 est mise au courant ;
- tests :
  - la fixture `PREFIXE` ne porte plus de nombre (`texte sans nombre.`) ;
  - `test_prefixe_dont_le_corps_porte_un_nombre` (attendu 1) ;
  - `test_prefixe_devant_une_ancre_longue` (attendu 0, tue MG2) ;
  - `test_autre_ligne_a_sha256_n_epingle_pas` (attendu 0, tue MG4) ;
  - `test_prefixe_sur_deux_lignes` : corps `suite.` sans chiffre, sinon MQ2 survit sous la garde C-2.
- Étape rouge : la suite corrigée sur l'outil du générateur donne 120 tests, 1 échec
  (`test_prefixe_dont_le_corps_porte_un_nombre`), sortie 1.
- Outil corrigé : 120 OK, sortie 0, aucune ligne `Exception ignored` ni `Warning`.
- Démonstration rejouée sur l'outil corrigé : `REFUS E-29 : nombre dans le corps de l'ajout daté en tête …`, NON CONFORME,
  sortie 1.
- État final : CONFORME 7/7, sortie identique à l'octet à la sortie versée.

| diff | rôle | sha256 |
|---|---|---|
| `diffs/revue-controle_public.C-2.diff` | remplace `revue-controle_public.diff` (origine `44265e7f…5be4` → `41ae98f781dcf0b03bfc1dd8cd5c246196cd4ee79a0a567d0839a89f7c9b8fd2`) | `4c02ad1f13a8cd4db750f84638c969c22667d7e6d336e59fb7d6468e085b964b` |
| `diffs/revue-test_controle_public.C-2.diff` | remplace `revue-test_controle_public.diff` (origine `dbf9a523…8f15` → `196482b9898589aef853e3389ace196a941b7fdf403de1816a70768dd64427ba`) | `83d8f89d20c160a6121d01f35d488f421cecd1797b875702ee3935a20cc8bb66` |
| `diffs/C-2-delta-controle_public.diff` | delta sur la copie du générateur (`92636b3b…aec`) | `3ad08b43858584de9883de355af86ec3843ec5c8aa3fd88f5770afb4c33d95f9` |
| `diffs/C-2-delta-test_controle_public.diff` | delta sur la copie du générateur (`b4dcae21…2c07`) | `99aa1f5e1be45f8f3a3e1679e7acc6a758a3f2ec55d406a5a8873f21c00b1630` |

Chaque diff est rejoué : l'origine plus le diff complet, comme la copie du générateur plus le delta, redonnent les fichiers
corrigés à l'octet.

## Checklist

| point | verdict | preuve |
|---|---|---|
| 1. Application, état final, lignes changées | **conforme** | `outils/appliquer.sh` : les dix diffs sortent en 0 dans l'ordre ; les neuf cibles sont égales à `../final/` ; chaque diff seul passe `git apply --check` (sortie 0) ; dernier octet saut de ligne, en-têtes `a/` `b/`. `outils/lignes_changees.py` : lignes de base changées `[7, 13]` en FR et `[5, 7]` en EN ; le reste de la base est préfixe ligne à ligne de l'état final (1081 → 1130 l., 760 → 771 l.). Dans les quatre lignes d'en-tête, seul `2026-10-16` est un nombre ajouté (contrôle 1 de `controle_public` : 0 inventé, 0 ajouté ; `controle_en` : nombres identiques par unité). |
| 2. Fidélité des 49 lignes | **conforme** | `outils/fidelite.py` (un `grep -F -x -n` par ligne) : 43 lignes trouvées à l'octet, chacune une seule fois, à l.N+10. Les 4 lignes vides sont à leur place. La l.1075 est le suffixe exact de FR l.1085 : seul le préfixe E-29 est ajouté. Dans la l.1096, seul `pas garanti,` devient `pas tenu,` (E-30). E-30 : voir ci-dessous. |
| 3. Traduction | **C-1** | Lecture bilingue de EN l.761-771 : sens, nombres, identifiants, renvois Q-B et Q-C et termes du glossaire respectés (lot, inféré, seuil, limitation, fenêtres sautées, bornes extérieures, déclencheur ; pièce = document, comme en l.9). Recompte indépendant (`outils/grep_bilingue.py`) : 113 suites de chiffres (48 distinctes) et 14 identifiants (8 distincts), FR = EN, 0 écart ; Q-B 2 / 2, Q-C 1 / 1, `[inféré]` 4 / `[inferred]` 4. Trois candidats examinés : `held` (C-1), `vanishing means` (O-2), `the document` pour la pièce de Croux et Dehon (O-3). `the publisher` pour l'éditeur évite bien le faux ami `editor`. |
| 4. Filtrage public | **conforme** | `outils/filtrage.py` : 0 mention des 28 alias d'acteurs (dont MONARK, Kraidle) dans FR l.1082-1130 et EN l.761-771. 0 motif retiré par E-01 à E-28 (ADR-0025, D.2, session, Drive, lettre de lecteur, VPS, `est mort`, `panne`, `validé`, identifiants de session ou d'agent, chemins locaux, `jsonl`, orchestrateur, sous-agent, PX-, M009, JOURNAL). Seuls restent Q-B, Q-C et `procurement`, gardés par la décision 5 de l'adjudication (L-5). Pièces nommées : `biblio/INDEX.md` et `scripts/post-s2/contenu.py`, chemins relatifs au dépôt (précédent G-14). Contrôle 2 de `controle_public` : 0 motif. |
| 5. Outils de contrôle | **C-2** | Copie de revue reconstruite : l'origine du lot d'amendements (`44265e7f…5be4`, `dbf9a523…8f15`) plus les diffs de revue donne `92636b3b…aec` et `b4dcae21…2c07`, égales aux copies du générateur. Sur l'état appliqué, `controle_public` est CONFORME 7/7, avec une sortie identique à l'octet à la versée. `controle_en` est CONFORME 11/11, avec une sortie identique hors le chemin de la table écrite (option `--table` dirigée vers `tmp/`) et une table anglaise identique. Tests : 117 OK et 108 OK. L'admission en tête est trop large (C-2). La section anglaise après le glossaire est serrée : alignée et soumise aux contrôles 1 à 9 ; la démonstration `threshold 42.7` est refusée. Mutants : tableau ci-dessous. |
| 6. PDF | **conforme (écart de dates expliqué)** | Rejoué hors réseau : `lancer_md2pdf.py` du générateur, `md2pdf_pa.py` `7ba84a6b…4652`, Chromium `--proxy-server=127.0.0.1:9`, TMPDIR retiré par l'outil. Markdown 3.9 : RECORD, 40 fichiers égaux, 1 absent hors lib (`../../bin/markdown_py`). HTML identique (`902c2c7e…6e0e`). PDF `4f26f007575e00ab3377361bea4fdf04a4982694cc5f38e83535a3f6d0710348` ≠ `66ef2d80…df62` : `zones_pdf.py` trouve 8 octets différents en 2 zones, toutes dans les dates PDF (`D:20261016183401` contre `D:20261016184958`), hors date 0, sortie 0. 18 pages ; `Draft — not published` : 1 occurrence. |
| 7. S-G5, R-13, avant_acte | **conforme** | presg5 sur les quatre fichiers de l'état : 0 fragment, sortie 0. R-13 : 0 sur les douze diffs. `avant_acte.py --lecture-seule diff --fichier … --rapport RAPPORT-GENERATEUR.md` : sortie 0 sur les dix diffs (`preuves/avant_acte.generateur.sortie.txt`). |
| 8. Écarts E-1 à E-5 | **conforme** | Aucun des cinq dossiers interdits nommés au brief n'est présent dans les huit copies (relevé `test -e` sur chemins explicites : 0). Tête du dépôt inchangée ; `git status` vide sur les dix chemins. E-1 (liste par motif `docs/publication/*.md` dans une copie) et E-3 (affichage par `tr`) restent sans effet sur les livrables. E-2 est recompté (49 lignes, `fidelite.py`). E-4 et E-5 : mutants refaits, chiffres du dernier tour reproduits ci-dessous. |

### E-30 (point 2) : le sens, le registre, la gate

- **Sens** : tenu. `n'est pas garanti` (rien n'assure le niveau) devient `n'est pas tenu` (le niveau n'est pas atteint),
  formule plus affirmative. Mais l'auteur l'affirme lui-même dans la même rangée, docs/11 l.1102 : `son niveau ne serait
  pas tenu`.
- **Doc 09** : ne l'exige pas à la lettre. Sa règle héritée (l.10-13) vise `guaranteed` comme qualificatif d'assurance ; une
  négation n'est pas une assurance, et sa table ne porte `garantit` qu'en affirmation (l.22, l.37, l.38).
- **S-G4** : n'exige rien en français. Sa liste ne porte que `prix garanti` (`xtask/src/sg4.rs` l.63), et docs/11, qui est
  dans son périmètre (`docs/**/*.md`, l.18), garde `pas garanti` à sa l.1096. En anglais, elle l'exige : `guaranteed`
  (l.93) serait refusé dans la version anglaise.
- **Ce qui l'exige en français** : l'extension lexicale `LOCUTIONS_09` de `controle_public` (resserrage, l.256 :
  `garanti`). Une exception motivée à la ligne exacte (`EXCEPTIONS`, l.267) aurait gardé l'octet source. Le choix E-30
  aligne le français sur l'anglais, qui doit changer de toute façon, et il est déclaré (table, en-tête l.7). Je le tiens
  pour acceptable : observation O-4, pas de correction.

## Mutants (`outils/mutants_g2.py` : groupe de processus neuf, borne 300 s, killpg des descendants, relevé ps de fin)

Chaque mutant se classe par la sortie du lanceur de la suite (`lancer_tests.py` : 0, 1, 3). Aucun job de `gates.yml` ne
lance ces suites (aucune ligne `publication` dans `.github/workflows/*.yml`) : le lanceur de la suite tient lieu de
commande du job.

| campagne | mutants | résultat |
|---|---|---|
| `controle_public`, outil et tests du générateur | MQ1-MQ10 rejoués (ceux du générateur) | 10 tués |
| idem | MG1 (site d'appel : ajouts datés cherchés dans la source), MG3 (date du préfixe remplacée), MG5 (`continue` retiré) | 3 tués |
| idem | MG2 (préfixe toujours retiré en fin), MG4 (épingle sur toute ligne `- … sha256`) | **2 vivants** → tests de C-2 |
| idem | MG6 (épingle exigée même absente) | FATAL (sortie 3 : toute fixture sans épingle devient fatale) ; mutant mal formé, non compté |
| `controle_public`, outil et tests corrigés (C-2) | MQ1-MQ10, MG1-MG5, MG7 (garde C-2 retirée) | 16 tués, 0 vivant ; MG6 FATAL, non compté |
| `controle_en`, état final | ME1-ME5, ME7 rejoués (ceux du générateur) | 6 tués |
| idem | MH1 (`AJOUTS_FIN_TITRE` non lu dans `separer`) | tué |
| idem | MH2 (titre de la section omis du texte du corps), MH3 (genre `titre` non exigé) | vivants, jugés équivalents (O-5) |

Relevé ps de fin : 0 groupe restant après chaque campagne. Mutants rejoués : 16 sur 16 (10 MQ, 6 ME). Mutants du
réviseur : 10 (MG1-MG7, MH1-MH3).

## Observations (non bloquantes, aucune correction demandée)

- **O-1** : FR l.1085 (EN l.764) dit `la section ci-dessous` / `the section below`, alors que le préfixe est placé sous le
  titre de la section (FR l.1083). La lecture reste claire (le texte qui suit) ; `cette section` serait plus exact, au prix
  d'une cascade (table, glossaire, sorties, PDF).
- **O-2** : EN l.768 `vanishing means` (moyennes nulles) : juste en mathématiques, moins courant que `zero means`, que le
  contrôle des nombres en lettres écarte à raison (constat 4 du générateur).
- **O-3** : EN l.768 `the document` pour la pièce de Croux et Dehon : conforme à l'usage du fichier (l.9) ; `the paper`
  serait plus idiomatique.
- **O-4** : E-30, voir ci-dessus.
- **O-5** : MH2 et MH3 sont équivalents. Le titre de la section est égal, par construction, à `AJOUTS_FIN_TITRE` (et aligné
  sur `TITRES`) ; une unité qui commence par `## ` est toujours un titre.
- **O-6** : le sha256 d'un PDF reconstruit change à chaque construction (dates PDF). Une phrase de fermeture qui cite le PDF
  le cite avec son HTML, qui est stable, ou avec la réserve des dates.

## Limites rendues comme items à former

- **L-G2-1** : la forme suffixe (contrat du 2026-10-15, décision 2) exclut elle aussi tout le corps d'un ajout daté (E-24 à
  E-26) ; le serrage C-2 ne porte que sur la forme en tête. Les corps versés portent des nombres : serrer la forme suffixe
  demande donc une adjudication, hors de ce lot. Proposition d'item : SHOGEN-PUBLICATION-AJOUTS-DATES-CORPS-1.
- **L-G2-2** : aucun job de CI ne lance les suites de `scripts/publication/en/tests/` ni celles de `controle_public`. Les
  mutants se classent donc par le lanceur de la suite, et non par une commande de `gates.yml`.
- **L-G2-3** : `controle_public.py` et ses tests restent hors dépôt (SHOGEN-PUBLICATION-OUTILS-PUBLIC-VERSES-1, inchangé) ;
  C-2 vit dans les diffs de revue jusqu'à leur versement.

## Écarts du réviseur

- **E-G2-1** : la commande `git archive` de la copie creuse portait un motif `docs/09-*.md`. C'est une liste par motif sur
  `docs/`, contraire à la consigne. Elle n'a résolu que `docs/09-vocabulaire.md`, et aucun emplacement interdit n'est
  touché.
- **E-G2-2** : un `git status --short -- docs scripts` nommait deux arbres entiers. Sa sortie était vide ; je l'ai refait
  sur les dix chemins du lot.
- **E-G2-3** : les diffs de test de C-2 avaient été dressés avant l'ajout de deux tests ; je les ai régénérés et rejoués
  avant la livraison.
- L'enregistrement du rôle G2 par `oracle_record.py` est sans objet : le lot n'est pas un dossier soumis au cp-2.

## Journal de provenance (G1 du réviseur)

Journal horodaté : `NOTES.md`.

- Sources [lu] en entier : `BRIEF-G2.md`, `revue-amendements/G2-transcrit.md`, `../BRIEF.md`, `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, les douze diffs,
  `git show 6c04e91 -- docs/11-mesures-pilotes.md`, `ACTEURS-NOMMES.md`, les sorties versées et régénérées.
- Sources [lu] en partie : `docs/09-vocabulaire.md` l.1-63 ; `xtask/src/sg4.rs` l.1-40 et 80-140 ; `controle_public.py`
  amendé ; `controle_en.py` (l.84-115, l.566-610, l.1015-1045) ; `TABLE-CORRESPONDANCE.md` l.10-79 ; glossaire anglais
  (EN l.641-760) ; `avant_acte.py` (l.1-90, l.990-1030) ; `md2pdf_pa.py` ; `lancer_md2pdf.py` ; `zones_pdf.py`
  (en-tête) ; `lancer_tests.py` ; rapport transcrit du lot d'amendements (l.268-285).
- Aucune source [2nd] : chaque chiffre de ce rapport est affiché par un outil dans `preuves/` ou au journal.
- Le précédent `docs/publication/interne/revue-amendements/G2-transcrit.md` (212 l.) est lu en entier, après une première
  rédaction de ce rapport. J'en reprends deux gestes : les tests sous Python 3.11.15, 3.12.3 et 3.13.14, avec
  `-X dev -W error` (public C-2 : 120 OK, anglais corrigé : 108 OK, 0 `Exception ignored`/`Warning` ; les deux contrôles
  sous `-X dev -W error` : CONFORMES, 0 `Warning` ; `preuves/tests-versions.sortie.txt`), et le constat qu'aucun job de
  `gates.yml` ne couvre `scripts/publication/en` (son O-4, ici L-G2-2).

Outils du réviseur (`outils/`, bibliothèque standard, 0 barre oblique inverse) : `appliquer.sh`, `lignes_changees.py`,
`fidelite.py`, `filtrage.py`, `grep_bilingue.py`, `mutants_g2.py`, `record.py`, `verifier_corriges.sh`. Empreintes :
`SHA256SUMS`.
