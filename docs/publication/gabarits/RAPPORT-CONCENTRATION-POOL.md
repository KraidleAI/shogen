# Rapport de concentration d'infrastructure de livraison — pool de `<libre.client>` (gabarit)
> Gabarit versé le 2026-10-15 (`date -u`, lot PRODUIT-R2) ; rattachement : ADR-0028 §4 pt 7 et D9, AVIS-PRODUIT-APRES-S2
> §3 et §4, doc 04 §1, §3, §4, doc 07 §3, §5, doc 09 ; règles : `docs/publication/gabarits/README.md` ; contrôle :
> `scripts/publication/gabarit_controle.py`. Chaque champ nomme la sortie du harnais qui le produit (`chemin:ligne` au
> commit du gabarit) ; un rapport rempli garde le texte fixe à l'octet, ses champs tous remplis ou tous vides.

## 1. Identité du pool et date
- Client (déclaration, rang R3 : ne modifie jamais k_eff, doc 04 §3) : `<libre.client>`
- Date du rapport (`date -u`, forme `AAAA-MM-JJTHH:MM:SSZ`) : `<date.rapport>`
- Pool configuré, ligne `pool` du bloc 1 du rendu (`s2-harness/shogen_s2/report.py:203` (`{key:24} = {params[key]}`)) :
  `<rendu.pool>` ; les flux sans lecture `ok` en sortent (ADR-0028 D1, `s2-harness/shogen_s2/report.py:268`
  (`pool_analyse_retrait`)), la partition ne porte que le pool d'analyse.
- Segment et plages exclues, ligne `segment` du bloc 1 (`s2-harness/shogen_s2/report.py:224` (`{'segment':24}`)), puis
  chaque ligne `exclusion_window_start` (`s2-harness/shogen_s2/report.py:232` (`exclusion_window_start`)) : `<rendu.segment>`

## 2. Méthode
- **k_eff côté livraison** : nombre de classes de la partition des hôtes par les recouvrements R2 mesurés
  (`s2-harness/shogen_s2/r2.py:772` (`def compute_partition`)) ; k nominal = nombre d'hôtes distincts. L'adresse
  observée est celle de la couche de livraison (CDN, anycast), non de l'origine (résidu 1, `s2-harness/shogen_s2/r2.py:87`
  (`RESIDUS_ASN`)). k_eff n'est pas un compte d'indépendance.
- **k nominal**, détail de méthode hors tête (doc 04 l.172 : seul k_eff est publié en tête), ligne `k nominal` du
  bloc 6 (`s2-harness/shogen_s2/report.py:623` (`k nominal = `)) : `<rendu.k-nominal>`
- **Partition ASN datée et cross-confirmée** : sonde par hôte (`s2-harness/shogen_s2/r2.py:345` (`def collect_asn`)),
  DNS-over-HTTPS puis RIPEstat et Team Cymru (`s2-harness/shogen_s2/r2.py:315` (`def resolve_host_real`)) ; seul un
  hôte dont les deux bases concordent fusionne, sinon singleton non confirmé et k_eff borne supérieure
  (`s2-harness/shogen_s2/r2.py:381` (`def _asn_state`)). Date : dernier relevé retenu par hôte.
- **Amonts déclarés `basis:doc`** : nommés, ne fusionnent pas (ADR-0008), désignent où mesurer le contenu
  (`s2-harness/shogen_s2/r2.py:120` (`METHOD_EDGES`)).
- **Corroborations de contenu** : cinq statistiques par paire de flux, seule l'identité exacte fusionne
  (`s2-harness/shogen_s2/r2.py:709` (`def compute_content`) ; `s2-harness/shogen_s2/r2.py:199` (`MERGE_CRITERION_V0`)).
- **Hors de ce rapport** : la co-défaillance mesurée (R1, doc 04 §2) ; blocs 3 et 4 et drapeaux du bloc 6 non recopiés.

## 3. Tête (bloc 6 du rendu)
- k_eff et sa note (`s2-harness/shogen_s2/report.py:631` (`k_eff     = `) ; borne supérieure :
  `s2-harness/shogen_s2/report.py:627` (`BORNE SUPÉRIEURE`)) : `<rendu.k-eff>`
- Date de la partition (`s2-harness/shogen_s2/report.py:635` (`date de la partition`)) : `<rendu.date-partition>`
- Partition nommée, amonts déclarés, caveats (`s2-harness/shogen_s2/report.py:645` (`PARTITION NOMMÉE`)) :
```text
<rendu.partition>
```

## 4. Observables (bloc 5 du rendu)
Lignes recopiées : (a) ASN datés, CNAME, divergences (`s2-harness/shogen_s2/report.py:525` (`(a) AXE ASN`)) ; (b)
lignes par paire (`s2-harness/shogen_s2/report.py:565` (`(b) AXE CONTENU`)) ; (c) arêtes `basis:doc`
(`s2-harness/shogen_s2/report.py:596` (`(c) AXE MÉTHODE`)) ; (e) résidus (`s2-harness/shogen_s2/report.py:616` (`(e) LES 7`)).
```text
--- (a)
<rendu.table-asn>
--- (b)
<rendu.contenu>
--- (c)
<rendu.amonts>
--- (e)
<rendu.residus>
```

## 5. Axes non mesurés (champ non optionnel)
Doc 04 l.129-139, recopiées :
> Chaque certificat embarque, en clair, son périmètre :
>
> 1. Un axe non mesuré reste un mode commun possible. La liste des axes
>    mesurés est exhaustive dans le certificat ; tout le reste est hors
>    mesure. (Knight & Leveson appliqué à nous-mêmes : nos axes sont nos
>    deux universités.) **Cette exhaustivité est un champ NON OPTIONNEL du
>    certificat** (ADR-0019 D7, GTM canal 2) : c'est la parade au seul canal de
>    conflit que ni la vérification offline ni le benchmark public ne ferment —
>    le jeu sur les axes ; le canal 2 payant (oracle certifiant son propre feed)
>    n'est défendable que si chaque certificat publie ce qu'il n'a **pas** mesuré.
>    Exigence ferme en S4, candidate à un ADR de spec du certificat.

Axes mesurés, liste exhaustive : l'ASN de l'adresse de livraison de chaque hôte (R2, cross-confirmé) ; l'identité exacte
de contenu entre flux (R2). Hors mesure, au moins : (1) la co-défaillance des flux (R1) ; (2) l'origine derrière un CDN
ou un anycast, et l'opérateur (résidus 1 et 2) ; (3) la pluralité des points d'observation et des résolveurs (résidus 3
et 5) ; (4) l'ASN et les CNAME entre deux relevés (résidus 4 et 7) ; (5) IPv6 : seuls les enregistrements A sont
résolus, la forme Cymru ne couvre pas IPv6 (`s2-harness/shogen_s2/r2.py:292` (`def _cymru_asn`)) ; (6) l'émetteur de
certificat TLS et les attestors (doc 04 §1) ; (7) une méthode commune hors des arêtes `basis:doc` recopiées, un amont qui
bruite ses copies (doc 04 §5) ; (8) la qualité du marché amont (doc 04 §4 pt 6) et les entrées rédigées (pt 5) ; (9) les
déclarations R3, publiées, jamais comptées. Propres à ce pool (hôtes non attribués, flux retirés par D1, autres) :
`<libre.axes-pool>`

## 6. Recette de recalcul hors ligne
Empreintes : `control.jsonl` `<sha256.control>` ; `journal.jsonl` `<sha256.journal>` ; `raw.jsonl` `<sha256.raw>` ;
rendu (sortie de la commande 3) `<sha256.rendu>`. Commit du harnais `<commit.harnais>` ; Python `<version.python>`.
Variables : `J` (dossier des trois journaux), `DEPOT` (dépôt), `H` (extraction), `S` (sortie), `O` (options du rendu).
```bash
cd "$J" && sha256sum control.jsonl journal.jsonl raw.jsonl        # 1. égal aux empreintes
git -C "$DEPOT" archive <commit.harnais> s2-harness | tar -x -C "$H"     # 2. extraction du commit
cd "$H/s2-harness" && env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m shogen_s2.report "$J" $O > "$S/rendu.txt"  # 3.
sha256sum "$S/rendu.txt"                                           # 4. égal à l'empreinte du rendu
```
Commande 3 : `s2-harness/shogen_s2/report.py:755` (`def main`) ; `O` se lit au champ du segment (§1) : `--segment-from`
avec `--segment-to` ou `--segment-n-fixe` (ligne `segment`), puis un `--exclude-window-start-range` par ligne
`exclusion_window_start`, dans leur ordre ; `O` est vide sans segment ni plage. R2 y est
calculé par `s2-harness/shogen_s2/r2.py:1030` (`def compute_r2`), comme au point d'entrée recalculable `s2-harness/shogen_s2/r2.py:1068`
(`def recompute_r2_from_journal`). Journaux du pool client seulement, jamais ceux scellés de S2 (SHOGEN-RENDU-CLI-REPORT-1).

## 7. Limites et vocabulaire
- Collecte : le harnais ne collecte que le pool figé de `s2-harness/shogen_s2/sources.py:239` (`SPECS`), avec les arêtes
  `basis:doc` de ce pool ; un pool client demande un lot rattaché, sans lequel ce gabarit ne se remplit pas.
- Partition instantanée ; un observateur, un résolveur par relevé (résidu 5) ; k_eff compté côté livraison : rien n'est
  dit de l'origine, de l'exactitude ou de la profondeur d'un flux (doc 09 l.24 et l.30), ni hors du pool, du segment et
  de l'observateur nommés. L'égalité à l'octet d'un rendu rejoué ailleurs n'est pas mesurée.
- Aucune prétention R1 tant que S2-bis n'a pas rendu ; aucune phrase réglementaire (aucun texte DORA ou MiCA détenu,
  AVIS-PRODUIT-APRES-S2 §3). Vocabulaire : doc 09 en entier ; le contrôle n'en mécanise qu'une partie.
