"""CB-11, E-C-25 à E-C-29 : sondes de santé, commande d'horloge, requêtes DNS et lancement injectés ; branchement à la
boucle (liste blanche des clés de `sante`). sha256 de la configuration du résolveur par printf et sha256sum."""
import concurrent.futures
import os
import subprocess
import tempfile
import threading
import time
import types
import unittest

from shogen_s2bis.collecte import boucle, sante
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import D, Temps, rapide
from tests.test_journal import FICHIER, Base, chaine
from tests.test_reprise import m, sans_chaine

GELEE = b"sortie gelee, une ligne : 0.000012,0.25\n" + bytes([0xFF])           # octet hors UTF-8 : remplacé
RESOLV, EMPREINTE = b"nameserver 192.0.2.53\n", "d6bb96afccde62f60825d960dc109539de2c9c4de7315256247fea6f6fce77c5"
TEMOINS, NOMS = ["192.0.2.1", "192.0.2.2", "192.0.2.3"], ["a.example.", "b.example."]


class Faux:
    """Lancement de commande et requête DNS injectés : consignent leurs arguments, attendent `pause` s (ou `porte`)."""
    def __init__(self, pause=0, porte=None):
        self.pause, self.porte, self.appels = pause, porte, []

    def lancer(self, *a, **k):
        self.appels.append(("lancer", a, k))
        time.sleep(self.pause)
        return types.SimpleNamespace(stdout=GELEE, returncode=0)

    def interroger(self, *a, **k):
        self.appels.append(("interroger", a, k))
        time.sleep(self.pause)
        if self.porte:
            self.porte.wait(5)                                          # attente bornée : un mutant ne pend pas
        return {"statut": "reponse", "rcode": 0}


class Sondes(unittest.TestCase):
    def test_horloge_systeme_sortie_brute_ou_erreur_typee(self):
        instants = iter([10, 20])
        f = Faux()
        self.assertEqual(sante.horloge_systeme(["horloge", "-x"], lancer=f.lancer, horloge=lambda: next(instants)),
                         {"sortie": GELEE[:-1].decode() + chr(0xFFFD), "code": 0, "debut": 10, "fin": 20})
        self.assertEqual(f.appels, [("lancer", (["horloge", "-x"],), {"capture_output": True, "timeout": 2.0})])
        for erreur, attendu in ((FileNotFoundError(2, "absente"), "absente"), (PermissionError(13, "refus"), "autre"),
                                (subprocess.TimeoutExpired("h", 2), "delai")):
            def lancer(*a, **k):
                raise erreur
            with self.subTest(attendu=attendu):
                self.assertEqual(sante.horloge_systeme(["h"], lancer=lancer)["erreur"], attendu)
        long = sante.horloge_systeme(["h"], lancer=lambda *a, **k: types.SimpleNamespace(stdout=b"x" * 5000,
                                                                                         returncode=1))
        self.assertEqual((len(long["sortie"]), long["code"]), (4096, 1))

    def test_disque_et_empreinte_du_resolveur(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "resolv.conf"), "wb") as f:
                f.write(RESOLV)
            disque, v = sante.disque(d), os.statvfs(d)
            self.assertEqual(disque, {"total": v.f_blocks * v.f_frsize, "libre": v.f_bavail * v.f_frsize})
            self.assertEqual(sante.empreinte(os.path.join(d, "resolv.conf")), EMPREINTE)
            self.assertEqual((sante.disque(os.path.join(d, "absent")), sante.empreinte(os.path.join(d, "absent"))),
                             ({"erreur": "FileNotFoundError"}, None))

    def test_sondes_en_parallele_arguments_et_ordre(self):
        f = Faux(pause=0.3)
        s = sante.Sondes(["horloge"], TEMOINS, NOMS, "192.0.2.53", ".", interroger=f.interroger, lancer=f.lancer)
        t0 = time.monotonic()
        lancees = s.lancer()
        concurrent.futures.wait([x for _c, x in lancees], 5)
        self.assertLess(time.monotonic() - t0, 0.9)                        # en série : 6 × 0,3 s
        r = s.joindre(lancees)
        self.assertEqual((r["d3"]["code"], r["d4"], r["d5"]),
                         (0, [{"adresse": a, "statut": "reponse", "rcode": 0} for a in TEMOINS],
                          [{"nom": n, "statut": "reponse", "rcode": 0} for n in NOMS]))
        self.assertEqual(sorted(x[1:] for x in f.appels if x[0] == "interroger"),
                         sorted([((a, ".", "SOA"), {"recursion": False, "delai": 2 * S}) for a in TEMOINS] +
                                [(("192.0.2.53", n, "A"), {"recursion": True, "delai": 2 * S}) for n in NOMS]))

    def test_sonde_inachevee_vaut_null(self):
        porte = threading.Event()
        self.addCleanup(porte.set)
        f = Faux(porte=porte)
        s = sante.Sondes(["horloge"], TEMOINS[:1], NOMS[:1], "192.0.2.53", ".", interroger=f.interroger,
                         lancer=f.lancer)
        lancees = s.lancer()
        concurrent.futures.wait([lancees[0][1]], 5)                         # la sonde d'horloge finit seule
        r = s.joindre(lancees)
        self.assertEqual((r["d3"]["code"], r["d4"], r["d5"]), (0, [None], [None]))


class Branchement(Base):
    def test_sante_liste_blanche_sondes_au_depart_jointes_avant_l_echeance(self):
        temps, instants = Temps(m(2) * S + 5 * S), []

        def interroger(*a, **k):
            instants.append(temps())
            time.sleep(0.3)                                             # plus lente que la lecture
            return {"statut": "reponse"}
        s = sante.Sondes(["horloge"], TEMOINS[:1], NOMS[:1], "192.0.2.53", self.d, os.path.join(self.d, "absent"),
                         interroger=interroger, lancer=Faux().lancer)
        boucle.Boucle(self.journal(m(2)), {"a": rapide}, [(S, "a")], 8, horloge=temps, dormir=temps.dormir,
                      attendre=temps.attendre, sondes=s).tourner(1)
        enr = sans_chaine(chaine(self.etat()[FICHIER])[2])[-2]
        self.assertEqual((sorted(enr), sorted(enr["d2"]), sorted(enr["fils"])),
                         (["d2", "d3", "d4", "d5", "disque", "fils", "resolveur", "type", "ws"],
                          ["non_parties", "retard_max"], ["abandonnes", "tardives"]))
        self.assertEqual((enr["d3"]["code"], enr["d4"], enr["d5"], enr["resolveur"], instants),
                         (0, [{"adresse": TEMOINS[0], "statut": "reponse"}], [{"nom": NOMS[0], "statut": "reponse"}],
                          None, [D, D]))
        self.assertEqual(temps.appels[:2], [("dormir", D), ("dormir", D + S)])
