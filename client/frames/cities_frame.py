import requests

import imgui

get_cities_response = False
show_cities_selectable = False
cities_selectable = {}
cities_info = {}
cities_refresh = {}
cities_changed = {}

button_clicked_update_cities = False

button_clicked_delete_cities = False

button_clicked_add_city = False
info_add_city = {
    "city_id": "",
    "city_name": "",
    "city_size": "",
    "country": ""
}

def cities_frame(host: str, port: int):
    global get_cities_response
    global cities_selectable
    global show_cities_selectable
    global cities_info
    global cities_refresh
    global cities_changed
    global button_clicked_update_cities
    global button_clicked_delete_cities
    global info_add_city

    imgui.begin("Cities")

    if imgui.button("Load cities list"):
        get_cities_response = requests.get(f"http://{host}:{port}/cities/get-cities")
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
                get_city_response = requests.get(f"http://{host}:{port}/cities/get-city/{city}")
                #imgui.begin_popup_modal()
                info = get_city_response.json()["Data"][0]
                cities_info[city] = {"city_name": info[1][:50], "city_size": info[2][:10], "country": info[3][:50]}
            
            imgui.begin_child("cities_editor", 1000, 200, border=True)

            imgui.text(city)
            imgui.same_line()
            imgui.push_item_width(300)
            changed, cities_info[city]["city_name"] = imgui.input_text(f"{city}: city_name", cities_info[city]["city_name"], 51)
            if changed:
                cities_changed[city] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(100)
            changed, cities_info[city]["city_size"] = imgui.input_text(f"{city}: city_size", cities_info[city]["city_size"], 11)
            if changed:
                cities_changed[city] = True
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(300)
            changed, cities_info[city]["country"] = imgui.input_text(f"{city}: country", cities_info[city]["country"], 51)
            if changed:
                cities_changed[city] = True
            imgui.pop_item_width()
            imgui.end_child()

    button_clicked_update_cities = imgui.button("Update cities")
    if button_clicked_update_cities:
        button_clicked_update_cities = False
        for city in cities_changed:
            if cities_changed[city]:
                update_response = requests.put(f"http://{host}:{port}/cities/update-city", json={"city_id": city, "city_name": cities_info[city]["city_name"], "city_size": cities_info[city]["city_size"], "country": cities_info[city]["country"]})

    button_clicked_delete_cities = imgui.button("Delete cities")
    if button_clicked_delete_cities:
        button_clicked_delete_cities = False
        for city in cities_selectable:
            if cities_selectable[city]:
                delete_response = requests.delete(f"http://{host}:{port}/cities/delete-city/{city}")

    imgui.push_item_width(50)
    _, info_add_city["city_id"] = imgui.input_text("Add city_id", info_add_city["city_id"], 5)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(300)
    _, info_add_city["city_name"] = imgui.input_text(f"Add city_name", info_add_city["city_name"], 51)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(100)
    _, info_add_city["city_size"] = imgui.input_text(f"Add city_size", info_add_city["city_size"], 11)
    imgui.pop_item_width()
    imgui.same_line()
    imgui.push_item_width(300)
    _, info_add_city["country"] = imgui.input_text(f"Add country", info_add_city["country"], 51)
    imgui.pop_item_width()
    imgui.same_line()

    button_clicked_add_city = imgui.button("Add a city")
    if button_clicked_add_city:
        button_clicked_add_city = False
        post_response = requests.post(f"http://{host}:{port}/cities/add-city", json=info_add_city)

    imgui.end()