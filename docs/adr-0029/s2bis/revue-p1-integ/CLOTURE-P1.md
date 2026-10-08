# Pièce de clôture de la partie P1 (collecteur de S2-bis, noyau), pour l'accord de partie

- **Rattachement** : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, point 5 et son ajout daté du
  2026-10-05 (accord rendu par un advisor sur cette pièce). Base relue : `98c8537` (branche
  `claude/compassionate-noether-szmdyj`). Rédigée le 2026-10-05 par le réviseur G2 d'intégration (`claude-opus-5-5`),
  qui n'a écrit ni relu aucune tranche de P1.
- **Verdict de la relecture d'intégration** : ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-5 (ci-dessous).

## 1. Ce que P1 fait

P1 est le noyau du programme qui tournera sur chacun des quatre serveurs d'observation (sous-lots CB-0 à CB-5, CB-10,
CB-11, CB-18 ; environ 1 100 lignes de code et 2 800 lignes de tests, bibliothèque standard de Python seule). À chaque
fenêtre d'une minute, il :
- lance les lectures des sources en parallèle, chacune avec un délai de 10 s, et tient une échéance dure une seconde
  avant la fin de la fenêtre ; une lecture qui ne rend pas à temps est classée en panne typée, jamais attendue ;
- note la santé de l'observateur (retard des départs, lectures non parties, horloge, témoins DNS, disque), en valeurs
  brutes, sans jugement ;
- écrit tout dans un journal chaîné (chaque ligne porte l'empreinte de la précédente), un fichier par jour, avec un
  fichier de sommes ; après un arrêt, il reprend la chaîne, déclare les octets abîmés au lieu de les réécrire, et
  déclare chaque fenêtre perdue avec sa cause ;
- refuse de démarrer sur une configuration incomplète ou incohérente, et inscrit au journal, à chaque démarrage, le
  commit et l'empreinte de chaque fichier de configuration.

P1 ne contient pas encore les décodeurs des sources, la carte, le relevé ASN, les têtes horodatées, le smoke ni la
commande `status` (partie P2), ni le déploiement (P5).

## 2. Ce qui est prouvé, et par quoi

- **Suites** (lancées par la commande des jobs, réseau coupé, `-X dev -W error`) : 184 tests du paquet (143 du
  collecteur, 41 du recalcul), 77 cas du vérificateur et 129 tests de SIM-BIS sous Python 3.10 à 3.13 ; suite S2
  (406) sous 3.11 à 3.13, aux planchers exacts (rouge sous 3.10 : item connu).
- **Format du journal** : une sonde écrite d'après le seul texte du FORMAT juge l'écrivain réel sur 1 000 journaux
  synthétiques, 4 876 redémarrages et 1 801 queues déclarées, avec pannes d'écriture et arrêts brutaux : aucun écart
  (déclarations, chaînage, état de reprise, refus, sommes).
- **Bout en bout** : le point d'entrée réel, contre des serveurs factices (HTTPS par une autorité de test, DNS), sur
  25 fenêtres en 7 exécutions (panne de source, lecture pendue, recul d'horloge de 2,5 s, arrêt brutal, SIGTERM ; une
  seconde instance refusée) : journal conforme ; puis 1 800 fenêtres en 30 minutes avec une lecture pendue à chaque
  fenêtre : journal conforme, mémoire en plateau (45,4 Mo), 18 fils au plus, sortie propre.
- **Entrées hostiles** : réponses HTTP énormes, lentes ou mal formées : toutes closes dans le délai, aucune exception.
- **Mutants** : 30 mutants neufs à l'échelle de la partie : 25 tués, 5 vivants, tous aux interfaces entre tranches
  (corrigés par C-3) ; les trois tranches avaient chacune leur relecture, leurs corrections et leurs contre-contrôles.

## 3. Ce qui reste à faire avant l'accord (corrections C-1 à C-5)

- **C-1** Une seule réponse DNS hostile de 64 Kio (au lieu des 512 octets au plus de la RFC 1035) fait dépasser à
  l'enregistrement de santé la taille de ligne admise : le collecteur s'arrête à chaque fenêtre, à chaque relance.
  Borner la taille des réponses et le nombre de sondes.
- **C-2** Durabilité : la reprise s'appuie sur des octets jamais synchronisés, et la création d'un fichier n'est pas
  suivie d'une synchronisation du dossier (point accepté en tranche A pour « au plus tard CB-18 », resté sans suite) ;
  après une coupure de courant, la chaîne peut paraître rompue et une somme fausse.
- **C-3** Tests d'interface manquants entre le client HTTP, la boucle et le point d'entrée (cinq mutants vivants,
  dont un qui empêcherait tout démarrage en production) ; un ordre d'écriture à corriger dans le client.
- **C-4** Quatre phrases du FORMAT à rendre exactes.
- **C-5** Outillage de la CI : l'enregistreur de rôle accepte un plancher 0 que le contrôle de la CI refuse ; un
  vérificateur qui sort en 0 dès son chargement fait passer le contrôle de la CI sans qu'aucun cas ne tourne.

## 4. Ce qui reste ouvert, et quand

| sujet | quand |
|---|---|
| calendrier dans `run_params` ; configurations de production scellées (valeurs de l'ADR, marge du pool) ; taille de `run_params` contrôlée avant l'ouverture | gel du collecteur |
| politique quand l'écrivain refuse une valeur d'un décodeur | G0 de CB-6 (P2) |
| journal illisible si la toute première écriture échoue (l'observateur ne redémarre plus seul) | procédure d'intervention et exercices (DB-6, A-7) |
| SIGTERM sans fermeture propre ; droits des fichiers ; dossier unique par journal ; lecture bornée de la configuration du résolveur | P5 (DB-1, DB-3) |
| format de `chronyc`, repli TCP du DNS, poignée TLS réelle | P2 (CB-12, CB-16, CB-17) |
| suite S2 rouge sous Python 3.10 | G0 de RB-2 |

## 5. Risques résiduels

- **Taille** : P1 mesure environ 2,4 fois l'estimation du G0 (tests compris) ; le calendrier annoncé à l'investisseur
  en dépend (item SHOGEN-S2BIS-P1-ESTIMATION-1).
- **Non éprouvé ici** : la forge ne lance pas les jobs ; la poignée TLS avec de vrais serveurs ; l'heure réelle d'un
  serveur (le recul d'horloge est simulé) ; la tenue sur des semaines (mesurée sur 30 minutes au plus).
- **Confiance dans l'outillage** : l'enregistreur de rôle et les jobs exécutent le vérificateur du commit relu ; un
  vérificateur altéré dans ce commit les tromperait tant que C-5 n'est pas faite, et l'enregistreur resterait trompé
  après elle : la relecture humaine du vérificateur reste nécessaire.
- **Après le gel**, toute correction du chemin de lecture ou du journal refait le rodage entier de 14 jours (Q-C-06).
