import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

from database import conectar_base_datos
from validate_type import validate_query_params


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            conexion = self.establecer_conexion_base_datos()
            if not conexion:
                self.handle_database_connection_error()
                return

            query_params = self.obtener_parametros_url()

            if not self.validar_path():
                return
            
            validated = validate_query_params(query_params)

            if isinstance(validated, list):
                return self.wfile.write(json.dumps(
                    {"error": validated}).encode())

            consulta = self.construir_consulta(query_params)
            resultado = self.ejecutar_consulta(conexion, consulta)

            if resultado:
                self.enviar_respuesta(resultado)
            else:
                self.enviar_respuesta_vacia()

        except Exception as e:
            self.send_error(500, str(e))
        finally:
            if conexion:
                conexion.close()

    def establecer_conexion_base_datos(self):
        try:
            conexion = conectar_base_datos()
            if not conexion:
                raise Exception("Error al conectar a la base de datos.")
            return conexion
        except Exception:
            self.handle_database_connection_error()
            return None

    def obtener_parametros_url(self):
        parsed_path = urllib.parse.urlparse(self.path)
        return urllib.parse.parse_qs(parsed_path.query)

    def validar_path(self):
        endpoint = "/get_and_search/"
        if self.path.startswith(endpoint):
            return True
        else:
            self.send_error(400, str('Error al ingresar el endpoint'))
            return False

    def construir_consulta(self, query_params):
        consulta = """
            SELECT p.address, p.city, s.name AS current_status, p.price, p.description
            FROM property p
            JOIN (
                SELECT sh.property_id, sh.status_id, sh.update_date
                FROM status_history sh
                JOIN (
                    SELECT property_id, MAX(update_date) AS max_update_date
                    FROM status_history
                    GROUP BY property_id
                ) max_sh ON sh.property_id = max_sh.property_id AND sh.update_date = max_sh.max_update_date
            ) latest_sh ON p.id = latest_sh.property_id
            JOIN status s ON latest_sh.status_id = s.id
            """
        estados_permitidos = ("pre_venta", "en_venta", "vendido")

        condiciones = []

        if 'year' in query_params:
            condiciones.append("p.year = {}".format(query_params['year'][0]))

        if 'city' in query_params:
            condiciones.append("p.city = '{}'".format(query_params['city'][0]))

        if 'state' in query_params:
            estado = query_params['state'][0]
            if estado in estados_permitidos:
                condiciones.append("s.name = '{}'".format(estado))
            else:
                self.send_error(
                    400, "Estado no permitido para la consulta, pruebe con los estados disponibles")
                return None

        if condiciones:
            consulta += " WHERE " + " AND ".join(condiciones)

        return consulta

    def ejecutar_consulta(self, conexion, consulta):
        cursor = conexion.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()

    def enviar_respuesta(self, resultado):
        resultado_json = json.dumps(resultado).encode()
        self.wfile.write(resultado_json)

    def enviar_respuesta_vacia(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(
            'No se encontraron coincidencias').encode())

    def handle_database_connection_error(self):
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(
            {"error": "Error al conectar a la base de datos"}).encode())
