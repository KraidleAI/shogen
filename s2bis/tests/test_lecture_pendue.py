"""CB-5 : tests « lecture pendue » (PROPOSITION §2.4, T-LP-1 à T-LP-6 ; ADR-0029 l.233), contre les mutants M-LP-1 à
M-LP-8, et borne du corps (SHOGEN-S2BIS-CORPS-BORNE-1). Chaque test a son propre délai : en processus, la boucle tourne
dans un fil joint en 5 s réelles au plus (un mutant qui pend fait échouer le test sans pendre la suite) ; T-LP-4 tourne
en sous-processus, fils et horloge réels."""
import base64
import concurrent.futures
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import time
import unittest

from shogen_s2bis.collecte import boucle, http, journal
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_boucle import D, E, Temps, borne, pendue, rapide
from tests.test_http_reseau import Resolveur, repondre, servir
from tests.test_journal import FICHIER, Base, chaine
from tests.test_reprise import m, sans_chaine

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REEL = """
import sys, threading, tests
from shogen_s2bis.collecte import boucle, journal
from shogen_s2bis.collecte.lecture import Lecture, S, horloge
jl = journal.Journal(sys.argv[1], "pool", w=1).ouvrir(horloge() // S)
porte = threading.Event()
def rapide(suivi):
    return Lecture("ok", suivi["depart"], horloge(), code=200)
boucle.Boucle(jl, {"p": lambda suivi: porte.wait(), "r": rapide}, [(0, "p"), (0, "r")], 4, w=1, delta=S * 6 // 10,
              marge=S // 5).tourner(3)
jl.fermer()
"""


class LecturePendue(Base):
    def setUp(self):
        super().setUp()
        self.porte = threading.Event()
        self.addCleanup(self.porte.set)

    def tourner(self, lectures=None, plan=None, n=1, places=8):
        """`n` fenêtres dans un fil joint en 5 s réelles au plus ; rend les enregistrements du journal."""
        if lectures is not None:
            self.temps = Temps(m(2) * S + 5 * S)
            self.b = boucle.Boucle(borne(self, self.journal, m(2)), lectures, plan, places, horloge=self.temps,
                                   dormir=self.temps.dormir, attendre=self.temps.attendre)
        borne(self, self.b.tourner, n)
        return sans_chaine(chaine(self.etat()[FICHIER])[2])[1:]

    def test_tlp1_lecture_qui_ne_rend_jamais(self):
        enrs = self.tourner({"p": pendue(self.porte, True), "r": rapide}, [(0, "p"), (0, "r")], n=2)
        self.assertEqual([(e["type"], e.get("forme"), e.get("sous_type"), e.get("fin")) for e in enrs[:4]],
                         [("lecture", "p", "delai", E), ("lecture", "r", None, D + 7), ("sante", None, None, None),
                          ("marqueur", None, None, None)])
        self.assertEqual([e["fils"]["abandonnes"] for e in enrs if e["type"] == "sante"], [1, 2])
        self.assertEqual(self.temps.appels, [("dormir", D), ("dormir", D), ("attendre", E), ("dormir", D + 60 * S),
                                             ("dormir", D + 60 * S), ("attendre", E + 60 * S)])

    def test_tlp2_resolution_bloquante_classee_dns(self):
        def lire(suivi):
            return http.lire(http.Requete("api.example", "/"), suivi, resoudre=lambda *a: self.porte.wait(), tls=None)
        enrs = self.tourner({"p": lire}, [(0, "p")])
        self.assertEqual((enrs[0]["statut"], enrs[0]["sous_type"], enrs[0]["phases"]), ("panne_transport", "dns", {}))

    def test_tlp3_resultat_tardif_jamais_ecrit_compte_ensuite(self):
        port, _r, fil = servir(repondre(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\n{}"))
        res = Resolveur(port)

        def lire(suivi):                                            # suivi propre : le client garde l'horloge réelle
            self.porte.wait(5)
            return http.lire(http.Requete("api.example", "/"), resoudre=res, tls=None)
        self.tourner({"p": lire}, [(0, "p")])
        self.porte.set()
        concurrent.futures.wait(self.b.abandons, 5)
        fil.join(5)
        enrs = self.tourner()
        self.assertEqual([(e["type"], e.get("ws")) for e in enrs], [(t, m(n)) for n in (3, 4)
                                                                     for t in ("lecture", "sante", "marqueur")])
        self.assertEqual([len(e["fils"]["tardives"]) for e in enrs if e["type"] == "sante"], [0, 1])

    def test_tlp4_sous_processus_fils_reels(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-B", "-c", REEL, d], cwd=RACINE, capture_output=True, timeout=30)
            octets = b"".join(pathlib.Path(d, n).read_bytes() for n in sorted(os.listdir(d)) if n.endswith(".jsonl"))
        enrs = chaine(octets)[2]
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        self.assertEqual(sum(e["type"] == "marqueur" for e in enrs), 3)
        self.assertEqual({(e["forme"], e["statut"], e["depart"] >= e["prevu"]) for e in enrs if e["type"] == "lecture"},
                         {("p", "panne_transport", True), ("r", "ok", True)})

    def test_tlp5_plus_de_fils_pendus_que_de_places(self):
        enrs = self.tourner({k: pendue(self.porte, False) for k in "ab"}, [(0, "a"), (0, "b")], n=2, places=1)
        self.assertEqual([(e["forme"], e["sous_type"]) for e in enrs if e["type"] == "lecture"], [("a", "dns")])
        self.assertEqual([(e["d2"]["non_parties"], e["fils"]["abandonnes"]) for e in enrs if e["type"] == "sante"],
                         [(1, 1), (2, 1)])
        self.porte.set()                                            # la lecture pendue finit : sa place se libère
        concurrent.futures.wait(self.b.abandons, 5)
        w5 = [e for e in self.tourner() if e.get("ws") == m(5)]        # « b » part ou non selon l'ordre des fils
        self.assertEqual((w5[0]["forme"], w5[0]["statut"], w5[-2]["fils"]["abandonnes"]), ("a", "ok", 0))

    def test_tlp6_corps_au_goutte_a_goutte_clos_au_delai_global(self):
        """Mis à l'échelle : un octet toutes les 0,05 s, délai global de 0,5 s (M-LP-8, délai par opération : 5 s)."""
        port, _r, fil = servir(repondre(b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n" + b"x" * 100, pas=0.05))
        lu = http.lire(http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=S // 2)
        fil.join(10)
        self.assertEqual((lu.statut, lu.sous_type), ("panne_transport", "delai"))
        self.assertTrue(S // 2 <= lu.fin - lu.depart < 2 * S, lu.fin - lu.depart)
        self.assertEqual(http.DELAI, 10 * S)                        # valeur scellée de l'ADR-0029, l.233

    def test_tlp6_derniere_attente_bornee_au_temps_qui_reste(self):
        def lent(conn, recues):                                     # un octet à 0,8 s, puis plus rien
            repondre(b"HTTP/1.1 200 OK\r\nContent-Length: 10\r\n\r\nx")(conn, recues)
            time.sleep(0.8)
            conn.sendall(b"x")
            conn.recv(1)                                            # jusqu'à la fermeture par le client
        port, _r, fil = servir(lent)
        lu = http.lire(http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=S)
        fil.join(10)
        self.assertEqual((lu.statut, lu.sous_type), ("panne_transport", "delai"))
        self.assertTrue(S <= lu.fin - lu.depart < 14 * S // 10, lu.fin - lu.depart)    # sans le temps qui reste : 1,8 s

    def test_corps_maximal_ecrit_sous_la_borne_de_ligne(self):
        """SHOGEN-S2BIS-CORPS-BORNE-1 : le plus grand corps que le client admet (PLAFOND octets reçus) donne une ligne
        `lecture` sous LIMITE, base64 compris : aucune lecture n'est perdue par JOURNAL/taille."""
        corps = bytes(range(256)) * (http.PLAFOND // 256)
        enrs = self.tourner({"p": lambda s: Lecture("ok", 0, 0, code=200, octets=corps)}, [(0, "p")])
        self.assertEqual((enrs[0]["type"], len(base64.b64decode(enrs[0]["brut"]))), ("lecture", http.PLAFOND))
        self.assertLess(max(map(len, self.etat()[FICHIER].split(b"\n"))), journal.LIMITE)
