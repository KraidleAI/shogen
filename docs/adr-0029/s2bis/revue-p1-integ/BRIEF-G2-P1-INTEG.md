# Brief — relecture G2 d'intégration de la partie P1 (noyau du collecteur de S2-bis), avant l'accord de partie

Tu es **réviseur G2 neuf** (`shogen-worker`). Tu n'as écrit aucun sous-lot de P1 et tu n'en as relu aucune tranche.

- Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Utilise `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu écris seulement dans `<scratchpad>/s2bis/p1-integ/`, et tu rends ton rapport par message.
- Tiens un `NOTES.md`. Après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Objet

Le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (point 5 et son ajout daté) exige pour chaque partie :
- une relecture G2 neuve ;
- un accord, rendu par un advisor sur la pièce de clôture.

Les tranches A, B et C de P1 ont chacune eu leur G2 et leurs contre-contrôles. **Ta relecture porte sur la partie entière, telle qu'elle est commise** : ce qu'aucune relecture de tranche n'a pu voir.

## Base

La tête poussée de la branche `claude/compassionate-noether-szmdyj`, après le versement de la tranche C. Lis `git log` : le dernier commit de P1 est « COLLECTE-BIS tranche C : pieces de revue versees ».

## Pièces

- G0, PROPOSITION et AVIS de `docs/adr-0029/g0-collecte/` ; ADR-0029 ; FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` ; METRIQUES.
- Pièces de revue des trois tranches : `docs/adr-0029/s2bis/revue-p1a/`, `revue-p1b/`, `revue-p1c/`.
- Annexe B : blocs B.60, B.63, B.65 et B.67 seulement.
- Le code : `s2bis/`, `enforcement/` (vérificateur et runner), `.github/workflows/gates.yml`, `s2-harness/tools/oracle_record.py` et son test.

## Contrôles

1. **Couverture du G0.** Pour chaque sous-lot de P1 (CB-0 à CB-5, CB-10, CB-11, CB-18) et chaque exigence E-C rattachée, dresse un tableau : où elle est tenue (fichier:ligne) et quel test la fige. Liste toute exigence sans test.
2. **Cohérence FORMAT ↔ code.** Le FORMAT dit-il exactement ce que fait le code ?
   - Écrivain : `_lire`, définition d'« intègre » au §7.1, noms et segments, imbrication, entiers, reprise, queue.
   - Boucle, lecture, DNS, santé, points d'entrée, `run_params`.
   - Écris une sonde indépendante d'après le FORMAT seul, et compare-la au code sur des journaux produits par l'écrivain réel avec pannes et redémarrages.
3. **Bout en bout.** Lance le point d'entrée réel `python3 -m shogen_s2bis.collecte` sur des serveurs locaux factices (HTTP, TLS de test, DNS), en réseau isolé avec `lo` allumée. Fais-le sur plusieurs fenêtres, avec une panne de source, une sonde pendue, un recul d'horloge et un redémarrage.
   - Le journal doit être conforme, et la reprise juste.
   - Le processus doit sortir proprement.
   - Mesure la mémoire et les fils sur la durée.
4. **Intégration entre tranches.** Interfaces entre écrivain, boucle, lecture, DNS, santé et points d'entrée : contrats implicites, exceptions non nommées, états partagés, fils.
   - Cherche les défauts qu'aucune tranche seule ne voyait. Par exemple : un refus de l'écrivain en pleine fenêtre, ou un échec du disque au moment d'une bascule de jour.
5. **Sécurité et robustesse.**
   - Entrées réseau hostiles : réponses énormes, lentes, malformées ; DNS empoisonné ou tronqué.
   - Fichiers de configuration hostiles.
   - Droits sur les fichiers. Aucun secret journalisé.
   - Garde réseau des tests.
6. **CI et gates.**
   - Runner (77 cas), jobs s2bis, S2 et sim-bis aux planchers exacts, sous Python 3.10 à 3.13 en `-X dev -W error`.
   - Enregistreur de rôle : essaie de le tromper.
   - `cargo --locked xtask verify` sur une copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
7. **Mutants transverses.** Au moins vingt mutants à toi, à l'échelle de la partie (interfaces, ordre des écritures, gestion d'erreurs), classés par la commande du job, avec une borne de temps (au-delà, FATAL).
8. **Registre.** Pour chaque item P1 de B.60, B.63 et B.67, dis s'il est réellement fermé ou ouvert, et si son déclencheur est juste. Tu ne fermes rien toi-même : tu signales.
9. **Pièce de clôture.** Écris-la : un résumé de la partie en deux pages au plus, pour l'advisor qui rendra l'accord. Elle dit :
   - ce que P1 fait ;
   - ce qui est prouvé, et par quoi ;
   - ce qui reste ouvert, et quand ;
   - les risques résiduels.

## Exécution

- Copies faites par `git archive`, avec les exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`.
- `TMPDIR` dédié.
- `unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`).
- Consigne le PID réel de chaque processus. Pas de `pgrep -f` sur un motif large.
- Nettoie tes copies lourdes à la fin.

## Interdits

- Les dossiers exclus des copies.
- Tout `*.jsonl` réel. Seuls des journaux synthétiques écrits par l'écrivain dans ton `TMPDIR` sont permis, et tu les déclares.
- Toute pièce de D.2.
- **Toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier.**

## Rendu

Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE, plus la pièce de clôture `CLOTURE-P1.md`.

Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
