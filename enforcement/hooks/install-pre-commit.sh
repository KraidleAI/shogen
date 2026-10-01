#!/usr/bin/env bash
# Shōgen, installeur du hook pre-commit versionné : lot D8c d'ADR-0028 D8 (G0 docs/adr-0028/G0-lot-D8c.md,
# CH-5 et CH-6 ; journal docs/G1-lot-D8c.md). Copie le blob COMMITTÉ enforcement/hooks/pre-commit, jamais
# le fichier de l'arbre de travail, dans le dossier des hooks du dépôt, si son sha256 égale ATTENDU.
# Hook déjà présent : égal à ATTENDU, rien n'est écrit ; d'empreinte connue (CONNUS), sauvegardé en
# pre-commit.<12 premiers caractères de son sha256> puis remplacé ; inconnu, refusé sans rien écrire.
# La copie est contrôlée après écriture. --verifier : lecture seule, 0 si le hook installé égale ATTENDU.
# Refus préalables, dans les deux modes : argument inconnu ; GIT_DIR, GIT_WORK_TREE ou GIT_INDEX_FILE
# posées ; hors d'un dépôt ; arbre lié (les hooks sont partagés : lancé d'un worktree, l'installeur
# écrirait dans le dossier du dépôt principal) ; core.hooksPath posé ; installeur différent de son blob
# committé ; blob committé du hook différent d'ATTENDU. Contrôle d'empreintes, pas de l'hôte (T-11).
# Tout changement du hook change ATTENDU dans le même commit (cas I-10). Sur F:/Shogen, l'installation
# est un acte de l'orchestrateur, après le G7 du lot (G0 CH-6).
# Usage : install-pre-commit.sh [--verifier]   Sortie : 0 installé ou conforme ; 2 refus (stderr).

set -u
ATTENDU='b8705ae822acab458e3ae50c32b0e9fce4e6ba873845673fe5555c7edcbe6198'
CONNUS='1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d'   # hook local, blob 9c4c846
refus() { echo "REFUS (HOOK/installation) : $1" >&2; exit 2; }
sha() { sha256sum < "$1" | cut -d' ' -f1; }
case "$#:${1-}" in 0:|1:--verifier) ;; *) refus "argument inconnu ; usage : install-pre-commit.sh [--verifier]" ;; esac
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; do [ -z "${!v+x}" ] || refus "$v posée : lancer sans variable GIT_* de dépôt"; done
MOI="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")" && [ -f "$MOI" ] || refus "chemin de l'installeur introuvable"
G="$(git rev-parse --path-format=absolute --git-dir 2>/dev/null)" && C="$(git rev-parse --path-format=absolute --git-common-dir)" &&
  HD="$(git rev-parse --path-format=absolute --git-path hooks)" && [ -n "$G" ] && [ -n "$HD" ] || refus "hors d'un dépôt git"
[ "$G" = "$C" ] || refus "arbre lié : les hooks sont partagés ; installer depuis l'arbre principal ($C)"
git config --get core.hooksPath >/dev/null; [ $? -eq 1 ] || refus "core.hooksPath posé ou illisible : git n'exécuterait pas $HD/pre-commit"
[ "$(sha "$MOI")" = "$(git show HEAD:enforcement/hooks/install-pre-commit.sh 2>/dev/null | sha256sum | cut -d' ' -f1)" ] ||
  refus "installeur différent de son blob committé (HEAD) : committer, ou reprendre le fichier de HEAD"
S="$(git show HEAD:enforcement/hooks/pre-commit 2>/dev/null | sha256sum | cut -d' ' -f1)"
[ "$S" = "$ATTENDU" ] || refus "blob committé du hook ($S) différent d'ATTENDU ($ATTENDU)"
D="$HD/pre-commit"; AV=absent; SV=
if [ "${1-}" = --verifier ]; then
  [ -f "$D" ] || refus "aucun hook installé ($D)"
  AV="$(sha "$D")"; [ "$AV" = "$ATTENDU" ] || refus "hook installé ($AV) différent d'ATTENDU ($ATTENDU)"
  echo "OK (installation) : hook installé conforme ($AV)"; exit 0
fi
if [ -e "$D" ]; then
  AV="$(sha "$D")"
  [ "$AV" = "$ATTENDU" ] && { echo "OK (installation) : déjà conforme ($AV) ; rien écrit"; exit 0; }
  case " $CONNUS " in *" $AV "*) ;; *) refus "hook présent d'empreinte inconnue ($AV) : examen manuel ; rien écrit" ;; esac
  SV="$D.${AV:0:12}"
  if [ -e "$SV" ]; then [ "$(sha "$SV")" = "$AV" ] || refus "sauvegarde $SV présente et différente ; rien écrit"
  else cp "$D" "$SV" && [ "$(sha "$SV")" = "$AV" ] || refus "sauvegarde $SV impossible"; fi
fi
T="$(mktemp "$HD/pre-commit.XXXXXX")" || refus "mktemp dans $HD impossible"
git show HEAD:enforcement/hooks/pre-commit > "$T" 2>/dev/null && [ "$(sha "$T")" = "$ATTENDU" ] && chmod 755 "$T" &&
  mv -f "$T" "$D" || { rm -f "$T"; refus "copie vers $D impossible"; }
AP="$(sha "$D")"; [ "$AP" = "$ATTENDU" ] || refus "hook installé ($AP) différent d'ATTENDU après copie"
echo "OK (installation) : $D ; avant $AV ; après $AP${SV:+ ; sauvegarde $SV}"
exit 0
