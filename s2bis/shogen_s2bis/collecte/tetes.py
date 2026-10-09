"""Têtes de chaîne et jeton RFC 3161 quotidien (CB-15 ; E-C-35, E-C-36 ; ADR-0029 §2.8 l.218, §2.9 l.240 ; AVIS du G0,
Q-D-03 : chaque observateur horodate chaque jour sa propre tête, et celles des autres quand elles sont lisibles).
CB-15a : requête d'horodatage (TimeStampReq, RFC 3161 §2.4.1) en DER, construite en bibliothèque standard : version 1,
empreinte SHA-256 (algorithme avec paramètres NULL, octets d'OpenSSL 3.0.13), nonce s'il est donné, certificat de la TSA
demandé (certReq), ni politique ni extension ; statut d'une réponse (TimeStampResp, §2.4.2) ; manifeste des têtes, ligne
JSON canonique du journal (FORMAT §1.2), dont le sha256 est l'empreinte horodatée. CB-15b : dépôt des têtes (un dossier,
lisible ou non) ; à chaque point de contrôle, la tête du journal y est exportée par écriture atomique ; les fichiers de
tête des autres journaux y sont lus, strictement, bornés en nombre et en taille, pour l'enregistrement `tetes`. Ni
l'export ni la lecture ne lèvent : le dépôt ne casse jamais la boucle, et aucune valeur lue n'est un entier que
l'écrivain refuserait (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1). CB-15d : jeton du jour : manifeste des têtes du dépôt, les
siennes lues d'abord, hors de la borne des autres (C-2), et requête (nonce donné par l'appelant), écrits au dépôt ;
envoi par la fonction que donne l'appelant, seulement s'il en donne une (E-C-36) ; réponse accordée liée à la requête
(TSTInfo : algorithme, empreinte, nonce ; RFC 3161 §2.2 ; C-1), puis conservée en `.tsr` ; la signature et le certificat
de la TSA se contrôlent hors ligne (`openssl ts -verify`, comme `scripts/sceau/verify.sh`)."""
import hashlib
import json
import os
import re

from shogen_s2bis.collecte import journal

SHA256 = bytes.fromhex("0609608648016503040201")          # OBJECT IDENTIFIER 2.16.840.1.101.3.4.2.1 (sha256)
SEQUENCE, INTEGER, BOOLEEN, OCTETS, NUL = 0x30, 0x02, 0x01, 0x04, 0x05
NOM = re.compile("([a-z0-9]{1,16})-([a-z]{1,16})[.]tete")   # <observateur>-<journal>.tete
CLES, TAILLE, NOMBRE = {"journal", "observateur", "seq", "sha256", "ws"}, 1024, 16   # octets, têtes lues au plus
BORNES = {"seq": 10 ** 18, "ws": 10 ** 12}                  # entiers d'une tête lue : 0 ≤ v < borne
SIGNE, TST = bytes.fromhex("2a864886f70d010702"), bytes.fromhex("2a864886f70d0109100104")   # contenus d'OID (G1)


class RefusJeton(ValueError):
    """Refus nommé (`code`) : JETON/empreinte, JETON/nonce, JETON/reponse, JETON/tete, JETON/rejet, JETON/liaison."""
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def _der(etiquette, contenu):
    """Élément DER : étiquette, longueur en forme courte sous 128 octets, longue au-delà (octets minimaux)."""
    n = len(contenu)
    longueur = bytes([n]) if n < 128 else bytes([0x80 | (k := (n.bit_length() + 7) // 8)]) + n.to_bytes(k, "big")
    return bytes([etiquette, *longueur]) + contenu


def _entier(n):
    """INTEGER DER d'un entier positif ou nul : complément à deux, octets minimaux (un zéro de tête si le bit fort)."""
    return _der(INTEGER, n.to_bytes(n.bit_length() // 8 + 1, "big"))


def requete(empreinte, nonce=None):
    """Octets DER de la requête pour `empreinte` (sha256, 32 octets) ; `nonce` : entier de 0 à 2^64 − 1, ou None."""
    if type(empreinte) is not bytes or len(empreinte) != 32:
        raise RefusJeton("JETON/empreinte", repr(empreinte)[:80])
    if nonce is not None and (type(nonce) is not int or not 0 <= nonce < 1 << 64):
        raise RefusJeton("JETON/nonce", repr(nonce)[:80])
    imprint = _der(SEQUENCE, _der(SEQUENCE, SHA256 + _der(NUL, b"")) + _der(OCTETS, empreinte))
    return _der(SEQUENCE, _entier(1) + imprint + (b"" if nonce is None else _entier(nonce)) + _der(BOOLEEN, b"\xff"))


def _element(octets, i, fin):
    """(étiquette, début du contenu, fin) de l'élément DER en `i`, qui doit finir avant `fin` ; longueur en forme
    longue de 1 à 4 octets, minimale (au moins 128, sans zéro de tête) ; sinon JETON/reponse."""
    if i + 2 > fin:
        raise RefusJeton("JETON/reponse", f"élément tronqué en {i}")
    etiquette, n, j = octets[i], octets[i + 1], i + 2
    if n & 0x80:
        k, j = n & 0x7F, j + (n & 0x7F)
        n = int.from_bytes(octets[i + 2:j], "big")
        if not 1 <= k <= 4 or j > fin or octets[i + 2] == 0 or n < 128:
            raise RefusJeton("JETON/reponse", f"longueur illisible en {i}")
    if j + n > fin:
        raise RefusJeton("JETON/reponse", f"élément en {i} au-delà de la réponse")
    return etiquette, j, j + n


def statut(tsr):
    """PKIStatus (0 accordé, 1 accordé avec modifications, 2 rejet, 3 attente, 4 et 5 révocation) d'une réponse : une
    SEQUENCE qui couvre les octets, dont le premier élément, une SEQUENCE, commence par un INTEGER d'un octet ; le
    jeton, une SEQUENCE qui finit la réponse, est présent si et seulement si le statut vaut 0 ou 1 (§2.4.2)."""
    etiquette, debut, fin = _element(tsr, 0, len(tsr))
    if etiquette != SEQUENCE or fin != len(tsr):
        raise RefusJeton("JETON/reponse", "réponse hors SEQUENCE ou octets en trop")
    etiquette, d, f = _element(tsr, debut, fin)
    if etiquette != SEQUENCE:
        raise RefusJeton("JETON/reponse", "PKIStatusInfo hors SEQUENCE")
    etiquette, ds, fs = _element(tsr, d, f)
    s = tsr[ds] if etiquette == INTEGER and fs - ds == 1 else -1
    if s not in range(6) or (f < fin) != (s in (0, 1)) or f < fin and _element(tsr, f, fin)[::2] != (SEQUENCE, fin):
        raise RefusJeton("JETON/reponse", f"statut {s}, jeton {'présent' if f < fin else 'absent'}")
    return s


def _sous(o, x, etiquette):
    """Éléments qui couvrent le contenu de l'élément `x` (étiquette, début, fin), d'étiquette `etiquette` ; sinon
    JETON/reponse."""
    if x[0] != etiquette:
        raise RefusJeton("JETON/reponse", f"étiquette {x[0]:#04x} en {x[1]}, {etiquette:#04x} attendue")
    r, i = [], x[1]
    while i < x[2]:
        r.append(_element(o, i, x[2]))
        i = r[-1][2]
    return r


def lier(tsr, empreinte, nonce):
    """Liaison d'une réponse accordée à la requête (RFC 3161 §2.2 ; §2.4.1, §2.4.2) : jeton ContentInfo id-signedData,
    SignedData, eContent id-ct-TSTInfo ; au TSTInfo, algorithme SHA-256 (paramètres NULL), empreinte `empreinte`,
    nonce `nonce` (absent si None). Chemin DER illisible : JETON/reponse ; écart : JETON/liaison. La signature et le
    certificat de la TSA se contrôlent hors ligne (`openssl ts -verify`)."""
    try:
        ci = _sous(tsr, _sous(tsr, _element(tsr, 0, len(tsr)), SEQUENCE)[1], SEQUENCE)
        eci = _sous(tsr, _sous(tsr, _sous(tsr, ci[1], 0xA0)[0], SEQUENCE)[2], SEQUENCE)
        tst = _sous(tsr, _sous(tsr, _sous(tsr, eci[1], 0xA0)[0], OCTETS)[0], SEQUENCE)
        alg, h = _sous(tsr, tst[2], SEQUENCE)
    except (IndexError, ValueError):
        raise RefusJeton("JETON/reponse", "jeton incomplet") from None
    v = lambda x: (x[0], tsr[x[1]:x[2]])                     # étiquette et contenu d'un élément
    if (v(ci[0]), v(eci[0])) != ((6, SIGNE), (6, TST)):
        raise RefusJeton("JETON/reponse", "jeton hors SignedData ou hors TSTInfo")
    for champ, ecart in (("algorithme", v(alg) != (SEQUENCE, SHA256 + _der(NUL, b""))),
                         ("empreinte", v(h) != (OCTETS, empreinte)),
                         ("nonce", [v(x) for x in tst[5:] if x[0] == INTEGER] != (
                             [] if nonce is None else [(INTEGER, _entier(nonce)[2:])]))):
        if ecart:
            raise RefusJeton("JETON/liaison", f"{champ} du TSTInfo autre que celui de la requête")


def manifeste(jour, observateur, tetes):
    """Octets du manifeste du jour `jour` de `observateur` : {jour, observateur, tetes}, têtes triées par observateur
    puis journal, en ligne canonique du journal (refus JOURNAL/… d'une valeur hors JSON exact)."""
    rangees = sorted(tetes, key=lambda t: (t["observateur"], t["journal"]))
    return journal.canonique({"jour": jour, "observateur": observateur, "tetes": rangees})


def ecrire(dossier, nom, octets, fsync=os.fsync):
    """Écriture atomique de `nom` : fichier temporaire « .<nom>.tmp » écrit et synchronisé, renommé, dossier
    synchronisé ; un lecteur voit l'ancien fichier ou le nouveau, jamais un fichier partiel."""
    tmp = os.path.join(dossier, f".{nom}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        journal._tout(fd, octets)
        fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, os.path.join(dossier, nom))
    fd = os.open(dossier, os.O_RDONLY)
    try:
        fsync(fd)
    finally:
        os.close(fd)


def _lire_tete(chemin, observateur, nom_journal):
    """(tête, None) ou (None, code) : au plus TAILLE octets, ligne canonique aux clés exactes, observateur et journal
    du nom du fichier, `seq` et `ws` entiers sous leurs bornes, `sha256` de 64 chiffres hexadécimaux minuscules."""
    try:
        with open(chemin, "rb") as f:
            octets = f.read(TAILLE + 1)
    except OSError:
        return None, "TETES/lecture"
    if len(octets) > TAILLE:
        return None, "TETES/taille"
    try:
        t = json.loads(octets)
        forme = type(t) is dict and set(t) == CLES and journal.canonique(t) == octets
    except (ValueError, RecursionError, journal.ErreurJournal):
        forme = False
    if not forme:
        return None, "TETES/forme"
    if (t["observateur"], t["journal"]) != (observateur, nom_journal) or not all(
            type(t[k]) is int and 0 <= t[k] < b for k, b in BORNES.items()) or not (
            type(t["sha256"]) is str and journal.HEX.fullmatch(t["sha256"])):
        return None, "TETES/champs"
    return t, None


class Depot:
    """Dépôt des têtes vu par le journal `nom_journal` de `observateur` (AVIS Q-D-03)."""
    def __init__(self, dossier, observateur, nom_journal="pool", fsync=os.fsync):
        self.dossier, self.observateur, self.journal, self.fsync, self.echec = (dossier, observateur, nom_journal,
                                                                               fsync, None)

    def exporter(self, ws, tete):
        """Tête (seq, sha256) du point de contrôle de la fenêtre `ws`, au fichier `<observateur>-<journal>.tete` ;
        un échec est noté (nom de l'exception) pour l'enregistrement `tetes` suivant, jamais levé."""
        t = {"journal": self.journal, "observateur": self.observateur, "seq": tete[0], "sha256": tete[1], "ws": ws}
        try:
            ecrire(self.dossier, f"{self.observateur}-{self.journal}.tete", journal.canonique(t), self.fsync)
            self.echec = None
        except Exception as e:                                      # attrape-tout : le dépôt ne casse pas la boucle
            self.echec = type(e).__name__

    def lire(self):
        """Champs de l'enregistrement `tetes` : `tetes`, `refus`, `ignores` de `lire_tetes`, sauf le fichier de ce
        journal, les têtes de l'observateur d'abord (C-2) ; `export`, échec du dernier export, ou null."""
        r = {"tetes": [], "refus": [], "ignores": 0, "export": self.echec}
        try:
            r["tetes"], r["refus"], r["ignores"] = lire_tetes(self.dossier, (self.observateur, self.journal),
                                                               self.observateur)
        except Exception:                                           # attrape-tout : dossier absent ou illisible
            r["refus"].append([".", "TETES/depot"])
        return r


def lire_tetes(dossier, exclure=None, propre=None):
    """(têtes valides, refus [nom, code], fichiers au-delà des bornes) des fichiers de tête de `dossier`, sauf celui de
    `exclure` (observateur, journal), dans l'ordre des noms : ceux de l'observateur `propre` d'abord, hors de la borne
    des autres (C-2 ; AVIS Q-D-03 (1) : sa tête est ancrée quoi qu'il arrive au dépôt), NOMBRE au plus de chaque
    sorte ; dossier illisible : OSError."""
    noms = [(n, m) for n in sorted(os.listdir(dossier)) if (m := NOM.fullmatch(n)) and m.groups() != exclure]
    siens, autres = [x for x in noms if x[1][1] == propre], [x for x in noms if x[1][1] != propre]
    tetes, refus = [], []
    for n, m in siens[:NOMBRE] + autres[:NOMBRE]:
        t, code = _lire_tete(os.path.join(dossier, n), *m.groups())
        tetes.append(t) if t else refus.append([n, code])
    return tetes, refus, max(0, len(siens) - NOMBRE) + max(0, len(autres) - NOMBRE)


def jeton(dossier, observateur, jour, nonce, envoyer=None, fsync=os.fsync):
    """Jeton du jour (AVIS Q-D-03, point 1) ; rend (état, fichier, sha256 de ses octets). Un `.tsr` du jour présent :
    « déjà émis », rien n'est redemandé. Sinon manifeste des têtes valides du dépôt, les siennes d'abord (JETON/tete
    sans tête de l'observateur) et requête au `nonce`, écrits au dépôt ; sans `envoyer`, « non armé » ; armé,
    `envoyer(requête)` rend la réponse : conservée si son statut vaut 0 ou 1 et qu'elle est liée à la requête
    (`lier`) (« émis ») ; sinon JETON/rejet, JETON/reponse ou JETON/liaison, rien de conservé."""
    nom = os.path.join(dossier, f"{observateur}-{jour}")
    if os.path.exists(nom + ".tsr"):
        return "déjà émis", f"{observateur}-{jour}.tsr", journal._empreinte(nom + ".tsr")[0]
    lues = lire_tetes(dossier, propre=observateur)[0]
    if not any(t["observateur"] == observateur for t in lues):
        raise RefusJeton("JETON/tete", f"aucune tête de {observateur} au dépôt")
    m = manifeste(jour, observateur, lues)
    tsq = requete(emp := hashlib.sha256(m).digest(), nonce)
    for suffixe, octets in ((".manifeste", m), (".tsq", tsq)):
        ecrire(dossier, f"{observateur}-{jour}{suffixe}", octets, fsync)
    if envoyer is None:
        return "non armé", f"{observateur}-{jour}.tsq", hashlib.sha256(tsq).hexdigest()
    tsr = envoyer(tsq)
    if (s := statut(tsr)) not in (0, 1):
        raise RefusJeton("JETON/rejet", f"statut {s}")
    lier(tsr, emp, nonce)                                   # C-1 : un jeton d'une autre requête n'est jamais gardé
    ecrire(dossier, f"{observateur}-{jour}.tsr", tsr, fsync)
    return "émis", f"{observateur}-{jour}.tsr", hashlib.sha256(tsr).hexdigest()
