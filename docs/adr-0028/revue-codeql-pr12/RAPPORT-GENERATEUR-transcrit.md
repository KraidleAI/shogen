# Rapport du générateur du correctif CQ-1 (l'orchestrateur) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:48:15 UTC du fichier codeql-pr12/RAPPORT-GENERATEUR.md ; générateur : l'orchestrateur lui-même, pas de transcript d'agent. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : correctif CQ-1 (alertes CodeQL de la PR n° 12 sur le crochet GARDE-FAITS)

Générateur : l'orchestrateur (`claude-fable-5-1`), 2026-10-16 12:21:20 UTC. Rattachement : ADR-0028, annexe B, B.102 (SHOGEN-GARDE-FOUS-ORCH-1, phase 2) ; précédent DT5-24 (B.94).

## Constat (contrôle CodeQL de la PR n° 12, tête c94fa9f, deux alertes « high »)
- `py/redos` l.130 : `NOM_PROPRE`, groupe `(?:[A-Z][A-Za-z0-9]*)+` : une majuscule peut ouvrir un groupe ou prolonger le précédent ; sur « A0A » + n « A » + « - » (regard avant qui échoue) le temps double par « A » (mesuré : 0,009 s à 16, 0,111 s à 20, 0,447 s à 22).
- `py/incomplete-url-substring-sanitization` l.409 : `"api.github.com" in c` : une commande curl vers un autre hôte dont le chemin porte ces mots passait pour une lecture de la forge.

## Correctif (diff `CQ-1.diff`, +15/−3 hors test)
- `NOM_PROPRE` : `(?:[A-Z][a-z0-9]*)+` : chaque groupe commence par la seule majuscule qu'il porte ; même langage (preuve : 95 986 chaînes de longueur 1 à 8 sur un alphabet de six à neuf signes, mêmes occurrences ; onze noms réels) ; temps 0,00001 s sur l'entrée adverse.
- `hote_forge(mots)` : hôte de chaque URL de la commande lu par `urllib.parse.urlsplit`, égalité stricte à `api.github.com` ; port admis, sous-domaine, chemin et requête refusés.
- `tests/test_garde_codeql.py` : 3 tests ; README des contrôles : ajout daté ; plancher `controle-unittest` 174 → 177 (suite rejouée : conforme, Ran = 177).

## Mutants (à la main, un par test ; crochet rendu à ses octets, `cmp`)
- M1 (`M1.diff`) : groupe rendu à `(?:[A-Z][A-Za-z0-9]*)+` : test_nom_propre_temps_borne rouge (AssertionError, temps > 1 s) : mutant tué.
- M2 (`M2.diff`) : `[A-Z]{3,}` → `[A-Z]{2,}` : test_nom_propre_memes_mots rouge (« AB » reconnu par le mutant seul) : mutant tué.
- M3 (`M3.diff`) : égalité d'hôte rendue à une sous-chaîne : test_curl_hote_de_la_forge rouge (`api.github.com.evil.example` accepté) : mutant tué.

## Limite
- Le lint statique `motifs_suspects` (P2A-5) n'a pas signalé `NOM_PROPRE` dans le crochet : il juge les diffs reçus, et le motif date de la phase 1 ; item à former (voir adjudication).

## Corrections de la G2 (C-1 à C-4) appliquées par l orchestrateur
- Diff final `CQ-1b.diff` ; mutants K1 à K11 du réviseur (11 tués sur 11, preuves/17 de la G2) : M1 à M3 reprises par K1 à K3 ; mutants tués consignés pour test_nom_propre_temps_borne (K1), test_nom_propre_memes_mots (K2), test_curl_hote_de_la_forge (K3 à K11).
