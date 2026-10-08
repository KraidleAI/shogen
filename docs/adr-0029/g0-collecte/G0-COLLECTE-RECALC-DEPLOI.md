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
