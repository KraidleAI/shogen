"""masque_fiv.py : masque des fenêtres évaluables (contrôle (b)), sortie et en-tête. Attendus écrits à la main,
empreintes par printf | sha256sum, dates par date -u ; chaque test nomme la mutation qui le rougit."""
import hashlib
import os
import time
import unittest
from collections import Counter

import masque_fiv
import socle
import tests

NL = chr(10)
T0 = 1787961000                 # vendredi 2026-08-28 23:50 UTC (date -u) ; samedi 00:00 = T0 + 600
CHAINE_SHA = "b262f67fd33ebb74df02c0cc80f19510630473a3ca03bf8bc62d15119208f147"   # printf ccccccccc----sss-sss
P3 = ("sous-arbres lus dans scripts/plan-s2bis/parametres.json : segment, strates, pool_d1bis, classes, episodes, fiv ;"
      " épingles : commit_analyse, harnais_sha256, rendu_j28, paquet_s2")
TETE = ("[MASQUE J28] positions j = (ws − t0)/w de la portée ; strate par jour UTC ; retenue = fenêtre retenue de la "
        "strate")


def h(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fixture(test, sc=1):
    """20 positions, vendredi 23:50 à samedi 00:09 UTC ; 9 et 16 absentes ; plage [10 ; 12] ; hôtes toujours ok."""
    ws = [T0 + 60 * i for i in range(20) if i not in (9, 16)]
    masque = {"calendrier_hors_d5": {"calme": 10, "stress": 7}, "sautees_hors_d5": {"calme": sc, "stress": 1}}
    argv = tests.banc(test, ws, lambda i, f: "ok", list("abcde"), plages=[(T0 + 600, T0 + 720)], masque=masque)
    return argv, argv[argv.index("--sortie") + 1]


def lire(dossier, nom):
    with open(os.path.join(dossier, nom), encoding="utf-8") as f:
        return f.read().split(NL)


class TestMasque(unittest.TestCase):
    def test_lacunes(self):
        """T-P2-MAS-1. Lacunes, comptes, chaîne et empreinte à la main ; 9 et [10 ; 12] : une lacune, sur deux strates.
        Mutation M-P2-04 : borne haute de la plage exclue ; M-P2-05 : lacunes contiguës non fusionnées ; M-P2R1-7 :
        plage exclue hors des lacunes ; M-P2R1-8 : calendrier compté plage comprise."""
        argv, s = fixture(self)
        self.assertEqual(masque_fiv.main(argv), 0)
        lignes = lire(s, "masque_j28.txt")
        self.assertIn(TETE, lignes)
        self.assertEqual(lignes[lignes.index(TETE) + 1:], [
            f"  portée : t0 = {T0} ; t_fin = {T0 + 1200} ; positions = 20 ; plage D5 : j = 10 à 12 (3 positions)",
            "  « calme » : calendrier hors D5 = 10 ; retenues = 9 ; sautées hors D5 = 1",
            "  « stress » : calendrier hors D5 = 7 ; retenues = 6 ; sautées hors D5 = 1",
            "  contrôle : retenues = n du bloc 3 ; sautées = ADR-0029 l.31 ; strate de chaque retenue = calendrier : "
            "égaux",
            "  empreinte : sha256 de la chaîne de 20 caractères (c calme retenue, s stress retenue, - non retenue) = "
            + CHAINE_SHA,
            "  lacunes : 2 suites maximales de positions non retenues, plage D5 comprise, en ordre croissant",
            "  lacune j = 9 à 12 : 4 positions (calme 1, stress 3)",
            "  lacune j = 16 à 16 : 1 positions (calme 0, stress 1)", ""])

    def test_portee_reelle(self):
        """T-P2-MAS-2. Bornes d'EP l.6 et D5 : 46 468 positions ; calendrier 32 068 et 14 400 ; D5 1 782 et 909
        (calc_p2.py, SB-10B l.148-161, date -u) ; heure locale UTC+9 (TZ = JST-9). Mutation M-P2-06 : jour pris en
        heure locale ; M-P2-07 : premier jour partiel ignoré."""
        avant = os.environ.get("TZ")
        self.addCleanup(time.tzset)
        self.addCleanup(lambda: os.environ.pop("TZ") if avant is None else os.environ.update(TZ=avant))
        os.environ["TZ"] = "JST-9"
        time.tzset()
        w = tests.fx.window
        pos = masque_fiv.portee((1787770800, 1790558880), 60, [(1790273880, 1790435280)], w.WEEKEND_STRATE_SPEC, w)
        tout, d5 = Counter(st for _ws, st, _x in pos), Counter(st for _ws, st, x in pos if x)
        self.assertEqual((len(pos), tout, d5),
                         (46468, {"calme": 32068, "stress": 14400}, {"calme": 1782, "stress": 909}))
        self.assertEqual({s: tout[s] - d5[s] for s in tout}, {"calme": 30286, "stress": 13491})

    def test_fail_closed(self):
        """T-P2-MAS-3. (b), un écart à la fois : retenues ≠ n du bloc 3 ; retenue exclue, d'une autre strate ou hors
        grille : P2/masque ; au script, sautées attendues fausses : code 1, aucune valeur. Mutation M-P2-08 : (b)
        retiré ; M-P2R1-9 : retenue exclue admise ; M-P2R1-10 : strate non comparée."""
        pos = [(0, "calme", False), (60, "calme", False), (120, "calme", True)]
        cas = (({0: "calme"}, 1, 1, None), ({0: "calme"}, 2, 1, "P2/masque"), ({0: "calme", 120: "calme"}, 2, 0,
               "P2/masque"), ({0: "stress"}, 1, 1, "P2/masque"), ({0: "calme", 30: "calme"}, 1, 1, "P2/masque"))
        for ret, n, sautees, code in cas:
            attendu = {"calendrier_hors_d5": {"calme": 2}, "sautees_hors_d5": {"calme": sautees}}
            args = (pos, masque_fiv.masque(pos, ret), ret, ["calme"], {"calme": [n, 0, "0"]}, attendu)
            try:
                self.assertEqual((masque_fiv.controle_b(*args), code), (None, None))
            except socle.Refus as e:
                self.assertEqual((e.code, code), ("P2/masque", "P2/masque"))
        argv, s = fixture(self, sc=2)
        self.assertEqual(masque_fiv.main(argv), 1)
        lignes = lire(s, "masque_j28.txt")
        self.assertEqual((lignes[-2][:17], lignes[-1], sum("[MASQUE" in x for x in lignes)),
                         ("REFUS P2/masque :", "", 0))

    def test_sortie(self):
        """T-P2-OUT-1. Étiquette mot pour mot ; sha256 de socle, masque_fiv, commun, regles, episodes, des deux
        parametres.json et d'EP ; ligne P-3 ; portée et pools à la main ; aucun .partiel. Mutation M-P2-19 : un module
        absent de l'en-tête."""
        argv, s = fixture(self)
        masque_fiv.main(argv)
        lignes, prm = lire(s, "masque_j28.txt"), socle.lire(argv[argv.index("--parametres") + 1])
        etiquette = "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)"
        self.assertEqual((lignes[0], tests.MODS["commun"].ETIQUETTE), (etiquette, etiquette))
        mods = [socle.__file__, masque_fiv.__file__] + [tests.CHEMINS[n] for n in ("commun", "regles", "episodes")]
        c = prm["plan_s2bis"]["chemins"]
        attendu = ["modules chargés : " + " ; ".join(f"{os.path.basename(q)} sha256 {h(q)}" for q in mods),
                   f"parametres.json du lot sha256 {h(argv[-1])} ; parametres.json de PLAN-S2BIS sha256 "
                   f"{h(c['parametres'])} ; EP episodes.txt sha256 {h(c['ep'])}",
                   P3.replace("scripts/plan-s2bis/parametres.json", c["parametres"])]
        self.assertEqual(lignes[2:5], attendu)
        for x in (f"portée : segment [{T0} ; {T0 + 1200}) (t0 = {T0}, n fixe = 18), plages exclues [({T0 + 600}, "
                  f"{T0 + 720})]", "pool S2 (D1) : « calme » 5 flux ; « stress » 5 flux ; retraits : aucun",
                  "pool D1-bis : « calme » 5 hôtes ; « stress » 5 hôtes ; retraits : aucun"):
            self.assertIn(x, lignes)
        self.assertEqual(sorted(os.listdir(s)), ["masque_j28.txt"])
