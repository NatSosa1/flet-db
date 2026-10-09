# Sistema Flet + MySQL (sin Docker)

## Archivos
- `db.py` – conexión y consultas (MySQL; PostgreSQL opcional)
- `config.ini` – usuario, contraseña y servidor de la base de datos
- `crear_bd.py` – crea la BD y carga tablas + datos (sin consola de MySQL)
- `app_consulta.py` – App 1: consulta de tablas
- `app_productos.py` – App 2: CRUD de productos
- `app_pedidos.py` – App 3: reporte de pedidos con totales
- `sql/schema_mysql.sql`, `sql/schema_postgres.sql` – estructura + datos
- `compilar.bat` / `compilar.sh` – generan los ejecutables

## Pasos
1. Instalar Python 3.12 y MySQL Server 8 (con MySQL corriendo).
2. Editar `config.ini` y poner tu contraseña de MySQL.
3. `pip install -r requirements.txt`
4. `python crear_bd.py`
5. Probar: `python app_consulta.py`, `python app_productos.py`, `python app_pedidos.py`
6. Compilar: `compilar.bat` (Windows) o `./compilar.sh` -> ejecutables en `dist/`

## iPhone / iPad (iOS)
Las apps corren en la Mac (donde está MySQL de Homebrew) y se abren desde el iPhone por Wi-Fi:
1. `brew services start mysql` y `python crear_bd.py` (una sola vez).
2. `./ios_web.sh` (o `pip install -r requirements.txt && python ios_web.py`).
3. En Safari del iPhone (misma red Wi-Fi) abre las URLs que imprime: puertos 8551, 8552 y 8553.
4. Opcional: Compartir > "Agregar a pantalla de inicio" para usarla como app.
Si macOS pregunta por conexiones entrantes, permite a Python.

## PostgreSQL (opcional)
En `config.ini` cambia `engine = postgres`, `port = 5432`, `user = postgres`
y ejecuta `python crear_bd.py`.

## Evidencias a subir
- `dist/` comprimido (ejecutables + config.ini)
- `sql/schema_mysql.sql` y `sql/schema_postgres.sql`
- Capturas de las 3 apps consultando la BD
