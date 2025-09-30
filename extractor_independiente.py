# -*- coding: utf-8 -*-
"""
EXTRACTOR INDEPENDIENTE - Sin dependencias externas
Diseñado para extraer TODA la información de PDFs DataCrédito
"""
import re
from typing import Dict, Any

class ExtractorIndependiente:
    """Extractor completamente independiente para PDFs DataCrédito"""
    
    def __init__(self):
        self.nombre = "Extractor Independiente"
        
    def extract(self, texto: str, archivo: str) -> Dict[str, Any]:
        """Extrae TODA la información del PDF"""
        
        print(f"\n🔍 EXTRAYENDO DE: {archivo}")
        print(f"📄 Texto length: {len(texto)} caracteres")
        
        # Normalizar texto
        texto_limpio = self.limpiar_texto(texto)
        
        # Mostrar muestra del texto
        print(f"📝 Primeras líneas:")
        for i, linea in enumerate(texto_limpio.split('\\n')[:10], 1):
            if linea.strip():
                print(f"   {i:2d}: {linea.strip()}")
        
        registro = {}
        
        # === INFORMACIÓN BÁSICA ===
        
        # 1. Consultado por
        consultado = self.extraer_consultado_por(texto_limpio)
        if consultado:
            registro['consultado_por'] = consultado
            print(f"✅ Consultado por: {consultado}")
        
        # 2. Fecha de consulta
        fecha = self.extraer_fecha_consulta(texto_limpio)
        if fecha:
            registro['fecha_consulta'] = fecha
            print(f"✅ Fecha consulta: {fecha}")
        
        # 3. Hora de consulta
        hora = self.extraer_hora_consulta(texto_limpio)
        if hora:
            registro['hora_consulta'] = hora
            print(f"✅ Hora consulta: {hora}")
        
        # 4. Tipo de documento
        tipo_doc = self.extraer_tipo_documento(texto_limpio)
        if tipo_doc:
            registro['tipo_documento'] = tipo_doc
            print(f"✅ Tipo documento: {tipo_doc}")
        
        # 5. Número de documento
        numero = self.extraer_numero_documento(texto_limpio)
        if numero:
            registro['numero_documento'] = numero
            print(f"✅ Número documento: {numero}")
        
        # 6. Estado documento
        estado = self.extraer_estado_documento(texto_limpio)
        if estado:
            registro['estado_documento'] = estado
            print(f"✅ Estado documento: {estado}")
        
        # 7. Lugar expedición
        lugar = self.extraer_lugar_expedicion(texto_limpio)
        if lugar:
            registro['lugar_expedicion'] = lugar
            print(f"✅ Lugar expedición: {lugar}")
        
        # 8. Fecha expedición
        fecha_exp = self.extraer_fecha_expedicion(texto_limpio)
        if fecha_exp:
            registro['fecha_expedicion'] = fecha_exp
            print(f"✅ Fecha expedición: {fecha_exp}")
        
        # 9. Nombre completo
        nombre = self.extraer_nombre_completo(texto_limpio)
        if nombre:
            registro['nombre_completo'] = nombre
            print(f"✅ Nombre: {nombre}")
        
        # 10. Rango edad
        edad = self.extraer_rango_edad(texto_limpio)
        if edad:
            registro['rango_edad'] = edad
            print(f"✅ Rango edad: {edad}")
        
        # 11. Género
        genero = self.extraer_genero(texto_limpio)
        if genero:
            registro['genero'] = genero
            print(f"✅ Género: {genero}")
        
        # 12. Antigüedad ubicación
        antiguedad = self.extraer_antiguedad_ubicacion(texto_limpio)
        if antiguedad:
            registro['antiguedad_ubicacion'] = antiguedad
            print(f"✅ Antigüedad ubicación: {antiguedad}")
        
        # === INFORMACIÓN ADICIONAL ===
        
        # 13. Dirección
        direccion = self.extraer_direccion(texto_limpio)
        if direccion:
            registro['direccion_residencia'] = direccion
            print(f"✅ Dirección: {direccion}")
        
        # 14. Ciudad
        ciudad = self.extraer_ciudad(texto_limpio)
        if ciudad:
            registro['ciudad_residencia'] = ciudad
            print(f"✅ Ciudad: {ciudad}")
        
        # 15. Teléfono
        telefono = self.extraer_telefono(texto_limpio)
        if telefono:
            registro['telefono'] = telefono
            print(f"✅ Teléfono: {telefono}")
        
        # 16. Email
        email = self.extraer_email(texto_limpio)
        if email:
            registro['email'] = email
            print(f"✅ Email: {email}")
        
        # 17. Score
        score = self.extraer_score(texto_limpio)
        if score:
            registro['score'] = score
            print(f"✅ Score: {score}")
        
        # 18. Saldo
        saldo = self.extraer_saldo(texto_limpio)
        if saldo:
            registro['saldo'] = saldo
            print(f"✅ Saldo: {saldo}")
        
        # === EXTRACCIÓN AUTOMÁTICA ===
        # Buscar más información automáticamente
        info_adicional = self.extraer_automatico(texto_limpio)
        registro.update(info_adicional)
        
        # Contar campos extraídos
        campos_extraidos = len([v for v in registro.values() if v and str(v).strip()])
        
        print(f"\\n📊 TOTAL EXTRAÍDO: {campos_extraidos} campos")
        
        # Metadatos
        registro['_metadata'] = {
            'archivo': archivo,
            'total_campos_extraidos': campos_extraidos,
            'texto_completo_length': len(texto),
            'procesado': campos_extraidos > 0
        }
        
        return registro
    
    def limpiar_texto(self, texto: str) -> str:
        """Limpia y normaliza el texto"""
        # Reemplazar saltos de línea problemáticos
        texto = texto.replace('\\r\\n', '\\n').replace('\\r', '\\n')
        # Normalizar espacios
        texto = re.sub(r'\\s+', ' ', texto)
        return texto
    
    def buscar_patron(self, patron: str, texto: str) -> str:
        """Busca un patrón en el texto"""
        try:
            match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
            if match:
                resultado = match.group(1).strip() if match.groups() else match.group(0).strip()
                return resultado
        except Exception:
            pass
        return ""
    
    def buscar_multiples_patrones(self, patrones: list, texto: str) -> str:
        """Busca múltiples patrones y retorna el primer match"""
        for patron in patrones:
            resultado = self.buscar_patron(patron, texto)
            if resultado:
                return resultado
        return ""
    
    # === MÉTODOS DE EXTRACCIÓN ESPECÍFICOS ===
    
    def extraer_consultado_por(self, texto: str) -> str:
        patrones = [
            r"Consultado por:\\s*([A-ZÁÉÍÓÚÑ]+\\s+[A-ZÁÉÍÓÚÑ]+\\s+[a-záéíóúñ]+)\\s+DELAGRO",
            r"Consultado por:\\s*([A-ZÁÉÍÓÚÑ][^\\n]*?)(?=\\s+(?:SAS|LTDA|S\\.A|DELAGRO))",
            r"([A-ZÁÉÍÓÚÑ]+\\s+[A-ZÁÉÍÓÚÑ]+\\s+[a-záéíóúñ]+)(?=\\s*DELAGRO)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_fecha_consulta(self, texto: str) -> str:
        patrones = [
            r"Fecha y Hora Consulta[:\\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",
            r"Fecha[^:]*:[\\s]*([0-9]{1,2}[/\\-][0-9]{1,2}[/\\-][0-9]{4})",
            r"\\b([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_hora_consulta(self, texto: str) -> str:
        patrones = [
            r"Fecha y Hora Consulta[^\\n]*([0-9]{1,2}:[0-9]{2}:[0-9]{2})",
            r"([0-9]{1,2}:[0-9]{2}:[0-9]{2})",
            r"([0-9]{1,2}:[0-9]{2})\\s*(?:AM|PM)?"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_tipo_documento(self, texto: str) -> str:
        patrones = [
            r"Tipo Documento[:\\s]*([^\\n]{3,30})",
            r"(Cédula de Ciudadanía)",
            r"(C\\.C\\.)",
            r"(Tarjeta de Identidad)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_numero_documento(self, texto: str) -> str:
        patrones = [
            r"Número Documento[:\\s]*([0-9\\.\\,]+)",
            r"C\\.C\\.?[\\s]*:?[\\s]*([0-9\\.\\,]+)",
            r"Documento[^:]*:[\\s]*([0-9\\.\\,]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_estado_documento(self, texto: str) -> str:
        patrones = [
            r"Estado Documento[:\\s]*([A-Za-záéíóúñ]+)",
            r"\\b(Vigente|Vencido|Activo|Inactivo)\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_lugar_expedicion(self, texto: str) -> str:
        patrones = [
            r"Lugar Expedición[:\\s]*([A-ZÁÉÍÓÚÑa-z\\s]+?)(?=\\s*Fecha|\\n)",
            r"Expedido en[:\\s]*([A-ZÁÉÍÓÚÑa-z\\s]+)",
            r"\\b(BOGOTA|MEDELLIN|CALI|IBAGUE|BARRANQUILLA)\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_fecha_expedicion(self, texto: str) -> str:
        patrones = [
            r"Fecha Expedición[:\\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",
            r"Expedido el[:\\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_nombre_completo(self, texto: str) -> str:
        patrones = [
            r"Nombre:\\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\\s]+?)(?=\\n|Rango)",
            r"Nombres y Apellidos:\\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\\s]+?)(?=\\n)",
            r"Nombres:\\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\\s]+?)(?=\\n)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_rango_edad(self, texto: str) -> str:
        patrones = [
            r"Rango Edad[:\\s]*([0-9\\-]+)",
            r"Edad[:\\s]*([0-9\\-]+)",
            r"\\b([0-9]{2}-[0-9]{2})\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_genero(self, texto: str) -> str:
        patrones = [
            r"Género[:\\s]*([A-Za-záéíóúñ]+)",
            r"Sexo[:\\s]*([A-Za-záéíóúñ]+)",
            r"\\b(Masculino|Femenino|Hombre|Mujer)\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_antiguedad_ubicacion(self, texto: str) -> str:
        patrones = [
            r"Antigüedad Ubicación[:\\s]*([^\\n]{5,50})",
            r"Antiguedad Ubicación[:\\s]*([^\\n]{5,50})",
            r"([0-9]+\\s*Meses\\s*[A-Za-z\\s]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_direccion(self, texto: str) -> str:
        patrones = [
            r"Dirección[:\\s]*([^\\n]{10,80})",
            r"Residencia[:\\s]*([^\\n]{10,80})",
            r"Domicilio[:\\s]*([^\\n]{10,80})"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_ciudad(self, texto: str) -> str:
        patrones = [
            r"Ciudad[:\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{3,30})",
            r"Municipio[:\\s]*([A-ZÁÉÍÓÚÑ][^\\n]{3,30})"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_telefono(self, texto: str) -> str:
        patrones = [
            r"Teléfono[:\\s]*([0-9\\s\\-\\(\\)]{7,15})",
            r"Tel[:\\s]*([0-9\\s\\-\\(\\)]{7,15})",
            r"Celular[:\\s]*([0-9\\s\\-\\(\\)]{7,15})"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_email(self, texto: str) -> str:
        patrones = [
            r"Email[:\\s]*([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})",
            r"Correo[:\\s]*([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})",
            r"\\b([a-zA-Z0-9\\._%+-]+@[a-zA-Z0-9\\.-]+\\.[a-zA-Z]{2,})\\b"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_score(self, texto: str) -> str:
        patrones = [
            r"Score[:\\s]*([0-9]+)",
            r"Puntaje[:\\s]*([0-9]+)",
            r"Calificación[:\\s]*([A-Z0-9]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_saldo(self, texto: str) -> str:
        patrones = [
            r"Saldo[:\\s]*([0-9\\.,\\$]+)",
            r"Valor[:\\s]*([0-9\\.,\\$]+)",
            r"Deuda[:\\s]*([0-9\\.,\\$]+)"
        ]
        return self.buscar_multiples_patrones(patrones, texto)
    
    def extraer_automatico(self, texto: str) -> Dict[str, str]:
        """Extrae información adicional automáticamente"""
        info = {}
        
        # Buscar líneas con formato "Campo: Valor"
        lineas = texto.split('\\n')
        contador = 0
        
        for linea in lineas:
            linea = linea.strip()
            if ':' in linea and len(linea) > 5 and contador < 20:  # Límite de 20 campos adicionales
                try:
                    campo, valor = linea.split(':', 1)
                    campo = campo.strip()
                    valor = valor.strip()
                    
                    if len(valor) > 0 and len(valor) < 100 and len(campo) < 50:
                        # Limpiar nombre del campo
                        campo_limpio = re.sub(r'[^A-Za-z0-9\\s]', '', campo)
                        campo_limpio = campo_limpio.replace(' ', '_').lower()
                        
                        if campo_limpio and campo_limpio not in info:
                            info[f"auto_{campo_limpio}"] = valor
                            contador += 1
                            print(f"✅ Auto-extraído {campo_limpio}: {valor}")
                except:
                    continue
        
        return info