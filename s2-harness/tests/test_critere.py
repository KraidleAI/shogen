"""Lot CRITERE d'ADR-0028 (A-1, A-3, A-4) : règle SHOGEN-CRITERE-R1-1 (texte : ADR-0028 §1 bis.1, pts 1-11),
r1.regle_critere et sa section au bloc 3 de report.py. Attendus écrits à la main et scellés avant le code
(fichier scellé du G1 §2, journal §4.2 ; FM-3.3) : table unitaire sur des strates au schéma de r1_out, puis
fixtures du collecteur réel (w = 60 s, la panne seule écart), valeurs en fractions ; ℓ ≠ 240 par la couture
de B-DEP-2 (D-10). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import contextlib
import os
import re
import tempfile
import unittest
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import count
from unittest import mock

from shogen_s2 import r1, r2, report
from tests import test_rendu_blocs as trb
from tests.test_blocs import d50
from tests.test_collector import BY_ID, SKELETON as FL
from tests.test_exclusion import cli
from tests.test_pool_analyse import fixture_b
from tests.test_rendu_blocs import E45, SAM, couture, journal, proche

S1, NN, NEUF = "NON ÉVALUABLE", "NE REJETTE PAS", "2.32" + "9" * 49      # NEUF : 2,33 − 10⁻⁵¹
TETE = ("  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; "
        "comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur")
FAMILLE = ("  famille de Bonferroni pré-enregistrée (ADR-0028 D2 pt 4) : m = {} (strates testées : {} ; "
           "m ≤ 2 ; §1 bis.1 pt 6), tests unilatéraux au seuil 2,33 ; borne P(au moins un rejet à tort) ≤ "
           "2 × 0,01 = 0,02 sous le modèle nul joint (§1 bis.1 pt 7) : modèle d'indépendance du pool de "
           "doc 10 §5.1 et dépendance sérielle des fenêtres de portée < ℓ = 240 (A(window-dependence), "
           "registre 08) ; niveau asymptotique, non démontré ≤ 0,01 en échantillon fini "
           "(SHOGEN-SIM-NIVEAU-1)")
R1D = "  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = "
AX = ("axes panne / staleness (résidu : staleness fail-open : kraken ; hors-enveloppe non évaluable : 500 "
      "cellules (fenêtre, flux))")    # SHOGEN-AXES-ENONCE-1 (b) ; J1, J2 : N = 3 < 4, (200 − 50)·2 + 200 cellules
EMD = (r"EMD_s = \(2,33 \+ 0,8416\)·max\(√\(n_s·P̂_more,s·\(1 − P̂_more,s\)\), σ̂_bloc,s\) = (\S+) "
       r"fenêtres ; fraction de n_s = (\S+) \(puissance 0,8 : choix de conception ; aucun seuil sur l'EMD\)")
NRJ = (f"« le modèle d'indépendance n'est pas rejeté sur 200 fenêtres, {AX} » ; un résultat négatif est "
       "un résultat")
NQ = " → NON ÉVALUABLE : rejet non qualifiable : niveau non tenu sous dépendance sérielle"
LAB = " (z_s ≤ −2,33 : hors famille, sans conclusion)"


def blk(z, zb, garde="16", s2="9", n=1000) -> dict:
    """Strate au schéma de r1_out["strates"][s], clés lues par la règle seules (fichier scellé, §2.1)."""
    return {"z": None if z is None else D(z), "n": n, "gate_value": D(garde),
            "bloc": {"z_bloc": None if zb is None else D(zb), "sigma2_bloc": D(s2)}}


U = {"U1": (blk(None, "3", "5", "1", 100), S1, "garde_5_4", None),
     "U2": (blk("2.33", "3"), "REJETTE", "rejette", None),
     "U3": (blk("3", "2.33"), "REJETTE", "rejette", None),
     "U4": (blk(NEUF, "5"), NN, "z_sous_seuil", "12.6864"),
     "U5": (blk("3", NEUF, s2="25"), NN, "discordance", "15.8580"),
     "U6": (blk("3", None), S1, "rejet_non_qualifiable", None),
     "U7": (blk("-3", None), NN, "z_sous_seuil", "12.6864"),
     "U8": (blk("1", "5"), NN, "z_sous_seuil", "12.6864")}


def deux(oc: int, os_: int):
    """Fixtures J1, J2 : coinbase en panne aux rangs j < 50, kraken aux rangs o ≤ j < o + 50 (o = oc en calme,
    os_ en stress), bitstamp jamais ; K = max(0, 50 − o)."""
    def panne(f, st, j):
        o = os_ if st else oc
        return j < 50 if f == "coinbase" else f == "kraken" and o <= j < o + 50
    return panne


def rotation(f: str, st: bool, j: int) -> bool:
    """Fixture J3 : en calme, deux flux sur trois en panne à chaque fenêtre (FL[j mod 3] répond) ; rien en
    stress."""
    return not st and f != FL[j % 3]


def ell(n: int):
    """ℓ = 240 : chemin de production, sans couture ; sinon la couture r1.bloc_strate de B-DEP-2 (D-10)."""
    return contextlib.nullcontext() if n == 240 else couture(n)


def regle(c: str, j: str, n: int = 240) -> tuple:
    with ell(n):
        out = r1.recompute_from_journal(c, j)
    return out, r1.regle_critere(out)


def rendu(c: str, j: str, n: int = 240) -> tuple:
    """(lignes de la section règle par strate, ligne « R1 discrimine », lignes de famille) du bloc 3 ; la
    section suit la ligne A(window-dependence) et une ligne vide."""
    with ell(n):
        b3 = report.render_report(c, j).split("[BLOC 3]")[1].split("[BLOC 4]")[0].split("\n")
    h, par = b3.index(TETE), {}
    assert b3[h - 1] == "" and b3[h - 2].startswith("  A(window-dependence)"), b3[h - 2:h]
    for ln in b3[h + 1:]:
        m = re.match(r"    « (\w+) » : (.*)$", ln)
        if not m:
            break
        par.setdefault(m.group(1), []).append(m.group(2))
    return par, b3[h + 1 + sum(map(len, par.values()))], [ln for ln in b3 if ln.startswith("  famille de B")]


def bloc3(txt: str) -> str:
    """Bloc 3 du rapport rendu, entre « [BLOC 3] » et « [BLOC 4] »."""
    return txt.split("[BLOC 3]")[1].split("[BLOC 4]")[0]


class TestRegleTable(unittest.TestCase):
    def test_table_de_verite_par_strate(self):
        """U1 à U8. Rougit si : « ≥ » remplacé par « > » sur z_s (U2) ou sur z_bloc (U3) ; arrondi avant
        comparaison (U4, U5) ; z_bloc ignoré (U5, U6) ; z_s ignoré (U8) ; garde §5.4 ignorée (U1) ; EMD omis
        ou sur la seule erreur-type binomiale (U5)."""
        for nom, (b, v, cas, emd) in U.items():
            e = r1.regle_critere({"strates": {"a": b}})["strates"]["a"]
            self.assertEqual((e["valeur"], e["cas"]), (v, cas), nom)
            att = (None, None) if emd is None else (D(emd), D(emd) / 1000)
            self.assertEqual((e["emd"], e["emd_fraction"]), att, nom)

    def test_r1_discrimine_m_et_poolee(self):
        """C1 à C7. Rougit si : rejet non qualifiable sans effet sur FAUX (C3) ; m statique ; strate poolée
        parmi les entrées de la règle (C7) ; strates qui rejettent non nommées."""
        u = {k: v[0] for k, v in U.items()}
        for st, d, rej, tst, nq in (({"a": u["U2"], "b": u["U6"]}, "VRAI", ["a"], ["a"], ["b"]),
                                    ({"a": u["U4"], "b": u["U1"]}, "FAUX", [], ["a"], []),
                                    ({"a": u["U4"], "b": u["U6"]}, S1, [], ["a"], ["b"]),
                                    ({"a": u["U5"], "b": u["U8"]}, "FAUX", [], ["a", "b"], []),
                                    ({}, S1, [], [], []), ({"a": u["U1"], "b": u["U1"]}, S1, [], [], [])):
            g = r1.regle_critere({"strates": st})
            self.assertEqual((g["r1_discrimine"], g["rejette"], g["testees"], g["m"], g["non_qualifiables"]),
                             (d, rej, tst, len(tst), nq), list(st))
        g = r1.regle_critere({"strates": {"a": u["U4"]}, "poolee": {"z_pool": D(9), "variance": D(1)}})
        self.assertEqual((list(g["strates"]), g["r1_discrimine"], g["m"]), (["a"], "FAUX", 1))


class TestRegleFixtures(unittest.TestCase):
    """Fixtures journal J1 à J3 (fichier scellé §2.2) : collecteur réel → journal → compute_r1 → règle."""

    @classmethod
    def setUpClass(cls):
        cls.j1, cls.j2 = journal(200, 200, deux(25, 29)), journal(200, 200, deux(50, 37))
        cls.j3 = journal(54, 10, rotation)

    def test_j1_couture_l1_rejette_et_discordance(self):
        """ℓ = 1 : calme REJETTE (z² = 40/3, z_bloc² = 50/7) ; stress discordance (z² = 2312/375, z_bloc² =
        14450/3759, EMD² = 236324725119/1250000000) ; VRAI [calme], m = 2. Rougit si : z_bloc ignoré ;
        « > » à la place de « ≥ »."""
        out, g = regle(*self.j1, 1)
        for st, z2, zb2 in (("calme", F(40, 3), F(50, 7)), ("stress", F(2312, 375), F(14450, 3759))):
            b = out["strates"][st]
            self.assertTrue(proche(str(b["z"]), z2, True) and proche(str(b["bloc"]["z_bloc"]), zb2, True), st)
        self.assertEqual([(e["valeur"], e["cas"]) for e in g["strates"].values()],
                         [("REJETTE", "rejette"), (NN, "discordance")])
        self.assertTrue(proche(str(g["strates"]["stress"]["emd"]), F(236324725119, 1250000000), True))
        self.assertEqual((g["r1_discrimine"], g["rejette"], g["m"]), ("VRAI", ["calme"], 2))

    def test_j1_production_rejet_non_qualifiable(self):
        """ℓ = 240, sans couture : n = 200 < 7 200, z_bloc non publiée, z_s ≥ 2,33 dans les deux strates :
        rejet non qualifiable, NON ÉVALUABLE, m = 0. Rougit si : z_bloc ignoré ; non qualifiable lu FAUX."""
        _out, g = regle(*self.j1)
        self.assertEqual([e["cas"] for e in g["strates"].values()], ["rejet_non_qualifiable"] * 2)
        self.assertEqual((g["r1_discrimine"], g["m"], g["non_qualifiables"]), (S1, 0, ["calme", "stress"]))

    def test_j2_k0_negatif_et_emd_sigma_bloc(self):
        """ℓ = 240 : calme K = 0, z ≤ −2,33 (z² = 40/3), EMD² = 188607123/1600000 (garde) ; stress K = 13,
        z² = 8/375, σ̂²_bloc = 2064751/48000 > garde, z_bloc non publiée, EMD² = 43269638424597/10¹¹ (C-7) ;
        FAUX, m = 2. Rougit si : EMD sur la seule erreur-type binomiale ; K = 0 ou z négatif non testés."""
        out, g = regle(*self.j2)
        c, s = out["strates"]["calme"], out["strates"]["stress"]
        self.assertTrue(proche(str(c["z"]), F(40, 3), True) and c["z"] < 0)
        self.assertTrue(proche(str(s["z"]), F(8, 375), True))
        self.assertEqual(s["bloc"]["sigma2_bloc"], d50(2064751, 48000))
        for st, emd2 in (("calme", F(188607123, 1600000)), ("stress", F(43269638424597, 10 ** 11))):
            e = g["strates"][st]
            self.assertEqual((e["valeur"], e["cas"]), (NN, "z_sous_seuil"), st)
            self.assertTrue(proche(str(e["emd"]), emd2, True), st)
            self.assertTrue(proche(str(e["emd_fraction"]), emd2 / 40000, True), st)
        self.assertEqual((g["r1_discrimine"], g["m"]), ("FAUX", 2))

    def test_j3_k_egal_n_et_garde(self):
        """ℓ = 1 : calme K = n = 54, z² = 189/10, σ̂²_bloc = 0 (seul motif, garde de blocs tenue à ℓ = 1) :
        rejet non qualifiable ; stress P̂_more = 0 : garde §5.4 ; NON ÉVALUABLE, m = 0. Rougit si : z_bloc
        ignoré ; garde §5.4 ignorée."""
        out, g = regle(*self.j3, 1)
        c = out["strates"]["calme"]
        self.assertTrue(proche(str(c["z"]), F(189, 10), True) and c["K"] == c["n"] == 54)
        self.assertEqual(c["bloc"]["z_bloc_motif"], "σ̂²_bloc = 0 (K ∈ {0, n})")
        self.assertEqual([e["cas"] for e in g["strates"].values()], ["rejet_non_qualifiable", "garde_5_4"])
        self.assertEqual((g["r1_discrimine"], g["m"]), (S1, 0))


class TestRegleRendu(unittest.TestCase):
    """Chaînes du fichier scellé §3.1 et §3.2 au bloc 3 : J1 (ℓ = 1 et 240), J2 (240), J3 (ℓ = 1)."""

    @classmethod
    def setUpClass(cls):
        j1, j2 = journal(200, 200, deux(25, 29)), journal(200, 200, deux(50, 37))
        j3 = journal(54, 10, rotation)
        cls.r = {"J1-1": rendu(*j1, 1), "J1": rendu(*j1), "J2": rendu(*j2), "J3-1": rendu(*j3, 1)}

    def val(self, ligne: str, motif: str, z2: F, signe: int = 1):
        """Ligne entière au motif ; groupe 1 : valeur imprimée, de carré z2 (10⁻⁴⁷ près), de signe donné."""
        m = re.fullmatch(motif, ligne)
        self.assertTrue(m and proche(m.group(1), z2, True) and (D(m.group(1)) > 0) == (signe > 0), ligne)
        return m

    def test_rendu_valeurs_enonces_emd(self):
        """Rougit si : EMD omis ; « R1 discrimine » sans strate nommée ; discordance imprimée « n'est pas
        rejeté » ; étiquette « hors famille, sans conclusion » retirée ; section hors place ; motif tu."""
        p, l1, _f = self.r["J1-1"]
        self.val(p["calme"][0], r"z_s = \S+ ≥ 2,33 ; z_bloc = (\S+) ≥ 2,33 → REJETTE", F(50, 7))
        self.assertEqual(p["calme"][1], "« le modèle d'indépendance du pool (k nominal_s = 3 flux du pool "
                         "de la strate, bloc 1 ; k_eff mesuré = non évaluable, bloc 6) est rejeté dans la "
                         f"strate calme sur 200 fenêtres, {AX}, tel qu'observé par cet instrument (hôte, DNS "
                         "et réseau du harnais compris) ; aucune dépendance de paire n'est établie »")
        self.val(p["stress"][0], r"z_s = (\S+) ≥ 2,33 ; z_bloc = \S+ < 2,33 → NE REJETTE PAS \(discordance\)",
                 F(2312, 375))
        self.assertEqual(p["stress"][1], "« le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, "
                         "est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et "
                         "dépendance sérielle des fenêtres »")
        self.val(p["stress"][2], EMD, F(236324725119, 1250000000))
        self.assertEqual(l1, R1D + "VRAI : strate(s) qui rejettent : calme")
        p, l1, _f = self.r["J2"]
        self.val(p["calme"][0], r"z_s = (\S+) < 2,33 \(z_s ≤ −2,33 : hors famille, sans conclusion\) → NE "
                 r"REJETTE PAS", F(40, 3), -1)
        self.val(p["stress"][0], r"z_s = (\S+) < 2,33 → NE REJETTE PAS", F(8, 375))
        for st, emd2 in (("calme", F(188607123, 1600000)), ("stress", F(43269638424597, 10 ** 11))):
            self.assertEqual(p[st][1], NRJ, st)
            self.assertTrue(proche(self.val(p[st][2], EMD, emd2).group(2), emd2 / 40000, True), st)
        self.assertEqual(l1, R1D + "FAUX : aucune strate ne rejette ; strate(s) testée(s) : calme, stress")
        p, l1, _f = self.r["J1"]
        self.val(p["calme"][0], r"z_s = (\S+) ≥ 2,33 ; z_bloc non publié \(garde de blocs : n_s = 200 < "
                 r"30·ℓ = 7200\)" + NQ, F(40, 3))
        self.assertEqual(l1, R1D + "NON ÉVALUABLE : aucune strate ne rejette ; rejet non qualifiable : "
                         "calme, stress")
        p, l1, _f = self.r["J3-1"]
        self.val(p["calme"][0], r"z_s = (\S+) ≥ 2,33 ; z_bloc non publié \(σ̂²_bloc = 0 \(K ∈ \{0, n\}\)\)"
                 + NQ, F(189, 10))
        self.assertEqual(p["stress"], ["z_s non publié (garde §5.4 : n·P̂_more·(1 − P̂_more) < 10) → NON "
                                       "ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2)"])
        self.assertEqual(l1, R1D + "NON ÉVALUABLE : aucune strate ne rejette ; rejet non qualifiable : calme")

    def test_famille_m_dynamique_premisse(self):
        """SHOGEN-POOLEE-FAMILLE-1, test nommé (D-8) : m = nombre de strates testées, « m ≤ 2 », borne 0,02 et
        prémisse du pt 7 sur une ligne, en place. Rougit si : m statique ; prémisse retirée ; strates tues."""
        for k, m, t in (("J1-1", 2, "calme, stress"), ("J2", 2, "calme, stress"), ("J1", 0, "aucune")):
            self.assertEqual(self.r[k][2], [FAMILLE.format(m, t)], k)

    def test_borne_exacte_et_voisine(self):
        """C-G2-2 (revue G2) : étiquette « z_s ≤ −2,33 » à la borne exacte z_s = −2,33, absente à
        z_s = −2,33 + 10⁻⁵⁰ (z_s de la strate calme de J2 forcé par mock de report.compute_r1). Rougit si :
        « < » au lieu de « ≤ » (MG01) ; étiquette sur tout z_s < 0 (MG02)."""
        c, j = journal(200, 200, deux(50, 37))
        orig = report.compute_r1
        with localcontext() as ctx:
            ctx.prec = 60
            voisine = D("-2.33") + D("1e-50")
        for z, att in ((D("-2.33"), True), (voisine, False)):
            def fake(*a, **k):
                out = orig(*a, **k)
                out["strates"]["calme"]["z"] = z
                return out
            with mock.patch.object(report, "compute_r1", fake):
                b3 = bloc3(report.render_report(c, j))
            ligne = [x for x in b3.split("\n") if x.startswith("    « calme » : z_s = ")][0]
            self.assertEqual(LAB in ligne, att, ligne)

    def test_z_negatif_au_dessus_de_la_borne(self):
        """C-G2-2 (revue G2) : −2,33 < z_s < 0 sans étiquette (deux(50, 40), stress : K = 10, z_s ≈ −0,73) ;
        calme (K = 0, z_s ≈ −3,65) étiqueté. Rougit si : étiquette sur tout z_s < 0 (MG02)."""
        par = rendu(*journal(200, 200, deux(50, 40)))[0]          # stress : K = 10, z_s ≈ −0,73
        self.assertRegex(par["stress"][0], r"^z_s = -0\.7\d+ < 2,33 → NE REJETTE PAS$")
        self.assertIn(LAB, par["calme"][0])                        # calme : K = 0, z_s ≈ −3,65


def asn(c: str, partage: bool = False) -> None:
    """Relevés ASN (r2.collect_asn) : un AS par hôte (k_eff = 3 = k nominal), ou coinbase et kraken sur un
    même AS (k_eff = 2) ; contrôlés sur la base au journal G1 (keff-base.out)."""
    n = count(64512)

    def resolve(host, resolvers):
        a = 64000 if partage and ("coinbase" in host or "kraken" in host) else next(n)
        return {"status": "ok", "resolver": resolvers[0], "ip": "192.0.2.1", "ip_secondary": [],
                "cname_chain": [], "prefix": "192.0.2.0/24", "asn_ripestat": a, "asn_cymru": a,
                "holder": "TEST"}
    r2.collect_asn([BY_ID[f] for f in FL], c, resolve_fn=resolve, now_fn=lambda: float(SAM))


def asn_discordant(c: str) -> None:
    """Relevés ASN : un AS par hôte ; l'hôte de kraken discordant (RIPEstat ≠ Cymru), donc non attribué :
    k_eff ≤ 3 (borne supérieure)."""
    n = count(64512)

    def resolve(host, resolvers):
        a = next(n)
        return {"status": "ok", "resolver": resolvers[0], "ip": "192.0.2.1", "ip_secondary": [],
                "cname_chain": [], "prefix": "192.0.2.0/24", "asn_ripestat": a,
                "asn_cymru": a + 1000 if "kraken" in host else a, "holder": "TEST"}
    r2.collect_asn([BY_ID[f] for f in FL], c, resolve_fn=resolve, now_fn=lambda: float(SAM))


def mort_en_calme(f: str, st: bool, j: int) -> bool:
    """J1 en calme et bitstamp sans lecture ok en calme (D1 cas b : retiré du pool de la strate calme)."""
    return (not st and f == "bitstamp") or deux(25, 29)(f, st, j)


ENT = (r"état = (\w+)\n.*\n      entrées \(ADR-0028 §1 bis\.1 pt 10\) : « R1 discrimine » = ([A-ZÉ ]+) "
       r"\(bloc 3.*?\) ; k_eff = (\S+) ; k nominal du segment \(hôtes\) = (\d+) ;")


def composer(t: unittest.TestCase, txt: str) -> str:
    """Composition exécutée sur l'artefact rendu (C-5) : valeurs par strate lues au bloc 3 → « R1 discrimine »
    (pt 6), comparé à la ligne imprimée → état attendu du drapeau 2 (pt 10, précédence D-4), comparé à l'état
    et à la ligne d'entrées du bloc 6. Rend l'état imprimé."""
    b3, b6 = txt.split("[BLOC 3]")[1].split("[BLOC 4]")[0], txt.split("[BLOC 6]")[1]
    v = dict(re.findall(r"\n    « (\w+) » : z_s .*→ (REJETTE|NE REJETTE PAS|NON ÉVALUABLE)", b3))
    nq = [s for s in v if re.search(rf"\n    « {s} » : z_s .*rejet non qualifiable", b3)]
    rej, tst = [s for s in v if v[s] == "REJETTE"], [s for s in v if v[s] != S1]
    d = "VRAI" if rej else "FAUX" if tst and not nq else S1
    t.assertIn(R1D + d + " : ", b3)
    etat, d6, ke, kn = re.search(ENT, b6).groups()
    t.assertEqual((d6, etat), (d, "NON_EVALUABLE" if ke == "-" or d == S1 else
                               "LEVE" if d == "VRAI" and ke == kn else "ETEINT"))
    return etat


class TestDrapeau2Regle(unittest.TestCase):
    """Drapeau 2 aligné sur la règle (fichier scellé §2.3 et §3.3) : J1 et J2 avec ASN distincts, partagés
    ou absents."""
    V = "« R1 discrimine » VRAI (strate(s) : calme) "
    RAISON = {"leve": V + "AVEC k_eff = 3 = k nominal du segment : les axes R2 ne capturent pas le mode "
              "commun (§5.6 / 04 §3) — signal sur A(axis-coverage), jamais la règle",
              "eteint-VRAI": V + "mais k_eff = 2 < k nominal du segment = 3 : recouvrement R2 mesuré "
              "explique au moins en partie la co-défaillance",
              "non_evaluable-NON ÉVALUABLE": "« R1 discrimine » NON ÉVALUABLE (règle SHOGEN-CRITERE-R1-1, "
              "bloc 3) — co-défaillance non qualifiable ; ni levé ni éteint",
              "eteint-FAUX": "« R1 discrimine » FAUX : le modèle d'indépendance n'est rejeté dans aucune "
              "strate testée (bloc 3)",
              "non_evaluable-FAUX": "k_eff non évaluable (axe ASN non mesuré/incomplet) — le drapeau exige "
              "une partition évaluable (§5.6)"}

    @classmethod
    def setUpClass(cls):
        cls.j = {}
        for nom, f, a in (("J1d", deux(25, 29), False), ("J1p", deux(25, 29), True),
                          ("J2d", deux(50, 37), False), ("J2n", deux(50, 37), None)):
            cls.j[nom] = journal(200, 200, f)
            if a is not None:
                asn(cls.j[nom][0], a)

    def test_drapeau2_aligne_sur_la_regle(self):
        """Rougit si : drapeau 2 lu sur le max des z (v0 : J1 à ℓ = 240 LEVÉ) ; LEVÉ sans k_eff = k nominal
        (J1 partagé) ; FAUX éteint avant le contrôle de k_eff (J2 sans ASN) ; z_max rendu ; k nominal_s
        absent."""
        for nom, n, etat, d, ke in (("J1d", 1, "leve", "VRAI", 3), ("J1p", 1, "eteint", "VRAI", 2),
                                    ("J1d", 240, "non_evaluable", S1, 3), ("J2d", 240, "eteint", "FAUX", 3),
                                    ("J2n", 240, "non_evaluable", "FAUX", None)):
            with ell(n):
                g = r2.recompute_r2_from_journal(*self.j[nom])["drapeau_2"]
            self.assertEqual((g["etat"], g["r1_discrimine"], g["k_eff"], g["k_nominal"]), (etat, d, ke, 3))
            cle = etat if etat == "leve" else f"{etat}-{d}"
            self.assertEqual((g["raison"], g["k_nominal_strates"]),
                             (self.RAISON[cle], {"calme": 3, "stress": 3}), nom)
            self.assertEqual(("z_max" in g, g.get("localisation_inter_clusters") is not None),
                             (False, d == "VRAI" and ke is not None), nom)

    def test_bloc6_entrees_k_nominal_heterogene(self):
        """Ligne d'entrées (§3.3) : J1 à ℓ = 1 (VRAI nommé), J2 avec ASN (FAUX), fixture_b de B0 (D1 cas b,
        k nominal_s = 2 ≠ 3 en stress : comparaison hétérogène déclarée). Rougit si : k nominal_s ou la
        déclaration retirés ; strates qui rejettent tues."""
        e = "\n      entrées (ADR-0028 §1 bis.1 pt 10) : « R1 discrimine » = "
        k3 = " ; k nominal du segment (hôtes) = 3 ; k nominal_s (flux du pool de la strate) : « calme » = 3, "
        fin = " ; strate poolée hors des entrées\n"
        with couture(1):
            t1 = report.render_report(*self.j["J1d"])
        t2 = report.render_report(*self.j["J2d"])
        tb = report.render_report(*fixture_b(tempfile.mkdtemp(prefix="s2crit_")))
        self.assertIn(e + "VRAI (bloc 3 ; strate(s) : calme) ; k_eff = 3" + k3 + "« stress » = 3" + fin, t1)
        self.assertIn(e + "FAUX (bloc 3) ; k_eff = 3" + k3 + "« stress » = 3" + fin, t2)
        self.assertIn(e + "NON ÉVALUABLE (bloc 3) ; k_eff = -" + k3 + "« stress » = 2 — comparaison "
                      "hétérogène déclarée" + fin, tb)

    def test_drapeau_run_max(self):
        """J1 sous la couture ℓ = 25 : run maximal 25 ≥ ℓ en calme (drapeau), 21 < ℓ en stress (aucun) ; à
        ℓ = 240, aucun drapeau. Rougit si : drapeau omis ; « > » à la place de « ≥ » ; autre strate."""
        dr = ("drapeau « run maximal ≥ ℓ » (run maximal = 25 ≥ ℓ = 25) : σ̂²_bloc,s biaisé vers le bas ; "
              "SHOGEN-DEP-FENETRES-2 prioritaire avant G10 — hors décision, sans effet sur la valeur")
        for n, att in ((25, {"calme": [dr], "stress": []}), (240, {"calme": [], "stress": []})):
            par = rendu(*self.j["J1d"], n)[0]
            self.assertEqual({s: [x for x in p if x.startswith("drapeau")] for s, p in par.items()}, att, n)

    def test_composition_cli_petites_fixtures(self):
        """Chemin servi (CLI, processus neuf) à ℓ = 240 : NON ÉVALUABLE (J1), ÉTEINT (J2), NON ÉVALUABLE sans
        ASN (J2) ; composition bloc 3 → bloc 6 sur la sortie. Rougit si : bloc 6 sur une autre règle."""
        for nom, att in (("J1d", "NON_EVALUABLE"), ("J2d", "ETEINT"), ("J2n", "NON_EVALUABLE")):
            txt = cli(os.path.dirname(self.j[nom][0])).decode("utf-8")
            self.assertEqual(composer(self, txt), att, nom)
            self.assertEqual(txt, report.render_report(*self.j[nom]) + "\n", nom)


class TestKeffBorneEtPoolStrate(unittest.TestCase):
    """Corrections C-G2-3 à C-G2-5 de la revue G2 (2026-10-01), J1 sous la couture ℓ = 1 : énoncé REJETTE du
    bloc 3 quand k_eff est une borne supérieure (hôte de kraken discordant) ou sous D1 cas b ; drapeau 2 quand
    la borne supérieure égale k nominal (Q-G2-1, option a de la démonstration du réviseur)."""

    def test_enonce_rejette_keff_borne(self):
        """C-G2-3 : énoncé REJETTE quand k_eff est une borne supérieure (hôte non attribué). Rougit si : la
        branche « ≤ … (borne supérieure) » est retirée (MG03)."""
        c, j = journal(200, 200, deux(25, 29))
        asn_discordant(c)
        with couture(1):
            txt = report.render_report(c, j)
        self.assertIn("\n  k_eff     ≤ 3  (BORNE SUPÉRIEURE ; 1 hôte(s) non attribué(s)", txt)
        self.assertIn("k_eff mesuré ≤ 3 (borne supérieure), bloc 6) est rejeté dans la strate calme",
                      bloc3(txt))

    def test_k_nominal_s_cas_b(self):
        """C-G2-4 : énoncé REJETTE sous D1 cas b, k nominal_s = flux du pool de la strate (2), pas celui du
        segment (3). Rougit si : k nominal_s lu sur le pool d'analyse du segment (MG04)."""
        c, j = journal(200, 200, mort_en_calme)
        asn(c)
        with couture(1):
            txt = report.render_report(c, j)
        self.assertIn("(k nominal_s = 2 flux du pool de la strate, bloc 1 ; k_eff mesuré = 3, bloc 6) est "
                      "rejeté dans la strate calme sur 200 fenêtres", bloc3(txt))
        self.assertIn("k nominal_s (flux du pool de la strate) : « calme » = 2, « stress » = 3 — comparaison "
                      "hétérogène déclarée", txt)

    def test_drapeau2_keff_borne(self):
        """C-G2-5 et Q-G2-1 (option a) : k_eff borne supérieure égale à k nominal. Rougit si : LEVÉ sur une
        égalité non établie (MG05R) ; « k_eff = 3 » imprimé au drapeau 2 quand le bloc 6 imprime « k_eff ≤ 3
        (BORNE SUPÉRIEURE) » (MG10R)."""
        c, j = journal(200, 200, deux(25, 29))
        asn_discordant(c)
        with couture(1):
            g = r2.recompute_r2_from_journal(c, j)["drapeau_2"]
            b6 = report.render_report(c, j).split("[BLOC 6]")[1]
        self.assertEqual((g["etat"], g["r1_discrimine"], g["k_eff"]), ("non_evaluable", "VRAI", 3))
        self.assertIn(" ; k_eff ≤ 3 (borne supérieure) ; k nominal du segment (hôtes) = 3 ;", b6)
        self.assertNotIn("k_eff = 3", b6.split("DRAPEAU 2")[1])


class TestRegleLong(unittest.TestCase):
    """Chemin de production ℓ = 240 sur la fixture B de B-DEP-2b (7 200 fenêtres calme, 60 stress) avec ASN
    distincts (C-9) ; composition bloc 3 → bloc 6 sur l'artefact, API et CLI en processus neuf (C-5)."""

    @classmethod
    def setUpClass(cls):
        cls.c, j = journal(7200, 60, trb.TestRenduBlocsLong.panne)
        asn(cls.c)
        cls.txt = report.render_report(cls.c, j)

    def test_production_l240_rejette_calme(self):
        """J4 (§2.2) : calme z² = 321723783226467079200/170332635149538239, z_bloc² =
        44683858781453761/253969241100300 : REJETTE ; stress sous la garde §5.4 ; VRAI [calme], m = 1.
        Rougit si : garde de blocs mal lue au chemin de production ; m statique ; énoncé sans k_eff."""
        b3 = self.txt.split("[BLOC 3]")[1].split("[BLOC 4]")[0]
        m = re.search(r"\n    « calme » : z_s = (\S+) ≥ 2,33 ; z_bloc = (\S+) ≥ 2,33 → REJETTE\n", b3)
        self.assertTrue(m and proche(m.group(1), F(321723783226467079200, 170332635149538239), True, E45)
                        and proche(m.group(2), F(44683858781453761, 253969241100300), True, E45))
        self.assertIn("k_eff mesuré = 3, bloc 6) est rejeté dans la strate calme sur 7200 fenêtres", b3)
        self.assertIn("\n    « stress » : z_s non publié (garde §5.4 : n·P̂_more·(1 − P̂_more) < 10) → NON "
                      "ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2)\n", b3)
        self.assertIn("\n" + FAMILLE.format(1, "calme") + "\n", b3)

    def test_composition_bloc3_bloc6_api_cli(self):
        """Rougit si : bloc 6 incohérent avec le bloc 3 (drapeau 2 sur le max des z, autre règle) ; chemin
        servi différent de l'API."""
        self.assertEqual(composer(self, self.txt), "LEVE")
        self.assertEqual(cli(os.path.dirname(self.c)), (self.txt + "\n").encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
