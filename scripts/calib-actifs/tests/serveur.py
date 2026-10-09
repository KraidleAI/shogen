"""Serveur local de fichiers synthétiques des tests d'acquisition (127.0.0.1, port libre) : GET d'un chemin
(requête comprise) servi depuis le dict `fichiers` ; en-tête Range « bytes=a-b » servi en 206 ; `pannes[chemin]`
réponses 500 avant de servir ; `sans_plage` : 200 et tout le corps ; `longs[chemin]` : un octet de trop sous ce
rang ; requêtes notées dans `vus`. Aucun accès hors de la boucle locale."""
import http.server
import threading


class Serveur:
    def __init__(self, fichiers: dict, pannes=None, sans_plage=(), longs=None):
        self.fichiers, self.pannes, self.vus, self.sans_plage = fichiers, dict(pannes or {}), [], sans_plage
        self.octets, self.longs = 0, longs or {}
        serveur = self

        class Gestion(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                serveur.vus.append(self.path)
                corps = serveur.fichiers.get(self.path)
                if corps is None or serveur.pannes.get(self.path, 0) > 0:
                    if corps is not None:
                        serveur.pannes[self.path] -= 1
                    self.send_response(404 if corps is None else 500)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                plage, total = self.headers.get("Range"), len(corps)
                if plage:
                    a, b = (int(x) for x in plage.split("=")[1].split("-"))
                    entier, trop = self.path in serveur.sans_plage, b"x" * (a < serveur.longs.get(self.path, 0))
                    corps = corps if entier else corps[a:b + 1] + trop
                    self.send_response(200 if entier else 206)
                    self.send_header("Content-Range", f"bytes {a}-{a + len(corps) - 1}/{total}")
                else:
                    self.send_response(200)
                self.send_header("Content-Length", str(len(corps)))
                self.end_headers()
                serveur.octets += len(corps)
                self.wfile.write(corps)

            def log_message(self, *_a):
                pass

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Gestion)
        self.httpd.handle_error = lambda *_a: None        # client parti avant la fin du corps : attendu
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.fil = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.fil.start()
        return self

    def __exit__(self, *_a):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.fil.join()
