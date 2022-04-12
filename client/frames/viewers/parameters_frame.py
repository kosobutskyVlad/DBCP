import requests

import imgui

from ..error_popups import (
    popup_server_down,
    popup_load_list,
    popup_already_exists,
    popup_deletion_rejected,
    popup_not_found,
    popup_argument_missing)

response_get_parameters = None
parameters_list = []
show_selectable_parameters = False
selectable_parameters = {}
parameters_info = {}
parameters_refresh = {}
parameters_changed = {}

show_popup_server_down = False
show_popup_argument_missing = False
show_popup_load_list = False
show_popup_already_exists = False
show_popup_not_found = False
item_id = ""

input_get_by_store_id = ""
input_get_by_product_id = ""

info_add_parameters = {
    "store_id": "",
    "product_id": "",
    "loyalty_charge_x": 0.0,
    "loyalty_charge_coef": 0.0,
    "storage_cost_coef": 0.0,
    "bank_rate_x": 0.0,
    "bank_rate_coef": 0.0,
    "product_cost_x": 0.0,
    "product_cost_coef": 0.0
}

def parameters_frame(host: str, port: int):
    global response_get_parameters
    global parameters_list
    global show_selectable_parameters
    global selectable_parameters
    global parameters_info
    global parameters_refresh
    global parameters_changed
    global info_add_parameters

    global show_popup_server_down
    global show_popup_argument_missing
    global show_popup_load_list
    global show_popup_already_exists
    global show_popup_not_found
    global item_id

    global input_get_by_store_id
    global input_get_by_product_id

    imgui.begin("Loss function parameters")

    show_popup_server_down = popup_server_down(show_popup_server_down)
    show_popup_argument_missing = popup_argument_missing(
        show_popup_argument_missing)
    show_popup_load_list = popup_load_list(
        show_popup_load_list, "stores")
    show_popup_already_exists = popup_already_exists(
        show_popup_already_exists, item_id)
    show_popup_not_found = popup_not_found(
        show_popup_not_found, item_id)

    imgui.push_item_width(100)
    _, input_get_by_store_id = imgui.input_text("Get by store_id",
                input_get_by_store_id, 6)

    _, input_get_by_product_id = imgui.input_text("Get by product_id",
                input_get_by_product_id, 6)
    imgui.pop_item_width()

    if imgui.button("Load parameters list"):
        try:
            response_get_parameters = requests.get(
                f"http://{host}:{port}/parameters/get-parameters",
                params={"store_id": input_get_by_store_id,
                "product_id": input_get_by_product_id})
            
            if response_get_parameters.status_code == 200:
                parameters_list = response_get_parameters.json()["parameters"]

                selectable_parameters = {parameters[0]: False for parameters in parameters_list}
                parameters_refresh = {parameters[0]: True for parameters in parameters_list}
                parameters_changed = {parameters[0]: False for parameters in parameters_list}
                show_selectable_parameters = False
            else:
                show_popup_argument_missing = True
        except requests.exceptions.ConnectionError:
            show_popup_server_down = True 

    if imgui.button("Show parameters list"):
        if response_get_parameters:
            if response_get_parameters.status_code == 200:
                show_selectable_parameters = True
        else:
            show_popup_load_list = True

    if show_selectable_parameters:
        imgui.begin_child("parameters_list", 1200, 200, border=True)
        imgui.columns(count=15, identifier=None, border=False)
        for parameters in parameters_list:
            label = parameters[1] if input_get_by_product_id else parameters[2]
            _, selectable_parameters[parameters[0]] = imgui.selectable(
                label=label, selected=selectable_parameters[parameters[0]])
            imgui.next_column()
        imgui.columns(1)
        imgui.end_child()

    for i, parameters in enumerate(selectable_parameters):
        if selectable_parameters[parameters]:
            if parameters_refresh[parameters]:
                parameters_refresh[parameters] = False
                try:
                    get_parameters_response = requests.get(
                        f"http://{host}:{port}/parameters/get-parameters/",
                        params={"store_id": input_get_by_store_id or parameters_list[i][1],
                        "product_id": input_get_by_product_id or parameters_list[i][2]})
                    info = get_parameters_response.json()["parameters"][0]
                    parameters_info[parameters] = {
                        "store_id": info[1][:5],
                        "product_id": info[2][:5],
                        "loyalty_charge_x": info[3],
                        "loyalty_charge_coef": info[4],
                        "storage_cost_coef": info[5],
                        "bank_rate_x": info[6],
                        "bank_rate_coef": info[7],
                        "product_cost_x": info[8],
                        "product_cost_coef": info[9]}
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True
                    parameters_list = []
                    show_selectable_parameters = False
                    selectable_parameters = {}
                    parameters_info = {}
                    parameters_refresh = {}
                    parameters_changed = {}

            if show_popup_server_down:
                break
            
            imgui.begin_child("parameters_editor", 1200, 200, border=True)
            imgui.text(parameters_list[i][2] if input_get_by_store_id else parameters_list[i][1])
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["store_id"] = \
                imgui.input_text(f"{parameters}: store_id",
                parameters_info[parameters]["store_id"], 6)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["product_id"] = \
                imgui.input_text(f"{parameters}: product_id",
                parameters_info[parameters]["product_id"], 6)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["loyalty_charge_x"] = \
                imgui.input_float(f"{parameters}: loyalty_charge_x",
                parameters_info[parameters]["loyalty_charge_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["loyalty_charge_coef"] = \
                imgui.input_float(f"{parameters}: loyalty_charge_coef",
                parameters_info[parameters]["loyalty_charge_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["storage_cost_coef"] = \
                imgui.input_float(f"{parameters}: storage_cost_coef",
                parameters_info[parameters]["storage_cost_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True

            changed, parameters_info[parameters]["bank_rate_x"] = \
                imgui.input_float(f"{parameters}: bank_rate_x",
                parameters_info[parameters]["bank_rate_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["bank_rate_coef"] = \
                imgui.input_float(f"{parameters}: bank_rate_coef",
                parameters_info[parameters]["bank_rate_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["product_cost_x"] = \
                imgui.input_float(f"{parameters}: product_cost_x",
                parameters_info[parameters]["product_cost_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.same_line()
            changed, parameters_info[parameters]["product_cost_coef"] = \
                imgui.input_float(f"{parameters}: product_cost_coef",
                parameters_info[parameters]["product_cost_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_parameters = imgui.button("Update parameters")
    if button_clicked_update_parameters:
        button_clicked_update_parameters = False
        for parameters in parameters_changed:
            if parameters_changed[parameters]:
                try:
                    response_update_parameters = requests.put(
                        f"http://{host}:{port}/parameters/update-parameters",
                        json={"store_id": parameters_info[parameters]["store_id"],
                        "product_id": parameters_info[parameters]["product_id"],
                        "loyalty_charge_x": parameters_info[parameters]["loyalty_charge_x"],
                        "loyalty_charge_coef": parameters_info[parameters]["loyalty_charge_coef"],
                        "storage_cost_coef": parameters_info[parameters]["storage_cost_coef"],
                        "bank_rate_x": parameters_info[parameters]["bank_rate_x"],
                        "bank_rate_coef": parameters_info[parameters]["bank_rate_coef"],
                        "product_cost_x": parameters_info[parameters]["product_cost_x"],
                        "product_cost_coef": parameters_info[parameters]["product_cost_coef"]})
                    if response_update_parameters.status_code == 422:
                        show_popup_not_found = True
                        item_id = " ".join(response_update_parameters.json()["detail"].split(" ")[:3])
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

    button_clicked_delete_parameters = imgui.button("Delete parameters")
    if button_clicked_delete_parameters:
        button_clicked_delete_parameters = False
        for parameters in selectable_parameters:
            if selectable_parameters[parameters]:
                try:
                    response_delete_parameters = requests.delete(
                        f"http://{host}:{port}/parameters/delete-parameters",
                        params={"store_id": input_get_by_store_id,
                        "product_id": input_get_by_product_id})
                except requests.exceptions.ConnectionError:
                    show_popup_server_down = True

    imgui.push_item_width(100)
    _, info_add_parameters["store_id"] = \
        imgui.input_text("store_id",
        info_add_parameters["store_id"], 6)
    imgui.same_line()
    _, info_add_parameters["product_id"] = \
        imgui.input_text("product_id",
        info_add_parameters["product_id"], 6)
    imgui.same_line()
    _, info_add_parameters["loyalty_charge_x"] = \
        imgui.input_float("loyalty_charge_x",
        info_add_parameters["loyalty_charge_x"], 0.1, 1)
    imgui.same_line()
    _, info_add_parameters["loyalty_charge_coef"] = \
        imgui.input_float("loyalty_charge_coef",
        info_add_parameters["loyalty_charge_coef"], 0.1, 1)
    imgui.same_line()
    _, info_add_parameters["storage_cost_coef"] = \
        imgui.input_float("storage_cost_coef",
        info_add_parameters["storage_cost_coef"], 0.1, 1)

    _, info_add_parameters["bank_rate_x"] = \
        imgui.input_float("bank_rate_x",
        info_add_parameters["bank_rate_x"], 0.1, 1)
    imgui.same_line()
    _, info_add_parameters["bank_rate_coef"] = \
        imgui.input_float("bank_rate_coef",
        info_add_parameters["bank_rate_coef"], 0.1, 1)
    imgui.same_line()
    _, info_add_parameters["product_cost_x"] = \
        imgui.input_float("product_cost_x",
        info_add_parameters["product_cost_x"], 0.1, 1)
    imgui.same_line()
    _, info_add_parameters["product_cost_coef"] = \
        imgui.input_float("product_cost_coef",
        info_add_parameters["product_cost_coef"], 0.1, 1)
    imgui.same_line()

    button_clicked_add_parameters = imgui.button("Add parameters")
    if button_clicked_add_parameters:
        button_clicked_add_parameters = False
        try:
            response_add_parameters = requests.post(
                f"http://{host}:{port}/parameters/add-parameters", json=info_add_parameters)
            if response_add_parameters.status_code == 422:
                if "already exists" in response_add_parameters.json()["detail"]:
                    show_popup_already_exists = True
                    item_id = f"{info_add_parameters['store_id']} and {info_add_parameters['product_id']}"
                else:
                    show_popup_not_found = True
                    item_id = response_add_parameters.json()["detail"].split(" ")[0]
        except requests.exceptions.ConnectionError:
            show_popup_server_down = True

    imgui.end()