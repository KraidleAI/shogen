"""Relevé ASN d'un hôte (CB-12b ; E-C-30 ; ADR-0029 l.79-80, l.247 ; PROPOSITION §2.1 ; FORMAT §15). Trois parties,
journalisées chacune à part, valeurs brutes et décodées, échec typé, sans jugement (la concordance se juge au recalcul,
`r2._asn_state`, E-R-29) : (1) A de l'hôte au résolveur de l'observateur (client DNS de CB-10, avec récursion ;
jamais 1.1.1.1, ADR-0029 l.82), dont la première adresse de type A est retenue (forme de S2,
`r2.resolve_host_real`, r2.py l.315-343) ; (2) RIPEstat prefix-overview sur cette adresse (client HTTPS de CB-3 ;
forme de S2 reprise, `r2._ripestat_asn` l.275-289 : `data.asns[0].asn` et `.holder`, `data.resource`) ; (3) Team
Cymru, TXT de `<d>.<c>.<b>.<a>.origin.asn.cymru.com` au même résolveur (forme de S2, `_cymru_asn` l.292-312 : premier
nombre du premier champ, première réponse lisible). Sans adresse (pas de réponse, pas de A, drapeau TC : FORMAT §12),
RIPEstat et Cymru ne sont pas interrogés. Ne lève jamais : les deux clients ne lèvent pas, le décodage est rattrapé."""
import json

from shogen_s2bis.collecte import dns, http, journal
from shogen_s2bis.collecte.lecture import Lecture

RIPESTAT, CHEMIN = "stat.ripe.net", "/data/prefix-overview/data.json?resource="
CYMRU = "origin.asn.cymru.com."
VALEURS = 4096                      # octets canoniques des valeurs de RIPEstat au plus, saut de ligne compris
ASN = 1 << 32                       # numéro d'AS : entier de 0 à 2^32 exclu (RFC 6793)


def _asn(x):
    """Numéro d'AS lu en entier, ou en texte décimal comme `int()` de S2 ; booléen, flottant ou hors bornes : refus."""
    n = int(x) if type(x) in (int, str) else -1
    if not 0 <= n < ASN:
        raise ValueError(f"numéro d'AS : {x!r}")
    return n


def ripestat(octets):
    """{asn, detenteur, prefixe} du corps de RIPEstat ; `asns` vide : `asn` et `detenteur` null (base muette, sans
    échec) ; lève si le corps est illisible, un champ d'un autre type, ou les valeurs au-delà de VALEURS octets."""
    d = json.loads(octets)["data"]
    asns = d.get("asns") or []
    v = {"asn": _asn(asns[0]["asn"]) if asns else None, "detenteur": asns[0].get("holder") if asns else None,
         "prefixe": d.get("resource")}
    if not all(x is None or type(x) is str for x in (v["detenteur"], v["prefixe"])) or len(
            journal.canonique(v)) > VALEURS:
        raise ValueError("ripestat : valeurs")
    return v


def cymru(resultat):
    """Numéro d'AS de la première réponse TXT lisible d'un résultat DNS (FORMAT §12), None sinon."""
    for _nom, genre, _ttl, chaines in resultat["reponses"] or []:
        if genre == 16 and chaines:                                 # TXT : liste de chaînes (FORMAT §12)
            try:
                return _asn(chaines[0].split("|", 1)[0].split()[0])
            except (ValueError, IndexError):
                continue
    return None


def releve(hote, resolveur, lire=http.lire, interroger=dns.interroger):
    """Champs d'un enregistrement `asn` : {hote, a, ip, ripestat, cymru} ; `ripestat` (champs d'une `lecture`, FORMAT
    §9.1, `valeurs` de `ripestat`) et `cymru` (résultat DNS et `asn`) null sans adresse."""
    a = interroger(resolveur, hote, "A")
    ip = next((x for _n, t, _ttl, x in a["reponses"] or [] if t == 1), None) if a["statut"] == "reponse" else None
    if ip is None:
        return {"hote": hote, "a": a, "ip": None, "ripestat": None, "cymru": None}
    lu = lire(http.Requete(RIPESTAT, CHEMIN + ip))
    if lu.statut == "ok":
        try:
            statut, valeurs = "ok", ripestat(lu.octets)
        except Exception:                                           # attrape-tout : un indécodable est une panne
            statut, valeurs = "panne_decode", None
        lu = Lecture(statut, lu.depart, lu.fin, lu.phases, lu.adresse, code=lu.code, octets=lu.octets, valeurs=valeurs)
    c = interroger(resolveur, ".".join(reversed(ip.split("."))) + "." + CYMRU, "TXT")
    return {"hote": hote, "a": a, "ip": ip, "ripestat": lu.enregistrement(), "cymru": {**c, "asn": cymru(c)}}
