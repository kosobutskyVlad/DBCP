import sys

import OpenGL.GL as gl
import imgui

from render_utils import *
from server import *

server_status = "offline"

def frame_server():
    global server_status
    
    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    io = imgui.get_io()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_quit, _ = imgui.menu_item("Quit", "", False, True)

            if clicked_quit:
                server_status = "offline"
                stop_server()
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()
    
    
    imgui.begin("Server Startup")
    
    if imgui.button("Start server"):
        try:
            start_server()
            server_status = "running"
        except Exception:
            server_status = "could not start a server"
        
        
    if imgui.button("Stop server"):
        stop_server()
        server_status = "offline"
    
    imgui.text(f"Server status: {server_status}")
    
    imgui.end()


def main():
    start_window(300, 200, "Sales Forecasting: Server", frame_server)


if __name__ == '__main__':
    main()