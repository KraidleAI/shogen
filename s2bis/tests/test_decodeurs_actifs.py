"""CB-7a (SHOGEN-S2BIS-DECODEURS-TYPES-1) : un conteneur remplacé ne rend jamais une autre valeur, à chaque décodeur
qui a une fixture (BTC compris)."""
import json
import os
import unittest
from decimal import Decimal

from shogen_s2bis.collecte import decodeurs

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BTC = os.path.join(RACINE, "tests", "fixtures", "btc")
PANNE = ("panne_decode", None)


def lire(*chemin):
    with open(os.path.join(*chemin), "rb") as f:
        return f.read()


def fixtures():
    """{décodeur : octets} : fixtures BTC (`btc/<flux>.bin`)."""
    return {n[:-4] + "_btc": lire(BTC, n) for n in os.listdir(BTC)}


def texte(x):
    """JSON compact, nombres écrits par leur texte Decimal (comme lus)."""
    if type(x) is dict:
        return "{" + ",".join(json.dumps(k) + ":" + texte(v) for k, v in x.items()) + "}"
    if type(x) is list:
        return "[" + ",".join(map(texte, x)) + "]"
    return str(x) if type(x) is Decimal else json.dumps(x)


def remplacements(x):
    """Variantes de x où un conteneur (racine comprise) est remplacé par son texte JSON, par l'autre sorte de
    conteneur (objet en liste de ses valeurs, liste en objet) ou par l'un de ses enfants scalaires (Kraken `c` en
    « 64025.00 »)."""
    if type(x) not in (dict, list):
        return
    enfants = list(x.values()) if type(x) is dict else x
    yield texte(x)
    yield enfants if type(x) is dict else {str(i): v for i, v in enumerate(x)}
    yield from (v for v in enfants if type(v) not in (dict, list))
    for k in (x if type(x) is dict else range(len(x))):
        for v in remplacements(x[k]):
            yield {**x, k: v} if type(x) is dict else x[:k] + [v] + x[k + 1:]


class Types(unittest.TestCase):                                   # SHOGEN-S2BIS-DECODEURS-TYPES-1
    def test_conteneur_remplace_jamais_une_autre_valeur(self):
        """Chaque conteneur de chaque fixture remplacé (texte, autre conteneur, enfant scalaire) : `panne_decode` ou la
        même valeur, jamais une autre (S2 : Kraken `c` en chaîne rendait « 6 »)."""
        for nom, corps in sorted(fixtures().items()):
            base = json.loads(corps, parse_float=Decimal, parse_int=Decimal)
            attendu = decodeurs.decoder(nom, texte(base).encode())
            self.assertEqual(attendu[0], "ok", nom)
            with self.subTest(nom=nom):
                self.assertEqual([v for v in map(texte, remplacements(base)) if decodeurs.decoder(nom, v.encode()) not
                                  in (PANNE, attendu)], [])
        self.assertEqual(decodeurs.decoder("kraken_btc", b'{"error":[],"result":{"XXBTZUSD":{"c":"64025.00"}}}'),
                         PANNE)


if __name__ == "__main__":
    unittest.main()
