"""Fusion des journaux des quatre observateurs de S2-bis (RB-2 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION l.470,
E-R-04 ; ADR-0029 l.219 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §14.4, §15.6). `Fusion(dossiers,
config, commit)` lit les journaux `pool` et `secondaire` de chaque observateur par le lecteur en flux de RB-1.
Passe 1, à la construction, avant tout calcul (E-R-04) : observateurs lus égaux à la liste fermée
d'`observateurs.json` ; un observateur sans aucun journal est absent (constat `FUSION/observateur-absent`, D-1 jugé à
RB-3 ; C-1, adjudication de Q-RB2-13), QUORUM présents au moins, sinon `FUSION/quorum` ; un journal sur deux :
`LECTEUR/absent`. Dans chaque journal présent, un `run_params` au moins, et pour chacun les clés porteuses présentes,
`commit` égal au commit scellé, `sha256` et contenus des fichiers scellés égaux à ceux du paquet (CONFIGS, lus en
octets), descripteur au nom de l'observateur, concordance avec le premier démarrage ; descripteur égal entre les deux
journaux de l'observateur. Tout écart est un refus nommé (RefusFusion, `FUSION/…` ; ceux du lecteur, `LECTEUR/…`,
remontent tels quels).
Passe 2 (`fenetres`) : les huit journaux relus en flux et fusionnés par fenêtre, observateur et journal (lectures par
forme, pannes comprises, `sante`, marqueur, démarrage, autres enregistrements), mémoire d'une fenêtre par journal ;
ruptures du lecteur, `trou` et `reprise` rendus à leur place, dans la fenêtre qui les suit, sans portée en fenêtres
(Q-R-03, AVIS l.108 : RB-3), ceux qu'aucun enregistrement de fenêtre ne suit en fin de journal (`sans_fenetre`,
C-3 de la G2) ; intégrité relue égale à celle de la passe 1 (C-2 de la G2) ; rien n'est imprimé (rendu : RB-15,
RB-16). Re-décodage (E-R-03) : chaque `lecture` `ok` ou `panne_decode` re-décodée en passe 2 par le décodeur scellé de
sa forme (`collecte.decodeurs`, seule entrée de `collecte`, RB2-a), `brut` au base64 canonique et sha256 contrôlés
d'abord (C-1 de la G2), verdict `redecodage` : égalités comptées, écarts listés, jamais réparés. Filtres nommés : témoin
(`est_temoin`, SHOGEN-S2BIS-TEMOIN-RECALC-1 ; ADR-0029 l.174), hors des classes USD et de tout vote, dans l'ensemble
descriptif `temoin`, daté par ses blocs ; remplaçants de la carte (`est_remplacant`,
SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 ; Q-C-08), hors des sources de la carte, dans l'ensemble `remplacants`."""
import base64
import binascii
import hashlib
import heapq
import itertools
import json
import os

from ..collecte.decodeurs import DECODEURS, decoder
from .config_analyse import TEMOIN
from .lecteur import RESERVES, Lecteur, RefusLecteur, _canonique

JOURNAUX = ("pool", "secondaire")                       # préfixes des deux journaux d'un observateur (FORMAT §15.1)
CONFIGS = ("formes", "sante", "observateurs", "carte")  # fichiers du paquet (s2bis/config/) portés par `run_params`
SCELLES = {"pool": ("formes", "sante", "observateurs"), "secondaire": ("formes", "carte")}      # FORMAT §14.4, §15.6
PORTEUSES = ("commit", "sha256", "descripteur")         # clés porteuses avec SCELLES ; `python` non porteuse (Q-RB2-2)
STRUCTURE = ("type", "seq", "prec", "ws")               # champs communs, hors des champs propres
LECTURE = ("forme", "prevu", "statut", "sous_type", "code", "depart", "fin", "phases", "adresse", "brut", "sha256",
           "valeurs")                                   # champs propres exacts d'une `lecture` (FORMAT §9.1, §11.2)
ENSEMBLES = ("pool", "temoin", "carte", "remplacants")  # pool et témoin au journal `pool`, les autres au secondaire
SUFFIXE = "_remplacant"                                 # formes remplaçantes de la carte (GEL-9, Q-C-08)
ATTENTE = ("ruptures", "trous", "reprises")             # rattachés à la fenêtre qui les suit
REDECODES = ("ok", "panne_decode")                      # statuts dont le corps a été décodé (E-R-03 ; Q-RB2-6)
QUORUM = 3                  # observateurs présents au moins (ADR-0029 l.78 : quorum 2 sur 3 ; l.219 : repli M = 3)


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


def releve(lec):
    """Intégrité d'une lecture complète du lecteur `lec` : tête, ruptures, queues déclarées, queue finale. Égale entre
    les deux passes, elle fixe chaque ligne intègre (chaque tronçon de chaîne est fixé par la ligne qui le clôt : la
    tête ou le `apres` de la rupture qui le suit) et chaque queue (sha256) : C-2 de la G2."""
    return {"tete": lec.tete, "ruptures": lec.ruptures, "queues": lec.queues, "queue_finale": lec.queue_finale}


def est_temoin(decodeur, valeurs):
    """Filtre du témoin (SHOGEN-S2BIS-TEMOIN-RECALC-1 ; ADR-0029 l.174 : « hors des classes USD et hors du vote ») :
    vrai si le décodeur scellé de la forme est de classe TEMOIN (pannes comprises), ou si un relevé journalisé l'est."""
    return DECODEURS[decodeur][2] == TEMOIN or type(valeurs) is list and any(
        type(r) is dict and r.get("classe") == TEMOIN for r in valeurs)


def est_remplacant(forme):
    """Filtre des remplaçants (SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 ; FORMAT §15.2) : forme de la carte au suffixe
    SUFFIXE, lue hors du vote (Q-C-08), écartée des sources de la carte descriptive."""
    return forme.endswith(SUFFIXE)


def blocs(valeurs):
    """Datage du témoin sur chaîne (B.115 ; FORMAT §9.1) : [(bloc_avant, bloc_apres)] entiers des relevés qui les
    portent ; [] pour OKX, daté par `ts_source`."""
    return [(int(r["extra"]["bloc_avant"]), int(r["extra"]["bloc_apres"])) for r in valeurs if "bloc_avant" in r[
        "extra"]]


def fenetre(ws):
    """Fenêtre `ws` d'un journal : lectures par forme dans les ENSEMBLES, `sante`, marqueur, démarrage
    (`run_params`), autres enregistrements (`tetes`, `asn`, `releve_asn`), ruptures, trous et reprises."""
    return {"ws": ws, **{k: {} for k in ENSEMBLES}, "sante": None, "marqueur": False, "demarrage": False,
            "autres": [], **{k: [] for k in ATTENTE}}


class Fusion:
    def __init__(self, dossiers, config, commit):
        """Passe 1. `dossiers` : {observateur : dossier de ses journaux `pool` et `secondaire`} (Q-RB2-4) ; `config` :
        dossier du paquet ; `commit` : commit scellé. Refus nommé au premier écart, avant tout calcul."""
        self.paquet, self.dossiers, self.commit = paquet(config), dossiers, commit
        self.liste = self.paquet["observateurs"][0]["observateurs"]
        if sorted(dossiers) != sorted(self.liste):
            raise RefusFusion("FUSION/observateurs", f"{sorted(dossiers)} lus, liste fermée {self.liste}")
        self.presents, self.constats = [], []
        for o in self.liste:
            lus = [j for j in JOURNAUX if self._present(o, j)]
            if len(lus) == len(JOURNAUX):
                self.presents.append(o)
            elif lus:
                raise RefusLecteur("LECTEUR/absent", f"{o} : {lus[0]} présent, l'autre journal absent")
            else:
                self.constats.append({"code": "FUSION/observateur-absent", "observateur": o})
        self.absents = [c["observateur"] for c in self.constats]
        if len(self.presents) < QUORUM:
            raise RefusFusion("FUSION/quorum", f"{len(self.presents)} observateurs présents, {QUORUM} au moins")
        self.run_params, self.passe1 = {}, {}
        for o in self.presents:
            for j in JOURNAUX:
                self.run_params[o, j], self.passe1[o, j] = self._demarrages(o, j)
            if len({_canonique(self.run_params[o, j]["descripteur"]) for j in JOURNAUX}) > 1:
                raise RefusFusion("FUSION/descripteur", f"{o} : descripteurs du pool et du secondaire différents")
        lus = {"pool": self.paquet["formes"][0], "secondaire": self.paquet["carte"][0]}
        self.formes = {j: {x["nom"]: x for x in c["formes"]} for j, c in lus.items()}       # forme : hôte, décodeur

    def _present(self, o, j):
        """Vrai si le journal `j` de `o` a un fichier au moins ; dossier absent ou aucun fichier : faux (C-1) ; tout
        autre refus du lecteur (noms hors grammaire) remonte."""
        try:
            return bool(Lecteur(self.dossiers[o], j).fichiers())
        except FileNotFoundError:
            return False
        except NotADirectoryError:                          # C-5 de la G2 : refus nommé, jamais une absence
            raise RefusFusion("FUSION/dossier", f"{o} : {self.dossiers[o]} n'est pas un dossier") from None
        except RefusLecteur as e:
            if e.code != "LECTEUR/absent":
                raise
            return False

    def _demarrages(self, o, j):
        """(premier `run_params`, intégrité) du journal `j` de `o` ; chaque `run_params` contrôlé (`_controler`)."""
        lec, premier = Lecteur(self.dossiers[o], j), None
        for genre, *x in lec:
            if genre == "enr" and x[1]["type"] == "run_params":
                premier = premier or champs(x[1])
                self._controler(f"{o}/{j}, seq {x[1]['seq']}", o, j, champs(x[1]), premier)
        if premier is None:
            raise RefusFusion("FUSION/run_params-absent", f"{o}/{j}")
        return premier, releve(lec)

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
        qui y ont écrit. Après l'itération, `integrite` : {(o, j) : tête, ruptures, queues déclarées, queue finale,
        `sans_fenetre`} ; `redecodage` : égalités, écarts {observateur, journal, seq, ws, forme, cause}."""
        self.integrite, self.redecodage = {}, {"egalites": 0, "ecarts": []}
        flux = heapq.merge(*(self._flux(o, j) for o in self.presents for j in JOURNAUX), key=lambda x: x[0])
        for ws, groupe in itertools.groupby(flux, key=lambda x: x[0]):
            par = {}
            for _ws, o, j, f in groupe:
                par.setdefault(o, {})[j] = f
            yield ws, par

    def _flux(self, o, j):
        """(ws, o, j, fenêtre) du journal `j` de `o` par ws croissant (FORMAT §3.2 ; sinon FUSION/ordre, Q-RB2-7) ;
        ruptures, `trou` et `reprise` rattachés à la fenêtre du premier enregistrement de fenêtre qui les suit, ou
        rendus en `sans_fenetre` si aucun ne les suit (C-3 de la G2) ; intégrité de la relecture (`releve`) égale à
        celle de la passe 1, sinon FUSION/relecture (Q-RB2-5 ; C-2 de la G2)."""
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
        if releve(lec) != self.passe1[o, j]:
            raise RefusFusion("FUSION/relecture", f"{o}/{j} : intégrité autre qu'en passe 1 (tête {lec.tete}, "
                                                  f"{self.passe1[o, j]['tete']} en passe 1)")
        self.integrite[o, j] = {**releve(lec), "sans_fenetre": attente}

    def _ranger(self, o, j, f, e):
        """Range l'enregistrement de fenêtre `e` dans `f` ; `lecture` aux champs exacts (FUSION/lecture), de forme
        configurée (FUSION/forme), re-décodée ; une forme ou une `sante` deux fois dans la fenêtre : FUSION/double."""
        t, c, ou = e["type"], champs(e), f"{o}/{j}, seq {e['seq']}"
        if t == "lecture":
            x = self.formes[j].get(c.get("forme")) if type(c.get("forme")) is str else None
            if sorted(c) != sorted(LECTURE) or x is None:
                raise RefusFusion("FUSION/lecture" if x else "FUSION/forme", f"{ou} : {sorted(c)}")
            if any(c["forme"] in f[k] for k in ENSEMBLES):
                raise RefusFusion("FUSION/double", f"{ou} : {c['forme']}")
            lu = {**{k: v for k, v in c.items() if k not in ("forme", "brut")}, "hote": x["hote"],
                  "decodeur": x["decodeur"], "redecodage": self._redecoder(o, j, e, x["decodeur"])}
            if j == "secondaire":
                f["remplacants" if est_remplacant(c["forme"]) else "carte"][c["forme"]] = lu
            elif est_temoin(x["decodeur"], c["valeurs"]):
                f["temoin"][c["forme"]] = {**lu, "blocs": blocs(c["valeurs"]) if lu["redecodage"] == "egal" and c[
                    "statut"] == "ok" else None}
            else:
                f["pool"][c["forme"]] = lu
        elif t == "sante":
            if f["sante"] is not None:
                raise RefusFusion("FUSION/double", f"{ou} : sante")
            f["sante"] = c
        elif t in ("marqueur", "run_params"):
            f["marqueur" if t == "marqueur" else "demarrage"] = True
        else:
            f["autres"].append({"type": t, **c})

    def _redecoder(self, o, j, e, dec):
        """E-R-03 : `brut` exigé égal au base64 canonique de ses octets (FORMAT §9.1 ; `b64decode` admet des bits de
        fin non nuls, et un remplissage en trop jusqu'à 3.12 : C-1 de la G2), sha256 journalisé contrôlé, puis octets
        re-décodés par le décodeur scellé `dec` de la forme ; égalité exigée du statut, des valeurs, puis de leurs
        `extra`. Verdict « egal », compté, ou cause
        de l'écart, consignée ; une égalité fausse est un constat, jamais une réparation : la lecture garde ses valeurs
        journalisées. Statut hors REDECODES : None (corps jamais décodé par le collecteur)."""
        if e["statut"] not in REDECODES:
            return None
        try:
            octets = base64.b64decode(e["brut"], validate=True)
            canonique = base64.b64encode(octets).decode("ascii") == e["brut"]
        except (binascii.Error, TypeError, ValueError):     # alphabet, remplissage, type ; texte non ASCII
            canonique = False
        if not canonique:
            cause = "base64"
        elif hashlib.sha256(octets).hexdigest() != e["sha256"]:
            cause = "sha256"                                # octets non authentifiés : jamais décodés
        else:
            statut, valeurs = decoder(dec, octets)
            cause = next((n for n, egal in (("statut", statut == e["statut"]), (
                "valeurs", _canonique(_sans_extra(valeurs)) == _canonique(_sans_extra(e["valeurs"]))),
                ("extra", _canonique(valeurs) == _canonique(e["valeurs"]))) if not egal), None)
        if cause is None:
            self.redecodage["egalites"] += 1
            return "egal"
        self.redecodage["ecarts"].append({"observateur": o, "journal": j, "seq": e["seq"], "ws": e["ws"],
                                          "forme": e["forme"], "cause": cause})
        return cause
