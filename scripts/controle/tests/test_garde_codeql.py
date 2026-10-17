"""Cas du correctif CQ-1 (alertes CodeQL de la PR n° 12 sur .claude/hooks/garde_faits.py : py/redos sur NOM_PROPRE,
py/incomplete-url-substring-sanitization sur la lecture d'une commande curl vers la forge). Le crochet est chargé par son
chemin, comme acte_shell.py l'est par lui : rien n'est écrit, aucun journal n'est lu."""
import importlib.util
import itertools
import os
import re
import time
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")


def charger():
    spec = importlib.util.spec_from_file_location("garde_faits_cq", GARDE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CasCodeql(unittest.TestCase):
    # Référence : le langage de l'ancien motif, écrit sans ambiguïté (alerte CodeQL n° 5, py/redos, sur l'ancienne forme
    # « (?:[A-Z][A-Za-z0-9]*)+ », dont la répétition se découpait de plusieurs façons) : une majuscule suivie de
    # minuscules ou chiffres, puis une majuscule et toute suite alphanumérique, reconnaît exactement les mêmes mots, car
    # le premier groupe répété absorbe tous les suivants ; les deux autres branches sont inchangées.
    ANCIEN = re.compile(r"(?<![\w@./-])([A-Z][a-z0-9]+[A-Z][A-Za-z0-9]*|[A-Z]{3,}[0-9]*|[A-ZÀ-Ý][a-zà-ÿ]{2,})"
                        r"(?![\w-])")

    def test_nom_propre_temps_borne(self):
        """py/redos : « A0A », vingt-six « A » puis un tiret (le regard avant échoue, le moteur revient en arrière) :
        moins d'une seconde ; l'ancien motif double son temps à chaque « A » (0,45 s à 22, mesuré) et dépasse."""
        g = charger()
        debut = time.perf_counter()
        g.NOM_PROPRE.search("A0A" + "A" * 26 + "-")
        self.assertLess(time.perf_counter() - debut, 1.0)

    def test_nom_propre_memes_mots(self):
        """Le motif neuf reconnaît les mêmes mots que l'ancien : toutes les chaînes de longueur 1 à 6 sur un alphabet de
        six signes (deux majuscules, une minuscule, un chiffre, une espace), et onze noms réels du JOURNAL."""
        g = charger()
        for n in range(1, 7):
            for t in itertools.product("AaB0Z ", repeat=n):
                s = "".join(t)
                self.assertEqual([m.group() for m in self.ANCIEN.finditer(s)],
                                 [m.group() for m in g.NOM_PROPRE.finditer(s)], s)
        for w in ("CoinGecko", "GitHub", "ReadNotifications", "CoinGECKO", "SHA256SUMS", "McDonald", "PDFReader",
                  "Monitor", "INT-25", "B.102", "x CoinGecko, GitHub."):
            self.assertEqual([m.group() for m in self.ANCIEN.finditer(w)],
                             [m.group() for m in g.NOM_PROPRE.finditer(w)], w)

    def test_curl_hote_de_la_forge(self):
        """py/incomplete-url-substring-sanitization : seule une URL dont l'hôte est api.github.com fait une lecture de
        la forge ; un autre hôte dont le chemin, le sous-domaine ou la requête porte ces mots n'en fait pas une."""
        g = charger()
        oui = ("curl -s https://api.github.com/repos/o/r/actions/runs", "curl -H 'A: b' https://api.github.com:443/x",
               "curl http://api.github.com/x", "curl HTTPS://api.github.com/x", "curl api.github.com/repos/o/r",
               "curl https://api.github.com./x", "U=https://api.github.com/repos/o/r; curl \"$U/issues\"",
               "curl 'http://[' https://evil.example/")
        non = ("curl https://evil.example/api.github.com/x", "curl https://api.github.com.evil.example/x",
               "curl https://evil.example/?u=api.github.com", "curl https://notapi.github.com/x",
               "curl -d x=api.github.com https://evil.example/", "curl https://github.com/o/r",
               "U=https://evil.example/r; curl \"$U/x\"", "U=https://notapi.github.com/r; curl \"$U/x\"")
        for c in oui:
            self.assertTrue(g.faits_de_la_commande(c, RACINE)["forge"], c)
        for c in non:
            self.assertFalse(g.faits_de_la_commande(c, RACINE)["forge"], c)


if __name__ == "__main__":
    unittest.main()
