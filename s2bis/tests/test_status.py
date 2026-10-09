"""CB-17a, E-C-38 : lecture du journal et jugement d'une `sante` pour `status`. Journaux écrits par l'écrivain
(CB-1, CB-2) ; codes attendus écrits à la main d'après ADR-0029 §2.3 (D-1 sans santé ; D-2 retard de plus de 5 s ou
lecture non partie, règle Q-C-02 de l'AVIS ; D-4 au moins 2 témoins sans réponse ; D-5 au moins 2 noms témoins non
résolus ; D-3 non jugé : format de `chronyc` non lu sur pièce, SHOGEN-S2BIS-CHRONYC-FORMAT-1) ; aucune ligne `lecture`
décodée (PROPOSITION §2.4 « Status »)."""
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from shogen_s2bis.collecte import journal, status
from shogen_s2bis.collecte.lecture import S, Lecture
from tests.test_reprise import m

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D3 = {"sortie": "suivi\n", "code": 0, "debut": 1, "fin": 2}


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

    def test_journal_absent(self):
        with self.assertRaises(status.RefusStatus) as r:
            list(status.enregistrements(self.d))
        self.assertEqual((r.exception.code, str(r.exception)), ("STATUS/journal", "STATUS/journal : aucun fichier du "
                                                                "journal « pool »"))


class Jugement(unittest.TestCase):
    def test_codes_d_une_sante(self):
        """(codes, relevé D-3 absent ou en erreur) écrits à la main, un défaut par cas ; sans santé lisible, D-1."""
        cas = [(sante(), [], False), (sante(retard=5 * S), [], False), (sante(retard=5 * S + 1), ["D-2"], False),
               (sante(retard=None), [], False), (sante(retard=-S), [], False), (sante(non_parties=1), ["D-2"], False),
               (sante(d4=[temoin("delai"), None, temoin()]), ["D-4"], False),
               (sante(d4=[temoin("reseau"), temoin(), temoin()]), [], False),
               (sante(d5=[nom(rcode=3), nom(reponses=(("t.example.", 5, 30, "x.example."),))]), ["D-5"], False),
               (sante(d5=[nom("delai"), nom()]), [], False), (sante(d5=[nom(reponses=()), nom(rcode=2)]), ["D-5"],
                                                              False),
               (sante(d3=None), [], True), (sante(d3={"erreur": "delai", "debut": 1, "fin": 2}), [], True),
               (sante(d3={**D3, "code": 1}), [], True),
               (sante(retard=6 * S, non_parties=2, d4=[None] * 3, d5=[None] * 2), ["D-2", "D-4", "D-5"], False),
               (None, ["D-1"], False), ({"d2": {}}, ["D-1"], False), ("x", ["D-1"], False)]
        self.assertEqual([status.juger(s) for s, _c, _a in cas], [(c, a) for _s, c, a in cas])

    def test_seuils_egaux_a_ceux_du_recalcul(self):
        """Seuils de `status` égaux à ceux de `s2bis/config/analyse.json` (bloc `degradation`, lu en JSON brut)."""
        with open(os.path.join(RACINE, "config", "analyse.json"), encoding="utf-8") as f:
            g = json.load(f)["degradation"]
        self.assertEqual((status.D2, status.D4, status.D5), (g["d2_retard_s"] * S, g["d4_echecs"], g["d5_echecs"]))


if __name__ == "__main__":
    unittest.main()
