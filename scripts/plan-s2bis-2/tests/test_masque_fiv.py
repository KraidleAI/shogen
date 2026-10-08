"""masque_fiv.py : masque des fenêtres évaluables (contrôle (b)), sortie et en-tête. Attendus écrits à la main,
empreintes par printf | sha256sum, dates par date -u ; chaque test nomme la mutation qui le rougit."""
import hashlib
import os
import time
import unittest
from collections import Counter
from decimal import Decimal

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


def fixture_fiv(test, modif_ep=None):
    """Forme de PS2 tests/test_episodes.py l.57-66 : 10 fenêtres de calme, la 5 exclue (n = 9) ; a en panne en 0, 4,
    6, 9 et périmée en 1 (ok 5 fois, gardé) ; b en panne en 0 ; x hors des unités, en panne sauf en 8."""
    ws = [tests.fx.VEN + 60 * i for i in range(10)]

    def motif(i, f):
        if (f == "a" and i in (0, 4, 6, 9)) or (f == "b" and i == 0) or (f == "x" and i != 8):
            return "panne_transport"
        return {"etat": "ok", "age": 200} if f == "a" and i == 1 else "ok"
    masque = {"calendrier_hors_d5": {"calme": 9}, "sautees_hors_d5": {"calme": 0}}
    argv = tests.banc(test, ws, motif, list("abcde"), pool=list("abcdex"), plages=[(ws[5], ws[5])], masque=masque,
                      sigma={"place": "100"}, strates=["calme"], modif_ep=modif_ep)
    return argv, argv[argv.index("--sortie") + 1]


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
        grille ; un des deux comptes attendus sans une strate de PLAN-S2BIS (C-3 c de la G2) : P2/masque ; au script,
        sautées attendues fausses : code 1, aucune valeur. Mutation M-P2-08 : (b) retiré ; M-P2R1-9 : retenue exclue
        admise ; M-P2R1-10 : strate non comparée ; G-14 (G2, adapté) : strate absente admise ; M-P2R6-16 : strates des
        deux comptes réunies ; M-P2R6-17 : calendrier seul contrôlé."""
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
        for attendu in ({"calendrier_hors_d5": {"calme": 2}, "sautees_hors_d5": {}},
                        {"calendrier_hors_d5": {}, "sautees_hors_d5": {"calme": 1}}):
            try:
                obtenu = masque_fiv.controle_b(pos, masque_fiv.masque(pos, {0: "calme"}), {0: "calme"}, ["calme"],
                                               {"calme": [1, 0, "0"]}, attendu)
            except Exception as e:
                obtenu = getattr(e, "code", type(e).__name__)
            self.assertEqual(obtenu, "P2/masque")
        argv, s = fixture(self, sc=2)
        self.assertEqual(masque_fiv.main(argv), 1)
        self.assertRefus(s, "P2/masque")

    def assertRefus(self, s, code):
        """Chaque sortie du script : une ligne de refus en dernier, aucune section de valeurs."""
        for nom in masque_fiv.SORTIES:
            lignes = lire(s, nom)
            self.assertEqual((lignes[-2].split(" : ")[0], lignes[-1], [x[:1] for x in lignes].count("[")),
                             (f"REFUS {code}", "", 0))

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
        self.assertEqual(sorted(os.listdir(s)), ["fiv_unites.txt", "masque_j28.txt"])

    def test_contre_ep(self):
        """T-P2-FIV-5. Fixture de FIV (a : 5 cellules d'écart, 4 de panne [calc]) ; EP produit par episodes.main
        épinglé : (c) et (f) égaux, code 0 ; EP altéré d'un chiffre (cellules d'écart de a ; K de la courbe D1-bis à
        ℓ = 2 ; dernier chiffre de σ̂²_bloc de la ligne D1-bis à ℓ = 3), ou portant une ligne D1-bis de plus : P2/ep,
        code 1, aucune valeur dans les deux sorties (lettre de (f) : EP l.128-161, chaîne pour chaîne). Mutation
        M-P2-13 : contrôle (f) neutralisé ; M-P2-32 : FIV_u sur le type panne ; M-P2R2-1 : (f) (ii) non comparée ;
        G-18 (G2) : n et K seuls comparés ; G-19 (G2) : compte des lignes D1-bis retiré ; M-P2R2-4 : chaînes comparées
        jusqu'à FIV_série ; M-P2R2-5 : lignes D1-bis en trop admises."""
        argv, s = fixture_fiv(self)
        self.assertEqual(masque_fiv.main(argv), 0)

        def remplacer(a, b):
            def alterer(texte):
                self.assertIn(a, texte)
                return texte.replace(a, b)
            return alterer

        def chiffre(texte):
            x = next(y for y in texte.split(NL) if y.startswith("  D1-bis « calme » ℓ = 3 : "))
            u, v = x.split(" ; γ̂₀ = ")
            return texte.replace(x, f"{u[:-1]}{(int(u[-1]) + 1) % 10} ; γ̂₀ = {v}")

        def de_plus(texte):
            return texte + [y for y in texte.split(NL) if y.startswith("  D1-bis « ")][-1] + NL
        a, k = "(hôte ua) ecart : n_s = 9 ; cellules = ", "D1-bis « calme » ℓ = 2 : n = 9 ; K = "
        for alterer in (remplacer(a + "5 ;", a + "6 ;"), remplacer(k + "1 ;", k + "2 ;"), chiffre, de_plus):
            argv, s = fixture_fiv(self, alterer)
            self.assertEqual(masque_fiv.main(argv), 1)
            self.assertRefus(s, "P2/ep")

    def test_contre_courbe(self):
        """T-P2-FIV-6. À la main (convention de PS2 tests/test_episodes.py l.36-44 ; SB-10A l.128-134) : positions 0, 1,
        3, 4, D = 1, 1, ·, 0, 0 : FIV_série(2) = FIV_série(3) = 3/2. Section [FIV_u(ℓ)] de la fixture de FIV = lignes
        construites ici par episodes.courbe épinglé sur les séries écrites à la main (positions réelles, fenêtre exclue
        absente), dans l'ordre des hôtes puis de ℓ. Mutation M-P2-10 : série comprimée (positions renumérotées)."""
        courbe, dec, v = tests.MODS["episodes"].courbe, tests.MODS["commun"].dec, tests.fx.VEN
        quatre = [(v, 1), (v + 60, 1), (v + 180, 0), (v + 240, 0)]
        self.assertEqual([c["FIV_serie"] for c in courbe(quatre, 60, [2, 3])], [Decimal("1.5")] * 2)
        argv, s = fixture_fiv(self)
        masque_fiv.main(argv)
        lignes = lire(s, "fiv_unites.txt")
        uns = {"a": (0, 1, 4, 6, 9), "b": (0,), "c": (), "d": (), "e": ()}
        attendu = [f"  « calme » {f} (hôte u{f}) ℓ = {c['ell']} : n = 9 ; K = {c['K']} ; FIV_série = "
                   f"{dec(c['FIV_serie'])} ; σ̂²_bloc = {dec(c['sigma2_bloc'])} ; γ̂₀ = {dec(c['gamma0'])} ; "
                   f"cv théorique = {dec(c['cv'])} ; garde : non tenue" for f in "abcde"
                   for c in courbe([(v + 60 * i, int(i in uns[f])) for i in range(10) if i != 5], 60, [1, 2, 3])]
        i = next(j for j, x in enumerate(lignes) if x.startswith("[FIV_u(ℓ)]"))
        self.assertEqual(lignes[i + 2:i + 17], attendu)
        self.assertTrue(lignes[i + 17].startswith("[SENSIBILITÉ VOISINAGE]"))

    def test_voisinage(self):
        """T-P2-VOI-1. Série à la main, positions 0 à 9, la 5 absente : d = 1 retire 0 et 9 (bords de la portée), 4 et 6
        (voisines de la lacune). Fixture de FIV : positions retirées 4, n′ = 5 ; K − K′ : ua 4 (K = 5, K′ = 1, la
        cellule périmée en 1), ub 1, uc, ud, ue 0 ; lignes des séries réduites à n = 5. Mutation M-P2-33 : bords de la
        portée non comptés comme lacunes ; M-P2R2-2 : séries réduites non imprimées (séries entières)."""
        serie = [(60 * i, int(i in (0, 1, 4, 6, 9))) for i in range(10) if i != 5]
        self.assertEqual(masque_fiv.reduite(serie, 60, 1), [(60, 1), (120, 0), (180, 0), (420, 0), (480, 0)])
        argv, s = fixture_fiv(self)
        masque_fiv.main(argv)
        lignes = lire(s, "fiv_unites.txt")
        i = next(j for j, x in enumerate(lignes) if x.startswith("[SENSIBILITÉ VOISINAGE]"))
        self.assertEqual(lignes[i + 1], "  « calme » : positions retirées = 4 ; n′ = 5 ; cellules d'écart voisines "
                                        "d'une lacune (K − K′) : ua 4 ; ub 1 ; uc 0 ; ud 0 ; ue 0")
        self.assertEqual([x.split(" ; ")[:2] for x in lignes[i + 2:-1]],
                         [[f"  « calme » {f} (hôte u{f}) ℓ = {ell} : n = 5", f"K = {int(f == 'a')}"] for f in "abcde"
                          for ell in (1, 2, 3)])
