"""Cas de scripts/publication/gabarit_controle.py (lot PRODUIT-R2, R2-c) : gabarits versés ; une phrase par entrée de
doc 09, écrite depuis sa colonne « interdit » ; champs, texte fixe, empreintes, R1 (gabarit synthétique) ; erreurs."""
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
OUTIL, GAB = RACINE / "scripts" / "publication" / "gabarit_controle.py", RACINE / "docs" / "publication" / "gabarits"
G = ("# R `<libre.client>`\n- k : `<rendu.k>` ; e `<sha256.rendu>` ; c `<commit.h>` ; d `<date.r>` ; v `<version.p>`\n"
     "```text\n<rendu.bloc>\n```\nfin `<libre.client>`\n")
VAL = {"libre.client": "Acme", "rendu.k": "4", "sha256.rendu": "a" * 64, "commit.h": "b" * 40,
       "date.r": "2026-10-15T23:00:00Z", "version.p": "3.11.15", "rendu.bloc": "k_eff = 4\nAS13335 x"}
INTERDITS = {11: "Verified data", 14: "donnée vérifiée", 20: "cinq sources diverses", 21: "sources indépendantes",
             22: "garantit l'indépendance", 23: "fait signé", 24: "prix correct", 25: "niveau de sécurité du lot",
             26: "k sources", 27: "prouve l'absence", 28: "personne ne mesure", 29: "diversité imposée",
             30: "qualité d'une source", 31: "attestor décentralisé", 37: "est sûr", 38: "ne peut pas paniquer",
             39: "couverture élevée", 42: "build reproductible", 43: "chaîne sécurisée", 44: "SLSA niveau 3",
             45: "CI verte donc", 51: "publiquement vérifiable", 53: "zkTLS trustless", 54: "subject normalisé",
             55: "donc deux ressources"}
PERMIS = "diversité mesurée ; modèle d'indépendance non rejeté ; vérifier une signature ; flux divers ; unsafe_code"


def lancer(gabarit, rapport, *options):
    with tempfile.TemporaryDirectory() as d:
        for nom, texte in (("g.md", gabarit), ("r.md", rapport)):
            (pathlib.Path(d) / nom).write_bytes(texte.encode("utf-8"))
        p = subprocess.run([sys.executable, "-B", str(OUTIL), d + "/g.md", d + "/r.md", *options], capture_output=True,
                           text=True, timeout=60)
    return p.returncode, p.stderr


def remplir(**autres):
    v = {**VAL, **{k.replace("_", "."): x for k, x in autres.items()}}
    return re.sub(r"<([a-z0-9.-]+)>", lambda m: v[m.group(1)], G)


class GabaritControle(unittest.TestCase):
    def test_gabarits_verses(self):
        doc04 = (RACINE / "docs" / "04-certificat-diversite.md").read_text(encoding="utf-8").split("\n")[128:139]
        for g in ("RAPPORT-CONCENTRATION-POOL.md", "RAPPORT-CONCENTRATION-POOL-EN.md"):
            texte = (GAB / g).read_text(encoding="utf-8")
            self.assertEqual(lancer(texte, texte), (0, ""), g)
            cites = re.findall(r"`(s2-harness/[^`]+?):(\d+)`\s*\(`([^`]+)`\)", texte)
            self.assertEqual(len(cites), 26, g)
            for chemin, n, nom in cites:
                self.assertIn(nom, (RACINE / chemin).read_text(encoding="utf-8").split("\n")[int(n) - 1], (chemin, n))
            bloc = [x[2:] if x.startswith("> ") else x[1:] for x in texte.split("\n") if x.startswith(">")][-11:]
            self.assertEqual(bloc, doc04, g)

    def test_mots_interdits(self):
        for ligne, phrase in INTERDITS.items():
            with self.subTest(ligne=ligne):
                texte = G.replace("# R", "# R " + phrase)
                code, err = lancer(texte, texte)
                self.assertEqual(code, 1)
                self.assertIn(f"(doc 09 l.{ligne})", err)
        self.assertEqual(lancer(*[G.replace("# R", "# R " + PERMIS)] * 2), (0, ""))

    def test_champs_et_texte_fixe(self):
        self.assertEqual(lancer(G, remplir()), (0, ""))
        for rapport, motif in ((remplir(libre_client="<libre.client>"), "ni tous remplis ni tous vides"),
                               (G.replace("fin `<libre.client>`", "fin `Acme 3, R1`"), "ni tous remplis ni tous vides"),
                               (remplir().replace("- k :", "- K :"), "changé ou absent après <libre.client>"),
                               (remplir().replace("# R", "# X"), "changé avant le premier champ"),
                               (remplir().replace("fin `Acme`", "fin `Beta`"), "<libre.client> : deux valeurs"),
                               (remplir() + "ajout", "texte en trop"), (remplir(rendu_k=""), "valeur vide"),
                               (remplir(libre_client="Acme`\n- k : `x"), "texte en trop"),
                               (remplir(libre_client="des sources indépendantes"), "(doc 09 l.21)")):
            code, err = lancer(G, rapport)
            self.assertEqual((code, motif in err), (1, True), (motif, err))

    def test_nombres_empreintes_et_r1(self):
        self.assertEqual(lancer(G, remplir(libre_client="Acme 3 [sha256.rendu l.12]")), (0, ""))
        for valeurs, motif in (({"sha256_rendu": "A" * 64}, "forme sha256"), ({"date_r": "2026-10-15"}, "forme date"),
                               ({"commit_h": "b" * 39}, "forme commit"), ({"version_p": "3.11.15+"}, "forme version"),
                               ({"libre_client": "Acme 3"}, "nombre sans empreinte"),
                               ({"libre_client": "Acme 3 [sha256.autre]"}, "nombre sans empreinte"),
                               ({"libre_client": "Acme [sha256.autre]"}, "empreinte inconnue"),
                               ({"libre_client": "Acme 3\n[sha256.rendu]"}, "nombre sans empreinte"),
                               ({"libre_client": "Acme\nR1"}, "prétention R1"),
                               ({"libre_client": "Acme, R1 mesuré"}, "prétention R1")):
            code, err = lancer(G, remplir(**valeurs))
            self.assertEqual((code, motif in err), (1, True), (motif, err))

    def test_erreurs(self):
        with tempfile.TemporaryDirectory() as d:
            (pathlib.Path(d) / "09.md").write_bytes((RACINE / "docs" / "09-vocabulaire.md").read_bytes().replace(
                "**sécurisée**".encode("utf-8"), b"x"))
            self.assertEqual(lancer(G, G, "--doc09", d + "/09.md")[0], 3)
        self.assertEqual(lancer("`<a.b><c.d>`", "`<a.b><c.d>`")[0], 3)
        self.assertEqual(lancer(G, G, "--autre")[0], 3)
