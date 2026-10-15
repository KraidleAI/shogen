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
SCRIPT = os.path.join(DEPLOI, "premier-demarrage.sh")
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


if __name__ == "__main__":
    unittest.main()
