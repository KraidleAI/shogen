"""CB-18e : test de bout en bout du collecteur (E-C-24 ; ADR-0029 l.239 ; principe de SHOGEN-FORMAT-JOURNAUX-1). Le
collecteur entier tourne en sous-processus, garde réseau posée par `import tests`, en temps réel (w = 1 s) ; son
journal est validé contre le FORMAT (docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md) par `anomalies`, écrit d'après le
texte, sans rien importer du collecteur. Exécution A : `entree.main` sans TLS, vers un serveur en clair de boucle
locale, trois fenêtres. Exécution B : le point d'entrée `python3 -m shogen_s2bis.collecte` tel quel (contexte TLS
d'urllib : poignée refusée par ce serveur), qui reprend le même journal, deux fenêtres."""
import base64
import hashlib
import json
import os
import pathlib
import re
import socket
import subprocess
import sys
import tempfile
import threading
import unittest

from tests.test_entree import COMMIT, configurations, port_ferme
from tests.test_journal import chaine

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIN, CRLF, CORPS, S = bytes([13, 10, 13, 10]), bytes([13, 10]), b'{"x":1}', 1_000_000
HARNAIS = """
import runpy, sys, tests
from shogen_s2bis.collecte import entree
if sys.argv[1] == "-m":
    del sys.argv[1]
    runpy.run_module("shogen_s2bis.collecte", run_name="__main__", alter_sys=True)
raise SystemExit(entree.main(sys.argv[1:], tls=None))
"""
CHAMPS = {"ouverture": {"jour", "suivante"}, "marqueur": {"ws"}, "point": {"ws"}, "cloture": {"jour"},
          "reprise": {"ws", "suivante", "queue"}, "trou": {"de", "a", "cause"},
          "run_params": {"ws", "commit", "sha256", "python", "formes", "sante", "descripteur"},
          "lecture": {"ws", "forme", "prevu", "statut", "sous_type", "code", "depart", "fin", "phases", "adresse",
                      "brut", "sha256", "valeurs"},
          "sante": {"ws", "d2", "fils", "horloges", "d3", "d4", "d5", "disque", "resolveur"}}      # §2, §9, §13, §14
PHASES = ["dns", "connexion", "tls", "requete", "corps"]                                         # §10.1
DNS = {"statut", "rcode", "tc", "reponses", "debut", "fin"}                                      # §12
HEX = re.compile("[0-9a-f]{64}")


def niveau(v):
    """Niveau d'imbrication (FORMAT §8.3) : 1 pour un objet ou une liste sans conteneur, 1 + celui de son plus profond
    conteneur sinon ; 0 pour une valeur simple."""
    return 1 + max([niveau(x) for x in (v.values() if isinstance(v, dict) else v)], default=0) if isinstance(
        v, (dict, list)) else 0


def entiers(*x):
    return all(type(v) is int for v in x)


def requete_dns(v, cle, attendu):
    """Résultat d'une sonde D-4 ou D-5 (§12, §13.4) : null, ou la clé du témoin puis les champs d'une requête."""
    return v is None or (set(v) == DNS | {cle} and v[cle] == attendu and entiers(v["debut"], v["fin"]) and
                         v["statut"] in ("reponse", "delai", "forme", "reseau"))


def brut_intact(e):
    try:                                                            # base64 standard, avec remplissage (§9.1)
        return hashlib.sha256(base64.b64decode(e["brut"], validate=True)).hexdigest() == e["sha256"]
    except (TypeError, ValueError):
        return False


def anomalies(enrs, f, s):
    """Écarts au FORMAT des enregistrements relus par `chaine` (§1 : JSON canonique, `seq` et `prec` chaînés) ; [] :
    conforme. `f`, `s` : contenus de `formes.json` et `sante.json` (grille, départ, échéance, sondes)."""
    ecarts, w, fenetre, marqueurs = [], f["w"], [], []

    def exige(ok, quoi):
        if not ok:
            ecarts.append(f"seq {e.get('seq')} {e.get('type')} : {quoi}")
    for i, e in enumerate(enrs):
        t, suivant = e.get("type"), enrs[i + 1].get("type") if i + 1 < len(enrs) else None
        exige(set(e) == CHAMPS.get(t, set()) | {"type", "seq", "prec"}, f"champs {sorted(e)}")
        exige(niveau(e) <= 64, "imbrication")                                                               # §8.3
        if t not in CHAMPS or set(e) != CHAMPS[t] | {"type", "seq", "prec"}:
            continue
        exige("ws" not in e or entiers(e["ws"]) and e["ws"] % w == 0, "ws hors grille")                    # §3.1
        if t in ("ouverture", "cloture"):
            exige(re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", e["jour"]) and entiers(e.get("suivante", 0)), "jour")
        elif t == "reprise":
            exige(entiers(e["suivante"]) and (e["queue"] is None or all(set(q) == {"fichier", "position", "octets",
                  "sha256"} for q in e["queue"])), "reprise")                                                 # §7.4
            fenetre = []
        elif t == "trou":
            exige(entiers(e["de"], e["a"]) and e["de"] <= e["a"] and e["cause"] in ("arret", "horloge_reculee", "saut")
                  and suivant == "marqueur", "trou")                                                          # §8.1
        elif t == "run_params":
            exige(re.fullmatch("[0-9a-f]{40}", e["commit"]) and sorted(e["sha256"]) == ["descripteur", "formes",
                  "sante"] and all(HEX.fullmatch(h) for h in e["sha256"].values()), "run_params")           # §14.4
            exige(i > 0 and enrs[i - 1]["type"] in ("ouverture", "reprise"), "run_params hors tête")       # §11.5
        elif t == "lecture":
            p, depart, fin = e["phases"], (e["ws"] + w) * S - f["delta"], (e["ws"] + w) * S - f["marge"]
            exige(e["statut"] in ("ok", "panne_http", "panne_transport", "panne_decode") and (
                e["sous_type"] in ("dns", "connexion", "tls", "delai", "coupure", "autre") if e["statut"] ==
                "panne_transport" else e["sous_type"] is None), "statut")                                    # §9.1
            exige(e["prevu"] == depart and entiers(e["depart"], e["fin"]) and e["depart"] >= depart and
                  e["fin"] <= fin, "instants")                                                               # §11
            exige(set(p) <= set(PHASES) and entiers(*p.values()) and [p[x] for x in PHASES if x in p] == sorted(
                p.values()) and (e["adresse"] is None) == ("dns" not in p), "phases")                         # §10.1
            exige(e["adresse"] is None or re.fullmatch("([0-9]{1,3}[.]){3}[0-9]{1,3}:[0-9]+", e["adresse"]), "ip")
            exige(brut_intact(e) and e["valeurs"] is None and (e["code"] is None or entiers(e["code"])), "corps")
            fenetre.append(e)
        elif t == "sante":
            exige(all(x["type"] == "lecture" and x["ws"] == e["ws"] for x in fenetre) and [(x["prevu"], x["forme"])
                  for x in fenetre] == sorted((x["prevu"], x["forme"]) for x in fenetre), "ordre des lectures")
            exige(e["d2"] == {"retard_max": max([x["depart"] - x["prevu"] for x in fenetre], default=None),
                              "non_parties": len(f["formes"]) - len(fenetre)}, "d2")                         # §11.6
            fils, h = e["fils"], e["horloges"]
            exige(set(fils) == {"abandonnes", "tardives", "sondes"} and entiers(fils["abandonnes"], fils["sondes"],
                  *fils["tardives"]) and fils["tardives"] == sorted(fils["tardives"]), "fils")              # §11.6
            exige(h is None or set(h) == {"murale", "monotone"} and entiers(*h.values()), "horloges")
            exige(e["d3"] is None or set(e["d3"]) in ({"sortie", "code", "debut", "fin"}, {"erreur", "debut", "fin"}),
                  "d3")                                                                                       # §13.3
            exige(len(e["d4"]) == len(s["temoins"]) and len(e["d5"]) == len(s["noms"]) and all(
                requete_dns(v, "adresse", a) for v, a in zip(e["d4"], s["temoins"])) and all(
                requete_dns(v, "nom", n) for v, n in zip(e["d5"], s["noms"])), "d4, d5")                     # §13.4
            exige(set(e["disque"]) in ({"total", "libre"}, {"erreur"}) and (
                e["resolveur"] is None or HEX.fullmatch(e["resolveur"])), "disque, resolveur")             # §13.5
            exige(suivant in ("trou", "marqueur"), "marqueur après la santé")                                 # §11.5
        elif t == "marqueur":
            exige(not marqueurs or e["ws"] > marqueurs[-1], "marqueurs strictement croissants")              # §3.2
            marqueurs, fenetre = marqueurs + [e["ws"]], []
        elif t == "point":
            exige((e["ws"] + w) % 3600 == 0 and enrs[i - 1]["type"] == "marqueur", "point")                 # §2
    return ecarts


def servir(test):
    """Serveur de boucle locale, une connexion par fil : GET /a, 200 et CORPS ; autre requête, 503 ; une poignée TLS
    (premier octet 22) reçoit la même réponse en clair et échoue. Fermé avec le test ; rend le port."""
    srv = socket.create_server(("127.0.0.1", 0))
    test.addCleanup(srv.close)

    def repondre(conn):
        with conn:
            try:
                conn.settimeout(5)
                recu = b""
                while FIN not in recu and recu[:1] != bytes([22]) and (bloc := conn.recv(4096)):
                    recu += bloc
                code, corps = (200, CORPS) if recu.startswith(b"GET /a ") else (503, b"indisponible")
                conn.sendall(CRLF.join([b"HTTP/1.1 %d X" % code, b"Content-Length: %d" % len(corps), b"", corps]))
            except OSError:                                         # client parti : fin du service de la connexion
                pass

    def accueil():
        while True:
            try:
                conn = srv.accept()[0]
            except OSError:                                         # serveur fermé à la fin du test
                return
            threading.Thread(target=repondre, args=(conn,), daemon=True).start()
    threading.Thread(target=accueil, daemon=True).start()
    return srv.getsockname()[1]


class BoutEnBout(unittest.TestCase):
    def test_collecteur_journal_conforme_au_format(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        f, s, o = configurations(servir(self))
        s["commande"], s["delai"] = ["/bin/echo", "suivi"], S // 5    # D-3 : python3 -c dépassait 0,1 s sous charge
        f["formes"].append({**f["formes"][0], "nom": "c", "port": port_ferme(), "chemin": "/c"})
        o["config_resolveur"], args, sha = os.path.join(d.name, "resolv.conf"), ["pool", "--commit", COMMIT], {}
        with open(o["config_resolveur"], "wb") as x:
            x.write(b"nameserver 127.0.9.53")
        for nom, donnees in (("formes", f), ("sante", s), ("descripteur", o)):
            octets = json.dumps(donnees).encode()
            with open(os.path.join(d.name, nom + ".json"), "wb") as x:
                x.write(octets)
            args, sha[nom] = args + [f"--{nom}", x.name], hashlib.sha256(octets).hexdigest()
        os.mkdir(journal := os.path.join(d.name, "journal"))
        a, b = (subprocess.run([sys.executable, "-B", "-c", HARNAIS, *m, *args, "--journal", journal, "--fenetres", n],
                               cwd=RACINE, capture_output=True, timeout=60) for m, n in (([], "3"), (["-m"], "2")))
        self.assertEqual((a.returncode, a.stderr, b.returncode, b.stderr), (0, b"", 0, b""))
        noms = sorted(n for n in os.listdir(journal) if n.endswith(".jsonl"))
        enrs = chaine(b"".join(pathlib.Path(journal, n).read_bytes() for n in noms))[2]
        self.assertEqual((anomalies(enrs, f, s), max(map(niveau, enrs))), ([], 4))      # M = 4 (FORMAT §8.3)
        types = [e["type"] for e in enrs[1:] if e["type"] in ("run_params", "reprise", "trou", "marqueur")]
        self.assertIn((enrs[0]["type"], types), [("ouverture", ["run_params"] + ["marqueur"] * 3 + ["reprise",
                      "run_params"] + x + ["marqueur"] * 2) for x in ([], ["trou"])])      # trou : redémarrage
        self.assertEqual([e["queue"] for e in enrs if e["type"] == "reprise"], [None])  # R-2 : §7.1 tient tout intègre
        self.assertEqual([(e["forme"], e["statut"], e["sous_type"], e["code"]) for e in enrs if e["type"] == "lecture"],
                         [("a", "ok", None, 200), ("b", "panne_http", None, 503), ("c", "panne_transport", "connexion",
                          None)] * 3 + [("a", "panne_transport", "tls", None), ("b", "panne_transport", "tls", None),
                                        ("c", "panne_transport", "connexion", None)] * 2)
        self.assertEqual({base64.b64decode(e["brut"]) for e in enrs if e["type"] == "lecture" and e["code"]}, {
            CORPS, b"indisponible"})
        self.assertEqual([{k: e[k] for k in ("commit", "sha256", "formes", "sante", "descripteur")} for e in enrs if
                          e["type"] == "run_params"], [{"commit": COMMIT, "sha256": sha, "formes": f, "sante": s,
                                                        "descripteur": o}] * 2)
        empreinte = hashlib.sha256(b"nameserver 127.0.9.53").hexdigest()
        self.assertEqual({(e["d3"]["sortie"], e["d3"]["code"], e["resolveur"]) for e in enrs if e["type"] == "sante"},
                         {("suivi" + chr(10), 0, empreinte)})
        self.assertTrue(any(v is not None for e in enrs if e["type"] == "sante" for v in e["d4"] + e["d5"]))  # §12 vu
        if os.path.exists(sommes := os.path.join(journal, "pool.sha256")):                       # bascule de 00:00 UTC
            for h, n in (ligne.split("  ") for ligne in pathlib.Path(sommes).read_text(encoding="utf-8").splitlines()):
                self.assertEqual(hashlib.sha256(pathlib.Path(journal, n).read_bytes()).hexdigest(), h)
