# Convertidor

¡Bienvenido al Convertidor!

Este programa te ayuda a convertir y manejar diferentes tipos de archivos (como PDF y Excel) de manera fácil y rápida. No necesitas saber nada de informática para usarlo.

## ¿Qué necesitas para usarlo?

1. **Una computadora con Windows** (también funciona en Mac y Linux, pero las instrucciones aquí son para Windows).
2. **Tener Python instalado**  
   Si no tienes Python, puedes descargarlo aquí: [Descargar Python](https://www.python.org/downloads/)

## Instalación paso a paso

### 1. Descarga el programa

- Ve a la página del proyecto: [Convertidor en GitHub](https://github.com/Juanpaven/Convertidor)
- Haz clic en el botón verde que dice `Code` y elige `Download ZIP`.
- Cuando termine la descarga, haz doble clic en el archivo ZIP para abrirlo.
- Arrastra la carpeta que está dentro del ZIP a tu escritorio o a donde quieras.

### 2. Instala Python (si no lo tienes)

- Abre el archivo descargado de Python y haz clic en `Install Now`.
- Espera unos minutos hasta que termine.

### 3. Instala lo que necesita el programa

- Abre la carpeta del Convertidor que descargaste.
- Haz clic derecho dentro de la carpeta mientras mantienes la tecla `Shift` presionada, y selecciona **"Abrir ventana de comandos aquí"** o **"Abrir PowerShell aquí"**.
- Escribe lo siguiente y presiona `Enter`:
    ```bash
    pip install -r requirements.txt
    ```
- Espera a que termine.

### 4. Ejecuta el programa

- En la misma ventana de comandos que abriste antes, escribe:
    ```bash
    python convertidor.py
    ```
- Presiona `Enter`.

¡Listo! El programa comenzará y te irá indicando qué hacer en pantalla.

---

## ¿Quieres que funcione sin instalar nada más? (Haz un instalador sencillo)

Puedes crear un archivo que funcione con solo hacer doble clic, siguiendo estos pasos:

### Cómo crear un ejecutable con PyInstaller

1. **Instala PyInstaller**  
   Abre la ventana de comandos y escribe:
   ```bash
   pip install pyinstaller
   ```
   Presiona `Enter`.

2. **Crea el ejecutable**
   - En la misma ventana de comandos, escribe:
     ```bash
     pyinstaller --onefile convertidor.py
     ```
   - Espera a que termine el proceso (puede tardar varios minutos).

3. **Busca tu programa listo para usar**
   - Abre la carpeta llamada `dist` que aparecerá dentro de la carpeta del Convertidor.
   - Dentro de `dist`, encontrarás un archivo llamado `convertidor.exe`.
   - ¡Haz doble clic en `convertidor.exe` para usar el programa!

### Nota
- Si tu programa necesita leer o guardar archivos, ponlos en la misma carpeta que el ejecutable.
- Si aparece una ventana negra (terminal), es normal: ahí verás las instrucciones y resultados.

---

## ¿Necesitas ayuda?

Si tienes dudas, pide ayuda a alguien de confianza o escríbeme por GitHub. ¡No tengas miedo de probar!

---

## Más información

Si eres curioso y quieres aprender más sobre cómo funciona este programa, puedes leer el código en el archivo `convertidor.py`.
