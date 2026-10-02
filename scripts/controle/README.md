# Outils de contrôle de l'orchestrateur (versés le 2026-10-02, partie 4 de S2, étape P2)

Outils écrits par l'orchestrateur de la session cloud du 2026-10-02 pour adjuger les lots des parties 2 et 3, versés
**à l'octet** (sha256 égaux à ceux que citent l'annexe B et le JOURNAL) pour qu'un réviseur puisse les relire et les
rejouer (SHOGEN-FM11-VERIFIABLE-1, SHOGEN-REGLE-EMPREINTE-OUTIL-1 ; annexe B.35). Hors des chemins de la garde (2)
(`s2-harness/shogen_s2`, `s2-harness/tools`) et hors de la suite `s2-harness` : ils ne changent ni le bloc machine du
paquet ni ce que lance l'exécution unique.

| fichier | sha256 | rôle | usage |
|---|---|---|---|
| `fm11.py` | `886cc676874e70e3fe49a259fda6cfc8591882d511a29edded5c651860c1e254` | contrôle FM-1.1 non-LLM d'une transcription de sous-agent (annexe C l.13) : repère par leur sha256 (jamais affichées) la cartographie du 2026-09-29 l.51 et ADR-0025 l.14 (`7f8b5cc`), cherche leurs fragments de 40 caractères et les noms de pièces de D.2 dans les résultats et les entrées d'outils ; n'affiche que des comptes | `python3 fm11.py <transcription.jsonl>` ; chemin du dépôt écrit en dur (`REPO = '/home/user/shogen'`, l.4) |
| `regle_fixtures.py` | `5557fb56e5edc3b4c0e3a736b65110d466a7b5118aa4e02bb7ea63d75e92f8ab` | valeurs de `r1.regle_critere` sur les 16 fixtures de `tests/test_critere.py` (U1-U8, J1, J1-ℓ1, J2, J3-ℓ1, J5, J4) ; JSON dont le sha256 attendu est `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` (non-régression de la règle, parties 2 et 3) | `python3 -B regle_fixtures.py <arbre s2-harness> <sortie.json>` |
| `render_fixture.py` | `4084c42b59ea7d7ce356f04a0ea05bb1ff3646de25b46dc571156dd249d2b395` | rendus de la fixture de `test_exclusion` sans et avec l'option PLAGE ; sha256 attendus = épingles `SHA_BASE_SANS_OPTION` (`4e62fbb8…`) et `SHA_BASE_AVEC_OPTION` (`d079dd9d…`) | `python3 -B render_fixture.py <arbre s2-harness> <dossier>` |

Sorties FM-1.1 versées (`sorties-fm11/`) : `redacteur.json`, `redacteur-final.json` (annexe B.32, B.33), `validateur.json`,
`validateur-final.json` (B.33), `g2p3.json` (B.35), `corr-worker.json` (worker G1 du lot CORR, partie 4). Elles portent des comptes, des noms d'outils et des numéros
d'événements, aucun extrait de transcription ; les transcriptions elles-mêmes ne sont pas versées (D.2 n° 11 pour celle
de l'orchestrateur ; celles des sous-agents restent dans la session).

Limites : `fm11.py` ne détecte que les fragments exacts de 40 caractères et les motifs nommés (une paraphrase n'est pas
détectée) ; son témoin positif (fragment de la l.51 injecté dans un résultat d'outil, détecté) a été rejoué le
2026-10-02 (annexe B.32) mais n'est pas versé comme test automatique ; `regle_fixtures.py` et `render_fixture.py`
dépendent des tests du harnais qu'ils importent.
