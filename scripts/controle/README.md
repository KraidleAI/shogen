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

> *Ajout daté du 2026-10-09 19:28:17 UTC (`date -u` ; lot DETTES-T4, DT4-d ; relecture G2, C-1 à C-4 et Q-G2-1
> adjugées)* : hors du contrôle par leur nom aussi, `docs/adr-0028/sceau/PAQUET.sha256`, manifeste du sceau (chemin
> depuis la racine), rejoué par `scripts/sceau/verify.sh` (l.13), et
> `docs/adr-0028/sceau/premier-2026-10-02/PAQUET.sha256`, archive du premier sceau d'un paquet depuis rescellé (A-8) :
> son rejeu échoue par construction (mesuré à `6356a94` : sorties 0 et 1). Un `SHA256SUMS` dont le chemin réel est
> interdit n'est pas ouvert ; un dossier illisible fait sortir le contrôle en 3. **Serrage gardé (Q-G2-1)** : une seule
> forme de chemin, relative et sans `./` (un `SHA256SUMS` produit par `find . -exec sha256sum` est refusé « ligne hors
> forme » alors que `sha256sum -c` l'accepte : l'écrire depuis le dossier, `sha256sum <fichiers>`). **Consigne** : un
> `SHA256SUMS` versé ne nomme que des pièces versées ; une pièce restée hors du dépôt se nomme dans le texte, jamais
> dans le `SHA256SUMS`.

> *Ajout daté du 2026-10-09 22:24:59 UTC (`date -u` ; lot DETTES-T5, DT5-7, adjudication Q-2 ; SHOGEN-CI-RUNNERS-1 ;
> relecture G2 du lot, C-7 ; compte et parenthèse retouchés par DT5-14, adjudication C-10 du 2026-10-09 22:37:10
> UTC)* : `tests/test_runners_epingles.py` porte les cas de `enforcement/runners-epingles.py`
> (étape du job `g1-model-pinning`) : aucun libellé de runner en `-latest` (casse ignorée) dans `runs-on`, dans une
> clé `os` ou dans une clé de matrice que nomme `runs-on`, sous les formes que ce lecteur par lignes lit ; 10 tests
> (adjudication C-10 : extension pliée en casse, fichiers cachés lus, autres entrées nommées), plancher du job
> `controle-unittest` 36. Les formes qu'il ne lit pas (alias, échappements, clé explicite) sont
> refusées dans le même job par `enforcement/workflows-yaml.py`, après lecture YAML (relecture G2, C-8).

> *Ajout daté du 2026-10-10 03:35:43 UTC (`date -u` ; correctif DT5-24, alerte CodeQL de la PR n° 11 ; relecture G2,
> C-2)* : VIDE et BLOC de `enforcement/runners-epingles.py` réécrits sans retour arrière exponentiel, mêmes chaînes
> acceptées ; `tests/test_runners_epingles.py` compte 11 tests (un test de temps borné sur des valeurs adverses ;
> `test_formes_hors_ligne` étendu, relecture G2 C-3), plancher du job `controle-unittest` 37 ; le compte de 10 tests et
> le plancher 36 de l'ajout du 2026-10-09 22:24:59 UTC précèdent ce correctif.

> *Ajout daté du 2026-10-10 05:28:37 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-1 ; G0 :
> `docs/adr-0028/G0-lots-DETTES.md`, ajout GF-0)* : `garde_commun.py` (sha256
> `db1528fd43cd50cd0dad532d7fb2e47af99018b6999ee3f6946ed687b8b8cbd0`), bibliothèque des contrôles avant l'acte, sans
> ligne de commande. Horloge lue par `date -u` en sous-processus, jamais par celle de Python ; `horodatages_fautifs`
> relève, hors code et hors guillemets français, une heure du jour plus tard que l'horloge + 120 s (`heure-future`,
> erreur E14 de l'orchestrateur) et une heure écrite `HH:Mx` ou `HH:xx` (`heure-approchee`) ; une date d'un autre jour
> n'est pas jugée. `tests/test_garde_commun.py` (6 tests ; horloge fixée par un faux `date` en tête du PATH), plancher
> du job `controle-unittest` 43.

> *Ajout daté du 2026-10-10 05:37:56 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-4)* : `garde_commun.py` (sha256
> `08595b043757aeb65fe417de44199f9bebcc81d47c0c88c62ce7ad5384a5519d`) : interdits sans nouvelle copie de la liste
> (`INTERDITS` de `enforcement/docs-sha256sums.py`, lus avec `ast` ; noms de D.2 : `motifs` de `fm11.py`, lus sans
> exécuter `fm11.py` ni afficher un motif), vus dans toute copie (composants consécutifs, casse pliée, liens suivis)
> et tout `*.jsonl` ; les motifs de D.2 ne jugent que la partie du chemin sous le dernier composant `scratchpad`, le
> chemin du scratchpad d'une session pouvant en porter un (mesuré le 2026-10-10). `racine_dangereuse` (`/`, le dépôt
> ou un ancêtre, un dossier `docs`, un interdit) ; `analyser_diff` (lignes ajoutées et blocs d'un diff de git, avec ou
> sans contexte) ; `etat_disque` : refus sous 3 Gio libres, avertissement sous 6, `--min-go` ne fait que serrer
> (erreur E4). `tests/test_garde_commun.py` compte 11 tests, plancher du job `controle-unittest` 48.

> *Ajout daté du 2026-10-10 05:45:29 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-2 ; erreurs E9 et E10 de
> l'orchestrateur)* : `presg5.py` (sha256 `60de40770b2889b7dc449b863b42755df757789c7063ba445cbd982c81a87ef0`),
> pré-contrôle S-G5 de l'orchestrateur (approximation de `xtask/src/sg5.rs`, régime complet), versé à l'octet depuis
> son scratchpad, tel qu'il a servi aux versements du 2026-10-10 ; il sort toujours en 0 et n'écarte pas les interdits
> : il devient un outil au diff suivant (GF-2b). `tests/test_presg5.py` (1 test) : sortie dorée, sha256 de sa sortie
> sur une fixture (bornes de 14 et 15 octets, un seul mot anglais, crochets de 31 caractères, guillemets courbes,
> tirets, accents graves, coupe à 160 caractères), mesuré avant le versement ; plancher du job `controle-unittest` 49.

> *Ajout daté du 2026-10-10 05:48:04 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-2b)* : `presg5.py` (sha256
> `6ae10d29e614c8ee6b65b3e2d465ad521fff81326f7724a727a67849d42075c8`) devient un outil, algorithme inchangé (lignes à
> barre oblique inverse reprises à l'octet, sortie dorée identique) : fonction `introuvables(racine, fichiers)` ;
> sorties 0 (aucun fragment), 1 (au moins un), 3 (erreur : sans fichier, `biblio/INDEX.md` absent, fichier illisible)
> ; un chemin interdit (argument ou fichier de `biblio/`) n'est jamais ouvert ni nommé ; fichiers ouverts par `with`
> (propre sous `-X dev -W error`). Usage : `python3 -I -B scripts/controle/presg5.py <racine du dépôt>
> <fichier.md>...`. `tests/test_presg5.py` compte 5 tests (erreur E9 reproduite : message d'outil anglais entre
> guillemets français, sortie 1) ; plancher du job `controle-unittest` 53.

> *Ajout daté du 2026-10-10 05:52:05 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-3 ; erreurs E16 et LA-N08)* :
> `garde_commun.py` (sha256 `a7b1f09d73da5d0635605fbe79c7a590c596b4c69a582598a4c423735d888e31`) : `citations(texte,
> racine)`. Forme stricte, citation entre guillemets français suivie de `(chemin:N)` ou `(chemin:N-M)` : refus si la
> citation ne se lit pas mot pour mot, fragments coupés aux points de suspension et dans l'ordre, entre les lignes N-2
> et M+2 (apostrophes et guillemets courbes pliés, blancs réduits), si la ligne sort du fichier, ou si le fichier est
> interdit (jamais ouvert ni nommé) ; chemin introuvable : avertissement. Forme libre `(nom l.N)` (nom résolu par
> `ALIAS` : JOURNAL, annexe B, ADR-0028) : avertissement compté (`citation-libre`, `citation-libre-absente`), à durcir
> après mesure (avis c.4 adopté). `tests/test_garde_commun.py` compte 14 tests ; plancher du job `controle-unittest`
> 56.
