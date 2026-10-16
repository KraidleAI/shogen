# Relecture G2 neuve du correctif CQ-1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:48:15 UTC du fichier codeql-pr12/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (89 occurrences). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 : correctif CQ-1 (alertes CodeQL de la PR n° 12 sur `.claude/hooks/garde_faits.py`)

- **Rôle** : réviseur G2, neuf (réviseur ≠ générateur ; le générateur est l'orchestrateur `claude-fable-5-1`).
- **Modèle résolu** : `claude-opus-5-5` (effort `high`).
- **Date** : 2026-10-16 12:34 UTC (`date -u`).
- **Base relue** : copie `/home/user/shogen`, branche `claude/compassionate-noether-szmdyj`, HEAD
  `c94fa9fa3e98d48fd12a2f37baaf49a4e2ec790f` (base du brief : `c94fa9f`, égale). L'arbre porte exactement `CQ-1.diff` :
  `git diff HEAD` limité aux quatre chemins du lot est identique octet pour octet à la pièce (`cmp`, sha256
  `3c02009c…a681663e`) (preuves/02, preuves/03).
- **Rattachement** : brief, ADR-0028 annexe B, B.108 (`docs/adr-0028/ANNEXE-B-items.md:1858`) ; le rapport du
  générateur cite B.102 (`:1756`, item SHOGEN-GARDE-FOUS-ORCH-1). Les deux blocs portent le lot ; écart sans effet.
- **Sommes des pièces** : les cinq lignes de `SHA256SUMS-generateur.txt` sont OK une fois `<scratchpad>` remplacé par
  le chemin réel (preuves/01). La forme `<scratchpad>/…` ne se rejoue pas telle quelle par `sha256sum -c`.
  `test_garde_codeql.py`, `M1.out` à `M3.out` ne sont pas dans les sommes ; la copie de `test_garde_codeql.py` est
  identique au fichier de l'arbre (`cmp`).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-4, liste fermée)

La partie `NOM_PROPRE` est juste : même langage et mêmes occurrences (preuve ci-dessous), retour arrière exponentiel
supprimé (mesure). La partie `hote_forge` introduit **un contournement complet du crochet** (C-1) et **desserre** R5
sur des actes réels vers la forge (C-2). Ces deux défauts bloquent l'acceptation en l'état ; les corrections sont
écrites au texte exact, appliquées sur une copie et prouvées (tests verts, mutants tués).

### Constat principal : à quoi sert `forge`

`f["forge"]` vrai ajoute le texte de la commande à `textes_ecrits` (`.claude/hooks/garde_faits.py:633-634`). R5 juge
ensuite ce texte : il refuse un identifiant de commit ou un numéro de PR qu'aucun outil n'a affiché. Une inclusion de
trop ne coûte donc qu'un contrôle R5 en plus : c'est le sens sûr. Une exclusion retire ce contrôle. L'alerte
`py/incomplete-url-substring-sanitization` suppose l'inverse (un filtre qui laisse passer une URL hostile). Ici,
l'ancienne sous-chaîne `"api.github.com" in c` jugeait seulement trop de commandes. Le rapport du générateur dit qu'une
telle commande `passait pour une lecture de la forge` : l'effet réel était un R5 de plus, sans aucun dégât.
Retirer ces faux positifs est admis. Retirer des actes réels vers la forge ne l'est pas (règle 7 : serrer, jamais
desserrer).

## Corrections

**C-1 (bloquante) — `.claude/hooks/garde_faits.py:379`** : `urlsplit` lève `ValueError` sur une URL à crochet
mal formé (`http://[`, `http://[::1`). L'exception remonte de `faits_de_la_commande` jusqu'au `except Exception` de
`main` (`:860-863`), qui écrit `erreur interne … acte permis sans contrôle` et sort 0. Un seul mot ajouté à une
commande suffit donc à faire sauter R1, R2, R3, R5 et R7 pour toute la commande. Mesure sur le crochet entier, journal
synthétique vide (preuves/08) :
`curl 'http://[' ; git commit -m 'essai'` sort 2 (refus R3) sous l'ancien crochet, mais 0 sous le neuf, avec
`GARDE-FAITS : erreur interne (ValueError('Invalid IPv6 URL')) ; acte permis sans contrôle.`
La seule commande `git commit -m 'essai'` sort 2 sous les deux crochets.
Texte exact : remplacer les l.375-379 (`def hote_forge(mots):` jusqu'à `return any(…)`) par :

```python
def hote_forge(mots):
    """Vrai si un mot de la commande vise l'API de la forge : URL dont l'hôte, lu par urlsplit (jamais par sous-chaîne),
    est api.github.com (schéma en toute casse, point final admis) ; mot sans schéma dont l'hôte est api.github.com (curl
    le lit en http) ; URL que urlsplit refuse (ValueError : sens sûr, jamais une erreur interne). Une URL d'un autre hôte
    dont le chemin, la requête ou un sous-domaine porte « api.github.com » ne compte pas."""
    for x in mots:
        if re.match(r"(?i)https?://", x):
            try:
                h = urlsplit(x).hostname or ""
            except ValueError:
                return True
        else:
            h = re.sub(r":[0-9]*$", "", re.split(r"[/?#]", x, maxsplit=1)[0].rsplit("@", 1)[-1]).lower()
        if h.rstrip(".") == "api.github.com":
            return True
    return False
```

(Texte au fichier `g2/proposition/hote_forge.txt`, à partir de sa l.4, sha256 `cdb3ee47…`. Ce texte porte aussi les
branches que réclame C-2.)

**C-2 (bloquante) — `.claude/hooks/garde_faits.py:378` et `:417`** : régressions mesurées, vraies sous l'ancien code,
fausses sous le neuf, sur des actes réels vers la forge (preuves/07, preuves/08) :
- `curl HTTPS://api.github.com/…` : `startswith(("http://", "https://"))` respecte la casse, alors que curl 8.5.0 lit
  le schéma en minuscules (`curl -sS --proto -all 'HTTPS://example.invalid/x'` rend `Protocol "https" not supported or
  disabled`, sans aucune connexion ; preuves/14) ;
- `curl api.github.com/repos/o/r` (sans schéma ; curl le lit en `http`, même preuve) ;
- `curl https://api.github.com./…` (point final) ;
- `U=https://api.github.com/repos/o/r; curl -d '…1a2b3c4d…' "$U/issues/1/comments"` : URL dans une variable du shell.
  L'ancien code la voyait dans `c` ; `hote_forge` ne lit que les mots, où `$U` n'est pas développé. Sous l'ancien
  crochet : refus R5 (sortie 2) ; sous le neuf : sortie 0 (preuves/08).
Texte exact : la fonction de C-1 couvre les trois premiers cas. Pour le quatrième, insérer avant la l.134
(`FORGE_JOB = …`) la ligne
`FORGE_HOTE = re.compile(r"(?i)(?<![\w-])api\.github\.com(?![\w-])")     # hôte de la forge dans le texte (sens sûr)`
et remplacer la l.417 par les deux lignes :

```python
        elif p == "gh" and m[1:2] in (["pr"], ["issue"], ["api"], ["release"]) or p == "curl" and (
                hote_forge(m) or any(re.search("[$`]", x) for x in m[1:]) and FORGE_HOTE.search(c)):
```

**C-3 — `scripts/controle/tests/test_garde_codeql.py:52-56`** : aucun test ne garde C-1 ni C-2. Remplacer les l.52-56
(`oui = (` jusqu'à la fin du tuple `non`) par le bloc de `g2/proposition/test_bloc.txt` (sha256 `60737685…`) :

```python
        oui = ("curl -s https://api.github.com/repos/o/r/actions/runs", "curl -H 'A: b' https://api.github.com:443/x",
               "curl http://api.github.com/x", "curl HTTPS://api.github.com/x", "curl api.github.com/repos/o/r",
               "curl https://api.github.com./x", "U=https://api.github.com/repos/o/r; curl \"$U/issues\"",
               "curl 'http://[' https://evil.example/")
        non = ("curl https://evil.example/api.github.com/x", "curl https://api.github.com.evil.example/x",
               "curl https://evil.example/?u=api.github.com", "curl https://notapi.github.com/x",
               "curl -d x=api.github.com https://evil.example/", "curl https://github.com/o/r",
               "U=https://evil.example/r; curl \"$U/x\"", "U=https://notapi.github.com/r; curl \"$U/x\"")
```

Le cas `curl -d api.github.com https://evil.example/` devient `curl -d x=api.github.com …`. Avec C-1, un mot nu
`api.github.com` compte comme hôte (sens sûr : on ne lit pas les options de curl) ; une donnée qui nomme l'hôte reste
exclue. Le compte des tests ne change pas (cas ajoutés dans un test existant) : le plancher 177 tient.

**C-4 — `scripts/controle/README.md:694`** : remplacer
`` > `urlsplit`) ; plancher du job `controle-unittest` 177. ``
par
`` > `urlsplit`, sens sûr : schéma en toute casse, mot sans schéma, URL que `urlsplit` refuse, URL dans une variable du shell) ; plancher du job `controle-unittest` 177. ``

### Preuve des corrections (copie `g2/copie-corrige`, jamais l'arbre ; diff `g2/proposition/C-corrige.diff`, sha256 `a1ca0992…`)
- `tests.test_garde_codeql` corrigé, contre le crochet corrigé, sous `-X dev -W error` : `Ran 3 tests`, `OK`,
  sortie 0, aucune ligne `Exception ignored` ni `Warning`. Le même test contre le crochet du générateur : rouge
  (`False is not true : curl HTTPS://api.github.com/x`), ce qui montre que les cas ajoutés séparent les deux versions
  (preuves/18).
- Les 30 tests de `test_garde_codeql`, `test_garde_acte`, `test_garde_regex` et `test_garde_suivi`, rejoués sur une
  copie de `scripts/controle` : mêmes quatre rouges d'artefact de copie sous le crochet du générateur et sous le
  crochet corrigé (`.claude/settings.json` absent, dépôt git absent) ; les 26 autres sont verts dans les deux cas
  (preuves/16).
- Crochet entier corrigé : les cinq commandes de preuves/08 sortent toutes 2. Le contournement de C-1 est fermé ;
  R5 juge de nouveau la variable et la forme sans schéma (preuves/20).
- Tableau ancien/corrigé (preuves/19) : les seules différences restantes sont les faux positifs voulus par le
  générateur (autre hôte, chemin, requête, `@`, fragment) et `API.GITHUB.COM`, désormais reconnu (serrage).
- `motifs_suspects` (E12) sur les cinq motifs neufs : aucune forme suspecte (preuves/23).
- Mutants de la proposition, K1 à K11 (preuves/17) : 11 tués sur 11 (sortie 1), aucun FATAL, 0 processus restant.
  K1 et K2 reprennent M1 et M2 ; K3 est la sous-chaîne d'hôte (M3) ; K4 rend `raise` au lieu de `return True` ;
  K5 ôte `(?i)` ; K6 vide la branche sans schéma ; K7 ôte `rstrip(".")` ; K8 et K9 mutent le repli sur variable ;
  K10 ôte le regard arrière de `FORGE_HOTE` (vivant avant l'ajout du cas `notapi` en variable, tué après) ;
  K11 mute le site d'appel (`hote_forge(m[:1])`).

## Point 1 de la checklist : `NOM_PROPRE` (`.claude/hooks/garde_faits.py:131`) — juste
- **Preuve d'équivalence** : les deux motifs ne diffèrent que dans le groupe répété de la première alternative.
  (a) Langages : `(?:[A-Z][A-Za-z0-9]*)+` et `(?:[A-Z][a-z0-9]*)+` décrivent tous deux `[A-Z][A-Za-z0-9]*`. Le second
  s'obtient en coupant la chaîne avant chaque majuscule ; l'inclusion inverse est immédiate.
  (b) Ordre d'essai : le regard avant `(?![\w-])` refuse toute fin placée à l'intérieur d'une suite de `[A-Za-z0-9]`,
  car ces signes sont tous dans `\w`. Une réussite de la première alternative finit donc à la fin de la suite
  maximale, quel que soit le chemin du moteur : même réussite, même occurrence, et la même retombée sur les
  alternatives 2 et 3 en cas d'échec. Le regard arrière et les alternatives 2 et 3 ne changent pas.
  Contrôle mécanique (preuves/05) : langages des groupes égaux à `[A-Z][A-Za-z0-9]*` sur les 524 287 mots de
  classes de longueur 0 à 18 ; `finditer` (étendues et groupe 1) égaux sur 3 257 436 chaînes, toutes celles de
  longueur 1 à 6 sur l'alphabet `ABa0 -_.@/éÉ`, et sur 300 000 chaînes tirées au hasard (graine 20261016, longueur 1 à
  40, 21 signes) : 0 différence.
- **Temps** (preuves/06, Python 3.11.15) : l'ancien motif sur `A0A`+n×`A`+`-` passe de 0,0025 s (n = 14) à 2,1 s
  (n = 24), soit environ ×4 par pas de 2. Le neuf prend 0,000004 s à n = 26 et 0,0087 s à n = 100 000 ; six autres
  formes adverses restent linéaires jusqu'à n = 100 000 (au plus 0,053 s).
- Le détecteur `garde_commun.motifs_suspects` signale bien l'ancien motif (`quantificateurs-imbriques`) et rien sur
  le neuf (preuves/12). La limite du générateur se précise ainsi : le détecteur est juste ; il n'a simplement jamais
  été lancé sur les motifs déjà présents dans l'arbre (voir L-1).

## Point 3 : tests et mutants du générateur rejoués (copies `g2/mut-*`, jamais l'arbre ; preuves/13)
| mutant | test rouge | sortie | classement |
|---|---|---|---|
| témoin (crochet du générateur) | aucun | 0 | vert |
| M1 (`M1.diff`) | `test_nom_propre_temps_borne` (`7.43 not less than 1.0`) | 1 | tué |
| M2 (`M2.diff`) | `test_nom_propre_memes_mots` (`[] != ['AA']`) | 1 | tué |
| M3 (`M3.diff`) | `test_curl_hote_de_la_forge` (`api.github.com.evil.example` accepté) | 1 | tué |
Chaque mutant ne fait rougir que son test ; les deux autres restent verts ; 0 processus restant.
**Valeur inerte, E13** : `avant_acte.py --lecture-seule diff --fichier CQ-1.diff --rapport RAPPORT-GENERATEUR.md`
sort 0 (preuves/11) : D4 trouve chacun des trois tests sur une ligne du rapport qui dit `mutant tué`. D3 est sans
objet (aucune fonction publique ajoutée sous `scripts/controle/*.py`). Aucune valeur n'est inerte : l'entrée
`A0A`+26×`A`+`-` déclenche bien le retour arrière de l'ancien motif (8 s mesurées) ; le test 2 compare à une copie
indépendante de l'ancien motif, écrite dans le test ; les cas de M3 séparent égalité et sous-chaîne.

## Point 4 : README, plancher, suite
- `.github/workflows/gates.yml:369` : plancher 174 → 177. Aucune autre occurrence du plancher dans `enforcement/`,
  `scripts/`, `.github/` ou `s2-harness/`, hors README.
- `scripts/controle/README.md:692-694` : ajout daté (`2026-10-16 12:17:57 UTC`), trois tests nommés, plancher 177.
- `env -u SHOGEN_S2_CAMPAGNE_CONTROL TMPDIR=g2/tmp python3 -B enforcement/verdict-suite-s2.py scripts/controle
  --aucun-saut --egal --plancher 177`, lancé dans l'arbre : `Ran 177 tests`, `OK`,
  `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 177)`, sortie 0, aucune ligne
  `Exception ignored` ni `Warning` (preuves/09). `run-fixtures-verdict-suite-s2.py` : `153 ok, 0 échec`
  (preuves/10). `git status` des chemins du lot est inchangé après ces runs.

## Point 5 : S-G5 et R-13
Aucun marqueur de dette dans les lignes ajoutées (CQ-1 comme proposition). Les textes entre « » sont `« A »`,
`« A0A »` et `« api.github.com »` : un nom d'hôte et des lettres, sans texte anglais (preuves/21).

## Constats mineurs (sans correction exigée)
- O-1 `RAPPORT-GENERATEUR.md` (section Mutants, M2) dit que `« AB »` est reconnu par le mutant seul ; la sortie
  `M2.out` montre `AA`.
- O-2 La docstring de `test_curl_hote_de_la_forge` (`scripts/controle/tests/test_garde_codeql.py:49-50`) et le rapport
  parlent de `lecture de la forge` ; `forge` couvre aussi les écritures (R5).
- O-3 Les M*.out du générateur portent des chemins `/home/user/shogen/…` : les mutants ont été joués dans l'arbre,
  puis le crochet rendu à ses octets (`garde_faits.sain.py` est égal à l'arbre, `cmp`). La fiche demande une copie à
  part (outil commun `scripts/controle/mutants.py`).
- O-4 Enregistrement de rôle `oracle_record.py` : sans objet, le lot n'est pas sur le chemin S2 (cp-2).

## Limites (items à former, règle PAROXYSME)
- L-1 Les motifs déjà présents dans l'arbre des crochets et outils ne passent jamais `motifs_suspects` (E12 ne juge
  que les motifs ajoutés) : il faudrait un balayage de l'arbre (rapport du générateur, confirmé par preuves/12).
- L-2 CodeQL n'a pas été rejoué ici (aucun réseau, outil absent) : rien ne garantit que la proposition C-1/C-2 ne
  lève pas une autre alerte (`FORGE_HOTE` est une expression sans ancre, aux points échappés). L'orchestrateur la juge
  au contrôle CodeQL de la PR. Si une alerte réapparaît, elle est fausse dans ce sens-ci (inclusion de trop = R5 de
  plus) et se ferme par justification écrite, jamais en retirant le repli.
- L-3 La suite complète `scripts/controle` n'a pas été rejouée avec la correction : l'arbre ne se modifie pas, et une
  copie complète exigerait `docs/`. Rejouée sur le diff du générateur : conforme, Ran = 177. L'orchestrateur la
  rejoue après application de C-1 à C-4 (plancher inchangé, 177).
- L-4 Une commande illisible par `shlex` passe par la voie des motifs, qui ne voit pas `curl` vers la forge
  (preuves/22, ancien et neuf égaux). Sans dégât mesuré : bash refuse lui-même la guillemet non fermée.

## Journal de provenance (G1)
Sources [lu] : `BRIEF-G2.md`, `RAPPORT-GENERATEUR.md`, `CQ-1.diff`, `M1-3.diff`, `M1-3.out`, `test_garde_codeql.py` ;
`.claude/hooks/garde_faits.py` (l.1-125, 330-425, 480-500, 590-700, 830-870) ; `scripts/controle/README.md`
(l.609, 630-645, 688-694) ; `scripts/controle/avant_acte.py` (l.1-30, 80-110, 179-190, 575-625) ;
`scripts/controle/tests/aide_garde.py` (l.1-30) ; `enforcement/verdict-suite-s2.py` (l.1-40) ;
`.github/workflows/gates.yml` (l.355-369) ; `docs/adr-0028/ANNEXE-B-items.md` (l.1756-1771 et 1858-1880, lus par `grep -n`
et `sed -n` sur ce seul fichier). Aucune pièce interdite ouverte, aucune recherche récursive sous `docs/`, aucun
`*.jsonl`, aucun réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `env -u`), TMPDIR sous `g2/tmp`.
Commandes et sorties : `g2/preuves/01` à `23` ; scripts sous `g2/scripts/` ; sommes dans `g2/preuves/SHA256SUMS.txt`.
Chiffres recomptés ici : tous ceux de ce rapport.
