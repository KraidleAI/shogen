"""Acquisition des historiques (PROPOSITION §6.1 CA-1, CA-2 ; E-CA-13, E-CA-14) : étape réseau du lancement,
séparée du calcul. Fichiers écrits sous <bruts>/<fenêtre>/<place>/<actif>/ en .partiel puis renommés ; manifeste
<bruts>/manifeste.tsv (étiquette, puis URL, date, taille, sha256, chemin relatif) tenu ligne à ligne ; un fichier déjà
au manifeste, présent et de même sha256, n'est pas relu (reprise). Aucun octet d'historique n'entre au dépôt."""
from __future__ import annotations

import datetime
import hashlib
import http.client
import os
import time
import urllib.request

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


def lire_url(prm: dict, url: str, plage=None) -> bytes:
    """Corps de la réponse à GET url (plage d'octets (a, b) éventuelle, réponse 206 exigée) ; essais et pauses de
    parametres.json ; échec persistant : CA/acquisition, nommé par le type de l'erreur, jamais par l'URL."""
    r, entetes = prm["reseau"], {"User-Agent": prm["reseau"]["agent"]}
    if plage:
        entetes["Range"] = f"bytes={plage[0]}-{plage[1]}"
    for essai in range(r["essais"]):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=entetes), timeout=r["delai_s"]) as rep:
                if plage and rep.status != 206:
                    raise OSError("plage d'octets non servie")
                return rep.read()
        except (OSError, http.client.HTTPException) as e:
            erreur = type(e).__name__
            if essai + 1 < r["essais"]:
                DORMIR(r["pause_s"])
    raise socle.Refus("CA/acquisition", f"téléchargement impossible ({erreur})")
