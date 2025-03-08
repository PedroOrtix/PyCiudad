#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo de manejo de geometrías WKT en PyCiudad
"""

import sys
import os
import logging
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyciudad")
logger.setLevel(logging.INFO)

# Añadir el directorio padre al sys.path para poder importar pyciudad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyciudad import CartoCiudad, CartoCiudadError


def extraer_coordenadas_manual(geom_wkt):
    """
    Extrae coordenadas de una geometría WKT manualmente.
    Ejemplo de cómo se podría implementar la extracción sin usar los métodos de la librería.
    """
    if not geom_wkt or not isinstance(geom_wkt, str):
        return None
    
    # Extraer coordenadas de un POINT
    point_match = re.search(r'POINT\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)', geom_wkt)
    if point_match:
        try:
            lon = float(point_match.group(1))
            lat = float(point_match.group(2))
            return (lon, lat)
        except (ValueError, IndexError):
            return None
    
    # Extraer coordenadas de un LINESTRING (primer punto)
    linestring_match = re.search(r'LINESTRING\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', geom_wkt)
    if linestring_match:
        try:
            lon = float(linestring_match.group(1))
            lat = float(linestring_match.group(2))
            return (lon, lat)
        except (ValueError, IndexError):
            return None
    
    # Extraer coordenadas de un POLYGON (primer punto)
    polygon_match = re.search(r'POLYGON\s*\(\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', geom_wkt)
    if polygon_match:
        try:
            lon = float(polygon_match.group(1))
            lat = float(polygon_match.group(2))
            return (lon, lat)
        except (ValueError, IndexError):
            return None
    
    return None


def main():
    print("Ejemplo de manejo de geometrías WKT en PyCiudad")
    print("=" * 50)
    
    # Crear cliente
    cliente = CartoCiudad()
    
    try:
        # Ejemplo 1: Obtener y procesar geometría WKT de un punto
        print("\nEjemplo 1: Geometría WKT de un punto")
        print("-" * 50)
        
        # Geocodificar una dirección que devuelve un punto
        ubicacion = cliente.geocodificar("Estación de metro Clínico, Málaga")
        
        print(f"Dirección: {ubicacion.direccion}")
        print(f"Tipo: {ubicacion.type}")
        print(f"Geometría WKT: {ubicacion.geom}")
        
        # Extraer coordenadas usando el método de la librería
        coords = ubicacion.extraer_coordenadas_wkt()
        if coords:
            lon, lat = coords
            print(f"Coordenadas extraídas (método de la librería): {lat}, {lon}")
        
        # Extraer coordenadas manualmente
        coords_manual = extraer_coordenadas_manual(ubicacion.geom)
        if coords_manual:
            lon, lat = coords_manual
            print(f"Coordenadas extraídas (método manual): {lat}, {lon}")
        
        # Ejemplo 2: Obtener y procesar geometría WKT de una calle
        print("\nEjemplo 2: Geometría WKT de una calle")
        print("-" * 50)
        
        # Geocodificar una calle (que debería devolver un linestring)
        ubicacion = cliente.geocodificar("Calle Mayor, Madrid", tipo="callejero")
        
        print(f"Dirección: {ubicacion.direccion}")
        print(f"Tipo: {ubicacion.type}")
        print(f"Geometría WKT: {ubicacion.geom}")
        
        # Extraer coordenadas usando el método de la librería
        coords = ubicacion.extraer_coordenadas_wkt()
        if coords:
            lon, lat = coords
            print(f"Coordenadas extraídas (método de la librería): {lat}, {lon}")
        else:
            print("No se pudieron extraer coordenadas con el método de la librería")
        
        # Extraer coordenadas manualmente
        coords_manual = extraer_coordenadas_manual(ubicacion.geom)
        if coords_manual:
            lon, lat = coords_manual
            print(f"Coordenadas extraídas (método manual): {lat}, {lon}")
        else:
            print("No se pudieron extraer coordenadas manualmente")
        
        # Ejemplo 3: Geocodificación inversa y geometría
        print("\nEjemplo 3: Geocodificación inversa y geometría")
        print("-" * 50)
        
        # Coordenadas del centro de Madrid
        lon, lat = -3.7037902, 40.4167754
        print(f"Coordenadas de entrada: {lat}, {lon}")
        
        direccion = cliente.geocodificacion_inversa(lon, lat)
        
        print(f"Dirección: {direccion.via}")
        if direccion.numero:
            print(f"Número: {direccion.numero}")
        print(f"Municipio: {direccion.municipio}")
        print(f"Geometría WKT: {direccion.geom}")
        
        # Extraer coordenadas de la geometría
        coords = direccion.extraer_coordenadas_wkt()
        if coords:
            lon_wkt, lat_wkt = coords
            print(f"Coordenadas extraídas de WKT: {lat_wkt}, {lon_wkt}")
            
            # Calcular la diferencia con las coordenadas originales
            dist_lon = abs(lon - lon_wkt)
            dist_lat = abs(lat - lat_wkt)
            print(f"Diferencia con coordenadas originales: {dist_lat:.8f}, {dist_lon:.8f}")
        
    except CartoCiudadError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 