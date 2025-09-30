# 📊 DataCrédito PDF Converter v2.0

> **Sistema modular profesional para convertir reportes DataCrédito de PDF a Excel**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🚀 **Características Principales**

- ✅ **Interfaz Gráfica Moderna** - Diseño intuitivo con procesamiento en background
- ✅ **Arquitectura Modular** - Sistema extensible y mantenible
- ✅ **Extracción Inteligente** - Validación automática de personas naturales
- ✅ **Excel Profesional** - Múltiples hojas con formato empresarial
- ✅ **Ejecutable Standalone** - Distribución sin instalación de Python

## 📁 **Estructura Organizada**

```
Convertidor/
├── 📄 Convertidor.py          # Aplicación principal
├── 📄 requirements.txt        # Dependencias
├── 📄 README.md              # Este archivo
├── 🗂️ src/                   # Código fuente modular
│   ├── extractors/           # Extractores especializados
│   ├── processors/           # Procesadores de salida
│   ├── utils/               # Utilidades comunes
│   └── config/              # Configuraciones
├── 🗂️ dist/                  # Ejecutables listos para usar
├── 🗂️ scripts/               # Scripts de desarrollo
├── 🗂️ docs/                  # Documentación técnica
├── 🗂️ legacy/                # Versiones anteriores
└── 🗂️ config/                # Archivos de configuración
```

## 🎯 **Uso Rápido**

### **Opción 1: Ejecutable (Recomendado)**
```bash
# Doble clic o desde terminal:
.\dist\ConvertidorDataCredito_v2.exe
```

### **Opción 2: Python Directo**
```bash
python Convertidor.py
```

### **Opción 3: Lanzador Automático**
```bash
.\Ejecutar_Convertidor.bat
```

## 📊 **Resultado Excel**

| Hoja | Contenido | Propósito |
|------|-----------|-----------|
| **Información Básica** | Datos limpios del usuario | Vista principal para análisis |
| **Resumen** | Estadísticas de procesamiento | Control de calidad |
| **Diagnóstico Técnico** | Información completa + errores | Debugging y soporte |

## 🔧 **Para Desarrolladores**

```bash
# Ejecutar tests
python scripts/test_modular.py

# Ejecutar demo
python scripts/demo_modular.py

# Instalar dependencias
pip install -r requirements.txt
```

## 📋 **Campos Extraídos**

- **Consultado por** (solo personas naturales)
- **Fecha y Hora Consulta**
- **Tipo y Número de Documento**
- **Estado y Lugar de Expedición**
- **Información Personal** (Nombre, Edad, Género)
- **Ubicación** (Antigüedad en dirección)

---

### 💡 **Tip**: Coloca todos los PDFs en una carpeta y selecciona la ruta. El sistema procesará automáticamente todos los archivos.