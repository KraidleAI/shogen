"""Sources du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lots SB-3 et SB-4 ; E-S-07 à E-S-16) : état vrai
par hôte sur la grille, en masques entiers (bit j = fenêtre T_début + j·w, comme calendrier.py). SB-3a : lois de durée
(empirique, géométrique) et leur loi résiduelle, renouvellement alterné stationnaire, chaîne à deux états (T-GEN-1),
masques. SB-3b : flux des composants pré-déclarés (E-S-41, Q-4) ; taux exacts par hôte et par strate (cellules/n_s,
Q-3 ; E-S-09) ; loi des longueurs « tous épisodes » d'EP (Q-2), regroupée en stress (E-S-10) ; taux exacts des
composantes (pannes longues, E-S-11 ; régime caché, E-S-12), de taux marginal conservé. SB-3c : indices des flux,
réplication (fond de la cellule, masques de strate), régime par hôte et par strate, union des composantes, pannes d'hôte
H(u) vues dans les fenêtres de chaque strate (E-S-08). SB-3d : dérives (E-S-13), par amincissement des épisodes d'une
série tirée au taux maximal, et panne initiale hors équilibre. SB-4a : classes jointes par hôte (E-S-07, E-S-08) : pools
par classe, écarts propres F(u, c) par classe (E-S-09, composante hors-enveloppe de Q-S-21), état vrai typé. SB-4b :
incidents communs (E-S-15 ; cible, grille, ETH : pannes de transport de l'hôte), unités faibles markoviennes, paires,
triplets et co-défaillances qui impliquent une unité faible (E-S-16). Chaque tirage compare random() à un seuil exact
(aleas.seuil, E-S-43) ; aucun autre flottant, aucune fonction transcendante, aucune puissance."""
import functools
from fractions import Fraction

import aleas
import calendrier
import commun

GENRES = ("commune", "tendances", "sauts", "transitoire", "initiale")
CLASSES = ("BTC", "ETH", "USDC", "USDT")


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
    sommés sur les hôtes de la liste scellée sources.indices_hotes (E-S-10 ; O-1 de la G2 de la tranche 3 : ancrée
    sur la liste de calibration, non sur le pool opérationnel, un retrait ne change l'état en stress d'aucun autre
    hôte). Hôte sans ligne d'EP : SOURCES/loi."""
    hotes = prm["sources"]["indices_hotes"] if strate in prm["sources"]["regroupees"] else [hote]
    if any((strate, h, type_) not in ep for h in hotes):
        raise commun.Refus("SOURCES/loi", f"« {strate} » {type_} : {hotes!r}, hôte sans ligne d'EP")
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


def rang(prm: dict, hote: str) -> int:
    """h des flux d'un hôte : son rang dans sources.indices_hotes, liste scellée et immuable des 10 hôtes D1-bis dans
    l'ordre de l'ADR-0029 l.168, distincte des listes opérationnelles (C-6 de la G2 de la tranche 2, avis Q-T2-11) :
    réordonner ou réduire un pool ne change le flux d'aucun autre hôte, un hôte retiré laisse son rang inemployé. Hôte
    absent de la liste, ou liste à doublon : SOURCES/indice."""
    liste = prm["sources"]["indices_hotes"]
    if hote not in liste or len(set(liste)) != len(liste):
        raise commun.Refus("SOURCES/indice", f"{hote!r} : hôte absent de sources.indices_hotes, ou liste à doublon")
    return liste.index(hote)


def indice(prm: dict, hote: str, strate: str, k: int = 0) -> int:
    """Indice de flux (E-S-41) d'une série : (h·S + s)·10 + k, h = rang(prm, hote), s rang de la strate, k emplacement
    de 0 à 9 (0 : l'hôte ; 1 + c : classe c), sinon SOURCES/indice."""
    strates = prm["calibration"]["strates"]
    if strate not in strates or type(k) is not int or not 0 <= k < 10:
        raise commun.Refus("SOURCES/indice", f"{hote!r}, {strate!r}, {k!r}")
    return (rang(prm, hote) * len(strates) + strates.index(strate)) * 10 + k


def loi_longues(prm: dict) -> Empirique:
    """Durées des pannes longues de sources.longues (E-S-11 : 1 h, 1 jour, 3 jours), de poids sources.poids_longues en
    nombre d'épisodes (1:1:1, avis Q-T2-5 adopté ; C-7 de la G2 de la tranche 2) ; autant de poids que de durées, sinon
    SOURCES/loi."""
    durees, poids = prm["sources"]["longues"], prm["sources"]["poids_longues"]
    if len(durees) != len(poids):
        raise commun.Refus("SOURCES/loi", f"{durees!r}, poids {poids!r} : autant de poids que de durées")
    return Empirique(list(zip(durees, poids)))


def regime_valide(reg):
    """Régime d'une strate (E-S-12) : None (C0) ou (φ, κ, τ_D), φ de [0, 1[, κ ≥ 1, τ_D entier ≥ 1, sinon
    SOURCES/regime ; contrôlé avant tout usage, par regime() et par union() (C-2 de la G2 de la tranche 2)."""
    if reg is not None and not (0 <= reg[0] < 1 <= reg[1] and type(reg[2]) is int and reg[2] >= 1):
        raise commun.Refus("SOURCES/regime", f"{reg!r} : φ de [0, 1[, κ ≥ 1, τ_D entier ≥ 1")
    return reg


class Replication:
    """Une réplication d'une cellule : paramètres, EP (calibration.charger(…)["episodes"]), fond (f ; régime par strate,
    (φ, κ, τ_D) ou None ; part des pannes longues ; derive, None ou {genres, duree} ; autres, multiplicateur d'écart
    hors de BTC ; hors_enveloppe, τ ; incidents et faibles, None ou leur spécification), nom de cellule et indice i ≥ 0
    (Q-4), masques de strate (calendrier.masques) et horizon T_max en fenêtres ; chaque série tire sur ses propres flux
    (composant, indice)."""

    def __init__(self, prm, ep, fond, cellule, i, masques, horizon):
        self.prm, self.ep, self.fond, self.cellule, self.i = prm, ep, fond, cellule, i
        self.masques, self.horizon, self._z, self._d = masques, horizon, {}, None

    def u(self, composant, hote, strate, k=0):
        return flux(self.prm, self.cellule, self.i, composant, indice(self.prm, hote, strate, k))

    def derives(self) -> dict:
        """Dérives de la réplication (derives, flux « derive » d'indice 0), tirées une fois."""
        if self._d is None:
            self._d = derives(self.prm, self.fond.get("derive"), flux(self.prm, self.cellule, self.i, "derive", 0))
        return self._d

    def regime(self, hote, strate) -> int:
        """Z(hôte, strate) (E-S-12), commun aux séries de l'hôte dans la strate : chaîne à deux états de durée moyenne
        τ_D en régime dégradé et de part φ (a = 1 − 1/τ_D, b = φ/(τ_D(1 − φ))) ; 0 sous C0 ; regime_valide."""
        if (hote, strate) not in self._z:
            reg = regime_valide(self.fond["regime"][strate])
            self._z[hote, strate] = 0 if reg is None else masque(markov(
                self.u("regime", hote, strate), 1 - Fraction(1, reg[2]), reg[0] / (reg[2] * (1 - reg[0])),
                self.prm["aleas"], self.horizon))
        return self._z[hote, strate]

    def union(self, hote, strate, k, p, loi, noms) -> int:
        """Masque sur la grille de E ∪ (E′ ∩ Z) ∪ L, série de taux marginal p (composantes), de loi `loi` pour E, de
        flux noms = (E, E′, L) ; L (loi_longues, part du fond) seulement si noms[2]. E′ est tirée fenêtre à fenêtre,
        indépendamment, de part r' (convention L = 1 de S2, G0 SIM-NIVEAU l.54) : en régime dégradé, la part κ·r_E peut
        dépasser μ/(μ + 1), borne d'un renouvellement à pauses d'au moins une fenêtre (points de la grille E1 à f = 1) ;
        r' ≥ 1 : SOURCES/taux ; régime contrôlé d'abord (regime_valide). Sous une dérive de l'hôte de maximum M : union
        tirée au taux M·p, puis amincie (flux « derive-episodes »)."""
        reg = regime_valide(self.fond["regime"][strate])
        d = self.derives()["specs"].get(hote)
        grand = max(d[1], d[2]) if d else 1
        c = composantes(grand * p, self.fond["longues"] if noms[2] else 0 * p, reg)
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
        if d:
            m = masque(amincir(self.u("derive-episodes", hote, strate, k), calendrier.segments(m), d))
        return m

    def pannes(self, hote, k=0) -> int:
        """H(hôte) (E-S-08) : dans chaque strate, union de taux f·p_panne(hôte, strate) (EP, Q-3), de loi « panne »
        (loi_longueurs) et de part longue du fond, vue dans les fenêtres de la strate (masque de calendrier) ; flux
        d'emplacement k = 0, celui de l'hôte."""
        h = 0
        for s in self.prm["calibration"]["strates"]:
            p, loi = self.fond["f"] * taux(self.ep, s, hote)[0], loi_longueurs(self.prm, self.ep, s, hote, "panne")
            h |= self.masques[s] & self.union(hote, s, k, p, loi, ("panne", "panne-regime", "longues"))
        if hote == self.derives()["initiale"]:
            h |= (1 << min(self.prm["sources"]["derive"]["initiale"], self.horizon)) - 1
        return h

    def ecarts(self, hote, c) -> int:
        """F(hôte, classe de rang c) (E-S-08, E-S-09) : dans chaque strate, union de taux f·p_écart_propre(hôte,
        strate), × fond["autres"] hors de BTC (F des autres classes = F de BTC du même hôte, déclaré ; sensibilité × 2),
        de loi « ecart » et de régime Z partagé avec H ; plus la composante hors-enveloppe, épisodes d'une fenêtre de
        part τ = fond["hors_enveloppe"], non multipliée par f (Q-S-21, côté source) ; flux d'emplacement 1 + c ; vue
        dans les fenêtres de la strate."""
        f, une = 0, Empirique([(1, 1)])
        for s in self.prm["calibration"]["strates"]:
            p = self.fond["f"] * taux(self.ep, s, hote)[1] * (1 if c == 0 else self.fond["autres"])
            m = self.union(hote, s, 1 + c, p, loi_longueurs(self.prm, self.ep, s, hote, "ecart"),
                           ("ecart", "ecart-regime", None))
            m |= masque(alterner(self.u("hors-enveloppe", hote, s, 1 + c), une, pause(self.fond["hors_enveloppe"], 1),
                                 self.prm["aleas"], self.horizon))
            f |= self.masques[s] & m
        return f

    def etat(self, surcharges=None) -> dict:
        """État vrai (E-S-08) : {(hôte, classe) : (panne, écart)} pour chaque hôte du pool et chaque classe qu'il sert
        (classes) ; panne = H(hôte) | surcharges[hôte] | incidents du fond (E-S-15) | unités faibles de type « panne »
        (E-S-16), commune à toutes les classes de l'hôte ; écart = F(hôte, classe), plus l'unité faible de type
        « ecart » en BTC seulement (flux déviant), hors panne (deux types, Q-S-22). Type d'unité faible inconnu :
        SOURCES/faible."""
        sur, fa = dict(surcharges or {}), self.fond.get("faibles")
        if fa is not None and fa["type"] not in ("panne", "ecart"):
            raise commun.Refus("SOURCES/faible", f"type {fa['type']!r} : « panne » ou « ecart »")
        mf = faibles(self.prm, self.cellule, self.i, fa, self.horizon)
        ajouts = incidents(self.prm, self.cellule, self.i, self.fond.get("incidents"), self.horizon)
        for hote, m in list(ajouts.items()) + (list(mf.items()) if fa and fa["type"] == "panne" else []):
            sur[hote] = sur.get(hote, 0) | m
        out, cl = {}, classes(self.prm)
        for hote, _f in self.prm["calibration"]["unites"]:
            h, e0 = self.pannes(hote) | sur.get(hote, 0), mf.get(hote, 0) if fa and fa["type"] == "ecart" else 0
            for c, (classe, pool) in enumerate(cl):
                if hote in pool:
                    out[hote, classe] = (h, (self.ecarts(hote, c) | (e0 if c == 0 else 0)) & ~h)
        return out


@functools.lru_cache(maxsize=None)
def _uniforme(n: int):
    return aleas.Empirique([(j, 1) for j in range(n)])        # j uniforme sur 0..n − 1 (seuils exacts j/n)


def multiplicateur(d: tuple, t: int) -> Fraction:
    """m(t) d'une dérive (E-S-13) : ("lineaire", m0, m1, L) : m0 + (m1 − m0)·min(t, L)/L, tenu au-delà de L ; ("saut",
    m0, m1, x) : m0 avant x, m1 à partir de x."""
    genre, m0, m1, x = d
    if genre == "lineaire":
        return m0 + (m1 - m0) * Fraction(min(t, x), x)
    return m0 if t < x else m1


def amincir(u, segs: list, d: tuple) -> list:
    """Épisodes gardés chacun avec la probabilité m(début)/M, M = max(m0, m1) : une série tirée au taux M·p prend le
    taux local ≈ m(t)·p, le multiplicateur étant pris au début de chaque épisode (O-2 de la G2 de la tranche 2),
    longueurs inchangées (E-S-13)."""
    grand = max(d[1], d[2])
    return [(a, b) for a, b in segs if aleas.bernoulli(u, aleas.seuil(multiplicateur(d, a) / grand))]


def derives(prm: dict, derive, u) -> dict:
    """Dérives d'une réplication (E-S-13 ; derive : None ou {"genres", "duree" : durée nominale L en fenêtres}) :
    {"specs" : {hôte : multiplicateur}, "initiale" : hôte ou None}. Tirages sur u, ancrés sur les rangs de la liste
    scellée sources.indices_hotes (O-A du contre-contrôle de la tranche 2, comme C-6 pour les flux), dans l'ordre :
    commune (d : un sens pour tous) ; tendances (a : un sens par rang de la liste) ; sauts (b : unites_saut rangs sans
    remise, chacun suivi de son sens et de son instant, jour puis fenêtre du jour) ; transitoire (d : × facteur sur les
    premières fenêtres, sans tirage) ; initiale (c : un rang hors de l'unité non décalée, premier hôte du pool par ordre
    alphabétique, ADR-0029 l.200 ; en panne dès 0). Un tirage tombé hors du pool reste inemployé : réordonner ou
    réduire le pool ne change la dérive d'aucun autre hôte. Sens croissant si u < 1/2. Hôte du pool absent de la liste
    (ou liste à doublon) : SOURCES/indice ; SOURCES/derive : genre inconnu, plus d'un multiplicateur, ou sauts sur une
    durée non multiple d'un jour."""
    out, hotes = {"specs": {}, "initiale": None}, [h for h, _f in prm["calibration"]["unites"]]
    if derive is None:
        return out
    g, n, p, fpj = derive["genres"], derive["duree"], prm["sources"]["derive"], 86400 // prm["calendrier"]["w"]
    if any(x not in GENRES for x in g) or sum(x in g for x in GENRES[:4]) > 1 or ("sauts" in g and n % fpj):
        raise commun.Refus("SOURCES/derive", f"genres {g!r}, durée {n!r}")
    bas, haut, liste = Fraction(*p["bornes"][0]), Fraction(*p["bornes"][1]), prm["sources"]["indices_hotes"]
    for h in hotes:
        rang(prm, h)

    def sens():
        return (bas, haut) if aleas.bernoulli(u, aleas.seuil(Fraction(1, 2))) else (haut, bas)
    if "commune" in g:
        s = sens()
        out["specs"] = {h: ("lineaire", *s, n) for h in hotes}
    if "tendances" in g:
        tires = [("lineaire", *sens(), n) for _h in liste]
        out["specs"] = {h: d for h, d in zip(liste, tires) if h in hotes}
    reste = list(liste)
    for _j in range(p["unites_saut"] if "sauts" in g else 0):
        h = reste.pop(_uniforme(len(reste)).tirer(u))
        s = sens()
        d = ("saut", *s, fpj * _uniforme(n // fpj).tirer(u) + _uniforme(fpj).tirer(u))
        if h in hotes:
            out["specs"][h] = d
    if "transitoire" in g:
        out["specs"] = {h: ("saut", Fraction(p["transitoire"][0]), Fraction(1), p["transitoire"][1]) for h in hotes}
    if "initiale" in g:
        rangs = [h for h in liste if h != min(hotes)]
        h = rangs[_uniforme(len(rangs)).tirer(u)]
        out["initiale"] = h if h in hotes else None
    return out


def classes(prm: dict) -> list:
    """[(classe, hôtes)] dans l'ordre CLASSES (sources.classes, E-S-07) : BTC servi par les hôtes du pool D1-bis
    (calibration.unites), les autres classes par des hôtes pris parmi eux (ADR l.173) ; sinon SOURCES/classes."""
    hotes = [h for h, _f in prm["calibration"]["unites"]]
    out = [(c, prm["sources"]["classes"][c]) for c in CLASSES]
    if out[0][1] != hotes or any(h not in hotes for _c, pool in out for h in pool):
        raise commun.Refus("SOURCES/classes", f"{prm['sources']['classes']!r} : BTC = pool D1-bis, autres parmi lui")
    return out


def chaine(p: Fraction, L: int) -> tuple:
    """(a, b) de la chaîne d'une unité faible de part stationnaire p et d'épisodes de longueur moyenne L (convention de
    S2, G0 SIM-NIVEAU l.54) : L = 1, tirages indépendants, a = b = p ; sinon a = 1 − 1/L, b = p/(L(1 − p))."""
    return (p, p) if L == 1 else (1 - Fraction(1, L), p / (L * (1 - p)))


def faibles(prm: dict, cellule: str, i: int, spec, horizon: int) -> dict:
    """{hôte : masque} des unités faibles (E-S-16) ; spec : None ou {"hotes", "p" (p_w), "L" (L_w), "type"} ; chaîne de
    chaine(p_w, L_w), départ stationnaire, un flux « faibles » par unité (indice : rang(prm, hôte), C-6 de la G2 de la
    tranche 2). Hôte hors du pool : SOURCES/faible (C-3 de la même G2), comme touches() pour un incident."""
    if spec is None:
        return {}
    if any(h not in [x for x, _f in prm["calibration"]["unites"]] for h in spec["hotes"]):
        raise commun.Refus("SOURCES/faible", f"{spec['hotes']!r} : hôtes du pool attendus")
    a_, b = chaine(spec["p"], spec["L"])
    return {h: masque(markov(flux(prm, cellule, i, "faibles", rang(prm, h)), a_, b, prm["aleas"], horizon))
            for h in spec["hotes"]}


def touches(prm: dict, v, mode: tuple) -> list:
    """Hôtes d'un incident (Q-S-05) : ("chacun", hôtes, π) : chacun avec la probabilité π, un tirage par hôte dans
    l'ordre (cible : les 7 hôtes AS13335, π = 7/10 ; « les 10 » : π = 1) ; ("parmi", hôtes, k, imposés) : un hôte
    uniforme parmi les imposés s'il y en a (unité faible), puis des hôtes uniformes sans remise parmi les autres jusqu'à
    k (paire tirée par incident, triplet). Hôte hors du pool : SOURCES/incident."""
    tous = [h for h, _f in prm["calibration"]["unites"]]
    if any(h not in tous for h in list(mode[1]) + (list(mode[3]) if mode[0] == "parmi" else [])):
        raise commun.Refus("SOURCES/incident", f"{mode!r} : hôtes du pool attendus")
    if mode[0] == "chacun":
        s = aleas.seuil(mode[2])
        return [h for h in mode[1] if aleas.bernoulli(v, s)]
    out = [mode[3][_uniforme(len(mode[3])).tirer(v)]] if mode[3] else []
    reste = [h for h in mode[1] if h not in out]
    while len(out) < mode[2]:
        out.append(reste.pop(_uniforme(len(reste)).tirer(v)))
    return out


def incidents(prm: dict, cellule: str, i: int, spec, horizon: int, u=None, v=None) -> dict:
    """{hôte : masque} des incidents communs (E-S-15) ; spec : None ou {"rho" (par jour de strate), "duree" D,
    "geometrique", "hotes" (touches)}. Débuts de Bernoulli de paramètre ρ·w/86 400 par fenêtre de grille (flux
    « incidents », ou u) ; durée D fixe (Q-S-05 a) ou géométrique de moyenne D (sensibilité b), tirée sur le même flux
    après le début, coupée à l'horizon ; hôtes tirés par incident (flux « incidents-hotes », ou v). Panne de transport :
    elle s'ajoute à H, donc frappe toutes les classes de l'hôte (ADR l.162 ; cible d'ETH)."""
    if spec is None:
        return {}
    u = u or flux(prm, cellule, i, "incidents", 0)
    v = v or flux(prm, cellule, i, "incidents-hotes", 0)
    debut, out, t = Geometrique(spec["rho"] * prm["calendrier"]["w"] / 86400, prm["aleas"]), {}, -1
    while True:
        g = debut.tirer(u, horizon - 1 - t)
        if g is None:
            return out
        t += g
        if spec["geometrique"]:
            d = Geometrique(Fraction(1, spec["duree"]), prm["aleas"]).tirer(u, horizon - t)
        else:
            d = min(spec["duree"], horizon - t)
        bits = ((1 << (horizon - t if d is None else d)) - 1) << t
        for h in touches(prm, v, spec["hotes"]):
            out[h] = out.get(h, 0) | bits
