# -*- coding: utf-8 -*-
"""
Extractor de Información Básica del reporte DataCrédito
"""
import re
from typing import Dict, Any
from .base_extractor import BaseExtractor

class InformacionBasicaExtractor(BaseExtractor):
    """Extrae información básica personal del cliente"""
    
    def __init__(self):
        super().__init__("Información Básica")
        
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """
        Extrae información básica del PDF
        
        Args:
            texto: Contenido del PDF
            archivo: Nombre del archivo
            
        Returns:
            Dict con información básica extraída
        """
        registro = self.crear_registro_vacio([
            "Consultado por", "Fecha y Hora Consulta", "Tipo Documento",
            "Número Documento", "Estado Documento", "Lugar Expedición",
            "Fecha Expedición", "Nombre", "Rango Edad", "Género",
            "Antigüedad Ubicación"
        ])
        
        errores = []
        campos_extraidos = 0
        
        try:
            # Fecha y hora de consulta
            fecha_hora = self.extraer_fecha_consulta(texto)
            if fecha_hora:
                registro["Fecha y Hora Consulta"] = fecha_hora
                campos_extraidos += 1
            
            # Consultado por (solo personas naturales)
            consultado = self.extraer_consultado_por(texto)
            if consultado:
                registro["Consultado por"] = consultado
                campos_extraidos += 1
            
            # Tipo de documento
            tipo_doc = self.extraer_tipo_documento(texto)
            if tipo_doc:
                registro["Tipo Documento"] = tipo_doc
                campos_extraidos += 1
            
            # Número de documento
            num_doc = self.extraer_numero_documento(texto)
            if num_doc:
                registro["Número Documento"] = num_doc
                campos_extraidos += 1
            
            # Estado del documento
            estado = self.extraer_estado_documento(texto)
            if estado:
                registro["Estado Documento"] = estado
                campos_extraidos += 1
            
            # Lugar de expedición
            lugar = self.extraer_lugar_expedicion(texto)
            if lugar:
                registro["Lugar Expedición"] = lugar
                campos_extraidos += 1
            
            # Fecha de expedición
            fecha_exp = self.extraer_fecha_expedicion(texto)
            if fecha_exp:
                registro["Fecha Expedición"] = fecha_exp
                campos_extraidos += 1
            
            # Nombre
            nombre = self.extraer_nombre(texto)
            if nombre:
                registro["Nombre"] = nombre
                campos_extraidos += 1
            
            # Rango de edad
            rango = self.extraer_rango_edad(texto)
            if rango:
                registro["Rango Edad"] = rango
                campos_extraidos += 1
            
            # Género
            genero = self.extraer_genero(texto)
            if genero:
                registro["Género"] = genero
                campos_extraidos += 1
            
            # Antigüedad ubicación
            antiguedad = self.extraer_antiguedad_ubicacion(texto)
            if antiguedad:
                registro["Antigüedad Ubicación"] = antiguedad
                campos_extraidos += 1
                
        except Exception as e:
            errores.append(f"Error general en extracción: {str(e)}")
        
        self.log_extraccion(archivo, campos_extraidos, errores)
        return registro
    
    def extraer_fecha_consulta(self, texto: str) -> str:
        """Extrae fecha y hora de consulta"""
        patrones = [
            r"Fecha y Hora Consulta\s*:?\s*([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\.[0-9]{2} (AM|PM))",
            r"(20[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\.[0-9]{2} (AM|PM))"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_consultado_por(self, texto: str) -> str:
        """Extrae el nombre de la persona que realizó la consulta (no la empresa)"""
        lineas = texto.splitlines()
        
        # Buscar la línea con "Consultado por" y luego la siguiente línea con el nombre de la persona
        for i, linea in enumerate(lineas):
            if 'Consultado por' in linea and ':' in linea:
                # La persona consultante está en la siguiente línea
                # Patrón: "Nombre Apellido apellido - número"
                if i + 1 < len(lineas):
                    linea_siguiente = lineas[i + 1].strip()
                    
                    # Patrón para extraer nombre completo antes del guión y número
                    patron_persona = r'^([A-Za-záéíóúñÁÉÍÓÚÑ\s]+)\s*-\s*\d+'
                    match = re.search(patron_persona, linea_siguiente)
                    if match:
                        nombre_persona = match.group(1).strip()
                        if self.es_persona_natural(nombre_persona):
                            return nombre_persona
                    
                    # Patrón alternativo: solo tomar la parte antes del guión
                    if ' - ' in linea_siguiente:
                        partes = linea_siguiente.split(' - ', 1)
                        nombre_candidato = partes[0].strip()
                        if self.es_persona_natural(nombre_candidato):
                            return nombre_candidato
        
        return None
    
    def es_persona_natural(self, texto: str) -> bool:
        """Verifica si el texto corresponde a una persona natural"""
        if not texto or len(texto.strip()) < 3:
            return False
        
        texto_limpio = texto.strip().upper()
        
        # Excluir empresas, entidades y códigos
        exclusiones = [
            'SAS', 'LTDA', 'S.A.', 'S.A.S', 'DELAGRO', 'EMPRESA', 'COMPAÑIA', 'COMPANIA',
            'CIA', 'CORP', 'CORPORACION', 'FUNDACION', 'BANCO', 'COOPERATIVA',
            'INMOBILIARIA', 'CONSTRUCTORA', 'COMERCIALIZADORA', 'IMPORTADORA',
            'E.U.', 'EU', 'UNIPERSONAL', 'Y CIA', '& CIA'
        ]
        
        # Si contiene alguna exclusión de empresa, no es persona natural
        if any(exclusion in texto_limpio for exclusion in exclusiones):
            return False
        
        # Si es solo números, no es persona natural
        if re.match(r'^\d+$', texto_limpio):
            return False
        
        # Si es muy corto y no contiene espacios, probablemente no sea nombre completo
        if len(texto_limpio) < 6 and ' ' not in texto_limpio:
            return False
        
        # Verificar que tenga al menos una letra
        if not re.search(r'[A-ZÁÉÍÓÚÑ]', texto_limpio):
            return False
        
        # Verificar patrón típico de nombre: al menos dos palabras
        palabras = texto_limpio.split()
        if len(palabras) >= 2:
            # Verificar que las palabras sean nombres válidos (solo letras y acentos)
            for palabra in palabras:
                if not re.match(r'^[A-ZÁÉÍÓÚÑ]+$', palabra):
                    return False
            return True
        
        return False
    
    def extraer_tipo_documento(self, texto: str) -> str:
        """Extrae tipo de documento"""
        patrones = [
            r"Tipo Documento\s*[:\s]*([A-Z.]+)",
            r"(C\.C\.)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_numero_documento(self, texto: str) -> str:
        """Extrae número de documento"""
        patrones = [
            r"Número Documento\s*[:\s]*([0-9]+)",
            r"C\.C\.\s*([0-9]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_estado_documento(self, texto: str) -> str:
        """Extrae estado del documento"""
        patrones = [
            r"Estado Documento\s*[:\s]*([A-Za-zÁÉÍÓÚÑ]+)",
            r"(Vigente)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_lugar_expedicion(self, texto: str) -> str:
        """Extrae lugar de expedición"""
        patrones = [
            r"Lugar Expedición\s*[:\s]*([A-ZÁÉÍÓÚÑa-z\s]+?)(?=\s*Fecha Expedici|$)",
            r"(IBAGUE)",
            r"(BOGOTA)",
            r"(MEDELLIN)",
            r"(CALI)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_fecha_expedicion(self, texto: str) -> str:
        """Extrae fecha de expedición"""
        patron = r"Fecha Expedición\s*[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})"
        return self.buscar_patron(patron, texto)
    
    def extraer_nombre(self, texto: str) -> str:
        """Extrae nombre para persona natural"""
        patrones = [
            r"Nombre\s*[:\s]*([A-ZÁÉÍÓÚÑ\s]+)(?=\s*Rango Edad|$)",
            r"([A-ZÁÉÍÓÚÑ]+\s+[A-ZÁÉÍÓÚÑ]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_rango_edad(self, texto: str) -> str:
        """Extrae rango de edad"""
        patrones = [
            r"Rango Edad\s*[:\s]*([0-9\-]+)",
            r"(\d{2}-\d{2})"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_genero(self, texto: str) -> str:
        """Extrae género"""
        patrones = [
            r"Género\s*[:\s]*([A-Za-zÁÉÍÓÚÑ]+)",
            r"(Femenino)",
            r"(Masculino)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_antiguedad_ubicacion(self, texto: str) -> str:
        """Extrae antigüedad de ubicación"""
        patrones = [
            r"Antiguedad Ubicación\s*[:\s]*([0-9]+\s*Meses\s*[A-Za-z\s]+?)(?=\s*ARTICULO|\s*-|$)",
            r"(\d+\s*Meses\s*[A-Za-z\s]+?)(?=\s*ARTICULO|\s*-|$)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)