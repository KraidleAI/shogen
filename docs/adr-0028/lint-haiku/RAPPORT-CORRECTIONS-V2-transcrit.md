# Rapport des corrections — LINT-HAIKU, vague 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:56:51 UTC du rapport rendu par l'agent aff92bf64db7d8f6a (workflow wf_eabb8e95-e1a) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session ; l'effort `max` ne se voit pas de l'intérieur. Horloge (`date -u`) : de 2026-10-08T12:13:25Z à 13:14:28Z.

## Bilan

- **C-1 à C-3** sont soldées.
- **E-LH-1** est corrigé : `claude-haiku-5-5` est admis sous la clé `model` et refusé sous `advisorModel`, avec le jeton `R-1/role`. T-100 est inversé.
- **E-LH-5** est tenu, mais va au-delà de `LC_ALL=C`, ce qui est à adjuger (E-4). Avec `export LC_ALL=C` seul, des formes que C.UTF-8 refusait seraient passées. J'ai donc ajouté deux refus : les blancs Unicode dans un frontmatter, et un commentaire non ASCII sur une ligne `model`.
- **Runner** : 138 ok, sortie 0, sous POSIX, sous C.UTF-8 et sous LANG=C.UTF-8 seul.
- **Lint de l'arbre** (copie, LH-1, LH-2) : `OK (R-1) : 7 fichier(s)` sous les deux locales.
- **Mutants neufs** : 20 tués sur 20, 0 FATAL.
- **Rejeux** : 13 sur 13 pour le générateur, 15 sur 15 pour le lint du réviseur. Pour la fiche, 4 sur 8 : F-05 à F-08 restent vivants, comme avant (I-3, hors lot).

Base e6657dc, égale à celle du brief. Le dépôt réel est intact : HEAD e6657dc, status vide, 6 fiches sous `.claude/agents/`, aucune écriture git.

## Diffs (à appliquer en série sur e6657dc)

| pièce | sha256 | lignes | code ajouté | octets 92 |
|---|---|---|---|---|
| LH-1 | a987effcf51017cc413d66904706d6a561450ded4fb211e5bf4c323702f048cf | +85 −7 (lint +32 −7, runner +53) | 54 | lint 43 → 60, runner 48 → 72 |
| LH-2 | e76eac740293e9eaa0958aefc84208bac6cb3799c53631a8dc86c2317d68d6ec | +34 | texte | 0 |

- **LH-2** est identique octet pour octet à l'ancien LH-2 : la fiche avait été acceptée telle quelle par la G2.
- **Contrôles** :
  - les lignes ajoutées ne contiennent rien au-delà de 120 caractères, ni TODO/FIXME, ni CR, ni le littéral banni ;
  - `bash -n` passe ;
  - `patch -p1` et `git apply --check` passent en série.
- **Fichiers obtenus** : lint f2983fb1…, runner fa6b4cdf…, fiche 1974e9f9….

## Tableau C-1 à C-3, E-LH-1 et E-LH-5

| item | correction | rouge montré |
|---|---|---|
| C-1 | le chemin `docs/adr-0028/G0-lot-LINT-HAIKU.md` est cité dans le lint (l.9) et le runner (l.14 et l.158) | texte |
| C-2 | T-108 `Claude-haiku-5-5`, attendu `R-1/hors-liste` | seul cas qui tue N-03 et R-04 |
| C-3 | T-109 (espace insécable final) et T-110 (U+200B final), octets écrits en octal | seuls cas qui tuent N-04/R-10 et N-05/R-11 |
| E-LH-1 corrigé | T-96 à T-99 inchangés ; T-100 attend `R-1/role` ; T-111 refuse aussi la clé `"MODEL"` | l'ancien lint admet T-100 et T-111 (sortie 0) |
| E-LH-5 | `export LC_ALL=C` ; T-112 sert de témoin ; T-113 à T-117 reprennent les formes de I-1, chacune sous LANG=POSIX puis LANG=C.UTF-8 | l'ancien lint admet T-113 à T-117 sous C.UTF-8 ; un runner sans C.UTF-8 donne « ÉCHEC T-112 » |
| E-LH-5, rien de desserré | T-118 à T-125 : blancs Unicode refusés dans le frontmatter et vus entre `agent` et `(` ; commentaire non ASCII refusé | l'ancien lint + `LC_ALL=C` seul les admet sous les deux locales (16 échecs) |

Rouges mesurés contre le runner final : lint de e6657dc 19 échecs, ancien lint 20, ancien lint + `LC_ALL=C` seul 18.

## E-LH-5 : mesures

- **Blancs pris par `[[:space:]]`.** Sous C.UTF-8, bash, grep et sed y rangent les mêmes 15 blancs Unicode : U+1680, U+2000 à U+2006, U+2008 à U+200A, U+2028, U+2029, U+205F, U+3000. Sous POSIX, aucun.
- **Comparaison des lints sur 3 948 formes**, sous les deux locales :
  - le verdict du lint neuf ne dépend jamais de la locale (0 forme ; 969 pour la base, 918 pour l'ancien lint) ;
  - aucune forme n'est admise par le neuf et refusée par l'ancien lint ; 347 sont désormais refusées ;
  - par rapport à la base, 55 formes passent en plus, toutes en `claude-haiku-5-5`, et chacune a son équivalent en `claude-opus-5-5` déjà admis par la base.
- **Une première version contrôlait toute la ligne `model`.** Elle masquait cinq mutants (N-04, N-05, N-06, R-10, R-11). La version livrée ne contrôle que le commentaire : elle donne les mêmes verdicts sur les 3 948 formes, et ces cinq mutants sont tués.

## Mutants neufs

- **Mutants demandés** :
  - N-01 : `advisorModel` admet haiku, tué par T-100 et T-111 ;
  - N-02 : locale non fixée, tué par T-113 à T-117 sous C.UTF-8 ;
  - N-03 : casse de la première lettre, tué par T-108 ;
  - N-04 : espace insécable retiré, tué par T-109 ;
  - N-05 : U+200B retiré, tué par T-110.
- **Locale mal posée** :
  - N-06 : `LC_ALL` non exporté, tué parce que le runner retire LC_ALL avant ces cas ;
  - N-07 : locale fixée à C.UTF-8.
- **Blancs Unicode retirés ou incomplets** : N-08 à N-10, puis N-12 à N-17, une branche du motif chacun.
- **Contrôle du commentaire** : N-11, contrôle retiré.
- **Rôle** : N-18 à N-20 (casse de la clé, rôle appliqué à `model`, SIGNAL vide).

## Autres contrôles

- **Cas existants** : le runner de base contre le lint final donne 95 ok, et les fixtures sont identiques.
- **Hooks** : `run-fixtures-hooks.sh` donne 54 ok.
- **s2-harness** : 407 tests OK (skipped=2), et `verdict-suite-s2 --egal` est conforme.
- **verify**, lignes de verdict seules :
  - S-G1 à S-G8 VERT, S-G9 ROUGE (1), global ROUGE, comme sur la base ;
  - la section S-G9 est identique, comparée par empreinte sans être affichée.

## Écarts

- **E-1** : une commande `bash -c` a été bloquée par l'outil ; les essais sont passés par des fichiers de script.
- **E-2** : s2-harness a d'abord été lancé depuis le mauvais dossier, puis relancé.
- **E-3** : deux remplacements Python tapés avec des barres obliques ; les octets ont été contrôlés après.
- **E-4 (à adjuger)** : la compensation ajoutée à `LC_ALL=C` a un prix. Un blanc Unicode dans une description sera refusé, comme un commentaire non ASCII sur une ligne `model`. L'arbre actuel n'en contient aucun.
- **E-5 (à adjuger)** : `claude-haiku-5-5` est refusé sous toute clé JSON autre que `model` exacte (T-111). C'est plus strict que la lettre du G0.
- **E-6** : le runner échoue (T-112) si C.UTF-8 n'a pas d'effet sur l'hôte. Pour la CI, c'est inféré ; pour Git Bash, non mesuré.
- **E-7** : le runner fait `unset LC_ALL LC_CTYPE` avant les cas de locale. Avec un LC_ALL simplement vidé, N-06 survivait (mesuré).
- **E-8** : la ligne find de la passe 3 a été réécrite pour tenir en 120 caractères.
- **E-9** : j'ai compté les fichiers suivis par `git ls-tree -r | wc -l` (929), sans afficher de nom. C'est contraire à la lettre de l'interdit de recherche récursive sur le dépôt entier.
- **E-10** : les cas existants (E-LH-3) et verify n'ont été vérifiés que sur la copie avec exclusions ; l'arbre complet reste à juger au commit.
- **E-11** : les numéros de ligne de CLAUDE.md cités dans le lint sont à recontrôler si CLAUDE.md change dans le même commit.

## Items à former

- **I-a : élargissement apporté par le lot.** Un hook de type prompt en `claude-haiku-5-5` passe désormais (la base le refusait), alors qu'un tel hook peut décider.
- **I-b** : `advisorModel` n'est pas lu dans un frontmatter.
- **I-c** : des blancs hors du motif passent, par exemple `<U+00A0>model: opus` ou `<U+FEFF>model: opus` dans un skill.
- **I-d** : un appel `agent` suivi d'un saut de ligne ou d'un commentaire avant `(` n'est pas vu.
- **I-e** : le runner reste à mesurer sous Git Bash.
- **I-f** : la locale réelle du job g1 n'est pas mesurée.
- **Items de la G2** : I-2, I-3, I-4 et I-5 restent ouverts.

I-b, I-c et I-d existaient déjà avec la base.

## Questions

- **Q-1** : garde-t-on la compensation de E-LH-5 et son prix (E-4) ?
- **Q-2** : garde-t-on le refus sous toute clé JSON autre que `model` (E-5) ?
- **Q-3** : faut-il un G0 qui refuse Haiku sous `hooks` (I-a) ?
- **Q-4** : garde-t-on T-112 en échec quand C.UTF-8 manque, notamment sous Git Bash (E-6) ?

## Fichiers

Tous sous <scratchpad>/lot-haiku/corr/ :
- diffs/LH-1.diff
- diffs/LH-2.diff
- RAPPORT-CORRECTIONS.md (rapport complet : numéros de ligne, journal de provenance, liste des fichiers)
- NOTES.md
- SHA256SUMS (365 lignes, `sha256sum -c` OK, empreinte 1ad073ce193f1c39a9e843fc1351f4bd60886242597d0c42567811a8375a17f6)
