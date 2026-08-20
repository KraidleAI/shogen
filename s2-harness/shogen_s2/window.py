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

Pur, stdlib seul. La strate par défaut du walking skeleton est **unique**
(« calme ») ; le calendrier ex ante à deux strates calme/stress (§5.3) est un
artefact de Phase B figé avant lancement (plan §4.3), hors périmètre skeleton —
le chemin de code reste par-strate, la strate étant enregistrée par fenêtre
dans le marqueur `window_close` (records.py).
"""

from __future__ import annotations

W_DEFAULT = 60  # secondes (10 §9, décision mainteneur 5 du 2026-08-05 : w = 60 s)

STRATE_DEFAUT = "calme"


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


def default_strate(ws: int) -> str:
    """Strate d'une fenêtre — skeleton mono-strate (§5.3 ; le calendrier
    calme/stress ex ante est Phase B, plan §4.3)."""
    return STRATE_DEFAUT
