"""Shōgen, lot DETTES-T3, DT3-B (SHOGEN-R1-FORME-RESOLUE-1 ; docs/adr-0028/G0-lot-D8a.md l.424 et CH-4 ; ADR-0028
annexe B, B.87 ; adjudication Q-B1 du 2026-10-09) : ligne « Modèle » des journaux G1/G2. Tout journal docs/G1-*.md ou
docs/G2-*.md hors d'EXEMPTES porte exactement une ligne qui commence par TETE, de la forme « - **Modèle** : `<id>` »,
fin de ligne ou espace ensuite, où <id> est un identifiant de la liste blanche du lint R-1 ou cet identifiant suivi de
[1m], par égalité exacte (`auteur_admis` de s2-harness/tools/oracle_record.py, jamais un test de préfixe). EXEMPTES :
les 52 journaux versés à 0cfbe3e, nom et sha256 ; un journal exempté puis modifié ne l'est plus : le commit qui le
modifie lui ajoute la ligne s'il n'en porte aucune (ajout daté, identifiant de son auteur ; 16 la portent déjà
dans la forme : une seconde les ferait refuser) ; G1-lot-DETTES-B2.md et G2-lot-DETTES-B2.md, qui portent une ligne de
cette tête hors forme, ne se modifient qu'avec leur sha256 changé ici, par un lot (texte de DT3-F).
Bibliothèque standard seule. Usage : python3 -B journaux-modele.py <racine> ; sortie 0 conforme, 1 refus (motifs sur
stderr), 3 erreur, toute exception comprise (DT3-F : une erreur n'est jamais un refus)."""
import glob
import hashlib
import importlib.util
import os
import sys

OUTIL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "s2-harness", "tools",
                     "oracle_record.py")      # auteur_admis : ligne ALLOWED= du lint, jamais recopiée
TETE = "- **Modèle** :"
EXEMPTES = dict([
    ("G1-lot-B-DEP-1-blocs.md", "0e001065dac7ce250c2709e49a2bdf0a5921027270811854ef3fc2ada593cbed"),
    ("G1-lot-B-DEP-2-bloc3.md", "f0cdefc385246edc5f0225fb41349e1d8e2e2a2614d550b3891d972fb1a75db4"),
    ("G1-lot-B-SEG-1-segment.md", "49ccdc79e1710d4d596761fa2464e1cdb9e994b9283ec89b9a619c7b3d641efe"),
    ("G1-lot-B-SEG-2-bloc1.md", "f2890d0d4ed6333aac5317345a84191c791c6c6d94d999159d19e78349fb8b07"),
    ("G1-lot-B-sensibilite.md", "8762dff16ba477fcae26ef4e855a8ea8bbd569d68007bab5616e4fb0b1ab1164"),
    ("G1-lot-B0-pool-analyse.md", "5303944c80e3689331526ed18e247e3edc08afa575bc53201a0d6dbee10c1372"),
    ("G1-lot-CORR.md", "1849053ce5f63336ab175237268289ede1c1f9f2e7c0cd152928c7367c53ac56"),
    ("G1-lot-CRITERE-regle.md", "ac77ef5ded62bea4b5c1ab0bb61e6c78cee9a1956f3c15c8e0d6f755dc7ad648"),
    ("G1-lot-D5-AMEND-descriptifs.md", "6fb26854a0b73ee526f62743da95535437ed00e1d8328de8ddc3ddd5d26f78dc"),
    ("G1-lot-D8a.md", "d466a140485ef743d4d1229cf8e24ef6a3ef26420536fbccf4d9b27d0865383a"),
    ("G1-lot-D8b.md", "76d3e018728e401f7c1fe189b0fa83117eb46a58a92ecbfc18aa0accac2e11ab"),
    ("G1-lot-D8c.md", "0db37099d9ea13e5bca84fd4d25601989403c1e99d703f912b118659079289ec"),
    ("G1-lot-DETTES-B1.md", "61c9b86d1d3f2b9b815c3188fe48de9d0a812c77c6f9b120f5f3e4176cac89ef"),
    ("G1-lot-DETTES-B2-corrections.md", "791729fe44e74ff0f1df3b124b1a7de96e50115bc9a7c8ff8fc97f850d94117f"),
    ("G1-lot-DETTES-B2.md", "0c62263c1a7515d749a02ca6ef8a1ca4907e77f34b726b5b14a44bfb0f82faa6"),
    ("G1-lot-DETTES-SIM-corrections.md", "35d67359f90efb386c85394e023ef449b74cc3d58147d3e8b5f1f53ab59ed0ac"),
    ("G1-lot-DETTES-SIM.md", "94a0b02f54f39e6df6ef3dbb8d953648dd6662215125e14841b48d1eac580f62"),
    ("G1-lot-DOCS-S2.md", "f3fe1351d9065ac81ea3c23033e90f1b5c09ed7723c9366d089104bde8af4e63"),
    ("G1-lot-DOCS11-EN.md", "f1b0faa984918683c3d98a4500e7bcd0440f6d031f2efef4b309f062acd8e0dc"),
    ("G1-lot-DOCS11-PUBLIC.md", "b847247173f708819f60c5e47b6f394520d4077571e8f7cb019f617ddc1b66d1"),
    ("G1-lot-E1-modele-de-menace.md", "88c6a7016ce157b0eea0bf541b23ee979173bfe1a6dd4da9fa53bdbddcb9fe9d"),
    ("G1-lot-POOLEE-strate-poolee.md", "07eb03e4a7b6c5a864b93135dd9e967d08f4a5388ac66d45876db3ec153239d9"),
    ("G1-lot-POST-PREREG.md", "0b84a1c378790e4f6c89d73db22dd4a636f2b37d72112bb6f5d204b8660bcf3a"),
    ("G1-lot-SG5-INTERDITS.md", "26b2f25f996d18bbff347b869de760e2de417970293b2996534424eb0843637c"),
    ("G1-lot-SIM-NIVEAU.md", "f78073986497208ec2799889ed7a5da7f3eee7f0c2c446b36f42f5da38e9f049"),
    ("G1-lot-adr0025-filtre.md", "5644582632554f332343cc62d9a33f023a14f91801020399ca97344dd0883e52"),
    ("G1-partie-2-P0.md", "b2a0be0446fd8772e58254f2ad0b72e58fb042e195e3c1095dae7e7adada8bfb"),
    ("G1-partie-2-corrections-G2.md", "736516587f3968849649d345d52f44b9e6a4a4de15a101d519707522381d26e0"),
    ("G1-partie-2-etape-A.md", "1e62ec9edac6a3b99b9a6138520945418658ba65446c665ceffbbe2812294ca5"),
    ("G1-partie-2-etape-B-1.md", "903a94d28709eeb8ee69107d30e84fcaacc389186ff3799eb88185eb40051e10"),
    ("G1-partie-2-etape-B-2.md", "60754608ee5d98e2783926fb6b6017137202de2d4581b4bf9c8402b20fb6a7ad"),
    ("G1-partie-2-etape-B-3.md", "a9a5b02e2a48a82ca08ecfcd1aaa3392ea35c00f1726eef13935964789d5ff71"),
    ("G1-partie-2-etape-C-1.md", "cc4f63cdb875c0c122a2a01ee1391cf6287cc0f84c9d3784b856444b7e9fb2d6"),
    ("G1-partie-2-etape-C-2.md", "8f6503fdd16e39e0a2728bab6b046dcf8a04021751601488d15b8246b8c0c071"),
    ("G1-partie-2-etape-C-3.md", "812806e1b72d6ed24b07e6b57d4b0b83ccdc4892c017c00ee627ba8ff57e0b1b"),
    ("G1-partie-3-P3.md", "b4b12680a2cad5d7e8f663a8340e9d483c7d045a1aa31057be16d7cca465565e"),
    ("G1-partie-3-P3g.md", "1028c80dbd121fcc9c2686d3dd17612f0e0c9df86457bb0ee8e5cadcba549cea"),
    ("G1-partie-3-R.md", "f11d6ccb88085e141fa6c430711aa8a01ca07d8f4512fc7ebd50d7d241a27a19"),
    ("G1-partie-3-S.md", "eb58e4732be812ba4e07007db524e6824e0962cd8e377d614e61ea67130c83b7"),
    ("G1-rapport-docs11.md", "61a492b7a36e1120a7a944b3176ecb06e145371a095b42119f8e10f80a32992f"),
    ("G2-lot-CORR.md", "96210705fe764df9345ff3e8459f3cd031bafa1049580428d65d1a1053ff680c"),
    ("G2-lot-DETTES-A.md", "4e2082f924791236852ae5f1fa25484d46875ddc4719a8c2662fc641bbde664c"),
    ("G2-lot-DETTES-B1.md", "0e0acfe1a02984aa4d37e72c6a14b13d95ed95c622ae832f80ac6fa8cc473f5c"),
    ("G2-lot-DETTES-B2.md", "e0612252db5963e48f001cbc602074f66a7f6f8f9e9306ebcd7f394026a386a7"),
    ("G2-lot-DETTES-SIM.md", "93b5881f4362b6a96a60559699044cb396c3794b74f4acfda17bcad594417c2b"),
    ("G2-lot-DOCS11-EN.md", "14e1d7183d82f9221d7a575f881f5dc74534447ebc276d2edf5d6bc3610fe6cf"),
    ("G2-lot-DOCS11-PUBLIC.md", "c58bba93b1cc7bc65814fe4a35c4702fd246205250c69405f3c591a037d97c2a"),
    ("G2-lot-POST-PREREG.md", "768f263d5a4510f8d23c9aaca0a8f597001c75d7eb2d43b7de5dcda136072020"),
    ("G2-lot-SG5-INTERDITS.md", "1547894337a2e83d636e24208136b84f33a4a1f5ec5d72027423c50a3d2c3a34"),
    ("G2-partie-2.md", "0b45a458a53878f70b5826653eecc82615b980d7f57ce0317bee5c20391914d9"),
    ("G2-partie-3.md", "c6e3962a440c0a32be9eb332c3807da538e3e5c6cbf0430ec96f3474dc20c138"),
    ("G2-partie-4.md", "a28bb38393f7d7ab8e40a4cdfeb03128555234e7438e12626cdd4ae11f3c5166"),
])


def refus(racine: str, admis) -> list:
    """Motifs de refus des journaux G1/G2 de `racine`/docs ; liste vide : conforme."""
    motifs = []
    for chemin in sorted(glob.glob(os.path.join(racine, "docs", "G1-*.md")) +
                         glob.glob(os.path.join(racine, "docs", "G2-*.md"))):
        nom = os.path.basename(chemin)
        with open(chemin, "rb") as f:
            octets = f.read()
        if EXEMPTES.get(nom) == hashlib.sha256(octets).hexdigest():
            continue
        lignes = [x for x in octets.decode("utf-8", "replace").split(chr(10)) if x.startswith(TETE)]
        if len(lignes) != 1:
            motifs.append(f"{nom} : {len(lignes)} ligne(s) « {TETE} », une exigée")
            continue
        reste = lignes[0][len(TETE):]
        ident, sep, apres = reste[2:].partition("`")
        if not reste.startswith(" `") or not sep or apres[:1] not in ("", " ") or not admis(ident):
            motifs.append(f"{nom} : ligne « Modèle » hors forme ou identifiant hors liste blanche : {lignes[0][:90]!r}")
    return motifs


def main(argv: list) -> int:
    if len(argv) != 1 or not os.path.isdir(os.path.join(argv[0], "docs")):
        print(f"journaux-modele : erreur : racine illisible {argv!r}", file=sys.stderr)
        return 3
    try:
        spec = importlib.util.spec_from_file_location("oracle_record", OUTIL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        motifs = refus(argv[0], module.auteur_admis)
    except Exception as e:      # DT3-F (C-4 de la G2) : sortie 3, jamais 1
        print(f"journaux-modele : erreur : {e}", file=sys.stderr)
        return 3
    for m in motifs:
        print(f"journaux-modele : refus : {m}", file=sys.stderr)
    if not motifs:
        print(f"journaux-modele : conforme ({len(EXEMPTES)} journaux exemptés par nom et sha256)")
    return 1 if motifs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
