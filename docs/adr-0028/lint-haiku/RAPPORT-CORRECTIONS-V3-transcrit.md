# Rapport des corrections — LINT-HAIKU, vague 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 17:39:28 UTC du rapport rendu par l'agent a7b8f730edf0a532e (workflow wf_ae64f812-f4d) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

Je rends le rapport de correction du troisième tour LINT-HAIKU, aussi écrit dans `corr3/RAPPORT-CORRECTIONS.md`.

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session, avec le préfixe attendu ; l'effort `max` ne se voit pas de l'intérieur.

- Horloge (`date -u`) : de 2026-10-08T14:58:27Z à 2026-10-08T16:01:54Z.
- `<C3>` = `<scratchpad>/lot-haiku/corr3`.
- Copie et diffs sur e6657dc, la base du brief ; l'archive est identique à celle des tours précédents (c1f09c21…).

## À rendre à l'orchestrateur : le dépôt réel a avancé pendant ma passe

- Au départ, HEAD valait e6657dc et le status était vide.
- À 15:59:14Z, HEAD valait 63c43faf, soit 9 commits PLAN-S2BIS-2, avec 4 fichiers indexés sous `scripts/plan-s2bis-2/`.
- Aucun fichier n'a changé sous `enforcement/`, `.claude/`, `.github/` ni `CLAUDE.md` : mes diffs ne recouvrent rien de ce qui a bougé.
- Je n'ai fait aucune écriture git et je n'ai rien créé sous `.claude/` du dépôt réel.

## Bilan

**G0 §7 tenu.**
- **Réglages JSON** : `claude-haiku-5-5` y est refusé partout avec `R-1/role`, sous toute clé, comme clé, valeur ou sous-chaîne. La casse est ignorée et l'échappement JSON `u00XX` est lu. T-99 est inversé ; T-142 à T-145 sont neufs.
- **Frontmatter** : Haiku n'est admis que comme valeur de la clé `model` de premier niveau d'un agent, d'une skill ou d'une commande. Il est refusé (`R-1/role`) dans deux cas, couverts par T-146 à T-155 :
  - sur une ligne `model` imbriquée, hook compris (I-a) ;
  - dans une collection de flux ouverte sur plusieurs lignes : PyYAML 6.0.1 y lit une ligne `model` de colonne 0 comme imbriquée (mesuré).
- **Commentaire d'une ligne `model`** : seul l'UTF-8 invalide est refusé.
  - `# décision` passe sous toutes les locales (T-127) ; `# x<FF>` (T-130) et `<TAB># x<FF>` (T-126) sont refusés.
  - Le validateur suit RFC 3629 ; sur 1 201 300 formes, il donne 0 désaccord avec glibc 2.39 sous C.UTF-8.

**C-1 à C-3 de la revue : soldées.** `casl` lance aussi le lint sous `LC_ALL=C.UTF-8` et sous `LC_CTYPE=C.UTF-8`. T-126 et T-127 sont adaptés à I-R-4 ; T-128 et T-129 sont ajoutés.

**Défaut trouvé dans la vague 2 et corrigé (E-4, à adjuger).**
- Sous C.UTF-8, un octet UTF-8 invalide en tête de ligne d'un frontmatter masquait l'indentation (forme a) ou la suite d'une valeur `model` (forme b).
- La base refusait ces formes sous C.UTF-8 ; la vague 2 les admettait partout (mesuré). Ni son différentiel ni la revue ne l'avaient vu.
- Remède : l'UTF-8 invalide est refusé (`R-1/cle-model`) sur toute ligne du frontmatter qui n'est pas une ligne `model` (T-140, T-141).

## Diffs, à appliquer en série sur e6657dc

| pièce | sha256 | lignes | code ajouté | octets 92 |
|---|---|---|---|---|
| LH-1 | fdedb72915a49d1c9d1a6f2c350ce1f5cfcc8f950ef3f933ca50e640e2b2ffe4 | +161 −10 (lint +60 −10, runner +101) | 34 + 77 = 111 (≤ 200) | lint 43 → 98, runner 48 → 142 |
| LH-2 | e76eac740293e9eaa0958aefc84208bac6cb3799c53631a8dc86c2317d68d6ec | +34 | texte | 0 |

- LH-2 est identique octet pour octet à celui des tours précédents.
- Lignes ajoutées : 119 caractères au plus ; aucun TODO/FIXME, CR, tabulation, blanc final ni littéral banni ; `bash -n` passe.
- `patch -p1` et `git apply` en série, hors de tout dépôt, donnent des fichiers identiques.
- Fichiers obtenus : lint ffb790b0…, runner 76a1d7a4…, fiche 1974e9f9….
- Lint et runner sont écrits par des scripts sans aucun octet 92 (les barres viennent de `chr(92)`) ; les octets écrits ont été contrôlés par `od -c`.

## Résultats

| contrôle | résultat |
|---|---|
| runner livré | 212 ok, sortie 0, sous 14 environnements (POSIX ; C.UTF-8 par LANG, LC_ALL et LC_CTYPE ; tr_TR.UTF-8 ; zh_CN.GB18030 ; ja_JP.EUC-JP ; LC_ALL invalide ; LOCPATH vide ; mixtes) |
| rouge d'abord | contre la vague 2 : 26 échecs d'assertion ; contre la base : 59 ; chaque cas neuf ou inversé a au moins un rouge (contre la vague 2, la base ou un mutant) |
| témoin T-112 | rouge si la locale manque (« ÉCHEC T-112 ») |
| mutants | M-01 à M-16 de la revue, portés sur le code du tour 3, et N3-01 à N3-26 neufs : 42 tués sur 42, sous P comme sous U ; 0 FATAL ; témoin vivant |
| différentiel | 2 970 formes ; 0 instable sous 8 environnements ; 0 desserrement |
| E-LH-3 | runner de base contre le lint final : 95 ok |
| lint de l'arbre | `OK (R-1) : 7 fichier(s)` sous 5 environnements (base : 6) |
| hooks | 54 ok |
| s2-harness | 407 tests OK (skipped=2) ; `verdict-suite-s2 --egal` conforme |
| verify | mêmes verdicts que la base : S-G1 à S-G8 VERT, S-G9 ROUGE (1, section identique par empreinte), global ROUGE |

- Parmi les mutants neufs, les deux demandés sont tués : N3-01 (un réglage JSON qui admet haiku sous `env` ou une permission) par T-143 à T-145 ; N3-04 (un commentaire non ASCII valide refusé à tort) par T-127 et T-131.
- Différentiel : 120 formes passent en plus, toutes en haiku, chacune avec sa jumelle en opus admise par la base sous POSIX et sous C.UTF-8. Les 375 serrages sont les prix décrits plus bas.

## Écarts

- **E-1 à E-3 : barres obliques inverses.**
  - Une sonde et une commande d'édition portaient des `\n` tapés : refaites ou contrôlées sur les octets écrits.
  - `mutants3.py` porte 102 échappements Python `\"`. Les barres des mutants viennent de `chr(92)` et sont contrôlées par le diff de chaque mutant.
- **E-4 (à adjuger)** : refus de l'UTF-8 invalide au-delà du commentaire. Prix : une description en Latin-1 serait refusée ; l'arbre n'en porte aucune.
- **E-5 (à adjuger)** : Haiku en premier niveau est refusé s'il vient après un crochet laissé ouvert dans de la prose plus haut.
- **E-6 (à adjuger)** : j'ai lu « partout » comme toute sous-chaîne d'un réglage JSON. Un réglage ne peut donc plus citer l'identifiant, même dans une description ou une permission.
- **E-7** : les cas de commentaire emploient `claude-opus-5-5`. Le contrôle ne dépend pas de l'identifiant, et ces cas montrent aussi leur rouge contre la base.
- **E-8** : base du dépôt réel avancée pendant la passe (voir plus haut).
- **E-9** : recompte des fichiers lus par une énumération de l'archive et de ma copie (comptes seuls).
- **E-10** : `du -sh` sur un seul dossier de la revue, avant d'en copier la cible de compilation.
- **E-11** : verify n'a tourné que sur la copie avec exclusions.
- **E-12** : les campagnes antérieures (N-, R-, GM-) ne sont pas rejouées, le brief ne le demandant pas.
- **E-13** : les renvois à CLAUDE.md (l.23-49 et l.35-42) sont exacts.

## Items à former

- **L-1 (neuf, la base fait pareil)** : un agent dont la seule ligne `model` est dans un flux ouvert sur plusieurs lignes (ou dans une chaîne entre guillemets sur plusieurs lignes) est compté comme ayant un modèle et admis. En réalité il hérite du modèle de session. Le remède tient en une condition ; je ne l'ai pas fait, c'est hors lot.
- **I-R-2** : `advisorModel:` n'est pas lu dans un frontmatter (hors lot, §7).
- **I-2** : la clé `env` n'est couverte que pour Haiku.
- **I-c, I-d, I-R-3, I-e, I-f, I-3, I-4, I-5** : toujours ouverts. S'y ajoute la durée du runner sous Git Bash, non mesurée, contre une borne de 5 min pour le job.

## Questions

- **Q-1** : garde-t-on le refus de l'UTF-8 invalide sur toute ligne du frontmatter (E-4) ?
- **Q-2** : garde-t-on le prix des flux (E-5), ou préfère-t-on refuser tout flux ouvert sur plusieurs lignes ?
- **Q-3** : garde-t-on « partout » au sens de toute sous-chaîne dans les réglages JSON (E-6) ?
- **Q-4** : ouvre-t-on un lot pour L-1 ?

`SHA256SUMS` couvre le rapport, `NOTES.md` et le reste des livrables (190 lignes, `sha256sum -c` OK) ; son empreinte est dc2c5131ccafb3686763a3d3500188eb9edad14955481dd465973ad15b13f59b, celle du rapport 642fc79cb584697101d403f49d9f4dfa6fcdbed336d40c2129d060abc3ee23aa. Le rapport complet (tables des rouges et des mutants, mesures, journal de provenance) et les notes horodatées sont dans les fichiers ci-dessous.

Fichiers, dans `<scratchpad>/lot-haiku/corr3/` :
- `diffs/LH-1.diff`
- `diffs/LH-2.diff`
- `RAPPORT-CORRECTIONS.md`
- `NOTES.md`
- `SHA256SUMS`
- `logs/`
- `mutants/`
- `scripts/`
- `tmp/final/` (base + LH-1 + LH-2)
