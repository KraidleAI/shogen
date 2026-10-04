"""CB-2, E-C-21 : reprise au dernier enregistrement intègre, queue non intègre conservée à l'octet et déclarée dans un
segment neuf, fenêtre du redémarrage refusée. Queues calculées sur les octets écrits par le test."""
import hashlib
import json
import os

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
        avant = self.preparer()
        jl = self.journal(m(7))                                 # redémarrage pendant la fenêtre de 23:05
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

    def test_queue_ligne_coupee(self):
        self.queue(lambda s, p: b'{"k":4,"prec":"5e3')

    def test_queue_octets_nuls(self):
        self.queue(lambda s, p: b"\x00" * 300 + b"\n")

    def test_queue_ligne_chainee_non_canonique(self):
        self.queue(lambda s, p: ligne(s, p, (", ", ": "), type="lecture", ws=m(4), k=4))

    def test_queue_ligne_canonique_mal_chainee(self):
        self.queue(lambda s, p: ligne(s, "0" * 64, type="lecture", ws=m(4), k=4))

    def test_queue_ligne_chainee_trop_longue_et_refus_a_l_ecriture(self):
        self.queue(lambda s, p: ligne(s, p, type="lecture", ws=m(4), x="a" * j.LIMITE))
        with self.assertRaises(j.ErreurJournal) as e:
            self.journal(m(9)).ecrire("lecture", m(10), x="a" * j.LIMITE)
        self.assertEqual(e.exception.code, "JOURNAL/taille")

    def segment(self, fabrique):
        """Segment 1 illisible dès sa première ligne : repli sur le segment 0, segment 1 déclaré, segment 2 ouvert."""
        intact = self.preparer()
        seq, prec, _e = chaine(intact)
        contenu = fabrique(seq, prec)
        with open(os.path.join(self.d, SEG1), "wb") as f:
            f.write(contenu)
        self.journal(m(7))
        e = self.etat()
        self.assertEqual(chaine(e[SEG2], seq, prec)[2][0]["queue"], [
            {"fichier": SEG1, "position": 0, "octets": len(contenu), "sha256": hashlib.sha256(contenu).hexdigest()}])

    def test_segment_neuf_tronque_repli_sur_le_precedent(self):
        self.segment(lambda s, p: b'{"jour":')                  # coupure juste après la création du segment

    def test_segment_ouvert_par_un_marqueur_repli(self):
        self.segment(lambda s, p: ligne(s, p, type="marqueur", ws=m(4)))

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
