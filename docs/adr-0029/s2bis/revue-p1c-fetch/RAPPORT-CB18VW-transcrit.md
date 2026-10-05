# Rapport du worker — CB-18v et CB-18w de P1 tranche C (fetch-depth du job sim-bis ; transcrit)

> Transcription par l'orchestrateur le 2026-10-05 16:08:18 UTC du rapport rendu par message par le worker (agent aa9c3df62627c22da) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0** : le modèle résolu est `claude-opus-5-5` (préfixe conforme). L'effort `max` vient de la fiche ; je ne peux pas l'observer de l'intérieur.

## Résumé (lot CB-18v et CB-18w, dossier `corr4/`)

1. **La base est conforme au brief.** La tête est 98c8537, `git status` vide, lue en `--no-optional-locks`.
   - J'ai reproduit ta mesure : la tête seule donne 77 ok ; la tête plus la série SIM-T4 (13 diffs, 13 sur 13 OK aux SHA256SUMS de sim4 et de sim4/corr) donne 76 ok et 1 échec (K-03).
   - Seul le gabarit refuse le job : l'analyseur admet déjà le job sim-bis du `gates.yml` d'e14h.
2. **CB-18v (à poser avant SIM-T4).** Dans `gabarit()`, pour le seul job sim-bis-unittest, la ligne `FETCH = 10 espaces + "fetch-depth: 0"` (égalité exacte) est admise, à la place qui suit `persist-credentials: false`. Les jobs s2bis et S2 sont inchangés.
   - Les cas ont été écrits d'abord :
     - L-37 : la ligne, admise ;
     - L-38 : `fetch-depth: 1`, refusé ;
     - L-39 : la ligne dans le job s2bis, refusée ;
     - L-40 : `ref: main` après la ligne, refusé ;
     - L-41 : la ligne avant `persist-credentials`, refusée (voir E-1).
   - Rouge : sous le gabarit de la tête, L-37 échoue (81 ok, 1 échec) ; avec SIM-T4, K-03 échoue aussi.
   - Vert : la tête passe à 82 ok (au-dessus de 77), et la tête plus CB-18v plus SIM-T4 donne aussi 82 ok, K-03 compris.
3. **CB-18w (à poser après SIM-T4), qui ferme O-2.** La ligne est désormais exigée dans le job sim-bis : si elle manque à sa place, le gabarit refuse.
   - L-42 (le job sim-bis sans la ligne, refusé) a été écrit d'abord. Il est rouge sur la tête plus CB-18v plus SIM-T4 (82 ok, 1 échec), et vert avec CB-18w (83 ok).
   - Contrôle de l'ordre : CB-18w posé sans SIM-T4 fait échouer K-03. Il faut donc committer CB-18w après la série.
4. **Mutants, lancés par la commande du job s2bis (borne 300 s, 0 FATAL).**
   - CB-18v : 5 sur 5 tués, chacun par un seul cas (tous les jobs → L-39, valeur quelconque → L-38, jamais admise → L-37, lignes suivantes du `with:` admises → L-40, ligne admise à toute place → L-41).
   - CB-18w : 6 sur 6 tués (seulement admise → L-42 ; exigée partout → K-01, K-02, L-00, L-39 ; ligne quelconque ou valeur quelconque → L-38 ; lignes suivantes → L-40 ; toute place → L-41).
   - Rejoués sur l'état final : r 8 sur 8, s 3 sur 3, t 4 sur 4, u 6 sur 6, CA-01 à CA-12 12 sur 12.
5. **Aucun cas existant affaibli.** Les deux diffs ne retirent que des lignes de docstring, plus la ligne `if` de CB-18v (dans CB-18w) et la parenthèse fermante qui suit L-41. Les 77 cas de la tête passent toujours (83 ok au total). Les leurres du réviseur (`leurres_cc.py`, `leurres_cc2.py`) donnent les mêmes verdicts sur la tête et sur l'état final ; N-20 est toujours refusé par K-03.
6. **Vérifications sur l'état final** (tête, CB-18v, SIM-T4, CB-18w ; copie hors exclusions, réseau isolé) :
   - job s2bis sous python3.10 à 3.13 : Ran 184, plancher 184 inchangé ;
   - S2 : Ran 406 ;
   - crochets : 54 ok ;
   - matrice `-X dev -W error` : s2bis 184 OK sous les quatre versions ; runner 83 ok sous les quatre versions ; test de l'enregistreur de rôle OK sous les quatre versions ; 0 avertissement ;
   - xtask : identique au témoin de la tête. Seule violation : S-G9 `docs/17-modele-de-menace.md:70`, connue ;
   - R-13 : aucune occurrence ;
   - secrets : sortie 0 en index pour CB-18v et pour CB-18w, et en `--tree` (805 fichiers) ;
   - job sim-bis : voir I-1.

## Diffs (`corr4/diffs/`)

Aucun octet 92 ajouté ; aucune ligne de plus de 120 caractères.

| diff | code | docs | sha256 |
|---|---|---|---|
| CB-18v | +31 / −8 | +32 | 8db2bfc9… |
| CB-18w | +13 / −9 | +25 | 15ec5079… |

`corr4/SHA256SUMS` : e64ebccd…, 92 sur 92 OK.

**Arbres**

- Copie hors exclusions : tête 1b01b83b → v 4f7c26de → plus SIM-T4 0f924172 → w **c0f20e9c**. La copie de contrôle reconstruite en appliquant les diffs donne aussi c0f20e9c, égale au commit final de w.
- Arbre complet : tête 5bbd1bc3 → v 65d37cd0 → SIM-T4 a33f919d → w **caf39a0e**.
- CB-18v et CB-18w s'appliquent avec 0 décalage.

## Points à décider

- **I-1, bloquant pour le job sim-bis, hors de mon lot.** Sur la tête plus SIM-T4, le job sim-bis échoue, avec ou sans mes diffs.
  - L'étape du runner passe (83 ok). La suite sim-bis lance 172 tests avec 1 échec : `test_g0_mesure`.
  - Cause : `G0-SIM-BIS.md` vaut d9cffc0a… à la tête, alors que SB-14H épingle a216a953…. Le G0 figé n'est pas dans la série ; SB-14H précise qu'« un G0 et une épingle commités séparément font échouer le job ».
  - Le même échec apparaît sans CB-18v ni CB-18w. L'extraction de f35a70c par `git archive`, elle, fonctionne : je l'ai testée dans une copie git qui partage les objets du dépôt.
  - Il faut committer le G0 figé avec la série SIM-T4.
- **I-2, ordre de commit.** CB-18v, puis SIM-T4, puis CB-18w.
- **E-1, à adjuger.** L-41 (ordre de la ligne) s'ajoute aux trois cas demandés. Sans lui, le mutant « ligne admise à toute place » survit. C'est un serrage : le gabarit garde l'ordre exact des lignes.
- **E-2, à savoir.** M-18r-04 n'était plus applicable depuis la mise en page du gabarit par CB-18u (dans corr3, la campagne r avait tourné sur l'état r). Pour le rejeu, je l'ai réécrit avec la même mutation ; il est tué, par L-29 d'après mon raisonnement (la campagne ne nomme pas le cas).
- **E-3, à savoir.** L'outil Edit a retiré une espace finale (`EXCLUES =DEBUT`). Je l'ai vu au `git diff` et corrigé avant toute preuve comptée.
- **E-4, à savoir.** La série SIM-T4 s'applique sur la tête avec un décalage de 2 lignes, sur 15 hunks, tous dans `gates.yml` : ce sont les lignes du commentaire CB-18m. Le résultat est identique sur la tête et sur la tête plus CB-18v.
- **[abs]** Le comportement de `fetch-depth: 0` sur la forge n'est pas vérifié.

## Journal G1

**Sources**

- [lu] Ton message.
- [lu] `sim4/corr/NOTES.md`, lignes 120 à 150.
- [lu] `gates.yml` d'e14h ; `commun.py` (RACINE) ; `oracle_r1.py` (extraction) ; `test_commun.py`, lignes 55 à 85 ; `parametres.json` (Q-T4-11, commit f35a70c19ba8…).
- [lu] `BRIEF-CB18.md`, ligne des exclusions.
- [lu] Le runner, le vérificateur et `gates.yml` de la tête.
- [abs] La forge.

**Commandes et sorties**

- `date -u` : 15:38:22 au départ, 16:05:22 à la fin.
- `serie_sim4.sh` / `verif_serie4.sh` : sorties ci-dessus.
- `rouge_variantes.py` → `rouge-CB-18v.txt`, `rouge-CB-18w-variantes.txt`.
- `campagne.py` : v et w.
- `verif_finale4.sh` : PID réel 3633 (SID 3633, parent setsid 3631), de 15:55:23 à 16:04:57, ligne FIN présente.
- `r13.py`, `gate-secrets.sh`, `leurres_cc*.py`.

**Chiffres recomptés** : runner 312 lignes et 82 cas pour CB-18v, 316 lignes et 83 cas pour CB-18w ; lignes par diff recomptées avec `compte_diffs.py`.

**État des autres dossiers** : nettoyage fait. Le dépôt est à HEAD 98c8537, status vide. corr2 (123 sur 123) et corr3 (133 sur 133) sont intacts.

Tout est dans `<scratchpad>/s2bis/cb18/corr4/` :
- `diffs/` : CB-18v.diff, CB-18w.diff
- SHA256SUMS
- NOTES.md
- fichiers-touches.txt
- `metriques/` : v.md, w.md
- `mutants/` : mutants_cb18v.py, mutants_cb18w.py, variantes_v.py, variantes_w.py, mutants_rejeu_r.py
- `preuves/` : rouge-CB-18v.txt, rouge-CB-18w.txt, rouge-CB-18w-variantes.txt, vert-CB-18w.txt, campagne-mutants_cb18v.txt, campagne-mutants_cb18w.txt, verif-serie.txt, application-sim4-sur-tete.txt, sim-bis-job-final-essai.txt, sim-bis-suite-tete-sim4.txt
- `preuves/final/`
- `outils/` : verif_finale4.sh, copie_git.sh
