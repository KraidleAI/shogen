"""Lecture typée (CB-3 ; E-C-03, E-C-04, E-C-17 ; ADR-0029 §2.9 l.233, l.236, l.238). Statut lisible par
`r1.classify_ecart` de S2 ; `panne_transport`, et lui seul, porte un sous-type. Instants entiers en microsecondes depuis
l'époque Unix (UTC ; moins de 2^53, exacts pour tout lecteur JSON) : départ, fin, fin de chaque phase atteinte. Les
délais se comptent sur l'horloge monotone, jamais journalisée (C-4 de la G2 de P1-B).
Adresse contactée ; octets du corps, au journal en base64 avec leur sha256 ; valeurs décodées (CB-6 et suivants)."""
import base64
import hashlib
import time

S = 1_000_000                                                       # microsecondes par seconde
STATUTS = ("ok", "panne_http", "panne_transport", "panne_decode")
SOUS_TYPES = ("dns", "connexion", "tls", "delai", "coupure", "autre")


def horloge():
    """Instant présent, en microsecondes entières depuis l'époque Unix (UTC)."""
    return time.time_ns() // 1000


def monotone():
    """Instant de l'horloge monotone, en microsecondes entières : délais seulement, jamais journalisé (C-4)."""
    return time.monotonic_ns() // 1000


class Lecture:
    __slots__ = ("statut", "sous_type", "code", "depart", "fin", "phases", "adresse", "octets", "valeurs")

    def __init__(self, statut, depart, fin, phases=None, adresse=None, sous_type=None, code=None, octets=b"",
                 valeurs=None):
        if statut not in STATUTS or (sous_type not in SOUS_TYPES if statut == "panne_transport" else
                                     sous_type is not None):
            raise ValueError(f"lecture : statut {statut!r}, sous-type {sous_type!r}")
        self.statut, self.sous_type, self.code, self.depart, self.fin = statut, sous_type, code, depart, fin
        self.phases, self.adresse, self.octets, self.valeurs = dict(phases or {}), adresse, bytes(octets), valeurs

    def enregistrement(self):
        """Champs de l'enregistrement `lecture` du journal (la boucle y ajoute la forme et l'instant prévu)."""
        return {"statut": self.statut, "sous_type": self.sous_type, "code": self.code, "depart": self.depart,
                "fin": self.fin, "phases": self.phases, "adresse": self.adresse, "valeurs": self.valeurs,
                "brut": base64.b64encode(self.octets).decode(), "sha256": hashlib.sha256(self.octets).hexdigest()}
