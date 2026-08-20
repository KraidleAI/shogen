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
    "pool", "w", "sigma_classe", "tau_classe", "decimal_prec",
    "seuil_historique_valeur", "n_min_hors_enveloppe", "strate_calendar",
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


def effective_run_params(params_list: list[dict]) -> dict:
    """run_params effectif après contrôle de **présence** ET de **concordance** des
    champs porteurs entre démarrages (fail-closed de recalculabilité, §E).

    Lève si : la liste est vide ; un champ porteur (LOAD_BEARING_KEYS) est ABSENT
    (ou nul) — sinon le harnais recalculerait sous un **défaut silencieux** là où un
    tiers refuse : asymétrie fermée ; ou deux démarrages DIVERGENT sur un champ
    porteur. La concordance garantissant que le dernier démarrage s'accorde au
    premier sur les champs présents, contrôler la présence sur `base` suffit."""
    if not params_list:
        raise ValueError("run_params absent de control.jsonl — journal incomplet")
    base = params_list[0]
    # PRÉSENCE des clés porteuses (symétrie avec l'oracle tiers, §E) : un journal
    # amputé d'une clé qui GOUVERNE le calcul (pool, seuils, calendrier…) n'est pas
    # recalculable — jamais un défaut deviné en silence.
    missing = [k for k in LOAD_BEARING_KEYS if base.get(k) is None]
    if missing:
        raise ValueError(
            f"run_params amputé de clé(s) porteuse(s) {missing} — recalcul refusé "
            "(fail-closed de présence, §E) : un tiers ne devine pas un défaut sur une "
            "clé qui gouverne le calcul"
        )
    divergences = []
    for p in params_list[1:]:
        for k in LOAD_BEARING_KEYS:
            if p.get(k) != base.get(k):
                divergences.append((k, base.get(k), p.get(k)))
    if divergences:
        raise ValueError(
            "run_params divergents entre démarrages — l'historique serait "
            f"reclassé silencieusement (fail-closed, §E) : {divergences}"
        )
    return params_list[-1]


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
    return run_params_list, clock_checks, markers
