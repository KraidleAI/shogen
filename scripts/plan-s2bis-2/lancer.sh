#!/usr/bin/env bash
# Lanceur unique du lot PLAN-S2BIS-2 (G0 docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §2, P2R-4 et
# P2R-5, et §7 ; forme de scripts/plan-s2bis/lancer.sh). Usage, par l'orchestrateur seul, une fois, détaché, après
# l'épinglage au JOURNAL :
#   bash scripts/plan-s2bis-2/lancer.sh <journaux> <sortie> <travail> <sha256 du SHA256SUMS du code>
# Ordre, chaque étape fermant la suivante :
#   1. variable de campagne non posée ; dossier des journaux présent ; sortie absente ou vide ;
#   2. épingle : sha256 du SHA256SUMS du lot égal à l'argument, puis sha256sum -c dans le dossier du lot ;
#   3. parametres.json de PLAN-S2BIS égal à son épingle ; paquet de S2 et commit d'analyse lus dans lui ;
#   4. aucune extraction dans le dossier de travail ; sha256 du paquet ; bloc machine (une ouverture, une clôture) ;
#      chaque journal du bloc présent et de sha256 égal ; commit du bloc = commit d'analyse ; control.jsonl et
#      journal.jsonl nommés.
# N'affiche que des noms, des codes et des sha256 : aucun journal n'est ouvert ici (sha256sum seul).
# Codes : 2 usage ; 3 refus avant tout lancement. Aucune barre oblique inverse dans ce fichier.
set -u -o pipefail
export LC_ALL=C
ICI="$(cd "$(dirname "$0")" && pwd)"
DEPOT="$(cd "$ICI/../.." && pwd)"
P="$ICI/parametres.json"
refus() { echo "REFUS $1 : $2" >&2; exit 3; }
empreinte() { sha256sum < "$1" | cut -d' ' -f1; }
egal() { [ -f "$1" ] && [ "$(empreinte "$1")" = "$2" ]; }
[ "$#" -eq 4 ] || { echo "REFUS P2/usage : bash lancer.sh <journaux> <sortie> <travail> <sha256>" >&2; exit 2; }
J="$1"; S="$2"; T="$3"; E="$4"
[ -z "${SHOGEN_S2_CAMPAGNE_CONTROL+x}" ] || refus P2/variable "SHOGEN_S2_CAMPAGNE_CONTROL est posée"
[ -d "$J" ] || refus P2/journal "dossier des journaux absent"
if [ -e "$S" ]; then { [ -d "$S" ] && [ -z "$(ls -A "$S")" ]; } || refus P2/sortie "dossier de sortie non vide"; fi
egal "$ICI/SHA256SUMS" "$E" || refus P2/epingle "sha256 du SHA256SUMS du lot différent de l'argument"
( cd "$ICI" && sha256sum --quiet --strict -c SHA256SUMS ) > /dev/null 2>&1 || refus P2/epingle "sha256sum -c en échec"
mapfile -t EPI < <(python3 -B - "$P" <<'FIN'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    p = json.load(f)
for k in sorted(p["plan_s2bis"]["chemins"]):
    print(k, p["plan_s2bis"]["chemins"][k], p["plan_s2bis"]["sha256"][k])
assert p["passes"]["variable"] == "PYTHONHASHSEED"
print("passes", p["passes"]["A"], p["passes"]["B"])
FIN
)
[ "${#EPI[@]}" -eq 9 ] || refus P2/plan-s2bis "épingles de PLAN-S2BIS illisibles dans parametres.json du lot"
declare -A CH SH
for x in "${EPI[@]}"; do read -r k c h <<< "$x"; CH[$k]="$c"; SH[$k]="$h"; done
PS2="$DEPOT/${CH[parametres]}"
egal "$PS2" "${SH[parametres]}" || refus P2/plan-s2bis "parametres.json de PLAN-S2BIS différent de son épingle"
echo "REFUS P2/usage : lanceur incomplet, passes A et B au sous-lot P2R-5" >&2
exit 5
