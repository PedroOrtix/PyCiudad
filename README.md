<div align="center">

![Logo PyCiudad](docs/pyCiudad_logo.webp)

# PyCiudad

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://pypi.org/classifiers/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)](https://github.com/PedroOrtix/PyCiudad)

**Una librería Python moderna y orientada a objetos para interactuar con la API REST de CartoCiudad del Instituto Geográfico Nacional de España.**

</div>

---

## 📋 Tabla de Contenidos

- [🚀 Características](#-características)
- [💡 ¿Por qué PyCiudad?](#-por-qué-pyciudad)
- [📦 Instalación](#-instalación)
- [🛠️ Uso básico](#️-uso-básico)
- [📚 Ejemplos avanzados](#-ejemplos-avanzados)
- [📖 Documentación](#-documentación)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contribuir](#-contribuir)
- [👨‍💻 Autor](#-autor)
- [📄 Licencia](#-licencia)

---

## 🚀 Características

| Funcionalidad | Descripción |
|---------------|-------------|
| 🗺️ **Geocodificación** | Conversión de direcciones de texto a coordenadas geográficas |
| 📍 **Geocodificación inversa** | Conversión de coordenadas a direcciones legibles |
| 🔍 **Búsqueda de candidatos** | Búsqueda inteligente de posibles ubicaciones |
| 🏢 **Geolocalización de entidades** | Localización de entidades específicas (municipios, provincias, etc.) |
| 🐍 **Interfaz Pythonica** | API diseñada siguiendo las mejores prácticas de Python |
| 📊 **Modelos tipados** | Uso de Pydantic para validación y tipado de datos |
| ⚡ **Manejo de errores** | Excepciones específicas para diferentes tipos de errores |
| 📚 **Documentación completa** | Guías detalladas y ejemplos de uso |

---

## 💡 ¿Por qué PyCiudad?

PyCiudad simplifica el acceso a los servicios de CartoCiudad del IGN España, proporcionando:

- **Simplicidad**: Interfaz clara y fácil de usar
- **Robustez**: Manejo de errores y validación de datos
- **Flexibilidad**: Soporte completo para todos los parámetros de la API
- **Calidad**: Código bien estructurado y documentado
- **Tipado**: Soporte completo para type hints

---

## 📦 Instalación

### Requisitos del sistema

- **Python**: 3.11 o superior
- **Sistema operativo**: Linux, macOS, Windows
- **Conexión a internet**: Requerida para acceder a la API de CartoCiudad

### Instalación desde GitHub

```bash
pip install git+https://github.com/PedroOrtix/PyCiudad.git
```

### Instalación para desarrollo

```bash
git clone https://github.com/PedroOrtix/PyCiudad.git
cd PyCiudad
pip install -e .
```

### Dependencias

```bash
# Dependencias principales
requests>=2.25.0
pydantic>=2.0.0
typing-extensions>=4.0.0
```

---

## 🛠️ Uso básico

### Inicialización

```python
from pyciudad import CartoCiudad

# Inicializar el cliente
cartociudad = CartoCiudad()
```

### Geocodificación (Dirección → Coordenadas)

```python
# Geocodificar una dirección
ubicacion = cartociudad.geocodificar("Calle Iglesia 5, Madrid")
print(f"📍 Coordenadas: {ubicacion.latitud}, {ubicacion.longitud}")
# Salida: 📍 Coordenadas: 40.4167754, -3.7037902
```

### Geocodificación inversa (Coordenadas → Dirección)

```python
# Obtener dirección desde coordenadas
direccion = cartociudad.geocodificacion_inversa(-3.7037902, 40.4167754)
print(f"🏠 Dirección: {direccion.via}, {direccion.numero} - {direccion.municipio}")
```

### Búsqueda de candidatos

```python
# Buscar candidatos para una consulta
candidatos = cartociudad.buscar_candidatos("Calle Iglesia 5, Madrid")

for candidato in candidatos:
    print(f"📍 {candidato.direccion}")
    print(f"🏙️ {candidato.municipio}, {candidato.provincia}")
    print(f"⭐ Relevancia: {candidato.relevancia}")
    print("---")
```

---

## 📚 Ejemplos avanzados

<details>
<summary>🔍 <strong>Búsqueda con filtros</strong></summary>

```python
# Búsqueda con parámetros específicos
candidatos = cartociudad.buscar_candidatos(
    texto="Plaza Mayor",
    limite=5,
    tipo_entidad="municipio"
)
```

</details>

<details>
<summary>🗺️ <strong>Trabajar con geometrías WKT</strong></summary>

```python
# Obtener geometría en formato WKT
ubicacion = cartociudad.geocodificar("Madrid", incluir_geometria=True)
if ubicacion.geometria_wkt:
    print(f"🗺️ Geometría: {ubicacion.geometria_wkt}")
```

</details>

<details>
<summary>⚠️ <strong>Manejo de errores</strong></summary>

```python
from pyciudad.excepciones import CartoCiudadError, APIError

try:
    ubicacion = cartociudad.geocodificar("Dirección inexistente")
except APIError as e:
    print(f"❌ Error de API: {e}")
except CartoCiudadError as e:
    print(f"❌ Error general: {e}")
```

</details>

Para más ejemplos detallados, consulta la carpeta [`ejemplos/`](ejemplos/).

---

## 📖 Documentación

| Recurso | Descripción |
|---------|-------------|
| [📘 Guía de uso](docs/guia_uso.md) | Documentación completa con todos los métodos y parámetros |
| [💡 Ejemplos](ejemplos/) | Scripts de ejemplo para casos de uso comunes |
| [📋 API Reference](docs/CartoCiudad_ServiciosWeb.pdf) | Documentación oficial de CartoCiudad |

---

## 🛣️ Roadmap

### Próximas características

- [ ] 📦 Publicación en PyPI
- [ ] 🧪 Ampliación de tests de integración
- [ ] 📊 Soporte para más formatos de geometría
- [ ] 🚀 Optimización de rendimiento
- [ ] 📚 Más ejemplos de uso

---

### Desarrollo local

```bash
# Clonar el repositorio
git clone https://github.com/PedroOrtix/PyCiudad.git
cd PyCiudad

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest
```

---

## 👨‍💻 Autor

**PedroOrtix**
- GitHub: [@PedroOrtix](https://github.com/PedroOrtix)
- Email: pedro.ortiz@alumnos.upm.es

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">
<strong>⭐ Si te gusta PyCiudad, ¡dale una estrella al repositorio! ⭐</strong>
</div> 