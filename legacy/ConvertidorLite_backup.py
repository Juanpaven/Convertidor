# -*- coding: utf-8 -*-
"""
DataCrédito PDF Converter v2.0 - Interfaz Principal Simplificada
Sistema modular con interfaz gráfica limpia
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import time
import os

# Configurar paths de importación
import setup_paths

# Importar sistema modular
from extractors.info_basica import InformacionBasicaExtractor
from processors.excel_processor import ExcelProcessor
from utils.pdf_reader import PDFReader
from ui.processing_manager import ProcessingManager

class ConvertidorDataCreditoLite:
    """Convertidor moderno simplificado de PDFs DataCrédito a Excel"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.setup_processors()
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("DataCrédito PDF Converter v2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
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
        
        # Configurar carpeta de salida por defecto
        default_output = str(Path.home() / "Downloads")
        self.carpeta_excel.set(default_output)
        
    def setup_widgets(self):
        """Crear widgets de la interfaz - versión simplificada"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Header
        self._create_header(main_frame)
        
        # Sección de archivos
        self._create_file_section(main_frame)
        
        # Sección de control
        self._create_control_section(main_frame)
        
        # Log de procesamiento
        self._create_log_section(main_frame)
        
        # Footer
        self._create_footer(main_frame)
    
    def _create_header(self, parent):
        """Crear header con título"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25))
        
        ttk.Label(header_frame, text="DataCrédito PDF Converter", 
                 font=('Segoe UI', 18, 'bold')).pack()
        ttk.Label(header_frame, text="v2.0 - Sistema Modular", 
                 font=('Segoe UI', 10), foreground='gray').pack()
    
    def _create_file_section(self, parent):
        """Crear sección de selección de archivos"""
        files_frame = ttk.LabelFrame(parent, text="📁 Selección de Archivos", padding="15")
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
        ttk.Button(pdf_frame, text="📂 Seleccionar", command=self.seleccionar_carpeta_pdfs).grid(row=0, column=1)
        
        # Carpeta de salida
        ttk.Label(files_frame, text="💾 Carpeta de salida:", font=('Segoe UI', 10, 'bold')).grid(
            row=2, column=0, sticky="w", pady=(0, 10))
        
        excel_frame = ttk.Frame(files_frame)
        excel_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        excel_frame.columnconfigure(0, weight=1)
        
        self.excel_entry = ttk.Entry(excel_frame, textvariable=self.carpeta_excel, font=('Segoe UI', 10))
        self.excel_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(excel_frame, text="📂 Seleccionar", command=self.seleccionar_carpeta_excel).grid(row=0, column=1)
    
    def _create_control_section(self, parent):
        """Crear sección de control"""
        control_frame = ttk.LabelFrame(parent, text="🎛️ Control", padding="15")
        control_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        # Botones
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_procesar = ttk.Button(button_frame, text="🚀 Procesar PDFs", 
                                      command=self.iniciar_procesamiento)
        self.btn_procesar.pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="📁 Abrir Salida", command=self.abrir_carpeta_salida).pack(side="left")
        
        # Progreso
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(progress_frame, text="Progreso:", font=('Segoe UI', 10, 'bold')).pack(anchor="w")
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progreso, maximum=100)
        self.progress_bar.pack(fill="x", pady=(5, 0))
        
        # Estado
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill="x")
        
        ttk.Label(status_frame, text="Estado:", font=('Segoe UI', 10, 'bold')).pack(anchor="w")
        self.status_label = ttk.Label(status_frame, textvariable=self.status, font=('Segoe UI', 10))
        self.status_label.pack(anchor="w", pady=(5, 0))
    
    def _create_log_section(self, parent):
        """Crear sección de log"""
        log_frame = ttk.LabelFrame(parent, text="📋 Log", padding="15")
        log_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
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
    
    def _create_footer(self, parent):
        """Crear footer"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        
        ttk.Label(footer_frame, text="💡 Tip: Coloca todos los PDFs en una carpeta y selecciona la ruta", 
                 font=('Segoe UI', 9), foreground='gray').pack(anchor="w")
        
    def setup_processors(self):
        """Configurar procesadores"""
        try:
            pdf_reader = PDFReader()
            excel_processor = ExcelProcessor()
            extractor = InformacionBasicaExtractor()
            
            self.processing_manager = ProcessingManager(pdf_reader, excel_processor, extractor)
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
        """Agregar mensaje al log"""
        timestamp = time.strftime("%H:%M:%S")
        color = {"error": "red", "success": "green", "warning": "orange"}.get(tipo, "black")
        
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        
        last_line = self.log_text.index(tk.END + "-2c linestart")
        self.log_text.tag_add(tipo, last_line, tk.END + "-1c")
        self.log_text.tag_config(tipo, foreground=color)
        
        self.log_text.see(tk.END)
        self.root.update()
        
    def iniciar_procesamiento(self):
        """Iniciar procesamiento - versión simplificada"""
        # Validaciones
        if not self._validar_entrada():
            return
            
        # Deshabilitar botón
        self.btn_procesar.config(state='disabled', text='🔄 Procesando...')
        self.status.set("🔄 Procesando archivos...")
        self.progreso.set(0)
        self.log("🚀 Iniciando procesamiento...", "info")
        
        # Usar ProcessingManager
        success = self.processing_manager.procesar_archivos_async(
            self.carpeta_pdfs.get(),
            self.carpeta_excel.get(),
            self._handle_progress_message
        )
        
        if not success:
            self.log("❌ Ya hay un procesamiento en curso", "error")
            self._restaurar_boton()
    
    def _validar_entrada(self):
        """Validar entrada del usuario"""
        if not self.carpeta_pdfs.get():
            messagebox.showerror("Error", "❌ Selecciona la carpeta de PDFs")
            return False
            
        if not self.carpeta_excel.get():
            messagebox.showerror("Error", "❌ Selecciona la carpeta de salida")
            return False
            
        if not Path(self.carpeta_pdfs.get()).exists():
            messagebox.showerror("Error", "❌ La carpeta de PDFs no existe")
            return False
            
        if not Path(self.carpeta_excel.get()).exists():
            messagebox.showerror("Error", "❌ La carpeta de salida no existe")
            return False
        
        return True
    
    def _handle_progress_message(self, mensaje):
        """Manejar mensajes de progreso del ProcessingManager"""
        tipo, data, *extra = mensaje
        
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
            self._restaurar_boton()
        elif tipo == 'completado':
            mensaje_final = f"✅ Procesamiento completado!\n\n📊 Archivo: {Path(data).name}\n\n¿Abrir carpeta?"
            if messagebox.askyesno("Completado", mensaje_final):
                os.startfile(str(Path(data).parent))
            self._restaurar_boton()
    
    def _restaurar_boton(self):
        """Restaurar botón de procesamiento"""
        self.btn_procesar.config(state='normal', text='🚀 Procesar PDFs')
        
    def on_closing(self):
        """Manejar cierre de ventana"""
        if hasattr(self, 'processing_manager') and self.processing_manager.procesando:
            if messagebox.askokcancel("Cerrar", "¿Cerrar mientras se procesa?"):
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
        app = ConvertidorDataCreditoLite()
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