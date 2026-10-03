"""R2 — les observables de diversité (§4), k_eff et le drapeau 2 (§5.6),
recalculés DEPUIS LE JOURNAL SEUL (ADR-0003). Ferme la Phase A (M1c).

Conception : docs/10-mesures-pilotes-design.md §4 (R2 : §4.1 axe ASN, §4.2 axe
contenu, §4.3 axe méthode), §5.5 pt 4 (corrélations entre clusters), §5.6 (k_eff
+ 2 drapeaux), §6 blocs 5-6 ; ADR-0007 (le certificat NOMME l'amont, jamais un
compte anonyme) ; ADR-0008 (une arête `basis:doc` seule ne partitionne pas —
elle DÉCLENCHE la mesure de contenu (b)) ; 04 §1 (les trois rangs) et §3 (k_eff =
nombre de classes de la partition R2 constatée).

**Nœud de partition = HÔTE, pas flux.** `okx_ticker` et `okx_index` partagent
`www.okx.com` → un seul hôte. C'est l'agrégation flux→source que M1b a différée
(lm.py) ET l'arithmétique de §4.1 (« k_eff = 2 pour k nominal = 5 » compte des
HÔTES). `k nominal = nombre d'hôtes distincts`. La carte flux→hôte est une clé
PORTEUSE de run_params (records.R2_LOAD_BEARING_KEYS) : elle gouverne la partition,
donc recalculable, jamais dérivée hors-bande de SPECS (sinon ADR-0003 casse).

**Injection de dépendances (résolution ASN)** : `collect_asn` prend un `resolve_fn`
injectable — mock par fixtures pour les tests déterministes ; DoH + RIPEstat réels
pour la campagne (que l'ORCHESTRATEUR lance, pas ce worker). Point d'entrée SÉPARÉ
de `collector.collect` : un défaut de résolveur réel n'entre jamais dans le chemin
de collecte de prix. Les enregistrements ASN vont dans `control.jsonl`
(`record:"asn_attribution"`, ignoré par `parse_control`, lu par `records.parse_asn`)
— pas de 4ᵉ fichier, recalculabilité préservée.

**Décisions de conception (renvois doc 10 ; arbitrages ADVISOR 2026-08-20)** :
  - **Fusion contenu** : 04 §3 ne fixe AUCUN seuil de fusion contenu (le « 0,999 »
    de 04 §1 est un exemple non normatif) ; ADR-0008 dit que `basis:doc` déclenche
    (b) mais ne fusionne pas. En v0, **seule l'identité exacte** fusionne sur l'axe
    contenu (série au tick identique sur TOUTES les fenêtres communes, N ≥ N_min,
    série non constante — « quasi-signature de copie », §4.2 (2b)) ; tout signal
    plus faible (ρ_resid haut) est publié comme CORROBORATION et désigne où mesurer,
    sans fusionner. Le rapport le déclare : « aucun seuil de fusion contenu sourcé
    en v0 ». Zéro seuil sans source (doc 03).
  - **Grille temporelle** : §4.2 écrit w = 1 s (places) / 10 s (agrégats) ; la
    décision mainteneur 5 (§9) fixe w = 60 s et le journal n'a QUE cette grille. Le
    contenu se calcule sur la grille du journal (w de run_params) ; la grille fine
    de §4.2 est remplacée par la décision budget §9 — écrit au bloc 5, jamais une
    déviation de spec silencieuse.
  - **k_eff « non mesuré » ≠ k_eff = k nominal** : sans enregistrement ASN, la
    partition dégénère en singletons — publiée « axe ASN non mesuré, k_eff non
    évaluable », JAMAIS un k_eff fabriqué par absence de donnée. Un hôte à résolution
    échouée = singleton « non attribué » ; RIPEstat ≠ Cymru = pas de fusion +
    discordance publiée (jamais « choisir une base »).
  - **Drapeau 2 tri-état** (règle SHOGEN-CRITERE-R1-1, pt 10 ; `drapeau_2`) : levé
    (« R1 discrimine » VRAI ∧ k_eff = k nominal, k_eff non borne supérieure) / éteint
    (FAUX, ou VRAI ∧ k_eff < k nominal) / non évaluable (k_eff non évaluable, « R1
    discrimine » NON ÉVALUABLE, ou VRAI ∧ borne supérieure égale à k nominal). La
    localisation consomme la matrice de co-écarts complète de M1b (lm.pair_phi) sur
    les paires inter-clusters.
  - **(K,z) co-aberrance** : marginales par signe observées, puis RÉUTILISE tel quel
    le trio r1.gate_value/z_score/binomial_tail_ge avec la garde §5.4 — « la
    machinerie de §5.1 recalculée sur les résidus » (§4.2 (2c)).

`Decimal` partout, précision FIXÉE (`r1.DECIMAL_PREC`) sur TOUT chemin numérique
(y compris `Decimal.ln`/`.sqrt`, correctement arrondis donc bit-identiques) →
recalcul identique par l'oracle (ADR-0003). Zéro dépendance hors stdlib.
"""

from __future__ import annotations

import socket
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, localcontext
from itertools import combinations
from typing import Callable, Optional

from . import r1, records
from .r1 import (
    DECIMAL_PREC,
    SEUIL_HIST,
    SEUIL_Z,
    _median,
    binomial_tail_ge,
    build_reading_map,
    build_window_strate,
    contexte_decimal,
    gate_value,
    z_score,
)
from .window import verify_markers_against_spec

# ── Les sept résidus de l'axe ASN (§4.1, verbatim — publiés avec la table) ─────
# Un observable R2 est lui-même un témoignage avec ses résidus (04 §4, pt 4).
RESIDUS_ASN: tuple[str, ...] = (
    "1. Fronting CDN/anycast : l'IP observée est la couche de LIVRAISON, pas "
    "l'origine. Côté origine, le regroupement peut être un faux positif ; côté "
    "livraison, le mode commun est réel (une panne du CDN partagé co-interrompt les "
    "chemins). Le certificat dit laquelle il compte — k_eff ici est « côté livraison ».",
    "2. Même ASN ≠ même opérateur ; ASN distincts ≠ opérateurs distincts.",
    "3. Mono-vantage : re-mesure depuis un seul point d'observation. v0 : UN résolveur "
    "par relevé (Cloudflare DoH-JSON, `cloudflare-dns.com` = le résolveur 1.1.1.1 de "
    "§4.1) — le résolveur EXACT est journalisé par enregistrement (champ `resolver`, "
    "auditable). La sonde MULTI-résolveurs de familles distinctes et multi-vantage "
    "prescrite par 10 §4.1 reste DUE au lancement de campagne (endpoints par famille à "
    "établir sur pièce — Google = dns.google/resolve, Quad9 dédié — plan §2 [C3]) ; "
    "écart au design nommé, jamais prétendu comblé.",
    "4. Instantanéité : TTL court ; l'attribution est un instantané daté, re-mesuré à "
    "chaque quorum (une divergence d'ASN entre deux relevés du même hôte est publiée, "
    "jamais écrasée en silence).",
    "5. Le chemin de mesure appartient à la classe mesurée : la résolution passe par un "
    "résolveur (Cloudflare `cloudflare-dns.com`) pour mesurer une dépendance à Cloudflare. "
    "Atténuation v0 : attribution croisée sur 2 bases BGP — la jambe RIPEstat va en HTTPS "
    "DIRECT vers stat.ripe.net (hors-résolveur). Les résolveurs de familles distinctes "
    "sont DUS à la campagne (résidu 3, plan §2 [C3]). En v0 les DEUX étapes DNS (A et "
    "Cymru TXT) transitent par le résolveur Cloudflare — le résidu est à son MAXIMUM, publié.",
    "6. RIPEstat et Team Cymru sont eux-mêmes des témoins (vues BGP, registres) ; leur "
    "concordance est une observation, pas une décharge — portée par A(asn-attribution) "
    "au registre (08 §8).",
    "7. La chaîne CNAME est un fait daté : un CNAME déterministe aujourd'hui peut "
    "changer demain.",
)

# ── Les cinq arêtes méthode (§4.3, `basis:doc`) — déclenchent (b), ne fusionnent
# pas (ADR-0008). Données re-établies le 2026-08-05 ; les 4 pages HTML sont passées
# par le résumeur de fetch (copie octets-exacts en dette 10 §10.4), seul llms-full.txt
# est verbatim-fiable. `basis:"doc"` sur chacune.
METHOD_EDGES: tuple[dict, ...] = (
    {
        "kind": "estimator",
        "node": "coingecko",
        "estimator": "filtre d'outliers par bornes MAD, puis VWAP des tickers restants",
        "panel_declared": "familles BTC/USD, USDT, USDC, EUR",
        "doc_url": "coingecko.com/en/methodology",
        "doc_fetched": "2026-08-05",
        "basis": "doc",
    },
    {
        "kind": "upstream",
        "from": "binance",
        "to": "coingecko",
        "relation": "intégration (table des marchés spot, 1372 paires au 2026-08-05 — "
        "chiffre daté) ; granularité « intégration », pas « ticker-set » (§3.2)",
        "doc_url": "coingecko.com/en/exchanges/binance",
        "doc_fetched": "2026-08-05",
        "basis": "doc",
    },
    {
        "kind": "estimator",
        "node": "pyth",
        "estimator": "médiane non pondérée des votes des publishers (p, p+c, p−c) ; "
        "« a hybrid between a mean and a median » (PAS « médiane pondérée par la "
        "confiance », formulation inexacte à ne pas réintroduire, §4.3)",
        "panel_declared": "publishers déclarés",
        "doc_url": "docs.pyth.network/price-feeds/how-pyth-works/price-aggregation",
        "doc_fetched": "2026-08-05",
        "basis": "doc",
    },
    {
        "kind": "upstream",
        "from": "coinbase",
        "to": "pyth",
        "relation": "Coinbase nommé publisher au NIVEAU RÉSEAU ; l'attribution au feed "
        "BTC/USD précis N'EST PAS établie (dette 10 §10.3) ; granularité « réseau »",
        "doc_url": "pyth.network/publishers",
        "doc_fetched": "2026-08-05",
        "basis": "doc",
    },
    {
        "kind": "upstream",
        "from": "coingecko",
        "to": "defillama",
        "relation": "« Almost all tokens are priced using CoinGecko's API » ; BTC "
        "majeur → coins.llama.fi n'est PAS un chemin d'amont distinct de coingecko",
        "doc_url": "docs.llama.fi/llms-full.txt",
        "doc_fetched": "2026-08-05",
        "basis": "doc",
    },
)

# Caveat §3.2 : pour la lecture on-chain, l'ASN mesuré est celui du fournisseur RPC
# (chemin de lecture), PAS l'amont du feed. Tout cluster touchant cet hôte le porte.
RPC_READ_PATH_HOST = "ethereum-rpc.publicnode.com"
CAVEAT_RPC_READ_PATH = (
    "chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC "
    f"({RPC_READ_PATH_HOST}), une infrastructure de lecture, pas l'amont du feed"
)

# Paramètres de contenu — VALEURS DU DESIGN (§4.2), pas inventées ; écrites dans
# run_params (PORTEUSES) → publiées et recalculables. Les paramètres laissés
# symboliques par le doc (ℓ, L) sont fixés en v0 et enregistrés : un balayage
# enregistré n'est pas un chiffre inventé (arbitrage ADVISOR 2026-08-20).
CONTENT_N_MIN = 300          # §4.2 : choix de conception (fenêtres communes par paire), non dérivé ;
                             # SE(artanh r) = 1/√(N−3) : biblio/INDEX.md, STAT 509 L7 §7.8 ; la valeur ici fait foi
CONTENT_KAPPA = 5            # §4.2 (2c) κ = 5 : aberrant si |e_s(j)| > κ·MAD_j(pool)
CONTENT_JUMP_SIGMA = 4       # §4.2 (2d) sauts |r_s(j)| > 4σ
CONTENT_DELTA_SECONDS = 60   # §4.2 (2b) contrôle décalé Δ = 60 s
CONTENT_LAG_L = 0            # v0 : co-aberrance à lag ℓ = 0 (même fenêtre) — enregistré
CONTENT_BIG_L = 3            # v0 : corrélation croisée δ aux lags −L..+L — enregistré
TICK_RULE_DEFAULT = "exact"  # quantification au tick : identité Decimal octet-exacte

GRID_NOTE = (
    "grille §4.2 (w=1s places / 10s agrégats) REMPLACÉE par la décision budget §9 "
    "(w=60s, décision mainteneur 5 du 2026-08-05) — contenu calculé sur la grille du "
    "journal (w de run_params), sur toutes les fenêtres (hors stratification R1 §5.3)"
)
MERGE_CRITERION_V0 = (
    "identité exacte T==1 sur ≥ N_min fenêtres communes, série non constante — SEUL "
    "critère de fusion contenu v0 (aucun seuil de corrélation sourcé : 04 §3 n'en fixe "
    "pas, le « 0,999 » de 04 §1 est un exemple ; ADR-0008 : basis:doc déclenche (b), "
    "ne fusionne pas). ρ_resid haut = corroboration publiée, désigne où mesurer."
)
COAB_STALENESS_NOTE = (
    "co-aberrance = |e_s(j)| > κ·MAD_j(pool) (§4.2 (2c)) ; le « ou staleness » du "
    "design est déjà porté par l'écart (ii) de R1 (§5.2) — non re-plombé ici, résidu nommé"
)


# ── Carte flux→hôte (l'agrégation flux→source de §5.5, réalisée) ───────────────

def flux_host(endpoint: str) -> str:
    """Hôte d'un endpoint (`urllib.parse`, stdlib). `okx_ticker` et `okx_index`
    rendent tous deux `www.okx.com` → un seul nœud de partition."""
    host = urllib.parse.urlparse(endpoint).hostname
    if not host:
        raise ValueError(f"endpoint sans hôte résoluble : {endpoint!r}")
    return host


def build_flux_hosts(specs) -> dict[str, str]:
    """Carte {flux_id: hôte} depuis les specs — écrite dans run_params (PORTEUSE)
    pour que la partition soit recalculable sans accès à SPECS (ADR-0003)."""
    return {s.flux_id: flux_host(s.endpoint) for s in specs}


def hosts_of_pool(flux_hosts: dict[str, str], pool: list[str]) -> list[str]:
    """Hôtes distincts du pool, triés (k nominal = len de cette liste)."""
    return sorted({flux_hosts[f] for f in pool if f in flux_hosts})


def flux_by_host(flux_hosts: dict[str, str], pool: list[str]) -> dict[str, list[str]]:
    """{hôte: [flux servis]} — okx apporte 2 flux à son hôte."""
    out: dict[str, list[str]] = {}
    for f in pool:
        h = flux_hosts.get(f)
        if h is not None:
            out.setdefault(h, []).append(f)
    return {h: sorted(v) for h, v in out.items()}


# ── Résolution ASN : le seam injectable (DI OBLIGATOIRE) ───────────────────────
# Le résolveur RÉEL (DoH + RIPEstat) n'est jamais lancé par ce worker ni exercé par
# les tests (comme sources.read : réseau, testé par fixtures gelées + smoke). Les
# tests injectent un mock déterministe. L'orchestrateur lance le réel à la campagne.

_UA = "Mozilla/5.0 (Shogen-S2-harness; +https://github.com/KraidleAI/shogen)"
_ASN_TIMEOUT = 15.0
# v0 : UN résolveur documenté (résidu 3). `cloudflare-dns.com` EST l'endpoint DoH-JSON
# de Cloudflare 1.1.1.1 (le résolveur de §4.1) — forme JSON LUE VIA FETCH (résumeur) le
# 2026-08-20 (developers.cloudflare.com/1.1.1.1/.../dns-json/ : GET
# https://cloudflare-dns.com/dns-query?name=&type=, header `accept: application/dns-json`,
# réponse `Answer[]` avec `type`/`data`). RANG (b) doc, comme les fetches §4.3 (résumeur,
# non octet-exact) — ré-établissement octet-exact des endpoints (Cloudflare/RIPEstat/Cymru)
# DÛ à [C3] avant le run. Le multi-résolveurs de §4.1 est DÛ à la campagne (endpoints par
# famille à établir sur pièce) — jamais deviné ici.
_DEFAULT_RESOLVERS = ("cloudflare-dns.com",)


def _doh_query(resolver: str, name: str, rrtype: str, timeout: float) -> dict:
    """Une requête DNS-over-HTTPS JSON (schéma Google/Cloudflare `application/dns-json`,
    forme lue via fetch 2026-08-20 — rang doc, non exercée par les tests) vers `resolver`
    — stdlib pure (urllib), aucune clé. Rend le JSON décodé (`Answer` porte A(type 1)/
    CNAME(type 5)/TXT(type 16))."""
    import json
    url = (f"https://{resolver}/dns-query?name={urllib.parse.quote(name)}"
           f"&type={rrtype}")
    req = urllib.request.Request(url, headers={"User-Agent": _UA,
                                               "Accept": "application/dns-json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _ripestat_asn(ip: str, timeout: float) -> tuple[Optional[int], Optional[str], Optional[str]]:
    """RIPEstat prefix-overview : (asn, holder, prefix). Base BGP n°1 (HTTPS DIRECT,
    hors-résolveur). Stdlib pure. Forme lue via fetch 2026-08-20, rang doc
    (stat.ripe.net/docs prefix-overview : `data.asns[]` porte `asn`/`holder`,
    `data.resource` = préfixe requêté) — ré-établissement octet-exact dû à [C3]."""
    import json
    url = f"https://stat.ripe.net/data/prefix-overview/data.json?resource={ip}"
    req = urllib.request.Request(url, headers={"User-Agent": _UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        d = json.loads(resp.read())["data"]
    asns = d.get("asns") or []
    asn = int(asns[0]["asn"]) if asns else None
    holder = asns[0].get("holder") if asns else None
    return asn, holder, d.get("resource")


def _cymru_asn(ip: str, resolver: str, timeout: float) -> Optional[int]:
    """Team Cymru par DoH TXT sur `<d.c.b.a>.origin.asn.cymru.com` — base BGP n°2,
    DISTINCTE de RIPEstat (§4.1). Forme TXT lue via fetch 2026-08-20, rang doc
    (team-cymru.com/.../ip-asn-mapping : octets INVERSÉs + zone ; TXT =
    « ASN | prefix | cc | registry | date ») — ré-établissement octet-exact dû à [C3].
    Attribution croisée. Stdlib pure."""
    octets = ip.split(".")
    if len(octets) != 4:
        return None  # IPv6 non couvert par cette forme Cymru (résidu publié)
    name = ".".join(reversed(octets)) + ".origin.asn.cymru.com"
    j = _doh_query(resolver, name, "TXT", timeout)
    for ans in j.get("Answer", []):
        txt = ans.get("data", "").strip('"')
        # forme « <ASN> | <prefix> | <cc> | <registry> | <date> » (1er champ = ASN)
        first = txt.split("|", 1)[0].strip()
        if first.split():
            try:
                return int(first.split()[0])
            except ValueError:
                continue
    return None


def resolve_host_real(host: str, resolvers: tuple[str, ...] = _DEFAULT_RESOLVERS,
                      timeout: float = _ASN_TIMEOUT) -> dict:
    """Résolveur RÉEL (campagne uniquement — NON lancé par ce worker) : DoH A →
    RIPEstat (base 1) + Cymru (base 2) sur l'IP primaire, résolveur du premier de
    la famille. Rend un dict `asn_attribution` (sans le champ `record`). Fail-soft :
    toute exception réseau → status `resolve_failed` (jamais une valeur inventée)."""
    try:
        resolver = resolvers[0]
        a = _doh_query(resolver, host, "A", timeout)
        answers = a.get("Answer", [])
        cname_chain = [x["data"] for x in answers if x.get("type") == 5]
        ips = [x["data"] for x in answers if x.get("type") == 1]
        if not ips:
            return {"host": host, "status": "resolve_failed", "resolver": resolver,
                    "note": "aucun enregistrement A"}
        ip = ips[0]
        asn_r, holder, prefix = _ripestat_asn(ip, timeout)
        asn_c = _cymru_asn(ip, resolver, timeout)
        return {
            "host": host, "status": "ok", "resolver": resolver,
            "ip": ip, "ip_secondary": ips[1:], "cname_chain": cname_chain,
            "prefix": prefix, "asn_ripestat": asn_r, "asn_cymru": asn_c,
            "holder": holder,
        }
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError,
            KeyError, ValueError) as e:
        return {"host": host, "status": "resolve_failed",
                "resolver": resolvers[0] if resolvers else None, "note": str(e)}


def collect_asn(
    specs,
    control_path: str,
    *,
    resolve_fn: Callable[..., dict] = resolve_host_real,
    resolvers: tuple[str, ...] = _DEFAULT_RESOLVERS,
    now_fn: Callable[[], float] = None,
    pool: Optional[list[str]] = None,
) -> list[dict]:
    """Sonde ASN de chaque HÔTE distinct du pool (1 relevé/hôte) et écrit un
    enregistrement `asn_attribution` DATÉ au journal de contrôle (append-only,
    recalculable). Point d'entrée SÉPARÉ de `collector.collect` — l'orchestrateur
    l'invoque au lancement de campagne. `resolve_fn` INJECTABLE (mock en test).
    Chaque enregistrement porte : hôte, flux servis, IP(+secondaires), préfixe, les
    DEUX attributions (RIPEstat, Cymru), holder (nom d'AS pour ADR-0007), résolveur,
    heure — la table ASN datée de §6 bloc 5, recalculable."""
    import time as _time
    if now_fn is None:
        now_fn = _time.time
    if pool is None:
        pool = [s.flux_id for s in specs]
    fh = build_flux_hosts(specs)
    fbh = flux_by_host(fh, pool)
    out: list[dict] = []
    for host in sorted(fbh):
        ts = now_fn()
        res = resolve_fn(host, resolvers)
        rec = records.asn_attribution_record(host=host, flux=fbh[host], ts=ts,
                                              resolvers=list(resolvers), attribution=res)
        records.append_asn(control_path, rec)
        out.append(rec)
    return out


# ── Attribution ASN par hôte : concordance, discordance, échec ─────────────────

def _asn_state(rec: dict) -> dict:
    """État d'attribution d'un hôte depuis son enregistrement : concordant (les deux
    bases s'accordent → ASN mergeable), discordant (RIPEstat ≠ Cymru → pas de fusion),
    non attribué (résolution échouée ou une base muette). Jamais « choisir une base »."""
    if rec is None:
        return {"attributed": False, "reason": "hôte non sondé (aucun enregistrement)",
                "kind": "missing"}
    if rec.get("status") != "ok":
        return {"attributed": False, "kind": "resolve_failed",
                "reason": rec.get("note", "résolution échouée")}
    ar = rec.get("asn_ripestat")
    ac = rec.get("asn_cymru")
    if ar is None or ac is None:
        return {"attributed": False, "kind": "one_base_silent",
                "reason": f"une base muette (RIPEstat={ar}, Cymru={ac}) — pas de fusion"}
    if ar != ac:
        return {"attributed": False, "kind": "discordant", "asn_ripestat": ar,
                "asn_cymru": ac,
                "reason": f"RIPEstat={ar} ≠ Cymru={ac} — discordance publiée, pas de fusion"}
    return {"attributed": True, "kind": "concordant", "asn": ar,
            "holder": rec.get("holder"), "reason": f"AS{ar} cross-confirmé (RIPEstat=Cymru)"}


class _UnionFind:
    """Union-find déterministe (racine = plus petit élément trié) pour la partition."""

    def __init__(self, items: list[str]):
        self.parent = {x: x for x in items}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            lo, hi = sorted((ra, rb))
            self.parent[hi] = lo

    def classes(self) -> dict[str, list[str]]:
        cl: dict[str, list[str]] = {}
        for x in self.parent:
            cl.setdefault(self.find(x), []).append(x)
        return {r: sorted(v) for r, v in cl.items()}


# ── Statistiques de contenu (§4.2) — Decimal, précision FIXÉE ──────────────────
# Tous les logarithmes passent par `lnprice_by_window` (précalcul unique, `Decimal.ln`
# à prec fixée = correctement arrondi → bit-identique, ADR-0003).

def pearson(xs: list[Decimal], ys: list[Decimal]) -> tuple[Optional[Decimal], str]:
    """Corrélation de Pearson SIGNÉE de deux séries appariées, précision FIXÉE.
    None si n < 2 ou une série est constante (variance nulle → ρ non défini) — jamais
    un 0 fabriqué (fail-closed de publication, §5.2). Rend (ρ, note)."""
    with localcontext(contexte_decimal()):
        n = len(xs)
        if n < 2:
            return None, f"n={n} < 2 — corrélation non définie"
        mx = sum(xs, Decimal(0)) / Decimal(n)
        my = sum(ys, Decimal(0)) / Decimal(n)
        cov = sum(((x - mx) * (y - my) for x, y in zip(xs, ys)), Decimal(0))
        vx = sum(((x - mx) ** 2 for x in xs), Decimal(0))
        vy = sum(((y - my) ** 2 for y in ys), Decimal(0))
        if vx == 0 or vy == 0:
            return None, "série constante (variance nulle) — ρ non défini"
        return +(cov / (vx * vy).sqrt()), "ok"


def _sgn(x: Decimal) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def price_map(readings: list, markers: list) -> tuple[list[int], dict]:
    """(fenêtres complétées triées ; carte (ws,flux)→ligne) — dédup marqueurs +
    last-wins, comme R1/L&M (helpers partagés → zéro divergence)."""
    win_strate = build_window_strate(markers)
    reading_map = build_reading_map(readings)
    return sorted(win_strate), reading_map


def _price_at(reading_map: dict, ws: int, f: str) -> Optional[Decimal]:
    rd = reading_map.get((ws, f))
    if rd is None or rd.get("status") != "ok" or rd.get("price") is None:
        return None
    return Decimal(rd["price"])


def lnprice_by_window(wins: list[int], reading_map: dict) -> dict[int, dict[str, Decimal]]:
    """PRÉCALCUL une fois : {ws: {flux: ln p}} pour toutes les cellules répondantes,
    `Decimal.ln` à précision FIXÉE. Toutes les statistiques ln-based (ρ_raw, ρ_resid,
    (K,z), δ) le partagent → coût O(fenêtres × flux) au lieu de O(paires × fenêtres² ×
    flux) (chaque ln calculé UNE fois, jamais par paire). Bit-identique : même valeur,
    calculée une fois ou N fois (arrondi correct, prec fixée — ADR-0003)."""
    out: dict[int, dict[str, Decimal]] = {}
    with localcontext(contexte_decimal()):
        for (ws, f), rd in reading_map.items():
            if rd.get("status") == "ok" and rd.get("price") is not None:
                p = Decimal(rd["price"])
                if p > 0:
                    out.setdefault(ws, {})[f] = +p.ln()
    return out


def log_returns(wins: list[int], lnp: dict, f: str, w: int) -> dict[int, Decimal]:
    """r_f(j) = ln p_f(j) − ln p_f(j−1) — DÉFINI seulement si j ET j−1 répondent ET
    sont adjacents (ws_j − ws_{j−1} == w). Un trou → rendement non défini, exclu et
    non ponté (un rendement enjambant un trou a la mauvaise variance). Clé = ws de j.
    Consomme le précalcul `lnp` (lnprice_by_window)."""
    out: dict[int, Decimal] = {}
    with localcontext(contexte_decimal()):
        for k in range(1, len(wins)):
            ws, prev = wins[k], wins[k - 1]
            if ws - prev != w:
                continue
            cur, pre = lnp.get(ws, {}), lnp.get(prev, {})
            if f in cur and f in pre:
                out[ws] = +(cur[f] - pre[f])
    return out


def rho_raw(wins, lnp, a, b, w, n_min) -> dict:
    """(1) ρ_raw : Pearson des log-rendements par paire (§4.2). ≈ 1 pour toute paire
    HONNÊTE (facteur marché) — un ρ_raw *bas* est le signal étrange. Garde N_min
    (choix de conception ; SE(artanh r) = 1/√(N−3), STAT 509 L7 §7.8) : sous le seuil, « historique de contenu insuffisant », jamais un ρ vide."""
    ra, rb = log_returns(wins, lnp, a, w), log_returns(wins, lnp, b, w)
    common = sorted(set(ra) & set(rb))
    if len(common) < n_min:
        return {"rho": None, "n": len(common), "sufficient": False,
                "note": f"historique de contenu insuffisant (n={len(common)} < N_min={n_min})"}
    rho, note = pearson([ra[j] for j in common], [rb[j] for j in common])
    return {"rho": rho, "n": len(common), "sufficient": True, "note": note}


def rho_resid(wins, lnp, a, b, n_min, k_min=4) -> dict:
    """(2a) ρ_resid : Pearson des résidus au pool e_s(j) = ln p_s(j) − ln m(j), où
    m(j) = médiane LEAVE-TWO-OUT des ln-prix (excl. a,b ; ≥ k_min=4 autres répondantes
    par fenêtre, §4.2). S'écarter du pool ENSEMBLE = signal d'amont commun. C'est aussi
    le résidu de peg USDT/USD (§9.4) pour les paires USDT×USD. Garde N_min. Une fenêtre
    à < k_min autres répondantes est exclue (jamais un résidu au pool mal défini).
    Consomme le précalcul `lnp` (O(fenêtres × flux), plus de re-balayage par paire)."""
    xa, xb, ncommon = [], [], []
    with localcontext(contexte_decimal()):
        for ws in wins:
            cell = lnp.get(ws, {})
            if a not in cell or b not in cell:
                continue
            others_ln = [v for f, v in cell.items() if f not in (a, b)]  # leave-two-out
            if len(others_ln) < k_min:
                continue
            m = _median(others_ln)                       # médiane leave-two-out des ln-prix
            xa.append(+(cell[a] - m)); xb.append(+(cell[b] - m)); ncommon.append(ws)
    if len(ncommon) < n_min:
        return {"rho": None, "n": len(ncommon), "sufficient": False,
                "note": f"historique de contenu insuffisant (n={len(ncommon)} < N_min={n_min})"}
    rho, note = pearson(xa, xb)
    return {"rho": rho, "n": len(ncommon), "sufficient": True, "note": note}


def _quantize(p: Decimal, tick_rule: str) -> Decimal:
    """Quantification au tick q_s(j). tick_rule « exact » = valeur Decimal telle
    quelle (identité octet-exacte = quasi-signature de copie, §4.2 (2b)) ; sinon un
    quantum décimal (ex. « 0.01 »)."""
    if tick_rule == "exact":
        return p
    with localcontext(contexte_decimal()):
        return p.quantize(Decimal(tick_rule))


def tick_identity(wins, reading_map, a, b, w, n_min, tick_rule, delta_windows) -> dict:
    """(2b) T, T_Δ : taux d'identité au tick. T = fenêtres où q_a(j)==q_b(j) ; T_Δ =
    contrôle décalé (q_a(j) vs q_b(j+Δ)) — « collision attendue au tick » calibrée par
    la ligne de base décalée. T ≫ T_Δ = signal de copie. Sur copie exacte, T=1."""
    price_a = {ws: _price_at(reading_map, ws, a) for ws in wins}
    price_b = {ws: _price_at(reading_map, ws, b) for ws in wins}
    n_common = eq = 0
    values_seen = set()
    for ws in wins:
        pa, pb = price_a[ws], price_b[ws]
        if pa is None or pb is None:
            continue
        n_common += 1
        qa, qb = _quantize(pa, tick_rule), _quantize(pb, tick_rule)
        values_seen.add(qa)
        if qa == qb:
            eq += 1
    # contrôle décalé : q_a(j) vs q_b(j') où j' est la fenêtre à ws + Δ·w
    n_shift = eq_shift = 0
    ws_set = set(wins)
    for ws in wins:
        pa = price_a[ws]
        ws2 = ws + delta_windows * w
        if pa is None or ws2 not in ws_set:
            continue
        pb2 = price_b[ws2]
        if pb2 is None:
            continue
        n_shift += 1
        if _quantize(pa, tick_rule) == _quantize(pb2, tick_rule):
            eq_shift += 1
    with localcontext(contexte_decimal()):
        T = None if n_common == 0 else +(Decimal(eq) / Decimal(n_common))
        T_delta = None if n_shift == 0 else +(Decimal(eq_shift) / Decimal(n_shift))
    non_constant = len(values_seen) >= 2
    # Fusion contenu v0 : identité exacte sur TOUTES les fenêtres communes, N ≥ N_min,
    # série non constante (sinon un peg gelé fusionnerait à tort — dégénérescence, pas copie).
    exact_copy = (n_common >= n_min and eq == n_common and non_constant)
    return {"T": T, "T_delta": T_delta, "n_common": n_common, "n_shift": n_shift,
            "sufficient": n_common >= n_min, "non_constant": non_constant,
            "exact_copy_merge": exact_copy}


def _aberrance_by_window(wins, lnp, pool, kappa) -> dict[int, dict]:
    """Par fenêtre : {flux: signe d'aberrance ∈ {+1,−1,0}} où aberrant ssi
    |e_s(j)| > κ·MAD_j(pool), e = ln p − médiane_pool des ln p (leave-none), MAD_j =
    médiane(|e − médiane(e)|). MAD_j == 0 → fenêtre non évaluable (skip). §4.2 (2c).
    Consomme le précalcul `lnp` ; la médiane des e est calculée UNE fois (pas par élément)."""
    out: dict[int, dict] = {}
    poolset = set(pool)
    with localcontext(contexte_decimal()):
        for ws in wins:
            elns = {f: v for f, v in lnp.get(ws, {}).items() if f in poolset}
            if len(elns) < 2:
                continue
            med = _median(list(elns.values()))
            e = {f: +(v - med) for f, v in elns.items()}
            med_e = _median(list(e.values()))            # UNE fois (pas dans la compréhension)
            mad = _median([abs(v - med_e) for v in e.values()])
            if mad == 0:
                continue
            thr = +(kappa * mad)
            out[ws] = {f: _sgn(v) if abs(v) > thr else 0 for f, v in e.items()}
    return out


def coaberrance_kz(aber: dict, a, b, seuil_hist=SEUIL_HIST) -> dict:
    """(2c) K, z : co-aberrance de même signe à lag ≤ ℓ (v0 : ℓ=0). Marginales par
    signe OBSERVÉES ; sous indépendance p = p̂_a⁺·p̂_b⁺ + p̂_a⁻·p̂_b⁻ ; puis RÉUTILISE
    r1.gate_value/z_score/binomial_tail_ge avec la garde §5.4 (« machinerie de §5.1
    recalculée sur les résidus », §4.2 (2c))."""
    ap = an = bp = bn = K = n = 0
    for ws, sgns in aber.items():
        if a not in sgns or b not in sgns:
            continue
        sa, sb = sgns[a], sgns[b]
        n += 1
        if sa > 0:
            ap += 1
        elif sa < 0:
            an += 1
        if sb > 0:
            bp += 1
        elif sb < 0:
            bn += 1
        if sa != 0 and sa == sb:
            K += 1
    if n == 0:
        return {"K": 0, "n": 0, "z": None, "queue": None,
                "note": "aucune fenêtre co-évaluable (MAD nulle ou pool trop petit)"}
    with localcontext(contexte_decimal()):
        pa_p, pa_n = Decimal(ap) / Decimal(n), Decimal(an) / Decimal(n)
        pb_p, pb_n = Decimal(bp) / Decimal(n), Decimal(bn) / Decimal(n)
        p_co = +(pa_p * pb_p + pa_n * pb_n)
    gate = gate_value(n, p_co)
    if gate < seuil_hist:
        degenere = (p_co == Decimal(0)) or (p_co == Decimal(1))
        queue = None if degenere else binomial_tail_ge(K, n, p_co)
        return {"K": K, "n": n, "z": None, "p_co": p_co, "gate": gate, "queue": queue,
                "note": ("garde §5.4 (n·p·(1−p) < 10) : queue exacte P(K≥K_obs|Bin(n,p_co))"
                         if not degenere else
                         "dégénérée p_co ∈ {0,1} — sans pouvoir de test (§5.4)")}
    return {"K": K, "n": n, "z": z_score(n, K, p_co), "p_co": p_co, "gate": gate,
            "queue": None, "note": f"z co-aberrance (seuil {SEUIL_Z}, unilatéral)"}


def _jumps(wins, lnp, f, w, jump_sigma) -> dict[int, int]:
    """Indicatrice de saut j_f(ws) = 1 si |r_f(ws)| > jump_sigma·σ_f, σ_f = écart-type
    des rendements définis de f. §4.2 (2d). Consomme le précalcul `lnp`."""
    r = log_returns(wins, lnp, f, w)
    if len(r) < 2:
        return {}
    with localcontext(contexte_decimal()):
        vals = list(r.values())
        m = sum(vals, Decimal(0)) / Decimal(len(vals))
        var = sum(((v - m) ** 2 for v in vals), Decimal(0)) / Decimal(len(vals))
        sd = var.sqrt()
        if sd == 0:
            return {ws: 0 for ws in r}
        thr = +(jump_sigma * sd)
        return {ws: (1 if abs(v) > thr else 0) for ws, v in r.items()}


def delta_direction(wins, lnp, a, b, w, jump_sigma, big_l) -> dict:
    """(2d) δ : corrélation croisée des indicatrices de saut aux lags −L..+L — le
    SEUL axe qui donne la DIRECTION (qui précède qui). δ = lag de corrélation max ;
    lag>0 : a précède b. §4.2 (2d)."""
    ja, jb = _jumps(wins, lnp, a, w, jump_sigma), _jumps(wins, lnp, b, w, jump_sigma)
    na, nb = sum(ja.values()), sum(jb.values())
    if not ja or not jb or na == 0 or nb == 0:
        return {"best_lag": None, "best_corr": None, "n_jumps_a": na, "n_jumps_b": nb,
                "note": "aucun saut sur au moins une source — direction non évaluable"}
    best_lag = best_corr = None
    for lag in range(-big_l, big_l + 1):
        xs, ys = [], []
        for ws in wins:
            ws2 = ws + lag * w
            if ws in ja and ws2 in jb:
                xs.append(Decimal(ja[ws])); ys.append(Decimal(jb[ws2]))
        if len(xs) < 2:
            continue
        rho, note = pearson(xs, ys)
        if rho is None:
            continue
        if best_corr is None or rho > best_corr:
            best_corr, best_lag = rho, lag
    return {"best_lag": best_lag, "best_corr": best_corr, "n_jumps_a": na,
            "n_jumps_b": nb,
            "note": ("aucun lag à corrélation définie" if best_lag is None else
                     f"lag={best_lag} (>0 : {a} précède {b})")}


def method_edge_pairs() -> set:
    """Paires de flux (frozenset) qu'une arête `basis:doc` désigne pour la mesure (b)
    (ADR-0008 : déclenche, ne fusionne pas)."""
    return {frozenset((e["from"], e["to"])) for e in METHOD_EDGES if e["kind"] == "upstream"}


def compute_content(markers, readings, pool, w, params) -> dict:
    """Les 5 statistiques de contenu (§4.2) PAR PAIRE de flux, JAMAIS fusionnées :
    ρ_raw, ρ_resid, T/T_Δ, (K,z) co-aberrance, δ. Sur toutes les fenêtres (grille du
    journal, hors stratification R1 — GRID_NOTE). Rend aussi les paires à fusion
    exacte (pour k_eff) et le résidu de peg USDT/USD (§9.4)."""
    n_min = int(params["content_n_min"])
    kappa = Decimal(str(params["content_kappa_value"]))
    tick_rule = params["tick_rule"]
    delta_windows = int(params["content_delta_windows"])
    jump_sigma = Decimal(str(params["content_jump_sigma"]))
    big_l = int(params["content_big_l"])
    # ℓ (co-aberrance à lag ≤ ℓ) est PORTEUR : la v0 n'implémente que ℓ=0 (même
    # fenêtre) ; une valeur ≠ 0 est fail-closed, jamais IGNORÉE en silence (sinon le
    # journal enregistrerait un ℓ que le calcul ne respecte pas — un mensonge, §E).
    if int(params["content_lag_l"]) != 0:
        raise ValueError(
            "co-aberrance v0 : seul ℓ=0 (même fenêtre) est supporté ; "
            f"content_lag_l={params['content_lag_l']} non honoré — fail-closed (§4.2 (2c))"
        )

    wins, reading_map = price_map(readings, markers)
    lnp = lnprice_by_window(wins, reading_map)          # ln p calculés UNE fois (perf + partage)
    aber = _aberrance_by_window(wins, lnp, pool, kappa)
    trig = method_edge_pairs()

    # devise par flux (pour le résidu de peg) — depuis le journal seul
    cur = {}
    for r in readings:
        c = r.get("currency")
        if c is not None:
            cur.setdefault(r["flux_id"], c)

    pairs: dict[str, dict] = {}
    exact_copy_pairs: list[frozenset] = []
    peg_pairs: list[str] = []
    for a, b in combinations(pool, 2):
        raw = rho_raw(wins, lnp, a, b, w, n_min)
        resid = rho_resid(wins, lnp, a, b, n_min)
        tick = tick_identity(wins, reading_map, a, b, w, n_min, tick_rule, delta_windows)
        coab = coaberrance_kz(aber, a, b)
        delta = delta_direction(wins, lnp, a, b, w, jump_sigma, big_l)
        is_peg = ({cur.get(a), cur.get(b)} == {"USD", "USDT"})
        key = f"{a}×{b}"
        pairs[key] = {
            "rho_raw": raw, "rho_resid": resid, "tick": tick, "coaberrance": coab,
            "delta": delta,
            "basis_doc_triggered": frozenset((a, b)) in trig,
            "is_peg_usdt_usd": is_peg,
        }
        if tick["exact_copy_merge"]:
            exact_copy_pairs.append(frozenset((a, b)))
        if is_peg and resid["sufficient"]:
            peg_pairs.append(key)
    return {
        "n_min": n_min, "grid_note": GRID_NOTE, "merge_criterion": MERGE_CRITERION_V0,
        "coab_staleness_note": COAB_STALENESS_NOTE,
        "pairs": pairs, "exact_copy_pairs": exact_copy_pairs, "peg_pairs": peg_pairs,
        "n_windows": len(wins),
    }


# ── Partition, k_eff, clusters nommés (§5.6, ADR-0007) ─────────────────────────

def compute_partition(asn_records, flux_hosts, pool, content) -> dict:
    """Partition des HÔTES par les recouvrements R2 **measured** (ASN cross-confirmé
    ∪ identité-copie contenu) — JAMAIS `basis:doc` seul (ADR-0008). k_eff = nombre de
    classes. Clusters NOMMÉS avec leurs amonts (ADR-0007). Fail-closed : sans ASN
    mesuré, k_eff non évaluable (jamais fabriqué par absence de donnée)."""
    hosts = hosts_of_pool(flux_hosts, pool)
    k_nominal = len(hosts)
    fbh = flux_by_host(flux_hosts, pool)

    # last-wins par hôte + détection de divergence d'ASN (résidu 4, jamais écrasé)
    by_host: dict[str, dict] = {}
    asn_divergences: list[dict] = []
    for rec in asn_records:
        h = rec.get("host")
        if h in by_host:
            prev, cur = by_host[h], rec
            if (prev.get("asn_ripestat"), prev.get("asn_cymru")) != \
               (cur.get("asn_ripestat"), cur.get("asn_cymru")):
                asn_divergences.append({
                    "host": h,
                    "avant": (prev.get("asn_ripestat"), prev.get("asn_cymru"), prev.get("ts")),
                    "apres": (cur.get("asn_ripestat"), cur.get("asn_cymru"), cur.get("ts")),
                })
        by_host[h] = rec

    states = {h: _asn_state(by_host.get(h)) for h in hosts}
    measured = any(st["kind"] not in ("missing",) for st in states.values())
    all_probed = all(states[h]["kind"] != "missing" for h in hosts)

    # merges measured
    uf = _UnionFind(hosts)
    merge_reasons: list[dict] = []
    # (a) ASN cross-confirmé partagé
    by_asn: dict[int, list[str]] = {}
    for h in hosts:
        st = states[h]
        if st["attributed"]:
            by_asn.setdefault(st["asn"], []).append(h)
    for asn, group in by_asn.items():
        if len(group) >= 2:
            g = sorted(group)
            for other in g[1:]:
                uf.union(g[0], other)
            merge_reasons.append({"axis": "asn_measured", "asn": asn,
                                  "holder": states[g[0]].get("holder"), "hosts": g})
    # (b) identité-copie contenu (measured) → fusionne les HÔTES des deux flux
    for pair in content["exact_copy_pairs"]:
        a, b = tuple(sorted(pair))
        ha, hb = flux_hosts.get(a), flux_hosts.get(b)
        if ha in uf.parent and hb in uf.parent and ha != hb:
            uf.union(ha, hb)
            merge_reasons.append({"axis": "content_exact_copy", "flux_pair": [a, b],
                                  "hosts": sorted((ha, hb))})

    classes = uf.classes()  # {racine: [hôtes]}
    # Nommage ADR-0007 : cluster = {hôtes} via AS<n> <holder> + qualifieur de fusion
    # selon l'AXE RÉEL (C-B, G2+oracle) : « côté livraison » ⇔ fusion ASN PARTAGÉ (fronting
    # CDN, résidu 1) SEULEMENT ; une fusion copie-exacte cross-ASN est « copie de contenu »,
    # jamais « côté livraison ». L'axe réel est porté par merge_reasons.
    clusters = []
    for root in sorted(classes):
        chosts = classes[root]
        chostset = set(chosts)
        cflux = sorted(f for h in chosts for f in fbh.get(h, []))
        asn_holder = {states[h]["asn"]: states[h].get("holder")
                      for h in chosts if states[h]["attributed"]}
        asns = sorted(asn_holder)
        holders = sorted({v for v in asn_holder.values() if v})
        cl_merges = [m for m in merge_reasons if set(m["hosts"]) & chostset]
        asn_shared = [m for m in cl_merges if m["axis"] == "asn_measured"]
        content_merges = [m for m in cl_merges if m["axis"] == "content_exact_copy"]
        merge_axes = sorted({m["axis"] for m in cl_merges})
        declared_up = [e for e in METHOD_EDGES if e["kind"] == "upstream"
                       and (e["from"] in cflux or e["to"] in cflux)]
        name = f"{{{', '.join(chosts)}}}"
        if asns:
            name += " via " + "/".join(f"AS{a} {asn_holder[a] or ''}".rstrip() for a in asns)
        quals = []
        if asn_shared:
            sh = "/".join(f"AS{m['asn']} {m.get('holder') or ''}".rstrip() for m in asn_shared)
            quals.append(f"fusion ASN partagé {sh} — côté livraison (§4.1, résidu 1)")
        if content_merges:
            fp = "; ".join("≡".join(m["flux_pair"]) for m in content_merges)
            quals.append(f"fusion COPIE DE CONTENU ({fp}, §4.2 (2b) — recouvrement de "
                         "CONTENU, ASN possiblement distincts ; pas un fronting CDN)")
        if quals:
            name += " [" + " + ".join(quals) + "]"
        caveats = []
        if RPC_READ_PATH_HOST in chosts:
            caveats.append(CAVEAT_RPC_READ_PATH)
        for h in chosts:
            st = states[h]
            if not st["attributed"]:
                caveats.append(f"{h} : {st['reason']} → singleton non fusionné sur ASN")
        clusters.append({
            "hosts": chosts, "flux": cflux, "asns": asns, "holders": holders,
            "merge_axes": merge_axes, "name": name, "declared_upstreams": declared_up,
            "caveats": caveats, "n_members_flux": len(cflux),
        })

    # Hôtes SONDÉS mais NON ATTRIBUÉS (résolution échouée, base muette, ou discordance) :
    # leur singleton n'est PAS une indépendance confirmée — ils rendent k_eff une BORNE
    # SUPÉRIEURE (C-A ; 04 §4.1 : un axe non mesuré reste un mode commun possible ; direction
    # dangereuse pour un certificat). k_eff reste calculé (all-probed), mais MARQUÉ « ≤ ».
    unattributed = [h for h in hosts
                    if states[h]["kind"] != "missing" and not states[h]["attributed"]]
    k_eff_is_upper_bound = False
    if not measured:
        k_eff = None
        k_eff_note = ("axe ASN NON MESURÉ (aucun enregistrement asn_attribution) — k_eff "
                      "NON ÉVALUABLE ; une partition en singletons ici ne serait pas une "
                      "indépendance mesurée mais une absence de donnée (fail-closed §5.6)")
    elif not all_probed:
        missing = [h for h in hosts if states[h]["kind"] == "missing"]
        k_eff = None
        k_eff_note = (f"axe ASN INCOMPLET — hôtes non sondés : {missing} ; k_eff non "
                      "évaluable tant que le pool n'est pas intégralement sondé (fail-closed)")
    elif unattributed:
        k_eff = len(classes)
        k_eff_is_upper_bound = True
        k_eff_note = (f"k_eff ≤ {k_eff} (BORNE SUPÉRIEURE) — {len(unattributed)} hôte(s) NON "
                      f"ATTRIBUÉ(s) {unattributed} restent des singletons NON CONFIRMÉS (ASN non "
                      "établi : résolution échouée / base muette / discordance) — 04 §4.1 : un "
                      "axe non mesuré est un mode commun possible ; k_eff n'est PAS un compte "
                      "d'indépendance confirmé (§5.6)")
    else:
        k_eff = len(classes)
        k_eff_note = "k_eff = nombre de classes de la partition R2 measured (§5.6)"

    return {
        "k_nominal": k_nominal, "k_eff": k_eff, "k_eff_note": k_eff_note,
        "k_eff_is_upper_bound": k_eff_is_upper_bound,
        "n_unattributed": len(unattributed), "unattributed": unattributed,
        "hosts": hosts, "flux_by_host": fbh, "asn_states": states,
        "attribution_by_host": by_host,   # relevé last-wins par hôte (table ASN §6 bloc 5)
        "clusters": clusters, "merge_reasons": merge_reasons,
        "asn_divergences": asn_divergences, "asn_measured": measured,
    }


def cluster_lm_correlations(partition, markers, readings, pool, w, sigma_by_class,
                            sigma_class_of_flux, tau, n_min) -> dict:
    """Corrélations L&M entre CLUSTERS (§5.5 pt 4, analogue éq. 35) : Pearson des
    séries (Θ̂_A,j, Θ̂_B,j), Θ̂_A,j = m_A,j/N_A = (flux du cluster A en écart)/(flux de A).
    Calculée seulement pour les clusters à ≥ 2 flux ; les singletons restent au φ par
    paire de flux de M1b (lm.py) — convention publiée. Réutilise la classification R1
    (r1.classify_cells, σ PAR CLASSE + τ RELATIF, ADR-0021) → zéro divergence."""
    from .r1 import ECARTS, classify_cells
    cells = classify_cells(markers, readings, pool, w, sigma_by_class,
                           sigma_class_of_flux, tau, n_min)
    win_strate = build_window_strate(markers)
    wins = sorted(win_strate)

    multi = [c for c in partition["clusters"] if c["n_members_flux"] >= 2]
    out: dict[str, dict] = {}
    for ca, cb in combinations(multi, 2):
        fa, fb = ca["flux"], cb["flux"]
        na, nb = len(fa), len(fb)
        xs, ys = [], []
        with localcontext(contexte_decimal()):
            for ws in wins:
                ma = sum(1 for f in fa if cells.get((ws, f)) in ECARTS)
                mb = sum(1 for f in fb if cells.get((ws, f)) in ECARTS)
                xs.append(Decimal(ma) / Decimal(na))
                ys.append(Decimal(mb) / Decimal(nb))
        rho, note = pearson(xs, ys)
        key = f"[{'+'.join(ca['hosts'])}]×[{'+'.join(cb['hosts'])}]"
        out[key] = {"rho": rho, "signe": ("+" if rho and rho > 0 else
                                          "−" if rho and rho < 0 else
                                          "0" if rho == 0 else "non_définie"),
                    "note": note, "n_windows": len(wins)}
    convention = ("corrélations Θ̂ entre clusters à ≥ 2 flux (analogue L&M éq. 35) ; "
                  "singletons → φ par paire de flux (M1b, bloc 4). Signées (Cov<0 possible).")
    return {"cluster_pairs": out, "convention": convention,
            "n_multi_clusters": len(multi)}


# ── Le drapeau 2 (§5.6) — tri-état, consomme la matrice de co-écarts M1b ────────

def drapeau_2(r1_out, partition, lm_out) -> dict:
    """« Co-défaillance observée non expliquée par les axes R2 » (§5.6 / 04 §3), aligné sur la règle
    SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pt 10) : « R1 discrimine » = r1.regle_critere(r1_out), qui ne lit
    que r1_out["strates"] (strate poolée hors des entrées). LEVÉ ⇔ VRAI et k_eff = k nominal du segment
    (hôtes distincts du pool), k_eff qui n'est pas une borne supérieure ; ÉTEINT ⇔ FAUX, ou VRAI avec k_eff
    < k nominal ; NON ÉVALUABLE ⇔ k_eff non évaluable (contrôlé d'abord, comme en v0 : CV2-35),
    « R1 discrimine » NON ÉVALUABLE, ou VRAI avec une borne supérieure de k_eff égale à k nominal (égalité
    non établie, 04 §4.1 ; revue G2, Q-G2-1, option a). Signal sur
    A(axis-coverage), jamais la règle. Quand VRAI, localise l'excès sur les paires INTER-CLUSTERS via la
    matrice de co-écarts complète de M1b (lm.pair_phi, n11 = co-écarts). k nominal_s : flux du pool de
    chaque strate (D1 cas b)."""
    k_eff, k_nom, rg = partition["k_eff"], partition["k_nominal"], r1.regle_critere(r1_out)
    d, rej = rg["r1_discrimine"], rg["rejette"]
    out = {"r1_discrimine": d, "rejette": rej, "k_eff": k_eff, "k_nominal": k_nom,
           "k_nominal_strates": {st: len(b["per_source"]) for st, b in r1_out.get("strates", {}).items()}}
    if k_eff is None:
        return {**out, "etat": "non_evaluable",
                "raison": "k_eff non évaluable (axe ASN non mesuré/incomplet) — "
                          "le drapeau exige une partition évaluable (§5.6)"}
    if d == "NON ÉVALUABLE":
        return {**out, "etat": "non_evaluable", "raison": "« R1 discrimine » NON ÉVALUABLE (règle "
                "SHOGEN-CRITERE-R1-1, bloc 3) — co-défaillance non qualifiable ; ni levé ni éteint"}
    loc, vrai = (_localize_intercluster(partition, lm_out) if d == "VRAI" else None,
                 f"« R1 discrimine » VRAI (strate(s) : {', '.join(rej)})")
    kt = f"≤ {k_eff} (borne supérieure)" if partition.get("k_eff_is_upper_bound") else f"= {k_eff}"
    if d == "VRAI" and k_eff == k_nom and partition.get("k_eff_is_upper_bound"):     # G2 Q-G2-1, option (a)
        return {**out, "etat": "non_evaluable", "localisation_inter_clusters": loc, "raison": (
            f"{vrai} mais k_eff {kt} : l'égalité à k nominal du segment n'est pas établie (hôte(s) non "
            "attribué(s), 04 §4.1) — ni levé ni éteint")}
    if d == "VRAI" and k_eff == k_nom:
        return {**out, "etat": "leve", "localisation_inter_clusters": loc, "raison": (
            f"{vrai} AVEC k_eff = {k_eff} = k nominal du segment : les axes R2 ne capturent pas le mode "
            "commun (§5.6 / 04 §3) — signal sur A(axis-coverage), jamais la règle")}
    return {**out, "etat": "eteint", "localisation_inter_clusters": loc, "raison": (
        f"{vrai} mais k_eff {kt} < k nominal du segment = {k_nom} : recouvrement R2 mesuré explique au "
        "moins en partie la co-défaillance" if d == "VRAI" else
        "« R1 discrimine » FAUX : le modèle d'indépendance n'est rejeté dans aucune strate testée (bloc 3)")}


def _cluster_of_flux(partition) -> dict[str, int]:
    """{flux: index de cluster} pour localiser les paires inter-clusters."""
    out = {}
    for i, c in enumerate(partition["clusters"]):
        for f in c["flux"]:
            out[f] = i
    return out


def _localize_intercluster(partition, lm_out) -> dict:
    """Consomme la matrice de co-écarts complète de M1b (lm.pair_phi par strate) et
    liste les paires INTER-CLUSTERS triées par co-écart (n11) — où se loge l'excès de
    co-défaillance que R2 n'explique pas (§5.6, raffinement)."""
    cof = _cluster_of_flux(partition)
    per_strate: dict[str, list] = {}
    for st, blk in lm_out.get("strates", {}).items():
        rows = []
        for key, v in blk.get("pair_phi", {}).items():
            a, b = key.split("×", 1)
            if cof.get(a) is not None and cof.get(b) is not None and cof[a] != cof[b]:
                rows.append({"pair": key, "n11": v["n11"], "phi": v["phi"],
                             "signe": v["signe"]})
        rows.sort(key=lambda r: (-r["n11"], r["pair"]))
        per_strate[st] = rows
    return {"note": ("paires inter-clusters triées par co-écart n11 — l'excès de "
                     "co-défaillance non expliqué par R2 s'y localise (§5.6)"),
            "par_strate": per_strate}


# ── Orchestration + point d'entrée recalculable (patron maison) ────────────────

def compute_r2(markers, readings, asn_records, pool, w, sigma_by_class,
               sigma_class_of_flux, tau, params, n_min_horsenv=None, pool_by_strate=None) -> dict:
    """R2 complet : partition/k_eff (ASN + contenu), statistiques de contenu par paire,
    arêtes méthode, corrélations clusters, drapeau 2. Consomme R1 et L&M (mêmes
    helpers, σ PAR CLASSE + τ RELATIF, zéro divergence). `params` = run_params
    effectif (clés R2 présentes). ADR-0028 D1 : R2 porte sur `pool` (cas a seul) ; R1 et L&M
    du drapeau 2 reçoivent `pool_by_strate` (cas b), comme les blocs 3 et 4."""
    if n_min_horsenv is None:
        n_min_horsenv = r1.N_MIN_HORSENV
    flux_hosts = params["flux_hosts"]

    content = compute_content(markers, readings, pool, w, params)
    partition = compute_partition(asn_records, flux_hosts, pool, content)
    # Même seuil_hist que le bloc 3 du rapport (run_params) → le z consommé par le
    # drapeau 2 est EXACTEMENT celui publié au bloc 3, jamais un recalcul divergent.
    seuil_hist = Decimal(str(params.get("seuil_historique_valeur", SEUIL_HIST)))
    r1_out = r1.compute_r1(markers, readings, pool, w, sigma_by_class,
                           sigma_class_of_flux, tau, seuil_hist=seuil_hist,
                           n_min=n_min_horsenv, pool_by_strate=pool_by_strate)
    from .lm import compute_lm
    lm_out = compute_lm(markers, readings, pool, w, sigma_by_class,
                        sigma_class_of_flux, tau, n_min_horsenv, pool_by_strate)
    clusters_lm = cluster_lm_correlations(partition, markers, readings, pool, w,
                                          sigma_by_class, sigma_class_of_flux, tau,
                                          n_min_horsenv)
    flag2 = drapeau_2(r1_out, partition, lm_out)

    return {
        "pool": pool,
        "partition": partition,
        "content": content,
        "method_edges": list(METHOD_EDGES),
        "residus_asn": list(RESIDUS_ASN),
        "cluster_correlations": clusters_lm,
        "drapeau_2": flag2,
    }


def recompute_r2_from_journal(control_path: str, journal_path: str, exclude_ranges=(),
                              segment=None) -> dict:
    """Point d'entrée « recalculable depuis le journal seul » (ADR-0003), jumeau de
    r1/lm : mêmes gardes fail-closed (effective_run_params sur R1+R2, strates ==
    calendrier committé). C'est ce que rejoue l'oracle de recalcul (contexte frais)."""
    params_list, _clock, markers = records.parse_control(control_path)
    asn_records = records.parse_asn(control_path)
    params = records.effective_run_params(
        params_list,
        load_bearing=records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS,
    )
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            "strates journalées incohérentes avec le calendrier committé "
            f"(fail-closed, §5.3) : {div[:5]}"
        )
    # Filtre de lecture unique (ADR-0025 amendée par ADR-0028 D5) APRÈS la garde §5.3 ; journal intact.
    markers, _clock, asn_records, _seg = records.filtre_lecture(params, markers, asn=asn_records,
                                                                ranges=exclude_ranges, segment=segment)
    readings = r1.parse_journal(journal_path)
    pools, pool, _retraits = r1.analysis_pools(markers, readings, list(params["pool"]))  # ADR-0028 D1
    sigma_by_class, sigma_class_of_flux, tau = records.sigma_tau_from_params(params)
    return compute_r2(
        markers=markers,
        readings=readings,
        asn_records=asn_records,
        pool=pool,
        pool_by_strate=pools,
        w=int(params["w"]),
        sigma_by_class=sigma_by_class,
        sigma_class_of_flux=sigma_class_of_flux,
        tau=tau,
        params=params,
        n_min_horsenv=int(params["n_min_hors_enveloppe"]),
    )
