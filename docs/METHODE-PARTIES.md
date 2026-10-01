# Méthode de travail par parties (texte de l'investisseur, versé tel quel)

Statut : adoptée pour Shōgen le 2026-10-01 (JOURNAL), **sauf la section 5 (messagerie entre sessions)** : investisseur, 2026-10-01 00:08 UTC, verbatim « non, pas de messagerie pour toi », application « maintenant, sur la suite de S2 » ; les lots déjà lancés finissent leur circuit. L'adaptation au dépôt (découpage des lots restants d'ADR-0028 en parties, siège de la « session propriétaire de la production », PR et fusion) est fixée par une ADR dédiée après avis des advisors (règle 6 : le fondateur ne tranche rien de technique).

---

MÉTHODE DE TRAVAIL PAR PARTIES — à appliquer sur chaque chantier

But : garder la rigueur, supprimer les étapes qui ne rapportent rien.

1. UN CHANTIER = UNE ADR + 3 OU 4 PARTIES
- Avant tout code, une ADR (décision d'architecture) écrite, avec un plan (G0) :
  contexte, décisions, alternatives rejetées, conséquences chiffrées, plan de tests, découpage en parties.
- Circuit de l'ADR (le seul endroit où l'on prend le temps) :
  a) avis d'advisors indépendants (statistique, domaine, produit) : conseil, jamais verdict ;
  b) tableau de réconciliation : chaque demande d'advisor apparaît avec sa décision (adoptée, adoptée avec
     changement, reportée avec responsable et déclencheur mesurable, rejetée avec raison) ;
  c) contrôle par la session propriétaire de la production (checkpoint-1) ;
  d) validation du fondateur, en langage clair, sans question technique.
- Découpage type en parties : 1) moteur pur (calcul, sans effet sur ce qui est servi) ;
  2) intégration serveur (politique, gardes) ; 3) textes servis / surface publique ;
  4) éventuellement données.

2. UNE PARTIE = UN PLAN, UNE RELECTURE, UNE REVUE
- Un plan court de la partie (liste fermée des fichiers, tests, risques).
- Implémentation : les tests d'abord, avec des valeurs de référence indépendantes du code
  (calcul exact, force brute, littérature) ; montrer qu'ils échouent avant la correction.
- Mutations : pour chaque test, une modification volontaire du code qui doit le faire échouer.
  Une mutation qui survit = test à renforcer, jamais à retirer.
- UNE relecture (G2) par une instance neuve qui n'a pas écrit le code, sur toute la partie.
- UNE revue par la session propriétaire de la production, sur l'ensemble des PR de la partie.

3. TAILLE DES PR
- Remplir les PR jusqu'au plafond de taille du dépôt au lieu de les émietter.
- Une partie qui dépasse le plafond part en PR consécutives, relues et revues ensemble.
- Les documents (ADR, plans) ne comptent pas dans la taille.

4. ACCORDS ET FUSIONS
- Le fondateur donne son accord une fois par partie (pas à chaque push).
  Tout push hors d'une partie validée demande son accord.
- On fusionne soi-même sa PR quand : CI entièrement verte sur la tête courante,
  ET revue de la partie faite. Commit de fusion, jamais de réécriture d'historique.
- Une PR en retard sur la branche principale se met à jour par fusion, jamais par rebase ni push forcé.

5. COORDINATION ENTRE SESSIONS
- Une messagerie partagée (fichiers dans un dossier coordination/messages/), lue au début de chaque session.
- Tout push ou changement qui peut gêner l'autre session est annoncé AVANT d'être fait ;
  chaque fusion est écrite aussitôt après.
- On lit ce que l'autre a laissé avant d'agir.
- Un propriétaire par zone : on n'écrit jamais dans la zone d'un autre, on lui adresse une demande.
- Journal : une ligne datée par décision ou livraison ; les décisions du fondateur sont citées mot pour mot.

6. RÈGLES PERMANENTES
- Vérifier avant d'agir : lire le fichier, ses tests et ses appelants avant de modifier ; citer fichier:ligne.
- Chaque chiffre est sourcé ou recalculé, et marqué « calcul ».
- Le fondateur ne tranche rien de technique : les choix techniques vont aux advisors.
- Un échec de CI « instable » n'est pas une cause : relancer une seule fois, et consigner chaque occurrence.
- Aucune dette sans responsable et déclencheur mesurable.
