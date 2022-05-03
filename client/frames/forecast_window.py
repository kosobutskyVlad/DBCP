import requests

import imgui

from frames.load_image import get_textureID
from frames.error_popup import error_popup
from forecasting.data_prep_utils import aggregate_history, ffill_history
from forecasting.predict import predict

input_store_id = ""
input_product_id = ""

response_get_purchases = None
purchases_dataframe = None
aggregation_window = None
loss_parameters = None

show_error_popup = False
error_popup_message = ""

prediction_results = None
update_image = False
textureID = None
image_size = None

def forecast_window(host: str, port: int):

    global input_store_id
    global input_product_id

    global response_get_purchases
    global purchases_dataframe
    global aggregation_window
    global response_get_parameters
    global loss_parameters

    global show_error_popup
    global error_popup_message

    global prediction_results
    global update_image
    global textureID
    global image_size

    imgui.begin("Forecast window")

    show_error_popup = error_popup(show_error_popup, error_popup_message)

    imgui.push_item_width(100)
    _, input_store_id = imgui.input_text("Get by store_id",
                input_store_id, 6)

    _, input_product_id = imgui.input_text("Get by product_id",
                input_product_id, 6)
    imgui.pop_item_width()

    if imgui.button("Predict sales"):
        try:
            if not input_store_id or not input_product_id:
                show_error_popup = True
                error_popup_message = "Specify both store_id and product_id."

            response_get_purchases = requests.get(
                f"http://{host}:{port}/purchases/get-purchases",
                params={"store_id": input_store_id,
                        "product_id": input_product_id})

            if response_get_purchases.status_code == 200:
                purchases_dataframe, aggregation_window = aggregate_history(ffill_history(response_get_purchases))
            else:
                show_error_popup = True
                error_popup_message = response_get_purchases.json()["detail"]

            response_get_parameters = requests.get(
                f"http://{host}:{port}/parameters/get-parameters/",
                params={"store_id": input_store_id,
                        "product_id": input_product_id})

            if response_get_parameters.status_code == 200:
                loss_parameters = response_get_parameters.json()["parameters"][0][3:]
            else:
                show_error_popup = True
                error_popup_message = response_get_parameters.json()["detail"]


            if (response_get_purchases.status_code == 200
                and response_get_parameters.status_code == 200):
                prediction_results = predict(
                    purchases_dataframe,
                    aggregation_window,
                    loss_parameters
                )
                update_image = True
            else:
                prediction_results = None

        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    if update_image:
        textureID, image_size = get_textureID(
            purchases_dataframe["sales"].values, prediction_results
        )
        update_image = False

    if prediction_results is not None:
        imgui.separator()
        imgui.text(f"Quality control for {input_store_id} and {input_product_id}")
        draw_list = imgui.get_window_draw_list()
        window_pos = imgui.get_window_position()
        draw_list.add_image(
            textureID, (window_pos[0]+5, window_pos[1]+120),
            (window_pos[0]+5+image_size[0], window_pos[1]+120+image_size[1]))

    imgui.end()