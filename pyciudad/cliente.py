"""
Cliente principal para interactuar con la API de CartoCiudad
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
import requests

from .constantes import (
    CANDIDATES_URL, 
    FIND_URL, 
    REVERSE_GEOCODE_URL, 
    DEFAULT_COUNTRY_CODE, 
    DEFAULT_LIMIT,
    DEFAULT_HEADERS,
    FILTROS_TIPO_ENTIDAD
)
from .excepciones import CartoCiudadError, APIError, PeticionInvalidaError
from .modelos import Candidato, Ubicacion, Direccion, TipoEntidad
from .utils import validar_coordenadas, construir_parametros_filtro, url_encode

# Configurar logging
logger = logging.getLogger("pycartociudad")


class CartoCiudad:
    """
    Cliente principal para interactuar con la API de CartoCiudad.
    
    Esta clase ofrece métodos para utilizar los diferentes servicios
    de CartoCiudad de forma sencilla y orientada a objetos.
    """
    
    def __init__(self, timeout: int = 10, verificar_ssl: bool = True, debug: bool = False):
        """
        Inicializa el cliente de CartoCiudad.
        
        Args:
            timeout: Tiempo máximo en segundos para esperar respuesta de la API
            verificar_ssl: Si se debe verificar el certificado SSL en las peticiones
            debug: Activa el modo de depuración con mensajes detallados
        """
        self.timeout = timeout
        self.verificar_ssl = verificar_ssl
        self.headers = DEFAULT_HEADERS.copy()
        
        # Configurar logging
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
            logger.setLevel(logging.INFO)
    
    def _realizar_peticion(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API de CartoCiudad.
        
        Args:
            url: URL del endpoint a consultar
            params: Parámetros de la petición
            
        Returns:
            Diccionario con la respuesta JSON
            
        Raises:
            APIError: Si hay un error en la petición
        """
        try:
            # Loguear la petición en modo debug
            if self.debug:
                logger.debug(f"Realizando petición a {url}")
                logger.debug(f"Parámetros: {params}")
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
                verify=self.verificar_ssl
            )
            
            # Loguear la URL completa en modo debug
            if self.debug:
                logger.debug(f"URL completa: {response.url}")
            
            # Verificar si la respuesta es exitosa
            response.raise_for_status()
            
            # Loguear la respuesta en modo debug
            if self.debug:
                logger.debug(f"Respuesta recibida: {response.status_code}")
                logger.debug(f"Contenido: {response.text[:500]}...")
            
            # Parsear la respuesta como JSON
            datos = response.json()
            
            return datos
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP: {e}")
            raise APIError(f"Error HTTP: {e}", codigo=response.status_code, respuesta=response.text)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión: {e}")
            raise APIError(f"Error de conexión con la API de CartoCiudad: {e}")
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout: {e}")
            raise APIError(f"Tiempo de espera agotado (timeout: {self.timeout}s): {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la petición: {e}")
            raise APIError(f"Error en la petición: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {e}")
            logger.error(f"Respuesta recibida: {response.text[:500]}...")
            raise APIError(f"Error al decodificar la respuesta JSON: {e}", respuesta=response.text)
    
    def buscar_candidatos(
        self, 
        consulta: str, 
        limite: int = DEFAULT_LIMIT,
        excluir_tipos: Optional[List[str]] = None,
        codigo_postal: Optional[Union[str, List[str]]] = None,
        municipio: Optional[Union[str, List[str]]] = None,
        provincia: Optional[Union[str, List[str]]] = None,
        comunidad_autonoma: Optional[Union[str, List[str]]] = None,
        poblacion: Optional[Union[str, List[str]]] = None,
        codigo_pais: str = DEFAULT_COUNTRY_CODE
    ) -> List[Candidato]:
        """
        Busca candidatos que coincidan con la consulta.
        
        Args:
            consulta: Texto de búsqueda
            limite: Número máximo de resultados a devolver
            excluir_tipos: Lista de tipos de entidades a excluir
            codigo_postal: Código(s) postal(es) para filtrar
            municipio: Municipio(s) para filtrar
            provincia: Provincia(s) para filtrar
            comunidad_autonoma: Comunidad(es) autónoma(s) para filtrar
            poblacion: Población(es) para filtrar
            codigo_pais: Código del país
            
        Returns:
            Lista de candidatos encontrados
            
        Raises:
            PeticionInvalidaError: Si algún parámetro es inválido
            APIError: Si hay un error en la petición
        """
        if not consulta:
            raise PeticionInvalidaError("La consulta no puede estar vacía", parametro="consulta")
        
        # Construir filtros geográficos
        filtros_geograficos = {}
        if codigo_postal:
            filtros_geograficos["cod_postal_filter"] = codigo_postal
        if municipio:
            filtros_geograficos["municipio_filter"] = municipio
        if provincia:
            filtros_geograficos["provincia_filter"] = provincia
        if comunidad_autonoma:
            filtros_geograficos["comunidad_autonoma_filter"] = comunidad_autonoma
        if poblacion:
            filtros_geograficos["poblacion_filter"] = poblacion
        
        # Construir parámetros
        params = construir_parametros_filtro(
            no_process=excluir_tipos,
            filtros_geograficos=filtros_geograficos,
            q=consulta,
            limit=limite,
            countrycodes=codigo_pais
        )
        
        # Realizar la petición
        respuesta = self._realizar_peticion(CANDIDATES_URL, params)
        
        # Procesar resultados
        candidatos = []
        if not respuesta:
            logger.warning("La API devolvió una respuesta vacía")
            return candidatos
        
        # Si la respuesta es un diccionario y tiene la clave 'error'
        if isinstance(respuesta, dict) and respuesta.get('error'):
            error_msg = respuesta.get('error', 'Error desconocido en la API')
            logger.error(f"Error en la API: {error_msg}")
            raise APIError(error_msg)
        
        # Verificar que la respuesta sea una lista
        if not isinstance(respuesta, list):
            logger.error(f"Respuesta inesperada: se esperaba una lista pero se recibió {type(respuesta)}")
            logger.error(f"Contenido: {respuesta}")
            raise APIError(f"Respuesta inesperada: se esperaba una lista pero se recibió {type(respuesta)}")
        
        # Procesar los candidatos
        for item in respuesta:
            try:
                candidato = Candidato.model_validate(item)
                candidatos.append(candidato)
            except Exception as e:
                # Loguear el error pero continuar con el siguiente candidato
                logger.warning(f"Error al parsear candidato: {e}")
                logger.debug(f"Datos del candidato: {item}")
                continue
        
        logger.info(f"Se encontraron {len(candidatos)} candidatos")
        return candidatos
    
    def geocodificar(
        self, 
        consulta: str,
        tipo: Optional[str] = None,
        id_entidad: Optional[str] = None,
        portal: Optional[str] = None,
        formato_salida: str = "json"
    ) -> Ubicacion:
        """
        Geocodifica una dirección o entidad y devuelve sus coordenadas.
        
        Args:
            consulta: Texto a geocodificar o None si se proporciona tipo e id_entidad
            tipo: Tipo de entidad (opcional)
            id_entidad: Identificador de la entidad (opcional)
            portal: Número de portal (opcional)
            formato_salida: Formato de salida ("json" o "geojson")
            
        Returns:
            Objeto Ubicacion con la información de la entidad geocodificada
            
        Raises:
            PeticionInvalidaError: Si algún parámetro es inválido
            APIError: Si hay un error en la petición
        """
        params = {}
        
        # Validar parámetros
        if consulta:
            params["q"] = consulta
        elif tipo and id_entidad:
            params["type"] = tipo
            params["id"] = id_entidad
        else:
            raise PeticionInvalidaError(
                "Debe proporcionar una consulta o un tipo y id de entidad",
                parametro="consulta/tipo/id_entidad"
            )
        
        # Añadir portal si se proporciona
        if portal:
            params["portal"] = portal
        
        # Añadir formato de salida
        if formato_salida and formato_salida.lower() in ["json", "geojson"]:
            if formato_salida.lower() == "geojson":
                params["outputformat"] = "geojson"
        
        # Realizar la petición
        respuesta = self._realizar_peticion(FIND_URL, params)
        
        # Si la respuesta es un diccionario y tiene la clave 'error'
        if isinstance(respuesta, dict) and respuesta.get('error'):
            error_msg = respuesta.get('error', 'Error desconocido en la API')
            logger.error(f"Error en la API: {error_msg}")
            raise APIError(error_msg)
        
        # Parsear la respuesta
        try:
            ubicacion = Ubicacion.model_validate(respuesta)
            return ubicacion
        except Exception as e:
            logger.error(f"Error al parsear la respuesta: {e}")
            logger.debug(f"Respuesta recibida: {respuesta}")
            raise APIError(f"Error al parsear la respuesta: {e}", respuesta=respuesta)
    
    def geocodificacion_inversa(
        self, 
        longitud: float, 
        latitud: float,
        tipo: Optional[str] = None
    ) -> Direccion:
        """
        Realiza una geocodificación inversa: coordenadas a dirección.
        
        Args:
            longitud: Coordenada de longitud en grados decimales
            latitud: Coordenada de latitud en grados decimales
            tipo: Tipo de entidad a buscar (opcional)
            
        Returns:
            Objeto Direccion con la información de la dirección encontrada
            
        Raises:
            PeticionInvalidaError: Si las coordenadas son inválidas
            APIError: Si hay un error en la petición
        """
        # Validar coordenadas
        validar_coordenadas(longitud, latitud)
        
        # Construir parámetros
        params = {
            "lon": longitud,
            "lat": latitud
        }
        
        if tipo:
            params["type"] = tipo
        
        # Realizar la petición
        respuesta = self._realizar_peticion(REVERSE_GEOCODE_URL, params)
        
        # Si la respuesta es un diccionario y tiene la clave 'error'
        if isinstance(respuesta, dict) and respuesta.get('error'):
            error_msg = respuesta.get('error', 'Error desconocido en la API')
            logger.error(f"Error en la API: {error_msg}")
            raise APIError(error_msg)
        
        # Parsear la respuesta
        try:
            direccion = Direccion.model_validate(respuesta)
            return direccion
        except Exception as e:
            logger.error(f"Error al parsear la respuesta: {e}")
            logger.debug(f"Respuesta recibida: {respuesta}")
            raise APIError(f"Error al parsear la respuesta: {e}", respuesta=respuesta) 