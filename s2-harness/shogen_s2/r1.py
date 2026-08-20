"""R1 — le test K&L §5 transposé, recalculé DEPUIS LE JOURNAL SEUL (ADR-0003).

Conception : docs/10-mesures-pilotes-design.md §5.1 (formules K&L : `P₀`, `P₁`
par l'**identité élémentaire**, `P_more`, `K`, `z`, seuil 2,33), §5.2 (écarts
i/ii/iii, précédence **panne > staleness > hors-enveloppe**), §5.4 (seuil
« historique insuffisant » `n·P̂_more·(1−P̂_more) ≥ 10`, source UConn OER Math
3160 ch.9 p.121). Plan S2 §3, [C5].

`Decimal` partout, **précision fixée** (`DECIMAL_PREC`) → recalcul
bit-identique par l'oracle. Ne lit QUE les fichiers de journal
(`control.jsonl` + `journal.jsonl`) : aucun accès à Shōgen, aucun paramètre
hors-bande (σ_classe, τ_classe, w, pool viennent de `run_params`).

**Portée skeleton (bornée, plan §3)** : PAS de queue binomiale exacte / Poisson
(§5.4, extension du harnais complet) — le bloc R1 rend « `z`, ou historique
insuffisant ». Chemin **par-strate**, strate unique par défaut. Le drapeau 2 de
§5.6 (« co-défaillance non expliquée par R2 ») requiert `k_eff` (R2), hors
périmètre skeleton — seul le drapeau « historique insuffisant » est calculé.

**Identité élémentaire** (10 §5.1, indépendante de la citation, donc du calcul
débloqué) :
    P₀ = Π(1 − p̂ᵢ)
    P₁ = Σᵢ p̂ᵢ · Πⱼ≠ᵢ (1 − p̂ⱼ)          (exactement une défaillance)
    P_more = 1 − P₀ − P₁                    (≥ 2 défaillances)
La FORME IMPRIMÉE de P₁ chez K&L reste une dette de RELECTURE (plan §2 [C2]
dette 9b, tâche lecteur Sonnet 5, une page) — nommée, pas nue ; elle ne bloque
pas ce calcul, qui n'en dépend pas.

**Dénominateur `n` (résolution ADVISOR, cette passe)** : `n` = fenêtres
**complétées** par strate. Une fenêtre où hors-enveloppe est « non évaluable »
(N < 4 répondantes, §5.2) entre dans `n` mais N'EST PAS un écart ; ce compte
« non évaluable » est **publié par source** (bloc R1) — `p̂ = 0` ne peut donc
se lire comme propreté confirmée (fail-closed de publication, §5.2). La lecture
alternative (exclure ces fenêtres de `n`) collapse `n → 0` sur un skeleton
propre à 3 sources et rend la sortie exigée impossible ; l'arithmétique de
budget (10 §9.5 : « n ≳ 10 010 fenêtres ≈ 7,0 jours ») compte bien `n` en
fenêtres calendaires.
"""

from __future__ import annotations

import enum
import json
from decimal import Decimal, localcontext
from typing import Optional

from . import records
from .window import window_end

DECIMAL_PREC = 50                 # précision fixée → recalcul bit-identique (oracle)
SEUIL_HIST = Decimal(10)          # n·P̂_more·(1−P̂_more) ≥ 10 (10 §5.4)
N_MIN_HORSENV = 4                 # N ≥ 4 répondantes pour l'enveloppe leave-one-out (10 §5.2)
SEUIL_Z = Decimal("2.33")         # point 99% normale standard (K&L — 10 §5.1)
A_WINDOW_STATIONARITY = (
    "A(window-stationarity) engagée par le test agrégé (10 §5.3 ; ancre "
    "Eckhardt & Lee TM-86369 p. fichier 2, hyp. (ii) « stationary input series ») "
    "— écrite dans chaque sortie R1 ; décharge = stratification ex ante (08)"
)


class Ecart(enum.Enum):
    """Résultat de classification d'un couple (fenêtre, source) — 10 §5.2."""

    PANNE = "panne"                                    # (iii)
    STALENESS = "staleness"                            # (ii)
    HORS_ENVELOPPE = "hors_enveloppe"                  # (i)
    PAS_ECART = "pas_ecart"                            # évalué, aucun écart
    NON_EVAL_HORSENV = "non_evaluable_hors_enveloppe"  # N < 4 répondantes


# Les trois vrais écarts qui alimentent p̂ᵢ (10 §5.1 : « fenêtres où i est en écart »).
ECARTS = frozenset({Ecart.PANNE, Ecart.STALENESS, Ecart.HORS_ENVELOPPE})


def _as_dec(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _median(values: list[Decimal]) -> Decimal:
    # Précision FIXÉE (pas le contexte ambiant) : sinon _median([1, 1+1e-27])
    # diverge prec 28 vs 50 (démontré par l'oracle) → recalcul non identique.
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        s = sorted(values)
        m = len(s)
        if m % 2 == 1:
            return +s[m // 2]
        return +((s[m // 2 - 1] + s[m // 2]) / Decimal(2))


def classify_ecart(
    reading: Optional[dict],
    others_prices: list[Decimal],
    n_responding: int,
    win_end: int,
    sigma: Decimal,
    tau: Decimal,
    n_min: int = N_MIN_HORSENV,
) -> Ecart:
    """Classe un couple (fenêtre, source), précédence **panne > staleness >
    hors-enveloppe** (10 §5.2). `reading` est la ligne `journal.jsonl` parsée
    (ou None si absente d'une fenêtre complétée = non-réponse). `others_prices`
    = prix des AUTRES répondantes (leave-one-out) ; `n_responding` = nombre
    total de répondantes de la fenêtre (OK avec prix). Toute l'arithmétique
    Decimal est à précision FIXÉE (DECIMAL_PREC), comme les statistiques."""
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        # (iii) panne — précédence maximale : une panne n'a pas de valeur.
        if reading is None or reading.get("status") != "ok" or reading.get("price") is None:
            return Ecart.PANNE
        # (ii) staleness — sur l'horodatage PORTÉ (source_ts), jamais l'horloge
        # harnais (03 §1). source_ts absent (ex. kraken) → staleness non
        # évaluable : on passe à (i), sans flaguer (résidu fail-open publié §G).
        src_ts = reading.get("source_ts")
        if src_ts is not None and (Decimal(win_end) - _as_dec(src_ts)) > sigma:
            return Ecart.STALENESS
        # (i) hors-enveloppe — l'enveloppe (médiane leave-one-out) exige N ≥ n_min
        # RÉPONDANTES (10 §5.2). Sinon « non évaluable », jamais « pas d'écart ».
        if n_responding >= n_min:
            m_loo = _median(others_prices)
            price = Decimal(reading["price"])
            if abs(price - m_loo) > tau:
                return Ecart.HORS_ENVELOPPE
            return Ecart.PAS_ECART
        return Ecart.NON_EVAL_HORSENV


# ── Formules K&L §5 (identité élémentaire) — Decimal, précision fixée ──────────

def poisson_binomial(phats: list[Decimal]) -> tuple[Decimal, Decimal, Decimal]:
    """(P₀, P₁, P_more) pour des écarts indépendants de probabilités `phats`
    (10 §5.1). P_more = 1 − P₀ − P₁ **par construction**."""
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        one = Decimal(1)
        p0 = one
        for p in phats:
            p0 *= (one - p)
        p1 = Decimal(0)
        for i, pi in enumerate(phats):
            term = pi
            for j, pj in enumerate(phats):
                if j != i:
                    term *= (one - pj)
            p1 += term
        p_more = one - p0 - p1
        return +p0, +p1, +p_more


def gate_value(n: int, p_more: Decimal) -> Decimal:
    """`n·P̂_more·(1−P̂_more)` (10 §5.4) — la forme produit-variance."""
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        return +(Decimal(n) * p_more * (Decimal(1) - p_more))


def insufficient_history(n: int, p_more: Decimal) -> bool:
    """Vrai si `n·P̂_more·(1−P̂_more) < 10` → pas de z publié (10 §5.4)."""
    return gate_value(n, p_more) < SEUIL_HIST


def z_score(n: int, k: int, p_more: Decimal) -> Decimal:
    """`z = (K − n·P_more)/√(n·P_more·(1−P_more))` (10 §5.1), test unilatéral.
    Appeler UNIQUEMENT si `not insufficient_history` (sinon division par ~0)."""
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        mean = Decimal(n) * p_more
        var = Decimal(n) * p_more * (Decimal(1) - p_more)
        return +((Decimal(k) - mean) / var.sqrt())


# ── Agrégation R1 depuis le journal ──────────────────────────────────────────

def parse_journal(path: str) -> list[dict]:
    """Relit `journal.jsonl` (une ligne par fenêtre×flux). `parse_float=Decimal`
    → `source_ts` exact (ADR-0003) ; `price` reste chaîne (déjà exacte).
    Lecture TOLÉRANTE à une dernière ligne tronquée (crash mi-écriture, §F)."""
    return records.read_jsonl_tolerant(path, parse_float=Decimal)


def build_window_strate(markers: list[dict]) -> dict[int, str]:
    """Fenêtres complétées, **dédupliquées** par `window_start` (reprise
    idempotente, §5.3) — le dernier marqueur gagne (strate déterministe)."""
    win_strate: dict[int, str] = {}
    for m in markers:
        win_strate[int(m["window_start"])] = m["strate"]
    return win_strate


def build_reading_map(readings: list[dict]) -> dict[tuple[int, str], dict]:
    """Lectures indexées par (fenêtre, flux) — **last-wins** (« le dernier de
    la fenêtre », §5.3 : règle de lecture autant que de collecte)."""
    reading_map: dict[tuple[int, str], dict] = {}
    for r in readings:
        reading_map[(int(r["window_start"]), r["flux_id"])] = r
    return reading_map


def _classify_window(
    ws: int,
    reading_map: dict[tuple[int, str], dict],
    pool: list[str],
    w: int,
    sigma: Decimal,
    tau: Decimal,
    n_min: int = N_MIN_HORSENV,
) -> dict[str, Ecart]:
    """Classe chaque source du pool dans la fenêtre `ws`. Répondantes = OK avec
    prix ; l'enveloppe leave-one-out se calcule sur elles (N ≥ n_min, §5.2)."""
    responding = [
        f for f in pool
        if reading_map.get((ws, f)) is not None
        and reading_map[(ws, f)].get("status") == "ok"
        and reading_map[(ws, f)].get("price") is not None
    ]
    resp_price = {f: Decimal(reading_map[(ws, f)]["price"]) for f in responding}
    n_resp = len(responding)
    out: dict[str, Ecart] = {}
    for f in pool:
        others = [resp_price[g] for g in responding if g != f]
        out[f] = classify_ecart(reading_map.get((ws, f)), others, n_resp,
                                 window_end(ws, w), sigma, tau, n_min)
    return out


def classify_cells(
    markers: list[dict],
    readings: list[dict],
    pool: list[str],
    w: int,
    sigma: Decimal,
    tau: Decimal,
    n_min: int = N_MIN_HORSENV,
) -> dict[tuple[int, str], Ecart]:
    """Écart de chaque cellule (fenêtre×source) des fenêtres complétées — pour
    le bloc « Journal brut » de la table §6 (report.py). Même logique que
    compute_r1 (helper partagé), donc jamais de divergence."""
    win_strate = build_window_strate(markers)
    reading_map = build_reading_map(readings)
    out: dict[tuple[int, str], Ecart] = {}
    for ws in sorted(win_strate):
        cls = _classify_window(ws, reading_map, pool, w, sigma, tau, n_min)
        for f in pool:
            out[(ws, f)] = cls[f]
    return out


def compute_r1(
    markers: list[dict],
    readings: list[dict],
    pool: list[str],
    w: int,
    sigma: Decimal,
    tau: Decimal,
    seuil_hist: Decimal = SEUIL_HIST,
    n_min: int = N_MIN_HORSENV,
) -> dict:
    """Calcule R1 par strate depuis les enregistrements du journal.

    - **Dédup des marqueurs** par `window_start` (reprise idempotente, §5.3).
    - **Last-wins** par (fenêtre, flux) : re-collecte d'une fenêtre → la
      dernière lecture gagne (« le dernier de la fenêtre », §5.3).
    - `n` = fenêtres complétées **par strate**.
    """
    win_strate = build_window_strate(markers)      # dédup par window_start (§5.3)
    reading_map = build_reading_map(readings)       # last-wins par (fenêtre, flux)

    if not win_strate:
        return {
            "pool": pool,
            "strates": {},
            "note": "aucune fenêtre complétée (n = 0)",
            "flag_historique_insuffisant": True,
            "A_window_stationarity": A_WINDOW_STATIONARITY,
        }

    # Groupement des fenêtres par strate.
    windows_by_strate: dict[str, list[int]] = {}
    for ws, st in sorted(win_strate.items()):
        windows_by_strate.setdefault(st, []).append(ws)

    strates_out: dict[str, dict] = {}
    for st, wins in windows_by_strate.items():
        n = len(wins)
        # Compteurs par source.
        tally = {f: {k: 0 for k in Ecart} for f in pool}
        stale_evaluable = {f: 0 for f in pool}
        ok_windows = {f: 0 for f in pool}
        k_count = 0
        for ws in wins:
            cls = _classify_window(ws, reading_map, pool, w, sigma, tau, n_min)
            win_ecarts = 0
            for f in pool:
                rd = reading_map.get((ws, f))
                if rd is not None and rd.get("status") == "ok" and rd.get("price") is not None:
                    ok_windows[f] += 1
                    if rd.get("source_ts") is not None:
                        stale_evaluable[f] += 1
                kind = cls[f]
                tally[f][kind] += 1
                if kind in ECARTS:
                    win_ecarts += 1
            if win_ecarts >= 2:
                k_count += 1

        per_source = {}
        phats: list[Decimal] = []
        residu_fail_open: list[str] = []
        for f in pool:
            t = tally[f]
            ecart = t[Ecart.PANNE] + t[Ecart.STALENESS] + t[Ecart.HORS_ENVELOPPE]
            # p̂ᵢ à la précision FIXÉE (pas le contexte ambiant) → recalcul
            # bit-identique quel que soit le contexte de l'oracle (ADR-0003).
            with localcontext() as ctx:
                ctx.prec = DECIMAL_PREC
                phat = +(Decimal(ecart) / Decimal(n))
            phats.append(phat)
            axes = ["panne"]                       # (iii) toujours évaluable
            if stale_evaluable[f] > 0:
                axes.append("staleness")           # (ii) si horodatage porté
            if t[Ecart.HORS_ENVELOPPE] + t[Ecart.PAS_ECART] > 0:
                axes.append("hors_enveloppe")      # (i) si une fenêtre eut N≥n_min
            # Résidu fail-open (§G) : source qui RÉPOND mais ne porte jamais
            # d'horodatage (ex. kraken) → (ii) non évaluable, un « stale mais
            # répondant » passerait inaperçu. Rendu VISIBLE, pas seulement en
            # commentaire.
            fail_open = ok_windows[f] > 0 and stale_evaluable[f] == 0
            if fail_open:
                residu_fail_open.append(f)
            per_source[f] = {
                "phat": phat,
                "ecart": ecart,
                "panne": t[Ecart.PANNE],
                "staleness": t[Ecart.STALENESS],
                "hors_enveloppe": t[Ecart.HORS_ENVELOPPE],
                "non_eval_hors_env": t[Ecart.NON_EVAL_HORSENV],
                "pas_ecart": t[Ecart.PAS_ECART],
                "ok_windows": ok_windows[f],
                "staleness_evaluable_windows": stale_evaluable[f],
                "staleness_fail_open": fail_open,
                "axes_evaluables": axes,
            }

        p0, p1, p_more = poisson_binomial(phats)
        gate = gate_value(n, p_more)
        insufficient = gate < seuil_hist
        z = None if insufficient else z_score(n, k_count, p_more)
        strates_out[st] = {
            "n": n,
            "K": k_count,
            "per_source": per_source,
            "P0": p0,
            "P1": p1,
            "P_more": p_more,
            "gate_value": gate,
            "seuil_historique": seuil_hist,
            "n_min_hors_enveloppe": n_min,
            "residu_staleness_fail_open": residu_fail_open,
            "flag_historique_insuffisant": insufficient,
            "z": z,
            "seuil_z": SEUIL_Z,
            "A_window_stationarity": A_WINDOW_STATIONARITY,
        }

    return {"pool": pool, "strates": strates_out, "A_window_stationarity": A_WINDOW_STATIONARITY}


def recompute_from_journal(control_path: str, journal_path: str) -> dict:
    """Point d'entrée « recalculable depuis le journal seul » (ADR-0003) :
    lit les paramètres de `run_params` et les lectures, calcule R1. C'est ce que
    rejoue l'oracle de recalcul (worker à contexte frais, plan §5)."""
    params_list, _clock, markers = records.parse_control(control_path)
    # Concordance des run_params successifs vérifiée (fail-closed, §E) : un
    # redémarrage avec des seuils différents ne reclasse pas l'historique en
    # silence.
    params = records.effective_run_params(params_list)
    readings = parse_journal(journal_path)
    return compute_r1(
        markers=markers,
        readings=readings,
        pool=list(params["pool"]),
        w=int(params["w"]),
        sigma=Decimal(str(params["sigma_classe"])),
        tau=Decimal(str(params["tau_classe"])),
        seuil_hist=Decimal(str(params.get("seuil_historique_valeur", SEUIL_HIST))),
        n_min=int(params.get("n_min_hors_enveloppe", N_MIN_HORSENV)),
    )
