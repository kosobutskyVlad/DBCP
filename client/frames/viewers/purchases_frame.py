import requests

import imgui

from ..error_popups import (
    popup_server_down,
    popup_load_list,
    popup_not_found,
    popup_argument_missing)

response_get_purchases = None
purchases_list = []
show_selectable_purchases = False
selectable_purchases = {}
purchases_info = {}
purchases_refresh = {}
purchases_changed = {}

show_popup_server_down = False
show_popup_argument_missing = False
show_popup_load_list = False
show_popup_already_exists = False
show_popup_not_found = False
item_id = ""

input_get_by_store_id = ""
input_get_by_product_id = ""

info_add_purchase = {
    "store_id": "",
    "product_id": "",
    "purchase_date": "",
    "price": 0.0,
    "sales": 0,
    "discount": 0.0,
    "revenue": 0.0
}

def purchases_frame(host: str, port: int):
    global response_get_purchases
    global purchases_list
    global show_selectable_purchases
    global selectable_purchases
    global purchases_info
    global purchases_refresh
    global purchases_changed
    global info_add_purchase

    global show_popup_server_down
    global show_popup_argument_missing
    global show_popup_load_list
    global show_popup_already_exists
    global show_popup_not_found
    global item_id

    global input_get_by_store_id
    global input_get_by_product_id

    imgui.begin("Purchases")

    show_popup_server_down = popup_server_down(show_popup_server_down)
    show_popup_argument_missing = popup_argument_missing(
        show_popup_argument_missing)
    show_popup_load_list = popup_load_list(
        show_popup_load_list, "purchases")
    show_popup_not_found = popup_not_found(
        show_popup_not_found, item_id)

    imgui.push_item_width(100)
    _, input_get_by_store_id = imgui.input_text("Get by store_id",
                input_get_by_store_id, 6)

    _, input_get_by_product_id = imgui.input_text("Get by product_id",
                input_get_by_product_id, 6)
    imgui.pop_item_width()

    if imgui.button("Load purchases list"):
        try:
            response_get_purchases = requests.get(
                f"http://{host}:{port}/purchases/get-purchases")
            
            if response_get_purchases.status_code == 200:
                purchases_list = response_get_purchases.json()["purchases"]

                selectable_purchases = {purchase[0]: False for purchase in purchases_list}
                purchases_refresh = {purchase[0]: True for purchase in purchases_list}
                purchases_changed = {purchase[0]: False for purchase in purchases_list}
                show_selectable_purchases = False
            else:
                show_popup_argument_missing = True
        except requests.exceptions.ConnectionError:
            show_popup_server_down = True 

    if imgui.button("Show purchases list"):
        if response_get_purchases:
            if response_get_purchases.status_code == 200:
                show_selectable_purchases = True
        else:
            show_popup_load_list = True

    if show_selectable_purchases:
        imgui.begin_child("purchases_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for purchase in purchases_list:
            label = purchase[0]
            _, selectable_purchases[purchase[0]] = imgui.selectable(
                label=label, selected=selectable_purchases[purchase[0]])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for i, purchase in enumerate(selectable_purchases):
        if selectable_purchases[purchases]:
            if purchases_refresh[purchases]:
                purchases_refresh[purchases] = False
                try:
                    get_purchases_response = requests.get(
                        f"http://{host}:{port}/purchases/get-purchases/",
                        params={"store_id": input_get_by_store_id or purchases_list[i][1],
                        "product_id": input_get_by_product_id or purchases_list[i][2]})
                    info = get_purchases_response.json()["purchases"][0]
                    purchases_info[purchases] = {
                        "store_id": info[1][:5],
                        "product_id": info[2][:5],
                        "purchase_date": info[3],
                        "price": info[4],
                        "sales": info[5],
                        "discount": info[6],
                        "revenue": info[7]}
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True
                    purchases_list = []
                    show_selectable_purchases = False
                    selectable_purchases = {}
                    purchases_info = {}
                    purchases_refresh = {}
                    purchases_changed = {}

            if show_popup_server_down:
                break
            
            imgui.begin_child("purchases_editor", 1200, 200, border=True)
            imgui.text(purchases_list[i][2] if input_get_by_store_id else purchases_list[i][1])
            imgui.same_line()
            imgui.push_item_width(100)
            changed, purchases_info[purchases]["store_id"] = \
                imgui.input_text(f"{purchases}: store_id",
                purchases_info[purchases]["store_id"], 6)
            if changed:
                purchases_changed[purchases] = True
            imgui.same_line()
            changed, purchases_info[purchases]["product_id"] = \
                imgui.input_text(f"{purchases}: product_id",
                purchases_info[purchases]["product_id"], 6)
            if changed:
                purchases_changed[purchases] = True
            imgui.same_line()
            changed, purchases_info[purchases]["purchase_date"] = \
                imgui.input_text(f"{purchases}: purchase_date",
                purchases_info[purchases]["purchase_date"], 11)
            if changed:
                purchases_changed[purchases] = True
            imgui.same_line()
            changed, purchases_info[purchases]["price"] = \
                imgui.input_float(f"{purchases}: price",
                purchases_info[purchases]["price"], 0.01, 1)
            if changed:
                purchases_changed[purchases] = True
            imgui.same_line()
            changed, purchases_info[purchases]["sales"] = \
                imgui.input_int(f"{purchases}: sales",
                purchases_info[purchases]["sales"], 1, 10)
            if changed:
                purchases_changed[purchases] = True

            changed, purchases_info[purchases]["discount"] = \
                imgui.input_float(f"{purchases}: discount",
                purchases_info[purchases]["discount"], 0.01, 0.1)
            if changed:
                purchases_changed[purchases] = True
            imgui.same_line()
            changed, purchases_info[purchases]["revenue"] = \
                imgui.input_float(f"{purchases}: revenue",
                purchases_info[purchases]["revenue"], 0.01, 1)
            if changed:
                purchases_changed[purchases] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_purchases = imgui.button("Update purchases")
    if button_clicked_update_purchases:
        button_clicked_update_purchases = False
        for i, purchases in enumerate(purchases_changed):
            if purchases_changed[purchases]:
                try:
                    response_update_purchases = requests.put(
                        f"http://{host}:{port}/purchases/update-purchase/{purchases_list[i][0]}",
                        json={"store_id": purchases_info[purchases]["store_id"],
                        "product_id": purchases_info[purchases]["product_id"],
                        "loyalty_charge_x": purchases_info[purchases]["loyalty_charge_x"],
                        "loyalty_charge_coef": purchases_info[purchases]["loyalty_charge_coef"],
                        "storage_cost_coef": purchases_info[purchases]["storage_cost_coef"],
                        "bank_rate_x": purchases_info[purchases]["bank_rate_x"],
                        "bank_rate_coef": purchases_info[purchases]["bank_rate_coef"],
                        "product_cost_x": purchases_info[purchases]["product_cost_x"],
                        "product_cost_coef": purchases_info[purchases]["product_cost_coef"]})
                    if response_update_purchases.status_code == 422:
                        show_popup_not_found = True
                        item_id = response_update_purchases.json()["detail"].split(" ")[0]
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

    button_clicked_delete_purchases = imgui.button("Delete purchases")
    if button_clicked_delete_purchases:
        button_clicked_delete_purchases = False
        for i, purchases in enumerate(selectable_purchases):
            if selectable_purchases[purchases]:
                try:
                    response_delete_purchases = requests.delete(
                        f"http://{host}:{port}/purchases/delete-purchase/{purchases_list[i][0]}")
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

    imgui.push_item_width(100)
    _, info_add_purchase["store_id"] = \
        imgui.input_text("store_id",
        info_add_purchase["store_id"], 6)
    imgui.same_line()
    _, info_add_purchase["product_id"] = \
        imgui.input_text("product_id",
        info_add_purchase["product_id"], 6)
    imgui.same_line()
    _, info_add_purchase["purchase_date"] = \
        imgui.input_text("purchase_date",
        info_add_purchase["purchase_date"], 11)
    imgui.same_line()
    _, info_add_purchase["price"] = \
        imgui.input_float("price",
        info_add_purchase["price"], 0.01, 1)
    imgui.same_line()
    _, info_add_purchase["sales"] = \
        imgui.input_int("sales",
        info_add_purchase["sales"], 1, 10)

    _, info_add_purchase["discount"] = \
        imgui.input_float("discount",
        info_add_purchase["discount"], 0.01, 0.1)
    imgui.same_line()
    _, info_add_purchase["revenue"] = \
        imgui.input_float("revenue",
        info_add_purchase["revenue"], 0.01, 1)
    imgui.same_line()

    button_clicked_add_purchases = imgui.button("Add purchases")
    if button_clicked_add_purchases:
        button_clicked_add_purchases = False
        try:
            response_add_purchases = requests.post(
                f"http://{host}:{port}/purchases/add-purchase", json=info_add_purchase)
            if response_add_purchases.status_code == 422:
                if "already exists" in response_add_purchases.json()["detail"]:
                    show_popup_not_found = True
                    item_id = response_add_purchases.json()["detail"].split(" ")[0]
        except requests.exceptions.ConnectionError:
            show_popup_server_down = True

    imgui.end()