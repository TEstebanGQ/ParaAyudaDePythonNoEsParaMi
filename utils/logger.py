import os
from datetime import datetime
from typing import Literal

NivelLog = Literal["INFO", "ADVERTENCIA", "ERROR"]

def crear_directorio_logs(ruta_log: str) -> None:
    """Crea el directorio de logs si no existe."""
    directorio = os.path.dirname(ruta_log)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

def registrar_log(ruta_log: str, nivel: NivelLog, mensaje: str, 
                 usuario: str = "SISTEMA") -> None:
    """Registra un evento en el archivo de log."""
    crear_directorio_logs(ruta_log)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{timestamp}] [{nivel}] [{usuario}] {mensaje}\n"
    
    with open(ruta_log, 'a', encoding='utf-8') as f:
        f.write(linea_log)

def log_info(ruta_log: str, mensaje: str, usuario: str = "SISTEMA") -> None:
    """Registra un mensaje informativo."""
    registrar_log(ruta_log, "INFO", mensaje, usuario)

def log_advertencia(ruta_log: str, mensaje: str, usuario: str = "SISTEMA") -> None:
    """Registra una advertencia."""
    registrar_log(ruta_log, "ADVERTENCIA", mensaje, usuario)

def log_error(ruta_log: str, mensaje: str, usuario: str = "SISTEMA") -> None:
    """Registra un error."""
    registrar_log(ruta_log, "ERROR", mensaje, usuario)

def leer_logs(ruta_log: str, ultimas_lineas: int = 50) -> List[str]:
    """Lee las últimas líneas del log."""
    crear_directorio_logs(ruta_log)
    
    if not os.path.exists(ruta_log):
        return []
    
    with open(ruta_log, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    return lineas[-ultimas_lineas:]