"""Collecteur fenêtré — walking skeleton : 3 sources USD, N fenêtres bornées.

Conception : docs/10-mesures-pilotes-design.md §3 (le pool), §5.3 (fenêtre
alignée UTC, 1 relevé/source/fenêtre = **le dernier**), §6 (journal
recalculable, ADR-0003/ADR-0005). Plan S2 §3 (walking skeleton, 3 sources),
§4 (les trois exigences opérationnelles).

**Ce n'est PAS le run de 24-48 h.** Le collecteur s'arrête après `n_windows`
(borné, configurable — plan §1 Phase A) ; le run réel est opérationnel
(orchestrateur). Le collecteur est à **injection de dépendances**
(`now_fn`, `sleep_fn`, `read_fn`) → testable déterministiquement sur fixtures
gelées, sans réseau (tests/test_collector.py).

Trois exigences opérationnelles tenues (plan §4) :
  (a) **harnais-down ≠ source-en-panne** : le marqueur `window_close` est posé
      APRÈS les 3 lectures. Un crash mi-fenêtre ne laisse pas de marqueur → la
      fenêtre n'entre pas dans `n` et n'est panne pour personne. `read()` (de
      sources.py) ne lève jamais : une panne source est un `Reading` typé
      PANNE, écrit dans une fenêtre complétée → compté en écart (iii, §5.2).
  (b) **journal append-only** : trois fichiers ouverts en mode "a", jamais
      réécrits (journal.append_jsonl).
  (c) **contrôle d'horloge au démarrage** consigné (plan §4.2 [C6]) — un
      processus qui redémarre ré-exécute ce démarrage, donc « démarrage = reprise
      par construction » : append-only + fenêtres alignées UTC + last-wins au
      parseur R1 rendent le redémarrage **toléré** sans code de détection de
      reprise (celui-ci serait de Phase B, hors périmètre skeleton).

Le contrôle d'horloge utilise la **plausibilité croisée** avec les `source_ts`
portés (03 §1), pas NTP : le « ou » de [C6] l'autorise, et SNTP ajouterait un
appel UDP externe et une dépendance (R-8 : zéro dépendance maintenu).
"""

from __future__ import annotations

import time
from decimal import Decimal
from statistics import median
from typing import Callable, Optional

from . import journal, r2, records, sources
from .model import Reading
# Précision + seuils du calcul R1, enregistrés numériquement dans run_params
# (recalculable depuis le journal seul, ADR-0003 ; source unique de vérité).
from .r1 import DECIMAL_PREC, N_MIN_HORSENV, SEUIL_HIST
from .sources import SourceSpec, read
from .window import (
    SINGLE_STRATE_SPEC,
    W_DEFAULT,
    make_strate_fn,
    window_start,
)

HARNESS_VERSION = "s2-harness/S2A-M1c"  # version du code (§6.1 bloc Paramètres)
SAMPLE_LEAD_DEFAULT = 5.0  # δ : échantillonnage à ws+w−δ (fin de fenêtre, §5.3/M-1)


def _iso_utc(ts: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(ts, timezone.utc).isoformat()


def clock_check(
    specs: list[SourceSpec],
    control_path: str,
    read_fn: Callable[[SourceSpec, float], Reading],
    harness_ts: float,
    phase: str = "startup",
) -> dict:
    """Consigne un contrôle d'horloge (plan §4.2 [C6]) : offset harnais vs
    `source_ts` porté, par source, plus la médiane. Jamais bloquant.

    Note ADR-0005 (§H) : ces lectures sont des **sondes jetables** — elles ne
    sont PAS écrites au journal ni hashées (l'exception assumée à « hash
    toujours » : une sonde d'horloge n'est pas une observation de marché ;
    seules les lectures de fenêtre le sont)."""
    offsets: dict = {}
    source_ts_used: dict = {}
    for spec in specs:
        r = read_fn(spec, harness_ts)
        if r.ok and r.source_ts is not None:
            offsets[spec.flux_id] = harness_ts - r.source_ts
            source_ts_used[spec.flux_id] = r.source_ts
    if offsets:
        med: Optional[float] = median(offsets.values())
        note = None
    else:
        med = None
        note = ("aucun horodatage porté disponible (source_ts absent sur tout le "
                "pool) — contrôle d'horloge non évaluable cette passe")
    rec = records.clock_check_record(harness_ts, phase, offsets, source_ts_used, med, note)
    journal.append_jsonl(control_path, rec)
    return rec


def collect(
    specs: list[SourceSpec],
    control_path: str,
    journal_path: str,
    raw_path: str,
    n_windows: int,
    *,
    sigma_by_class: dict,
    tau_classe: dict,
    w: int = W_DEFAULT,
    sample_lead: float = SAMPLE_LEAD_DEFAULT,
    strate_spec: Optional[dict] = None,
    strate_fn: Optional[Callable[[int], str]] = None,
    now_fn: Callable[[], float] = time.time,
    sleep_fn: Callable[[float], None] = time.sleep,
    read_fn: Callable[[SourceSpec, float], Reading] = read,
    harness_version: str = HARNESS_VERSION,
    kappa_note: str = ("5 (10 §4.2 (2c), paramètre R2 co-aberrance — exercé par M1c "
                       "via content_kappa_value)"),
) -> int:
    """Collecte `n_windows` fenêtres UTC-alignées, 1 relevé/source/fenêtre.

    **σ PAR CLASSE + τ RELATIF (ADR-0021)** : `sigma_by_class` est un mapping
    classe→plancher (Decimal secondes, ou `None` = « non évaluable ») ; le dispatch
    flux→classe est dérivé de `sources.SIGMA_CLASS_OF_FLUX` (source unique de vérité)
    et écrit dans run_params (porteur, recalculable). `tau_classe` est un MAPPING
    classe→fraction relative (ADR-0022), consommé par `r1.classify_ecart` en
    `|prix − médiane_LOO| / médiane_LOO > τ`. La CAPTURE reste SANS SEUIL (ADR-0020
    reframe) : ces paramètres ne gouvernent que le scoring DÉRIVÉ, pas l'archive.

    **Échantillonnage en FIN de fenêtre** (M-1) : on dort jusqu'à `ws+w−δ`
    (`δ = sample_lead`) puis on lit — « le DERNIER relevé de la fenêtre » (§5.3).
    Lire au début ferait paraître stale de ~w toute source fraîche (la staleness
    se mesure `(ws+w) − source_ts`, §5.2). `δ > 0` évite aussi le piège
    demi-ouvert (lire à exactement `ws+w` tomberait dans la fenêtre suivante) et
    doit couvrir la latence de lecture du pool ET rester `< σ_classe` (sinon une
    source fraîche, stale de ~δ, franchirait le seuil) — responsabilité de
    l'opérateur, publié dans run_params.

    Écrit trois journaux append-only : `control.jsonl` (run_params, clock_check,
    marqueurs), `journal.jsonl` (lectures décodées + sha256), `raw.jsonl`
    (octets bruts). Retourne le nombre de fenêtres complétées.
    """
    if not (0.0 < sample_lead < w):
        raise ValueError(f"sample_lead δ={sample_lead} doit vérifier 0 < δ < w={w}")
    # Spec de calendrier committée = source de vérité (auditable ex ante,
    # recalculable depuis run_params). La fermeture strate_fn en dérive ; un
    # strate_fn explicite (injection de test) reste possible mais la spec
    # enregistrée doit le décrire (vérif recompute==marqueur, §5.3).
    if strate_spec is None:
        strate_spec = SINGLE_STRATE_SPEC
    if strate_fn is None:
        strate_fn = make_strate_fn(strate_spec)
    start_ts = now_fn()

    # Bloc Paramètres (§6.1) dans le journal → recalculabilité littérale (ADR-0003).
    pool = [s.flux_id for s in specs]
    # σ PAR CLASSE (ADR-0021) : le dispatch flux→classe vient de la SOURCE UNIQUE DE
    # VÉRITÉ (sources.SIGMA_CLASS_OF_FLUX), restreint au pool ; écrit dans run_params
    # → recalculable, PORTEUR (§E). `sigma_by_class` (classe→plancher) doit couvrir
    # toutes les classes du pool, sinon un flux aurait un σ deviné (fail-closed).
    sigma_class_of_flux = sources.sigma_class_of_flux_for(pool)
    classes_needed = set(sigma_class_of_flux.values())
    classes_missing = [c for c in classes_needed if c not in sigma_by_class]
    if classes_missing:
        raise ValueError(
            f"sigma_by_class ne couvre pas les classes du pool {classes_missing} "
            "— fail-closed (ADR-0021 : aucun σ de classe deviné)"
        )
    # Decimal → chaîne exacte par classe ; None (« non évaluable ») préservé (null JSON).
    sigma_classe_serialized = {
        k: (None if v is None else str(v)) for k, v in sigma_by_class.items()
    }
    params = {
        "pool": pool,
        "w": w,
        "sample_lead": sample_lead,          # δ (fin de fenêtre) — §M-1
        # σ PAR CLASSE (mapping) + dispatch flux→classe (ADR-0021 item 2) — porteurs
        # (§E, records.LOAD_BEARING_KEYS) : un scalaire legacy y lève au recalcul.
        "sigma_classe": sigma_classe_serialized,
        "sigma_class_of_flux": sigma_class_of_flux,
        "tau_classe": {k: str(v) for k, v in tau_classe.items()},  # MAPPING classe→fraction (ADR-0022)
        "kappa": kappa_note,
        # Calendrier de strates committé ex ante (§5.3) — clé PORTEUSE (§E,
        # records.LOAD_BEARING_KEYS) : recalculable + immutable entre reprises.
        "strate_calendar": strate_spec,
        # Seuils PORTEURS en champs numériques propres (§C) — décident le drapeau
        # et la porte hors-env ; ne pas les laisser dans la seule prose.
        "seuil_historique_valeur": int(SEUIL_HIST),   # 10 (10 §5.4)
        "n_min_hors_enveloppe": N_MIN_HORSENV,        # 4 (10 §5.2)
        "strate_defaut": strate_fn(window_start(start_ts, w)),
        "decimal_prec": DECIMAL_PREC,        # gouverne classification ET stats (§B)
        "harness_version": harness_version,
        # Prose DÉRIVÉE du pool réel (§D) — ne code plus « 3 sources » en dur.
        "classe": (f"BTC/USD-stable, devise marquée par flux (10 §9, décision 4) ; "
                   f"pool configuré = {len(pool)} flux : {pool}"),
        "seuil_historique": ("n·P̂_more·(1−P̂_more) ≥ 10 (10 §5.4 ; UConn OER "
                             "Math 3160 ch.9 p.121)"),
        "seuil_z": "2.33 (point 99% normale standard, K&L — 10 §5.1)",
        "residu_staleness": ("(ii) non évaluable sur une source sans horodatage "
                             "porté (ex. kraken/bitfinex) — fail-open publié par "
                             "source dans le bloc R1 (§G, 03 §1)"),
        "n_windows_demande": n_windows,
        "started_epoch": start_ts,
        "started_utc": _iso_utc(start_ts),
        "note_skeleton": ("walking skeleton borné (plan §3) — PAS le run 24-48 h ; "
                          "hors-enveloppe (i) « non évaluable » quand N<n_min "
                          "répondantes (10 §5.2)"),
        # ── Paramètres R2 (M1c) — PORTEURS (records.R2_LOAD_BEARING_KEYS, §E) : ils
        # gouvernent la partition et les statistiques de contenu (§4.2), donc
        # recalculables et fail-closed sur divergence mi-campagne. Valeurs = design
        # §4.2, jamais inventées (source unique : r2.CONTENT_*).
        "flux_hosts": r2.build_flux_hosts(specs),   # nœuds de partition ; k nominal = #hôtes
        "content_n_min": r2.CONTENT_N_MIN,          # 300 (Fisher, §4.2)
        "content_kappa_value": r2.CONTENT_KAPPA,    # 5 (co-aberrance, §4.2 (2c))
        "content_jump_sigma": r2.CONTENT_JUMP_SIGMA,  # 4σ (δ, §4.2 (2d))
        "content_delta_windows": max(1, round(r2.CONTENT_DELTA_SECONDS / w)),  # Δ=60s → fenêtres
        "content_lag_l": r2.CONTENT_LAG_L,          # ℓ=0 (v0, enregistré)
        "content_big_l": r2.CONTENT_BIG_L,          # L=3 (v0, enregistré)
        "tick_rule": r2.TICK_RULE_DEFAULT,          # « exact » (identité octet-exacte)
        "content_merge_criterion": r2.MERGE_CRITERION_V0,
        # Informationnels (publiés, non fail-closed) :
        # v0 : un résolveur documenté (Cloudflare DoH-JSON) ; multi-résolveurs DÛ à la
        # campagne (résidu 3, plan §2 [C3]). Le résolveur EXACT est aussi journalisé
        # par enregistrement asn_attribution (champ `resolver`).
        "asn_resolvers": list(r2._DEFAULT_RESOLVERS),
        "r2_grid_note": r2.GRID_NOTE,
    }
    journal.append_jsonl(control_path, records.run_params_record(params))

    # Contrôle d'horloge au démarrage (= à chaque reprise) — exigence (c).
    clock_check(specs, control_path, read_fn, start_ts, phase="startup")

    prev_ws: Optional[int] = None
    completed = 0
    while completed < n_windows:
        now = now_fn()
        ws = window_start(now, w)
        if prev_ws is not None and ws <= prev_ws:
            ws = prev_ws + w            # fenêtre courante déjà complétée → la suivante
        # Échantillonner en FIN de fenêtre : dormir jusqu'à ws+w−δ puis lire (le
        # DERNIER relevé de la fenêtre, §5.3 ; δ<w garde l'instant dans [ws,ws+w)).
        ts_sample = ws + w - sample_lead
        if now < ts_sample:
            sleep_fn(ts_sample - now)
        t_read = now_fn()               # instant réel de lecture (≈ ts_sample)
        # 1 relevé/source/fenêtre. fetch_ts = t_read (horloge de mesure du
        # harnais) ; l'écart n'utilise QUE source_ts porté (03 §1).
        for spec in specs:
            r = read_fn(spec, t_read)
            journal.append_jsonl(journal_path, journal.journal_entry(ws, r))
            journal.append_jsonl(raw_path, journal.raw_entry(ws, r))
        # Marqueur de fenêtre COMPLÉTÉE — après les lectures (exigence (a)).
        journal.append_jsonl(control_path, records.window_close_record(ws, strate_fn(ws), t_read))
        prev_ws = ws
        completed += 1
    return completed
