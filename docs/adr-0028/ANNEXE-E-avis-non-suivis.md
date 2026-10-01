# ADR-0028 — Annexe E : points où l'ADR ne suit pas les avis, ou les tranche autrement (C-1, reliquat)

Rédaction : 2026-09-29 (rédacteur `claude-opus-5-5`). C-1 demande cette liste. La mention « presque intégralement » que cite C-1 ne figure pas dans l'ADR (recherche : 0 occurrence dans `docs/adr-0028/`, `JOURNAL.md` et `docs/DECISIONS.md`) ; la liste est produite quand même.

Statuts :
- **suivi** ;
- **non suivi** : l'avis réservait le point à l'investisseur, et l'ADR le tranche par délégation, sous veto (§4.10 a) ;
- **tranché autrement** : par le cp-1 ou par le rédacteur ;
- **omis puis porté** : absent de la version du 2026-09-29 soumise au cp-1, ajouté par cette révision.

| id | avis (fichier, question, ligne) | recommandation de l'avis | dans ADR-0028 | statut |
|---|---|---|---|---|
| E-D1 | advisor-defi Q1, l.11-18 | option (a), règle générale | D1 | suivi |
| E-D1b | advisor-defi Q1 | la règle ne traite pas un flux mort dans une seule strate | D1 cas (b) : retrait de la seule strate, pour R1 et L&M ; k nominal alors imprimé par strate au bloc 1 | tranché autrement (rédacteur, **à ratifier**) |
| E-D1c | advisor-defi Q1, l.36 | acceptation d'ADR-0023 (pt 5 amendé) : acte de l'investisseur | D1 l'accepte par délégation | non suivi, veto §4.10 a |
| E-D2a | advisor-defi Q2 pt 4, l.46-51, l.69 | amender la décision 273 : décision de l'investisseur | D2 pt 4 l'amende par délégation | non suivi, veto §4.10 a |
| E-D2b | advisor-defi Q2 pt 9, l.58-62, l.70 | choix entre sensibilité par blocs et résidu déclaré : à l'investisseur | D2 pt 7 retient les blocs | non suivi, veto §4.10 a |
| E-D2c | advisor-defi Q2 pt 10, l.63 | G1/G2 sur fixtures, un seul rendu | D2 pt 9, durci par C-11 et C-12 (annexe D.4) | suivi, puis tranché autrement (cp-1) |
| E-D2d | advisor Q2, l.197, l.202 | poolé exploratoire ; « accepter qu'un résultat poolé soit publié comme exploratoire » = décision de message | étiquette en D2 pt 4 ; la publication n'était pas portée au §4 | omis puis porté (§4.10 a) |
| E-D3 | advisor-defi Q3, l.74-90 | variante de l'option A | D3 ; structure à deux étages déclarée (C-10 iv) | suivi |
| E-D4a | advisor-defi Q4, l.94-103 | coupe principale semi-ouverte ; troncature de tous les types | D4 | suivi |
| E-D4b | advisor-defi Q4, l.107 | « dire que la décision 270 contredit une ADR acceptée avant les données » | D4 reformulée : la décision de l'investisseur (produire le J14) est exécutée ; seule la coupe transcrite est remplacée | tranché autrement (cp-1 C-9) |
| E-D5a | advisor-defi Q5, l.111-121 | exclure aussi `asn_attribution` et `clock_check` | D5 | suivi |
| E-D5b | advisor-defi Q5, l.125 | l'extension d'ADR-0025 demande une ratification de l'investisseur (269) | D5 l'étend par délégation | non suivi, veto §4.10 a |
| E-D6a | advisor Q6, l.40-44 | option C : instrument non promu sous gates, sortie branchée | D6 réécrite : chemin de recalcul de qualité produit sous G0-G7, collecte en quarantaine | tranché autrement (cp-1 §4 pt 4, C-5) ; rejoint advisor-marché Q6, l.85-89 |
| E-D6b | advisor Q6, l.48 | garde-fou : tout changement hors des points 1 et 2 exige un G0 | absent de la version soumise | omis puis porté (D6 i) |
| E-D6c | advisor-marché Q6, l.88 | collecteur jetable **si** le format des journaux est spécifié et scellé | absent | omis puis porté (D6 vii ; SHOGEN-FORMAT-JOURNAUX-1) |
| E-D7 | advisor Q7 (d), l.71-73 | bundle, préfixe, reste après réponse sur le périmètre ; condition : relecture R-21 des 7 diffs ; `.claude/launch.json` (GC-13) part avec le préfixe | D7 suivi ; la condition et la mention manquaient | suivi ; omis puis porté (§4.3) |
| E-D8a | advisor Q8 (c), l.93-99 | lot neuf, collision consignée, tag puis suppression | D8 | suivi |
| E-D8b | advisor Q8 pt 2, l.97 | « la source canonique devient le blob de `adb2213`, sha cité » | absent | omis puis porté (D8) |
| E-D8c | advisor Q8, l.105 | l'investisseur confirme que la décision du 2026-08-20 tient dans sa forme g1/g3/g5 | absent du §4 | omis puis porté (§4.10 a) |
| E-D8d | advisor Q8, l.103 | G1 : cas positif `claude-sonnet-5-5`, cas négatif `claude-opus-5` | D8 ; étendu par C-14 | suivi |
| E-D8b-G1 | advisor Q8 pt 2, l.97 (source canonique = blob d'`adb2213`) ; cp-1 D8b C-2 ; revue G2 de D8b, C-G2-1, 2, 8, 9 | porter le blob `6789a30` tel quel | D8, lot D8b : blob porté avec des écarts nommés : messages en français et jetons ASCII `SECRETS/…` (CH-6) ; argument inconnu refusé au lieu du repli sur le mode indexé (CH-7) ; `LC_ALL=C` exporté (CH-8) ; références à `ADR-0004` (neuf lignes du blob) réattribuées à l'ADR-0004 de VibeGates (trois occurrences, en-tête) ou retirées des messages, `pass-4-report.md` cité en amont complet, deux pourcentages [abs] retirés, filet d'un scanner dédié déclaré absent (CH-5) ; mode `--history` ajouté (fonction neuve, D8b-3) ; type d'entrée lu par une pathspec `:(literal)` (C-G2-1 : un nom à caractère de glob était pris pour une autre entrée) ; `GIT_NO_REPLACE_OBJECTS=1` exporté (C-G2-2 : objets réels) ; chemins en forme d'identifiant masqués dans les constats et les avis non-blob (C-G2-8) ; variables de pathspec de l'appelant retirées (C-G2-9) | tranché autrement (G0 CH-5 à CH-8, cp-1 C-2 ; revue G2 C-G2-1, 2, 8, 9) |
| E-D9a | advisor Q9 (d), l.129-141 ; advisor-defi Q9, l.129-134 ; advisor-marché §5, l.58-83 | T0 d'abord ; voies A et B ; G4 en recherche dès maintenant ; S4 en dernier, conditionné à J28 | D9 | suivi |
| E-D9b | advisor-marché §5, l.91-97 | signal de demande falsifiable : acteur nommé hors de l'équipe, 90 jours après G9, trois formes | D9 citait le signal sans borne de temps ni condition « hors de l'équipe » | omis puis porté (D9), comme proposition soumise à l'investisseur (§4.10 b) |
| E-D9c | advisor Q9, l.137 ; advisor-marché §8, l.118 | options G5 (a)/(b) : décision du mainteneur | D9 prévoyait de les trancher « par ADR courte » | tranché autrement (cp-1 C-8) : rendues au mainteneur |
| E-D10a | advisor Q10, l.159-165 | E1 et fuzz maintenant ; le reste après S2 ; ADR « passage public par export filtré » | D10 | suivi |
| E-D10b | advisor Q10, l.174 | mécanisme du passage public (export filtré ou bascule) : investisseur | D10 le tranchait (export filtré) | tranché autrement (cp-1 C-8) : décision de l'investisseur (§4.10 b) |
| E-§4 | advisor-marché §8, l.113-120 | sept décisions de l'investisseur | §4, points 4, 5, 7, 8 et 9, et §4.10 | suivi. PXP-20, demandé par cet avis, est livré (JOURNAL l.92), ce n'est donc pas une omission |

## Amendement daté du 2026-09-30 (décisions A-1 à A-12 ; ADR §1 bis)

Rédaction : 2026-09-30, rédacteur `claude-opus-5-5` (contexte frais). Statut ajouté : **non suivi (A-n)** : l'orchestrateur, sous la délégation du 2026-09-30, tranche le point autrement sur le fond, par la décision A-n de DECISIONS-orchestrateur (`c082036f…`). Les points suivis sont dans la table de traçabilité de l'ADR (§1 bis). Les avis cités sont ceux du 2026-09-30 : AVIS-advisor (`fe6e4a8e…`) et AVIS-advisor-defi (`5619e2ac…`).

| id | avis (fichier, question) | recommandation de l'avis | dans ADR-0028 | statut |
|---|---|---|---|---|
| E-A1 | advisor, Q2 | règle à z_s seul ; z_bloc et sensibilités hors décision ; une discordance est une « fragilité déclarée » | règle à plancher d'erreur-type (§1 bis.1). Forme de l'avis suivie : renommage, z_s principal, « ≥ », valeur non arrondie, garde §5.4 dans la règle, non évaluable distinct du négatif, drapeau 2 hors règle, 2,576 offert sans recommandation. La règle de l'avis devient le repli (§1 bis.3) | non suivi sur le fond (A-1) ; suivi sur la forme (A-3, A-5) |
| E-A2 | advisor-defi, Q1 et Q2 | l'étiquette « sensibilité » reste à z_bloc, qui entre pourtant dans la décision | z_bloc est le plancher d'erreur-type de la règle ; amendement déclaré de D2 pt 7 (§1 bis.2) | non suivi (A-1 ; CV2-34) |
| E-A3 | advisor-defi, Q2 (texte, pt 2) | strate « non testée » dès que z_bloc n'est pas publiable | NE REJETTE PAS dès que z_s < 2,33 ; NON ÉVALUABLE réservé à la strate sous la garde §5.4 (non testée) et au rejet non qualifiable (§1 bis.1 pt 5) | non suivi (A-1 ; RECONCILIATION-Q2-advisor-defi §5 (ii) ; CV2-10) |
| E-A4 | advisor-defi, Q2 (texte, pt 3) | « niveau ≤ 0,01 » par strate, sans qualification | niveau asymptotique, conservateur sous fenêtres iid, non démontré en échantillon fini ; mesuré par SIM-NIVEAU avant le scellement (§1 bis.1 pt 7) | non suivi (A-1 ; RECONCILIATION-Q2-advisor-defi §5 (i)) |
| E-A5 | advisor-defi, Q4 (item 3) | bornes de censure « extérieures » à P̂_more fixé, avec la lecture « identifié sous censure arbitraire » | bornes à P̂ fixé étiquetées « non extérieures », sans lecture d'identification ; les bornes extérieures deviennent SHOGEN-CENSURE-INFO-2 (annexe D.5 amendée ; annexe B.6) | non suivi (A-6 ; CV2-24) |

E-D1b (ci-dessus, « à ratifier ») : ratifié par l'orchestrateur le 2026-09-29 (CB-8, rappelé par la DEMANDE Q4), confirmé par l'avis advisor-defi Q4 (item 6), avec la limite « flux presque mort » déclarée à l'annexe D.5 (amendement du 2026-09-30) et son item PAROXYSME SHOGEN-FLUX-QUASI-MORT-1 (annexe B.6 ; C-4 du cp-1 de l'amendement).
