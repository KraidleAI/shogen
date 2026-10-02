#!/usr/bin/env bash
# Vérification hors ligne du sceau du paquet de pré-enregistrement S2 (ADR-0028 D2, annexe D.4 c ; décision A-9 du 2026-09-30).
# Entrées (dans docs/adr-0028/sceau/) : PAQUET.sha256 (manifeste : UTF-8 sans BOM, LF, format `sha256sum`, chemins
#   relatifs à la racine du dépôt, comme make-tsq.sh les écrit),
#   paquet.tsq (requête RFC 3161, générée localement), paquet.tsr (jeton rendu par la TSA), chain/cacert.pem, chain/tsa.crt.
# Sortie : 0 si (1) le manifeste re-vérifie les octets du paquet, (2) le jeton vérifie contre la requête et la chaîne publiée,
#   (3) le genTime du jeton est imprimé (horloge de la TSA, pas la nôtre). Sinon ≠ 0. Aucun réseau.
set -euo pipefail
D="${1:-docs/adr-0028/sceau}"
cd "$(git rev-parse --show-toplevel)"
echo "== (1) manifeste -> octets du paquet"
sha256sum -c "$D/PAQUET.sha256" || { echo "MANIFESTE : ÉCART" ; exit 2 ; }     # relu depuis la racine (SCEAU-VERIFY-CHEMINS-1)
echo "== (2) jeton RFC 3161 -> requête + chaîne (racine de confiance : la TSA nommée dans chain/)"
openssl ts -verify -in "$D/paquet.tsr" -queryfile "$D/paquet.tsq" -CAfile "$D/chain/cacert.pem" -untrusted "$D/chain/tsa.crt" || { echo "JETON : ÉCART" ; exit 3 ; }
echo "== (3) genTime du jeton (horloge de la TSA)"
openssl ts -reply -in "$D/paquet.tsr" -text | grep -E "Time stamp|Hash Algorithm|Message data|Serial|TSA" || true
echo "== empreinte du manifeste horodaté (celle que le jeton porte)"
sha256sum "$D/PAQUET.sha256"
echo "SCEAU : VÉRIFIÉ HORS LIGNE (sous confiance en la TSA nommée ; l'ancre n'atteste pas les lectures antérieures, annexe D.1/D.3)"
