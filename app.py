# ============================================================
#  INVENTARIO DE EQUIPOS — app.py (V2 — CRUD completo)
#  Aplicación web con Flask: listar, añadir, editar y borrar.
# ============================================================

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DATOS = "inventario.db"


# ------------------------------------------------------------
#  FUNCIÓN: leer todos los equipos de la base de datos
# ------------------------------------------------------------
def obtener_equipos():
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos ORDER BY nombre")
    equipos = cursor.fetchall()
    conexion.close()
    return equipos


# ------------------------------------------------------------
#  FUNCIÓN: guardar un equipo nuevo en la base de datos
# ------------------------------------------------------------
def guardar_equipo(datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
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
    conexion.commit()
    conexion.close()


# ------------------------------------------------------------
#  FUNCIÓN: leer UN equipo por su id
# ------------------------------------------------------------
def obtener_equipo(id):
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id = ?", (id,))
    equipo = cursor.fetchone()
    conexion.close()
    return equipo


# ------------------------------------------------------------
#  FUNCIÓN: actualizar un equipo existente
# ------------------------------------------------------------
def actualizar_equipo(id, datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE equipos SET
            nombre = ?, tipo = ?, marca = ?, modelo = ?,
            numero_serie = ?, procesador = ?, ram = ?,
            almacenamiento = ?, sistema_op = ?, estado = ?,
            asignado_a = ?, ubicacion = ?, fecha_compra = ?, notas = ?
        WHERE id = ?
        """,
        datos + (id,)
    )
    conexion.commit()
    conexion.close()


# ------------------------------------------------------------
#  FUNCIÓN: borrar un equipo por su id
# ------------------------------------------------------------
def eliminar_equipo(id):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()


# ------------------------------------------------------------
#  RUTA: la página principal ("/")
# ------------------------------------------------------------
@app.route("/")
def index():
    equipos = obtener_equipos()
    return render_template("index.html", equipos=equipos)


# ------------------------------------------------------------
#  RUTA: añadir un equipo ("/anadir")
#  GET muestra el formulario, POST lo guarda.
# ------------------------------------------------------------
@app.route("/anadir", methods=["GET", "POST"])
def anadir():
    if request.method == "POST":
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
        return redirect(url_for("index"))
    return render_template("anadir.html")


# ------------------------------------------------------------
#  RUTA: editar un equipo ("/editar/<id>")
#  GET muestra el formulario relleno, POST guarda cambios.
# ------------------------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
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
    equipo = obtener_equipo(id)
    return render_template("editar.html", equipo=equipo)


# ------------------------------------------------------------
#  RUTA: borrar un equipo ("/borrar/<id>") — SOLO POST.
# ------------------------------------------------------------
@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    eliminar_equipo(id)
    return redirect(url_for("index"))


# ------------------------------------------------------------
#  ARRANQUE
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)