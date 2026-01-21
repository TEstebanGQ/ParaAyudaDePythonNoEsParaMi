import re
from typing import Any

def validar_no_vacio(valor: str, nombre_campo: str) -> tuple[bool, str]:
    """Valida que un campo no esté vacío."""
    if not valor or not valor.strip():
        return False, f"{nombre_campo} no puede estar vacío"
    return True, ""

def validar_longitud_minima(valor: str, longitud: int, nombre_campo: str) -> tuple[bool, str]:
    """Valida que un campo tenga una longitud mínima."""
    if len(valor) < longitud:
        return False, f"{nombre_campo} debe tener al menos {longitud} caracteres"
    return True, ""

def validar_numero_positivo(valor: Any, nombre_campo: str) -> tuple[bool, str]:
    """Valida que un valor sea un número positivo."""
    try:
        numero = float(valor)
        if numero < 0:
            return False, f"{nombre_campo} debe ser positivo"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{nombre_campo} debe ser un número válido"

def validar_telefono(telefono: str) -> tuple[bool, str]:
    """Valida el formato de un teléfono."""
    # Acepta números con o sin espacios, guiones o paréntesis
    patron = r'^[\d\s\-\(\)]+$'
    if not re.match(patron, telefono):
        return False, "El teléfono contiene caracteres inválidos"
    
    # Verificar longitud mínima de dígitos
    digitos = re.sub(r'[^\d]', '', telefono)
    if len(digitos) < 7:
        return False, "El teléfono debe tener al menos 7 dígitos"
    
    return True, ""

def validar_en_lista(valor: str, lista_valida: list, nombre_campo: str) -> tuple[bool, str]:
    """Valida que un valor esté en una lista de opciones válidas."""
    if valor not in lista_valida:
        return False, f"{nombre_campo} debe ser uno de: {', '.join(lista_valida)}"
    return True, ""

def generar_id(prefijo: str, numero: int) -> str:
    """Genera un ID con formato prefijo-numero."""
    return f"{prefijo}-{numero:04d}"