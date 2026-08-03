# ============================================================
#  INVENTARIO DE EQUIPOS — app.py (V1)
#  Aplicación web con Flask que LISTA los equipos.
# ============================================================

import sqlite3
from flask import Flask, render_template

# Creamos la aplicación Flask. '__name__' le dice a Flask
# dónde está este archivo, para encontrar las carpetas
# 'templates' y 'static'.
app = Flask(__name__)

# Nombre del archivo de base de datos.
BASE_DATOS = "inventario.db"


# ------------------------------------------------------------
#  FUNCIÓN: leer todos los equipos de la base de datos
# ------------------------------------------------------------
def obtener_equipos():
    conexion = sqlite3.connect(BASE_DATOS)

    # row_factory hace que cada fila se pueda leer por el NOMBRE
    # de la columna (fila["nombre"]) en vez de por su número.
    # Mucho más cómodo y legible.
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos ORDER BY nombre")
    equipos = cursor.fetchall()   # trae TODAS las filas

    conexion.close()
    return equipos


# ------------------------------------------------------------
#  RUTA: la página principal ("/")
# ------------------------------------------------------------
# El @app.route("/") dice: "cuando alguien abra la dirección
# raíz, ejecuta esta función". A esto se le llama una RUTA.
@app.route("/")
def index():
    equipos = obtener_equipos()
    # render_template coge index.html y le pasa los equipos.
    return render_template("index.html", equipos=equipos)


# ------------------------------------------------------------
#  ARRANQUE
# ------------------------------------------------------------
if __name__ == "__main__":
    # debug=True: recarga solo al guardar cambios y muestra
    # errores detallados. Solo para desarrollo, nunca en real.
    app.run(debug=True)