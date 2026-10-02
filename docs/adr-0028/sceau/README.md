# Sceau du paquet de pré-enregistrement S2 (ADR-0028 D2, annexe D.4 c ; §1 bis.11 pt 10)

Ce fichier est hors des octets scellés (CV2-27) : il porte ce que le paquet ne peut pas porter sur lui-même.

| élément | valeur |
|---|---|
| paquet | `docs/adr-0028/PAQUET-PREREG-S2.md`, commit `ddf8c54`, sha256 `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097` |
| manifeste (objet horodaté) | `PAQUET.sha256` (UTF-8 sans BOM, LF, format `sha256sum -b`, attribut `-text`), sha256 `680a95fdf50908cea797ae4fe9f0b42c43b5a99fcad755cb410e26fa6e794209` |
| requête RFC 3161 | `paquet.tsq` (sha256 du manifeste, nonce, certificat demandé), préparée par `scripts/sceau/make-tsq.sh` le 2026-10-02 |
| chaîne de confiance | `chain/cacert.pem` (`2151b611…`), `chain/tsa.crt` (`8bfb0305…`), FreeTSA, téléchargés sur le go de l'investisseur du 2026-10-02 (JOURNAL) |
| scellement | sha256 du paquet et du manifeste écrits au JOURNAL le 2026-10-02 (entrée « SCELLEMENT ») |

## État des ancres

- **Ancre (1), FreeTSA (condition d'exécution)** : go de l'investisseur donné le 2026-10-02 (« go ancre FreeTSA », JOURNAL). Jeton : à demander après le commit du scellement ; `paquet.tsr`, genTime et échéance du délai seront ajoutés ici, par ajout daté.
- **Ancre (2), OpenTimestamps (durabilité, hors des conditions d'exécution)** : non faite (client non installé ; dépendance nouvelle, R-8, sur go seulement).

## Vérifier

`bash scripts/sceau/verify.sh` (hors ligne) : le manifeste re-vérifie le paquet ; le jeton vérifie contre la requête, contre les octets du manifeste et contre la chaîne ; genTime imprimé.

Limites (annexe D.4 c ; paquet §12 pt 16) : le jeton atteste l'existence des octets au plus tard à genTime, rien sur des lectures antérieures des données (D.1, D.3) ; contrôle sous confiance en FreeTSA, opérateur individuel, sans accord de niveau de service lu. Délai de 24 h à compter du genTime ; l'exécution unique est ouverte par un acte distinct de l'investisseur, jamais par l'horloge seule (D.4 b (5)-(6)).
