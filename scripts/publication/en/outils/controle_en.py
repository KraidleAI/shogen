# -*- coding: utf-8 -*-
"""Contrôle de la traduction anglaise du brouillon public de docs/11 (lot DOCS11-EN).

Rattachement : brief du lot DOCS11-EN (sha256 cfe6c0d5…0e69), points 1 à 7 ; JOURNAL, entrée du 2026-10-04
15:16:03 UTC ; G0 docs/adr-0029/G0-lots-S2BIS.md (ligne DOCS11-PUBLIC) ; annexe B.57 d'ADR-0028 ; outillage du lot
DOCS11-PUBLIC (controle_public.py) pour les motifs interdits et le registre.

Onze contrôles, tous bloquants :
   1. structure et alignement : mêmes unités (titres, paragraphes, éléments de liste, lignes de table, blocs de
      code, paragraphes de citation) dans le même ordre ; titres traduits selon le glossaire ; blocs de code
      identiques à l'octet ; mêmes codes en ligne par unité ; même nombre de cellules par ligne de table ;
   2. nombres : par unité, le multiensemble des nombres normalisés (virgule décimale française ou point anglais,
      espace française ou virgule anglaise de milliers, codes en ligne et blocs de code bruts, citations gardées
      lues à la française, gloses exclues) est identique, et les nombres s'y suivent dans le même ordre ; de même
      pour les nombres écrits en lettres (multiensemble) ;
   3. citations : chaque citation « … » de la source est gardée à l'identique (espaces normalisées) ou traduite
      selon la liste déclarée, dans la même unité ; aucune autre citation ;
   4. gloses : chaque passage gardé en français porte sa glose déclarée à sa première occurrence, une seule fois ;
      aucune glose non déclarée ; aucune glose n'ajoute de nombre ; toute citation gardée est glosée, neutre ou
      couverte ;
   5. passages protégés et libellés de verdict : mêmes comptes dans la source et dans la traduction ;
   6. motifs interdits (lot DOCS11-PUBLIC et équivalents anglais) : 0 occurrence ;
   7. registre du doc 09 transposé en anglais (dont les 15 locutions de la gate S-G4) : 0 hors exceptions motivées,
      citations traduites et gloses comprises ;
   8. résidus français : aucun mot-outil français dans les zones anglaises ;
   9. convention des nombres : aucune virgule décimale ni espace de milliers à la française en zone anglaise ;
  10. en-tête anglais (brief, point 6) ;
  11. glossaire final : tables identiques au glossaire fixé.

Contrat de sortie : 0 tous les contrôles passent ; 1 au moins un échoue ; 3 erreur fatale (entrée illisible,
glossaire incohérent avec la source, document malformé : bloc de code ou guillemet non fermé, accent grave impair).

Aucune barre oblique inverse n'est écrite dans ce fichier (SHOGEN-HARNAIS-ECHAPPEMENTS-1).

Usage : python3 -B controle_en.py SOURCE TRADUCTION [--table SORTIE]
"""
import collections
import hashlib
import importlib
import os
import re
import sys

NL = chr(10)
TAB = chr(9)
CR = chr(13)
BS = chr(92)
NUL = chr(0)
SEP_VECTEUR = chr(31)
OUV = chr(0xAB)
FER = chr(0xBB)
LDQ = chr(0x201C)
RDQ = chr(0x201D)
CLOTURE = "```"


class ErreurFatale(Exception):
    """Entrée inexploitable : le contrôle ne conclut pas (sortie 3)."""


Unite = collections.namedtuple("Unite", "genre texte ligne")


def normaliser_espaces(s):
    return " ".join(s.split())


# --- Unités ----------------------------------------------------------------------------------------------------------

RE_TITRE = re.compile("^#{1,6} ")
RE_LISTE = re.compile("^ {0,3}(?:[-*] |[0-9]+[.] )")


def est_delimiteur(ligne):
    """Ligne de délimitation d'une table Markdown : « | », « - », « : » et espaces seulement, au moins un « - »."""
    return ligne.startswith("|") and "-" in ligne and set(ligne.strip()) <= set("|-: ")


def unites(texte):
    """Découpe en unités : titre, para, liste, table (une ligne), code (bloc entier), bloc (paragraphe de citation)."""
    lignes = texte.split(NL)
    res = []
    courant = []

    def fermer():
        if courant:
            genre, ls, debut = courant[0]
            res.append(Unite(genre, NL.join(ls), debut))
            courant.clear()

    i = 0
    dans_table = False
    while i < len(lignes):
        ligne = lignes[i]
        if not (ligne.startswith("|") and dans_table):
            dans_table = False
        if ligne.startswith(CLOTURE):
            fermer()
            j = i + 1
            while j < len(lignes) and not lignes[j].startswith(CLOTURE):
                j += 1
            if j >= len(lignes):
                raise ErreurFatale("bloc de code non fermé (l." + str(i + 1) + ")")
            res.append(Unite("code", NL.join(lignes[i:j + 1]), i + 1))
            i = j + 1
            continue
        if not ligne.strip():
            fermer()
        elif RE_TITRE.match(ligne):
            fermer()
            res.append(Unite("titre", ligne, i + 1))
        elif ligne.startswith("|") and (dans_table or (i + 1 < len(lignes) and est_delimiteur(lignes[i + 1]))):
            fermer()
            res.append(Unite("table", ligne, i + 1))
            dans_table = True
        elif ligne.startswith(">"):
            contenu = ligne[1:]
            if contenu.startswith(" "):
                contenu = contenu[1:]
            if courant and courant[0][0] == "bloc":
                if contenu.strip():
                    courant[0][1].append(contenu)
                else:
                    fermer()
            else:
                fermer()
                if contenu.strip():
                    courant.append(("bloc", [contenu], i + 1))
        elif RE_LISTE.match(ligne):
            fermer()
            courant.append(("liste", [ligne], i + 1))
        elif courant and courant[0][0] in ("para", "liste"):
            courant[0][1].append(ligne)
        else:
            fermer()
            courant.append(("para", [ligne], i + 1))
        i += 1
    fermer()
    return res


# --- Masques ---------------------------------------------------------------------------------------------------------

RE_CODE_LIGNE = re.compile("`[^`" + NL + "]*`")
CROCHET_O, CROCHET_F, ETOILE = re.escape("["), re.escape("]"), re.escape("*")
RE_GLOSE = re.compile(CROCHET_O + ETOILE + "(.*?)" + ETOILE + CROCHET_F)


def blanchir_blocs_code(texte):
    """Remplace les lignes des blocs de code (clôtures comprises) par des espaces de même longueur."""
    sortie, dedans = [], False
    for ligne in texte.split(NL):
        if ligne.startswith(CLOTURE):
            dedans = not dedans
            sortie.append(" " * len(ligne))
        else:
            sortie.append(" " * len(ligne) if dedans else ligne)
    return NL.join(sortie)


def masquer_code(texte):
    """Masque les codes en ligne par des NUL de même longueur ; rend (masque, codes). Accent grave impair : fatal."""
    codes = []

    def remplacer(m):
        codes.append(m.group(0))
        return NUL * len(m.group(0))

    masque = RE_CODE_LIGNE.sub(remplacer, texte)
    if "`" in masque:
        n = texte.count(NL, 0, masque.index("`")) + 1
        raise ErreurFatale("accent grave impair (l." + str(n) + ")")
    return masque, codes


def gloses(texte):
    return [(m.start(), m.end(), m.group(1)) for m in RE_GLOSE.finditer(texte)]


def retirer_gloses(texte):
    return re.sub(" ?" + RE_GLOSE.pattern, "", texte)


def masquer_gloses(texte):
    return RE_GLOSE.sub(lambda m: NUL * len(m.group(0)), texte)


def spans_imbriques(masque, ouvrant, fermant):
    spans, pile = [], []
    for i, c in enumerate(masque):
        if c == ouvrant:
            pile.append(i)
        elif c == fermant:
            if not pile:
                raise ErreurFatale("guillemet fermant sans ouvrant (l." + str(masque.count(NL, 0, i) + 1) + ")")
            debut = pile.pop()
            if not pile:
                spans.append((debut, i + 1))
    if pile:
        raise ErreurFatale("guillemet ouvrant non fermé (l." + str(masque.count(NL, 0, pile[0]) + 1) + ")")
    return spans


def _masque_citations(texte):
    masque, _ = masquer_code(blanchir_blocs_code(texte))
    return masquer_gloses(masque)


def citations_fr(texte):
    """Citations « … » de premier niveau, hors codes et gloses : (début, fin, contenu à espaces normalisées)."""
    masque = _masque_citations(texte)
    return [(a, b, normaliser_espaces(texte[a + 1:b - 1])) for a, b in spans_imbriques(masque, OUV, FER)]


def citations_en(texte):
    """Citations “ … ” de premier niveau, hors codes, gloses et citations « … » ; une paire vide n'est pas une citation."""
    masque = list(_masque_citations(texte))
    for a, b in spans_imbriques("".join(masque), OUV, FER):
        for k in range(a, b):
            masque[k] = NUL
    res = []
    for a, b in spans_imbriques("".join(masque), LDQ, RDQ):
        contenu = normaliser_espaces(texte[a + 1:b - 1])
        if contenu:
            res.append((a, b, contenu))
    return res


# --- Nombres ---------------------------------------------------------------------------------------------------------

SUP = "".join(chr(c) for c in [0x2070, 0x00B9, 0x00B2, 0x00B3] + list(range(0x2074, 0x207A)))
SUB = "".join(chr(c) for c in range(0x2080, 0x208A))
CHIFFRES = "0123456789" + SUP + SUB
CLASSE = "0-9A-Za-z_" + SUP + SUB + chr(0x207B)
SEPARATEURS = re.escape(".,:/+" + chr(0xB7) + "-")
RE_COMPOSITE = re.compile("[" + CLASSE + "]+(?:[" + SEPARATEURS + "][" + CLASSE + "]+)*")
RE_CHIFFRES = re.compile("[0-9]+")
RE_FR_VECTEUR = re.compile(CROCHET_O + "[0-9]+(?: [0-9]+)+" + CROCHET_F)
RE_FR_GROUPE = re.compile("(?<![0-9A-Za-z.,])[0-9]{1,3}(?: [0-9]{3})+(?![0-9])")
RE_FR_DECIMALE = re.compile("(?<![0-9A-Za-z.,])([0-9]+),([0-9]+)(?![0-9])")
RE_EN_GROUPE = re.compile("(?<![0-9A-Za-z.,])[0-9]{1,3}(?:,[0-9]{3})+(?![0-9])")


def normaliser_nombres(texte, langue):
    """Forme canonique : point décimal, aucun séparateur de milliers ; « brut » : inchangé."""
    if langue == "brut":
        return texte
    if langue == "fr":
        t = RE_FR_VECTEUR.sub(lambda m: m.group(0).replace(" ", SEP_VECTEUR), texte)
        t = RE_FR_GROUPE.sub(lambda m: m.group(0).replace(" ", ""), t)
        t = RE_FR_DECIMALE.sub(lambda m: m.group(1) + "." + m.group(2), t)
        return t.replace(SEP_VECTEUR, " ")
    if langue == "en":
        return RE_EN_GROUPE.sub(lambda m: m.group(0).replace(",", ""), texte)
    raise ErreurFatale("langue inconnue : " + str(langue))


def jetons(texte):
    """Multiensemble des jetons numériques : composites (« c ») et suites de chiffres ASCII (« d »)."""
    compte = collections.Counter()
    for m in RE_COMPOSITE.finditer(texte):
        if any(ch in CHIFFRES for ch in m.group(0)):
            compte[("c", m.group(0))] += 1
    for m in RE_CHIFFRES.finditer(texte):
        compte[("d", m.group(0))] += 1
    return compte


LANGUE = {"b": "brut", "f": "fr", "e": "en"}


def etiquettes(texte, cote):
    """Langue de chaque caractère : b code en ligne, x glose (exclue), f français, e anglais."""
    lab = ["f" if cote == "fr" else "e"] * len(texte)
    masque, _ = masquer_code(texte)
    for i, ch in enumerate(masque):
        if ch == NUL:
            lab[i] = "b"
    if cote == "en":
        for m in RE_GLOSE.finditer(masque):
            debut = m.start() - 1 if m.start() > 0 and texte[m.start() - 1] == " " else m.start()
            for k in range(debut, m.end()):
                lab[k] = "x"
        for a, b in spans_imbriques(masquer_gloses(masque), OUV, FER):
            for k in range(a, b):
                if lab[k] == "e":
                    lab[k] = "f"
    return lab


def segments(texte, cote):
    lab = etiquettes(texte, cote)
    segs = []
    for k, ch in enumerate(texte):
        if segs and segs[-1][0] == lab[k]:
            segs[-1][1].append(ch)
        else:
            segs.append((lab[k], [ch]))
    return [(l, "".join(cs)) for l, cs in segs]


def sequence_unite(unite, cote):
    """Suite ordonnée des nombres composites de l'unité (mêmes zones et normalisations que jetons_unite)."""
    if unite.genre == "code":
        morceaux = [("b", unite.texte)]
    else:
        morceaux = segments(unite.texte, cote)
    suite = []
    for lab, seg in morceaux:
        if lab == "x":
            continue
        texte = normaliser_nombres(seg, LANGUE[lab])
        suite.extend(m.group(0) for m in RE_COMPOSITE.finditer(texte) if any(ch in CHIFFRES for ch in m.group(0)))
    return suite


def jetons_unite(unite, cote):
    if unite.genre == "code":
        return jetons(unite.texte)
    total = collections.Counter()
    for lab, seg in segments(unite.texte, cote):
        if lab != "x":
            total.update(jetons(normaliser_nombres(seg, LANGUE[lab])))
    return total


MOTS_FR = {"zéro": "0", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6", "sept": "7", "huit": "8",
           "dix": "10", "onze": "11", "douze": "12", "treize": "13", "quatorze": "14", "quinze": "15", "seize": "16",
           "vingt": "20", "trente": "30", "quarante": "40", "cinquante": "50", "soixante": "60", "cent": "100",
           "mille": "1000", "premier": "1er", "première": "1er", "premiers": "1er", "premières": "1er",
           "second": "2e", "seconde": "2e", "seconds": "2e", "secondes": "2e", "deuxième": "2e", "deuxièmes": "2e",
           "troisième": "3e", "quatrième": "4e", "cinquième": "5e", "moitié": "1/2"}
# « neuf » n'est pas compté : sa seule occurrence dans la source signifie « nouveau » (« un G0 neuf », l.69).
MOTS_EN = {"zero": "0", "two": "2", "both": "2", "twice": "2", "three": "3", "four": "4", "five": "5", "six": "6",
           "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
           "fourteen": "14", "fifteen": "15", "sixteen": "16", "twenty": "20", "thirty": "30", "forty": "40",
           "fifty": "50", "sixty": "60", "hundred": "100", "thousand": "1000", "first": "1er", "second": "2e",
           "third": "3e", "fourth": "4e", "fifth": "5e", "half": "1/2"}
LETTRES = "A-Za-zÀ-ÖØ-öø-ÿ"
RE_MOT = re.compile("[" + LETTRES + "]+")


def mots_nombres(texte, langue):
    table = MOTS_FR if langue == "fr" else MOTS_EN
    compte = collections.Counter()
    for m in RE_MOT.finditer(texte):
        avant = texte[m.start() - 1] if m.start() > 0 else " "
        apres = texte[m.end()] if m.end() < len(texte) else " "
        if avant == "-" or apres == "-":
            continue
        if langue == "en" and m.group(0).lower() == "third" and texte[m.end():m.end() + 6].lower() == " party":
            continue
        if langue == "en" and m.group(0).lower() == "third" and texte[m.end():m.end() + 8].lower() == " parties":
            continue
        valeur = table.get(m.group(0).lower())
        if valeur:
            compte[valeur] += 1
    return compte


def mots_unite(unite, cote):
    if unite.genre == "code":
        return mots_nombres(unite.texte, "fr")
    total = collections.Counter()
    for lab, seg in segments(unite.texte, cote):
        if lab in ("f", "e"):
            total.update(mots_nombres(seg, LANGUE[lab]))
    return total


# --- Motifs interdits (lot DOCS11-PUBLIC, contrôle 2, et équivalents anglais) ----------------------------------------

BARRE = re.escape(BS)
NON_ESPACE = "[^ " + TAB + NL + CR + "]"

MOTIFS = [
    ("chemin local", "lecteur Windows suivi d'une barre", "(?<![0-9A-Za-z])[A-Za-z]:[/" + BARRE + "]", False),
    ("chemin local", "lecteur C:, D: ou F: accolé", "(?<![0-9A-Za-z_])[CDF]:(?=" + NON_ESPACE + ")", False),
    ("chemin local", "barre oblique inverse", BARRE, False),
    ("chemin local", "dossier d'utilisateur Windows", "Users" + BARRE + "|kacimi", True),
    ("bac à sable", "/tmp", "/tmp|tmp/", False),
    ("bac à sable", "scratchpad", "scratchpad", True),
    ("bac à sable", "racine d'hôte (/home, /root, /mnt)", "/home/|/root/|/mnt/", False),
    ("bac à sable", "dossier de session du harnais", "7ba84933|claude-0", True),
    ("dossier non public", "docs/15-*", "docs/15|15-etude", True),
    ("dossier non public", "docs/16-*", "docs/16|16-plan", True),
    ("dossier non public", "docs/rapports/", "rapports/", True),
    ("dossier non public", "ADR-0025 (docs/adr-0025/)", "adr-0025", True),
    ("dossier non public", "docs/adr-0028/monark-m009a/", "monark-m009a", True),
    ("dossier non public", "Pocket", "pocket|pokt", True),
    ("pièce D.2", "n° 1 : dossier shogen-j28", "shogen-j28|baseline_step0|campagne-copie", True),
    ("pièce D.2", "n° 2 et 12 : mesure M009a", "measure-m009a|lot-m009|adr-m002|hikae|ukemi|m009 measured", True),
    ("pièce D.2", "n° 3 et 4 : cartographie hors dépôt",
     "shogen-carto|campagne[.]md|cache_|_result[.]json|_workflow-output", True),
    ("pièce D.2", "n° 5 : cartographie l.51", "cartographie-20|5cc89b56", True),
    ("pièce D.2", "n° 6 : ADR-0025 l.14", "0fe88f1a", True),
    ("pièce D.2", "n° 7 et 8 : dossier de campagne",
     "shogen-campagne|J0-STATUS|LISEZ-MOI|REPAIR-|INCIDENT-|CLOTURE-20|SHA256SUMS-cloture|shogen-g2-lot", False),
    ("pièce D.2", "n° 8 : étude hors dépôt",
     "ARCHIVE-shogen|shogen-interne|AVIS-advisor-2026-09-26|PRODUITS|etude-2026-09-25", False),
    ("pièce D.2", "n° 10 : registre PAROXYSME", "paroxysme-shogen|a655c401", True),
    ("pièce D.2", "n° 11 : transcription de session", "013dvmub", True),
    ("pièce D.2", "n° 12 : commit aa04924", "aa04924", True),
    ("pièce D.2", "Drive", "(?<![0-9A-Za-z])Drive(?![0-9A-Za-z])", False),
    ("dépôt privé", "organisation KraidleAI", "kraidleai", True),
    ("dépôt privé", "monark-governance", "monark-governance", True),
    ("identifiant", "session_", "session_", True),
    ("identifiant", "session courte 90684fb2", "90684fb2", True),
    ("identifiant", "session suivie d'un hexadécimal", "session[ `]{0,2}[0-9a-f]{6,}(?![0-9a-z])", True),
    ("identifiant", "agent carto:", "carto:", True),
    ("identifiant", "workflow wf_", "(?<![0-9A-Za-z])wf_", False),
    ("identifiant", "fiche d'agent shogen-*", "shogen-(?:worker|validateur|orchestrator|orchestrateur|devops)", True),
    ("identifiant", "lien ou marque de session", "claude[.]ai/code|claude-session", True),
    ("gouvernance interne", "priorité stratégique", "Position d'abord", False),
    ("gouvernance interne", "routage interne", "remis à l'orchestrateur", False),
    ("décision de l'investisseur", "« Pyth est mort »", "pyth est mort", True),
    ("décision de l'investisseur", "consigne verbatim « pas sur mon PC »", "pas sur mon PC|cette fois on le fait sur un VPS",
     False),
    ("décision de l'investisseur", "pièces présentées comme remises avec le rapport", "remis avec ce", False),
    # Équivalents anglais (brief DOCS11-EN, point 5).
    ("gouvernance interne (anglais)", "priorité stratégique", "position first|positioning first", True),
    ("gouvernance interne (anglais)", "routage interne",
     "(?:handed|passed|referred|returned|escalated|forwarded)(?: over| back)? to the orchestrator", True),
    ("décision de l'investisseur (anglais)", "« Pyth est mort »", "pyth (?:is|was) dead|pyth died|dead pyth", True),
    ("décision de l'investisseur (anglais)", "consigne « pas sur mon PC »",
     "not on my (?:pc|computer|machine)|this time (?:we do it )?on a vps", True),
    ("décision de l'investisseur (anglais)", "pièces présentées comme remises avec le rapport",
     "(?:provided|delivered|enclosed|attached|supplied|included|shipped|handed over) with this report", True),
    ("pièce D.2 (anglais)", "Google Drive", "google ?drive|gdrive", True),
    ("bac à sable (anglais)", "poste de travail Windows nommé", "windows workstation of|kacimi", True),
]


def motifs_trouves(texte):
    """Motifs présents : (catégorie, libellé, nombre d'occurrences, lignes)."""
    trouves = []
    for categorie, libelle, motif, insensible in MOTIFS:
        rx = re.compile(motif, re.IGNORECASE if insensible else 0)
        positions = [m.start() for m in rx.finditer(texte)]
        if positions:
            lignes = sorted({texte.count(NL, 0, p) + 1 for p in positions})
            trouves.append((categorie, libelle, len(positions), lignes))
    return trouves


# --- Registre du doc 09 transposé en anglais -------------------------------------------------------------------------

LOCUTIONS_SG4 = [
    "donnée vérifiée", "données vérifiées", "donnée vraie", "données vraies", "fait signé", "faits signés",
    "prix garanti", "sources indépendantes", "sources diverses", "niveau de sécurité du lot", "attestor décentralisé",
    "attestors décentralisés", "verified", "validated", "guaranteed",
]
LOCUTIONS_EN = [
    "independent source", "independent sources", "independent feed", "independent feeds", "diverse source",
    "diverse sources", "diverse feeds", "verified data", "validated data", "true data", "correct data", "true price",
    "correct price", "accurate price", "tells the truth", "says the truth", "signed fact", "signed facts", "prove",
    "proves", "proved", "proven", "proving", "nobody measures", "no one measures", "no-one measures", "guarantee",
    "guarantees", "guaranteeing", "ensure", "ensures", "ensured", "ensuring", "safe", "safely", "secure", "secured",
    "security level", "enforced diversity", "imposed diversity", "quality of a source", "sources are good",
    "good sources", "decentralized", "decentralised", "trustless", "trust-free", "zero trust", "reproducible",
    "publicly verifiable", "cannot panic", "high coverage",
]
RE_K_SOURCES = re.compile("(?<![0-9A-Za-z])[0-9]+ sources(?![0-9A-Za-z])")


def _borne(texte, debut, fin):
    avant = texte[debut - 1] if debut > 0 else " "
    apres = texte[fin] if fin < len(texte) else " "
    return not (avant.isalnum() or avant == "_") and not (apres.isalnum() or apres == "_")


def _admise(texte, debut, fin, cle, exceptions):
    for exc_cle, contexte, _ in exceptions:
        if exc_cle != cle:
            continue
        depart = 0
        while True:
            i = texte.find(contexte, depart)
            if i < 0:
                break
            if i <= debut and fin <= i + len(contexte):
                return True
            depart = i + 1
    return False


def registre_en(texte, exceptions):
    """Occurrences bornées des formules du registre : (locution, ligne, extrait, admise ?)."""
    bas = texte.lower()
    if len(bas) != len(texte):
        raise ErreurFatale("la mise en minuscules change la longueur du texte")
    hits = []
    for locution in LOCUTIONS_SG4 + LOCUTIONS_EN:
        cible = locution.lower()
        depart = 0
        while True:
            i = bas.find(cible, depart)
            if i < 0:
                break
            if _borne(bas, i, i + len(cible)):
                n = texte.count(NL, 0, i) + 1
                hits.append((locution, n, texte[max(0, i - 40):i + len(cible) + 40].replace(NL, " "),
                             _admise(texte, i, i + len(cible), locution, exceptions)))
            depart = i + 1
    for m in RE_K_SOURCES.finditer(texte):
        n = texte.count(NL, 0, m.start()) + 1
        hits.append(("k sources", n, texte[max(0, m.start() - 40):m.end() + 40].replace(NL, " "),
                     _admise(texte, m.start(), m.end(), "k sources", exceptions)))
    return sorted(hits, key=lambda h: (h[1], h[0]))


def zones_anglaises(texte):
    """Texte des zones anglaises : blocs de code, codes en ligne et citations « … » remplacés par des espaces."""
    base = blanchir_blocs_code(texte)
    masque, _ = masquer_code(base)
    sortie = [" " if c == NUL else c for c in masque]
    for a, b in spans_imbriques(masquer_gloses(masque), OUV, FER):
        for k in range(a, b):
            if sortie[k] != NL:
                sortie[k] = " "
    return "".join(sortie)


# --- Convention des nombres et résidus français ----------------------------------------------------------------------

RE_CONV_DECIMALE = re.compile("(?<![0-9A-Za-z.,])[0-9]+,(?:[0-9]{1,2}|[0-9]{4,})(?![0-9])")
RE_CONV_GROUPE = re.compile("(?<![0-9A-Za-z.,])[0-9]{1,3}(?: [0-9]{3})+(?![0-9])")


def convention_en(texte):
    """Formes françaises en zone anglaise : virgule décimale, espace de milliers (vecteurs entre crochets exclus)."""
    zones = zones_anglaises(texte)
    zones = RE_FR_VECTEUR.sub(lambda m: m.group(0).replace(" ", SEP_VECTEUR), zones)
    trouves = [(m.start(), m.group(0)) for m in RE_CONV_DECIMALE.finditer(zones)]
    trouves += [(m.start(), m.group(0)) for m in RE_CONV_GROUPE.finditer(zones)]
    return [(forme, zones.count(NL, 0, p) + 1) for p, forme in sorted(trouves)]


MOTS_OUTILS_FR = {
    "le", "la", "les", "des", "du", "de", "et", "est", "une", "un", "pour", "dans", "sur", "avec", "qui", "que", "pas",
    "au", "aux", "ne", "ce", "cette", "ces", "sont", "été", "être", "leur", "leurs", "sans", "mais", "ou", "où",
    "entre", "selon", "chaque", "aucun", "aucune", "depuis", "donc", "ni", "il", "elle", "ils", "par", "en", "sa",
    "son", "ses", "cet", "dont", "lors", "après", "avant", "sous", "vers", "chez", "très", "aussi", "comme", "même",
    "mêmes", "qu", "jusqu", "lorsque", "puis", "tous", "toutes", "tout", "toute",
}


def residus_francais(texte, libelles):
    """Mots-outils français en zone anglaise (libellés nus déclarés retirés ; mots accolés à - _ / . ignorés)."""
    zones = zones_anglaises(texte)
    for libelle in sorted(libelles, key=len, reverse=True):
        zones = zones.replace(libelle, " " * len(libelle))
    trouves = []
    for m in RE_MOT.finditer(zones):
        avant = zones[m.start() - 1] if m.start() > 0 else " "
        apres = zones[m.end()] if m.end() < len(zones) else " "
        if avant in "-_/." or apres in "-_/":
            continue
        if len(m.group(0)) > 1 and m.group(0).isupper():
            continue
        if m.group(0).lower() in MOTS_OUTILS_FR:
            trouves.append((m.group(0), zones.count(NL, 0, m.start()) + 1))
    return trouves


# --- Séparation de la traduction : en-tête ajouté, corps, glossaire final ------------------------------------------

def corps(texte, donnees):
    """Texte de la traduction jusqu'au titre du glossaire final (exclu)."""
    lignes = texte.split(NL)
    for i, ligne in enumerate(lignes):
        if ligne == donnees.GLOSSAIRE_TITRE:
            return NL.join(lignes[:i])
    return texte


def separer(unites_en, donnees):
    """(unités du corps, unités de l'en-tête ajouté, unités du glossaire final, problèmes)."""
    problemes = []
    fin = next((i for i, u in enumerate(unites_en) if u.genre == "titre" and u.texte == donnees.GLOSSAIRE_TITRE),
               None)
    if fin is None:
        problemes.append("glossaire final absent (titre « " + donnees.GLOSSAIRE_TITRE + " »)")
        fin = len(unites_en)
    entete = []
    if len(unites_en) > 1 and unites_en[1].genre == "bloc" and unites_en[1].texte.startswith(donnees.ENTETE_BROUILLON):
        entete.append(unites_en[1])
        if (len(unites_en) > 2 and unites_en[2].genre == "bloc"
                and unites_en[2].texte.startswith(donnees.ENTETE_CONVENTIONS)):
            entete.append(unites_en[2])
    if len(entete) != 2:
        problemes.append("en-tête anglais absent ou mal placé (deux paragraphes de citation après le titre)")
    corps_unites = unites_en[:1] + unites_en[1 + len(entete):fin]
    return corps_unites, entete, unites_en[fin:], problemes


def aligner(unites_fr, unites_en, donnees):
    problemes = []
    if len(unites_fr) != len(unites_en):
        premier = next((i for i in range(min(len(unites_fr), len(unites_en)))
                        if unites_fr[i].genre != unites_en[i].genre), min(len(unites_fr), len(unites_en)))
        problemes.append("nombre d'unités : source " + str(len(unites_fr)) + ", traduction " + str(len(unites_en))
                         + " ; premier écart de genre à l'unité " + str(premier + 1))
    return list(zip(unites_fr, unites_en)), problemes


def _cellules(ligne):
    masque, _ = masquer_code(ligne)
    return masque.count("|")


def controle_structure(paires, donnees):
    titres = dict(donnees.TITRES)
    problemes = []
    for uf, ue in paires:
        lieu = "l." + str(uf.ligne) + " / l." + str(ue.ligne)
        if uf.genre != ue.genre:
            problemes.append(lieu + " : genre " + uf.genre + " contre " + ue.genre)
            continue
        if uf.genre == "titre":
            if titres.get(uf.texte) != ue.texte:
                problemes.append(lieu + " : titre non conforme au glossaire : « " + ue.texte + " »")
        elif uf.genre == "code":
            if uf.texte != ue.texte:
                problemes.append(lieu + " : bloc de code modifié")
            continue
        elif uf.genre == "table" and _cellules(uf.texte) != _cellules(ue.texte):
            problemes.append(lieu + " : nombre de cellules " + str(_cellules(uf.texte)) + " contre "
                             + str(_cellules(ue.texte)))
        if collections.Counter(masquer_code(uf.texte)[1]) != collections.Counter(masquer_code(ue.texte)[1]):
            problemes.append(lieu + " : codes en ligne différents")
    return problemes


def _diff(a, b):
    return sorted((k[1] if isinstance(k, tuple) else k, v) for k, v in (a - b).items())


def controle_nombres(paires):
    problemes = []
    for uf, ue in paires:
        jf, je = jetons_unite(uf, "fr"), jetons_unite(ue, "en")
        lieu = "l." + str(uf.ligne) + " / l." + str(ue.ligne)
        if jf != je:
            problemes.append(lieu + " : nombres inventés " + str(_diff(je, jf)) + " ; perdus " + str(_diff(jf, je)))
        elif sequence_unite(uf, "fr") != sequence_unite(ue, "en"):
            problemes.append(lieu + " : mêmes nombres, ordre différent (échange dans l'unité)")
        mf, me = mots_unite(uf, "fr"), mots_unite(ue, "en")
        if mf != me:
            problemes.append(lieu + " : nombres en lettres en trop " + str(_diff(me, mf)) + " ; manquants "
                             + str(_diff(mf, me)))
    return problemes


# --- Citations et gloses -----------------------------------------------------------------------------------------------

def est_citation(forme):
    if not (forme.startswith(OUV) and forme.endswith(FER)):
        return False
    try:
        spans = spans_imbriques(forme, OUV, FER)
    except ErreurFatale:
        return False
    return spans == [(0, len(forme))]


def contenu_citation(forme):
    return normaliser_espaces(forme[1:-1])


def gardees(donnees):
    """Contenus des citations gardées : glosées (formes citées), neutres, couvertes."""
    glosees = {contenu_citation(f) for _, f, _, _ in donnees.GLOSES if est_citation(f)}
    return glosees, {n for n, _ in donnees.NEUTRES}, {c for c, _, _ in donnees.COUVERTS}


def controle_citations(paires, donnees):
    glosees, neutres, couverts = gardees(donnees)
    gardees_set = glosees | neutres | couverts
    traductions = {normaliser_espaces(fr): normaliser_espaces(en) for _, fr, en, _ in donnees.CITATIONS_TRADUITES}
    problemes = []
    for uf, ue in paires:
        if uf.genre == "code":
            continue
        lieu = "l." + str(uf.ligne) + " / l." + str(ue.ligne)
        attendues_g, attendues_t = collections.Counter(), collections.Counter()
        for _, _, s in citations_fr(uf.texte):
            if s in gardees_set:
                attendues_g[s] += 1
            elif s in traductions:
                attendues_t[traductions[s]] += 1
            else:
                problemes.append(lieu + " : citation de la source non déclarée : « " + s[:80] + " »")
        for _, _, s in citations_en(uf.texte):
            attendues_t[s] += 1
        trouvees_g = collections.Counter(s for _, _, s in citations_fr(ue.texte))
        trouvees_t = collections.Counter(s for _, _, s in citations_en(ue.texte))
        if trouvees_g != attendues_g:
            problemes.append(lieu + " : citations gardées en trop " + str(_diff(trouvees_g, attendues_g))
                             + " ; manquantes " + str(_diff(attendues_g, trouvees_g)))
        if trouvees_t != attendues_t:
            problemes.append(lieu + " : citations traduites en trop " + str(_diff(trouvees_t, attendues_t))
                             + " ; manquantes " + str(_diff(attendues_t, trouvees_t)))
    return problemes


def _texte_de_recherche(texte, forme, libelle):
    base = blanchir_blocs_code(texte)
    if not forme.startswith("`"):
        base, _ = masquer_code(base)
    base = masquer_gloses(base)
    if libelle:
        sortie = list(base)
        for a, b in spans_imbriques(base, OUV, FER):
            for k in range(a, b):
                sortie[k] = NUL
        base = "".join(sortie)
    return base


def controle_gloses(texte_corps, source, donnees):
    problemes = []
    declarees = {g for _, _, g, _ in donnees.GLOSES}
    for _, _, contenu in gloses(texte_corps):
        if contenu not in declarees:
            problemes.append("glose non déclarée : [*" + contenu[:80] + "*]")
    premieres = {}
    for gid, forme, glose, _ in donnees.GLOSES:
        marque = "[*" + glose + "*]"
        n = texte_corps.count(marque)
        if n != 1:
            problemes.append(gid + " : glose présente " + str(n) + " fois (une exigée)")
        libelle = gid in donnees.REGEX_LIBELLES
        rx = re.compile(donnees.REGEX_LIBELLES[gid] if libelle else re.escape(forme))
        m = rx.search(_texte_de_recherche(texte_corps, forme, libelle))
        if m is None:
            problemes.append(gid + " : forme absente de la traduction")
            continue
        premieres[gid] = (m.start(), m.end())
        suite = texte_corps[m.end():].lstrip("*")
        if not suite.startswith(" " + marque):
            problemes.append(gid + " : glose absente à la première occurrence (l."
                             + str(texte_corps.count(NL, 0, m.start()) + 1) + ")")
        langue = "brut" if forme.startswith("`") else "fr"
        surplus = jetons(normaliser_nombres(glose, "en")) - jetons(normaliser_nombres(forme, langue))
        if surplus:
            problemes.append(gid + " : la glose ajoute des nombres " + str(_diff(surplus, collections.Counter())))
    sources = {s for _, _, s in citations_fr(source)}
    glosees, neutres, couverts = gardees(donnees)
    couvreur = {c: gid for c, gid, _ in donnees.COUVERTS}
    vues = set()
    for a, b, s in citations_fr(texte_corps):
        if s not in sources:
            problemes.append("citation française nouvelle ou modifiée (l." + str(texte_corps.count(NL, 0, a) + 1)
                             + ") : « " + s[:80] + " »")
            continue
        if s in vues:
            continue
        vues.add(s)
        if s in glosees or s in neutres:
            continue
        if s in couverts:
            span = premieres.get(couvreur[s])
            if span is None or not (span[0] <= a and b <= span[1]):
                problemes.append("citation couverte hors de la forme qui la couvre : « " + s[:80] + " »")
            continue
        problemes.append("citation gardée sans glose ni déclaration (l." + str(texte_corps.count(NL, 0, a) + 1)
                         + ") : « " + s[:80] + " »")
    return problemes


def controle_proteges(source, texte_corps, donnees):
    ws_s, ws_t = normaliser_espaces(source), normaliser_espaces(texte_corps)
    problemes = []
    for pid, fr, en in donnees.PROTEGES:
        ns, nt = ws_s.count(normaliser_espaces(fr)), ws_t.count(normaliser_espaces(en))
        if ns == 0 or ns != nt:
            problemes.append(pid + " : source " + str(ns) + ", traduction " + str(nt) + " — « " + en[:70] + " »")
    return problemes


def controle_libelles(source, texte_corps, donnees):
    problemes = []
    ws_s, ws_t = normaliser_espaces(source), normaliser_espaces(texte_corps)
    for nom, rx in donnees.LIBELLES_COMPTES.items():
        ns, nt = len(re.findall(rx, ws_s)), len(re.findall(rx, ws_t))
        if ns != nt:
            problemes.append("libellé " + nom + " : source " + str(ns) + ", traduction " + str(nt))
    return problemes


def controle_entete(entete, donnees):
    if len(entete) != 2:
        return ["en-tête : deux paragraphes attendus, " + str(len(entete)) + " trouvés"]
    problemes = []
    premier, second = entete[0].texte, entete[1].texte
    if not premier.startswith(donnees.ENTETE_BROUILLON):
        problemes.append("en-tête : mention « " + donnees.ENTETE_BROUILLON + " » absente en tête")
    for attendu in (donnees.ENTETE_PHRASE, donnees.ENTETE_MENTION):
        if attendu not in normaliser_espaces(premier):
            problemes.append("en-tête : phrase absente : « " + attendu[:70] + " »")
    if not second.startswith(donnees.ENTETE_CONVENTIONS):
        problemes.append("en-tête : conventions de traduction absentes")
    for u in entete:
        if RE_CHIFFRES.search(u.texte):
            problemes.append("en-tête ajouté : chiffre présent (l." + str(u.ligne) + ")")
    return problemes


def _lignes_de_donnees(unites_table):
    """Lignes de données d'une table (en-tête et ligne de séparation retirés)."""
    return [u.texte for u in unites_table[2:]]


def controle_glossaire_final(glossaire, donnees):
    problemes = []
    if not glossaire or glossaire[0].texte != donnees.GLOSSAIRE_TITRE:
        return ["glossaire final : titre absent"]
    attendus = [
        (donnees.GLOSSAIRE_A, ["| " + f + " | " + g + " |" for _, f, g, _ in donnees.GLOSES]),
        (donnees.GLOSSAIRE_B, ["| " + fr + " | " + en + " | " + note + " |" for fr, en, note in donnees.TERMES]),
    ]
    i = 1
    for titre, lignes in attendus:
        if i >= len(glossaire) or glossaire[i].texte != titre:
            problemes.append("glossaire final : sous-titre attendu « " + titre + " »")
            return problemes
        j = i + 1
        while j < len(glossaire) and glossaire[j].genre == "table":
            j += 1
        trouvees = _lignes_de_donnees(glossaire[i + 1:j])
        if trouvees != lignes:
            manquantes = [l for l in lignes if l not in trouvees]
            en_trop = [l for l in trouvees if l not in lignes]
            problemes.append("glossaire final, « " + titre + " » : " + str(len(manquantes)) + " ligne(s) manquante(s), "
                             + str(len(en_trop)) + " en trop" + (" ; première : " + (manquantes + en_trop)[0][:90]
                                                                 if manquantes or en_trop else " ; ordre différent"))
        i = j
    if i != len(glossaire):
        problemes.append("glossaire final : " + str(len(glossaire) - i) + " unité(s) en trop après les deux tables")
    return problemes


def cellules_anglaises_glossaire(glossaire, donnees):
    """Cellules anglaises des tables du glossaire final (pour le registre)."""
    textes, table = [], None
    for u in glossaire:
        if u.genre == "titre":
            table = u.texte
            continue
        if u.genre != "table" or u.texte.startswith("|---"):
            continue
        cellules = [c.strip() for c in masquer_code(u.texte)[0].strip().strip("|").split("|")]
        brutes = [c.strip() for c in u.texte.strip().strip("|").split(" | ")]
        if table == donnees.GLOSSAIRE_A and len(brutes) >= 2:
            textes.append(brutes[1])
        elif table == donnees.GLOSSAIRE_B and len(cellules) >= 3:
            textes.extend(brutes[1:3])
    return NL.join(textes)


# --- Données du glossaire ---------------------------------------------------------------------------------------------

def titres_de(texte):
    return [u.texte for u in unites(texte) if u.genre == "titre"]


def verifier_epingle(donnees, sha_source):
    """La source est-elle celle que décrit le glossaire ? Il épingle son sha256 (synchronisation fr → en,
    SHOGEN-PUBLIC-EN-SYNCHRO-1) : toute autre source arrête le contrôle (fatal), avant tout calcul."""
    attendu = getattr(donnees, "SOURCE_SHA256", None)
    if not attendu:
        raise ErreurFatale("glossaire sans empreinte de source (SOURCE_SHA256)")
    if sha_source != attendu:
        raise ErreurFatale("source non épinglée : sha256 " + sha_source + ", attendu " + attendu
                           + " (glossaire et traduction à revoir avant tout contrôle)")


def verifier_donnees(donnees, source):
    """Le glossaire fixé décrit-il bien la source ? Sinon : fatal (le contrôle ne conclut pas)."""
    if titres_de(source) != [fr for fr, _ in donnees.TITRES]:
        raise ErreurFatale("titres du glossaire différents des titres de la source")
    ws_source = normaliser_espaces(source)
    contenus_source = [s for _, _, s in citations_fr(source)]
    ids = {gid for gid, _, _, _ in donnees.GLOSES}
    for gid, forme, _, _ in donnees.GLOSES:
        if est_citation(forme):
            if contenu_citation(forme) not in contenus_source:
                raise ErreurFatale(gid + " : citation glosée absente de la source")
        elif forme.startswith("`"):
            if forme not in source:
                raise ErreurFatale(gid + " : code en ligne glosé absent de la source")
        elif normaliser_espaces(forme) not in ws_source:
            raise ErreurFatale(gid + " : forme glosée absente de la source")
    for gid in donnees.REGEX_LIBELLES:
        if gid not in ids:
            raise ErreurFatale("expression de libellé sans glose : " + gid)
    glosees, neutres, couverts = gardees(donnees)
    for c, gid, _ in donnees.COUVERTS:
        if gid not in ids:
            raise ErreurFatale("citation couverte par une glose inconnue : " + gid)
    traduites = {normaliser_espaces(fr) for _, fr, _, _ in donnees.CITATIONS_TRADUITES}
    ensembles = [glosees, neutres, couverts, traduites]
    for i, a in enumerate(ensembles):
        for b in ensembles[i + 1:]:
            if a & b:
                raise ErreurFatale("citation déclarée deux fois : « " + sorted(a & b)[0][:60] + " »")
    declarees = set().union(*ensembles)
    for s in declarees:
        if s not in contenus_source:
            raise ErreurFatale("citation déclarée absente de la source : « " + s[:60] + " »")
    for s in contenus_source:
        if s not in declarees:
            raise ErreurFatale("citation de la source non couverte par le glossaire : « " + s[:60] + " »")
    for pid, fr, _ in donnees.PROTEGES:
        if normaliser_espaces(fr) not in ws_source:
            raise ErreurFatale(pid + " : passage protégé absent de la source")


# --- Table de correspondance et rapport ------------------------------------------------------------------------------

def table_correspondance(paires, donnees, sha_source, sha_traduction):
    """Table section par section (fr → en), tirée de l'alignement des unités."""
    sections, courante = [], None
    for uf, ue in paires:
        if uf.genre == "titre":
            courante = {"fr": uf.texte, "en": ue.texte, "lf": uf.ligne, "le": ue.ligne,
                        "genres": collections.Counter(), "nf": 0, "ne": 0, "egal": True, "g": 0, "t": 0, "q": 0}
            sections.append(courante)
            continue
        if courante is None:
            continue
        courante["genres"][uf.genre] += 1
        jf, je = jetons_unite(uf, "fr"), jetons_unite(ue, "en")
        courante["nf"] += sum(v for k, v in jf.items() if k[0] == "c")
        courante["ne"] += sum(v for k, v in je.items() if k[0] == "c")
        courante["egal"] = courante["egal"] and jf == je and mots_unite(uf, "fr") == mots_unite(ue, "en")
        if uf.genre != "code":
            courante["q"] += len(citations_fr(ue.texte))
            courante["t"] += len(citations_en(ue.texte))
            courante["g"] += len(gloses(ue.texte))
    lignes = [
        "# Table de correspondance, section par section (fr → en) — lot DOCS11-EN",
        "",
        "Générée par `controle_en.py --table` depuis l'alignement des unités (une unité : titre, paragraphe, élément de "
        "liste, ligne de table, bloc de code ou paragraphe de citation). Source sha256 `" + sha_source + "` ; "
        "traduction sha256 `" + sha_traduction + "`. Les deux paragraphes d'en-tête ajoutés (brief, point 6) et le "
        "glossaire final ne figurent pas ici : ce sont des ajouts déclarés, contrôlés à part (contrôles 10 et 11).",
        "",
        "| # | titre français (l.) | titre anglais (l.) | unités : para / liste / table / code / bloc | nombres "
        "(composites) fr = en | nombres identiques par unité | citations gardées | citations traduites | gloses |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for k, s in enumerate(sections, 1):
        g = s["genres"]
        lignes.append("| " + str(k) + " | " + s["fr"].lstrip("#").strip() + " (l." + str(s["lf"]) + ") | "
                      + s["en"].lstrip("#").strip() + " (l." + str(s["le"]) + ") | "
                      + " / ".join(str(g[x]) for x in ("para", "liste", "table", "code", "bloc")) + " | "
                      + str(s["nf"]) + " = " + str(s["ne"]) + " | " + ("oui" if s["egal"] else "NON") + " | "
                      + str(s["q"]) + " | " + str(s["t"]) + " | " + str(s["g"]) + " |")
    return NL.join(lignes) + NL


def lire(chemin):
    with open(chemin, "rb") as f:
        octets = f.read()
    return octets.decode("utf-8"), hashlib.sha256(octets).hexdigest()


def _court(texte, n=110):
    texte = texte.replace(NL, " / ")
    return texte if len(texte) <= n else texte[:n] + "…"


def _section(titre, problemes, echecs, nom, details=()):
    print()
    print("--- " + titre + " ---")
    for d in details:
        print("  " + d)
    for p in problemes[:60]:
        print("  ÉCHEC " + _court(p, 160))
    if len(problemes) > 60:
        print("  … " + str(len(problemes) - 60) + " problème(s) de plus")
    if problemes:
        echecs.append(nom)
    print("  => " + ("ÉCHEC (" + str(len(problemes)) + ")" if problemes else "OK"))


def main(argv, donnees=None):
    table_sortie = None
    if len(argv) == 4 and argv[2] == "--table":
        table_sortie = argv[3]
        argv = argv[:2]
    if len(argv) != 2:
        print("usage : controle_en.py SOURCE TRADUCTION [--table SORTIE]")
        return 3
    try:
        (source, sha_s), (trad, sha_t) = [lire(c) for c in argv]
    except (OSError, UnicodeDecodeError) as erreur:
        print("FATAL : entrée illisible : " + str(erreur))
        return 3
    try:
        if donnees is None:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            donnees = importlib.import_module("glossaire_en")
        sha_g = ""
        if getattr(donnees, "__file__", None):
            sha_g = lire(donnees.__file__)[1]
        verifier_epingle(donnees, sha_s)
        verifier_donnees(donnees, source)
        uf = unites(source)
        corps_u, entete_u, glossaire_u, pb_sep = separer(unites(trad), donnees)
        paires, pb_al = aligner(uf, corps_u, donnees)
        texte_corps = corps(trad, donnees)
        p_structure = pb_sep + pb_al + controle_structure(paires, donnees)
        p_nombres = controle_nombres(paires)
        p_citations = controle_citations(paires, donnees)
        p_gloses = controle_gloses(texte_corps, source, donnees)
        p_proteges = controle_proteges(source, texte_corps, donnees) + controle_libelles(source, texte_corps, donnees)
        motifs = motifs_trouves(trad)
        hits = registre_en(zones_anglaises(texte_corps), donnees.EXCEPTIONS_REGISTRE)
        hits += registre_en(cellules_anglaises_glossaire(glossaire_u, donnees), donnees.EXCEPTIONS_REGISTRE)
        libelles = [f for _, f, _, _ in donnees.GLOSES if not f.startswith(OUV) and not f.startswith("`")]
        residus = residus_francais(texte_corps, libelles)
        convention = convention_en(texte_corps)
        p_entete = controle_entete(entete_u, donnees)
        p_glossaire = controle_glossaire_final(glossaire_u, donnees)
        total_fr, total_en = collections.Counter(), collections.Counter()
        mots_fr, mots_en = collections.Counter(), collections.Counter()
        for a, b in paires:
            total_fr.update(jetons_unite(a, "fr"))
            total_en.update(jetons_unite(b, "en"))
            mots_fr.update(mots_unite(a, "fr"))
            mots_en.update(mots_unite(b, "en"))
        cites_fr = citations_fr(source)
        cites_en_g = citations_fr(texte_corps)
        cites_en_t = citations_en(texte_corps)
        nb_gloses = len(gloses(texte_corps))
        table = table_correspondance(paires, donnees, sha_s, sha_t) if table_sortie else None
    except ErreurFatale as erreur:
        print("FATAL : " + str(erreur))
        return 3

    echecs = []
    print("=== Contrôle de la traduction anglaise (lot DOCS11-EN) ===")
    print("source     : " + argv[0])
    print("             sha256 " + sha_s)
    print("traduction : " + argv[1])
    print("             sha256 " + sha_t)
    if sha_g:
        print("glossaire  : sha256 " + sha_g)
    _section("1. Structure et alignement", p_structure, echecs, "1. structure et alignement", [
        "unités : source " + str(len(uf)) + " ; traduction : corps " + str(len(corps_u)) + ", en-tête ajouté "
        + str(len(entete_u)) + ", glossaire final " + str(len(glossaire_u)),
        "titres alignés : " + str(sum(1 for a, _ in paires if a.genre == "titre")) + " ; blocs de code : "
        + str(sum(1 for a, _ in paires if a.genre == "code")) + " ; lignes de table : "
        + str(sum(1 for a, _ in paires if a.genre == "table")),
    ])
    familles = []
    for fam, nom in (("c", "composites"), ("d", "suites de chiffres")):
        familles.append(nom + " : source " + str(sum(1 for k in total_fr if k[0] == fam)) + " distincts / "
                        + str(sum(v for k, v in total_fr.items() if k[0] == fam)) + " occurrences ; traduction "
                        + str(sum(1 for k in total_en if k[0] == fam)) + " distincts / "
                        + str(sum(v for k, v in total_en.items() if k[0] == fam)) + " occurrences")
    inventes, perdus = total_en - total_fr, total_fr - total_en
    familles.append("multiensemble global normalisé : inventés " + str(sum(inventes.values())) + ", perdus "
                    + str(sum(perdus.values())) + (" — identique" if not inventes and not perdus else " — DIFFÉRENT"))
    familles.append("nombres en lettres : source " + str(dict(sorted(mots_fr.items()))) + " ; traduction "
                    + str(dict(sorted(mots_en.items()))))
    if inventes or perdus:
        p_nombres = p_nombres + ["multiensemble global différent : inventés " + str(_diff(inventes, perdus))
                                 + " ; perdus " + str(_diff(perdus, inventes))]
    _section("2. Nombres (par unité, puis global)", p_nombres, echecs, "2. nombres", familles)
    _section("3. Citations", p_citations, echecs, "3. citations", [
        "source : " + str(len(cites_fr)) + " citations « … » de premier niveau, " + str(len({c[2] for c in cites_fr}))
        + " distinctes ; traduction (corps) : " + str(len(cites_en_g)) + " gardées « … », " + str(len(cites_en_t))
        + " traduites “ … ”",
    ])
    _section("4. Gloses (première occurrence)", p_gloses, echecs, "4. gloses", [
        "gloses déclarées " + str(len(donnees.GLOSES)) + " ; trouvées dans le corps " + str(nb_gloses),
    ])
    _section("5. Passages protégés et libellés de verdict", p_proteges, echecs, "5. passages protégés et libellés", [
        str(len(donnees.PROTEGES)) + " passages protégés ; " + str(len(donnees.LIBELLES_COMPTES)) + " libellés comptés",
    ])
    p_motifs = [m[0] + " / " + m[1] + " : " + str(m[2]) + " (l." + ",".join(str(x) for x in m[3]) + ")" for m in motifs]
    _section("6. Motifs interdits (0 exigé dans la traduction)", p_motifs, echecs, "6. motifs interdits", [
        str(len(MOTIFS)) + " motifs ; présents dans la source : " + str(len(motifs_trouves(source)))
        + " ; dans la traduction : " + str(len(motifs)),
    ])
    p_registre = [h[0] + " (l." + str(h[1]) + ") : " + h[2] for h in hits if not h[3]]
    admises = [h for h in hits if h[3]]
    _section("7. Registre du doc 09 en anglais (S-G4 comprise)", p_registre, echecs, "7. registre", [
        str(len(LOCUTIONS_SG4)) + " locutions S-G4 + " + str(len(LOCUTIONS_EN)) + " locutions anglaises + motif "
        "« k sources » ; occurrences admises : " + str(len(admises))] + [
        "admise : « " + h[0] + " » (l." + str(h[1]) + ") — " + _court(h[2], 80) for h in admises])
    _section("8. Résidus français en zone anglaise", [m + " (l." + str(n) + ")" for m, n in residus], echecs,
             "8. résidus français", [str(len(MOTS_OUTILS_FR)) + " mots-outils cherchés"])
    _section("9. Convention des nombres en zone anglaise", [f + " (l." + str(n) + ")" for f, n in convention], echecs,
             "9. convention des nombres")
    _section("10. En-tête anglais (brief, point 6)", p_entete, echecs, "10. en-tête")
    _section("11. Glossaire final", p_glossaire, echecs, "11. glossaire final", [
        str(len(donnees.GLOSES)) + " passages gardés ; " + str(len(donnees.TERMES)) + " lignes de termes"])

    print()
    print("--- Informatif : rapport de longueur anglais / français par unité (hors [0,6 ; 1,5]) ---")
    for a, b in paires:
        if a.genre in ("code", "titre", "table"):
            continue
        lf, le = len(a.texte), len(retirer_gloses(b.texte))
        if lf >= 80 and not 0.6 <= le / lf <= 1.5:
            print("  l." + str(a.ligne) + " / l." + str(b.ligne) + " : " + str(round(le / lf, 2)))
    if table is not None:
        with open(table_sortie, "w", encoding="utf-8") as f:
            f.write(table)
        print()
        print("table de correspondance écrite : " + table_sortie)
    print()
    if echecs:
        print("VERDICT : NON CONFORME — " + " ; ".join(echecs) + " (sortie 1)")
        return 1
    print("VERDICT : CONFORME — onze contrôles sur onze (sortie 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
