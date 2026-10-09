# Outils de contrôle de l'orchestrateur (versés le 2026-10-02, partie 4 de S2, étape P2)

Outils écrits par l'orchestrateur de la session cloud du 2026-10-02 pour adjuger les lots des parties 2 et 3, versés
**à l'octet** (sha256 égaux à ceux que citent l'annexe B et le JOURNAL) pour qu'un réviseur puisse les relire et les
rejouer (SHOGEN-FM11-VERIFIABLE-1, SHOGEN-REGLE-EMPREINTE-OUTIL-1 ; annexe B.35). Hors des chemins de la garde (2)
(`s2-harness/shogen_s2`, `s2-harness/tools`) et hors de la suite `s2-harness` : ils ne changent ni le bloc machine du
paquet ni ce que lance l'exécution unique.

| fichier | sha256 | rôle | usage |
|---|---|---|---|
| `fm11.py` | `4a0b8abcc0b249034eb2e73397334e85f35d19a957ac4f8a9ddcf3efdda958b5` (DT3-E ; avant : `886cc676…`) | contrôle FM-1.1 non-LLM d'une transcription de sous-agent (annexe C l.13) : repère par leur sha256 (jamais affichées) la cartographie du 2026-09-29 l.51 et ADR-0025 l.14 (`7f8b5cc`), cherche leurs fragments de 40 caractères et les noms de pièces de D.2 dans les résultats et les entrées d'outils ; n'affiche que des comptes | `python3 fm11.py <transcription.jsonl>` ; chemin du dépôt écrit en dur (`REPO = '/home/user/shogen'`, l.4) |
| `regle_fixtures.py` | `5557fb56e5edc3b4c0e3a736b65110d466a7b5118aa4e02bb7ea63d75e92f8ab` | valeurs de `r1.regle_critere` sur les 16 fixtures de `tests/test_critere.py` (U1-U8, J1, J1-ℓ1, J2, J3-ℓ1, J5, J4) ; JSON dont le sha256 attendu est `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` (non-régression de la règle, parties 2 et 3) | `python3 -B regle_fixtures.py <arbre s2-harness> <sortie.json>` |
| `render_fixture.py` | `4084c42b59ea7d7ce356f04a0ea05bb1ff3646de25b46dc571156dd249d2b395` | rendus de la fixture de `test_exclusion` sans et avec l'option PLAGE ; sha256 attendus = épingles `SHA_BASE_SANS_OPTION` (`4e62fbb8…`) et `SHA_BASE_AVEC_OPTION` (`d079dd9d…`) | `python3 -B render_fixture.py <arbre s2-harness> <dossier>` |

Sorties FM-1.1 versées (`sorties-fm11/`) : `redacteur.json`, `redacteur-final.json` (annexe B.32, B.33), `validateur.json`,
`validateur-final.json` (B.33), `g2p3.json` (B.35), `corr-worker.json` (worker G1 du lot CORR, partie 4), `g2-corr.json` (réviseur G2 du lot CORR), `validateur-revision.json` (cp-1 bref du paquet révisé). Elles portent des comptes, des noms d'outils et des numéros
d'événements, aucun extrait de transcription ; les transcriptions elles-mêmes ne sont pas versées (D.2 n° 11 pour celle
de l'orchestrateur ; celles des sous-agents restent dans la session).

Limites : `fm11.py` ne détecte que les fragments exacts de 40 caractères et les motifs nommés (une paraphrase n'est pas
détectée) ; son témoin positif (fragment de la l.51 injecté dans un résultat d'outil, détecté) a été rejoué le
2026-10-02 (annexe B.32) mais n'est pas versé comme test automatique ; `regle_fixtures.py` et `render_fixture.py`
dépendent des tests du harnais qu'ils importent.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-8 ; B-5)* : sorties FM-1.1 des contrôles de la partie 4 versées : `advisor-seuil.json` (B.39), `lecteur-inventaire.json` (B.40), `rattrapage-r-c.json` (B.41), `rattrapage-r-b.json` (B.42 ; 637 événements, égal au compte écrit en B.42), `rattrapage-r-a.json` (B.43), `g2-corr-interrompu.json` (première relecture G2 du lot CORR, interrompue), `g2-partie-4.json` (relecture G2 de la partie 4) ; sha256 dans `SHA256SUMS`.

> *Ajout daté du 2026-10-09 16:23:29 UTC (heure lue par `date -u` ; lot DETTES-T3, DT3-A ; SHOGEN-FM11-VERIFIABLE-1,
> annexe B.35 et B.87)* : témoin automatique versé, `tests/test_fm11.py` (job `controle-unittest`, cas K-04 du runner) :
> `fm11.py` tel que versé, sur transcriptions synthétiques, lignes de D.2 jamais lues (doublures). `SHA256SUMS` couvre
> toutes les sorties ; les 28 sommes ajoutées attestent les octets versés à `0cfbe3e`, non l'égalité avec les sorties
> d'origine. Le témoin ne prouve pas que les vraies lignes de D.2 sont trouvées : chaque exécution réelle le dit, en
> sortant sur « contrôle impossible » sinon.

> *Ajout daté du 2026-10-09 16:23:29 UTC (`date -u` ; lot DETTES-T3, DT3-E)* : `fm11.py` l.19 excluait la dernière
> fenêtre (`range(0, len - 40, 20)`) : les 1 à 20 derniers caractères d'une ligne interdite n'étaient dans aucun
> fragment. Les 40 derniers caractères sont désormais toujours un fragment (une ligne de moins de 40 caractères en est
> un entier) ; tests `test_fragment_en_queue` et `test_queue_aux_longueurs_limites`. Garantie : tout extrait d'au moins
> 60 caractères consécutifs d'une ligne interdite contient un fragment et est détecté ; un extrait de 40 à 59
> caractères ne l'est que s'il contient une fenêtre (pas de 20) ou la queue. Nouveau sha256 `4a0b8abc…` ; l'ancien
> (`886cc676…`) reste celui des contrôles déjà versés, valables pour ce qu'ils ont contrôlé.

> *Ajout daté du 2026-10-09 18:50:07 UTC (`date -u` ; lot DETTES-T4, DT4-c ; SHOGEN-DOCS-SHA256SUMS-GATE-1, annexe B.90,
> L-1 adjugée)* : `tests/test_docs_sha256sums.py` porte les cas de `enforcement/docs-sha256sums.py` (étape du job
> `g1-model-pinning`), qui rejoue chaque fichier nommé exactement `SHA256SUMS` sous `docs/`, hors des emplacements
> interdits. Hors du contrôle par leur nom : `docs/adr-0029/etude-marche/carto/SHA256SUMS.raw` (37 lignes),
> `docs/adr-0029/etude-marche/hylo/SHA256SUMS.copies` (193) et `docs/adr-0029/calib/SHA256SUMS-ECHANTILLONS.txt` (148),
> manifestes de copies dont aucun fichier listé n'a été versé : leur rejeu échouerait sur chaque ligne (mesuré à
> `963eba9`).
