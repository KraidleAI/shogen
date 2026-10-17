"""Smoke sans prix (CB-16 ; E-C-37 ; PROPOSITION l.224, l.278 ; ADR-0029 l.81, l.222 ; FORMAT §14.1) : une lecture de
chaque forme du pool et du témoin (`formes.json`), de chaque forme de la carte (`carte.json`), décodée par le
décodeur de sa forme, puis CryptoCompare, écartée du pool, dont le 401 sans clé est re-confirmé (exclusion vérifiée,
pas postulée : `s2-harness/shogen_s2/smoke.py` l.46-53). Une ligne par lecture : rôle (`pool`, `temoin` pour un
décodeur de la classe `temoin`, `carte`), nom de la forme, hôte, statut, code HTTP, sous-type, latence en
millisecondes, décodable oui ou non. Jamais un prix, une valeur décodée, une fourchette ni un octet du corps : le
rodage interdit toute lecture de prix (ADR-0029 l.222) ; la capture des octets est une autre commande, qui n'imprime
rien (AVIS Q-C-05). Lecture HTTP injectable (`lire`, `pause`) : tests sur fixtures, sans réseau. Lectures en série ;
deux lectures d'un hôte à `espace` vrai sont séparées d'une seconde au moins. Code 0 si et seulement si toutes les
formes du pool et du témoin décodent ; une forme de la carte qui ne décode pas est déclarée sans changer le code
(ADR-0029 l.81 : la source reste hors de la carte que lit l'observateur)."""
import time

from shogen_s2bis.collecte import decodeurs, http

CRYPTOCOMPARE = http.Requete("min-api.cryptocompare.com", "/data/price?fsym=BTC&tsyms=USD", 443, "GET", None)


def role(x):
    """`temoin` pour une forme dont le décodeur est de la classe `temoin` (C-P2D-1), `pool` sinon."""
    return "temoin" if decodeurs.DECODEURS.get(x["decodeur"], (None,) * 4)[2] == "temoin" else "pool"


def ligne(r, nom, hote, lu, decodable):
    """Texte d'une lecture : métadonnées seules, jamais `valeurs` ni `octets`."""
    return " ".join((r, nom, hote, lu.statut, "-" if lu.code is None else str(lu.code), lu.sous_type or "-",
                     f"{(lu.fin - lu.depart) // 1000} ms", decodable))


def jouer(formes, carte, delais, lire=None, pause=time.sleep, tls=http.CONTEXTE, sortie=print):
    """Lit chaque forme de `formes`, puis de `carte` ({nom, hote, port, chemin, methode, corps, espace, decodeur}),
    puis CryptoCompare ; `delais` : (délai du pool, délai de la carte), en µs ; `lire` : `http.lire` par défaut, lu à
    l'appel. Imprime une ligne par lecture et le verdict ; rend le code (0 : pool et témoin décodent tous ; 1 sinon)."""
    lire, vus, echecs = lire or http.lire, set(), 0
    for x, delai, r in [(x, delais[0], role(x)) for x in formes] + [(x, delais[1], "carte") for x in carte]:
        if x["espace"] and x["hote"] in vus:
            pause(1)
        vus.add(x["hote"])
        req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
        lu = decodeurs.appliquer(x["decodeur"], lire(req, {}, delai=delai, tls=tls))
        echecs += r != "carte" and lu.statut != "ok"
        sortie(ligne(r, x["nom"], x["hote"], lu, "décodable " + ("oui" if lu.statut == "ok" else "non")))
    lu = lire(CRYPTOCOMPARE, {}, delai=delais[0], tls=tls)
    sortie(ligne("exclue", "cryptocompare", CRYPTOCOMPARE.hote, lu, "attendu 401 : " + (
        "OK" if lu.code == 401 else "ÉCART")))
    sortie(f"smoke : {'ÉCHEC' if echecs else 'OK'} ({len(formes) - echecs}/{len(formes)} formes du pool et du "
           "témoin décodées)")
    return 1 if echecs else 0
