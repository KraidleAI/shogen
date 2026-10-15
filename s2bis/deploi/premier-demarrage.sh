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
SERVEURS_NTP="sth1.nts.netnod.se gbg1.nts.netnod.se ntppool1.time.nl ntppool2.time.nl"    # décision 4 de DB-0
R=""
if [ "$#" -eq 2 ] && [ "$1" = --essai ]; then
    R="$(cd "$2" && pwd -P)" || R=""
    [ -n "$R" ] && ! [ "$R" -ef / ] && [ -f "$R/essai.getent" ] ||  # vide (cd en échec), « / », « // » : refus
        { echo "premier-demarrage : ESSAI/racine refusée" >&2; exit 2; }
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
    # Octet IPv4 de 0 à 255 sans zéro de tête (nft et getaddrinfo lisent 010 en octal : 8) ; clé : bloc ed25519 de 68
    # caractères, en-tête fixe (type ssh-ed25519, clé de 32 octets) puis 43 caractères.
    local o='(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])' cle='^ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI[A-Za-z0-9+/]{43}'
    local ip4="$o([.]$o){3}" https='^https://[a-z0-9.-]+(/[A-Za-z0-9._-]+)+$' nom='^[a-z0-9-]{1,32}$'
    local liste="^$ip4( $ip4){0,3}$" cle="$cle( [A-Za-z0-9@._-]+)?$"
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
    mkdir -p "$R$(dirname "$1")"                # le temporaire naît 0600, même après un lancement interrompu : rien
    rm -f "$R$1.nouveau"                        # de lisible par autrui avant le mode final (observateur.conf, Q-6)
    (umask 077 && cat > "$R$1.nouveau")
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
    if getent passwd intervention > /dev/null; then     # relance : root n'écrit rien sous ce dossier, où le compte a pu
        echo "premier-demarrage : COMPTES/intervention présent, clé inchangée" >&2; return 0     # poser des liens
    fi
    useradd --user-group --create-home --shell /bin/bash intervention       # clé posée à la création seule
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

adresses() {    # adresses IPv4 du nom $1 par le résolveur du système, jointes par des virgules ; refus si aucune
    local a
    a="$(getent ahostsv4 "$1" | awk '{ print $1 }' | sort -u | paste -sd , -)" || a=""
    [ -n "$a" ] || { echo "premier-demarrage : PARE-FEU/résolution : $1" >&2; exit 3; }
    echo "$a"
}

etape_pare_feu() {      # E-D-05, décision 3, Q-D-07 : commun embarqué (égal à s2bis/deploi/nftables.conf), ensembles
    local r ntp="" n sauvegarde
    case "$FAMILLE_RESOLVEUR" in
        unbound) r=0.0.0.0/0 ;;                         # O1 récursif : toute autorité (Q-D-07)
        quad9) r=9.9.9.9,149.112.112.112 ;;             # ADR-0029 l.82
        google) r=8.8.8.8,8.8.4.4 ;;                    # ADR-0029 l.82
        fournisseur) r="${RESOLVEUR_FOURNISSEUR// /,}" ;;
    esac
    for n in $SERVEURS_NTP; do ntp="$ntp${ntp:+,}$(adresses "$n")"; done
    sauvegarde="$(adresses "${ADRESSE_SAUVEGARDE#*@}")"
    ecrire /etc/nftables.conf 0644 <<'NFT'
#!/usr/sbin/nft -f
# Shōgen S2-bis, pare-feu commun des quatre observateurs (DEPLOI-BIS, DB-1 ; ADR-0029 l.243 ; PROPOSITION §4.2
# E-D-05 ; décision 3 de DB-0 ; Q-D-07) : refus par défaut dans les deux sens, IPv6 refusé, IPv4 seul admis.
# Les ensembles d'observateur (résolveur, serveurs NTP, espace de sauvegarde) sont remplis par /etc/nftables.d/*.nft,
# écrit au premier démarrage et jamais versé ; sans ce fichier, ils restent vides : refus.
flush ruleset

table inet shogen {
	set resolveurs {
		type ipv4_addr
		flags interval
	}

	set ntp {
		type ipv4_addr
	}

	set sauvegarde {
		type ipv4_addr
	}

	chain entree {
		type filter hook input priority filter; policy drop;
		iif "lo" accept
		meta nfproto ipv6 drop
		ct state established,related accept
		ct state invalid drop
		udp sport 67 udp dport 68 accept  # DHCP : réponses au renouvellement du bail
		tcp dport 22 accept  # SSH, clé seule (E-D-03)
	}

	chain sortie {
		type filter hook output priority filter; policy drop;
		oif "lo" accept
		meta nfproto ipv6 drop
		ct state established,related accept
		ct state invalid drop
		udp sport 68 udp dport 67 accept  # DHCP : renouvellement du bail
		ip daddr 169.254.169.254 tcp dport 80 meta skuid 0 accept  # métadonnées du fournisseur (cloud-init, root)
		tcp dport 443 accept  # HTTPS : sources, archive Debian, signal de vie, horodatage
		ip daddr { 198.41.0.4, 192.36.148.17, 193.0.14.129 } udp dport 53 accept  # témoins D-4 (ADR-0029 l.109)
		ip daddr @resolveurs udp dport 53 accept
		ip daddr @resolveurs tcp dport 53 accept
		ip daddr @ntp udp dport 123 accept
		ip daddr @ntp tcp dport 4460 accept  # NTS-KE (RFC 8915)
		ip daddr @sauvegarde tcp dport 23 accept  # rsync sur SSH vers l'espace de sauvegarde (port 23)
	}

	chain transit {
		type filter hook forward priority filter; policy drop;
	}
}

include "/etc/nftables.d/*.nft"
NFT
    ecrire /etc/nftables.d/shogen-observateur.nft 0644 <<EOF
# Ensembles d'observateur du pare-feu, écrits au premier démarrage : jamais versés.
add element inet shogen resolveurs { $r }
add element inet shogen ntp { $ntp }
add element inet shogen sauvegarde { $sauvegarde }
EOF
    nft -c -f "$R/etc/nftables.conf"
    systemctl enable nftables.service
    systemctl restart nftables.service
}

etape() { echo "premier-demarrage : étape $1"; "etape_$1"; }
verifier_parametres
etape sources
etape paquets
etape comptes
etape observateur
etape ssh
etape mises_a_jour
# Point d'entrée DB-2, avant le pare-feu dont les ensembles en dépendent (décision 3 : noms résolus par le résolveur de
# l'observateur) : horloge (E-D-06, Q-D-06) et résolveur par famille (E-D-07, Q-D-05).
etape pare_feu
# Points d'entrée suivants (PROPOSITION §4.3) : code au commit scellé (DB-2, E-D-08, Q-D-01), descripteur et smoke
# (DB-2, E-D-13, E-D-14) ; unités et minuteries (DB-3, E-D-09) ; sauvegarde, échange des têtes, signal de vie, alerte
# disque (DB-4, E-D-10, E-D-11) ; empreintes de rejouabilité (DB-5, E-D-02).
echo "premier-demarrage : fin"
