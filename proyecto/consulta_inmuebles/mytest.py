import json
from http.server import HTTPServer
import socketserver
import threading
import urllib.request
from unittest import TestCase
from unittest.mock import patch, MagicMock

from consulta_handler import RequestHandler, validate_path


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

    def test_get_request_not_matches(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/?year=2020&city=Medellin&state=en_venta')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, str)

    def test_get_request_with_invalid_state_parameter(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/?year=2020&city=Medellin&state=invalido')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIn('Estado no permitido', response_data['message'])

    def test_get_request_without_parameters(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, list)

    def test_get_request_with_one_response(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/?city=bucaramanga&state=en_venta&year=2021')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, list)

    def test_parsed_path_equal_to_endpoint(self):
        parsed_path = urllib.parse.urlparse("/get_and_search/")
        result = validate_path(self, parsed_path)
        self.assertTrue(result)

    # returns False and sends a 400 error if parsed_path is None
    def test_parsed_path_none(self):
        parsed_path = None
        with self.assertRaises(Exception) as context:
            try:
                validate_path(self, parsed_path)
            except AttributeError as e:
                self.assertEqual(
                    str(e), "'AttributeError' object has no attribute 'code'")
                self.assertEqual(
                    context.exception.__class__.__name__, 'AttributeError')
            else:
                self.fail("Expected an AttributeError to be raised")
