# Rapport du générateur de SB-13, première passe (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 00:44:06 UTC du texte rendu par l'agent a761f7e752732d85e (workflow wf_b92ecd95-a7d) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : SB-13, première passe (`oracle_recalc.py`, oracle croisé avec RB-6 ; E-S-51, première moitié)

**Gate 0** : le modèle qui tourne est `claude-opus-5-5` (identifiant exact), worker G1, effort max. Travail du 2026-10-08, de 19:28:48 à 21:09 UTC (`date -u`).

Je n'ai fait aucune écriture git dans `/home/user/shogen`, aucun commit, et rien sous un `.claude/` du dépôt. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Je n'ai ouvert ni `*.jsonl` ni aucune pièce de D.2.

Le rapport complet est dans `<scratchpad>/s2bis/sb13/RAPPORT-GENERATEUR.md` (sha256 `d539ea06…b217`). `SHA256SUMS` couvre les 412 fichiers du dossier (sha256 `37437c3a…cfe`).

## 0. En bref

- **E-S-51, première moitié : tenue.** Les o(r, u) et K^(r) de la réplique sont égaux à ceux de RB-6 :
  - sur les 6 vecteurs du contrat, dont o = 0 et o = n − 1, aux valeurs recalculées par `sha256sum` et `bc` ;
  - sur 100 séries synthétiques à graine fixe : 0 écart, sur 90 180 o(r, u) et 105 714 K^(r) comparés.
- **SHOGEN-SIM-BIS-CONTRAT-RB6-1** : trois tests lient les règles de noms, de seuils et de vecteurs des deux textes. Je propose de fermer l'item ; c'est à toi d'adjuger.
- **Frontière E-S-01** : toujours testée.
- **Mutants** : 49 lancés, 49 tués, 0 vivant, 0 FATAL.
- **Mode strict** (`-X dev -W error`, Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14, sous `PYTHONHASHSEED` 0 et 7) : 8 runs sur 8 verts, aucune ligne « Exception ignored » ni « Warning ». Python 3.10 passe aussi.
- **La base a avancé pendant le lot.** Tu as commis SB-15A…G (`ec83756`…`eb83db6`) puis `5e386c4`. Je n'ai avancé aucune base.
  - Sur `5e386c4`, la série faite sur `5cfe746` ne bute que sur la ligne de plancher de `gates.yml`.
  - Je livre donc une **variante pour 5e386c4** (`diffs-apres-sb15/`), aux planchers 199, 203, 206, 209. Elle s'applique sur une copie de `5e386c4`, ses 4 jobs sont conformes et le mode strict y donne 8 runs sur 8 (Ran 209).

## 1. Diffs

Il y a quatre diffs au lieu de trois. Mon premier découpage faisait +241 lignes de code dans un seul diff ; je l'ai écarté (E-5).

| diff | objet | sha256 (base 5cfe746) | code | plancher |
|---|---|---|---|---|
| SB-13A | épingle (section `oracle_recalc` de `parametres.json` et son schéma dans `commun.py`), `extraire`, 5 tests | `eb399732c37fd93b745f82499f469cfb0966b80aab4815a9f359fc7d214b718e` | +160 −2 | 177 |
| SB-13B | `epingle`, `charger` (shogen_s2bis par importlib, contrôle des modules, cache sur l'épingle, nettoyage), 4 tests | `8f85c7777c4a7073978721f63e3db5deea459ebf8db2dcb596c911d2ee51cd0a` | +116 −6 | 181 |
| SB-13C | `replique`, `recalcul`, `croiser` ; tests d'E-S-51 (vecteurs, 100 séries, sensibilité) | `d5ffed18eacfce9e54c2109d0eb44ab56922a6b8e62877338d16e3e6bcda4953` | +165 −5 | 184 |
| SB-13D | tests de CONTRAT-RB6-1 (noms, seuils, vecteurs) | `354190b879b63ab35128f3302d0860fd75630ada87e000730859799da7f12ed3` | +115 −3 | 187 |

Variante pour 5e386c4 :

| diff | sha256 |
|---|---|
| SB-13A | `eef6803d32a00cf6ac51dc9a62a2059b170572dde473ecaba9bf659e167eae1f` |
| SB-13B | `d736ea70148e122a05f0cb8dcfa5f08c9442a6d11b48defdbfc1d6e4fa26b32d` |
| SB-13C | `d91f51c91a4f46fe867abb2c1d176b78f0a2c1593474bad4304fd28a9edfed9e` |
| SB-13D | `a4c7bb7a6156c384acca269905e10db19173c08bdb5da7d8df653f3a9518e7e5` |

Contrôles sur les diffs :
- aucun octet 92 ;
- aucune ligne de plus de 120 caractères, sauf la ligne `"source"` du JSON (E-7) ;
- la série appliquée sur une copie neuve de 5cfe746 donne exactement l'étape e13d.

## 2. Tableau E-S-51 et CONTRAT-RB6-1

Les lignes renvoient à l'état final, sous `scripts/sim-bis/`.

| exigence | code | test | référence |
|---|---|---|---|
| E-S-01 : adaptateur au commit cité, extrait par git archive | `oracle_recalc.py:38` (`extraire`), `:66` (`charger`) ; `commun.py:102-107` ; `parametres.json:111-120` | `tests/test_oracle_recalc.py:36`, `:42`, `:55`, `:68`, `:118`, `:128`, `:139`, `:152` | commit et 6 empreintes obtenus par `git show f458980:s2bis/<chemin>` puis `sha256sum` |
| E-S-01 : frontière lue par `ast` | `test_fitness.py` inchangé | `tests/test_oracle_recalc.py:88` | — |
| E-S-51 : o(r, u) sur les vecteurs, dont o = 0 et o = n − 1 | `oracle_recalc.py:123` (`croiser`) | `tests/test_oracle_recalc.py:220` | 107527, 24225, 39743, 0, 6, 52807 (`sha256sum` et `bc`) |
| E-S-51 : K^(r) sur les vecteurs | `oracle_recalc.py:100` (`replique`), `:114` (`recalcul`) | `tests/test_oracle_recalc.py:220` | K^(r) = S^(r) = 1 ou 0, calculés à la main |
| E-S-51 : 100 séries synthétiques | `oracle_recalc.py:123` | `tests/test_oracle_recalc.py:235` (générateur `:182`) | couverture comptée : R = 99 / 999 / 9 999 → 90 / 8 / 2 ; première unité None 20 fois, absente de BTC 20 fois |
| sensibilité de l'oracle | `oracle_recalc.py:123` | `tests/test_oracle_recalc.py:254` | neuf clés écrites à la main |
| CONTRAT-RB6-1, noms | `regle.py:25`, `:28`, `:130` comparés à `rotation.HOTE` | `tests/test_oracle_recalc.py:299` | 38 caractères admis sur 1 114 112 ; 57 admis sur 159 noms d'essai |
| CONTRAT-RB6-1, seuils à chaque R | `regle.py:102`, `:207` comparés à `config_analyse` et `analyse.json` | `tests/test_oracle_recalc.py:329` | 99 à R = 9 999, 9 à R = 999 ; 100 R admis de 1 à 9 999 ; R = 9 998 et R de 10 000 à 10 099 refusés des deux côtés ; gardes égales |
| CONTRAT-RB6-1, vecteurs et même chaîne hachée | vecteurs de `test_regle.py` et de `s2bis/tests/test_rotation.py` (épinglé) | `tests/test_oracle_recalc.py:372` | empreintes entières de `sha256sum`, à n = 2^256 |

## 3. Rouges et mutants

**Rouges.** Chacun est montré avec une ébauche du code (contrôles retirés). Aucun ne compte d'ERROR :

| diff | ébauche | FAIL |
|---|---|---|
| SB-13A | extraction sans ses contrôles | 2 |
| SB-13B | chargement sans ses contrôles | 3 |
| SB-13C | réplique nulle, o non comparés | 3 |
| SB-13D | divergences historiques de SB-8c (noms) et SB-7b (seuil) | 8, dont `test_noms` et `test_seuils` |

**Mutants.** Ils sont classés par la commande du job, avec une limite de 300 s :

| diff | mutants | tués |
|---|---|---|
| SB-13a | 12 | 12 |
| SB-13b | 10 + 2 en complément | 12 |
| SB-13c | 13 | 13 |
| SB-13d | 12 | 12 |

Deux remarques :
- **M-13B-01** est tué parce que le module de tests ne se charge plus, et non par le test qu'il visait. Les deux compléments M-13B-11 et M-13B-12 visent ce test et le rougissent.
- **Correction C-1.** Le test de sensibilité lisait les clés attendues dans `oracle_recalc.CLES`, donc dans le code même qu'il vérifiait. Je les ai écrites à la main, puis j'ai régénéré les étapes et relancé les campagnes 13c et 13d.

## 4. Matrice et planchers

| contrôle | résultat |
|---|---|
| runner du vérificateur | 136 ok |
| sim-bis (aussi sous `unshare -n`) | 187, conforme |
| s2bis | 255, conforme |
| S2 | 415 OK (2 sauts), conforme |
| hooks / model-pinning / secrets | 54 / 227 / 147 ok |
| gate-secrets | OK |
| R-13 | 0 constat |
| `cargo --locked xtask verify` | identique entre série et base : S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE, la violation déjà connue sur copie (`docs/17-modele-de-menace.md:70`) |
| coût en CI | la suite sim-bis passe d'environ 24 s à environ 28 s |

Planchers du job sim-bis :
- sur 5cfe746 : 172 → 177 → 181 → 184 → 187 ;
- sur 5e386c4 : 194 → 199 → 203 → 206 → 209.

Les planchers de s2bis (255) et de S2 (415) ne changent pas.

## 5. Questions (mon choix est appliqué, à adjuger)

- **Q-SB13-1.** Le point 1 du brief demande l'épingle dans `parametres.json`, mais la liste des fichiers autorisés ne contient que `oracle_recalc.py`, son test et le plancher.
  - J'ai mis la section dans `parametres.json` et son schéma dans `commun.py` (E-S-03), à des endroits que SB-15 ne touche pas.
  - Mesuré : le seul conflit restant est la ligne de plancher de `gates.yml`.
- **Q-SB13-2. Commit cité : `f458980`**, le dernier commit qui touche le code ou le contrat de RB-6. Les six fichiers ont les mêmes octets à `e6d201a`, `f5915a5` et `5cfe746`.
  - J'écarte le commit de RB-6b (`e66f9f3`). Mesuré avec une épingle à ce commit : `test_noms` en ERROR (il n'y a pas encore `HOTE`) et `test_seuils` en FAIL.
- **Q-SB13-3. Ce que l'oracle compare** : o, K, S, K^(r), S^(r), C, C1, C_S, K_crit et la moyenne de K.
  - S_crit et S_moyen ne sont pas comparés (avis de la tranche 3, P-5).
  - Pour RB-6, C1 est calculé avec `resume`, à partir du k_crit lu dans `analyse.json`.
- **Q-SB13-4. Périmètre de l'extraction** : six fichiers épinglés, pas seulement `rotation.py`.
  - En plus : `config_analyse.py` et `analyse.json`, qui portent les règles de seuil de RB-6.
  - Et `tests/test_rotation.py`, lu comme texte et jamais exécuté, qui porte les vecteurs de RB-6.
  - Sans eux, CONTRAT-RB6-1 ne peut pas lier les seuils et les vecteurs.
- **Q-SB13-5. Forme des 100 séries.**
  - Une « série » est une entrée complète {classe : {unité : masque}}, tirée d'un flux SHA-256, sans module `random`.
  - R vaut 99, 999 ou 9 999 selon la répartition 90 / 8 / 2. Le test prend 1,7 s, contre environ 14 s si tout tournait à R = 999.
- **Q-SB13-6. L'item SHOGEN-S2BIS-HOTE-COMMUN-1** (annexe B l.1113) a pour déclencheur « brief de SB-13 », mais le brief ne le nomme pas.
  - Mes tests lient deux des trois textes de la règle des noms (SIM-BIS et le recalcul). Le troisième, `collecte/entree.py` l.25, reste hors du test.
  - Je peux l'ajouter si tu le veux : une ligne d'épingle et environ 5 lignes de test.
- **Q-SB13-7. README de `scripts/sim-bis` non modifié** (liste des fichiers autorisés, et risque de conflit avec SB-15). La ligne à ajouter est rédigée au §8 du rapport complet.

## 6. Écarts

- **E-1.** Un octet 92 écrit dans l'outil `vecteurs.sh`, réécrit par gabarit ; les valeurs sont restées identiques.
- **E-2.** Dans SB-13a, j'ai écrit le module avant ses tests ; le rouge a ensuite été montré par ébauche.
- **E-3.** Des barres obliques inverses tapées dans des heredocs Python, plus une barre d'échappement dans le rapport. J'ai contrôlé les octets : 0 octet 92 dans les fichiers du lot, les diffs et le rapport.
- **E-4.** Deux octets 92 voulus dans l'outil `rouges_jobs.sh`, contrôlés.
- **E-5.** Le découpage en trois diffs (+241 lignes dans l'un) a été écarté.
- **E-6.** J'ai lancé un `git grep` borné au dossier `s2bis/shogen_s2bis/collecte/` (ni `docs/`, ni le dépôt entier) pour trouver le troisième texte de la règle des noms.
- **E-7.** La ligne `"source"` du JSON dépasse 120 caractères ; c'est la forme de toutes les `source` du fichier.

## 7. Items et limites

- **SHOGEN-SIM-BIS-ORACLE-RB7-1 reste ouvert.** La seconde passe devra déplacer l'épingle sur le commit de RB-7, comparer la valeur de la règle, prendre la première unité calculée par RB-7 et la table des identifiants.
- **L-1.** `replique` appelle `regle._entrees`, une fonction privée du moteur. Si l'intérieur de `regle` change, l'oracle échoue de façon visible.
- **L-2.** Le test des vecteurs lit la structure de `test_regle.py`. Une refonte de ce test casse le lien de façon visible.
- **L-3.** L'égalité des seuils suppose α = 1/100.

Fichiers utiles, dans `<scratchpad>/s2bis/sb13/` :
- RAPPORT-GENERATEUR.md
- NOTES.md
- SHA256SUMS
- diffs/
- diffs-apres-sb15/
- etapes/
- journal/