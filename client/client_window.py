import sys

import OpenGL.GL as gl
import imgui

from render_utils import start_window
from frames.main_menu_frame import main_menu_frame
from test_window import show_test_window

host = "127.0.0.1"
port = "5001"
client_running = False
prev_host = host
prev_port = port

def frame_client():
    global client_running
    global host
    global port
    
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
    
    
    imgui.begin("Connection Settings")
    _, host = imgui.input_text("Server host", host, 256)    
    _, port = imgui.input_text("Server port", port, 256)
    
    if imgui.button("Start client"):
        client_running = True
        
    if imgui.button("Exit client"):
        client_running = False
    
    imgui.end()

    if client_running:
        main_menu_frame(host, port)

def main():
    #start_window(1600, 900, "Sales Forecasting: Client", show_test_window)
    start_window(1600, 900, "Sales Forecasting: Client", frame_client)

if __name__ == '__main__':
    main()