"""CB-17a, E-C-38 : lecture du journal et jugement d'une `sante` pour `status`. Journaux écrits par l'écrivain
(CB-1, CB-2) ; codes attendus écrits à la main d'après ADR-0029 §2.3 (D-1 sans santé ; D-2 retard de plus de 5 s ou
lecture non partie, règle Q-C-02 de l'AVIS ; D-4 au moins 2 témoins sans réponse ; D-5 au moins 2 noms témoins non
résolus) ; aucune ligne `lecture` décodée (PROPOSITION §2.4 « Status »). DT6-e (SHOGEN-S2BIS-CHRONYC-FORMAT-1) : D-3
jugé sur une sortie gelée de `chronyc tracking`, l'exemple de la documentation de chrony 4.6.1 (doc/chronyc.adoc
l.147-159, sha256 dc955e0f…c5a7, copié octet pour octet dans tests/fixtures/chrony/tracking.txt), bornes et variantes
écrites à la main.
CB-17b : état par fenêtre et rapport écrits à la main ; tête recalculée sur les octets du fichier ; strates par jour
UTC (stress : samedi et dimanche, ADR-0029 l.196) ; sortie identique avec et sans `lecture` ; rien d'écrit ;
commande.
CB-17c (AVIS Q-D-03, point 2) : résumés par jour écrits à la main d'après le scénario, liste blanche de leurs clés ;
commande `resume` ; grille bornée (C-3) : journaux corrompus de la G2, `status` en sous-processus borné en mémoire.
CB-17d (point 3) : compte à quorum et âges calculés à la main ; résumés hostiles refusés."""
import contextlib
import hashlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from shogen_s2bis.collecte import entree, journal, status
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_entree import configurations, port_ferme
from tests.test_reprise import m
from tests.test_tetes import sans_attente

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKING = pathlib.Path(RACINE, "tests", "fixtures", "chrony", "tracking.txt").read_text(encoding="utf-8")
D3 = {"sortie": TRACKING, "code": 0, "debut": 1, "fin": 2}


def temoin(statut="reponse"):
    """Résultat D-4 (FORMAT §12, §13.4) : réponse retenue, ou `delai`."""
    ok = statut == "reponse"
    return {"adresse": "192.0.2.1", "statut": statut, "rcode": 0 if ok else None, "tc": False if ok else None,
            "reponses": [[".", 6, 86400, ["a.", "b.", 1, 2, 3, 4, 5]]] if ok else None, "debut": 1, "fin": 2}


def nom(statut="reponse", rcode=0, reponses=(("t.example.", 1, 30, "192.0.2.7"),)):
    """Résultat D-5 : nom résolu (réponse A), rcode non nul, réponse sans A, ou aucune réponse."""
    ok = statut == "reponse"
    return {"nom": "t.example.", "statut": statut, "rcode": rcode if ok else None, "tc": False if ok else None,
            "reponses": [list(r) for r in reponses] if ok else None, "debut": 1, "fin": 2}


def sante(retard=0, non_parties=0, d4=None, d5=None, d3=D3):
    return {"d2": {"retard_max": retard, "non_parties": non_parties}, "fils": {"abandonnes": 0, "tardives": [],
            "sondes": 0}, "horloges": None, "d3": d3, "d4": d4 or [temoin()] * 3, "d5": d5 or [nom()] * 2,
            "disque": {"total": 5000, "libre": 1000}, "resolveur": "c" * 64}


def lectures_de(n, panne):
    """Lectures d'une fenêtre : `ok` ; ou, en panne, la k-ième en `panne_transport:dns` (adresse null), en
    `panne_http` (503) ou en `panne_decode`."""
    t = m(n) * S
    if not panne:
        return [Lecture("ok", t + 1, t + 2, {"dns": t + 1}, "192.0.2.9:443", code=200, octets=b"x", valeurs={"prix":
                                                                                                           "1.5"})]
    return [Lecture("panne_transport", t + 1, t + 2, {}, None, sous_type="dns"),
            Lecture("panne_http", t + 1, t + 2, {"dns": t + 1}, "192.0.2.9:443", code=503, octets=b"indisponible"),
            Lecture("panne_decode", t + 1, t + 2, {"dns": t + 1}, "192.0.2.9:443", code=200, octets=b"{")]


class LectureDuJournal(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d = d.name

    def petit_journal(self):
        """m(1) : une lecture `ok` ; m(2) : trois lectures en panne ; m(3) : aucune ; chacune suivie de `sante` et du
        marqueur."""
        jl = journal.Journal(self.d, "pool").ouvrir(m(0))
        for n, lus in ((1, lectures_de(1, False)), (2, lectures_de(2, True)), (3, [])):
            for k, lu in enumerate(lus):
                jl.ecrire("lecture", m(n), forme=f"f{k}", prevu=m(n) * S, **lu.enregistrement())
            jl.ecrire("sante", m(n), **sante())
            jl.marqueur(m(n))
        jl.fermer()

    def test_aucune_lecture_decodee(self):
        """Les lignes `lecture` (`ok`, en panne, adresse null) ne passent jamais par le décodeur JSON ; les autres sont
        rendues dans l'ordre de la chaîne (PROPOSITION §2.4 « Status »)."""
        self.petit_journal()
        vus, charger = [], json.loads
        with mock.patch.object(status.json, "loads", side_effect=lambda x: vus.append(x) or charger(x)):
            types = [e["type"] for e, _ligne in status.enregistrements(self.d)]
        self.assertEqual((types, [x for x in vus if b'"type":"lecture"' in x], len(vus)),
                         (["ouverture", "sante", "marqueur", "point"] + ["sante", "marqueur"] * 2, [], 8))

    def test_ligne_illisible_arrete_le_fichier(self):
        """Comme la lecture d'un fichier au FORMAT §7.1, la première ligne illisible (JSON coupé, objet sans `seq`,
        liste) arrête le fichier : un marqueur écrit après elle n'est pas lu ; une dernière ligne sans saut de ligne
        non plus."""
        self.petit_journal()
        sain = pathlib.Path(self.d, "pool-2026-10-04-0.jsonl").read_bytes()
        suite = b'{"prec":"' + b"0" * 64 + b'","seq":999,"type":"marqueur","ws":1791154920}\n{"prec"'
        for illisible in (b'{"x":', b'{"type":"marqueur","ws":60}', b"[1]"):
            pathlib.Path(self.d, "pool-2026-10-04-0.jsonl").write_bytes(sain + illisible + b"\n" + suite)
            self.assertEqual([e.get("ws") for e, _l in status.enregistrements(self.d)][-1], m(3), illisible)

    def test_fichier_special_non_lu_sans_attente(self):      # DT6-c, SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1 (O-4, P2B)
        """Tube nommé, puis dossier, au nom d'un fichier du journal : `status` ne l'ouvre pas en attente (le tube
        bloquait, le dossier levait IsADirectoryError) et ne le lit pas ; les autres fichiers sont rendus."""
        self.petit_journal()
        attendu = [e["type"] for e, _l in status.enregistrements(self.d)]
        chemin = os.path.join(self.d, "pool-2026-10-04-1.jsonl")
        for faire, defaire in ((os.mkfifo, os.remove), (os.mkdir, os.rmdir)):
            faire(chemin)
            self.assertEqual(sans_attente(lambda: [e["type"] for e, _l in status.enregistrements(self.d)]), attendu)
            defaire(chemin)

    def test_journal_absent(self):
        with self.assertRaises(status.RefusStatus) as r:
            list(status.enregistrements(self.d))
        self.assertEqual((r.exception.code, str(r.exception)), ("STATUS/journal", "STATUS/journal : aucun fichier du "
                                                                "journal « pool »"))


class Jugement(unittest.TestCase):
    def test_codes_d_une_sante(self):
        """Codes écrits à la main, un défaut par cas ; sans santé lisible, D-1 ; D-3 se juge sur les relevés de
        plusieurs fenêtres (`etat`, DT6-e)."""
        cas = [(sante(), []), (sante(retard=5 * S), []), (sante(retard=5 * S + 1), ["D-2"]), (sante(retard=None), []),
               (sante(retard=-S), []), (sante(non_parties=1), ["D-2"]),
               (sante(d4=[temoin("delai"), None, temoin()]), ["D-4"]),
               (sante(d4=[temoin("reseau"), temoin(), temoin()]), []),
               (sante(d5=[nom(rcode=3), nom(reponses=(("t.example.", 5, 30, "x.example."),))]), ["D-5"]),
               (sante(d5=[nom("delai"), nom()]), []), (sante(d5=[nom(reponses=()), nom(rcode=2)]), ["D-5"]),
               (sante(d3=None), []),
               (sante(retard=6 * S, non_parties=2, d4=[None] * 3, d5=[None] * 2), ["D-2", "D-4", "D-5"]),
               (None, ["D-1"]), ({"d2": {}}, ["D-1"]), ("x", ["D-1"])]
        self.assertEqual([status.juger(s) for s, _c in cas], [c for _s, c in cas])

    def test_seuils_egaux_a_ceux_du_recalcul(self):
        """Seuils de `status` égaux à ceux de `s2bis/config/analyse.json` (bloc `degradation`, lu en JSON brut)."""
        with open(os.path.join(RACINE, "config", "analyse.json"), encoding="utf-8") as f:
            g = json.load(f)["degradation"]
        self.assertEqual((status.D2, status.D4, status.D5, getattr(status, "D3_BORNE", None),
                          getattr(status, "D3_AGE", None)),
                         (g["d2_retard_s"] * S, g["d4_echecs"], g["d5_echecs"], g["d3_borne_s"] * 10 ** 9,
                          g["d3_age_s"]))


SCENARIO = {1: None, 2: sante(retard=5 * S + 1), 4: sante(d4=[temoin("delai"), None, temoin()],
            d5=[nom(rcode=3), nom(reponses=(("t.example.", 5, 30, "x.example."),))]),
            5: sante(non_parties=1, d4=[temoin("reseau"), temoin(), temoin()], d5=[nom("delai"), nom()]),
            6: "sans sante", 7: sante(retard=5 * S, d3={"erreur": "absente", "debut": 1, "fin": 2}),
            8: sante(d3={**D3, "code": 1}), 63: sante(retard=6 * S)}
INVALIDES = {1: ["D-1"], 2: ["D-2"], 4: ["D-4", "D-5"], 5: ["D-2"], 6: ["D-1"], 7: ["D-3"], 8: ["D-3"],
             63: ["D-2"]}       # SCENARIO, à la main ; m(7), m(8) : dernier relevé lisible, m(5), à 120 s et plus
NOW = (m(63) + 60 + 120) * S                                       # deux minutes après la fin de la dernière fenêtre
VEN = 1791589800                                                  # vendredi 9 octobre 2026, 23:50 UTC (G2)
ATTENDU = ["status : journal « pool », lecture seule",
           "fenêtres : de 2026-10-04 22:59 à 2026-10-05 00:01 UTC, 63 ; dernier marqueur : 2026-10-05 00:01 UTC",
           "tête : seq {seq}, sha256 {sha}",
           "disque : 1000 octets libres sur 5000",
           "dégradations : D-1 2 ; D-2 3 ; D-3 2 ; D-4 1 ; D-5 1",
           "dernière fenêtre : dégradée (D-2)",
           "fenêtres valides (compte local) : calme 1 ; stress 54"]


def ecrire_journal(d, lectures=True, panne=False):
    """Fenêtres m(1) à m(63) (22:59 le dimanche 4 octobre à 00:01 le lundi 5, UTC) : lectures (aucune, une `ok`, ou
    trois en panne), puis `sante` selon SCENARIO (valide hors scénario), puis marqueur, sauf m(1) (aucun
    enregistrement : trou déclaré au marqueur suivant)."""
    jl = journal.Journal(d, "pool").ouvrir(m(0))
    for n in range(2, 64):
        s = SCENARIO.get(n, sante())
        for k, lu in enumerate(lectures_de(n, panne) if lectures else []):
            jl.ecrire("lecture", m(n), forme=f"f{k}", prevu=m(n) * S, **lu.enregistrement())
        if s != "sans sante":
            jl.ecrire("sante", m(n), **s)
        jl.marqueur(m(n))
    jl.fermer()


def tete_du_fichier(d):
    """(seq, sha256) de la dernière ligne du dernier fichier, sans le code du collecteur."""
    derniere = pathlib.Path(d, "pool-2026-10-05-0.jsonl").read_bytes().split(b"\n")[-2] + b"\n"
    return json.loads(derniere)["seq"], hashlib.sha256(derniere).hexdigest()


class Base(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d = d.name

    def journal(self, nom_, **k):
        os.mkdir(chemin := os.path.join(self.d, nom_))
        ecrire_journal(chemin, **k)
        return chemin


class Etat(Base):
    def test_d3_jugee_sur_la_sortie_gelee(self):            # DT6-e, SHOGEN-S2BIS-CHRONYC-FORMAT-1 (ADR-0029 §2.3)
        """Une fenêtre par variante de la sortie gelée (borne de l'exemple : 0,000006523 + 0,001100737 + 0,013639022 / 2
        = 0,007926771 s, calcul à la main) : « Not synchronised », borne de 1 s exactement (0,5 + 0,25 + 0,5 / 2) puis
        d'1 ns de plus, « Invalid », « fast », « Insert second », « Delete second » : D-3 si le statut n'est pas
        Normal, Insert second ou Delete second, ou si la borne passe 1 s. Relevé illisible (ligne manquante, code 1
        ou faux, ligne en double, erreur, null, valeur sans ses neuf décimales) : la fenêtre prend le dernier relevé
        lisible d'une fenêtre commencée moins de 120 s avant elle, sinon D-3 (la première fenêtre, sans relevé
        lisible avant elle, est D-3) ; une fenêtre sans `sante` reste D-1 seul."""
        def chronyc(**champs):
            t = TRACKING
            for cle, valeur in champs.items():
                t = re.sub("(?m)^(" + cle.replace("_", " ") + " *: ).*$", lambda x: x[1] + valeur, t)
            return {**D3, "sortie": t}
        nominal = chronyc()
        un = dict(System_time="0.500000000 seconds slow of NTP time", Root_dispersion="0.250000000 seconds",
                  Root_delay="0.500000000 seconds")
        variantes = [({**D3, "code": 1}, ["D-3"]), (nominal, []), (chronyc(Leap_status="Not synchronised"), ["D-3"]),
                     (chronyc(**un), []),
                     (chronyc(**{**un, "Root_dispersion": "0.250000001 seconds"}), ["D-3"]),
                     (chronyc(Leap_status="Invalid"), ["D-3"]), (nominal, []),
                     ({**D3, "sortie": TRACKING.replace("Root delay", "Root  delay")}, []),
                     ({**D3, "code": 1}, ["D-3"]),
                     ({**D3, "sortie": TRACKING + "Leap status     : Normal" + chr(10)}, ["D-3"]),
                     ({"erreur": "absente", "debut": 1, "fin": 2}, ["D-3"]),
                     (chronyc(System_time="0.000006523 seconds fast of NTP time"), []), (None, []),
                     (chronyc(Leap_status="Insert second"), []), (chronyc(Leap_status="Delete second"), []),
                     (chronyc(System_time="1.5 seconds slow of NTP time"), []), ({**D3, "code": False}, ["D-3"])]
        jl = journal.Journal(self.d, "pool").ouvrir(VEN)
        for n, (d3, _c) in enumerate(variantes, 1):
            jl.ecrire("sante", VEN + 60 * n, **sante(d3=d3))
            jl.marqueur(VEN + 60 * n)
        jl.marqueur(VEN + 60 * 18)                          # sans `sante` : D-1 seul (dernier relevé lisible à 180 s)
        jl.fermer()
        self.assertEqual(status.etat(self.d)[0], {**{VEN + 60 * n: c for n, (_d, c) in enumerate(variantes, 1)},
                                                  VEN + 60 * 18: ["D-1"]})

    def test_jugement_par_fenetre_tete_et_releves_absents(self):
        """Chaque fenêtre de m(1) à m(63) jugée (codes écrits à la main), y compris m(1), première admise sans
        marqueur ; dernière santé, tête du dernier enregistrement ; relevés D-3 illisibles en m(7) et m(8) (DT6-e)."""
        jdir = self.journal("a")
        r = status.etat(jdir)
        self.assertEqual(r[0], {m(n): INVALIDES.get(n, []) for n in range(1, 64)})
        self.assertEqual((r[1]["ws"], r[1]["disque"], r[2:]),
                         (m(63), {"total": 5000, "libre": 1000}, (tete_du_fichier(jdir),)))

    def test_grille_bornee_par_le_jour_des_fichiers(self):
        """C-3, journaux d'un chiffre corrompu (JSON valide) de la G2 : `ws` d'un marqueur ou `suivante` portés en
        2280 (2 → 9) : la ligne est illisible, le fichier s'arrête ; `suivante` ramenée en 2001 : la grille part du jour
        du premier fichier, moins un jour (2 876 fenêtres, comptées à la main) ; un fichier au 30 février n'est pas lu.
        `status` en sous-processus, espace d'adressage borné à 512 Mio : sortie 0 en moins de 2 s."""
        borne = ("import resource, sys; resource.setrlimit(resource.RLIMIT_AS, (1 << 29, 1 << 29)); from "
                 "shogen_s2bis.collecte import entree; raise SystemExit(entree.main(sys.argv[1:]))")
        for i, (avant, apres, attendu) in enumerate((
                (b'"type":"marqueur","ws":17915', b'"type":"marqueur","ws":97915', "fenêtres : aucune fenêtre close"),
                (b'"suivante":1791589860', b'"suivante":9791589860', "fenêtres : aucune fenêtre close"),
                (b'"suivante":1791589860', b'"suivante":1000000080', "fenêtres : de 2026-10-08 00:00 à 2026-10-09 "
                 "23:55 UTC, 2876 ; dernier marqueur : 2026-10-09 23:55 UTC"))):
            os.mkdir(d := os.path.join(self.d, str(i)))
            jl = journal.Journal(d, "pool").ouvrir(VEN)
            for n in range(1, 6):
                jl.ecrire("sante", VEN + 60 * n, **sante())
                jl.marqueur(VEN + 60 * n)
            jl.fermer()
            p = pathlib.Path(d, "pool-2026-10-09-0.jsonl")
            p.write_bytes(p.read_bytes().replace(avant, apres, 1))
            pathlib.Path(d, "pool-2026-02-30-0.jsonl").write_bytes(b"")
            debut = time.monotonic()
            r = subprocess.run([sys.executable, "-B", "-c", borne, "status", "--journal", d], cwd=RACINE,
                               capture_output=True, text=True, timeout=60)
            self.assertEqual((r.returncode, r.stdout.splitlines()[1:2], r.stderr), (0, [attendu], ""))
            self.assertLess(time.monotonic() - debut, 2)


class Etendue(Base):                                # DT6-d, SHOGEN-S2BIS-STATUS-QUEUES-1 (O-3, R-B1 de P2B ; I-3)
    def test_fichiers_arretes_avant_leur_fin_nommes(self):
        """O-3 de la G2 de P2B : un fichier arrêté avant sa fin est nommé, avec son motif, en dernière ligne du rapport
        local (ligne illisible, hors FORMAT, jour postérieur au sien, ligne coupée, pas un fichier ordinaire) ; le reste
        du rapport est celui du journal sain."""
        jdir = self.journal("a")
        seq, sha = tete_du_fichier(jdir)
        posterieur = ligne({"prec": "0" * 64, "seq": 9, "type": "marqueur", "ws": 1791244800})    # 2026-10-06 00:00
        for k, octets in enumerate((b'{"x":' + bytes([10]), b"[1]" + bytes([10]), posterieur, b'{"prec"'), 1):
            pathlib.Path(jdir, f"pool-2026-10-05-{k}.jsonl").write_bytes(octets)
        os.mkfifo(os.path.join(jdir, "pool-2026-10-05-5.jsonl"))
        motifs = ("ligne illisible", "hors FORMAT", "jour postérieur au sien", "ligne coupée",
                  "pas un fichier ordinaire")
        self.assertEqual(sans_attente(lambda: status.rapport(jdir)), [x.format(seq=seq, sha=sha) for x in ATTENDU] + [
            "fichiers arrêtés avant leur fin : " + " ; ".join(f"pool-2026-10-05-{k}.jsonl ({x})" for k, x in enumerate(
                motifs, 1))])

    def test_saut_d_horloge_en_avant_refus_nomme(self):
        """R-B1 du contre-contrôle de P2B : un saut d'horloge en avant fait écrire par l'écrivain réel, sans fichier
        forgé, un fichier d'un jour lointain (2999-01-01 : 32472144000, date -u -d) ; `status` (sous-processus, 512 Mio
        d'espace d'adressage) sort en 1 sur le refus nommé STATUS/grille en moins de 2 s (avant : MemoryError, trace
        Python, en 3,6 s, mesuré)."""
        jl = journal.Journal(self.d, "pool").ouvrir(VEN)
        for ws in (VEN + 60, 32472144000):
            jl.ecrire("sante", ws, **sante())
            jl.marqueur(ws)
        jl.fermer()
        borne = ("import resource, sys; resource.setrlimit(resource.RLIMIT_AS, (1 << 29, 1 << 29)); from "
                 "shogen_s2bis.collecte import entree; raise SystemExit(entree.main(sys.argv[1:]))")
        debut = time.monotonic()
        r = subprocess.run([sys.executable, "-B", "-c", borne, "status", "--journal", self.d], cwd=RACINE,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual((r.returncode, r.stdout, r.stderr.split(" : ")[:3], "pool-2999-01-01-0.jsonl" in os.listdir(
            self.d)), (1, "", ["status", "refus", "STATUS/grille"], True))
        self.assertLess(time.monotonic() - debut, 2)

    def test_etendue_de_la_grille_a_la_borne(self):
        """Grille de 32 jours au plus : 46 080 fenêtres, de 2026-10-01 00:00 (1790812800, date -u -d ; le plancher de
        C-3, jour du premier fichier moins un jour) à 2026-11-01 23:59 : jugées ; une de plus : refus STATUS/grille.
        Lignes écrites ici, sans l'écrivain (`status` ne contrôle pas la chaîne)."""
        p = 1790812800
        ouverture = {"jour": "2026-10-02", "prec": "0" * 64, "seq": 0, "suivante": p, "type": "ouverture"}
        pathlib.Path(self.d, "pool-2026-10-02-0.jsonl").write_bytes(ligne(ouverture))
        lus = []
        for nom, ws in (("pool-2026-11-01-0.jsonl", p + 46079 * 60), ("pool-2026-11-02-0.jsonl", p + 46080 * 60)):
            pathlib.Path(self.d, nom).write_bytes(ligne({"prec": "0" * 64, "seq": 1, "type": "marqueur", "ws": ws}))
            try:
                lus.append(status.rapport(self.d)[1])
            except status.RefusStatus as e:
                lus.append(e.code)
        self.assertEqual(lus, ["fenêtres : de 2026-10-01 00:00 à 2026-11-01 23:59 UTC, 46080 ; dernier marqueur : "
                               "2026-11-01 23:59 UTC", "STATUS/grille"])

    def test_ligne_hors_format_jamais_une_trace(self):
        """I-3 du générateur de P2B : une `sante` au `disque` partiel, puis une `sante` au `ws` non entier, puis une
        `sante` sans `ws` (DT6-e), lignes JSON valides hors FORMAT : le rapport dit le disque non relevé, sans lever."""
        jl = journal.Journal(self.d, "pool").ouvrir(VEN)
        jl.ecrire("sante", VEN + 60, **{**sante(), "disque": {"libre": 1000}})
        jl.marqueur(VEN + 60)
        jl.fermer()
        self.assertEqual(sans_attente(lambda: status.rapport(self.d)[3]), "disque : non relevé ({'libre': 1000})")
        with open(os.path.join(self.d, "pool-2026-10-09-0.jsonl"), "ab") as f:
            f.write(ligne({"disque": {"total": 5}, "prec": "0" * 64, "seq": 9, "type": "sante", "ws": "x"}))
        self.assertEqual(sans_attente(lambda: status.rapport(self.d)[3]), "disque : non relevé ({'total': 5})")
        with open(os.path.join(self.d, "pool-2026-10-09-0.jsonl"), "ab") as f:
            f.write(ligne({"prec": "0" * 64, "seq": 10, "type": "sante"}))
        self.assertEqual(sans_attente(lambda: status.rapport(self.d)[3]), "disque : non relevé (None)")


class Rapport(Base):
    def test_sante_seule_jugee_et_comptee_par_strate(self):
        """Rapport écrit à la main : m(1) à m(61) le dimanche (stress), m(62) et m(63) le lundi (calme)."""
        jdir = self.journal("a")
        seq, sha = tete_du_fichier(jdir)
        self.assertEqual(status.rapport(jdir), [x.format(seq=seq, sha=sha) for x in ATTENDU])

    def test_sortie_identique_avec_et_sans_lectures(self):
        """PROPOSITION §2.4 « Status » : même sortie, hors la ligne de tête, sans lecture, avec une lecture `ok` ou
        trois en panne par fenêtre."""
        rapports = [[x for x in status.rapport(self.journal(str(i), lectures=lectures, panne=panne)) if not
                     x.startswith("tête : ")] for i, (lectures, panne) in enumerate(((False, False), (True, False),
                                                                                      (True, True)))]
        self.assertEqual((rapports[1], rapports[2]), (rapports[0], rapports[0]))

    def test_rien_n_est_ecrit_meme_pendant_l_ecriture(self):
        """Le dossier du journal est le même, octet pour octet, avant et après ; `status` lit pendant que l'écrivain
        tient le verrou, sans le prendre."""
        jdir = self.journal("a")
        avant = {n: pathlib.Path(jdir, n).read_bytes() for n in sorted(os.listdir(jdir))}
        self.assertEqual(status.rapport(jdir)[1], ATTENDU[1])
        self.assertEqual({n: pathlib.Path(jdir, n).read_bytes() for n in sorted(os.listdir(jdir))}, avant)
        jl = journal.Journal(jdir, "pool").ouvrir(m(70))             # l'écrivain reprend et tient le verrou
        self.addCleanup(jl.fermer)
        tenu = {n: pathlib.Path(jdir, n).read_bytes() for n in sorted(os.listdir(jdir))}
        self.assertEqual(status.rapport(jdir)[1], ATTENDU[1])
        self.assertEqual({n: pathlib.Path(jdir, n).read_bytes() for n in sorted(os.listdir(jdir))}, tenu)

    def test_commande_status(self):
        """`status --journal DOSSIER` : le rapport sur la sortie, code 0 ; dossier sans journal : refus, code 1."""
        jdir = self.journal("a")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(entree.main(["status", "--journal", jdir]), 0)
        self.assertEqual(out.getvalue(), "\n".join(status.rapport(jdir)) + "\n")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(entree.main(["status", "--journal", self.d]), 1)
        self.assertEqual((out.getvalue(), err.getvalue()), ("", "status : refus : STATUS/journal : aucun fichier du "
                                                                "journal « pool »\n"))


def ligne(r):
    return json.dumps(r, sort_keys=True, separators=(",", ":")).encode() + b"\n"


class Resumes(Base):
    def setUp(self):
        super().setUp()
        self.jdir = self.journal("journal")
        os.mkdir(depot := os.path.join(self.d, "depot"))
        self.depot = depot

    def test_resume_par_jour_et_liste_blanche(self):
        """Un résumé par jour UTC, ligne canonique {jour, observateur, fenetres}, chaque fenêtre [ws, codes] : clés
        fermées, aucune donnée de lecture (AVIS Q-D-03, risque : liste blanche)."""
        attendu = {"o1-2026-10-04.resume": {"jour": "2026-10-04", "observateur": "o1", "fenetres": [
            [m(n), INVALIDES.get(n, [])] for n in range(1, 62)]}, "o1-2026-10-05.resume": {
            "jour": "2026-10-05", "observateur": "o1", "fenetres": [[m(62), []], [m(63), ["D-2"]]]}}
        r = status.resumes(self.jdir, "o1")
        self.assertEqual(r, {n: ligne(x) for n, x in attendu.items()})
        for octets in r.values():
            x = json.loads(octets)
            self.assertEqual((sorted(x), {type(w) for w, _c in x["fenetres"]}, {c for _w, cs in x["fenetres"] for c in
                                                                                cs} <= set(status.CODES)),
                             (["fenetres", "jour", "observateur"], {int}, True))

    def poser(self, fichiers):
        for nom_, contenu in fichiers.items():
            pathlib.Path(self.depot, nom_).write_bytes(contenu if type(contenu) is bytes else ligne(contenu))

    def test_compte_a_quorum_ages_et_refus(self):
        """M_j ≥ 2 (ADR-0029 §2.2, pt 5) avec o2 valide hors m(10), o3 valide en m(2) et m(4) seulement ; son propre
        résumé ignoré ; un résumé hors liste blanche refusé ; âges au bout de la dernière fenêtre lue."""
        self.poser({"o2-2026-10-04.resume": {"jour": "2026-10-04", "observateur": "o2", "fenetres": [
            [m(n), ["D-1"] if n == 10 else []] for n in range(1, 62)]}, "o2-2026-10-05.resume": {
            "jour": "2026-10-05", "observateur": "o2", "fenetres": [[m(62), []], [m(63), []]]},
            "o3-2026-10-04.resume": {"jour": "2026-10-04", "observateur": "o3", "fenetres": [
                [m(2), []], [m(3), ["D-4"]], [m(4), []]]},
            "o4-2026-10-04.resume": {"jour": "2026-10-04", "observateur": "o4", "fenetres": [], "x": 1},
            "o1-2026-10-04.resume": {"jour": "2026-10-04", "observateur": "o1", "fenetres": [[m(1), []]]}})
        self.assertEqual(status.rapport(self.jdir, depot=self.depot, observateur="o1", maintenant=NOW)[7:], [
            "quorum (au moins 2 observateurs valides) : calme 1 ; stress 55",      # m(7), m(8) en D-3 ici (DT6-e)
            "résumés lus : o2 jusqu'à 2026-10-05 00:01 UTC (âge 120 s) ; o3 jusqu'à 2026-10-04 23:02 UTC (âge 3660 s)",
            "résumés refusés : o4-2026-10-04.resume (RESUME/forme)"])
        for n in ("o2-2026-10-04.resume", "o2-2026-10-05.resume", "o3-2026-10-04.resume"):
            os.remove(os.path.join(self.depot, n))
        self.assertEqual(status.rapport(self.jdir, depot=self.depot, observateur="o1", maintenant=NOW)[7:], [
            "quorum : aucun résumé d'un autre observateur lisible",
            "résumés refusés : o4-2026-10-04.resume (RESUME/forme)"])

    def test_resumes_hostiles_refuses(self):
        """Un défaut par fichier : taille, forme non canonique, clé en trop, observateur autre que le nom, ws hors du
        jour ou hors grille, booléen, code inconnu ou en double, code qui n'est pas un texte, fenêtres vides ; un jour
        hors du journal local, ou un nom en majuscules (C-6), est ignoré. Aucun résumé ne fait lever : chacun est un
        refus nommé."""
        b = {"jour": "2026-10-04", "observateur": "p1", "fenetres": [[m(2), []]]}
        cas = {"p1": (ligne(b)[:-1] + b" " * (1 << 17) + b"\n", "taille"),
               "p2": (json.dumps({**b, "observateur": "p2"}).encode() + b"\n", "forme"),
               "p3": ({**b, "observateur": "p3", "y": 0}, "forme"), "p4": ({**b, "observateur": "p5"}, "champs"),
               "p5": ({**b, "observateur": "p5", "fenetres": [[m(62), []]]}, "champs"),
               "p6": ({**b, "observateur": "p6", "fenetres": [[m(2) + 1, []]]}, "champs"),
               "p7": ({**b, "observateur": "p7", "fenetres": [[True, []]]}, "champs"),
               "p8": ({**b, "observateur": "p8", "fenetres": [[m(2), ["D-6"]]]}, "champs"),
               "p9": ({**b, "observateur": "p9", "fenetres": [[m(2), ["D-2", "D-2"]]]}, "champs"),
               "q1": ({**b, "observateur": "q1", "fenetres": []}, "champs"),
               "q3": ({**b, "observateur": "q3", "fenetres": [[m(2), [["D-1"]]]]}, "champs"),
               "q4": ({**b, "observateur": "q4", "fenetres": [[m(2), ["D-1", 1]]]}, "champs"),
               "q5": ({**b, "observateur": "q5", "fenetres": [[m(2), [{}]]]}, "champs")}
        self.poser({f"{o}-2026-10-04.resume": x for o, (x, _c) in cas.items()})
        self.poser({"q2-2026-10-99.resume": {**b, "observateur": "q2", "jour": "2026-10-99"},
                    "P2-2026-10-04.resume": {**b, "observateur": "P2", "fenetres": []}})   # lu, il serait refusé
        try:
            refus = status.rapport(self.jdir, depot=self.depot, observateur="o1", maintenant=NOW)[-1]
        except Exception as e:                                      # attrape-tout : une exception est un échec ici
            refus = f"{type(e).__name__} : {e}"
        self.assertEqual(refus, "résumés refusés : " + " ; ".join(f"{o}-2026-10-04.resume (RESUME/{c})" for o, (_x, c)
                                                                    in cas.items()))

    def test_resume_qui_n_est_pas_un_fichier(self):
        """Un tube nommé au nom d'un résumé : refus `RESUME/lecture`, sans attente (CB-15f)."""
        os.mkfifo(os.path.join(self.depot, "o2-2026-10-04.resume"))
        self.assertEqual(sans_attente(lambda: status.rapport(self.jdir, depot=self.depot, observateur="o1",
                                                             maintenant=NOW)[-2:]),
                         ["quorum : aucun résumé d'un autre observateur lisible",
                          "résumés refusés : o2-2026-10-04.resume (RESUME/lecture)"])

    def test_depot_illisible_le_compte_local_reste(self):
        """Dépôt absent : le rapport local entier, puis `quorum : dépôt illisible (<exception>)` ; le compte local est
        toujours rendu (AVIS Q-D-03, point 3) (CB-15f)."""
        local = status.rapport(self.jdir)
        self.assertEqual(sans_attente(lambda: status.rapport(self.jdir, depot=os.path.join(self.depot, "absent"),
                                                             observateur="o1", maintenant=NOW)),
                         local + ["quorum : dépôt illisible (FileNotFoundError)"])

    def test_commande_status_avec_depot(self):
        """`status` avec `--depot` et `--descripteur` ajoute le compte à quorum ; `--depot` sans `--descripteur` :
        refus, sortie 2."""
        _f, _s, o = configurations(port_ferme())
        pathlib.Path(desc := os.path.join(self.d, "descripteur.json")).write_text(json.dumps(o), encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(entree.main(["status", "--journal", self.jdir, "--depot", self.depot, "--descripteur",
                                          desc]), 0)
        self.assertEqual(out.getvalue().split("\n")[7:], ["quorum : aucun résumé d'un autre observateur lisible", ""])
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(entree.main(["status", "--journal", self.jdir, "--depot", self.depot]), 2)
        self.assertEqual(err.getvalue(), "status : refus : CONFIG/options : --depot exige --descripteur\n")

    def test_commande_resume(self):
        """`resume --journal J --depot D --descripteur F` écrit les résumés du journal, sortie 0 ; descripteur refusé :
        sortie 2 ; journal absent : sortie 1."""
        _f, _s, o = configurations(port_ferme())
        desc = os.path.join(self.d, "descripteur.json")
        pathlib.Path(desc).write_text(json.dumps(o), encoding="utf-8")

        def lancer(jdir):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = entree.main(["resume", "--journal", jdir, "--depot", self.depot, "--descripteur", desc])
            return rc, out.getvalue(), err.getvalue()
        self.assertEqual(lancer(self.jdir), (0, "resume : o1-2026-10-04.resume, o1-2026-10-05.resume\n", ""))
        self.assertEqual({n: pathlib.Path(self.depot, n).read_bytes() for n in os.listdir(self.depot)},
                         status.resumes(self.jdir, "o1"))
        self.assertEqual(lancer(self.depot)[0], 1)
        pathlib.Path(desc).write_text(json.dumps({**o, "observateur": "o-1"}), encoding="utf-8")
        self.assertEqual(lancer(self.jdir), (2, "", "resume : refus : CONFIG/incoherent : observateur-nom\n"))


if __name__ == "__main__":
    unittest.main()
