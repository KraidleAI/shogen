"""Lecteur en flux des journaux d'observateur de S2-bis (RB-1 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION E-R-01,
E-R-02 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §1 à §8). Fichiers d'un préfixe lus dans l'ordre de la
chaîne (jour, segment), ligne à ligne (LIMITE octets au plus), jamais un fichier en mémoire : mémoire bornée quelle que
soit la longueur du journal. Ligne intègre au sens de la définition unique du FORMAT §7.1, points (a) à (e), celle de
l'écrivain de référence (`collecte/journal.py` `_lire` ; lettres C-1 et C-2 du FORMAT, C-14 de la G2 de RB-18) :
terminée par 0x0A, objet JSON canonique aux conteneurs de 64 niveaux au plus, comptés par le lecteur (lettre C-4 ;
C-15), `type` chaîne, `seq` entier, `prec` de 64 chiffres hexadécimaux minuscules, champs propres du §2 présents et
typés (un booléen n'est jamais un entier), chaînée à la précédente du fichier, première ligne `ouverture` ou
`reprise` ; la première ligne non intègre d'un fichier et la suite forment sa queue, cause nommée
(`LECTEUR/entier-long` pour un entier de plus de CHIFFRES chiffres, quel que soit le réglage `int_max_str_digits` de
l'interpréteur). Le lecteur contrôle en plus ce que l'écrivain ne contrôle pas (FORMAT §7.7) :
genèse (`seq` 0, `prec` nul, `ouverture`), lien de chaque fichier au précédent, déclaration exacte des queues par la
`reprise` qui les suit, dans l'ordre (jour, k) de leurs fichiers, comparée sous forme canonique (FORMAT §7.4, lettre
C-3 ; C-15). Tout autre cas est une rupture : rendue à sa place dans le flux avec toutes les queues en attente, sans
arrêt ni réparation ; l'enregistrement qui la suit devient l'ancre de la chaîne (portée en fenêtres : Q-R-03,
sous-lot RB-3). Une queue non déclarée en fin de journal est tolérée (`queue_finale`)."""
import hashlib
import json
import os
import re

GENESE = "0" * 64
LIMITE = 1 << 22                       # octets d'une ligne au plus, saut de ligne compris (FORMAT §7.1)
CHIFFRES = 640                         # entier JSON : 640 chiffres au plus, plus petit int_max_str_digits non nul
NIVEAUX = 64                           # conteneurs au niveau 64 au plus, la racine au niveau 1 (FORMAT §8.3, C-4)
BARRE = bytes([92])                    # barre oblique inverse, écrite par sa valeur
HORS_CROCHETS = bytes(x for x in range(256) if x not in b"[]{}")      # octets effacés avant le compte des niveaux
ENTIER, CHAINE = (int,), (str,)        # types exacts, comparés par type(v) : un booléen n'est jamais un entier (C-2)
CHAMPS = {"ouverture": {"jour": CHAINE, "suivante": ENTIER}, "marqueur": {"ws": ENTIER}, "point": {"ws": ENTIER},
          "cloture": {"jour": CHAINE}, "reprise": {"ws": ENTIER, "suivante": ENTIER, "queue": (list, type(None))},
          "trou": {"de": ENTIER, "a": ENTIER, "cause": CHAINE}}      # champs propres des types réservés (§2, §7.1 d)
RESERVES = set(CHAMPS)
HEX = re.compile("[0-9a-f]{64}")       # `prec` : 64 chiffres hexadécimaux minuscules (FORMAT §1.3, §7.1 c)
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


def _trop_profonde(ligne):
    """Vrai si un conteneur de la ligne passe le niveau NIVEAUX (FORMAT §8.3, lettre C-4 ; la racine au niveau 1).
    Niveaux comptés sur les octets, sans décodeur, donc sans dépendre de RecursionError ni de la version : échappements
    retirés (barre doublée, puis barre et guillemet), les guillemets restants bornent les chaînes, et seuls les
    crochets hors des chaînes comptent."""
    hors = b"".join(ligne.replace(BARRE * 2, b"").replace(BARRE + b'"', b"").split(b'"')[::2])
    n = 0
    for c in hors.translate(None, HORS_CROCHETS):
        n += 1 if c in b"[{" else -1
        if n > NIVEAUX:
            return True
    return False


def _types(e):
    """Points (c) et (d) du FORMAT §7.1 (lettre C-2 ; C-14) : un objet ; `type` chaîne, `seq` entier, `prec` de 64
    chiffres hexadécimaux minuscules ; champs propres du §2 présents, aux types exacts, `ws` entier pour un type non
    réservé (risque R-2). `type(v)`, jamais `isinstance`, qui admettrait un booléen pour un entier."""
    if type(e) is not dict or type(e.get("type")) is not str:
        return False
    exiges = {"seq": ENTIER, "prec": CHAINE, **CHAMPS.get(e["type"], {"ws": ENTIER})}
    return all(k in e and type(e[k]) in t for k, t in exiges.items()) and HEX.fullmatch(e["prec"]) is not None


def _canonique(v):
    """Texte JSON canonique de `v` (FORMAT §1.2 : clés triées, séparateurs sans espace, UTF-8 en clair). Deux valeurs
    s'y égalent si et seulement si elles s'écrivent de même : `true` n'y égale jamais `1`, ce que `==` admet (C-15)."""
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _integre(ligne, etat):
    """(enregistrement, état) d'une ligne intègre, sinon _NonIntegre(cause) ; définition unique du FORMAT §7.1 : (a)
    ligne close par 0x0A (`LECTEUR/fin`), d'au plus LIMITE octets (borne de sa lecture, `readline(LIMITE)`) ; (b)
    conteneurs au niveau NIVEAUX au plus, comptés avant tout décodeur (`LECTEUR/imbrication` ; une RecursionError du
    décodeur n'est jamais un verdict : elle remonte, C-4), objet JSON canonique (`LECTEUR/json`, `canonique`,
    `flottant`), entiers de CHIFFRES chiffres au plus (`LECTEUR/entier-long`) ; (c), (d) types de `_types`
    (`LECTEUR/champ`) ; (e) chaînée à la ligne précédente du fichier, la première étant une `ouverture` ou une
    `reprise` (`LECTEUR/chaine`). `etat` : celui de la ligne précédente du fichier, None pour la première. État rendu :
    (seq + 1, sha256 de la ligne, attendu, dernière fenêtre) ; seq + 1 et le sha256 sont le `seq` et le `prec` exigés
    de la ligne suivante ; attendu : `suivante` d'une `ouverture` ou d'une `reprise`, `ws` d'un `marqueur`, `a` d'un
    `trou`, sinon celui de l'état précédent (l'écrivain retient `ws + w` et `a + w`) ; dernière fenêtre : `ws` d'un
    `marqueur` ou d'un enregistrement hors RESERVES, sinon celle de l'état précédent (None à la première ligne)."""
    if not ligne.endswith(b"\n"):
        raise _NonIntegre("LECTEUR/fin")
    if _trop_profonde(ligne):
        raise _NonIntegre("LECTEUR/imbrication")
    try:
        e = json.loads(ligne, parse_int=_entier, parse_float=_cause("LECTEUR/flottant"),
                       parse_constant=_cause("LECTEUR/flottant"))
        canon = _canonique(e).encode() + b"\n"
    except ValueError:
        raise _NonIntegre("LECTEUR/json") from None
    if canon != ligne:
        raise _NonIntegre("LECTEUR/canonique")
    if not _types(e):
        raise _NonIntegre("LECTEUR/champ")
    t = e["type"]
    lien = (e["seq"], e["prec"]) == etat[:2] if etat else t in ("ouverture", "reprise")
    if not lien:
        raise _NonIntegre("LECTEUR/chaine")
    if t in ("ouverture", "reprise"):
        attendu = e["suivante"]
    elif t in ("marqueur", "trou"):
        attendu = e["ws" if t == "marqueur" else "a"]
    else:
        attendu = etat[2]                                       # la première ligne est une ouverture ou une reprise
    derniere = e["ws"] if t == "marqueur" or t not in RESERVES else etat and etat[3]
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
        `reprise` : déclaration exacte des queues en attente, dans l'ordre (jour, k) de leurs fichiers, comparée sous
        forme canonique (null sans queue ; FORMAT §7.4, lettre C-3 ; C-15) ; sinon, aucune queue en attente."""
        if premier and ((e["seq"], e.get("prec")) != chaine or e["seq"] == 0 and e["type"] != "ouverture"):
            return "LECTEUR/lien"
        if e["type"] == "reprise":
            declare = [{k: q[k] for k in QUEUE} for q in attente] or None
            return None if _canonique(e["queue"]) == _canonique(declare) else "LECTEUR/declaration"
        return "LECTEUR/queue-non-declaree" if attente else None
