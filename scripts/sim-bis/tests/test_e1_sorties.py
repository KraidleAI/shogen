"""E1 câblée, lots et sorties (SB-11o ; E-S-05, E-S-38, E-S-45, E-S-48) : attendus recalculés ici depuis des appels
indépendants de replication_e1, ou écrits à la main ; chaque test nomme les mutations qui le rougissent."""
import functools
import hashlib
import json
import os
import shutil
import tempfile
import unittest
import unittest.mock
from fractions import Fraction

import calib_fiv
import calibration
import commun
import e1
import executer

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
E1R = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5], tau_D=[60], replications=2,
                        cellule="E1-essai"))


@functools.lru_cache(maxsize=None)
def cal_e1():
    return calib_fiv.calendrier_e1(PRM, environ={})


def dossier(test):
    d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
    test.addCleanup(shutil.rmtree, d)
    return d


class TestCalculerE1(unittest.TestCase):
    def test_lots_par_point_et_reprise(self):
        """C0 et les deux points de la grille réduite, deux réplications, plan d'une réplication par lot (coût 10,
        borne 10) : six lots « <cellule>.<a>-<b>.lot », moyennes de chaque point égales à moyennes_point des
        enregistrements de replication_e1 recalculés ici et passés en JSON ; lot (1/10, 5, 60) [1, 2) perdu, E1
        relancée : ce seul lot refait, de mêmes octets (sha256 égal), moyennes inchangées ; lots présents relus, jamais
        récrits. Mutations M-11O-01 (C0 omis), M-11O-02 (lot présent refait : SORTIE/existe), M-11O-03 (moyennes du
        point précédent), M-11O-04 (plan sur la borne par défaut), M-11O-05 (réplications lues à R − 1)."""
        d, cal = dossier(self), cal_e1()
        moy, journal = e1.calculer_e1(E1R, EP, cal, d, 1, 10, ["e"], 10)
        noms = [os.path.basename(c) for c, _h in journal]
        self.assertEqual(noms, [f"E1-essai-{x}.00000{a}-00000{a + 1}.lot" for x in ("C0-v2", "1_100-5-60", "1_10-5-60")
                                for a in (0, 1)])
        for p in [None] + calib_fiv.grille(E1R):
            recs = [executer.jsonable(e1.replication_e1(E1R, EP, cal, p, i)) for i in (0, 1)]
            self.assertEqual(moy[p], e1.moyennes_point(json.loads(json.dumps(recs)), E1R["calibration"]), p)
        perdu = os.path.join(d, noms[5])
        os.unlink(perdu)
        moy2, journal2 = e1.calculer_e1(E1R, EP, cal, d, 1, 10, ["e"], 10)
        self.assertEqual(journal2, [journal[5]])
        self.assertEqual(moy2, moy)


class TestEcrireE1(unittest.TestCase):
    def test_e_s_48(self):
        """E-S-48 et E-S-05 : calibration_e1.json (JSON canonique) et calibration_e1.txt (lignes, première ligne
        l'étiquette) écrits si tous les oracles passent, sha256 des octets écrits rendus ; aucun oracle, un oracle en
        échec : SORTIE/oracle ; étiquette absente en tête du texte ou de l'entête : SORTIE/etiquette ; un des deux
        fichiers présent : SORTIE/existe, l'autre jamais écrit (à la main). Mutations M-11O-06 (oracles non lus),
        M-11O-07 (liste vide admise), M-11O-08 (étiquette non contrôlée), M-11O-09 (texte écrit avant le contrôle de
        présence du JSON), M-11O-10 (JSON non canonique), M-11O-11 (sha256 du JSON rendu pour le texte)."""
        et, ok = commun.ETIQUETTE, {"suite sim-bis conforme": True, "E-S-39 r1": True}
        obj, lignes = {"entete": [et, "sha256 a b"], "x": [Fraction(1, 3)]}, [et, "sha256 a b", "ligne"]
        for oracles in ({}, dict(ok, **{"E-S-39 r1": False})):
            d = dossier(self)
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, obj, lignes, oracles)
            self.assertEqual((c.exception.code, os.listdir(d)), ("SORTIE/oracle", []))
        for o, li in ((obj, ["autre"] + lignes[1:]), (dict(obj, entete=["autre"]), lignes)):
            d = dossier(self)
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, o, li, ok)
            self.assertEqual((c.exception.code, os.listdir(d)), ("SORTIE/etiquette", []))
        d = dossier(self)
        r = e1.ecrire_e1(d, obj, lignes, ok)
        j, t = (os.path.join(d, "calibration_e1." + x) for x in ("json", "txt"))
        with open(j, "rb") as f, open(t, "rb") as g:
            bj, bt = f.read(), g.read()
        self.assertEqual(bj, ('{"entete":["' + et + '","sha256 a b"],"x":["1/3"]}' + commun.NL).encode("utf-8"))
        self.assertEqual(bt, (commun.NL.join(lignes) + commun.NL).encode("utf-8"))
        self.assertEqual(r, [(j, hashlib.sha256(bj).hexdigest()), (t, hashlib.sha256(bt).hexdigest())])
        for x in ("json", "txt"):
            d = dossier(self)
            with open(os.path.join(d, "calibration_e1." + x), "w", encoding="utf-8") as f:
                f.write("déjà")
            with self.assertRaises(commun.Refus) as c:
                e1.ecrire_e1(d, obj, lignes, ok)
            self.assertEqual((c.exception.code, sorted(os.listdir(d))), ("SORTIE/existe", ["calibration_e1." + x]))



P = (Fraction(1, 10), Fraction(5), 60)
P0 = (Fraction(1, 100), Fraction(5), 60)
VRAIE = calib_fiv.selection


def forcee(*a):
    """calib_fiv.selection enveloppée : C1 = P0 et C2 = P en calme, l'inverse en stress (C1 ≠ C2)."""
    x = VRAIE(*a)
    x["calme"].update(C1=P0, C2=P)
    x["stress"].update(C1=P, C2=P0)
    return x


def pt(p):
    return f"(φ = {p[0]}, κ = {p[1]}, τ_D = {p[2]})"


class TestRenduE1(unittest.TestCase):
    def test_sections_et_lancer(self):
        """E1 de la grille réduite lancée entière (lancer_e1 : lots, moyennes, calibrer, pauses de C1, rendu, écriture),
        sélection enveloppée (C1 ≠ C2) : texte écrit = entête (étiquette en tête), ligne de schéma (à la main), par
        strate [E1] (C2, C1), [RÉSIDUS C2] aux ℓ gardés d'EP, ligne [BORD E1], une ligne par hôte (résidus à C1, point
        de Q₁ de l'hôte seul, réplications indéfinies par point), [ÉCART-TYPE I_t] par point et par strate,
        [FAISABILITÉ] à C1 et à C2, phrases du bord, puis la section des pauses de C1 ; chaque section recomposée ici
        depuis calibrer et pauses_c1 appelés à part sur les lots relus ; entête des lots = entête des sorties ; JSON :
        mêmes entête, phrases, points sous leurs noms de cellule. Mutations M-11P-01 (pauses rejouées à C2),
        M-11P-02 (entête prise avant fiv_unites.txt : E1/entete), M-11P-03 (résidus de C2 sous des ℓ non gardés),
        M-11P-04 (écart-type d'un autre point), M-11P-05 (faisabilité de C2 sous l'étiquette C1), M-11P-06 (phrases
        omises), M-11P-07 (hôtes d'une autre strate), M-11P-09 (moyennes de C0 sous chaque nom), M-11P-11 (nombre
        de points de la ligne de schéma), M-11P-13 (entête d'une autre lecture dans les sorties)."""
        lots, sorties, cal = dossier(self), dossier(self), cal_e1()
        lus = {}
        ok = {"suite sim-bis conforme": True}
        with unittest.mock.patch.object(calib_fiv, "selection", side_effect=forcee):
            r, journal = e1.lancer_e1(E1R, lots, sorties, 1, 1, ok, lus, {})
            self.assertEqual(len(journal), 3)
            moy = {p: e1.moyennes_point(executer.lire_lots(lots, calib_fiv.cellule(E1R, p), 2, commun.entete(lus)),
                                        E1R["calibration"]) for p in [None] + calib_fiv.grille(E1R)}
            res = e1.calibrer(E1R, cal, moy, None, {})
        with open(r[1][0], encoding="utf-8") as f:
            lignes = f.read().split(commun.NL)
        with open(r[0][0], encoding="utf-8") as f:
            obj = json.load(f)
        ent = commun.entete(lus)
        self.assertEqual((lignes[:len(ent)], obj["entete"], lignes[0]), (ent, ent, commun.ETIQUETTE))
        k = len(ent)
        self.assertEqual(lignes[k], "schéma shogen.sim-bis.v1 ; sortie calibration_e1 (E1, E-S-38 ; ajout daté du "
                                    "G0 du 2026-10-05 15:05:43 UTC) ; 2 réplications par point ; C0 et 2 points de "
                                    "la grille")
        ep = calibration.charger(PRM, environ={})
        att = []
        for s, c1 in (("calme", P0), ("stress", P)):
            x = res["strates"][s]
            self.assertEqual(x["C1"], c1)
            ells = [c["ell"] for c in ep["fiv"]["D1-bis", s] if c["garde"]]
            self.assertEqual(obj["strates"][s]["ell_residus"], ells)
            att += [f"[E1] « {s} » : C2 = {pt(x['C2'])} ; C1 = {pt(c1)}",
                    f"[RÉSIDUS C2] « {s} » : ln F_C2(ℓ) − ln F_EP(ℓ) aux ℓ gardés d'EP : "
                    + " ; ".join(f"ℓ = {e} : {v}" for e, v in zip(ells, x["residus"])), x["ligne_bord"]]
            for h, _f in E1R["calibration"]["unites"]:
                u = x["unites"][h]
                att.append(f"  « {s} » hôte {h} : résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) : "
                           + (" ; ".join(f"ℓ = {e} : {'-' if v is None else v}" for e, v in u["residus_C1"])
                              or "aucun ℓ retenu") + " ; point de Q₁ minimal pour cet hôte seul (diagnostic, jamais "
                           "candidat) : " + (pt(u["point_Q1"]) if u["point_Q1"] else "aucun") + " ; réplications à "
                           "FIV indéfini : " + ", ".join(f"{c} {n}" for c, n in u["indefinies"].items()))
        for p in [None] + calib_fiv.grille(E1R):
            for s in ("calme", "stress"):
                m = moy[p][s]
                att.append(f"[ÉCART-TYPE I_t] {calib_fiv.cellule(E1R, p)} « {s} » : {m['I']['definies']} réplications "
                           f"définies, {m['I']['indefinies']} indéfinies ; " + " ; ".join(
                               f"ℓ = {e} : {'-' if v is None else v}" for e, v in zip(E1R["calibration"]["ell"],
                                                                                     m["ecart_type"])))
        for n in ("C1", "C2"):
            for s in ("calme", "stress"):
                f = res["faisabilite"][n][s]
                att.append(f"[FAISABILITÉ {n}] « {s} » : r′ maximal = {f['max']} ({f['ou'][0]}, {f['ou'][1]}) : "
                           + ("faisable, r′ < 1" if f["faisable"] else "INFAISABLE, r′ ≥ 1 (REGIME-FAISABILITE-1)"))
        texte = commun.lire_entree(PRM, "intervalles", environ={}, sommes="sommes_plan2").decode("utf-8")
        att += res["phrases"] + e1.lignes_pauses(E1R, e1.pauses_c1(E1R, EP, cal, {"calme": P0, "stress": P}, 1),
                                                 {"calme": P0, "stress": P}, 2, texte) + [""]
        self.assertEqual(lignes[k + 1:], att)
        self.assertEqual((obj["phrases"], sorted(obj["points"])), (res["phrases"], sorted(
            calib_fiv.cellule(E1R, p) for p in [None] + calib_fiv.grille(E1R))))
        for p in [None] + calib_fiv.grille(E1R):
            self.assertEqual(obj["points"][calib_fiv.cellule(E1R, p)],
                             json.loads(json.dumps(executer.jsonable(moy[p]))))
        with open(journal[0][0], "rb") as f:
            self.assertEqual(json.loads(f.read().split(commun.NL.encode(), 1)[1])["entete"], ent)

    def test_entete_changee(self):
        """Entrée lue en cours d'E1 (calibrer enveloppé : `lus` gagne une ligne) : E1/entete, aucune sortie écrite.
        Mutation M-11P-08 (contrôle de l'entête retiré)."""
        lots, sorties, vraie = dossier(self), dossier(self), e1.calibrer

        def calibrer(*a):
            a[3]["docs/autre.txt"] = "0" * 64
            return vraie(*a)
        with unittest.mock.patch.object(e1, "calibrer", side_effect=calibrer):
            with self.assertRaises(commun.Refus) as c:
                e1.lancer_e1(E1R, lots, sorties, 1, 1, {"suite sim-bis conforme": True}, {}, {})
        self.assertEqual((c.exception.code, os.listdir(sorties)), ("E1/entete", []))

if __name__ == "__main__":
    unittest.main()
