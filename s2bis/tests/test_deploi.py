"""DEPLOI-BIS, sous-lot DB-1 (G0 docs/adr-0029/g0-collecte/ : PROPOSITION §4.2 et §4.4 ; décisions 1 à 5 de DB-0) :
script I de premier démarrage (s2bis/deploi/premier-demarrage.sh), lancé en mode d'essai sur une racine factice, sans
privilège ni réseau (apt-get, systemctl et les commandes système y sont des enregistreurs) ; chaque méthode porte le
numéro de son test (T-DP-n de la PROPOSITION §4.4, décision 5 de DB-0). Valeurs attendues écrites ici depuis les
pièces (ADR-0029, RAPPORT-DB0, index Debian lus à DB-0), jamais lues dans le script."""
import os
import subprocess
import tempfile
import unittest

NL = chr(10)
DEPLOI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "deploi")
SCRIPT, NFT = (os.path.join(DEPLOI, n) for n in ("premier-demarrage.sh", "nftables.conf"))
CLE = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEssaiDB1EssaiDB1EssaiDB1EssaiDB1EssaiDB1Ess investisseur@poste"
OBS = {"o1": ("hetzner", "hel1", "unbound", ""), "o2": ("ovhcloud", "gra", "quad9", ""),     # décision 2 de DB-0
       "o3": ("digitalocean", "ams3", "google", ""),
       "o4": ("linode", "sg-sin-2", "fournisseur", "203.0.113.53 203.0.113.54")}
NTP = ["sth1.nts.netnod.se", "gbg1.nts.netnod.se", "ntppool1.time.nl", "ntppool2.time.nl"]     # décision 4 de DB-0
DNS = {**dict(zip(NTP, ["192.0.2.11", "192.0.2.12", "192.0.2.13", "192.0.2.14"])),
       "u1.your-storagebox.de": "192.0.2.23"}
IMAGE = {"usr/share/keyrings/debian-archive-keyring.pgp": "",           # image Debian 13 factice (adresses RFC 5737)
         "etc/apt/sources.list": "deb http://miroir.example/debian trixie main" + NL,
         "etc/apt/sources.list.d/fournisseur.list": "deb http://agent.example/apt stable main" + NL,
         "etc/ssh/sshd_config.d/50-cloud-init.conf": "PasswordAuthentication yes" + NL}
ETAPES = ["sources", "paquets", "comptes", "observateur", "ssh", "mises_a_jour", "pare_feu"]
GARDES = {"usr/share/keyrings/debian-archive-keyring.pgp", "etc/ssh/sshd_config.d/50-cloud-init.conf"}
PRODUITS = {"etc/apt/sources.list.disabled", "etc/apt/sources.list.d/fournisseur.list.disabled",
            "etc/apt/sources.list.d/debian.sources", "home/intervention/.ssh/authorized_keys",
            "etc/shogen/observateur.conf", "etc/ssh/sshd_config.d/00-shogen.conf",
            "etc/apt/apt.conf.d/90shogen-securite", "etc/nftables.conf", "etc/nftables.d/shogen-observateur.nft"}
SSHD = [["PermitRootLogin", "no"], ["PasswordAuthentication", "no"], ["KbdInteractiveAuthentication", "no"],
        ["PermitEmptyPasswords", "no"], ["PubkeyAuthentication", "yes"], ["AuthenticationMethods", "publickey"],
        ["AllowUsers", "intervention"], ["DisableForwarding", "yes"]]
APT = ['APT::Periodic::Update-Package-Lists "1";', 'APT::Periodic::Unattended-Upgrade "1";',
       "#clear Unattended-Upgrade::Allowed-Origins;", "#clear Unattended-Upgrade::Origins-Pattern;",
       'Unattended-Upgrade::Origins-Pattern { "origin=Debian,codename=trixie-security,label=Debian-Security"; };',
       'Unattended-Upgrade::Automatic-Reboot "false";']        # Origin, Label, Codename : InRelease de trixie-security
ENTREE = ['iif "lo" accept', "meta nfproto ipv6 drop", "ct state established,related accept", "ct state invalid drop",
          "udp sport 67 udp dport 68 accept", "tcp dport 22 accept"]
SORTIE = ['oif "lo" accept', "meta nfproto ipv6 drop", "ct state established,related accept", "ct state invalid drop",
          "udp sport 68 udp dport 67 accept", "ip daddr 169.254.169.254 tcp dport 80 meta skuid 0 accept",
          "tcp dport 443 accept", "ip daddr { 198.41.0.4, 192.36.148.17, 193.0.14.129 } udp dport 53 accept",
          "ip daddr @resolveurs udp dport 53 accept", "ip daddr @resolveurs tcp dport 53 accept",
          "ip daddr @ntp udp dport 123 accept", "ip daddr @ntp tcp dport 4460 accept",
          "ip daddr @sauvegarde tcp dport 23 accept"]
TEMOINS = {"198.41.0.4", "192.36.148.17", "193.0.14.129"}     # témoins D-4, ADR-0029 l.109


def commandes(o):
    """Commandes système attendues de l'observateur o, dans l'ordre (racine factice retirée des chemins)."""
    return ["apt-get update", "apt-get install -y --no-install-recommends chrony nftables python3 rsync "
            "unattended-upgrades" + " unbound" * (o == "o1"), "getent passwd shogen",
            "useradd --system --user-group --home-dir /var/lib/shogen --create-home --shell /usr/sbin/nologin shogen",
            "getent passwd intervention", "useradd --user-group --create-home --shell /bin/bash intervention",
            "chown -R intervention:intervention /home/intervention/.ssh",
            "chown root:shogen /etc/shogen/observateur.conf", "sshd -t", "systemctl try-reload-or-restart ssh.service",
            "systemctl enable apt-daily.timer apt-daily-upgrade.timer",
            *("getent ahostsv4 " + n for n in [*NTP, "u1.your-storagebox.de"]), "nft -c -f /etc/nftables.conf",
            "systemctl enable nftables.service", "systemctl restart nftables.service"]


def pare_feu(texte):
    """(tables, {chaîne : [crochet, politique, règles]}) d'un fichier nftables, commentaires et blancs retirés."""
    tables, chaines, nom = [], {}, None
    for ligne in texte.splitlines():
        t = " ".join(ligne.split("#")[0].split())
        if t.startswith("table "):
            tables.append(t)
        elif t.startswith("chain "):
            nom = t.split()[1]
            chaines[nom] = [None, None, []]
        elif nom and t == "}":
            nom = None
        elif nom and t.startswith("type filter hook "):
            chaines[nom][:2] = [t.split()[3], t.split()[-1]]
        elif nom and t:
            chaines[nom][2].append(t)
    return tables, chaines


class Essai(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory(prefix="db1_")
        self.addCleanup(t.cleanup)
        self.tmp = t.name

    def parametres(self, o, **x):
        f, r, fam, rf = OBS[o]
        return {"OBSERVATEUR": o, "FOURNISSEUR": f, "REGION": r, "FAMILLE_RESOLVEUR": fam, "RESOLVEUR_FOURNISSEUR": rf,
                "ADRESSE_SURVEILLANCE": "https://hc-ping.com/essai-db1", "CLE_INTERVENTION": CLE,
                "ADRESSE_SAUVEGARDE": "u1-sub1@u1.your-storagebox.de", **x}

    def lire(self, *chemin, mode="r"):
        self.assertTrue(os.path.isfile(os.path.join(*chemin)), os.path.join(*chemin))
        with open(os.path.join(*chemin), mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
            return f.read()

    def rempli(self, params):
        """Texte du script, paramètres collés en tête comme par l'investisseur."""
        texte = self.lire(SCRIPT)
        for k, v in params.items():
            self.assertEqual(texte.count(NL + k + '=""'), 1, k)
            texte = texte.replace(NL + k + '=""', NL + k + '="' + v + '"')
        return texte

    def lancer(self, params, image=IMAGE, dns=DNS):
        """(code, sortie, erreur, racine) du script rempli de `params`, en essai sur une racine factice neuve."""
        racine, script = tempfile.mkdtemp(dir=self.tmp), os.path.join(tempfile.mkdtemp(dir=self.tmp), "script.sh")
        resolution = "".join(f"ahostsv4 {n} {a}" + NL for n, a in dns.items())
        for chemin, texte in {**image, "essai.getent": resolution}.items():
            os.makedirs(os.path.dirname(os.path.join(racine, chemin)), exist_ok=True)
            with open(os.path.join(racine, chemin), "w", encoding="utf-8") as f:
                f.write(texte)
        with open(script, "w", encoding="utf-8") as f:
            f.write(self.rempli(params))
        p = subprocess.run(["bash", script, "--essai", racine], capture_output=True, timeout=120,
                           env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
        return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8"), racine

    def fichiers(self, racine):
        """Fichiers sous la racine factice (chemins relatifs), hors fichiers de l'essai."""
        return {os.path.relpath(os.path.join(d, n), racine).replace(os.sep, "/") for d, _s, ns in os.walk(racine)
                for n in ns} - {"essai.commandes", "essai.getent"}

    def journal(self, racine):
        """Commandes enregistrées, racine factice retirée des chemins ; [] sans journal."""
        if not os.path.isfile(os.path.join(racine, "essai.commandes")):
            return []
        return self.lire(racine, "essai.commandes").replace(os.path.realpath(racine), "").splitlines()


class PremierDemarrage(Essai):
    def test_tdp1_syntaxe(self):
        self.assertTrue(os.path.isfile(SCRIPT), SCRIPT)
        p = subprocess.run(["bash", "-n", SCRIPT], capture_output=True, timeout=60)
        self.assertEqual((p.returncode, p.stderr), (0, b""))

    def test_tdp1_usage_et_racine_refusees(self):
        """Script non rempli : hors du mode d'essai, le refus des paramètres arrêterait tout avant tout changement."""
        vide = tempfile.mkdtemp(dir=self.tmp)                               # racine sans essai.getent
        for args, motif in ((["--essai", vide], "ESSAI/racine"), (["--essai", vide + "/absente"], "ESSAI/racine"),
                            (["--essai"], "usage"), (["--autre", vide], "usage")):
            with self.subTest(args=args):
                p = subprocess.run(["bash", SCRIPT, *args], capture_output=True, timeout=60,
                                   env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
                self.assertEqual((p.returncode, p.stdout, os.listdir(vide)), (2, b"", []))
                self.assertIn(motif, p.stderr.decode("utf-8"))

    def test_tdp1_parametre_refuse_rien_ne_change(self):
        cas = [("o2", k, "") for k in ("OBSERVATEUR", "FOURNISSEUR", "REGION", "FAMILLE_RESOLVEUR",
                                       "ADRESSE_SURVEILLANCE", "ADRESSE_SAUVEGARDE", "CLE_INTERVENTION")]
        cas += [("o2", "OBSERVATEUR", "o5"), ("o2", "FAMILLE_RESOLVEUR", "cloudflare"),
                ("o2", "RESOLVEUR_FOURNISSEUR", "9.9.9.9"), ("o4", "RESOLVEUR_FOURNISSEUR", ""),
                ("o2", "ADRESSE_SURVEILLANCE", "http://hc-ping.com/x"), ("o2", "ADRESSE_SAUVEGARDE", "u1@h;reboot"),
                ("o2", "CLE_INTERVENTION", "ssh-rsa AAAAB3NzaC1yc2E")]
        for o, k, v in cas:
            with self.subTest(o=o, k=k, v=v):
                code, sortie, erreur, racine = self.lancer(self.parametres(o, **{k: v}))
                self.assertEqual((code, sortie, self.journal(racine), self.fichiers(racine)), (2, "", [], set(IMAGE)))
                self.assertIn(f"PARAMETRE/{k} ", erreur)

    def test_decision5_taille(self):
        borne = 32 * 1024      # Hetzner, « This field is limited to 32KiB » (RAPPORT-DB0 §2, [lu]) : la plus petite lue

        def tient(texte):
            return len(texte.encode("utf-8")) <= borne
        self.assertFalse(tient("#" * (borne + 1)))                 # témoin : la borne refuse au-delà
        self.assertTrue(tient(self.rempli(self.parametres("o4", **{k: "x" * 200 for k in (
            "FOURNISSEUR", "REGION", "ADRESSE_SURVEILLANCE", "ADRESSE_SAUVEGARDE", "CLE_INTERVENTION")}))))

    def test_tdp1_essai_quatre_observateurs(self):
        for o in OBS:
            with self.subTest(o=o):
                code, sortie, erreur, racine = self.lancer(self.parametres(o))
                self.assertEqual((code, erreur), (0, ""))
                self.assertEqual(sortie.splitlines(), [f"premier-demarrage : étape {e}" for e in ETAPES]
                                 + ["premier-demarrage : fin"])
                self.assertEqual(self.journal(racine), commandes(o))
                self.assertEqual(self.fichiers(racine), PRODUITS | GARDES)

    def test_tdp1_parametres_gardes_et_cle(self):
        p = self.parametres("o4")
        code, _s, _e, racine = self.lancer(p)
        self.assertEqual(code, 0)
        self.assertEqual(self.lire(racine, "etc/shogen/observateur.conf"), "".join(f'{k}="{p[k]}"' + NL for k in (
            "OBSERVATEUR", "FOURNISSEUR", "REGION", "FAMILLE_RESOLVEUR", "RESOLVEUR_FOURNISSEUR",
            "ADRESSE_SURVEILLANCE", "ADRESSE_SAUVEGARDE")))
        self.assertEqual(self.lire(racine, "home/intervention/.ssh/authorized_keys"), CLE + NL)
        self.assertEqual([os.stat(os.path.join(racine, c)).st_mode & 0o777 for c in (
            "etc/shogen/observateur.conf", "home/intervention/.ssh", "home/intervention/.ssh/authorized_keys")],
            [0o640, 0o700, 0o600])

    def test_tdp1_sources_https_et_trousseau(self):
        bloc = "Types: deb{0}URIs: https://deb.debian.org/{1}{0}Suites: {2}{0}Components: main{0}Signed-By: {3}{0}"
        sans = {k: v for k, v in IMAGE.items() if not k.startswith("usr/")}
        for ext in ("pgp", "gpg"):
            with self.subTest(ext=ext):
                cle = "/usr/share/keyrings/debian-archive-keyring." + ext
                code, _s, _e, racine = self.lancer(self.parametres("o2"), {**sans, cle[1:]: ""})
                self.assertEqual(code, 0)
                self.assertEqual(self.lire(racine, "etc/apt/sources.list.d/debian.sources"), bloc.format(
                    NL, "debian", "trixie", cle) + NL + bloc.format(NL, "debian-security", "trixie-security", cle))
                self.assertEqual([self.lire(racine, c + ".disabled") for c in sans if c.startswith("etc/apt/")],
                                 [IMAGE["etc/apt/sources.list"], IMAGE["etc/apt/sources.list.d/fournisseur.list"]])
        code, sortie, erreur, racine = self.lancer(self.parametres("o2"), sans)
        self.assertEqual((code, self.journal(racine), self.fichiers(racine)), (3, [], set(sans)))
        self.assertIn("APT/trousseau", erreur)

    def test_tdp5_sshd_cle_seule(self):
        code, _s, _e, racine = self.lancer(self.parametres("o3"))
        self.assertEqual(code, 0)
        self.assertEqual(sorted(os.listdir(os.path.join(racine, "etc/ssh/sshd_config.d"))),
                         ["00-shogen.conf", "50-cloud-init.conf"])          # première valeur lue retenue par sshd
        self.assertEqual([x.split(None, 1) for x in self.lire(racine, "etc/ssh/sshd_config.d/00-shogen.conf").split(
            NL) if x.strip() and not x.startswith("#")], SSHD)

    def test_tdp9_securite_seule_sans_redemarrage(self):
        code, _s, _e, racine = self.lancer(self.parametres("o1"))
        self.assertEqual(code, 0)
        self.assertEqual([x.strip() for x in self.lire(racine, "etc/apt/apt.conf.d/90shogen-securite").split(NL)
                          if x.strip() and not x.startswith("//")], APT)
        self.assertEqual(os.listdir(os.path.join(racine, "etc/apt/apt.conf.d")), ["90shogen-securite"])

    def test_tdp2_refus_par_defaut_ipv4_et_ipv6(self):
        texte = self.lire(NFT)
        lignes = [t for t in (" ".join(x.split("#")[0].split()) for x in texte.split(NL)) if t]
        self.assertEqual((lignes[0], lignes[-1]), ("flush ruleset", 'include "/etc/nftables.d/*.nft"'))
        tables, chaines = pare_feu(texte)
        self.assertEqual(tables, ["table inet shogen {"])         # inet : IPv4 et IPv6 passent par les mêmes chaînes
        self.assertEqual({n: c[:2] for n, c in chaines.items()},
                         {"entree": ["input", "drop;"], "sortie": ["output", "drop;"], "transit": ["forward", "drop;"]})
        self.assertEqual([chaines[n][2][:2] for n in ("entree", "sortie")],
                         [['iif "lo" accept', "meta nfproto ipv6 drop"], ['oif "lo" accept', "meta nfproto ipv6 drop"]])

    def test_tdp2_regles_exactes(self):
        _t, chaines = pare_feu(self.lire(NFT))
        self.assertEqual([chaines[n][2] for n in ("entree", "sortie", "transit")], [ENTREE, SORTIE, []])
        self.assertEqual([set(r.split("{")[1].split("}")[0].replace(",", " ").split()) for r in chaines["sortie"][2]
                          if "dport 53" in r and "{" in r], [TEMOINS])

    def test_tdp2_commun_embarque_et_ensembles(self):
        resolveurs = {"o1": "0.0.0.0/0", "o2": "9.9.9.9,149.112.112.112", "o3": "8.8.8.8,8.8.4.4",
                      "o4": "203.0.113.53,203.0.113.54"}                    # ADR-0029 l.82 ; O1 récursif (Q-D-07)
        for o, r in resolveurs.items():
            with self.subTest(o=o):
                code, _s, _e, racine = self.lancer(self.parametres(o))
                self.assertEqual(code, 0)
                self.assertEqual(self.lire(racine, "etc/nftables.conf", mode="rb"), self.lire(NFT, mode="rb"))
                self.assertEqual(self.lire(racine, "etc/nftables.d/shogen-observateur.nft").split(NL)[1:], [
                    "add element inet shogen resolveurs { " + r + " }",
                    "add element inet shogen ntp { 192.0.2.11,192.0.2.12,192.0.2.13,192.0.2.14 }",
                    "add element inet shogen sauvegarde { 192.0.2.23 }", ""])

    def test_tdp2_nom_non_resolu_refuse(self):
        for nom in ("ntppool2.time.nl", "u1.your-storagebox.de"):
            with self.subTest(nom=nom):
                dns = {k: v for k, v in DNS.items() if k != nom}
                code, _s, erreur, racine = self.lancer(self.parametres("o2"), dns=dns)
                self.assertEqual(code, 3)
                self.assertIn("PARE-FEU/résolution : " + nom, erreur)
                self.assertEqual(self.fichiers(racine) & {"etc/nftables.conf", "etc/nftables.d/shogen-observateur.nft"},
                                 set())
                self.assertNotIn("systemctl restart nftables.service", self.journal(racine))


if __name__ == "__main__":
    unittest.main()
