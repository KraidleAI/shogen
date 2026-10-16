# Rapport du générateur du groupe B (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2b/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# GARDE-FOUS-ORCH, phase 2, groupe B : rapport du générateur G1

Générateur : `claude-opus-5-5` (Gate 0 : identifiant système de la session du worker). Rattachement : ADR-0028 annexe B,
B.102 (items SHOGEN-GARDE-OUTIL-E18-E20-1, SHOGEN-GARDE-OUTIL-E26-E27-E28-1, SHOGEN-GARDE-CROCHET-ACTE-1) ; G0 :
`docs/adr-0028/G0-lots-DETTES.md`, ajout GF-0, puce Phase 2. Base : HEAD `84993090d81781293a7720e601faa387c340e77f`,
copie creuse par `git archive` (interdits exclus, `chemin_interdit` : 0 écarté). Journal G1 : `NOTES.md`.

## 1. Série (huit diffs, `diffs/`, ordre d'application)

| diff | lignes ajoutées | contenu | plancher `controle-unittest` |
|---|---|---|---|
| GFB-1 | 198 | `.claude/hooks/acte_shell.py` (neuf) : lecture de l'acte par shlex | 117 |
| GFB-2 | 120 | crochet : R1, R2, R3, R5 jugés sur les actes ; README (ajout GFB-1) | 117 |
| GFB-2t | 133 | `tests/test_garde_acte.py` (cas LN-6) ; README (ajout GFB-2) | 124 |
| GFB-3 | 83 | R7 : sleep d'avant-plan, pkill -f et pgrep -f non ancrés (E18, E28) | 126 |
| GFB-4 | 119 | R8 : forge avant create_pull_request, `garde/forge-actions.txt` (E20) | 128 |
| GFB-5 | 130 | R9 : seuil de coût Agent et Workflow, jeton (E27) | 131 |
| GFB-6 | 176 | R10 : relevé UserPromptSubmit, dossier au Stop, `settings.json` (E26) | 134 |
| GFB-7 | 116 | `avant_acte.py verser` V6, V7 ; skill `shogen-avant-committer` (E28) | 136 |

Chaque diff : ≤ 200 lignes ajoutées (R-25), aucun marqueur de dette nu (R-13), fin de fichier en saut de ligne ;
README : ajouts datés en fin seulement ; `gates.yml` : ligne du plancher changée en place (aucune ligne décalée, C-3).
Rouge puis vert (`outils/rouge_vert.sh`, `tmp/rouge-vert.txt`) : chaque diff s'applique sur la base plus les
précédents ; vert à son plancher (`Ran` égal) ; rouge avant : 6, 2, 2, 3, 3, 2 cas en échec (GFB-2t à GFB-7), ceux de
l'étape seulement. GROUPES proposé : aucun (chaque pas est vert seul) ; GFB-2t porte les cas de GFB-1 et GFB-2.
Matrice : python3.11, 3.12, 3.13 sous `-X dev -W error` : sortie 0, `Ran 136`, aucune ligne Warning.
Diff E29 de l'orchestrateur (`r6b/E29-garde.diff`) : s'applique avant comme après la série, même crochet dans les deux
ordres ; ligne du job conforme avec lui.

## 2. Outils

### LN-6, acte lu (GFB-1, GFB-2, GFB-2t ; SHOGEN-GARDE-CROCHET-ACTE-1)
- Erreur visée : le crochet jugeait le texte de la commande ; une commande qui écrit un journal synthétique par un
  heredoc python portant un commit était refusée en R3 puis en R5 (sonde du contre-contrôle, E-3) ; cas revécu par moi
  dans cette passe (NOTES, refus R5 sur un identifiant fictif d'un heredoc).
- Ce qu'il refuse : les mêmes actes qu'avant, lus sur la commande découpée (rm récursif d'un arbre git, écriture d'un
  fichier non lu par redirection, tee, sed -i, open en écriture d'un code python ; git commit et push, y compris dans
  bash -c, eval, une substitution, derrière une affectation ou des options globales) ; R5 lit le message de commit,
  fichier de `-F` compris (serrage : il ne le lisait pas). Commande illisible par shlex, ou module absent : motifs
  d'avant (sens sûr). Le crochet n'écrit plus de bytecode à côté de lui (défaut trouvé en vérification, corrigé).
- Preuve : 7 cas ; rouges sur le code d'avant (6, dont la sonde et le contrôle d'une poussée), verts après.
- Fermeture proposée : « LN-6 fermé : R1, R2, R3 et le texte de R5 se jugent sur les actes lus par shlex
  (`acte_shell.py`) ; la sonde du contre-contrôle passe, les vrais commits et poussées restent refusés. »

### E18 et moniteur de E28 (GFB-3 ; SHOGEN-GARDE-OUTIL-E18-E20-1)
- Refuse : `sleep` d'avant-plan hors boucle until et hors arrière-plan (&, groupe ou liste au fond,
  run_in_background) ; `pkill -f` ou `pgrep -f` dont le motif ne commence pas par `^`.
- Preuve : cas réel `sleep 60` ; auto-reconnaissance mesurée sur l'hôte (motif non ancré : trouvé sans chaîne ; ancré :
  rien) ; 2 cas, rouges avant.
- Fermeture : « E18 fermé : R7 refuse le sleep d'avant-plan et le motif de processus non ancré. »

### E20 (GFB-4)
- Refuse : `mcp__github__create_pull_request` sans preuve, au journal de l'agent, d'un run conclu success ou d'un job à
  runner_id non nul sur le même owner/repo (outil `mcp__github__actions_*`, ou gh run, gh api), ni ligne du jour au
  marqueur `scripts/controle/garde/forge-actions.txt`.
- Preuve : cas réel runner_id 0 ; 2 cas, rouges avant. Fermeture : « E20 fermé : R8 refuse la PR sans constat de jobs
  de la forge sur ce dépôt. »

### E27 (GFB-5)
- Refuse : workflow de plus de 3 agents (nombre illisible ou multiplié par une boucle : refus), ou lancement qui porte
  les sous-agents vivants au-delà de 4 ; sauf `FANOUT-AUTORISE` ou les mots fan out au dernier message de l'humain
  (journal de la session, même pour un sous-agent).
- Preuve : cas réel de 10 agents ; 3 cas, rouges avant. Fermeture : « E27 fermé : R9 refuse le fan-out au-delà du
  seuil sans jeton de l'investisseur. »

### E26 (GFB-6)
- Fait : à la soumission, relevé des noms propres au JOURNAL et dans docs/publication/ (affiché en contexte, gardé) ;
  au Stop, refus une fois d'une réponse qui nomme un dossier (Pocket, MONARK, publication, préavis, procurement,
  S2-bis) absent du message et des faits du tour.
- Preuve : cas réel CoinGecko rattaché à Pocket ; 3 cas, rouges avant (dont le branchement de `settings.json`).
  Fermeture : « E26 fermé : R10 relève les noms propres d'un message et refuse le rattachement sans relevé. »

### E28 (GFB-7)
- Refuse (`verser`) : V6, octet de biblio/ sans mention en accents graves dans INDEX.md, ou compte d'en-tête faux
  (forme de S-G6) ; V7, versement pendant qu'une chaîne tourne (pgrep -f ancré ; pgrep en erreur : 3).
- Preuve : cas réel (livre sans rangée, compte 204 contre 205) ; vraie chaîne d'essai vue ; 2 cas, rouges avant. Une
  vraie chaîne tournait sur l'hôte pendant la passe : les autres cas de verser fixent pgrep par un faux.
  Fermeture : « E28 fermé : verser refuse l'octet de biblio/ sans rangée et le versement pendant une chaîne. »

## 3. Mutants
`base/scripts/controle/mutants.py` (arbre relu) sur la copie, job `controle-unittest`, borne 300 s, détaché ; 73 mutants
distincts (dont 9 de sites d'appel et d'étiquettes, et 1 de la garde du bytecode) ; 7 survivants intermédiaires (S14,
S15, H17, H36, H37, A10, C09), chacun tué après un cas ajouté ; tous tués à la fin, aucun FATAL ; relevés ps vides.
Sorties : `tmp/mutants-run*.txt`, `mutants-sortie*/`.

## 4. Limites (items à former)
- L-1 Le schéma d'entrée de l'outil Workflow n'est pas connu (aucun journal réel lu) : le compte lit les appels
  `agent(` et une clé `agents` ; autre forme : nombre illisible, refus sans jeton.
- L-2 Agents vivants : journaux de `subagents/` touchés depuis 300 s (un agent muet plus longtemps n'est pas compté).
- L-3 Une boucle while d'attente est refusée (forme écrite du brief : until) : question à adjuger.
- L-4 R10 : liste fixe de six dossiers ; noms propres par heuristique (faux positifs possibles, refus une fois par
  tour) ; tout fait du tour qui affiche le dossier vaut relevé ; Stop de l'agent principal seulement.
- L-5 `acte_shell.py` : un opérateur seul entre guillemets est lu comme opérateur ; un script lancé par son nom n'est
  pas lu ; case non analysé.
- L-6 V6 et V7 jugent au moment de `verser` ; une copie dans biblio/ hors de `verser` n'est vue que par S-G6 (item
  possible : crochet sur l'écriture dans biblio/ pendant une chaîne).
- L-7 Les cas de `.claude/hooks/tests/` (hors CI) échouent sous un TMPDIR qui porte un segment hexadécimal (R5),
  avant comme après la série.
- L-8 Conflits attendus avec les groupes A et C : même ligne du plancher de `gates.yml` et fin du README ; recalage à
  la chaîne.

## 5. Écarts
E-1 à E-7 de `NOTES.md` (liste de noms sous docs/adr-0028, TMPDIR hors du lot deux fois, retouche non idempotente
corrigée, un sleep d'avant-plan, git apply hors dépôt sur copies jetables, campagne d'un autre groupe simultanée,
substitution d'un heredoc non cité).
