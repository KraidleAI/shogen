# Contre-contrôle de la phase 4 de DETTES-T15 (DT15-m ; R-M1, O-M1) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:29:19 UTC du fichier dettes15/g2/cc/RAPPORT-CC-M.md ; contrôle FM-1.1 des transcripts du générateur (phases 1 à 4), du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle de DT15-m (phase 4 du lot DETTES-T15), reprise par message

Rédaction : 2026-10-15, à partir de 21:30:42 UTC (`date -u`) ; reprise à 21:13:24 UTC.

## 0. Gate 0, rôle, cadre

- Modèle : **`claude-opus-5-5`** ; effort `max` demandé, non observable de l'intérieur. Contre-contrôleur de la passe ;
  je n'ai pas écrit DT15-m.
- Lus en entier : la section « Phase 4 » de `RAPPORT-GENERATEUR.md` (l.886 à 1035), `diffs/DT15-m.diff` (187 lignes,
  sha256 `7403df170530ae05b8a51f9b7b2c630832806ad97e9e0c1225103b17e203759d`, égal au message), `outils/m_generique.py`,
  l'ajout de 16:37:17 à `ADJUDICATION.md` (R-1 à R-8 adoptées ; ordre de la série de commit).
- Tout sur des copies (`git archive` avec exclusions, filtre à moi) ; aucune commande git en écriture, aucun `cargo
  xtask verify`, un processus lourd à la fois, réseau isolé (`outils/iso.sh`), `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
  posée.

## 1. Verdict

**CONFORME-AVEC-RÉSERVES (R-M1)**. DT15-m fait, à l'octet, ce que dit la phase 4, points (1) à (6). La réserve ne porte
pas sur DT15-m. Elle porte sur l'outil qui refait C-10 : à la tête `f3d26a5`, il refuse, parce qu'une ancre de
`gates.yml` a changé (R-M1, forme exacte). Une observation bloque encore le versement à cette tête : **O-M1**, une
incohérence du lot DETTES-T7 que les deux outils refusent à bon droit.

## 2. Les six points

État de départ, construit par moi :
- tête `9dbf692` (1448 membres, 0 écarté) ;
- C-10 refait par mon outil, qui est `g2/outils/c10_generique.py` avec R-5 puis R-8 (sorties redirigées), daté
  `2026-10-15 20:18:02`. Il est **égal à l'octet** à `phase4/C-10-9dbf692.diff` (`0ac8be64…`) ; sans date, l'outil
  refuse ;
- puis les 22 diffs de la série de commit (sommes de la G2 et des miennes conformes), dans l'ordre de l'adjudication.

`presg5.py`, le README et `gates.yml` de cet état égalent ceux de `etats/p4-avant`. DT15-m s'y applique (`--check`,
puis `git apply`).

1. **`presg5.py`** : `retirer_balises` et `scinder_crochets` sont égales à l'octet, source de leur arbre, à celles de
   DT15-i (`presg5/apres`, que j'avais retrouvé en appliquant DT15-i). Les 20 autres nœuds de premier niveau sont égaux
   à l'octet. La doc du module ne diffère que par la phrase ajoutée (`outils/verif_m.py`).
2. **`tests/test_presg5_lineaire.py`** : aucune occurrence de `__file__`. L'outil est trouvé par
   `importlib.util.find_spec`, à côté de `garde_commun.py` ; s'il manque, le test échoue, il n'est pas sauté. Il compte
   3 tests.
   - Ancien `presg5.py` (celui de la tête) : `Ran 3`, `FAILED (failures=2)` ; les deux tests de temps échouent
     d'assertion (`plus de 20 s pour 8000000 caractères`), le test des valeurs passe.
   - Nouveau : `Ran 3`, OK, en 0,786 s.
3. **Plancher** : le job `controle-unittest` passe de 116 à 119.
   - Ligne exacte du job (python3.12) : `Ran = 116`, conforme, sur l'état de départ ; `Ran = 119`, conforme, sur l'état
     final.
   - Matrice 3.10, 3.11, 3.12 et 3.13 en `-X dev -W error` : `Ran 119`, OK, 0 avertissement.
4. **README** : celui d'avant est un préfixe exact de celui d'après (436 → 443 lignes). L'ajout est en fin, daté
   `2026-10-15 21:00:52`, après le dernier (`20:18:02`) ; aucune ligne n'est décalée. `garde/lignes-citees.txt` liste
   ce fichier et n'y admet qu'un ajout en fin ; `gates.yml` et `presg5.py` n'y sont pas. Deux paires d'ajouts
   préexistants portent la même date (l.27 et 34, l.404 et 415) : sans effet sur DT15-m.
5. **`outils/m_generique.py`**, sur mon état de départ :
   - avec `2026-10-15 21:00:52`, il redonne `DT15-m.diff` à l'octet (`7403df17…`) ;
   - il refuse (`AssertionError`, aucun fichier écrit) avec `20:18:02` (date égale au dernier ajout), `20:18:01`,
     `11:48:38` et `2026-10-10 08:45:35`.
6. **Corpus** : copie de l'état final, plus les octets de `/home/user/shogen/biblio/` (INDEX égal, `91f7dab3…`). Le
   corpus est lu par les fonctions des deux `presg5.py` ; je n'imprime que des empreintes, des comptes et des durées
   (`outils/presg5_corpus_cc.py`).
   - Nouvelle lecture, corpus entier : 201 textes en 4,89 s. Leur liste d'empreintes est égale, dans l'ordre, à celle
     du générateur. Les sorties avant et après du générateur sont identiques (`d455794e…`).
   - L'ancienne lecture sur le corpus entier dépasse 300 s. Je l'ai donc rejouée sur un échantillon : tous les fichiers
     d'au plus 3 Mo (256 pris, 6 écartés). Un seul texte du corpus en sort, la page de plus de 3 Mo.
     - Textes : 200 sur l'échantillon, ancienne lecture en 51,51 s, nouvelle en 3,55 s ; listes d'empreintes égales une
       à une (`59f68434…`).
     - Sortie de l'outil sur les 35 documents de `phase4/fichiers-presg5.txt` : identique à l'octet (rc 0, une ligne
       `presg5 : 0 fragment(s) introuvable(s)`, stderr vide) ; 51 s avant, 4 s après.
   - Les « 991 s » du README sont la mesure du générateur ; je ne les ai pas rejouées (règle des 300 s).

Autres contrôles :
- DT15-m : +110 −26, aucune ligne ajoutée de plus de 120 caractères, aucun marqueur TODO, FIXME ou XXX.
- Quatre mutants à moi, jugés par la ligne exacte du job : fenêtres 299 et 31, chevron perdu, recopie du reste. Tous
  tués (valeurs, sortie dorée, test de temps) ; témoin `Ran 119`.

## 3. Têtes suivantes

- **`d48818f`** (DETTES-T7, nouveau vérificateur), lue à 21:23:58 :
  - C-10 (daté 21:26:04) et DT15-m (daté 21:26:26, `26d4d42a…`) refaits ;
  - tout s'applique ; ce DT15-m est égal à `DT15-m.diff`, hors date de l'ajout et tête nommée ;
  - `presg5.py` et le test neuf sont égaux à l'état final ;
  - ligne du job `Ran = 119`, conforme ; runner `152 ok` ; `runners-epingles`, `workflows-yaml` et `docs-sha256sums`
    conformes.
- **`f3d26a5`** (DT7-f), lue à 21:27:47 :
  - l'outil de C-10 (R-5 + R-8) **refuse** : DT7-f a écrit un commentaire entre celui du correctif DT5-24 et
    `name: controle-unittest`, et l'ancre de l'outil ne se trouve plus ;
  - corrigé par R-M1, il passe cette étape, puis **refuse** au garde du README (`AssertionError: ('39', 117)`) ;
  - `m_generique.py` refuse de même (`('39', 117)`) : voir O-M1.

## 4. Réserve et observation

| R-n | fichier (sha256, 16 chiffres) | +/− | objet | preuve |
|---|---|---|---|---|
| R-M1 | `propose/R-M1.diff` (`fdb5e993afb22423`), hors dépôt, après R-5 et R-8, pour `g2/outils/c10_generique.py` | +8 −5 | le commentaire de DT15-f est posé juste avant `name: controle-unittest` (ancre sur le nom du job, le commentaire de DT5-24 exigé avant lui), et non plus collé à celui de DT5-24 | sortie égale à celle de R-8 à `9dbf692` (`0ac8be64…`) et à `d48818f` ; R-5, R-8 puis R-M1 appliqués à l'outil de la G2 donnent l'outil éprouvé ; à `f3d26a5`, l'étape de `gates.yml` passe |

**O-M1 (DETTES-T7, bloquant à `f3d26a5`)** : l'ajout de DT7-f au README des contrôles, daté du 2026-10-15 21:17:22,
écrit « plancher du job `controle-unittest` 39 ». `gates.yml`, à la même tête, porte 117. Le garde des deux outils
(dernier plancher du README égal à celui de `gates.yml`) refuse donc C-10 comme DT15-m : c'est un échec fermé, et la
cause est un texte de DETTES-T7, qui n'a pas été recalé. Ce constat ne se corrige pas dans DT15 : c'est une correction
de DETTES-T7, à former (règle PAROXYSME).

J'ai simulé cette correction sur une copie seulement : la ligne de DT7-f dit 117. Alors :
- C-10, refait par R-M1, passe de 117 à 118 ;
- les 22 diffs et DT15-m (118 → 121) s'appliquent ;
- la ligne du job donne `Ran = 121`, conforme.

Sans cette correction, la série ne se verse qu'à une tête antérieure à DT7-f.

## 5. Écarts

- **E-M1** : j'ai listé, sans récursion, ma copie de `biblio/` (`os.listdir`) pour bâtir l'échantillon ; seuls des
  comptes sont imprimés. Le corpus est lu par les fonctions de l'outil relu ; je n'imprime que des empreintes, des
  comptes et des durées.
- **E-M2** : la simulation d'O-M1 touche une copie (`copies/sim-f3d26a5`), jamais l'arbre ; elle est nommée comme telle
  ici et dans les notes.

## 6. Journal de provenance (G1)

- [lu] la phase 4 du rapport du générateur ; `DT15-m.diff` ; `m_generique.py` ; `c10_p4.py` (égal à mon outil hors
  chemins de sortie) ; l'ajout de 16:37:17 à `ADJUDICATION.md` ; `presg5.py` de la tête en entier ; le job
  `controle-unittest` et `garde/lignes-citees.txt` aux têtes `9dbf692` et `f3d26a5` ; la fin du README à `f3d26a5`.
- [2nd] la durée de 990,86 s de l'ancienne lecture sur le corpus entier (mesure du générateur, non rejouée).
- **Journaux** (`g2/cc/journaux/`) : `m-job-*.txt`, `m-test-*.txt`, `m-matrice-*.txt`, `m-corpus-*.txt`,
  `m-echantillon-*.txt`, `m-textes-*.txt`, `m-cli-*`, `campagne-m.txt`, `py-Q*.txt`, `m-runner-t9.txt`,
  `m-job-sim-f3d26a5.txt`.
- **Outils** : `verif_m.py`, `presg5_corpus_cc.py`, `mutants_m_cc.py`, `c10_rm1.py`.
- **Sorties** : `phase4/` (DT15-m refait aux têtes, et pour la simulation) ; `corrections/C-10-*` (dont
  `C-10-rm1-*`).

## 7. Livrables

`RAPPORT-CC-M.md`, `propose/R-M1.diff`, `NOTES.md` (section de reprise), `SHA256SUMS` mis à jour.
