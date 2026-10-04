"""CB-2, E-C-22 : toute fenêtre sans marqueur porte sa cause, déclarée par un `trou` juste avant le marqueur qui suit
(arrêt du processus, horloge reculée, saut en cours d'exécution) ; window_start strictement croissant d'un démarrage au
suivant. Valeurs attendues écrites à la main ; chaîne recalculée par `chaine`."""
import os

from shogen_s2bis.collecte import journal as j
from tests.test_fichiers import J1, J2
from tests.test_journal import FICHIER, chaine
from tests.test_reprise import AvecJournal, ligne, m, sans_chaine


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
        jl = self.journal(m(3))                                 # même fenêtre que le dernier marqueur : pas un recul
        self.assertRaises(j.ErreurJournal, jl.ecrire, "lecture", m(4), k=0)    # m4 entamée avant l'arrêt (S-2)
        jl.marqueur(m(5))
        self.assertEqual(self.derniers(3), [{"type": "reprise", "ws": m(3), "suivante": m(4), "queue": None},
                                            {"type": "trou", "de": m(4), "a": m(4), "cause": "arret"},
                                            {"type": "marqueur", "ws": m(5)}])

    def test_cause_remise_a_saut_par_un_marqueur_sans_trou(self):
        jl = self.journal()                                     # aucune fenêtre entamée sans marqueur (Q-4, C-1)
        for n in (1, 2, 3):
            jl.marqueur(m(n))
        jl.fermer()
        jl = self.journal(m(3))
        jl.marqueur(m(4))
        jl.marqueur(m(6))
        self.assertEqual(self.derniers(3), [{"type": "marqueur", "ws": m(4)},
                                            {"type": "trou", "de": m(5), "a": m(5), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(6)}])

    def test_horloge_reculee_sans_doublon_et_trou_declare(self):
        self.preparer()
        jl = self.journal(m(-8))                                # l'horloge du redémarrage dit 22:50
        for n in (-7, 0, 3, 4):                                 # m4 : entamée sans marqueur avant l'arrêt (S-1)
            self.assertRaises(j.ErreurJournal, jl.marqueur, m(n))
        self.assertRaises(j.ErreurJournal, jl.ecrire, "lecture", m(4), k=0)
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

    def test_refus_n_ecrit_ni_trou_ni_bascule(self):                    # C-6 (a) ; sonde S-11 de la G2
        jl = self.journal()
        jl.marqueur(m(1))
        avant = self.etat()
        for code, appel in (("JOURNAL/taille", lambda: jl.marqueur(m(4), x="a" * j.LIMITE)),   # trou dû
                            ("JOURNAL/type", lambda: jl.ecrire("lecture", J2, prix=1.5))):    # bascule due
            with self.assertRaises(j.ErreurJournal) as e:
                appel()
            self.assertEqual((e.exception.code, self.etat()), (code, avant))
        jl.marqueur(m(4))
        jl.marqueur(m(5))
        self.assertEqual(self.derniers(4), [{"type": "point", "ws": m(1)},
                                            {"type": "trou", "de": m(2), "a": m(3), "cause": "saut"},
                                            {"type": "marqueur", "ws": m(4)}, {"type": "marqueur", "ws": m(5)}])

    def test_controle_au_rang_reel_apres_bascule_et_trou(self):         # C-6 (a) : rang 10, et non 7, 8 ou 9
        jl = self.journal(J1 - 300)                             # 23:54 ; marqueurs de 23:55 à 23:59, point : rangs 1-6
        for ws in range(J1 - 240, J1 + 60, 60):
            jl.marqueur(ws)
        avant, x = self.etat(), "a" * (j.LIMITE + 1 - len(ligne(10, "0" * 64, type="marqueur", ws=J2 + 60, x="")))
        with self.assertRaises(j.ErreurJournal) as e:           # rangs 7 à 10 : cloture, ouverture, trou, marqueur
            jl.marqueur(J2 + 60, x=x)
        self.assertEqual((e.exception.code, self.etat()), ("JOURNAL/taille", avant))

    def test_reprise_apres_un_trou_sans_marqueur(self):                  # coupure entre un trou et son marqueur
        jl = self.journal()
        jl.marqueur(m(1))
        jl.fermer()
        seq, prec, _e = chaine(self.etat()[FICHIER])
        with open(os.path.join(self.d, FICHIER), "ab") as f:
            f.write(ligne(seq, prec, type="trou", de=m(2), a=m(3), cause="saut"))
        self.journal(m(5)).marqueur(m(7))
        self.assertEqual(self.derniers(4), [{"type": "trou", "de": m(2), "a": m(3), "cause": "saut"},
                                            {"type": "reprise", "ws": m(5), "suivante": m(4), "queue": None},
                                            {"type": "trou", "de": m(4), "a": m(6), "cause": "arret"},
                                            {"type": "marqueur", "ws": m(7)}])

    def test_fenetre_anterieure_a_une_fenetre_ecrite_refusee(self):     # C-1 : S-3, puis S-4 (J après J+1)
        jl = self.journal()
        for ecrite, refusee in ((m(3), m(1)), (J2, J1)):
            jl.ecrire("lecture", ecrite, k=1)
            avant = self.etat()
            for appel in (lambda: jl.ecrire("lecture", refusee, k=2), lambda: jl.marqueur(refusee)):
                with self.assertRaises(j.ErreurJournal) as e:
                    appel()
                self.assertEqual((e.exception.code, self.etat()), ("JOURNAL/fenetre", avant))

    def test_derniere_fenetre_cherchee_dans_le_fichier_precedent(self):  # C-1 : fichier du jour sans fenêtre écrite
        jl = self.journal(J1 - 60)
        jl.ecrire("lecture", J1, k=1)                           # 23:59, sans marqueur
        jl.ecrire("lecture", J2, k=2)                           # 00:00 : bascule
        jl.fermer()
        n2 = "pool-2026-10-05-0.jsonl"
        ouverture = self.etat()[n2].split(b"\n")[0]             # coupure : la lecture de 00:00 n'est pas sur le disque
        with open(os.path.join(self.d, n2), "wb") as f:
            f.write(ouverture + b"\n")
        self.assertRaises(j.ErreurJournal, self.journal(J1 - 120).ecrire, "lecture", J1, k=3)   # horloge : veille
