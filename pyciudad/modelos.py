"""
Modelos de datos para PyCartoCiudad
"""

import re
from enum import Enum
from typing import List, Dict, Optional, Any, Union, Tuple
from pydantic import BaseModel, Field, validator, field_validator, ConfigDict


class TipoEntidad(str, Enum):
    """Tipos de entidades disponibles en CartoCiudad."""
    CALLEJERO = "callejero"  # Viales urbanos
    PORTAL = "portal"  # Portal o punto kilométrico
    CARRETERA = "carretera"  # Viales interurbanos
    CODIGO_POSTAL = "Codpost"  # Código postal
    MUNICIPIO = "municipio"
    PROVINCIA = "provincia"
    COMUNIDAD_AUTONOMA = "comunidad autonoma"
    TOPONIMO = "toponimo"
    POBLACION = "poblacion"
    EXPENDEDURIA = "expendeduria"
    PUNTO_RECARGA_ELECTRICA = "punto_recarga_electrica"
    NGBE = "ngbe"  # Topónimos orográficos del NGBE
    REF_CATASTRAL = "refcatastral"


class EntidadBase(BaseModel):
    """Modelo base para todas las entidades de CartoCiudad."""
    id: Optional[str] = None
    type: Optional[str] = None  # Cambiado de TipoEntidad a str para mayor flexibilidad
    address: Optional[str] = None
    tip_via: Optional[str] = None
    muni: Optional[str] = None
    muniCode: Optional[str] = None
    province: Optional[str] = None
    provinceCode: Optional[str] = None
    comunidadAutonoma: Optional[str] = None
    comunidadAutonomaCode: Optional[str] = None
    poblacion: Optional[str] = None
    postalCode: Optional[str] = None
    countryCode: Optional[str] = Field(default="011")  # Por defecto España
    refCatastral: Optional[str] = None
    state: Optional[int] = None
    stateMsg: Optional[str] = None

    model_config = ConfigDict(extra="allow")  # Permitir campos adicionales


class Candidato(EntidadBase):
    """Modelo para candidatos retornados por el método candidates."""
    portalNumber: Optional[Union[str, int]] = None  # Puede ser int o str
    noNumber: Optional[bool] = None
    extension: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

    @field_validator('portalNumber', mode='before')
    def validar_portal_number(cls, v):
        """Convierte el número de portal a string si es necesario."""
        if v is not None:
            return str(v)
        return v

    @property
    def direccion(self) -> str:
        """Devuelve la dirección formateada."""
        return self.address or ""
    
    @property
    def municipio(self) -> str:
        """Devuelve el nombre del municipio."""
        return self.muni or ""
    
    @property
    def provincia(self) -> str:
        """Devuelve el nombre de la provincia."""
        return self.province or ""
    
    @property
    def codigo_postal(self) -> str:
        """Devuelve el código postal."""
        return self.postalCode or ""
    
    @property
    def latitud(self) -> Optional[float]:
        """Devuelve la latitud."""
        return self.lat
    
    @property
    def longitud(self) -> Optional[float]:
        """Devuelve la longitud."""
        return self.lng


class Ubicacion(EntidadBase):
    """Modelo para ubicaciones retornadas por el método find."""
    portalNumber: Optional[Union[str, int]] = None  # Puede ser int o str
    noNumber: Optional[bool] = None
    extension: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    geom: Optional[Union[Dict[str, Any], str]] = None  # Puede ser un diccionario o una cadena
    
    @field_validator('portalNumber', mode='before')
    def validar_portal_number(cls, v):
        """Convierte el número de portal a string si es necesario."""
        if v is not None:
            return str(v)
        return v
    
    @property
    def direccion(self) -> str:
        """Devuelve la dirección formateada."""
        return self.address or ""
    
    @property
    def latitud(self) -> Optional[float]:
        """Devuelve la latitud."""
        return self.lat
    
    @property
    def longitud(self) -> Optional[float]:
        """Devuelve la longitud."""
        return self.lng
    
    @property
    def municipio(self) -> str:
        """Devuelve el nombre del municipio."""
        return self.muni or ""
    
    @property
    def provincia(self) -> str:
        """Devuelve el nombre de la provincia."""
        return self.province or ""
    
    @property
    def geometria(self) -> Optional[Union[Dict[str, Any], str]]:
        """Devuelve la geometría de la entidad."""
        return self.geom
    
    def extraer_coordenadas_wkt(self) -> Optional[Tuple[float, float]]:
        """
        Extrae las coordenadas de una geometría WKT.
        
        Returns:
            Tupla (longitud, latitud) o None si no se puede extraer
        """
        if not self.geom or not isinstance(self.geom, str):
            return None
        
        # Intentar extraer coordenadas de un POINT WKT
        match = re.search(r'POINT\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)', self.geom)
        if match:
            try:
                lon = float(match.group(1))
                lat = float(match.group(2))
                return (lon, lat)
            except (ValueError, IndexError):
                return None
        
        return None


class Direccion(EntidadBase):
    """Modelo para direcciones retornadas por el método reverseGeocode."""
    portalNumber: Optional[Union[str, int]] = None  # Puede ser int o str
    noNumber: Optional[bool] = None
    extension: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    geom: Optional[Union[Dict[str, Any], str]] = None  # Puede ser un diccionario o una cadena
    
    @field_validator('portalNumber', mode='before')
    def validar_portal_number(cls, v):
        """Convierte el número de portal a string si es necesario."""
        if v is not None:
            return str(v)
        return v
    
    @property
    def via(self) -> str:
        """Devuelve el nombre de la vía."""
        return self.address or ""
    
    @property
    def numero(self) -> str:
        """Devuelve el número del portal."""
        return self.portalNumber or ""
    
    @property
    def municipio(self) -> str:
        """Devuelve el nombre del municipio."""
        return self.muni or ""
    
    @property
    def provincia(self) -> str:
        """Devuelve el nombre de la provincia."""
        return self.province or ""
    
    @property
    def codigo_postal(self) -> str:
        """Devuelve el código postal."""
        return self.postalCode or ""
    
    @property
    def latitud(self) -> Optional[float]:
        """Devuelve la latitud."""
        return self.lat
    
    @property
    def longitud(self) -> Optional[float]:
        """Devuelve la longitud."""
        return self.lng
    
    def extraer_coordenadas_wkt(self) -> Optional[Tuple[float, float]]:
        """
        Extrae las coordenadas de una geometría WKT.
        
        Returns:
            Tupla (longitud, latitud) o None si no se puede extraer
        """
        if not self.geom or not isinstance(self.geom, str):
            return None
        
        # Intentar extraer coordenadas de un POINT WKT
        match = re.search(r'POINT\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)', self.geom)
        if match:
            try:
                lon = float(match.group(1))
                lat = float(match.group(2))
                return (lon, lat)
            except (ValueError, IndexError):
                return None
        
        return None 