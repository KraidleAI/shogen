# Verifie que chaque citation de quotes.txt (format fichier||texte) figure verbatim dans le fichier copie.
# Comparaison SENSIBLE A LA CASSE (G2, C2b). Normalisation : espaces, apostrophes/guillemets typographiques, \$, ** et ` du markdown. Plus de 25 mots = signale.
import re, json, html
def norm(s):
    s = s.replace('\\$', '$').replace('’', "'").replace('“', '"').replace('”', '"').replace('**', '').replace('`', '')
    return re.sub(r'\s+', ' ', s)
def text(fn):
    t = open(fn, errors='ignore').read()
    if fn.endswith('.json') and 'inc-moonwell' in fn:
        d = json.loads(t)
        t += ' ' + ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', p['cooked'])) for p in d['post_stream']['posts'])
    return norm(t)
ko = 0
for l in open('quotes.txt'):
    if not l.strip(): continue
    f, s = l.rstrip('\n').split('||', 1)
    ok = norm(s) in text(f); w = len(s.split())
    if not ok or w > 25: ko += 1
    print('OK  ' if ok else 'MISS', 'LONG' if w > 25 else '    ', w, f, '|', s[:70])
print('problemes:', ko)
