# -*- coding: utf-8 -*-
"""
Test básico del sistema modular
"""
import sys
import os
from pathlib import Path

# Configurar paths de importación
import setup_paths

def test_imports():
    """Prueba las importaciones del sistema"""
    try:
        print("Probando importaciones...")
        
        from config.field_mappings import FIELD_MAPPINGS, SECCIONES
        print("✓ Config importado correctamente")
        
        from extractors.base_extractor import BaseExtractor
        print("✓ BaseExtractor importado correctamente")
        
        from extractors.info_basica import InformacionBasicaExtractor
        print("✓ InformacionBasicaExtractor importado correctamente")
        
        from utils.pdf_reader import PDFReader
        print("✓ PDFReader importado correctamente")
        
        from processors.excel_processor import ExcelProcessor
        print("✓ ExcelProcessor importado correctamente")
        
        print("\n✅ Todas las importaciones exitosas")
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_extractor():
    """Prueba el extractor con texto de ejemplo"""
    try:
        from extractors.info_basica import InformacionBasicaExtractor
        
        extractor = InformacionBasicaExtractor()
        
        # Texto de prueba
        texto_prueba = """
        Fecha y Hora Consulta: 2024/01/15 2.30 PM
        Consultado por: JUAN PEREZ
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
        
        resultado = extractor.extract(texto_prueba, "test.pdf")
        
        print("\n🧪 Resultado de extracción de prueba:")
        for campo, valor in resultado.items():
            if valor:  # Solo mostrar campos con datos
                print(f"  {campo}: {valor}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test extractor: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("TEST DEL SISTEMA MODULAR DATACREDITO")
    print("="*50)
    
    if test_imports() and test_extractor():
        print("\n✅ Todos los tests pasaron correctamente")
    else:
        print("\n❌ Algunos tests fallaron")

# Field mappings for the modular system

FIELD_MAPPINGS = {
    "Fecha y Hora Consulta": "fecha_hora_consulta",
    "Consultado por": "consultado_por",
    "Tipo Documento": "tipo_documento",
    "Número Documento": "numero_documento",
    "Estado Documento": "estado_documento",
    "Lugar Expedición": "lugar_expedicion",
    "Fecha Expedición": "fecha_expedicion",
    "Nombre": "nombre",
    "Rango Edad": "rango_edad",
    "Género": "genero",
    "Antiguedad Ubicación": "antiguedad_ubicacion"
}

SECCIONES = [
    "InformacionBasica",
    "DatosPersonales",
    "HistorialCrediticio"
]