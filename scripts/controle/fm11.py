"""Contrôle FM-1.1 non-LLM d'une transcription de sous-agent (annexe C l.13 ; D.2 pts 1-11).
N'affiche jamais le contenu d'une pièce de D.2 : comptes, rôles et numéros d'événement seulement."""
import json, sys, hashlib, re, subprocess
REPO = '/home/user/shogen'
# lignes interdites, repérées par sha256, jamais affichées
def ligne_par_sha(chemin, sha, rev=None):
    txt = subprocess.run(['git','-C',REPO,'show',f'{rev}:{chemin}'],capture_output=True).stdout if rev \
          else open(f'{REPO}/{chemin}','rb').read()
    for l in txt.split(b'\n'):
        if hashlib.sha256(l + b'\n').hexdigest() == sha: return l.decode()
    return None
SHA51 = '5cc89b563f73d213e38021165a360c3bf2e297e36be467786a007021c71db358'
SHA14 = '0fe88f1a3810244ecce91b31c1f4e2117f397a7c65d381a75afdbf0b9954b71f'
interdites = {'carto_l51': ligne_par_sha('docs/rapports/cartographie-2026-09-29.md', SHA51),
              'adr0025_l14': ligne_par_sha('docs/adr-0025/ADR-0025-periode-doublee-S2.md', SHA14, '7f8b5cc')}
for k,v in interdites.items():
    if v is None: sys.exit(f'ligne {k} introuvable par sha : contrôle impossible')
# fragments : tous les segments de 40 caractères (pas 20) de chaque ligne interdite, et toujours les 40 derniers
# (lot DETTES-T3, DT3-E : la queue n'était dans aucun fragment) ; une ligne de moins de 40 caractères est un fragment
frags = {k: {v[i:i+40] for i in range(0, max(1,len(v)-40), 20)} | {v[-40:]} for k,v in interdites.items()}
motifs = [r'cartographie-2026-09-29', r'CARTOGRAPHIE-2026-09-29', r'adr-0025', r'ADR-0025\.md', r'shogen-carto',
          r'shogen-j28', r'campagne-copie', r'shogen-campagne', r'measure-M009a', r'lot-m009', r'ADR-M002',
          r'PAROXYSME-Shogen', r'paroxysme-2026-09-27', r'session_013dvmub', r'7ba84933-ba6d', r'shogen-g2-lotA',
          r'ARCHIVE-shogen-interne', r'AVIS-advisor-2026-09-26', r'baseline_step0', r'SHA256SUMS-cloture',
          r'(?<![\w-])(control|journal|raw)\.jsonl']
def textes(obj):
    if isinstance(obj,str): yield obj
    elif isinstance(obj,dict):
        for v in obj.values(): yield from textes(v)
    elif isinstance(obj,list):
        for v in obj: yield from textes(v)
res = {'evenements':0, 'resultats':{}, 'entrees':{}, 'fragments_l51_l14':{'resultats':0,'entrees':0}}
for n, ligne in enumerate(open(sys.argv[1], encoding='utf-8')):
    ev = json.loads(ligne); res['evenements'] += 1
    msg = ev.get('message') or {}
    contenu = msg.get('content') if isinstance(msg,dict) else None
    if not isinstance(contenu, list): contenu = [{'type':'text','text':c} for c in textes(contenu)] if contenu else []
    for bloc in contenu:
        if not isinstance(bloc, dict): continue
        role = 'resultats' if bloc.get('type')=='tool_result' else 'entrees'
        t = '\n'.join(textes(bloc.get('content') if role=='resultats' else bloc))
        for m in motifs:
            c = len(re.findall(m, t))
            if c: res[role].setdefault(m, []).append((n, c))
        for k,fs in frags.items():
            if any(f in t for f in fs): res['fragments_l51_l14'][role] += 1; res[role].setdefault('FRAGMENT:'+k,[]).append(n)
print(json.dumps(res, ensure_ascii=False, indent=1))
