"""CB-18c : configurations scellées, descripteur et câblage du collecteur (E-C-02, E-C-23 ; SHOGEN-S2BIS-PLAN-
CABLAGE-1 pour les sondes). Configurations de test écrites ici, sha256 attendus calculés par hashlib sur les octets
écrits."""
import hashlib
import json
import os
import sys
import tempfile
import unittest

from shogen_s2bis.collecte import entree
from shogen_s2bis.collecte.lecture import S

COMMIT = "0123456789abcdef0123456789abcdef01234567"


def refus(appel):
    """Texte de l'exception que lève `appel`, None sans exception."""
    try:
        appel()
    except Exception as e:                                          # refus nommé, ou OSError d'un fichier absent
        return str(e)
    return None


def configurations(port):
    """(formes, sante, descripteur) de test ; w = 1 s, δ = 0,6 s, délai 0,3 s, marge 0,2 s."""
    forme = {"hote": "127.0.0.1", "port": port, "methode": "GET", "corps": "", "espace": False}
    return ({"w": 1, "delta": 6 * S // 10, "delai": 3 * S // 10, "marge": S // 5, "places": 4,
             "formes": [{**forme, "nom": "a", "chemin": "/a"}, {**forme, "nom": "b", "chemin": "/b"}]},
            {"commande": [sys.executable, "-c", "print('suivi')"], "temoins": ["127.0.9.1", "127.0.9.2", "127.0.9.3"],
             "noms": ["a.example.", "b.example."], "delai": S // 10},
            {"observateur": "O1", "fournisseur": "essai", "region": "boucle-locale", "asn": 64512,
             "resolveur": "127.0.9.53", "config_resolveur": "resolv.conf", "versions": ["python3 essai"],
             "empreinte": "e" * 64})


class Entree(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.journal = d.name, os.path.join(d.name, "journal")
        os.mkdir(self.journal)

    def ecrire(self, formes, sante, descripteur):
        """Écrit les trois fichiers ; rend leurs sha256 (sur les octets écrits) et leurs chemins."""
        sha, chemins = {}, {}
        for nom, donnees in (("formes", formes), ("sante", sante), ("descripteur", descripteur)):
            octets = json.dumps(donnees).encode()
            with open(os.path.join(self.d, nom + ".json"), "wb") as f:
                f.write(octets)
            sha[nom], chemins[nom] = hashlib.sha256(octets).hexdigest(), f.name
        return sha, chemins

    def test_refus_nommes_de_configuration(self):                         # E-C-02
        """Configuration incomplète ou incohérente (une règle nommée par cas), commit illisible : refus nommé,
        RefusConfig ou RefusBoucle, au chargement ; fichier absent : OSError."""
        f, s, d = configurations(1)
        x, y = f["formes"]
        cas = [("CONFIG/champ-absent", {**f, "places": None}, s, d),
               ("CONFIG/incoherent : w-divise", {**f, "w": 7}, s, d),
               ("CONFIG/incoherent : marge-delta", {**f, "marge": 6 * S // 10}, s, d),
               ("CONFIG/incoherent : budget", {**f, "delai": S}, s, d),
               ("CONFIG/incoherent : noms-uniques", {**f, "formes": [x, x]}, s, d),
               ("CONFIG/incoherent : methode-corps", {**f, "formes": [x, {**y, "methode": "POST"}]}, s, d),
               ("CONFIG/incoherent : espace-par-hote", {**f, "formes": [x, {**y, "espace": True}]}, s, d),
               ("CONFIG/incoherent : empreinte-hex", f, s, {**d, "empreinte": "E" * 64}),
               ("CONFIG/incoherent : temoins-ipv4", f, {**s, "temoins": ["127.0.9.01"]}, d),
               ("CONFIG/incoherent : noms-dns", f, {**s, "noms": ["a..b"]}, d),
               ("CONFIG/incoherent : resolveur-ipv4", f, s, {**d, "resolveur": "localhost"}),
               ("CONFIG/incoherent : delai-sondes", f, {**s, "delai": S // 2}, d),
               ("BOUCLE/hote", {**f, "formes": [{**x, "nom": str(k)} for k in range(6)]}, s, d)]
        for attendu, *fichiers in cas:
            fichiers[0] = {k: v for k, v in fichiers[0].items() if v is not None}
            with self.subTest(attendu=attendu):
                self.assertTrue(str(refus(lambda: entree.configurer(self.ecrire(*fichiers)[1], COMMIT))).startswith(
                    attendu))
        chemins = self.ecrire(f, s, d)[1]
        self.assertEqual((refus(lambda: entree.configurer(chemins, "abc")), refus(lambda: entree.configurer(
            {**chemins, "formes": "absent.json"}, COMMIT))[:9]), ("CONFIG/commit : abc", "[Errno 2]"))
        self.assertEqual(sorted(entree.configurer(chemins, COMMIT)), ["descripteur", "formes", "sante"])

    def test_cablage_des_sondes_et_de_la_boucle(self):                  # SHOGEN-S2BIS-PLAN-CABLAGE-1
        """Les sondes reçoivent la commande, les témoins, les noms et le délai de `sante.json`, le résolveur et sa
        configuration du descripteur, le dossier du journal ; la boucle, ses paramètres de `formes.json` ; le plan, une
        lecture par forme."""
        f, s, d = configurations(1)
        jl, b = entree.construire(f, s, d, self.journal)
        o = b.sondes
        self.assertEqual((o.commande, o.temoins, o.noms, o.delai, o.resolveur, o.resolv, o.dossier),
                         (s["commande"], s["temoins"], s["noms"], S // 10, "127.0.9.53", "resolv.conf", self.journal))
        self.assertEqual((b.w, b.delta, b.marge, b.journal, jl.dossier, jl.prefixe, jl.w, sorted(b.lectures), b.plan),
                         (1, 6 * S // 10, S // 5, jl, self.journal, "pool", 1, ["a", "b"], [(0, "a"), (0, "b")]))
