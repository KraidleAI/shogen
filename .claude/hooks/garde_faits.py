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

Règles PreToolUse (R1 à R5, R11) :
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
     l'agent et les refus de ce crochet ne comptent pas. Dans un brief (fichier BRIEF*.md écrit par Write, Edit,
     MultiEdit ou une redirection du shell), chaque compte à unité (N tests, N fichiers, N lignes, N mutants, N cas,
     N commits, N diffs, N gardes, N items, en chiffres ou de deux à douze en lettres ; Ran N) doit avoir été affiché
     avec la même unité (E7) ; un compte précédé d'une borne (≤, au plus, moins de, chacun…) n'est pas jugé ; un
     nombre affiché seul (ou suivi d'un nom) par une commande de comptage (wc, grep -c) vaut pour toute unité
     (relecture G2 du groupe A, C-6 : un compte lu par grep -c ou wc -l est un compte lu).
  R11 lancer un sous-agent ou un workflow dont la consigne nomme un fichier BRIEF*.md : le brief passe
     scripts/controle/avant_acte.py brief (items de l'annexe B, E6 ; constats relayés, E22 ; faisabilité, E23 ;
     règle git, E24), avec --fiche <subagent_type> si la fiche existe ; brief absolu absent : refus ; erreur de
     l'outil (sortie 3, délai) : acte permis, note sur stderr (lot GARDE-FOUS-ORCH, phase 2, groupe A) ; une consigne
     (prompt) de plus de CONSIGNE_MAX caractères qui ne nomme aucun BRIEF*.md : refus, le brief s'écrit dans un
     fichier (relecture G2 du groupe A, C-5 : une consigne en ligne échappait à B1-B4).
Crochets Stop et SubagentStop (R6) : le dernier texte de l'agent ne porte aucun nombre de trois chiffres ou plus (ni, E29, aucun
nombre d'un ou deux chiffres suivi d'une unité ou d'une grandeur de la feuille de route : jours, semaines, %, observateurs, …),
ni décimal, qu'aucun outil n'a affiché (séparateurs de milliers admis : 1 715, 1,715, 1 715). Au second arrêt
du même tour, laisser passer et le consigner (fichier d'état sous le dossier de la session).
Journal des décisions : <dossier de session>/garde-faits.log (une ligne par refus et par passage consigné).
Sortie : 0 permis ; 2 refusé ; journal illisible ou erreur interne : voir SHOGEN-GARDE-ERREUR-INTERNE-1 en fin de texte.
Acte lu, non texte (phase 2, SHOGEN-GARDE-CROCHET-ACTE-1, LN-6) : R1, R2, R3 et le texte de R5 se lisent sur les actes
de la commande (acte_shell.py, voisin : rm récursif, git worktree remove, redirections, tee, sed -i, open en écriture
d'un code python, git commit et push, gh et curl vers la forge) ; un commit cité dans un heredoc ou un argument n'en est
pas un ; R5 lit le message de git commit (-m, et le fichier de -F). Commande illisible par shlex : motifs (sens sûr).
G2, C-2 : un acte dont le programme (ou l'argument d'eval) porte $ ou `, ou un code python qui lance un processus
(subprocess, os.system, os.popen, os.exec*, os.spawn*, pty.spawn), est jugé aussi par les motifs d'avant (sens sûr).
R7 (E18, E28) : refus d'un sleep d'avant-plan (hors boucle until, hors arrière-plan : &, run_in_background) et d'un
pkill -f ou pgrep -f dont le motif ne commence pas par ^ (le shell qui le lance porte le motif : il se reconnaît).
G2, C-3 (L-3 adjugée) : une boucle while ou until à condition de sortie admet son sleep comme until ; une boucle à
condition constante (while true, while :, until false) ne l'admet que si la commande porte break, exit ou return.
R8 (E20) : create_pull_request refusé sans preuve que la forge lance des jobs sur ce dépôt : au journal, un résultat
de mcp__github__actions_* (ou de gh run, gh api) du même owner/repo qui montre un run conclu success ou un job à
runner_id non nul ; ou, au marqueur scripts/controle/garde/forge-actions.txt, la ligne owner/repo AAAA-MM-JJ du jour
(date -u), écrite après constat.
G2, C-4 : la ligne du marqueur porte l'identifiant du run lu (owner/repo AAAA-MM-JJ <id>) ; elle ne vaut que si cet
identifiant figure dans une preuve du même dépôt (résultat ci-dessus) d'un journal de la session (journal principal ou
subagents/agent-*) : un marqueur écrit sans lecture de la forge, ou sans identifiant, ne vaut rien.
R9 (E27) : seuil de coût avant Agent et Workflow : refus d'un workflow de plus de SEUIL_WORKFLOW agents (appels agent(
du script ; nombre inconnu, boucle qui les multiplie : refus), ou d'un lancement qui porterait les sous-agents vivants
(journal touché depuis VIVANT_S s) au-delà de SEUIL_VIVANTS ; sauf jeton FANOUT-AUTORISE (ou les mots fan out) écrit
par l'humain dans son dernier message (journal de la session, jamais un résultat d'outil). G2, C-7 : les mots fan out
ne valent jeton que dans une phrase sans négation (pas, ne, non, sans, jamais, aucun, interdit, no, not, never…).
R10 (E26) : UserPromptSubmit relève les noms propres du message (capitale hors début de phrase et mots courants,
capitales internes, sigles, domaine d'un courriel) au JOURNAL et dans docs/publication/ (chemin:N: ligne), l'affiche
en contexte et le garde (garde-faits.releve) ; au Stop, si le dernier message de l'humain porte un nom propre, une
réponse qui nomme un dossier de DOSSIERS absent du message et de tout fait du tour (résultat d'outil, relevé) est
refusée une fois (stop_hook_active : passage consigné). G2, C-5 : DOSSIERS se lit dans le fichier versé
scripts/controle/garde/dossiers.txt (un nom par ligne, # : commentaire) ; absent ou vide : R10 ne refuse rien.
Phase 3 (journal des refus, SHOGEN-GARDE-FOUS-ORCH-1) : chaque refus et chaque passage écrit une ligne au journal
scripts/controle/garde/refus.tsv (consigner : heure, événement, règle ou permis, acte abrégé sans secret, agent) ; au
premier message d'une session, UserPromptSubmit affiche les refus depuis le dernier relevé (releve_refus).
SHOGEN-GARDE-ERREUR-INTERNE-1 (GARDE-FOUS phase 3, groupe B ; G2 du correctif CQ-1, C-1) : sens sûr par règle. Une
erreur interne, ou un journal illisible, pendant le jugement d'un acte qui écrit, commet, pousse, supprime ou crée une
PR (R1 à R3, R5, R8 : tout PreToolUse hors lecture pure) est un refus qui nomme l'erreur ; une lecture pure
(lecture_pure : commandes simples de LECTURE, git en GIT_LECTURE, sans redirection d'écriture, substitution,
affectation ni $ sur git ; outils mcp__github__ get_, list_, search_) reste permise, l'erreur écrite sur stderr et au
journal des décisions ; Stop, SubagentStop et UserPromptSubmit : permis, erreur écrite (ni écriture ni acte).
R12 (E29, SHOGEN-GARDE-REPONSE-INVESTISSEUR-1), Stop seul : chaque nombre à unité de la réponse (texte de l'agent après
son dernier appel d'outil ; unités de R12_NOMBRE) doit être porté, avec une forme de son unité (R12_FORMES, française
ou anglaise) sur la même ligne, par un résultat d'outil ou une pièce jointe du tour, ou par le message de l'humain qui
l'ouvre ; fenêtre : depuis le dernier message de l'humain (tour_humain). Sinon refus qui nomme le nombre et demande la
lecture de la pièce ; au second arrêt du tour (stop_hook_active), passage consigné. R6 n'est pas modifiée."""
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from urllib.parse import urlsplit

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
NOMBRES = {"deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
           "onze": 11, "douze": 12}
UNITES = {"file": "fichier", "line": "ligne", "case": "cas", "cas": "cas"}
COMPTE = re.compile("(?i)(?<![0-9A-Za-zà-ÿ.,/-])([0-9]+|" + "|".join(NOMBRES) + ") (tests?|fichiers?|files?|lignes?"
                    "|lines?|mutants?|cas|cases?|commits?|diffs?|gardes?|items?)(?![A-Za-zà-ÿ])"
                    "|(?<![A-Za-z])Ran ([0-9]+)(?![0-9])")
COMPTEUR = re.compile(r"\bwc\b|\bgrep\b[^|;&]*\s-[A-Za-z]*c")      # commandes de comptage (C-6)
NU = re.compile(r"^ *(?:[^ :]+:)?([0-9]+)(?: +[^ ]+)? *$", re.M)      # ligne de wc ou de grep -c : N, N nom, nom:N
BORNE = re.compile("(?i)(?:≤|≥|<|>|au plus|au moins|moins de|plus de|jusqu'à|jusqu’à|maximum|minimum|chacun) ?$")
BRIEF_NOMME = re.compile("(?:[^ " + chr(9) + chr(10) + "\"'`<>|;,()]*/)?BRIEF[^ " + chr(9) + chr(10) + "\"'`<>|;,()/]*[.]md")
CONSIGNE_MAX = 1500       # caractères d'une consigne sans fichier BRIEF*.md au-delà desquels R11 refuse (C-5)
OUTILS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))      # racine du dépôt du crochet
GIT_CMD = re.compile(r"\bgit(?:\s+(?:-C\s+\S+|--no-optional-locks|--git-dir=\S+|--work-tree=\S+))*\s+(\w[\w-]*)")
PY_PROCESSUS = re.compile(r"\b(subprocess|os\s*\.\s*(system|popen|exec\w*|spawn\w*|posix_spawn\w*)|pty\s*\.\s*spawn)\b")


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
NEGATION = re.compile(r"\b(pas|ne|non|sans|jamais|aucune?|interdite?s?|no|not|never|without|don't)\b|\bn'", re.I)
COMMUNS = {"le", "la", "les", "un", "une", "je", "tu", "il", "elle", "nous", "vous", "bonjour", "merci", "salut", "oui",
           "non", "cordialement", "hello", "hi", "dear", "thanks", "thank", "best", "regards", "the", "this", "we",
           "our", "utc", "api", "url", "pr", "ok", "json", "ci", "pdf", "http", "https", "readme"}
NOM_PROPRE = re.compile(r"(?<![\w@./-])([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+|[A-Z]{3,}[0-9]*|[A-ZÀ-Ý][a-zà-ÿ]{2,})"
                        r"(?![\w-])")
RAPPEL = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
FORGE_HOTE = re.compile(r"(?i)(?<![\w-])api\.github\.com(?![\w-])")     # hôte de la forge dans le texte (sens sûr)
ENTETE_REFUS = chr(9).join(["heure", "evenement", "regle", "acte", "agent"]) + chr(10)
REGLE = ["permis"]         # règle du refus en cours (phase 3, journal des refus) : posée par refuser et par juger
CLE_SECRETE = re.compile("(?i)((?:api[_-]?key|secret|token|passw(?:or)?d|authorization|bearer)[^ =:]*[ ]*[=:]?[ ]*"
                         "(?:(?:bearer|basic|token) )?)([^ '" + chr(34) + "]+|'[^']*'|" + chr(34) + "[^" + chr(34) + "]*"
                         + chr(34) + ")")
JETON_SECRET = re.compile("(?<![A-Za-z0-9_+/=-])(?:(?=[A-Za-z0-9_+/=-]*[0-9])(?=[A-Za-z0-9_+/=-]*[a-z])"
                          "(?=[A-Za-z0-9_+/=-]*[A-Z])[A-Za-z0-9_+/=-]{24,}|(?:sk-|ghp_|gho_|github_pat_|xox[baprs]-|AIza"
                          "|AKIA)[A-Za-z0-9_-]{8,})")
MOT_DE_PASSE = re.compile("(?i)(?<![a-z0-9+.-])([a-z][a-z0-9+.-]*://[^/ :@]*:)[^/ @]+(?=@)"      # URL user:mot@hôte
                          "|(?<![^ ])((?:-u|--user)[ =]?[^ :]*:)[^ ]+")      # curl -u user:mot (G2 du groupe C, C-2)
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
            c = (e.get("message") or {}).get("content")     # SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1 : chaîne ou liste
            for b in [c] if isinstance(c, str) else c or []:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    txt = contenus(b)
                    if MARQUE not in txt:
                        faits.append(txt)
                elif MARQUE not in contenus(b):      # refus du crochet : jamais un texte humain (R5 ; G2 B, C-2)
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
    REGLE[0] = (re.match("R[0-9]+", motif) or ["?"])[0]
    sys.stderr.write(f"{MARQUE} : REFUS. {motif}\n")
    sys.exit(2)


def journaliser(dossier, ligne):
    try:
        with open(os.path.join(dossier, "garde-faits.log"), "a", encoding="utf-8") as f:
            f.write(ligne.rstrip("\n") + "\n")
    except OSError:
        pass


def abreger(texte):
    """Acte abrégé du journal des refus : blancs réduits (ni tabulation ni saut de ligne), secrets masqués (***),
    80 caractères au plus (le masque passe avant la coupe) ; mot de passe d'une URL et de curl -u masqué (G2, C-2)."""
    t = CLE_SECRETE.sub(lambda m: m[1] + "***", " ".join(str(texte).split()))
    t = MOT_DE_PASSE.sub(lambda m: (m[1] or m[2]) + "***", t)
    return JETON_SECRET.sub("***", t)[:80]


def chemin_refus():
    """Journal des refus (phase 3) : SHOGEN_GARDE_REFUS si posé (les tests le posent ; /dev/null : éteint), sinon
    scripts/controle/garde/refus.tsv du dépôt du crochet (non versionné : .gitignore du dossier)."""
    return os.environ.get("SHOGEN_GARDE_REFUS") or os.path.join(RACINE, "scripts", "controle", "garde", "refus.tsv")


def consigner(entree, regle, acte="-"):
    """Phase 3 : une ligne au journal des refus (heure lue par date -u, événement, règle ou permis, erreur, releve,
    acte abrégé, agent) ; en-tête posé par lien d'un fichier complet (jamais deux, jamais à demi), ligne ajoutée d'un
    seul write en O_APPEND (atomique entre crochets concurrents) ; dossier absent, erreur, chemin en .jsonl : rien,
    jamais un refus."""
    try:
        chemin = chemin_refus()
        if chemin.endswith(".jsonl"):
            return
        heure = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True, timeout=10).stdout
        ev = entree.get("hook_event_name", "") + (":" + entree["tool_name"] if entree.get("tool_name") else "")
        champs = [heure, ev, regle, abreger(acte), entree.get("agent_id") or "principal"]
        ligne = chr(9).join(" ".join(str(x).split()) or "-" for x in champs) + chr(10)
        if not os.path.exists(chemin):
            tmp = f"{chemin}.{os.getpid()}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(ENTETE_REFUS)
            try:
                os.link(tmp, chemin)
            except FileExistsError:
                pass
            finally:
                os.unlink(tmp)
        fd = os.open(chemin, os.O_WRONLY | os.O_APPEND)
        try:
            os.write(fd, ligne.encode("utf-8"))
        finally:
            os.close(fd)
    except Exception:
        pass


def lire_tete(chemin):
    """Entrées JSON du journal de session, lues une à une depuis son début (releve_refus, G2 du groupe C, C-3 : le
    premier message de l'humain est en tête ; la queue d'un journal de plus de QUEUE octets ne le porte plus)."""
    try:
        with open(chemin, "rb") as f:
            for ligne in f:
                try:
                    yield json.loads(ligne)
                except ValueError:
                    continue
    except OSError:
        return


def releve_refus(entree):
    """Phase 3 : au premier message d'une session (aucun autre message de l'humain à son journal), ligne du relevé :
    refus du journal depuis la dernière ligne releve, par règle ; une ligne releve est écrite ; sinon None (journal
    éteint, /dev/null, compris). G2, C-3 : journal de session lu depuis sa tête (lire_tete) ; journal des refus absent
    ou non écrit après la ligne releve : le relevé le dit, jamais « 0 refus »."""
    prompt = (entree.get("prompt") or "").strip()
    if chemin_refus() == os.devnull:
        return None
    for e in lire_tete(entree.get("transcript_path") or ""):
        c = (e.get("message") or {}).get("content") if e.get("type") == "user" and not e.get("isMeta") else None
        blocs = [c] if isinstance(c, str) else [b for b in c or [] if isinstance(b, dict) and b.get("type") == "text"]
        txt = RAPPEL.sub("", chr(10).join(contenus(b) for b in blocs)).strip()
        outils = isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c)
        if txt and txt != prompt and MARQUE not in txt and not outils:
            return None
    try:
        with open(chemin_refus(), "rb") as f:
            f.seek(0, 2)
            n = f.tell()
            f.seek(max(0, n - QUEUE))
            brut = f.read().decode("utf-8", "replace").split(chr(10))[1 if n > QUEUE else 0:]
    except OSError:
        brut = []
    lignes = [x.split(chr(9)) for x in brut if x.count(chr(9)) == 4]
    k = max((i for i, x in enumerate(lignes) if x[2] == "releve"), default=-1)
    refus = [x[2] for x in lignes[k + 1:] if re.fullmatch("R[0-9]+", x[2])]
    regles = sorted(set(refus), key=lambda r: (-refus.count(r), int(r[1:])))
    consigner(entree, "releve", f"{len(refus)} refus")
    if not os.path.isfile(chemin_refus()):
        return (f"RELEVÉ DES REFUS (crochet du dépôt, phase 3) : journal {chemin_refus()} absent ou non écrit : aucun "
                "refus relevé")
    return (f"RELEVÉ DES REFUS (crochet du dépôt, phase 3) : {len(refus)} refus depuis "
            + (f"le dernier relevé ({lignes[k][0]})" if k >= 0 else "le début du journal")
            + (" : " + ", ".join(f"{r} ×{refus.count(r)}" for r in regles) if regles else "")
            + " ; détail : python3 -I -B scripts/controle/avant_acte.py refus"
            + (f" --depuis {lignes[k][0][:10]}" if k >= 0 else ""))


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


def hote_forge(mots):
    """Vrai si un mot de la commande vise l'API de la forge : URL dont l'hôte, lu par urlsplit (jamais par sous-chaîne),
    est api.github.com (schéma en toute casse, point final admis) ; mot sans schéma dont l'hôte est api.github.com (curl
    le lit en http) ; URL que urlsplit refuse (ValueError : sens sûr, jamais une erreur interne). Une URL d'un autre hôte
    dont le chemin, la requête ou un sous-domaine porte « api.github.com » ne compte pas."""
    for x in mots:
        if re.match(r"(?i)https?://", x):
            try:
                h = urlsplit(x).hostname or ""
            except ValueError:
                return True
        else:
            h = re.sub(r":[0-9]*$", "", re.split(r"[/?#]", x, maxsplit=1)[0].rsplit("@", 1)[-1]).lower()
        if h.rstrip(".") == "api.github.com":
            return True
    return False


def faits_de_la_commande(c, cwd, fond=False):
    """Ce que fait la commande : rm (cibles d'un rm récursif), worktree (git worktree remove), ecrit (fichiers écrits),
    git (sous-commandes), messages (textes que R5 juge pour un commit), forge (gh, curl vers l'API). Lu sur les actes
    (LN-6) ; par les motifs d'avant si shlex ne lit pas la commande (sens sûr)."""
    actes = AS.analyser(c, fond) if AS else None
    g = GIT_CMD.search(c)
    motifs = {"rm": [m.group(2) for m in RM.finditer(c)] if re.search(r"\brm\s+-[a-zA-Z]*[rR]", c) else [],
              "worktree": "git worktree remove" in c, "git": {g.group(1)} if g else set(), "messages": [c],
              "ecrit": [m.group(3) for m in REDIR.finditer(c)] + [m.group(2) for m in SED_I.finditer(c)]
              + PY_W.findall(c),
              "forge": bool(re.search(r"\bgh\s+pr\s+(create|comment|review|merge)|pull_request", c)), "actes": None}
    if actes is None:
        return motifs
    # G2, C-2 : acte non lisible sur ses mots (programme ou argument d'eval portant $ ou `, code python qui lance un
    # processus) : les motifs d'avant jugent aussi la commande, en plus des actes (sens sûr)
    douteux = any(re.search("[$`]", a["prog"]) or a["prog"] == "eval" and re.search("[$`]", " ".join(a["mots"][1:]))
                  or any(PY_PROCESSUS.search(code) for code in a["python"]) for a in actes)
    f = {"rm": [], "worktree": False, "git": set(), "messages": [], "ecrit": [], "forge": False}
    f = {k: (type(v)(motifs[k]) if douteux else v) for k, v in f.items()}
    f["actes"] = actes
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
        elif p == "gh" and m[1:2] in (["pr"], ["issue"], ["api"], ["release"]) or p == "curl" and (
                hote_forge(m) or any(re.search("[$`]", x) for x in m[1:]) and FORGE_HOTE.search(c)):
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


def preuves_forge(entrees, cible):
    """Résultats d'outil du journal qui montrent, pour cible (owner/repo), un run conclu success ou un job à runner_id
    non nul (outil mcp__github__actions_* du même dépôt, ou gh run, gh api qui le nomme)."""
    out = []
    for nom, inp, txt in appels_resultats(entrees):
        if MARQUE in txt or not FORGE_JOB.search(txt):
            continue
        depot = f"{inp.get('owner', '')}/{inp.get('repo', '')}".casefold()
        c = inp.get("command", "") if nom == "Bash" else ""
        if nom.startswith("mcp__github__actions_") and depot == cible or re.search(r"\bgh\s+(run|api)\b", c) and (
                cible in c.casefold()):
            out.append(txt)
    return out


def forge_lance(entrees, owner, repo, entree):
    """Vrai si le journal de l'agent, ou le marqueur du jour adossé à une preuve d'un journal de la session, montre que
    la forge lance des jobs sur owner/repo (R8, E20 ; G2, C-4)."""
    cible = f"{owner}/{repo}".casefold()
    if preuves_forge(entrees, cible):
        return True
    marqueur = lire_texte(os.path.join(RACINE, "scripts", "controle", "garde", "forge-actions.txt"))
    lignes = [x.split() for x in marqueur.casefold().split("\n") if x.strip() and not x.startswith("#")]
    ids = {x[2] for x in lignes if len(x) == 3 and x[2].isdigit() and x[:2] == [cible, jour_utc()]}
    tp = entree.get("transcript_path") or ""
    d = os.path.join(tp[:-6] if tp.endswith(".jsonl") else os.path.dirname(tp), "subagents")
    try:
        journaux = [tp] + [os.path.join(d, x) for x in sorted(os.listdir(d)) if x.startswith("agent-")] if ids else []
    except OSError:
        journaux = [tp]
    return any(re.search(r"(?<![\w.])" + i + r"(?![\w.])", t) for j in journaux
               for t in preuves_forge(lire_queue(j) or [], cible) for i in ids)


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


def noms_propres(texte):
    """Noms propres d'un message, douze au plus : capitale hors début de phrase et hors COMMUNS, capitales internes
    (CoinGecko), sigles (MONARK), domaine d'une adresse (coingecko.com)."""
    t, out = RAPPEL.sub("", texte), []
    for m in NOM_PROPRE.finditer(t):
        avant, mot = t[:m.start()].rstrip(" \t\"'«(*"), m.group(1)
        simple = re.fullmatch(r"[A-ZÀ-Ý][a-zà-ÿ]+", mot)
        if not (simple and (not avant or avant[-1] in ".!?:\n")) and mot.casefold() not in COMMUNS and mot not in out:
            out.append(mot)
    return (out + [d for d in dict.fromkeys(re.findall(r"@([A-Za-z0-9-]+)[.]", t)) if d not in out])[:12]


def releve(noms):
    """Lignes du JOURNAL et des .md et .txt de docs/publication/ qui portent chaque nom (casse ignorée), cinq par
    nom."""
    sources = [os.path.join(RACINE, "JOURNAL.md")]
    for base, ds, fs in os.walk(os.path.join(RACINE, "docs", "publication")):
        ds[:] = sorted(ds)
        sources += [os.path.join(base, x) for x in sorted(fs) if x.endswith((".md", ".txt"))]
    out = []
    for nom in noms:
        vus = [f"{os.path.relpath(x, RACINE)}:{n}: {ligne.strip()[:200]}" for x in sources
               for n, ligne in enumerate(lire_texte(x).split("\n"), 1) if nom.casefold() in ligne.casefold()][:5]
        out += vus or [f"{nom} : aucune ligne au JOURNAL ni sous docs/publication/"]
    return out


def soumission(entree):
    """UserPromptSubmit (R10, E26) : relevé des noms propres du message, affiché en contexte et gardé ; sortie 0. Phase
    3 : au premier message d'une session, la ligne du relevé des refus (releve_refus) en dernier."""
    try:
        ligne = releve_refus(entree)
    except Exception:      # G2 du groupe C, C-3 : le relevé des refus ne fait jamais tomber le relevé E26
        ligne = None
    noms = noms_propres(entree.get("prompt") or "")
    if not noms:
        print(ligne or "", end=chr(10) if ligne else "")
        return 0
    texte = (f"RELEVÉ (crochet du dépôt, E26) : noms propres du message : {', '.join(noms)}. Avant de rattacher ce "
             "message à un dossier, lire ces lignes (grep -n) :\n" + "\n".join(releve(noms)))
    try:
        with open(os.path.join(os.path.dirname(entree.get("transcript_path") or "") or ".", "garde-faits.releve"), "w",
                  encoding="utf-8") as f:
            f.write(json.dumps(noms, ensure_ascii=False) + "\n" + texte)
    except OSError:
        pass
    print(texte + (chr(10) + ligne if ligne else ""))
    return 0


def dossiers():
    """Dossiers du projet (R10, E26 ; G2, C-5), lus dans scripts/controle/garde/dossiers.txt : un nom par ligne."""
    texte = lire_texte(os.path.join(RACINE, "scripts", "controle", "garde", "dossiers.txt"))
    return [x.strip() for x in texte.split("\n") if x.strip() and not x.lstrip().startswith("#")]


def dossiers_sans_releve(entree):
    """R10 (E26) : dossiers que le dernier texte du tour nomme sans relevé, si le message de l'humain porte un nom
    propre ; au second arrêt (stop_hook_active), passage consigné, rien rendu."""
    entrees = lire_queue(entree.get("transcript_path") or "") or []
    i, humains = tour_humain(entrees)
    noms = noms_propres("\n".join(humains)) if i is not None else []
    faits, _appels, agent, _humain = faits_et_appels(entrees[i + 1:] if noms else [])
    if not agent:
        return []
    garde = lire_texte(os.path.join(os.path.dirname(entree.get("transcript_path") or ""), "garde-faits.releve"))
    if garde.split("\n", 1)[0] == json.dumps(noms_propres(humains[0]), ensure_ascii=False):
        faits.append(garde)
    vus = "\n".join(faits + humains).casefold()
    manque = [d for d in dossiers() if re.search(r"(?<!\w)" + re.escape(d) + r"(?!\w)", agent[-1], re.I)
              and d.casefold() not in vus]
    if manque and entree.get("stop_hook_active"):
        journaliser(os.path.dirname(entree.get("transcript_path") or "") or ".",
                    f"PASSAGE R10 au second arrêt : {manque}")
        return []
    return manque


def jeton(texte):
    """Jeton du fan-out (R9, E27) : FANOUT-AUTORISE, ou les mots fan out dans une phrase sans négation (G2, C-7)."""
    return bool(re.search("FANOUT-AUTORISE", texte, re.I)) or any(
        JETON.search(p) and not NEGATION.search(p) for p in re.split(r"[.!?;\n]+", texte))


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
        if acte_qui_ecrit(entree):          # SHOGEN-GARDE-ERREUR-INTERNE-1 : sens sûr
            refuser(f"R0 (erreur interne) : journal illisible ({chemin}) : un acte qui écrit, commet, pousse, supprime "
                    "ou crée une PR ne se juge pas sans lui (R1 à R3, R5, R8) ; relire le chemin du journal, ou agir "
                    "par une lecture.")
        REGLE[0] = "erreur"          # journal des refus : lecture permise sans contrôle (CC de l'intégration P3, R-1)
        sys.stderr.write(f"{MARQUE} : journal illisible ({chemin}) ; lecture pure permise sans contrôle.\n")
        return 0
    faits, appels, agent, humain = faits_et_appels(entrees)
    cmds = commandes_git_recentes(appels)
    textes_ecrits = []     # textes où un identifiant écrit doit avoir été affiché (R5)
    briefs_ecrits = []     # textes de BRIEF*.md où un compte écrit doit avoir été affiché (R5, E7)

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
        if any(re.fullmatch("BRIEF.*[.]md", os.path.basename(x)) for x in fc["ecrit"]):
            briefs_ecrits.append(c)
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
        attente = "R7 (E18) : sleep d'avant-plan ; attendre par une boucle while ou until à condition de sortie (until "
        attente += "<condition>; do sleep N; done) "
        attente += "ou lancer en arrière-plan (run_in_background, ou commande suivie de &) et sonder."
        ancre = "R7 (E28) : pkill -f ou pgrep -f à motif non ancré, qui reconnaît le shell qui le lance ; ancrer par ^ "
        ancre += "(pgrep -f '^bash chaine_x.sh')."
        sortie = any(a["prog"] in ("break", "exit", "return") for a in fc["actes"] or [])
        for a in fc["actes"] or []:
            en_boucle = any(b in ("while", "until") or b.endswith("-sans-fin") and sortie for b in a["boucles"])
            if a["prog"] == "sleep" and not a["fond"] and not en_boucle:
                refuser(attente)
            if a["prog"] in ("pkill", "pgrep") and motif_non_ancre(a["mots"]):
                refuser(ancre)
        motifs = fc["actes"] is None            # commande illisible par shlex : motifs (sens sûr)
        if motifs and re.search(r"(^|[;&|(\s])sleep\s", c) and not re.search(r"\b(until|while)\b", c) and not inp.get(
                "run_in_background"):
            refuser(attente)
        if motifs and re.search(r"\bp(kill|grep)\s[^;&|]*-[a-zA-Z]*f", c) and not re.search(r"\s['\"]?\^", c):
            refuser(ancre)
    elif nom in ("Edit", "MultiEdit", "Write"):
        fp = inp.get("file_path", "")
        if fp.endswith((".md", ".txt", ".tsv", ".yml", ".yaml", ".json")):
            textes_ecrits.append(inp.get("new_string", "") or inp.get("content", "") or json.dumps(inp.get("edits", []), ensure_ascii=False))
            if re.fullmatch("BRIEF.*[.]md", os.path.basename(fp)):
                briefs_ecrits.append(textes_ecrits[-1])
    elif nom in ("Agent", "Workflow", "SendMessage"):
        p = json.dumps(inp, ensure_ascii=False)
        # R4 : lancer un sous-agent sur un arbre
        if nom in ("Agent", "Workflow") and re.search(r"/home/user/shogen|dépôt|depot|worktree|git archive|\.git\b", p):
            if not a_lu(cmds, r"\bgit(\s+(-C\s+\S+|--no-optional-locks))*\s+(status|log)\b"):
                refuser("R4 : lancer un sous-agent sur un arbre git exige l'état de cet arbre lu avant (git status ou git log).")
        if nom in ("Agent", "Workflow"):
            controler_briefs(inp, cwd)      # R11
        # R9 (E27) : seuil de coût
        n = 1 if nom == "Agent" else agents_du_workflow(inp) if nom == "Workflow" else 0
        vivants = agents_vivants(entree) if n else 0
        if n is None or (nom == "Workflow" and n > SEUIL_WORKFLOW) or vivants + (n or 0) > SEUIL_VIVANTS:
            tp = entree.get("transcript_path") or ""
            session = entrees if chemin == tp else lire_queue(tp)
            if not any(jeton(t) for t in tour_humain(session or [])[1]):
                lances = "nombre d’agents illisible" if n is None else f"{n} agent(s) lancé(s)"
                refuser(f"R9 (E27) : seuil de coût : {lances}, {vivants} vivant(s) (seuils : {SEUIL_WORKFLOW} par "
                        f"workflow, {SEUIL_VIVANTS} vivants) ; faire en direct, ou attendre le jeton FANOUT-AUTORISE "
                        "écrit par l'investisseur dans son message.")
        textes_ecrits.append(p)
    elif nom.startswith("mcp__github__") and nom.split("__")[-1] in ("create_pull_request", "add_issue_comment", "update_pull_request", "pull_request_review_write", "add_reply_to_pull_request_comment"):
        o, r = inp.get("owner", ""), inp.get("repo", "")
        if nom.endswith("__create_pull_request") and not forge_lance(entrees, o, r, entree):
            refuser(f"R8 (E20) : aucune preuve que la forge lance des jobs sur {o}/{r} (dépôt privé : runner_id 0, "
                    "échec en 2 s) ; lire mcp__github__actions_list de ce dépôt (un run conclu success, un job à "
                    "runner_id non nul), ou écrire après ce constat la ligne owner/repo AAAA-MM-JJ <id du run lu> "
                    "dans scripts/controle/garde/forge-actions.txt.")
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
    if briefs_ecrits:      # R5, comptes d'un brief (E7)
        vus = {(n, u) for txt in faits + humain for n, u, _x in comptes(txt, bornes=False)}
        nus = comptes_nus(entrees)
        for n, u, brut in [x for txt in briefs_ecrits for x in comptes(txt)]:
            if (n, u) not in vus and n not in nus:
                refuser(f"R5 : le compte « {brut} » du brief n'a été affiché par aucun outil, avec son unité, dans le journal de cet agent (E7) ; affiche-le (printf '%s {u}s' $(…), wc ou grep -c) avant de l'écrire.")
    return 0


def comptes(texte, bornes=True):
    """[(nombre, unité, texte écrit)] des comptes à unité (E7) ; bornes : les comptes précédés d'une borne écartés."""
    out = []
    for m in COMPTE.finditer(texte):
        if m[3] or not (bornes and BORNE.search(texte[max(0, m.start() - 12):m.start()])):
            unite = "test" if m[3] else m[2].lower()
            unite = UNITES.get(unite, UNITES.get(unite.rstrip("s"), unite.rstrip("s")))
            out.append((int(m[3] or NOMBRES.get(m[1].lower(), m[1])), unite, m[0]))
    return out


def comptes_nus(entrees):
    """Nombres affichés seuls sur leur ligne (ou suivis d'un nom, ou après nom:) par une commande de comptage (wc,
    grep -c) : comptes lus sans unité, admis pour toute unité (C-6, E7). Résultat apparié à sa commande par l'id."""
    ids, out = set(), set()
    for e in entrees:
        m = e.get("message")
        if e.get("type") not in ("assistant", "user") or not isinstance(m, dict) or not isinstance(m.get("content"), list):
            continue
        for b in m["content"]:
            if not isinstance(b, dict):
                continue
            entree = b.get("input") if isinstance(b.get("input"), dict) else {}
            if b.get("type") == "tool_use" and b.get("id") and COMPTEUR.search(str(entree.get("command", ""))):
                ids.add(b["id"])
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in ids and MARQUE not in contenus(b):
                out |= {int(x) for x in NU.findall(contenus(b))}
    return out


def controler_briefs(inp, cwd):
    """R11 : chaque fichier BRIEF*.md nommé par la consigne passe avant_acte.py brief (dépôt : CLAUDE_PROJECT_DIR)."""
    depot = os.environ.get("CLAUDE_PROJECT_DIR") or OUTILS
    acte = os.path.join(OUTILS, "scripts", "controle", "avant_acte.py")
    textes = "\n".join(v for v in inp.values() if isinstance(v, str))
    noms = sorted(set(BRIEF_NOMME.findall(textes)))
    consigne = inp.get("prompt") if isinstance(inp.get("prompt"), str) else ""
    if not noms and len(consigne) > CONSIGNE_MAX:
        refuser(f"R11 : consigne de {len(consigne)} caractères sans fichier BRIEF*.md (plus de {CONSIGNE_MAX}) : écris le "
                "brief dans un fichier BRIEF*.md, contrôlé par avant_acte.py brief (E6, E22, E23, E24), et nomme-le.")
    for nom_brief in noms:
        chemin = resoudre(nom_brief, cwd)
        if not os.path.isfile(chemin):
            if os.path.isabs(nom_brief):
                refuser(f"R11 : la consigne nomme un brief absent : {chemin} ; écris-le, ou corrige le chemin.")
            continue
        cmd = [sys.executable, "-I", "-B", acte, "--depot", depot, "brief", "--texte", chemin]
        fiche = inp.get("subagent_type") or ""
        if re.fullmatch("[a-z0-9-]+", fiche) and os.path.isfile(os.path.join(depot, ".claude", "agents", fiche + ".md")):
            cmd += ["--fiche", fiche]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired) as e:
            sys.stderr.write(f"{MARQUE} : R11 non contrôlé ({e!r}) ; acte permis.\n")
            continue
        if p.returncode == 1:
            refus = [x for x in p.stdout.splitlines() if x.startswith("REFUS")]
            refuser(f"R11 : le brief {chemin} échoue à avant_acte.py brief : " + " | ".join(refus[:6]))
        elif p.returncode:
            sys.stderr.write(f"{MARQUE} : R11 : avant_acte.py brief, sortie {p.returncode} ; acte permis.\n")


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


BLANC = "[ " + chr(0xa0) + chr(0x202f) + "]"        # espace, insécable, fine insécable (R12)
R12_NOMBRE = re.compile(r"(?<![\w.,:/-])(\d+(?:[.,]\d+)?)" + BLANC + "?(" + r"jours?|semaines?|mois|heures?|minutes?"
                        r"|années?|ans?|%|commits?|tests?|fichiers?)(?![A-Za-zà-ÿ])", re.I)
R12_FORMES = {"jour": "jours?|days?", "semaine": "semaines?|weeks?", "mois": "mois|months?", "heure": "heures?|hours?",
              "minute": "minutes?", "an": "ans?|années?|years?", "%": "%|pour ?cent|percent", "commit": "commits?",
              "test": "tests?", "fichier": "fichiers?|files?"}


def piece_porte(n, unite, lignes):
    """R12 : vrai si une ligne porte le nombre n (virgule ou point décimal) et une forme de son unité."""
    formes = {n, n.replace(",", "."), n.replace(".", ",")}
    r_n = re.compile(r"(?<![\w.,:/-])(?:" + "|".join(map(re.escape, formes)) + r")(?![\d]|[.,]\d)")
    r_u = re.compile(r"(?<![A-Za-zà-ÿ])(?:" + R12_FORMES[unite] + r")(?![A-Za-zà-ÿ])", re.I)
    return any(r_n.search(x) and r_u.search(x) for x in lignes)


def nombres_sans_piece(entree):
    """R12 (E29) : nombres à unité de la réponse du tour qu'aucune pièce du tour ne porte avec leur unité ; au second
    arrêt (stop_hook_active), passage consigné, rien rendu."""
    entrees = lire_queue(entree.get("transcript_path") or "") or []
    i, pieces = tour_humain(entrees)
    pieces, reponse = list(pieces), []
    for e in entrees[i + 1:] if i is not None else entrees:
        if e.get("type") == "attachment":
            pieces.append(contenus(e.get("attachment")))
        c = (e.get("message") or {}).get("content")
        for b in [b for b in (c if isinstance(c, list) else []) if isinstance(b, dict)]:
            if b.get("type") == "tool_result" and MARQUE not in contenus(b):
                pieces.append(contenus(b))
            elif b.get("type") == "tool_use":
                reponse = []
            elif b.get("type") == "text" and e.get("type") == "assistant":
                reponse.append(b.get("text", ""))
    lignes = "\n".join(pieces).split("\n")
    unite = lambda u: "an" if u in ("an", "ans") or u.startswith("ann") else u if u in ("%", "mois") else u.rstrip("s")  # noqa: E731
    nus = comptes_nus(entrees[i + 1:] if i is not None else entrees)      # comptes lus par wc, grep -c (G2, C-4)
    manque = list(dict.fromkeys(m[0] for m in R12_NOMBRE.finditer(RAPPEL.sub("", "\n".join(reponse)))
                                if not piece_porte(m[1], unite(m[2].lower()), lignes) and not (
                                    unite(m[2].lower()) in ("commit", "test", "fichier") and m[1].isdigit()
                                    and int(m[1]) in nus)))
    if manque and entree.get("stop_hook_active"):
        journaliser(os.path.dirname(entree.get("transcript_path") or "") or ".",
                    f"PASSAGE R12 au second arrêt : {manque[:8]}")
        return []
    return manque


LECTURE = {"cat", "head", "tail", "grep", "ls", "wc", "sha256sum", "cmp", "diff", "od", "stat", "pwd", "echo",
           "df", "du", "cut", "tr", "nl", "basename", "dirname", "realpath", "readlink", "true", "cd"}
GIT_LECTURE = {"status", "log", "diff", "show", "rev-parse", "ls-files", "ls-tree", "blame", "cat-file"}


def lecture_pure(c):
    """Vrai seulement si chaque commande simple de c est une lecture connue (SHOGEN-GARDE-ERREUR-INTERNE-1) : programme
    de LECTURE, ou git (options -C, --no-pager, --no-optional-locks) en GIT_LECTURE sans --output ni $ ; aucune
    redirection d'écriture (hors 2>&1 et vers /dev/null), substitution, affectation en tête. Découpe aux séparateurs
    avant shlex : un séparateur entre guillemets fait une commande illisible, donc pas une lecture (sens sûr). G2 du
    groupe B, C-1 : programme nommé sans chemin (./cat, /x/git : refus) ; >&N suivi d'un mot n'est pas un descripteur
    (>&1b écrit le fichier 1b) ; printf hors de LECTURE (printf -v affecte une variable, PATH compris)."""
    reste = re.sub(r"[0-9]?>&[0-9]+(?![^\s;&|])|[0-9]?>[ ]*/dev/null(?![^\s;&|])", "", c)
    if re.search(r"[>`]|\$\(|<\(", reste):
        return False
    for seg in re.split(r"&&|\|\||[;&|\n]", reste):
        mots = shlex.split(seg)
        if mots and "=" in mots[0]:
            return False
        if mots and mots[0] == "git":
            k = 1
            while mots[k:k + 1] and mots[k] in ("-C", "--no-pager", "--no-optional-locks"):
                k += 2 if mots[k] == "-C" else 1
            if not (mots[k:k + 1] and mots[k] in GIT_LECTURE) or "$" in seg or any(
                    m.startswith("--output") for m in mots):
                return False
        elif mots and mots[0] not in LECTURE:
            return False
    return True


def acte_qui_ecrit(entree):
    """Vrai sauf lecture pure (SHOGEN-GARDE-ERREUR-INTERNE-1) : un PreToolUse Bash dont la commande n'est pas une
    lecture_pure, tout autre outil que mcp__github__ get_, list_ ou search_ ; une erreur ici même : vrai (sens sûr)."""
    try:
        nom = entree.get("tool_name", "")
        if nom.startswith("mcp__github__"):
            return not nom.split("__")[-1].startswith(("get_", "list_", "search_"))
        return nom != "Bash" or not lecture_pure((entree.get("tool_input") or {}).get("command", ""))
    except Exception:
        return True


def main():
    """Phase 3 : chaque passage (permis, erreur) et chaque refus (règle) du crochet consigné au journal des refus."""
    try:
        entree = json.load(sys.stdin)
    except Exception:
        return 0
    acte = texte_appel(entree.get("tool_name") or "", entree.get("tool_input") if isinstance(entree.get(
        "tool_input"), dict) else {}) if entree.get("tool_name") else "-"
    try:
        code = juger(entree)
    except SystemExit as e:
        consigner(entree, REGLE[0] if e.code == 2 else "permis", acte)
        raise
    consigner(entree, REGLE[0] if code == 2 or REGLE[0] == "erreur" else "permis", acte)
    return code


def juger(entree):
    ev = entree.get("hook_event_name", "")
    dossier = os.path.dirname(entree.get("transcript_path") or "") or "."
    try:
        if ev == "PreToolUse":
            return pre_tool_use(entree)
        if ev == "UserPromptSubmit":
            return soumission(entree)
        if ev in ("Stop", "SubagentStop"):
            manque = dossiers_sans_releve(entree) if ev == "Stop" else []
            REGLE[0] = "R6"
            code = stop(entree, ev == "SubagentStop")
            if manque:
                REGLE[0] = "R10"
                sys.stderr.write(f"{MARQUE} : REFUS. R10 (E26) : la réponse nomme {', '.join(manque)} sans relevé du "
                                 "tour : relever d'abord les noms propres du message (grep -n <nom> JOURNAL.md "
                                 "docs/publication/), puis rattacher.\n")
                journaliser(dossier, f"REFUS Stop R10 : {manque}")
                code = 2
            sans = nombres_sans_piece(entree) if ev == "Stop" else []      # R12 (E29), jugée aussi après R6 ou R10 (G2, C-3)
            if sans:
                REGLE[0] = "R12"
                sys.stderr.write(f"{MARQUE} : REFUS. R12 (E29) : la réponse porte {', '.join(sans[:8])}, qu'aucun "
                                 "résultat d'outil ni pièce du tour ne porte avec son unité ; lire la pièce qui porte "
                                 "chaque nombre (Read, grep -n), puis répondre.\n")
                journaliser(dossier, f"REFUS Stop R12 : {sans[:8]}")
                return 2
            return code
    except SystemExit as e:
        if e.code == 2:
            journaliser(dossier, f"REFUS {ev} {entree.get('tool_name', '')} agent={entree.get('agent_id', '')}")
        raise
    except Exception as exc:  # SHOGEN-GARDE-ERREUR-INTERNE-1 : sens sûr par règle, jamais un refus aveugle
        if ev == "PreToolUse" and acte_qui_ecrit(entree):
            REGLE[0] = "R0"           # journal des refus : marque R0 (refus sur erreur interne ; intégration P3)
            sys.stderr.write(f"{MARQUE} : REFUS. erreur interne ({exc!r}) pendant le jugement d'un acte qui écrit, "
                             "commet, pousse, supprime ou crée une PR (R1 à R3, R5, R8) : acte refusé (sens sûr).\n")
            journaliser(dossier, f"REFUS {ev} {entree.get('tool_name', '')} erreur interne {exc!r}")
            return 2
        REGLE[0] = "erreur"
        sys.stderr.write(f"{MARQUE} : erreur interne ({exc!r}) ; lecture pure ou arrêt : permis, erreur écrite.\n")
        journaliser(dossier, f"ERREUR {ev} {exc!r}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
