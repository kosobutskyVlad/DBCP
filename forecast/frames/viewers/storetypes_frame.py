import requests

import imgui

from ..error_popup import error_popup

response_get_storetypes = None
storetypes_list = []
show_selectable_storetypes = False
selectable_storetypes = {}
storetypes_info = {}
storetypes_refresh = {}
storetypes_changed = {}

show_error_popup = False
error_popup_message = ""

info_add_storetype = {
    "storetype_id": "",
    "storetype_description": ""
}

def storetypes_frame(host: str, port: int):
    global response_get_storetypes
    global storetypes_list
    global show_selectable_storetypes
    global selectable_storetypes
    global storetypes_info
    global storetypes_refresh
    global storetypes_changed
    global info_add_storetype

    global show_error_popup
    global error_popup_message

    imgui.begin("Storetypes")

    show_error_popup = error_popup(show_error_popup, error_popup_message)

    if imgui.button("Load storetypes list"):
        try:
            response_get_storetypes = requests.get(
                f"http://{host}:{port}/storetypes/get-storetypes")

            if response_get_storetypes.status_code == 200:
                storetypes_list = response_get_storetypes.json()

                selectable_storetypes = {storetype[0]: False for storetype
                                        in storetypes_list}
                storetypes_refresh = {storetype[0]: True for storetype
                                    in storetypes_list}
                storetypes_changed = {storetype[0]: False for storetype
                                    in storetypes_list}
                show_selectable_storetypes = False

        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."
        
    if imgui.button("Show storetypes list"):
        if response_get_storetypes:
            if response_get_storetypes.status_code == 200:
                show_selectable_storetypes = True
        else:
            show_error_popup = True
            error_popup_message = "Load the storetypes list first."

    if show_selectable_storetypes:
        imgui.begin_child("storetypes_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for storetype in storetypes_list:
            label = storetype[0]
            _, selectable_storetypes[storetype[0]] = imgui.selectable(
                label, selectable_storetypes[storetype[0]])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for storetype in selectable_storetypes:
        if selectable_storetypes[storetype]:
            if storetypes_refresh[storetype]:
                storetypes_refresh[storetype] = False
                try:
                    get_storetype_response = requests.get(
                        f"http://{host}:{port}/storetypes/get-storetype/{storetype}")
                    info = get_storetype_response.json()[0]
                    storetypes_info[storetype] = {
                        "storetype_description": info[1]}
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."
                    storetypes_list = []
                    show_selectable_storetypes = False
                    selectable_storetypes = {}
                    storetypes_info = {}
                    storetypes_refresh = {}
                    storetypes_changed = {}

            if show_error_popup:
                break
            
            imgui.begin_child("storetypes_editor",
                              1200, 200, border=True)
            imgui.text(storetype)
            imgui.same_line()
            imgui.push_item_width(600)
            changed, storetypes_info[storetype]["storetype_description"] = \
                imgui.input_text(f"{storetype}: storetype_description",
                storetypes_info[storetype]["storetype_description"], 101)
            if changed:
                storetypes_changed[storetype] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_storetypes = imgui.button("Update storetypes")
    if button_clicked_update_storetypes:
        button_clicked_update_storetypes = False
        for storetype in storetypes_changed:
            if storetypes_changed[storetype]:
                try:
                    response_update_storetype = requests.put(
                        f"http://{host}:{port}/storetypes/update-storetype",
                        json={"storetype_id": storetype,
                        "storetype_description": storetypes_info[storetype]["storetype_description"]})
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    button_clicked_delete_storetypes = imgui.button("Delete storetypes")
    if button_clicked_delete_storetypes:
        button_clicked_delete_storetypes = False
        for storetype in selectable_storetypes:
            if selectable_storetypes[storetype]:
                try:
                    response_delete_storetype = requests.delete(
                        f"http://{host}:{port}/storetypes/delete-storetype/{storetype}")
                    if response_delete_storetype.status_code == 409:
                        show_error_popup = True
                        error_popup_message = response_delete_storetype.json()["detail"]
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.push_item_width(50)
    _, info_add_storetype["storetype_id"] = imgui.input_text(
        "Add storetype_id", info_add_storetype["storetype_id"], 5)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(600)
    _, info_add_storetype["storetype_description"] = imgui.input_text(
        f"Add storetype_description",
        info_add_storetype["storetype_description"], 101)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_storetype = imgui.button("Add a storetype")
    if button_clicked_add_storetype:
        button_clicked_add_storetype = False
        try:
            response_add_storetype = requests.post(
                f"http://{host}:{port}/storetypes/add-storetype",
                json=info_add_storetype)

            if response_add_storetype.status_code == 422:
                show_error_popup = True
                error_popup_message = response_add_storetype.json()["detail"]
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.end()