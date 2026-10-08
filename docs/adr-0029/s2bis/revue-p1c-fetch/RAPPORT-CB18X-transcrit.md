# Rapport du worker — CB-18x (CC4-1) de P1 tranche C (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 16:27:56 UTC du rapport rendu par message par le worker (agent aa9c3df62627c22da) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0** : le modèle résolu est `claude-opus-5-5` (préfixe conforme).

## CB-18x (CC4-1) : fait, posé après CB-18w

1. **Ce que contient le diff.** Deux cas, et aucune ligne de code du gabarit ne change :
   - L-43 « job sim-bis, fetch-depth: 0 à l'indentation 8 (égalité exacte, CB-18x) » : refusé ;
   - L-44 « job sim-bis, fetch-depth: 0 après le nom de l'étape du runner (place exacte, CB-18x) » : refusé.

   Les deux libellés tiennent sous 120 caractères et ne mentionnent pas le POC. La docstring du module reçoit une phrase, et METRIQUES une section CB-18x.
2. **Rouge.** Sur l'état w (tête, v, SIM-T4, w), le runner de w sans les deux cas donne 83 ok sous MV-01 comme sous MV-02 : les deux mutants vivent.
   - J'ai pris MV-01 et MV-02 tels quels, par runpy, dans une copie du fichier du réviseur (a98af3cb).
3. **Vert.**
   - Avec CB-18x, le runner donne **85 ok** sur la tête plus v, SIM-T4, w et x.
   - Sous MV-02, seul L-43 échoue ; sous MV-01, seul L-44 échoue.
4. **Deux mutants neufs à moi, lancés par la commande du job s2bis** (témoin Ran 184) :
   - M-18x-01, qui cherche la ligne de b[7] à b[9], n'est tué que par L-44 ;
   - M-18x-02, qui admet n'importe quelle indentation (regex), n'est tué que par L-43.

   Lancés de la même façon, MV-01 et MV-02 sont tués, et les 6 mutants de CB-18w, rejoués, aussi.
5. **Leurres du réviseur.** `leurres_cc`, `leurres_cc2` et `leurres_fetch` donnent les mêmes verdicts sur w et sur x. F-01 à F-07 sont refusés par K-03.
6. **Contrôles.**
   - CB-18x compte code +8/−3 et docs +25. Les lignes retirées sont la docstring re-coupée et la parenthèse de fin de L-42.
   - 0 octet 92 ; aucune ligne de plus de 120 caractères ; R-13 : 0 occurrence ; secrets en index : sortie 0.
   - Job s2bis : Ran 184 sous python3.10 à 3.13. S2 : 406. Crochets : 54 ok.
   - Runner sous 3.10 à 3.13 en `-X dev -W error` : 85 ok, 0 avertissement.
   - xtask : identique au témoin de la tête. Seule violation : S-G9 `docs/17:70`.
7. **Preuve d'arbre.**
   - J'ai reconstruit les états à partir de la base ; ils retombent sur les mêmes arbres (tête 1b01b83b, w c0f20e9c).
   - CB-18x s'applique avec 0 décalage.
   - Copie hors exclusions : **cd873376**.
   - Arbre complet : 5bbd1bc3 → v 65d37cd0 → SIM-T4 a33f919d → w caf39a0e → x **fe319805**.
8. **Livrables.**
   - `corr4/diffs/CB-18x.diff` : sha256 2731041083cc5bd5895f1e926d6450d90730aedbfaf5c9e54498d240cc7c708a.
   - CB-18v (8db2bfc9) et CB-18w (15ec5079) sont inchangés.
   - `corr4/SHA256SUMS` : 033561ff…, 134 sur 134 OK.
9. **État final.** Le dépôt est à HEAD 98c8537, `git status` vide. corr2, corr3 et cc4 sont intacts. Le nettoyage est fait. Le PID réel de la vérification était 15853, et il est terminé.

## Journal G1

- **Lus** [lu] : `cc4/CONTRE-CONTROLE-4-CB18-transcrit.md` (230539cd) ; `poc-cc4-1.diff` (ec09417a) et `.txt` ; `mutants_cc4.py` (a98af3cb) ; en-tête de `leurres_fetch.py` (2c0462b2).
- **Horloge** (`date -u`) : 16:19:07 au départ, 16:27:22 à la fin.

Tout est dans `<scratchpad>/s2bis/cb18/corr4/` :
- `diffs/CB-18x.diff`
- `metriques/x.md`
- `mutants/` : mutants_cb18x.py, mutants_mv.py
- `preuves/` : rouge-CB-18x-sans-cas.txt, vert-CB-18x-mutants.txt, campagne-x-*.txt, verif-serie-x.txt, verif-x.log, x/
- NOTES.md
- SHA256SUMS
