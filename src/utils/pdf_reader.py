# -*- coding: utf-8 -*-
"""
Utilidades para lectura de archivos PDF
"""
import pdfplumber
from pathlib import Path
from typing import Optional

class PDFReader:
    """Lector de archivos PDF optimizado"""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def extraer_texto(self, ruta_pdf: str) -> Optional[str]:
        """
        Extrae todo el texto de un PDF
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            
        Returns:
            Texto extraído o None si hay error
        """
        try:
            ruta = Path(ruta_pdf)
            
            if not ruta.exists():
                raise FileNotFoundError(f"El archivo {ruta_pdf} no existe")
            
            if not ruta.suffix.lower() == '.pdf':
                raise ValueError(f"El archivo {ruta_pdf} no es un PDF")
            
            texto_completo = ""
            
            with pdfplumber.open(ruta_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + "\n"
            
            return texto_completo.strip() if texto_completo else None
            
        except Exception as e:
            print(f"Error leyendo PDF {ruta_pdf}: {e}")
            return None
    
    def extraer_texto_pagina(self, ruta_pdf: str, numero_pagina: int) -> Optional[str]:
        """
        Extrae texto de una página específica
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            numero_pagina: Número de página (base 0)
            
        Returns:
            Texto de la página o None si hay error
        """
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                if numero_pagina < len(pdf.pages):
                    return pdf.pages[numero_pagina].extract_text()
                else:
                    raise IndexError(f"La página {numero_pagina} no existe")
                    
        except Exception as e:
            print(f"Error leyendo página {numero_pagina} del PDF {ruta_pdf}: {e}")
            return None
    
    def obtener_info_pdf(self, ruta_pdf: str) -> dict:
        """
        Obtiene información básica del PDF
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            
        Returns:
            Dict con información del PDF
        """
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                return {
                    'numero_paginas': len(pdf.pages),
                    'metadata': pdf.metadata,
                    'archivo': Path(ruta_pdf).name,
                    'tamaño': Path(ruta_pdf).stat().st_size
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'archivo': Path(ruta_pdf).name
            }