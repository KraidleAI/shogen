# Contre-contrôle bref de CC2-1 et CC2-2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 14:04:45 UTC du rapport rendu par message par le réviseur G2 (agent a2fb4f197970d4d60) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

**Gate 0 :** je tourne sous `claude-opus-5-5`.

# Contre-contrôle bref de CC2-1 et CC2-2 : **CONFORME**

J'ai lu l'horloge (`date -u`) à 13:54:17 au début et à 14:03:45 à la fin.

**Base.**
- SHA256SUMS de corr3 : 133 OK. Diffs recalés neufs : 20 OK (c80d92bc).
- J'ai recalculé les arbres dans mon propre clone nu : série 2d180042, puis r 0faf158e, s 6c24f32b, t e81e24a3 et u **176ab70e**, comme annoncé.
- L'extraction de u avec les exclusions donne 02c3baa5.

## 1. CC2-2 : conforme
- **Régénération.** J'ai régénéré les deux outils de recalage dans mon dossier, avec des copies dont les sorties sont redirigées : je n'ai rien écrit dans `cb18/rebase`.
  - v1 redonne exactement les anciens diffs (somme eb39992b) et l'arbre f342a14b.
  - v2 redonne les 20 diffs publiés, octet pour octet, et l'arbre 2d180042.
- **Ancien contre neuf, ligne à ligne :** **49 nombres décalés de 42**, mon compte exact, et rien d'autre ne bouge.
- **Neuf contre les originaux :** seuls changent le plancher de `gates.yml` et ces 49 valeurs de METRIQUES.
- **Commit par commit :** la section METRIQUES de chaque diff cite le plancher du `gates.yml` du même état, de 159 (a) à 183 (q).
  - k, l et m ne citent aucun plancher ; ENREG-ROLE n'a pas de section.
  - CB-18f cite aussi 170, son premier passage historique (128 + 42), qui reste cohérent.
- Les autres nombres de 114 à 141 encore présents dans ces sections sont des comptes de lignes, des durées en µs ou un préfixe de commit, jamais un compte de la suite.
- **Note E-7 retirée de r.** C'est la seule différence entre les diffs r, s et t de corr3 et ceux de corr2 ; le code est identique.

## 2. CC2-1 : conforme
- **CB-18u applique mon remède tel quel :** les trois `name` suivent `[0-9A-Za-z].*` et `timeout-minutes` suit `[1-9][0-9]*` ; aucun octet 92 n'est ajouté.
- **Rouge puis vert.** J'ai remis le GABARIT de t dans le runner de u : 72 ok et **5 échecs**, exactement L-35, L-36, G-02, G-03 et G-04. Avec u tel quel : **77 ok**.
- **Aucun cas affaibli de t à u :** V, E et C sont identiques, les 72 identifiants sont gardés et leurs libellés n'ont pas changé ; 5 cas sont ajoutés. CA-01 à CA-12 : 12 tués sur 12 par la commande du job sur u.
- **Leurres, avec mes outils sur u.** Mes fichiers régénérés sont identiques à ceux du worker. Ne passent que **N-12, N-14, LC-02, LC-08, LC-09 et LC-10** ; le runner réel de u le confirme (77 ok sur ces six, 76 ok et K-02 en échec sur LC-01, LC-03, LC-07 et LC-13).
- **LC-08 : j'accepte l'adjudication.** `timeout-minutes: 600` n'a pas d'effet sur ce que K certifie, comme je l'avais classé. LC-13 refusé est plus strict, et c'est mieux ainsi.
- **LC-09 et LC-10, mesurés cette fois.** Dans ma première relecture, je n'avais fait que le déduire. Par la commande du job : sortie 127 pour LC-09 (`python3: command not found`), sortie 3 pour LC-10 (`arguments illisibles … '184\xa0'`). La gate reste fermée, et le point « [2nd] » du worker est levé.

## 3. Arbre final 176ab70e : conforme
- **Jobs** (borne de 300 s, réseau isolé) : s2bis Ran **184** sous 3.10, 3.11, 3.12 et 3.13 ; S2 **406** avec `--egal` ; sim-bis **129** ; runner 77 ok.
- **`-X dev -W error`** : 184 OK sous les quatre versions, 0 avertissement.
  - Le module `test_oracle_record` entier a sous 3.10 un échec déjà connu (PY310-1, `test_enregistrement_champs_et_sha`), identique depuis e9.
  - Le « OK ×4 » du worker ne porte que sur le test neuf ; il est exact dans cette portée.
- **xtask :** les verdicts sont identiques à ceux de 9b21c597 et de f342a14b : S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE pour `docs/17:70` seul (connu).
- **R-13 :** 0 occurrence sur les 2 565 lignes ajoutées des 24 diffs ; contrôle positif 2 sur 2.
- **Octets 92 :** 0 ajouté dans les 24 diffs ; 1 retiré dans r, comme déclaré. Aucun import neuf.

## Journal G1
- **[lu] :**
  - rapport du worker cf582a19 (entier) ; outils de recalage v1 0d4431f3 et v2 ff254c50 (comparés ligne à ligne) ;
  - diff u (entier) ; METRIQUES de u (section u, puis les 20 sections par grep) ;
  - preuves du worker : `final3/final-xdev-role-*` et `verif_finale3.sh` l.35.
- **[abs] :** `lecteur.py`, pièces D.2, tout `*.jsonl`, dossiers exclus, comportement YAML de la forge.
- **PID réel :** 30594 (terminé). Aucune écriture git dans le dépôt : un clone nu `--shared` et les copies de régénération, tous dans mon dossier.
- **Nettoyage :** copies, clones et cible cargo supprimés.

## Fichiers
- `<scratchpad>/s2bis/cb18/cc3/SHA256SUMS` (119 entrées, 119 OK, sha256 63a01c35…)
- `<scratchpad>/s2bis/cb18/cc3/travail/preuves/` :
  - `compare-v1-v2.txt`, `coherence-metriques-gates.txt`, `compare-corr2-corr3.txt`, `arbres-rstu.txt` ;
  - `rouge-vert-u.txt`, `leurres-u.txt`, `leurres2-u.txt`, `leurres-runner-reel-u.txt`, `lc09-lc10-execution.txt` ;
  - `verif-u.log`, `xtask-u-verdicts.txt`, `mutants-CA-u.txt`.
- `<scratchpad>/s2bis/cb18/cc3/travail/regen-v1/` et `regen-v2/` (diffs régénérés)
- `<scratchpad>/s2bis/cb18/cc3/travail/NOTES-CC3.md`
