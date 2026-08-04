# ============================================================
#  INVENTARIO DE EQUIPOS — app.py (V1)
#  Aplicación web con Flask que LISTA los equipos.
# ============================================================

import sqlite3
from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
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
    # ------------------------------------------------------------
#  FUNCIÓN: guardar un equipo nuevo en la base de datos
# ------------------------------------------------------------
def guardar_equipo(datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    # Fíjate: SIEMPRE con ? (nunca f-strings) -> anti inyección SQL.
    # Hay 14 columnas -> 14 signos ? -> 14 valores en 'datos'.
    cursor.execute(
        """
        INSERT INTO equipos
            (nombre, tipo, marca, modelo, numero_serie,
             procesador, ram, almacenamiento, sistema_op,
             estado, asignado_a, ubicacion, fecha_compra, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        datos
    )

    conexion.commit()   # guarda de verdad
    conexion.close()
    # ------------------------------------------------------------
#  RUTA: añadir un equipo ("/anadir")  — GET muestra el
#  formulario, POST lo guarda.
# ------------------------------------------------------------
@app.route("/anadir", methods=["GET", "POST"])
def anadir():
    # Si llega un POST, el usuario ENVIÓ el formulario.
    if request.method == "POST":
        # Leemos cada casilla por su 'name'.
        # .get(campo, "") -> si faltara, devuelve "" en vez de fallar.
        datos = (
            request.form.get("nombre", ""),
            request.form.get("tipo", ""),
            request.form.get("marca", ""),
            request.form.get("modelo", ""),
            request.form.get("numero_serie", ""),
            request.form.get("procesador", ""),
            request.form.get("ram", ""),
            request.form.get("almacenamiento", ""),
            request.form.get("sistema_op", ""),
            request.form.get("estado", ""),
            request.form.get("asignado_a", ""),
            request.form.get("ubicacion", ""),
            request.form.get("fecha_compra", ""),
            request.form.get("notas", ""),
        )
        guardar_equipo(datos)
        # Tras guardar, reenviamos al usuario a la lista.
        return redirect(url_for("index"))

    # Si llega un GET, mostramos el formulario vacío.
    return render_template("anadir.html")