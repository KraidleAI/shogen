# Rapport du worker — LINT-HAIKU (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 12:11:04 UTC du rapport rendu par l'agent a3605789a88cf302d (workflow wf_34ba9b2a-037) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot LINT-HAIKU (G1), 2026-10-08

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session ; il porte le préfixe attendu. L'effort `max` ne se voit pas de l'intérieur.

**Base** : e6657dcc3154bf2d35c69b84d9deae1385e702a7, la même que celle du brief. Le dépôt réel n'a pas bougé : HEAD inchangé, status vide, aucune écriture git, aucun fichier créé sous son `.claude/agents/`. Toutes les copies sont sous `TMPDIR`.

**Bilan :**
- Le lint de l'arbre est vert.
- Le runner est vert : 107 cas.
- Les 13 mutants sont tués.
- **`cargo --locked xtask verify` sort ROUGE sur la copie**, pour une seule raison (E-1) : S-G9 ne trouve pas un fichier de `docs/rapports`, que les exclusions habituelles du brief retirent de la copie. Le même ROUGE apparaît sur la base sans mes diffs, donc il ne vient pas du lot. Le critère de sortie « verify VERT » ne peut pas être atteint sur une copie.

`<LH>` = `<scratchpad>/lot-haiku`

## Diffs (à appliquer en série sur e6657dc ; `git apply --check` et `patch -p1 --dry-run` passent)

| pièce | sha256 | lignes |
|---|---|---|
| `<LH>/diffs/LH-1.diff` | afcc0872ab5f9191cf6ca2944b7cf9fafe2a89b5719ee854d893560ed191a283 | +23 −3 (lint +6 −3, runner +17) |
| `<LH>/diffs/LH-2.diff` | e76eac740293e9eaa0958aefc84208bac6cb3799c53631a8dc86c2317d68d6ec | +34 (fichier neuf) |

Fichiers obtenus après application :
- lint : f806c036a4a917d67def301d930bdd14ffaf2fb1d2ace9453f2426a001b74f8a ;
- runner : 9744dfb7cb156ab6952f2e0008becc2f15fd507331203e071289305fda0c8a63 ;
- `.claude/agents/shogen-extracteur.md` : 1974e9f94a62b716a9d67bb2ae6324d75c536eaff565dd0229368c9ff7a015fc.

Contrôles sur les lignes ajoutées :
- octets 92 : 0 (le lint en garde 43 et le runner 48, comme avant) ;
- lignes de plus de 120 caractères : 0 ;
- littéral banni : 0 ;
- TODO/FIXME : 0 ;
- CR : 0.

Aucune dépendance neuve : bash et la bibliothèque standard seulement.

**Ce que fait LH-1 :**
- `ALLOWED` reçoit `claude-haiku-5-5`, et rien d'autre.
- L'en-tête du lint cite :
  - le roster (CLAUDE.md l.23-49, point 7) ;
  - la décision du 2026-10-08 et le bloc B.76 ;
  - une limite nouvelle : le lint ne lie pas un identifiant à un rôle (CLAUDE.md l.41-42).
- Le runner reçoit 12 cas datés.

## Résultats

- **Rouge d'abord.** Le runner neuf contre le lint de e6657dc donne 101 ok et 6 échecs, sortie 1 :
  - T-96 à T-100 sont refusés en `R-1/hors-liste` ;
  - T-104 obtient `hors-liste` au lieu de `suffixe`.
- **Vert.** Le runner neuf contre le lint neuf donne 107 ok et 0 échec, sortie 0, en 3,4 s.
- **E-LH-3 :**
  - le runner d'origine contre le lint neuf donne 95 ok ;
  - les lignes T-01 à T-95 sont identiques octet pour octet.
- **Lint de l'arbre** (copie + LH-1 + LH-2) : `OK (R-1) : 7 fichier(s)`, sortie 0. J'ai recompté le compte attendu (6 + la fiche) sur la liste des noms de l'archive, sans passer par le lint.
- **Fiche sans LH-1.** Le brouillon comme la fiche corrigée sont refusés (`R-1/hors-liste`, sortie 2), comme le relate B.76.
- **`cargo --locked xtask verify` sur la copie : ROUGE global** (écart E-1). Lignes de verdict :
  - S-G1 à S-G8 : VERT (0 violation) ;
  - S-G9 : ROUGE (1 violation) ;
  - `cargo fmt --check` : VERT ;
  - no_std du vérificateur : VERT ;
  - `cargo clippy -D warnings` : VERT ;
  - `=== VERDICT GLOBAL : ROUGE ===`.
- **s2-harness** sur la copie finale : 407 tests, OK (2 sautés).

## Cas neufs (E-LH-1, E-LH-2)

| cas | forme | attendu | contre le lint de e6657dc |
|---|---|---|---|
| T-96 | agent `model: claude-haiku-5-5` | 0, 1 fichier | ÉCHEC |
| T-97 | skill | 0, 2 | ÉCHEC |
| T-98 | commande | 0, 2 | ÉCHEC |
| T-99 | `settings.json`, `model` | 0, 2 | ÉCHEC |
| T-100 | `settings.local.json`, `advisorModel` | 0, 2 | ÉCHEC |
| T-101 | `claude-haiku-4-5` | 2, R-1/hors-liste | ok |
| T-102 | `claude-haiku-5` | 2, R-1/hors-liste | ok |
| T-103 | `claude-haiku-5-5-20260101` | 2, R-1/hors-liste | ok |
| T-104 | `claude-haiku-5-5[1m]` | 2, R-1/suffixe | ÉCHEC (hors-liste) |
| T-105 | `Claude-Haiku-5-5` | 2, R-1/hors-liste | ok |
| T-106 | `model: "claude-haiku-5-5 "` (entre guillemets) | 2, R-1/hors-liste | ok |
| T-107 | JSON `"model": "claude-haiku-5-5 "` | 2, R-1/hors-liste | ok |

T-48 (`haiku` nu, attendu `R-1/tier-nu`) n'a pas changé et passe.

## Mutants

Les mutants portent sur le lint final, une mutation chacun. Ils sont classés par la sortie du runner final : 1 = tué, 0 = vivant, autre = FATAL.

Bilan : **13 tués sur 13**, 0 vivant, 0 FATAL.

| mutant | mutation | cas qui échouent |
|---|---|---|
| M-01 | motif : `claude-haiku-*` admis | T-101 à T-104, T-106, T-107 |
| M-02 | motif : sous-chaîne d'un identifiant admis | T-12, T-13, T-31, T-33, T-42, T-103, T-104, T-106, T-107 |
| M-03 | casse ignorée (toute la liste) | T-17, T-105 |
| M-04 | casse ignorée (Haiku seul) | **T-105 seul** |
| M-05 | suffixe toléré (`-date`) | **T-103 seul** |
| M-06 | suffixe toléré (crochets retirés) | T-13, T-42, T-104 |
| M-07 | liste remplacée (Haiku seul) | 31 cas, dont T-01 à T-03 |
| M-08 | Haiku à la place de Fable | T-01, T-23, T-25, T-30, T-38, T-85, T-90, T-91 |
| M-09 | tier nu admis (`haiku` dans la liste) | T-48 |
| M-10 | `haiku` retiré des tiers | T-48 |
| M-11 | ordre inversé dans `norm` (guillemets avant blancs) | **T-106 seul** |
| M-12 | ordre inversé dans `verdict` (base avant égalité) | T-13, T-17, T-42, T-104, T-105 |
| M-13 | espace final toléré en JSON | **T-107 seul** |

Les mutants sont dans `<LH>/mutants/` (M-xx.sh et M-xx.diff). Le journal de la campagne est `<LH>/logs/campagne.tsv`.

## Écarts

**E-1. verify ROUGE sur la copie, pour une cause hors lot.**
- La seule violation est S-G9 (a) : `docs/17-modele-de-menace.md:70` cite `docs/rapports/cartographie-2026-09-29.md:21`. Ce dossier est exclu de la copie par le brief.
- Le contrôle sur la copie de base sans les diffs donne une section S-G9 identique et le même verdict.
- La référence existe depuis e970c38 (2026-09-30). Depuis, toute copie faite avec les exclusions habituelles sort ROUGE d'office.

**E-2. Espace final.**
- Il est refusé quand il fait partie de la valeur : YAML entre guillemets (T-106) et chaîne JSON (T-107).
- En YAML nu, il ne fait pas partie de la valeur. Mesure faite avec PyYAML 6.0.1, déjà présent, en brouillon seulement : la forme nue donne `'claude-haiku-5-5'`.
- `norm` retire cet espace pour toute la liste, et le lint final admet la forme nue (sortie 0). Ce comportement est antérieur au lot ; je ne l'ai pas serré.

**E-3. E-LH-1 contredit le roster sur `advisorModel`.** E-LH-1 exige que `advisorModel: claude-haiku-5-5` passe (T-100), alors que le roster exclut Haiku des advisors. La limite est écrite dans l'en-tête du lint et dans le commentaire du runner, sans code.

**E-4. Corrections de la fiche par rapport au brouillon** (`<LH>/logs/fiche-brouillon-vers-corrigee.diff`) :
- ajouts tirés du roster :
  - « prover, red team » ;
  - « pas de rôle mémoire » ;
  - « (annote, ne retire jamais) » ;
  - « relit la source avant tout acte » ;
  - quorum et diversité (doctrine Knight et Leveson) ;
- « Ne modifie aucun fichier » au lieu de « aucun fichier suivi », pour s'accorder avec le corps et les outils ;
- en tête du corps, l'identifiant et l'effort, comme dans les fiches voisines ;
- point 6 nouveau, qui inclut « rendu à l'orchestrateur, non exécuté ». Cette phrase est un ajout de ma part.

**E-5. `setsid` sous contrôle de travaux** (`set -m`, actif sur cet hôte).
- `setsid` fourche, et `$!` n'est pas le PID du travail. Mesure : PID externe 25834, déjà fini ; PID interne 25836.
- `setsid -w` garde le PID externe vivant jusqu'à la fin du travail (mesuré).
- Pour mes deux verify, j'ai constaté la fin par la ligne `rc_verify` écrite par le travail et par l'absence de processus.

## Items à former (règle PAROXYSME)

1. **Rôles.** Le lint ne lie pas un identifiant à un rôle : un identifiant admis passe en `advisorModel`, Haiku compris. Serrer demanderait un G0, par exemple `advisorModel` réservé à `claude-fable-5-1` ; T-100 s'inverserait.
2. **verify sur copie.** Sur une copie faite avec les exclusions habituelles, verify sort ROUGE à cause de S-G9. Il faut soit lancer verify sur l'arbre complet, soit donner à S-G9 un mode qui connaît les exclusions.
3. **Consigne SHOGEN-HARNAIS-TACHE-10MIN-1.** Elle dit « fin constatée en sondant le PID ». Il faut y préciser `setsid -w`, ou un PID écrit depuis l'intérieur du travail.

## Questions

- **Q-1** (E-3) : garder T-100 tel quel, ou ouvrir un G0 qui lie l'identifiant au rôle ?
- **Q-2** (E-2) : la forme nue `model: claude-haiku-5-5 ` reste-t-elle admise, ce qui est la lecture YAML ?
- **Q-3** : le runner et le lint citent « G0 du lot » sans chemin. Quel chemin versionné faut-il citer ?
- **Q-4** (E-4) : la phrase « rendu à l'orchestrateur, non exécuté » du point 6 est-elle gardée ?
- **Q-5** (E-1) : l'orchestrateur peut-il lancer verify sur l'arbre complet après application, pour satisfaire le critère de sortie ?

Pièces jointes, toutes dans `<LH>` :
- `SHA256SUMS` : 54 lignes, `sha256sum -c` OK ; empreinte du fichier : cece1463d4e46f6dd9307d0eaa252346075df2928eb6377384f0a34292cf438f ;
- `NOTES.md` ;
- `JOURNAL-G1.md` ;
- `RAPPORT-GENERATEUR.md` : ce rapport, sans l'empreinte de `SHA256SUMS`, calculée après ;
- `scripts/` ;
- `logs/`.
