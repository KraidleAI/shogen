"""Serveur local de fichiers synthétiques des tests d'acquisition (127.0.0.1, port libre) : GET d'un chemin
(requête comprise) servi depuis le dict `fichiers` ; en-tête Range « bytes=a-b » servi en 206 ; `pannes[chemin]`
réponses 500 avant de servir ; chaque requête notée dans `vus`. Aucun accès hors de la boucle locale."""
import http.server
import threading


class Serveur:
    def __init__(self, fichiers: dict, pannes=None):
        self.fichiers, self.pannes, self.vus = fichiers, dict(pannes or {}), []
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
                plage = self.headers.get("Range")
                if plage:
                    a, b = (int(x) for x in plage.split("=")[1].split("-"))
                    corps, code = corps[a:b + 1], 206
                    self.send_response(code)
                    total = len(serveur.fichiers[self.path])
                    self.send_header("Content-Range", f"bytes {a}-{a + len(corps) - 1}/{total}")
                else:
                    self.send_response(200)
                self.send_header("Content-Length", str(len(corps)))
                self.end_headers()
                self.wfile.write(corps)

            def log_message(self, *_a):
                pass

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Gestion)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.fil = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.fil.start()
        return self

    def __exit__(self, *_a):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.fil.join()
