"""RB-2 : fusion des journaux des quatre observateurs (E-R-03, E-R-04 ; Q-R-03 ; témoin et remplaçants). Journaux
synthétiques seulement, écrits par l'écrivain de collecte/journal.py ; `run_params` par le câblage de collecte/entree.py
(`configurer`, `configurer_secondaire`, `_liste`, `_run_params`) sur les configurations de production et des
descripteurs d'essai ; aucun journal de campagne. Attendus écrits ici (listes, codes nommés, sha256 par hashlib sur les
octets des fichiers), indépendants du code de la fusion."""
import hashlib
import json
import os
import shutil
import tempfile
import unittest

from shogen_s2bis.collecte import entree, journal
from shogen_s2bis.collecte.lecture import S
from shogen_s2bis.recalc import fusion

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RACINE, "config")
COMMIT = "c" * 40
WS = 1791158220                         # 2026-10-04 23:57 UTC (`date -u -d @1791158220`)
OBS = ("o1", "o2", "o3", "o4")          # liste fermée d'observateurs.json (GEL-7)
SANTE = {"d2": {"retard_max": 0, "non_parties": 0}}           # `sante` d'essai, sans sondes


def sha(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Paquet(unittest.TestCase):                            # quatre fichiers lus en octets ; liste fermée
    def test_quatre_fichiers_lus_en_octets(self):
        lus = fusion.paquet(CONFIG)
        self.assertEqual(({n: lus[n][1] for n in lus}, lus["observateurs"][0]), (
            {n: sha(os.path.join(CONFIG, n + ".json")) for n in ("formes", "sante", "observateurs", "carte")},
            {"observateurs": list(OBS)}))
        with tempfile.TemporaryDirectory() as d:
            for n in ("formes", "sante", "observateurs", "carte"):
                shutil.copy(os.path.join(CONFIG, n + ".json"), d)
            for octets in (b"{", b'{"formes": "' + bytes([255]) + b'"}'):     # JSON coupé ; chaîne hors UTF-8
                with open(os.path.join(d, "carte.json"), "wb") as f:
                    f.write(octets)
                with self.assertRaises(fusion.RefusFusion) as e:
                    fusion.paquet(d)
                self.assertEqual(e.exception.code, "FUSION/config")

    def test_liste_fermee(self):
        """Observateurs lus autres que la liste fermée (o1 à o4) : refus, avant toute lecture (dossiers absents)."""
        with tempfile.TemporaryDirectory() as base:
            d = {o: os.path.join(base, o) for o in OBS}
            cinq = os.path.join(base, "o5")
            for lus in ({o: d[o] for o in OBS[:3]}, {**d, "o5": cinq}, {**{o: d[o] for o in OBS[:3]}, "o5": cinq},
                        {**d, "O1": d["o1"]}, {}):
                with self.subTest(lus=sorted(lus)):
                    with self.assertRaises(fusion.RefusFusion) as e:
                        fusion.Fusion(lus, CONFIG, COMMIT)
                    self.assertEqual(e.exception.code, "FUSION/observateurs")


class Observateurs:
    """Dossier d'essai : par observateur, un descripteur et un dossier de journaux `pool` et `secondaire`."""

    def __init__(self, base, config=CONFIG):
        self.base, self.config = base, config

    def descripteur(self, o, nom=None):
        chemin = os.path.join(self.base, o + ".descripteur.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump({"observateur": nom or o, "fournisseur": "essai", "region": "essai", "asn": 64512, "resolveur":
                       "127.0.9.53", "config_resolveur": "resolv.conf", "versions": ["python3"], "empreinte": "e" * 64},
                      f)
        return chemin

    def run_params(self, o, j, nom=None):
        """Champs de `run_params` du câblage (FORMAT §14.4, §15.6), `--observateurs` pour le pool."""
        c = {n: os.path.join(self.config, n + ".json") for n in fusion.CONFIGS}
        d = self.descripteur(o, nom)
        if j == "pool":
            lus = entree.configurer({"formes": c["formes"], "sante": c["sante"], "descripteur": d}, COMMIT)
            lus["observateurs"] = entree._liste(c["observateurs"], nom or o, sha=True)
        else:
            lus = entree.configurer_secondaire({"formes": c["formes"], "carte": c["carte"], "descripteur": d}, COMMIT)
        return entree._run_params(lus, COMMIT)

    def ecrire(self, o, j, ws0, fenetres=(), rp=None, lire=None):
        """Un démarrage du journal `j` de `o`, ouvert à ws0 : `run_params` (`rp`, ou celui du câblage ; False : aucun),
        puis pour chaque fenêtre (ws, [(forme, décodeur)]) ses lectures (`lire(décodeur, ws)`), une `sante` et le
        marqueur."""
        dossier = os.path.join(self.base, o)
        os.makedirs(dossier, exist_ok=True)
        jl = journal.Journal(dossier, j, fsync=lambda fd: None)
        jl.ouvrir(ws0)
        try:
            if rp is not False:
                jl.ecrire("run_params", jl.suivante, **(rp or self.run_params(o, j)))
            for ws, formes in fenetres:
                for nom, dec in formes:
                    jl.ecrire("lecture", ws, forme=nom, prevu=ws * S, **lire(dec, ws).enregistrement())
                jl.ecrire("sante", ws, **SANTE)
                jl.marqueur(ws)
        finally:
            jl.fermer()
        return dossier

    def quatre(self, ws0=WS, rp=None, fenetres=None, lire=None):
        """Les huit journaux, un démarrage chacun, ouverts à ws0 (`rp`, `fenetres` : {(o, j) : run_params, fenêtres}
        imposés, lectures de `lire`) ; {observateur : dossier}."""
        return {o: [self.ecrire(o, j, ws0, (fenetres or {}).get((o, j), ()), (rp or {}).get((o, j)), lire)
                    for j in fusion.JOURNAUX][0] for o in OBS}


class Base(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base)
        self.obs = Observateurs(self.base)

    def refus(self, *a):
        with self.assertRaises((fusion.RefusFusion,)) as e:
            fusion.Fusion(*a)
        return e.exception.code


class RunParams(Base):                                      # E-R-04 ; liste fermée des observateurs
    def test_deux_demarrages_concordants_egaux_au_paquet(self):
        dossiers = self.obs.quatre()
        for o in OBS:
            for j in fusion.JOURNAUX:
                self.obs.ecrire(o, j, WS + 600)             # second démarrage : `reprise`, puis `run_params`
        f = fusion.Fusion(dict(reversed(dossiers.items())), CONFIG, COMMIT)
        d = {o: sha(os.path.join(self.base, o + ".descripteur.json")) for o in OBS}
        c = {n: sha(os.path.join(CONFIG, n + ".json")) for n in ("formes", "sante", "observateurs", "carte")}
        self.assertEqual((f.liste, sorted(f.run_params)), (list(OBS), [(o, j) for o in OBS for j in fusion.JOURNAUX]))
        for o in OBS:
            self.assertEqual((f.run_params[o, "pool"]["sha256"], f.run_params[o, "secondaire"]["sha256"]), (
                {"formes": c["formes"], "sante": c["sante"], "observateurs": c["observateurs"], "descripteur": d[o]},
                {"formes": c["formes"], "carte": c["carte"], "descripteur": d[o]}))
            self.assertEqual(f.run_params[o, "pool"]["descripteur"]["observateur"], o)

    def test_refus_nommes(self):
        """Chaque écart, au second démarrage de o2 (le premier est conforme), est un refus nommé."""
        def sha256(rp, **x):
            return {**rp, "sha256": {**rp["sha256"], **x}}
        for j, modifier, code in (
                ("pool", lambda rp: {**rp, "commit": "d" * 40}, "FUSION/commit"),
                ("secondaire", lambda rp: {**rp, "commit": "d" * 40}, "FUSION/commit"),
                ("pool", lambda rp: sha256(rp, formes="0" * 64), "FUSION/sha256"),
                ("pool", lambda rp: sha256(rp, sante="0" * 64), "FUSION/sha256"),
                ("pool", lambda rp: sha256(rp, observateurs="0" * 64), "FUSION/sha256"),
                ("secondaire", lambda rp: sha256(rp, carte="0" * 64), "FUSION/sha256"),
                ("secondaire", lambda rp: sha256(rp, formes="0" * 64), "FUSION/sha256"),
                ("pool", lambda rp: sha256(rp, carte="0" * 64), "FUSION/sha256"),            # clé en trop
                ("pool", lambda rp: {**rp, "sha256": "0" * 64}, "FUSION/sha256"),
                ("pool", lambda rp: {**rp, "sante": {**rp["sante"], "delai": 1}}, "FUSION/contenu"),
                ("pool", lambda rp: {**rp, "formes": {**rp["formes"], "places": 39}}, "FUSION/contenu"),
                ("pool", lambda rp: {**rp, "observateurs": {"observateurs": list(OBS[:3])}}, "FUSION/contenu"),
                ("secondaire", lambda rp: {**rp, "carte": {**rp["carte"], "places": 3}}, "FUSION/contenu"),
                ("secondaire", lambda rp: {**rp, "formes": {**rp["formes"], "w": 30}}, "FUSION/contenu"),
                ("pool", lambda rp: {k: v for k, v in rp.items() if k != "observateurs"}, "FUSION/run_params-cle"),
                ("secondaire", lambda rp: {k: v for k, v in rp.items() if k != "carte"}, "FUSION/run_params-cle"),
                ("pool", lambda rp: {k: v for k, v in rp.items() if k != "descripteur"}, "FUSION/run_params-cle"),
                ("pool", lambda rp: {**rp, "descripteur": {**rp["descripteur"], "observateur": "o3"}},
                 "FUSION/observateur"),
                ("pool", lambda rp: {**rp, "descripteur": {**rp["descripteur"], "versions": ["python3", "chrony"]}},
                 "FUSION/run_params-discordant"),
                ("secondaire", lambda rp: sha256(rp, descripteur="0" * 64), "FUSION/run_params-discordant")):
            with self.subTest(j=j, code=code):
                base = tempfile.mkdtemp(dir=self.base)
                obs = Observateurs(base)
                dossiers = obs.quatre()
                obs.ecrire("o2", j, WS + 600, rp=modifier(obs.run_params("o2", j)))
                with self.assertRaises(fusion.RefusFusion) as e:
                    fusion.Fusion(dossiers, CONFIG, COMMIT)
                self.assertEqual(e.exception.code, code)

    def test_python_non_porteuse_et_commit_du_paquet(self):  # Q-RB2-2 : la version de Python peut changer
        dossiers = self.obs.quatre()
        self.obs.ecrire("o4", "pool", WS + 600, rp={**self.obs.run_params("o4", "pool"), "python": "3.13.0"})
        self.assertEqual(fusion.Fusion(dossiers, CONFIG, COMMIT).liste, list(OBS))
        self.assertEqual(self.refus(dossiers, CONFIG, "d" * 40), "FUSION/commit")

    def test_descripteurs_differents_ou_run_params_absent(self):
        rp = self.obs.run_params("o3", "secondaire")
        rp = {**rp, "descripteur": {**rp["descripteur"], "region": "autre"}}
        self.assertEqual(self.refus(self.obs.quatre(rp={("o3", "secondaire"): rp}), CONFIG, COMMIT),
                         "FUSION/descripteur")
        obs = Observateurs(tempfile.mkdtemp(dir=self.base))
        self.assertEqual(self.refus(obs.quatre(rp={("o1", "pool"): False}), CONFIG, COMMIT), "FUSION/run_params-absent")
