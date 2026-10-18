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

from shogen_s2bis.collecte import decodeurs, entree, journal
from shogen_s2bis.collecte.lecture import S, Lecture
from shogen_s2bis.recalc import fusion

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RACINE, "config")
FIXTURES = os.path.join(RACINE, "tests", "fixtures")
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


def m(n):                               # fenêtre n minutes après WS ; m(3) = 2026-10-05 00:00 UTC
    return WS + 60 * n


def corps(dec):
    """Octets de la fixture du décodeur `dec` (fixtures/actifs, temoin, ou btc sans le suffixe `_btc`)."""
    for chemin in (f"actifs/{dec}.bin", f"temoin/{dec}.bin", f"btc/{dec[:-4]}.bin"):
        if os.path.exists(os.path.join(FIXTURES, chemin)):
            with open(os.path.join(FIXTURES, chemin), "rb") as f:
                return f.read()
    raise KeyError(dec)


def ok(dec, ws):
    """Lecture `ok` de la fixture, décodée par le décodeur scellé comme dans la boucle (`decodeurs.appliquer`)."""
    return decodeurs.appliquer(dec, Lecture("ok", ws * S + 40 * S, ws * S + 41 * S, code=200, octets=corps(dec)))


def panne(_dec, ws):
    return Lecture("panne_transport", ws * S + 40 * S, ws * S + 50 * S, sous_type="delai")


BTC = [("binance_btc", "binance_btc"), ("coinbase_btc", "coinbase_btc")]
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
        return {o: [self.ecrire(o, j, ws0, (fenetres or {}).get((o, j), ()), (rp or {}).get((o, j)), lire or ok)
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


class Flux(Base):                                           # passe 2 ; Q-R-03 : ruptures rendues à leur place
    def test_fenetres_fusionnees(self):
        """Fenêtres par ws croissant, journaux présents seuls ; lectures par forme (hôte et décodeur de formes.json ou
        de carte.json, forme et décodeur de noms différents, sans `brut`), panne gardée, `sante`, marqueur, démarrage
        (`run_params` à la première fenêtre admise), autre enregistrement (`asn`, écrit ici par l'écrivain)."""
        d = {"o1": self.obs.ecrire("o1", "pool", WS, [(m(1), BTC), (m(2), BTC)], lire=ok),
             "o2": self.obs.ecrire("o2", "pool", m(1), [(m(2), BTC)], lire=lambda x, ws: (panne if x == "coinbase_btc"
                                                                                           else ok)(x, ws))}
        self.obs.ecrire("o1", "secondaire", WS, [(m(1), [("binance_btc_remplacant", "binance_btc")])], lire=ok)
        self.obs.ecrire("o2", "secondaire", m(1))
        d["o3"], d["o4"] = self.obs.ecrire("o3", "pool", m(2)), [self.obs.ecrire("o4", j, m(2)) for j in
                                                                   fusion.JOURNAUX][0]
        jl = journal.Journal(d["o3"], "secondaire", fsync=lambda fd: None).ouvrir(m(2))
        jl.ecrire("run_params", m(3), **self.obs.run_params("o3", "secondaire"))
        jl.ecrire("asn", m(3), hote="api.binance.com", a=None, ip=None, ripestat=None, cymru=None)
        jl.fermer()
        f = fusion.Fusion(d, CONFIG, COMMIT)
        vues = list(f.fenetres())
        self.assertEqual([(ws, {o: sorted(x) for o, x in par.items()}) for ws, par in vues], [
            (m(1), {"o1": ["pool", "secondaire"]}), (m(2), {"o1": ["pool"], "o2": ["pool", "secondaire"]}),
            (m(3), {"o3": ["pool", "secondaire"], "o4": ["pool", "secondaire"]})])
        p = vues[0][1]["o1"]["pool"]
        self.assertEqual({k: p[k] for k in p if k != "pool"}, {
            "ws": m(1), "carte": {}, "sante": SANTE, "marqueur": True,
            "demarrage": True, "autres": [], "ruptures": [], "trous": [], "reprises": []})
        self.assertEqual({k: v for k, v in p["pool"]["binance_btc"].items() if k not in ("depart", "fin")}, {
            "prevu": m(1) * S, "statut": "ok", "sous_type": None, "code": 200, "phases": {}, "adresse": None,
            "sha256": hashlib.sha256(corps("binance_btc")).hexdigest(), "hote": "data-api.binance.vision",
            "decodeur": "binance_btc", "valeurs": [{
                "actif": "BTC", "classe": "sans_horodatage", "devise": "USDT", "extra": {}, "prix": "64529.50000000",
                "ts_source": None}]})
        o1, o2 = vues[1][1]["o1"]["pool"], vues[1][1]["o2"]["pool"]
        self.assertEqual((o1["demarrage"], o1["pool"]["coinbase_btc"]["valeurs"][0]["ts_source"], o2["demarrage"],
                          {k: o2["pool"]["coinbase_btc"][k] for k in ("statut", "sous_type", "valeurs", "hote")}),
                         (False, 1785946281674372, True, {"statut": "panne_transport", "sous_type": "delai",
                                                          "valeurs": None, "hote": "api.exchange.coinbase.com"}))
        s = vues[1][1]["o2"]["secondaire"]
        self.assertEqual((s["demarrage"], s["marqueur"], s["sante"], s["carte"]), (True, False, None, {}))
        r = vues[0][1]["o1"]["secondaire"]["carte"]
        self.assertEqual(({n: (x["hote"], x["decodeur"], x["statut"]) for n, x in r.items()},
                          vues[2][1]["o3"]["secondaire"]["autres"]), ({"binance_btc_remplacant": (
                              "api.binance.com", "binance_btc", "ok")}, [{"type": "asn", "hote": "api.binance.com", "a":
                                                                         None, "ip": None, "ripestat": None,
                                                                         "cymru": None}]))
        self.assertEqual(sorted((k, v["ruptures"]) for k, v in f.integrite.items()), [
            ((o, j), []) for o in OBS for j in fusion.JOURNAUX])

    def test_ruptures_trous_et_reprises_a_leur_place(self):
        """o2 : ligne `sante` de m(2) rendue non intègre au fichier du 2026-10-04 (octet 0xFF) : queue de ce fichier,
        rupture LECTEUR/lien au fichier du 2026-10-05, rendue dans la fenêtre m(3), sans portée en fenêtres (RB-3).
        o1 : arrêt après m(1), reprise à m(5) : `reprise` (FORMAT §2 : `suivante`, première fenêtre ni close ni
        déclarée, m(2)) et `trou` (FORMAT §8.1 : de = suivante, a = ws − w, cause `arret`) dans la fenêtre m(6)."""
        d = self.obs.quatre(fenetres={("o2", "pool"): [(m(n), BTC) for n in (1, 2, 3, 4)],
                                      ("o1", "pool"): [(m(1), BTC)]})
        chemin = os.path.join(d["o2"], "pool-2026-10-04-0.jsonl")
        with open(chemin, "rb") as f:
            lignes = f.readlines()
        k = [i for i, x in enumerate(lignes) if b'"type":"sante"' in x and b'"ws":%d' % m(2) in x][0]
        with open(chemin, "wb") as f:
            f.write(b"".join(lignes[:k]) + lignes[k].replace(b'"non_parties"', b'"\xffon_parties"') + b"".join(
                lignes[k + 1:]))
        self.obs.ecrire("o1", "pool", m(5), [(m(6), BTC)], lire=ok)
        f = fusion.Fusion(d, CONFIG, COMMIT)
        vues = {ws: par for ws, par in f.fenetres()}
        o2 = {ws: vues[ws]["o2"]["pool"] for ws in vues if "pool" in vues[ws].get("o2", {})}
        r = f.integrite["o2", "pool"]["ruptures"]
        self.assertEqual(([x["code"] for x in r], r[0]["fichier"], [(q["fichier"], q["position"], q["cause"]) for q in
                                                                    r[0]["queues"]]), (
            ["LECTEUR/lien"], "pool-2026-10-05-0.jsonl",
            [("pool-2026-10-04-0.jsonl", len(b"".join(lignes[:k])), "LECTEUR/utf8")]))
        formes = ["binance_btc", "coinbase_btc"]
        self.assertEqual({ws: (x["ruptures"], x["sante"] is not None, x["marqueur"], sorted(x["pool"])) for ws, x in
                          o2.items()}, {m(1): ([], True, True, formes), m(2): ([], False, False, formes),
                                        m(3): (r, True, True, formes), m(4): ([], True, True, formes)})
        o1 = vues[m(6)]["o1"]["pool"]
        self.assertEqual(([{k: x[k] for k in x if k != "seq"} for x in o1["reprises"]], [{k: x[k] for k in x if k !=
                                                                                         "seq"} for x in o1["trous"]],
                          o1["demarrage"], m(5) in vues), ([{"ws": m(5), "suivante": m(2), "queue": None}], [
                              {"de": m(2), "a": m(5), "cause": "arret"}], True, False))
