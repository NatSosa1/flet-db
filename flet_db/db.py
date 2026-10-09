"""Capa de acceso a datos: MySQL o PostgreSQL según DB_ENGINE."""
import configparser
import os
import sys

# config.ini junto al .exe (o junto al .py). Las variables de entorno tienen prioridad.
_BASE = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(_BASE, "config.ini"), encoding="utf-8")


def _get(env, key, default):
    return os.getenv(env) or _cfg.get("db", key, fallback=default)


ENGINE = _get("DB_ENGINE", "engine", "mysql").lower()
HOST = _get("DB_HOST", "host", "localhost")
PORT = int(_get("DB_PORT", "port", "3306" if ENGINE == "mysql" else "5432"))
USER = _get("DB_USER", "user", "root" if ENGINE == "mysql" else "postgres")
PASSWORD = _get("DB_PASSWORD", "password", "")
NAME = _get("DB_NAME", "name", "tienda")

TABLAS = ["categorias", "productos", "clientes", "pedidos", "detalle_pedidos"]


def get_conn():
    if ENGINE == "mysql":
        import mysql.connector
        return mysql.connector.connect(
            host=HOST, port=PORT, user=USER, password=PASSWORD, database=NAME
        )
    import psycopg2
    return psycopg2.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, dbname=NAME
    )


def consultar(sql, params=None):
    """Devuelve (columnas, filas) de un SELECT."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        return cols, cur.fetchall()
    finally:
        conn.close()


def ejecutar(sql, params=None):
    """INSERT / UPDATE / DELETE con commit."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
    finally:
        conn.close()


def consultar_tabla(tabla, limite=100):
    if tabla not in TABLAS:  # lista blanca: evita inyección SQL
        raise ValueError("Tabla no permitida")
    return consultar(f"SELECT * FROM {tabla} LIMIT {int(limite)}")
