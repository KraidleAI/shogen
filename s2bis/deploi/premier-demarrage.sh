#!/bin/bash
# Shōgen S2-bis, DEPLOI-BIS, script I : premier démarrage d'un observateur (ADR-0029 §2.9 l.243-245 ; G0
# docs/adr-0029/g0-collecte/ : PROPOSITION §4.1 et §4.2, E-D-01 à E-D-05 et E-D-12 ; décisions 1 à 5 de DB-0).
# Un seul script pour les quatre observateurs, collé dans la console du fournisseur (cloud-init, lancé par root) ou
# lancé à la main par root (OVHcloud, décision 5) ; rempli, il tient sous 32 KiB (borne Hetzner, décision 5).
# Mode d'essai (T-DP-1) : bash premier-demarrage.sh --essai <racine factice>. Sans privilège ni réseau : les fichiers
# s'écrivent sous la racine factice (refusée sans <racine>/essai.getent, résolution factice que getent y lit) ;
# apt-get, systemctl, useradd, chown, nft et sshd y sont des enregistreurs (<racine>/essai.commandes).

# Paramètres d'observateur (E-D-01) : collés par l'investisseur avant le lancement, jamais versés au dépôt.
OBSERVATEUR=""            # o1, o2, o3 ou o4
FOURNISSEUR=""            # minuscules, chiffres, tirets : hetzner, ovhcloud, digitalocean, linode
REGION=""                 # région du fournisseur : hel1, gra, ams3, sg-sin-2
FAMILLE_RESOLVEUR=""      # unbound (O1), quad9 (O2), google (O3) ou fournisseur (O4)
RESOLVEUR_FOURNISSEUR=""  # famille fournisseur seule : 1 à 4 adresses IPv4 séparées par une espace
ADRESSE_SURVEILLANCE=""   # adresse https du signal de vie (Healthchecks), secrète
ADRESSE_SAUVEGARDE=""     # sous-compte de l'espace de sauvegarde : compte@hôte
CLE_INTERVENTION=""       # clé publique ssh-ed25519 de l'investisseur, sur une ligne

set -euo pipefail
umask 022
export LC_ALL=C DEBIAN_FRONTEND=noninteractive PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
R=""
if [ "$#" -eq 2 ] && [ "$1" = --essai ]; then
    R="$(cd "$2" && pwd -P)" || R=""
    [ "$R" != / ] && [ -f "$R/essai.getent" ] || { echo "premier-demarrage : ESSAI/racine refusée" >&2; exit 2; }
    enregistrer() { echo "$*" >> "$R/essai.commandes"; }
    apt-get() { enregistrer apt-get "$@"; }
    systemctl() { enregistrer systemctl "$@"; }
    useradd() { enregistrer useradd "$@"; }
    chown() { enregistrer chown "$@"; }
    nft() { enregistrer nft "$@"; }
    sshd() { enregistrer sshd "$@"; }
    getent() {
        enregistrer getent "$@"
        awk -v b="$1" -v k="$2" '$1 == b && $2 == k { print $3; t = 1 } END { exit t ? 0 : 2 }' "$R/essai.getent"
    }
elif [ "$#" -ne 0 ] || [ "$(id -u)" -ne 0 ]; then
    echo "premier-demarrage : usage : root, sans argument ; ou --essai <racine factice>" >&2
    exit 2
fi

refuser() { echo "premier-demarrage : PARAMETRE/$1 : $2" >&2; exit 2; }
verifier_parametres() {     # E-D-01 : tout est contrôlé avant le premier changement ; refus et arrêt sinon
    local ip4='[0-9]{1,3}([.][0-9]{1,3}){3}' cle='^ssh-ed25519 [A-Za-z0-9+/]+={0,2}( [A-Za-z0-9@._-]+)?$'
    local liste="^$ip4( $ip4){0,3}$" https='^https://[a-z0-9.-]+(/[A-Za-z0-9._-]+)+$' nom='^[a-z0-9-]{1,32}$'
    [[ $OBSERVATEUR =~ ^o[1-4]$ ]] || refuser OBSERVATEUR "o1 à o4"
    [[ $FOURNISSEUR =~ $nom ]] || refuser FOURNISSEUR "minuscules, chiffres, tirets"
    [[ $REGION =~ $nom ]] || refuser REGION "minuscules, chiffres, tirets"
    case "$FAMILLE_RESOLVEUR" in
        unbound | quad9 | google) [ -z "$RESOLVEUR_FOURNISSEUR" ] || refuser RESOLVEUR_FOURNISSEUR "vide attendu" ;;
        fournisseur) [[ $RESOLVEUR_FOURNISSEUR =~ $liste ]] || refuser RESOLVEUR_FOURNISSEUR "1 à 4 adresses IPv4" ;;
        *) refuser FAMILLE_RESOLVEUR "unbound, quad9, google ou fournisseur" ;;
    esac
    [[ $ADRESSE_SURVEILLANCE =~ $https ]] || refuser ADRESSE_SURVEILLANCE "adresse https"
    [[ $ADRESSE_SAUVEGARDE =~ ^[a-z0-9-]+@[a-z0-9.-]+$ ]] || refuser ADRESSE_SAUVEGARDE "compte@hôte"
    [[ $CLE_INTERVENTION =~ $cle ]] || refuser CLE_INTERVENTION "clé publique ssh-ed25519"
}

ecrire() {      # ecrire <chemin du système> <mode> : l'entrée standard sous la racine (vide hors essai), par renommage
    mkdir -p "$R$(dirname "$1")"
    cat > "$R$1.nouveau"
    chmod "$2" "$R$1.nouveau"
    mv -f "$R$1.nouveau" "$R$1"
}

etape_sources() {       # E-D-04, E-D-12, décision 1 : l'archive Debian seule, en HTTPS (le pare-feu ne laisse que 443)
    local cle=/usr/share/keyrings/debian-archive-keyring.pgp f
    [ -f "$R$cle" ] || cle=/usr/share/keyrings/debian-archive-keyring.gpg
    [ -f "$R$cle" ] || { echo "premier-demarrage : APT/trousseau Debian absent" >&2; exit 3; }
    for f in "$R/etc/apt/sources.list" "$R"/etc/apt/sources.list.d/*.list "$R"/etc/apt/sources.list.d/*.sources; do
        if [ -f "$f" ] && [ "$f" != "$R/etc/apt/sources.list.d/debian.sources" ]; then mv -f "$f" "$f.disabled"; fi
    done
    ecrire /etc/apt/sources.list.d/debian.sources 0644 <<EOF
Types: deb
URIs: https://deb.debian.org/debian
Suites: trixie
Components: main
Signed-By: $cle

Types: deb
URIs: https://deb.debian.org/debian-security
Suites: trixie-security
Components: main
Signed-By: $cle
EOF
}

etape_paquets() {       # E-D-04 et décision 1 : paquets de la distribution ; unbound pour la famille unbound (O1) seule
    local p=(chrony nftables python3 rsync unattended-upgrades)
    [ "$FAMILLE_RESOLVEUR" != unbound ] || p+=(unbound)
    apt-get update
    apt-get install -y --no-install-recommends "${p[@]}"
}

etape_comptes() {       # E-D-03 : compte de service sans droit d'administration ; compte d'intervention, clé seule
    local service=(--system --user-group --home-dir /var/lib/shogen --create-home --shell /usr/sbin/nologin shogen)
    getent passwd shogen > /dev/null || useradd "${service[@]}"
    getent passwd intervention > /dev/null || useradd --user-group --create-home --shell /bin/bash intervention
    mkdir -p "$R/home/intervention"
    install -d -m 0700 "$R/home/intervention/.ssh"
    echo "$CLE_INTERVENTION" | ecrire /home/intervention/.ssh/authorized_keys 0600
    chown -R intervention:intervention "$R/home/intervention/.ssh"
}

etape_observateur() {   # E-D-01 : paramètres gardés pour les étapes suivantes (DB-2 à DB-5), lisibles du service seul
    ecrire /etc/shogen/observateur.conf 0640 <<EOF
OBSERVATEUR="$OBSERVATEUR"
FOURNISSEUR="$FOURNISSEUR"
REGION="$REGION"
FAMILLE_RESOLVEUR="$FAMILLE_RESOLVEUR"
RESOLVEUR_FOURNISSEUR="$RESOLVEUR_FOURNISSEUR"
ADRESSE_SURVEILLANCE="$ADRESSE_SURVEILLANCE"
ADRESSE_SAUVEGARDE="$ADRESSE_SAUVEGARDE"
EOF
    chown root:shogen "$R/etc/shogen/observateur.conf"
}

etape_ssh() {           # E-D-03, T-DP-5 : clé seule, ni root ni mot de passe ; lu avant les fichiers des images (00-)
    ecrire /etc/ssh/sshd_config.d/00-shogen.conf 0644 <<'EOF'
# Shōgen S2-bis (E-D-03) : clé seule, ni root ni mot de passe ; seul le compte d'intervention se connecte.
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
PubkeyAuthentication yes
AuthenticationMethods publickey
AllowUsers intervention
DisableForwarding yes
EOF
    sshd -t
    systemctl try-reload-or-restart ssh.service
}

etape_mises_a_jour() {  # E-D-12, T-DP-9, décision 1 : sécurité seule (trixie-security), sans redémarrage automatique
    ecrire /etc/apt/apt.conf.d/90shogen-securite 0644 <<'EOF'
// Shōgen S2-bis (E-D-12) : mises à jour de sécurité seules, sans redémarrage automatique. Lu après
// 50unattended-upgrades : #clear vide les listes d'origines des fichiers lus avant.
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
#clear Unattended-Upgrade::Allowed-Origins;
#clear Unattended-Upgrade::Origins-Pattern;
Unattended-Upgrade::Origins-Pattern { "origin=Debian,codename=trixie-security,label=Debian-Security"; };
Unattended-Upgrade::Automatic-Reboot "false";
EOF
    systemctl enable apt-daily.timer apt-daily-upgrade.timer
}

etape() { echo "premier-demarrage : étape $1"; "etape_$1"; }
verifier_parametres
etape sources
etape paquets
etape comptes
etape observateur
etape ssh
etape mises_a_jour
# Points d'entrée suivants (PROPOSITION §4.3) : horloge (DB-2, E-D-06, Q-D-06), résolveur par famille (DB-2, E-D-07,
# Q-D-05), code au commit scellé (DB-2, E-D-08, Q-D-01), descripteur et smoke (DB-2, E-D-13, E-D-14) ; unités et
# minuteries (DB-3, E-D-09) ; sauvegarde, échange des têtes, signal de vie, alerte disque (DB-4, E-D-10, E-D-11) ;
# empreintes de rejouabilité (DB-5, E-D-02).
echo "premier-demarrage : fin"
