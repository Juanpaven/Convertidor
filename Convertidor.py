# -*- coding: utf-8 -*-
"""
DataCrédito PDF Converter v2.1 - Versión Unificada
Sistema modular con interfaz gráfica optimizada
Combina lo mejor de las versiones completa y lite
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import queue
import time
import os

# Configurar paths de importación
import setup_paths

# Importar sistema modular
from extractors.info_basica import InformacionBasicaExtractor
from extractors.extractor_completo import ExtractorCompleto
from extractor_independiente import ExtractorIndependiente
from processors.excel_processor import ExcelProcessor
from excel_processor_simple import ExcelProcessorSimple
from utils.pdf_reader import PDFReader
from ui.processing_manager import ProcessingManager

class ConvertidorDataCredito:
    """Convertidor unificado de PDFs DataCrédito a Excel - Versión 2.1"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.setup_processors()
        
        # Control de procesamiento
        self.queue = queue.Queue()
        self.procesando = False
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("DataCrédito PDF Converter v2.1 - Unificado")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Icono de la ventana (si existe)
        try:
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450)
        y = (self.root.winfo_screenheight() // 2) - (350)
        self.root.geometry(f"900x700+{x}+{y}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_variables(self):
        """Configurar variables de la interfaz"""
        self.carpeta_pdfs = tk.StringVar()
        self.carpeta_excel = tk.StringVar()
        self.progreso = tk.DoubleVar()
        self.status = tk.StringVar(value="✅ Listo para procesar")
        
    def setup_widgets(self):
        """Configurar widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="DataCrédito PDF Converter v2.1", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Versión Unificada - Sistema Modular Optimizado", 
                                  font=("Segoe UI", 10))
        subtitle_label.pack()
        
        # Separador
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=(0, 20))
        
        # Frame de selección de carpetas
        self.setup_folder_selection(main_frame)
        
        # Separador
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=(20, 20))
        
        # Frame de progreso y control
        self.setup_progress_control(main_frame)
        
        # Separador
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=(20, 20))
        
        # Frame de información y resultados
        self.setup_info_results(main_frame)
        
    def setup_folder_selection(self, parent):
        """Configurar sección de selección de carpetas"""
        folder_frame = ttk.LabelFrame(parent, text="📁 Configuración de Carpetas", padding=15)
        folder_frame.pack(fill="x", pady=(0, 10))
        
        # Carpeta de PDFs
        pdfs_frame = ttk.Frame(folder_frame)
        pdfs_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(pdfs_frame, text="📄 Carpeta de PDFs:", width=20).pack(side="left")
        
        pdf_entry_frame = ttk.Frame(pdfs_frame)
        pdf_entry_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        self.pdf_entry = ttk.Entry(pdf_entry_frame, textvariable=self.carpeta_pdfs, 
                                  font=("Consolas", 10))
        self.pdf_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(pdf_entry_frame, text="Buscar", 
                  command=self.seleccionar_carpeta_pdfs, width=10).pack(side="right", padx=(5, 0))
        
        # Carpeta de Excel
        excel_frame = ttk.Frame(folder_frame)
        excel_frame.pack(fill="x")
        
        ttk.Label(excel_frame, text="📊 Carpeta de Excel:", width=20).pack(side="left")
        
        excel_entry_frame = ttk.Frame(excel_frame)
        excel_entry_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        self.excel_entry = ttk.Entry(excel_entry_frame, textvariable=self.carpeta_excel,
                                    font=("Consolas", 10))
        self.excel_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(excel_entry_frame, text="Buscar", 
                  command=self.seleccionar_carpeta_excel, width=10).pack(side="right", padx=(5, 0))
    
    def setup_progress_control(self, parent):
        """Configurar sección de progreso y control"""
        control_frame = ttk.LabelFrame(parent, text="⚙️ Control de Procesamiento", padding=15)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Botones de control
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_procesar = ttk.Button(button_frame, text="🚀 Procesar PDFs", 
                                      command=self.procesar_pdfs, style="Accent.TButton")
        self.btn_procesar.pack(side="left", padx=(0, 10))
        
        self.btn_abrir_excel = ttk.Button(button_frame, text="📊 Abrir Carpeta Excel", 
                                         command=self.abrir_carpeta_excel)
        self.btn_abrir_excel.pack(side="left", padx=(0, 10))
        
        self.btn_limpiar = ttk.Button(button_frame, text="🧹 Limpiar", 
                                     command=self.limpiar_interfaz)
        self.btn_limpiar.pack(side="left")
        
        # Barra de progreso
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(progress_frame, text="Progreso:").pack(side="left")
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progreso, 
                                           mode="determinate", length=400)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(10, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="0%", width=8)
        self.progress_label.pack(side="right")
        
        # Estado
        self.status_label = ttk.Label(control_frame, textvariable=self.status, 
                                     font=("Segoe UI", 10, "bold"))
        self.status_label.pack(fill="x")
        
    def setup_info_results(self, parent):
        """Configurar sección de información y resultados"""
        info_frame = ttk.LabelFrame(parent, text="📋 Información y Resultados", padding=15)
        info_frame.pack(fill="both", expand=True)
        
        # Área de texto con scroll
        text_frame = ttk.Frame(info_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.info_text = tk.Text(text_frame, height=15, wrap="word", 
                                font=("Consolas", 10), bg="#f8f9fa", fg="#212529")
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mensaje inicial
        self.mostrar_info_inicial()
        
    def setup_processors(self):
        """Configurar procesadores del sistema modular"""
        try:
            # Inicializar componentes MEJORADOS para extraer TODA la información
            self.pdf_reader = PDFReader()
            self.excel_processor = ExcelProcessorSimple()  # Procesador simple y robusto
            self.extractor = ExtractorIndependiente()  # Extractor independiente robusto
            
            # Configurar ProcessingManager con componentes completos
            self.processing_manager = ProcessingManager(self.pdf_reader, self.excel_processor, self.extractor)
            
            self.agregar_info("✅ Sistema MEJORADO inicializado correctamente")
            self.agregar_info("✅ Extractor con patrones FLEXIBLES configurado")
            self.agregar_info("✅ Procesador Excel para tabla única completa")
            self.agregar_info("✅ Diseñado para extraer información incluso con variaciones de formato")
            
        except Exception as e:
            self.agregar_info(f"❌ Error al inicializar sistema completo: {e}")
            messagebox.showerror("Error", f"Error al inicializar sistema completo: {e}")
    
    def mostrar_info_inicial(self):
        """Mostrar información inicial en el área de texto"""
        info_inicial = """
🎯 DataCrédito PDF Converter v2.1 - EXTRACTOR COMPLETO
========================================================

✨ CARACTERÍSTICAS AVANZADAS:
   • Sistema completo de extracción de TODA la información
   • Tabla única de Excel con más de 90 campos de datos
   • Procesamiento integral de reportes DataCrédito
   • Captura ABSOLUTAMENTE TODA la información disponible
   • Análisis completo: personal, crediticio, judicial, comercial

📋 INSTRUCCIONES DE USO:
   1. Selecciona la carpeta que contiene los PDFs de DataCrédito
   2. Selecciona la carpeta donde guardar los archivos Excel
   3. Haz clic en '🚀 Procesar PDFs' para iniciar la conversión
   4. El progreso se mostrará en tiempo real

🔍 EXTRACTOR COMPLETO INCLUYE:
   • Información personal y demográfica completa
   • Historial crediticio detallado
   • Obligaciones financieras de todo tipo
   • Información judicial y legal
   • Datos comerciales y económicos
   • Historial de consultas y referencias
   • Scores y calificaciones crediticias
   • Alertas y observaciones especiales

🎉 ¡Extrae TODA la información de tus PDFs DataCrédito!
        """
        self.info_text.insert("1.0", info_inicial.strip())
        self.info_text.config(state="disabled")
    
    def seleccionar_carpeta_pdfs(self):
        """Seleccionar carpeta de PDFs"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de PDFs")
        if carpeta:
            self.carpeta_pdfs.set(carpeta)
            self.agregar_info(f"📁 Carpeta PDFs seleccionada: {carpeta}")
            
            # Contar PDFs
            try:
                pdf_files = list(Path(carpeta).glob("*.pdf"))
                self.agregar_info(f"📄 Encontrados {len(pdf_files)} archivos PDF")
            except Exception as e:
                self.agregar_info(f"⚠️ Error al contar PDFs: {e}")
                
    def seleccionar_carpeta_excel(self):
        """Seleccionar carpeta de Excel"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta para Excel")
        if carpeta:
            self.carpeta_excel.set(carpeta)
            self.agregar_info(f"📊 Carpeta Excel seleccionada: {carpeta}")
    
    def procesar_pdfs(self):
        """Procesar PDFs usando el sistema unificado"""
        if self.procesando:
            messagebox.showwarning("Procesando", "Ya hay un procesamiento en curso...")
            return
            
        # Validar carpetas
        carpeta_pdfs = self.carpeta_pdfs.get().strip()
        carpeta_excel = self.carpeta_excel.get().strip()
        
        if not carpeta_pdfs or not carpeta_excel:
            messagebox.showerror("Error", "Debes seleccionar ambas carpetas")
            return
            
        if not Path(carpeta_pdfs).exists():
            messagebox.showerror("Error", "La carpeta de PDFs no existe")
            return
            
        if not Path(carpeta_excel).exists():
            messagebox.showerror("Error", "La carpeta de Excel no existe")
            return
        
        # Iniciar procesamiento en hilo separado
        self.procesando = True
        self.btn_procesar.config(state="disabled", text="🔄 Procesando...")
        self.status.set("🔄 Procesando PDFs...")
        
        # Limpiar área de información
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.config(state="disabled")
        
        # Iniciar hilo de procesamiento
        thread = threading.Thread(target=self._procesar_en_hilo, 
                                 args=(carpeta_pdfs, carpeta_excel), 
                                 daemon=True)
        thread.start()
        
        # Iniciar monitoreo de progreso
        self.root.after(100, self.actualizar_progreso)
    
    def _procesar_en_hilo(self, carpeta_pdfs, carpeta_excel):
        """Procesar PDFs directamente sin ProcessingManager para evitar conflictos"""
        try:
            carpeta_pdfs_path = Path(carpeta_pdfs)
            carpeta_excel_path = Path(carpeta_excel)
            
            # Buscar archivos PDF
            archivos_pdf = list(carpeta_pdfs_path.glob("*.pdf"))
            total_archivos = len(archivos_pdf)
            
            if total_archivos == 0:
                self.queue.put(("error", "No se encontraron archivos PDF en la carpeta"))
                return
                
            self.queue.put(("mensaje", f"📄 Encontrados {total_archivos} archivos PDF"))
            
            # Procesar cada archivo
            datos_procesados = []
            exitosos = 0
            
            for i, archivo_pdf in enumerate(archivos_pdf):
                try:
                    # Actualizar progreso
                    progreso = (i / total_archivos) * 90
                    self.queue.put(("progreso", (progreso, f"Procesando: {archivo_pdf.name}")))
                    self.queue.put(("mensaje", f"🔄 ({i+1}/{total_archivos}) {archivo_pdf.name}"))
                    
                    # Leer y extraer PDF con extractor COMPLETO
                    texto = self.pdf_reader.extraer_texto(str(archivo_pdf))
                    datos = self.extractor.extract(texto, str(archivo_pdf))
                    
                    # Agregar metadatos
                    datos['_metadata'] = {
                        'archivo': archivo_pdf.name,
                        'procesado': True,
                        'fecha_procesamiento': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    datos_procesados.append(datos)
                    exitosos += 1
                    
                    self.queue.put(("mensaje", f"✅ {archivo_pdf.name} procesado correctamente"))
                    
                except Exception as e:
                    error_msg = f"❌ Error en {archivo_pdf.name}: {str(e)}"
                    self.queue.put(("mensaje", error_msg))
                    
                    # Registro de error
                    registro_error = {
                        '_metadata': {
                            'archivo': archivo_pdf.name, 
                            'procesado': False,
                            'error': str(e),
                            'fecha_procesamiento': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    }
                    datos_procesados.append(registro_error)
            
            # Generar Excel final
            self.queue.put(("progreso", (95, "Generando archivo Excel...")))
            self.queue.put(("mensaje", "📊 Generando archivo Excel final..."))
            
            # Generar nombre de archivo con timestamp
            timestamp = int(time.time())
            archivo_salida = carpeta_excel_path / f"DataCredito_{timestamp}.xlsx"
            
            self.excel_processor.generar_excel(
                datos_procesados, str(archivo_salida)
            )
            archivo_excel = str(archivo_salida)
            
            # Resultado final
            resultado = {
                "procesados": total_archivos,
                "exitosos": exitosos,
                "errores": total_archivos - exitosos,
                "archivo_excel": str(archivo_excel) if archivo_excel else "Excel generado"
            }
            
            self.queue.put(("progreso", (100, "Completado")))
            self.queue.put(("final", resultado))
            
        except Exception as e:
            self.queue.put(("error", f"Error en procesamiento: {e}"))
        finally:
            self.queue.put(("terminar", None))
    
    def _callback_progreso(self, porcentaje, mensaje=""):
        """Callback para actualizar progreso desde ProcessingManager"""
        self.queue.put(("progreso", (porcentaje, mensaje)))
    
    def _callback_mensaje(self, mensaje):
        """Callback para mensajes desde ProcessingManager"""
        self.queue.put(("mensaje", mensaje))
    
    def actualizar_progreso(self):
        """Actualizar progreso y mensajes desde la cola"""
        try:
            while True:
                tipo, datos = self.queue.get_nowait()
                
                if tipo == "progreso":
                    porcentaje, mensaje = datos
                    self.progreso.set(porcentaje)
                    self.progress_label.config(text=f"{porcentaje:.1f}%")
                    if mensaje:
                        self.status.set(mensaje)
                        
                elif tipo == "mensaje":
                    self.agregar_info(datos)
                    
                elif tipo == "final":
                    self._finalizar_procesamiento(datos)
                    return
                    
                elif tipo == "error":
                    self._manejar_error(datos)
                    return
                    
                elif tipo == "terminar":
                    self._terminar_procesamiento()
                    return
                    
        except queue.Empty:
            pass
        
        # Continuar monitoreando si aún está procesando
        if self.procesando:
            self.root.after(100, self.actualizar_progreso)
    
    def _finalizar_procesamiento(self, resultado):
        """Finalizar procesamiento exitoso"""
        self.agregar_info("\n" + "="*50)
        self.agregar_info("✅ PROCESAMIENTO COMPLETADO")
        self.agregar_info("="*50)
        
        if resultado:
            self.agregar_info(f"📊 Archivos procesados: {resultado.get('procesados', 0)}")
            self.agregar_info(f"✅ Exitosos: {resultado.get('exitosos', 0)}")
            self.agregar_info(f"❌ Errores: {resultado.get('errores', 0)}")
            
            if resultado.get('archivo_excel'):
                self.agregar_info(f"📄 Excel generado: {resultado['archivo_excel']}")
        
        self.status.set("✅ Procesamiento completado")
        messagebox.showinfo("Completado", "¡Procesamiento completado exitosamente!")
        self._terminar_procesamiento()
    
    def _manejar_error(self, error):
        """Manejar error en procesamiento"""
        self.agregar_info(f"\n❌ ERROR: {error}")
        self.status.set("❌ Error en procesamiento")
        messagebox.showerror("Error", f"Error durante el procesamiento:\n{error}")
        self._terminar_procesamiento()
    
    def _terminar_procesamiento(self):
        """Terminar procesamiento y restaurar interfaz"""
        self.procesando = False
        self.btn_procesar.config(state="normal", text="🚀 Procesar PDFs")
        
        if self.progreso.get() < 100:
            self.progreso.set(0)
            self.progress_label.config(text="0%")
    
    def agregar_info(self, mensaje):
        """Agregar información al área de texto"""
        self.info_text.config(state="normal")
        self.info_text.insert("end", f"{mensaje}\n")
        self.info_text.see("end")
        self.info_text.config(state="disabled")
        self.root.update_idletasks()
    
    def abrir_carpeta_excel(self):
        """Abrir carpeta de Excel en el explorador"""
        carpeta = self.carpeta_excel.get().strip()
        if carpeta and Path(carpeta).exists():
            os.startfile(carpeta)
            self.agregar_info(f"📂 Abriendo carpeta: {carpeta}")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una carpeta de Excel válida")
    
    def limpiar_interfaz(self):
        """Limpiar la interfaz"""
        if self.procesando:
            messagebox.showwarning("Procesando", "No se puede limpiar durante el procesamiento")
            return
            
        self.carpeta_pdfs.set("")
        self.carpeta_excel.set("")
        self.progreso.set(0)
        self.progress_label.config(text="0%")
        self.status.set("✅ Listo para procesar")
        
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.config(state="disabled")
        
        self.mostrar_info_inicial()
        self.agregar_info("🧹 Interfaz limpiada")
    
    def on_closing(self):
        """Manejar cierre de ventana"""
        if self.procesando:
            if messagebox.askokcancel("Salir", "Hay un procesamiento en curso. ¿Deseas salir?"):
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Ejecutar la aplicación"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()

def main():
    """Función principal"""
    try:
        app = ConvertidorDataCredito()
        app.run()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{e}")

if __name__ == "__main__":
    main()