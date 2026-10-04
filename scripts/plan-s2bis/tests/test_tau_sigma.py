"""TAU-SIGMA-S2BIS : population de l'axe (i) sur le pool D1-bis, P99,9 et maximum sur les strates ; σ sur deux
populations, celle de la règle de clôture au paquet (adjudication A-1), celle de l'axe (i) descriptive ; refus nommé à
la borne haute de τ (A-2). Attendus écrits à la main ; chaque test nomme la mutation qui le rougit."""
import os
import unittest
from decimal import Decimal, localcontext

import commun
import regles
import tau_sigma
from tests import fixtures as fx

POOL = list("abcdefx")                    # x : flux du pool S2 hors des unités D1-bis (comme okx_index)
CLASSES = {"a": "place", "b": "place", "c": "place", "x": "place", "d": "agr", "e": "agr", "f": "sans"}
PRIX = {  # fenêtre : {flux : (état, prix, âge)} ; défaut (ok, 1000, 10) ; f sans horodatage ; x toujours à 1100
    0: {"e": ("ok", "1002", 10), "c": ("ok", "1000", 20)},           # vendredi : calme
    1: {"c": ("ok", "1001", 10)},
    2: {"a": ("panne_transport", None, 10)},                         # a en panne : hors des deux populations
    3: {"a": ("ok", "1100", 200)},                                   # a périmé (200 s > σ de S2 100 s) : (B) seule
    4: {"c": None, "d": None, "f": None, "e": ("ok", "1500", 10)},   # 3 répondantes D1-bis : non évaluable, (B) seule
    5: {"b": ("ok", "1004", 10), "d": ("ok", "1000", 50)},           # samedi : stress
    6: {},
}


def motif(i, f):
    e = PRIX[i].get(f, ("ok", "1100" if f == "x" else "1000", 10))
    if e is None:
        return None
    etat, prix, age = e
    return {"etat": etat, "prix": prix, "age": None if f == "f" else age}


def journaux(d):
    ws = [fx.VEN + 60 * i for i in range(5)] + [fx.VEN + 86400 + 60 * i for i in range(2)]
    fx.journaux(d, ws, motif, POOL, CLASSES, {"place": "100", "agr": "1000", "sans": None},
                {"place": "0.5", "agr": "0.5", "sans": "0.5"})
    return ws


def prm(ws, bloc3, sha):
    p = fx.prm_fixture(list("abcdef"), bloc3, sha, ws[0], 7)
    p["classes"] = {f: CLASSES[f] for f in "abcdef"}
    p["sigma"] = dict(p["sigma"], planchers_s={"place": 30, "agr": 300, "sans": None})
    return p


class TestTauSigma(unittest.TestCase):
    def setUp(self):
        self.d = fx.dossier(self, "plan_tau_")

    def test_population_axe_i_et_cloture_sur_le_pool_d1bis(self):
        """(rapports et staleness de l'axe (i) (A), staleness de clôture (B)) par (classe, strate), à la main. (A) : place
        calme 9 × 0 et 0,001, staleness 9 × 10 et 20 ; agr calme 7 × 0 et 0,002 ; place stress 5 × 0 et 0,004 ; agr stress
        10, 10, 10, 50. (B), répondantes horodatées, périmée et non évaluables comprises : place calme 11 × 10, 20 et 200 ;
        agr calme 9 × 10 ; sans : aucune ; x absent. Mutation MT-1 : cellules périmées admises à l'axe (i) ; MT-10 : (B)
        réduite aux cellules de l'axe (i)."""
        ws = journaux(self.d)
        d = commun.charger(self.d, prm(ws, {}, "-"))
        pops = tau_sigma.populations(commun.classer(d, d["pools_bis"]), d)
        z, D = Decimal(0), Decimal
        attendu = {("place", "calme"): ([z] * 9 + [D("0.001")], [D(10)] * 9 + [D(20)], [D(10)] * 11 + [D(20), D(200)]),
                   ("place", "stress"): ([z] * 5 + [D("0.004")], [D(10)] * 6, [D(10)] * 6),
                   ("agr", "calme"): ([z] * 7 + [D("0.002")], [D(10)] * 8, [D(10)] * 9),
                   ("agr", "stress"): ([z] * 4, [D(10)] * 3 + [D(50)], [D(10)] * 3 + [D(50)]),
                   ("sans", "calme"): ([z] * 4, [], []), ("sans", "stress"): ([z] * 2, [], [])}
        self.assertEqual({k: tuple(sorted(x) for x in v) for k, v in pops.items()}, attendu)

    def test_regle_p999_maximum_et_deux_populations_de_sigma(self):
        """Calme : 999 rapports à 0,001 et un à 0,02 (P99,9 : 0,001 ; maximum 0,02) ; stress : 0,002. τ = 0,0030 ; règle au
        maximum 0,03 ≥ 0,0285 : REFUS, valeur de la règle 0,0300. (B) : calme 100 × 20 s et une à 1 000 s (P99 au rang
        100 : 20), stress 25 s : σ = max(30, 75) = 75 ; (A) : calme 100 × 20 s : σ = 60. σ de S2 25 s : au-delà 1 en calme,
        0 en stress (25 n'est pas au-delà). Mutation MT-3 : τ au maximum ; MT-4 : stress ignorée pour τ ; MT-5 : σ sur la
        première strate seule (60) ; MT-6 : σ au maximum (3 000) ; MT-9 : « au-delà » compté avec ≥."""
        D = Decimal
        pops = {("place", "calme"): ([D("0.001")] * 999 + [D("0.02")], [D(20)] * 100, [D(20)] * 100 + [D(1000)]),
                ("place", "stress"): ([D("0.002")], [], [D(25)])}
        v = tau_sigma.regle(pops, prm([0], {}, "-"), ["place"], {"place": D(25)})["place"]
        self.assertEqual((v["tau"], v["sigma_cloture"], v["sigma_axe_i"]),
                         ((D("0.0030"), None, D("0.0030")), (D(75), None), (D(60), None)))
        self.assertEqual((v["tau_max"][0], v["tau_max"][1].startswith("REFUS"), v["tau_max"][2]), (None, True, D("0.03")))
        self.assertEqual((v["strates"]["calme"]["p999"], v["strates"]["calme"]["max"]), (D("0.001"), D("0.02")))
        self.assertEqual([v["strates"][s]["au_dela"] for s in ("calme", "stress")], [1, 0])

    def test_p999_distinct_du_p99(self):
        """990 rapports à 0,001 puis 10 à 0,003 : P99 (rang 990) = 0,001 ; P99,9 (rang 999) = 0,003 ; τ = grid-ceil(1,5 ×
        0,003) = 0,0045 (au P99 : 0,0015). Prototype P-1 du réviseur. Mutation RV-01 : quantile de parametres.json à
        [99, 100] ; RV-02 : P99 dans le code."""
        D = Decimal
        v = tau_sigma.regle({("place", "calme"): ([D("0.001")] * 990 + [D("0.003")] * 10, [], [])}, prm([0], {}, "-"),
                            ["place"], {})["place"]
        self.assertEqual((v["strates"]["calme"]["p999"], v["strates"]["calme"]["p99"]), (D("0.003"), D("0.001")))
        self.assertEqual(v["tau"], (D("0.0045"), None, D("0.0045")))

    def test_mediane_des_rapports_sur_le_pool_d1bis(self):
        """Une fenêtre : a, b, c à 1000, d, e à 1010 (unités D1-bis), x à 1100 (pool S2 seul). À la main : a, b, c :
        |1000 − 1005|/1005 = 5/1005 ; d, e : 10/1000 ; avec x dans la médiane, a, b, c donneraient 10/1010. Prototype P-2
        du réviseur. Mutation RV-22 : répondantes du rapport prises au pool S2."""
        prix = {"a": "1000", "b": "1000", "c": "1000", "d": "1010", "e": "1010", "x": "1100"}
        fx.journaux(self.d, [fx.VEN], lambda i, f: {"etat": "ok", "prix": prix[f]}, list("abcdex"))
        d = commun.charger(self.d, fx.prm_fixture(list("abcde"), {}, "-", fx.VEN, 1))
        r = tau_sigma.populations(commun.classer(d, d["pools_bis"]), d)[("place", "calme")][0]
        with localcontext(fx.r1.contexte_decimal()):
            cinq, dix = Decimal(5) / Decimal(1005), Decimal(10) / Decimal(1000)
        self.assertEqual(sorted(r), [cinq] * 3 + [dix] * 2)

    def test_refus_a_la_borne_haute(self):
        """1,5 × P99,9 = 1,5 × 0,02 = 0,03 ≥ 0,0285 : la ligne du paquet porte REFUS et la valeur de la règle 0.0300,
        jamais 0.0280 (A-2) ; classe sans cellule : « - ». Mutation MR-5 : écrêtage au lieu du refus."""
        D, p = Decimal, prm([0], {}, "-")
        v = tau_sigma.regle({("place", "calme"): ([D("0.02")], [], [D(10)]), ("agr", "calme"): ([D("0.001")], [], [])},
                            p, ["agr", "place", "sans"], {})
        self.assertEqual(tau_sigma.valeurs_paquet(v, ["agr", "place", "sans"], p),
                         ["tau agr 0.0015", "tau place REFUS 0.0300 (valeur de la règle, ≥ borne haute exclue 0.0285)",
                          "tau sans - (aucune cellule)", "sigma agr 300", "sigma place 30", "sigma sans aucun"])

    def test_sortie_valeurs_pour_le_paquet(self):
        """Fixture complète : calme n = 5, K = 1 (5e fenêtre : c, d, f absentes), p̂ = (2/5, 0, 1/5, 1/5, 0, 1/5, 0),
        P̂_more = 161/625 = 0,2576 ; stress n = 2, K = 0, P̂_more = 0 (à la main). τ place = grid-ceil(1,5 × 0,004) =
        0,0060, agr 0,0030, sans 0 → borne basse 0,0005. σ au paquet (clôture) : place max(30, 3 × 200) = 600, agr
        max(300, 150) = 300, sans aucun ; σ de l'axe (i), descriptif : place 60 ; au-delà du σ de S2 en place calme : 1.
        En-tête : sha256 de regles.py. Mutation MT-2 : analyse classée sur le pool S2 ; MT-7 : τ committés de S2 au
        paquet ; MT-8 : σ du paquet pris à l'axe (i) (60) ; MC-13 : regles.py absent de l'en-tête."""
        ws = journaux(self.d)
        b3 = {"calme": (5, 1, "0.2576"), "stress": (2, 0, "0")}
        r = fx.rendu(os.path.join(self.d, "r.out"), b3)
        p = fx.ecrire_prm(os.path.join(self.d, "p.json"), prm(ws, b3, commun.sha256(r)))
        s = os.path.join(self.d, "s.txt")
        rc = tau_sigma.main(["--journaux", self.d, "--harnais", fx.HARNAIS, "--sortie", s, "--parametres", p, "--rendu", r])
        with open(s, encoding="utf-8") as f:
            lignes = f.read().split(fx.NL)
        machine = lignes[lignes.index("[VALEURS POUR LE PAQUET DE S2-BIS]") + 1:]
        self.assertEqual((rc, lignes[0]), (0, commun.ETIQUETTE))
        self.assertEqual(machine, ["tau agr 0.0030", "tau place 0.0060", "tau sans 0.0005", "sigma agr 300",
                                   "sigma place 600", "sigma sans aucun", ""])
        self.assertIn(f"regles.py sha256 {commun.sha256(regles.__file__)}", lignes[2])
        for debut in ("  τ_c = 0.0005", "  σ, population (A) de l'axe (i) (descriptif, hors paquet) = 60 s",
                      "  « calme » staleness : population (B) de clôture N = 13, au-delà du σ de S2 1, P99 = 200 s ;",
                      "limite écrite : population (A) censurée à σ_S2 : σ_c ≤ max(plancher, 3 × σ_S2) par construction"):
            self.assertTrue(any(x.startswith(debut) for x in lignes), debut)


if __name__ == "__main__":
    unittest.main()
