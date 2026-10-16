# Rapport du générateur des amendements (phases 1 et 2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:39:39 UTC du fichier publication-amendements/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur et du réviseur G2 (deux relectures) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche, à deux exceptions : le chemin du scratchpad est abrégé en `<scratchpad>` ; les fragments anglais que le générateur proposait pour l'en-tête du rapport public (lignes signalées par presg5 : 172, 255, 320 de cette transcription) sont passés des guillemets français au code, règle S-G5 (une citation anglaise entre « » doit être détenue au registre ; ce ne sont pas des citations), texte inchangé.

# Rapport du générateur G1 — lot PUBLICATION-S2-AMENDEMENTS (SHOGEN-PUBLICATION-S2-AMENDEMENTS-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (worker `shogen-worker`, générateur G1 ; réviseur G2 à nommer, distinct).
- **Rattachement (G0)** : annexe B d'ADR-0028, §B.98, item SHOGEN-PUBLICATION-S2-AMENDEMENTS-1 (`ANNEXE-B-items.md` l.1704) ;
  engagements envoyés à CoinGecko le 2026-10-10 (`docs/publication/envoi-preavis/reponses/COINGECKO-2026-10-10.md` §4, lu en entier) ;
  brief de l'orchestrateur du 2026-10-15 20:14:32 UTC. Échéance : avant la publication, au plus tard le 2026-10-25.
- **Base** : copie `/home/user/shogen` à `9dbf69279c2a8ce7959281108d1450f163a76670` à l'ouverture (20:15:51 UTC, `date -u`) ; la tête a
  avancé pendant le lot (chaîne de l'orchestrateur, lot DETTES-T7 : `d76f95e`, `fecd3c31c01a8643f6abcc05a3421d470ef88e40`, puis
  `0dd5fe5710d969130a3092b8ee6b03b0333050b5` à 20:57 UTC) sans toucher aux fichiers du lot (`git diff --stat` vide sur `docs/publication`,
  `scripts/publication`, `docs/11-mesures-pilotes.md`, `ANNEXE-B-items.md` ; sha256 des trois fichiers cibles égaux à la base). Les quatre
  diffs s'appliquent (`git apply --check`, sortie 0, sur des copies de la base et sur la copie éparse de `fecd3c3`).
- **Horodatage des ajouts datés** : `2026-10-15 20:37:28 UTC`, lu par `date -u` au moment de l'écriture (un essai à 20:37:15 avait échoué
  avant toute écriture, E-3).
- **Aucune écriture dans le dépôt, aucune opération git en écriture.** Tout est sous
  `<scratchpad>/publication-amendements/`.

## 1. Changements, ligne par ligne (avant → après)

Règle tenue : chaque amendement est une substitution de mot(s) dans la ligne ou un ajout daté écrit à la fin de la ligne de son
paragraphe ; aucun saut de ligne ajouté dans les deux rapports (760 et 1081 lignes avant et après) ; aucun bloc de code, aucune
étiquette scellée, aucune valeur ni aucun verdict ne change ; aucune citation « … » ne change (151 en anglais, 146 en français,
identiques et dans le même ordre).

### PA-a — rapport anglais, corps (`docs/publication/11-pilot-measurements-public-en.md`)

| l. | avant | après |
|---|---|---|
| 23 | `weekend windows, outage, staleness and out-of-envelope axes` | `weekend windows, failed-reading, staleness and out-of-envelope axes` (forme épithète à trait d'union, pour éviter la lecture « failed (… axes) ») |
| 62 | `if it is in outage (reading absent, status not ok or price absent), stale (carried…` | `if it has a failed reading (reading absent, status not ok or price absent), is stale (carried…` |
| 90 | `precedence outage > staleness > out-of-envelope` | `precedence failed reading > staleness > out-of-envelope` |
| 202 | glose `[*outage / stale / out-of-envelope / not evaluable*]` | `[*failed reading / stale / out-of-envelope / not evaluable*]` (étiquette `(panne / stale / horsE / nonÉv)` inchangée) |
| 244 | fin : `…they do not merge (ADR-0008, recalled at l.435786-435788).` | + ` *Addition dated 2026-10-15 20:37:28 UTC*: the edge binance → coingecko records only that Binance is one of the exchanges whose markets CoinGecko integrates (coingecko.com/en/exchanges/binance; field relation of the edge in s2-harness/shogen_s2/r2.py at the collection commit ed479c5); it implies neither that Binance is CoinGecko's only source nor that it is its main source, and it has no effect on any result.` (codes entre accents graves dans le fichier) |
| 253 | fin : `…which trigger (b) and do not partition.` | + ` *Addition dated 2026-10-15 20:37:28 UTC*: the edge binance → coingecko records only that Binance is one of the exchanges whose markets CoinGecko integrates; it implies neither a sole nor a main source, and it has no effect on any result (§4.1).` |
| 437 | fin : `…no pair dependence established. **Hors décision; does not change the verdict.**` | + ` *Addition dated 2026-10-15 20:37:28 UTC*: as the anomalies are almost all failed readings (§9.3 pt 2), a high φ between two feeds describes readings that the harness failed to obtain in the same windows, with a single observer (one collection host and one DNS resolver per probe record, §2.7); it does not establish a dependence between the providers. See also §5.2 (composition of K by panne_transport readings) and §11.1 (concentration of K in the starts whose ASN probe carries a resolve_failed: compatible with a common mode of the observer, without establishing it).` |
| 547 | `The counted anomalies are almost all outages:` | `The counted anomalies are almost all failed readings:` |

Inchangée : l.553 (« nothing shows an outage of Pyth », panne d'un fournisseur ; passage exigé par décision de l'investisseur).
Fondement de la note (ii) : arête `upstream` binance → coingecko de `s2-harness/shogen_s2/r2.py` à `ed479c5`, champ `relation`
« intégration (table des marchés spot, … — chiffre daté) », `doc_url` coingecko.com/en/exchanges/binance ; même `METHOD_EDGES` au commit
d'analyse `f35a70c` ; son seul effet dans le code est le booléen `basis_doc_triggered` de l'axe contenu (`compute_content`), et la
partition n'est jamais faite sur `basis:doc` seul (`compute_partition`, ADR-0008).

### PA-c — rapport anglais, glossaire final

| l. | avant | après |
|---|---|---|
| 672 | `(panne / stale / horsE / nonÉv)` → `outage / stale / out-of-envelope / not evaluable` | → `failed reading / stale / out-of-envelope / not evaluable` |
| 714 | `panne` → `outage` → `status panne_transport kept as printed` | → `failed reading` → `status panne_transport kept as printed; ordinary sense (outage of a provider, §9.3 pt 8): outage` |
| 715 | note `a feed is anomalous in a window if in outage, stale or out of envelope` | `a feed is anomalous in a window if it has a failed reading, is stale or out of envelope` |

La note de la l.714 dit le sens ordinaire du mot (l.553) : sans elle, le glossaire (« panne → failed reading ») contredirait la l.553.

### PA-b — version française publique (`docs/publication/11-mesures-pilotes-public.md`)

| l. | avant | après |
|---|---|---|
| 51 | `axes panne, staleness` | `axes lecture en échec, staleness` |
| 120 | `s'il est en panne (lecture absente, statut non ok` | `s'il a une lecture en échec (lecture absente, statut non ok` |
| 161 | `précédence panne >` | `précédence lecture en échec >` |
| 370 | fin : `(ADR-0008, rappelé l.435786-435788).` | + ` *Ajout daté du 2026-10-15 20:37:28 UTC* : l'arête binance → coingecko enregistre seulement que Binance est l'une des places dont CoinGecko intègre les marchés (coingecko.com/en/exchanges/binance ; champ relation de l'arête dans s2-harness/shogen_s2/r2.py au commit de collecte ed479c5) ; elle n'implique pas que Binance soit la seule source de CoinGecko ni sa source principale, et elle n'a d'effet sur aucun résultat.` |
| 393 | fin : `qui déclenchent (b) et ne partitionnent pas.` | + ` *Ajout daté du 2026-10-15 20:37:28 UTC* : l'arête binance → coingecko enregistre seulement que Binance est l'une des places dont CoinGecko intègre les marchés ; elle n'implique ni source unique ni source principale, et elle n'a d'effet sur aucun résultat (§4.1).` |
| 681 | fin : `de paire établie. **Hors décision ; ne change pas le verdict.**` | + ` *Ajout daté du 2026-10-15 20:37:28 UTC* : comme les écarts sont presque tous des lectures en échec (§9.3 pt 2), un φ élevé entre deux flux décrit des lectures que le harnais n'a pas obtenues dans les mêmes fenêtres, avec un seul observateur (un hôte de collecte et un résolveur DNS par relevé, §2.7) ; il n'établit pas une dépendance entre les fournisseurs. Voir aussi le §5.2 (composition de K par lectures panne_transport) et le §11.1 (concentration de K dans les démarrages dont la sonde ASN porte un resolve_failed : compatible avec un mode commun de l'observateur, sans l'établir).` |
| 883 | `presque tous des pannes :` | `presque tous des lectures en échec :` |

**Le mot « panne » en français : je propose de le remplacer dans le texte courant, pas dans les étiquettes.** Raisons :
- « panne » porte en français la connotation que CoinGecko reproche à « outage » (défaillance du service) ;
- B.98 annonce la mise en cohérence de la version française, « étiquette scellée « panne » inchangée » ;
- la classification suivie est celle de la traduction : sont gardés les passages que l'anglais garde en français (glossaire A). Les
  l.51, 120, 161 et 883 sont traduites, donc du texte courant.

Restent inchangés :
- les étiquettes et sorties scellées : en-tête du bloc 3 `(panne / stale / horsE / nonÉv)` (l.323), `panne_transport` (l.61, 450,
  455-457, 460, 463, 886), énoncé recopié du J14 principal « axes panne / staleness / hors-enveloppe » (l.576) ;
- la l.902 « rien ne montre une panne de Pyth » (sens fournisseur ; passage exigé).

Les quatre blocs des l.51, 120, 161 et 883 se détachent un à un si l'orchestrateur préfère garder « panne » en français :
- conséquences d'un retrait : l'empreinte épinglée par PA-d et le sha256 de la version française changent ;
- à refaire alors : `controle_en`, puis le PDF.

### PA-d — données du contrôle de la traduction (`scripts/publication/en/outils/glossaire_en.py`)

- l.7 : empreinte courte de la source traduite (`f5eddc6a…9d11`, amendement A-8 ; avant `c101998b…6561`).
- l.40 : titre de section « amendements A-7 et A-8 » (longueur de ligne conservée).
- l.42 : `SOURCE_SHA256` épinglé sur la version française amendée (`f5eddc6a157f45295f2e1498a382915b4c776e20ac12922bec5aa4a28d0a9d11`).
- l.186 : glose G-26 → `failed reading / stale / out-of-envelope / not evaluable`.
- l.450 et l.453 : termes « panne » et « écart » comme au glossaire final (l.714, 715).
- l.515-521 : note de l'amendement A-8, écrite en fin de fichier (aucune ligne décalée).

Sans PA-d, l'outil versé `controle_en.py` s'arrête en FATAL sur la version française amendée (épingle) ; avec l'épingle seule, il échoue
aux contrôles 4 et 11 (gloses et glossaire). Ce n'est pas un desserrage : l'outil est inchangé, ses données suivent le texte.

## 2. Contrôles rejoués (sorties dans `sorties/`)

| contrôle | entrée | résultat |
|---|---|---|
| `outils/verifier_pa.py` (spécification écrite à la main avant le script d'application) | base → base | NON CONFORME, 23 écarts, sortie 1 (étape rouge) |
| idem | base → finale | CONFORME, sortie 0 |
| mutants de `verifier_pa.py` (`outils/mutants_pa.py`, une mutation par cas) | 14 mutants | 14 tués, 0 vivant, 0 FATAL |
| `controle_en.py` versé (`b42777db…bb4c`, inchangé), glossaire d'origine (`4beaf064…d76c`) | paire de base | CONFORME 11/11 |
| idem | paire finale | FATAL (sortie 3) : source non épinglée (étape rouge) |
| idem, épingle seule mise à jour | paire finale | NON CONFORME (4. gloses ; 11. glossaire) ; contrôles 1-3 et 5-10 OK |
| idem, glossaire PA-d (`86d44bbb…3d83`) | paire finale | **CONFORME, onze contrôles sur onze** (sortie 0) ; nombres identiques par unité ; 0 motif interdit ; registre S-G4 et anglais OK |
| tests de `controle_en` (`lancer_tests.py`, 101 tests) avec le glossaire PA-d | — | OK, sortie 0 |
| table de correspondance anglaise régénérée (`sorties/TABLE-CORRESPONDANCE-EN.pa.md`) | — | seuls changent les sha256 et les comptes de nombres des sections 4.1 (84→88), 4.2 (35→38), 7.5 (51→58), « oui » partout ; numéros de titres inchangés |
| `controle_public.py` (`35ba9a6c…2067`, lot DOCS11-PUBLIC), source `docs/11` à `2db4f40` (`fcf93b87…53b7`) | brouillon de base | CONFORME 7/7 |
| idem, table d'origine | brouillon amendé | NON CONFORME : 1. nombres ; 5. sections 2.1, 4.1, 4.2, 7.5 et lexique non déclarées, rejeu ≠ |
| idem, table étendue E-21 à E-27 (`work/TABLE-CORRESPONDANCE.etendue.md`, pièce de travail) | brouillon amendé | NON CONFORME sur **1. nombres seulement** : les trois ajouts datés apportent des nombres absents de `docs/11` (date, heure, renvois de section, chemin `r2.py`) ; motifs interdits 0, registre OK, passages protégés et exigés OK, sections = déclarées, rejeu identique à l'octet, structure et citations OK |
| `outils/lignes_fixes_pa.py` (adaptation de `lignes_fixes.py`, outil voisin de `refs_decalees.py`) | base → finale | CONFORME : EN 760→760, FR 1081→1081, `glossaire_en.py` 514→521 (7 lignes en fin) ; aucune ligne non déclarée changée |
| `outils/refs_pa.py` sur 18 documents nommés (liste `work/liste-renvois.txt`) | — | 110 jetons « l.N » tombant sur une ligne réécrite ; voir ci-dessous |
| `outils/citations_fr_pa.py` (spans « … » de S-G5, même algorithme que `citations_francaises` de `sg5.rs`) | base → finale | identiques et dans le même ordre (EN 151, FR 146) : S-G5 voit les mêmes fragments dans ces deux fichiers |
| `enforcement/docs-sha256sums.py` (`67c1e3f2…db81`) sur la copie éparse | avant / après les diffs | conforme / conforme (46 SHA256SUMS, 344 lignes, 11 absentes admises, 4 fichiers non listés) |
| `scripts/controle/presg5.py` | deux rapports amendés | interrompu par ma borne de 300 s (sortie 124) : **sans résultat, non compté** ; remplacé par la preuve d'invariance des citations ci-dessus |
| `cargo --locked xtask gates` (CARGO_TARGET_DIR du lot, hors réseau) | copie éparse de base (HEAD `fecd3c3`, sans les dossiers interdits) | S-G1 à S-G8 VERT ; S-G9 ROUGE (1 violation : `docs/17-modele-de-menace.md:70` renvoie à un fichier de `docs/rapports/`, exclu de la copie) ; global ROUGE |
| `xtask gates`, même binaire | copie éparse amendée | verdicts et violations identiques à la base (diff vide) ; S-G5 : mêmes comptes (régime corpus incomplet, aucun fragment non contrôlé dans `docs/publication/11-*`) |
| `cargo --locked xtask verify` | copie éparse amendée | S-G1 à S-G8 VERT (S-G4 et S-G5 compris) ; S-G9 ROUGE, même artefact de copie ; `cargo fmt --check` VERT ; no_std VERT ; `cargo clippy -D warnings` VERT ; global ROUGE par S-G9 seul. Le vert global se constate sur l'arbre réel (chaîne de commit) |

**Renvois par numéro de ligne.** Aucun numéro ne se décale : le nombre de lignes est conservé et seules les lignes déclarées changent. Les
renvois qui visent une ligne réécrite pointent toujours le même paragraphe, amendé :
- `COINGECKO-2026-10-10.md` l.87 (rapport l.244, l.253) et l.89 (l.437) ;
- `ANNEXE-B-items.md` l.1704 (l.23, 62, 90, 202, 547, 672, 714, 715) ;
- `interne/ACTEURS-NOMMES.md` l.52-53 (brouillon français l.51-52 et l.120-122). La citation de la l.51-52 reste intacte ; la paraphrase
  de la l.53 dit encore « une panne » pour la définition de la l.120 (pièce interne, hors liste du brief, non touchée : voir L-4).

Les autres jetons relevés visent d'autres documents (code de collecte, cartographie, ADR, journaux).

**PDF.**
- Chaîne : la même que le dossier d'envoi (`scratchpad/outils-pdf/md2pdf.py`, `e8d8b479…33c5` ; Markdown 3.9 dont les 40 fichiers
  hachés de RECORD sont égaux ; Chromium 141.0.7390.37).
- Variante sans réseau (`outils/md2pdf_pa.py`, `7ba84a6b…4652`) : drapeaux ajoutés à Chromium, et TMPDIR retiré (E-2).
- Preuve d'équivalence : la base reconstruite redonne le HTML d'origine à l'octet (`97c22e9b…9f9a`). Son PDF ne diffère de `fd60b4e6…7c88`
  que par 16 octets, tous dans les deux dates PDF (`outils/zones_pdf.py`, sortie 0).
- PDF amendé : `sorties/pdf/Shogen-S2-pilot-measurements-DRAFT.pdf`, sha256 `fcea115a9af288440bcdf59b1840ca1538fe5b0d86bbf4b307159683f6569726`,
  17 pages, 851624 octets ; HTML `f49c5092…8d03`.
- Lecture par `pdftotext` : « outage » passe de 9 à 3 occurrences (l.553, et deux dans la note de la l.714) ; « failed reading » 8 ;
  « failed-reading » 1 ; les trois ajouts datés présents ; mention « Draft — not published » présente ; pied de page = sha256 de l'anglais
  amendé.
- Le versement du PDF reste à la décision de l'orchestrateur.

## 3. Écarts et expositions

- **E-1** (exposition, déclarée) : une recherche des lignes « | E-… » de `interne/TABLE-CORRESPONDANCE.md` (pièce interne, autorisée), tronquée
  à 80 caractères, a affiché des noms retirés du public : chemin à lettre de lecteur, nom de dépôt privé, identifiant court de session. De
  même, la lecture de `controle_public.sortie.txt` a affiché des libellés de motifs. Pour expliquer le S-G9 rouge de la copie éparse, les
  chemins entre accents graves de `docs/17-modele-de-menace.md` l.70 ont été affichés ; l'un est un fichier de `docs/rapports/`. Pour lui,
  seule son existence a été testée (`test -e`), sans ouverture. Aucun contenu d'une pièce D.2 n'a été ouvert ni affiché.
- **E-2** (outil) : Chromium meurt (SIGTRAP, sortie 133) quand TMPDIR pointe sous le dossier du lot. Le chemin fait 107 octets, à la borne
  des chemins de socket.
  - Un essai sans TMPDIR, avec les drapeaux d'origine, a laissé Chromium tenter des connexions HTTPS de fond : échec TLS (-202), aucune
    donnée reçue ni envoyée par le lot.
  - Les constructions suivantes passent par `md2pdf_pa.py` (`--disable-background-networking`, `--proxy-server=127.0.0.1:9`) : aucune
    erreur réseau dans la sortie de Chromium.
  - Écart à la consigne « TMPDIR sous ce dossier », pour Chromium seul.
- **E-3** (mon script) : premier lancement d'`appliquer_pa.py`, FATAL avant toute écriture (ancre des ajouts mal construite). Corrigé,
  puis horloge relue avant le second lancement.
- **E-4** (garde-fous) :
  - la copie des octets locaux de `biblio/` dans la copie éparse a été refusée par le classifieur du mode auto (exfiltration) ;
  - une suppression `rm` dans un sous-dossier de sortie a été refusée par la garde de sécurité ;
  - un `ps` a été refusé.
  Aucune n'a été contournée. Conséquence : S-G5 de xtask tourne sur les copies en régime « corpus incomplet » (notes, jamais de
  violation) ; l'invariance des citations le complète.
- **E-5** (mes notes) : trois empreintes courtes écrites de travers dans `NOTES.md` (suffixes) ont été corrigées après affichage par outil ;
  rien n'a été versé avec ces formes.

## 4. Limites, rendues comme items à former

- **L-1 — en-têtes.** L'en-tête anglais (l.7) et l'en-tête français (l.13) affirment `no number is changed or added` / « aucun nombre
  n'est changé ni ajouté ». Les ajouts datés portent pourtant une date, une heure, des renvois de section et un chemin.
  - Proposition, hors du mandat donc non faite : `no measured value is changed or added; dated additions are marked as such` et
    l'équivalent français.
  - Sinon : adjudication écrite que ces nombres ne sont pas des valeurs.
- **L-2 — contrat de `controle_public`.** Ce contrat (« aucun nombre ajouté » par rapport à `docs/11`) ne peut pas être conforme avec des
  ajouts datés. Trois voies :
  - (a) verser une table de correspondance étendue (E-21 à E-27) avec adjudication du contrôle 1 ;
  - (b) reporter les mêmes ajouts dans `docs/11` (rapport accepté : décision de l'orchestrateur) ;
  - (c) acter que la version française publique n'est plus une simple version filtrée de `docs/11`.
  Le contrôle n'a pas été desserré.
- **L-3 — `docs/11` a changé depuis la construction des versions publiques.** `docs/11` est à `10f368da…52c9`, la source des versions
  publiques à `fcf93b87…53b7`. Le commit `6c04e91` (DETTES-T14, 2026-10-10) y a ajouté 49 lignes datées en fin de document, absentes des
  deux versions publiques. Ce point est hors du périmètre du lot ; il reste à décider avant la publication.
- **L-4 — `interne/ACTEURS-NOMMES.md` l.53** paraphrase encore la définition avec « une panne ». C'est une pièce interne ; une mise en
  cohérence optionnelle, dans un lot à venir, est possible.
- **L-5 — résolveur des lectures.** « one DNS resolver per probe record » reprend les mots des §2.7 et §9.3 pt 5, qui parlent du relevé ASN.
  Les lectures de prix passent par le résolveur système de l'hôte (`urllib`, `sources.py` à `ed479c5` l.48-58), que le rapport ne
  décrit pas.
- **L-6 — sorties des contrôles.** Les sorties versées (`interne/controle_en.sortie.txt`, `TABLE-CORRESPONDANCE-EN.md`,
  `controle_public.sortie.txt`) décrivent l'état d'avant. Leurs régénérations sont dans `sorties/` ; leur versement revient à
  l'orchestrateur.

## 5. Phrase de fermeture proposée pour l'annexe B

« SHOGEN-PUBLICATION-S2-AMENDEMENTS-1 : fermé le <date> (commit `<…>`, G2 neuve <verdict>).
- (i) `outage` devient `failed reading` aux l.23, 62, 90, 202 et 547 du rapport anglais et au glossaire (l.672, 714, 715). Le sens
  ordinaire reste à la l.553 (Pyth) et dans la note de la l.714.
- (ii) Note datée près de l'amont déclaré `binance → coingecko` (l.244, l.253) : une place parmi celles dont CoinGecko intègre les marchés,
  ni source unique ni source principale, sans effet sur aucun résultat. Le bloc 6 recopié est inchangé.
- (iii) Phrase datée au §7.5 (l.437) : un φ élevé décrit des lectures manquées en même temps par le harnais, avec un seul observateur ; il
  n'établit pas de dépendance entre fournisseurs (renvois §2.7, §5.2, §11.1).
- Version française mise en cohérence : « panne » du texte courant devient « lecture en échec » aux l.51, 120, 161 et 883 ; ajouts datés
  aux l.370, 393 et 681 ; étiquettes scellées inchangées.
- Aucune ligne décalée, aucune valeur ni aucun verdict changé. Contrôle de la traduction conforme 11/11 (glossaire, amendement A-8). PDF
  reconstruit `<sha256>`. »

## 6. Journal de provenance (G1)

Le journal horodaté est `NOTES.md` (même dossier). En résumé :

**Sources [lu]** (sha256 recomptés) :
- brief (24 l.) ;
- `COINGECKO-2026-10-10.md` (`2f4669ad…3514`, en entier) ;
- `ANNEXE-B-items.md` §B.98 (l.1679-1706 ; fichier `677a8e51…e035`) ;
- rapport anglais en entier (`60f7dc7a…21d6`) ;
- version française aux sections touchées et voisines (`c101998b…6561`) ;
- `controle_en.py` en entier, `glossaire_en.py` (l.1-200, 355-514) ;
- `controle_public.py` (partiel), `construire_public.py` (en-tête) ;
- `refs_decalees.py` et `lignes_fixes.py` ;
- `r2.py` à `ed479c5` et `f35a70c` (arêtes, `compute_content`, `compute_partition`) ;
- `sources.py` à `ed479c5` (l.36-58, 378-402) ;
- `sg5.rs` (partiel), `docs-sha256sums.py` ;
- `JOURNAL.md` l.396-420 ;
- `md2pdf.py`, `req.txt`, `garde_faits.py` (règles R5, R6).

**[2nd]** : aucun chiffre de seconde main. Les comptes cités sont affichés par les outils dans ce journal.

## 7. Livrables

`diffs/PA-a.diff`, `diffs/PA-b.diff`, `diffs/PA-c.diff`, `diffs/PA-d.diff` (chacun ≤ 13 lignes ajoutées) ; `sorties/pdf/` (PDF et HTML) ;
`outils/` (scripts du lot) ; `sorties/` (sorties des contrôles) ; `NOTES.md` ; `SHA256SUMS`.

## Phase 2 (2026-10-15, après la G2 neuve ACCEPTE ; `ADJUDICATION.md`)

- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (même générateur).
- **Rattachement** : demande du coordinateur ; `ADJUDICATION.md` de l'orchestrateur (2026-10-15 21:22:39 UTC, sha256 `64be462a…24fd`,
  lu en entier), décisions 2 et 3 (L-1, L-2, L-4, L-6) et O-5.
- **Base** : état après PA-a, PA-c, PA-b, PA-d (adoptés à l'octet, non retouchés), appliqués sur des copies. Tête observée :
  `f3d26a534faacd2fe1e7d37eb18ddc91fadf2369`, puis `c724e5677a8b2ae1f1cc0f0d7763842e8e44276a` (lot DETTES-T7) ; fichiers cibles inchangés à la tête.
- **Horodatage** : `2026-10-15 21:33:46 UTC` (`date -u`), pour la note A-9 du glossaire. La date des ajouts datés reste `2026-10-15 20:37:28 UTC`.
- **Ordre d'application** : PA-a, PA-c, PA-b, PA-d, puis PA-e, PA-f, PA-g. `git apply` des sept diffs en séquence sur des copies de la tête : les
  huit fichiers touchés sont égaux à l'octet aux versions finales. Un `git apply --check` de toute la série en un seul appel refuse PA-f sur
  `glossaire_en.py` (il contrôle chaque diff sur l'état d'origine, que PA-d a déjà changé) ; un commit par diff, dans l'ordre, passe.

### Diffs de la phase 2

| diff | fichiers | lignes ajoutées / retirées | sha256 |
|---|---|---|---|
| `diffs/PA-e.diff` | rapport anglais l.7, version française l.13, `interne/ACTEURS-NOMMES.md` l.52 | 3 / 3 | `92ad54af…27a9` |
| `diffs/PA-f.diff` | `interne/TABLE-CORRESPONDANCE.md` (l.3, 6, 7 en place ; 13 lignes en fin), `glossaire_en.py` (l.7, 42 ; 4 lignes en fin) | 22 / 5 | `06e54f11…673e` |
| `diffs/PA-g.diff` | `interne/controle_en.sortie.txt`, `interne/TABLE-CORRESPONDANCE-EN.md`, `interne/controle_public.sortie.txt` (régénérées) | 22 / 21 | `3fb8a83c…a9e6` |

### Changements (avant → après)

- Rapport anglais l.7 : `…; no number is changed or added.` → `…; no number is changed or added, except the dates of the dated additions of 2026-10-15.`
- Version française l.13 : « … ; aucun nombre n'est changé ni ajouté. » → « … ; aucun nombre n'est changé ni ajouté, hors les dates des
  ajouts datés du 2026-10-15. »
- `ACTEURS-NOMMES.md` l.52 : « un écart est une panne, une staleness » → « un écart est une lecture en échec, une staleness ».
- `TABLE-CORRESPONDANCE.md` :
  - l.3 : portée « E-21 à E-28, écrites en fin de fichier, hors de ce script » ;
  - l.6 : empreinte du brouillon final (`5de6e716…08b6` ; avant `c101998b…6561`) ;
  - l.7 : le diff source → brouillon cité est l'état d'avant E-21 à E-28 ;
  - en fin : section « Retouches E-21 à E-28 », huit lignes au format lu par `controle_public.py`. E-21 à E-27 sont tirées des listes
    fermées de PA-b ; E-28 est l'en-tête l.13.
- `glossaire_en.py` : l.7 et l.42, épingle de la source française finale `5de6e716…08b6` ; note de l'amendement A-9 en fin de fichier.
- Sorties régénérées (PA-g), sur l'état final, avec des chemins relatifs :
  - `controle_en.sortie.txt` : CONFORME 11/11 ;
  - `TABLE-CORRESPONDANCE-EN.md` : changent les sections 1 (date de l'en-tête), 4.1, 4.2 et 7.5 ;
  - `controle_public.sortie.txt` : CONFORME 7/7. Sa source est `docs/11` à `2db4f40`, nommée `11-mesures-pilotes.2db4f40.md` dans la
    sortie, car `docs/11` à la tête en diffère (item SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1).

### Contrat de `controle_public` (L-2)

- **L'outil n'est pas versé au dépôt.** L'original est dans le scratchpad du lot DOCS11-PUBLIC (`s2bis/docs11pub/outils/controle_public.py`,
  `35ba9a6c…2067`). La copie modifiée est `outils-public/controle_public.py` (`44265e7f…5be4`). Son diff de revue,
  `diffs/revue-controle_public.diff` (`dfcf929f…b891`, 86 lignes ajoutées), n'est pas un diff du dépôt.
- **Seul le contrôle 1 change.** Les ajouts datés de la liste fermée `AJOUTS_DATES` (E-24, E-25, E-26) sortent du compte des nombres,
  à trois conditions, sinon le contrôle 1 échoue :
  - « après = avant + ` *Ajout daté du AAAA-MM-JJ hh:mm:ss UTC* : …` », sur une seule ligne ;
  - le suffixe se trouve une seule fois dans le brouillon ;
  - la retouche est déclarée dans la liste.
- Les retouches de `MENTIONS_DE_DATE` (E-28) ne peuvent ajouter que les jetons de la date de ces ajouts.
- Les contrôles 2 à 7 ne changent pas ; le rejeu porte sur les 28 retouches.
- **Tests d'abord** : 12 cas ajoutés (`tests-public/test_controle_public.py`, `0696e698…15f4` ; diff de revue `bd21207f…d46d`).
  - Outil d'origine : 99 tests, 4 échecs (sortie 1). Pour mémoire, la suite d'origine passe : 87 OK.
  - Outil modifié : 99 OK (sortie 0).
  - Mutants du code ajouté (`outils/mutants_public_pa.py`) : 7, tués 7.
- **Sur l'état final** : CONFORME 7/7. Les comptes de nombres sont ceux de la sortie versée du lot DOCS11-PUBLIC (0 inventé, 0 ajouté,
  11 retirés), une fois les ajouts datés et la mention exclus.

### Contrôles de la phase 2

- `verifier_pa.py` étendu (`--phase2`, `24245293…cdd3` ; copie d'origine `verifier_pa.v1.py`, `20995085…aed8`) :
  - rouge sur l'état d'avant la phase 2 (10 écarts, sortie 1), vert sur l'état final ;
  - mode phase 1 inchangé : CONFORME, et les mutants de la phase 1 rejoués sont tués 14 sur 14 ;
  - mutants de la phase 2 (`outils/mutants_pa2.py`) : 12 tués sur 12.
- `controle_en` : CONFORME 11/11 (glossaire `d909935c…328f`).
- `outils/lignes_fixes_pa2.py` (tête du dépôt → copie munie des sept diffs) : CONFORME. Aucune ligne non déclarée ne change :
  - rapport anglais 760→760, version française 1081→1081, `ACTEURS-NOMMES.md` 104→104 ;
  - `TABLE-CORRESPONDANCE.md` 59→72 (13 lignes en fin), `glossaire_en.py` 514→525 (11 lignes en fin) ;
  - sorties régénérées, hors verdict : `controle_public.sortie.txt` gagne une ligne, celle du contrat amendé (l.10).
- **Renvois par numéro.** Dans les 18 documents nommés, aucun renvoi ne vise les pièces de la phase 2, sauf `docs/G2-lot-DOCS11-EN.md`
  l.67 (`glossaire_en.py` l.37 : historique, ligne inchangée). Les renvois vers le rapport anglais l.7 sont dans les comptes rendus
  historiques des lots DOCS11 et visent le même paragraphe, amendé en place. Aucun renvoi ne vise la version française l.13.
- `refs_decalees.py` d'origine (`c15a0ace…7a56`) rejoué, copie de la tête → copie amendée, liste des 18 documents : 56 renvois relevés,
  0 décalé.
- `docs-sha256sums` : conforme avant et après (46 SHA256SUMS, 344 lignes).
- **Citations « … ».** Inchangées et dans le même ordre : rapport anglais 151, version française 146, `ACTEURS-NOMMES.md` 25. Dans la
  table : 23 inchangées et 8 nouvelles, toutes françaises ; aucune n'a l'allure anglaise, S-G5 ne les contrôle pas.
- **Gates lexicales** (`xtask gates` du binaire du lot ; ni cargo ni verify) : verdicts identiques entre la copie de la tête et la copie
  amendée (8 vertes ; S-G9 rouge, même artefact de copie éparse).

### PDF (variante hors réseau seulement)

- `sorties/pdf-p2/Shogen-S2-pilot-measurements-DRAFT.pdf`, sha256 `aa3e580225c5de10fbbc688ba0904561cd01c4cfc7f0a06b118bfdcb43e2bfd7`,
  17 pages, 851608 octets ; HTML `5f039799…3c67`.
- Pied de page = sha256 de l'anglais final (`34d5b233…c10d`).
- Lecture par `pdftotext` :
  - la clause `except the dates of the dated additions of 2026-10-15` est présente ;
  - outage 3, failed reading 8, trois ajouts datés, mention Draft présente.
- Versement et envoi : actes de l'investisseur (adjudication, décision 7).

### Écarts de la phase 2

- **E-6** (exposition, déclarée) : la sortie de `refs_pa2.py` a réaffiché en contexte la ligne E-06 de la table interne (chemin à lettre de
  lecteur, nom de dossier de campagne). Ce sont des noms seuls ; aucun contenu D.2 n'a été affiché.
- **E-7** (SHOGEN-HARNAIS-ECHAPPEMENTS-1) :
  - une recherche par `grep` portait des barres obliques inverses tapées ; elle a été refaite par un script sans barre, même résultat
    (1 renvoi) ;
  - une chaîne Python d'un heredoc portait un saut de ligne échappé ; le fichier écrit ne contient aucune barre (contrôle `grep -F` sur
    l'octet).
- **E-8** (consigne « aucune liste récursive sur le scratchpad ») : pour dresser `SHA256SUMS`, un `find` a listé `work/p2/` de ce dossier,
  sous-arbre qui ne contient que des fichiers écrits par ce lot. La liste des sommes est écrite en chemins explicites.

### Limites de la phase 2 (items à former)

- **L-7 — relevé de `ACTEURS-NOMMES.md`.** Le §1 (relevé mécanique) ne suit plus le brouillon. `acteurs_nommes.py`, sur le brouillon final,
  donne Binance 32 mentions (26 avant) et CoinGecko 24 (18 avant), avec la ligne 370 en plus. La l.7 vise encore l'empreinte `c101998b…6561`.
  C'est hors du mandat de la phase 2 (L-4 = l.52 seule).
- **L-8 — outils non versés.** `controle_public.py`, `construire_public.py` et leurs tests (lot DOCS11-PUBLIC) ne sont pas versés au dépôt.
  Le contrat amendé vit dans `outils-public/` de ce dossier. Leur versement dépasse 200 lignes : il demande un lot à part.
- **L-9 — ordre des commits.** Entre les commits PA-e et PA-f, `controle_en` sort en FATAL (épingle) : il faut les commiter à la suite.
- **L-10 — en-tête de la table.** La l.3 dit que la table est générée par `construire_public.py` ; c'est vrai de E-01 à E-20, pas de E-21
  à E-28. La l.3 le dit désormais.

### Phrase de fermeture proposée (annexe B ; remplace celle du §5)

« SHOGEN-PUBLICATION-S2-AMENDEMENTS-1 : fermé le <date> (commits <…> ; G2 neuve ACCEPTE ; adjudication du 2026-10-15 21:22:39 UTC).
- (i) `outage` devient `failed reading` aux l.23, 62, 90, 202 et 547 du rapport anglais et au glossaire (l.672, 714, 715). Le sens
  ordinaire reste à la l.553 (Pyth) et dans la note de la l.714.
- (ii) Note datée près de l'amont déclaré `binance → coingecko` (l.244, l.253) ; le bloc 6 recopié est inchangé.
- (iii) Phrase datée au §7.5 (l.437) : un φ élevé décrit des lectures manquées en même temps par le harnais, avec un seul observateur ; il
  n'établit pas de dépendance entre fournisseurs.
- Version française mise en cohérence : « lecture en échec » aux l.51, 120, 161 et 883 ; ajouts datés aux l.370, 393 et 681 ; étiquettes
  scellées inchangées.
- En-têtes (anglais l.7, français l.13) : les dates des ajouts datés du 2026-10-15 sont les seuls nombres ajoutés. `ACTEURS-NOMMES.md`
  l.52 mise en cohérence.
- Contrôle de la traduction conforme 11/11 (amendement A-8 du glossaire, puis A-9 pour l'épingle de la phase 2).
- Brouillon public conforme 7/7 au contrat amendé de `controle_public` : ajouts datés exclus du compte des nombres, table E-21 à E-28
  versée. Sorties de contrôle régénérées.
- Aucune ligne décalée, aucune valeur ni aucun verdict changé. PDF reconstruit `<sha256>`. »

### Livrables de la phase 2

- `diffs/PA-e.diff`, `diffs/PA-f.diff`, `diffs/PA-g.diff` (chacun ≤ 22 lignes ajoutées) ; `diffs/revue-controle_public.diff` et
  `diffs/revue-test_controle_public.diff` (revue de l'outil non versé, hors dépôt).
- `outils-public/` et `tests-public/` (outil modifié et tests).
- `sorties/pdf-p2/` (PDF et HTML) ; `sorties/p2-*` (sorties des contrôles) ; `work/p2/final/` (fichiers finaux) ; `SHA256SUMS` régénéré.
