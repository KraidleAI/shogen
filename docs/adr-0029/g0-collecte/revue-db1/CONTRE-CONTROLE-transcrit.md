# Contre-contrôle neuf de DB-1 (R-1 à R-3 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:55:47 UTC du fichier db1/g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-CC — contre-contrôle neuf du sous-lot DB-1 de DEPLOI-BIS (série recalée DB1-a à DB1-q), 2026-10-10

- **Gate 0** : contre-contrôleur `claude-opus-5-5` (identifiant exact déclaré par l'environnement). Je n'ai ni écrit ni
  relu DB-1 avant ce contre-contrôle. Heures lues par `date -u` : ouverture 07:33:10 UTC, rédaction 08:39:22 UTC.
- **Brief** : `g2/cc/BRIEF-CC.md`, sha256 `e428f0ca912816254b3045e015db0adced5d13a9934d3d1cc41b2e9c8c82e148`, lu en entier.
- **Série** : `diffs-recales/DB1-a.diff` à `DB1-q.diff`, concaténation dans l'ordre recalculée
  `9f6522d87dea9c5dd8680bd4e7ff533f539806441c5a3a3ff29f99e5777a09c1`, égale à celle de la « Phase 3 » du rapport du
  générateur (§13.4) ; a à p `f775d0da…93b71` (§12.4) ; chacun des 17 sha256 égal au tableau du §12.4 et à DB1-q
  `eaf35fa9…bf27d` ; +818 −60 en tout, chaque diff ≤ 185 lignes ajoutées.
- **Base** : tête au début `2fcd30369e3c0bcdf2e3c80a197a4e09d713eb18` (DETTES-T6 DT6-g) ; DT6-a à g de la tête égaux à
  leurs diffs (`git patch-id --stable` sur les chemins de chaque diff) ; copie creuse (`git archive` avec exclusions,
  puis `tar -x --exclude`, `test -e` des dossiers interdits) ; DT6-h à w (concaténation `8661c7c5…`) puis DB1-a à q
  appliqués (`git apply --check` puis `git apply`, hors dépôt), cinq fichiers gardés à chacun des 18 états.
- **Tête à la fin** : `3876fe80a6ef145cec1a2cf047519ec4f662e243` (DETTES-T6 DT6-r, relevée à 08:42:00 UTC) : DT6-a à r
  égaux à leurs diffs (corps comparé sur les chemins nommés), DT6-s à w puis DB1-a à q s'y appliquent, et les 24
  chemins de DT6 et de DB-1 sont égaux octet pour octet à l'état vérifié ici (`preuves/tete-finale-2.txt` ; même
  constat sur `42d23d3`, DT6-q, à 08:37:19 UTC, `preuves/tete-finale.txt`). **La série s'applique sur la tête du
  moment, après DT6-s à w.**
- **Interdits** : aucune pièce de D.2, aucun `*.jsonl`, rien des dossiers interdits (copie creuse) ; sortie brute de
  `xtask` jamais lue (`outils/verdicts_xtask.py` n'en extrait que l'identifiant des sections, les lignes VERDICT et la
  seule référence `chemin:ligne` de S-G9) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -u` à chaque lancement) ;
  aucun réseau (suites sous `isole.sh`, sondes dans des espaces de noms neufs) ; aucun `sudo` ; aucune écriture git au
  dépôt. Écarts : §8.

## Verdict : CONFORME-AVEC-RÉSERVES (R-1, R-2, R-3)

C-1 à C-9 sont reprises à l'identique, justes, et leurs rouges se rejouent ; DB1-q admet exactement les blocs ed25519
bien formés ; le pare-feu n'ouvre que les flux de l'avis ; les planchers sont exacts aux 18 états ; toutes les lignes
de jobs sont vertes. Trois réserves, chacune avec sa forme exacte (`propose/R-n.diff`, à appliquer dans l'ordre après
DB1-q), éprouvées sur la série entière (rouge, vert, mutants, ligne du job s2bis : Ran = 374, plancher inchangé) :

| R-n | objet | fichiers (+/−) | sha256 |
|---|---|---|---|
| R-1 | `ADRESSE_SAUVEGARDE` : compte et hôte commencent par une lettre ou un chiffre (un hôte `--` passait le contrôle et remplissait l'ensemble `sauvegarde` des adresses de `/etc/hosts`, sortie 0) | script +2 −1, test +1 | `50204b62…cfbfb4ce` |
| R-2 | test de la clé : les 64 valeurs du 26e caractère, sur un bloc portant « + » et « / » (trois mutants vivants : `[A-PR]`, `[A-HJ-P]`, « / » refusé) | test +15 −1 | `efffd758…abcd1338c` |
| R-3 | pare-feu : `drop` explicite en dernière règle des trois chaînes de base (un rechargement par `nft -f` laissait passer des paquets interdits : 48 à 81 par série de 60 à 100 rechargements ; 0 avec `drop`) | `nftables.conf` +3, script +3, test +3 −3 | `ed6df86d…71fed2c32` |

Concaténation R-1, R-2, R-3 : `d57a3d97235844eb8b6992a92fa9ccb5c38b769be11b6982edd5b166bd5919e2`. Aucune ligne ajoutée
au-delà de 120 caractères, aucune barre oblique inverse, aucun blanc final ; script rempli après R-3 : 13 282 octets.

## 1. C-1 à C-9 (DB1-h à DB1-p) : copies, justesse, rouges, lecture du script

- **Copies** : DB1-h, i, l, m, n, o, p identiques à C-1, C-2, C-5 à C-9 (`cmp`) ; DB1-j et DB1-k diffèrent de C-3 et
  C-4 dans la seule section `gates.yml` (plancher 371→372 et 372→373 au lieu de 355→356 et 356→357, bloc `@@ -288` au
  lieu de `@@ -284`, lignes `index`) ; leurs sections script et test sont identiques (comparaison par section,
  `outils/sections.py`). Concaténation C-1 à C-9 : `d33a3c68…7a7c4`, conforme à l'adjudication.
- **Rouges puis verts** (`outils/rouges.py`, module `test_deploi`, python3.12, isolé ; `preuves/rouges.txt`) : tests de
  chaque état sur le code de l'état précédent. C-1 et C-2 : verts (texte ; garde non éprouvable par la suite, L-6).
  C-3 : 1 échec (`test_tdp1_temporaires_nes_0600`) ; C-4 : 2 (`test_tdp1_relance_rien_sous_le_compte_d_intervention`) ;
  C-5 : 5 (`test_tdp1_parametre_refuse_rien_ne_change`) ; C-6 : 4 (`test_tdp1_essai_quatre_observateurs`) ; DB1-q : 8
  (`test_tdp1_cle_bloc_ed25519_exact`). Corrections de tests seuls, par **mes** mutants, vivants avant et tués après :
  C-7 `n1` (règle de premier niveau `add rule inet shogen entree tcp dport 23 accept`, deux copies) et `n2` (ensemble
  `resolveurs` prérempli de `0.0.0.0/0`) ; C-8 `o1` (`umask 002`) ; C-9 `p1` (`debian.sources` de l'image désactivé
  lui aussi). Tous les verts conformes, aucune erreur.
- **Justesse, une ligne par correction** :
  - C-1 : la phrase est vraie (la garde de « / » se relit l.26-28 : vide, « / », « // »).
  - C-2 : `[ -n "$R" ] && ! [ "$R" -ef / ]` ferme la racine vide (`cd` en échec) et « // » ; **preuve hors suite**
    (`outils/chroot_c2.sh`, chroot sur un tmpfs d'un espace de montage privé, `/usr` de l'hôte en lecture seule,
    `essai.getent` à la racine du chroot ; `preuves/chroot-c2.txt`) : script de l'état h, `--essai //` et
    `--essai /absente` : code 0, huit fichiers et `essai.commandes` écrits sur la racine, `sources.list` désactivé ;
    état i : code 2, `ESSAI/racine refusée`, rien d'écrit. Hôte inchangé (`/essai.getent`, `/etc/shogen`,
    `/etc/nftables.d`, `/home/intervention` absents avant et après).
  - C-3 : `rm -f` puis `(umask 077 && cat > …)` : chaque temporaire naît 0600, même sur un reste 0644.
  - C-4 : compte présent, message nommé et retour avant toute écriture sous son dossier ; conséquence (rotation de la clé
    par la console) déjà écrite par l'adjudication ; un sous-cas s'y ajoute (L-4).
  - C-5 : octet 0 à 255 sans zéro de tête ; valeurs à deux lignes refusées ; bloc de la clé serré par DB1-q (§2).
  - C-6 : `enable --now` des minuteries ; `reload-or-restart` : rechargement en une transaction, mesuré au §3 (R-3).
  - C-7, C-8, C-9 : tests justes (premier niveau et ensembles exacts ; dossiers 0755 ; image Debian 13).
- **Lecture intégrale de l'état final** (script 258 lignes, 12 940 octets ; `nftables.conf` 54 lignes, 1 875 octets) :
  - *Second lancement* (`outils/essai_cc.py`, `preuves/essai-relance-liens.txt`) : même racine, comptes présents,
    `sources.list` recréé par le fournisseur : code 0, sortie d'erreur réduite à `premier-demarrage : COMPTES/intervention
    présent, clé inchangée`, sortie standard identique, tous les fichiers identiques (sha256, modes) sauf
    `sources.list.disabled` (le fichier recréé) ; journal = celui du premier lancement moins les deux `useradd` et le
    `chown -R` ; aucun `.nouveau` restant.
  - *Liens posés d'avance* aux chemins écrits (`etc/nftables.conf`, `debian.sources`, `00-shogen.conf`) et aux
    temporaires (`observateur.conf.nouveau`, `shogen-observateur.nft.nouveau`), cibles hors de la racine : liens
    remplacés par des fichiers ou retirés, cibles intactes (contenu et 0644).
  - *Droits posés* : 0644 (`debian.sources`, `00-shogen.conf`, `90shogen-securite`, `nftables.conf`,
    `shogen-observateur.nft`), 0640 (`observateur.conf`, root:shogen journalisé), 0600 (`authorized_keys`), 0700
    (`.ssh`), 0755 (dossiers créés).
  - *Paramètres hostiles* : formes fermées tenues (guillemet, `$`, accent grave, retour à la ligne exclus), **sauf** un
    tiret en tête de l'hôte de `ADRESSE_SAUVEGARDE`, seul paramètre passé en argument d'une commande (`getent ahostsv4
    "$1"`). Mesuré sur la fonction `adresses()` recopiée à l'octet : `--` rend les adresses de `/etc/hosts` (code 0,
    admises) ; `--help`, `--usage`, `--version`, `-V`, `--he` rendent le texte d'aide de getent, admis comme adresses,
    que `nft -c` refuse (code 1, non nommé) après l'écriture des fichiers du pare-feu ; une liste d'adresses passe
    `nft -c` (code 0). → **R-1**.
  - *Mode d'essai* : enregistreurs `apt-get`, `systemctl`, `useradd`, `chown`, `nft`, `sshd` ; `getent` lit
    `essai.getent` ; toute écriture porte le préfixe `$R` (`ecrire`, `mv` des sources, `mkdir` et `install` du compte,
    journal) ; garde C-2.

## 2. DB1-q : le motif admet exactement les clés ed25519 bien formées

- **Par position** : un bloc de 51 octets s'écrit en 68 caractères base64 sans remplissage (51 = 17 × 3), six bits par
  caractère : les chaînes de 68 caractères de l'alphabet et les blocs de 51 octets se correspondent un à un. Octets 0 à
  17 fixes (`00 00 00 0b`, « ssh-ed25519 », `00 00 00`) : caractères 1 à 24 `AAAAC3NzaC1lZDI1NTE5AAAA` ; caractère 25 :
  six bits hauts de l'octet 18 (`0x20` → `001000` → `I`) ; caractère 26 : deux bits bas de l'octet 18 (nuls pour la
  longueur 32) puis quatre bits du premier octet de clé, soit `A` à `P` exactement (`Q` à `/` donnent les longueurs 33
  à 35) ; caractères 27 à 68 : les 252 bits restants de la clé, libres. Le motif
  `^ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI[A-P][A-Za-z0-9+/]{42}( [A-Za-z0-9@._-]+)?$` (l.51 et 53, `LC_ALL=C` posé
  l.22) décrit donc exactement « longueur 11, ssh-ed25519, longueur 32, 32 octets », plus un commentaire d'un mot.
- **Par décodage** (`outils/cle_ed25519.py`, motif lu dans le script et exécuté par bash, attendus par `base64` de
  Python, indépendants du motif ; `preuves/cle-ed25519.txt`) : en-tête recalculé sur les 19 octets fixes ; 3 × 64
  valeurs du 26e caractère : accord 192 sur 192, admises `A` à `P` ; `Q` décode 33 ; 3 000 clés au hasard, 4 aux bords
  (nulle, pleine, `F0 00…`, `0F FF…`) et 200 avec commentaire : 3 204 admises, toutes bien formées ; 20 formes fausses
  refusées (longueurs 31 et 33, 33 annoncé pour 32 octets, blocs de 67, 69 et 72 caractères, `=`, types `ssh-ed25518`
  et `ssh-rsa` dans le bloc, préfixe `ssh-rsa`, deux espaces, tabulation, espace en tête, commentaire de deux mots ou
  avec `=`, retour chariot, espace finale, option en tête, majuscules, base64url).
- **Refus nommé** : `PARAMETRE/CLE_INTERVENTION`, code 2, rien d'écrit (test de DB1-q, 8 caractères ; R-2 : les 48).
- **Trou du test** : les mutants `K15` (`[A-PR]` : longueur 33 admise), `K16` (`[A-HJ-P]` : une clé vraie sur 16
  refusée) et `K17` (« / » refusé dans les 42 derniers : environ 48 % des clés tirées au hasard [calc]) restent vivants
  sous la ligne du job ; aucune clé admise du test ne porte « / » dans ses 42 derniers caractères. → **R-2**.

## 3. Pare-feu

- **Structure** (`nftables.conf` et copie embarquée, égales) : table `inet`, trois chaînes de base `policy drop`
  (input, output, forward) ; boucle locale admise ; `meta nfproto ipv6 drop` en deuxième règle d'entrée et de sortie ;
  `established,related` admis, `invalid` jeté. Sortant : TCP/443 vers tout ; UDP/53 vers les trois témoins ; UDP et
  TCP/53 vers `@resolveurs` ; UDP/123 et TCP/4460 vers `@ntp` ; TCP/23 vers `@sauvegarde` ; UDP 68→67 ; TCP/80 vers
  169.254.169.254 pour `skuid 0`. Entrant : TCP/22, UDP 67→68. Conforme mot pour mot à l'avis (Q-3) et au G0 (DB1-g, 4).
- **`nft -c` et `nft -f`** (nft 1.0.9 de l'hôte, espace réseau neuf, `/etc` sur un tmpfs d'un espace de montage privé ;
  `outils/sonde.sh`, `preuves/sonde.txt`) sur les jeux produits par l'essai : o1 à o4 code 0 ; ensembles chargés : o1
  `0.0.0.0/0`, o2 Quad9, o3 Google, o4 les adresses collées, `ntp` quatre, `sauvegarde` une ; doublons (deux serveurs NTP
  de même adresse, deux résolveurs collés égaux) : code 0, dédoublonnés.
- **Sonde sur le fil** (`outils/sonde.py`, à moi : tun `t0`, route de lien, envois par uid 0 et 65534 observés sur
  `t0`, entrées forgées à sommes de contrôle justes ; attendus écrits depuis l'avis, pas depuis le jeu) : sans jeu,
  37 envois sur 37 passent et 14 entrées sur 14 sont admises (la sonde voit) ; avec les jeux o1, o2, o3, o4 : **0 écart**
  (37 envois et 14 entrées chacun, dont réponse d'un flux 443 admise et SYN-ACK sans SYN jeté).
- **IPv6** : non sondable (noyau de l'hôte sans IPv6 : `Address family not supported by protocol`) ; refus établi par
  la structure, le test et le mutant `K14` (L-1).
- **`reload-or-restart` sans vidage** : unité de l'hôte (Ubuntu 24.04, nftables 1.0.9-1ubuntu0.1, sha256 `e040269f…`)
  [lu] : `ExecReload=/usr/sbin/nft -f /etc/nftables.conf`, `ExecStop=/usr/sbin/nft flush ruleset` ; celle de trixie
  [abs]. Fichier fautif (`flush ruleset` en tête, règle invalide en fin) : `nft -f` code 1, jeu inchangé (tout ou
  rien). Envoi interdit continu (uid 65534 vers 10.9.0.1:9999) pendant des rechargements (`outils/recharge.py`,
  `preuves/recharge.txt`, `sonde.txt`) : *restart* (vidage puis chargement) 351 346 paquets passés sur 60 cycles et
  570 654 sur 100 ; *reload* du fichier déployé 48 sur 60, 69 et 81 sur 100 ; **même fichier avec un `drop` en fin de
  chaque chaîne : 0 et 0 sur 100** ; fichier de R-3 produit par le script : 0 sur 60, 0 et 0 sur 100. C-6 supprime
  l'essentiel (environ 7 000 fois moins de paquets passés), pas tout : la politique des chaînes recréées par la transaction ne tient
  pas pendant toute la validation [inféré, L-3]. → **R-3**.

## 4. Recalage : plancher exact à chaque état

Ligne du job s2bis lue dans le `gates.yml` de chaque état, exécutée comme la forge (`bash --noprofile --norc -eo
pipefail`), python3 = python3.12, isolée (`outils/jobs_etats.sh`, `preuves/jobs-etats.txt`, 07:44:12 à 07:57:45 UTC) :
code 0, `conforme`, aucun saut, **Ran = plancher** aux 18 états.

| état | 0 | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plancher = Ran | 358 | 358 | 362 | 365 | 367 | 369 | 371 | 371 | 371 | 371 | 372 | 373 | 373 | 373 | 373 | 373 | 373 | 374 |

## 5. Rejeu sur l'état final (tête 2fcd303 + DT6-h à w + DB1-a à q)

Sous `isole.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL -u HTTPS_PROXY … -u no_proxy`, python3 = python3.12 (image
ubuntu-24.04), blocs `run:` lus dans `gates.yml` (`outils/gates_finales.sh`, `preuves/gates/`, 08:26:55 à 08:34:06 UTC).

| gate | résultat |
|---|---|
| runner `run-fixtures-verdict-suite-s2.py` (premier pas des jobs unittest) | 137 ok, 0 échec |
| job s2bis | conforme, aucun saut, Ran = 374 |
| job S2 | conforme, sauts nommant la variable, Ran = 419 |
| job sim-bis (`GIT_DIR` du dépôt, lecture seule, E-9) | conforme, Ran = 279 |
| job calib-actifs ; job controle | conforme, Ran = 65 ; conforme, Ran = 37 |
| job g1 : `runners-epingles` ; `workflows-yaml` (cas, arbre) ; cas du lint ; lint ; `journaux-modele` ; `docs-sha256sums` | conforme (7 workflows) ; 16 ok sur 16, conforme (PyYAML 6.0.1) ; 227 ok ; OK (7 fichiers) ; conforme ; conforme (40 SHA256SUMS, 319 lignes, 11 absentes admises, 4 non listés) |
| job g5 : cas du hook ; R-13 (motif lu dans `gates.yml`, `git grep --no-index` sur les quatre fichiers de DB-1, `gates.yml` exclu comme au job) | 57 ok, 0 échec ; code 1, 0 ligne |
| matrice s2bis, python3.10, 3.11, 3.12, 3.13, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` | 4 × conforme, Ran = 374, 0 avertissement |
| `cargo --locked xtask verify` (lignes VERDICT seules) | S-G1 à S-G8 et S-G7a VERT (0 violation) ; S-G9 ROUGE, 1 violation `docs/17-modele-de-menace.md:70` ; global ROUGE, code 1 ; **verdicts identiques à l'état 0 (sans DB-1)** : effet de la copie creuse, non de la série |
| `cargo --locked test`, cible par défaut de la copie (`arbre/target`, règle I-1) | code 0 ; 28 lignes `test result: ok` ; 269 passés, 0 échec, 0 ignoré ; cible supprimée ensuite |

## 6. Mes mutants (ligne du job s2bis, état final)

`outils/mutants_cc.py` (07:59:49 à 08:13:39 UTC ; `preuves/mutants.txt`, `preuves/mutants/`) ; classement par la sortie du
vérificateur : 1 avec `FAILED (` et Ran = 374 : tué ; 0 : vivant ; autre : FATAL. Fichiers remis à l'état final après
chaque mutant (`cmp`). **18 mutants : 14 tués, 4 vivants, 0 FATAL.**

| id | mutation | issue (test qui tue) |
|---|---|---|
| K1 | garde : `essai.getent` non exigé | tué (`test_tdp1_usage_et_racine_refusees`) |
| K2 | garde : `! [ "$R" -ef / ]` remplacé par `[ "$R" != / ]` | **vivant par construction** (L-6 ; prouvé hors suite, §1) |
| K3 | `.ssh` en 0750 | tué (`test_tdp1_parametres_gardes_et_cle`) |
| K4 | `observateur.conf` en 0644 | tué (`test_tdp1_parametres_gardes_et_cle`) |
| K5 | temporaire né 0640 (`umask 027`) | tué (`test_tdp1_temporaires_nes_0600`) |
| K6 | relance : message `COMPTES/…` sur la sortie standard | tué (`test_tdp1_relance_rien_sous_le_compte_d_intervention`) |
| K7 | refus `PARAMETRE/CLE` au lieu de `CLE_INTERVENTION` | tué (deux tests de refus) |
| K8 | `APT/trousseau` en code 2 | tué (`test_tdp1_sources_https_et_trousseau`) |
| K9 | `PARE-FEU/resolution` sans accent | tué (`test_tdp2_nom_non_resolu_refuse`) |
| K10 | entrée TCP/22 et 2222 (deux copies) | tué (`test_tdp2_regles_exactes`) |
| K11 | métadonnées pour tout uid (deux copies) | tué (`test_tdp2_regles_exactes`) |
| K12 | copie embarquée seule : sortie TCP/80 ouverte | tué (`test_tdp2_commun_embarque_et_ensembles`) |
| K13 | transit en `policy accept` (deux copies) | tué (`test_tdp2_refus_par_defaut_ipv4_et_ipv6`) |
| K14 | IPv6 jeté après `established` (entrée, deux copies) | tué (deux tests T-DP-2) |
| K15 | clé : 26e caractère `[A-PR]` | **vivant** → R-2 (tué sous R-2 : `c='R', longueur=33`) |
| K16 | clé : 26e caractère `[A-HJ-P]` | **vivant** → R-2 (tué sous R-2 : `c='I', longueur=32`) |
| K17 | clé : « / » retiré des 42 derniers | **vivant** → R-2 (tué sous R-2 : 16 échecs) |
| K20 | mode d'essai : enregistreur `sshd` retiré | tué (dix tests) |

Équivalents : aucun mutant sémantiquement équivalent ; K2 seul est non tuable par construction (garde de « / », que la
suite ne peut pas éprouver sans écrire sur la racine de l'hôte), déclaré. Autres mutants tués : `n1`, `n2`, `o1`, `p1`
(§1) ; `r1-hote`, `r1-compte`, `r3-sortie`, `r3-embarque` (§7).

## 7. Réserves (forme exacte : `propose/R-n.diff`, dans l'ordre R-1, R-2, R-3 après DB1-q)

- **R-1 — `ADRESSE_SAUVEGARDE`, tiret en tête refusé.** Script l.63 : `^[a-z0-9-]+@[a-z0-9.-]+$` devient
  `^[a-z0-9][a-z0-9-]*@[a-z0-9][a-z0-9.-]*$`, une ligne de commentaire au-dessus ; test des refus : `u1@--`, `u1@--help`,
  `-u1@h`. Le compte est fermé du même trait : DB-4 le passera à ssh et rsync. Rouge (tests de R-1 sur le code de q) :
  3 échecs ; vert ; mutants `r1-hote` (hôte rouvert : 2 échecs) et `r1-compte` (1 échec) tués
  (`preuves/reserves-rouges.txt`).
- **R-2 — test de la clé : les 64 valeurs du 26e caractère.** Image sans trousseau : admise exactement si la longueur
  décodée vaut 32 (sortie `premier-demarrage : étape sources`, code 3, `APT/trousseau`, rien d'écrit), refus nommé
  sinon (code 2) ; bloc `…I<c>+` puis 41 « / ». Attendus calculés par décodage, jamais lus dans le script ; `import
  string` ; sous-tests seulement, plancher inchangé. Vert ; K15, K16, K17 vivants sous les tests de R-1, tués sous ceux
  de R-2. Coût : module de 3,2 à 4,0 s.
- **R-3 — `drop` explicite en fin de chaque chaîne de base**, dans `nftables.conf` et la copie embarquée (commentaire :
  `refus explicite, tenu aussi pendant un rechargement (nft -f)`) ; listes `ENTREE`, `SORTIE` et transit du test. Rouge
  (tests de R-3 sur le code d'avant) : 1 échec (`test_tdp2_regles_exactes`) ; vert ; mutants `r3-sortie` (drop retiré,
  deux copies : 1 échec) et `r3-embarque` (copie embarquée seule : 5 échecs) tués (`preuves/reserve-r3-rouges.txt`).
  Jeu commun produit par le script = `nftables.conf` de R-3 ; `nft -c` code 0 (o1 à o4, doublon) ; sonde : 0 écart
  (o1 à o4, mêmes flux) ; rechargements : 0 paquet passé (`preuves/recharge-r3.txt`, `sonde-r3.txt`). Le G0 reste vrai
  (« refus par défaut ») ; aucun ajout daté requis.
- **Sur la série entière avec R-1 à R-3** : ligne du job s2bis : conforme, Ran = 374 ; module `test_deploi` sous 3.10 à
  3.13 en `-X dev -W error` : OK, 16 tests, 0 avertissement (`preuves/reserves/`).

## 8. Écarts du contre-contrôleur

- **E-1** Une commande `bash -c` (sonde de getent, sans `rm`) refusée par le contrôle de sûreté du harnais : relancée
  sans `bash -c`, sur la fonction `adresses()` recopiée dans un fichier.
- **E-2** Un `rm -f $A/$f` (remise de l'état 0 pour le témoin xtask) refusé par le même contrôle, rien d'exécuté :
  réécrit `"${A:?}"/"${f:?}"`, forme proposée par le contrôle.
- **E-3** Barres obliques inverses tapées dans des commandes : échappements Python (retour à la ligne, apostrophe) dans
  des documents en ligne de retouche de mes outils, une tabulation échappée dans une mesure (rien d'écrit), des motifs
  `grep` de contrôle, un `printf` de liste dont la sortie n'est pas apparue. Octets écrits contrôlés : 0 octet 92 dans
  mes outils, mes diffs et ce rapport ; la première version de `copie.sh` (six continuations) réécrite avant tout
  lancement.
- **E-4** Fautes de mes outils, refaites, rien de compté : `sonde.py` (route : `EINVAL`, puis port 40001 réutilisé
  d'un lancement à l'autre ; résultats pris au troisième lancement) ; `cle_ed25519.py` (extraction des lignes du motif) ;
  `cargo_cc.sh` affichait `$?` après une substitution de commande (codes affichés 0) : codes relevés par relance
  (`xtask` 1, `cargo test` 0).
- **E-5** Première version de `tete_finale.sh` : les diffs DT6-l à r, v et w n'ont pas d'en-tête `diff --git` ; liste de
  chemins vide, d'où un `git diff` du commit `d3d897b` sans chemins nommés et un `git diff --numstat` qui a affiché ses
  deux chemins (`s2bis/…`, aucun contenu) ; faux « différent ». Outil refait (chemins lus sur `---`/`+++`, corps
  comparé) : 17 commits égaux.
- **E-6** Deux recherches par motif non récursives dans le code de ma copie (`scripts/sim-bis/*.py` pour `archive`,
  `xtask/src/*.rs` pour `VERDICT`) ; rien sous `docs/`.
- **E-7** `SHA256SUMS` du dossier : liste de mes seuls sous-dossiers (`outils`, `preuves`, `propose`) et fichiers nommés.
- **E-8** Écriture hors du dossier : `cargo` a mis à jour `/root/.cargo/.global-cache` (08:34:20 UTC), propre à cargo.
- **E-9** Job g5 : ses cas créent des dépôts jetables (commits réels) sous mon TMPDIR, jamais dans le dépôt ; job
  sim-bis : `GIT_DIR=/home/user/shogen/.git`, `GIT_OPTIONAL_LOCKS=0`, pour le seul `git archive` des fichiers épinglés
  des oracles (lecture seule).
- **E-10** Charge sur 1 min à 5,18 pendant la campagne de mutants (autres chaînes ; 3,3 au lancement) ; aucun run
  interrompu ni FATAL.

## 9. Limites rendues (règle PAROXYSME)

- **L-1** IPv6 non sondable sur cet hôte : sonde IPv6 du smoke de DB-2 (déjà à l'adjudication).
- **L-2** Outils de l'hôte (nft 1.0.9, unité Ubuntu, noyau 6.18.44) au lieu de ceux de trixie : `systemctl cat
  nftables.service` au smoke de DB-2 ; avec R-3, le refus ne dépend plus du moment où la politique prend effet.
- **L-3** Mécanisme de la fenêtre du rechargement inféré (politique `drop` des chaînes recréées appliquée en fin de
  validation, après le retrait des anciennes) : code du noyau non relu en session ; seul l'effet est mesuré. Une
  connexion entrante admise dans la fenêtre resterait admise ensuite (`established`) [inféré].
- **L-4** Sous-cas de C-4 : un premier lancement interrompu entre `useradd intervention` et la pose de la clé laisse
  un compte sans clé ; la relance répond `COMPTES/intervention présent, clé inchangée`. Remède : la console, comme
  pour la rotation ; à écrire dans la procédure de DB-6.
- **L-5** `FOURNISSEUR` et `REGION` admettent aussi un tiret en tête ; DB-1 ne les passe à aucune commande (ils ne vont
  qu'à `observateur.conf`). Pour les briefs de DB-2 à DB-5 : tout paramètre passé en argument se ferme en tête
  alphanumérique ou suit `--`.
- **L-6** Garde de « / » non éprouvable par la suite (K2) ; éprouvée hors suite (chroot, §1).
- **L-7** Clés TEST 1 et TEST 3 de la RFC 8032 : relues par l'orchestrateur (adjudication), pas par moi [2nd] ; la
  preuve du §2 n'en dépend pas (tout bloc de 32 octets est admis).

## 10. Journal de provenance (G1)

- **Lu [lu]** : `BRIEF-CC.md` (`e428f0ca`) ; `../../ADJUDICATION.md` (`1d7d29ce`, quatre ajouts datés) ;
  `../RAPPORT-G2.md` (`9accc4c5`) ; `../corrections/C-1.diff` à `C-9.diff` ; `../../RAPPORT-GENERATEUR.md` §12 et §13
  (`2935acb1`) ; `../../AVIS.md` (`c9eb967b`) ; `../../BRIEF-DB1.md` (`1413926f`) ; G0 `G0-COLLECTE-RECALC-DEPLOI.md`
  à l'état final (`08c1e6b0`, l.20-100, ajouts datés de DB-1) ; les 17 diffs ; script, `nftables.conf` et `test_deploi.py`
  de l'état final en entier ; `gates.yml` (jobs g5, g1, S2, s2bis, sim-bis, calib-actifs, controle) ;
  `verdict-suite-s2.py` (`main`) ; `s2bis/tests/__init__.py` ; `run-fixtures-hooks.sh` (en-tête) ; `oracle_r1.py`
  (`extraire`) et `parametres.json` (épingles) de sim-bis ; `xtask/src/rapport.rs` et `lib.rs` (format, code de
  sortie) ; unité `nftables.service` de l'hôte ; `isole.sh` (`ebaa1c78`) et `lo_up.py` (`b532be4b`).
- **Calculé [calc]** : empreintes (série, diffs, corrections, DT6, réserves) ; blocs ed25519 (Python `base64`,
  `struct`) ; 1 − (63/64)^42 = 0,4839 ; comptes de lignes des diffs (`git apply --numstat`, `outils/forme_diffs.py`).
- **Inféré [inféré]** : mécanisme de la fenêtre du rechargement (L-3) ; unité et noyau de trixie (L-2) ; usage d'un
  compte de sauvegarde par ssh et rsync à DB-4 (R-1).
- **Seconde main [2nd]** : vecteurs de la RFC 8032 (L-7). Aucun autre chiffre repris sans recompte.
- **Commandes** (outils dans `outils/`, sorties dans `preuves/`) : `copie.sh`, `etats.sh`, `jobs_etats.sh`, `sections.py`,
  `rouges.py`, `cle_ed25519.py`, `essai_cc.py`, `produire.py`, `sonde.sh` et `sonde.py`, `recharge.sh` et `recharge.py`,
  `chroot_c2.sh`, `mutants_cc.py`, `propose.py`, `propose_r3.py`, `verif_r.py`, `verif_r3.py`, `forme_diffs.py`,
  `gates_finales.sh`, `run_job.py`, `cargo_cc.sh`, `verdicts_xtask.py`, `diffs_util.py`, `tete_finale.sh` ; `git
  rev-parse`, `git log` (sujets), `git diff` et `git patch-id` bornés aux chemins des diffs (sauf E-5) ; `nft -c`,
  `nft -f`, `unshare -m -n`, `chroot` ; `df -h /` et charge relevés avant chaque campagne (6,8 à 7,4 Go libres, jamais sous 3).
