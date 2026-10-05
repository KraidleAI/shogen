# Contre-contrôle bref de SB-8H (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 10:49:12 UTC du rapport rendu par message par le réviseur G2 (agent a388ef21916294a7b) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

claude-opus-5-5

# Contre-contrôle bref de SB-8H (correction de CC-1) : CONFORME

Les quatre points demandés tiennent.

- **Horloge** (`date -u`) : 2026-10-05, de 10:44:14 à 10:48:45 UTC.
- **Dépôt** : tête f5915a5, arbre propre. Aucune opération git en écriture.
- **Diff** : `cc1/SB-8H.diff`, sha256 016a7ccd…, correct. `cc1/SHA256SUMS` (52cdb92f…) : 95 sur 95 OK.
- **Application** : copie de f5915a5 avec les 7 exclusions. Les 13 diffs de la série, puis SB-8H, passent `git apply --check` puis `git apply`, sans fichier .orig ni .rej. L'état avant SB-8H est égal à c8g.

## Les quatre points
1. **X-01 et S-8H-01 sont tués par la commande du job.**
   - Commande : runner, puis ligne de `gates.yml`, borne 300 s ; 0 FATAL.
   - Le témoin non muté est vert (24,0 s).
   - X-01 est tué en 24,3 s, S-8H-01 en 25,8 s, tous deux par `test_oracle_frontiere_c_s_t_reg_2`.
   - La copie de X-01 du worker est identique à la mienne, comparée par programme.
   - Mon prototype de frontière, rejoué sur SB-8H : 4 cas sur 4 OK.
2. **Docstring de `Couche`** : identique une fois les blancs retirés.
   - Le reste du module est identique, arbre `ast` comparé avec cette docstring vidée.
   - 3 lignes changent ; aucune ne dépasse 120 caractères.
3. **Plancher exact 129** :
   - runner 33 sur 33, puis la ligne du job : sortie 0, Ran 129 ;
   - la même ligne, lancée sous Python 3.10, 3.11, 3.12 et 3.13 : Ran 129, conforme 4 fois sur 4.
4. **R-13 et octets 92** :
   - R-13 (motif lu dans `gates.yml`) : 0 constat sur les 19 fichiers de `scripts/sim-bis` et sur les 27 lignes ajoutées ;
   - aucun octet 92, ni dans le diff ni dans le lot final ;
   - taille : code +27 −4, sous la limite de 200 lignes.

## Mon écart
Dans mon rapport précédent, j'ai nommé le prototype `outils/proto_corrections_cc1.py`. Le fichier réel est `outils/proto_cc1.py`, comme le worker l'a relevé. Le contenu cité était bien le sien.

## Preuves
- Fichiers `c8h-*` de `<scratchpad>/s2bis/sim3/g2/rev/sorties/`.
- `SHA256SUMS` de `rev/` : 0de1e191…, 130 sur 130 OK.
- Copies supprimées.
