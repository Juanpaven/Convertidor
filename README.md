# 📋 CONVERTIDOR DE PDFs A EXCEL - GUÍA DE INSTALACIÓN Y USO

## 🚀 INSTALACIÓN RÁPIDA

### Opción 1: Usar el archivo ejecutable (.exe)
1. Descargar el archivo `ConvertirPDFaExcel.exe`
2. Ejecutar directamente (no requiere instalación)
3. Seguir la interfaz gráfica

### Opción 2: Instalación desde código fuente
```bash
# 1. Clonar o descargar el proyecto
# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python Convertidor.py
```

## 📊 CAPACIDAD DE PROCESAMIENTO

### Hardware Mínimo:
- **RAM**: 4GB (8GB+ recomendado para gran volumen)
- **Disco**: 1GB libre (más según cantidad de PDFs)
- **OS**: Windows 10+, macOS 10.14+, Linux Ubuntu 18+

### Capacidad por Hardware:
| RAM | PDFs Pequeños | PDFs Medianos | PDFs Grandes |
|-----|--------------|---------------|--------------|
| 4GB | 500-1,000    | 200-500       | 50-200       |
| 8GB | 1,000-2,000  | 500-1,000     | 200-500      |
| 16GB| 2,000-5,000  | 1,000-2,000   | 500-1,000    |

## 🎯 CÓMO USAR LA APLICACIÓN

### 1. Preparar archivos PDF
- Colocar todos los PDFs en una carpeta
- Los PDFs deben ser de reportes crediticios válidos
- Formatos soportados: PDF con texto extraíble

### 2. Ejecutar aplicación
- Abrir `ConvertirPDFaExcel.exe` o ejecutar `python Convertidor.py`
- Seleccionar carpeta con PDFs
- Seleccionar carpeta donde guardar Excel
- Hacer clic en "Procesar PDFs"

### 3. Resultado
- Se genera `resultado_detallado.xlsx`
- Datos organizados por cliente
- Formato profesional con colores
- Información crediticia completa

## 📈 CARACTERÍSTICAS DEL EXCEL GENERADO

### Estructura de datos:
- **Información Personal**: 11 columnas
- **Créditos Vigentes**: 7 columnas por sector
- **Créditos Cerrados**: 7 columnas por sector
- **Créditos Reestructurados**: 7 columnas por sector
- **Créditos Refinanciados**: 7 columnas por sector
- **Consultas Últimos 6 Meses**: 7 columnas por sector
- **Desacuerdos Vigentes**: 7 columnas por sector
- **Antigüedad**: 3 columnas por sector

### Formato visual:
- ✅ Encabezados anidados con colores
- ✅ Ordenamiento automático por cliente
- ✅ Colores alternos por persona
- ✅ Campos numéricos: "0" si vacío
- ✅ Campos texto: "SIN INFO" si vacío

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "No se encontraron archivos PDF"
- Verificar que la carpeta contiene archivos .pdf
- Verificar permisos de lectura

### Error: "Memoria insuficiente"
- Procesar archivos en lotes más pequeños
- Cerrar otros programas
- Considerar upgrade de RAM

### Error: "No se puede crear Excel"
- Verificar permisos de escritura en carpeta destino
- Cerrar Excel si está abierto
- Verificar espacio en disco

## 🔧 CREAR ARCHIVO EJECUTABLE

Para desarrolladores que quieran crear el .exe:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear ejecutable
pyinstaller --onefile --windowed --name "ConvertirPDFaExcel" Convertidor.py
```

El archivo .exe se generará en la carpeta `dist/`

## 📞 SOPORTE

Para reportar problemas o solicitar mejoras:
- Verificar que se cumplan los requisitos mínimos
- Incluir descripción detallada del error
- Adjuntar captura de pantalla si es posible