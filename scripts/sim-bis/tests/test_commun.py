"""Socle SB-0 (E-S-02, E-S-03, E-S-05, E-S-06, E-S-43, E-S-48 ; T-FRO-1 pour la variable et les empreintes) :
attendus écrits à la main, empreintes par `sha256sum` ; chaque test nomme les mutations qui le rougissent. La variable
scellée n'apparaît que dans un mapping fictif, jamais dans l'environnement d'un processus."""
import decimal
import hashlib
import json
import os
import tempfile
import unittest
from unittest import mock

import commun

NL = chr(10)
FICTIF = {commun.VARIABLE: ""}
DONNEE = "0d59576e2b5da6b81d8dfd5d480c4afe1f67520bece762c24bca9f09da98da90"   # echo donnee | sha256sum
AUTRE = "ac948da2e7a22124eccd4494e6d57616ae3e84ab3f0d54cf2ef4f7aa034f2ddc"    # echo autre | sha256sum
SOMMES = "e5e3a15b454622a49f80bb7fcd586c1ec7bb52f0ba040b727cf8bd26edbd095c"   # echo "<DONNEE>  e.txt" | sha256sum


class TestSocle(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.r = d.name

    def poser(self, rel, octets):
        os.makedirs(os.path.dirname(os.path.join(self.r, rel)), exist_ok=True)
        with open(os.path.join(self.r, rel), "wb") as f:
            f.write(octets)
        return os.path.join(self.r, rel)

    def refus(self, code, f, *a, **k):
        with self.assertRaises(commun.Refus) as c:
            f(*a, **k)
        self.assertEqual(c.exception.code, code)

    def test_parametres_du_lot(self):
        """parametres.json du dépôt : schéma tenu ; épingles égales aux empreintes mesurées par sha256sum ; empreinte
        des octets lus inscrite sous le chemin relatif à la racine ; chaque section du schéma porte sa source
        (E-S-03). Mutations M-0-02 (épingle retouchée), M-0-26 (section sans source)."""
        lus = {}
        prm = commun.charger_parametres(lus=lus, environ={})
        self.assertEqual([k for k, s in commun.SCHEMA.items() if type(s) is dict and "source" not in s], [])
        self.assertEqual((prm["lot"], prm["schema"], list(lus)), ("SIM-BIS", "shogen.sim-bis.v1",
                                                                  ["scripts/sim-bis/parametres.json"]))
        self.assertEqual([prm["entrees"][k]["sha256"] for k in ("episodes", "sommes")],
                         ["c0371ca5de876d0f2cb038b732172c8b1db50340fa526400078cfbb83d27dbc6",
                          "f21f929329f11e9baf00057e3a7b250e5fb3a05a31fd5bcc64bb9860218f601f"])
        with open(commun.PARAMETRES, "rb") as f:
            self.assertEqual(lus["scripts/sim-bis/parametres.json"], hashlib.sha256(f.read()).hexdigest())

    def test_schema_ferme(self):
        """Clé en trop (racine, section), clé manquante, texte vide, empreinte en majuscules, entier pour un texte :
        PARAMETRES/schema. Mutations M-0-03 (clés incluses au lieu d'égales), M-0-04 (texte vide admis), M-0-05
        (hexadécimal majuscule admis), M-0-06 (prédicat non appelé) ; SB-1 : booléen ou zéro pour un entier positif
        (M-1-16, M-1-17) ; SB-2 : liste vide, couple de trois éléments, élément refusé, texte pour une liste (M-2-21
        liste vide admise, M-2-22 longueur du couple non contrôlée, M-2-23 éléments non contrôlés)."""
        prm = commun.charger_parametres(environ={})
        commun.controler(prm, commun.SCHEMA)
        for f in (lambda p: p.update(extra="x"), lambda p: p["entrees"]["sommes"].update(extra="x"),
                  lambda p: p.pop("lot"), lambda p: p.update(lot=""), lambda p: p.update(lot=7),
                  lambda p: p["entrees"]["episodes"].update(sha256=p["entrees"]["episodes"]["sha256"].upper()),
                  lambda p: p["aleas"].update(graine=True), lambda p: p["aleas"].update(graine=0),
                  lambda p: p["calibration"].update(strates=[]), lambda p: p["calibration"]["unites"][0].append("x"),
                  lambda p: p["calibration"].update(ell=[1, 0]), lambda p: p["calibration"].update(types="panne")):
            p = json.loads(json.dumps(prm))
            f(p)
            self.refus("PARAMETRES/schema", commun.controler, p, commun.SCHEMA)

    def test_json_strict(self):
        """Flottant, NaN, clé double, JSON tronqué, imbrication excessive, octets non UTF-8 : refus nommés. Mutations
        M-0-07 (flottant admis), M-0-08 (clé double admise), M-0-09 (RecursionError non capturée) ; chemin
        `.jsonl` : ENTREE/jsonl (M-0-27, refus retiré)."""
        for texte, code in (('{"a": 1.5}', "PARAMETRES/flottant"), ('{"a": NaN}', "PARAMETRES/flottant"),
                            ('{"a": 1, "a": 2}', "PARAMETRES/cle-double"), ('{"a": ', "PARAMETRES/json"),
                            ("[" * 100000, "PARAMETRES/json")):
            self.refus(code, commun.charger_parametres, self.poser("p.json", texte.encode("utf-8")), environ={})
        self.refus("PARAMETRES/json", commun.charger_parametres, self.poser("q.json", bytes([255])), environ={})
        self.refus("ENTREE/jsonl", commun.charger_parametres, self.poser("p.jsonl", b"{}"), environ={})

    def test_garde_campagne(self):
        """Variable posée, même vide (mapping fictif) : CAMPAGNE/variable ; absente : rien. Mutations M-0-10 (garde
        retirée de charger_parametres), M-0-11 (valeur vide admise)."""
        commun.garde_campagne({})
        self.refus("CAMPAGNE/variable", commun.garde_campagne, FICTIF)
        self.refus("CAMPAGNE/variable", commun.charger_parametres, environ=FICTIF)

    def test_entree_reelle(self):
        """EP lu sous ses deux épingles (40 337 octets, `wc -c`), fichiers lus inscrits ; variable posée :
        CAMPAGNE/variable. Mutation M-0-12 : garde retirée de lire_entree."""
        lus, prm = {}, commun.charger_parametres(environ={})
        self.assertEqual(len(commun.lire_entree(prm, "episodes", lus, {})), 40337)
        self.assertEqual(lus, {"docs/adr-0029/plan-s2bis/episodes.txt": prm["entrees"]["episodes"]["sha256"],
                               "docs/adr-0029/plan-s2bis/SHA256SUMS": prm["entrees"]["sommes"]["sha256"]})
        self.refus("CAMPAGNE/variable", commun.lire_entree, prm, "episodes", {}, FICTIF)

    def test_lire_entree_double_controle(self):
        """Fixture écrite ici. Refus : empreinte ≠ épingle (M-FRO-2), absente des sommes (M-0-13), sommes ≠ leur épingle
        (M-0-14), entrée hors du dossier des sommes, nom seul comparé (M-0-15), `.jsonl` (M-0-16)."""
        for rel, octets in (("d/e.txt", b"donnee"), ("x/e.txt", b"donnee"), ("d/g.txt", b"autre"), ("d/f.jsonl", b"")):
            self.poser(rel, octets + NL.encode())
        self.poser("d/SHA256SUMS", (DONNEE + "  e.txt" + NL).encode())
        e = {"sommes": ("d/SHA256SUMS", SOMMES), "e": ("d/e.txt", DONNEE), "x": ("x/e.txt", DONNEE),
             "g": ("d/g.txt", AUTRE), "j": ("d/f.jsonl", DONNEE)}
        prm = {"entrees": {k: {"chemin": c, "sha256": s} for k, (c, s) in e.items()}}
        lus = {}
        self.assertEqual(commun.lire_entree(prm, "e", lus, {}, self.r), b"donnee" + NL.encode())
        self.assertEqual(lus, {"d/SHA256SUMS": SOMMES, "d/e.txt": DONNEE})
        self.refus("ENTREE/sha256-sommes", commun.lire_entree, prm, "g", {}, {}, self.r)
        self.refus("ENTREE/sha256-sommes", commun.lire_entree, prm, "x", {}, {}, self.r)
        self.refus("ENTREE/jsonl", commun.lire_entree, prm, "j", {}, {}, self.r)
        prm["entrees"]["e"]["sha256"] = AUTRE
        self.refus("ENTREE/sha256-parametres", commun.lire_entree, prm, "e", {}, {}, self.r)
        prm["entrees"]["e"]["sha256"], prm["entrees"]["sommes"]["sha256"] = DONNEE, AUTRE
        self.refus("ENTREE/sha256-parametres", commun.lire_entree, prm, "e", {}, {}, self.r)

    def test_ecrire_atomique_sans_ecrasement(self):
        """En entier, sans partiel restant ; cible existante : SORTIE/existe, contenu intact ; partiel présent :
        SORTIE/partiel-present ; `.jsonl` : SORTIE/jsonl. Mutations M-0-17 (os.replace), M-0-18 (partiel laissé),
        M-0-19 (partiel sous un autre suffixe), M-0-43 (fsync retiré ; espion : un appel, avant le lien)."""
        c, fsync = os.path.join(self.r, "s.json"), []
        with mock.patch.object(os, "fsync", side_effect=lambda fd: fsync.append(os.path.exists(c))):
            commun.ecrire(c, b"un")
        self.assertEqual(fsync, [False])
        self.refus("SORTIE/existe", commun.ecrire, c, b"deux")
        with open(c, "rb") as f:
            self.assertEqual((f.read(), sorted(os.listdir(self.r))), (b"un", ["s.json"]))
        self.poser("t.json.partiel", b"")
        self.refus("SORTIE/partiel-present", commun.ecrire, os.path.join(self.r, "t.json"), b"x")
        self.refus("SORTIE/jsonl", commun.ecrire, os.path.join(self.r, "u.jsonl"), b"x")
        self.assertEqual(sorted(os.listdir(self.r)), ["s.json", "t.json.partiel"])

    def test_json_canonique(self):
        """Clés triées, séparateurs fixes, UTF-8 sans échappement, saut de ligne final ; flottant, même imbriqué :
        SORTIE/flottant ; Decimal : SORTIE/type. Mutations M-0-20 (clés non triées), M-0-21 (flottant admis)."""
        self.assertEqual(commun.json_canonique({"b": 1, "a": ["é", None, True, (2,)]}),
                         '{"a":["é",null,true,[2]],"b":1}'.encode("utf-8") + NL.encode())
        for x in (1.0, [{"a": 0.5}], {"a": (1, 2.5)}):
            self.refus("SORTIE/flottant", commun.json_canonique, x)
        self.refus("SORTIE/type", commun.json_canonique, {"a": decimal.Decimal(1)})

    def test_etiquette_e_s_05(self):
        """Recopiée de PROPOSITION l.139. Mutation M-0-01 : étiquette retouchée."""
        self.assertEqual(commun.ETIQUETTE, "synthétique ; préparation de S2-bis ; ne lit aucune donnée de S2-bis ni "
                                           "aucun journal de S2 ; ne change ni R, ni le seuil, ni la règle")

    def test_entete(self):
        """Étiquette, puis « sha256 <chemin> <empreinte> » triés : modules du lot chargés (commun.py, empreinte
        recalculée) et fichiers lus. Mutations M-0-22 (lus omis), M-0-23 (modules hors du lot inclus)."""
        t = commun.entete({"docs/x.txt": "ab"})
        with open(commun.__file__, "rb") as f:
            moi = "sha256 scripts/sim-bis/commun.py " + hashlib.sha256(f.read()).hexdigest()
        self.assertEqual((t[0], t[1:] == sorted(t[1:])), (commun.ETIQUETTE, True))
        self.assertTrue({moi, "sha256 docs/x.txt ab"} <= set(t))
        self.assertEqual([x for x in t[1:] if not x.startswith("sha256 scripts/sim-bis/")], ["sha256 docs/x.txt ab"])
