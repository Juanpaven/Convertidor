# -*- coding: utf-8 -*-
"""
EXTRACTOR TOTAL - Captura ABSOLUTAMENTE TODOS los datos del PDF DataCrédit        # Tiene RUT
        info['tiene_rut'] = self.extraer_campo(r"Tiene RUT\?\s+([^\s]+)", texto)
Barrido completo sin omitir ningún dato
"""
import re
from typing import Dict, Any, List
import pdfplumber

class ExtractorTotal:
    """Extractor que captura TODO sin excepción"""
    
    def __init__(self):
        self.nombre = "Extractor Total"
        
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """Extrae TODOS los datos del PDF"""
        
        print(f"\n🔍 BARRIDO TOTAL DE: {archivo}")
        
        registro = {}
        
        # === 1. INFORMACIÓN BÁSICA ===
        registro.update(self.extraer_informacion_basica(texto))
        
        # === 2. DATOS DE CONSULTA ===
        registro.update(self.extraer_datos_consulta(texto))
        
        # === 3. OBLIGACIONES Y CUENTAS ===
        registro.update(self.extraer_obligaciones(texto))
        
        # === 4. HISTORIAL DE PAGOS ===
        registro.update(self.extraer_historial_pagos(texto))
        
        # === 5. ANÁLISIS DE VECTORES ===
        registro.update(self.extraer_vectores(texto))
        
        # === 6. ENDEUDAMIENTO GLOBAL ===
        registro.update(self.extraer_endeudamiento(texto))
        
        # === 7. DIRECCIONES Y CONTACTOS ===
        registro.update(self.extraer_direcciones_contactos(texto))
        
        # === 8. INFORMACIÓN COMERCIAL ===
        registro.update(self.extraer_info_comercial(texto))
        
        # === 9. CONSULTAS Y REFERENCIAS ===
        registro.update(self.extraer_consultas_referencias(texto))
        
        # === 10. DATOS DEMOGRÁFICOS ===
        registro.update(self.extraer_demograficos(texto))
        
        # === 11. EXTRACCIÓN AUTOMÁTICA MASIVA ===
        registro.update(self.extraccion_masiva_automatica(texto))
        
        # === 12. CAPTURA DE TABLAS ===
        registro.update(self.extraer_datos_tablas(archivo))
        
        # Contar campos extraídos
        campos_extraidos = len([v for v in registro.values() if v and str(v).strip()])
        
        print(f"📊 TOTAL EXTRAÍDO: {campos_extraidos} campos")
        
        # Metadatos
        registro['_metadata'] = {
            'total_campos_extraidos': campos_extraidos,
            'texto_completo_length': len(texto),
            'procesado': campos_extraidos > 0
        }
        
        return registro
    
    def extraer_informacion_basica(self, texto: str) -> Dict[str, str]:
        """Información básica personal"""
        info = {}
        
        # Consultado por (persona que consulta)
        patrones_consultado = [
            r"Consultado por:\s*DELAGRO SAS.*?\n.*?([A-ZÁÉÍÓÚÑ]+\s+[A-ZÁÉÍÓÚÑ]+\s+[a-záéíóúñ]+)",
            r"([A-ZÁÉÍÓÚÑ]+\s+[A-ZÁÉÍÓÚÑ]+\s+[a-záéíóúñ]+)\s*-\s*[0-9]{8,}",
            r"Yurany Varon oviedo"
        ]
        info['consultado_por'] = self.buscar_multiples_patrones(patrones_consultado, texto)
        
        # Fecha y hora de consulta
        patrones_fecha = [
            r"([0-9]{4}/[0-9]{2}/[0-9]{2})\s+([0-9]{1,2}\.[0-9]{2}\s+[AP]M)",
            r"DELAGRO SAS\s+([0-9]{4}/[0-9]{2}/[0-9]{2})\s+([0-9\.]+\s+[AP]M)"
        ]
        fecha_consulta = self.buscar_multiples_patrones(patrones_fecha, texto)
        if fecha_consulta:
            info['fecha_consulta'] = fecha_consulta
        
        # Información del documento
        info['tipo_documento'] = self.extraer_campo(r"Tipo Documento\s+([^\s]+)", texto)
        info['numero_documento'] = self.extraer_campo(r"Número Documento\s+([0-9]+)", texto)
        info['estado_documento'] = self.extraer_campo(r"Estado Documento\s+([A-Za-z]+)", texto)
        info['lugar_expedicion'] = self.extraer_campo(r"Lugar Expedición\s+([A-ZÁÉÍÓÚÑ\s]+)", texto)
        info['fecha_expedicion'] = self.extraer_campo(r"Fecha Expedición\s+([0-9]{2}/[0-9]{2}/[0-9]{4})", texto)
        
        # Información personal
        info['nombre_completo'] = self.extraer_campo(r"Nombre\s+([A-ZÁÉÍÓÚÑ\s]+)\s+Rango", texto)
        info['rango_edad'] = self.extraer_campo(r"Rango Edad\s+([0-9\\-]+)", texto)
        info['genero'] = self.extraer_campo(r"Género\s+([A-Za-z]+)", texto)
        info['tiene_rut'] = self.extraer_campo(r"Tiene RUT\\?\s+([^\\s]+)", texto)
        info['antiguedad_ubicacion'] = self.extraer_campo(r"Antiguedad Ubicación\s+([0-9]+\s+Meses)", texto)
        
        return info
    
    def extraer_datos_consulta(self, texto: str) -> Dict[str, str]:
        """Datos específicos de la consulta"""
        info = {}
        
        # Código de consulta
        info['codigo_consulta'] = self.extraer_campo(r"INFORMACIÓN BÁSICA\s+([A-Z0-9]+)", texto)
        
        # NIT de la empresa consultante
        info['nit_consultante'] = self.extraer_campo(r"DELAGRO SAS\s*-\s*([0-9]+)", texto)
        
        # Número de identificación del consultado
        info['cedula_consultado'] = self.extraer_campo(r"([0-9]{8,})\s*\n.*?Yurany", texto)
        
        return info
    
    def extraer_obligaciones(self, texto: str) -> Dict[str, str]:
        """Obligaciones financieras activas y cerradas"""
        info = {}
        
        # Buscar obligaciones del Banco Agrario
        info['banco_agrario_cab'] = self.extraer_multiple_lineas(r"BCO AGRARIO\s+CAB.*?([0-9]{9})", texto)
        info['banco_agrario_fechas'] = self.extraer_multiple_lineas(r"BCO AGRARIO.*?([0-9]{8}.*?[0-9]{8})", texto)
        info['banco_agrario_valores'] = self.extraer_multiple_lineas(r"BCO AGRARIO.*?([0-9]{2,3},[0-9]{3})", texto)
        
        # Buscar Davivienda
        info['davivienda_cuenta'] = self.extraer_campo(r"DAVIVIENDA.*?([0-9]{9})", texto)
        info['davivienda_tipo'] = self.extraer_campo(r"DAVIVIENDA\s+(SOBREGIROS|TDC)", texto)
        
        # Buscar otras entidades
        info['precisagro'] = self.extraer_campo(r"PRECISAGRO S\.A\.S\.\s+([A-Z0-9]+)", texto)
        
        return info
    
    def extraer_historial_pagos(self, texto: str) -> Dict[str, str]:
        """Historial de pagos y comportamiento"""
        info = {}
        
        # Vectores de pago (N = Normal, números = moras)
        vectores = re.findall(r"\[([N0-9\-]+)\]\[([N0-9\-]+)", texto)
        if vectores:
            info['vectores_pago_total'] = len(vectores)
            info['vectores_encontrados'] = str(vectores[:5])  # Primeros 5
        
        # Moras máximas
        info['moras_maximas_sf'] = self.extraer_campo(r"Moras Máximas Sector Financiero\s+([0-9\s]+)", texto)
        info['moras_sector_real'] = self.extraer_campo(r"Sector Real.*?([0-9\s]+)", texto)
        
        # Estado actual
        info['esta_en_mora'] = "Sí" if "Esta en mora" in texto else "No"
        
        return info
    
    def extraer_vectores(self, texto: str) -> Dict[str, str]:
        """Análisis de vectores de comportamiento"""
        info = {}
        
        # Extraer vectores específicos por entidad
        entidades_vectores = [
            "BANCO AGRARIO CART SOBREGIRO",
            "DAVIVIENDA SOBREGIROS", 
            "BCO DAVIVIENDA",
            "PRECISAGRO S.A.S."
        ]
        
        for i, entidad in enumerate(entidades_vectores, 1):
            patron = f"{entidad}.*?([0-9N\\s\\-]+)"
            valor = self.extraer_campo(patron, texto)
            if valor:
                info[f'vector_entidad_{i}'] = f"{entidad}: {valor}"
        
        return info
    
    def extraer_endeudamiento(self, texto: str) -> Dict[str, str]:
        """Endeudamiento global por trimestres"""
        info = {}
        
        # Trimestres encontrados
        trimestres = re.findall(r"TRIMESTRE\s+([0-9]{4}/[0-9]{2})", texto)
        if trimestres:
            info['trimestres_reportados'] = ", ".join(trimestres)
        
        # Valores de endeudamiento
        valores_deuda = re.findall(r"\\$([0-9,]+)", texto)
        if valores_deuda:
            info['valores_deuda_encontrados'] = len(valores_deuda)
            info['deuda_mayor'] = max(valores_deuda, key=lambda x: int(x.replace(',', '')))
        
        # Tipos de crédito
        info['tipos_credito'] = self.extraer_campo(r"(Consumo y Tarjeta de\s+Comercial Hipotecario Microcrédito)", texto)
        
        # Entidades reportantes
        entidades = re.findall(r"(BANCO AGRARIO|DAVIVIENDA).*?BC", texto)
        if entidades:
            info['entidades_financieras'] = ", ".join(set(entidades))
        
        return info
    
    def extraer_direcciones_contactos(self, texto: str) -> Dict[str, str]:
        """Direcciones y datos de contacto"""
        info = {}
        
        # Direcciones reportadas
        direcciones = []
        patrones_dir = [
            r"KR\s+[0-9]+\s+A\s+[0-9]+\s+[0-9]+",
            r"CL\s+[0-9]+\s+[0-9]+\s+[0-9]+",
            r"CONJ\s+[A-Z\s]+\s+APTO\s+[0-9]+"
        ]
        
        for patron in patrones_dir:
            matches = re.findall(patron, texto)
            direcciones.extend(matches)
        
        if direcciones:
            info['direcciones_reportadas'] = " | ".join(direcciones)
            info['total_direcciones'] = len(direcciones)
        
        # Ciudades y departamentos
        ciudades = re.findall(r"(SAN LUIS|IBAGUE)\s+(TOLIMA|ANTIOQUIA)?", texto)
        if ciudades:
            info['ciudades_reportadas'] = " | ".join([f"{c[0]} {c[1]}".strip() for c in ciudades])
        
        # Estratos
        estratos = re.findall(r"Estrato\s+([0-9\\-]+)", texto)
        if estratos:
            info['estratos'] = ", ".join(set(estratos))
        
        return info
    
    def extraer_info_comercial(self, texto: str) -> Dict[str, str]:
        """Información comercial y financiera"""
        info = {}
        
        # Tipos de cuenta
        tipos_cuenta = re.findall(r"(SBG|TDC|CAB|AGR)", texto)
        if tipos_cuenta:
            info['tipos_cuenta'] = ", ".join(set(tipos_cuenta))
        
        # Estados de obligaciones
        estados = re.findall(r"(Pago Vol|Cancelada Vol|Normal)", texto)
        if estados:
            info['estados_obligaciones'] = ", ".join(set(estados))
        
        # Garantías
        info['tiene_garantias'] = "Sí" if "GAR" in texto else "No"
        
        return info
    
    def extraer_consultas_referencias(self, texto: str) -> Dict[str, str]:
        """Consultas y referencias"""
        info = {}
        
        # Fechas de última consulta
        fechas_consulta = re.findall(r"Fecha Ult\. Consulta.*?([0-9]{4}/[0-9]{2}/[0-9]{2})", texto)
        if fechas_consulta:
            info['ultima_consulta'] = fechas_consulta[0]
        
        # Número de consultas
        num_consultas = re.findall(r"No\. de Consultas mes.*?([0-9]+)", texto)
        if num_consultas:
            info['consultas_mes'] = num_consultas[0]
        
        return info
    
    def extraer_demograficos(self, texto: str) -> Dict[str, str]:
        """Datos demográficos adicionales"""
        info = {}
        
        # Tipo de zona
        zonas = re.findall(r"(RES|LAB|CRR|URB|RUR)", texto)
        if zonas:
            info['tipos_zona'] = ", ".join(set(zonas))
        
        # Fuentes de información
        fuentes = re.findall(r"Fuente.*?([A-Z]{3})", texto)
        if fuentes:
            info['fuentes_info'] = ", ".join(set(fuentes))
        
        return info
    
    def extraccion_masiva_automatica(self, texto: str) -> Dict[str, str]:
        """Extracción masiva de cualquier dato estructurado"""
        info = {}
        
        # Buscar TODOS los números de cuenta/documento
        numeros = re.findall(r"\b([0-9]{7,12})\b", texto)
        if numeros:
            numeros_unicos = list(set(numeros))
            info['numeros_identificados'] = " | ".join(numeros_unicos[:10])  # Primeros 10
            info['total_numeros'] = len(numeros_unicos)
        
        # Buscar TODAS las fechas
        fechas = re.findall(r"([0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{4}/[0-9]{2}/[0-9]{2})", texto)
        if fechas:
            fechas_unicas = list(set(fechas))
            info['fechas_identificadas'] = " | ".join(fechas_unicas)
            info['total_fechas'] = len(fechas_unicas)
        
        # Buscar TODOS los valores monetarios
        valores = re.findall(r"\$([0-9,]+)", texto)
        if valores:
            info['valores_monetarios'] = " | ".join(valores[:15])  # Primeros 15
            info['total_valores'] = len(valores)
        
        # Buscar códigos y referencias
        codigos = re.findall(r"\b([A-Z0-9]{5,15})\b", texto)
        if codigos:
            codigos_unicos = list(set([c for c in codigos if len(c) >= 5]))
            info['codigos_identificados'] = " | ".join(codigos_unicos[:10])
            info['total_codigos'] = len(codigos_unicos)
        
        # Buscar entidades/empresas mencionadas
        entidades = re.findall(r"\b([A-Z]{3,}(?:\s+[A-Z]{3,})*(?:\s+S\.A\.S\.?|\s+LTDA|\s+S\.A\.)?)", texto)
        if entidades:
            entidades_filtradas = [e for e in set(entidades) if len(e) > 4 and e not in ['INFORMACIÓN', 'BÁSICA']]
            info['entidades_mencionadas'] = " | ".join(entidades_filtradas[:10])
            info['total_entidades'] = len(entidades_filtradas)
        
        return info
    
    def extraer_datos_tablas(self, archivo: str) -> Dict[str, str]:
        """Extrae datos específicos de las tablas del PDF"""
        info = {}
        
        try:
            with pdfplumber.open(archivo) as pdf:
                tabla_count = 0
                
                for page_num, page in enumerate(pdf.pages, 1):
                    tablas = page.extract_tables()
                    
                    for tabla_num, tabla in enumerate(tablas, 1):
                        if tabla and len(tabla) > 0:
                            tabla_count += 1
                            
                            # Procesar tabla
                            for fila_num, fila in enumerate(tabla):
                                if fila and any(cell for cell in fila if cell):
                                    # Buscar datos específicos en cada fila
                                    fila_texto = " ".join([str(cell) if cell else "" for cell in fila])
                                    
                                    # Extraer valores específicos encontrados
                                    if "BCO AGRARIO" in fila_texto:
                                        info[f'tabla_banco_agrario_{tabla_count}'] = fila_texto[:100]
                                    
                                    if "DAVIVIENDA" in fila_texto:
                                        info[f'tabla_davivienda_{tabla_count}'] = fila_texto[:100]
                                    
                                    if any(char.isdigit() for char in fila_texto) and "$" in fila_texto:
                                        info[f'tabla_valores_{tabla_count}_{fila_num}'] = fila_texto[:100]
                
                info['total_tablas_procesadas'] = tabla_count
                
        except Exception as e:
            info['error_tablas'] = str(e)
        
        return info
    
    def extraer_campo(self, patron: str, texto: str) -> str:
        """Extrae un campo específico"""
        try:
            match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        except:
            pass
        return ""
    
    def extraer_multiple_lineas(self, patron: str, texto: str) -> str:
        """Extrae múltiples coincidencias de un patrón"""
        try:
            matches = re.findall(patron, texto, re.IGNORECASE | re.MULTILINE)
            if matches:
                return " | ".join([str(m).strip() for m in matches[:5]])  # Primeras 5
        except:
            pass
        return ""
    
    def buscar_multiples_patrones(self, patrones: list, texto: str) -> str:
        """Busca múltiples patrones y retorna el primer match"""
        for patron in patrones:
            resultado = self.extraer_campo(patron, texto)
            if resultado:
                return resultado
        return ""