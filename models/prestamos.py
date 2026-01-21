from datetime import datetime, timedelta
from typing import Dict, Any

def crear_prestamo(id: str, id_usuario: str, id_herramienta: str,
                  cantidad: int, dias_prestamo: int = 7,
                  observaciones: str = "") -> Dict[str, Any]:
    """Crea una estructura de datos para un préstamo."""
    fecha_inicio = datetime.now()
    fecha_devolucion = fecha_inicio + timedelta(days=dias_prestamo)
    
    return {
        "id": id,
        "idUsuario": id_usuario,
        "idHerramienta": id_herramienta,
        "cantidad": cantidad,
        "fechaInicio": fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        "fechaDevolucionEstimada": fecha_devolucion.strftime("%Y-%m-%d %H:%M:%S"),
        "fechaDevolucionReal": None,
        "estado": "pendiente",
        "observaciones": observaciones,
        "aprobadoPor": None
    }

def validar_prestamo(prestamo: Dict[str, Any]) -> tuple[bool, str]:
    """Valida los datos de un préstamo."""
    if not prestamo.get("idUsuario"):
        return False, "Debe especificar un usuario"
    
    if not prestamo.get("idHerramienta"):
        return False, "Debe especificar una herramienta"
    
    if prestamo.get("cantidad", 0) < 1:
        return False, "La cantidad debe ser al menos 1"
    
    estado = prestamo.get("estado", "")
    estados_validos = ["pendiente", "aprobado", "activo", "devuelto", "rechazado"]
    if estado not in estados_validos:
        return False, f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
    
    return True, "Válido"

def esta_vencido(prestamo: Dict[str, Any]) -> bool:
    """Verifica si el préstamo está vencido."""
    if prestamo.get("estado") != "activo":
        return False
    
    fecha_devolucion = datetime.strptime(
        prestamo["fechaDevolucionEstimada"], 
        "%Y-%m-%d %H:%M:%S"
    )
    return datetime.now() > fecha_devolucion

def marcar_devuelto(prestamo: Dict[str, Any]) -> None:
    """Marca el préstamo como devuelto."""
    prestamo["estado"] = "devuelto"
    prestamo["fechaDevolucionReal"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def aprobar_prestamo(prestamo: Dict[str, Any], id_aprobador: str) -> None:
    """Aprueba un préstamo pendiente."""
    prestamo["estado"] = "aprobado"
    prestamo["aprobadoPor"] = id_aprobador

def activar_prestamo(prestamo: Dict[str, Any]) -> None:
    """Activa un préstamo aprobado."""
    prestamo["estado"] = "activo"