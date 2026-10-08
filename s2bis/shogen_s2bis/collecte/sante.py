"""Sondes de santé par fenêtre (CB-11 ; E-C-25 à E-C-29 ; ADR-0029 §2.3, §2.9 l.237). Elles partent au départ des
lectures (ws + w − δ, Q-C-03), chacune sur son fil démon, hors du pool des lectures ; la boucle les joint avant
l'échéance. D-3 : sortie brute de la commande d'horloge scellée, sans analyse ici (son format n'est pas supposé : le
recalcul l'analyse, sur pièce) ; D-4 : SOA de « . » vers chaque témoin, adresse IPv4 littérale, sans récursion ; D-5 :
A de chaque nom témoin, par le résolveur de l'observateur ; délai de 2 s (l.109-110). S'y ajoutent, au relevé, le
disque du journal et l'empreinte de la configuration du résolveur. Valeurs brutes, aucun jugement (E-C-26). Une sonde
dont l'instance précédente n'a pas rendu n'est pas relancée : au plus un fil par sonde (C-5 de la G2 de P1-B).
CB-18b (SHOGEN-S2BIS-SONDES-ECHEANCE-1) : chaque sonde rend aussi l'instant de sa fin sur l'horloge monotone de la
boucle (jamais journalisé) ; au relevé, une sonde finie après l'échéance vaut null, et disque et empreinte ne se
relèvent qu'après l'état des futurs."""
import concurrent.futures
import hashlib
import os
import subprocess
import threading

from shogen_s2bis.collecte import dns
from shogen_s2bis.collecte.lecture import S, horloge, monotone

SORTIE = 4096                                                       # caractères gardés de la sortie D-3


def horloge_systeme(commande, delai=2 * S, lancer=subprocess.run, horloge=horloge):
    """D-3 : {sortie, code} de la commande, ou {erreur : absente, delai, autre} ; instants de début et de fin."""
    debut = horloge()
    try:
        p = lancer(commande, capture_output=True, timeout=delai / S)
        r = {"sortie": p.stdout.decode("utf-8", "replace")[:SORTIE], "code": p.returncode}
    except FileNotFoundError:
        r = {"erreur": "absente"}
    except subprocess.TimeoutExpired:
        r = {"erreur": "delai"}
    except Exception:                                               # attrape-tout : une sonde ne lève jamais
        r = {"erreur": "autre"}
    return {**r, "debut": debut, "fin": horloge()}


def disque(dossier):
    """Octets du système de fichiers du journal : total, et libres pour un utilisateur ordinaire (statvfs)."""
    try:
        v = os.statvfs(dossier)
        return {"total": v.f_blocks * v.f_frsize, "libre": v.f_bavail * v.f_frsize}
    except OSError as e:
        return {"erreur": type(e).__name__}


def empreinte(chemin):
    """sha256 des octets de la configuration du résolveur ; None si elle ne se lit pas."""
    try:
        with open(chemin, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


class Sondes:
    def __init__(self, commande, temoins, noms, resolveur, dossier, resolv="/etc/resolv.conf", delai=2 * S,
                 interroger=dns.interroger, lancer=subprocess.run):
        self.commande, self.temoins, self.noms, self.resolveur = commande, temoins, noms, resolveur
        self.dossier, self.resolv, self.delai = dossier, resolv, delai
        self.interroger, self.lanceur, self.encours = interroger, lancer, {}           # rang → dernier futur (C-5)

    def lancer(self, monotone=monotone):
        """Lance chaque sonde sur un fil démon ; rend [(clé, futur)] dans l'ordre : d3, témoins, noms. Une sonde dont
        l'instance précédente n'a pas rendu n'est pas relancée : futur None, elle vaut null (C-5). Le futur rend
        (valeur, fin sur l'horloge `monotone`, celle de la boucle) (CB-18b)."""
        taches = [("d3", lambda: horloge_systeme(self.commande, self.delai, self.lanceur))]
        taches += [("d4", lambda a=a: {"adresse": a, **self.interroger(a, ".", "SOA", recursion=False,
                                                                       delai=self.delai)}) for a in self.temoins]
        taches += [("d5", lambda n=n: {"nom": n, **self.interroger(self.resolveur, n, "A", recursion=True,
                                                                   delai=self.delai)}) for n in self.noms]
        lancees = []
        for rang, (cle, tache) in enumerate(taches):
            if rang in self.encours and not self.encours[rang].done():
                lancees.append((cle, None))
                continue
            futur = self.encours[rang] = concurrent.futures.Future()
            threading.Thread(target=_sonder, args=(tache, futur, monotone), daemon=True).start()
            lancees.append((cle, futur))
        return lancees

    def vivantes(self):
        """Instances de sonde encore en cours (C-5) : au plus une par sonde."""
        return sum(not f.done() for f in self.encours.values())

    def joindre(self, lancees, limite=None):
        """Champs de santé des sondes ; une sonde inachevée, non relancée, ou finie après `limite` (échéance sur
        l'horloge monotone de `lancer`, CB-18b) vaut None. Disque et résolveur se relèvent après l'état des futurs."""
        etats = [(cle, futur.result() if futur is not None and futur.done() else (None, 0)) for cle, futur in lancees]
        r = {"d3": None, "d4": [], "d5": [], "disque": disque(self.dossier), "resolveur": empreinte(self.resolv)}
        for cle, (v, fin) in etats:
            v = None if limite is not None and fin > limite else v
            if cle == "d3":
                r["d3"] = v
            else:
                r[cle].append(v)
        return r


def _sonder(tache, futur, monotone):
    """Fil d'une sonde. Le futur rend toujours (valeur, fin sur l'horloge `monotone`) : une sonde qui lève vaut None et
    repart à la fenêtre suivante (C-5) ; une BaseException suit son cours."""
    v = None
    try:
        v = tache()
    except Exception:                                               # attrape-tout : une sonde ne lève jamais
        pass
    finally:
        futur.set_result((v, monotone()))
