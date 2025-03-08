"""
Tests para el cliente principal de PyCiudad
"""

import pytest
import json
import responses
from unittest.mock import patch, MagicMock

from pyciudad.cliente import CartoCiudad, CartoCiudadError, APIError, PeticionInvalidaError
from pyciudad.constantes import CANDIDATES_URL, FIND_URL, REVERSE_GEOCODE_URL


# Datos de prueba
RESPUESTA_CANDIDATOS = [
    {
        "id": "280790529087",
        "province": "Madrid",
        "provinceCode": "28",
        "comunidadAutonoma": "Comunidad de Madrid",
        "comunidadAutonomaCode": "13",
        "muni": "Madrid",
        "muniCode": "28079",
        "type": "portal",
        "address": "CALLE IGLESIA 5, Madrid",
        "postalCode": "28019",
        "poblacion": "Madrid",
        "geom": None,
        "tip_via": "CALLE",
        "lat": 40.395794980401,
        "lng": -3.71771161209991,
        "portalNumber": 5,
        "noNumber": False,
        "stateMsg": "",
        "extension": None,
        "state": 0,
        "refCatastral": None,
        "countryCode": "011"
    },
    {
        "id": "491030130195",
        "province": "Zamora",
        "provinceCode": "49",
        "comunidadAutonoma": "Castilla y León",
        "comunidadAutonomaCode": "07",
        "muni": "Madridanos",
        "muniCode": "49103",
        "type": "portal",
        "address": "CALLE IGLESIA 5, Madridanos",
        "postalCode": "49157",
        "poblacion": "Madridanos",
        "geom": None,
        "tip_via": "CALLE",
        "lat": 41.478594022696,
        "lng": -5.60384855916362,
        "portalNumber": 5,
        "noNumber": False,
        "stateMsg": "",
        "extension": None,
        "state": 0,
        "refCatastral": None,
        "countryCode": "011"
    }
]

RESPUESTA_FIND = {
    "id": "2906755300",
    "province": "Málaga",
    "provinceCode": "29",
    "comunidadAutonoma": "Andalucía",
    "comunidadAutonomaCode": "01",
    "muni": "Málaga",
    "muniCode": "29067",
    "type": "toponimo",
    "address": "Estación de metro Clínico",
    "postalCode": "29010",
    "poblacion": "Málaga",
    "geom": "POINT(-4.478817 36.716583)",
    "tip_via": "Estación de metro",
    "lat": 36.716583,
    "lng": -4.478817,
    "portalNumber": None,
    "noNumber": None,
    "stateMsg": "",
    "extension": None,
    "state": 0,
    "countryCode": "011",
    "refCatastral": None
}

RESPUESTA_REVERSE = {
    "id": "2462500046202",
    "province": "València/Valencia",
    "provinceCode": "46",
    "comunidadAutonoma": "Comunitat Valenciana",
    "comunidadAutonomaCode": "10",
    "muni": "València",
    "muniCode": "46250",
    "type": "portal",
    "address": "BLASCO IBÁÑEZ",
    "postalCode": "46022",
    "poblacion": "València",
    "geom": "POINT(-0.344584775170868 39.4724113171326)",
    "tip_via": "AVENIDA",
    "lat": 39.472411317132554,
    "lng": -0.3445847751708685,
    "portalNumber": 146,
    "noNumber": False,
    "stateMsg": "",
    "extension": None,
    "state": 0,
    "countryCode": "011",
    "refCatastral": None
}


class TestCartoCiudad:
    """Tests para el cliente CartoCiudad."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.cliente = CartoCiudad()
    
    @responses.activate
    def test_buscar_candidatos(self):
        """Test para el método buscar_candidatos."""
        # Configurar respuesta mock
        responses.add(
            responses.GET,
            f"{CANDIDATES_URL}?q=Calle+Iglesia+5%2C+Madrid&limit=2&countrycodes=es",
            json=RESPUESTA_CANDIDATOS,
            status=200,
        )
        
        # Ejecutar método
        candidatos = self.cliente.buscar_candidatos("Calle Iglesia 5, Madrid", limite=2)
        
        # Verificar resultados
        assert len(candidatos) == 2
        assert candidatos[0].id == "280790529087"
        assert candidatos[0].address == "CALLE IGLESIA 5, Madrid"
        assert candidatos[0].type == "portal"
        assert candidatos[0].portalNumber == "5"
        assert candidatos[0].municipio == "Madrid"
        assert candidatos[0].provincia == "Madrid"
        assert candidatos[0].latitud == 40.395794980401
        assert candidatos[0].longitud == -3.71771161209991
    
    @responses.activate
    def test_geocodificar(self):
        """Test para el método geocodificar."""
        # Configurar respuesta mock
        responses.add(
            responses.GET,
            f"{FIND_URL}?q=Estaci%C3%B3n+de+metro+Cl%C3%ADnico%2C+M%C3%A1laga",
            json=RESPUESTA_FIND,
            status=200,
        )
        
        # Ejecutar método
        ubicacion = self.cliente.geocodificar("Estación de metro Clínico, Málaga")
        
        # Verificar resultados
        assert ubicacion.id == "2906755300"
        assert ubicacion.type == "toponimo"
        assert ubicacion.address == "Estación de metro Clínico"
        assert ubicacion.muni == "Málaga"
        assert ubicacion.province == "Málaga"
        assert ubicacion.latitud == 36.716583
        assert ubicacion.longitud == -4.478817
        assert ubicacion.geom == "POINT(-4.478817 36.716583)"
        
        # Verificar extracción de coordenadas WKT
        coords = ubicacion.extraer_coordenadas_wkt()
        assert coords == (-4.478817, 36.716583)
    
    @responses.activate
    def test_geocodificacion_inversa(self):
        """Test para el método geocodificacion_inversa."""
        # Configurar respuesta mock
        responses.add(
            responses.GET,
            f"{REVERSE_GEOCODE_URL}?lon=-0.344579&lat=39.472413",
            json=RESPUESTA_REVERSE,
            status=200,
        )
        
        # Ejecutar método
        direccion = self.cliente.geocodificacion_inversa(-0.344579, 39.472413)
        
        # Verificar resultados
        assert direccion.id == "2462500046202"
        assert direccion.type == "portal"
        assert direccion.address == "BLASCO IBÁÑEZ"
        assert direccion.tip_via == "AVENIDA"
        assert direccion.muni == "València"
        assert direccion.province == "València/Valencia"
        assert direccion.via == "BLASCO IBÁÑEZ"
        assert direccion.numero == "146"
        assert direccion.codigo_postal == "46022"
    
    @responses.activate
    def test_error_api(self):
        """Test para manejo de errores de la API."""
        # Configurar respuesta de error
        responses.add(
            responses.GET,
            f"{CANDIDATES_URL}?q=invalid&limit=10&countrycodes=es",
            json={"error": "Error en la API"},
            status=400,
        )
        
        # Verificar que se lance la excepción
        with pytest.raises(APIError) as excinfo:
            self.cliente.buscar_candidatos("invalid")
        
        assert "Error HTTP" in str(excinfo.value)
    
    def test_validacion_parametros(self):
        """Test para validación de parámetros."""
        # Consulta vacía en buscar_candidatos
        with pytest.raises(PeticionInvalidaError) as excinfo:
            self.cliente.buscar_candidatos("")
        
        assert "consulta no puede estar vacía" in str(excinfo.value)
        
        # Coordenadas inválidas en geocodificacion_inversa (fuera del rango de España)
        with pytest.raises(PeticionInvalidaError) as excinfo:
            self.cliente.geocodificacion_inversa(100.0, 50.0)
        
        assert "Longitud fuera del rango válido" in str(excinfo.value)
    
    @patch('pyciudad.cliente.requests.get')
    def test_timeout(self, mock_get):
        """Test para timeout en la petición."""
        # Configurar mock para simular timeout
        from requests.exceptions import Timeout
        mock_get.side_effect = Timeout("Connection timed out")
        
        # Verificar que se lance la excepción
        with pytest.raises(APIError) as excinfo:
            self.cliente.buscar_candidatos("Calle Iglesia 5, Madrid")
        
        assert "Tiempo de espera agotado" in str(excinfo.value)
    
    @patch('pyciudad.cliente.requests.get')
    def test_error_conexion(self, mock_get):
        """Test para error de conexión."""
        # Configurar mock para simular error de conexión
        from requests.exceptions import ConnectionError
        mock_get.side_effect = ConnectionError("Connection refused")
        
        # Verificar que se lance la excepción
        with pytest.raises(APIError) as excinfo:
            self.cliente.buscar_candidatos("Calle Iglesia 5, Madrid")
        
        assert "Error de conexión" in str(excinfo.value) 