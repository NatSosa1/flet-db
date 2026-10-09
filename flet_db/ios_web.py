"""Levanta las 3 apps como sitios web accesibles desde iPhone/iPad en la misma red Wi-Fi.

Uso (en la Mac):  python ios_web.py
Luego abre en Safari del iPhone las URLs que se imprimen.
"""
import os
import socket
import subprocess
import sys

APPS = [("app_consulta.py", 8551, "Consulta de tablas"),
        ("app_productos.py", 8552, "CRUD de productos"),
        ("app_pedidos.py", 8553, "Reporte de pedidos")]


def ip_lan():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    aqui = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, FLET_IOS_WEB="1")
    procs = [subprocess.Popen([sys.executable, os.path.join(aqui, f)], cwd=aqui, env=env)
             for f, _, _ in APPS]
    ip = ip_lan()
    print("\nAbre en Safari (iPhone en el mismo Wi-Fi que la Mac):")
    for _, p, n in APPS:
        print(f"  {n}: http://{ip}:{p}")
    print("\nCtrl+C para detener.")
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()
