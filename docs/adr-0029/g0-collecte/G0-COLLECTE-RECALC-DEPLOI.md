# G0 des lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS (S2-bis)

Adjugé par l'orchestrateur le 2026-10-04 17:03:38 UTC (heure produite par le script). Rattachement : ADR-0029 révision 3, acceptée ; G0 de vague
`docs/adr-0029/G0-lots-S2BIS.md`. Pièces : proposition du rédacteur (`docs/adr-0029/g0-collecte/PROPOSITION.md`, worker
`claude-opus-5-5`, sha256 `0cdf84c2…bfd0`, 45 questions techniques) ; avis de l'advisor (`docs/adr-0029/g0-collecte/AVIS.md`,
`claude-fable-5-1` : 37 recommandations du rédacteur adoptées, 8 modifiées).

## Adjudications
1. **La proposition est le contenu de ce G0** (périmètre, exigences numérotées, sous-lots, tests, critères de sortie, actes de
   l'investisseur), **corrigée par l'avis** : pour chacune des 45 questions, la recommandation de l'avis s'applique telle qu'écrite
   (§2 et §3 de l'avis), y compris ses huit modifications (Q-C-02, Q-C-05, Q-C-06, Q-D-01, Q-D-03, Q-D-05, Q-R-13, Q-G-04).
2. **Écarts à l'ADR** adoptés, portés par l'ajout daté du même jour à l'ADR-0029 (§6) : archive du seul paquet `s2bis/` avec manifeste
   par fichier au lieu d'un clone (l.241) ; réplication par l'espace de sauvegarde seul et rétention locale de 7 jours (l.245) ; règle
   D-2 reformulée « plus de 5 s après son instant planifié » (l.107) ; précisions du pare-feu (l.241) ; sens de « réutilisé » (l.231) ;
   taille et jalons (l.308, l.393).
3. **Ordre** (Q-G-02, amendement du G0 de vague) : P1 (collecteur, noyau) et RB-0 à RB-6 commencent maintenant ; RB-7 (règle R1-2)
   attend la clôture de SIM-NIVEAU-BIS, ou se rouvre par décision écrite.
4. **Jalons** (Q-G-04) : la préparation passe d'environ 8 semaines à 11-12 semaines (lots 3 à 6 à S+7/8, sceau à S+10/11) ; budget
   inchangé (les serveurs ne se louent qu'au déploiement). Information de l'investisseur et choix « carte réduite » : question de valeur,
   posée par l'orchestrateur.
5. Chaque partie (P1 à P5) reçoit une relecture G2 neuve et un accord de l'investisseur ; chaque sous-lot ≤ 200 lignes ajoutées.

*Ajout daté du 2026-10-05 04:38:22 UTC (heure produite par le script d'écriture), point 5* : par décision de l'investisseur (message en session, heure lue 2026-10-05 04:09:04 UTC : « demande aux advisors. tout en gardant le but de tout ton travail »), l'accord de chaque partie est rendu par un advisor (`claude-fable-5-1`, effort `medium`, R-26), sur la pièce de clôture de la partie (relecture G2 neuve, contre-contrôle, items ouverts) et au regard du but du projet : faire de Shōgen un standard institutionnel vendable, sans baisse de qualité. Restent à l'investisseur les questions de valeur : dépense, calendrier annoncé, déclaration publique, et tout ce qui touche Pocket.

*Ajout daté du 2026-10-05 09:20:01 UTC (heure produite par le script d'écriture), recalcul P3 tranche 1* : (a) **Q-RB-13** : les noms d'unité admis par le recalcul (rotation et `analyse.json`) sont restreints aux caractères d'un nom d'hôte en minuscules, `[a-z0-9.-]{1,253}` (resserrement du complément (3) de l'AVIS Q-R-02, qui admettait tout l'ASCII imprimable sans « : ») ; la structure en étiquettes (RFC 1123) est portée par l'item SHOGEN-S2BIS-NOMS-HOTE-RFC1123-1 ; même règle pour SIM-BIS (P-7 de sa tranche 3). (b) **Q-RB-14** : le mutant obligatoire « modulo n_s au lieu de n′_s » (§3.4) ne peut pas s'écrire dans RB-6, qui ne reçoit que n ; il est dû à RB-7.

*Ajout daté du 2026-10-09 16:59:08 UTC (heure lue par `date -u` à la dernière écriture du texte ; lot DETTES-T3, DT3-D ; adjudication Q-D1 de l'orchestrateur, 2026-10-09 15:51:56 UTC), point 4, règle d'estimation (SHOGEN-S2BIS-P1-ESTIMATION-1, annexe B, B.60 ; volets B.61 et B.85)* : toute taille [inféré] d'une partie ou d'un lot de S2-bis entre au calendrier multipliée par 2 (borne basse) et par 3 (borne haute), le jalon se posant sur la borne haute ; à la clôture de chaque partie, son rapport mesuré (lignes ajoutées sur estimation) remplace ce facteur pour les parties de même nature, et le calendrier annoncé à l'investisseur suit. Fondement : CALIB-ACTIFS, 3 168 lignes ajoutées en 21 commits (`1ed872c` à `19a0c7e`, recompté par `git show --numstat`) contre environ 1 100 à 1 300 estimées, soit ×2,44 à ×2,88 [calc]. Le compte de P1 (998 lignes de code pour CB-0 à CB-2 contre environ 560, ×1,78, environ ×2 avec les corrections) est lu dans `docs/adr-0029/s2bis/revue-p1a/G2-P1A.md` l.389, base de compte non retrouvée au recompte ; la règle n'en dépend pas.

*Ajout daté du 2026-10-10 04:06:47 UTC (heure lue par `date -u` à la dernière écriture du texte ; lot DEPLOI-BIS,
sous-lot DB-1, diff DB1-a ; décisions 1 à 10 de l'adjudication de l'orchestrateur sur DB-0, 2026-10-09 21:51:16 UTC,
prise sur le rapport du lecteur `claude-sonnet-5-5`)* : (1) **E-D-04, E-D-12** : le système est Debian 13 « trixie » ;
les versions des paquets entrent au descripteur ; la suite `trixie-security` est admise, pour les seules mises à jour de
sécurité ; `unattended-upgrades` s'ajoute à la liste d'E-D-04 (R-8 : ligne au tableau des paquets, licence lue à DB-6).
(2) **E-D-15, E-D-16** : O1 Hetzner Helsinki (FI), O2 OVHcloud Gravelines (FR), O3 DigitalOcean AMS3 (NL), O4 Akamai
Linode Singapour (SG, hors UE et hors États-Unis) ; repli : Linode Tokyo si une source géobloque Singapour ; Hetzner
Singapour (7,99 €) est un choix payant de l'investisseur, non retenu par défaut ; les ASN se contrôlent sur le
descripteur au démarrage. (3) **E-D-05, Q-D-07** (précision de l.241) : en sortie, le pare-feu admet aussi TCP/4460
(échange de clés NTS), TCP/23 (rsync vers l'espace de sauvegarde, port documenté) et HTTPS vers Healthchecks et
Certigna ; les serveurs NTP sont désignés par leur nom, résolu par le résolveur de l'observateur ; le refus par défaut
reste ; IPv6 est refusé. (4) **Q-D-06** : serveurs NTP `sth1.nts.netnod.se`, `gbg1.nts.netnod.se`, `ntppool1.time.nl` et
`ntppool2.time.nl`, en NTS ; limite écrite : le non-lissage de la seconde intercalaire chez Netnod est inféré, il n'est
pas déclaré sur les pages lues. (5) **E-D-20, A-3** : la commande OVHcloud n'offre aucun champ de script ; le script de
premier démarrage reste exécutable à la main (A-3 précisé pour O2) ; il tient sous 32 KiB (borne Hetzner, la plus petite
lue), et un test contrôle sa taille. (6) **E-D-21, Q-D-10** : caducs depuis la décision Certigna de l'investisseur
(2026-10-08) ; E-D-21 se lit « conditions et accès de Certigna » ; l'URL et l'authentification sont un acte extérieur
(documentation d'API demandée à Certigna par l'investisseur), dû avant DB-3 (minuterie de `jeton`) ; l'échéance de la
décision ANSSI (vers le 2027-02-17) se relit avant le sceau. (7) **Q-D-03** : un sous-compte d'écriture par
observateur ; un sous-compte en lecture seule dont la home englobe les quatre, sous réserve de l'essai de l'investisseur
à la mise en service ; repli écrit sans lecture croisée ; SHOGEN-S2BIS-STATUS-RETENTION-1 : la mémoire de `status` est
faite des résumés quotidiens clos, exclus de la purge locale de 7 jours et copiés au dépôt, avec les deux tests proposés
(au sous-lot DB-4, ou au diff de `status` qui les porte). (8) **Q-D-02** : N = 7 jours ; le CPX02 (20 Go) suffit
(environ 23 jours d'autonomie sans copie) ; le volume se mesure au rodage. (9) **Items** : SHOGEN-S2BIS-R8-PAQUETS-1 et
SHOGEN-S2BIS-HETZNER-DISPO-1 sont fermés par DB-0, leurs phrases versées avec P5 ; SHOGEN-S2BIS-REGIONS-1 : volet
régions fermé, volet cloud-init re-daté au premier déploiement (OVHcloud, image Debian 13 de Hetzner, user data de
DigitalOcean) ; SHOGEN-S2BIS-TSA-CERTIGNA-1 : volets lus fermés, volet URL et authentification en acte extérieur
(point 6). (10) **Écart du lecteur de DB-0** : un `rm -rf /root/.gnupg` hors du scratchpad (répertoire créé par son
propre premier appel `gpg`, absent avant et après, contrôlé) est admis ; les briefs suivants posent `GNUPGHOME` sous le
TMPDIR du dossier. Les actes de l'investisseur ajoutés par l'adjudication sont au dossier des actes (§11 du rapport de
DB-0) ; le texte validé de ce G0 reste tel quel.

*Ajout daté du 2026-10-10 04:39:03 UTC (heure lue par `date -u` à la dernière écriture du texte ; lot DEPLOI-BIS,
sous-lot DB-1, diff DB1-g ; adjudication de l'orchestrateur sur DB-1, 2026-10-10 04:33:52 UTC : questions Q-1 à Q-6 du
générateur adoptées dans la forme de l'avis OPS de l'advisor `claude-fable-5-1`, §3 ; chaque phrase relue contre le code
de DB1-b à DB1-f)* : (1) **E-D-01** : les paramètres en tête du script sont l'identité o (`OBSERVATEUR`), le
fournisseur, la région, la famille de résolveur, le résolveur du fournisseur (`RESOLVEUR_FOURNISSEUR`, une à quatre
adresses IPv4, famille fournisseur seule, celle d'O4), les adresses de surveillance et de sauvegarde et la clé publique
d'intervention (`CLE_INTERVENTION`, `ssh-ed25519`) ; tous sont vides au dépôt, collés par l'investisseur et jamais
versés ; chacun est contrôlé avant le premier changement, refus et arrêt sinon ; tous sauf la clé sont gardés dans
`/etc/shogen/observateur.conf` (0640, root:shogen), seule interface des paramètres pour DB-2 à DB-5, qui ne se copie
jamais hors de l'observateur (la copie horaire de DB-4 doit l'exclure) ; la clé est le seul contenu du fichier
`authorized_keys` du compte `intervention` (0600) (Q-1, Q-6). (2) **E-D-03** : compte de service `shogen`, compte
système sans shell (`/usr/sbin/nologin`) ni groupe ajouté ; compte de connexion `intervention`, sans droit
d'administration (aucun groupe ajouté, aucun fichier sudoers), clé `ssh-ed25519` seule ; réglages de sshd dans
`/etc/ssh/sshd_config.d/00-shogen.conf`, nommé pour être lu avant les fichiers de l'image (constat par `sshd -T` au
smoke de DB-2) : `PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`,
`PermitEmptyPasswords no`, `PubkeyAuthentication yes`, `AuthenticationMethods publickey`, `AllowUsers intervention`,
`DisableForwarding yes`, contrôlés par `sshd -t` avant rechargement ; le script ne supprime ni ne verrouille les comptes
de l'image, à qui `AllowUsers` ferme SSH ; N2 et N3 passent par la console du fournisseur (Q-1 ; JOURNAL l.382, q. 6 :
« l'investisseur seul, un agent au cas par cas sur son accord écrit »). (3) **E-D-04** : source APT unique, l'archive
Debian en HTTPS (`https://deb.debian.org/debian`, suite `trixie` ; `https://deb.debian.org/debian-security`, suite
`trixie-security` ; composant `main`), signée par le trousseau `debian-archive-keyring` (`.pgp`, sinon `.gpg` ; arrêt
sans trousseau) ; les autres fichiers de sources de l'image sont désactivés (renommés `*.disabled`) ; `trixie-updates`
n'est pas posée (décision 1 : sécurité seule) ; les paquets s'installent sans leurs recommandés (Q-2). (4) **T-DP-2** se
lit désormais : refus par défaut en entrée, sortie et transit ; boucle locale admise ; IPv6 jeté hors de la boucle
locale (Q-D-07) ; `established,related` admis, `invalid` jeté ; sortant, exactement : TCP/443 vers tout, UDP/53 vers les
trois témoins D-4, UDP et TCP/53 vers l'ensemble `resolveurs` (toute destination pour la famille unbound, celle d'O1),
UDP/123 et TCP/4460 vers l'ensemble `ntp`, TCP/23 vers l'ensemble `sauvegarde` (décision 3), UDP 68→67 (bail DHCP),
TCP/80 vers 169.254.169.254 pour root seul (métadonnées du fournisseur) ; entrant, exactement : TCP/22 et UDP 67→68 ;
mutants : tout le sortant ouvert, un témoin oublié, IPv6 admis ; ce texte remplace « exactement 443/tcp … Entrant : SSH
seul » (Q-3). (5) **Décision 3**, précision : le jeu commun est embarqué dans le script, égal octet pour octet à
`s2bis/deploi/nftables.conf` (test) ; les ensembles d'observateur s'écrivent au premier démarrage dans
`/etc/nftables.d/shogen-observateur.nft`, jamais versé : `resolveurs` par famille (unbound : toute destination ; quad9
et google : les adresses de l.82 ; fournisseur : les adresses collées), `ntp` et `sauvegarde` par les adresses IPv4 des
quatre serveurs de la décision 4 et de l'hôte de `ADRESSE_SAUVEGARDE`, résolues une seule fois, par `getent` ; un nom
non résolu arrête le script avant toute écriture du pare-feu ; le jeu passe `nft -c`, puis le service nftables est
activé et relancé ; l'étape résolveur de DB-2 se place avant l'étape pare-feu, pour que ces noms soient résolus par le
résolveur de l'observateur ; une minuterie de DB-3 rafraîchira les ensembles par nom (SHOGEN-S2BIS-PAREFEU-NOMS-1) ; le
smoke de DB-2 constatera les adresses NTS négociées (Q-4, Q-5). (6) **E-D-22**, constat (e) : un N2 volontaire sur
chaque observateur, après lequel le bail DHCP et la lecture des métadonnées du fournisseur sont constatés (L-5). Le
texte validé de ce G0 reste tel quel.
