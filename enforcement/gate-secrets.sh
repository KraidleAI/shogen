#!/usr/bin/env bash
# Shōgen, gate G3 des secrets : plancher de motifs sur le contenu suivi. Lot D8b (ADR-0028 D8 ;
# G0 docs/adr-0028/G0-lot-D8b.md ; journal docs/G1-lot-D8b.md). Portée depuis le blob 6789a30
# (adb2213:enforcement/gate-secrets.sh, soit VibeGates enforcement/gate-secrets.sh au commit
# 1eb1b33, HEAD amont 1263f2a). Cas : enforcement/tests/run-fixtures-secrets.sh, conçu d'après
# le runner amont (blob 7960238) ; un constat hors de ces cas est une proposition de changement
# du contrat (R-23).
# PORTÉE : blobs réguliers (100644, 100755) connus de git, lus dans l'index comme des OCTETS,
#   octets NUL retirés : un NUL ne coupe pas le balayage, l'UTF-16 devient lisible, une forme
#   dans un binaire bloque. Sans argument : contenu indexé ENTIER de chaque fichier touché par
#   le commit en préparation (suppressions exclues) ; --tree : tous les fichiers suivis ;
#   --history (fonction neuve, absente du blob) : lignes ajoutées de tout l'historique atteint
#   depuis les refs et les HEAD des arbres de travail (--all), en un seul flux git log -p aux
#   drapeaux forcés contre la config locale ; verdict par grep seul, attribution par awk pour
#   le message seulement. Lancement ramené à la racine du dépôt, quel que soit le dossier courant.
#   Objets réels, ceux que la poussée transmet : objets de remplacement (refs/replace) ignorés.
#   Lot D8d (2026-10-04, SHOGEN-D8D-SECRETS-1) : modes indexé et arbre, noms de chemin de la
#   portée balayés, toute entrée comprise ; entrée lue à l'étage 0 nommé (":0:<chemin>") ;
#   --history, messages de commit et de tag annoté (chaque niveau d'un tag imbriqué), et objets
#   des refs vers un blob ou un arbre ; --hors-refs, objets que les refs n'atteignent pas
#   (inatteignables, des seuls journaux de refs), comptes seuls ; un bundle de custodie se balaie
#   dans son clone non nu, par --history.
# HORS PORTÉE, déclaré : fichiers de garde (enforcement/gate-*, enforcement/lint-*) et
#   enforcement/tests/, dans tous les modes (ils nomment leurs motifs ; avis à chaque lancement ;
#   le reste d'enforcement/ est balayé) ; contenu des liens symboliques (120000) et des gitlinks
#   (160000), ignoré avec un avis ; secret coupé sur deux lignes ; formats nouveaux ; entropie. Aucun
#   scanner dédié ne tourne dans Shōgen (items SHOGEN-SECRETS-SCANNER-DEDIE-1 et
#   SHOGEN-FORGE-SECRET-SCANNING-1) : ce plancher n'a aucun filet derrière lui.
# ÉCHEC FERMÉ (sortie 2) : erreur git, hors d'un dépôt, échec de mktemp, exclusion refusée,
#   argument inconnu (écart au blob, où un argument inconnu retombait sur le mode indexé),
#   historique superficiel ou greffé (info/grafts, GIT_GRAFT_FILE) en --history et en
#   --hors-refs ; grep sorti au-delà de 1 (D8d).
# SORTIE MASQUÉE PAR CONSTRUCTION : aucun octet de contenu n'est dirigé vers la sortie ; seuls
#   le chemin, la ligne et, en historique, le commit que la gate calcule ; troncature annoncée.
#   Chemin ou pathspec en forme d'identifiant : masqué partout, constats, avis, messages
#   d'exclusion, des greffes et d'échec compris (lot D8d).
# Amont : versions 1 à 4 rejetées en revue G2 dans VibeGates (ADR-0004 de VibeGates,
#   docs/adr/ADR-0004-guard-escalation-adjudication.md ; VibeGates docs/passes/pass-4-report.md,
#   section U2, commit 1263f2a).
# Remèdes : vrai secret : le révoquer (le retirer ne suffit pas) ; fixture : pathspec avec un
#   marqueur ADR- dans .vibegates-secretscan-exclude (marqueur d'attribution, non contrôlé comme
#   référence ; fichier SUIVI ; formes globales refusées ; chaque exclusion annoncée avec son
#   compte : règles de l'ADR-0004 de VibeGates) ; valeur factice : la sortir de la forme.
# Usage : gate-secrets.sh [--tree|--history|--hors-refs]   Sortie : 0 propre, 2 blocage. Jetons
#   ASCII sur stderr : SECRETS/forme, SECRETS/historique, SECRETS/hors-refs, SECRETS/exclusion,
#   SECRETS/tronque (historique superficiel ou greffé), SECRETS/echec.

set -u
export LC_ALL=C   # grep, awk, sed et tr en octets ASCII, sous Git Bash comme sur l'image (CH-8)
export GIT_NO_REPLACE_OBJECTS=1   # objets réels, ceux que la poussée transmet : refs/replace ignorées (G2 C-G2-2)
unset GIT_LITERAL_PATHSPECS GIT_GLOB_PATHSPECS GIT_NOGLOB_PATHSPECS GIT_ICASE_PATHSPECS   # pathspecs du contrat lus tels qu'écrits (G2 C-G2-9)
MODE="${1-}"
EXCL_FILE=".vibegates-secretscan-exclude"

refus() { echo "REFUS (SECRETS/$1) : $2" >&2; exit 2; }
echec() { refus echec "le balayage ne peut pas tourner : $1 ; échec fermé"; }
case "$#:$MODE" in 0:|1:--tree|1:--history|1:--hors-refs) ;; *) echec "argument inconnu ; usage : gate-secrets.sh [--tree|--history|--hors-refs]" ;; esac
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echec "hors d'un arbre de travail git"
TOP="$(git rev-parse --show-toplevel 2>/dev/null)" && [ -n "$TOP" ] || echec "racine du dépôt introuvable"
cd "$TOP" || echec "cd vers la racine du dépôt impossible"

VENDOR='AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}|xox[baprs]-[0-9A-Za-z-]{10,}|sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{35}|eyJhbGciOi[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]{10,}'
GENERIC='(api[_-]?key|secret|passwd|password|token)[[:space:]]*[:=][[:space:]]*["'"'"'][A-Za-z0-9+/_-]{16,}["'"'"']|(api[_-]?key|secret|passwd|password|token|aws_[a-z_]*key[a-z_]*)=[A-Za-z0-9+/]{16,}'

masque() { sed -E "s#$VENDOR#[forme masquée]#g; s#$GENERIC#[forme masquée]#gI"; }   # tout chemin ou pathspec imprimé passe par masque (CH-14 ; I-G2-4, lot D8d)
mq() { printf '%s' "$1" | masque; }
# formes <préfixe> <fichier> : numéros des lignes qui portent une forme (VENDOR, ou GENERIC sans casse) après le préfixe,
#   triés ; sortie 2 si un grep sort au-delà de 1 : une erreur de grep n'est jamais un vert (I-G2-2, lot D8d).
formes() { local v g; v="$( set -o pipefail; grep -anE "$1($VENDOR)" "$2" | cut -d: -f1 )"; [ $? -le 1 ] || return 2
  g="$( set -o pipefail; grep -aniE "$1($GENERIC)" "$2" | cut -d: -f1 )"; [ $? -le 1 ] || return 2
  printf '%s\n%s\n' "$v" "$g" | sed '/^$/d' | sort -un; }
EXCLUDES=()
if [ -f "$EXCL_FILE" ]; then
  git ls-files --error-unmatch -- "$EXCL_FILE" >/dev/null 2>&1 ||
    refus exclusion "$EXCL_FILE existe sans être suivi (une exclusion non suivie n'atteint jamais la revue)"
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    printf '%s' "$line" | grep -q 'ADR-' || refus exclusion "$(mq "entrée de $EXCL_FILE sans marqueur ADR- (R-23) : $line")"
    p="${line%% #*}"; p="${p%"${p##*[![:space:]]}"}"
    [ -z "$p" ] && continue
    pn="$(printf '%s' "$p" | sed 's|//*|/|g; s|/$||')"   # normalisation : // réduits, / final retiré
    case "$pn" in .|\*|\*\*|'') refus exclusion "$(mq "pathspec global '$p' refusé")" ;; esac
    case "$pn" in *..*) refus exclusion "$(mq "pathspec traversant '$p' refusé")" ;; esac
    git ls-files -- ":(exclude)$p" >/dev/null 2>&1 || refus exclusion "$(mq "pathspec inutilisable '$p' dans $EXCL_FILE")"
    NREM=$(git ls-files -- "$p" 2>/dev/null | wc -l); NTOT=$(git ls-files | wc -l)
    [ "$NREM" -ge "$NTOT" ] && [ "$NTOT" -gt 0 ] && refus exclusion "$(mq "l'exclusion '$p' retirerait toute la portée")"
    echo "AVIS (secrets) : l'exclusion '$p' retire $NREM fichier(s) suivi(s) de la portée ($EXCL_FILE)." | masque >&2
    EXCLUDES+=(":(exclude)$p")
  done < "$EXCL_FILE"
fi
[ "$MODE" = --hors-refs ] || echo "AVIS (secrets) : fichiers de garde (enforcement/gate-*, enforcement/lint-*) et enforcement/tests/ exclus par contrat (ils nomment leurs motifs) ; le reste d'enforcement/ est balayé." >&2

T="$(mktemp -d)" && [ -n "$T" ] && [ -d "$T" ] && [ -w "$T" ] || echec "mktemp a échoué"
trap 'rm -rf "$T"' EXIT
TMP="$T/l"; C="$T/c"   # liste ou flux ; contenu d'un fichier, ou liste des noms
PS=(-- . ':(exclude)enforcement/gate-*' ':(exclude)enforcement/lint-*' ':(exclude)enforcement/tests/' ${EXCLUDES[@]+"${EXCLUDES[@]}"})
if [ "$MODE" = --history ] || [ "$MODE" = --hors-refs ]; then
  [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" = false ] ||
    refus tronque "historique superficiel ou illisible : le balayage exige tout l'historique (fetch-depth: 0 en CI)"
  GF="$(git rev-parse --git-path info/grafts 2>/dev/null)" && [ -n "$GF" ] || echec "erreur git (greffes)"
  [ ! -e "$GF" ] || refus tronque "$(mq "greffes ($GF) : l'historique affiché n'est pas celui des objets")"
fi
if [ "$MODE" = --hors-refs ]; then
  # Objets que les refs n'atteignent pas (inatteignables, ou des seuls journaux de refs) : mêmes motifs, comptes seuls
  # (SHOGEN-SECRETS-HORS-REFS-1) ; un bundle se balaie dans son clone non nu, par --history.
  ( set -o pipefail; git cat-file --batch-all-objects --batch-check='%(objectname)' ) > "$T/a" &&
    ( set -o pipefail; git rev-list --objects --all | cut -d' ' -f1 | sort -u ) > "$T/b" || echec "erreur git (objets)"
  comm -23 "$T/a" "$T/b" > "$T/h" && ( set -o pipefail; git cat-file --batch < "$T/h" | tr -d '\000' ) > "$C" || echec "erreur git (objets hors refs)"
  N="$(formes '' "$C")" || echec "grep a échoué (hors refs) ; un vert serait faux"
  NH=$(wc -l < "$T/h"); NA=$(wc -l < "$T/a")
  [ -z "$N" ] && { echo "OK (secrets) : hors refs, $NH objet(s) hors refs sur $NA, sans forme d'identifiant (objets sans chemin : exclusions sans effet)."; exit 0; }
  echo "REFUS (SECRETS/hors-refs) : $(printf '%s\n' "$N" | wc -l) ligne(s) en forme d'identifiant dans $NH objet(s) hors refs sur $NA (comptes seuls ; objets sans chemin : exclusions sans effet)." >&2
  echo "Remèdes : vrai secret : le révoquer ; puis, sur décision, expirer les journaux de refs et élaguer (git reflog expire, git gc --prune) avant toute copie brute de .git." >&2
  exit 2
fi
if [ "$MODE" = --history ]; then
  # Refs vers un blob ou un arbre, directes ou par un tag : objets balayés par les mêmes motifs au lieu du refus (Q-C-2) ;
  # arbre : noms et blobs réguliers, exclusions du contrat comprises (diff-tree contre l'arbre vide ; git archive lirait export-ignore).
  E="$(git hash-object -t tree /dev/null)" && ( set -o pipefail; git for-each-ref --format='%(objecttype) %(*objecttype) %(refname)' |
    awk '$1 != "commit" && !($1 == "tag" && $2 == "commit") { print $NF }' ) > "$T/r" || echec "erreur git (refs)"
  REFO=
  while IFS= read -r r; do
    o="$(git rev-parse --verify -q "$r^{}")" && ty="$(git cat-file -t "$o")" || echec "$(mq "erreur git (objet de $r)")"
    ( set -o pipefail; if [ "$ty" = blob ]; then git cat-file blob "$o"; else git diff-tree -r -z --no-renames --raw "$E" "$o" "${PS[@]}" |
      while IFS= read -r -d '' x && IFS= read -r -d '' p; do set -- $x; printf '%s\n' "$p"; [ "$2" != 100644 ] && [ "$2" != 100755 ] || git cat-file blob "$4" || exit 1; done
      fi | tr -d '\000' ) > "$C" || echec "$(mq "erreur git (objet de $r)")"
    N="$(formes '' "$C")" || echec "grep a échoué (refs) ; un vert serait faux"
    [ -z "$N" ] || REFO="$REFO$r:(objet)"$'\n'
  done < "$T/r"
  # Messages de commit (--all) et de tag annoté (ref vers un objet tag ; tag imbriqué : chaque niveau), chaque ligne indentée
  # de quatre espaces sous son en-tête « commit » ou « tag » : mêmes motifs, attribution à l'objet (SHOGEN-SECRETS-MESSAGES-1).
  ( set -o pipefail; { git --no-optional-locks -c color.ui=never -c i18n.logOutputEncoding=UTF-8 log --all --no-color --no-notes \
    --no-show-signature --format='commit %H%n%w(0,4,4)%B' && git for-each-ref --format='%(objecttype) %(refname)' | awk '$1 == "tag" { print $2 }' |
    while IFS= read -r t; do printf 'tag %s\n' "$t"; o="$t"; while y="$(git cat-file -t "$o")" || exit 1; [ "$y" = tag ]; do
      git cat-file tag "$o" | sed -e '1,/^$/d' -e 's/^/    /' || exit 1; o="$(git cat-file tag "$o" | sed -n '1s/^object //p')" || exit 1
    done; done; } | tr -d '\000' ) > "$T/m" || echec "erreur git (messages)"
  MSG="$(formes '^    .*' "$T/m")" || echec "grep a échoué (messages) ; un vert serait faux"
  NC="$(git rev-list --count --all 2>/dev/null)" || echec "erreur git (compte des commits)"
  # Un seul flux ; drapeaux forcés contre la config locale ; NUL retirés ; verdict par grep seul (CH-2 du G0).
  ( set -o pipefail; git --no-optional-locks -c core.quotePath=false -c log.showRoot=true -c color.ui=never \
    -c diff.noprefix=false -c diff.mnemonicPrefix=false -c diff.dstPrefix=b/ -c diff.suppressBlankEmpty=false log -p --text --no-color \
    --no-ext-diff --no-textconv --no-renames --diff-merges=first-parent --full-history --no-notes --no-show-signature \
    --format='commit %H' --all "${PS[@]}" 2>/dev/null | tr -d '\000' ) >"$TMP" || echec "erreur git (historique)"
  HITS="$(formes '^\+.*' "$TMP")" || echec "grep a échoué (historique) ; un vert serait faux"
  [ -z "$HITS$MSG$REFO" ] && { echo "OK (secrets) : historique, $NC commit(s) (--all), sans forme d'identifiant ajoutée (lignes, messages, objets des refs non-commit)."; exit 0; }
  if [ -n "$HITS" ]; then
  echo "REFUS (SECRETS/historique) : $(printf '%s\n' "$HITS" | wc -l) ligne(s) ajoutée(s) en forme d'identifiant (sortie masquée ; 20 au plus, commit:chemin:ligne) :" >&2
  # Attribution, pour le message seulement : en-têtes commit, +++ hors hunk, compteurs des @@ (ligne vide = contexte).
  printf '%s\n' "$HITS" | head -20 | awk 'NR == FNR { h[$1] = 1; next }
    !o && !m && /^commit / { c = substr($2, 1, 12); next }
    !o && !m && /^\+\+\+ / { p = substr($0, 5); sub(/^b\//, "", p); sub(/\t$/, "", p); if (FNR in h) print c ":" p ":(chemin)"; next }
    !o && !m && /^@@ -/ { split($2, x, ","); split($3, y, ","); o = (x[2] == "") ? 1 : x[2] + 0; m = (y[2] == "") ? 1 : y[2] + 0; l = substr(y[1], 2) + 0; next }
    o || m { t = substr($0, 1, 1); if (t == "+") { if (FNR in h) print c ":" p ":" l; l++; m-- } else if (t == "-") o--; else if (t == " " || t == "") { l++; o--; m-- } }' - "$TMP" | masque >&2
  fi
  if [ -n "$MSG" ]; then
    echo "REFUS (SECRETS/historique) : $(printf '%s\n' "$MSG" | wc -l) ligne(s) de message (commit ou tag annoté) en forme d'identifiant (sortie masquée ; 20 au plus, objet:(message)) :" >&2
    printf '%s\n' "$MSG" | head -20 | awk 'NR == FNR { h[$1] = 1; next } /^commit / { c = substr($2, 1, 12); next } /^tag / { c = substr($0, 5); next }
      (FNR in h) && !(c in v) { v[c] = 1; print c ":(message)" }' - "$T/m" | masque >&2
  fi
  [ -z "$REFO" ] || { echo "REFUS (SECRETS/historique) : ref(s) vers un blob ou un arbre en forme d'identifiant (sortie masquée, ref:(objet)) :" >&2; printf '%s' "$REFO" | masque >&2; }
  echo "Remèdes : vrai secret : le révoquer (l'historique n'est pas réécrit, ADR-0028 D7 : item SHOGEN-SECRETS-REVOQUE-1) ; fixture : pathspec avec marqueur ADR- dans $EXCL_FILE." >&2
  exit 2
fi
if [ "$MODE" = --tree ]; then
  git ls-files -z "${PS[@]}" >"$TMP" 2>/dev/null || echec "erreur git (liste des fichiers)"
else
  git diff --cached --name-only -z --diff-filter=d "${PS[@]}" >"$TMP" 2>/dev/null || echec "erreur git (liste des fichiers)"
fi

FOUND=0; NF=0; HC=0
# Noms de chemin de la portée, toute entrée comprise (I-G2-3, lot D8d) ; un nom coupé par un saut de ligne n'échappe pas
# au verdict, seule son attribution, pour le message, en pâtit.
tr '\000' '\n' < "$TMP" > "$C" && NOMS="$(formes '' "$C")" || echec "grep a échoué (noms de chemin) ; un vert serait faux"
if [ -n "$NOMS" ]; then
  FOUND=1; echo "REFUS (SECRETS/forme) : nom de chemin en forme d'identifiant (sortie masquée ; 8 au plus) :" >&2
  printf '%s\n' "$NOMS" | head -8 | while IFS= read -r n; do sed -n "${n}s/\$/:(chemin)/p" "$C"; done | masque >&2
fi
while IFS= read -r -d '' f; do
  m="$(git ls-files -s -- ":(literal)$f" 2>/dev/null | awk '{print $1; exit}')"
  case "$m" in
    120000|160000) echo "AVIS (secrets) : '$f' ignoré, entrée non-blob (mode $m, hors portée du contrat)." | masque >&2; continue ;;
  esac
  # ":0:" nomme l'étage 0 : un chemin « 0:x » est lu tel quel, jamais comme l'étage 0 de « x » (I-G2-1, lot D8d).
  ( set -o pipefail; git show ":0:$f" 2>/dev/null | tr -d '\000' ) > "$C" || echec "$(mq "git show a échoué pour '$f'")"
  NF=$((NF + 1))
  # Octets, NUL retirés : un NUL ne coupe pas le balayage ; l'UTF-16 devient lisible.
  LNS="$(formes '' "$C")" || echec "grep a échoué (contenu) ; un vert serait faux"
  if [ -n "$LNS" ]; then
    [ "$HC" -eq 0 ] && echo "REFUS (SECRETS/forme) : contenu en forme d'identifiant (sortie masquée par construction ; inspecter en local les lignes nommées) :" >&2
    FOUND=1; HC=1
    N=$(printf '%s\n' "$LNS" | wc -l)
    { printf '%s\n' "$LNS" | head -8 | while IFS= read -r ln; do printf '%s:%s: [contenu masqué]\n' "$f" "$ln"; done
      [ "$N" -gt 8 ] && printf '%s : (+%d ligne(s) non listée(s))\n' "$f" "$((N - 8))"; } | masque >&2
  fi
done <"$TMP"

if [ "$FOUND" -ne 0 ]; then
  echo "Remèdes : vrai secret : le révoquer (le retirer ne suffit pas) ; fixture : pathspec avec marqueur ADR- dans $EXCL_FILE ; valeur factice : la sortir de la forme d'identifiant." >&2
  exit 2
fi
echo "OK (secrets) : $NF fichier(s) sans forme d'identifiant dans la portée."
exit 0
