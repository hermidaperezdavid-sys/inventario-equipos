# ============================================================
#  CREAR LA BASE DE DATOS — Inventario de equipos (V1)
#  Se ejecuta UNA sola vez para montar la tabla vacía.
# ============================================================

# 'sqlite3' viene incluido con Python: no hay que instalar nada.
# Nos deja crear y usar bases de datos SQLite (un solo archivo).
import sqlite3

# Nos conectamos al archivo de base de datos.
# Si 'inventario.db' no existe, SQLite lo CREA en este momento.
conexion = sqlite3.connect("inventario.db")

# El 'cursor' es quien ejecuta las órdenes SQL sobre la base de datos.
cursor = conexion.cursor()

# --- Creamos la tabla 'equipos' ---
# 'CREATE TABLE IF NOT EXISTS' = crea la tabla, pero solo si no
# existe ya (así no da error si ejecutas el script otra vez).
cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre         TEXT NOT NULL,
        tipo           TEXT,
        marca          TEXT,
        modelo         TEXT,
        numero_serie   TEXT,
        procesador     TEXT,
        ram            TEXT,
        almacenamiento TEXT,
        sistema_op     TEXT,
        estado         TEXT,
        asignado_a     TEXT,
        ubicacion      TEXT,
        fecha_compra   TEXT,
        notas          TEXT
    )
""")

# Guardamos los cambios (commit) y cerramos la conexión.
conexion.commit()
conexion.close()

print("✅ Base de datos 'inventario.db' lista, con la tabla 'equipos'.")