"""CB-18c : configurations scellées, descripteur et câblage du collecteur (E-C-02, E-C-23 ; SHOGEN-S2BIS-PLAN-
CABLAGE-1 pour les sondes). CB-18d : point d'entrée `pool`, `run_params`, fermeture du journal à la sortie (E-C-16 ;
SHOGEN-S2BIS-ECRIVAIN-USAGE-1). Configurations de test écrites ici, sha256 attendus calculés par hashlib sur les
octets écrits ; temps réel, w = 1 s ; lectures vers un port local fermé ; sondes vers des adresses de boucle locale
où rien n'écoute (délai de 0,1 s)."""
import contextlib
import errno
import fcntl
import hashlib
import io
import json
import os
import pathlib
import socket
import subprocess
import sys
import tempfile
import unittest

from shogen_s2bis.collecte import entree, journal
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import borne
from tests.test_journal import chaine

COMMIT = "0123456789abcdef0123456789abcdef01234567"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def refus(appel):
    """Texte de l'exception que lève `appel`, None sans exception."""
    try:
        appel()
    except Exception as e:                                          # refus nommé, ou OSError d'un fichier absent
        return str(e)
    return None


def port_ferme():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]                                   # port rendu : rien n'y écoute


def configurations(port):
    """(formes, sante, descripteur) de test ; w = 1 s, δ = 0,6 s, délai 0,3 s, marge 0,2 s."""
    forme = {"hote": "127.0.0.1", "port": port, "methode": "GET", "corps": "", "espace": False}
    return ({"w": 1, "delta": 6 * S // 10, "delai": 3 * S // 10, "marge": S // 5, "places": 4,
             "formes": [{**forme, "nom": "a", "chemin": "/a"}, {**forme, "nom": "b", "chemin": "/b"}]},
            {"commande": [sys.executable, "-c", "print('suivi')"], "temoins": ["127.0.9.1", "127.0.9.2", "127.0.9.3"],
             "noms": ["a.example.", "b.example."], "delai": S // 10},
            {"observateur": "O1", "fournisseur": "essai", "region": "boucle-locale", "asn": 64512,
             "resolveur": "127.0.9.53", "config_resolveur": "resolv.conf", "versions": ["python3 essai"],
             "empreinte": "e" * 64})


class Entree(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.journal = d.name, os.path.join(d.name, "journal")
        os.mkdir(self.journal)

    def ecrire(self, formes, sante, descripteur):
        """Écrit les trois fichiers ; rend leurs sha256 (sur les octets écrits) et leurs chemins."""
        sha, chemins = {}, {}
        for nom, donnees in (("formes", formes), ("sante", sante), ("descripteur", descripteur)):
            octets = json.dumps(donnees).encode()
            with open(os.path.join(self.d, nom + ".json"), "wb") as f:
                f.write(octets)
            sha[nom], chemins[nom] = hashlib.sha256(octets).hexdigest(), f.name
        return sha, chemins

    def test_refus_nommes_de_configuration(self):                         # E-C-02
        """Configuration incomplète ou incohérente (une règle nommée par cas), commit illisible : refus nommé,
        RefusConfig ou RefusBoucle, au chargement ; fichier absent : OSError."""
        f, s, d = configurations(1)
        x, y = f["formes"]
        cas = [("CONFIG/champ-absent", {**f, "places": None}, s, d),
               ("CONFIG/incoherent : w-divise", {**f, "w": 7}, s, d),
               ("CONFIG/incoherent : marge-delta", {**f, "marge": 6 * S // 10}, s, d),
               ("CONFIG/incoherent : budget", {**f, "delai": S}, s, d),
               ("CONFIG/incoherent : noms-uniques", {**f, "formes": [x, x]}, s, d),
               ("CONFIG/incoherent : methode-corps", {**f, "formes": [x, {**y, "methode": "POST"}]}, s, d),
               ("CONFIG/incoherent : espace-par-hote", {**f, "formes": [x, {**y, "espace": True}]}, s, d),
               ("CONFIG/incoherent : empreinte-hex", f, s, {**d, "empreinte": "E" * 64}),
               ("CONFIG/incoherent : temoins-ipv4", f, {**s, "temoins": ["127.0.9.01"]}, d),
               ("CONFIG/incoherent : noms-dns", f, {**s, "noms": ["a..b"]}, d),
               ("CONFIG/incoherent : resolveur-ipv4", f, s, {**d, "resolveur": "localhost"}),
               ("CONFIG/incoherent : delai-sondes", f, {**s, "delai": S // 2}, d),
               ("BOUCLE/hote", {**f, "formes": [{**x, "nom": str(k)} for k in range(6)]}, s, d)]
        for attendu, *fichiers in cas:
            fichiers[0] = {k: v for k, v in fichiers[0].items() if v is not None}
            with self.subTest(attendu=attendu):
                self.assertTrue(str(refus(lambda: entree.configurer(self.ecrire(*fichiers)[1], COMMIT))).startswith(
                    attendu))
        chemins = self.ecrire(f, s, d)[1]
        self.assertEqual((refus(lambda: entree.configurer(chemins, "abc")), refus(lambda: entree.configurer(
            {**chemins, "formes": "absent.json"}, COMMIT))[:9]), ("CONFIG/commit : abc", "[Errno 2]"))
        self.assertEqual(sorted(entree.configurer(chemins, COMMIT)), ["descripteur", "formes", "sante"])

    def test_cablage_des_sondes_et_de_la_boucle(self):                  # SHOGEN-S2BIS-PLAN-CABLAGE-1
        """Les sondes reçoivent la commande, les témoins, les noms et le délai de `sante.json`, le résolveur et sa
        configuration du descripteur, le dossier du journal ; la boucle, ses paramètres de `formes.json` ; le plan, une
        lecture par forme."""
        f, s, d = configurations(1)
        jl, b = entree.construire(f, s, d, self.journal)
        o = b.sondes
        self.assertEqual((o.commande, o.temoins, o.noms, o.delai, o.resolveur, o.resolv, o.dossier),
                         (s["commande"], s["temoins"], s["noms"], S // 10, "127.0.9.53", "resolv.conf", self.journal))
        self.assertEqual((b.w, b.delta, b.marge, b.journal, jl.dossier, jl.prefixe, jl.w, sorted(b.lectures), b.plan),
                         (1, 6 * S // 10, S // 5, jl, self.journal, "pool", 1, ["a", "b"], [(0, "a"), (0, "b")]))

    def pool(self, chemins, dossier, *options, **injections):
        """`entree.main` dans le fil borné du test (10 s : une boucle qui ne s'arrête pas fait échouer le test sans
        pendre la suite), sortie d'erreur captée : (code, texte)."""
        args, err = ["pool", "--journal", dossier, "--commit", COMMIT, *options], io.StringIO()
        for nom, chemin in chemins.items():
            args += [f"--{nom}", chemin]
        with contextlib.redirect_stderr(err):
            code = borne(self, lambda: entree.main(args, **injections), delai=10)
        return code, err.getvalue()

    def test_point_d_entree_refus_sortie_2(self):                        # CB-18d
        """Refus de configuration au point d'entrée : sortie 2, refus nommé sur la sortie d'erreur, rien au dossier du
        journal (`--fenetres 1` : un refus manqué fait tourner une fenêtre et échouer le test, sans le pendre) ; la
        commande `python3 -m shogen_s2bis.collecte` sort de même."""
        f, s, d = configurations(1)
        hote = {**f, "formes": [{**f["formes"][0], "nom": str(k)} for k in range(6)]}
        code, err = self.pool(self.ecrire(hote, s, d)[1], self.journal, "--fenetres", "1")
        self.assertEqual((code, err.split(" : ")[:3]), (2, ["collecte", "refus", "BOUCLE/hote"]))  # refus de la boucle
        attendu = (2, "collecte : refus : CONFIG/incoherent : budget" + chr(10))
        self.assertEqual((self.pool(self.ecrire({**f, "delai": S}, s, d)[1], self.journal, "--fenetres", "1"),
                          os.listdir(self.journal)), (attendu, []))
        args = [x for n, c in self.ecrire(f, s, d)[1].items() for x in (f"--{n}", c)]
        p = subprocess.run([sys.executable, "-B", "-m", "shogen_s2bis.collecte", "pool", "--journal", self.journal,
                            "--commit", "abc", "--fenetres", "1", *args], cwd=RACINE, capture_output=True, text=True,
                           timeout=60)
        self.assertEqual((p.returncode, p.stderr), (2, "collecte : refus : CONFIG/commit : abc" + chr(10)))

    def test_run_params_et_fermeture_sur_erreur_du_journal(self):       # CB-18d, ECRIVAIN-USAGE-1 (point d'entrée)
        """`run_params` porte le commit, le sha256 des octets de chaque fichier chargé, leurs contenus et la version de
        Python, à la première fenêtre admise (§14.4 : aucun trou de plus au démarrage). Une OSError ou JOURNAL/casse
        levée au premier fsync arrête la boucle : sortie 1, refus nommé, journal fermé (verrou libre aussitôt) ;
        l'instance suivante reprend et réécrit `run_params`."""
        f, s, d = configurations(port_ferme())
        sha, chemins = self.ecrire(f, s, d)
        for i, erreur in enumerate((OSError(errno.EIO, "fsync (simulé)"), journal.ErreurJournal("JOURNAL/casse", "s"))):
            def fsync(fd):                                          # journal neuf : premier fsync au premier marqueur
                raise erreur
            os.mkdir(dossier := os.path.join(self.d, f"j{i}"))
            code, err = self.pool(chemins, dossier, "--fenetres", "3", fsync=fsync)
            with self.subTest(erreur=erreur), open(os.path.join(dossier, "pool.verrou"), "rb") as v:
                fcntl.flock(v, fcntl.LOCK_EX | fcntl.LOCK_NB)         # verrou rendu par la fermeture
                fcntl.flock(v, fcntl.LOCK_UN)
                self.assertEqual((code, err.split(" : ")[:2]), (1, ["collecte", "arrêt"]))
                self.assertIn(getattr(erreur, "code", "OSError"), err)
        self.assertEqual(self.pool(chemins, dossier, "--fenetres", "1"), (0, ""))
        octets = b"".join(pathlib.Path(dossier, n).read_bytes() for n in sorted(os.listdir(dossier))
                          if n.endswith(".jsonl"))
        enrs = chaine(octets)[2]
        self.assertEqual((enrs[0]["type"], [e["type"] for e in enrs if e["type"] in ("reprise", "marqueur")]),
                         ("ouverture", ["marqueur", "reprise", "marqueur"]))
        premier = [e["type"] for e in enrs][:[e["type"] for e in enrs].index("marqueur")]
        self.assertNotIn("trou", premier)                           # journal ouvert à la fenêtre courante
        reprise = next(e for e in enrs if e["type"] == "reprise")    # fenêtre admise : après celle du redémarrage
        self.assertEqual([e["ws"] for e in enrs if e["type"] == "run_params"],
                         [enrs[0]["suivante"], max(reprise["suivante"], reprise["ws"] + 1)])
        self.assertEqual([{k: v for k, v in e.items() if k not in ("seq", "prec", "ws")} for e in enrs
                          if e["type"] == "run_params"],
                         [{"type": "run_params", "commit": COMMIT, "sha256": sha, "python": sys.version, "formes": f,
                           "sante": s, "descripteur": d}] * 2)
