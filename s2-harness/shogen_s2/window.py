"""Alignement de fenêtre sur l'époque UTC et strate ex ante.

Conception : docs/10-mesures-pilotes-design.md §5.3 (« grille alignée sur
l'époque UTC — personne ne choisit ses bords de fenêtre », A(history-integrity),
04 §5) et §4.2 (`t_j = [j·w, (j+1)·w)`). La convention est **demi-ouverte**
`[début, fin)` : un relevé à l'instant `t` appartient à la fenêtre
`window_start(t) = floor(t/w)·w`. Collecteur et oracle de recalcul DOIVENT
partager cette convention au bord près (test test_window) — sinon `n` diverge.

Calcul **entier** (jamais de division flottante) : `int(t) // w * w`. Les bords
tombent sur des multiples entiers de `w` depuis l'époque, recalculables sans
flottant (ADR-0003) ; `int(t)` tronque vers zéro, ce qui EST `floor` pour un
horodatage epoch (toujours ≥ 0).

Pur, stdlib seul. La strate est une **fonction pure de `window_start` (UTC)**
et d'une **spec de calendrier committée ex ante** (jamais des données testées —
§5.3, A(history-integrity)). M1b ajoute le calendrier **2-strates** calme/stress
(§5.3) : la strate est enregistrée par fenêtre dans le marqueur `window_close`
(records.py) ET la spec dans `run_params` (recalculable + auditable ex ante).

**Cadrage (important, doc 03).** La stratification est une **partition
pré-engagée par calendrier**, PAS une affirmation empirique du monde : elle ne
prétend PAS « les week-ends sont plus volatils » (ce serait un fait à sourcer,
et cela violerait « jamais déduit des données », §5.3) ; elle PARTITIONNE ex
ante pour que n/K/garde §5.4 et l'estimateur L&M se comptent PAR strate si le
régime diffère. Deux niveaux à ne pas confondre : la justification de **principe**
(POURQUOI stratifier par régime) est citée au design (§5.3, cas motivant SK Hynix
2026-07-28 — le régime où A(window-stationarity) casse) ; le **contenu** du
calendrier stress d'un actif **24/7** comme BTC/USD (qui n'a pas d'analogue
littéral de « calendrier de place / heures d'ouverture ») est une **décision
opérateur** à committer ex ante (plan §4.3), jamais une mesure de marché. Le
défaut livré (`WEEKEND_STRATE_SPEC`) est un opt-in ; l'absence de spec = strate
unique silencieuse (`SINGLE_STRATE_SPEC`).
"""

from __future__ import annotations

W_DEFAULT = 60  # secondes (10 §9, décision mainteneur 5 du 2026-08-05 : w = 60 s)
_SECONDS_PER_DAY = 86400

STRATE_DEFAUT = "calme"

# Spec mono-strate (skeleton, back-compat) : toute fenêtre est « calme ».
SINGLE_STRATE_SPEC: dict = {
    "kind": "single",
    "strate": STRATE_DEFAUT,
    "note": "mono-strate (skeleton) — une seule strate « calme » (10 §5.3)",
}

# Spec 2-strates par défaut (M1b) : stress = samedi+dimanche UTC. Partition ex
# ante PAR DÉFAUT, à confirmer/committer par l'opérateur avant lancement
# (plan §4.3). `stress_weekdays` en convention lundi=0..dimanche=6 (comme
# datetime.weekday()) : [5, 6] = {samedi, dimanche}.
WEEKEND_STRATE_SPEC: dict = {
    "kind": "weekend_utc",
    "stress_weekdays": [5, 6],
    "calme": "calme",
    "stress": "stress",
    "note": ("stress = samedi+dimanche UTC. SK Hynix 2026-07-28 (pré-marché "
             "illiquide) motive POURQUOI stratifier par régime en général (10 §5.3) "
             "— PAS « week-end = stress BTC » : BTC/USD est 24/7, sans analogue "
             "littéral de « calendrier de place / heures d'ouverture ». Le choix "
             "week-end=stress pour un actif 24/7 est une DÉCISION OPÉRATEUR à "
             "committer ex ante avant lancement (plan §4.3), défaut par opt-in ; "
             "jamais déduit des données"),
}


def window_start(t: float, w: int = W_DEFAULT) -> int:
    """Début (epoch s **entier**) de la fenêtre UTC demi-ouverte contenant `t`.

    `window_start(t) = floor(t/w)·w`. Retour entier : les statistiques R1 le
    comparent et le regroupent sans flottant (ADR-0003).
    """
    if t < 0:
        raise ValueError(f"horodatage epoch négatif inattendu : {t!r}")
    return (int(t) // w) * w


def window_end(ws: int, w: int = W_DEFAULT) -> int:
    """Fin (exclue) de la fenêtre commençant à `ws` : `t_fin(j) = ws + w`
    (10 §5.2, staleness : `t_fin(j) − horodatageᵢ > σ_classe`)."""
    return ws + w


def weekday_utc(ws: int) -> int:
    """Jour de semaine UTC de la fenêtre `ws`, convention **lundi=0..dimanche=6**
    (comme `datetime.weekday()`), en **arithmétique entière** (jamais de flottant,
    même discipline que `window_start` — ADR-0003).

    L'époque Unix (1970-01-01) est un **jeudi** = 3 dans cette convention, d'où
    `(ws // 86400 + 3) % 7`. Épinglé par test croisé contre
    `datetime.fromtimestamp(ws, timezone.utc).weekday()` (test_window) — aucune
    constante crue sur parole."""
    return (ws // _SECONDS_PER_DAY + 3) % 7


def strate_from_spec(ws: int, spec: dict) -> str:
    """Strate d'une fenêtre depuis une **spec de calendrier committée** (§5.3) —
    fonction pure de `ws` (UTC) et de la spec, jamais des données. Recalculable
    par l'oracle depuis `run_params` seul (ADR-0003)."""
    kind = spec.get("kind")
    if kind == "single":
        return spec.get("strate", STRATE_DEFAUT)
    if kind == "weekend_utc":
        stress_days = spec["stress_weekdays"]
        return spec["stress"] if weekday_utc(ws) in stress_days else spec["calme"]
    raise ValueError(f"spec de calendrier de strate inconnue : {kind!r}")


def make_strate_fn(spec: dict):
    """Ferme sur une spec committée → `strate_fn(ws)` pour le collecteur. La spec
    (et non la fermeture) est enregistrée dans `run_params` : c'est elle qui est
    auditable ex ante et recalculable."""
    return lambda ws: strate_from_spec(ws, spec)


def verify_markers_against_spec(markers: list, spec: dict) -> list:
    """Recalcule la strate de chaque marqueur depuis la spec et retourne les
    divergences `(window_start, strate_journalée, strate_recalculée)`. Une strate
    journalée qui ne concorde pas avec le calendrier committé = strate trafiquée
    ou spec incohérente → **fail-closed** chez l'appelant (oracle/rapport). Preuve
    que les strates du journal SONT celles du calendrier ex ante (anti-complaisance,
    §5.3)."""
    div = []
    for m in markers:
        ws = int(m["window_start"])
        got = m.get("strate")
        want = strate_from_spec(ws, spec)
        if got != want:
            div.append((ws, got, want))
    return div


def default_strate(ws: int) -> str:
    """Strate d'une fenêtre — mono-strate par défaut (back-compat skeleton) : la
    spec `SINGLE_STRATE_SPEC` (§5.3). Le calendrier 2-strates ex ante passe par
    `make_strate_fn(WEEKEND_STRATE_SPEC)` (M1b)."""
    return strate_from_spec(ws, SINGLE_STRATE_SPEC)
