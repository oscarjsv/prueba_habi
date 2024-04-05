# consulta.py

import json
from http.server import BaseHTTPRequestHandler
import urllib.parse

from database import conectar_base_datos


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Establecer conexión a la base de datos
            try:
                conexion = conectar_base_datos()
                if not conexion:
                    raise Exception("Error al conectar a la base de datos.")
                # Proceder con el manejo de la solicitud asumiendo que la conexión a la base de datos es exitosa
            except Exception as e:
                self.handle_database_connection_error()
                return

            cursor = conexion.cursor()

            # Obtener parámetros de la URL
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)

            if not validate_path(self, parsed_path):
                return  # Verificar si el path es válido


            # Consulta a la base de datos 
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

            # Filtrar por año de construcción si está presente en los parámetros
            if 'year' in query_params:
                condiciones.append(
                    "p.year = {}".format(query_params['year'][0]))

            # Filtrar por ciudad si está presente en los parámetros
            if 'city' in query_params:
                condiciones.append(
                    "p.city = '{}'".format(query_params['city'][0]))

            if 'state' in query_params:
                estado = query_params['state'][0]
                if estado in estados_permitidos:
                    condiciones.append(
                        "s.name = '{}'".format(estado))
                else:
                    # Si el estado no está permitido, enviar un mensaje de error en JSON
                    self.wfile.write(json.dumps(
                        {"message": "Estado no permitido para la consulta pruebe con los estados disponible"}).encode())
                    cursor.close()
                    conexion.close()
                    return
            
            if condiciones:
                consulta += "WHERE " + " AND ".join(condiciones)

            cursor.execute(consulta)
            resultado = cursor.fetchall()
            if resultado:
                # Convertir resultado a formato JSON y enviar como respuesta
                resultado = json.dumps(resultado).encode()
                self.wfile.write(resultado)
            else:
                self.send_response(200, 'no se encuentran coincidencias')
                self.wfile.write(json.dumps(
                    'no se encontraron coincidencias').encode())

        except Exception as e:
            self.send_error(500, str(e),)
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()


def handle_database_connection_error(self):
    self.send_response(500)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(
        {"error": "Error al conectar a la base de datos"}).encode())


def validate_path(self, parsed_path):
    endpoint = "/get_and_search/"
    if parsed_path.path == endpoint:
        return True
    else:
        self.send_error(400, str('Error al ingresar el endpoint'))
        return False
