"""Loi des pauses sur le masque (SB-11m ; point (6) de l'ajout daté du G0 du 2026-10-05 15:05:43 UTC) : attendus
écrits à la main ; chaque test nomme les mutations qui le rougissent."""
import unittest

import e1


def bits(*js):
    return sum(1 << j for j in js)


class TestPauses(unittest.TestCase):
    def test_definitions_d_ep(self):
        """Positions présentes 0-3, 5-9, 12-13 ; d = 1 en 1, 2, 4 (absente), 6, 9 : épisodes (1-2) et (6) complets,
        (9) censuré à la fin ; pauses (0), (3), (5) de bord, (7-8) complète, segment 12-13 sans épisode ; d = 0 sur un
        segment : une pause de bord, segment sans épisode ; d = m : un épisode censuré, aucune pause (à la main).
        Mutations M-11M-01 (censure au début sans la position 0), M-11M-02 (pause complète à une censure),
        M-11M-03 (segment sans épisode à une censure), M-11M-04 (d hors des positions présentes)."""
        m = bits(0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 13)
        self.assertEqual(e1.pauses(m, bits(1, 2, 4, 6, 9)),
                         {"completes": {2: 1}, "bord": {1: 3, 2: 1}, "complets": {2: 1, 1: 1}, "episodes": 3,
                          "vides": 1, "segments": 3})
        self.assertEqual(e1.pauses(bits(3, 4, 5), 0), {"completes": {}, "bord": {3: 1}, "complets": {}, "episodes": 0,
                                                       "vides": 1, "segments": 1})
        self.assertEqual(e1.pauses(bits(3, 4, 5), bits(3, 4, 5)),
                         {"completes": {}, "bord": {}, "complets": {}, "episodes": 1, "vides": 0, "segments": 1})
        self.assertEqual(e1.pauses(bits(0, 2), bits(2)), {"completes": {}, "bord": {1: 1}, "complets": {},
                                                          "episodes": 1, "vides": 1, "segments": 2})


if __name__ == "__main__":
    unittest.main()
