# Contre-contrôle de la correction `python3 -S` de PLAN-S2BIS-2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 15:20:10 UTC du rapport écrit par le réviseur de la G2 (agent a77f6435bdf260604, reprise) dans `<scratchpad>/s2bis/plan2/cc2/RAPPORT-CC2.md` (sha256 ca544510…) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle de la correction complémentaire `python3 -S` de PLAN-S2BIS-2 (Q-CORR-5, Q-CORR-6)

- **Gate 0** : modèle résolu `claude-opus-5-5`. Je suis le réviseur de la G2 et des deux contre-contrôles de ce lot ; je n'ai écrit aucune correction.
- **Horloge** (`date -u`) : début le 2026-10-08 à 15:13:07 UTC, fin à 15:19 UTC.
- **Base** : tête `e6657dcc3154bf2d35c69b84d9deae1385e702a7`, relevée au début et à la fin ; `git status --short` vide aux deux relevés.
- **Pièces** :
  - `corr/RAPPORT-CORRECTION-S-transcrit.md` (section 13), lu en entier ;
  - `corr/SHA256SUMS`, vérifié d'abord : sha256 `fd572b7b719b…fc00`, `-c` OK sur 176 lignes ;
  - les 11 diffs de `corr/diffs/` ;
  - `corr/outils/ajout_S.py` : littéraux lus par `ast`, jamais exécuté.

## 1. Verdict : CONFORME (liste fermée vide)

| point à contrôler | constat | preuve |
|---|---|---|
| série des 11 diffs sur e6657dc | s'applique **sans retouche** (`--check`, puis `--whitespace=error-all`) ; chaque état est égal à `corr/snap/P2R-x` | sha256 fichier par fichier |
| épingle neuve | sha256 de `scripts/plan-s2bis-2/SHA256SUMS` = `ffe6e5aaf683a782200d65c4ba1541556917fe788afce000d8c9ec5332a4d005` ; `--strict -c` 12/12 | — |
| P2R-0a à P2R-5 identiques à l'état déclaré CONFORME | **oui, à l'octet** : les 9 états intermédiaires sont égaux, fichier par fichier, aux empreintes que j'avais relevées au contre-contrôle précédent (`cc/tmp/etat-*.txt`), et les sha256 des 9 diffs sont inchangés | `cmp` des états |
| delta de cette passe | final contre l'état CONFORME : seuls `README.md`, `lancer.sh`, `tests/test_lancer.py` et `SHA256SUMS` changent | J'ai reconstruit les trois fichiers d'avant en inversant les remplacements déclarés par le correcteur. Leurs empreintes sont **égales** à celles de l'état CONFORME (`d77a28a0…`, `0293fdeb…`, `d92c6526…`) : le delta est exactement celui qui est déclaré, sans changement caché |
| `-S` posé partout où le correcteur le dit | `lancer.sh` l.47 et l.66 : heredocs en `python3 -I -S -B -` ; l.117 : scripts en `python3 -S -B` ; ce sont les trois seuls appels de `python3` du lanceur. Commentaire de tête et README (Lancement, point 2) mis à jour | lu ligne à ligne |
| S24, mon scénario : `.pth` hostile dans le site-packages d'un venv jetable en tête du PATH | sans `-S` (état d'avant) : **12 exécutions**, dont 4 dans les heredocs et 8 dans les scripts (2 scripts × 2 passes × 2 lectures du `.pth`), code 0. Avec `-S` (état final) : **aucune**, code 0, quatre sorties. Le témoin direct du venv exécute le `.pth` deux fois sans `-S` et aucune avec `-S` | `outils/cc2_e2e.py`, dépôt jetable, vrais scripts, fixtures |
| LAN-14 | dans la suite verte, sur les six combinaisons ; c'est le test qui tue M-P2R6-18 à 20 | — |
| S0 avant et après | **identique à l'octet** : mêmes sha256 des quatre sorties (`SHA256SUMS` `aa35fc3e…`, `fiv_unites.txt` `a746f0e1…`, `intervalles.txt` `95ad5265…`, `masque_j28.txt` `61a74a32…`), code 0 des deux côtés | même dépôt jetable et mêmes journaux, lanceur d'avant puis d'après |
| M-P2R6-18 à 20 | **tués** tous trois, par mes propres substitutions : scripts sans `-S` ; premier heredoc sans `-S` ; second heredoc sans `-S`. Mes mutants H-11 (scripts en `-s` au lieu de `-S`) et H-13 (second heredoc en `-S` sans `-I`) sont tués aussi. 5 sur 5, 0 FATAL | témoins 35 OK au début et à la fin ; restauration contrôlée par sha256 ; borne 300 s |
| suite | **35 tests OK** sous 3.11, 3.12 et 3.13 × graines 0 et 1, en `-X dev -W error`, 0 ligne d'avertissement ; 3.10 : échec d'import connu (`hashlib.file_digest`, PY310-1) | `tmp/suite-*.txt` |
| rien de retiré ni d'affaibli | Tests : on passe de 34 à 35 (LAN-14). La reconstruction le montre : l'ancien `test_lancer.py` est exactement le nouveau sans LAN-14. Code : `-S` seulement ajouté, la liste fermée de C-1 et `-I` sont inchangés | empreintes de la reconstruction |
| forme | P2R-6a +149 / −38, P2R-6b +184 / −40, les autres inchangés, donc toutes ≤ 200 ; 0 octet 92, 0 tabulation, 0 retour chariot, 0 ligne de plus de 120 caractères, 0 TODO ou FIXME dans les lignes ajoutées ; rien hors de `scripts/plan-s2bis-2/` ; lot final de 1 717 lignes | script de forme |

**Q-CORR-6** (`-S` posé aussi aux deux heredocs) est retenu par l'adjudication. Ma mesure le justifie : 4 des 12 exécutions de S24 venaient des heredocs, et `-I` n'arrête pas un `.pth` du site-packages de l'interpréteur. H-13 montre en outre que `-I` reste nécessaire à côté de `-S` : sans lui, l'ombre `PYTHONPATH` de LAN-11 revient.

## 2. Répétition à l'échelle : non rejouée

Je juge que `-S` ne peut pas en changer le résultat, pour quatre raisons :
- **Ce que retire `-S`.** `-S` ne retire que le module `site` et ce qu'il charge : site-packages système et utilisateur, fichiers `.pth` et `sitecustomize`.
- **Ce qu'importent les scripts.** Aucun de leurs imports n'en vient : bibliothèque standard ; modules du lot, depuis le dossier du script, que `-S` ne retire pas de `sys.path` ; pièces de PLAN-S2BIS chargées par chemin ; harnais inséré par `commun.importer_harnais`.
- **Ce qui reste en effet.** `PYTHONHASHSEED`, dont dépend l'identité A = B, et `PYTHONPYCACHEPREFIX` restent en effet sous `-S`.
- **Ce qui le confirme.** S0 est identique à l'octet avant et après, par le vrai lanceur. Les deux scripts donnaient déjà des sorties identiques sous `-S` au contre-contrôle précédent.

Le calcul est donc inchangé. La mesure à l'échelle du contre-contrôle précédent (code 0, A = B, 111,9 s, 932 188 Kio) reste valable. La seule différence attendue est l'import du module `site` en moins, de l'ordre de la milliseconde par processus.

## 3. Écarts de ma propre exécution

- **E-1. Chemin faux de `suite.sh`.** Une recopie de `suite.sh` par `sed` a produit un chemin faux (`cc22`). Les six premiers passages de la suite sont sortis en code 9 (`cd`) avant tout test ; ils ne sont pas comptés. J'ai réécrit le fichier puis rejoué.
- **E-2. Pièces du correcteur.** J'ai lu `corr/outils/ajout_S.py` par `ast` pour reconstruire l'état d'avant, sans l'exécuter. J'ai listé un niveau, noms seuls, de `corr/`, `corr/journal/` et `corr/outils/`.
- **E-3. Variable de campagne.** La suite du lot (LAN-6, exception A-3) pose `SHOGEN_S2_CAMPAGNE_CONTROL` dans son seul sous-processus de lanceur, à chacun de mes passages. Je ne l'ai jamais posée moi-même.
- **Ce que je n'ai pas fait.** Je n'ai tapé aucune barre oblique inverse dans mes commandes ; mes fichiers en comptent 0. Le venv et les marques sont sous `cc2/tmp`, retirés ensuite ; rien n'a été écrit dans le HOME réel.

## 4. Fichiers produits

Tous sont sous `<scratchpad>/s2bis/plan2/cc2/` :
- `RAPPORT-CC2.md` (ce rapport) et `NOTES.md` ;
- `outils/` : `cc2_e2e.py`, `reconstruire.py`, `e2e.py`, `compare.py`, `sonde.py` ;
- `mutants/` : `campagne_S.py`, `campagne_S.out` ;
- `travail/` : `suite.sh`, et `avant/` (les trois fichiers reconstruits, aux empreintes de l'état CONFORME) ;
- `tmp/` : sorties des suites et de l'e2e, états.

`SHA256SUMS` : 64 lignes, `-c` OK, ce rapport exclu ; sha256 `d46005b7b1987740b1be72b71c542afb674b6c3ec176b474105042c53cb39707`.

Les copies lourdes (copie de e6657dc, harnais, copie de mutants) ont été retirées. Le dépôt est intact : `git status` vide, HEAD e6657dc.

## 5. Attestation (forme D.3)

- Aucun journal réel de S2 ni de S2-bis n'a été touché. Les seuls `*.jsonl` sont synthétiques, écrits et lus sous `cc2/tmp`, retirés, jamais affichés.
- `lancer.sh` n'a tourné que dans des dépôts jetables, sur fixtures.
- Aucune pièce de la liste D.2 et aucun dossier interdit n'ont été ouverts.
- Je n'ai fait aucune recherche ni énumération récursive sur `docs/`, sur le dépôt ni sur le scratchpad entier.
- Je n'ai fait aucune écriture git sur le dépôt, rien dans le HOME réel, et rien sur Pocket.
