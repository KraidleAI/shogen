"""Enregistrements de contrôle du collecteur — écrits via journal.append_jsonl.

`journal.py`, `model.py`, `sources.py` restent **intacts** (plan S2 §3 :
réutilisés tels quels). Ce module n'ajoute que des SCHÉMAS d'enregistrement de
contrôle, écrits dans un troisième journal append-only `control.jsonl`, distinct
de `journal.jsonl` (lectures — une ligne par fenêtre×flux, contrat inchangé) et
de `raw.jsonl` (octets bruts). L'écriture passe par `journal.append_jsonl`
(réutilisé) ; seuls les DICTS sont neufs.

Trois types, discriminés par le champ ``record`` (les lignes de lecture de
`journal.jsonl` produites par `journal.journal_entry` n'ont PAS ce champ) :

  - ``run_params`` : les paramètres de la campagne (§6.1, bloc Paramètres),
    écrits au démarrage pour rendre « recalculable depuis le journal seul »
    (ADR-0003) **littéral** — l'oracle de recalcul ne lit aucun paramètre
    hors-bande (σ_classe, τ_classe, w, précision Decimal… viennent d'ici).
  - ``clock_check`` : le contrôle d'horloge (plan §4.2 [C6]) — plausibilité
    croisée des `source_ts` PORTÉS (jamais l'horloge du harnais, 03 §1),
    consigné, **jamais bloquant** (aucun seuil de rejet). Les offsets ET les
    `source_ts` utilisés sont journalisés pour que l'oracle recalcule la
    médiane depuis l'enregistrement.
  - ``window_close`` : marqueur de fenêtre **complétée**, posé APRÈS les
    lectures (exigence (a) plan §4.1 : harnais-down ≠ source-en-panne — un
    crash mi-fenêtre ne laisse pas de marqueur, la fenêtre n'entre pas dans `n`
    et n'est comptée en panne pour aucune source).
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from typing import Optional

# Champs de run_params qui GOUVERNENT LA RECLASSIFICATION : un désaccord entre
# démarrages ferait recalculer l'historique sous les derniers en silence (§E,
# le mal visé). Les sept premiers sont les entrées de compute_r1. `strate_calendar`
# n'est PAS une entrée de compute_r1 mais gouverne les **étiquettes de strate**
# des marqueurs que compute_r1/L&M groupent : un changement de calendrier
# mi-campagne mélangerait DEUX partitions dans le même `n` par strate — même mal
# visé (§E, anti-complaisance §5.3), donc fail-closed lui aussi. `sample_lead`
# (instant d'échantillonnage), `started_*` et `n_windows_demande` diffèrent
# LÉGITIMEMENT d'une reprise à l'autre et n'entrent nulle part → exclus
# (publiés/visibles, non fail-closed).
LOAD_BEARING_KEYS = (
    "pool", "w", "sigma_classe", "sigma_class_of_flux", "tau_classe",
    "decimal_prec", "seuil_historique_valeur", "n_min_hors_enveloppe",
    "strate_calendar",
)
# `sigma_classe` est désormais un MAPPING classe→plancher (ADR-0021 item 2) et
# `sigma_class_of_flux` un MAPPING flux→classe (nouveau, porteur : un dispatch σ
# divergent entre démarrages reclasserait l'historique en silence, §E). `tau_classe`
# est désormais un MAPPING classe→fraction relative (ADR-0022) — plus un scalaire. Un
# journal legacy portant `sigma_classe` OU `tau_classe` SCALAIRE lève (fail-closed, cf.
# `effective_run_params`) : jamais réinterprété.

# Clés porteuses PROPRES À R2 (M1c) : elles gouvernent la PARTITION et les
# statistiques de contenu — un changement mi-campagne re-partitionnerait en silence
# (même mal §E que les seuils R1). `flux_hosts` définit les nœuds de partition et
# donc k nominal ; les paramètres de contenu (N_min, κ, tick, Δ, ℓ/L, critère de
# fusion) décident quelle paire fusionne. Vérifiées présentes+concordantes par
# `effective_run_params(load_bearing=LOAD_BEARING_KEYS + R2_LOAD_BEARING_KEYS)` dans
# les seuls chemins R2 (r2.recompute_r2_from_journal, report blocs 5-6) — les chemins
# R1/L&M gardent le jeu R1 par défaut (découplage : R1 n'exige pas les clés R2).
R2_LOAD_BEARING_KEYS = (
    "flux_hosts", "content_n_min", "content_kappa_value", "content_lag_l",
    "content_big_l", "content_delta_windows", "content_jump_sigma", "tick_rule",
    "content_merge_criterion",
)


def read_jsonl_tolerant(path: str, *, parse_float=None) -> list[dict]:
    """Relit un JSONL en TOLÉRANT une **dernière** ligne tronquée (crash
    mi-écriture — la machine de Phase A a un historique de coupures, plan §4.2).

    - dernière ligne non vide illisible → **consignée** sur stderr puis ignorée
      (jamais silencieux) ;
    - une ligne illisible **non finale** → corruption → ValueError (fail-closed :
      un journal au milieu corrompu n'est pas recalculable).
    """
    with open(path, encoding="utf-8") as f:
        raw_lines = f.readlines()
    idx = [i for i, ln in enumerate(raw_lines) if ln.strip()]
    objs: list[dict] = []
    for pos, i in enumerate(idx):
        s = raw_lines[i].strip()
        try:
            objs.append(json.loads(s, parse_float=parse_float))
        except json.JSONDecodeError as e:
            if pos == len(idx) - 1:
                sys.stderr.write(
                    f"[s2-harness] AVERTISSEMENT : dernière ligne tronquée ignorée "
                    f"dans {path} (ligne {i + 1}) — crash mi-écriture probable "
                    f"(plan §4.2) ; consigné, non silencieux.\n"
                )
            else:
                raise ValueError(
                    f"ligne JSON corrompue NON finale dans {path} (ligne {i + 1}) : "
                    f"recalcul impossible (fail-closed)"
                ) from e
    return objs


def effective_run_params(params_list: list[dict], load_bearing=LOAD_BEARING_KEYS) -> dict:
    """run_params effectif après contrôle de **présence** ET de **concordance** des
    champs porteurs entre démarrages (fail-closed de recalculabilité, §E).

    Lève si : la liste est vide ; un champ porteur (`load_bearing`) est ABSENT (ou
    nul) — sinon le harnais recalculerait sous un **défaut silencieux** là où un tiers
    refuse : asymétrie fermée ; ou deux démarrages DIVERGENT sur un champ porteur. La
    concordance garantissant que le dernier démarrage s'accorde au premier sur les
    champs présents, contrôler la présence sur `base` suffit.

    `load_bearing` par défaut = jeu R1 (LOAD_BEARING_KEYS) ; les chemins R2 (M1c)
    passent `LOAD_BEARING_KEYS + R2_LOAD_BEARING_KEYS` — R1/L&M restent découplés des
    clés R2 (un journal R1-seul recalcule R1 sans exiger flux_hosts/params contenu)."""
    if not params_list:
        raise ValueError("run_params absent de control.jsonl — journal incomplet")
    base = params_list[0]
    # PRÉSENCE des clés porteuses (symétrie avec l'oracle tiers, §E) : un journal
    # amputé d'une clé qui GOUVERNE le calcul (pool, seuils, calendrier…) n'est pas
    # recalculable — jamais un défaut deviné en silence.
    missing = [k for k in load_bearing if base.get(k) is None]
    if missing:
        raise ValueError(
            f"run_params amputé de clé(s) porteuse(s) {missing} — recalcul refusé "
            "(fail-closed de présence, §E) : un tiers ne devine pas un défaut sur une "
            "clé qui gouverne le calcul"
        )
    # FAIL-CLOSED SCALAIRE LEGACY (ADR-0021 item 6 [C3]) : `sigma_classe` DOIT être un
    # mapping classe→plancher (σ PAR CLASSE). Un journal legacy portant un scalaire
    # (ex. "1e12") LÈVE ici — jamais réinterprété comme un σ unique appliqué à tout
    # (ce serait la déviation silencieuse d'ADR-0020 déc. 3 que cette passe supprime).
    if "sigma_classe" in load_bearing and not isinstance(base.get("sigma_classe"), dict):
        raise ValueError(
            "sigma_classe est un SCALAIRE legacy "
            f"({base.get('sigma_classe')!r}) — attendu : mapping classe→plancher "
            "(σ par classe, ADR-0021 item 2/6). Recalcul refusé, jamais réinterprété "
            "en σ unique (fail-closed) : un scalaire dévierait silencieusement "
            "d'ADR-0020 déc. 3."
        )
    # FAIL-CLOSED SCALAIRE LEGACY τ (ADR-0022) : `tau_classe` DOIT être un mapping
    # classe→fraction (τ PAR CLASSE). Un journal legacy portant un scalaire (ex.
    # "0.005") LÈVE ici — jamais réinterprété comme un τ unique appliqué à tout.
    if "tau_classe" in load_bearing and not isinstance(base.get("tau_classe"), dict):
        raise ValueError(
            "tau_classe est un SCALAIRE legacy "
            f"({base.get('tau_classe')!r}) — attendu : mapping classe→fraction "
            "(τ par classe, ADR-0022). Recalcul refusé, jamais réinterprété en τ unique "
            "(fail-closed) : un scalaire dévierait silencieusement d'ADR-0022."
        )
    divergences = []
    for p in params_list[1:]:
        for k in load_bearing:
            if p.get(k) != base.get(k):
                divergences.append((k, base.get(k), p.get(k)))
    if divergences:
        raise ValueError(
            "run_params divergents entre démarrages — l'historique serait "
            f"reclassé silencieusement (fail-closed, §E) : {divergences}"
        )
    return params_list[-1]


def sigma_tau_from_params(params: dict):
    """`(sigma_by_class, sigma_class_of_flux, tau)` depuis un run_params EFFECTIF
    (ADR-0021) — source partagée par les 4 lecteurs recalculables (r1/lm/r2/report),
    donc jamais de divergence de décodage. `sigma_classe` = mapping classe→secondes
    (Decimal) ou `None` (« non évaluable ») ; `sigma_class_of_flux` = mapping
    flux→classe ; `tau` = mapping classe→fraction (Decimal, ADR-0022). Précondition : `params` est
    passé par `effective_run_params` (qui garantit la présence porteuse ET que
    `sigma_classe` est un mapping — fail-closed sur scalaire legacy)."""
    sbc_raw = params["sigma_classe"]
    sigma_by_class = {
        k: (None if v is None else Decimal(str(v))) for k, v in sbc_raw.items()
    }
    sigma_class_of_flux = dict(params["sigma_class_of_flux"])
    # τ PAR CLASSE (ADR-0022) : mapping classe→fraction, miroir de `sigma_by_class`.
    tau_by_class = {k: Decimal(str(v)) for k, v in params["tau_classe"].items()}
    # Pas de garde 0<τ<1 ICI (chemin recompute) : le collecteur écrit TOUJOURS des τ
    # fractionnels (clé LOAD_BEARING, concordance fail-closed) ; et la suite de tests
    # utilise un τ volontairement grand comme sentinelle « désactive l'axe enveloppe »
    # (miroir du σ géant). La garde de plausibilité τ vit au POINT D'ENTRÉE OPÉRATEUR —
    # le fichier σ/τ committé (`run_campaign._load_committed_sigma_tau`, PAR CLASSE),
    # seul endroit où une main humaine fixe τ.
    return sigma_by_class, sigma_class_of_flux, tau_by_class


def run_params_record(params: dict) -> dict:
    """Bloc Paramètres (§6.1) — recalculabilité littérale (ADR-0003)."""
    return {"record": "run_params", **params}


def clock_check_record(
    harness_ts: float,
    phase: str,
    offsets: dict,
    source_ts_used: dict,
    median_offset: Optional[float],
    note: Optional[str] = None,
) -> dict:
    """Contrôle d'horloge par plausibilité croisée (plan §4.2 [C6], 03 §1).

    `offsets[flux] = harness_ts − source_tsᵢ` pour chaque source portant un
    horodatage ; `source_ts_used` conserve les `source_tsᵢ` pour recalcul.
    """
    return {
        "record": "clock_check",
        "harness_ts": harness_ts,
        "phase": phase,
        "offsets": offsets,
        "source_ts_used": source_ts_used,
        "median_offset": median_offset,
        "note": note,
    }


def window_close_record(ws: int, strate: str, harness_ts: float) -> dict:
    """Marqueur de fenêtre complétée (exigence (a) plan §4.1)."""
    return {
        "record": "window_close",
        "window_start": ws,
        "strate": strate,
        "harness_ts": harness_ts,
    }


def asn_attribution_record(host: str, flux: list, ts: float, resolvers: list,
                           attribution: dict) -> dict:
    """Table ASN datée (§6 bloc 5, R2 axe ASN §4.1) — un relevé par HÔTE, écrit dans
    `control.jsonl` (`record:"asn_attribution"`, ignoré par `parse_control`, lu par
    `parse_asn`). Porte l'hôte, les flux servis, l'heure, les résolveurs, et
    l'attribution rendue par le seam (IP, préfixe, les DEUX bases BGP RIPEstat+Cymru,
    holder pour le nommage ADR-0007, statut). Recalculable : la partition R2 se
    recompute depuis ces lignes seules (r2.compute_partition)."""
    return {"record": "asn_attribution", "host": host, "flux": list(flux),
            "ts": ts, "resolvers": list(resolvers), **attribution}


def append_asn(path: str, rec: dict) -> None:
    """Écrit un enregistrement ASN au journal de contrôle (append-only, via
    journal.append_jsonl — même contrat que les autres records de control.jsonl)."""
    from . import journal
    journal.append_jsonl(path, rec)


def parse_asn(path: str) -> list[dict]:
    """Relit les enregistrements `asn_attribution` de `control.jsonl` (les autres
    types sont ignorés — symétrique de parse_control, qui ignore ceux-ci). Ordre
    d'écriture préservé ; le last-wins par hôte et la détection de divergence d'ASN
    (résidu 4, §4.1) sont faits en aval (r2.compute_partition). Tolérant à une
    dernière ligne tronquée (§F)."""
    return [o for o in read_jsonl_tolerant(path) if o.get("record") == "asn_attribution"]


def parse_control(path: str) -> tuple[list[dict], list[dict], list[dict]]:
    """Relit `control.jsonl` → (run_params_list, clock_checks, window_close).

    **TOUS** les `run_params` sont retournés (un par démarrage), pas seulement
    le dernier : la concordance est vérifiée en aval par `effective_run_params`
    (§E, fail-closed). Marqueurs et clock_checks accumulés dans l'ordre ; la
    déduplication des marqueurs par `window_start` est faite en aval (r1.py),
    pour que la reprise qui re-collecte une fenêtre soit idempotente.
    Lecture tolérante à une dernière ligne tronquée (§F).
    """
    run_params_list: list[dict] = []
    clock_checks: list[dict] = []
    markers: list[dict] = []
    for obj in read_jsonl_tolerant(path):
        rt = obj.get("record")
        if rt == "run_params":
            run_params_list.append(obj)
        elif rt == "clock_check":
            clock_checks.append(obj)
        elif rt == "window_close":
            markers.append(obj)
        # `asn_attribution` (M1c) est volontairement IGNORÉ ici (lu par parse_asn) —
        # rétro-compatible : les trois consommateurs R1/L&M/rapport ne changent pas.
    return run_params_list, clock_checks, markers


def exclusion_ranges(ranges=()) -> list:
    """Plages d'exclusion du lecteur (ADR-0025 déc. 2) : entières, FERMÉES `[from, to]`,
    TRIÉES (déterminisme) ; `from > to` LÈVE (fail-closed, jamais une exclusion vide
    silencieuse). Fournies par l'appelant (CLI du rapport), jamais par une constante."""
    out = sorted((int(a), int(b)) for a, b in ranges)
    inversees = [r for r in out if r[0] > r[1]]
    if inversees:
        raise ValueError(f"plage(s) d'exclusion inversée(s) {inversees} (from > to) — "
                         "fail-closed, jamais une exclusion vide silencieuse")
    return out


def exclude_window_start_ranges(markers: list, ranges=()) -> list:
    """Filtre d'ANALYSE (ADR-0025 déc. 2), jamais une excision du journal : retire les
    marqueurs `window_close` dont le `window_start` ∈ `[from, to]` (bornes incluses), à
    appeler APRÈS `verify_markers_against_spec` ; leurs lectures deviennent orphelines,
    donc hors n, K, P̂_more de toutes les strates (RUNBOOK §6). Sans plage : inchangé."""
    rs = exclusion_ranges(ranges)
    return [m for m in markers if not any(a <= int(m["window_start"]) <= b for a, b in rs)]
