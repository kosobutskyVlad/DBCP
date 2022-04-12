import imgui

def popup_server_down(show: bool):
    if show:
        imgui.open_popup("Server not available")
    if imgui.begin_popup_modal("Server not available")[0]:
        imgui.text("Server not available.\nPlease retry later.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def popup_load_list(show: bool, list_name: str):
    if show:
        imgui.open_popup(f"Error: {list_name} not loaded")
    if imgui.begin_popup_modal(f"Error: {list_name} not loaded")[0]:
        imgui.text(f"Load the {list_name} list first.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def popup_already_exists(show: bool, item_id: str):
    if show:
        imgui.open_popup(f"Error: {item_id} already exists")
    if imgui.begin_popup_modal(f"Error: {item_id} already exists")[0]:
        imgui.text(f"{item_id} can't be created.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def popup_not_found(show: bool, item_id: str):
    if show:
        imgui.open_popup(f"Error: {item_id} not found")
    if imgui.begin_popup_modal(f"Error: {item_id} not found")[0]:
        imgui.text(f"{item_id} can't be accessed.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def popup_deletion_rejected(show: bool, item_id: str):
    if show:
        imgui.open_popup(f"Error: {item_id} can't be deleted")
    if imgui.begin_popup_modal(f"Error: {item_id} can't be deleted")[0]:
        imgui.text(f"{item_id} is being referenced by a foreign key.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show

def popup_argument_missing(show: bool):
    if show:
        imgui.open_popup(f"Specify ID")
    if imgui.begin_popup_modal(f"Specify ID")[0]:
        imgui.text(f"Specify at least one of: store_id, product_id.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show = False
        imgui.end_popup()
    return show