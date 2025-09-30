# -*- coding: utf-8 -*-
"""
Demo del sistema modular con datos de prueba
"""
import sys
import os
from pathlib import Path

# Configurar paths de importación
import setup_paths

from extractors.info_basica import InformacionBasicaExtractor
from processors.excel_processor import ExcelProcessor

def generar_datos_demo():
    """Genera datos de demostración simulando varios PDFs"""
    
    extractor = InformacionBasicaExtractor()
    
    # Simular contenido de varios PDFs
    pdfs_demo = [
        {
            'archivo': 'datacredito_001.pdf',
            'contenido': """
            Fecha y Hora Consulta: 2024/01/15 2.30 PM
            Consultado por: JUAN CARLOS PEREZ
            Tipo Documento: C.C.
            Número Documento: 12345678
            Estado Documento: Vigente
            Lugar Expedición: BOGOTA
            Fecha Expedición: 15/01/1990
            Nombre: JUAN CARLOS PEREZ LOPEZ
            Rango Edad: 30-35
            Género: Masculino
            Antiguedad Ubicación: 24 Meses En La Misma Direccion
            """
        },
        {
            'archivo': 'datacredito_002.pdf',
            'contenido': """
            Fecha y Hora Consulta: 2024/01/16 10.15 AM
            Consultado por: MARIA FERNANDA GONZALEZ
            Tipo Documento: C.C.
            Número Documento: 87654321
            Estado Documento: Vigente
            Lugar Expedición: MEDELLIN
            Fecha Expedición: 22/03/1985
            Nombre: MARIA FERNANDA GONZALEZ TORRES
            Rango Edad: 35-40
            Género: Femenino
            Antiguedad Ubicación: 36 Meses En La Misma Direccion
            """
        },
        {
            'archivo': 'datacredito_003.pdf',
            'contenido': """
            Fecha y Hora Consulta: 2024/01/17 4.45 PM
            Consultado por: CARLOS ANDRES RODRIGUEZ
            Tipo Documento: C.C.
            Número Documento: 11223344
            Estado Documento: Vigente
            Lugar Expedición: CALI
            Fecha Expedición: 10/07/1992
            Nombre: CARLOS ANDRES RODRIGUEZ SILVA
            Rango Edad: 25-30
            Género: Masculino
            Antiguedad Ubicación: 12 Meses En La Misma Direccion
            """
        }
    ]
    
    # Procesar cada PDF simulado
    datos_procesados = []
    
    print("="*60)
    print("DEMO DEL SISTEMA MODULAR DATACREDITO")
    print("="*60)
    print(f"Procesando {len(pdfs_demo)} archivos de demostración...\n")
    
    for i, pdf_data in enumerate(pdfs_demo, 1):
        print(f"Procesando ({i}/{len(pdfs_demo)}): {pdf_data['archivo']}")
        
        # Extraer datos
        info_basica = extractor.extract(pdf_data['contenido'], pdf_data['archivo'])
        
        # Crear registro completo
        registro = {
            'informacion_basica': info_basica,
            '_metadata': {
                'archivo': pdf_data['archivo'],
                'ruta': f"demo/{pdf_data['archivo']}",
                'tamaño_texto': len(pdf_data['contenido']),
                'procesado': True
            }
        }
        
        datos_procesados.append(registro)
        print()
    
    return datos_procesados

def main():
    """Función principal del demo"""
    try:
        # Generar datos de demo
        datos = generar_datos_demo()
        
        # Crear procesador Excel
        excel_processor = ExcelProcessor()
        
        # Generar archivo Excel
        archivo_salida = "Demo_DataCredito_Modular.xlsx"
        excel_processor.generar_excel(datos, archivo_salida)
        
        # Mostrar estadísticas
        print("="*60)
        print("ESTADÍSTICAS DEL DEMO")
        print("="*60)
        print(f"Total procesados: {len(datos)}")
        print(f"Exitosos: {len(datos)}")
        print(f"Con errores: 0")
        print(f"Archivo generado: {archivo_salida}")
        
        print(f"\n✅ Demo completado exitosamente")
        print(f"📊 Revisa el archivo '{archivo_salida}' para ver los resultados")
        
    except Exception as e:
        print(f"❌ Error en demo: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()