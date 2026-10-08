# Relecture G2 de la tranche B de P1 (CB-3a à CB-11b) — transcription par l'orchestrateur

Rapport rendu par message (le harnais interdit les fichiers de rapport). Réviseur G2 neuf `claude-opus-5-5`, 2026-10-04 23:18:00 à
2026-10-05 00:06:23 UTC. Pièces du réviseur : `…/p1b/g2/travail/` (index `SHA256SUMS-reviseur`, sha256 `49613c42…832a`, 101 lignes).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-7)
(1) 8 diffs en série sur `435fa12` et `6535821` ; 200, 199, 200, 135, 142, 85, 170, 40 lignes ; arbre = 14 empreintes ; chaque état vert
seul, plancher exact 49 → 92. (2) Conformes : E-C-03, 04, 05, 11, 14, 15, 26, 28, 29 ; partiels attendus : E-C-09, 17 ; réserves :
E-C-12, 13 (C-1, C-5), E-C-27 (C-2), CB-5 (C-6), CB-10 (C-2, C-7). (3) Sondes HTTP S-H1 à S-H10 classées juste ; échéance tenue avec
12 lectures et sondes pendues ; défauts : C-1, C-2, C-4, C-5. (4) 31 mutants du réviseur : 17 tués, 14 vivants (MG-22 équivalent en
pratique) ; M-LP du worker rejoués sur la suite entière : 13 tués, M-LP-3 FATAL (la suite pend). (5) CI : seul le plancher monte,
`--egal` gardé. (7) R-13 0 ; R-8 bibliothèque standard ; S2 405 OK ; runner 32 ; hook 54 ; secrets OK ; xtask S-G1 à S-G8 vertes.

## Corrections
- **C-1 Échéance exacte** (E-C-12, E-C-13, FORMAT §11.4) : une lecture finie après l'échéance mais avant son classement est écrite comme
  lecture (S-B1 : `ok`, +50,2 ms). Relever l'état de chaque lecture une seule fois à E, avant toute écriture ; non finie si le résultat
  n'était pas là ou si `fin` > E (chemin des résultats tardifs) ; `fin` = E pour une non finie, ou FORMAT corrigé. Test : écrivain
  ralenti injecté.
- **C-2 DNS** (FORMAT §12, E-C-27, E-C-28) : (a) un datagramme qui ne répond pas à la requête (source, identifiant, QR, question) est
  ignoré et l'attente continue ; `forme` réservé à une réponse appariée mal formée ; (b) adresse non IPv4 littérale canonique refusée en
  `forme`, sans exception ni résolution. Tests : S-D1, S-D2, S-D7, S-D8, S-D9.
- **C-3 TLS** : (a) armer `CONTEXTE` comme le contexte d'urllib (ALPN `http/1.1`, `post_handshake_auth`), ou déclarer l'écart au FORMAT
  §9 ; (b) tests sans réseau : attributs de `CONTEXTE` (CERT_REQUIRED, contrôle du nom, ALPN) ; chemin réussi par une couche TLS injectée
  qui note `server_hostname` et journalise la phase `tls` (tuent MG-01 à MG-03).
- **C-4 Horloge** (ferme SHOGEN-S2BIS-HORLOGE-RECUL-JOURNAL-1) : délais de `lire` et `interroger` sur `time.monotonic`, instants
  journalisés sur l'horloge murale ; tout recul de l'horloge murale observé d'une fenêtre à la suivante journalisé brut dans `sante` ;
  FORMAT §11 et §13. Tests : S-C1, S-C2, recul injecté entre deux fenêtres.
- **C-5 Sondes bornées** (Q-C-03, E-C-13) : ne pas relancer une sonde dont l'instance précédente n'a pas rendu (valeur null) ; journaliser
  le nombre de sondes vivantes. Test : sondes pendues sur trois fenêtres, nombre de fils constant.
- **C-6 Tests de la boucle bornés en temps** : `test_boucle.py` et `test_sante.Branchement` font tourner la boucle dans un fil joint
  borné ; preuve : M-LP-3 rejoué sur la suite entière sort en 1 en temps borné.
- **C-7 Mutants vivants à tuer** : MG-11, MG-13, MG-18, MG-19, MG-21, MG-23, MG-24, MG-26, MG-29, MG-31 ; un test nommé par mutant, rouge
  montré sur le mutant.

## Avis sur les écarts et questions du worker
E-1, E-2 d'accord ; E-3 (a) pas de ThreadPoolExecutor : d'accord (essai refait : un exécuteur à tâche pendue empêche la sortie, même avec
`shutdown(wait=False, cancel_futures=True)` ; la lettre de l'ADR l.235 est tenue : `Future`, `wait`, `BoundedSemaphore`) ; (b), (c),
(d), (g), (h) d'accord ; (e) D-3 brut d'accord sous I-B1 avant le gel ; (f) aucune redirection : d'accord (S2 suivait par `urlopen` ;
aucune trace de redirection d'un hôte du pool [abs] ; le smoke de CB-16 imprime code et hôte du `Location` d'une 3xx sans la suivre) ;
(i) TC sans repli TCP d'accord pour D-4, D-5. Q1 un commit par diff ; Q2 pas d'ajout daté requis, motif au JOURNAL (FORMAT §11.7) ;
Q3, Q4, Q6 acceptées ; Q5 HORLOGE-RECUL dans C-4, « fermer et sortir » à CB-18.

## Items
I-B1 CHRONYC-FORMAT (G0 de CB-17 et de RB-validité, avant le gel ; capture d'erreur bornée, O-3) ; I-B2 TLS réussi : en partie absorbé
par C-3, poignée réelle au smoke CB-16 (une fixture de clé privée buterait sur la gate des secrets) ; I-B3 TC (CB-12, O-4) ; I-B4 nom du
plan sans lecture refusé à la construction (CB-18, O-6) ; I-B5 exposition E-4. Neuf : **SHOGEN-S2BIS-MUT-COMMANDE-1** — les campagnes de
mutants se classent par la commande du job (suite entière), sinon un mutant qui pend la suite est compté tué. Effets B.60 :
CORPS-BORNE-1 volet corps fermé par construction (pire ligne 1 398 705 octets), volet graphe redaté à CB-6 ; ECRIVAIN-USAGE-1 redaté à
CB-18 ; G3-LIGNE-JOB-1 appliqué ; P1 ≈ 3 000 à 3 300 lignes.

## Observations O-1 à O-10 (non bloquantes)
O-1 rouge de CB-5 pris sur un arbre antérieur à CB-4 ; O-2 compte de lignes METRIQUES (135/134) ; O-3 sortie d'erreur de D-3 jetée ;
O-4 TC coupé → `forme`, drapeau perdu ; O-5 `BaseException` dans une lecture : futur en attente, `abandonnes` surcompte ; O-6 nom du
plan sans lecture → `panne_transport:autre` ; O-7 `Boucle(sondes=None)` écrit un `sante` incomplet ; O-8 bornes de temps tenues sous
charge ; O-9 cas corrects à la sonde mais absents des tests (S-H2 à S-H8, S-H10) ; O-10 identifiant hors 16 bits → `struct.error`
(injection seule).

## Exposition du réviseur
E-R1 `grep -rn` sur `s2-harness/` (`*.jsonl` exclus) : une ligne d'une fixture de S2 affichée ; E-R2 R-13 et secrets bornés aux fichiers
du lot ; E-R3 quatre lignes « note » de S-G5 citant des documents permis ; E-R4 la sortie de `ps` a porté la ligne de commande du
processus parent (identifiant et URL de session, déjà présents dans les messages de commit). Constat de Gate 0 : processus parent en
`--effort high`. Réseau isolé (`unshare -n`), clés TLS de test détruites.
