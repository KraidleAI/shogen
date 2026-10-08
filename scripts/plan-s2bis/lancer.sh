#!/usr/bin/env bash
# Lanceur unique du lot PLAN-S2BIS (G0 docs/adr-0029/G0-lot-PLAN-S2BIS.md ; ADR-0029 §6 lot 3 ; annexe B d'ADR-0028,
# SHOGEN-POSTPREREG-PARAMS-SCEAU-1). Usage, depuis n'importe quel dossier, après épinglage au JOURNAL :
#   bash scripts/plan-s2bis/lancer.sh <dossier des journaux> <dossier de sortie> <dossier de travail>
# Ordre, chaque étape fermant la suivante :
#   1. SHOGEN_S2_CAMPAGNE_CONTROL non posée ; sortie absente ou vide ; aucune extraction dans le dossier de travail ;
#   2. sha256 du paquet de S2 égal à l'épingle de parametres.json ;
#   3. bloc machine shogen-paquet-v1 (une ouverture, une clôture) : commit_analyse égal à celui de parametres.json ;
#      chaque ligne « journal <nom> <sha256> » égale au sha256 du fichier du dossier des journaux ; control.jsonl et
#      journal.jsonl nommés ;
#   4. extraction du commit d'analyse dans <travail>/<7 premiers caractères>, dossiers interdits exclus ;
#   5. les trois scripts, sorties dans <sortie>, messages des scripts dans <travail>/lancer.log, sommes dans
#      <sortie>/SHA256SUMS.
# N'affiche que des noms, des codes et des sha256 : aucun journal n'est ouvert ici (sha256sum seul), aucune sortie n'est
# affichée. Durée non mesurée sur les journaux : lancer détaché (setsid nohup) ou en tâche de fond à délai explicite.
# Codes : 0 trois scripts en 0 ; 2 usage ; 3 refus avant tout lancement ; 4 extraction impossible ; 5 un script hors 0.
# Aucune barre oblique inverse dans ce fichier (consigne SHOGEN-HARNAIS-ECHAPPEMENTS-1).
set -u -o pipefail
export LC_ALL=C
ICI="$(cd "$(dirname "$0")" && pwd)"
DEPOT="$(cd "$ICI/../.." && pwd)"
P="$ICI/parametres.json"
refus() { echo "REFUS : $1" >&2; exit 3; }
empreinte() { sha256sum < "$1" | cut -d' ' -f1; }
[ "$#" -eq 3 ] || { echo "usage : bash lancer.sh <journaux> <sortie> <travail>" >&2; exit 2; }
J="$1"; S="$2"; T="$3"
[ -z "${SHOGEN_S2_CAMPAGNE_CONTROL+x}" ] || refus "SHOGEN_S2_CAMPAGNE_CONTROL est posée"
[ -d "$J" ] || refus "dossier des journaux absent"
if [ -e "$S" ]; then { [ -d "$S" ] && [ -z "$(ls -A "$S")" ]; } || refus "dossier de sortie non vide"; fi
mapfile -t V < <(python3 -B - "$P" <<'FIN'
import json, sys
p = json.load(open(sys.argv[1], encoding="utf-8"))
print(p["paquet_s2"]["chemin"])
print(p["paquet_s2"]["sha256"])
print(p["commit_analyse"])
FIN
)
[ "${#V[@]}" -eq 3 ] || refus "parametres.json illisible"
PAQ="$DEPOT/${V[0]}"
COMMIT="${V[2]}"
[[ "$COMMIT" =~ ^[0-9a-f]{40}$ ]] || refus "commit_analyse de parametres.json malformé"
X="$T/${COMMIT:0:7}"
[ ! -e "$X" ] || refus "extraction déjà présente dans le dossier de travail"
{ [ -f "$PAQ" ] && [ "$(empreinte "$PAQ")" = "${V[1]}" ]; } || refus "sha256 du paquet de S2 différent de l'épingle"
[ "$(grep -c '^```shogen-paquet-v1$' "$PAQ")" = 1 ] || refus "bloc machine : ouverture absente ou multiple"
LIRE='f && /^```$/ {g = 1; exit} f {print} /^```shogen-paquet-v1$/ {f = 1} END {exit !g}'
BLOC="$(awk "$LIRE" "$PAQ")" || refus "bloc machine non fermé"
NOMS=" "
CB=""
while read -r cle a b reste; do
  case "$cle" in
    commit_analyse) CB="$a" ;;
    journal)
      { [ -z "$reste" ] && [[ "$b" =~ ^[0-9a-f]{64}$ ]]; } || refus "ligne journal malformée au bloc machine"
      case "$a" in ''|*/*|.*) refus "nom de journal refusé" ;; esac
      [ -f "$J/$a" ] || refus "journal absent : $a"
      [ "$(empreinte "$J/$a")" = "$b" ] || refus "sha256 de $a différent du bloc machine"
      echo "journal $a : sha256 égal au bloc machine"
      NOMS="$NOMS$a " ;;
  esac
done <<< "$BLOC"
[ "$CB" = "$COMMIT" ] || refus "commit_analyse du bloc machine différent de parametres.json"
for n in control.jsonl journal.jsonl; do
  case "$NOMS" in *" $n "*) ;; *) refus "$n absent du bloc machine" ;; esac
done
EXCL=(--exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a)
EXCL+=("--exclude=docs/15-*" "--exclude=docs/16-*" --exclude=docs/pocket-report)
mkdir -p "$X" || exit 4
git -C "$DEPOT" archive "$COMMIT" | tar -x -C "$X" "${EXCL[@]}" || { echo "extraction impossible" >&2; exit 4; }
mkdir -p "$S" || exit 4
RC=0
ARGS=(--journaux "$J" --harnais "$X/s2-harness" --parametres "$P")
PY=(env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B)
for s in tau_sigma episodes okx; do
  "${PY[@]}" "$ICI/$s.py" "${ARGS[@]}" --sortie "$S/$s.txt" >> "$T/lancer.log" 2>&1
  r=$?
  echo "$s : code $r"
  [ "$r" -eq 0 ] || RC=5
done
( cd "$S" && for s in tau_sigma episodes okx; do [ ! -f "$s.txt" ] || sha256sum "$s.txt"; done ) > "$T/sommes" || RC=5
mv "$T/sommes" "$S/SHA256SUMS" && cat "$S/SHA256SUMS"
exit "$RC"
