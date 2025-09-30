# -*- coding: utf-8 -*-
"""
Configuración de campos y mapeos para extracción de datos DataCrédito
"""

# Mapeo de campos por sección
FIELD_MAPPINGS = {
    'informacion_basica': {
        'consultado_por': ['Consultado por', 'consultado por'],
        'fecha_consulta': ['Fecha y Hora Consulta', 'fecha y hora consulta'],
        'tipo_documento': ['Tipo Documento', 'tipo documento'],
        'numero_documento': ['Número Documento', 'numero documento'],
        'estado_documento': ['Estado Documento', 'estado documento'],
        'lugar_expedicion': ['Lugar Expedición', 'lugar expedicion'],
        'fecha_expedicion': ['Fecha Expedición', 'fecha expedicion'],
        'nombre': ['Nombre', 'nombre'],
        'rango_edad': ['Rango Edad', 'rango edad'],
        'genero': ['Género', 'genero'],
        'antiguedad_ubicacion': ['Antiguedad Ubicación', 'antiguedad ubicacion']
    },
    
    'perfil_general': {
        'creditos_vigentes': {
            'sector_financiero': 'Créditos Vigentes - Sector Financiero',
            'sector_cooperativo': 'Créditos Vigentes - Sector Cooperativo',
            'sector_real': 'Créditos Vigentes - Sector Real',
            'sector_telcos': 'Créditos Vigentes - Sector Telcos',
            'total_sectores': 'Créditos Vigentes - Total Sectores',
            'total_principal': 'Créditos Vigentes - Total Principal',
            'total_codeudor': 'Créditos Vigentes - Total Codeudor'
        },
        'creditos_cerrados': {
            'sector_financiero': 'Créditos Cerrados - Sector Financiero',
            'sector_cooperativo': 'Créditos Cerrados - Sector Cooperativo',
            'sector_real': 'Créditos Cerrados - Sector Real',
            'sector_telcos': 'Créditos Cerrados - Sector Telcos',
            'total_sectores': 'Créditos Cerrados - Total Sectores',
            'total_principal': 'Créditos Cerrados - Total Principal',
            'total_codeudor': 'Créditos Cerrados - Total Codeudor'
        },
        'creditos_reestructurados': {
            'sector_financiero': 'Créditos Reestructurados - Sector Financiero',
            'sector_cooperativo': 'Créditos Reestructurados - Sector Cooperativo',
            'sector_real': 'Créditos Reestructurados - Sector Real',
            'sector_telcos': 'Créditos Reestructurados - Sector Telcos',
            'total_sectores': 'Créditos Reestructurados - Total Sectores',
            'total_principal': 'Créditos Reestructurados - Total Principal',
            'total_codeudor': 'Créditos Reestructurados - Total Codeudor'
        }
    }
}

# Patrones regex comunes
REGEX_PATTERNS = {
    'fecha_hora': r"(20[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\.[0-9]{2} (AM|PM))",
    'numero_documento': r"([0-9]{6,12})",
    'fechas': r"([0-9]{2}/[0-9]{2}/[0-9]{4})",
    'nombres': r"([A-ZÁÉÍÓÚÑ\s]+)",
    'numeros': r"(\d+)",
    'montos': r"(\$[\d,]+)",
    'scores': r"([0-9]{3})"
}

# Valores por defecto
DEFAULT_VALUES = {
    'numerico': '0',
    'texto': 'SIN INFO',
    'no_aplica': 'NO APLICA'
}

# Secciones disponibles
SECCIONES = [
    'informacion_basica',
    'perfil_general',
    'tendencia_endeudamiento',
    'endeudamiento_actual',
    'habito_pago',
    'evolucion_deuda',
    'demandas_judiciales',
    'historico_consultas',
    'endeudamiento_global',
    'reconocer',
    'puntaje_acierta'
]

# Configuración de Excel
EXCEL_CONFIG = {
    'formato_fecha': 'DD/MM/YYYY',
    'formato_moneda': '$#,##0',
    'colores': {
        'header_principal': '1f4e79',
        'header_secundario': '8db4e2',
        'fila_par': 'f2f2f2',
        'fila_impar': 'ffffff'
    },
    'fuentes': {
        'header': {'bold': True, 'size': 11, 'color': 'FFFFFF'},
        'subheader': {'bold': True, 'size': 10, 'color': '000000'},
        'data': {'size': 9, 'color': '000000'}
    }
}