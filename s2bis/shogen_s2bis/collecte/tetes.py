"""Têtes de chaîne et jeton RFC 3161 quotidien (CB-15 ; E-C-35, E-C-36 ; ADR-0029 §2.8 l.218, §2.9 l.240 ; AVIS du G0,
Q-D-03 : chaque observateur horodate chaque jour sa propre tête, et celles des autres quand elles sont lisibles).
CB-15a : requête d'horodatage (TimeStampReq, RFC 3161 §2.4.1) en DER, construite en bibliothèque standard : version 1,
empreinte SHA-256 (algorithme avec paramètres NULL, octets d'OpenSSL 3.0.13), nonce s'il est donné, certificat de la TSA
demandé (certReq), ni politique ni extension ; statut d'une réponse (TimeStampResp, §2.4.2) ; manifeste des têtes, ligne
JSON canonique du journal (FORMAT §1.2), dont le sha256 est l'empreinte horodatée. CB-15b : dépôt des têtes (un dossier,
lisible ou non) ; à chaque point de contrôle, la tête du journal y est exportée par écriture atomique ; les fichiers de
tête des autres journaux y sont lus, strictement, bornés en nombre et en taille, pour l'enregistrement `tetes`. Ni
l'export ni la lecture ne lèvent : le dépôt ne casse jamais la boucle, et aucune valeur lue n'est un entier que
l'écrivain refuserait (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1)."""
import json
import os
import re

from shogen_s2bis.collecte import journal

SHA256 = bytes.fromhex("0609608648016503040201")          # OBJECT IDENTIFIER 2.16.840.1.101.3.4.2.1 (sha256)
SEQUENCE, INTEGER, BOOLEEN, OCTETS, NUL = 0x30, 0x02, 0x01, 0x04, 0x05
NOM = re.compile("([a-z0-9]{1,16})-([a-z]{1,16})[.]tete")   # <observateur>-<journal>.tete
CLES, TAILLE, NOMBRE = {"journal", "observateur", "seq", "sha256", "ws"}, 1024, 16   # octets, têtes lues au plus
BORNES = {"seq": 10 ** 18, "ws": 10 ** 12}                  # entiers d'une tête lue : 0 ≤ v < borne


class RefusJeton(ValueError):
    """Refus nommé (`code`) : JETON/empreinte, JETON/nonce, JETON/reponse."""
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
        """Champs de l'enregistrement `tetes` : `tetes`, têtes valides des fichiers de tête du dépôt, sauf celui de ce
        journal, NOMBRE au plus dans l'ordre des noms ; `refus`, [nom, code] des autres ; `ignores`, fichiers au-delà
        de NOMBRE ; `export`, échec du dernier export ou null."""
        r = {"tetes": [], "refus": [], "ignores": 0, "export": self.echec}
        try:
            noms = [(n, m) for n in sorted(os.listdir(self.dossier)) if (m := NOM.fullmatch(n)) and
                    m.groups() != (self.observateur, self.journal)]
        except Exception:                                           # attrape-tout : dossier absent ou illisible
            r["refus"].append([".", "TETES/depot"])
            return r
        r["ignores"] = max(0, len(noms) - NOMBRE)
        for n, m in noms[:NOMBRE]:
            t, code = _lire_tete(os.path.join(self.dossier, n), *m.groups())
            r["tetes"].append(t) if t else r["refus"].append([n, code])
        return r
