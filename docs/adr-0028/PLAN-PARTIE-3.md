# Partie 3 de S2 — texte scellé : plan (2026-10-02 ; accord de l'investisseur du même jour)

Accord de l'investisseur (verbatim, 2026-10-02) : « oui, lance la partie 3 ». Rattachement : ADR-0028 D2 (contenu
du paquet, pts 1 à 10), §1 bis (règle SHOGEN-CRITERE-R1-1, décisions A-1 à A-12), D6 (viii) ; annexe A, ligne
PAQUET (cp-1 complet) ; annexe C (FM-1.1) ; annexe D (D.1 inventaire, D.2 pièces interdites, D.3 attestations,
D.4 c sceau) ; annexe B (items dont le déclencheur est « G0 du PAQUET », « avant le scellement » ou « partie 3 ») ;
`docs/adr-0028/PARTIES-S2.md` ; méthode `docs/METHODE-PARTIES.md`.

Branche : `partie-3-paquet`, depuis `claude/compassionate-noether-szmdyj` (`0711cc1`, `main` locale : passation,
partie 1, partie 2).

## 1. Étapes

| étape | contenu | qui |
|---|---|---|
| **P — préalables** | (P1) inventaire D.1 complété (exposition de l'orchestrateur de la session cloud, SHOGEN-EXPOSITION-ORCH-CLOUD-1), ligne D.2 (SHOGEN-E1-D2-COMPLETUDE-1), modèle d'attestation D.3 ; (P2) fiches d'agents du roster manquantes en cloud (lecteur `claude-sonnet-5-5` high, validateur `claude-fable-5-1` high, advisor `claude-fable-5-1` medium), actives au démarrage de la session suivante ; (P3) un lot de code court : SHOGEN-SCEAU-VERIFY-CHEMINS-1, et les petits items reportés au G0 du PAQUET (SENS-PLAGES-2, CONTEXTE-MUTABLE-1, RENDU-RENAME-POSIX-1, RENDU-STATUS-HEAD-1, GO-PICKAXE-1) | orchestrateur ; worker pour P3 |
| **L — lectures** | Künsch 1989 (P-01) aux pages visées par §1 bis.1 (pts 3 et 7) ; Fisher 1921 (P-03) ; état de SHOGEN-POOLEE-SOURCE-1 (Mantel-Haenszel 1959, Cochran 1954, Agresti 2013) ; versement à `biblio/` et entrées d'`INDEX.md` ; clause C-6 selon l'état de `biblio/` | lecteur ; orchestrateur pour le versement |
| **S — niveau de la garde** | SHOGEN-CRITERE-GARDE-NIVEAU-1 (cas de simulation, cp-1 du PAQUET) | worker |
| **R — rédaction** | `docs/adr-0028/PAQUET-PREREG-S2.md` : D2 pts 1 à 10, annexe D.5, textes dus au PAQUET par les items de l'annexe B, bloc machine `shogen-paquet-v1` (format fixé au G0 §C de la partie 2) | rédacteurs **frais**, sans accès aux pièces de D.2, attestation écrite |
| **V — validation** | validateur frais (cp-1 complet), contrôle non-LLM FM-1.1 des transcriptions des rédacteurs et du validateur (recherche des chemins de D.2), attestations D.3, re-consultation courte des advisors (SHOGEN-ATTEST-ADVISOR-1) | validateur, advisors ; orchestrateur pour FM-1.1 |
| **Sc — scellement** | sceau préparé (`scripts/sceau/make-tsq.sh` : `PAQUET.sha256`, `paquet.tsq`, `docs/adr-0028/sceau/README.md`) ; sha256 du paquet et du manifeste écrits au JOURNAL (= scellement) | orchestrateur |

Une relecture G2 par une instance neuve sur toute la partie, une revue de partie par l'orchestrateur, puis fusion
`--no-ff` dans la `main` locale.

## 2. Dépendances hors de la session (actes ou données de l'investisseur)

1. **Künsch 1989 et Fisher 1921** : dossier Drive `biblio-a-verser`, à ouvrir par lien quelques minutes (même
   procédé que `biblio`, passation §5 bis) — avant l'étape L.
2. **Empreintes complètes des journaux scellés et du fichier de sommes de clôture** (EX-E1-2) : elles ne sont que
   sur le poste local (`SHA256SUMS-cloture-2026-09-28.txt`) ; seule celle de `control.jsonl` est au dépôt (épingle
   `SHA_CONTROL_SCELLE`). Avant le bloc machine du paquet. Les journaux eux-mêmes ne viennent **pas** dans la
   session avant le scellement (D.2 n° 7 : pièces interdites aux rédacteurs frais).
3. **`cacert.pem` et `tsa.crt` de FreeTSA** (D.4 c) : leur téléchargement est un acte de l'investisseur, après la
   lecture des conditions d'usage (P-12) ; leurs sha256 complets entrent au bloc machine.
4. **Hôte de l'exécution unique** (SHOGEN-RENDU-HOTE-1) : à fixer avant le scellement (poste local ou session
   cloud) ; il conditionne OpenSSL et Python attestés au paquet.

## 3. Risques

- Exposition : la transcription de la session cloud de l'orchestrateur porte la cartographie l.51 (JOURNAL,
  05:56 UTC) ; elle n'est jamais transmise aux rédacteurs ni au validateur ; aucun brief n'en recopie rien.
- Fiches Fable 5.1 : actives seulement au démarrage d'une session ; sans elles, la validation attend.
- Rédacteurs frais : le contrôle FM-1.1 porte sur leurs appels d'outils (transcriptions des sous-agents de la
  session) ; un chemin de D.2 trouvé = rédaction refaite par une instance neuve.
