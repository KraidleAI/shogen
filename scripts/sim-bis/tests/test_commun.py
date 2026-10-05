"""Socle SB-0 (E-S-02, E-S-03, E-S-43 ; T-FRO-1 pour la variable) :
attendus écrits à la main, empreintes par `sha256sum` ; chaque test nomme les mutations qui le rougissent. La variable
scellée n'apparaît que dans un mapping fictif, jamais dans l'environnement d'un processus."""
import hashlib
import json
import os
import tempfile
import unittest

import commun

FICTIF = {commun.VARIABLE: ""}


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
        (hexadécimal majuscule admis), M-0-06 (prédicat non appelé)."""
        prm = commun.charger_parametres(environ={})
        commun.controler(prm, commun.SCHEMA)
        for f in (lambda p: p.update(extra="x"), lambda p: p["entrees"]["sommes"].update(extra="x"),
                  lambda p: p.pop("lot"), lambda p: p.update(lot=""), lambda p: p.update(lot=7),
                  lambda p: p["entrees"]["episodes"].update(sha256=p["entrees"]["episodes"]["sha256"].upper())):
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
