import json
from http.server import HTTPServer
import socketserver
import threading
import urllib.request
from unittest import TestCase
from unittest.mock import patch

from consulta_handler import RequestHandler

# Assuming the RequestHandler class and conectar_base_datos function are defined elsewhere and imported here


class TestRequestHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup a simple HTTP server for testing
        handler = RequestHandler
        # 0 means any free port
        cls.server = HTTPServer(('localhost', 0), handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    @patch('database.conectar_base_datos')
    def test_get_request_with_valid_parameters(self, mock_db):
        # Mock the database connection to return a dummy connection object
        mock_db.return_value = True
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/?year=2020&city=Medellin&state=en_venta')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        print(type(response_data))
        # Assuming the response is a list of properties
        self.assertIsInstance(response_data, str)

    @patch('database.conectar_base_datos')
    def test_get_request_with_database_connection_failure(self, mock_db):
        # Mock the database connection to return None, simulating a failure
        mock_db.return_value = None
        print("RESPONSE: ")
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/?year=2020&city=Medellin&state=en_venta')
        print("RESPONSE: ", response)
        self.assertEqual(response.status, 500)
        response_data = json.loads(response.read().decode())
        self.assertIn('Error al conectar a la base de datos',
                      response_data['error'])

    def test_get_request_with_invalid_state_parameter(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/?year=2020&city=Medellin&state=invalido')
        # Assuming the server still responds with 200 but includes an error message
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIn('Estado no permitido', response_data['error'])
import json
from http.server import HTTPServer
import socketserver
import threading
import urllib.request
from unittest import TestCase
from unittest.mock import patch

# Assuming the RequestHandler class and conectar_base_datos function are defined elsewhere and imported here

class TestRequestHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup a simple HTTP server for testing
        handler = RequestHandler
        cls.server = HTTPServer(('localhost', 0), handler)  # 0 means any free port
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    @patch('database.conectar_base_datos')
    def test_get_request_with_valid_parameters(self, mock_db):
        # Mock the database connection to return a dummy connection object
        mock_db.return_value = True
        response = urllib.request.urlopen(f'http://localhost:{self.port}/?year=2020&city=Medellin&state=en_venta')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, str)  # Assuming the response is a list of properties

    #!PENDIENTE
    @patch('database.conectar_base_datos')
    def test_get_request_with_database_connection_failure(self, mock_db):
        # Mock the database connection to return None, simulating a failure
        mock_db.return_value = None
        response = urllib.request.urlopen(f'http://localhost:{self.port}/?year=2020&city=Medellin&state=en_venta')
        self.assertEqual(response.status, 500)
        response_data = json.loads(response.read().decode())
        self.assertIn('Error al conectar a la base de datos', response_data['error'])

    def test_get_request_with_invalid_state_parameter(self):
        response = urllib.request.urlopen(f'http://localhost:{self.port}/?year=2020&city=Medellin&state=invalido')
        self.assertEqual(response.status, 200)  # Assuming the server still responds with 200 but includes an error message
        response_data = json.loads(response.read().decode())
        self.assertIn('Estado no permitido', response_data['error'])
    