"""
Módulo de registro de eventos y errores del sistema
Autor: Sistema de Gestión de Herramientas Comunitarias
"""

from datetime import datetime
import os

def registrar_evento(tipo, mensaje):
    """
    Registra un evento en el archivo de logs
    
    Args:
        tipo (str): Tipo de evento (INFO, ERROR, WARNING, SUCCESS)
        mensaje (str): Descripción del evento
    """
    # Crear carpeta logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Formato: [2024-01-21 10:30:45] INFO: Mensaje aquí
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea_log = f"[{timestamp}] {tipo}: {mensaje}\n"
    
    # Escribir en archivo
    try:
        with open('logs/eventos.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(linea_log)
    except Exception as e:
        print(f"Error al escribir en el log: {e}")

def registrar_error(funcion, error):
    """
    Registra un error específico con detalles
    
    Args:
        funcion (str): Nombre de la función donde ocurrió el error
        error (Exception): Objeto de excepción capturado
    """
    mensaje = f"Error en {funcion}: {str(error)}"
    registrar_evento('ERROR', mensaje)

def registrar_info(mensaje):
    """Atajo para registrar eventos informativos"""
    registrar_evento('INFO', mensaje)

def registrar_warning(mensaje):
    """Atajo para registrar advertencias"""
    registrar_evento('WARNING', mensaje)

def registrar_success(mensaje):
    """Atajo para registrar operaciones exitosas"""
    registrar_evento('SUCCESS', mensaje)