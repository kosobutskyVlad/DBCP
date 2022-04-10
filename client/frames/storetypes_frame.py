import requests

import imgui

response_get_storetypes = None
storetypes_list = []
show_selectable_storetypes = False
selectable_storetypes = {}
storetypes_info = {}
storetypes_refresh = {}
storetypes_changed = {}

show_popup_get_storetypes_error = False
show_popup_delete_error = False

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

    global show_popup_get_storetypes_error
    global show_popup_delete_error

    imgui.begin("Storetypes")

    if imgui.button("Load storetypes list"):
        response_get_storetypes = requests.get(
            f"http://{host}:{port}/storetypes/get-storetypes")
        
        if response_get_storetypes.status_code == 200:
            storetypes_list = response_get_storetypes.json()["storetypes"]

            selectable_storetypes = {storetype[0]: False for storetype
                                     in storetypes_list}
            storetypes_refresh = {storetype[0]: True for storetype
                                  in storetypes_list}
            storetypes_changed = {storetype[0]: False for storetype
                                  in storetypes_list}
            show_selectable_storetypes = False

    if imgui.button("Show storetypes list"):
        if response_get_storetypes:
            if response_get_storetypes.status_code == 200:
                show_selectable_storetypes = True
        else:
            show_popup_get_storetypes_error = True
    
    if show_popup_get_storetypes_error:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        imgui.text("Load the storetypes list.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_get_storetypes_error = False
        imgui.end_popup()

    if show_selectable_storetypes:
        imgui.columns(count=15, identifier=None, border=False)
        for storetype in storetypes_list:
            label = storetype[0]
            _, selectable_storetypes[storetype[0]] = imgui.selectable(
                label, selectable_storetypes[storetype[0]])
            imgui.next_column()
        imgui.columns(1)

    for storetype in selectable_storetypes:
        if selectable_storetypes[storetype]:
            if storetypes_refresh[storetype]:
                storetypes_refresh[storetype] = False
                get_storetype_response = requests.get(
                    f"http://{host}:{port}/storetypes/get-storetype/{storetype}")
                info = get_storetype_response.json()["Data"][0]
                storetypes_info[storetype] = {
                    "storetype_description": info[1][:100]}
            
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
                response_update_storetype = requests.put(
                    f"http://{host}:{port}/storetypes/update-storetype",
                    json={"storetype_id": storetype,
                    "storetype_description": storetypes_info[storetype]["storetype_description"]})

    button_clicked_delete_storetypes = imgui.button("Delete storetypes")
    if button_clicked_delete_storetypes:
        button_clicked_delete_storetypes = False
        for storetype in selectable_storetypes:
            if selectable_storetypes[storetype]:
                response_delete_storetype = requests.delete(
                    f"http://{host}:{port}/storetypes/delete-storetype/{storetype}")
                if response_delete_storetype.status_code == 409:
                    show_popup_delete_error = True
    
    if show_popup_delete_error:
        imgui.open_popup("Integrity Error")
    if imgui.begin_popup_modal("Integrity Error")[0]:
        imgui.text(f"Record {storetype} could not be deleted because \
                   it is being referenced by a foreign key.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_delete_error = False
        imgui.end_popup()

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
        response_add_storetype = requests.post(
            f"http://{host}:{port}/storetypes/add-storetype",
            json=info_add_storetype)

    imgui.end()