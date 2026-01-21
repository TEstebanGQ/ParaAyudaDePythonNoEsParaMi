"""
Módulo de gestión de usuarios del sistema
Maneja el CRUD de vecinos y administradores
"""

from modulos.persistencia import cargar_datos, guardar_datos, generar_id
from modulos.logger import registrar_info, registrar_error, registrar_warning

ARCHIVO_USUARIOS = 'datos/usuarios.json'

def crear_usuario(nombres, apellidos, telefono, direccion, tipo_usuario='residente', password='1234'):
    """
    Crea un nuevo usuario en el sistema
    
    Args:
        nombres (str): Nombres del usuario
        apellidos (str): Apellidos del usuario
        telefono (str): Teléfono de contacto
        direccion (str): Dirección de residencia
        tipo_usuario (str): 'residente' o 'administrador'
        password (str): Contraseña del usuario (por defecto '1234')
    
    Returns:
        dict: Usuario creado o None si hubo error
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        
        # Validar tipo de usuario
        if tipo_usuario not in ['residente', 'administrador']:
            registrar_warning(f"Tipo de usuario inválido: {tipo_usuario}")
            return None
        
        nuevo_id = generar_id(usuarios)
        
        nuevo_usuario = {
            'id': nuevo_id,
            'nombres': nombres.strip(),
            'apellidos': apellidos.strip(),
            'telefono': telefono.strip(),
            'direccion': direccion.strip(),
            'tipo_usuario': tipo_usuario,
            'password': password,
            'activo': True
        }
        
        usuarios.append(nuevo_usuario)
        guardar_datos(ARCHIVO_USUARIOS, usuarios)
        registrar_info(f'Usuario creado: {nombres} {apellidos} (ID: {nuevo_id}, Tipo: {tipo_usuario})')
        
        return nuevo_usuario
    except Exception as e:
        registrar_error('crear_usuario', e)
        return None

def listar_usuarios(solo_activos=True):
    """
    Lista todos los usuarios del sistema
    
    Args:
        solo_activos (bool): Si es True, solo muestra usuarios activos
    
    Returns:
        list: Lista de usuarios
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        if solo_activos:
            return [u for u in usuarios if u.get('activo', True)]
        return usuarios
    except Exception as e:
        registrar_error('listar_usuarios', e)
        return []

def buscar_usuario_por_id(id_usuario):
    """
    Busca un usuario por su ID
    
    Args:
        id_usuario (int): ID del usuario a buscar
    
    Returns:
        dict: Usuario encontrado o None
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        for usuario in usuarios:
            if usuario['id'] == id_usuario:
                return usuario
        registrar_warning(f"Usuario con ID {id_usuario} no encontrado")
        return None
    except Exception as e:
        registrar_error('buscar_usuario_por_id', e)
        return None

def buscar_usuarios_por_nombre(nombre):
    """
    Busca usuarios que coincidan con el nombre
    
    Args:
        nombre (str): Nombre o apellido a buscar
    
    Returns:
        list: Lista de usuarios que coinciden
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        nombre_lower = nombre.lower()
        resultados = []
        
        for usuario in usuarios:
            if (nombre_lower in usuario['nombres'].lower() or 
                nombre_lower in usuario['apellidos'].lower()):
                resultados.append(usuario)
        
        return resultados
    except Exception as e:
        registrar_error('buscar_usuarios_por_nombre', e)
        return []

def actualizar_usuario(id_usuario, **kwargs):
    """
    Actualiza los datos de un usuario
    
    Args:
        id_usuario (int): ID del usuario a actualizar
        **kwargs: Campos a actualizar (nombres, apellidos, telefono, direccion, tipo_usuario)
    
    Returns:
        bool: True si se actualizó correctamente
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        
        for usuario in usuarios:
            if usuario['id'] == id_usuario:
                # Actualizar solo los campos proporcionados
                campos_permitidos = ['nombres', 'apellidos', 'telefono', 'direccion', 'tipo_usuario', 'password']
                for campo, valor in kwargs.items():
                    if campo in campos_permitidos:
                        usuario[campo] = valor
                
                guardar_datos(ARCHIVO_USUARIOS, usuarios)
                registrar_info(f'Usuario ID {id_usuario} actualizado')
                return True
        
        registrar_warning(f"No se pudo actualizar: Usuario ID {id_usuario} no encontrado")
        return False
    except Exception as e:
        registrar_error('actualizar_usuario', e)
        return False

def eliminar_usuario(id_usuario):
    """
    Marca un usuario como inactivo (eliminación lógica)
    
    Args:
        id_usuario (int): ID del usuario a eliminar
    
    Returns:
        bool: True si se eliminó correctamente
    """
    try:
        usuarios = cargar_datos(ARCHIVO_USUARIOS)
        
        for usuario in usuarios:
            if usuario['id'] == id_usuario:
                usuario['activo'] = False
                guardar_datos(ARCHIVO_USUARIOS, usuarios)
                registrar_info(f'Usuario ID {id_usuario} marcado como inactivo')
                return True
        
        registrar_warning(f"No se pudo eliminar: Usuario ID {id_usuario} no encontrado")
        return False
    except Exception as e:
        registrar_error('eliminar_usuario', e)
        return False

def autenticar_usuario(id_usuario, password):
    """
    Autentica un usuario verificando su contraseña
    
    Args:
        id_usuario (int): ID del usuario
        password (str): Contraseña del usuario
    
    Returns:
        dict: Usuario autenticado o None si falla
    """
    try:
        usuario = buscar_usuario_por_id(id_usuario)
        if usuario and usuario.get('password') == password and usuario.get('activo', True):
            registrar_info(f"Usuario ID {id_usuario} autenticado correctamente")
            return usuario
        registrar_warning(f"Fallo de autenticación para usuario ID {id_usuario}")
        return None
    except Exception as e:
        registrar_error('autenticar_usuario', e)
        return None