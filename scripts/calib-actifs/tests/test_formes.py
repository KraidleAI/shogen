"""Formes des API (SHOGEN-CALIB-FORMES-API-1 ; DECISION pts 2 et 3 ; DETTES-T2) : pages écrites à la main, chargées par
bougies.charger ; outils communs des tests de formes : marché synthétique, vérité, écart minute pour minute ; un refus
ou une exception devient une valeur comparée (rouge d'assertion). 1775001600 = 2026-04-01 00:00 UTC (date -u -d)."""
import json
import os
import unittest
from decimal import Decimal

import bougies
import socle
from tests.test_acquerir import local

NL, W0 = chr(10), 1775001600


def essai(f):
    try:
        return f()
    except socle.Refus as e:
        return str(e)
    except Exception as e:
        return type(e).__name__


def marche(fen, k=0, marge=20):
    """{t : (clôture, volume)} en chaînes, de `marge` minutes avant la fenêtre à `marge` après ; clôture distincte par
    minute et par place (rang k) ; sans échange (volume « 0 ») aux minutes de rang i % 7 == 2 depuis le début."""
    n = (fen["fin"] - fen["debut"]) // 60
    return {fen["debut"] + 60 * i: (f"{1000 + 10 * k + i // 1000}.{i % 1000:03d}", "0" if i % 7 == 2 else f"{i % 3}.5")
            for i in range(-marge, n + marge)}


def verite(m, fen, absentes):
    """Série attendue : minutes sans échange absentes (Coinbase, Bitfinex) ou présentes inactives (Bitstamp, OKX)."""
    return {t: (Decimal(c), v != "0") for t, (c, v) in m.items()
            if fen["debut"] <= t < fen["fin"] and not (absentes and v == "0")}


def ecart(obtenu, attendu):
    """(manquantes, en trop, différentes), triées."""
    return (sorted(set(attendu) - set(obtenu)), sorted(set(obtenu) - set(attendu)),
            sorted(t for t in set(attendu) & set(obtenu) if attendu[t] != obtenu[t]))


class TestFormes(unittest.TestCase):
    def test_doublons_et_decoupage(self):
        """DECISION pts 2 et 3, pages de Coinbase écrites à la main (pas 6, chevauchement 1 ; pages en 0, 4, 8, 12 ;
        fenêtres de filtre [-1 ; 5), [3 ; 9), [7 ; 13), [11 ; 14)) : minute de chevauchement servie deux fois,
        identique : gardée une fois ; minute 6 dans la page 0 (clôture altérée) et minute 14 dans la dernière :
        écartées ; minute 8 à clôture ou volume différent dans les pages 4 et 8, minute 3 différente dans les pages 0 et
        4 (chevauchement de début) : refus nommé ; double dans une page : refus « minute en double » ; page hors
        découpage ou absente : refus. Mutations : doublon identique refusé ; contradictoire admis ; volume non comparé ;
        double dans une page admis ; filtre à la fenêtre ou depuis le début de page ; plan libre."""
        fen = {"debut": W0, "fin": W0 + 840}
        m, rep = marche(fen), os.path.join("principale", "coinbase", "ETH")
        base = {f"page-{W0 + 60 * a}.json": [W0 + 60 * i for i in range(a, b)]
                for a, b in ((0, 5), (4, 9), (8, 13), (12, 15))}
        base[f"page-{W0}.json"].append(W0 + 360)
        altere, p8, c8, v8 = {(f"page-{W0}.json", W0 + 360): ("9.99", "1")}, f"page-{W0 + 480}.json", *m[W0 + 480]
        refus, p4 = "REFUS CA/format : {} ; actif ETH ; place coinbase", f"page-{W0 + 240}.json"
        vd = refus.format("minute en double aux valeurs différentes")
        plan = refus.format("pages différentes du découpage de la fenêtre")
        cas = [({}, {}, ([], [], [])), ({}, {(p8, W0 + 480): ("9.99", v8)}, vd), ({}, {(p8, W0 + 480): (c8, "7")}, vd),
               ({p4: base[p4] + [W0 + 300]}, {}, refus.format("minute en double")),
               ({p4: [W0 + 180] + base[p4]}, {(p4, W0 + 180): ("9.99", "1")}, vd),
               ({f"page-{W0 + 60}.json": [W0 + 60]}, {}, plan), ({p8: None}, {}, plan)]
        for k, (pages, alterees, attendu) in enumerate(cas):
            with self.subTest(cas=k):
                prm, d, _p = local(self, "http://127.0.0.1:9")
                prm["series"]["coinbase"].update(pas=6, chevauchement=1)
                os.makedirs(os.path.join(d, rep))
                for nom, ts in (base | pages).items():
                    if ts is not None:
                        rangs = [[t, 1, 2, 0.5, *(altere | alterees).get((nom, t), m[t])] for t in ts if m[t][1] != "0"]
                        with open(os.path.join(d, rep, nom), "w", encoding="ascii") as f:
                            f.write(json.dumps(rangs).replace('"', ""))
                obtenu = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", fen))
                self.assertEqual(ecart(obtenu, verite(m, fen, True)) if isinstance(obtenu, dict) else obtenu, attendu)


if __name__ == "__main__":
    unittest.main()
