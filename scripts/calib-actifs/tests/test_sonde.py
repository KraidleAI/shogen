"""Sonde de première bougie (SHOGEN-CALIB-FORMES-API-1 ; DECISION, ajout daté 22:03:39, C-15 ; lot DETTES-T2) : pour une
place à couverture double, recherche par dichotomie de la première sonde non vide (sondes de ⌊pas/2⌋ créneaux, de
`historique.debut` à fin − ⌊pas/2⌋ minutes) ; T0 = première bougie de cette sonde. Refus CA/avant-historique : requête
de la fenêtre partant moins de pas − ⌊pas/2⌋ + 1 minutes après T0 ; réponse portant une bougie au plus tard en T0 ;
aucune bougie servie. Banc de test_couverture (pas 30, chevauchement 1, fenêtre de 40 minutes ; requête la plus
précoce : double −6, départ −7 ; seuil 16 minutes ; sondes depuis −999)."""
import os
import unittest

import bougies

from tests import test_couverture as tc
from tests.test_couverture import FEN, lecture
from tests.test_formes import essai

REFUS = "REFUS CA/avant-historique : {} ; actif ETH ; place coinbase"


class TestSonde(unittest.TestCase):
    acquis = tc.TestCouverture.acquis                      # banc de test_couverture, classe non importée ici

    def test_avant_historique(self):
        """Plafond de 30 bougies ancré 100 000 minutes avant start, historique depuis −200 : toute réponse porte les 30
        premières bougies de l'historique (−200 à −171), sondes comprises (T0 = −200) : refus. Plafond de 30 créneaux
        ancré de même : toute réponse vide, sondes comprises : refus. Lecture exacte, historique depuis −10 : sondes à
        la main jusqu'à −24, T0 = −10, départ −7 avant −10 + 16 : refus ; depuis −20 (T0 = −20, −7 avant −4 ; admise
        avec un seuil d'une page, 13, ou le seul premier découpage, départ −1) : refus ; depuis −23 : T0 = −23,
        −7 = −23 + 16 : admise, série égale à la vérité ; échanges de −200 à −50 seulement : fenêtre muette admise
        (sondes en recul 25, 10, −20, −80, puis dichotomie : historique trouvé) ; puis sonde ajoutée hors recherche, ou
        effacée (bruts du dernier cas, « −23 ») : refus nommé. R-4 du contre-contrôle cc2 : depuis −22, T0 = −22, −7
        avant −22 + 16 : refus (un seuil d'une minute de moins l'admettrait). R-1 du contre-contrôle cc2 : fenêtre
        décalée de 100 minutes, historique depuis −57, ou plafond de 30 créneaux ancré 100 minutes avant start,
        historique depuis −36 : seule la requête la plus tardive (double 33, [−68 ; −54] ; page 39, [−62 ; −33]) touche
        l'historique, toutes les sondes (25, 10, −20, …, −999 ; portée décalée [x − 100 ; …]) reviennent vides : refus
        (avant R-1 : admise, 40 minutes perdues). Mutations : sonde omise ; seuil strict, d'une page ou sur le seul
        premier découpage ; T0 pris au départ de la sonde ; réponse à T0 admise ; fenêtre vide admise ; fenêtre muette
        refusée ; recul linéaire ; recherche non vérifiée ; fenêtre servie sans sonde non vide admise (R-1) ; seuil
        d'une minute de moins (R-4)."""
        avant = REFUS.format("fenêtre commencée moins d'une page après la première bougie servie")
        cas = [(lecture, "cpt", 100000, -200, 200, REFUS.format("réponse portant la première bougie de l'historique")),
               (lecture, "crenp", 100000, -200, 200, REFUS.format("aucune bougie servie")),
               (lecture, "exact", 0, -10, 200, avant), (lecture, "exact", 0, -20, 200, avant),
               (lecture, "exact", 0, -22, 200, avant),                    # R-4 du contre-contrôle cc2 : bord du seuil
               (lecture, "cren", 100, -57, 200, REFUS.format("bougies servies, aucune sonde non vide")),   # R-1
               (lecture, "crenp", 100, -36, 200, REFUS.format("bougies servies, aucune sonde non vide")),
               (lecture, "exact", 0, -200, -50, ([], [], [])), (lecture, "exact", 0, -23, 200, ([], [], []))]
        for k, (f, mode, g, debut, fin, attendu) in enumerate(cas):
            with self.subTest(cas=k):
                self.assertEqual(self.acquis(FEN, lambda m: f(m, mode, g), pas=30, chevauchement=1, couverture=2,
                                             historique=debut, fin=fin)[2], attendu)
        prm, d = self.bruts
        rep, refus = os.path.join(d, "principale", "coinbase", "ETH"), []
        for nom, ajout in (("sonde-1775001540.json", True), ("sonde-1775001540.json", False),    # −1 : hors recherche
                           ("sonde-1775001180.json", False)):                                     # −7 : de la recherche
            if ajout:
                with open(os.path.join(rep, nom), "w", encoding="ascii") as f:
                    f.write("[]")
            elif os.path.exists(os.path.join(rep, nom)):                                  # absente : code d'avant C-15
                os.remove(os.path.join(rep, nom))
            x = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
            refus.append(x if isinstance(x, str) else "admise")
        self.assertEqual(refus, [f"REFUS CA/format : {x} ; actif ETH ; place coinbase" if x else "admise" for x in (
            "sondes différentes de la recherche", "", "sonde absente ou illisible")])


if __name__ == "__main__":
    unittest.main()
