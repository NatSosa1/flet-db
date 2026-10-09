"""Arranque común: escritorio por defecto; modo web (para iPhone/iPad) con FLET_IOS_WEB=1."""
import os
import flet as ft


def lanzar(main, puerto):
    if os.getenv("FLET_IOS_WEB") == "1":
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0",
               port=int(os.getenv("FLET_PORT", puerto)))
    else:
        ft.app(target=main)
