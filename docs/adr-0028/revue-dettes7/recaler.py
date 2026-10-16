"""Recalage orchestrateur des diffs DT7-f, DT7-l, R-1, R-2, R-5 sur la tete d'apres GARDE-FOUS : code et tests a
l'octet ; seuls changent le plancher du job controle-unittest (39 -> 117 : 115 + les deux tests de test_mutants.py),
la ligne de commentaire de gates.yml, et l'ajout date du README des controles, place en fin de fichier a la date
UTC donnee (ordre des dates, garde/lignes-citees.txt n'admet qu'un ajout en fin).
Usage : python3 -I -B recaler.py DIFF "<date UTC>" SORTIE.diff SORTIE-readme.txt"""
import re, sys
src, date, out, outr = sys.argv[1:5]
assert re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date), date
t = open(src, encoding='utf-8').read().split('\n')
# sections par fichier
sections, cur = [], None
for l in t:
    if l.startswith('diff --git '):
        cur = [l]; sections.append(cur)
    else:
        assert cur is not None, 'en-tete attendu'
        cur.append(l)
keep, readme = [], []
for s in sections:
    if s[0].endswith(' b/scripts/controle/README.md'):
        plus = [l[1:] for l in s if l.startswith('+') and not l.startswith('+++')]
        moins = [l for l in s if l.startswith('-') and not l.startswith('---')]
        assert not moins, 'hunk README non additif'
        n = 0
        for i, l in enumerate(plus):
            m = re.search(r'\*Ajout daté du \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', l)
            if m:
                plus[i] = l[:m.start()] + f'*Ajout daté du {date} UTC' + l[m.end():]; n += 1
        assert n == 1, ('un seul ajout date attendu', n)
        readme = [l.replace('plancher 39', 'plancher 117').replace('`controle-unittest` 39', '`controle-unittest` 117') for l in plus]
    else:
        keep.extend(s)
o = '\n'.join(keep)
o = o.replace('--plancher 37\n', '--plancher 115\n').replace('--plancher 39\n', '--plancher 117\n')
o = o.replace('# Lot DETTES-T7, DT7-f (2026-10-10) :', '# Lot DETTES-T7, DT7-f (2026-10-10, recalé ' + date[:10] + ') :')
o = o.replace('`controle-unittest` 39', '`controle-unittest` 117').replace('plancher 39.', 'plancher 117.').replace('plancher 39 ', 'plancher 117 ').replace('plancher 39)', 'plancher 117)')
assert 'plancher 39' not in o and all('plancher 39' not in l for l in readme)
if not o.endswith('\n'): o += '\n'  # section README en fin de diff : la ligne vide finale partait avec elle
open(out, 'w', encoding='utf-8', newline='\n').write(o)
open(outr, 'w', encoding='utf-8', newline='\n').write('\n'.join(readme) + ('\n' if readme else ''))
print(src, '->', out, len(readme), 'lignes README')
