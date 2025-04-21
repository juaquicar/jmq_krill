# jmq_krill

**Paquete de Integración Krill con Python**

![PyPI version](https://img.shields.io/pypi/v/jmq_krill) ![License](https://img.shields.io/badge/license-MIT-blue)

## Descripción

`jmq_krill` es un cliente en Python para interactuar con la API de Krill, facilitando:

- Autenticación y gestión de tokens.
- Consultas de CPEs por topología.
- Obtención de información en tiempo real de un CPE.
- Recuperación del estado de ONUs en una OLT específica.
- Paginación automática de resultados de monitoring.

## Instalación

Instala el paquete desde PyPI:

```bash
pip install jmq_krill
```

O clona el repositorio y construye en modo editable:

```bash
git clone https://github.com/juaquicar/jmq_krill.git
cd jmq_krill
pip install -e .
```

## Requisitos

- Python 3.6 o superior
- Dependencias definidas en `requirements.txt` (actualmente solo `requests`)

## Uso

```python
from jmq_krill.krill_api import PyJMQKrill, APIError

client = PyJMQKrill(
    host="https://api.tudominio.com", 
    username="usuario", 
    password="contraseña"
)

try:
    # Autenticación
    token = client.login()
    print(f"Token obtenido: {token}")

    # Ejemplo: obtener CPEs por topología
    cpes = client.get_cpes_by_gen_equipos("topologia-uuid")
    print(cpes)

    # Ejemplo: información de un CPE específico
    info = client.get_cpe_info("cpe-id")
    print(info)

    # Ejemplo: estado de ONUs en una OLT
    status = client.get_cpes_by_olt("olt-name", frame=0, slot=1, port=2)
    print(status)

    # Ejemplo: paginación de monitoring
    all_cpes = client.get_cpes_monitoring()
    print(f"Total CPEs: {len(all_cpes)}")

except APIError as e:
    print("Error en API:", e)
```

## Ejemplos

En el directorio `Examples/` encontrarás archivos JSON con respuestas de la API para:

- `Example_get_cpe_info.json`
- `Example_get_cpes_by_gen_equipos.json`
- `Example_get_cpes_by_olt.json`
- `Example_get_cpes_monitoring.json`

También hay un script de ejemplo en `tests/Example.py`.

## Tests

Los tests unitarios están en `tests/TestUnittest.py`. Para ejecutarlos:

```bash
pytest tests
```

## Estructura de proyecto

```
├── Examples/                # Ejemplos de respuestas JSON
├── jmq_krill/               # Código fuente del paquete
│   ├── __init__.py
│   └── krill_api.py
├── tests/                   # Tests y ejemplos de uso
│   ├── Example.py
│   └── TestUnittest.py
├── LICENSE
├── MANIFEST.in
├── pyproject.toml           # Configuración de proyecto
├── README.md                # Este archivo
├── requirements.txt
```

## Contribuyendo

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y añade tests.
4. Abre un Pull Request describiendo tu propuesta.

## Licencia

Este proyecto está bajo la licencia MIT. Véase el archivo [LICENSE](LICENSE) para más detalles.


## Enlaces

- Homepage: https://github.com/juaquicar/jmq_krill
- PyPI: https://pypi.org/project/jmq_krill
