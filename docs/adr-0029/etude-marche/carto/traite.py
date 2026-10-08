#!/usr/bin/env python3
"""Traitement rejouable : raw/protocols.json + raw/hacks.json -> out/perimetre.csv, out/rows.json, out/tables.md, out/biais.json.
Usage : python3 traite.py   (aucun reseau ; lit seulement raw/). Date de reference lue sur l'horloge (NOW) ou RAW_DATE."""
import json, csv, os, sys, collections, datetime, re
HERE=os.path.dirname(os.path.abspath(__file__))
RAW=os.path.join(HERE,'raw'); OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
TODAY=datetime.date.fromisoformat(os.environ.get('RAW_DATE','2026-10-04'))
P=json.load(open(f'{RAW}/protocols.json')); H=json.load(open(f'{RAW}/hacks.json'))

CORE={'Lending','CDP','Derivatives','Options','Options Vault','RWA','Leveraged Farming','Synthetics','Basis Trading',
 'Algo-Stables','Partially Algorithmic Stablecoin','Dual-Token Stablecoin','Stablecoin Issuer','NFT Lending'}
EXCL_ALWAYS={'CEX','Chain','Oracle'}
TIERS=[('G','Grande (>= 1 Md$)',1e9,float('inf')),('M','Moyenne (50 M$ a 1 Md$)',5e7,1e9),('P','Petite (1 a 50 M$)',1e6,5e7)]
MAINCH=['Ethereum','Solana','Base','Arbitrum','BNB Chain','Sui','Aptos','Avalanche','Hyperliquid','Tron']
CHMAP={'Binance':'BNB Chain','Hyperliquid L1':'Hyperliquid'}
ONAME={'API3':'Api3','Umbrella Network':'Umbrella','Uniswap V3':'Uniswap','Uniswap':'Uniswap'}
INTERNAL={'TWAP','Internal','Uniswap','Curve','PulseX','Balancer Pool LP token','Coingecko','Coinmarketcap'}
STUDIED={'parent#aave','parent#spark','parent#morpho','parent#euler','parent#compound-finance','parent#kamino-finance','parent#venus-finance'}
def chname(k): return CHMAP.get(k,k)
def tier(v):
    for c,_,lo,hi in TIERS:
        if lo<=v<hi: return c
    return None
def plain_chains(p):
    return {chname(k):v for k,v in p['chainTvls'].items() if '-' not in k and k not in('borrowed','staking','pool2') and v}
def pd(s):
    try: return datetime.date.fromisoformat(s)
    except Exception: return None
def active_oracles(p,skip=()):
    """-> (liste de (nom, type, chains|None), source) ; source in breakdown/legacy/none/ended"""
    b=p.get('oraclesBreakdown') or []
    if b:
        out=[]
        for o in b:
            sd,ed=pd(o.get('startDate') or ''),pd(o.get('endDate') or '')
            if sd and sd>TODAY: continue
            if ed and ed<=TODAY: continue
            if o.get('type') in skip: continue
            n=ONAME.get(o['name'],o['name'])
            out.append((n,o.get('type'),[chname(c['chain'] if isinstance(c,dict) else c) for c in o['chains']] if o.get('chains') else None))
        return (out,'breakdown') if out else ([],'ended')
    l=p.get('oracles') or []
    if l: return ([(ONAME.get(n,n),'legacy',None) for n in l],'legacy')
    return ([],'none')
ALIAS={'bsc':'bnb chain'}   # alias ecrit a la main (les noms de chaines des entrees d oracle ne sont pas normalises par DefiLlama)
def chains_all(p):
    """chaines de chainTvls, hors borrowed/staking/pool2 et cles composees, ZERO CONSERVE (une chaine presente a TVL nulle vaut 0)."""
    return {chname(k):(v or 0) for k,v in p['chainTvls'].items() if '-' not in k and k not in('borrowed','staking','pool2')}
def oracle_value(p,ents):
    """Regle 2.3, toutes les entrees d un meme oracle pour un protocole. -> (valeur, repli:bool)
    - une entree sans chaine : TVL totale ; - sinon union des chaines citees, comparees sans casse (alias bsc -> BNB Chain),
    somme des TVL des chaines correspondantes (meme nulles) ; - aucune chaine ne correspond : TVL totale, comptee a part (repli)."""
    tvl=p.get('tvl') or 0
    if any(not oc for _,_,oc in ents): return tvl,False
    vues={ALIAS.get(c.lower(),c.lower()) for _,_,oc in ents for c in oc}
    ct=chains_all(p); corr=[c for c in ct if c.lower() in vues]
    if not corr: return tvl,True
    return sum(ct[c] for c in corr),False
hack_by_id=collections.defaultdict(list)
for h in H:
    t=(h.get('technique') or '')+' '+(h.get('classification') or '')
    if 'racle' in t and h.get('defillamaId'): hack_by_id[str(h['defillamaId'])].append(h)
    if 'racle' in t and h.get('parentProtocolId') and not h.get('defillamaId'): hack_by_id['P:'+h['parentProtocolId']].append(h)
hack_by_parent=collections.defaultdict(list)
byid={p['id']:p for p in P}
for i,hs in hack_by_id.items():
    if i in byid and byid[i].get('parentProtocol'): hack_by_parent[byid[i]['parentProtocol']]+=hs

oracle_providers=[]
def build(skip=()):
    rows=[]
    for p in P:
        cat=p.get('category')
        if cat=='Oracle': 
            if (p['tvl'] or 0)>0 and not skip: oracle_providers.append(p)
            continue
        if cat in EXCL_ALWAYS: continue
        if p.get('rugged') or p.get('deprecated') or p.get('deadFrom'): continue
        tvl=p.get('tvl') or 0
        if tvl<1e6: continue
        ors,src=active_oracles(p,skip)
        scope='A' if cat in CORE else ('B' if ors else None)
        if not scope: continue
        chs=plain_chains(p)
        primary=max(chs,key=chs.get) if chs else (chname(p.get('chain') or 'inconnue'))
        pc=primary if primary in MAINCH else 'Autres'
        names=sorted({o[0] for o in ors}); ext=[n for n in names if n not in INTERNAL]
        rows.append(dict(id=p['id'],name=p['name'],slug=p['slug'],parent=p.get('parentProtocol') or '',category=cat,scope=scope,
            tvl=tvl,tier=tier(tvl),chains=chs,primary=primary,pchain=pc,oracles=ors,osrc=src,onames=names,n=len(names),next=len(ext),
            deadUrl=bool(p.get('deadUrl')),misrep=bool(p.get('misrepresentedTokens')),url=p.get('url') or '',
            hacks=[h for h in hack_by_id.get(p['id'],[])]+(hack_by_id.get('P:'+(p.get('parentProtocol') or '-'),[])),studied=(p.get('parentProtocol') in STUDIED or p['slug'] in('compound-blue',))))
    return rows
rows=build()
with open(f'{OUT}/perimetre.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow('id name slug parent category scope tvl_usd taille chaine_principale chaines_tvl oracles_actifs source_oracles n_oracles n_externes deja_etudie incidents_oracle_defillama'.split())
    for r in sorted(rows,key=lambda r:-r['tvl']):
        w.writerow([r['id'],r['name'],r['slug'],r['parent'],r['category'],r['scope'],round(r['tvl']),r['tier'],r['primary'],
          ';'.join(f'{c}={round(v)}' for c,v in sorted(r['chains'].items(),key=lambda x:-x[1])[:6]),
          ';'.join(f"{o[0]}{'('+o[1]+')' if o[1] else ''}"+('@'+'/'.join(o[2]) if o[2] else '') for o in r['oracles']),
          r['osrc'],r['n'],r['next'],int(r['studied']),len(r['hacks'])])
M=lambda v:f'{v/1e6:,.0f}'.replace(',',' ')
def Md(v): return f'{v/1e9:,.2f}'
out=[]
# --- couverture
out.append('## T0. Perimetre et couverture de la declaration des oracles\n')
out.append('| Perimetre (TVL >= 1 M$, hors rugged/deprecated/mort = champ `deadFrom` renseigne) | Protocoles | TVL (M$) | avec oracle declare | % protocoles | TVL declaree (M$) | % TVL |\n|---|---:|---:|---:|---:|---:|---:|')
for lab,sel in [('A. categories dependantes d un prix (liste ecrite d avance)',lambda r:r['scope']=='A'),('B. autres categories avec oracle declare',lambda r:r['scope']=='B'),('A+B',lambda r:True)]:
    s=[r for r in rows if sel(r)]; d=[r for r in s if r['n']]
    out.append(f"| {lab} | {len(s)} | {M(sum(r['tvl'] for r in s))} | {len(d)} | {100*len(d)/max(1,len(s)):.0f} % | {M(sum(r['tvl'] for r in d))} | {100*sum(r['tvl'] for r in d)/max(1,sum(r['tvl'] for r in s)):.0f} % |")
out.append('\nPar categorie du perimetre A+B (protocoles >= 1 M$ ; categories B marquees (B)) :\n\n| Categorie | Protocoles | TVL (M$) | oracle declare (nb) | TVL declaree (M$) |\n|---|---:|---:|---:|---:|')
cc=collections.defaultdict(list)
for r in rows: cc[r['category']+(' (B)' if r['scope']=='B' else '')].append(r)
for k,s in sorted(cc.items(),key=lambda kv:-sum(r['tvl'] for r in kv[1])):
    d=[r for r in s if r['n']]; out.append(f"| {k} | {len(s)} | {M(sum(r['tvl'] for r in s))} | {len(d)} | {M(sum(r['tvl'] for r in d))} |")
out.append('')
# --- chaine x taille (chaine principale)
for lab,sel in [('T1a. Chaine principale x taille — perimetre A+B (nombre de protocoles ; TVL en M$ entre parentheses)',lambda r:True),
                ('T1b. Idem, seulement protocoles avec oracle declare',lambda r:r['n']>0)]:
    out.append(f'## {lab}\n\n| Chaine principale | Grande | Moyenne | Petite | Total |\n|---|---:|---:|---:|---:|')
    for ch in MAINCH+['Autres']:
        cells=[];tot=[0,0]
        for t,_,_,_ in TIERS:
            s=[r for r in rows if sel(r) and r['pchain']==ch and r['tier']==t]
            cells.append(f"{len(s)} ({M(sum(r['tvl'] for r in s))})"); tot[0]+=len(s); tot[1]+=sum(r['tvl'] for r in s)
        out.append(f"| {ch} | "+' | '.join(cells)+f" | {tot[0]} ({M(tot[1])}) |")
    s=[r for r in rows if sel(r)]
    out.append('| **Total** | '+' | '.join(f"{len([r for r in s if r['tier']==t])} ({M(sum(r['tvl'] for r in s if r['tier']==t))})" for t,_,_,_ in TIERS)+f" | {len(s)} ({M(sum(r['tvl'] for r in s))}) |\n")
# --- presence par chaine (TVL sur la chaine)
out.append('## T1c. Presence par chaine (TVL posee sur la chaine, tous protocoles A+B ; un protocole multi-chaines compte sur chacune)\n\n| Chaine | Protocoles presents (>= 1 M$ sur la chaine) | TVL sur la chaine (M$) | dont avec oracle declare (M$) |\n|---|---:|---:|---:|')
for ch in MAINCH+['Autres']:
    n=0;t=0;td=0
    for r in rows:
        for c,v in r['chains'].items():
            cc_=c if c in MAINCH else 'Autres'
            if cc_==ch:
                t+=v; td+=v if r['n'] else 0; n+= 1 if v>=1e6 else 0
    out.append(f'| {ch} | {n} | {M(t)} | {M(td)} |')
out.append('')
ac=collections.defaultdict(list)
for r in rows:
    if r['pchain']=='Autres': ac[r['primary']].append(r)
_top=sorted(ac.items(),key=lambda kv:-sum(r['tvl'] for r in kv[1]))[:15]
_nt=sum(len(s_) for _,s_ in _top); _na=sum(len(s_) for s_ in ac.values())
out.append(f'## T1d. Detail de la ligne Autres (chaine principale, A+B) : {len(_top)} premieres des {len(ac)} chaines ({_nt} des {_na} protocoles de la ligne Autres)\n\n| Chaine | Protocoles | TVL (M$) |\n|---|---:|---:|')
for k,s_ in sorted(ac.items(),key=lambda kv:-sum(r['tvl'] for r in kv[1]))[:15]: out.append(f"| {k} | {len(s_)} | {M(sum(r['tvl'] for r in s_))} |")
out.append('')
# --- par oracle
orc=collections.defaultdict(lambda:dict(ids=set(),val=0,repli=0,repli_l=[],multi=set(),single=set(),t=collections.Counter(),ch=collections.Counter()))
for r in rows:
    p=byid[r['id']]; grp=collections.defaultdict(list)
    for e in r['oracles']: grp[e[0]].append(e)          # TOUTES les entrees d un meme oracle
    for n,ents in grp.items():
        o=orc[n]; o['ids'].add(r['id']); v,rep_=oracle_value(p,ents); o['val']+=v
        if rep_: o['repli']+=v; o['repli_l'].append((r['name'],round(v/1e6),sorted({c for _,_,oc in ents for c in oc})))
        (o['multi'] if r['n']>1 else o['single']).add(r['id']); o['t'][r['tier']]+=1; o['ch'][r['pchain']]+=1
out.append('## T2. Par oracle declare (perimetre A+B, TVL >= 1 M$ ; valeur = somme des TVL des protocoles qui le declarent, limitee aux chaines indiquees quand DefiLlama les donne ; un protocole a plusieurs oracles est compte pour chacun : NE PAS additionner les lignes)\n')
out.append('| Oracle | Protocoles | Valeur declaree (M$) | dont repli sur la TVL totale (M$) | Seul oracle | Un parmi plusieurs | Grandes | Moyennes | Petites | Chaines principales (top 3) |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---|')
for n,o in sorted(orc.items(),key=lambda kv:-kv[1]['val']):
    out.append(f"| {n} | {len(o['ids'])} | {M(o['val'])} | {M(o['repli']) if o['repli'] else 0} | {len(o['single'])} | {len(o['multi'])} | {o['t']['G']} | {o['t']['M']} | {o['t']['P']} | "+', '.join(f'{c} {k}' for c,k in o['ch'].most_common(3))+' |')
out.append('\nRepli sur la TVL totale (aucune chaine citee par DefiLlama ne correspond a une chaine de TVL du protocole), montre a part : '+'; '.join(f"{n} {M(o['repli'])} M$ ({', '.join(f'{x[0]}, chaine citee {chr(8220)}'+'/'.join(x[2])+chr(8221) for x in o['repli_l'])})" for n,o in orc.items() if o['repli'])+'. Pour toutes les autres lignes la valeur est la somme des TVL des chaines correspondantes (casse ignoree, alias bsc = BNB Chain, chaine a TVL nulle = 0).')
d=[r for r in rows if r['n']]
cn=collections.Counter(r['n'] for r in d)
out.append('\n## T3. Nombre d oracles actifs declares par protocole (perimetre A+B declare)\n\n| Nb d oracles | Protocoles | TVL (M$) |\n|---|---:|---:|')
for k in sorted(cn): out.append(f"| {k} | {cn[k]} | {M(sum(r['tvl'] for r in d if r['n']==k))} |")
ce=collections.Counter(r['next'] for r in d)
out.append('\nNb d oracles **externes** (hors TWAP, Internal, Uniswap, Curve, PulseX, LP-token, Coingecko, Coinmarketcap) :\n\n| Nb externes | Protocoles | TVL (M$) |\n|---|---:|---:|')
for k in sorted(ce): out.append(f"| {k} | {ce[k]} | {M(sum(r['tvl'] for r in d if r['next']==k))} |")
pairs=collections.Counter(); pv=collections.Counter(); pex=collections.Counter(); pexv=collections.Counter()
for r in d:
    ns=[n for n in r['onames']]
    for i in range(len(ns)):
        for j in range(i+1,len(ns)):
            k_=(ns[i],ns[j]); pairs[k_]+=1; pv[k_]+=r['tvl']
            if len(ns)==2: pex[k_]+=1; pexv[k_]+=r['tvl']
out.append('\n## T4. Paires d oracles co-declarees les plus frequentes (NON additives ; ce ne sont pas des combinaisons : un protocole a trois oracles figure dans trois paires)\n\n| Paire | Protocoles qui declarent les deux | TVL cumulee (M$) | dont protocoles qui declarent exactement ces deux oracles | TVL de ceux-la (M$) |\n|---|---:|---:|---:|---:|')
for k,v in pairs.most_common(15): out.append(f"| {k[0]} + {k[1]} | {v} | {M(pv[k])} | {pex[k]} | {M(pexv[k])} |")
# --- prestataires d oracle (cat Oracle)
out.append('\n## T5. Fournisseurs listes par DefiLlama en categorie Oracle (TVL > 0 ; ce sont des fournisseurs, pas des clients)\n\n| Nom | TVL (M$) | Chaines |\n|---|---:|---|')
for p in sorted(oracle_providers,key=lambda p:-p['tvl'])[:15]: out.append(f"| {p['name']} | {M(p['tvl'])} | {', '.join(list(p['chains'])[:5])} |")
open(f'{OUT}/tables.md','w').write('\n'.join(out)+'\n')
# --- candidats
def key(r): return r
json.dump([{k:v for k,v in r.items()} for r in rows],open(f'{OUT}/rows.json','w'),default=str)
# --- chiffres des biais declares (C-2, C-3, C-5) -> out/biais.json
def agg(rs):
    dd=[r for r in rs if r['n']]
    return dict(n=len(rs),tvl_m=round(sum(r['tvl'] for r in rs)/1e6),decl=len(dd),decl_tvl_m=round(sum(r['tvl'] for r in dd)/1e6))
du=[r for r in rows if r['deadUrl']]
alt=build(skip=('RNG','PoR'))
named=lambda nm:[r for r in rows if r['name']==nm][0]
typed=[]
for r in rows:
    for o in r['oracles']:
        if o[1] in('RNG','PoR'): typed.append(dict(name=r['name'],cat=r['category'],scope=r['scope'],tvl_m=round(r['tvl']/1e6,1),oracle=o[0],type=o[1]))
big_multi=[dict(name=r['name'],studied=r['studied'],next=r['next'],tvl_m=round(r['tvl']/1e6)) for r in rows if r['tier']=='G' and r['next']>=2]
pool=[r for r in rows if r['tier']=='G' and not r['studied']]
json.dump(dict(base=agg(rows),
  deadurl=dict(**agg(du),nA=sum(r['scope']=='A' for r in du),nB=sum(r['scope']=='B' for r in du),names=[(r['name'],round(r['tvl']/1e6)) for r in sorted(du,key=lambda r:-r['tvl'])[:6]]),
  sans_rng_por=dict(**agg(alt),nA=sum(r['scope']=='A' for r in alt),nB=sum(r['scope']=='B' for r in alt),chainlink=sum('Chainlink' in r['onames'] for r in alt),witnet=sum('Witnet' in r['onames'] for r in alt),chainlink_base=sum('Chainlink' in r['onames'] for r in rows)),
  typed=typed,
  non_type=[dict(name=n,cat=named(n)['category'],tvl_m=round(named(n)['tvl']/1e6,1),oracles=named(n)['onames']) for n in ('Polymarket International','Across','PoolTogether V3')],
  grands_multi=big_multi,
  vivier_G=dict(n=len(pool),hors_ethereum=sum(r['primary']!='Ethereum' for r in pool),names=[(r['name'],r['primary'],r['next']) for r in pool]),
  cinq_oracles=[dict(name=r['name'],tvl_m=round(r['tvl']/1e6,1)) for r in rows if r['n']==5]),open(f'{OUT}/biais.json','w'),indent=1,default=str)
print('\n'.join(out))
