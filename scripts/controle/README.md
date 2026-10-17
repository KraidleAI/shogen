# Outils de contrôle de l'orchestrateur (versés le 2026-10-02, partie 4 de S2, étape P2)

Outils écrits par l'orchestrateur de la session cloud du 2026-10-02 pour adjuger les lots des parties 2 et 3, versés
**à l'octet** (sha256 égaux à ceux que citent l'annexe B et le JOURNAL) pour qu'un réviseur puisse les relire et les
rejouer (SHOGEN-FM11-VERIFIABLE-1, SHOGEN-REGLE-EMPREINTE-OUTIL-1 ; annexe B.35). Hors des chemins de la garde (2)
(`s2-harness/shogen_s2`, `s2-harness/tools`) et hors de la suite `s2-harness` : ils ne changent ni le bloc machine du
paquet ni ce que lance l'exécution unique.

| fichier | sha256 | rôle | usage |
|---|---|---|---|
| `fm11.py` | `17caaa358ce471c8a9b734873f874794f8c97e66f0125fa05a9dc0cff04452b7` (SHOGEN-FM11-MOTIF-SESSION-1 ; avant : `4a0b8abc…`, DT3-E, puis `886cc676…`) | contrôle FM-1.1 non-LLM d'une transcription de sous-agent (annexe C l.13) : repère par leur sha256 (jamais affichées) la cartographie du 2026-09-29 l.51 et ADR-0025 l.14 (`7f8b5cc`), cherche leurs fragments de 40 caractères et les noms de pièces de D.2 dans les résultats et les entrées d'outils ; n'affiche que des comptes | `python3 fm11.py <transcription.jsonl>` ; chemin du dépôt écrit en dur (`REPO = '/home/user/shogen'`, l.4) |
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

> *Ajout daté du 2026-10-10 05:58:57 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-4b, suite de GF-4)* : `garde_commun.py`
> (sha256 `a7237b2cfc5835b3ff8f6b363f0c924b84825795b7d8c79835e5f641ade3c998`) : `lignes_ajoutees(depot)`, lignes
> ajoutées de l'index par rapport à HEAD (`git diff --cached -U0`), noms d'abord puis diff des seuls chemins admis :
> le contenu d'un fichier interdit n'est jamais lu ; rend aussi le nombre de fichiers écartés. `tests/aide_garde.py` :
> dépôts git temporaires isolés de la configuration de l'hôte (ni configuration globale ni système : ni crochet ni
> signature), jamais le dépôt du projet. `tests/test_garde_commun.py` compte 15 tests ; plancher du job
> `controle-unittest` 57.

> *Ajout daté du 2026-10-10 06:01:41 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-5 ; erreur LA-N05)* : `avant_acte.py`
> (sha256 `2666baf289bc3e7a419f3abeeed2a771890805a5d5ed1eceef8e25e6308e514b`), contrôles avant l'acte : `python3 -I -B
> scripts/controle/avant_acte.py [--depot D] <sous-commande>` ; sorties 0 conforme, 1 refus (une ligne `REFUS <code> :
> <raison> ; à faire : <geste>` par faute), 3 erreur ; journal non versionné `<git-path shogen-garde>/journal.tsv` :
> heure de `date -u`, sous-commande, code, niveau, colonne `contourne` (avis b.5 adopté), une ligne par refus,
> avertissement ou contournement, une ligne conforme sinon. `sceller`, derrière la vérification complète
> (`<vérification> && avant_acte.py sceller`) : sceau sous la clé sha256 de HEAD et de l'arbre de l'index, ou de
> `HEAD^{tree}` avec `--tete` ; refusé (S1) si un chemin est hors de l'index ou non suivi, ou, avec `--tete`, non
> commis. `tests/test_avant_acte.py` (3 tests) ; plancher du job `controle-unittest` 60.

> *Ajout daté du 2026-10-10 06:05:46 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-5b ; erreurs E8, LA-N03, LA-N05)* :
> `avant_acte.py` (sha256 `b6880e94a21f95f12d6ff1eefefc7b5296f1bb039dffa6e7053909fc9a183dbc`) : `commit --message M
> --source S [--source S]...`, à lancer juste avant `git commit -F M` (`avant_acte.py commit … && git commit -q -F
> M`). C1 : sceau de l'index et de la tête présent. C2 (remplace la date de fichier, adjudication) : pour chaque
> source, une ligne `Source-Sha: <sha256>` du message égale à son sha256 au moment du commit, et aucune ligne sans
> source égale : une source retouchée après l'écriture du message est refusée. C3 : verdicts, nombres de passes (en
> lettres ou en chiffres), identifiants `SHOGEN-…`, G-n, C-n, R-n, Q-n, L-n, E-n, O-n, I-n et sha courts du message,
> hors pieds (`Source-Sha`, `Diff-Id`, `Co-Authored-By`, `Claude-Session`, `Décalage admis`), lus dans les sources ;
> un sha court absent des sources doit se résoudre en commit. `tests/test_avant_acte.py` compte 6 tests ; plancher du
> job `controle-unittest` 63.

> *Ajout daté du 2026-10-10 06:17:36 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-6 ; erreurs E14, E16, E21, LA-N04)* :
> `avant_acte.py` (sha256 `f922bcc36fd3a4aa3b18f132888a1b6a346c89c1f1be8f87b8e73e6bf80b48f8`), `commit` complété : C4,
> heures du message et des lignes ajoutées des `.md` (un `.py` porte des heures d'essai, non jugées) ; C5, citations
> des mêmes textes (forme stricte fausse : refus ; autres formes : avertissement) ; C6, `--diff D...` : HEAD plus les
> diffs nommés, dans l'ordre, égale l'arbre de l'index ; C7, aucun bloc ne décale une ligne existante d'un fichier de
> `garde/lignes-citees.txt` (sha256 `a1fc278bff87efe9e94a2bb74cd67114002bfd815bb5b7409b65bd2093db0b16`), sauf une
> ligne `Décalage admis : <chemin>` du message, admise et journalisée en contournement ; C9, `--id ID` : ligne
> `Diff-Id: ID` du message ; un fichier indexé sous un interdit n'est jamais lu (avertissement).
> `tests/test_avant_acte.py` compte 10 tests ; plancher du job `controle-unittest` 67.

> *Ajout daté du 2026-10-10 06:21:50 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-6b ; erreurs E1, E9, E14, E16, E21 ;
> avis b.2 adopté)* : `avant_acte.py` (sha256 `25bf3e8001b9ffdfa3be946103043aeb4543fb35acf8b6716184731d57313ef1`) :
> C8, un workflow touché : `enforcement/workflows-yaml.py` du dépôt lit les workflows de l'index (sortie 1 : refus ;
> absent ou autre sortie : erreur), lancé par `commit` et par `diff`. `diff --fichier F`, à la réception d'un diff de
> worker, avant la G2 : D1, fichier du diff sous un interdit (ni lu ni nommé) ; D2, diff qui ne s'applique pas sur la
> tête (base ancienne) ; puis, sur HEAD plus le diff dans un index temporaire : C4, C5 et `presg5.py` (G5) sur les
> lignes ajoutées des `.md`, C7 sur les fichiers cités, C8. `tests/test_avant_acte.py` compte 13 tests ; plancher du
> job `controle-unittest` 70.

> *Ajout daté du 2026-10-10 06:27:44 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-7 ; erreurs E9 et E10)* :
> `avant_acte.py` (sha256 `d3a7a718485c61e5f2af36179c0d61ce9380af901fe9856d1175b3945acbea77`) : `verser --pieces
> DOSSIER`, à lancer avant `xtask` sur les pièces d'un versement : V0, fichier sous un interdit (ni lu ni nommé) ; V2,
> deux pièces de même sha256, ou une pièce `.md` (500 caractères pliés ou plus) contenue en entier dans une autre ;
> V3, chemin absolu du scratchpad ; V4, chaque `SHA256SUMS` rejoué par `verifier()` de
> `enforcement/docs-sha256sums.py` (forme de la gate : chemin relatif, sans `./`), présent à la racine du dossier,
> chaque pièce listée ; puis C4, C5 et `presg5.py` (G5) sur les pièces `.md`. `tests/test_avant_acte.py` compte 15
> tests ; plancher du job `controle-unittest` 72.

> *Ajout daté du 2026-10-10 06:32:31 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-8 ; erreurs LA-N05, E14, E17 ; ADR-0028
> l.293)* : `avant_acte.py` (sha256 `1f564219f54fa5b6d6dcaee2078c54115f8b823b00a9227efde5c36d656d14fa`) : `pousser
> --distant NOM --branche B`, juste avant `git push` : P1, sceau de la tête (`sceller --tete` après la vérification
> complète) ; P2, aucun chemin `chemin` de `garde/hors-distant.txt` (sha256
> `89928795caa9d5eb7fb73e3bf2fde07117317578824c3fb156d8aefb2ea90f0e`) changé entre `NOM/B` (l'arbre vide pour une
> branche neuve) et HEAD, jamais nommé ; C8 sur les workflows de HEAD si la plage en touche. `pousser --acte TEXTE` :
> P4, acte sur la forge que le mandataire réseau a déjà refusé (lignes `acte`, annexe B, bloc B.95). `publier --texte
> F`, avant toute publication : C4, C5, P5 (motif de secret de `enforcement/gate-secrets.sh`, jamais recopié), V3
> (chemin absolu du scratchpad). `tests/test_avant_acte.py` compte 18 tests ; plancher du job `controle-unittest` 75.

> *Ajout daté du 2026-10-10 06:38:31 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-8b ; erreurs E4 et E15)* :
> `avant_acte.py` (sha256 `fc51b3288b1c42fe6bf7c09a5f69aa5edb83e7b3a6844daed19b5c1cb2300a82`) : `existe NOM`, avant
> d'écrire qu'un fichier manque : chemins du dépôt, suivis ou non, qui portent ce nom, hors interdits (jamais
> affichés) ; X1 si aucun ; un chemin ou un motif : erreur. `disque [--min-go N] [--lister D...]` : DQ, refus sous 3
> Gio libres sur `/` (`--min-go` ne fait que serrer), avertissement sous 6 ; `--lister` imprime les dossiers `target`
> qui portent `CACHEDIR.TAG` (cibles cargo), à profondeur 4 au plus, sans entrer dans `docs`, `.git` ni un interdit,
> sans suivre de lien, avec leur taille ; rien n'est effacé ; racine refusée : `/`, le dépôt ou un ancêtre, un dossier
> `docs`, un interdit. `tests/test_avant_acte.py` compte 20 tests ; plancher du job `controle-unittest` 77.

> *Ajout daté du 2026-10-10 06:44:41 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-9 ; erreurs E3, E8, LA-N04, LA-N05)* :
> `gabarits/chaine.sh` (sha256 `b762b754164dd253da8f4671d04b71c58e85cf98a53196489f4762598b2531f7`), modèle de chaîne
> de commits, à copier par lot et à lancer détaché avec un délai (`setsid nohup timeout 6600 bash chaine.sh`) : plan
> d'une ligne par commit (`id|diffs|message|sources`), contrôle du disque au départ, arbre propre exigé, `git apply
> --index` des diffs du pas, `verif <id> && avant_acte.py sceller` (vérification complète : xtask, `cargo test -p
> xtask` à la cible par défaut, lignes `python3 -B enforcement/` de `gates.yml`, lint R-1), `avant_acte.py commit …
> --diff … --id <id> && git commit -q -F <message>`, reprise par la ligne `Diff-Id:`, arrêt nommé au premier refus ;
> la chaîne n'écrit jamais un message. Un arrêt laisse le pas appliqué à l'index : le retirer avant de relancer.
> `tests/test_gabarit_chaine.py` (5 tests, `verif` remplacée par un faux) ; plancher du job `controle-unittest` 82.

> *Ajout daté du 2026-10-10 06:58:08 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-9b ; erreurs E11 et E25 ; avis b.3
> adopté)* : `avant_acte.py` (sha256 `c6972d99666c6f5fef6d3977be3b6fd62daa5e6499b8608cf5f9dafef2289544`) : `chaine
> --plan P --cc RAPPORT [--duree-pas MIN] [--detache]`, avant de lancer une chaîne : G1, le rapport de contre-contrôle
> porte une seule ligne fixe `GROUPES :` (`aucun`, ou `A+B ; C+D` : diffs verts seulement ensemble) ; G2, aucun pas du
> plan ne commet une partie d'un groupe sans le reste ; G3, durée estimée (pas × durée mesurée d'un pas, 6 min par
> défaut) au-delà de 100 min sans `--detache` : lancement lié refusé, lancement détaché donné (`DETACHE=1 setsid nohup
> timeout …`, attente dans un appel séparé). `gabarits/rapport-cc.md` (sha256
> `9f0f79dee307ae37ecd386460f03582486a16df0552a95ce50ceb3dfa517dea3`), gabarit du rapport de contre-contrôle à la
> ligne fixe ; `gabarits/chaine.sh` (sha256 `11852ada40517b5c775fa61e85cd9c031483c6e354f353cbb2042097b32ff49e`) lance
> `chaine` avant tout pas (variables `CC`, `DUREE_PAS`, `DETACHE`). `tests/test_avant_acte.py` compte 22 tests,
> `tests/test_gabarit_chaine.py` 7 ; plancher du job `controle-unittest` 86.

> *Ajout daté du 2026-10-10 07:04:30 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-10 ; avis c.6 adopté)* : quatre skills,
> un par moment de l'acte, qui donnent les commandes à passer et le moment, sans répéter les règles du bloc commun des
> fiches : `.claude/skills/shogen-avant-lancer/SKILL.md` (disque, `chaine`, lancement détaché),
> `shogen-avant-committer` (`diff` à la réception, `sceller`, `commit`, `verser`, `presg5.py`), `shogen-avant-pousser`
> (`sceller --tete`, `pousser`, `pousser --acte`, `publier`), `shogen-avant-ecrire` (`date -u`, `existe`, `publier`).
> `avant_acte.py` (sha256 `17af293ca899f2ab2f5e2be2ce81a1187905dcfd2e5af24cce4d23f92993ac86`) expose `parseur()`.
> `tests/test_skills.py` (2 tests) : en-tête (name égal au dossier, description de forme commune, aucune clé model),
> sous-commandes et chemins cités existants, options exigées présentes, erreurs visées nommées, aucun marqueur de
> dette nu ; plancher du job `controle-unittest` 88.

> *Ajout daté du 2026-10-10 07:30:53 UTC (`date -u` ; lot GARDE-FOUS-ORCH, GF-10b)* : `avant_acte.py` (sha256
> `fd4cd2e666f24d1041f3595bc28ba1932a3b1a5c68d533b6a83bf6780cb8166d`) : toute exception d'une sous-commande sort en 3,
> avec une ligne `ERREUR <sous-commande> : <type> : <message>` sur la sortie d'erreur ; jamais en 1, qui est un refus
> (une ligne de plan illisible sortait en 1 avec une trace). `tests/test_avant_acte.py` compte 23 tests ; plancher du
> job `controle-unittest` 89.

> *Ajout daté du 2026-10-10 08:47:10 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-1 ; erreurs LA-N05 et E25)* :
> `gabarits/chaine.sh` (sha256 `0db95f4cdef695f40854511dd52942db5dc6c5a5c384ba412dcb740a37a643fa`) : la
> fonction `verif`, appelée par `verif <id> && avant_acte.py sceller`, tourne hors de `set -e` (règle de bash pour
> une commande à gauche de `&&`) : seule sa dernière commande décidait ; un verdict ROUGE de `xtask`, un `cargo test`
> ou une ligne de `gates.yml` en échec laissaient sceller et commettre le pas. Chaque pas sort désormais en 1 à son
> échec ; une ligne de `gates.yml` lit `/dev/null`, jamais la suite des lignes ; délai du lancement détaché écrit
> `<s> = 120 × pas × minutes d'un pas` (le 6600 fixe tuait une chaîne de plus de 110 min, E25).
> `tests/test_gabarit_chaine.py` compte 8 tests (`test_c1_verif_reelle` : cargo et portes factices) ; plancher du
> job `controle-unittest` 90.

> *Ajout daté du 2026-10-10 08:48:26 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-2 ; LA-N05, LA-N01)* :
> `avant_acte.py` (sha256 `d89b567a9e721521508987f1917910c4d5c4e3665c89c32786427bb7f5da430c`) : `pousser` P3,
> la branche poussée (`refs/heads/B`, ce que pousse `git push NOM B`, commande du skill) est HEAD ; sinon refus.
> P1 et P2 jugeaient HEAD seule : une branche B en avance sur une tête scellée, porteuse d'un commit non vérifié
> ou d'un `docs/15-*`, passait. `tests/test_avant_acte.py` compte 24 tests (`test_c2_branche_autre_que_la_tete`) ;
> plancher du job `controle-unittest` 91.

> *Ajout daté du 2026-10-10 08:52:48 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-3 ; erreurs E9, E16, E21)* :
> `avant_acte.py` (sha256 `7f3818d79c1db7d5184bbe74637db57f26d03cb290eb9fd57d843f3fdb2eda95`) et
> `garde_commun.py` (sha256 `03820cef512866f929b3ce2e9f5af54c0b6673ba0018de71bdf56cd052341984`) : `diff` lit
> le diff comme git l'applique : D1 sur les chemins de `git apply --numstat` et des en-têtes, avant toute
> application ; puis HEAD plus le diff, dans un index temporaire, est analysé par `git diff -U0` comme au `commit` :
> un diff sans en-tête `diff --git` (`diff -u`) ou à préfixes de `diff.mnemonicPrefix` n'échappe plus à C4, C5, C7
> ni G5. Citations (C5) et corpus de `presg5.py` (G5) lus dans l'état d'après le diff : une citation anglaise que
> le diff inscrit à `biblio/INDEX.md` n'est plus refusée (DT14-a et DT14-b, commis : 65 faux refus G5 avant cette
> correction), une citation de l'ancien texte d'une ligne changée l'est. `lignes_ajoutees` force les préfixes a/ et
> b/ (au `commit`, un dépôt réglé en `diff.mnemonicPrefix` désarmait C7). `tests/test_avant_acte.py` compte 27
> tests ; plancher du job `controle-unittest` 94.

> *Ajout daté du 2026-10-10 08:54:33 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-4 ; Q-4, erreur E17)* :
> `garde/hors-distant.txt` (sha256 `02db356c2493521d58e1af6caca1b80c9c59717e07cb3c7f4bd3c473cf131cfe`) : la
> suppression de branche se fonde sur l'annexe B, B.92 (`docs/adr-0028/ANNEXE-B-items.md` l.1568, sha256 de la
> ligne écrit au fichier : réponse 403 du mandataire à la suppression de la branche jetable `essai/analyseur-residus`
> par une écriture de l'API), non sur E17 ; les trois lignes de commentaire sont récrites à nombre égal, le reste
> ajouté en fin. Motifs ajoutés : suppression par l'API (forme constatée) et par le protocole git (`-d`,
> `:branche`), méthode après le chemin, `gh repo edit`. `avant_acte.py` (sha256
> `917eb65c700f1dcd080da331e7f459737adba29c6a2f1624589e7db397a391a3`) ramène `-XPUT`, `--method PUT` et
> `--method=PUT` à `-X PUT` avant les motifs. `tests/test_avant_acte.py` compte 28 tests
> (`test_c4_actes_voisins_et_sources` : sha256 des deux lignes sources rejoués) ; plancher du job
> `controle-unittest` 95.

> *Ajout daté du 2026-10-10 08:55:30 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-5 ; erreur E16)* :
> `garde_commun.py` (sha256 `49eb836efe8a217cdbebf4331d50c548a6dbc3d24e115d976380d1dda834a238`) : la forme
> stricte de citation admet la référence écrite en code, (`` `chemin:N` ``) ou (`` `chemin`:N ``), forme courante du
> projet, qui n'était vue ni en refus ni en avertissement ; le nom d'une forme libre perd ses accents graves.
> `tests/test_garde_commun.py` compte 16 tests ; plancher du job `controle-unittest` 96.

> *Ajout daté du 2026-10-10 08:56:46 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-6 ; erreur E15)* :
> `avant_acte.py` (sha256 `933dc1a2ef0babfcf301d9fc17e752584c108f54b22695fed6816a055f36345c`) : `existe NOM`
> cherche le nom en toute casse, comme fichier ou comme dossier (un dossier s'imprime avec sa barre finale) ; un nom
> écrit dans une autre casse ou un nom de dossier sortaient en X1, absence fausse. Le refus X1 nomme ce qui n'est pas
> cherché : fichiers ignorés par git et interdits. `tests/test_avant_acte.py` compte 29 tests ; plancher du job
> `controle-unittest` 97.

> *Ajout daté du 2026-10-10 08:58:13 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-7 ; erreur E11)* :
> `avant_acte.py` (sha256 `59c2149d8740d9960dc4a1c2f64614ff1ca9cc8ba7e2e2e1a03f4d7c62b38638`) : `chaine` G1,
> chaque nom de la ligne `GROUPES :` (hors la valeur `aucun`) nomme un diff du plan ; un nom écrit autrement (casse,
> suffixe `.diff`, diffs du plan en `.patch`, préfixe de série) faisait ignorer le groupe sans refus.
> `gabarits/rapport-cc.md` (sha256 `10537176d1ee3bb75d1c849a12546cbd5b0a71139a8587fcf74ca4893c917cc5`) : la
> ligne fixe est à remplir (`<à remplir : aucun, ou les groupes>`, refusée en G1), au lieu de `aucun` par défaut.
> `tests/test_avant_acte.py` compte 30 tests ; plancher du job `controle-unittest` 98.

> *Ajout daté du 2026-10-10 09:00:09 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-8 ; erreurs E19, E24)* :
> `avant_acte.py` (sha256 `2fccbfb9d0606f29f3344ae7524b1345c62aee10d803aeb6ae4fe8c0a44c8485`) : `verser`
> refuse en erreur un dossier de pièces égal à `/`, au dépôt ou à l'un de ses ancêtres, avant tout parcours (il
> parcourait et lisait tout fichier non interdit) ; un dossier interdit des pièces n'est jamais parcouru (V0 : il
> était listé) ; un fichier non ordinaire (lien brisé, tube, appareil) n'est jamais ouvert (V5 : un tube bloquait
> l'outil). `tests/test_avant_acte.py` compte 31 tests ; plancher du job `controle-unittest` 99.

> *Ajout daté du 2026-10-10 09:01:10 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-9 ; contrat de GF-10b)* :
> `avant_acte.py` (sha256 `d688cd2c0c6788ce860cd00a9fbd30ecebb77cef14fa668cf03e278dded96a55`) : une exception
> du journal, écrit après la sous-commande (dossier `shogen-garde` impossible à créer, dépôt en lecture seule,
> horloge en échec), sort en 3 avec une ligne `ERREUR journal`, jamais en 1 avec une trace : `existe` sortait en 1,
> lu comme absent, sur un fichier trouvé. `tests/test_avant_acte.py` compte 32 tests ; plancher du job
> `controle-unittest` 100.

> *Ajout daté du 2026-10-10 09:01:55 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-10)* : `presg5.py` (sha256
> `8af899db31ce2dd955e836a5f452ca589de2c8d673db4c85535214469ac2951e`) : la racine passe au contrôle des
> interdits comme les fichiers (sortie 3, rien d'ouvert ni de nommé) ; une racine sous un interdit faisait lire son
> `biblio/INDEX.md`, ou nommer ce chemin dans l'erreur. `tests/test_presg5.py` compte 6 tests ; plancher du job
> `controle-unittest` 101.

> *Ajout daté du 2026-10-10 09:04:10 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-11 ; erreur E14)* :
> `garde_commun.py` (sha256 `e6772475d222ae986b0f655011f3890df637e100a544f86d5053e61b94c7e94c`) : toute
> heure écrite dans les 25 caractères qui suivent une date du jour est jugée, la seconde heure d'une plage comprise
> (`de 04:10 à 04:22`, `04:10-04:22` : seule la première l'était) ; l'extrait va de la date à l'heure ; une heure
> approchée écrite en X majuscule (`19:5X`, `21:XX`) est vue. `tests/test_garde_commun.py` compte 17 tests ;
> plancher du job `controle-unittest` 102.

> *Ajout daté du 2026-10-10 09:06:28 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-12 ; Q-10, erreur E21)* :
> `garde/lignes-citees.txt` (sha256 `6c4a36213dc765907a9cb3007770ecb935b572ebac31cde112aaa8ec8c2f1398`) :
> ajout en fin des documents que `docs/17-modele-de-menace.md` cite par numéro de ligne (`docs/AUDIT-ENTREE.md`,
> docs 03, 04, 09 et 13, `docs/G1-lot-B0-pool-analyse.md`, `CLAUDE.md`) ; `biblio/INDEX.md` et les workflows, cités
> aussi, restent hors de la liste (limite de la relecture G2). `tests/test_avant_acte.py` compte 33 tests
> (`test_c12_documents_cites_par_docs17`) ; plancher du job `controle-unittest` 103.

> *Ajout daté du 2026-10-10 09:14:52 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-15 ; erreur E5, règle I-1)* :
> `gabarits/chaine.sh` (sha256 `42bcb5b5d687dc14e7529187760dcc17b148fd47233275f45e938e9937c5979f`) : `verif`
> lance cargo sans `CARGO_TARGET_DIR` ni `CARGO_BUILD_TARGET_DIR`, à la cible par défaut de la copie, comme la
> forge ; une variable héritée de l'environnement de l'orchestrateur déplaçait la cible (forme de E5).
> `tests/test_gabarit_chaine.py` : `test_c1_verif_reelle` pose `CARGO_TARGET_DIR`, le cargo factice échoue s'il la
> voit ; 8 tests, plancher du job `controle-unittest` inchangé, 103.

> *Ajout daté du 2026-10-10 09:20:04 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-16 ; E8, faux refus)* :
> `avant_acte.py` (sha256 `b0d5b0658ffc14170d7d3370d4668d694956cbe5ab5e87c0acb1a1c618d2fef6`) : C3 lit aussi
> dans les sources la forme `passe N` (N passes faites), hors négation (`sans`, `aucune`, `pas de`) : l'adjudication
> de DETTES-T6 n'écrit que `passe 2` et `sans passe 3`, et le message réel de DT6-d (`en deux passes`) était refusé
> à tort ; le message réel de DT5-22 (`en trois passes`, erreur E8) reste refusé. `tests/test_avant_acte.py` compte
> 34 tests ; plancher du job `controle-unittest` 104.

> *Ajout daté du 2026-10-10 09:30:21 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-17 ; erreurs LA-N04, E11)* :
> `avant_acte.py` (sha256 `531673a8033bfd991a282be6d744467c9b64f88803579b4583810f35c34067e9`) : `chaine`
> G4, un `Diff-Id` du plan déjà porté par un commit dont le message diffère de celui du plan (après `git
> stripspace`) est refusé : la reprise du modèle, qui lit tout l'historique, sautait ce pas sans rien dire (un nom
> courant comme `C-1` d'un autre lot suffisait) ; même message, reprise après un arrêt : admis.
> `tests/test_avant_acte.py` compte 35 tests ; plancher du job `controle-unittest` 105.

> *Ajout daté du 2026-10-15 10:31:37 UTC (`date -u` ; lot GARDE-FOUS-ORCH, relecture G2, C-18 ; contrat GF-10b, L-16)* :
> `avant_acte.py` (sha256 `2d274a8f23431d32e88c57a23f70df743cda033cb64613dadbb0ad14c0952d37`) et
> `presg5.py` (sha256 `fb352419e5c5c70c8d89dd17ce32d4c410d08d212935a98901838349739cba4d`) : un module frère illisible
> (installation abîmée), des interdits illisibles (`presg5` copié sans `enforcement/`), une exception hors des
> sous-commandes ou l'échec du vidage final de la sortie standard (tube sans lecteur) sortent en 3 ; ils sortaient en
> 1, qui se lit refus (ou fragment introuvable pour `presg5`), ou en 120 (vidage à la fin de l'interpréteur). Reste :
> une erreur de syntaxe de l'outil lui-même sort en 1 (l'interpréteur, avant toute ligne de l'outil).
> `tests/test_avant_acte.py` compte 36 tests, `tests/test_presg5.py` 7 ; plancher du job `controle-unittest` 107.

> *Ajout daté du 2026-10-15 11:34:46 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-2 ; LA-N01, ADR-0028
> l.293)* : `avant_acte.py` (sha256 `7aa53095f5cb9879bda43046228759cff61fd5857219c591378cb1d877a988af`) : `pousser` P2
> juge aussi chaque commit de la plage poussée (`git rev-list HEAD --not --remotes=NOM` sur les chemins de
> `garde/hors-distant.txt`) : un `docs/15-*` ajouté puis retiré avant la tête passait, l'arbre de la tête n'en portant
> plus, alors que la poussée en porte le contenu (ADR-0028 l.293 : préfixes sans ces fichiers).
> `tests/test_avant_acte.py` compte 37 tests ; plancher du job `controle-unittest` 108.

> *Ajout daté du 2026-10-15 11:35:07 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-3 ; E17, B.92, B.95)* :
> `avant_acte.py` (sha256 `eb3327f5a7ca9c88a7283817c4e954927e26556c34f161f19c930e2328b6b6c6`) et
> `garde/hors-distant.txt` (sha256 `bc4bbc78dd41850607194159660a8fb115ce49eee0f0ca8da437795bdef4f547`) : `pousser
> --acte` ramène aussi, avant les motifs, les guillemets du shell, les blancs répétés et les options de git placées
> avant la sous-commande (`-C`, `-c`, `--git-dir`, `--work-tree`, `--no-optional-locks`) ; motifs ajoutés : refspec
> `+:branche`, DELETE et POST sur la protection de branche (refus conservateur). Dix formes voisines des actes de B.92
> et B.95 passaient (`git -C … push origin -d b`, `':b'`, méthode entre guillemets, DELETE de la protection).
> `tests/test_avant_acte.py` compte 38 tests ; plancher du job `controle-unittest` 109.

> *Ajout daté du 2026-10-15 11:35:35 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-4 ; E21)* :
> `avant_acte.py` (sha256 `22da65fb8e0b28732765ad8fea81b56add6ae7cedd0b43c56218ef0c21b264f9`) : C7 refuse aussi le
> retrait ou le renommage d'un fichier de `garde/lignes-citees.txt` (ses renvois par numéro ne mènent plus nulle
> part), au `commit` et au `diff` ; voulu : ligne `Décalage admis : <chemin>` du message, journalisée en
> contournement. Un fichier cité retiré ou renommé passait sans refus. `tests/test_avant_acte.py` compte 39 tests ;
> plancher du job `controle-unittest` 110.

> *Ajout daté du 2026-10-15 11:35:58 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-5 ; LA-N04, E11)* :
> `avant_acte.py` (sha256 `47602814a5e604ed88e152e984bfdfb92e3b4095168230bb9b6be7575e1398ab`) : `chaine` G4 refuse
> aussi un plan dont deux pas portent le même `Diff-Id` : le modèle commettait le premier et sautait le second (déjà
> commis) sans rien dire, chaîne sortie 0. `tests/test_avant_acte.py` compte 40 tests ; plancher du job
> `controle-unittest` 111.

> *Ajout daté du 2026-10-15 11:36:06 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-6 ; LA-N05)* :
> `gabarits/chaine.sh` (sha256 `fe3f3d8bd396d1f9cde33abedb84bc20c73afb456b9e1b4932cbbbb94e13a80a`) : `verif` lance
> aussi une étape de `gates.yml` écrite `- run: python3 -B enforcement/…` (forme courante des workflows), que son
> motif sautait : une telle étape rouge laissait sceller et commettre le pas. `tests/test_gabarit_chaine.py` compte 8
> tests (`test_c1_verif_reelle` : étape en tiret) ; plancher du job `controle-unittest` inchangé, 111.

> *Ajout daté du 2026-10-15 11:38:16 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-7 ; E19, C-8)* :
> `avant_acte.py` (sha256 `a78d3e674738d3b1ed8826136052c9e4247cf392e90f9a72042a5a2aba112dda`) : `verser` compte les
> fichiers et les octets du dossier de pièces avant toute lecture et sort en erreur au-delà de 5000 fichiers ou 512
> Mio (racine fausse, voisine de `/` : `/root`, `/usr`, le scratchpad entier) ; ces racines étaient parcourues et lues
> en entier, leurs `.md` jugés, des extraits imprimés aux refus. `tests/test_avant_acte.py` compte 41 tests ; plancher
> du job `controle-unittest` 112.

> *Ajout daté du 2026-10-15 11:38:22 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-8 ; articulation avec le
> crochet GARDE-FAITS)* : `.claude/skills/shogen-avant-committer/SKILL.md` (sha256
> `9f049982f6a4f07919d10ea99fb35c83aa85e95019dc1478f89aaed34d51e3d9`) et
> `.claude/skills/shogen-avant-pousser/SKILL.md` (sha256
> `e808a465fc824873eb85ba025196253936658f4b61230b73cfc42a4dd2263b9a`) : chaque commande qui commet, pousse ou contrôle
> une poussée est précédée, dans son point, de la lecture que le crochet GARDE-FAITS du dépôt
> (`.claude/hooks/garde_faits.py`, R3) exige (`git diff --cached --stat`, `git log --oneline origin/<b>..HEAD`, `git
> status --short`) ; telles qu'écrites, les commandes des points 4 (commit), 2 (poussée) et 3 (`pousser --acte` d'une
> suppression) étaient refusées par le crochet. `tests/test_skills.py` compte 3 tests (`test_r8_crochet_garde_faits` :
> crochet lancé sur un journal synthétique) ; plancher du job `controle-unittest` 113.

> *Ajout daté du 2026-10-15 11:38:22 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-9 ; E14)* :
> `garde_commun.py` (sha256 `b386dbd80acc775b0d6cafb42a311f03e80f78c0bf72fc039e375ae82063ae89`) : la date d'une ligne
> se lit aussi en code ou dans une citation, l'heure seule restant masquée en code : une heure future écrite après une
> date du jour en code (forme `` `AAAA-MM-JJ` HH:MM ``) n'était pas vue ; l'extrait se lit sur la ligne écrite.
> `tests/test_garde_commun.py` compte 18 tests ; plancher du job `controle-unittest` 114.

> *Ajout daté du 2026-10-15 11:48:38 UTC (`date -u` ; lot GARDE-FOUS-ORCH, contre-contrôle, R-10 ; E8)* :
> `avant_acte.py` (sha256 `2992ac33117f4ebb55c96b64717efe9de5d9294f40560eb35dfd4bf7e8283fde`) : C3 lit aussi, au
> message et aux sources, le verdict `CONFORME-AVEC-RÉSERVES` du gabarit de contre-contrôle, accentué ou non (les
> messages de commit du projet sont écrits sans accents) : un message qui l'écrivait contre des sources NON-CONFORME
> passait, le verdict n'étant pas lu. `tests/test_avant_acte.py` compte 42 tests ; plancher du job `controle-unittest`
> 115.

> *Ajout daté du 2026-10-15 21:17:22 UTC (`date -u` ; lot DETTES-T7, DT7-f ; SHOGEN-S2BIS-MUT-COMMANDE-1,
> SHOGEN-MUTANTS-ORPHELINS-1)* : `mutants.py`, outil commun des campagnes de mutants (bibliothèque standard, POSIX) :
> chaque mutant (fichier, texte avant présent une fois, texte après) est posé dans une copie, puis classé par la
> commande du job qui porte le code muté, lue dans le `gates.yml` de la copie par l'analyseur unique du vérificateur
> (étapes `run:` dans l'ordre, runner d'abord, `bash -eo pipefail` comme la forge), sous une borne de temps (300 s par
> défaut) : tué (sortie 1, ou les codes de `--tue`), vivant (0), FATAL (borne, sortie hors contrat, mutant
> inapplicable ; jamais compté tué). Chaque étape tourne dans un groupe de processus neuf, arrêté en entier après elle
> (`os.killpg`) ; la campagne finit par un relevé `ps` de ses groupes, vide exigé. Témoin d'abord (job sans mutant
> vivant), copie rendue à ses octets après chaque mutant, diff et sortie de chaque mutant versés dans `--sortie`.
> L'outil se lance depuis un arbre relu, à part de la copie qu'il mute. Cas : `tests/test_mutants.py` (deux tests ;
> plancher du job `controle-unittest` 117).
>
> *Ajout daté du 2026-10-15 22:04:01 UTC (`date -u` ; relecture G2 du lot DETTES-T7, correction C-1 ;
> SHOGEN-MUTANTS-ORPHELINS-1, SHOGEN-S2BIS-MUT-COMMANDE-1)* : à la borne, `mutants.py` arrête aussi le groupe de
> chaque descendant de l'étape, relevé par parenté (`ps -A -o pid=,ppid=,pgid=`, avant l'arrêt de l'enfant direct),
> et le compte au relevé de fin : la suite que `enforcement/verdict-suite-s2.py` lance dans sa propre session depuis
> DT7-d n'est pas du groupe de l'étape (mesure M-F1 de la relecture : elle survivait à la borne, relevé vide). Après
> cet arrêt, la sortie n'est plus attendue que `RELIQUAT` s (5 s) : un descendant détaché de son parent (double
> fork, `setsid`) n'est pas suivi et peut rester vivant. La première étape du job doit être le checkout ; les étapes
> sont relues sur la copie mutée : un mutant de `gates.yml` se classe par la ligne qu'il écrit (avant C-1, par la
> ligne d'origine : vivant à tort, mesure M-F2), et des étapes illisibles sous un mutant le classent FATAL. Cas :
> M6, M7, M8 et le refus `tete` de `tests/test_mutants.py` (toujours deux tests ; plancher 117 inchangé).
>
> *Ajout daté du 2026-10-15 23:13:50 UTC (`date -u` ; contre-contrôle du lot DETTES-T7, réserve R-1 ;
> SHOGEN-S2BIS-MUT-COMMANDE-1)* : la première étape du job est le checkout épinglé du gabarit K (`ETAPES[1]` du
> vérificateur, `with:` réduit à `persist-credentials: false`, puis `fetch-depth: 0` admis), lu sur les lignes
> brutes du job ; avant R-1, toute première étape non admise passait pour le checkout (étape `if:` qui échouerait
> sur la forge, autre action, `with:` autre : mesure du contre-contrôle). Cas : refus `tete-if`, `tete-action`,
> `tete-with` et `fetch-depth: 0` admis, dans `tests/test_mutants.py` (toujours deux tests ; plancher 117 inchangé).
>
> *Ajout daté du 2026-10-15 23:21:37 UTC (`date -u` ; contre-contrôle du lot DETTES-T7, réserve R-2 ;
> SHOGEN-MUTANTS-ORPHELINS-1)* : sous Linux, l'outil se déclare moissonneur de ses descendants
> (`prctl(PR_SET_CHILD_SUBREAPER)`) ; après chaque étape, à la borne comme à la sortie normale, tout descendant
> vivant, orphelin compris (double fork, `setsid`, parent sorti), est arrêté jusqu'au dernier (`balayer`), et le
> relevé de fin le dit ; avant R-2, un tel descendant survivait à la campagne sous un relevé vide, et un enfant né
> entre le relevé `ps` et l'arrêt pouvait échapper (mesures du contre-contrôle). Hors de Linux (POSIX sans
> moissonneur), la limite de C-1 demeure : un descendant détaché n'est pas suivi. Cas : M9 et M10 de
> `tests/test_mutants.py` (toujours deux tests ; plancher 117 inchangé).
>
> *Ajout daté du 2026-10-15 23:45:31 UTC (`date -u` ; contre-contrôle du lot DETTES-T7, réserve R-5 ;
> SHOGEN-S2BIS-MUT-COMMANDE-1)* : le classement FATAL d'un mutant de `gates.yml` qui rend les étapes
> illisibles (C-1) a son cas : M11 (`if:` posé sur une étape : FATAL, aucune étape jouée) ; avant R-5, ce
> classement pouvait devenir `tué` sans qu'aucun cas ne rougisse (mutant CC7 du contre-contrôle, vivant).

> *Ajout daté du 2026-10-16 00:56:42 UTC (`date -u` ; lot DETTES-T15 ; SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1,
> relecture G2 du correctif DT5-24, O-5 ; texte de DT15-f du 2026-10-10 08:45:35 UTC, plancher recalé sur la
> tête `413321b`)* :
> FLOTTANT de `enforcement/runners-epingles.py` ne prend une occurrence qu'au début d'une suite de caractères de
> libellé (regard arrière) : temps linéaire, mêmes occurrences que l'ancienne forme (preuve du lot : partition
> d'Unicode par le moteur, contrôles exhaustifs et aléatoire à trois voix, aucun écart, sous Python 3.10 à 3.13) ;
> `tests/test_runners_epingles.py` compte 12 tests (un test de temps borné sur des libellés de 200 000 caractères),
> plancher du job `controle-unittest` 118 ; le compte de 11 tests de l'ajout du 2026-10-10 03:35:43 UTC et les
> planchers des ajouts suivants, jusqu'à 117 (ajout du 2026-10-15 23:45:31 UTC), précèdent ce lot.

> *Ajout daté du 2026-10-16 03:55:54 UTC (`date -u` ; lot DETTES-T15, DT15-m ; SHOGEN-PRESG5-QUADRATIQUE-1, port de
> DT15-i)* : `presg5.py` lit les balises et les crochets par indices, le fermant cherché dans la seule fenêtre (300
> et 30 caractères) : temps linéaire, mêmes sorties (sortie dorée de `tests/test_presg5.py` inchangée ; sur le corpus
> du dépôt, mêmes textes et mêmes lignes avant et après, le corpus lu en 5 s au lieu de 991 s).
> `tests/test_presg5_lineaire.py` compte 3 tests (deux tests de temps bornés à 20 s sur 8 000 000 de caractères,
> rouges sur l'ancienne lecture ; des valeurs de référence) ; plancher du job `controle-unittest` 121.

> *Ajout daté du 2026-10-16 06:58:15 UTC (`date -u` ; lot PRODUIT-R2, R2-c ; ADR-0028 §4 pt 7 et D9, AVIS-PRODUIT-APRES-S2 §3)* :
> `../publication/gabarit_controle.py` (sha256 `81512aeaac3f72131fe4ae57a47f05885deb5115da1f0f16c180eefbd1688abd`) contrôle un rapport écrit depuis un
> gabarit de `docs/publication/gabarits/` : locutions de doc 09 (25 entrées, chacune ancrée à sa ligne de doc 09 ;
> ancre absente : erreur 3), texte fixe à l'octet, champs tous remplis ou tous vides, nombre sans empreinte, R1 dans un
> champ libre. `tests/test_gabarit_controle.py` compte 5 tests (une phrase par entrée de doc 09 ; les 26 renvois
> chemin:ligne des deux gabarits relus contre le harnais ; doc 04 l.129-139 recopiées) ; plancher du job
> `controle-unittest` 126. Un lot qui décale une ligne citée de `s2-harness/shogen_s2/report.py`, `r2.py` ou
> `sources.py` fait échouer ce test : il met à jour les renvois des deux gabarits. Limites : docstring de l'outil.


> *Ajout daté du 2026-10-16 09:03:03 UTC (`date -u` ; lot INTEGRATION-P2 : GARDE-FOUS-ORCH, phase 2, groupe C, pas INT-01 à INT-07 ;
> annexe B, B.102 : SHOGEN-FM11-MOTIF-SESSION-1, SHOGEN-GARDE-DATE-PASSEE-1, SHOGEN-GARDE-ATTRIBUTION-DIFF-1,
> SHOGEN-GARDE-VERIF-VERSIONNEE-1, SHOGEN-GARDE-DISQUE-CHAINE-1, SHOGEN-GARDE-LIGNE-REMPLACEE-1,
> SHOGEN-GARDE-LECTURE-SEULE-1 ; relecture G2 du groupe, C-1 à C-4)* : un ajout pour le groupe ; empreintes au pas
> INT-07 : `fm11.py` `17caaa358ce471c8a9b734873f874794f8c97e66f0125fa05a9dc0cff04452b7`,
> `garde_commun.py` `8904ec0a1918ca4f29c54550a5bad7d9aa079a4867a08b1414b026d132b93f2a`,
> `avant_acte.py` `25a3a8ddee0d4d35b21f98e21f9a99d6bb5a52ed89097d2cd88767390479f8ea`,
> `gabarits/chaine.sh` `0d07d39c2d0b809d0d8168931cfe0a40dc4f71277856338227d88f7b546fe511`,
> `garde/lignes-citees.txt` `8b6cf5ab967ad7f77e9851a969428c898c8e0097d59b8247a646f56cdab6b8ae`.
> - FM-1.1 (Q-3) : le motif de la session de `fm11.py` (l.23 changée en place, l.4 intacte) ne compte plus
>   l'identifiant de session écrit comme composant du chemin du scratchpad (`…/<projet>/<session>/scratchpad`), que
>   porte toute transcription de la session ; nommée ailleurs (transcription, dossier de la session, dossier voisin du
>   scratchpad), la session reste comptée. `SHA256SUMS` et la ligne de `fm11.py` de la table de tête mis à jour en
>   place. Limites : un chemin qui ressort du scratchpad (`<session>/scratchpad/../…`) n'est pas compté ; une ligne
>   `Claude-Session:` l'est.
> - DATE-PASSEE (L-1, E14) : `garde_commun.py`, `horodatages_fautifs` refuse aussi une heure écrite sans sa date
>   (heure-sans-date : aucune date dans les 25 caractères qui la précèdent ; code et guillemets français masqués) ;
>   `dates_passees` (avec `entree_datee`) refuse une entrée datée ajoutée (ligne qui commence par la date et l'heure, ou
>   par un mot en capitale suivi de `daté du`) antérieure à la dernière entrée datée du fichier à HEAD ou à une entrée
>   ajoutée avant elle ; une date seule du même jour n'est pas jugée. `avant_acte.py`, C4 (`passees`) : aux .md du
>   commit et du diff d'un worker. Les ajouts datés de ce README se posent donc en fin, datés du moment.
> - ATTRIBUTION-DIFF (L-3, E8) : C3 attribue chaque mot qu'il lit au message (verdict, nombre de passes, identifiant,
>   sha court) au diff que le message décrit (ligne `Diff-Id:`, ou `--id`) : sources coupées en passages (`unites`),
>   diffs nommés par passage (`nommes`, plages `C-1 à C-18` et `GF-0 … GF-10b` lues), refus d'un mot que seuls des
>   passages nommant d'autres diffs du même préfixe portent, sauf s'il est dans les lignes ajoutées du diff
>   (`attribuer`). Limite : une plage à bornes en lettres (`DT15-a à DT15-m`) n'est pas lue (faux refus).
> - VERIF-VERSIONNEE (L-4, LA-N05) : `sceller --verif F` (texte de `declare -f verif` ; `-` : entrée standard) écrit
>   au sceau la ligne `verif <sha256>` ; `commit` refuse (C1) un sceau dont cette ligne n'est pas l'empreinte de la
>   fonction `verif` de `gabarits/chaine.sh` des outils (`empreinte_verif`, de `verif() {` à `# --- fin de verif`,
>   passée par `declare -f` de bash) ; le modèle scelle par `declare -f verif | acte sceller --verif -` (l.24 et l.50
>   changées en place). Une chaîne copiée du modèle depuis L-4 dont la vérification diffère de celle du modèle scelle,
>   mais ne commet plus. Un sceau sans ligne `verif` n'est pas jugé : vérification hors du modèle
>   (`<vérification> && sceller` des skills), chaîne copiée d'un modèle antérieur à L-4, chaîne qui n'appelle pas
>   `avant_acte.py`. Une chaîne propre à un lot prend la fonction du modèle :
>   `source <(sed -n '/^verif() {/,/^# --- fin de verif/p' "$OUTILS/gabarits/chaine.sh")`. Une vérification propre à
>   un lot se verse au modèle par un diff relu, commis au premier pas d'une chaîne copiée du modèle d'après ce diff
>   (`OUTILS` dans le dépôt : la fonction comparée est celle de l'arbre après `git apply` ; une chaîne copiée du modèle
>   d'avant est refusée en C1).
> - DISQUE-CHAINE (LN-1 ; E4, E28) : le modèle de chaîne contrôle le disque à chaque pas, avant `git apply`
>   (`acte disque --min-go "${DISQUE_MIN_GO:-0}"`, seuils lus dans `garde_commun.py`) ; un refus imprime
>   `ROUGE disque avant <id> (LN-1) : arrêt, rien appliqué` et arrête la chaîne, l'arbre propre. Limite : le disque
>   mesuré est `/`, non le système de fichiers du dépôt.
> - LIGNE-REMPLACEE (L-13, E21) : C7 (`cites`) lit aussi les empreintes des renvois par numéro (`empreintes`) : rangées
>   du registre `docs/RENVOIS-LIGNES.tsv` de l'état d'après (colonnes `cible`, `lignes`, `empreinte` ; `lignes` à `-`
>   sautées ; en-tête ou rangée illisible : erreur 3) et lignes `<chemin>:<a>[-<b>] <empreinte>` de
>   `garde/lignes-citees.txt` (ajout en fin : ADR-0028 l.293 et `fm11.py` l.4) ; sha256 des lignes jointes par LF,
>   sans LF final, comparé sur la longueur écrite. Un renvoi qui répondait à HEAD et n'y répond plus après le diff est
>   refusé, à nombre de lignes égal compris (`remplacees`), sauf empreinte mise à jour dans le même diff ; sans réponse
>   ni avant ni après : avertissement. Registre lu par l'outil à la tête `ccc29190` : 110 renvois répondent, 0 non,
>   23 hors de l'arbre (`lignes` à `-`) ; à la tête `9c04eec` : 111 répondent, 0 non, 23 hors de l'arbre.
> - LECTURE-SEULE (L-12, Q-5) : `--lecture-seule`, avant la sous-commande, pour `diff` et `commit` seulement (autre
>   sous-commande : erreur 3) : git tourne dans un dépôt jetable de `TMPDIR` (`jetable` : `git clone --shared
>   --no-checkout`, HEAD du dépôt lu, son index copié pour `commit`) ; fichiers cités, lecteur YAML (`workflows`,
>   paramètre `racine`), sceaux et interdits (`lignes_ajoutees`, paramètre `racine`) se lisent dans le dépôt lu, où
>   rien n'est écrit ; le journal de ces passages va au dépôt jetable et se perd avec lui.
>
> Tests : `tests/test_fm11.py` 10 tests, `tests/test_garde_commun.py`
> 20 tests, `tests/test_avant_acte.py` 49 tests,
> `tests/test_gabarit_chaine.py` 10 tests ; le groupe ajoute 12 tests ; plancher du job
> `controle-unittest` 138.


> *Ajout daté du 2026-10-16 10:27:25 UTC (`date -u` ; lot INTEGRATION-P2 : GARDE-FOUS-ORCH, phase 2, groupe B, pas INT-08 à INT-16 ;
> annexe B, B.102 : SHOGEN-GARDE-CROCHET-ACTE-1, SHOGEN-GARDE-OUTIL-E18-E20-1, SHOGEN-GARDE-OUTIL-E26-E27-E28-1 ;
> relecture G2 du groupe, C-1 à C-8)* : un ajout pour le groupe ; empreintes au pas INT-16 :
> `.claude/hooks/acte_shell.py` `a74689b1d67eec7630a7c046e86a940c9697ebbf94645b2b72b25acf062b736d`,
> `.claude/hooks/garde_faits.py` `bb90a337977e2f6c4833157cb0ffa902d6f3951c072d9fe112f72d440aaaedfc`,
> `.claude/settings.json` `952f4a781c8837c13de413dc3b1e7a1cedbfd367b263708a0f2db486f8167bcc`,
> `.claude/skills/shogen-avant-committer/SKILL.md` `600531d3b74737e02783378196428c01d82fd2b49151d725760787ab6668b205`,
> `avant_acte.py` `23fcaa3460439442a0b68df194315ca9d35c4dd2023bf777c3d010d4bc8f889a`,
> `garde/forge-actions.txt` `0ce631b4c66783152afff919699f7d6f006aae7536a447fc014a37261a850ff9`,
> `garde/dossiers.txt` `cd22558b07b70752428801ade3fa5f5f2c4f1f418df6087844008b07bb017fa8`.
> - Acte lu (LN-6) : `.claude/hooks/acte_shell.py`, voisin du crochet GARDE-FAITS, bibliothèque standard seule, lit
>   l'acte d'une commande shell par shlex (commandes simples, programme après les enveloppes, redirections, corps de
>   heredoc, arrière-plan, boucles ; bash -c, eval et substitutions lus récursivement ; None si shlex ne lit pas la
>   commande). Le crochet juge R1, R2, R3 et le texte de R5 sur ces actes : la sonde du contre-contrôle (journal
>   synthétique écrit par un heredoc python qui porte un commit) passe ; un commit dans bash -c, une substitution,
>   derrière une affectation ou des options globales reste refusé ; R5 lit le message de git commit, fichier de -F
>   compris. Commande illisible, ou module absent : motifs d'avant. Un acte dont le programme ou l'argument d'eval
>   porte `$` ou un accent grave, ou un code python qui lance un processus, est jugé aussi par les motifs d'avant
>   (C-2 : régressions de LN-6 refermées).
> - R7 (E18, E28) : refus d'un sleep d'avant-plan (hors arrière-plan : &, run_in_background) et d'un pkill -f ou
>   pgrep -f dont le motif ne commence pas par ^. Une boucle while ou until à condition de sortie admet son sleep ;
>   une boucle à condition constante (while true, until false), seulement si la commande porte break, exit ou return
>   (C-3) ; for reste refusé.
> - R8 (E20) : mcp__github__create_pull_request refusé sans preuve que la forge lance des jobs sur ce owner/repo
>   (résultat de mcp__github__actions_*, gh run ou gh api du même dépôt : run conclu success ou job à runner_id non
>   nul) ; ou ligne `owner/repo AAAA-MM-JJ <id du run lu>` du jour au marqueur `garde/forge-actions.txt`, qui ne vaut
>   que si l'identifiant figure dans une telle preuve d'un journal de la session (C-4).
> - R9 (E27) : seuil de coût avant Agent et Workflow : workflow de plus de 3 agents (nombre illisible ou multiplié par
>   une boucle : refus), lancement qui porterait au-delà de 4 les sous-agents vivants (journal touché depuis moins de
>   300 s) ; sauf jeton FANOUT-AUTORISE, ou les mots fan out dans une phrase sans négation (C-7), au dernier message
>   de l'humain.
> - R10 (E26) : à la soumission d'un message (UserPromptSubmit, `.claude/settings.json`), ses noms propres sont
>   relevés au JOURNAL et dans docs/publication/, affichés en contexte et gardés pour le tour ; au Stop, une réponse
>   qui nomme un dossier de `garde/dossiers.txt` (C-5 : liste versée, un nom par ligne ; absent ou vide : aucun refus)
>   absent du message et de tout fait du tour est refusée une fois.
> - E28, `verser` : V6 (`biblio`), chaque fichier de biblio/ (hors INDEX.md et `*.sidecar`, répertoire plat) nommé en
>   accents graves dans biblio/INDEX.md et compte d'en-tête égal au compte réel, sauf corpus partiel tout nommé
>   (forme de S-G6) ; V7 (`chaine_active`, `MOTIF_CHAINE`), refus pendant qu'une chaîne de commits tourne (pgrep -f
>   ancré ; pgrep en erreur : 3). Skill `shogen-avant-committer`, point 5.
> - Cas hors CI (C-6, L-7) : `.claude/hooks/tests/test_garde_faits.py` écrit `NOTES.md` par son nom relatif ; un
>   segment hexadécimal du TMPDIR n'y est plus pris pour un identifiant (R5).
>
> Tests : `tests/test_garde_acte.py` 21 tests (cas des mutants vivants de la G2 compris,
> C-8), `tests/test_avant_acte.py` 51 tests ; le groupe ajoute 23 tests ; plancher du job
> `controle-unittest` 161.


> *Ajout daté du 2026-10-16 11:35:43 UTC (`date -u` ; lot INTEGRATION-P2 : GARDE-FOUS-ORCH, phase 2, groupe A, pas INT-17 à INT-24 ;
> annexe B, B.102 : SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1, SHOGEN-GARDE-OUTIL-E22-E23-E24-1 ; relecture G2 du groupe,
> C-1 à C-8)* : un ajout pour le groupe. La règle du brief, nommée R7 aux pièces du groupe A, est R11 : R7 à R10 sont
> les règles du groupe B.
> - E6 : `garde_commun.py`, `etat_items` (avec `marque`) : état fermé ou ouvert de chaque item `SHOGEN-…` ou `MONARK-…`
>   de l'annexe B, lu par marqueurs (fermé, clos, soldé, sans objet, non niés ; cellule de tableau ; en-tête d'items
>   fermés ; reste ouvert, rouvert), dernière décision du texte ; tranché n'est pas lu. `avant_acte.py brief --texte F
>   [--fiche NOM]` (`brief`), B1 : un item fermé à l'annexe B que le brief cite sans l'écrire fermé est refusé.
> - E24 : B4, un brief qui nomme une commande git (options globales `-C`, `-c`, `--no-pager`, `--git-dir=`,
>   `--work-tree=` comprises) porte lui-même la règle `liste explicite de chemins`, quelle que soit la fiche.
> - E22, E23 : B2, un constat relayé (sujet : le CC, la G2, le réviseur, le contre-contrôleur, l'avis, un lot nommé ;
>   singulier ou pluriel ; ou `selon`, `d'après`) porte sur sa ligne ou la suivante `chemin:N`, `chemin l.N` ou
>   `JOURNAL l.N` ; B3 (`resoudre`, `faisable`) : chaque `chemin:N` et `chemin l.N` se lit, chaque chemin de base connue
>   existe sauf sur une ligne qui dit le produire, chaque sha court est un commit, chaque sous-commande `avant_acte.py`
>   nommée existe.
> - R11 (crochet GARDE-FAITS, PreToolUse Agent et Workflow) : tout fichier `BRIEF*.md` que nomme la consigne passe
>   `avant_acte.py brief` (dépôt : `CLAUDE_PROJECT_DIR`), refus sur sa sortie 1 ; brief absolu absent : refus ; une
>   consigne `prompt` de plus de `CONSIGNE_MAX` (1500) caractères sans `BRIEF*.md` : refus ; sortie 3 ou délai :
>   acte permis, note. Appelée après R4, avant R9. Skill `shogen-avant-lancer`, point 5.
> - E7, R5 étendue : dans un `BRIEF*.md` écrit par Write, Edit, MultiEdit ou une redirection du shell, chaque compte à
>   unité (tests, fichiers, lignes, mutants, cas, commits, diffs, gardes, items ; `Ran N`) a été affiché avec son
>   unité, ou lu sans unité par `wc` ou `grep -c` (`comptes_nus`, résultat apparié à sa commande). Les fichiers écrits
>   par le shell se lisent sur l'acte (LN-6) : `test_bash_juge_apres_la_serie` (`tests/test_garde_acte.py`) prouve
>   qu'une commande Bash interdite reste refusée après la série, sans erreur interne du crochet.
> - E12 : `garde_commun.py`, `motifs_suspects` (détecteur statique de retour arrière exponentiel sur l'arbre de
>   l'analyseur de `re`, jeux de caractères clos par la casse sous IGNORECASE) et `motifs_ajoutes` ;
>   `lignes_ajoutees(depot, env, racine, plage)` ; `avant_acte.py`, contrôle RX (`motifs`) à `commit`, `diff` et
>   `pousser` ; ligne qui porte `redos-admis` : admis, journalisé.
> - E13 : `avant_acte.py diff --fichier F --rapport R`, `suivi` : D3, toute fonction publique ajoutée à
>   `scripts/controle/*.py` est nommée dans ce README d'après le diff ; D4, tout test ajouté est nommé au rapport R
>   sur une ligne qui dit un mutant tué. Fonctions publiques ajoutées par la phase 2 et nommées ici ou plus haut :
>   C : `passees`, `entree_datee`, `dates_passees`, `unites`, `nommes`, `attribuer`, `empreinte_verif`, `cites`,
>   `empreintes`, `remplacees`, `jetable`, `workflows`, `lignes_ajoutees` ; B : `biblio`, `chaine_active` ; A : `brief`,
>   `marque`, `etat_items`, `resoudre`, `faisable`, `motifs_suspects`, `motifs`, `motifs_ajoutes`, `suivi`.
>
> | règle | crochet | acte jugé | origine |
> |---|---|---|---|
> | R1 | PreToolUse Bash | effacer un worktree ou un clone : status et commits non poussés lus | phase 1 ; LN-6 |
> | R2 | PreToolUse Bash | écrire dans un fichier existant par le shell : fichier lu avant | phase 1 ; acte lu (LN-6) |
> | R3 | PreToolUse Bash | `git commit` : diff ou status lu ; `git push` : ce qui part lu | phase 1 ; acte lu (LN-6) |
> | R4 | PreToolUse Agent, Workflow | consigne qui nomme un arbre git : état de l'arbre lu avant | phase 1 |
> | R5 | PreToolUse | commit ou PR écrit : affiché avant ; comptes d'un brief | phase 1 ; E7 (A) |
> | R6 | Stop, SubagentStop | nombres du dernier texte affichés par un outil | phase 1 ; E29 |
> | R7 | PreToolUse Bash | sleep d'avant-plan ; pkill -f ou pgrep -f à motif non ancré | E18, E28 (B) |
> | R8 | PreToolUse create_pull_request | preuve que la forge lance des jobs sur le dépôt | E20 (B) |
> | R9 | PreToolUse Agent, Workflow | seuil de coût ; jeton FANOUT-AUTORISE | E27 (B) |
> | R10 | UserPromptSubmit, Stop | relevé des noms propres ; dossier nommé sans relevé | E26 (B) |
> | R11 | PreToolUse Agent, Workflow | brief : `avant_acte.py brief` ; consigne longue sans brief | E6, E22-E24 (A) |
>
> Cas de chaque règle (`tests/` du job `controle-unittest` ; R4 et R6 : cas hors CI de
> `.claude/hooks/tests/test_garde_faits.py`) : R1 `test_r1_effacement_lu_sur_l_acte` ; R2
> `test_r2_ecriture_lue_sur_l_acte` ; R3 `test_vrais_refus_restent`, `test_bash_juge_apres_la_serie` ; R4
> `R4_SousAgent.test_refuse_sans_etat` ; R5 `test_r5_lit_le_message_et_le_fichier_de_f`, `test_e7_comptes_du_brief` ;
> R6 `R6_Stop.test_refuse_nombre_non_affiche_puis_passe_au_second_arret`, `R6_Stop.test_refuse_duree_de_memoire_E29` ;
> R7 `test_e18_sleep_d_avant_plan`, `test_e18_boucle_a_condition_de_sortie`, `test_e28_motif_non_ancre_se_reconnait` ;
> R8 `test_e20_forge_sans_job`, `test_e20_marqueur_du_jour` ; R9 `test_e27_workflow_de_dix_agents`,
> `test_e27_fan_out_dans_une_phrase_niee`, `test_e27_jeton_lu_au_journal_de_la_session`, `test_e27_agents_vivants` ;
> R10 `test_e26_courriel_rattache_sans_releve`, `test_e26_releve_puis_rattachement`,
> `test_e26_dossiers_lus_au_fichier`, `test_e26_crochet_branche` ; R11 `test_r11_crochet_agent`.
>
> Empreintes à l'état final de la série (pas INT-24) :
>
> | fichier | sha256 |
> |---|---|
> | `avant_acte.py` | `2cc267b4f93be377fdfc7614280b877b60b299ab09892f6325e855d7d59be1f8` |
> | `garde_commun.py` | `c07b85d96a1c95ea68483539491e2b7e4c367466a972b055e2da95497c8fb41a` |
> | `fm11.py` | `17caaa358ce471c8a9b734873f874794f8c97e66f0125fa05a9dc0cff04452b7` |
> | `SHA256SUMS` | `631e302d48201b35c2ccdab6b1b65c76585c47e8da9cf91edcfbe55ee783bed4` |
> | `gabarits/chaine.sh` | `0d07d39c2d0b809d0d8168931cfe0a40dc4f71277856338227d88f7b546fe511` |
> | `garde/lignes-citees.txt` | `8b6cf5ab967ad7f77e9851a969428c898c8e0097d59b8247a646f56cdab6b8ae` |
> | `garde/forge-actions.txt` | `0ce631b4c66783152afff919699f7d6f006aae7536a447fc014a37261a850ff9` |
> | `garde/dossiers.txt` | `cd22558b07b70752428801ade3fa5f5f2c4f1f418df6087844008b07bb017fa8` |
> | `.claude/hooks/garde_faits.py` | `4a5fcf2d479c1dc6fa937466cb2a8abe1d1b97b3876c1ddfa937784582306790` |
> | `.claude/hooks/acte_shell.py` | `a74689b1d67eec7630a7c046e86a940c9697ebbf94645b2b72b25acf062b736d` |
> | `.claude/settings.json` | `952f4a781c8837c13de413dc3b1e7a1cedbfd367b263708a0f2db486f8167bcc` |
> | `.claude/skills/shogen-avant-committer/SKILL.md` | `50c2844f96d1ac7e7767c1a73f5c8a5dbb6638c25634b996cc15f30b064e1498` |
> | `.claude/skills/shogen-avant-lancer/SKILL.md` | `57f5b4eee9e16ecb0807b094424ba4f2b5c3f980a3ba5c728ec1f773250ecef8` |
> | `.claude/hooks/tests/test_garde_faits.py` | `ec7283fe85c1cdc84ff7d13dcbbef04a42fb1db5d8d72e552af5313490f4d1fc` |
>
> Tests : `tests/test_garde_brief.py` 7 tests, `tests/test_garde_regex.py`
> 3 tests, `tests/test_garde_suivi.py` 2 tests,
> `tests/test_garde_acte.py` 22 tests ; le groupe ajoute 13 tests (dont un de l'intégration) ;
> plancher du job `controle-unittest` 174.

> Ajout daté du 2026-10-16 12:17:57 UTC (`date -u`), correctif CQ-1 (alertes CodeQL de la PR n° 12 sur le crochet GARDE-FAITS) :
> `tests/test_garde_codeql.py` 3 tests (temps borné de `NOM_PROPRE`, mêmes mots reconnus, hôte de la forge lu par
> `urlsplit`, sens sûr : schéma en toute casse, mot sans schéma, URL que `urlsplit` refuse, URL dans une variable du shell) ; plancher du job `controle-unittest` 177.

> Ajout daté du 2026-10-16 23:37:58 UTC (`date -u`), lot ISOLE-ENV (erreur E39 du registre de l'orchestrateur) : `tests/aide_garde.py`,
> `variables_de_chaine()` lit les variables `${NOM:` des modèles `gabarits/*.sh` ; `env_git` ne les hérite plus de
> l'environnement ambiant (une chaîne lancée avec `DETACHE=1` faisait rougir `test_e25_lancement_lie`) ;
> `tests/test_aide_garde.py` 2 tests ; plancher du job `controle-unittest` 179.

> *Ajout daté du 2026-10-17 01:50:28 UTC (`date -u` ; lot INTEGRATION-P3 : GARDE-FOUS phase 3, groupe C, pas INT-01 à INT-06 ;
> annexe B, B.108 et B.109 : SHOGEN-GARDE-D3-MOT-COMMUN-1, SHOGEN-MOTIFS-ARBRE-REDOS-1, phase 3 de
> SHOGEN-GARDE-FOUS-ORCH-1 ; relecture G2 du groupe, C-1 à C-5)* : un ajout pour le groupe.
> - D3 (SHOGEN-GARDE-D3-MOT-COMMUN-1) : D3 de `avant_acte.py diff` cherche le nom d'une fonction publique ajoutée au
>   README en code (`nomme_en_code(nom, texte)` : passage entre accents graves qui est le nom seul ou qualifié) ou en
>   signature (`nom(`, en code ou non, qualifiée ou non : `module.nom(a)`), non plus comme mot courant : une fonction
>   `suivi` n'est plus nommée par « non suivi » ; `nom(` après `/`, `-` ou `$` (URL, chemin, identifiant composé :
>   `non-suivi(x)`) ne compte pas (G2, C-1). Cas : `tests/test_garde_suivi.py`, `test_d3_mot_commun`.
> - Motifs de l'arbre (SHOGEN-MOTIFS-ARBRE-REDOS-1) : `avant_acte.py motifs --arbre` (`motifs_arbre(a, fautes)` ;
>   `motifs(fichiers, fautes, liste=None)` reçoit la liste lue) passe le détecteur `motifs_suspects` sur tous les
>   motifs déjà dans l'arbre, non plus sur les seuls diffs reçus : appels de `re` des `.py` de `scripts/controle/`,
>   `.claude/hooks/` et `enforcement/` (`DOSSIERS_MOTIFS`), lus sur l'arbre d'ast par `motifs_du_code(texte)` de
>   `garde_commun.py` (appel sur plusieurs lignes, concaténation, `chr(N)`, `sep.join`, noms de premier niveau,
>   drapeaux `re.I` et `re.X` ; la méthode d'un motif compilé, `SAIN.search(…)`, porte un sujet et n'est pas lue, G2,
>   C-5), et motifs YAML des `.yml` (`motifs_ajoutes`). Sortie : une ligne `REFUS RX` par motif suspect avec
>   `chemin:ligne` (sortie 1), `ADMIS RX` sous `redos-admis`, `NON-LU chemin:ligne` par motif construit autrement
>   (variable, `re.escape`), jamais jugé, puis un bilan. Limites : les motifs des scripts shell et des workflows de
>   `.github/` ne sont pas lus ; un motif non lu n'est pas jugé. Cas : `tests/test_garde_regex.py`, `test_motifs_arbre`.
> - Journal des refus (phase 3 de SHOGEN-GARDE-FOUS-ORCH-1, écriture) : chaque refus et chaque passage du crochet
>   `.claude/hooks/garde_faits.py` écrit une ligne au journal `scripts/controle/garde/refus.tsv` (`consigner(entree,
>   regle, acte)`) : heure lue par `date -u`, événement (`PreToolUse:Bash`, `Stop`…), règle du refus (`R1` à `R11`)
>   ou `permis`, `erreur` (erreur interne, acte permis sans contrôle), acte abrégé à 80 caractères (`abreger(texte)` :
>   blancs réduits, valeur d'une clé `token`, `secret`, `password`, `api_key`, `authorization`…, mot de passe d'une
>   URL (`https://alice:***@hôte`) et de `curl -u alice:***` (`MOT_DE_PASSE`, G2, C-2 ; port gardé) et jeton mêlant
>   chiffres, minuscules et majuscules masqués par `***` avant la coupe), agent (`principal` ou identifiant du
>   sous-agent). Écriture atomique : en-tête posé par lien d'un fichier complet, ligne ajoutée d'un seul `write` en
>   `O_APPEND` ; dossier absent ou erreur : rien, jamais un refus. Le journal n'est pas versionné : choix du
>   `.gitignore` de son contenu (`scripts/controle/garde/.gitignore`), non de l'en-tête seul, qui rendrait l'arbre
>   sale à chaque passage (refus S1 de `sceller`) ; le journal du dépôt reste donc vide au commit. `SHOGEN_GARDE_REFUS`
>   (`chemin_refus()`) le déplace : les cas le posent (`tests/__init__.py` : `/dev/null`, journal éteint). Cas :
>   `tests/test_garde_refus.py`, `test_refus_journal_des_passages` (refus R11 et R10 consignés sous leur règle, G2,
>   C-4), `test_refus_entete_unique`.
> - Relevé des refus au premier message (même item) : au premier message d'une session (aucun autre message de
>   l'humain au journal de la session, lu depuis sa tête par `lire_tete`, G2, C-3), le crochet UserPromptSubmit
>   affiche, après le relevé E26 des noms propres, une ligne `RELEVÉ DES REFUS` : refus du journal depuis la dernière
>   ligne `releve`, par règle (la plus fréquente d'abord), et la commande du détail (`avant_acte.py refus --depuis` le
>   jour du dernier relevé), puis écrit une ligne `releve` (`releve_refus(entree)`) ; journal éteint (`/dev/null`) :
>   rien ; journal des refus absent ou non écrit : le relevé le dit (jamais 0 refus) ; une erreur du relevé des refus
>   ne fait plus tomber le relevé E26 (G2, C-3). Cas : `tests/test_garde_refus.py`, `test_refus_releve_premier_message`.
> - Lecture du journal (même item) : `avant_acte.py refus [--depuis AAAA-MM-JJ] [--journal F]` (`refus(a, fautes)`)
>   lit `scripts/controle/garde/refus.tsv` du dépôt et rend : refus par règle et par jour, les dix actes refusés les
>   plus fréquents (avec leurs règles), les règles du crochet sans refus depuis trente jours, borne lue par `date -u`
>   et comprise, sur tout le journal (candidates à relire ; règles lues dans la docstring du crochet par
>   `regles_du_crochet(chemin)`), le nombre de passages (`permis`, `erreur` ; lignes `releve` exclues) et les lignes
>   illisibles ; `--depuis` filtre tout sauf les règles sans refus ; date mal formée ou journal absent : 3. Cas :
>   `tests/test_garde_refus.py`, `test_refus_lecteur`.
>
> Le groupe ajoute 6 tests (`test_d3_mot_commun`, `test_motifs_arbre`, `test_refus_journal_des_passages`,
> `test_refus_entete_unique`, `test_refus_releve_premier_message`, `test_refus_lecteur`) ; plancher du job
> `controle-unittest` 185.
