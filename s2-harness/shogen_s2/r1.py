"""R1 — le test K&L §5 transposé, recalculé DEPUIS LE JOURNAL SEUL (ADR-0003).

Conception : docs/10-mesures-pilotes-design.md §5.1 (formules K&L : `P₀`, `P₁`
par l'**identité élémentaire**, `P_more`, `K`, `z`, seuil 2,33), §5.2 (écarts
i/ii/iii, précédence **panne > staleness > hors-enveloppe**), §5.4 (seuil
« historique insuffisant » `n·P̂_more·(1−P̂_more) ≥ 10`, source UConn OER Math
3160 ch.9 p.121). Plan S2 §3, [C5].

`Decimal` partout, **précision fixée** (`DECIMAL_PREC`) et **arrondi fixé**
(`contexte_decimal()`, neuf, dans chaque `localcontext`, jamais celui de l'appelant : SHOGEN-DECIMAL-ARRONDI-1 et 2,
SHOGEN-DECIMAL-CONTEXTE-1) → recalcul bit-identique par l'oracle. Ne lit QUE les fichiers de journal
(`control.jsonl` + `journal.jsonl`) : aucun accès à Shōgen, aucun paramètre
hors-bande (σ_classe, τ_classe, w, pool viennent de `run_params`).

**Portée (skeleton étendu par M1b, plan §3)** : la **queue binomiale exacte**
`P(K ≥ K_obs | Bin(n, P̂_more))` est ajoutée (§5.4, `binomial_tail_ge`) — sous la
garde, le bloc R1 rend la queue exacte au lieu d'un `z` vide de sens ;
« historique insuffisant » **nu** est réservé aux dégénérés `P̂_more ∈ {0,1}` ou
`n = 0` (queue triviale, sans pouvoir de test). Chemin **par-strate** ; le
calendrier 2-strates ex ante est dans `window.py` (M1b). Le drapeau 2 de §5.6
(« co-défaillance non expliquée par R2 ») requiert `k_eff` (R2) : **réalisé en M1c
(`r2.drapeau_2`)** — ici (bloc R1) seul le drapeau « historique insuffisant » est
calculé ; `r2.drapeau_2` consomme la règle par strate (`regle_critere`, ADR-0028 §1 bis.1 pt 10).

**Identité élémentaire** (10 §5.1, indépendante de la citation, donc du calcul
débloqué) :
    P₀ = Π(1 − p̂ᵢ)
    P₁ = Σᵢ p̂ᵢ · Πⱼ≠ᵢ (1 − p̂ⱼ)          (exactement une défaillance)
    P_more = 1 − P₀ − P₁                    (≥ 2 défaillances)
La FORME IMPRIMÉE de P₁ chez K&L reste une dette de RELECTURE (plan §2 [C2]
dette 9b, tâche lecteur Sonnet 5, une page) — nommée, pas nue ; elle ne bloque
pas ce calcul, qui n'en dépend pas.

**Dénominateur `n` (résolution ADVISOR, cette passe)** : `n` = fenêtres
**complétées** par strate. Une fenêtre où hors-enveloppe est « non évaluable »
(N < 4 répondantes, §5.2) entre dans `n` mais N'EST PAS un écart ; ce compte
« non évaluable » est **publié par source** (bloc R1) — `p̂ = 0` ne peut donc
se lire comme propreté confirmée (fail-closed de publication, §5.2). La lecture
alternative (exclure ces fenêtres de `n`) collapse `n → 0` sur un skeleton
propre à 3 sources et rend la sortie exigée impossible ; l'arithmétique de
budget (10 §9.5 : « n ≳ 10 010 fenêtres ≈ 7,0 jours ») compte bien `n` en
fenêtres calendaires.
"""

from __future__ import annotations

import enum
import math
import sys
from bisect import bisect_left
from collections import Counter
from decimal import ROUND_HALF_EVEN, Context, Decimal, DivisionByZero, InvalidOperation, Overflow, localcontext
from typing import Optional

from . import records
from .model import Status
from .window import strate_from_spec, verify_markers_against_spec, window_end

DECIMAL_PREC = 50                 # précision fixée → recalcul bit-identique (oracle)


def contexte_decimal() -> Context:
    """Contexte nommé complet (SHOGEN-DECIMAL-CONTEXTE-1), neuf à chaque appel : aucun objet partagé à modifier
    (SHOGEN-CONTEXTE-MUTABLE-1) ; passé à chaque localcontext de r1, lm, r2 et report : valeurs du DefaultContext de
    la bibliothèque standard, précision mise à part ; closure.py (quarantaine, D6 i) hors champ."""
    return Context(prec=DECIMAL_PREC, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0,
                   flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])


SEUIL_HIST = Decimal(10)          # n·P̂_more·(1−P̂_more) ≥ 10 (10 §5.4)
N_MIN_HORSENV = 4                 # N ≥ 4 répondantes pour l'enveloppe leave-one-out (10 §5.2)
SEUIL_Z = Decimal("2.33")         # point 99% normale standard (K&L — 10 §5.1)
ELL_BLOC = 240                    # ℓ, fenêtres : choix de conception, seule valeur rendue (ADR-0028 §1 bis.2)
GARDE_BLOCS = 30                  # garde de blocs : z_bloc publié si n_s ≥ 30·ℓ (ADR-0028 §1 bis.1 pt 3)
Z_PUISSANCE = Decimal("0.8416")   # EMD, puissance 0,8 : choix de conception (ADR-0028 §1 bis.1 pt 8)
ETIQUETTE_POOLEE = "exploratoire, hors famille, hors décision"   # strate poolée (ADR-0028 D2 pt 4)
PANNE_TRANSPORT = Status.PANNE_TRANSPORT.value   # lecture PRÉSENTE seule (ADR-0028 annexe D.5)
A_WINDOW_STATIONARITY = (
    "A(window-stationarity) engagée par le test agrégé (10 §5.3 ; ancre "
    "Eckhardt & Lee TM-86369 p. fichier 2, hyp. (ii) « stationary input series ») "
    "— écrite dans chaque sortie R1 ; décharge = stratification ex ante (08)"
)


class Ecart(enum.Enum):
    """Résultat de classification d'un couple (fenêtre, source) — 10 §5.2."""

    PANNE = "panne"                                    # (iii)
    STALENESS = "staleness"                            # (ii)
    HORS_ENVELOPPE = "hors_enveloppe"                  # (i)
    PAS_ECART = "pas_ecart"                            # évalué, aucun écart
    NON_EVAL_HORSENV = "non_evaluable_hors_enveloppe"  # N < 4 répondantes


# Les trois vrais écarts qui alimentent p̂ᵢ (10 §5.1 : « fenêtres où i est en écart »).
ECARTS = frozenset({Ecart.PANNE, Ecart.STALENESS, Ecart.HORS_ENVELOPPE})


def _as_dec(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _median(values: list[Decimal]) -> Decimal:
    # Précision FIXÉE (pas le contexte ambiant) : sinon _median([1, 1+1e-27])
    # diverge prec 28 vs 50 (démontré par l'oracle) → recalcul non identique.
    with localcontext(contexte_decimal()):
        s = sorted(values)
        m = len(s)
        if m % 2 == 1:
            return +s[m // 2]
        return +((s[m // 2 - 1] + s[m // 2]) / Decimal(2))


def _sigma_floor_for_flux(
    flux_id: str,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
) -> Optional[Decimal]:
    """σ (secondes) applicable au flux, par DISPATCH DE CLASSE (ADR-0020 déc. 3 /
    ADR-0021 item 1) : flux → classe (`sigma_class_of_flux`) → plancher
    (`sigma_by_class`). Rend `None` = axe (ii) staleness « non évaluable » pour
    ce flux — soit sa classe porte un plancher `None` (ex. `sans_horodatage`, ou
    `oracle_chainlink` non confirmé, ADR-0021 item 7), soit le flux n'a pas de
    classe déclarée (fail-closed de dispatch : jamais un σ deviné). Aucun littéral
    de classe ici — la VALEUR par classe est injectée via run_params."""
    klass = sigma_class_of_flux.get(flux_id)
    if klass is None:
        return None
    return sigma_by_class.get(klass)


def _tau_for_flux(
    flux_id: str,
    tau_by_class: dict,
    sigma_class_of_flux: dict,
) -> Optional[Decimal]:
    """τ RELATIF applicable au flux, par DISPATCH DE CLASSE (ADR-0022 : τ PAR CLASSE ;
    miroir exact de `_sigma_floor_for_flux`) : flux → classe (`sigma_class_of_flux`) →
    τ (`tau_by_class` classe→fraction). Rend `None` si le flux n'a pas de classe
    déclarée OU si sa classe ne porte pas de τ — l'axe (i) hors-enveloppe devient « non
    évaluable » pour ce flux (fail-closed : jamais un τ deviné). Le loader campagne
    (`run_campaign._load_committed_sigma_tau`) garantit la complétude au lancement."""
    klass = sigma_class_of_flux.get(flux_id)
    if klass is None:
        return None
    return tau_by_class.get(klass)


def classify_ecart(
    reading: Optional[dict],
    others_prices: list[Decimal],
    n_responding: int,
    win_end: int,
    flux_id: str,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
    tau: dict,
    n_min: int = N_MIN_HORSENV,
) -> Ecart:
    """Classe un couple (fenêtre, source), précédence **panne > staleness >
    hors-enveloppe** (10 §5.2). `reading` est la ligne `journal.jsonl` parsée
    (ou None si absente d'une fenêtre complétée = non-réponse). `others_prices`
    = prix des AUTRES répondantes (leave-one-out) ; `n_responding` = nombre
    total de répondantes de la fenêtre (OK avec prix).

    **σ PAR CLASSE (ADR-0021 item 1)** : reçoit `flux_id` et dispatche σ selon la
    CLASSE de la source (`sigma_by_class` classe→plancher, `sigma_class_of_flux`
    flux→classe). σ=None → staleness non évaluable pour ce flux.

    **τ RELATIF PAR CLASSE (ADR-0022 ; ADR-0020 déc. 2, ADR-0021 item 1 [C2a])** :
    hors-enveloppe = `|prix − médiane_LOO| / médiane_LOO > τ_classe`, `τ_classe`
    dispatché par `_tau_for_flux(flux_id, tau, sigma_class_of_flux)` (`tau` = mapping
    classe→fraction ; `None` → axe non évaluable). L'`abs()` reste au
    NUMÉRATEUR ; c'est la DIVISION par la médiane qui définit le critère. GARDE
    `médiane_LOO > 0` fail-closed : une médiane ≤ 0 rend l'enveloppe relative
    indéfinie → « non évaluable », jamais « pas d'écart » (§5.2 ; jamais une
    division par zéro ni un verdict fabriqué). Toute l'arithmétique Decimal est à
    précision FIXÉE (DECIMAL_PREC), comme les statistiques."""
    with localcontext(contexte_decimal()):
        # (iii) panne — précédence maximale : une panne n'a pas de valeur.
        if reading is None or reading.get("status") != "ok" or reading.get("price") is None:
            return Ecart.PANNE
        # (ii) staleness — sur l'horodatage PORTÉ (source_ts), jamais l'horloge
        # harnais (03 §1). σ dispatché PAR CLASSE. source_ts absent (ex. kraken) OU
        # σ_classe None (classe non évaluable) → staleness non évaluable : on passe
        # à (i), sans flaguer (résidu fail-open publié §G).
        sigma = _sigma_floor_for_flux(flux_id, sigma_by_class, sigma_class_of_flux)
        src_ts = reading.get("source_ts")
        if (sigma is not None and src_ts is not None
                and (Decimal(win_end) - _as_dec(src_ts)) > sigma):
            return Ecart.STALENESS
        # (i) hors-enveloppe — l'enveloppe (médiane leave-one-out) exige N ≥ n_min
        # RÉPONDANTES (10 §5.2). Sinon « non évaluable », jamais « pas d'écart ».
        if n_responding >= n_min:
            m_loo = _median(others_prices)
            # GARDE médiane_LOO > 0 (fail-closed [C2a]) : l'écart RELATIF est
            # indéfini pour une médiane ≤ 0 (division par zéro / signe inversé sur
            # une médiane de prix, structurellement dégénérée). Non évaluable —
            # jamais « pas d'écart » (§5.2), jamais un crash du recalcul.
            if m_loo <= 0:
                return Ecart.NON_EVAL_HORSENV
            price = Decimal(reading["price"])
            tau_flux = _tau_for_flux(flux_id, tau, sigma_class_of_flux)
            if tau_flux is None:
                # classe sans τ committé → axe (i) NON évaluable (fail-closed :
                # jamais « pas d'écart » ni « hors-enveloppe » sans τ dispatché).
                return Ecart.NON_EVAL_HORSENV
            if abs(price - m_loo) / m_loo > tau_flux:
                return Ecart.HORS_ENVELOPPE
            return Ecart.PAS_ECART
        return Ecart.NON_EVAL_HORSENV


# ── Formules K&L §5 (identité élémentaire) — Decimal, précision fixée ──────────

def poisson_binomial(phats: list[Decimal]) -> tuple[Decimal, Decimal, Decimal]:
    """(P₀, P₁, P_more) pour des écarts indépendants de probabilités `phats` (10 §5.1). P_more = 1 − P₀ − P₁
    tenu en rationnels exacts, sans annulation Decimal (SHOGEN-PMORE-RESIDU-1) : p̂ᵢ = aᵢ/bᵢ exact
    (`as_integer_ratio`), D = Π bᵢ, N₀ = Π (bᵢ − aᵢ), N₁ = Σᵢ aᵢ·Πⱼ≠ᵢ (bⱼ − aⱼ) en entiers, puis une seule division
    Decimal par valeur : N₀/D, N₁/D, (D − N₀ − N₁)/D. Un seul p̂ᵢ non nul : P_more = 0 exact."""
    d, n0, n1 = 1, 1, 0
    for p in phats:
        a, b = p.as_integer_ratio()
        d, n0, n1 = d * b, n0 * (b - a), n1 * (b - a) + n0 * a
    with localcontext(contexte_decimal()):
        return Decimal(n0) / Decimal(d), Decimal(n1) / Decimal(d), Decimal(d - n0 - n1) / Decimal(d)


def _ecart_relatif(rep: dict, f: str) -> Decimal:
    """|p_f − médiane_LOO|/médiane_LOO d'une cellule arrivée à l'axe (i), `rep` = prix des répondantes de la
    fenêtre : le rapport que classify_ecart compare à τ_classe, même médiane, même précision (ADR-0028
    annexe D.5)."""
    with localcontext(contexte_decimal()):
        m = _median([p for g, p in rep.items() if g != f])
        return +(abs(rep[f] - m) / m)


def _tau_observe(ratios: dict, tau: dict) -> dict:
    """τ observé par classe de τ_classe, sur le segment (ADR-0028 annexe D.5, SHOGEN-TAU-REDERIV-1), sans
    ré-estimation : N cellules, P99 au rang le plus proche (99·N + 99)//100, 1-indexé (méthode documentée de
    closure.percentile_nearest_rank, citée ; closure, en quarantaine, n'est pas importé), maximum ; N = 0 :
    None."""
    out = {}
    for cl in sorted(tau):
        v = sorted(ratios.get(cl, ()))
        out[cl] = {"tau_classe": tau[cl], "N": len(v), "P99": v[(99 * len(v) + 99) // 100 - 1] if v else None,
                   "max": v[-1] if v else None}
    return out


def gate_value(n: int, p_more: Decimal) -> Decimal:
    """`n·P̂_more·(1−P̂_more)` (10 §5.4) — la forme produit-variance."""
    with localcontext(contexte_decimal()):
        return +(Decimal(n) * p_more * (Decimal(1) - p_more))


def insufficient_history(n: int, p_more: Decimal) -> bool:
    """Vrai si `n·P̂_more·(1−P̂_more) < 10` → pas de z publié (10 §5.4)."""
    return gate_value(n, p_more) < SEUIL_HIST


def z_score(n: int, k: int, p_more: Decimal) -> Decimal:
    """`z = (K − n·P_more)/√(n·P_more·(1−P_more))` (10 §5.1), test unilatéral.
    Appeler UNIQUEMENT si `not insufficient_history` (sinon division par ~0)."""
    with localcontext(contexte_decimal()):
        mean = Decimal(n) * p_more
        var = Decimal(n) * p_more * (Decimal(1) - p_more)
        return +((Decimal(k) - mean) / var.sqrt())


def binomial_tail_ge(k_obs: int, n: int, p_more: Decimal) -> Decimal:
    """Queue binomiale exacte `P(K ≥ k_obs | K ~ Bin(n, P̂_more))` — la loi de K
    (§5.1), publiée SOUS la garde §5.4 « au lieu d'un z vide de sens ».

    Somme **directe** `Σ_{x=k_obs}^{n} C(n,x)·p^x·(1−p)^(n−x)` : termes positifs,
    **zéro annulation** (contrairement à `1 − CDF`). Récurrence sur le terme
    `pmf(x+1)/pmf(x) = ((n−x)/(x+1))·(p/(1−p))` → `O(n)` opérations Decimal, sans
    grand entier hormis l'ancre `C(n,k_obs)` (`math.comb`, exacte ; `Decimal(int)`
    est exact — l'arrondi prec ne vient que des produits). Précision FIXÉE
    (`DECIMAL_PREC`) → recalcul bit-identique par l'oracle (ADR-0003).

    **Pré-condition** : `0 < P̂_more < 1` (donc `q = 1 − p > 0`, la récurrence ne
    divise jamais par zéro) et `n ≥ 1`. L'appelant écarte les dégénérés
    `P̂_more ∈ {0,1}` et `n = 0` → « historique insuffisant » **nu** (§5.4 : la
    queue y est triviale, sans pouvoir de test).

    **Poisson `sans objet`** : le « ou Poisson(n·P̂_more) » de §5.4 est une
    *alternative*, jamais une co-publication (l'arête nomme sa statistique, §4.2) ;
    la queue exacte est toujours calculable à l'échelle de campagne (`n ≲ 2·10⁴`,
    10 §9.5), donc Poisson serait du code mort — non implémenté à dessein."""
    with localcontext(contexte_decimal()):
        one = Decimal(1)
        if k_obs <= 0:
            return +one                          # P(K ≥ 0) = 1 (toutes les fenêtres)
        if k_obs > n:
            return +Decimal(0)                   # P(K ≥ k) = 0 pour k > n
        q = one - p_more
        # Ancre pmf(k_obs) = C(n,k_obs)·p^k_obs·q^(n−k_obs) ; puis récurrence O(n).
        term = Decimal(math.comb(n, k_obs)) * (p_more ** k_obs) * (q ** (n - k_obs))
        total = term
        for x in range(k_obs, n):
            term = term * Decimal(n - x) / Decimal(x + 1) * p_more / q
            total += term
        return +total


def z_pool_stratifie(termes) -> tuple[Decimal, Decimal, Decimal]:
    """Strate poolée en forme stratifiée (ADR-0028 D2 pt 4), `termes` = [(n_s, K_s, P̂_more,s)] :
    (Σ_s (K_s − n_s·P̂_s), Σ_s n_s·P̂_s·(1 − P̂_s), z_pool = premier / √second). Jamais l'union brute
    des fenêtres. Un seul terme : la valeur de `z_score`. Dénominateur ≤ 0 : ValueError, jamais une
    valeur fabriquée."""
    with localcontext(contexte_decimal()):
        num = sum((Decimal(k) - Decimal(n) * p for n, k, p in termes), Decimal(0))
        var = sum((Decimal(n) * p * (Decimal(1) - p) for n, k, p in termes), Decimal(0))
        if var <= 0:
            raise ValueError("strate poolée : Σ_s n_s·P̂_s·(1 − P̂_s) ≤ 0, z_pool non défini "
                             "(ADR-0028 D2 pt 4)")
        return +num, +var, +(num / var.sqrt())


def block_long_run_variance(serie, w: int, ell: int = ELL_BLOC) -> dict:
    """Variance de long terme par blocs d'UNE strate (ADR-0028 §1 bis.1 pt 3 ; A-2) :
    σ̂²_bloc = γ̂₀ + 2·Σ_{k=1}^{ℓ−1} (1 − k/ℓ)·γ̂_k, γ̂_k = Σ (I_t − Ī)(I_{t+k} − Ī) sur les paires de la
    grille, Ī = K/n. Forme de Künsch 1989 (P-01, versé et lu : Thm 3.1, éq. (3.9), p. 1224 ; avec ces γ̂_k
    centrés sur Ī, correspondance par les poids, approchée : paquet §10.4) : blocs mobiles, noyau de Bartlett, non
    restreinte. Elle égale (1/ℓ)·Σ_j B_j² (sommes de blocs de la série centrée complétée par des 0), d'où
    σ̂² ≥ 0 et σ̂² = 0 ⇔ K ∈ {0, n} (CRITIQUE v2 §4.1). `serie` : couples (window_start, I_t), window_start
    entiers strictement croissants, écarts multiples de `w`, I_t ∈ {0, 1} ; sinon ValueError. Lag k ⇔ écart
    k·w : une fenêtre absente, exclue ou d'une autre strate ne forme pas de paire. Comptes entiers par lag sur
    masques de bits (bit t : position de grille (ws − ws₀)/w) : M_k paires, C_k = Σ I_t·I_{t+k}, S_g et S_d
    sommes des I des deux membres ; N = ℓ·n²·σ̂² = ℓ·n·K(n − K)
    + Σ_{k=1}^{ℓ−1} 2(ℓ − k)·(n²·C_k − n·K·(S_g + S_d) + M_k·K²), puis une division Decimal par valeur
    (DECIMAL_PREC). Rend n, K, `numerateur` (N), `gamma0`, `sigma2_bloc` ; n = 0 : ces trois-là à None."""
    if not (isinstance(w, int) and isinstance(ell, int) and w >= 1 and ell >= 1):
        raise ValueError(f"variance par blocs : w = {w!r} et ℓ = {ell!r} doivent être des entiers ≥ 1")
    serie, pres, val = list(serie), 0, 0
    for i, (ws, it) in enumerate(serie):
        ok = isinstance(ws, int) and isinstance(it, int) and it in (0, 1)
        d = ws - serie[i - 1][0] if ok and i else w             # types contrôlés avant la soustraction
        if not (ok and d > 0 and d % w == 0):
            raise ValueError(f"variance par blocs : couple n° {i} ({ws!r}, {it!r}) refusé (window_start "
                             f"entier, strictement croissant, écart multiple de w = {w} ; I_t ∈ {{0, 1}})")
        pres |= 1 << (ws - serie[0][0]) // w
        val |= it << (ws - serie[0][0]) // w
    n, k1 = len(serie), val.bit_count()
    if n == 0:
        return {"n": 0, "K": 0, "numerateur": None, "gamma0": None, "sigma2_bloc": None}
    num = ell * n * k1 * (n - k1)                                  # lag 0 : ℓ·n²·γ̂₀
    for k in range(1, ell):
        pk, vk = pres >> k, val >> k                               # bit t : position t + k
        num += 2 * (ell - k) * (n * n * (val & vk).bit_count() + (pres & pk).bit_count() * k1 * k1
                                - n * k1 * ((val & pk).bit_count() + (pres & vk).bit_count()))   # n²·γ̂_k
    with localcontext(contexte_decimal()):
        return {"n": n, "K": k1, "numerateur": num, "gamma0": +(Decimal(n * k1 - k1 * k1) / Decimal(n)),
                "sigma2_bloc": +(Decimal(num) / Decimal(ell * n * n))}


def bloc_strate(serie, w: int, p_more: Decimal, gate: Decimal, ell: int = ELL_BLOC) -> dict:
    """Clé `bloc` d'une strate (ADR-0028 §1 bis.1 pts 3 et 9 ; A-2), schéma fermé de 12 clés : ell, gamma0,
    sigma2_bloc, cv_theorique, FIV, R_centrage, FIV_serie, FIV_motif, FIV_serie_motif, z_bloc, z_bloc_motif,
    runs. `serie` : celle de `block_long_run_variance` ; `p_more`, `gate` : P̂_more et n·P̂_more(1 − P̂_more)
    (`gate_value`) de la strate. FIV = σ̂²_bloc/garde, R_centrage = γ̂₀/garde (= Ī(1 − Ī)/(P̂(1 − P̂))),
    FIV_serie = σ̂²_bloc/γ̂₀ : une division Decimal chacune, sur les valeurs publiées ; garde ≤ 0 : FIV et
    R_centrage à None (FIV_motif) ; γ̂₀ = 0 : FIV_serie à None (FIV_serie_motif). cv_theorique = √(4ℓ/(3n))
    [inféré : dérivation AVIS-advisor-defi Q1 (iv), pas un énoncé de Künsch]. z_bloc = (K − n·P̂_more)/
    σ̂_bloc, numérateur de z_s, publié si σ̂²_bloc > 0 et n ≥ GARDE_BLOCS·ℓ (pt 3), que la garde §5.4 soit
    tenue ou non (le NON ÉVALUABLE du pt 5 relève du lot CRITERE) ; sinon None et z_bloc_motif. runs (pt 9,
    descriptif) : un run = positions de grille consécutives à I_t = 1 ; une fenêtre absente ou d'une autre
    strate le coupe ; longueur_moyenne = K/nombre, None si nombre = 0."""
    serie = list(serie)                                   # deux parcours (variance, runs) : itérateur admis
    v = block_long_run_variance(serie, w, ell)
    n, k1, g0, s2 = v["n"], v["K"], v["gamma0"], v["sigma2_bloc"]
    nombre = run_max = c = 0
    avant = None
    for ws, it in serie:
        c = (c + 1 if avant == ws - w else 1) if it else 0
        nombre, run_max, avant = nombre + (c == 1), max(run_max, c), ws
    with localcontext(contexte_decimal()):
        if n == 0:
            mz = mf = ms = "aucune fenêtre (n = 0)"
        else:
            garde_b = f"garde de blocs : n_s = {n} < {GARDE_BLOCS}·ℓ = {GARDE_BLOCS * ell}"
            mz = " ; ".join(m for m, oui in (("σ̂²_bloc = 0 (K ∈ {0, n})", s2 == 0),
                                             (garde_b, n < GARDE_BLOCS * ell)) if oui) or None
            mf = None if gate > 0 else "garde n·P̂_more·(1 − P̂_more) ≤ 0 : FIV, R_centrage indéfinis"
            ms = None if g0 != 0 else "γ̂₀ = 0 (K ∈ {0, n}) : FIV_serie indéfini"
        moy = +(Decimal(k1) / Decimal(nombre)) if nombre else None
        return {"ell": ell, "gamma0": g0, "sigma2_bloc": s2,
                "cv_theorique": +(Decimal(4 * ell) / Decimal(3 * n)).sqrt() if n else None,
                "FIV": None if mf else +(s2 / gate), "R_centrage": None if mf else +(g0 / gate),
                "FIV_serie": None if ms else +(s2 / g0), "FIV_motif": mf, "FIV_serie_motif": ms,
                "z_bloc": None if mz else +((Decimal(k1) - Decimal(n) * p_more) / s2.sqrt()),
                "z_bloc_motif": mz, "runs": {"nombre": nombre, "longueur_moyenne": moy, "run_max": run_max}}


# ── Agrégation R1 depuis le journal ──────────────────────────────────────────

class PrixIllisible(ValueError):
    """Prix de journal.jsonl ni chaîne ni nombre JSON, ou chaîne que Decimal ne lit pas (SHOGEN-PRIX-ILLISIBLE-1)."""


class PrixHorsContexte(ValueError):
    """Prix fini de journal.jsonl d'exposant ajusté au-delà d'Emax du contexte nommé (SHOGEN-PRIX-HORS-CONTEXTE-1)."""


def parse_journal(path: str) -> list[dict]:
    """Relit `journal.jsonl` (une ligne par fenêtre×flux). `parse_float=Decimal`
    → `source_ts` exact (ADR-0003) ; `price` reste chaîne (déjà exacte).
    Lecture TOLÉRANTE à une dernière ligne tronquée (crash mi-écriture, §F).
    Point unique des lectures de R1, L&M, R2 et du rapport (lot CORR, SHOGEN-PRIX-NON-FINI-1) : un prix non fini (NaN,
    sNaN, Infinity, toute casse ou forme que Decimal admet) est lu comme absent (None : panne au sens de
    classify_ecart), quel que soit le statut, compté par flux sur stderr, jamais la valeur. Refus nommés, quel que soit
    le statut, valeur jamais reproduite : prix ni chaîne ni nombre JSON (booléen, liste, objet), ou chaîne que Decimal
    ne lit pas, PrixIllisible (SHOGEN-PRIX-ILLISIBLE-1) ; prix fini non nul d'exposant ajusté au-delà d'Emax du
    contexte nommé, PrixHorsContexte (SHOGEN-PRIX-HORS-CONTEXTE-1) ; tout autre prix fini : inchangé."""
    lus, nf, ctx = records.read_jsonl_tolerant(path, parse_float=Decimal), Counter(), contexte_decimal()
    with localcontext(ctx):                         # « abc » lève sous ce contexte (illisible : refus), jamais NaN
        for r in (x for x in lus if isinstance(x, dict) and x.get("price") is not None):
            p = r["price"]
            try:                                    # float : jetons JSON NaN, Infinity (parse_float ne les lit pas)
                d = Decimal(p) if isinstance(p, (str, int, float, Decimal)) and not isinstance(p, bool) else None
            except (ValueError, ArithmeticError):
                d = None
            if d is None or d.is_finite() and d and d.adjusted() > ctx.Emax:
                ou = (f"dans {path} (flux {r.get('flux_id')!r}, window_start {r.get('window_start')!r} ; valeur non "
                      "reproduite)")
                if d is None:
                    raise PrixIllisible(f"prix ni chaîne ni nombre JSON lu par Decimal {ou} — refus "
                                        "(SHOGEN-PRIX-ILLISIBLE-1)")
                raise PrixHorsContexte(f"prix fini d'exposant au-delà d'Emax = {ctx.Emax} du contexte nommé {ou} — "
                                       "refus (SHOGEN-PRIX-HORS-CONTEXTE-1)")
            if not d.is_finite():
                r["price"] = None
                nf[r.get("flux_id")] += 1
    if nf:
        sys.stderr.write(f"[s2-harness] AVERTISSEMENT : prix non fini(s) lu(s) comme absent(s) dans {path}, fichier "
                         "entier — par flux : " + ", ".join(f"{f} {k}" for f, k in sorted(nf.items(), key=str))
                         + " (SHOGEN-PRIX-NON-FINI-1 : panne au sens de classify_ecart ; valeurs non reproduites).\n")
    return lus


def build_window_strate(markers: list[dict]) -> dict[int, str]:
    """Fenêtres complétées, **dédupliquées** par `window_start` (reprise
    idempotente, §5.3) — le dernier marqueur gagne (strate déterministe)."""
    win_strate: dict[int, str] = {}
    for m in markers:
        win_strate[int(m["window_start"])] = m["strate"]
    return win_strate


def build_reading_map(readings: list[dict]) -> dict[tuple[int, str], dict]:
    """Lectures indexées par (fenêtre, flux) — **last-wins** (« le dernier de
    la fenêtre », §5.3 : règle de lecture autant que de collecte)."""
    reading_map: dict[tuple[int, str], dict] = {}
    for r in readings:
        reading_map[(int(r["window_start"]), r["flux_id"])] = r
    return reading_map


def analysis_pools(markers: list[dict], readings: list[dict], pool: list[str]) -> tuple:
    """Pool d'analyse (ADR-0028 D1) sur les fenêtres RETENUES (après garde §5.3 et exclusion) et
    leurs lectures last-wins, orphelines exclues ; ok = statut ok ET prix (le prédicat de réponse
    de `classify_ecart`). Rend (pool par strate, pool du segment [cas a], retraits (strate, flux,
    ok, lectures, n)) ; sans fenêtre retenue, aucun retrait."""
    win_strate = build_window_strate(markers)
    n = Counter(win_strate.values())
    ok: Counter = Counter()
    tot: Counter = Counter()
    for (ws, f), rd in build_reading_map(readings).items():
        if ws in win_strate:
            tot[win_strate[ws], f] += 1
            ok[win_strate[ws], f] += rd.get("status") == "ok" and rd.get("price") is not None
    by_strate = {st: [f for f in pool if ok[st, f]] for st in sorted(n)}
    segment = [f for f in pool if not n or any(ok[st, f] for st in n)]
    retraits = [(st, f, ok[st, f], tot[st, f], n[st]) for st in sorted(n) for f in pool
                if not ok[st, f]]
    return by_strate, segment, retraits


def _classify_window(
    ws: int,
    reading_map: dict[tuple[int, str], dict],
    pool: list[str],
    w: int,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
    tau: dict,
    n_min: int = N_MIN_HORSENV,
) -> dict[str, Ecart]:
    """Classe chaque source du pool dans la fenêtre `ws`. Répondantes = OK avec
    prix ; l'enveloppe leave-one-out se calcule sur elles (N ≥ n_min, §5.2).
    σ dispatché PAR CLASSE via `sigma_by_class`/`sigma_class_of_flux` (ADR-0021)."""
    responding = [
        f for f in pool
        if reading_map.get((ws, f)) is not None
        and reading_map[(ws, f)].get("status") == "ok"
        and reading_map[(ws, f)].get("price") is not None
    ]
    resp_price = {f: Decimal(reading_map[(ws, f)]["price"]) for f in responding}
    n_resp = len(responding)
    out: dict[str, Ecart] = {}
    for f in pool:
        others = [resp_price[g] for g in responding if g != f]
        out[f] = classify_ecart(reading_map.get((ws, f)), others, n_resp,
                                 window_end(ws, w), f, sigma_by_class,
                                 sigma_class_of_flux, tau, n_min)
    return out


def classify_cells(
    markers: list[dict],
    readings: list[dict],
    pool: list[str],
    w: int,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
    tau: dict,
    n_min: int = N_MIN_HORSENV,
) -> dict[tuple[int, str], Ecart]:
    """Écart de chaque cellule (fenêtre×source) des fenêtres complétées — pour
    le bloc « Journal brut » de la table §6 (report.py). Même logique que
    compute_r1 (helper partagé), donc jamais de divergence."""
    win_strate = build_window_strate(markers)
    reading_map = build_reading_map(readings)
    out: dict[tuple[int, str], Ecart] = {}
    for ws in sorted(win_strate):
        cls = _classify_window(ws, reading_map, pool, w, sigma_by_class,
                               sigma_class_of_flux, tau, n_min)
        for f in pool:
            out[(ws, f)] = cls[f]
    return out


def strate_poolee(strates: dict) -> dict:
    """Strate poolée (ADR-0028 D2 pt 4 ; §1 bis.1 pt 9 ; §1 bis.11 item 14) : hors de `strates`, donc
    hors règle, drapeau 2 et famille. Entrées par strate : n, K, P̂_more, pool d'analyse D1 et sa taille.
    z_pool publié si au moins deux strates et si chacune publie son z (garde §5.4 tenue) ; sinon None
    et motif."""
    ent = {st: {"n": b["n"], "K": b["K"], "P_more": b["P_more"], "pool": list(b["per_source"]),
                "N": len(b["per_source"])} for st, b in strates.items()}
    sous = [f"« {st} »" + ("" if b["queue_exacte_applicable"] else " (dégénérée : P̂_more ∈ {0,1})")
            for st, b in strates.items() if b["z"] is None]
    motif = ("aucune fenêtre complétée (n = 0)" if not strates else
             f"une seule strate au segment (« {next(iter(strates))} ») : la forme stratifiée somme au moins "
             "deux strates" if len(strates) < 2 else
             "strate(s) sous la garde §5.4, z de strate non publié : " + " ; ".join(sous) if sous else None)
    num, var, z = (None,) * 3 if motif else z_pool_stratifie(
        [(b["n"], b["K"], b["P_more"]) for b in strates.values()])
    return {"etiquette": ETIQUETTE_POOLEE, "strates": ent, "numerateur": num, "variance": var, "z_pool": z,
            "motif": motif}


def compute_r1(
    markers: list[dict],
    readings: list[dict],
    pool: list[str],
    w: int,
    sigma_by_class: dict,
    sigma_class_of_flux: dict,
    tau: dict,
    seuil_hist: Decimal = SEUIL_HIST,
    n_min: int = N_MIN_HORSENV,
    pool_by_strate: Optional[dict] = None,
) -> dict:
    """Calcule R1 par strate depuis les enregistrements du journal.

    - **Dédup des marqueurs** par `window_start` (reprise idempotente, §5.3).
    - **Last-wins** par (fenêtre, flux) : re-collecte d'une fenêtre → la
      dernière lecture gagne (« le dernier de la fenêtre », §5.3).
    - `n` = fenêtres complétées **par strate** ; `pool_by_strate` : pool de chaque strate
      (ADR-0028 D1, cas b), `pool` par défaut.
    """
    win_strate = build_window_strate(markers)      # dédup par window_start (§5.3)
    reading_map = build_reading_map(readings)       # last-wins par (fenêtre, flux)

    if not win_strate:
        return {
            "pool": pool,
            "strates": {},
            "note": "aucune fenêtre complétée (n = 0)",
            "flag_historique_insuffisant": True,
            "poolee": strate_poolee({}),
            "tau_observe": _tau_observe({}, tau),
            "A_window_stationarity": A_WINDOW_STATIONARITY,
        }

    # Groupement des fenêtres par strate.
    windows_by_strate: dict[str, list[int]] = {}
    for ws, st in sorted(win_strate.items()):
        windows_by_strate.setdefault(st, []).append(ws)

    strates_out: dict[str, dict] = {}
    ratios: dict = {}                              # τ observé : classe → rapports de l'axe (i) du segment
    for st, wins in windows_by_strate.items():
        n = len(wins)
        ps = pool if pool_by_strate is None else pool_by_strate[st]
        # Compteurs par source.
        tally = {f: {k: 0 for k in Ecart} for f in ps}
        stale_evaluable = {f: 0 for f in ps}
        ok_windows = {f: 0 for f in ps}
        k_count = 0
        dk = dict.fromkeys(("pt_2_plus", "pt_1", "pt_0", "tous_hors_enveloppe", "c"), 0)   # annexe D.5
        serie = []                                 # (window_start, I_t) de la strate (ADR-0028 §1 bis.1 pt 3)
        for ws in wins:
            cls = _classify_window(ws, reading_map, ps, w, sigma_by_class,
                                   sigma_class_of_flux, tau, n_min)
            win_ecarts = pt = he = 0
            rep = {}                               # répondantes de la fenêtre (enveloppe leave-one-out)
            for f in ps:
                rd = reading_map.get((ws, f))
                if rd is not None and rd.get("status") == "ok" and rd.get("price") is not None:
                    ok_windows[f] += 1
                    rep[f] = Decimal(rd["price"])
                    if rd.get("source_ts") is not None:
                        stale_evaluable[f] += 1
                pt += rd is not None and rd.get("status") == PANNE_TRANSPORT
                kind = cls[f]
                tally[f][kind] += 1
                if kind in ECARTS:
                    win_ecarts += 1
                    he += kind is Ecart.HORS_ENVELOPPE
            for f in ps:                           # axe (i) atteint : hors-enveloppe ou pas d'écart
                if cls[f] in (Ecart.HORS_ENVELOPPE, Ecart.PAS_ECART):
                    ratios.setdefault(sigma_class_of_flux[f], []).append(_ecart_relatif(rep, f))
            if win_ecarts >= 2:
                k_count += 1
                dk["pt_2_plus" if pt >= 2 else f"pt_{pt}"] += 1
                dk["tous_hors_enveloppe"] += he == win_ecarts
            dk["c"] += bool(ps) and pt == len(ps)
            serie.append((ws, int(win_ecarts >= 2)))  # même sommande que K

        per_source = {}
        phats: list[Decimal] = []
        residu_fail_open: list[str] = []
        for f in ps:
            t = tally[f]
            ecart = t[Ecart.PANNE] + t[Ecart.STALENESS] + t[Ecart.HORS_ENVELOPPE]
            # p̂ᵢ à la précision FIXÉE (pas le contexte ambiant) → recalcul
            # bit-identique quel que soit le contexte de l'oracle (ADR-0003).
            with localcontext(contexte_decimal()):
                phat = +(Decimal(ecart) / Decimal(n))
            phats.append(phat)
            axes = ["panne"]                       # (iii) toujours évaluable
            if stale_evaluable[f] > 0:
                axes.append("staleness")           # (ii) si horodatage porté
            if t[Ecart.HORS_ENVELOPPE] + t[Ecart.PAS_ECART] > 0:
                axes.append("hors_enveloppe")      # (i) si une fenêtre eut N≥n_min
            # Résidu fail-open (§G) : source qui RÉPOND mais ne porte jamais
            # d'horodatage (ex. kraken) → (ii) non évaluable, un « stale mais
            # répondant » passerait inaperçu. Rendu VISIBLE, pas seulement en
            # commentaire.
            fail_open = ok_windows[f] > 0 and stale_evaluable[f] == 0
            if fail_open:
                residu_fail_open.append(f)
            per_source[f] = {
                "phat": phat,
                "ecart": ecart,
                "panne": t[Ecart.PANNE],
                "staleness": t[Ecart.STALENESS],
                "hors_enveloppe": t[Ecart.HORS_ENVELOPPE],
                "non_eval_hors_env": t[Ecart.NON_EVAL_HORSENV],
                "pas_ecart": t[Ecart.PAS_ECART],
                "ok_windows": ok_windows[f],
                "staleness_evaluable_windows": stale_evaluable[f],
                "staleness_fail_open": fail_open,
                "axes_evaluables": axes,
            }

        p0, p1, p_more = poisson_binomial(phats)
        gate = gate_value(n, p_more)
        insufficient = gate < seuil_hist
        z = None if insufficient else z_score(n, k_count, p_more)
        # Sous la garde (§5.4) : au lieu d'un z vide de sens, la QUEUE BINOMIALE
        # EXACTE P(K ≥ K_obs | Bin(n, P̂_more)). Dégénérés P̂_more ∈ {0,1} ou n=0 :
        # queue triviale (0/1), sans pouvoir de test → « historique insuffisant » nu.
        queue = None
        queue_note = None
        queue_applicable = False
        if insufficient:
            with localcontext(contexte_decimal()):
                degenere = (n == 0) or (p_more == Decimal(0)) or (p_more == Decimal(1))
            if degenere:
                queue_note = ("dégénérée : P̂_more ∈ {0,1} ou n=0 — queue triviale, "
                              "sans pouvoir de test ; « historique insuffisant » nu (10 §5.4)")
            else:
                queue = binomial_tail_ge(k_count, n, p_more)
                queue_note = "P(K ≥ K_obs | Bin(n, P̂_more)) — loi de K, 10 §5.1/§5.4"
                queue_applicable = True
        strates_out[st] = {
            "n": n,
            "K": k_count,
            "per_source": per_source,
            "P0": p0,
            "P1": p1,
            "P_more": p_more,
            "gate_value": gate,
            "seuil_historique": seuil_hist,
            "n_min_hors_enveloppe": n_min,
            "residu_staleness_fail_open": residu_fail_open,
            "flag_historique_insuffisant": insufficient,
            "z": z,
            "seuil_z": SEUIL_Z,
            # Queue exacte sous la garde (§5.4) — recalculable, publiée au bloc R1.
            "queue_exacte_applicable": queue_applicable,
            "queue_binomiale_P_K_ge_Kobs": queue,
            "queue_note": queue_note,
            "A_window_stationarity": A_WINDOW_STATIONARITY,
            "bloc": bloc_strate(serie, w, p_more, gate),   # ℓ = ELL_BLOC (ADR-0028 §1 bis.1 pt 3)
            "decomposition_K": dk,               # panne_transport : ≥ 2, 1, 0 sur K ; c_s (annexe D.5)
        }

    return {"pool": pool, "strates": strates_out, "poolee": strate_poolee(strates_out),   # clé à part
            "tau_observe": _tau_observe(ratios, tau), "A_window_stationarity": A_WINDOW_STATIONARITY}


def regle_critere(r1_out: dict) -> dict:
    """Règle SHOGEN-CRITERE-R1-1, forme scellée sans repli. Texte normatif : le paquet de pré-enregistrement scellé,
    docs/adr-0028/PAQUET-PREREG-S2.md §10.2, pts 1-11 (recopie d'ADR-0028 §1 bis.1), non recopié ici (une seule
    vérité). Lit r1_out["strates"] seul : la strate poolée n'y est jamais (pt 9). Compare les Decimal publiées par
    compute_r1 (z, bloc.z_bloc), sans arrondi ni contexte posé, à SEUIL_Z par « ≥ » ; aucune p-valeur (pt 4).
    Par strate (pt 5) : valeur, cas (garde_5_4, z_sous_seuil, rejette, discordance, rejet_non_qualifiable)
    et, pour toute strate qui NE REJETTE PAS, EMD = (SEUIL_Z + Z_PUISSANCE)·√max(n·P̂(1 − P̂), σ̂²_bloc)
    fenêtres et sa fraction de n (pt 8). Rend « R1 discrimine », les strates qui rejettent, les strates
    testées et m (pt 6)."""
    par = {}
    for st, b in r1_out.get("strates", {}).items():
        z, zb = b["z"], b["bloc"]["z_bloc"]
        cas = ("garde_5_4" if z is None else "z_sous_seuil" if z < SEUIL_Z else
               "rejet_non_qualifiable" if zb is None else "rejette" if zb >= SEUIL_Z else "discordance")
        v = ("NON ÉVALUABLE" if cas in ("garde_5_4", "rejet_non_qualifiable") else
             "REJETTE" if cas == "rejette" else "NE REJETTE PAS")
        emd = frac = None
        if v == "NE REJETTE PAS":
            with localcontext(contexte_decimal()):
                emd = +((SEUIL_Z + Z_PUISSANCE) * max(b["gate_value"], b["bloc"]["sigma2_bloc"]).sqrt())
                frac = +(emd / Decimal(b["n"]))
        par[st] = {"valeur": v, "cas": cas, "emd": emd, "emd_fraction": frac}
    rej = [s for s, e in par.items() if e["valeur"] == "REJETTE"]
    tst = [s for s, e in par.items() if e["valeur"] != "NON ÉVALUABLE"]
    nq = [s for s, e in par.items() if e["cas"] == "rejet_non_qualifiable"]
    return {"strates": par, "rejette": rej, "testees": tst, "m": len(tst), "non_qualifiables": nq,
            "r1_discrimine": "VRAI" if rej else "FAUX" if tst and not nq else "NON ÉVALUABLE"}


def fenetres_sautees(ws_journal, spec: dict, w: int, borne=None, ranges=()) -> dict:
    """Fenêtres sautées par strate, toutes causes confondues (ADR-0028 annexe D.5, SHOGEN-CENSURE-INFO-1) :
    window_start de la grille de pas w (multiples de w) sur borne = [t0 ; t_fin) (segment ; None : [premier ;
    dernier + w) de `ws_journal`), strate par `spec` (strate_calendar), sans marqueur window_close
    (`ws_journal`, garde §5.3 passée), hors des plages D5 fermées sur window_start (une fenêtre exclue n'est
    pas sautée). Compte par jour UTC, en O(jours + marqueurs) : grille, moins l'union des plages, moins les
    marqueurs retenus ; la strate ne dépend que du jour (kinds single et weekend_utc). Marqueur hors grille ou
    autre kind : ValueError. Rend {strate : s}, strates sans fenêtre sautée absentes."""
    ws_journal, out, union = set(ws_journal), {}, []
    if any(x % w for x in ws_journal) or spec.get("kind") not in ("single", "weekend_utc"):
        raise ValueError(f"fenêtres sautées : window_start hors de la grille de pas w = {w}, ou calendrier "
                         f"{spec.get('kind')!r} non journalier — fail-closed")
    if borne is None and not ws_journal:
        return {}
    t0, t_fin = (math.ceil(x) for x in borne or (min(ws_journal), max(ws_journal) + w))

    def grille(lo, hi, signe):                   # débuts de fenêtre dans [lo ; hi), par jour UTC
        for d in range(lo // 86400, -(-hi // 86400)):
            st, a, b = strate_from_spec(d * 86400, spec), max(lo, d * 86400), min(hi, d * 86400 + 86400)
            out[st] = out.get(st, 0) + signe * max(0, -(-b // w) + (-a // w))     # ⌈b/w⌉ − ⌈a/w⌉
    grille(t0, t_fin, 1)
    for a, b in sorted(ranges):                    # union des plages fermées, retirée une seule fois
        if union and a <= union[-1][1]:
            union[-1][1] = max(union[-1][1], b)
        else:
            union.append([a, b])
    for a, b in union:
        grille(max(a, t0), min(b + 1, t_fin), -1)
    for x in ws_journal:
        if t0 <= x < t_fin and not any(a <= x <= b for a, b in union):
            out[strate_from_spec(x, spec)] -= 1
    return {st: s for st, s in out.items() if s}


def fenetres_sautees_vivant(ws_journal, demarrages, spec: dict, w: int, borne=None, ranges=()) -> dict:
    """Part « harnais vivant » des fenêtres sautées (SHOGEN-CENSURE-CAUSES-1, option (a), ADR-0028 annexe B.23) : les
    fenêtres comptées par `fenetres_sautees` (mêmes marqueurs, portée et plages) qui tombent entre deux marqueurs d'un
    même démarrage (`demarrages` : records.demarrages), c'est-à-dire dans l'union des intervalles [premier marqueur ;
    dernier marqueur] des démarrages (bornes marquées, jamais sautées ; chevauchements comptés une fois) ; aucun seuil
    de temps. Le reste de s : arrêt ou passage entre démarrages, cause non attribuée par le journal. Rend {strate :
    nombre}, strates sans fenêtre vivante absentes."""
    ws = sorted(set(ws_journal))
    if borne is None and not ws:
        return {}
    t0, t_fin = borne or (ws[0], ws[-1] + w)
    union, out = [], {}
    for a, b in sorted((min(g), max(g)) for g in demarrages if g):
        if union and a <= union[-1][1]:
            union[-1][1] = max(union[-1][1], b)
        else:
            union.append([a, b])
    for a, b in union:                    # marqueurs de la portée seuls : coût linéaire en jours, portées, marqueurs
        lo, hi = max(a, t0), min(b, t_fin)
        for st, k in (fenetres_sautees(ws[bisect_left(ws, lo):bisect_left(ws, hi)], spec, w, (lo, hi), ranges).items()
                      if lo < hi else ()):
            out[st] = out.get(st, 0) + k
    return out


def bornes_censure(n: int, k: int, p_more: Decimal, s: int, sigma2_bloc: Optional[Decimal] = None) -> dict:
    """Bornes à P̂_more fixé (ADR-0028 annexe D.5, SHOGEN-CENSURE-INFO-1 ; A-6), s fenêtres sautées imputées
    sans co-écart (bas) puis avec (haut) : z_bas = z_score(n + s, K, P̂), z_haut = z_score(n + s, K + s, P̂),
    la fonction de z_s (s = 0 : z_s) ; si sigma2_bloc est donné, (K [+ s] − (n + s)·P̂)/σ̂_bloc, l'expression
    de bloc_strate (s = 0 : z_bloc). Non extérieures (CV2-24). À n'appeler que si z_s est publiée (§5.4)."""
    with localcontext(contexte_decimal()):
        zb = [None, None] if sigma2_bloc is None else [
            +((Decimal(x) - Decimal(n + s) * p_more) / sigma2_bloc.sqrt()) for x in (k, k + s)]
    return {"s": s, "z_bas": z_score(n + s, k, p_more), "z_haut": z_score(n + s, k + s, p_more),
            "z_bloc_bas": zb[0], "z_bloc_haut": zb[1]}


def recompute_from_journal(control_path: str, journal_path: str, exclude_ranges=(),
                           segment=None) -> dict:
    """Point d'entrée « recalculable depuis le journal seul » (ADR-0003) :
    lit les paramètres de `run_params` et les lectures, calcule R1. C'est ce que
    rejoue l'oracle de recalcul (worker à contexte frais, plan §5)."""
    params_list, _clock, markers = records.parse_control(control_path)
    # Concordance des run_params successifs vérifiée (fail-closed, §E) : un
    # redémarrage avec des seuils différents ne reclasse pas l'historique en
    # silence.
    params = records.effective_run_params(params_list)
    # Strates journalées == calendrier committé ex ante (fail-closed, §5.3) : une
    # étiquette de strate trafiquée (ou une spec incohérente) casse la partition
    # anti-complaisance — recalculée depuis run_params seul (ADR-0003). Clé porteuse
    # PRÉSENTE (garantie par effective_run_params), lue sans défaut silencieux.
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            "strates journalées incohérentes avec le calendrier committé "
            f"(fail-closed, §5.3) : {div[:5]}{' …' if len(div) > 5 else ''}"
        )
    # Filtre de lecture unique (ADR-0025 amendée par ADR-0028 D5) APRÈS la garde §5.3 ; journal intact.
    markers, _clock, _asn, _seg = records.filtre_lecture(params, markers, ranges=exclude_ranges,
                                                         segment=segment)
    readings = parse_journal(journal_path)
    pools, pool, _retraits = analysis_pools(markers, readings, list(params["pool"]))  # ADR-0028 D1
    # σ PAR CLASSE + τ RELATIF depuis run_params (ADR-0021 ; effective_run_params a
    # déjà garanti que sigma_classe est un mapping, fail-closed sur scalaire legacy).
    sigma_by_class, sigma_class_of_flux, tau = records.sigma_tau_from_params(params)
    return compute_r1(
        markers=markers,
        readings=readings,
        pool=pool,
        pool_by_strate=pools,
        w=int(params["w"]),
        sigma_by_class=sigma_by_class,
        sigma_class_of_flux=sigma_class_of_flux,
        tau=tau,
        seuil_hist=Decimal(str(params["seuil_historique_valeur"])),
        n_min=int(params["n_min_hors_enveloppe"]),
    )


def recompute_d5_from_journal(control_path: str, journal_path: str, exclude_ranges=(), segment=None) -> dict:
    """Fonction sœur de `recompute_from_journal` pour le lecteur tiers (SHOGEN-D5-RECALCUL-TIERS-1 ; ADR-0028 annexe
    D.5) : garde §5.3 et filtre de lecture (`records.filtre_lecture`) par `recompute_from_journal`, puis, comme le
    rendu, s par strate (`fenetres_sautees` sur les marqueurs du journal entier, portée du segment, plages D5 ; bloc 1)
    et bornes de censure par strate de R1 (bloc 3) : None sous la garde §5.4 (z_s non publiée), variante σ̂_bloc si
    z_bloc est publiée ; part « harnais vivant » de s, comme le bloc 1 (SHOGEN-CENSURE-CAUSES-TIERS-1). Rend
    {"fenetres_sautees": {strate : s}, "fenetres_sautees_vivant": {strate : part}, "bornes_censure": {strate : bornes
    ou None}} (strates à 0 absentes des deux premiers)."""
    out = recompute_from_journal(control_path, journal_path, exclude_ranges, segment)
    params_list, _clock, markers = records.parse_control(control_path)
    params, ranges = records.effective_run_params(params_list), records.exclusion_ranges(exclude_ranges)
    seg = records.filtre_lecture(params, markers, ranges=ranges, segment=segment)[3]
    ws, spec, w = build_window_strate(markers), params["strate_calendar"], int(params["w"])
    s = fenetres_sautees(ws, spec, w, seg, ranges)
    return {"fenetres_sautees": s, "fenetres_sautees_vivant": fenetres_sautees_vivant(
        ws, records.demarrages(control_path), spec, w, seg, ranges), "bornes_censure": {
        st: None if b["z"] is None else bornes_censure(b["n"], b["K"], b["P_more"], s.get(st, 0), b["bloc"][
            "sigma2_bloc"] if b["bloc"]["z_bloc"] is not None else None) for st, b in out["strates"].items()}}
