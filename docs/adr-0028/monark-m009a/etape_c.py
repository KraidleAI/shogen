# Étape C — MONARK-S2-M009A-EXPOSITION-1 : rôles des sessions et circulation du chiffre, sans jamais l'afficher.
import json, os, re, sys, glob, subprocess, collections, hashlib
MONARK = os.environ.get('MONARK', r'F:\Monark')
RACINES = [r for r in sys.argv[1:] if os.path.isdir(r)] or [os.path.expanduser('~/.claude/projects')]
DOSSIERS = [d for d in os.environ.get('DOSSIERS', r'F:\tmp\shogen-carto-2026-09-29;F:\tmp\shogen-paquet;F:\Shogen\docs').split(';') if os.path.isdir(d)]
FICHIERS = [f for f in os.environ.get('FICHIERS', r'F:\Shogen\JOURNAL.md').split(';') if os.path.isfile(f)]
titre = os.environ.get('TITRE_TEST') or subprocess.run(['git', '-C', MONARK, 'log', '-1', '--format=%s', 'aa04924c'],
                                                        capture_output=True, text=True).stdout
var = set()
for j in re.findall(r'\d+[.,]\d+', titre):
    var |= {j, j.replace('.', ','), j.replace(',', '.')}
print('C0 jetons numériques du titre :', len(var), '; empreinte', hashlib.sha256('|'.join(sorted(var)).encode()).hexdigest()[:12])
if not var: sys.exit('C0 aucun jeton : arrêt')
JET = re.compile(r'(?<![\d.,])(' + '|'.join(re.escape(v) for v in sorted(var)) + r')(?![\d])')
CTX = re.compile(r'M009|p-hat|p̂|P̂|phat', re.I)
def occ(t):
    n = c = 0
    for m in JET.finditer(t):
        n += 1
        if CTX.search(t[max(0, m.start() - 300):m.end() + 300]): c += 1
    return n, c
def txt(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from txt(v)
    elif isinstance(o, list):
        for v in o: yield from txt(v)
agg = collections.defaultdict(lambda: [0, 0, None, None])
jours = collections.defaultdict(collections.Counter)
adr = collections.defaultdict(collections.Counter)
roles = {}
for rac in RACINES:
    for f in glob.glob(os.path.join(rac, '**', '*.jsonl'), recursive=True):
        rel = os.path.relpath(f, rac)
        principal = 'subagents' not in rel.replace('\\', '/').split('/')
        for ligne in open(f, encoding='utf-8', errors='replace'):
            try: ev = json.loads(ligne)
            except Exception: continue
            ts = ev.get('timestamp') or ''
            m = ev.get('message') or {}
            role = m.get('role') if isinstance(m, dict) else None
            c = m.get('content') if isinstance(m, dict) else None
            if principal and ts and role in ('user', 'assistant'): jours[rel][ts[:10]] += 1
            blocs = c if isinstance(c, list) else ([{'type': 'text', 'text': c}] if isinstance(c, str) else [])
            for b in blocs:
                if not isinstance(b, dict): continue
                ty = b.get('type')
                if ty == 'tool_use':
                    inp = b.get('input') or {}
                    if principal and b.get('name') in ('Write', 'Edit') and re.search(r'ADR-0028|ANNEXE-[A-E]', str(inp.get('file_path', ''))):
                        adr[rel][ts[:10]] += 1
                    t, genre = '\n'.join(txt(inp)), 'entree_outil'
                elif ty == 'tool_result': t, genre = '\n'.join(txt(b.get('content'))), 'resultat_outil'
                elif ty == 'text': t, genre = b.get('text') or '', f'texte_{role}'
                else: continue
                n, co = occ(t)
                if n:
                    a = agg[(rel, genre)]; a[0] += n; a[1] += co
                    if ts: a[2] = min(a[2] or ts, ts); a[3] = max(a[3] or ts, ts)
        if f.endswith('.jsonl') and 'subagents' in rel.replace('\\', '/'):
            meta = f[:-6] + '.meta.json'
            if os.path.isfile(meta):
                try:
                    d = json.load(open(meta, encoding='utf-8'))
                    roles[rel] = (str(d.get('agentType', ''))[:40], str(d.get('description', ''))[:100])
                except Exception: pass
print('\nC1 activité des fils principaux (messages par jour, 2026-09-25 à 2026-10-01) et écritures dans ADR-0028/annexes :')
for rel, cnt in sorted(jours.items()):
    sel = {j: n for j, n in sorted(cnt.items()) if '2026-09-25' <= j <= '2026-10-01'}
    if sel or adr.get(rel): print(' ', rel, '| messages', sel, '| écritures ADR-0028/annexes', dict(sorted(adr.get(rel, {}).items())))
print('\nC2 occurrences d\'un jeton du titre dans les transcriptions (n ; dont à moins de 300 caractères de M009/p-hat) :')
for (rel, genre), a in sorted(agg.items(), key=lambda kv: kv[1][2] or ''):
    if a[1]: print(f'  {genre} | {a[0]} ; {a[1]} | {a[2]} -> {a[3]} | {rel}')
print('  (lignes avec co-occurrence :', sum(1 for a in agg.values() if a[1]), '; sans co-occurrence, non listées :', sum(1 for a in agg.values() if not a[1]), ')')
print('\nC3 rôles des sous-agents nommés (type ; description tronquée) :')
CIBLES = os.environ.get('AGENTS', 'adf632be932312faa;a5310587045f17a80;abe5bb926883b9a33').split(';')
for rel, (ty, de) in sorted(roles.items()):
    if any(c in rel for c in CIBLES): print(' ', rel, '|', ty, '|', de)
print('\nC4 fichiers (n ; dont à moins de 300 caractères de M009/p-hat) :')
cand = list(FICHIERS)
for d in DOSSIERS:
    for f in glob.glob(os.path.join(d, '**', '*'), recursive=True):
        if os.path.isfile(f) and f.lower().endswith(('.md', '.txt', '.json', '.tsv', '.csv')) and os.path.getsize(f) < 50_000_000: cand.append(f)
cand = list(dict.fromkeys(os.path.normcase(os.path.abspath(f)) for f in cand))
k = 0
for f in cand:
    try: t = open(f, encoding='utf-8', errors='replace').read()
    except Exception: continue
    n, co = occ(t)
    if co: print(f'  {n} ; {co} | {f}'); k += 1
print('  fichiers avec co-occurrence :', k, 'sur', len(cand))
