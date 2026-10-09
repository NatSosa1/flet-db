"""App 1: consulta de tablas de la base de datos (MySQL / PostgreSQL)."""
import flet as ft
import db
from webmode import lanzar


def main(page: ft.Page):
    page.title = f"Consulta de tablas ({db.ENGINE})"
    page.scroll = ft.ScrollMode.AUTO
    estado = ft.Text()
    tabla_ui = ft.Row(scroll=ft.ScrollMode.AUTO)

    def cargar(nombre):
        try:
            cols, filas = db.consultar_tabla(nombre)
            tabla_ui.controls = [ft.DataTable(
                columns=[ft.DataColumn(ft.Text(c)) for c in cols],
                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in f]) for f in filas],
            )]
            estado.value = f"{len(filas)} registros en '{nombre}'"
        except Exception as e:
            tabla_ui.controls = []
            estado.value = f"Error: {e}"
        page.update()

    dd = ft.Dropdown(
        label="Tabla", width=250,
        options=[ft.dropdown.Option(t) for t in db.TABLAS],
        on_change=lambda e: cargar(e.control.value),
    )
    page.add(ft.Text("Consulta de tablas", size=24, weight=ft.FontWeight.BOLD), dd, estado, tabla_ui)


if __name__ == "__main__":
    lanzar(main, 8551)
