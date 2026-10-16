#!/usr/bin/env python3
# Contrôle des citations contre l'extraction texte (sidecar) du livre de Shostack.
# Usage : python3 -I check_citations.py <sidecar> <quotes.tsv> <citations.tsv>
# Règle : mot pour mot après repliement des blancs et NFKC (ligatures) ; une seule occurrence ; <= 25 mots ;
# page trouvée = étiquette "Page N" du pied de la page qui contient la citation.
import re, sys, unicodedata
side, qfile, out = sys.argv[1:4]
raw = open(side, encoding='utf-8').read()
foot = re.compile(r'\.indd\s.*?Page\s+(\S+)\s*$', re.M)
def norm(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', s)).strip()
# segments : chaque page se termine par sa ligne de pied
segs = []; start = 0
for m in foot.finditer(raw):
    segs.append((m.group(1), start, m.end())); start = m.end()
segs.append(('TAIL', start, len(raw)))
# texte normalisé segment par segment, concaténé avec un séparateur de page
parts = []; bounds = []; pos = 0
for label, a, b in segs:
    t = norm(raw[a:b]); parts.append(t)
    bounds.append((label, pos, pos + len(t))); pos += len(t) + 1
full = ' '.join(parts)
def page_of(off):
    for label, a, b in bounds:
        if a <= off < b + 1:
            return label
    return '?'
rows = []; ok_all = True
for line in open(qfile, encoding='utf-8'):
    line = line.rstrip('\n')
    if not line: continue
    qid, page, quote = line.split('\t')
    q = norm(quote); words = len(q.split())
    offs = [m.start() for m in re.finditer(re.escape(q), full)]
    found = len(offs) == 1
    pf = page_of(offs[0]) if offs else '-'
    good = found and pf == page and words <= 25
    ok_all &= good
    rows.append((qid, quote, page, pf, str(len(offs)), str(words), 'oui' if good else 'non'))
with open(out, 'w', encoding='utf-8') as f:
    f.write('id\tcitation\tpage_attendue\tpage_trouvee\toccurrences\tmots\ttrouvee_une_fois_bonne_page_25_mots_max\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print(len(rows), 'citations ;', sum(1 for r in rows if r[6] == 'oui'), 'oui ;', sum(1 for r in rows if r[6] != 'oui'), 'non')
for r in rows:
    if r[6] != 'oui': print('ECHEC', r[0], 'page_attendue', r[2], 'trouvee', r[3], 'occ', r[4], 'mots', r[5], '|', r[1][:70])
sys.exit(0 if ok_all else 1)
