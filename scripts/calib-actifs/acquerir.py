"""Acquisition des historiques (PROPOSITION §6.1 CA-1, CA-2 ; E-CA-13, E-CA-14) : étape réseau du lancement,
séparée du calcul. Fichiers écrits sous <bruts>/<fenêtre>/<place>/<actif>/ en .partiel puis renommés ; manifeste
<bruts>/manifeste.tsv (étiquette, puis URL, date, taille, sha256, chemin relatif) tenu ligne à ligne ; un fichier déjà
au manifeste, présent et de même sha256, n'est pas relu (reprise). Aucun octet d'historique n'entre au dépôt."""
from __future__ import annotations

import datetime
import hashlib
import http.client
import io
import os
import sys
import time
import urllib.request
import zipfile

import socle

NL, TAB = chr(10), chr(9)
DORMIR, HORLOGE = time.sleep, time.monotonic        # remplaçables par les tests (débit, pauses)


class Manifeste:
    """Manifeste de l'acquisition : lignes déjà écrites relues (reprise), puis ajout ligne à ligne."""

    def __init__(self, bruts: str):
        self.bruts, self.chemin, self.vus = bruts, os.path.join(bruts, "manifeste.tsv"), {}
        if os.path.exists(self.chemin):
            with open(self.chemin, encoding="utf-8") as f:
                lignes = f.read().split(NL)
            if lignes[0] != socle.ETIQUETTE:
                raise socle.Refus("CA/acquisition", "manifeste existant sans l'étiquette du lot")
            for x in filter(None, lignes[1:]):
                _u, _d, _t, sha, rel = x.split(TAB)
                self.vus[rel] = sha
        else:
            os.makedirs(bruts, exist_ok=True)
            with open(self.chemin, "w", encoding="utf-8") as f:
                f.write(socle.ETIQUETTE + NL)

    def present(self, rel: str) -> bool:
        p = os.path.join(self.bruts, rel)
        return rel in self.vus and os.path.isfile(p) and socle.empreinte(p) == self.vus[rel]

    def ajouter(self, url: str, rel: str, octets: bytes) -> None:
        p = os.path.join(self.bruts, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p + ".partiel", "wb") as f:
            f.write(octets)
        os.replace(p + ".partiel", p)
        sha = hashlib.sha256(octets).hexdigest()
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(self.chemin, "a", encoding="utf-8") as f:
            f.write(TAB.join([url, date, str(len(octets)), sha, rel]) + NL)
        self.vus[rel] = sha


def lire_url(prm: dict, url: str, plage=None, total=False):
    """Corps de la réponse à GET url (plage d'octets (a, b) éventuelle, réponse 206 exigée ; total : (corps, taille
    du fichier lue dans Content-Range)) ; essais et pauses de parametres.json ; échec persistant : CA/acquisition,
    nommé par le type de l'erreur, jamais par l'URL."""
    r, entetes = prm["reseau"], {"User-Agent": prm["reseau"]["agent"]}
    if plage:
        entetes["Range"] = f"bytes={plage[0]}-{plage[1]}"
    for essai in range(r["essais"]):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=entetes), timeout=r["delai_s"]) as rep:
                if plage and rep.status != 206:
                    raise OSError("plage d'octets non servie")
                corps = rep.read()
                return (corps, int((rep.headers.get("Content-Range") or "/").rsplit("/", 1)[1])) if total else corps
        except (OSError, ValueError, http.client.HTTPException) as e:
            erreur = type(e).__name__
            if essai + 1 < r["essais"]:
                DORMIR(r["pause_s"])
    raise socle.Refus("CA/acquisition", f"téléchargement impossible ({erreur})")


def mois(fen: dict, voisins: int = 0) -> list:
    """Mois (AAAA-MM) couverts par la fenêtre [debut ; fin), dans l'ordre, et `voisins` mois de chaque côté (OKX :
    alignement des mensuels en UTC ou UTC+8 non écrit, DECISION de FORMES-API-1 pt 4) ; rang du mois borné."""
    return [f"{k // 12:04d}-{k % 12 + 1:02d}" for k in socle.rangs_mois(fen, voisins)]


def mensuels(prm: dict, man: Manifeste, nom: str, fen: dict, place: str, actif: str) -> None:
    """Fichiers mensuels d'une (place, actif) : Binance avec son .CHECKSUM (sha256 différent : CA/acquisition, E-CA-13),
    OKX sans somme publiée ; mois voisins de parametres.json (minutes hors fenêtre écartées au chargement)."""
    s = prm["series"][place]
    for m in mois(fen, s["voisins"]):
        url = s["url"].format(s=s["paires"][actif], m=m, mm=m.replace("-", ""))
        rel = os.path.join(nom, place, actif, url.rsplit("/", 1)[1])
        if man.present(rel):
            continue
        try:                                                        # C-2 de la G2 : refus nommé par le mois
            octets = lire_url(prm, url)
            somme = lire_url(prm, url + ".CHECKSUM") if s["acces"] == "mensuel_checksum" else None
        except socle.Refus as r:
            raise socle.Refus("CA/acquisition", f"mensuel {m} non obtenu ({str(r).split(' : ', 1)[1]}) ; un mensuel "
                              "n'est publié qu'après la fin de son mois", actif, place=place) from None
        if somme is not None and somme.decode("ascii", "replace").split(" ")[0] != hashlib.sha256(octets).hexdigest():
            raise socle.Refus("CA/acquisition", "sha256 différent du .CHECKSUM publié", actif, place=place)
        man.ajouter(url, rel, octets)


class Plages(io.RawIOBase):
    """Fichier distant lu par plages d'octets (Range, 206 exigée), pour zipfile : seuls le répertoire central et les
    membres demandés de l'archive de Kraken sont transférés (E-CA-13 ; SOURCES-HISTORIQUES §3.1)."""

    def __init__(self, prm: dict, url: str):
        super().__init__()
        self.prm, self.url, self.pos = prm, url, 0
        self.taille = lire_url(prm, url, (0, 0), total=True)[1]

    def readable(self):
        return True

    def seekable(self):
        return True

    def seek(self, n, depuis=0):
        self.pos = (n, self.pos + n, self.taille + n)[depuis]
        return self.pos

    def readinto(self, b):
        n = min(len(b), self.taille - self.pos)
        octets = lire_url(self.prm, self.url, (self.pos, self.pos + n - 1)) if n > 0 else b""
        if len(octets) != max(n, 0):
            raise OSError("plage incomplète")
        b[:len(octets)] = octets
        self.pos += len(octets)
        return len(octets)


def kraken(prm: dict, man: Manifeste, nom: str, actif: str) -> None:
    """CSV d'une paire, membre de l'archive trimestrielle lue par plages ; sha256 différent de SOURCES-HISTORIQUES
    l.156-158 : CA/kraken (E-CA-14) ; membre absent ou répété, archive illisible : CA/kraken."""
    s, rel = prm["series"]["kraken"], os.path.join(nom, "kraken", actif, prm["series"]["kraken"]["paires"][actif])
    if man.present(rel):
        return
    try:
        with zipfile.ZipFile(io.BufferedReader(Plages(prm, s["url"]), 1 << 20)) as z:
            noms = [x for x in z.namelist() if x.rsplit("/", 1)[-1] == s["paires"][actif]]
            octets = z.read(noms[0]) if len(noms) == 1 else b""
    except (zipfile.BadZipFile, OSError, EOFError) as e:
        raise socle.Refus("CA/kraken", f"archive illisible ({type(e).__name__})", actif, place="kraken") from None
    if hashlib.sha256(octets).hexdigest() != prm["kraken_sha256"][actif]:
        raise socle.Refus("CA/kraken", "CSV absent ou de sha256 différent de SH l.156-158", actif, place="kraken")
    man.ajouter(s["url"] + "#" + s["paires"][actif], rel, octets)


class Debit:
    """Débit borné par place (E-CA-13 ; SOURCES-HISTORIQUES §3 : Coinbase 3 requêtes par seconde au plus, Bitfinex 30
    par minute au plus) : au moins intervalle_ms entre deux requêtes d'une même place."""

    def __init__(self):
        self.dernier = {}

    def attendre(self, place: str, intervalle_ms: int) -> None:
        d = self.dernier.get(place)
        if d is not None and (HORLOGE() - d) * 1000 < intervalle_ms:
            DORMIR(intervalle_ms / 1000 - (HORLOGE() - d))
        self.dernier[place] = HORLOGE()


def iso(t: int) -> str:
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pages(prm: dict, man: Manifeste, nom: str, fen: dict, place: str, actif: str, debit: Debit) -> None:
    """API paginée d'une (place, actif) : découpage de socle.pages (requête de départ à borne, `pas` bougies au plus,
    chevauchement de chaque côté ; la première et la dernière peuvent demander une minute hors fenêtre, écartée au
    chargement) ; une page par fichier page-<début>.json ; reprise sur le manifeste."""
    s = prm["series"][place]
    for debut, _f, depart, fin in socle.pages(prm, place, fen):
        rel = os.path.join(nom, place, actif, f"page-{debut}.json")
        if man.present(rel):
            continue
        url = s["url"].format(s=s["paires"][actif], debut=depart, fin=fin, n=(fin - depart) // 60 + 1,
                              debut_ms=depart * 1000, fin_ms=fin * 1000, debut_iso=iso(depart), fin_iso=iso(fin))
        debit.attendre(place, s["intervalle_ms"])
        man.ajouter(url, rel, lire_url(prm, url))


def main(argv=None, env=None) -> int:
    """python3 acquerir.py --bruts <dossier> [--parametres <fichier>] : chaque (fenêtre, actif, place) de la lecture
    retenue, fenêtre descriptive sans ses places exclues. Codes : 0 ; 3 variable posée ; 4 acquisition impossible ou
    refus (CA/acquisition, CA/kraken), nommé sur stderr ; 2 usage."""
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) not in (2, 4) or a[0] != "--bruts" or (len(a) == 4 and a[2] != "--parametres"):
        print("REFUS CA/usage : acquerir.py --bruts <dossier> [--parametres <fichier>]", file=sys.stderr)
        return 2
    try:
        socle.garde(os.environ if env is None else env)
        prm = socle.lire(a[3] if len(a) == 4 else socle.PARAMETRES)
        man, debit, lec = Manifeste(a[1]), Debit(), socle.lecture(prm)
        for nom, fen in (("principale", prm["fenetre"]), ("descriptive", prm["fenetre_descriptive"])):
            for actif in socle.ACTIFS:
                for place in (x for x in lec["places"][actif] if nom == "principale" or x not in fen["sans"]):
                    acces = prm["series"][place]["acces"]
                    if acces == "pages":
                        pages(prm, man, nom, fen, place, actif, debit)
                    elif acces == "archive":
                        kraken(prm, man, nom, actif)
                    else:
                        mensuels(prm, man, nom, fen, place, actif)
    except socle.Refus as r:
        print(r, file=sys.stderr)
        return 3 if r.code in ("CA/variable", "CA/parametres") else 4
    except Exception as e:                                          # jamais une trace : refus nommé par le type
        print(socle.Refus("CA/acquisition", f"acquisition en échec ({type(e).__name__})"), file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
