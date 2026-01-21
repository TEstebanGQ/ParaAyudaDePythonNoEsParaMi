"""
Sistema de Gestión de Herramientas Comunitarias
Programa principal con menús interactivos
"""

import os
import sys
from modulos.persistencia import inicializar_directorios
from modulos.logger import registrar_info
from modulos import usuarios, herramientas, prestamos, reportes

# Usuario actual en sesión
usuario_actual = None

def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    """Pausa hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def mostrar_encabezado(titulo):
    """Muestra un encabezado decorado"""
    print("\n" + "="*60)
    print(f"  {titulo}")
    print("="*60 + "\n")

def login():
    """Sistema de autenticación"""
    global usuario_actual
    
    limpiar_pantalla()
    mostrar_encabezado("INICIO DE SESIÓN")
    
    try:
        id_usuario = int(input("Ingrese su ID de usuario: "))
        password = input("Ingrese su contraseña: ")
        
        usuario = usuarios.autenticar_usuario(id_usuario, password)
        
        if usuario:
            usuario_actual = usuario
            print(f"\n✓ Bienvenido/a {usuario['nombres']} {usuario['apellidos']}")
            print(f"  Tipo de usuario: {usuario['tipo_usuario'].upper()}")
            pausa()
            return True
        else:
            print("\n✗ Credenciales incorrectas")
            pausa()
            return False
    except ValueError:
        print("\n✗ ID inválido")
        pausa()
        return False

# ==================== MENÚS DE ADMINISTRADOR ====================

def menu_admin_usuarios():
    """Menú de gestión de usuarios (solo admin)"""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE USUARIOS")
        print("1. Crear nuevo usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Actualizar usuario")
        print("5. Eliminar usuario")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            crear_usuario_interactivo()
        elif opcion == '2':
            listar_usuarios_interactivo()
        elif opcion == '3':
            buscar_usuario_interactivo()
        elif opcion == '4':
            actualizar_usuario_interactivo()
        elif opcion == '5':
            eliminar_usuario_interactivo()
        elif opcion == '0':
            break

def crear_usuario_interactivo():
    """Crea un usuario de forma interactiva"""
    limpiar_pantalla()
    mostrar_encabezado("CREAR NUEVO USUARIO")
    
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    
    print("\nTipo de usuario:")
    print("1. Residente")
    print("2. Administrador")
    tipo = input("Seleccione (1-2): ")
    tipo_usuario = 'administrador' if tipo == '2' else 'residente'
    
    password = input("Contraseña (Enter para usar '1234'): ") or '1234'
    
    usuario = usuarios.crear_usuario(nombres, apellidos, telefono, direccion, tipo_usuario, password)
    
    if usuario:
        print(f"\n✓ Usuario creado exitosamente")
        print(f"  ID: {usuario['id']}")
        print(f"  Nombre: {usuario['nombres']} {usuario['apellidos']}")
        print(f"  Tipo: {usuario['tipo_usuario']}")
    else:
        print("\n✗ Error al crear usuario")
    
    pausa()

def listar_usuarios_interactivo():
    """Lista todos los usuarios"""
    limpiar_pantalla()
    mostrar_encabezado("LISTA DE USUARIOS")
    
    lista = usuarios.listar_usuarios()
    
    if not lista:
        print("No hay usuarios registrados")
    else:
        for u in lista:
            print(f"\nID: {u['id']}")
            print(f"Nombre: {u['nombres']} {u['apellidos']}")
            print(f"Teléfono: {u['telefono']}")
            print(f"Dirección: {u['direccion']}")
            print(f"Tipo: {u['tipo_usuario']}")
            print("-" * 40)
    
    pausa()

def buscar_usuario_interactivo():
    """Busca usuarios"""
    limpiar_pantalla()
    mostrar_encabezado("BUSCAR USUARIO")
    
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    opcion = input("\nSeleccione opción: ")
    
    if opcion == '1':
        try:
            id_usuario = int(input("Ingrese ID: "))
            usuario = usuarios.buscar_usuario_por_id(id_usuario)
            
            if usuario:
                print(f"\n✓ Usuario encontrado:")
                print(f"  ID: {usuario['id']}")
                print(f"  Nombre: {usuario['nombres']} {usuario['apellidos']}")
                print(f"  Teléfono: {usuario['telefono']}")
                print(f"  Tipo: {usuario['tipo_usuario']}")
            else:
                print("\n✗ Usuario no encontrado")
        except ValueError:
            print("\n✗ ID inválido")
    
    elif opcion == '2':
        nombre = input("Ingrese nombre: ")
        resultados = usuarios.buscar_usuarios_por_nombre(nombre)
        
        if resultados:
            print(f"\n✓ Se encontraron {len(resultados)} resultados:")
            for u in resultados:
                print(f"\n  ID: {u['id']} - {u['nombres']} {u['apellidos']}")
        else:
            print("\n✗ No se encontraron usuarios")
    
    pausa()

def actualizar_usuario_interactivo():
    """Actualiza un usuario"""
    limpiar_pantalla()
    mostrar_encabezado("ACTUALIZAR USUARIO")
    
    try:
        id_usuario = int(input("Ingrese ID del usuario: "))
        usuario = usuarios.buscar_usuario_por_id(id_usuario)
        
        if not usuario:
            print("\n✗ Usuario no encontrado")
            pausa()
            return
        
        print(f"\nUsuario actual: {usuario['nombres']} {usuario['apellidos']}")
        print("\nDeje en blanco para no modificar")
        
        nombres = input(f"Nombres [{usuario['nombres']}]: ") or usuario['nombres']
        apellidos = input(f"Apellidos [{usuario['apellidos']}]: ") or usuario['apellidos']
        telefono = input(f"Teléfono [{usuario['telefono']}]: ") or usuario['telefono']
        direccion = input(f"Dirección [{usuario['direccion']}]: ") or usuario['direccion']
        
        if usuarios.actualizar_usuario(id_usuario, nombres=nombres, apellidos=apellidos, 
                                       telefono=telefono, direccion=direccion):
            print("\n✓ Usuario actualizado correctamente")
        else:
            print("\n✗ Error al actualizar usuario")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def eliminar_usuario_interactivo():
    """Elimina (inactiva) un usuario"""
    limpiar_pantalla()
    mostrar_encabezado("ELIMINAR USUARIO")
    
    try:
        id_usuario = int(input("Ingrese ID del usuario: "))
        usuario = usuarios.buscar_usuario_por_id(id_usuario)
        
        if not usuario:
            print("\n✗ Usuario no encontrado")
            pausa()
            return
        
        print(f"\nUsuario: {usuario['nombres']} {usuario['apellidos']}")
        confirmacion = input("¿Confirmar eliminación? (S/N): ")
        
        if confirmacion.upper() == 'S':
            if usuarios.eliminar_usuario(id_usuario):
                print("\n✓ Usuario eliminado correctamente")
            else:
                print("\n✗ Error al eliminar usuario")
        else:
            print("\nOperación cancelada")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def menu_admin_herramientas():
    """Menú de gestión de herramientas (solo admin)"""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE HERRAMIENTAS")
        print("1. Crear nueva herramienta")
        print("2. Listar herramientas")
        print("3. Buscar herramienta")
        print("4. Actualizar herramienta")
        print("5. Eliminar herramienta")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            crear_herramienta_interactivo()
        elif opcion == '2':
            listar_herramientas_interactivo()
        elif opcion == '3':
            buscar_herramienta_interactivo()
        elif opcion == '4':
            actualizar_herramienta_interactivo()
        elif opcion == '5':
            eliminar_herramienta_interactivo()
        elif opcion == '0':
            break

def crear_herramienta_interactivo():
    """Crea una herramienta"""
    limpiar_pantalla()
    mostrar_encabezado("CREAR NUEVA HERRAMIENTA")
    
    nombre = input("Nombre: ")
    categoria = input("Categoría (ej: construcción, jardinería): ")
    
    try:
        cantidad = int(input("Cantidad disponible: "))
        valor = float(input("Valor estimado: "))
        
        print("\nEstado:")
        print("1. Activa")
        print("2. En reparación")
        print("3. Fuera de servicio")
        est = input("Seleccione (1-3): ")
        
        estados = {'1': 'activa', '2': 'en reparación', '3': 'fuera de servicio'}
        estado = estados.get(est, 'activa')
        
        herramienta = herramientas.crear_herramienta(nombre, categoria, cantidad, estado, valor)
        
        if herramienta:
            print(f"\n✓ Herramienta creada exitosamente")
            print(f"  ID: {herramienta['id']}")
            print(f"  Nombre: {herramienta['nombre']}")
        else:
            print("\n✗ Error al crear herramienta")
    except ValueError:
        print("\n✗ Valores inválidos")
    
    pausa()

def listar_herramientas_interactivo():
    """Lista todas las herramientas"""
    limpiar_pantalla()
    mostrar_encabezado("LISTA DE HERRAMIENTAS")
    
    lista = herramientas.listar_herramientas()
    
    if not lista:
        print("No hay herramientas registradas")
    else:
        for h in lista:
            print(f"\nID: {h['id']} - {h['nombre']}")
            print(f"Categoría: {h['categoria']}")
            print(f"Disponible: {h['cantidad_disponible']} / {h['cantidad_total']}")
            print(f"Estado: {h['estado']}")
            print(f"Valor: ${h['valor_estimado']}")
            print("-" * 40)
    
    pausa()

def buscar_herramienta_interactivo():
    """Busca herramientas"""
    limpiar_pantalla()
    mostrar_encabezado("BUSCAR HERRAMIENTA")
    
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion = input("\nSeleccione opción: ")
    
    if opcion == '1':
        try:
            id_h = int(input("Ingrese ID: "))
            h = herramientas.buscar_herramienta_por_id(id_h)
            
            if h:
                print(f"\n✓ Herramienta encontrada:")
                print(f"  ID: {h['id']} - {h['nombre']}")
                print(f"  Disponible: {h['cantidad_disponible']} / {h['cantidad_total']}")
            else:
                print("\n✗ Herramienta no encontrada")
        except ValueError:
            print("\n✗ ID inválido")
    
    elif opcion == '2':
        nombre = input("Ingrese nombre: ")
        resultados = herramientas.buscar_herramientas_por_nombre(nombre)
        
        if resultados:
            print(f"\n✓ Se encontraron {len(resultados)} resultados:")
            for h in resultados:
                print(f"\n  ID: {h['id']} - {h['nombre']}")
        else:
            print("\n✗ No se encontraron herramientas")
    
    elif opcion == '3':
        categoria = input("Ingrese categoría: ")
        resultados = herramientas.buscar_herramientas_por_categoria(categoria)
        
        if resultados:
            print(f"\n✓ Se encontraron {len(resultados)} resultados:")
            for h in resultados:
                print(f"\n  ID: {h['id']} - {h['nombre']}")
        else:
            print("\n✗ No se encontraron herramientas")
    
    pausa()

def actualizar_herramienta_interactivo():
    """Actualiza una herramienta"""
    limpiar_pantalla()
    mostrar_encabezado("ACTUALIZAR HERRAMIENTA")
    
    try:
        id_h = int(input("Ingrese ID de la herramienta: "))
        h = herramientas.buscar_herramienta_por_id(id_h)
        
        if not h:
            print("\n✗ Herramienta no encontrada")
            pausa()
            return
        
        print(f"\nHerramienta actual: {h['nombre']}")
        print("\nDeje en blanco para no modificar")
        
        nombre = input(f"Nombre [{h['nombre']}]: ") or h['nombre']
        categoria = input(f"Categoría [{h['categoria']}]: ") or h['categoria']
        
        if herramientas.actualizar_herramienta(id_h, nombre=nombre, categoria=categoria):
            print("\n✓ Herramienta actualizada correctamente")
        else:
            print("\n✗ Error al actualizar herramienta")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def eliminar_herramienta_interactivo():
    """Elimina una herramienta"""
    limpiar_pantalla()
    mostrar_encabezado("ELIMINAR HERRAMIENTA")
    
    try:
        id_h = int(input("Ingrese ID de la herramienta: "))
        h = herramientas.buscar_herramienta_por_id(id_h)
        
        if not h:
            print("\n✗ Herramienta no encontrada")
            pausa()
            return
        
        print(f"\nHerramienta: {h['nombre']}")
        confirmacion = input("¿Confirmar eliminación? (S/N): ")
        
        if confirmacion.upper() == 'S':
            if herramientas.eliminar_herramienta(id_h):
                print("\n✓ Herramienta eliminada correctamente")
            else:
                print("\n✗ Error al eliminar herramienta")
        else:
            print("\nOperación cancelada")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def menu_admin_prestamos():
    """Menú de gestión de préstamos (admin)"""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE PRÉSTAMOS")
        print("1. Crear préstamo directo")
        print("2. Ver solicitudes pendientes")
        print("3. Aprobar solicitud")
        print("4. Rechazar solicitud")
        print("5. Registrar devolución")
        print("6. Ver préstamos activos")
        print("7. Ver préstamos vencidos")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            crear_prestamo_directo()
        elif opcion == '2':
            ver_solicitudes_pendientes()
        elif opcion == '3':
            aprobar_solicitud_interactivo()
        elif opcion == '4':
            rechazar_solicitud_interactivo()
        elif opcion == '5':
            registrar_devolucion()
        elif opcion == '6':
            ver_prestamos_activos()
        elif opcion == '7':
            ver_prestamos_vencidos()
        elif opcion == '0':
            break

def crear_prestamo_directo():
    """Crea un préstamo directamente (admin)"""
    limpiar_pantalla()
    mostrar_encabezado("CREAR PRÉSTAMO DIRECTO")
    
    try:
        id_usuario = int(input("ID del usuario: "))
        id_herramienta = int(input("ID de la herramienta: "))
        cantidad = int(input("Cantidad: "))
        dias = int(input("Días de préstamo: "))
        obs = input("Observaciones: ")
        
        prestamo = prestamos.crear_prestamo(id_usuario, id_herramienta, cantidad, dias, obs)
        
        if prestamo:
            print(f"\n✓ Préstamo creado exitosamente")
            print(f"  ID Préstamo: {prestamo['id']}")
        else:
            print("\n✗ Error al crear préstamo")
    except ValueError:
        print("\n✗ Valores inválidos")
    
    pausa()

def ver_solicitudes_pendientes():
    """Muestra solicitudes pendientes"""
    limpiar_pantalla()
    mostrar_encabezado("SOLICITUDES PENDIENTES")
    
    solicitudes = prestamos.listar_solicitudes(filtro_estado='pendiente')
    
    if not solicitudes:
        print("No hay solicitudes pendientes")
    else:
        for s in solicitudes:
            usuario = usuarios.buscar_usuario_por_id(s['id_usuario'])
            herramienta = herramientas.buscar_herramienta_por_id(s['id_herramienta'])
            
            print(f"\nID Solicitud: {s['id']}")
            print(f"Usuario: {usuario['nombres']} {usuario['apellidos']}" if usuario else "Usuario desconocido")
            print(f"Herramienta: {herramienta['nombre']}" if herramienta else "Herramienta desconocida")
            print(f"Cantidad: {s['cantidad']}")
            print(f"Días: {s['dias_prestamo']}")
            print(f"Justificación: {s['justificacion']}")
            print(f"Fecha solicitud: {s['fecha_solicitud']}")
            print("-" * 40)
    
    pausa()

def aprobar_solicitud_interactivo():
    """Aprueba una solicitud"""
    limpiar_pantalla()
    mostrar_encabezado("APROBAR SOLICITUD")
    
    try:
        id_solicitud = int(input("ID de la solicitud: "))
        obs = input("Observaciones (opcional): ")
        
        prestamo = prestamos.aprobar_solicitud(id_solicitud, usuario_actual['id'], obs)
        
        if prestamo:
            print(f"\n✓ Solicitud aprobada y préstamo creado")
            print(f"  ID Préstamo: {prestamo['id']}")
        else:
            print("\n✗ Error al aprobar solicitud")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def rechazar_solicitud_interactivo():
    """Rechaza una solicitud"""
    limpiar_pantalla()
    mostrar_encabezado("RECHAZAR SOLICITUD")
    
    try:
        id_solicitud = int(input("ID de la solicitud: "))
        motivo = input("Motivo del rechazo: ")
        
        if prestamos.rechazar_solicitud(id_solicitud, usuario_actual['id'], motivo):
            print("\n✓ Solicitud rechazada")
        else:
            print("\n✗ Error al rechazar solicitud")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def registrar_devolucion():
    """Registra la devolución de un préstamo"""
    limpiar_pantalla()
    mostrar_encabezado("REGISTRAR DEVOLUCIÓN")
    
    try:
        id_prestamo = int(input("ID del préstamo: "))
        obs = input("Observaciones (opcional): ")
        
        if prestamos.devolver_prestamo(id_prestamo, obs):
            print("\n✓ Devolución registrada correctamente")
        else:
            print("\n✗ Error al registrar devolución")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def ver_prestamos_activos():
    """Muestra préstamos activos"""
    limpiar_pantalla()
    mostrar_encabezado("PRÉSTAMOS ACTIVOS")
    
    lista = reportes.prestamos_activos()
    
    if not lista:
        print("No hay préstamos activos")
    else:
        for p in lista:
            print(f"\nID: {p['id_prestamo']}")
            print(f"Usuario: {p['usuario']}")
            print(f"Herramienta: {p['herramienta']}")
            print(f"Cantidad: {p['cantidad']}")
            print(f"Devolución estimada: {p['fecha_devolucion_estimada']}")
            print("-" * 40)
    
    pausa()

def ver_prestamos_vencidos():
    """Muestra préstamos vencidos"""
    limpiar_pantalla()
    mostrar_encabezado("PRÉSTAMOS VENCIDOS")
    
    lista = reportes.prestamos_vencidos()
    
    if not lista:
        print("No hay préstamos vencidos")
    else:
        for p in lista:
            print(f"\nID: {p['id_prestamo']}")
            print(f"Usuario: {p['usuario']}")
            print(f"Teléfono: {p['telefono']}")
            print(f"Herramienta: {p['herramienta']}")
            print(f"Debía devolver: {p['fecha_devolucion_estimada']}")
            print("-" * 40)
    
    pausa()

def menu_reportes():
    """Menú de reportes"""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("REPORTES Y ESTADÍSTICAS")
        print("1. Resumen general")
        print("2. Herramientas con stock bajo")
        print("3. Herramientas más solicitadas")
        print("4. Usuarios más activos")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            mostrar_resumen_general()
        elif opcion == '2':
            mostrar_stock_bajo()
        elif opcion == '3':
            mostrar_mas_solicitadas()
        elif opcion == '4':
            mostrar_usuarios_activos()
        elif opcion == '0':
            break

def mostrar_resumen_general():
    """Muestra resumen general"""
    limpiar_pantalla()
    mostrar_encabezado("RESUMEN GENERAL DEL SISTEMA")
    
    resumen = reportes.resumen_general()
    
    print(f"Total de herramientas: {resumen.get('total_herramientas', 0)}")
    print(f"Total unidades: {resumen.get('total_unidades', 0)}")
    print(f"Unidades disponibles: {resumen.get('unidades_disponibles', 0)}")
    print(f"Unidades prestadas: {resumen.get('unidades_prestadas', 0)}")
    print(f"\nTotal usuarios: {resumen.get('total_usuarios', 0)}")
    print(f"\nPréstamos activos: {resumen.get('prestamos_activos', 0)}")
    print(f"Préstamos vencidos: {resumen.get('prestamos_vencidos', 0)}")
    print(f"Préstamos devueltos: {resumen.get('prestamos_devueltos', 0)}")
    print(f"Total préstamos: {resumen.get('total_prestamos', 0)}")
    
    pausa()

def mostrar_stock_bajo():
    """Muestra herramientas con stock bajo"""
    limpiar_pantalla()
    mostrar_encabezado("HERRAMIENTAS CON STOCK BAJO")
    
    lista = reportes.herramientas_stock_bajo()
    
    if not lista:
        print("No hay herramientas con stock bajo")
    else:
        for h in lista:
            print(f"\nID: {h['id']} - {h['nombre']}")
            print(f"Categoría: {h['categoria']}")
            print(f"Disponible: {h['cantidad_disponible']} / {h['cantidad_total']}")
            print("-" * 40)
    
    pausa()

def mostrar_mas_solicitadas():
    """Muestra herramientas más solicitadas"""
    limpiar_pantalla()
    mostrar_encabezado("HERRAMIENTAS MÁS SOLICITADAS")
    
    lista = reportes.herramientas_mas_solicitadas()
    
    if not lista:
        print("No hay datos disponibles")
    else:
        for i, h in enumerate(lista, 1):
            print(f"\n{i}. {h['nombre']}")
            print(f"   Categoría: {h['categoria']}")
            print(f"   Veces solicitada: {h['veces_solicitada']}")
            print(f"   Disponible: {h['cantidad_disponible']}")
    
    pausa()

def mostrar_usuarios_activos():
    """Muestra usuarios más activos"""
    limpiar_pantalla()
    mostrar_encabezado("USUARIOS MÁS ACTIVOS")
    
    lista = reportes.usuarios_mas_activos()
    
    if not lista:
        print("No hay datos disponibles")
    else:
        for i, u in enumerate(lista, 1):
            print(f"\n{i}. {u['nombre']}")
            print(f"   Total préstamos: {u['total_prestamos']}")
            print(f"   Teléfono: {u['telefono']}")
    
    pausa()

# ==================== MENÚS DE USUARIO RESIDENTE ====================

def menu_usuario_consultas():
    """Menú de consultas para usuarios"""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("CONSULTAS DE HERRAMIENTAS")
        print("1. Ver todas las herramientas")
        print("2. Buscar herramienta")
        print("3. Ver quién tiene una herramienta")
        print("4. Ver mi historial de préstamos")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            listar_herramientas_interactivo()
        elif opcion == '2':
            buscar_herramienta_interactivo()
        elif opcion == '3':
            ver_quien_tiene_herramienta()
        elif opcion == '4':
            ver_mi_historial()
        elif opcion == '0':
            break

def ver_quien_tiene_herramienta():
    """Muestra quién tiene una herramienta"""
    limpiar_pantalla()
    mostrar_encabezado("¿QUIÉN TIENE LA HERRAMIENTA?")
    
    try:
        id_h = int(input("Ingrese ID de la herramienta: "))
        
        h = herramientas.buscar_herramienta_por_id(id_h)
        if not h:
            print("\n✗ Herramienta no encontrada")
            pausa()
            return
        
        print(f"\nHerramienta: {h['nombre']}")
        print(f"Disponible: {h['cantidad_disponible']} / {h['cantidad_total']}")
        
        lista = reportes.quien_tiene_herramienta(id_h)
        
        if not lista:
            print("\nNadie tiene esta herramienta actualmente")
        else:
            print("\n¿Quién la tiene?")
            for item in lista:
                print(f"\n  {item['usuario']}")
                print(f"  Teléfono: {item['telefono']}")
                print(f"  Dirección: {item['direccion']}")
                print(f"  Cantidad: {item['cantidad']}")
                print(f"  Debe devolver: {item['fecha_devolucion_estimada']}")
    except ValueError:
        print("\n✗ ID inválido")
    
    pausa()

def ver_mi_historial():
    """Muestra el historial del usuario actual"""
    limpiar_pantalla()
    mostrar_encabezado("MI HISTORIAL DE PRÉSTAMOS")
    