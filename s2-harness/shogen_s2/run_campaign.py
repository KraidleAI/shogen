"""Driver de lancement de la campagne S2 — glu opératoire MINCE et JETABLE (R-22).

Provenance : mission M2 (worker `claude-opus-4-8`, effort max, 2026-08-20) ;
spec = `RUNBOOK-campagne.md` §2 (driver) et §4 (vérif live) ; paramètres =
`docs/DECISIONS.md` ADR-0020 ; pool = `docs/10-mesures-pilotes-design.md` §3.1.

Ce module n'AJOUTE rien au harnais fermé (skeleton + M1b + M1c) : il ORCHESTRE
`collector.collect(...)` (read path réel) et `r2.collect_asn(...)` (axe ASN réel)
en une boucle restart-tolérante. Zéro dépendance hors stdlib (R-8). Il ne
committe rien et ne déclenche aucun workflow (R-20) : le lancement temps réel
(48 h calibration puis 24-28 j) appartient à l'orchestrateur/investisseur (RUNBOOK
§1/§9). Les journaux vont dans un dossier de segment paramétrable, JAMAIS un
fichier suivi du dépôt (RUNBOOK §1).

────────────────────────────────────────────────────────────────────────────────
CONSTAT M2 (σ/τ) — pourquoi le driver ne peut PAS écrire des `run_params` de
campagne fidèles à ADR-0020 sans décision hors-worker
────────────────────────────────────────────────────────────────────────────────
Le harnais M1c fermé/adjugé ne peut REPRÉSENTER les deux paramètres qu'ADR-0020
(ratifié le 2026-08-20, APRÈS l'adjudication du harnais) rend normatifs :

  • τ RELATIF (ADR-0020 déc. 2 : « |vᵢ − médiane_LOO| / médiane_LOO > τ », un seul
    τ pour la classe) — le harnais compare en ABSOLU : `r1.py:126`
    `abs(price - m_loo) > tau`. τ=0,5 % ne se code pas en un Decimal absolu.

  • σ PAR CLASSE de source (ADR-0020 déc. 3 : places horodatées 30 s ; agrégateurs
    300 s ; sources SANS horodatage → axe (ii) « non évaluable » ; Chainlink 5400 s ;
    Pyth 30 s) — le harnais applique UN scalaire à TOUTES les cellules :
    `r1.py:119` `(win_end - src_ts) > sigma` ; et `report.py:84-85` /
    `r1.py:455-456` lisent un seul `Decimal(str(params["sigma_classe"]))`.
    Un dict y ferait crasher la table §6 (`Decimal(str(dict))` lève) — fail-closed
    DÉMONTRABLE ; un scalaire serait une déviation SILENCIEUSE d'ADR-0020 (P5 ; le
    « mensonge §E » que le harnais lui-même fail-close ailleurs, cf.
    `r2.compute_content` sur `content_lag_l != 0`).

  Nuance mesurée : la sous-règle « sans horodatage → non évaluable » d'ADR-0020
  déc. 3 est DÉJÀ honorée par le harnais (garde `if src_ts is not None`,
  `r1.py:118`) — binance/kraken/bitfinex ne sont jamais flaggés stale, quel que
  soit σ. La partie NON implémentée est donc (a) le τ relatif et (b) la VALEUR de
  σ par classe pour les sources HORODATÉES (place 30 / agrégateur 300 / Pyth 30 /
  Chainlink 5400), qu'un scalaire unique ne peut distinguer.

FAIT qui borne l'urgence (à mettre en tête, ADR-0020 reframe / RUNBOOK §3) : la
CAPTURE est SANS SEUIL. Le journal brut (prix, source_ts, sha256) est
σ/τ-indépendant ; les statuts d'écart sont DÉRIVÉS au recompute. Donc l'archive
J0 n'est PAS bloquée par ce trou : il ne mord qu'au RECOMPUTE (table §6, rapports
J14/J28) et au COMMIT des σ/τ finaux à la clôture de calibration (J0+48 h).

Deux voies de résolution — décision hors-worker (R-20), remontée à l'orchestrateur :
  (1) MISSION HARNAIS : τ relatif + dispatch σ par classe dans `r1.classify_ecart`
      (+ schéma `run_params`, `report.py`, `r2.py`), avec son PROPRE ADR et
      passage G0–G7 (change un comportement adjugé, tests à mettre à jour).
  (2) LANCEMENT en scalaires INTERIM déclarés (`--interim-sigma`/`--interim-tau`),
      DÉCISION INVESTISSEUR — enregistrés comme interim, jamais présentés comme
      ADR-0020 ; à remplacer par les σ/τ fidèles avant toute fenêtre scorée.

Le canon ADR-0020 (σ par classe, τ relatif) vit ici en DONNÉES (constantes
ci-dessous) et dans le compte rendu M2 — JAMAIS écrit au journal comme un
paramètre que le calcul n'honore pas (advisor 2026-08-20, lock 3).
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time
from decimal import Decimal
from typing import Callable, Optional

from . import collector, r2, records, sources, window
from .sources import SPECS

DRIVER_VERSION = "run_campaign(M2)"

# ── ADR-0020 : les σ/τ CANONIQUES — DONNÉES (non exécutables par M1c, cf. CONSTAT) ──
# Unité ÉPINGLÉE (advisor lock 2, anti-piège 100×) : τ est une FRACTION relative
# (0,5 % = 0.005), ni un pourcentage « 0,5 » ni un montant en dollars ; σ en
# SECONDES, par classe de source.
TAU_CLASSE_ADR0020_FRACTION = Decimal("0.005")   # 0,5 % RELATIF — ADR-0020 déc. 2
SIGMA_FLOORS_ADR0020_SECONDS: dict = {           # planchers σ par classe — ADR-0020 déc. 3
    "place_horodatee": 30,       # places à horodatage porté
    "agregateur": 300,           # agrégateurs (CoinGecko/DefiLlama)
    "sans_horodatage": None,     # binance/kraken/bitfinex → axe (ii) « non évaluable »
    "oracle_pyth": 30,           # Pyth : 1,5 × heartbeat établi
    "oracle_chainlink": 5400,    # Chainlink : 1,5 × heartbeat 3600 s (PS-S2-01)
}
# Dispatch flux → classe σ qu'exigerait une implémentation fidèle. Concorde avec
# la disponibilité RÉELLE de source_ts (décodeurs `sources.py`) : les trois
# « sans_horodatage » sont EXACTEMENT les flux dont le décodeur rend source_ts=None.
SIGMA_CLASS_OF_FLUX: dict = {
    "binance": "sans_horodatage", "kraken": "sans_horodatage",
    "bitfinex": "sans_horodatage",
    "coinbase": "place_horodatee", "okx_ticker": "place_horodatee",
    "okx_index": "place_horodatee", "bitstamp": "place_horodatee",
    "gemini": "place_horodatee",
    "coingecko": "agregateur", "defillama": "agregateur",
    "pyth": "oracle_pyth", "chainlink": "oracle_chainlink",
}

# ── σ/τ de DÉMONSTRATION (phase 'demo') — scalaires EXPLICITEMENT non-ADR-0020,
# but = prouver la table §6 de bout en bout (recalculable, déterministe). Ne PAS
# lire comme des seuils de campagne. σ=300 s est évaluable (flag Chainlink stale,
# réaliste) ; τ=50 (absolu, comme les tests adjugés) — ni relatif ni par classe. ──
DEMO_SIGMA_SECONDS = Decimal("300")
DEMO_TAU_ABSOLUTE = Decimal("50")

SAMPLE_LEAD_DEFAULT = 10.0   # δ : 12 lectures HTTP en série dépassent le 5 s du
# skeleton (advisor lock 5) ; 10 < w=60 (piège demi-ouvert) ET 10 < σ_floor min
# évaluable (30 s, places/Pyth) → une source fraîche stale de ~δ ne franchit pas
# le seuil. Publié dans run_params (§M-1), non fail-closed — responsabilité opérateur.


# ── CONSTAT σ/τ : SOURCE DE VÉRITÉ du message fail-closed (robuste à `python -OO`,
# où __doc__ est None). Le résumé du module (docstring) en reprend l'essentiel ;
# ce texte-ci est celui que porte l'exception. ──
CONSTAT_SIGMA_TAU = (
    "CONSTAT M2 (σ/τ) — le harnais M1c fermé/adjugé ne peut REPRÉSENTER les deux "
    "paramètres qu'ADR-0020 (ratifié 2026-08-20, APRÈS l'adjudication du harnais) "
    "rend normatifs.\n"
    "FAIT qui borne l'urgence (en tête) : la CAPTURE est SANS SEUIL (ADR-0020 "
    "reframe / RUNBOOK §3) — le journal brut (prix, source_ts, sha256) est "
    "σ/τ-indépendant ; les statuts d'écart sont DÉRIVÉS au recompute. L'archive J0 "
    "n'est donc PAS bloquée ; le trou ne mord qu'au RECOMPUTE (table §6, J14/J28) et "
    "au COMMIT des σ/τ finaux à la clôture de calibration (J0+48 h — et ce calcul "
    "même, P99 écart LOO relatif + P99 staleness PAR CLASSE d'ADR-0020 déc. 3, "
    "n'existe pas non plus dans le harnais : il fait partie de la voie (1)).\n"
    "Preuves : (a) τ RELATIF (ADR-0020 déc. 2 : |vᵢ−médiane_LOO|/médiane_LOO > τ) — "
    "le harnais compare en ABSOLU (r1.py:126 `abs(price - m_loo) > tau`) ; (b) σ PAR "
    "CLASSE (ADR-0020 déc. 3 : place 30 s / agrégateur 300 s / sans-horodatage « non "
    "évaluable » / Chainlink 5400 s / Pyth 30 s) — le harnais applique UN scalaire "
    "(r1.py:119 `(win_end - src_ts) > sigma`), et report.py:84-85 / r1.py:455-456 "
    "lisent un seul `Decimal(str(params['sigma_classe']))` (un dict y crashe la table "
    "§6 ; un scalaire = déviation silencieuse « mensonge §E »). Nuance : « sans "
    "horodatage → non évaluable » est DÉJÀ honoré (garde `src_ts is not None`, "
    "r1.py:118) ; la partie NON implémentée est τ relatif + la VALEUR de σ par classe "
    "des sources HORODATÉES.\n"
    "Deux voies (décision hors-worker, R-20, remontée orchestrateur) : (1) MISSION "
    "HARNAIS — τ relatif + dispatch σ par classe + le calcul de clôture P99, avec son "
    "propre ADR et G0–G7 (change un comportement adjugé) ; (2) LANCEMENT en scalaires "
    "INTERIM déclarés (--interim-sigma/--interim-tau), DÉCISION INVESTISSEUR, à "
    "remplacer par les σ/τ fidèles avant toute fenêtre scorée. Le canon ADR-0020 "
    "(SIGMA_FLOORS_ADR0020_SECONDS, TAU_CLASSE_ADR0020_FRACTION) vit en DONNÉES + "
    "compte rendu M2, JAMAIS au journal comme un paramètre que le calcul n'honore "
    "pas (advisor 2026-08-20, lock 3)."
)


class SigmaTauNonRepresentable(RuntimeError):
    """Levée quand on demande des `run_params` de campagne/calibration sans σ/τ
    représentables par M1c (cf. CONSTAT du module) et sans override interim
    explicite. Fail-closed : le driver ne fabrique JAMAIS un σ/τ silencieux."""


def _log(msg: str) -> None:
    """Journalisation opératoire sur stderr (stdout réservé). Injectable (tests)."""
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def resolve_sigma_tau(
    phase: str,
    interim_sigma: Optional[str] = None,
    interim_tau: Optional[str] = None,
) -> tuple[Decimal, Decimal, str]:
    """Résout les (σ, τ) SCALAIRES que `collector.collect` sait consommer, sous la
    discipline du CONSTAT σ/τ. Rend `(sigma, tau, regime_label)` ou lève
    `SigmaTauNonRepresentable` (fail-closed).

    - `demo` → scalaires DÉMONSTRATION (non-ADR-0020, but = table §6 de bout en bout).
    - `calibration`/`campagne` SANS interim → fail-closed (CONSTAT).
    - `calibration`/`campagne` AVEC interim explicite → scalaires INTERIM déclarés
      (décision investisseur), à remplacer par les σ/τ fidèles avant scoring.
    """
    if phase == "demo":
        return DEMO_SIGMA_SECONDS, DEMO_TAU_ABSOLUTE, "DÉMO (scalaire, NON-ADR-0020)"
    if interim_sigma is not None and interim_tau is not None:
        return (Decimal(str(interim_sigma)), Decimal(str(interim_tau)),
                "INTERIM scalaire déclaré (décision investisseur — cf. CONSTAT σ/τ ; "
                "à remplacer par les σ/τ fidèles ADR-0020 avant scoring)")
    if interim_sigma is not None or interim_tau is not None:
        raise SigmaTauNonRepresentable(
            "override interim PARTIEL : --interim-sigma ET --interim-tau sont requis "
            "ensemble (les deux seuils définissent l'écart) — fail-closed."
        )
    raise SigmaTauNonRepresentable(CONSTAT_SIGMA_TAU)


def distinct_completed(control_path: str) -> int:
    """Nombre de fenêtres DISTINCTES déjà complétées (dédup par window_start), depuis
    le journal de contrôle seul — support de reprise idempotente (RUNBOOK §2 pt 4 /
    §6). Un fichier absent = 0 (démarrage à froid)."""
    if not os.path.exists(control_path):
        return 0
    _params_list, _clock, markers = records.parse_control(control_path)
    return len({int(m["window_start"]) for m in markers})


def run_segment(
    specs,
    journal_dir: str,
    phase: str,
    n_windows: int,
    *,
    w: int,
    sample_lead: float,
    sigma: Decimal,
    tau: Decimal,
    regime: str,
    chunk_windows: int,
    resolvers: tuple = r2._DEFAULT_RESOLVERS,
    now_fn: Callable[[], float] = time.time,
    sleep_fn: Callable[[float], None] = time.sleep,
    read_fn: Callable = sources.read,
    resolve_fn: Callable[..., dict] = r2.resolve_host_real,
    log: Callable[[str], None] = _log,
) -> int:
    """Boucle de collecte restart-tolérante par CHUNKS (advisor lock 1). Chaque
    itération : (1) `r2.collect_asn` — re-mesure de l'axe ASN (≥ 1 instantané daté
    par chunk = par fenêtre de rapport, RUNBOOK §2 pt 5) ; (2) `collector.collect`
    d'un chunk de fenêtres — qui écrit run_params + clock_check au DÉBUT de chaque
    appel, donc à chaque (re)démarrage de chunk (concordance fail-closed +
    contrôle d'horloge journalisés « gratuitement »).

    Restart-tolérance : la boucle vise `n_windows` fenêtres DISTINCTES complétées ;
    à chaque tour elle relit le compte depuis le journal (dédup marqueurs). Un
    redémarrage de process (coupure de courant, RUNBOOK §1) relance le même chemin
    → run_params réécrit, horloge re-contrôlée, reprise idempotente (last-wins).

    DI complète (now_fn/sleep_fn/read_fn/resolve_fn) : testable sans réseau et
    rejouable par l'oracle (même patron que `collector.collect`)."""
    if n_windows < 1:
        raise ValueError(f"n_windows={n_windows} doit être ≥ 1")
    if chunk_windows < 1:
        raise ValueError(f"chunk_windows={chunk_windows} doit être ≥ 1")
    os.makedirs(journal_dir, exist_ok=True)
    control = os.path.join(journal_dir, "control.jsonl")
    journal_p = os.path.join(journal_dir, "journal.jsonl")
    raw_p = os.path.join(journal_dir, "raw.jsonl")
    pool = [s.flux_id for s in specs]
    # Provenance dans run_params (BLOC 1 de la table §6) : version harnais + driver +
    # régime σ/τ, pour qu'un lecteur de la table VOIE le régime (non porteur, §E).
    hv = f"{collector.HARNESS_VERSION} + {DRIVER_VERSION} [σ/τ={regime}]"

    already = distinct_completed(control)
    if already:
        log(f"[reprise] {already} fenêtre(s) déjà complétée(s) dans {control} — "
            f"poursuite jusqu'à {n_windows} (idempotent : dédup marqueurs, last-wins).")

    chunk_idx = 0
    while True:
        done = distinct_completed(control)
        if done >= n_windows:
            break
        this_chunk = min(chunk_windows, n_windows - done)
        chunk_idx += 1
        log(f"[chunk {chunk_idx}] {done}/{n_windows} fenêtres faites ; "
            f"collecte de {this_chunk} fenêtre(s) + re-mesure ASN.")
        # (1) Axe ASN réel — resolve_fn = r2.resolve_host_real câblé (mission A.3),
        # re-mesuré à chaque chunk (instantané daté, résidu 4 §4.1).
        r2.collect_asn(specs, control, resolve_fn=resolve_fn, resolvers=resolvers,
                       pool=pool)
        # (2) Read path réel — read_fn = sources.read câblé (mission A.3). collect()
        # réécrit run_params (concordance fail-closed) + clock_check à CHAQUE appel.
        collector.collect(
            specs, control, journal_p, raw_p, this_chunk,
            sigma_classe=sigma, tau_classe=tau, w=w, sample_lead=sample_lead,
            strate_spec=window.WEEKEND_STRATE_SPEC,   # week-end=stress (mission A.1)
            now_fn=now_fn, sleep_fn=sleep_fn, read_fn=read_fn,
            harness_version=hv,
        )
    final = distinct_completed(control)
    log(f"[fin] {final} fenêtres distinctes complétées dans {journal_dir}.")
    return final


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m shogen_s2.run_campaign",
        description="Driver de lancement de la campagne S2 (glu jetable — RUNBOOK §2). "
                    "Ne committe rien, ne publie rien (R-20 ; RUNBOOK §8).",
    )
    p.add_argument("--phase", required=True,
                   choices=["demo", "calibration", "campagne"],
                   help="segment. 'demo' = vérif live (σ/τ démo) ; 'calibration'/"
                        "'campagne' = fail-closed sur σ/τ sauf --interim-* (cf. CONSTAT).")
    p.add_argument("--journal-dir", required=True,
                   help="dossier de SEGMENT pour control/journal/raw.jsonl — HORS dépôt "
                        "(RUNBOOK §1) ; calibration et campagne = 2 dossiers DISTINCTS "
                        "(RUNBOOK §3).")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--windows", type=int, help="nombre de fenêtres à collecter.")
    g.add_argument("--duration", type=float,
                   help="durée en SECONDES → n_windows = ceil(durée / w).")
    p.add_argument("--chunk", type=int, default=10,
                   help="fenêtres par chunk (une re-mesure ASN + un run_params/clock_check "
                        "par chunk). Défaut 10.")
    p.add_argument("--w", type=int, default=window.W_DEFAULT,
                   help=f"largeur de fenêtre en s (défaut {window.W_DEFAULT}, ADR-0020/§9).")
    p.add_argument("--sample-lead", type=float, default=SAMPLE_LEAD_DEFAULT,
                   help=f"δ : échantillonnage à ws+w−δ (défaut {SAMPLE_LEAD_DEFAULT}).")
    p.add_argument("--interim-sigma", default=None,
                   help="σ scalaire INTERIM (calibration/campagne) — décision investisseur, "
                        "cf. CONSTAT σ/τ. Requiert --interim-tau.")
    p.add_argument("--interim-tau", default=None,
                   help="τ scalaire INTERIM (calibration/campagne). Requiert --interim-sigma.")
    return p


def main(argv: list) -> int:
    args = _build_parser().parse_args(argv)
    n_windows = (args.windows if args.windows is not None
                 else math.ceil(args.duration / args.w))

    try:
        sigma, tau, regime = resolve_sigma_tau(
            args.phase, args.interim_sigma, args.interim_tau)
    except SigmaTauNonRepresentable as e:
        _log("[FAIL-CLOSED σ/τ] " + str(e))
        return 3

    if args.phase in ("calibration", "campagne"):
        _log(f"[segment] phase={args.phase} → dossier de segment DISTINCT exigé "
             f"(RUNBOOK §3, 2 segments calibration/campagne) : {args.journal_dir}")
    _log(f"[{DRIVER_VERSION}] phase={args.phase} ; régime σ/τ = {regime} ; "
         f"pool = {len(SPECS)} flux (11 sources, OKX en fournit 2) ; "
         f"w={args.w}s δ={args.sample_lead}s ; n_windows={n_windows} chunk={args.chunk} ; "
         f"journal={args.journal_dir}")

    done = run_segment(
        SPECS, args.journal_dir, args.phase, n_windows,
        w=args.w, sample_lead=args.sample_lead, sigma=sigma, tau=tau,
        regime=regime, chunk_windows=args.chunk,
    )
    _log(f"[{DRIVER_VERSION}] terminé : {done}/{n_windows} fenêtres. La table §6 se "
         f"rend par `python -m shogen_s2.report {args.journal_dir}` (recalculable, "
         f"ADR-0003). Aucun commit, aucune publication (R-20 ; RUNBOOK §8).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
