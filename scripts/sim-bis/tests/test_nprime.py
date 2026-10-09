"""Strate sans fenêtre retenue, n′_s = 0 (SB-11x ; SHOGEN-SIM-BIS-NPRIME-NUL-1, option (b) adjugée le
2026-10-09 ; E-S-28, E-S-45, E-S-52) : enregistrement dégénéré de executer.replication, regle inchangée (n ≥ 1,
contrat RB-6 §4). Fixture : cellule T-imp de tests/test_impressions.py, grille « large », repli, W = 1, i = 1
(recette du contre-contrôle de SB-11 : n′ de stress 0 pour n_s = 2 736). Attendus écrits à la main, ou rendus par
regle.tester et variante.tester sur séries vides à n = 1 ; chaque test nomme les mutations qui le rougissent."""
import copy
import os
import tempfile
import unittest
from fractions import Fraction
from unittest import mock

import aleas
import commun
import executer
import regle
import variante
from tests import test_impressions as ti

# R du prm (199) distinct du R de la cellule (99), de n_s (2 736), de n′ (0) et de N (0) : chaque valeur se lit seule.
P = dict(ti.P99, regle=dict(ti.P99["regle"], R=199, R_approche=99))
RICHE = {"classes": ["BTC", "ETH", "USDC", "USDT"], "S": True, "absorption": True, "variante": [4, 8], "evenements": 2}
CAUSES = ["unites", "k_crit", "runs", "n_prime"]
COURT = ("valeur", "causes", "C", "C1", "C_S", "r", "K", "S", "runs", "unites")


def cellule(**regle_):
    return ti.cel(couche__grille="large", couche__repli=True, regle=dict(copy.deepcopy(ti.CEL["regle"]), **regle_))


def rep(test, prm, cel, i=1):
    """executer.replication(…, W = 1, i) ; un refus nommé est un échec du test, code en clair."""
    try:
        return executer.replication(prm, ti.EP, cel, ti.POINTS, 1, i)
    except commun.Refus as e:
        test.fail(f"refus {e.code} : {e}")


def reference(rg, n_s):
    """Ce que regle.tester (« avec » : séries restées, retirées et indice de regle.filtrer) et variante.tester rendent
    sur séries vides à n = 1, en stress, sous P et la règle rg de la cellule (R, S, absorption, diviseurs)."""
    a = ({}, None, aleas.graine_regle(P["aleas"], "T-imp", 1), "stress", 1, n_s, P, rg["R"])
    out = {k: x for k, x in regle.tester(*a, rg["S"]).items() if k in COURT}
    if rg["absorption"]:
        reste, ret, ind = regle.filtrer({}, 1, P)
        out["avec"] = dict({k: x for k, x in regle.tester(reste, *a[1:], rg["S"]).items() if k in COURT},
                           retirees=ret, indice=ind)
    for d in rg["variante"]:
        w = variante.tester(*a, d)
        out.setdefault("variante", {})[str(d)] = dict({k: x for k, x in w.items() if k in COURT}, N=w["N"])
    return out


def octets(x):
    """JSON canonique de l'enregistrement (C-4 de la G2 de SB-11x : Fraction(0) et 0, 0 et False s'y distinguent)."""
    return commun.json_canonique(executer.jsonable(x))


class TestNPrimeNul(unittest.TestCase):
    def test_reproduction(self):
        """Test 1 de l'avis : la recette du contre-contrôle ne lève plus (elle levait REGLE/entier) ; garde de
        fixture : n′ de stress nul, n′ de calme non nul ; chaque classe de stress : NON ÉVALUABLE, les quatre causes
        (écrites ici), aucune première unité, retraits non vides. Mutations M-NP-01 (n′ = 0 jamais pris), M-NP-06
        (n′ de calme lu pour stress)."""
        r = rep(self, ti.P99, cellule())["strates"]
        self.assertEqual(r["stress"]["n"], 0)
        self.assertGreater(r["calme"]["n"], 0)
        x = r["stress"]
        self.assertIsNone(x["premiere"])
        for cl, y in x["classes"].items():
            self.assertEqual((y["valeur"], y["causes"]), ("NON ÉVALUABLE", CAUSES), cl)
            self.assertTrue(x["retraits"][cl], cl)

    def test_forme_et_agreger(self):
        """Test 2 de l'avis, cellule à quatre classes, S suivie, critère collectif, variante 4 et 8, événements sur
        i < 2, R = 99 sous un prm à R = 199 : regle.oracle (8 appels), variante.deux_modes (8) et regle.loi_evenements
        (4) en calme seulement ; en stress, enregistrement écrit à la main (C = r = C_S = R de la cellule ; C1, K, S,
        runs, unites nuls ; « avec » : rien de retiré, indice 0 ; variante : C_S None, N = 0) ; mêmes clés qu'en
        calme, « evenements » à part (branche sautée) ; agreger sur trois copies : NON ÉVALUABLE 3, insuffisante 3,
        chaque cause 3, une combinaison. Mutations M-NP-03 (événements à n′ = 0), M-NP-04 (C = 0), M-NP-05 (n′ de
        stress lu pour calme), M-NP-07 (R du prm), M-NP-08 (« avec » omis), M-NP-09 (variante omise), M-NP-10 (C_S
        sans S), M-NP-11 (S None), M-NP-12 (C_S de la variante), M-NP-13 (N = diviseur), M-NP-14 (indice None),
        M-NP-15 (S omis de « avec »)."""
        espions = [mock.patch.object(m, f, wraps=getattr(m, f)) for m, f in (
            (regle, "oracle"), (variante, "deux_modes"), (regle, "loi_evenements"))]
        vus = [e.start() for e in espions]
        try:
            r = rep(self, P, cellule(**RICHE))
        finally:
            mock.patch.stopall()
        n = r["strates"]["calme"]["n"]
        self.assertEqual([[(x.args[3], x.args[4]) for x in v.call_args_list] for v in vus],
                         [[("calme", n)] * 8, [("calme", n)] * 8, [("calme", n)] * 4])
        base = {"valeur": "NON ÉVALUABLE", "causes": CAUSES, "C": 99, "C1": 0, "C_S": 99, "r": 99, "K": 0, "S": 0,
                "runs": 0, "unites": 0}
        v = dict({k: x for k, x in base.items() if k != "S"}, C_S=None, N=0)
        attendu = dict(base, avec=dict(base, retirees=[], indice=Fraction(0)), variante={"4": v, "8": v})
        for cl in RICHE["classes"]:
            y, z = r["strates"]["stress"]["classes"][cl], r["strates"]["calme"]["classes"][cl]
            self.assertEqual(y, attendu, cl)
            self.assertEqual((sorted(y), "evenements" in z), (sorted(k for k in z if k != "evenements"), True), cl)
            self.assertEqual((sorted(y["avec"]), sorted(y["variante"]["8"])),
                             (sorted(z["avec"]), sorted(z["variante"]["8"])), cl)
        g = executer.agreger(P["calibration"], [r] * 3)["strates"]["stress"]["classes"]
        for cl in RICHE["classes"]:
            for b in (g[cl], g[cl]["avec"], g[cl]["variante"]["4"], g[cl]["variante"]["8"]):
                f = b["frequences"]
                self.assertEqual((f["valeurs"]["NON ÉVALUABLE"], f["insuffisante"], f["causes"], f["combinaisons"]),
                                 (3, 3, dict.fromkeys(CAUSES, 3), {"+".join(CAUSES): 3}), cl)

    def test_equivalence_regle(self):
        """Test 3 de l'avis (rien d'inventé) : S non suivie (ni critère, ni variante), puis suivie (critère, variante
        4 et 8) ; l'enregistrement de stress égale, champ par champ, ce que rendent sur séries vides à n = 1 et
        n_s = 2 736 regle.tester (« avec » : séries restées, retirées et indice de regle.filtrer) et variante.tester ;
        liste de causes permutée dans regle (regle.CAUSES) : l'enregistrement la suit ; C-9 (R-2 du contre-contrôle de
        SB-11y) : égalité aussi en octets du JSON canonique avec la référence à n_s = 3, 4, 7 et 2 736. Mutations
        M-NP-02 (causes écrites dans executer), M-NP-04, M-NP-07 à M-NP-15, M-NP-20, M-NP-21."""
        for causes in (regle.CAUSES, tuple(reversed(regle.CAUSES))):
            with mock.patch.object(regle, "CAUSES", causes):
                for c in (cellule(R=99), cellule(**RICHE)):
                    rg = c["regle"]
                    y = rep(self, P, c)["strates"]["stress"]["classes"]
                    for cl in rg["classes"]:
                        self.assertEqual((y[cl], y[cl]["causes"]), (reference(rg, 2736), list(causes)), (cl, rg["S"]))
                        for n_s in (3, 4, 7, 2736):
                            self.assertEqual(octets(y[cl]), octets(reference(rg, n_s)), (cl, rg["S"], n_s))

    def test_etiquettes_croisees_et_octets(self):
        """C-1, C-2 et C-4 de la G2 de SB-11x : S et absorption de valeurs opposées, (S, critère absent, variante 8)
        puis (S absente, critère, variante 4) ; R de la cellule égal au R_approche (99), puis au R (199) de P ; chaque
        classe de stress égale la référence de regle et variante en octets du JSON canonique ; C = r = R de la
        cellule. Mutants G2-M04, G2-M05, G2-M06, G2-M08, G2-M12, G2-M13, M-NP-16 à M-NP-21."""
        for R in (99, 199):
            for S, ab, va in ((True, False, [8]), (False, True, [4])):
                c = cellule(R=R, classes=["BTC", "ETH"], S=S, absorption=ab, variante=va)
                y = rep(self, P, c)["strates"]["stress"]
                self.assertEqual(y["n"], 0)
                for cl in ("BTC", "ETH"):
                    z = y["classes"][cl]
                    self.assertEqual((octets(z), z["C"], z["r"]), (octets(reference(c["regle"], 2736)), R, R),
                                     (R, S, cl))

    def test_n_prime_partiel(self):
        """C-3 de la G2 de SB-11x (source de « vide ») : 0 < n′ < n_s/2 (même cellule, i = 65 : n′ de stress 650 pour
        n_s = 2 736, suffisant faux) passe par la règle : regle.oracle appelé en stress à n = 650, valeur de la règle
        (cause n_prime). Mutants G2-M01, M-NP-22."""
        with mock.patch.object(regle, "oracle", wraps=regle.oracle) as o:
            r = rep(self, ti.P99, cellule(), 65)["strates"]["stress"]
        self.assertEqual((r["n"], r["suffisant"], "n_prime" in r["classes"]["BTC"]["causes"]), (650, False, True))
        self.assertIn(("stress", 650), [(x.args[3], x.args[4]) for x in o.call_args_list])

    def test_premiere_absente(self):
        """C-3 de la G2 de SB-11x : n′ > 0 dans les deux strates (i = 0) et aucune première unité BTC (regle.premiere
        rendue None) : la règle est appelée dans chaque strate. Mutants G2-M03, M-NP-23."""
        with mock.patch.object(regle, "premiere", return_value=None), mock.patch.object(
                regle, "oracle", wraps=regle.oracle) as o:
            r = rep(self, ti.P99, cellule(), 0)["strates"]
        self.assertEqual([r[s]["n"] > 0 for s in ("calme", "stress")], [True, True])
        self.assertEqual(sorted({x.args[3] for x in o.call_args_list}), ["calme", "stress"])

    def test_n_prime_partiel_resultat(self):
        """C-11 (R-4 du contre-contrôle de SB-11y ; C-3 en entier) : à 0 < n′ < n_s/2 (i = 65, n′ de stress 650),
        l'enregistrement BTC de stress est celui que _tester a rendu (espion), jamais l'enregistrement dégénéré : pas de
        cause « unites » ; C-13 (R-6) : octets du JSON canonique figés au moment de l'appel. Mutants M-CC-01 (règle
        appelée, résultat remplacé par l'enregistrement dégénéré), M-CC-06 (résultat retouché sur place après
        l'appel)."""
        vrai, vus = executer._tester, []

        def espion(p, rg, i, a):
            r = vrai(p, rg, i, a)
            vus.append((a[3], octets(r)))
            return r
        with mock.patch.object(executer, "_tester", side_effect=espion):
            r = rep(self, ti.P99, cellule(), 65)["strates"]["stress"]
        self.assertEqual([x for s, x in vus if s == "stress"], [octets(r["classes"]["BTC"])])
        self.assertEqual((r["n"], "unites" in r["classes"]["BTC"]["causes"]), (650, False))

    def test_compte_premiere_absente(self):
        """C-12 (R-5 du contre-contrôle de SB-11y ; C-7, source des comptes) : regle.premiere rendue None aux
        réplications 0 (n′ > 0 dans les deux strates) et 1 (n′ de stress nul) : n′ nul calme 0, stress 1 ; oracle
        calme 2, stress 1 ; cellule 3. Mutants M-CC-03 (n′ nul lu sur « aucune première unité »), M-CC-04 (oracle lu
        sur « première unité présente »)."""
        with mock.patch.object(regle, "premiere", return_value=None):
            x = [rep(self, ti.P99, cellule(), i) for i in (0, 1)]
        self.assertEqual([[r["strates"][s]["n"] > 0 for r in x] for s in ("calme", "stress")],
                         [[True, True], [True, False]])
        g = executer.agreger(ti.P99["calibration"], x)
        self.assertEqual([[g["strates"][s].get(k) for k in ("n_prime_nul", "oracle")] for s in ("calme", "stress")]
                         + [g.get("oracle")], [[0, 2], [1, 1], 3])

    def test_compte_n_prime_et_oracle(self):
        """C-7 (I-2, I-3) : agreger imprime, par strate, les réplications à n′_s = 0 et les comparaisons effectives de
        l'oracle d'E-S-29 (réplication i < ORACLE, n′_s > 0), et leur somme par cellule. T-imp, grille large, repli :
        i = 1 et 5 (n′ de stress nul), 65 (n′ 650, suffisant faux) ; la réplication 5 relue sous i = ORACLE. Calme :
        0 à n′ nul, 2 comparaisons ; stress : 2 et 1 ; cellule : 3. Mutants M-NP-24 à M-NP-27."""
        x = [rep(self, ti.P99, cellule(), i) for i in (1, 65, 5)]
        x[2] = dict(x[2], i=executer.ORACLE)
        self.assertEqual([[r["strates"][s]["n"] > 0 for r in x] for s in ("calme", "stress")],
                         [[True] * 3, [False, True, False]])
        g = executer.agreger(ti.P99["calibration"], x)
        self.assertEqual([[g["strates"][s].get(k) for k in ("n_prime_nul", "oracle")] for s in ("calme", "stress")]
                         + [g.get("oracle")], [[0, 2], [2, 1], 3])

    def test_contrat_regle_inchange(self):
        """Test 4 de l'avis : regle garde son contrat (RB-6 §4, SHOGEN-SIM-BIS-CONTRAT-RB6-1) : à n = 0 et séries
        vides, tester, oracle, deux_modes, loi_evenements, filtrer et variante.tester lèvent toujours REGLE/entier."""
        g = aleas.graine_regle(P["aleas"], "T-imp", 1)
        a = ({}, None, g, "stress", 0, 2736, P, 99)
        for f, x in ((regle.tester, a), (regle.oracle, a), (regle.deux_modes, a), (variante.tester, a),
                     (regle.loi_evenements, a[:5] + (99, P)), (regle.filtrer, ({}, 0, P))):
            with self.subTest(f=f.__name__), self.assertRaises(commun.Refus) as e:
                f(*x)
            self.assertEqual(e.exception.code, "REGLE/entier", f.__name__)

    def test_determinisme(self):
        """Test 5 de l'avis (E-S-44, dans la suite) : la réplication à n′ = 0, refaite, rend le même enregistrement ;
        son lot écrit deux fois (ecrire_lot, deux dossiers) a les mêmes octets et le même sha256. Le passage hors
        suite (un contre quatre processus, PYTHONHASHSEED 0 contre 1) est joint au rapport du sous-lot."""
        c = cellule(**RICHE)
        x, y = rep(self, P, c), rep(self, P, c)
        self.assertEqual(executer.empreinte([x]), executer.empreinte([y]))
        h = []
        with tempfile.TemporaryDirectory() as d:
            for k, z in (("a", x), ("b", y)):
                os.mkdir(os.path.join(d, k))
                chemin, s = executer.ecrire_lot(os.path.join(d, k), "T-imp", 1, 2, [z], ["e"])
                with open(chemin, "rb") as f:
                    h.append((f.read(), s))
        self.assertEqual(h[0], h[1])


if __name__ == "__main__":
    unittest.main()
