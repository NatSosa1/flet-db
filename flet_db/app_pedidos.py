"""App 3: reporte de pedidos con totales (JOIN de 4 tablas)."""
import flet as ft
import db
from webmode import lanzar

SQL = """
SELECT p.id_pedido, c.nombre, p.fecha, p.estado,
       SUM(d.cantidad * d.precio_unitario) AS total
FROM pedidos p
JOIN clientes c ON c.id_cliente = p.id_cliente
JOIN detalle_pedidos d ON d.id_pedido = p.id_pedido
{where}
GROUP BY p.id_pedido, c.nombre, p.fecha, p.estado
ORDER BY p.id_pedido
"""


def main(page: ft.Page):
    page.title = f"Reporte de pedidos ({db.ENGINE})"
    page.scroll = ft.ScrollMode.AUTO
    resumen = ft.Text(size=16)
    tabla = ft.Column()

    def cargar(estado=None):
        if estado and estado != "todos":
            cols, filas = db.consultar(SQL.format(where="WHERE p.estado = %s"), (estado,))
        else:
            cols, filas = db.consultar(SQL.format(where=""))
        tabla.controls = [ft.DataTable(
            columns=[ft.DataColumn(ft.Text(t)) for t in
                     ["Pedido", "Cliente", "Fecha", "Estado", "Total"]],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in f]) for f in filas],
        )]
        total = sum(float(f[4]) for f in filas)
        resumen.value = f"{len(filas)} pedidos | Total: ${total:,.2f}"
        page.update()

    filtro = ft.Dropdown(
        label="Estado", width=200, value="todos",
        options=[ft.dropdown.Option(x) for x in ["todos", "pendiente", "enviado", "entregado"]],
        on_change=lambda e: cargar(e.control.value),
    )
    page.add(ft.Text("Reporte de pedidos", size=24, weight=ft.FontWeight.BOLD),
             filtro, resumen, tabla)
    cargar()


if __name__ == "__main__":
    lanzar(main, 8553)
