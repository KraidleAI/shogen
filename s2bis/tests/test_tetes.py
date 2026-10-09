"""CB-15a, E-C-36 : requête RFC 3161 construite en bibliothèque standard, statut d'une réponse, manifeste des têtes.
Octets de référence produits hors du code (journal G1 de CB-15a) : `openssl ts -query -data <fichier> -sha256 -cert
-no_nonce` (OpenSSL 3.0.13, PROPOSITION §2.4 « Jeton »), puis la même commande avec nonce, dont la valeur est lue par
`openssl ts -query -in … -text` ; entiers et longueurs DER par `openssl asn1parse` ; réponse de rejet produite par
`openssl ts -reply` d'une TSA jetable (clés détruites) ; autres réponses écrites à la main d'après RFC 3161 §2.4.2
(forme DER des longueurs : X.690, non détenue) ; manifeste écrit à la main."""
import unittest

from shogen_s2bis.collecte import tetes

EMPREINTE = bytes.fromhex("7527d85120a51adc70645317ff05c72f6ad103fa864f3d74b9be3ff1beeba2f0")   # sha256 du fichier
SANS_NONCE = ("30390201013031300d0609608648016503040201050004207527d85120a51adc70645317ff05c72f6ad103fa864f3d74b9be3ff1"
              "beeba2f00101ff")                                             # de 18 octets « manifeste de test\n »
AVEC_NONCE = {0xDA4C619F927CC9E7: "3044020101" + SANS_NONCE[10:-6] + "020900da4c619f927cc9e70101ff",
              0x02510A27C1EDD5E4: "3043020101" + SANS_NONCE[10:-6] + "020802510a27c1edd5e40101ff"}
ENTIERS = {0: "020100", 1: "020101", 127: "02017f", 128: "02020080", 255: "020200ff", 256: "02020100",
           1 << 63: "0209008000000000000000", (1 << 64) - 1: "020900ffffffffffffffff"}
REJET = ("30373035020102302c0c2a4d6573736167652064696765737420616c676f726974686d206973206e6f7420737570706f727465642e"
         "03020780")                                                      # openssl ts -reply, sha1 refusé (badAlg)
JETON = "30820101" + "00" * 257                                         # jeton factice : SEQUENCE de 257 octets
MAL_FORMEES = {"accordée sans jeton": "30053003020100", "rejet avec jeton": "3082010a3003020102" + JETON,
               "statut 6": "30053003020106", "statut négatif": "300530030201ff", "octet de trop": REJET + "00",
               "tronquée": REJET[:-2], "statut sur deux octets": "3082010b300402020000" + JETON,
               "SET au lieu de SEQUENCE": "3082010a3103020100" + JETON, "statut hors INTEGER": "30053003040102",
               "jeton hors SEQUENCE": "3082010a3003020100" + "31" + JETON[2:],
               "jeton qui ne finit pas la réponse": "3082010b3003020100" + JETON + "00",
               "réponse en SET": "31053003020102", "longueur longue sous 128": "3081053003020102",
               "longueur à zéro de tête": "308200053003020102", "vide": "", "un octet": "30",
               "statut tronqué": "300430020201"}


def code(appel):
    try:
        appel()
    except tetes.RefusJeton as e:
        return e.code
    return None


class Requete(unittest.TestCase):
    def test_requete_egale_aux_octets_d_openssl(self):
        """Sans nonce : octets de `openssl ts -query -sha256 -cert -no_nonce` ; avec nonce (bit fort posé, puis non) :
        octets d'openssl pour le nonce qu'il a tiré, relu par `-text`."""
        self.assertEqual(tetes.requete(EMPREINTE).hex(), SANS_NONCE)
        for nonce, attendu in AVEC_NONCE.items():
            self.assertEqual(tetes.requete(EMPREINTE, nonce).hex(), attendu)

    def test_entier_der_minimal(self):
        self.assertEqual({v: tetes._entier(v).hex() for v in ENTIERS}, ENTIERS)

    def test_longueurs_der(self):
        """Longueur en forme courte sous 128 octets, longue et minimale au-delà : en-têtes et tailles des OCTET STRING
        d'`openssl asn1parse -genstr` (et `-genconf` pour 70 000 octets)."""
        attendus = {1: "0401", 127: "047f", 128: "048180", 255: "0481ff", 256: "04820100", 70000: "0483011170"}
        self.assertEqual({n: (tetes._der(4, bytes(n))[:len(h) // 2].hex(), len(tetes._der(4, bytes(n))) - n) for n, h
                          in attendus.items()}, {n: (h, len(h) // 2) for n, h in attendus.items()})

    def test_refus_nommes(self):
        """Empreinte de 32 octets exactement (RFC 3161 §2.4.1 : longueur de l'algorithme) ; nonce entier de 0 à
        2^64 − 1, jamais un booléen."""
        for e in (EMPREINTE[:31], EMPREINTE + b"x", EMPREINTE.hex(), bytearray(EMPREINTE)):
            self.assertEqual(code(lambda: tetes.requete(e)), "JETON/empreinte", e)
        for n in (-1, 1 << 64, True, 1.0, "1"):
            self.assertEqual(code(lambda: tetes.requete(EMPREINTE, n)), "JETON/nonce", n)
        self.assertEqual(tetes.requete(EMPREINTE, (1 << 64) - 1).hex()[-28:], "020900ffffffffffffffff0101ff")


class Reponse(unittest.TestCase):
    def test_statut_d_une_reponse(self):
        """PKIStatus (RFC 3161 §2.4.2) : rejet d'openssl, 2 ; accordée avec jeton (longueurs en forme longue), 0 ou 1 ;
        attente et révocation sans jeton, 3 et 5."""
        self.assertEqual(tetes.statut(bytes.fromhex(REJET)), 2)
        for s in (0, 1):
            self.assertEqual(tetes.statut(bytes.fromhex(f"3082010a30030201{s:02x}" + JETON)), s)
        self.assertEqual([tetes.statut(bytes.fromhex(h)) for h in ("30053003020103", "30053003020105")], [3, 5])

    def test_reponses_refusees(self):
        """Une réponse mal formée est un refus nommé, jamais un statut : chaque cas porte un seul défaut."""
        for nom, h in MAL_FORMEES.items():
            self.assertEqual(code(lambda: tetes.statut(bytes.fromhex(h))), "JETON/reponse", nom)


class Manifeste(unittest.TestCase):
    def test_manifeste_canonique_et_trie(self):
        """Ligne JSON canonique, têtes triées par observateur puis journal quel que soit l'ordre donné ; octets écrits à
        la main."""
        t1 = {"journal": "pool", "observateur": "o1", "seq": 12, "sha256": "a" * 64, "ws": 1791158340}
        t2 = {"journal": "carte", "observateur": "o2", "seq": 7, "sha256": "b" * 64, "ws": 1791158340}
        t3 = {**t2, "journal": "pool", "seq": 9}
        attendu = ('{"jour":"2026-10-05","observateur":"o1","tetes":[{"journal":"pool","observateur":"o1","seq":12,'
                   '"sha256":"' + "a" * 64 + '","ws":1791158340},{"journal":"carte","observateur":"o2","seq":7,'
                   '"sha256":"' + "b" * 64 + '","ws":1791158340},{"journal":"pool","observateur":"o2","seq":9,'
                   '"sha256":"' + "b" * 64 + '","ws":1791158340}]}\n').encode()
        self.assertEqual(tetes.manifeste("2026-10-05", "o1", [t3, t1, t2]), attendu)


if __name__ == "__main__":
    unittest.main()
