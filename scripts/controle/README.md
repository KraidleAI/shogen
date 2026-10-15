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
