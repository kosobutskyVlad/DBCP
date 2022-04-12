import imgui

def server_down_frame(show: bool):
    if show:
        imgui.open_popup("Server not available")
    if imgui.begin_popup_modal("Server not available")[0]:
        imgui.text("Server not available.\nPlease retry later")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show