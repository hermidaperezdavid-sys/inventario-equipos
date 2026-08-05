import sqlite3

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS programas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        version TEXT,
        licencia TEXT,
        notas TEXT,
        FOREIGN KEY (equipo_id) REFERENCES equipos(id)
    )
""")

conexion.commit()
conexion.close()
print("Tabla 'programas' creada (o ya existia).")