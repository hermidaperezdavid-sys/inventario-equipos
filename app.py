# ============================================================
#  INVENTARIO DE EQUIPOS — app.py (V3)
#  Flask: listar, buscar/filtrar, CRUD de equipos
#  + tabla relacionada 'programas' (uno-a-varios).
# ============================================================

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "inventario-clave-secreta-cambiar-en-produccion"

BASE_DATOS = "inventario.db"


# ============================================================
#  FUNCIONES DE BASE DE DATOS — EQUIPOS
# ============================================================

# ------------------------------------------------------------
#  Leer equipos, con filtros opcionales (buscador V3)
# ------------------------------------------------------------
def obtener_equipos(buscar="", tipo="", estado=""):
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    # WHERE 1=1 siempre es verdad: nos deja ir pegando
    # " AND ..." sin mirar si es el primer filtro.
    consulta = "SELECT * FROM equipos WHERE 1=1"
    parametros = []

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

    if tipo:
        consulta += " AND tipo = ?"
        parametros.append(tipo)

    if estado:
        consulta += " AND estado = ?"
        parametros.append(estado)

    consulta += " ORDER BY nombre"

    cursor.execute(consulta, parametros)
    equipos = cursor.fetchall()
    conexion.close()
    return equipos


# ------------------------------------------------------------
#  Guardar un equipo nuevo (INSERT)
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
#  Leer UN equipo por su id
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
#  Actualizar un equipo existente (UPDATE)
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
#  Borrar un equipo por su id.
#  Primero borramos SUS programas (para no dejar filas
#  huerfanas apuntando a un equipo que ya no existe).
# ------------------------------------------------------------
def eliminar_equipo(id):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM programas WHERE equipo_id = ?", (id,))
    cursor.execute("DELETE FROM equipos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()


# ------------------------------------------------------------
#  Comprobar si ya existe un nº de serie (validacion).
#  ignorar_id sirve para que al EDITAR no choque consigo mismo.
# ------------------------------------------------------------
def numero_serie_existe(numero_serie, ignorar_id=None):
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
        cursor.execute(
            "SELECT id FROM equipos WHERE numero_serie = ? AND id != ?",
            (numero_serie, ignorar_id)
        )

    encontrado = cursor.fetchone()
    conexion.close()
    return encontrado is not None


# ============================================================
#  FUNCIONES DE BASE DE DATOS — PROGRAMAS (relacion uno-a-varios)
# ============================================================

def obtener_programas(equipo_id):
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM programas WHERE equipo_id = ? ORDER BY nombre",
        (equipo_id,)
    )
    programas = cursor.fetchall()
    conexion.close()
    return programas


def guardar_programa(equipo_id, datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO programas (equipo_id, nombre, version, licencia, notas)
           VALUES (?, ?, ?, ?, ?)""",
        (equipo_id, datos["nombre"], datos["version"],
         datos["licencia"], datos["notas"])
    )
    conexion.commit()
    conexion.close()


def eliminar_programa(programa_id):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM programas WHERE id = ?", (programa_id,))
    conexion.commit()
    conexion.close()


# ============================================================
#  RUTAS
# ============================================================

# ------------------------------------------------------------
#  Pagina principal: lista + buscador/filtros
# ------------------------------------------------------------
@app.route("/")
def index():
    buscar = request.args.get("buscar", "")
    tipo = request.args.get("tipo", "")
    estado = request.args.get("estado", "")

    equipos = obtener_equipos(buscar, tipo, estado)

    return render_template(
        "index.html",
        equipos=equipos,
        buscar=buscar,
        tipo=tipo,
        estado=estado,
    )


# ------------------------------------------------------------
#  Anadir equipo (GET muestra form, POST guarda) + validacion
# ------------------------------------------------------------
@app.route("/anadir", methods=["GET", "POST"])
def anadir():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        numero_serie = request.form.get("numero_serie", "").strip()

        # --- VALIDACION ---
        if not nombre:
            flash("⚠️ El nombre es obligatorio.")
            return redirect(url_for("anadir"))

        if numero_serie_existe(numero_serie):
            flash("⚠️ Ya existe un equipo con ese número de serie.")
            return redirect(url_for("anadir"))
        # --- fin validacion ---

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
        guardar_equipo(datos)
        flash("✅ Equipo añadido correctamente.")
        return redirect(url_for("index"))
    return render_template("anadir.html")


# ------------------------------------------------------------
#  Editar equipo (GET form relleno, POST guarda) + validacion
# ------------------------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        numero_serie = request.form.get("numero_serie", "").strip()

        # --- VALIDACION ---
        if not nombre:
            flash("⚠️ El nombre es obligatorio.")
            return redirect(url_for("editar", id=id))

        if numero_serie_existe(numero_serie, ignorar_id=id):
            flash("⚠️ Ya existe otro equipo con ese número de serie.")
            return redirect(url_for("editar", id=id))
        # --- fin validacion ---

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
#  Borrar equipo — SOLO POST
# ------------------------------------------------------------
@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    eliminar_equipo(id)
    flash("🗑️ Equipo eliminado.")
    return redirect(url_for("index"))


# ------------------------------------------------------------
#  Detalle de un equipo + sus programas instalados
# ------------------------------------------------------------
@app.route("/equipo/<int:id>")
def detalle(id):
    equipo = obtener_equipo(id)
    if equipo is None:
        flash("Ese equipo no existe.")
        return redirect(url_for("index"))
    programas = obtener_programas(id)
    return render_template("detalle.html", equipo=equipo, programas=programas)


# ------------------------------------------------------------
#  Anadir un programa a un equipo — SOLO POST
# ------------------------------------------------------------
@app.route("/equipo/<int:equipo_id>/programa/anadir", methods=["POST"])
def anadir_programa(equipo_id):
    nombre = request.form.get("nombre", "").strip()
    if not nombre:
        flash("El nombre del programa es obligatorio.")
        return redirect(url_for("detalle", id=equipo_id))

    datos = {
        "nombre": nombre,
        "version": request.form.get("version", "").strip(),
        "licencia": request.form.get("licencia", "").strip(),
        "notas": request.form.get("notas", "").strip(),
    }
    guardar_programa(equipo_id, datos)
    flash("✅ Programa añadido correctamente.")
    return redirect(url_for("detalle", id=equipo_id))


# ------------------------------------------------------------
#  Borrar un programa — SOLO POST
# ------------------------------------------------------------
@app.route("/equipo/<int:equipo_id>/programa/borrar/<int:programa_id>", methods=["POST"])
def borrar_programa(equipo_id, programa_id):
    eliminar_programa(programa_id)
    flash("🗑️ Programa eliminado.")
    return redirect(url_for("detalle", id=equipo_id))


# ============================================================
#  ARRANQUE — SIEMPRE AL FINAL, sin nada de codigo detras.
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)