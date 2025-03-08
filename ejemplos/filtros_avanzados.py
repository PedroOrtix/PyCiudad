#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo de uso de filtros avanzados en PyCiudad
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyciudad")
logger.setLevel(logging.INFO)

# Añadir el directorio padre al sys.path para poder importar pyciudad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyciudad import CartoCiudad, CartoCiudadError


def mostrar_resultados(candidatos, titulo):
    """Función auxiliar para mostrar resultados de manera formateada."""
    print(f"\n{titulo}")
    print("-" * 50)
    print(f"Se encontraron {len(candidatos)} candidatos:\n")
    for i, candidato in enumerate(candidatos, 1):
        print(f"{i}. {candidato.direccion}")
        print(f"   Tipo: {candidato.type}")
        print(f"   Municipio: {candidato.municipio}")
        print(f"   Provincia: {candidato.provincia}")
        if candidato.codigo_postal:
            print(f"   Código Postal: {candidato.codigo_postal}")
        if candidato.latitud and candidato.longitud:
            print(f"   Coordenadas: {candidato.latitud}, {candidato.longitud}")
        print()


def main():
    # Crear cliente
    cliente = CartoCiudad()
    
    try:
        # Ejemplo 1: Filtrado por código postal
        print("Ejemplo 1: Filtrado por código postal")
        print("-" * 50)
        consulta = "Calle Mayor"
        codigos_postales = ["28013", "28001"]
        print(f"Búsqueda: '{consulta}' en códigos postales {', '.join(codigos_postales)}")
        
        candidatos = cliente.buscar_candidatos(
            consulta,
            limite=5,
            codigo_postal=codigos_postales
        )
        
        mostrar_resultados(candidatos, "Resultados filtrados por código postal")
        
        # Ejemplo 2: Filtrado por municipio
        print("\nEjemplo 2: Filtrado por municipio")
        print("-" * 50)
        consulta = "Gran Vía"
        municipios = ["Madrid", "Salamanca"]
        print(f"Búsqueda: '{consulta}' en municipios {', '.join(municipios)}")
        
        candidatos = cliente.buscar_candidatos(
            consulta,
            limite=5,
            municipio=municipios
        )
        
        mostrar_resultados(candidatos, "Resultados filtrados por municipio")
        
        # Ejemplo 3: Exclusión de tipos de entidades
        print("\nEjemplo 3: Exclusión de tipos de entidades")
        print("-" * 50)
        consulta = "Retiro"
        tipos_excluidos = ["callejero", "portal"]
        print(f"Búsqueda: '{consulta}' excluyendo tipos: {', '.join(tipos_excluidos)}")
        
        candidatos = cliente.buscar_candidatos(
            consulta,
            limite=8,
            excluir_tipos=tipos_excluidos
        )
        
        mostrar_resultados(candidatos, "Resultados excluyendo tipos")
        
        # Ejemplo 4: Combinación de filtros
        print("\nEjemplo 4: Combinación de filtros")
        print("-" * 50)
        consulta = "Atocha"
        provincia = "Madrid"
        tipos_excluidos = ["portal", "poblacion"]
        print(f"Búsqueda: '{consulta}' en provincia {provincia}, excluyendo: {', '.join(tipos_excluidos)}")
        
        candidatos = cliente.buscar_candidatos(
            consulta,
            limite=5,
            provincia=provincia,
            excluir_tipos=tipos_excluidos
        )
        
        mostrar_resultados(candidatos, "Resultados con filtros combinados")
        
    except CartoCiudadError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 