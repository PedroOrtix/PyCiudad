"""
Tests de integración para PyCiudad.

Estos tests realizan peticiones reales a la API de CartoCiudad.
Para ejecutarlos: pytest tests/test_integracion.py -v
"""

import pytest
from pyciudad import CartoCiudad, CartoCiudadError


@pytest.mark.integracion
class TestIntegracion:
    """Tests de integración con la API real."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.cliente = CartoCiudad(timeout=15)
    
    def test_buscar_candidatos_integracion(self):
        """Test de integración para buscar_candidatos."""
        consulta = "Calle Iglesia 5, Madrid"
        
        candidatos = self.cliente.buscar_candidatos(consulta, limite=2)
        
        # Verificar que haya resultados
        assert len(candidatos) > 0
        
        # Verificar que el primer resultado tenga todos los campos necesarios
        assert candidatos[0].id is not None
        assert candidatos[0].type is not None
        assert candidatos[0].address is not None
        assert candidatos[0].municipio is not None
        assert candidatos[0].provincia is not None
        
        # Si tiene coordenadas, verificar que sean números
        if candidatos[0].latitud is not None:
            assert isinstance(candidatos[0].latitud, float)
        if candidatos[0].longitud is not None:
            assert isinstance(candidatos[0].longitud, float)
    
    def test_geocodificar_integracion(self):
        """Test de integración para geocodificar."""
        consulta = "Estación de metro Clínico, Málaga"
        
        ubicacion = self.cliente.geocodificar(consulta)
        
        # Verificar campos básicos
        assert ubicacion.id is not None
        assert ubicacion.type is not None
        assert ubicacion.address is not None
        assert ubicacion.municipio is not None
        assert ubicacion.provincia is not None
        
        # Verificar coordenadas
        assert ubicacion.latitud is not None
        assert ubicacion.longitud is not None
        assert isinstance(ubicacion.latitud, float)
        assert isinstance(ubicacion.longitud, float)
        
        # Si tiene geometría, verificar que se puedan extraer coordenadas
        if ubicacion.geom and isinstance(ubicacion.geom, str):
            coordenadas = ubicacion.extraer_coordenadas_wkt()
            if coordenadas:
                lon, lat = coordenadas
                assert isinstance(lon, float)
                assert isinstance(lat, float)
    
    def test_geocodificacion_inversa_integracion(self):
        """Test de integración para geocodificacion_inversa."""
        # Coordenadas del centro de Madrid
        lon, lat = -3.7037902, 40.4167754
        
        direccion = self.cliente.geocodificacion_inversa(lon, lat)
        
        # Verificar campos básicos
        assert direccion.id is not None
        assert direccion.type is not None
        assert direccion.via is not None
        assert direccion.municipio is not None
        assert direccion.provincia is not None
        
        # Verificar coordenadas
        assert direccion.latitud is not None
        assert direccion.longitud is not None
        assert isinstance(direccion.latitud, float)
        assert isinstance(direccion.longitud, float)
    
    def test_consulta_invalida(self):
        """Test de integración con consulta que no debería dar resultados."""
        consulta = "xyzabcdeasdksjdhaksjdbakjsd"  # Consulta que no debería existir
        
        # Debería devolver una lista vacía, no dar error
        candidatos = self.cliente.buscar_candidatos(consulta)
        assert len(candidatos) == 0 