"""
Módulo de reportes y consultas
Genera estadísticas e informes del sistema
"""

from modulos.persistencia import cargar_datos
from modulos.logger import registrar_error
from modulos.herramientas import listar_herramientas
from modulos.prestamos import listar_prestamos

def herramientas_stock_bajo(limite=3):
    """
    Obtiene herramientas con stock bajo
    
    Args:
        limite (int): Cantidad mínima para considerar stock bajo
    
    Returns:
        list: Herramientas con stock bajo
    """
    try:
        herramientas = listar_herramientas(solo_activas=True)
        stock_bajo = []
        
        for herramienta in herramientas:
            if herramienta['cantidad_disponible'] <= limite:
                stock_bajo.append({
                    'id': herramienta['id'],
                    'nombre': herramienta['nombre'],
                    'categoria': herramienta['categoria'],
                    'cantidad_disponible': herramienta['cantidad_disponible'],
                    'cantidad_total': herramienta['cantidad_total']
                })
        
        return stock_bajo
    except Exception as e:
        registrar_error('herramientas_stock_bajo', e)
        return []

def prestamos_activos():
    """
    Obtiene todos los préstamos activos
    
    Returns:
        list: Préstamos activos con información completa
    """
    try:
        from modulos.usuarios import buscar_usuario_por_id
        from modulos.herramientas import buscar_herramienta_por_id
        
        prestamos = listar_prestamos(filtro_estado='activo')
        resultado = []
        
        for prestamo in prestamos:
            usuario = buscar_usuario_por_id(prestamo['id_usuario'])
            herramienta = buscar_herramienta_por_id(prestamo['id_herramienta'])
            
            if usuario and herramienta:
                resultado.append({
                    'id_prestamo': prestamo['id'],
                    'usuario': f"{usuario['nombres']} {usuario['apellidos']}",
                    'herramienta': herramienta['nombre'],
                    'cantidad': prestamo['cantidad'],
                    'fecha_inicio': prestamo['fecha_inicio'],
                    'fecha_devolucion_estimada': prestamo['fecha_devolucion_estimada'],
                    'observaciones': prestamo['observaciones']
                })
        
        return resultado
    except Exception as e:
        registrar_error('prestamos_activos', e)
        return []

def prestamos_vencidos():
    """
    Obtiene todos los préstamos vencidos
    
    Returns:
        list: Préstamos vencidos con información completa
    """
    try:
        from modulos.usuarios import buscar_usuario_por_id
        from modulos.herramientas import buscar_herramienta_por_id
        
        prestamos = listar_prestamos(filtro_estado='vencido')
        resultado = []
        
        for prestamo in prestamos:
            usuario = buscar_usuario_por_id(prestamo['id_usuario'])
            herramienta = buscar_herramienta_por_id(prestamo['id_herramienta'])
            
            if usuario and herramienta:
                resultado.append({
                    'id_prestamo': prestamo['id'],
                    'usuario': f"{usuario['nombres']} {usuario['apellidos']}",
                    'telefono': usuario['telefono'],
                    'herramienta': herramienta['nombre'],
                    'cantidad': prestamo['cantidad'],
                    'fecha_devolucion_estimada': prestamo['fecha_devolucion_estimada']
                })
        
        return resultado
    except Exception as e:
        registrar_error('prestamos_vencidos', e)
        return []

def historial_prestamos_usuario(id_usuario):
    """
    Obtiene el historial completo de préstamos de un usuario
    
    Args:
        id_usuario (int): ID del usuario
    
    Returns:
        list: Historial de préstamos
    """
    try:
        from modulos.prestamos import buscar_prestamos_por_usuario
        from modulos.herramientas import buscar_herramienta_por_id
        
        prestamos = buscar_prestamos_por_usuario(id_usuario)
        resultado = []
        
        for prestamo in prestamos:
            herramienta = buscar_herramienta_por_id(prestamo['id_herramienta'])
            
            if herramienta:
                resultado.append({
                    'id_prestamo': prestamo['id'],
                    'herramienta': herramienta['nombre'],
                    'cantidad': prestamo['cantidad'],
                    'fecha_inicio': prestamo['fecha_inicio'],
                    'fecha_devolucion_estimada': prestamo['fecha_devolucion_estimada'],
                    'fecha_devolucion_real': prestamo.get('fecha_devolucion_real', 'No devuelto'),
                    'estado': prestamo['estado']
                })
        
        return resultado
    except Exception as e:
        registrar_error('historial_prestamos_usuario', e)
        return []

def herramientas_mas_solicitadas(top=5):
    """
    Obtiene las herramientas más solicitadas
    
    Args:
        top (int): Número de herramientas a mostrar
    
    Returns:
        list: Herramientas ordenadas por popularidad
    """
    try:
        herramientas = listar_herramientas(solo_activas=True)
        
        # Ordenar por veces solicitada
        herramientas_ordenadas = sorted(
            herramientas,
            key=lambda h: h.get('veces_solicitada', 0),
            reverse=True
        )
        
        resultado = []
        for herramienta in herramientas_ordenadas[:top]:
            resultado.append({
                'id': herramienta['id'],
                'nombre': herramienta['nombre'],
                'categoria': herramienta['categoria'],
                'veces_solicitada': herramienta.get('veces_solicitada', 0),
                'cantidad_disponible': herramienta['cantidad_disponible']
            })
        
        return resultado
    except Exception as e:
        registrar_error('herramientas_mas_solicitadas', e)
        return []

def usuarios_mas_activos(top=5):
    """
    Obtiene los usuarios que más herramientas han solicitado
    
    Args:
        top (int): Número de usuarios a mostrar
    
    Returns:
        list: Usuarios ordenados por número de préstamos
    """
    try:
        from modulos.usuarios import listar_usuarios
        from modulos.prestamos import buscar_prestamos_por_usuario
        
        usuarios = listar_usuarios(solo_activos=True)
        usuarios_con_conteo = []
        
        for usuario in usuarios:
            prestamos = buscar_prestamos_por_usuario(usuario['id'])
            total_prestamos = len(prestamos)
            
            if total_prestamos > 0:
                usuarios_con_conteo.append({
                    'id': usuario['id'],
                    'nombre': f"{usuario['nombres']} {usuario['apellidos']}",
                    'total_prestamos': total_prestamos,
                    'telefono': usuario['telefono']
                })
        
        # Ordenar por total de préstamos
        usuarios_ordenados = sorted(
            usuarios_con_conteo,
            key=lambda u: u['total_prestamos'],
            reverse=True
        )
        
        return usuarios_ordenados[:top]
    except Exception as e:
        registrar_error('usuarios_mas_activos', e)
        return []

def resumen_general():
    """
    Obtiene un resumen general del sistema
    
    Returns:
        dict: Resumen con estadísticas generales
    """
    try:
        from modulos.usuarios import listar_usuarios
        
        herramientas = listar_herramientas(solo_activas=True)
        usuarios = listar_usuarios(solo_activos=True)
        prestamos_todos = listar_prestamos()
        
        total_herramientas_disponibles = sum(h['cantidad_disponible'] for h in herramientas)
        total_herramientas = sum(h['cantidad_total'] for h in herramientas)
        
        prestamos_act = [p for p in prestamos_todos if p['estado'] == 'activo']
        prestamos_venc = [p for p in prestamos_todos if p['estado'] == 'vencido']
        prestamos_dev = [p for p in prestamos_todos if p['estado'] == 'devuelto']
        
        return {
            'total_herramientas': len(herramientas),
            'total_unidades': total_herramientas,
            'unidades_disponibles': total_herramientas_disponibles,
            'unidades_prestadas': total_herramientas - total_herramientas_disponibles,
            'total_usuarios': len(usuarios),
            'prestamos_activos': len(prestamos_act),
            'prestamos_vencidos': len(prestamos_venc),
            'prestamos_devueltos': len(prestamos_dev),
            'total_prestamos': len(prestamos_todos)
        }
    except Exception as e:
        registrar_error('resumen_general', e)
        return {}

def quien_tiene_herramienta(id_herramienta):
    """
    Muestra quién tiene actualmente una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
    
    Returns:
        list: Lista de usuarios que tienen la herramienta
    """
    try:
        from modulos.prestamos import buscar_prestamos_por_herramienta
        from modulos.usuarios import buscar_usuario_por_id
        
        prestamos = buscar_prestamos_por_herramienta(id_herramienta)
        prestamos_activos = [p for p in prestamos if p['estado'] == 'activo']
        
        resultado = []
        for prestamo in prestamos_activos:
            usuario = buscar_usuario_por_id(prestamo['id_usuario'])
            if usuario:
                resultado.append({
                    'usuario': f"{usuario['nombres']} {usuario['apellidos']}",
                    'telefono': usuario['telefono'],
                    'direccion': usuario['direccion'],
                    'cantidad': prestamo['cantidad'],
                    'fecha_devolucion_estimada': prestamo['fecha_devolucion_estimada']
                })
        
        return resultado
    except Exception as e:
        registrar_error('quien_tiene_herramienta', e)
        return []