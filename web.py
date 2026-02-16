from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        if self.url().path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("home.html", "r", encoding="utf-8") as archivo:
                html = archivo.read()
            self.wfile.write(html.encode("utf-8"))
            return #Dejar de ejecutar el resto del código
        else:
            self.send_error(404, "Página no encontrada")
            return #Mostrar error en caso de que la ruta sea una distinta 

        """
        if self.query_data().get("autor") is None:
            self.send_error(400, "No se proporcionó el autor")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))
        """

    def get_response(self):
        return f"""
        <h1> Proyecto: {self.url().path.split('/')[-1]} Autor: {self.query_data()['autor']}</h1>
    """

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8080), WebRequestHandler)
    server.serve_forever()
