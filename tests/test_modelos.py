"""
Tests para los modelos de datos de PyCiudad
"""

import pytest
import json
from pyciudad.modelos import Candidato, Ubicacion, Direccion, TipoEntidad, EntidadBase


class TestModelos:
    """Tests para los modelos de datos."""
    
    def test_candidato_basico(self):
        """Test de creación básica de un Candidato."""
        datos = {
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
            "tip_via": "CALLE",
            "lat": 40.395794980401,
            "lng": -3.71771161209991,
            "portalNumber": 5,
            "noNumber": False,
        }
        
        candidato = Candidato.model_validate(datos)
        
        assert candidato.id == "280790529087"
        assert candidato.type == "portal"
        assert candidato.address == "CALLE IGLESIA 5, Madrid"
        assert candidato.lat == 40.395794980401
        assert candidato.lng == -3.71771161209991
        
        # Probar propiedades
        assert candidato.direccion == "CALLE IGLESIA 5, Madrid"
        assert candidato.municipio == "Madrid"
        assert candidato.provincia == "Madrid"
        assert candidato.codigo_postal == "28019"
        assert candidato.latitud == 40.395794980401
        assert candidato.longitud == -3.71771161209991
        
        # Verificar conversión de portalNumber
        assert candidato.portalNumber == "5"
    
    def test_ubicacion_con_geom_wkt(self):
        """Test de Ubicacion con geometría WKT."""
        datos = {
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
        }
        
        ubicacion = Ubicacion.model_validate(datos)
        
        assert ubicacion.id == "2906755300"
        assert ubicacion.type == "toponimo"
        assert ubicacion.address == "Estación de metro Clínico"
        assert ubicacion.geom == "POINT(-4.478817 36.716583)"
        
        # Probar extracción de coordenadas WKT
        coordenadas = ubicacion.extraer_coordenadas_wkt()
        assert coordenadas is not None
        lon, lat = coordenadas
        assert lon == -4.478817
        assert lat == 36.716583
    
    def test_direccion_basica(self):
        """Test de creación básica de una Dirección."""
        datos = {
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
        }
        
        direccion = Direccion.model_validate(datos)
        
        assert direccion.id == "2462500046202"
        assert direccion.type == "portal"
        assert direccion.address == "BLASCO IBÁÑEZ"
        assert direccion.tip_via == "AVENIDA"
        
        # Probar propiedades
        assert direccion.via == "BLASCO IBÁÑEZ"
        assert direccion.numero == "146"
        assert direccion.municipio == "València"
        assert direccion.provincia == "València/Valencia"
        assert direccion.codigo_postal == "46022"
        
        # Probar extracción de coordenadas WKT
        coordenadas = direccion.extraer_coordenadas_wkt()
        assert coordenadas is not None
        lon, lat = coordenadas
        assert lon == -0.344584775170868
        assert lat == 39.4724113171326
    
    def test_geometria_invalida(self):
        """Test de manejo de geometría WKT inválida."""
        # Caso con geometría inválida
        datos = {
            "id": "test",
            "type": "test",
            "geom": "INVALID_GEOM",
        }
        
        ubicacion = Ubicacion.model_validate(datos)
        assert ubicacion.extraer_coordenadas_wkt() is None
        
        # Caso con geometría None
        datos = {
            "id": "test",
            "type": "test",
            "geom": None,
        }
        
        ubicacion = Ubicacion.model_validate(datos)
        assert ubicacion.extraer_coordenadas_wkt() is None
        
        # Caso con geometría como diccionario
        datos = {
            "id": "test",
            "type": "test",
            "geom": {"type": "Point", "coordinates": [-4.478817, 36.716583]},
        }
        
        ubicacion = Ubicacion.model_validate(datos)
        assert ubicacion.extraer_coordenadas_wkt() is None
    
    def test_portal_number_conversion(self):
        """Test de conversión de portalNumber."""
        # Caso con portalNumber como entero
        datos = {"portalNumber": 5}
        candidato = Candidato.model_validate(datos)
        assert candidato.portalNumber == "5"
        
        # Caso con portalNumber como string
        datos = {"portalNumber": "10A"}
        candidato = Candidato.model_validate(datos)
        assert candidato.portalNumber == "10A"
        
        # Caso con portalNumber None
        datos = {"portalNumber": None}
        candidato = Candidato.model_validate(datos)
        assert candidato.portalNumber is None 