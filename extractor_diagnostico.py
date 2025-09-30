# -*- coding: utf-8 -*-
"""
EXTRACTOR CON DIAGNÓSTICO EN TIEMPO REAL
Muestra exactamente qué extrae de cada PDF paso a paso
"""
import re
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.extractors.base_extractor import BaseExtractor

class ExtractorDiagnostico(BaseExtractor):
    """Extractor que muestra diagnóstico detallado de cada extracción"""
    
    def __init__(self):
        super().__init__("Extractor con Diagnóstico")
        self.debug = True
        
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """Extrae información con diagnóstico completo"""
        
        print(f"\n{'='*80}")
        print(f"🔍 DIAGNÓSTICO DE EXTRACCIÓN: {archivo}")
        print(f"{'='*80}")
        print(f"📄 Longitud del texto: {len(texto)} caracteres")
        print(f"📝 Líneas de texto: {len(texto.split('\\n'))}")
        
        # Mostrar primeras líneas del texto
        print(f"\n📋 PRIMERAS 20 LÍNEAS DEL PDF:")
        lineas = texto.split('\\n')
        for i, linea in enumerate(lineas[:20], 1):
            if linea.strip():
                print(f"   {i:2d}: {linea.strip()}")
        
        registro = {}
        campos_extraidos = 0
        
        # === INFORMACIÓN BÁSICA ===
        print(f"\n🔍 EXTRAYENDO INFORMACIÓN BÁSICA:")
        
        # 1. Consultado por
        consultado = self.extraer_con_diagnostico(
            "Consultado por", 
            [
                r"Consultado por[:\\s]*([A-ZÁÉÍÓÚÑ]+(?:\\s+[A-ZÁÉÍÓÚÑ]+)+)(?:\\s+(?:DELAGRO|SAS|LTDA|S\\.A\\.S|S\\.A|EMPRESA))",
                r"([A-ZÁÉÍÓÚÑ]+\\s+[A-ZÁÉÍÓÚÑ]+\\s+[a-záéíóúñ]+)(?=\\s*DELAGRO)",
                r"Consultado por[:\\s]*([A-ZÁÉÍÓÚÑ\\s]+?)(?=\\s*(?:DELAGRO|SAS|LTDA))"
            ],
            texto
        )
        if consultado:
            registro['consultado_por'] = consultado
            campos_extraidos += 1
        
        # 2. Fecha y hora
        fecha_hora = self.extraer_con_diagnostico(
            "Fecha y Hora",
            [
                r"Fecha y Hora Consulta[:\\s]*([0-9]{2}/[0-9]{2}/[0-9]{4}\\s+[0-9]{1,2}:[0-9]{2})",
                r"([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\\s+[0-9]{1,2}:[0-9]{2}",
                r"Fecha[:\\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})"
            ],
            texto
        )
        if fecha_hora:
            registro['fecha_consulta'] = fecha_hora
            campos_extraidos += 1
        
        # 3. Tipo de documento
        tipo_doc = self.extraer_con_diagnostico(
            "Tipo Documento",
            [
                r"Tipo Documento[:\\s]*([A-Za-z\\.\\s]+?)(?=\\s*Número|\\s*$)",
                r"(Cédula de Ciudadanía)",
                r"(C\\.C\\.)"
            ],
            texto
        )
        if tipo_doc:
            registro['tipo_documento'] = tipo_doc
            campos_extraidos += 1
        
        # 4. Número de documento
        numero_doc = self.extraer_con_diagnostico(
            "Número Documento",
            [
                r"Número Documento[:\\s]*([0-9\\.]+)",
                r"C\\.C\\.[:\\s]*([0-9\\.]+)",
                r"No\\.[:\\s]*([0-9\\.]+)"
            ],
            texto
        )
        if numero_doc:
            registro['numero_documento'] = numero_doc
            campos_extraidos += 1
        
        # 5. Nombre
        nombre = self.extraer_con_diagnostico(
            "Nombre",
            [
                r"Nombre[:\\s]*([A-ZÁÉÍÓÚÑ\\s]+)(?=\\s*Rango Edad|$)",
                r"Nombres y Apellidos[:\\s]*([A-ZÁÉÍÓÚÑ\\s]+)"
            ],
            texto
        )
        if nombre:
            registro['nombre_completo'] = nombre
            campos_extraidos += 1
        
        # 6. Estado documento
        estado = self.extraer_con_diagnostico(
            "Estado Documento",
            [
                r"Estado Documento[:\\s]*([A-Za-zÁÉÍÓÚÑ]+)",
                r"(Vigente)",
                r"(Vencido)"
            ],
            texto
        )
        if estado:
            registro['estado_documento'] = estado
            campos_extraidos += 1
        
        # 7. Lugar expedición
        lugar = self.extraer_con_diagnostico(
            "Lugar Expedición",
            [
                r"Lugar Expedición[:\\s]*([A-ZÁÉÍÓÚÑa-z\\s]+?)(?=\\s*Fecha Expedici|$)",
                r"Expedido en[:\\s]*([A-ZÁÉÍÓÚÑa-z\\s]+)"
            ],
            texto
        )
        if lugar:
            registro['lugar_expedicion'] = lugar
            campos_extraidos += 1
        
        # 8. Fecha expedición
        fecha_exp = self.extraer_con_diagnostico(
            "Fecha Expedición",
            [
                r"Fecha Expedición[:\\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})",
                r"Expedido el[:\\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})"
            ],
            texto
        )
        if fecha_exp:
            registro['fecha_expedicion'] = fecha_exp
            campos_extraidos += 1
        
        # 9. Rango edad
        edad = self.extraer_con_diagnostico(
            "Rango Edad",
            [
                r"Rango Edad[:\\s]*([0-9\\-]+)",
                r"(\\d{2}-\\d{2})",
                r"Edad[:\\s]*([0-9\\-]+)"
            ],
            texto
        )
        if edad:
            registro['rango_edad'] = edad
            campos_extraidos += 1
        
        # 10. Género
        genero = self.extraer_con_diagnostico(
            "Género",
            [
                r"Género[:\\s]*([A-Za-zÁÉÍÓÚÑ]+)",
                r"(Femenino)",
                r"(Masculino)"
            ],
            texto
        )
        if genero:
            registro['genero'] = genero
            campos_extraidos += 1
        
        # 11. Antigüedad ubicación
        antiguedad = self.extraer_con_diagnostico(
            "Antigüedad Ubicación",
            [
                r"Antiguedad Ubicación[:\\s]*([0-9]+\\s*Meses\\s*[A-Za-z\\s]+?)(?=\\s*ARTICULO|\\s*-|$)",
                r"(\\d+\\s*Meses\\s*[A-Za-z\\s]+?)(?=\\s*ARTICULO|\\s*-|$)"
            ],
            texto
        )
        if antiguedad:
            registro['antiguedad_ubicacion'] = antiguedad
            campos_extraidos += 1
        
        # === INFORMACIÓN ADICIONAL ===
        print(f"\n🔍 EXTRAYENDO INFORMACIÓN ADICIONAL:")
        
        # Buscar patrones adicionales
        patrones_adicionales = {
            'direccion': r"(?:Dirección|Residencia)[:\\s]*([^\\n]+)",
            'telefono': r"(?:Teléfono|Tel)[:\\s]*([^\\n]+)",
            'email': r"(?:Email|Correo)[:\\s]*([^\\n]+)",
            'score': r"(?:Score|Puntaje)[:\\s]*([^\\n]+)",
            'saldo': r"(?:Saldo|Valor)[:\\s]*([^\\n]+)",
            'obligaciones': r"(?:Obligacion|Credito|Tarjeta)[:\\s]*([^\\n]+)"
        }
        
        for campo, patron in patrones_adicionales.items():
            valor = self.extraer_con_diagnostico(campo, [patron], texto)
            if valor:
                registro[campo] = valor
                campos_extraidos += 1
        
        # === RESUMEN ===
        print(f"\n{'='*80}")
        print(f"📊 RESUMEN DE EXTRACCIÓN")
        print(f"{'='*80}")
        print(f"✅ Total de campos extraídos: {campos_extraidos}")
        print(f"📋 Campos encontrados:")
        for campo, valor in registro.items():
            print(f"   → {campo}: {valor}")
        
        if campos_extraidos == 0:
            print(f"❌ ¡NO SE EXTRAJO NINGÚN CAMPO!")
            print(f"💡 Mostrando texto completo para análisis manual:")
            print(f"\\n{'-'*40}")
            print(texto[:2000])  # Primeros 2000 caracteres
            print(f"{'-'*40}")
        
        # Agregar metadatos
        registro['_metadata'] = {
            'archivo': archivo,
            'total_campos_extraidos': campos_extraidos,
            'texto_completo_length': len(texto),
            'procesado': campos_extraidos > 0
        }
        
        return registro
    
    def extraer_con_diagnostico(self, nombre_campo: str, patrones: list, texto: str) -> str:
        """Extrae un campo con diagnóstico detallado"""
        print(f"\\n🔍 Extrayendo '{nombre_campo}':")
        
        for i, patron in enumerate(patrones, 1):
            print(f"   Patrón {i}: {patron}")
            matches = re.findall(patron, texto, re.IGNORECASE | re.MULTILINE)
            
            if matches:
                valor = matches[0].strip() if isinstance(matches[0], str) else str(matches[0]).strip()
                print(f"   ✅ ENCONTRADO: '{valor}' (patrón {i})")
                return valor
            else:
                print(f"   ❌ No encontrado")
        
        return ""

def main():
    """Función principal para probar el extractor"""
    import pdfplumber
    from pathlib import Path
    
    if len(sys.argv) > 1:
        archivo_pdf = sys.argv[1]
        if not Path(archivo_pdf).exists():
            print(f"❌ Archivo no encontrado: {archivo_pdf}")
            return
    else:
        # Buscar el primer PDF
        pdfs = list(Path('.').glob('*.pdf'))
        if not pdfs:
            print("❌ No se encontraron archivos PDF")
            print("💡 USO: python extractor_diagnostico.py archivo.pdf")
            return
        archivo_pdf = pdfs[0]
    
    print(f"🔍 PROBANDO EXTRACTOR CON: {archivo_pdf}")
    
    # Extraer texto del PDF
    try:
        with pdfplumber.open(archivo_pdf) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text() or ""
    except Exception as e:
        print(f"❌ Error leyendo PDF: {e}")
        return
    
    # Usar el extractor con diagnóstico
    extractor = ExtractorDiagnostico()
    resultado = extractor.extract(texto, str(archivo_pdf))
    
    print(f"\\n{'='*80}")
    print(f"🎯 RESULTADO FINAL:")
    print(f"{'='*80}")
    for campo, valor in resultado.items():
        if campo != '_metadata':
            print(f"{campo}: {valor}")

if __name__ == "__main__":
    main()