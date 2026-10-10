"""CB-12b (E-C-30 ; ADR-0029 l.79-80, l.247 ; PROPOSITION §2.1) : relevé ASN d'un hôte par le résolveur de
l'observateur (client DNS de CB-10), RIPEstat (client HTTP de CB-3) et Team Cymru (TXT). Serveurs factices de boucle
locale ; messages DNS écrits à la main (RFC 1035 §4.1, nom en pointeur c00c) ; corps RIPEstat synthétique, de la
forme que lit S2 (r2.py l.275-289, [2nd] : aucune capture, aucun réseau), AS de documentation 64500 (RFC 5398),
préfixe 192.0.2.0/24 (RFC 5737)."""
import json
import socket
import struct
import threading

from shogen_s2bis.collecte import asn, dns, http, journal
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_dns import Q_A
from tests.test_http_reseau import Resolveur, repondre, servir
from tests.test_journal import FICHIER, WS, Base

CRLF, WE = bytes([13, 10]), "witness.example."
CORPS = json.dumps({"data": {"asns": [{"asn": 64500, "holder": "EXEMPLE-AS - documentation"}],
                             "resource": "192.0.2.0/24"}, "status": "ok"}).encode()
TXT = b"64500 | 192.0.2.0/24 | ZZ | test | 2026-10-08"
V = {"asn": 64500, "detenteur": "EXEMPLE-AS - documentation", "prefixe": "192.0.2.0/24"}
ARABE = "".join(map(chr, (0x661, 0x663, 0x663, 0x663, 0x665)))           # 13335 en chiffres arabes-indiens (L-A1)


def reponse(requete, rrs, drapeaux=0x8180):
    """Réponse à `requete` : même identifiant et question, `rrs` [(type, données)], nom en pointeur c00c, TTL 60."""
    return (requete[:2] + struct.pack(">5H", drapeaux, 1, len(rrs), 0, 0) + requete[12:] +
            b"".join(struct.pack(">HHHIH", 0xC00C, t, 1, 60, len(d)) + d for t, d in rrs))


def serveur_dns(test, a=((1, bytes([192, 0, 2, 1])), (1, bytes([192, 0, 2, 2]))), txt=(TXT,), drapeaux=0x8180):
    """Serveur UDP de boucle locale : A, réponses `a` sous `drapeaux` ; TXT, chaînes `txt` ; rend (port, requêtes)."""
    srv, recues = socket.socket(socket.AF_INET, socket.SOCK_DGRAM), []
    srv.bind(("127.0.0.1", 0))
    test.addCleanup(srv.close)

    def fil():
        while True:
            try:
                m, client = srv.recvfrom(4096)
            except OSError:                                         # serveur fermé à la fin du test
                return
            recues.append(m)
            un_a = struct.unpack(">H", m[-4:-2])[0] == 1
            rrs = [(16, bytes([len(x)]) + x) for x in txt]
            srv.sendto(reponse(m, a, drapeaux) if un_a else reponse(m, rrs), client)
    threading.Thread(target=fil, daemon=True).start()
    return srv.getsockname()[1], recues


def releve(test, corps=CORPS, code=200, hote=WE, **dns_):
    port, recues = serveur_dns(test, **dns_)
    hport, requetes, fil = servir(repondre(b"HTTP/1.1 %d X" % code + CRLF + b"Content-Length: %d" % len(corps) + CRLF
                                           + CRLF + corps))
    r = asn.releve(hote, "127.0.0.1", lire=lambda req: http.lire(req, tls=None, resoudre=Resolveur(hport)),
                   interroger=lambda a, n, t: dns.interroger(a, n, t, delai=S // 2, port=port))
    return r, recues, requetes


class Releve(Base):
    def test_releve_complet_par_le_resolveur_de_l_observateur(self):
        """A de l'hôte, puis RIPEstat sur la première adresse, puis TXT de 1.2.0.192.origin.asn.cymru.com au même
        résolveur ; chaque partie journalisée à part, valeurs brutes et décodées."""
        r, recues, requetes = releve(self)
        cymru = b"".join(bytes([len(x)]) + x for x in (b"1", b"2", b"0", b"192", b"origin", b"asn", b"cymru", b"com"))
        self.assertEqual([m[12:] for m in recues], [Q_A[12:], cymru + bytes([0, 0, 16, 0, 1])])
        self.assertEqual((sorted(r), r["hote"], r["ip"], r["a"]["statut"], [x[3] for x in r["a"]["reponses"]]),
                         (["a", "cymru", "hote", "ip", "ripestat"], WE, "192.0.2.1", "reponse", ["192.0.2.1",
                                                                                                "192.0.2.2"]))
        self.assertEqual(requetes[0].split(CRLF)[0], b"GET /data/prefix-overview/data.json?resource=192.0.2.1 HTTP/1.1")
        self.assertEqual((r["ripestat"]["statut"], r["ripestat"]["code"], r["ripestat"]["valeurs"]), ("ok", 200, V))
        self.assertEqual((r["cymru"]["statut"], r["cymru"]["asn"], r["cymru"]["reponses"][0][3]), ("reponse", 64500,
                                                                                                   [TXT.decode()]))

    def test_echecs_types_sans_jugement(self):
        """NXDOMAIN, CNAME seul, drapeau TC : pas d'adresse, RIPEstat et Cymru non interrogés (null) ; RIPEstat en 503
        ou illisible, TXT illisible : statut typé, l'autre base relevée quand même."""
        cas = {"nx": dict(a=(), drapeaux=0x8183), "cname": dict(a=((5, bytes([0])),)), "tc": dict(drapeaux=0x8380)}
        for nom, d in cas.items():
            r, recues, _q = releve(self, **d)
            with self.subTest(cas=nom):
                self.assertEqual((r["ip"], r["ripestat"], r["cymru"], len(recues)), (None, None, None, 1))
        r1, _r, _q = releve(self, code=503, txt=(b"abc | x",))
        r2, _r, _q = releve(self, corps=b"<html>", a=((5, bytes([0])), (1, bytes([192, 0, 2, 7]))))   # CNAME, puis A
        self.assertEqual((r1["ip"], r2["ip"]), ("192.0.2.1", "192.0.2.7"))
        self.assertEqual([(r["ripestat"]["statut"], r["ripestat"]["code"], r["ripestat"]["valeurs"], r["cymru"]["asn"])
                          for r in (r1, r2)], [("panne_http", 503, None, None), ("panne_decode", 200, None, 64500)])

    def test_hote_ipv4_litterale_releve_directement(self):    # DT6-f, SHOGEN-S2BIS-ASN-HOTE-IPV4-1 (O-6 de P2A)
        """Un hôte écrit en IPv4 littérale canonique est relevé directement : aucune requête A (la lecture le contacte
        sans résolution), `a` null, `ip` l'hôte, RIPEstat sur lui, TXT de 7.2.0.192.origin.asn.cymru.com ; écrit
        autrement (zéros de tête), c'est un nom : requête A d'abord, adresse du résolveur."""
        r, recues, requetes = releve(self, hote="192.0.2.7")
        cymru = b"".join(bytes([len(x)]) + x for x in (b"7", b"2", b"0", b"192", b"origin", b"asn", b"cymru", b"com"))
        self.assertEqual(([m[12:] for m in recues], r["a"], r["ip"], requetes[0].split(CRLF)[0],
                          r["ripestat"]["valeurs"], r["cymru"]["asn"]),
                         ([cymru + bytes([0, 0, 16, 0, 1])], None, "192.0.2.7",
                          b"GET /data/prefix-overview/data.json?resource=192.0.2.7 HTTP/1.1", V, 64500))
        r, recues, _q = releve(self, hote="192.0.2.007")
        self.assertEqual((struct.unpack(">H", recues[0][-4:-2])[0], r["a"]["statut"], r["ip"]),
                         (1, "reponse", "192.0.2.1"))


class Decodage(Base):
    def test_ripestat_forme_de_s2_bornes_et_base_muette(self):
        """Forme de S2 ; `asn` entier, ou texte de chiffres ASCII seuls (DT6-f, SHOGEN-S2BIS-ASN-LECTURE-1 : `int()`
        de S2 admettait souligné, signe, blancs et chiffres arabes-indiens, mesuré par la G2 de P2A, L-A1 et L-A2)."""
        def v(d):
            try:
                return asn.ripestat(json.dumps({"data": d}).encode())
            except Exception:
                return "refus"
        ok = {"asns": [{"asn": 64500, "holder": V["detenteur"]}], "resource": "192.0.2.0/24"}
        cas = [(ok, V), ({**ok, "asns": []}, {**V, "asn": None, "detenteur": None}),
               ({**ok, "asns": [{"asn": "64500"}]}, {**V, "detenteur": None}),
               ({**ok, "asns": [{"asn": 0}]}, {**V, "asn": 0, "detenteur": None})]                  # C-2 (G14) : AS 0
        cas += [({**ok, "asns": [{"asn": x}]}, "refus") for x in (True, -1, 1 << 32, 64500.0)]
        cas += [({**ok, "asns": [{"asn": x}]}, "refus")                     # DT6-f : ASN-LECTURE-1, chiffres ASCII
                for x in ("13_335", "+13335", "-0", " 13335", "13335 ", ARABE, "4294967296", "")]
        cas += [({**ok, "resource": 5}, "refus"), ({**ok, "asns": [{"asn": 1, "holder": "x" * 4096}]}, "refus"),
                ({**ok, "asns": [{"asn": 64500, "holder": V["detenteur"]}, {"asn": 64501, "holder": "B"}]}, V)]
        self.assertEqual([v(d) for d, _a in cas], [a for _d, a in cas])
        self.assertEqual(asn.ripestat(json.dumps({"data": {**ok, "asns": [{"asn": (1 << 32) - 1}]}}).encode())["asn"],
                         (1 << 32) - 1)

    def test_cymru_premier_txt_lisible_forme_de_s2(self):
        def c(*chaines, t=16):
            return asn.cymru({"reponses": [[WE, t, 60, [x]] for x in chaines]})
        self.assertEqual([c("64500 | x"), c("64500 64501 | x"), c("abc | x", "64501 | y"), c("4294967296 | x"),
                          c("64500 | x", t=1), asn.cymru({"reponses": None}), asn.cymru({"reponses": [
                              [WE, 5, 60, None], [WE, 16, 60, []], [WE, 16, 60, ["64502 | z"]]]}), c("0 | x"),
                          asn.cymru({"reponses": [[WE, 16, 60, ["64500 | x", "64501 | y"]]]})],     # C-2 : G14, G17
                         [64500, 64500, 64501, None, None, None, 64502, 0, 64500])     # CNAME, TXT vide, puis TXT
        self.assertEqual([c(x + " | y") for x in ("+13335", "1_3335", ARABE, " 13335", "-0")],
                         [None, None, None, 13335, None])                                    # DT6-f, ASN-LECTURE-1

    def test_plus_grand_releve_sous_limite(self):
        """Témoin : A et TXT au plus grand résultat du FORMAT §13.6 (14 réponses SOA, noms de 1 024 caractères de
        contrôle), RIPEstat de 1 048 576 octets et valeurs à leur borne, hôte de 253 caractères : sous LIMITE."""
        nom = chr(1) * 2 * dns.UDP
        r = {"debut": 10 ** 16, "fin": 10 ** 16, "rcode": None, "statut": "reponse", "tc": False,
             "reponses": [[nom, 65535, 2 ** 32 - 1, [nom, nom, *[2 ** 32 - 1] * 5]]] * 14}
        n = asn.VALEURS - len(json.dumps({"asn": 1, "detenteur": "", "prefixe": ""}, separators=(",", ":"))) - 1
        lu = Lecture("ok", 10 ** 16, 10 ** 16, octets=bytes(1 << 20), valeurs={"asn": 1, "detenteur": "a" * n,
                                                                               "prefixe": ""}, code=200)
        champs = {"hote": "h" * 253, "a": r, "ip": "255.255.255.255", "ripestat": lu.enregistrement(),
                  "cymru": {**r, "asn": 2 ** 32 - 1}}
        self.assertEqual(len(journal.canonique(lu.valeurs)), asn.VALEURS)
        self.journal().ecrire("asn", WS + 60, **champs)
        self.assertLess(len(self.etat()[FICHIER].split(bytes([10]))[1]), 2000000)
