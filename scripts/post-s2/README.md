# Analyses ajoutées après le pré-enregistrement (lot POST-PREREG), hors décision

Rattachement : `docs/adr-0028/G0-lots-DETTES.md` (ligne POST-PREREG) ; items de l'annexe B d'ADR-0028, nommés dans la
docstring de chaque script. Aucune de ces analyses n'entre dans la règle scellée ni ne remplace une valeur des rendus
versés (`docs/adr-0028/execution/rendu-2026-10-04/`) ; le verdict reste celui du rendu J28 (« R1 discrimine » = FAUX,
`docs/11-mesures-pilotes.md` §3).

- `commun.py` : lecture des journaux par les lecteurs du harnais (mêmes appels que `r1.recompute_from_journal`, portée
  du J28 : t0, n fixe 38 600, plage D5 exclue), étiquette de tête, provenance (sha256 du script et des journaux),
  contrôle de cohérence contre le bloc 3 du rendu J28 (n, K, P̂_more par strate, chaîne pour chaîne ; en écart, aucune
  valeur d'analyse, code 1).
- Chaque script d'analyse : `python3 -B <script>.py --journaux <dossier des journaux scellés> --sortie <fichier>` ; la
  sortie ne contient que des comptes et des statistiques, jamais une ligne de journal. Les journaux ne sont pas versés.
- Tests sur fixtures seulement (annexe D.4 a), depuis ce dossier :
  `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .`
