from datetime import datetime
from typing import Dict, Any

def crear_usuario(id: str, nombres: str, apellidos: str, 
                 telefono: str, direccion: str, 
                 tipo: str = "residente") -> Dict[str, Any]:
    """Crea una estructura de datos para un usuario."""
    return {
        "id": id,
        "nombres": nombres.strip().title(),
        "apellidos": apellidos.strip().title(),
        "telefono": telefono.strip(),
        "direccion": direccion.strip(),
        "tipo": tipo,
        "fechaRegistro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "activo": True
    }

def validar_usuario(usuario: Dict[str, Any]) -> tuple[bool, str]:
    """Valida los datos de un usuario."""
    if not usuario.get("nombres") or len(usuario["nombres"]) < 2:
        return False, "Los nombres deben tener al menos 2 caracteres"
    
    if not usuario.get("apellidos") or len(usuario["apellidos"]) < 2:
        return False, "Los apellidos deben tener al menos 2 caracteres"
    
    if not usuario.get("telefono") or len(usuario["telefono"]) < 7:
        return False, "El teléfono debe tener al menos 7 caracteres"
    
    if not usuario.get("direccion"):
        return False, "La dirección es obligatoria"
    
    tipo = usuario.get("tipo", "")
    if tipo not in ["residente", "administrador"]:
        return False, "El tipo debe ser 'residente' o 'administrador'"
    
    return True, "Válido"

def es_administrador(usuario: Dict[str, Any]) -> bool:
    """Verifica si el usuario es administrador."""
    return usuario.get("tipo") == "administrador"

def nombre_completo(usuario: Dict[str, Any]) -> str:
    """Retorna el nombre completo del usuario."""
    return f"{usuario.get('nombres', '')} {usuario.get('apellidos', '')}"

def esta_activo(usuario: Dict[str, Any]) -> bool:
    """Verifica si el usuario está activo."""
    return usuario.get("activo", False)