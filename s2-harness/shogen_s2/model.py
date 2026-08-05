"""Modèle du relevé — un flux, une fenêtre, une lecture.

Conception : docs/10-mesures-pilotes-design.md §3.1 (le pool), §5.2 (les
définitions d'écart, dont la panne). Instrument JETABLE (10 §1) — il meurt
après le rapport S2, n'est pas un ancêtre du produit.

Décisions de rigueur, documentées ici parce que le mainteneur a délégué les
dilemmes techniques (2026-08-05) sous contrainte « solutions documentées » :

- **`Decimal`, jamais `float`, pour tout prix.** Le journal est recalculable
  offline (ADR-0003) ; un prix qui transite par un binaire flottant n'est
  plus recalculable à l'octet. On parse depuis la chaîne exacte de la source.
- **La devise est un champ du relevé, jamais une constante de classe**
  (10 §2, décision « BTC/USD-stable, devise marquée par flux » du 2026-08-05).
- **Précédence panne > staleness > hors-enveloppe** (10 §5.2) : une panne
  n'a pas de valeur, donc pas d'écart hors-enveloppe évaluable. Ici on ne
  décide que la panne (au décodage) ; staleness et hors-enveloppe sont des
  jugements de fenêtre calculés en aval (r1.py), pas à la lecture.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


class Status(enum.Enum):
    """Statut d'une lecture. Tout ce qui n'est pas OK est une panne (iii)
    au sens de 10 §5.2 — non-réponse, transport, ou indécodable."""

    OK = "ok"
    PANNE_HTTP = "panne_http"          # réponse reçue, statut != 200
    PANNE_TRANSPORT = "panne_transport"  # pas de réponse (timeout, DNS, reset)
    PANNE_DECODE = "panne_decode"      # 200 mais forme inattendue / indécodable


class Currency(enum.Enum):
    USD = "USD"
    USDT = "USDT"


@dataclass(frozen=True)
class Reading:
    """Une lecture datée d'un flux. `raw` sont les octets exacts de la
    réponse — conservés (journal recalculable, ADR-0005 : hash toujours,
    octets par politique ; pour ce benchmark on garde les deux)."""

    flux_id: str
    kind: str                      # "place" | "aggregator" | "oracle"
    endpoint: str
    fetch_ts: float                # epoch s, horloge du harnais (mesure)
    status: Status
    http_status: Optional[int] = None
    raw: bytes = b""
    price: Optional[Decimal] = None
    currency: Optional[Currency] = None
    source_ts: Optional[float] = None  # epoch s, horodatage PORTÉ par la source
    extra: dict = field(default_factory=dict)  # conf (Pyth), roundId (Chainlink)…

    @property
    def ok(self) -> bool:
        return self.status is Status.OK


class DecodeError(Exception):
    """Levée par un décodeur quand la forme 200 n'est pas celle attendue.
    Convertie en Status.PANNE_DECODE — jamais avalée en une valeur inventée
    (fail-closed de publication, 10 §5.2)."""
