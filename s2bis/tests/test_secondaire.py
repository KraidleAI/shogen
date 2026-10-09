"""CB-13a (E-C-30 à E-C-32 ; ADR-0029 l.235 ; AQT Q1 ; Q-C-04) : processus secondaire, boucle de la carte et relevé ASN
hors de tout fil qui écrit. Horloges et attentes injectées (`test_boucle.Temps`), relevé injecté, journal relu par
`chaine`. Fenêtres : m(3) = 2026-10-04 23:01 UTC = 1791154860 (date -u -d) ; 1791154860 mod 120 = 60 (bc). CB-13b
(E-C-32, E-C-33) : `carte.json`, budget de débit partagé par hôte, règles croisées, commande `secondaire` ; isolement
du pool éprouvé de bout en bout, les deux processus ensemble, carte pendue et carte refusée."""
import json
import os
import pathlib
import socket
import subprocess
import sys
import threading
from unittest import mock

from shogen_s2bis.collecte import entree, secondaire
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import Temps, borne, rapide
from tests.test_bout_en_bout import HARNAIS, servir
from tests.test_entree import COMMIT, RACINE, configurations, port_ferme, refus
from tests.test_journal import Base, chaine
from tests.test_reprise import m, sans_chaine

NUL = {"hote": None, "a": None, "ip": None, "ripestat": None, "cymru": None}


def carte(port, n=1, **champs):
    """carte.json de test, sur la grille du pool de `configurations` (w = 1 s, δ = 0,6 s) : n formes vers 127.0.0.1,
    départ 0,05 s, délai 0,3 s (0,05 + 0,3 ≤ 1 − 0,6), marge 0,2 s ; relevé ASN toutes les 3 600 s."""
    x = {"hote": "127.0.0.1", "port": port, "methode": "GET", "corps": "", "espace": False, "decodeur": "binance_btc"}
    return {"depart": S // 20, "delai": 3 * S // 10, "marge": S // 5, "places": 4, "asn": {"periode": 3600,
            "decalage": 0}, "formes": [{**x, "nom": f"m{k}", "chemin": f"/m{k}"} for k in range(n)], **champs}


def fichiers(dossier, **contenus):
    """Écrit chaque configuration en JSON dans `dossier` ; rend {nom : chemin}."""
    for nom, donnees in contenus.items():
        pathlib.Path(dossier, nom + ".json").write_text(json.dumps(donnees), encoding="utf-8")
    return {nom: os.path.join(dossier, nom + ".json") for nom in contenus}


class Secondaire(Base):
    def tourner(self, n, releve, periode=60, decalage=0):
        """`n` fenêtres de la carte (une lecture « c ») depuis m(3), relevé de a.example et b.example à la cadence."""
        if "b" not in vars(self):
            self.temps = Temps(m(2) * S + 5 * S)
            jl = borne(self, self.journal, m(2), "secondaire")
            h = self.temps
            self.b = secondaire.Secondaire(jl, {"c": rapide}, [(0, "c")], 4, ["b.example", "a.example"], "127.0.9.53",
                                           periode, decalage, releve=releve, horloge=h, dormir=h.dormir,
                                           attendre=h.attendre, monotone=h.monotone, delta=55 * S)
        borne(self, self.b.tourner, n)
        return [(e["type"], e.get("ws"), e.get("hote", e.get("lance"))) for e in sans_chaine(chaine(
            self.etat()["secondaire-2026-10-04-0.jsonl"])[2])[1:]]

    def test_carte_part_a_ws_plus_5_secondes_sans_sondes(self):     # E-C-32 : hors de δ, D-1 à D-5 du pool
        self.tourner(1, lambda h, r: {**NUL, "hote": h}, periode=86400, decalage=0)
        lecture, sante = [e for e in sans_chaine(chaine(self.etat()["secondaire-2026-10-04-0.jsonl"])[2]) if e[
            "type"] in ("lecture", "sante")]
        self.assertEqual((lecture["prevu"], lecture["forme"], sante["d3"], sante["d4"], sante["d5"], sante["disque"]),
                         ((m(3) + 5) * S, "c", None, [], [], None))

    def test_releve_au_demarrage_et_instant_saute_rattrape(self):     # C-4 de la G2 de P2A (Q-2), E-C-15
        """Cadence de 120 s, décalage nul : m(4) et m(6) sont des instants de la cadence, m(3) non (mod 120 = 60).
        Relevé à la première fenêtre de l'exécution, m(3) ; m(4) sautée (horloge portée au-delà de son échéance) :
        rattrapé à m(5), fenêtre lue suivante ; m(6) à sa cadence ; m(7), rien."""
        for avance in (None, (m(5) + 1) * S, None, None):
            if avance:
                self.temps.avancer(avance)
            vus = self.tourner(1, lambda h, r: {**NUL, "hote": h}, periode=120)
            if self.b.fil:
                self.b.fil.join(5)
        self.assertEqual(([(w, x) for t, w, x in vus if t == "releve_asn"], [w for t, w, _x in vus if t == "lecture"]),
                         ([(m(3), True), (m(5), True), (m(6), True)], [m(3), m(5), m(6), m(7)]))

    def test_releve_hors_du_fil_qui_ecrit_jamais_relance_en_double(self):     # E-C-31, Q-C-04
        """Relevé pendu : la boucle écrit ses marqueurs, le relevé dû ensuite est sauté (`lance` faux) ; rendu, chaque
        hôte s'écrit en `asn` en tête de la fenêtre suivante, par le fil de la boucle, hôtes dans l'ordre."""
        porte, fils = threading.Event(), set()
        self.addCleanup(porte.set)

        def releve(h, resolveur):
            fils.add(threading.current_thread())
            porte.wait()
            return {**NUL, "hote": h, "ip": resolveur}
        bloc = [("lecture", m(3), None), ("sante", m(3), None), ("marqueur", m(3), None)]
        self.assertEqual(self.tourner(2, releve), [("releve_asn", m(3), True), *bloc, ("releve_asn", m(4), False),
                                                     *[(t, m(4), x) for t, _w, x in bloc]])
        porte.set()
        self.b.fil.join(5)
        self.assertEqual(self.tourner(1, releve)[8:11], [("asn", m(5), "a.example"), ("asn", m(5), "b.example"),
                                                         ("releve_asn", m(5), True)])
        self.b.fil.join(5)
        self.assertEqual((len(fils), threading.current_thread() in fils, self.b.fil in fils), (2, False, True))
        ecrits = chaine(self.etat()["secondaire-2026-10-04-0.jsonl"])[2]
        self.assertEqual([e["ip"] for e in ecrits if e["type"] == "asn"], ["127.0.9.53"] * 2)   # résolveur transmis

    def test_releve_a_la_cadence_scellee_defaut_note_sans_arret(self):        # E-C-30 : cadence, échec typé
        """Période de 120 s, décalage de 60 s : relevé à m(3) et m(5) seulement ; un relevé qui lève (défaut imprévu)
        donne un `asn` à `a` null pour son hôte, et le relevé continue."""
        def releve(h, resolveur):
            if h == "a.example":
                raise RuntimeError("défaut imprévu")
            return {**NUL, "hote": h, "ip": "192.0.2.1"}
        for _i in range(4):                                         # relevé joint à chaque fenêtre : déterministe
            vus = [x for x in self.tourner(1, releve, periode=120, decalage=60) if x[0] in ("releve_asn", "asn")]
            if self.b.fil:
                self.b.fil.join(5)
        self.assertEqual(vus[:2], [("releve_asn", m(3), True), ("asn", m(4), "a.example")])
        self.assertEqual(vus[2:], [("asn", m(4), "b.example"), ("releve_asn", m(5), True), ("asn", m(6), "a.example"),
                                   ("asn", m(6), "b.example")])
        e = [x for x in sans_chaine(chaine(self.etat()["secondaire-2026-10-04-0.jsonl"])[2]) if x["type"] == "asn"]
        self.assertEqual([(x["a"], x["ip"]) for x in e[:2]], [(None, None), (None, "192.0.2.1")])


class Configuration(Base):                                         # CB-13b (E-C-32, E-C-33 ; FORMAT §15.2)
    def test_carte_budget_partage_et_regles_croisees(self):
        """Pool de deux formes sur 127.0.0.1 (w = 1 s, δ = 0,6 s). Carte de trois formes sur cet hôte : 5 lectures par
        fenêtre, admis ; quatre : 6 > 5 (PAR_HOTE), `budget-partage` ; carte vide admise ; hôte espacé d'un côté :
        `espace-partage`. Départ + délai = 0,4 s = w − δ : admis ; 1 µs de plus, ou deux lectures espacées de 1 s :
        `hors-delta`. Marge, cadence (grille de 60 s), décodeur : refus nommés ; `periode` de 86 401 s : borne."""
        f, _s, d = configurations(1)
        g, x = {**f, "w": 60}, carte(1)["formes"][0]
        e = [{**x, "hote": "b.example", "espace": True, "nom": n} for n in ("m0", "m1")]     # décalages 0 et 1 s
        cas = [(f, carte(1, 3), None), (f, carte(1, 4), "budget-partage"), (f, carte(1, 0), None),
               (f, carte(1, formes=[{**x, "espace": True}]), "espace-partage"), (f, carte(1, depart=S // 10), None),
               (f, carte(1, depart=S // 10 + 1), "hors-delta"), (f, carte(1, formes=e), "hors-delta"),
               (f, carte(1, marge=S), "marge-carte"), (f, carte(1, formes=[{**x, "decodeur": "x"}]), "decodeur-connu")]
        cas += [(f, carte(1, asn={"periode": 3600, "decalage": 3600}), "cadence"),
                (g, carte(1, asn={"periode": 3600, "decalage": 60}), None),
                (g, carte(1, asn={"periode": 90, "decalage": 0}), "cadence"),
                (g, carte(1, asn={"periode": 3600, "decalage": 30}), "cadence"),
                (f, carte(1, asn={"periode": 86401, "decalage": 0}), "CONFIG/borne : $.asn.periode")]    # C-2 (G20)
        for formes, c, regle in cas:
            with self.subTest(regle=regle, carte=c):
                r = refus(lambda: entree.configurer_secondaire(fichiers(self.d, formes=formes, carte=c, descripteur=d),
                                                               COMMIT))
                self.assertEqual(r and r.split(" = ")[0], regle and (regle if "/" in regle else
                                                                     "CONFIG/incoherent : " + regle))

    def test_construction_journal_propre_hors_delta_sans_sondes(self):
        """Journal `secondaire` sur la grille du pool ; départ ws + `depart` (δ de la carte : w − `depart`), échéance
        ws + w − `marge`, sans sondes ; délai et places de la carte jusqu'aux lectures ; hôtes du pool et de la carte,
        résolveur du descripteur, cadence de `asn`."""
        f, _s, d = configurations(1)
        c = carte(1, 2, delai=S // 4, marge=S // 8, places=3)
        c["formes"] = [{**x, "hote": "b.example"} for x in c["formes"]]
        jl, b = entree.construire_secondaire(f, c, d, self.d)
        with mock.patch.object(entree.http, "lire") as lire:
            b.lectures["m1"]({})
        self.assertEqual((jl.prefixe, jl.dossier, jl.w, b.journal, b.w, b.delta, b.marge, b.sondes, b.plan,
                          lire.call_args.args[0][:2], lire.call_args.kwargs.get("delai")),
                         ("secondaire", self.d, 1, jl, 1, S - S // 20, S // 8, None, [(0, "m0"), (0, "m1")],
                          ("b.example", "/m1"), S // 4))
        self.assertEqual((b.hotes, b.resolveur, b.periode, b.decalage, [b.places.acquire(blocking=False) for _ in
                                                                         range(4)]),
                         (["127.0.0.1", "b.example"], "127.0.9.53", 3600, 0, [True] * 3 + [False]))


class Isolement(Base):                                             # E-C-32 ; PROPOSITION §2.4, processus secondaire
    def test_carte_pendue_ou_refusee_le_pool_intact(self):
        """Pool et secondaires ensemble, trois fenêtres (w = 1 s) : la carte lit un serveur qui accepte et ne répond
        jamais ; un second secondaire, au budget dépassé, sort en 2 sans rien écrire. Le journal du pool ne porte que
        ses lectures (a, b, c), aucun fil abandonné, trois marqueurs ; celui du secondaire, sa lecture en panne."""
        pendu, tenues = socket.create_server(("127.0.0.1", 0)), []
        self.addCleanup(lambda: [x.close() for x in (pendu, *tenues)])

        def tenir():
            try:
                while True:
                    tenues.append(pendu.accept()[0])
            except OSError:                                         # serveur fermé à la fin du test
                return
        threading.Thread(target=tenir, daemon=True).start()
        f, s, d = configurations(servir(self))
        f["formes"].append({**f["formes"][0], "nom": "c", "port": port_ferme(), "chemin": "/c"})
        s["commande"], s["delai"], d["config_resolveur"] = ["/bin/echo", "suivi"], S // 5, os.path.join(self.d, "r")
        ch = fichiers(self.d, formes=f, sante=s, descripteur=d, carte=carte(pendu.getsockname()[1]), trop=carte(1, 4))
        lancer, dossiers = [], {}
        for nom, cmd, cfg in (("pool", "pool", ("formes", "sante", "descripteur")), ("sec", "secondaire", ("formes",
                              "carte", "descripteur")), ("trop", "secondaire", ("formes", "trop", "descripteur"))):
            os.mkdir(dossiers.setdefault(nom, os.path.join(self.d, "j-" + nom)))
            args = [x for c in cfg for x in ("--" + c.replace("trop", "carte"), ch[c])]
            lancer.append(subprocess.Popen([sys.executable, "-B", "-c", HARNAIS, cmd, *args, "--journal", dossiers[nom],
                                            "--commit", COMMIT, "--fenetres", "3"], cwd=RACINE, stderr=subprocess.PIPE))
            self.addCleanup(lambda p=lancer[-1]: (p.kill(), p.wait(), p.stderr.close()))
        refuse = [b"collecte", b"refus", b"CONFIG/incoherent", b"budget-partage"]
        self.assertEqual([(p.communicate(timeout=60)[1].strip().split(b" : "), p.returncode) for p in lancer],
                         [([b""], 0), ([b""], 0), (refuse, 2)])
        lus = {n: chaine(b"".join(pathlib.Path(x, y).read_bytes() for y in sorted(os.listdir(x)) if y.endswith(
            ".jsonl")))[2] if os.listdir(x) else [] for n, x in dossiers.items()}
        lectures = [[(e["forme"], e["statut"]) for e in lus[n] if e["type"] == "lecture"] for n in ("pool", "sec")]
        self.assertEqual(lectures, [[("a", "ok"), ("b", "panne_http"), ("c", "panne_transport")] * 3,
                                    [("m0", "panne_transport")] * 3])
        self.assertEqual(([e["fils"]["abandonnes"] for e in lus["pool"] if e["type"] == "sante"], [len([e for e in lus[
            n] if e["type"] == "marqueur"]) for n in ("pool", "sec")], lus["trop"]), ([0] * 3, [3, 3], []))
