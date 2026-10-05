"""CB-18f, SHOGEN-S2BIS-FORMAT-RETOUCHES-1 (annexe B d'ADR-0028, B.63), étendu par I-2 de la G2 du recalcul : le FORMAT
porte les retouches de l'item. Valeurs attendues tirées du texte de l'item, non du FORMAT : « FORMAT §12 : citer aussi
RFC 1035 §7.3 et marquer la règle de source (adresse et port interrogés) comme choix du lot ; ajouter CB-11h à l'en-tête
« Corrections » » ; I-2 : « FORMAT §7.1 doit dire les contrôles de type que fait `_lire` (`suivante`, `ws`, `a`,
dernière fenêtre) ». CB-18j (G2 de la tranche C) : convention des citations « ADR-0029 l.N » écrite dans l'en-tête
(SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1 : « elles suivent l'ADR au commit e16956b, convention du G0 ») ; `run_params`
placé dans l'ordre de la première fenêtre d'une exécution (§11.5, observation de la G2)."""
import hashlib
import json
import os
import pathlib
import tempfile
import unittest

from shogen_s2bis.collecte import journal

NL = chr(10)
FORMAT = pathlib.Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs",
                      "adr-0029", "s2bis", "FORMAT-JOURNAUX-S2BIS.md")
W, WS = 60, 1791154680                                              # 2026-10-04 22:58 UTC


def decoupe(texte):
    """(puces de l'en-tête, {numéro : texte de la section « ## n. », espaces ramenés à un seul})."""
    parties = texte.split(NL + "## ")
    return parties[0].split(NL + "- "), {p.split(".", 1)[0]: " ".join(p.split()) for p in parties[1:]}


def integres(*enrs):
    """Nombre de lignes intègres selon `Journal._lire` d'un fichier fait des enregistrements `enrs`, chaînés ici."""
    prec, lignes = "0" * 64, []
    for seq, e in enumerate(enrs):
        lignes.append(json.dumps({**e, "seq": seq, "prec": prec}, sort_keys=True, separators=(",", ":")).encode()
                      + NL.encode())
        prec = hashlib.sha256(lignes[-1]).hexdigest()
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, "pool-2026-10-04-0.jsonl").write_bytes(b"".join(lignes))
        pos = journal.Journal(d, "pool", w=W)._lire("pool-2026-10-04-0.jsonl")[0]
    return [len(b"".join(lignes[:i + 1])) <= pos for i in range(len(lignes))].count(True)


class Format(unittest.TestCase):
    def test_retouches_du_paragraphe_12_et_de_l_en_tete(self):
        """§12 : la citation de la RFC 1035 garde §4.1.1-4.1.2 et ajoute §7.3 ; la phrase de la règle de source nomme
        l'adresse et le port interrogés, la marque choix du lot, non règle de la RFC, et renvoie au §7.3. En-tête : la
        puce « Corrections », une seule, nomme CB-11h."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        self.assertIn("12", sections)
        douze = sections["12"]
        self.assertIn("RFC 1035 §4.1.1-4.1.2, §7.3", douze)
        phrases = [p for p in douze.split(". ") if "adresse et du port interrogés" in p]
        self.assertEqual([("choix du lot" in p, "non une règle de la RFC 1035" in p, "§7.3" in p) for p in phrases],
                         [(True, True, True)])
        corrections = [p for p in puces if p.startswith("**Corrections** :")]
        self.assertEqual([("CB-11h" in p) for p in corrections], [True])

    def test_paragraphe_7_1_dit_les_controles_de_type_de_lire(self):
        """I-2 : au point 1 du §7, une phrase, une seule, dit les contrôles de type et nomme `suivante`, `ws`, `a` et la
        dernière fenêtre, en entiers ; `_lire` les fait : la même ligne, intègre au champ entier, ne l'est plus quand ce
        champ est une chaîne (le texte ne promet rien que le code ne fasse)."""
        _puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        point1 = sections["7"].split(" 2. ")[0]
        phrases = [p for p in point1.split(". ") if "contrôlés en type" in p]
        noms = ("`suivante`", "`ws`", "`a`", "dernière fenêtre", "entier")
        self.assertEqual([[x in p for x in noms] for p in phrases], [[True] * 5])
        o = {"type": "ouverture", "jour": "2026-10-04", "suivante": WS}
        for champ, enr in (("suivante", o), ("ws", {"type": "marqueur", "ws": WS}),
                           ("ws", {"type": "lecture", "ws": WS}), ("a", {"type": "trou", "de": WS, "a": WS})):
            avant = [] if enr is o else [o]
            with self.subTest(champ=champ, type=enr["type"]):
                self.assertEqual((integres(*avant, enr), integres(*avant, {**enr, champ: "x"})),
                                 (len(avant) + 1, len(avant)))

    def test_convention_des_citations_et_run_params_dans_l_ordre_de_la_fenetre(self):     # CB-18j
        """En-tête : une puce « Citations », une seule, dit que « ADR-0029 l.N » renvoie à l'ADR au commit e16956b et
        nomme l'item. §11.5 : `run_params` y est placé, en tête de la première fenêtre admise d'une exécution, avant
        toute `lecture`."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        citations = [" ".join(p.split()) for p in puces if p.startswith("**Citations**")]
        self.assertEqual([("« ADR-0029 l.N » renvoie à la ligne N de l'ADR-0029 au commit `e16956b`" in p,
                           "CITATIONS-ADR-DECALEES-1" in p) for p in citations], [(True, True)])
        cinq = sections["11"].split(" 5. ", 1)[1].split(" 6. ", 1)[0]
        self.assertEqual([("première fenêtre" in p, "précède toute `lecture`" in p) for p in cinq.split(". ") if
                          "`run_params`" in p], [(True, True)])


if __name__ == "__main__":
    unittest.main()
