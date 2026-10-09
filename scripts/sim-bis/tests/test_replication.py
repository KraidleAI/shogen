"""Réplication d'une cellule SB-11f (E-S-14, E-S-22 à E-S-28, E-S-41) : référence = la chaîne écrite à la main ici, pas
à pas, depuis les modules du moteur (calendrier, sources, observateurs, regle) et le flux « debut » tiré par
aleas.flux ; fixtures réduites (W = 1 semaine, R = 99) ; chaque test nomme les mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction
from unittest import mock

import aleas
import calendrier
import calibration
import commun
import executer
import observateurs
import regle
import sources
import variante

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
    regle.tester (S suivie selon la cellule). Rend {strate : (n, première, {classe : (retraits, résultat, séries,
    n_s)})}, le jour tiré et la graine de règle."""
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
                       regle.tester(series, prem, graine, s, n[s], e["n"][s], prm, 99, cel["regle"]["S"]), series,
                       e["n"][s])
        out[s] = (n[s], prem, res)
    return out, (debut - cal["lundi_reference"]) // 86400, graine


class TestReplication(unittest.TestCase):
    def egal(self, prm, cel, i, ep=EP):
        """Enregistrement de executer.replication égal à la chaîne écrite à la main ; rendu."""
        r = executer.replication(prm, ep, cel, POINTS, 1, i)
        attendu, jour, _g = chaine(prm, cel, 1, i, ep)
        self.assertEqual((r["i"], r["jour"], sorted(r["strates"])), (i, jour, sorted(attendu)))
        cles = ("valeur", "causes", "C", "C1", "K", "runs", "unites")
        for s, (n, prem, res) in attendu.items():
            x = r["strates"][s]
            self.assertEqual((x["n"], x["premiere"]), (n, prem), (i, s))
            for cl, (rt, t, _x, _n) in res.items():
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


COURT = ("valeur", "causes", "C", "C1", "C_S", "r", "K", "S", "runs", "unites")


class TestRegleCellule(unittest.TestCase):
    def test_absorption_s_variante_evenements(self):
        """Cellule à deux unités faibles (2/5, L = 1, panne), S suivie, critère collectif, variante aux diviseurs 4 et
        8, compte d'événements sur la première réplication : sur les séries comprimées de la chaîne écrite à la main,
        « avec » = regle.tester des séries restées après regle.filtrer (retirées, indice), variante = variante.tester,
        événements = regle.loi_evenements (suite comprimée, P-3), C_S de regle.tester. Mutations M-11G-01 (« avec »
        sur toutes les séries), M-11G-02 (diviseur ignoré), M-11G-03 (« g sur la grille », P-3), M-11G-04 (S non
        suivie)."""
        cel = copy.deepcopy(CEL)
        cel.update(nom="T-3", faibles={"k": 2, "p": [2, 5], "L": 1, "type": "panne"},
                   regle=dict(CEL["regle"], S=True, absorption=True, variante=[4, 8], evenements=1))
        r = executer.replication(P99, EP, cel, POINTS, 1, 0)
        attendu, _j, g = chaine(P99, cel, 1, 0)
        for s, (n, prem, res) in attendu.items():
            for cl, (_rt, t, series, ns) in res.items():
                y = r["strates"][s]["classes"][cl]
                reste, ret, ind = regle.filtrer(series, n, P99)
                a = regle.tester(reste, prem, g, s, n, ns, P99, 99, True)
                self.assertEqual(y.get("avec"), dict({k: a[k] for k in COURT}, retirees=ret, indice=ind), (s, cl))
                for d in (4, 8):
                    v = variante.tester(series, prem, g, s, n, ns, P99, 99, d)
                    self.assertEqual(y.get("variante", {}).get(str(d)), dict({k: v[k] for k in COURT if k in v},
                                                                              N=v["N"]), (s, cl, d))
                ev = regle.loi_evenements(series, prem, g, s, n, 99, P99)
                self.assertEqual((y.get("evenements"), y["C_S"]), ({str(k): x for k, x in ev.items()}, t["C_S"]))
        self.assertIsNotNone(r["strates"]["calme"]["classes"]["BTC"]["C_S"])
        self.assertNotIn("evenements", executer.replication(P99, EP, cel, POINTS, 1, 1)["strates"]["calme"]["classes"][
            "BTC"])

    def test_oracle_e_s_29(self):
        """E-S-29 et O-4 de la G2 de la tranche 4 : les 200 premières réplications d'une cellule passent par
        regle.oracle (huit appels : quatre classes, deux strates) et la variante par variante.deux_modes ; i = 200 :
        regle.tester et variante.tester ; variante dont les deux modes diffèrent : VARIANTE/oracle. Mutations
        M-11G-05 (oracle sur la seule première réplication), M-11G-06 (variante sans oracle), M-11G-07 (écart des
        deux modes de la variante admis)."""
        cel = copy.deepcopy(CEL)
        cel["regle"]["variante"] = [4]
        for i, attendu in ((0, (8, 0, 8, 0)), (199, (8, 0, 8, 0)), (200, (0, 8, 0, 8))):
            with mock.patch.object(regle, "oracle", wraps=regle.oracle) as o, mock.patch.object(
                    regle, "tester", wraps=regle.tester) as t, mock.patch.object(
                    variante, "deux_modes", wraps=variante.deux_modes) as d, mock.patch.object(
                    variante, "tester", wraps=variante.tester) as v:
                executer.replication(P99, EP, cel, POINTS, 1, i)
            self.assertEqual((o.call_count, t.call_count, d.call_count, v.call_count), attendu, i)
        faux = ({"valeur": "REJETTE", "causes": [], "N": 1}, {"valeur": "NE REJETTE PAS", "causes": [], "N": 1})
        with mock.patch.object(variante, "deux_modes", return_value=faux):
            try:
                executer.replication(P99, EP, cel, POINTS, 1, 0)
                code = None
            except commun.Refus as e:
                code = e.code
        self.assertEqual(code, "VARIANTE/oracle")

    def test_n_prime_aux_sites_d_appel(self):
        """C-6 de la G2 de SB-11 (E-S-24, E-S-35) : fixture de test_chaine_a_la_main où n′_s < n_s (n_s de calme porté
        à 12 000, couche dégradée au repli ; garde : n′ de calme < 12 000), critère collectif actif : regle.retraits
        reçoit les n′_s retenus des deux strates à chaque classe, regle.filtrer le n′_s de sa strate, jamais n_s.
        Mutants G-09 (n_s aux retraits), G-12 (n_s au critère collectif)."""
        p = dict(P99, calendrier=dict(P99["calendrier"], n_par_semaine={"calme": 12000, "stress": 2736}))
        c = cel2(couche__grille="degradee", couche__repli=True, regle=dict(CEL["regle"], classes=["BTC", "ETH"],
                                                                           absorption=True))
        with mock.patch.object(regle, "retraits", wraps=regle.retraits) as rt, mock.patch.object(
                regle, "filtrer", wraps=regle.filtrer) as fl:
            r = executer.replication(p, EP, c, POINTS, 1, 0)
        n = {s: r["strates"][s]["n"] for s in ("calme", "stress")}
        self.assertLess(n["calme"], 12000)
        self.assertEqual([x.args[1] for x in rt.call_args_list], [n, n])
        self.assertEqual([x.args[1] for x in fl.call_args_list], [n["calme"]] * 2 + [n["stress"]] * 2)

    def test_surcharges_jusqu_aux_sources(self):
        """C-7 de la G2 de SB-11 (source des données) : la surcharge {longues : [60], poids_longues : [1]} de la cellule
        (PRM : [60, 1 440, 4 320] et [1, 1, 1]) atteint sources.Replication et observateurs.Couche lors d'une
        réplication ; le prm du lot reste intact. Mutant G-10 (sources.Replication sur le prm du lot), M-11V-02
        (observateurs.Couche sur le prm du lot)."""
        s = {"longues": [60], "poids_longues": [1]}
        with mock.patch.object(sources, "Replication", wraps=sources.Replication) as rp, mock.patch.object(
                observateurs, "Couche", wraps=observateurs.Couche) as co:
            executer.replication(P99, EP, cel2(surcharges=s, regle=dict(CEL["regle"], classes=["BTC"])), POINTS, 1, 200)
        self.assertEqual([{k: x.args[0]["sources"][k] for k in s} for x in rp.call_args_list + co.call_args_list],
                         [s, s])
        self.assertEqual(P99["sources"]["longues"], [60, 1440, 4320])

    def test_r_de_la_cellule(self):
        """C-8 de la G2 de SB-11 (Q-S-06, complément 1) et C-12 du contre-contrôle : une cellule à R = 999 (R_approche),
        critère collectif actif, sous un prm à R = 99, deux strates, une classe ; i = 0 : 999 à regle.oracle (valeur
        sans, puis « avec », par strate : 4 appels), à variante.deux_modes et à regle.loi_evenements (2 chacun) ;
        i = 200 : 999 à regle.tester (4 appels) et à variante.tester (2) ; jamais le R du prm. Mutants G-11 (R du prm
        passé à la règle), M-11V-04 (à la variante), M-11V-05 (au compte d'événements), M-CC-03 (au calcul « avec »),
        M-CC-04 (à variante.tester)."""
        c = cel2(regle=dict(CEL["regle"], R=999, classes=["BTC"], variante=[4], evenements=1, absorption=True))
        vus = {}
        for i in (0, 200):
            with mock.patch.object(regle, "oracle", wraps=regle.oracle) as o, mock.patch.object(
                    regle, "tester", wraps=regle.tester) as t, mock.patch.object(
                    variante, "deux_modes", wraps=variante.deux_modes) as d, mock.patch.object(
                    variante, "tester", wraps=variante.tester) as v, mock.patch.object(
                    regle, "loi_evenements", wraps=regle.loi_evenements) as ev:
                executer.replication(P99, EP, c, POINTS, 1, i)
            vus[i] = tuple([x.args[k] for x in f.call_args_list] for f, k in ((o, 7), (t, 7), (d, 7), (v, 7), (ev, 5)))
        self.assertEqual(vus, {0: ([999] * 4, [], [999] * 2, [], [999] * 2), 200: ([], [999] * 4, [], [999] * 2, [])})


if __name__ == "__main__":
    unittest.main()
