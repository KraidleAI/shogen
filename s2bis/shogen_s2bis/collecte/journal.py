"""Journal chaîné du collecteur (CB-1 ; E-C-18, E-C-19 ; ADR-0029 §2.9 l.238). Chaque enregistrement est une ligne
JSON canonique (clés triées, séparateurs « , » et « : », UTF-8 sans échappement, saut de ligne final, aucun flottant)
qui porte `seq` (rang depuis 0) et `prec` (sha256 des octets de la ligne précédente, saut de ligne compris ; GENESE
pour la première). Écriture sans tampon ; `fsync` (injectable) au marqueur de fenêtre seulement ; la fenêtre qui clôt
une heure est suivie d'un point de contrôle `point`, dont l'empreinte est la tête exportée. Un enregistrement de
fenêtre n'est admis que sur la grille et pour une fenêtre non close (ws ≥ `suivante`). Tout refus est nommé
(ErreurJournal) et n'écrit rien. E-C-16 : un seul écrivain par journal, verrou
exclusif sans attente (`fcntl.flock`) ; une seconde instance lève JournalOccupe avant toute lecture ou écriture.
E-C-20 (CB-2) : un fichier par jour UTC ; le premier enregistrement d'une fenêtre d'un jour nouveau clôt le fichier
(`cloture`, fsync), inscrit son sha256 au fichier de sommes `<préfixe>.sha256` (format de sha256sum, fsync), puis
ouvre le fichier du jour par `ouverture` ; la chaîne continue. E-C-21, E-C-22 (CB-2) : un journal existant reprend
au dernier enregistrement intègre ; une queue non intègre (ligne coupée, octets NUL, ligne de plus de LIMITE octets)
n'est jamais réécrite : un segment neuf s'ouvre par `reprise`, qui la déclare (fichier, position, octets, sha256). La
fenêtre du redémarrage et toute fenêtre close restent refusées ; le marqueur qui suit des fenêtres sans marqueur est
précédé d'un `trou` (cause `arret`, `horloge_reculee` ou `saut`)."""
import fcntl
import hashlib
import json
import os
import re
import time

GENESE = "0" * 64
HEURE = 3600
LIMITE = 1 << 22                                                   # octets d'une ligne au plus, saut de ligne compris
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
    except (TypeError, ValueError, RecursionError) as e:          # RecursionError : imbrication excessive
        raise ErreurJournal("JOURNAL/type", e) from None


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
        motif = re.compile(re.escape(self.prefixe) + r"-([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]+)[.]jsonl")
        fichiers = sorted((x[1], int(x[2]), x[0]) for x in map(motif.fullmatch, os.listdir(self.dossier)) if x)
        if fichiers:
            self._reprendre(ws, fichiers)
        else:
            self.seq, self.prec, self.suivante, self.attendu, self.cause = -1, GENESE, ws + self.w, ws + self.w, "saut"
            self._creer(jour(ws), 0, {"type": "ouverture", "jour": jour(ws), "suivante": self.attendu})
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
        self.suivante, self.attendu, self.cause = ws + self.w, ws + self.w, "saut"
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
            self._creer(jour(ws), 0, {"type": "ouverture", "jour": jour(ws), "suivante": self.attendu})
        if genre == "marqueur" and ws > self.attendu:
            self._ecrire({"type": "trou", "de": self.attendu, "a": ws - self.w, "cause": self.cause})
            self.attendu, self.cause = ws, "saut"
        return self._ecrire({**champs, "type": genre, "ws": ws})

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
        """(position de la queue, état, empreinte du préfixe intègre) du fichier `n`. Intègre : ligne canonique, chaînée
        à la précédente ; la première est une `ouverture` ou une `reprise`. État : celui du dernier intègre, ou None."""
        etat, pos, h = None, 0, hashlib.sha256()
        with open(os.path.join(self.dossier, n), "rb") as f:
            while (ligne := f.readline(LIMITE)).endswith(b"\n"):
                try:
                    e = json.loads(ligne)
                    t = e["type"]
                    if etat:
                        lien = (e["seq"], e["prec"]) == (etat["seq"] + 1, etat["prec"])
                    else:
                        lien = t in ("ouverture", "reprise") and type(e["seq"]) is int
                    if t in ("ouverture", "reprise"):
                        attendu = e["suivante"]                # première fenêtre ni close ni déclarée en trou
                    elif t in ("marqueur", "trou"):
                        attendu = e["ws" if t == "marqueur" else "a"] + self.w
                    else:
                        attendu = etat["attendu"]
                    intact = lien and type(attendu) is int and canonique(e) == ligne
                except (ValueError, KeyError, TypeError, RecursionError, ErreurJournal):
                    intact = False
                if not intact:
                    break
                etat = {"seq": e["seq"], "prec": hashlib.sha256(ligne).hexdigest(), "type": t, "attendu": attendu}
                h.update(ligne)
                pos += len(ligne)
        return pos, etat, h

    def _reprendre(self, ws, fichiers):
        """Reprise au dernier intègre ; queues déclarées, fichiers achevés sommés ; segment neuf si queue, fichier clos
        ou jour passé (clos ici)."""
        queues = []
        for j, k, n in reversed(fichiers):
            pos, etat, h = self._lire(n)
            q, taille = _empreinte(os.path.join(self.dossier, n), pos)
            if taille:
                queues.insert(0, {"fichier": n, "position": pos, "octets": taille, "sha256": q})
            if etat:
                break
        else:
            raise ErreurJournal("JOURNAL/illisible", "aucun enregistrement intègre")
        self.seq, self.prec, self.attendu = etat["seq"], etat["prec"], etat["attendu"]
        self.jour, self.k, self.h = j, k, h
        self.suivante = max(self.attendu, ws + self.w)
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
                os.close(self.fd)
            self._sommes([x for _j, _k, x in fichiers])
            jn = max(jour(ws), j)
            self._creer(jn, 1 + max([kk for jj, kk, _x in fichiers if jj == jn], default=-1), reprise)
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
        octets = canonique({**enr, "seq": self.seq + 1, "prec": self.prec})
        if len(octets) > LIMITE:
            raise ErreurJournal("JOURNAL/taille", len(octets))
        _tout(self.fd, octets)
        self.h.update(octets)
        self.seq, self.prec = self.seq + 1, hashlib.sha256(octets).hexdigest()
        return self.seq, self.prec
