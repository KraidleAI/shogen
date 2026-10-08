"""Socle du lot PLAN-S2BIS-2 : variable, schéma, épingles, sous-arbres, écarts (d), pool (c). Attendus écrits à la main
ou par sha256sum ; chaque test nomme la mutation qui le rougit."""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

import socle
import tests

NL = chr(10)
EPINGLES = {    # sha256sum des huit pièces à 12ce67f, recopiés à la main (PERIMETRE-REDUIT.md §1)
    "commun": "14920e8703febf43de324960975413e276227ac2281bb4f85380cf465d47b3f2",
    "regles": "a01401880714e2baa792d1e7a2c36414df2b848c055c73429e22b4646d2f88a6",
    "episodes": "90c7842d9e1193b0629de41cfd91fbbebb45d4ec4731af89b77e70a96af43fd2",
    "parametres": "7e214864e23634e9b3a4174745e3f5bbabf8c5a74d8e78e0411b449ee7d1d632",
    "fixtures": "17ae3c130a1e4a1fcde2b3fc8d8a4384a77f513533836f0ec6fad657b4903913",
    "sha256sums": "65c26310c98db6e4ddd7293d06601fffd3599dde3892fc606806c59aa9c94398",
    "ep": "c0371ca5de876d0f2cb038b732172c8b1db50340fa526400078cfbb83d27dbc6",
    "ep_sha256sums": "f21f929329f11e9baf00057e3a7b250e5fb3a05a31fd5bcc64bb9860218f601f"}


def prm_avec(**chemins):
    """parametres.json du lot, chemins de pièces remplacés (copie profonde)."""
    p = json.loads(json.dumps(tests.PRM))
    p["plan_s2bis"]["chemins"].update(chemins)
    return p


def analyse(d, ps2, prm, ep):
    return {"a.txt": ["ANALYSE"]}


def processus_neuf(prm):
    """socle.charger(prm) dans un processus neuf : [code du refus ou « - », [[nom, fichier] des modules chargés]]."""
    code = NL.join(["import json, sys, socle", "try:", "    socle.charger(json.loads(sys.argv[1])); r = '-'",
                    "except socle.Refus as e:", "    r = e.code",
                    "print(json.dumps([r, [(n, m.__file__) for n, m in sys.modules.items() if n in socle.MODULES]]))"])
    return json.loads(subprocess.run([sys.executable, "-B", "-c", code, json.dumps(prm)], cwd=socle.ICI, check=True,
                                     capture_output=True, text=True).stdout)


def appel(argv, analyse_=analyse):
    """socle.executer dans ce processus, stderr capté : (code, ou type de l'exception sortie ; stderr)."""
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err):
            rc = socle.executer("essai", "objet", ("a.txt",), analyse_, argv)
    except (Exception, SystemExit) as e:
        rc = type(e).__name__
    return rc, err.getvalue()


def reecrire(d, nom, f):
    """Journal de fixture `nom` du dossier d réécrit : lignes = f(lignes)."""
    with open(os.path.join(d, nom), encoding="utf-8") as g:
        lignes = g.read().split(NL)[:-1]
    with open(os.path.join(d, nom), "w", encoding="utf-8") as g:
        g.write(NL.join(f(lignes)) + NL)


def lecture0(lignes, **sur):
    """Lignes de journal.jsonl, première lecture modifiée : clés de sur posées, ou retirées si None."""
    return [json.dumps({k: v for k, v in {**json.loads(lignes[0]), **sur}.items() if v is not None}), *lignes[1:]]


class TestSocle(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="p2_socle_")
        self.addCleanup(shutil.rmtree, self.d, True)

    def refus(self, code, f, *args):
        with self.assertRaises(socle.Refus) as c:
            f(*args)
        self.assertEqual(c.exception.code, code)

    def test_variable(self):
        """T-P2-SOC-2. Environnement passé en argument : la variable posée, même vide, refuse ; absente, aucun refus.
        Aucun test Python ne pose la variable. Mutation M-P2-02 : garde retirée ; M-P2R0-1 : garde sur la valeur."""
        for v in ("x", ""):
            self.refus("P2/variable", socle.garde, {"SHOGEN_S2_CAMPAGNE_CONTROL": v})
        self.assertIsNone(socle.garde({"AUTRE": "1"}))

    def test_schema(self):
        """T-P2-SOC-5. parametres.json du lot conforme ; clé en trop ou manquante (premier niveau ou imbriquée),
        flottant, booléen pour un entier (d ; un compte du masque), clé dupliquée, JSON illisible : P2/parametres.
        Mutation M-P2-35 : contrôle de schéma retiré ; M-P2R0-2 : sous-arbres non contrôlés ; M-P2R0-3 : clé dupliquée
        admise ; G-10 (G2) : booléen admis dans les comptes ; M-P2R0-9 : idem, par type ; M-P2R0-10 : calendrier hors
        D5 typé dict seul."""
        self.assertEqual(socle.lire(), tests.PRM)

        def variante(f):
            p = json.loads(json.dumps(tests.PRM))
            f(p)
            return json.dumps(p, ensure_ascii=False)
        cas = [variante(lambda p: p.update(autre="x")), variante(lambda p: p.pop("passes")),
               variante(lambda p: p["masque"].update(autre="x")), variante(lambda p: p["passes"].update(A=0.0)),
               variante(lambda p: p["masque"]["sautees_hors_d5"].update(calme=5701.0)),
               variante(lambda p: p["masque"]["calendrier_hors_d5"].update(calme=True)),
               variante(lambda p: p["voisinage"].update(d=True)), '{"lot": "x", ' + json.dumps(tests.PRM)[1:], "{"]
        for i, texte in enumerate(cas):
            with open(os.path.join(self.d, f"p{i}.json"), "w", encoding="utf-8") as f:
                f.write(texte)
            self.refus("P2/parametres", socle.lire, os.path.join(self.d, f"p{i}.json"))

    def test_epingles(self):
        """T-P2-SOC-1. Huit sha256 recopiés = épingles ; épingle d'un fichier de PLAN-S2BIS = sa ligne du SHA256SUMS de
        son dossier ; copie altérée d'un octet de chaque pièce, ou pièce absente : P2/plan-s2bis ; commun altéré
        refusé avant tout import (processus neuf) ; commun, regles, episodes chargés dans cet ordre, sous ces noms,
        depuis leurs chemins (P-1) ; module « regles » déjà chargé d'ailleurs : P2/plan-s2bis. Mutation M-P2-01 :
        contrôle de sha256 retiré ; M-P2R0-4 : pièce absente non refusée ; M-P2R0-5 : episodes chargé avant regles ;
        M-P2R0-8 : chemin du module chargé non contrôlé."""
        p = tests.PRM["plan_s2bis"]
        self.assertEqual(p["sha256"], EPINGLES)
        for cle in ("commun", "regles", "episodes", "parametres", "fixtures", "ep"):
            sums = "ep_sha256sums" if cle == "ep" else "sha256sums"
            with open(tests.CHEMINS[sums], encoding="utf-8") as f:
                lignes = f.read().split(NL)
            rel = os.path.relpath(p["chemins"][cle], os.path.dirname(p["chemins"][sums]))
            self.assertIn(f"{EPINGLES[cle]}  {rel}", lignes, cle)
        for cle, chemin in tests.CHEMINS.items():
            with open(chemin, "rb") as f:
                b = f.read()
            with open(os.path.join(self.d, cle), "wb") as f:
                f.write(b[:-1] + bytes([b[-1] ^ 1]))
            for faux in ("", ".absent"):
                self.refus("P2/plan-s2bis", socle.charger, prm_avec(**{cle: os.path.join(self.d, cle + faux)}))
        self.assertEqual(processus_neuf(prm_avec(commun=os.path.join(self.d, "commun"))), ["P2/plan-s2bis", []])
        self.assertEqual(processus_neuf(tests.PRM),
                         ["-", [[n, tests.CHEMINS[n]] for n in ("commun", "regles", "episodes")]])
        self.addCleanup(sys.modules.__setitem__, "regles", sys.modules["regles"])
        sys.modules["regles"] = types.ModuleType("regles")
        sys.modules["regles"].__file__ = os.path.join(self.d, "regles.py")
        self.refus("P2/plan-s2bis", socle.charger, tests.PRM)

    def test_sous_arbres(self):
        """T-P2-SOC-3. Valeurs recopiées à la main de scripts/plan-s2bis/parametres.json, égales à ce que lit le
        socle ; seuls les sous-arbres et épingles de la ligne P-3 sont lus. Mutation M-P2-03 : sous-arbres pris au
        parametres.json du lot ; M-P2R0-6 : sous-arbres non filtrés."""
        s = tests.PS2["segment"]
        self.assertEqual((s["t0"], s["n_fixe"], s["plages_exclues"]), (1787770800, 38600, [[1790273880, 1790435280]]))
        self.assertEqual((len(tests.PS2["pool_d1bis"]["unites"]), tests.PS2["fiv"]["ell"]),
                         (10, [1, 2, 3, 5, 10, 15, 20, 30, 60, 90, 120, 180, 240, 360, 480, 720, 1440]))
        self.assertEqual(sorted(tests.PS2), ["classes", "commit_analyse", "episodes", "fiv", "harnais_sha256",
                                             "paquet_s2", "pool_d1bis", "rendu_j28", "segment", "strates"])

    def test_ecarts(self):
        """T-P2-SOC-4. Type « ecart » de PLAN-S2BIS sans staleness, ou de même longueur avec pas_ecart au lieu de
        staleness : P2/ecarts ; tel quel : aucun refus. Mutation M-P2-36 : contrôle (d) retiré ; G-03 (G2) : longueurs
        seules comparées ; M-P2R0-11 : valeurs de r1.Ecart admises ; M-P2R0-12 : panne et hors_enveloppe seules."""
        r1 = tests.fx.r1
        self.assertIsNone(socle.controle_d(tests.PS2, r1))
        for faux in (["panne", "hors_enveloppe"], ["panne", "pas_ecart", "hors_enveloppe"]):
            self.refus("P2/ecarts", socle.controle_d, {"episodes": {"types": {"ecart": faux}}}, r1)

    def test_pool(self):
        """T-P2-POOL-1. (c) : hôte absent du pool d'une strate ; retrait non vide ; ligne « pool D1-bis » différente
        d'EP l.8 : P2/pool. Ligne écrite à la main pour deux hôtes ; ligne d'EP l.8 recopiée et regénérée pour dix.
        Mutation M-P2-37 : contrôle (c) retiré ; M-P2R0-7 : ligne « pool D1-bis » non comparée à EP l.8."""
        ps2 = {"strates": ["calme", "stress"], "pool_d1bis": {"unites": {"ha": "a", "hb": "b"}}}
        bon = {"pools_bis": {"calme": ["a", "b"], "stress": ["a", "b"]}, "retraits_bis": []}
        ep = [""] * 7 + ["pool D1-bis : « calme » 2 hôtes ; « stress » 2 hôtes ; retraits : aucun"]
        self.assertIsNone(socle.controle_c(bon, ps2, ep))
        retrait = [("stress", "hb", "b", 1, 3, "2·ok < n_s (seuil de flux presque mort, B.39)")]
        manque = dict(bon, pools_bis={"calme": ["a", "b"], "stress": ["a"]})
        trois = ep[:7] + [ep[7].replace("2 h", "3 h")]
        for d, e in ((manque, ep), (dict(bon, retraits_bis=retrait), ep), (bon, trois)):
            self.refus("P2/pool", socle.controle_c, d, ps2, e)
        dix = {"pools_bis": {"calme": list("abcdefghij"), "stress": list("abcdefghij")}, "retraits_bis": []}
        self.assertEqual((tests.EP[7], socle.ligne_pool_bis(dix)),
                         ("pool D1-bis : « calme » 10 hôtes ; « stress » 10 hôtes ; retraits : aucun",) * 2)

    def test_executer_refus(self):
        """T-P2-SOC-6, étendu à l'ordre des contrôles de executer. Fixture de 4 fenêtres de calme (a et b en panne à la
        1re, a seule à la 2e : a ok 2 fois, 2·2 = 4, gardé) : égale, code 0, corps de l'analyse. Bloc 3 épinglé à
        K + 1 : P2/coherence ; épingle d'un module du harnais altérée : P2/harnais ; type « ecart » sans staleness :
        P2/ecarts ; 3 fenêtres (a ok 1 fois sur 3, retiré) : P2/pool ; variable dans l'environnement passé :
        P2/variable. En refus : code 1, étiquette, ligne 2, une ligne de refus, aucune ligne d'analyse. Mutation
        M-P2-40 : contrôle (a) neutralisé ; M-P2-41 : harnais importé sans commun.importer_harnais ; M-P2R1-1 : code 0
        en refus ; M-P2R1-2 : étiquette omise ; M-P2R1-3 : (c) non appelé ; M-P2R1-4 : (d) non appelé ;
        M-P2R1-5 : garde non appelée ; M-P2R1-6 : .partiel non renommé."""
        def motif(i, f):
            return "panne_transport" if (i == 0 and f in "ab") or (i == 1 and f == "a") else "ok"

        def k_plus_un(p):
            p["rendu_j28"]["bloc3"]["calme"][1] += 1

        def harnais(p):
            p["harnais_sha256"]["shogen_s2/r1.py"] = "0" * 64

        def ecart(p):
            p["episodes"]["types"]["ecart"] = ["panne", "hors_enveloppe"]
        variable = {"SHOGEN_S2_CAMPAGNE_CONTROL": "x"}
        for n, modif, env, code in ((4, None, None, None), (4, k_plus_un, None, "P2/coherence"), (4, harnais, None,
                                    "P2/harnais"), (4, ecart, None, "P2/ecarts"), (3, None, None, "P2/pool"),
                                    (4, None, variable, "P2/variable")):
            ws = [tests.fx.VEN + 60 * i for i in range(n)]
            argv = tests.banc(self, ws, motif, list("abcde"), modif=modif, strates=["calme"])
            rc = socle.executer("essai", "objet", ("a.txt",), analyse, argv, env)
            with open(os.path.join(argv[argv.index("--sortie") + 1], "a.txt"), encoding="utf-8") as f:
                lignes = f.read().split(NL)
            tete = (socle.ETIQUETTE, "essai — objet (PLAN-S2BIS-2 ; SHOGEN-SIM-BIS-FIV-IDENTIF-1)")
            self.assertEqual((rc, tuple(lignes[:2]), lignes[-1]), (int(bool(code)), tete, ""))
            self.assertTrue(lignes[-2].startswith(f"REFUS {code} : ") if code else lignes[-2] == "ANALYSE")
            refus = [x[:6] for x in lignes].count("REFUS ")
            self.assertEqual(("ANALYSE" in lignes, refus), (not code, int(bool(code))))

    def test_lecture(self):
        """T-P2-LEC-1 (Q-P2R-3 ; SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1). Toute exception de la lecture des entrées,
        des contrôles ou de l'analyse : P2/lecture, nommé par le seul type de l'exception ; code 1, une ligne de refus,
        aucune analyse, stderr vide, aucune valeur de journal (fenêtre hors grille, message). Un cas par chemin :
        journal absent ; ligne corrompue non finale ; ligne non objet ; fenêtre hors grille ; strate journalisée
        incohérente ; strate hors paramètres ; unité hors pool ; classe divergente ; rendu absent ; prix illisible ;
        lecture sans flux ; analyse en échec. Mutation M-P2R1-11 : Refus et ValueError seuls rattrapés ; M-P2R1-12 :
        message de l'exception recopié ; M-P2R1-13 : refus nommés convertis en P2/lecture."""
        fx, ven = tests.fx, tests.fx.VEN
        hors = str(ven + 90)

        def echec(d, ps2, prm, ep):
            raise ValueError(f"valeur de journal {hors}")

        def j(nom, f):
            return lambda d, a: reecrire(d, nom, f)
        incoherente = json.dumps(fx.records.window_close_record(ven + 240, "stress", ven + 295.0))
        cas = [("FileNotFoundError", None, lambda d, a: os.remove(os.path.join(d, "control.jsonl")), analyse),
               ("ValueError", None, j("journal.jsonl", lambda x: ["{", *x]), analyse),
               ("AttributeError", None, j("control.jsonl", lambda x: ["[1]", *x]), analyse),
               ("ValueError", None, j("control.jsonl", lambda x: [*x, json.dumps(fx.marqueur(ven + 90))]), analyse),
               ("ValueError", None, j("control.jsonl", lambda x: [*x, incoherente]), analyse),
               ("ValueError", lambda p: p.update(strates=["stress"]), None, analyse),
               ("ValueError", lambda p: p["pool_d1bis"]["unites"].update(uz="z"), None, analyse),
               ("ValueError", lambda p: p["classes"].update(a="autre"), None, analyse),
               ("FileNotFoundError", None, lambda d, a: os.remove(a[a.index("--rendu") + 1]), analyse),
               ("InvalidOperation", None, j("journal.jsonl", lambda x: lecture0(x, price="abc")), analyse),
               ("KeyError", None, j("journal.jsonl", lambda x: lecture0(x, flux_id=None)), analyse),
               ("ValueError", None, None, echec)]
        for i, (nom, modif, apres, an) in enumerate(cas):
            with self.subTest(cas=i):
                argv = tests.banc(self, [ven + 60 * k for k in range(4)], lambda k, f: "ok", list("abcde"),
                                  modif=modif, strates=["calme"])
                if apres:
                    apres(argv[argv.index("--journaux") + 1], argv)
                self.assertEqual(appel(argv, an), (1, ""))
                with open(os.path.join(argv[argv.index("--sortie") + 1], "a.txt"), encoding="utf-8") as f:
                    texte = f.read()
                lignes = texte.split(NL)
                self.assertEqual((lignes[-2].split(" : ")[0], lignes[-2].endswith(f"({nom})"), lignes[-1],
                                  hors in texte, [x[:6] for x in lignes].count("REFUS "), "ANALYSE" in lignes),
                                 ("REFUS P2/lecture", True, "", False, 1, False))

    def test_usage_et_sortie(self):
        """T-P2-LEC-2 (SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1). Arguments hors CLI (--sortie absent, -h, option
        inconnue) : REFUS P2/usage sur stderr, code 2, aucune sortie ; --sortie qui est un fichier : REFUS P2/sortie
        sur stderr, code 1. Mutation M-P2R1-14 : erreur d'arguments laissée à argparse ; M-P2R1-15 : aide admise ;
        M-P2R1-16 : écriture des sorties non rattrapée ; M-P2R1-17 : code 1 en usage."""
        argv = tests.banc(self, [tests.fx.VEN + 60 * k for k in range(4)], lambda k, f: "ok", list("abcde"),
                          strates=["calme"])
        i = argv.index("--sortie")
        for a in (argv[:i] + argv[i + 2:], argv + ["-h"], argv + ["--autre", "x"]):
            self.assertEqual(appel(a), (2, "REFUS P2/usage : arguments de essai hors de la CLI" + NL))
        self.assertFalse(os.path.exists(argv[i + 1]))
        with open(argv[i + 1], "w", encoding="utf-8") as f:
            f.write("fichier")
        self.assertEqual(appel(argv), (1, "REFUS P2/sortie : sorties non écrites dans le dossier de sortie "
                                          "(FileExistsError)" + NL))
