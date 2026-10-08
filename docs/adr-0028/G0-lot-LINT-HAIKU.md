# G0 — lot LINT-HAIKU : admettre `claude-haiku-5-5` à la liste blanche du lint R-1, en rôles de signal

Orchestrateur, 2026-10-08. Rattachement : ADR-0028 D8 et C-14 (lint d'épinglage, lots D8a et D8c ; G0 `docs/adr-0028/G0-lot-D8a.md` et `G0-lot-D8c.md`) ; roster de `CLAUDE.md` point 7 (ajout Haiku 5.5 du 2026-10-08, commit e6657dc) ; annexe B, bloc B.76.

## 1. Objet
La décision du fondateur du 2026-10-08 adopte Haiku 5.5 (`claude-haiku-5-5`, effort `high`) en rôles de signal seulement. Le lint `enforcement/lint-model-pinning.sh` refuse tout identifiant hors de sa liste blanche, et son en-tête dit : « la changer demande un lot ». Ce lot ajoute l'identifiant exact, et rien d'autre.

## 2. Périmètre (fichiers)
- `enforcement/lint-model-pinning.sh` : `ALLOWED` reçoit `claude-haiku-5-5` ; l'en-tête cite le roster et B.76 (lignes de `CLAUDE.md` à jour).
- `enforcement/tests/run-fixtures-model-pinning.sh` : cas neufs à partir de T-96 ; en-tête daté.
- `.claude/agents/shogen-extracteur.md` : la fiche (brouillon de l'orchestrateur, `<scratchpad>/lot-haiku/shogen-extracteur.md`), relue par le lot.
- Hors périmètre : `.github/workflows/gates.yml` (le job g1-model-pinning reste tel quel), tout autre fichier.

## 3. Exigences
- E-LH-1 : `model: claude-haiku-5-5` est accepté (agent, skill, commande, réglage JSON `model` et `advisorModel`).
- E-LH-2 : rien d'autre n'est élargi : le tier nu `haiku` reste refusé (T-48 inchangé) ; `claude-haiku-4-5`, `claude-haiku-5`, `claude-haiku-5-5-20260101`, `claude-haiku-5-5[1m]`, `Claude-Haiku-5-5` et `claude-haiku-5-5 ` (espace final) sont refusés, chacun avec son jeton.
- E-LH-3 : les 95 cas existants passent sans changement de leur attendu ; le lint sur l'arbre complet, fiche extracteur comprise, sort en 0 avec le bon compte de fichiers.
- E-LH-4 : la fiche extracteur dit son rôle de signal et ses interdits (roster point 7) ; sa clé `effort: high` est écrite.

## 4. Tests et mutants
Tests d'abord, rouge montré (le cas T-96 doit échouer sur le lint actuel). Au moins 6 mutants (identifiant élargi par motif, casse ignorée, suffixe toléré, liste remplacée, tier nu admis, ordre de contrôle inversé), classés par le runner du lint.

## 5. Critères de sortie
Runner du lint vert (95 + cas neufs), lint de l'arbre vert, `cargo --locked xtask verify` VERT, relecture G2 neuve ACCEPTE ou corrections soldées.

## 6. Ajout daté du 2026-10-08 12:12:38 UTC (orchestrateur, après la relecture G2) : correction du G0 et adjudication

- **Erreur du G0 corrigée.** E-LH-1 exigeait que `advisorModel: claude-haiku-5-5` passe. C'était contraire au roster (Haiku jamais advisor). **E-LH-1 se lit désormais :** `claude-haiku-5-5` est accepté pour la clé `model` (agent, skill, commande, réglage JSON) et **refusé pour `advisorModel`**, avec un jeton nommé (par exemple `R-1/role`). T-100 s'inverse. Réserver `advisorModel` à `claude-fable-5-1` seul reste hors lot (item à former).
- **E-LH-5 (nouveau, item I-1 de la G2, mesuré).** Le verdict du lint dépend de la locale (sous C.UTF-8, `model:<U+3000>id` et voisins passent ; sous POSIX, ils sont refusés). Le lint fixe sa locale (`LC_ALL=C` exporté en tête, ou équivalent motivé) ; cas neufs qui lancent le lint sous C.UTF-8 et sous POSIX pour ces formes, attendus refusés dans les deux.
- **Chemin versionné du G0 (C-1 de la G2).** Ce G0 sera versé à `docs/adr-0028/G0-lot-LINT-HAIKU.md` ; le lint et le runner citent ce chemin.
- **C-2 et C-3 de la G2.** Cas T-108 (`Claude-haiku-5-5`), T-109 (espace insécable final), T-110 (U+200B final), attendus `R-1/hors-liste`.
- Adjugé : Q-2 (forme nue admise, lecture YAML) tenu ; Q-4 (phrase de la fiche) tenu ; Q-5 : verify sur l'arbre complet est fait par l'orchestrateur au commit. Écart d'affichage des lignes de S-G9 : ce sont des notes de l'outil lui-même, qui par construction ne recopient aucune forme de D.2 (note (f)) ; pas d'attestation D.3, écart consigné.

## 7. Ajout daté du 2026-10-08 14:58:00 UTC (orchestrateur, après la revue de la vague 2) : adjudication

- **Q-2, I-R-1 et I-a : Haiku est refusé partout dans les réglages JSON** (`.claude/settings.json`, `.claude/settings.local.json` : clés `model`, `advisorModel`, hooks et toute autre clé), avec le jeton `R-1/role` : la clé `model` des réglages fixe le modèle de la session principale (l'orchestrateur, qui décide), et un hook de type prompt peut décider. `claude-haiku-5-5` n'est admis **que** comme valeur de la clé `model` du frontmatter d'un agent, d'une skill ou d'une commande. E-LH-1 se lit ainsi.
- **Q-1 et I-R-4 :** le refus des blancs Unicode est gardé. Le contrôle du commentaire d'une ligne `model` ne refuse que l'UTF-8 invalide : `# décision` reste admis sous toutes les locales ; `# x<0xFF>` et `<TAB># x<0xFF>` sont refusés. Les deux bornes sont figées par des cas.
- **Q-4 :** T-112 gardé (échec fermé si C.UTF-8 manque) ; Git Bash et la locale réelle du job : items.
- **C-1 à C-3 de la revue :** à faire (cas de locale par `LC_ALL` et `LC_CTYPE` aussi ; T-126, T-127 adaptés à I-R-4 ; T-128, T-129).
- Écart E-9 du correcteur (compte des fichiers suivis par `git ls-tree -r | wc -l`, sans nom affiché) : consigné, sans suite. Items hors lot à former : I-R-2 (`advisorModel` non lu dans un frontmatter), I-R-3, I-c, I-d (blancs et sauts de ligne non vus), I-e (Git Bash), I-f (locale du job), I-2 à I-5 de la G2.
