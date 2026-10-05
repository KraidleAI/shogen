"""Lecteur en flux des journaux d'observateur de S2-bis (RB-1 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION E-R-01,
E-R-02 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §1 à §8). Fichiers d'un préfixe lus dans l'ordre de la
chaîne (jour, segment), ligne à ligne (LIMITE octets au plus), jamais un fichier en mémoire : mémoire bornée quelle que
soit la longueur du journal. Ligne intègre au sens de l'écrivain de référence (FORMAT §7.1, `collecte/journal.py`
`_lire`) : terminée par 0x0A, JSON canonique, chaînée à la précédente du fichier, première ligne `ouverture` ou
`reprise`, champs typés comme l'écrivain les relit ; la première ligne non intègre d'un fichier et la suite forment sa
queue, cause nommée (`LECTEUR/entier-long` pour un entier de plus de CHIFFRES chiffres, quel que soit le réglage
`int_max_str_digits` de l'interpréteur). Le lecteur contrôle en plus ce que l'écrivain ne contrôle pas (FORMAT §7.7) :
genèse (`seq` 0, `prec` nul, `ouverture`), lien de chaque fichier au précédent, déclaration exacte des queues par la
`reprise` qui les suit. Tout autre cas est une rupture : rendue à sa place dans le flux, sans arrêt ni réparation ;
l'enregistrement qui la suit devient l'ancre de la chaîne (portée en fenêtres : Q-R-03, sous-lot RB-3). Une queue non
déclarée en fin de journal est tolérée (`queue_finale`)."""
import hashlib
import json
import os
import re

GENESE = "0" * 64
LIMITE = 1 << 22                       # octets d'une ligne au plus, saut de ligne compris (FORMAT §7.1)
RESERVES = {"ouverture", "marqueur", "point", "cloture", "reprise", "trou"}
CHIFFRES = 640                         # entier JSON : 640 chiffres au plus, plus petit int_max_str_digits non nul
QUEUE = ("fichier", "position", "octets", "sha256")    # champs d'une queue déclarée (FORMAT §7.4)


class RefusLecteur(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


class _NonIntegre(Exception):
    pass


def _cause(code):
    def lever(*_a):
        raise _NonIntegre(code)
    return lever


def _entier(t):
    if len(t.lstrip("-")) > CHIFFRES:
        raise _NonIntegre("LECTEUR/entier-long")
    return int(t)


def _integre(ligne, etat):
    """(enregistrement, état) d'une ligne intègre, sinon _NonIntegre(cause) ; `etat` : celui de la ligne précédente du
    fichier, None pour la première. État rendu : (seq + 1, sha256 de la ligne, attendu, dernière fenêtre) ; seq + 1 et
    le sha256 sont le `seq` et le `prec` exigés de la ligne suivante ; attendu : `suivante` d'une `ouverture` ou d'une
    `reprise`, `ws` d'un `marqueur`, `a` d'un `trou`, sinon celui de l'état précédent (l'écrivain retient `ws + w` et
    `a + w` ; le lecteur n'en garde que le type, entier exigé, contrôlé comme chez l'écrivain) ; dernière fenêtre :
    `ws` d'un `marqueur` ou d'un enregistrement hors RESERVES, sinon celle de l'état précédent (None à la première
    ligne)."""
    if not ligne.endswith(b"\n"):
        raise _NonIntegre("LECTEUR/fin")
    try:
        e = json.loads(ligne, parse_int=_entier, parse_float=_cause("LECTEUR/flottant"),
                       parse_constant=_cause("LECTEUR/flottant"))
        canon = json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
    except (ValueError, RecursionError):
        raise _NonIntegre("LECTEUR/json") from None
    if canon != ligne:
        raise _NonIntegre("LECTEUR/canonique")
    try:
        t = e["type"]
        lien = (e["seq"], e["prec"]) == etat[:2] if etat else t in ("ouverture", "reprise") and type(e["seq"]) is int
        if t in ("ouverture", "reprise"):
            attendu = e["suivante"]
        elif t in ("marqueur", "trou"):
            attendu = e["ws" if t == "marqueur" else "a"] + 0          # type de « ws + w » chez l'écrivain
        else:
            attendu = etat[2] if etat else None                  # première ligne : seules ouverture et reprise
        derniere = e["ws"] if t == "marqueur" or t not in RESERVES else etat and etat[3]
    except (KeyError, TypeError):
        raise _NonIntegre("LECTEUR/champ") from None
    if not lien:
        raise _NonIntegre("LECTEUR/chaine")
    if type(attendu) is not int or not (derniere is None or type(derniere) is int):
        raise _NonIntegre("LECTEUR/champ")
    return e, (e["seq"] + 1, hashlib.sha256(ligne).hexdigest(), attendu, derniere)


def _empreinte(chemin, debut):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        f.seek(debut)
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


class Lecteur:
    """`iter(Lecteur(dossier, préfixe))` rend ("enr", fichier, enregistrement) pour chaque enregistrement intègre, dans
    l'ordre de la chaîne, et ("rupture", {code, fichier, seq, apres, queues}) juste avant l'ancre qui suit une rupture.
    Après la lecture : `tete` (seq et sha256 de la dernière ligne intègre, ou None), `ruptures`, `queues` (déclarées et
    contrôlées), `queue_finale` (non déclarées en fin de journal, tolérées) ; chaque queue porte sa cause."""

    def __init__(self, dossier, prefixe):
        self.dossier, self.prefixe = dossier, prefixe

    def fichiers(self):
        motif = re.compile(re.escape(self.prefixe) + r"-([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]+)[.]jsonl")
        noms = sorted((m[1], int(m[2]), m[0]) for m in map(motif.fullmatch, os.listdir(self.dossier)) if m)
        if not noms:
            raise RefusLecteur("LECTEUR/absent", f"aucun fichier {self.prefixe}-*.jsonl dans {self.dossier}")
        return [n for _j, _k, n in noms]

    def __iter__(self):
        self.tete, self.ruptures, self.queues, self.queue_finale = None, [], [], []   # d'une lecture
        chaine, attente = (0, GENESE), []                   # (seq attendu, prec attendu) ; queues non encore déclarées
        for nom in self.fichiers():
            chemin, pos, etat, cause = os.path.join(self.dossier, nom), 0, None, "LECTEUR/fin"
            with open(chemin, "rb") as f:
                while ligne := f.readline(LIMITE):
                    try:
                        e, etat_suivant = _integre(ligne, etat)
                    except _NonIntegre as x:
                        cause = x.args[0]
                        break
                    code = self._controle(e, etat is None, chaine, attente)
                    if code:
                        self.ruptures.append({"code": code, "fichier": nom, "seq": e["seq"], "apres": self.tete,
                                              "queues": attente})
                        yield "rupture", self.ruptures[-1]
                    elif e["type"] == "reprise":
                        self.queues += attente
                    attente = []
                    etat, pos = etat_suivant, pos + len(ligne)
                    chaine, self.tete = etat[:2], (e["seq"], etat[1])
                    yield "enr", nom, e
            taille = os.path.getsize(chemin) - pos
            if taille:
                attente = attente + [{"fichier": nom, "position": pos, "octets": taille,
                                      "sha256": _empreinte(chemin, pos), "cause": cause}]
        self.queue_finale = attente

    @staticmethod
    def _controle(e, premier, chaine, attente):
        """Code de rupture, ou None. Au premier enregistrement d'un fichier : genèse ou lien au précédent ; à toute
        `reprise` : déclaration exacte des queues en attente (null sans queue) ; sinon, aucune queue en attente."""
        if premier and ((e["seq"], e.get("prec")) != chaine or e["seq"] == 0 and e["type"] != "ouverture"):
            return "LECTEUR/lien"
        if e["type"] == "reprise":
            declare = [{k: q[k] for k in QUEUE} for q in attente] or None
            return None if e.get("queue") == declare else "LECTEUR/declaration"
        return "LECTEUR/queue-non-declaree" if attente else None
