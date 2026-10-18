"""Fusion des journaux des quatre observateurs de S2-bis (RB-2 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION l.470,
E-R-04 ; ADR-0029 l.219 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §14.4, §15.6). `Fusion(dossiers,
config, commit)` lit les journaux `pool` et `secondaire` de chaque observateur par le lecteur en flux de RB-1.
Passe 1, à la construction, avant tout calcul (E-R-04) : observateurs lus égaux à la liste fermée
d'`observateurs.json`, l'un des fichiers du paquet (CONFIGS, lus en octets). Tout écart est un refus nommé
(RefusFusion, `FUSION/…`)."""
import hashlib
import json
import os

JOURNAUX = ("pool", "secondaire")                       # préfixes des deux journaux d'un observateur (FORMAT §15.1)
CONFIGS = ("formes", "sante", "observateurs", "carte")  # fichiers du paquet (s2bis/config/) portés par `run_params`


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


class Fusion:
    def __init__(self, dossiers, config, commit):
        """Passe 1. `dossiers` : {observateur : dossier de ses journaux `pool` et `secondaire`} (Q-RB2-4) ; `config` :
        dossier du paquet ; `commit` : commit scellé. Refus nommé au premier écart, avant tout calcul."""
        self.paquet, self.dossiers, self.commit = paquet(config), dossiers, commit
        self.liste = self.paquet["observateurs"][0]["observateurs"]
        if sorted(dossiers) != sorted(self.liste):
            raise RefusFusion("FUSION/observateurs", f"{sorted(dossiers)} lus, liste fermée {self.liste}")
