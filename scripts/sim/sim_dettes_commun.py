"""Lot DETTES-SIM (2026-10-04) : fonctions communes aux scripts neufs du lot, sans statistique de la règle.
Pool optionnel (ordre de imap conservé), moyenne et erreur-type, contrôle « |mesure − théorie| ≤ 5 SE » des oracles
internes, écriture fail-closed des sorties (json, txt, log.txt ; mode xb, jamais d'écrasement ; heures et durées au
seul log.txt). Worker G1 DETTES-SIM, claude-opus-5-5."""
import contextlib, hashlib, json, math, multiprocessing, os, platform, sys, time

import sim_niveau as S

ETIQUETTE = "ajoutée après l'exécution unique ; synthétique ; hors décision"


def pool(k):
    return multiprocessing.Pool(k) if k > 1 else contextlib.nullcontext()


def imap(pl, f, taches, paquet):
    return pl.imap(f, taches, paquet) if pl else map(f, taches)


def moy_se(v):
    m, s = S.moy_sd(v)
    return m, s / math.sqrt(len(v))


def controle(nom, m, th, se):
    """Oracle interne : |m − th| ≤ 5·se, sinon RuntimeError (le script sort sans écrire de fichier)."""
    if not abs(m - th) <= 5 * se:
        raise RuntimeError(f"oracle interne {nom} : {m!r} contre {th!r}, SE {se!r}")
    return {"controle": nom, "mesure": m, "theorie": th, "ecart_en_SE": (m - th) / se if se else 0.0}


def shas(*fichiers):
    return {os.path.basename(f): S.sha256_fichier(f) for f in fichiers}


def chemins(sortie, base):
    c = [os.path.join(sortie, base + x) for x in (".json", ".txt", ".log.txt")]
    if any(map(os.path.exists, c)):
        sys.exit("refus : un fichier de sortie existe deja (jamais d'ecrasement)")
    return c


def ecrire(ch, ent, tx, processus, debut, journal):
    js = json.dumps(ent, ensure_ascii=False, indent=1) + "\n"
    log = [f"sha256 des scripts {ent['script_sha256']}", f"python {sys.version} ; {sys.executable}",
           f"plateforme {platform.platform()} ; cpu_count {os.cpu_count()} ; processus {processus}",
           f"ligne de commande {sys.argv}", time.strftime("debut %Y-%m-%dT%H:%M:%SZ", debut)
           + time.strftime(" ; fin %Y-%m-%dT%H:%M:%SZ", time.gmtime()), *journal]
    log += [f"sha256 {os.path.basename(c)} {hashlib.sha256(x.encode('utf-8')).hexdigest()}" for c, x in zip(ch, (js, tx))]
    os.makedirs(os.path.dirname(ch[0]) or ".", exist_ok=True)
    for c, x in zip(ch, (js, tx, "\n".join(log) + "\n")):
        with open(c, "xb") as f:
            f.write(x.encode("utf-8"))
