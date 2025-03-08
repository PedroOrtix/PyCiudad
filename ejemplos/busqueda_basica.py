#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo básico de uso de PyCiudad
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pyciudad")
logger.setLevel(logging.DEBUG)

# Añadir el directorio padre al sys.path para poder importar pyciudad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyciudad import CartoCiudad, CartoCiudadError


def main():
    # Crear cliente con modo debug activado
    cliente = CartoCiudad(debug=True)
    
    try:
        # Ejemplo 1: Buscar candidatos
        print("Ejemplo 1: Búsqueda de candidatos")
        print("-" * 50)
        consulta = "Calle Iglesia 5, Madrid"
        print(f"Búsqueda: '{consulta}'")
        
        candidatos = cliente.buscar_candidatos(consulta, limite=3)
        
        print(f"Se encontraron {len(candidatos)} candidatos:\n")
        for i, candidato in enumerate(candidatos, 1):
            print(f"{i}. {candidato.direccion}")
            print(f"   Municipio: {candidato.municipio}")
            print(f"   Provincia: {candidato.provincia}")
            if candidato.latitud and candidato.longitud:
                print(f"   Coordenadas: {candidato.latitud}, {candidato.longitud}")
            print()
        
        # Ejemplo 2: Geocodificar dirección
        print("\nEjemplo 2: Geocodificación de dirección")
        print("-" * 50)
        consulta = "Estación de metro Clínico, Málaga"
        print(f"Geocodificando: '{consulta}'")
        
        ubicacion = cliente.geocodificar(consulta)
        
        print(f"Dirección: {ubicacion.direccion}")
        print(f"Municipio: {ubicacion.muni}")
        print(f"Provincia: {ubicacion.province}")
        print(f"Coordenadas: {ubicacion.latitud}, {ubicacion.longitud}")
        print(f"Geometría: {ubicacion.geometria}")
        
        # Extraer coordenadas de la geometría WKT
        coordenadas_wkt = ubicacion.extraer_coordenadas_wkt()
        if coordenadas_wkt:
            lon, lat = coordenadas_wkt
            print(f"Coordenadas extraídas de WKT: {lat}, {lon}")
        
        # Ejemplo 3: Geocodificación inversa
        print("\nEjemplo 3: Geocodificación inversa")
        print("-" * 50)
        lon, lat = -0.344579, 39.472413
        print(f"Coordenadas: {lat}, {lon}")
        
        direccion = cliente.geocodificacion_inversa(lon, lat)
        
        print(f"Dirección: {direccion.via}")
        if direccion.numero:
            print(f"Número: {direccion.numero}")
        print(f"Municipio: {direccion.municipio}")
        print(f"Provincia: {direccion.provincia}")
        print(f"Código Postal: {direccion.codigo_postal}")
        
        # Extraer coordenadas de la geometría WKT
        if direccion.geom:
            print(f"Geometría: {direccion.geom}")
            coordenadas_wkt = direccion.extraer_coordenadas_wkt()
            if coordenadas_wkt:
                lon, lat = coordenadas_wkt
                print(f"Coordenadas extraídas de WKT: {lat}, {lon}")
        
    except CartoCiudadError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 