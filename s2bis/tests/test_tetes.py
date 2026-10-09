"""CB-15a, E-C-36 : requête RFC 3161 construite en bibliothèque standard, statut d'une réponse, manifeste des têtes.
Octets de référence produits hors du code (journal G1 de CB-15a) : `openssl ts -query -data <fichier> -sha256 -cert
-no_nonce` (OpenSSL 3.0.13, PROPOSITION §2.4 « Jeton »), puis la même commande avec nonce, dont la valeur est lue par
`openssl ts -query -in … -text` ; entiers et longueurs DER par `openssl asn1parse` ; réponse de rejet produite par
`openssl ts -reply` d'une TSA jetable (clés détruites) ; autres réponses écrites à la main d'après RFC 3161 §2.4.2
(forme DER des longueurs : X.690, non détenue) ; manifeste écrit à la main. CB-15b, E-C-35 : fichiers de tête du dépôt
(AVIS Q-D-03), écrits à la main par le test ; export atomique relevé par un espion de fsync. CB-15c : enregistrement
`tetes` et export dans la fenêtre qui clôt l'heure (boucle à horloge injectée, journal relu par `chaine`, tête du point
prise au `prec` qui le suit) ; option `--depot` et nom d'observateur au point d'entrée."""
import contextlib
import io
import json
import os
import pathlib
import stat
import tempfile
import unittest
from unittest import mock

from shogen_s2bis.collecte import boucle, entree, journal, tetes
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import Temps, borne, rapide
from tests.test_entree import COMMIT, configurations, port_ferme
from tests.test_journal import FICHIER, Base, chaine
from tests.test_reprise import m

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


WS_H, A, B = 1791154740, "a" * 64, "b" * 64                  # 2026-10-04 22:59 UTC : fenêtre qui clôt l'heure de 23:00


def tete(o, jl="pool", seq=12, sha=A, ws=WS_H, **autres):
    return {"journal": jl, "observateur": o, "seq": seq, "sha256": sha, "ws": ws, **autres}


def ligne_tete(t, sep=(",", ":")):
    """Fichier de tête écrit par le test, sans le code : objet JSON, clés triées, saut de ligne final."""
    return json.dumps(t, sort_keys=True, separators=sep).encode() + b"\n"


class Depot(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.sync = d.name, []

    def espion(self, fd):
        """fsync relevé : (« dossier », noms) ou (« fichier », taille, noms présents)."""
        st, noms = os.fstat(fd), sorted(os.listdir(self.d))
        self.sync.append(("dossier", noms) if stat.S_ISDIR(st.st_mode) else ("fichier", st.st_size, noms))

    def poser(self, fichiers):
        for nom, contenu in fichiers.items():
            p = pathlib.Path(self.d, nom)
            p.mkdir() if contenu is None else p.write_bytes(contenu if type(contenu) is bytes else ligne_tete(contenu))

    def test_export_atomique_a_chaque_point(self):
        """Ligne canonique {journal, observateur, seq, sha256, ws} (octets écrits à la main), écrite dans un fichier
        temporaire synchronisé, renommée, puis dossier synchronisé ; un export suivant remplace le fichier."""
        dep = tetes.Depot(self.d, "o1", fsync=self.espion)
        dep.exporter(WS_H, (12, A))
        attendu = ('{"journal":"pool","observateur":"o1","seq":12,"sha256":"' + A + '","ws":1791154740}\n').encode()
        self.assertEqual((os.listdir(self.d), self.sync), (["o1-pool.tete"], [
            ("fichier", len(attendu), [".o1-pool.tete.tmp"]), ("dossier", ["o1-pool.tete"])]))
        self.assertEqual(pathlib.Path(self.d, "o1-pool.tete").read_bytes(), attendu)
        dep.exporter(WS_H + 3600, (73, B))
        self.assertEqual((os.listdir(self.d), pathlib.Path(self.d, "o1-pool.tete").read_bytes(), dep.echec),
                         (["o1-pool.tete"], ligne_tete(tete("o1", seq=73, sha=B, ws=WS_H + 3600)), None))

    def test_export_en_echec_ne_leve_jamais(self):
        """Dossier absent, fsync en panne : aucune exception ; l'échec, nommé par son type, va au `tetes` suivant ; un
        export réussi l'efface et remplace le fichier temporaire laissé."""
        dep = tetes.Depot(os.path.join(self.d, "absent"), "o1")
        dep.exporter(WS_H, (12, A))
        self.assertEqual(dep.lire(), {"tetes": [], "refus": [[".", "TETES/depot"]], "ignores": 0,
                                      "export": "FileNotFoundError"})

        pannes = [OSError(5, "EIO")]

        def panne(fd):
            if pannes:
                raise pannes.pop()
        dep = tetes.Depot(self.d, "o1", fsync=panne)
        dep.exporter(WS_H, (12, A))
        self.assertEqual((dep.lire()["export"], os.listdir(self.d)), ("OSError", [".o1-pool.tete.tmp"]))
        dep.exporter(WS_H, (12, A))                                 # l'export suivant réussit : échec effacé
        self.assertEqual((dep.lire()["export"], os.listdir(self.d)), (None, ["o1-pool.tete"]))

    def test_lecture_du_depot_et_refus_nommes(self):
        """Têtes valides des autres fichiers (la sienne exclue, celle de son autre journal comprise), dans l'ordre des
        noms ; un défaut par fichier, refus nommé ; noms hors grammaire ignorés, jumeau en majuscules compris (C-6)."""
        self.poser({"o1-pool.tete": b"illisible", "o1-carte.tete": tete("o1", "carte", 5), "o2-pool.tete": tete("o2"),
                    "o2-carte.tete": ligne_tete(tete("o2", "carte"))[:-1] + b" " * 1024 + b"\n",
                    "o3-pool.tete": ligne_tete(tete("o3"), (", ", ": ")), "o3-carte.tete": tete("o3", "carte", x=1),
                    "o4-pool.tete": tete("o5"), "o4-carte.tete": tete("o4", "carte", True),
                    "o5-pool.tete": tete("o5", seq=10 ** 18), "o5-carte.tete": tete("o5", "carte", 10 ** 700),
                    "o6-pool.tete": tete("o6", sha=A.upper()), "o6-carte.tete": tete("o6", "carte", ws=-60),
                    "o7-pool.tete": b"[1]\n", "o7-carte.tete": None, "o8_pool.tete": tete("o8"),
                    ".o2-pool.tete.tmp": tete("o2"), "o2-Pool.tete": tete("o2", "Pool"),
                    "o2-pool.tete.tmp": tete("o2"), "O2-pool.tete": tete("O2")})
        refus = {"o2-carte.tete": "taille", "o3-carte.tete": "forme", "o3-pool.tete": "forme",
                 "o4-carte.tete": "champs", "o4-pool.tete": "champs", "o5-carte.tete": "forme",
                 "o5-pool.tete": "champs", "o6-carte.tete": "champs", "o6-pool.tete": "champs",
                 "o7-carte.tete": "lecture", "o7-pool.tete": "forme"}
        self.assertEqual(tetes.Depot(self.d, "o1").lire(),
                         {"tetes": [tete("o1", "carte", 5), tete("o2")], "refus": [[n, "TETES/" + c] for n, c in
                                                                                   refus.items()],
                          "ignores": 0, "export": None})

    def test_seize_tetes_au_plus_et_enregistrement_admis_par_l_ecrivain(self):
        """Au-delà de 16 fichiers, les premiers par nom sont lus, les autres comptés ; l'enregistrement `tetes` tiré
        d'un dépôt hostile s'écrit sans refus de l'écrivain (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1)."""
        self.poser({f"p{k:02d}-pool.tete": tete(f"p{k:02d}", seq=k) for k in range(20)})
        lu = tetes.Depot(self.d, "o1").lire()
        self.assertEqual((lu["tetes"], lu["ignores"]), ([tete(f"p{k:02d}", seq=k) for k in range(16)], 4))
        self.poser({"a99-pool.tete": tete("a99", seq=10 ** 700), "a98-pool.tete": tete("a98", ws=10 ** 12)})
        lu = tetes.Depot(self.d, "o1").lire()
        self.assertEqual((lu["refus"], len(lu["tetes"])), ([["a98-pool.tete", "TETES/champs"], ["a99-pool.tete",
                                                                                            "TETES/forme"]], 14))
        with tempfile.TemporaryDirectory() as d:
            jl = journal.Journal(d, "pool").ouvrir(WS_H - 120)
            jl.ecrire("tetes", WS_H, **lu)
            jl.fermer()
            octets = pathlib.Path(d, "pool-2026-10-04-0.jsonl").read_bytes()
        self.assertEqual(({k: v for k, v in chaine(octets)[2][1].items() if k not in ("seq", "prec")}, lu["ignores"]),
                         ({"type": "tetes", "ws": WS_H, **lu}, 6))


class Branchement(Base):
    def tourner(self, depot, n):
        """`n` fenêtres depuis 22:59 UTC (fenêtre qui clôt l'heure de 23:00), journal ouvert à 22:58:05 ; lecture `a`
        rapide ; rend les enregistrements relus par `chaine`."""
        temps = Temps(m(0) * S + 5 * S)
        jl = borne(self, self.journal, m(0))
        b = boucle.Boucle(jl, {"a": rapide}, [(0, "a")], 4, horloge=temps, dormir=temps.dormir,
                          attendre=temps.attendre, monotone=temps.monotone, depot=depot)
        borne(self, b.tourner, n)
        return chaine(self.etat()[FICHIER])[2]

    def test_tetes_avant_la_sante_puis_export_de_la_tete_du_point(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        pathlib.Path(d.name, "o2-pool.tete").write_bytes(ligne_tete(tete("o2", seq=40, sha=B)))
        enrs = self.tourner(tetes.Depot(d.name, "o1"), 2)
        self.assertEqual([(e["type"], e.get("ws")) for e in enrs], [("ouverture", None)] + [
            (t, m(1)) for t in ("lecture", "tetes", "sante", "marqueur", "point")] + [
            (t, m(2)) for t in ("lecture", "sante", "marqueur")])
        self.assertEqual({k: enrs[2][k] for k in ("tetes", "refus", "ignores", "export")},
                         {"tetes": [tete("o2", seq=40, sha=B)], "refus": [], "ignores": 0, "export": None})
        self.assertEqual(sorted(os.listdir(d.name)), ["o1-pool.tete", "o2-pool.tete"])
        self.assertEqual(pathlib.Path(d.name, "o1-pool.tete").read_bytes(),
                         ligne_tete(tete("o1", seq=enrs[5]["seq"], sha=enrs[6]["prec"], ws=m(1))))

    def test_sans_depot_ni_tetes_ni_export(self):
        self.assertEqual([e["type"] for e in self.tourner(None, 1)], ["ouverture", "lecture", "sante", "marqueur",
                                                                      "point"])

    def test_depot_absent_la_boucle_continue(self):
        enrs = self.tourner(tetes.Depot(os.path.join(self.d, "absent"), "o1"), 2)
        self.assertEqual([(e["type"], e.get("refus")) for e in enrs if e["type"] in ("tetes", "marqueur")],
                         [("tetes", [[".", "TETES/depot"]]), ("marqueur", None), ("marqueur", None)])

    def test_point_d_entree_depot_et_nom_d_observateur(self):
        """`--depot` câble un dépôt au nom de l'observateur du descripteur, journal `pool` ; sans lui, aucun ; un nom
        d'observateur hors de `[a-z0-9]{1,16}` est refusé avant l'ouverture du journal (sortie 2)."""
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        f, s, o = configurations(port_ferme())
        os.mkdir(jdir := os.path.join(d.name, "journal"))

        def lancer(observateur, *depot):
            args = ["pool", "--commit", COMMIT, "--journal", jdir, *depot]
            for nom, donnees in (("formes", f), ("sante", s), ("descripteur", {**o, "observateur": observateur})):
                pathlib.Path(d.name, nom + ".json").write_text(json.dumps(donnees), encoding="utf-8")
                args += [f"--{nom}", os.path.join(d.name, nom + ".json")]
            vus, err = [], io.StringIO()
            with mock.patch.object(boucle.Boucle, "tourner", lambda b, n: vus.append(b.depot)), \
                    contextlib.redirect_stderr(err):
                return entree.main(args), [x and (x.dossier, x.observateur, x.journal) for x in vus], err.getvalue()
        self.assertEqual(lancer("o1", "--depot", d.name), (0, [(d.name, "o1", "pool")], ""))
        self.assertEqual(lancer("o1"), (0, [None], ""))
        for nom in ("O1", "o-1", "o/1", "Ö1", "o1 "):
            self.assertEqual(lancer(nom, "--depot", d.name),
                             (2, [], "collecte : refus : CONFIG/incoherent : observateur-nom\n"), nom)


if __name__ == "__main__":
    unittest.main()
