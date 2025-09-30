# -*- coding: utf-8 -*-
"""
EXTRACTOR MEJORADO - Patrones más amplios y flexibles
Diseñado para capturar información incluso con variaciones de formato
"""
import re
from typing import Dict, Any

class ExtractorMejorado:
    """Extractor con patrones más flexibles y robustos"""
    
    def __init__(self):
        self.nombre = "Extractor Mejorado"
        
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """Extrae información con patrones mejorados"""
        
        # Normalizar texto
        texto_limpio = self.normalizar_texto(texto)
        
        registro = {}
        
        # === EXTRACCIÓN CON MÚLTIPLES ESTRATEGIAS ===
        
        # 1. Información de consulta
        registro.update(self.extraer_info_consulta(texto_limpio))
        
        # 2. Información personal
        registro.update(self.extraer_info_personal(texto_limpio))
        
        # 3. Información demográfica
        registro.update(self.extraer_info_demografica(texto_limpio))
        
        # 4. Información crediticia
        registro.update(self.extraer_info_crediticia(texto_limpio))
        
        # 5. Información adicional por líneas
        registro.update(self.extraer_por_lineas(texto_limpio))
        
        # 6. Extracción por palabras clave
        registro.update(self.extraer_por_palabras_clave(texto_limpio))
        
        # Contar campos extraídos
        campos_extraidos = len([v for v in registro.values() if v and str(v).strip()])
        
        # Metadatos
        registro['_metadata'] = {
            'archivo': archivo,
            'total_campos_extraidos': campos_extraidos,
            'texto_completo_length': len(texto),
            'procesado': campos_extraidos > 0
        }
        
        return registro
    
    def normalizar_texto(self, texto: str) -> str:
        """Normaliza el texto para mejor extracción"""
        # Reemplazar caracteres problemáticos
        texto = texto.replace('\\n', ' ').replace('\\r', ' ')
        texto = re.sub(r'\\s+', ' ', texto)  # Múltiples espacios a uno
        texto = texto.replace(':', ': ')  # Normalizar separadores
        return texto
    
    def extraer_info_consulta(self, texto: str) -> Dict[str, str]:
        """Extrae información de la consulta"""
        info = {}
        
        # Consultado por - MÚLTIPLES PATRONES
        patrones_consultado = [
            r"Consultado por[:\\s]*([A-ZÁÉÍÓÚÑ][^\\n]*?)(?:SAS|LTDA|S\\.A|DELAGRO|\\n)",
            r"Consultado por[:\\s]*([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\\s]{10,50})",
            r"([A-ZÁÉÍÓÚÑ]+\\s+[A-ZÁÉÍÓÚÑ]+\\s+[a-záéíóúñ]+)(?=\\s*DELAGRO)",
            r"Consultado[^:]*:[\\s]*([^\\n]{10,})"
        ]
        info['consultado_por'] = self.buscar_multiples_patrones(patrones_consultado, texto)
        
        # Fecha y hora - MÚLTIPLES FORMATOS
        patrones_fecha = [
            r"Fecha[^:]*:[\\s]*([0-9]{1,2}[/\\-][0-9]{1,2}[/\\-][0-9]{4})",
            r"([0-9]{1,2}[/\\-][0-9]{1,2}[/\\-][0-9]{4})[\\s]+([0-9]{1,2}:[0-9]{2})",
            r"\\b([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\\b"
        ]
        fecha = self.buscar_multiples_patrones(patrones_fecha, texto)
        if fecha:
            info['fecha_consulta'] = fecha
        
        # Hora
        patrones_hora = [
            r"([0-9]{1,2}:[0-9]{2}:[0-9]{2})",
            r"([0-9]{1,2}:[0-9]{2})\\s*(?:AM|PM|am|pm)?",
            r"Hora[^:]*:[\\s]*([0-9]{1,2}:[0-9]{2})"
        ]
        info['hora_consulta'] = self.buscar_multiples_patrones(patrones_hora, texto)
        
        return info
    
    def extraer_info_personal(self, texto: str) -> Dict[str, str]:
        """Extrae información personal"""
        info = {}
        
        # Tipo de documento
        patrones_tipo_doc = [
            r"Tipo[^:]*Documento[^:]*:[\\s]*([^\\n]{3,30})",
            r"(Cédula[^\\n]*)",
            r"(C\\.C\\.)",
            r"(Tarjeta[^\\n]*Identidad)"
        ]
        info['tipo_documento'] = self.buscar_multiples_patrones(patrones_tipo_doc, texto)
        
        # Número de documento
        patrones_numero = [
            r"Número[^:]*:[\\s]*([0-9\\.\\,]+)",
            r"C\\.C\\.?[\\s]*:?[\\s]*([0-9\\.\\,]+)",
            r"Documento[^:]*:[\\s]*([0-9\\.\\,]+)",
            r"\\b([0-9]{6,12})\\b"  # Números largos que podrían ser documentos
        ]
        info['numero_documento'] = self.buscar_multiples_patrones(patrones_numero, texto)
        
        # Nombre completo
        patrones_nombre = [
            r"Nombre[^:]*:[\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{5,50})",
            r"Nombres[^:]*:[\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{5,50})",
            r"Apellidos[^:]*:[\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{5,50})"
        ]
        info['nombre_completo'] = self.buscar_multiples_patrones(patrones_nombre, texto)
        
        # Estado documento
        patrones_estado = [
            r"Estado[^:]*:[\\s]*([A-Za-záéíóúñ]+)",
            r"(Vigente|Vencido|Activo|Inactivo)"
        ]
        info['estado_documento'] = self.buscar_multiples_patrones(patrones_estado, texto)
        
        # Género
        patrones_genero = [
            r"Género[^:]*:[\\s]*([A-Za-záéíóúñ]+)",
            r"Sexo[^:]*:[\\s]*([A-Za-záéíóúñ]+)",
            r"\\b(Masculino|Femenino|Hombre|Mujer)\\b"
        ]
        info['genero'] = self.buscar_multiples_patrones(patrones_genero, texto)
        
        # Edad
        patrones_edad = [
            r"Edad[^:]*:[\\s]*([0-9\\-]+)",
            r"Rango[^:]*:[\\s]*([0-9\\-]+)",
            r"\\b([0-9]{2}-[0-9]{2})\\b años?"
        ]
        info['rango_edad'] = self.buscar_multiples_patrones(patrones_edad, texto)
        
        return info
    
    def extraer_info_demografica(self, texto: str) -> Dict[str, str]:
        """Extrae información demográfica"""
        info = {}
        
        # Dirección
        patrones_direccion = [
            r"Dirección[^:]*:[\\s]*([^\\n]{10,80})",
            r"Residencia[^:]*:[\\s]*([^\\n]{10,80})",
            r"Domicilio[^:]*:[\\s]*([^\\n]{10,80})"
        ]
        info['direccion_residencia'] = self.buscar_multiples_patrones(patrones_direccion, texto)
        
        # Ciudad
        patrones_ciudad = [
            r"Ciudad[^:]*:[\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{3,30})",
            r"Municipio[^:]*:[\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{3,30})",
            r"\\b(BOGOTA|MEDELLIN|CALI|BARRANQUILLA|CARTAGENA|IBAGUE)\\b"
        ]
        info['ciudad_residencia'] = self.buscar_multiples_patrones(patrones_ciudad, texto)
        
        # Teléfono
        patrones_telefono = [
            r"Teléfono[^:]*:[\\s]*([0-9\\s\\-\\(\\)]+)",
            r"Tel[^:]*:[\\s]*([0-9\\s\\-\\(\\)]+)",
            r"Celular[^:]*:[\\s]*([0-9\\s\\-\\(\\)]+)",
            r"\\b([0-9]{7,10})\\b"  # Números que podrían ser teléfonos
        ]
        info['telefono'] = self.buscar_multiples_patrones(patrones_telefono, texto)
        
        # Email
        patrones_email = [
            r"Email[^:]*:[\\s]*([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})",
            r"Correo[^:]*:[\\s]*([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})",
            r"\\b([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})\\b"
        ]
        info['email'] = self.buscar_multiples_patrones(patrones_email, texto)
        
        return info
    
    def extraer_info_crediticia(self, texto: str) -> Dict[str, str]:
        """Extrae información crediticia"""
        info = {}
        
        # Score
        patrones_score = [
            r"Score[^:]*:[\\s]*([0-9]+)",
            r"Puntaje[^:]*:[\\s]*([0-9]+)",
            r"Calificación[^:]*:[\\s]*([A-Z0-9]+)"
        ]
        info['score'] = self.buscar_multiples_patrones(patrones_score, texto)
        
        # Saldos
        patrones_saldo = [
            r"Saldo[^:]*:[\\s]*([0-9\\.,\\$]+)",
            r"Valor[^:]*:[\\s]*([0-9\\.,\\$]+)",
            r"Deuda[^:]*:[\\s]*([0-9\\.,\\$]+)"
        ]
        info['saldo'] = self.buscar_multiples_patrones(patrones_saldo, texto)
        
        # Obligaciones
        patrones_obligaciones = [
            r"Obligacion[^:]*:[\\s]*([^\\n]{5,50})",
            r"Crédito[^:]*:[\\s]*([^\\n]{5,50})",
            r"Tarjeta[^:]*:[\\s]*([^\\n]{5,50})"
        ]
        info['obligaciones'] = self.buscar_multiples_patrones(patrones_obligaciones, texto)
        
        return info
    
    def extraer_por_lineas(self, texto: str) -> Dict[str, str]:
        """Extrae información analizando línea por línea"""
        info = {}
        
        # Buscar líneas con formato "Campo: Valor"
        lineas = texto.split('\\n')
        for linea in lineas:
            linea = linea.strip()
            if ':' in linea and len(linea) > 5:
                try:
                    campo, valor = linea.split(':', 1)
                    campo = campo.strip().lower().replace(' ', '_')
                    valor = valor.strip()
                    
                    if len(valor) > 0 and len(valor) < 100:
                        # Solo agregar si el campo no existe ya
                        if campo not in info:
                            info[f"linea_{campo}"] = valor
                except:
                    continue
        
        return info
    
    def extraer_por_palabras_clave(self, texto: str) -> Dict[str, str]:
        """Extrae información buscando palabras clave"""
        info = {}
        
        palabras_clave = {
            'empresa': r"\\b([A-ZÁÉÍÓÚÑ][A-Za-z\\s]{5,40}(?:S\\.A\\.S|LTDA|S\\.A|SAS))\\b",
            'fecha_nacimiento': r"\\b([0-9]{1,2}[/\\-][0-9]{1,2}[/\\-][0-9]{4})\\b",
            'cedula': r"\\b([0-9]{6,12})\\b",
            'valor_monetario': r"\\$[\\s]*([0-9\\.,]+)",
            'porcentaje': r"([0-9]+[\\.,]?[0-9]*)%"
        }
        
        for clave, patron in palabras_clave.items():
            matches = re.findall(patron, texto, re.IGNORECASE)
            if matches:
                info[f"detectado_{clave}"] = matches[0] if isinstance(matches[0], str) else str(matches[0])
        
        return info
    
    def buscar_multiples_patrones(self, patrones: list, texto: str) -> str:
        """Busca con múltiples patrones y retorna el primer match"""
        for patron in patrones:
            try:
                matches = re.findall(patron, texto, re.IGNORECASE | re.MULTILINE)
                if matches:
                    resultado = matches[0]
                    if isinstance(resultado, tuple):
                        resultado = ' '.join(resultado)
                    return str(resultado).strip()
            except Exception:
                continue
        return ""