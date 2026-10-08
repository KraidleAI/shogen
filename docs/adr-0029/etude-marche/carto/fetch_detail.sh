#!/bin/bash
# Telecharge /protocol/{slug} pour les 30 cibles (reseau). Usage : bash fetch_detail.sh
cd "$(dirname "$0")"; mkdir -p raw/detail
for s in $(python3 -c "
import json
R={r['name']:r['slug'] for r in json.load(open('out/rows.json'))}; C=json.load(open('cibles.json'))
print(' '.join(R[n] for t in 'GMP' for n in C[t]))"); do
  curl -sS -m 90 -o raw/detail/$s.json -w "$s %{http_code} %{size_download}\n" https://api.llama.fi/protocol/$s
done
