# Contre-contrôle bref cc4 de CB-18v et CB-18w (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 16:18:31 UTC du rapport rendu par message par le réviseur (agent a2fb4f197970d4d60) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 :** je tourne sous `claude-opus-5-5`.

# Contre-contrôle bref cc4 de CB-18v et CB-18w : **NON-CONFORME**, liste fermée **CC4-1** (mineur, remède prêt)

J'ai lu l'horloge (`date -u`) à 16:08:56 au début et à 16:17:19 à la fin.

**Pièces.** SHA256SUMS de corr4 : 92 OK (e64ebccd). Diffs : v 8db2bfc9, w 15ec5079. Sommes de sim4 et de sim4/corr : 13 diffs OK.

**Le point CC4-1 seul fait obstacle.** Tout le reste est conforme, y compris l'ordre de commit et I-1.

## 1. Application et arbres : conformes
- J'ai appliqué la série dans un index privé, sur 98c8537 (arbre 5bbd1bc3) :
  - v : 0 décalage, arbre 65d37cd0 ;
  - SIM-T4 (13 diffs, SB-14H compris, comme le worker) : arbre a33f919d ;
  - w : 0 décalage, arbre **caf39a0e**.
- La copie hors exclusions donne **c0f20e9c**, comme annoncé.
- E-4 confirmé : 15 hunks décalés de 2 lignes, tous dans `gates.yml`.

## 2. Runner : conforme
- **Comptes par état :** 77 ok à la tête, 82 après v (sans SIM-T4 comme avec), 83 après w. La tête plus SIM-T4 sans v donne 76 ok et K-03 en échec.
- **Rouges reproduits :**
  - le runner de v avec le gabarit de la tête fait échouer L-37 (81 ok) ; s'y ajoute K-03 avec SIM-T4 ;
  - le runner de w avec le gabarit de v fait échouer L-42 (82 ok) ;
  - w posé sans SIM-T4 fait échouer K-03 : l'ordre v, SIM-T4, w est nécessaire.
- **Mutants du worker, par la commande du job s2bis :**
  - v, 5 sur 5, chacun tué par son cas : L-39, L-38, L-37 (avec K-03), L-40, L-41 ;
  - w, 6 sur 6 : L-42 ; K-01, K-02, L-00 et L-39 ; L-38 ; L-40 ; L-41 ; L-38.
- **E-2 :** M-18r-04 est tué, **par L-29**.
- **Aucun cas retiré ni affaibli.** V, E et C sont identiques, les 77 identifiants sont gardés et leurs libellés n'ont pas changé ; 6 cas sont ajoutés. Les lignes retirées sont des docstrings, la ligne `if` de v (remplacée par l'exigence de w) et la parenthèse de fin de L-41.

## 3. Gabarit : conforme
- La ligne n'est lue que pour `sim-bis-unittest`, à b[7] (juste après `persist-credentials: false`), et elle doit y être identique à la lettre.
- **7 leurres neufs** sur cette ligne, tous refusés par K-03 sans toucher K-01 ni K-02 : `"0"` entre guillemets, ligne suivie d'un commentaire, ligne répétée, indentation 8, ligne après le nom de l'étape du runner, `00`, ligne absente.
- Les jobs s2bis et S2 de `gates.yml` sont identiques entre la tête et w. Seul le job sim-bis change : commentaires, la ligne, plancher 129 → 172.
- **Mes 33 leurres** (`leurres_cc.py`, `leurres_cc2.py`) donnent les mêmes verdicts sur la tête et sur w : seuls passent N-12, N-14, LC-02, LC-08, LC-09 et LC-10. N-20 reste refusé par K-03.

## 4. Mes mutants neufs, par la commande du job s2bis : CC4-1
- **Tués :** MV-03 (une ligne de trop retirée ; tué par K-03, L-37 et L-40) et MV-04 (toute valeur numérique admise ; tué par L-38).
- **VIVANTS : MV-01 et MV-02.** Ils ne sont pas équivalents :
  - **MV-01** admet aussi la ligne après le nom de l'étape du runner. Mon leurre F-05 le distingue.
  - **MV-02** compare la ligne après `strip()`, ce qui relâche indentation et espaces. Mon leurre F-04 (indentation 8) le distingue.
- **Portée :** ces deux formes ne peuvent pas donner un faux vert.
  - Pour PyYAML, F-05 est du YAML invalide.
  - F-04 fait de `fetch-depth` une clé de l'étape, que le schéma de la forge refuserait [abs].
  - Mais l'« égalité exacte, à la place exacte », écrite dans le docstring, n'est fixée par aucun cas.
- **Remède prêt** (`preuves/poc-cc4-1.diff`) : deux cas.
  - **L-43** : la ligne à l'indentation 8.
  - **L-44** : la ligne après le nom de l'étape du runner.
  - Résultat : 85 ok. Sous MV-02, seul L-43 échoue ; sous MV-01, seul L-44 échoue. Sans ces cas, w plus chacun des deux mutants donne 83 ok.
  - Le libellé de L-44 est à replier sous 120 caractères.
- Si l'orchestrateur préfère ne pas ajouter ces cas, il faut au moins inscrire ces deux formes au résidu de validité.

## 5. Règles de forme et xtask : conformes
- **Octets 92 :** 0 ajouté et 0 retiré, dans v comme dans w.
- **R-13 :** 0 occurrence sur 101 lignes ajoutées ; contrôle positif 2 sur 2.
- **Largeur :** 118 caractères au plus. `awk` compte en octets et signale à tort une ligne accentuée par diff.
- **Code ajouté :** +31 lignes dans v, +13 dans w, donc sous 200.
- **xtask :** S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE pour `docs/17:70` seul. Les verdicts sont identiques aux témoins de cc3.

## 6. Jobs sur l'état final, sous `isole.sh` : conformes
- s2bis : Ran **184** sous 3.10, 3.11, 3.12 et 3.13, runner à 83 ok. S2 : **406**.
- `-X dev -W error` : s2bis 184 OK sous les quatre versions, 0 avertissement. Le module de l'enregistreur de rôle a sous 3.10 un échec déjà connu (PY310-1).
- **I-1 confirmé.** J'ai donné les objets git à la copie (alternates, dans mon dossier seulement) : le job sim-bis lance 172 tests et seul `test_g0_mesure` échoue (a216a953 attendu, d9cffc0a trouvé). Sans historique, il y a en plus 2 erreurs `ORACLE/extraction` : c'est l'échec fermé prévu.

## Journal G1
- **[lu] :**
  - rapport du worker 08f860cf (entier) ; diffs v et w (entiers, lignes retirées relues) ;
  - mutants du worker (v, w, rejeu de r) et `serie_sim4.sh` ;
  - les jobs de `gates.yml` (tête et w), le runner (tête, v et w) ; `oracle_r1.py`, l.44-52.
- **[abs] :** pièces D.2, tout `*.jsonl`, dossiers exclus, `lecteur.py`, comportement de la forge.
- **PID réels :** 11090 et 17923, terminés.
- **Aucune écriture git dans le dépôt :** un clone nu `--shared` et un `.git` à alternates, tous dans mon dossier, puis supprimés. La copie est revenue à c0f20e9c.
- **Nettoyage :** copies, clone, cible cargo et TMP supprimés.

## Fichiers
- `<scratchpad>/s2bis/cb18/cc4/SHA256SUMS` (54 entrées, 54 OK, sha256 ae5c1a30…)
- `<scratchpad>/s2bis/cb18/cc4/travail/preuves/` :
  - `arbres-serie.txt`, `runners-etats.txt`, `rouges-v-w.txt` ;
  - `mutants-v-sur-vs.txt`, `mutants-w-sur-w.txt`, `mutants-r04-sur-w.txt`, `mutants-cc4-sur-w.txt` ;
  - `leurres-fetch-w.txt`, `poc-cc4-1.diff` et `.txt` ;
  - `verif-w.log`, `xtask-w-verdicts.txt`, `job-w-sim-bis-avec-git.txt`.
- `<scratchpad>/s2bis/cb18/cc4/travail/outils/` (`mutants_cc4.py`, `leurres_fetch.py`, `verif_w.sh`…)
- `<scratchpad>/s2bis/cb18/cc4/travail/NOTES.md`
