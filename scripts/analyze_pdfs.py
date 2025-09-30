# -*- coding: utf-8 -*-
"""
Analizador de PDFs con Sistema de Memoria
Procesa archivos PDF y los almacena para aprendizaje continuo
"""
import sys
from pathlib import Path

# Configurar paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import setup_paths

from extractors.info_basica import InformacionBasicaExtractor
from utils.pdf_reader import PDFReader
from learning.pdf_memory import PDFMemorySystem

class PDFAnalyzer:
    """Analizador de PDFs con memoria de aprendizaje"""
    
    def __init__(self):
        self.pdf_reader = PDFReader()
        self.extractor = InformacionBasicaExtractor()
        self.memory = PDFMemorySystem()
        
    def analyze_pdf_file(self, pdf_path: str) -> dict:
        """
        Analizar un archivo PDF y guardarlo en memoria
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            Diccionario con análisis completo
        """
        pdf_path = Path(pdf_path)
        
        print(f"\n🔍 ANALIZANDO: {pdf_path.name}")
        print("="*60)
        
        try:
            # Extraer texto del PDF
            print("📄 Extrayendo texto del PDF...")
            extracted_text = self.pdf_reader.extraer_texto(str(pdf_path))
            
            if not extracted_text:
                print("❌ No se pudo extraer texto del PDF")
                return {'error': 'No se pudo extraer texto'}
            
            print(f"✅ Texto extraído: {len(extracted_text)} caracteres")
            
            # Extraer datos estructurados
            print("🎯 Extrayendo datos estructurados...")
            extracted_data = {
                'informacion_basica': self.extractor.extract(extracted_text, pdf_path.name),
                '_metadata': {
                    'archivo': pdf_path.name,
                    'ruta': str(pdf_path),
                    'tamaño_texto': len(extracted_text),
                    'procesado': True
                }
            }
            
            # Mostrar datos extraídos
            self._display_extracted_data(extracted_data)
            
            # Agregar a memoria del sistema
            print("\n🧠 Agregando a memoria del sistema...")
            sample_id = self.memory.add_pdf_sample(
                pdf_path.name, 
                extracted_text, 
                extracted_data
            )
            
            # Generar análisis detallado
            analysis = self._generate_detailed_analysis(extracted_text, extracted_data)
            
            result = {
                'sample_id': sample_id,
                'pdf_name': pdf_path.name,
                'extracted_text': extracted_text,
                'extracted_data': extracted_data,
                'analysis': analysis,
                'success': True
            }
            
            print(f"\n✅ Análisis completado - ID de muestra: {sample_id}")
            return result
            
        except Exception as e:
            print(f"❌ Error analizando {pdf_path.name}: {e}")
            return {'error': str(e), 'success': False}
    
    def _display_extracted_data(self, data: dict):
        """Mostrar datos extraídos de forma organizada"""
        info_basica = data.get('informacion_basica', {})
        
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
    
    def _generate_detailed_analysis(self, text: str, data: dict) -> dict:
        """Generar análisis detallado del PDF"""
        lines = text.splitlines()
        
        analysis = {
            'text_stats': {
                'total_lines': len(lines),
                'total_characters': len(text),
                'total_words': len(text.split()),
                'non_empty_lines': len([l for l in lines if l.strip()])
            },
            'content_analysis': {},
            'extraction_issues': [],
            'recommendations': []
        }
        
        # Análisis de contenido
        info_basica = data.get('informacion_basica', {})
        
        # Buscar patrones problemáticos
        for field, value in info_basica.items():
            if not value or not str(value).strip():
                # Buscar posibles valores en el texto
                suggestions = self._find_field_suggestions(field, text)
                if suggestions:
                    analysis['extraction_issues'].append({
                        'field': field,
                        'issue': 'Campo vacío',
                        'suggestions': suggestions[:3]  # Top 3 sugerencias
                    })
        
        # Recomendaciones generales
        if analysis['extraction_issues']:
            analysis['recommendations'].append(
                "Revisar patrones de extracción para campos vacíos"
            )
        
        return analysis
    
    def _find_field_suggestions(self, field: str, text: str) -> list:
        """Buscar posibles valores para un campo en el texto"""
        suggestions = []
        
        if 'consultado' in field.lower():
            # Buscar nombres de personas
            import re
            patterns = [
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
                r'Consultado por[:\s]*([A-ZÁÉÍÓÚÑ\s]+)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                suggestions.extend(matches)
        
        elif 'fecha' in field.lower():
            # Buscar fechas
            import re
            patterns = [
                r'\d{4}/\d{2}/\d{2}',
                r'\d{2}/\d{2}/\d{4}',
                r'\d{4}-\d{2}-\d{2}'
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                suggestions.extend(matches)
        
        return list(set(suggestions))  # Eliminar duplicados
    
    def show_memory_report(self):
        """Mostrar reporte de memoria del sistema"""
        print("\n" + "="*60)
        print(self.memory.generate_memory_report())
        print("="*60)
    
    def get_recommendations(self):
        """Obtener recomendaciones del sistema"""
        recommendations = self.memory.get_extraction_recommendations()
        
        print("\n🎯 RECOMENDACIONES DEL SISTEMA:")
        print("-" * 40)
        
        if recommendations['problematic_fields']:
            print("⚠️  Campos problemáticos:")
            for field_info in recommendations['problematic_fields']:
                print(f"   • {field_info['field']}: {field_info['success_rate']:.1f}% éxito")
                if field_info['suggestions']:
                    print(f"     Sugerencias: {', '.join(field_info['suggestions'][:2])}")
        
        if recommendations['improved_patterns']:
            print("\n🔧 Patrones mejorados disponibles:")
            for field, patterns in recommendations['improved_patterns'].items():
                print(f"   • {field}: {len(patterns)} patrones aprendidos")

def main():
    """Función principal para análisis interactivo"""
    analyzer = PDFAnalyzer()
    
    print("🧠 ANALIZADOR DE PDFs CON MEMORIA")
    print("="*50)
    print("Proporciona archivos PDF para análisis y aprendizaje continuo")
    print("El sistema recordará cada archivo para mejorar las extracciones")
    print()
    
    # Mostrar estado actual de la memoria
    analyzer.show_memory_report()
    
    return analyzer

if __name__ == "__main__":
    analyzer = main()