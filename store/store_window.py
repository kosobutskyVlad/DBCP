import sys

import OpenGL.GL as gl
import imgui

from render_utils import start_window


server_host = "127.0.0.1"
server_port = "5000"

forecast_host = "127.0.0.1"
forecast_port = "5001"

def frame_server():

    global server_host
    global server_port

    global forecast_host
    global forecast_port
    
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


def main():
    start_window(300, 200, "Sales Forecasting: Server", frame_server)


if __name__ == '__main__':
    main()