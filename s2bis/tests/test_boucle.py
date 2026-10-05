"""CB-4, E-C-09, E-C-11 à E-C-15 : boucle du pool, horloge et attentes injectées, journal relu par `chaine`. Valeurs
écrites à la main : instants par date -u -d ; base64 et sha256 de b"x" par printf, base64 et sha256sum."""
import concurrent.futures
import threading

from shogen_s2bis.collecte import boucle
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_journal import FICHIER, Base, chaine
from tests.test_reprise import m, sans_chaine

D, E = 1791154900 * S, 1791154919 * S                      # départ et échéance de la fenêtre m(3), 23:01 UTC
X = {"statut": "ok", "sous_type": None, "code": 200, "adresse": "127.0.0.1:443", "valeurs": None, "brut": "eA==",
     "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"}


class Temps:
    """Horloge injectée, portée à t par `dormir(t)` et `attendre(futurs, t)` (plus `saut`), consignés ; 0,5 s réelle."""
    def __init__(self, t, saut=0):
        self.t, self.saut, self.appels = t, saut, []

    def __call__(self):
        return self.t

    def dormir(self, t):
        self.appels.append(("dormir", t))
        self.t = max(self.t, t)

    def attendre(self, futurs, t):
        self.appels.append(("attendre", t))
        concurrent.futures.wait(futurs, 0.5)
        self.t = max(self.t, t) + self.saut


def rapide(suivi):
    return Lecture("ok", suivi["depart"], suivi["depart"] + 7, {"dns": suivi["depart"] + 1}, "127.0.0.1:443", code=200,
                   octets=b"x")


def pendue(porte, dns):
    """Lecture qui attend `porte` ; si `dns`, la résolution a rendu avant (phase et adresse posées dans le suivi)."""
    def lire(suivi):
        if dns:
            suivi["phases"], suivi["adresse"] = {"dns": suivi["depart"] + 1}, "127.0.0.1:443"
        porte.wait()
        return rapide(suivi)
    return lire


class Boucle(Base):
    def tourner(self, lectures, plan, n=1, places=8, saut=0):
        self.temps = Temps(m(2) * S + 5 * S, saut)                  # journal ouvert à 23:00:05 ; 1re fenêtre, 23:01
        self.b = boucle.Boucle(self.journal(m(2)), lectures, plan, places, horloge=self.temps,
                               dormir=self.temps.dormir, attendre=self.temps.attendre)
        self.b.tourner(n)
        return sans_chaine(chaine(self.etat()[FICHIER])[2])[1:]

    def test_planifier_par_hote(self):
        self.assertEqual(boucle.planifier([("a", "h1"), ("b", "h1"), ("c", "h2"), ("d", "h2")], espaces={"h1"}),
                         [(0, "a"), (0, "c"), (0, "d"), (S, "b")])
        with self.assertRaises(ValueError):
            boucle.planifier([(str(k), "h") for k in range(6)])
        self.assertEqual(len(boucle.planifier([(str(k), "h") for k in range(5)], espaces={"h"})), 5)

    def test_lectures_a_l_heure_puis_sante_et_marqueur(self):
        enrs = self.tourner({"a": rapide, "b": rapide}, [(0, "a"), (S, "b")])
        self.assertEqual(self.temps.appels, [("dormir", D), ("dormir", D + S), ("attendre", E)])
        self.assertEqual(enrs, [{"type": "lecture", "ws": m(3), "forme": n, "prevu": p, "depart": p, "fin": p + 7,
                                 "phases": {"dns": p + 1}, **X} for n, p in (("a", D), ("b", D + S))] +
                         [{"type": "sante", "ws": m(3), "d2": {"retard_max": 0, "non_parties": 0},
                           "fils": {"abandonnes": 0, "tardives": []}}, {"type": "marqueur", "ws": m(3)}])

    def test_echeance_lectures_non_finies_classees_fils_abandonnes(self):
        porte = threading.Event()
        self.addCleanup(porte.set)
        enrs = self.tourner({"a": rapide, "b": pendue(porte, True), "c": pendue(porte, False)},
                            [(0, "a"), (0, "b"), (0, "c")], n=2)
        self.assertEqual([(e["type"], e.get("forme"), e.get("statut"), e.get("sous_type")) for e in enrs[:5]],
                         [("lecture", "a", "ok", None), ("lecture", "b", "panne_transport", "delai"),
                          ("lecture", "c", "panne_transport", "dns"), ("sante", None, None, None),
                          ("marqueur", None, None, None)])
        self.assertEqual([(e["depart"], e["fin"], e["phases"], e["adresse"], e["code"]) for e in enrs[1:3]],
                         [(D, E, {"dns": D + 1}, "127.0.0.1:443", None), (D, E, {}, None, None)])
        self.assertEqual([e["fils"]["abandonnes"] for e in enrs if e["type"] == "sante"], [2, 4])
        self.assertEqual([x for x in self.temps.appels if x[0] == "dormir"], [("dormir", D)] * 3 +
                         [("dormir", D + 60 * S)] * 3)

    def test_pool_borne_lecture_non_partie_jamais_ecrite(self):
        porte = threading.Event()
        self.addCleanup(porte.set)
        enrs = self.tourner({k: pendue(porte, False) for k in "abc"}, [(0, k) for k in "abc"], n=2, places=2)
        self.assertEqual([e.get("forme") for e in enrs if e["type"] == "lecture"], ["a", "b"])
        self.assertEqual([(e["d2"], e["fils"]["abandonnes"]) for e in enrs if e["type"] == "sante"],
                         [({"retard_max": 0, "non_parties": 1}, 2), ({"retard_max": None, "non_parties": 3}, 2)])

    def test_resultat_tardif_compte_jamais_ecrit(self):
        porte = threading.Event()
        self.tourner({"a": pendue(porte, True)}, [(0, "a")])
        porte.set()
        concurrent.futures.wait(self.b.abandons, 5)
        self.b.tourner(1)
        enrs = sans_chaine(chaine(self.etat()[FICHIER])[2])[1:]
        self.assertEqual([(e["type"], e.get("statut")) for e in enrs], [("lecture", "panne_transport"), ("sante", None),
                                                                       ("marqueur", None), ("lecture", "ok"),
                                                                       ("sante", None), ("marqueur", None)])
        self.assertEqual([e["fils"] for e in enrs if e["type"] == "sante"],
                         [{"abandonnes": 1, "tardives": []}, {"abandonnes": 0, "tardives": [7]}])

    def test_attrape_tout_et_fenetre_dont_l_echeance_est_passee_sautee(self):
        def casse(suivi):
            raise RuntimeError("défaut imprévu")
        enrs = self.tourner({"a": casse}, [(0, "a")], n=2, saut=120 * S)       # l'attente déborde de deux minutes
        self.assertEqual([(e["type"], e.get("ws"), e.get("sous_type")) for e in enrs],
                         [("lecture", m(3), "autre"), ("sante", m(3), None), ("marqueur", m(3), None),
                          ("lecture", m(6), "autre"), ("sante", m(6), None), ("trou", None, None),
                          ("marqueur", m(6), None)])
        self.assertEqual(enrs[5], {"type": "trou", "de": m(4), "a": m(5), "cause": "saut"})
