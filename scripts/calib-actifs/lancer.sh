#!/usr/bin/env bash
# Lanceur unique du lot CALIB-ACTIFS (G0 docs/adr-0029/g0-calib/ ; PROPOSITION §5.7 et §6.1 CA-6 ; E-CA-03, E-CA-13,
# E-CA-21, E-CA-27, E-CA-28 ; forme de scripts/plan-s2bis-2/lancer.sh). Par l'orchestrateur seul, une fois, détaché,
# après l'épinglage au JOURNAL :
#   bash scripts/calib-actifs/lancer.sh <bruts> <sortie> <travail> <sha256 du SHA256SUMS du lot>
# Ordre, chaque étape fermant la suivante :
#   1. quatre arguments ; variable de campagne non posée ; sortie et travail absents ou vides ;
#   2. épingle : sha256 du SHA256SUMS du lot égal à l'argument, sha256sum -c, aucune entrée hors de SHA256SUMS ;
#   3. étape réseau (E-CA-13) : acquerir.py --bruts <bruts>, reprise sur le manifeste des bruts ;
#   4. passes A puis B (PYTHONHASHSEED de parametres.json) : tau.py --bruts <bruts> --sortie <travail>/A ou B ; un code
#      hors 0 arrête tout ; 5. SHA256SUMS des deux sorties de A et de B comparés à l'octet (E-CA-21) ;
#   6. sorties de A, manifeste des bruts et leur SHA256SUMS copiés dans <sortie>.
# Scripts en python3 -S -B sous env -i : PATH, LC_ALL, PYTHONDONTWRITEBYTECODE, PYTHONPYCACHEPREFIX vers <travail>/pyc,
# TMPDIR vers <travail>/tmp (E-CA-05), PYTHONHASHSEED de la passe ; l'étape réseau garde en plus les seules variables de
# mandataire et de certificats présentes (liste fermée). Codes : 0 ; 2 usage ; 3 refus avant tout lancement ; 4
# acquisition impossible ; 5 calcul hors 0, A ≠ B ou écriture impossible. L'écran ne porte que des noms, des codes et
# des sha256 ; messages des scripts dans <travail>/lancer.log. Aucune barre oblique inverse dans ce fichier.
set -u -o pipefail
export LC_ALL=C
ICI="$(cd "$(dirname "$0")" && pwd)"
refus() { echo "REFUS $1 : $2" >&2; exit "$3"; }
empreinte() { sha256sum < "$1" | cut -d' ' -f1; }
vide() { [ ! -e "$1" ] || { [ -d "$1" ] && [ -z "$(ls -A "$1")" ]; }; }
[ "$#" -eq 4 ] || refus CA/usage "bash lancer.sh <bruts> <sortie> <travail> <sha256>" 2
B="$1"; S="$2"; T="$3"; E="$4"
[ -z "${SHOGEN_S2_CAMPAGNE_CONTROL+x}" ] || refus CA/variable "SHOGEN_S2_CAMPAGNE_CONTROL est posée" 3
vide "$S" || refus CA/sortie "dossier de sortie non vide" 3
vide "$T" || refus CA/sortie "dossier de travail non vide" 3
{ [ -f "$ICI/SHA256SUMS" ] && [ "$(empreinte "$ICI/SHA256SUMS")" = "$E" ]; } ||
  refus CA/epingle "sha256 du SHA256SUMS du lot différent de l'argument" 3
( cd "$ICI" && sha256sum --quiet --strict -c SHA256SUMS ) > /dev/null 2>&1 || refus CA/epingle "sha256sum -c en échec" 3
LISTE="$(cut -d' ' -f3- "$ICI/SHA256SUMS" | sort)"
[ "$(cd "$ICI" && find . ! -type d ! -path ./SHA256SUMS | cut -c3- | sort)" = "$LISTE" ] ||
  refus CA/epingle "entrée du dossier du lot hors de SHA256SUMS" 3
read -r GA GB < <(python3 -I -S -B -c 'import json, sys
p = json.load(open(sys.argv[1], encoding="utf-8"))["passes"]
print(p["A"], p["B"])' "$ICI/parametres.json" 2> /dev/null)
[[ "${GA:-}" =~ ^[0-9]+$ && "${GB:-}" =~ ^[0-9]+$ ]] || refus CA/parametres "passes illisibles dans parametres.json" 3
mkdir -p "$T/pyc" "$T/tmp" "$B" 2> /dev/null || refus CA/sortie "dossier de travail ou des bruts impossible" 3
PYC="$(cd "$T/pyc" && pwd)"
PY=(env -i PATH="$PATH" LC_ALL=C PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$PYC" TMPDIR="$(cd "$T/tmp" && pwd)")
RESEAU=()
for v in HTTPS_PROXY https_proxy HTTP_PROXY http_proxy NO_PROXY no_proxy SSL_CERT_FILE SSL_CERT_DIR; do
  [ -z "${!v+x}" ] || RESEAU+=("$v=${!v}")
done
LOG="$T/lancer.log"
"${PY[@]}" "${RESEAU[@]}" python3 -S -B "$ICI/acquerir.py" --bruts "$B" >> "$LOG" 2>&1
r=$?
echo "acquisition : code $r"
[ "$r" -eq 0 ] || refus CA/acquisition "acquerir.py en code $r (lancer.log)" 4
for passe in A B; do
  graine="$GA"; [ "$passe" = A ] || graine="$GB"
  "${PY[@]}" PYTHONHASHSEED="$graine" python3 -S -B "$ICI/tau.py" --bruts "$B" --sortie "$T/$passe" >> "$LOG" 2>&1
  r=$?
  echo "passe $passe : code $r"
  [ "$r" -eq 0 ] || exit 5
  { ( cd "$T/$passe" && sha256sum calib_actifs.txt fragment_analyse.json ) > "$T/$passe.sommes" &&
    mv "$T/$passe.sommes" "$T/$passe/SHA256SUMS"; } 2> /dev/null ||
    refus CA/sortie "passe $passe : SHA256SUMS impossible" 5
done
if ! cmp -s "$T/A/SHA256SUMS" "$T/B/SHA256SUMS"; then
  echo "REFUS CA/identite : SHA256SUMS des passes A et B différents (A puis B ci-dessous)" >&2
  cat "$T/A/SHA256SUMS" "$T/B/SHA256SUMS"
  exit 5
fi
{ mkdir -p "$S" && cp "$T/A/calib_actifs.txt" "$T/A/fragment_analyse.json" "$B/manifeste.tsv" "$S/" &&
  ( cd "$S" && sha256sum calib_actifs.txt fragment_analyse.json manifeste.tsv > SHA256SUMS ); } 2> /dev/null ||
  refus CA/sortie "copie de la passe A impossible" 5
cat "$S/SHA256SUMS"
exit 0
