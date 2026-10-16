"""CB-11, E-C-25 à E-C-29 : sondes de santé, commande d'horloge, requêtes DNS et lancement injectés ; branchement à la
boucle (liste blanche des clés de `sante`). sha256 de la configuration du résolveur par printf et sha256sum. CB-11c
(G2 de P1-B) : boucle dans un fil joint en temps borné (C-6) ; sondes relevées à l'échéance (C-1). CB-11d : sonde
pendue jamais relancée, sondes vivantes comptées (C-5) ; disque du dossier du journal (MG-26). CB-18b
(SHOGEN-S2BIS-SONDES-ECHEANCE-1) : règle `fin` > E des sondes sur l'horloge monotone ; disque relevé après l'état
des futurs. CB-19b (C-1 (b) de la relecture d'intégration de P1) : témoin de la plus grande `sante`, sous LIMITE."""
import concurrent.futures
import os
import subprocess
import sys
import tempfile
import threading
import time
import types
import unittest
from unittest import mock

from shogen_s2bis.collecte import boucle, dns, entree, journal, sante
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import D, Lent, Temps, borne, rapide
from tests.test_journal import FICHIER, WS, Base, chaine
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
        self.assertEqual(f.appels, [("lancer", (["horloge", "-x"],), {"stdout": subprocess.PIPE,
                                                                      "stderr": subprocess.STDOUT, "timeout": 2.0})])
        for erreur, attendu in ((FileNotFoundError(2, "absente"), "absente"), (PermissionError(13, "refus"), "autre"),
                                (subprocess.TimeoutExpired("h", 2), "delai")):
            def lancer(*a, **k):
                raise erreur
            with self.subTest(attendu=attendu):
                self.assertEqual(sante.horloge_systeme(["h"], lancer=lancer)["erreur"], attendu)
        long = sante.horloge_systeme(["h"], lancer=lambda *a, **k: types.SimpleNamespace(stdout=b"x" * 5000,
                                                                                         returncode=1))
        self.assertEqual((len(long["sortie"]), long["code"]), (4096, 1))

    def test_sortie_d_erreur_gardee_dans_la_borne(self):  # DT6-e, SHOGEN-S2BIS-CHRONYC-FORMAT-1 (O-3 de la G2 de P1-B)
        """Commande réelle (l'interpréteur) qui écrit sur ses deux sorties puis sort en 1 : le message d'erreur, jeté
        avant DT6-e, est dans `sortie`, après la sortie standard ; un flot d'erreur reste coupé à 4 096 caractères."""
        ecrire = "import sys; sys.stdout.write('a'); sys.stdout.flush(); sys.stderr.write(%r); sys.exit(1)"
        r = [sante.horloge_systeme([sys.executable, "-c", ecrire % x], delai=10 * S) for x in (
            "506 Cannot talk to daemon", "e" * 5000)]
        self.assertEqual([(x["sortie"], x["code"]) for x in r],
                         [("a506 Cannot talk to daemon", 1), ("a" + "e" * 4095, 1)])

    def test_disque_et_empreinte_du_resolveur(self):
        """`disque` lit le statvfs du dossier donné, injecté ici (SHOGEN-S2BIS-TEST-DISQUE-INSTABLE-1 : deux lectures du
        vrai statvfs différaient de 4 096 octets libres sous écritures concurrentes) : total = f_blocks × f_frsize,
        libre = f_bavail × f_frsize (f_bsize et f_bfree, distincts, ne comptent pas) ; valeurs écrites à la main."""
        vus = []

        def statvfs(chemin):
            vus.append(chemin)
            return types.SimpleNamespace(f_bsize=8192, f_frsize=4096, f_blocks=1000, f_bfree=300, f_bavail=200)
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "resolv.conf"), "wb") as f:
                f.write(RESOLV)
            with mock.patch.object(os, "statvfs", statvfs):
                disque = sante.disque(d)
            self.assertEqual((disque, vus), ({"total": 4096000, "libre": 819200}, [d]))
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
        tard = s.joindre(lancees, 0)    # R-8 du contre-contrôle (DETTES-T6) : `fin` > E nulle chaque sonde, d3 comprise
        self.assertEqual((tard["d3"], tard["d4"], tard["d5"]), (None, [None] * 3, [None] * 2))
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

    def test_sonde_pendue_jamais_relancee(self):
        """C-5 : une sonde dont l'instance précédente n'a pas rendu n'est pas relancée (futur None, valeur null) ;
        `vivantes` compte les instances en cours ; elle repart dès que l'instance précédente a rendu."""
        porte = threading.Event()
        self.addCleanup(porte.set)
        f = Faux(porte=porte)
        s = sante.Sondes(["horloge"], TEMOINS[:1], NOMS[:1], "192.0.2.53", ".", interroger=f.interroger,
                         lancer=f.lancer)
        l1 = s.lancer()
        concurrent.futures.wait([l1[0][1]], 5)                              # la sonde d'horloge finit seule
        l2 = s.lancer()
        concurrent.futures.wait([l2[0][1]], 5)
        r = s.joindre(l2)
        self.assertEqual(([x is None for _c, x in l2], r["d3"]["code"], r["d4"], r["d5"], s.vivantes()),
                         ([False, True, True], 0, [None], [None], 2))
        porte.set()
        concurrent.futures.wait([x for _c, x in l1], 5)
        self.assertEqual(sorted(a[0] for a in f.appels), ["interroger", "interroger", "lancer", "lancer"])
        self.assertEqual([x is None for _c, x in s.lancer()], [False] * 3)

    def test_sonde_qui_leve_vaut_null_et_repart(self):
        """C-5 : une sonde qui lève vaut null ; son futur rend quand même, et elle repart à la fenêtre suivante."""
        def casse(*a, **k):
            raise RuntimeError("défaut imprévu")
        s = sante.Sondes(["horloge"], TEMOINS[:1], [], "192.0.2.53", ".", interroger=casse, lancer=Faux().lancer)
        l1 = s.lancer()
        concurrent.futures.wait([x for _c, x in l1], 5)
        self.assertEqual((s.joindre(l1)["d4"], [x is None for _c, x in s.lancer()]), ([None], [False, False]))

    def test_disque_et_empreinte_releves_apres_l_etat_des_futurs(self):    # CB-18b, SONDES-ECHEANCE-1
        """`joindre` relève l'état des futurs avant le disque et l'empreinte (deux entrées-sorties) : un témoin rendu
        pendant le relevé du disque (lent) n'était pas rendu, et vaut null. Sans échéance donnée, seul cet ordre en
        décide ; à la boucle, relevée après E, la règle `fin` > E le nulle aussi."""
        porte = threading.Event()
        self.addCleanup(porte.set)
        f = Faux(porte=porte)
        s = sante.Sondes(["horloge"], TEMOINS[:1], [], "192.0.2.53", ".", interroger=f.interroger, lancer=f.lancer)
        lancees = s.lancer()
        concurrent.futures.wait([lancees[0][1]], 5)                         # la sonde d'horloge finit seule

        def disque_lent(dossier):                                   # le témoin rend pendant le relevé du disque
            porte.set()
            concurrent.futures.wait([x for _c, x in lancees], 5)
            return {"total": 1, "libre": 1}
        with mock.patch.object(sante, "disque", disque_lent):
            r = s.joindre(lancees)
        self.assertEqual((r["d3"]["code"], r["d4"], r["disque"]), (0, [None], {"total": 1, "libre": 1}))

    def test_disque_du_dossier_du_journal(self):
        """MG-26 : `disque` se relève sur le dossier donné aux sondes (ici absent), jamais sur un autre."""
        with tempfile.TemporaryDirectory() as d:
            s = sante.Sondes(["horloge"], [], [], "192.0.2.53", os.path.join(d, "absent"), lancer=Faux().lancer)
            self.assertEqual(s.joindre([])["disque"], {"erreur": "FileNotFoundError"})


class Branchement(Base):
    def test_sante_liste_blanche_sondes_au_depart_jointes_avant_l_echeance(self):
        temps, instants = Temps(m(2) * S + 5 * S), []

        def interroger(*a, **k):
            instants.append(temps())
            time.sleep(0.3)                                             # plus lente que la lecture
            return {"statut": "reponse"}
        s = sante.Sondes(["horloge"], TEMOINS[:1], NOMS[:1], "192.0.2.53", self.d, os.path.join(self.d, "absent"),
                         interroger=interroger, lancer=Faux().lancer)
        jl = borne(self, self.journal, m(2))                        # ouvert dans le fil de la boucle (CB-18a)
        borne(self, boucle.Boucle(jl, {"a": rapide}, [(S, "a")], 8, horloge=temps, dormir=temps.dormir,
                                  attendre=temps.attendre, sondes=s).tourner, 1)
        enr = sans_chaine(chaine(self.etat()[FICHIER])[2])[-2]
        self.assertEqual((sorted(enr), sorted(enr["d2"]), sorted(enr["fils"])),
                         (["d2", "d3", "d4", "d5", "disque", "fils", "horloges", "resolveur", "type", "ws"],
                          ["non_parties", "retard_max"], ["abandonnes", "sondes", "tardives"]))
        self.assertEqual((enr["d3"]["code"], enr["d4"], enr["d5"], enr["resolveur"], instants),
                         (0, [{"adresse": TEMOINS[0], "statut": "reponse"}], [{"nom": NOMS[0], "statut": "reponse"}],
                          None, [D, D]))
        self.assertEqual(temps.appels[:2], [("dormir", D), ("dormir", D + S)])

    def test_sonde_finie_apres_l_echeance_vaut_null(self):
        """C-1 : les sondes sont relevées avec les lectures, une seule fois à l'échéance, avant toute écriture : une
        sonde qui rend pendant l'écriture des lectures (écrivain ralenti) vaut null."""
        temps, porte = Temps(m(2) * S + 5 * S), threading.Event()
        self.addCleanup(porte.set)

        def interroger(*a, **k):
            porte.wait(5)
            return {"statut": "reponse"}
        s = sante.Sondes(["horloge"], TEMOINS[:1], [], "192.0.2.53", self.d, interroger=interroger,
                         lancer=Faux().lancer)
        b = boucle.Boucle(Lent(borne(self, self.journal, m(2)), temps, porte), {"a": rapide}, [(0, "a")], 8,
                          horloge=temps, dormir=temps.dormir, attendre=temps.attendre, sondes=s)
        borne(self, b.tourner, 1)
        enr = sans_chaine(chaine(self.etat()[FICHIER])[2])[-2]
        self.assertEqual((enr["type"], enr["d3"]["code"], enr["d4"]), ("sante", 0, [None]))

    def test_sondes_pendues_trois_fenetres_fils_constants(self):
        """C-5 : sondes pendues sur trois fenêtres : jamais relancées (trois fils de sonde en tout, toujours vivants),
        null à chaque fenêtre ; `fils.sondes` journalise les sondes vivantes."""
        temps, porte, fils = Temps(m(2) * S + 5 * S), threading.Event(), []
        self.addCleanup(porte.set)

        def pendre(*a, **k):
            fils.append(threading.current_thread())
            porte.wait(5)
            return {"statut": "reponse"}
        s = sante.Sondes(["horloge"], TEMOINS[:1], NOMS[:1], "192.0.2.53", self.d, interroger=pendre,
                         lancer=lambda *a, **k: pendre() and types.SimpleNamespace(stdout=b"", returncode=0))
        b = boucle.Boucle(borne(self, self.journal, m(2)), {"a": rapide}, [(0, "a")], 8, horloge=temps,
                          dormir=temps.dormir, attendre=temps.attendre, sondes=s)
        comptes = []
        for _ in range(3):
            borne(self, b.tourner, 1)
            comptes.append((len(fils), sum(f.is_alive() for f in fils)))
        enrs = [e for e in sans_chaine(chaine(self.etat()[FICHIER])[2]) if e["type"] == "sante"]
        self.assertEqual([(e["d3"], e["d4"], e["d5"], e["fils"]["sondes"]) for e in enrs],
                         [(None, [None], [None], 3)] * 3)
        self.assertEqual(comptes, [(3, 3)] * 3)

    def test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null(self):  # CB-18b, SONDES-ECHEANCE-1
        """Règle `fin` > E appliquée aux sondes, sur l'horloge monotone de la boucle (E-1 des corrections de P1-B) :
        l'attente déborde de 1 ms ; le premier témoin, rendu à E, est gardé ; le second, rendu après E mais avant le
        relevé, vaut null. La lecture et d3, rendues avant E, sont attendues d'abord ; d3 rend 20 ms réelles après son
        départ (DT6-u, SHOGEN-S2BIS-TEST-SANTE-CHARGE-1 : sans cette attente, un fil de d3 retardé par la charge
        rendait après E + 1 ms et d3 valait null : ERROR une fois en 81 suites chargées)."""
        temps, portes = Temps(m(2) * S + 5 * S), [threading.Event(), threading.Event()]
        for p in portes:
            self.addCleanup(p.set)

        def interroger(a, *x, **k):
            portes[TEMOINS.index(a)].wait(5)
            return {"statut": "reponse"}

        def attendre(futurs, t):                                    # futurs : lecture, d3, puis les deux témoins
            concurrent.futures.wait(futurs[:2], 5)                  # DT6-u : lecture et d3 rendues avant E
            for porte, futur, instant in zip(portes, futurs[2:], (t, t + 1000)):
                temps.avancer(instant)
                porte.set()
                concurrent.futures.wait([futur], 5)
        s = sante.Sondes(["horloge"], TEMOINS[:2], [], "192.0.2.53", self.d, interroger=interroger,
                         lancer=Faux(pause=0.02).lancer)
        jl = borne(self, self.journal, m(2))
        borne(self, boucle.Boucle(jl, {"a": rapide}, [(0, "a")], 8, horloge=temps, dormir=temps.dormir,
                                  attendre=attendre, sondes=s, monotone=temps.monotone).tourner, 1)
        enr = sans_chaine(chaine(self.etat()[FICHIER])[2])[-2]
        self.assertEqual((enr["d3"]["code"], enr["d4"]), (0, [{"adresse": TEMOINS[0], "statut": "reponse"}, None]))


class Taille(Base):
    def test_plus_grande_sante_sous_la_borne_de_ligne(self):          # CB-19b, C-1 (b) de la relecture d'intégration
        """Témoin du FORMAT §13.6 : chaque champ de `sante` à sa borne, lue au code (témoins et noms au plus, longueur
        d'un nom, places du pool, sortie de D-3, taille d'une réponse UDP) ; `reponses` de chaque sonde : 14 réponses
        SOA dont les trois noms ont 2 × 512 caractères de contrôle, au-delà de la borne 1 + 495 × (18 × 1 024 + 85) / 36
        du FORMAT ; `tardives` : 2 × places ; entiers à leur plus longue écriture. Ligne canonique de 3 823 224 octets
        (calcul du FORMAT, recompté), sous LIMITE ; l'écrivain écrit ces champs sans refus."""
        sch, i17, i18 = entree.SCHEMAS, -(10 ** 16 - 1), -(10 ** 17 - 1)
        t, n, long_nom = sch["sante"]["temoins"][-1], sch["sante"]["noms"][-1], sch["sante"]["noms"][0][2]
        self.assertEqual((type(t), type(n)), (int, int))             # nombre de témoins et de noms borné au schéma
        nom = chr(1) * 2 * dns.UDP
        r = {"debut": i17, "fin": i17, "rcode": None, "statut": "reponse", "tc": False,
             "reponses": [[nom, 65535, 2 ** 32 - 1, [nom, nom, *[2 ** 32 - 1] * 5]]] * 14}
        champs = {"d2": {"non_parties": 10 ** 19 - 1, "retard_max": i18}, "horloges": {"monotone": i18, "murale": i18},
                  "fils": {"abandonnes": 10 ** 19 - 1, "sondes": 10 ** 19 - 1,
                           "tardives": [i18] * 2 * sch["formes"]["places"][2]},
                  "d3": {"code": -2 ** 31, "debut": i17, "fin": i17, "sortie": chr(1) * sante.SORTIE},
                  "d4": [{"adresse": "255.255.255.255", **r}] * t, "d5": [{"nom": chr(1) * long_nom, **r}] * n,
                  "disque": {"libre": 2 ** 128 - 1, "total": 2 ** 128 - 1}, "resolveur": "f" * 64}
        ligne = journal.canonique({**champs, "type": "sante", "ws": -(10 ** 10 - 1), "seq": 10 ** 640 - 1,
                                   "prec": "f" * 64})
        self.assertEqual((len(ligne), len(ligne) < journal.LIMITE), (3823224, True))
        self.journal().ecrire("sante", WS + 60, **champs)
        self.assertLess(len(self.etat()[FICHIER].split(bytes([10]))[-2]), 3823224)
