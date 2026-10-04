# -*- coding: utf-8 -*-
"""Campagne de mutants du lot DOCS11-EN.

Deux familles (registres du doc 09, ADR-0011 pt 4) :
  - mutants de programme (MC) : copie du dossier outils/, une seule retouche de controle_en.py, lancement de
    tests/lancer_tests.py sur la copie ;
  - octets mutés du lot (MT) : une seule retouche de la traduction, lancement du contrôle réel sur la copie mutée
    (MT-30 : témoin négatif, la source passée comme traduction).
Classement par la sortie (SHOGEN-MUT-FATAL-1) : 1 tué ; 0 vivant ; 3 ou toute autre sortie FATAL (run invalide,
jamais compté tué). Une retouche qui ne s'applique pas exactement une fois rend le mutant FATAL.
Deux témoins sans mutation (T-0a code, T-0b texte) doivent sortir 0. Un troisième (T-0c, ajouté avec la retouche
E-19) lance le contrôle réel sur la source française précédente (4de98654…) : l'épingle doit le refuser (sortie 3).
Enfin : chaque nom de test doit avoir échoué au moins une fois (étapes rouges ou mutants).
Aucune barre oblique inverse n'est écrite dans ce fichier.

Usage : python3 -B campagne_mutants.py
"""
import os
import re
import shutil
import subprocess
import sys

NL = chr(10)
DQ = chr(34)
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
OUTILS = os.path.join(RACINE, "outils")
TESTS = os.path.join(RACINE, "tests")
TMP = os.path.join(ICI, "tmp")
SOURCE = "/home/user/shogen/docs/publication/11-mesures-pilotes-public.md"
TRADUCTION = os.path.join(RACINE, "11-pilot-measurements-public-en.md")
CE = "controle_en.py"
SOURCE_PRECEDENTE = os.path.join(RACINE, "explo", "source-4de98654.md")

CODE = [
    ("MC-01", '        t = RE_FR_DECIMALE.sub(lambda m: m.group(1) + "." + m.group(2), t)', "        t = t",
     "virgule décimale française non convertie"),
    ("MC-02", '        t = RE_FR_GROUPE.sub(lambda m: m.group(0).replace(" ", ""), t)', "        t = t",
     "espace de milliers français non retirée"),
    ("MC-03", '        return RE_EN_GROUPE.sub(lambda m: m.group(0).replace(",", ""), texte)', "        return texte",
     "virgule de milliers anglaise non retirée"),
    ("MC-04", '        t = RE_FR_VECTEUR.sub(lambda m: m.group(0).replace(" ", SEP_VECTEUR), texte)', "        t = texte",
     "vecteurs entre crochets non protégés"),
    ("MC-05", '            compte[("c", m.group(0))] += 1', "            pass", "famille composite débranchée"),
    ("MC-06", '        if lab != "x":' + NL + "            total.update(jetons(normaliser_nombres(seg, LANGUE[lab])))",
     "        if True:" + NL + '            total.update(jetons(normaliser_nombres(seg, LANGUE.get(lab, "en"))))',
     "gloses comptées dans les nombres"),
    ("MC-07", '                if lab[k] == "e":' + NL + '                    lab[k] = "f"',
     "                if False:" + NL + '                    lab[k] = "f"', "citations gardées lues à l'anglaise"),
    ("MC-08", '        if avant == "-" or apres == "-":' + NL + "            continue",
     "        if False:" + NL + "            continue", "mots composés à trait d'union comptés"),
    ("MC-09", '        if langue == "en" and m.group(0).lower() == "third" and texte[m.end():m.end() + 6].lower() == " party":'
     + NL + "            continue" + NL, "", "« third party » compté comme ordinal"),
    ("MC-10", '        if lab in ("f", "e"):' + NL + "            total.update(mots_nombres(seg, LANGUE[lab]))",
     "        if False:" + NL + "            total.update(mots_nombres(seg, LANGUE[lab]))",
     "nombres en lettres jamais comptés par unité"),
    ("MC-11", '        elif ligne.startswith("|") and (dans_table or (i + 1 < len(lignes) and est_delimiteur(lignes[i + 1]))):',
     '        elif ligne.startswith("|"):', "toute ligne « | » prise pour une ligne de table"),
    ("MC-12", "                if contenu.strip():" + NL + "                    courant[0][1].append(contenu)" + NL
     + "                else:" + NL + "                    fermer()",
     "                courant[0][1].append(contenu)", "paragraphes de citation non séparés"),
    ("MC-13", '    if "`" in masque:', "    if False:", "accent grave impair non fatal"),
    ("MC-14", "            debut = pile.pop()" + NL + "            if not pile:" + NL
     + "                spans.append((debut, i + 1))",
     "            debut = pile.pop()" + NL + "            spans.append((debut, i + 1))", "imbrication des guillemets ignorée"),
    ("MC-15", "        if contenu:" + NL + "            res.append((a, b, contenu))", "        res.append((a, b, contenu))",
     "paire vide “ ” prise pour une citation"),
    ("MC-16", '        elif uf.genre == "code":' + NL + "            if uf.texte != ue.texte:",
     '        elif uf.genre == "code":' + NL + "            if False:", "blocs de code non comparés"),
    ("MC-17", "        if collections.Counter(masquer_code(uf.texte)[1]) != collections.Counter(masquer_code(ue.texte)[1]):",
     "        if False:", "codes en ligne non comparés"),
    ("MC-18", "            if titres.get(uf.texte) != ue.texte:", "            if False:", "titres non contrôlés"),
    ("MC-19", '        elif sequence_unite(uf, "fr") != sequence_unite(ue, "en"):', "        elif False:",
     "ordre des nombres par unité non contrôlé"),
    ("MC-20", "        if jf != je:" + NL + '            problemes.append(lieu + " : nombres inventés "',
     "        if False:" + NL + '            problemes.append(lieu + " : nombres inventés "',
     "multiensemble par unité non contrôlé"),
    ("MC-21", "        if trouvees_t != attendues_t:", "        if False:", "citations traduites non contrôlées"),
    ("MC-22", '        if not suite.startswith(" " + marque):', "        if False:", "glose à la première occurrence non exigée"),
    ("MC-23", "        if n != 1:", "        if False:", "nombre de gloses non contrôlé"),
    ("MC-24", "        if surplus:", "        if False:", "nombres ajoutés par une glose non contrôlés"),
    ("MC-25", "        if s not in sources:" + NL + '            problemes.append("citation française nouvelle ou modifiée',
     "        if False:" + NL + '            problemes.append("citation française nouvelle ou modifiée',
     "citation française nouvelle non signalée"),
    ("MC-26", "        if ns == 0 or ns != nt:", "        if False:", "passages protégés jamais en écart"),
    ("MC-27", "    ws_s, ws_t = normaliser_espaces(source), normaliser_espaces(texte_corps)" + NL
     + "    for nom, rx in donnees.LIBELLES_COMPTES.items():",
     "    ws_s, ws_t = source, texte_corps" + NL + "    for nom, rx in donnees.LIBELLES_COMPTES.items():",
     "libellés comptés sans normaliser les espaces"),
    ("MC-28", "    (" + DQ + "décision de l'investisseur (anglais)" + DQ + ", " + DQ + "« Pyth est mort »" + DQ + ", " + DQ + "pyth (?:is|was) dead|pyth died|dead pyth" + DQ + ", True),"
     + NL, "", "motif anglais « Pyth est mort » retiré"),
    ("MC-29", '    return not (avant.isalnum() or avant == "_") and not (apres.isalnum() or apres == "_")', "    return True",
     "registre : bornes de mot ignorées"),
    ("MC-30", "            if i <= debut and fin <= i + len(contexte):" + NL + "                return True",
     "            if False:" + NL + "                return True", "registre : exceptions ignorées"),
    ("MC-31", "        if m.group(0).lower() in MOTS_OUTILS_FR:", "        if False:", "résidus français jamais signalés"),
    ("MC-32", "        if len(m.group(0)) > 1 and m.group(0).isupper():" + NL + "            continue" + NL, "",
     "mots en capitales pris pour des mots-outils"),
    ("MC-33", "    trouves = [(m.start(), m.group(0)) for m in RE_CONV_DECIMALE.finditer(zones)]", "    trouves = []",
     "virgule décimale française en zone anglaise non signalée"),
    ("MC-34", "        if RE_CHIFFRES.search(u.texte):", "        if False:", "chiffre dans l'en-tête ajouté non signalé"),
    ("MC-35", "        if trouvees != lignes:", "        if False:", "glossaire final jamais en écart"),
    ("MC-36", "    for s in contenus_source:" + NL + "        if s not in declarees:",
     "    for s in contenus_source:" + NL + "        if False:", "citation de la source non couverte acceptée"),
    ("MC-37", '        print("VERDICT : NON CONFORME — " + " ; ".join(echecs) + " (sortie 1)")' + NL + "        return 1",
     '        print("VERDICT : NON CONFORME — " + " ; ".join(echecs) + " (sortie 1)")' + NL + "        return 0",
     "main rend 0 sur échec"),
    ("MC-38", "    if len(entete) != 2:" + NL + '        problemes.append("en-tête anglais absent ou mal placé',
     "    if False:" + NL + '        problemes.append("en-tête anglais absent ou mal placé', "en-tête absent non signalé par separer"),
    ("MC-39", "    if len(unites_fr) != len(unites_en):", "    if False:", "nombre d'unités non comparé"),
    ("MC-40", '    return ligne.startswith("|") and "-" in ligne and set(ligne.strip()) <= set("|-: ")', "    return False",
     "ligne de délimitation jamais reconnue"),
    ("MC-41", 'RE_GLOSE = re.compile(CROCHET_O + ETOILE + "(.*?)" + ETOILE + CROCHET_F)', 'RE_GLOSE = re.compile("(?!x)x")',
     "gloses jamais reconnues"),
    ("MC-42", "            if sortie[k] != NL:" + NL + '                sortie[k] = " "',
     "            if False:" + NL + '                sortie[k] = " "', "citations « … » laissées dans les zones anglaises"),
    ("MC-43", '                problemes.append(lieu + " : citation de la source non déclarée : « " + s[:80] + " »")',
     "                pass", "citation de la source non déclarée non signalée"),
    ("MC-44", '    p_motifs = [m[0] + " / " + m[1] + " : " + str(m[2]) + " (l." + ",".join(str(x) for x in m[3]) + ")" for m in motifs]',
     "    p_motifs = []", "motifs jamais en échec dans main"),
    ("MC-45", '    p_registre = [h[0] + " (l." + str(h[1]) + ") : " + h[2] for h in hits if not h[3]]', "    p_registre = []",
     "registre jamais en échec dans main"),
    ("MC-46", '[f + " (l." + str(n) + ")" for f, n in convention]', "[]", "convention jamais en échec dans main"),
    ("MC-47", '[m + " (l." + str(n) + ")" for m, n in residus]', "[]", "résidus jamais en échec dans main"),
    ("MC-48", "        p_glossaire = controle_glossaire_final(glossaire_u, donnees)", "        p_glossaire = []",
     "glossaire final jamais en échec dans main"),
    ("MC-49", "        p_entete = controle_entete(entete_u, donnees)", "        p_entete = []", "en-tête jamais en échec dans main"),
    ("MC-50", "        p_citations = controle_citations(paires, donnees)", "        p_citations = []",
     "citations jamais en échec dans main"),
    ("MC-51", "        p_gloses = controle_gloses(texte_corps, source, donnees)", "        p_gloses = []",
     "gloses jamais en échec dans main"),
    ("MC-52", "        p_proteges = controle_proteges(source, texte_corps, donnees) + controle_libelles(source, texte_corps, donnees)",
     "        p_proteges = []", "passages protégés jamais en échec dans main"),
    ("MC-53", "        p_structure = pb_sep + pb_al + controle_structure(paires, donnees)", "        p_structure = []",
     "structure jamais en échec dans main"),
    ("MC-54", "        p_nombres = controle_nombres(paires)", "        p_nombres = []",
     "nombres par unité jamais en échec dans main"),
    ("MC-55", "    if titres_de(source) != [fr for fr, _ in donnees.TITRES]:", "    if False:",
     "titres du glossaire non confrontés à la source"),
    ("MC-56", "    return [(m.start(), m.end(), m.group(1)) for m in RE_GLOSE.finditer(texte)]", "    return []",
     "fonction gloses rend toujours vide"),
    ("MC-57", '    if langue == "brut":' + NL + "        return texte", '    if langue == "brut":' + NL + '        langue = "fr"',
     "zone brute normalisée à la française"),
    ("MC-58", '        return RE_EN_GROUPE.sub(lambda m: m.group(0).replace(",", ""), texte)', '        return re.sub("[.,]", "", texte)',
     "normalisation anglaise qui efface aussi le point décimal"),
    ("MC-59", '        t = RE_FR_DECIMALE.sub(lambda m: m.group(1) + "." + m.group(2), t)', '        t = t.replace(",", ".")',
     "toute virgule française convertie en point"),
    ("MC-60", '        suite = texte_corps[m.end():].lstrip("*")', "        suite = texte_corps[m.end():]",
     "glose après un gras non reconnue (faux positif)"),
    ("MC-61", "        if positions:" + NL + "            lignes = sorted(", "        if True:" + NL + "            lignes = sorted(",
     "motifs à zéro occurrence rapportés (faux positif)"),
    ("MC-62", "        if ns == 0 or ns != nt:", "        if ns == 0 or ns == nt:", "passages protégés égaux signalés (comparaison inversée)"),
    ("MC-63", '        if avant in "-_/." or apres in "-_/":' + NL + "            continue", "        if False:" + NL + "            continue",
     "mots des identifiants pris pour des résidus français"),
    ("MC-64", "            if titres.get(uf.texte) != ue.texte:", "            if uf.texte != ue.texte:",
     "titres comparés sans la table de traduction"),
    ("MC-65", "        if normaliser_espaces(fr) not in ws_source:", "        if normaliser_espaces(fr) in ws_source:",
     "passage protégé présent jugé absent (faux fatal)"),
    ("MC-66", "    if sha_source != attendu:", "    if False:", "source non épinglée acceptée"),
    ("MC-67", '    attendu = getattr(donnees, "SOURCE_SHA256", None)',
     '    attendu = getattr(donnees, "SOURCE_SHA256", None) or sha_source',
     "empreinte de source absente remplacée par celle de la source"),
    ("MC-68", "        verifier_epingle(donnees, sha_s)", "        pass", "épingle non appelée par main"),
    ("MC-69", "    if sha_source != attendu:", "    if sha_source == attendu:", "épingle inversée (source attendue refusée)"),
]

TEXTE = [    ("MT-01", "On J28 (35,982 one-minute windows", "On J28 (35,983 one-minute windows", "nombre changé"),
    ("MT-02", "EMD_s ≈ 196 windows in calm and ≈ 211 in stress", "EMD_s ≈ 211 windows in calm and ≈ 196 in stress",
     "deux nombres échangés dans une unité"),
    ("MT-03", "The two skipped tests are the count tests", "The three skipped tests are the count tests",
     "nombre écrit en lettres changé"),
    ("MT-04", "  famille de Bonferroni pré-enregistrée (ADR-0028 D2 pt 4)",
     "  famille de Bonferroni pre-enregistree (ADR-0028 D2 pt 4)", "bloc de code retouché"),
    ("MT-05", "« causalité non établie » [*causality not established*]",
     "« causalité non établie. » [*causality not established*]", "citation gardée modifiée"),
    ("MT-06", "returns NE REJETTE PAS in both strata", "returns DOES NOT REJECT in both strata",
     "libellé de verdict traduit"),
    ("MT-07", "**« R1 discrimine » = FAUX** [*", "**« R1 discrimine » = VRAI** [*", "verdict inversé"),
    ("MT-08", "**ÉTEINT** [*off*]", "**ÉTEINT**", "glose retirée"),
    ("MT-09", "It establishes no pair dependence", "It establishes independent sources and no pair dependence",
     "formule interdite du registre"),
    ("MT-10", "the sealed text is authoritative", "the sealed text is verified", "locution S-G4"),
    ("MT-11", "All are in `docs/adr-0028/execution/rendu-2026-10-04/`", "All are in /home/user/shogen and "
     "`docs/adr-0028/execution/rendu-2026-10-04/`", "chemin d'hôte"),
    ("MT-12", "The publication covers this report only", "The publication covers this report only (Pocket excluded)",
     "Pocket"),
    ("MT-13", "the session or agent identifiers", "the session_ or agent identifiers", "identifiant de session"),
    ("MT-14", "and nothing shows an outage of Pyth", "and Pyth was dead", "formule écartée par l'investisseur"),
    ("MT-15", "documents provided on request, under agreement. Checking the seal",
     "documents provided with this report, under agreement. Checking the seal", "pièces présentées comme remises"),
    ("MT-16", "The renderings are cited by abbreviation", "Les rendus sont cités par abréviation",
     "phrase laissée en français"),
    ("MT-17", "(≈ 20.8 in calm, ≈ 28.5 in stress)", "(≈ 20,8 in calm, ≈ 28.5 in stress)", "virgule décimale française"),
    ("MT-18", "> **Draft — not published.** English", "> **Draft.** English", "mention « Draft — not published » retirée"),
    ("MT-19", "| flux | feed |", "| flux | stream |", "glossaire final modifié"),
    ("MT-20", "Reading conventions and lexicon: next section." + NL + NL, "", "paragraphe supprimé"),
    ("MT-21", "### 8.8 Duration", "### 8.8 Time", "titre non conforme"),
    ("MT-22", "| `oracle_pyth` | pyth | `33.0` | `0.0015` |", "| `oracle_pyth` | pyth | `33.0` | `0.0015` | x |",
     "cellule ajoutée"),
    ("MT-23", "« gardes levées » [*guards cleared*]", "“guards cleared”", "sortie imprimée traduite au lieu d'être gardée"),
    ("MT-24", "`4f223a22950778c799b39b1856a400c965ac18b4b57625bfef3136c04daaeb3a`",
     "`4f223a22950778c799b39b1856a400c965ac18b4b57625bfef3136c04daaeb3b`", "empreinte modifiée"),
    ("MT-25", "P̂_more ≈ 0.00136, guard ≈ 33.5", "P̂_more ≈ 0.00163, guard ≈ 33.5", "chiffres transposés"),
    ("MT-26", "fixed n = 38,600 (J28 l.31)", "fixed n = 386,00 (J28 l.31)", "séparateur de milliers déplacé"),
    ("MT-27", "are hors décision [*outside the decision*] and identify no cause",
     "are outside the decision [*outside the decision*] and identify no cause", "libellé « hors décision » traduit"),
    ("MT-28", "the sealed package and the original outputs prevail in case of discrepancy",
     "the original outputs prevail in case of discrepancy", "phrase d'en-tête du brief altérée"),
    ("MT-29", "“Stop it (Recommended)”", "“Stop (Recommended)”", "citation traduite altérée"),
    ("MT-31", "[*configured pool = 12 feeds*]", "[*configured pool = 13 feeds*]", "nombre ajouté par une glose"),
    ("MT-32", "are hors décision [*outside the decision*] and identify no cause. The hors décision outputs",
     "are hors décision and identify no cause. The hors décision [*outside the decision*] outputs",
     "glose déplacée après la première occurrence"),
    ("MT-33", "the sealed package, the seal, the renderings, the records and the scripts are provided on request",
     "the seal, the renderings and the records are provided on request", "liste E-19 de l'en-tête ramenée à l'ancienne"),
    ("MT-34", "Checking the seal requires the sealed package, which is provided together with the seal on request: ",
     "", "phrase E-19 du contrôle du sceau retirée"),
    ("MT-35", "The sealed package, the seal, the renderings, the records and the scripts are in the same private",
     "The renderings, the seal and the records are in the same private", "liste E-19 du §12 ramenée à l'ancienne"),
]


def lancer(argv):
    r = subprocess.run([sys.executable, "-B"] + argv, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def classe(code):
    return {0: "vivant", 1: "tué"}.get(code, "FATAL")


def echecs_de(sortie):
    for ligne in sortie.split(NL):
        if ligne.startswith("tests en échec : "):
            return [n.strip() for n in ligne[len("tests en échec : "):].split(",")]
    return []


def main():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    with open(os.path.join(OUTILS, CE), encoding="utf-8") as f:
        code_reel = f.read()
    with open(TRADUCTION, encoding="utf-8") as f:
        texte_reel = f.read()
    with open(SOURCE, encoding="utf-8") as f:
        source = f.read()
    bilan = {"tué": 0, "vivant": 0, "FATAL": 0}
    vus_en_echec = set()

    print("=== Campagne de mutants du lot DOCS11-EN ===")
    code, sortie = lancer([os.path.join(TESTS, "lancer_tests.py"), OUTILS])
    print("T-0a témoin code (tests sur le module réel) : sortie " + str(code) + (" — OK" if code == 0 else " — ÉCHEC"))
    code_t, sortie_t = lancer([os.path.join(OUTILS, CE), SOURCE, TRADUCTION])
    print("T-0b témoin texte (contrôle réel sur la traduction) : sortie " + str(code_t)
          + (" — OK" if code_t == 0 else " — ÉCHEC"))
    code_c, sortie_c = lancer([os.path.join(OUTILS, CE), SOURCE_PRECEDENTE, TRADUCTION])
    print("T-0c témoin d'épingle (contrôle réel sur la source précédente) : sortie " + str(code_c)
          + (" — OK (refus attendu)" if code_c == 3 else " — ÉCHEC"))
    temoins_ok = code == 0 and code_t == 0 and code_c == 3
    print()

    for ident, avant, apres, libelle in CODE:
        dossier = os.path.join(TMP, "outils-" + ident)
        shutil.copytree(OUTILS, dossier, ignore=shutil.ignore_patterns("__pycache__"))
        n = code_reel.count(avant)
        if n != 1:
            print(ident + " FATAL — retouche trouvée " + str(n) + " fois — " + libelle)
            bilan["FATAL"] += 1
            continue
        with open(os.path.join(dossier, CE), "w", encoding="utf-8") as f:
            f.write(code_reel.replace(avant, apres))
        code, sortie = lancer([os.path.join(TESTS, "lancer_tests.py"), dossier])
        c = classe(code)
        bilan[c] += 1
        noms = echecs_de(sortie)
        vus_en_echec.update(noms)
        print(ident + " " + c + " (sortie " + str(code) + ") — " + libelle + (" — tests en échec : " + ", ".join(noms)
                                                                            if noms else ""))
        shutil.rmtree(dossier)
    print()

    mutes = [(i, a, b, l) for i, a, b, l in TEXTE]
    for ident, avant, apres, libelle in mutes:
        n = texte_reel.count(avant)
        if n != 1:
            print(ident + " FATAL — retouche trouvée " + str(n) + " fois — " + libelle)
            bilan["FATAL"] += 1
            continue
        chemin = os.path.join(TMP, ident + ".md")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte_reel.replace(avant, apres))
        code, sortie = lancer([os.path.join(OUTILS, CE), SOURCE, chemin])
        c = classe(code)
        bilan[c] += 1
        verdict = next((l for l in sortie.split(NL) if l.startswith("VERDICT") or l.startswith("FATAL")), "?")
        print(ident + " " + c + " (sortie " + str(code) + ") — " + libelle + " — " + verdict)
        os.remove(chemin)
    chemin = os.path.join(TMP, "MT-30.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(source)
    code, sortie = lancer([os.path.join(OUTILS, CE), SOURCE, chemin])
    c = classe(code)
    bilan[c] += 1
    verdict = next((l for l in sortie.split(NL) if l.startswith("VERDICT") or l.startswith("FATAL")), "?")
    print("MT-30 " + c + " (sortie " + str(code) + ") — témoin négatif : la source passée comme traduction — " + verdict)
    os.remove(chemin)

    print()
    rouges = []
    for nom in sorted(os.listdir(TESTS)):
        if nom.startswith("etape-rouge") and nom.endswith(".sortie.txt"):
            with open(os.path.join(TESTS, nom), encoding="utf-8") as f:
                noms = echecs_de(f.read())
            rouges.append((nom, len(noms)))
            vus_en_echec.update(noms)
    with open(os.path.join(TESTS, "test_controle_en.py"), encoding="utf-8") as f:
        tous = sorted(set(re.findall("def (test_[a-z0-9_]+)", f.read())))
    jamais = [t for t in tous if t not in vus_en_echec]
    print("étapes rouges lues : " + ", ".join(n + " (" + str(k) + ")" for n, k in rouges))
    print("tests : " + str(len(tous)) + " ; vus en échec au moins une fois (étapes rouges ou mutants) : "
          + str(len(tous) - len(jamais)))
    for t in jamais:
        print("  JAMAIS EN ÉCHEC : " + t)
    total = sum(bilan.values())
    print()
    print("BILAN : " + str(total) + " mutants ; tués " + str(bilan["tué"]) + " ; vivants " + str(bilan["vivant"])
          + " ; FATAL " + str(bilan["FATAL"]) + " ; témoins " + ("OK" if temoins_ok else "EN ÉCHEC"))
    shutil.rmtree(TMP)
    return 0 if (temoins_ok and bilan["vivant"] == 0 and bilan["FATAL"] == 0 and not jamais) else 1


if __name__ == "__main__":
    sys.exit(main())
