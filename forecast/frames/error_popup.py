import imgui

def error_popup(show: bool, error_message: str) -> bool:
    if show:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        error_message = process_error_message(error_message)
        imgui.text(error_message)

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def process_error_message(error_message) -> str:
    if isinstance(error_message, str):
        return error_message

    errors = []
    for error in error_message:
        errors.append(f"{error['loc'][1]}: {error['msg']}")

    return "\n".join(errors)