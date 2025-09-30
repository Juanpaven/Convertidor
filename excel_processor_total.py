# -*- coding: utf-8 -*-
"""
PROCESADOR EXCEL TOTAL - Genera Excel con TODOS los datos extraídos
"""
import pandas as pd
from typing import Dict, Any, List
import os
from datetime import datetime

class ExcelProcessorTotal:
    """Procesador que maneja TODOS los campos extraídos"""
    
    def __init__(self):
        self.nombre = "Procesador Excel Total"
        
    def procesar(self, datos: List[Dict[str, Any]], carpeta_pdfs: str) -> bool:
        """Procesa todos los datos y genera Excel completo"""
        
        if not datos:
            print("❌ No hay datos para procesar")
            return False
        
        print(f"\n📊 PROCESANDO {len(datos)} PDFs con datos completos")
        
        # Crear DataFrame con TODOS los campos posibles
        df = self.crear_dataframe_completo(datos)
        
        # Generar archivo Excel
        archivo_excel = self.generar_excel(df, carpeta_pdfs)
        
        if archivo_excel:
            print(f"✅ ARCHIVO EXCEL CREADO: {archivo_excel}")
            print(f"📈 Total filas: {len(df)}")
            print(f"📈 Total columnas: {len(df.columns)}")
            
            # Estadísticas
            self.mostrar_estadisticas(df)
            
            return True
        
        return False
    
    def crear_dataframe_completo(self, datos: List[Dict[str, Any]]) -> pd.DataFrame:
        """Crea DataFrame con TODAS las columnas posibles"""
        
        print("🔄 Unificando campos de todos los PDFs...")
        
        # Recopilar TODOS los campos únicos de todos los PDFs
        todos_campos = set()
        
        for registro in datos:
            todos_campos.update(registro.keys())
        
        print(f"📊 Total campos únicos encontrados: {len(todos_campos)}")
        
        # Crear estructura completa
        datos_completos = []
        
        for registro in datos:
            fila_completa = {}
            
            # Llenar TODOS los campos
            for campo in sorted(todos_campos):  # Ordenar alfabéticamente
                valor = registro.get(campo, "")
                
                # Limpiar y formatear valor
                if valor is None:
                    valor = ""
                elif isinstance(valor, (list, dict)):
                    valor = str(valor)
                else:
                    valor = str(valor).strip()
                
                fila_completa[campo] = valor
            
            datos_completos.append(fila_completa)
        
        # Crear DataFrame
        df = pd.DataFrame(datos_completos)
        
        # Reordenar columnas: campos importantes primero
        columnas_prioritarias = [
            'nombre_completo', 'numero_documento', 'cedula_consultado',
            'consultado_por', 'fecha_consulta', 'archivo',
            'total_campos_extraidos', 'procesado'
        ]
        
        columnas_ordenadas = []
        
        # Agregar columnas prioritarias si existen
        for col in columnas_prioritarias:
            if col in df.columns:
                columnas_ordenadas.append(col)
        
        # Agregar resto de columnas alfabéticamente
        columnas_restantes = sorted([col for col in df.columns if col not in columnas_ordenadas])
        columnas_ordenadas.extend(columnas_restantes)
        
        # Reordenar DataFrame
        df = df[columnas_ordenadas]
        
        return df
    
    def generar_excel(self, df: pd.DataFrame, carpeta_pdfs: str) -> str:
        """Genera archivo Excel con formato"""
        
        try:
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"DataCredito_COMPLETO_{timestamp}.xlsx"
            ruta_excel = os.path.join(carpeta_pdfs, nombre_archivo)
            
            # Crear archivo Excel con formato
            with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
                
                # Hoja principal con todos los datos
                df.to_excel(writer, sheet_name='Datos_Completos', index=False)
                
                # Obtener workbook y worksheet para formato
                workbook = writer.book
                worksheet = writer.sheets['Datos_Completos']
                
                # Formato para headers
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#366092',
                    'font_color': 'white'
                })
                
                # Aplicar formato a headers
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    # Establecer ancho mínimo y máximo
                    adjusted_width = min(max(max_length, 10), 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # Hoja de resumen/estadísticas
                self.crear_hoja_resumen(writer, df)
            
            return ruta_excel
            
        except Exception as e:
            print(f"❌ Error creando Excel: {e}")
            return ""
    
    def crear_hoja_resumen(self, writer, df: pd.DataFrame):
        """Crea hoja de resumen con estadísticas"""
        
        # Estadísticas generales
        resumen_data = {
            'Estadística': [
                'Total PDFs procesados',
                'Total campos únicos',
                'Promedio campos por PDF',
                'PDFs con datos completos',
                'Fechas procesamiento'
            ],
            'Valor': [
                len(df),
                len(df.columns),
                df['total_campos_extraidos'].mean() if 'total_campos_extraidos' in df.columns else 'N/A',
                len(df[df['procesado'] == True]) if 'procesado' in df.columns else 'N/A',
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
        }
        
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
        
        # Top 10 campos más completos
        if len(df) > 0:
            completitud = {}
            for col in df.columns:
                if col not in ['_metadata', 'archivo']:
                    valores_no_vacios = df[col].notna().sum()
                    completitud[col] = valores_no_vacios
            
            top_campos = sorted(completitud.items(), key=lambda x: x[1], reverse=True)[:15]
            
            df_top = pd.DataFrame(top_campos, columns=['Campo', 'PDFs_con_datos'])
            df_top.to_excel(writer, sheet_name='Campos_Principales', index=False)
    
    def mostrar_estadisticas(self, df: pd.DataFrame):
        """Muestra estadísticas del procesamiento"""
        
        print("\n📈 ESTADÍSTICAS DE PROCESAMIENTO:")
        print(f"   📄 PDFs procesados: {len(df)}")
        print(f"   📊 Campos totales: {len(df.columns)}")
        
        if 'total_campos_extraidos' in df.columns:
            promedio = df['total_campos_extraidos'].mean()
            print(f"   📈 Promedio campos por PDF: {promedio:.1f}")
        
        # Campos con más datos
        completitud = {}
        for col in df.columns:
            if col not in ['_metadata', 'archivo']:
                valores_no_vacios = df[col].notna().sum()
                if valores_no_vacios > 0:
                    completitud[col] = valores_no_vacios
        
        top_5 = sorted(completitud.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print("\n🏆 TOP 5 CAMPOS MÁS COMPLETOS:")
        for i, (campo, count) in enumerate(top_5, 1):
            porcentaje = (count / len(df)) * 100
            print(f"   {i}. {campo}: {count}/{len(df)} PDFs ({porcentaje:.1f}%)")
        
        print("\n✅ Procesamiento completado exitosamente")