"""
PyCiudad - Librería Python para la API de CartoCiudad del IGN España
"""

__version__ = "0.1.0"

from .cliente import CartoCiudad
from .modelos import (
    Candidato, 
    Ubicacion, 
    Direccion, 
    TipoEntidad,
    EntidadBase
)
from .excepciones import (
    CartoCiudadError,
    APIError,
    PeticionInvalidaError
)

__all__ = [
    "CartoCiudad",
    "Candidato", 
    "Ubicacion", 
    "Direccion",
    "TipoEntidad",
    "EntidadBase",
    "CartoCiudadError",
    "APIError",
    "PeticionInvalidaError"
] 