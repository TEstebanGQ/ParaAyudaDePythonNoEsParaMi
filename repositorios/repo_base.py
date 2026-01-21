import json
import os
from typing import List, Dict, Any, Optional, Callable

def crear_archivo_si_no_existe(ruta_archivo: str) -> None:
    """Crea el archivo JSON si no existe."""
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
    
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump([], f)

def leer_datos(ruta_archivo: str) -> List[Dict[str, Any]]:
    """Lee todos los registros del archivo JSON."""
    crear_archivo_si_no_existe(ruta_archivo)
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_datos(ruta_archivo: str, datos: List[Dict[str, Any]]) -> None:
    """Guarda los datos en el archivo JSON con atomicidad."""
    crear_archivo_si_no_existe(ruta_archivo)
    
    # Guardar en archivo temporal primero
    ruta_temp = ruta_archivo + '.tmp'
    with open(ruta_temp, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    # Reemplazar el archivo original
    os.replace(ruta_temp, ruta_archivo)

def crear(ruta_archivo: str, registro: Dict[str, Any]) -> bool:
    """Crea un nuevo registro."""
    datos = leer_datos(ruta_archivo)
    
    # Verificar que no exista el ID
    if any(r.get("id") == registro.get("id") for r in datos):
        return False
    
    datos.append(registro)
    guardar_datos(ruta_archivo, datos)
    return True

def obtener_por_id(ruta_archivo: str, id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un registro por su ID."""
    datos = leer_datos(ruta_archivo)
    for registro in datos:
        if registro.get("id") == id:
            return registro
    return None

def obtener_todos(ruta_archivo: str) -> List[Dict[str, Any]]:
    """Obtiene todos los registros."""
    return leer_datos(ruta_archivo)

def actualizar(ruta_archivo: str, id: str, registro_actualizado: Dict[str, Any]) -> bool:
    """Actualiza un registro existente."""
    datos = leer_datos(ruta_archivo)
    
    for i, registro in enumerate(datos):
        if registro.get("id") == id:
            datos[i] = registro_actualizado
            guardar_datos(ruta_archivo, datos)
            return True
    
    return False

def eliminar(ruta_archivo: str, id: str) -> bool:
    """Elimina un registro por su ID."""
    datos = leer_datos(ruta_archivo)
    datos_filtrados = [r for r in datos if r.get("id") != id]
    
    if len(datos) == len(datos_filtrados):
        return False
    
    guardar_datos(ruta_archivo, datos_filtrados)
    return True

def buscar(ruta_archivo: str, criterio: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """Busca registros que cumplan un criterio."""
    datos = leer_datos(ruta_archivo)
    return [r for r in datos if criterio(r)]