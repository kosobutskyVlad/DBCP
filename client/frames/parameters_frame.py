import requests

import imgui

response_get_parameters = None
parameters_list = []
show_selectable_parameters = False
selectable_parameters = {}
parameters_info = {}
parameters_refresh = {}
parameters_changed = {}

show_popup_get_parameters_error = False

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

    global show_popup_get_parameters_error

    global input_get_by_store_id
    global input_get_by_product_id

    imgui.begin("Loss function parameters")

    imgui.push_item_width(100)
    _, input_get_by_store_id = imgui.input_text("Get by store_id",
                input_get_by_store_id, 6)

    _, input_get_by_product_id = imgui.input_text("Get by product_id",
                input_get_by_product_id, 6)
    imgui.pop_item_width()

    if imgui.button("Load parameters list"):
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

    if imgui.button("Show parameters list"):
        if response_get_parameters:
            if response_get_parameters.status_code == 200:
                show_selectable_parameters = True
        else:
            show_popup_get_parameters_error = True
    
    if show_popup_get_parameters_error:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        imgui.text("Load the parameters list.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_get_parameters_error = False
        imgui.end_popup()

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
            
            imgui.begin_child("parameters_editor", 1200, 200, border=True)
            imgui.text(f"id: {parameters}")
            imgui.same_line()
            imgui.push_item_width(50)
            changed, parameters_info[parameters]["store_id"] = \
                imgui.input_text(f"{parameters}: store_id",
                parameters_info[parameters]["store_id"], 6)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(50)
            changed, parameters_info[parameters]["product_id"] = \
                imgui.input_text(f"{parameters}: product_id",
                parameters_info[parameters]["product_id"], 6)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["loyalty_charge_x"] = \
                imgui.input_float(f"{parameters}: loyalty_charge_x",
                parameters_info[parameters]["loyalty_charge_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["loyalty_charge_coef"] = \
                imgui.input_float(f"{parameters}: loyalty_charge_coef",
                parameters_info[parameters]["loyalty_charge_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["storage_cost_coef"] = \
                imgui.input_float(f"{parameters}: storage_cost_coef",
                parameters_info[parameters]["storage_cost_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["bank_rate_x"] = \
                imgui.input_float(f"{parameters}: bank_rate_x",
                parameters_info[parameters]["bank_rate_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["bank_rate_coef"] = \
                imgui.input_float(f"{parameters}: bank_rate_coef",
                parameters_info[parameters]["bank_rate_coef"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, parameters_info[parameters]["product_cost_x"] = \
                imgui.input_float(f"{parameters}: product_cost_x",
                parameters_info[parameters]["product_cost_x"], 0.1, 1)
            if changed:
                parameters_changed[parameters] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
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

    button_clicked_delete_parameters = imgui.button("Delete parameters")
    if button_clicked_delete_parameters:
        button_clicked_delete_parameters = False
        for parameters in selectable_parameters:
            if selectable_parameters[parameters]:
                response_delete_parameters = requests.delete(
                    f"http://{host}:{port}/parameters/delete-parameters",
                    params={"store_id": input_get_by_store_id,
                    "product_id": input_get_by_product_id})

    imgui.push_item_width(50)
    _, info_add_parameters["store_id"] = \
        imgui.input_text("store_id",
        info_add_parameters["store_id"], 6)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(50)
    _, info_add_parameters["product_id"] = \
        imgui.input_text("product_id",
        info_add_parameters["product_id"], 6)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["loyalty_charge_x"] = \
        imgui.input_float("loyalty_charge_x",
        info_add_parameters["loyalty_charge_x"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["loyalty_charge_coef"] = \
        imgui.input_float("loyalty_charge_coef",
        info_add_parameters["loyalty_charge_coef"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["storage_cost_coef"] = \
        imgui.input_float("storage_cost_coef",
        info_add_parameters["storage_cost_coef"], 0.1, 1)
    imgui.pop_item_width()
    imgui.push_item_width(100)
    _, info_add_parameters["bank_rate_x"] = \
        imgui.input_float("bank_rate_x",
        info_add_parameters["bank_rate_x"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["bank_rate_coef"] = \
        imgui.input_float("bank_rate_coef",
        info_add_parameters["bank_rate_coef"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["product_cost_x"] = \
        imgui.input_float("product_cost_x",
        info_add_parameters["product_cost_x"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_parameters["product_cost_coef"] = \
        imgui.input_float("product_cost_coef",
        info_add_parameters["product_cost_coef"], 0.1, 1)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_parameters = imgui.button("Add parameters")
    if button_clicked_add_parameters:
        button_clicked_add_parameters = False
        response_add_parameters = requests.post(
            f"http://{host}:{port}/parameters/add-parameters", json=info_add_parameters)

    imgui.end()