# -*- coding: utf-8 -*-
"""
Clase base para todos los extractores de secciones
"""
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from config.field_mappings import REGEX_PATTERNS, DEFAULT_VALUES

class BaseExtractor(ABC):
    """Clase base abstracta para extractores de secciones"""
    
    def __init__(self, nombre_seccion: str):
        self.nombre_seccion = nombre_seccion
        self.regex_patterns = REGEX_PATTERNS
        self.default_values = DEFAULT_VALUES
    
    @abstractmethod
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """
        Método abstracto para extraer datos de una sección
        
        Args:
            texto: Contenido del PDF
            archivo: Nombre del archivo
            
        Returns:
            Dict con datos extraídos
        """
        pass
    
    def buscar_patron(self, patron: str, texto: str) -> Optional[str]:
        """
        Busca un patrón regex en el texto
        
        Args:
            patron: Patrón regex a buscar
            texto: Texto donde buscar
            
        Returns:
            Primer resultado encontrado o None
        """
        try:
            match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
            if match:
                resultado = match.group(1) if match.groups() else match.group(0)
                return self.limpiar_texto(resultado)
            return None
        except Exception:
            return None
    
    def buscar_multiples_patrones(self, patrones: List[str], texto: str) -> Optional[str]:
        """
        Busca múltiples patrones hasta encontrar uno
        
        Args:
            patrones: Lista de patrones a probar
            texto: Texto donde buscar
            
        Returns:
            Primer resultado encontrado o None
        """
        for patron in patrones:
            resultado = self.buscar_patron(patron, texto)
            if resultado:
                return resultado
        return None
    
    def extraer_numeros_linea(self, texto: str, palabra_clave: str) -> Optional[str]:
        """
        Extrae números de la línea que contiene una palabra clave
        
        Args:
            texto: Texto completo
            palabra_clave: Palabra a buscar
            
        Returns:
            Números encontrados o None
        """
        lineas = texto.split('\n')
        for linea in lineas:
            if palabra_clave.lower() in linea.lower():
                numeros = re.findall(r'[\d,\.]+', linea)
                if numeros:
                    return numeros[0].replace(',', '')
        return None
    
    def limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza texto extraído
        
        Args:
            texto: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not texto:
            return ""
        
        # Remover espacios extra y caracteres de control
        texto = re.sub(r'\s+', ' ', str(texto)).strip()
        
        # Remover caracteres especiales problemáticos
        texto = texto.replace('\r', '').replace('\n', ' ')
        
        return texto
    
    def validar_campo_numerico(self, valor: str) -> Optional[str]:
        """
        Valida y limpia campos numéricos
        
        Args:
            valor: Valor a validar
            
        Returns:
            Valor limpio o None si no es válido
        """
        if not valor:
            return None
        
        # Extraer solo números, comas y puntos
        numerico = re.sub(r'[^\d,\.]', '', valor)
        
        if numerico and any(c.isdigit() for c in numerico):
            return numerico
        
        return None
    
    def crear_registro_vacio(self, campos: List[str]) -> Dict[str, str]:
        """
        Crea un registro con campos vacíos
        
        Args:
            campos: Lista de nombres de campos
            
        Returns:
            Dict con campos inicializados vacíos
        """
        return {campo: "" for campo in campos}
    
    def log_extraccion(self, archivo: str, campos_extraidos: int, errores: List[str]):
        """
        Log de resultados de extracción
        
        Args:
            archivo: Nombre del archivo procesado
            campos_extraidos: Cantidad de campos extraídos
            errores: Lista de errores encontrados
        """
        print(f"  └─ {self.nombre_seccion}: {campos_extraidos} campos extraídos")
        
        if errores:
            print(f"     Errores: {len(errores)}")
            for error in errores[:3]:  # Solo primeros 3 errores
                print(f"       - {error}")