# ============================================================
#  INVENTARIO DE EQUIPOS — app.py (V2 — CRUD completo)
#  Aplicación web con Flask: listar, añadir, editar y borrar.
# ============================================================

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "inventario-clave-secreta-cambiar-en-produccion"

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
        nombre = request.form.get("nombre", "").strip()
        numero_serie = request.form.get("numero_serie", "").strip()

        # --- VALIDACIÓN ---
        if not nombre:
            flash("⚠️ El nombre es obligatorio.")
            return redirect(url_for("editar", id=id))

        if numero_serie_existe(numero_serie, ignorar_id=id):
            flash("⚠️ Ya existe otro equipo con ese número de serie.")
            return redirect(url_for("editar", id=id))
        # --- fin validación ---

        datos = (
            nombre,
            request.form.get("tipo", ""),
            request.form.get("marca", ""),
            request.form.get("modelo", ""),
            numero_serie,
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
        flash("✅ Cambios guardados correctamente.")
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
    # ------------------------------------------------------------
#  FUNCIÓN: comprobar si ya existe un nº de serie
#  (ignorar_id sirve para que al EDITAR un equipo no choque
#   consigo mismo). Devuelve True si está repetido.
# ------------------------------------------------------------
def numero_serie_existe(numero_serie, ignorar_id=None):
    # Un nº de serie vacío no cuenta como duplicado.
    if not numero_serie.strip():
        return False

    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    if ignorar_id is None:
        cursor.execute(
            "SELECT id FROM equipos WHERE numero_serie = ?",
            (numero_serie,)
        )
    else:
        # Al editar, excluimos el propio equipo de la búsqueda.
        cursor.execute(
            "SELECT id FROM equipos WHERE numero_serie = ? AND id != ?",
            (numero_serie, ignorar_id)
        )

    encontrado = cursor.fetchone()
    conexion.close()
    return encontrado is not None
def obtener_equipos(buscar="", tipo="", estado=""):
    conexion = sqlite3.connect("inventario.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    # Empezamos con algo que SIEMPRE es verdad.
    # Asi podemos ir pegando " AND ..." sin preocuparnos
    # de si es el primer filtro o no.
    consulta = "SELECT * FROM equipos WHERE 1=1"
    parametros = []

    # Busqueda por texto en varias columnas a la vez
    if buscar:
        consulta += """ AND (
            nombre LIKE ?
            OR marca LIKE ?
            OR modelo LIKE ?
            OR numero_serie LIKE ?
            OR asignado_a LIKE ?
        )"""
        comodin = f"%{buscar}%"
        parametros.extend([comodin, comodin, comodin, comodin, comodin])

    # Filtro por tipo
    if tipo:
        consulta += " AND tipo = ?"
        parametros.append(tipo)

    # Filtro por estado
    if estado:
        consulta += " AND estado = ?"
        parametros.append(estado)

    consulta += " ORDER BY nombre"

    cursor.execute(consulta, parametros)
    equipos = cursor.fetchall()
    conexion.close()
    return equipos
@app.route("/")
def index():
    # Leemos los filtros de la URL (query string).
    # Si no vienen, quedan en "" (cadena vacia) y no filtran nada.
    buscar = request.args.get("buscar", "")
    tipo = request.args.get("tipo", "")
    estado = request.args.get("estado", "")

    equipos = obtener_equipos(buscar, tipo, estado)

    # Pasamos tambien los filtros a la plantilla para que el
    # formulario "recuerde" lo buscado tras darle a Buscar.
    return render_template(
        "index.html",
        equipos=equipos,
        buscar=buscar,
        tipo=tipo,
        estado=estado,
    )