"""
Utilidades para PyCartoCiudad
"""

from typing import Dict, Any, List, Optional, Union
import urllib.parse
from .excepciones import PeticionInvalidaError


def validar_coordenadas(longitud: float, latitud: float) -> None:
    """
    Valida que las coordenadas estén dentro de rangos lógicos para España.
    
    Args:
        longitud: Coordenada de longitud en grados decimales
        latitud: Coordenada de latitud en grados decimales
        
    Raises:
        PeticionInvalidaError: Si las coordenadas están fuera de rangos válidos
    """
    # Rango aproximado para España (con margen)
    if not (-10.0 <= longitud <= 5.0):
        raise PeticionInvalidaError(
            "Longitud fuera del rango válido para España (-10.0 a 5.0)",
            parametro="longitud"
        )
    
    if not (35.0 <= latitud <= 44.0):
        raise PeticionInvalidaError(
            "Latitud fuera del rango válido para España (35.0 a 44.0)",
            parametro="latitud"
        )


def construir_parametros_filtro(
    no_process: Optional[List[str]] = None,
    filtros_geograficos: Optional[Dict[str, Union[str, List[str]]]] = None,
    **kwargs
) -> Dict[str, str]:
    """
    Construye los parámetros de filtro para las peticiones a la API.
    
    Args:
        no_process: Lista de tipos de entidades a excluir
        filtros_geograficos: Diccionario con filtros geográficos
        **kwargs: Parámetros adicionales
        
    Returns:
        Diccionario con los parámetros listos para la petición
    """
    params = {}
    
    # Añadir no_process si existe
    if no_process and isinstance(no_process, list) and len(no_process) > 0:
        params["no_process"] = ",".join(no_process)
    
    # Añadir filtros geográficos
    if filtros_geograficos:
        for nombre, valor in filtros_geograficos.items():
            if valor:
                if isinstance(valor, list):
                    params[nombre] = ",".join(valor)
                else:
                    params[nombre] = valor
    
    # Añadir el resto de parámetros
    for nombre, valor in kwargs.items():
        if valor is not None:
            params[nombre] = str(valor)
    
    return params


def url_encode(texto: str) -> str:
    """
    Codifica un texto para usarlo en URLs.
    
    Args:
        texto: Texto a codificar
        
    Returns:
        Texto codificado para URL
    """
    return urllib.parse.quote(texto) 