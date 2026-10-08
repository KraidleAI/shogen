"""CB-18c : configurations scellées, descripteur et câblage du collecteur (E-C-02, E-C-23 ; SHOGEN-S2BIS-PLAN-
CABLAGE-1 pour les sondes). CB-18d : point d'entrée `pool`, `run_params`, fermeture du journal à la sortie (E-C-16 ;
SHOGEN-S2BIS-ECRIVAIN-USAGE-1). Configurations de test écrites ici, sha256 attendus calculés par hashlib sur les
octets écrits ; temps réel, w = 1 s ; lectures vers un port local fermé ; sondes vers des adresses de boucle locale
où rien n'écoute (délai de 0,1 s). CB-18g (C-1 de la G2 de la tranche C) : tolérance de départ scellée (`tolerance`),
budget de l'ADR-0029 l.233-234 à la borne, valeurs prises au texte de l'ADR. CB-18h (SHOGEN-S2BIS-CONFIG-REGLES-1) :
places du pool, forme de l'hôte (règle `[a-z0-9.-]{1,253}` de Q-RB-13 du recalcul) et du chemin, commit en minuscules,
délai des sondes à la borne. CB-19f (C-3 (c) et (d) de la relecture d'intégration de P1) : point d'entrée à w = 60,
journal ouvert sur la grille ; délai et places de `formes.json` jusqu'à la boucle."""
import contextlib
import errno
import fcntl
import hashlib
import io
import json
import os
import pathlib
import socket
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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
    """(formes, sante, descripteur) de test ; w = 1 s, δ = 0,6 s, tolérance 0,05 s, délai 0,3 s, marge 0,2 s."""
    forme = {"hote": "127.0.0.1", "port": port, "methode": "GET", "corps": "", "espace": False}
    return ({"w": 1, "delta": 6 * S // 10, "tolerance": S // 20, "delai": 3 * S // 10, "marge": S // 5, "places": 4,
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
        cas = [("CONFIG/champ-absent", {**f, "places": None}, s, d), ("CONFIG/borne", {**f, "tolerance": 0}, s, d),
               ("CONFIG/incoherent : w-divise", {**f, "w": 7}, s, d),
               ("CONFIG/incoherent : marge-delta", {**f, "marge": 6 * S // 10}, s, d),
               ("CONFIG/incoherent : budget", {**f, "delai": S}, s, d),
               ("CONFIG/incoherent : noms-uniques", {**f, "formes": [x, x]}, s, d),
               ("CONFIG/incoherent : methode-corps", {**f, "formes": [x, {**y, "methode": "POST"}]}, s, d),
               ("CONFIG/incoherent : hote-forme", {**f, "formes": [x, {**y, "hote": "Api.example"}]}, s, d),
               ("CONFIG/incoherent : chemin-forme", {**f, "formes": [x, {**y, "chemin": "b"}]}, s, d),
               ("CONFIG/incoherent : places-formes", {**f, "places": 1}, s, d),
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

    def test_budget_de_l_adr_a_la_borne(self):                          # CB-18g, C-1 de la G2 de la tranche C
        """Budget de l'ADR-0029 l.233-234 : tolérance de départ de D-2 (5 s) + plus grand décalage (4 s : cinq
        lectures espacées sur un hôte) + délai (10 s) + marge (1 s) = 20 s ≤ δ = 20 s : admis à l'égalité ; 1 µs de
        plus sur un terme, ou de moins sur δ : refus nommé. Délai de 14 s (sonde du réviseur : admis avant C-1, car
        4 + 14 + 1 ≤ 20) : 24 s > 20 s, refusé."""
        f, s, d = configurations(1)
        cinq = [{**f["formes"][0], "hote": "api.example", "espace": True, "nom": f"f{k}", "chemin": f"/{k}"}
                for k in range(5)]
        adr = {**f, "w": 60, "delta": 20 * S, "tolerance": 5 * S, "delai": 10 * S, "marge": S, "places": 5,
               "formes": cinq}
        budget = "CONFIG/incoherent : budget"
        cas = [(adr, None), ({**adr, "delta": 20 * S - 1}, budget), ({**adr, "delai": 14 * S}, budget)]
        cas += [({**adr, k: adr[k] + 1}, budget) for k in ("tolerance", "delai", "marge")]
        for formes, attendu in cas:
            with self.subTest(formes={k: formes[k] for k in ("delta", "tolerance", "delai", "marge")}):
                r = refus(lambda: entree.configurer(self.ecrire(formes, {**s, "delai": 2 * S}, d)[1], COMMIT))
                self.assertEqual(r and r[:len(budget)], attendu)

    def test_regles_de_configuration_a_la_borne(self):                  # CB-18h, SHOGEN-S2BIS-CONFIG-REGLES-1
        """Places : autant que de formes, admis ; une de moins, refusé (pool dimensionné sur les lectures, ADR-0029
        l.234). Hôte : minuscules, chiffres, « . » et « - » seuls (Q-RB-13). Chemin : « / » puis ASCII imprimable sans
        espace (la lecture refuserait tout autre chemin à chaque fenêtre, FORMAT §10.4). Délai des sondes + marge = δ,
        admis ; 1 µs de plus, refusé. Commit : 40 chiffres hexadécimaux minuscules, seuls admis."""
        f, s, d = configurations(1)
        x, y = f["formes"]
        ok = None
        cas = [({**f, "places": 2}, s, COMMIT, ok), ({**f, "places": 1}, s, COMMIT, "places-formes"),
               (f, {**s, "delai": 2 * S // 5}, COMMIT, ok), (f, {**s, "delai": 2 * S // 5 + 1}, COMMIT, "delai-sondes"),
               (f, s, COMMIT.upper(), "commit"), (f, s, COMMIT[:39] + "g", "commit"), (f, s, COMMIT[:39], "commit")]
        cas += [({**f, "formes": [x, {**y, "hote": h}]}, s, COMMIT, ok) for h in ("api.example", "a-1.b", "z" * 253)]
        cas += [({**f, "formes": [x, {**y, "hote": h}]}, s, COMMIT, "hote-forme") for h in (
            "API.EXAMPLE", "a b", "a:443", "a_b", "é.example", "a/b")]
        cas += [({**f, "formes": [x, {**y, "chemin": c}]}, s, COMMIT, ok) for c in ("/", "/a/b?c=1&d=%20~")]
        cas += [({**f, "formes": [x, {**y, "chemin": c}]}, s, COMMIT, "chemin-forme") for c in (
            "b", "*", "/a b", "/é", "/a" + chr(127), "http://h/a")]
        for formes, sante, commit, regle in cas:
            attendu = regle and (["CONFIG/commit", commit] if regle == "commit" else ["CONFIG/incoherent", regle])
            with self.subTest(formes=formes, sante=sante["delai"], commit=commit):
                r = refus(lambda: entree.configurer(self.ecrire(formes, sante, d)[1], commit))
                self.assertEqual(r and r.split(" : ")[:2], attendu)

    def test_temoins_et_noms_bornes_au_schema(self):                    # CB-19b, C-1 (b) de la relecture d'intégration
        """Sept témoins et sept noms au plus (FORMAT §13.6, §14.1 : la plus grande `sante` reste sous LIMITE) : sept
        admis, huit refusés (CONFIG/borne), chaque liste à son tour ; valeurs prises au calcul du FORMAT."""
        f, s, d = configurations(1)
        listes = {"temoins": [f"127.0.9.{k}" for k in range(1, 9)], "noms": [f"n{k}.example." for k in range(8)]}
        for champ, valeurs in listes.items():
            for k, attendu in ((7, None), (8, "CONFIG/borne")):
                with self.subTest(champ=champ, k=k):
                    r = refus(lambda: entree.configurer(self.ecrire(f, {**s, champ: valeurs[:k]}, d)[1], COMMIT))
                    self.assertEqual(r and r.split(" : ")[0], attendu)

    def test_point_d_entree_w_60_journal_ouvert_sur_la_grille(self):    # CB-19f, C-3 (c) de la relecture d'intégration
        """w = 60 (production ; δ 20 s, tolérance 5 s, délai 10 s, marge 1 s : valeurs de l'ADR) et une horloge hors de
        la grille, 2026-10-05 12:34:56,789012 UTC (12:34:00 = 1791203640 par date -u -d) : le journal s'ouvre à la
        fenêtre de 12:34, `suivante` 12:35, et `run_params` y est écrit ; sortie 0 (`--fenetres 0` : aucune fenêtre
        lue). Tue MI-12 (journal ouvert à la seconde de l'horloge : refus JOURNAL/fenetre)."""
        f, s, d = configurations(port_ferme())
        f = {**f, "w": 60, "delta": 20 * S, "tolerance": 5 * S, "delai": 10 * S, "marge": S}
        with mock.patch.object(entree, "horloge", lambda: (1791203640 + 56) * S + 789012):
            self.assertEqual(self.pool(self.ecrire(f, s, d)[1], self.journal, "--fenetres", "0"), (0, ""))
        enrs = chaine(pathlib.Path(self.journal, "pool-2026-10-05-0.jsonl").read_bytes())[2]
        self.assertEqual([(e["type"], e.get("suivante"), e.get("ws")) for e in enrs],
                         [("ouverture", 1791203700, None), ("run_params", None, 1791203700)])

    def test_delai_et_places_de_formes_json_jusqu_a_la_boucle(self):    # CB-19f, C-3 (d) de la relecture d'intégration
        """`delai` et `places` lus de `formes.json` (0,3 s ; quatre places pour deux formes) arrivent à la boucle :
        chaque lecture appelle le client avec ce délai, et le pool a quatre places, pas une de plus. Tue MI-13 (délai
        non transmis) et MI-14 (places prises au nombre de formes)."""
        f, s, d = configurations(1)
        lus = entree.configurer(self.ecrire(f, s, d)[1], COMMIT)
        _jl, b = entree.construire(lus["formes"][0], lus["sante"][0], lus["descripteur"][0], self.journal)
        with mock.patch.object(entree.http, "lire") as lire:
            b.lectures["a"]({})
        places = [b.places.acquire(blocking=False) for _ in range(5)]
        self.assertEqual((lire.call_args.kwargs.get("delai"), places), (3 * S // 10, [True] * 4 + [False]))

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
            def fsync(fd):                                          # journal neuf : premier fsync d'un fichier au
                if stat.S_ISDIR(os.fstat(fd).st_mode):              # premier marqueur ; celui du dossier, après la
                    return os.fsync(fd)                             # création (CB-19c, C-2 (a)), passe
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
