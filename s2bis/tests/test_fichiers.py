"""CB-2, E-C-20 : fichiers quotidiens bornés à 00:00 UTC, clos par `cloture`, sommés ; la chaîne continue d'un fichier
au suivant. Sommes recalculées ici sur les octets lus ; chaîne recalculée par `chaine` (tests/test_journal.py). CB-19c
(C-2 (a) de la relecture d'intégration de P1) : fsync du dossier après chaque création, relevé par l'espion."""
import errno
import hashlib
import os
from unittest import mock

from tests.test_journal import WS, Base, chaine, code

J1, J2, J3 = WS + 3660, WS + 3720, WS + 3720 + 86400   # 2026-10-04 23:59, 2026-10-05 00:00, 2026-10-06 00:00 (UTC)
NOMS = ["pool-2026-10-04-0.jsonl", "pool-2026-10-05-0.jsonl", "pool-2026-10-06-0.jsonl"]


class Fichiers(Base):
    def test_bascules_cloture_sommes_et_chaine_continue(self):
        jl = self.journal(J1 - 60)
        for ws in range(J1, J3 + 60, 60):
            jl.ecrire("lecture", ws, k=1)
            jl.marqueur(ws)
        e, seq, prec, par_fichier = self.etat(), 0, "0" * 64, []
        for n in NOMS:
            seq, prec, enrs = chaine(e[n], seq, prec)
            par_fichier.append((enrs[0]["type"], enrs[0]["jour"], enrs[0]["suivante"], enrs[-1]["type"],
                                enrs[-1].get("jour")))
        self.assertEqual(par_fichier, [("ouverture", "2026-10-04", J1, "cloture", "2026-10-04"),
                                       ("ouverture", "2026-10-05", J2, "cloture", "2026-10-05"),
                                       ("ouverture", "2026-10-06", J3, "marqueur", None)])
        sommes = "".join(f"{hashlib.sha256(e[n]).hexdigest()}  {n}\n" for n in NOMS[:2])
        self.assertEqual(e["pool.sha256"], sommes.encode())
        ino = {n: os.stat(os.path.join(self.d, n)).st_ino for n in (NOMS[0], "pool.sha256")}
        self.assertEqual((self.fsyncs.count(ino[NOMS[0]]), self.fsyncs.count(ino["pool.sha256"])), (2, 2))

    def test_fsync_du_dossier_apres_chaque_creation(self):        # CB-19c, C-2 (a) de la relecture d'intégration
        """Après la création d'un fichier du journal (journal neuf, bascule, segment de reprise) et du fichier de
        sommes, l'écrivain appelle fsync sur le dossier, une fois, le fichier créé déjà écrit (sa première ligne, ou la
        première somme) : à chaque appel, les fichiers créés jusque-là, et eux seuls, sont présents et non vides. Un
        marqueur sans création n'en appelle aucun."""
        jl = self.journal(J1 - 60)
        for ws in (J1, J2, J2 + 60):                            # J2 : bascule, sommes créées ; J2 + 60 : rien
            jl.marqueur(ws)
        jl.fermer()
        with open(os.path.join(self.d, NOMS[1]), "ab") as f:
            f.write(b'{"coupee"')                              # queue : la reprise ouvre un segment neuf
        self.journal(J2 + 180).fermer()
        crees = [NOMS[0], "pool.sha256", NOMS[1], "pool-2026-10-05-1.jsonl"]
        self.assertEqual([[n for n in crees if inst.get(n)] for nom, inst in self.appels if nom == "."],
                         [crees[:1], crees[:2], crees[:3], crees])

    def test_bascule_en_echec_puis_fermer(self):              # C-2 (O-3 de la G2) : création du lendemain refusée
        jl, vrai = self.journal(J1 - 60), os.open

        def ouvrir(chemin, drapeaux, *a):                       # disque plein à la création exclusive du lendemain
            if drapeaux & os.O_EXCL:
                raise OSError(errno.ENOSPC, "disque plein (simulé)")
            return vrai(chemin, drapeaux, *a)
        with mock.patch.object(os, "open", ouvrir):
            self.assertRaises(OSError, jl.marqueur, J2)
        jl.fermer()                                             # le descripteur clos à la bascule n'est pas refermé
        self.assertEqual(code(lambda: jl.marqueur(J2)), "JOURNAL/casse")

    def test_bascule_vers_un_jour_deja_present_segment_suivant(self):   # SHOGEN-S2BIS-SEGMENT-JOUR-1 (N-1)
        """`cloture` perdue avant la coupure, fichier vide du lendemain laissé : la reprise s'écrit à la suite du
        fichier repris ; la bascule crée le segment suivant du lendemain (1 + le plus grand numéro du jour), chaîné, au
        lieu de heurter le fichier présent (avant : FileExistsError, écrivain cassé)."""
        jl = self.journal(J1 - 60)
        jl.marqueur(J1)
        jl.fermer()
        open(os.path.join(self.d, NOMS[1]), "wb").close()
        jl = self.journal(J1)
        self.assertEqual(code(lambda: jl.marqueur(J2)), None)
        e, suivant = self.etat(), "pool-2026-10-05-1.jsonl"
        seq, prec, enrs = chaine(e[NOMS[0]])
        self.assertEqual(([n for n in e if n.endswith(".jsonl")], e[NOMS[1]], [x["type"] for x in enrs[-2:]],
                          [x["type"] for x in chaine(e[suivant], seq, prec)[2]]),
                         ([NOMS[0], NOMS[1], suivant], b"", ["reprise", "cloture"], ["ouverture", "marqueur"]))

    def test_grammaire_des_noms_refus_a_l_ouverture_ignore_a_la_bascule(self):   # CB-18q, lettre C-5 (§6.1, §7.7)
        """k suit `0|[1-9][0-9]*`. À l'ouverture, un nom qui commence par « pool- » et finit par « .jsonl » sans suivre
        la grammaire est refusé (JOURNAL/nom) : rien n'est écrit, le verrou est rendu. Un nom d'un autre préfixe ou
        d'une autre fin est ignoré. À la bascule, un nom non conforme apparu en cours d'exécution est ignoré : le
        lendemain prend le numéro 0, chaîné ; le redémarrage suivant refuse."""
        for n in ("pool.verrou", "pool.sha256", "pool-2026-10-04-0.jsonl.bak", "pool-2026-10-04-01.JSONL",
                  "autre-2026-10-04-01.jsonl", "pool2026-10-04-01.jsonl"):
            open(os.path.join(self.d, n), "wb").close()
        avant = self.etat()
        for n in ("pool-2026-10-04-01.jsonl", "pool-2026-10-04-00.jsonl", "pool-2026-1-04-0.jsonl", "pool-x.jsonl",
                  "pool-2026-10-04-.jsonl", "pool-2026-10-04-1a.jsonl", "pool--2026-10-04-0.jsonl"):
            open(os.path.join(self.d, n), "wb").close()
            with self.subTest(nom=n):
                self.assertEqual((code(lambda: self.journal(J1 - 60)), self.etat()), ("JOURNAL/nom", {**avant, n: b""}))
            os.remove(os.path.join(self.d, n))
        jl = self.journal(J1 - 60)
        jl.marqueur(J1)
        open(os.path.join(self.d, "pool-2026-10-05-01.jsonl"), "wb").close()
        jl.marqueur(J2)
        jl.fermer()
        e = self.etat()
        self.assertEqual((chaine(e[NOMS[1]], *chaine(e[NOMS[0]])[:2])[2][0]["type"], code(lambda: self.journal(J2))),
                         ("ouverture", "JOURNAL/nom"))
