"""CB-13a (E-C-30 à E-C-32 ; ADR-0029 l.235 ; AQT Q1 ; Q-C-04) : processus secondaire, boucle de la carte et relevé ASN
hors de tout fil qui écrit. Horloges et attentes injectées (`test_boucle.Temps`), relevé injecté, journal relu par
`chaine`. Fenêtres : m(3) = 2026-10-04 23:01 UTC = 1791154860 (date -u -d) ; 1791154860 mod 120 = 60 (bc). CB-13b
(E-C-32, E-C-33) : `carte.json`, budget de débit partagé par hôte, règles croisées, commande `secondaire` ; isolement
du pool éprouvé de bout en bout, les deux processus ensemble, carte pendue et carte refusée."""
import contextlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import threading
from unittest import mock

from shogen_s2bis.collecte import boucle, entree, secondaire, tetes
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_boucle import Temps, borne, pendue, rapide
from tests.test_asn import CORPS as RIPESTAT, V, serveur_dns
from tests.test_bout_en_bout import CHAMPS, DNS, anomalies, brut_intact, servir
from tests.test_entree import COMMIT, RACINE, configurations, port_ferme, refus
from tests.test_journal import Base, chaine
from tests.test_reprise import m, sans_chaine

NUL = {"hote": None, "a": None, "ip": None, "ripestat": None, "cymru": None}
SECONDAIRE = """
import sys, tests
from shogen_s2bis.collecte import asn, dns, entree, http
from shogen_s2bis.collecte.lecture import S
from tests.test_http_reseau import Resolveur
dns_, rs = map(int, sys.argv[1:3])
releve = lambda h, r: asn.releve(h, r, lire=lambda q: http.lire(q, tls=None, resoudre=Resolveur(rs)),
                                 interroger=lambda a, n, t: dns.interroger(a, n, t, delai=S // 5, port=dns_))
raise SystemExit(entree.main(sys.argv[3:], tls=None, releve=releve))
"""                      # DT6-f : relevé ASN du secondaire vers des ports de boucle locale (RIPEstat, résolveur)


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

    def test_tete_du_secondaire_exportee_au_point(self):             # C-10 ; SHOGEN-S2BIS-TETE-SECONDAIRE-1
        """Avec un dépôt, la fenêtre qui clôt l'heure (m(1), `22:59`) : la tête du point du journal `secondaire` est
        exportée en `o1-secondaire.tete` (seq du point, sha256 pris au `prec` qui le suit, comme au pool) ; aucun
        enregistrement `tetes` au journal du secondaire (il reste au pool) ; `lire_tetes` la lit sous la liste
        fermée."""
        dep = tempfile.TemporaryDirectory()
        self.addCleanup(dep.cleanup)
        t = Temps(m(0) * S + 5 * S)
        jl = borne(self, self.journal, m(0), "secondaire")
        b = secondaire.Secondaire(jl, {"c": rapide}, [(0, "c")], 4, ["a.example"], "127.0.9.53", 86400, 0,
                                  releve=lambda h, r: {**NUL, "hote": h}, horloge=t, dormir=t.dormir,
                                  attendre=t.attendre, monotone=t.monotone, delta=55 * S,
                                  depot=tetes.Depot(dep.name, "o1", "secondaire"))
        borne(self, b.tourner, 2)
        enrs = chaine(self.etat()["secondaire-2026-10-04-0.jsonl"])[2]
        i = [e["type"] for e in enrs].index("point")
        attendu = {"journal": "secondaire", "observateur": "o1", "seq": enrs[i]["seq"], "sha256": enrs[i + 1]["prec"],
                   "ws": m(1)}
        self.assertEqual(("tetes" in {e["type"] for e in enrs}, enrs[i]["ws"], sorted(os.listdir(dep.name)),
                          tetes.lire_tetes(dep.name, propre="o2", liste=["o1", "o2", "o3", "o4"])),
                         (False, m(1), ["o1-secondaire.tete"], ([attendu], [], 0)))

    def test_commande_secondaire_avec_depot(self):                   # C-10
        """`secondaire --depot P` câble un dépôt au nom de l'observateur du descripteur, journal `secondaire` ; sans
        lui, aucun ; observateur o3 (le nom de test o1 ne séparerait pas un nom écrit en dur)."""
        f, _s, d = configurations(port_ferme())
        ch = fichiers(self.d, formes=f, carte=carte(1), descripteur={**d, "observateur": "o3"})
        os.mkdir(j := os.path.join(self.d, "j"))
        vus = []
        with mock.patch.object(secondaire.Secondaire, "tourner", lambda b, n: vus.append(b.depot)):
            for plus in (["--depot", self.d], []):
                self.assertEqual(entree.main(["secondaire", *[x for n in ("formes", "carte", "descripteur") for x in (
                    "--" + n, ch[n])], "--journal", j, "--commit", COMMIT, *plus]), 0)
        self.assertEqual([x and (x.dossier, x.observateur, x.journal) for x in vus],
                         [(self.d, "o3", "secondaire"), None])

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
    def test_carte_pendue_ou_refusee_le_pool_intact(self):          # C-11 (I-7 de la G2 du lot de gel)
        """Horloges et attentes injectées (`test_boucle.Temps`), lectures injectées, trois fenêtres chacun : la carte
        lit une forme pendue (lecture en panne de transport, fil abandonné à chaque fenêtre) ; puis le pool, dans le
        même processus, ses fils de carte encore pendus : il ne porte que ses lectures (a, b, c), aucun fil
        abandonné, trois marqueurs ; un secondaire au budget dépassé sort en 2 sans rien écrire. C-11 : avant, trois
        processus à w = 1 s en temps réel (faux rouge sous 3.11 : `b` en délai sous la charge) ; les deux processus
        sont séparés par le déploiement (deux unités), et la carte d'un processus réel est éprouvée par `Conformite`
        ci-dessous."""
        porte = threading.Event()
        self.addCleanup(porte.set)
        temps = [Temps(m(2) * S + 5 * S), Temps(m(2) * S + 5 * S)]
        horloges = [{"horloge": h, "dormir": h.dormir, "attendre": h.attendre, "monotone": h.monotone} for h in temps]
        jc, jp = (borne(self, self.journal, m(2), x) for x in ("secondaire", "pool"))
        carte_ = secondaire.Secondaire(jc, {"m0": pendue(porte, True)}, [(0, "m0")], 4, [], "127.0.9.53", 86400, 0,
                                       releve=lambda h, r: NUL, delta=55 * S, **horloges[0])
        def b(s):
            return Lecture("panne_http", s["depart"], s["depart"] + 9, code=503)

        def c(s):
            return Lecture("panne_transport", s["depart"], s["depart"] + 9, sous_type="connexion")
        pool = boucle.Boucle(jp, {"a": rapide, "b": b, "c": c}, [(0, "a"), (0, "b"), (0, "c")], 4, **horloges[1])
        borne(self, carte_.tourner, 3)
        borne(self, pool.tourner, 3)
        lus = {n: chaine(self.etat()[f"{n}-2026-10-04-0.jsonl"])[2] for n in ("pool", "secondaire")}
        self.assertEqual([[(e["forme"], e["statut"]) for e in lus[n] if e["type"] == "lecture"] for n in (
            "pool", "secondaire")], [[("a", "ok"), ("b", "panne_http"), ("c", "panne_transport")] * 3,
                                     [("m0", "panne_transport")] * 3])
        self.assertEqual(tuple([e["fils"]["abandonnes"] for e in lus[n] if e["type"] == "sante"] for n in (
            "pool", "secondaire")), ([0] * 3, [1, 2, 3]))
        self.assertEqual([len([e for e in lus[n] if e["type"] == "marqueur"]) for n in lus], [3, 3])
        f, _s, d = configurations(1)
        ch = fichiers(self.d, formes=f, carte=carte(1, 4), descripteur=d)
        os.mkdir(j := os.path.join(self.d, "j-trop"))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = entree.main(["secondaire", *[x for n in ("formes", "carte", "descripteur") for x in ("--" + n, ch[n])],
                              "--journal", j, "--commit", COMMIT, "--fenetres", "3"])
        self.assertEqual((rc, err.getvalue().split(" : ")[:4], os.listdir(j)), (
            2, ["collecte", "refus", "CONFIG/incoherent", "budget-partage\n"], []))


class Conformite(Base):         # DT6-g, SHOGEN-S2BIS-SECONDAIRE-CONFORMITE-1 (O-5 de la G2 de P2A ; E-C-24)
    def test_journal_secondaire_conforme_au_format(self):
        """Le processus secondaire entier en sous-processus (w = 1 s, cinq fenêtres), son relevé ASN dirigé vers des
        serveurs factices de boucle locale (résolveur : A 192.0.2.1 et 192.0.2.2, TXT « 64500 | … » ; RIPEstat en
        clair). Chaque enregistrement est contrôlé contre le FORMAT par `anomalies` (§1 à §14 ; `sante` sans sondes,
        §13.1 ; lectures de la carte aux instants du §15.3), puis contre le §15 par les règles écrites ici, sans rien
        importer du collecteur : préfixe ; `run_params` à `{formes, carte, descripteur}` ; `releve_asn` des hôtes du
        pool et de la carte, dans l'ordre ; un `asn` par hôte, en tête d'une fenêtre ; `a`, `ip`, `ripestat`, `cymru`
        d'un hôte nommé et d'une IPv4 littérale."""
        port_dns, _recues = serveur_dns(self)
        port_rs = servir(self, ((b"GET /data/prefix-overview/data.json?resource=", RIPESTAT),))
        f, _s, d = configurations(servir(self))
        f["formes"][0]["hote"], d["resolveur"], c = "localhost", "127.0.0.1", carte(f["formes"][1]["port"])
        c["formes"][0]["chemin"] = "/a"
        ch = fichiers(self.d, formes=f, carte=c, descripteur=d)
        os.mkdir(j := os.path.join(self.d, "j"))
        r = subprocess.run([sys.executable, "-B", "-c", SECONDAIRE, str(port_dns), str(port_rs), "secondaire",
                            *[x for n in ("formes", "carte", "descripteur") for x in ("--" + n, ch[n])], "--journal", j,
                            "--commit", COMMIT, "--fenetres", "5"], cwd=RACINE, capture_output=True, timeout=60)
        noms = sorted(n for n in os.listdir(j) if n.endswith(".jsonl"))
        enrs = chaine(b"".join(pathlib.Path(j, n).read_bytes() for n in noms))[2]
        champs = {**CHAMPS, "run_params": {"ws", "commit", "sha256", "python", "formes", "carte", "descripteur"},
                  "releve_asn": {"ws", "hotes", "lance"}, "asn": {"ws", "hote", "a", "ip", "ripestat", "cymru"}}
        g = {"w": f["w"], "delta": S - c["depart"], "marge": c["marge"], "formes": c["formes"]}       # §15.3
        self.assertEqual((r.returncode, r.stderr, anomalies(enrs, g, None, champs)), (0, b"", []))
        self.assertTrue(all(re.fullmatch("secondaire-[0-9]{4}-[0-9]{2}-[0-9]{2}-(0|[1-9][0-9]*)[.]jsonl", n)
                            for n in noms) and "secondaire.verrou" in os.listdir(j))                 # §15.1
        hotes, i = ["127.0.0.1", "localhost"], [k for k, e in enumerate(enrs) if e["type"] == "asn"]
        avant = {enrs[k - 1]["type"] for k in i}                                      # en tête de fenêtre (§15.4)
        self.assertEqual(([(e["hotes"], e["lance"]) for e in enrs if e["type"] == "releve_asn"][:1],
                          [enrs[k]["hote"] for k in i], avant <= {"marqueur", "point", "asn"},
                          [x["statut"] for x in enrs if x["type"] == "lecture"]),
                         ([(hotes, True)], hotes, True, ["ok"] * 5))
        lit, nom = (enrs[k] for k in i)
        lecture = champs["lecture"] - {"ws", "forme", "prevu"}
        adresses = [x[3] for x in nom["a"]["reponses"] if x[1] == 1]
        self.assertEqual((lit["a"], lit["ip"], set(nom["a"]), nom["a"]["statut"], nom["ip"], adresses),
                         (None, "127.0.0.1", DNS, "reponse", "192.0.2.1", ["192.0.2.1", "192.0.2.2"]))
        for x in (lit, nom):
            rs, cy = x["ripestat"], x["cymru"]
            self.assertEqual((set(rs), rs["statut"], rs["valeurs"], brut_intact(rs), set(cy), cy["statut"], cy["asn"]),
                             (lecture, "ok", V, True, DNS | {"asn"}, "reponse", 64500))
