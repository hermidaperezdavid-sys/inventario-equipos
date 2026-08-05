# 📋 Inventario de Equipos

Aplicación web para gestionar un inventario de equipos informáticos (activos IT): ordenadores, servidores, monitores, impresoras y dispositivos de red. Permite dar de alta cada equipo con sus especificaciones técnicas, buscarlos y filtrarlos, y registrar el software instalado en cada uno.

Proyecto desarrollado como práctica de **desarrollo web full stack** (frontend + backend + base de datos), partiendo de mi experiencia previa en soporte IT y administración de sistemas.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-web%20framework-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-base%20de%20datos-003B57?logo=sqlite&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📸 Capturas

> _Sustituye estas líneas por capturas reales de la app (arrástralas al editor de GitHub o súbelas a una carpeta `docs/` y enlázalas)._

| Listado y buscador | Detalle de equipo |
|---|---|
| `docs/captura-listado.png` | `docs/captura-detalle.png` |

---

## ✨ Características

- **Listado de equipos** con contador total y vista en tabla.
- **Alta, edición y baja** de equipos (CRUD completo).
- **Buscador y filtros combinables**: búsqueda por texto (nombre, marca, modelo, nº de serie o persona asignada) y filtros por tipo y por estado. La búsqueda viaja en la URL, así que se puede compartir o guardar en favoritos.
- **Ficha de detalle** de cada equipo con todas sus especificaciones.
- **Software instalado por equipo**: cada equipo puede tener una lista de programas asociados (relación uno-a-varios en la base de datos).
- **Validación en el servidor**: nombre obligatorio y número de serie único; mensajes de aviso al usuario.
- **Mensajes flash** de confirmación tras cada acción (guardar, editar, borrar).

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python + [Flask](https://flask.palletsprojects.com/) |
| Base de datos | SQLite (módulo `sqlite3` de la librería estándar) |
| Frontend | HTML5 + CSS3 |
| Plantillas | Jinja2 (integrado en Flask) |

Sin dependencias externas más allá de Flask: SQLite viene incluido con Python, lo que mantiene el proyecto ligero y fácil de arrancar.

---

## 📂 Estructura del proyecto

```
inventario-equipos/
├── app.py                 # Aplicación Flask: rutas y lógica
├── crear_db.py            # Crea la BD y la tabla 'equipos' (ejecutar 1 vez)
├── crear_programas.py     # Crea la tabla 'programas' (ejecutar 1 vez)
├── datos_ejemplo.py       # Inserta equipos de ejemplo (opcional)
├── inventario.db          # Base de datos SQLite (generada; NO se sube a GitHub)
├── .gitignore
├── README.md
├── static/
│   └── estilo.css         # Hoja de estilos
└── templates/
    ├── index.html         # Listado + buscador
    ├── anadir.html        # Formulario de alta
    ├── editar.html        # Formulario de edición
    └── detalle.html       # Ficha del equipo + software instalado
```

---

## 🚀 Instalación y puesta en marcha

### Requisitos previos

- Python 3.x instalado ([descargar aquí](https://www.python.org/downloads/)).

### Pasos

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/TU_USUARIO/inventario-equipos.git
   cd inventario-equipos
   ```

2. **(Recomendado) Crea un entorno virtual e instala Flask:**

   ```bash
   python -m venv venv
   # Activar el entorno:
   #   Windows:  venv\Scripts\activate
   #   macOS/Linux:  source venv/bin/activate
   pip install flask
   ```

3. **Crea la base de datos y las tablas** (solo la primera vez):

   ```bash
   python crear_db.py
   python crear_programas.py
   ```

4. **(Opcional) Carga datos de ejemplo** para ver la app con contenido:

   ```bash
   python datos_ejemplo.py
   ```

5. **Arranca el servidor:**

   ```bash
   python app.py
   ```

6. Abre el navegador en **http://localhost:5000**

> ℹ️ Verás en la terminal un aviso de que es un servidor de desarrollo. Es normal: Flask lo indica porque este servidor está pensado para pruebas, no para producción.

---

## 🕹️ Uso

- **Añadir equipo:** botón _"➕ Añadir equipo"_ → rellena el formulario → Guardar.
- **Buscar / filtrar:** escribe en el cuadro de búsqueda o usa los desplegables de tipo y estado. Puedes combinarlos. El botón _"Limpiar"_ resetea los filtros.
- **Ver detalle:** haz clic en el **nombre** de un equipo en la tabla.
- **Software instalado:** dentro del detalle de un equipo, añade o elimina los programas de ese equipo.
- **Editar / Borrar:** botones en la columna de acciones de cada fila (el borrado pide confirmación).

---

## 🗄️ Modelo de datos

La base de datos tiene dos tablas relacionadas:

```
┌────────────────────┐          ┌────────────────────┐
│      equipos       │          │     programas      │
├────────────────────┤          ├────────────────────┤
│ id (PK)            │◄────────┐│ id (PK)            │
│ nombre             │         ││ equipo_id (FK) ────┼──┐
│ tipo               │         ││ nombre             │  │
│ marca              │         ││ version            │  │
│ modelo             │         ││ licencia           │  │
│ numero_serie       │         ││ notas              │  │
│ procesador         │         │└────────────────────┘  │
│ ram                │         │                         │
│ ...                │         └─────────────────────────┘
└────────────────────┘        un equipo → muchos programas
```

Cada fila de `programas` guarda en `equipo_id` a qué equipo pertenece (**clave foránea**). Así, **un equipo puede tener muchos programas** sin necesidad de columnas fijas del tipo `programa1`, `programa2`… Es el modelo relacional clásico de **uno-a-varios**.

---

## 🔍 Decisiones técnicas destacadas

Algunos detalles que reflejan buenas prácticas más allá de "que funcione":

- **Prevención de inyección SQL:** todas las consultas usan parámetros (`?`) y nunca insertan texto del usuario directamente en la cadena SQL. Incluso el buscador, que construye la consulta por trozos, pasa siempre los valores como parámetros.
- **Validación en el servidor:** el `required` del HTML es comodidad, no seguridad (se puede saltar). Por eso las comprobaciones de "nombre obligatorio" y "número de serie único" se hacen también en el backend, con `.strip()` para no colar valores en blanco.
- **Patrón Post/Redirect/Get:** tras guardar datos (POST) se redirige a una página de listado (GET). Evita que al recargar con F5 se reenvíe el formulario y se dupliquen registros.
- **GET para consultar, POST para modificar:** el buscador usa GET (es una consulta, la URL se puede compartir); las acciones de borrar y guardar usan POST.
- **Integridad al borrar:** al eliminar un equipo, primero se borran sus programas asociados para no dejar filas "huérfanas" apuntando a un equipo inexistente.

---

## 🧭 Mejoras futuras

- [ ] Exportar el inventario a CSV.
- [ ] Editar programas ya registrados (ahora solo se pueden añadir y borrar).
- [ ] Mover la `secret_key` a una variable de entorno (no dejarla en el código).
- [ ] Paginación cuando el listado crezca mucho.
- [ ] Restricción de acceso / login para uso multiusuario.

---

## 👤 Sobre este proyecto

Vengo del mundo del **soporte IT, sistemas y redes**, y este proyecto une esa experiencia con el desarrollo: un inventario de activos es exactamente el tipo de herramienta que se usa en un departamento de sistemas. Lo he construido por versiones, cada una funcionando antes de pasar a la siguiente, para consolidar los fundamentos de Flask, SQL y el modelo relacional.

Forma parte de mi portfolio de proyectos para dar el salto al desarrollo profesional.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Puedes usarlo, modificarlo y compartirlo libremente.
