# PyCiudad

![Logo PyCiudad](docs/pyCiudad_logo.webp)

Una librería Python para interactuar con la API REST de CartoCiudad del Instituto Geográfico Nacional de España.

## Descripción

PyCiudad es una biblioteca orientada a objetos que facilita el acceso a los servicios de geocodificación de CartoCiudad, permitiendo:

- Geocodificación por identificador geográfico (texto a coordenadas)
- Geocodificación inversa (coordenadas a dirección)
- Búsqueda de candidatos por texto
- Geolocalización de entidades específicas

## Instalación

### Desde GitHub (recomendado)

```bash
pip install git+https://github.com/PedroOrtix/PyCiudad.git
```

### Desde PyPI (próximamente)

```bash
pip install pyciudad
```

### Requisitos

- Python 3.11 o superior
- Dependencias: requests, pydantic, typing-extensions

## Uso básico

```python
from pyciudad import CartoCiudad

# Inicializar el cliente
cartociudad = CartoCiudad()

# Buscar candidatos
candidatos = cartociudad.buscar_candidatos("Calle Iglesia 5, Madrid")
for candidato in candidatos:
    print(f"{candidato.direccion} - {candidato.municipio}, {candidato.provincia}")

# Geocodificar una dirección
ubicacion = cartociudad.geocodificar("Calle Iglesia 5, Madrid")
print(f"Coordenadas: {ubicacion.latitud}, {ubicacion.longitud}")

# Geocodificación inversa
direccion = cartociudad.geocodificacion_inversa(-3.7037902, 40.4167754)
print(f"Dirección: {direccion.via}, {direccion.numero} - {direccion.municipio}")
```

## Características

- Interfaz Pythonica para todos los servicios de CartoCiudad
- Modelos de datos completos con tipos definidos
- Manejo de excepciones específicas
- Soporte para todos los parámetros de la API
- Documentación completa

## Documentación

- [Guía de uso](docs/guia_uso.md): Documentación detallada sobre cómo utilizar la librería
- [Ejemplos](ejemplos/): Scripts de ejemplo para casos de uso comunes

## Autor

Desarrollado por [PedroOrtix](https://github.com/PedroOrtix)

## Licencia

MIT 