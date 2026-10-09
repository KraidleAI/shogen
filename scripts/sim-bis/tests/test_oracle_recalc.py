"""Adaptateur d'oracle croisé avec RECALC-BIS, SB-13 première passe (E-S-01, E-S-51 ; SHOGEN-SIM-BIS-CONTRAT-RB6-1).
SB-13a : épingles du paquet s2bis au commit f458980 égales aux valeurs de `git show f458980:s2bis/<chemin> | sha256sum`
(rotation.py : 4183fbe6…, l'empreinte que cite le contre-contrôle de la tranche 3), extraction, refus nommés d'une
épingle fausse et d'un commit absent, frontière d'E-S-01 lue par `ast`. SB-13b : chargement sous shogen_s2bis. SB-13c
(E-S-51) : o(r, u) des six vecteurs du contrat RB-6 recalculés par sha256sum et bc (journal de SB-13,
vecteurs-rb6.txt), K^(r) écrit à la main, 100 séries synthétiques à graine fixe. Chaque test nomme les mutations
qui le rougissent."""
import ast
import functools
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import commun
import oracle_recalc
import regle
from tests import test_fitness, test_fitness_tirages

PRM = commun.charger_parametres(environ={})
COMMIT = "f45898040e10858d5f7ed8944ad66f5ec7e9bdde"
FICHIERS = {"config/analyse.json": "e9243c79ff942c3444fbd93495644b6b5556435fe193a0f959ad1708233a1d00",
            "shogen_s2bis/__init__.py": "3908b0944bac803df5d2e447dddc9344d5dc61db2e5531d729b5c926425762d8",
            "shogen_s2bis/recalc/__init__.py": "42e2623a7d8fd15b6a90aeb4b7551bc45198df176187af526e7657cd12ca78d1",
            "shogen_s2bis/recalc/config_analyse.py": "82abdba525d90c829998dd4539b7fb16b9366e4599f33d13c3916f155bcd8b26",
            "shogen_s2bis/recalc/rotation.py": "4183fbe6bf633f394e8d289066c0dd0323cfa5561f173b54b15b9f0ad13a4202",
            "tests/test_rotation.py": "049e0b5165450011b8870e03660465de546bdf573516e13c4bc46287dfa8dc0a"}


class TestExtraction(unittest.TestCase):
    def test_epingles(self):
        """Section « oracle_recalc » : commit f458980 complet, dossier s2bis, six empreintes égales aux valeurs de
        sha256sum. Mutations M-13A-01 (empreinte de rotation.py de RB-6b, 7ff0d437…), M-13A-02 (commit de RB-6b)."""
        o = PRM["oracle_recalc"]
        self.assertEqual((o["commit"], o["dossier"], o["fichiers"]), (COMMIT, "s2bis", FICHIERS))

    def test_extraction(self):
        """extraire écrit sous le dossier donné les six fichiers épinglés, et eux seuls, aux empreintes de sha256sum ;
        il rend le dossier s2bis de l'extraction. Mutations M-13A-03 (dossier rendu sans s2bis), M-13A-04 (dernier
        fichier non écrit), M-13A-05 (fichier tronqué d'un octet à l'écriture)."""
        with tempfile.TemporaryDirectory() as d:
            racine = oracle_recalc.extraire(PRM, d)
            ecrits = sorted(os.path.relpath(os.path.join(x, f), racine) for x, _s, fs in os.walk(d) for f in fs)
            lus = {}
            for f in ecrits:
                with open(os.path.join(racine, f), "rb") as g:
                    lus[f] = hashlib.sha256(g.read()).hexdigest()
        self.assertEqual((racine, lus), (os.path.join(d, "s2bis"), FICHIERS))

    def test_schema(self):
        """Commit abrégé, en majuscules ou de 41 caractères, fichier en moins ou en plus, empreinte en majuscules :
        PARAMETRES/schema. Mutations M-13A-06 (commit non contraint), M-13A-07 (fichiers non contraints)."""
        for f in (lambda o: o.update(commit="f458980"), lambda o: o.update(commit=COMMIT.upper()),
                  lambda o: o.update(commit=COMMIT + "0"), lambda o: o["fichiers"].pop("config/analyse.json"),
                  lambda o: o["fichiers"].update({"shogen_s2bis/collecte/config.py": "0" * 64}),
                  lambda o: o["fichiers"].update({"config/analyse.json": FICHIERS["config/analyse.json"].upper()})):
            p = json.loads(json.dumps(PRM))
            f(p["oracle_recalc"])
            with self.assertRaises(commun.Refus) as c:
                commun.controler(p, commun.SCHEMA)
            self.assertEqual(c.exception.code, "PARAMETRES/schema")

    def test_refus(self):
        """Variable de la copie scellée posée : CAMPAGNE/variable (E-S-02) ; empreinte fausse : ORACLE/sha256 ; commit
        absent, fichier absent du commit (2fe7d9c, RB-0a : sous-paquet recalc sans rotation.py), dépôt sans git :
        ORACLE/extraction. Mutations M-13A-08 (empreintes non contrôlées), M-13A-09 (sortie de git non contrôlée),
        M-13A-10 (garde de campagne retirée)."""
        with mock.patch.object(commun.os, "environ", {commun.VARIABLE: ""}), tempfile.TemporaryDirectory() as d:
            with self.assertRaises(commun.Refus) as c:
                oracle_recalc.extraire(PRM, d)
            self.assertEqual(c.exception.code, "CAMPAGNE/variable")
        o = PRM["oracle_recalc"]
        for faux, depot, code in ((dict(o, fichiers=dict(FICHIERS, **{"config/analyse.json": "0" * 64})), commun.RACINE,
                                   "ORACLE/sha256"),
                                  (dict(o, commit="0" * 40), commun.RACINE, "ORACLE/extraction"),
                                  (dict(o, commit="2fe7d9c56f63471d61ef5d5371f41a4a90002266"), commun.RACINE,
                                   "ORACLE/extraction"),
                                  (o, os.path.join(commun.RACINE, "inexistant"), "ORACLE/extraction")):
            with tempfile.TemporaryDirectory() as d, self.assertRaises(commun.Refus) as c:
                oracle_recalc.extraire(dict(PRM, oracle_recalc=faux), d, depot)
            self.assertEqual(c.exception.code, code, faux["commit"][:8])

    def test_frontiere_e_s_01(self):
        """E-S-01 : oracle_recalc.py présent et adaptateur pour les deux gardes `ast` (frontière et tirages) ; ses
        imports écrits : bibliothèque standard et modules du moteur seuls (le paquet s2bis n'entre que par l'extraction
        épinglée) ; un module du moteur qui l'importe est refusé. Mutations M-13A-11 (import shogen_s2bis écrit dans
        l'adaptateur), M-13A-12 (oracle_recalc.py hors des adaptateurs de test_fitness_tirages)."""
        f = "oracle_recalc.py"
        self.assertTrue(os.path.exists(os.path.join(commun.ICI, f)))
        self.assertIn(f, test_fitness.ORACLES & test_fitness_tirages.ORACLES)
        with open(os.path.join(commun.ICI, f), encoding="utf-8") as g:
            arbre = ast.parse(g.read())
        noms = {a.name.split(".")[0] for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
        noms |= {n.module.split(".")[0] for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
        moteur = {x[:-3] for x in os.listdir(commun.ICI) if x.endswith(".py") and x not in test_fitness.ORACLES}
        self.assertEqual(sorted(x for x in noms if x not in sys.stdlib_module_names and x not in moteur), [])
        self.assertNotEqual(test_fitness.refus_imports("import oracle_recalc", moteur | {"oracle_recalc"}), [])


H = oracle_recalc.charger(PRM)


def processus(lignes: list, tmpdir=None) -> subprocess.CompletedProcess:
    """Processus neuf lancé depuis le dossier du lot, sans la variable de campagne (TMPDIR donné le cas échéant)."""
    env = {k: v for k, v in os.environ.items() if k != commun.VARIABLE}
    if tmpdir:
        env["TMPDIR"] = tmpdir
    return subprocess.run([sys.executable, "-B", "-c", chr(10).join(lignes)], cwd=commun.ICI, env=env,
                          capture_output=True, text=True, timeout=120)


class TestChargement(unittest.TestCase):
    def test_modules_charges(self):
        """charger rend rotation et config_analyse, chargés sous shogen_s2bis.recalc depuis un dossier
        « oracle_recalc_… » de TMPDIR, et analyse.json lu (bloc rotations R = 9 999, seuil = 99, lu à la main).
        Mutations M-13B-01 (modules chargés sous un autre nom), M-13B-02 (analyse.json non lu)."""
        d = os.path.join(tempfile.gettempdir(), "oracle_recalc_")
        self.assertEqual((sorted(H), H["rotation"].__name__, H["config_analyse"].__name__, H["analyse"]["rotations"],
                          [H[m].__file__.startswith(d) for m in ("rotation", "config_analyse")]),
                         (["analyse", "config_analyse", "rotation"], "shogen_s2bis.recalc.rotation",
                          "shogen_s2bis.recalc.config_analyse", {"R": 9999, "seuil": 99}, [True, True]))

    def test_nettoyage_du_dossier(self):
        """Dans un processus neuf, à TMPDIR vide (E-S-06) : un seul dossier « oracle_recalc_… », d'où rotation est
        chargée, retiré à la sortie du processus. Mutation M-13B-03 (dossier jamais retiré)."""
        code = ["import os, tempfile, commun, oracle_recalc",
                "h = oracle_recalc.charger(commun.charger_parametres(environ={}))",
                "d = tempfile.gettempdir()",
                "print(sorted(x[:14] for x in os.listdir(d)), h['rotation'].__file__.startswith(d))"]
        with tempfile.TemporaryDirectory() as d:
            p = processus(code, d)
            self.assertEqual((p.stdout.strip(), os.listdir(d)), ("['oracle_recalc_'] True", []), p.stderr[-300:])

    def test_cache_indexe_sur_l_epingle(self):
        """Même épingle (source changée), mêmes modules sans nouvelle extraction ; autre commit, autre dossier ou autre
        empreinte : ORACLE/epingle. Mutations M-13B-04 (épingle non comparée), M-13B-05 (empreintes hors de
        l'épingle), M-13B-06 (source dans l'épingle), M-13B-07 (extraction refaite à chaque appel)."""
        o = PRM["oracle_recalc"]
        self.assertIs(oracle_recalc.charger(dict(PRM, oracle_recalc=dict(o, source="autre")))["rotation"],
                      H["rotation"])
        for faux in (dict(o, commit="0" * 40), dict(o, dossier="ailleurs"),
                     dict(o, fichiers=dict(o["fichiers"], **{"shogen_s2bis/recalc/rotation.py": "0" * 64}))):
            with self.assertRaises(commun.Refus) as c:
                oracle_recalc.charger(dict(PRM, oracle_recalc=faux))
            self.assertEqual(c.exception.code, "ORACLE/epingle")

    def test_modules_hors_epingles(self):
        """Dans un processus neuf : un shogen_s2bis déjà chargé d'ailleurs, ou un module shogen_s2bis.* hors des
        fichiers épinglés : ORACLE/modules. Mutations M-13B-08 (contrôle des modules chargés retiré), M-13B-09
        (shogen_s2bis déjà chargé admis), M-13B-10 (modules chargés comptés sur le seul paquet de tête)."""
        for intrus in ("shogen_s2bis", "shogen_s2bis.intrus"):
            code = ["import sys, types", f"m = types.ModuleType({intrus!r})", "m.__file__ = '/hors/x.py'",
                    f"sys.modules[{intrus!r}] = m", "import commun, oracle_recalc", "try:",
                    "    oracle_recalc.charger(commun.charger_parametres(environ={}))",
                    "except commun.Refus as e:", "    print(e.code)"]
            p = processus(code)
            self.assertEqual(p.stdout.strip(), "ORACLE/modules", (intrus, p.stderr[-300:]))

    def test_analyse_lu_dans_l_extraction(self):
        """C-6 de la G2 (O-1) : dans un processus neuf, config/analyse.json est écrit puis lu en octets dans le dossier
        s2bis extrait du commit épinglé, jamais dans l'arbre de travail (dont les octets sont aujourd'hui les mêmes) :
        fichiers ouverts par builtins.open pendant charger, relevés avec leur mode. Mutations M-G2-12 (lu sous
        commun.RACINE), M-13B-13 (lu par un chemin tiré de commun.ICI), M-13B-14 (arbre de travail préféré s'il
        existe)."""
        code = ["import builtins, os, commun, oracle_recalc", "lus, vrai = [], builtins.open",
                "def ouvrir(f, mode='r', *a, **k):", "    lus.append((os.path.realpath(f), mode))",
                "    return vrai(f, mode, *a, **k)", "builtins.open = ouvrir",
                "h = oracle_recalc.charger(commun.charger_parametres(environ={}))", "builtins.open = vrai",
                "s2bis = os.path.realpath(os.path.join(os.path.dirname(h['rotation'].__file__), '..', '..'))",
                "print(sorted((os.path.relpath(f, s2bis), m) for f, m in lus if f.endswith('analyse.json')))"]
        p = processus(code)
        self.assertEqual(p.stdout.strip(), "[('config/analyse.json', 'rb'), ('config/analyse.json', 'wb')]",
                         p.stderr[-300:])


G6 = "6fce4df75bac7db6ff01817b407f6331e49ec2ebf31f02e6672d3ab8a3bc9688"  # printf %s SHOGEN-RB6-VECTEURS | sha256sum
# (strate, r, u, n, o, R) : vecteurs du contrat RB-6 (ROTATION-S2BIS.md §5), o par sha256sum et bc ; R : plus petit R
# de la règle (R + 1 multiple de 100, seuil entier) au moins égal à r.
VECTEURS = (("calme", 1, "api.binance.com", 109440, 107527, 99),
            ("stress", 9999, "ethereum-rpc.publicnode.com", 43776, 24225, 9999),
            ("calme", 4242, "api.kraken.com", 54720, 39743, 4299), ("calme", 1, "api.coinbase.com", 7, 0, 99),
            ("calme", 7, "api.coinbase.com", 7, 6, 99), ("calme", 1, "api.binance.com", 54720, 52807, 99))
P = "api-pub.bitfinex.com"                       # unité non décalée des vecteurs (« - » = 0x2D précède « . » = 0x2E)
HOTES = ("api-pub.bitfinex.com", "api.binance.com", "api.coinbase.com", "api.gemini.com", "api.kraken.com",
         "ethereum-rpc.publicnode.com", "okx", "www.bitstamp.net")
HOTES10 = HOTES + ("api.coingecko.com", "api.llama.fi")                   # dix unités par classe (C-4 de la G2)


def flux(*cle) -> int:
    """Entier de 256 bits, SHA-256 big-endian de « SB-13|<clé>|… » : graine fixe, aucun module random."""
    return int.from_bytes(hashlib.sha256("|".join(map(str, ("SB-13",) + cle)).encode("ascii")).digest(), "big")


def synthetique(i: int) -> tuple:
    """Série synthétique i (0 ≤ i < 100) : (graine, strate, n, classes, première unité, R, n_s). R = 99 (i < 90), 999
    (i < 98), 9 999 ; n = 1, 2, 3 pour i = 0, 1, 2, puis 4 à 203 (4 à 43 à R = 9 999) ; BTC : 2 à 6 hôtes (2 ou 3 à
    R = 9 999), ETH, USDC, USDT parmi eux (ETH seul à R = 9 999) ; masques : ET de 1 à 3 tirages, les mêmes pour
    toutes les unités d'une classe si i % 4 = 1 (séries liées) ; première unité : min du pool BTC (regle.premiere),
    retirée de BTC si i % 5 = 3 (critère d'absorption), None et BTC vide si i % 5 = 4 ; i % 10 = 5 (dix séries) :
    les dix hôtes de HOTES10 dans les quatre classes (C-4 de la G2 : m_t ≥ 8, plan de bits 3 de regle.paires) ;
    n_s = n, sauf i % 6 = 5 : n < n_s ≤ 2n (C-2 de la G2)."""
    R = 99 if i < 90 else 999 if i < 98 else 9999
    n = (1, 2, 3)[i] if i < 3 else 4 + flux(i, "n") % (200 if R < 9999 else 40)
    dix, k = i % 10 == 5, 2 + flux(i, "k") % (5 if R < 9999 else 2)
    btc = sorted(HOTES10 if dix else sorted(HOTES, key=lambda h: flux(i, "h", h))[:k])

    def masque(c, u):
        x, u = (1 << n) - 1, "lie" if i % 4 == 1 else u
        for j in range(1 + flux(i, "d", c, u) % 3):
            x &= flux(i, "m", c, u, j)
        return x
    classes = {"BTC": {u: masque("BTC", u) for u in btc}}
    for c in ("ETH", "USDC", "USDT") if R < 9999 else ("ETH",):
        if sous := [u for u in btc if dix or flux(i, "c", c, u) % 3]:
            classes[c] = {u: masque(c, u) for u in sous}
    p = regle.premiere(btc)
    if i % 5 == 3:
        del classes["BTC"][p]
    elif i % 5 == 4:
        p, classes["BTC"] = None, {}
    ns = n + 1 + flux(i, "ns") % n if i % 6 == 5 else n
    return format(flux(i, "graine"), "064x"), ("calme", "stress")[i % 2], n, classes, p, R, ns


@functools.lru_cache(maxsize=None)
def croisements() -> tuple:
    """Les 100 séries synthétiques croisées une fois par processus : ((i, entrée, écarts, réplique, RB-6), …)."""
    out = []
    for i in range(100):
        g, s, n, classes, p, R, ns = e = synthetique(i)
        out.append((i, e, *oracle_recalc.croiser(PRM, H, g, s, n, ns, classes, p, R)))
    return tuple(out)


class TestCroisement(unittest.TestCase):
    def test_vecteurs_e_s_51(self):
        """E-S-51, six vecteurs du contrat RB-6 (cinq exigés, dont o = 0 et o = n − 1) : o(r, u) de la réplique et de
        RB-6 extrait égaux à sha256sum et bc ; deux unités, P non décalée au bit o, u au bit 0 : la rotation r porte le
        bit 0 de u en o (sens du contrat §2.2), d'où K^(r) = S^(r) = 1 des deux côtés ; P au bit (o + 1) mod n : 0 ;
        croiser sans écart sur les R rotations ; la sixième entrée aussi à n′ = 54 720 < n_s = 109 440 (C-2 de la G2).
        Mutations M-13C-01 (premiere non transmise à RB-6), M-13C-02 (K_r pris dans la loi triée de complet), M-13C-03
        (sens de rotation inversé dans regle.tourner), M-13C-04 (rotations de regle._entrees à trois séries non nulles
        au moins), M-G2-02 (n_s transmis à RB-6), M-13C-16 (n et n_s échangés vers la réplique), M-13C-17 (rotations
        de regle._entrees modulo n_s), M-13C-18 (o de la réplique comparé modulo n_s)."""
        rot = H["rotation"]
        for s, r, u, n, o, R in VECTEURS:
            self.assertEqual((regle.decalage(G6, s, r, u, n), rot.decalage(G6, s, r, u, n)), (o, o), (s, r, u, n))
            for bit, x in ((o, 1), ((o + 1) % n, 0)):
                e, a, b = oracle_recalc.croiser(PRM, H, G6, s, n, n, {"BTC": {P: 1 << bit, u: 1}}, P, R)
                self.assertEqual((e, [(y["BTC"]["K_r"][r - 1], y["BTC"]["S_r"][r - 1]) for y in (a, b)]),
                                 ([], [(x, x), (x, x)]), (s, r, u, n, bit))
        s, r, u, n, o, R = VECTEURS[5]
        e, a, b = oracle_recalc.croiser(PRM, H, G6, s, n, 109440, {"BTC": {P: 1 << o, u: 1}}, P, R)
        self.assertEqual((e, a["BTC"]["K_r"][r - 1], b["BTC"]["K_r"][r - 1]), ([], 1, 1))

    def test_series_synthetiques_e_s_51(self):
        """E-S-51, 100 séries synthétiques à graine fixe (synthetique) : aucun écart de croiser (o(r, u) de toute unité
        décalée, K, S, K^(r), S^(r), C, C1, C_S, K_crit, moyenne, à R complet). Couverture comptée : R = 99, 999,
        9 999 (90, 8, 2) ; 50 en calme ; première unité None (20) ou absente de BTC (20) ; n = 1 ; au moins une classe
        à C ≤ seuil et une à C > seuil ; n_s > n (16, C-2 de la G2) ; 40 classes de dix unités, dont 22 à m_t ≥ 8 à une
        même position (C-4). Mutations M-13C-05 (arrêt anticipé, regle.decider, au lieu de complet), M-13C-06
        (seuil + 1 transmis à RB-6), M-13C-07 (C1 au seuil k_crit au lieu de k_crit − 1), M-13C-08 (S non suivie par la
        réplique), M-13C-09 (K_crit de regle.complet décalé d'un rang), M-G2-13 (plan de bits 3 de regle.paires
        faussé), M-13C-19 (termes croisés du plan 3 omis), M-13C-20 (trois plans de bits)."""
        tout = croisements()
        self.assertEqual([(i, e[:12]) for i, _x, e, _a, _b in tout if e], [])
        R = [x[5] for _i, x, *_ in tout]
        alpha = PRM["regle"]["alpha"]
        rejets = [sum(y["C"] <= regle.seuil(x[5], alpha) for y in a.values()) for _i, x, _e, a, _b in tout]
        self.assertEqual(([R.count(v) for v in (99, 999, 9999)], [x[1] for _i, x, *_ in tout].count("calme"),
                          sum(x[4] is None for _i, x, *_ in tout),
                          sum(x[4] is not None and x[4] not in x[3]["BTC"] for _i, x, *_ in tout),
                          [x[2] for _i, x, *_ in tout].count(1), min(sum(rejets), 1),
                          min(sum(len(a) - k for (*_r, a, _b), k in zip(tout, rejets)), 1)),
                         ([90, 8, 2], 50, 20, 20, 1, 1, 1))
        dix = [max(sum(m >> t & 1 for m in c.values()) for t in range(x[2])) for _i, x, *_ in tout
               for c in x[3].values() if len(c) == 10]
        self.assertEqual((sum(x[6] > x[2] for _i, x, *_ in tout), len(dix), sum(v >= 8 for v in dix)), (16, 40, 22))

    def test_croiser_voit_les_ecarts(self):
        """croiser voit chaque écart : RB-6 altéré en des points connus (o(3, « c.d ») et o(99, « e ») + 1 mod n,
        R = 99 ; K, S, K^(1), S^(1), C, C_S, K_crit et moyenne + 1 ; C1 + 1 par resume ; classe ZZZ en plus) : écarts
        exactement (BTC, clé) pour les neuf clés, (ZZZ, clé) pour les neuf, puis (o, 3, c.d) et (o, 99, e). Mutations
        M-13C-10 (écarts des classes d'un seul côté ignorés), M-13C-11 (dernière unité décalée hors de la comparaison
        des o), M-13C-12 (dernière rotation hors de la comparaison des o), M-13C-13 (S_r non comparé). C-1 de la G2 :
        une unité décalée absente de BTC (g.h, en ETH seule), o(7, g.h) altéré : seul écart (o, 7, g.h). Mutations
        M-G2-01 (o des seules unités de BTC), M-13C-14 (unités de la première classe seule), M-13C-15 (unités de
        toutes les classes sauf la dernière)."""
        vrai = H["rotation"]

        def lois(*a):
            sortie = vrai.lois(*a)
            x = sortie["BTC"]
            x.update({k: x[k] + 1 for k in ("K", "S", "C", "C_S", "K_crit", "K_moyen")},
                     K_r=[x["K_r"][0] + 1] + x["K_r"][1:], S_r=[x["S_r"][0] + 1] + x["S_r"][1:])
            return dict(sortie, ZZZ=x)
        faux = types.SimpleNamespace(lois=lois, resume=lambda *a: (vrai.resume(*a)[0] + 1,) + vrai.resume(*a)[1:],
                                     decalage=lambda g, s, r, u, n: (vrai.decalage(g, s, r, u, n)
                                                                     + ((r, u) in ((3, "c.d"), (99, "e")))) % n)
        e, _a, _b = oracle_recalc.croiser(PRM, dict(H, rotation=faux), G6, "calme", 4, 4,
                                          {"BTC": {"a.b": 11, "c.d": 6, "e": 13}}, "a.b", 99)
        cles = ("K", "S", "K_r", "S_r", "C", "C1", "C_S", "K_crit", "K_moyen")      # écrites à la main
        self.assertEqual(e, [("BTC", k) for k in cles] + [("ZZZ", k) for k in cles] + [("o", 3, "c.d"), ("o", 99, "e")])
        un = types.SimpleNamespace(lois=vrai.lois, resume=vrai.resume, decalage=lambda g, s, r, u, n: (
            vrai.decalage(g, s, r, u, n) + ((r, u) == (7, "g.h"))) % n)
        e, _a, _b = oracle_recalc.croiser(PRM, dict(H, rotation=un), G6, "stress", 5, 5,
                                          {"BTC": {"a.b": 3}, "ETH": {"a.b": 1, "g.h": 5}}, "a.b", 99)
        self.assertEqual(e, [("o", 7, "g.h")])


if __name__ == "__main__":
    unittest.main()
