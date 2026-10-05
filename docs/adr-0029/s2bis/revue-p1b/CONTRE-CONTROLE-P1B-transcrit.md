# Contre-contrôle des corrections de la tranche B (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 02:55:27 UTC du rapport rendu par message par le réviseur G2 (agent a89713614f46e2240 ; le harnais a refusé le fichier de rapport) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

# Contre-contrôle des corrections de la tranche B (CB-11c à CB-11g) de la G2 de P1-B, et des citations RFC

**Verdict : ACCEPTE-AVEC-CORRECTIONS.** C-1 à C-7, O-5 et O-7 sont tous corrigés : je l'ai vérifié moi-même, tests et mutants rejoués par la commande du job. Il ne reste que deux retouches de texte (citations RFC), CC-1 et CC-2, pour le diff CB-11h (§6).

- **Gate 0** : je tourne sous `claude-opus-5-5` (identifiant exact donné par le harnais). L'effort `max` ne s'observe pas de l'intérieur.
- **Horloge** (`date -u`) : début le 2026-10-05 à 02:14:44 UTC, fin à 02:53:35 UTC.
- **Dépôt** : tête `784ebd2` au début et à la fin, `git status` vide. Aucune opération git en écriture.
- **Rapport par message** : le harnais interdit les fichiers de rapport. `CONTRE-CONTROLE-P1B.md` n'est donc pas écrit ; ses pièces sont dans `…/p1b/g2/travail/`.
- **Pièces vérifiées** :
  - `corr/SHA256SUMS` : `e67dae39…2edc`, égal à l'annoncé, 111 lignes, toutes OK ;
  - `rebase-784ebd2/SHA256SUMS` : toutes les lignes OK ;
  - rapport du worker transcrit : `5820dd8b…0830` ;
  - brief des corrections : `c2a0572b…e2c3`.

## 1. Recalage et états

- **Recalage** (`outils/compare_rebase.py`, `d2bb59d8…`) : pour les 13 diffs recalés, comparés aux originaux, les sections hors `gates.yml` sont égales à l'octet près, ligne `index` exclue. Dans `gates.yml`, les lignes retirées et ajoutées sont identiques (seule la ligne `--plancher` change). Seuls le contexte et `index` diffèrent. **Recalage conforme.**
- **Précision à ta note** : entre `6535821` et `784ebd2`, le runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` a aussi changé (cas K-03 ajouté). Les diffs ne le touchent pas, mais le runner compte désormais **33** cas, contre 32 dans le rapport du worker sur `6535821`.
- **Arbres comparés** :
  - A = `6535821` + 8 diffs originaux + 5 diffs de correction : égal au `final/` du worker sur `s2bis/`, sur `docs/adr-0029/s2bis/` et sur `gates.yml` (`diff -r`).
  - B = `784ebd2` + 13 diffs recalés : égal à A sur `s2bis/` et sur les documents.
- **Tailles** (lignes de code ajoutées, `git apply --numstat`) : 162, 107, 143, 69 et 87, toutes ≤ 200.
- **États sur `784ebd2`**, ligne du job lancée telle qu'écrite, en réseau isolé :

  | état | plancher | Ran | verdict | runner |
  |---|---|---|---|---|
  | après CB-11b | 92 | 92 | conforme | 33 ok |
  | après CB-11c | 97 | 97 | conforme | 33 ok |
  | après CB-11d | 101 | 101 | conforme | 33 ok |
  | après CB-11e | 106 | 106 | conforme | 33 ok |
  | après CB-11f | 111 | 111 | conforme | 33 ok |
  | après CB-11g | 114 | 114 | conforme | 33 ok |

- **Rouge sur l'état précédent** (code de l'état k−1, tests de l'état k) :

  | diff | tests en échec | détail |
  |---|---|---|
  | CB-11c | 3 | 2 échecs, 1 erreur |
  | CB-11d | 6 | 4 échecs, 2 erreurs |
  | CB-11e | 17 | 4 échecs, 13 erreurs |
  | CB-11f | 8 | 3 échecs, 5 erreurs |
  | CB-11g | 1 | 1 échec |

  Ces nombres sont égaux à ceux du worker. Les tests en échec sont bien ceux qui visent C-1, O-5, C-5, O-7, C-4, C-2 et C-3.

## 2. Chaque correction : corrigée ou non

Toutes les sondes ont été rejouées sur l'arbre B.

- **C-1, échéance exacte : corrigé.**
  - Sonde S-B1 : la forme `b` sort maintenant `panne_transport` avec fin − E = 0,0 ms. Avant la correction, elle sortait `ok` avec +50,2 ms.
  - FORMAT §11.4 est aligné : `fin` = E.
  - Mutants MC-01 (règle `fin` > E retirée), MC-02 (phases postérieures à E gardées) et MC-03 (`fin` pris à l'instant du classement) : tous tués.
- **C-2, DNS : corrigé.**
  - S-D1 (écho de la requête sans bit QR) et S-D2 (autre question) donnent maintenant `reponse` ; avant, `forme`.
  - S-D7 (« 127.1 »), S-D8 (`None`) et S-D9 (« localhost ») donnent `forme`, sans exception.
  - Crochet d'audit : **aucun événement socket** pour ces adresses, ni création, ni résolution, ni envoi. Le témoin `127.0.0.1` lève bien `socket.__new__` puis `socket.sendto`.
  - Mutants MC-08, MC-09, R-MG-17 et R-MG-21 : tous tués.
- **C-3, TLS : corrigé.**
  - Avec mon outil, la ClientHello envoyée en boucle locale porte la même liste d'extensions que celle d'urllib, sous Python 3.10 à 3.13 : `[0, 11, 10, 35, 16, 22, 23, 49, 13, 43, 45, 51, 21]`.
  - Poignée réelle avec une AC de test (clés détruites après usage) :
    - serveur qui propose `h2` et `http/1.1` : `ok`, `http/1.1` négocié ;
    - serveur sans ALPN : `ok` ;
    - certificat d'un autre nom : `tls` ;
    - `CONTEXTE` face à une AC inconnue : `tls` ;
    - `CONTEXTE` porte bien CERT_REQUIRED, le contrôle du nom d'hôte et `post_handshake_auth`.
  - Mutants MG-01, MG-02, MG-03, MC-10 et MC-11 : tous tués.
- **C-4, horloge : corrigé.** SHOGEN-S2BIS-HORLOGE-RECUL-JOURNAL-1 est fermé, avec un cas résiduel suivi par SOMMEIL-MURAL-1 (§4).
  - S-C1 et S-C2 : avec un recul de 2 s, la durée réelle reste 1,00 s ; avant, 3,00 s.
  - Un recul de 180 s entre deux fenêtres se lit dans `horloges` : `{murale : 60 s, monotone : 240 s}`.
  - Mutants MC-06, MC-07, MC-14 et R-MG-23 : tous tués.
- **C-5, sondes bornées : corrigé.**
  - S-B2 : fils vivants 9, 9, 9, 9 ; avant, 9, 12, 15, 18.
  - `fils.sondes` = 3 ; les sondes pendues valent null ; l'échéance est tenue (4 marqueurs en 8,8 s).
  - Mutants MC-04 et MC-05 : tués.
- **C-6, tests de la boucle bornés en temps : corrigé.** M-LP-3, lancé par la commande du job, sort en **1 en 78,9 s**. Avant, il faisait pendre la suite au-delà de 200 s (FATAL).
- **C-7, vivants à tuer : corrigé.**
  - Tués tels quels : MG-11, MG-13, MG-18, MG-19, MG-24, MG-26, MG-29 et MG-31.
  - Tués sous forme réécrite : MG-21 et MG-23.
  - MG-22 reste vivant, équivalent en pratique, comme déjà adjugé.
- **O-5 : corrigé.** MC-12 et M-5-03 sont tués ; le test de BaseException passe.
- **O-7 : corrigé.** MC-13 est tué ; la `sante` est complète, champs nuls, quand la boucle n'a pas de sondes.

**Campagnes, toutes par la commande du job.**
- Lanceur : `outils/campagne_job_g2.py` (`7fb3f3b8…`), écrit par moi et indépendant de celui du worker.
- Contrat : ligne du job lue dans `gates.yml`, python3.12, réseau isolé, borne de 300 s, groupe de processus tué à la borne. Sortie 1 = tué, 0 = vivant, tout le reste = FATAL.

| jeu | mutants | tués | vivants | inapplicables (texte changé) |
|---|---|---|---|---|
| `mutants_g2.py` | 30 | 24 | 1 (MG-22) | 5 |
| `mutants_g2_b.py` | 1 | 1 | 0 | 0 |
| M-LP du worker (`mutants-final-cb5.py`, via mon adaptateur) | 14 | 11 | 0 | 3 |
| `mutants_cc.py` (à moi : 8 réécritures R-…, 14 mutants des corrections MC-…) | 22 | 22 | 0 | 0 |

Aucun mutant n'a dépassé la borne. Incident de ma part : le premier lancement des M-LP a échoué dans mon outil (fichier du worker au format à 7 champs) avant tout run. Je l'ai relancé par l'adaptateur et je n'ai rien compté du lancement raté.

## 3. Tes adjudications des écarts du worker

- **E-1** : d'accord, avec l'item à CB-18. Les sondes sont bornées à 2 s sur l'horloge monotone et finissent vers D + 2 s, alors que l'échéance tombe à D + 19 s. Précision pour l'item : `joindre` relève `disque` et `empreinte` avant de lire l'état des futurs, si bien que l'intervalle entre E et le relevé des sondes contient deux entrées-sorties.
- **E-2** : d'accord.
- **E-3** : d'accord.
- **E-4** : d'accord. Je propose de rattacher cette limite à SOMMEIL-MURAL-1 : un départ monotone porté dans `suivi` la lèverait.
- **E-5** : d'accord. La ClientHello mesurée est égale sous 3.10 à 3.13.
- **E-6** : vérifié. J'ai réécrit moi-même les huit mutants : ce sont les mêmes remplacements, donc la même mutation. Les huit sont tués.
- **E-7, E-8** : notés. Mes rejeux sur l'arbre final recalé couvrent leur champ.
- **E-9** : consigné. C'est le même cas que mon E-R4.
- **E-10** : vérifié pour `essai_hello.py` par crochet d'audit, avec 0 événement socket. Pour les essais `ipaddress` et la gate des secrets, l'absence de socket est seulement [inféré] : je ne les ai pas rejoués sous audit.

## 4. Items proposés par le worker

**SHOGEN-S2BIS-SOMMEIL-MURAL-1 : mesure reproduite**, avec ma sonde `sonde_sommeil_mural_cc.py` (`848e4a9b…`) et avec celle du worker.

| essai | moment du recul | départ en avance de | `horloges` à la fenêtre suivante |
|---|---|---|---|
| ma sonde, recul de 1,5 s | pendant le premier sommeil | −1 499 726 µs | égales |
| ma sonde, recul de 1,5 s | entre deux relevés | −1 499 804 µs | `{murale : 0,5 s, monotone : 2,0 s}` |
| sonde du worker, réglages par défaut | pendant le premier sommeil | −999 810 µs | égales |

Conséquence : un recul survenu avant le premier relevé d'une exécution ne se voit que par un `retard_max` négatif. Je propose que la règle de validité du recalcul (RB) lise les deux champs, `retard_max` négatif et `horloges`. Déclencheur au G0 de CB-18 : d'accord.

**O-10 en item** : d'accord.

**Citations RFC : vérifiées par moi** sur les fichiers .txt, empreintes notées : `rfc1035` `d14ae809…`, `rfc8446` `47871bc8…`, `rfc7301` `ba122aee…`.
- (a) RFC 1035 :
  - §4.1 (l.1351) ne traite que du format des messages ;
  - §4.1.1 décrit l'identifiant, « used by the requester to match up replies to outstanding queries » (l.1423-1426), et le bit QR (l.1428).
  - Dans l'arbre final, la seule occurrence mal placée est le FORMAT §12, l.271.
  - La docstring de `dns.py` (« format RFC 1035 (§4.1) ») est juste.
  - Je l'avais manquée dans ma G2, alors que la citation était déjà dans CB-10b.
- (b) RFC 8446 : `post_handshake_auth(49)` figure à la l.1941, dans le §4.2 (qui commence l.1911). Le §4.2.6 (l.2583) ne dit que « zero length » (l.2593-2594).

## 5. Gates sur la copie complète B (`784ebd2` et les 13 diffs)

- Python 3.10 à 3.13 en `-X dev -W error` : 114 tests OK, 0 avertissement, 0 exception ignorée.
- Ligne du job sous les quatre versions : conforme, Ran = 114.
- Runner : 33 cas OK. Hooks : 54 cas OK.
- Suite S2 : 405 tests, OK (skipped=2), conforme.
- Secrets, en mode indexé et `--tree` : OK, 14 fichiers.
- R-13 : 0 marqueur. Le motif est octet pour octet celui du job (même sha256) ; il est lancé sur les seuls fichiers du lot.
- `xtask` : S-G1 à S-G8 vertes ; fmt, no_std et clippy verts ; S-G9 rouge sur `docs/17-modele-de-menace.md:70` seulement (défaut connu des copies, que la série ne touche pas).

## 6. Liste fermée, pour un diff CB-11h (texte seul)

- **CC-1** : dans le FORMAT §12, dernier paragraphe (l.271), mettre « RFC 1035 §4.1.1-4.1.2 » après la phrase d'appariement (identifiant, QR, une seule question, la même). Après la phrase sur l'IPv4 littérale, ne garder que « ADR-0029 l.109 ».
- **CC-2** : dans `s2bis/tests/test_http_reseau.py`, l.228-229 (docstring de `test_contexte_tls_d_urllib`), écrire « RFC 8446 §4.2 (numéro 49), §4.2.6 (données vides) ».
- Facultatif, hors liste : RFC 7301 « §3.1 (syntaxe), §6 (identifiant) » (l.141-158 et l.374).
- Le plancher reste à 114. Après le diff, relancer R-13, secrets et la ligne du job.

## 7. Journal de provenance (G1)

**Lectures [lu]** :
- les 5 diffs de correction en entier ; les 13 diffs recalés, comparés par script ;
- brief et rapport des corrections ;
- outils du worker : `campagne_job.py`, `mutants_reecrits.py` ;
- essais du worker : `essai_hello.py`, `essai_backlog.py`, `sonde_sommeil_mural*.py`, et leurs preuves ;
- `RFC-CITATIONS.md` du lecteur ;
- lignes citées des RFC : 1035 l.1351-1432, 1530-1545, 1634-1654 ; 8446 l.1911, 1925-1946, 2583-2596 ; 7301 l.141-160, 368-376 ;
- `http.client` : 3.10.20 l.1441-1448 et 3.12.3 l.824-835. Ces lignes sont exactes, comme le cite la docstring de `http.py`.

**Commandes et sorties** : `travail/preuves/cc-*`, indexées par `SHA256SUMS-contre-controle` (`9b32c9fe…6abd`, 63 lignes). Les outils et sondes de ma G2 sont inchangés (vérifiés contre `SHA256SUMS-reviseur`). Aucun chiffre de seconde main.

**Exposition** :
- Aucun dossier interdit ouvert, aucun `*.jsonl` réel, aucune pièce de D.2.
- Recherches non récursives sur `docs/` : `grep -n` sur des fichiers uniques, `grep -rn` sur `s2bis/` de ma seule copie. `git diff --stat` n'a affiché que des noms de fichiers.
- Tous les lancements sous `unshare -n`.
- Incident : une commande `rm` combinée a été bloquée par le contrôle de sécurité du harnais ; rien n'a tourné. Je l'ai refaite avec des chemins littéraux.

**Nettoyage** : copies lourdes et cible cargo supprimées. `travail/` pèse 1,4 Mo ; disque à 77 %.

Fichiers utiles, dans `<scratchpad>/s2bis/p1b/g2/travail/` :
- `SHA256SUMS-contre-controle`
- `outils/mutants_cc.py`
- `outils/campagne_job_g2.py`
- `preuves/cc-mutants-g2.txt`
- `preuves/cc-mutants-mlp.txt`
- `preuves/cc-mutants-cc.txt`
- `preuves/cc-gates.txt`
- `preuves/cc-sommeil-mural.txt`