from datetime import datetime
from typing import Dict, Any

def crear_herramienta(id: str, nombre: str, categoria: str, 
                     cantidad_total: int, valor_estimado: float,
                     estado: str = "activa", descripcion: str = "") -> Dict[str, Any]:
    """Crea una estructura de datos para una herramienta."""
    return {
        "id": id,
        "nombre": nombre.strip().title(),
        "categoria": categoria,
        "cantidadDisponible": cantidad_total,
        "cantidadTotal": cantidad_total,
        "estado": estado,
        "valorEstimado": valor_estimado,
        "fechaRegistro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "descripcion": descripcion
    }

def validar_herramienta(herramienta: Dict[str, Any]) -> tuple[bool, str]:
    """Valida los datos de una herramienta."""
    if not herramienta.get("nombre") or len(herramienta["nombre"]) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if herramienta.get("cantidadTotal", 0) < 1:
        return False, "La cantidad total debe ser al menos 1"
    
    if herramienta.get("cantidadDisponible", 0) < 0:
        return False, "La cantidad disponible no puede ser negativa"
    
    if herramienta.get("cantidadDisponible", 0) > herramienta.get("cantidadTotal", 0):
        return False, "La cantidad disponible no puede superar la total"
    
    if herramienta.get("valorEstimado", 0) < 0:
        return False, "El valor estimado no puede ser negativo"
    
    return True, "Válida"

def esta_disponible(herramienta: Dict[str, Any]) -> bool:
    """Verifica si la herramienta está disponible para préstamo."""
    return (herramienta.get("estado") == "activa" and 
            herramienta.get("cantidadDisponible", 0) > 0)

def reducir_stock(herramienta: Dict[str, Any], cantidad: int) -> tuple[bool, str]:
    """Reduce el stock disponible de una herramienta."""
    if cantidad > herramienta.get("cantidadDisponible", 0):
        return False, f"Stock insuficiente. Disponible: {herramienta['cantidadDisponible']}"
    
    herramienta["cantidadDisponible"] -= cantidad
    return True, "Stock reducido correctamente"

def aumentar_stock(herramienta: Dict[str, Any], cantidad: int) -> tuple[bool, str]:
    """Aumenta el stock disponible de una herramienta."""
    nueva_cantidad = herramienta.get("cantidadDisponible", 0) + cantidad
    
    if nueva_cantidad > herramienta.get("cantidadTotal", 0):
        return False, "No se puede exceder la cantidad total"
    
    herramienta["cantidadDisponible"] = nueva_cantidad
    return True, "Stock aumentado correctamente"