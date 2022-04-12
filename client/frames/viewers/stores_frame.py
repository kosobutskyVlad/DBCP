import requests

import imgui

from ..error_popups import (
    popup_server_down,
    popup_load_list,
    popup_already_exists,
    popup_deletion_rejected,
    popup_not_found)

response_get_stores = None
stores_list = []
show_selectable_stores = False
selectable_stores = {}
stores_info = {}
stores_refresh = {}
stores_changed = {}

show_popup_server_down = False
show_popup_load_list = False
show_popup_already_exists = False
show_popup_deletion_rejected = False
show_popup_not_found = False
item_id = ""

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

    global show_popup_server_down
    global show_popup_load_list
    global show_popup_already_exists
    global show_popup_deletion_rejected
    global show_popup_not_found
    global item_id

    imgui.begin("Stores")

    show_popup_server_down = popup_server_down(show_popup_server_down)
    show_popup_load_list = popup_load_list(
        show_popup_load_list, "stores")
    show_popup_already_exists = popup_already_exists(
        show_popup_already_exists, item_id)
    show_popup_deletion_rejected = popup_deletion_rejected(
        show_popup_deletion_rejected, item_id)
    show_popup_not_found = popup_not_found(
        show_popup_not_found, item_id)

    if imgui.button("Load stores list"):
        try:
            response_get_stores = requests.get(
                f"http://{host}:{port}/stores/get-stores")
            
            if response_get_stores.status_code == 200:
                stores_list = response_get_stores.json()["stores"]

                selectable_stores = {store[0]: False for store in stores_list}
                stores_refresh = {store[0]: True for store in stores_list}
                stores_changed = {store[0]: False for store in stores_list}
                show_selectable_stores = False

        except requests.exceptions.ConnectionError:
            show_popup_server_down = True 

    if imgui.button("Show stores list"):
        if response_get_stores:
            if response_get_stores.status_code == 200:
                show_selectable_stores = True
        else:
            show_popup_load_list = True

    if show_selectable_stores:
        imgui.begin_child("stores_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for store in stores_list:
            label = store[0]
            _, selectable_stores[store[0]] = imgui.selectable(
                label=label, selected=selectable_stores[store[0]])
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
                    info = get_store_response.json()["Data"][0]
                    stores_info[store] = {"storetype_id": info[1][:4],
                                        "city_id": info[2][:4],
                                        "store_size": info[3]}
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True
                    stores_list = []
                    show_selectable_stores = False
                    selectable_stores = {}
                    stores_info = {}
                    stores_refresh = {}
                    stores_changed = {}
            
            if show_popup_server_down:
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
                        show_popup_not_found = True
                        item_id = response_update_store.json()["detail"].split(" ")[0]
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

    button_clicked_delete_stores = imgui.button("Delete stores")
    if button_clicked_delete_stores:
        button_clicked_delete_stores = False
        for store in selectable_stores:
            if selectable_stores[store]:
                try:
                    response_delete_store = requests.delete(
                        f"http://{host}:{port}/stores/delete-store/{store}")
                    if response_delete_store.status_code == 409:
                        show_popup_deletion_rejected = True
                        item_id = store
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

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
                if "already exists" in response_add_store.json()["detail"]:
                    show_popup_already_exists = True
                    item_id = info_add_store["store_id"]
                else:
                    show_popup_not_found = True
                    item_id = response_add_store.json()["detail"].split(" ")[0]
        except requests.exceptions.ConnectionError:
            show_popup_server_down = True

    imgui.end()