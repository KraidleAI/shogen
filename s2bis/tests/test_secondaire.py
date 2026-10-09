"""CB-13a (E-C-30 à E-C-32 ; ADR-0029 l.235 ; AQT Q1 ; Q-C-04) : processus secondaire, boucle de la carte et relevé ASN
hors de tout fil qui écrit. Horloges et attentes injectées (`test_boucle.Temps`), relevé injecté, journal relu par
`chaine`. Fenêtres : m(3) = 2026-10-04 23:01 UTC = 1791154860 (date -u -d) ; 1791154860 mod 120 = 60 (bc)."""
import threading

from shogen_s2bis.collecte import secondaire
from shogen_s2bis.collecte.lecture import S
from tests.test_boucle import Temps, borne, rapide
from tests.test_journal import Base, chaine
from tests.test_reprise import m, sans_chaine

NUL = {"hote": None, "a": None, "ip": None, "ripestat": None, "cymru": None}


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
