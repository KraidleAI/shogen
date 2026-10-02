"""Lot B-DEP-2 d'ADR-0028 (A-2 ; §1 bis.1 pts 3 et 9) : bloc 3 de report.py, section « z_bloc par strate »
rendue depuis r1_out["strates"][s]["bloc"] (lot B-DEP-1) sans recalcul, après les strates confirmatoires et
avant la famille ; ligne A(window-dependence) après A(window-stationarity). Dorés comparés à des valeurs
écrites à la main avant le code (journal G1 du lot, §3 ; annexe C, FM-3.3 : CRITIQUE v2 §4.1 à ℓ = 3 et
ℓ = 1, par la couture r1.bloc_strate) et, à ℓ = 240, à un oracle d'une autre forme (sommes de blocs de la
série tirée du script de pannes, fractions). Fixtures du collecteur réel, w = 60 s ; la panne est le seul
écart (σ énorme, N = 3 < 4 répondantes). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import re
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction

from shogen_s2 import r1, report
from tests.test_blocs import d50          # lot B-DEP-1 (couplage déclaré au G1)
from tests.test_exclusion import WS, build_fixture
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

