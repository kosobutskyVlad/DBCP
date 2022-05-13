import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

from xml_generation.xml_utils import indent

show_error_popup = False
error_popup_message = ""

categories = None
offers = None
file_count = 1

def init_file(store_id):
    global categories
    global offers
    yml_catalog = ET.Element(
        "yml_catalog",
        {"date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    )
    shop = ET.SubElement(yml_catalog, "shop")
    name = ET.SubElement(shop, "name")
    name.text = store_id
    company = ET.SubElement(shop, "company")
    company.text = "company_placeholder"
    currencies = ET.SubElement(shop, "currencies")
    currency = ET.SubElement(currencies, "currency", id="RUB", rate="1")
    categories = ET.SubElement(shop, "categories")
    offers = ET.SubElement(shop, "offers")

    return yml_catalog

def add_categories(offer, product):
    global categories

    add_cat = True
    for cat in categories:
        if cat.attrib["id"] == product[2][1:9]:
            add_cat = False

    if add_cat:
        category = ET.SubElement(
            categories,
            "category",
            id=product[2][1:9]
        )
        category.text = f"ph_{product[2][1:9]}"

    categoryId = ET.SubElement(offer, "categoryId")
    categoryId.text = product[2][1:9]


def add_offer(offers, stock, product):
    
    offer = ET.SubElement(
        offers,
        "offer",
        id=stock[1]+"_"+stock[2]
    )

    price_elem = ET.SubElement(offer, "price")
    price_elem.text = str(round(product[3], 2))
    count = ET.SubElement(offer, "count")
    count.text = str(stock[3])
    currencyId = ET.SubElement(offer, "currencyId")
    currencyId.text = "USD"
    picture = ET.SubElement(offer, "picture")
    picture.text = "https://thumbs.dreamstime.com/z/shop-building-colorful-isolated-white-33822015.jpg"
    delivery = ET.SubElement(offer, "delivery")
    delivery.text = "false"
    name = ET.SubElement(offer, "name")
    name.text = product[1]
    description = ET.SubElement(offer, "description")
    description.text = "description placeholer"

    add_categories(offer, product)

def generate_yml(path, server_host, server_port, store_id):

    global categories
    global file_count

    global show_error_popup
    global error_popup_message

    abs_path = path if os.path.isabs(path) else os.path.join(os.getcwd(), path)
    yml_catalog = init_file(store_id)

    try:
        response_get_stock = requests.get(
            f"http://{server_host}:{server_port}/stock/get-stock",
            params={"store_id": store_id}
        )

        if response_get_stock.status_code == 200:
            stock_list = response_get_stock.json()["stock"]
        else:
            show_error_popup = True
            error_popup_message = response_get_stock.json()["detail"]
            return

    except requests.exceptions.ConnectionError:
        show_error_popup = True
        error_popup_message = "Server unavailable.\nPlease retry later."

    for i, stock in enumerate(stock_list, 1):
        try:
            response_get_product = requests.get(
                f"http://{server_host}:{server_port}/products/get-product/{stock[2]}"
            )

            if response_get_product.status_code == 200:
                product = response_get_product.json()["Data"][0]

        except requests.exceptions.ConnectionError:
            show_error_popup = True
            error_popup_message = "Server unavailable.\nPlease retry later."

        add_offer(offers, stock, product)

        if i % 8000 == 0:
            indent(yml_catalog)
            tree = ET.ElementTree(yml_catalog)
            tree.write(os.path.join(abs_path, f"catalogue_{file_count}.xml"), encoding="utf-8")
            file_count += 1
            yml_catalog = init_file(store_id)

    indent(yml_catalog)
    tree = ET.ElementTree(yml_catalog)
    tree.write(os.path.join(abs_path, f"catalogue_{file_count}.xml"), encoding="utf-8")
    file_count += 1