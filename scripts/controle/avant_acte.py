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
Contre-contrôle, R-4 : C7 refuse aussi le retrait ou le renommage d'un fichier cité.
Contre-contrôle, R-5 : chaine G4 refuse aussi un Diff-Id porté par plus d'un pas du plan.
Contre-contrôle, R-7 : verser compte fichiers et octets avant toute lecture (borne).
Contre-contrôle, R-10 : C3 lit aussi le verdict CONFORME-AVEC-RÉSERVES, accentué ou non.
Phase 2, L-1 : C4 refuse aussi une heure écrite sans sa date et, au commit et au diff, une entrée datée ajoutée d'un .md
antérieure à la dernière entrée datée du fichier à HEAD (garde_commun.dates_passees).
Phase 2, L-3 : C3 attribue aussi chaque mot lu (verdict, passes, identifiant, sha court) au diff du message (Diff-Id,
ou --id) : refus si les sources ne l'écrivent que dans des passages (paragraphe, rangée de tableau, point de liste) qui
nomment d'autres diffs du même préfixe (plages N à M lues) et si les lignes ajoutées du diff ne le portent pas.
Phase 2, L-4 : sceller --verif F (texte de declare -f verif, - : entrée standard) écrit au sceau la ligne verif
<sha256> ; commit C1 refuse un sceau dont la ligne verif n'est pas l'empreinte de la fonction verif de
gabarits/chaine.sh des outils (fonction versionnée, declare -f par bash) ; un sceau sans ligne verif n'est pas jugé.
Phase 2, L-13 : C7 lit aussi les empreintes des lignes citées (lignes <chemin>:<a>[-<b>] <empreinte> de
garde/lignes-citees.txt ; rangées du registre docs/RENVOIS-LIGNES.tsv de DETTES-T15, de l'état d'après, colonnes
cible, lignes, empreinte) : un renvoi qui répondait à son empreinte à HEAD et n'y répond plus après le diff est refusé
(à nombre de lignes égal compris), sauf empreinte mise à jour dans le même diff ; empreinte du registre.
Phase 2, L-12, Q-5 : --lecture-seule (diff et commit seulement) : git tourne dans un dépôt jetable de TMPDIR (git clone
--shared --no-checkout, HEAD du dépôt lu, son index copié pour commit) ; fichiers, sceaux et outils lus dans le dépôt
lu, rien n'y est écrit ; le journal va au dépôt jetable (perdu avec lui).
Phase 2 (E28, SHOGEN-GARDE-OUTIL-E26-E27-E28-1) : verser V6, chaque fichier de biblio/ du dépôt (hors INDEX.md et
*.sidecar, répertoire plat) nommé `nom` dans biblio/INDEX.md de l'arbre de travail (la rangée va dans le même diff que
l'octet), compte « N artefacts détenus » des 500 premiers octets égal au compte réel, sauf corpus partiel tout nommé
(forme de S-G6, xtask/src/sg6.rs) ; V7, refus pendant qu'une chaîne de commits tourne : pgrep -f ancré
(MOTIF_CHAINE, bash ou sh qui lance chaine.sh ou chaine_*.sh ; ancré, il ne reconnaît pas le shell qui le lance) ;
pgrep en erreur : 3.
Phase 2, groupe A : brief --texte F [--fiche NOM], avant de lancer un agent (crochet GARDE-FAITS R11) : B1, tout item
SHOGEN-… ou MONARK-… du brief est ouvert à l'annexe B (garde_commun.etat_items), sauf si le brief l'écrit fermé ; absent
de l'annexe : avertissement (E6) ; B4, un brief qui nomme une commande git porte, lui ou la fiche NOM
(.claude/agents/NOM.md), la règle des commandes git limitées à une « liste explicite de chemins » (E24).
B2, un constat relayé (le CC, la G2, le réviseur, un lot nommé… a relevé, a trouvé, dit… ; selon la G2) porte sur sa
ligne ou la suivante une référence fichier et ligne (chemin:N, chemin l.N, JOURNAL l.N ; E22). B3, faisabilité (E23) :
chaque chemin:N se lit (fichier présent, ligne dans le fichier) ; chaque chemin entre accents graves de base connue
(absolu, ou premier composant présent à la racine du dépôt) existe, hors ligne qui dit le produire ; chaque sha court
(hors sha256) est un commit ; chaque sous-commande avant_acte.py nommée existe ; les interdits ne sont jamais lus.
RX (E12), à commit (index), diff (HEAD plus le diff) et pousser (plage poussée) : chaque motif ajouté
(garde_commun.motifs_ajoutes) passe garde_commun.motifs_suspects ; forme exponentielle : refus, sauf ligne qui porte
redos-admis (journalisée en contournement) ; motif illisible : avertissement.
diff --rapport R (E13) : D3, toute fonction publique (def de premier niveau, sans _) ajoutée à scripts/controle/*.py
est nommée dans scripts/controle/README.md d'après le diff ; D4, tout test ajouté (def test_… d'un .py sous tests/) est
nommé dans le rapport R sur une ligne qui dit un mutant tué ; tests ajoutés sans --rapport : refus.
Relecture G2 du groupe A, C-2 (E24, décision de l'orchestrateur) : B4 exige la règle dans le brief lui-même, quelle
que soit la fiche (une fiche qui la porte ne suffit plus) ; --fiche vérifie seulement que la fiche existe et la nomme
dans le refus ; une commande git précédée d'options globales (-C, -c, --no-pager, --git-dir=, --work-tree=) est vue.
Relecture G2 du groupe A, C-3 (E22) : B2 lit aussi les sujets au pluriel et le contre-contrôleur, les verbes au pluriel
(relèvent, signalent, constatent, rapportent) et les participes accordés, et d'après comme selon.
Relecture G2 du groupe A, C-4 (E23) : B3 lit aussi chemin l.N et `chemin` l.N (plage l.N-M comprise), la forme de
référence que B2 admet : un fichier ou une ligne inexistants y sont refusés comme dans chemin:N.
Phase 3, groupe C (SHOGEN-GARDE-D3-MOT-COMMUN-1) : D3 cherche le nom de la fonction en code ou en signature au README
(nomme_en_code), non comme mot courant : une fonction suivi n'est pas nommée par « non suivi ».
Phase 3, groupe C (SHOGEN-MOTIFS-ARBRE-REDOS-1) : motifs --arbre, RX sur tous les motifs de l'arbre (appels de re des
.py lus par l'arbre d'ast, motifs YAML) de scripts/controle/, .claude/hooks/ et enforcement/ (motifs_arbre).
Phase 3, groupe C (SHOGEN-GARDE-FOUS-ORCH-1, phase 3) : refus [--depuis J] [--journal F], relevé du journal des refus
du crochet GARDE-FAITS (refus, regles_du_crochet).
Phase 3, groupe B (SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1) : chaque passage en --lecture-seule ajoute une ligne au
journal garde/lecture-seule.tsv des outils (JOURNAL_LS, ignoré par git) : heure lue par date -u, sous-commande, tête du
dépôt lu, verdict (conforme, refus, erreur) ; journal non écrit : sortie 3.
Phase 3, groupe B (SHOGEN-GARDE-DISQUE-DU-DEPOT-1) : disque (DQ, GF-8b) mesure le système de fichiers du dépôt, et
celui de TMPDIR s'il en diffère (lieux_disque), non / ; le modèle de chaîne l'appelle avec --depot "$DEPOT".
Phase 3, groupe A, PLAGE-LETTRES : C3 (L-3) lit aussi une plage à bornes en lettres (DT15-a à DT15-m ; rang : lettres
de tête, z avant aa) ; deux bornes de sortes différentes (nombre, lettres) ne forment pas de plage.
Phase 3, groupe A, RECALAGE-CHECK : chaine --blanc --script S [--diffs D...] (diffs du plan à défaut), avant le
lancement (E30, E31, E36) : sur une copie creuse de HEAD (git archive, interdits exclus), chaque diff dans l'ordre : K0
interdit, K5 git apply --check après les précédents, K6 motif R-13 du job g5 (lu dans gates.yml) et G5 presg5 sur ses
seules lignes ajoutées."""
import argparse
import ast
import collections
import contextlib
import fnmatch
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import timedelta


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
VERDICT = re.compile("(?<![A-Z-])(ACCEPTE-AVEC-CORRECTIONS|CONFORME-AVEC-R[ÉE]SERVES|NON-CONFORME|CONFORME"
                     "|ACCEPTE|REFUSE)(?![A-Z-])")      # R-10 : verdict avec réserves, accentué ou non
PASSES = re.compile("(?i)(?<![0-9a-zé])([0-9]+|une?|deux|trois|quatre|cinq|six) passes?(?![a-z])")
PASSE_N = re.compile("(?i)(?<![0-9a-zé])passe ([0-9]+)(?![0-9])")
NEGATION = re.compile("(?i)(?:sans|aucune|pas de|ni) (?:la |une )?$")
NOMBRES = {"un": "1", "une": "1", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6"}
IDENT = re.compile("(?<![A-Za-z0-9-])(SHOGEN-[A-Z0-9]+(?:-[A-Z0-9]+)*|[GCRQLEOI]-[0-9]+)(?![A-Za-z0-9-])")
SHA = re.compile("(?<![A-Za-z0-9-])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])([0-9a-f]{7,40})(?![A-Za-z0-9…-])")
PIEDS = ("Source-Sha:", "Diff-Id:", "Co-Authored-By:", "Claude-Session:", "Décalage admis :")
CITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "garde", "lignes-citees.txt")
HORS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "garde", "hors-distant.txt")
JOURNAL_LS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "garde", "lecture-seule.tsv")    # ignoré par git
MODELE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gabarits", "chaine.sh")
REGISTRE = "docs/RENVOIS-LIGNES.tsv"
EMPREINTE = re.compile("([^ :]+):([0-9]+)(?:-([0-9]+))? ([0-9a-f]{16,64})")
BORNE_LIEE = 100
PIECES_MAX, OCTETS_MAX = 5000, 512 * 2 ** 20      # verser : borne d'un dossier de pièces (R-7)
MOTIF_CHAINE = "^(/usr/bin/|/bin/)?(bash|sh) ([^ ]*/)?chaine(_[^ /]*)?[.]sh( |$)"     # V7 (E28), ancré


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


def jetable(source, dossier, index):
    """Dépôt jetable dans dossier : clone --shared --no-checkout de source, HEAD détachée sur celle de source, index de
    source copié si index ; source n'est que lue (L-12)."""
    tete, cible = git(source, "rev-parse", "--verify", "HEAD").strip(), os.path.join(dossier, "depot")
    p = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", "--", source, cible], capture_output=True)
    if p.returncode:
        raise Erreur(f"git clone : sortie {p.returncode}")
    git(cible, "update-ref", "--no-deref", "HEAD", tete)
    if index:
        shutil.copyfile(os.path.join(source, git(source, "rev-parse", "--git-path", "index").strip()),
                        os.path.join(cible, git(cible, "rev-parse", "--git-path", "index").strip()))
    return cible


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
    verif = None if a.verif is None else sys.stdin.buffer.read() if a.verif == "-" else lire(a.verif)
    with open(os.path.join(garde(a.depot, "sceaux"), cle(a.depot, a.tete)), "w", encoding="utf-8") as f:
        f.write(GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ") + chr(10))
        f.write("" if verif is None else "verif " + hashlib.sha256(verif).hexdigest() + chr(10))


def empreinte_verif(chaine=MODELE):
    """sha256 de declare -f verif (bash) de la fonction verif d'un modèle de chaîne, de verif() { à # --- fin de
    verif (L-4)."""
    lignes = lire(chaine).decode("utf-8").split(chr(10))
    debut = [k for k, x in enumerate(lignes) if x.startswith("verif() {")]
    fin = [k for k, x in enumerate(lignes) if x.startswith("# --- fin de verif") and debut and k > debut[0]]
    if not fin:
        raise Erreur("fonction verif introuvable dans le modèle de chaîne")
    p = subprocess.run(["bash", "-c", 'eval "$1" && declare -f verif', "_", chr(10).join(lignes[debut[0]:fin[0]])],
                       capture_output=True)
    if p.returncode:
        raise Erreur(f"bash : sortie {p.returncode} sur la fonction verif du modèle")
    return hashlib.sha256(p.stdout).hexdigest()


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
    lieu = os.path.join(a.racine, git(a.racine, "rev-parse", "--git-path", "shogen-garde").strip(), "sceaux")
    sceau = os.path.join(lieu if a.lecture_seule else garde(a.depot, "sceaux"), cle(a.depot))
    if not os.path.exists(sceau):
        fautes.append(("refus", "C1", "aucun sceau pour cet index et cette tête (LA-N05)",
                       "relancer la vérification complète puis sceller : <vérification> && avant_acte.py sceller", "-"))
    else:
        with open(sceau, encoding="utf-8") as f:
            v = [x[6:] for x in f.read().split(chr(10)) if x.startswith("verif ")]
        if v and v[0] != empreinte_verif():
            fautes.append(("refus", "C1", f"sceau d'une vérification ({v[0][:12]}…) autre que la fonction verif "
                           "versionnée de gabarits/chaine.sh (L-4)", "relancer la chaîne copiée du modèle versionné, "
                           "ou verser au modèle la vérification voulue par un diff relu", "-"))
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
    verdicts = lambda t: {x.replace("RESERVES", "RÉSERVES") for x in VERDICT.findall(t)}
    manques = [("verdict", x) for x in sorted(verdicts(corps) - verdicts(src))]
    manques += [("nombre de passes", x) for x in sorted(passes(corps) - passes(src, source=True))]
    manques += [("identifiant", x) for x in sorted(set(IDENT.findall(corps)) - set(IDENT.findall(src)))]
    manques += [("sha court", x) for x in sorted(set(SHA.findall(corps))) if x not in src and not resolu(a.depot, x)]
    for genre, x in manques:
        fautes.append(("refus", "C3", f"{genre} du message absent des sources : {x} (E8)",
                       "reprendre les mots de l'adjudication et de la ligne d'annexe relues", "-"))
    fichiers, ecartes = GC.lignes_ajoutees(a.depot, racine=a.racine)
    ident = a.id or next((x[9:].strip() for x in texte.split(chr(10)) if x.startswith("Diff-Id: ")), None)
    if ident and "-" in ident:
        juges = [("verdict", verdicts), ("nombre de passes", lambda u: passes(u, source=True)),
                 ("identifiant", lambda u: set(IDENT.findall(u))), ("sha court", lambda u: set(SHA.findall(u)))]
        ajoute = chr(10).join(x for f in fichiers for _n, x in f["ajouts"])
        attribuer(ident, corps, [b.decode("utf-8", "replace") for b in sources], ajoute, juges, fautes)
    if ecartes:
        fautes.append(("avertissement", "C4", f"{ecartes} fichier(s) indexé(s) sous un interdit, non lus", "", "-"))
    textes = [(f["apres"], place(f["ajouts"])) for f in fichiers if (f["apres"] or "").endswith(".md")]
    heures_et_citations(a.racine, [("message", texte)] + textes, fautes)
    passees(a.depot, fichiers, fautes)
    if a.diff:
        diffs_nommes(a, fautes)
    cites(a.depot, texte, fichiers, fautes)
    workflows(a.depot, fichiers, fautes, racine=a.racine)
    motifs(fichiers, fautes)
    if a.id and f"Diff-Id: {a.id}" not in texte.split(chr(10)):
        fautes.append(("refus", "C9", f"le message ne porte pas la ligne Diff-Id: {a.id}", "l'ajouter au message", "-"))


def unites(texte):
    """Passages d'une source : paragraphes, chaque rangée de tableau, point de liste ou titre à part ; une ligne qui
    ne commence par aucune marque continue le passage d'avant ; blancs et marques de citation > de tête ôtés."""
    vus, cour = [], []
    for x in texte.split(chr(10)):
        x = re.sub("^[ >]*", "", x)
        if not x or re.match("(?:[|#]|[-*+] |[0-9]+[.)] )", x):
            vus, cour = vus + [chr(10).join(cour)] if cour else vus, []
        if x:
            cour.append(x)
    return vus + ([chr(10).join(cour)] if cour else [])


def rang(suffixe):
    """Rang d'un suffixe de diff dans une plage : nombre de tête (0, n), ou lettres de tête (1, longueur, lettres), z
    avant aa (DT7-a … DT7-aa) ; None sans l'un ni l'autre (PLAGE-LETTRES)."""
    m = re.match("([0-9]+)|([a-z]+)", suffixe)
    return None if not m else (0, int(m[1])) if m[1] else (1, len(m[2]), m[2])


def nommes(unite, prefixe):
    """(suffixes, plages) des diffs du préfixe nommés dans un passage ; plage N à M (ou a, au, …, ..) : rangs des deux
    bornes, nombres de tête (GF-0 … GF-10b : 0 à 10) ou lettres de tête (DT15-a à DT15-m : a à m), de même sorte."""
    e, bord, borne = re.escape(prefixe), "(?<![A-Za-z0-9-])", "([0-9]+[a-z]?|[a-z]+[0-9]*)"
    vus = set(re.findall(bord + e + "([0-9A-Za-z]+)(?![A-Za-z0-9-])", unite))
    plages = re.findall(bord + e + borne + " ?(?:à|a|au|…|[.]{2,3}) ?" + e + borne + "(?![0-9A-Za-z-])", unite)
    return vus, [(rang(i), rang(j)) for i, j in plages if rang(i)[0] == rang(j)[0]]


def attribuer(ident, corps, sources, ajoute, juges, fautes):
    """C3, L-3 : mot du message lu dans les sources, que seuls des passages qui nomment d'autres diffs du préfixe
    de ident portent (sans ident, ni une plage qui le couvre), absent des lignes ajoutées : refus."""
    prefixe, suffixe = ident.rsplit("-", 1)
    tete = rang(suffixe)
    autre = lambda vus, plages: (vus - {suffixe} or plages) and suffixe not in vus and not any(
        tete is not None and i <= tete <= j for i, j in plages)
    passages = [(u, nommes(u, prefixe + "-")) for s in sources for u in unites(s)]
    for genre, juge in juges:
        for x in sorted(juge(corps)):
            porteurs = [noms for u, noms in passages if x in juge(u)]
            if porteurs and all(autre(*noms) for noms in porteurs) and x not in juge(ajoute):
                fautes.append(("refus", "C3", f"attribué par les sources à un autre diff que {ident} : {genre} {x} "
                               "(L-3)", "reprendre les mots du passage de la source qui nomme ce diff", "-"))


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


def passees(depot, fichiers, fautes):
    """C4 (L-1) : entrée datée ajoutée d'un .md antérieure à la dernière entrée datée du fichier à HEAD."""
    for f in [f for f in fichiers if (f["apres"] or "").endswith(".md")]:
        avant = git(depot, "cat-file", "-p", "HEAD:" + f["avant"]) if f["avant"] else ""
        for n, code, x in GC.dates_passees(avant, f["ajouts"]):
            fautes.append(("refus", "C4", f"{code} à {f['apres']}:{n} : {x} (L-1)",
                           "lire date -u, puis dater l'entrée du moment, en fin de fichier", "-"))


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


def cites(depot, texte, fichiers, fautes, env=None):
    """C7 (E21) sur les fichiers de garde/lignes-citees.txt ; ligne Décalage admis : <chemin> du message : admis,
    journalisé en contournement."""
    with open(CITES, encoding="utf-8") as f:
        motifs = [x.strip() for x in f if x.strip() and not x.startswith("#") and not EMPREINTE.fullmatch(x.strip())]
    decales = set()
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
        decales.add(chemin)
        if "Décalage admis : " + chemin in texte.split(chr(10)):
            fautes.append(("admis", "C7", f"{chemin} : ligne {ligne} décalée, admis par le message", "",
                           "decalage-admis"))
        else:
            fautes.append(("refus", "C7", f"{chemin} : {quoi} (E21)",
                           "ajouter en fin ; décalage voulu : ligne Décalage admis : " + chemin + " au message", "-"))
    remplacees(depot, fichiers, decales, fautes, env)


def empreintes(depot, env=None):
    """[(chemin, a, b, empreinte, source)] : lignes d'empreinte de garde/lignes-citees.txt, puis rangées du registre de
    l'état d'après (index, ou index temporaire d'env) aux colonnes cible, lignes (a ou a-b ; - : hors de l'arbre,
    sautée), empreinte ; lignes # sautées."""
    with open(CITES, encoding="utf-8") as f:
        vus = [(m[1], int(m[2]), int(m[3] or m[2]), m[4], "garde/lignes-citees.txt")
               for m in map(EMPREINTE.fullmatch, map(str.strip, f)) if m]
    if not git(depot, "ls-files", "-z", "--", REGISTRE, env=env):
        return vus
    rangees = [x.split(chr(9)) for x in git(depot, "show", ":" + REGISTRE, env=env).split(chr(10))
               if x.strip() and not x.startswith("#")]
    tete = rangees[0] if rangees else []
    if not {"cible", "lignes", "empreinte"} <= set(tete):
        raise Erreur(f"{REGISTRE} : colonnes cible, lignes, empreinte attendues en tête")
    k = [tete.index(c) for c in ("cible", "lignes", "empreinte")]
    for r in rangees[1:]:
        m = re.fullmatch("([0-9]+)(?:-([0-9]+))?|-", r[k[1]] if len(r) == len(tete) else "?")
        if not m or not re.fullmatch("[0-9a-f]{16,64}", r[k[2]]):
            raise Erreur(f"{REGISTRE} : rangée illisible")
        vus += [(r[k[0]], int(m[1]), int(m[2] or m[1]), r[k[2]], REGISTRE)] if m[1] else []
    return vus


def remplacees(depot, fichiers, decales, fautes, env=None):
    """C7 (L-13) : renvoi (lignes a à b) qui répondait à son empreinte à HEAD et n'y répond plus après le diff : refus ;
    empreinte qui ne répond ni à HEAD ni à l'état d'après : avertissement ; fichier déjà décalé (refusé ou admis) : non
    jugé. Empreinte : sha256 des lignes jointes par LF, sans LF final, comparé sur sa longueur (16 au registre)."""
    touches = {f["avant"]: f for f in fichiers if f["avant"] and f["avant"] not in decales}
    for chemin, a, b, e, source in empreintes(depot, env):
        if chemin not in touches:
            continue
        avant = git(depot, "cat-file", "-p", "HEAD:" + chemin).split(chr(10))
        apres = git(depot, "show", ":" + chemin, env=env).split(chr(10)) if touches[chemin]["apres"] else []
        h = lambda t: hashlib.sha256(chr(10).join(t[a - 1:b]).encode()).hexdigest()[:len(e)] if b < len(t) else None
        renvoi = str(a) + ("-" + str(b) if b != a else "")
        if h(apres) == e:
            continue
        if h(avant) == e:
            fautes.append(("refus", "C7", f"{chemin} : renvoi {renvoi} changé ou retiré (empreinte de {source}, "
                           "L-13)", "écrire l'erratum en fin ; changement voulu : mettre l'empreinte à jour au "
                           "registre dans le même diff", "-"))
        else:
            fautes.append(("avertissement", "C7", f"{chemin} : empreinte du renvoi {renvoi} ({source}) sans "
                           "réponse à HEAD ni après le diff", "", "-"))


def workflows(depot, fichiers, fautes, env=None, racine=None):
    """C8 (E1) : un workflow touché : enforcement/workflows-yaml.py du dépôt lit les workflows de l'index, ou de
    l'index temporaire d'un diff (env)."""
    if not any((f["apres"] or f["avant"] or "").startswith(".github/workflows/") for f in fichiers):
        return
    lecteur = os.path.join(racine or depot, "enforcement", "workflows-yaml.py")
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


def motifs(fichiers, fautes, liste=None):
    """RX (E12) : motifs des lignes ajoutées (ou de liste, [(chemin, ligne, motif, texte)]) à retour arrière
    exponentiel ; admis par redos-admis sur la ligne."""
    for chemin, n, motif, ligne in GC.motifs_ajoutes(fichiers) if liste is None else liste:
        codes = GC.motifs_suspects(motif)
        if codes == ["motif-illisible"]:
            fautes.append(("avertissement", "RX", f"{chemin}:{n} : motif illisible par re, non jugé", "", "-"))
        elif codes and "redos-admis" in ligne:
            fautes.append(("admis", "RX", f"{chemin}:{n} : {', '.join(codes)}, admis par redos-admis", "", "redos-admis"))
        elif codes:
            fautes.append(("refus", "RX", f"{chemin}:{n} : motif à retour arrière exponentiel ({', '.join(codes)}) "
                           "(E12)", "réécrire sans répétition ambiguë (forme de DT5-24 : séparateur obligatoire entre "
                           "deux répétitions) ; motif voulu : redos-admis et sa raison sur la ligne", "-"))


DOSSIERS_MOTIFS = ("scripts/controle", ".claude/hooks", "enforcement")


def motifs_arbre(a, fautes):
    """motifs --arbre (SHOGEN-MOTIFS-ARBRE-REDOS-1) : RX sur les motifs de l'arbre (fichiers .py, .yml et .yaml de
    DOSSIERS_MOTIFS, interdits et __pycache__ sautés) : appels de re lus par GC.motifs_du_code, motifs YAML par
    GC.motifs_ajoutes ; chaque motif construit autrement (non lu) imprimé NON-LU chemin:ligne, puis un bilan."""
    liste, lus, non_lus = [], 0, []
    for d in DOSSIERS_MOTIFS:
        for base, dossiers, fichiers in os.walk(os.path.join(a.depot, d)):
            dossiers[:] = sorted(x for x in dossiers if x != "__pycache__" and not GC.chemin_interdit(os.path.join(base, x)))
            for x in sorted(f for f in fichiers if f.endswith((".py", ".yml", ".yaml"))):
                chemin = os.path.join(base, x)
                if GC.chemin_interdit(chemin):
                    continue
                rel, lignes = os.path.relpath(chemin, a.depot), lire(chemin).decode("utf-8", "replace").split(chr(10))
                if not x.endswith(".py"):
                    vus = GC.motifs_ajoutes([{"apres": rel, "ajouts": list(enumerate(lignes, 1))}])
                    liste, lus = liste + vus, lus + len(vus)
                    continue
                try:
                    appels = GC.motifs_du_code(chr(10).join(lignes))
                except (SyntaxError, ValueError):
                    fautes.append(("avertissement", "RX", f"{rel} : code illisible par ast, non jugé", "", "-"))
                    continue
                non_lus += [f"{rel}:{n}" for n, _f, m in appels if m is None]
                vus = [(rel, n, m, chr(10).join(lignes[n - 1:fin])) for n, fin, m in appels if m is not None]
                liste, lus = liste + vus, lus + len(vus)
    for x in non_lus:
        print("NON-LU " + x + " : motif construit hors littéraux, non jugé")
    print(f"motifs --arbre : {lus} motif(s) lu(s), {len(non_lus)} non lu(s), dossiers {', '.join(DOSSIERS_MOTIFS)}")
    motifs(None, fautes, liste)


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
    if noms and any(GC.chemin_interdit(os.path.join(a.racine, c)) for c in noms):
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
        fichiers, ecartes = GC.lignes_ajoutees(a.depot, env, a.racine)
        if ecartes:
            fautes.append(interdit)
            return
        apres = os.path.join(d, "apres")
        biblio = [x for x in git(a.depot, "ls-files", "-z", "--", "biblio", env=env).split(chr(0)) if x.count("/") == 1]
        touches = sorted({f["apres"] for f in fichiers if f["apres"]} | set(biblio))
        if touches:
            git(a.depot, "checkout-index", "--prefix=" + apres + os.sep, "--", *touches, env=env)
        textes = [(f["apres"], place(f["ajouts"])) for f in fichiers if (f["apres"] or "").endswith(".md")]
        heures_et_citations(a.racine, textes, fautes, apres)
        passees(a.depot, fichiers, fautes)
        presg5(apres, textes, fautes)
        cites(a.depot, "", fichiers, fautes, env)
        workflows(a.depot, fichiers, fautes, env, a.racine)
        motifs(fichiers, fautes)
        suivi(a, fichiers, env, fautes)


DEF_PUBLIQUE = re.compile("def ([a-z][A-Za-z0-9_]*)[(]")
DEF_TEST = re.compile(" *def (test_[A-Za-z0-9_]*)[(]")
TUE = re.compile("(?i)(?<![a-zà-ÿ])(?:tués?|tuées?|killed)(?![a-zà-ÿ])")


def nomme_en_code(nom, texte):
    """D3 (SHOGEN-GARDE-D3-MOT-COMMUN-1) : vrai si texte nomme la fonction nom en code (passage entre accents graves
    qui est le nom seul ou qualifié : `nom`, `module.nom`) ou en signature (nom( , en code ou non, qualifiée ou non :
    `nom(a, b)`, `module.nom(a)`) ; un mot courant (non suivi), un passage de code qui ne fait que porter le mot (`le
    suivi des diffs`) ou nom( après / - ou $ (URL, chemin, identifiant composé) ne compte pas (G2 du groupe C, C-1)."""
    code = "(?:[A-Za-z0-9_]+[.])*" + re.escape(nom)
    return any(re.fullmatch(code, x.strip()) for x in re.findall("`([^`" + chr(10) + "]*)`", texte)) or bool(
        re.search("(?<![A-Za-z0-9_./$-])" + code + "[(]", texte))


def suivi(a, fichiers, env, fautes):
    """D3 et D4 (E13) : README des contrôles d'après le diff (index temporaire env), rapport du générateur."""
    ajouts = [(f["apres"], n, x) for f in fichiers if (f["apres"] or "").endswith(".py") for n, x in f["ajouts"]]
    publiques = [(c, n, m[1]) for c, n, x in ajouts if re.fullmatch("scripts/controle/[^/]+", c)
                 for m in [DEF_PUBLIQUE.match(x)] if m]
    try:
        readme = git(a.depot, "cat-file", "-p", ":scripts/controle/README.md", env=env) if publiques else ""
    except Erreur:
        readme = ""
    for c, n, nom in publiques:
        if not nomme_en_code(nom, readme):
            fautes.append(("refus", "D3", f"{c}:{n} : fonction publique {nom} absente de scripts/controle/README.md "
                           "(E13)", "la nommer dans l'ajout daté du README (rôle, usage)", "-"))
    tests = [(c, n, m[1]) for c, n, x in ajouts if "/tests/" in "/" + c for m in [DEF_TEST.match(x)] if m]
    if tests and not a.rapport:
        fautes.append(("refus", "D4", f"{len(tests)} test(s) ajouté(s), aucun rapport de mutants (--rapport) (E13)",
                       "relancer avec --rapport <rapport du générateur>", "-"))
        return
    lignes = lire(a.rapport).decode("utf-8").split(chr(10)) if tests else []
    for c, n, nom in tests:
        if not any(nom in x and TUE.search(x) for x in lignes):
            fautes.append(("refus", "D4", f"{c}:{n} : {nom} sans mutant tué au rapport (E13)",
                           "muter le code que le test garde, le voir rouge, consigner le mutant tué", "-"))


def verser(a, fautes):
    racine = os.path.abspath(a.pieces)
    if not os.path.isdir(racine) or GC.chemin_interdit(racine):
        raise Erreur("dossier de pièces absent ou interdit (non lu)")
    reel, depot = os.path.realpath(racine), os.path.realpath(a.depot)
    if depot == reel or depot.startswith(reel.rstrip(os.sep) + os.sep):
        raise Erreur("dossier de pièces refusé : /, le dépôt ou l'un de ses ancêtres (jamais parcouru)")
    pieces, ecartes, autres, octets = {}, 0, 0, 0
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
                pieces[os.path.relpath(p, racine)], octets = p, octets + os.path.getsize(p)
                if len(pieces) > PIECES_MAX or octets > OCTETS_MAX:      # racine fausse (R-7)
                    raise Erreur(f"dossier de pièces de plus de {PIECES_MAX} fichiers ou {OCTETS_MAX >> 20} Mio : "
                                 "racine fausse ? (aucun fichier lu)")
    pieces = {r: lire(p) for r, p in pieces.items()}
    if chaine_active():
        fautes.append(("refus", "V7", "une chaîne de commits tourne : aucun versement pendant qu'elle lit l'arbre "
                       "(E28)", "attendre sa fin (sondage du PID), puis verser", "-"))
    biblio(a.depot, fautes)
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



def biblio(depot, fautes):
    """V6 (E28) : octets de biblio/ sans rangée d'INDEX, ou compte d'en-tête faux (forme de S-G6)."""
    d = os.path.join(depot, "biblio")
    if not os.path.isdir(d):
        return
    noms = sorted(os.listdir(d))
    if any(os.path.isdir(os.path.join(d, x)) for x in noms):
        fautes.append(("refus", "V6", "sous-dossier dans biblio/ : le registre suppose un répertoire plat (S-G6)",
                       "ranger l'octet à plat dans biblio/", "-"))
    artefacts = [x for x in noms if x != "INDEX.md" and not x.casefold().endswith(".sidecar")
                 and os.path.isfile(os.path.join(d, x))]
    index = lire(os.path.join(d, "INDEX.md")) if os.path.isfile(os.path.join(d, "INDEX.md")) else b""
    sans = [x for x in artefacts if f"`{x}`".encode() not in index]
    if sans:
        fautes.append(("refus", "V6", f"{len(sans)} octet(s) de biblio/ sans rangée d'INDEX : "
                       f"{', '.join(sans[:5])} (E28)", "ajouter la rangée `nom` à biblio/INDEX.md dans le même "
                       "diff que l'octet", "-"))
    m = re.search("([0-9]+) artefacts détenus", index[:500].decode("utf-8", "ignore"))
    declare = int(m.group(1)) if m else None
    if artefacts and declare != len(artefacts) and not (declare and len(artefacts) < declare and not sans):
        fautes.append(("refus", "V6", f"compte d'en-tête de biblio/INDEX.md ({declare}) différent du compte réel "
                       f"({len(artefacts)}) (E28, S-G6)", "remesurer « N artefacts détenus » dans le même diff", "-"))


def chaine_active():
    """V7 (E28) : vrai si une chaîne de commits tourne (pgrep -f MOTIF_CHAINE) ; pgrep hors de 0 et 1 : erreur."""
    p = subprocess.run(["pgrep", "-f", MOTIF_CHAINE], capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise Erreur(f"pgrep : sortie {p.returncode}")
    return p.returncode == 0


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
    motifs(GC.lignes_ajoutees(a.depot, plage=(base, "HEAD"))[0], fautes)      # RX sur la plage poussée (E12)


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


def lieux_disque(depot):
    """SHOGEN-GARDE-DISQUE-DU-DEPOT-1 : chemins dont disque mesure le système de fichiers (os.statvfs, par
    GC.etat_disque) : le dépôt, puis TMPDIR s'il est sur un autre système de fichiers (st_dev) ; jamais / par défaut."""
    lieux = [os.path.realpath(depot)]
    tmp = os.path.realpath(os.environ.get("TMPDIR") or tempfile.gettempdir())
    if os.path.isdir(tmp) and os.stat(tmp).st_dev != os.stat(lieux[0]).st_dev:
        lieux.append(tmp)
    return lieux


def disque(a, fautes):
    for lieu in lieux_disque(a.depot):
        etat, libre = GC.etat_disque(lieu, a.min_go)
        if etat != "ok":
            fautes.append(("refus" if etat == "refus" else "avertissement", "DQ", f"{libre:.1f} Gio libres sur {lieu} "
                           "(E4)", "lister les cibles cargo des lots clos (disque --lister <dossier>), puis les "
                           "supprimer", "-"))
    for racine in a.lister:
        if GC.racine_dangereuse(racine, a.depot):
            raise Erreur("disque --lister : racine refusée (/, dépôt ou ancêtre, dossier docs, interdit)")
        for chemin, octets in cibles(racine):
            print(f"{octets / 2 ** 30:.2f} Gio" + chr(9) + chemin)



def copie_creuse(depot, dossier):
    """Copie de HEAD (git archive ; préfixes INTERDITS de la gate et *.jsonl exclus, jamais extraits) dans
    dossier/copie, dépôt git neuf dont l'index porte la copie ; le dépôt n'est que lu. Rend (copie, env de git)."""
    pre = GC.constante(os.path.join(GC.RACINE_OUTILS, "enforcement", "docs-sha256sums.py"), "INTERDITS")
    hors = [":(exclude" + (")" + p.rstrip("/") if p.endswith("/") else ",glob)" + p + "*") for p in pre]
    tar = subprocess.run(["git", "-C", depot, "archive", "--format=tar", "HEAD", "--", ".", *hors,
                          ":(exclude,glob)**/*.jsonl"], capture_output=True)
    copie, env = os.path.join(dossier, "copie"), dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    os.makedirs(copie)
    if tar.returncode or subprocess.run(["tar", "-x", "-C", copie], input=tar.stdout, capture_output=True).returncode:
        raise Erreur("git archive ou tar : copie creuse non faite")
    git(copie, "init", "-q", env=env)
    git(copie, "add", "-A", env=env)
    return copie, env


def motif_r13():
    """(motif, exclusions) de l'étape R-13 du job g5 de gates.yml des outils : lus, jamais recopiés (E35)."""
    with open(os.path.join(GC.RACINE_OUTILS, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
        ligne = [x for x in f.read().split(chr(10)) if "git grep -nE '" in x]
    if len(ligne) != 1:
        raise Erreur("étape R-13 du job g5 introuvable dans gates.yml")
    return ligne[0].split("git grep -nE '", 1)[1].split("'", 1)[0], re.findall("':!([^']+)'", ligne[0])


def portes(depot, nom, ajouts, fautes):
    """Portes textuelles sur les seules lignes ajoutées, jamais un fichier entier (E36) : K6, motif R-13 du job g5
    hors de ses exclusions (E35) ; G5, presg5 sur celles des .md (E33). ajouts : [(chemin, [(n, ligne)])]."""
    motif, hors = motif_r13()
    juges = [(c, n, x) for c, lignes in ajouts if not any(c == h.rstrip("/") or c.startswith(h.rstrip("/") + "/")
                                                          for h in hors) for n, x in lignes]
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "ajouts"), "w", encoding="utf-8") as f:
            f.writelines(x + chr(10) for _c, _n, x in juges)
        p = subprocess.run(["grep", "-nE", "--", motif, os.path.join(d, "ajouts")], capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise Erreur(f"grep : sortie {p.returncode}")
    for c, n, _x in [juges[int(x.split(":", 1)[0]) - 1] for x in p.stdout.split(chr(10)) if x]:
        fautes.append(("refus", "K6", f"{nom} : {c}:{n} : marqueur de dette nu (motif R-13 du job g5, E35)",
                       "mettre le mot en code, ou inscrire la dette au registre (R-13)", "-"))
    presg5(depot, [(f"{nom} : {c}", place(lignes)) for c, lignes in ajouts if c.endswith(".md")], fautes)


def blanc(a, fautes):
    """RECALAGE-CHECK (E30, E31, E36) : chaque diff, dans l'ordre, sur une copie creuse de HEAD qui porte déjà les
    précédents (K0, K5, K6, G5)."""
    if not a.script:
        raise Erreur("chaine --blanc : --script exigé")
    plan = [x for x in lire(a.plan).decode("utf-8").split(chr(10)) if x.strip()] if a.plan else []
    diffs = a.diffs or [d for x in plan for d in x.split("|")[1].split(",")]
    if not diffs:
        raise Erreur("chaine --blanc : aucun diff (--diffs, ou --plan)")
    with tempfile.TemporaryDirectory() as d:
        copie, env = copie_creuse(a.depot, d)
        for x in diffs:
            texte, nom = lire(x).decode("utf-8"), os.path.basename(x)
            try:
                noms = chemins_du_patch(copie, texte, x)
            except Erreur:      # patch illisible : aucun message de git recopié (un chemin interdit n'est pas nommé)
                noms = None
            if noms and any(GC.chemin_interdit(os.path.join(os.path.abspath(a.depot), c)) for c in noms):
                fautes.append(("refus", "K0", f"{nom} : fichier(s) sous un interdit (ni lus ni nommés)",
                               "retirer ces fichiers du diff", "-"))
                return
            p = subprocess.run(["git", "-C", copie, "apply", "--check", os.path.abspath(x)], capture_output=True,
                               text=True, env=env)
            if noms is None or p.returncode:
                raison = (p.stderr.strip() + chr(10)).split(chr(10))[0][:160] if noms is not None else "patch illisible"
                fautes.append(("refus", "K5", f"{nom} ne s'applique pas sur HEAD plus les diffs qui le précèdent "
                               f"(E30, E31) : {raison}", "refaire le "
                               "diff sur l'état d'après les précédents, chemins a/ et b/ relatifs au dépôt, saut de "
                               "ligne final", "-"))
                return
            git(copie, "apply", os.path.abspath(x), env=env)
            portes(a.depot, nom, [(f["apres"], f["ajouts"]) for f in GC.analyser_diff(texte) if f["apres"]], fautes)


def chaine(a, fautes):
    if (a.plan is None) != (a.cc is None) or not (a.plan or a.blanc):
        raise Erreur("chaine : --plan et --cc ensemble, ou --blanc --script S --diffs D...")
    if a.blanc:
        blanc(a, fautes)
    if a.plan is None:
        return
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
    ids = [ligne.split("|")[0] for ligne in plan]
    doubles = sorted({x for x in ids if ids.count(x) > 1})      # contre-contrôle, R-5
    if doubles:
        fautes.append(("refus", "G4", f"Diff-Id porté par plus d'un pas du plan : {', '.join(doubles)} (la "
                       "reprise sauterait les suivants sans rien dire)", "donner à chaque pas un identifiant propre",
                       "-"))
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


ANNEXE = os.path.join("docs", "adr-0028", "ANNEXE-B-items.md")
GIT_NOMME = re.compile("(?<![A-Za-z0-9_./-])git(?: -[Cc] [^ ]+| --no-pager| --no-optional-locks"
                       "| --(?:git-dir|work-tree)=[^ ]+)* (?:diff|log|show|status|ls-files|ls-tree|read-tree|archive"
                       "|apply|grep|rev-list|rev-parse|cat-file|blame|add|commit|checkout|restore|stash|reset|clone"
                       "|worktree)(?![A-Za-z-])|(?i:commandes? git)(?![A-Za-z-])")
REGLE_GIT = "liste explicite de chemins"
SUJET = ("(?:(?<![A-Za-zà-ÿ])(?i:le|la|les|l'|l’) ?(?i:cc|contre-contrôle(?:ur)?|g2|relecture|réviseur|générateur"
         "|worker|advisor|avis|lecteur|rapport|chercheur|validateur)s?|(?<![A-Za-z0-9-])[A-Z][A-Z0-9]+-[A-Z0-9]+"
         "(?:-[A-Z0-9]+)*)"
         "(?![A-Za-zà-ÿ0-9-])")
VERBE = ("(?<![a-zà-ÿ])(?i:dit|disent|trouvée?s?|relève|relèvent|relevée?s?|signale|signalent|signalée?s?|constate"
         "|constatent|constatée?s?|rapporte|rapportent|rapportée?s?|mesurée?s?|montrée?s?|notée?s?)(?![a-zà-ÿ])")
RELAIS = re.compile(SUJET + "[^.;:" + chr(10) + "]{0,40}?" + VERBE + "|(?<![a-zà-ÿ])(?i:selon|d'après|d’après) " + SUJET)
REF = re.compile("[A-Za-z0-9_-][.][A-Za-z0-9]+`?(?::| l[.] ?)[0-9]+|(?:JOURNAL|annexe B|ADR-[0-9]{4}) l[.] ?[0-9]+")
REF_LIGNE = re.compile("(?<![A-Za-z0-9_./~-])((?:/|[.]?[A-Za-z0-9_-]+/)[A-Za-z0-9_./~-]*[.][A-Za-z0-9]+)(?::|`? l[.] ?)"
                       "([0-9]+)(?:-([0-9]+))?")
PRODUIRE = re.compile("(?i)(?<![a-zà-ÿ])(?:produire|produit|produits|créer|crée|créé|créés|écrire|écris|écrit|écrits"
                      "|ajouter|ajoute|ajouté|ajoutés|nouveau|nouvelle|nouveaux|neuf|neuve|poser|pose|posé|sortie"
                      "|sorties|verser|versé|à faire)(?![a-zà-ÿ])")


def resoudre(depot, base, chemin):
    """Chemin réel d'un nom du brief (absolu, ou sous le dépôt, le dossier du brief ou son parent) ; None si absent ou
    interdit (jamais lu) ; '' si la base est inconnue (premier composant absent de la racine du dépôt)."""
    essais = [chemin] if os.path.isabs(chemin) else [os.path.join(d, chemin) for d in (depot, base, os.path.dirname(base))]
    if any(GC.chemin_interdit(x) for x in essais):
        return None
    trouve = next((x for x in essais if os.path.exists(x)), None)
    connue = os.path.isabs(chemin) or os.path.exists(os.path.join(depot, chemin.split("/")[0]))
    return trouve if trouve or not connue else ""


def faisable(a, texte, fautes):
    """B3 (E23) : chemins, lignes, commits et sous-commandes nommés par le brief."""
    base, lignes = os.path.dirname(os.path.abspath(a.texte)), texte.split(chr(10))
    for n, ligne in enumerate(lignes, 1):
        for m in REF_LIGNE.finditer(ligne):
            p = resoudre(a.depot, base, m[1])
            if p and os.path.isfile(p):
                with open(p, encoding="utf-8", errors="replace") as f:
                    total = f.read().count(chr(10))
                if not 1 <= int(m[2]) <= int(m[3] or m[2]) <= total:
                    fautes.append(("refus", "B3", f"l.{n} : {m[0]} hors du fichier ({total} lignes) (E23)",
                                   "relire le fichier et citer une ligne qui existe", "-"))
            elif p == "" or (p and not os.path.isfile(p)):
                fautes.append(("refus", "B3", f"l.{n} : {m[1]} absent (E23)", "nommer un fichier qui existe", "-"))
        for x in re.findall("`([A-Za-z0-9_./~-]*/[A-Za-z0-9_./~-]*)`", ligne):
            if x.startswith("-") or PRODUIRE.search(ligne) or resoudre(a.depot, base, x.rstrip("/")) != "":
                continue
            fautes.append(("refus", "B3", f"l.{n} : {x} absent (E23)",
                           "vérifier le chemin (avant_acte.py existe <nom>) ou écrire qu'il est à produire", "-"))
        for m in SHA.finditer(ligne):
            if "sha256" not in ligne[max(0, m.start() - 16):m.start()] and not resolu(a.depot, m[1]):
                fautes.append(("refus", "B3", f"l.{n} : {m[1]} n'est pas un commit du dépôt (E23)",
                               "lire l'identifiant par git log avant de l'écrire", "-"))
        for c in re.findall("avant_acte[.]py(?: --depot [^ ]+)? ([a-z]+)", ligne):
            if c not in COMMANDES:
                fautes.append(("refus", "B3", f"l.{n} : sous-commande avant_acte.py {c} inconnue (E23)",
                               "nommer une sous-commande de avant_acte.py --help", "-"))


def brief(a, fautes):
    """B1 (E6) et B4 (E24) sur le brief F ; --fiche NOM : fiche .claude/agents/NOM.md, qui doit exister (C-2)."""
    texte = lire(a.texte).decode("utf-8")
    if a.fiche:
        chemin = os.path.join(a.depot, ".claude", "agents", a.fiche + ".md")
        if not re.fullmatch("[a-z0-9-]+", a.fiche) or not os.path.isfile(chemin):
            raise Erreur(f"brief --fiche : fiche {a.fiche} absente de .claude/agents/")
    etats, propres = GC.etat_items(lire(os.path.join(a.depot, ANNEXE)).decode("utf-8")), GC.etat_items(texte)
    for item in sorted(propres):
        etat, n = etats.get(item, (None, 0))
        if etat is None:
            fautes.append(("avertissement", "B1", f"{item} absent de l'annexe B", "", "-"))
        elif etat == "fermé" and propres[item][0] != "fermé":
            fautes.append(("refus", "B1", f"{item} cité ouvert ; fermé à l'annexe B l.{n} (E6)",
                           "relire la ligne de l'annexe, retirer l'item du brief ou l'écrire fermé", "-"))
    if GIT_NOMME.search(texte) and REGLE_GIT not in GC.plier(texte):      # le brief lui-même (C-2)
        fautes.append(("refus", "B4", "le brief nomme une commande git sans porter lui-même la règle « toute commande "
                       "git limitée à une liste explicite de chemins » ; elle vaut pour tout brief, quelle que soit la "
                       f"fiche ({a.fiche or 'aucune'}) : une fiche qui la porte ne suffit pas (E24)",
                       "ajouter la règle au brief : toute commande git qui liste ou compare des chemins est limitée à "
                       "une liste explicite de chemins", "-"))
    lignes = texte.split(chr(10)) + [""]
    for n, ligne in enumerate(lignes[:-1], 1):
        relais = RELAIS.search(GC.MASQUE.sub(lambda m: " " * len(m[0]), ligne))      # hors citations et code
        if relais and not REF.search(ligne + " " + lignes[n]):
            fautes.append(("refus", "B2", f"l.{n} : constat relayé sans fichier ni ligne : {relais[0]} (E22)", "citer la pièce du constat (chemin:N) ou le nommer exactement", "-"))
    faisable(a, texte, fautes)


REFUS_TSV = os.path.join("scripts", "controle", "garde", "refus.tsv")
CROCHET = os.path.join(GC.RACINE_OUTILS, ".claude", "hooks", "garde_faits.py")


def regles_du_crochet(chemin=CROCHET):
    """Règles du crochet GARDE-FAITS (R1, R2…) nommées dans la docstring de son module, triées par numéro."""
    doc = ast.get_docstring(ast.parse(lire(chemin).decode("utf-8"))) or ""
    return sorted(set(re.findall("(?<![A-Za-z0-9-])(R[0-9]+)(?![0-9])", doc)), key=lambda r: int(r[1:]))


def refus(a, fautes):
    """refus [--depuis AAAA-MM-JJ] [--journal F] (phase 3, SHOGEN-GARDE-FOUS-ORCH-1) : relevé du journal des refus du
    crochet (REFUS_TSV du dépôt) : refus par règle et par jour, dix actes refusés les plus fréquents, règles du crochet
    sans refus depuis trente jours (date -u), passages (permis, erreur) ; ligne illisible comptée ; journal absent : 3."""
    if a.depuis and not re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", a.depuis):
        raise Erreur("refus --depuis : AAAA-MM-JJ")
    brut = [x for x in lire(a.journal or os.path.join(a.depot, REFUS_TSV)).decode("utf-8", "replace").split(chr(10))
            if x.strip() and not x.startswith("heure" + chr(9))]
    lignes = [c for c in (x.split(chr(9)) for x in brut) if len(c) == 5 and re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}T", c[0])]
    vus = [x for x in lignes if x[0][:10] >= (a.depuis or "")]
    regle = lambda x: re.fullmatch("R[0-9]+", x[2]) is not None      # noqa: E731
    numero = lambda r: int(r[1:])      # noqa: E731
    refuses = [x for x in vus if regle(x)]
    print(f"journal des refus : {len(lignes)} ligne(s) lue(s), {len(brut) - len(lignes)} illisible(s) ; depuis "
          f"{a.depuis or 'le début'} : {len(refuses)} refus")
    print("refus par règle et par jour :")
    par_jour = collections.Counter((x[0][:10], x[2]) for x in refuses)
    for (jour, r), n in sorted(par_jour.items(), key=lambda kv: (kv[0][0], numero(kv[0][1]))):
        print(f"  {jour}{chr(9)}{r}{chr(9)}{n}")
    print("actes refusés les plus fréquents (dix au plus) :")
    for acte, n in sorted(collections.Counter(x[3] for x in refuses).items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
        regles = ",".join(sorted({x[2] for x in refuses if x[3] == acte}, key=numero))
        print(f"  {n}{chr(9)}{regles}{chr(9)}{acte}")
    borne = (GC.maintenant() - timedelta(days=30)).strftime("%Y-%m-%d")
    actives = {x[2] for x in lignes if regle(x) and x[0][:10] >= borne}
    muettes = [r for r in regles_du_crochet() if r not in actives]
    print(f"règles sans refus depuis trente jours (depuis le {borne}, candidates à relire) : {', '.join(muettes) or '-'}")
    passages = [x[2] for x in vus if x[2] in ("permis", "erreur")]
    print(f"passages : {len(passages)} (dont {passages.count('erreur')} erreur(s) interne(s), acte permis sans contrôle)")


COMMANDES = {"sceller": sceller, "commit": commit, "diff": diff, "verser": verser, "pousser": pousser,
             "publier": publier, "existe": existe, "disque": disque, "chaine": chaine, "brief": brief,
             "motifs": motifs_arbre, "refus": refus}


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
    p.add_argument("--lecture-seule", action="store_true")
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sceller")
    s.add_argument("--tete", action="store_true")
    s.add_argument("--verif")
    c = sp.add_parser("commit")
    c.add_argument("--message", required=True)
    c.add_argument("--source", action="append", required=True)
    c.add_argument("--diff", action="append", default=[])
    c.add_argument("--id")
    s = sp.add_parser("diff")
    s.add_argument("--fichier", required=True)
    s.add_argument("--rapport")
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
    s.add_argument("--plan")
    s.add_argument("--cc")
    s.add_argument("--duree-pas", type=float, default=6)
    s.add_argument("--detache", action="store_true")
    s.add_argument("--blanc", action="store_true")
    s.add_argument("--script")
    s.add_argument("--diffs", nargs="+", default=[])
    s = sp.add_parser("brief")
    s.add_argument("--texte", required=True)
    s.add_argument("--fiche")
    sp.add_parser("motifs").add_argument("--arbre", action="store_true", required=True)
    s = sp.add_parser("refus")
    s.add_argument("--depuis")
    s.add_argument("--journal")
    return p


def journal_lecture_seule(a, verdict):
    """SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 : une ligne par passage en --lecture-seule au journal JOURNAL_LS des outils
    (heure lue par date -u, sous-commande, tête du dépôt lu ou -, verdict : conforme, refus, erreur) ; le dépôt lu
    n'est pas écrit."""
    try:
        tete = git(a.racine, "rev-parse", "--verify", "HEAD").strip()
    except Erreur:
        tete = "-"
    ligne = [GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ"), a.cmd, tete, verdict]
    with open(JOURNAL_LS, "a", encoding="utf-8") as f:
        f.write(chr(9).join(ligne) + chr(10))


def main(argv=None):
    try:
        a = parseur().parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    a.racine = a.depot
    code = _jouer(a)
    if a.lecture_seule:
        try:
            journal_lecture_seule(a, {0: "conforme", 1: "refus"}.get(code, "erreur"))
        except Exception as e:      # journal de lecture seule non écrit : erreur de l'outil, jamais 0 ni 1
            print(f"ERREUR journal de lecture seule : {type(e).__name__} : {e}", file=sys.stderr)
            return 3
    return code


def _jouer(a):
    """Sous-commande jouée (dépôt jetable sous --lecture-seule), fautes imprimées, journal du dépôt : 0, 1 ou 3."""
    fautes = []
    with contextlib.ExitStack() as pile:
        try:
            if a.lecture_seule:
                if a.cmd not in ("diff", "commit"):
                    raise Erreur("--lecture-seule : diff et commit seulement")
                a.depot = jetable(a.racine, pile.enter_context(tempfile.TemporaryDirectory()), a.cmd == "commit")
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
