"""Pré-contrôle S-G5 (approximation de xtask/src/sg5.rs, régime complet), versé depuis le scratchpad de
l'orchestrateur (sha256 d'origine 60de4077…87ef0 ; lot GARDE-FOUS-ORCH, GF-2 ; erreurs E9 et E10). Algorithme
inchangé : fragment anglais d'au moins 15 octets entre guillemets français, introuvable dans biblio/INDEX.md et les
octets texte de biblio/. Changements : fonction introuvables(racine, fichiers) ; sorties 0 (aucun fragment), 1 (au
moins un), 3 (erreur, biblio/INDEX.md absent compris) ; fichiers ouverts par `with` ; chemin interdit jamais ouvert
ni nommé (garde_commun), la racine comprise (relecture G2, C-10).

Usage : python3 -I -B presg5.py <racine du dépôt> <fichier.md>...
Imprime chemin:ligne et le fragment anglais introuvable, puis le compte, comme l'outil d'origine.
Signal seulement : la gate de xtask reste le juge.
"""
import importlib.util
import os
import re
import sys


def _module(nom):
    """Module frère chargé par son chemin : sous -I, le dossier du script n'est pas dans sys.path."""
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), nom + ".py")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


GC = _module("garde_commun")

MOTS = [" the ", " of ", " to ", " is ", " are ", " that ", " not ", " be ", " with ", " it ", " we ",
        " this ", " they ", " has ", " have "]
TEXTE = {"html", "htm", "txt", "md", "sidecar", "json", "xml", "rs", "toml", "yml", "yaml", "lock"}
ENTITES = [("&quot;", '"'), ("&#39;", "'"), ("&#x27;", "'"), ("&#8217;", "'"), ("&rsquo;", "'"), ("&lsquo;", "'"),
           ("&#8220;", '"'), ("&#8221;", '"'), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&apos;", "'"), ("&nbsp;", " "),
           ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("ﬀ", "ff"), ("ﬁ", "fi"), ("ﬂ", "fl"),
           ("ﬃ", "ffi"), ("ﬄ", "ffl")]


def lire(chemin, **texte):
    with open(chemin, "r" if texte else "rb", **texte) as f:
        return f.read()


def plier(c):
    return {"‘": "'", "’": "'", "“": '"', "”": '"'}.get(c, c)


def normaliser(t):
    for a, b in ENTITES:
        t = t.replace(a, b)
    out, blanc = [], False
    for c in t:
        c = plier(c)
        if c in "*`":
            continue
        if c.isspace():
            if not blanc:
                out.append(" ")
            blanc = True
        else:
            out.append(c)
            blanc = False
    return "".join(out).strip()


def retirer_balises(t):
    out, reste = [], t
    while "<" in reste:
        i = reste.find("<")
        out.append(reste[:i])
        apres = reste[i:]
        j = apres[1:].find(">")
        if 0 <= j <= 300:
            reste = apres[j + 2:]
        else:
            out.append("<")
            reste = apres[1:]
    out.append(reste)
    return "".join(out)


def retirer_pagination_rfc(t):
    def garder(l):
        n = l.rstrip()
        pied = n.endswith("]") and "[Page " in n and ("Standards Track" in n or "Informational" in n)
        fin = n.rsplit(" ", 1)[-1]
        entete = n.startswith("RFC ") and len(n) > 40 and len(fin) == 4 and fin.isdigit()
        return not (pied or entete or "\x0c" in n)
    return "\n".join(l for l in t.splitlines() if garder(l))


def scinder_crochets(t):
    out, reste = [], t
    while "[" in reste:
        i = reste.find("[")
        out.append(reste[:i])
        apres = reste[i:]
        j = apres[1:].find("]")
        if 0 <= j <= 30:
            out.append("…")
            reste = apres[j + 2:]
        else:
            out.append("[")
            reste = apres[1:]
    out.append(reste)
    return "".join(out)


def fragments(cit):
    p = "".join(plier(c) for c in cit).replace("[…]", "…").replace("[...]", "…").replace("...", "…")
    p = scinder_crochets(p)
    return re.split(r"[…]|[^\u0000-ɏ -⁯]", p)


def anglais(f):
    b = f" {f.lower()} "
    return sum(b.count(m) for m in MOTS) >= 2


def corpus(racine):
    c = [normaliser(lire(os.path.join(racine, "biblio", "INDEX.md"), encoding="utf-8", errors="replace"))]
    for n in sorted(os.listdir(os.path.join(racine, "biblio"))):
        p = os.path.join(racine, "biblio", n)
        ext = n.rsplit(".", 1)[-1].lower() if "." in n else ""
        if n == "INDEX.md" or not os.path.isfile(p) or GC.chemin_interdit(p):
            continue
        t = lire(p).decode("utf-8", "replace")
        if ext == "sidecar":
            c.append(normaliser(t))
        elif ext in TEXTE:
            c.append(normaliser(retirer_balises(retirer_pagination_rfc(t))))
    return c


def introuvables(racine, fichiers):
    """[(fichier, ligne, fragment)] : fragments anglais d'au moins 15 octets, entre guillemets français, introuvables
    dans biblio/INDEX.md et les octets texte de biblio/."""
    c = corpus(racine)
    cc = [x.replace("-", "").replace(" ", "") for x in c]
    trouves = []
    for f in fichiers:
        t = lire(f, encoding="utf-8")
        for m in re.finditer("«([^»]*)»", t):
            for fr in fragments(m.group(1)):
                x = normaliser(fr)
                x = re.sub(r"^\W+|\W+$", "", x)
                if len(x.encode()) < 15 or not anglais(x):
                    continue
                xc = x.replace("-", "").replace(" ", "")
                if any(x in p for p in c) or any(xc in p for p in cc):
                    continue
                trouves.append((f, t.count(chr(10), 0, m.start()) + 1, x))
    return trouves


def main(argv):
    """Sortie 0 : aucun fragment ; 1 : au moins un (lignes de l'outil d'origine) ; 3 : erreur (arguments, fichier
    illisible, biblio/INDEX.md absent, chemin interdit : jamais ouvert ni nommé)."""
    if len(argv) < 2:
        print("usage : presg5.py <racine du dépôt> <fichier.md>...", file=sys.stderr)
        return 3
    interdits = sum(map(GC.chemin_interdit, argv))
    if interdits:
        print(f"presg5 : {interdits} chemin(s) interdit(s), non ouvert(s)", file=sys.stderr)
        return 3
    try:
        trouves = introuvables(argv[0], argv[1:])
    except (OSError, UnicodeDecodeError) as e:
        print(f"presg5 : erreur : {type(e).__name__} : {e}", file=sys.stderr)
        return 3
    for f, n, x in trouves:
        print(f"{f}:{n}: « {x[:160]} »")
    print(f"presg5 : {len(trouves)} fragment(s) introuvable(s)")
    return 1 if trouves else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
