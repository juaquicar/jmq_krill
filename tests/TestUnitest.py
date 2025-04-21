import unittest
from unittest.mock import patch, Mock
from pyjmqkrill import PyJMQKrill, APIError


class TestPyJMQKrill(unittest.TestCase):
    def setUp(self):
        self.host = "http://example.com"
        self.username = "user"
        self.password = "pass"
        self.client = PyJMQKrill(self.host, self.username, self.password)

    def test_init_invalid_params(self):
        with self.assertRaises(ValueError):
            PyJMQKrill("", "user", "pass")
        with self.assertRaises(ValueError):
            PyJMQKrill(self.host, "", "pass")
        with self.assertRaises(ValueError):
            PyJMQKrill(self.host, "user", "")

    @patch("pyjmqkrill.requests.Session")
    def test_login_success(self, mock_session_class):
        mock_session = mock_session_class.return_value
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access": "token123"}
        mock_session.request.return_value = mock_response

        token = self.client.login()
        self.assertEqual(token, "token123")
        self.assertEqual(self.client.token, "token123")
        self.assertIn("Authorization", self.client.session.headers)

    @patch("pyjmqkrill.requests.Session")
    def test_login_failure(self, mock_session_class):
        mock_session = mock_session_class.return_value
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_session.request.return_value = mock_response

        with self.assertRaises(APIError) as context:
            self.client.login()
        self.assertIn("HTTP 401", str(context.exception))

    @patch("pyjmqkrill.requests.Session")
    def test_request_no_token(self, mock_session_class):
        mock_session = mock_session_class.return_value
        # Sin login -> token None
        with self.assertRaises(APIError):
            self.client._request("GET", "/api/v2/isp/cpes/")

    def test_get_cpes_by_gen_equipos_invalid(self):
        self.client.token = "token"
        with self.assertRaises(ValueError):
            self.client.get_cpes_by_gen_equipos("")

if __name__ == '__main__':
    unittest.main()
