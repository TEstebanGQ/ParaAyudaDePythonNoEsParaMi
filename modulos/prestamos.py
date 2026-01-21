"""
Módulo de gestión de préstamos
Maneja los préstamos de herramientas a vecinos
"""

from datetime import datetime, timedelta
from modulos.persistencia import cargar_datos, guardar_datos, generar_id
from modulos.logger import registrar_info, registrar_error, registrar_warning
from modulos.herramientas import verificar_disponibilidad, ajustar_cantidad_disponible, incrementar_veces_solicitada
from modulos.usuarios import buscar_usuario_por_id

ARCHIVO_PRESTAMOS = 'datos/prestamos.json'
ARCHIVO_SOLICITUDES = 'datos/solicitudes.json'

def crear_prestamo(id_usuario, id_herramienta, cantidad, dias_prestamo=7, observaciones=''):
    """
    Crea un nuevo préstamo de herramienta
    
    Args:
        id_usuario (int): ID del usuario que solicita
        id_herramienta (int): ID de la herramienta
        cantidad (int): Cantidad a prestar
        dias_prestamo (int): Días de duración del préstamo
        observaciones (str): Observaciones adicionales
    
    Returns:
        dict: Préstamo creado o None si hubo error
    """
    try:
        # Verificar que el usuario existe
        usuario = buscar_usuario_por_id(id_usuario)
        if not usuario:
            registrar_warning(f"Usuario ID {id_usuario} no encontrado")
            return None
        
        # Verificar disponibilidad
        if not verificar_disponibilidad(id_herramienta, cantidad):
            registrar_warning(f"No hay suficiente cantidad disponible de herramienta ID {id_herramienta}")
            return None
        
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        nuevo_id = generar_id(prestamos)
        
        fecha_inicio = datetime.now()
        fecha_devolucion_estimada = fecha_inicio + timedelta(days=dias_prestamo)
        
        nuevo_prestamo = {
            'id': nuevo_id,
            'id_usuario': id_usuario,
            'id_herramienta': id_herramienta,
            'cantidad': cantidad,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_devolucion_estimada': fecha_devolucion_estimada.strftime('%Y-%m-%d'),
            'fecha_devolucion_real': None,
            'estado': 'activo',  # activo, devuelto, vencido
            'observaciones': observaciones.strip()
        }
        
        # Ajustar cantidad disponible de la herramienta
        if ajustar_cantidad_disponible(id_herramienta, -cantidad):
            prestamos.append(nuevo_prestamo)
            guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
            incrementar_veces_solicitada(id_herramienta)
            registrar_info(f'Préstamo creado: ID {nuevo_id}, Usuario: {id_usuario}, Herramienta: {id_herramienta}')
            return nuevo_prestamo
        else:
            registrar_error('crear_prestamo', 'No se pudo ajustar la cantidad disponible')
            return None
    except Exception as e:
        registrar_error('crear_prestamo', e)
        return None

def devolver_prestamo(id_prestamo, observaciones_devolucion=''):
    """
    Registra la devolución de un préstamo
    
    Args:
        id_prestamo (int): ID del préstamo
        observaciones_devolucion (str): Observaciones de la devolución
    
    Returns:
        bool: True si se devolvió correctamente
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        
        for prestamo in prestamos:
            if prestamo['id'] == id_prestamo:
                if prestamo['estado'] != 'activo':
                    registrar_warning(f"Préstamo ID {id_prestamo} no está activo")
                    return False
                
                # Actualizar estado del préstamo
                prestamo['estado'] = 'devuelto'
                prestamo['fecha_devolucion_real'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if observaciones_devolucion:
                    prestamo['observaciones'] += f" | Devolución: {observaciones_devolucion}"
                
                # Restaurar cantidad disponible
                if ajustar_cantidad_disponible(prestamo['id_herramienta'], prestamo['cantidad']):
                    guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
                    registrar_info(f'Préstamo ID {id_prestamo} devuelto exitosamente')
                    return True
                else:
                    registrar_error('devolver_prestamo', 'No se pudo restaurar cantidad disponible')
                    return False
        
        registrar_warning(f"Préstamo ID {id_prestamo} no encontrado")
        return False
    except Exception as e:
        registrar_error('devolver_prestamo', e)
        return False

def listar_prestamos(filtro_estado=None):
    """
    Lista préstamos con filtro opcional
    
    Args:
        filtro_estado (str): 'activo', 'devuelto', 'vencido' o None para todos
    
    Returns:
        list: Lista de préstamos
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        
        # Actualizar estados de préstamos vencidos
        actualizar_estados_vencidos()
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)  # Recargar después de actualizar
        
        if filtro_estado:
            return [p for p in prestamos if p['estado'] == filtro_estado]
        return prestamos
    except Exception as e:
        registrar_error('listar_prestamos', e)
        return []

def buscar_prestamo_por_id(id_prestamo):
    """
    Busca un préstamo por su ID
    
    Args:
        id_prestamo (int): ID del préstamo
    
    Returns:
        dict: Préstamo encontrado o None
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        for prestamo in prestamos:
            if prestamo['id'] == id_prestamo:
                return prestamo
        return None
    except Exception as e:
        registrar_error('buscar_prestamo_por_id', e)
        return None

def buscar_prestamos_por_usuario(id_usuario):
    """
    Busca todos los préstamos de un usuario
    
    Args:
        id_usuario (int): ID del usuario
    
    Returns:
        list: Lista de préstamos del usuario
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        return [p for p in prestamos if p['id_usuario'] == id_usuario]
    except Exception as e:
        registrar_error('buscar_prestamos_por_usuario', e)
        return []

def buscar_prestamos_por_herramienta(id_herramienta):
    """
    Busca todos los préstamos de una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
    
    Returns:
        list: Lista de préstamos de la herramienta
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        return [p for p in prestamos if p['id_herramienta'] == id_herramienta]
    except Exception as e:
        registrar_error('buscar_prestamos_por_herramienta', e)
        return []

def actualizar_estados_vencidos():
    """
    Actualiza el estado de préstamos que están vencidos
    
    Returns:
        int: Número de préstamos actualizados
    """
    try:
        prestamos = cargar_datos(ARCHIVO_PRESTAMOS)
        fecha_actual = datetime.now()
        actualizados = 0
        
        for prestamo in prestamos:
            if prestamo['estado'] == 'activo':
                fecha_estimada = datetime.strptime(prestamo['fecha_devolucion_estimada'], '%Y-%m-%d')
                if fecha_actual > fecha_estimada:
                    prestamo['estado'] = 'vencido'
                    actualizados += 1
        
        if actualizados > 0:
            guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
            registrar_info(f'{actualizados} préstamos marcados como vencidos')
        
        return actualizados
    except Exception as e:
        registrar_error('actualizar_estados_vencidos', e)
        return 0

# Sistema de solicitudes para usuarios normales
def crear_solicitud(id_usuario, id_herramienta, cantidad, dias_prestamo=7, justificacion=''):
    """
    Crea una solicitud de préstamo que debe ser aprobada por un administrador
    
    Args:
        id_usuario (int): ID del usuario solicitante
        id_herramienta (int): ID de la herramienta
        cantidad (int): Cantidad solicitada
        dias_prestamo (int): Días de préstamo solicitados
        justificacion (str): Justificación de la solicitud
    
    Returns:
        dict: Solicitud creada o None
    """
    try:
        solicitudes = cargar_datos(ARCHIVO_SOLICITUDES)
        nuevo_id = generar_id(solicitudes)
        
        nueva_solicitud = {
            'id': nuevo_id,
            'id_usuario': id_usuario,
            'id_herramienta': id_herramienta,
            'cantidad': cantidad,
            'dias_prestamo': dias_prestamo,
            'justificacion': justificacion.strip(),
            'fecha_solicitud': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estado': 'pendiente',  # pendiente, aprobada, rechazada
            'id_administrador': None,
            'fecha_respuesta': None,
            'observaciones_admin': ''
        }
        
        solicitudes.append(nueva_solicitud)
        guardar_datos(ARCHIVO_SOLICITUDES, solicitudes)
        registrar_info(f'Solicitud creada: ID {nuevo_id}, Usuario: {id_usuario}')
        
        return nueva_solicitud
    except Exception as e:
        registrar_error('crear_solicitud', e)
        return None

def listar_solicitudes(filtro_estado=None):
    """
    Lista solicitudes con filtro opcional
    
    Args:
        filtro_estado (str): 'pendiente', 'aprobada', 'rechazada' o None
    
    Returns:
        list: Lista de solicitudes
    """
    try:
        solicitudes = cargar_datos(ARCHIVO_SOLICITUDES)
        if filtro_estado:
            return [s for s in solicitudes if s['estado'] == filtro_estado]
        return solicitudes
    except Exception as e:
        registrar_error('listar_solicitudes', e)
        return []

def aprobar_solicitud(id_solicitud, id_administrador, observaciones=''):
    """
    Aprueba una solicitud y crea el préstamo automáticamente
    
    Args:
        id_solicitud (int): ID de la solicitud
        id_administrador (int): ID del administrador que aprueba
        observaciones (str): Observaciones del administrador
    
    Returns:
        dict: Préstamo creado o None
    """
    try:
        solicitudes = cargar_datos(ARCHIVO_SOLICITUDES)
        
        for solicitud in solicitudes:
            if solicitud['id'] == id_solicitud:
                if solicitud['estado'] != 'pendiente':
                    registrar_warning(f"Solicitud ID {id_solicitud} ya fue procesada")
                    return None
                
                # Crear el préstamo
                prestamo = crear_prestamo(
                    solicitud['id_usuario'],
                    solicitud['id_herramienta'],
                    solicitud['cantidad'],
                    solicitud['dias_prestamo'],
                    f"Aprobado por admin ID {id_administrador}. {observaciones}"
                )
                
                if prestamo:
                    # Actualizar solicitud
                    solicitud['estado'] = 'aprobada'
                    solicitud['id_administrador'] = id_administrador
                    solicitud['fecha_respuesta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    solicitud['observaciones_admin'] = observaciones
                    guardar_datos(ARCHIVO_SOLICITUDES, solicitudes)
                    registrar_info(f'Solicitud ID {id_solicitud} aprobada')
                    return prestamo
                
                return None
        
        registrar_warning(f"Solicitud ID {id_solicitud} no encontrada")
        return None
    except Exception as e:
        registrar_error('aprobar_solicitud', e)
        return None

def rechazar_solicitud(id_solicitud, id_administrador, motivo=''):
    """
    Rechaza una solicitud de préstamo
    
    Args:
        id_solicitud (int): ID de la solicitud
        id_administrador (int): ID del administrador que rechaza
        motivo (str): Motivo del rechazo
    
    Returns:
        bool: True si se rechazó correctamente
    """
    try:
        solicitudes = cargar_datos(ARCHIVO_SOLICITUDES)
        
        for solicitud in solicitudes:
            if solicitud['id'] == id_solicitud:
                if solicitud['estado'] != 'pendiente':
                    registrar_warning(f"Solicitud ID {id_solicitud} ya fue procesada")
                    return False
                
                solicitud['estado'] = 'rechazada'
                solicitud['id_administrador'] = id_administrador
                solicitud['fecha_respuesta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                solicitud['observaciones_admin'] = motivo
                guardar_datos(ARCHIVO_SOLICITUDES, solicitudes)
                registrar_info(f'Solicitud ID {id_solicitud} rechazada')
                return True
        
        registrar_warning(f"Solicitud ID {id_solicitud} no encontrada")
        return False
    except Exception as e:
        registrar_error('rechazar_solicitud', e)
        return False