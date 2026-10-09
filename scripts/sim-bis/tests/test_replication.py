"""Réplication d'une cellule SB-11f (E-S-14, E-S-22 à E-S-28, E-S-41) : référence = la chaîne écrite à la main ici, pas
à pas, depuis les modules du moteur (calendrier, sources, observateurs, regle) et le flux « debut » tiré par
aleas.flux ; fixtures réduites (W = 1 semaine, R = 99) ; chaque test nomme les mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction

import aleas
import calendrier
import calibration
import commun
import executer
import observateurs
import regle
import sources

PRM = commun.charger_parametres(environ={})
P99 = dict(PRM, regle=dict(PRM["regle"], R=99))
EP = calibration.charger(PRM, environ={})["episodes"]
F = Fraction
POINTS = {"C1": {"calme": (F(1, 100), F(5), 60), "stress": (F(1, 50), F(10), 240)}}
CEL = {"nom": "T-1", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [1, 4000],
       "derive": None, "incidents": None, "faibles": None,
       "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                  "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
       "regle": {"R": 99, "classes": ["BTC", "ETH", "USDC", "USDT"], "S": False, "variante": [], "evenements": 0,
                 "absorption": False},
       "surcharges": {}}


def cel2(**k):
    """CEL retouchée (clés de premier niveau, ou « couche__x »)."""
    c = copy.deepcopy(CEL)
    for cle, v in k.items():
        a, _p, b = cle.partition("__")
        c[a] = dict(c[a], **{b: v}) if b else v
    return c


def chaine(prm, cel, W, i, ep=EP):
    """Réplication écrite à la main : spécification (executer.cellule, SB-11d et SB-11e), T_début par le flux
    « debut » d'indice 0 (aleas.flux), masques de strate, état vrai, couche, quorum ; par strate, fenêtres retenues,
    retraits par classe (ok consolidé sur les retenues), première unité BTC après retraits, séries D comprimées,
    regle.tester. Rend {strate : (n, première, {classe : (retraits, résultat)})} et le jour tiré."""
    c, nom = executer.cellule(prm, ep, cel, POINTS, W), cel["nom"]
    cal = prm["calendrier"]
    e = calendrier.echelle(cal, W)
    debut = calendrier.t_debut(cal, aleas.flux(prm["aleas"], nom, i, "debut", 0))
    m = calendrier.masques(cal, debut, e["t_max"])
    etat = sources.Replication(c["prm"], ep, c["fond"], nom, i, m, e["t_max"]).etat()
    q, cons = observateurs.Couche(c["prm"], c["couche"], nom, i, e["t_max"]).consolidation(etat, m)
    st, pools = prm["calibration"]["strates"], dict(sources.classes(prm))
    ret = {s: calendrier.retenues(q.evaluables, m[s], e["n"][s]) for s in st}
    n = {s: ret[s]["n"] for s in st}
    rt = {cl: regle.retraits({(u, s): (cons[u, cl][1] & ret[s]["masque"]).bit_count() for u in pools[cl] for s in st},
                             n) for cl in cel["regle"]["classes"]}
    out, graine = {}, aleas.graine_regle(prm["aleas"], nom, i)
    for s in st:
        prem = regle.premiere([u for u in pools["BTC"] if (u, s) not in rt["BTC"]])
        segs = calendrier.segments(ret[s]["masque"])
        res = {}
        for cl in cel["regle"]["classes"]:
            series = {u: calendrier.comprimer(cons[u, cl][0], segs) for u in pools[cl] if (u, s) not in rt[cl]}
            res[cl] = (sorted([u, x] for (u, t), x in rt[cl].items() if t == s),
                       regle.tester(series, prem, graine, s, n[s], e["n"][s], prm, 99))
        out[s] = (n[s], prem, res)
    return out, (debut - cal["lundi_reference"]) // 86400


class TestReplication(unittest.TestCase):
    def egal(self, prm, cel, i, ep=EP):
        """Enregistrement de executer.replication égal à la chaîne écrite à la main ; rendu."""
        r = executer.replication(prm, ep, cel, POINTS, 1, i)
        attendu, jour = chaine(prm, cel, 1, i, ep)
        self.assertEqual((r["i"], r["jour"], sorted(r["strates"])), (i, jour, sorted(attendu)))
        cles = ("valeur", "causes", "C", "C1", "K", "runs", "unites")
        for s, (n, prem, res) in attendu.items():
            x = r["strates"][s]
            self.assertEqual((x["n"], x["premiere"]), (n, prem), (i, s))
            for cl, (rt, t) in res.items():
                self.assertEqual((x["retraits"][cl], [x["classes"][cl][k] for k in cles]), (rt, [t[k] for k in cles]),
                                 (i, s, cl))
            self.assertEqual(x["valeurs"], regle.strate({cl: v[1] for cl, v in res.items()}), (i, s))
        return r

    def test_chaine_a_la_main(self):
        """Cellule N1 réduite (W = 1, R = 99), i = 0, 1, 2, puis cellule à couche dégradée au repli M = 3 (fenêtres non
        évaluables) et n_s de calme porté à 12 000 (n′_s < n_s à T_max) : jour tiré, n retenu, première unité, retraits
        par classe, valeur, causes, C, C1, K, runs et unités de chaque classe dans chaque strate, égaux à la chaîne
        écrite à la main ; valeurs de la strate par regle.strate. Mutations M-11F-01 (séries « ok » au lieu de D),
        M-11F-02 (flux de T_début d'un autre indice), M-11F-04 (retenues sans le quorum), M-11F-05 (n_s au lieu de
        n′_s), M-11F-08 (retraits sur D au lieu de l'ok)."""
        for i in range(3):
            self.egal(P99, CEL, i)
        p = dict(P99, calendrier=dict(P99["calendrier"], n_par_semaine={"calme": 12000, "stress": 2736}))
        r = self.egal(p, cel2(couche__grille="degradee", couche__repli=True), 0)
        self.assertEqual((r["strates"]["calme"]["suffisant"], r["strates"]["calme"]["n"] < 12000), (True, True))

    def test_premiere_apres_retrait(self):
        """Q-T3-15 : binance « presque mort » en calme (EP retouché en mémoire : 16 000 cellules de panne et d'écart sur
        24 585, épisodes de 100 fenêtres ; f = 1 ; C0, un régime à cette part étant infaisable, REGIME-FAISABILITE-1) :
        retirée de toutes les classes en calme, première unité bitfinex, égale à la chaîne écrite à la main. Mutation
        M-11F-03 (première unité prise avant les retraits)."""
        ep = dict(EP)
        for ty in ("panne", "ecart"):
            ep["calme", "binance", ty] = dict(EP["calme", "binance", ty], cellules=16000, histogramme=[(100, 160)])
        r = self.egal(P99, cel2(niveau="C0", f=[1, 1], hors_enveloppe=[0, 1]), 0, ep)
        x = r["strates"]["calme"]
        self.assertEqual((x["premiere"], x["retraits"]["BTC"]), ("bitfinex", [["binance", "presque mort"]]))

    def test_quorum_par_strate(self):
        """Impression due (ADR-0029 l.97 a ; AVIS-SIM-T3 Q-T3-2) : nombre de fenêtres de la strate à M_j = 0, 1, 2, 3, 4
        observateurs valides, de somme le nombre de fenêtres de la strate sur la grille. Mutation M-11F-06 (M_j compté
        sur la grille entière)."""
        r = executer.replication(P99, EP, CEL, POINTS, 1, 0)
        e = calendrier.echelle(PRM["calendrier"], 1)
        jour = r["jour"]
        self.assertEqual(sorted(r["strates"]), ["calme", "stress"])
        m = calendrier.masques(PRM["calendrier"], PRM["calendrier"]["lundi_reference"] + 86400 * jour, e["t_max"])
        for s, x in r["strates"].items():
            self.assertEqual((len(x["M"]), sum(x["M"])), (5, m[s].bit_count()), s)

    def test_composant_debut(self):
        """E-S-41 et Q-4 (composants en liste fermée avant E0) : T_début tiré sur le composant « debut », déclaré dans
        sources.composants ; une liste sans lui : SOURCES/composant. Mutation M-11F-07 (composant non déclaré)."""
        self.assertIn("debut", PRM["sources"]["composants"])
        p = copy.deepcopy(P99)
        p["sources"]["composants"].remove("debut")
        with self.assertRaises(commun.Refus) as c:
            executer.replication(p, EP, CEL, POINTS, 1, 0)
        self.assertEqual(c.exception.code, "SOURCES/composant")


if __name__ == "__main__":
    unittest.main()
