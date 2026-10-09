"""Relevé de cadence des agrégateurs (AVIS Q-CA-11 modifiée) contre le serveur local : horodatages distincts et leurs
intervalles, écrits à la main ; aucun prix dans la sortie ; script hors de lancer.sh. Chaque test nomme sa mutation."""
import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest

import acquerir
import cadence
import socle
import tests
from tests.serveur import Serveur

P = socle.lire()
CG = "/cg?ids=bitcoin,ethereum,usd-coin,tether&vs_currencies=usd&include_last_updated_at=true"
DL = "/dl/coingecko:bitcoin,coingecko:ethereum,coingecko:usd-coin,coingecko:tether"
SUITES = {"BTC": [100, 160, 160, 220], "ETH": [100, 100, 400, 400], "USDC": [50, 50, 50, 50], "USDT": [0, 10, 30, 100]}


class TestCadence(unittest.TestCase):
    def test_releve(self):
        """Quatre lectures, pas de 60 s (trois attentes) : BTC 100, 160, 160, 220 : intervalles 60, 60 ; ETH 100, 400 :
        300, plus lent que BTC ; USDT 0, 10, 30, 100 : médiane 20, P90 70 ; USDC un seul horodatage : aucun intervalle,
        et en chaîne chez CoinGecko : omis ; une réponse DefiLlama illisible : un échec ; prix 12345.678 jamais écrit ;
        étiquette en tête. Mutations : horodatage répété compté ; prix gardé ; échec compté comme horodatage ;
        comparaison à BTC inversée ; P90 remplacé par la médiane ; horodatage non entier admis."""
        d = tempfile.mkdtemp(prefix="ca_cad_")
        self.addCleanup(shutil.rmtree, d, True)
        prm, ids, k = json.loads(json.dumps(P)), P["cadence"]["coingecko"]["ids"], [0]
        with Serveur({}) as s:
            prm["cadence"].update(lectures=4)
            prm["cadence"]["coingecko"]["url"] = s.base + "/cg?ids={ids}&{options}"
            prm["cadence"]["defillama"]["url"] = s.base + "/dl/{ids}"

            def servir():
                s.fichiers[CG] = json.dumps({ids[a]: {"usd": 12345.678, "last_updated_at": str(v[k[0]]) if a == "USDC"
                                                      else v[k[0]]} for a, v in SUITES.items()}).encode()
                s.fichiers[DL] = b"{" if k[0] == 2 else json.dumps({"coins": {"coingecko:" + ids[a]: {
                    "price": 12345.678, "timestamp": v[k[0]], "confidence": 0.99} for a, v in SUITES.items()}}).encode()
            pauses = []
            dormir, acquerir.DORMIR = acquerir.DORMIR, lambda x: (pauses.append(x), k.__setitem__(0, k[0] + 1),
                                                                  servir())
            self.addCleanup(setattr, acquerir, "DORMIR", dormir)
            servir()
            argv = ["--sortie", os.path.join(d, "c.txt"), "--parametres", self.prm(d, prm)]
            self.assertEqual(cadence.main(argv, {}), 0)
        with open(os.path.join(d, "c.txt"), encoding="utf-8") as f:
            texte = f.read()
        lignes = texte.split(socle.NL)
        self.assertEqual((lignes[0], pauses, "12345" in texte), (socle.ETIQUETTE, [60, 60, 60], False))
        self.assertIn("lectures en échec : 1", lignes[1])
        tete = " intervalles ; minimum, médiane, P90, maximum (s) : "
        self.assertIn("coingecko BTC : 2" + tete + "60, 60, 60, 60 ; 60 60", lignes)
        self.assertIn("coingecko ETH : 1" + tete + "300, 300, 300, 300 ; 300", lignes)
        self.assertIn("defillama USDC : 0" + tete + "-, -, -, - ; ", lignes)
        self.assertIn("coingecko USDT : 3" + tete + "10, 20, 70, 70 ; 10 20 70", lignes)
        self.assertFalse([x for x in lignes if x.startswith("coingecko USDC")])     # horodatage en chaîne : omis
        self.assertIn("defillama ETH plus lent que BTC (médiane) : oui", lignes)
        self.assertIn("coingecko USDT plus lent que BTC (médiane) : non", lignes)

    def prm(self, d, prm):
        with open(os.path.join(d, "p.json"), "w", encoding="utf-8") as f:
            json.dump(prm, f)
        return f.name

    def test_cli_hors_lanceur(self):
        """Variable posée : code 3, sur des paramètres locaux (C-3 : sans la garde, le relevé irait au serveur local,
        jamais à un hôte réel : tests.TENTATIVES inchangé) ; arguments faux : code 2 ; lancer.sh ne nomme pas cadence.py
        (relevé séparé). Mutations : garde retirée ; relevé greffé au lanceur."""
        d, err, avant = tempfile.mkdtemp(prefix="ca_cad_"), io.StringIO(), list(tests.TENTATIVES)
        self.addCleanup(shutil.rmtree, d, True)
        prm = json.loads(json.dumps(P))
        with Serveur({}) as s, contextlib.redirect_stderr(err):
            prm["cadence"].update(lectures=1)
            prm["reseau"].update(essais=1)
            for nom in cadence.AGREGATEURS:
                prm["cadence"][nom]["url"] = s.base + "/{ids}"
            argv = ["--sortie", os.path.join(d, "c.txt"), "--parametres", self.prm(d, prm)]
            codes = [cadence.main(argv, {"SHOGEN_S2_CAMPAGNE_CONTROL": "x"}), cadence.main(["--x"], {})]
        self.assertEqual(tests.TENTATIVES, avant)
        self.assertEqual((codes, [x[:14] for x in err.getvalue().split(socle.NL)]),
                         ([3, 2], ["REFUS CA/varia", "REFUS CA/usage", ""]))
        with open(os.path.join(os.path.dirname(socle.PARAMETRES), "lancer.sh"), encoding="utf-8") as f:
            self.assertNotIn("cadence", f.read())

    def test_corps_hors_forme(self):
        """C-10 : corps [] ou "x" (liste, chaîne) chez les deux agrégateurs : deux lectures comptées en échec, aucune
        trace ; BTC différent d'un agrégateur à l'autre : chacun comparé à son propre BTC (defillama ETH, médiane 150,
        sous son BTC 200 : non ; coingecko ETH, 150 sur 100 : oui). Mutations : TypeError ou AttributeError non captée
        (G28) ; BTC de l'autre agrégateur (G10)."""
        prm = json.loads(json.dumps(P))
        prm["cadence"].update(lectures=1)
        with Serveur({}) as s:
            for nom in cadence.AGREGATEURS:
                prm["cadence"][nom]["url"] = s.base + "/{ids}"
            vus = []
            for corps in (b"[]", b'"x"'):
                s.defaut = corps
                try:
                    vus.append(cadence.releve(prm))
                except Exception as e:                      # une trace est le défaut cherché : rendue en assertion
                    vus.append(type(e).__name__)
        self.assertEqual(vus, [({}, 2), ({}, 2)])
        ts = {("coingecko", "BTC"): [0, 100, 200], ("defillama", "BTC"): [0, 200, 400]}
        lignes = cadence.lignes(P, ts | {(n, "ETH"): [0, 150, 300] for n in cadence.AGREGATEURS}, 0)
        self.assertEqual([x for x in lignes if "plus lent" in x], ["coingecko ETH plus lent que BTC (médiane) : oui",
                                                                  "defillama ETH plus lent que BTC (médiane) : non"])


if __name__ == "__main__":
    unittest.main()
