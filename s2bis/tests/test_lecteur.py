"""RB-1 : lecteur en flux des journaux (E-R-01, E-R-02 ; FORMAT §1 à §8). Lignes fabriquées ici (`ligne`, de
tests/test_reprise.py) et journaux synthétiques écrits par l'écrivain de collecte/journal.py, aucun journal de
campagne ; attendus recalculés par `chaine` (tests/test_journal.py), code de test indépendant du lecteur ; empreintes
par hashlib sur les octets du test. Lettres C-1 à C-5 du FORMAT, corrections C-14 et C-15 de la G2 de RB-18 : types,
ordres et bornes pris au texte du FORMAT de la tête, non au code."""
import hashlib
import json
import os
import sys
import tempfile
import tracemalloc
import unittest

from shogen_s2bis.recalc import lecteur as lec
from tests.test_fichiers import J1, J2, J3, NOMS
from tests.test_journal import FICHIER, Base, chaine
from tests.test_reprise import SEG1, SEG2, ligne, m

OUVERTURE = ligne(0, "0" * 64, type="ouverture", jour="2026-10-04", suivante=m(1))
P = hashlib.sha256(OUVERTURE).hexdigest()
JOUR = "2026-10-04"
TYPES = {"ouverture": {"jour": JOUR, "suivante": m(1)}, "marqueur": {"ws": m(1)}, "point": {"ws": m(1)},
         "cloture": {"jour": JOUR}, "reprise": {"ws": m(1), "suivante": m(1), "queue": None},
         "trou": {"de": m(1), "a": m(1), "cause": "saut"}, "lecture": {"ws": m(1)}, "sante": {"ws": m(1)},
         "run_params": {"ws": m(1)}}        # champs propres et leurs types, pris à la lettre (FORMAT §2, §7.1 d)


def verdict(octets, etat):
    """Cause nommée du refus de `_integre`, ou « intègre »."""
    try:
        lec._integre(octets, etat)
    except lec._NonIntegre as e:
        return e.args[0]
    return "intègre"


class LigneIntegre(unittest.TestCase):                      # FORMAT §7.1 ; écrivain de référence : `_lire`
    def test_lignes_integres_et_etat(self):
        e, etat = lec._integre(OUVERTURE, None)
        lecture = ligne(1, P, type="lecture", ws=m(1), k=1)
        e2, etat2 = lec._integre(lecture, etat)
        trou = ligne(2, etat2[1], type="trou", de=m(2), a=m(3), cause="saut")
        etat3 = lec._integre(trou, etat2)[1]
        marqueur = ligne(3, etat3[1], type="marqueur", ws=m(4))  # C-4 : ws et a retenus (l'écrivain : ws + w, a + w)
        self.assertEqual((e["type"], etat, e2["k"], etat2, etat3, lec._integre(marqueur, etat3)[1]), (
            "ouverture", (1, P, m(1), None), 1, (2, hashlib.sha256(lecture).hexdigest(), m(1), m(1)),
            (3, hashlib.sha256(trou).hexdigest(), m(3), m(1)), (4, hashlib.sha256(marqueur).hexdigest(), m(4), m(4))))
        etat4 = lec._integre(marqueur, etat3)[1]
        point = ligne(4, etat4[1], type="point", ws=m(9))         # réservé (§2) : ni attendu ni dernière fenêtre
        self.assertEqual(lec._integre(point, etat4)[1], (5, hashlib.sha256(point).hexdigest(), m(4), m(4)))

    def test_causes_nommees(self):
        etat = lec._integre(OUVERTURE, None)[1]
        lect = {"type": "lecture", "ws": m(1)}
        for cause, octets, avant in (("LECTEUR/fin", OUVERTURE[:-1], None), ("LECTEUR/json", bytes(9) + b"\n", etat),
                                     ("LECTEUR/json", b"[" * 100000 + b"]" * 100000 + b"\n", etat),
                                     ("LECTEUR/canonique", ligne(1, P, (", ", ": "), **lect), etat),
                                     ("LECTEUR/canonique", b'{"seq":1,' + ligne(1, P, **lect)[1:].replace(
                                         b'"seq":1,', b""), etat),                              # clés non triées
                                     ("LECTEUR/chaine", ligne(1, "0" * 64, **lect), etat),
                                     ("LECTEUR/chaine", ligne(2, P, **lect), etat),
                                     ("LECTEUR/chaine", ligne(0, "0" * 64, **lect), None),       # première ligne
                                     ("LECTEUR/champ", ligne(1, P, type="lecture", ws="23:02"), etat),
                                     ("LECTEUR/champ", ligne(1, P, type="marqueur", ws=True), etat),
                                     ("LECTEUR/champ", ligne(1, P, ws=m(1)), etat),
                                     ("LECTEUR/champ", ligne(1, P, type="lecture"), etat),
                                     ("LECTEUR/champ", ligne(0, "0" * 64, type="ouverture"), None),
                                     ("LECTEUR/champ", ligne(0, "0" * 64, type="ouverture", suivante="x"), None),
                                     ("LECTEUR/flottant", ligne(1, P, x=0.5, **lect), etat),
                                     ("LECTEUR/flottant", ligne(1, P, x=float("nan"), **lect), etat),
                                     ("LECTEUR/entier-long", ligne(1, P, x=10 ** 640, **lect), etat)):
            with self.subTest(cause=cause, octets=octets[:50]):
                with self.assertRaises(lec._NonIntegre) as e:
                    lec._integre(octets, avant)
                self.assertEqual(e.exception.args[0], cause)

    def test_entier_de_640_chiffres_lu_641_nomme_quel_que_soit_le_reglage(self):
        etat, reglage = lec._integre(OUVERTURE, None)[1], sys.get_int_max_str_digits()
        lus = [ligne(1, P, type="lecture", ws=m(1), x=x) for x in (10 ** 639, -10 ** 639)]
        nommes = [ligne(1, P, type="lecture", ws=m(1), x=x) for x in (10 ** 640, -10 ** 640)]
        for limite in (0, 640, 4300):                           # 0 : sans limite ; 640 : plus petite limite admise
            sys.set_int_max_str_digits(limite)
            try:
                valeurs, causes = [lec._integre(x, etat)[0]["x"] for x in lus], []
                for x in nommes:
                    with self.assertRaises(lec._NonIntegre) as e:
                        lec._integre(x, etat)
                    causes.append(e.exception.args[0])
            finally:
                sys.set_int_max_str_digits(reglage)
            self.assertEqual((valeurs == [10 ** 639, -10 ** 639], causes), (True, ["LECTEUR/entier-long"] * 2), limite)

    def test_champs_propres_aux_types_du_paragraphe_2(self):          # C-2 (FORMAT §7.1 d) ; C-14 : `a` booléen
        """Chaque champ propre au type de la lettre laisse la ligne intègre ; à un autre type (un booléen n'est jamais
        un entier ; null compris) ou absent, il la rend non intègre. `ws` d'un type non réservé : requis, entier."""
        etat = lec._integre(OUVERTURE, None)[1]
        for genre, champs in TYPES.items():
            for champ, bon in champs.items():
                mauvais = ([{}, "x", 5, True] if champ == "queue" else [5, True, None, []] if type(bon) is str else
                           ["60", True, False, None, {}])
                octets = [ligne(1, P, type=genre, **{**champs, champ: v}) for v in [bon, *mauvais]] + [
                    ligne(1, P, type=genre, **{k: v for k, v in champs.items() if k != champ})]
                with self.subTest(type=genre, champ=champ):
                    self.assertEqual([verdict(x, etat) for x in octets],
                                     ["intègre"] + ["LECTEUR/champ"] * (len(mauvais) + 1))
        self.assertEqual([verdict(ligne(1, P, type="reprise", ws=m(1), suivante=m(1), queue=q), etat) for q in (
            [], [{"fichier": "f"}])], ["intègre"] * 2)             # une liste : son contenu relève du §7.4

    def test_champs_communs_et_objet(self):                          # C-2 (FORMAT §7.1 b, c) ; C-14 : seq, prec
        """`type` chaîne ; `seq` entier, jamais booléen (True == 1 en Python) ; `prec` de 64 chiffres hexadécimaux
        minuscules, en tête de fichier aussi ; une ligne JSON qui n'est pas un objet n'est pas intègre."""
        etat, tete = lec._integre(OUVERTURE, None)[1], {"type": "ouverture", **TYPES["ouverture"]}
        lect, sep = {"type": "lecture", "ws": m(1)}, (",", ":")
        refus = [(ligne(1, P, **{**lect, "type": t}), etat) for t in (5, None, ["lecture"], {})] + [
            (ligne(s, P, **lect), etat) for s in (True, "1", None)] + [(ligne(True, "0" * 64, **tete), None)] + [
            (ligne(0, p, **tete), None) for p in ("0" * 63, "0" * 65, "A" * 64, "g" * 64, None, 0)] + [
            (json.dumps({"seq": 0, **tete}, sort_keys=True, separators=sep).encode() + b"\n", None)] + [
            (x + b"\n", etat) for x in (b"[1]", b'"x"', b"5", b"null")]
        self.assertEqual([verdict(x, e) for x, e in refus], ["LECTEUR/champ"] * len(refus))
        self.assertEqual([verdict(ligne(0, p, **tete), None) for p in ("0" * 64, "a" * 64, "0123456789abcdef" * 4)],
                         ["intègre"] * 3)                        # en tête, le lien se juge à part (§7.7)

    def test_caracteres_hors_ascii_en_clair(self):                    # C-2 (FORMAT §7.1 b, §1.2)
        """Canonique : un caractère hors ASCII s'écrit en UTF-8, jamais en séquence d'échappement ; « é » en clair
        laisse la ligne intègre, sa séquence d'échappement la rend non intègre (`LECTEUR/canonique`)."""
        etat = lec._integre(OUVERTURE, None)[1]
        clair = ligne(1, P, type="lecture", ws=m(1), note="X").replace(b'"X"', '"é"'.encode())
        echappee = ligne(1, P, type="lecture", ws=m(1), note="é")      # json.dumps échappe par défaut
        self.assertEqual((verdict(clair, etat), lec._integre(clair, etat)[0]["note"], verdict(echappee, etat)),
                         ("intègre", "é", "LECTEUR/canonique"))

    def test_ws_null_type_par_type(self):                            # C-2, risque R-2 de l'avis (FORMAT §7.1)
        """`ws` null rend non intègre toute ligne d'un type qui porte `ws` (marqueur, point, reprise, type non
        réservé) ; ouverture, cloture et trou n'ont pas `ws` parmi leurs champs propres : là, un `ws` null est un champ
        ordinaire et la ligne reste intègre (définition ni relâchée ni resserrée)."""
        etat = lec._integre(OUVERTURE, None)[1]
        self.assertEqual({t: verdict(ligne(1, P, type=t, **{**c, "ws": None}), etat) for t, c in TYPES.items()},
                         {**dict.fromkeys(TYPES, "LECTEUR/champ"), **dict.fromkeys(("ouverture", "cloture", "trou"),
                                                                                    "intègre")})


class Fichiers(unittest.TestCase):
    def test_ordre_de_la_chaine_et_journal_absent(self):  # segments en ordre numérique ; autres fichiers ignorés
        with tempfile.TemporaryDirectory() as d:
            for n in ("pool-2026-10-04-10.jsonl", "pool-2026-10-05-0.jsonl", "pool-2026-10-04-2.jsonl", "pool.sha256",
                      "pool.verrou", "secondaire-2026-10-04-0.jsonl", "pool-2026-10-04-1.jsonl.bak"):
                open(os.path.join(d, n), "wb").close()
            self.assertEqual(lec.Lecteur(d, "pool").fichiers(), ["pool-2026-10-04-2.jsonl", "pool-2026-10-04-10.jsonl",
                                                                 "pool-2026-10-05-0.jsonl"])
            with self.assertRaises(lec.RefusLecteur) as e:
                lec.Lecteur(d, "carte").fichiers()
            self.assertEqual(e.exception.code, "LECTEUR/absent")


def lire(dossier, prefixe="pool"):
    lecteur = lec.Lecteur(dossier, prefixe)
    return lecteur, list(lecteur)


def queue(nom, position, octets, cause):
    return {"fichier": nom, "position": position, "octets": len(octets), "sha256": hashlib.sha256(octets).hexdigest(),
            "cause": cause}


def jours(test, fenetres=(J1, J2, J2 + 60, J3, J3 + 60)):
    """Journal ouvert le 2026-10-04 à 23:58 : une lecture et un marqueur par fenêtre de `fenetres`, sur un à trois jours
    UTC (les fenêtres sautées : `trou` de l'écrivain) ; flux courts, diff rapide en cas d'échec ; rend la tête."""
    jl = test.journal(J1 - 60)
    for ws in fenetres:
        jl.ecrire("lecture", ws, k=ws % 7)
        tete = jl.marqueur(ws)
    jl.fermer()
    return tete


class Lecture(Base):
    def attendus(self, noms, seq=0, prec="0" * 64):
        """Enregistrements des fichiers `noms`, chaîne recalculée par le test depuis (seq, prec) ; et la tête."""
        sortie, octets = [], self.etat()
        for n in noms:
            seq, prec, enrs = chaine(octets[n], seq, prec)
            sortie += [("enr", n, x) for x in enrs]
        return sortie, (seq - 1, prec)

    def ancre(self, nom):
        premier = json.loads(self.etat()[nom].split(b"\n")[0])
        return premier["seq"], premier["prec"]

    def test_journal_de_l_ecrivain_lu_en_entier(self):
        tete = jours(self)
        lecteur, flux = lire(self.d)
        self.assertEqual((flux, lecteur.tete, lecteur.ruptures, lecteur.queue_finale),
                         (self.attendus(NOMS)[0], tete, [], []))

    def test_fichier_retire_lien_rompu_puis_ancre(self):     # FORMAT §7.7 : lien d'un fichier au précédent
        tete = jours(self)
        os.remove(os.path.join(self.d, NOMS[1]))
        (avant, apres), (suite, _t) = self.attendus(NOMS[:1]), self.attendus(NOMS[2:], *self.ancre(NOMS[2]))
        rupture = {"code": "LECTEUR/lien", "fichier": NOMS[2], "seq": self.ancre(NOMS[2])[0], "apres": apres,
                   "queues": []}
        lecteur, flux = lire(self.d)
        self.assertEqual((flux, lecteur.tete, lecteur.ruptures), (avant + [("rupture", rupture)] + suite, tete,
                                                                  [rupture]))
        self.assertEqual((list(lecteur), lecteur.ruptures), (flux, [rupture]))     # seconde lecture : état remis à zéro

    def test_genese_absente(self):                          # premier enregistrement : seq 0, prec nul, ouverture
        jours(self, (J1, J2, J2 + 60))
        os.remove(os.path.join(self.d, NOMS[0]))
        rupture = {"code": "LECTEUR/lien", "fichier": NOMS[1], "seq": self.ancre(NOMS[1])[0], "apres": None,
                   "queues": []}
        _lecteur, flux = lire(self.d)
        self.assertEqual(flux, [("rupture", rupture)] + self.attendus(NOMS[1:2], *self.ancre(NOMS[1]))[0])

    def test_derniere_ligne_d_un_fichier_alteree_lien_rompu_par_l_empreinte(self):   # seq continu, prec faux
        jours(self)
        clos = self.etat()[NOMS[0]]
        i = clos.rindex(b'"jour":"2026-10-04"')                 # la clôture seule, toujours canonique et chaînée
        with open(os.path.join(self.d, NOMS[0]), "wb") as f:
            f.write(clos[:i] + b'"jour":"2026-10-03"' + clos[i + 19:])
        lecteur, _flux = lire(self.d)
        self.assertEqual([(x["code"], x["fichier"], x["seq"]) for x in lecteur.ruptures],
                         [("LECTEUR/lien", NOMS[1], chaine(clos)[0])])

    def test_genese_par_une_reprise_refusee(self):
        with open(os.path.join(self.d, FICHIER), "wb") as f:
            f.write(ligne(0, "0" * 64, type="reprise", ws=m(1), suivante=m(2), queue=None))
        lecteur, flux = lire(self.d)
        self.assertEqual([x[0] for x in flux], ["rupture", "enr"])


class AvecQueues(Base):
    def preparer(self):
        """Lectures et marqueurs de 22:59 à 23:01, lecture de 23:02 sans marqueur (tests/test_reprise.py)."""
        jl = self.journal()
        for n in (1, 2, 3, 4):
            jl.ecrire("lecture", m(n), k=n)
            if n < 4:
                jl.marqueur(m(n))
        jl.fermer()
        return self.etat()[FICHIER]

    def ajouter(self, nom, octets):
        with open(os.path.join(self.d, nom), "ab") as f:
            f.write(octets)


class Queues(AvecQueues):
    def test_queue_finale_toleree_jusqu_a_la_fin_du_fichier(self):   # une ligne d'allure intègre y reste
        for cause, fabrique in (("LECTEUR/fin", lambda s, p: b'{"k":4'),
                                ("LECTEUR/json", lambda s, p: bytes(9) + b"\n" + OUVERTURE),
                                ("LECTEUR/entier-long", lambda s, p: ligne(s, p, type="lecture", ws=m(4),
                                                                           x=10 ** 640) + OUVERTURE),
                                ("LECTEUR/fin", lambda s, p: ligne(s, p, type="lecture", ws=m(4), x="a" * lec.LIMITE))):
            with self.subTest(cause=cause):
                self.setUp()
                intact = self.preparer()
                seq, prec, enrs = chaine(intact)
                self.ajouter(FICHIER, fabrique(seq, prec))
                lecteur, flux = lire(self.d)
                self.assertEqual((flux, lecteur.tete, lecteur.ruptures, lecteur.queue_finale),
                                 ([("enr", FICHIER, x) for x in enrs], (seq - 1, prec), [],
                                  [queue(FICHIER, len(intact), fabrique(seq, prec), cause)]))

    def test_ligne_de_limite_octets_integre_un_octet_de_plus_queue(self):   # C-2 (FORMAT §7.1 a)
        """LIMITE = 4 194 304 octets (valeur de la lettre) : une ligne de LIMITE octets, saut compris, est intègre ;
        d'un octet de plus, elle forme la queue du fichier (`LECTEUR/fin` : lue jusqu'à LIMITE octets, sans saut)."""
        for de_plus in (0, 1):
            with self.subTest(de_plus=de_plus):
                self.setUp()
                intact = self.preparer()
                seq, prec, enrs = chaine(intact)
                vide = ligne(seq, prec, type="lecture", ws=m(4), x="")
                longue = ligne(seq, prec, type="lecture", ws=m(4), x="a" * (4194304 - len(vide) + de_plus))
                self.ajouter(FICHIER, longue)
                lecteur, flux = lire(self.d)
                self.assertEqual((len(longue), len(flux), lecteur.queue_finale), (4194304 + de_plus, len(enrs) + 1 -
                                 de_plus, [queue(FICHIER, len(intact), longue, "LECTEUR/fin")] if de_plus else []))

    def test_queue_non_declaree_suivie_d_un_fichier(self):
        jours(self, (J1, J2, J2 + 60))
        clos = self.etat()[NOMS[0]]
        self.ajouter(NOMS[0], b"queue\n")                       # après la clôture du 2026-10-04
        seq, prec, enrs = chaine(clos)
        rupture = {"code": "LECTEUR/queue-non-declaree", "fichier": NOMS[1], "seq": seq, "apres": (seq - 1, prec),
                   "queues": [queue(NOMS[0], len(clos), b"queue\n", "LECTEUR/json")]}
        _lecteur, flux = lire(self.d)
        self.assertEqual(flux, [("enr", NOMS[0], x) for x in enrs] + [("rupture", rupture)] + [
            ("enr", NOMS[1], x) for x in chaine(self.etat()[NOMS[1]], seq, prec)[2]])


class Declarations(AvecQueues):
    def test_reprise_dans_le_meme_fichier_puis_queue_declaree(self):
        self.preparer()
        self.journal(m(7)).fermer()                             # reprise dans le même fichier : queue null
        avant, coupee = self.etat()[FICHIER], b'{"k":4,"prec":"5e3'
        self.ajouter(FICHIER, coupee)
        self.journal(m(9)).fermer()                             # segment 1 : sa reprise déclare la queue
        seq, prec, enrs = chaine(avant)
        suite = chaine(self.etat()[SEG1], seq, prec)[2]
        lecteur, flux = lire(self.d)
        self.assertEqual((flux, lecteur.ruptures, lecteur.queues, lecteur.queue_finale),
                         ([("enr", FICHIER, x) for x in enrs] + [("enr", SEG1, x) for x in suite], [],
                          [queue(FICHIER, len(avant), coupee, "LECTEUR/fin")], []))

    def test_declaration_alteree_rupture(self):              # un octet de la queue change après sa déclaration
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        self.ajouter(FICHIER, b'{"k":4,"prec":"5e3')
        self.journal(m(7)).fermer()
        with open(os.path.join(self.d, FICHIER), "r+b") as f:
            f.seek(len(intact) + 2)
            f.write(b"K")
        lecteur, _flux = lire(self.d)
        observee = queue(FICHIER, len(intact), b'{"K":4,"prec":"5e3', "LECTEUR/fin")
        self.assertEqual((lecteur.ruptures, lecteur.queues), ([{"code": "LECTEUR/declaration", "fichier": SEG1,
                                                                "seq": seq, "apres": (seq - 1, prec),
                                                                "queues": [observee]}], []))

    def test_memoire_bornee_independante_de_la_longueur(self):   # pic de tracemalloc, tailles 1 et 4
        pics = []
        for n in (500, 2000):
            self.setUp()
            jl = self.journal()
            for i in range(n):
                jl.ecrire("lecture", m(1 + i // 50), k=i, x="a" * 200)
            jl.fermer()
            tracemalloc.start()
            for _x in lec.Lecteur(self.d, "pool"):
                pass
            pics.append((tracemalloc.get_traced_memory()[1], os.path.getsize(os.path.join(self.d, FICHIER))))
            tracemalloc.stop()
        (p1, _t1), (p4, t4) = pics
        self.assertTrue(p4 < p1 + 32768 and p4 < t4 // 4, pics)


def declaree(q):                                             # champs déclarés d'une queue (FORMAT §7.4)
    return {k: q[k] for k in ("fichier", "position", "octets", "sha256")}


class Pannes(AvecQueues):              # C-2 de la G2 de RB-T1 : un cas par mutant vivant (G-13 à G-16, G-19, G-20)
    def coupe(self):
        """Journal de `preparer` puis ligne coupée par une panne : (seq, prec) exigés ensuite, queue relevée."""
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        self.ajouter(FICHIER, b'{"k":4,"prec":"5e3')
        return seq, prec, queue(FICHIER, len(intact), b'{"k":4,"prec":"5e3', "LECTEUR/fin")

    def reprise(self, seq, prec, queues):                     # reprise écrite par le test (FORMAT §7.4)
        return ligne(seq, prec, type="reprise", ws=m(9), suivante=m(4), queue=queues)

    def rupture(self, code, fichier, seq, prec, queues):
        return [{"code": code, "fichier": fichier, "seq": seq, "apres": (seq - 1, prec), "queues": queues}]

    def test_reprise_a_queue_nulle_derriere_une_queue(self):            # G-13
        seq, prec, q = self.coupe()
        self.ajouter(SEG1, self.reprise(seq, prec, None))
        lecteur, _flux = lire(self.d)
        self.assertEqual((lecteur.ruptures, lecteur.queues),
                         (self.rupture("LECTEUR/declaration", SEG1, seq, prec, [q]), []))

    def test_reprise_declarant_une_queue_quand_aucune_n_attend(self):    # G-14
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        self.ajouter(FICHIER, self.reprise(seq, prec, [declaree(queue(FICHIER, len(intact), b"x", ""))]))
        lecteur, _flux = lire(self.d)
        self.assertEqual(lecteur.ruptures, self.rupture("LECTEUR/declaration", FICHIER, seq, prec, []))

    def test_deux_queues_en_fin_de_journal(self):                       # G-15 : reprise coupée par une seconde panne
        seq, prec, q = self.coupe()
        coupee = self.reprise(seq, prec, [declaree(q)])[:40]
        self.ajouter(SEG1, coupee)
        lecteur, _flux = lire(self.d)
        self.assertEqual((lecteur.ruptures, lecteur.queues, lecteur.queue_finale),
                         ([], [], [q, queue(SEG1, 0, coupee, "LECTEUR/fin")]))

    def test_deux_queues_declarees_ensemble_par_l_ecrivain(self):       # G-16 : deux pannes, puis l'écrivain réel
        seq, prec, q = self.coupe()
        coupee = self.reprise(seq, prec, [declaree(q)])[:40]
        self.ajouter(SEG1, coupee)
        self.journal(m(11)).fermer()                            # segment 2 : sa reprise déclare les deux queues
        q1 = queue(SEG1, 0, coupee, "LECTEUR/fin")
        lecteur, _flux = lire(self.d)
        self.assertEqual((chaine(self.etat()[SEG2], seq, prec)[2][0]["queue"], lecteur.ruptures, lecteur.queues,
                          lecteur.queue_finale), ([declaree(q), declaree(q1)], [], [q, q1], []))

    def test_queue_d_un_octet_relevee(self):                            # G-19
        intact = self.preparer()
        self.ajouter(FICHIER, b"{")
        lecteur, _flux = lire(self.d)
        self.assertEqual(lecteur.queue_finale, [queue(FICHIER, len(intact), b"{", "LECTEUR/fin")])

    def test_reprise_en_tete_de_segment_au_lien_faux(self):              # G-20 : déclaration exacte, prec faux
        seq, prec, q = self.coupe()
        self.ajouter(SEG1, self.reprise(seq, "f" * 64, [declaree(q)]))
        lecteur, _flux = lire(self.d)
        self.assertEqual((lecteur.ruptures, lecteur.queues), (self.rupture("LECTEUR/lien", SEG1, seq, prec, [q]), []))

    def test_tete_de_segment_non_integre_par_ses_types(self):          # C-2, C-14 : le §7.1 avant le §7.4
        """Reprise en tête de segment dont `queue` est un objet nu (§7.1 d), ou dont `prec` est en majuscules (§7.1 c) :
        la ligne n'est pas intègre, donc ni rupture ni déclaration ; les deux queues restent en fin de journal."""
        for nom, fabrique in (("objet nu", lambda s, p, q: self.reprise(s, p, {})),
                              ("prec en majuscules", lambda s, p, q: self.reprise(s, p.upper(), [declaree(q)]))):
            with self.subTest(nom):
                self.setUp()
                seq, prec, q = self.coupe()
                tete = fabrique(seq, prec, q)
                self.ajouter(SEG1, tete)
                lecteur, _flux = lire(self.d)
                self.assertEqual((prec != prec.upper(), lecteur.ruptures, lecteur.queues, lecteur.queue_finale),
                                 (True, [], [], [q, queue(SEG1, 0, tete, "LECTEUR/champ")]))

    def test_declaration_exacte_sous_forme_canonique(self):            # C-15, C-3 (FORMAT §7.4)
        """Deux queues en attente (ligne coupée du jour, segment sans ligne intègre) : seule leur liste exacte, dans
        l'ordre croissant (jour, k) des fichiers, les déclare. Autre ordre, booléens pour des entiers (False == 0 et
        True == 1 en Python), champ de plus, liste vide ou null : rupture `LECTEUR/declaration` ; lien faux sous une
        déclaration exacte, ou une `ouverture` au lieu d'une reprise : `LECTEUR/lien`, `LECTEUR/queue-non-declaree`.
        Toute rupture rend les deux queues, et aucune n'est réputée déclarée."""
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        self.ajouter(FICHIER, b"{")
        self.ajouter(SEG1, b"x")
        q1, q2 = queue(FICHIER, len(intact), b"{", "LECTEUR/fin"), queue(SEG1, 0, b"x", "LECTEUR/fin")
        d1, d2 = declaree(q1), declaree(q2)
        for nom, tete, code in (
                ("exacte", self.reprise(seq, prec, [d1, d2]), None),
                ("ordre décroissant", self.reprise(seq, prec, [d2, d1]), "LECTEUR/declaration"),
                ("booléens", self.reprise(seq, prec, [d1, {**d2, "position": False, "octets": True}]),
                 "LECTEUR/declaration"),
                ("champ de plus", self.reprise(seq, prec, [d1, {**d2, "cause": "LECTEUR/fin"}]), "LECTEUR/declaration"),
                ("liste vide", self.reprise(seq, prec, []), "LECTEUR/declaration"),
                ("null", self.reprise(seq, prec, None), "LECTEUR/declaration"),
                ("lien faux", self.reprise(seq, "f" * 64, [d1, d2]), "LECTEUR/lien"),
                ("ouverture", ligne(seq, prec, type="ouverture", jour=JOUR, suivante=m(9)),
                 "LECTEUR/queue-non-declaree")):
            with self.subTest(nom):
                with open(os.path.join(self.d, SEG2), "wb") as f:
                    f.write(tete)
                lecteur, _flux = lire(self.d)
                self.assertEqual((lecteur.ruptures, lecteur.queues), ([], [q1, q2]) if code is None else (
                    self.rupture(code, SEG2, seq, prec, [q1, q2]), []))

    def test_liste_vide_sans_queue_en_attente(self):                   # C-3 (FORMAT §7.4) : null exigé
        """Reprise écrite à la suite du fichier repris, aucune queue en attente : `queue` null est exacte ; une liste
        vide est une déclaration fausse, rupture `LECTEUR/declaration` sans queue rendue."""
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        for liste, ruptures in ((None, []), ([], self.rupture("LECTEUR/declaration", FICHIER, seq, prec, []))):
            with self.subTest(liste=liste):
                with open(os.path.join(self.d, FICHIER), "wb") as f:
                    f.write(intact + self.reprise(seq, prec, liste))
                self.assertEqual(lire(self.d)[0].ruptures, ruptures)
