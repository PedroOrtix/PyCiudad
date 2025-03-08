"""
Constantes utilizadas en la librería PyCartoCiudad
"""

# URLs base de la API
BASE_URL = "https://www.cartociudad.es/geocoder/api/geocoder"
CANDIDATES_URL = f"{BASE_URL}/candidates"
FIND_URL = f"{BASE_URL}/find"
REVERSE_GEOCODE_URL = f"{BASE_URL}/reverseGeocode"

# Valores por defecto
DEFAULT_COUNTRY_CODE = "es"
DEFAULT_LIMIT = 10  # Aunque la API permite hasta 33

# Tipos de filtros
FILTROS_TIPO_ENTIDAD = {
    "municipio": "municipio",
    "provincia": "provincia", 
    "comunidad_autonoma": "comunidad autonoma",
    "poblacion": "poblacion",
    "toponimo": "toponimo",
    "expendeduria": "expendeduria",
    "punto_recarga_electrica": "punto_recarga_electrica",
    "ngbe": "ngbe",
    "callejero": "callejero",
    "carretera": "carretera",
    "portal": "portal",
}

# Tipos de filtros geográficos
FILTROS_GEOGRAFICOS = [
    "cod_postal_filter", 
    "municipio_filter", 
    "provincia_filter", 
    "comunidad_autonoma_filter", 
    "poblacion_filter"
]

# Headers para las peticiones HTTP
DEFAULT_HEADERS = {
    "User-Agent": "PyCartoCiudad/0.1.0",
    "Accept": "application/json",
} 