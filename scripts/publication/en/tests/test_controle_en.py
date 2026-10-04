# -*- coding: utf-8 -*-
"""Tests du contrôle de la traduction anglaise (lot DOCS11-EN), écrits avant le module.

Valeurs attendues posées à la main sur de petits documents (source française, traduction anglaise) et un glossaire
réduit ; aucune n'est tirée du module testé. Aucune barre oblique inverse dans ce fichier : NL = chr(10).
"""
import collections
import contextlib
import hashlib
import io
import os
import tempfile
import types
import unittest

import controle_en as ce

NL = chr(10)
TAB = chr(9)


def donnees_mini(**changes):
    d = types.SimpleNamespace(
        ENTETE_BROUILLON="**Draft — not published.**",
        ENTETE_PHRASE="PHRASE.",
        ENTETE_MENTION="MENTION.",
        ENTETE_CONVENTIONS="*Translation conventions.*",
        GLOSSAIRE_TITRE="## Glossary (French → English)",
        GLOSSAIRE_A="### A. Kept",
        GLOSSAIRE_B="### B. Terms",
        TITRES=[("# Titre FR", "# Title EN"), ("## 1. Section", "## 1. Section")],
        GLOSES=[("G-01", "NE REJETTE PAS", "does not reject", ""),
                ("G-02", "« R1 discrimine » = FAUX", "“R1 discriminates” = false", ""),
                ("G-14", "« ok = 0 / 24585 lectures »", "ok = 0 / 24585 readings", "")],
        REGEX_LIBELLES={"G-01": "NE REJETTE PAS"},
        NEUTRES=[],
        COUVERTS=[("R1 discrimine", "G-02", "")],
        CITATIONS_TRADUITES=[("C-11", "L'arrêter (Recommandé)", "Stop it (Recommended)", "")],
        PROTEGES=[("P-11", "NE REJETTE PAS", "NE REJETTE PAS")],
        LIBELLES_COMPTES={"FAUX": "FAUX"},
        TERMES=[("flux", "feed", "")],
        EXCEPTIONS_REGISTRE=[],
        SOURCE_SHA256=hashlib.sha256(SOURCE.encode("utf-8")).hexdigest(),
    )
    for cle, valeur in changes.items():
        setattr(d, cle, valeur)
    return d


SOURCE = NL.join([
    "# Titre FR",
    "",
    "> Paragraphe d'en-tête avec 2,5 et 1 709.",
    "",
    "## 1. Section",
    "",
    "Texte **« R1 discrimine » = FAUX** et NE REJETTE PAS. Les deux strates : 24 585 fenêtres, "
    "« ok = 0 / 24585 lectures ».",
    "",
    "- Point « L'arrêter (Recommandé) » avec `code 2,33`.",
    "",
    "| a | b |",
    "|---|---|",
    "| calme | 0,5 |",
    "",
    "```text",
    "sortie « calme » : 2,33",
    "```",
    "",
])

PARA_EN = ("Text **« R1 discrimine » = FAUX** [*“R1 discriminates” = false*] and NE REJETTE PAS [*does not reject*]. "
           "The two strata: 24,585 windows, « ok = 0 / 24585 lectures » [*ok = 0 / 24585 readings*].")
ITEM_EN = "- Item “Stop it (Recommended)” with `code 2,33`."

CORPS_EN = [
    "# Title EN",
    "",
    "> **Draft — not published.** PHRASE. MENTION.",
    ">",
    "> *Translation conventions.* Kept outputs stay in French.",
    "",
    "> Header paragraph with 2.5 and 1,709.",
    "",
    "## 1. Section",
    "",
    PARA_EN,
    "",
    ITEM_EN,
    "",
    "| a | b |",
    "|---|---|",
    "| calm | 0.5 |",
    "",
    "```text",
    "sortie « calme » : 2,33",
    "```",
    "",
]
GLOSSAIRE_EN = [
    "## Glossary (French → English)",
    "",
    "### A. Kept",
    "",
    "| French, as printed | English gloss |",
    "|---|---|",
    "| NE REJETTE PAS | does not reject |",
    "| « R1 discrimine » = FAUX | “R1 discriminates” = false |",
    "| « ok = 0 / 24585 lectures » | ok = 0 / 24585 readings |",
    "",
    "### B. Terms",
    "",
    "| French | English | Note |",
    "|---|---|---|",
    "| flux | feed |  |",
    "",
]
TRAD = NL.join(CORPS_EN + GLOSSAIRE_EN)


def remplacer(texte, avant, apres):
    assert texte.count(avant) == 1, avant
    return texte.replace(avant, apres)


def contenus(spans):
    return [s[2] for s in spans]


class TestEspacesEtUnites(unittest.TestCase):
    def test_normaliser_espaces(self):
        self.assertEqual(ce.normaliser_espaces("a " + NL + "  b" + TAB + "c "), "a b c")

    def test_unites_genres_source(self):
        u = ce.unites(SOURCE)
        self.assertEqual([x.genre for x in u],
                         ["titre", "bloc", "titre", "para", "liste", "table", "table", "table", "code"])
        self.assertEqual([x.ligne for x in u], [1, 3, 5, 7, 9, 11, 12, 13, 15])

    def test_unites_genres_traduction(self):
        u = ce.unites(TRAD)
        self.assertEqual([x.genre for x in u],
                         ["titre", "bloc", "bloc", "bloc", "titre", "para", "liste", "table", "table", "table", "code",
                          "titre", "titre", "table", "table", "table", "table", "table", "titre", "table", "table",
                          "table"])

    def test_unites_continuation(self):
        u = ce.unites(NL.join(["- a", "  b", "c", "", "d"]))
        self.assertEqual([x.genre for x in u], ["liste", "para"])
        self.assertIn("c", u[0].texte)

    def test_unites_bloc_paragraphes(self):
        u = ce.unites(NL.join(["> a", ">", "> b", "", "> c"]))
        self.assertEqual([(x.genre, x.texte) for x in u], [("bloc", "a"), ("bloc", "b"), ("bloc", "c")])

    def test_unites_code_non_ferme(self):
        with self.assertRaises(ce.ErreurFatale):
            ce.unites(NL.join(["```text", "x"]))

    def test_unites_ligne_pipe_dans_paragraphe(self):
        # Ajouté à 16:2x après le premier contrôle réel : une suite de paragraphe qui commence par « | » n'est pas
        # une ligne de table (Markdown exige une ligne de délimitation).
        u = ce.unites(NL.join(["Le texte de", "|p − m|/m continue", "fin."]))
        self.assertEqual([x.genre for x in u], ["para"])

    def test_unites_table_avec_delimiteur(self):
        u = ce.unites(NL.join(["| a | b |", "|---|---|", "| 1 | 2 |", "", "|x| seul"]))
        self.assertEqual([x.genre for x in u], ["table", "table", "table", "para"])


class TestMasquageEtCitations(unittest.TestCase):
    def test_masquer_code(self):
        masque, codes = ce.masquer_code("a `x « y »` b")
        self.assertEqual(len(masque), len("a `x « y »` b"))
        self.assertNotIn("«", masque)
        self.assertEqual(codes, ["`x « y »`"])

    def test_masquer_impair(self):
        with self.assertRaises(ce.ErreurFatale):
            ce.masquer_code("a `x b")

    def test_gloses(self):
        self.assertEqual(contenus(ce.gloses("« plage incluse » [*range included*] puis [calc] et [2 1 1 6]")),
                         ["range included"])

    def test_retirer_gloses(self):
        self.assertEqual(ce.retirer_gloses("A [*b c*] D [*e*]"), "A D")

    def test_citations_fr_imbriquees(self):
        self.assertEqual(contenus(ce.citations_fr("« a « b » c » et « d »")), ["a « b » c", "d"])

    def test_citations_fr_ignorent_code(self):
        self.assertEqual(contenus(ce.citations_fr("`« x »` « y »")), ["y"])

    def test_citations_fr_espaces(self):
        self.assertEqual(contenus(ce.citations_fr("« a" + NL + "  b »")), ["a b"])

    def test_citations_fr_non_fermee(self):
        with self.assertRaises(ce.ErreurFatale):
            ce.citations_fr("« a")

    def test_citations_en(self):
        self.assertEqual(contenus(ce.citations_en("“a ‘b’ c” and « “d” » [*“e”*]")), ["a ‘b’ c"])

    def test_citations_en_vide_ignoree(self):
        self.assertEqual(contenus(ce.citations_en("rendered as “ ” here")), [])


class TestNombres(unittest.TestCase):
    def test_fr_decimale(self):
        self.assertEqual(ce.normaliser_nombres("≈ 20,8 et 2,33", "fr"), "≈ 20.8 et 2.33")

    def test_fr_groupe(self):
        self.assertEqual(ce.normaliser_nombres("35 982 = 24 585 + 11 397", "fr"), "35982 = 24585 + 11397")

    def test_fr_vecteur(self):
        attendu = collections.Counter()
        for n in ["52", "320", "423", "23790"]:
            attendu[("c", n)] += 1
            attendu[("d", n)] += 1
        self.assertEqual(ce.jetons(ce.normaliser_nombres("[52 320 423 23790]", "fr")), attendu)

    def test_fr_virgule_espace(self):
        self.assertEqual(ce.normaliser_nombres("l.435547, l.435551", "fr"), "l.435547, l.435551")

    def test_en_groupe(self):
        self.assertEqual(ce.normaliser_nombres("35,982 and 1,709", "en"), "35982 and 1709")

    def test_en_decimale(self):
        self.assertEqual(ce.normaliser_nombres("2.33 and 0.00136", "en"), "2.33 and 0.00136")

    def test_brut(self):
        self.assertEqual(ce.normaliser_nombres("2,33 et 24 585", "brut"), "2,33 et 24 585")

    def test_jetons(self):
        attendu = collections.Counter({("c", "J28"): 1, ("d", "28"): 1, ("c", "l.435522"): 1, ("d", "435522"): 1,
                                       ("c", "10⁻⁵⁰"): 1, ("d", "10"): 1})
        self.assertEqual(ce.jetons("J28 l.435522 10⁻⁵⁰"), attendu)

    def test_jetons_unite_egaux(self):
        fr = ce.Unite("para", "Sur 24 585 fenêtres, z ≈ 20,8 « ok = 0 / 24585 lectures ».", 1)
        en = ce.Unite("para", "On 24,585 windows, z ≈ 20.8 « ok = 0 / 24585 lectures » [*ok = 0 / 24585 readings*].",
                      1)
        self.assertEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(en, "en"))

    def test_jetons_unite_ecart(self):
        fr = ce.Unite("para", "Sur 24 585 fenêtres.", 1)
        en = ce.Unite("para", "On 24,586 windows.", 1)
        self.assertNotEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(en, "en"))

    def test_jetons_unite_glose_exclue(self):
        fr = ce.Unite("para", "« ok = 0 »", 1)
        en = ce.Unite("para", "« ok = 0 » [*ok = 0 / 99999*]", 1)
        self.assertEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(en, "en"))

    def test_jetons_unite_code_brut(self):
        fr = ce.Unite("para", "a `2,33`", 1)
        self.assertNotEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(ce.Unite("para", "a `2.33`", 1), "en"))
        self.assertEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(ce.Unite("para", "a `2,33`", 1), "en"))

    def test_jetons_unite_citation_gardee_fr(self):
        fr = ce.Unite("para", "« 2,5 » et 3,5", 1)
        en = ce.Unite("para", "« 2,5 » and 3.5", 1)
        self.assertEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(en, "en"))

    def test_mots_nombres_fr_en(self):
        attendu = collections.Counter({"2": 1, "3": 1, "1er": 1})
        self.assertEqual(ce.mots_nombres("les deux strates, trois paires, le premier sceau, un G0 neuf", "fr"),
                         attendu)
        self.assertEqual(ce.mots_nombres("both strata, three pairs, the first seal, a new G0", "en"), attendu)

    def test_mots_nombres_ecart(self):
        self.assertNotEqual(ce.mots_nombres("deux strates, trois paires", "fr"),
                            ce.mots_nombres("two strata, four pairs", "en"))

    def test_mots_composes_non_comptes(self):
        # Ajouté après le premier contrôle réel : un mot-nombre lié par un trait d'union (« third-party »,
        # « half-open ») est un adjectif composé, pas un compte.
        self.assertEqual(ce.mots_nombres("third-party recomputation, half-open segment, one-minute", "en"),
                         collections.Counter())
        self.assertEqual(ce.mots_nombres("the third test", "en"), collections.Counter({"3e": 1}))

    def test_mots_tiers_non_compte(self):
        # Ajouté après le deuxième contrôle réel : « third party » rend le nom « tiers », pas un ordinal.
        self.assertEqual(ce.mots_nombres("a third party who is given", "en"), collections.Counter())
        self.assertEqual(ce.mots_nombres("third parties", "en"), collections.Counter())
        self.assertEqual(ce.mots_nombres("the third value", "en"), collections.Counter({"3e": 1}))

    def test_mots_unite_zones(self):
        fr = ce.Unite("para", "les deux strates « seconde coupe »", 1)
        en = ce.Unite("para", "the two strata « seconde coupe » [*second cut*]", 1)
        self.assertEqual(ce.mots_unite(fr, "fr"), ce.mots_unite(en, "en"))
        self.assertEqual(ce.mots_unite(en, "en"), collections.Counter({"2": 1, "2e": 1}))


class TestMotifsRegistreConventionResidus(unittest.TestCase):
    def test_motifs_chemins(self):
        for s in ["see C:/Users/x", "under /tmp/a", "the scratchpad", "docs/rapports/x", "Pocket network"]:
            self.assertTrue(ce.motifs_trouves(s), s)

    def test_motifs_anglais(self):
        for s in ["Pyth was dead", "handed to the orchestrator", "not on my PC", "provided with this report",
                  "Position first"]:
            self.assertTrue(ce.motifs_trouves(s), s)

    def test_motifs_propre(self):
        self.assertEqual(ce.motifs_trouves("The rule returns a value per stratum."), [])

    def test_registre_locutions(self):
        for s in ["independent sources", "verified data", "the correct price", "it proves the price",
                  "nobody measures independence", "guaranteed", "validated"]:
            hits = ce.registre_en(s, [])
            self.assertTrue([h for h in hits if not h[3]], s)

    def test_registre_bornes(self):
        self.assertEqual(ce.registre_en("the verifier and independent windows and unverified", []), [])

    def test_registre_k_sources(self):
        self.assertEqual([h[3] for h in ce.registre_en("10 sources / 11 feeds", [])], [False])
        exc = [("k sources", "10 sources / 11 feeds", "motif")]
        self.assertEqual([h[3] for h in ce.registre_en("10 sources / 11 feeds", exc)], [True])

    def test_zones_anglaises(self):
        self.assertEqual(ce.normaliser_espaces(ce.zones_anglaises("« donnée vraie » `x` “y z” [*w*] t")),
                         "“y z” [*w*] t")

    def test_convention(self):
        formes = [f for f, _ in ce.convention_en("≈ 20,8 and 35 982 and 1,709 and [52 320 423 23790] and 0,5")]
        self.assertEqual(formes, ["20,8", "35 982", "0,5"])

    def test_residus(self):
        self.assertEqual([m for m, _ in ce.residus_francais("the value of la règle and NE REJETTE PAS",
                                                             ["NE REJETTE PAS"])], ["la"])

    def test_residus_identifiants(self):
        self.assertEqual(ce.residus_francais("SHOGEN-FLUX-QUASI-MORT-1 and des_x and `le`", []), [])


class TestGlosesEtCitationsGardees(unittest.TestCase):
    def corps(self, texte=TRAD):
        return ce.corps(texte, donnees_mini())

    def test_gloses_ok(self):
        self.assertEqual(ce.controle_gloses(self.corps(), SOURCE, donnees_mini()), [])

    def test_glose_absente(self):
        t = remplacer(TRAD, "NE REJETTE PAS [*does not reject*]", "NE REJETTE PAS")
        self.assertTrue(ce.controle_gloses(self.corps(t), SOURCE, donnees_mini()))

    def test_glose_pas_a_la_premiere(self):
        t = remplacer(TRAD, "Header paragraph with", "Header paragraph NE REJETTE PAS with")
        self.assertTrue(ce.controle_gloses(self.corps(t), SOURCE, donnees_mini()))

    def test_glose_inconnue(self):
        t = remplacer(TRAD, "The two strata:", "The two strata [*foo*]:")
        self.assertTrue(ce.controle_gloses(self.corps(t), SOURCE, donnees_mini()))

    def test_glose_double(self):
        t = remplacer(TRAD, "- Item", "- Item NE REJETTE PAS [*does not reject*]")
        self.assertTrue(ce.controle_gloses(self.corps(t), SOURCE, donnees_mini()))

    def test_glose_nombres(self):
        d = donnees_mini(GLOSES=[("G-01", "NE REJETTE PAS", "does not reject", ""),
                                 ("G-02", "« R1 discrimine » = FAUX", "“R1 discriminates” = false", ""),
                                 ("G-14", "« ok = 0 / 24585 lectures »", "ok = 0 / 24586 readings", "")])
        t = remplacer(TRAD, "[*ok = 0 / 24585 readings*]", "[*ok = 0 / 24586 readings*]")
        self.assertTrue(ce.controle_gloses(ce.corps(t, d), SOURCE, d))

    def test_citation_gardee_non_couverte(self):
        t = remplacer(TRAD, "“Stop it (Recommended)”", "« L'arrêter (Recommandé) »")
        self.assertTrue(ce.controle_gloses(self.corps(t), SOURCE, donnees_mini()))

    def test_citation_gardee_modifiee(self):
        t = remplacer(TRAD, "« ok = 0 / 24585 lectures » [*", "« ok = 0 / 24585 lecture » [*")
        problemes = ce.controle_gloses(self.corps(t), SOURCE, donnees_mini())
        self.assertTrue([p for p in problemes if "nouvelle ou modifiée" in p], problemes)


class TestAlignementEtUnites(unittest.TestCase):
    def paires(self, texte=TRAD, d=None):
        d = d or donnees_mini()
        corps, entete, glossaire, problemes = ce.separer(ce.unites(texte), d)
        paires, pb = ce.aligner(ce.unites(SOURCE), corps, d)
        return paires, problemes + pb

    def test_aligner_ok(self):
        paires, pb = self.paires()
        self.assertEqual(pb, [])
        self.assertEqual(len(paires), 9)

    def test_aligner_unite_manquante(self):
        t = remplacer(TRAD, ITEM_EN + NL + NL, "")
        _, pb = self.paires(t)
        self.assertTrue(pb)

    def test_titre_non_conforme(self):
        paires, _ = self.paires(remplacer(TRAD, "## 1. Section", "## 1. Part"))
        self.assertTrue(ce.controle_structure(paires, donnees_mini()))

    def test_code_modifie(self):
        paires, _ = self.paires(remplacer(TRAD, "sortie « calme » : 2,33", "sortie « calme » : 2.33"))
        self.assertTrue(ce.controle_structure(paires, donnees_mini()))

    def test_table_cellules(self):
        paires, _ = self.paires(remplacer(TRAD, "| calm | 0.5 |", "| calm | 0.5 | x |"))
        self.assertTrue(ce.controle_structure(paires, donnees_mini()))

    def test_structure_ok(self):
        paires, _ = self.paires()
        self.assertEqual(ce.controle_structure(paires, donnees_mini()), [])

    def test_nombres_par_unite_ok(self):
        paires, _ = self.paires()
        self.assertEqual(ce.controle_nombres(paires), [])

    def test_nombres_par_unite_ecart(self):
        paires, _ = self.paires(remplacer(TRAD, "24,585 windows", "24,586 windows"))
        problemes = ce.controle_nombres(paires)
        self.assertTrue([p for p in problemes if "inventés" in p], problemes)

    def test_nombres_deplaces(self):
        t = remplacer(TRAD, "The two strata: 24,585 windows,", "The two strata: windows,")
        t = remplacer(t, "with `code 2,33`.", "with `code 2,33` 24,585.")
        paires, _ = self.paires(t)
        self.assertTrue(ce.controle_nombres(paires))

    def test_nombres_echanges_dans_une_unite(self):
        # Ajouté après la relecture (resserrage) : un échange de deux nombres dans une même unité garde le
        # multiensemble ; l'ordre des nombres par unité le révèle.
        fr = ce.Unite("para", "EMD_s ≈ 196 en calme et ≈ 211 en stress.", 1)
        en_bon = ce.Unite("para", "EMD_s ≈ 196 in calm and ≈ 211 in stress.", 1)
        en_echange = ce.Unite("para", "EMD_s ≈ 211 in calm and ≈ 196 in stress.", 1)
        self.assertEqual(ce.controle_nombres([(fr, en_bon)]), [])
        self.assertEqual(ce.jetons_unite(fr, "fr"), ce.jetons_unite(en_echange, "en"))
        self.assertTrue(ce.controle_nombres([(fr, en_echange)]))

    def test_mots_nombres_par_unite(self):
        paires, _ = self.paires(remplacer(TRAD, "The two strata:", "The three strata:"))
        self.assertTrue(ce.controle_nombres(paires))

    def test_citations_ok(self):
        paires, _ = self.paires()
        self.assertEqual(ce.controle_citations(paires, donnees_mini()), [])

    def test_citation_traduite_absente(self):
        paires, _ = self.paires(remplacer(TRAD, "“Stop it (Recommended)”", "“Stop it”"))
        self.assertTrue(ce.controle_citations(paires, donnees_mini()))

    def test_citation_fr_non_declaree(self):
        paires, _ = self.paires()
        problemes = ce.controle_citations(paires, donnees_mini(CITATIONS_TRADUITES=[]))
        self.assertTrue([p for p in problemes if "non déclarée" in p], problemes)

    def test_code_en_ligne_par_unite(self):
        paires, _ = self.paires(remplacer(TRAD, "with `code 2,33`.", "with `code 2,34`."))
        self.assertTrue(ce.controle_structure(paires, donnees_mini()))


class TestProtegesEnteteGlossaire(unittest.TestCase):
    def test_proteges_ok(self):
        self.assertEqual(ce.controle_proteges(SOURCE, ce.corps(TRAD, donnees_mini()), donnees_mini()), [])

    def test_proteges_ecart(self):
        t = remplacer(TRAD, "and NE REJETTE PAS [*", "and DOES NOT REJECT [*")
        self.assertTrue(ce.controle_proteges(SOURCE, ce.corps(t, donnees_mini()), donnees_mini()))

    def test_libelles_ecart(self):
        t = remplacer(TRAD, "**« R1 discrimine » = FAUX** [*", "**« R1 discrimine » = false** [*")
        self.assertTrue(ce.controle_libelles(SOURCE, ce.corps(t, donnees_mini()), donnees_mini()))

    def test_libelles_espaces_normalises(self):
        # Ajouté après le deuxième contrôle réel : un libellé coupé par un retour à la ligne dans la source compte.
        d = donnees_mini(LIBELLES_COMPTES={"R1 discrimine": "R1 discrimine"})
        self.assertEqual(ce.controle_libelles("« R1" + NL + "discrimine »", "« R1 discrimine »", d), [])
        self.assertTrue(ce.controle_libelles("« R1" + NL + "discrimine »", "« R1 »", d))

    def test_entete_ok(self):
        _, entete, _, pb = ce.separer(ce.unites(TRAD), donnees_mini())
        self.assertEqual(pb, [])
        self.assertEqual(ce.controle_entete(entete, donnees_mini()), [])

    def test_entete_absente(self):
        t = remplacer(TRAD, "> **Draft — not published.** PHRASE. MENTION." + NL + ">" + NL, "")
        _, entete, _, pb = ce.separer(ce.unites(t), donnees_mini())
        self.assertTrue(pb)
        self.assertTrue(ce.controle_entete(entete, donnees_mini()))

    def test_entete_chiffre(self):
        t = remplacer(TRAD, "PHRASE. MENTION.", "PHRASE. MENTION. 2026.")
        _, entete, _, _ = ce.separer(ce.unites(t), donnees_mini())
        self.assertTrue(ce.controle_entete(entete, donnees_mini()))

    def test_glossaire_ok(self):
        _, _, glossaire, _ = ce.separer(ce.unites(TRAD), donnees_mini())
        self.assertEqual(ce.controle_glossaire_final(glossaire, donnees_mini()), [])

    def test_glossaire_ligne_manquante(self):
        t = remplacer(TRAD, "| « ok = 0 / 24585 lectures » | ok = 0 / 24585 readings |" + NL, "")
        _, _, glossaire, _ = ce.separer(ce.unites(t), donnees_mini())
        self.assertTrue(ce.controle_glossaire_final(glossaire, donnees_mini()))

    def test_verifier_donnees_ok(self):
        # Une donnée cohérente jugée fatale est un échec du test, pas une erreur d'exécution (contrat 0/1/3).
        try:
            ce.verifier_donnees(donnees_mini(), SOURCE)
        except ce.ErreurFatale as erreur:
            self.fail("données cohérentes jugées fatales : " + str(erreur))

    def test_verifier_donnees_forme_absente(self):
        d = donnees_mini(GLOSES=[("G-01", "NE REJETTE JAMAIS", "never rejects", "")])
        with self.assertRaises(ce.ErreurFatale):
            ce.verifier_donnees(d, SOURCE)

    def test_verifier_donnees_citation_non_couverte(self):
        with self.assertRaises(ce.ErreurFatale):
            ce.verifier_donnees(donnees_mini(CITATIONS_TRADUITES=[]), SOURCE)


class TestEpingleSource(unittest.TestCase):
    # Ajout daté du 2026-10-04 (retouche E-19 de la source française) : le glossaire épingle le sha256 de la source
    # qu'il décrit ; toute autre source est refusée (fatal), avant tout contrôle. Tests écrits avant le code.
    def test_epingle_ok(self):
        try:
            ce.verifier_epingle(donnees_mini(SOURCE_SHA256="ab" * 32), "ab" * 32)
        except ce.ErreurFatale as erreur:
            self.fail("source épinglée jugée fatale : " + str(erreur))

    def test_epingle_autre_source(self):
        with self.assertRaises(ce.ErreurFatale) as ctx:
            ce.verifier_epingle(donnees_mini(SOURCE_SHA256="ab" * 32), "cd" * 32)
        self.assertIn("cd" * 32, str(ctx.exception))
        self.assertIn("ab" * 32, str(ctx.exception))

    def test_epingle_absente(self):
        d = donnees_mini()
        del d.SOURCE_SHA256
        with self.assertRaises(ce.ErreurFatale):
            ce.verifier_epingle(d, "ab" * 32)


class TestMain(unittest.TestCase):
    def ecrire(self, dossier, nom, texte):
        chemin = os.path.join(dossier, nom)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        return chemin

    def lancer(self, argv, d):
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            code = ce.main(argv, donnees=d)
        return code, tampon.getvalue()

    def verdict(self, sortie):
        lignes = [l for l in sortie.split(NL) if l.startswith("VERDICT")]
        self.assertEqual(len(lignes), 1, sortie[-400:])
        return lignes[0]

    def cas(self, avant, apres, controle):
        with tempfile.TemporaryDirectory() as dossier:
            s = self.ecrire(dossier, "s.md", SOURCE)
            t = self.ecrire(dossier, "t.md", remplacer(TRAD, avant, apres))
            code, sortie = self.lancer([s, t], donnees_mini())
        self.assertEqual(code, 1)
        self.assertIn(controle, self.verdict(sortie))

    def test_main_conforme(self):
        with tempfile.TemporaryDirectory() as dossier:
            s = self.ecrire(dossier, "s.md", SOURCE)
            t = self.ecrire(dossier, "t.md", TRAD)
            code, sortie = self.lancer([s, t], donnees_mini())
        self.assertEqual(code, 0)
        self.assertIn("CONFORME", self.verdict(sortie))

    def test_main_nombres(self):
        self.cas("24,585 windows", "24,586 windows", "2. nombres")

    def test_main_nombres_deplaces(self):
        # Ajouté pendant la conception des mutants : un nombre déplacé d'une unité à l'autre garde le multiensemble
        # global ; seul le contrôle par unité le voit.
        with tempfile.TemporaryDirectory() as dossier:
            s = self.ecrire(dossier, "s.md", SOURCE)
            t = remplacer(TRAD, "The two strata: 24,585 windows,", "The two strata: windows,")
            t = self.ecrire(dossier, "t.md", remplacer(t, "with `code 2,33`.", "with `code 2,33` 24,585."))
            code, sortie = self.lancer([s, t], donnees_mini())
        self.assertEqual(code, 1)
        self.assertIn("2. nombres", self.verdict(sortie))

    def test_main_illisible(self):
        with tempfile.TemporaryDirectory() as dossier:
            t = self.ecrire(dossier, "t.md", TRAD)
            self.assertEqual(self.lancer([os.path.join(dossier, "absent.md"), t], donnees_mini())[0], 3)

    def test_main_donnees_incoherentes(self):
        with tempfile.TemporaryDirectory() as dossier:
            s = self.ecrire(dossier, "s.md", SOURCE)
            t = self.ecrire(dossier, "t.md", TRAD)
            d = donnees_mini(TITRES=[("# Autre titre", "# Title EN"), ("## 1. Section", "## 1. Section")])
            self.assertEqual(self.lancer([s, t], d)[0], 3)

    def test_main_source_non_epinglee(self):
        # Ajout daté du 2026-10-04 (E-19) : une source qui n'est pas celle du glossaire arrête le contrôle (sortie 3).
        with tempfile.TemporaryDirectory() as dossier:
            s = self.ecrire(dossier, "s.md", SOURCE)
            t = self.ecrire(dossier, "t.md", TRAD)
            code, sortie = self.lancer([s, t], donnees_mini(SOURCE_SHA256="0" * 64))
        self.assertEqual(code, 3)
        self.assertIn("FATAL", sortie)
        self.assertIn("0" * 64, sortie)

    def test_main_usage(self):
        self.assertEqual(self.lancer([], donnees_mini())[0], 3)

    def test_main_structure(self):
        self.cas("## 1. Section", "## 1. Part", "1. structure")

    def test_main_citations(self):
        self.cas("“Stop it (Recommended)”", "“Stop it”", "3. citations")

    def test_main_gloses(self):
        self.cas("NE REJETTE PAS [*does not reject*]", "NE REJETTE PAS", "4. gloses")

    def test_main_proteges(self):
        self.cas("and NE REJETTE PAS [*", "and DOES NOT REJECT [*", "5. passages protégés")

    def test_main_motif(self):
        self.cas("Header paragraph", "Header paragraph from /tmp/x", "6. motifs")

    def test_main_registre(self):
        self.cas("Header paragraph", "Verified header paragraph", "7. registre")

    def test_main_residu_francais(self):
        self.cas("Header paragraph with", "Header paragraph avec", "8. résidus")

    def test_main_convention(self):
        self.cas("| calm | 0.5 |", "| calm | 0,5 |", "9. convention")

    def test_main_entete(self):
        self.cas("PHRASE. MENTION.", "PHRASE.", "10. en-tête")

    def test_main_glossaire(self):
        self.cas("| flux | feed |  |", "| flux | feeds |  |", "11. glossaire")


if __name__ == "__main__":
    unittest.main()
