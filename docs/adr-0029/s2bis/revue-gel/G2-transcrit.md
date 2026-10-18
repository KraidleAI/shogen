# Relecture G2 neuve du lot GEL-COLLECTEUR-1 (C-3, C-4) (transcrit)

> Transcription par l'orchestrateur le 2026-10-18 15:17:59 UTC du fichier s2bis/gel/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (443 occurrences, aucune autre). Texte ci-dessous avec 4 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date mises en code (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 — lot GEL-COLLECTEUR-1 (gel du collecteur de S2-bis, Q-C-06)

Gate 0 : modèle `claude-opus-5-5` (worker `shogen-worker`, effort high), réviseur distinct du générateur. Écrit le
2026-10-18 entre 04:50 et `05:15` UTC (`date -u`). Brief : `BRIEF-G2.md` (sha256
`cf3965cd18b1bd0cfb22f3554d54f0f4edca6169508439d568855c7d1aacb849`). Base : `1d7e5d485e78a8b3d3b713557de5cf236279f833`
(`git rev-parse` sur le dépôt réel et sur chaque copie), égale à la tête du brief. Dépôt réel jamais écrit ; copies
creuses non-cone (interdits du brief et `*.jsonl` exclus) ; tests sous `unshare -n` (lo allumée), `TMPDIR` du G2,
variable scellée jamais posée ; tout Python en `python3 -I -B`.

Série relue : les neuf diffs du générateur (`../diffs/GEL-1.diff` à `GEL-9.diff` ; `../SHA256SUMS` contrôlé : 11 OK),
ordre 1, 2, 3, 4, 5, 7, 8, 6, 9 ; empreinte de leur concaténation dans cet ordre :
`00c7b034c5b2a768ae601de5880b82886e1b7428d8084e3339f474f02423c91a`.

## Verdict : ACCEPTE-AVEC-CORRECTIONS

Liste fermée (C-1 et C-2 sont les corrections du brief de correction du générateur ; la G2 numérote à la suite) :

- **C-3 — amende GEL-7** (`diffs/C-3.diff`, contre l'arbre final de la série) : (a) la liste fermée filtre les noms
  des fichiers de tête **avant** la borne de lecture `NOMBRE` (16) : sur la série, seize têtes valides d'un nom hors de
  la liste, triées avant `o2`, évincent la tête de `o2` du manifeste du jeton (sonde D-1 ; `preuves/C-3-rouge.txt` :
  `o2` absente, `o9` même pas nommé) : la liste fermée ne protège pas le manifeste, contre l'objet de
  SHOGEN-S2BIS-OBSERVATEURS-LISTE-1 et contre FORMAT §16.8 (têtes hors liste « ignorées (hors du manifeste) ») ; (b)
  mutant R-09 vivant (`--envoi` comparé par préfixe) : cas `https://x/ts`, `https://x/tsr/`, `https://x` ajoutés ; (c)
  FORMAT §16.8 : ligne de 170 colonnes remise à 120, `(au gel : C-1)` qualifié ; docstring de `test_commande_jeton`
  remise à jour (l'URL http n'y est plus testée ; elle l'est par `test_envoi_http_vers_la_boucle_locale`). 31 lignes
  de code ajoutées.
- **C-4 — amende GEL-4** (`diffs/C-4.diff`, contre l'arbre final de la série) : (a) à la reprise, le manifeste et
  chaque fichier listé sont ouverts sans suivre de lien ni attendre (`O_NOFOLLOW`, `O_NONBLOCK`, fichier ordinaire
  exigé), le manifeste en ajout (`O_APPEND`) : sur la série, un lien au nom de `captures.txt` vers un fichier hors du
  dossier fait écrire les lignes de la reprise hors du dossier (sonde D-2 : 4 lignes écrites dehors, code 0), et un tube
  nommé bloque la commande (limite déclarée par le générateur) ; le §19 pt 3 (`Chaque fichier, manifeste compris, est
  ouvert en création exclusive`) était inexact sous `--reprise` ; (b) mutants R-05 (somme comparée sur 63 chiffres),
  R-06 (carte listée en panne comptée au code), R-07 (manifeste vide refusé) vivants : cas ajoutés ; (c) cas de course
  (lien posé entre la lecture du manifeste et son ajout). 82 lignes de code ajoutées.

Chaque correction se verse en **diff distinct après GEL-9** : GEL-7 + C-3 = 204 et GEL-4 + C-4 = 230 lignes de code
ajoutées, au-delà des 200 de R-25. Les deux s'appliquent seuls et ensemble, dans les deux ordres
(`preuves/C-apply-check.txt`) ; cas ajoutés dans des tests existants : plancher inchangé, 442. Arbre final corrigé :
job s2bis vert (runner 153 ok, `Ran = 442`) pour C-3 seul, C-4 seul et les deux (`preuves/corr3-vert.txt`,
`corr4-vert.txt`, `corr-vert.txt`) ; matrice 3.10 à 3.13 verte (`preuves/corr-matrice-*.txt`) ; xtask : même verdict
que la série (`preuves/xtask-corr-verdicts.txt`).

## Checklist

1. **Série — conforme.** `git apply --check` puis `git apply` des neuf diffs dans l'ordre sur une extraction neuve
   (`preuves/apply-check.txt`). À chaque état, commande du job s2bis (runner, puis ligne `--egal` au plancher écrit dans
   le diff) verte : 433, 433, 434, 436, 437, 440, 440, 441, 442 (`preuves/GEL-k-vert.txt` ; runner 153 ok à chaque
   état). Arbre final : S2 `conforme (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)`,
   sim-bis `conforme (code 0, résumé final, aucun saut, Ran = 279)` ; matrice `-X dev -W error` 3.10.20, 3.11.15,
   3.12.3, 3.13.14 : code 0, `Ran 442`, `OK`, 0 ligne `Exception ignored` ou `Warning` (`preuves/matrice-*.txt`) ;
   `cargo --locked xtask verify` (cible par défaut de la copie, hors ligne) : S-G1 à S-G8 `VERDICT : VERT (0
   violation(s))`, `cargo fmt --check : VERT`, `no_std … : VERT`, `cargo clippy -D warnings : VERT`, S-G9 `VERDICT :
   ROUGE (1 violation(s))`, `VIOLATION docs/17-modele-de-menace.md:70` (renvoi vers `docs/rapports/…`, exclu de la
   copie) : la violation connue, aucune autre (`preuves/xtask-verdicts.txt`). Comptes R-25 recomptés par
   `git apply --numstat` (`.py`, `.yml`) : 61, 16, 29, 148, 116, 173, 0, 30, 24, ceux du rapport du générateur.
2. **Configurations scellées — conforme.** `formes.json` : ses 33 formes sont celles de l'ancien `formes-pool.json`
   octet pour octet (27 lignes de forme et la fermeture identiques), sauf le seul champ `hote` des quatre formes
   `binance_*` (`data-api.binance.vision`) et le `corps` d'`uniswap_usdc_usdt` et `curve_usdc_usdt` (lot JSON-RPC) ;
   `w` 60 (ADR l.88), `delta` 20 000 000 et `delai` 10 000 000 (l.233), `tolerance` 5 000 000 (l.107), `marge`
   1 000 000 (l.233), `places` 40 (décision de l'orchestrateur), budget 5 + 4 + 10 + 1 = 20 s. `sante.json` :
   `["chronyc", "-n", "tracking"]` (FORMAT §13.3), témoins 198.41.0.4, 192.36.148.17, 193.0.14.129 (l.109), noms
   `www.kernel.org`, `www.arin.net` (ceux de `../ADJUDICATION-DNS.md`), `delai` 2 000 000 (l.109-110).
   `observateurs.json` : `o1` à `o4`, **aucune `tsa`** (aucune URL de TSA scellée ; Certigna à DB-3). `carte.json` :
   vide, `depart` 5 s (E-C-32), `delai` et `marge` du pool, `places` 1, `asn` {86 400, 0}. Lignes de l'ADR contrôlées à
   `e16956b` (convention du FORMAT) : l.78-83, 88, 107-110, 171-172, 233-235 portent les valeurs citées. Aucun flottant
   dans les quatre fichiers (`parse_float` instrumenté : 0). Chargements : `formes` et `sante` par `entree.configurer`,
   `carte` par `configurer_secondaire`, `observateurs` par `config.charger` (schéma et règles) ; règle `budget` à
   l'égalité. Réserve : `places` 1 et `decalage` 0 de la carte n'ont pas de pièce (choix déclaré du lot) : Q-2.
3. **Bloc du témoin (GEL-5) — conforme.** `CORPS` = `[eth_blockNumber id 1, eth_call latest id 2, eth_blockNumber id
   3]`, `json.dumps` aux séparateurs par défaut, égal au texte écrit à la main du test et au `corps` de `formes.json`
   (règle `corps-du-decodeur`) ; appariement par `id` (`parse_int=Decimal` ; `id` 1.0 ou `"1"` refusés) ; trois
   réponses exigées ; `error`, lot incomplet ou de quatre, bloc hors de `0x[0-9a-fA-F]{1,16}`, `bloc_apres` <
   `bloc_avant` : panne entière ; extra `bloc_avant`, `bloc_apres` en chaînes décimales. Fixtures recomposées par script
   depuis celles de `1d7e5d4` (`outils/fixtures.py`) : égales octet pour octet (élément id 2 = ancienne réponse,
   `id` 1 → 2 ; blocs 0x18f039f, 0x18f03a4, 0x18f03a5 ; Curve dans l'ordre 3, 1, 2 ; sha256 de Curve
   `596550e9eb1ab3d69a6206965241d4bea90544949752edb0ff6cef285fe61dd9`, celui du test) ; blocs 26 149 791 et
   26 149 796 lus à `PAIRES-ET-TEMOIN.md` l.90 et l.94. FORMAT §9.1 : « non atomique », écart attendu d'au plus un bloc.
4. **Reprise de capture (GEL-4) — non conforme sur un point, corrigé par C-4.** Conformes : manifeste créé avant la
   première lecture et vidé ligne à ligne ; sommes recontrôlées (`somme`), formes listées sautées, fichier non listé
   refusé (`fichier`), manifeste refusé (`manifeste`) ; sans `--reprise`, comportement d'avant ; noms lus au manifeste
   pris dans la liste fermée du plan (aucune traversée par le nom) ; rien sur la sortie standard. Défaut : traversée par
   **lien** à la reprise (ajout au manifeste à travers un lien symbolique, hors du dossier) et tube nommé bloquant
   (`preuves/C-4-rouge.txt` : 5 FAIL, dont deux `bloqué`) ; trois trous de test (R-05, R-06, R-07).
5. **Observateurs et jeton (GEL-7) — non conforme sur un point, corrigé par C-3.** Conformes : liste fermée lue par
   `status` (avec `--depot`), `resume`, `jeton` ; nom hors liste ignoré et nommé (résumés, têtes) ; descripteur hors
   liste : `CONFIG/observateur`, sortie 2 ; `--envoi` refusé sans `tsa` scellée et refusé si autre que la `tsa`
   (`CONFIG/tsa`, sortie 2) ; `.armement` écrit par `tetes.ecrire` (temporaire exclusif, `fsync`, `os.replace`, dossier
   synchronisé), ligne canonique `{arme, jour, observateur, tsa}` testée octet pour octet, aucun secret au gel (`tsa`
   null, ou l'URL armée). Défaut : têtes hors liste lues avant le filtre et comptées dans la borne (D-1) ; trou de test
   R-09.
6. **Tests — conforme.** Rouge avant, vert après, pour chaque diff de code : tests du diff seuls appliqués sur l'état
   précédent (`preuves/GEL-k-rouge.txt`) : GEL-1 2 FAIL et 8 ERROR ; GEL-2 3 FAIL ; GEL-3 2 FAIL et 1 ERROR ; GEL-4
   2 FAIL et 12 ERROR ; GEL-5 11 FAIL (`test_capture` seul vert : report de sha256 déclaré) ; GEL-7 1 FAIL et 6 ERROR ;
   GEL-6 1 FAIL et 1 ERROR ; GEL-9 1 FAIL et 1 ERROR. Les ERROR sont des fichiers ou attributs absents (le générateur a
   montré ses rouges d'assertion sur des squelettes). Caractérisation déclarée : `ORDRE` (ordre de `formes-pool.json`
   à la base), sha256 de Curve (`sha256sum`). Valeurs scellées : `SCELLEES`, `SONDES`, `CARTE_GEL`, chacune sous sa
   ligne ou sa source, texte des lignes cherché dans l'ADR ; liste des observateurs : l.78-82.
7. **Mutants — deux fautes, corrigées.** Outil `scripts/controle/mutants.py` du dépôt réel (sha256
   `3e21878363ad7a106357abb666c3d8c5351f8ac94fcf3d95c4e64400abddad64`), commande du job `s2bis-unittest`, borne 300 s,
   copie mutée à part, relevé `ps` de fin vide à chaque campagne. Échantillon rejoué sur l'arbre final (25 mutants du
   générateur, GEL-3 à GEL-9) : 24 tués, G3-05 vivant, classements identiques aux siens (`mutants/rejoues.*`).
   Mutants de la G2 (12, `mutants/mien.*`) : R-01 appariement par position, R-02 comparaison des blocs inversée, R-03
   blocs permutés à la lecture, R-04 `match` au lieu de `fullmatch`, R-08 statut lu dans la colonne du code, R-10 noms
   ignorés pris après le filtre, R-11 nom de fichier au lieu du nom d'observateur, R-12 liste non transmise par
   `status.rapport` (site d'appel) : **tués** ; R-05, R-06, R-07 (GEL-4) et R-09 (GEL-7) : **vivants, non
   équivalents** → C-4 et C-3. Mutants des corrections (12, K-01 à K-12, `mutants/corrections.*`) : 12 tués, 0 vivant,
   0 FATAL, au second passage (premier passage gardé : `mutants/corrections-passage1.*`, K-08 vivant). **G3-05 jugé
   équivalent** : `entree.NOM = re.compile("[a-z0-9_][a-z0-9_.-]{0,63}")` rend, par le cache de `re`, l'objet même de
   `capture.NOM` (même motif, mêmes drapeaux) : aucun comportement ne diffère ; `assertIs` ne prouve pas l'unicité de
   la constante dans le source, il en prouve le comportement, ce qui suffit à l'item (G3-05b, autre texte, est tué).
8. **Documentation — conforme, deux inexactitudes corrigées.** FORMAT §9.1, §14.1, §15.2, §16.8, §17.5-6, §19 et
   paquet §4 à §6 relus : remplaçants `api.binance.com` et `www.cern.ch`, Q-C-07, carte vide au gel, exacts ; aucune
   mention de FreeTSA dans le FORMAT, le paquet ni les diffs (0) ; R-13 : 0 `TODO`/`FIXME` ajouté ; heures : seules
   `00:00 UTC` (heure quotidienne d'une cadence, non un instant) et des heures datées. Inexactitudes : §19 pt 3 sous
   `--reprise` et §16.8 (170 colonnes, `C-1` ambigu) : corrigées par C-4 et C-3. METRIQUES : une section par diff,
   forme INT-P2 ; chaque correction ajoute son paragraphe dans la section du diff qu'elle amende.
9. **Items — conformes ; trois items et deux questions à former.** Tests nommés au rapport du générateur : les 13
   présents (chargés un à un par `unittest`). Re-datages justes : `resolv.conf` → DB-2 (configuration de déploiement,
   hors du paquet Python) ; URL de la TSA → DB-3 (G0 l.44-46 ; ANNEXE-B l.1325). SHOGEN-S2BIS-DNS-TEMOINS-RODAGE-1
   juste (TTL d'origine non lu sur autoritaire : pièce §0 et l.75). CONFIG-PRODUCTION-1 : fermeture partielle juste
   (E-C-11, E-C-27, E-C-28 liés par test ; marge 40 ; état d'armement).

## Items et questions à former (règle PAROXYSME)

- **I-1 SHOGEN-S2BIS-OBSERVATEURS-LISTE-BOUCLE-1** : l'enregistrement `tetes` de la boucle (`Depot.lire`) ne lit pas
  la liste fermée : il consigne au journal les têtes de tout nom de la grammaire, et seize têtes hors liste triées avant
  un observateur de la liste l'en évincent (même borne `NOMBRE` que D-1). Hors du périmètre de l'item fermé (status,
  resume, jeton), mais il touche le journal : à décider **avant le gel** (après, une correction refait le rodage
  entier, AVIS l.95).
- **I-2 SHOGEN-S2BIS-REMPLACANTS-LECTURE-1** : Q-C-08 adoptée (PROPOSITION l.350, AVIS l.97) veut les remplaçants
  « lus par le processus secondaire, hors du vote » ; au gel, la carte est vide (C-2) : `api.binance.com` n'est lu par
  aucun processus, et une bascule n'aurait aucune lecture de rodage à l'appui ; le paquet §4 dit pourtant qu'un
  remplaçant « n'est lu que par le processus secondaire ». À adjuger : forme du remplaçant lue par le processus
  secondaire (hors de la carte descriptive), ou texte du paquet amendé.
- **I-3 volet de SHOGEN-S2BIS-TSA-CERTIGNA-1** (l.1325) : la règle `tsa-https` refuse port et majuscules d'hôte, et
  `.armement` écrit l'URL armée en clair au dépôt : l'URL scellée à DB-3 ne doit porter aucun secret (authentification
  hors de l'URL), et la règle se relit sur l'URL de Certigna.
- **Q-1** : paquet §4, « refait le rodage selon Q-C-06 (7 jours, dont un week-end, AVIS l.95) » : à l'AVIS l.95, les
  7 jours valent pour « un remplaçant (l.224) », règle de remplacement d'un observateur ; leur extension à une bascule
  de source est la lecture de l'advisor (Q-A), adoptée par l'orchestrateur : à écrire comme telle au paquet.
- **Q-2** : `places` 1 et `decalage` 0 de `carte.json` sont des choix du lot sans pièce (ADR l.219 met au paquet la
  cadence des relevés ASN) : à ratifier.
- Observations, sans correction : `status --journal J --observateurs L` sans `--descripteur` est refusé par
  `CONFIG/observateur : None hors de la liste` (message non documenté ; `CONFIG/options` serait plus juste) ;
  `.armement` est réécrit à chaque relance du jour (une tentative armée suivie d'une relance non armée n'en laisse pas
  trace au dépôt).

## Écarts de la G2

- E-1 : deux énumérations récursives (`find … -name __pycache__`) sur mes copies `travail/base` et `travail/serie`,
  sous le scratchpad, contre l'interdit du brief ; rien trouvé ; copies creuses (interdits exclus) ; remplacées ensuite
  par `ls -d` sur les racines de suite nommées.
- E-2 : `outils/isole.sh` partagé appelle un `lo_up.py` absent (même constat que l'E-1 du générateur) : copie locale
  (`outils/isole.sh`, avec le `lo_up.py` du générateur, relu : ioctl `SIOCSIFFLAGS`) ; isolement contrôlé (boucle
  locale joignable, 1.1.1.1 : `Network is unreachable`).
- E-3 : le hook a refusé un script nommé `chaine.sh` (règle R13, chaînes de commit) ; c'était une suite de contrôles
  sans commit : renommé `controles_lourds.sh`, contenu inchangé.
- E-4 : premier passage des rouges invalide (`-I` retire le dossier courant de `sys.path` : `-m unittest tests.x` ne
  s'importait pas) ; refait par `discover -p` (`outils/rouges.sh`), sorties remplacées.
- E-5 : campagne K, premier passage : K-08 vivant (le lien était refusé dès la lecture) ; cas de course ajouté à C-4,
  campagne entière rejouée.
- E-6 : pour situer la violation S-G9, lecture du bloc S-G9 de la sortie brute de xtask (chemins couverts, notes) ;
  seules les lignes de verdict sont versées.
- E-7 : enregistrement du rôle G2 par `oracle_record.py` non fait : la consigne vise le chemin S2 (dossier soumis au
  cp-2) ; ce lot est de S2-bis (ADR-0029). À faire si l'orchestrateur le juge applicable.

## Journal de provenance (G1)

Sources [lu] (sha256 complets) : `BRIEF-G2.md` `cf3965cd18b1bd0cfb22f3554d54f0f4edca6169508439d568855c7d1aacb849` ;
`../RAPPORT-GENERATEUR.md` `1032a05c0d42416433ed788cfa53db44001596d807bf575b4a3ad3511280eeee` ; `../NOTES.md`
`1c69fb7915a36630956aedd029232a130098c4bfad57bb0c148129c9b1b0e4ba` ; `../BRIEF-GEL.md`
`dfe047b50ae67f063353b2449bd4dc2c8e4169910fe789ff749ab03024bb5793` ; `../BRIEF-GEL-CORR.md`
`83e75b3c77adba44e3643241dcdc80d62c24bd69d6976af6a4941461d855ca88` ; `../AVIS-ADVISOR.md`
`10ed1f5f2ffa1211e7bcfb9fe819323248af8a215db4934a1288a58a2149fb69` ; `../ADJUDICATION-DNS.md`
`c55e443ec61e25828cd79fdd4da548fc8f1f691ffb16198348f5d8f7c5448620` ; `../LECTURE-DNS-TEMOINS.md`
`76d170cb8f99bed2191eb221492b690902931db74223ab645d869aef351a91d6` (tous entiers) ; les neuf diffs (entiers ; sha256
de `../SHA256SUMS`, contrôlés). À la base : PROPOSITION
`0cdf84c25092101a9f2d8075fc90f59a5af7b689458b025635d42adb865fbfd0` (l.172, 188-193, 201, 336-355) ; AVIS
`a919b307e80f860733f9e114504c0ec93e30a87fabb0970b9384a854421616ce` (l.30-45, 68-100) ; ADR-0029
`32a598931dd35c91afbc7e61fec532a1a18de2e4c69e188b2d22b97aadaa2801` (l.76-90, 105-112, 165-176, 215-240) et sa version
au commit `e16956b` `02f8f6ccd1c40c423d120d9a9d7267429ff35dd4dc2943b6f283f097e106a6d0` (l.78-83, 88, 107-110, 171-172,
233-235) ; ANNEXE-B `a531fd23554ccd0a68a6793b03258324501b4f238026b813d620806ec5221a73` (l.1152, 1325, 1327-1339,
1980, 1982-1984 ; ce seul fichier) ; G0 `08c1e6b0d307e11509798bd9409c6947e11df381602e22ad20f10a32c8ec691d` (l.40-50) ;
PAIRES-ET-TEMOIN `75535ad5a43c3d1b0fc7eaaaed52f260bc9c8c51f1dfbc45feb4dcddddc1258b` (l.37, 44, 90, 94, 131) ;
gates.yml `77182a393264c1a559b82d1e1ba97130a94eef9d80166354cc00c0c3c43de632` (l.270-300). À l'arbre final : FORMAT
`8b6f745a5cf3e5a71c05c0bc9e0cfb38b71c22edcd1635a475b7658990185a5f` et paquet
`5fab36f25bd87c08a1cea7140e4239c523cb1ba14fd5e9f7fe38fbf3f791be87` (sections touchées) ; code et tests de `s2bis/`
touchés (capture, decodeurs, entree, status, tetes, `journal.ordinaire` ; test_capture, test_tetes, test_status,
test_format, test_formes_pool, test_temoin, test_entree) ; configurations finales : `formes.json`
`3377811cbf172ec11c6ae4c2697dcc7fd11ca2352ce458cfbe962fc5f950e7a7`, `sante.json`
`30d96460c8cebcb54281a33d2df4815a2656d9444a540896f40748ce64e06724`, `observateurs.json`
`acc3964716b97d1c1745b1e681eaa51d679beea36f76f130b604a39abd0f3274`, `carte.json`
`2a417366f14056263aca57c68bd3d03064d0d9452240335f9069d267dc22d3e4` ; `scripts/controle/mutants.py`
`3e21878363ad7a106357abb666c3d8c5351f8ac94fcf3d95c4e64400abddad64` (docstring). [2nd] : aucune. [abs] : les premières
versions de GEL-6 et GEL-8 (régénérées, non gardées) : l'identité de leurs lignes ajoutées et retirées, déclarée par
le générateur, n'est pas recontrôlée.

Commandes (sorties sous `preuves/` et `mutants/`) : `git clone` local, `git sparse-checkout` non-cone, `git rev-parse` ;
`git apply --check`, `git apply`, `git apply --numstat` ; `outils/etats.sh` (vert à chaque état) ; `outils/rouges.sh`
(rouges) ; `outils/controles_lourds.sh` (S2, sim-bis, matrice, xtask, campagnes de la série) ;
`outils/controles_corrections.sh` et `outils/controles_finaux.sh` (corrections) ; `outils/fixtures.py`,
`outils/formes.py` (recomptes) ; `outils/sonde_defauts.py` (D-1, D-2) ; `outils/ecrire_mutants.py`,
`outils/ecrire_mutants_k.py` (mutants, `avant` contrôlé présent une fois) ; `outils/corr_c3.py`, `corr_c4.py`,
`corr_c4_test.py`, `corr_metriques.py` (corrections, chaque remplacement contrôlé présent une fois). Chiffres recomptés
ici : planchers par `Ran`, comptes R-25, lignes et écarts de `formes.json`, hexadécimal des blocs (`hex()`), sha256 des
fixtures, classements des campagnes (sorties JSON de l'outil).

Copies lourdes supprimées en fin de relecture (`travail/`, `tmp/`) ; gardés : `NOTES.md`, ce rapport, `diffs/`,
`preuves/`, `mutants/`, `outils/`, `SHA256SUMS`.

## Suite : C-5, C-6

Gate 0 : `claude-opus-5-5`, même réviseur, distinct du générateur. Écrit le 2026-10-18 entre 06:17 et `07:15` UTC
(`date -u`). Brief : `BRIEF-G2-SUITE.md` (sha256 `add57aad069811301ab1725958df5351c1a06ed38d642e74622d978b38747e92`) ;
lus : `../BRIEF-GEL-CORR2.md` (`3a826cdb9157d28bf336587c9c57eebb3b879114b0fadc5d08970a2d40c357aa`),
`../RAPPORT-GENERATEUR.md` (`c7995d7b67fda559ef5ac92aa304375d95a02fd74e4a5d5f7867b2680eea7ebd`, sections C-5, C-6),
`../diffs/C-5.diff` (`defe420786310897411a466230377fc1ff5518c0cca1133cafb5cd30087684a3`) et `../diffs/C-6.diff`
(`4aa04e61f6a905bf80ba010915c7b8787195716324471496da9adc54b6721955`), entiers ; `../SHA256SUMS` : 13 OK. Base relevée
`1d7e5d485e78a8b3d3b713557de5cf236279f833`.

### Verdict : ACCEPTE-AVEC-CORRECTIONS (C-7)

- **C-7 — amende C-5** (`diffs/C-7.diff`, sha256 `cab5ba3f41222bb86d97271f154a0b84d6b16a59ef8a1b1a6e6a97d4e3294550`,
  contre l'arbre final des treize diffs ; documentation et tests, 16 lignes de code de test) : (a) FORMAT §14.4 ne
  nommait que le sha256 de la liste dans `run_params`, alors que le code (`entree._run_params`) en écrit aussi le
  contenu `observateurs`, que le test de C-5 lit : contenu nommé ; (b) mutant S-03 vivant (`pool --observateurs L`
  sans `--depot` : liste ignorée, ni contrôle ni `run_params`, contre le §14.4 « avec `--observateurs` ») : cas ajouté
  (contenu à `run_params`, `o9` refusé) et §14.3 précisé ; (c) mutant S-05 vivant (`ignores` écrasé au lieu d'être
  cumulé quand la borne de `lire_tetes` et celle de `TETES/liste` débordent ensemble) : cas ajouté (2 + 1). Rouge sur
  l'arbre final : 1 FAIL du FORMAT (`preuves/suite/C-7-rouge.txt`) ; arbre final + C-7 : job s2bis vert (runner 153 ok,
  `Ran = 443`, plancher inchangé), matrice 3.10 à 3.13 verte ; S-03, S-05 et S-06 (FORMAT) tués au rejeu
  (`mutants/suite-c7.*`).

### Checklist restreinte

1. **Série — conforme.** Treize diffs appliqués dans l'ordre sur une extraction neuve (`preuves/suite-apply-check.txt`) ;
   à chaque état, commande du job verte au plancher écrit : 433, 433, 434, 436, 437, 440, 440, 441, 442, 442, 442, 443,
   443 (`preuves/suite/etats.txt` ; la ligne `DIFFERE s2bis/config/formes-pool.json` est un artefact du contrôle :
   fichier absent des deux arbres). Arbre final : S2 `Ran = 423`, sim-bis `Ran = 279` (`final-s2-simbis.txt`) ; matrice
   3.10.20 à 3.13.14 : code 0, `Ran 443`, aucune ligne `Exception ignored` ni `Warning` ; xtask : S-G1 à S-G8 VERT, fmt,
   no_std, clippy VERT, S-G9 seule `VIOLATION docs/17-modele-de-menace.md:70` (connue) (`preuves/suite/`).
2. **C-5 — conforme (avec C-7).** Sonde de l'éviction mesurée en G2, rejouée sur `Depot.lire` : `o2` lue, 16 refus
   `TETES/liste` (`outils/sonde_suite.py`) ; refus `TETES/liste` bornés à `NOMBRE`, reste aux `ignores` ;
   `pool --depot` sans `--observateurs` : `CONFIG/options`, sortie 2 ; descripteur hors liste : `CONFIG/observateur` ;
   `run_params` porte sha256 et contenu de la liste ; taille de l'enregistrement `tetes` sous LIMITE (4 Mio). R-25 : 66.
3. **C-6 — conforme.** Les quatre `binance_<actif>_remplacant` ne diffèrent des formes `binance_*` du pool que par
   `nom` et `hote` (contrôle champ à champ) ; `api.binance.com` absent du pool (aucun budget partagé) ; `places` 4
   (ratifié) ; carte chargée par `configurer_secondaire` ; aucun flottant. Paquet §4 (Q-1) et §6 (Q-2, `decalage` 0)
   écrits comme décisions. R-25 : 22.
4. **Rouges et mutants — conformes après C-7.** Rouge des tests seuls sur l'état précédent : C-5 1 FAIL et 2 ERROR,
   C-6 3 FAIL (`preuves/suite/C-5-rouge.txt`, `C-6-rouge.txt`). Mutants du générateur rejoués : 14 (C5-01 à C5-09,
   C5-11 ; C6-01, C6-03, C6-04, C6-09), 14 tués (`mutants/suite-rejoues.*`). Mutants de la G2 sur C-5 (5, S-01 à S-05,
   `mutants/suite-mien.*`) : S-01 (16 → 15 refus nommés), S-02 (débord compté de moins), S-04 (FORMAT) tués ; S-03 et
   S-05 vivants, non équivalents → C-7, tués au rejeu. Relevé `ps` vide à chaque campagne.
5. **Documentation — conforme, une inexactitude corrigée (C-7).** FORMAT et paquet : aucune ligne neuve de plus de 120
   colonnes hors tableaux ; R-13 : 0 ; heures : seule `00:00 UTC` (cadence quotidienne). METRIQUES : trois lignes
   neuves de plus de 120 colonnes (deux titres de section, une ligne de C-5 à 121), sans correction.

### À former, observations

- **I-4 SHOGEN-S2BIS-TETES-JOURNAUX-LISTE-1** : la grammaire des noms de journal (`[a-z]{1,16}`) n'est pas une liste
  fermée : un observateur de la liste qui pose seize têtes de journaux inventés (`o2-ja.tete` …) évince encore la tête
  d'un autre observateur de la liste, au jeton comme à l'enregistrement `tetes` (mesuré : `o3` non lue). Résidu de la
  borne commune, hors de C-5 : liste fermée des journaux (`pool`, `carte`) ou borne par observateur.
- **I-5 SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1** : la carte porte désormais des relevés de Binance (remplaçants) : la
  carte descriptive du rendu (RB) doit les écarter ou les nommer comme remplaçants, non comme sources de la carte.
- Au versement, textes du rapport du générateur à reprendre : CONFIG-PRODUCTION-1 cite `test_carte_de_production_vide`,
  renommé `test_carte_de_production` par C-6 ; la limite « `capture --reprise` sans `O_NONBLOCK` » est fermée par C-4.
- Écart E-8 de la G2 : `git diff --name-only HEAD -- s2bis docs/adr-0029/s2bis .github/workflows/gates.yml` dans
  `outils/controles_suite.sh` (dossiers nommés, aucun emplacement interdit, sortie non affichée) ; E-1 non répété.

## Suite 2 : C-8

Gate 0 : `claude-opus-5-5`, même réviseur, distinct du générateur. Écrit le 2026-10-18 entre 07:59 et `08:45` UTC
(`date -u`). Brief : `BRIEF-G2-SUITE2.md` (sha256 `877e48cc403e10b69d1cb48a04b42e5c2798e1fcbbba8a68c1c1e95d9ba81904`) ;
lus entiers : `../BRIEF-GEL-CORR3.md` (`58f94c45ec4024609feddacec808a0738fb9fba6a030e99192624eae20e04937`),
`../diffs/C-8.diff` (`cbb16c6e4c1835a25af013ea555804127a4cfa75f6e15d712993c1bf7273232a`), section C-8 de
`../RAPPORT-GENERATEUR.md` (`8734607c9f81fc5c36a0b1c63859a4d2bd16e05641c0d4c5fd76fe90b943283e`) ; `../SHA256SUMS` OK.
Base relevée `1d7e5d485e78a8b3d3b713557de5cf236279f833`.

### Verdict : ACCEPTE-AVEC-CORRECTIONS (C-9)

- **C-9 — amende C-8** (`diffs/C-9.diff`, sha256 `f5466f5da5c13fc7f6a04919ad8a5fb43bfa1a415e22a9206614815cba9d2c7a`,
  contre l'arbre final des quinze diffs ; test seul, 8 lignes) : mutant T-01 vivant (filtre de `lire_tetes` sur
  `JOURNAUX[:1]` : une tête valide du journal `secondaire` serait refusée `TETES/journal`) : aucun cas n'avait de tête
  `secondaire` ; `test_journaux_inventes_n_evincent_rien` lit désormais `o3-secondaire.tete`, à l'enregistrement
  `tetes` comme au manifeste du jeton. Arbre final + C-9 : job vert (runner 153 ok, `Ran = 444`, plancher inchangé),
  matrice 3.10 à 3.13 verte ; T-01 tué au rejeu (`mutants/suite2-c9.*`).

### Checklist restreinte

1. **Série — conforme.** Quinze diffs appliqués dans l'ordre sur une extraction neuve (`preuves/suite2/apply-check.txt`) ;
   job vert à chaque état au plancher écrit, 433 … 443, 444 (`preuves/suite2/etats.txt`). Arbre final : S2 `Ran = 423`,
   sim-bis `Ran = 279` ; xtask : S-G1 à S-G8 VERT, fmt, no_std, clippy VERT, S-G9 seule
   `VIOLATION docs/17-modele-de-menace.md:70` (connue). Matrice : 3.10, 3.12, 3.13 vertes au premier passage ; 3.11 :
   un FAIL au premier passage, `test_secondaire.Isolement.test_carte_pendue_ou_refusee_le_pool_intact` (test à temps
   réel, w = 1 s : `b` lu `panne_transport` au lieu de `panne_http` à la troisième fenêtre), module non touché par le
   lot ; vert aux deux passages suivants et 8 fois sur 8 isolé (`matrice-3.11-passage1..3.txt`) ; matrice de C-9 verte.
   Fragilité préexistante : item I-7 ci-dessous.
2. **Éviction I-4 — fermée.** Seize têtes d'`o2` à des journaux inventés n'évincent plus `o3`, au jeton comme à
   l'enregistrement `tetes` (test du générateur, rouge sur C-7 : 3 FAIL et 1 FAIL du FORMAT,
   `preuves/suite2/C-8-rouge.txt`) ; refus `TETES/journal` borné à 16, reste aux `ignores` ; au plus huit têtes lues.
   R-25 : 45.
3. **Espion de `lier` dans `test_commande_jeton` — admis, sans correction.** La liaison réelle reste prouvée sur le
   chemin de `tetes.jeton` par `test_jeton_lie_a_la_requete` (refus `JETON/liaison` de quatre jetons non liés,
   conservation du jeton lié) et `test_jeton_du_jour_non_arme_puis_emis_une_fois` (jeton lié conservé avec la vraie
   `lier`) ; l'espion de la commande vérifie les arguments exacts (jeton, sha256 du manifeste écrit, nonce). Mesuré :
   T-03 (exception de `lier` avalée dans `jeton`) tué par `test_jeton_lie_a_la_requete` ; T-04 (nonce faux passé à
   `lier`) tué par l'espion et par les tests réels. Ce que l'espion retire : l'acceptation de bout en bout d'un jeton
   réel par la commande avec la liste, qui se déduit de ces deux preuves ; un jeton de test recalculé exigerait une clé
   de TSA de test nouvelle (celle des jetons actuels est détruite), sans gain de preuve.
4. **Rouges et mutants — conformes après C-9.** Mutants du générateur rejoués : 7 (C8-01, 03, 04, 06, 07, 08, 09),
   7 tués ; mutants de la G2 : T-01 vivant → C-9 ; T-02 (15 refus nommés), T-03, T-04 tués (`mutants/suite2.*`).
5. **Documentation — conforme.** FORMAT §16.4 et §16.5 exacts ; lignes ajoutées ≤ 120 colonnes ; R-13 : 0 ; aucune
   heure sans date.

### À former, observations

- **I-6** : SHOGEN-S2BIS-TETE-SECONDAIRE-1 (ANNEXE-B l.1348, déclencheur « intégration de P2 », passé) reste ouvert au
  gel : la tête du journal secondaire n'est ni exportée ni consignée, contre l'échange des têtes de l'ADR (l.235 à
  `e16956b`) ; son texte nomme le journal `carte` (`tetes.Depot(dossier, observateur, "carte")`), que `JOURNAUX`
  refuserait : le journal à exporter est `secondaire`. À adjuger avant le gel (il touche la boucle du secondaire).
- **I-7 SHOGEN-S2BIS-SECONDAIRE-ISOLEMENT-TEMPS-1** : `test_carte_pendue_ou_refusee_le_pool_intact` dépend du temps
  réel (w = 1 s) et a échoué une fois sur trois passages complets sous 3.11 : un faux rouge possible du job s2bis
  (`--egal`, aucun saut) ; à rendre déterministe (horloge injectée) ou à borner.
- Le test de C-8 lie `JOURNAUX` à `set(entree.FICHIERS)`, clés des commandes : même texte que les noms de journal, mais
  lien indirect (le nom du journal est écrit dans `construire` et `construire_secondaire`).

## Suite 3 : C-10, C-11, clôture

Gate 0 : `claude-opus-5-5`, même réviseur, distinct du générateur. Écrit le 2026-10-18 entre 09:49 et `10:35` UTC
(`date -u`). Brief : `BRIEF-G2-SUITE3.md` (sha256 `49c2b33b991e461590d7132a6f4771b4961a0c48ff19f294cc524376b579b3c8`) ;
lus entiers : `../BRIEF-GEL-CORR4.md` (`94c21128175e8dd47528ac321b7922c8fcde7db2366cfd269509a8f3c882f716`),
`../diffs/C-10.diff` (`7458664db7b1e49fadfccb6572d84923316626c5cf11846f12ae4f32d789fa46`), `../diffs/C-11.diff`
(`474b9245db55427d24cbdcb894033e9708e6ee5c80ac256e489cfd6dd72721a0`), sections C-10 et C-11 de
`../RAPPORT-GENERATEUR.md` (`f1de1392701ef2157be9861570e6fffeaabade7e75556e6982969d53a583d541`) ; `../SHA256SUMS` OK.
Base relevée `1d7e5d485e78a8b3d3b713557de5cf236279f833`.

### Verdict de clôture : ACCEPTE-AVEC-CORRECTIONS (C-12, mineure)

- **C-12 — amende C-10** (`diffs/C-12.diff`, sha256 `70172e7158fcfb80cf0c31c64ef4ee54f0d352334489f7751e5211303b52ccca`,
  contre l'arbre final des dix-huit diffs ; docstring de test et METRIQUES) : la docstring de
  `test_tete_du_secondaire_exportee_au_point` donnait une heure sans date (`m(1), 22:59`) : `m(1), 2026-10-04 22:59 UTC`
  (recompté : 1791154860 − 120 = 2026-10-04 22:59 UTC). Arbre final + C-12 : job vert (`Ran = 446`), module vert.
- Avec C-12, la G2 du lot GEL-COLLECTEUR-1 est close : série de dix-neuf diffs, ordre GEL-1, 2, 3, 4, 5, 7, 8, 6, 9,
  C-3, C-4, C-5, C-6, C-7, C-8, C-9, C-10, C-11, C-12 ; plancher final 446.

### Checklist restreinte

1. **Série — conforme.** Dix-huit diffs appliqués sur une extraction neuve (`preuves/suite3/apply-check.txt`) ; job
   vert à chaque état au plancher écrit, de 433 à 446 (`preuves/suite3/etats.txt`). Arbre final : S2 `Ran = 423`,
   sim-bis `Ran = 279` ; matrice 3.10, 3.11 (deux passages complets), 3.12, 3.13 : code 0, `Ran 446`, aucune ligne
   `Exception ignored` ni `Warning` ; xtask : S-G1 à S-G8 VERT, fmt, no_std, clippy VERT, S-G9 seule
   `VIOLATION docs/17-modele-de-menace.md:70` (connue).
2. **C-10 — conforme.** `<observateur>-secondaire.tete` est exportée au point de contrôle (seq du point, sha256 du
   `prec` suivant) et lue par `lire_tetes` sous la liste fermée (journal de `JOURNAUX`) ; aucun enregistrement `tetes`
   au journal secondaire ; `consigner` vaut vrai par défaut et le pool est inchangé (C10-08, défaut inversé, tué par
   les tests du pool) ; noms des temporaires d'export distincts entre les deux processus (`.<nom>.tmp`). Rouge des
   tests seuls sur C-9 : 1 FAIL et 1 ERROR, plus 1 FAIL du FORMAT (`preuves/suite3/C-10-rouge.txt`). R-25 : 60.
3. **C-11 — conforme.** Le test tourne en un processus, horloges, attentes et lectures injectées (`Temps`, `pendue`,
   lectures factices) : plus aucune dépendance au temps réel dans ce test ; la docstring et METRIQUES disent
   exactement ce qui n'est plus prouvé (séparation des processus du système d'exploitation, relevant du déploiement) et
   ce qui reste éprouvé en processus réel (`Conformite`). R-25 : 44.
4. **Mutants — conformes.** Rejoués du générateur : C10-01, 02, 03, 04, 06, 07, 08, C11-02, C11-03, C11-01b : 10 tués ;
   C11-01 (un seul site) vivant, comme au générateur, équivalent admis (la liste `abandons` est réassignée à chaque
   fenêtre : un partage par un seul site ne s'observe pas ; C11-01b, deux sites, tué). Mutants de la G2 sur C-10 :
   U-02 (dépôt créé sans `--depot`, sur `.`) tué ; U-01 (`fsync` non transmis au `Depot` du secondaire) vivant :
   équivalent pour le programme déployé (le point d'entrée n'est appelé qu'avec `os.fsync`, défaut de `Depot`) ; seule
   l'injection de test diffère : observation, sans correction (`mutants/suite3.*`, `mutants/suite3-c11b.*`).
5. **Documentation — conforme après C-12.** FORMAT §15.6 et §16.6 exacts ; lignes ajoutées au FORMAT ≤ 120 colonnes ;
   R-13 : 0 ; heure sans date : la seule, dans une docstring de test de C-10, corrigée par C-12 ; un titre METRIQUES de
   C-10 passe 120 colonnes (même forme que les titres précédents), sans correction.

### Items à former (hors du code de la série, ou préexistants)

| item | constat | qui | déclencheur | sortie | source |
|---|---|---|---|---|---|
| SHOGEN-S2BIS-TESTS-TEMPS-REEL-1 | `test_secondaire.Conformite` (sous-processus, w = 1 s, cinq fenêtres, `["ok"] * 5` attendu) et les tests de bout en bout du pool restent à temps réel : même classe que le faux rouge d'I-7 ; aucun échec mesuré sur une vingtaine de suites complètes | orch. | avant le sceau (le job `--egal` sans saut ne tolère pas un faux rouge) | marges mesurées sous charge, ou horloge injectée là où la preuve n'exige pas le processus réel [inféré] | G2 du lot GEL-COLLECTEUR-1, suite 3 |
| SHOGEN-S2BIS-ISOLEMENT-PROCESSUS-DEPLOI-1 | depuis C-11, aucun test ne fait tourner ensemble le pool et un secondaire pendu en processus séparés ; l'isolement des processus repose sur le déploiement (deux unités systemd, `MemoryMax`, ADR-0029 l.235 à `e16956b`) | orch. | DB-2 (mise en service) | un essai à la mise en service : secondaire pendu, pool à ses lectures, journal relevé [inféré] | G2 du lot GEL-COLLECTEUR-1, suite 3 ; rapport du générateur, C-11 |
| SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 | la carte porte les relevés des remplaçants de Binance (C-6) : la carte descriptive du rendu doit les écarter ou les nommer comme remplaçants | orch. | G0 de RB (carte descriptive) | un filtre nommé et un test au recalcul [inféré] | G2 du lot GEL-COLLECTEUR-1, suite 1 (I-5) |
| volet de SHOGEN-S2BIS-TSA-CERTIGNA-1 | `.armement` écrit l'URL armée en clair au dépôt ; la règle `tsa-https` refuse port et majuscules d'hôte | orch. | DB-3 | URL scellée sans secret (authentification hors de l'URL) ; règle relue sur l'URL de Certigna [inféré] | G2 du lot GEL-COLLECTEUR-1 (I-3) |

Items à fermer au versement (textes du rapport du générateur, relus) : SHOGEN-S2BIS-NOM-FORME-1,
SHOGEN-S2BIS-CAPTURE-PARTIELLE-1, SHOGEN-S2BIS-TEMOIN-BLOC-1, SHOGEN-S2BIS-OBSERVATEURS-LISTE-1,
SHOGEN-S2BIS-TETE-SECONDAIRE-1 (C-10) ; SHOGEN-S2BIS-CONFIG-PRODUCTION-1 en fermeture partielle (`resolv.conf` → DB-2,
URL de la TSA → DB-3) ; à former : SHOGEN-S2BIS-DNS-TEMOINS-RODAGE-1 (adjudication DNS) et les quatre lignes ci-dessus.
Hors de la série, aucun constat de la G2 ne reste sans item.

Écart E-9 de la G2 : le commentaire de tête de `outils/controles_suite3.sh` dit encore « rouge des tests de C-8 »
(copie du script de la suite 2) ; le script lance bien les tests de C-10 (`preuves/suite3/C-10-rouge.txt`).
