# Importamos unittest, que es la librería estándar de Python para hacer tests unitarios.
import unittest

# Importamos 'patch' y 'Mock' para simular comportamientos y evitar llamadas reales a servicios externos (como APIs).
from unittest.mock import patch, Mock

# Importamos la clase a probar (PyJMQKrill) y una excepción personalizada que lanza (APIError)
from jmq_krill.krill_api import PyJMQKrill, APIError


# Creamos una clase que agrupa todos los tests que queremos hacer sobre PyJMQKrill.
# Esta clase hereda de unittest.TestCase, lo que indica que contiene pruebas unitarias.
class TestPyJMQKrill(unittest.TestCase):
    # Este método se ejecuta automáticamente antes de cada test individual.
    # Se usa para crear un entorno común, como objetos compartidos.
    def setUp(self):
        self.host = "http://example.com"
        self.username = "user"
        self.password = "pass"
        self.client = PyJMQKrill(self.host, self.username, self.password)

    # Test 1: Verificamos que el constructor de PyJMQKrill lanza un ValueError si los parámetros están vacíos
    def test_init_invalid_params(self):
        with self.assertRaises(ValueError):  # Esperamos que se lance un ValueError
            PyJMQKrill("", "user", "pass")  # Host vacío
        with self.assertRaises(ValueError):
            PyJMQKrill(self.host, "", "pass")  # Usuario vacío
        with self.assertRaises(ValueError):
            PyJMQKrill(self.host, "user", "")  # Contraseña vacía

    # Test 2: Simulamos un login exitoso usando patch para evitar una llamada HTTP real
    @patch("jmq_krill.krill_api.requests.Session")  # 'patch' reemplaza la clase 'Session' con un mock
    def test_login_success(self, mock_session_class):
        # Creamos una instancia simulada de la sesión HTTP
        mock_session = mock_session_class.return_value

        # Simulamos que la sesión tiene un diccionario de headers (evita errores en la implementación real)
        mock_session.headers = {}  # <- esto evita errores si tu código intenta modificar headers directamente

        # Creamos una respuesta simulada como si fuera una respuesta real del servidor
        mock_response = Mock()
        mock_response.status_code = 200  # Código HTTP de éxito
        mock_response.json.return_value = {"access": "token123"}  # Simulamos el cuerpo de la respuesta

        # Indicamos que cuando se llame a session.request, devuelva la respuesta simulada
        mock_session.request.return_value = mock_response

        # Creamos el cliente (se usará el mock)
        client = PyJMQKrill(self.host, self.username, self.password)

        # Llamamos a login, que usará el mock
        token = client.login()

        # Verificamos que el token devuelto sea correcto
        self.assertEqual(token, "token123")
        # Verificamos que el token fue guardado en el objeto
        self.assertEqual(client.token, "token123")
        # Verificamos que se haya añadido la cabecera Authorization en la sesión
        self.assertIn("Authorization", client.session.headers)

    # Test 3: Simulamos un fallo en el login (por ejemplo, usuario incorrecto)
    @patch("jmq_krill.krill_api.requests.Session")
    def test_login_failure(self, mock_session_class):
        mock_session = mock_session_class.return_value

        # Simulamos una respuesta con error 401 (no autorizado)
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_session.request.return_value = mock_response

        # Creamos el cliente y probamos login
        client = PyJMQKrill(self.host, self.username, self.password)

        # Verificamos que se lanza la excepción APIError
        with self.assertRaises(APIError) as context:
            client.login()
        # Verificamos que el mensaje contiene "HTTP 401"
        self.assertIn("HTTP 401", str(context.exception))

    # Test 4: Simulamos que se hace una petición sin haber hecho login antes (token es None)
    @patch("jmq_krill.krill_api.requests.Session")
    def test_request_no_token(self, mock_session_class):
        mock_session = mock_session_class.return_value
        # No se llama a login -> token sigue siendo None
        with self.assertRaises(APIError):
            self.client._request("GET", "/api/v2/isp/cpes/")

    # Test 5: Verificamos que el método get_cpes_by_gen_equipos lanza ValueError si se le pasa un parámetro vacío
    def test_get_cpes_by_gen_equipos_invalid(self):
        self.client.token = "token"  # Simulamos que el cliente ya tiene un token
        with self.assertRaises(ValueError):
            self.client.get_cpes_by_gen_equipos("")  # Le pasamos un valor inválido


# Este bloque se asegura que si ejecutamos este archivo directamente con `python test_file.py`,
# se ejecuten todos los tests definidos arriba.
if __name__ == '__main__':
    unittest.main()
