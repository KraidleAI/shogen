"""Sources du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lots SB-3 et SB-4 ; E-S-07 à E-S-16) : état vrai
par hôte sur la grille, en masques entiers (bit j = fenêtre T_début + j·w, comme calendrier.py). SB-3a : lois de durée
(empirique, géométrique) et leur loi résiduelle, renouvellement alterné stationnaire, chaîne à deux états (T-GEN-1),
masques. SB-3b : flux des composants pré-déclarés (E-S-41, Q-4) ; taux exacts par hôte et par strate (cellules/n_s,
Q-3 ; E-S-09) ; loi des longueurs « tous épisodes » d'EP (Q-2), regroupée en stress (E-S-10) ; taux exacts des
composantes (pannes longues, E-S-11 ; régime caché, E-S-12), de taux marginal conservé. SB-3c : indices des flux,
réplication (fond de la cellule, masques de strate), régime par hôte et par strate, union des composantes, pannes d'hôte
H(u) vues dans les fenêtres de chaque strate (E-S-08). Chaque tirage compare random() à un seuil exact (aleas.seuil,
E-S-43) ; aucun autre flottant, aucune fonction transcendante, aucune puissance."""
import functools
from fractions import Fraction

import aleas
import commun


def flux(prm: dict, cellule: str, i: int, composant: str, indice: int):
    """aleas.flux d'un composant pré-déclaré dans sources.composants de parametres.json (Q-4), sinon
    SOURCES/composant."""
    if composant not in prm["sources"]["composants"]:
        raise commun.Refus("SOURCES/composant", f"{composant!r} : non déclaré dans parametres.json")
    return aleas.flux(prm["aleas"], cellule, i, composant, indice)


@functools.lru_cache(maxsize=None, typed=True)
def _table_geometrique(q: Fraction, rangs: int, garde: int):
    return aleas.Geometrique(q, rangs, garde)       # ≈ 70 ms par table : une seule par paramètre (I-4)


@functools.lru_cache(maxsize=None, typed=True)
def _table_empirique(hist: tuple):
    return aleas.Empirique(list(hist))


class Empirique:
    """Loi de durée empirique d'un histogramme ((longueur, nombre), …), longueurs entières ≥ 1 (sinon SOURCES/loi),
    nombres entiers > 0 (sinon ALEAS/empirique) ; moyenne exacte."""

    def __init__(self, hist):
        self.hist = tuple(tuple(x) for x in hist)
        if any(type(lg) is not int or lg < 1 for lg, _n in self.hist):
            raise commun.Refus("SOURCES/loi", f"{self.hist!r} : longueurs entières ≥ 1 attendues")
        self.table = _table_empirique(self.hist)
        self.moyenne = Fraction(sum(lg * n for lg, n in self.hist), sum(n for _lg, n in self.hist))

    def tirer(self, u, borne: int):
        """Durée si ≤ borne, None sinon ; un appel de u()."""
        v = self.table.tirer(u)
        return v if v <= borne else None

    def residu(self):
        """Durée restante, instant compris, d'une période en cours à un instant fixé d'un régime stationnaire :
        P(R = k) = P(L ≥ k)/E[L], soit les poids entiers Σ_{l ≥ k} n_l, k = 1..max."""
        return _residu(self.hist)


@functools.lru_cache(maxsize=None)
def _residu(hist: tuple) -> Empirique:
    return Empirique([(k, sum(n for lg, n in hist if lg >= k)) for k in range(1, max(lg for lg, _n in hist) + 1)])


class Geometrique:
    """Loi géométrique sur {1, 2, …} de paramètre q rationnel de ]0, 1], moyenne 1/q (table d'aleas, rangs et garde de
    parametres.json) ; sans mémoire, elle est sa propre loi résiduelle."""

    def __init__(self, q: Fraction, a: dict):
        self.table, self.moyenne = _table_geometrique(q, a["rangs"], a["garde"]), 1 / q

    def tirer(self, u, borne: int):
        return self.table.tirer(u, borne)

    def residu(self):
        return self


def stationnaire(moyenne: Fraction, q: Fraction) -> Fraction:
    """Part stationnaire du temps en cours d'un renouvellement alterné de pauses géométriques de paramètre q :
    μ/(μ + 1/q) = μq/(μq + 1) ; pour la chaîne à deux états (μ = 1/(1 − a), q = b) : b/(1 − a + b)."""
    m = Fraction(moyenne) * q
    return m / (m + 1)


def pause(r: Fraction, moyenne: Fraction) -> Fraction:
    """Paramètre q des pauses qui donne la part stationnaire r : q = r/(μ(1 − r)) ; SOURCES/taux si r n'est pas un
    rationnel de [0, 1[ ou si r > μ/(μ + 1) (q > 1 : une pause d'au moins une fenêtre suit chaque période)."""
    if not (type(r) is Fraction and 0 <= r < 1) or r * (moyenne + 1) > moyenne:
        raise commun.Refus("SOURCES/taux", f"r = {r!r}, moyenne {moyenne} : part de [0, μ/(μ + 1)] attendue")
    return r / (moyenne * (1 - r))


def alterner(u, loi, q: Fraction, a: dict, horizon: int) -> list:
    """Segments [(début, fin)] sur [0, horizon) d'un renouvellement alterné stationnaire : périodes de loi `loi`,
    chacune suivie d'une pause géométrique de paramètre q ; à l'instant 0, en cours avec la part stationnaire, pour une
    durée restante de loi loi.residu(), sinon en pause (reste géométrique, sans mémoire). q = 0 : aucun segment. Ordre
    des tirages : départ, reste, puis pause, durée, pause, durée…"""
    if q == 0 or horizon < 1:
        return []
    pauses, segs, t = Geometrique(q, a), [], 0
    if aleas.bernoulli(u, aleas.seuil(stationnaire(loi.moyenne, q))):
        d = loi.residu().tirer(u, horizon)
        t = horizon if d is None else d
        segs.append((0, t))
    while t < horizon:
        g = pauses.tirer(u, horizon - 1 - t)
        if g is None:
            break
        d = loi.tirer(u, horizon - t - g)
        segs.append((t + g, horizon if d is None else t + g + d))
        t = segs[-1][1]
    return segs


def markov(u, a_: Fraction, b: Fraction, a: dict, horizon: int) -> list:
    """Chaîne à deux états (1 = en cours) : P(1 → 1) = a_, P(0 → 1) = b ; durées en cours géométriques de paramètre
    1 − a_, pauses géométriques de paramètre b, départ stationnaire b/(1 − a_ + b) (T-GEN-1)."""
    return alterner(u, Geometrique(1 - a_, a), b, a, horizon)


def masque(segs: list) -> int:
    """Entier dont le bit j vaut 1 si la fenêtre j est dans l'un des segments (disjoints, dans l'ordre)."""
    morceaux, t = [], 0
    for d, f in segs:
        morceaux += ["0" * (d - t), "1" * (f - d)]
        t = f
    return int("".join(morceaux)[::-1] or "0", 2)


def taux(ep: dict, strate: str, hote: str) -> tuple:
    """(p_panne, p_ecart_propre) exacts de l'hôte dans la strate (E-S-09 ; Q-3) : cellules/n_s de la ligne « panne »
    d'EP, puis (cellules d'écart − cellules de panne)/n_s ; SOURCES/taux si les n_s diffèrent ou si l'écart compte moins
    de cellules que la panne (l'écart d'EP comprend la panne)."""
    p, e = ep[strate, hote, "panne"], ep[strate, hote, "ecart"]
    if p["n_s"] != e["n_s"] or e["cellules"] < p["cellules"]:
        raise commun.Refus("SOURCES/taux", f"« {strate} » {hote} : panne {p['cellules']}/{p['n_s']}, écart "
                                           f"{e['cellules']}/{e['n_s']}")
    return Fraction(p["cellules"], p["n_s"]), Fraction(e["cellules"] - p["cellules"], p["n_s"])


def loi_longueurs(prm: dict, ep: dict, strate: str, hote: str, type_: str) -> Empirique:
    """Loi « tous épisodes » d'EP (adjudication Q-2 : censurés compris, à leur longueur vue, qui minore la vraie) de
    l'hôte dans la strate, pour le type « panne » ou « ecart » ; dans une strate de sources.regroupees, histogrammes
    sommés sur les hôtes du pool (E-S-10)."""
    hotes = [h for h, _f in prm["calibration"]["unites"]] if strate in prm["sources"]["regroupees"] else [hote]
    c = {}
    for h in hotes:
        for lg, n in ep[strate, h, type_]["histogramme"]:
            c[lg] = c.get(lg, 0) + n
    return Empirique(sorted(c.items()))


def composantes(p: Fraction, part: Fraction, regime) -> dict:
    """Taux des composantes indépendantes et stationnaires d'une série de taux marginal p : pannes longues L,
    r_L = part·p (E-S-11) ; reste A = E ∪ (E′ ∩ Z), p_A = (p − r_L)/(1 − r_L), d'où P(A ∪ L) = p ; régime caché Z de
    part φ et de rapport de taux κ (E-S-12 ; None : C0, sans régime) : r_E = p_A/(1 − φ + φκ) en régime normal,
    r_E + (1 − r_E)r' = κ·r_E en régime dégradé, d'où r' = r_E(κ − 1)/(1 − r_E) et P(A) = p_A exactement."""
    r_l = part * p
    p_a = (p - r_l) / (1 - r_l)
    if regime is None:
        return {"longues": r_l, "base": p_a, "regime": 0 * p}
    phi, kappa, _tau = regime
    r_e = p_a / (1 - phi + phi * kappa)
    return {"longues": r_l, "base": r_e, "regime": r_e * (kappa - 1) / (1 - r_e)}


def indice(prm: dict, hote: str, strate: str, k: int = 0) -> int:
    """Indice de flux (E-S-41) d'une série : (h·S + s)·10 + k, h rang de l'hôte dans calibration.unites (pool BTC
    D1-bis), s rang de la strate, k emplacement de 0 à 9 (0 : l'hôte ; 1 + c : classe c), sinon SOURCES/indice."""
    hotes, strates = [h for h, _f in prm["calibration"]["unites"]], prm["calibration"]["strates"]
    if hote not in hotes or strate not in strates or type(k) is not int or not 0 <= k < 10:
        raise commun.Refus("SOURCES/indice", f"{hote!r}, {strate!r}, {k!r}")
    return (hotes.index(hote) * len(strates) + strates.index(strate)) * 10 + k


def loi_longues(prm: dict) -> Empirique:
    """Durées des pannes longues de sources.longues (E-S-11 : 1 h, 1 jour, 3 jours), également probables."""
    return Empirique([(d, 1) for d in prm["sources"]["longues"]])


class Replication:
    """Une réplication d'une cellule : paramètres, EP (calibration.charger(…)["episodes"]), fond (f ; régime par strate,
    (φ, κ, τ_D) ou None ; part des pannes longues), nom de cellule et indice i ≥ 0 (Q-4), masques de strate
    (calendrier.masques) et horizon T_max en fenêtres ; chaque série tire sur ses propres flux (composant, indice)."""

    def __init__(self, prm, ep, fond, cellule, i, masques, horizon):
        self.prm, self.ep, self.fond, self.cellule, self.i = prm, ep, fond, cellule, i
        self.masques, self.horizon, self._z = masques, horizon, {}

    def u(self, composant, hote, strate, k=0):
        return flux(self.prm, self.cellule, self.i, composant, indice(self.prm, hote, strate, k))

    def regime(self, hote, strate) -> int:
        """Z(hôte, strate) (E-S-12), commun aux séries de l'hôte dans la strate : chaîne à deux états de durée moyenne
        τ_D en régime dégradé et de part φ (a = 1 − 1/τ_D, b = φ/(τ_D(1 − φ))) ; 0 sous C0."""
        if (hote, strate) not in self._z:
            reg = self.fond["regime"][strate]
            if reg is not None and not (0 <= reg[0] < 1 <= reg[1] and type(reg[2]) is int and reg[2] >= 1):
                raise commun.Refus("SOURCES/regime", f"{reg!r} : φ de [0, 1[, κ ≥ 1, τ_D entier ≥ 1")
            self._z[hote, strate] = 0 if reg is None else masque(markov(
                self.u("regime", hote, strate), 1 - Fraction(1, reg[2]), reg[0] / (reg[2] * (1 - reg[0])),
                self.prm["aleas"], self.horizon))
        return self._z[hote, strate]

    def union(self, hote, strate, k, p, loi, noms) -> int:
        """Masque sur la grille de E ∪ (E′ ∩ Z) ∪ L, série de taux marginal p (composantes), de loi `loi` pour E, de
        flux noms = (E, E′, L) ; L (loi_longues, part du fond) seulement si noms[2]. E′ est tirée fenêtre à fenêtre,
        indépendamment, de part r' (convention L = 1 de S2, G0 SIM-NIVEAU l.54) : en régime dégradé, la part κ·r_E peut
        dépasser μ/(μ + 1), borne d'un renouvellement à pauses d'au moins une fenêtre (points de la grille E1 à f = 1) ;
        r' ≥ 1 : SOURCES/taux."""
        c = composantes(p, self.fond["longues"] if noms[2] else 0 * p, self.fond["regime"][strate])
        lois, m = (loi, None, loi_longues(self.prm)), 0
        for j, cle in enumerate(("base", "regime", "longues")):
            if c[cle] and cle == "regime":
                if c[cle] >= 1:
                    raise commun.Refus("SOURCES/taux", f"r' = {c[cle]} : part de [0, 1[ attendue (régime {strate})")
                s = masque(markov(self.u(noms[j], hote, strate, k), c[cle], c[cle], self.prm["aleas"], self.horizon))
                m |= s & self.regime(hote, strate)
            elif c[cle]:
                m |= masque(alterner(self.u(noms[j], hote, strate, k), lois[j], pause(c[cle], lois[j].moyenne),
                                     self.prm["aleas"], self.horizon))
        return m

    def pannes(self, hote) -> int:
        """H(hôte) (E-S-08) : dans chaque strate, union de taux f·p_panne(hôte, strate) (EP, Q-3), de loi « panne »
        (loi_longueurs) et de part longue du fond, vue dans les fenêtres de la strate (masque de calendrier)."""
        h = 0
        for s in self.prm["calibration"]["strates"]:
            p, loi = self.fond["f"] * taux(self.ep, s, hote)[0], loi_longueurs(self.prm, self.ep, s, hote, "panne")
            h |= self.masques[s] & self.union(hote, s, 0, p, loi, ("panne", "panne-regime", "longues"))
        return h
