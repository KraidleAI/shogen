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
#   le commit en préparation (suppressions exclues) ; --tree : tous les fichiers suivis.
#   Lancement ramené à la racine du dépôt, quel que soit le dossier courant.
#   Objets réels, ceux que la poussée transmet : objets de remplacement (refs/replace) ignorés.
# HORS PORTÉE, déclaré : fichiers de garde (enforcement/gate-*, enforcement/lint-*) et
#   enforcement/tests/, dans tous les modes (ils nomment leurs motifs ; avis à chaque lancement ;
#   le reste d'enforcement/ est balayé) ; liens symboliques (120000) et gitlinks (160000),
#   ignorés avec un avis ; secret coupé sur deux lignes ; formats nouveaux ; entropie. Aucun
#   scanner dédié ne tourne dans Shōgen (items SHOGEN-SECRETS-SCANNER-DEDIE-1 et
#   SHOGEN-FORGE-SECRET-SCANNING-1) : ce plancher n'a aucun filet derrière lui.
# ÉCHEC FERMÉ (sortie 2) : erreur git, hors d'un dépôt, échec de mktemp, exclusion refusée,
#   argument inconnu (écart au blob, où un argument inconnu retombait sur le mode indexé).
# SORTIE MASQUÉE PAR CONSTRUCTION : aucun octet de contenu n'est dirigé vers la sortie ; seuls
#   le chemin et la ligne que la gate calcule ; troncature annoncée.
#   Chemin en forme d'identifiant : masqué dans les constats et les avis non-blob, en clair dans
#   les messages d'exclusion et d'échec (item SHOGEN-SECRETS-MASQUE-EXCLUSION-1).
# Amont : versions 1 à 4 rejetées en revue G2 dans VibeGates (ADR-0004 de VibeGates,
#   docs/adr/ADR-0004-guard-escalation-adjudication.md ; VibeGates docs/passes/pass-4-report.md,
#   section U2, commit 1263f2a).
# Remèdes : vrai secret : le révoquer (le retirer ne suffit pas) ; fixture : pathspec avec un
#   marqueur ADR- dans .vibegates-secretscan-exclude (marqueur d'attribution, non contrôlé comme
#   référence ; fichier SUIVI ; formes globales refusées ; chaque exclusion annoncée avec son
#   compte : règles de l'ADR-0004 de VibeGates) ; valeur factice : la sortir de la forme.
# Usage : gate-secrets.sh [--tree]   Sortie : 0 propre, 2 blocage. Jetons ASCII sur stderr :
#   SECRETS/forme, SECRETS/exclusion, SECRETS/echec.

set -u
export LC_ALL=C   # grep, awk, sed et tr en octets ASCII, sous Git Bash comme sur l'image (CH-8)
export GIT_NO_REPLACE_OBJECTS=1   # objets réels, ceux que la poussée transmet : refs/replace ignorées (G2 C-G2-2)
unset GIT_LITERAL_PATHSPECS GIT_GLOB_PATHSPECS GIT_NOGLOB_PATHSPECS GIT_ICASE_PATHSPECS   # pathspecs du contrat lus tels qu'écrits (G2 C-G2-9)
MODE="${1-}"
EXCL_FILE=".vibegates-secretscan-exclude"

refus() { echo "REFUS (SECRETS/$1) : $2" >&2; exit 2; }
echec() { refus echec "le balayage ne peut pas tourner : $1 ; échec fermé"; }
case "$#:$MODE" in 0:|1:--tree) ;; *) echec "argument inconnu ; usage : gate-secrets.sh [--tree]" ;; esac
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echec "hors d'un arbre de travail git"
TOP="$(git rev-parse --show-toplevel 2>/dev/null)" && [ -n "$TOP" ] || echec "racine du dépôt introuvable"
cd "$TOP" || echec "cd vers la racine du dépôt impossible"

VENDOR='AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}|xox[baprs]-[0-9A-Za-z-]{10,}|sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{35}|eyJhbGciOi[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]{10,}'
GENERIC='(api[_-]?key|secret|passwd|password|token)[[:space:]]*[:=][[:space:]]*["'"'"'][A-Za-z0-9+/_-]{16,}["'"'"']|(api[_-]?key|secret|passwd|password|token|aws_[a-z_]*key[a-z_]*)=[A-Za-z0-9+/]{16,}'

masque() { sed -E "s#$VENDOR#[forme masquée]#g; s#$GENERIC#[forme masquée]#gI"; }   # chemin en forme d'identifiant : masqué dans les constats et les avis non-blob (CH-14)
EXCLUDES=()
if [ -f "$EXCL_FILE" ]; then
  git ls-files --error-unmatch -- "$EXCL_FILE" >/dev/null 2>&1 ||
    refus exclusion "$EXCL_FILE existe sans être suivi (une exclusion non suivie n'atteint jamais la revue)"
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    printf '%s' "$line" | grep -q 'ADR-' || refus exclusion "entrée de $EXCL_FILE sans marqueur ADR- (R-23) : $line"
    p="${line%% #*}"; p="${p%"${p##*[![:space:]]}"}"
    [ -z "$p" ] && continue
    pn="$(printf '%s' "$p" | sed 's|//*|/|g; s|/$||')"   # normalisation : // réduits, / final retiré
    case "$pn" in .|\*|\*\*|'') refus exclusion "pathspec global '$p' refusé" ;; esac
    case "$pn" in *..*) refus exclusion "pathspec traversant '$p' refusé" ;; esac
    git ls-files -- ":(exclude)$p" >/dev/null 2>&1 || refus exclusion "pathspec inutilisable '$p' dans $EXCL_FILE"
    NREM=$(git ls-files -- "$p" 2>/dev/null | wc -l); NTOT=$(git ls-files | wc -l)
    [ "$NREM" -ge "$NTOT" ] && [ "$NTOT" -gt 0 ] && refus exclusion "l'exclusion '$p' retirerait toute la portée"
    echo "AVIS (secrets) : l'exclusion '$p' retire $NREM fichier(s) suivi(s) de la portée ($EXCL_FILE)." >&2
    EXCLUDES+=(":(exclude)$p")
  done < "$EXCL_FILE"
fi
echo "AVIS (secrets) : fichiers de garde (enforcement/gate-*, enforcement/lint-*) et enforcement/tests/ exclus par contrat (ils nomment leurs motifs) ; le reste d'enforcement/ est balayé." >&2

TMP="$(mktemp)" && [ -n "$TMP" ] && [ -w "$TMP" ] || echec "mktemp a échoué"
trap 'rm -f "$TMP"' EXIT
PS=(-- . ':(exclude)enforcement/gate-*' ':(exclude)enforcement/lint-*' ':(exclude)enforcement/tests/' ${EXCLUDES[@]+"${EXCLUDES[@]}"})
if [ "$MODE" = --tree ]; then
  git ls-files -z "${PS[@]}" >"$TMP" 2>/dev/null || echec "erreur git (liste des fichiers)"
else
  git diff --cached --name-only -z --diff-filter=d "${PS[@]}" >"$TMP" 2>/dev/null || echec "erreur git (liste des fichiers)"
fi

FOUND=0; NF=0
while IFS= read -r -d '' f; do
  m="$(git ls-files -s -- ":(literal)$f" 2>/dev/null | awk '{print $1; exit}')"
  case "$m" in
    120000|160000) echo "AVIS (secrets) : '$f' ignoré, entrée non-blob (mode $m, hors portée du contrat)." | masque >&2; continue ;;
  esac
  git show ":$f" >/dev/null 2>&1 || echec "git show a échoué pour '$f'"
  NF=$((NF + 1))
  # Octets, NUL retirés : un NUL ne coupe pas le balayage ; l'UTF-16 devient lisible.
  LNS="$(git show ":$f" 2>/dev/null | tr -d '\000' | { grep -anE "$VENDOR"; git show ":$f" 2>/dev/null | tr -d '\000' | grep -aniE "$GENERIC"; } | cut -d: -f1 | sort -un || true)"
  if [ -n "$LNS" ]; then
    [ "$FOUND" -eq 0 ] && echo "REFUS (SECRETS/forme) : contenu en forme d'identifiant (sortie masquée par construction ; inspecter en local les lignes nommées) :" >&2
    FOUND=1
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
