import sys

import OpenGL.GL as gl
import imgui

from render_utils import start_window
from forecast_process import start_forecast, stop_forecast
from frames.main_menu_frame import main_menu_frame

forecast_status = "offline"

host = "127.0.0.1"
port = "5000"

show_main_menu = False

def frame_forecast():
    global forecast_status

    global host
    global port

    global show_main_menu

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    io = imgui.get_io()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_quit, _ = imgui.menu_item("Quit", "", False, True)

            if clicked_quit:
                stop_forecast()
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()

    imgui.begin("Network settings")
    imgui.text("Server connection settings")
    _, host = imgui.input_text("Server host", host, 256)
    _, port = imgui.input_text("Server port", port, 256)
    imgui.separator()

    if imgui.button("Start forecast"):
        try:
            start_forecast()
            forecast_status = "running"
        except Exception:
            forecast_status = "could not start a forecast"

    if imgui.button("Stop forecast"):
        stop_forecast()
        forecast_status = "offline"
    
    imgui.text(f"Forecast status: {forecast_status}")

    imgui.separator()

    if imgui.button("Open main menu"):
            show_main_menu = True

    if imgui.button("Close main menu"):
        show_main_menu = False

    imgui.end()

    if show_main_menu:
        main_menu_frame(host, port)
            

def main():
    start_window(1600, 900, "Sales Forecasting: Forecast", frame_forecast)


if __name__ == '__main__':
    main()
    stop_forecast()