# Régénère quotes.txt depuis la pièce : une ligne « copie||citation » par citation “ ” distincte (citations vides ignorées).
# Désignation : la copie qui contient la citation (comparaison sensible à la casse) ; surcharges OVER pour les cas où plusieurs copies conviennent.
import re,glob,json,html
rep=open('HYLO-ET-AUTRES-CHAINES.md').read()
def norm(s):
    s=s.replace('\\$','$').replace('’',"'").replace('“','"').replace('”','"').replace('**','').replace('`','')
    return re.sub(r'\s+',' ',s)
files=[f for f in sorted(glob.glob('pages/*')+glob.glob('pages2/*')) if not f.endswith(('.pdf','.raw','.html'))]
corp={f:norm(open(f,errors='ignore').read()) for f in files}
for fn in glob.glob('pages2/inc-moonwell-*.json'):
    d=json.load(open(fn)); corp[fn]+=' '+norm(' '.join(html.unescape(re.sub(r'<[^>]+>',' ',p['cooked'])) for p in d['post_stream']['posts']))
OVER={'a highly decentralized stablecoin with no single point of failure':'pages/hylodocs-introduction.md','No fund manager, no third-party trading dependencies.':'pages/hylodocs-introduction.md','Coming soon.':'pages/hylodocs-product-guide-xassets.md','Dual-Token Stablecoin':'pages/llama-protocols.json','Pyth HYPE/USD price oracle':'pages/hylodocs-technical-addendum-hylo-equations.md','permissioned':'pages2/pyth-pro-how.txt','The price from the primary oracle is always preferred unless the price feed reports a stale price or detects unusual price movements':'pages2/thala-oracles.txt','The Custody account stores parameters and state for each token (SOL, ETH, BTC, USDC, USDT, JupUSD) managed by the JLP pool':'pages2/jup-dev-llms.txt','suspected':'pages2/x-fullsail-2026-08-29.txt'}
out=[];bad=[];seen=set()
for m in re.finditer(r'“([^”]+)”',rep):
    s=m.group(1)
    if not s.strip() or s in seen: continue
    seen.add(s)
    hit=[f for f,t in corp.items() if norm(s) in t]
    if s in OVER and OVER[s] in hit: f=OVER[s]
    elif hit:
        hit.sort(key=lambda f:('llama' in f,'llms' in f,'ddg' in f,f.endswith('.json') and 'moonwell' not in f)); f=hit[0]
    else: bad.append(s); continue
    out.append(f'{f}||{s}')
open('quotes.txt','w').write('\n'.join(out)+'\n')
print(len(out),'citations distinctes ;',len(bad),'introuvables :',bad)
