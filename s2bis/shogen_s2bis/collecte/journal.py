"""Journal chaîné du collecteur (CB-1 ; E-C-18, E-C-19 ; ADR-0029 §2.9 l.238). Chaque enregistrement est une ligne
JSON canonique (clés triées, séparateurs « , » et « : », UTF-8 sans échappement, saut de ligne final, aucun flottant)
qui porte `seq` (rang depuis 0) et `prec` (sha256 des octets de la ligne précédente, saut de ligne compris ; GENESE
pour la première). Écriture sans tampon ; `fsync` (injectable) au marqueur de fenêtre seulement ; la fenêtre qui clôt
une heure est suivie d'un point de contrôle `point`, dont l'empreinte est la tête exportée. Un enregistrement de
fenêtre n'est admis que sur la grille et pour une fenêtre non close (ws ≥ `suivante`). Tout refus est nommé
(ErreurJournal) et n'écrit rien. CB-1 : journal neuf seulement. E-C-16 : un seul écrivain par journal, verrou
exclusif sans attente (`fcntl.flock`) ; une seconde instance lève JournalOccupe avant toute lecture ou écriture.
E-C-20 (CB-2) : un fichier par jour UTC ; le premier enregistrement d'une fenêtre d'un jour nouveau clôt le fichier
(`cloture`, fsync), inscrit son sha256 au fichier de sommes `<préfixe>.sha256` (format de sha256sum, fsync), puis
ouvre le fichier du jour par `ouverture` ; la chaîne continue."""
import fcntl
import hashlib
import json
import os
import time

GENESE = "0" * 64
HEURE = 3600
RESERVES = {"ouverture", "marqueur", "point", "cloture", "reprise", "trou"}


class ErreurJournal(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


class JournalOccupe(ErreurJournal):
    pass


def canonique(enr):
    """Octets canoniques de `enr` ; flottant, clé non textuelle ou valeur hors JSON : refus JOURNAL/type."""
    pile = [enr]
    while pile:
        v = pile.pop()
        if isinstance(v, float) or isinstance(v, dict) and not all(isinstance(k, str) for k in v):
            raise ErreurJournal("JOURNAL/type", repr(v)[:80])
        pile += v.values() if isinstance(v, dict) else v if isinstance(v, (list, tuple)) else []
    try:
        return json.dumps(enr, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
    except (TypeError, ValueError) as e:
        raise ErreurJournal("JOURNAL/type", e) from None


def jour(ws):
    return time.strftime("%Y-%m-%d", time.gmtime(ws))


def _tout(fd, octets):
    while octets:
        octets = octets[os.write(fd, octets):]


def nom(prefixe, j, k=0):
    """Fichier quotidien `k` (segment) du jour UTC `j`."""
    return f"{prefixe}-{j}-{k}.jsonl"


class Journal:
    def __init__(self, dossier, prefixe, w=60, fsync=os.fsync):
        if type(w) is not int or w <= 0 or HEURE % w:
            raise ErreurJournal("JOURNAL/grille", w)
        self.dossier, self.prefixe, self.w, self.fsync = dossier, prefixe, w, fsync
        self.fd = self.verrou = None

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
        if any(n.startswith(self.prefixe + "-") for n in os.listdir(self.dossier)):
            raise ErreurJournal("JOURNAL/existant", self.prefixe)
        self.seq, self.prec, self.suivante = -1, GENESE, ws + self.w
        self._creer(jour(ws), 0, "ouverture")
        return self

    def ecrire(self, genre, ws, **champs):
        """Enregistrement `genre` de la fenêtre non close `ws` ; rend la tête (seq, sha256)."""
        if not isinstance(genre, str) or genre in RESERVES:
            raise ErreurJournal("JOURNAL/reserve", genre)
        return self._fenetre(genre, ws, champs)

    def marqueur(self, ws, **champs):
        """Clôt la fenêtre `ws` : marqueur, point de contrôle si elle clôt une heure, un seul fsync ; rend la tête."""
        tete = self._fenetre("marqueur", ws, champs)
        if (ws + self.w) % HEURE == 0:
            tete = self._ecrire({"type": "point", "ws": ws})
        self.fsync(self.fd)
        self.suivante = ws + self.w
        return tete

    def fermer(self):
        """Ferme le fichier et libère le verrou, sans fsync : n'est durable que ce qui précède le dernier marqueur."""
        for fd in (self.fd, self.verrou):
            if fd is not None:
                os.close(fd)
        self.fd = self.verrou = None

    def _fenetre(self, genre, ws, champs):
        if champs.keys() & {"seq", "prec"}:
            raise ErreurJournal("JOURNAL/reserve", sorted(champs.keys() & {"seq", "prec"}))
        if type(ws) is not int or ws % self.w or ws < self.suivante:
            raise ErreurJournal("JOURNAL/fenetre", f"{genre} {ws!r} hors grille ou close (suivante {self.suivante})")
        if jour(ws) > self.jour:                                    # bascule de 00:00 UTC
            self._ecrire({"type": "cloture", "jour": self.jour})
            self.fsync(self.fd)
            os.close(self.fd)
            self._sommer(nom(self.prefixe, self.jour, self.k), self.h.hexdigest())
            self._creer(jour(ws), 0, "ouverture")
        return self._ecrire({**champs, "type": genre, "ws": ws})

    def _sommer(self, n, h):
        """Ligne « sha256  nom » du fichier clos `n` au fichier de sommes (format de sha256sum), puis fsync."""
        fd = os.open(os.path.join(self.dossier, self.prefixe + ".sha256"), os.O_WRONLY | os.O_APPEND | os.O_CREAT,
                     0o644)
        _tout(fd, f"{h}  {n}\n".encode())
        self.fsync(fd)
        os.close(fd)

    def _creer(self, j, k, genre, **champs):
        """Fichier neuf du jour `j`, segment `k`, ouvert par l'enregistrement `genre`, qui porte `suivante`."""
        self.jour, self.k, self.h = j, k, hashlib.sha256()
        self.fd = os.open(os.path.join(self.dossier, nom(self.prefixe, j, k)), os.O_WRONLY | os.O_APPEND | os.O_CREAT |
                          os.O_EXCL, 0o644)
        return self._ecrire({**champs, "type": genre, "jour": j, "suivante": self.suivante})

    def _ecrire(self, enr):
        octets = canonique({**enr, "seq": self.seq + 1, "prec": self.prec})
        _tout(self.fd, octets)
        self.h.update(octets)
        self.seq, self.prec = self.seq + 1, hashlib.sha256(octets).hexdigest()
        return self.seq, self.prec
