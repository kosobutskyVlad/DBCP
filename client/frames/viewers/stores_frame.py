import requests

import imgui

response_get_stores = None
stores_list = []
show_selectable_stores = False
selectable_stores = {}
stores_info = {}
stores_refresh = {}
stores_changed = {}

show_popup_get_stores_error = False
show_popup_delete_error = False

info_add_store = {
    "store_id": "",
    "storetype_id": "",
    "city_id": "",
    "store_size": 0
}

def stores_frame(host: str, port: int):
    global response_get_stores
    global stores_list
    global show_selectable_stores
    global selectable_stores
    global stores_info
    global stores_refresh
    global stores_changed
    global info_add_store

    global show_popup_get_stores_error
    global show_popup_delete_error

    imgui.begin("Stores")

    if imgui.button("Load stores list"):
        response_get_stores = requests.get(
            f"http://{host}:{port}/stores/get-stores")
        
        if response_get_stores.status_code == 200:
            stores_list = response_get_stores.json()["stores"]

            selectable_stores = {store[0]: False for store in stores_list}
            stores_refresh = {store[0]: True for store in stores_list}
            stores_changed = {store[0]: False for store in stores_list}
            show_selectable_stores = False

    if imgui.button("Show stores list"):
        if response_get_stores:
            if response_get_stores.status_code == 200:
                show_selectable_stores = True
        else:
            show_popup_get_stores_error = True
    
    if show_popup_get_stores_error:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        imgui.text("Load the stores list.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_get_stores_error = False
        imgui.end_popup()

    if show_selectable_stores:
        imgui.columns(count=15, identifier=None, border=False)
        for store in stores_list:
            label = store[0]
            _, selectable_stores[store[0]] = imgui.selectable(
                label=label, selected=selectable_stores[store[0]])
            imgui.next_column()
        imgui.columns(1)

    for store in selectable_stores:
        if selectable_stores[store]:
            if stores_refresh[store]:
                stores_refresh[store] = False
                get_store_response = requests.get(
                    f"http://{host}:{port}/stores/get-store/{store}")
                info = get_store_response.json()["Data"][0]
                stores_info[store] = {"storetype_id": info[1][:4],
                                     "city_id": info[2][:4],
                                     "store_size": info[3]}
            
            imgui.begin_child("stores_editor", 1200, 200, border=True)
            imgui.text(store)
            imgui.same_line()
            imgui.push_item_width(300)
            changed, stores_info[store]["storetype_id"] = \
                imgui.input_text(f"{store}: storetype_id",
                stores_info[store]["storetype_id"], 5)
            if changed:
                stores_changed[store] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, stores_info[store]["city_id"] = \
                imgui.input_text(f"{store}: city_id",
                stores_info[store]["city_id"], 5)
            if changed:
                stores_changed[store] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, stores_info[store]["store_size"] = \
                imgui.input_int(f"{store}: store_size",
                stores_info[store]["store_size"], 100, 1000)
            if changed:
                stores_changed[store] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_stores = imgui.button("Update stores")
    if button_clicked_update_stores:
        button_clicked_update_stores = False
        for store in stores_changed:
            if stores_changed[store]:
                response_update_store = requests.put(
                    f"http://{host}:{port}/stores/update-store",
                    json={"store_id": store,
                    "storetype_id": stores_info[store]["storetype_id"],
                    "city_id": stores_info[store]["city_id"],
                    "store_size": stores_info[store]["store_size"]})

    button_clicked_delete_stores = imgui.button("Delete stores")
    if button_clicked_delete_stores:
        button_clicked_delete_stores = False
        for store in selectable_stores:
            if selectable_stores[store]:
                response_delete_store = requests.delete(
                    f"http://{host}:{port}/stores/delete-store/{store}")
                if response_delete_store.status_code == 409:
                    show_popup_delete_error = True
    
    if show_popup_delete_error:
        imgui.open_popup("Integrity Error")
    if imgui.begin_popup_modal("Integrity Error")[0]:
        imgui.text(f"Record {store} could not be deleted because \
                   it is being referenced by a foreign key.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_delete_error = False
        imgui.end_popup()

    imgui.push_item_width(50)
    _, info_add_store["store_id"] = imgui.input_text(
        "Add store_id", info_add_store["store_id"], 6)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(300)
    _, info_add_store["storetype_id"] = imgui.input_text(
        f"Add storetype_id", info_add_store["storetype_id"], 5)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_store["city_id"] = imgui.input_text(
        f"Add city_id", info_add_store["city_id"], 5)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_store["store_size"] = imgui.input_int(
        f"Add store_size", info_add_store["store_size"], 100, 1000)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_store = imgui.button("Add a store")
    if button_clicked_add_store:
        button_clicked_add_store = False
        response_add_store = requests.post(
            f"http://{host}:{port}/stores/add-store", json=info_add_store)

    imgui.end()