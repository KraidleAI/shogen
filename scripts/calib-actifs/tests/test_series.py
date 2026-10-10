"""Dernier prix connu et âges (T-CA-SER-1), chargement des bruts, oracle de SH §4 (T-CA-ORX-1 ; E-CA-15). Séries et
comptes écrits à la main ; comptes du paramètre relus sur SOURCES-HISTORIQUES §4. Chaque test nomme sa mutation."""
import os
import shutil
import tempfile
import unittest
from decimal import Decimal

import bougies
import socle

T0 = 1775001600
P = socle.lire()


def s(actives, inactives=()):
    """Série synthétique : {T0 + 60·i : (clôture, active)}."""
    return {T0 + 60 * i: (Decimal(c), True) for i, c in actives} | {T0 + 60 * i: (Decimal(99), False)
                                                                     for i in inactives}


class TestSeries(unittest.TestCase):
    def test_dernier_prix(self):
        """T-CA-SER-1 : actives en 1, 2 et 5, clôtures 10, 11 et 14, minute 3 reportée (99) : c = (-, 10, 11, 11, 11,
        14) et âges (-, 0, 0, 1, 2, 0) ; indéfini avant la première active. Mutations M-CA-08 : âge compté depuis le
        début de la fenêtre ; clôture d'une minute non active reprise."""
        c, a = bougies.derniers(s([(1, 10), (2, 11), (5, 14)], [3]), {"debut": T0, "fin": T0 + 360})
        self.assertEqual((c, a), ([None, 10, 11, 11, 11, 14], [None, 0, 0, 1, 2, 0]))

    def test_charger(self):
        """Fichiers d'une (place, actif) lus, .partiel ignoré ; dossier vide : CA/format. Fenêtre de 600 minutes,
        pages de Coinbase du découpage (DETTES-T2 : 298 minutes utiles, en T0, T0 + 17880, T0 + 35760). Mutations :
        .partiel lu ; format de la place ignoré."""
        d = tempfile.mkdtemp(prefix="ca_ch_")
        self.addCleanup(shutil.rmtree, d, True)
        os.makedirs(os.path.join(d, "principale", "coinbase", "ETH"))
        fen = {"debut": T0, "fin": T0 + 36000}
        for nom, t in ((f"page-{T0}.json", T0), (f"page-{T0 + 17880}.json", T0 + 17880),
                       (f"page-{T0 + 35760}.json", T0 + 35760), (f"page-{T0 + 35760}.json.partiel", T0 + 60)):
            with open(os.path.join(d, "principale", "coinbase", "ETH", nom), "w", encoding="ascii") as f:
                f.write(f"[[{t}, 1, 2, 1, 1.5, 3]]")
        self.assertEqual(sorted(bougies.charger(P, d, "principale", "coinbase", "ETH", fen)),
                         [T0, T0 + 17880, T0 + 35760])
        with self.assertRaises(socle.Refus) as r:
            bougies.charger(P, d, "principale", "coinbase", "USDT", P["fenetre"])
        self.assertEqual(r.exception.code, "CA/format")

    def test_oracle(self):
        """T-CA-ORX-1, semaine réduite à 6 minutes : binance actif en 0, 1, 2 ; kraken en 1, 2, 3, 4 ; bitstamp en 2 :
        3 minutes actives pour binance ; à au moins 4, 3, 2 places : 0, 1, 2 minutes. Compte de binance porté à 4 ou
        concurrence (0, 1, 3) : CA/oracle-sh ; bitfinex hors lecture : non applicable. Mutations M-CA-20 : contrôle
        retiré ; seuil de concurrence décalé ; minute inactive comptée."""
        q = socle.json.loads(socle.json.dumps(P))
        q["oracle_sh"] = {"debut": T0, "fin": T0 + 360, "actives": [["USDC", "binance", 3], ["USDC", "bitfinex", 9]],
                          "concurrences": [["USDC", ["binance", "bitstamp", "kraken"], [0, 1, 2]]]}
        series = {("USDC", "binance"): s([(-1, 1), (0, 1), (1, 1), (2, 1), (9, 1)], [3]),  # -1 et 9 : hors semaine
                  ("USDC", "kraken"): s([(i, 1) for i in (1, 2, 3, 4)]),
                  ("USDC", "bitstamp"): s([(2, 1)], [0, 1, 3, 4, 5])}
        try:
            lignes = bougies.oracle_sh(q, series)
        except socle.Refus as e:              # rouge d'assertion sous G07 (minute 9) et X09 (minute -1, R-2)
            lignes = [str(e)]
        self.assertEqual(lignes[0], "oracle de SH §4 : USDC bitfinex non applicable (place hors lecture)")
        trois = ["binance", "bitstamp", "kraken"]
        for cle, valeur in (("actives", [["USDC", "binance", 4]]), ("concurrences", [["USDC", trois, [0, 1, 3]]])):
            r = socle.json.loads(socle.json.dumps(q))
            r["oracle_sh"][cle] = valeur
            with self.assertRaises(socle.Refus) as e:
                bougies.oracle_sh(r, series)
            self.assertEqual(e.exception.code, "CA/oracle-sh")

    def test_comptes_de_sh(self):
        """C-6 : chaque compte du paramètre oracle_sh lié à sa place et à sa colonne (SOURCES-HISTORIQUES l.103-111) :
        concurrences = lignes du tableau dans l'ordre (classe ; jeu de places lu dans sa colonne, « ci-dessus » et
        « sans » compris ; comptes à au moins 4, 3, 2 places) ; actives = phrase « Minutes actives par place », place
        nommée puis son compte. Mutations : compte altéré ; comptes permutés entre places (G29) ; compte pris à une
        autre place (G30)."""
        with open(os.path.join(socle.RACINE, "docs", "adr-0029", "calib", "SOURCES-HISTORIQUES.md"),
                  encoding="utf-8") as f:
            sh = f.read().split(socle.NL)[102:111]
        conc, prec = [], []
        for x in [x.split(" | ") for x in sh if x.startswith("| ") and "/USD" in x]:
            nommees = {p for p in socle.PLACES if p.capitalize() in x[1] or p.upper() in x[1]}
            prec = sorted(set(prec) - nommees if "sans" in x[1] else nommees | set(prec if "ci-dessus" in x[1] else []))
            comptes = [int(c.strip("*| ").split(" (")[0].replace(" ", "")) for c in x[2:5]]
            conc.append([x[0][2:].split("/")[0], prec, comptes])
        self.assertEqual(conc, P["oracle_sh"]["concurrences"])
        phrase = next(x for x in sh if x.startswith("Minutes actives par place"))
        motif = "([A-Z][a-z]+) [*]{0,2}([0-9]+(?: [0-9]{3})*)"             # place, puis compte (espace des milliers)
        lus = {a: {m[0].lower(): int(m[1].replace(" ", "")) for m in socle.re.findall(
            motif, phrase.split(a + "/USD")[1].split("/USD")[0])} for a in socle.F3}
        actives = P["oracle_sh"]["actives"]
        self.assertEqual([[a, p, lus[a].get(p)] for a, p, _n in actives], actives)


if __name__ == "__main__":
    unittest.main()
