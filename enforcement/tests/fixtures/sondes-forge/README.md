# Sondes de forge de SHOGEN-S2BIS-ANALYSEUR-RESIDUS-1 (fixtures, lot DETTES-T7)

Écrit le 2026-10-10 à 05:42:11 UTC (`date -u`). Huit workflows de sonde, octets exacts, poussés le 2026-10-10 sur la
branche jetable `essai/analyseur-residus` (commit `84e5363`, accord de l'investisseur) et lus sur la forge (GitHub
Actions) le même jour vers 01:59 UTC ; adjudication de l'orchestrateur du 2026-10-10 02:01:56 UTC (décisions 1 à 4).
Chaque sonde porte un job `s2bis-unittest` dont l'étape du vérificateur est écrite comme dans `gates.yml` ; un leurre
`python3` imprime ce que la forge lance, sans rien lancer. Ce ne sont pas des jobs à la forme K (aucun checkout,
quatre étapes) : elles éprouvent la lecture de la forge, non l'enregistreur. Fixtures des cas du runner
(`run-fixtures-verdict-suite-s2.py`) et des tests de l'enregistreur (`s2-harness/tests/test_oracle_record.py`).

| fichier | forme | sha256 | run | réponse de la forge |
|---|---|---|---|---|
| `sonde-t00-temoin.yml` | témoin | `c10a883d…c981` | 38015225743 | job vert, script du bloc `cde425e5…` |
| `sonde-n12-cle-guillemets.yml` | N-12 | `12afdedc…1d63` | 38015223763 | refusé : clé déjà définie (l.42, col. 3) |
| `sonde-n14-controle-us.yml` | N-14 | `7d562eb3…c517` | 38015224164 | refusé : erreur de syntaxe YAML |
| `sonde-l02-commentaire-set-e.yml` | LC-02 | `08620e5d…ee0a` | 38015224723 | refusé : erreur de syntaxe YAML (l.32) |
| `sonde-l03-etape-avalee.yml` | LC-03 | `03ecfd66…46ad` | 38015225784 | job vert à 3 étapes, vérificateur non lancé |
| `sonde-l08-timeout-600.yml` | LC-08 | `ab293ba8…c1f6` | 38015225738 | job vert, script du bloc `cde425e5…` |
| `sonde-l13-ancre-alias.yml` | LC-13 | `694711eb…ec4f` | 38015225196 | refusé : valeur inattendue (l.8, col. 11) |
| `sonde-an1-ancre-valide.yml` | AN1 | `a7cb180a…eb4e` | 38015225753 | job vert, étape 4 nommée par l'alias |

Sommes complètes : `SHA256SUMS` de ce dossier (sha256 de chaque sonde, égal à celui du plan des sondes). Les messages
exacts de la forge sont dans le dossier de l'épreuve (`messages-refus.txt`, hors dépôt) ; ils sont cités ici en
résumé, jamais entre guillemets.
