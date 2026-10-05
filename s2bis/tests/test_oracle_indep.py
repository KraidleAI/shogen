"""RB-18, lecteur indépendant (E-R-33 ; PROPOSITION du G0 de RECALC-BIS l.396, l.486, l.539-540, l.551) : attendus
construits depuis le FORMAT (docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md), jamais depuis un autre lecteur. Lignes,
valeurs et noms écrits à la main ici ; barre oblique inverse et saut de ligne jamais tapés (chr(92), octet 10)."""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

from shogen_s2bis.collecte import journal as j
from shogen_s2bis.recalc import oracle_indep as o
from tests.test_fitness import violations

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS, NL, PREC = chr(92), bytes((10,)), "ab" * 32
T0 = 1791158280                     # 2026-10-04 23:58:00 UTC (date -u -d @1791158280) ; T0 + 120 : 00:00 du 5
J1, J1S1 = "pool-2026-10-04-0.jsonl", "pool-2026-10-04-1.jsonl"
J2, J3 = "pool-2026-10-05-0.jsonl", "pool-2026-10-06-0.jsonl"


def ligne(texte):
    return texte.encode("utf-8") + NL


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Ligne(unittest.TestCase):
    def test_canonique_admise(self):                                        # FORMAT §1.1, §1.2
        t = '{"a":[1,-2,{"b":null}],"n":"é' + chr(0x2028) + '","z":true}'
        self.assertEqual(o.objet(ligne(t)), {"a": [1, -2, {"b": None}], "n": "é" + chr(0x2028), "z": True})

    def test_echappements_de_json(self):                                    # Q-R18-3
        admis = '{"s":"' + BS + '"' + BS + BS + BS + "n" + BS + 'u001f"}'
        self.assertEqual(o.objet(ligne(admis)), {"s": '"' + BS + chr(10) + chr(31)})
        for autre in ("u000a", "u00e9", "/", "u001F"):
            self.assertIsNone(o.objet(ligne('{"s":"' + BS + autre + '"}')), autre)

    def test_non_canonique(self):                                           # §1.2 : réécrire redonne les octets
        for t in ('{"a": 1}', '{"b":1,"a":2}', ' {"a":1}', '{"a":1} ', '{"a":1}' + chr(13), '{"a":1,"a":1}',
                  '{"a":-0}', '{"a":01}', '{"a":1.5}', '{"a":1e3}', '{"a":NaN}', '{"a":-Infinity}', "[1]", '"a"',
                  "1", "", "{}{}"):
            self.assertIsNone(o.objet(ligne(t)), t)
        self.assertIsNone(o.objet(b'{"a":1}'))                              # sans 0x0A final

    def test_octets_hors_utf8(self):                                        # §1.1 : UTF-8
        for brut in (b'{"a":"' + bytes((0xC3,)) + b'"}', b'{"a":"' + bytes((0xED, 0xA0, 0x80)) + b'"}',
                     ('{"a":"' + BS + 'ud800"}').encode(), bytes((0xEF, 0xBB, 0xBF)) + b'{"a":1}'):
            self.assertIsNone(o.objet(brut + NL), brut)

    def test_imbrication_comptee_par_le_lecteur(self):                      # §8.3, §7.1 b (lettre C-4) : N = 64
        def listes(n):                                                      # n niveaux : l'objet, n - 1 listes
            return '{"a":' + "[" * (n - 1) + "]" * (n - 1) + "}"

        def alternes(n):                                                    # n niveaux : listes et objets alternés
            t = "7"
            for k in range(n - 1):
                t = "[" + t + "]" if k % 2 else '{"b":' + t + "}"
            return '{"a":' + t + "}"
        v = []
        for _k in range(62):
            v = [v]
        self.assertEqual(o.objet(ligne(listes(64))), {"a": v})              # la racine au niveau 1
        self.assertIsNotNone(o.objet(ligne(alternes(64))))
        for t in (listes(65), alternes(65), listes(100000)):                # lisible par json, ou RecursionError
            self.assertIsNone(o.objet(ligne(t)), len(t))
        dans = '{"a":"' + "[" * 70 + '","b":"' + BS + '"' + "{" * 70 + '","c":"' + BS * 2 + '","d":"' + "[" * 70 + '"}'
        self.assertEqual(o.objet(ligne(dans)), {"a": "[" * 70, "b": '"' + "{" * 70, "c": BS, "d": "[" * 70})

    def test_entiers_longs(self):                                           # §1.2, §7.1 b (lettre C-1)
        t = '{"a":' + "9" * 640 + ',"b":-1' + "0" * 639 + "}"
        self.assertEqual(o.objet(ligne(t)), {"a": 10 ** 640 - 1, "b": -(10 ** 639)})
        for t in ('{"a":' + "1" * 641 + "}", '{"a":-' + "1" * 641 + "}", '{"a":[' + "2" * 700 + "]}",
                  '{"a":' + "3" * 5000 + "}", '{"a":' + "1" * 641 + ',"b":1.5}', '{"a":' + "1" * 641 + ",}"):
            self.assertIsNone(o.objet(ligne(t)), t[-9:])                    # non intègre, jamais un refus

    def test_independant_du_reglage_de_l_interpreteur(self):                # PYTHONINTMAXSTRDIGITS, -X int_max…
        self.addCleanup(sys.set_int_max_str_digits, sys.get_int_max_str_digits())
        for reglage in (640, 0, 4300):
            sys.set_int_max_str_digits(reglage)
            self.assertEqual(o.objet(ligne('{"a":-' + "7" * 640 + "}")), {"a": -int("7" * 640)})
            self.assertIsNone(o.objet(ligne('{"a":' + "7" * 641 + "}")), reglage)


class Champs(unittest.TestCase):
    def test_champs_communs(self):                                          # FORMAT §1.3
        bon = {"type": "x", "seq": 3, "prec": PREC, "ws": 60}
        self.assertTrue(o.champs(bon))
        for k, v in (("type", 1), ("seq", True), ("seq", "3"), ("seq", None), ("prec", "AB" * 32),
                     ("prec", "ab" * 31), ("prec", PREC + "a"), ("prec", 0)):
            self.assertFalse(o.champs({**bon, k: v}), (k, v))
        for k in ("type", "seq", "prec"):
            self.assertFalse(o.champs({x: v for x, v in bon.items() if x != k}), k)


class Noms(unittest.TestCase):
    def test_grammaire_et_ordre(self):                                      # FORMAT §6.1, §7.2 ; Q-R18-5
        with tempfile.TemporaryDirectory() as d:
            for n in ("pool-2026-10-05-10.jsonl", "pool-2026-10-05-2.jsonl", "pool-2026-10-04-0.jsonl",
                      "pool-2026-10-05-0.jsonl", "pool-2026-10-05-01.jsonl", "pool.sha256", "pool.verrou",
                      "autre-2026-10-04-0.jsonl", "pool-2026-10-04-0.jsonl.bak", "pool-2026-1-04-0.jsonl",
                      "xpool-2026-10-04-0.jsonl", "pool-2026-10-04-0.json", "p.l-2026-10-04-0.jsonl",
                      "pxl-2026-10-04-0.jsonl"):
                open(os.path.join(d, n), "wb").close()
            self.assertEqual(o.fichiers(d, "pool"), ["pool-2026-10-04-0.jsonl", "pool-2026-10-05-0.jsonl",
                                                       "pool-2026-10-05-2.jsonl", "pool-2026-10-05-10.jsonl"])
            self.assertEqual(o.fichiers(d, "p.l"), ["p.l-2026-10-04-0.jsonl"])


class Frontiere(unittest.TestCase):
    def test_ni_lecteur_principal_ni_ecrivain(self):                        # l.539-540 : bibliothèque standard seule
        with open(o.__file__, "rb") as f:
            self.assertEqual(violations("shogen_s2bis", f.read()), [])
        code = "import sys, shogen_s2bis.recalc.oracle_indep; print(sorted(m for m in sys.modules if 'shogen' in m))"
        p = subprocess.run([sys.executable, "-B", "-c", code], cwd=RACINE, capture_output=True, timeout=60)
        self.assertEqual(p.stdout, b"['shogen_s2bis', 'shogen_s2bis.recalc', 'shogen_s2bis.recalc.oracle_indep']" + NL)


class Journaux(unittest.TestCase):
    """Journaux de l'écrivain réel (CB-1, CB-2), puis altérés à la main. Attendus : lignes complètes découpées sur
    l'octet 10 (§1.1) ; queues prises sur les octets (§7.1, §7.4) ; types et rangs lus dans le FORMAT (§2, §6, §7)."""
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.d = t.name

    def ecrivain(self, ws, fenetres=(), dernier=None):
        """Ouvert à `ws` : lecture et marqueur par fenêtre de `fenetres`, puis lecture « é » de `dernier` ; fermé."""
        jl = j.Journal(self.d, "pool", fsync=lambda fd: None).ouvrir(ws)
        try:
            for x in fenetres:
                jl.ecrire("lecture", x, v=x % 7)
                jl.marqueur(x)
            if dernier:
                jl.ecrire("lecture", dernier, note="é")
        finally:
            jl.fermer()

    def octets(self, nom):
        with open(os.path.join(self.d, nom), "rb") as f:
            return f.read()

    def couper(self, nom, n):
        """Arrêt brutal : retire les `n` derniers octets, pris dans la dernière ligne ; rend la queue attendue."""
        b = self.octets(nom)
        debut, fin = b.rfind(NL, 0, len(b) - 1) + 1, len(b) - n
        with open(os.path.join(self.d, nom), "r+b") as f:
            f.truncate(fin)
        return {"fichier": nom, "position": debut, "octets": fin - debut, "sha256": sha(b[debut:fin])}

    def types(self, r):
        return [x["enr"]["type"] for x in r["enregistrements"]]

    def lignes(self, nom):
        """(fichier, position, sha256) de chaque ligne complète de `nom`."""
        r, pos = [], 0
        for x in self.octets(nom).split(NL)[:-1]:
            r.append((nom, pos, sha(x + NL)))
            pos += len(x) + 1
        return r

    def lire(self):
        r = o.lire(self.d, "pool")
        return r, [(x["fichier"], x["position"], x["sha256"]) for x in r["enregistrements"]]

    def test_journal_intact_sur_deux_jours(self):                         # §1.3, §1.4, §6.2
        self.ecrivain(T0, range(T0 + 60, T0 + 240, 60))                    # 23:59 (point), 00:00 et 00:01 du 5
        r, flux = self.lire()
        attendu = self.lignes(J1) + self.lignes(J2)
        self.assertEqual((flux, [x["enr"]["seq"] for x in r["enregistrements"]]), (attendu, list(range(10))))
        self.assertEqual([x["enr"]["type"] for x in r["enregistrements"]][3:6], ["point", "cloture", "ouverture"])
        self.assertEqual((r["fichiers"], r["ruptures"], r["queues_declarees"], r["queue_finale"], r["tete"]),
                         ([J1, J2], [], [], [], {"seq": 9, "sha256": attendu[-1][2]}))

    def test_queue_tronquee_en_fin_du_dernier_fichier(self):              # E-R-01 ; §4
        self.ecrivain(T0, range(T0 + 60, T0 + 240, 60))
        taille = len(self.octets(J2))
        with open(os.path.join(self.d, J2), "ab") as f:
            f.write(b'{"prec":"')                                          # ligne coupée par un arrêt brutal
        r, flux = self.lire()
        q = {"fichier": J2, "position": taille, "octets": 9, "sha256": sha(b'{"prec":"')}
        self.assertEqual((flux, r["ruptures"], r["queues_declarees"]), (self.lignes(J1) + self.lignes(J2), [], []))
        self.assertEqual((r["queue_finale"], r["tete"]["seq"]), ([q], 9))

    def test_rupture_sans_reprise(self):                                  # §7.1, §7.7 : chaîne rompue, aucune reprise
        self.ecrivain(T0, range(T0 + 60, T0 + 240, 60))
        b, j2 = self.octets(J1), self.lignes(J2)
        p2, p3 = self.lignes(J1)[2][1], self.lignes(J1)[3][1]               # le marqueur de 23:59, rang 2
        for avant, apres, k in ((b'"seq":2,', b'"seq":7,', 2), (b'"type":"marqueur",', b'', 2),
                                (b'"ws":1791158340', b'"ws":1791158400', 3)):
            with open(os.path.join(self.d, J1), "wb") as f:                 # seq faux ; prec du suivant faux
                f.write(b[:p2] + b[p2:p3].replace(avant, apres) + b[p3:])
            r, flux = self.lire()
            j1 = self.lignes(J1)
            reste = self.octets(J1)[j1[k][1]:]
            q = {"fichier": J1, "position": j1[k][1], "octets": len(reste), "sha256": sha(reste)}
            self.assertEqual((flux, r["queue_finale"], r["tete"]["seq"]), (j1[:k] + j2, [], 9), k)
            self.assertEqual(r["ruptures"], [{"fichier": J2, "position": 0, "seq": 5, "queues": [q],
                                              "causes": ["lien", "queue-non-declaree"]}], k)

    def test_lien_rompu_par_le_seul_prec(self):                           # §7.7 : seq juste, prec faux entre fichiers
        self.ecrivain(T0, range(T0 + 60, T0 + 240, 60))
        b, p4 = self.octets(J1), self.lignes(J1)[4][1]                      # la clôture du 4, rang 4
        with open(os.path.join(self.d, J1), "wb") as f:
            f.write(b[:p4] + b[p4:].replace(b"2026-10-04", b"2026-10-03"))
        r, flux = self.lire()
        rupture = {"fichier": J2, "position": 0, "seq": 5, "causes": ["lien"], "queues": []}
        self.assertEqual((flux, r["ruptures"]), (self.lignes(J1) + self.lignes(J2), [rupture]))

    def test_fichiers_manquants(self):                                    # §1.3 : genèse ; §7.7 : lien entre fichiers
        self.ecrivain(T0, (T0 + 60, T0 + 120, T0 + 86520))                 # 4, 5 et 6 octobre
        j1, j3 = self.lignes(J1), self.lignes(J3)
        self.assertEqual((len(j1), len(self.lignes(J2)), len(j3)), (5, 4, 4))   # §2, §6.2, §8 : rangs 0 à 12
        os.remove(os.path.join(self.d, J2))
        r, flux = self.lire()
        self.assertEqual((r["fichiers"], flux, r["tete"]["seq"]), ([J1, J3], j1 + j3, 12))
        rupture = {"fichier": J3, "position": 0, "seq": 9, "causes": ["lien"], "queues": []}
        self.assertEqual(r["ruptures"], [rupture])

    def test_genese_et_premiere_ligne(self):                              # §1.3, §2, §7.1 : lignes écrites ici
        z = "0" * 64
        for t, seq, prec, attendu in (("ouverture", 0, z, (1, [], 0)), ("reprise", 0, z, (1, [["genese"]], 0)),
                                      ("ouverture", 0, "1" * 64, (1, [["genese"]], 0)),
                                      ("ouverture", 1, z, (1, [["genese"]], 0)), ("lecture", 0, z, (0, [], 1))):
            with open(os.path.join(self.d, J1), "wb") as f:
                f.write(ligne('{"prec":"' + prec + '","seq":' + str(seq) + ',"type":"' + t + '"}'))
            r, flux = self.lire()
            self.assertEqual((len(flux), [x["causes"] for x in r["ruptures"]], len(r["queue_finale"])), attendu, t)

    def test_dossier_vide_ou_absent(self):
        r, flux = self.lire()
        self.assertEqual((flux, r["fichiers"], r["tete"], r["ruptures"], r["queue_finale"]), ([], [], None, [], []))
        with self.assertRaises(o.RefusOracle) as e:
            o.lire(os.path.join(self.d, "absent"), "pool")
        self.assertEqual(e.exception.code, "ORACLE/lecture")

    def test_ligne_coupee_dans_un_caractere(self):                        # SHOGEN-TORN-LINE-UTF8-1 ; §1.1
        self.ecrivain(T0, (), dernier=T0 + 60)
        b = self.octets(J1)
        q = self.couper(J1, len(b) - b.index("é".encode()) - 1)            # entre les deux octets de « é »
        r, flux = self.lire()
        self.assertEqual(self.octets(J1)[-1:], "é".encode()[:1])
        self.assertEqual((flux, r["queue_finale"], r["tete"]["seq"]), (self.lignes(J1), [q], 0))

    def test_reprise_declare_la_queue(self):                              # §7.2, §7.4 : segment neuf
        self.ecrivain(T0 - 600, (T0 - 540, T0 - 480), dernier=T0 - 420)
        q = self.couper(J1, 5)
        self.ecrivain(T0 - 300, (T0 - 240,))
        r, flux = self.lire()
        self.assertEqual((flux, r["fichiers"]), (self.lignes(J1) + self.lignes(J1S1), [J1, J1S1]))
        self.assertEqual((r["queues_declarees"], r["ruptures"], r["queue_finale"]), ([q], [], []))
        self.assertEqual(self.types(r)[5:], ["reprise", "lecture", "trou", "marqueur"])

    def test_reprise_sans_queue_a_la_suite(self):                         # §7.3
        self.ecrivain(T0 - 600, (T0 - 540,))
        self.ecrivain(T0 - 420, (T0 - 360,))
        r, flux = self.lire()
        self.assertEqual((flux, r["ruptures"], r["queues_declarees"], r["queue_finale"]), (self.lignes(J1), [], [], []))
        self.assertEqual(self.types(r), ["ouverture", "lecture", "marqueur", "reprise", "lecture", "trou", "marqueur"])

    def test_reprise_un_autre_jour(self):                                 # §7.3 : clôture tardive, puis reprise
        self.ecrivain(T0 - 600, (T0 - 540,))
        self.ecrivain(T0 + 300, (T0 + 360,))
        r, flux = self.lire()
        self.assertEqual((r["fichiers"], flux, self.types(r)[3:5]), ([J1, J2], self.lignes(J1) + self.lignes(J2),
                                                                      ["cloture", "reprise"]))
        self.assertEqual((r["ruptures"], r["queues_declarees"], r["queue_finale"]), ([], [], []))

    def test_segments_de_jour(self):                                      # §6.1, §7.2 : segment 1, puis bascule
        self.ecrivain(T0 - 600, (T0 - 540,), dernier=T0 - 480)
        q = self.couper(J1, 3)
        self.ecrivain(T0 - 300, range(T0 - 240, T0 + 180, 60))
        self.ecrivain(T0 + 300, (T0 + 360,))
        r, flux = self.lire()
        self.assertEqual((r["fichiers"], flux), ([J1, J1S1, J2], self.lignes(J1) + self.lignes(J1S1) + self.lignes(J2)))
        self.assertEqual((r["queues_declarees"], r["ruptures"], r["queue_finale"]), ([q], [], []))

    def test_declaration_fausse(self):                                    # §7.4 : queue changée après la reprise
        self.ecrivain(T0 - 600, (T0 - 540,), dernier=T0 - 480)
        q = self.couper(J1, 3)
        self.ecrivain(T0 - 300, (T0 - 240,))
        b = self.octets(J1)
        with open(os.path.join(self.d, J1), "wb") as f:
            f.write(b[:-1] + b"x")
        r, flux = self.lire()
        q = {**q, "sha256": sha(b[q["position"]:-1] + b"x")}
        rupture = {"fichier": J1S1, "position": 0, "seq": 3, "causes": ["declaration", "queue-non-declaree"],
                   "queues": [q]}
        self.assertEqual((r["queues_declarees"], len(flux), r["ruptures"]), ([], 7, [rupture]))

    def test_declaration_stricte(self):                                   # §7.4 : `true` n'est pas l'entier 1
        self.ecrivain(T0 - 600, (T0 - 540,))
        with open(os.path.join(self.d, J1), "ab") as f:
            f.write(b"{")                                                   # queue d'un octet
        p = len(self.octets(J1)) - 1
        q = '{"fichier":"' + J1 + '","octets":%s,"position":' + str(p) + ',"sha256":"' + sha(b"{") + '"}'
        for octets, causes in (("1", []), ("true", [["declaration", "queue-non-declaree"]])):
            with open(os.path.join(self.d, J1S1), "wb") as f:              # reprise écrite à la main, chaînée
                f.write(ligne('{"prec":"' + self.lignes(J1)[-1][2] + '","queue":[' + q % octets + '],"seq":3,'
                              '"suivante":1791157800,"type":"reprise","ws":1791157800}'))
            r, flux = self.lire()
            self.assertEqual(([x["causes"] for x in r["ruptures"]], len(flux), len(r["queues_declarees"])),
                             (causes, 4, 1 - len(causes)), octets)

    def test_douze_segments_d_un_jour(self):                              # §6.1, §7.2 : k comparé en entier
        noms = [f"pool-2026-10-04-{k}.jsonl" for k in range(12)]
        for k, nom in enumerate(noms):
            a = T0 - 6000 + 240 * k
            self.ecrivain(a, (a + 60,), dernier=a + 120)
            q = self.couper(nom, 2)
        r, flux = self.lire()
        self.assertEqual((r["fichiers"], r["ruptures"], len(r["queues_declarees"]), r["queue_finale"]),
                         (noms, [], 11, [q]))
        self.assertEqual(flux, [x for n in noms for x in self.lignes(n)])

    def test_fichier_renomme(self):                                       # §7.2 : ordre des noms, ordre de la chaîne
        self.ecrivain(T0, (T0 + 60, T0 + 120, T0 + 86520))
        j1, j2, j3, j7 = self.lignes(J1), self.lignes(J2), self.lignes(J3), "pool-2026-10-07-0.jsonl"
        os.rename(os.path.join(self.d, J2), os.path.join(self.d, j7))
        r, flux = self.lire()
        self.assertEqual((r["fichiers"], flux), ([J1, J3, j7], j1 + j3 + [(j7, p, h) for _n, p, h in j2]))
        self.assertEqual(r["ruptures"], [{"fichier": J3, "position": 0, "seq": 9, "causes": ["lien"], "queues": []},
                                         {"fichier": j7, "position": 0, "seq": 5, "causes": ["lien"], "queues": []}])

    def test_reprise_au_milieu_ne_declare_rien(self):                     # §7.3 : à la suite, `queue` null
        self.ecrivain(T0 - 600, (T0 - 540,))
        q = '[{"fichier":"' + J1 + '","octets":1,"position":0,"sha256":"' + sha(b"{") + '"}]'
        with open(os.path.join(self.d, J1), "ab") as f:                     # reprise écrite à la main, chaînée
            f.write(ligne('{"prec":"' + self.lignes(J1)[-1][2] + '","queue":' + q + ',"seq":3,"suivante":1791157800,'
                          '"type":"reprise","ws":1791157800}'))
        r, flux = self.lire()
        self.assertEqual((len(flux), r["ruptures"]), (4, [{"fichier": J1, "position": self.lignes(J1)[3][1], "seq": 3,
                                                            "causes": ["declaration"], "queues": []}]))

    def test_limite_d_une_ligne(self):                                    # §7.1 : 4 194 304 octets, 0x0A compris
        l0 = ligne(LigneDeCommande.L0)

        def longue(seq, prec, n):                                          # ligne `lecture` de n octets exactement
            fin = '","prec":"' + prec + '","seq":' + str(seq) + ',"type":"lecture","ws":' + str(T0) + "}"
            return ligne('{"pad":"' + "x" * (n - len(fin) - 9) + fin)
        l1 = longue(1, sha(l0), 4194304)
        l2 = longue(2, sha(l1), 4194305)
        with open(os.path.join(self.d, J1), "wb") as f:
            f.write(l0 + l1 + l2)
        r, flux = self.lire()
        q = {"fichier": J1, "position": len(l0 + l1), "octets": len(l2), "sha256": sha(l2)}
        self.assertEqual((len(l1), len(l2), [x[2] for x in flux], r["queue_finale"]),
                         (4194304, 4194305, [sha(l0), sha(l1)], [q]))

    def test_entier_long_ou_imbrication_dans_un_journal(self):            # §1.2, §8.3 : la ligne ouvre la queue
        jl = j.Journal(self.d, "pool", fsync=lambda fd: None).ouvrir(T0 - 600)
        self.addCleanup(jl.fermer)
        jl.ecrire("lecture", T0 - 540, grand=int("9" * 640), petit=-int("9" * 640))
        jl.marqueur(T0 - 540)
        enr = self.lire()[0]["enregistrements"][1]["enr"]
        self.assertEqual((enr["grand"], enr["petit"]), (10 ** 640 - 1, 1 - 10 ** 640))
        j1, b = self.lignes(J1), self.octets(J1)
        for valeur in ("9" * 641, "[" * 64 + "]" * 64, "[" * 100000 + "]" * 100000):   # l'écrivain les refuse :
            l3 = ligne('{"prec":"' + j1[-1][2] + '","seq":3,"trop":' + valeur      # lignes écrites à la main
                       + ',"type":"lecture","ws":' + str(T0 - 480) + "}")
            with open(os.path.join(self.d, J1), "wb") as f:
                f.write(b + l3)
            r, flux = self.lire()
            q = {"fichier": J1, "position": len(b), "octets": len(l3), "sha256": sha(l3)}
            self.assertEqual((flux, r["queue_finale"], r["ruptures"]), (j1, [q], []), len(valeur))

    def test_premier_fichier_manquant(self):                              # §1.3 : la genèse manque
        self.ecrivain(T0, range(T0 + 60, T0 + 240, 60))
        os.remove(os.path.join(self.d, J1))
        r, flux = self.lire()
        self.assertEqual((flux, r["ruptures"]), (self.lignes(J2), [{"fichier": J2, "position": 0, "seq": 5,
                                                                   "causes": ["genese"], "queues": []}]))

    def test_queue_finale_sur_deux_fichiers(self):                        # Q-R18-8 : la reprise déchirée à son tour
        self.ecrivain(T0 - 600, (T0 - 540,), dernier=T0 - 480)
        q1 = self.couper(J1, 3)
        self.ecrivain(T0 - 300)
        q2 = self.couper(J1S1, len(self.octets(J1S1)) - 10)
        r, flux = self.lire()
        self.assertEqual((flux, r["queue_finale"], r["queues_declarees"], r["ruptures"]),
                         (self.lignes(J1), [q1, q2], [], []))


class LigneDeCommande(unittest.TestCase):                                  # forme canonique documentée : JSON trié
    H = "e256795529f7f3d0de68dee480a8f269e4e4cff9325a75d7d20ae02e90487409"   # printf '%s' L0 0x0A | sha256sum (G1)
    L0 = '{"jour":"2026-10-04","prec":"' + "0" * 64 + '","seq":0,"suivante":1791158340,"type":"ouverture"}'

    def lancer(self, *args):
        p = subprocess.run([sys.executable, "-B", "-m", "shogen_s2bis.recalc.oracle_indep", *args], cwd=RACINE,
                           capture_output=True, timeout=60)
        return p.returncode, p.stdout

    def test_sortie_doree_refus_et_usage(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, J1), "wb") as f:
                f.write(ligne(self.L0))
            attendu = ('{"enregistrements":[{"enr":' + self.L0 + ',"fichier":"' + J1 + '","position":0,"sha256":"'
                       + self.H + '"}],"fichiers":["' + J1 + '"],"format":"shogen.s2bis.oracle-indep.v1",'
                       '"queue_finale":[],"queues_declarees":[],"ruptures":[],"tete":{"seq":0,"sha256":"'
                       + self.H + '"}}')
            self.assertEqual(self.lancer(d, "pool"), (0, ligne(attendu)))
            refus = '{"fichier":null,"format":"shogen.s2bis.oracle-indep.v1","position":null,"refus":"ORACLE/lecture"}'
            self.assertEqual(self.lancer(os.path.join(d, "absent"), "pool"), (1, ligne(refus)))
        self.assertEqual(self.lancer(), (2, b""))
