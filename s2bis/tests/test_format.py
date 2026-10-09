"""CB-18f, SHOGEN-S2BIS-FORMAT-RETOUCHES-1 (annexe B d'ADR-0028, B.63), étendu par I-2 de la G2 du recalcul : le FORMAT
porte les retouches de l'item. Valeurs attendues tirées du texte de l'item, non du FORMAT : « FORMAT §12 : citer aussi
RFC 1035 §7.3 et marquer la règle de source (adresse et port interrogés) comme choix du lot ; ajouter CB-11h à l'en-tête
« Corrections » » ; I-2 : « FORMAT §7.1 doit dire les contrôles de type que fait `_lire` (`suivante`, `ws`, `a`,
dernière fenêtre) ». CB-18j (G2 de la tranche C) : convention des citations « ADR-0029 l.N » écrite dans l'en-tête
(SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1 : « elles suivent l'ADR au commit e16956b, convention du G0 ») ; `run_params`
placé dans l'ordre de la première fenêtre d'une exécution (§11.5, observation de la G2). CB-18o (lettres C-1 et C-2 du
FORMAT, avis sur le banc de concordance) : une seule définition d'« intègre » au §7.1, points (a) à (e), sans limite
déclarée, et `_lire` la fait. CB-19a (C-1 (a) de la relecture d'intégration de P1) : §12, réponse appariée de plus
de 512 octets en `forme`, deux citations de la RFC 1035 mot pour mot (texte lu au fichier du registre, sha256
d14ae809…)."""
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
    """Nombre de lignes intègres selon `Journal._lire` d'un fichier fait des enregistrements `enrs`, chaînés ici
    (`seq` et `prec` d'un enregistrement, s'il les porte, remplacent ceux de la chaîne ; des octets : ligne brute)."""
    prec, lignes = "0" * 64, []
    for seq, e in enumerate(enrs):
        lignes.append(e if type(e) is bytes else json.dumps({"seq": seq, "prec": prec, **e}, sort_keys=True,
                                                             separators=(",", ":")).encode() + NL.encode())
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

    def test_paragraphe_12_reponse_de_plus_de_512_octets(self):     # CB-19a, C-1 (a) de la relecture d'intégration
        """§12 : le statut `forme` nomme la réponse appariée de plus de 512 octets ; la règle cite la RFC 1035 §2.3.4 et
        §4.2.1 mot pour mot ; la puce « Corrections » nomme CB-19a. Citations prises au fichier de la RFC (l.529,
        l.1756-1758), blancs ramenés à un seul."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        douze = sections["12"]
        attendus = ("réponse appariée de plus de 512 octets ou mal formée",
                    "RFC 1035 §2.3.4 : « UDP messages 512 octets or less »",
                    "§4.2.1 : « Messages carried by UDP are restricted to 512 bytes (not counting the IP or UDP "
                    "headers). Longer messages are truncated and the TC bit is set in the header. »")
        self.assertEqual([x in douze for x in attendus], [True] * 3)
        self.assertEqual([("CB-19a" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_paragraphe_13_6_taille_de_la_plus_grande_sante(self):    # CB-19b, C-1 (b) de la relecture d'intégration
        """§13.6 : sept témoins et sept noms au plus, borne de `reponses`, ligne du témoin (3 823 224 octets, recomptée
        par `test_sante.Taille`) sous LIMITE, hypothèse sur `tardives` écrite ; §14.1 : les deux bornes à `sante.json` ;
        la puce « Corrections » nomme CB-19b."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        six = sections["13"].split(" 6. ", 1)[-1]
        attendus = ("sept témoins et sept noms au plus", "1 + 495 × (18 × 1 024 + 85) / 36", "3 823 224 octets",
                    "marge de 371 080 octets", "hypothèse : `tardives` compte au plus 2 × `places` latences")
        self.assertEqual([x in six for x in attendus], [True] * 5)
        self.assertEqual([x in sections["14"] for x in ("canoniques, sept au plus", "valides, sept au plus")],
                         [True] * 2)
        self.assertEqual([("CB-19b" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_paragraphe_6_4_fsync_du_dossier(self):                  # CB-19c, C-2 (a) de la relecture d'intégration
        """§6.4 : fsync du dossier après la création d'un fichier du journal et du fichier de sommes (texte de la
        correction), la limite déclarée d'avant retirée, celle du modèle du banc écrite ; puce « Corrections » :
        CB-19c."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        quatre = sections["6"].split(" 4. ", 1)[-1]
        self.assertEqual([x in quatre for x in ("l'écrivain appelle `fsync` sur le dossier", "fichier du journal",
                                                "fichier de sommes", "ne le prouve pas",
                                                "n'est pas suivie d'un `fsync` du dossier")], [True] * 4 + [False])
        self.assertEqual([("CB-19c" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_paragraphe_4_points_de_fsync_et_preuve_du_banc(self):    # CB-19d, C-2 (b) et C-4 (c) de la relecture
        """§4 : « et seulement là » retiré (C-4 (c) : contredit les §6.2, §6.3 et §7.4) ; les fsync de C-2 (b) nommés
        (fichier chaîné, queues déclarées, avant la `reprise` en segment neuf ; fichier sommé, avant sa somme) ; preuve
        du banc à coupures (0 rupture, 0 somme fausse, contre 128 et 131), ce que son modèle prouve et ne prouve pas ;
        puce « Corrections » : CB-19d."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        attendus = ("et seulement là", "dont elle chaîne la dernière ligne intègre", "dont elle déclare la queue",
                    "avant d'écrire la somme d'un fichier", "0 rupture et 0 somme fausse (128 et 131 avant C-2)",
                    "Ce que le modèle prouve", "Ce qu'il ne prouve pas")
        self.assertEqual([x in sections["4"] for x in attendus], [False] + [True] * 6)
        self.assertEqual([("CB-19d" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_paragraphe_11_4_adresse_avant_la_phase_dns(self):       # CB-19e, C-3 (b) de la relecture d'intégration
        """§11.4 : le client pose l'adresse au suivi avant la phase `dns`, la boucle relève les phases avant l'adresse ;
        puce « Corrections » : CB-19e."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        quatre = sections["11"].split(" 4. ", 1)[1].split(" 5. ", 1)[0]
        self.assertEqual([x in quatre for x in ("le client pose l'adresse au suivi avant la phase `dns`",
                                                "relève les phases avant l'adresse")], [True] * 2)
        self.assertEqual([("CB-19e" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_corrections_c4_tardives_run_params_adresse(self):       # CB-19g, C-4 (a), (b), (d) de la relecture
        """C-4, FORMAT seul (valeurs prises au texte de l'adjudication) : (a) §11.6, une lecture finie entre E et le
        relevé compte en `tardives` à la fenêtre suivante ; (b) §11.5, `run_params` suit l'`ouverture` de la bascule
        qu'il déclenche, dans la phrase unique de `run_params` ; (d) §9.1, l'adresse est l'adresse résolue, contactée
        seulement si `phases` porte la connexion ; §10.1, une `dns` rendue après une résolution tardive porte
        `phases.dns` et une adresse non contactée. (c), au §4, est portée par CB-19d. Puce « Corrections » : CB-19g."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        cinq = sections["11"].split(" 5. ", 1)[1].split(" 6. ", 1)[0]
        attendus = [(sections["11"], "une lecture finie entre E et le relevé compte en `tardives` à la fenêtre "
                                     "suivante"),
                    (cinq, "`run_params` suit l'`ouverture` de la bascule qu'il déclenche"),
                    (sections["9"], "l'adresse résolue"),
                    (sections["9"], "contactée que si `phases` porte la connexion"),
                    (sections["10"], "une `dns` rendue après une résolution tardive porte `phases.dns` et une adresse "
                                     "non contactée")]
        self.assertEqual([x in s for s, x in attendus], [True] * 5)
        self.assertEqual([("CB-19g" in p) for p in puces if p.startswith("**Corrections** :")], [True])

    def test_paragraphe_7_1_definition_unique_d_integre(self):        # CB-18o, lettres C-1 et C-2 (et I-2)
        """Au point 1 du §7, une seule définition d'« intègre », points (a) à (e) de la lettre (bornes de 640 chiffres
        et de 64 niveaux, types du §1.3 et du §2, chaîne), un booléen n'étant jamais un entier, et plus aucune « limite
        déclarée ». `_lire` la fait : chaque champ commun ou propre, au type du FORMAT, laisse la ligne intègre ; à un
        autre type (booléen pour un entier compris), ou absent, il la rend non intègre (le texte ne promet rien que le
        code ne fasse). Valeurs prises au texte de la lettre."""
        _puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        point1 = sections["7"].split(" 2. ")[0]
        self.assertEqual([x in point1 for x in ("(a)", "(b) ", "(c) ", "(d) ", "(e) ", "640 chiffres", "N = 64",
                                                 "Un booléen JSON n'est jamais un entier", "Limites déclarées")],
                         [True] * 8 + [False])
        o, cle = {"type": "ouverture", "jour": "2026-10-04", "suivante": WS}, "2026-10-04"
        types = {"ouverture": {"jour": cle, "suivante": WS}, "marqueur": {"ws": WS}, "point": {"ws": WS},
                 "cloture": {"jour": cle}, "reprise": {"ws": WS, "suivante": WS, "queue": None},
                 "trou": {"de": WS, "a": WS, "cause": "saut"}, "lecture": {"ws": WS}}
        for genre, champs in types.items():
            for champ, bon in champs.items():
                mauvais = ["x", True, None] if type(bon) is int else [5, None] if bon == cle or champ == "cause" else [
                    {}, "x", 5]
                with self.subTest(type=genre, champ=champ):
                    self.assertEqual([integres(o, {"type": genre, **champs, champ: v}) for v in [bon] + mauvais] + [
                        integres(o, {"type": genre, **{k: v for k, v in champs.items() if k != champ}})],
                        [2] + [1] * (len(mauvais) + 1))
        self.assertEqual([integres(o, {"type": "lecture", "ws": WS, "seq": s}) for s in (1, True)], [2, 1])   # (c)
        self.assertEqual([integres(o, {"type": 5, "ws": WS}), integres({**o, "prec": "0" * 63}),
                          integres({**o, "prec": None})] + [integres({**o, "prec": p * 64}) for p in "0aAg"],
                         [1, 0, 0, 1, 1, 0, 0])                                                             # (c)
        self.assertEqual([integres(o, {"type": "reprise", "ws": WS, "suivante": WS, "queue": [{"fichier": "f"}]}),
                          integres(o, ("[1]" + NL).encode())], [2, 1])                                     # (d), (b)

    def test_paragraphe_7_4_objet_nu_et_reprises_declarees(self):    # contre-contrôle de CB-18, O-1 (CB-18t)
        """§7.4 (point 4 du §7) : l'incise d'O-1 sur l'objet nu, la phrase de l'avis l.78 sur les reprises déclarées,
        mot pour mot, et l'ordre de lecture, §7.1 avant §7.4. Valeurs prises au texte de l'adjudication et de l'avis."""
        _puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        point4 = sections["7"].split(" 4. `reprise` porte")[1].split(" 5. ")[0]
        attendus = ("un objet nu (un objet nu rend déjà la ligne non intègre, §7.1 d)",
                    "Une `reprise` au lien rompu ou à déclaration fausse est une rupture **non déclarée** ; sa "
                    "déclaration n'est pas lue ; toutes les queues en attente sont rendues avec elle. Ne comptent "
                    "comme reprises déclarées que les `reprise` intègres, au lien juste, à déclaration exacte.",
                    "Les lecteurs appliquent le §7.1 avant le §7.4.")
        self.assertEqual([x in point4 for x in attendus], [True] * 3)

    def test_paragraphes_9_et_14_valeurs_et_decodeur(self):        # CB-6c, SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1
        """§9.1 : clés exactes d'un relevé, borne de 2 097 152 octets, item nommé ; §14.1 : `decodeur` et sa règle ;
        puce « Partie P2 » : CB-6c et l'item."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        attendus = [(sections["9"], "`actif`, `classe`, `devise`, `prix`, `ts_source` et `extra`"),
                    (sections["9"], "borne de 2 097 152 octets de JSON canonique"),
                    (sections["9"], "SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1"), (sections["14"], "règle `decodeur-connu`"),
                    (sections["9"], "« T » majuscule"), (sections["9"], "ne lit pas la même chose de 3.10 à 3.13")]
        self.assertEqual([x in s for s, x in attendus], [True] * 6)          # deux derniers : C-5 de la G2 de P2A
        self.assertEqual([("CB-6c" in p, "ECRIVAIN-REFUS-ARRET-1" in p) for p in puces if p.startswith(
            "**Partie P2, tranche A**")], [(True, True)])

    def test_paragraphes_8_et_13_items_de_cb_6d(self):                # CB-6d : trois items de l'annexe B
        """§8.3 : niveaux comptés sur les octets avant le décodeur ; §8.4 : valeurs comptées par occurrence ; §13.6 :
        résultat rendu avant la place ; la puce « Partie P2 » nomme CB-6d et les trois items."""
        puces, sections = decoupe(FORMAT.read_text(encoding="utf-8"))
        huit, six = sections["8"], sections["13"].split(" 6. ", 1)[-1]
        attendus = [(huit, "sur ses octets, avant tout décodeur"), (huit, "une fois par occurrence"),
                    (six, "le résultat d'une lecture est rendu avant sa place")]
        self.assertEqual([x in s for s, x in attendus], [True] * 3)
        self.assertEqual([all(x in p for x in ("CB-6d", "TARDIVES-BORNE-1", "IMBRICATION-OCTETS-1", "CORPS-BORNE-1"))
                          for p in puces if p.startswith("**Partie P2, tranche A**")], [True])

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
