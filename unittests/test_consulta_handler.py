import json
import threading
import urllib.request
from unittest import TestCase
from http.server import HTTPServer

from consulta_inmuebles.validate_type import QueryParams
from consulta_inmuebles.consulta_handler import RequestHandler


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

    # Check if the type returned from a request is a list when no parameters are passed

    def test_get_request_without_parameters(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, list)

    # Check if the type returned from a request is a list when multiple parameters are not passed
    def test_get_request_with_one_response(self):
        response = urllib.request.urlopen(
            f'http://localhost:{self.port}/get_and_search/?city=bucaramanga&state=en_venta&year=2021')
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.read().decode())
        self.assertIsInstance(response_data, list)

    # Returns False and sends a 400 error if parsed_path is None
    def test_parsed_path_none(self):
        with self.assertRaises(Exception) as context:
            try:
                RequestHandler.validate_path(self)
            except AttributeError as e:
                self.assertEqual(
                    str(e), "'AttributeError' object has no attribute 'code'")
                self.assertEqual(
                    context.exception.__class__.__name__, 'AttributeError')
            else:
                self.fail("Expected an AttributeError to be raised")

    # Creating an instance of QueryParams with no arguments should result in an object with all attributes set to None.
    def test_instance_with_no_arguments(self):
        query_params = QueryParams()
        self.assertIsNone(query_params.year)
        self.assertIsNone(query_params.city)
        self.assertIsNone(query_params.state)

    def test_non_integer_year_attribute(self):
        with self.assertRaises(TypeError):
            query_params = QueryParams(year='string')

    # Creating an instance of QueryParams with a non-integer value for the 'year' attribute should not result in a ValidationError being raised.
    def test_non_integer_year_attribute(self):
        query_params = QueryParams(year='2021')
        self.assertEqual(query_params.year, 2021)
