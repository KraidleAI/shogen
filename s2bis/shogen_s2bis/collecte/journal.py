"""Journal chaîné du collecteur (CB-1 ; E-C-18, E-C-19 ; ADR-0029 §2.9 l.238). Chaque enregistrement est une ligne
JSON canonique (clés triées, séparateurs « , » et « : », UTF-8 sans échappement, saut de ligne final, aucun flottant,
entiers de 640 chiffres au plus : SHOGEN-S2BIS-ENTIER-ECRIVAIN-1, I-1 de la G2 du recalcul ; 64 niveaux
d'imbrication au plus, la racine au niveau 1 : lettre C-4 du FORMAT, CB-18n) qui porte `seq` (rang depuis 0) et
`prec` (sha256 des octets de la ligne précédente, saut de ligne compris ; GENESE pour la première). Écriture sans
tampon ; `fsync` (injectable) au marqueur de fenêtre seulement ; la fenêtre qui clôt une heure est suivie d'un point
de contrôle `point`, dont l'empreinte est la tête exportée. Un enregistrement de
fenêtre n'est admis que sur la grille, pour une fenêtre non close (ws ≥ `suivante`) et jamais avant la dernière
fenêtre écrite (C-1). Tout refus est nommé (ErreurJournal) et n'écrit rien : l'enregistrement est contrôlé avant
toute bascule et tout trou (C-6). Après une OSError, tout appel est refusé (JOURNAL/casse, C-2). E-C-16 : un seul
écrivain par journal, verrou
exclusif sans attente (`fcntl.flock`) ; une seconde instance lève JournalOccupe avant toute lecture ou écriture.
CB-18a (SHOGEN-S2BIS-ECRIVAIN-USAGE-1) : un seul fil écrit, celui qui a ouvert l'écrivain (JOURNAL/fil sinon) ; un
écrivain s'ouvre une fois (JOURNAL/ouvert) et n'écrit qu'ouvert (JOURNAL/ferme) ; ces gardes et celle de C-2 sont
portées par `_terminal`, sur toute méthode publique d'écriture ; `fermer` s'appelle de tout fil.
E-C-20 (CB-2) : un fichier par jour UTC ; le premier enregistrement d'une fenêtre d'un jour nouveau clôt le fichier
(`cloture`, fsync), inscrit son sha256 au fichier de sommes `<préfixe>.sha256` (format de sha256sum, fsync), puis
ouvre le fichier du jour par `ouverture` ; la chaîne continue. E-C-21, E-C-22 (CB-2) : un journal existant reprend
au dernier enregistrement intègre ; une queue non intègre (ligne coupée, octets NUL, ligne de plus de LIMITE octets)
n'est jamais réécrite : un segment neuf s'ouvre par `reprise`, qui la déclare (fichier, position, octets, sha256). N-1
(SHOGEN-S2BIS-SEGMENT-JOUR-1) : un fichier neuf, à la bascule comme à la reprise, prend le numéro suivant de son jour ;
un segment de reprise prend le jour le plus tardif entre l'horloge et les fichiers présents ; l'ordre (jour, k entier)
reste celui de la chaîne, k sans zéro de tête, et un nom du préfixe hors de cette grammaire est refusé à l'ouverture
(JOURNAL/nom, lettre C-5 du FORMAT). La fenêtre du redémarrage, toute fenêtre close et toute fenêtre jusqu'à la
dernière écrite restent refusées (C-1) ; le marqueur qui suit des fenêtres sans marqueur est précédé d'un `trou`
(cause `arret`, `horloge_reculee` ou `saut`)."""
import fcntl
import hashlib
import json
import os
import re
import threading
import time

GENESE = "0" * 64
HEURE = 3600
LIMITE = 1 << 22                                                   # octets d'une ligne au plus, saut de ligne compris
ENTIER, CHAINE = (int,), (str,)    # C-2 : types exacts, comparés par type(v) ; un booléen n'est jamais un entier
CHAMPS = {"ouverture": {"jour": CHAINE, "suivante": ENTIER}, "marqueur": {"ws": ENTIER}, "point": {"ws": ENTIER},
          "cloture": {"jour": CHAINE}, "reprise": {"ws": ENTIER, "suivante": ENTIER, "queue": (list, type(None))},
          "trou": {"de": ENTIER, "a": ENTIER, "cause": CHAINE}}  # champs propres des types réservés (FORMAT §2, §7.1 d)
RESERVES = set(CHAMPS)
HEX = re.compile("[0-9a-f]{64}")
CHIFFRES = 640                     # I-1 : plus petite limite non nulle de conversion des entiers (sys.int_info)
BORNE = 10 ** CHIFFRES
NIVEAUX = 64                       # C-4 : niveaux d'imbrication au plus, la racine au niveau 1 (FORMAT §8.3)


class ErreurJournal(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


class JournalOccupe(ErreurJournal):
    pass


def _parcours(enr):
    """(entier de plus de CHIFFRES chiffres ?, niveau du plus profond conteneur de `enr`, None sur un cycle), sans
    récursion. Chaque conteneur n'est développé qu'une fois et sa hauteur est retenue : un conteneur partagé compte à
    sa plus grande profondeur, sans parcours exponentiel ; un cycle n'arrête pas la recherche des entiers."""
    long_, cycle, haut, chemin, pile = False, False, {}, set(), [(enr, False)]
    while pile:
        v, fin = pile.pop()
        long_ = long_ or isinstance(v, int) and not -BORNE < v < BORNE
        if not isinstance(v, (dict, list, tuple)) or not fin and id(v) in haut:
            continue
        enfants = list(v.values()) if isinstance(v, dict) else list(v)
        if fin:
            chemin.discard(id(v))
            haut[id(v)] = 1 + max([haut.get(id(x), 0) for x in enfants if isinstance(x, (dict, list, tuple))],
                                  default=0)
        elif id(v) in chemin:
            cycle = True                                            # le sérialiseur le refusera (JOURNAL/type)
        else:
            chemin.add(id(v))
            pile += [(v, True)] + [(x, False) for x in enfants]
    return long_, None if cycle else haut[id(enr)]


def _types(e):
    """C-2 (FORMAT §7.1, points c et d) : objet dont `type` est une chaîne, `seq` un entier et `prec` 64 chiffres
    hexadécimaux minuscules, et dont les champs propres du §2 (`ws` seul pour un type non réservé : R-2) sont présents,
    aux types exacts ; `type(v)`, jamais `isinstance`, qui admettrait un booléen pour un entier."""
    if type(e) is not dict or type(e.get("type")) is not str:
        return False
    champs = {"seq": ENTIER, "prec": CHAINE, **CHAMPS.get(e["type"], {"ws": ENTIER})}
    return all(k in e and type(e[k]) in t for k, t in champs.items()) and HEX.fullmatch(e["prec"]) is not None


def canonique(enr):
    """Octets canoniques de `enr` ; flottant, clé non textuelle, valeur hors JSON ou cycle : refus JOURNAL/type. Le
    contrôle de cycle de `json` précède le parcours, qui se termine donc (C-3). Un entier de plus de CHIFFRES chiffres
    (JOURNAL/entier, I-1) et un conteneur au-delà du niveau NIVEAUX (JOURNAL/imbrication, C-4) sont refusés avant le
    sérialiseur, quel que soit le réglage de l'interpréteur."""
    long_, niveaux = _parcours(enr)
    if long_:
        raise ErreurJournal("JOURNAL/entier", f"entier de plus de {CHIFFRES} chiffres")
    if niveaux is not None and niveaux > NIVEAUX:
        raise ErreurJournal("JOURNAL/imbrication", f"{niveaux} niveaux, {NIVEAUX} au plus")
    try:
        octets = json.dumps(enr, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
    except (TypeError, ValueError, RecursionError) as e:          # ValueError : cycle ; RecursionError : imbrication
        raise ErreurJournal("JOURNAL/type", e) from None
    pile = [enr]
    while pile:
        v = pile.pop()
        if isinstance(v, float) or isinstance(v, dict) and not all(isinstance(k, str) for k in v):
            raise ErreurJournal("JOURNAL/type", repr(v)[:80])
        pile += v.values() if isinstance(v, dict) else v if isinstance(v, (list, tuple)) else []
    return octets


def jour(ws):
    return time.strftime("%Y-%m-%d", time.gmtime(ws))


def _tout(fd, octets):
    while octets:
        octets = octets[os.write(fd, octets):]


def _empreinte(chemin, debut=0):
    """(sha256, octets) du fichier `chemin` à partir de `debut`, lu par blocs."""
    h, n = hashlib.sha256(), 0
    with open(chemin, "rb") as f:
        f.seek(debut)
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
            n += len(bloc)
    return h.hexdigest(), n


def nom(prefixe, j, k=0):
    """Fichier quotidien `k` (segment) du jour UTC `j`."""
    return f"{prefixe}-{j}-{k}.jsonl"


def _terminal(methode):
    """C-2 : une OSError (ouverture, écriture, fsync, fermeture de fichier) rend l'écrivain inutilisable ; tout
    appel suivant est refusé (JOURNAL/casse) sans rien écrire ; `fermer` rend le verrou ; l'instance suivante
    déclare la queue (`reprise`). CB-18a : écriture d'un écrivain neuf ou fermé, JOURNAL/ferme ; second `ouvrir`,
    JOURNAL/ouvert ; appel hors du fil qui a ouvert, JOURNAL/fil ; une ouverture refusée ferme l'écrivain."""
    ouverture = methode.__name__ == "ouvrir"

    def appel(self, *a, **k):
        if self.casse:
            raise ErreurJournal("JOURNAL/casse", self.casse)
        if self.etat == "ferme" or self.etat == "neuf" and not ouverture:
            raise ErreurJournal("JOURNAL/ferme", f"{methode.__name__} : écrivain {self.etat}")
        if ouverture and self.etat == "ouvert":
            raise ErreurJournal("JOURNAL/ouvert", self.prefixe)
        if self.etat == "ouvert" and self.fil is not threading.current_thread():
            raise ErreurJournal("JOURNAL/fil", f"{methode.__name__} hors du fil qui a ouvert l'écrivain")
        if ouverture:
            self.etat, self.fil = "ouvert", threading.current_thread()
        try:
            return methode(self, *a, **k)
        except OSError as e:
            self.casse = f"{methode.__name__} : {e!r}"
            raise
        except ErreurJournal:
            if ouverture:
                self.fermer()
            raise
    appel.__doc__, appel.terminal = methode.__doc__, True
    return appel


class Journal:
    def __init__(self, dossier, prefixe, w=60, fsync=os.fsync):
        if type(w) is not int or w <= 0 or HEURE % w:
            raise ErreurJournal("JOURNAL/grille", w)
        self.dossier, self.prefixe, self.w, self.fsync = dossier, prefixe, w, fsync
        self.fd = self.verrou = self.casse = self.fil = None
        self.etat = "neuf"                                          # neuf, ouvert, puis ferme (CB-18a)

    @_terminal
    def ouvrir(self, ws):
        """Verrou exclusif, puis journal ouvert à la fenêtre courante `ws` (horloge de l'appelant) ; rend le journal."""
        self.verrou = os.open(os.path.join(self.dossier, self.prefixe + ".verrou"), os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(self.verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.fermer()
            raise JournalOccupe("JOURNAL/occupe", self.prefixe) from None
        if type(ws) is not int or ws % self.w:
            raise ErreurJournal("JOURNAL/fenetre", ws)
        fichiers = self._fichiers(refus=True)
        if fichiers:
            self._reprendre(ws, fichiers)
        else:
            self.seq, self.prec, self.suivante, self.attendu, self.cause = -1, GENESE, ws + self.w, ws + self.w, "saut"
            self._creer(jour(ws), 0, {"type": "ouverture", "jour": jour(ws), "suivante": self.attendu})
        return self

    @_terminal
    def ecrire(self, genre, ws, **champs):
        """Enregistrement `genre` de la fenêtre non close `ws` ; rend la tête (seq, sha256)."""
        if not isinstance(genre, str) or genre in RESERVES:
            raise ErreurJournal("JOURNAL/reserve", genre)
        return self._fenetre(genre, ws, champs)

    @_terminal
    def marqueur(self, ws, **champs):
        """Clôt la fenêtre `ws` : marqueur, point de contrôle si elle clôt une heure, un seul fsync ; rend la tête."""
        tete = self._fenetre("marqueur", ws, champs)
        if (ws + self.w) % HEURE == 0:
            tete = self._ecrire({"type": "point", "ws": ws})
        self.fsync(self.fd)
        self.suivante, self.attendu, self.cause = ws + self.w, ws + self.w, "saut"
        return tete

    def fermer(self):
        """Ferme le fichier et libère le verrou, sans fsync : n'est durable que ce qui précède le dernier marqueur. Le
        verrou est rendu même si la fermeture du fichier échoue (C-2). Appel admis de tout fil ; l'écrivain reste
        fermé (CB-18a)."""
        try:
            if self.fd is not None:
                self._clore()
        finally:
            verrou, self.verrou, self.etat = self.verrou, None, "ferme"
            if verrou is not None:
                os.close(verrou)

    def _clore(self):
        """Ferme le fichier courant ; son descripteur est oublié d'abord : un numéro rendu n'est jamais refermé."""
        fd, self.fd = self.fd, None
        os.close(fd)

    def _fenetre(self, genre, ws, champs):
        if champs.keys() & {"seq", "prec"}:
            raise ErreurJournal("JOURNAL/reserve", sorted(champs.keys() & {"seq", "prec"}))
        if type(ws) is not int or ws % self.w or ws < self.suivante:
            raise ErreurJournal("JOURNAL/fenetre", f"{genre} {ws!r} hors grille ou passée (suivante {self.suivante})")
        enr, bascule = {**champs, "type": genre, "ws": ws}, jour(ws) > self.jour
        trou = genre == "marqueur" and ws > self.attendu
        self._ligne(enr, self.seq + 1 + 2 * bascule + trou)         # C-6 : refus avant toute bascule et tout trou
        if bascule:                                                 # bascule de 00:00 UTC
            self._ecrire({"type": "cloture", "jour": self.jour})
            self.fsync(self.fd)
            self._clore()
            self._sommer(nom(self.prefixe, self.jour, self.k), self.h.hexdigest())
            self._creer(jour(ws), self._numero(jour(ws)),                     # N-1 : numéro suivant du jour
                        {"type": "ouverture", "jour": jour(ws), "suivante": self.attendu})
        if trou:
            self._ecrire({"type": "trou", "de": self.attendu, "a": ws - self.w, "cause": self.cause})
        self.suivante = ws                                          # C-1 : ws non décroissant dans l'exécution
        return self._ecrire(enr)

    def _fichiers(self, refus=False):
        """(jour, k, nom) des fichiers du journal, dans l'ordre (jour, k entier) ; k en décimal sans zéro de tête (C-5,
        FORMAT §6.1). `refus` (à l'ouverture) : un nom du préfixe en `.jsonl` hors de cette grammaire est refusé
        (JOURNAL/nom) ; sinon (bascule) il est ignoré."""
        motif = re.compile(re.escape(self.prefixe) + "-([0-9]{4}-[0-9]{2}-[0-9]{2})-(0|[1-9][0-9]*)[.]jsonl")
        noms = os.listdir(self.dossier)
        autres = [n for n in noms if n.startswith(self.prefixe + "-") and n.endswith(".jsonl") and not
                  motif.fullmatch(n)]
        if refus and autres:
            raise ErreurJournal("JOURNAL/nom", sorted(autres))
        return sorted((x[1], int(x[2]), x[0]) for x in map(motif.fullmatch, noms) if x)

    def _numero(self, j):
        """Numéro du fichier neuf du jour `j` : 1 + le plus grand présent au dossier, 0 sans fichier du jour (N-1)."""
        return 1 + max([k for jj, k, _n in self._fichiers() if jj == j], default=-1)

    def _sommer(self, n, h):
        """Ligne « sha256  nom » du fichier clos `n` au fichier de sommes (format de sha256sum), puis fsync."""
        fd = os.open(os.path.join(self.dossier, self.prefixe + ".sha256"), os.O_WRONLY | os.O_APPEND | os.O_CREAT,
                     0o644)
        _tout(fd, f"{h}  {n}\n".encode())
        self.fsync(fd)
        os.close(fd)

    def _creer(self, j, k, premier):
        """Fichier neuf du jour `j`, segment `k`, ouvert par l'enregistrement `premier`."""
        self.jour, self.k, self.h = j, k, hashlib.sha256()
        self.fd = os.open(os.path.join(self.dossier, nom(self.prefixe, j, k)), os.O_WRONLY | os.O_APPEND | os.O_CREAT |
                          os.O_EXCL, 0o644)
        return self._ecrire(premier)

    def _lire(self, n):
        """(position de la queue, état, empreinte du préfixe intègre) du fichier `n`. Intègre : définition unique du
        FORMAT §7.1, points (a) à (e) (lettres C-1, C-2 et C-4) ; la lecture s'arrête à la première ligne non intègre.
        État : celui du dernier intègre, ou None ; `derniere` : ws du dernier enregistrement écrit par `ecrire` ou
        `marqueur`, None si le fichier n'en a pas."""
        etat, pos, h = None, 0, hashlib.sha256()
        with open(os.path.join(self.dossier, n), "rb") as f:
            while (ligne := f.readline(LIMITE)).endswith(b"\n"):
                try:
                    e = json.loads(ligne)
                    intact = _types(e) and canonique(e) == ligne                     # (c), (d), puis (b)
                except (ValueError, RecursionError, ErreurJournal):
                    intact = False
                if intact:                                                          # (e)
                    intact = (e["seq"], e["prec"]) == (etat["seq"] + 1, etat["prec"]) if etat else e["type"] in (
                        "ouverture", "reprise")
                if not intact:
                    break
                t = e["type"]
                if t in ("ouverture", "reprise"):
                    attendu = e["suivante"]                    # première fenêtre ni close ni déclarée en trou
                elif t in ("marqueur", "trou"):
                    attendu = e["ws" if t == "marqueur" else "a"] + self.w
                else:
                    attendu = etat["attendu"]
                derniere = e["ws"] if t == "marqueur" or t not in RESERVES else etat and etat["derniere"]
                etat = {"seq": e["seq"], "prec": hashlib.sha256(ligne).hexdigest(), "type": t, "attendu": attendu,
                        "derniere": derniere}
                h.update(ligne)
                pos += len(ligne)
        return pos, etat, h

    def _reprendre(self, ws, fichiers):
        """Reprise au dernier intègre ; queues déclarées, fichiers achevés sommés ; segment neuf si queue, fichier clos
        ou jour passé (clos ici). C-1 : la dernière fenêtre écrite, cherchée au besoin dans les fichiers précédents, et
        toute fenêtre antérieure restent refusées."""
        queues, lus = [], ((j, k, n, *self._lire(n)) for j, k, n in reversed(fichiers))
        for j, k, n, pos, etat, h in lus:
            q, taille = _empreinte(os.path.join(self.dossier, n), pos)
            if taille:
                queues.insert(0, {"fichier": n, "position": pos, "octets": taille, "sha256": q})
            if etat:
                break
        else:
            raise ErreurJournal("JOURNAL/illisible", "aucun enregistrement intègre")
        derniere = etat["derniere"]
        while derniere is None and (x := next(lus, None)):        # fichier sans fenêtre écrite : le précédent
            derniere = x[4] and x[4]["derniere"]
        self.seq, self.prec, self.attendu = etat["seq"], etat["prec"], etat["attendu"]
        self.jour, self.k, self.h = j, k, h
        self.suivante = max(self.attendu, (derniere or 0) + self.w, ws + self.w)
        self.cause = "horloge_reculee" if ws + self.w < self.attendu else "arret"
        ouvert = not queues and etat["type"] != "cloture"
        if ouvert:
            self.fd = os.open(os.path.join(self.dossier, n), os.O_WRONLY | os.O_APPEND)
        reprise = {"type": "reprise", "ws": ws, "suivante": self.attendu, "queue": queues or None}
        if ouvert and jour(ws) <= j:
            self._sommes([x for _j, _k, x in fichiers if x != n])
            self._ecrire(reprise)
        else:
            if ouvert:
                self._ecrire({"type": "cloture", "jour": j})
                self.fsync(self.fd)
                self._clore()
            self._sommes([x for _j, _k, x in fichiers])
            jn = max(jour(ws), fichiers[-1][0])                 # N-1 : jamais avant le jour d'un fichier présent
            self._creer(jn, self._numero(jn), reprise)
        self.fsync(self.fd)

    def _sommes(self, noms):
        """Inscrit au fichier de sommes chaque fichier de `noms` qui n'y est pas (coupure avant l'inscription) ; une
        dernière ligne coupée y est close par un saut de ligne, jamais réécrite."""
        chemin, texte = os.path.join(self.dossier, self.prefixe + ".sha256"), ""
        if os.path.exists(chemin):
            with open(chemin, encoding="utf-8", errors="replace") as f:
                texte = f.read()
        if texte and not texte.endswith("\n"):
            fd = os.open(chemin, os.O_WRONLY | os.O_APPEND)
            _tout(fd, b"\n")
            os.close(fd)
        lus = {ligne.split("  ", 1)[-1] for ligne in texte.split("\n")}
        for x in noms:
            if x not in lus:
                self._sommer(x, _empreinte(os.path.join(self.dossier, x))[0])

    def _ecrire(self, enr):
        octets = self._ligne(enr, self.seq + 1, self.prec)
        _tout(self.fd, octets)
        self.h.update(octets)
        self.seq, self.prec = self.seq + 1, hashlib.sha256(octets).hexdigest()
        return self.seq, self.prec

    def _ligne(self, enr, seq, prec=GENESE):
        """Octets canoniques de `enr` au rang `seq` ; un `prec` fictif a la longueur du vrai. Plus de LIMITE octets :
        refus JOURNAL/taille."""
        octets = canonique({**enr, "seq": seq, "prec": prec})
        if len(octets) > LIMITE:
            raise ErreurJournal("JOURNAL/taille", len(octets))
        return octets
