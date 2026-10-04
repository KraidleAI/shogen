"""CB-2, E-C-21 : reprise au dernier enregistrement intègre, queue non intègre conservée à l'octet et déclarée dans un
segment neuf, fenêtre du redémarrage refusée, sommes rattrapées. Queues calculées sur les octets du test."""
import errno
import hashlib
import json
import os
from unittest import mock

from shogen_s2bis.collecte import journal as j
from tests.test_fichiers import J1, J2
from tests.test_journal import FICHIER, WS, Base, chaine

SEG1, SEG2 = "pool-2026-10-04-1.jsonl", "pool-2026-10-04-2.jsonl"


def m(n):                                                     # fenêtre n minutes après 22:58 UTC (WS)
    return WS + 60 * n


def sans_chaine(enrs):
    return [{k: v for k, v in e.items() if k not in ("seq", "prec")} for e in enrs]


def ligne(seq, prec, sep=(",", ":"), **champs):
    """Ligne d'enregistrement écrite par le test, sans l'écrivain."""
    return json.dumps({**champs, "seq": seq, "prec": prec}, sort_keys=True, separators=sep).encode() + b"\n"


class AvecJournal(Base):
    def preparer(self):
        """Journal ouvert à 22:58, lectures et marqueurs de 22:59 à 23:01, lecture de 23:02 coupée par l'arrêt."""
        jl = self.journal()
        for n in (1, 2, 3, 4):
            jl.ecrire("lecture", m(n), k=n, suivante=0)             # « suivante » : champ ordinaire d'une lecture
            if n < 4:
                jl.marqueur(m(n))
        jl.fermer()
        return self.etat()[FICHIER]


class Reprise(AvecJournal):
    def test_reprise_dans_le_meme_fichier_fenetre_du_redemarrage_refusee(self):
        avant, n = self.preparer(), len(self.fsyncs)
        jl = self.journal(m(7))                                 # redémarrage pendant la fenêtre de 23:05
        self.assertEqual(self.fsyncs[n:], [os.stat(os.path.join(self.d, FICHIER)).st_ino])   # C-5 (G-06) : fsync
        self.assertRaises(j.ErreurJournal, jl.ecrire, "lecture", m(7), k=0)
        jl.ecrire("lecture", m(8), k=8)
        octets = self.etat()[FICHIER]
        self.assertEqual(octets[:len(avant)], avant)
        self.assertEqual(sans_chaine(chaine(octets)[2][-2:]), [
            {"type": "reprise", "ws": m(7), "suivante": m(4), "queue": None}, {"type": "lecture", "ws": m(8), "k": 8}])

    def queue(self, fabrique):
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        q = fabrique(seq, prec)
        with open(os.path.join(self.d, FICHIER), "ab") as f:
            f.write(q)
        self.journal(m(7)).fermer()
        e = self.etat()
        self.assertEqual(e[FICHIER], intact + q)                 # jamais réécrite
        enrs = chaine(e[SEG1], seq, prec)[2]                      # la chaîne reprend au dernier enregistrement intègre
        self.assertEqual(sans_chaine(enrs), [{"type": "reprise", "ws": m(7), "suivante": m(4), "queue": [
            {"fichier": FICHIER, "position": len(intact), "octets": len(q), "sha256": hashlib.sha256(q).hexdigest()}]}])
        self.assertEqual(e["pool.sha256"], f"{hashlib.sha256(intact + q).hexdigest()}  {FICHIER}\n".encode())

    def test_queue_ligne_coupee(self):
        self.queue(lambda s, p: b'{"k":4,"prec":"5e3')

    def test_queue_octets_nuls(self):
        self.queue(lambda s, p: b"\x00" * 300 + b"\n")

    def test_queue_ligne_chainee_non_canonique(self):
        self.queue(lambda s, p: ligne(s, p, (", ", ": "), type="lecture", ws=m(4), k=4))

    def test_queue_ligne_canonique_mal_chainee(self):
        self.queue(lambda s, p: ligne(s, "0" * 64, type="lecture", ws=m(4), k=4))

    def test_queue_fenetre_non_entiere(self):                   # C-1 : jamais prise pour la dernière fenêtre écrite
        self.queue(lambda s, p: ligne(s, p, type="lecture", ws="23:02", k=4))

    def test_queue_ligne_chainee_trop_longue_et_refus_a_l_ecriture(self):
        self.queue(lambda s, p: ligne(s, p, type="lecture", ws=m(4), x="a" * j.LIMITE))
        with self.assertRaises(j.ErreurJournal) as e:
            self.journal(m(9)).ecrire("lecture", m(10), x="a" * j.LIMITE)
        self.assertEqual(e.exception.code, "JOURNAL/taille")

    def test_ecriture_partielle_ecrivain_casse_queue_declaree(self):     # C-2 (sonde S-6 de la G2)
        jl = self.journal()
        jl.marqueur(m(1))
        intact = self.etat()[FICHIER]

        def coupe(fd, octets):                                  # disque plein : 40 octets écrits, puis ENOSPC
            os.write(fd, octets[:40])
            raise OSError(errno.ENOSPC, "disque plein (simulé)")
        with mock.patch.object(j, "_tout", coupe):
            self.assertRaises(OSError, jl.ecrire, "lecture", m(2), k=2)
        for appel in (lambda: jl.ecrire("lecture", m(2), k=2), lambda: jl.marqueur(J2)):
            with self.assertRaises(j.ErreurJournal) as e:
                appel()
            self.assertEqual(e.exception.code, "JOURNAL/casse")
        jl.fermer()
        self.journal(m(3)).fermer()
        e, (seq, prec, _e) = self.etat(), chaine(intact)
        q = e[FICHIER][len(intact):]
        self.assertEqual(chaine(e[SEG1], seq, prec)[2][0]["queue"], [
            {"fichier": FICHIER, "position": len(intact), "octets": 40, "sha256": hashlib.sha256(q).hexdigest()}])
        self.assertEqual(e["pool.sha256"], f"{hashlib.sha256(e[FICHIER]).hexdigest()}  {FICHIER}\n".encode())

    def test_queue_imbrication_profonde_et_refus_a_l_ecriture(self):
        self.queue(lambda s, p: b"[" * 100000 + b"]" * 100000 + b"\n")
        x = []
        for _i in range(100000):
            x = [x]
        with self.assertRaises(j.ErreurJournal) as e:
            self.journal(m(9)).ecrire("lecture", m(10), x=x)
        self.assertEqual(e.exception.code, "JOURNAL/type")

    def segment(self, fabrique):
        """Segment 1 illisible dès sa première ligne : repli sur le segment 0, segment 1 déclaré, segment 2 ouvert."""
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        contenu = fabrique(seq, prec)
        with open(os.path.join(self.d, SEG1), "wb") as f:
            f.write(contenu)
        self.journal(m(7)).fermer()
        e = self.etat()
        self.assertEqual(chaine(e[SEG2], seq, prec)[2][0]["queue"], [
            {"fichier": SEG1, "position": 0, "octets": len(contenu), "sha256": hashlib.sha256(contenu).hexdigest()}])
        sommes = f"{hashlib.sha256(intact).hexdigest()}  {FICHIER}\n{hashlib.sha256(contenu).hexdigest()}  {SEG1}\n"
        self.journal(m(9))                                      # seconde reprise : aucune somme inscrite deux fois
        self.assertEqual((e["pool.sha256"], self.etat()["pool.sha256"]), (sommes.encode(), sommes.encode()))

    def test_segment_neuf_tronque_repli_sur_le_precedent(self):
        self.segment(lambda s, p: b'{"jour":')                  # coupure juste après la création du segment

    def test_segment_ouvert_par_un_marqueur_repli(self):
        self.segment(lambda s, p: ligne(s, p, type="marqueur", ws=m(4)))

    def test_segment_ouvert_par_un_seq_non_entier_repli(self):         # C-5 (G-07)
        self.segment(lambda s, p: ligne(True, p, type="reprise", ws=m(5), suivante=m(4), queue=None))

    def test_deux_queues_declarees_dans_l_ordre(self):                 # C-5 (G-08)
        seq, prec, _e = chaine(self.preparer())
        for n, q in ((FICHIER, b'{"k":4'), (SEG1, b'{"jour":')):
            with open(os.path.join(self.d, n), "ab") as f:
                f.write(q)
        self.journal(m(7)).fermer()
        self.assertEqual([x["fichier"] for x in chaine(self.etat()[SEG2], seq, prec)[2][0]["queue"]], [FICHIER, SEG1])

    def test_reprise_sur_fichier_clos_fichier_neuf(self):              # C-5 (G-02)
        seq, prec, _e = chaine(self.preparer())
        with open(os.path.join(self.d, FICHIER), "ab") as f:
            f.write(ligne(seq, prec, type="cloture", jour="2026-10-04"))
        clos = self.etat()[FICHIER]
        self.journal(m(7)).fermer()
        e = self.etat()
        self.assertEqual((e[FICHIER], chaine(e[SEG1], *chaine(clos)[:2])[2][0]["type"]), (clos, "reprise"))

    def test_reprise_un_jour_plus_tard_cloture_a_la_veille(self):      # C-5 (G-01, M-18)
        avant = self.preparer()
        self.journal(J2 + 3600).fermer()                        # 2026-10-05 01:00 : fichier de la veille propre
        e = self.etat()
        seq, prec, enrs = chaine(e[FICHIER])
        self.assertEqual((e[FICHIER][:len(avant)], sans_chaine(enrs[-1:])), (avant, [{"type": "cloture",
                                                                                         "jour": "2026-10-04"}]))
        self.assertEqual(sans_chaine(chaine(e["pool-2026-10-05-0.jsonl"], seq, prec)[2]), [
            {"type": "reprise", "ws": J2 + 3600, "suivante": m(4), "queue": None}])
        self.assertEqual(e["pool.sha256"], f"{hashlib.sha256(e[FICHIER]).hexdigest()}  {FICHIER}\n".encode())

    def test_ligne_de_limite_octets_admise_un_de_plus_refusee(self):   # C-5 (G-10, G-11)
        self.preparer()
        jl = self.journal(m(8))
        seq, prec, _e = chaine(self.etat()[FICHIER])
        x = "a" * (j.LIMITE - len(ligne(seq, prec, type="lecture", ws=m(9), x="")))
        jl.ecrire("lecture", m(9), x=x)                         # LIMITE octets : écrite
        self.assertRaises(j.ErreurJournal, jl.ecrire, "lecture", m(9), x=x + "a")      # LIMITE + 1 : refusée
        jl.fermer()
        seq, prec, _e = chaine(self.etat()[FICHIER])            # relue intègre
        with open(os.path.join(self.d, FICHIER), "ab") as f:
            f.write(ligne(seq, prec, type="lecture", ws=m(9), x=x + "a"))     # LIMITE + 1, chaînée : une queue
        self.journal(m(10)).fermer()
        self.assertEqual(chaine(self.etat()[SEG1], seq, prec)[2][0]["queue"][0]["octets"], j.LIMITE + 1)

    def test_horloge_reculee_d_un_jour_segment_du_jour_repris(self):
        jl = self.journal(J1 - 60)
        jl.marqueur(J1)
        jl.marqueur(J2)
        jl.fermer()
        with open(os.path.join(self.d, "pool-2026-10-05-0.jsonl"), "ab") as f:
            f.write(b'{"jour":')
        self.journal(J1 - 120)                                  # l'horloge dit la veille, 23:57
        self.assertEqual(sorted(n for n in self.etat() if n.endswith(".jsonl")), [
            FICHIER, "pool-2026-10-05-0.jsonl", "pool-2026-10-05-1.jsonl"])

    def test_sommes_rattrapees_et_ligne_coupee_close(self):
        jl = self.journal(J1 - 60)
        jl.marqueur(J1)
        jl.marqueur(J2)
        jl.fermer()
        with open(os.path.join(self.d, "pool.sha256"), "wb") as f:
            f.write(b"0123")                                    # coupure pendant l'inscription de la somme
        self.journal(J2 + 120)
        e = self.etat()
        self.assertEqual(e["pool.sha256"], f"0123\n{hashlib.sha256(e[FICHIER]).hexdigest()}  {FICHIER}\n".encode())
