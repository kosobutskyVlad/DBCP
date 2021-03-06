import requests

import imgui

from ..error_popup import error_popup

response_get_products = None
products_list = []
show_selectable_products = False
selectable_products = {}
products_info = {}
products_refresh = {}
products_changed = {}

show_error_popup = False
error_popup_message = ""

info_add_product = {
    "product_id": "",
    "product_name": "",
    "hierarchy_code": "",
    "price": 0.0,
    "product_length": 0.0,
    "product_depth": 0.0,
    "product_width": 0.0
}

def products_frame(host: str, port: int):
    global response_get_products
    global products_list
    global show_selectable_products
    global selectable_products
    global products_info
    global products_refresh
    global products_changed
    global info_add_product

    global show_error_popup
    global error_popup_message

    imgui.begin("Products")

    show_error_popup = error_popup(show_error_popup, error_popup_message)

    if imgui.button("Load products list"):
        try:
            response_get_products = requests.get(
                f"http://{host}:{port}/products/get-products")
            
            if response_get_products.status_code == 200:
                products_list = response_get_products.json()

                selectable_products = {product[0]: False for product in products_list}
                products_refresh = {product[0]: True for product in products_list}
                products_changed = {product[0]: False for product in products_list}
                show_selectable_products = False
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    if imgui.button("Show products list"):
        if response_get_products:
            if response_get_products.status_code == 200:
                show_selectable_products = True
        else:
            show_error_popup = True
            error_popup_message = "Load the products list first."

    if show_selectable_products:
        imgui.begin_child("products_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for product in products_list:
            label = product[0]
            _, selectable_products[product[0]] = imgui.selectable(
                label=label, selected=selectable_products[product[0]])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for product in selectable_products:
        if selectable_products[product]:
            if products_refresh[product]:
                products_refresh[product] = False
                try:
                    get_product_response = requests.get(
                        f"http://{host}:{port}/products/get-product/{product}")
                    info = get_product_response.json()[0]
                    products_info[product] = {
                        "product_name": info[1],
                        "hierarchy_code": info[2],
                        "price": info[3],
                        "product_length": info[4],
                        "product_depth": info[5],
                        "product_width": info[6]}
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."
                    products_list = []
                    show_selectable_products = False
                    selectable_products = {}
                    products_info = {}
                    products_refresh = {}
                    products_changed = {}
            
            if error_popup_message:
                break

            imgui.begin_child("products_editor", 1200, 200, border=True)
            imgui.text(product)
            imgui.same_line()
            imgui.push_item_width(300)
            changed, products_info[product]["product_name"] = \
                imgui.input_text(f"{product}: product_name",
                products_info[product]["product_name"], 51)
            if changed:
                products_changed[product] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, products_info[product]["hierarchy_code"] = \
                imgui.input_text(f"{product}: hierarchy_code",
                products_info[product]["hierarchy_code"], 12)
            if changed:
                products_changed[product] = True
            
            changed, products_info[product]["price"] = \
                imgui.input_float(f"{product}: price",
                products_info[product]["price"], 0.01, 1)
            if changed:
                products_changed[product] = True
            imgui.same_line()
            changed, products_info[product]["product_length"] = \
                imgui.input_float(f"{product}: product_length",
                products_info[product]["product_length"], 0.1, 1)
            if changed:
                products_changed[product] = True
            imgui.same_line()
            changed, products_info[product]["product_depth"] = \
                imgui.input_float(f"{product}: product_depth",
                products_info[product]["product_depth"], 0.1, 1)
            if changed:
                products_changed[product] = True
            imgui.same_line()
            changed, products_info[product]["product_width"] = \
                imgui.input_float(f"{product}: product_width",
                products_info[product]["product_width"], 0.1, 1)
            if changed:
                products_changed[product] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_products = imgui.button("Update products")
    if button_clicked_update_products:
        button_clicked_update_products = False
        for product in products_changed:
            if products_changed[product]:
                try:
                    response_update_product = requests.put(
                        f"http://{host}:{port}/products/update-product",
                        json={"product_id": product,
                        "product_name": products_info[product]["product_name"],
                        "hierarchy_code": products_info[product]["hierarchy_code"],
                        "price": products_info[product]["price"],
                        "product_length": products_info[product]["product_length"],
                        "product_depth": products_info[product]["product_depth"],
                        "product_width": products_info[product]["product_width"]})
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    button_clicked_delete_products = imgui.button("Delete products")
    if button_clicked_delete_products:
        button_clicked_delete_products = False
        for product in selectable_products:
            if selectable_products[product]:
                try:
                    response_delete_product = requests.delete(
                        f"http://{host}:{port}/products/delete-product/{product}")
                    if response_delete_product.status_code == 409:
                        show_error_popup = True
                        error_popup_message = response_delete_product.json()["detail"]
                except requests.exceptions.ConnectionError:
                    show_error_popup = True
                    error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.push_item_width(50)
    _, info_add_product["product_id"] = imgui.input_text(
        "Add product_id", info_add_product["product_id"], 6)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(300)
    _, info_add_product["product_name"] = imgui.input_text(
        f"Add product_name", info_add_product["product_name"], 51)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_product["hierarchy_code"] = imgui.input_text(
        f"Add hierarchy_code", info_add_product["hierarchy_code"], 12)

    _, info_add_product["price"] = imgui.input_float(
        f"Add price", info_add_product["price"], 0.01, 1)
    imgui.same_line()
    _, info_add_product["product_length"] = imgui.input_float(
        f"Add product length", info_add_product["product_length"], 0.1, 1)
    imgui.same_line()
    _, info_add_product["product_depth"] = imgui.input_float(
        f"Add product depth", info_add_product["product_depth"], 0.1, 1)
    imgui.same_line()
    _, info_add_product["product_width"] = imgui.input_float(
        f"Add product width", info_add_product["product_width"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_product = imgui.button("Add a product")
    if button_clicked_add_product:
        button_clicked_add_product = False
        try:
            response_add_product = requests.post(
                f"http://{host}:{port}/products/add-product", json=info_add_product)

            if response_add_product.status_code == 422:
                show_error_popup = True
                error_popup_message = response_add_product.json()["detail"]
                print(error_popup_message)
        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    imgui.end()