# ============================================================
#  DATOS DE EJEMPLO — Inventario de equipos (V1)
#  Se ejecuta UNA vez para meter equipos de prueba.
# ============================================================

import sqlite3

# Nos conectamos a la base de datos que ya creamos.
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Una lista de equipos de ejemplo. Cada equipo es una tupla
# con sus datos EN EL MISMO ORDEN que las columnas de abajo.
equipos_ejemplo = [
    ("PC-Recepcion", "Sobremesa", "HP", "ProDesk 400", "SN-A1B2C3",
     "Intel i5-10400", "8 GB", "256 GB SSD", "Windows 11",
     "Activo", "María López", "Recepción", "2023-05-12", "Equipo de atención al público"),

    ("Portatil-Ventas1", "Portátil", "Lenovo", "ThinkPad E15", "SN-D4E5F6",
     "Intel i7-1165G7", "16 GB", "512 GB SSD", "Windows 11",
     "Activo", "Carlos Ruiz", "Comercial", "2022-11-03", ""),

    ("Servidor-NAS", "Servidor", "Synology", "DS220+", "SN-G7H8I9",
     "Intel Celeron J4025", "2 GB", "2x 4TB HDD", "DSM 7",
     "Activo", "-", "CPD", "2021-09-20", "Copias de seguridad"),

    ("Portatil-Averiado", "Portátil", "Dell", "Latitude 5400", "SN-J1K2L3",
     "Intel i5-8265U", "8 GB", "256 GB SSD", "Windows 10",
     "Reparación", "Ana Gómez", "Taller IT", "2020-02-15", "No enciende, pendiente de placa"),

    ("Monitor-Old", "Monitor", "Samsung", "S24F350", "SN-M4N5O6",
     "-", "-", "-", "-",
     "Baja", "-", "Almacén", "2018-06-01", "Retirado por antigüedad"),
]

# INSERT con ? por cada columna (14 columnas de datos; el id
# NO se pone, lo genera solo la base de datos con AUTOINCREMENT).
cursor.executemany("""
    INSERT INTO equipos (
        nombre, tipo, marca, modelo, numero_serie,
        procesador, ram, almacenamiento, sistema_op,
        estado, asignado_a, ubicacion, fecha_compra, notas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", equipos_ejemplo)

conexion.commit()
conexion.close()

print(f"✅ Insertados {len(equipos_ejemplo)} equipos de ejemplo.")