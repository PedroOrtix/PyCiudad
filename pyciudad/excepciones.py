"""
Módulo de excepciones para PyCartoCiudad
"""

class CartoCiudadError(Exception):
    """Excepción base para errores de PyCartoCiudad."""
    pass


class APIError(CartoCiudadError):
    """Excepción para errores de la API de CartoCiudad."""
    
    def __init__(self, mensaje="Error en la API de CartoCiudad", codigo=None, respuesta=None):
        self.codigo = codigo
        self.respuesta = respuesta
        super().__init__(f"{mensaje} (Código: {codigo})")


class PeticionInvalidaError(CartoCiudadError):
    """Excepción para peticiones inválidas a la API."""
    
    def __init__(self, mensaje="Petición inválida", parametro=None):
        self.parametro = parametro
        mensaje_completo = mensaje
        if parametro:
            mensaje_completo += f" - Parámetro inválido: {parametro}"
        super().__init__(mensaje_completo) 