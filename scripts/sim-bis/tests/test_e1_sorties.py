"""E1 câblée, lots et sorties (SB-11o ; E-S-05, E-S-38, E-S-45, E-S-48) : attendus recalculés ici depuis des appels
indépendants de replication_e1, ou écrits à la main ; chaque test nomme les mutations qui le rougissent."""
import functools
import hashlib
import json
import os
import shutil
import tempfile
import unittest
from fractions import Fraction

import calib_fiv
import calibration
import commun
import e1
import executer

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
E1R = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5], tau_D=[60], replications=2,
                        cellule="E1-essai"))


@functools.lru_cache(maxsize=None)
def cal_e1():
    return calib_fiv.calendrier_e1(PRM, environ={})


def dossier(test):
    d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
    test.addCleanup(shutil.rmtree, d)
    return d


class TestCalculerE1(unittest.TestCase):
    def test_lots_par_point_et_reprise(self):
        """C0 et les deux points de la grille réduite, deux réplications, plan d'une réplication par lot (coût 10,
        borne 10) : six lots « <cellule>.<a>-<b>.lot », moyennes de chaque point égales à moyennes_point des
        enregistrements de replication_e1 recalculés ici et passés en JSON ; lot (1/10, 5, 60) [1, 2) perdu, E1
        relancée : ce seul lot refait, de mêmes octets (sha256 égal), moyennes inchangées ; lots présents relus, jamais
        récrits. Mutations M-11O-01 (C0 omis), M-11O-02 (lot présent refait : SORTIE/existe), M-11O-03 (moyennes du
        point précédent), M-11O-04 (plan sur la borne par défaut), M-11O-05 (réplications lues à R − 1)."""
        d, cal = dossier(self), cal_e1()
        moy, journal = e1.calculer_e1(E1R, EP, cal, d, 1, 10, ["e"], 10)
        noms = [os.path.basename(c) for c, _h in journal]
        self.assertEqual(noms, [f"E1-essai-{x}.00000{a}-00000{a + 1}.lot" for x in ("C0-v2", "1_100-5-60", "1_10-5-60")
                                for a in (0, 1)])
        for p in [None] + calib_fiv.grille(E1R):
            recs = [executer.jsonable(e1.replication_e1(E1R, EP, cal, p, i)) for i in (0, 1)]
            self.assertEqual(moy[p], e1.moyennes_point(json.loads(json.dumps(recs)), E1R["calibration"]), p)
        perdu = os.path.join(d, noms[5])
        os.unlink(perdu)
        moy2, journal2 = e1.calculer_e1(E1R, EP, cal, d, 1, 10, ["e"], 10)
        self.assertEqual(journal2, [journal[5]])
        self.assertEqual(moy2, moy)


class TestEcrireE1(unittest.TestCase):
    def test_e_s_48(self):
        """E-S-48 et E-S-05 : calibration_e1.json (JSON canonique) et calibration_e1.txt (lignes, première ligne
        l'étiquette) écrits si tous les oracles passent, sha256 des octets écrits rendus ; aucun oracle, un oracle en
        échec : SORTIE/oracle ; étiquette absente en tête du texte ou de l'entête : SORTIE/etiquette ; un des deux
        fichiers présent : SORTIE/existe, l'autre jamais écrit (à la main). Mutations M-11O-06 (oracles non lus),
        M-11O-07 (liste vide admise), M-11O-08 (étiquette non contrôlée), M-11O-09 (texte écrit avant le contrôle de
        présence du JSON), M-11O-10 (JSON non canonique), M-11O-11 (sha256 du JSON rendu pour le texte)."""
        et, ok = commun.ETIQUETTE, {"suite sim-bis conforme": True, "E-S-39 r1": True}
        obj, lignes = {"entete": [et, "sha256 a b"], "x": [Fraction(1, 3)]}, [et, "sha256 a b", "ligne"]
        for oracles in ({}, dict(ok, **{"E-S-39 r1": False})):
            d = dossier(self)
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, obj, lignes, oracles)
            self.assertEqual((c.exception.code, os.listdir(d)), ("SORTIE/oracle", []))
        for o, li in ((obj, ["autre"] + lignes[1:]), (dict(obj, entete=["autre"]), lignes)):
            d = dossier(self)
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, o, li, ok)
            self.assertEqual((c.exception.code, os.listdir(d)), ("SORTIE/etiquette", []))
        d = dossier(self)
        r = e1.ecrire_e1(d, obj, lignes, ok)
        j, t = (os.path.join(d, "calibration_e1." + x) for x in ("json", "txt"))
        with open(j, "rb") as f, open(t, "rb") as g:
            bj, bt = f.read(), g.read()
        self.assertEqual(bj, ('{"entete":["' + et + '","sha256 a b"],"x":["1/3"]}' + commun.NL).encode("utf-8"))
        self.assertEqual(bt, (commun.NL.join(lignes) + commun.NL).encode("utf-8"))
        self.assertEqual(r, [(j, hashlib.sha256(bj).hexdigest()), (t, hashlib.sha256(bt).hexdigest())])
        for x in ("json", "txt"):
            d = dossier(self)
            with open(os.path.join(d, "calibration_e1." + x), "w", encoding="utf-8") as f:
                f.write("déjà")
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, obj, lignes, ok)
            self.assertEqual((c.exception.code, sorted(os.listdir(d))), ("SORTIE/existe", ["calibration_e1." + x]))


if __name__ == "__main__":
    unittest.main()
