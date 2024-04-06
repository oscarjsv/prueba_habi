from consulta_handler import RequestHandler
from http.server import HTTPServer

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("HTTP server started on port 8000")
    httpd.serve_forever()
