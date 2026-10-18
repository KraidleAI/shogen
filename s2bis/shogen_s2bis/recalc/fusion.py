"""Fusion des journaux des quatre observateurs de S2-bis (RB-2 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION l.470,
E-R-04 ; ADR-0029 l.219 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §14.4, §15.6). `Fusion(dossiers,
config, commit)` lit les journaux `pool` et `secondaire` de chaque observateur par le lecteur en flux de RB-1.
Passe 1, à la construction, avant tout calcul (E-R-04) : observateurs lus égaux à la liste fermée
d'`observateurs.json` ; dans chaque journal, un `run_params` au moins, et pour chacun les clés porteuses présentes,
`commit` égal au commit scellé, `sha256` et contenus des fichiers scellés égaux à ceux du paquet (CONFIGS, lus en
octets), descripteur au nom de l'observateur, concordance avec le premier démarrage ; descripteur égal entre les deux
journaux de l'observateur. Tout écart est un refus nommé (RefusFusion, `FUSION/…` ; ceux du lecteur, `LECTEUR/…`,
remontent tels quels)."""
import hashlib
import json
import os

from .lecteur import Lecteur, _canonique

JOURNAUX = ("pool", "secondaire")                       # préfixes des deux journaux d'un observateur (FORMAT §15.1)
CONFIGS = ("formes", "sante", "observateurs", "carte")  # fichiers du paquet (s2bis/config/) portés par `run_params`
SCELLES = {"pool": ("formes", "sante", "observateurs"), "secondaire": ("formes", "carte")}      # FORMAT §14.4, §15.6
PORTEUSES = ("commit", "sha256", "descripteur")         # clés porteuses avec SCELLES ; `python` non porteuse (Q-RB2-2)
STRUCTURE = ("type", "seq", "prec", "ws")               # champs communs, hors des champs propres


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
