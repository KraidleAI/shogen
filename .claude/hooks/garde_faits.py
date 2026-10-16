#!/usr/bin/env python3
"""Shōgen, garde des faits (crochets Claude Code). Règle du fondateur (2026-10-15) : « aucun acte n'est
possible sans vérification, rien de mémoire ». Le journal de la session (transcript) est le registre des
faits : chaque commande lancée et chaque résultat affiché. Un acte dont la vérification manque dans les
derniers appels de l'agent qui agit est REFUSÉ (sortie 2, motif sur stderr) ; les motifs commencent par
GARDE-FAITS et ne comptent jamais comme des faits affichés.

Crochets : PreToolUse (Bash, Edit, Write, MultiEdit, Agent, Workflow) ; Stop et SubagentStop.
Entrée : JSON sur stdin (session_id, transcript_path, cwd, tool_name, tool_input, agent_id éventuel).
Journal lu : celui de l'agent qui agit ; pour un sous-agent, <dossier de session>/subagents/agent-<agent_id>.jsonl.
Seule la fin du journal est lue (QUEUE octets), il devient très gros.

Règles PreToolUse (R1 à R6) :
  R1 effacer un worktree ou un clone (rm -rf, git worktree remove) : « git status » et « git log origin/… ..HEAD »
     (ou @{u}..HEAD, --not --remotes) lus avant ;
  R2 écrire dans un fichier existant par le shell (>, >>, tee, sed -i, python open 'w'/'a', Add-Content) :
     le fichier lu avant (Read, cat, tail, head, sed -n, grep, less, diff, git show, python open 'r') ;
  R3 git commit : diff ou status lu avant ; git push : ce qui part lu avant (git log …origin…, status, ls-remote,
     rev-list …origin…) ;
  R4 lancer un sous-agent ou un workflow dont la consigne nomme un arbre git : l'état de cet arbre lu avant
     (git status ou git log dans la fenêtre) ;
  R5 écrire un identifiant de commit (7 à 40 hexadécimaux, lettres et chiffres mêlés) ou un numéro de PR
     (#123, PR n° 123, pull/123) dans un .md, un message de commit, une PR, un texte écrit par le shell :
     il doit avoir été affiché par un outil (tool_result, attachment, queue-operation) ; le texte tapé par
     l'agent et les refus de ce crochet ne comptent pas.
Crochets Stop et SubagentStop (R6) : le dernier texte de l'agent ne porte aucun nombre de trois chiffres ou plus (ni, E29, aucun
nombre d'un ou deux chiffres suivi d'une unité ou d'une grandeur de la feuille de route : jours, semaines, %, observateurs, …),
ni décimal, qu'aucun outil n'a affiché (séparateurs de milliers admis : 1 715, 1,715, 1 715). Au second arrêt
du même tour, laisser passer et le consigner (fichier d'état sous le dossier de la session).
Journal des décisions : <dossier de session>/garde-faits.log (une ligne par refus et par passage consigné).
Sortie : 0 permis ; 2 refusé ; 0 avec note sur stderr si le journal est illisible (jamais un refus aveugle).
Acte lu, non texte (phase 2, SHOGEN-GARDE-CROCHET-ACTE-1, LN-6) : R1, R2, R3 et le texte de R5 se lisent sur les actes
de la commande (acte_shell.py, voisin : rm récursif, git worktree remove, redirections, tee, sed -i, open en écriture
d'un code python, git commit et push, gh et curl vers la forge) ; un commit cité dans un heredoc ou un argument n'en est
pas un ; R5 lit le message de git commit (-m, et le fichier de -F). Commande illisible par shlex : motifs (sens sûr).
R7 (E18, E28) : refus d'un sleep d'avant-plan (hors boucle until, hors arrière-plan : &, run_in_background) et d'un
pkill -f ou pgrep -f dont le motif ne commence pas par ^ (le shell qui le lance porte le motif : il se reconnaît).
R8 (E20) : create_pull_request refusé sans preuve que la forge lance des jobs sur ce dépôt : au journal, un résultat
de mcp__github__actions_* (ou de gh run, gh api) du même owner/repo qui montre un run conclu success ou un job à
runner_id non nul ; ou, au marqueur scripts/controle/garde/forge-actions.txt, la ligne owner/repo AAAA-MM-JJ du jour
(date -u), écrite après constat.
R9 (E27) : seuil de coût avant Agent et Workflow : refus d'un workflow de plus de SEUIL_WORKFLOW agents (appels agent(
du script ; nombre inconnu, boucle qui les multiplie : refus), ou d'un lancement qui porterait les sous-agents vivants
(journal touché depuis VIVANT_S s) au-delà de SEUIL_VIVANTS ; sauf jeton FANOUT-AUTORISE (ou les mots fan out) écrit
par l'humain dans son dernier message (journal de la session, jamais un résultat d'outil)."""
import importlib.util
import json
import os
import re
import sys

QUEUE = 6_000_000          # octets lus en fin de journal (faits affichés)
FENETRE_APPELS = 60        # derniers appels d'outil de l'agent pour les lectures préalables (R1 à R4)
MARQUE = "GARDE-FAITS"

HEX_ID = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{7,40})(?![0-9a-fA-F])")
PR_NUM = re.compile(r"(?:(?<![\w/])#|\bPR\s*(?:n°|no\.?|#)?\s*|pull/|pulls/)(\d{1,6})\b", re.I)
NOMBRE = re.compile(r"(?<![\w.,])(\d{1,3}(?:[   ,]\d{3})+(?:[.,]\d+)?|\d+[.,]\d+|\d{3,})(?![\w])")
# E29 (2026-10-15) : un nombre d un ou deux chiffres suivi d une unite ou d une grandeur de la feuille de route est un fait
NOMBRE_UNITE = re.compile(r"(?<![\w.,])(\d{1,2})(?=\s*(?:%|jours?|semaines?|mois|heures?|minutes?|ans?|années?|observateurs?|actifs?|commits?|fenêtres?|pas|tests?|hôtes?|unités?|sources?|pages?|citations?|lignes?|items?|lots?|diffs?|machines?|places?|classes?|strates?|étapes?)\b)", re.I)
LECTURE_SHELL = re.compile(r"\b(cat|tail|head|less|more|diff|grep|awk|sed\s+-n|git\s+show|sha256sum\s+-c|wc)\b")
REDIR = re.compile(r"(?<![<>])(>>?|\btee(?:\s+-a)?)\s+(?!&)(['\"]?)([^\s'\"|;&]+)\2")
SED_I = re.compile(r"\bsed\s+(?:-[a-zA-Z]*i[a-zA-Z]*\b[^|;]*?)\s+(['\"]?)([^\s'\"|;&]+)\1\s*(?:[;&|]|$)")
PY_W = re.compile(r"open\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"][wa]")
RM = re.compile(r"\brm\s+(?:-[a-zA-Z]*\s+)*(['\"]?)([^\s'\"|;&]+)\1")
GIT_CMD = re.compile(r"\bgit(?:\s+(?:-C\s+\S+|--no-optional-locks|--git-dir=\S+|--work-tree=\S+))*\s+(\w[\w-]*)")


def _acte_shell():
    """acte_shell.py, voisin, chargé par son chemin (sous -I), sans bytecode écrit dans l'arbre ; None s'il manque ou
    ne se charge pas (motifs)."""
    sys.dont_write_bytecode = True
    try:
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "acte_shell.py")
        spec = importlib.util.spec_from_file_location("acte_shell", chemin)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    except Exception:
        return None


AS = _acte_shell()
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEUIL_WORKFLOW, SEUIL_VIVANTS, VIVANT_S = 3, 4, 300
JETON = re.compile(r"FANOUT-AUTORISE|\bfan[ -]?out\b", re.I)
RAPPEL = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
FORGE_JOB = re.compile(r'"runner_id"\s*:\s*[1-9]|"conclusion"\s*:\s*"success"|\bcompleted\s+success\b')


def lire_queue(chemin):
    """Lit la fin du journal (QUEUE octets), rend la liste des entrées JSON décodées."""
    out = []
    try:
        with open(chemin, "rb") as f:
            f.seek(0, 2)
            n = f.tell()
            f.seek(max(0, n - QUEUE))
            if n > QUEUE:
                f.readline()
            for ligne in f:
                try:
                    out.append(json.loads(ligne))
                except Exception:
                    continue
    except OSError:
        return None
    return out


def contenus(bloc):
    """Texte d'un bloc de contenu (str, dict content, liste)."""
    if bloc is None:
        return ""
    if isinstance(bloc, str):
        return bloc
    if isinstance(bloc, list):
        return "\n".join(contenus(b) for b in bloc)
    if isinstance(bloc, dict):
        if bloc.get("type") == "tool_result":
            return contenus(bloc.get("content"))
        if bloc.get("type") == "text":
            return bloc.get("text", "")
        if "content" in bloc and bloc.get("type") in (None, "queued_command"):
            return contenus(bloc.get("content"))
        return bloc.get("prompt", "") or bloc.get("text", "") or ""
    return str(bloc)


def faits_et_appels(entrees):
    """Sépare : textes affichés par des outils ou la veille (faits) ; appels d'outil (dans l'ordre) ;
    textes tapés par l'agent ; textes de l'humain. Les résultats qui portent la marque du crochet sont écartés
    des faits (ils citent l'identifiant refusé)."""
    faits, appels, agent, humain = [], [], [], []
    for e in entrees:
        t = e.get("type")
        if t == "user":
            for b in (e.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    txt = contenus(b)
                    if MARQUE not in txt:
                        faits.append(txt)
                else:
                    humain.append(contenus(b))
            tur = e.get("toolUseResult")
            if tur is not None:
                txt = json.dumps(tur, ensure_ascii=False) if not isinstance(tur, str) else tur
                if MARQUE not in txt:
                    faits.append(txt)
        elif t == "assistant":
            for b in (e.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    appels.append((b.get("name", ""), b.get("input") or {}))
                elif isinstance(b, dict) and b.get("type") == "text":
                    agent.append(b.get("text", ""))
        elif t == "attachment":
            faits.append(contenus(e.get("attachment")))
        elif t == "queue-operation":
            faits.append(e.get("content", "") or "")
    return faits, appels, agent, humain


def texte_appel(nom, inp):
    if nom == "Bash":
        return inp.get("command", "")
    if nom in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
        return inp.get("file_path", "") or inp.get("notebook_path", "")
    if nom in ("Grep",):
        return inp.get("path", "") or ""
    return json.dumps(inp, ensure_ascii=False)


def resoudre(chemin, cwd):
    if not chemin:
        return chemin
    chemin = os.path.expanduser(chemin)
    if not os.path.isabs(chemin):
        chemin = os.path.join(cwd or "", chemin)
    return os.path.normpath(chemin)


def fichier_lu_avant(cible, appels, cwd):
    """Vrai si un appel récent a lu la cible : Read/Edit/Write sur ce chemin, ou commande shell de lecture
    qui nomme ce chemin (absolu, relatif, ou son nom de base précédé d'un séparateur)."""
    base = os.path.basename(cible)
    for nom, inp in appels[-FENETRE_APPELS:]:
        if nom in ("Read", "Edit", "Write", "MultiEdit") and resoudre(inp.get("file_path", ""), cwd) == cible:
            return True
        if nom == "Bash":
            c = inp.get("command", "")
            if (cible in c or re.search(r"(^|[\s/'\"=])" + re.escape(base) + r"(?=$|[\s'\";|&)])", c)) and (
                LECTURE_SHELL.search(c) or PY_W.sub("", c) != c and "'r'" in c
            ):
                return True
    return False


def commandes_git_recentes(appels):
    out = []
    for nom, inp in appels[-FENETRE_APPELS:]:
        if nom == "Bash":
            out.append(inp.get("command", ""))
    return out


def a_lu(cmds, motif):
    r = re.compile(motif)
    return any(r.search(c) for c in cmds)


def identifiants_affiches(faits, humain):
    """Ensemble des identifiants hexadécimaux et numéros de PR affichés par des outils (ou tapés par l'humain)."""
    hexs, prs = set(), set()
    for txt in faits + humain:
        for h in HEX_ID.findall(txt):
            hexs.add(h.lower())
        for p in PR_NUM.findall(txt):
            prs.add(p)
    return hexs, prs


def est_identifiant_commit(h):
    """Un sha court ou long : lettres et chiffres mêlés (écarte les nombres purs et les mots comme 'deadbeef' ? non :
    'deadbeef' est admis comme identifiant possible ; seuls les suites purement numériques sont écartées)."""
    return any(c.isdigit() for c in h) and any(c.isalpha() for c in h)


def hex_affiche(h, hexs):
    """h est couvert si lui-même, un préfixe affiché de 7+ caractères, ou un affiché dont il est préfixe, existe."""
    h = h.lower()
    if h in hexs:
        return True
    for x in hexs:
        if len(x) >= 7 and (h.startswith(x) or x.startswith(h)):
            return True
    return False


def refuser(motif):
    sys.stderr.write(f"{MARQUE} : REFUS. {motif}\n")
    sys.exit(2)


def journaliser(dossier, ligne):
    try:
        with open(os.path.join(dossier, "garde-faits.log"), "a", encoding="utf-8") as f:
            f.write(ligne.rstrip("\n") + "\n")
    except OSError:
        pass


def journal_de_l_agent(entree):
    tp = entree.get("transcript_path") or ""
    agent = entree.get("agent_id") or entree.get("agentId") or ""
    if entree.get("agent_transcript_path"):
        return entree["agent_transcript_path"], os.path.dirname(tp)
    if agent:
        dossier = tp[:-6] if tp.endswith(".jsonl") else os.path.dirname(tp)
        return os.path.join(dossier, "subagents", f"agent-{agent}.jsonl"), os.path.dirname(tp)
    return tp, os.path.dirname(tp)


def fichiers_sed(mots):
    """Fichiers qu'un sed -i (ou --in-place) récrit, sinon [] : le script (premier mot, sauf -e ou -f) n'en est pas."""
    if not any(m.startswith("--in-place") or m[:1] == "-" and m[1:2] != "-" and "i" in m for m in mots[1:]):
        return []
    out, script, k = [], False, 1
    while k < len(mots):
        m = mots[k]
        script |= m in ("-e", "-f", "--expression", "--file") or m.startswith(("--expression=", "--file="))
        if m in ("-e", "-f", "--expression", "--file"):
            k += 1
        elif not m.startswith("-") or m == "-":
            out.append(m)
        k += 1
    return out if script else out[1:]


def messages_commit(args, corps, cwd):
    """Textes des messages d'un git commit : -m, --message, groupées (-am) ou collées ; fichier de -F et --file lu
    (-F - : corps du heredoc)."""
    out, k = [], 0
    while k < len(args):
        m, opt, v = args[k], None, None
        if m.startswith(("--message=", "--file=")):
            opt, v = m[2], m.split("=", 1)[1]
        elif m in ("--message", "--file"):
            opt, v, k = m[2], args[k + 1] if k + 1 < len(args) else "", k + 1
        elif m[:1] == "-" and m[1:2] != "-" and re.search("[mF]", m[1:]):
            p = re.search("[mF]", m[1:]).start() + 1
            opt, v = m[p].lower(), m[p + 1:] or (args[k + 1] if k + 1 < len(args) else "")
            k += 0 if m[p + 1:] else 1
        if opt == "m":
            out.append(v)
        elif opt == "f":
            out.append("\n".join(corps) if v == "-" else lire_texte(resoudre(v, cwd)))
        k += 1
    return out


def lire_texte(chemin):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            return f.read(1_000_000)
    except OSError:
        return ""


def motif_non_ancre(mots):
    """Vrai si pkill ou pgrep porte -f (--full, ou groupée : -af) et que son motif ne commence pas par ^."""
    plein, k = False, 1
    while k < len(mots):
        m = mots[k]
        if m == "--" or not m.startswith("-") or m == "-":
            motif = mots[k + 1] if m == "--" and k + 1 < len(mots) else (None if m == "--" else m)
            return plein and motif is not None and not motif.startswith("^")
        if m.startswith("--"):
            plein |= m == "--full"
            k += 2 if m in ("--signal", "--euid", "--uid", "--group", "--pgroup", "--parent", "--session", "--terminal",
                            "--pidfile", "--ns", "--nslist", "--runstates", "--delimiter", "--cgroup") else 1
        elif mots[0].endswith("pkill") and re.fullmatch(r"-([0-9]+|[A-Z][A-Z0-9+-]*)", m):
            k += 1                  # signal : -9, -TERM
        else:
            plein |= "f" in m[1:]
            k += 2 if m[-1] in "dgGPstuUFr" else 1
    return False


def faits_de_la_commande(c, cwd, fond=False):
    """Ce que fait la commande : rm (cibles d'un rm récursif), worktree (git worktree remove), ecrit (fichiers écrits),
    git (sous-commandes), messages (textes que R5 juge pour un commit), forge (gh, curl vers l'API). Lu sur les actes
    (LN-6) ; par les motifs d'avant si shlex ne lit pas la commande (sens sûr)."""
    actes = AS.analyser(c, fond) if AS else None
    if actes is None:
        g = GIT_CMD.search(c)
        return {"rm": [m.group(2) for m in RM.finditer(c)] if re.search(r"\brm\s+-[a-zA-Z]*[rR]", c) else [],
                "worktree": "git worktree remove" in c, "git": {g.group(1)} if g else set(), "messages": [c],
                "ecrit": [m.group(3) for m in REDIR.finditer(c)] + [m.group(2) for m in SED_I.finditer(c)]
                + PY_W.findall(c),
                "forge": bool(re.search(r"\bgh\s+pr\s+(create|comment|review|merge)|pull_request", c)), "actes": None}
    f = {"rm": [], "worktree": False, "git": set(), "messages": [], "ecrit": [], "forge": False, "actes": actes}
    for a in actes:
        m, p = a["mots"], a["prog"]
        f["ecrit"] += [x for op, x in a["redirs"] if ">" in op and not op.endswith("&")]
        f["ecrit"] += [x for code in a["python"] for x in PY_W.findall(code)]
        if p == "rm" and {"r", "R", "--recursive"} & AS.options_courtes(m):
            f["rm"] += [x for x in m[1:] if not x.startswith("-")]
        elif p == "tee":
            f["ecrit"] += [x for x in m[1:] if not x.startswith("-")]
        elif p == "sed":
            f["ecrit"] += fichiers_sed(m)
        elif p == "git":
            sous, reste = AS.git_sous_commande(m)
            f["git"].add(sous)
            f["worktree"] |= sous == "worktree" and reste[:1] == ["remove"]
            f["messages"] += messages_commit(reste, a["corps"], cwd) if sous == "commit" else []
        elif p == "gh" and m[1:2] in (["pr"], ["issue"], ["api"], ["release"]) or p == "curl" and "api.github.com" in c:
            f["forge"] = True
    return f


def appels_resultats(entrees):
    """[(nom, entrée, texte du résultat)] : appels d'outil appariés à leur résultat par l'identifiant d'appel."""
    blocs = lambda genre: [b for e in entrees if e.get("type") == genre for b in (e.get("message") or {}).get(
        "content") or [] if isinstance(b, dict)]      # noqa: E731
    res = {b.get("tool_use_id"): contenus(b) for b in blocs("user") if b.get("type") == "tool_result"}
    return [(b.get("name", ""), b.get("input") or {}, res.get(b.get("id"), "")) for b in blocs("assistant")
            if b.get("type") == "tool_use"]


def jour_utc():
    """Date du jour lue par date -u (les cas la fixent par un faux date en tête du PATH)."""
    import subprocess
    return subprocess.run(["date", "-u", "+%Y-%m-%d"], capture_output=True, text=True, timeout=10).stdout.strip()


def forge_lance(entrees, owner, repo):
    """Vrai si le journal ou le marqueur du jour montre que la forge lance des jobs sur owner/repo (R8, E20)."""
    cible = f"{owner}/{repo}".casefold()
    for nom, inp, txt in appels_resultats(entrees):
        if MARQUE in txt or not FORGE_JOB.search(txt):
            continue
        depot = f"{inp.get('owner', '')}/{inp.get('repo', '')}".casefold()
        if nom.startswith("mcp__github__actions_") and depot == cible:
            return True
        c = inp.get("command", "") if nom == "Bash" else ""
        if re.search(r"\bgh\s+(run|api)\b", c) and cible in c.casefold():
            return True
    marqueur = lire_texte(os.path.join(RACINE, "scripts", "controle", "garde", "forge-actions.txt"))
    lignes = {x.strip().casefold() for x in marqueur.split("\n") if x.strip() and not x.startswith("#")}
    return f"{cible} {jour_utc()}" in lignes


def tour_humain(entrees):
    """(indice, textes) du dernier message de l'humain (hors résultats d'outil, rappels du système et refus de ce
    crochet), suivi des messages qu'il a mis en file après lui."""
    idx, textes = None, []
    for i, e in enumerate(entrees):
        c = (e.get("message") or {}).get("content") if e.get("type") == "user" and not e.get("isMeta") else None
        blocs = [c] if isinstance(c, str) else [b for b in c or [] if isinstance(b, dict) and b.get("type") == "text"]
        txt = RAPPEL.sub("", "\n".join(contenus(b) for b in blocs))
        outils = isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c)
        if txt.strip() and MARQUE not in txt and not outils:
            idx, textes = i, [txt]
        elif idx is not None and e.get("type") == "attachment" and (e.get("attachment") or {}).get(
                "type") == "queued_command":
            textes.append(contenus(e.get("attachment")))
    return idx, textes


def agents_du_workflow(inp):
    """Agents qu'un Workflow lance : appels agent( de son texte, ou liste agents ; None si inconnu (aucun compte, ou
    boucle qui les multiplie)."""
    t = json.dumps(inp, ensure_ascii=False)
    n = len(re.findall(r"\bagent\s*\(", t))
    if n and re.search(r"\b(for|while)\s*\(|\.(map|forEach|flatMap)\s*\(|Array\.from|\bfor\s+\w+\s+(of|in)\b", t):
        return None
    liste = inp.get("agents") if isinstance(inp, dict) else None
    return n or (len(liste) if isinstance(liste, list) and liste else None)


def agents_vivants(entree):
    """Sous-agents de la session dont le journal a bougé depuis VIVANT_S secondes (identifiants distincts)."""
    import time
    tp = entree.get("transcript_path") or ""
    d = os.path.join(tp[:-6] if tp.endswith(".jsonl") else os.path.dirname(tp), "subagents")
    try:
        noms = os.listdir(d)
    except OSError:
        return 0
    return len({x.split(".")[0] for x in noms if x.startswith("agent-")
                and time.time() - os.path.getmtime(os.path.join(d, x)) < VIVANT_S})


def pre_tool_use(entree):
    nom = entree.get("tool_name", "")
    inp = entree.get("tool_input") or {}
    cwd = entree.get("cwd") or os.getcwd()
    chemin, dossier = journal_de_l_agent(entree)
    entrees = lire_queue(chemin)
    if entrees is None:
        sys.stderr.write(f"{MARQUE} : journal illisible ({chemin}) ; acte permis sans contrôle.\n")
        return 0
    faits, appels, agent, humain = faits_et_appels(entrees)
    cmds = commandes_git_recentes(appels)
    textes_ecrits = []     # textes où un identifiant écrit doit avoir été affiché (R5)

    if nom == "Bash":
        c = inp.get("command", "")
        fc = faits_de_la_commande(c, cwd, bool(inp.get("run_in_background")))
        # R1 : effacer un worktree ou un clone
        cibles_rm = [resoudre(x, cwd) for x in fc["rm"]]
        if fc["worktree"] or any(os.path.exists(os.path.join(p, ".git")) for p in cibles_rm):
            if not a_lu(cmds, r"\bgit(\s+-C\s+\S+)?\s+status\b"):
                refuser("R1 : effacer un arbre git exige « git status » lu avant, dans les derniers appels de cet agent.")
            if not a_lu(cmds, r"\bgit(\s+-C\s+\S+)?\s+(log|rev-list)\b.*(origin/\S+\.\.|@\{u\}\.\.|--not\s+--remotes|\.\.HEAD)"):
                refuser("R1 : effacer un arbre git exige ses commits non poussés lus avant (git log origin/<branche>..HEAD).")
        # R2 : écrire dans un fichier existant par le shell
        for cib in fc["ecrit"]:
            if not cib or cib in ("/dev/null", "/dev/stderr", "/dev/stdout") or cib.startswith("&"):
                continue
            abs_c = resoudre(cib, cwd)
            if os.path.isfile(abs_c) and not fichier_lu_avant(abs_c, appels, cwd):
                refuser(f"R2 : écrire dans un fichier existant exige sa lecture avant (Read, cat, tail…) : {abs_c}")
            if os.path.isfile(abs_c) and abs_c.endswith((".md", ".txt", ".tsv", ".yml", ".yaml", ".json")):
                textes_ecrits.append(c)
        # R3 : commit et push (sous-commandes de git lues sur les actes)
        if "commit" in fc["git"]:
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+(status|diff)\b"):
                refuser("R3 : « git commit » exige le diff ou le status de l'arbre lu avant, dans les derniers appels de cet agent.")
            textes_ecrits += fc["messages"]
        if "push" in fc["git"]:
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+((log|rev-list)\b.*origin|status\b|ls-remote\b)"):
                refuser("R3 : « git push » exige ce qui part lu avant (git log origin/<branche>..HEAD, git status ou ls-remote).")
        if fc["forge"]:
            textes_ecrits.append(c)
        # R7 (E18, E28) : attente d'avant-plan, motif de processus non ancré
        attente = "R7 (E18) : sleep d'avant-plan ; attendre par une boucle until (until <condition>; do sleep N; done) "
        attente += "ou lancer en arrière-plan (run_in_background, ou commande suivie de &) et sonder."
        ancre = "R7 (E28) : pkill -f ou pgrep -f à motif non ancré, qui reconnaît le shell qui le lance ; ancrer par ^ "
        ancre += "(pgrep -f '^bash chaine_x.sh')."
        for a in fc["actes"] or []:
            if a["prog"] == "sleep" and not a["fond"] and "until" not in a["boucles"]:
                refuser(attente)
            if a["prog"] in ("pkill", "pgrep") and motif_non_ancre(a["mots"]):
                refuser(ancre)
        motifs = fc["actes"] is None            # commande illisible par shlex : motifs (sens sûr)
        if motifs and re.search(r"(^|[;&|(\s])sleep\s", c) and not re.search(r"\buntil\b", c) and not inp.get(
                "run_in_background"):
            refuser(attente)
        if motifs and re.search(r"\bp(kill|grep)\s[^;&|]*-[a-zA-Z]*f", c) and not re.search(r"\s['\"]?\^", c):
            refuser(ancre)
    elif nom in ("Edit", "MultiEdit", "Write"):
        fp = inp.get("file_path", "")
        if fp.endswith((".md", ".txt", ".tsv", ".yml", ".yaml", ".json")):
            textes_ecrits.append(inp.get("new_string", "") or inp.get("content", "") or json.dumps(inp.get("edits", []), ensure_ascii=False))
    elif nom in ("Agent", "Workflow", "SendMessage"):
        p = json.dumps(inp, ensure_ascii=False)
        # R4 : lancer un sous-agent sur un arbre
        if nom in ("Agent", "Workflow") and re.search(r"/home/user/shogen|dépôt|depot|worktree|git archive|\.git\b", p):
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+(status|log)\b"):
                refuser("R4 : lancer un sous-agent sur un arbre git exige l'état de cet arbre lu avant (git status ou git log).")
        # R9 (E27) : seuil de coût
        n = 1 if nom == "Agent" else agents_du_workflow(inp) if nom == "Workflow" else 0
        vivants = agents_vivants(entree) if n else 0
        if n is None or (nom == "Workflow" and n > SEUIL_WORKFLOW) or vivants + (n or 0) > SEUIL_VIVANTS:
            tp = entree.get("transcript_path") or ""
            session = entrees if chemin == tp else lire_queue(tp)
            if not any(JETON.search(t) for t in tour_humain(session or [])[1]):
                lances = "nombre d’agents illisible" if n is None else f"{n} agent(s) lancé(s)"
                refuser(f"R9 (E27) : seuil de coût : {lances}, {vivants} vivant(s) (seuils : {SEUIL_WORKFLOW} par "
                        f"workflow, {SEUIL_VIVANTS} vivants) ; faire en direct, ou attendre le jeton FANOUT-AUTORISE "
                        "écrit par l'investisseur dans son message.")
        textes_ecrits.append(p)
    elif nom.startswith("mcp__github__") and nom.split("__")[-1] in ("create_pull_request", "add_issue_comment", "update_pull_request", "pull_request_review_write", "add_reply_to_pull_request_comment"):
        o, r = inp.get("owner", ""), inp.get("repo", "")
        if nom.endswith("__create_pull_request") and not forge_lance(entrees, o, r):
            refuser(f"R8 (E20) : aucune preuve que la forge lance des jobs sur {o}/{r} (dépôt privé : runner_id 0, "
                    "échec en 2 s) ; lire mcp__github__actions_list de ce dépôt (un run conclu success, un job à "
                    "runner_id non nul), ou écrire après constat la ligne owner/repo AAAA-MM-JJ du jour dans "
                    "scripts/controle/garde/forge-actions.txt.")
        textes_ecrits.append(json.dumps(inp, ensure_ascii=False))

    # R5 : identifiants de commit et numéros de PR écrits
    if textes_ecrits:
        hexs, prs = identifiants_affiches(faits, humain)
        for txt in textes_ecrits:
            for h in HEX_ID.findall(txt):
                if est_identifiant_commit(h) and not hex_affiche(h, hexs):
                    refuser(f"R5 : l'identifiant « {h} » n'a été affiché par aucun outil dans le journal de cet agent ; lis-le (git log) avant de l'écrire.")
            for p in PR_NUM.findall(txt):
                if p not in prs:
                    refuser(f"R5 : le numéro de PR « {p} » n'a été affiché par aucun outil dans le journal de cet agent ; lis-le avant de l'écrire.")
    return 0


def formes_nombre(s):
    """Lectures possibles d'un nombre écrit : la virgule est un séparateur de milliers (1,715 → 1715) ou une
    décimale (0,901 → 0.901) ; les deux formes sont rendues, il suffit qu'une soit affichée."""
    s = re.sub(r"[   ]", "", s)
    formes = {s.replace(",", ".")}
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):
        formes.add(s.replace(",", ""))
    return formes


def normaliser_nombre(s):
    return min(formes_nombre(s))


def stop(entree, sous_agent):
    if entree.get("stop_hook_active"):
        return 0
    chemin, dossier = journal_de_l_agent(entree)
    entrees = lire_queue(chemin)
    if not entrees:
        return 0
    faits, appels, agent, humain = faits_et_appels(entrees)
    if not agent:
        return 0
    dernier = agent[-1]
    # identifiant du tour : uuid de la dernière entrée assistant
    uuid = next((e.get("uuid") for e in reversed(entrees) if e.get("type") == "assistant"), "sans-uuid")
    corpus = "\n".join(faits + humain)
    corpus_norm = set()
    for m in NOMBRE.findall(corpus):
        corpus_norm |= formes_nombre(m)
    corpus_plat = re.sub(r"[   ,]", "", corpus)
    manquants = []
    for m in NOMBRE.findall(dernier):
        fs = formes_nombre(m)
        if fs & corpus_norm or any(f.replace(".", "") in corpus_plat for f in fs) or m in corpus:
            continue
        manquants.append(m)
    for m in NOMBRE_UNITE.findall(dernier):
        if re.search(r"(?<![\d.,])" + m + r"(?![\d])", corpus) or m in manquants:
            continue
        manquants.append(m)
    if not manquants:
        return 0
    etat = os.path.join(dossier, "garde-faits.etat")
    deja = ""
    try:
        with open(etat, encoding="utf-8") as f:
            deja = f.read().strip()
    except OSError:
        pass
    if deja == uuid:
        journaliser(dossier, f"PASSAGE consigné au second arrêt ({'sous-agent' if sous_agent else 'agent'} {entree.get('agent_id', '')}) : nombres non affichés {manquants[:8]}")
        return 0
    try:
        with open(etat, "w", encoding="utf-8") as f:
            f.write(uuid)
    except OSError:
        pass
    journaliser(dossier, f"REFUS Stop ({'sous-agent' if sous_agent else 'agent'} {entree.get('agent_id', '')}) : {manquants[:8]}")
    sys.stderr.write(f"{MARQUE} : REFUS. R6 : le dernier texte porte des nombres qu'aucun outil n'a affichés : {', '.join(manquants[:8])}. Lis-les par un outil, ou retire-les.\n")
    return 2


def main():
    try:
        entree = json.load(sys.stdin)
    except Exception:
        return 0
    ev = entree.get("hook_event_name", "")
    dossier = os.path.dirname(entree.get("transcript_path") or "") or "."
    try:
        if ev == "PreToolUse":
            return pre_tool_use(entree)
        if ev in ("Stop", "SubagentStop"):
            return stop(entree, ev == "SubagentStop")
    except SystemExit as e:
        if e.code == 2:
            journaliser(dossier, f"REFUS {ev} {entree.get('tool_name', '')} agent={entree.get('agent_id', '')}")
        raise
    except Exception as exc:  # jamais un refus aveugle
        sys.stderr.write(f"{MARQUE} : erreur interne ({exc!r}) ; acte permis sans contrôle.\n")
        journaliser(dossier, f"ERREUR {ev} {exc!r}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
