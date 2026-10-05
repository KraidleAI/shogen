"""Lecteur indépendant des journaux de S2-bis (RB-18 ; E-R-33 ; PROPOSITION du G0 de RECALC-BIS l.396, l.459, l.486,
l.539-540, l.551 ; AVIS Q-R-08). Écrit d'après le seul FORMAT (docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md) par un
autre auteur que le lecteur principal (RB-1) ; n'importe ni lui ni l'écrivain : bibliothèque standard seule.
Ligne (§1.1, §1.2, §7.1 a et b, §8.3) : octets terminés par 0x0A, objet JSON canonique, sans flottant ni NaN
(échappements de `json` : Q-R18-3), dont tout entier a au plus CHIFFRES chiffres, signe exclu, et tout conteneur un
niveau d'au plus NIVEAUX, l'objet de la ligne au niveau 1 ; les niveaux sont comptés ici sur le texte, avant le
décodeur, jamais par son exception (lettres C-1 et C-4 du FORMAT). Hors de ces bornes, la ligne n'est pas intègre :
jamais un refus. Champs (§1.3, §2, §7.1 c et d ; lettre C-2) : `type` chaîne, `seq` entier, `prec` 64 chiffres
hexadécimaux minuscules ; champs propres d'un type réservé, `ws` de tout autre type, présents et aux types du §2.
Fichiers (§6.1, §7.2) : `<préfixe>-AAAA-MM-JJ-k.jsonl`, k décimal sans zéro de tête, en ordre (jour, k entier) ;
autres noms ignorés (Q-R18-5). Fichier (§7.1) : lignes intègres jusqu'à la première qui ne l'est pas (sans 0x0A,
plus de LIMITE octets, non canonique, sans les champs communs, non chaînée ; la première est une `ouverture` ou une
`reprise`), qui ouvre la queue du fichier.
Jonction au premier enregistrement de chaque fichier et à chaque `reprise` (§1.3, §7.4, §7.7) : lien au dernier intègre
(genèse : `ouverture`, `seq` 0, `prec` nul) ; queues en attente déclarées par la `reprise` (quatre champs, comparés
sous forme canonique) ; sinon rupture à causes nommées (`genese`, `lien`, `queue-non-declaree`, `declaration`), la
lecture continue, rien n'est réparé (Q-R18-6, Q-R18-7). Queue finale : queues qu'aucun intègre ne suit (E-R-01 ;
Q-R18-8). Tête : dernier intègre (§1.4). Sortie (`sortie`, `main`) : JSON canonique, clés triées, un objet suivi
de 0x0A."""
import hashlib
import json
import os
import re
import sys

LIMITE = 1 << 22            # octets d'une ligne au plus, saut de ligne compris (§7.1 a)
CHIFFRES = 640              # chiffres d'un entier au plus, signe exclu (§1.2) : lu sous tout réglage de l'interpréteur
NIVEAUX = 64                # niveau d'un conteneur au plus, l'objet de la ligne au niveau 1 (§8.3)
GENESE, NL, BS = "0" * 64, bytes((10,)), chr(92)
HEX = re.compile("[0-9a-f]{64}")
PROPRES = {"ouverture": "jour suivante", "marqueur": "ws", "point": "ws", "cloture": "jour",
           "reprise": "ws suivante queue", "trou": "de a cause"}             # champs propres des types réservés (§2)
SORTES = {"type": (str,), "prec": (str,), "jour": (str,), "cause": (str,), "queue": (list, type(None))}  # sinon int
ECHAPPEMENTS, CHAINES, AUTRES = re.compile(BS * 2 + "."), re.compile('"[^"]*"'), re.compile("[^][{}]+")
FORMAT = "shogen.s2bis.oracle-indep.v1"


class RefusOracle(Exception):
    def __init__(self, code, detail, fichier=None, position=None):
        super().__init__(f"{code} : {detail}")
        self.code, self.fichier, self.position = code, fichier, position


def entier(t):
    """Entier JSON `t`, lu exactement s'il a au plus CHIFFRES chiffres, signe exclu (§1.2) ; sinon ValueError."""
    if len(t) - t.startswith("-") > CHIFFRES:
        raise ValueError(f"plus de {CHIFFRES} chiffres")
    return int(t)


def interdit(t):
    """Nombre à virgule, NaN ou infini : jamais dans une ligne (§1.2)."""
    raise ValueError(t)


def niveau(texte):
    """Niveau du plus profond conteneur de `texte` (§8.3), compté ici, sans décodeur : échappements, puis chaînes, puis
    tout sauf crochets et accolades sont retirés ; le compte s'arrête au-delà de NIVEAUX."""
    n = haut = 0
    for c in AUTRES.sub("", CHAINES.sub("", ECHAPPEMENTS.sub("", texte))):
        n += 1 if c in "[{" else -1
        haut = max(haut, n)
        if haut > NIVEAUX:
            break
    return haut


def objet(ligne):
    """Objet canonique porté par `ligne` (octets, 0x0A final compris), ou None : la ligne n'en porte pas (§7.1 b)."""
    if not ligne.endswith(NL):
        return None
    try:
        texte = ligne[:-1].decode("utf-8")
        if niveau(texte) > NIVEAUX:                         # avant le décodeur : jamais RecursionError (§8.3)
            return None
        e = json.loads(texte, parse_int=entier, parse_float=interdit, parse_constant=interdit)
        forme = cle(e).encode("utf-8") + NL
    except ValueError:              # UTF-8, JSON, entier long, nombre interdit, surrogat seul (UnicodeEncodeError)
        return None
    return e if type(e) is dict and forme == ligne else None


def champs(e):
    """Types des champs de l'objet `e` (§7.1 c et d) : `seq`, `prec`, puis les champs propres du type (`ws` pour un type
    non réservé), présents ; `jour` et `cause` chaînes, `queue` liste ou null, les autres entiers. Un booléen n'est
    jamais un entier ; un champ de plus est admis."""
    if type(e.get("type")) is not str:
        return False
    noms = ["seq", "prec", *PROPRES.get(e["type"], "ws").split()]
    return all(n in e and type(e[n]) in SORTES.get(n, (int,)) for n in noms) and HEX.fullmatch(e["prec"]) is not None


def fichiers(dossier, prefixe):
    """Noms des fichiers du journal `prefixe` de `dossier`, dans l'ordre de la chaîne."""
    motif = re.compile(re.escape(prefixe) + "-([0-9]{4}-[0-9]{2}-[0-9]{2})-(0|[1-9][0-9]*)[.]jsonl")
    return [n for _j, _k, n in sorted((m[1], int(m[2]), m[0]) for m in map(motif.fullmatch, os.listdir(dossier)) if m)]


def cle(x):
    """Forme canonique (§1.2) : clés triées, séparateurs sans espace, hors ASCII en UTF-8 ; `true` n'égale pas 1."""
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class Lecture:
    """Lecture en flux du journal `prefixe` de `dossier` : itérer rend chaque enregistrement intègre {fichier, position,
    sha256, enr}, dans l'ordre de la chaîne ; l'itération finie, `ruptures`, `queues_declarees`, `queue_finale` et
    `tete` sont complets. Mémoire : une ligne de LIMITE octets au plus, et les queues en attente."""

    def __init__(self, dossier, prefixe):
        self.dossier, self.prefixe = dossier, prefixe
        self.noms, self.ruptures, self.queues_declarees, self.queue_finale, self.tete = [], [], [], [], None

    def __iter__(self):
        base, attente = None, []                            # (seq, sha256) du dernier intègre ; queues non soldées
        try:
            self.noms = fichiers(self.dossier, self.prefixe)
            for nom in self.noms:
                with open(os.path.join(self.dossier, nom), "rb") as f:
                    pos, prec = 0, None
                    while ligne := f.readline(LIMITE):
                        e = self._integre(ligne, prec)
                        if e is None:
                            attente.append(self._queue(f, nom, pos))
                            break
                        h = hashlib.sha256(ligne).hexdigest()
                        if prec is None or e["type"] == "reprise":
                            self._jonction(nom, pos, e, base, attente)
                        yield {"fichier": nom, "position": pos, "sha256": h, "enr": e}
                        prec = base = (e["seq"], h)
                        pos += len(ligne)
        except OSError as x:
            raise RefusOracle("ORACLE/lecture", repr(x)) from None
        self.queue_finale, self.tete = attente, base and {"seq": base[0], "sha256": base[1]}

    @staticmethod
    def _integre(ligne, prec):
        """Enregistrement intègre de `ligne`, ou None (§7.1) ; `prec` : (seq, sha256) de la ligne d'avant, ou None."""
        e = objet(ligne)
        if e is None or not champs(e):
            return None
        if prec is None:
            return e if e["type"] in ("ouverture", "reprise") else None
        return e if (e["seq"], e["prec"]) == (prec[0] + 1, prec[1]) else None

    @staticmethod
    def _queue(f, nom, pos):
        """Queue de `f` à partir de l'octet `pos` : {fichier, position, octets, sha256} (§7.4)."""
        f.seek(pos)
        h, n = hashlib.sha256(), 0
        while bloc := f.read(1 << 20):
            h.update(bloc)
            n += len(bloc)
        return {"fichier": nom, "position": pos, "octets": n, "sha256": h.hexdigest()}

    def _jonction(self, nom, pos, e, base, attente):
        causes = []
        if base is None:
            causes += ["genese"] * ((e["type"], e["seq"], e["prec"]) != ("ouverture", 0, GENESE))
        else:
            causes += ["lien"] * ((e["seq"], e["prec"]) != (base[0] + 1, base[1]))
        d = e.get("queue") if e["type"] == "reprise" else None
        declarees, non = [cle(x) for x in (d if type(d) is list else [] if d is None else [d])], []
        for q in attente:
            if cle(q) in declarees:
                declarees.remove(cle(q))
                self.queues_declarees.append(q)
            else:
                non.append(q)
        causes += ["queue-non-declaree"] * bool(non) + ["declaration"] * bool(declarees)
        if causes:
            self.ruptures.append({"fichier": nom, "position": pos, "seq": e["seq"], "causes": sorted(causes),
                                  "queues": non})
        attente.clear()


def lire(dossier, prefixe):
    """Sortie de l'oracle, tout le journal en mémoire (fixtures et bancs)."""
    lec = Lecture(dossier, prefixe)
    enregistrements = list(lec)
    return {"enregistrements": enregistrements, "fichiers": lec.noms, "format": FORMAT, "tete": lec.tete,
            "queue_finale": lec.queue_finale, "queues_declarees": lec.queues_declarees, "ruptures": lec.ruptures}


def sortie(r):
    """Octets canoniques de `r` (clés triées, séparateurs sans espace, UTF-8), suivis de 0x0A."""
    return cle(r).encode("utf-8") + NL


def main(argv):
    """`python3 -m shogen_s2bis.recalc.oracle_indep DOSSIER PREFIXE`, lancé depuis s2bis/ : `sortie(lire(…))`, code 0 ;
    refus nommé : {fichier, format, position, refus}, code 1 ; usage : code 2, rien sur la sortie standard."""
    if len(argv) != 2:
        print("usage : python3 -m shogen_s2bis.recalc.oracle_indep DOSSIER PREFIXE", file=sys.stderr)
        return 2
    try:
        octets, code = sortie(lire(*argv)), 0
    except RefusOracle as r:
        octets, code = sortie({"fichier": r.fichier, "format": FORMAT, "position": r.position, "refus": r.code}), 1
    sys.stdout.buffer.write(octets)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
