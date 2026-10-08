# CP1 bref — révision du paquet de pré-enregistrement S2 (commit `245cbe0`)

Validateur frais `shogen-validateur`. Rapport écrit au fil de l'eau. Début (`date -u`) : 2026-10-03 00:51:58 UTC ; fin : 2026-10-03 00:57:28 UTC.

## 0. Gate 0

Modèle sous lequel tourne cette instance : `claude-fable-5-1` (Fable 5.1). Effort : `high` selon le brief ; non lisible depuis l'intérieur de la session, non attesté par moi. Conforme à l'attendu.

## 1. Attestation D.3

« Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun ; je n'ai lu aucun taux d'écart, de présence ou de panne d'une source réelle. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à 12, liste lue à l'annexe D l.32-45 sans ouvrir aucune pièce). Je n'ai rien lu sous `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, ni `JOURNAL.md`, ni aucun `*.jsonl` ; rien hors de `/home/user/shogen` sauf mon dossier `validation-2/`. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (`env | grep -c` = 0 ; sonde Python sous `env -u`). Aucune opération git en écriture ; `git status --short` vide au début et à la fin. »

Ce à quoi j'ai été exposé (classe M ou synthétique, déjà écrit dans les pièces admises) :
- comptes de classe M portés par l'annexe D (D.1 n° 7 et n° 9, l.19 et l.21, vus en lisant l'annexe entière) et par le paquet (§2 l.46 : Pyth 0 `ok` sur 40 804 ; §3 l.51 : `resolve_failed` 15,3 % contre 1,85 %, 5 313, 815, 483 ; comptes de fenêtres 35 982, 17 314, 9 261, 38 600, 2 618) ;
- D.3 (a) masquée (annexe D l.54) ;
- sorties **synthétiques** de SIM-NIVEAU et de l'étape S (paquet §10.3, l.135-166) ;
- seuils de conception antérieurs à la campagne (2,33 ; 10 ; ℓ = 240 ; 7 200 ; 0,8416) ;
- noms de pièces de D.2 (liste de l'annexe D ; brief ; G0 du lot CORR l.67 ; G2 du lot CORR §16 ; annexe B l.586, l.603 ; paquet §8 l.89 et §12 pt 18) ;
- sujets des commits de ce dépôt (`git log --oneline 8b14567..245cbe0`, 54 sujets ; comptes de tests et de mutants, aucun taux de source) ; le nom du dossier `monark-m009a` et le nom `JOURNAL.md` dans des sorties `ls` et `git diff --name-only` (noms seuls, contenu non ouvert).

## 2. Brief et identité de la pièce

- Brief : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/validation-2/BRIEF-CP1-BREF.md`, sha256 `02f391963b504c53a8bdae43075919b646e9e9de7f034b4d3a12829aa9a7d898` (= attendu).
- Branche `partie-4-execution` ; HEAD = `245cbe06b79a722ee1e431a4f233147bb861e789` ; `ddf8c54` = `ddf8c547d066388247f1b1c408eda6ca86082273` ; `f35a70c` = `f35a70c19ba8269f1f7e2bcd31775e4fc513da20`.
- sha256 de `docs/adr-0028/PAQUET-PREREG-S2.md` à `245cbe0` : `2252ad4e44c96e8d21aa9a85271888746c57072a6324bfa60409972578f3db02` (= attendu ; identique dans l'arbre de travail) ; à `ddf8c54` : `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097` (= base citée par la puce l.8).
- Copies de travail : `validation-2/paquet-ddf8c54.md`, `validation-2/paquet-245cbe0.md` (lignes citées ci-dessous = lignes de `245cbe0`).

## 3. Contrôle 1 — périmètre

- `git diff ddf8c54 245cbe0 -- docs/adr-0028/PAQUET-PREREG-S2.md` : `1 file changed, 3 insertions(+), 2 deletions(-)`.
  - Hunk 1 (`@@ -5,6 +5,7 @@`) : une seule ligne ajoutée, l.8, « **Révision datée du 2026-10-03 00:49:47 UTC** … » ; l.5-7 et l.9 inchangées.
  - Hunk 2 (`@@ -211,8 +212,8 @@`, section 13) : `commit_analyse 41f087ef3e0a621ddb04fa4f2af8733e5fd5a0f9` → `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` ; `sha256_script 67b897a949b76071e1b3f8508d877217ac33f957f92463dd8e9b5e672ab8f8d9` → `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050`. Rien d'autre.
- Section 10 à l'octet : extraction `sed -n '/^## 10\. /,/^## 11\. /p' | sed '$d'` sur les deux copies : 64 lignes, sha256 `1f9c94561cd0b81b8b2ef72ba3ab5c74215520f12aed994ce1f823464c5fb08f` les deux fois (identique ; §10.1 à §10.4 compris, donc §10.2).
- Sections 1 à 12 : aucune ligne dans le diff (l.11-209 inchangées, décalées de 1).

Périmètre tenu.

## 4. Contrôle 2 — exactitude de la puce (l.8), affirmation par affirmation

| # | affirmation de la puce | source lue | constat |
|---|---|---|---|
| a | « Révision datée du 2026-10-03 00:49:47 UTC (A-8 ; annexe D.4 c ; heure produite par le script d'écriture) » | `git log --format='%h %cI'` : `972612a` 2026-10-03T00:49:18Z, `245cbe0` 00:51:22Z ; B.44 daté 00:44:44 ; README du sceau l.32 daté 00:48:08 | heure comprise entre le commit précédent et le commit de la pièce ; ordre cohérent. A-8 : annexe D l.165 (« nouveau paquet, nouveau sha, nouvelle ancre, délai recommencé ; le premier sha reste cité ») [lu] |
| b | « remplace, avant toute exécution, le paquet scellé le 2026-10-02 (commit `ddf8c54`, sha256 `494d770d…8097`, jeton FreeTSA de genTime 2026-10-02T17:44:30Z) » | README `sceau/premier-2026-10-02/README.md` l.7 (commit `ddf8c54`, sha `494d770d…8097`), l.11 (scellement 2026-10-02), l.28 (genTime 2026-10-02T17:44:30Z) ; sha recalculé par `git show ddf8c54:… \| sha256sum` | exact |
| c | « qui reste cité et n'ouvre plus aucune exécution (`docs/adr-0028/sceau/premier-2026-10-02/`) » | README l.32-41 (« remplacé avant toute exécution … Ce jeton n'ouvre plus aucune exécution ») ; `ls docs/adr-0028/sceau/` : `chain`, `premier-2026-10-02` (le jeton n'est plus à la racine lue par la garde (6)) | exact |
| d | « Motif : deux constats de classe A des relectures G2 de rattrapage, chacun capable de laisser l'exécution unique sans sortie (annexe B.42, B.43) » | B.42 l.588 (A-1 : « ne laisse aucune sortie ») ; B.43 l.605 (A-1 conditionnel : « exécution sans sortie ») | exact (« capable » rend bien le caractère conditionnel de B.43) |
| e | « décision de l'investisseur du 2026-10-02, “Corriger et resceller” » | G0 du lot CORR l.3 (« décision de l'investisseur du 2026-10-02 22:1x UTC … “Corriger et resceller” ») ; README du sceau l.34 ; B.43 l.605 | exact |
| f | « lot CORR (annexe A, ligne CORR ; annexe B.44) » | annexe A l.130 (ligne **CORR**, 2026-10-03, commits `02f9c00` … `f35a70c`) ; B.44 l.615-643 | exact |
| g | « Les sections 1 à 12 sont inchangées, la section 10.2 à l'octet ; aucune valeur, aucun seuil, aucune inégalité de la règle ne change » | §3 de ce rapport ; G2 du lot CORR §5 l.77-80 (JSON de la règle `ea3a2d94…` et épingles inchangés) [2nd] ; annexe A l.130 | exact |
| h | (i) prix non fini (NaN, Infinity, toute forme que `Decimal` admet) lu comme absent, panne au sens de `classify_ecart`, point unique `r1.parse_journal`, avertissement avec compte par flux, jamais les valeurs ; prix fini : rien ne change (SHOGEN-PRIX-NON-FINI-1) | `git show f35a70c:s2-harness/shogen_s2/r1.py` l.398-420 : `not Decimal(r["price"]).is_finite()` → `r["price"] = None`, `Counter` par `flux_id`, `sys.stderr.write(... " — par flux : " ... "valeurs non reproduites")` ; G2 du lot CORR §7.1 (seul point de lecture des prix, l.118-137) et §7.2 (0 écart pour tout prix fini, l.152) [2nd] ; G0 l.12-20 | exact. Précision non dite par la puce, sans fausseté : la requalification vaut quel que soit le statut (Q-1, G0 l.79-80 ; docstring l.404) |
| i | (ii) « le recalcul tiers écrit les paires de copies exactes en listes triées (SHOGEN-RECALCUL-JSON-COPIE-1) » | `rendu_unique.py` à `f35a70c` l.363-368 : `if isinstance(x, (set, frozenset)): return sorted(x)` | exact |
| j | (iii) trois points hors décision : « DIVERGENCE ASN » entre relevés complets seulement ; bloc 4 « (pool d'analyse, ADR-0028 D1) » au cas (a) ; verdict de refus du journal brut sans le chemin du dossier | `r2.py` l.781-798 (`status == "ok"` et `None not in (asn_ripestat, asn_cymru)` ; `complet[h]`) ; `report.py` l.489-491 ; `rendu_unique.py` l.400 (`replace(os.path.join(a.journaux, ""), "")`) ; G2 §6 l.114 : `asn_divergences` lu seulement par `report.py` (k_eff, drapeau 2 inchangés) [2nd] ; B.44 l.633-635 | exact. B.44 parle de « deux points » pour les rendus J14/J28 ; le troisième de la puce est le run `raw` : cohérent |
| k | (iv) « les renvois “l.n” au code restent ceux de `8b14567` » | paquet l.5 (« “l.n” renvoie à la ligne n … à `8b14567` ») ; exemples décalés à `f35a70c` : §1 l.15 cite `rendu_unique.py` l.29 (`CHEMINS`), à `f35a70c` l.30 ; §12 pt 1 cite l.392-398 (run `raw`), à `f35a70c` l.395-401 ; `lire_bloc` reste à l.83 | exact et utile (déclaration qui couvre les décalages) |
| l | (iv) « le code exécuté est celui de `commit_analyse` (section 13), **qui est la tête de la branche `partie-4-execution` au remplissage**, et non plus celle de `partie-3-paquet` » | `git log f35a70c..245cbe0` : `638f914` (00:46:08Z), `972612a` (00:49:18Z), `245cbe0` (00:51:22Z) ; puce datée 00:49:47Z ; `git branch -a --contains f35a70c` : `partie-4-execution` seule | **inexact** : au remplissage (00:49:47Z), la tête de `partie-4-execution` était `972612a`, dont `f35a70c` est l'ancêtre à deux commits (documents seuls : `git diff --stat f35a70c 245cbe0 -- s2-harness/shogen_s2 s2-harness/tools` vide). La valeur du bloc est juste (contrôle 4) ; c'est la phrase qui ne décrit pas le fait. **Constat C-1** |
| m | (iv) « les commits de la session cloud y sont signés comme le dit la section 12, point 16 » | `git cat-file commit` : `gpgsig` présent (SSH SIGNATURE, ed25519) sur `f35a70c`, `638f914`, `972612a`, `245cbe0` ; §12 pt 16 l.204 (« signés par la clé SSH de la session ») | exact pour la signature. Le pt 16 nomme encore `partie-3-paquet` et la PR #1 non fusionnée : voir observation O-2 |
| n | (v) annexe D sha256 `deb64179…eaf`, dernier changement `e586c0b` | `sha256sum docs/adr-0028/ANNEXE-D-preenregistrement.md` = `deb64179a8d9fe8689b5b26021e4de649af2e6fb0c5b29235bd76955b5690eaf` (arbre et `245cbe0`) ; `git log -1 -- <annexe D>` = `e586c0b` 2026-10-02T21:28:42Z | exact |
| o | (v) « 16 lectures en D.1 (la n° 16 … datée du 2026-10-02 après le premier sceau et avant celui-ci) » | lignes de table l.13-28 : 16 lignes numérotées 1 à 16 ; l.28 : n° 16, orchestrateur de la session cloud, « 2026-10-02 17:57Z », « après le scellement » ; genTime du premier sceau 17:44:30Z | exact (17:57Z > 17:44:30Z ; antérieur au sceau à venir) |
| p | (v) « 12 points en D.2 » | l.34-45 : points numérotés 1 à 12 (liste lue, aucune pièce ouverte) | exact |
| q | (v) « les attestations (a) à (j) en D.3 » | en-têtes (a) l.51, (b) l.61, (c) l.69, (d) l.77, (e) l.83, (f) l.87, (g) l.112, (h) l.118, (i) l.196, (j) l.198 : dix | exact |
| r | (v) « MONARK-S2-M009A-EXPOSITION-1 est fermé (annexe B.38 : aucun auteur de la règle ni décideur n'a vu la lecture 2, sous les limites de B.37), ce qui lève la limite écrite à la section 8 » | B.38 l.544 (« fermé … aucun auteur de la règle SHOGEN-CRITERE-R1-1 ni décideur, sous les limites de B.37 ») ; B.37 l.540 (limites : jetons exacts, fenêtre de 300 caractères, fichiers textuels) ; D.3 (i) l.196 (« non ») ; §8 l.89 (« n'est pas clos à la rédaction de ce paquet : limite déclarée … consignée au JOURNAL, sans réécriture de ce texte ») | exact ; la puce est le lieu prévu par §8 (pas de réécriture de §8) |
| s | Règle d'écriture (paquet l.6) : aucune valeur de z, K, P̂_more, φ de campagne dans la puce | lecture de l.8 : sha256, commits, dates, comptes de lignes de l'annexe D, noms d'items | tenue |

## 5. Contrôle 3 — effet sur la règle et sur les autres sections

- §10.2 : identique à l'octet (§3) ; aucune des précisions (i)-(iii) ne touche une valeur, un seuil (2,33 ; 10 ; 7 200 ; ℓ = 240 ; 0,8416) ni une inégalité. (i) agit en amont de `classify_ecart` sur une lecture dont le prix n'est pas un nombre : §10.2 pt 1 (« panne / staleness / hors-enveloppe ») et §2 (« lectures `ok` » du pool D1, prédicat statut ok et prix non nul, G2 §7.1 l.132) gardent leur sens, un prix non fini étant traité exactement comme un prix nul. (ii) est une sérialisation. (iii) touche des impressions hors décision (§10.2 pt 9 : L&M bloc 4 hors décision ; divergences ASN lues par `report.py` seul ; verdict `raw` : §12 pt 1).
- §2, §6, §11 : aucun changement de sens.
- §8 : « 15 lectures », « points 1 à 11 », « D.3 (l.47-108) », item MONARK « n'est pas clos » (l.89) : dépassés, et la puce (v) le dit tous (16, 12, (a)-(j), fermé). Pas de contradiction non déclarée.
- §9 : garde (6) voie (a) lit `docs/adr-0028/sceau/` (l.104) ; le jeton y est absent depuis le déplacement (README du sceau l.40-41) : l'exécution est fermée jusqu'au nouveau sceau, ce que la puce dit (« n'ouvre plus aucune exécution »). Renvois de lignes à `rendu_unique.py` (l.97, l.105, l.106, l.107) : décalés, couverts par (iv).
- §12 pt 16 : voir O-2 ; pt 1 (l.392-398) : décalage couvert par (iv) ; pt 20 : inchangé.
- §13 texte (l.212) : « tête de `partie-3-paquet` au remplissage » et « `rendu_unique.py` l.83-105 » : contredits par la puce (iv), qui le dit explicitement. Reste la formulation de la puce elle-même (C-1).
- §1 l.15 (« tête de `partie-3-paquet` », « `rendu_unique.py` l.29 ») : même traitement, couvert par (iv). §1 l.17 : voir O-1.

## 6. Contrôle 4 — bloc machine (valeurs recalculées par moi)

- `git rev-parse f35a70c` = `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` = clé `commit_analyse` (l.215).
- `git show f35a70c:s2-harness/tools/rendu_unique.py | sha256sum` = `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050` = clé `sha256_script` (l.216) ; égal au préfixe `06d189cf…` du G2 du lot CORR l.83.
- `git diff --stat f35a70c 245cbe0 -- s2-harness/shogen_s2 s2-harness/tools` : vide (code identique). Dernier commit touchant ces chemins : `a5a9de9` (00:42:29Z) ; `f35a70c` n'ajoute que des tests (K-1, K-2), code inchangé : cohérent avec la garde (2).
- Six autres lignes : `diff` des deux blocs (`ddf8c54` contre `245cbe0`) ne montre que `commit_analyse` et `sha256_script` ; `journal control.jsonl`, `journal journal.jsonl`, `journal raw.jsonl`, `sommes`, `cacert_sha256`, `tsa_crt_sha256` inchangées.
- `cacert_sha256` et `tsa_crt_sha256` égales aux sha256 de `docs/adr-0028/sceau/chain/cacert.pem` (`2151b611…4438`) et `tsa.crt` (`8bfb0305…3467`), préfixes de D.4 c.
- Ouvertures « ```shogen-paquet-v1 » : `grep -c` = 1 (l.214) ; l'autre occurrence du mot est en prose (l.210, l.212).
- Sonde `lire_bloc` : extraction `git archive f35a70c s2-harness/tools s2-harness/shogen_s2` dans `validation-2/sonde/` (hors dépôt ; sha256 de la copie de `rendu_unique.py` = `06d189cf…9050`), script `validation-2/sonde/sonde_lire_bloc.py`, sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B` : `lire_bloc OK`, six clés + trois journaux aux valeurs du bloc, exit 0 ; 0 `__pycache__`. Deux mutants du texte (ligne `sha256_script` dupliquée ; `commit_analyse` en majuscules) : `ValueError: ligne du bloc malformée, dupliquée ou inconnue` (refus).

Format et valeurs recalculées : conformes.

## 7. Contrôle 5 — vocabulaire (doc 09)

`grep -o -i` sur l.8 puis sur le fichier entier pour `garanti*`, `prouv*`, `\bsûr*`, `vérifié*`, `validé*`, `sécuris*` : 0 occurrence dans la puce ; 0 occurrence de `garanti*`, `prouv*`, `sûr*` dans tout le fichier. Règle d'écriture : aucune valeur de z, K, P̂_more, φ de campagne dans la puce (§4 s).

## 8. Contrôle 6 — gates

`env -u SHOGEN_S2_CAMPAGNE_CONTROL cargo --locked xtask verify` (sortie `validation-2/xtask-verify.out`, 90 lignes) : code de sortie **0** ; `grep -c VIOLATION` = **0** ; huit gates « VERDICT : VERT (0 violation(s)) », `cargo fmt --check : VERT`, `no_std … : VERT`, `cargo clippy -D warnings : VERT`, « VERDICT GLOBAL : VERT ».

## 9. Constats

**C-1 (puce l.8, précision (iv) ; exactitude d'une affirmation de traçabilité ; sans effet sur la règle ni sur le bloc).** La puce écrit que `commit_analyse` « est la tête de la branche `partie-4-execution` au remplissage ». Au remplissage (00:49:47Z, heure de la puce), la tête était `972612a` (00:49:18Z) ; `f35a70c` (00:44:31Z) en est l'ancêtre, suivi de deux commits de documents (`638f914`, `972612a`). La valeur `f35a70c` est la bonne (code de `s2-harness/shogen_s2` et `s2-harness/tools` identique jusqu'à `245cbe0` ; dernier commit du lot CORR ; gel déclaré par `972612a`) ; seule la phrase est inexacte. Correction en §11.

**Observations (hors liste fermée, aucune correction demandée) :**
- **O-1** (§1 l.17) : « les 91 commits cités par ce texte sous 7 chiffres sont … ancêtres de `8b14567` » ; la puce cite `ddf8c54` et `e586c0b`, le bloc `f35a70c`, postérieurs à `8b14567` (tous ancêtres de `245cbe0`, vérifié). La phrase reste vraie pour ce qu'elle contrôlait à `8b14567` ; la puce ne le dit pas.
- **O-2** (§12 pt 16, l.204) : le point nomme la branche `partie-3-paquet` et « `main` n'est pas touchée tant que la PR KraidleAI/shogen#1 n'est pas fusionnée » ; depuis, `fdc7252` (« Fusion de la partie 3 ») est dans l'ascendance de `245cbe0` et la branche est `partie-4-execution`. La puce (iv) couvre le changement de branche et la signature ; la limite « sceau privé » (clé de signature de la session, pas de bundle hors ligne) reste telle quelle. Rien de faux dans la puce.
- **O-3** (§13 l.212 et §1 l.15) : « tête de `partie-3-paquet` au remplissage » reste écrit ; la puce (iv) le remplace explicitement. Après C-1, la description sera exacte.
- **O-4** (§4 l.56, D.1 n° 16) : la lecture n° 16 (classe R présumée, orchestrateur de la session cloud, après le premier sceau) est déclarée par la puce ; son analyse contre D2 pt 4 est portée par B.35 (sujet du commit `04beacd`, non lu par moi [2nd]). Hors du périmètre de ce cp-1 bref ; signalé parce que §4 lie le statut confirmatoire aux attestations des décideurs.
- **O-5** (puce (i)) : l'omission de « quel que soit le statut » (Q-1) n'est pas une fausseté ; l'effet est nul sur les lectures non `ok` (aucun prix écrit, G2 §7.3 l.170-171).

Aucun constat ne touche §10.2, le bloc machine ni un choix de valeur : pas d'ESCALADE-INVESTISSEUR.

## 10. Verdict : **ACCEPTE-AVEC-CORRECTIONS**

Liste fermée : **C-1**, une correction, limitée à la puce (l.8). Après son application, je n'ai aucune autre réserve sur le texte ni sur le format du bloc.

## 11. Correction C-1 (l.8, à l'intérieur de la précision (iv))

Texte actuel (extrait exact de l.8) :

```
le code exécuté est celui de `commit_analyse` (section 13), qui est la tête de la branche `partie-4-execution` au remplissage, et non plus celle de `partie-3-paquet` ;
```

Texte proposé :

```
le code exécuté est celui de `commit_analyse` (section 13) : `f35a70c`, dernier commit du lot CORR sur la branche `partie-4-execution` (gel déclaré au commit `972612a`), ancêtre de la tête de cette branche au remplissage, dont le code de `s2-harness/shogen_s2` et `s2-harness/tools` est identique au sien (garde (2)) ; ce commit n'est plus pris sur `partie-3-paquet` ;
```

(Le texte « tête de `partie-3-paquet` au remplissage » de §1 l.15 et §13 l.212 n'est pas à toucher : sections 1 à 12 inchangées par construction, et la puce le remplace.)

## 12. Fichiers ouverts (lignes)

- Brief (entier, l.1-61).
- `docs/adr-0028/PAQUET-PREREG-S2.md` à `ddf8c54` et à `245cbe0` (copies ; `245cbe0` lu en entier, l.1-224).
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` (entier, l.1-212 ; liste D.2 l.32-45 lue, aucune pièce ouverte).
- `docs/adr-0028/ANNEXE-B-items.md` : en-têtes de blocs (`grep -n '^## '`), l.533-546 (B.37, B.38), l.584-643 (B.42, B.43, B.44).
- `docs/adr-0028/ANNEXE-A-lots.md` : l.126-131 (ligne CORR l.130).
- `docs/adr-0028/G0-lot-CORR.md` (entier, l.1-93, dont « Adjudication » l.63-92).
- `docs/G2-lot-CORR.md` (entier, l.1-448).
- `docs/adr-0028/sceau/premier-2026-10-02/README.md` (entier, l.1-42).
- `docs/09-vocabulaire.md` (entier, l.1-64).
- Code à `f35a70c` par `git show` : `r1.py` l.396-425 (+ `grep -n`) ; `r2.py` l.778-806 (+ `grep -n`) ; `report.py` l.484-493 (+ `grep -n`) ; `rendu_unique.py` l.1-35, l.83-120, l.360-372, l.392-412 (+ `grep -n`).
- `ls docs/adr-0028/`, `docs/adr-0028/sceau/`, `docs/adr-0028/sceau/premier-2026-10-02/` (noms seuls).

## 13. Commandes principales et sorties

| commande | sortie |
|---|---|
| `date -u` (début / fin) | 00:51:58Z / 00:57:28Z, 2026-10-03 |
| `sha256sum` du brief | `02f39196…d898` |
| `git status --short`, `git branch --show-current`, `git rev-parse HEAD 245cbe0 ddf8c54 f35a70c` | vide ; `partie-4-execution` ; `245cbe0…`, `ddf8c54…`, `f35a70c…` (§2) |
| `git show 245cbe0:<paquet> \| sha256sum` ; idem `ddf8c54` ; `sha256sum` arbre | `2252ad4e…db02` ; `494d770d…8097` ; `2252ad4e…db02` |
| `git diff --stat` / `git diff ddf8c54 245cbe0 -- <paquet>` | 3 insertions, 2 suppressions ; deux hunks (§3) |
| section 10 extraite des deux copies, `sha256sum`, `wc -l` | `1f9c9456…b08f` ×2 ; 64 lignes |
| `grep -c '^```shogen-paquet-v1'` ; `diff` des deux blocs | 1 ; `2,3c2,3` seulement |
| `git show f35a70c:s2-harness/tools/rendu_unique.py \| sha256sum` | `06d189cf…9050` |
| `git diff --stat f35a70c 245cbe0 -- s2-harness/shogen_s2 s2-harness/tools` | vide |
| `git log -1 --format=%h -- s2-harness/shogen_s2 s2-harness/tools` | `a5a9de9` |
| `sha256sum` annexe D ; `git log -1 -- annexe D` ; `git show 245cbe0:annexe D \| sha256sum` | `deb64179…eaf` ; `e586c0b` 2026-10-02T21:28:42Z ; `deb64179…eaf` |
| `sha256sum sceau/chain/cacert.pem tsa.crt` | `2151b611…4438` ; `8bfb0305…3467` |
| `git log --format='%h %cI' -6` ; `git log --oneline f35a70c..245cbe0` ; `git merge-base --is-ancestor f35a70c 245cbe0` ; `git branch -a --contains f35a70c` | §4 l ; trois commits ; ancêtre ; `partie-4-execution` |
| `git cat-file commit <c> \| grep -c '^gpgsig'` ×4 | 1, 1, 1, 1 (SSH SIGNATURE) |
| `git log --oneline 8b14567..245cbe0` | 54 sujets (chronologie du lot CORR, du sceau et des relectures) |
| `git archive f35a70c …` + `sonde_lire_bloc.py` (×3) sous `env -u … python3 -B` | OK / refus / refus (§6) ; `env \| grep -c SHOGEN_S2_CAMPAGNE_CONTROL` = 0 ; 0 `__pycache__` |
| `grep -o -i` vocabulaire (puce, fichier) | 0 occurrence |
| `cargo --locked xtask verify` (arrière-plan, sortie capturée) | EXIT=0 ; 0 VIOLATION ; VERDICT GLOBAL : VERT |

## 14. Déclaration FM-1.1 — occurrences de chemins ou de noms de pièces de D.2 dans mes appels d'outils

Entrées (arguments de mes commandes) : **aucun chemin de D.2 passé en argument** à `cat`, `sed`, `grep`, `git show`, `ls` ou `Read`. Aucune option `--exclude` utilisée (aucune recherche multi-fichiers dans `docs/` : les `grep` ont porté sur des fichiers nommés et admis, en en-têtes ou lignes ciblées). Les seules occurrences de ces noms dans mes entrées sont les écritures de ce rapport (`Write` de `CP1-BREF-REVISION.md`), qui citent `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `JOURNAL.md`, `*.jsonl` comme noms (§1, §14).

Sorties (résultats d'outils) portant des noms de D.2 ou des pièces listées par le brief : le brief lui-même ; annexe D l.32-45 (liste) ; G0 du lot CORR l.67 (exclusions citées) ; G2 du lot CORR §16 l.388-389, l.410-415 ; annexe B l.586, l.603 ; paquet §8 l.89, §12 pt 18 ; `ls docs/adr-0028/` (nom `monark-m009a`) ; `git diff --name-only f35a70c 245cbe0` (nom `JOURNAL.md`) ; sujets de commits de ce dépôt (noms `monark-m009a`, « sujet du commit `aa04924` » sans son contenu). Aucun fragment de la cartographie l.51, d'ADR-0025 l.14, ni du sujet du commit `aa04924` de `monark-governance` (dépôt jamais interrogé).

## 15. Clôture

- Aucune opération git en écriture ; `git status --short` vide à la fin ; rien écrit hors de `validation-2/` (copies `paquet-*.md`, `sonde/`, `xtask-verify.out`, ce rapport).
- Attestation D.3 du §1 confirmée en l'état à la clôture.
