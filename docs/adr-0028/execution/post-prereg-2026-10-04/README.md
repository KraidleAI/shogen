# Sorties du lot POST-PREREG : analyses ajoutées après le pré-enregistrement, hors décision (2026-10-04)

Chaque fichier porte en première ligne : « ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict
de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3) ». Aucun ne remplace une valeur des rendus versés
(`../rendu-2026-10-04/`). Rattachement : `docs/adr-0028/G0-lots-DETTES.md`, ligne POST-PREREG ; synthèse :
`docs/11-mesures-pilotes.md` §11.1.

Produits dans la session cloud le 2026-10-04, entre 04:59 et 05:31 UTC, par les scripts de `scripts/post-s2/`
(`python3 -B <script> [<analyse>] --journaux <dossier des journaux scellés> --sortie <fichier>`, variable
`SHOGEN_S2_CAMPAGNE_CONTROL` non posée), sur les journaux scellés désignés par leurs sha256 (bloc machine du paquet,
l.217-219 ; rappelés en tête de chaque fichier). Les journaux ne sont pas versés. Chaque fichier porte aussi le sha256 du
script et de `commun.py` qui l'ont produit, le sha256 du rendu J28 et le contrôle de cohérence contre son bloc 3 (n, K,
P̂_more par strate, chaîne pour chaîne). Paramètres fixés avant toute exécution sur les journaux (journal G1 du worker,
2026-10-04 04:18:36 UTC).

Version du harnais : les scripts importent `s2-harness/shogen_s2` (`r1`, `records`, `window`, `r2`), dont dépendent
toutes les valeurs ; les en-têtes portent le sha256 des scripts et de `commun.py`, pas celui de ces modules. Les sorties
ont été produites avec le harnais du commit d'analyse `f35a70c` (bloc machine du paquet, `commit_analyse`) :
`s2-harness/shogen_s2` et `s2-harness/tools` sont identiques à `f35a70c` aux têtes `5afbdd2` (production des sorties),
`3e275a2` (rejeu de la relecture G2, sorties identiques à l'octet) et `52b9b4e`. Un rejeu se fait à cette version : par
exemple, scripts de ce lot et `s2-harness/` tiré de `f35a70c` (`git archive f35a70c s2-harness`) dans une même copie.
Depuis `0221a74` (lot DETTES-B1), `s2-harness/shogen_s2` diffère de `f35a70c` (entre autres, `r1.parse_journal` refuse
par une erreur nommée un prix illisible ou hors contexte).

| fichier | item(s) de l'annexe B | commande |
|---|---|---|
| `quasi-mort.txt` | SHOGEN-FLUX-QUASI-MORT-1, SHOGEN-QUASI-MORT-PREDICAT-1, SHOGEN-POOL-MIN-1 | `sens_pool.py quasi-mort` |
| `deviant.txt` | SHOGEN-FLUX-DEVIANT-1 | `sens_pool.py deviant` |
| `poolee-bloc.txt` | SHOGEN-POOLEE-BLOC-1 (a) | `poolee_bloc.py` |
| `hote-degrade.txt` | SHOGEN-HOST-DEGRADED-2 | `hote_horloge.py hote` |
| `horloge-etendue.txt` | SHOGEN-HORLOGE-ETENDUE-1 | `hote_horloge.py horloge` |
| `censure.txt` | SHOGEN-CENSURE-INFO-2 | `censure.py` |
| `sigma-indep.txt` | SHOGEN-SIGMA-BLOC-INDEP-1 | `sigma_indep.py` |
| `influence.txt` | SHOGEN-DEP-FENETRES-2 (b) et (c), SHOGEN-R1-PLUGIN-1 (a) et (b) | `influence.py` |
| `contenu.txt` | SHOGEN-CONTENU-DEP-1 | `contenu.py` |

Sommes : `SHA256SUMS` (format de `sha256sum`).
