"""Exécution SB-11 (E-S-40 à E-S-48, E-S-52) : attendus écrits à la main ou produits par un outil distinct (`bc -l`,
`sha256sum`) ; chaque test nomme les mutations qui le rougissent."""
import hashlib
import json
import os
import tempfile
import time
import unittest
from decimal import Decimal
from fractions import Fraction

import commun
import executer

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]


def code_de(f, *a):
    """Code du refus nommé levé par f(*a), nom de l'exception sinon, None sans exception (rouge d'assertion)."""
    try:
        f(*a)
    except commun.Refus as e:
        return e.code
    except Exception as e:                                          # noqa: BLE001 (rouge d'assertion, jamais d'erreur)
        return type(e).__name__
    return None


class TestTaux(unittest.TestCase):
    def test_taux_e_s_40(self):
        """E-S-40 : x = 122 sur 10⁴ : r̂ = 61/5 000, SE = √(122·9 878/10¹²) (bc -l, à 10⁻⁵² près : 50 chiffres sous le
        contexte de r1), aucune borne ; x = 0 sur 10⁴ : SE nulle, borne 1 − 0,05^(1/10⁴) (bc -l :
        1 - e(l(0.05)/10000), à 10⁻⁴⁸ près) ; x = 1 sur 100 : SE = √(99/10⁶) ; x = R : SE nulle, aucune borne.
        Mutations M-11A-06 (SE sans racine), M-11A-07 (R − 1 au dénominateur), M-11A-08 (borne quand x > 0), M-11A-09
        (borne 1 − 0,05^R), M-11A-10 (contexte par défaut, 28 chiffres)."""
        se = Decimal("0.0010977777552856497920739905119903281276065317669013518111719989972695")
        t = executer.taux(122, 10000, K_)
        self.assertEqual((t["x"], t["R"], t["r"], t["borne"]), (122, 10000, Fraction(61, 5000), None))
        self.assertLess(abs(t["SE"] - se), Decimal("1E-52"))
        b = Decimal("0.0002995283597766120092834713389476236471831496972729805716154849335380")
        t = executer.taux(0, 10000, K_)
        self.assertEqual((t["r"], t["SE"]), (0, 0))
        self.assertLess(abs(t["borne"] - b), Decimal("1E-48"))
        se = Decimal("0.0099498743710661995473447982100120600517812656367680607911760464383494")
        self.assertLess(abs(executer.taux(1, 100, K_)["SE"] - se), Decimal("1E-52"))
        t = executer.taux(7, 7, K_)
        self.assertEqual((t["r"], t["SE"], t["borne"]), (1, 0, None))

    def test_borne_a_2000(self):
        """Borne à R = 2 000 (familles secondaires, Q-S-06) : 1 − 0,05^(1/2 000) (bc -l, à 10⁻⁴⁸ près). Mutation
        M-11A-09 (borne 1 − 0,05^R)."""
        b = Decimal("0.0014967448951882842161127126443267129932794737843594269185378142370390")
        x = executer.taux(0, 2000, K_)
        self.assertIsInstance(x["borne"], Decimal)
        self.assertLess(abs(x["borne"] - b), Decimal("1E-48"))

    def test_taux_refus(self):
        """x < 0, x > R, R = 0, booléen, R en Fraction : EXEC/taux, jamais une autre exception. Mutation M-11A-11
        (contrôle retiré)."""
        for x, r in ((-1, 10), (11, 10), (0, 0), (True, 10), (1, Fraction(10))):
            self.assertEqual(code_de(executer.taux, x, r, K_), "EXEC/taux", (x, r))


class TestFrequences(unittest.TestCase):
    R6 = [{"valeur": "REJETTE", "causes": []}, {"valeur": "NE REJETTE PAS", "causes": []},
          {"valeur": "NON ÉVALUABLE", "causes": ["unites", "k_crit", "runs"]},
          {"valeur": "NON ÉVALUABLE", "causes": ["k_crit", "runs"]}, {"valeur": "NON ÉVALUABLE", "causes": ["n_prime"]},
          {"valeur": "NON ÉVALUABLE", "causes": ["k_crit", "runs"]}]

    def test_frequences_e_s_52(self):
        """E-S-52 et AVIS-SIM-T3, observation 3 : six résultats écrits à la main ; valeurs 1, 1, 4 ; causes (non
        exclusives) unites 1, k_crit 3, runs 3, n_prime 1 ; information insuffisante (unites, k_crit ou runs) 3 ;
        combinaisons « unites+k_crit+runs » 1, « k_crit+runs » 2, « n_prime » 1, de somme 4, le compte de NON
        ÉVALUABLE. Mutations M-11A-12 (combinaisons omises), M-11A-13 (n_prime compté en information insuffisante),
        M-11A-14 (première cause seule comptée). C-2 de la G2 de SB-11 : une NON ÉVALUABLE de causes unites, k_crit,
        runs et n_prime (regle.tester à n′_s = 1) compte en information insuffisante : 4 sur 7. Mutant G-01 (toutes
        les causes exigées parmi unites, k_crit, runs)."""
        f = executer.frequences(self.R6)
        self.assertEqual(f, {"valeurs": {"REJETTE": 1, "NE REJETTE PAS": 1, "NON ÉVALUABLE": 4},
                             "causes": {"unites": 1, "k_crit": 3, "runs": 3, "n_prime": 1}, "insuffisante": 3,
                             "combinaisons": {"unites+k_crit+runs": 1, "k_crit+runs": 2, "n_prime": 1}})
        self.assertEqual(sum(f["combinaisons"].values()), f["valeurs"]["NON ÉVALUABLE"])
        mixte = {"valeur": "NON ÉVALUABLE", "causes": ["unites", "k_crit", "runs", "n_prime"]}
        f = executer.frequences(self.R6 + [mixte])
        self.assertEqual((f["insuffisante"], f["causes"]["n_prime"], f["combinaisons"]["unites+k_crit+runs+n_prime"]),
                         (4, 2, 1))

    def test_frequences_refus(self):
        """« NON TESTÉ (séquence) » (présentation de regle.strate, non une valeur du moteur), cause inconnue, causes
        dans le désordre ou en double, NON ÉVALUABLE sans cause, REJETTE avec une cause : EXEC/frequences. Mutation
        M-11A-15 (contrôle retiré)."""
        for v, c in (("NON TESTÉ (séquence)", []), ("NON ÉVALUABLE", ["garde"]), ("NON ÉVALUABLE", ["runs", "k_crit"]),
                     ("NON ÉVALUABLE", ["runs", "runs"]), ("NON ÉVALUABLE", []), ("REJETTE", ["runs"])):
            self.assertEqual(code_de(executer.frequences, self.R6 + [{"valeur": v, "causes": c}]), "EXEC/frequences",
                             (v, c))


def lent(k: int, n: int) -> int:
    """Tâche de test : rend k après (n − k)·50 ms, d'où un achèvement dans l'ordre inverse des tâches."""
    time.sleep((n - k) * 0.05)
    return k


def pid(k: int) -> int:
    """Tâche de test : numéro du processus qui l'exécute."""
    return os.getpid()


R2 = [{"i": 0, "x": Fraction(1, 3), "d": Decimal("0.5"), "t": (1, 2)}, {"i": 1, "x": Fraction(2), "d": None, "t": []}]


class TestLots(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.r = d.name

    def test_empreinte_e_s_44(self):
        """E-S-44 : sha256 de la suite ordonnée des enregistrements, JSON canonique d'une ligne chacun : Fraction en
        « num/den », Decimal en chaîne, tuple en liste ; attendu par echo | sha256sum (c4a6d8b4…). Mutations M-11B-01
        (ordre des enregistrements perdu), M-11B-02 (Fraction écrite autrement)."""
        self.assertEqual(executer.empreinte(R2), "c4a6d8b4f33a2487e1e7951af1da654f8d50f7064a1121a1de40deb5bece3afb")
        self.assertNotEqual(executer.empreinte(R2[::-1]), executer.empreinte(R2))

    def test_lot_octets(self):
        """E-S-45, E-S-05, E-S-06 : lot (N1, [0, 1)), entête ["e"] : étiquette en première ligne, puis le JSON canonique
        écrit à la main ; nom N1.000000-000001.lot ; sha256 rendu = echo | sha256sum (ccf13dfc…) ; réécriture :
        SORTIE/existe ; lot perdu, puis refait : mêmes octets. Mutations M-11B-03 (étiquette absente), M-11B-04
        (extension .jsonl)."""
        c, h = executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0}], ["e"])
        h0 = "ccf13dfc9e5665f73fa08c0f64dbcb47c1267e0f28afcb1502c6972d3fc9d6b8"
        self.assertEqual((os.path.basename(c), h), ("N1.000000-000001.lot", h0))
        with open(c, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), h)
        self.assertEqual(code_de(executer.ecrire_lot, self.r, "N1", 0, 1, [{"i": 0}], ["e"]), "SORTIE/existe")
        os.unlink(c)
        self.assertEqual(executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0}], ["e"]), (c, h))

    def test_lots_couverture(self):
        """E-S-45 : chaque i de [0, R) une fois et une seule. Lots [0, 2) et [2, 4) : quatre enregistrements dans
        l'ordre, ceux de N10 ignorés ; [2, 4) retiré : LOT/manquant ; [1, 3) ajouté : LOT/double ; R = 3 : LOT/surplus ;
        trou au milieu ([0, 2) et [3, 4)) : LOT/manquant ; dossier vide : LOT/manquant. Mutations M-11B-05 (trou
        admis), M-11B-06 (recouvrement admis), M-11B-07 (cellule par préfixe sans point)."""
        for a, b in ((0, 2), (2, 4)):
            executer.ecrire_lot(self.r, "N1", a, b, [{"i": i, "v": 10 * i} for i in range(a, b)], ["e"])
        executer.ecrire_lot(self.r, "N10", 0, 1, [{"i": 0, "v": 99}], ["e"])
        self.assertEqual([x["v"] for x in executer.lire_lots(self.r, "N1", 4, ["e"])], [0, 10, 20, 30])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 3, ["e"]), "LOT/surplus")
        executer.ecrire_lot(self.r, "N1", 1, 3, [{"i": i, "v": 10 * i} for i in (1, 2)], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/double")
        for n in ("N1.000001-000003.lot", "N1.000002-000004.lot"):
            os.unlink(os.path.join(self.r, n))
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/manquant")
        executer.ecrire_lot(self.r, "N1", 3, 4, [{"i": 3, "v": 30}], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/manquant")
        self.assertEqual(code_de(executer.lire_lots, self.r, "X1", 1, ["e"]), "LOT/manquant")

    def test_lot_forme(self):
        """Entête différente : LOT/entete ; enregistrement retouché (empreinte), étiquette retouchée, JSON non
        canonique : LOT/forme ; i hors de la plage, plage vide, nom de cellule à « / » ou à « . » : LOT/indices ou
        LOT/nom. Mutations M-11B-08 (empreinte non recalculée), M-11B-09 (entête non comparée), M-11B-10 (forme
        canonique non exigée). C-3 de la G2 de SB-11 : lot dont les i sont permutés, empreinte recalculée sur
        l'ordre permuté, JSON canonique : LOT/forme. Mutant G-03 (i des enregistrements non contrôlés)."""
        c, _h = executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0, "v": 1}], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 1, ["autre"]), "LOT/entete")
        with open(c, "rb") as f:
            o = f.read()
        for avant, apres in ((b'"v":1', b'"v":2'), (b"synth", b"Synth"), (b'"fin":1', b'"fin": 1')):
            with open(c, "wb") as f:
                f.write(o.replace(avant, apres))
            self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 1, ["e"]), "LOT/forme", apres)
        c, _h = executer.ecrire_lot(self.r, "N3", 0, 2, [{"i": 0, "v": 0}, {"i": 1, "v": 1}], ["e"])
        with open(c, "rb") as f:
            tete, nl, corps = f.read().partition(commun.NL.encode("utf-8"))
        o = json.loads(corps)
        o["enregistrements"] = [{"i": 1, "v": 0}, {"i": 0, "v": 1}]
        o["empreinte"] = executer.empreinte(o["enregistrements"])
        with open(c, "wb") as f:
            f.write(tete + nl + commun.json_canonique(o))
        self.assertEqual(code_de(executer.lire_lots, self.r, "N3", 2, ["e"]), "LOT/forme")
        for cel, a, b, e, code in (("N2", 0, 1, [{"i": 1}], "LOT/indices"), ("N2", 1, 1, [], "LOT/nom"),
                                   ("E1/1", 0, 1, [{"i": 0}], "LOT/nom"), ("N1.x", 0, 1, [{"i": 0}], "LOT/nom")):
            self.assertEqual(code_de(executer.ecrire_lot, self.r, cel, a, b, e, ["e"]), code, cel)


class TestProcessus(unittest.TestCase):
    def test_appliquer_ordonne(self):
        """E-S-42 : quatre tâches achevées dans l'ordre inverse (lent) : résultats dans l'ordre des tâches, en 1 et en 4
        processus, ceux-ci hors du processus appelant ; processus 0 ou booléen : EXEC/processus. Mutations M-11C-01
        (ordre d'achèvement, imap_unordered), M-11C-06 (un seul processus quel que soit le nombre demandé)."""
        taches = [(k, 4) for k in range(4)]
        self.assertEqual([executer.appliquer(lent, taches, p) for p in (1, 4)], [[0, 1, 2, 3], [0, 1, 2, 3]])
        self.assertNotIn(os.getpid(), executer.appliquer(pid, [(k,) for k in range(4)], 4))
        for p in (0, True):
            self.assertEqual(code_de(executer.appliquer, lent, taches, p), "EXEC/processus")

    def test_plan_90_min(self):
        """Adjudication 6 du G0 (lots de 90 min au plus), C1-COUT-1 : 1 000 réplications de 60 s, un processus : lots de
        90 (5 400 s), le dernier de 10 ; 200 réplications de 30 s, deux processus : un lot ; 400 : 360 et 40 ; 10
        réplications de 5 401 s : EXEC/plan. C-1 de la G2 de SB-11, compte non multiple du nombre de processus : 10⁴
        réplications de 41 s, quatre processus : ⌊5 400/41⌋ = 131 tours (5 371 s ; 132 en feraient 5 412), lots de
        131·4 = 524, 20 lots, le dernier (9 956, 10 000) ; chaque lot en ⌈(b − a)/4⌉·41 s ≤ 5 400 s. Mutations
        M-11C-02 (processus ignorés), M-11C-03 (borne dépassée d'une réplication), M-11V-01 (⌊borne·processus/ns⌋ :
        lots de 526, 132 tours), M-11V-03 (processus ignorés dans le plan corrigé)."""
        s = 10 ** 9
        p = executer.plan(1000, 60 * s, 1)
        self.assertEqual((len(p), p[:1], p[-2:]), (12, [(0, 90)], [(900, 990), (990, 1000)]))
        self.assertEqual(executer.plan(200, 30 * s, 2), [(0, 200)])
        self.assertEqual(executer.plan(400, 30 * s, 2), [(0, 360), (360, 400)])
        self.assertEqual(code_de(executer.plan, 10, 5401 * s, 4), "EXEC/plan")
        p = executer.plan(10000, 41 * s, 4)
        self.assertEqual((len(p), p[:2], p[-1]), (20, [(0, 524), (524, 1048)], (9956, 10000)))
        self.assertEqual(max(-(-(b - a) // 4) for a, b in p) * 41, 5371)


def rv(v, *c):
    return {"valeur": v, "causes": list(c)}


class TestAgregat(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.r = d.name

    def test_agreger(self):
        """Cinq enregistrements écrits à la main (strate « calme », BTC et ETH, valeurs « avec », variante aux
        diviseurs 4 et 8) : BTC 2 REJETTE, 2 NE REJETTE PAS, 1 NON ÉVALUABLE (k_crit, runs) ; ETH testé sans condition
        2 REJETTE ; familial 2 sur 5 ; séquence BTC puis ETH 1 (le second rejet de BTC est suivi d'ETH NE REJETTE PAS) ;
        « avec » et variante (5 NE REJETTE PAS au diviseur 8) comptés à part ; r̂ = 2/5 et SE = √(6/125) (bc -l :
        sqrt(6/125), à 10⁻⁵⁰ près) ; aucun enregistrement : EXEC/agreger ; empreinte = executer.empreinte des cinq,
        dans l'ordre. Mutations M-11H-02
        (familial inversé), M-11H-03 (séquence lue sur BTC), M-11H-04 (« avec » pris aux valeurs sans), M-11H-05 (un
        diviseur pour tous), M-11H-06 (R faux), M-11H-09 (empreinte à rebours), M-11H-10 (précision 28), M-11H-11
        (aucun enregistrement admis)."""
        x = [(rv("REJETTE"), rv("REJETTE"), True, "REJETTE", rv("REJETTE"), rv("NE REJETTE PAS")),
             (rv("NE REJETTE PAS"), rv("REJETTE"), False, "NON TESTÉ (séquence)", rv("NE REJETTE PAS"),
              rv("NON ÉVALUABLE", "runs")),
             (rv("NON ÉVALUABLE", "k_crit", "runs"), rv("NE REJETTE PAS"), False, "NON TESTÉ (séquence)",
              rv("NON ÉVALUABLE", "unites", "k_crit", "runs"), rv("NON ÉVALUABLE", "k_crit", "runs")),
             (rv("REJETTE"), rv("NE REJETTE PAS"), True, "NE REJETTE PAS", rv("REJETTE"), rv("NE REJETTE PAS")),
             (rv("NE REJETTE PAS"), rv("NE REJETTE PAS"), False, "NON TESTÉ (séquence)", rv("NE REJETTE PAS"),
              rv("NE REJETTE PAS"))]
        h = rv("NE REJETTE PAS")
        recs = [{"i": i, "strates": {"calme": {"classes": {"BTC": dict(b, avec=a, variante={"4": v, "8": h}),
                                                           "ETH": dict(e, avec=a, variante={"4": v, "8": h})},
                                               "valeurs": {"familial": f, "ETH": {"valeur": s}}}}}
                for i, (b, e, f, s, a, v) in enumerate(x)]
        g = executer.agreger(K_, recs)
        self.assertEqual(sorted(g), ["R", "empreinte", "strates"])
        c = g["strates"]["calme"]
        b = c["classes"]["BTC"]
        self.assertEqual((g["R"], g["empreinte"], c["familial"]["x"], c["sequence_eth"]["x"]),
                         (5, executer.empreinte(recs), 2, 1))
        self.assertEqual((b["frequences"]["valeurs"], c["classes"]["ETH"]["frequences"]["valeurs"]),
                         ({"REJETTE": 2, "NE REJETTE PAS": 2, "NON ÉVALUABLE": 1},
                          {"REJETTE": 2, "NE REJETTE PAS": 3, "NON ÉVALUABLE": 0}))
        v = b["variante"]
        self.assertEqual((b["avec"]["frequences"]["combinaisons"], v["4"]["frequences"]["combinaisons"],
                          v["8"]["frequences"]["valeurs"]["NE REJETTE PAS"]),
                         ({"unites+k_crit+runs": 1}, {"runs": 1, "k_crit+runs": 1}, 5))
        t = b["taux"]["REJETTE"]
        se = Decimal("0.219089023002066445382787913120320853581097877999193301690757")
        self.assertEqual((t["r"], t["R"]), (Fraction(2, 5), 5))
        self.assertLess(abs(t["SE"] - se), Decimal("1E-50"))
        self.assertEqual(code_de(executer.agreger, K_, []), "EXEC/agreger")

    def test_ecrire_agrege(self):
        """Agrégat « <cellule>.agrege.json » : JSON canonique d'une ligne, entête en tête de laquelle l'étiquette
        (E-S-05), cellule, agrégat ; nom de cellule à « / » : LOT/nom. Mutations M-11H-07 (nom non contrôlé),
        M-11H-08 (entête omise)."""
        c = executer.ecrire_agrege(self.r, "N1", {"R": 1}, [commun.ETIQUETTE, "sha256 x y"])
        self.assertTrue(os.path.isfile(c), c)
        with open(c, "rb") as f:
            o = f.read()
        self.assertEqual((os.path.basename(c), o.count(b"{"), json.loads(o)), (
            "N1.agrege.json", 1, {"R": 1, "cellule": "N1", "entete": [commun.ETIQUETTE, "sha256 x y"]}))
        self.assertEqual(code_de(executer.ecrire_agrege, self.r, "E1/x", {"R": 1}, []), "LOT/nom")


if __name__ == "__main__":
    unittest.main()
