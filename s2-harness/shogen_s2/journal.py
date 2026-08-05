"""Le journal recalculable — deux logs append-only, JSONL.

Conception : docs/10-mesures-pilotes-design.md §6 (table de sortie
recalculable offline, ADR-0003) et ADR-0005 (rétention : hash toujours,
octets par politique — pour ce benchmark on garde les deux, donc le
DÉCODAGE lui-même est recalculable, pas seulement les statistiques).

Deux fichiers, séparés à dessein :
  - `journal.jsonl` : une ligne par (fenêtre × flux) — la valeur DÉCODÉE, la
    devise, les horodatages, le statut, et le sha256 des octets bruts. Suffit
    à recalculer toutes les statistiques R1/R2 offline.
  - `raw.jsonl` : une ligne par lecture — les octets bruts (base64) + leur
    sha256. Suffit à recalculer le DÉCODAGE offline, et à vérifier qu'aucun
    octet n'a bougé (le sha256 du journal doit y correspondre).

Le prix est stocké en CHAÎNE (repr Decimal exact) — jamais en flottant JSON,
qui casserait la recalculabilité à l'octet.
"""

from __future__ import annotations

import base64
import hashlib
import json

from .model import Reading


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def journal_entry(window_start: float, r: Reading) -> dict:
    """La ligne de `journal.jsonl` — valeur décodée + sha256, pas les octets."""
    return {
        "window_start": window_start,
        "flux_id": r.flux_id,
        "kind": r.kind,
        "currency": r.currency.value if r.currency else None,
        "status": r.status.value,
        "http_status": r.http_status,
        "price": str(r.price) if r.price is not None else None,  # Decimal exact
        "source_ts": r.source_ts,
        "fetch_ts": r.fetch_ts,
        "sha256_raw": sha256_hex(r.raw) if r.raw else None,
        "extra": r.extra,
    }


def raw_entry(window_start: float, r: Reading) -> dict:
    """La ligne de `raw.jsonl` — les octets bruts (base64) + leur sha256."""
    return {
        "window_start": window_start,
        "flux_id": r.flux_id,
        "fetch_ts": r.fetch_ts,
        "sha256_raw": sha256_hex(r.raw) if r.raw else None,
        "raw_b64": base64.b64encode(r.raw).decode("ascii") if r.raw else None,
    }


def append_jsonl(path: str, obj: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
