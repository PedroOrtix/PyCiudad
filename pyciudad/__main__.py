#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Punto de entrada para ejecutar PyCartoCiudad como módulo
"""

import sys
import argparse
from pycartociudad import CartoCiudad, CartoCiudadError


def geocodificar(args):
    """Geocodificar una dirección."""
    cliente = CartoCiudad()
    try:
        ubicacion = cliente.geocodificar(args.direccion)
        print(f"Dirección: {ubicacion.direccion}")
        print(f"Municipio: {ubicacion.muni}")
        print(f"Provincia: {ubicacion.province}")
        print(f"Coordenadas: {ubicacion.latitud}, {ubicacion.longitud}")
    except CartoCiudadError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def geocodificacion_inversa(args):
    """Geocodificación inversa."""
    cliente = CartoCiudad()
    try:
        direccion = cliente.geocodificacion_inversa(args.longitud, args.latitud)
        print(f"Dirección: {direccion.via}")
        if direccion.numero:
            print(f"Número: {direccion.numero}")
        print(f"Municipio: {direccion.municipio}")
        print(f"Provincia: {direccion.provincia}")
        print(f"Código Postal: {direccion.codigo_postal}")
    except CartoCiudadError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def buscar_candidatos(args):
    """Buscar candidatos para una dirección."""
    cliente = CartoCiudad()
    try:
        candidatos = cliente.buscar_candidatos(args.consulta, limite=args.limite)
        print(f"Se encontraron {len(candidatos)} candidatos:")
        for i, candidato in enumerate(candidatos, 1):
            print(f"{i}. {candidato.direccion}")
            print(f"   Municipio: {candidato.municipio}")
            print(f"   Provincia: {candidato.provincia}")
            if candidato.latitud and candidato.longitud:
                print(f"   Coordenadas: {candidato.latitud}, {candidato.longitud}")
            print()
    except CartoCiudadError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Cliente de línea de comandos para la API de CartoCiudad"
    )
    subparsers = parser.add_subparsers(dest="comando", help="Comando a ejecutar")
    
    # Subcomando para geocodificar
    parser_geo = subparsers.add_parser("geocodificar", help="Geocodificar una dirección")
    parser_geo.add_argument("direccion", help="Dirección a geocodificar")
    parser_geo.set_defaults(func=geocodificar)
    
    # Subcomando para geocodificación inversa
    parser_inv = subparsers.add_parser("inversa", help="Geocodificación inversa")
    parser_inv.add_argument("longitud", type=float, help="Longitud en grados decimales")
    parser_inv.add_argument("latitud", type=float, help="Latitud en grados decimales")
    parser_inv.set_defaults(func=geocodificacion_inversa)
    
    # Subcomando para buscar candidatos
    parser_cand = subparsers.add_parser("candidatos", help="Buscar candidatos")
    parser_cand.add_argument("consulta", help="Texto de búsqueda")
    parser_cand.add_argument("--limite", "-l", type=int, default=5, help="Límite de resultados")
    parser_cand.set_defaults(func=buscar_candidatos)
    
    args = parser.parse_args()
    
    if args.comando is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main() 