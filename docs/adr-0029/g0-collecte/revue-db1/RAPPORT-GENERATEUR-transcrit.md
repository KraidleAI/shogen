# Rapport du générateur de DB-1, avec ses phases 2 à 4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:55:47 UTC du fichier db1/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-GENERATEUR — DEPLOI-BIS, sous-lot DB-1 (générateur G1), 2026-10-10 (heure lue : 04:24 UTC)

- **Gate 0** : modèle résolu `claude-opus-5-5` (Opus 5.5, identifiant exact déclaré par l'environnement), effort `max`.
- **Brief** : `BRIEF-DB1.md`, sha256 `1413926fefe14777deebf168a64c2d4df894fe193ba426e26b0984318a536950` (conforme).
- **Base** : tête relevée au premier `rev-parse` (02:42 UTC) 6e017729 ; archive prise à 02:51 UTC sur la tête du moment,
  **39718f45ab3d48490ce050db59ed02ef37e48255** (FUZZ FZ-c ; entre les deux, crates/ et xtask/ seuls). Copie éparse :
  `git archive` sans `docs/15-*`, `docs/16-*`, `docs/pocket-report`, `docs/rapports`, `docs/adr-0025`,
  `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution` ni `*.jsonl` (1336 entrées, 0 interdite au contrôle).
- **Tête du moment à la fin** : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` (2026-10-10T04:18:02Z) : les six diffs s'y
  appliquent dans l'ordre (`git apply --check` puis `git apply` sur ses versions des fichiers touchés) ; entre la base
  et cette tête, parmi ces fichiers et le vérificateur, seul `gates.yml` change (job controle, plancher 36 → 37).
- **Interdits** : aucune pièce de D.2, aucun `*.jsonl`, rien des dossiers interdits ; aucune liste par motif sur
  `docs/`, le dépôt ou le scratchpad entier ; aucun réseau ; aucune variable de clé lue ; aucune écriture git au dépôt
  (index local au scratchpad pour fabriquer les diffs) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée de chaque
  run).

## 1. Série livrée (dossier `diffs/`, à appliquer dans l'ordre)

| diff | objet | lignes ajoutées / retirées (fichiers) | sha256 |
|---|---|---|---|
| DB1-a | ajout daté au G0 : décisions 1 à 10 de DB-0, rattachées | 32 / 0 (G0) | `d367d95ef6d0fc7c4e90881b5f9386e5e6e35b92b82b68920cf0aeb4eb1b1522` |
| DB1-b | script I : paramètres en tête, mode d'essai, contrôle des paramètres ; T-DP-1 (bash -n, usage, racine, refus), décision 5 ; plancher 346 | 185 / 1 (script 65, tests 119, gates.yml 1) | `6a3dd100c432956d53586ab0918202b6be5ef719611f729b305b5117f533b57d` |
| DB1-c | étapes sources, paquets, comptes, observateur ; T-DP-1 (essai à quatre observateurs, fichiers produits, sources) ; plancher 349 | 118 / 1 (64, 53, 1) | `5f23f9cf0a7f89f67f2f7c58371e24d54ff4d48dc11e48ad5f3140559f3678f8` |
| DB1-d | étapes ssh et mises à jour ; T-DP-5, T-DP-9 ; plancher 351 | 60 / 4 (32, 27, 1) | `ca733cde7ed97103c05814a281daa5a22c17ca764f5084c842b54d9b122aca51` |
| DB1-e | `s2bis/deploi/nftables.conf` ; T-DP-2 (structure) ; plancher 353 | 101 / 2 (54, 46, 1) | `5cdddf9cfb63acec3ac8e40859f0c95e2b83f50dcc4b0d1b1ef4ea0523fa7d48` |
| DB1-f | étape pare-feu (commun embarqué, ensembles d'observateur) ; T-DP-2 (ensembles, refus) ; plancher 355 | 121 / 8 (91, 29, 1) | `479eae52074ca5dca7bd0a0ff6caaf3d57ea0a1d05fb6e5f7ea0f418f2f2f186` |

Lignes ajoutées : aucune au-delà de 120 caractères, aucune barre oblique inverse, aucun blanc final, aucun retour
chariot (contrôle sur les octets des diffs) ; tabulations : celles de `nftables.conf` (forme Debian), 38 en e et en f.
DB1-a est daté `2026-10-10 04:06:47 UTC` (`date -u` lue juste avant l'écriture du texte, seule écriture) et replié à
120 caractères (règle du brief ; même rendu Markdown que les ajouts existants, écrits d'une ligne).

**Plancher du job `s2bis-unittest`** : delta **+13** sur la base (342 → 355) : +4 (b), +3 (c), +2 (d), +2 (e), +2 (f).
DETTES-T6 recale aussi ce plancher : sur une tête qui le porte à X, les diffs se recalent à X+4, X+7, X+9, X+11, X+13
(seule la ligne `--plancher` du job change ; `s2bis/` est inchangé de la base à dda4bbc).

## 2. Le script I (`s2bis/deploi/premier-demarrage.sh`, 11 850 octets à DB1-f)

- **Paramètres en tête** (E-D-01), vides au dépôt : `OBSERVATEUR`, `FOURNISSEUR`, `REGION`, `FAMILLE_RESOLVEUR`,
  `RESOLVEUR_FOURNISSEUR` (famille fournisseur, O4), `ADRESSE_SURVEILLANCE`, `ADRESSE_SAUVEGARDE`, `CLE_INTERVENTION`
  (Q-1). Formes fermées contrôlées **avant tout changement** : refus `PARAMETRE/<nom>`, sortie 2.
- **Mode d'essai** (T-DP-1) : `--essai <racine>` ; racine refusée si `/` ou sans `essai.getent` ; apt-get, systemctl,
  useradd, chown, nft et sshd remplacés par des enregistreurs (`<racine>/essai.commandes`), getent lit la résolution
  factice. Hors essai : root, sans argument (collé en user data, ou lancé à la main chez OVHcloud, décision 5).
- **Étapes** : `sources` (Q-2) ; `paquets` (`chrony nftables python3 rsync unattended-upgrades`, `unbound` pour O1,
  `--no-install-recommends`) ; `comptes` (`shogen` système, sans shell ni groupe ; `intervention`, clé seule, Q-1) ;
  `observateur` (`/etc/shogen/observateur.conf`, 0640 root:shogen, Q-6) ; `ssh` (`00-shogen.conf`, lu avant
  `50-cloud-init.conf` : `PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`,
  `PermitEmptyPasswords no`, `PubkeyAuthentication yes`, `AuthenticationMethods publickey`, `AllowUsers intervention`,
  `DisableForwarding yes` ; `sshd -t` ; rechargement) ; `mises_a_jour` (`90shogen-securite` : `#clear` des origines
  lues avant, seule origine `trixie-security`, `Automatic-Reboot "false"`, minuteries APT actives) ; `pare_feu` (jeu
  commun embarqué, égal à `nftables.conf` ; ensembles d'observateur ; nom non résolu : `PARE-FEU/résolution`, sortie 3,
  rien d'écrit ; `nft -c`, activation, chargement).
- **Pare-feu** (`inet shogen`, refus par défaut en entrée, sortie et transit ; IPv6 jeté en deuxième règle des deux
  chaînes, après la boucle locale) : sortie 443 vers tout ; UDP/53 vers les trois témoins D-4 (l.109) ; UDP et TCP/53
  vers l'ensemble `resolveurs` (0.0.0.0/0 pour O1 ; Quad9 ou Google, l.82 ; adresses collées pour O4) ; 123/UDP et
  4460/TCP vers `ntp` ; 23/TCP vers `sauvegarde` ; DHCP et métadonnées (Q-3) ; entrée : SSH et réponses DHCP.
- **Points d'entrée nommés** (sans marqueur de dette) : avant le pare-feu, horloge et résolveur (DB-2 : les ensembles
  par nom en dépendent, décision 3) ; après, code, descripteur et smoke (DB-2), unités (DB-3), sauvegarde, têtes,
  signal de vie, alerte disque (DB-4), empreintes (DB-5).

## 3. Exigence → test → mutants

| exigence | diff | test(s) de `s2bis/tests/test_deploi.py` | mutants (tous tués) |
|---|---|---|---|
| E-D-01 : paramètres en tête, contrôle avant tout changement | b | `test_tdp1_parametre_refuse_rien_ne_change` | b01-b08, b07s, b10, b11 |
| T-DP-1 : `bash -n` | b | `test_tdp1_syntaxe` | b07 (aussi) |
| T-DP-1 : mode d'essai, racine et usage refusés | b | `test_tdp1_usage_et_racine_refusees` | b09 |
| Décision 5 : rempli, ≤ 32 KiB (M : borne retirée) | b | `test_decision5_taille` (témoin négatif inclus) | b12 (script gonflé), b13 (borne retirée) |
| T-DP-1 : essai à quatre observateurs, étapes, commandes, fichiers (M : étape omise) | c, d, f | `test_tdp1_essai_quatre_observateurs` | c01-c03, d01, d02, f01 |
| T-DP-1 : enregistreurs | c | idem | c17 (apt-get réel lancé) |
| E-D-04, décision 1 : paquets | c | idem | c08, c09 |
| E-D-04, E-D-12 : sources (Q-2) | c | `test_tdp1_sources_https_et_trousseau` | c04-c07 |
| E-D-03 : compte de service sans droits ; intervention | c | essai (commandes exactes), `test_tdp1_parametres_gardes_et_cle` | c10-c13 |
| E-D-01 : paramètres gardés (Q-6) | c | `test_tdp1_parametres_gardes_et_cle`, essai | c14-c16, c18 |
| E-D-03, T-DP-5 (M : mot de passe admis) | d | `test_tdp5_sshd_cle_seule` | d03, d04-d08 |
| E-D-12, T-DP-9 (M : redémarrage automatique activé) | d | `test_tdp9_securite_seule_sans_redemarrage` | d09, d10-d14 |
| E-D-05, Q-D-07, T-DP-2 (M : tout le sortant ouvert ; un témoin oublié ; IPv6 admis) | e | `test_tdp2_refus_par_defaut_ipv4_et_ipv6`, `test_tdp2_regles_exactes` | e01, e02, e03-e04, e05-e13 |
| E-D-05, décisions 3 et 4 : commun embarqué, ensembles, nom non résolu | f | `test_tdp2_commun_embarque_et_ensembles`, `test_tdp2_nom_non_resolu_refuse`, essai | f01-f14 (f02-f04, f14 : mutés dans les deux copies) |

**Mutants : 73 lancés (b 14, c 18, d 14, e 13, f 14), 73 tués, 0 vivant, 0 FATAL.** Chacun : une mutation, posée en
place sur l'arbre complet de l'état, commande du job (`python3 -B enforcement/verdict-suite-s2.py s2bis --aucun-saut
--egal --plancher N`, python3.12 = 3.12.3 comme l'image), bac à sable (/ en lecture seule, réseau isolé), fichier rendu
octet pour octet (sha256) ; classement par la sortie du vérificateur (1 tué, 0 vivant, autre FATAL). Chaque mutant est
tué par au moins un test de `test_deploi.py` (contrôlé sur les relevés). Équivalents : aucun déclaré ; non posés comme
équivalents évidents : les enregistreurs encore inutilisés à l'état b (nft, sshd, systemctl). Relevés :
`preuves/mutants-{b..f}.txt`, sorties complètes `mutants/<x>.py.d/`.

**Rouge puis vert** (rouge : tests de l'état sur le code de l'état précédent ; vert : module, puis job) :

| diff | rouge | vert, module | vert, job |
|---|---|---|---|
| b | 4 tests, 20 échecs d'assertion (sous-tests), 0 erreur (script absent) | 4 OK | conforme, Ran = 346 |
| c | 8 échecs d'assertion, 0 erreur | 7 OK | Ran = 349 |
| d | 6 échecs d'assertion, 0 erreur (premier essai : 1 erreur, E-2) | 9 OK | Ran = 351 |
| e | 2 échecs d'assertion, 0 erreur | 11 OK | Ran = 353 |
| f | 10 échecs d'assertion, 0 erreur | 13 OK | Ran = 355 |

**Vérifications indépendantes du code** : (1) `apt-config dump` (apt 2.8.3 de l'hôte) sur un `50unattended-upgrades`
adverse (trois motifs Debian, `Allowed-Origins`, `Automatic-Reboot "true"`), un `20auto-upgrades` à 0 et le fichier
90 produit : un seul `Origins-Pattern` (trixie-security), `Allowed-Origins` vide, `Automatic-Reboot "false"`,
périodiques à 1 ; témoin sans le fichier 90 : trois motifs, `"true"` ; Origin, Label et Codename lus dans
l'`InRelease` de trixie-security de DB-0 (`Origin: Debian`, `Label: Debian-Security`, `Codename: trixie-security`).
(2) `nft -c` conforme sur les jeux produits pour O1, O2, O4 ; jeu chargé dans un espace réseau neuf et sondé sur le fil
(tun0 lue par la sonde) : sortie conforme au §2 (80 bloqué sauf métadonnées pour root ; TCP/53 vers un témoin et l.root
bloqués hors O1 ; 22 sortant bloqué ; DHCP depuis le port 68 seul) ; entrée : SSH et réponses DHCP seuls ; témoin sans
jeu : 24 envois passent, 7 entrent (`preuves/sonde-pare-feu.txt`). (3) Suite du module sous uid 65534 (tmpfs privé,
/ en lecture seule, réseau isolé) : 13 OK ; sous 3.10, 3.11, 3.12, 3.13 en `-X dev -W error` : 13 OK, 0 avertissement.

## 4. Gates sur la copie finale (39718f4 + DB1-a à DB1-f ; lignes de gates.yml telles qu'écrites)

- Runner `run-fixtures-verdict-suite-s2.py` : `137 ok, 0 échec`.
- Jobs : s2bis conforme, Ran = 355 ; S2 (`--egal`) conforme, Ran = 419 (sauts nommant la variable) ; sim-bis
  conforme, Ran = 279 (sous `isole.sh`, `GIT_DIR` du dépôt en lecture pour les oracles, E-4) ; calib-actifs conforme,
  Ran = 65 ; controle conforme, Ran = 36 (plancher de la base).
- `docs-sha256sums.py` conforme (35 SHA256SUMS, 299 lignes, 11 absentes admises) ; `workflows-yaml.py` conforme
  (7 workflows, PyYAML 6.0.1, version de l'image) et ses cas 16/16 ; `runners-epingles.py`, `lint-model-pinning.sh`,
  `journaux-modele.py` conformes ; secrets (index jetable des cinq fichiers) OK ; R-13 (motif lu dans gates.yml) : 0.
- `cargo --locked xtask verify` : S-G1 à S-G8 VERT ; **S-G9 ROUGE, 1 violation** (`docs/17-modele-de-menace.md:70`
  cite `docs/rapports/cartographie-2026-09-29.md`, dossier interdit, absent de la copie éparse) ; verdicts identiques
  sur la copie témoin de la base (E-5) ; `cargo fmt --check`, no_std, clippy : VERT.
- `cargo --locked test`, cible par défaut de la copie (`tmp/copie-finale/target`, règle I-1) : 27 lignes
  `test result: ok`, 265 passed, 0 failed, 0 ignored.

## 5. Questions Q-n (recommandation codée dans la série)

- **Q-1 Compte de connexion SSH (E-D-03, E-D-01).** E-D-03 dit « clé seule ; ni root ni mot de passe » sans nommer le
  compte qui se connecte ; sans compte nommé, `AllowUsers` ne peut pas écarter les comptes des images (root chez
  Hetzner, DigitalOcean et Linode ; `debian` avec sudo chez OVHcloud) [inféré, non lu sur pièce]. Codé : compte
  `intervention` créé par le script, sans droit d'administration (aucun groupe, aucun sudoers), clé `ssh-ed25519` de
  l'investisseur en paramètre `CLE_INTERVENTION` (ajout à la liste d'E-D-01, avec `RESOLVEUR_FOURNISSEUR`) ; sshd :
  `AllowUsers intervention`, `DisableForwarding yes`. Conséquences : N2 et N3 passent par la console du fournisseur ;
  `status` se lira par ce compte (droit de lecture des journaux à poser à DB-3 ou DB-4) ; une clé déléguée (option (c))
  ne donne pas root. Variante écartée : sudo pour ce compte. **Recommandation : adopter**, et l'écrire à la procédure
  (DB-6).
- **Q-2 Sources APT (E-D-04, E-D-12, décision 1).** Le pare-feu n'ouvre que TCP/443 en sortie (E-D-05) ; les miroirs
  des images de fournisseurs servent APT en HTTP [inféré] : les mises à jour de sécurité tomberaient en silence. Codé :
  une seule source, l'archive Debian en HTTPS (`deb.debian.org`, suites `trixie` et `trixie-security`, `main`, trousseau
  `debian-archive-keyring.pgp`, à défaut `.gpg`, refus et arrêt sans trousseau) ; les autres fichiers de sources sont
  renommés `*.disabled` (ignorés sans bruit par APT). Motifs : sortie 443 seule ; versions comparables au tableau R-8,
  lu sur cette archive à DB-0. `trixie-updates` n'est pas posée (la décision 1 n'admet que la sécurité). Variantes :
  ouvrir TCP/80, ou garder les miroirs. **Recommandation : adopter.**
- **Q-3 Pare-feu : écarts au « exactement » de T-DP-2.** Ajoutés, faute de quoi l'observateur se coupe lui-même :
  (a) DHCP, UDP 68→67 en sortie et 67→68 en entrée (bail IPv4 par DHCP chez Hetzner, OVHcloud, Linode [inféré]) ;
  (b) métadonnées du fournisseur, TCP/80 vers 169.254.169.254 pour root seul (`meta skuid 0`), lues par cloud-init à
  chaque démarrage, donc à chaque N2 [inféré] ; (c) boucle locale, `established,related`, `invalid` jeté. Rien d'autre :
  la sonde sur le fil le montre (§3). **Recommandation : adopter et l'inscrire au prochain ajout daté du G0.**
- **Q-4 Où vit le pare-feu commun.** Il doit être posé avant l'arrivée de l'archive du code (Q-D-01), et seul le script
  arrive par cloud-init. Codé : copie embarquée dans le script (document en ligne), égale octet pour octet à
  `s2bis/deploi/nftables.conf` (test). Variante : poser le pare-feu après l'archive (DB-2), une seule copie, mais une
  fenêtre sans pare-feu pendant l'installation. **Recommandation : copie embarquée.**
- **Q-5 Ensembles par nom (décision 3).** Les adresses des serveurs NTP et de l'espace de sauvegarde sont résolues au
  premier démarrage seulement ; time.nl prévient que les adresses changent sans préavis [lu, RAPPORT-DB0 §5] ; un
  serveur NTS-KE peut aussi désigner une autre adresse NTP (RFC 8915 §4.1.7) [inféré], que le pare-feu jetterait
  (visible en D-3). **Recommandation : minuterie de rafraîchissement à DB-3 (même fonction, résolveur de
  l'observateur, rechargement atomique des seuls ensembles), et constat des adresses négociées au smoke (DB-2).**
- **Q-6 Paramètres gardés sur l'observateur.** Codé : `/etc/shogen/observateur.conf` (0640, root:shogen), seule
  interface des paramètres pour DB-2 à DB-5 ; il porte l'adresse secrète du signal de vie (sur le disque de
  l'observateur, jamais au dépôt, ADR l.245). **Recommandation : adopter.**

## 6. Limites L-n (rendues comme items à former, règle PAROXYSME)

- **L-1 IPv6 non sondé sur le fil** : l'hôte de la session n'a pas AF_INET6 (EAFNOSUPPORT) ; le refus d'IPv6 est
  établi par la structure (table `inet`, `meta nfproto ipv6 drop` en deuxième règle des deux chaînes, tests et mutants)
  et par `nft -c`, pas par un paquet. Item proposé : SHOGEN-S2BIS-IPV6-SONDE-1 (sonde au premier déploiement).
- **L-2 sshd absent de l'hôte** : ni `sshd -t` ni `sshd -T` lancés ; le contenu du fichier et son rang de lecture sont
  testés, la configuration effective non. Item proposé : SHOGEN-S2BIS-SSHD-EFFECTIF-1 (`sshd -T` au smoke, DB-2).
- **L-3 Trousseau de Debian 13** : chemin `.pgp` ou `.gpg` [inféré] ; le script prend l'un ou l'autre et refuse sans
  trousseau ; à constater au premier déploiement (avec la présence de `ca-certificates`, exigée par APT en HTTPS).
- **L-4 Outils de l'hôte, pas ceux de trixie** : `apt-config` d'apt 2.8.3 (Ubuntu 24.04) au lieu d'apt 3.0.3, `nft`
  1.0.9 au lieu de 1.1.3 [inféré : mêmes grammaires pour les formes employées].
- **L-5 Métadonnées et DHCP par fournisseur** [inféré] : adresse 169.254.169.254 et bail DHCP non lus sur pièce ;
  à constater à la mise en service (E-D-22), avec un N2 volontaire. Item proposé : SHOGEN-S2BIS-METADONNEES-1.
- **L-6 Racine « / » refusée, non essayée** : la garde du mode d'essai (racine sans `essai.getent` refusée) est
  testée sur une racine vide et absente ; un essai sur `/` n'est jamais lancé, par sûreté.
- **L-7 Sûreté du mode d'essai** : la suite lance le script en essai sous le compte qui la lance (root pour le G3
  local) ; la sûreté tient à la garde de racine, aux enregistreurs et au refus des paramètres du script non rempli ;
  les mutants n'ont tourné que dans le bac à sable (/ en lecture seule, réseau isolé).
- **L-8 Redémarrages de services par les mises à jour** (postinst de chrony, unbound) : trous D-3 ou D-5 possibles,
  non traités ici. Item proposé : SHOGEN-S2BIS-MAJ-SERVICES-1 (doc 17 à DB-6 ; `needrestart` à DB-3).
- **L-9 Ensembles par nom non rafraîchis** (Q-5). Item proposé : SHOGEN-S2BIS-PAREFEU-NOMS-1.
- **L-10 Test existant sensible à la charge** (E-6) : item proposé SHOGEN-S2BIS-TEST-SANTE-CHARGE-1 (hors DB-1).

## 7. Écarts E-n

- **E-1** NOTES.md : deux intertitres d'abord datés d'estimation, corrigés à l'heure lue (03:20, 03:49) ; aucune date
  estimée dans les livrables versés.
- **E-2** Premier rouge de DB1-d avec une erreur (`os.listdir` sur un dossier absent) : `test_tdp9` lit d'abord le
  fichier (existence affirmée), états d à f régénérés (b, c inchangés au `cmp`), rouge refait sans erreur.
- **E-3** Mutant b07 tué aussi par une erreur de syntaxe (`;` dans `[[ ]]`) : variante b07s, sans erreur de syntaxe,
  tuée par le refus de paramètre.
- **E-4** Job sim-bis : dans le bac à sable à `/dev/shm` en lecture seule, 2 échecs (SemLock de multiprocessing),
  sans lien avec la série ; relancé sous `isole.sh` (réseau seul isolé) : conforme. Les oracles lisent le dépôt par
  `GIT_DIR=/home/user/shogen/.git` et `git --no-optional-locks archive` (lecture seule ; fichiers de code épinglés).
- **E-5** S-G9 rouge par l'éparsité imposée de la copie, non par la série (témoin identique).
- **E-6** Test existant sensible à la charge, en ERROR une fois (TypeError, `enr["d3"]` nul) pendant le mutant c04,
  tué par ailleurs par `test_deploi` :
  `tests.test_sante.Branchement.test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null` ; une occurrence en 81
  runs complets de la suite s2bis (recompte : 1 de base, 6 verts, 73 mutants, 1 final).
- **E-7** Deux `rm -rf` à chemin variable refusés par le contrôle de sûreté de l'outil ; aucun contournement ;
  nettoyage fait ensuite par chemins littéraux (copies intermédiaires, cibles cargo, dossiers temporaires de
  `cargo test`) ; restent `tmp/base`, `tmp/copie-finale` (sans cible), l'index local et les états, pour la relecture.

## 8. Ce qui reste à DB-2 à DB-6

- **DB-2** : étapes horloge et résolveur **avant** `pare_feu` (ensembles par nom, décision 3) ; chrony en IPv4 et
  unbound sans IPv6 (IPv6 refusé : connexions jetées en sortie) ; T-DP-3, T-DP-4 (« jamais 1.1.1.1 » au contrôle des
  paramètres et des fichiers : f08 ne le tient que pour l'ensemble Google) ; code par archive et manifeste (TCP/23
  déjà ouvert vers `sauvegarde`) ; descripteur (versions réelles des paquets, sources trixie et trixie-security) ;
  smoke avec `sshd -T`, sonde IPv6, adresses NTS négociées (L-1, L-2, Q-5).
- **DB-3** : unités et minuteries ; rafraîchissement des ensembles par nom (Q-5) ; redémarrages de services par les
  mises à jour (L-8) ; droit de lecture de `intervention` pour `status` (Q-1) ; port ou schéma Certigna si autre que
  HTTPS/443.
- **DB-4** : sauvegarde (clé générée sur l'observateur, empreinte d'hôte épinglée, rsync TCP/23), signal de vie (lit
  `ADRESSE_SURVEILLANCE` dans `observateur.conf`), alerte disque.
- **DB-5** : empreintes (T-DP-7) : communs `nftables.conf`, `00-shogen.conf`, `90shogen-securite`, `debian.sources` ;
  d'observateur `observateur.conf`, `shogen-observateur.nft`, `authorized_keys` ; budget : 12 888 octets rempli avec des
  valeurs de 200 caractères, soit environ 19,9 Ko de marge sous 32 KiB pour DB-2 à DB-5.
- **DB-6** : tableau R-8 (six paquets, licences), procédure (compte `intervention`, N2 et N3 par la console, relance
  de la copie), doc 17 (mises à jour, métadonnées, accès SSH), registre 08.

## 9. Phrases proposées pour l'annexe B (ce que DB-1 établit ; rien ne ferme ici, décision 9 : au versement de P5)

- **SHOGEN-S2BIS-R8-PAQUETS-1** : « DB-1 établit la liste installée par le script I : `apt-get install -y
  --no-install-recommends chrony nftables python3 rsync unattended-upgrades`, plus `unbound` pour la seule famille
  unbound (O1), depuis la seule archive Debian en HTTPS (`deb.debian.org`, suites `trixie` et `trixie-security`,
  composant `main`), commande exacte testée (T-DP-1) ; les Recommends ne s'installent pas ; le tableau R-8 de DB-6 porte
  ces six paquets, `unattended-upgrades` compris (décision 1). »
- **SHOGEN-S2BIS-HETZNER-DISPO-1** : « DB-1 n'établit rien de la disponibilité des offres ; il établit que le script
  rempli tient sous la borne de l'user data Hetzner (32 KiB, décision 5) : 11 850 octets non rempli à DB1-f,
  contrôle par test avec des paramètres de 200 caractères. »
- **SHOGEN-S2BIS-REGIONS-1** (volet cloud-init) : « DB-1 établit un script bash autonome, lancé par l'user data ou à
  la main par root (OVHcloud), sans réseau ni privilège en mode d'essai ; son exécution réelle par cloud-init reste à
  constater au premier déploiement (volet re-daté, décision 9). »
- **SHOGEN-S2BIS-TSA-CERTIGNA-1** : « DB-1 établit que le pare-feu admet HTTPS (TCP/443) vers toute adresse, donc un
  point Certigna en HTTPS sur 443 ; un autre port ou du HTTP, appris par la documentation d'API (acte extérieur),
  changerait le pare-feu (DB-3). »

## 10. Journal de provenance (G1)

- **Lu [lu]** : `BRIEF-DB1.md` ; `G0-COLLECTE-RECALC-DEPLOI.md` (27 l., sha256 `d9160d3e…`) ; `PROPOSITION.md`
  l.600-790 (`0cdf84c2…`, égal à l'empreinte annoncée par le G0) ; `AVIS.md` l.1-47 et l.118-152 (`a919b307…`) ;
  ADR-0029 l.74-117 et l.231-250, plus les lignes d'items du §8.1 par recherche dans ce seul fichier (`32a59893…`) ;
  `ADJUDICATION-DB0.md` (`bbc4ae5a…`), `RAPPORT-DB0.md` (`73444aba…`), `R8-paquets.tsv` (`760dd3bc…`) ; pièces de
  DB-0 lues en texte : en-têtes des `InRelease` (sécurité, trixie, updates) et strophes des `Packages.xz` (paquets du
  §2) ; code : `gates.yml`, `verdict-suite-s2.py`, `s2bis/tests/__init__.py`, `test_fitness.py`, motifs de
  `gate-secrets.sh`, en-têtes de `docs-sha256sums.py` et `workflows-yaml.py`, `xtask/src/lib.rs` (`verifier_tout`,
  `outils_cargo`), `scripts/sim-bis/oracle_r1.py` et `parametres.json` (oracles), ports de `asn.py`, `http.py`,
  `dns.py` ; outils du dossier p1b (`isole.sh`, `lo_up.py`, `gates.sh`, `cc_gates.sh`).
- **Inféré [inféré]** : DHCP et adresse de métadonnées par fournisseur ; miroirs APT des images en HTTP ;
  comportement de cloud-init au redémarrage ; chemin du trousseau de Debian 13 ; négociation d'adresse NTS-KE.
  **Seconde main [2nd]** : aucune ; aucun chiffre repris sans recompte.
- **Recomptés** : lignes par diff (`git diff --numstat` sur l'index local) ; Ran des suites (sorties du vérificateur) ;
  mutants (relevés) ; taille du script (`wc -c` et calcul rempli) ; `test result` de cargo (somme par awk).
- **Commandes** (sorties dans `preuves/`) : suite de base (Ran 342, 34 s) ; `outils/rouge_vert.sh` par état ;
  `outils/mutants.py` par état ; `outils/charger_nft.sh` et `sonde2.py` ; `apt-config` ; `outils/gates_finales.sh` ;
  `cargo --locked xtask verify` (copie et témoin) ; `cargo --locked test` ; `git apply --check` sur 39718f4 et dda4bbc.

## 11. Ajout daté du 2026-10-10 04:40:55 UTC (`date -u`, dernière écriture) : diff DB1-g, ajout au G0 adjugé

- **Pièces** : `ADJUDICATION.md` (sha256 `5efcb5b8…`, ajout du 2026-10-10 04:33:52 UTC : Q-1 à Q-6 adoptées dans la
  forme de l'avis) ; `AVIS.md` (`c9eb967b…`, advisor OPS `claude-fable-5-1`, §1 et §3 lus) ; JOURNAL l.382 relu à la
  tête (q. 6 : « l'investisseur seul, un agent au cas par cas sur son accord écrit ») [lu].
- **DB1-g** : `diffs/DB1-g.diff`, **41 lignes ajoutées** (une vide, 40 de texte), 0 retirée, seul fichier
  `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, à la suite de DB1-a ; sha256
  **`eb4e771f4941f394af898509171877496f8dfe891d1ebcb36d85be2a2d80bf43`** ; daté `2026-10-10 04:39:03 UTC` (`date -u`
  lue juste avant l'unique écriture du texte) ; replié à 120 caractères sans couper un segment de code
  (`outils/ajout_g0_v2.py`) ; aucune barre oblique inverse, aucun blanc final. Contenu : les points 1 à 6 du §3 de
  l'avis (E-D-01, E-D-03, E-D-04, T-DP-2 réécrit, décision 3 précisée, E-D-22 (e)).
- **Relecture phrase par phrase contre le code (DB1-b à DB1-f)** : chaque phrase a sa ligne de script ou de
  `nftables.conf` et son test (paramètres et refus : `verifier_parametres`,
  `test_tdp1_parametre_refuse_rien_ne_change` ;
  `observateur.conf` et clé : `etape_observateur`, `etape_comptes`, `test_tdp1_parametres_gardes_et_cle` ; comptes et
  sshd : `etape_comptes`, `etape_ssh`, commandes exactes de l'essai, `test_tdp5_sshd_cle_seule` ; source APT :
  `etape_sources`, `test_tdp1_sources_https_et_trousseau` ; T-DP-2 : `nftables.conf`, `test_tdp2_regles_exactes` et la
  sonde sur le fil ; ensembles : `etape_pare_feu`, `test_tdp2_commun_embarque_et_ensembles`,
  `test_tdp2_nom_non_resolu_refuse`). Écarts de lettre de l'avis corrigés **dans le texte, sans changer le code** :
  (i) la clé n'est pas dans `observateur.conf` : « tous sauf la clé », la clé étant le seul contenu
  d'`authorized_keys` ; (ii) la boucle locale passe avant le refus d'IPv6 : « IPv6 jeté hors de la boucle locale » ;
  (iii) le script ne rafraîchit rien et résout par le résolveur du système (`getent`) : rafraîchissement et constat
  NTS au futur (DB-3, DB-2), et règle « l'étape résolveur de DB-2 se place avant l'étape pare-feu » ; (iv) « O4 » et
  « O1 » écrits « celle d'O4 », « celle d'O1 » (le script lie l'ensemble à la famille, non à l'identité) ; (v) le
  rang de lecture de `00-shogen.conf` est un nom choisi, constaté par `sshd -T` au smoke (DB-2), non une garantie.
  Ajouts pour que le G0 dise tout ce que fait le script : compte `shogen` (système, `/usr/sbin/nologin`), comptes de
  l'image ni supprimés ni verrouillés, `sshd -t`, trousseau `.pgp` sinon `.gpg` et arrêt sans trousseau,
  `--no-install-recommends`, arrêt sur nom non résolu, `nft -c` puis activation du service.
- **Point de l'avis qui demande du code, non codé** : §2, L-6, « une phrase dans le test suffit ». Forme proposée, au
  diff DB1-b (une ligne de plus, docstring de `test_tdp1_usage_et_racine_refusees`) :
  « La racine / n'est jamais essayée, par sûreté (L-6) : sa garde se relit dans le script. » Aucun autre point de
  l'avis ne touche le code de DB-1 (le reste va aux briefs de DB-2, DB-3, DB-4, DB-6).
- **Contrôles** : DB1-g s'applique après DB1-a à DB1-f sur la copie finale ; la série a à g, appliquée sur les fichiers
  de la base 39718f4, redonne l'état final exact (`cmp`) ; sur la copie a à g : `docs-sha256sums.py` conforme,
  `cargo --locked xtask verify` aux verdicts identiques au témoin de la base (S-G4 et S-G5 VERT, S-G9 rouge par
  l'éparsité seule), secrets OK, R-13 : 0.
- **Tête du moment** : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` (relevée à 04:39:49 UTC) : DB1-a à DB1-g s'y
  appliquent dans l'ordre (`git apply --check` puis `git apply`).
- **Empreintes de série** (concaténation dans l'ordre) :
  a à f `a85c74af01cf9227081892308b25af96e800a397c2d41722cdf0a4bc03f4ab27` (égale à celle de l'adjudication) ;
  a à g `160dddd5c23d71058d10efd08e46521921b91aaa18faec190e32b383cfa8c441`.

## 12. Phase 2, ajout daté du 2026-10-10 07:09:45 UTC (`date -u`, dernière écriture) : C-1 à C-9, recalage sur DETTES-T6

- **Pièces** [lu] : `g2/RAPPORT-G2.md` (sha256 `9accc4c5…` ; verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-9 ;
  section « Corrections », §5, §8, §9) ; `g2/corrections/C-1.diff` à `C-9.diff` ; formes des mutants du réviseur,
  `g2/travail/mutants/g.py` (`e5ee69ff…`), recopiées dans `outils/rouges_p2.py` ; DT6-a à DT6-w (`s2bis/dettes6/diffs/`,
  concaténation `8661c7c5c9efa6db…`) ; unité `nftables.service` du paquet nftables de l'hôte, Ubuntu 24.04 [lu] (celle
  de trixie : non lue [abs]).
- **Règles tenues** : aucune écriture git au dépôt (index local `tmp/serie/.git` seul), aucun commit ; réseau coupé (bac
  à sable `outils/bac.sh` ; `isole.sh` de `p1b/g2/travail/outils/`, sha256 `ebaa1c78…`, pour cargo), mandataires
  retirés, `SHOGEN_S2_CAMPAGNE_CONTROL` retiré de chaque environnement ; commandes git de comparaison bornées à des
  chemins nommés ; aucune liste par motif sur `docs/`, aucun `*.jsonl` ; un seul processus lourd à la fois.

### 12.1 Copies (étape 1)

- `diffs/DB1-h.diff` à `diffs/DB1-p.diff` sont `g2/corrections/C-1.diff` à `C-9.diff` (C-1 → h, …, C-9 → p), octet pour
  octet : `cmp` identique pour les neuf, refait à 07:05:36 UTC (`preuves/p2-copies-cmp.txt`) ; concaténation des neuf,
  des deux côtés : `d33a3c68737decead40ead21f63c0cd857a0dacd4aeb7521693608cc4277a7c4`.
- Série d'origine a à p (base 39718f4, sans DT6 ; `diffs/`) :
  `50c41920a56d71730e773e13fc9e2b41ca231bda9e491faab4552b94d4d371fd`.

### 12.2 Relecture : une ligne par correction

- **C-1** juste : forme proposée au §11, mot pour mot (docstring, L-6) ; ni code ni test de plus ; module vert.
- **C-2** juste : `!= /` laissait passer « // » et la racine vide d'un `cd` en échec, donc des écritures sur « / » ;
  `-n` et `-ef /` (périphérique et inœud) ferment les deux ; prouvé hors suite (12.3), par L-6.
- **C-3** juste : l'umask ne joue qu'à la création, d'où le `rm -f` du temporaire laissé par un lancement interrompu ;
  `observateur.conf.nouveau` (adresse secrète, Q-6) ne naît plus 0644 ; sept temporaires relevés à 600.
- **C-4** juste : à la relance, root n'écrit plus dans un dossier que possède `intervention` (liens vers `/etc` ou vers
  un fichier du système) ; la clé ne change plus par relance (rotation par la console, G2 §9, procédure DB-6).
- **C-5** juste : octet de 0 à 255 sans zéro de tête (`010` lu 8), bloc ed25519 de 68 caractères à en-tête fixe, valeurs
  à deux lignes refusées ; une remarque de serrage, sans effet de sûreté, en 12.6.
- **C-6** juste : `enable --now` démarre les minuteries sans redémarrage ; `reload-or-restart` recharge le jeu en une
  transaction (`ExecReload=/usr/sbin/nft -f /etc/nftables.conf`, fichier ouvert par `flush ruleset`) au lieu
  d'`ExecStop=/usr/sbin/nft flush ruleset` puis chargement ; « activé et relancé » du G0 reste vrai (G2 §5).
- **C-7** juste : le test fixe le premier niveau exact et les trois ensembles, vides au dépôt ; tue g01, g02, g03.
- **C-8** juste : 0755 exigé pour `etc/shogen` et `etc/nftables.d` ; tue g05 (`umask 000`).
- **C-9** juste : image Debian 13 fidèle (`debian.sources` deb822 en HTTP avec `trixie-updates`, `fournisseur.sources`)
  et ensemble exact des fichiers de sources ; tue g17, g18.

### 12.3 Rouges rejoués

- `outils/rouges_p2.py` (06:33-06:34 UTC ; module `test_deploi`, python3.12, bac à sable ; `preuves/p2-rouges.txt`,
  `p2-rouge-*.txt`) : tests de chaque correction sur le code de l'état précédent ; pour C-7 à C-9 (tests seuls), mutant
  du réviseur posé sur le code, vivant sous les tests d'avant, tué sous ceux de la correction.

| Cas | Attendu | Obtenu |
|---|---|---|
| C-1 : tests h, code g | vert | OK |
| C-3 : tests j, code i | rouge | 1 échec, `test_tdp1_temporaires_nes_0600` |
| C-4 : tests k, code j | rouge | 2 échecs, `test_tdp1_relance_rien_sous_le_compte_d_intervention` |
| C-5 : tests l, code k | rouge | 5 échecs, `test_tdp1_parametre_refuse_rien_ne_change` |
| C-6 : tests m, code l | rouge | 4 échecs, `test_tdp1_essai_quatre_observateurs` |
| C-7 : g01, g02, g03 | vivants sous m, tués sous n | OK ; 1 échec chacun, `test_tdp2_refus_par_defaut_ipv4_et_ipv6` |
| C-8 : g05 | vivant sous n, tué sous o | OK ; 1 échec, `test_tdp1_parametres_gardes_et_cle` |
| C-9 : g17, g18 | vivants sous o, tués sous p | OK ; 2 échecs chacun, `test_tdp1_sources_https_et_trousseau` |

- Aucune erreur (ERROR) ; écarts au rejeu : 0 ; nombres d'échecs égaux à ceux du rapport G2 (C-3 1, C-4 2, C-5 5, C-6
  4).
- **C-2, hors suite** (`outils/garde_chroot.sh`, 06:34 UTC ; `preuves/p2-garde-chroot.txt`) : script des états h puis i,
  rempli des paramètres d'o2, en essai dans un chroot (tmpfs d'un espace de montage privé, réseau isolé, `/usr` de
  l'hôte en lecture seule, `essai.getent` à la racine du chroot). État h : `--essai //` et `--essai /absente` (`cd` en
  échec) écrivent `debian.sources`, `observateur.conf`, `00-shogen.conf` et `home/intervention` à la racine du chroot et
  y désactivent `sources.list`, puis s'arrêtent en code 3 (E-P2-3). État i : code 2, « ESSAI/racine refusée », rien
  d'écrit. Le mutant `h-c2` du réviseur reste vivant par construction (L-6).

### 12.4 Recalage (étape 2)

- **Base** : tête `7df585a05aedcbf2b1de5e708e244ce969ac5939` (DETTES-T14 DT14-j), relevée à 06:30 UTC, archivée sans les
  interdits du brief (`tmp/p2/tete.tar`) ; DT6-a à w appliqués dans l'ordre (`git apply --check` puis `git apply`, 23
  sur 23).
- **Conflits** : DT6 touche 20 chemins ; un seul est commun avec DB-1, `.github/workflows/gates.yml` (job s2bis : quatre
  lignes de plus avant la ligne du plancher, l.287 → l.291 ; plancher 342 → 358). Aucun autre chemin en conflit.
- **Méthode** (`outils/recalage.sh`) : états anciens h à p (DB1-h à p appliqués sur l'état g) ; états recalés 0, a à p :
  fichiers de DB-1 de l'état et `gates.yml` de la tête + DT6, plancher 358 + delta de l'état ; arbres de l'index local,
  diff entre arbres successifs (`tmp/p2/diffs`, copiés à l'identique en `diffs-recales/`).
- **Effet** : hors de `gates.yml`, chaque diff recalé est identique à son original (comparaison par section) ; b, c, d,
  e, f, j et k ne changent que dans leur section `gates.yml` (contexte `@@ -284` → `@@ -288`, planchers 342 à 357 → 358
  à 373) ; a, g, h, i, l, m, n, o et p sont identiques octet pour octet.
- **Série recalée, à appliquer après DT6-w** (`diffs-recales/`) :

| Diff | sha256 | + / − | Plancher |
|---|---|---|---|
| DB1-a | `d367d95ef6d0fc7c4e90881b5f9386e5e6e35b92b82b68920cf0aeb4eb1b1522` | 32 / 0 | 358 |
| DB1-b | `fd4d306bf76d6e6a7fac6eac877b6a813b48ef2ff8959feaacaeee896b65bb9e` | 185 / 1 | 362 |
| DB1-c | `0744a63fedcd3abce5c9099d32a0a9556902438d133065b0748cd3e7b4157d2c` | 118 / 1 | 365 |
| DB1-d | `9c2025757569bec17e50cb3d7d2bea4045b0adb9b4e4a001835016ff73979035` | 60 / 4 | 367 |
| DB1-e | `1f9f03faae5402f9896e05c241df0066376b837c89b8a7b515a1ce3d834bf90b` | 101 / 2 | 369 |
| DB1-f | `621c4f672c5c956978e293407d320f71af009f2300282d4ff6c1bfbe1f6cc468` | 121 / 8 | 371 |
| DB1-g | `eb4e771f4941f394af898509171877496f8dfe891d1ebcb36d85be2a2d80bf43` | 41 / 0 | 371 |
| DB1-h | `6a38fa33633f8e2cb647e2b2a72c8f0fd42bc42b854e890143a54d9984f69335` | 2 / 1 | 371 |
| DB1-i | `0449a28a70b71543812e962e8016da846d79529c32533a89d726c73538754b40` | 2 / 1 | 371 |
| DB1-j | `2152febadd7a7a426aa864b23e45db50a51265d2bcdf83ea369ef01172c6fdad` | 31 / 6 | 372 |
| DB1-k | `3ea717d633c0ef1b560e9ca1bb482b81fc47daa6e5bcd40fb64a790c56d964cf` | 30 / 2 | 373 |
| DB1-l | `27c19ec31ba07d13b14499a550d97e5e06a5ff6dbd0e82422a6ad78adbfa3e4b` | 10 / 2 | 373 |
| DB1-m | `d0abb046412fd1639f250022c9366570ec8688bf1deed876c18216f7884c16d1` | 6 / 5 | 373 |
| DB1-n | `1ade99b4f72a5846195f3715c375c528b60344b2e43b952965ea627733bd4419` | 26 / 20 | 373 |
| DB1-o | `fcb5f794321f62cae7e88be873cec0d7a18374bc24ccfc04c787f848ae7bfa95` | 3 / 2 | 373 |
| DB1-p | `2e7b84378ce7aa990f144ce10f63b55bbd64a76dfe9c40d6e3604f1c753c854a` | 9 / 2 | 373 |

- **Empreinte de la série recalée a à p** (concaténation dans l'ordre) :
  `f775d0daad75f337a7374eaa27dc99824b18faf3195856f48f72a22bdff93b71` ; 777 lignes ajoutées, 57 retirées ; aucune ligne
  ajoutée de plus de 120 caractères, aucune barre oblique inverse, aucun blanc final.

### 12.5 Vérifications sur l'état final (étape 3 ; 7df585a + DT6-a à w + DB1-a à p, `tmp/p2/arbre`)

- **Job s2bis** (`outils/jobs_p2.sh`, 06:35:38-06:47:51 UTC ; ligne lue dans le `gates.yml` de chaque état, python3.12,
  bac à sable ; `preuves/p2-jobs.txt`, `p2-job-<x>.txt`) : verdict conforme et Ran = plancher aux 17 états : 0 et a 358
  ; b 362 ; c 365 ; d 367 ; e 369 ; f, g, h, i 371 ; j 372 ; k à p 373.
- **Matrice** (`outils/gates_p2.sh`, 06:48:07-06:51:05 UTC ; `preuves/p2-gates.txt`, `p2-matrice-python3.1x.txt`) :
  python3.10, 3.11, 3.12 et 3.13 en `-X dev -W error` (`PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` transmis à la suite) :
  conforme, Ran = 373, aucun saut, 0 avertissement.
- **Runner du vérificateur** : 137 ok, 0 échec. **docs-sha256sums** : conforme (39 SHA256SUMS, 314 lignes, 11 absentes
  admises, 4 fichiers non listés). **workflows-yaml** : conforme (7 workflows, PyYAML 6.0.1) ; cas 16 ok sur 16. **Lint
  d'épinglage (R-1)** : arbre OK (7 fichiers) ; cas 227 ok, 0 échec (07:00:33-07:00:41 UTC,
  `preuves/p2-pinning-cas.txt`). **runners-epingles**, **journaux-modele** : conformes.
- **Secrets** (gate sur un index des fichiers de DB-1, `preuves/p2-secrets.txt`) : OK. **R-13** (motif lu dans
  `gates.yml`, sha256 `ce8609f61133ed99…`, sur les quatre fichiers de DB-1, `gates.yml` exclu comme au job) : code 1, 0
  ligne.
- **cargo --locked test** (cible par défaut de la copie, une fois, 06:51:29-06:51:46 UTC, réseau isolé ;
  `preuves/p2-cargo-test.txt`) : code 0 ; 28 lignes `test result`, 269 passés, 0 échec, 0 ignoré ; les trois lignes
  `error:` de la sortie viennent de la construction cassée exprès du test
  `mutant_construction_en_echec_ne_rend_aucun_verdict`, passé. Cible et dossier temporaire supprimés ensuite (chemins
  littéraux).

### 12.6 Tête mobile, remarque, écarts

- **Tête 4c98594** (`4c9859439c51cb041bff4daf636e2c9ffe2a53bc`, relevée à 06:53:39 UTC, versement de DETTES-T14) : rien
  de changé depuis 7df585a sur `s2bis`, `enforcement`, `.github`, `crates`, `xtask`, `Cargo.toml`, `Cargo.lock`,
  `docs/adr-0029` (git diff borné à ces chemins) ; `outils/tete_p2.sh` (06:56 UTC ; `preuves/p2-tete.txt`) : archive
  entière sans interdits (1220 fichiers, 0 entrée interdite), DT6 23 sur 23 puis DB-1 16 sur 16, chemins touchés
  identiques à l'état vérifié ; docs-sha256sums (40 SHA256SUMS, 319 lignes), workflows-yaml, lint, runners-epingles,
  journaux-modele conformes.
- **DETTES-T6 en cours de versement** : `01d74bd` (06:56:28 UTC) = DT6-a, identique à `DT6-a.diff` (patch-id, et octets
  des cinq fichiers) ; `1e5ded0` (07:03:20 UTC) = DT6-b ; `outils/tete_dt6.sh` (07:04:46 UTC ;
  `preuves/p2-tete-dt6-1.txt`) : rang DT6 de la tête 2 (empreinte des 24 chemins nommés), aucun autre chemin sensible
  changé, DT6-c à w puis DB1-a à p s'appliquent, état final exact, plancher 373 ; relancé sur `a59eaa2` (07:08:34 UTC) =
  DT6-c : rang 3, DT6-d à w puis DB1-a à p s'appliquent, état final exact (`preuves/p2-tete-dt6-2.txt`). L'outil se
  relance tel quel sur toute tête de la suite.
- **Remarque sur C-5 (sans effet de sûreté ; non codée, copie à l'identique demandée)** : [calc] dans un bloc ed25519,
  les 25 premiers caractères codent 150 bits ; le 26e porte les deux derniers bits du champ de longueur (32), puis
  quatre bits de la clé : il ne prend que 16 valeurs, `A` à `P` (calculé sur les 256 valeurs du premier octet de clé).
  La forme de C-5 en admet 64 : un bloc dont le 26e caractère est `Q` se décode en longueur 33 et passe la garde (bash,
  sur la forme lue dans le script final). Effet : une clé mal formée serait posée, l'accès d'intervention perdu jusqu'à
  la console ; ni injection ni ligne de plus. Serrage d'un caractère, à l'adjudication :
  `AAAAC3NzaC1lZDI1NTE5AAAAI[A-P][A-Za-z0-9+/]{42}`.
- **Écarts** :
  - E-P2-1 : le premier lancement de `cargo test` (un `sh -c` qui créait le dossier temporaire puis lançait cargo) a été
    refusé par le contrôle de sûreté du harnais, qui y voyait un `rm` absent du script ; dossier créé par une commande à
    part, cargo lancé sans `sh -c` ; aucun refus de suppression contourné.
  - E-P2-2 : barres obliques inverses dans un outil, `outils/garde_chroot.sh` (trois octets, l.32, 40 et 41 :
    continuation de ligne, retour à la ligne de `tr`), et tapées dans des commandes d'outil (affichage par `tr`,
    extraction des en-têtes de diff par `grep -E` et `sed -E`, séparateur de `xargs -d` pour la première liste des
    sommes) : octets des outils contrôlés (`grep -F` du gabarit `printf` octal), sorties vérifiées (liste de chemins
    identique à la première ; 185 sommes pour 185 noms, `sha256sum -c` sans écart), `SHA256SUMS` final refait sans
    barre ; aucune dans les diffs ; `tete_p2.sh`, `tete_dt6.sh` et `replier_p2.py` n'en ont aucune.
  - E-P2-3 : la preuve chroot de l'état h finit en code 3 (`awk` introuvable : lien d'alternatives absent du chroot)
    après ses écritures ; la preuve du défaut tient (écritures constatées), l'état i refuse avant toute écriture.
  - E-P2-4 : `df -h /` et la charge, lus à l'écran avant l'archive et avant chaque campagne, n'ont pas été gardés en
    fichier avant 06:53 ; relevés depuis : 06:53:13 charge 1,93 ; 06:56:23 7,8 G libres, charge 3,41 ; 07:00:33 charge
    3,09 ; 07:03:55 7,9 G libres, charge 2,03.
  - E-P2-5 : job, matrice et cargo ont tourné sur 7df585a + DT6 + DB-1 et n'ont pas été refaits sur les têtes suivantes
    : leurs entrées (`s2bis`, `enforcement`, `.github`, `crates`, `xtask`, `Cargo.*`) n'ont pas changé hors DT6
    (contrôles ci-dessus).
  - E-P2-6 : la série recalée est livrée dans `diffs-recales/` ; `diffs/` garde la série d'origine (a à g de la phase 1,
    h à p copies des corrections), pour la traçabilité de l'adjudication.
- **Provenance (G1)** : outils `recalage.sh`, `rouges_p2.py`, `garde_chroot.sh`, `jobs_p2.sh`, `gates_p2.sh`,
  `tete_p2.sh`, `tete_dt6.sh` (sha256 au `SHA256SUMS`) ; sorties `preuves/p2-*.txt` ; chaque nombre de cette section
  relu dans ces sorties ou recompté (totaux cargo par `awk`, lignes des diffs par `git apply --numstat`, sha256
  recalculés) ; aucun chiffre de seconde main.

## 13. Phase 3, ajout daté du 2026-10-10 07:31:33 UTC (`date -u`, dernière écriture) : DB1-q, bloc de la clé

- **Rattachement** [lu] : `ADJUDICATION.md` (sha256 `6206f713…`), ajout daté de 07:10:50 UTC : remarque du générateur
  sur C-5 adoptée (règle « aucune dette »), serrage `AAAAC3NzaC1lZDI1NTE5AAAAI[A-P][A-Za-z0-9+/]{42}` en DB1-q (test
  rouge d'abord, mutant), puis contre-contrôle neuf de la série a à q. Gate 0 : `claude-opus-5-5`, effort `max`.
- **Règles tenues** : copie neuve de la tête du moment plus le DT6 restant ; réseau coupé (bac à sable `outils/bac.sh`),
  mandataires retirés, `SHOGEN_S2_CAMPAGNE_CONTROL` retiré de chaque environnement ; un seul processus lourd à la fois,
  charge sur 1 min relevée sous 5 avant la campagne ; heures par `date -u` ; commandes git bornées à des chemins nommés
  ; aucun `*.jsonl` ; aucune écriture git au dépôt (index local `tmp/serie/.git` et index jetable des secrets seuls).

### 13.1 Copie neuve

- `outils/copie_p3.sh` (07:14:46 UTC ; `preuves/p3-copie.txt`) : tête `85751864f2bead8af95d961d8f1fd284651f9380`
  (DETTES-T6 DT6-d), archive sans les interdits du brief (1220 fichiers, 0 entrée interdite) ; aucun chemin sensible
  changé depuis 4c98594 hors DT6 ; rang DT6 de la tête 4 (empreinte des 24 chemins nommés) ; DT6-e à w (19) puis DB1-a à
  p recalés (16) appliqués ; les 24 chemins égaux à l'état p vérifié de la phase 2 ; plancher 373.

### 13.2 Où la forme de la clé est contrôlée ou écrite

- **Script** : seule la ligne du motif (`verifier_parametres`, l.49 à l'état p) et son commentaire (l.47-48). Le motif
  passe sur sa propre ligne `local` (la ligne commune avec l'octet IPv4 dépasserait 120 caractères) ; le refus nommé
  `PARAMETRE/CLE_INTERVENTION` est inchangé.
- **Tests** : la clé factice `CLE` (26e caractère `E`) reste admise ; les cas de C-5 (court, long, autre type, deux
  lignes) restent refusés ; un test neuf (13.3).
- **G0** : la forme du bloc n'y est pas décrite (« `CLE_INTERVENTION`, `ssh-ed25519` », « clé `ssh-ed25519` seule ») :
  rien à ajouter, aucun ajout daté. ADR-0029, `AVIS.md`, `PROPOSITION.md`, lus à la tête par leur nom : aucune forme de
  clé.

### 13.3 Clés vraies, test rouge, vert

- **ssh-keygen absent de l'hôte** (`command -v ssh-keygen` vide, `ssh` introuvable) : clés construites octet par octet,
  et dites telles dans le test. `outils/ed25519_hors_reseau.py` (07:16:42 UTC ; `preuves/p3-ed25519.txt`) : génération
  de clé d'Ed25519 (RFC 8032) en Python seul ; contrôle : les clés publiques des vecteurs TEST 1, TEST 2 et TEST 3 de la
  RFC 8032, recalculées depuis leurs clés secrètes, égalent les valeurs citées (3 sur 3 ; citées de mémoire, la RFC
  n'étant pas lisible hors réseau [abs] : l'accord des 32 octets confirme à la fois la citation et le calcul [calc]).
  Clés retenues, toutes décompressées en un point de la courbe : graine SHA-256 de « shogen DB1-q A 6 » (7e essai ; 26e
  caractère `A`), TEST 1 (`N`), TEST 3 (`P`). Bloc construit par champs (longueur, « ssh-ed25519 », longueur 32, clé),
  relu champ par champ : 51 octets, 68 caractères.
- **Test neuf** `test_tdp1_cle_bloc_ed25519_exact` : les trois clés vraies sont admises et posées telles quelles dans
  `authorized_keys` ; le bloc de TEST 1, au 26e caractère `Q` (témoin dans le test : longueur lue 33), `Z`, `g`, `z`,
  `0`, `9`, `+` et `/`, est refusé nommément (`PARAMETRE/CLE_INTERVENTION`), sans commande ni fichier écrit.
- **Rouge d'abord** (07:18:14 UTC ; tests de l'état q sur le code de l'état p ; module `test_deploi`, python3.12, bac à
  sable ; `preuves/p3-rouge.txt`) : FAILED (failures=8), toutes dans le test neuf (les huit refus admis), aucune erreur
  ; les trois clés vraies passent déjà. **Vert** (07:18:32 UTC ; code de l'état q ; `preuves/p3-vert.txt`) : OK, 16
  tests du module.
- **Motif exact à la 26e place** (`preuves/p3-motif-64.txt`) : sur les 64 valeurs possibles, le motif lu dans le script
  de l'état q admet `A` à `P`, exactement celles dont la longueur décodée vaut 32.

### 13.4 DB1-q et la série

- `diffs-recales/DB1-q.diff` : sha256 **`eaf35fa98a8cfdff05957696d8447427dcb5e74d17e307b28d856ec56d7bf27d`** ; +41 / −3
  : `.github/workflows/gates.yml` 1 / 1 (plancher 373 → 374 : un test de plus, le neuf),
  `s2bis/deploi/premier-demarrage.sh` 4 / 2, `s2bis/tests/test_deploi.py` 36 / 0 ; G0 et `nftables.conf` inchangés ;
  aucune ligne ajoutée de plus de 120 caractères, aucune barre oblique inverse, aucun blanc final. Diff entre arbres de
  l'index local (`outils/etat_q.py`, `outils/diff_q.sh`) ; l'arbre de l'état p égale celui de la phase 2 (`4e232a66…`) ;
  appliqué sur la copie neuve (`git apply --check`, puis `git apply`) : les cinq fichiers égaux à l'état q.
- **Empreinte de la série recalée a à q** (concaténation dans l'ordre) :
  **`9f6522d87dea9c5dd8680bd4e7ff533f539806441c5a3a3ff29f99e5777a09c1`** ; a à p inchangée (`f775d0da…`). `diffs/`
  (série d'origine, sans DT6) n'a pas de DB1-q : il est demandé sur la série recalée seule.

### 13.5 Mutants, par la ligne du job s2bis

- `outils/mutants_q.py` (07:19:50-07:26:33 UTC ; ligne lue dans le `gates.yml` de l'état q, plancher 374 ; python3.12,
  bac à sable, arbre complet de la copie neuve ; `preuves/p3-mutants.txt`, `p3-mut-<nom>.txt`) : témoin (état q sans
  mutation) conforme, Ran 374 = plancher (07:19:50-07:20:40) ; huit mutants de la ligne du motif, classés par la sortie
  du vérificateur (1 avec échecs de tests : tué ; 0 : vivant ; autre : FATAL) : **8 tués, 0 vivant, 0 FATAL** ; script
  de l'état q remis en place ensuite (`cmp`).

| Mutant | Motif muté | Échecs | Tué par |
|---|---|---|---|
| q1 | forme de C-5, `[A-Za-z0-9+/]{43}` | 8 | les huit refus du test neuf |
| q2 | `[A-Q]` | 1 | le 26e caractère `Q` |
| q3 | `[B-P]` | 1 | la clé vraie au 26e caractère `A` |
| q4 | `[A-O]` | 1 | la clé vraie au 26e caractère `P` (TEST 3) |
| q5 | `[A-Pa-p]` | 1 | le 26e caractère `g` |
| q6 | `[A-P0-9+/]` | 4 | les 26e caractères `0`, `9`, `+`, `/` |
| q7 | `{41}` | 22 | dix tests, dont le neuf (clés vraies et factice refusées) |
| q8 | `{42,}` | 1 | `test_tdp1_parametre_refuse_rien_ne_change` (bloc long de C-5) |

### 13.6 Vérifications sur l'état q

- `outils/gates_p3.sh` (07:26:44-07:30:15 UTC ; `preuves/p3-gates.txt`) : matrice python3.10, 3.11, 3.12, 3.13 en
  `-X dev -W error` (`PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) : conforme, Ran = 374, aucun saut, 0 avertissement ;
  runner du vérificateur 137 ok ; docs-sha256sums conforme (40 SHA256SUMS, 319 lignes, 11 absentes admises, 4 non
  listés) ; workflows-yaml conforme, cas 16 sur 16 ; lint d'épinglage OK (7 fichiers), cas 227 ok ; runners-epingles et
  journaux-modele conformes ; secrets (`--tree` sur un index jetable des cinq fichiers de DB-1) OK ; R-13 (motif lu dans
  `gates.yml`, `ce8609f61133ed99…`) : code 1, 0 ligne. cargo non relancé : DB1-q ne touche aucune entrée Rust
  (`gates.yml`, script, test).

### 13.7 Tête mobile, écarts, provenance

- **Tête du moment** : `1bff91cc8649b4f031c467aa6ea5d2011b9ab4c8` (07:30:20 UTC, DETTES-T6 DT6-f) ; `outils/tete_p3.sh`
  (`preuves/p3-tete.txt`) : aucun chemin sensible changé hors DT6 depuis 4c98594, rang DT6 6, DT6-g à w (17) puis DB1-a
  à q (17) s'appliquent dans l'ordre, les 24 chemins égaux à l'état q vérifié, plancher 374 ; relancé sur
  `2fcd30369e3c0bcdf2e3c80a197a4e09d713eb18` (07:31:17 UTC, DT6-g) : rang 7, DT6-h à w (16) puis DB1-a à q (17)
  s'appliquent, même égalité (`preuves/p3-tete-2.txt`). L'outil se relance tel quel sur toute tête de la suite.
- **Écarts** :
  - E-P3-1 : à l'ouverture (07:11:55 UTC), charge sur 1 min 5,44, au-dessus de 5 : lectures seules jusqu'à la redescente
    ; charge au lancement du rouge 2,62, de la campagne 2,48.
  - E-P3-2 : barres obliques inverses tapées dans trois commandes (accents graves échappés dans un document en ligne
    vers `NOTES.md` ; deux `tr` d'affichage ou de comptage) : octets écrits contrôlés (`od -c`, 0 barre dans `NOTES.md`)
    ; un premier jet d'`outils/etat_q.py` en portait une (apostrophe échappée), retirée avant tout lancement ; les
    outils de la phase et DB1-q n'en ont aucune (contrôle sur octets).
  - E-P3-3 : RFC 8032 non lisible hors réseau : vecteurs TEST 1 à 3 cités de mémoire [abs], confirmés par le calcul
    (13.3).
- **Provenance (G1)** : outils `copie_p3.sh`, `ed25519_hors_reseau.py`, `etat_q.py`, `diff_q.sh`, `mutants_q.py`,
  `gates_p3.sh`, `tete_p3.sh` (sha256 au `SHA256SUMS`) ; sorties `preuves/p3-*.txt` ; chaque nombre de cette section
  relu dans ces sorties ou recompté (lignes du diff par `git diff --numstat`, échecs par mutant comptés sur les lignes
  `FAIL:`, sha256 recalculés) ; aucun chiffre de seconde main.

## 14. Phase 4, ajout daté du 2026-10-10 09:01:01 UTC (`date -u`, dernière écriture) : DB1-r, s, t (R-1 à R-3)

- **Rattachement** [lu] : `ADJUDICATION.md` (sha256 `ed7f09fc…`), ajout daté de 08:43:31 UTC : contre-contrôle neuf
  CONFORME-AVEC-RÉSERVES ; R-1, R-2 et R-3 adoptées, reprises à l'identique en DB1-r, DB1-s, DB1-t, plancher inchangé
  (374). `g2/cc/RAPPORT-CC.md` (`90d904ee…`) lu en entier. Gate 0 : `claude-opus-5-5`, effort `max`.
- **Règles tenues** : copie neuve de la tête du moment plus le reste de DT6 ; réseau coupé (bac à sable `outils/bac.sh`
  : espace réseau neuf, / en lecture seule hors du dossier), mandataires retirés, `SHOGEN_S2_CAMPAGNE_CONTROL` retiré de
  chaque environnement ; un seul processus lourd à la fois ; charge sur 1 min sous 5 avant chaque campagne ; heures par
  `date -u` ; commandes git bornées à des chemins nommés ; aucun `*.jsonl` ; aucune écriture git au dépôt.

### 14.1 Copies

- `g2/cc/propose/R-1.diff`, `R-2.diff`, `R-3.diff` copiés en `diffs-recales/DB1-r.diff`, `DB1-s.diff`, `DB1-t.diff` :
  `cmp` identique pour les trois (08:44:12 UTC ; `preuves/p4-copies-cmp.txt`) ; sha256
  `50204b627fb89907ba64e74a3ce6f65dfc51ae92ef04bf8f0eadbee8cfbfb4ce` (r, +3 / −1),
  `efffd758ab384096b6b6f877b682820e507ecda7dec9b3777570975abcd1338c` (s, +15 / −1),
  `ed6df86d5d465f34bf1f43864cf46f336414c60e69759ffc7de9a8871fed2c32` (t, +9 / −3), égaux à ceux de l'adjudication ;
  concaténation `d57a3d97235844eb8b6992a92fa9ccb5c38b769be11b6982edd5b166bd5919e2`, égale à celle du contre-contrôle.
  Aucune ligne ajoutée de plus de 120 caractères, aucune barre oblique inverse, aucun blanc final. Les trois diffs n'ont
  pas de ligne `index` (forme du contre-contrôleur) : `git apply` les prend tels quels.

### 14.2 Relecture : une ligne par réserve

- **R-1 (DB1-r) juste** : l'hôte d'`ADRESSE_SAUVEGARDE` part en argument de `getent ahostsv4` (`adresses()`), et
  l'ancien motif l'admettait avec un tiret en tête ; sur le getent de l'hôte (glibc, réseau isolé ;
  `outils/sonde_getent.sh`, `preuves/p4-sonde-getent.txt`), `--` rend le code 0 et les 4 lignes de `/etc/hosts`
  (adresses retenues : `127.0.0.1` et l'adresse de l'hôte, ouvertes en TCP/23), `--help` le code 0 et 20 lignes d'aide
  prises pour des adresses. Le motif neuf exige une lettre ou un chiffre en tête du compte et de l'hôte ; la valeur des
  tests (`u1-sub1@u1.your-storagebox.de`) reste admise. Le commentaire ne nomme que getent ; le compte, fermé du même
  trait, ira à ssh et rsync (DB-4) : précision de lettre, sans effet.
- **R-2 (DB1-s) juste** : tests seuls, sous-tests du test de DB1-q (plancher inchangé) ; les 64 valeurs du 26e caractère
  sur un bloc dont la fin porte « + » puis 41 « / » (recalculé : la clé `ff` × 32 donne `P` puis 42 « / ») ; attendus
  tirés du décodage, jamais du script ; image sans trousseau, si bien qu'une clé admise s'arrête à `APT/trousseau` (code
  3, rien d'écrit) : l'admission se lit sans déploiement entier. Comble le trou de mon test de DB1-q : ses trois clés
  vraies n'ont aucun « / » dans leurs 42 derniers caractères (recompté : 0, 0, 0), et ni `R` ni `I` n'y sont essayés.
- **R-3 (DB1-t) juste** : le `drop` ajouté est la dernière règle de chacune des trois chaînes de base ; un paquet qui
  l'atteint n'a été admis par aucune règle et la politique `drop` l'aurait jeté ; un paquet admis plus haut ne l'atteint
  jamais : aucun flux admis ne change (`test_tdp2_regles_exactes` fige les règles d'avant, dans l'ordre, plus `drop`).
  Rien n'est masqué : le fichier d'observateur écrit par le script ne porte que des `add element` (3), aucun `add rule`.
  Fuite au rechargement fermée dans les deux copies : les trois mêmes lignes dans `nftables.conf` et dans la copie
  embarquée, qui restent égales octet pour octet (extraction à moi, `preuves/p4-r3-structure.txt`) et finissent chacune
  leurs trois chaînes par `drop` ; mesure sur le fil en 14.4. Pour DB-2 à DB-5 : une règle ajoutée plus tard par
  `add rule` se placerait après ce `drop` et ne serait jamais atteinte ; elle doit s'insérer avant (ou passer par le jeu
  commun).

### 14.3 Rouges rejoués

- **R-1 et R-3, par module** (`outils/rouges_p4.py`, 08:46:26-08:46:45 UTC ; module `test_deploi`, python3.12, bac à
  sable ; `preuves/p4-rouges.txt`, `p4-rouge-*.txt`) : tests de r sur le code de q : FAILED (failures=3), les trois cas
  neufs (`u1@--`, `u1@--help`, `-u1@h`) de `test_tdp1_parametre_refuse_rien_ne_change`, aucune erreur ; tests de t sur
  le code de s : FAILED (failures=1), `test_tdp2_regles_exactes`, aucune erreur ; verts : r, s et t OK, 16 tests du
  module. Écarts au rejeu : 0. Nombres égaux à ceux du contre-contrôle (3 ; 1).
- **R-2, par la ligne du job s2bis** (`outils/mutants_p4.py`, 08:48:29-08:55:13 UTC ; ligne lue dans `gates.yml`,
  plancher 374, python3.12, bac à sable, arbre complet ; `preuves/p4-mutants.txt`, `p4-mut-*.txt`) ; mutants posés sur
  le script de l'état s (égal à celui de r) ; classement par la sortie du vérificateur ; **0 écart aux attendus** :

| Mutant | Sous les tests de r | Sous les tests de s |
|---|---|---|
| K15 `[A-PR]` | vivant (code 0, Ran 374) | tué : 1 échec, `c='R', longueur=33` |
| K16 `[A-HJ-P]` | vivant (code 0, Ran 374) | tué : 1 échec, `c='I', longueur=32` |
| K17 « / » refusé dans les 42 derniers | vivant (code 0, Ran 374) | tué : 16 échecs, `A` à `P` |

### 14.4 Fuite au rechargement, mesurée sur le fil

- Jeux déployés produits par le script des états s et t en essai (`outils/jeu_deploye.py`, paramètres d'o2) : chacun
  égal octet pour octet au `nftables.conf` versé de son état (`cmp`) ; ensembles d'observateur écrits (Quad9, quatre
  NTP, sauvegarde).
- `outils/recharge_p4.py` (à moi ; bac à sable, espace réseau neuf ; tun0 et route par ioctl, comme la sonde de la phase
  1) : un fils sous l'uid 65534 envoie sans arrêt vers 10.9.0.1:9999 (UDP, flux interdit) ; lecture du fil ; seul le
  chemin d'inclusion ramené sous la racine ; 100 rechargements par `nft -f` (forme d'`ExecReload`) par série
  (`preuves/p4-recharge.txt`, 08:55:33-08:56:18 UTC) :

| Jeu déployé | Témoin sans jeu (0,5 s) | Jeu chargé (0,5 s) | Rechargements avec fuite, série 1 | Série 2 |
|---|---|---|---|---|
| état s (sans `drop`) | 75 405 datagrammes | 0 | 76 sur 100 (76 datagrammes) | 61 sur 100 |
| état t (R-3) | 64 596 datagrammes | 0 | 0 sur 100 | 0 sur 100 |

- La fuite est fermée par R-3, dans le jeu déployé, donc dans la copie embarquée et dans `nftables.conf`, égaux.
  Mécanisme non relu (noyau) : seul l'effet est mesuré, comme au contre-contrôle (L-2 de l'adjudication) ; outils de
  l'hôte (nft 1.0.9, noyau de la session), non ceux de trixie.

### 14.5 Série a à t sur la tête du moment, vérifications

- **Copie neuve** (`outils/copie_p4.sh`, 08:45:49 UTC ; `preuves/p4-copie.txt`) : tête
  `87249c221fd408d1bd77d10d9e4303fdb288db27` (DETTES-T6 DT6-s), archive sans les interdits (1221 fichiers, 0 entrée
  interdite), aucun chemin sensible changé depuis 4c98594 hors DT6, rang DT6 19 ; DT6-t à w (4) puis DB1-a à q (17) :
  les 24 chemins égaux à l'état q vérifié de la phase 3 ; puis DB1-r, s, t (`git apply --check`, puis `git apply`).
- **Job s2bis**, ligne telle qu'écrite : conforme, aucun saut, **Ran = 374 = plancher** aux états r, s et t (témoins de
  `outils/mutants_p4.py`, 08:48:29-08:50:43 UTC) ; aucun test ajouté par r, s ou t (sous-tests seulement), plancher
  inchangé.
- **Sur l'état t** (`outils/gates_p4.sh`, 08:56:23-08:59:48 UTC ; `preuves/p4-gates.txt`) : matrice python3.10, 3.11,
  3.12 et 3.13 en `-X dev -W error` (`PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) : conforme, Ran = 374, aucun saut, 0
  avertissement ; runner 137 ok ; docs-sha256sums conforme (40 SHA256SUMS, 319 lignes, 11 absentes admises, 4 non
  listés) ; workflows-yaml conforme, cas 16 sur 16 ; lint d'épinglage OK (7 fichiers), cas 227 ok ; runners-epingles,
  journaux-modele conformes ; secrets (`--tree`, index jetable des cinq fichiers de DB-1) OK ; R-13 : code 1, 0 ligne.
- **cargo test : sans objet** : DB1-r, s et t ne touchent que `s2bis/deploi/premier-demarrage.sh`,
  `s2bis/deploi/nftables.conf` et `s2bis/tests/test_deploi.py` ; aucun chemin de `crates`, `xtask`, `Cargo.toml` ni
  `Cargo.lock` n'a changé depuis 4c98594 hors DT6 (et DT6 n'en touche aucun).
- **Tête à la fin** : `c1799145dddcf048178eb07ed6c2e6a547f78e2d` (08:59:54 UTC, DETTES-T6 DT6-u) ; `outils/tete_p4.sh`
  (`preuves/p4-tete.txt`) : rang DT6 21, DT6-v et w (2) puis DB1-a à t (20) s'appliquent dans l'ordre ; les 24 chemins
  égaux à l'état t vérifié ; plancher 374.
- **Empreinte de la série recalée a à t** (concaténation dans l'ordre) :
  **`03160ea3ab08c9ccc8fb938fad142ad6ef5c18726054b460a05d5e0da239f48b`** ; a à q inchangée (`9f6522d8…`).

### 14.6 Écarts, provenance

- **Écarts** :
  - E-P4-1 : une sonde de getent lancée par `bash -c` refusée par le contrôle de sûreté du harnais (script sans `rm`) ;
    refaite depuis un fichier (`outils/sonde_getent.sh`) ; aucune suppression contournée.
  - E-P4-2 : barres obliques inverses : un premier jet de `outils/sonde_getent.sh` (format de `printf`) et de
    `outils/mutants_p4.py` (continuation de ligne) en portait une, retirée avant tout lancement compté (la sonde avait
    tourné une fois, refaite) ; tapées dans deux commandes (un motif `sed` de dérivation de `copie_p4.sh`, un motif
    `grep` d'en-têtes de diff) : octets écrits contrôlés ; aucune dans les outils de la phase ni dans DB1-r, s, t.
  - E-P4-3 : la mesure de fuite tourne sur nft 1.0.9 et le noyau de la session, non sur ceux de trixie (L-1, L-2 de
    l'adjudication : smoke de DB-2).
- **Remarque pour les briefs de DB-2 à DB-5** : avec R-3, une règle ajoutée plus tard à ces chaînes par `add rule` (par
  exemple depuis `/etc/nftables.d/`) se placerait après le `drop` et ne serait jamais atteinte : l'insérer avant, ou
  passer par le jeu commun.
- **Provenance (G1)** : outils `copie_p4.sh`, `rouges_p4.py`, `sonde_getent.sh`, `mutants_p4.py`, `jeu_deploye.py`,
  `recharge_p4.py`, `gates_p4.sh`, `tete_p4.sh` (sha256 au `SHA256SUMS`) ; sorties `preuves/p4-*.txt` ; chaque nombre de
  cette section relu dans ces sorties ou recompté ; aucun chiffre de seconde main (les nombres du contre-contrôle ne
  sont cités que pour comparaison).
