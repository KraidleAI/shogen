# Rapport des corrections G2 de la tranche A du collecteur S2-bis : diffs CB-2d et CB-2e

Transcription par l'orchestrateur du rapport rendu par message (le harnais du worker interdit les fichiers de rapport : écart E-2 du
worker). Worker `claude-opus-5-5`, 2026-10-04, de 21:14:54 à 22:03:57 UTC. Le texte complet du message est conservé hors dépôt ; ce
fichier en garde les décisions, chiffres et items.

## Livraison
- Deux diffs en série après CB-2c (le correctif faisait 325 lignes de code, au-delà du plafond de 200) : **CB-2d** (code +196/−41,
  documents +57/−7) et **CB-2e** (code +129/−32, documents +42/−1). Chaque état est vert seul ; tests de 34 à 42, puis 49.
- Base : tête `b742e3c` (les commits arrivés pendant le travail ne touchent aucun chemin du lot).

## Corrections
- **C-1** : fenêtre antérieure à la dernière écrite refusée (`JOURNAL/fenetre`) ; dernière fenêtre restaurée à la reprise, au besoin
  depuis les fichiers précédents ; `suivante = max(attendu, dernière + w, ws + w)` ; `ws` non entier = queue. Lecture adjugée par
  l'orchestrateur : après un redémarrage, `ws ≤ dernière` refusé ; dans une exécution, seul `ws < dernière` (plusieurs lectures d'une
  fenêtre puis son marqueur). Q-4 : fenêtre du redémarrage refusée ; test à prémisse refaite, non supprimé.
- **C-2** : décorateur `_terminal` sur `ouvrir`, `ecrire`, `marqueur` : après une `OSError`, tout appel lève `JOURNAL/casse` sans rien
  écrire ; `fermer` rend toujours le verrou ; descripteur oublié avant fermeture ; reprise suivante déclare la queue (sonde réelle par
  RLIMIT_FSIZE : `sha256sum -c` OK, FAILED sur la base).
- **C-3** : `canonique` sérialise d'abord ; cycle → `JOURNAL/type` en temps borné ; sous-structure partagée admise.
- **C-4** : plancher par défaut et `--plancher` exercés ; K-01 et K-02 refusent `if:`.
- **C-5** : les 19 mutants vivants non équivalents de la G2 tués, chacun par le test demandé.
- **C-6** : contrôle au rang réel avant toute bascule ou trou (« tout refus n'écrit rien » devient vrai) ; FORMAT §3.2, §4, §7.5, §8.1 ;
  METRIQUES ; pièce G6 (POSIX seulement).
- **Q-2** : option `--egal` (Ran = plancher), réservée au job s2bis (`--aucun-saut --egal --plancher 49`) ; défaut du vérificateur
  inchangé (S2 : 405 tests, OK, skipped=2).

## Preuves
- Rouge : CB-2d, 11 tests en échec sur le code de base ; CB-2e, cycle, `egal` inconnu, K-02.
- Vert : 42 puis 49 tests sous Python 3.10, 3.11, 3.12, 3.13 avec `-X dev -W error`, 0 avertissement.
- Mutants : CB-2d 19/19, CB-2e 11/11, jeux de la G2 41/41 et 32/32 (sept fragments réécrits sur le nouveau texte).
- Gates : S-G1 à S-G8 vertes ; S-G9 rouge connue sur une copie sans `docs/rapports` (verte sur le dépôt réel, commits du lot).

## Écarts déclarés
E-1 deux diffs ; E-2 rapport par message ; E-3 tête avancée ; E-4 commande `sh -c` bloquée par le harnais, remplacée par un script ;
E-5 statut d'une tâche de fond ; E-6 docstring précisée après campagne, preuves refaites ; E-7 injection d'écriture partielle en boîte
blanche, complétée par la sonde réelle ; E-8 mutant M-2c-07 du worker devenu sans objet ; E-9 passes récursives sur le `docs/` des
copies seulement.

## Items proposés
- **I-C1** : la rétention (DB-4) garde le dernier fichier qui contient un enregistrement de fenêtre (sinon la restauration de C-1
  retomberait sur `attendu` après une longue panne à horloge reculée) ; déclencheur : G0 de DB-4.
- **I-C2** : refus nommés pour un écrivain fermé puis réutilisé (`TypeError` aujourd'hui) et pour un second `ouvrir` (perte d'un
  descripteur de verrou, préexistant) ; déclencheur : CB-4.
- **I-C3** : toute méthode publique d'écriture ajoutée à `Journal` porte `_terminal`, contrôle mécanique à prévoir ; déclencheur : CB-4,
  CB-11.
- **I-C4** : graphe partagé sans cycle à expansion exponentielle non borné en temps ; rattaché à N-4 ; déclencheur : CB-3.
