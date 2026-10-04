"""CB-2, E-C-22 : toute fenêtre sans marqueur porte sa cause, déclarée par un `trou` juste avant le marqueur qui suit
(arrêt du processus, horloge reculée, saut en cours d'exécution) ; window_start strictement croissant d'un démarrage au
suivant. Valeurs attendues écrites à la main ; chaîne recalculée par `chaine`."""
from shogen_s2bis.collecte import journal as j
from tests.test_journal import FICHIER, chaine
from tests.test_reprise import AvecJournal, m, sans_chaine


class Trous(AvecJournal):
    def derniers(self, n):
        return sans_chaine(chaine(self.etat()[FICHIER])[2][-n:])

    def test_trou_arret_apres_reprise_puis_saut(self):
        self.preparer()
        jl = self.journal(m(7))
        jl.marqueur(m(8))
        jl.marqueur(m(10))
        self.assertEqual(self.derniers(5), [{"type": "reprise", "ws": m(7), "suivante": m(4), "queue": None},
                                            {"type": "trou", "de": m(4), "a": m(7), "cause": "arret"},
                                            {"type": "marqueur", "ws": m(8)},
                                            {"type": "trou", "de": m(9), "a": m(9), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(10)}])

    def test_redemarrage_dans_la_fenetre_du_dernier_marqueur(self):
        self.preparer()
        self.journal(m(3)).marqueur(m(5))                       # même fenêtre que le dernier marqueur : pas un recul
        self.assertEqual(self.derniers(2), [{"type": "trou", "de": m(4), "a": m(4), "cause": "arret"},
                                            {"type": "marqueur", "ws": m(5)}])

    def test_cause_remise_a_saut_par_un_marqueur_sans_trou(self):
        self.preparer()
        jl = self.journal(m(3))
        jl.marqueur(m(4))
        jl.marqueur(m(6))
        self.assertEqual(self.derniers(3), [{"type": "marqueur", "ws": m(4)},
                                            {"type": "trou", "de": m(5), "a": m(5), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(6)}])

    def test_horloge_reculee_sans_doublon_et_trou_declare(self):
        self.preparer()
        jl = self.journal(m(-8))                                # l'horloge du redémarrage dit 22:50
        for n in (-7, 0, 3):
            self.assertRaises(j.ErreurJournal, jl.marqueur, m(n))
        jl.marqueur(m(6))
        self.assertEqual(self.derniers(3), [{"type": "reprise", "ws": m(-8), "suivante": m(4), "queue": None},
                                            {"type": "trou", "de": m(4), "a": m(5), "cause": "horloge_reculee"},
                                            {"type": "marqueur", "ws": m(6)}])

    def test_saut_en_cours_d_execution(self):
        jl = self.journal()
        jl.marqueur(m(1))
        jl.marqueur(m(4))
        self.assertEqual(self.derniers(2), [{"type": "trou", "de": m(2), "a": m(3), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(4)}])

    def test_marqueur_refuse_apres_son_trou_sans_doublon(self):
        jl = self.journal()
        jl.marqueur(m(1))
        self.assertRaises(j.ErreurJournal, jl.marqueur, m(4), x="a" * j.LIMITE)   # trou écrit, marqueur trop long
        jl.marqueur(m(4))
        jl.marqueur(m(5))
        self.assertEqual(self.derniers(4), [{"type": "point", "ws": m(1)},
                                            {"type": "trou", "de": m(2), "a": m(3), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(4)}, {"type": "marqueur", "ws": m(5)}])

    def test_reprise_apres_un_trou_sans_marqueur(self):
        jl = self.journal()
        jl.marqueur(m(1))
        self.assertRaises(j.ErreurJournal, jl.marqueur, m(4), x="a" * j.LIMITE)
        jl.fermer()
        self.journal(m(5)).marqueur(m(7))
        self.assertEqual(self.derniers(4), [{"type": "trou", "de": m(2), "a": m(3), "cause": "saut"},
                                            {"type": "reprise", "ws": m(5), "suivante": m(4), "queue": None},
                                            {"type": "trou", "de": m(4), "a": m(6), "cause": "arret"},
                                            {"type": "marqueur", "ws": m(7)}])
