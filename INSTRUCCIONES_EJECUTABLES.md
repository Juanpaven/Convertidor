# Guía de Uso de los Ejecutables

## Archivos Disponibles

1. **ConvertirPDFaExcel.exe** - Versión principal (sin consola)
2. **ConvertirPDFaExcel_Debug.exe** - Versión con consola para debugging

## Resolución de Problemas

### Error "Failed to start embedded python interpreter!"

Este error puede ocurrir por falta de librerías de Windows. Soluciones:

1. **Instalar Visual C++ Redistributable 2015-2022**:
   - Descargar desde: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Instalar y reiniciar el PC

2. **Usar la versión Debug**:
   - Ejecutar `ConvertirPDFaExcel_Debug.exe`
   - Esta versión muestra mensajes de error detallados
   - Ayuda a identificar qué librerías faltan

3. **Verificar permisos**:
   - Ejecutar como administrador
   - Verificar que el antivirus no esté bloqueando

4. **Verificar sistema**:
   - Windows 10/11 de 64 bits
   - Al menos 4GB de RAM disponible
   - 500MB de espacio libre en disco

## Uso Normal

1. Ejecutar `ConvertirPDFaExcel.exe`
2. Seleccionar carpeta con archivos PDF
3. Seleccionar carpeta donde guardar el Excel
4. Esperar a que procese todos los archivos
5. Revisar el archivo `resultado_detallado.xlsx`

## Si Continúan los Problemas

- Usar la versión con Python instalado manualmente
- Contactar soporte con el mensaje de error específico
- Verificar los logs en la versión Debug