# Avis de l'advisor OPS sur le sous-lot DB-1 (compte d'intervention, source APT, pare-feu, jeu commun, ensembles, configuration) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:55:47 UTC du fichier db1/AVIS.md ; contrôle FM-1.1 du transcript de l'advisor OPS : fragments_l51_l14 = 0 ; modèle résolu : claude-fable-5-1. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# AVIS OPS — DEPLOI-BIS, sous-lot DB-1 (six choix techniques du script I)

- **Modèle** : `claude-fable-5-1` (Fable 5.1), advisor, effort `medium` (CLAUDE.md §7, amendement 2026-09-18).
- **Date** : 2026-10-10 (date de session ; aucune horloge lue, la fiche n'a pas d'outil shell).
- **Pièces lues [lu]** : `s2bis/db1/RAPPORT-GENERATEUR.md` (§5, §6, §8, et §2-§3 pour les faits codés) ;
  `s2bis/db0/ADJUDICATION-DB0.md` (décisions 1 à 10) ; `s2bis/db1/BRIEF-DB1.md` ;
  `docs/adr-0029/g0-collecte/PROPOSITION.md` l.616-781 ; `JOURNAL.md` l.382.
- **Non lu** : le code des diffs, le G0 lui-même, l'ADR-0029, `RAPPORT-DB0.md`. Mes affirmations sur le script sont donc
  celles du rapport du générateur, pas une relecture du code (ce n'est pas le G2).
- **Attestation D.3** : aucune pièce de la liste D.2 ouverte ; aucune liste par motif ni recherche récursive ; seule
  écriture : ce fichier.

Convention : [lu] = lu sur la pièce citée ; [inféré] = raisonnement, non lu sur pièce.

## 1. Les six questions

### Q-1 Compte de connexion SSH `intervention`, clé en paramètre `CLE_INTERVENTION` — **adopter**

- **Pourquoi.** E-D-03 exige « SSH entrant par clé seule ; ni root ni mot de passe » sans nommer le compte
  (PROPOSITION l.644 [lu]). Sans compte nommé, `AllowUsers` ne peut pas écarter les comptes des images (RAPPORT §5 Q-1
  [lu ; le fait « root ou `debian` avec sudo selon l'image » est inféré par le générateur]). Un compte sans groupe ni
  sudoers, clé seule, est la forme la plus étroite qui satisfait E-D-03 et E-D-18 (« sans accès d'agent », l.659 [lu]).
- **Cohérence avec l'investisseur.** JOURNAL l.382 q. 6 [lu] : interventions « l'investisseur seul, un agent au cas par
  cas sur son accord écrit ». Un compte unique dont la seule clé est celle de l'investisseur, sans droit
  d'administration, met cette décision dans le code : une clé d'agent ajoutée au cas par cas (option (c), E-D-17 l.658
  [lu]) ne donne jamais root (RAPPORT §5 Q-1 [lu]).
- **Forme à garder.** La variante « sudo pour `intervention` » reste écartée (RAPPORT §5 Q-1 [lu]) : N2 et N3 passent
  par la console du fournisseur, ce qui est conforme à Q-D-08 (« redémarrage N2 par l'investisseur », l.773-774 [lu]).
- **Risques.**
  1. `status` doit être lisible par `intervention` (E-D-18) : droit de lecture à poser à DB-3 ou DB-4 (RAPPORT §8
     [lu]) ; sans cela, E-D-18 n'est pas tenue à la mise en service. À écrire dans le brief de DB-3.
  2. Le compte de l'image (root, `debian`) n'est pas supprimé ni verrouillé par DB-1 : il reste le chemin de la console
     (N2/N3). C'est voulu, mais la procédure (DB-6) doit le dire en clair, avec la consigne « jamais de clé SSH sur ce
     compte » [inféré : rien dans les pièces ne dit ce que le script fait de ce compte].
  3. Le script n'accepte qu'une clé `ssh-ed25519` (RAPPORT §5 Q-1 [lu]) : l'investisseur doit en avoir une. Acte
     extérieur à nommer dans la procédure (DB-6), avant le collage (A-x du §8 de la PROPOSITION, non lu ici).
  4. La clé publique n'est pas un secret, mais elle identifie l'investisseur : elle est collée, pas versée (même règle
     que les adresses d'E-D-01, l.642 [lu]).
- **Au G0 (ajout daté).** E-D-01 : la liste des paramètres en tête devient « identité o, fournisseur, région, famille
  de résolveur, résolveur du fournisseur (O4), adresses de surveillance et de sauvegarde, clé publique
  d'intervention » ; les trois derniers sont collés et jamais versés. E-D-03, précision : « le compte qui se connecte
  est `intervention`, sans droit d'administration ; `AllowUsers intervention` ; N2 et N3 par la console du
  fournisseur ». Texte proposé au §3.

### Q-2 Une seule source APT, archive Debian en HTTPS, autres sources en `*.disabled` — **adopter**

- **Pourquoi.** Le pare-feu n'ouvre que TCP/443 en sortie (E-D-05, l.646 [lu] ; T-DP-2 l.698 [lu]). Un miroir en HTTP
  tomberait en silence et E-D-12 (mises à jour de sécurité) ne serait plus tenue (RAPPORT §5 Q-2 [lu ; HTTP des miroirs
  d'images : inféré par le générateur]). L'archive `deb.debian.org` est celle lue à DB-0 pour le tableau R-8
  (PROPOSITION l.678-680 [lu] ; ADJUDICATION décision 1 [lu]) : une seule origine pour les versions et pour
  l'installation, c'est ce que E-D-04 demande (« versions au descripteur »).
- **`trixie-updates` non posée** : conforme à la décision 1 (« mises à jour de sécurité seules ») [lu]. Conséquence à
  écrire dans doc 17 (« dérive par mises à jour », E-D-19 l.660 [lu]) : les correctifs hors sécurité (fuseaux,
  autorités de certification) n'arrivent pas sans acte N2. Ce n'est pas un défaut de DB-1, c'est la décision 1.
- **Risques.**
  1. APT en HTTPS exige `ca-certificates` ; le script refuse sans trousseau Debian mais le rapport ne dit pas qu'il
     contrôle `ca-certificates` (RAPPORT L-3 [lu]). Si l'image en manque, `apt-get update` échoue sans source HTTP de
     secours. À constater au premier déploiement, et à mettre au smoke (DB-2) : « `apt-get update` réussi sur les deux
     suites ».
  2. Le renommage en `*.disabled` peut être défait par un outil du fournisseur à un redémarrage [inféré] : le
     contrôle d'empreinte de `debian.sources` (DB-5, RAPPORT §8 [lu]) le verra. Rien de plus à DB-1.
  3. Le chemin du trousseau (`.pgp` ou `.gpg`) est inféré (L-3) : refus et arrêt sans trousseau est la bonne forme
     (visible, pas silencieux).
- **Au G0.** E-D-04, précision : « source unique : archive Debian en HTTPS (`deb.debian.org`, suites `trixie` et
  `trixie-security`, composant `main`) ; les autres fichiers de sources de l'image sont désactivés ».

### Q-3 Écarts au « exactement » de T-DP-2 (DHCP, métadonnées, boucle locale, états) — **adopter, et réécrire T-DP-2**

- **Pourquoi.** Sans bail DHCP ni métadonnées, l'observateur se coupe lui-même au premier N2 (RAPPORT §5 Q-3 [lu ;
  DHCP et 169.254.169.254 par fournisseur : inférés]). La boucle locale, `established,related` et `invalid` jeté sont
  la forme ordinaire d'un refus par défaut qui laisse passer les réponses des flux déjà admis [inféré]. La sonde sur le
  fil (RAPPORT §3 (2) [lu]) montre qu'il n'y a rien d'autre.
- **Ce qui change dans la lettre.** T-DP-2 dit (l.698-699 [lu]) : « exactement 443/tcp ; 53 vers le résolveur et les
  trois témoins ; 123/udp vers les serveurs fixés ; SSH vers l'espace de sauvegarde. Entrant : SSH seul ». La décision 3
  [lu] a déjà ajouté TCP/4460 et remplacé « SSH vers l'espace de sauvegarde » par TCP/23 ; le script ajoute TCP/53 vers
  les résolveurs (RAPPORT §2 [lu]), DHCP, métadonnées pour root seul, et des réponses DHCP en entrée. Le mot
  « exactement » n'est plus vrai tel qu'écrit ; il faut le réécrire plutôt que le laisser contredit par le code.
- **Forme exacte proposée pour T-DP-2 (ajout daté).** « Refus par défaut en entrée, sortie et transit ; IPv6 jeté
  (Q-D-07). Sortant autorisé, exactement : TCP/443 vers tout ; UDP/53 vers les trois témoins D-4 ; UDP et TCP/53 vers
  l'ensemble `resolveurs` (toute destination pour O1) ; UDP/123 et TCP/4460 vers l'ensemble `ntp` (décision 3) ; TCP/23
  vers l'ensemble `sauvegarde` (décision 3) ; UDP 68→67 (bail DHCP) ; TCP/80 vers 169.254.169.254 pour root seul
  (métadonnées du fournisseur). Entrant, exactement : TCP/22 et UDP 67→68. Boucle locale, `established,related`
  admis ; `invalid` jeté. Mutants : tout le sortant ouvert ; un témoin oublié ; IPv6 admis. »
- **Risques.**
  1. Métadonnées : l'adresse et le protocole varient par fournisseur [inféré, L-5]. Si un fournisseur sert les
     métadonnées autrement, cloud-init échoue au N2 mais le système démarre ; visible au N2 volontaire. À constater à
     la mise en service : je propose d'ajouter un constat (e) à E-D-22 (voir §3) plutôt qu'un item.
  2. `meta skuid 0` : seule la racine atteint 169.254.169.254:80. Le service `shogen` ne peut pas s'en servir :
     bon. `unattended-upgrades` tourne en root et pourrait l'atteindre : sans conséquence [inféré].
  3. UDP 67→68 entrant : ouvert à toute source. Portée : un paquet forgé vers le client DHCP ; le risque existe sur
     tout hôte en DHCP, DB-1 ne l'aggrave pas [inféré]. Doc 17 (DB-6) : « fournisseur qui altère le réseau ».
  4. IPv6 entièrement jeté : si une image n'a qu'IPv6 pour un service du fournisseur, il tombe. Aucun indice de cela
     dans les pièces ; L-1 le couvre au smoke.

### Q-4 Pare-feu commun embarqué dans le script, égal octet pour octet à `nftables.conf` — **adopter**

- **Pourquoi.** Seul le script arrive par cloud-init ; l'archive du code arrive après (Q-D-01, l.740-745 [lu]) et par
  TCP/23 déjà filtré. Poser le pare-feu après l'archive laisse une fenêtre sans pare-feu pendant l'installation
  (RAPPORT §5 Q-4 [lu]) : c'est l'option à écarter. Le test d'égalité octet pour octet ferme le risque de dérive entre
  les deux copies (RAPPORT §3, `test_tdp2_commun_embarque_et_ensembles`, mutants f02-f04, f14 « mutés dans les deux
  copies » [lu]).
- **Risques.**
  1. Deux copies : toute modification de `nftables.conf` (DB-2, DB-3 pour le rafraîchissement) doit toucher les deux ;
     le test le force. Dire dans le brief de DB-2 et DB-3 : « le test d'égalité est la règle, pas une gêne ».
  2. Taille : 11 850 octets à DB1-f, environ 19,9 Ko de marge sous 32 KiB (RAPPORT §8 DB-5 [lu]) ; DB-2 à DB-5
     consomment cette marge. Le test de la décision 5 le tient.
- **Au G0.** Rien de normatif à ajouter ; une ligne de constat : « le jeu commun est embarqué dans le script et égal à
  `s2bis/deploi/nftables.conf` (test) ».

### Q-5 Ensembles par nom : rafraîchissement à DB-3, constat des adresses négociées au smoke (DB-2) — **adopter**

- **Pourquoi.** La décision 3 fixe « serveurs NTP par nom (résolus par le résolveur de l'observateur) » [lu] ; le script
  résout au premier démarrage seulement (RAPPORT §5 Q-5 [lu]). time.nl prévient que les adresses changent sans préavis
  (RAPPORT §5 Q-5 citant RAPPORT-DB0 §5 [lu de seconde main : je n'ai pas lu RAPPORT-DB0]). Sans rafraîchissement, un
  changement d'adresse coupe le NTP ou la sauvegarde ; c'est visible en D-3 ou par le silence de la copie horaire, mais
  c'est une panne évitable. La minuterie à DB-3 est le bon endroit (unités et minuteries, l.672 [lu]).
- **Forme à exiger à DB-3.** Même fonction de résolution que le script (une seule source de vérité), rechargement
  atomique des seuls ensembles (jamais du jeu), échec de résolution = ensembles inchangés, journalisé. Le rapport dit
  déjà ces trois points (RAPPORT §5 Q-5 [lu]) ; ils doivent être dans le brief de DB-3.
- **Risques.**
  1. Le pare-feu dépend alors du DNS : un résolveur menteur peut ouvrir UDP/123, TCP/4460 et TCP/23 vers des adresses
     de son choix [inféré]. Portée bornée (trois ports, pas 443). À écrire dans doc 17 (DB-6) ; NTS (décision 4)
     authentifie le serveur de temps, ce qui réduit le risque sur 123/4460 [inféré]. Pour TCP/23, la sauvegarde épingle
     l'empreinte d'hôte (RAPPORT §8 DB-4 [lu]).
  2. NTS-KE peut désigner une autre adresse NTP (RFC 8915 §4.1.7, inféré par le générateur) : le constat au smoke
     (DB-2) doit lire les adresses négociées par chrony et les comparer à l'ensemble `ntp` ; sinon, D-3 le montrera
     tard.
- **Au G0.** Précision à la décision 3 : « les ensembles par nom sont rafraîchis par une minuterie (DB-3) ; les
  adresses NTS négociées sont constatées au smoke (DB-2) ».

### Q-6 `/etc/shogen/observateur.conf`, 0640 root:shogen, seule interface des paramètres — **adopter**

- **Pourquoi.** Une seule interface pour DB-2 à DB-5 évite que chaque sous-lot relise la tête du script [inféré]. Les
  droits 0640 root:shogen donnent la lecture au service (signal de vie, E-D-11) et la refusent à `intervention` : c'est
  conforme à « adresses jamais versées » (E-D-01 [lu]) et à l'ADR l.245 citée par le rapport (adresse secrète sur le
  disque seulement ; non lue ici).
- **Risques.**
  1. Ce fichier contient un secret (adresse du signal de vie) : la sauvegarde horaire (DB-4) ne doit **jamais** le
     copier, et les empreintes (DB-5) le classent par observateur, pas commun (RAPPORT §8 DB-5 le fait [lu]). À écrire
     dans le brief de DB-4 : « `observateur.conf` exclu de la copie ».
  2. Reconstruction N3 (E-D-17) : le fichier se régénère par le script rempli ; la procédure (DB-6) doit dire que
     l'investisseur garde ses paramètres hors des serveurs.
  3. `intervention` ne lit pas ce fichier : `status` (E-D-18) ne doit pas en dépendre, ou DB-3/DB-4 pose un
     fichier de lecture distinct, sans l'adresse secrète.
- **Au G0.** Précision à E-D-01 : « les paramètres sont gardés dans `/etc/shogen/observateur.conf` (0640, root:shogen),
  seule interface des sous-lots suivants ; jamais copié hors de l'observateur ».

## 2. Les limites L-1 à L-9 : items ou non

Règle que j'applique : un item seulement si son déclencheur est un lot nommé ou un acte extérieur et qu'aucune exigence
existante ne le porte déjà ; sinon, la limite se range dans le brief du sous-lot qui la ferme.

| limite | item ? | déclencheur | motif |
|---|---|---|---|
| L-1 IPv6 non sondé | non | DB-2 (smoke : sonde IPv6) puis E-D-22 | déjà au §8 DB-2 du rapport ; le smoke est le lieu |
| L-2 `sshd -T` non lancé | non | DB-2 (smoke : `sshd -T`) | idem ; à écrire dans le brief de DB-2 |
| L-3 trousseau, `ca-certificates` | non | DB-2 (smoke : `apt-get update` des deux suites) et premier déploiement | se fond dans le volet cloud-init re-daté de REGIONS-1 (décision 9) |
| L-4 outils de l'hôte ≠ trixie | non | DB-2 (smoke sur trixie : `nft -c`, `apt-config dump` réels) | limite de l'environnement de preuve, fermée par le premier smoke réel |
| L-5 métadonnées, DHCP par fournisseur | non, **ajout à E-D-22** | mise en service (acte de l'investisseur) | constat (e) : « N2 volontaire : bail DHCP et métadonnées constatés après redémarrage » |
| L-6 racine `/` jamais essayée | non | aucun | limite de conception voulue (sûreté) ; une phrase dans le test suffit |
| L-7 sûreté du mode d'essai | non | DB-6 (doc 17 : entrée « mode d'essai ») | propriété à documenter, rien à déclencher |
| L-8 redémarrages de services par les mises à jour | **oui**, SHOGEN-S2BIS-MAJ-SERVICES-1 | DB-6 (doc 17, « dérive par mises à jour ») ; décision à DB-3 | trou D-3/D-5 réel ; `needrestart` serait un paquet de plus (R-8) : décision d'orchestrateur, pas de DB-3 seul |
| L-9 ensembles par nom non rafraîchis | **oui**, SHOGEN-S2BIS-PAREFEU-NOMS-1 | DB-3 (minuterie) + DB-2 (constat NTS) | voir Q-5 |

Si la règle PAROXYSME (non lue ici) impose un item par limite, les déclencheurs ci-dessus sont ceux à écrire ; aucun
item ne doit rester sans lot ou sans acte.

## 3. Ce qui entre au G0 par ajout daté (texte proposé, une ligne par point, à dater à l'écriture)

1. E-D-01, paramètres : liste étendue (`RESOLVEUR_FOURNISSEUR` pour O4, `CLE_INTERVENTION`) ; gardés dans
   `/etc/shogen/observateur.conf` (0640, root:shogen), seule interface de DB-2 à DB-5, jamais copié hors de
   l'observateur (Q-1, Q-6).
2. E-D-03, précision : compte `intervention`, clé `ssh-ed25519` seule, sans droit d'administration ;
   `AllowUsers intervention`, `DisableForwarding yes` ; N2 et N3 par la console du fournisseur (Q-1 ; JOURNAL l.382
   q. 6).
3. E-D-04, précision : source unique, archive Debian en HTTPS (`deb.debian.org`, `trixie` et `trixie-security`,
   `main`) ; autres sources désactivées ; `trixie-updates` non posée (décision 1) (Q-2).
4. T-DP-2, réécrit : la forme exacte du §1 Q-3 (remplace « exactement 443/tcp … Entrant : SSH seul »).
5. Décision 3, précision : jeu commun embarqué, égal à `nftables.conf` (test) ; ensembles par nom rafraîchis par
   minuterie (DB-3) ; adresses NTS négociées constatées au smoke (DB-2) (Q-4, Q-5).
6. E-D-22, constat (e) : N2 volontaire sur chaque observateur, bail DHCP et métadonnées constatés (L-5).
7. Items ouverts : SHOGEN-S2BIS-MAJ-SERVICES-1 (déclencheur DB-6, décision DB-3) ; SHOGEN-S2BIS-PAREFEU-NOMS-1
   (déclencheur DB-3).

Rappel : seul l'orchestrateur écrit au G0 et committe (CLAUDE.md §7) ; ce texte est une proposition.

## 4. Points pour les briefs suivants (hors G0)

- DB-2 : smoke avec `sshd -T`, sonde IPv6, `apt-get update` des deux suites, adresses NTS négociées comparées à
  l'ensemble `ntp` ; étapes horloge et résolveur avant `pare_feu` (RAPPORT §8 [lu]).
- DB-3 : minuterie de rafraîchissement (même fonction, ensembles seuls, échec = inchangé) ; droit de lecture de
  `intervention` pour `status` sans l'adresse secrète.
- DB-4 : `observateur.conf` exclu de la copie.
- DB-6 : procédure : compte de l'image = console seule, jamais de clé ; clé ed25519 de l'investisseur avant le
  collage ; doc 17 : dépendance du pare-feu au DNS, absence de `trixie-updates`, redémarrages de services.
