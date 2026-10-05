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

    def test_provenance_c_5(self):
        """C-5 de la G2 de la tranche 2 (E-S-03) : le rattachement porte l'empreinte actuelle du G0 (sha256sum à la tête
        784ebd2, ajout daté du 2026-10-05 01:45:03 UTC compris) et cite celle d'avant cet ajout comme telle ;
        sources.source cite cet ajout daté (points 2 et 3), et non plus l'adjudication provisoire du brief. Mutation
        M-C5-01 : ancienne empreinte remise."""
        prm = commun.charger_parametres(environ={})
        g0 = ("G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md (sha256 "
              "d9cffc0aec3634138f58ba33b9a9679484f2532460b3e5177c0c5ae194648034")
        self.assertTrue(prm["rattachement"].startswith(g0), prm["rattachement"][:100])
        self.assertIn("avant cet ajout : eeaceb6bb15fd1a98bd65ab80e4326609a612596f954991ad7455b5ab2c41c39",
                      prm["rattachement"])
        s = prm["sources"]["source"]
        self.assertEqual([x in s for x in ("ajout daté du G0 du 2026-10-05 01:45:03 UTC, point 3",
                                           "même ajout daté, point 2", "adjudication provisoire")], [True, True, False])

    def test_valeurs_avis_t3(self):
        """P-2 des corrections G2 de la tranche 3 (adjugé avant E0, comme C-7 de la tranche 2) : les valeurs Q-T3-2 à
        Q-T3-16 adoptées ou modifiées par l'avis sont écrites dans parametres.json, chacune avec sa source :
        observateurs.questions (Q-T3-2 à Q-T3-12, Q-T3-16) et regle.questions (Q-T3-13 à Q-T3-15), textes qui citent
        les lignes de l'AVIS-SIM-T3 et de la PROPOSITION. Forme tenue par le schéma : question manquante, en trop, dans
        l'autre section, texte vide ou sans ses deux citations : PARAMETRES/schema. Chaque numéro est marqué dans le
        module qui emploie la valeur. Mutations M-8G-01 (citation de l'avis non exigée), M-8G-02 (citation de la
        PROPOSITION non exigée), M-8G-03 (marque retirée d'un module)."""
        def marques(texte):
            out, i = set(), texte.find("Q-T3-")
            while i >= 0:
                j = i + 5
                while j < len(texte) and texte[j].isdigit():
                    j += 1
                out.add(texte[i:j])
                i = texte.find("Q-T3-", j)
            return out
        prm = commun.charger_parametres(environ={})
        o, r = prm["observateurs"].get("questions", {}), prm["regle"].get("questions", {})
        self.assertEqual((sorted(o, key=lambda k: int(k[5:])), sorted(r)),
                         ([f"Q-T3-{n}" for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16)], ["Q-T3-13", "Q-T3-14",
                                                                                              "Q-T3-15"]))
        cite = [k for k, v in {**o, **r}.items() if "AVIS-SIM-T3.md l." in v and "PROPOSITION l." in v]
        self.assertEqual(len(cite), 15)
        for f in (lambda p: p["observateurs"]["questions"].pop("Q-T3-7"),
                  lambda p: p["regle"]["questions"].update({"Q-T3-1": p["regle"]["questions"]["Q-T3-13"]}),
                  lambda p: p["observateurs"]["questions"].update({"Q-T3-13": p["regle"]["questions"]["Q-T3-13"]}),
                  lambda p: p["regle"]["questions"].update({"Q-T3-14": ""}),
                  lambda p: p["regle"]["questions"].update({"Q-T3-15": "AVIS-SIM-T3.md l.101-106 seule"}),
                  lambda p: p["observateurs"]["questions"].update({"Q-T3-16": "PROPOSITION l.161-164 seule"})):
            p = json.loads(json.dumps(prm))
            f(p)
            self.refus("PARAMETRES/schema", commun.controler, p, commun.SCHEMA)
        for module, numeros in (("observateurs.py", o), ("regle.py", r)):
            with open(os.path.join(commun.ICI, module), encoding="utf-8") as g:
                self.assertLessEqual(set(numeros), marques(g.read()), module)

    def test_valeurs_avis_t4(self):
        """Corrections G2 de la tranche 4 (forme P-2 de la tranche 3, adjugées avant E0) : les valeurs Q-T4-1 à Q-T4-13
        de l'avis (douze adoptées, Q-T4-8 modifiée) sont écrites dans parametres.json, chacune avec sa source :
        variante.questions (Q-T4-1 à Q-T4-4), e1.questions (Q-T4-5 à Q-T4-10, Q-T4-13), oracle_r1.questions
        (Q-T4-11, Q-T4-12), textes qui citent les lignes de l'AVIS-SIM-T4 et de la PROPOSITION ; la source de chacune
        de ces sections cite l'adjudication (brief des corrections et avis, par leurs empreintes) ; Q-T4-8 porte la
        forme adjugée du nom de cellule. Forme tenue par le schéma : question manquante, en trop, dans une autre
        section, texte vide ou sans ses deux citations : PARAMETRES/schema. Chaque numéro est marqué dans le module qui
        emploie la valeur. Mutations M-14F-01 (citation de l'avis non exigée), M-14F-02 (citation de la PROPOSITION non
        exigée), M-14F-03 (marque retirée d'un module), M-14F-04 (forme « / » remise dans Q-T4-8), M-14F-05
        (adjudication retirée d'une source)."""
        def marques(texte):
            out, i = set(), texte.find("Q-T4-")
            while i >= 0:
                j = i + 5
                while j < len(texte) and texte[j].isdigit():
                    j += 1
                out.add(texte[i:j])
                i = texte.find("Q-T4-", j)
            return out
        prm = commun.charger_parametres(environ={})
        sections = {"variante": (1, 2, 3, 4), "e1": (5, 6, 7, 8, 9, 10, 13), "oracle_r1": (11, 12)}
        q = {s: prm[s].get("questions", {}) for s in sections}
        self.assertEqual({s: sorted(v, key=lambda k: int(k[5:])) for s, v in q.items()},
                         {s: [f"Q-T4-{n}" for n in ns] for s, ns in sections.items()})
        self.assertEqual(len([1 for v in q.values() for x in v.values()
                              if "AVIS-SIM-T4.md l." in x and "PROPOSITION l." in x]), 13)
        self.assertIn("« E1-<num>_<den>-<κ>-<τ_D> »", q["e1"]["Q-T4-8"])
        adj = ("adjugées par l'orchestrateur le 2026-10-05, avant E0 (brief des corrections G2 de la tranche 4, sha256 "
               "5e4487bc17fafb1a881f760e7bce5c8f543072e2f6e84cacf52cdec9ab382eff", "AVIS-SIM-T4.md (sha256 "
               "6dfc13e71633c29acd6446812dc0abdd2f4255d91bb8296c5811b2d9eed7ad8c)")
        self.assertEqual([s for s in sections if not all(x in prm[s]["source"] for x in adj)], [])
        for f in (lambda p: p["variante"]["questions"].pop("Q-T4-3"),
                  lambda p: p["e1"]["questions"].update({"Q-T4-14": p["e1"]["questions"]["Q-T4-13"]}),
                  lambda p: p["variante"]["questions"].update({"Q-T4-11": p["oracle_r1"]["questions"]["Q-T4-11"]}),
                  lambda p: p["oracle_r1"]["questions"].update({"Q-T4-12": ""}),
                  lambda p: p["e1"]["questions"].update({"Q-T4-9": "AVIS-SIM-T4.md l.61-63 seule"}),
                  lambda p: p["e1"]["questions"].update({"Q-T4-6": "PROPOSITION l.197 seule"})):
            p = json.loads(json.dumps(prm))
            f(p)
            self.refus("PARAMETRES/schema", commun.controler, p, commun.SCHEMA)
        for module, s in (("variante.py", "variante"), ("calib_fiv.py", "e1"), ("oracle_r1.py", "oracle_r1")):
            with open(os.path.join(commun.ICI, module), encoding="utf-8") as g:
                self.assertLessEqual(set(q[s]), marques(g.read()), module)

    def test_schema_ferme(self):
        """Clé en trop (racine, section), clé manquante, texte vide, empreinte en majuscules, entier pour un texte :
        PARAMETRES/schema. Mutations M-0-03 (clés incluses au lieu d'égales), M-0-04 (texte vide admis), M-0-05
        (hexadécimal majuscule admis), M-0-06 (prédicat non appelé) ; SB-1 : booléen ou zéro pour un entier positif
        (M-1-16, M-1-17) ; SB-2 : liste vide, couple de trois éléments, élément refusé, texte pour une liste (M-2-21
        liste vide admise, M-2-22 longueur du couple non contrôlée, M-2-23 éléments non contrôlés) ; SB-5 : jour 7,
        facteur T_max d'un seul terme (M-5-15 : jour 7 admis)."""
        prm = commun.charger_parametres(environ={})
        commun.controler(prm, commun.SCHEMA)
        for f in (lambda p: p.update(extra="x"), lambda p: p["entrees"]["sommes"].update(extra="x"),
                  lambda p: p.pop("lot"), lambda p: p.update(lot=""), lambda p: p.update(lot=7),
                  lambda p: p["entrees"]["episodes"].update(sha256=p["entrees"]["episodes"]["sha256"].upper()),
                  lambda p: p["aleas"].update(graine=True), lambda p: p["aleas"].update(graine=0),
                  lambda p: p["calibration"].update(strates=[]), lambda p: p["calibration"]["unites"][0].append("x"),
                  lambda p: p["calibration"].update(ell=[1, 0]), lambda p: p["calibration"].update(types="panne"),
                  lambda p: p["calendrier"].update(jours_stress=[5, 7]), lambda p: p["calendrier"].update(t_max=[3])):
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

    def test_garde_chemin_par_defaut(self):
        """C-1 de la G2 (E-S-02, annexe D.4 a) : sans argument `environ`, la garde lit os.environ, remplacé le temps du
        cas par un mapping (mock.patch.object : ni putenv, ni sous-processus) ; vide, charger_parametres() et
        lire_entree(prm, "episodes") lisent ; fictif, ils rendent CAMPAGNE/variable. Mutation R-28 : chemin par défaut
        neutralisé."""
        with mock.patch.object(commun.os, "environ", {}):
            prm = commun.charger_parametres()
            self.assertEqual(len(commun.lire_entree(prm, "episodes")), 40337)
        with mock.patch.object(commun.os, "environ", FICTIF):
            self.refus("CAMPAGNE/variable", commun.charger_parametres)
            self.refus("CAMPAGNE/variable", commun.lire_entree, prm, "episodes")

    def test_schema_controle_au_chargement(self):
        """C-2 de la G2 (E-S-03) : JSON valide hors schéma ({"lot": "SIM-BIS"}) refusé par charger_parametres :
        PARAMETRES/schema. Mutation R-26 : schéma non contrôlé au chargement."""
        self.refus("PARAMETRES/schema", commun.charger_parametres, self.poser("p.json", b'{"lot": "SIM-BIS"}'),
                   environ={})

    def test_jsonl_en_majuscules(self):
        """C-5 de la G2 (R-07) : « .JSONL » refusé en entrée (ENTREE/jsonl) et en sortie (SORTIE/jsonl), rien
        d'écrit. Mutation R-07 : extension d'entrée comparée sans passage en minuscules."""
        self.refus("ENTREE/jsonl", commun.charger_parametres, self.poser("p.JSONL", b"{}"), environ={})
        self.refus("SORTIE/jsonl", commun.ecrire, os.path.join(self.r, "u.JSONL"), b"x")
        self.assertEqual(os.listdir(self.r), ["p.JSONL"])

    def test_epingle_de_64_caracteres(self):
        """C-5 de la G2 (R-08) : une épingle compte exactement 64 caractères hexadécimaux ; 65 (et 63) refusés au
        schéma : PARAMETRES/schema. Mutation R-08 : « len(v) >= 64 »."""
        prm = commun.charger_parametres(environ={})
        sha = prm["entrees"]["episodes"]["sha256"]
        for s in (sha + "0", sha[:-1]):
            prm["entrees"]["episodes"]["sha256"] = s
            self.refus("PARAMETRES/schema", commun.controler, prm, commun.SCHEMA)

    def test_cle_flottante(self):
        """O-2 de la G2 (E-S-43) : clé flottante d'un dict, même imbriqué, refusée (SORTIE/flottant) ; json.dumps
        l'écrirait en chaîne (« 0.5 »). Mutation : clés non parcourues par _sans_flottant."""
        for x in ({0.5: 1}, {"a": [{1.0: "b"}]}):
            self.refus("SORTIE/flottant", commun.json_canonique, x)
