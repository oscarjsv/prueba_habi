import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

from .database import connect_to_database
from .validate_type import validate_query_params


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handles GET requests.
        """

        try:
            connection = self.establish_database_connection()
            if not connection:
                self.handle_database_connection_error()
                return

            query_params = self.get_url_parameters()

            if not self.validate_path():
                return

            validated = validate_query_params(query_params)

            if isinstance(validated, list):
                error_message = f"Validation error: {validated[0]}"
                self.api_response(404, error_message)
                return

            query = self.build_query(query_params)
            result = self.execute_query(connection, query)

            if result:
                self.response(result)
            else:
                self.api_response(200, "No matches found")

        except Exception as e:
            self.wfile.write(json.dumps(
                {"error": str(e)}).encode())
        finally:
            if connection:
                connection.close()

    def establish_database_connection(self):
        """
        Establishes connection to the database.
        """
        try:
            connection = connect_to_database()
            if not connection:
                raise Exception("Error connecting to the database.")
            return connection
        except Exception:
            self.handle_database_connection_error()
            return None

    def get_url_parameters(self):
        """
        Parses and retrieves URL parameters.
        """
        parsed_path = urllib.parse.urlparse(self.path)
        return urllib.parse.parse_qs(parsed_path.query)

    def validate_path(self):
        """
        Validates the path of the request.
        """
        endpoint = "/get_and_search/"
        if self.path.startswith(endpoint):
            return True
        else:
            self.api_response(404, "Error entering the endpoint")
            return False

    def build_query(self, query_params):
        """
        Builds the SQL query based on the query parameters.
        """
        query = """
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

        conditions = []

        if 'year' in query_params:
            conditions.append("p.year = {}".format(query_params['year'][0]))

        if 'city' in query_params:
            conditions.append("p.city = '{}'".format(query_params['city'][0]))

        if 'state' in query_params:
            conditions.append("s.name = '{}'".format(
                query_params['state'][0]))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query

    def execute_query(self, connection, query):
        """
        Executes the SQL query.
        """
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def response(self, result):
        """
        Sends the response with the result.
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        result_json = json.dumps(result).encode()
        self.wfile.write(result_json)

    def handle_database_connection_error(self):
        """
        Handles the error when there is an issue with the database connection.
        """
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(
            {"error": "Error connecting to the database"}).encode())

    def api_response(self, code, message):
        """
        Send an response.
        """
        self.send_response(code)  # Cambiado a un código de estado 400
        self.send_header("Content-type",  "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(
            {"messaje": message}).encode())
