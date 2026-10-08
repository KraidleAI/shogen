# Contre-contrôle de la correction finale d'OUT-2j (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 18:42:05 UTC du texte écrit par l'agent a2e19320cea9d85a0 dans `<scratchpad>/s2bis/outillage2/corr3/revue/cc/RAPPORT-CC.md` (sha256 c23b880e…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle de la correction C-1 (OUT-2j corrigé) — revue G2 neuve d'OUT-2, troisième tour

**Gate 0 : `claude-opus-5-5`** (contexte système ; effort `max` selon la fiche, non mesurable de l'intérieur).
Horloge (`date -u`) : de 17:54:07 à 18:04 UTC, le 2026-10-08. Réviseur : le même que pour la revue de corr3 ; je n'ai
écrit ni OUT-2j ni sa correction.

## Verdict : CONFORME (liste fermée vide)

## Contrôles

| Point | Mesure | Résultat |
|---|---|---|
| SHA256SUMS de corr3 | sha256 `1f94c5c597d8f20aa4957736aaa7e829a61ee3960e7f7145d268e247836bcb96` ; 736 entrées, 736 OK | conforme au déclaré |
| OUT-2j corrigé | sha256 `3f5ed4dc2636732ee80c18775a9084197c15489af928037c540ac89f3a52a66f` ; OUT-2g, h, i inchangés (`0c6ca1e6…`, `640c3d7d…`, `96094e91…`) | conforme |
| Série sur `e6657dc` | `git archive` (7 exclusions), OUT-2a à OUT-2f (`corr/diffs`) puis OUT-2g à OUT-2j, `patch -p1 -F0` | ni décalage ni rejet ; 9/9 fichiers du contrat égaux à `livrables/fichiers-j.sha256` |
| Série sur `b46672b` (tête actuelle) | idem | ni décalage ni rejet ; 9/9 égaux ; fichier de test identique octet pour octet à celui de la série sur `e6657dc` |
| Code inchangé (tests seuls) | `diff` de l'ancien OUT-2j (`livrables/avant-C1/OUT-2j.diff`, `9b41f9d1…`, celui de ma revue) et du nouveau ; listes `avant-C1/fichiers-j.sha256` et `fichiers-j.sha256` | seul `s2-harness/tests/test_oracle_record.py` change (`0cda4bba…` → `64bacc32…`) ; vérificateur `de48c6bf…`, outil `4d0e4503…`, runner, `test_rendu_production`, `gates.yml` (`ee03d7b1…`), READMEs, FORMAT : inchangés |
| Changement | un sous-test `{"PYTHONDEVMODE": "0", "PYTHONWARNINGS": ""}` → `["-X", "dev"]` ; le « Rougit si » ajoute le motif « non vide autre que « 1 » … pris pour absent », garde tous les anciens | conforme au remède de C-1 |
| J09 tué par S2 | mutant de la revue (`== "1"`), et deux voisins, sur l'état corrigé, par les lignes du job (3.12, borne 300 s) | voir le tableau des mutants : 6 sur 6 tués par S2, 0 FATAL |
| Rien retiré ni affaibli | cas du runner et tests S2, ancien j contre j corrigé, sous 3.11 à 3.13 | runner 136 = 136 (mêmes identifiants) ; S2 415 = 415, aucun retiré ni ajouté (sous-test seulement) ; `PLANCHER` 415, `CAS` 136 inchangés |
| Forme | OUT-2j corrigé | 49 lignes ajoutées, 10 retirées (≤ 200) ; aucune de plus de 120 caractères ; aucun marqueur R-13 ; aucun import ajouté ; octets 92 : 1 ajouté et 1 retiré (la même ligne `f"argv …\n"` qu'avant) ; par fichier à l'état final : 18, 30, 8, 66, 58, inchangés |

## Mutants (Python 3.12, état corrigé, classés runner, puis s2bis, S2, sim-bis)

| Mutant | Sous la matrice (`-X dev -W error` par l'environnement) | Hors matrice (PYTHONDEVMODE et PYTHONWARNINGS vides) |
|---|---|---|
| J09 : `bool(environ.get("PYTHONDEVMODE"))` → `== "1"` | TUÉ, S2 : FAIL du sous-test `PYTHONDEVMODE='0'` (runner 0, s2bis 0, S2 1) | TUÉ, S2, même sous-test |
| J09b : « 0 » pris pour absent | TUÉ, S2, même sous-test | TUÉ, S2 |
| J02 (témoin de non-régression) : vide pris pour posé | TUÉ, S2 : sous-test `PYTHONDEVMODE=''` | TUÉ, S2 |

FAIL seulement, aucun ERROR ; aucun FATAL ; S2 en 42 à 48 s.

## Lignes du job (état corrigé ; réseau isolé ; variable scellée retirée ; PYTHONDEVMODE=1, PYTHONWARNINGS=error)

| Python | runner | s2bis | sim-bis | S2 |
|---|---|---|---|---|
| 3.10 | 136 ok | 255 | 172 | rouge connu PY310-1 : 80 entêtes FAIL/ERROR, identiques à la base et à l'ancien j ; FAILED (failures=77, errors=3, skipped=2) ; `test_drapeaux…` « ok » |
| 3.11 | 136 ok | 255 | 172 | Ran = 415, conforme |
| 3.12 | 136 ok | 255 | 172 | Ran = 415, conforme |
| 3.13 | 136 ok | 255 | 172 | Ran = 415, conforme |
| 3.12, série sur `b46672b` | 136 ok | 255 | 172 | Ran = 415, conforme |

Aucune ligne « Exception ignored » ni « Warning ».

## Confrontation avec la section « Correction finale du 2026-10-08 17:53 UTC » (lue après mes mesures)

D'accord sur tout : sha256 et lignes du diff, code inchangé, rouge puis vert, série sur les deux têtes, matrice, rien
retiré. Son écart E-9 (premier J09 mal parenthésé, invalidé et refait) ne change pas le résultat : mon J09, à la forme
de ma revue, est tué.

## Écarts

- Aucun. Une note : le SHA256SUMS de corr3 couvre aussi `revue/` (dont mon `RAPPORT-REVUE.md`, `5f66eb98…`, égal au
  mien) ; le dossier `revue/cc/`, créé après lui, n'y est pas : il a son propre `SHA256SUMS`.

**Interdits** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit ouvert, variable scellée jamais posée,
aucune écriture git (tête `b46672b`, statut vide, `.git/HEAD` `e29f8e8d…` et `.git/index` `488e6338…` inchangés), rien
sur Pocket. Copies lourdes supprimées (deux arbres, clone nu, mutants), aucun processus restant.

## Fichiers

Dans `<scratchpad>/s2bis/outillage2/corr3/revue/cc/` : `RAPPORT-CC.md`, `NOTES.md`, `SHA256SUMS`, `outils/`
(lance, lignes, matrice, muter), `mutants/spec_cc.py`, `preuves/` (matrice, tête, mutants et leurs sorties, journaux).
