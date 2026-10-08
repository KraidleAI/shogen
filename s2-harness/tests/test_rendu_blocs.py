"""Lot B-DEP-2 d'ADR-0028 (A-2 ; §1 bis.1 pts 3 et 9) : bloc 3 de report.py, section « z_bloc par strate »
rendue depuis r1_out["strates"][s]["bloc"] (lot B-DEP-1) sans recalcul, après les strates confirmatoires et
avant la famille ; ligne A(window-dependence) après A(window-stationarity). Dorés comparés à des valeurs
écrites à la main avant le code (journal G1 du lot, §3 ; annexe C, FM-3.3 : CRITIQUE v2 §4.1 à ℓ = 3 et
ℓ = 1, par la couture r1.bloc_strate) et, à ℓ = 240, à un oracle d'une autre forme (sommes de blocs de la
série tirée du script de pannes, fractions). Fixtures du collecteur réel, w = 60 s ; la panne est le seul
écart (σ énorme, N = 3 < 4 répondantes). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import functools
import os
import re
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from unittest import mock

from shogen_s2 import r1, report
from tests.test_blocs import blocs_numerateur, d50          # lot B-DEP-1 (couplage déclaré au G1)
from tests.test_exclusion import WS, build_fixture, cli
from tests.test_sensibilite import fixture

SAM = int(datetime(2026, 8, 8, tzinfo=timezone.utc).timestamp())      # sam. 00:00Z : première fenêtre stress
S1, S2 = (0, 1, 1, 0, 0, 0, 1, 0, 0, 1), (1, 1, 0, 0, 0, 0, 0, 1, 1, 0)   # CRITIQUE v2 §4.1
TETE = ("  ── z_bloc par strate : plancher d'erreur-type pré-enregistré (blocs mobiles, noyau de Bartlett ; "
        "ADR-0028 §1 bis) — z_s reste la statistique confirmatoire")
F1 = ("    z_bloc = (K − n·P̂_more)/σ̂_bloc, même numérateur que z ; σ̂²_bloc = γ̂₀ + 2·Σ_{k=1}^{ℓ−1} "
      "(1 − k/ℓ)·γ̂_k sur la série I_t = 1{m_t ≥ 2} de la strate, γ̂_k centrés sur Ī = K/n, lag sur la "
      "grille de pas w : paires de deux fenêtres de la strate, fenêtre absente sans paire")
F2 = ("    z_bloc publié si σ̂²_bloc > 0 et n ≥ 30·ℓ (garde de blocs, distincte du drapeau 1), que la "
      "garde §5.4 soit tenue ou non ; FIV = σ̂²_bloc/(n·P̂_more·(1 − P̂_more)) = R_centrage × FIV_série, "
      "R_centrage = γ̂₀/(n·P̂_more·(1 − P̂_more)), FIV_série = σ̂²_bloc/γ̂₀ ; cv théorique = √(4ℓ/(3n)) "
      "[inféré : dérivation de l'AVIS-advisor-defi Q1 (iv)]")
ADEP = ("  A(window-dependence) engagée par le niveau de R1 (ADR-0028 §1 bis.1 pt 7 ; registre 08) : "
        "dépendance sérielle de I_t = 1{m_t ≥ 2} d'une strate de portée < ℓ = 240 fenêtres ; exercée "
        "par z_bloc et le diagnostic de runs de I_t ; décharge = SHOGEN-DEP-FENETRES-2 (08 ; ADR-0028 "
        "annexe B.6)")
R14 = "1.7857142857142857142857142857142857142857142857143"              # 25/14 : γ̂₀ = 2.4, garde = 1.344
RUNS = "diagnostic de runs de I_t (hors décision) : "
GARDE = "z_bloc = non publié : garde de blocs : n_s = "
E45 = Fraction(1, 10 ** 45)


def journal(n_c: int, n_s: int, panne) -> tuple:
    """Collecteur réel, w = 60 s : n_c fenêtres calme jusqu'à SAM, puis n_s stress ; panne(flux, stress, j),
    j = rang de la fenêtre dans sa strate."""
    t0 = SAM - 60 * n_c
    return fixture(tempfile.mkdtemp(prefix="s2bdep2_"), blocs=[range(t0, SAM + 60 * n_s, 60)], w=60,
                   en_panne=lambda f, ws: panne(f, ws >= SAM, (ws - (SAM if ws >= SAM else t0)) // 60))


def panne_s(f: str, st: bool, j: int) -> bool:
    """Fixture S : coinbase et kraken en panne ensemble aux I_t = 1 (calme S1, stress S2), bitstamp jamais."""
    return f != "bitstamp" and (S2 if st else S1)[j] == 1


def section(txt: str) -> tuple:
    """(lignes du bloc 3, index de TETE ou -1, {strate : ses lignes de section, préfixe « s » : retiré})."""
    b3 = txt.split("[BLOC 3]")[1].split("[BLOC 4]")[0].split("\n")
    h, par = (b3.index(TETE) if TETE in b3 else -1), {}
    for ln in b3[h + 3:b3.index("", h)] if h >= 0 else ():
        st, reste = re.match(r"    « (\w+) » : (.*)$", ln).groups()
        par.setdefault(st, []).append(reste)
    return b3, h, par


def vals(ligne: str) -> dict:
    return dict(re.findall(r"(\S+) = (\S+)", ligne))


def proche(x, exact: Fraction, carre: bool = False, tol: Fraction = Fraction(1, 10 ** 47)) -> bool:
    """Chaîne imprimée x (au carré si carre) à tol relatif de la fraction exacte ; x absent ou non
    décimal : faux."""
    try:
        return abs(Fraction(Decimal(x)) ** (2 if carre else 1) / exact - 1) < tol
    except (TypeError, ArithmeticError, ValueError):
        return False


class TestRenduBlocsStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.txt = report.render_report(*journal(10, 10, panne_s))

    def test_section_position_etiquette_vocabulaire(self):
        """Fixture S, production. Rougit si : étiquette absente ou altérée ; section hors position (après la
        famille) ou en-tête dans la boucle des strates ; formules changées ; A(window-dependence) omise ou
        déplacée ; « sensibilité », un mot proscrit par docs/09 ou un mot de valeur dans la section."""
        b3, h, par = section(self.txt)
        self.assertEqual([k for k, ln in enumerate(b3) if ln.startswith("  ── z_bloc")], [h])
        self.assertLess(max(k for k, ln in enumerate(b3) if ln.startswith("  ── strate «")), h)
        self.assertEqual(b3[h - 1:h + 3], ["", TETE, F1, F2])
        self.assertEqual([re.match(r"    « (\w+) » : ", ln) and ln.split("»")[0] for ln in b3[h + 3:h + 11]],
                         ["    « calme "] * 4 + ["    « stress "] * 4)
        fin = b3[h + 11:h + 13]
        self.assertTrue(fin[0] == "" and fin[1].startswith("  famille de Bonferroni"), fin)
        self.assertEqual(b3[b3.index("  " + r1.A_WINDOW_STATIONARITY) + 1], ADEP)
        self.assertEqual(self.txt.count(ADEP), 1)
        mots = re.compile(r"sensibilit|ind[ée]pendant|rejet|évaluable|concord", re.I)
        self.assertEqual([ln for ln in b3[h:h + 11] + [ADEP] if mots.search(ln)], [])
        self.assertTrue(all(p[0].endswith(" [inféré]") for p in par.values()), par)

    def test_motif_garde_de_blocs_production(self):
        """Fixture S, ℓ = 240 : 0 < K < n, n = 10 < 7 200 (journal G1 §3). Rougit si : valeur imprimée à
        la place du motif (garde de blocs ignorée) ; facteur de FIV non imprimé ; valeur d'une autre clé ;
        bloc d'une autre strate."""
        att = {"calme": (str(d50(1, 75)), Fraction(5, 504), Fraction(1, 180)),
               "stress": ("0.03", Fraction(5, 224), Fraction(1, 80))}
        for st, (s2, fiv, fs) in att.items():
            l1, l2, l3, _l4 = section(self.txt)[2].get(st, [""] * 4)
            v, f = vals(l1), vals(l2)
            self.assertEqual((v.get("ℓ"), v.get("γ̂₀"), v.get("σ̂²_bloc"), f.get("R_centrage")),
                             ("240", "2.4", s2, R14))
            self.assertTrue(proche(f.get("FIV"), fiv) and proche(f.get("FIV_série"), fs), l2)
            self.assertTrue(proche(v.get("théorique"), Fraction(32), carre=True), l1)
            self.assertEqual(l3, GARDE + "10 < 30·ℓ = 7200")

    def test_motifs_sigma2_nul_garde_nulle(self):
        """Fixture du lot A (build_fixture : K = 0, P̂_more = 0, drapeau 1 levé, n = 3 par strate).
        Rougit si : FIV_motif ou FIV_serie_motif ignoré ; valeur à la place du motif de z_bloc ; section
        soumise au drapeau 1."""
        _b3, h, par = section(report.render_report(*build_fixture(tempfile.mkdtemp(prefix="s2bdep2_"))))
        self.assertGreater(h, 0)
        for st in ("calme", "stress"):
            l1, l2, l3, l4 = par.get(st, [""] * 4)
            self.assertTrue(l1.startswith("ℓ = 240 ; γ̂₀ = 0 ; σ̂²_bloc = 0 ; cv théorique = "), l1)
            self.assertEqual(l2, "garde n·P̂_more·(1 − P̂_more) ≤ 0 : FIV, R_centrage indéfinis ; "
                                 "γ̂₀ = 0 (K ∈ {0, n}) : FIV_serie indéfini")
            self.assertEqual(l3, "z_bloc = non publié : σ̂²_bloc = 0 (K ∈ {0, n}) ; garde de blocs : "
                                 "n_s = 3 < 30·ℓ = 7200")
            self.assertEqual(l4, RUNS + "nombre = 0 ; longueur moyenne = - ; run maximal = 0")

    def test_sans_strate_ni_en_tete_ligne_adep_seule(self):
        """D-3 (ajouté après le scellement, mutant MR19 écrit avec le code) : plage qui retire toutes les
        fenêtres, aucune strate au bloc 3. Rougit si : en-tête et formules imprimés sans strate ;
        A(window-dependence) omise sans strate."""
        txt = report.render_report(*build_fixture(tempfile.mkdtemp(prefix="s2bdep2_")),
                                   exclude_ranges=[(WS[0], WS[-1])])
        self.assertIn("aucune fenêtre complétée (n = 0)", txt)
        self.assertEqual((TETE in txt, txt.count(ADEP)), (False, 1))


def couture(ell: int):
    """ℓ ≠ 240 au rendu : compute_r1 appelle r1.bloc_strate par son nom de module (D-10 du journal G1)."""
    return mock.patch.object(r1, "bloc_strate", functools.partial(r1.bloc_strate, ell=ell))


class TestRenduBlocsMain(unittest.TestCase):
    """Valeurs à la main de la CRITIQUE v2 §4.1 au rendu (annexe C, FM-3.3), ℓ ≠ 240 par la couture."""

    def test_couture_l3_valeurs_critique(self):
        """Fixture S, ℓ = 3 : σ̂² = 88/75 et 208/75, FIV = 55/63 et 130/63, FIV_série = 22/45 et 52/45.
        Rougit si : facteur de FIV non imprimé ; valeur d'une autre clé ; ℓ lu ailleurs que dans le bloc ;
        « [inféré] » retiré ; longueur moyenne et run maximal permutés ; bloc d'une autre strate ; motif
        remplacé."""
        c, j = journal(10, 10, panne_s)
        with couture(3):
            par = section(report.render_report(c, j))[2]
        m3 = "1.3333333333333333333333333333333333333333333333333"
        att = {"calme": ("1.1733333333333333333333333333333333333333333333333", Fraction(55, 63),
                         Fraction(22, 45), f"nombre = 3 ; longueur moyenne = {m3} ; run maximal = 2"),
               "stress": ("2.7733333333333333333333333333333333333333333333333", Fraction(130, 63),
                          Fraction(52, 45), "nombre = 2 ; longueur moyenne = 2 ; run maximal = 2")}
        for st, (s2, fiv, fs, runs) in att.items():
            l1, l2, l3, l4 = par.get(st, [""] * 4)
            v, f = vals(l1), vals(l2)
            self.assertEqual((v.get("ℓ"), v.get("γ̂₀"), v.get("σ̂²_bloc"), f.get("R_centrage")),
                             ("3", "2.4", s2, R14))
            self.assertTrue(l1.endswith(" [inféré]") and proche(v.get("théorique"), Fraction(2, 5), True), l1)
            self.assertTrue(proche(f.get("FIV"), fiv) and proche(f.get("FIV_série"), fs), l2)
            produit = Fraction(Decimal(R14)) * Fraction(Decimal(f["FIV_série"]))
            self.assertTrue(proche(f.get("FIV"), produit), l2)           # FIV = R_centrage × FIV_série
            self.assertEqual((l3, l4), (GARDE + "10 < 30·ℓ = 90", RUNS + runs))

    def test_couture_l1_fiv_critique(self):
        """Fixture U, ℓ = 1 : FIV(ℓ = 1) = Ī(1−Ī)/(P̂(1−P̂)) à P̂ = 0,01 pour des excès de +20 % et +50 %
        (1,1976 et 1,4924) ; z_bloc publié alors que z ne l'est pas (drapeau 1). Rougit si : FIV_série ou
        R_centrage pour FIV ; motif imprimé quand z_bloc est publié ; section soumise au drapeau 1 ; ℓ lu
        ailleurs."""
        def panne(f, st, j):
            a, b = (20, 17) if st else (25, 22)
            return j < a if f == "coinbase" else f == "kraken" and b <= j < b + a
        c, j = journal(250, 200, panne)
        with couture(1):
            txt = report.render_report(c, j)
        self.assertEqual(txt.count("    z       = non publié (garde §5.4"), 2)
        att = {"calme": ("2.964", "1.1975757575757575757575757575757575757575757575758", "1.1976",
                         Fraction(125, 1482)),
               "stress": ("2.955", "1.4924242424242424242424242424242424242424242424242", "1.4924",
                          Fraction(200, 591))}
        for st, (g0, fiv, arrondi, z2) in att.items():
            l1, l2, l3, l4 = section(txt)[2].get(st, [""] * 4)
            self.assertTrue(l1.startswith(f"ℓ = 1 ; γ̂₀ = {g0} ; σ̂²_bloc = {g0} ; cv théorique = "), l1)
            self.assertEqual(l2, f"FIV = {fiv} ; R_centrage = {fiv} ; FIV_série = 1")
            self.assertEqual(str(round(Decimal(vals(l2)["FIV"]), 4)), arrondi)
            z = vals(l3).get("z_bloc")
            self.assertTrue(proche(z, z2, True, E45) and Decimal(z) > 0, l3)
            self.assertEqual(l4, RUNS + "nombre = 1 ; longueur moyenne = 3 ; run maximal = 3")


class TestRenduBlocsLong(unittest.TestCase):
    """Garde de blocs tenue au rendu de production (ℓ = 240, n = 30·ℓ) : fixture B, 7 200 fenêtres
    calme puis 60 stress, construite une fois (collecteur réel ; temps mesuré au journal G1)."""

    @staticmethod
    def panne(f: str, st: bool, j: int) -> bool:
        if st:
            return f != "bitstamp" and j < 10
        b, o = divmod(j, 100)
        lb = b * 5 % 11
        return {"coinbase": o < lb + 2, "kraken": o < lb or j % 37 == 0, "bitstamp": j % 53 == 0}[f]

    @classmethod
    def setUpClass(cls):
        cls.c, _j = journal(7200, 60, cls.panne)
        cls.txt = report.render_report(cls.c, _j)

    def test_garde_tenue_l240_oracle_sommes_de_blocs(self):
        """Oracle d'une autre forme : série I_t tirée du script de pannes (jamais d'une sortie de r1),
        sommes de blocs entières (tests.test_blocs.blocs_numerateur), P̂_more exact (Poisson-binomiale en
        fractions sur les comptes du script). Rougit si : motif imprimé quand la garde de blocs est tenue
        (n = 30·ℓ) ; garde recalculée au rendu ; valeur d'une autre clé ; bloc d'une autre strate."""
        fl, n, t0 = ("coinbase", "kraken", "bitstamp"), 7200, SAM - 60 * 7200
        serie = [(t0 + 60 * j, int(sum(self.panne(f, False, j) for f in fl) >= 2)) for j in range(n)]
        k, num = sum(i for _, i in serie), blocs_numerateur(serie, 60, 240)
        runs = [len(x) for x in re.findall("1+", "".join(str(i) for _, i in serie))]
        self.assertEqual((k, num, len(runs), max(runs)), (383, 7525014551120, 78, 10))   # journal G1 §3
        p0, p1 = Fraction(1), Fraction(0)
        for f in fl:
            p = Fraction(sum(self.panne(f, False, j) for j in range(n)), n)
            p0, p1 = p0 * (1 - p), p1 * (1 - p) + p0 * p
        pm = 1 - p0 - p1
        garde, s2, g0 = n * pm * (1 - pm), Fraction(num, 240 * n * n), Fraction(n * k - k * k, n)
        par = section(self.txt)[2]
        l1, l2, l3, l4 = par.get("calme", [""] * 4)
        v, f = vals(l1), vals(l2)
        self.assertEqual((v.get("ℓ"), v.get("γ̂₀"), v.get("σ̂²_bloc")),
                         ("240", str(d50(n * k - k * k, n)), str(d50(num, 240 * n * n))))
        self.assertTrue(proche(v.get("théorique"), Fraction(2, 45), True, E45), l1)
        for nom, exact in (("R_centrage", g0 / garde), ("FIV", s2 / garde), ("FIV_série", s2 / g0)):
            self.assertTrue(proche(f.get(nom), exact, tol=E45), (nom, l2))
        produit = Fraction(Decimal(f["R_centrage"])) * Fraction(Decimal(f["FIV_série"]))
        self.assertTrue(proche(f["FIV"], produit), l2)
        z = vals(l3).get("z_bloc")
        self.assertTrue(proche(z, (k - n * pm) ** 2 / s2, True, E45) and Decimal(z) > 0, l3)
        self.assertEqual(l4, RUNS + f"nombre = 78 ; longueur moyenne = {d50(k, 78)} ; run maximal = 10")
        self.assertEqual(par.get("stress", [""] * 3)[2], GARDE + "60 < 30·ℓ = 7200")
        self.assertEqual(self.txt.count("    z       = non publié (garde §5.4"), 1)   # z de calme publié

    def test_cli_processus_neuf_long(self):
        """Chemin servi (python -m shogen_s2.report, processus neuf, PYTHONHASHSEED imposé) = API sur la
        fixture longue. Rougit si : le rendu servi diffère du rendu de l'API."""
        self.assertEqual(cli(os.path.dirname(self.c)), (self.txt + "\n").encode("utf-8"))


class TestRenduBlocsG2(unittest.TestCase):
    """Revue G2 du lot (corrections C-1 à C-3, tests seuls) : branches du rendu qu'aucun test du G1 n'exécute,
    chacune avec le mutant du réviseur qui la rougit (MG01 à MG06, revue G2 du lot B-DEP-2, §5)."""

    def test_g2_mono_strate_nommee(self):
        """C-1 (cp-1 C-3 : « chaque strate de r1_out["strates"] », fixture mono-strate) : calendrier
        mono-strate « unique », n = 40, I_t = 1 aux rangs j ≡ 0, 1 (mod 7) : K = 12, six runs de 2 ;
        σ̂²_bloc recalculé ici par la somme des lags en fractions. Rougit si : section réservée à deux
        strates (MG01) ; strates prises au calendrier « calme » / « stress » plutôt qu'à r1 (MG02)."""
        t0, n = SAM - 60 * 400, 40
        spec = {"kind": "single", "strate": "unique", "note": "mono-strate nommée (revue G2)"}
        c, j = fixture(tempfile.mkdtemp(prefix="s2bdep2g2_"), spec, [range(t0, t0 + 60 * n, 60)], 60,
                       lambda f, ws: f != "bitstamp" and (ws - t0) // 60 % 7 < 2)
        b3, h, par = section(report.render_report(c, j))
        serie = [int(t % 7 < 2) for t in range(n)]
        ib = Fraction(sum(serie), n)
        g = [sum((serie[t] - ib) * (serie[t + k] - ib) for t in range(n - k)) for k in range(n)]
        s2 = g[0] + 2 * sum((1 - Fraction(k, 240)) * g[k] for k in range(1, n))
        self.assertTrue(h > 0 and list(par) == ["unique"], (h, list(par)))
        l1, _l2, l3, l4 = par["unique"]
        v = vals(l1)
        self.assertEqual((v.get("ℓ"), v.get("γ̂₀"), v.get("σ̂²_bloc")),
                         ("240", "8.4", str(d50(s2.numerator, s2.denominator))))
        self.assertEqual((l3, l4), (GARDE + "40 < 30·ℓ = 7200",
                                    RUNS + "nombre = 6 ; longueur moyenne = 2 ; run maximal = 2"))
        self.assertTrue(b3[h + 7] == "" and b3[h + 8].endswith(": non applicable (calendrier mono-strate)"))

    def test_g2_z_bloc_negatif_et_nul_publies(self):
        """C-2 : couture ℓ = 1 (garde de blocs 30), bitstamp jamais en panne, P̂_more = p̂_c·p̂_k = 1/100,
        une fenêtre de panne commune : calme n = 250, K = 1 < n·P̂_more = 5/2, z_bloc² = 375/166,
        z_bloc < 0 ; stress n = 100, K = 1 = n·P̂_more, z_bloc = 0 publié. Rougit si : signe de z_bloc
        perdu au rendu (MG03) ; z_bloc nul lu comme non publié (MG04)."""
        def panne(f, st, j):
            a = 10 if st else 25
            return j < a if f == "coinbase" else f == "kraken" and a - 1 <= j < 2 * a - 1
        c, j = journal(250, 100, panne)
        with couture(1):
            par = section(report.render_report(c, j))[2]
        lc, ls = (par.get(st, [""] * 4)[2] for st in ("calme", "stress"))
        zc, zs = vals(lc).get("z_bloc"), vals(ls).get("z_bloc")
        self.assertTrue(proche(zc, Fraction(375, 166), True, E45) and Decimal(zc) < 0, lc)
        self.assertTrue(ls.startswith("z_bloc = ") and "non publié" not in ls and Decimal(zs) == 0, ls)

    def test_g2_k_nul_garde_positive(self):
        """C-3 : K = 0 et P̂_more > 0 (coinbase puis kraken en panne, jamais ensemble ; ℓ = 240) : FIV et
        R_centrage publiés et nuls, motif de FIV_série à leur suite ; z_bloc non publié (σ̂²_bloc = 0,
        garde de blocs). Forme imprimée du zéro non figée ici (observation de la revue G2). Rougit si :
        motif de FIV_série tenu au motif de FIV (MG05) ; FIV et R_centrage tus si FIV_série a un motif
        (MG06)."""
        def panne(f, st, j):
            a = 10 if st else 25
            return j < a if f == "coinbase" else f == "kraken" and a <= j < 2 * a
        par = section(report.render_report(*journal(250, 100, panne)))[2]
        fin = " ; γ̂₀ = 0 (K ∈ {0, n}) : FIV_serie indéfini"
        for st, n in (("calme", 250), ("stress", 100)):
            _l1, l2, l3, _l4 = par.get(st, [""] * 4)
            f = vals(l2)
            self.assertTrue(l2.startswith("FIV = ") and l2.endswith(fin)
                            and Decimal(f["FIV"]) == 0 == Decimal(f["R_centrage"]), l2)
            self.assertEqual(l3, "z_bloc = non publié : σ̂²_bloc = 0 (K ∈ {0, n}) ; garde de blocs : "
                                 f"n_s = {n} < 30·ℓ = 7200")
