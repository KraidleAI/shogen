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
Crochets Stop et SubagentStop (R6) : le dernier texte de l'agent ne porte aucun nombre de trois chiffres ou plus,
ni décimal, qu'aucun outil n'a affiché (séparateurs de milliers admis : 1 715, 1,715, 1 715). Au second arrêt
du même tour, laisser passer et le consigner (fichier d'état sous le dossier de la session).
Journal des décisions : <dossier de session>/garde-faits.log (une ligne par refus et par passage consigné).
Sortie : 0 permis ; 2 refusé ; 0 avec note sur stderr si le journal est illisible (jamais un refus aveugle)."""
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
LECTURE_SHELL = re.compile(r"\b(cat|tail|head|less|more|diff|grep|awk|sed\s+-n|git\s+show|sha256sum\s+-c|wc)\b")
REDIR = re.compile(r"(?<![<>])(>>?|\btee(?:\s+-a)?)\s+(?!&)(['\"]?)([^\s'\"|;&]+)\2")
SED_I = re.compile(r"\bsed\s+(?:-[a-zA-Z]*i[a-zA-Z]*\b[^|;]*?)\s+(['\"]?)([^\s'\"|;&]+)\1\s*(?:[;&|]|$)")
PY_W = re.compile(r"open\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"][wa]")
RM = re.compile(r"\brm\s+(?:-[a-zA-Z]*\s+)*(['\"]?)([^\s'\"|;&]+)\1")
GIT_CMD = re.compile(r"\bgit(?:\s+(?:-C\s+\S+|--no-optional-locks|--git-dir=\S+|--work-tree=\S+))*\s+(\w[\w-]*)")


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
        # R1 : effacer un worktree ou un clone
        cibles_rm = [resoudre(m.group(2), cwd) for m in RM.finditer(c)] if re.search(r"\brm\s+-[a-zA-Z]*[rR]", c) else []
        if "git worktree remove" in c or any(os.path.isdir(os.path.join(p, ".git")) or os.path.isfile(os.path.join(p, ".git")) for p in cibles_rm):
            if not a_lu(cmds, r"\bgit(\s+-C\s+\S+)?\s+status\b"):
                refuser("R1 : effacer un arbre git exige « git status » lu avant, dans les derniers appels de cet agent.")
            if not a_lu(cmds, r"\bgit(\s+-C\s+\S+)?\s+(log|rev-list)\b.*(origin/\S+\.\.|@\{u\}\.\.|--not\s+--remotes|\.\.HEAD)"):
                refuser("R1 : effacer un arbre git exige ses commits non poussés lus avant (git log origin/<branche>..HEAD).")
        # R2 : écrire dans un fichier existant par le shell
        cibles = [m.group(3) for m in REDIR.finditer(c)] + [m.group(2) for m in SED_I.finditer(c)] + PY_W.findall(c)
        for cib in cibles:
            if cib in ("/dev/null", "/dev/stderr", "/dev/stdout") or cib.startswith("&"):
                continue
            abs_c = resoudre(cib, cwd)
            if os.path.isfile(abs_c) and not fichier_lu_avant(abs_c, appels, cwd):
                refuser(f"R2 : écrire dans un fichier existant exige sa lecture avant (Read, cat, tail…) : {abs_c}")
            if os.path.isfile(abs_c) and abs_c.endswith((".md", ".txt", ".tsv", ".yml", ".yaml", ".json")):
                textes_ecrits.append(c)
        # R3 : commit et push
        g = GIT_CMD.search(c)
        sub = g.group(1) if g else ""
        if sub == "commit":
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+(status|diff)\b"):
                refuser("R3 : « git commit » exige le diff ou le status de l'arbre lu avant, dans les derniers appels de cet agent.")
            textes_ecrits.append(c)
        if sub == "push":
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+((log|rev-list)\b.*origin|status\b|ls-remote\b)"):
                refuser("R3 : « git push » exige ce qui part lu avant (git log origin/<branche>..HEAD, git status ou ls-remote).")
        if re.search(r"\bgh\s+pr\s+(create|comment|review|merge)|pull_request", c):
            textes_ecrits.append(c)
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
        textes_ecrits.append(p)
    elif nom.startswith("mcp__github__") and nom.split("__")[-1] in ("create_pull_request", "add_issue_comment", "update_pull_request", "pull_request_review_write", "add_reply_to_pull_request_comment"):
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
