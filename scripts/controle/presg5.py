"""Pré-contrôle S-G5 (approximation de xtask/src/sg5.rs, régime complet) sur des fichiers hors du dépôt.

Usage : python3 -I presg5.py <racine du dépôt> <fichier.md>...
Imprime chemin:ligne et le fragment anglais introuvable dans biblio/INDEX.md et les octets texte de biblio/.
Signal seulement : la gate de xtask reste le juge.
"""
import os, re, sys

MOTS = [" the ", " of ", " to ", " is ", " are ", " that ", " not ", " be ", " with ", " it ", " we ",
        " this ", " they ", " has ", " have "]
TEXTE = {"html", "htm", "txt", "md", "sidecar", "json", "xml", "rs", "toml", "yml", "yaml", "lock"}
ENTITES = [("&quot;", '"'), ("&#39;", "'"), ("&#x27;", "'"), ("&#8217;", "'"), ("&rsquo;", "'"), ("&lsquo;", "'"),
           ("&#8220;", '"'), ("&#8221;", '"'), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&apos;", "'"), ("&nbsp;", " "),
           ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("ﬀ", "ff"), ("ﬁ", "fi"), ("ﬂ", "fl"),
           ("ﬃ", "ffi"), ("ﬄ", "ffl")]


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
    c = [normaliser(open(os.path.join(racine, "biblio", "INDEX.md"), encoding="utf-8", errors="replace").read())]
    for n in sorted(os.listdir(os.path.join(racine, "biblio"))):
        p = os.path.join(racine, "biblio", n)
        ext = n.rsplit(".", 1)[-1].lower() if "." in n else ""
        if n == "INDEX.md" or not os.path.isfile(p):
            continue
        t = open(p, "rb").read().decode("utf-8", "replace")
        if ext == "sidecar":
            c.append(normaliser(t))
        elif ext in TEXTE:
            c.append(normaliser(retirer_balises(retirer_pagination_rfc(t))))
    return c


def main():
    racine, fichiers = sys.argv[1], sys.argv[2:]
    c = corpus(racine)
    cc = [x.replace("-", "").replace(" ", "") for x in c]
    n = 0
    for f in fichiers:
        t = open(f, encoding="utf-8").read()
        for m in re.finditer("«([^»]*)»", t):
            for fr in fragments(m.group(1)):
                x = normaliser(fr)
                x = re.sub(r"^\W+|\W+$", "", x)
                if len(x.encode()) < 15 or not anglais(x):
                    continue
                xc = x.replace("-", "").replace(" ", "")
                if any(x in p for p in c) or any(xc in p for p in cc):
                    continue
                n += 1
                print(f"{f}:{t.count(chr(10), 0, m.start()) + 1}: « {x[:160]} »")
    print(f"presg5 : {n} fragment(s) introuvable(s)")


main()
