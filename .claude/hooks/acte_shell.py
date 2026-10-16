"""Shōgen, lecture de l'acte d'une commande shell, pour le crochet GARDE-FAITS (lot GARDE-FOUS-ORCH, phase 2 ; item
SHOGEN-GARDE-CROCHET-ACTE-1, LN-6 du contre-contrôle : le crochet jugeait le texte de la commande, et un commit écrit
dans un heredoc ou entre guillemets passait pour un commit). La commande est découpée par shlex (POSIX, ponctuation
du shell, saut de ligne séparateur) en commandes simples : programme (après affectations, mots réservés et
enveloppes timeout, env, nohup, …), mots, redirections, corps de heredoc, arrière-plan (& d'une commande, d'une liste,
d'un groupe, d'une boucle), boucles englobantes ; bash -c, sh -c, eval, heredoc donné à un shell et substitutions
$(…) et `…` entre guillemets sont lus récursivement. analyser() rend None si shlex ne lit pas la commande : le crochet
revient alors à ses motifs (sens sûr). G2, C-3 : une boucle while ou until à condition constante (while true, while :,
until false, ou leur négation) est marquée sans fin (while-sans-fin, until-sans-fin) dans boucles.
Limites : un opérateur seul entre guillemets est lu comme opérateur ; un script lancé par son nom (bash x.sh)
n'est pas lu ; case n'est pas analysé. Bibliothèque standard seule (R-8)."""
import os
import re
import shlex

PONCT = "();<>|&\n"
ponctuation = lambda t: bool(t) and all(c in PONCT for c in t)  # noqa: E731 (jeton d'opérateurs du shell)
AFFECT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?=")
SEPARATEUR = re.compile(r"&&|\|\||;;|\|&|[;&|()\n]")
DEBUT = {"!", "if", "then", "else", "elif", "do", "time", "{", "while", "until"}
FIN = {"done", "fi", "esac", "}"}
SHELLS = {"bash", "sh", "dash", "zsh", "ksh"}
PYTHON = re.compile(r"^python[0-9.]*$")
ENVELOPPES = {      # nom : (options suivies d'une valeur, arguments positionnels avant la commande)
    "timeout": ({"-s", "--signal", "-k", "--kill-after"}, 1), "nohup": (set(), 0), "setsid": (set(), 0),
    "env": ({"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}, 0), "command": (set(), 0),
    "exec": ({"-a"}, 0), "nice": ({"-n", "--adjustment"}, 0), "stdbuf": ({"-i", "-o", "-e"}, 0),
    "ionice": ({"-c", "-n", "-p", "--class", "--classdata"}, 0), "sudo": ({"-u", "-g", "-U", "-C", "-h", "-p"}, 0),
    "xargs": ({"-n", "-I", "-d", "-P", "-L", "-s", "-a", "-E"}, 0), "time": (set(), 0)}


def jetons(texte):
    """Jetons shlex du texte (heredocs ôtés) ; ValueError si shlex ne le lit pas."""
    lex = shlex.shlex(texte, posix=True, punctuation_chars=PONCT)
    lex.whitespace_split, lex.whitespace, lex.commenters = True, " \t\r", ""
    return list(lex)


def decouper(texte):
    """(jetons, corps des heredocs dans l'ordre des opérateurs) : chaque corps est ôté du texte avant la lecture."""
    lignes, vues, corps, i = texte.split("\n"), [], [], 0
    while i < len(lignes):
        vues.append(lignes[i])
        i += 1
        try:
            t = jetons("\n".join(vues))
        except ValueError:
            continue            # guillemet ouvert sur la ligne suivante
        for fin in [t[k + 1] for k in range(len(t) - 1) if t[k] == "<<"][len(corps):]:
            ote, lu = fin.startswith("-"), []          # <<-FIN : tabulations de tête ôtées
            fin = fin[1:] if ote else fin
            while i < len(lignes) and (lignes[i].lstrip("\t") if ote else lignes[i]) != fin:
                lu.append(lignes[i])
                i += 1
            i += 1
            corps.append("\n".join(lu))
    return jetons("\n".join(vues)), corps


def deballer(mots):
    """Mots après les enveloppes (timeout 60 env X=1 nohup cmd … → cmd …)."""
    while mots and os.path.basename(mots[0]) in ENVELOPPES:
        valeurs, positions = ENVELOPPES[os.path.basename(mots[0])]
        i = 1
        while i < len(mots) and mots[i].startswith("-") and mots[i] != "-":
            if mots[i] == "--":
                i += 1
                break
            i += 2 if mots[i] in valeurs else 1
        while i < len(mots) and AFFECT.match(mots[i]):
            i += 1
        mots = mots[i + positions:]
    return mots


def substitutions(mot):
    """Textes des $(…) (parenthèses équilibrées) et `…` d'un mot."""
    out, i = re.findall(r"`([^`]*)`", mot), mot.find("$(")
    while i >= 0:
        n, j = 1, i + 2
        while j < len(mot) and n:
            n += {"(": 1, ")": -1}.get(mot[j], 0)
            j += 1
        out.append(mot[i + 2:j - 1] if not n else mot[i + 2:])
        i = mot.find("$(", j)
    return out


def options_c(mots):
    """Script d'un shell lancé avec -c (option seule ou groupée : -lc, -ec), sinon None."""
    k = 1
    while k < len(mots) and mots[k][:1] in "-+" and mots[k] not in ("-", "--"):
        if not mots[k].startswith("--") and "c" in mots[k][1:]:
            return next((x for x in mots[k + 1:] if not x.startswith("-")), None)
        k += 2 if mots[k] in ("-o", "+o", "-O", "+O") else 1
    return None


def analyser(texte, fond=False, boucles=(), profondeur=0):
    """Liste des actes (dict : mots, prog, redirs [(op, cible)], corps, fond, boucles, python) de la commande, actes
    lus récursivement à la suite de leur parent ; None si un texte ne se lit pas."""
    if profondeur > 5:
        return []
    try:
        toks, corps = decouper(texte)
    except ValueError:
        return None
    evenements, cur, corps_restants = [], {"mots": [], "redirs": [], "corps": []}, iter(corps)
    k = 0
    while k < len(toks):
        t = toks[k]
        if ponctuation(t) and ("<" in t or ">" in t):
            cible = toks[k + 1] if k + 1 < len(toks) and not ponctuation(toks[k + 1]) else ""
            if cur["mots"] and cur["mots"][-1].isdigit() and re.search(re.escape(cur["mots"][-1] + t), texte):
                cur["mots"].pop()           # descripteur collé (2>, 1>>) : pas un mot
            if t == "<<":
                cur["corps"].append(next(corps_restants, ""))
            else:
                cur["redirs"].append((t, cible))
            k += 2 if cible else 1
            continue
        if ponctuation(t):
            evenements += [("cmd", cur), ("sep", t)]
            cur = {"mots": [], "redirs": [], "corps": []}
        else:
            cur["mots"].append(t)
        k += 1
    evenements.append(("cmd", cur))
    actes, pile, debut = [], [], 0
    for genre, x in evenements:
        if genre == "sep":
            for s in SEPARATEUR.findall(x):
                if s == "&":
                    for a in actes[debut:]:
                        a["fond"] = True
                if s in ("&", ";", ";;", "\n"):       # && et || : la liste entière va au fond avec son &
                    debut = len(actes)
                elif s == "(":
                    pile.append(("(", debut))
                    debut = len(actes)
                elif s == ")":
                    while pile and pile[-1][0] != "(":
                        pile.pop()
                    debut = pile.pop()[1] if pile else debut
            continue
        mots, boucle = list(x["mots"]), None
        while mots and (mots[0] in DEBUT or mots[0] in FIN or mots[0] == "for" or AFFECT.match(mots[0])):
            m = mots.pop(0)
            if m in ("while", "until", "for", "{"):
                pile.append((m, debut))
                debut = len(actes)
                boucle = [m, False] if m in ("while", "until") else boucle
            elif m in ("done", "}"):
                while pile and pile[-1][0].split("-")[0] not in (("while", "until", "for") if m == "done" else ("{",)):
                    pile.pop()
                debut = pile.pop()[1] if pile else debut
            elif m == "!" and boucle:
                boucle[1] = not boucle[1]
            if m == "for":
                mots = []           # for x in liste : la liste n'est pas une commande
        if boucle and pile and pile[-1][0] == boucle[0]:    # G2, C-3 : condition constante, boucle sans fin
            sans_fin = mots[:1] in (["true"], [":"]) if (boucle[0] == "while") != boucle[1] else mots[:1] == ["false"]
            pile[-1] = (boucle[0] + "-sans-fin", pile[-1][1]) if sans_fin else pile[-1]
        mots = deballer(mots)
        if not mots and not x["redirs"] and not x["corps"]:
            continue
        acte = {"mots": mots, "prog": os.path.basename(mots[0]) if mots else "", "redirs": x["redirs"],
                "corps": x["corps"], "fond": fond, "boucles": tuple(boucles) + tuple(g for g, _ in pile if g != "("),
                "python": []}
        actes.append(acte)
        sous = [y for m in mots[1:] for y in substitutions(m)]
        if acte["prog"] in SHELLS:
            script = options_c(mots)
            sous += [script] if script is not None else ([] if len(mots) > 1 and not mots[1].startswith("-")
                                                           else x["corps"])
        elif acte["prog"] == "eval":
            sous.append(" ".join(mots[1:]))
        elif PYTHON.match(acte["prog"]):
            c = [mots[k + 1] for k in range(1, len(mots) - 1) if mots[k] == "-c"]
            acte["python"] = c or (x["corps"] if all(m.startswith("-") for m in mots[1:]) else [])
        acte["sous"] = sous
    resultat = []
    for a in actes:
        resultat.append(a)
        for s in a.pop("sous"):
            lu = analyser(s, a["fond"], a["boucles"], profondeur + 1)
            if lu is None:
                return None
            resultat += lu
    return resultat


def options_courtes(mots):
    """Lettres des options courtes groupées (-rf → r, f) et options longues, jusqu'à --, où qu'elles soient."""
    out = set()
    for m in mots[1:mots.index("--") if "--" in mots else len(mots)]:
        out |= (set(m[1:]) if not m.startswith("--") else {m}) if m.startswith("-") else set()
    return out


def git_sous_commande(mots):
    """(sous-commande, arguments) d'un appel à git, options globales sautées (-C D, -c X, --git-dir=…)."""
    i = 1
    while i < len(mots) and mots[i].startswith("-"):
        i += 2 if mots[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path") else 1
    return (mots[i], mots[i + 1:]) if i < len(mots) else ("", [])
