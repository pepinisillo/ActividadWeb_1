from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        contenido = {'/': 'home.html', '/proyecto/1': '1.html', '/proyecto/web-uno': self.respuesta_autor, '/proyecto/web-dos': self.respuesta_autor}
        valor = contenido.get(self.url().path)

        if self.url().path not in contenido:
            self.send_error(404, "Archivo no encontrado")
            return
        else:
            if callable(valor):
                if not self.query_data().get("autor"):
                    self.send_error(400, "Falta el parámetro 'autor'")
                    return
                else:
                    self.info_html()
                    self.wfile.write(valor().encode("utf-8"))
                    return
            else:
                self.info_html()
                self.regresar_html(valor)
                return
      
    def regresar_html(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            html = f.read()
        self.wfile.write(html.encode("utf-8"))
        return 
    
    def info_html(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def respuesta_autor(self):
        return f"""
        <h1> Proyecto: {self.url().path.split('/')[-1]} Autor: {self.query_data()['autor']}</h1>
    """

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8080), WebRequestHandler)
    server.serve_forever()
