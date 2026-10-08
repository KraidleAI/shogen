#!/usr/bin/env python3
"""raw/detail/*.json(.gz) + cibles.json -> out/cibles-actifs.json (part des actifs S2-bis dans la TVL, par symbole : [inferé])"""
import json,gzip,os,re,datetime
HERE=os.path.dirname(os.path.abspath(__file__)); D=f'{HERE}/raw/detail'
R={r['name']:r for r in json.load(open(f'{HERE}/out/rows.json'))}; C=json.load(open(f'{HERE}/cibles.json'))
def load(s):
    for ext,op in(('.json.gz',gzip.open),('.json',open)):
        p=f'{D}/{s}{ext}'
        if os.path.exists(p):
            with op(p,'rt') as f: return json.load(f)
def grp(sym):
    u=sym.upper()
    if u in('USDC','USDC.E','USDBC','AUSDC','USDCE'): return 'USDC'
    if u in('USDT','USDT0','USDT.E','USDTE','BSC-USD'): return 'USDT'
    if 'BTC' in u: return 'BTC'
    if u in('ETH','WETH','STETH','WSTETH','WEETH','RETH','CBETH','EZETH','RSETH','METH','WRSETH','WEETHS','SFRXETH','OSETH','EETH','PUFETH','SWETH','ETHX','WBETH'): return 'ETH'
    return 'autre'
out={}
for t in 'GMP':
    for n in C[t]:
        r=R[n]; d=load(r['slug'])
        if d is None:   # detail absent de raw/detail (a telecharger par fetch_detail.sh) : on ne comble pas
            out[n]={'date':None,'absent':True}; continue
        tk=d.get('tokensInUsd') or []
        last=tk[-1] if tk else None
        s={'BTC':0,'ETH':0,'USDC':0,'USDT':0,'autre':0}
        if last:
            for k,v in last['tokens'].items(): s[grp(k)]+=v
        tot=sum(s.values()) or 1
        top=sorted(last['tokens'].items(),key=lambda kv:-kv[1])[:4] if last else []
        out[n]={'date':datetime.datetime.fromtimestamp(last['date'],datetime.timezone.utc).date().isoformat() if last else None,
          'total_tokens_usd':round(sum(s.values())),'parts':{k:round(100*v/tot,2) for k,v in s.items()},
          'top':[(k,round(v/1e6,1)) for k,v in top],'top_pct':[(k,round(100*v/tot,2)) for k,v in sorted(last['tokens'].items(),key=lambda kv:-kv[1])[:8]] if last else [],'hacks_detail':[(datetime.date.fromtimestamp(h['date']).isoformat(),h.get('technique'),h.get('amount')) for h in d.get('hacks') or []],
          'ob_detail':[(o['name'],o.get('type'),o.get('startDate'),o.get('endDate')) for o in d.get('oraclesBreakdown') or []]}
json.dump(out,open(f'{HERE}/out/cibles-actifs.json','w'),indent=1)
for n,v in out.items(): print(n,v['date'],v.get('parts','ABSENT'),v.get('top',[])[:3],len(v.get('hacks_detail',[])))
