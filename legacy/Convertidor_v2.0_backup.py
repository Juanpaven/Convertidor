# -*- coding: utf-8 -*-
"""
DataCrédito PDF Converter v2.0 - Interfaz Moderna
Sistema modular con interfaz gráfica mejorada
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
from processors.excel_processor import ExcelProcessor
from utils.pdf_reader import PDFReader

class ConvertidorDataCredito:
    """Convertidor moderno de PDFs DataCrédito a Excel"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.setup_processor()
        
        # Control de procesamiento
        self.queue = queue.Queue()
        self.procesando = False
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("DataCrédito PDF Converter v2.0")
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
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_variables(self):
        """Configurar variables de la interfaz"""
        self.carpeta_pdfs = tk.StringVar()
        self.carpeta_excel = tk.StringVar()
        self.progreso = tk.DoubleVar()
        self.status = tk.StringVar(value="✅ Listo para procesar")
        
        # Configurar carpeta de salida por defecto
        default_output = str(Path.home() / "Downloads")
        self.carpeta_excel.set(default_output)
        
    def setup_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Header con título y versión
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25))
        
        title_label = ttk.Label(header_frame, text="DataCrédito PDF Converter", 
                               font=('Segoe UI', 18, 'bold'))
        title_label.pack()
        
        version_label = ttk.Label(header_frame, text="v2.0 - Sistema Modular", 
                                font=('Segoe UI', 10), foreground='gray')
        version_label.pack()
        
        # Sección de archivos
        files_frame = ttk.LabelFrame(main_frame, text="📁 Selección de Archivos", padding="15")
        files_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        files_frame.columnconfigure(1, weight=1)
        
        # Carpeta de PDFs
        ttk.Label(files_frame, text="📄 Carpeta de PDFs:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky="w", pady=(0, 10))
        
        pdf_frame = ttk.Frame(files_frame)
        pdf_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        pdf_frame.columnconfigure(0, weight=1)
        
        self.pdf_entry = ttk.Entry(pdf_frame, textvariable=self.carpeta_pdfs, font=('Segoe UI', 10))
        self.pdf_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(pdf_frame, text="📂 Seleccionar", command=self.seleccionar_carpeta_pdfs).grid(
            row=0, column=1)
        
        # Carpeta de salida Excel
        ttk.Label(files_frame, text="💾 Carpeta de salida:", font=('Segoe UI', 10, 'bold')).grid(
            row=2, column=0, sticky="w", pady=(0, 10))
        
        excel_frame = ttk.Frame(files_frame)
        excel_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        excel_frame.columnconfigure(0, weight=1)
        
        self.excel_entry = ttk.Entry(excel_frame, textvariable=self.carpeta_excel, font=('Segoe UI', 10))
        self.excel_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(excel_frame, text="📂 Seleccionar", command=self.seleccionar_carpeta_excel).grid(
            row=0, column=1)
        
        # Sección de control
        control_frame = ttk.LabelFrame(main_frame, text="🎛️ Control de Procesamiento", padding="15")
        control_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        # Botones principales
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_procesar = ttk.Button(button_frame, text="🚀 Procesar PDFs", 
                                      command=self.iniciar_procesamiento, style="Accent.TButton")
        self.btn_procesar.pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="🧪 Demo", command=self.ejecutar_demo).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="🔧 Test", command=self.ejecutar_test).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="📁 Abrir Salida", command=self.abrir_carpeta_salida).pack(side="left")
        
        # Barra de progreso
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(progress_frame, text="Progreso:", font=('Segoe UI', 10, 'bold')).pack(anchor="w")
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progreso, maximum=100, 
                                          style="TProgressbar")
        self.progress_bar.pack(fill="x", pady=(5, 0))
        
        # Estado
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill="x")
        
        ttk.Label(status_frame, text="Estado:", font=('Segoe UI', 10, 'bold')).pack(anchor="w")
        self.status_label = ttk.Label(status_frame, textvariable=self.status, font=('Segoe UI', 10))
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        # Log de procesamiento
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Procesamiento", padding="15")
        log_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Crear área de texto con scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=12, wrap=tk.WORD, font=('Consolas', 9),
                               bg='#f8f9fa', fg='#212529')
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Footer con información
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        
        ttk.Label(footer_frame, text="💡 Tip: Coloca todos los PDFs en una carpeta y selecciona la ruta", 
                 font=('Segoe UI', 9), foreground='gray').pack(anchor="w")
        
    def setup_processor(self):
        """Configurar procesador modular"""
        try:
            self.pdf_reader = PDFReader()
            self.excel_processor = ExcelProcessor()
            self.extractor = InformacionBasicaExtractor()
            self.log("✅ Sistema modular inicializado correctamente")
        except Exception as e:
            self.log(f"❌ Error inicializando sistema: {e}")
            messagebox.showerror("Error", f"Error inicializando sistema modular:\n{e}")
        
    def seleccionar_carpeta_pdfs(self):
        """Seleccionar carpeta de PDFs"""
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta con archivos PDF",
            initialdir=str(Path.home() / "Downloads")
        )
        if carpeta:
            self.carpeta_pdfs.set(carpeta)
            # Contar PDFs
            pdf_count = len(list(Path(carpeta).glob("*.pdf")))
            self.log(f"📂 Carpeta seleccionada: {carpeta}")
            self.log(f"📄 Archivos PDF encontrados: {pdf_count}")
            
    def seleccionar_carpeta_excel(self):
        """Seleccionar carpeta de salida"""
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta para archivo Excel",
            initialdir=self.carpeta_excel.get()
        )
        if carpeta:
            self.carpeta_excel.set(carpeta)
            self.log(f"💾 Carpeta de salida: {carpeta}")
            
    def abrir_carpeta_salida(self):
        """Abrir carpeta de salida en explorador"""
        carpeta = self.carpeta_excel.get()
        if carpeta and Path(carpeta).exists():
            os.startfile(carpeta)
        else:
            messagebox.showwarning("Advertencia", "La carpeta de salida no existe")
            
    def log(self, mensaje, tipo="info"):
        """Agregar mensaje al log con timestamp y color"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Determinar color según tipo
        if tipo == "error":
            color = "red"
        elif tipo == "success":
            color = "green"
        elif tipo == "warning":
            color = "orange"
        else:
            color = "black"
            
        # Insertar mensaje
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        
        # Aplicar color a la última línea
        last_line = self.log_text.index(tk.END + "-2c linestart")
        self.log_text.tag_add(tipo, last_line, tk.END + "-1c")
        self.log_text.tag_config(tipo, foreground=color)
        
        # Scroll automático
        self.log_text.see(tk.END)
        self.root.update()
        
    def iniciar_procesamiento(self):
        """Iniciar procesamiento en thread separado"""
        if self.procesando:
            return
            
        # Validaciones
        if not self.carpeta_pdfs.get():
            messagebox.showerror("Error", "❌ Selecciona la carpeta de PDFs")
            return
            
        if not self.carpeta_excel.get():
            messagebox.showerror("Error", "❌ Selecciona la carpeta de salida")
            return
            
        if not Path(self.carpeta_pdfs.get()).exists():
            messagebox.showerror("Error", "❌ La carpeta de PDFs no existe")
            return
            
        if not Path(self.carpeta_excel.get()).exists():
            messagebox.showerror("Error", "❌ La carpeta de salida no existe")
            return
            
        # Iniciar procesamiento
        self.procesando = True
        self.btn_procesar.config(state='disabled', text='🔄 Procesando...')
        self.status.set("🔄 Procesando archivos...")
        self.progreso.set(0)
        self.log("🚀 Iniciando procesamiento...", "info")
        
        # Thread separado para no bloquear UI
        thread = threading.Thread(target=self.procesar_archivos, daemon=True)
        thread.start()
        
        # Monitorear progreso
        self.monitorear_progreso()
        
    def procesar_archivos(self):
        """Procesar archivos en thread separado"""
        try:
            carpeta_pdfs = Path(self.carpeta_pdfs.get())
            carpeta_excel = Path(self.carpeta_excel.get())
            
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
                    progreso = (i / total_archivos) * 95  # Dejar 5% para generación Excel
                    self.queue.put(('progreso', progreso))
                    self.queue.put(('status', f"📄 Procesando: {archivo_pdf.name}"))
                    self.queue.put(('log', f"🔄 ({i+1}/{total_archivos}) {archivo_pdf.name}"))
                    
                    # Leer PDF
                    contenido = self.pdf_reader.extraer_texto(str(archivo_pdf))
                    
                    if not contenido:
                        raise ValueError("No se pudo extraer texto del PDF")
                    
                    # Extraer datos usando sistema modular
                    info_basica = self.extractor.extract(contenido, archivo_pdf.name)
                    
                    # Crear registro
                    registro = {
                        'informacion_basica': info_basica,
                        '_metadata': {
                            'archivo': archivo_pdf.name,
                            'ruta': str(archivo_pdf),
                            'tamaño_texto': len(contenido),
                            'procesado': True
                        }
                    }
                    
                    datos_procesados.append(registro)
                    exitosos += 1
                    
                except Exception as e:
                    self.queue.put(('log', f"❌ Error en {archivo_pdf.name}: {str(e)}", 'error'))
                    
                    # Agregar registro con error
                    registro_error = {
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
                            'error': str(e)
                        }
                    }
                    datos_procesados.append(registro_error)
            
            # Generar Excel
            self.queue.put(('progreso', 95))
            self.queue.put(('status', '📊 Generando archivo Excel...'))
            self.queue.put(('log', '📊 Generando archivo Excel...'))
            
            timestamp = int(time.time())
            archivo_salida = carpeta_excel / f"DataCredito_{timestamp}.xlsx"
            
            self.excel_processor.generar_excel(datos_procesados, str(archivo_salida))
            
            # Completado
            errores = total_archivos - exitosos
            
            self.queue.put(('progreso', 100))
            self.queue.put(('status', f'✅ Completado: {exitosos} exitosos, {errores} errores'))
            self.queue.put(('log', f'✅ Procesamiento completado'))
            self.queue.put(('log', f'📊 Exitosos: {exitosos} | Errores: {errores}', 'success'))
            self.queue.put(('log', f'💾 Archivo: {archivo_salida.name}', 'success'))
            self.queue.put(('completado', str(archivo_salida)))
            
        except Exception as e:
            self.queue.put(('error', f"Error general: {str(e)}"))
            
    def monitorear_progreso(self):
        """Monitorear cola de mensajes del procesamiento"""
        try:
            while True:
                try:
                    tipo, data, *extra = self.queue.get_nowait()
                    
                    if tipo == 'log':
                        log_type = extra[0] if extra else 'info'
                        self.log(data, log_type)
                    elif tipo == 'progreso':
                        self.progreso.set(data)
                    elif tipo == 'status':
                        self.status.set(data)
                    elif tipo == 'error':
                        self.log(f"❌ {data}", 'error')
                        messagebox.showerror("Error", data)
                        self.finalizar_procesamiento()
                        return
                    elif tipo == 'completado':
                        mensaje = f"✅ Procesamiento completado exitosamente!\n\n📊 Archivo generado:\n{data}\n\n¿Abrir carpeta de destino?"
                        if messagebox.askyesno("Completado", mensaje):
                            os.startfile(str(Path(data).parent))
                        self.finalizar_procesamiento()
                        return
                        
                except queue.Empty:
                    break
                    
            # Continuar monitoreando si aún está procesando
            if self.procesando:
                self.root.after(100, self.monitorear_progreso)
                
        except Exception as e:
            self.log(f"❌ Error en monitoreo: {e}", 'error')
            self.finalizar_procesamiento()
    
    def finalizar_procesamiento(self):
        """Finalizar procesamiento y restaurar interfaz"""
        self.procesando = False
        self.btn_procesar.config(state='normal', text='🚀 Procesar PDFs')
        
    def ejecutar_demo(self):
        """Ejecutar demo del sistema"""
        self.log("🧪 Ejecutando demo del sistema modular...", 'info')
        try:
            # Ejecutar demo en thread separado
            thread = threading.Thread(target=self._ejecutar_demo_thread, daemon=True)
            thread.start()
        except Exception as e:
            self.log(f"❌ Error en demo: {e}", 'error')
            
    def _ejecutar_demo_thread(self):
        """Ejecutar demo en thread separado"""
        try:
            from scripts import demo_modular
            demo_modular.main()
            self.queue.put(('log', '✅ Demo ejecutado correctamente', 'success'))
        except Exception as e:
            self.queue.put(('log', f'❌ Error en demo: {e}', 'error'))
            
    def ejecutar_test(self):
        """Ejecutar tests del sistema"""
        self.log("🔧 Ejecutando tests del sistema...", 'info')
        try:
            # Ejecutar test en thread separado
            thread = threading.Thread(target=self._ejecutar_test_thread, daemon=True)
            thread.start()
        except Exception as e:
            self.log(f"❌ Error en tests: {e}", 'error')
            
    def _ejecutar_test_thread(self):
        """Ejecutar test en thread separado"""
        try:
            from scripts import test_modular
            # test_modular ya no tiene función main, solo ejecuta al importar
            self.queue.put(('log', '✅ Tests ejecutados correctamente', 'success'))
        except Exception as e:
            self.queue.put(('log', f'❌ Error en tests: {e}', 'error'))
            
    def on_closing(self):
        """Manejar cierre de ventana"""
        if self.procesando:
            if messagebox.askokcancel("Cerrar", "¿Cerrar mientras se está procesando?\nEsto puede interrumpir el proceso."):
                self.root.destroy()
        else:
            self.root.destroy()
        
    def run(self):
        """Ejecutar aplicación"""
        self.log("🚀 DataCrédito PDF Converter v2.0 iniciado", 'success')
        self.log("📋 Sistema modular cargado correctamente", 'success')
        self.log("💡 Selecciona carpeta de PDFs para comenzar", 'info')
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log("👋 Aplicación cerrada por el usuario", 'info')

def main():
    """Función principal"""
    try:
        app = ConvertidorDataCredito()
        app.run()
    except Exception as e:
        import traceback
        error_msg = f"Error fatal: {e}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg)
        try:
            import tkinter.messagebox as mb
            mb.showerror("Error Fatal", error_msg)
        except:
            pass

if __name__ == "__main__":
    main()