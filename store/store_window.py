import sys

import OpenGL.GL as gl
import imgui

from render_utils import start_window
from xml_generation.procurement_plan import generate_plan

server_host = "127.0.0.1"
server_port = "5000"

forecast_host = "127.0.0.1"
forecast_port = "5001"

store_id = ""

def frame_store():

    global server_host
    global server_port

    global forecast_host
    global forecast_port

    global store_id

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    io = imgui.get_io()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_quit, _ = imgui.menu_item("Quit", "", False, True)

            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()


    imgui.begin("Network settings")
    imgui.text("Server connection settings")
    _, server_host = imgui.input_text("Server host", server_host, 256)    
    _, server_port = imgui.input_text("Server port", server_port, 256)
    imgui.separator()
    imgui.text("Forecast connection settings")
    _, forecast_host = imgui.input_text("Server host", forecast_host, 256)    
    _, forecast_port = imgui.input_text("Server port", forecast_port, 256)
    imgui.separator()

    imgui.end()

    _, store_id = imgui.input_text("Store ID", store_id, 256)

    if imgui.button("Generate procurement plan"):
        generate_plan(
            server_host, server_port,
            forecast_host, forecast_port,
            store_id
        )


def main():
    start_window(300, 200, "Sales Forecasting: Server", frame_store)


if __name__ == '__main__':
    main()