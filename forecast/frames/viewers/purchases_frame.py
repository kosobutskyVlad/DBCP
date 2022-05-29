import requests

import imgui

from ..error_popup import error_popup

response_get_purchases = None
purchases_list = []
show_selectable_purchases = False
selectable_purchases = {}
purchases_info = {}
purchases_refresh = {}
purchases_changed = {}

show_error_popup = False
error_popup_message = ""

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

    global show_error_popup
    global error_popup_message

    global input_get_by_store_id
    global input_get_by_product_id

    imgui.begin("Purchases")

    show_error_popup = error_popup(show_error_popup, error_popup_message)

    imgui.push_item_width(100)
    _, input_get_by_store_id = imgui.input_text("Get by store_id",
                input_get_by_store_id, 6)

    _, input_get_by_product_id = imgui.input_text("Get by product_id",
                input_get_by_product_id, 6)
    imgui.pop_item_width()

    if imgui.button("Load purchases list"):
        try:
            if not input_get_by_store_id or not input_get_by_product_id:
                show_error_popup = True
                error_popup_message = "Specify both store_id and product_id."

            response_get_purchases = requests.get(
                f"http://{host}:{port}/purchases/get-purchases",
                params={"store_id": input_get_by_store_id,
                        "product_id": input_get_by_product_id})
            
            if response_get_purchases.status_code == 200:
                purchases_list = response_get_purchases.json()

                selectable_purchases = {purchase[0]: False for purchase in purchases_list}
                purchases_refresh = {purchase[0]: True for purchase in purchases_list}
                purchases_changed = {purchase[0]: False for purchase in purchases_list}
                show_selectable_purchases = False
                
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    if imgui.button("Show purchases list"):
        if response_get_purchases:
            if response_get_purchases.status_code == 200:
                show_selectable_purchases = True
        else:
            show_error_popup = True
            error_popup_message = "Load the purchases list first."

    if show_selectable_purchases:
        imgui.begin_child("purchases_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for purchase in purchases_list:
            label = str(purchase[0])
            _, selectable_purchases[purchase[0]] = imgui.selectable(
                label=label, selected=selectable_purchases[purchase[0]])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for i, purchase in enumerate(selectable_purchases):
        if selectable_purchases[purchase]:
            if purchases_refresh[purchase]:
                purchases_refresh[purchase] = False
                try:
                    get_purchase_response = requests.get(
                        f"http://{host}:{port}/purchases/get-purchase/",
                        params={"purchase_id": purchases_list[i][0]})
                    info = get_purchase_response.json()[0]
                    purchases_info[purchase] = {
                        "store_id": info[1],
                        "product_id": info[2],
                        "purchase_date": info[3],
                        "price": info[4],
                        "sales": info[5],
                        "discount": info[6],
                        "revenue": info[7]}
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."
                    purchases_list = []
                    show_selectable_purchases = False
                    selectable_purchases = {}
                    purchases_info = {}
                    purchases_refresh = {}
                    purchases_changed = {}

            if show_error_popup:
                break
            
            imgui.begin_child("purchases_editor", 1200, 200, border=True)
            imgui.text(purchases_list[i][2] if input_get_by_store_id else purchases_list[i][1])
            imgui.same_line()
            imgui.push_item_width(100)
            changed, purchases_info[purchase]["store_id"] = \
                imgui.input_text(f"{purchase}: store_id",
                purchases_info[purchase]["store_id"], 6)
            if changed:
                purchases_changed[purchase] = True
            imgui.same_line()
            changed, purchases_info[purchase]["product_id"] = \
                imgui.input_text(f"{purchase}: product_id",
                purchases_info[purchase]["product_id"], 6)
            if changed:
                purchases_changed[purchase] = True
            imgui.same_line()
            changed, purchases_info[purchase]["purchase_date"] = \
                imgui.input_text(f"{purchase}: purchase_date",
                purchases_info[purchase]["purchase_date"], 11)
            if changed:
                purchases_changed[purchase] = True
            imgui.same_line()
            changed, purchases_info[purchase]["price"] = \
                imgui.input_float(f"{purchase}: price",
                purchases_info[purchase]["price"], 0.01, 1)
            if changed:
                purchases_changed[purchase] = True
            imgui.same_line()
            changed, purchases_info[purchase]["sales"] = \
                imgui.input_int(f"{purchase}: sales",
                purchases_info[purchase]["sales"], 1, 10)
            if changed:
                purchases_changed[purchase] = True

            changed, purchases_info[purchase]["discount"] = \
                imgui.input_float(f"{purchase}: discount",
                purchases_info[purchase]["discount"], 0.01, 0.1)
            if changed:
                purchases_changed[purchase] = True
            imgui.same_line()
            changed, purchases_info[purchase]["revenue"] = \
                imgui.input_float(f"{purchase}: revenue",
                purchases_info[purchase]["revenue"], 0.01, 1)
            if changed:
                purchases_changed[purchase] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_purchases = imgui.button("Update purchases")
    if button_clicked_update_purchases:
        button_clicked_update_purchases = False
        for i, purchase in enumerate(purchases_changed):
            if purchases_changed[purchase]:
                try:
                    response_update_purchase = requests.put(
                        f"http://{host}:{port}/purchases/update-purchase",
                        json={"store_id": purchases_info[purchase]["store_id"],
                        "product_id": purchases_info[purchase]["product_id"],
                        "purchase_date": purchases_info[purchase]["purchase_date"],
                        "price": purchases_info[purchase]["price"],
                        "sales": purchases_info[purchase]["sales"],
                        "discount": purchases_info[purchase]["discount"],
                        "revenue": purchases_info[purchase]["revenue"]},
                        params={"purchase_id": purchases_list[i][0]})
                    if response_update_purchase.status_code != 200:
                        show_error_popup = True
                        error_popup_message = response_update_purchase.json()["detail"]
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    button_clicked_delete_purchases = imgui.button("Delete purchases")
    if button_clicked_delete_purchases:
        button_clicked_delete_purchases = False
        for i, purchases in enumerate(selectable_purchases):
            if selectable_purchases[purchases]:
                try:
                    response_delete_purchase = requests.delete(
                        f"http://{host}:{port}/purchases/delete-purchase/{purchases_list[i][0]}")
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

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
            response_add_purchase = requests.post(
                f"http://{host}:{port}/purchases/add-purchase", json=info_add_purchase)
            if response_add_purchase.status_code == 422:
                show_error_popup = True
                error_popup_message = response_add_purchase.json()["detail"]
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.end()