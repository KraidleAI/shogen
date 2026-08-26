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
CONSTAT M2 (σ/τ) — RÉSOLU par ADR-0021 (voie 1)
────────────────────────────────────────────────────────────────────────────────
Le CONSTAT M2 relevait que le harnais M1c ne pouvait REPRÉSENTER τ RELATIF
(ADR-0020 déc. 2) ni σ PAR CLASSE (déc. 3) : il comparait en ABSOLU et appliquait
un σ SCALAIRE unique. **ADR-0021 (voie 1) a rendu l'instrument fidèle** :
  • `r1.classify_ecart` reçoit l'identité du flux et dispatche σ PAR CLASSE
    (`sources.SIGMA_CLASS_OF_FLUX` → `sigma_by_class`), et compare τ en RELATIF
    (`|prix − médiane_LOO| / médiane_LOO > τ`, garde médiane > 0) ;
  • `run_params` porte `sigma_classe` (mapping classe→plancher) + `sigma_class_of_flux`
    (flux→classe) + `tau_classe` (mapping classe→FRACTION, ADR-0022) — un scalaire legacy LÈVE
    (`records.effective_run_params`), jamais réinterprété ;
  • `shogen_s2.closure` calcule, depuis les fenêtres de calibration SEULES, les σ/τ
    FINAUX (`σ_s = max(plancher, 3×P99 staleness/classe)` ; clause de révision τ).

FAIT qui bornait l'urgence (conservé, ADR-0020 reframe / RUNBOOK §3) : la CAPTURE
est SANS SEUIL. Le journal brut (prix, source_ts, sha256) est σ/τ-indépendant ; les
statuts d'écart sont DÉRIVÉS au recompute. Le driver écrit donc des σ/τ FIDÈLES
(plus aucun chemin scalaire, ADR-0021 item 6 [C3]) :
  • `demo`/`calibration` : σ = planchers ADR-0020 PROVISOIRES (per-classe) + τ=0,5 % ;
    la valeur provisoire n'altère pas l'archive (capture sans seuil), et les σ finaux
    sont calculés post-hoc par `closure` sur le journal de calibration ;
  • `campagne` : σ/τ FINAUX committés (clôture de calibration) fournis via
    `--sigma-tau-file` ; ABSENT → fail-closed (ADR-0020 déc. 1 : « seuils finaux
    committés avant la campagne »). Les anciens scalaires INTERIM (voie 2) sont
    SUPPRIMÉS — ADR-0021 :3154-3156 écarte la voie 2.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from decimal import Decimal
from typing import Callable, Optional

from . import collector, records, r2, sources, window
from .sources import SPECS, default_sigma_by_class, default_tau_by_class
# La taxonomie σ (SIGMA_CLASS_OF_FLUX, planchers) est la SOURCE UNIQUE DE VÉRITÉ de
# `sources` (ADR-0021) — les consommateurs l'importent de là ; le driver n'en a
# besoin que via `default_sigma_by_class` (planchers provisoires).

DRIVER_VERSION = "run_campaign(M2+ADR0021)"

SAMPLE_LEAD_DEFAULT = 10.0   # δ : 12 lectures HTTP en série dépassent le 5 s du
# skeleton (advisor lock 5) ; 10 < w=60 (piège demi-ouvert) ET 10 < σ_floor min
# évaluable (30 s, places/Pyth) → une source fraîche stale de ~δ ne franchit pas
# le seuil. Publié dans run_params (§M-1), non fail-closed — responsabilité opérateur.


class SigmaTauNonRepresentable(RuntimeError):
    """Fail-closed σ/τ (ADR-0021) : `campagne` SANS σ/τ finaux committés (clôture de
    calibration, `--sigma-tau-file`), ou fichier committé malformé. Le driver ne
    fabrique JAMAIS un σ/τ silencieux (ADR-0020 déc. 1 : seuils finaux committés avant
    la campagne). Le CONSTAT M2 (harnais non fidèle) est RÉSOLU par ADR-0021 ; ne
    subsiste que ce fail-closed de FOURNITURE des seuils de campagne."""


def _log(msg: str) -> None:
    """Journalisation opératoire sur stderr (stdout réservé). Injectable (tests)."""
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def _load_committed_sigma_tau(path: str) -> tuple[dict, dict, str]:
    """Charge les σ/τ FINAUX committés ASSEMBLÉS (σ = clôture `shogen_s2.closure` ;
    τ PAR CLASSE = ADR-0022 ; PAS la sortie brute de closure — ADR-0020 déc. 1)
    depuis un fichier JSON : `{"sigma_classe": {classe: sec|null}, "tau_classe": {classe: frac}}`.
    Rend `(sigma_by_class, tau_by_class, label)`. Fail-closed (`SigmaTauNonRepresentable`)
    sur fichier absent/illisible, `sigma_classe`/`tau_classe` non-mapping, `tau_classe`
    null (révision τ en attente d'ADR), τ hors (0,1), ou classe sans τ — jamais deviné."""
    if not os.path.exists(path):
        raise SigmaTauNonRepresentable(
            f"--sigma-tau-file introuvable : {path} — les σ/τ FINAUX (clôture de "
            "calibration, `python -m shogen_s2.closure <dir_calib>`) doivent être "
            "committés AVANT la campagne (ADR-0020 déc. 1) — fail-closed."
        )
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
    except (OSError, ValueError) as e:
        raise SigmaTauNonRepresentable(
            f"--sigma-tau-file illisible ({path}) : {e} — fail-closed."
        ) from e
    sc = obj.get("sigma_classe")
    if not isinstance(sc, dict):
        raise SigmaTauNonRepresentable(
            "--sigma-tau-file : `sigma_classe` doit être un mapping classe→plancher "
            f"(σ par classe), reçu {sc!r} — fail-closed (jamais un scalaire, ADR-0021)."
        )
    tc = obj.get("tau_classe")
    if tc is None:
        raise SigmaTauNonRepresentable(
            "--sigma-tau-file : `tau_classe` absent/null → révision de τ EN ATTENTE "
            "(clause ADR-0020 ; P99 écart relatif > seuil). La campagne ne peut lancer "
            "sans τ committé par ADR — fail-closed."
        )
    if not isinstance(tc, dict):
        raise SigmaTauNonRepresentable(
            "--sigma-tau-file : `tau_classe` doit être un mapping classe→fraction "
            f"(τ PAR CLASSE, ADR-0022), reçu {tc!r} — fail-closed (jamais un scalaire)."
        )
    tau = {}
    for k, v in tc.items():
        tv = Decimal(str(v))
        if not (Decimal(0) < tv < Decimal(1)):
            raise SigmaTauNonRepresentable(
                f"--sigma-tau-file : `tau_classe[{k}]`={tv} hors de (0, 1) — τ est une "
                "FRACTION relative (0,45 % = 0.0045), jamais un montant absolu — "
                "fail-closed (garde de plausibilité G7)."
            )
        tau[k] = tv
    sigma_by_class = {k: (None if v is None else Decimal(str(v))) for k, v in sc.items()}
    # Complétude τ PAR CLASSE : chaque classe de σ doit porter un τ (l'axe hors-enveloppe
    # exige un τ dispatché par classe ; un manque = config incomplète, fail-closed).
    missing = [k for k in sigma_by_class if k not in tau]
    if missing:
        raise SigmaTauNonRepresentable(
            f"--sigma-tau-file : classes sans τ committé {missing} — τ PAR CLASSE "
            "incomplet (ADR-0022), fail-closed (jamais un τ deviné)."
        )
    return (sigma_by_class, tau,
            f"CAMPAGNE — σ/τ finaux committés (clôture + ADR τ par classe) : {path}")


def resolve_sigma_tau(
    phase: str,
    sigma_tau_file: Optional[str] = None,
) -> tuple[dict, dict, str]:
    """Résout `(sigma_by_class, tau_by_class, regime_label)` FIDÈLES (σ PAR CLASSE + τ
    PAR CLASSE, ADR-0022 — plus aucun scalaire). Lève `SigmaTauNonRepresentable` (fail-closed).

    - `demo`/`calibration` → σ = planchers ADR-0020 PROVISOIRES (per-classe,
      `sources.default_sigma_by_class`) + τ = 0,5 % relatif. La capture étant SANS
      SEUIL (ADR-0020 reframe), la valeur provisoire n'altère pas l'archive ; les σ
      FINAUX sont calculés post-hoc par `shogen_s2.closure` sur le journal de
      calibration (`σ_s = max(plancher, 3×P99)`).
    - `campagne` → σ/τ FINAUX committés via `--sigma-tau-file` (σ clôture + τ PAR CLASSE
      ADR-0022, ASSEMBLÉS) ; ABSENT/malformé → fail-closed (ADR-0020 déc. 1).
    """
    if phase in ("demo", "calibration"):
        label = ("DÉMO/live-verif — σ planchers ADR-0020 PROVISOIRES (per-classe), "
                 "τ=0,5 % relatif" if phase == "demo" else
                 "CALIBRATION — σ planchers ADR-0020 PROVISOIRES (per-classe) ; σ "
                 "finaux = clôture P99 post-hoc (`shogen_s2.closure`)")
        return default_sigma_by_class(), default_tau_by_class(), label
    if phase == "campagne":
        return _load_committed_sigma_tau(sigma_tau_file) if sigma_tau_file else (
            _raise_campagne_needs_file())
    raise SigmaTauNonRepresentable(f"phase inconnue : {phase!r}")


def _ignored_file_warning(phase: str, sigma_tau_file: Optional[str]) -> Optional[str]:
    """Message d'avertissement (ou None) — mineur G2 : `--sigma-tau-file` n'a de sens
    que pour `campagne` ; fourni à `demo`/`calibration`, il est IGNORÉ (σ planchers
    provisoires per-classe). Fonction PURE → testable sans réseau (le seam d'avertissement
    de `main` est ainsi prouvé, pas seulement documenté)."""
    if sigma_tau_file is not None and phase in ("demo", "calibration"):
        return (f"--sigma-tau-file IGNORÉ en phase '{phase}' (σ planchers provisoires "
                "per-classe ; le fichier ne sert qu'à 'campagne').")
    return None


def _raise_campagne_needs_file():
    raise SigmaTauNonRepresentable(
        "campagne SANS --sigma-tau-file : les σ/τ FINAUX (clôture de calibration, "
        "`python -m shogen_s2.closure <dir_calib>`) doivent être committés avant la "
        "campagne (ADR-0020 déc. 1 ; ADR-0021 :3154-3156 écarte les scalaires INTERIM) "
        "— fail-closed."
    )


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
    sigma_by_class: dict,
    tau: dict,
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
            sigma_by_class=sigma_by_class, tau_classe=tau, w=w, sample_lead=sample_lead,
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
                   help="segment. 'demo'/'calibration' = σ planchers ADR-0020 provisoires "
                        "(per-classe) + τ=0,5 %% ; 'campagne' = σ/τ finaux committés via "
                        "--sigma-tau-file (fail-closed si absent).")
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
    p.add_argument("--sigma-tau-file", default=None,
                   help="phase 'campagne' : chemin du JSON des σ/τ FINAUX committés à la "
                        "clôture de calibration (artefact `python -m shogen_s2.closure "
                        "<dir_calib>`). REQUIS pour 'campagne' ; ignoré (avec "
                        "avertissement) pour 'demo'/'calibration'.")
    return p


def main(argv: list) -> int:
    args = _build_parser().parse_args(argv)
    n_windows = (args.windows if args.windows is not None
                 else math.ceil(args.duration / args.w))

    # Avertissement de configuration incohérente (mineur G2) : --sigma-tau-file n'a de
    # sens que pour 'campagne' ; sur 'demo'/'calibration' il est IGNORÉ (σ provisoires).
    _warn = _ignored_file_warning(args.phase, args.sigma_tau_file)
    if _warn:
        _log("[AVERTISSEMENT] " + _warn)

    try:
        sigma_by_class, tau, regime = resolve_sigma_tau(args.phase, args.sigma_tau_file)
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
        w=args.w, sample_lead=args.sample_lead, sigma_by_class=sigma_by_class, tau=tau,
        regime=regime, chunk_windows=args.chunk,
    )
    _log(f"[{DRIVER_VERSION}] terminé : {done}/{n_windows} fenêtres. La table §6 se "
         f"rend par `python -m shogen_s2.report {args.journal_dir}` (recalculable, "
         f"ADR-0003). Aucun commit, aucune publication (R-20 ; RUNBOOK §8).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
