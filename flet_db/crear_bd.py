"""Crea la base de datos y carga tablas + datos desde los .sql (sin usar la consola de MySQL).

Uso:
    python crear_bd.py            -> usa el motor de config.ini (mysql por defecto)
    python crear_bd.py postgres   -> fuerza PostgreSQL
"""
import os
import sys

if len(sys.argv) > 1:
    os.environ["DB_ENGINE"] = sys.argv[1]

import db  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))


def mysql():
    import mysql.connector
    conn = mysql.connector.connect(host=db.HOST, port=db.PORT, user=db.USER, password=db.PASSWORD)
    cur = conn.cursor()
    script = open(os.path.join(AQUI, "sql", "schema_mysql.sql"), encoding="utf-8").read()
    for stmt in script.split(";"):
        lineas = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
        stmt = "\n".join(lineas).strip()
        if stmt:
            cur.execute(stmt)
    conn.commit()
    conn.close()


def postgres():
    import psycopg2
    conn = psycopg2.connect(host=db.HOST, port=db.PORT, user=db.USER,
                            password=db.PASSWORD, dbname="postgres")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db.NAME,))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{db.NAME}"')
    conn.close()
    conn = psycopg2.connect(host=db.HOST, port=db.PORT, user=db.USER,
                            password=db.PASSWORD, dbname=db.NAME)
    cur = conn.cursor()
    cur.execute(open(os.path.join(AQUI, "sql", "schema_postgres.sql"), encoding="utf-8").read())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(f"Motor: {db.ENGINE} | {db.USER}@{db.HOST}:{db.PORT}")
    (mysql if db.ENGINE == "mysql" else postgres)()
    print("Base de datos 'tienda' creada con tablas y datos.")
    cols, filas = db.consultar("SELECT COUNT(*) FROM productos")
    print(f"Verificación: {filas[0][0]} productos cargados.")
