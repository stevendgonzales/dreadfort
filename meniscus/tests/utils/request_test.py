from meniscus.api.utils.request import http_request

from mock import MagicMock
from mock import patch

from httpretty import HTTPretty
from httpretty import httprettified

import falcon
import requests
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WhenTestingUtilsRequest())
    return suite


class WhenTestingUtilsRequest(unittest.TestCase):

    def setUp(self):
        self.requests = MagicMock()
        self.url = 'http://localhost:8080/somewhere'
        self.json_payload = u'{}'

    @httprettified
    def test_should_raise_value_error(self):
        HTTPretty.register_uri(HTTPretty.PATCH, self.url,
                               body=self.json_payload,
                               content_type="application/json")

        with self.assertRaises(ValueError):
            http_request(self.url, self.json_payload, 'PATCH')

    @httprettified
    def test_should_return_http_200(self):
        HTTPretty.register_uri(HTTPretty.POST, self.url,
                               body=self.json_payload,
                               content_type="application/json",
                               status=200)

        self.assertTrue(http_request(self.url,
                                     self.json_payload,
                                     http_verb='POST'),
                        falcon.HTTP_200)

    @httprettified
    def test_should_cause_a_connection_exception(self):
        HTTPretty.register_uri(HTTPretty.POST, self.url,
                               body=self.json_payload,
                               content_type="application/json",
                               status=200)

        with self.assertRaises(requests.ConnectionError):
            http_request(self.url, self.json_payload, 'POST')

    def test_should_cause_a_connection_exception(self):
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(requests.ConnectionError):
                mock_method.side_effect = requests.ConnectionError
                http_request(self.url, self.json_payload)

    def test_should_cause_a_http_exception(self):
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(requests.HTTPError):
                mock_method.side_effect = requests.HTTPError
                http_request(self.url, self.json_payload)

    def test_should_cause_a_request_exception(self):
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(requests.RequestException):
                mock_method.side_effect = requests.RequestException
                http_request(self.url, self.json_payload)

if __name__ == '__main__':
    unittest.main()