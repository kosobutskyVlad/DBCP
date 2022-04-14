import imgui

from frames.viewers.cities_frame import cities_frame
from frames.viewers.storetypes_frame import storetypes_frame
from frames.viewers.stores_frame import stores_frame
from frames.viewers.products_frame import products_frame
from frames.viewers.purchases_frame import purchases_frame
from frames.viewers.parameters_frame import parameters_frame

active = {
    "storetypes": False,
    "cities": False,
    "stores": False,
    "products": False,
    "purchases": False,
    "parameters": False,
}

def main_menu_frame(host, port):

    global active

    imgui.begin("Main menu")

    for frame in active:
        _, active[frame] = imgui.checkbox(f"Show {frame} frame", active[frame])

    imgui.end()

    if active["cities"]:
        cities_frame(host, port)

    if active["storetypes"]:
        storetypes_frame(host, port)

    if active["stores"]:
        stores_frame(host, port)

    if active["products"]:
        products_frame(host, port)

    if active["purchases"]:
        purchases_frame(host, port)

    if active["parameters"]:
        parameters_frame(host, port)