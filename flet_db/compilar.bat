@echo off
REM Genera los ejecutables de las 3 apps en la carpeta dist\
pip install -r requirements.txt pyinstaller
flet pack app_consulta.py  --name consulta_tablas
flet pack app_productos.py --name crud_productos
flet pack app_pedidos.py   --name reporte_pedidos
copy /Y config.ini dist\config.ini
echo.
echo Listo. Ejecutables en la carpeta dist\
pause
