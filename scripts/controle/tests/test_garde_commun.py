"""Cas de garde_commun.py (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout GF-0), rouges sur l'erreur
réelle reproduite, verts sur le cas sain. GF-1 : horloge et heures. E14 : vers 04:18 et 04:22 écrits à 04:14 ; le
2026-10-02 : une heure écrite 19:5x. L'horloge est fixée par un faux `date` dans le PATH, jamais par une variable.
GF-4 : interdits (E19, LA-N08), racines, analyse d'un diff, disque (E4 : 222 Mio vus par un agent).
GF-3 : citations (E16 : citation inexacte d'une ligne du JOURNAL ; LA-N08 : citation d'un interdit).
GF-4b : lignes ajoutées de l'index, dans un dépôt git temporaire (tests/aide_garde.py), sans lire un interdit.
Relecture G2 : C-5 (référence de citation écrite en code) ; C-11 (heures d'une plage).
Contre-contrôle : R-9 (date en code)."""
import collections
import os
import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock

import garde_commun as gc
from tests import aide_garde as ag


def ag_ecrire(d, fichiers):
    for chemin, texte in fichiers.items():
        os.makedirs(os.path.dirname(os.path.join(d, chemin)), exist_ok=True)
        with open(os.path.join(d, chemin), "w", encoding="utf-8") as f:
            f.write(texte)

NL = chr(10)
H = datetime(2026, 10, 10, 4, 14, tzinfo=timezone.utc)      # E14 : il était 04:14:00


def codes(texte, horloge=H):
    return [(n, c) for n, c, _x in gc.horodatages_fautifs(texte, horloge)]


class Heures(unittest.TestCase):
    def test_e14_heures_futures(self):
        """E14 : refus du mandataire daté vers 04:18 et page des actes datée 04:22, écrits à 04:14 : deux refus."""
        texte = NL.join(["Refus du mandataire le 2026-10-10 vers 04:18 UTC.", "Page des actes, 2026-10-10 04:22."])
        self.assertEqual(codes(texte), [(1, "heure-future"), (2, "heure-future")])
        self.assertEqual(gc.horodatages_fautifs(texte, H)[1][2], "2026-10-10 04:22")

    def test_heure_approchee(self):
        """2026-10-02 : 19:5x écrit hors guillemets ; 21:2x et 19:xx aussi ; 19:50 et 1:5x (pas une heure) non."""
        texte = NL.join(["le 2026-10-02 vers 19:5x UTC", "à 21:2x puis 19:xx", "à 19:50, version 1:5x"])
        self.assertEqual(codes(texte), [(1, "heure-approchee"), (2, "heure-approchee"), (2, "heure-approchee")])

    def test_borne_tolerance(self):
        """Tolérance de 120 s : 04:16 et 04:16:00 admis à 04:14:00, 04:16:01 refusé ; secondes lues."""
        self.assertEqual(codes("2026-10-10 04:16 et 2026-10-10 04:16:00 et 2026-10-10T04:13:59Z"), [])
        self.assertEqual(codes("le 2026-10-10 à 04:16:01"), [(1, "heure-future")])

    def test_autres_jours(self):
        """Une date d'un autre jour n'est pas jugée (échéance, veille) ; la date la plus proche de l'heure compte."""
        self.assertEqual(codes("2026-10-11 09:00 ; 2026-10-09 23:59"), [])
        self.assertEqual(codes("du 2026-10-09 au 2026-10-10 04:22"), [(1, "heure-future")])

    def test_exemptions(self):
        """Mot de plan dans les 40 caractères d'avant, code et guillemets français : rien n'est jugé."""
        g, d = chr(171), chr(187)
        texte = NL.join(["prévu le 2026-10-10 05:00", "jalon : 2026-10-10 05:00", "`2026-10-10 05:00` et `19:5x`",
                         g + " écrit le 2026-10-10 05:00, vers 19:5x " + d])
        self.assertEqual(codes(texte), [])

    def test_c11_plages(self):
        """C-11 : seconde heure d'une plage écrite après la date du jour (de 04:10 à 04:22, 04:10-04:22) : refus,
        l'extrait va de la date à l'heure ; plage passée, comme celle de refus-mandataire.txt : rien ; heure approchée
        écrite en X majuscule : vue."""
        self.assertEqual(codes("le 2026-10-10 de 04:10 à 04:22"), [(1, "heure-future")])
        self.assertEqual(codes("le 2026-10-10 04:10-04:22"), [(1, "heure-future")])
        self.assertEqual(codes("le 2026-10-10 entre 04:11:39 et 04:13:17 UTC"), [])
        extrait = gc.horodatages_fautifs("le 2026-10-10 de 04:10 à 04:22", H)[0][2]
        self.assertEqual(extrait, "2026-10-10 de 04:10 à 04:22")
        self.assertEqual(codes("vers 19:5X, puis 21:XX"), [(1, "heure-approchee"), (1, "heure-approchee")])

    def test_r9_date_en_code(self):
        """R-9 : date du jour en code ou citée, heure future écrite hors du code : refus, extrait de la date à
        l'heure ; date et heure dans le même code (extrait de journal) : rien."""
        self.assertEqual(codes("ajout daté du `2026-10-10` 04:22 UTC"), [(1, "heure-future")])
        self.assertEqual(codes(G + " lu le 2026-10-10 " + D + " à 04:22"), [(1, "heure-future")])
        self.assertEqual(gc.horodatages_fautifs("`2026-10-10` 04:22", H)[0][2], "2026-10-10` 04:22")
        self.assertEqual(codes("journal : `2026-10-10 04:22 démarrage`"), [])

    def test_horloge_lue_par_date_u(self):
        """L'horloge vient de `date -u` (faux `date` en tête du PATH), jamais de l'horloge de Python."""
        with tempfile.TemporaryDirectory() as d:
            faux = os.path.join(d, "date")
            with open(faux, "w", encoding="utf-8") as f:
                f.write(NL.join(["#!/bin/sh", 'if [ "$1" = -u ]; then echo 2031-02-03T04:05:06Z;',
                                 "else echo 2031-02-03T09:09:09Z; fi", ""]))
            os.chmod(faux, 0o755)
            with mock.patch.dict(os.environ, {"PATH": d + os.pathsep + os.environ.get("PATH", "")}):
                self.assertEqual(gc.maintenant(), datetime(2031, 2, 3, 4, 5, 6, tzinfo=timezone.utc))


class Interdits(unittest.TestCase):
    def test_e19_copies_et_formes(self):
        """E19, LA-N08 : un interdit est vu dans toute copie (composants), en casse pliée, en *.jsonl ; 150- non."""
        for c in ["docs/rapports/carto.md", "/tmp/x/docs/rapports/a.md", "docs/15-x.md", "DOCS/Rapports/a",
                  "docs/adr-0028/execution/p.md", "copie/docs/adr-0025/a.md", "a/b/t.jsonl", "docs/pocket-report/x"]:
            self.assertTrue(gc.chemin_interdit(c), c)
        for c in ["docs/150-x.md", "docs/adr-0028/revue-fuzz/a.md", "docs/rapport.md", "rapports/a.md", "x.json"]:
            self.assertFalse(gc.chemin_interdit(c), c)

    def test_une_seule_source_et_d2(self):
        """Liste lue dans enforcement/docs-sha256sums.py ; noms de D.2 lus dans fm11.py, jamais affichés, jugés sous le
        dernier composant scratchpad (le chemin du scratchpad de la session en porte un)."""
        motifs, d2 = gc.interdits()
        self.assertEqual(len(motifs), 7)
        simples = [r.pattern for r in d2 if r.pattern.replace("-", "").replace("_", "").isalnum()]
        self.assertGreater(len(simples), 10)
        for i, m in enumerate(simples):
            self.assertTrue(gc.chemin_interdit("copie/" + m + ".md"), f"motif de D.2 n° {i}")
            self.assertTrue(gc.chemin_interdit("/s/scratchpad/" + m + ".md"), f"motif de D.2 n° {i}")
            self.assertFalse(gc.chemin_interdit("/s/" + m + "/scratchpad/a.md"), f"motif de D.2 n° {i}")
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "docs", "rapports"))
            os.symlink(os.path.join(d, "docs", "rapports"), os.path.join(d, "lien"))
            self.assertTrue(gc.chemin_interdit(os.path.join(d, "lien", "a.md")))

    def test_racines(self):
        """Jamais de parcours depuis /, le dépôt ou un ancêtre, un dossier docs ou un interdit."""
        r = gc.RACINE_OUTILS
        for x in ["/", r, os.path.dirname(r), "/tmp/x/docs", os.path.join(r, "docs", "adr-0028")]:
            self.assertTrue(gc.racine_dangereuse(x), x)
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(gc.racine_dangereuse(d))
        self.assertFalse(gc.racine_dangereuse(os.path.join(r, "scripts", "controle")))

    def test_lignes_ajoutees_sans_interdit(self):
        """Fichier interdit indexé dans un dépôt temporaire : son contenu n'est jamais lu ; numéros des lignes."""
        with tempfile.TemporaryDirectory() as t:
            d, env = ag.depot(t, {"a.md": NL.join(["un", "deux", ""])})
            ag.ecrire(d, {"a.md": NL.join(["un", "neuf", "deux", "fin", ""]), "docs/rapports/r.md": "MARQUE"})
            ag.git(d, env, "add", "-A")
            with mock.patch.dict(os.environ, env, clear=True):
                fichiers, caches = gc.lignes_ajoutees(d)
        self.assertEqual(caches, 1)
        self.assertEqual([(f["apres"], f["ajouts"]) for f in fichiers], [("a.md", [(2, "neuf"), (4, "fin")])])
        self.assertEqual([b[:4] for b in fichiers[0]["blocs"]], [(1, 0, 2, 1), (2, 0, 4, 1)])
        self.assertNotIn("MARQUE", repr(fichiers))

    def test_analyse_diff_de_worker(self):
        """Diff à trois lignes de contexte : lignes ajoutées numérotées, blocs, fichier nouveau ; un --- dans un bloc
        est une ligne retirée, non un en-tête."""
        diff = NL.join(["diff --git a/x.md b/x.md", "index 1..2 100644", "--- a/x.md", "+++ b/x.md", "@@ -1,4 +1,4 @@",
                        " a", "--- tiret", "+b", " c", " d", "@@ -10,2 +10,3 @@", " j", "+k", " l",
                        "diff --git a/n.md b/n.md", "new file mode 100644", "--- /dev/null", "+++ b/n.md",
                        "@@ -0,0 +1,2 @@", "+x", "+y", ""])
        f, n = gc.analyser_diff(diff)
        self.assertEqual((f["avant"], f["apres"], f["ajouts"]), ("x.md", "x.md", [(2, "b"), (11, "k")]))
        self.assertEqual([b[:4] for b in f["blocs"]], [(1, 4, 1, 4), (10, 2, 10, 3)])
        self.assertEqual((n["avant"], n["apres"], n["ajouts"]), (None, "n.md", [(1, "x"), (2, "y")]))


class Disque(unittest.TestCase):
    def test_e4_seuils(self):
        """E4 : 222 Mio vus par un agent ; refus sous 3 Gio, avertissement sous 6 Gio ; --min-go ne fait que serrer."""
        usage = collections.namedtuple("usage", "total used free")
        cas = [(222 / 1024, None, "refus"), (2.9, None, "refus"), (3.1, None, "avertissement"),
               (5.9, None, "avertissement"), (6.1, None, "ok"), (6.1, 8, "refus"), (2.9, 1, "refus")]
        for gio, mini, attendu in cas:
            with mock.patch.object(gc.shutil, "disk_usage", return_value=usage(1, 1, int(gio * 2 ** 30))):
                self.assertEqual(gc.etat_disque("/", mini)[0], attendu, (gio, mini))


G, D = chr(171), chr(187)
JOURNAL = NL.join(["l." + str(i) for i in range(1, 143)] + [
    "les questions techniques routées vers les advisors : Q-FUZZ-1 rangée parmi elles", "suite de la phrase",
    "ligne 145", "ligne 146 l’apostrophe courbe", ""])


class Citations(unittest.TestCase):
    def juger(self, texte, brut=False):
        with tempfile.TemporaryDirectory() as d:
            ag_ecrire(d, {"JOURNAL.md": JOURNAL, "docs/rapports/a.md/x": "", "b.md": "un" + NL})
            refus, avert = gc.citations(texte, d)
        return (refus, avert) if brut else ([(n, c) for n, c, _r in refus], [(n, c) for n, c, _r in avert])

    def test_e16_forme_stricte_refusee(self):
        """E16 : citation inexacte d'une ligne du JOURNAL, forme stricte : refus ; forme de E16 (JOURNAL l.143) :
        avertissement compté (avis c.4 adopté)."""
        cit = G + " Q-FUZZ-1 routée vers les advisors " + D
        self.assertEqual(self.juger(cit + " (JOURNAL.md:143)"), ([(1, "citation-absente")], []))
        self.assertEqual(self.juger("x" + NL + cit + " (JOURNAL l.143)"), ([], [(2, "citation-libre-absente")]))

    def test_citations_exactes(self):
        """Mot pour mot, entre les lignes N-2 et M+2, fragments coupés par points de suspension dans l'ordre,
        apostrophe courbe contre droite, sur deux lignes ; forme libre exacte : avertissement citation-libre."""
        textes = [G + " questions techniques routées " + D + " (JOURNAL.md:143)",
                  G + " routées vers […] rangée parmi " + D + " (JOURNAL.md:143-144)",
                  G + " phrase ligne 145 " + D + " (JOURNAL.md:143)", G + " l'apostrophe " + D + " (JOURNAL.md:144)",
                  G + " rangée parmi" + NL + "elles suite " + D + " (JOURNAL.md:143)"]
        for t in textes:
            self.assertEqual(self.juger(t), ([], []), t)
        self.assertEqual(self.juger(G + " suite de la phrase " + D + " (JOURNAL l.144)"), ([], [(1, "citation-libre")]))

    def test_c5_reference_en_code(self):
        """C-5 : forme stricte écrite avec la référence en code (`chemin:N` ou `chemin`:N) : refus si la citation est
        inexacte (E16), rien si elle est exacte ; forme libre au nom en code : nom résolu (avertissement)."""
        cit = G + " Q-FUZZ-1 routée vers les advisors " + D
        for ref in (" (`JOURNAL.md:143`)", " (`JOURNAL.md`:143)"):
            self.assertEqual(self.juger(cit + ref), ([(1, "citation-absente")], []), ref)
        self.assertEqual(self.juger(G + " questions techniques routées " + D + " (`JOURNAL.md:143`)"), ([], []))
        self.assertEqual(self.juger(cit + " (`JOURNAL.md` l.143)"), ([], [(1, "citation-libre-absente")]))

    def test_citations_fausses(self):
        """Hors de la fenêtre, fragments dans le désordre, ligne hors du fichier : refus ; chemin introuvable :
        avertissement ; LA-N08 : citation d'un interdit refusée sans ouverture (le chemin est un dossier)."""
        cas = [(G + " ligne 146 " + D + " (JOURNAL.md:143)", "citation-absente"),
               (G + " rangée parmi […] questions techniques " + D + " (JOURNAL.md:143)", "citation-absente"),
               (G + " questionstechniques " + D + " (JOURNAL.md:143)", "citation-absente"),
               (G + " un " + D + " (b.md:2)", "reference-hors-fichier"),
               (G + " texte du rapport " + D + " (docs/rapports/a.md:3)", "citation-interdite")]
        for t, code in cas:
            self.assertEqual(self.juger(t), ([(1, code)], []), t)
        self.assertEqual(self.juger(G + " un " + D + " (absent.md:1)"), ([], [(1, "reference-introuvable")]))
        self.assertNotIn("rapports", repr(self.juger(G + " x " + D + " (docs/rapports/a.md:1)", brut=True)))
