#!/usr/bin/env python3
"""out/tables.md + cibles.json + out/cibles-actifs.json + pourquoi.json -> CARTO-DEFI-ORACLES.md"""
import json,os,datetime,collections,hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); O=lambda f:f'{HERE}/{f}'
R={r['name']:r for r in json.load(open(O('out/rows.json')))}; C=json.load(open(O('cibles.json')))
A=json.load(open(O('out/cibles-actifs.json'))); W=json.load(open(O('pourquoi.json'))); B=json.load(open(O('out/biais.json')))
T=open(O('out/tables.md')).read()
# garde-fous : les chiffres cites en texte doivent etre ceux des tables (sinon l assemblage s arrete)
for must in ['| Chainlink | 129 | 46 060 | 0 |','| RedStone | 51 | 11 084 | 1 256 |','| Pyth | 66 | 5 947 | 88 |','| Chainlink + RedStone | 28 | 15 730 | 8 | 185 |','| Chainlink + Pyth | 17 | 2 851 | 9 |','RedStone 1 256 M$ (Pendle V2','Pyth 88 M$ (Usual USD0','15 premieres des 67 chaines (52 des 136 protocoles']:
    assert must in T,must
assert B['deadurl']['n']==24 and B['deadurl']['tvl_m']==353 and B['deadurl']['nA']==20 and B['deadurl']['nB']==4 and B['deadurl']['decl']==15
assert (B['sans_rng_por']['nB'],B['sans_rng_por']['n'],B['sans_rng_por']['decl'],B['sans_rng_por']['decl_tvl_m'],B['sans_rng_por']['chainlink'],B['sans_rng_por']['witnet'])==(78,423,244,67349,128,0)
assert not any(r['deadUrl'] for n,r in R.items() if n in [x for t in 'GMP' for x in C[t]]), 'une cible deadUrl'
assert [g['name'] for g in B['grands_multi'] if g['studied']]==['SparkLend','Compound V3','Kamino Lend','Venus Core Pool']
assert sorted(c['name'] for c in B['cinq_oracles'])==['Re7 Labs','River Omni-CDP','ZeroLend Lending']
CC=collections.Counter(R[n]['primary'] for t in 'GMP' for n in C[t])
P=json.load(open(O('raw/protocols.json')))
sha=lambda f:hashlib.sha256(open(O(f),'rb').read()).hexdigest()
M=lambda v:f'{v/1e6:,.1f}'.replace(',',' ')
def oracs(r):
    s=[]
    for n,t,ch in r['oracles']:
        s.append(n+(f' ({t})' if t and t!='legacy' else (' (champ ancien)' if t=='legacy' else ''))+(' @'+','.join(ch) if ch else ''))
    return '; '.join(s) if s else '**non renseigne [abs]**'
def chs(r): return ', '.join(f"{c} {v/1e6:.0f}" for c,v in sorted(r['chains'].items(),key=lambda x:-x[1]) if v>=1e6)   # liste entiere (>= 1 M$ par chaine), sans coupure
def inc(r):
    return '; '.join(f"{datetime.date.fromtimestamp(h['date'])} {h['technique']} {h['amount']/1e6:.2f} M$" if h.get('amount') else f"{datetime.date.fromtimestamp(h['date'])} {h['technique']}" for h in sorted(r['hacks'],key=lambda h:h['date'])) or 'aucun classe'
def par(n):
    if A[n].get('absent'): return '**non calcule [abs]** (detail absent de `raw/detail/`)'
    p=A[n]['parts']; return f"BTC {p['BTC']:.0f} / ETH {p['ETH']:.0f} / USDC {p['USDC']:.0f} / USDT {p['USDT']:.0f} %"
L=[]
L.append(f"""# CARTO-DEFI-ORACLES — protocoles DeFi qui dependent d oracles, toutes chaines, toutes tailles (source : DefiLlama)

Gate 0 : modele resolu `claude-sonnet-5-5`, effort high (lecteur `shogen-lecteur`), pour la passe initiale et pour la passe de corrections. Date de lecture des donnees : 2026-10-04 (horloge `date -u` : 18:30 a 18:35 UTC) ; passe de corrections G2 : 2026-10-04, `date -u` 21:02 a 21:11 UTC.
Brief : `BRIEF-CARTO-DEFI.md`, sha256 `bd8855d9763fa0f7b4c5560750f8dda6518339737149e4f1d64f7548c31f14bf` (recalcule, identique). Relecture G2 : `g2/G2-CARTO.md`, sha256 `{sha('g2/G2-CARTO.md')}` (verdict ACCEPTE-AVEC-CORRECTIONS, corrections C-1 a C-13) ; brief des corrections : `g2/BRIEF-CORRECTIONS-CARTO.md`, sha256 `{sha('g2/BRIEF-CORRECTIONS-CARTO.md')}`. Cette version applique les corrections (section 9) ; la version precedente est gardee hors versement dans `v1/`.
Niveaux : [lu] = lu dans la reponse de l API DefiLlama du jour ou dans le depot ; [abs] = absent de la source ; [inféré] = ma deduction ; [calc] = calcul de mes scripts sur des [lu]. Aucune prise de contact ; aucune operation git ; aucun reseau pendant la passe de corrections.
Attestation d exposition : aucune piece de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl`, aucune piece de la liste D.2 de l annexe D d ADR-0028 ouverte, aucun journal de campagne lu. Pieces du depot lues, en lecture seule, pour la passe de corrections : `docs/09-vocabulaire.md` (en entier, sha256 `001b960674e15cdf4d68301d3a79a65b78249dfa77999b6c47fa441e3e9f2831`) ; `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md` (sha256 `69f9ddbb78f374d82bd062909719e160f05e8e206753ef6bf097a738908eea9b`, lignes 322, 344, 359, 463 et titres) ; `docs/adr-0029/etude-marche/P1-DEFI-PRET.md` (sha256 `b4161c5291c62a754e9fea96e997af8880bea9b91aad2b4c26eac78569ecf7d4`, lignes 8, 42, 117) ; `docs/adr-0029/ADR-0029-campagne-S2-bis.md` (lignes 10 a 13 seulement) ; `CLAUDE.md`. Passe initiale : la piece cite P1 et SYNTHESE (recherche de mots, section 4, ligne USDD) ; le reste de son attestation n est pas reconstitue ici et reste a confirmer par le controle de transcription de l orchestrateur. Aucune ecriture hors du dossier de travail de la carte, aucune cle, aucun compte.

## 1. Resume

- DefiLlama liste **{len(P)} protocoles**. Apres filtre (TVL >= 1 M$, ni CEX, ni chaine, ni mort : mort = champ `deadFrom` renseigne), **{len(R)}** protocoles dependent d un prix ou declarent un oracle : 345 dans les categories ecrites d avance (A) et 79 dans d autres categories mais avec un oracle declare (B). Trois biais de perimetre sont declares en section 7 (points 11 a 13) : 24 protocoles `deadUrl` restes dans le perimetre, des usages d oracle sans lien avec un prix, des paires presentees comme des combinaisons.
- Seuls **246 sur 424 (58 %)** ont un oracle declare ; ils pesent 67,8 Md$ sur 93,3 Md$ (73 % de la TVL). Le champ est vide pour 42 % des protocoles, dont des geants (Ethena USDe, 4,9 Md$ ; Falcon Finance ; Morpho Blue — deja etudie).
- Parmi les 246 : **170 n ont qu un oracle declare** (dependance unique), **76 en ont deux ou plus** (question des racines communes). Paires d oracles co-declarees les plus frequentes (non additives : un protocole a trois oracles figure dans trois paires) : Chainlink et RedStone sont declares ensemble par 28 protocoles, dont 8 (185 M$) declarent exactement ces deux oracles ; Chainlink et Pyth par 17, dont 9 exactement ces deux (T4).
- Chainlink est declare par 129 protocoles (46,1 Md$ de valeur declaree, regle de la section 2.3 ; la version precedente de la piece donnait 44,7 Md$ par erreur de code, section 9), Pyth par 66, RedStone par 51.
- Liste courte de 30 cibles plus bas : 10 grandes, 10 moyennes, 10 petites, sur {len(CC)} chaines principales ; les 7 familles deja etudiees (Aave, Spark, Morpho, Euler, Compound, Kamino, Venus) en sont exclues. Sky Lending, present dans la version precedente, est sorti de la liste : son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” (P1 l.117 ; SYNTHESE l.322) ; Jito Liquid Staking (Solana) entre a sa place.
- Limite majeure : ce que DefiLlama declare n'est pas verifie (section 7) ; le point d acces officiel par oracle (`/oracles`) est reserve a l offre payante : les tableaux par oracle sont **recalcules par moi** a partir des champs des protocoles.

## 2. Methode (rejouable)

1. [lu] Documentation lue : `https://api-docs.defillama.com/` (copie `raw/api-docs.html`) et `llms-free.txt`. Elle annonce l API gratuite `https://api.llama.fi` “No authentication required” et classe `/api/oracles` et `/api/hacks` dans la liste Pro. Constat du jour : `GET /oracles` repond **402** (“Upgrade to the paid API plan”) ; `GET /hacks` repond 200 sans cle (ecart avec la doc, signale).
2. Reponses brutes gardees (sha256 en section 8) : `/protocols` (9,07 Mo, {len(P)} entrees), `/lite/protocols2` (gardee, non exploitee), `/oracles` (le refus 402), `/hacks` (1 293 incidents), et `/protocol/{{slug}}` pour les 30 cibles (composition des actifs ; compresses en .gz).
3. Source des oracles : champ `oraclesBreakdown` (971 protocoles ; nom, role Primary/Secondary/Aggregator/Fallback, preuve, dates, chaines), sinon ancien champ `oracles` (242 protocoles, sans role : marque “champ ancien”). Un oracle dont `endDate` est passee ou `startDate` future n est pas compte. Si DefiLlama liste des chaines pour un oracle, la valeur de cet oracle est limitee a ces chaines, selon la regle suivante : toutes les entrees d un meme oracle pour un protocole sont reunies ; les noms de chaines sont compares sans tenir compte de la casse, avec l alias “bsc” = BNB Chain (ecrit a la main : DefiLlama ne publie pas de table d alias [abs]) ; une chaine presente avec une TVL nulle compte pour 0 ; la TVL totale du protocole n est reprise que si aucune chaine citee ne correspond a une chaine du protocole, et cette part est montree a part dans T2 : RedStone 1 256 M$ (Pendle V2, chaine citee “Redstone”, absente de ses TVL) et Pyth 88 M$ (Usual USD0, chaine citee “Arbitrum”, absente de ses TVL).
4. **Categories dependantes d un prix (A, ecrites avant de regarder les chiffres)** : Lending, CDP, Derivatives, Options, Options Vault, RWA, Leveraged Farming, Synthetics, Basis Trading, Algo-Stables, Partially Algorithmic Stablecoin, Dual-Token Stablecoin, Stablecoin Issuer, NFT Lending. **B** : toute autre categorie (curateurs, rendement, jeux d options, indices, staking liquide, marches de prediction...) des qu un oracle est declare. Exclus : CEX, Chain, Oracle (fournisseurs, pas clients), protocoles marques rugged, deprecated ou morts. **Mort = champ `deadFrom` renseigne**, ecrit tel quel dans les donnees de DefiLlama ; le champ `deadUrl` n est pas utilise, et 24 protocoles `deadUrl: true` restent dans le perimetre (declares en section 7, point 11).
5. **Tailles (seuils ecrits d avance, valeur deposee = champ `tvl` de DefiLlama, qui exclut les emprunts)** : Grande >= 1 Md$ ; Moyenne 50 M$ a 1 Md$ ; Petite 1 a 50 M$. Pourquoi : 1 Md$ isole la vingtaine de protocoles systemiques ; 50 M$ separe, a mon avis [inféré], ceux qui ont une equipe de risque dediee des petits ; sous 1 M$ la valeur securisee est trop faible pour un contrat (7 101 entrees de la liste sont sous 1 M$).
6. **Chaine principale** = chaine ou le protocole a le plus de TVL (champ `chainTvls`, hors `borrowed`, `staking`, `pool2`). “BNB Chain” = cle `Binance` ; “Hyperliquid” = cle `Hyperliquid L1` ([inféré] : c est la couche EVM). Hors des dix chaines demandees : “Autres” (detail T1d).
7. Liste courte : regle dans `cibles.json` (hors familles deja etudiees, un protocole par organisation, au moins deux oracles externes de preference, incident d oracle classe, etalement des chaines) ; choix final a la main. La composition des actifs vient de `/protocol/{{slug}}` (derniere ligne `tokensInUsd`, 2026-10-04) ; le regroupement BTC / ETH / USDC / USDT est fait **par symbole** [inféré] (BTC = tout symbole contenant BTC ; ETH = ETH et derives liquides courants).

## 3. Tableaux de synthese
""")
T=open(O('out/tables.md')).read()
T=T.replace('## T','### T')
L.append(T)
L.append("""
Lecture : T1a et T1b comptent les protocoles par chaine principale (un protocole = une case) ; T1c compte la TVL posee sur chaque chaine (un protocole multi-chaines y figure plusieurs fois). **Les TVL ne s additionnent pas entre couches** : curateurs, agregateurs de rendement et protocoles de base deposent les uns chez les autres (par ex. Steakhouse et Gauntlet au-dessus de Morpho) ; les totaux surestiment donc la valeur reellement exposee [inféré].
""")
# shortlist
names={'G':'Grandes (>= 1 Md$)','M':'Moyennes (50 M$ a 1 Md$)','P':'Petites (1 a 50 M$)'}
L.append('## 4. Liste courte de 30 cibles\n\nColonnes : chaines = toutes les chaines a 1 M$ ou plus, liste entiere ; TVL en M$ ; oracles tels que declares par DefiLlama [lu] avec leur role et les chaines indiquees ; panier = part du BTC, ETH, USDC, USDT dans les actifs deposes, par symbole [inféré] ; incidents = classes “Oracle Manipulation” par DefiLlama dans `/hacks` (champ `source` vide pour tous : cause non verifiee). La colonne “Pourquoi” est mon interpretation [inféré] sauf mention [lu]/[abs].\n')
i=0
for t in 'GMP':
    L.append(f'### {names[t]}\n\n| # | Protocole | Categorie | Chaines (M$, >= 1 M$) | TVL | Oracles declares (n) | Panier S2-bis | Incidents d oracle | Pourquoi |\n|---|---|---|---|---:|---|---|---|---|')
    for n in C[t]:
        i+=1; r=R[n]
        L.append(f"| {i} | {n} | {r['category']} | {chs(r)} | {M(r['tvl'])} | {oracs(r)} ({r['n']}) | {par(n)} | {inc(r)} | {W[n]} |")
    L.append('')
cc=collections.Counter(R[n]['primary'] for t in 'GMP' for n in C[t])
L.append('Repartition par chaine principale : '+', '.join(f'{k} {v}' for k,v in cc.most_common())+f'. Soit {len(cc)} chaines.\n')
L.append("""Reserve (non retenus, meme profil) : Sky Lending (CDP, 5 919 M$, Chronicle + Internal ; sorti de la liste courte par la correction C-7 : son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” — P1 l.117, SYNTHESE l.322 [lu] — donc la cible n est pas une organisation nouvelle ; DefiLlama le range sous un autre parent, parent#maker, que SparkLend, parent#spark), Jupiter Perps (820 M$, meme equipe que Jupiter Lend ; Chainlink + Chaos + Pyth, preuve fournie par DefiLlama), Fluid (714 M$, Chainlink seul), Bonzo Lend (Hedera, 5,4 M$, Chainlink + Supra ; incident classe 2026-07-11, 9,05 M$), Angle (1,8 M$, trois fournisseurs externes — Chainlink, RedStone, Pyth — et un TWAP, tous dans l ancien champ), Neverland (Monad, 8,4 M$, Chainlink + RedStone).

Cas particuliers a ne pas confondre : (a) Steakhouse, Gauntlet : couches de curation, TVL en partie comptee ailleurs ; (b) Ethena USDe : aucun oracle declare [abs] ; (c) JustLend et USDD : dependance unique, sans question de racines communes ; (d) Dolomite : aucun oracle declare pour Ethereum, ou se trouvent 329 M$ sur 360 [lu].
""")
L.append("""## 5. Ce que la carte dit des clients possibles [inféré]

- Le terrain des racines communes est etroit en valeur mais large en nombre : 73 protocoles ont au moins 2 oracles externes declares (48 petits, 18 moyens, 7 grands) ; 76 en ont au moins 2 en comptant les sources internes. Par chaine principale (les 76) : hors liste 26, Ethereum 19, BNB Chain 8, Solana 6, Base 4, Sui 4, Hyperliquid 3, Arbitrum 3, Aptos 2, Avalanche 1, Tron 0.
- Parmi les grandes declarees, la plupart sont en dependance unique ou interne (Maple, USDD, Jupiter Lend, JustLend, Pendle, Jito Liquid Staking) ou en couple (Sky Lending : Chronicle + interne, hors liste courte). Sept grands protocoles declarent au moins 2 oracles externes ; **quatre sont des familles deja etudiees** (SparkLend, Compound V3, Venus Core Pool, Kamino Lend). Hors familles deja etudiees, les grands multi-oracles sont les curateurs (Steakhouse, Gauntlet) et Lista.
- Arbitrum, Sui, Aptos, Avalanche et Hyperliquid n ont aucun protocole de plus de 1 Md$ comme chaine principale ; Tron en a deux (JustLend, USDD), a source unique ou interne (T1a).
- Chiffres a ne pas surinterpreter : l absence d oracle declare (42 % du perimetre) est un manque de documentation DefiLlama, pas une preuve d absence d oracle.

## 6. Pistes pour la suite (aucune action prise)

- Verifier par la documentation propre de chaque cible (lecture de pages officielles) les oracles declares avant tout contact : surtout Dolomite (Ethereum), Ethena, Pendle.
- Lire les post-mortems des incidents “Oracle Manipulation” de la liste (champ source vide chez DefiLlama) avant de les citer.
- Cette carte a ete relue par un reviseur different (G2, verdict ACCEPTE-AVEC-CORRECTIONS) ; les corrections sont appliquees (section 9) et restent a faire controler (reviseur ou controle de transcription de l orchestrateur).
""")
L.append(f"""## 7. Limites

1. **Declaratif non verifie** : tous les oracles, roles et dates viennent de DefiLlama (preuves en liens, non ouvertes par moi). Je n ai lu aucune documentation de protocole.
2. **Couverture partielle** : 971 protocoles sur {len(P)} ont `oraclesBreakdown` et 242 l ancien champ ; 42 % du perimetre n a rien [abs]. Les protocoles a champ ancien n ont ni role ni preuve.
3. **Oracles par chaine** : quand DefiLlama liste des chaines, la chaine principale peut rester sans oracle declare (Dolomite sur Ethereum).
4. **TVL** : valeur deposee declaree par DefiLlama, hors emprunts, hors staking ; peut compter deux fois la meme valeur entre couches ; peut etre mal evaluee (champ `misrepresentedTokens` non filtre). Pas de verification sur chaine.
5. **Tableau par oracle recalcule par moi** : l endpoint officiel `/oracles` est payant (402) ; les lignes ne sont pas additives (un protocole a plusieurs oracles est compte dans chacun) ; les valeurs suivent la regle de la section 2.3. Seules les deux parts de repli montrees a part dans T2 sont des bornes hautes : RedStone 1 256 M$ (Pendle V2) et Pyth 88 M$ (Usual USD0). La version precedente de la piece sous-evaluait Chainlink de 1,3 Md$ et surevaluait Chaos, RedStone et DIA (section 9, C-1).
6. **Classification des chaines** : chaine principale = plus forte TVL ; les noms de chaines suivent DefiLlama (“Binance”, “Hyperliquid L1”).
7. **Incidents** : `/hacks` classe “Oracle Manipulation” dont la grande majorite en “Spot Price Manipulation” (prix de pool), ce qui ne designe pas une faute d un fournisseur comme Chainlink ou Pyth. Champ `source` vide pour tous les incidents du fichier : non verifiables ici. Lecture des incidents limitee aux liens par `defillamaId` ou parent. La colonne “Incidents d oracle” ne montre que les incidents classes oracle ; les incidents d un autre type, lies par identifiant ou par parent, sont cites dans la colonne “Pourquoi” (GMX, NAVI, Usual USD0, Ostium, Scallop).
8. **Panier S2-bis** : regroupement par symbole, approximatif (par ex. un symbole ETH sur Tron). Symboles non classes qui changent la lecture : Gearbox, `SAVETH` (37,7 %) et `WMOOCURVEETH+-WETH` (16,2 %) ne sont pas comptes en ETH alors que la ligne dit ETH 20 % (l identite de `SAVETH` n est pas etablie [abs]) ; `AVALANCHEUSDC` n est pas compte en USDC (GMX : 43 % au lieu de 41 % ; Benqi : 3 % au lieu de 0 %). Le panier de Jito Liquid Staking (SOL 100 %) vient d un detail telecharge apres les 29 autres, le meme jour (2026-10-04, 21:11 UTC).
9. **Hors perimetre** : aucune donnee sur les montants empruntes, les liquidations, ni sur le prix reel paye pour un oracle ; aucune verification de l appetit commercial.
10. Donnees vivantes : elles changent chaque jour ; la lecture date du 2026-10-04.
11. **Definition de mort et protocoles `deadUrl`** : la regle ecrite d avance retient `deadFrom` renseigne, tel quel. Le sens des champs `deadUrl` et `deadFrom` n est pas documente dans les copies de la documentation lues [abs]. **24 protocoles a `deadUrl: true` restent dans le perimetre** : {B['deadurl']['tvl_m']} M$ de TVL (0,4 % des 93 313 M$), {B['deadurl']['nA']} en A et {B['deadurl']['nB']} en B, {B['deadurl']['decl']} avec un oracle declare ({B['deadurl']['decl_tvl_m']} M$) ; les plus grands : RealT Tokens 155 M$, AZverse Perps 52 M$, Alpaca Leveraged Yield Farming 37 M$, RealT RMM Marketplace V2 29 M$. Aucun n est parmi les 30 cibles [calc]. Pas de recomptage : les chiffres des tables incluent ces 24 protocoles.
12. **Usages d oracle sans lien avec un prix** : DefiLlama ne type l usage d une entree d oracle que pour 9 entrees sur 1 201 (`RNG` 7, `PoR` 2) [lu]. Dans le perimetre : Re (RWA, 398 M$) a pour seul oracle Chainlink de type `PoR` (preuve de reserves) ; il est compte comme ayant un oracle declare, et chez Chainlink comme seul oracle ; PoolTogether V5 (Yield Lottery, 2,4 M$) a pour seul oracle Witnet de type `RNG` (aleatoire), seule raison de son entree en B. Cas sans type, d apres mon raisonnement [inféré] : Polymarket International (UMA, 368 M$) et Across (UMA, 21 M$) resolvent des evenements ou des relais, pas un prix ; PoolTogether V3 (Chainlink, 5,0 M$) sert a un tirage au sort. Ils restent comptes. **Chiffres indicatifs** sans les deux entrees typees `RNG`/`PoR` [calc, `out/biais.json`] : B {B['sans_rng_por']['nB']}, A+B {B['sans_rng_por']['n']}, {B['sans_rng_por']['decl']} avec oracle declare ({format(B['sans_rng_por']['decl_tvl_m'],',').replace(',',' ')} M$), Chainlink {B['sans_rng_por']['chainlink']} protocoles, ligne Witnet supprimee. La part du perimetre qui depend reellement d un prix n est pas etablie [abs].
13. **T4 : des paires, pas des combinaisons** : T4 compte les protocoles qui declarent deux oracles donnes (paires co-declarees, non additives) ; la colonne “exactement ces deux oracles” donne les protocoles qui n en declarent pas d autres.
14. **T1d partielle** : T1d ne montre que les 15 premieres des 67 chaines de la ligne Autres (52 des 136 protocoles).

## 8. Fichiers, versement et empreintes

**Versement prevu** : `docs/adr-0029/etude-marche/carto/`, comme piece de contexte commercial non normative d ADR-0029. Fichiers verses :
- la piece `CARTO-DEFI-ORACLES.md` ;
- les scripts `traite.py`, `enrichit.py`, `assemble.py`, `fetch_detail.sh` ;
- les entrees de choix `cibles.json` et `pourquoi.json` ;
- `out/perimetre.csv` (424 lignes, sha256 `{sha('out/perimetre.csv')}`) : liste “pour chacun” du perimetre (identifiant, nom, parent, categorie, perimetre A ou B, TVL, taille, chaine principale, TVL par chaine, oracles actifs avec role et chaines, source des oracles, nombres d oracles et d oracles externes, famille deja etudiee, nombre d incidents d oracle classes) ;
- `SHA256SUMS` (empreintes de tous les fichiers de la carte, `raw/` compris).

**`raw/` reste hors depot** : seules ses empreintes sont versees (`SHA256SUMS`). Les reponses changent chaque jour ; une relecture ne peut donc rejouer la chaine que sur une copie de `raw/` conservee ailleurs.

**Ordre de rejeu** (chaque etape lit la sortie de la precedente) :
1. `python3 traite.py` (hors reseau ; lit `raw/protocols.json` et `raw/hacks.json` ; ecrit `out/rows.json`, `out/perimetre.csv`, `out/tables.md`, `out/biais.json`) ;
2. `bash fetch_detail.sh` (reseau ; lit `out/rows.json` et `cibles.json` ; ecrit `raw/detail/{{slug}}.json`) ;
3. `gzip -n raw/detail/*.json` : **la compression n est pas scriptee** ; `enrichit.py` lit `{{slug}}.json.gz` avant `{{slug}}.json`, donc un `.json.gz` ancien l emporte sur un `.json` frais (supprimer les `.gz` perimes avant de rejouer) ;
4. `python3 enrichit.py` (hors reseau ; ecrit `out/cibles-actifs.json`) ;
5. `python3 assemble.py` (hors reseau ; ecrit cette piece).
Hors reseau, avec `raw/` et `raw/detail/` deja presents : etapes 1, 4 et 5. Le detail `raw/detail/jito-liquid-staking.json.gz` a ete telecharge seul par l orchestrateur (2026-10-04 21:11 UTC, HTTP 200, `gzip -n`), apres la passe de corrections ; meme jour que les 29 autres lignes.

Empreintes des reponses brutes (sha256) : voir `SHA256SUMS`. Principales :
""")
for f in ['raw/protocols.json','raw/lite_protocols2.json','raw/oracles.json','raw/hacks.json','raw/api-docs.html','raw/llms-free.txt']:
    L.append(f'- `{f}` `{sha(f)}`')
L.append('')
L.append(f"""
## 9. Corrections G2 appliquees (relecture `g2/G2-CARTO.md`, section 7, C-1 a C-13)

Adjudications de l orchestrateur appliquees la ou la G2 laissait un choix (brief des corrections). Passe : 2026-10-04, `date -u` 21:02 a 21:11 UTC, sans reseau.

- **C-1 (T2, valeur declaree)** : appliquee. `traite.py` corrige sur les quatre points : toutes les entrees d un meme oracle sont reunies (Venus ne perd plus son entree `@Binance`) ; chaines comparees sans casse, alias “bsc” = BNB Chain ; une chaine presente a TVL nulle compte pour 0 (Steakhouse n est plus compte en entier chez Chaos et RedStone, River chez DIA) ; repli sur la TVL totale seulement sans correspondance, montre a part (nouvelle colonne de T2). Resultat : Chainlink 46 060 ; Chronicle 11 856 ; Internal 11 180 ; RedStone 11 084 dont 1 256 de repli ; Pyth 5 947 dont 88 de repli ; Atlas 2 576 ; Switchboard 1 483 ; Binance Oracle 1 133 ; Chaos 828 ; eOracle 241 ; DIA 117 ; egal a `g2/sortie-t2-attendu.txt` sur les 18 lignes (comparaison par script, 0 ecart) ; les autres lignes de T2 inchangees. Textes corriges : §1 (44,7 devient 46,1 Md$), §2.3 (le montant du repli), §7.5 (bornes hautes limitees aux deux parts de repli ; Chainlink etait sous-evalue). Le reste de la chaine est inchange : `out/perimetre.csv` garde le meme sha256.
- **C-2 (definition de mort)** : appliquee, sans recomptage. Mort = champ `deadFrom` renseigne (§1, §2.4, T0). Declare en §7 point 11 : 24 protocoles `deadUrl` restes dans le perimetre, 353 M$, 20 en A et 4 en B, 15 avec un oracle declare, aucun parmi les cibles (verifie par l assemblage).
- **C-3 (usages sans lien avec un prix)** : appliquee. Comptes inchanges ; cas Re (`PoR`), PoolTogether V5 (`RNG`), PoolTogether V3, Polymarket International et Across (UMA, [inféré]) declares en §7 point 12, avec les chiffres sans `RNG`/`PoR` a titre indicatif (B 78, A+B 423, 244 declares, 67 349 M$, Chainlink 128, ligne Witnet supprimee ; retrouves par mon propre script, `out/biais.json`). §1 reformule : “dependent d un prix ou declarent un oracle”.
- **C-4 (T4)** : appliquee. T4 retitre en paires co-declarees non additives, avec la colonne “exactement ces deux oracles” (Chainlink et RedStone : 28 dont 8, 185 M$ ; Chainlink et Pyth : 17 dont 9) ; §1 puce 3 et §7 point 13 corriges.
- **C-5 (grands multi-oracles)** : appliquee. §5 puce 2 : sur les 7 grands a au moins 2 oracles externes, 4 sont SparkLend, Compound V3, Venus Core Pool et Kamino Lend ; Steakhouse, Gauntlet et Lista le sont hors familles deja etudiees.
- **C-6 et C-7 (liste courte G, Sky)** : appliquees. Sky Lending sort de la liste (son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” : dit dans la reserve et en §1) ; Jito Liquid Staking entre a sa place (Solana, Switchboard seul declare, B) avec sa ligne ; Ethereum tombe a 3 cibles G ; repartition par chaine recalculee ({', '.join(f'{k} {v}' for k,v in cc.most_common())}). **Ecart motive** : le panier de Jito n est pas calcule (detail `/protocol/jito-liquid-staking` absent de `raw/detail/`, reseau interdit par le brief) ; la ligne le disait [abs] et la limite a ete rendue a l orchestrateur, qui a telecharge le detail le meme jour (2026-10-04 21:11 UTC) et rejoue enrichit puis assemble : panier SOL 100 %.
- **C-8 (Gauntlet)** : appliquee. SYNTHESE cite Gauntlet comme comparable de prix (§1.10 l.359, C20 l.463) ; ses cabinets de risque sont Chaos Labs et LlamaRisk (l.322).
- **C-9 (incidents)** : appliquee. Ostium (“Private Key Compromised”, 23,75 M$, 2026-07-15) et Scallop (“Reward Logic Flaw”, 0,142 M$, 2026-04-26) attribues a DefiLlama, source vide ; Moonwell : reserve de la ligne Rhea ajoutee, incident du 2025-11-04 sur Base et Optimism ; incidents non oracle ajoutes pour GMX (parent GMX V1), NAVI et Usual USD0. Precision : l incident cite pour NAVI est une entree Volo Vault (id 3711) dont le champ parent est `parent#navi-protocol`.
- **C-10 (registre 09)** : appliquee. Trois formulations de la version precedente reecrites : JustLend (l.246), GMX (l.259), River (l.258). JustLend et GMX parlent maintenant d une relation mesuree entre l oracle declare et d autres sources, sans juger la valeur de l une ; River : cinq fournisseurs declares, le nombre le plus eleve du perimetre, a egalite avec Re7 Labs et ZeroLend Lending (declare, non mesure ; verifie par `out/biais.json`). Citations web entre “”, aucun guillemet francais ; relecture de la piece contre les entrees du registre.
- **C-11 (paniers)** : appliquee. Ethena : USDe 97,3 %, USDtb 1,4 %, USDC 1,3 % ; Benqi : BTC 5,5 % dont BTC.b 3,7 % et WBTC.e 1,9 % ; JustLend : BTC 15 (14,53 %) dans le tableau, par arrondi a deux decimales dans `enrichit.py` (le double arrondi disparait) ; Gearbox : USDC 4 % ; symboles non classes nommes en §7.8 ; Angle : trois fournisseurs externes et un TWAP, ancien champ.
- **C-12 (libelles)** : appliquee. “Par categorie du perimetre A+B (categories B marquees (B))” ; T1d : 15 premieres des 67 chaines (52 des 136 protocoles) ; colonne des chaines des cibles : **liste entiere** a 1 M$ ou plus, sans coupure.
- **C-13 (versement)** : appliquee. Section 8 : chemins de versement `docs/adr-0029/etude-marche/carto/`, `raw/` hors depot (empreintes seules), `out/perimetre.csv` verse et cite avec son sha256, ordre de rejeu corrige (traite, fetch_detail, gzip -n, enrichit, assemble), compression non scriptee et priorite du `.json.gz` signalees ; ligne d exposition en tete de piece. **Ecart motive** : l attestation de la passe initiale n est pas reconstituable par la passe de corrections ; elle est limitee a ce que la piece cite et reste a confirmer par le controle de transcription.
- **Hors liste** : la docstring de `traite.py` n annonce plus un `out/shortlist.json` qu il ne produit pas (O-8) ; accents (O-1), unification “valeur securisee”/“valeur declaree” (O-7) et vivier M (O-5) non traites.
""")
open(O('CARTO-DEFI-ORACLES.md'),'w').write('\n'.join(L))
print(len('\n'.join(L)))
