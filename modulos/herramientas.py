"""
Módulo de gestión de herramientas
Maneja el inventario de herramientas de la comunidad
"""

from modulos.persistencia import cargar_datos, guardar_datos, generar_id
from modulos.logger import registrar_info, registrar_error, registrar_warning

ARCHIVO_HERRAMIENTAS = 'datos/herramientas.json'

def crear_herramienta(nombre, categoria, cantidad, estado='activa', valor_estimado=0.0):
    """
    Crea una nueva herramienta en el inventario
    
    Args:
        nombre (str): Nombre de la herramienta
        categoria (str): Categoría (construcción, jardinería, etc.)
        cantidad (int): Cantidad disponible
        estado (str): 'activa', 'en reparación', 'fuera de servicio'
        valor_estimado (float): Valor estimado en dinero
    
    Returns:
        dict: Herramienta creada o None si hubo error
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        
        # Validar estado
        estados_validos = ['activa', 'en reparación', 'fuera de servicio']
        if estado not in estados_validos:
            registrar_warning(f"Estado inválido: {estado}")
            return None
        
        # Validar cantidad
        if cantidad < 0:
            registrar_warning("La cantidad no puede ser negativa")
            return None
        
        nuevo_id = generar_id(herramientas)
        
        nueva_herramienta = {
            'id': nuevo_id,
            'nombre': nombre.strip(),
            'categoria': categoria.strip(),
            'cantidad_total': cantidad,
            'cantidad_disponible': cantidad,
            'estado': estado,
            'valor_estimado': float(valor_estimado),
            'activa': True,
            'veces_solicitada': 0
        }
        
        herramientas.append(nueva_herramienta)
        guardar_datos(ARCHIVO_HERRAMIENTAS, herramientas)
        registrar_info(f'Herramienta creada: {nombre} (ID: {nuevo_id}, Cantidad: {cantidad})')
        
        return nueva_herramienta
    except Exception as e:
        registrar_error('crear_herramienta', e)
        return None

def listar_herramientas(solo_activas=True):
    """
    Lista todas las herramientas del inventario
    
    Args:
        solo_activas (bool): Si es True, solo muestra herramientas activas
    
    Returns:
        list: Lista de herramientas
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        if solo_activas:
            return [h for h in herramientas if h.get('activa', True)]
        return herramientas
    except Exception as e:
        registrar_error('listar_herramientas', e)
        return []

def buscar_herramienta_por_id(id_herramienta):
    """
    Busca una herramienta por su ID
    
    Args:
        id_herramienta (int): ID de la herramienta
    
    Returns:
        dict: Herramienta encontrada o None
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        for herramienta in herramientas:
            if herramienta['id'] == id_herramienta:
                return herramienta
        registrar_warning(f"Herramienta con ID {id_herramienta} no encontrada")
        return None
    except Exception as e:
        registrar_error('buscar_herramienta_por_id', e)
        return None

def buscar_herramientas_por_nombre(nombre):
    """
    Busca herramientas por nombre
    
    Args:
        nombre (str): Nombre o parte del nombre
    
    Returns:
        list: Lista de herramientas que coinciden
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        nombre_lower = nombre.lower()
        resultados = []
        
        for herramienta in herramientas:
            if nombre_lower in herramienta['nombre'].lower():
                resultados.append(herramienta)
        
        return resultados
    except Exception as e:
        registrar_error('buscar_herramientas_por_nombre', e)
        return []

def buscar_herramientas_por_categoria(categoria):
    """
    Busca herramientas por categoría
    
    Args:
        categoria (str): Categoría a buscar
    
    Returns:
        list: Lista de herramientas de esa categoría
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        categoria_lower = categoria.lower()
        return [h for h in herramientas if h['categoria'].lower() == categoria_lower]
    except Exception as e:
        registrar_error('buscar_herramientas_por_categoria', e)
        return []

def actualizar_herramienta(id_herramienta, **kwargs):
    """
    Actualiza los datos de una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
        **kwargs: Campos a actualizar
    
    Returns:
        bool: True si se actualizó correctamente
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        
        for herramienta in herramientas:
            if herramienta['id'] == id_herramienta:
                campos_permitidos = ['nombre', 'categoria', 'estado', 'valor_estimado']
                for campo, valor in kwargs.items():
                    if campo in campos_permitidos:
                        herramienta[campo] = valor
                
                guardar_datos(ARCHIVO_HERRAMIENTAS, herramientas)
                registrar_info(f'Herramienta ID {id_herramienta} actualizada')
                return True
        
        registrar_warning(f"No se pudo actualizar: Herramienta ID {id_herramienta} no encontrada")
        return False
    except Exception as e:
        registrar_error('actualizar_herramienta', e)
        return False

def eliminar_herramienta(id_herramienta):
    """
    Marca una herramienta como inactiva
    
    Args:
        id_herramienta (int): ID de la herramienta
    
    Returns:
        bool: True si se eliminó correctamente
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        
        for herramienta in herramientas:
            if herramienta['id'] == id_herramienta:
                herramienta['activa'] = False
                guardar_datos(ARCHIVO_HERRAMIENTAS, herramientas)
                registrar_info(f'Herramienta ID {id_herramienta} marcada como inactiva')
                return True
        
        registrar_warning(f"No se pudo eliminar: Herramienta ID {id_herramienta} no encontrada")
        return False
    except Exception as e:
        registrar_error('eliminar_herramienta', e)
        return False

def ajustar_cantidad_disponible(id_herramienta, cantidad_cambio):
    """
    Ajusta la cantidad disponible de una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
        cantidad_cambio (int): Cantidad a sumar (positivo) o restar (negativo)
    
    Returns:
        bool: True si se ajustó correctamente
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        
        for herramienta in herramientas:
            if herramienta['id'] == id_herramienta:
                nueva_cantidad = herramienta['cantidad_disponible'] + cantidad_cambio
                
                # Validar que no sea negativa
                if nueva_cantidad < 0:
                    registrar_warning(f"No se puede ajustar: cantidad resultante sería negativa")
                    return False
                
                # Validar que no exceda el total
                if nueva_cantidad > herramienta['cantidad_total']:
                    registrar_warning(f"No se puede ajustar: excede cantidad total")
                    return False
                
                herramienta['cantidad_disponible'] = nueva_cantidad
                guardar_datos(ARCHIVO_HERRAMIENTAS, herramientas)
                registrar_info(f'Cantidad ajustada para herramienta ID {id_herramienta}: {cantidad_cambio}')
                return True
        
        registrar_warning(f"Herramienta ID {id_herramienta} no encontrada")
        return False
    except Exception as e:
        registrar_error('ajustar_cantidad_disponible', e)
        return False

def verificar_disponibilidad(id_herramienta, cantidad_requerida):
    """
    Verifica si hay suficiente cantidad disponible de una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
        cantidad_requerida (int): Cantidad que se necesita
    
    Returns:
        bool: True si hay disponibilidad
    """
    try:
        herramienta = buscar_herramienta_por_id(id_herramienta)
        if not herramienta:
            return False
        
        if herramienta['estado'] != 'activa':
            registrar_warning(f"Herramienta ID {id_herramienta} no está activa")
            return False
        
        return herramienta['cantidad_disponible'] >= cantidad_requerida
    except Exception as e:
        registrar_error('verificar_disponibilidad', e)
        return False

def incrementar_veces_solicitada(id_herramienta):
    """
    Incrementa el contador de veces que se ha solicitado una herramienta
    
    Args:
        id_herramienta (int): ID de la herramienta
    
    Returns:
        bool: True si se incrementó correctamente
    """
    try:
        herramientas = cargar_datos(ARCHIVO_HERRAMIENTAS)
        
        for herramienta in herramientas:
            if herramienta['id'] == id_herramienta:
                herramienta['veces_solicitada'] = herramienta.get('veces_solicitada', 0) + 1
                guardar_datos(ARCHIVO_HERRAMIENTAS, herramientas)
                return True
        return False
    except Exception as e:
        registrar_error('incrementar_veces_solicitada', e)
        return False