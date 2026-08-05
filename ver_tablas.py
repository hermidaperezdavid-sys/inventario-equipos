import sqlite3, os

print("Carpeta actual:", os.getcwd())
print("Ruta del .db:", os.path.abspath("inventario.db"))

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = [fila[0] for fila in cursor.fetchall()]
conexion.close()

print("Tablas:", tablas)