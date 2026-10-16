"""Temps et valeurs de presg5.py (lot DETTES-T15, DT15-m ; SHOGEN-PRESG5-QUADRATIQUE-1) : `retirer_balises` et
`scinder_crochets` lisent par indices, le fermant cherché dans la seule fenêtre (300 et 30 caractères) ; l'ancienne
lecture recopiait le reste du texte à chaque `<` ou `[` (temps quadratique). Portable : l'outil est trouvé par le chemin
d'import de la suite (importlib.util.find_spec, à côté de garde_commun.py), sans lire le chemin du fichier de test, et
chargé comme un module, dont importlib pose le chemin (le chargeur de DT15-i exécutait l'arbre de l'outil hors de tout
module : NameError ici). Les tests de temps tournent en sous-processus (-X dev -W error -I -B), arrêtés à la borne."""
import importlib.util
import os
import subprocess
import sys
import unittest

BORNE, TAILLE = 20, 8_000_000  # secondes, caractères : la lecture par indices y met moins d'une seconde
ENFANT = """
import importlib.util, sys, time
chemin, fonction, bloc, taille = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
spec = importlib.util.spec_from_file_location("presg5", chemin)
outil = importlib.util.module_from_spec(spec)
spec.loader.exec_module(outil)
page = (bloc * (taille // len(bloc) + 1))[:taille]
debut = time.perf_counter()
sortie = getattr(outil, fonction)(page)
print(f"{time.perf_counter() - debut:.3f} {len(sortie)}")
"""


def chemin_de_l_outil():
    """Chemin de presg5.py, à côté de garde_commun.py dans la racine de la suite (scripts/controle)."""
    outil, frere = importlib.util.find_spec("presg5"), importlib.util.find_spec("garde_commun")
    if outil is None or frere is None or os.path.dirname(outil.origin) != os.path.dirname(frere.origin):
        raise AssertionError("presg5.py introuvable à côté de garde_commun.py dans le chemin d'import de la suite")
    return outil.origin


def charger():
    spec = importlib.util.spec_from_file_location("presg5_dt15m", chemin_de_l_outil())
    outil = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(outil)
    return outil


class Presg5Lineaire(unittest.TestCase):
    def en_temps_borne(self, fonction, bloc):
        try:
            p = subprocess.run([sys.executable, "-X", "dev", "-W", "error", "-I", "-B", "-c", ENFANT,
                                chemin_de_l_outil(), fonction, bloc, str(TAILLE)],
                               capture_output=True, text=True, timeout=BORNE)
        except subprocess.TimeoutExpired:
            self.fail(f"{fonction} : plus de {BORNE} s pour {TAILLE} caractères")
        self.assertEqual((p.returncode, p.stderr), (0, ""))

    def test_balises_en_temps_borne(self):
        """L'ancienne lecture recopiait le reste du texte à chaque balise : plus de 20 s pour 8 000 000 de
        caractères."""
        bloc = '<div class="ligne"><span>prix 1,23 € la part</span><a href="/x">lien</a></div>' + chr(10)
        self.en_temps_borne("retirer_balises", bloc)

    def test_crochets_en_temps_borne(self):
        """Même recopie à chaque crochet ouvrant dans `scinder_crochets`."""
        self.en_temps_borne("scinder_crochets", "the text [s] is [sic] cited ")

    def test_valeurs_de_reference(self):
        """Valeurs écrites à la main, vraies sur l'ancienne lecture comme sur la nouvelle : une balise va d'un chevron
        ouvrant au premier fermant qui le suit, à 300 caractères au plus ; une insertion, d'un crochet ouvrant au
        premier fermant, à 30 au plus ; au-delà, le chevron ou le crochet reste au texte."""
        outil = charger()
        cas_balises = [("a<b>c", "ac"), ("a<b c", "a<b c"), ("<" + "x" * 300 + ">z", "z"),
                       ("<" + "x" * 301 + ">z", "<" + "x" * 301 + ">z"), ("<<b>", ""), ("x<>y", "xy"),
                       ("é<p>€</p>", "é€")]
        for entree, attendu in cas_balises:
            self.assertEqual(outil.retirer_balises(entree), attendu, entree[:20])
        cas_crochets = [("a[s]b", "a…b"), ("[" + "y" * 30 + "]", "…"), ("[" + "y" * 31 + "]", "[" + "y" * 31 + "]"),
                        ("a[b", "a[b"), ("[[s]", "…")]
        for entree, attendu in cas_crochets:
            self.assertEqual(outil.scinder_crochets(entree), attendu, entree[:20])


if __name__ == "__main__":
    unittest.main()
