"""CB-2, E-C-21 : reprise au dernier enregistrement intègre, queue non intègre conservée à l'octet et déclarée dans un
segment neuf, fenêtre du redémarrage refusée, sommes rattrapées. Queues calculées sur les octets du test."""
import errno
import hashlib
import json
import os
from unittest import mock

from shogen_s2bis.collecte import journal as j
from tests.test_fichiers import J1, J2, J3
from tests.test_journal import FICHIER, WS, Base, chaine, code, imbrique

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

    def test_queue_entier_de_641_chiffres(self):                       # SHOGEN-S2BIS-ENTIER-ECRIVAIN-1 (I-1)
        self.queue(lambda s, p: ligne(s, p, type="lecture", ws=m(4), x=10 ** 640))

    def test_queue_ligne_chainee_de_65_niveaux(self):                  # CB-18n, lettre C-4 du FORMAT (§8.3)
        self.queue(lambda s, p: ligne(s, p, type="lecture", ws=m(4), x=imbrique(64)))

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
        self.assertEqual(e.exception.code, "JOURNAL/imbrication")          # avant le sérialiseur (C-4)

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

    def test_horloge_avant_le_jour_d_un_fichier_sans_ligne_integre(self):   # SHOGEN-S2BIS-SEGMENT-JOUR-1 (N-1)
        """Panne juste après la bascule : le fichier du lendemain n'a aucune ligne intègre (vide, ou ouverture coupée à
        8 octets) ; l'horloge du redémarrage dit la veille. Le segment neuf prend le jour le plus tardif des fichiers
        présents, au numéro suivant : les noms gardent l'ordre de la chaîne et des sommes (FORMAT §7.2) ; la bascule
        suivante ne heurte aucun fichier (avant : segment de la veille nommé avant le fichier qu'il déclare, puis
        FileExistsError à la bascule)."""
        for p, taille in (("vide", 0), ("coupe", 8)):
            noms = [f"{p}-2026-10-0{x}.jsonl" for x in ("4-0", "5-0", "5-1", "6-0")]
            jl = self.journal(J1 - 60, p)
            jl.marqueur(J1)
            jl.marqueur(J2)                                     # bascule : fichier du 10-05 ouvert
            jl.fermer()
            os.truncate(os.path.join(self.d, noms[1]), taille)  # panne : rien d'intègre au fichier du 10-05
            queue = self.etat()[noms[1]]
            jl = self.journal(J1 - 120, p)                      # l'horloge dit la veille, 23:57
            with self.subTest(prefixe=p):
                self.assertEqual(sorted(n for n in self.etat() if n.startswith(p + "-")), noms[:3])
                jl.marqueur(J2)
                jl.marqueur(J3)
                e = self.etat()
                seq, prec, enrs = chaine(e[noms[2]], *chaine(e[noms[0]])[:2])
                q = [{"fichier": noms[1], "position": 0, "octets": taille, "sha256": hashlib.sha256(queue).hexdigest()}]
                self.assertEqual((sans_chaine(enrs[:1]), chaine(e[noms[3]], seq, prec)[2][0]["type"],
                                  [x.split("  ")[1] for x in e[p + ".sha256"].decode().split(chr(10))[:-1]]), (
                    [{"type": "reprise", "ws": J1 - 120, "suivante": J2, "queue": q if taille else None}], "ouverture",
                    noms[:3]))

    def test_onze_redemarrages_d_un_jour_segments_a_deux_chiffres(self):    # SHOGEN-S2BIS-SEGMENTS-10-1 (MR-26)
        """Onze redémarrages d'un même jour, chacun sur une ligne coupée du dernier segment : segments 1 à 11 du jour.
        Le numéro se lit en entier, jamais dans l'ordre des noms en texte (« -10 » y trie avant « -2 ») : chaque
        segment déclare la queue du précédent par numéro, se chaîne à sa `reprise`, et les sommes suivent ce même
        ordre (FORMAT §6.1, §7.2). Avant : aucun test au-delà de 9 segments (MR-26, segments à deux chiffres
        invisibles, survivait à la G2 de la tranche C)."""
        self.preparer()
        noms = [FICHIER] + [f"pool-2026-10-04-{k}.jsonl" for k in range(1, 12)]
        for k in range(1, 12):
            with open(os.path.join(self.d, noms[k - 1]), "ab") as f:
                f.write(b'{"k":')                                    # coupure : queue du dernier segment
            self.assertEqual(code(lambda: self.journal(m(6 + k)).fermer()), None)
        e = self.etat()
        lignes = {n: e[n].split(bytes([10]))[0] for n in noms[1:]}          # première ligne de chaque segment
        tetes = {n: json.loads(x) for n, x in lignes.items()}
        self.assertEqual(sorted(n for n in e if n.endswith(".jsonl")), sorted(noms))
        self.assertEqual([(tetes[n]["type"], tetes[n]["queue"][0]["fichier"]) for n in noms[1:]],
                         [("reprise", n) for n in noms[:-1]])
        self.assertEqual([tetes[n]["prec"] for n in noms[2:]],
                         [hashlib.sha256(lignes[n] + bytes([10])).hexdigest() for n in noms[1:-1]])
        self.assertEqual([x.split("  ")[1] for x in e["pool.sha256"].decode().split(chr(10))[:-1]], noms[:-1])

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
