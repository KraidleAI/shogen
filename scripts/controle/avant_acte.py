"""Contrôles avant l'acte de l'orchestrateur (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout GF-0 ;
adjudication de l'orchestrateur du 2026-10-10). Bibliothèque standard seule (R-8), Python 3.10 à 3.13.
Usage : python3 -I -B scripts/controle/avant_acte.py [--depot D] <sous-commande> [options] ; sortie 0 conforme, 1 refus
(une ligne REFUS <code> : <raison> ; à faire : <geste> par faute), 3 erreur (argument, fichier absent, git en erreur,
chemin interdit jamais ouvert) ; jamais 0 sur une erreur. Chaque passage ajoute au journal <git-path
shogen-garde>/journal.tsv (non versionné) une ligne par refus, avertissement ou contournement, ou une ligne conforme :
heure lue par date -u, sous-commande, code, niveau, contourne (moyen du contournement, sinon -) ; il mesure les refus
et les faux refus (avis b.5 adopté).
GF-5 : sceller, derrière la vérification complète (verif && sceller) : sha256 de HEAD et de l'arbre de l'index (git
write-tree), ou de HEAD^{tree} avec --tete ; refusé si un chemin diffère hors de l'index ou n'est pas suivi (LA-N05 :
pièce retouchée après la vérification). Le sceau est exigé par commit (GF-5b).
GF-5b : commit --message M --source S [--source S]... C1, sceau de l'index et de la tête présent (LA-N05) ; C2, pour
chaque source, une ligne Source-Sha: <sha256> du message égale à son sha256 au moment du commit, et aucune ligne
Source-Sha sans source égale (E8 : message écrit avant la clôture de la source, retouchée ensuite ; remplace la date de
fichier, avis c.2) ; C3, verdicts, nombres de passes, identifiants SHOGEN-…, G-n, C-n, R-n, Q-n, L-n, E-n, O-n, I-n
et sha courts du message (hors pieds Source-Sha, Diff-Id, Co-Authored-By, Claude-Session, Décalage admis) lus dans
les sources, un sha court absent des sources résolu par git (E8, LA-N03).
GF-6 : commit C4, heures du message et des lignes ajoutées des .md (E14) ; C5, citations des mêmes textes, forme
stricte refusée si fausse, autres formes en avertissement (E16) ; C6, --diff D... : HEAD plus les diffs nommés, dans
l'ordre, donne l'arbre de l'index (LA-N04) ; C7, aucun bloc ne décale une ligne existante d'un fichier de
garde/lignes-citees.txt, sauf ligne Décalage admis : <chemin> du message, journalisée en contournement (E21) ; C9,
--id ID : ligne Diff-Id: ID dans le message.
GF-6b : C8, un workflow touché : enforcement/workflows-yaml.py du dépôt lit les workflows de l'index (sortie 1 : refus ;
absent ou autre sortie : erreur ; E1). diff --fichier F, à la réception d'un diff de worker, avant la G2 (avis b.2) :
D1, fichier sous un interdit (ni lu ni nommé) ; D2, diff qui ne s'applique pas sur HEAD ; puis C4, C5 et presg5 (G5,
E9) sur les lignes ajoutées des .md, C7 (E21), C8 sur les workflows de HEAD plus le diff.
GF-7 : verser --pieces DOSSIER, avant xtask (E9, E10) : V0, fichier sous un interdit (ni lu ni nommé) ; V2, deux pièces
de même sha256, ou une pièce .md (500 caractères pliés ou plus) contenue en entier dans une autre ; V3, chemin absolu
du scratchpad ; V4, chaque SHA256SUMS rejoué par verifier() de enforcement/docs-sha256sums.py (forme de la gate),
présent à la racine du dossier, chaque pièce listée ; puis C4, C5 et presg5 (G5) sur les pièces .md entières.
GF-8 : pousser --distant NOM --branche B : P1, sceau de la tête (sceller --tete, LA-N05) ; P2, aucun chemin de
garde/hors-distant.txt changé entre NOM/B (ou l'arbre vide, branche neuve) et HEAD, jamais nommé (ADR-0028 l.293) ;
C8 sur les workflows de HEAD si la plage en touche. pousser --acte TEXTE : P4, acte sur la forge déjà refusé par le
mandataire (E17). publier --texte F : C4, C5, P5 motif de secret de enforcement/gate-secrets.sh (jamais recopié), V3
chemin absolu du scratchpad.
GF-8b : existe NOM, avant d'écrire qu'un fichier manque (E15) : chemins du dépôt (suivis et non suivis) qui portent ce
nom, hors interdits ; X1 si aucun. disque [--min-go N] [--lister D...] (E4) : DQ, refus sous 3 Gio libres sur /
(--min-go ne fait que serrer), avertissement sous 6 ; --lister : dossiers target qui portent CACHEDIR.TAG (cibles
cargo), à profondeur 4 au plus, sans entrer dans docs, .git, un lien ou un interdit, avec leur taille ; rien n'est
effacé.
GF-9b : chaine --plan P --cc RAPPORT [--duree-pas MIN] [--detache], avant de lancer une chaîne (E11, E25) : G1, le
rapport de contre-contrôle porte une seule ligne fixe GROUPES : (aucun, ou A+B ; C+D+E : diffs verts seulement
ensemble ; un nom seul ne groupe rien) ; G2, aucun pas du plan ne commet une partie d'un groupe sans le reste (diff
nommé par son fichier, sans .diff) ; G3, durée estimée (pas × durée mesurée d'un pas, 6 min par défaut) au-delà de
BORNE_LIEE min sans --detache : lancement lié refusé, lancement détaché donné.
GF-10b : toute exception d'une sous-commande sort en 3 (ligne ERREUR), jamais en 1, qui est un refus.
Relecture G2, C-2 : pousser P3, la branche poussée (refs/heads/B, que pousse git push NOM B) est HEAD.
Relecture G2, C-3 : diff lu comme git l'applique (format du diff indifférent : D1 sur les chemins de git apply
--numstat et des en-têtes, puis analyse de HEAD plus le diff par git diff -U0) ; citations (C5) et corpus de presg5
(G5) lus dans l'état d'après le diff.
Relecture G2, C-4 : pousser --acte ramène -XPUT, --method PUT et --method=PUT à -X PUT avant les motifs.
Relecture G2, C-6 : existe cherche le nom en toute casse, comme fichier ou comme dossier (imprimé avec sa barre).
Relecture G2, C-7 : chaine G1, chaque nom de GROUPES (hors la valeur aucun) nomme un diff du plan.
Relecture G2, C-8 : verser refuse /, le dépôt et ses ancêtres (erreur, aucun parcours), ne parcourt jamais un dossier
interdit (V0) et ne lit que des fichiers ordinaires (V5).
Relecture G2, C-9 : une exception du journal (après la sous-commande) sort en 3, jamais en 1.
Relecture G2, C-16 : C3 lit aussi dans les sources « passe N » (N passes faites), hors négation (sans, aucune, pas
de).
Relecture G2, C-17 : chaine G4, un Diff-Id du plan déjà porté par un commit d'un autre message est refusé (la reprise
du modèle sauterait le pas).
Relecture G2, C-18 : un module frère illisible (installation abîmée), une exception hors des sous-commandes ou l'échec
du vidage final de la sortie standard (tube sans lecteur) sortent en 3, jamais en 1 (un refus) ni en 120.
Contre-contrôle, R-2 : pousser P2 juge aussi chaque commit de la plage (git rev-list HEAD --not --remotes=NOM).
Contre-contrôle, R-3 : pousser --acte ramène aussi les guillemets du shell, les blancs répétés et les options de git
placées avant la sous-commande.
Contre-contrôle, R-4 : C7 refuse aussi le retrait ou le renommage d'un fichier cité."""
import argparse
import contextlib
import fnmatch
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile


def _module(nom, chemin=None):
    """Module chargé par son chemin (frère par défaut) : sous -I, le dossier du script n'est pas dans sys.path."""
    chemin = chemin or os.path.join(os.path.dirname(os.path.abspath(__file__)), nom + ".py")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


try:
    GC = _module("garde_commun")
    P5 = _module("presg5")
except Exception as _e:         # module frère illisible (installation abîmée) : erreur de l'outil, jamais 1 (C-18)
    print(f"ERREUR chargement : {type(_e).__name__} : {_e}", file=sys.stderr)
    sys.exit(3)
VERDICT = re.compile("(?<![A-Z-])(ACCEPTE-AVEC-CORRECTIONS|NON-CONFORME|CONFORME|ACCEPTE|REFUSE)(?![A-Z-])")
PASSES = re.compile("(?i)(?<![0-9a-zé])([0-9]+|une?|deux|trois|quatre|cinq|six) passes?(?![a-z])")
PASSE_N = re.compile("(?i)(?<![0-9a-zé])passe ([0-9]+)(?![0-9])")
NEGATION = re.compile("(?i)(?:sans|aucune|pas de|ni) (?:la |une )?$")
NOMBRES = {"un": "1", "une": "1", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6"}
IDENT = re.compile("(?<![A-Za-z0-9-])(SHOGEN-[A-Z0-9]+(?:-[A-Z0-9]+)*|[GCRQLEOI]-[0-9]+)(?![A-Za-z0-9-])")
SHA = re.compile("(?<![A-Za-z0-9-])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])([0-9a-f]{7,40})(?![A-Za-z0-9…-])")
PIEDS = ("Source-Sha:", "Diff-Id:", "Co-Authored-By:", "Claude-Session:", "Décalage admis :")
CITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "garde", "lignes-citees.txt")
HORS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "garde", "hors-distant.txt")
BORNE_LIEE = 100


class Erreur(Exception):
    """Erreur de l'outil : sortie 3, jamais un refus."""


def git(depot, *args, env=None):
    p = subprocess.run(["git", "-C", depot, "-c", "core.quotePath=false", *args], capture_output=True, text=True,
                       env=env)
    if p.returncode:
        raise Erreur(f"git {args[0]} : sortie {p.returncode}")
    return p.stdout


def garde(depot, *sous):
    """Dossier non versionné de l'état local (sceaux, journal), créé au besoin."""
    d = os.path.join(depot, git(depot, "rev-parse", "--git-path", "shogen-garde").strip(), *sous)
    os.makedirs(d, exist_ok=True)
    return d


def lire(chemin):
    """Octets d'un fichier qui n'est pas sous un interdit (sinon erreur, sans ouverture ni nom)."""
    if GC.chemin_interdit(chemin):
        raise Erreur("chemin interdit, non ouvert")
    with open(chemin, "rb") as f:
        return f.read()


def cle(depot, tete=False):
    """Clé du sceau : sha256 de HEAD et de l'arbre de l'index (git write-tree), ou de HEAD^{tree} avec --tete."""
    h = git(depot, "rev-parse", "--verify", "HEAD").strip()
    arbre = git(depot, *(["rev-parse", "HEAD^{tree}"] if tete else ["write-tree"])).strip()
    return hashlib.sha256(f"{'tete' if tete else 'index'} {h} {arbre}".encode()).hexdigest()


def sceller(a, fautes):
    etat = [x for x in git(a.depot, "status", "--porcelain", "--untracked-files=all").split(chr(10)) if x]
    hors = [x for x in etat if x[1] != " " or (a.tete and x[0] != " ")]
    if hors:
        fautes.append(("refus", "S1", f"{len(hors)} chemin(s) hors de l'index ou non suivi(s) (--tete : non commis)",
                       "indexer ou retirer, relancer la vérification complète, puis sceller", "-"))
        return
    with open(os.path.join(garde(a.depot, "sceaux"), cle(a.depot, a.tete)), "w", encoding="utf-8") as f:
        f.write(GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ") + chr(10))


def passes(texte, source=False):
    """Nombres de passes écrits (N passes) ; dans une source, aussi passe N hors négation (relecture G2, C-16)."""
    vus = {NOMBRES.get(n.lower(), n) for n in PASSES.findall(texte)}
    if source:
        vus |= {m[1] for m in PASSE_N.finditer(texte) if not NEGATION.search(texte[max(0, m.start() - 12):m.start()])}
    return vus


def resolu(depot, sha):
    return subprocess.run(["git", "-C", depot, "rev-parse", "--verify", "--quiet", sha + "^{commit}"],
                          capture_output=True).returncode == 0


def commit(a, fautes):
    texte, sources = lire(a.message).decode("utf-8"), [lire(s) for s in a.source]
    if not os.path.exists(os.path.join(garde(a.depot, "sceaux"), cle(a.depot))):
        fautes.append(("refus", "C1", "aucun sceau pour cet index et cette tête (LA-N05)",
                       "relancer la vérification complète puis sceller : <vérification> && avant_acte.py sceller", "-"))
    ecrits = set(re.findall("(?m)^Source-Sha: ([0-9a-f]{64})$", texte))
    reels = [hashlib.sha256(b).hexdigest() for b in sources]
    refaire = "relire la source finale et réécrire le message depuis elle, avec Source-Sha: <sha256 de la source>"
    for s, h in zip(a.source, reels):
        if h not in ecrits:
            fautes.append(("refus", "C2", f"aucune ligne Source-Sha au sha256 actuel de {os.path.basename(s)} (source "
                           "retouchée après le message, ou message écrit sans elle ; E8)", refaire, "-"))
    for h in sorted(ecrits - set(reels)):
        fautes.append(("refus", "C2", f"Source-Sha {h[:12]}… ne répond à aucune source : source retouchée", refaire,
                       "-"))
    corps = chr(10).join(x for x in texte.split(chr(10)) if not x.startswith(PIEDS))
    src = chr(10).join(b.decode("utf-8", "replace") for b in sources)
    manques = [("verdict", x) for x in sorted(set(VERDICT.findall(corps)) - set(VERDICT.findall(src)))]
    manques += [("nombre de passes", x) for x in sorted(passes(corps) - passes(src, source=True))]
    manques += [("identifiant", x) for x in sorted(set(IDENT.findall(corps)) - set(IDENT.findall(src)))]
    manques += [("sha court", x) for x in sorted(set(SHA.findall(corps))) if x not in src and not resolu(a.depot, x)]
    for genre, x in manques:
        fautes.append(("refus", "C3", f"{genre} du message absent des sources : {x} (E8)",
                       "reprendre les mots de l'adjudication et de la ligne d'annexe relues", "-"))
    fichiers, ecartes = GC.lignes_ajoutees(a.depot)
    if ecartes:
        fautes.append(("avertissement", "C4", f"{ecartes} fichier(s) indexé(s) sous un interdit, non lus", "", "-"))
    textes = [(f["apres"], place(f["ajouts"])) for f in fichiers if (f["apres"] or "").endswith(".md")]
    heures_et_citations(a.depot, [("message", texte)] + textes, fautes)
    if a.diff:
        diffs_nommes(a, fautes)
    cites(a.depot, texte, fichiers, fautes)
    workflows(a.depot, fichiers, fautes)
    if a.id and f"Diff-Id: {a.id}" not in texte.split(chr(10)):
        fautes.append(("refus", "C9", f"le message ne porte pas la ligne Diff-Id: {a.id}", "l'ajouter au message", "-"))


def place(ajouts):
    """Lignes ajoutées posées à leur numéro, les autres vides : chaque faute porte le vrai numéro de ligne."""
    lignes = [""] * max([n for n, _x in ajouts] or [0])
    for n, x in ajouts:
        lignes[n - 1] = x
    return chr(10).join(lignes)


def heures_et_citations(depot, textes, fautes, surcouche=None):
    """C4 (E14) et C5 (E16) sur des textes nommés ; surcouche : fichiers d'après un diff, lus avant ceux du dépôt."""
    h = GC.maintenant()
    for nom, t in textes:
        for n, code, x in GC.horodatages_fautifs(t, h):
            fautes.append(("refus", "C4", f"{code} à {nom}:{n} : {x} (E14)", "lire date -u, puis récrire l'heure", "-"))
        refus, avert = GC.citations(t, depot, surcouche)
        for n, code, ref in refus:
            fautes.append(("refus", "C5", f"{code} à {nom}:{n} ({ref}) (E16)",
                           "ouvrir la ligne citée, la copier mot pour mot", "-"))
        for n, code, ref in avert:
            fautes.append(("avertissement", "C5", f"{code} à {nom}:{n} ({ref})", "", "-"))


def diffs_nommes(a, fautes):
    """C6 (LA-N04) : dans un index temporaire, HEAD plus les diffs nommés, dans l'ordre, égale l'arbre de l'index."""
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(d, "index"))
        git(a.depot, "read-tree", "HEAD", env=env)
        try:
            for x in a.diff:
                git(a.depot, "apply", "--cached", os.path.abspath(x), env=env)
            egal = git(a.depot, "write-tree", env=env) == git(a.depot, "write-tree")
        except Erreur:
            egal = False
    if not egal:
        fautes.append(("refus", "C6", "l'index n'est pas HEAD plus les diffs nommés, dans l'ordre (LA-N04)",
                       "retirer de l'index ce qui n'est pas dans les diffs nommés, ou nommer le diff manquant", "-"))


def decalage(blocs, longueur):
    """Première ligne existante (numéro d'avant) qu'un bloc décale, sinon None : un ajout après la dernière ligne et
    un remplacement à nombre de lignes égal n'en décalent aucune (E21)."""
    pos = ecart = 0
    for a, b, _c, _d, lignes in blocs:
        debut = a - 1 if b else a
        if debut > pos and ecart:
            return pos + 1
        pos = debut
        for x in lignes:
            if x[0] == " " and ecart:
                return pos + 1
            pos += x[0] != "+"
            ecart += (x[0] == "+") - (x[0] == "-")
    return pos + 1 if pos < longueur and ecart else None


def cites(depot, texte, fichiers, fautes):
    """C7 (E21) sur les fichiers de garde/lignes-citees.txt ; ligne Décalage admis : <chemin> du message : admis,
    journalisé en contournement."""
    with open(CITES, encoding="utf-8") as f:
        motifs = [x.strip() for x in f if x.strip() and not x.startswith("#")]
    for f in fichiers:
        chemin = f["avant"]
        if not chemin or not any(fnmatch.fnmatchcase(chemin, m) for m in motifs):
            continue
        if f["apres"] is None:      # fichier cité retiré, ou renommé (--no-renames) : ses renvois tombent (R-4)
            ligne, quoi = 1, "fichier retiré ou renommé, ses renvois par numéro ne mènent plus nulle part"
        else:
            contenu = git(depot, "cat-file", "-p", "HEAD:" + chemin)
            ligne = decalage(f["blocs"], contenu.count(chr(10)) + (contenu[-1:] not in ("", chr(10))))
            quoi = f"un bloc décale la ligne {ligne} et les suivantes"
        if ligne is None:
            continue
        if "Décalage admis : " + chemin in texte.split(chr(10)):
            fautes.append(("admis", "C7", f"{chemin} : ligne {ligne} décalée, admis par le message", "",
                           "decalage-admis"))
        else:
            fautes.append(("refus", "C7", f"{chemin} : {quoi} (E21)",
                           "ajouter en fin ; décalage voulu : ligne Décalage admis : " + chemin + " au message", "-"))


def workflows(depot, fichiers, fautes, env=None):
    """C8 (E1) : un workflow touché : enforcement/workflows-yaml.py du dépôt lit les workflows de l'index, ou de
    l'index temporaire d'un diff (env)."""
    if not any((f["apres"] or f["avant"] or "").startswith(".github/workflows/") for f in fichiers):
        return
    lecteur = os.path.join(depot, "enforcement", "workflows-yaml.py")
    if not os.path.isfile(lecteur):
        raise Erreur("enforcement/workflows-yaml.py absent : lecture YAML impossible")
    with tempfile.TemporaryDirectory() as d:
        noms = [x for x in git(depot, "ls-files", "-z", "--", ".github/workflows", env=env).split(chr(0)) if x]
        git(depot, "checkout-index", "--prefix=" + d + os.sep, "--", *noms, env=env)
        p = subprocess.run([sys.executable, "-B", lecteur, d], capture_output=True, text=True)
    if p.returncode == 1:
        fautes.append(("refus", "C8", "un workflow de l'index ne se lit pas en YAML (E1) : " + p.stderr.strip()[:200],
                       "corriger le workflow, relancer enforcement/workflows-yaml.py", "-"))
    elif p.returncode:
        raise Erreur(f"enforcement/workflows-yaml.py : sortie {p.returncode}")



def presg5(depot, textes, fautes):
    """S-G5 approché par presg5.py (E9) : fragment anglais entre guillemets français, introuvable dans biblio/."""
    with tempfile.TemporaryDirectory() as d:
        for k, (nom, t) in enumerate(textes):
            with open(os.path.join(d, str(k)), "w", encoding="utf-8") as f:
                f.write(t)
            for _p, n, x in P5.introuvables(depot, [os.path.join(d, str(k))]):
                fautes.append(("refus", "G5", f"{nom}:{n} : {x[:80]} (E9)",
                               "mettre le texte anglais ou le message d'outil en code", "-"))


def chemins_du_patch(depot, texte, fichier):
    """Chemins qu'un patch nomme, lus sans rien appliquer : en-têtes (diff --git, ---, +++, rename, copy) et chemins de
    git apply --numstat (préfixes ôtés comme à l'application, quel que soit le format du diff)."""
    noms = {c for f in GC.analyser_diff(texte) for c in (f["avant"], f["apres"]) if c}
    entetes = [x for x in texte.split(chr(10)) if x.startswith(("rename ", "copy ")) and x.count(" ") > 1]
    noms |= {x.split(" ", 2)[2] for x in entetes}
    numstat = git(depot, "apply", "--numstat", "-z", os.path.abspath(fichier))
    noms |= {x.split(chr(9))[-1] for x in numstat.split(chr(0))}
    return {x for x in noms if x}


def diff(a, fautes):
    interdit = ("refus", "D1", "fichier(s) du diff sous un interdit : ni lus ni nommés", "retirer ces fichiers du diff",
                "-")
    try:
        noms = chemins_du_patch(a.depot, lire(a.fichier).decode("utf-8"), a.fichier)
    except Erreur:
        noms = None
    if noms and any(GC.chemin_interdit(os.path.join(a.depot, c)) for c in noms):
        fautes.append(interdit)
        return
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(d, "index"))
        git(a.depot, "read-tree", "HEAD", env=env)
        try:
            if noms is None:
                raise Erreur("patch illisible par git apply --numstat")
            git(a.depot, "apply", "--cached", os.path.abspath(a.fichier), env=env)
        except Erreur:
            fautes.append(("refus", "D2", "le diff ne s'applique pas sur la tête du dépôt (base ancienne ?)",
                           "refaire le diff sur la tête du moment", "-"))
            return
        fichiers, ecartes = GC.lignes_ajoutees(a.depot, env)
        if ecartes:
            fautes.append(interdit)
            return
        apres = os.path.join(d, "apres")
        biblio = [x for x in git(a.depot, "ls-files", "-z", "--", "biblio", env=env).split(chr(0)) if x.count("/") == 1]
        touches = sorted({f["apres"] for f in fichiers if f["apres"]} | set(biblio))
        if touches:
            git(a.depot, "checkout-index", "--prefix=" + apres + os.sep, "--", *touches, env=env)
        textes = [(f["apres"], place(f["ajouts"])) for f in fichiers if (f["apres"] or "").endswith(".md")]
        heures_et_citations(a.depot, textes, fautes, apres)
        presg5(apres, textes, fautes)
        cites(a.depot, "", fichiers, fautes)
        workflows(a.depot, fichiers, fautes, env)



def verser(a, fautes):
    racine = os.path.abspath(a.pieces)
    if not os.path.isdir(racine) or GC.chemin_interdit(racine):
        raise Erreur("dossier de pièces absent ou interdit (non lu)")
    reel, depot = os.path.realpath(racine), os.path.realpath(a.depot)
    if depot == reel or depot.startswith(reel.rstrip(os.sep) + os.sep):
        raise Erreur("dossier de pièces refusé : /, le dépôt ou l'un de ses ancêtres (jamais parcouru)")
    pieces, ecartes, autres = {}, 0, 0
    for base, dossiers, fichiers in os.walk(racine):
        caches = {x for x in dossiers if GC.chemin_interdit(os.path.join(base, x))}
        ecartes += len(caches)
        dossiers[:] = sorted(set(dossiers) - caches)
        for x in sorted(fichiers):
            p = os.path.join(base, x)
            if GC.chemin_interdit(p):
                ecartes += 1
            elif not os.path.isfile(p):
                autres += 1
            else:
                pieces[os.path.relpath(p, racine)] = lire(p)
    if ecartes:
        fautes.append(("refus", "V0", f"{ecartes} fichier(s) ou dossier(s) sous un interdit : ni lus, ni parcourus, "
                       "ni nommés", "les retirer", "-"))
    if autres:
        fautes.append(("refus", "V5", f"{autres} fichier(s) non ordinaire(s) (lien brisé, tube, appareil) : non lus",
                       "les retirer", "-"))
    vues, md = {}, {r: b.decode("utf-8") for r, b in pieces.items() if r.endswith(".md")}
    for r, b in pieces.items():
        h = hashlib.sha256(b).hexdigest()
        if h in vues:
            fautes.append(("refus", "V2", f"{r} et {vues[h]} ont le même sha256 (E10)", "verser chaque pièce une fois",
                           "-"))
        vues.setdefault(h, r)
    plies = {r: GC.plier(x) for r, x in md.items()}
    for r1, t1 in plies.items():
        for r2 in [r2 for r2, t2 in plies.items() if r2 != r1 and len(t1) >= 500 and t1 in t2]:
            fautes.append(("refus", "V2", f"{r1} est contenu en entier dans {r2} (E10)",
                           "verser la source entière une fois, sans copie dans une autre pièce", "-"))
    for r in [r for r, b in pieces.items() if b"/tmp/claude-" in b]:
        fautes.append(("refus", "V3", f"{r} porte un chemin absolu du scratchpad", "l'abréger en <scratchpad>", "-"))
    if "SHA256SUMS" not in pieces:
        fautes.append(("refus", "V4", "SHA256SUMS absent du dossier", "l'écrire depuis le dossier : sha256sum <pièces>",
                       "-"))
    ds = _module("docs_sha256sums", os.path.join(GC.RACINE_OUTILS, "enforcement", "docs-sha256sums.py"))
    parent, nom = os.path.split(racine)
    for s in [r for r in pieces if os.path.basename(r) == "SHA256SUMS"]:
        motifs = []
        non_listes = ds.verifier(parent, (nom + "/" + s).replace(os.sep, "/"), motifs)[2]
        motifs += [f"{non_listes} pièce(s) non listée(s) dans {s}"] if non_listes else []
        fautes += [("refus", "V4", m, "écrire SHA256SUMS depuis le dossier : sha256sum <pièces>", "-") for m in motifs]
    textes = sorted(md.items())
    heures_et_citations(a.depot, textes, fautes)
    presg5(a.depot, textes, fautes)



def pousser(a, fautes):
    with open(HORS, encoding="utf-8") as f:
        regles = [x.split(" ", 1) for x in f.read().split(chr(10)) if x.strip() and not x.startswith("#")]
    if a.acte is not None:
        acte = " ".join(a.acte.replace('"', " ").replace("'", " ").split())      # R-3
        acte = re.sub("(^| )git(?: -[Cc] [^ ]+| --no-optional-locks| --(?:git-dir|work-tree)=[^ ]+)+ ",
                      lambda m: m[1] + "git ", acte)
        acte = re.sub("(?:--method[ =]|-X ?)([A-Za-z]+)", lambda m: "-X " + m[1].upper(), acte)
        if any(fnmatch.fnmatchcase(acte, m) for k, m in regles if k == "acte"):
            fautes.append(("refus", "P4", "acte sur la forge déjà refusé par le mandataire réseau (B.95, E17)",
                           "ne pas le retenter : le décrire pas à pas à l'investisseur", "-"))
        return
    if not (a.distant and a.branche):
        raise Erreur("pousser : --distant et --branche, ou --acte")
    poussee = subprocess.run(["git", "-C", a.depot, "rev-parse", "--verify", "--quiet", f"refs/heads/{a.branche}"],
                             capture_output=True, text=True).stdout.strip()
    if poussee != git(a.depot, "rev-parse", "--verify", "HEAD").strip():
        fautes.append(("refus", "P3", f"la branche {a.branche} n'est pas HEAD : git push {a.distant} {a.branche} "
                       "pousserait un commit ni scellé ni contrôlé (LA-N05, LA-N01)",
                       f"se placer sur {a.branche}, vérifier, sceller --tete, relancer", "-"))
    if not os.path.exists(os.path.join(garde(a.depot, "sceaux"), cle(a.depot, tete=True))):
        fautes.append(("refus", "P1", "aucun sceau de la tête (LA-N05 : poussée rouge)",
                       "vérification complète de la tête, puis avant_acte.py sceller --tete", "-"))
    try:
        base = git(a.depot, "rev-parse", "--verify", f"refs/remotes/{a.distant}/{a.branche}").strip()
    except Erreur:
        base = git(a.depot, "hash-object", "-t", "tree", os.devnull).strip()
    chemins = [m for k, m in regles if k == "chemin"]
    p = subprocess.run(["git", "-C", a.depot, "diff", "--quiet", base, "HEAD", "--", *chemins], capture_output=True)
    if p.returncode not in (0, 1):
        raise Erreur(f"git diff : sortie {p.returncode}")
    historique = subprocess.run(["git", "-C", a.depot, "rev-list", "-n", "1", "HEAD", "--not",
                                 f"--remotes={a.distant}", "--", *chemins], capture_output=True, text=True)
    if historique.returncode:
        raise Erreur(f"git rev-list : sortie {historique.returncode}")
    if p.returncode or historique.stdout.strip():      # tête, ou un commit de la plage (contre-contrôle, R-2)
        fautes.append(("refus", "P2", "la plage poussée change un chemin de garde/hors-distant.txt, dans la tête "
                       "ou dans un de ses commits (non nommé)", "retirer ce chemin de l'historique poussé "
                       "(ADR-0028 l.293 : préfixes sans ces fichiers)", "-"))
    noms = [x for x in git(a.depot, "diff", "--name-only", "-z", base, "HEAD", "--", ".github/workflows").split(chr(0))]
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(d, "index"))
        git(a.depot, "read-tree", "HEAD", env=env)
        workflows(a.depot, [{"apres": x, "avant": None} for x in noms if x], fautes, env)


def publier(a, fautes):
    texte = lire(a.texte).decode("utf-8")
    heures_et_citations(a.depot, [(os.path.basename(a.texte), texte)], fautes)
    with open(os.path.join(GC.RACINE_OUTILS, "enforcement", "gate-secrets.sh"), encoding="utf-8") as f:
        motif = [x for x in f.read().split(chr(10)) if x.startswith("VENDOR='")][0][8:].rsplit("'", 1)[0]
    if re.search(motif, texte):
        fautes.append(("refus", "P5", "motif de secret de la gate G3 dans le texte (non recopié)", "le retirer", "-"))
    if "/tmp/claude-" in texte:
        fautes.append(("refus", "V3", "chemin absolu du scratchpad dans le texte", "l'abréger en <scratchpad>", "-"))



def existe(a, fautes):
    if "/" in a.nom or set(a.nom) & set("*?[]") or GC.chemin_interdit(a.nom):
        raise Erreur("existe : un nom de fichier simple, ni chemin, ni motif, ni interdit")
    motifs = [":(glob,icase)**/" + a.nom, ":(glob,icase)**/" + a.nom + "/**"]
    sortie = git(a.depot, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", *motifs)
    trouves = set()
    for x in [x for x in sortie.split(chr(0)) if x and not GC.chemin_interdit(os.path.join(a.depot, x))]:
        parts = x.split("/")
        k = next((i for i, p in enumerate(parts) if p.casefold() == a.nom.casefold()), len(parts) - 1)
        trouves.add("/".join(parts[:k + 1]) + ("/" if k + 1 < len(parts) else ""))
    print(*sorted(trouves), sep=chr(10), end=chr(10) if trouves else "")
    if not trouves:
        fautes.append(("refus", "X1", f"{a.nom} absent du dépôt (fichiers et dossiers, suivis ou non, toute casse ; "
                       "hors fichiers ignorés par git et interdits)", "", "-"))


def cibles(racine, profondeur=4):
    """(chemin, octets) des dossiers target qui portent CACHEDIR.TAG, à profondeur 4 au plus sous racine ; os.walk ne
    suit aucun lien."""
    trouves = []
    for base, dossiers, fichiers in os.walk(racine):
        if os.path.basename(base) == "target" and "CACHEDIR.TAG" in fichiers:
            trouves.append((base, sum(os.path.getsize(os.path.join(b, x)) for b, _d, fs in os.walk(base) for x in fs
                                      if not os.path.islink(os.path.join(b, x)))))
            dossiers[:] = []
            continue
        niveau = 0 if base == racine else os.path.relpath(base, racine).count(os.sep) + 1
        dossiers[:] = sorted(x for x in dossiers if niveau < profondeur and x not in ("docs", ".git")
                             and not GC.chemin_interdit(os.path.join(base, x)))
    return trouves


def disque(a, fautes):
    etat, libre = GC.etat_disque("/", a.min_go)
    if etat != "ok":
        fautes.append(("refus" if etat == "refus" else "avertissement", "DQ", f"{libre:.1f} Gio libres sur / (E4)",
                       "lister les cibles cargo des lots clos (disque --lister <dossier>), puis les supprimer", "-"))
    for racine in a.lister:
        if GC.racine_dangereuse(racine, a.depot):
            raise Erreur("disque --lister : racine refusée (/, dépôt ou ancêtre, dossier docs, interdit)")
        for chemin, octets in cibles(racine):
            print(f"{octets / 2 ** 30:.2f} Gio" + chr(9) + chemin)



def chaine(a, fautes):
    plan = [x for x in lire(a.plan).decode("utf-8").split(chr(10)) if x.strip()]
    duree = len(plan) * a.duree_pas
    if duree > BORNE_LIEE and not a.detache:
        fautes.append(("refus", "G3", f"durée estimée {duree:.0f} min ({len(plan)} pas × {a.duree_pas:g} min), "
                       f"au-delà de {BORNE_LIEE} min pour un lancement lié (E25)",
                       f"lancer détaché : DETACHE=1 setsid nohup timeout {int(duree * 120)} bash chaine.sh > "
                       "chaine.log 2>&1 & (PID et journal consignés), puis attendre la fin dans un appel séparé", "-"))
    lignes = [x for x in lire(a.cc).decode("utf-8").split(chr(10)) if x.startswith("GROUPES :")]
    valeur = lignes[0][9:].strip() if len(lignes) == 1 else ""
    groupes = [[x.strip() for x in g.split("+")] for g in valeur.split(";")]
    if any(not all(re.fullmatch("[A-Za-z0-9._-]+", x) for x in g) for g in groupes):
        fautes.append(("refus", "G1", "le rapport de contre-contrôle ne porte pas une seule ligne GROUPES : lisible",
                       "ajouter la ligne fixe du gabarit rapport-cc.md (GROUPES : aucun, ou A+B ; C+D)", "-"))
        return
    noms = {os.path.basename(d).removesuffix(".diff") for ligne in plan for d in ligne.split("|")[1].split(",")}
    inconnus = [] if valeur == "aucun" else sorted({x for g in groupes for x in g} - noms)
    if inconnus:
        fautes.append(("refus", "G1", f"GROUPES nomme des diffs absents du plan : {', '.join(inconnus)} (E11)",
                       "nommer chaque diff du groupe par son fichier, sans .diff, comme au plan", "-"))
        return
    for ligne in plan:
        pas = {os.path.basename(d).removesuffix(".diff") for d in ligne.split("|")[1].split(",")}
        for g in [g for g in groupes if set(g) & pas and not set(g) <= pas]:
            fautes.append(("refus", "G2", f"le pas {ligne.split('|')[0]} coupe le groupe {'+'.join(g)} (E11)",
                           "commettre le groupe en un seul pas", "-"))
    nettoye = lambda t: subprocess.run(["git", "stripspace"], input=t, capture_output=True, text=True).stdout
    for ligne in plan:
        ident, message = ligne.split("|")[0], ligne.split("|")[2]
        for h in git(a.depot, "log", "--format=%H", "-F", f"--grep=Diff-Id: {ident}", "HEAD").split():
            corps = git(a.depot, "log", "-1", "--format=%B", h)
            ecrit = nettoye(lire(message).decode("utf-8")) if f"Diff-Id: {ident}" in corps.split(chr(10)) else None
            if ecrit is not None and nettoye(corps) != ecrit:
                fautes.append(("refus", "G4", f"Diff-Id: {ident} déjà porté par {h[:12]}, d'un autre message : la "
                               "reprise sauterait ce pas", "donner au pas un identifiant propre au lot", "-"))
                break


COMMANDES = {"sceller": sceller, "commit": commit, "diff": diff, "verser": verser, "pousser": pousser,
             "publier": publier, "existe": existe, "disque": disque, "chaine": chaine}


def journal(a, fautes):
    try:
        d = garde(a.depot)
    except Erreur:
        return
    h = GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ")
    lignes = [(code, niveau, c) for niveau, code, _r, _g, c in fautes] or [("-", "conforme", "-")]
    with open(os.path.join(d, "journal.tsv"), "a", encoding="utf-8") as f:
        f.writelines(chr(9).join([h, a.cmd, *x]) + chr(10) for x in lignes)


def parseur():
    """Lignes de commande des sous-commandes (lues aussi par tests/test_skills.py : options exigées)."""
    p = argparse.ArgumentParser(prog="avant_acte.py", description=__doc__.split(chr(10))[0])
    p.add_argument("--depot", default=".")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("sceller").add_argument("--tete", action="store_true")
    c = sp.add_parser("commit")
    c.add_argument("--message", required=True)
    c.add_argument("--source", action="append", required=True)
    c.add_argument("--diff", action="append", default=[])
    c.add_argument("--id")
    sp.add_parser("diff").add_argument("--fichier", required=True)
    sp.add_parser("verser").add_argument("--pieces", required=True)
    s = sp.add_parser("pousser")
    for option in ("--distant", "--branche", "--acte"):
        s.add_argument(option)
    sp.add_parser("publier").add_argument("--texte", required=True)
    sp.add_parser("existe").add_argument("nom")
    s = sp.add_parser("disque")
    s.add_argument("--min-go", type=float)
    s.add_argument("--lister", nargs="+", default=[])
    s = sp.add_parser("chaine")
    s.add_argument("--plan", required=True)
    s.add_argument("--cc", required=True)
    s.add_argument("--duree-pas", type=float, default=6)
    s.add_argument("--detache", action="store_true")
    return p


def main(argv=None):
    try:
        a = parseur().parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    fautes = []
    try:
        COMMANDES[a.cmd](a, fautes)
    except Exception as e:      # erreur de l'outil, jamais un refus (contrat 0, 1, 3)
        print(f"ERREUR {a.cmd} : {type(e).__name__} : {e}", file=sys.stderr)
        return 3
    for niveau, code, raison, geste, _c in fautes:
        print(f"{niveau.upper()} {code} : {raison}" + (f" ; à faire : {geste}" if geste else ""))
    try:
        journal(a, fautes)
    except Exception as e:      # journal non écrit : erreur de l'outil, jamais un refus (C-9)
        print(f"ERREUR journal : {type(e).__name__} : {e}", file=sys.stderr)
        return 3
    return 1 if any(f[0] == "refus" for f in fautes) else 0


def sortir(principal):
    """C-18 : une exception hors des sous-commandes (écriture de la sortie) ou l'échec du vidage final de la sortie
    standard (tube sans lecteur) rend 3, jamais 1 (un refus) ni 120 (vidage à la fin de l'interpréteur) ; la sortie
    est alors détournée vers /dev/null, que l'interpréteur vide sans erreur."""
    try:
        code = principal()
        sys.stdout.flush()
    except Exception as e:
        with contextlib.suppress(Exception):
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        print(f"ERREUR : {type(e).__name__} : {e}", file=sys.stderr)
        return 3
    return code


if __name__ == "__main__":
    sys.exit(sortir(main))
