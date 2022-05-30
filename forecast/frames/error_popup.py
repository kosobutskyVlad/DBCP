import imgui

def error_popup(show: bool, error_message: str) -> bool:
    if show:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        imgui.text(error_message)

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show