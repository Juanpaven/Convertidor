# -*- coding: utf-8 -*-
"""
Sistema de Memoria y Aprendizaje de PDFs
Almacena y analiza archivos de muestra para mejorar la extracción
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class PDFMemorySystem:
    """Sistema que aprende de archivos PDF para mejorar extracciones"""
    
    def __init__(self, memory_dir: str = None):
        if memory_dir is None:
            memory_dir = Path(__file__).parent / "memory_data"
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Archivos de memoria
        self.samples_file = self.memory_dir / "pdf_samples.json"
        self.patterns_file = self.memory_dir / "learned_patterns.json"
        self.statistics_file = self.memory_dir / "extraction_stats.json"
        
        # Cargar datos existentes
        self.samples = self._load_samples()
        self.patterns = self._load_patterns()
        self.statistics = self._load_statistics()
    
    def add_pdf_sample(self, pdf_name: str, extracted_text: str, 
                      extracted_data: Dict[str, Any]) -> str:
        """
        Agregar una muestra de PDF al sistema de memoria
        
        Args:
            pdf_name: Nombre del archivo PDF
            extracted_text: Texto completo extraído
            extracted_data: Datos estructurados extraídos
            
        Returns:
            ID único de la muestra
        """
        # Crear ID único basado en contenido
        sample_id = hashlib.md5(extracted_text.encode()).hexdigest()[:12]
        
        # Crear registro de muestra
        sample = {
            'id': sample_id,
            'pdf_name': pdf_name,
            'timestamp': datetime.now().isoformat(),
            'text_length': len(extracted_text),
            'extracted_text': extracted_text,
            'extracted_data': extracted_data,
            'analysis': self._analyze_sample(extracted_text, extracted_data)
        }
        
        # Guardar muestra
        self.samples[sample_id] = sample
        self._save_samples()
        
        # Actualizar patrones aprendidos
        self._update_patterns(sample)
        
        # Actualizar estadísticas
        self._update_statistics(sample)
        
        print(f"✅ Muestra agregada: {pdf_name} (ID: {sample_id})")
        return sample_id
    
    def _analyze_sample(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar una muestra para identificar patrones"""
        analysis = {
            'field_patterns': {},
            'text_characteristics': {},
            'extraction_quality': {}
        }
        
        # Analizar patrones de campos
        for field, value in data.get('informacion_basica', {}).items():
            if value and value.strip():
                pattern_info = self._identify_field_pattern(field, value, text)
                analysis['field_patterns'][field] = pattern_info
        
        # Características del texto
        analysis['text_characteristics'] = {
            'has_multiple_pages': 'Página' in text,
            'has_timestamps': bool(re.search(r'\d{4}/\d{2}/\d{2}', text)),
            'has_document_numbers': bool(re.search(r'\d{8,}', text)),
            'character_encoding': 'utf-8' if any(ord(c) > 127 for c in text) else 'ascii',
            'line_count': len(text.splitlines()),
            'word_count': len(text.split())
        }
        
        # Calidad de extracción
        total_fields = len(data.get('informacion_basica', {}))
        filled_fields = sum(1 for v in data.get('informacion_basica', {}).values() 
                           if v and str(v).strip())
        
        analysis['extraction_quality'] = {
            'total_fields': total_fields,
            'filled_fields': filled_fields,
            'success_rate': (filled_fields / total_fields) * 100 if total_fields > 0 else 0,
            'empty_fields': [k for k, v in data.get('informacion_basica', {}).items() 
                           if not v or not str(v).strip()]
        }
        
        return analysis
    
    def _identify_field_pattern(self, field: str, value: str, full_text: str) -> Dict[str, Any]:
        """Identificar patrones para un campo específico"""
        pattern_info = {
            'value': value,
            'value_type': self._classify_value_type(value),
            'context_before': '',
            'context_after': '',
            'line_context': '',
            'regex_patterns': []
        }
        
        # Buscar contexto en el texto
        lines = full_text.splitlines()
        for i, line in enumerate(lines):
            if value in line:
                pattern_info['line_context'] = line.strip()
                if i > 0:
                    pattern_info['context_before'] = lines[i-1].strip()
                if i < len(lines) - 1:
                    pattern_info['context_after'] = lines[i+1].strip()
                break
        
        # Generar patrones regex posibles
        pattern_info['regex_patterns'] = self._generate_regex_patterns(field, value)
        
        return pattern_info
    
    def _classify_value_type(self, value: str) -> str:
        """Clasificar el tipo de valor"""
        if re.match(r'^\d{4}/\d{2}/\d{2}', value):
            return 'date'
        elif re.match(r'^\d{8,}$', value):
            return 'document_number'
        elif re.match(r'^[A-ZÁÉÍÓÚÑ\s]+$', value):
            return 'name'
        elif 'AM' in value or 'PM' in value:
            return 'datetime'
        elif re.match(r'^\d+-\d+$', value):
            return 'age_range'
        elif value.upper() in ['MASCULINO', 'FEMENINO']:
            return 'gender'
        elif 'C.C.' in value:
            return 'document_type'
        else:
            return 'text'
    
    def _generate_regex_patterns(self, field: str, value: str) -> List[str]:
        """Generar patrones regex para un campo"""
        patterns = []
        
        # Patrones específicos por tipo de campo
        if 'fecha' in field.lower():
            patterns.append(r'\d{4}/\d{2}/\d{2}')
            patterns.append(r'\d{2}/\d{2}/\d{4}')
        elif 'documento' in field.lower() and 'numero' in field.lower():
            patterns.append(r'\d{8,12}')
        elif 'consultado' in field.lower():
            patterns.append(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+')
        elif 'nombre' in field.lower():
            patterns.append(r'[A-ZÁÉÍÓÚÑ\s]+')
        elif 'edad' in field.lower():
            patterns.append(r'\d+-\d+')
        
        return patterns
    
    def _update_patterns(self, sample: Dict[str, Any]):
        """Actualizar patrones aprendidos"""
        analysis = sample['analysis']
        
        for field, pattern_info in analysis['field_patterns'].items():
            if field not in self.patterns:
                self.patterns[field] = {
                    'common_patterns': [],
                    'regex_patterns': [],
                    'context_patterns': [],
                    'success_count': 0,
                    'total_count': 0
                }
            
            field_patterns = self.patterns[field]
            field_patterns['total_count'] += 1
            
            if pattern_info['value']:
                field_patterns['success_count'] += 1
                
                # Agregar patrones regex únicos
                for regex in pattern_info['regex_patterns']:
                    if regex not in field_patterns['regex_patterns']:
                        field_patterns['regex_patterns'].append(regex)
                
                # Agregar contextos únicos
                context = pattern_info['line_context']
                if context and context not in field_patterns['context_patterns']:
                    field_patterns['context_patterns'].append(context)
        
        self._save_patterns()
    
    def _update_statistics(self, sample: Dict[str, Any]):
        """Actualizar estadísticas generales"""
        self.statistics['total_samples'] = len(self.samples)
        self.statistics['last_updated'] = datetime.now().isoformat()
        
        # Estadísticas de calidad
        quality = sample['analysis']['extraction_quality']
        if 'quality_history' not in self.statistics:
            self.statistics['quality_history'] = []
        
        self.statistics['quality_history'].append({
            'sample_id': sample['id'],
            'success_rate': quality['success_rate'],
            'filled_fields': quality['filled_fields'],
            'total_fields': quality['total_fields']
        })
        
        # Mantener solo últimas 100 entradas
        if len(self.statistics['quality_history']) > 100:
            self.statistics['quality_history'] = self.statistics['quality_history'][-100:]
        
        self._save_statistics()
    
    def get_learned_patterns_for_field(self, field: str) -> Dict[str, Any]:
        """Obtener patrones aprendidos para un campo específico"""
        return self.patterns.get(field, {})
    
    def get_extraction_recommendations(self) -> Dict[str, Any]:
        """Obtener recomendaciones basadas en el aprendizaje"""
        recommendations = {
            'improved_patterns': {},
            'problematic_fields': [],
            'suggested_validations': {}
        }
        
        for field, pattern_data in self.patterns.items():
            success_rate = (pattern_data['success_count'] / pattern_data['total_count'] 
                          if pattern_data['total_count'] > 0 else 0) * 100
            
            if success_rate < 70:
                recommendations['problematic_fields'].append({
                    'field': field,
                    'success_rate': success_rate,
                    'suggestions': pattern_data['regex_patterns'][:3]  # Top 3 patterns
                })
            
            if pattern_data['regex_patterns']:
                recommendations['improved_patterns'][field] = pattern_data['regex_patterns']
        
        return recommendations
    
    def generate_memory_report(self) -> str:
        """Generar reporte de memoria del sistema"""
        total_samples = len(self.samples)
        if total_samples == 0:
            return "📊 No hay muestras en memoria aún."
        
        # Calcular estadísticas
        avg_success_rate = 0
        if self.statistics.get('quality_history'):
            rates = [entry['success_rate'] for entry in self.statistics['quality_history']]
            avg_success_rate = sum(rates) / len(rates)
        
        report = f"""
📊 REPORTE DE MEMORIA DEL SISTEMA
{'='*50}

📁 Muestras Almacenadas: {total_samples}
📈 Tasa de Éxito Promedio: {avg_success_rate:.1f}%
🧠 Patrones Aprendidos: {len(self.patterns)} campos

🎯 CAMPOS CON PATRONES:
"""
        
        for field, data in self.patterns.items():
            success_rate = (data['success_count'] / data['total_count'] * 100 
                          if data['total_count'] > 0 else 0)
            report += f"   • {field}: {success_rate:.1f}% éxito ({data['success_count']}/{data['total_count']})\n"
        
        # Recomendaciones
        recommendations = self.get_extraction_recommendations()
        if recommendations['problematic_fields']:
            report += f"\n⚠️  CAMPOS PROBLEMÁTICOS:\n"
            for prob in recommendations['problematic_fields']:
                report += f"   • {prob['field']}: {prob['success_rate']:.1f}% éxito\n"
        
        return report
    
    def _load_samples(self) -> Dict[str, Any]:
        """Cargar muestras desde archivo"""
        if self.samples_file.exists():
            try:
                with open(self.samples_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_samples(self):
        """Guardar muestras a archivo"""
        with open(self.samples_file, 'w', encoding='utf-8') as f:
            json.dump(self.samples, f, ensure_ascii=False, indent=2)
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Cargar patrones desde archivo"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_patterns(self):
        """Guardar patrones a archivo"""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)
    
    def _load_statistics(self) -> Dict[str, Any]:
        """Cargar estadísticas desde archivo"""
        if self.statistics_file.exists():
            try:
                with open(self.statistics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'total_samples': 0, 'quality_history': []}
    
    def _save_statistics(self):
        """Guardar estadísticas a archivo"""
        with open(self.statistics_file, 'w', encoding='utf-8') as f:
            json.dump(self.statistics, f, ensure_ascii=False, indent=2)