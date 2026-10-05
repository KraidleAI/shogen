"""CB-3, E-C-03 à E-C-05 : lecture par phases sur serveurs factices de boucle locale, résolveur injecté. CB-11e (C-4 de
la G2 de P1-B) : délais sur l'horloge monotone, horloge murale reculée pendant une lecture. CB-11g (C-3) : contexte TLS
d'urllib (attributs et ClientHello écrit en mémoire, sans réseau), chemin TLS réussi par une couche injectée ; MG-31.
CB-18b (limite E-4 levée) : le délai court depuis le départ monotone que la boucle porte dans le suivi. CB-19e (C-3 (b)
de la relecture d'intégration de P1) : adresse posée au suivi avant la phase `dns` (suivi espion)."""
import contextlib
import socket
import ssl
import struct
import threading
import time
import unittest

from shogen_s2bis.collecte import http
from shogen_s2bis.collecte.lecture import S, horloge, monotone
from tests.test_http import CORPS, OK7, REQUETE


def servir(comportement):
    """Serveur d'une connexion sur 127.0.0.1, servie par `comportement(conn, recues)` ; rend (port, recues, fil)."""
    srv, recues = socket.create_server(("127.0.0.1", 0)), []

    def fil():
        with srv:
            srv.settimeout(10)
            try:
                with srv.accept()[0] as conn:
                    conn.settimeout(10)
                    comportement(conn, recues)
            except OSError:                                         # aucun client, ou client parti : fin du service
                pass
    t = threading.Thread(target=fil, daemon=True)
    t.start()
    return srv.getsockname()[1], recues, t


def repondre(octets, rst=False, pas=0):
    """Lit la requête (jusqu'à la ligne vide), envoie `octets` (un octet toutes les `pas` s si `pas`), RST si `rst`."""
    def comportement(conn, recues):
        recu = b""
        while b"\r\n\r\n" not in recu and (bloc := conn.recv(4096)):
            recu += bloc
        recues.append(recu)
        for morceau in [octets[i:i + 1] for i in range(len(octets))] if pas else [octets]:
            time.sleep(pas)
            conn.sendall(morceau)
        if rst:                                                     # SO_LINGER nul : la fermeture envoie un RST
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    return comportement


class Resolveur:
    """getaddrinfo injecté : note ses arguments, attend, lève `erreur`, ou rend 127.0.0.1:`port` puis 127.0.0.2:1."""
    def __init__(self, port, erreur=None, pause=0):
        self.port, self.erreur, self.pause, self.appels = port, erreur, pause, []

    def __call__(self, *args):
        self.appels.append(args)
        time.sleep(self.pause)
        if self.erreur:
            raise self.erreur
        a = (socket.AF_INET, socket.SOCK_STREAM, 6, "")
        return [] if self.port is None else [(*a, ("127.0.0.1", self.port)), (*a, ("127.0.0.2", 1))]


class Recul:
    """Horloge murale injectée (C-4) : l'heure réelle, reculée de `recul` µs passé `apres` µs après le premier appel."""
    def __init__(self, recul, apres):
        self.recul, self.apres, self.t0 = recul, apres, None

    def __call__(self):
        t = horloge()
        self.t0 = t if self.t0 is None else self.t0
        return t - self.recul if t - self.t0 > self.apres else t


def hello(contexte, nom="api.example"):
    """ClientHello que `contexte` écrit en mémoire (MemoryBIO), sans socket ni réseau."""
    sortie = ssl.MemoryBIO()
    tls = contexte.wrap_bio(ssl.MemoryBIO(), sortie, server_hostname=nom)
    with contextlib.suppress(ssl.SSLWantReadError):
        tls.do_handshake()
    return sortie.read()


def extensions(h):
    """{type : données} des extensions d'un ClientHello (RFC 8446 §4.1.2), lues à la main."""
    i = 5 + 4 + 2 + 32                                              # enregistrement, poignée, version, aléa
    i += 1 + h[i]                                                   # identifiant de session
    i += 2 + int.from_bytes(h[i:i + 2], "big")                      # suites de chiffrement
    i += 1 + h[i]                                                   # méthodes de compression
    fin, i, ext = i + 2 + int.from_bytes(h[i:i + 2], "big"), i + 2, {}
    while i < fin:
        n = int.from_bytes(h[i + 2:i + 4], "big")
        ext[int.from_bytes(h[i:i + 2], "big")] = h[i + 4:i + 4 + n]
        i += 4 + n
    return ext


class TlsNote:
    """Couche TLS injectée (C-3) : note `server_hostname` et chaque poignée, puis laisse passer le flux en clair."""
    def __init__(self):
        self.noms, self.poignees = [], 0

    def wrap_socket(self, s, server_hostname=None, do_handshake_on_connect=True):
        self.noms.append((server_hostname, do_handshake_on_connect))
        note = self

        class Couche:
            def __getattr__(self, nom):
                return getattr(s, nom)

            def do_handshake(self):
                note.poignees += 1
        return Couche()


class Client(unittest.TestCase):
    def lire(self, comportement, req=http.Requete("api.example", "/v1/btc?x=1"), **k):
        port, recues, fil = servir(comportement)
        self.res = Resolveur(port)
        lu = http.lire(req, resoudre=self.res, **{"delai": 2 * S, "tls": None, **k})
        fil.join(10)
        return lu, recues, port

    def test_reponse_200_phases_ipv4(self):
        lu, recues, port = self.lire(repondre(OK7))
        self.assertEqual((lu.statut, lu.sous_type, lu.code, lu.octets, lu.adresse, recues),
                         ("ok", None, 200, CORPS, f"127.0.0.1:{port}", [REQUETE]))
        self.assertEqual(self.res.appels, [("api.example", 443, socket.AF_INET, socket.SOCK_STREAM)])
        instants = [lu.depart, *(lu.phases[p] for p in ("dns", "connexion", "requete", "corps")), lu.fin]
        self.assertEqual((sorted(lu.phases), sorted(instants)), (["connexion", "corps", "dns", "requete"], instants))

    def test_codes_http(self):
        for code in (301, 403, 429, 451):
            with self.subTest(code=code):
                lu = self.lire(repondre(b"HTTP/1.1 %d Refus\r\nContent-Length: 2\r\n\r\nno" % code))[0]
                self.assertEqual((lu.statut, lu.sous_type, lu.code, lu.octets), ("panne_http", None, code, b"no"))

    def test_corps_coupe_ou_reponse_vide(self):                      # essai 1 de la PROPOSITION (§9), en réel
        tete = b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n0123456789"
        for comportement in (repondre(tete, rst=True), repondre(tete), repondre(b"")):
            with self.subTest(comportement=comportement):
                lu = self.lire(comportement)[0]
                self.assertEqual((lu.statut, lu.sous_type, lu.code, "requete" in lu.phases),
                                 ("panne_transport", "coupure", None, True))

    def test_resolution_en_echec_vide_ou_trop_lente(self):
        for res in (Resolveur(1, socket.gaierror(-2, "Name or service not known")), Resolveur(None),
                    Resolveur(1, pause=0.3)):
            with self.subTest(erreur=res.erreur, pause=res.pause):
                lu = http.lire(http.Requete("api.example", "/"), resoudre=res, tls=None, delai=S // 5)
                self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases)),
                                 ("panne_transport", "dns", ["dns"] if res.pause else []))

    def test_connexion_refusee(self):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]                               # port rendu : rien n'y écoute
        lu = http.lire(http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=2 * S)
        self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases), lu.adresse),
                         ("panne_transport", "connexion", ["dns"], f"127.0.0.1:{port}"))

    def test_poignee_tls_refusee_ou_sans_reponse(self):
        def charabia(conn, recues):
            recues.append(conn.recv(4096))                          # ClientHello
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")

        def muet(conn, recues):
            recues.append(conn.recv(4096))
            conn.recv(4096)                                         # jusqu'à la fermeture par le client
        for comportement, sous_type in ((charabia, "tls"), (muet, "delai")):
            with self.subTest(sous_type=sous_type):
                lu, recues, _p = self.lire(comportement, tls=ssl.create_default_context(), delai=S // 2)
                self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases), recues[0][:1]),
                                 ("panne_transport", sous_type, ["connexion", "dns"], b"\x16"))

    def test_attrape_tout_et_requete_refusee_avant_tout_reseau(self):
        class TlsCasse:
            def wrap_socket(self, *a, **k):
                raise RuntimeError("défaut imprévu")
        lu, recues, _p = self.lire(repondre(b""), tls=TlsCasse())
        self.assertEqual((lu.statut, lu.sous_type, recues), ("panne_transport", "autre", [b""]))
        res = Resolveur(1)
        lu = http.lire(http.Requete("api.example", "/x\r\nX-Injecte: 1"), resoudre=res, tls=None)
        self.assertEqual((lu.statut, lu.sous_type, lu.phases, res.appels), ("panne_transport", "autre", {}, []))

    def test_delai_epuise_entre_deux_phases(self):
        instants = iter([0, 0, 0, S])             # horloge monotone : début, dns, reste avant connexion, avant envoi
        lu = self.lire(repondre(OK7), monotone=lambda: next(instants, S), delai=S)[0]
        self.assertEqual((lu.sous_type, sorted(lu.phases)), ("delai", ["connexion", "dns"]))   # statut contrôlé

    def test_depart_pose_par_la_boucle_et_suivi(self):
        """CB-18b (SOMMEIL-MURAL-1, limite E-4 levée) : le délai court depuis le départ que la boucle porte dans le
        suivi sur l'horloge monotone (`monotone`), jamais depuis l'horloge murale (`depart`) : départ monotone 1 s
        avant, délai de 1 s épuisé dès la résolution (`dns`) ; départ mural 5 s avant, départ monotone présent : le
        délai court encore, la connexion est tentée (port fermé : `connexion`)."""
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]                               # port rendu : rien n'y écoute
        for mono, mural, attendu in ((monotone() - S, horloge(), "dns"), (monotone(), horloge() - 5 * S, "connexion")):
            suivi = {"depart": mural, "monotone": mono}
            lu = http.lire(http.Requete("api.example", "/"), suivi, resoudre=Resolveur(port), tls=None, delai=S)
            with self.subTest(attendu=attendu):
                self.assertEqual((lu.statut, lu.sous_type, lu.depart, sorted(suivi)),
                                 ("panne_transport", attendu, mural, ["adresse", "depart", "monotone", "phases"]))

    def test_adresse_posee_au_suivi_avant_la_phase_dns(self):     # CB-19e, C-3 (b) de la relecture d'intégration
        """La boucle relève `phases`, puis `adresse` ; le client pose donc l'adresse au suivi avant la phase `dns`
        (sinon un relevé entre les deux lit une phase `dns` sans adresse). Suivi espion : à l'écriture de chaque
        phase, l'adresse est-elle déjà au suivi ? Port fermé : une seule phase, `dns`."""
        class Phases(dict):
            def __setitem__(self, cle, valeur):
                vues.append((cle, "adresse" in suivi))
                super().__setitem__(cle, valeur)
        vues, suivi = [], {"phases": Phases()}
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]                               # port rendu : rien n'y écoute
        lu = http.lire(http.Requete("api.example", "/"), suivi, resoudre=Resolveur(port), tls=None, delai=S)
        self.assertEqual((vues, lu.sous_type, lu.adresse), ([("dns", True)], "connexion", f"127.0.0.1:{port}"))

    def test_delai_sur_l_horloge_monotone_malgre_un_recul(self):
        """C-4 (S-C1 de la G2) : l'horloge murale recule de 3 s, 0,1 s après le départ d'une lecture servie octet par
        octet ; le délai global de 0,3 s, compté sur l'horloge monotone, tient ; les instants restent ceux de l'horloge
        murale (la fin, reculée, précède le départ)."""
        port, _r, fil = servir(repondre(b"HTTP/1.1 200 OK\r\nX-Long: " + b"a" * 100, pas=0.02))
        t = time.monotonic()
        lu = http.lire(http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=3 * S // 10,
                       horloge=Recul(3 * S, S // 10))
        duree = time.monotonic() - t
        fil.join(10)
        self.assertEqual((lu.statut, lu.sous_type), ("panne_transport", "delai"))
        self.assertTrue(0.3 <= duree < 1, duree)
        self.assertLess(lu.fin, lu.depart)

    def test_depart_pose_apres_le_debut_ne_prolonge_pas_le_delai(self):
        """C-4, CB-18b : `depart` posé 5 s après le début de la lecture (horloge murale reculée entre la boucle et le
        fil), sans départ monotone : le délai de 0,2 s court depuis le début de la lecture, l'horloge murale n'y entre
        pas."""
        def muet(conn, recues):
            conn.recv(4096)
            conn.recv(4096)                                         # jusqu'à la fermeture par le client
        port, _r, fil = servir(muet)
        t = time.monotonic()
        lu = http.lire(http.Requete("api.example", "/"), {"depart": horloge() + 5 * S}, resoudre=Resolveur(port),
                       tls=None, delai=S // 5)
        duree = time.monotonic() - t
        fil.join(10)
        self.assertEqual((lu.statut, lu.sous_type), ("panne_transport", "delai"))
        self.assertLess(duree, 1)

    def test_contexte_tls_d_urllib(self):
        """C-3 : CONTEXTE vérifie le certificat et le nom d'hôte, et annonce, comme le contexte d'urllib en S2, l'ALPN
        `http/1.1` (RFC 7301 §3.1 : liste de 9 octets, nom de 8) et l'authentification après poignée (RFC 8446
        §4.2 (numéro 49), §4.2.6 (données vides)) ; le nom de la requête part en SNI."""
        ext = extensions(hello(http.CONTEXTE))
        self.assertEqual((http.CONTEXTE.verify_mode, http.CONTEXTE.check_hostname), (ssl.CERT_REQUIRED, True))
        self.assertEqual((ext.get(16), ext.get(49), ext[0][5:]), (bytes([0, 9, 8]) + b"http/1.1", b"", b"api.example"))

    def test_poignee_tls_reussie_couche_injectee(self):
        """C-3 : chemin réussi par une couche TLS injectée : nom d'hôte de la requête en `server_hostname`, jamais
        l'adresse (MG-01) ; poignée faite à part, une fois ; phase `tls` entre `connexion` et `requete`."""
        tls = TlsNote()
        lu, recues, _p = self.lire(repondre(OK7), tls=tls)
        self.assertEqual((lu.statut, lu.code, lu.octets, recues, tls.noms, tls.poignees),
                         ("ok", 200, CORPS, [REQUETE], [("api.example", False)], 1))
        self.assertTrue(lu.phases["connexion"] <= lu.phases["tls"] <= lu.phases["requete"], lu.phases)

    def test_connexion_sans_reponse_close_au_delai(self):
        """MG-31 : une connexion qui ne s'établit pas (file d'attente d'écoute pleine : les SYN restent sans réponse)
        est close au délai, sous-type `delai` ; la lecture tourne dans un fil joint en 5 s."""
        with socket.socket() as srv:
            srv.bind(("127.0.0.1", 0))
            srv.listen(0)
            port, pleins, lus = srv.getsockname()[1], [socket.socket() for _ in range(3)], []
            for c in pleins:
                self.addCleanup(c.close)
                c.setblocking(False)
                c.connect_ex(("127.0.0.1", port))
            time.sleep(0.2)                                         # la file d'attente se remplit
            fil = threading.Thread(target=lambda: lus.append(http.lire(
                http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=S // 5)), daemon=True)
            fil.start()
            fil.join(5)
            self.assertFalse(fil.is_alive(), "la connexion pend")
        self.assertEqual((lus[0].statut, lus[0].sous_type, sorted(lus[0].phases)),
                         ("panne_transport", "delai", ["dns"]))
