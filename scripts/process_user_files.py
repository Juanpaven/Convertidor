# -*- coding: utf-8 -*-
"""
Utilidad para procesar archivos PDF enviados por el usuario
"""
import sys
from pathlib import Path
import tempfile
import os

# Configurar paths
sys.path.insert(0, str(Path(__file__).parent.parent))
import setup_paths

from scripts.analyze_pdfs import PDFAnalyzer

def process_uploaded_pdf(pdf_content: bytes, filename: str) -> dict:
    """
    Procesar un PDF enviado por el usuario
    
    Args:
        pdf_content: Contenido binario del PDF
        filename: Nombre del archivo
        
    Returns:
        Resultado del análisis
    """
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_file.write(pdf_content)
        temp_path = temp_file.name
    
    try:
        # Analizar con el sistema de memoria
        analyzer = PDFAnalyzer()
        result = analyzer.analyze_pdf_file(temp_path)
        
        # Agregar nombre original
        if result.get('success'):
            result['original_filename'] = filename
        
        return result
        
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def analyze_sample_text(text_content: str, filename: str) -> dict:
    """
    Analizar texto de muestra directamente
    
    Args:
        text_content: Contenido de texto extraído
        filename: Nombre del archivo
        
    Returns:
        Resultado del análisis
    """
    from extractors.info_basica import InformacionBasicaExtractor
    from learning.pdf_memory import PDFMemorySystem
    
    extractor = InformacionBasicaExtractor()
    memory = PDFMemorySystem()
    
    print(f"\n🔍 ANALIZANDO TEXTO: {filename}")
    print("="*60)
    
    # Extraer datos
    extracted_data = {
        'informacion_basica': extractor.extract(text_content, filename),
        '_metadata': {
            'archivo': filename,
            'tamaño_texto': len(text_content),
            'procesado': True
        }
    }
    
    # Mostrar resultados
    info_basica = extracted_data.get('informacion_basica', {})
    
    print("\n📊 DATOS EXTRAÍDOS:")
    print("-" * 40)
    
    for field, value in info_basica.items():
        status = "✅" if value and str(value).strip() else "❌"
        display_value = value if value else "(vacío)"
        print(f"{status} {field}: {display_value}")
    
    # Estadísticas
    total_fields = len(info_basica)
    filled_fields = sum(1 for v in info_basica.values() if v and str(v).strip())
    success_rate = (filled_fields / total_fields) * 100 if total_fields > 0 else 0
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   • Campos totales: {total_fields}")
    print(f"   • Campos extraídos: {filled_fields}")
    print(f"   • Tasa de éxito: {success_rate:.1f}%")
    
    # Agregar a memoria
    sample_id = memory.add_pdf_sample(filename, text_content, extracted_data)
    
    return {
        'sample_id': sample_id,
        'filename': filename,
        'extracted_data': extracted_data,
        'success_rate': success_rate,
        'success': True
    }

if __name__ == "__main__":
    print("🧠 Sistema de Memoria de PDFs - Listo para recibir archivos")
    print("Sube archivos PDF o proporciona texto extraído para análisis")