# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO COMPLETO - Analizar contenido real de PDFs DataCrédito
Para entender exactamente qué información contienen y cómo extraerla
"""
import sys
from pathlib import Path
import pdfplumber
import re

def analizar_pdf_completo(ruta_pdf):
    """Analiza completamente un PDF y muestra su estructura"""
    print(f"\n{'='*80}")
    print(f"ANALIZANDO: {Path(ruta_pdf).name}")
    print(f"{'='*80}")
    
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            print(f"📄 Total de páginas: {len(pdf.pages)}")
            
            texto_completo = ""
            
            for i, page in enumerate(pdf.pages):
                print(f"\n--- PÁGINA {i+1} ---")
                
                # Extraer texto
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina + "\n"
                    
                    # Mostrar primeras líneas de la página
                    lineas = texto_pagina.split('\n')[:10]
                    print("📝 Primeras 10 líneas:")
                    for j, linea in enumerate(lineas, 1):
                        if linea.strip():
                            print(f"   {j:2d}: {linea.strip()}")
                
                # Analizar tablas
                tablas = page.extract_tables()
                print(f"📊 Tablas encontradas: {len(tablas)}")
                
                for t, tabla in enumerate(tablas):
                    print(f"   Tabla {t+1}: {len(tabla)} filas")
                    if tabla and len(tabla) > 0:
                        print(f"   Primera fila: {tabla[0]}")
            
            print(f"\n{'='*80}")
            print("ANÁLISIS DE CONTENIDO COMPLETO")
            print(f"{'='*80}")
            
            # Buscar patrones específicos
            patrones_importantes = {
                'Consultado por': r'Consultado por[:\s]*([^\n]+)',
                'Fecha y Hora': r'Fecha y Hora[:\s]*([^\n]+)',
                'Nombre': r'Nombre[:\s]*([^\n]+)',
                'Documento': r'(?:Número Documento|C\.C\.)[:\s]*([^\n]+)',
                'Score': r'(?:Score|Puntaje)[:\s]*([^\n]+)',
                'Saldo': r'(?:Saldo|Valor)[:\s]*([^\n]+)',
                'Obligaciones': r'(?:Obligacion|Credito|Tarjeta)[:\s]*([^\n]+)',
                'Direccion': r'(?:Dirección|Residencia)[:\s]*([^\n]+)',
                'Telefono': r'(?:Teléfono|Tel)[:\s]*([^\n]+)',
                'Email': r'(?:Email|Correo)[:\s]*([^\n]+)',
            }
            
            print("\n🔍 PATRONES ENCONTRADOS:")
            for nombre, patron in patrones_importantes.items():
                matches = re.findall(patron, texto_completo, re.IGNORECASE)
                if matches:
                    print(f"✅ {nombre}: {len(matches)} coincidencias")
                    for match in matches[:3]:  # Mostrar primeras 3
                        print(f"    → {match.strip()}")
                else:
                    print(f"❌ {nombre}: No encontrado")
            
            # Mostrar estructura general
            print(f"\n📋 ESTRUCTURA DEL TEXTO:")
            lineas_importantes = []
            for linea in texto_completo.split('\n'):
                linea = linea.strip()
                if linea and ':' in linea and len(linea) < 100:
                    lineas_importantes.append(linea)
            
            print(f"💼 Líneas con estructura 'Campo: Valor' encontradas: {len(lineas_importantes)}")
            for linea in lineas_importantes[:20]:  # Mostrar primeras 20
                print(f"    → {linea}")
            
            # Guardar texto completo para análisis
            archivo_texto = Path(ruta_pdf).with_suffix('.txt')
            with open(archivo_texto, 'w', encoding='utf-8') as f:
                f.write(texto_completo)
            print(f"\n💾 Texto completo guardado en: {archivo_texto}")
            
            return texto_completo
            
    except Exception as e:
        print(f"❌ Error analizando {ruta_pdf}: {e}")
        return None

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DE PDFs DataCrédito")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Analizar PDF específico
        ruta_pdf = sys.argv[1]
        if Path(ruta_pdf).exists():
            analizar_pdf_completo(ruta_pdf)
        else:
            print(f"❌ Archivo no encontrado: {ruta_pdf}")
    else:
        # Buscar PDFs en el directorio actual
        pdfs = list(Path('.').glob('*.pdf'))
        if pdfs:
            print(f"📄 Encontrados {len(pdfs)} PDFs para analizar:")
            for pdf in pdfs:
                print(f"   → {pdf.name}")
            
            # Analizar el primero
            print(f"\n🔍 Analizando el primer PDF: {pdfs[0].name}")
            analizar_pdf_completo(pdfs[0])
        else:
            print("❌ No se encontraron archivos PDF")
            print("\n💡 USO:")
            print("   python diagnostico_completo.py archivo.pdf")
            print("   O coloca PDFs en este directorio")

if __name__ == "__main__":
    main()