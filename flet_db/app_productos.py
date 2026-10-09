"""App 2: CRUD de productos."""
import flet as ft
import db
from webmode import lanzar


def main(page: ft.Page):
    page.title = f"Productos ({db.ENGINE})"
    page.scroll = ft.ScrollMode.AUTO
    msg = ft.Text()
    nombre = ft.TextField(label="Nombre", width=250)
    precio = ft.TextField(label="Precio", width=120)
    stock = ft.TextField(label="Stock", width=100)
    categoria = ft.Dropdown(label="Categoría", width=200)
    tabla = ft.Column()
    editando = {"id": None}

    def cargar_categorias():
        _, filas = db.consultar("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
        categoria.options = [ft.dropdown.Option(key=str(i), text=n) for i, n in filas]

    def refrescar():
        _, filas = db.consultar(
            "SELECT p.id_producto, p.nombre, p.precio, p.stock, c.nombre "
            "FROM productos p JOIN categorias c ON c.id_categoria = p.id_categoria "
            "ORDER BY p.id_producto")
        tabla.controls = [ft.DataTable(
            columns=[ft.DataColumn(ft.Text(t)) for t in
                     ["ID", "Nombre", "Precio", "Stock", "Categoría", "Acciones"]],
            rows=[ft.DataRow(cells=[
                *[ft.DataCell(ft.Text(str(v))) for v in f],
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, f=f: editar(f)),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, i=f[0]: borrar(i)),
                ])),
            ]) for f in filas],
        )]
        page.update()

    def limpiar():
        editando["id"] = None
        nombre.value = precio.value = stock.value = ""
        categoria.value = None

    def editar(f):
        editando["id"] = f[0]
        nombre.value, precio.value, stock.value = f[1], str(f[2]), str(f[3])
        page.update()

    def guardar(e):
        try:
            datos = (nombre.value, float(precio.value), int(stock.value), int(categoria.value))
            if editando["id"]:
                db.ejecutar("UPDATE productos SET nombre=%s, precio=%s, stock=%s, id_categoria=%s "
                            "WHERE id_producto=%s", datos + (editando["id"],))
                msg.value = "Producto actualizado"
            else:
                db.ejecutar("INSERT INTO productos (nombre, precio, stock, id_categoria) "
                            "VALUES (%s,%s,%s,%s)", datos)
                msg.value = "Producto agregado"
            limpiar()
            refrescar()
        except Exception as ex:
            msg.value = f"Error: {ex}"
            page.update()

    def borrar(i):
        try:
            db.ejecutar("DELETE FROM productos WHERE id_producto=%s", (i,))
            msg.value = "Producto eliminado"
        except Exception as ex:
            msg.value = f"No se pudo eliminar: {ex}"
        refrescar()

    cargar_categorias()
    page.add(
        ft.Text("CRUD de productos", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([nombre, precio, stock, categoria, ft.ElevatedButton("Guardar", on_click=guardar)],
               wrap=True),
        msg, tabla)
    refrescar()


if __name__ == "__main__":
    lanzar(main, 8552)
