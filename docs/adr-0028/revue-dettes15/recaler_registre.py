"""DETTES-T15, recalage orchestrateur : colonne `lignes` du registre docs/RENVOIS-LIGNES.tsv a la tete donnee.
Pour chaque entree dont `lignes` n est pas `-` : le bloc cite (empreinte = 16 premiers hex du SHA-256 des lignes
a..b de la cible au commit de lecture, jointes par LF) est cherche dans la cible a COMMIT ; `lignes` prend sa
position unique ; `-` s il n y est plus ; toute autre colonne inchangee. N imprime que des jetons et des comptes.
Usage : python3 -I -B recaler_registre.py DEPOT COMMIT REGISTRE SORTIE"""
import hashlib, subprocess, sys
R, C, REG, OUT = sys.argv[1:5]
def show(commit, chemin):
    p = subprocess.run(["git", "-C", R, "show", f"{commit}:{chemin}"], capture_output=True)
    return p.stdout.decode("utf-8") if p.returncode == 0 else None
def emp(lignes): return hashlib.sha256("\n".join(lignes).encode("utf-8")).hexdigest()[:16]
def plage(s):
    a, _, b = s.partition("-"); return int(a), int(b or a)
out, chang, perdus, inchanges, cache = [], [], [], 0, {}
for l in open(REG, encoding="utf-8").read().split("\n"):
    if not l or l.startswith("#") or l.startswith("renvoi\t"):
        out.append(l); continue
    c = l.split("\t"); assert len(c) == 7, c[:2]
    renvoi, jeton, cible, ecrit, lignes, e, commit = c
    if lignes == "-":
        out.append(l); continue
    key = (C, cible)
    if key not in cache: cache[key] = show(C, cible)
    t = cache[key]
    if t is None:
        c[4] = "-"; perdus.append(renvoi); out.append("\t".join(c)); continue
    L = t.split("\n"); a, b = plage(lignes); n = b - a + 1
    if emp(L[a - 1:b]) == e:
        inchanges += 1; out.append(l); continue
    pos = [i for i in range(len(L) - n + 1) if emp(L[i:i + n]) == e]
    if len(pos) == 1:
        c[4] = f"{pos[0] + 1}" if n == 1 else f"{pos[0] + 1}-{pos[0] + n}"; chang.append((renvoi, lignes, c[4]))
    else:
        c[4] = "-"; perdus.append((renvoi, lignes, len(pos)))
    out.append("\t".join(c))
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"inchangees {inchanges} ; deplacees {len(chang)} ; perdues {len(perdus)}")
for x in chang: print("  deplacee", *x)
for x in perdus: print("  perdue", x)
