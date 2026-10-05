"""Règle SHOGEN-CRITERE-R1-2 répliquée (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lots SB-7 et SB-8 ; ADR-0029 §2.7
pts 2 à 6 ; E-S-24 à E-S-35) : la simulation ne l'importe pas de RECALC-BIS (Q-S-02 : réplique, recoupée par oracle
croisé à SB-13). Séries consolidées comprimées en entiers (bit t = position t de la suite comprimée des fenêtres
retenues de la strate, calendrier.comprimer). SB-7a : décalages SHA-256 (Q-R-02 adjugée), rotation enroulée, K par le
compteur « au moins deux » et S = Σ_j C(m_j, 2) par plans de bits (E-S-26). SB-7b : seuil entier, retraits D1-bis et
flux presque mort (E-S-24), unité non décalée, décision par strate avec arrêt anticipé exact et garde d'information
(E-S-28, E-S-29). SB-8a : mode à R complet, oracle d'équivalence de l'arrêt anticipé, séquence d'ETH et F3 (E-S-29 à
E-S-31). SB-8b : compte d'événements à tolérance g et critère collectif d'absorption candidat (E-S-34, E-S-35).
SB-8c : alignement sur le contrat de rotation de RB-6 (docs/adr-0029/s2bis/ROTATION-S2BIS.md, diffs RB-6a et RB-6b en
relecture G2 ; adjugé par l'orchestrateur, risque R-2) : libellés de strate calme et stress, r et R de 1 à 9 999, refus
nommés de toutes les entrées avant tout calcul (graine, n, noms d'unité, unité non décalée, masques de [0, 2^n)).
SB-8d (C-1 de la G2 de la tranche 3) : l'oracle d'équivalence compare aussi « C_S ≤ seuil » quand S est suivie.
SB-8e (P-7 de l'avis de la tranche 3) : noms d'unité aux caractères d'un nom d'hôte en minuscules, refusés par _cle.
SB-8f (Q-T3-13 et Q-T3-15 adjugées) : deux queues de la loi du compte d'événements ; unité non décalée prise avant
le critère collectif d'absorption.
Entiers et rationnels seuls : aucun flottant, aucune puissance."""
import hashlib
from fractions import Fraction

import calendrier
import commun

SEP = ":"
STRATES, R_MAX = ("calme", "stress"), 9999      # libellés et borne de r scellés (E-S-27 ; contrat RB-6 §1, pts 2 et 5)
NOM_UNITE, LONG_UNITE = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-."), 253    # P-7 ; comme Q-RB-13 pour RB-6


def _libelle(v, nom: str) -> str:
    """Nom d'unité (P-7 de l'avis de la tranche 3, adjugé avant E0 comme Q-RB-13 adoptée pour RB-6) : caractères d'un
    nom d'hôte en minuscules (NOM_UNITE : lettres a à z, chiffres, « - », « . »), 1 à LONG_UNITE caractères, sinon
    REGLE/libelle ; les noms courts du pool et les noms d'hôte de configuration y passent."""
    if type(v) is str and 0 < len(v) <= LONG_UNITE and set(v) <= NOM_UNITE:
        return v
    raise commun.Refus("REGLE/libelle", f"{nom} = {v!r} : nom d'hôte en minuscules (lettres, chiffres, « - », « . »), "
                                        f"1 à {LONG_UNITE} caractères")


def _cle(graine: str, strate: str, n: int, unites=()) -> None:
    """Graine (64 hexadécimaux minuscules, sinon REGLE/graine), strate parmi STRATES (sinon REGLE/libelle), n entier
    ≥ 1 (sinon REGLE/entier) et noms d'unité (_libelle, sinon REGLE/libelle ; P-7) de l'entrée des décalages, contrôlés
    avant tout calcul (contrat RB-6 §4)."""
    if not commun.hex64(graine):
        raise commun.Refus("REGLE/graine", f"{graine!r} : 64 hexadécimaux minuscules attendus")
    if strate not in STRATES:
        raise commun.Refus("REGLE/libelle", f"strate {strate!r} : {' ou '.join(STRATES)} attendu")
    if type(n) is not int or n < 1:
        raise commun.Refus("REGLE/entier", f"n = {n!r} : entier ≥ 1 attendu")
    for u in unites:
        _libelle(u, "unité")


def decalage(graine: str, strate: str, r: int, u: str, n: int) -> int:
    """o(r, u) (E-S-27 ; ADR-0029 l.200 ; Q-R-02 adjugée, AVIS-C l.57-63 ; contrat RB-6 §2) : entier big-endian des 32
    octets de SHA-256 de la chaîne ASCII « <graine>:<strate>:<r>:<u> », modulo n (n_s, ou n′_s, de la strate). Graine,
    strate, n et unité (nom d'hôte en minuscules, P-7) : _cle ; r de 1 à 9 999, en décimal sans zéro de tête (sinon
    REGLE/entier)."""
    _cle(graine, strate, n, [u])
    if type(r) is not int or not 1 <= r <= R_MAX:
        raise commun.Refus("REGLE/entier", f"r = {r!r} : entier de 1 à {R_MAX} attendu")
    chaine = SEP.join([graine, strate, str(r), u])
    return int.from_bytes(hashlib.sha256(chaine.encode("ascii")).digest(), "big") % n


def tourner(x: int, o: int, n: int) -> int:
    """Rotation enroulée de la suite comprimée de longueur n (ADR-0029 l.200 ; sens de Q-R-02) : la valeur de la
    position t va en (t + o) mod n, 0 ≤ o < n."""
    return ((x << o) | (x >> (n - o))) & ((1 << n) - 1)


def deux(series: list) -> int:
    """Masque I des positions où au moins deux séries valent 1 (compteur « au moins deux » sur masques de bits,
    E-S-26) : K = |I| (ADR-0029 §2.4 : K_s = #{j : m_j ≥ 2}) ; les runs de I se comptent sur la suite comprimée
    (E-S-28)."""
    un = au_moins_deux = 0
    for x in series:
        au_moins_deux |= un & x
        un |= x
    return au_moins_deux


def paires(series: list) -> int:
    """S = Σ_j C(m_j, 2) (E-S-26 ; ADR-0029 l.164, l.212) : m_j en quatre plans de bits p_b (additionneur à retenue, au
    plus 15 séries, sinon REGLE/plans), puis S = Σ_b ((4^b − 2^b)/2)·|p_b| + Σ_{b<c} 2^(b+c)·|p_b ∧ p_c|, puisque
    m² = Σ_b 4^b·p_b + 2·Σ_{b<c} 2^(b+c)·p_b·p_c ; puissances de deux par décalage."""
    if len(series) > 15:
        raise commun.Refus("REGLE/plans", f"{len(series)} séries : au plus 15")
    p = [0, 0, 0, 0]
    for x in series:
        for b in range(4):
            p[b], x = p[b] ^ x, p[b] & x
    s = 0
    for b in range(4):
        s += (((1 << (2 * b)) - (1 << b)) >> 1) * p[b].bit_count()
        for c in range(b + 1, 4):
            s += (1 << (b + c)) * (p[b] & p[c]).bit_count()
    return s


CAUSES = ("unites", "k_crit", "runs", "n_prime")


def seuil(R: int, alpha) -> int:
    """Seuil entier de C (ADR-0029 l.202) : C ≤ seuil ⇔ (C + 1)/(R + 1) ≤ α, soit seuil = α·(R + 1) − 1 (99 à R = 9 999,
    9 à R = 999 : AVIS Q-S-06), entier ≥ 0 exigé, R entier de 1 à 9 999 (contrat RB-6 §1, pt 9), sinon REGLE/seuil."""
    s = Fraction(*alpha) * (R + 1) - 1 if type(R) is int and 1 <= R <= R_MAX else Fraction(-1)
    if s.denominator != 1 or s < 0:
        raise commun.Refus("REGLE/seuil", f"R = {R!r}, α = {alpha!r} : α·(R + 1) − 1 entier ≥ 0 attendu")
    return int(s)


def retraits(ok: dict, n: dict) -> dict:
    """Retraits d'une classe avant K (E-S-24 ; ADR-0029 l.170 : règle D1 reprise, flux presque mort ex ante) : ok =
    {(u, s) : fenêtres retenues de la strate s à « ok » consolidé}, n = {s : n_s, ou n′_s} ; rend {(u, s) : motif} :
    « D1-bis (a) » si u n'a aucun ok dans aucune strate (retirée partout), « D1-bis (b) » s'il n'en a aucun dans s,
    « presque mort » si 2·ok(u, s) < n(s) ; les autres unités restent."""
    out = {}
    for u in sorted({u for u, _s in ok}):
        strates = [s for s in n if (u, s) in ok]
        aucun = all(ok[u, s] == 0 for s in strates)
        for s in strates:
            if aucun:
                out[u, s] = "D1-bis (a)"
            elif ok[u, s] == 0:
                out[u, s] = "D1-bis (b)"
            elif 2 * ok[u, s] < n[s]:
                out[u, s] = "presque mort"
    return out


def premiere(btc: list):
    """Unité non décalée (ADR-0029 l.200 ; Q-T3-15, avis modifié, adjugé avant E0) : premier hôte, par ordre des points
    de code (« alphabétique »), du pool BTC D1-bis de la strate, pris après les retraits D1-bis (a), (b) et « presque
    mort » (retraits) et avant le critère collectif d'absorption (filtrer), sans être recalculé après lui : si le
    critère la retire d'une classe, elle y manque et toutes les unités de la classe sont décalées (rotation) ; None si
    ce pool est vide."""
    return min(btc) if btc else None


def decider(K: int, runs: int, unites: int, suffisant: bool, ks, R: int, prm: dict, S=None) -> dict:
    """Valeur de R1-2 dans une strate (E-S-28, E-S-29 ; ADR-0029 l.200-203). Entrées : K = K_s, runs de I sur la suite
    comprimée, nombre d'unités avec au moins un écart consolidé, n′_s ≥ n_s/2, itérable des (K^(r), S^(r)) pour
    r = 1, 2, … (S^(r) lu si S, valeur observée, est donnée), R. C = #{r : K^(r) ≥ K}, C1 = #{r : K^(r) ≥ k_crit − 1}
    (K_crit,s ≥ k_crit ⇔ C1 > seuil), C_S = #{r : S^(r) ≥ S} ; arrêt anticipé exact dès que C > seuil et C1 > seuil (et
    C_S > seuil si S est suivie) : les compteurs ne décroissent pas en r. Garde (causes de NON ÉVALUABLE, non
    exclusives) : unites, k_crit, runs, n_prime. REJETTE ⇔ aucune cause et C ≤ seuil. Moins de R rotations sans arrêt :
    REGLE/rotations."""
    g, s_, it = prm["regle"]["garde"], seuil(R, prm["regle"]["alpha"]), iter(ks)
    c = c1 = cs = 0
    for r in range(1, R + 1):
        try:
            k, sr = next(it)
        except StopIteration:
            raise commun.Refus("REGLE/rotations", f"{r - 1} rotations, R = {R}") from None
        c, c1 = c + (k >= K), c1 + (k >= g["k_crit"] - 1)
        if S is not None:
            cs += sr >= S
        if c > s_ and c1 > s_ and (S is None or cs > s_):
            break
    return dict(_valeur(unites, c1, runs, suffisant, c, g, s_), C=c, C1=c1, C_S=None if S is None else cs, r=r)


def _valeur(unites: int, c1: int, runs: int, suffisant: bool, c: int, g: dict, s_: int) -> dict:
    """Garde (causes de NON ÉVALUABLE, non exclusives, dans l'ordre de CAUSES) et valeur (ADR-0029 l.203)."""
    causes = [x for x, v in zip(CAUSES, (unites < g["unites"], c1 <= s_, runs < g["runs"], not suffisant)) if v]
    return {"valeur": "NON ÉVALUABLE" if causes else "REJETTE" if c <= s_ else "NE REJETTE PAS", "causes": causes}


def rotation(series: dict, premier, graine: str, strate: str, r: int, n: int) -> list:
    """Séries tournées de la rotation r (rotations jointes par hôte : o(r, u) ne dépend pas de la classe, ADR-0029
    l.200) ; l'unité `premier` n'est pas décalée (None : toutes le sont)."""
    return [x if u == premier else tourner(x, decalage(graine, strate, r, u, n), n) for u, x in series.items()]


def _masques(series: dict, n: int) -> None:
    """n entier ≥ 1 (sinon REGLE/entier) ; chaque série, masque entier de [0, 2^n), booléen refusé (bit t = position t
    de la suite comprimée ; sinon REGLE/masque ; contrat RB-6 §1, pt 7)."""
    if type(n) is not int or n < 1:
        raise commun.Refus("REGLE/entier", f"n = {n!r} : entier ≥ 1 attendu")
    for u, x in series.items():
        if type(x) is not int or x < 0 or x >> n:
            raise commun.Refus("REGLE/masque", f"{u!r} : {x!r} hors de [0, 2^{n})")


def _controler(series: dict, premier, graine: str, strate: str, n: int, prm: dict) -> None:
    """Refus nommés de toutes les entrées, avant tout calcul, même sans rotation (contrat RB-6 §4) : strate parmi
    calibration.strates (REGLE/libelle), puis par _cle graine, strate, n et noms des unités et de l'unité non décalée
    (REGLE/libelle, P-7), masques (_masques)."""
    if strate not in prm["calibration"]["strates"]:
        raise commun.Refus("REGLE/libelle", f"strate {strate!r}")
    _cle(graine, strate, n, [*series, *([] if premier is None else [premier])])
    _masques(series, n)


def _entrees(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, avec_S: bool):
    """(base, arguments de decider et complet, générateur des (K^(r), S^(r)), S) d'une classe dans une strate, entrées
    contrôlées par _controler ; avec au plus une série non nulle, K^(r) = S^(r) = 0 pour tout r, exactement : aucune
    rotation calculée."""
    _controler(series, premier, graine, strate, n, prm)
    vals = list(series.values())
    i, unites, S = deux(vals), sum(1 for x in vals if x), paires(vals) if avec_S else None

    def ks():
        for r in range(1, R + 1):
            rot = rotation(series, premier, graine, strate, r, n) if unites >= 2 else []
            yield deux(rot).bit_count(), paires(rot) if avec_S else None
    base = {"K": i.bit_count(), "S": S, "runs": calendrier.runs(i), "unites": unites}
    return base, (base["K"], base["runs"], unites, 2 * n >= n_s), ks(), S


def tester(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, avec_S=False) -> dict:
    """R1-2 pour une classe dans une strate, avec arrêt anticipé : series = {u : D(u, ·) comprimée sur les n fenêtres
    retenues (n_s, ou n′_s)} des unités restées après retraits ; premier : unité non décalée (premiere) ; graine de
    règle de la réplication (aleas.graine_regle) ; rend decider(), plus K, S, runs et unites."""
    base, a, ks, S = _entrees(series, premier, graine, strate, n, n_s, prm, R, avec_S)
    return {**decider(*a, ks, R, prm, S), **base}


def complet(K: int, runs: int, unites: int, suffisant: bool, ks, R: int, prm: dict, S=None) -> dict:
    """Mode à R complet (E-S-29 ; ADR-0029 l.199-200) : les R rotations, sans arrêt ; C, C1, C_S exacts, loi des K^(r),
    K_crit,s = plus petit k tel que #{r : K^(r) ≥ k} ≤ seuil, moyenne K̄_rot,s exacte ; même garde, même valeur que
    decider(). Autre nombre de rotations que R : REGLE/rotations."""
    g, s_, vals = prm["regle"]["garde"], seuil(R, prm["regle"]["alpha"]), list(ks)
    if len(vals) != R:
        raise commun.Refus("REGLE/rotations", f"{len(vals)} rotations, R = {R}")
    loi = {}
    for k, _s in vals:
        loi[k] = loi.get(k, 0) + 1

    def au_moins(x):
        return sum(v for k, v in loi.items() if k >= x)
    c, c1, k_crit = au_moins(K), au_moins(g["k_crit"] - 1), 0
    while au_moins(k_crit) > s_:
        k_crit += 1
    cs = None if S is None else sum(1 for _k, x in vals if x >= S)
    return dict(_valeur(unites, c1, runs, suffisant, c, g, s_), C=c, C1=c1, C_S=cs, r=R, K_crit=k_crit,
                moyenne=Fraction(sum(k * v for k, v in loi.items()), R), loi=sorted(loi.items()))


def deux_modes(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, avec_S=False):
    """(arrêt anticipé, R complet) sur les mêmes R rotations, calculées une fois (oracle d'équivalence, E-S-29)."""
    base, a, ks, S = _entrees(series, premier, graine, strate, n, n_s, prm, R, avec_S)
    vals = list(ks)
    return {**decider(*a, vals, R, prm, S), **base}, {**complet(*a, vals, R, prm, S), **base}


def oracle(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, avec_S=False) -> dict:
    """Oracle d'équivalence de l'arrêt anticipé (E-S-29 : sous-ensemble pré-déclaré, les 200 premières réplications de
    chaque cellule) : rend le résultat anticipé si sa valeur et ses causes égalent celles du mode à R complet et, S
    suivie, si « C_S ≤ seuil » y a la même réponse (C-1 de la G2 de la tranche 3 : l'arrêt attend aussi C_S > seuil),
    sinon REGLE/oracle."""
    a, f = deux_modes(series, premier, graine, strate, n, n_s, prm, R, avec_S)
    s_ = seuil(R, prm["regle"]["alpha"])

    def cle(x):
        return x["valeur"], x["causes"], avec_S and x["C_S"] <= s_
    if cle(a) != cle(f):
        raise commun.Refus("REGLE/oracle", f"anticipé {a['valeur']} {a['causes']} C_S {a['C_S']}, complet "
                                           f"{f['valeur']} {f['causes']} C_S {f['C_S']}")
    return a


F3, ETIQUETTE_F3 = ("USDC", "USDT"), "exploratoire, hors décision"


def strate(resultats: dict) -> dict:
    """Valeurs d'une strate par classe (E-S-30, E-S-31 ; ADR-0029 l.204, l.211) : BTC (F1) telle quelle ; ETH (F2) :
    valeur de son test si BTC REJETTE dans la strate, sinon « NON TESTÉ (séquence) », le test sans condition gardé en
    diagnostic ; USDC et USDT (F3) : valeur et causes du moteur, étiquette « exploratoire, hors décision », aucune
    valeur de registre ; familial : au moins un rejet dans la séquence BTC puis ETH."""
    btc = resultats["BTC"]
    out = {"BTC": {"famille": "F1", "valeur": btc["valeur"], "causes": btc["causes"]}}
    if "ETH" in resultats:
        e = resultats["ETH"]
        out["ETH"] = {"famille": "F2", "valeur": e["valeur"] if btc["valeur"] == "REJETTE" else "NON TESTÉ (séquence)",
                      "causes": e["causes"], "sans_condition": e["valeur"]}
    for c in (c for c in F3 if c in resultats):
        out[c] = {"famille": "F3", "valeur": resultats[c]["valeur"], "causes": resultats[c]["causes"], "registre": None,
                  "etiquette": ETIQUETTE_F3}
    out["familial"] = "REJETTE" in (out["BTC"]["valeur"], out.get("ETH", {}).get("valeur"))
    return out


def evenements(i: int, g: int, n: int) -> int:
    """Compte d'événements (E-S-34 ; ADR-0029 l.212, hors décision) : runs de I sur la suite comprimée de longueur n,
    deux runs séparés par au plus g positions à 0 fusionnés (tolérance en positions de la suite comprimée, jamais de la
    grille ; suite linéaire, sans enroulement) : chaque 1 étendu de g positions vers l'avant, par doublements."""
    x, fait = i, 1
    while fait < g + 1:
        pas = min(fait, g + 1 - fait)
        x, fait = x | (x << pas), fait + pas
    return calendrier.runs(x & ((1 << n) - 1))


def loi_evenements(series: dict, premier, graine: str, strate: str, n: int, R: int, prm: dict) -> dict:
    """Loi de rotation du compte d'événements (E-S-34 : mêmes rotations r = 1..R que K, R complet, statistique hors
    décision ; suite comprimée lue linéairement pour I comme pour I^(r)) pour chaque tolérance g de regle.tolerances :
    {g : {"E" : compte observé, "C" : #{r : E^(r) ≥ E}, "C_bas" : #{r : E^(r) ≤ E}}}, les deux queues (Q-T3-13, avis
    modifié : Q-S-18 se lit sur la queue pré-déclarée C, C_bas est imprimée hors décision) ; entrées contrôlées par
    _controler, R entier de 1 à 9 999 (sinon REGLE/entier), avant tout calcul."""
    _controler(series, premier, graine, strate, n, prm)
    if type(R) is not int or not 1 <= R <= R_MAX:
        raise commun.Refus("REGLE/entier", f"R = {R!r} : entier de 1 à {R_MAX} attendu")
    gs, i = prm["regle"]["tolerances"], deux(list(series.values()))
    obs, c, b = {g: evenements(i, g, n) for g in gs}, {g: 0 for g in gs}, {g: 0 for g in gs}
    for r in range(1, R + 1):
        j = deux(rotation(series, premier, graine, strate, r, n))
        for g in gs:
            e = evenements(j, g, n)
            c[g], b[g] = c[g] + (e >= obs[g]), b[g] + (e <= obs[g])
    return {g: {"E": obs[g], "C": c[g], "C_bas": b[g]} for g in gs}


def absorption(p: dict, c_etoile) -> tuple:
    """Critère collectif d'absorption candidat (E-S-35 ; Q-R-10 ; Q-S-15 : mesuré, adoption décidée par
    l'orchestrateur) : p = {u : p̂_u} rationnels de [0, 1] ; retraits un à un par p̂ décroissant (égalité : nom
    croissant) tant que Σ_u p̂_u/(1 − p̂_u) > c* (un p̂_u = 1 rend l'indice infini) ; rend (retirées dans l'ordre,
    indice final). Il ne lit que des marges, invariantes par rotation."""
    reste, retirees = dict(p), []

    def indice():
        return None if 1 in reste.values() else sum((x / (1 - x) for x in reste.values()), Fraction(0))
    while reste and (indice() is None or indice() > c_etoile):
        u = sorted(reste, key=lambda v: (-reste[v], v))[0]
        retirees.append(u)
        del reste[u]
    return retirees, indice()


def filtrer(series: dict, n: int, prm: dict) -> tuple:
    """Séries restées après le critère collectif (valeurs « avec » ; les valeurs « sans » prennent toutes les séries) :
    p̂_u = écarts consolidés de u sur la suite comprimée / n, après les retraits ; rend (séries restées, retirées,
    indice final). L'unité non décalée reste celle de premiere(), prise avant ce critère (Q-T3-15). Masques et n
    contrôlés par _masques."""
    _masques(series, n)
    p = {u: Fraction(x.bit_count(), n) for u, x in series.items()}
    ret, ind = absorption(p, Fraction(*prm["regle"]["c_etoile"]))
    return {u: x for u, x in series.items() if u not in ret}, ret, ind
