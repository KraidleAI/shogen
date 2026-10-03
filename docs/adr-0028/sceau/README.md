# Sceau du paquet de pré-enregistrement S2 (ADR-0028 D2, annexe D.4 c ; §1 bis.11 pt 10)

Ce fichier est hors des octets scellés (CV2-27) : il porte ce que le paquet ne peut pas porter sur lui-même. Écrit le
2026-10-03 01:04:33 UTC (heure produite par le script d'écriture). Second sceau : il remplace, avant toute exécution, celui du 2026-10-02,
archivé tel quel dans `premier-2026-10-02/` (A-8 ; décision de l'investisseur « Corriger et resceller » ; lot CORR).

| élément | valeur |
|---|---|
| paquet | `docs/adr-0028/PAQUET-PREREG-S2.md`, commit `3be95be`, sha256 `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528` |
| manifeste (objet horodaté) | `PAQUET.sha256` (UTF-8 sans BOM, LF, format `sha256sum -b`, attribut `-text`), sha256 `519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9` |
| requête RFC 3161 | `paquet.tsq` (sha256 du manifeste, nonce, certificat demandé), préparée par `scripts/sceau/make-tsq.sh` le 2026-10-03 |
| chaîne de confiance | `chain/cacert.pem` (`2151b611…`), `chain/tsa.crt` (`8bfb0305…`), FreeTSA, inchangés depuis le premier sceau |
| scellement | sha256 du paquet et du manifeste écrits au JOURNAL le 2026-10-03 (entrée « SCELLEMENT … RÉVISÉ », commit `2d51940`) |
| premier sceau, cité | paquet `494d770d…8097` (`ddf8c54`), manifeste `680a95fd…`, genTime 2026-10-02T17:44:30Z ; n'ouvre plus aucune exécution |

## État des ancres

- **Ancre (1), FreeTSA (condition d'exécution)** : requête envoyée à `https://freetsa.org/tsr` le 2026-10-03 à
  01:04:10 UTC (horloge de la session), réponse HTTP 200 ; jeton `paquet.tsr`, 4 644 octets, sha256 `9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e`, numéro de
  série `0x08CFC8D5`. **genTime : 2026-10-03T01:04:10Z** (horloge de FreeTSA). `scripts/sceau/verify.sh` : sortie 0
  (manifeste → paquet OK ; jeton → requête, manifeste et chaîne : `Verification: OK` deux fois).
- **Échéance du délai de rétractation (A-7) : 2026-10-04T01:04:10Z.** Avant elle, la garde (5) refuse toute exécution ;
  après elle, l'exécution unique reste ouverte par un acte distinct de l'investisseur, jamais par l'horloge seule.
- **Ancre (2), OpenTimestamps (durabilité, hors des conditions d'exécution)** : non faite (client non installé ;
  dépendance nouvelle, R-8, sur go seulement).

## Vérifier

`bash scripts/sceau/verify.sh` (hors ligne) : le manifeste re-vérifie le paquet ; le jeton vérifie contre la requête,
contre les octets du manifeste et contre la chaîne ; genTime imprimé.

Limites (annexe D.4 c ; paquet §12 pt 16) : le jeton atteste l'existence des octets au plus tard à genTime, rien sur des
lectures antérieures des données (D.1, D.3) ; contrôle sous confiance en FreeTSA, opérateur individuel, sans accord de
niveau de service lu.
