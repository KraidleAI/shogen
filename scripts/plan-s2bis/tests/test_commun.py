"""Commun du lot PLAN-S2BIS : étiquette, portée du J28, épingles du harnais, bloc 3, contrôle de cohérence, pool
D1-bis, chargeur, classement, refus. Attendus écrits à la main ; chaque test nomme la mutation qui le rougit."""
import json
import os
import subprocess
import sys
import unittest
from decimal import Decimal

import commun
from tests import fixtures as fx

DEUX_NEUVIEMES = "0." + "2" * 50          # 2/9 à 50 chiffres significatifs, écrit à la main


def analyse(d, prm):
    return ["ANALYSE"]


class TestCommun(unittest.TestCase):
    def setUp(self):
        self.d = fx.dossier(self, "plan_commun_")

    def test_etiquette_mot_pour_mot(self):
        """Texte du G0 (l.25). Mutation MC-1 : un caractère de ETIQUETTE change."""
        attendu = "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)"
        self.assertEqual((commun.ETIQUETTE, fx.PRM["etiquette"]), (attendu, attendu))

    def test_portee_egale_a_la_table_du_rendu(self):
        """Sortie « j28 » de rendu_unique.SORTIES, lue dans un sous-processus (aucun module hors épingles ici).
        Mutation MC-2 : n_fixe de parametres.json porté à 38601."""
        code = ("import importlib.util, json, sys; s = importlib.util.spec_from_file_location('ru', sys.argv[1]); "
                "m = importlib.util.module_from_spec(s); s.loader.exec_module(m); "
                "print(json.dumps([[x[1], [list(p) for p in x[2]]] for x in m.SORTIES if x[0] == 'j28']))")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        out = subprocess.run([sys.executable, "-B", "-c", code, os.path.join(fx.HARNAIS, "tools", "rendu_unique.py")],
                             capture_output=True, text=True, env=env, check=True).stdout
        seg = fx.PRM["segment"]
        self.assertEqual(json.loads(out), [[{"t0": seg["t0"], "n_fixe": seg["n_fixe"]}, seg["plages_exclues"]]])
        self.assertEqual((seg["t0"], seg["n_fixe"], seg["plages_exclues"]), (1787770800, 38600, [[1790273880, 1790435280]]))

    def test_importer_harnais_refuse_une_epingle_fausse(self):
        """Mutation MC-3 : contrôle des épingles retiré (l'import passerait)."""
        faux = dict(fx.PRM["harnais_sha256"], **{"shogen_s2/r1.py": "0" * 64})
        with self.assertRaises(ValueError):
            commun.importer_harnais(fx.HARNAIS, faux)
        with self.assertRaises(ValueError):
            commun.importer_harnais(fx.HARNAIS, dict(fx.PRM["harnais_sha256"], **{"shogen_s2/absent.py": "0" * 64}))

    def test_module_hors_epingles_refuse(self):
        """Module de shogen_s2 non épinglé (sources) déjà chargé : importer_harnais refuse, dans un sous-processus.
        Prototype P-4 du réviseur. Mutation RV-03 : garde des modules chargés hors épingles retirée."""
        code = ("import sys; sys.path.insert(0, sys.argv[1]); import shogen_s2.sources; import commun; "
                "p = commun.lire_parametres(); commun.importer_harnais(sys.argv[1], p['harnais_sha256'])")
        r = subprocess.run([sys.executable, "-B", "-c", code, fx.HARNAIS], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), cwd=os.path.dirname(os.path.dirname(
                               os.path.abspath(fx.__file__))))
        self.assertEqual((r.returncode != 0, "hors des fichiers épinglés" in r.stderr), (True, True))

    def test_parametres_figes_par_adr(self):
        """Pool D1-bis d'ADR-0029 §2.5 l.166 (10 hôtes, okx par okx_ticker ; ni okx_index ni pyth) ; classes et planchers
        d'ADR-0020 (§2.6 l.180) égaux à sources.py du harnais épinglé (sous-processus) ; facteurs, quantiles, grille et
        bornes de §2.6 l.179-180 ; σ au paquet : population de clôture (adjudication A-1). Prototype P-3 du réviseur.
        Mutation RV-01, RV-25, RV-26, RV-28 du réviseur ; MC-14 : population de σ « axe_i »."""
        code = ("import json, sys; sys.path.insert(0, sys.argv[1]); from shogen_s2 import sources as s; "
                "print(json.dumps([s.SIGMA_FLOORS_ADR0020_SECONDS, s.SIGMA_CLASS_OF_FLUX]))")
        planchers, classes = json.loads(subprocess.run([sys.executable, "-B", "-c", code, fx.HARNAIS], check=True,
                                                       capture_output=True, text=True).stdout)
        p, u = fx.PRM, fx.PRM["pool_d1bis"]["unites"]
        hotes = {"binance", "coinbase", "kraken", "okx", "bitstamp", "gemini", "bitfinex", "coingecko", "defillama",
                 "chainlink"}
        self.assertEqual((set(u), u["okx"], p["pool_d1bis"]["seuil_presque_mort"]), (hotes, "okx_ticker", True))
        self.assertEqual({h: f for h, f in u.items() if h != "okx"}, {h: h for h in hotes - {"okx"}})
        attendu = {"place_horodatee": 30, "agregateur": 300, "oracle_chainlink": 5400, "sans_horodatage": None}
        self.assertEqual((p["sigma"]["planchers_s"], {c: planchers[c] for c in attendu}), (attendu, attendu))
        self.assertEqual(p["classes"], {f: classes[f] for f in u.values()})
        self.assertEqual([p["tau"][k] for k in ("facteur", "quantile", "pas", "borne_basse", "borne_haute_exclue")],
                         ["1.5", [999, 1000], "0.0005", "0.0005", "0.0285"])
        self.assertEqual((p["sigma"]["facteur"], p["sigma"]["quantile"], p["sigma_population"]), ("3", [99, 100], "cloture"))

    def test_lire_bloc3_premier_bloc_seulement(self):
        """La ligne de strate poolée et le bloc 3 répété de la sensibilité ne sont pas lus. Mutation MC-4 : lecture
        poursuivie après le premier bloc 4 (n = 1, K = 0 de la sensibilité)."""
        r = fx.rendu(os.path.join(self.d, "r.out"), {"calme": (24585, 154, "0.0013"), "stress": (11397, 133, "0.0014")})
        self.assertEqual(commun.lire_bloc3(r), {"calme": (24585, 154, "0.0013"), "stress": (11397, 133, "0.0014")})

    def test_controle_egal_et_ecarts(self):
        """Égal ; puis K, dernier chiffre de P̂_more, strate absente du recompte, sha du rendu, bloc 3 du rendu différent
        de l'épingle : écart. Mutation MC-5 : rendu relu non comparé à l'épingle (dernier cas égal)."""
        d = {"base": {"strates": {"calme": {"n": 3, "K": 1, "P_more": Decimal(DEUX_NEUVIEMES)}}}}
        bon = fx.rendu(os.path.join(self.d, "a.out"), {"calme": (3, 1, DEUX_NEUVIEMES)})

        def ok(b3, chemin=bon, sha=None):
            p = {"rendu_j28": {"sha256": sha or commun.sha256(chemin), "bloc3": b3}}
            return commun.controle(d, p, chemin)[0]
        self.assertTrue(ok({"calme": [3, 1, DEUX_NEUVIEMES]}))
        self.assertFalse(ok({"calme": [3, 2, DEUX_NEUVIEMES]}, fx.rendu(os.path.join(self.d, "b.out"),
                                                                       {"calme": (3, 2, DEUX_NEUVIEMES)})))
        trois = DEUX_NEUVIEMES[:-1] + "3"
        self.assertFalse(ok({"calme": [3, 1, trois]}, fx.rendu(os.path.join(self.d, "c.out"), {"calme": (3, 1, trois)})))
        deux = {"calme": (3, 1, DEUX_NEUVIEMES), "stress": (1, 0, "0")}
        self.assertFalse(ok({s: list(v) for s, v in deux.items()}, fx.rendu(os.path.join(self.d, "e.out"), deux)))
        self.assertFalse(ok({"calme": [3, 1, DEUX_NEUVIEMES]}, sha="0" * 64))
        autre = fx.rendu(os.path.join(self.d, "f.out"), {"calme": (3, 1, DEUX_NEUVIEMES), "stress": (1, 0, "0")})
        self.assertFalse(ok({"calme": [3, 1, DEUX_NEUVIEMES]}, autre))

    def _dix(self, seuil=True, classes=None):
        """10 fenêtres calmes ; c jamais ok, d ok 5 fois, e ok 4 fois puis statut ok sans prix (non ok, B.39) puis absente,
        f hors des unités."""
        ws = [fx.VEN + 60 * i for i in range(10)]
        pool = ["a", "b", "c", "d", "e", "f"]
        fx.journaux(self.d, ws, lambda i, f: "panne_transport" if f == "c" else "panne_http" if f == "d" and i >= 5
                    else "nul" if f == "e" and i == 4 else None if f == "e" and i > 4 else "ok", pool, classes)
        p = fx.prm_fixture(pool[:5], {}, "-", ws[0], 10)
        p["pool_d1bis"]["seuil_presque_mort"] = seuil
        return commun.charger(self.d, p)

    def test_pool_d1bis_seuil_et_egalite(self):
        """n = 10 : c retiré (ok = 0), e retiré (2·4 < 10), d gardé (2·5 = 10, égalité). Mutation MC-6 : « ≤ » au lieu
        de « < » (d retiré) ; MC-7 : seuil ignoré (e gardé) ; RV-05 : ok sans exigence de prix (e ok 5 fois, gardé)."""
        d = self._dix()
        self.assertEqual(d["pools_bis"], {"calme": ["a", "b", "d"]})
        self.assertEqual([r[:5] for r in d["retraits_bis"]], [("calme", "uc", "c", 0, 10), ("calme", "ue", "e", 4, 10)])

    def test_pool_d1bis_sans_seuil(self):
        """Seuil non posé : seul c (ok = 0, D1) est retiré. Mutation MC-8 : seuil appliqué quel que soit le drapeau."""
        self.assertEqual(self._dix(seuil=False)["pools_bis"], {"calme": ["a", "b", "d", "e"]})

    def test_pool_d1bis_refuse_une_classe_divergente(self):
        """Classe journalisée d'une unité différente de parametres.json : refus. Mutation MC-9 : contrôle retiré."""
        with self.assertRaises(ValueError):
            self._dix(classes={"a": "autre", **{f: "place" for f in "bcdef"}})

    def _vingt(self):
        """10 fenêtres calmes (vendredi 23:50-23:59), 10 de stress ; plage [23:52 ; 23:53] ; n fixe 18 ; e mort en
        stress : n = 8 et 8, pool S2 de stress a-d."""
        ws = [fx.VEN + 86400 - 600 + 60 * i for i in range(20)]
        fx.journaux(self.d, ws, lambda i, f: "panne_transport" if (f == "e" and i >= 10) or (f in "ab" and i % 3 == 0)
                    else "ok", list("abcde"))
        p = fx.prm_fixture(list("abcde"), {}, "-", ws[0], 18, [(ws[2], ws[3])])
        return commun.charger(self.d, p), ws

    def test_charger_egal_au_point_d_entree_scelle(self):
        """Mutation MC-10 : plages non passées au filtre de lecture."""
        d, ws = self._vingt()
        c, j = (os.path.join(self.d, n) for n in ("control.jsonl", "journal.jsonl"))
        self.assertEqual(d["base"], fx.r1.recompute_from_journal(c, j, [(ws[2], ws[3])], {"t0": ws[0], "n_fixe": 18}))
        self.assertEqual((d["base"]["strates"]["calme"]["n"], d["base"]["strates"]["stress"]["n"]), (8, 8))
        self.assertEqual(d["pools_s2"]["stress"], ["a", "b", "c", "d"])

    def test_classer_egal_a_compute_r1(self):
        """K, écarts par source et flux classés de chaque strate égaux à ceux de compute_r1. Mutation MC-11 : pool de
        la première strate appliqué à toutes."""
        d, _ = self._vingt()
        par = commun.classer(d, d["pools_s2"])
        for st, b in d["base"]["strates"].items():
            ecarts = [{f for f, e in cls.items() if e in fx.r1.ECARTS} for _ws, cls, _rep in par[st]]
            self.assertEqual(sum(len(e) >= 2 for e in ecarts), b["K"])
            self.assertEqual({f: sum(f in e for e in ecarts) for f in d["pools_s2"][st]},
                             {f: v["ecart"] for f, v in b["per_source"].items()})
            self.assertEqual({tuple(sorted(cls)) for _ws, cls, _rep in par[st]}, {tuple(sorted(d["pools_s2"][st]))})

    def test_executer_fail_closed_etiquette_en_tete(self):
        """3 fenêtres calmes : a et b en panne à la 1re, a seule à la 2e : n = 3, K = 1, P̂_more = 2/9 (à la main).
        Égal : code 0, ligne d'analyse ; K du rendu à 2 : code 1, aucune ligne d'analyse. Mutation MC-12 : analyse
        écrite quel que soit le contrôle."""
        ws = [fx.VEN + 60 * i for i in range(3)]
        fx.journaux(self.d, ws, lambda i, f: "panne_transport" if (i == 0 and f in "ab") or (i == 1 and f == "a")
                    else "ok", list("abcde"))
        for k, code in ((1, 0), (2, 1)):
            r = fx.rendu(os.path.join(self.d, f"r{k}.out"), {"calme": (3, k, DEUX_NEUVIEMES)})
            p = fx.ecrire_prm(os.path.join(self.d, f"p{k}.json"), fx.prm_fixture(
                list("abcde"), {"calme": (3, k, DEUX_NEUVIEMES)}, commun.sha256(r), ws[0], 3))
            s = os.path.join(self.d, f"s{k}.txt")
            rc = commun.executer("essai", "item", analyse, ["--journaux", self.d, "--harnais", fx.HARNAIS, "--sortie", s,
                                                           "--parametres", p, "--rendu", r])
            with open(s, encoding="utf-8") as f:
                lignes = f.read().split(fx.NL)
            self.assertEqual((rc, lignes[0], "ANALYSE" in lignes), (code, commun.ETIQUETTE, code == 0))
            self.assertEqual(any("ÉCART" in x for x in lignes), code == 1)


if __name__ == "__main__":
    unittest.main()
