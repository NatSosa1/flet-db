#!/bin/sh
# Genera los ejecutables de las 3 apps en dist/
pip install -r requirements.txt pyinstaller
flet pack app_consulta.py  --name consulta_tablas
flet pack app_productos.py --name crud_productos
flet pack app_pedidos.py   --name reporte_pedidos
cp config.ini dist/config.ini
echo "Listo. Ejecutables en dist/"
