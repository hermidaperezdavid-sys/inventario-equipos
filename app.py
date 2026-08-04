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

# ------------------------------------------------------------
#  FUNCIÓN: leer UN equipo por su id
# ------------------------------------------------------------
def obtener_equipo(id):
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    # ? también aquí: el id viene de la URL, así que lo tratamos
    # como dato no fiable -> parametrizado, nunca f-string.
    cursor.execute("SELECT * FROM equipos WHERE id = ?", (id,))
    equipo = cursor.fetchone()   # UNA sola fila (o None si no existe)

    conexion.close()
    return equipo


# ------------------------------------------------------------
#  FUNCIÓN: actualizar un equipo existente
# ------------------------------------------------------------
def actualizar_equipo(id, datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    # UPDATE cambia una fila que YA existe. El WHERE id = ? es
    # CRÍTICO: sin él, actualizaría TODOS los equipos a la vez.
    # Fíjate en el orden: primero los 14 valores, y el id AL FINAL
    # (porque en la consulta el ? del id va el último).
    cursor.execute(
        """
        UPDATE equipos SET
            nombre = ?, tipo = ?, marca = ?, modelo = ?,
            numero_serie = ?, procesador = ?, ram = ?,
            almacenamiento = ?, sistema_op = ?, estado = ?,
            asignado_a = ?, ubicacion = ?, fecha_compra = ?, notas = ?
        WHERE id = ?
        """,
        datos + (id,)   # los 14 datos + el id al final
    )

    conexion.commit()
    conexion.close()
    # ------------------------------------------------------------
#  RUTA: editar un equipo ("/editar/<id>")
#  GET -> muestra el formulario relleno. POST -> guarda cambios.
# ------------------------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        # Mismos 14 campos que en añadir.
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
        actualizar_equipo(id, datos)
        return redirect(url_for("index"))

    # GET: buscamos el equipo y mostramos el formulario relleno.
    equipo = obtener_equipo(id)
    return render_template("editar.html", equipo=equipo)
# ------------------------------------------------------------
#  FUNCIÓN: borrar un equipo por su id
# ------------------------------------------------------------
def eliminar_equipo(id):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    # DELETE con WHERE id = ? -> borra SOLO ese equipo.
    # Igual que en UPDATE: sin el WHERE, borraría TODA la tabla.
    # Y el id parametrizado con ? (viene de fuera, no es fiable).
    cursor.execute("DELETE FROM equipos WHERE id = ?", (id,))

    conexion.commit()
    conexion.close()
    # ------------------------------------------------------------
#  RUTA: borrar un equipo ("/borrar/<id>")  — SOLO POST.
#  No hay GET: borrar no se muestra, se ejecuta y se vuelve.
# ------------------------------------------------------------
@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    eliminar_equipo(id)
    return redirect(url_for("index"))