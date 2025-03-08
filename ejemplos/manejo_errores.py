#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo de manejo de errores en PyCiudad
"""

import sys
import os
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyciudad")
logger.setLevel(logging.INFO)

# Añadir el directorio padre al sys.path para poder importar pyciudad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyciudad import CartoCiudad, CartoCiudadError, APIError, PeticionInvalidaError


def main():
    print("Ejemplo de manejo de errores en PyCiudad")
    print("=" * 50)
    
    # Crear cliente con timeout bajo para provocar errores
    cliente_timeout = CartoCiudad(timeout=0.001)
    
    # Crear cliente normal
    cliente = CartoCiudad()
    
    # Ejemplo 1: Manejo de error por consulta vacía
    print("\nEjemplo 1: Error por consulta vacía")
    print("-" * 50)
    try:
        candidatos = cliente.buscar_candidatos("")
        print("Resultados:", candidatos)
    except PeticionInvalidaError as e:
        print(f"Error capturado (PeticionInvalidaError): {e}")
    except CartoCiudadError as e:
        print(f"Error capturado (CartoCiudadError): {e}")
    
    # Ejemplo 2: Manejo de error por timeout
    print("\nEjemplo 2: Error por timeout")
    print("-" * 50)
    try:
        # Usamos el cliente con timeout muy bajo
        candidatos = cliente_timeout.buscar_candidatos("Calle Mayor, Madrid")
        print("Resultados:", candidatos)
    except APIError as e:
        print(f"Error capturado (APIError): {e}")
    except CartoCiudadError as e:
        print(f"Error capturado (CartoCiudadError): {e}")
    
    # Ejemplo 3: Manejo de error por coordenadas inválidas
    print("\nEjemplo 3: Error por coordenadas inválidas")
    print("-" * 50)
    try:
        # Coordenadas fuera del rango de España
        direccion = cliente.geocodificacion_inversa(100.0, 80.0)
        print("Dirección:", direccion)
    except PeticionInvalidaError as e:
        print(f"Error capturado (PeticionInvalidaError): {e}")
    except CartoCiudadError as e:
        print(f"Error capturado (CartoCiudadError): {e}")
    
    # Ejemplo 4: Manejo de error por parámetros faltantes
    print("\nEjemplo 4: Error por parámetros faltantes")
    print("-" * 50)
    try:
        # Intentar geocodificar sin proporcionar consulta ni id/tipo
        ubicacion = cliente.geocodificar(consulta=None, tipo=None, id_entidad=None)
        print("Ubicación:", ubicacion)
    except PeticionInvalidaError as e:
        print(f"Error capturado (PeticionInvalidaError): {e}")
    except CartoCiudadError as e:
        print(f"Error capturado (CartoCiudadError): {e}")
    
    # Ejemplo 5: Manejo de errores con bloque try-except general
    print("\nEjemplo 5: Manejo de errores con bloque try-except general")
    print("-" * 50)
    
    # Lista de operaciones que pueden fallar
    operaciones = [
        {"desc": "Consulta vacía", "func": lambda: cliente.buscar_candidatos("")},
        {"desc": "Timeout", "func": lambda: cliente_timeout.buscar_candidatos("Calle Mayor")},
        {"desc": "Coordenadas inválidas", "func": lambda: cliente.geocodificacion_inversa(200.0, 100.0)},
        {"desc": "Parámetros faltantes", "func": lambda: cliente.geocodificar(None)},
        {"desc": "Operación válida", "func": lambda: cliente.buscar_candidatos("Calle Mayor, Madrid", limite=1)}
    ]
    
    for op in operaciones:
        print(f"\nIntentando: {op['desc']}")
        try:
            resultado = op["func"]()
            print(f"Operación exitosa: {resultado}")
        except CartoCiudadError as e:
            print(f"Error: {e}")
            print(f"Tipo de error: {type(e).__name__}")


if __name__ == "__main__":
    main() 