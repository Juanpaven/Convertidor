# -*- coding: utf-8 -*-
"""
CONVERTIDOR TOTAL - Sistema completo de extracción masiva
Captura ABSOLUTAMENTE TODOS los datos de los PDFs DataCrédito
"""
import os
import pdfplumber
from typing import List, Dict, Any
import sys
from datetime import datetime

# Importar extractores
try:
    from extractor_total import ExtractorTotal
    from excel_processor_total import ExcelProcessorTotal
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

class ConvertidorTotal:
    """Convertidor completo con extracción masiva"""
    
    def __init__(self):
        self.nombre = "Convertidor Total DataCrédito"
        self.version = "1.0 - EXTRACCIÓN MASIVA"
        self.extractor = ExtractorTotal()
        self.procesador = ExcelProcessorTotal()
        
    def procesar_todos_pdfs(self, carpeta_pdfs: str) -> bool:
        """Procesa TODOS los PDFs de la carpeta con extracción completa"""
        
        print(f"🚀 INICIANDO {self.nombre} v{self.version}")
        print(f"📁 Carpeta: {carpeta_pdfs}")
        print("="*80)
        
        # Validar carpeta
        if not os.path.exists(carpeta_pdfs):
            print(f"❌ La carpeta no existe: {carpeta_pdfs}")
            return False
        
        # Buscar PDFs
        archivos_pdf = self.buscar_pdfs(carpeta_pdfs)
        
        if not archivos_pdf:
            print("❌ No se encontraron archivos PDF")
            return False
        
        print(f"📄 PDFs encontrados: {len(archivos_pdf)}")
        
        # Procesar cada PDF
        todos_datos = []
        procesados = 0
        errores = 0
        
        for i, archivo_pdf in enumerate(archivos_pdf, 1):
            print(f"\n🔍 [{i}/{len(archivos_pdf)}] Procesando: {os.path.basename(archivo_pdf)}")
            
            try:
                # Extraer datos completos
                datos = self.procesar_pdf_completo(archivo_pdf)
                
                if datos and datos.get('_metadata', {}).get('procesado', False):
                    # Agregar información del archivo
                    datos['archivo'] = os.path.basename(archivo_pdf)
                    datos['ruta_completa'] = archivo_pdf
                    datos['fecha_procesamiento'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    todos_datos.append(datos)
                    procesados += 1
                    
                    # Mostrar resumen del PDF
                    campos_extraidos = datos.get('_metadata', {}).get('total_campos_extraidos', 0)
                    print(f"   ✅ Extraídos: {campos_extraidos} campos")
                    
                else:
                    print(f"   ⚠️ PDF sin datos útiles")
                    errores += 1
                    
            except Exception as e:
                print(f"   ❌ Error procesando: {e}")
                errores += 1
        
        # Resumen final
        print("\n" + "="*80)
        print(f"📊 RESUMEN FINAL:")
        print(f"   ✅ PDFs procesados exitosamente: {procesados}")
        print(f"   ❌ PDFs con errores: {errores}")
        print(f"   📄 Total PDFs: {len(archivos_pdf)}")
        
        if procesados == 0:
            print("❌ No se procesó ningún PDF exitosamente")
            return False
        
        # Generar Excel con TODOS los datos
        print(f"\n🔄 Generando archivo Excel con {procesados} PDFs...")
        
        exito_excel = self.procesador.procesar(todos_datos, carpeta_pdfs)
        
        if exito_excel:
            print("\n🎉 ¡PROCESAMIENTO COMPLETADO EXITOSAMENTE!")
            print("📈 El archivo Excel contiene TODOS los datos extraídos")
            return True
        else:
            print("\n❌ Error generando archivo Excel")
            return False
    
    def buscar_pdfs(self, carpeta: str) -> List[str]:
        """Busca todos los archivos PDF en la carpeta"""
        pdfs = []
        
        try:
            for archivo in os.listdir(carpeta):
                if archivo.lower().endswith('.pdf'):
                    ruta_completa = os.path.join(carpeta, archivo)
                    if os.path.isfile(ruta_completa):
                        pdfs.append(ruta_completa)
        except Exception as e:
            print(f"❌ Error buscando PDFs: {e}")
        
        return sorted(pdfs)
    
    def procesar_pdf_completo(self, archivo_pdf: str) -> Dict[str, Any]:
        """Procesa un PDF completo extrayendo TODOS los datos"""
        
        try:
            # Extraer texto completo
            texto_completo = self.extraer_texto_completo(archivo_pdf)
            
            if not texto_completo:
                print(f"   ⚠️ No se pudo extraer texto")
                return {}
            
            # Aplicar extractor total
            datos_extraidos = self.extractor.extract(texto_completo, archivo_pdf)
            
            return datos_extraidos
            
        except Exception as e:
            print(f"   ❌ Error procesando PDF: {e}")
            return {}
    
    def extraer_texto_completo(self, archivo_pdf: str) -> str:
        """Extrae todo el texto del PDF"""
        
        texto_completo = ""
        
        try:
            with pdfplumber.open(archivo_pdf) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        texto_completo += f"\n=== PÁGINA {page_num} ===\n"
                        texto_completo += texto_pagina
                        texto_completo += "\n"
                        
        except Exception as e:
            print(f"   ❌ Error extrayendo texto: {e}")
            return ""
        
        return texto_completo

def main():
    """Función principal"""
    
    # Carpeta con los PDFs
    carpeta_pdfs = r"C:\Users\delag\OneDrive\Escritorio\Juan Avendaño\Convertidor"
    
    # Crear convertidor
    convertidor = ConvertidorTotal()
    
    # Procesar todos los PDFs
    exito = convertidor.procesar_todos_pdfs(carpeta_pdfs)
    
    if exito:
        print("\n🎉 ¡CONVERSIÓN TOTAL COMPLETADA!")
        print("📂 Revisa el archivo Excel generado en la carpeta")
    else:
        print("\n❌ Error en el procesamiento")
    
    # Pausa para ver resultados
    input("\n📋 Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()