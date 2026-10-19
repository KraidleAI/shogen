"""Fusion des journaux des quatre observateurs de S2-bis (RB-2 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION l.470,
E-R-04 ; ADR-0029 l.219 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §14.4, §15.6). `Fusion(dossiers,
config, commit)` lit les journaux `pool` et `secondaire` de chaque observateur par le lecteur en flux de RB-1.
Passe 1, à la construction, avant tout calcul (E-R-04) : observateurs lus égaux à la liste fermée
d'`observateurs.json` ; dans chaque journal, un `run_params` au moins, et pour chacun les clés porteuses présentes,
`commit` égal au commit scellé, `sha256` et contenus des fichiers scellés égaux à ceux du paquet (CONFIGS, lus en
octets), descripteur au nom de l'observateur, concordance avec le premier démarrage ; descripteur égal entre les deux
journaux de l'observateur. Tout écart est un refus nommé (RefusFusion, `FUSION/…` ; ceux du lecteur, `LECTEUR/…`,
remontent tels quels).
Passe 2 (`fenetres`) : les huit journaux relus en flux et fusionnés par fenêtre, observateur et journal (lectures par
forme, pannes comprises, `sante`, marqueur, démarrage, autres enregistrements), mémoire d'une fenêtre par journal ;
ruptures du lecteur, `trou` et `reprise` rendus à leur place, dans la fenêtre qui les suit, sans portée en fenêtres
(Q-R-03, AVIS l.108 : RB-3) ; rien n'est imprimé (rendu : RB-15, RB-16). Re-décodage (E-R-03) : chaque `lecture`
`ok` ou `panne_decode` re-décodée en passe 2 par le décodeur scellé de sa forme (`collecte.decodeurs`, seule entrée de
`collecte`, RB2-a), verdict `redecodage` : égalités comptées, écarts listés, jamais réparés."""
import base64
import binascii
import hashlib
import heapq
import itertools
import json
import os

from ..collecte.decodeurs import decoder
from .lecteur import RESERVES, Lecteur, _canonique

JOURNAUX = ("pool", "secondaire")                       # préfixes des deux journaux d'un observateur (FORMAT §15.1)
CONFIGS = ("formes", "sante", "observateurs", "carte")  # fichiers du paquet (s2bis/config/) portés par `run_params`
SCELLES = {"pool": ("formes", "sante", "observateurs"), "secondaire": ("formes", "carte")}      # FORMAT §14.4, §15.6
PORTEUSES = ("commit", "sha256", "descripteur")         # clés porteuses avec SCELLES ; `python` non porteuse (Q-RB2-2)
STRUCTURE = ("type", "seq", "prec", "ws")               # champs communs, hors des champs propres
LECTURE = ("forme", "prevu", "statut", "sous_type", "code", "depart", "fin", "phases", "adresse", "brut", "sha256",
           "valeurs")                                   # champs propres exacts d'une `lecture` (FORMAT §9.1, §11.2)
ENSEMBLE = {"pool": "pool", "secondaire": "carte"}      # ensemble des lectures de chaque journal
ATTENTE = ("ruptures", "trous", "reprises")             # rattachés à la fenêtre qui les suit
REDECODES = ("ok", "panne_decode")                      # statuts dont le corps a été décodé (E-R-03 ; Q-RB2-6)


class RefusFusion(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def paquet(dossier):
    """{nom : (données, sha256 des octets lus)} des fichiers `<nom>.json` de CONFIGS dans `dossier` ; JSON illisible :
    FUSION/config."""
    lus = {}
    for nom in CONFIGS:
        with open(os.path.join(dossier, nom + ".json"), "rb") as f:
            octets = f.read()
        try:
            lus[nom] = json.loads(octets.decode("utf-8")), hashlib.sha256(octets).hexdigest()
        except ValueError as e:                             # UnicodeDecodeError comprise
            raise RefusFusion("FUSION/config", f"{nom}.json : {e}") from None
    return lus


def champs(e):
    """Champs propres de l'enregistrement `e`."""
    return {k: v for k, v in e.items() if k not in STRUCTURE}


def _sans_extra(v):
    """Relevés `v` sans leur `extra` : comparaison des valeurs seules, puis des `extra`."""
    return [{k: x for k, x in r.items() if k != "extra"} if type(r) is dict else r for r in v] if type(v) is list else v


def fenetre(ws):
    """Fenêtre `ws` d'un journal : lectures par forme dans les ensembles `pool` et `carte`, `sante`, marqueur,
    démarrage (`run_params`), autres enregistrements (`tetes`, `asn`, `releve_asn`), ruptures, trous et reprises."""
    return {"ws": ws, **{k: {} for k in ENSEMBLE.values()}, "sante": None, "marqueur": False, "demarrage": False,
            "autres": [], **{k: [] for k in ATTENTE}}


class Fusion:
    def __init__(self, dossiers, config, commit):
        """Passe 1. `dossiers` : {observateur : dossier de ses journaux `pool` et `secondaire`} (Q-RB2-4) ; `config` :
        dossier du paquet ; `commit` : commit scellé. Refus nommé au premier écart, avant tout calcul."""
        self.paquet, self.dossiers, self.commit = paquet(config), dossiers, commit
        self.liste = self.paquet["observateurs"][0]["observateurs"]
        if sorted(dossiers) != sorted(self.liste):
            raise RefusFusion("FUSION/observateurs", f"{sorted(dossiers)} lus, liste fermée {self.liste}")
        self.run_params, self.tetes = {}, {}
        for o in self.liste:
            for j in JOURNAUX:
                self.run_params[o, j], self.tetes[o, j] = self._demarrages(o, j)
            if len({_canonique(self.run_params[o, j]["descripteur"]) for j in JOURNAUX}) > 1:
                raise RefusFusion("FUSION/descripteur", f"{o} : descripteurs du pool et du secondaire différents")
        lus = {"pool": self.paquet["formes"][0], "secondaire": self.paquet["carte"][0]}
        self.formes = {j: {x["nom"]: x for x in c["formes"]} for j, c in lus.items()}       # forme : hôte, décodeur

    def _demarrages(self, o, j):
        """(premier `run_params`, tête) du journal `j` de `o` ; chaque `run_params` contrôlé (`_controler`)."""
        lec, premier = Lecteur(self.dossiers[o], j), None
        for genre, *x in lec:
            if genre == "enr" and x[1]["type"] == "run_params":
                premier = premier or champs(x[1])
                self._controler(f"{o}/{j}, seq {x[1]['seq']}", o, j, champs(x[1]), premier)
        if premier is None:
            raise RefusFusion("FUSION/run_params-absent", f"{o}/{j}")
        return premier, lec.tete

    def _controler(self, ou, o, j, rp, premier):
        """Un `run_params` (E-R-04) : clés porteuses présentes ; commit scellé ; `sha256` aux clés exactes, égal au
        paquet pour SCELLES ; contenus égaux au paquet (forme canonique, Q-RB2-3) ; descripteur de l'observateur `o` ;
        clés porteuses égales à celles du premier démarrage (le descripteur, le reste étant égal au paquet)."""
        cles = PORTEUSES + SCELLES[j]
        if absentes := [k for k in cles if k not in rp]:
            raise RefusFusion("FUSION/run_params-cle", f"{ou} : {absentes}")
        if rp["commit"] != self.commit:
            raise RefusFusion("FUSION/commit", f"{ou} : {rp['commit']!r}")
        sha = rp["sha256"]
        if type(sha) is not dict or sorted(sha) != sorted(SCELLES[j] + ("descripteur",)) or any(
                sha[n] != self.paquet[n][1] for n in SCELLES[j]):
            raise RefusFusion("FUSION/sha256", ou)
        if any(_canonique(rp[n]) != _canonique(self.paquet[n][0]) for n in SCELLES[j]):
            raise RefusFusion("FUSION/contenu", ou)
        if type(rp["descripteur"]) is not dict or rp["descripteur"].get("observateur") != o:
            raise RefusFusion("FUSION/observateur", ou)
        if discordantes := [k for k in cles if _canonique(rp[k]) != _canonique(premier[k])]:
            raise RefusFusion("FUSION/run_params-discordant", f"{ou} : {discordantes}")

    def fenetres(self):
        """Passe 2 : (ws, {observateur : {journal : fenêtre}}) par ws croissant ; une fenêtre ne porte que les journaux
        qui y ont écrit. Après l'itération, `integrite` : {(o, j) : tête, ruptures, queues déclarées, queue finale} ;
        `redecodage` : égalités, écarts {observateur, journal, seq, ws, forme, cause}."""
        self.integrite, self.redecodage = {}, {"egalites": 0, "ecarts": []}
        flux = heapq.merge(*(self._flux(o, j) for o in self.liste for j in JOURNAUX), key=lambda x: x[0])
        for ws, groupe in itertools.groupby(flux, key=lambda x: x[0]):
            par = {}
            for _ws, o, j, f in groupe:
                par.setdefault(o, {})[j] = f
            yield ws, par

    def _flux(self, o, j):
        """(ws, o, j, fenêtre) du journal `j` de `o` par ws croissant (FORMAT §3.2 ; sinon FUSION/ordre, Q-RB2-7) ;
        ruptures, `trou` et `reprise` rattachés à la fenêtre du premier enregistrement de fenêtre qui les suit ; tête
        de la relecture égale à celle de la passe 1, sinon FUSION/relecture (Q-RB2-5)."""
        lec, f, attente = Lecteur(self.dossiers[o], j), None, {k: [] for k in ATTENTE}
        for genre, *x in lec:
            if genre == "rupture":
                attente["ruptures"].append(x[0])
                continue
            e = x[1]
            if e["type"] in ("trou", "reprise"):
                attente[e["type"] + "s"].append({k: v for k, v in e.items() if k not in ("type", "prec")})
            if e["type"] in RESERVES - {"marqueur"}:
                continue
            if f is not None and e["ws"] != f["ws"]:
                if e["ws"] < f["ws"]:
                    raise RefusFusion("FUSION/ordre", f"{o}/{j}, seq {e['seq']} : ws {e['ws']} après {f['ws']}")
                yield f["ws"], o, j, f
                f = None
            f = f or fenetre(e["ws"])
            for k in ATTENTE:
                f[k] += attente[k]
            attente = {k: [] for k in ATTENTE}
            self._ranger(o, j, f, e)
        if f is not None:
            yield f["ws"], o, j, f
        if lec.tete != self.tetes[o, j]:
            raise RefusFusion("FUSION/relecture", f"{o}/{j} : tête {lec.tete}, {self.tetes[o, j]} en passe 1")
        self.integrite[o, j] = {"tete": lec.tete, "ruptures": lec.ruptures, "queues": lec.queues,
                                "queue_finale": lec.queue_finale}

    def _ranger(self, o, j, f, e):
        """Range l'enregistrement de fenêtre `e` dans `f` ; `lecture` aux champs exacts (FUSION/lecture), de forme
        configurée (FUSION/forme), re-décodée ; une forme ou une `sante` deux fois dans la fenêtre : FUSION/double."""
        t, c, ou = e["type"], champs(e), f"{o}/{j}, seq {e['seq']}"
        if t == "lecture":
            x = self.formes[j].get(c.get("forme")) if type(c.get("forme")) is str else None
            if sorted(c) != sorted(LECTURE) or x is None:
                raise RefusFusion("FUSION/lecture" if x else "FUSION/forme", f"{ou} : {sorted(c)}")
            if c["forme"] in f[ENSEMBLE[j]]:
                raise RefusFusion("FUSION/double", f"{ou} : {c['forme']}")
            f[ENSEMBLE[j]][c["forme"]] = {**{k: v for k, v in c.items() if k not in ("forme", "brut")},
                                          "hote": x["hote"], "decodeur": x["decodeur"],
                                          "redecodage": self._redecoder(o, j, e, x["decodeur"])}
        elif t == "sante":
            if f["sante"] is not None:
                raise RefusFusion("FUSION/double", f"{ou} : sante")
            f["sante"] = c
        elif t in ("marqueur", "run_params"):
            f["marqueur" if t == "marqueur" else "demarrage"] = True
        else:
            f["autres"].append({"type": t, **c})

    def _redecoder(self, o, j, e, dec):
        """E-R-03 : octets de `brut` (base64 strict) re-décodés par le décodeur scellé `dec` de la forme ; égalité
        exigée du sha256 journalisé, du statut, des valeurs, puis de leurs `extra`. Verdict « egal », compté, ou cause
        de l'écart, consignée ; une égalité fausse est un constat, jamais une réparation : la lecture garde ses valeurs
        journalisées. Statut hors REDECODES : None (corps jamais décodé par le collecteur)."""
        if e["statut"] not in REDECODES:
            return None
        try:
            octets = base64.b64decode(e["brut"], validate=True)
        except (binascii.Error, TypeError, ValueError):     # alphabet, remplissage, type ; texte non ASCII
            cause = "base64"
        else:
            statut, valeurs = decoder(dec, octets)
            cause = next((n for n, egal in (
                ("sha256", hashlib.sha256(octets).hexdigest() == e["sha256"]), ("statut", statut == e["statut"]),
                ("valeurs", _canonique(_sans_extra(valeurs)) == _canonique(_sans_extra(e["valeurs"]))),
                ("extra", _canonique(valeurs) == _canonique(e["valeurs"]))) if not egal), None)
        if cause is None:
            self.redecodage["egalites"] += 1
            return "egal"
        self.redecodage["ecarts"].append({"observateur": o, "journal": j, "seq": e["seq"], "ws": e["ws"],
                                          "forme": e["forme"], "cause": cause})
        return cause
