"""CB-1, E-C-16, E-C-18, E-C-19 : écrivain chaîné. Octets attendus et sha256 écrits à la main (printf et sha256sum,
journal G1 de CB-1) ; chaîne recalculée par `chaine`, code de test indépendant de l'écrivain, sur les octets écrits.
CB-2d (C-2 de la G2 de P1) : après une OSError, l'écrivain refuse tout ; `fermer` rend toujours le verrou."""
import errno
import fcntl
import hashlib
import json
import os
import tempfile
import threading
import unittest

from shogen_s2bis.collecte import journal as j

WS = 1791154680             # 2026-10-04 22:58:00 UTC (date -u -d) ; la fenêtre suivante, 22:59, clôt l'heure de 23:00
H1, H2, H3 = ("dcc14fc4178d420c810974ae6605c8b36ea85176b3df064b7460ca254c7b4821",
              "0cd9c0052f3300de44714d13bd796dbe975300cb7338ad4e4b9ae447ee3c108d",
              "5e36358e082175a48f4fd673edf056edcd541490d430c61a5d0704197b74408e")
ATTENDU = ('{"jour":"2026-10-04","prec":"' + "0" * 64 + '","seq":0,"suivante":1791154740,"type":"ouverture"}\n'
           '{"n":1,"note":"é","prec":"' + H1 + '","seq":1,"type":"lecture","ws":1791154740}\n'
           '{"prec":"' + H2 + '","seq":2,"type":"marqueur","ws":1791154740}\n'
           '{"prec":"' + H3 + '","seq":3,"type":"point","ws":1791154740}\n').encode("utf-8")
TETE = (3, "24c367efe9318810fe57beb1d7ec97bbd3cf9b4fb4475a0b6c68114faae8afef")
FICHIER = "pool-2026-10-04-0.jsonl"


def chaine(octets, seq=0, prec="0" * 64):
    """Chaque ligne : JSON canonique (clés triées, séparateurs « , » et « : », UTF-8), `seq` suivant et `prec` = sha256
    de la ligne précédente, saut de ligne compris. Rend (seq attendu ensuite, tête, enregistrements)."""
    lignes, enrs = octets.split(b"\n"), []
    assert lignes.pop() == b"", "dernière ligne sans saut de ligne"
    for ligne in lignes:
        e = json.loads(ligne)
        assert ligne == json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(), ligne
        assert (e["seq"], e["prec"]) == (seq, prec), (e, seq, prec)
        seq, prec = seq + 1, hashlib.sha256(ligne + b"\n").hexdigest()
        enrs.append(e)
    return seq, prec, enrs


class Base(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.fsyncs, self.panne = d.name, [], None

    def espion(self, fd):
        """fsync injecté : relève l'inode du fichier ; lève `panne` si elle est posée (C-2)."""
        if self.panne:
            raise self.panne
        self.fsyncs.append(os.fstat(fd).st_ino)

    def journal(self, ws=WS):
        jl = j.Journal(self.d, "pool", fsync=self.espion)
        self.addCleanup(jl.fermer)
        return jl.ouvrir(ws)

    def etat(self):
        """Octets de chaque fichier du dossier."""
        e = {}
        for n in sorted(os.listdir(self.d)):
            with open(os.path.join(self.d, n), "rb") as f:
                e[n] = f.read()
        return e


class Ecrivain(Base):
    def test_octets_ecrits_a_la_main(self):
        jl = self.journal()
        jl.ecrire("lecture", WS + 60, note="é", n=1)
        self.assertEqual((jl.marqueur(WS + 60), self.etat()[FICHIER]), (TETE, ATTENDU))

    def test_chaine_et_points_horaires(self):
        jl = self.journal()
        for ws in range(WS + 60, WS + 62 * 60, 60):            # 22:59 à 23:59 : 61 fenêtres, deux fins d'heure
            jl.ecrire("lecture", ws, k=ws)
            tete = jl.marqueur(ws)
        seq, prec, enrs = chaine(self.etat()[FICHIER])
        self.assertEqual((seq - 1, prec), tete)
        self.assertEqual([e["ws"] for e in enrs if e["type"] == "point"], [WS + 60, WS + 61 * 60])

    def test_fsync_un_appel_par_marqueur_sur_le_journal(self):
        jl, n = self.journal(), []
        for ws in (WS + 60, WS + 120):                         # 22:59 porte aussi un point de contrôle
            jl.ecrire("lecture", ws, k=1)
            n.append(len(self.fsyncs))
            jl.marqueur(ws)
            n.append(len(self.fsyncs))
        self.assertEqual((n, set(self.fsyncs)), ([0, 1, 1, 2], {os.stat(os.path.join(self.d, FICHIER)).st_ino}))

    def test_seconde_instance_refusee_sans_ecriture(self):
        self.jl = self.journal()
        avant, res = self.etat(), []

        def essai():
            try:
                j.Journal(self.d, "pool").ouvrir(WS + 600)
                res.append("ouvert")
            except j.JournalOccupe as e:
                res.append(e.code)
        t = threading.Thread(target=essai, daemon=True)      # un verrou bloquant pendrait le fil, pas la suite
        t.start()
        t.join(5)
        self.assertEqual((res, self.etat()), (["JOURNAL/occupe"], avant))
        self.jl.fermer()                                       # fermer libère le verrou : un tiers le prend aussitôt
        with open(os.path.join(self.d, "pool.verrou"), "rb") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_refus_nommes_sans_ecriture(self):
        jl = self.journal()
        jl.marqueur(WS + 60)
        avant = self.etat()
        for code, appel in (("JOURNAL/type", lambda: jl.ecrire("lecture", WS + 120, prix=1.5)),
                            ("JOURNAL/type", lambda: jl.ecrire("lecture", WS + 120, brut=b"x")),
                            ("JOURNAL/type", lambda: jl.ecrire("lecture", WS + 120, d={1: 2})),
                            ("JOURNAL/reserve", lambda: jl.ecrire("marqueur", WS + 120)),
                            ("JOURNAL/reserve", lambda: jl.ecrire("lecture", WS + 120, seq=9)),
                            ("JOURNAL/fenetre", lambda: jl.ecrire("lecture", WS + 60, k=2)),
                            ("JOURNAL/fenetre", lambda: jl.marqueur(WS + 60)),
                            ("JOURNAL/fenetre", lambda: jl.ecrire("lecture", WS + 150, k=2)),
                            ("JOURNAL/fenetre", lambda: jl.ecrire("lecture", float(WS + 120), k=2))):
            with self.subTest(code=code):
                with self.assertRaises(j.ErreurJournal) as e:
                    appel()
                self.assertEqual(e.exception.code, code)
        self.assertEqual((self.etat(), len(self.fsyncs)), (avant, 1))

    def test_fsync_en_echec_ecrivain_casse_sans_doublon(self):          # C-2 (sonde S-5 de la G2)
        jl = self.journal()
        jl.marqueur(WS + 60)
        self.panne = OSError(errno.EIO, "fsync en échec (simulé)")
        self.assertRaises(OSError, jl.marqueur, WS + 120)
        self.panne, avant = None, self.etat()
        for appel in (lambda: jl.marqueur(WS + 120), lambda: jl.ecrire("lecture", WS + 180), lambda: jl.ouvrir(WS)):
            with self.assertRaises(j.ErreurJournal) as e:
                appel()
            self.assertEqual((e.exception.code, self.etat()), ("JOURNAL/casse", avant))
        self.assertEqual([e["ws"] for e in chaine(avant[FICHIER])[2] if e["type"] == "marqueur"], [WS + 60, WS + 120])
        jl.fermer()                                             # verrou rendu : l'instance suivante reprend
        self.journal(WS + 240)

    def test_fermer_rend_le_verrou_si_la_fermeture_du_fichier_echoue(self):     # C-2
        jl = self.journal()
        os.close(jl.fd)                                         # la fermeture du fichier échouera (EBADF)
        self.assertRaises(OSError, jl.fermer)
        with open(os.path.join(self.d, "pool.verrou"), "rb") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
