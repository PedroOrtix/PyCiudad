# Guía de Uso de PyCiudad

Esta guía proporciona información detallada sobre cómo utilizar la librería PyCiudad para interactuar con la API REST de CartoCiudad.

## Instalación

### Desde GitHub

```bash
pip install git+https://github.com/PedroOrtix/PyCiudad.git
```

### Requisitos

- Python 3.11 o superior
- Dependencias: requests, pydantic, typing-extensions

## Funcionalidades principales

### 1. Inicializar el cliente

```python
from pyciudad import CartoCiudad

# Cliente básico
cliente = CartoCiudad()

# Cliente con timeout personalizado (en segundos)
cliente = CartoCiudad(timeout=10)

# Cliente con logger personalizado
import logging
logger = logging.getLogger("mi_aplicacion")
cliente = CartoCiudad(logger=logger)
```

### 2. Búsqueda de candidatos

Busca posibles coincidencias para un texto de búsqueda:

```python
# Búsqueda básica
candidatos = cliente.buscar_candidatos("Calle Mayor, Madrid")

# Limitar resultados
candidatos = cliente.buscar_candidatos("Calle Mayor", limite=5)

# Filtrar por tipo de vía
candidatos = cliente.buscar_candidatos("Mayor", tipo_via="CALLE")

# Filtrar por provincia
candidatos = cliente.buscar_candidatos("Calle Mayor", provincia="Madrid")

# Filtrar por municipio
candidatos = cliente.buscar_candidatos("Calle Mayor", municipio="Madrid")

# Acceder a los datos de los candidatos
for candidato in candidatos:
    print(f"Dirección: {candidato.direccion}")
    print(f"Municipio: {candidato.municipio}")
    print(f"Provincia: {candidato.provincia}")
    print(f"Referencia catastral: {candidato.ref_catastral}")
    print(f"Tipo de vía: {candidato.tipo_via}")
    print(f"Coordenadas: {candidato.latitud}, {candidato.longitud}")
```

### 3. Geocodificación

Convierte una dirección en coordenadas geográficas:

```python
# Geocodificación básica
ubicacion = cliente.geocodificar("Plaza Mayor 1, Madrid")

# Acceder a los datos de la ubicación
print(f"Latitud: {ubicacion.latitud}")
print(f"Longitud: {ubicacion.longitud}")
print(f"Dirección: {ubicacion.direccion}")
print(f"Municipio: {ubicacion.municipio}")
print(f"Provincia: {ubicacion.provincia}")
```

### 4. Geocodificación inversa

Convierte coordenadas geográficas en una dirección:

```python
# Geocodificación inversa
direccion = cliente.geocodificacion_inversa(-3.7037902, 40.4167754)

# Acceder a los datos de la dirección
print(f"Vía: {direccion.via}")
print(f"Número: {direccion.numero}")
print(f"Municipio: {direccion.municipio}")
print(f"Provincia: {direccion.provincia}")
print(f"Código postal: {direccion.codigo_postal}")
```

### 5. Manejo de errores

```python
from pyciudad import CartoCiudadError, APIError, PeticionInvalidaError

try:
    ubicacion = cliente.geocodificar("Dirección inexistente")
except PeticionInvalidaError as e:
    print(f"Error en la petición: {e}")
except APIError as e:
    print(f"Error en la API: {e}")
except CartoCiudadError as e:
    print(f"Error general: {e}")
```

## Ejemplos avanzados

Para ejemplos más avanzados, consulta los scripts en la carpeta `ejemplos/` del repositorio:

- `busqueda_basica.py`: Ejemplos básicos de uso
- `filtros_avanzados.py`: Uso de filtros avanzados
- `manejo_errores.py`: Manejo de diferentes tipos de errores
- `geometria_wkt.py`: Trabajo con geometrías WKT 