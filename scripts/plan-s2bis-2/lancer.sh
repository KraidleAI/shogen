#!/usr/bin/env bash
# Lanceur unique du lot PLAN-S2BIS-2 (G0 docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §2, P2R-4 et
# P2R-5, et §7 ; forme de scripts/plan-s2bis/lancer.sh). Usage, par l'orchestrateur seul, une fois, détaché, après
# l'épinglage au JOURNAL :
#   bash scripts/plan-s2bis-2/lancer.sh <journaux> <sortie> <travail> <sha256 du SHA256SUMS du code>
# Ordre du code, chaque étape fermant la suivante :
#   1. quatre arguments ; variable de campagne non posée ; dossier des journaux présent ; sortie absente ou vide ;
#   2. épingle : sha256 du SHA256SUMS du lot égal à l'argument, sha256sum -c dans le dossier du lot, et aucune entrée
#      de ce dossier, dossiers à part, hors de SHA256SUMS (__pycache__ compris) ;
#   3. épingles de PLAN-S2BIS lues dans le parametres.json du lot ; parametres.json de PLAN-S2BIS égal à son épingle,
#      puis les sept autres pièces égales aux leurs ; paquet de S2 et commit d'analyse lus dans ce parametres.json ;
#   4. commit d'analyse bien formé ; ni extraction ni cache de bytecode (pyc) dans le dossier de travail ; sha256 du
#      paquet ; bloc machine (une ouverture, une clôture) ; chaque journal du bloc présent et de sha256 égal ; commit
#      du bloc = commit d'analyse ; control.jsonl et journal.jsonl nommés ;
#   5. extraction du commit d'analyse dans <travail>/<7 premiers caractères>, dossiers interdits exclus (P-9) ;
#   6. passe A (PYTHONHASHSEED de A), puis passe B : masque_fiv.py, puis intervalles.py, sorties dans <travail>/A et
#      <travail>/B, chacune avec son SHA256SUMS ; un script hors 0 arrête tout (B non commencée si A échoue, P-7) ;
#   7. SHA256SUMS de A et de B comparés à l'octet : égaux, les trois sorties de A et son SHA256SUMS copiés dans
#      <sortie> ; différents, refus P2/identite, rien dans <sortie>, les deux SHA256SUMS affichés (P-8).
# Code exécuté = code épinglé (C-1 de la G2 ; Q-CORR-5) : parametres.json lus par python3 -I -S ; scripts en
# python3 -S -B sous un environnement réduit à une liste fermée (PATH, LC_ALL, PYTHONHASHSEED de la passe,
# PYTHONDONTWRITEBYTECODE, PYTHONPYCACHEPREFIX vers <travail>/pyc, neuf) : ni site-packages, système ou utilisateur,
# ni .pth, ni bytecode voisin des sources.
# N'affiche que des noms, des codes et des sha256 : aucun journal n'est ouvert ici (sha256sum seul), aucune sortie
# n'est affichée ; messages des scripts dans <travail>/lancer.log. Codes : 0 ; 2 usage ; 3 refus avant tout
# lancement ; 4 extraction impossible ; 5 un script hors 0, A ≠ B, ou écriture impossible ; toute sortie hors 0 est
# nommée sur l'écran. Aucune barre oblique inverse dans ce fichier.
set -u -o pipefail
export LC_ALL=C
ICI="$(cd "$(dirname "$0")" && pwd)"
DEPOT="$(cd "$ICI/../.." && pwd)"
P="$ICI/parametres.json"
refus() { echo "REFUS $1 : $2" >&2; exit 3; }
echec() { echo "$2 : code $1" >&2; exit "$1"; }
empreinte() { sha256sum < "$1" | cut -d' ' -f1; }
egal() { [ -f "$1" ] && [ "$(empreinte "$1")" = "$2" ]; }
[ "$#" -eq 4 ] || { echo "REFUS P2/usage : bash lancer.sh <journaux> <sortie> <travail> <sha256>" >&2; exit 2; }
J="$1"; S="$2"; T="$3"; E="$4"
[ -z "${SHOGEN_S2_CAMPAGNE_CONTROL+x}" ] || refus P2/variable "SHOGEN_S2_CAMPAGNE_CONTROL est posée"
[ -d "$J" ] || refus P2/journal "dossier des journaux absent"
if [ -e "$S" ]; then { [ -d "$S" ] && [ -z "$(ls -A "$S")" ]; } || refus P2/sortie "dossier de sortie non vide"; fi
egal "$ICI/SHA256SUMS" "$E" || refus P2/epingle "sha256 du SHA256SUMS du lot différent de l'argument"
( cd "$ICI" && sha256sum --quiet --strict -c SHA256SUMS ) > /dev/null 2>&1 || refus P2/epingle "sha256sum -c en échec"
LISTE="$(cut -d' ' -f3- "$ICI/SHA256SUMS" | sort)"
[ "$(cd "$ICI" && find . ! -type d ! -path ./SHA256SUMS | cut -c3- | sort)" = "$LISTE" ] ||
  refus P2/epingle "entrée du dossier du lot hors de SHA256SUMS"
mapfile -t EPI < <(python3 -I -S -B - "$P" 2> /dev/null <<'FIN'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    p = json.load(f)
for k in sorted(p["plan_s2bis"]["chemins"]):
    print(k, p["plan_s2bis"]["chemins"][k], p["plan_s2bis"]["sha256"][k])
assert p["passes"]["variable"] == "PYTHONHASHSEED" and "parametres" in p["plan_s2bis"]["chemins"]
print("passes", p["passes"]["A"], p["passes"]["B"])
FIN
)
[ "${#EPI[@]}" -eq 9 ] || refus P2/plan-s2bis "épingles de PLAN-S2BIS illisibles dans parametres.json du lot"
declare -A CH SH
for x in "${EPI[@]}"; do read -r k c h <<< "$x"; CH[$k]="$c"; SH[$k]="$h"; done
PS2="$DEPOT/${CH[parametres]}"
egal "$PS2" "${SH[parametres]}" || refus P2/plan-s2bis "parametres.json de PLAN-S2BIS différent de son épingle"
for x in "${EPI[@]:0:8}"; do
  read -r k c h <<< "$x"
  [ "$k" = parametres ] || egal "$DEPOT/$c" "$h" || refus P2/plan-s2bis "pièce $k de PLAN-S2BIS ≠ son épingle"
done
mapfile -t V < <(python3 -I -S -B - "$PS2" 2> /dev/null <<'FIN'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    p = json.load(f)
print(p["paquet_s2"]["chemin"])
print(p["paquet_s2"]["sha256"])
print(p["commit_analyse"])
FIN
)
[ "${#V[@]}" -eq 3 ] || refus P2/plan-s2bis "parametres.json de PLAN-S2BIS illisible"
PAQ="$DEPOT/${V[0]}"
COMMIT="${V[2]}"
[[ "$COMMIT" =~ ^[0-9a-f]{40}$ ]] || refus P2/plan-s2bis "commit_analyse de PLAN-S2BIS malformé"
X="$T/${COMMIT:0:7}"
[ ! -e "$X" ] && [ ! -e "$T/pyc" ] ||
  refus P2/sortie "extraction ou cache de bytecode déjà présent dans le dossier de travail"
egal "$PAQ" "${V[1]}" || refus P2/paquet "sha256 du paquet de S2 différent de l'épingle"
[ "$(grep -c '^```shogen-paquet-v1$' "$PAQ")" = 1 ] || refus P2/paquet "bloc machine : ouverture absente ou multiple"
LIRE='f && /^```$/ {g = 1; exit} f {print} /^```shogen-paquet-v1$/ {f = 1} END {exit !g}'
BLOC="$(awk "$LIRE" "$PAQ")" || refus P2/paquet "bloc machine non fermé"
NOMS=" "
CB=""
while read -r cle a b reste; do
  case "$cle" in
    commit_analyse) CB="$a" ;;
    journal)
      { [ -z "$reste" ] && [[ "$b" =~ ^[0-9a-f]{64}$ ]]; } || refus P2/journal "ligne journal malformée au bloc machine"
      case "$a" in ''|*/*|.*) refus P2/journal "nom de journal refusé" ;; esac
      [ -f "$J/$a" ] || refus P2/journal "journal absent : $a"
      [ "$(empreinte "$J/$a")" = "$b" ] || refus P2/journal "sha256 de $a différent du bloc machine"
      echo "journal $a : sha256 égal au bloc machine"
      NOMS="$NOMS$a " ;;
  esac
done <<< "$BLOC"
[ "$CB" = "$COMMIT" ] || refus P2/commit "commit_analyse du bloc machine différent de celui de PLAN-S2BIS"
for n in control.jsonl journal.jsonl; do
  case "$NOMS" in *" $n "*) ;; *) refus P2/journal "$n absent du bloc machine" ;; esac
done
EXCL=(--exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a)
EXCL+=(--exclude=docs/adr-0028/execution "--exclude=docs/15-*" "--exclude=docs/16-*" --exclude=docs/pocket-report)
mkdir -p "$X" "$T/pyc" 2> /dev/null || echec 4 "extraction impossible"
PYC="$(cd "$T/pyc" 2> /dev/null && pwd)" || echec 4 "extraction impossible"
git --no-optional-locks -C "$DEPOT" archive "$COMMIT" | tar -x -C "$X" "${EXCL[@]}" || echec 4 "extraction impossible"
PY=(env -i PATH="$PATH" LC_ALL=C PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$PYC")
ARGS=(--journaux "$J" --harnais "$X/s2-harness" --parametres "$P")
LOG="$T/lancer.log"
read -r _p GA GB <<< "${EPI[8]}"
for passe in A B; do
  graine="$GA"; [ "$passe" = A ] || graine="$GB"
  mkdir -p "$T/$passe" 2> /dev/null || echec 5 "passe $passe : dossier impossible"
  for s in masque_fiv intervalles; do
    "${PY[@]}" PYTHONHASHSEED="$graine" python3 -S -B "$ICI/$s.py" "${ARGS[@]}" --sortie "$T/$passe" >> "$LOG" 2>&1
    r=$?
    echo "passe $passe $s : code $r"
    [ "$r" -eq 0 ] || exit 5
  done
  { ( cd "$T/$passe" && sha256sum fiv_unites.txt intervalles.txt masque_j28.txt ) > "$T/$passe.sommes" &&
    mv "$T/$passe.sommes" "$T/$passe/SHA256SUMS"; } 2> /dev/null || echec 5 "passe $passe : SHA256SUMS impossible"
done
if ! cmp -s "$T/A/SHA256SUMS" "$T/B/SHA256SUMS"; then
  echo "REFUS P2/identite : SHA256SUMS des passes A et B différents (affichés ci-dessous, A puis B)" >&2
  cat "$T/A/SHA256SUMS" "$T/B/SHA256SUMS"
  exit 5
fi
{ mkdir -p "$S" && cp "$T/A/SHA256SUMS" "$T/A/fiv_unites.txt" "$T/A/intervalles.txt" "$T/A/masque_j28.txt" "$S/"
  } 2> /dev/null || echec 5 "copie de la passe A impossible"
cat "$S/SHA256SUMS"
exit 0
