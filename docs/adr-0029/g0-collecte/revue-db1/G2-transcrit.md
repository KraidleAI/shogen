# Relecture G2 neuve de DB-1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:55:47 UTC du fichier db1/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-G2 — relecture G2 neuve du sous-lot DB-1 de DEPLOI-BIS (2026-10-10, heures lues par `date -u`)

- **Gate 0** : réviseur `claude-opus-5-5` (identifiant exact déclaré par l'environnement ; préfixe attendu conforme). Ni
  générateur ni relecteur antérieur de DB-1.
- **Brief** : `g2/BRIEF-G2.md`, sha256 `1992b975ebe985c7daf477a73b191e82f30c0b39092674d6a09d7a1e133a1fe0` (conforme).
- **Série relue** : `diffs/DB1-a` à `DB1-g`, empreinte de la concaténation dans l'ordre recalculée
  `160dddd5c23d71058d10efd08e46521921b91aaa18faec190e32b383cfa8c441` (conforme) ; base
  `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` = tête du dépôt au début (`git rev-parse`, arbre propre) ; la série s'y
  applique (`git apply --check` puis `git apply`, hors dépôt) et redonne les blobs annoncés (G0 `772f1af`, script
  `c23fd04`, `nftables.conf` `86f3178`, tests `5c3aefe`). Tête relue à 06:04 UTC : `6e648a8` (DETTES-T14) ; `gates.yml`,
  le G0 de DEPLOI, `s2bis/` et `verdict-suite-s2.py` y sont inchangés (`git diff --quiet dda4bbc 6e648a8`) : série et
  corrections s'y appliquent telles quelles.
- **Interdits** : aucune pièce de D.2, aucun `*.jsonl`, rien des dossiers interdits (copie éparse `git archive dda4bbc |
  tar -x` avec les exclusions du brief, contrôle par `test -e`) ; aucun réseau (suites sous `isole.sh`, sondes dans des
  espaces réseau neufs) ; aucun `sudo` ; aucune écriture hors de `g2/` ; aucune écriture git au dépôt (index local au
  dossier, sans commit) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -u` à chaque lancement) ; de `xtask`, lignes
  VERDICT seules. Écarts : §8.

## Verdict : ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-9

Corrections à appliquer dans l'ordre après DB1-g (`corrections/C-1.diff` à `C-9.diff`, éprouvées sur la série :
`git apply --check` puis `git apply` sur la copie a à g, égalité octet pour octet avec l'état corrigé, suites vertes) :

| C-n | objet | fichiers (lignes +/−) | sha256 du diff |
|---|---|---|---|
| C-1 | **DB1-h (L-6)** : ligne de docstring adoptée | test_deploi.py +2 −1 | `6a38fa33…69335` |
| C-2 | garde de la racine d'essai : refus de la racine vide et de « // » | script +2 −1 | `0449a28a…54b40` |
| C-3 | `ecrire` : le temporaire naît 0600 (adresse secrète d'`observateur.conf`) ; test | gates.yml +1 −1, script +3 −2, tests +27 −3 | `f8253b51…67a47` |
| C-4 | relance : root n'écrit plus sous le dossier du compte `intervention` ; refus nommé ; test | gates.yml +1 −1, script +4 −1, tests +25 | `06b4575b…c8ae8b7e` |
| C-5 | formes fermées : octet IPv4 0-255 sans zéro de tête ; clé ed25519 exacte ; cas hostiles au test | script +5 −2, tests +5 | `27c19ec3…bfa3e4b` |
| C-6 | `systemctl enable --now` des minuteries APT ; `reload-or-restart` de nftables | script +2 −2, tests +4 −3 | `d0abb046…4c16d1` |
| C-7 | test T-DP-2 : rien hors des blocs attendus (premier niveau et ensembles exacts) | tests +26 −20 | `1ade99b4…bd4419` |
| C-8 | test : dossiers créés (`etc/shogen`, `etc/nftables.d`) en 0755 | tests +3 −2 | `fcb5f794…7bfa95` |
| C-9 | test des sources : image Debian 13 (`debian.sources` de l'image, `.sources` du fournisseur) | tests +9 −2 | `2e7b8437…53c854a` |

Empreinte de la série C-1 à C-9 (concaténation dans l'ordre) :
`d33a3c68737decead40ead21f63c0cd857a0dacd4aeb7521693608cc4277a7c4`.
**Plancher** : C-3 et C-4 ajoutent chacun un test (355 → 356 → 357) ; delta total de DB-1 corrigé : **+15** sur la base
(342 → 357), soit, sur la tête qui portera DETTES-T6 (358 attendu), 362 … 371 pour DB1-b à DB1-g, puis 372 (C-3) et 373
(C-4). Aucune ligne ajoutée au-delà de 120 caractères, aucune barre oblique inverse, aucun blanc final, aucun marqueur
TODO/FIXME (contrôle sur les octets des diffs ; motif R-13 de `gates.yml` passé sur l'index local : code 1).

## 1. Script et pare-feu (point 1 du brief) : exigences, lecture intégrale

Lecture du script entier (état g, 248 lignes, 11 850 octets) et de `nftables.conf` (54 lignes), en attaquant (paramètre
hostile, relance, liens posés par un compte, lecture concurrente) et en opérateur pressé (paramètre vide, chemin faux,
second lancement). Numéros de ligne : script à l'état g.

| exigence (forme de l'avis et de DB1-g) | code | preuve | état |
|---|---|---|---|
| E-D-01 : huit paramètres en tête, vides au dépôt, contrôlés avant tout changement, refus `PARAMETRE/<nom>` (sortie 2) | l.11-18, 44-59, 235 | `test_tdp1_parametre_refuse_rien_ne_change` (journal vide, image intacte) ; `rempli` exige `K=""` une fois | tenue, **sauf deux formes** : `010.1.1.1` passe le contrôle et nft le lit `8.1.1.1` (octal) ; `256.1.1.1` passe et n'échoue qu'à `nft -c`, après six étapes ; une clé `ssh-ed25519` de bloc faux (longueur, type) passe → **C-5** |
| E-D-01 / Q-6 : `observateur.conf` 0640 root:shogen, sans la clé | l.107-118 | `test_tdp1_parametres_gardes_et_cle` | tenue à l'état final ; le temporaire `.nouveau` naît **0644** (umask 022) avec l'adresse secrète, et le reste si le lancement est interrompu → **C-3** |
| E-D-03 / Q-1 : `shogen` système sans shell ; `intervention` sans droit d'administration, clé seule | l.97-105 | journal exact, modes | tenue au premier lancement ; **à la relance**, root suit les liens que le compte a pu poser sous son dossier → **C-4** |
| E-D-03 / T-DP-5 : `00-shogen.conf`, huit directives, `sshd -t` puis rechargement | l.120-134 | `test_tdp5_sshd_cle_seule` (lignes exactes), journal | tenue (configuration effective : `sshd -T` au smoke, L-2 du générateur) |
| E-D-04 / Q-2 : source unique HTTPS, autres sources désactivées, trousseau `.pgp` sinon `.gpg`, arrêt sans | l.68-88 | `test_tdp1_sources_https_et_trousseau` | tenue ; image du test sans `debian.sources` (présent sur Debian 13) ni `.sources` de fournisseur : deux mutants vivants → **C-9** |
| E-D-04 / décision 1 : paquets, `--no-install-recommends`, `unbound` pour la famille unbound seule | l.90-95 | journal exact | tenue |
| E-D-12 / T-DP-9 : sécurité seule (`#clear` puis `trixie-security`), sans redémarrage | l.136-148 | `test_tdp9_securite_seule_sans_redemarrage` | politique tenue ; les minuteries sont *activées* sans être *lancées* (`enable` sans `--now`) : livrées arrêtées par une image, rien ne tourne avant un redémarrage → **C-6** |
| E-D-05 / T-DP-2 réécrit / Q-D-07 / décision 3 | l.150-232 ; `nftables.conf` | T-DP-2, `nft -c`, sonde (§2) | tenue ; à une relance, `restart` exécute `ExecStop=nft flush ruleset` avant de recharger : jeu vide un instant → **C-6** ; trous de test (règle de premier niveau, ensembles) → **C-7** |
| Décision 5 : rempli ≤ 32 KiB, lancement à la main par root | l.39-42 ; taille | `test_decision5_taille` ; mesure | tenue : 11 850 octets (12 803 après C-1 à C-9 ; 13 879 rempli au pire, valeurs de 200 caractères et quatre adresses de 15) |

**Points éprouvés sans constat** :
- *Injection* : toutes les formes fermées excluent guillemet, `$`, accent grave, barre oblique inverse et retour à la
  ligne (ancrage `^…$` sans `REG_NEWLINE`) ; ni `observateur.conf` (`CLE="valeur"`, relu par les sous-lots suivants) ni
  `authorized_keys` (aucune option possible avant `ssh-ed25519`, commentaire d'un seul mot) ne peuvent recevoir une ligne
  ou une option de plus ; refus constatés pour une valeur à deux lignes de **chacun** des huit paramètres et pour les
  espaces (cas ajoutés par C-5). Une valeur portant `"` ou `$(…)` collée dans le script agit au collage, avant le script :
  hors de sa portée (acte de l'investisseur).
- *Ordre* : paramètres, puis sources, paquets, comptes, observateur, ssh, mises à jour, pare-feu ; point d'entrée de DB-2
  (horloge, résolveur) avant le pare-feu ; aucun changement avant le contrôle des paramètres.
- *Refus nommés* : `PARAMETRE/<nom>` (2), `ESSAI/racine` (2), usage (2), `APT/trousseau` (3), `PARE-FEU/résolution` (3) ;
  rien d'écrit avant chacun (tests, journal vide, fichiers inchangés).
- *Relance* : second lancement sur la même racine factice (comptes présents, `sources.list` recréé par le fournisseur) :
  sortie 0, fichiers identiques au premier lancement (sha256), à l'état g comme à l'état corrigé ; à l'état corrigé,
  message nommé `COMPTES/intervention présent, clé inchangée` et rien sous le dossier du compte.
- *Droits posés* : `debian.sources`, `00-shogen.conf`, `90shogen-securite`, `nftables.conf`, `shogen-observateur.nft`
  0644 root ; `observateur.conf` 0640 root:shogen ; `.ssh` 0700 et `authorized_keys` 0600 au compte `intervention` ;
  dossiers créés 0755 (umask 022 du script ; épinglé par C-8).
- *Forme adoptée, non changée* : le compte `intervention` possède son `authorized_keys` ; un agent porteur d'une clé
  déléguée (E-D-17 (c)) peut donc y ajouter ou retirer des clés, la console du fournisseur restant le recours de
  l'investisseur. C'est la forme de Q-1 et de DB1-g (1) ; la variante `AuthorizedKeysFile` sous `/etc`, tenue par root,
  changerait l'ajout daté : non proposée.

## 2. Pare-feu (point 2)

- **Jeu commun** : refus par défaut en entrée, sortie et transit (`inet`, `policy drop`) ; boucle locale admise ; IPv6
  jeté en deuxième règle des deux chaînes ; `established,related` admis, `invalid` jeté ; sortant : TCP/443 vers tout,
  UDP/53 vers les trois témoins (198.41.0.4, 192.36.148.17, 193.0.14.129 : ADR-0029 l.109 relue), UDP et TCP/53 vers
  `resolveurs`, UDP/123 et TCP/4460 vers `ntp`, TCP/23 vers `sauvegarde`, UDP 68→67, TCP/80 vers 169.254.169.254 pour
  `skuid 0` ; entrant : TCP/22 et UDP 67→68. Quad9 et Google : adresses de l.82 relues. Rien d'autre.
- **`nft -c`** (nft 1.0.9 de l'hôte) sur les jeux produits par l'essai (commun + ensembles d'observateur) pour o1, o2,
  o4 : conformes. **Inclusion réelle** : `nft -c -f /etc/nftables.conf` puis `nft -f` dans un espace de montage privé où
  `/etc` est un tmpfs (hôte inchangé : `/etc/nftables.d` absent avant et après) : conformes, ensembles chargés égaux aux
  attendus (o1 `0.0.0.0/0` ; o2 Quad9 ; o4 adresses collées ; `ntp` quatre adresses ; `sauvegarde` une).
- **Sonde sur le fil** (outil propre, `outils/sonde_g2.py` : espace réseau neuf, tun `t0`, route par défaut par netlink,
  paquets forgés en entrée, envois par uid 0 et 65534 en sortie ; aucune adresse jointe) : sans jeu, 26 envois passent et
  9 entrées sont admises ; avec les jeux o1, o2, o4, ne passent que les flux listés ci-dessus (TCP/53 vers un témoin et
  `1.1.1.1` jetés hors o1, admis pour o1 ; 8.8.8.8 jeté pour o2 ; NTP et sauvegarde vers une autre adresse jetés ; TCP/22
  et UDP/443 sortants jetés ; DHCP depuis un autre port que 68 jeté ; métadonnées jetées pour uid 65534) ; en entrée,
  seuls TCP/22 et UDP 67→68 sont admis (TCP/23, 80, 443, UDP 53→68, 67→69, 123 et l'écho ICMP jetés). 140 lignes,
  aucune incohérence (`preuves/sonde-g2.txt`).
- **IPv6** : non sondable (noyau de l'hôte sans IPv6 : ni `/proc/net/if_inet6` ni `/proc/sys/net/ipv6`) ; refus établi
  par la structure, les tests et les mutants `o-f04` et `e03`/`f04` du générateur (L-1 du générateur, smoke de DB-2).
- **Doublons** : un même élément deux fois dans `ntp` ou `resolveurs` passe `nft -c` (rc 0) : la concaténation par nom
  sans dédoublonnage entre noms est sans effet.

## 3. Mode d'essai (point 3)

- Enregistreurs : `apt-get`, `systemctl`, `useradd`, `chown`, `nft`, `sshd` (fonctions ; journal `essai.commandes`) ;
  `getent` lit `essai.getent` ; tous les chemins écrits portent le préfixe `$R`. Hors essai : root et aucun argument.
- **L'essai ne touche pas l'hôte** : lancé (états g et h, o1 à o4) dans un espace de montage privé où `/` est remonté en
  lecture seule, seules la racine factice et un dossier de sortie restant en écriture (`/tmp` est sur `/`) : sortie 0,
  « fin », huit fichiers écrits sous la racine, aucune erreur d'écriture ; toute écriture ailleurs aurait échoué.
- **Garde de racine** : elle refuse « / » et exige `essai.getent` à la racine donnée. Le refus explicite de « / » ne
  couvre ni la racine **vide** (`cd` en échec : `R=""`, puis `[ -f /essai.getent ]`) ni « **//** » (`pwd -P` rend `//`).
  Les deux contournements se ramènent à un `/essai.getent` présent sur l'hôte : absent ici (contrôlé avant et après), et
  le test des refus utilise le script non rempli, dont le contrôle des paramètres arrête tout. Démonstration sans toucher
  l'hôte (`outils/chroot_garde.sh` : chroot sur un tmpfs d'un espace de montage privé, `/usr` de l'hôte en lecture seule,
  `/essai.getent` posé dans le chroot) : script g en essai sur `/absente` et sur `//` → l'essai écrit sur « / »
  (`etc/apt`, `etc/shogen/observateur.conf`, `etc/ssh/sshd_config.d/00-shogen.conf`, `home/intervention/.ssh`) et désactive
  `sources.list` ; script corrigé (C-2) → `ESSAI/racine refusée`, sortie 2, rien d'écrit (`preuves/c2-garde-chroot.txt`).
  La garde ne peut pas être éprouvée par la suite (L-6) : C-1 le dit dans le test.

## 4. Tests et mutants (point 4)

- **Rouge reproduit** (tests de chaque état sur le code de l'état précédent, module seul, python3.12, isolé) : b 20 échecs
  d'assertion (4 tests), c 8, d 6, e 2, f 10 ; aucune erreur ; chaque test nouveau d'un état est rouge (conforme au
  rapport du générateur).
- **Plancher exact à chaque état** (ligne du job s2bis de l'état, python3.12 comme l'image, `--aucun-saut --egal`) :
  0 342, a 342, b 346, c 349, d 351, e 353, f 355, g 355 ; états corrigés : C-1 355, C-2 355, C-3 356, C-4 à C-9 357 ;
  chaque fois Ran = plancher, verdict conforme (`preuves/job-*.txt`, `job-corr-C-n.txt`).
- **Mutants obligatoires** (PROPOSITION §4.4, et IPv6 par l'avis), formes du générateur reposées sur g : 7 tués, chacun
  par le test qu'il vise : `c01` (étape omise : essai, paramètres gardés), `f02` (sortant ouvert : refus par défaut),
  `f03` (témoin oublié : règles exactes), `f04` (IPv6 admis : les deux tests T-DP-2), `d03` (mot de passe : T-DP-5),
  `d09` (redémarrage : T-DP-9), `b13` (borne retirée : décision 5).
- **Campagne g, mutants du réviseur** (21, état g, ligne du job) : **11 tués** — `g10` (`chown -R` du dossier entier),
  `g11` (`AuthenticationMethods any`), `g12` (témoin élargi à un /24), `g13` (métadonnées /16), `g14` (entrées
  nouvelles admises), `g15` (DHCP de tout port), `g16` (`ahosts`), `g21` (refus sur la sortie standard), `g22` (journal
  écrasé), `g24` (`apt-get update` retiré), `g25` (`PermitEmptyPasswords` retiré) ; **9 vivants, trous de tests** —
  `g01`, `g02`, `g03` (pare-feu hors des chaînes : C-7), `g05` (umask 000 : C-8), `g06`, `g07`, `g20` (valeurs à deux
  lignes : C-5), `g17`, `g18` (sources de l'image : C-9) ; **1 vivant par construction** — `g23` (refus de « / » retiré :
  L-6).
- **Campagne h, mutants du réviseur sur l'état corrigé** (19 ; le commentaire de C-7 était alors dans sa première
  forme, texte seul) : les 9 vivants de g sont **tués** (`g06h` : même mutation sur la forme corrigée de la clé) ;
  mutants des corrections **tués** : `h-c3a`, `h-c3b`, `h-c4a`, `h-c4b`, `h-c5a`, `h-c5b`, `h-c5c`, `h-c6a`, `h-c6b` ;
  `h-c2` (garde revenue à `!= /`) vivant par construction (L-6). Complément (2, état corrigé) : `h-s1` (erreur de
  syntaxe : `test_tdp1_syntaxe` et les essais) et `h-s2` (racine admise sans `essai.getent` :
  `test_tdp1_usage_et_racine_refusees`) tués : chaque test de la série a un mutant qui le rougit.
- **Bilan** : 31 mutants du réviseur tués par la ligne du job s2bis (11 + 18 + 2), 7 mutants obligatoires tués ; 0 FATAL
  (classement par la sortie du vérificateur : 1 tué, 0 vivant, autre FATAL) ; fichiers rendus octet pour octet (sha256)
  après chaque mutant. **Équivalents** : aucun mutant sémantiquement équivalent ; deux non tuables par construction
  (`g23`, `h-c2` : la garde de « / » se relit dans le script, L-6, C-1), déclarés.

## 5. G0 : DB1-a et DB1-g (point 5)

- **Ajouts seulement** : DB1-a et DB1-g n'ont aucune ligne retirée ; leurs blocs suivent la dernière ligne existante ; le
  texte validé est inchangé (contexte des blocs identique au fichier de `dda4bbc`, blob `fcda662`).
- **Dates** : DB1-a `04:06:47 UTC` = `tmp/g0/date-ecriture.txt` (écrit à 04:06:47.098) et date de `DB1-a.diff`
  (04:06:47.113) ; DB1-g `04:39:03 UTC` = `tmp/g0/date-ecriture-g.txt` (04:39:03.339) et `DB1-g.diff` (04:39:03.356) ;
  journal `../NOTES.md` l.82 et l.106-107 conformes. Heure lue juste avant l'unique écriture : forme des ajouts antérieurs.
- **DB1-a contre les décisions 1 à 10** (`ADJUDICATION-DB0.md`, relue phrase par phrase) : chaque décision est rendue sans
  ajout ni retrait de sens (rattachements E-D-04, E-D-12, E-D-15, E-D-16, E-D-05, Q-D-07, Q-D-06, E-D-20, A-3, E-D-21,
  Q-D-10, Q-D-03, Q-D-02 ; items de la décision 9 ; écart du lecteur et consigne `GNUPGHOME`).
- **DB1-g contre le code** (points 1 à 6, relus contre DB1-b à DB1-f) : chaque phrase est vraie sur le code, avec une
  réserve sur (1) : « chacun est contrôlé avant le premier changement, refus et arrêt sinon » pour « une à quatre
  adresses IPv4 » et une clé « `ssh-ed25519` » ; sur la série seule, `256.1.1.1`, `010.1.1.1` et un bloc de clé faux
  passent ce contrôle (§1). Après C-5 la phrase est vraie ; aucun texte du G0 n'est à changer. (5) « activé et relancé »
  reste vrai après C-6 (`reload-or-restart`). Les écarts de lettre corrigés par le générateur (clé hors
  d'`observateur.conf`, boucle locale avant IPv6, résolution par `getent`, famille et non identité, rang de lecture
  constaté au smoke) sont exacts sur le code.

## 6. Gates (point 6)

Copie finale : `git archive dda4bbc` éparse + DB1-a à DB1-g ; état corrigé : la même + C-1 à C-9. Lignes de `gates.yml`
de chaque copie, `python3` lancé en `python3.12` (version de l'image), sous `isole.sh` et `env -u
SHOGEN_S2_CAMPAGNE_CONTROL -u HTTPS_PROXY … -u no_proxy` ; une commande lourde à la fois (`outils/gates_finales.sh`,
`matrice.sh`, `cargo.sh` ; sorties `travail/preuves/gates-*`, `matrice-*`, `cargo-*`, `xtask-*`).

| gate | copie finale (a à g) | état corrigé (C-1 à C-9) |
|---|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | 137 ok, 0 échec | 137 ok, 0 échec |
| job s2bis (`--aucun-saut --egal`) | conforme, Ran = 355 | conforme, Ran = 357 |
| job S2 (`--egal`) | conforme, Ran = 419 (sauts nommant la variable) | non touché par les corrections |
| job sim-bis | conforme, Ran = 279 (E-4) | non touché |
| job calib-actifs | conforme, Ran = 65 | non touché |
| job controle | conforme, Ran = 37 | non touché |
| matrice s2bis, python3.10 à 3.13, `-X dev -W error` (et `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | 4 × conforme, Ran = 355, 0 avertissement | 4 × conforme, Ran = 357, 0 avertissement |
| `docs-sha256sums.py` | conforme (39 SHA256SUMS, 314 lignes, 11 absentes admises) | idem |
| `workflows-yaml.py` et ses cas (PyYAML 6.0.1 du système) | conforme (7 workflows) ; 16 cas ok | idem |
| `runners-epingles.py`, `lint-model-pinning.sh`, `journaux-modele.py` | conformes | conformes |
| secrets (`gate-secrets.sh`, index local des 5 fichiers) | — | OK, 5 fichiers |
| R-13 (motif du job `g5-dette`, index local) | — | code 1 (aucun marqueur) |
| `cargo --locked xtask verify` (lignes VERDICT seules, cible partagée) | S-G1 à S-G8 VERT (0 violation) ; S-G9 ROUGE, 1 violation : `docs/17-modele-de-menace.md:70` ; verdicts identiques à ceux de la base `dda4bbc` (témoin) | identiques à la base |
| `cargo --locked test`, cible par défaut de la copie (`arbre/target`, règle I-1) | 28 lignes `test result: ok` ; 269 passed, 0 failed, 0 ignored | — |

S-G9 rouge par l'éparsité de la copie (la cible citée à cette ligne est dans un dossier interdit, absent), non par la
série : même violation sur la base. Gate 0 de l'environnement Rust : cargo 1.97.1.

## 7. L-6 : forme exacte de DB1-h (point 7)

Une ligne ajoutée à la docstring de `test_tdp1_usage_et_racine_refusees` (guillemets fermants déplacés) ; c'est C-1 :

```
        """Script non rempli : hors du mode d'essai, le refus des paramètres arrêterait tout avant tout changement.
        La racine / n'est jamais essayée, par sûreté (L-6) : sa garde se relit dans le script."""
```

Éprouvée sur la série : `corrections/C-1.diff` (+2 −1) s'applique après DB1-g ; 115 caractères au plus ; module et job
s2bis verts (Ran 355 à cet état) ; la phrase reste vraie après C-2 (garde relue : vide, « / », « // »).

## Corrections C-1 à C-9 (liste fermée ; forme exacte : `corrections/C-n.diff`)

Chaque correction s'applique après la précédente (C-1 après DB1-g). Rouge : tests de la correction posés sur le code de
l'état précédent (module `test_deploi`, python3.12, isolé) ; vert : module, puis ligne du job s2bis à l'état de la
correction (§4). Mutants : campagne h (§4).

- **C-1 — DB1-h, docstring L-6** (adjugée) : forme au §7. Aucun test à rougir (texte de docstring).
- **C-2 — garde de la racine d'essai.** Constat : §3 (racine vide après un `cd` en échec, « // »). Forme : l.27 devient
  `[ -n "$R" ] && ! [ "$R" -ef / ] && [ -f "$R/essai.getent" ] ||` (commentaire : vide, « / », « // ») suivi, à la ligne,
  du refus inchangé ; `-ef` compare périphérique et inœud, donc refuse « / » sous toute écriture. Preuve hors suite
  (L-6) : chroot (§3), rouge sur g, refus sur C-2. Mutant `h-c2` (retour à `!= /`) : vivant **par construction**.
- **C-3 — temporaire né 0600.** Constat : `ecrire` crée `X.nouveau` sous l'umask 022 (0644) puis le passe à son mode ;
  pour `observateur.conf`, l'adresse secrète du signal de vie (Q-6 : refusée à `intervention`) est lisible de tous entre
  la création et le `chmod` (un lecteur qui attend la création, par inotify sur `/etc/shogen` lisible, garde un
  descripteur ouvert) et reste lisible si le lancement est interrompu avant le `chmod` ; une relance réécrit le fichier
  restant sans changer son mode. Forme : `rm -f "$R$1.nouveau"` puis `(umask 077 && cat > "$R$1.nouveau")`.
  Test `test_tdp1_temporaires_nes_0600` : une fonction `chmod` exportée relève le mode de chaque temporaire juste avant
  son `chmod` (sept fichiers, tous `600`), un temporaire 0644 laissé par un lancement interrompu étant posé d'avance.
  Rouge sur C-2 : 1 échec (`644` au lieu de `600`). Mutants `h-c3a` (sans `rm -f`), `h-c3b` (sans umask 077).
- **C-4 — relance : rien sous le dossier du compte `intervention`.** Constat : à un second lancement (réparation,
  reprise après un échec), root refait `install -d -m 0700 /home/intervention/.ssh`, écrit `authorized_keys.nouveau`
  et le passe en 0600, dans un dossier que le compte possède depuis le premier lancement ; un agent porteur d'une clé
  déléguée (E-D-17 (c)) qui y a posé des liens obtient de root le passage en 0700 d'un dossier quelconque (`.ssh` lien
  vers `/etc` : services sans lecture de `/etc`), l'écriture de la ligne de clé dans un fichier quelconque (`.nouveau`
  lien vers un fichier : écrasé, mis 0600 ; vers `/etc/apt/apt.conf.d` par `.ssh` : APT en erreur de syntaxe, plus de
  mises à jour), sans droit d'administration au départ (Q-1 : « une clé d'agent ne donne jamais root »). Démontré en
  dossier temporaire (`install -d` suit le lien de dossier ; `cat >` suit le lien de fichier ; `chown -R` ne suit pas le
  lien de la ligne de commande). Forme : si `getent passwd intervention` trouve le compte, message nommé
  `COMPTES/intervention présent, clé inchangée` sur la sortie d'erreur et retour ; sinon création et clé comme avant
  (premier lancement inchangé, journal compris). Test `test_tdp1_relance_rien_sous_le_compte_d_intervention` : compte
  présent (`essai.getent`), lien `.nouveau` vers un fichier et lien `.ssh` vers un dossier, cibles hors de la racine
  factice : cibles intactes (contenu, mode 0644 et 0755, dossier vide), message nommé, seule commande du compte
  `getent passwd intervention`. Rouge sur C-3 : 2 échecs (`chown -R` journalisé ; dossier passé 0700 et clé écrite
  dedans). Mutants `h-c4a` (poursuite après le message), `h-c4b` (sans message). Conséquence pour la procédure (DB-6) :
  changer la clé d'intervention passe par la console du fournisseur.
- **C-5 — formes fermées.** Constat : §1 (`010.1.1.1` lu `8.1.1.1` par nft et par `getaddrinfo`, contrôlé ;
  `256.1.1.1` refusé tard par `nft -c` après six étapes ; bloc de clé faux admis). Forme : octet
  `(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])` ; clé `^ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI[A-Za-z0-9+/]{43}` suivie du
  commentaire facultatif inchangé (bloc de 68 caractères : chaîne « ssh-ed25519 » et clé de 32 octets, en-tête fixe de 25
  caractères ; recalculé en base64 sur une clé nulle, une pleine et une tirée au hasard, admise). Tests ajoutés au
  test des refus : `010.1.1.1`, `256.1.1.1`, deux espaces entre adresses ; bloc court (40), long (69), d'en-tête
  faux ; commentaire de deux mots ; une valeur à deux lignes pour chacun des huit paramètres. Rouge sur C-4 : 5 échecs
  (`010`, `256`, court, long, en-tête). Mutants : `h-c5a` (octet `[0-9]{1,3}`), `h-c5b` (bloc libre), `h-c5c`
  (`{43,}`) ; et `g06h`, `g07`, `g20` (suffixes et ancre) vivants à g, tués à h par les cas à deux lignes.
- **C-6 — minuteries APT lancées ; pare-feu rechargé.** Constat : §1 (`enable` sans `--now` ; `restart` = `nft flush
  ruleset` puis chargement, lu sur l'unité `nftables.service` de l'hôte : `ExecStop=/usr/sbin/nft flush ruleset`,
  `ExecReload=/usr/sbin/nft -f /etc/nftables.conf`). Forme : `systemctl enable --now apt-daily.timer
  apt-daily-upgrade.timer` ; `systemctl reload-or-restart nftables.service` (service actif : rechargement atomique du
  jeu, qui commence par `flush ruleset` ; inactif : démarrage). Tests : commandes attendues ; le test du nom non résolu
  exige qu'aucune commande `nft` ni du service nftables ne soit journalisée (au lieu de la seule absence de `restart`).
  Rouge sur C-5 : 4 échecs (journal des quatre observateurs). Mutants `h-c6a`, `h-c6b`.
- **C-7 — test T-DP-2 : rien hors des blocs attendus.** Constat : mutants vivants à g : `g01` (règle de premier niveau
  `add rule inet shogen sortie accept` dans les deux copies : tout le sortant ouvert), `g02` (ensemble `resolveurs`
  pré-rempli de `0.0.0.0/0`), `g03` (`flags interval` retiré : O1 refusé par `nft -c` au seul déploiement). Forme :
  `pare_feu` rend le premier niveau, les ensembles et les chaînes ; le test exige le premier niveau exact (`flush
  ruleset`, `table inet shogen {`, `}`, l'inclusion) et les trois ensembles exacts, vides au dépôt. Tue `g01` à `g03`.
- **C-8 — test : dossiers créés en 0755.** Constat : mutant vivant `g05` (`umask 000` : `etc/shogen` et `etc/nftables.d`
  en 0777, où tout compte pourrait remplacer `observateur.conf` ou poser un `.nft` inclus par le pare-feu). Forme : le
  test des paramètres gardés exige 0755 pour ces deux dossiers. Tue `g05`.
- **C-9 — test des sources fidèle à Debian 13.** Constat : mutants vivants `g17` (fichiers `.sources` du fournisseur
  gardés) et `g18` (`debian.sources` de l'image gardé, miroir HTTP, que le pare-feu coupe : plus de mises à jour) ;
  l'image du test n'avait ni l'un ni l'autre. Forme : l'image du test porte un `debian.sources` (deb822, HTTP, avec
  `trixie-updates`) et un `fournisseur.sources` ; le test exige leur sort (remplacé ; désactivé, contenu intact) et
  l'ensemble exact des fichiers de sources. Tue `g17`, `g18`.

## 8. Écarts du réviseur

- **E-1** `NOTES.md` : deux heures écrites avant lecture de l'horloge (« 05:40-06:00 », « 06:10 »), corrigées à l'heure lue
  (05:45, 05:54:30) ; aucune heure estimée dans les livrables.
- **E-2** Une comparaison `diff -rq` entre mes deux copies (base et série) a parcouru leur `docs/` (noms de fichiers
  différents seuls affichés ; copies sans dossiers interdits ni `*.jsonl`), et un `du -sh` a mesuré mon dossier
  temporaire ; aucun autre parcours récursif.
- **E-3** Deux premiers lancements de démonstration sans résultat (sorties visées hors des montages en écriture : bac à
  lecture seule ; chroot), refaits ; aucune écriture hors du dossier, contrôlée (`/essai.getent` et `/etc/nftables.d`
  de l'hôte absents avant et après).
- **E-4** Job sim-bis : `GIT_DIR` du dépôt, `GIT_OPTIONAL_LOCKS=0`, pour les seuls `git --no-optional-locks archive` des
  oracles (lecture seule, fichiers épinglés), comme l'E-4 du générateur ; les tests de sim-bis n'appellent `git` que par
  ces adaptateurs (fichiers nommés relus).
- **E-5** Barres obliques inverses tapées dans des commandes d'outils (`sed`, `tr`, `od`, motif R-13) : octets contrôlés
  par `od -c` ; aucune dans les diffs de correction (contrôle sur octets).
- **E-6** Une boucle d'attente en tâche de fond (`pgrep -f` sur le nom de l'outil de mutants) se reconnaissait dans sa
  propre ligne de commande et bloquait l'enchaînement des gates : arrêtée par moi (processus de mon outil), sans effet
  sur un résultat ; l'enchaînement est reparti à 06:06:28 UTC.
- **E-7** `xtask` : pour donner la violation de S-G9 par `chemin:ligne`, une première extraction (`grep -o` de motifs
  `chemin:ligne`) a porté sur toute la sortie et affiché la liste des références des autres gates (chemins et numéros
  seuls, aucun contenu) ; la seconde s'est bornée à la section S-G9. Aucun fichier cité n'a été ouvert.
- **E-8** Machine chargée par d'autres chaînes (charge 4 sur 4 cœurs) : un mutant tous les 40 à 90 s ; aucun run
  interrompu ni FATAL.

## 9. Limites rendues (règle PAROXYSME) et points pour les briefs suivants

- **IPv6** non sondable sur cet hôte (noyau sans IPv6) : même limite que L-1 du générateur ; la sonde IPv6 du smoke
  (DB-2) la ferme.
- **Outils de l'hôte** (nft 1.0.9, apt 2.8.3, unité `nftables.service` du paquet Ubuntu 1.0.9) au lieu de ceux de trixie
  (L-4 du générateur) : C-6 suppose un `ExecReload` à l'unité de trixie ; sans lui, `reload-or-restart` redémarre, comme
  la série : aucune régression ; à constater au smoke (DB-2, `systemctl cat nftables.service`).
- **Garde de racine** : non éprouvable par la suite (L-6, C-1) ; éprouvée hors suite (chroot) pour C-2.
- **DB-6 (procédure)** : avec C-4, une relance ne change pas la clé d'intervention (refus nommé) : la rotation de cette
  clé passe par la console du fournisseur ; à écrire dans la procédure d'intervention.
- **Observation hors lot** : à 06:26 UTC, `git status` du dépôt montre `biblio/INDEX.md` modifié et indexé ; ni DB-1
  ni ce réviseur n'y ont touché (dépôt propre à 05:11 UTC ; commandes git du réviseur en lecture seule).
- **Enregistrement de rôle G2** (SHOGEN-G2-ENREG-ROLE-1) : sans objet, DB-1 n'est pas un lot du chemin S2 soumis au cp-2
  (campagne S2-bis, ADR-0029) ; le brief ne le demande pas.

## 10. Journal de provenance (G1)

- **Lu [lu]** (sha256 tronqué) : `g2/BRIEF-G2.md` (`1992b975`) ; `../ADJUDICATION.md` (`355e7a76`) ; `../AVIS.md`
  (`c9eb967b`) ; `../RAPPORT-GENERATEUR.md` (`e888b9a2`) ; `../BRIEF-DB1.md` (`1413926f`) ; `../NOTES.md` (`1ddba6cb`) ;
  `../SHA256SUMS` (90 lignes, `sha256sum -c` conforme) ; `db0/ADJUDICATION-DB0.md` (`bbc4ae5a`) ; `db0/RAPPORT-DB0.md`
  (`73444aba`, 225 l.) ; `PROPOSITION.md` l.616-781 (`0cdf84c2`) ; `G0-COLLECTE-RECALC-DEPLOI.md` à la base (`d9160d3e`,
  27 l.) ; ADR-0029 l.79-83 et l.107-110 (`32a59893` ; Quad9, Google, témoins D-4) ; `CP2-S2.md` l.30-40 (enregistrement de
  rôle) ; les sept diffs en entier ; script, `nftables.conf` et `test_deploi.py` de l'état g en entier ; `gates.yml`
  (jobs unittest et R-13) ; tête de `verdict-suite-s2.py` et de `gate-secrets.sh` ; `s2bis/tests/__init__.py` ;
  appels `git` et `subprocess` de `scripts/sim-bis` (fichiers nommés) ; définitions de mutants du générateur
  (`mutants/{b..f}.py`) ; `tmp/g0/date-ecriture*.txt` du générateur ; unité `nftables.service` et aide de `systemctl`
  de l'hôte ; outils `isole.sh`, `lo_up.py`, `gates.sh` du dossier p1b.
- **Calculé [calc]** : bloc ed25519 (base64 de « ssh-ed25519 » et d'une clé de 32 octets : 68 caractères, en-tête de 25
  fixe) sur une clé nulle, une pleine et une tirée au hasard ; tailles du script (`wc -c`, rempli au pire) ; lignes des diffs
  (comptes sur octets, caractères par Python) ; empreintes des séries.
- **Inféré [inféré]** : sémantique de `restart` et `reload-or-restart` sur l'unité de trixie (lue sur celle d'Ubuntu de
  l'hôte) ; lecture concurrente par inotify du temporaire 0644 (mécanisme connu, non joué) ; usage d'une relance
  (réparation, reprise) ; format RFC 8709 de la clé (non relu en session ; recoupé par le calcul et la clé du test).
  **Seconde main [2nd]** : aucun chiffre repris sans recompte (rouges, planchers, tailles, comptes de lignes recomptés).
- **Commandes** (sorties dans `travail/preuves/`) : `outils/etats.sh` (états 0, a à g) ; `outils/job_etat.sh` (job à
  chaque état) ; rouge par module (`rouge-<x>.txt`) ; `outils/mutants_g2.py` (campagnes g, obligatoires, h) ;
  `outils/serie_corrections.sh`, `module.sh`, `job_corr.sh`, `jobs_corrections.sh` (corrections, rouge et vert) ;
  `outils/chroot_garde.sh` (garde) ; bac `/` en lecture seule (essai) ; `strace` d'un essai (sans conclusion :
  `mkdir -p` nomme ses composants en relatif ; preuve retenue : le bac) ;
  `outils/sonde_g2.py` (sonde) ; `nft -c` et inclusion réelle (espaces privés) ; `apt-config` (ligne de clé dans
  `apt.conf.d` : `E: Syntax error`, code 100 ; témoin 0) ; `gate-secrets.sh` et motif R-13 sur l'index local ;
  `outils/gates_finales.sh`, `matrice.sh` ; `cargo --locked test`, `cargo --locked xtask verify` (lignes VERDICT).
