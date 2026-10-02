#!/usr/bin/env bash
# Prépare LOCALEMENT la requête RFC 3161 du sceau (aucun envoi, aucun réseau) — décision A-9 (2026-09-30).
# 1. Fige le manifeste PAQUET.sha256 (UTF-8 sans BOM, LF, format `sha256sum -b`) sur les fichiers du paquet.
# 2. Génère paquet.tsq = requête d'horodatage sur les octets du manifeste (sha256, avec nonce, certificat demandé).
# L'ENVOI (curl vers la TSA) est un acte de l'investisseur (§4.10 b) : commande dans AU-REVEIL.
set -euo pipefail
D="${1:-docs/adr-0028/sceau}"
shift || true
cd "$(git rev-parse --show-toplevel)"
mkdir -p "$D/chain"
[ "$#" -ge 1 ] || { echo "usage: make-tsq.sh <dossier sceau> <fichier du paquet>..." ; exit 2 ; }
# convention unique du manifeste (SCEAU-VERIFY-CHEMINS-1, relue depuis la racine par verify.sh) : chemin relatif à
# la racine, sans « .. » ni lecteur ni barre inverse ; contrôlée avant toute écriture
for f in "$@"; do case "/$f/" in //*|*/../*|/[A-Za-z]:*|*\\*) echo "refus : $f hors de la convention du manifeste" ; exit 2 ;; esac ; done
# manifeste : chemins relatifs à la racine du dépôt, LF, sans BOM
: > "$D/PAQUET.sha256"
for f in "$@"; do sha256sum -b "$f" >> "$D/PAQUET.sha256"; done
sed -i 's/\r$//' "$D/PAQUET.sha256"
echo "manifeste :"; cat "$D/PAQUET.sha256"
echo "sha256 du manifeste (celui que le jeton portera) :"; sha256sum -b "$D/PAQUET.sha256"
openssl ts -query -data "$D/PAQUET.sha256" -sha256 -cert -out "$D/paquet.tsq"
openssl ts -query -in "$D/paquet.tsq" -text | head -20
echo "REQUÊTE PRÊTE : $D/paquet.tsq (rien n'a été envoyé)."
