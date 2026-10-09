"""Cellules SB-11d et SB-11e (SHOGEN-SIM-BIS-SB11-BRIEF-1, L-2 et O-5 ; SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1, schéma
fermé et refus nommés) : attendus écrits à la main depuis la PROPOSITION, l'AVIS et EP ; chaque test nomme les
mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction

import calibration
import commun
import executer

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
F = Fraction
AS = ["bitfinex", "chainlink", "coinbase", "coingecko", "defillama", "kraken", "okx"]
POINTS = {"C1": {"calme": (F(1, 100), F(5), 60), "stress": (F(1, 50), F(10), 240)},
          "C2": {"calme": (F(1, 10), F(50), 4320), "stress": (F(1, 10), F(50), 1440)}}
N1 = {"nom": "N1", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [1, 4000],
      "derive": None, "incidents": None, "faibles": None,
      "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                 "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
      "regle": {"R": 9999, "classes": ["BTC", "ETH", "USDC", "USDT"], "S": False, "variante": [], "evenements": 0,
                "absorption": False},
      "surcharges": {}}


def cel(**k):
    """N1 retouchée : clés de premier niveau, ou « couche.x », « regle.x », remplacées."""
    c = copy.deepcopy(N1)
    for cle, v in k.items():
        a, _p, b = cle.partition("__")
        if b:
            c[a][b] = v
        else:
            c[a] = v
    return c


def code_de(f, *a):
    """Code du refus nommé levé par f(*a), nom de l'exception sinon, None sans exception (rouge d'assertion)."""
    try:
        f(*a)
    except commun.Refus as e:
        return e.code
    except Exception as e:                                          # noqa: BLE001 (rouge d'assertion, jamais d'erreur)
        return type(e).__name__
    return None


class TestCellules(unittest.TestCase):
    def test_couches_o_5(self):
        """O-5 de la G2 de la tranche 3 : grille de la couche d'observateurs portée par les cellules, dans
        parametres.json (cellules.couches), recopiée de Q-S-11 (a) (PROPOSITION l.537-538) et de l'AVIS (l.54, point
        large) : nominale 1/200, 1/200, paires 1/30 par jour, sans perte ; dégradée 1/50, 1/50, paires 1/7, perte ;
        large 1/20, 1/20, paires 1/7, perte, défaut local 1/1 000, artefacts 1/20 par jour ; source citée. Mutations
        M-11D-01 (grille dégradée à 1/100), M-11D-02 (perte nominale)."""
        g = PRM.get("cellules", {}).get("couches")
        z = [0, 1]
        self.assertEqual(g, {
            "nominale": {"absences": [1, 200], "degradations": [1, 200], "paires": [1, 30], "perte": False, "local": z,
                         "artefacts": z},
            "degradee": {"absences": [1, 50], "degradations": [1, 50], "paires": [1, 7], "perte": True, "local": z,
                         "artefacts": z},
            "large": {"absences": [1, 20], "degradations": [1, 20], "paires": [1, 7], "perte": True,
                      "local": [1, 1000], "artefacts": [1, 20]}})
        s = PRM.get("cellules", {}).get("source", "")
        self.assertTrue(all(x in s for x in ("PROPOSITION l.537-538", "AVIS.md l.54", "O-5")), s[:80])

    def test_couche_l_2(self):
        """L-2 (SB11-BRIEF-1) : la perte est tirée sur le W de la cellule, celui passé à calendrier.echelle (16), jamais
        sur T_max en semaines (24) ; nominale : aucune perte. Chemin de référence (1 − f)·p̂ : binance calme 7/10 ×
        372/24 585 ; facteur 1/10 : 7/100 × 372/24 585 ; fixe 3/10 000 partout. Surcharges de la cellule : repli,
        défaut local, artefacts, régionales, manques. Mutations M-11D-03 (T_max au lieu de W), M-11D-04 (chemin à f
        au lieu de 1 − f), M-11D-05 (grille ignorée), M-11D-06 (facteur ignoré)."""
        c = executer.couche(PRM, EP, cel(couche__grille="degradee"), 16)
        self.assertEqual((c["perte"], c["absences"], c["degradations"], c["paires"], c["repli"]),
                         (16, F(1, 50), F(1, 50), F(1, 7), False))
        self.assertEqual(c["chemin"]["binance", "calme"], F(7, 10) * F(372, 24585))
        self.assertIsNone(executer.couche(PRM, EP, N1, 16)["perte"])
        c = executer.couche(PRM, EP, cel(couche__chemin={"mode": "reference", "facteur": [1, 10]}), 16)
        self.assertEqual(c["chemin"]["binance", "calme"], F(7, 100) * F(372, 24585))
        c = executer.couche(PRM, EP, cel(couche__chemin={"mode": "fixe", "epsilon": [3, 10000]}, couche__repli=True,
                                         couche__local=[1, 1000], couche__artefacts=[1, 20],
                                         couche__regionale=[1, 5], couche__manque=[1, 4]), 16)
        self.assertEqual(set(c["chemin"].values()), {F(3, 10000)})
        self.assertEqual((c["repli"], c["local"], c["artefacts"], c["regionale"], c["manque"]),
                         (True, F(1, 1000), F(1, 20), F(1, 5), F(1, 4)))

    def test_fond(self):
        """Fond de sources.Replication : N1 à C1 (régime de la strate, points d'E1), f 3/10, hors-enveloppe 1/4 000 ;
        C0 : aucun régime ; cible (ρ = 1/10, D = 20 fixe, chacun des 7 hôtes AS13335 à 7/10) ; tendances sur W = 16
        semaines (161 280 fenêtres) ; deux unités faibles à 2/5, L = 1, panne : les deux premiers hôtes AS13335 ;
        partenaire imposé parmi elles. Mutations M-11D-07 (durée de dérive sur T_max), M-11D-08 (régime de C2 pour
        C1), M-11D-09 (unités faibles prises au pool)."""
        f = executer.fond(PRM, N1, POINTS, 16)
        self.assertEqual(f, {"f": F(3, 10), "regime": POINTS["C1"], "longues": 0, "autres": 1,
                             "hors_enveloppe": F(1, 4000), "derive": None, "incidents": None, "faibles": None})
        self.assertEqual(executer.fond(PRM, cel(niveau="C0"), {}, 16)["regime"], {"calme": None, "stress": None})
        inc = {"rho": [1, 10], "duree": 20, "geometrique": False, "mode": "chacun", "population": "as13335",
               "p": [7, 10]}
        f = executer.fond(PRM, cel(incidents=inc, derive=["tendances"]), POINTS, 16)
        self.assertEqual((f["incidents"], f["derive"]), (
            {"rho": F(1, 10), "duree": 20, "geometrique": False, "hotes": ("chacun", AS, F(7, 10))},
            {"genres": ["tendances"], "duree": 161280}))
        inc = dict(inc, mode="parmi", k=2, imposes="faibles")
        del inc["p"]
        f = executer.fond(PRM, cel(incidents=inc, faibles={"k": 2, "p": [2, 5], "L": 1, "type": "panne"}), POINTS, 16)
        self.assertEqual((f["faibles"], f["incidents"]["hotes"]), (
            {"hotes": AS[:2], "p": F(2, 5), "L": 1, "type": "panne"}, ("parmi", AS, 2, AS[:2])))

    def test_refus_nommes_o_1(self):
        """O-1 de la G2 de la tranche 2 (SB11-IMPRESSIONS-1) : unité faible à p = 1 ou L = 0, incident à ρ = 0, de mode
        inconnu ou de durée nulle, W nul (durée de dérive nulle), surcharge de longues sans poids_longues, clé en trop,
        niveau inconnu, C1 absent des points d'E1, grille de couche inconnue : refus nommés, jamais une autre
        exception. Mutations M-11D-10 (p = 1 admis), M-11D-11 (L = 0 admis), M-11D-12 (ρ = 0 admis), M-11D-13 (mode
        inconnu admis), M-11D-14 (longues sans poids admis)."""
        fa = {"k": 1, "p": [1, 1], "L": 1, "type": "panne"}
        inc = {"rho": [0, 1], "duree": 20, "geometrique": False, "mode": "chacun", "population": "as13335",
               "p": [7, 10]}
        cas = [(cel(faibles=fa), 16, "CELLULE/faible-p"),
               (cel(faibles=dict(fa, p=[2, 5], L=0)), 16, "CELLULE/faible-L"),
               (cel(incidents=inc), 16, "CELLULE/rho"), (cel(incidents=dict(inc, rho=[1, 10], mode="trois")), 16,
                                                         "CELLULE/incident-mode"),
               (cel(incidents=dict(inc, rho=[1, 10], duree=0)), 16, "CELLULE/incident-duree"),
               (cel(derive=["tendances"]), 0, "CELLULE/duree"),
               (cel(surcharges={"longues": [60, 1440]}), 16, "CELLULE/longues"),
               (dict(N1, autre=1), 16, "CELLULE/schema"), (cel(niveau="C3"), 16, "CELLULE/schema"),
               (cel(couche__grille="moyenne"), 16, "CELLULE/couche")]
        for c, w, code in cas:
            self.assertEqual(code_de(executer.cellule, PRM, EP, c, POINTS, w), code, code)
        self.assertEqual(code_de(executer.cellule, PRM, EP, N1, {"C2": POINTS["C2"]}, 16), "CELLULE/niveau")

    def test_l_2_au_site_d_appel(self):
        """C-4 de la G2 de SB-11 (L-2 au site d'appel) : executer.cellule passe à la couche le W de la cellule, celui de
        calendrier.echelle : perte 16 à W = 16 (T_max : 24 semaines), 2 à W = 2 ; chacun distinct de ⌊(W + 1)/2⌋ (8 et
        1). C-13 du contre-contrôle (E-S-13) : le même W passé au fond, durée de dérive W·tendance_par_semaine,
        161 280 fenêtres à W = 16 (test_fond), 20 160 à W = 2. Mutants G-06 (⌊(W + 1)/2⌋ passé à la couche par
        cellule), M-CC-05 (⌊(W + 1)/2⌋ passé au fond : 80 640 et 10 080)."""
        for w, duree in ((16, 161280), (2, 20160)):
            c = executer.cellule(PRM, EP, cel(couche__grille="degradee", derive=["tendances"]), POINTS, w)
            self.assertEqual((c["couche"]["perte"], c["fond"]["derive"]["duree"]), (w, duree))

    def test_schema_ferme_c_5(self):
        """C-5 de la G2 de SB-11 : sous PRM, où N1 passe le schéma (garde : None), et l'incident « parmi » à imposés
        « faibles » aussi quand la cellule a ses unités faibles : imposés « faibles » sans unité faible, classes sans
        BTC en tête ([ETH]) ou hors de l'ordre ([ETH, BTC] ; [BTC, USDT, ETH], BTC en tête, ordre seul en défaut, quand
        [BTC, ETH, USDT] passe : C-11 du contre-contrôle), f nul : CELLULE/schema. Mutants G-07 (imposés « faibles »
        admis sans unité faible), G-08 (BTC en tête non exigé), G-19 (f nul admis), M-CC-09 (ordre non exigé)."""
        inc = {"rho": [1, 10], "duree": 20, "geometrique": False, "mode": "parmi", "population": "as13335", "k": 2,
               "imposes": "faibles"}
        fa = {"k": 2, "p": [2, 5], "L": 1, "type": "panne"}
        for c in (N1, cel(incidents=inc, faibles=fa), cel(regle__classes=["BTC", "ETH", "USDT"])):
            self.assertIsNone(code_de(executer.cellule, PRM, EP, c, POINTS, 16))
        for c in (cel(incidents=inc), cel(regle__classes=["ETH"]), cel(regle__classes=["ETH", "BTC"]),
                  cel(regle__classes=["BTC", "USDT", "ETH"]), cel(f=[0, 1])):
            self.assertEqual(code_de(executer.cellule, PRM, EP, c, POINTS, 16), "CELLULE/schema", (c["f"], c["regle"]))

    def test_surcharges_longues(self):
        """SB11-IMPRESSIONS-1 : une surcharge de sources.longues surcharge sources.poids_longues ; le prm de la cellule
        les porte, celui du lot reste intact. Mutation M-11D-15 (surcharge appliquée au prm du lot)."""
        s = {"longues": [60, 1440], "poids_longues": [2, 1]}
        p = executer.cellule(PRM, EP, cel(surcharges=s), POINTS, 16)["prm"]
        self.assertEqual((p["sources"]["longues"], p["sources"]["poids_longues"]), ([60, 1440], [2, 1]))
        self.assertEqual((PRM["sources"]["longues"], PRM["sources"]["poids_longues"]), ([60, 1440, 4320], [1, 1, 1]))


if __name__ == "__main__":
    unittest.main()
