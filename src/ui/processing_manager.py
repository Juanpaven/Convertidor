# -*- coding: utf-8 -*-
"""
Manejador de procesamiento de archivos
"""
import threading
import queue
import time
from pathlib import Path
from typing import Callable

class ProcessingManager:
    """Maneja el procesamiento de archivos PDF en background"""
    
    def __init__(self, pdf_reader, excel_processor, extractor):
        self.pdf_reader = pdf_reader
        self.excel_processor = excel_processor
        self.extractor = extractor
        self.queue = queue.Queue()
        self.procesando = False
        
    def procesar_archivos_async(self, carpeta_pdfs: str, carpeta_excel: str, 
                               callback_progress: Callable = None):
        """Iniciar procesamiento asíncrono"""
        if self.procesando:
            return False
            
        self.procesando = True
        thread = threading.Thread(
            target=self._procesar_archivos, 
            args=(carpeta_pdfs, carpeta_excel),
            daemon=True
        )
        thread.start()
        
        if callback_progress:
            self._monitorear_progreso(callback_progress)
        
        return True
    
    def _procesar_archivos(self, carpeta_pdfs: str, carpeta_excel: str):
        """Procesar archivos en thread separado"""
        try:
            carpeta_pdfs = Path(carpeta_pdfs)
            carpeta_excel = Path(carpeta_excel)
            
            # Buscar archivos PDF
            archivos_pdf = list(carpeta_pdfs.glob("*.pdf"))
            total_archivos = len(archivos_pdf)
            
            if total_archivos == 0:
                self.queue.put(('error', 'No se encontraron archivos PDF en la carpeta'))
                return
                
            self.queue.put(('log', f"📄 Procesando {total_archivos} archivos PDF"))
            
            # Procesar cada archivo
            datos_procesados = []
            exitosos = 0
            
            for i, archivo_pdf in enumerate(archivos_pdf):
                try:
                    # Actualizar progreso
                    progreso = (i / total_archivos) * 95
                    self.queue.put(('progreso', progreso))
                    self.queue.put(('status', f"📄 Procesando: {archivo_pdf.name}"))
                    self.queue.put(('log', f"🔄 ({i+1}/{total_archivos}) {archivo_pdf.name}"))
                    
                    # Procesar archivo
                    registro = self._procesar_archivo_individual(archivo_pdf)
                    datos_procesados.append(registro)
                    
                    if registro['_metadata']['procesado']:
                        exitosos += 1
                        
                except Exception as e:
                    self.queue.put(('log', f"❌ Error en {archivo_pdf.name}: {str(e)}", 'error'))
                    registro_error = self._crear_registro_error(archivo_pdf, str(e))
                    datos_procesados.append(registro_error)
            
            # Generar Excel
            self._generar_excel_final(datos_procesados, carpeta_excel, exitosos, total_archivos)
            
        except Exception as e:
            self.queue.put(('error', f"Error general: {str(e)}"))
        finally:
            self.procesando = False
    
    def _procesar_archivo_individual(self, archivo_pdf: Path):
        """Procesar un archivo PDF individual"""
        # Leer PDF
        contenido = self.pdf_reader.extraer_texto(str(archivo_pdf))
        
        if not contenido:
            raise ValueError("No se pudo extraer texto del PDF")
        
        # Extraer datos
        info_basica = self.extractor.extract(contenido, archivo_pdf.name)
        
        # Crear registro
        return {
            'informacion_basica': info_basica,
            '_metadata': {
                'archivo': archivo_pdf.name,
                'ruta': str(archivo_pdf),
                'tamaño_texto': len(contenido),
                'procesado': True
            }
        }
    
    def _crear_registro_error(self, archivo_pdf: Path, error: str):
        """Crear registro para archivo con error"""
        return {
            'informacion_basica': self.extractor.crear_registro_vacio([
                "Consultado por", "Fecha y Hora Consulta", "Tipo Documento",
                "Número Documento", "Estado Documento", "Lugar Expedición",
                "Fecha Expedición", "Nombre", "Rango Edad", "Género",
                "Antigüedad Ubicación"
            ]),
            '_metadata': {
                'archivo': archivo_pdf.name,
                'ruta': str(archivo_pdf),
                'procesado': False,
                'error': error
            }
        }
    
    def _generar_excel_final(self, datos_procesados, carpeta_excel, exitosos, total):
        """Generar archivo Excel final"""
        self.queue.put(('progreso', 95))
        self.queue.put(('status', '📊 Generando archivo Excel...'))
        self.queue.put(('log', '📊 Generando archivo Excel...'))
        
        timestamp = int(time.time())
        archivo_salida = carpeta_excel / f"DataCredito_{timestamp}.xlsx"
        
        self.excel_processor.generar_excel(datos_procesados, str(archivo_salida))
        
        # Completado
        errores = total - exitosos
        
        self.queue.put(('progreso', 100))
        self.queue.put(('status', f'✅ Completado: {exitosos} exitosos, {errores} errores'))
        self.queue.put(('log', f'✅ Procesamiento completado'))
        self.queue.put(('log', f'📊 Exitosos: {exitosos} | Errores: {errores}', 'success'))
        self.queue.put(('log', f'💾 Archivo: {archivo_salida.name}', 'success'))
        self.queue.put(('completado', str(archivo_salida)))
    
    def _monitorear_progreso(self, callback):
        """Monitorear progreso y ejecutar callback"""
        def monitor():
            while self.procesando:
                try:
                    while True:
                        try:
                            mensaje = self.queue.get_nowait()
                            callback(mensaje)
                        except queue.Empty:
                            break
                except:
                    break
                time.sleep(0.1)
        
        threading.Thread(target=monitor, daemon=True).start()