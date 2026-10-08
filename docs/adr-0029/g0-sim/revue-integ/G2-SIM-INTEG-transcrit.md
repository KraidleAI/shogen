# Relecture G2 neuve — SIM-BIS, intégration des sorties de PLAN-S2BIS-2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 18:31:28 UTC du rapport rendu par l'agent a059fa5f14a203e0a (workflow wf_fdc8272f-e05) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : modèle `claude-opus-5-5`** (réviseur G2 neuf, effort max ; je n'ai écrit aucun des diffs relus). Relecture du 2026-10-08, de 17:41 à 18:31 UTC.

# Relecture G2 de SIM-INTEG (SB-15A à SB-15F) : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-4)

Le code de production tient à la lettre les points (1), (3), (7) et (8) de l'ajout daté. Les corrections portent sur les tests seulement : six de mes mutants non équivalents survivent, et une docstring renvoie à la mauvaise question. Aucune valeur et aucune ligne de code de production ne sont à changer.

## Point à trancher d'abord : la base a bougé pendant la relecture

Ce n'est pas de mon fait, et je n'ai rien avancé.
- **Nouvelle tête :** la HEAD du dépôt est passée de b46672b à **f139242** (COLLECTE-BIS OUT-2g), 7 commits plus loin ; b46672b en est l'ancêtre.
- **Fichiers indexés par un autre acteur, non commis :**
  - `enforcement/tests/run-fixtures-verdict-suite-s2.py`
  - `enforcement/verdict-suite-s2.py`
  - `s2-harness/tests/test_oracle_record.py`
  - `s2-harness/tools/oracle_record.py`
- **Contrôle sur f139242 :** `scripts/sim-bis` et `gates.yml` y sont inchangés. Les six diffs s'appliquent (6/6), le runner donne 123 ok et le job sim-bis 189 conforme.

## Corrections

| id | où | preuve | remède |
|---|---|---|---|
| C-1 | `scripts/sim-bis/calib_fiv.py:316` (`min(d1, key=_rang)`) ; tests `tests/test_calib_fiv.py:530` et `:546`, sur une grille réduite où tous les points ont τ_D = 60 | MR-03, MR-04 et MR-05 survivent : pour C1, départage par τ_D avant κ, par φ avant τ_D, ou au plus grand φ | un test de C1 sur la grille scellée, Q₁ nul aux deux points, le premier doit gagner : (1/100, 5, 4320) contre (1/100, 50, 60) ; (1/10, 5, 60) contre (1/100, 5, 240) ; (1/100, 20, 240) contre (1/20, 20, 240) |
| C-2 | `calib_fiv.py:248` (hôtes de `q1`) et `:276` (compte de `bord`) ; fixtures `tests/test_calib_fiv.py:400` (`UNITES`) et `:597` (`modele_bord`) | MR-06 et MR-26 survivent : le dernier hôte du format est ignoré. Sur les données versées, c'est okx | un test de `q1` à dix hôtes où seul le dernier s'écarte (Q₁ = 16·(ln 2)²) ; un cas de bord dont les six hôtes négatifs sont les six derniers |
| C-3 | `calib_fiv.py:318` ; `tests/test_calib_fiv.py:662`, où le bord est toujours vrai par τ_D = 60 et où le compte d'hôtes n'est pas affirmé | MR-10 survit : il garde l'étiquette C1 avec les moyennes de C2. Le M-15F-14 du générateur changeait l'étiquette et les moyennes ensemble | un test de `selection` sur la grille scellée : C1 = (1/50, 10, 240), C2 ailleurs, six hôtes négatifs à C1 ; affirmer `hotes = 6`, `extremes = []`, `au_bord` vrai |
| C-4 | `tests/test_calib_fiv.py:640` : « pas de vérité vide : Q-SI-2 » | le rapport du générateur (§7) numérote la vacuité Q-SI-1 | écrire Q-SI-1 pour la vacuité et Q-SI-2 pour l'hôte à F_u indéfini |

Les remèdes sont faisables : mes trois tests (`g2/outils/test_revue_g2.py`) portent la suite à 192 tests, conforme, témoins verts, et tuent MR-03, -04, -05, -06, -10 et -26. Il faudra relever le plancher et refaire les campagnes.

## Points du contrat (état final)

| point | réalisation | tests qui le figent | verdict |
|---|---|---|---|
| (1) C1 | `calibration.py:22`, `:66`, `:80`, `:136` (section [FIV_u(ℓ)] seule), `:166` ; `calib_fiv.py:180-181`, `:184`, `:218`, `:240` `q1`, `:258`, `:292`, `:316` | `test_calibration.py:143`, `:164` ; `test_calib_fiv.py:513`, `:530`, `:546`, `:557` | tenu, avec les lacunes de test C-1 et C-2 |
| (3) calendrier d'E1 | `parametres.json:8-11` ; `commun.py:167` ; `calib_fiv.py:109`, `:148`, `:168-181` | `test_commun.py:229`, `:248` ; `test_calib_fiv.py:147`, `:279`, `:294`, `:321`, `:344`, `:358` ; `test_oracle_r1.py:132` | tenu |
| (7) retrait de `e1.ell_c1` | `parametres.json:93` ; `commun.py:95` ; refus `E1/ell` supprimé | `test_calib_fiv.py:416` | tenu ; la clé ne reste que dans des textes |
| (8) bord | `parametres.json:94` ; `commun.py:96` ; `calib_fiv.py:264`, `:282`, `:318` | `test_calib_fiv.py:609` à `:662` | tenu, avec les lacunes C-2 et C-3 ; « extrême » lu comme la plus grande valeur de chaque grille, conforme à la parenthèse du G0 |

## Ce que j'ai vérifié

- **Entrée :**
  - `SHA256SUMS` du générateur : 274/274 OK.
  - Diffs : préfixes égaux au rapport (A 3c2c8f77…, B 8b70e5b7…, C 91cb1953…, D c4e9676c…, E 11bc8970…, F 0949c81d…).
  - Application sur b46672b : 6/6 ; résultat égal aux étapes du générateur.
  - Entrées versées contrôlées, préfixes égaux au JOURNAL l.478.
- **Mon estimateur**, écrit avant toute lecture du code du lot, sur 13 jeux de fixtures à moi :
  - le lot donne le même C1, le même Q₁ (écart au plus 8·10⁻⁴⁷, dû à l'ordre de sommation) et le même constat de bord ;
  - jeux couverts : égalités départagées par κ, par τ_D, par φ, puis à trois points ; F_u indéfini (K = 0, K = n) ; point écarté ; gardes [60] puis aucune ; six puis cinq hôtes sur dix exactement (OUI, puis NON) ; bord par chaque coordonnée ; refus `E1/indefini` (aucun Q₁ défini, aucun couple retenu) ;
  - sur le fichier réel, 340/340 couples (F, garde) sont égaux.
  - Seul écart, voulu : un hôte du format absent du fichier fait refuser le lot en `CALIB/forme` (lecture du format, précision B.77), alors que mon estimateur l'ignore.
- **Masque :**
  - Mon oracle donne 46 468 positions, 386 lacunes, 24 585 en calme et 11 397 en stress, empreinte 670dc46e…, égale à celle du lot caractère pour caractère.
  - La génération porte bien sur la portée hors D5.
  - Le masque s'applique après la génération, vérifié sur deux réplications réelles : états D*(u) indépendants du masque, I_t et D*(u) rendus égaux à la génération restreinte au masque.
  - Les 680 FIV des séries D*(u) masquées sont égaux à ceux de r1 extrait de f35a70c.
  - Seul E1 est touché.
- **Mutants à moi**, classés par la commande du job, borne 300 s :
  - 26 mutants : 19 tués, 7 vivants, aucun FATAL.
  - MR-18 est équivalent sur toute entrée cohérente : sur 819 cas, σ̂²_bloc est positif dès que 0 < K < n.
- **Rouges du générateur rejoués** avec ses ébauches : SB-15E 4 FAIL / 0 ERROR, SB-15F 5 FAIL / 0 ERROR.
- **Matrice stricte** (`-X dev -W error`, `PYTHONHASHSEED` 1 et 4242), Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14 : 8/8 verts, Ran 189, aucune ligne « Exception ignored » ni « Warning ».
- **Jobs sim-bis à chaque étape :** 172, 174, 177, 179, 181, 183, 189, tous conformes ; planchers exacts.
- **Portes sur l'état final :**

| porte | résultat |
|---|---|
| runner | 97 ok |
| s2bis | 255 conforme |
| s2-harness | 407 conforme (deux sauts nommant la variable) |
| sim-bis | 189 conforme |
| hooks / model-pinning / secrets | 54 / 95 / 147 ok |
| lint R-1 | OK |
| R-13 | 0 constat |
| `gate-secrets --tree` | OK |
| `cargo --locked xtask verify` | égal à la base témoin : S-G1 à S-G8, fmt, no_std et clippy verts ; S-G9 rouge, 1 violation connue (`docs/17-modele-de-menace.md:70`) |

- **Forme :**
  - Code ajouté par diff : 66, 152, 68, 144, 157 et 120 lignes, tous au plus 200.
  - Octets 92 : 0 dans les diffs.
  - Imports ajoutés : bibliothèque standard seule.
  - Python : 0 ligne de plus de 120 caractères.
  - Observation non bloquante : la ligne 9 du README est une nouvelle ligne de prose de 160 caractères, que l'écart E-7 du générateur ne couvre pas.

## Avis sur les questions Q-SI et les items

- **Q-SI-1 à Q-SI-6 : à adopter.**
  - Q-SI-1, Q-SI-2 : sans effet sur les données (recompté : ℓ retenus de 60 à 720 en calme, de 60 à 360 en stress ; 20 F_u définis).
  - Q-SI-3, Q-SI-4 : même forme que Q-T4-10.
  - Q-SI-5 : n'affecte que le dernier chiffre, aucun C1 changé.
  - Q-SI-6 : C0 reste une sortie d'E1.
- **Q-SI-7 :** laisser le texte adjugé de Q-T4-10 intact ; c'est à vous de poser une phrase datée, au plus tard au brief de SB-11.
- **Q-SI-8 : à adopter, en ajoutant une ligne (e) :** les courbes de I_t et celles des D*(u) d'un même (point, réplication) doivent venir du même appel `replication`, avec un test au câblage.
- **Q-SI-9 : à adopter pour ce lot, et former un item :** contrôler à l'exécution que n de `fiv_unites.txt` égale le nombre de positions présentes du masque, et K les cellules « ecart » d'EP.
- **I-1 (coût de C1) :** à former. J'ai remesuré 0,32 à 0,33 s par réplication pour les 20 courbes, soit environ 70 min pour E1.
- **I-2, I-3 :** I-2 est à verser dans SHOGEN-SIM-BIS-SB11-BRIEF-1 plutôt qu'en item neuf ; I-3 se confond avec Q-SI-7.

## Items que je propose

- **I-R1 (proposé : SHOGEN-SIM-BIS-C1-CROISEMENT-1) :** le contrôle croisé n et K de Q-SI-9.
- **I-R2 :** la ligne (e) de Q-SI-8.
- **I-R3, méthode pour les campagnes de mutants :** muter aussi le site d'appel d'une fonction partagée, et la source des données passées sous une étiquette inchangée. Les six survivants relèvent de ce cas.

## Écarts

**Écarts du générateur :**
- Son E-2 (`diff -r` sur deux copies entières du dépôt) enfreint la lettre de l'interdit. Il est déclaré et sans exposition ; c'est à vous de l'adjuger.

**Mes écarts :**
- **Exposition :** j'ai lu, comme le contrat le demandait, des lignes de `fiv_unites.txt` qui portent n, K et P̂_more par strate et n, K par hôte, ainsi que les lignes 1 à 24 de `masque_j28.txt`. Aucune pièce de D.2, aucun `*.jsonl`, et `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Clone du dépôt :** j'ai cloné le dépôt en lecture seule (`git clone --bare --no-hardlinks`) pour l'adaptateur `oracle_r1` ; le clone est supprimé.
- **Octets 92 dans mes outils :** 122, des échappements Python écrits par l'outil d'écriture et contrôlés par leur effet ; aucun dans mon rapport ni dans NOTES.
- **Remède rejoué :** au premier essai, le témoin était rouge par ma propre référence calculée en précision 28 ; corrigé et refait.
- **Chemin vu dans la sortie S-G9 :** elle nomme un fichier sous `docs/rapports/`. Je n'en ai vu que le chemin : le fichier est absent de la copie et n'a pas été ouvert.
- **Lectures non faites :** ni `AVIS.md` de SIM-BIS ni la PROPOSITION §3.

## Fichiers produits

Dossier `<scratchpad>/s2bis/sim5/g2/` ; `tmp/` est vide, les copies lourdes sont supprimées.
- `RAPPORT-G2.md` (le rapport complet), sha256 42b37db76eebfe5f601d07d357d911016f25a1a8f05160e73ac2d1b71c5c019e
- `NOTES.md`, sha256 4e4a722e009c29449f8e93033bfd8d5144e510c81a1456f4ee0cdc670a93d595
- `SHA256SUMS`, 47 fichiers, `sha256sum -c` tout OK, sha256 8daaed4241aa582c04aed5c94a50165180eb58505703b499a138c030a77757ae
- `outils/` : mon estimateur, l'oracle du masque, les scripts de confrontation, de mutants et de portes, et `test_revue_g2.py` (les tests de remède, non versés)
- `journal/` : sorties des jobs, de la confrontation, du masque, des mutants, du remède, du mode strict, des portes, de xtask et des contrôles sur f139242
