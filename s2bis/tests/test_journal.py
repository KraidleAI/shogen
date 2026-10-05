"""CB-1, E-C-16, E-C-18, E-C-19 : écrivain chaîné. Octets attendus et sha256 écrits à la main (printf et sha256sum,
journal G1 de CB-1) ; chaîne recalculée par `chaine`, code de test indépendant de l'écrivain, sur les octets écrits.
CB-2d, CB-2e (C-2, C-3, C-5 de la G2 de P1) : écrivain inutilisable après une OSError ; cycle refusé en temps borné.
CB-18a (SHOGEN-S2BIS-ECRIVAIN-USAGE-1) : garde d'un seul fil, refus nommés de l'écrivain neuf, fermé ou déjà ouvert,
garde `_terminal` sur toute méthode publique d'écriture (contrôle mécanique). SHOGEN-S2BIS-ENTIER-ECRIVAIN-1 (I-1 de
la G2 du recalcul) : entiers de 640 chiffres au plus. CB-18n (lettre C-4 du FORMAT, avis sur le banc de concordance) :
64 niveaux d'imbrication au plus, la racine au niveau 1 (`JOURNAL/imbrication`)."""
import errno
import fcntl
import hashlib
import json
import os
import sys
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


def imbrique(n, fond=None):
    """n listes emboîtées ; la plus profonde est vide, ou contient `fond`."""
    x = [] if fond is None else [fond]
    for _i in range(n - 1):
        x = [x]
    return x


def code(appel):
    """Code du refus nommé que lève `appel`, nom du type de toute autre exception, None sans exception."""
    try:
        appel()
    except Exception as e:                                          # refus nommé, ou défaut relevé par son type
        return getattr(e, "code", type(e).__name__)
    return None


class Base(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.fsyncs, self.tailles, self.panne = d.name, [], [], None

    def espion(self, fd):
        """fsync injecté : relève l'inode et la taille du fichier ; lève `panne` si elle est posée (C-2)."""
        if self.panne:
            raise self.panne
        self.fsyncs.append(os.fstat(fd).st_ino)
        self.tailles.append(os.fstat(fd).st_size)

    def journal(self, ws=WS, prefixe="pool"):
        jl = j.Journal(self.d, prefixe, fsync=self.espion)
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
        jl, n, t = self.journal(), [], []
        for ws in (WS + 60, WS + 120):                         # 22:59 porte aussi un point de contrôle
            jl.ecrire("lecture", ws, k=1)
            n.append(len(self.fsyncs))
            jl.marqueur(ws)
            n.append(len(self.fsyncs))
            t.append(len(self.etat()[FICHIER]))                 # C-5 (M-07) : fsync après le point
        self.assertEqual((n, set(self.fsyncs)), ([0, 1, 1, 2], {os.stat(os.path.join(self.d, FICHIER)).st_ino}))
        self.assertEqual(self.tailles, t)

    def test_seconde_instance_refusee_sans_ecriture(self):
        self.jl, seconde = self.journal(), j.Journal(self.d, "pool")
        avant, res = self.etat(), []

        def essai():
            try:
                seconde.ouvrir(WS + 600)
                res.append("ouvert")
            except j.JournalOccupe as e:
                res.append(e.code)
        t = threading.Thread(target=essai, daemon=True)      # un verrou bloquant pendrait le fil, pas la suite
        t.start()
        t.join(5)
        self.assertEqual((res, self.etat()), (["JOURNAL/occupe"], avant))
        self.assertEqual((seconde.fd, seconde.verrou), (None, None))     # C-5 (G-19) : descripteur fermé
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
                            *[("JOURNAL/reserve", lambda t=t: jl.ecrire(t, WS + 120)) for t in (
                                "ouverture", "marqueur", "point", "cloture", "reprise", "trou")],   # FORMAT §2
                            ("JOURNAL/reserve", lambda: jl.ecrire("lecture", WS + 120, seq=9)),
                            ("JOURNAL/reserve", lambda: jl.ecrire("lecture", WS + 120, prec="0")),    # C-5 (G-13)
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

    def test_refus_nommes_a_l_ouverture(self):                          # C-5 : G-03, G-04, G-05
        with open(os.path.join(self.d, "vide-2026-10-04-0.jsonl"), "wb") as f:
            f.write(b'{"jour":')                                # aucun enregistrement intègre
        for code, appel in (("JOURNAL/grille", lambda: j.Journal(self.d, "pool", w=7)),
                            ("JOURNAL/fenetre", lambda: self.journal(WS + 1)),
                            ("JOURNAL/illisible", lambda: self.journal(prefixe="vide"))):
            with self.subTest(code=code):
                with self.assertRaises(j.ErreurJournal) as e:
                    appel()
                self.assertEqual(e.exception.code, code)

    def test_structure_cyclique_refusee_en_temps_borne(self):          # C-3 (sonde S-7 de la G2)
        boucle, partage, res, avant = [], [1], [], []
        boucle.append(boucle)

        def essai():                                              # ouvert dans le fil qui écrit (CB-18a)
            jl = self.journal()
            avant.append(self.etat())
            res.append(code(lambda: jl.ecrire("lecture", WS + 60, c=boucle)))      # refus attendu : nommé
            res.append(code(lambda: jl.ecrire("lecture", WS + 60, c=imbrique(70, boucle))))   # cycle avant C-4
        t = threading.Thread(target=essai, daemon=True)          # une boucle sans fin pendrait le fil, pas la suite
        t.start()
        t.join(5)
        self.assertEqual((res, [self.etat()]), (["JOURNAL/type"] * 2, avant))
        self.assertEqual(j.canonique({"a": partage, "b": partage}), b'{"a":[1],"b":[1]}\n')   # partage sans cycle

    def test_entiers_de_640_chiffres_au_plus(self):                    # SHOGEN-S2BIS-ENTIER-ECRIVAIN-1 (I-1)
        """640 chiffres, signe non compté, plus petite limite non nulle de conversion des entiers de l'interpréteur :
        admis, et relus intègres ; 641 : refus JOURNAL/entier sans rien écrire, à toute profondeur et dans tout
        conteneur (tuple compris, écrit en liste JSON : MR-09 de la G2 de la tranche C), quel que soit le réglage de
        l'interpréteur (limite abaissée à 640, ou levée) et au-delà de sa limite par défaut (FORMAT §1.2)."""
        self.assertEqual(sys.int_info.str_digits_check_threshold, 640)
        jl, grand, refus = self.journal(), 10 ** 640, []                # grand : 641 chiffres
        for x in (grand - 1, -(grand - 1), [grand - 1], {"y": {"z": 1 - grand}}, (0, grand - 1)):
            jl.ecrire("lecture", WS + 60, x=x)
        avant, ancien = self.etat(), sys.get_int_max_str_digits()
        for x in (grand, -grand, [1, [grand]], {"y": {"z": grand}}, 10 ** 5000, (0, grand), [(grand,)]):
            refus.append(code(lambda: jl.ecrire("lecture", WS + 60, x=x)))
        for limite in (640, 0):
            sys.set_int_max_str_digits(limite)
            try:
                refus.append(code(lambda: jl.ecrire("lecture", WS + 60, x=grand)))
            finally:
                sys.set_int_max_str_digits(ancien)
        self.assertEqual((refus, self.etat()), (["JOURNAL/entier"] * 9, avant))
        jl.marqueur(WS + 60)
        jl.fermer()
        self.journal(WS + 120).fermer()                                 # lignes de 640 chiffres relues intègres
        dernier = chaine(self.etat()[FICHIER])[2][-1]
        self.assertEqual((dernier["type"], dernier["queue"]), ("reprise", None))

    def test_imbrication_de_64_niveaux_au_plus(self):                  # CB-18n, lettre C-4 du FORMAT (§8.3)
        """Niveau : 1 pour l'objet de la ligne, n + 1 dans un conteneur de niveau n. Tous les conteneurs au niveau 64
        au plus : écrit, puis relu intègre ; un conteneur au niveau 65 : refus JOURNAL/imbrication sans rien écrire.
        Une liste partagée compte à sa plus grande profondeur, qu'elle soit vue d'abord par le chemin court ou par le
        long (64 et 65 niveaux par ce chemin)."""
        s = imbrique(10)                                    # s au niveau L : sa liste la plus profonde au niveau L + 9
        jl, refus = self.journal(), []
        for x in (imbrique(63), imbrique(62, {}), {"a": s, "b": imbrique(52, s)}, {"b": imbrique(52, s), "a": s}):
            jl.ecrire("lecture", WS + 60, x=x)
        avant = self.etat()
        for x in (imbrique(64), imbrique(63, {}), {"a": s, "b": imbrique(53, s)}, {"b": imbrique(53, s), "a": s}):
            refus.append(code(lambda: jl.ecrire("lecture", WS + 60, x=x)))
        self.assertEqual((refus, self.etat()), (["JOURNAL/imbrication"] * 4, avant))
        jl.marqueur(WS + 60)
        jl.fermer()
        self.journal(WS + 120).fermer()                                 # lignes de 64 niveaux relues intègres
        dernier = chaine(self.etat()[FICHIER])[2][-1]
        self.assertEqual((dernier["type"], dernier["queue"]), ("reprise", None))

    def test_garde_d_un_seul_fil(self):                                 # CB-18a, ECRIVAIN-USAGE-1
        """Le fil qui ouvre l'écrivain est le seul qui écrive : `ecrire` et `marqueur` appelés d'un autre fil sont
        refusés (JOURNAL/fil) sans rien écrire ; le fil propriétaire écrit ensuite."""
        jl, codes = self.journal(), []
        avant = self.etat()
        t = threading.Thread(target=lambda: codes.extend(code(a) for a in (
            lambda: jl.ecrire("lecture", WS + 60, k=1), lambda: jl.marqueur(WS + 60))), daemon=True)
        t.start()
        t.join(5)
        self.assertEqual((codes, self.etat()), (["JOURNAL/fil", "JOURNAL/fil"], avant))
        jl.marqueur(WS + 60)
        self.assertEqual([e["type"] for e in chaine(self.etat()[FICHIER])[2]], ["ouverture", "marqueur", "point"])

    def test_refus_nommes_ecrivain_neuf_ferme_ou_deja_ouvert(self):    # CB-18a, ECRIVAIN-USAGE-1 (I-C2)
        """Écriture avant `ouvrir` ou après `fermer`, ouverture d'un écrivain fermé : JOURNAL/ferme ; second `ouvrir` :
        JOURNAL/ouvert, et l'écrivain écrit encore (verrou et fichier intacts) ; une ouverture refusée ferme l'écrivain
        et rend le verrou. Aucun refus n'écrit."""
        neuf, jl = j.Journal(self.d, "pool"), self.journal()
        avant = self.etat()
        self.assertEqual([code(lambda: neuf.ecrire("lecture", WS + 60)), code(lambda: neuf.marqueur(WS + 60)),
                          code(lambda: jl.ouvrir(WS))], ["JOURNAL/ferme", "JOURNAL/ferme", "JOURNAL/ouvert"])
        self.assertEqual(self.etat(), avant)
        jl.marqueur(WS + 60)                                    # écrivain intact après le second `ouvrir`
        jl.fermer()
        apres = self.etat()
        self.assertEqual([code(lambda: jl.ecrire("lecture", WS + 120)), code(lambda: jl.marqueur(WS + 120)),
                          code(lambda: jl.ouvrir(WS + 120))], ["JOURNAL/ferme"] * 3)
        refuse = j.Journal(self.d, "pool")
        self.assertEqual((code(lambda: refuse.ouvrir(WS + 1)), code(lambda: refuse.ouvrir(WS + 120)), self.etat()),
                         ("JOURNAL/fenetre", "JOURNAL/ferme", apres))
        with open(os.path.join(self.d, "pool.verrou"), "rb") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)        # verrou rendu par l'ouverture refusée

    def test_terminal_sur_toute_methode_publique_d_ecriture(self):     # CB-18a, ECRIVAIN-USAGE-1 (I-C3)
        """Contrôle mécanique : les méthodes publiques de `Journal` sont `ouvrir`, `ecrire`, `marqueur` et `fermer` ;
        les trois premières portent la garde `_terminal` (C-2 et refus de CB-18a) ; `fermer`, nettoyage admis de tout
        fil et après une casse, ne la porte pas. Une méthode publique ajoutée sans la garde fait échouer ce test."""
        publiques = [n for n in dir(j.Journal) if not n.startswith("_") and callable(getattr(j.Journal, n))]
        self.assertEqual({n: getattr(getattr(j.Journal, n), "terminal", False) for n in publiques},
                         {"ouvrir": True, "ecrire": True, "marqueur": True, "fermer": False})
