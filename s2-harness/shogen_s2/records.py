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

import base64
import hashlib
import json
import sys
from collections import Counter
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

    - dernière ligne non vide illisible (JSON, ou UTF-8 coupé dans un caractère) → **consignée** sur stderr
      puis ignorée (jamais silencieux) ;
    - une ligne illisible **non finale** → corruption → ValueError (fail-closed :
      un journal au milieu corrompu n'est pas recalculable).
    Lecture en octets, fins de ligne universelles (LF, CRLF, CR, comme le mode texte), décodage UTF-8 ligne par
    ligne : une coupure dans un caractère multi-octets n'empêche plus la lecture (SHOGEN-TORN-LINE-UTF8-1, HS2-03).
    """
    with open(path, "rb") as f:
        raw_lines = f.read().splitlines()
    idx = [i for i, ln in enumerate(raw_lines) if ln.decode("utf-8", "replace").strip()]
    objs: list[dict] = []
    for pos, i in enumerate(idx):
        try:
            objs.append(json.loads(raw_lines[i].decode("utf-8").strip(), parse_float=parse_float))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            utf = isinstance(e, UnicodeDecodeError)
            if pos == len(idx) - 1:
                sys.stderr.write(
                    f"[s2-harness] AVERTISSEMENT : dernière ligne tronquée ignorée "
                    f"dans {path} (ligne {i + 1}{', non décodable en UTF-8' if utf else ''}) — crash mi-écriture "
                    f"probable (plan §4.2) ; consigné, non silencieux.\n"
                )
            else:
                raise ValueError(
                    f"ligne {'non décodable en UTF-8' if utf else 'JSON corrompue'} NON finale dans {path} "
                    f"(ligne {i + 1}) : recalcul impossible (fail-closed)"
                ) from e
    return objs


def verifier_raw(raw_path: str, journal_path: str) -> dict:
    """Lecteur et oracle de `raw.jsonl` (SHOGEN-RAW-LECTEUR-1 ; promesse de journal.py : « le sha256 du journal doit
    y correspondre ») : relecture par le lecteur tolérant, décodage de raw_b64 (base64 strict), sha256 recalculé égal
    à sha256_raw de la ligne, puis à celui de la lecture correspondante de journal.jsonl (même window_start, flux_id,
    fetch_ts ; multiplicités comprises). Tout écart lève ValueError, refus nommé. Rend les comptes de lectures."""
    def cle(o):
        return o.get("window_start"), o.get("flux_id"), o.get("fetch_ts")
    brut: Counter = Counter()
    for o in read_jsonl_tolerant(raw_path, parse_float=Decimal):
        try:
            sha = None if o.get("raw_b64") is None else hashlib.sha256(
                base64.b64decode(o["raw_b64"], validate=True)).hexdigest()
        except (TypeError, ValueError) as e:
            raise ValueError(f"raw.jsonl, lecture {cle(o)} : raw_b64 non décodable (base64 strict) — refus "
                             "(SHOGEN-RAW-LECTEUR-1)") from e
        if sha != o.get("sha256_raw"):
            raise ValueError(f"raw.jsonl, lecture {cle(o)} : sha256 recalculé {sha} ≠ sha256_raw de la ligne "
                             f"{o.get('sha256_raw')} — refus (SHOGEN-RAW-LECTEUR-1)")
        brut[cle(o), sha] += 1
    jour = Counter((cle(o), o.get("sha256_raw")) for o in read_jsonl_tolerant(journal_path, parse_float=Decimal))
    r, j = {k for k, _ in brut - jour}, {k for k, _ in jour - brut}
    for ecart, motif in ((r & j, "sha256 des octets ≠ sha256_raw de journal.jsonl"),
                         (r - j, "lecture(s) de raw.jsonl absente(s) de journal.jsonl"),
                         (j - r, "lecture(s) de journal.jsonl absente(s) de raw.jsonl")):
        if ecart:
            raise ValueError(f"{motif} : {sorted(ecart, key=str)[:5]} — refus (SHOGEN-RAW-LECTEUR-1)")
    return {"lectures": sum(brut.values()), "avec_octets": sum(n for (_k, s), n in brut.items() if s is not None)}


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


def demarrages(path: str) -> list:
    """window_start des marqueurs window_close de chaque démarrage, dans l'ordre du journal (SHOGEN-CENSURE-CAUSES-1,
    ADR-0028 annexe B.23) : un démarrage s'ouvre à chaque run_params et à chaque clock_check de phase « startup »
    (collector.collect écrit les deux en tête de chaque appel, chunk ou reprise : l'un suffit si l'autre manque) ;
    marqueurs écrits avant toute ligne de démarrage : hors de tout démarrage. Lecture tolérante (§F)."""
    out: list = []
    for o in read_jsonl_tolerant(path):
        if o.get("record") == "run_params" or o.get("record") == "clock_check" and o.get("phase") == "startup":
            out.append([])
        elif o.get("record") == "window_close" and out:
            out[-1].append(int(o["window_start"]))
    return out


def exclusion_ranges(ranges=()) -> list:
    """Plages d'exclusion du lecteur (ADR-0025 déc. 2) : entières, FERMÉES `[from, to]`,
    TRIÉES (déterminisme) ; `from > to` ou borne < 0 LÈVE (fail-closed, jamais une exclusion vide
    silencieuse ; SHOGEN-NEG-EPOCH-1). Fournies par l'appelant (CLI du rapport), jamais par une constante."""
    brutes = [tuple(r) for r in ranges]
    if any(float(x) < 0 for r in brutes for x in r):     # avant int() : -0,5 tronqué à 0 passerait
        raise ValueError(f"epoch négatif dans les plages {brutes} — fail-closed (SHOGEN-NEG-EPOCH-1)")
    out = sorted((int(a), int(b)) for a, b in brutes)
    inversees = [r for r in out if r[0] > r[1]]
    if inversees:
        raise ValueError(f"plage(s) d'exclusion inversée(s) {inversees} (from > to) — "
                         "fail-closed, jamais une exclusion vide silencieuse")
    return out


# Champ d'horodatage de chaque type de control.jsonl (ADR-0028 D4, D5 ; HS2-08) ; run_params n'en a pas.
HORODATAGE = {"window_close": "window_start", "asn_attribution": "ts", "clock_check": "harness_ts",
              "run_params": None}


def filtre_horodatage(recs: list, ranges=(), w=None, segment=None) -> list:
    """UN SEUL outil de lecture par horodatage, pour tous les types (ADR-0028 D4, D5 ; HS2-08) : filtre
    d'ANALYSE, jamais une excision du journal. Exclusion d'ADR-0025 déc. 1 amendée par D5 : `window_start`
    dans la plage FERMÉE [A ; B] ; `ts` et `harness_ts` dans [A ; B + w), durée de la dernière fenêtre
    (w de run_params) ; run_params conservé ; type sans règle : ValueError. Segment `(t0, t_fin)`, avant
    l'exclusion : [t0 ; t_fin) semi-ouvert, MÊME borne, tous types (D4). Sans plage ni segment : inchangé."""
    rs = exclusion_ranges(ranges)
    if not rs and segment is None:
        return list(recs)
    out = []
    for r in recs:
        if r.get("record") not in HORODATAGE:
            raise ValueError(f"type {r.get('record')!r} sans champ d'horodatage connu — fail-closed")
        champ = HORODATAGE[r["record"]]
        if champ is not None and r.get(champ) is None:     # jamais KeyError (SHOGEN-BLOC6-TS-1)
            raise ValueError(f"{r['record']} sans {champ} : placement dans le segment ou la plage indécidable — "
                             "fail-closed (SHOGEN-BLOC6-TS-1)")
        if champ is not None and segment is not None and not segment[0] <= r[champ] < segment[1]:
            continue
        if champ == "window_start":
            dedans = any(a <= int(r[champ]) <= b for a, b in rs)
        else:
            dedans = champ is not None and any(a <= r[champ] < b + w for a, b in rs)
        if not dedans:
            out.append(r)
    return out


def t_fin_n_fixe(markers: list, t0, n: int, w: int) -> int:
    """Règle d'arrêt à n fixe (ADR-0024 déc. 1 et 4 ; ADR-0028 D2 pt 6) : `window_start` de la n-ième fenêtre
    DISTINCTE, en ordre croissant, parmi les marqueurs à window_start ≥ t0, comptés AVANT segment et
    exclusion, + w. Aucun défaut (n vient du paquet, w de run_params) ; moins de n fenêtres : ValueError."""
    ws = sorted({int(m["window_start"]) for m in markers if int(m["window_start"]) >= t0})
    if not 1 <= n <= len(ws):
        raise ValueError(f"n fixe = {n} hors de [1 ; {len(ws)}] (fenêtres distinctes ≥ t0) — fail-closed")
    return ws[n - 1] + w


def filtre_lecture(params: dict, markers: list, clock_checks=(), asn=(), ranges=(), segment=None) -> tuple:
    """Point d'application UNIQUE (ADR-0028 D4, D5) des quatre points d'entrée, APRÈS `effective_run_params`
    (run_params conservés) et la garde §5.3 sur TOUS les marqueurs ; w = run_params. Rend (marqueurs,
    clock_checks, asn) filtrés ; journal.jsonl n'est jamais filtré : les lectures d'un marqueur retiré
    deviennent orphelines (hors n, K, P̂_more). `segment` : {"t0", et "t_fin" OU "n_fixe"} ; à n fixe, t_fin
    est lu des marqueurs AVANT segment et exclusion ; t0 ≥ t_fin : ValueError ; bornes (ou None) en 4e.
    t0 < 0 : ValueError (SHOGEN-NEG-EPOCH-1) ; t_fin < 0 ≤ t0 : segment inversé, ValueError aussi."""
    w, seg = params["w"], None
    if segment is not None:
        t0, t_fin, n = segment["t0"], segment.get("t_fin"), segment.get("n_fixe")
        if (t_fin is None) == (n is None):
            raise ValueError("segment : une fin et une seule, t_fin ou n_fixe — fail-closed")
        if t0 < 0:
            raise ValueError(f"segment à epoch négatif (t0 = {t0}) — fail-closed (SHOGEN-NEG-EPOCH-1)")
        seg = (t0, t_fin if n is None else t_fin_n_fixe(markers, t0, n, w))
        if not seg[0] < seg[1]:
            raise ValueError(f"segment [{seg[0]} ; {seg[1]}) vide ou inversé — fail-closed")
    return tuple(filtre_horodatage(list(x), ranges, w, seg) for x in (markers, clock_checks, asn)) + (seg,)


def exclude_window_start_ranges(markers: list, ranges=()) -> list:
    """Cas `window_close` de `filtre_horodatage` (ADR-0025 déc. 2 ; ADR-0028 D5), jamais une excision
    du journal : retire les marqueurs dont le `window_start` ∈ `[from, to]` (bornes incluses), à
    appeler APRÈS `verify_markers_against_spec` ; leurs lectures deviennent orphelines,
    donc hors n, K, P̂_more de toutes les strates (RUNBOOK §6). Sans plage : inchangé."""
    return filtre_horodatage(markers, ranges)
