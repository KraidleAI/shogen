# Brief — outillage de preuve, trois items « avant la G2 de P2 » (SHOGEN-S2BIS-RUNNER-REJEU-1, SHOGEN-S2BIS-ENREG-ANCRE-1, SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/outillage2/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu (reprise depuis lui, jamais depuis un `.jsonl`).

## Base et contrat
- Tête **e6657dc** de `claude/compassionate-noether-szmdyj` (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).
- Rattachement : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` ; annexe B, bloc **B.73** (fin de `docs/adr-0028/ANNEXE-B-items.md` : lis B.73 seulement, et B.71/B.72 si un renvoi l'exige) ; pièces de la réserve R-1 `docs/adr-0029/s2bis/revue-r1/` (BRIEF-R1.md, RAPPORT-R1-transcrit.md, CONTRE-CONTROLE-R1-transcrit.md : leurres D4 à D7, observations O-1 et O-2).
- Fichiers : `enforcement/tests/run-fixtures-verdict-suite-s2.py` (runner, 97 cas), `enforcement/verdict-suite-s2.py` (vérificateur), `s2-harness/tools/oracle_record.py` et `s2-harness/tests/test_oracle_record.py` (enregistreur), `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (si la règle d'usage y va), `.github/workflows/gates.yml` (lignes des jobs, à ne changer que si nécessaire).
- Planchers actuels : suite s2bis 255, runner 97 cas, S2 407, sim-bis 172.

## À faire (liste fermée)
1. **RUNNER-REJEU-1.** Mesuré (D7) : un module sans code de vérification qui rejoue un transcript capturé du canal fait sortir le runner en 0. (a) Écris dans la docstring du runner la garantie réelle (« sortie 0 seulement si les cas ont été joués et jugés sur le canal », pas « les réponses viennent du code relu ») et sa limite (un vérificateur qui reconnaît `--serveur` peut répondre juste au runner et mentir au job ; la lecture humaine du diff du vérificateur reste nécessaire). (b) Ferme le rejeu : nonce imprévisible par requête renvoyé dans la réponse, ou refus d'une réponse disponible avant sa requête, ou toute construction équivalente ; écris ton choix et sa raison (Q-n). Leurre D7 rejoué : sortie non nulle, refus nommé. D4, D5, D6b restent refusés ; D6a reste sans effet.
2. **ENREG-ANCRE-1.** Écris la règle d'usage de l'enregistreur (au FORMAT ou dans un README de l'outil, à toi de motiver) : la comparaison des vérificateurs ne vaut que si l'outil tourne depuis un arbre dont le vérificateur a été relu ; lancée depuis l'arbre relu lui-même, elle est triviale. Si une garde mécanique simple et juste existe (par exemple consigner l'arbre d'où l'outil tourne), propose-la en Q-n sans l'imposer.
3. **SUITE-MASQUE-UNITTEST-1.** Mesuré : un `unittest.py` (ou `unittest/`) à la racine du dossier d'une suite masque le module standard pour `-m unittest` ; la suite peut imprimer un résumé conforme que ni le vérificateur, ni l'enregistreur, ni le job ne voient. Ferme-le : refus nommé d'un `unittest*` à la racine d'une suite, ou lancement qui l'exclut (attention : `-P` n'existe pas sous 3.10 ; dis ce que fait `-I` avec `-m` sous 3.10 à 3.13, mesuré). Leurre neuf : sortie non nulle, refus nommé, sous 3.10 à 3.13.
4. Aucun cas existant du runner ni test de l'enregistreur retiré ou affaibli ; leurres du contre-contrôle de R-1 (`<scratchpad>/s2bis/outillage/cc/leurres_runner.py`, `leurres_enregistreur_r1.py`) : mêmes verdicts, sauf D7 qui doit être refusé.

## Règles
- Tests d'abord, rouge d'assertion montré. Au moins 8 mutants par diff, classés par la commande du job (runner, puis ligne s2bis de `gates.yml`, borne 300 s, dépassement FATAL).
- Bibliothèque standard seule ; Python 3.10 à 3.13 en `-X dev -W error` (critère de vert : code 0 et aucune ligne « Exception ignored » ni « Warning »).
- Diffs en série **OUT-2a, OUT-2b, OUT-2c** (un par item, dans l'ordre qui te paraît juste), chacun ≤ 200 lignes de code ajoutées ; planchers exacts (`--egal`) recalés ; section METRIQUES par diff si la suite s2bis change.
- R-13, R-8, octets 92 comptés juste, lignes ≤ 120 caractères. Isolement réseau (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL`). `cargo --locked xtask verify` sur la copie : lignes de verdict seules (S-G9 `docs/17:70` connu).
- Livrables dans ton dossier : `diffs/OUT-2*.diff`, `SHA256SUMS`, `NOTES.md`, journal G1 bref, tableau des cas et des mutants. PID réels ; nettoyage final des copies lourdes.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` réel ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier. Rien sur Pocket.

## Rendu
Rapport final par message (c'est ta valeur de retour), court, en français : Gate 0 (identifiant exact du modèle) en tête, puis diffs (sha256, lignes ajoutées), choix Q-n, tableau des leurres, mutants, matrice 3.10 à 3.13, écarts, items à former.
