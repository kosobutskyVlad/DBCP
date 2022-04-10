import imgui

from frames.cities_frame import cities_frame

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

    