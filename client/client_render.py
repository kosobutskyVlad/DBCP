import requests

import imgui

active = {
    "storetypes": False,
    "cities": False,
    "stores": False,
    "products": False,
    "purchases": False,
    "parameters": False,
}

HOST = None
PORT = None

get_cities_response = False
show_cities_selectable = False
cities_selectable = {}
cities_info = {}
cities_refresh = {}
cities_changed = {}
update_cities = False

def main_menu_frame(host, port):
    global HOST
    global PORT
    HOST = host
    PORT = port
    imgui.begin("Main menu")
    imgui.text("aasdas")
    

    if imgui.button("Show cities frame"):
        active["cities"] = True
    
    if imgui.button("Close cities frame"):
        active["cities"] = False

    imgui.end()

    if active["cities"]:
        cities_frame()


def cities_frame():
    global get_cities_response
    global cities_selectable
    global show_cities_selectable
    global cities_info
    global cities_refresh
    global cities_changed
    global update_cities

    imgui.begin("Cities")

    if imgui.button("Load cities list"):
        get_cities_response = requests.get(f"http://{HOST}:{PORT}/cities/get-cities")
        if get_cities_response.status_code == 200:
            cities_selectable = {city[0]: False for city in get_cities_response.json()["cities"]}
            cities_refresh = {city[0]: True for city in get_cities_response.json()["cities"]}
            cities_changed = {city[0]: False for city in get_cities_response.json()["cities"]}
            show_cities_selectable = False

    if imgui.button("Show cities list"):
        if get_cities_response.status_code == 200:
            show_cities_selectable = True
    
    if show_cities_selectable:
        imgui.columns(count=5, identifier=None, border=False)
        for city in get_cities_response.json()["cities"]:
            label = city[0]
            _, cities_selectable[city[0]] = imgui.selectable(
                label=label, selected=cities_selectable[city[0]]
            )
            imgui.next_column()
        imgui.columns(1)

    for city in cities_selectable:
        if cities_selectable[city]:
            if cities_refresh[city]:
                cities_refresh[city] = False
                get_city_response = requests.get(f"http://{HOST}:{PORT}/cities/get-city/{city}")
                info = get_city_response.json()["Data"][0]
                cities_info[city] = {"city_name": info[1], "city_size": info[2], "country": info[3]}
            
            imgui.begin_child("cities_editor", 1000, 200, border=True)

            imgui.text(city)
            imgui.same_line()
            imgui.push_item_width(300)
            changed, cities_info[city]["city_name"] = imgui.input_text(f"{city}: city_name", cities_info[city]["city_name"], 50)
            if changed:
                cities_changed[city] = True
            imgui.same_line()
            imgui.pop_item_width()
            imgui.push_item_width(100)
            changed, cities_info[city]["city_size"] = imgui.input_text(f"{city}: city_size", cities_info[city]["city_size"], 10)
            if changed:
                cities_changed[city] = True
            imgui.same_line()
            imgui.pop_item_width()
            imgui.push_item_width(300)
            changed, cities_info[city]["country"] = imgui.input_text(f"{city}: country", cities_info[city]["country"], 50)
            if changed:
                cities_changed[city] = True
            imgui.pop_item_width()
            imgui.end_child()

    update_cities = imgui.button("Update cities")
    if update_cities:
        update_cities = False
        for city in cities_changed:
            if cities_changed[city]:
                print({"city_id": city, "city_name": cities_info[city]["city_name"], "city_size": cities_info[city]["city_size"], "country": cities_info[city]["country"]})
                update_response = requests.put(f"http://{HOST}:{PORT}/cities/update-city", json={"city_id": city, "city_name": cities_info[city]["city_name"], "city_size": cities_info[city]["city_size"], "country": cities_info[city]["country"]})

    imgui.end()