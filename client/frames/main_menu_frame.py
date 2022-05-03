import imgui

from frames.viewers.cities_frame import cities_frame
from frames.viewers.storetypes_frame import storetypes_frame
from frames.viewers.stores_frame import stores_frame
from frames.viewers.products_frame import products_frame
from frames.viewers.purchases_frame import purchases_frame
from frames.viewers.parameters_frame import parameters_frame
from frames.forecast_window import forecast_window

active_editors = {
    "storetypes": False,
    "cities": False,
    "stores": False,
    "products": False,
    "purchases": False,
    "parameters": False,
}

show_forecast_window = False

def main_menu_frame(host, port):

    global active_editors
    global show_forecast_window

    imgui.begin("Main menu")

    for editor in active_editors:
        _, active_editors[editor] = imgui.checkbox(
            f"Show {editor} editor",
            active_editors[editor]
        )

    imgui.separator()
    _, show_forecast_window = imgui.checkbox(
            f"Show forecast window",
            show_forecast_window
        )

    imgui.end()

    for editor in active_editors:
        if active_editors[editor]:
            eval(f"{editor}_frame(host, port)")

    if show_forecast_window:
        forecast_window(host, port)