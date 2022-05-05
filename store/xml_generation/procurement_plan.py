import requests
import xml.etree.ElementTree as ET
from datetime import datetime

show_error_popup = False
error_popup_message = ""

def generate_plan(server_host, server_port,
        forecast_host, forecast_port, store_id
    ):

    global show_error_popup
    global error_popup_message

    try:
        response_get_products = requests.get(
            f"http://{server_host}:{server_port}/products/get-by-storeid",
            params={"store_id": store_id}
        )

        if response_get_products.status_code == 200:
            products_list = response_get_products.json()["Data"]

    except requests.exceptions.ConnectionError:
        show_error_popup = True
        error_popup_message = "Server unavailable.\nPlease retry later."

    products = ET.Element(
        "products",
        {"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "store_id": store_id}
    )
    for product_id in products_list:
        try:
            response_get_prediction = requests.get(
                f"http://{forecast_host}:{forecast_port}/predict/",
                params={"store_id": store_id,
                "product_id": product_id,
                "host": server_host,
                "port": server_port}
            )

            if response_get_prediction.status_code == 200:
                product_prediction = response_get_prediction.json()
                product = ET.SubElement(products, "product", id=product_id)
                product.text = str(product_prediction[0])

        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

    indent(products)
    tree = ET.ElementTree(products)
    tree.write(f"procurement_plan.xml", encoding="utf-8")


def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i