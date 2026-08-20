"""Calcul de CLÔTURE DE CALIBRATION (ADR-0021 item 4) — recalculable (ADR-0003).

Pièce ABSENTE du harnais M1c (« P99 » n'existait qu'en prose, CONSTAT M2). Depuis
les **fenêtres de calibration SEULES** (ADR-0020 déc. 1 : 48 h pré-committées, exclues
à jamais de l'inférence), calcule les seuils FINAUX de la campagne :

  - `P99(|écart LOO relatif| honnête)` — clause de révision τ (ADR-0020 :3084-3086 :
    « Révisé par ADR avant lancement si la calibration montre P99(|écart relatif|)
    > 0,25 % ») ;
  - `P99(staleness honnête PAR CLASSE)` puis, par classe évaluable,
    `σ_s = max(plancher_classe, 3 × P99)` (ADR-0020 déc. 3, :3090-3091).

« Honnête » : en calibration, AUCUNE anomalie n'est injectée — les écarts LOO et les
staleness observés SONT la concordance honnête (ADR-0020 déc. 1). On ne filtre donc
que par ÉVALUABILITÉ (enveloppe définie N ≥ n_min et médiane_LOO > 0 ; source_ts
porté pour la staleness), jamais par un jugement d'« honnêteté » qui trierait les
données (ce serait fabriquer le résultat, 04 §5).

**Méthode de percentile — NEAREST-RANK (rang le plus proche), documentée et
déterministe.** Pour N valeurs triées croissant et p ∈ (0,100], le p-ième percentile
est la valeur au rang `⌈p/100 · N⌉` (1-indexé, borné [1, N]) — Wikipedia « Percentile »,
méthode du rang le plus proche. Choisie car : (1) le résultat EST une valeur observée
(aucune interpolation → aucun arrondi Decimal → recalcul bit-identique, ADR-0003) ;
(2) le rang est un ENTIER exact `(p·N + 99)//100` (aucun flottant). Un percentile
interpolé (type 7 R/numpy) introduirait une division Decimal arrondie ; écarté à dessein.

`Decimal` partout, précision FIXÉE (`r1.DECIMAL_PREC`) → recalcul bit-identique par
l'oracle. Zéro dépendance hors stdlib (R-8). Ne lit QUE `control.jsonl` + `journal.jsonl`
(aucun paramètre hors-bande : le dispatch flux→classe vient de run_params).
"""

from __future__ import annotations

import json
import os
import sys
from decimal import Decimal, localcontext
from typing import Optional

from . import records
from .r1 import DECIMAL_PREC, _median, build_window_strate, parse_journal
from .sources import (
    SIGMA_FLOORS_ADR0020_SECONDS,
    TAU_CLASSE_ADR0020_FRACTION,
    TAU_REVISION_THRESHOLD_FRACTION,
)
from .window import verify_markers_against_spec, window_end

PERCENTILE_METHOD = "nearest-rank (rank=ceil(p/100*N), 1-indexe) — Wikipedia Percentile"
STALENESS_MULTIPLIER = 3   # σ_s = max(plancher, 3×P99) (ADR-0020 déc. 3 :3090-3091)


def percentile_nearest_rank(values: list, p: int = 99) -> Optional[Decimal]:
    """p-ième percentile par la méthode du RANG LE PLUS PROCHE (nearest-rank).

    `rang = ⌈p/100 · N⌉` (1-indexé) sur les valeurs triées croissant ; renvoie la
    valeur observée à ce rang. `None` si la liste est vide (percentile non défini —
    fail-closed, jamais un 0 fabriqué). Rang = `(p·N + 99)//100` (entier exact,
    `p ∈ (0,100]`), borné [1, N]. Déterministe et recalculable (ADR-0003)."""
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    rank = (p * n + 99) // 100        # ⌈p·n/100⌉ pour p entier — aucun flottant
    rank = max(1, min(rank, n))
    return s[rank - 1]


def compute_closure(
    control_path: str,
    journal_path: str,
    floors_by_class: Optional[dict] = None,
    percentile: int = 99,
    tau_base: Decimal = TAU_CLASSE_ADR0020_FRACTION,
    tau_revision_threshold: Decimal = TAU_REVISION_THRESHOLD_FRACTION,
) -> dict:
    """Seuils finaux de campagne depuis les fenêtres de CALIBRATION seules.

    Mêmes gardes fail-closed que les points d'entrée recalculables (r1/lm/r2) :
    `effective_run_params` (présence + concordance + sigma_classe mapping) et strates
    journalées == calendrier committé. `floors_by_class` par défaut = planchers
    ADR-0020 (`sources.SIGMA_FLOORS_ADR0020_SECONDS`) ; l'orchestrateur peut passer un
    plancher `oracle_chainlink=None` si le heartbeat n'est PAS confirmé aux feed docs
    (ADR-0021 item 7, injection de VALEUR — jamais un littéral dans le calcul).

    Rend un dict recalculable :
      - `sigma_classe` : classe→σ_s finale (`max(plancher, 3×P99)`), Decimal ou None ;
      - `tau_classe` : τ à committer (= `tau_base` si la clause de révision n'est PAS
        déclenchée ; sinon `None` + `tau_revision_needed=True` — fail-closed : une
        révision de τ est une DÉCISION ADR, jamais devinée ici) ;
      - `p99_ecart_relatif`, `p99_staleness_par_classe`, comptes, méthode.
    """
    if floors_by_class is None:
        floors_by_class = dict(SIGMA_FLOORS_ADR0020_SECONDS)

    params_list, _clock, markers = records.parse_control(control_path)
    params = records.effective_run_params(params_list)
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            "strates journalées incohérentes avec le calendrier committé "
            f"(fail-closed, §5.3) : {div[:5]}{' …' if len(div) > 5 else ''}"
        )
    readings = parse_journal(journal_path)

    _sbc, sigma_class_of_flux, _tau = records.sigma_tau_from_params(params)
    pool = list(params["pool"])
    w = int(params["w"])
    n_min = int(params["n_min_hors_enveloppe"])

    win_strate = build_window_strate(markers)          # fenêtres complétées (dédup)
    reading_map: dict = {}
    for r in readings:                                  # last-wins par (fenêtre, flux)
        reading_map[(int(r["window_start"]), r["flux_id"])] = r

    rel_devs: list = []                                 # |écart LOO relatif| global
    stale_by_class: dict = {}                           # classe → [staleness observées]

    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        for ws in sorted(win_strate):
            we = window_end(ws, w)
            responding = [
                f for f in pool
                if reading_map.get((ws, f)) is not None
                and reading_map[(ws, f)].get("status") == "ok"
                and reading_map[(ws, f)].get("price") is not None
            ]
            resp_price = {f: Decimal(reading_map[(ws, f)]["price"]) for f in responding}
            n_resp = len(responding)
            for f in responding:
                rd = reading_map[(ws, f)]
                # (ii) staleness honnête PAR CLASSE — seulement si horodatage porté.
                src_ts = rd.get("source_ts")
                if src_ts is not None:
                    klass = sigma_class_of_flux.get(f)
                    if klass is not None:
                        stale = Decimal(we) - (src_ts if isinstance(src_ts, Decimal)
                                               else Decimal(str(src_ts)))
                        stale_by_class.setdefault(klass, []).append(+stale)
                # (i) écart LOO RELATIF honnête — enveloppe définie (N ≥ n_min) et
                # médiane_LOO > 0 (même garde fail-closed que classify_ecart).
                if n_resp >= n_min:
                    others = [resp_price[g] for g in responding if g != f]
                    m_loo = _median(others)
                    if m_loo > 0:
                        rel_devs.append(+(abs(resp_price[f] - m_loo) / m_loo))

        # P99 écart relatif (clause τ) + P99 staleness par classe → σ_s.
        p99_rel = percentile_nearest_rank(rel_devs, percentile)
        p99_stale: dict = {}
        sigma_classe: dict = {}
        mult = Decimal(STALENESS_MULTIPLIER)
        for klass, floor in floors_by_class.items():
            observed = stale_by_class.get(klass, [])
            p99 = percentile_nearest_rank(observed, percentile)
            p99_stale[klass] = p99
            if floor is None:
                # Classe « non évaluable » (ex. sans_horodatage, ou oracle_chainlink
                # non confirmé) : σ reste None quelle que soit la donnée (fidélité).
                sigma_classe[klass] = None
            elif p99 is None:
                # Aucune staleness observée en calibration → repli sur le plancher
                # ADR-0020 (pas de 3×P99 calculable) ; nommé, jamais deviné.
                sigma_classe[klass] = Decimal(floor)
            else:
                sigma_classe[klass] = +max(Decimal(floor), mult * p99)

        tau_revision_needed = (p99_rel is not None) and (p99_rel > tau_revision_threshold)

    return {
        "sigma_classe": sigma_classe,
        "tau_classe": (None if tau_revision_needed else tau_base),
        "tau_base": tau_base,
        "tau_revision_needed": tau_revision_needed,
        "tau_revision_threshold": tau_revision_threshold,
        "p99_ecart_relatif": p99_rel,
        "p99_staleness_par_classe": p99_stale,
        "n_ecart_relatif_evaluables": len(rel_devs),
        "n_staleness_par_classe": {k: len(v) for k, v in stale_by_class.items()},
        "n_fenetres_calibration": len(win_strate),
        "floors_by_class": {k: (None if v is None else int(v))
                            for k, v in floors_by_class.items()},
        "staleness_multiplier": STALENESS_MULTIPLIER,
        "percentile": percentile,
        "percentile_method": PERCENTILE_METHOD,
        "note": (
            "Clôture de calibration (ADR-0021 item 4) : σ_s = max(plancher, 3×P99 "
            "staleness honnête PAR CLASSE) ; τ committé = τ_base sauf clause de révision "
            "(P99 écart relatif > seuil → révision par ADR, fail-closed). Recalculable "
            "depuis le journal de calibration seul (ADR-0003)."
        ),
    }


def _jsonable(v):
    """Decimal → chaîne exacte, None préservé (sortie JSON déterministe, recalculable)."""
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, bool):
        return v
    return v


def main(argv: list) -> int:
    """CLI : `python -m shogen_s2.closure <journal_dir_calibration>` → émet le résultat
    de clôture en JSON déterministe (UTF-8) sur stdout. C'est l'artefact que
    l'orchestrateur COMMITTE avant la campagne (ADR-0020 déc. 1 ; R-20 : le worker ne
    committe pas). Ne modifie aucun journal."""
    if len(argv) != 1:
        sys.stderr.write("usage: python -m shogen_s2.closure <journal_dir_calibration>\n")
        return 2
    d = argv[0]
    out = compute_closure(os.path.join(d, "control.jsonl"),
                          os.path.join(d, "journal.jsonl"))
    payload = _jsonable(out)
    sys.stdout.buffer.write(
        (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        .encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
