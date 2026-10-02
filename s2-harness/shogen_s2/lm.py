"""L&M — l'estimateur de la fonction de difficulté §5.5, recalculé DEPUIS LE
JOURNAL SEUL (ADR-0003).

Conception : docs/10-mesures-pilotes-design.md §5.5 (transposition Shōgen de
Littlewood & Miller 1989, TSE 1989 — formules re-établies aux pages du PDF) :

    Θ̂_j = m_j/N ;  Ê(Θ) = (1/n)·Σ_j m_j/N ;
    Ê(Θ²) = (1/n)·Σ_j m_j(m_j−1)/(N(N−1))     — **forme par paires** ;
    Var̂(Θ) = Ê(Θ²) − Ê(Θ)²                     — l'écart au modèle d'indépendance
                                                  (L&M éq. 16 : « governed by
                                                  Var(Θ) ») ;
    corrélations **signées** par paire de sources — Cov<0 possible (L&M p.j.1601 :
    un pool anti-corrélé fait *mieux* que l'indépendance), publié avec son signe.

**N = taille du pool (nombre de FLUX), constant** (résolution ADVISOR, M1b) — amendé le
2026-09-29 par ADR-0028 D1 (lot B0) : N = taille du POOL D'ANALYSE de la strate, qui diffère
d'une strate à l'autre au cas (b) (`pool_by_strate`). Motif d'origine : le
design écrit un N sans indice et `m_j | θ_j ~ Binomiale(N, θ_j)` — l'analogue
exact des N versions de K&L. Chaque flux étant toujours évaluable pour la panne
(iii), « N évaluables » = le pool entier. `m_j` = nombre de flux EN ÉCART dans la
fenêtre j, via la MÊME classification que R1 (`r1.classify_cells`, helper partagé)
— zéro divergence R1/L&M, d'où l'**identité de cohérence exacte**

    Ê(Θ) = (1/N)·Σ_i p̂_i        (la moyenne des p̂_i de R1),

car Σ_j m_j = Σ_i écarts(i) = n·Σ_i p̂_i. Exercée par test (test_lm).

**Réalisé en M1c (r2.py) — ce module (bloc 4) reste au niveau FLUX** :
  - corrélations entre CLUSTERS R2 (≥2 membres) via (Θ̂_A,j, Θ̂_B,j), l'analogue
    de l'éq. 35 — exigent la partition R2, calculées par `r2.cluster_lm_correlations`
    (bloc 5, 10 §5.5 pt 4) ; ici, la base commune φ par paire de flux ;
  - agrégation d'indicatrices flux→source (okx_ticker+okx_index → hôte www.okx.com)
    réalisée par la carte flux→hôte de r2 (bloc 5). Ici : phi par paire de **FLUX**
    (C(12,2)=66 paires).

`Decimal` partout, précision FIXÉE (`r1.DECIMAL_PREC`) sur TOUT chemin numérique
→ recalcul bit-identique par l'oracle (ADR-0003). Caveat publié : `m_j` ne compte
que les vrais écarts (`ECARTS`) ; une fenêtre à enveloppe non définie (N<n_min
répondantes) n'invente pas d'écart — NON_EVAL compté 0, comme dans p̂ (fail-closed
de publication, §5.2).
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from itertools import combinations
from typing import Optional

from . import r1
from .r1 import CONTEXTE_DECIMAL, ECARTS, build_window_strate, classify_cells

RENVOI_M1C_CLUSTERS = (
    "corrélations entre CLUSTERS R2 (≥2 membres, analogue L&M éq. 35, séries "
    "(Θ̂_A,j, Θ̂_B,j)) — RÉALISÉ M1c (r2.cluster_lm_correlations, bloc 5) ; requièrent "
    "la partition R2 (10 §5.5 pt 4). Ici (bloc 4) : φ par paire de FLUX, base commune."
)
RENVOI_M1C_FLUX_SOURCE = (
    "agrégation d'indicatrices flux→source (ex. okx_ticker+okx_index) — RÉALISÉ M1c : "
    "les deux flux okx partagent l'hôte www.okx.com → un seul nœud de partition "
    "(r2.build_flux_hosts, bloc 5). Ici (bloc 4) : φ par paire de FLUX (10 §5.5)."
)
CAVEAT_NON_EVAL = (
    "m_j ne compte que les vrais écarts (panne ∨ staleness ∨ hors-env) ; NON_EVAL "
    "hors-env compté 0 comme dans p̂ (fail-closed de publication, 10 §5.2)"
)


def pairwise_second_moment(m: int, N: int) -> Decimal:
    """`m(m−1)/(N(N−1))` — la FORME PAR PAIRES (§5.5). Estimateur sans biais de
    E(Θ²) sous le modèle binomial intra-fenêtre : `E[m(m−1)] = N(N−1)·θ²` (la
    dérivation de rédaction, §5.5 — exercée par test de propriété en S2, test_lm).
    Exige N ≥ 2 (garde chez l'appelant). Précision FIXÉE → recalcul identique."""
    with localcontext(CONTEXTE_DECIMAL):
        return +(Decimal(m * (m - 1)) / Decimal(N * (N - 1)))


def _ecart_indicator(cell) -> int:
    """Indicatrice d'écart d'une cellule (fenêtre×flux) : 1 si vrai écart, sinon 0.
    NON_EVAL et PAS_ECART → 0 (cohérent avec p̂, caveat publié)."""
    return 1 if cell in ECARTS else 0


def phi_coefficient(n11: int, n10: int, n01: int, n00: int) -> Optional[Decimal]:
    """Coefficient phi (Pearson des indicatrices binaires d'écart) — **SIGNÉ**.

    `phi = (n11·n00 − n10·n01) / √((n11+n10)(n01+n00)(n11+n01)(n10+n00))`.
    None si une marge est nulle (une indicatrice constante sur la strate → phi non
    défini) : jamais un 0 fabriqué (fail-closed de publication, §5.2). Précision
    FIXÉE."""
    with localcontext(CONTEXTE_DECIMAL):
        row1, row0 = n11 + n10, n01 + n00
        col1, col0 = n11 + n01, n10 + n00
        if row1 == 0 or row0 == 0 or col1 == 0 or col0 == 0:
            return None
        num = Decimal(n11 * n00 - n10 * n01)
        den = (Decimal(row1) * Decimal(row0) * Decimal(col1) * Decimal(col0)).sqrt()
        return +(num / den)


def _sign(phi: Optional[Decimal]) -> str:
    if phi is None:
        return "non_définie"
    if phi > 0:
        return "+"
    if phi < 0:
        return "−"
    return "0"


def compute_lm(
    markers: list,
    readings: list,
    pool: list,
    w: int,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
    tau: dict,
    n_min: int = r1.N_MIN_HORSENV,
    pool_by_strate: Optional[dict] = None,
) -> dict:
    """Estimateur L&M **par strate**, depuis les enregistrements du journal.

    Consomme la MÊME classification (`r1.classify_cells`, σ PAR CLASSE + τ RELATIF,
    ADR-0021) et les MÊMES marqueurs dédupliqués (`r1.build_window_strate`) que
    `compute_r1` — d'où l'identité de cohérence `Ê(Θ) = (1/N)·Σ_i p̂_i`. Rien n'est
    re-classifié ici. `pool_by_strate` (ADR-0028 D1, cas b) : N = taille du pool de la strate.
    """
    win_strate = build_window_strate(markers)
    cells = classify_cells(markers, readings, pool, w, sigma_by_class,
                           sigma_class_of_flux, tau, n_min)

    windows_by_strate: dict[str, list[int]] = {}
    for ws, st in sorted(win_strate.items()):
        windows_by_strate.setdefault(st, []).append(ws)

    strates_out: dict[str, dict] = {}
    for st, wins in windows_by_strate.items():
        n = len(wins)
        ps = pool if pool_by_strate is None else pool_by_strate[st]
        N = len(ps)
        # m_j et indicatrices d'écart par flux (réutilise la classification R1).
        m_by_win: dict[int, int] = {}
        ind: dict[str, list[int]] = {f: [] for f in ps}
        for ws in wins:
            mj = 0
            for f in ps:
                b = _ecart_indicator(cells[(ws, f)])
                ind[f].append(b)
                mj += b
            m_by_win[ws] = mj
        sum_m = sum(m_by_win.values())

        with localcontext(CONTEXTE_DECIMAL):
            e_theta = (None if (n == 0 or N == 0)
                       else +(Decimal(sum_m) / (Decimal(n) * Decimal(N))))
            if n > 0 and N >= 2:
                acc = Decimal(0)
                for ws in wins:
                    acc += pairwise_second_moment(m_by_win[ws], N)
                e_theta2 = +(acc / Decimal(n))
                var_theta = +(e_theta2 - e_theta * e_theta)
            else:
                # N < 2 : la forme par paires N(N−1) n'existe pas → non calculable
                # (nommé, jamais un 0 fabriqué).
                e_theta2 = None
                var_theta = None

        # Corrélations phi SIGNÉES par paire de FLUX (66 paires pour 12).
        pair_phi: dict[str, dict] = {}
        for a, b in combinations(ps, 2):
            n11 = n10 = n01 = n00 = 0
            for ia, ib in zip(ind[a], ind[b]):
                if ia and ib:
                    n11 += 1
                elif ia and not ib:
                    n10 += 1
                elif not ia and ib:
                    n01 += 1
                else:
                    n00 += 1
            phi = phi_coefficient(n11, n10, n01, n00)
            pair_phi[f"{a}×{b}"] = {
                "phi": phi,
                "signe": _sign(phi),
                "n11": n11, "n10": n10, "n01": n01, "n00": n00,
            }

        strates_out[st] = {
            "n": n,
            "N": N,
            "sum_m": sum_m,
            "E_theta": e_theta,
            "E_theta2": e_theta2,
            "Var_theta": var_theta,
            "pair_phi": pair_phi,
            "renvoi_m1c_clusters": RENVOI_M1C_CLUSTERS,
            "renvoi_m1c_flux_source": RENVOI_M1C_FLUX_SOURCE,
            "caveat_non_eval": CAVEAT_NON_EVAL,
        }

    return {"pool": pool, "N": len(pool), "strates": strates_out}


def recompute_lm_from_journal(control_path: str, journal_path: str, exclude_ranges=(),
                              segment=None) -> dict:
    """Point d'entrée « recalculable depuis le journal seul » (ADR-0003) pour le
    bloc L&M (§6 bloc 4), jumeau de `r1.recompute_from_journal` : lit les paramètres
    de `run_params` et les lectures, calcule L&M par strate."""
    from . import records
    from .window import verify_markers_against_spec

    params_list, _clock, markers = records.parse_control(control_path)
    # Présence + concordance des clés porteuses (fail-closed, §E) — symétrique avec
    # les deux autres points d'entrée recalculables.
    params = records.effective_run_params(params_list)
    # Même garde fail-closed que r1.recompute_from_journal / render_report (§5.3) :
    # les trois points d'entrée « recalculable » rejettent des strates trafiquées.
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            f"strates journalées incohérentes avec le calendrier committé (§5.3) : {div[:5]}"
        )
    # Filtre de lecture unique (ADR-0025 amendée par ADR-0028 D5) APRÈS la garde §5.3 ; journal intact.
    markers, _clock, _asn, _seg = records.filtre_lecture(params, markers, ranges=exclude_ranges,
                                                         segment=segment)
    readings = r1.parse_journal(journal_path)
    pools, pool, _retraits = r1.analysis_pools(markers, readings, list(params["pool"]))  # ADR-0028 D1
    sigma_by_class, sigma_class_of_flux, tau = records.sigma_tau_from_params(params)
    return compute_lm(
        markers=markers,
        readings=readings,
        pool=pool,
        pool_by_strate=pools,
        w=int(params["w"]),
        sigma_by_class=sigma_by_class,
        sigma_class_of_flux=sigma_class_of_flux,
        tau=tau,
        n_min=int(params["n_min_hors_enveloppe"]),
    )
