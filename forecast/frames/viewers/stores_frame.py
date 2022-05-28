import requests

import imgui

from ..error_popup import error_popup

response_get_stores = None
stores_list = []
show_selectable_stores = False
selectable_stores = {}
stores_info = {}
stores_refresh = {}
stores_changed = {}

show_error_popup = False
error_popup_message = ""

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

    global show_error_popup
    global error_popup_message

    imgui.begin("Stores")

    show_error_popup = error_popup(show_error_popup, error_popup_message)

    if imgui.button("Load stores list"):
        try:
            response_get_stores = requests.get(
                f"http://{host}:{port}/stores/get-stores")
            
            if response_get_stores.status_code == 200:
                stores_list = response_get_stores.json()

                selectable_stores = {store: False for store in stores_list}
                stores_refresh = {store: True for store in stores_list}
                stores_changed = {store: False for store in stores_list}
                show_selectable_stores = False

        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    if imgui.button("Show stores list"):
        if response_get_stores:
            if response_get_stores.status_code == 200:
                show_selectable_stores = True
        else:
            show_error_popup = True
            error_popup_message = "Load the stores list first."

    if show_selectable_stores:
        imgui.begin_child("stores_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for store in stores_list:
            label = store
            _, selectable_stores[store] = imgui.selectable(
                label=label, selected=selectable_stores[store])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for store in selectable_stores:
        if selectable_stores[store]:
            if stores_refresh[store]:
                stores_refresh[store] = False
                try:
                    get_store_response = requests.get(
                        f"http://{host}:{port}/stores/get-store/{store}")
                    info = get_store_response.json()[0]
                    stores_info[store] = {"storetype_id": info[1],
                                        "city_id": info[2],
                                        "store_size": info[3]}
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."
                    stores_list = []
                    show_selectable_stores = False
                    selectable_stores = {}
                    stores_info = {}
                    stores_refresh = {}
                    stores_changed = {}
            
            if show_error_popup:
                break
            
            imgui.begin_child("stores_editor", 1200, 200, border=True)
            imgui.text(store)
            imgui.same_line()
            imgui.push_item_width(100)
            changed, stores_info[store]["storetype_id"] = \
                imgui.input_text(f"{store}: storetype_id",
                stores_info[store]["storetype_id"], 5)
            if changed:
                stores_changed[store] = True
            imgui.same_line()
            changed, stores_info[store]["city_id"] = \
                imgui.input_text(f"{store}: city_id",
                stores_info[store]["city_id"], 5)
            if changed:
                stores_changed[store] = True
            imgui.same_line()
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
                try:
                    response_update_store = requests.put(
                        f"http://{host}:{port}/stores/update-store",
                        json={"store_id": store,
                        "storetype_id": stores_info[store]["storetype_id"],
                        "city_id": stores_info[store]["city_id"],
                        "store_size": stores_info[store]["store_size"]})
                    if response_update_store.status_code == 422:
                        show_error_popup = True
                        error_popup_message = response_update_store.json()["detail"]
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    button_clicked_delete_stores = imgui.button("Delete stores")
    if button_clicked_delete_stores:
        button_clicked_delete_stores = False
        for store in selectable_stores:
            if selectable_stores[store]:
                try:
                    response_delete_store = requests.delete(
                        f"http://{host}:{port}/stores/delete-store/{store}")
                    if response_delete_store.status_code == 409:
                        show_error_popup = True
                        error_popup_message = response_delete_store.json()["detail"]
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.push_item_width(100)
    _, info_add_store["store_id"] = imgui.input_text(
        "Add store_id", info_add_store["store_id"], 6)
    imgui.same_line()
    _, info_add_store["storetype_id"] = imgui.input_text(
        f"Add storetype_id", info_add_store["storetype_id"], 5)
    imgui.same_line()
    _, info_add_store["city_id"] = imgui.input_text(
        f"Add city_id", info_add_store["city_id"], 5)
    imgui.same_line()
    _, info_add_store["store_size"] = imgui.input_int(
        f"Add store_size", info_add_store["store_size"], 100, 1000)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_store = imgui.button("Add a store")
    if button_clicked_add_store:
        button_clicked_add_store = False
        try:
            response_add_store = requests.post(
                f"http://{host}:{port}/stores/add-store", json=info_add_store)
            if response_add_store.status_code == 422:
                show_error_popup = True
                error_popup_message = response_add_store.json()["detail"]
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.end()