import os
import re
import pdfplumber
import pandas as pd
import openpyxl

# Ruta a la carpeta donde tienes los PDFs
carpeta_pdfs = "C:\\Users\\delag\\OneDrive\\Escritorio\\Juan Avendaño\\prueba"

# Lista donde guardaremos los resultados
datos = []

def extraer_info(texto, archivo):
    """Extrae datos para persona natural y jurídica, ajustando 'Consultado por' según el tipo de documento"""
    registro = {
        "Consultado por": "NO APLICA",
        "Fecha y Hora Consulta": "NO APLICA",
        "Tipo Documento": "NO APLICA",
        "Número Documento": "NO APLICA",
        "Estado Documento": "NO APLICA",
        "Lugar Expedición": "NO APLICA",
        "Fecha Expedición": "NO APLICA",
        "Nombre": "NO APLICA",
        "Rango Edad": "NO APLICA",
        "Género": "NO APLICA",
        "Antigüedad Ubicación": "NO APLICA"
    }

    # Buscar fecha y hora de consulta
    fecha_hora = re.search(r"Fecha y Hora Consulta\s*:?\s*([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\.[0-9]{2} (AM|PM))", texto)
    if not fecha_hora:
        fecha_hora = re.search(r"(20[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\.[0-9]{2} (AM|PM))", texto)
    if fecha_hora:
        registro["Fecha y Hora Consulta"] = fecha_hora.group(1).strip()

    # Detectar si es persona jurídica (NIT)
    nit = re.search(r"NIT\s*:?\s*([0-9A-Z-]+)", texto)
    nombre_jur = re.search(r"Nombre\s*:?\s*([A-ZÁÉÍÓÚÑ\s]+SAS|LTDA|S\.A\.)", texto)
    if nit:
        registro["Tipo Documento"] = "NIT"
        registro["Número Documento"] = nit.group(1).strip()
        # Nombre para persona jurídica
        if nombre_jur:
            registro["Nombre"] = nombre_jur.group(1).strip()
        else:
            nombre_simple = re.search(r"Nombre\s*:?\s*([A-ZÁÉÍÓÚÑ\s]+)", texto)
            if nombre_simple:
                registro["Nombre"] = nombre_simple.group(1).strip()
        # Consultado por para persona jurídica: buscar la línea que contiene 'Consultado por:' y tomar el valor después de los dos puntos
        consultado_jur = re.search(r"Consultado por\s*:?\s*([A-ZÁÉÍÓÚÑa-z\s]+)", texto)
        if consultado_jur:
            valor = consultado_jur.group(1).strip()
            # Si el valor no es empresa, lo tomamos
            if not any(x in valor.upper() for x in ['SAS', 'LTDA', 'S.A.', 'DELAGRO']):
                registro["Consultado por"] = valor
    else:
        # Persona natural: buscar la línea que contiene 'Consultado por' y tomar solo el nombre de la persona
        consultado_nat = None
        for linea in texto.splitlines():
            if 'Consultado por' in linea:
                partes = linea.split(':', 1)
                if len(partes) > 1:
                    valor = partes[1].strip()
                    # Omitir empresas, números y AM/PM
                    valor = re.sub(r"\b(AM|PM)\b", "", valor, flags=re.IGNORECASE).strip()
                    if not any(x in valor.upper() for x in ['SAS', 'LTDA', 'S.A.', 'DELAGRO']) and not re.search(r"\d", valor):
                        consultado_nat = valor
                else:
                    idx = texto.splitlines().index(linea)
                    if idx + 1 < len(texto.splitlines()):
                        valor = texto.splitlines()[idx + 1].strip()
                        valor = re.sub(r"\b(AM|PM)\b", "", valor, flags=re.IGNORECASE).strip()
                        if not any(x in valor.upper() for x in ['SAS', 'LTDA', 'S.A.', 'DELAGRO']) and not re.search(r"\d", valor):
                            consultado_nat = valor
        if consultado_nat:
            registro["Consultado por"] = consultado_nat
        else:
            # Buscar patrón alternativo: nombre seguido de guion y número, tomar solo el nombre y quitar AM/PM
            persona = re.search(r"([A-ZÁÉÍÓÚÑa-z\s]+)\s*-\s*[0-9]+", texto)
            if persona:
                valor = persona.group(1).strip()
                valor = re.sub(r"\b(AM|PM)\b", "", valor, flags=re.IGNORECASE).strip()
                if not any(x in valor.upper() for x in ['SAS', 'LTDA', 'S.A.', 'DELAGRO']):
                    registro["Consultado por"] = valor
    # ...existing code para los demás campos...
    tipo_doc = re.search(r"Tipo Documento\s*[:\s]*([A-Z.]+)", texto)
    if tipo_doc:
        registro["Tipo Documento"] = tipo_doc.group(1).strip()
    else:
        cc = re.search(r"C\.C\.", texto)
        if cc:
            registro["Tipo Documento"] = "C.C."
    num_doc = re.search(r"Número Documento\s*[:\s]*([0-9]+)", texto)
    if num_doc:
        registro["Número Documento"] = num_doc.group(1).strip()
    else:
        cc_num = re.search(r"C\.C\.\s*([0-9]+)", texto)
        if cc_num:
            registro["Número Documento"] = cc_num.group(1).strip()
    estado = re.search(r"Estado Documento\s*[:\s]*([A-Za-zÁÉÍÓÚÑ]+)", texto)
    if estado:
        registro["Estado Documento"] = estado.group(1).strip()
    else:
        vigente = re.search(r"Vigente", texto)
        if vigente:
            registro["Estado Documento"] = "Vigente"
    # Lugar Expedición (solo hasta antes de 'Fecha Expedicion')
    lugar = re.search(r"Lugar Expedición\s*[:\s]*([A-ZÁÉÍÓÚÑa-z\s]+?)(?=\s*Fecha Expedici|$)", texto)
    if lugar:
        registro["Lugar Expedición"] = lugar.group(1).strip()
    else:
        ibague = re.search(r"IBAGUE", texto)
        if ibague:
            registro["Lugar Expedición"] = "IBAGUE"
    fecha = re.search(r"Fecha Expedición\s*[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})", texto)
    if fecha:
        registro["Fecha Expedición"] = fecha.group(1).strip()
    # Nombre para persona jurídica
    if nit:
        nombre_jur = re.search(r"Nombre\s*:?\s*([A-ZÁÉÍÓÚÑ\s]+)(?=\s*NIT)", texto)
        if nombre_jur:
            registro["Nombre"] = nombre_jur.group(1).strip()
        else:
            nombre_simple = re.search(r"Nombre\s*:?\s*([A-ZÁÉÍÓÚÑ\s]+)", texto)
            if nombre_simple:
                registro["Nombre"] = nombre_simple.group(1).strip()
    else:
        # Nombre para persona natural
        nombre = re.search(r"Nombre\s*[:\s]*([A-ZÁÉÍÓÚÑ\s]+)(?=\s*Rango Edad|$)", texto)
        if nombre:
            registro["Nombre"] = nombre.group(1).strip()
        else:
            nombre2 = re.search(r"([A-ZÁÉÍÓÚÑ]+\s+[A-ZÁÉÍÓÚÑ]+)", texto)
            if nombre2:
                registro["Nombre"] = nombre2.group(1).strip()
    rango = re.search(r"Rango Edad\s*[:\s]*([0-9\-]+)", texto)
    if rango:
        registro["Rango Edad"] = rango.group(1).strip()
    else:
        rango2 = re.search(r"(\d{2}-\d{2})", texto)
        if rango2:
            registro["Rango Edad"] = rango2.group(1).strip()
    genero = re.search(r"Género\s*[:\s]*([A-Za-zÁÉÍÓÚÑ]+)", texto)
    if genero:
        registro["Género"] = genero.group(1).strip()
    else:
        femenino = re.search(r"Femenino", texto)
        if femenino:
            registro["Género"] = "Femenino"
    # Antigüedad Ubicación (solo hasta antes de 'ARTICULO' o guion '-')
    antig = re.search(r"Antiguedad Ubicación\s*[:\s]*([0-9]+\s*Meses\s*[A-Za-z\s]+?)(?=\s*ARTICULO|\s*-|$)", texto)
    if antig:
        registro["Antigüedad Ubicación"] = antig.group(1).strip()
    else:
        antig2 = re.search(r"(\d+\s*Meses\s*[A-Za-z\s]+?)(?=\s*ARTICULO|\s*-|$)", texto)
        if antig2:
            registro["Antigüedad Ubicación"] = antig2.group(1).strip()
    return registro


# 🔹 Procesar todos los PDFs en la carpeta
for archivo in os.listdir(carpeta_pdfs):
    if archivo.endswith(".pdf"):
        ruta_pdf = os.path.join(carpeta_pdfs, archivo)
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"

        datos.append(extraer_info(texto, archivo))

# Convertir a DataFrame y guardar en Excel
df = pd.DataFrame(datos)
# Reordenar columnas para que 'Fecha y Hora Consulta' esté después de 'Consultado por' y 'Nombre' después de 'Fecha y Hora Consulta'
cols = list(df.columns)
if 'Consultado por' in cols and 'Fecha y Hora Consulta' in cols and 'Nombre' in cols:
    cols.remove('Fecha y Hora Consulta')
    idx_consultado = cols.index('Consultado por') + 1
    cols.insert(idx_consultado, 'Fecha y Hora Consulta')
    cols.remove('Nombre')
    idx_fecha = cols.index('Fecha y Hora Consulta') + 1
    cols.insert(idx_fecha, 'Nombre')
    df = df[cols]
# Guardar en Excel
excel_path = os.path.join(carpeta_pdfs, "resultado.xlsx")
df.to_excel(excel_path, index=False)
# Ajustar ancho de columnas automáticamente
wb = openpyxl.load_workbook(excel_path)
ws = wb.active
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter # Letra de la columna
    for cell in col:
        try:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass
    adjusted_width = max_length + 2
    ws.column_dimensions[column].width = adjusted_width
wb.save(excel_path)

print("✅ Datos extraídos y guardados en resultado.xlsx con ancho de columnas ajustado")
