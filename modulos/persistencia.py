"""
Módulo de persistencia de datos
Maneja la carga y guardado de datos en formato JSON
"""

import json
import os
from modulos.logger import registrar_error, registrar_info

def inicializar_directorios():
    """Crea los directorios necesarios si no existen"""
    directorios = ['datos', 'logs']
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            registrar_info(f"Directorio '{directorio}' creado")

def cargar_datos(archivo):
    """
    Carga datos desde un archivo JSON
    
    Args:
        archivo (str): Ruta del archivo JSON
    
    Returns:
        list: Lista de datos cargados, vacía si el archivo no existe
    """
    try:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                registrar_info(f"Datos cargados desde {archivo}")
                return datos
        else:
            registrar_info(f"Archivo {archivo} no existe, retornando lista vacía")
            return []
    except json.JSONDecodeError as e:
        registrar_error('cargar_datos', f"Error al decodificar JSON de {archivo}: {e}")
        return []
    except Exception as e:
        registrar_error('cargar_datos', e)
        return []

def guardar_datos(archivo, datos):
    """
    Guarda datos en un archivo JSON
    
    Args:
        archivo (str): Ruta del archivo JSON
        datos (list): Datos a guardar
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        # Asegurar que el directorio existe
        directorio = os.path.dirname(archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        registrar_info(f"Datos guardados en {archivo}")
        return True
    except Exception as e:
        registrar_error('guardar_datos', e)
        return False

def generar_id(lista_datos):
    """
    Genera un nuevo ID basado en el máximo ID existente
    
    Args:
        lista_datos (list): Lista de diccionarios con campo 'id'
    
    Returns:
        int: Nuevo ID único
    """
    if not lista_datos:
        return 1
    return max([item['id'] for item in lista_datos], default=0) + 1