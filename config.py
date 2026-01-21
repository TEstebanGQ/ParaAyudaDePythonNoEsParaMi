RUTA_DATOS = "datos/"
RUTA_LOGS = "logs/"

ARCHIVO_HERRAMIENTAS = RUTA_DATOS + "herramientas.json"
ARCHIVO_USUARIOS = RUTA_DATOS + "usuarios.json"
ARCHIVO_PRESTAMOS = RUTA_DATOS + "prestamos.json"
ARCHIVO_LOG = RUTA_LOGS + "sistema.log"

# Configuración de stock
STOCK_MINIMO = 3

# Días de préstamo por defecto
DIAS_PRESTAMO_DEFAULT = 7

# Usuario activo (simulación de sesión)
USUARIO_ACTUAL = None

# Estados válidos
ESTADOS_HERRAMIENTA = ["activa", "en_reparacion", "fuera_servicio"]
CATEGORIAS_HERRAMIENTA = ["construccion", "jardineria", "electricidad", 
                          "plomeria", "pintura", "carpinteria", "otros"]
TIPOS_USUARIO = ["residente", "administrador"]
ESTADOS_PRESTAMO = ["pendiente", "aprobado", "activo", "devuelto", "rechazado"]