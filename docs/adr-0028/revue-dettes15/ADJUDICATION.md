# Adjudication de l'orchestrateur — lot DETTES-T15, phase 1 (2026-10-10 09:25:00 UTC, `date -u`)

Contrôles faits avant lecture du rapport :
- Gate 0 : 412 champs `model` du transcript du générateur, tous `claude-opus-5-5`.
- FM-1.1 : 0 avec le `fm11.py` versé et 0 avec celui de DT3-E (`resultats: 0, entrees: 0`).
- `SHA256SUMS` du dossier : conforme.
- Empreinte de la concaténation DT15-a à f recalculée : `cb06725a95b1e70b57315dfdfa3a683cf76dbff0b10a0a0b4ba42ee193986032`, égale à celle du rapport.

## Questions

- **Q-1 adoptée** : registre compagnon `docs/RENVOIS-LIGNES.tsv` (forme B), avec épinglage au commit (forme C) pour un texte sorti de l'arbre. Aucun texte validé n'est réécrit.
- **Q-2 adoptée** : 43 entrées retrouvées, 13 épinglées, 1 exclusion (« corpus doc 06 l.269 », hors dépôt). Le paquet scellé se lit à `8b14567`, et la constante `SCELLES` l'exige.
- **Q-3 adoptée, avec un motif ajouté**. Les renvois exacts ne sont pas portés au registre. Ce qui les protège :
  - la règle C-3 (pas de décalage dans un document cité par numéro de ligne ; ajouts datés en fin) ;
  - les 43 entrées à lignes actuelles, qui servent de fils-pièges ;
  - le contrôle mécanique des lignes citées du lot GARDE-FOUS-ORCH (`garde/lignes-citees.txt`), après sa G2. Cette liste devra couvrir les cibles du registre, et la G2 de GARDE-FOUS le jugera (Q-10 de son brief).
- **Q-4 adoptée** : commentaires ôtés en `html`, `htm` et `md` ; pas en `xml`.
- **Q-5 : la recommandation (former un item) n'est pas adoptée ; c'est l'autre voie, DT15-g dans ce lot**, par la règle « aucune dette ». DT15-g ôte du corpus le contenu des éléments `script` et `style`.
  - Extensions : celles de Q-4, sauf avis motivé du générateur.
  - Tests rouges sur DT15-f, au moins 8 mutants, corpus complet rejoué.
  - La limite L-6 se ferme dans le même lot (DT15-g ou DT15-h) : les commentaires factices (`<!…>` sans `--`, `<?…>`) sont ôtés jusqu'au premier `>`, sans la borne de 300 octets. C'est la règle de tokenisation déjà suivie pour les commentaires vrais ; mêmes exigences de tests, de mutants et de corpus.
- **Q-6 adoptée** : `docs/17:70` reste en borne (emplacement interdit).
  - Dans le dépôt réel, où la pièce existe, la plage est contrôlée et xtask doit rester GLOBAL VERT. La chaîne de commit le vérifie avant chaque commit.
- **Q-7 adoptée** : la G2 relit la table `BASES` et les 3 exceptions `LECTURES`, renvoi par renvoi, sur un échantillon qu'elle choisit, d'au moins 15 renvois. Elle relit aussi les 5 entrées déplacées de docs/17.

## Observation et limites

- **O-1** : le compte de B.96 (DETTES-T14 : « 75 décalés, 6 réécrits, 2 hors plage ») datait chaque renvoi par `git blame`. Il sera précisé par un ajout daté dans le bloc de DETTES-T15 au versement : 43 entrées retrouvées, 13 épinglées, 1 exclue, lues à la base que déclare chaque document. Le bloc B.96 n'est pas réécrit.
- **L-1 : limite juste**. Le contenu d'une entrée épinglée se lit dans l'historique git, qui n'est jamais réécrit (règle du projet). Une entrée vérifiée une fois reste donc vraie : il n'y a pas de dérive possible, seulement une erreur de saisie. La G2 recontrôle les 23 entrées épinglées par un outil à elle, qui sert de troisième voix.
- **L-2** : la complétude mécanique porte sur docs/17. Pour les autres documents, la protection est C-3 et le contrôle des lignes citées de GARDE-FOUS. La règle de procédure sera écrite au bloc daté.
- **L-3** et **L-4** : adoptées comme limites écrites. L-3 se juge par la relecture de Q-7.
- **L-5** : bornes listées, adoptée.
- **L-6** : fermée en phase 2 (voir Q-5).
- **L-7** : la G2 rejoue la preuve de FLOTTANT sous 3.10, 3.11, 3.12 et 3.13. Le job tourne sous le `python3` d'une image de runner épinglée. L-7 se ferme si les quatre rejeux donnent 0 écart.
- **L-8** : adoptée. La marge du test est d'un facteur d'environ 9 entre l'ancien coût et la borne, et d'environ 28 entre la borne et le nouveau coût.

## Écarts

- **E-1** : accepté. Le fichier est permis et FM-1.1 donne 0.
- **E-3** : deux processus lourds ont tourné ensemble (la règle en permet un), charge sous 4,5 ; rappelé pour la phase 2.
- **E-2** et **E-4** à **E-7** : acceptés.

## Suite

- Phase 2 : le générateur produit DT15-g (et DT15-h s'il les sépare) et met à jour son rapport et ses sommes.
- Puis une G2 neuve sur DT15-a à la fin de la série.

## Ajout daté du 2026-10-15 12:39:11 UTC (`date -u`) : adjudication de la phase 2

Contrôles : Gate 0, 718 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme ; empreinte a…h, j recalculée : `8f219939fef3d356…`, égale. DT15-g, DT15-h et DT15-j : adoptés (DT15-j corrige un défaut de DT15-g trouvé par le générateur lui-même ; la lettre i est prise par DT15-i, hors dépôt). DT15-i (`presg5.py` du scratchpad, coût linéaire, sorties identiques sur le corpus) : adopté, posé par l'orchestrateur après la G2 ; ferme SHOGEN-PRESG5-QUADRATIQUE-1 avant même sa formation (il n'est pas formé au versement de DETTES-T16 : la précision va au bloc de DETTES-T15).

**Q-8 et Q-9 : la recommandation (former un item) n'est pas adoptée ; règle « aucune dette », phase 3 dans ce lot.** Q-8 : une balise de plus de 300 octets gardée entière laisse le texte de ses attributs au corpus (sens dangereux : faux vert possible) ; le débalisage doit lire une balise jusqu'à son vrai `>` (règle de DT15-j, étendue à toute balise), sans borne de 300 octets ; tests rouges, mutants, corpus complet rejoué. Q-9 : la recherche du `>` doit être linéaire (indices, sans recopie), comme DT15-i ; test de temps borné rouge sur l'ancien code. Diffs DT15-k (Q-8) et DT15-l (Q-9), ou un seul si R-25 le permet. L-9 (SVG, MathML lus comme du HTML) : limite juste, écrite au bloc. L-10 : la G2 lit la spécification WHATWG (brief G2, point 2) ; ce qu'elle contredit devient C-n.

## Ajout daté du 2026-10-15 13:07:03 UTC (`date -u`) : adjudication de la phase 3

Contrôles : Gate 0, 835 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 ; `SHA256SUMS` conforme ; empreinte a…h, j, k recalculée `8949734c888d31f8…`, égale. DT15-k adopté : Q-8 et Q-9 fermées. L-11 et L-12 : limites justes, écrites au bloc (sens sûr : L-12 ôte en trop). Écarts E-13 à E-19 acceptés. Série close côté générateur : DT15-a à h, j, k (dépôt) et DT15-i (scratchpad). G2 neuve sur la série entière (brief `g2/BRIEF-G2.md`, dont la lecture de la spécification WHATWG pour L-10).

## Ajout daté du 2026-10-15 15:05:10 UTC (`date -u`) : adjudication de la G2 neuve (ACCEPTE-AVEC-CORRECTIONS, C-1 à C-10)

Contrôles : Gate 0, 905 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme (379 fichiers) ; page WHATWG détenue dans `g2/pieces/` (rangée d'INDEX C-1, à placer après la section DETTES-T16, compte 204 → 205).
- **C-1 à C-10 adoptées telles quelles.** C-10 remplace DT15-f (recalage du plancher `controle-unittest` et de l'ajout daté du README sur la tête du moment) ; la forme à retenir est celle refaite sur la tête de fin de la chaîne GARDE-FOUS (`outils/c10_generique.py`), au moment de la chaîne de commit.
- **C-4 amende Q-2** : les renvois du paquet scellé vers doc 10 recopiés d'ADR-0028 (PAQUET l.56, l.63 ; CP1 l.101) se lisent au commit où leur texte correspond (`ce63fed`), non à `8b14567` ; l'entrée PAQUET l.57 est ajoutée. Le texte du paquet n'est pas touché ; la constante `SCELLES` suit la forme de C-4. Adopté.
- **C-2** : `<?` ouvre une instruction de traitement (WHATWG 13.2.5.72 à 13.2.5.76 lus par la G2) ; code juste, doc et phrases corrigées. L-10 fermée (règles lues). L-7 fermée (matrice 3.10 à 3.13). L-13 neuve (ouvreur HTML écrit dans un extrait ou un bloc de code) : limite juste, écrite au bloc.
- **`scripts/controle/presg5.py` (versé par GF-2, outil par GF-2b)** garde la lecture quadratique que DT15-i corrige : règle « aucune dette », pas d'item : **phase 4** du générateur, DT15-m = port de DT15-i sur le fichier du dépôt tel qu'il sera à la fin de la chaîne GARDE-FOUS (C-10, C-18 et R-x le touchent), avec un test portable (sans `__file__` nu), rouge sur l'ancien code, mutants, matrice 3.10 à 3.13. La phase 4 démarre à la fin de la chaîne GARDE-FOUS. La phrase de fermeture de PRESG5-QUADRATIQUE-1 dira « dans le dépôt ».
- Écarts E-1 à E-6 admis.
- Suite : contre-contrôle neuf de la série a…h, j, k + C-2 à C-9 (+ C-10 recalé), brief `g2/cc/BRIEF-CC.md` ; DT15-m rejoint la série avant la chaîne.

## Ajout daté du 2026-10-15 16:37:17 UTC (`date -u`) : adjudication du contre-contrôle neuf (CONFORME-AVEC-RÉSERVES, R-1 à R-8)

Contrôles : Gate 0, 482 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme (366 fichiers).
- **R-1 à R-8 adoptées telles quelles.** R-3 (lecture triple de la page : balisage, texte brut partout, lecture de C-6 ; seul ce que les trois gardent reste ; jamais plus laxiste que la série ni que C-6 par construction ; 16 des 18 sondes fausses fermées, 11 tests rouges avant, 9 mutants tués) **remplace le choix de C-6** : sens sûr, décidé. R-4 (`frameset`) adopté ; la 18e sonde (`textarea` dans le `title` d'un SVG) est une limite écrite (L-14). R-8 : l'ajout daté du README de DT15-f porte le `date -u` du recalage, l'ancienne date restant dans la phrase : adopté (l'heure d'un ajout est celle de son écriture ; règle E14). R-5 et R-8 corrigent `c10_generique.py` (outil hors dépôt). R-6 et R-7 : textes, adoptés.
- **Ordre de la série de commit** : DT15-a à e, C-10 (recalé par l'outil R-5 + R-8 à la tête de la chaîne, avec le `date -u` du moment), g, h, j, k, puis C-2 à C-9, puis R-1 à R-4 et R-6 (R-7 au bloc daté), puis DT15-m (phase 4). C-1 (rangée d'INDEX de la page WHATWG) au versement, après la section DETTES-T16.
- **Clôture : CONFORME sans passe 3** après DT15-m (formes écrites et éprouvées par le contre-contrôleur, commises à l'octet ; précédents DT2-q à t, DB1-r à t, DT7-u à aa). DT15-m sera relu par le contre-contrôleur de cette passe (reprise par message) avant la chaîne.
- Mutants vivants M11 (sens sûr), N10, D6, D7 (équivalents), D2 et D9 (limites L-1, L-2) : admis. Écarts admis.

## Ajout daté du 2026-10-15 21:33:16 UTC (`date -u`) : adjudication du contre-contrôle de la phase 4 (DT15-m) — CONFORME-AVEC-RÉSERVES (R-M1)

Contrôles : Gate 0 du générateur de la phase 4 (972 champs `model`, tous `claude-opus-5-5`) et du contre-contrôleur (584, tous `claude-opus-5-5`) ; FM-1.1 = 0 (deux outils, les deux transcripts) ; SHA256SUMS conformes (229 ; 414). DT15-m conforme à l'octet sur les six points ; `m_generique.py` redonne le diff à l'octet (`7403df17…`).
- **R-M1 adoptée** (outil de C-10 ancré sur le nom du job, un commentaire d'un autre lot pouvant se glisser avant) : appliquée à la copie de l'outil que la chaîne lance (`outils/c10_p4m.py` = `c10_p4.py` + R-M1), sortie égale à R-8 aux têtes relues.
- **O-M1** : l'ajout de DT7-f au README des contrôles disait « plancher du job `controle-unittest` 39 » quand `gates.yml` porte 117 : défaut du recalage de l'orchestrateur dans DETTES-T7 (motif « plancher 39 » seul remplacé) ; corrigé par `recaler.py` pour les pas suivants et par un commit DT7-ab (texte recalé à 117) après la fin de la chaîne DT7 ; les deux outils de DETTES-T15 refusent tant que ce texte n'est pas corrigé (échec fermé).
- Ordre de la chaîne DT15 (23 commits) : a à e, C-10 recalé (c10_p4m, `date -u`), g, h, j, k, C-2 à C-7, C-9, R-1 à R-4, R-6, DT15-m recalé (m_generique, `date -u`). Plancher attendu 121 (117 de DT7 + 1 + 3). Clôture CONFORME sans passe 3. C-1 (rangée WHATWG de l'INDEX), R-7 et C-8 (phrases) au versement.

## Ajout daté du 2026-10-16 00:56:41 UTC (`date -u`) : arrêt de la chaîne au pas DT15-c (S-G9 ROUGE, 11 violations) et recalage du registre

Le registre commis par DT15-b (colonne `lignes` calculée à la tête `9dbf692`) visait 11 blocs déplacés depuis par DT7-g (`squelette.yml`), DT7-h (`temoignage_reel.rs`) et GARDE-FOUS/DT7-f (`gates.yml`) : S-G9 (c) les a refusés dès que DT15-c l'a activé ; arrêt avant commit, arbre remis propre. Recalage par l'orchestrateur (`outils/recaler_registre.py`, même règle que la colonne `lignes` de `registre_renvois.py` : position unique du bloc d'empreinte égale à la tête, `-` sinon) : 99 entrées inchangées, 11 déplacées, 0 perdue ; toutes les autres colonnes identiques. Pas DT15-b2 inséré avant DT15-c ; la série restante (c à R-6, C-10 recalé compris) vérifiée par `git apply --check` et appliquée pas à pas sur une copie creuse de la tête portant b2 : 20 sur 20. Règle E30/E31 appliquée.
