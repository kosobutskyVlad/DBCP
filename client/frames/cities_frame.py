from regex import S
import requests

import imgui

response_get_cities = None
cities_list = []
show_selectable_cities = False
selectable_cities = {}
cities_info = {}
cities_refresh = {}
cities_changed = {}

show_popup_get_cities_error = False
show_popup_delete_error = False

info_add_city = {
    "city_id": "",
    "city_name": "",
    "city_size": "",
    "country": ""
}

def cities_frame(host: str, port: int):
    global response_get_cities
    global cities_list
    global show_selectable_cities
    global selectable_cities
    global cities_info
    global cities_refresh
    global cities_changed
    global info_add_city

    global show_popup_get_cities_error
    global show_popup_delete_error

    imgui.begin("Cities")

    if imgui.button("Load cities list"):
        response_get_cities = requests.get(
            f"http://{host}:{port}/cities/get-cities")
        
        if response_get_cities.status_code == 200:
            cities_list = response_get_cities.json()["cities"]

            selectable_cities = {city[0]: False for city in cities_list}
            cities_refresh = {city[0]: True for city in cities_list}
            cities_changed = {city[0]: False for city in cities_list}
            show_selectable_cities = False

    if imgui.button("Show cities list"):
        if response_get_cities:
            if response_get_cities.status_code == 200:
                show_selectable_cities = True
        else:
            show_popup_get_cities_error = True
    
    if show_popup_get_cities_error:
        imgui.open_popup("Error")
    if imgui.begin_popup_modal("Error")[0]:
        imgui.text("Load the cities list.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_get_cities_error = False
        imgui.end_popup()

    if show_selectable_cities:
        imgui.columns(count=15, identifier=None, border=False)
        for city in cities_list:
            label = city[0]
            _, selectable_cities[city[0]] = imgui.selectable(
                label=label, selected=selectable_cities[city[0]])
            imgui.next_column()
        imgui.columns(1)

    for city in selectable_cities:
        if selectable_cities[city]:
            if cities_refresh[city]:
                cities_refresh[city] = False
                get_city_response = requests.get(
                    f"http://{host}:{port}/cities/get-city/{city}")
                #imgui.begin_popup_modal()
                info = get_city_response.json()["Data"][0]
                cities_info[city] = {"city_name": info[1][:50], "city_size": info[2][:10], "country": info[3][:50]}
            
            imgui.begin_child("cities_editor", 1200, 200, border=True)
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
                response_update_city = requests.put(f"http://{host}:{port}/cities/update-city", json={"city_id": city, "city_name": cities_info[city]["city_name"], "city_size": cities_info[city]["city_size"], "country": cities_info[city]["country"]})

    button_clicked_delete_cities = imgui.button("Delete cities")
    if button_clicked_delete_cities:
        button_clicked_delete_cities = False
        for city in selectable_cities:
            if selectable_cities[city]:
                response_delete_city = requests.delete(f"http://{host}:{port}/cities/delete-city/{city}")
                if response_delete_city.status_code == 409:
                    show_popup_delete_error = True
    
    if show_popup_delete_error:
        imgui.open_popup("Integrity Error")
    if imgui.begin_popup_modal("Integrity Error")[0]:
        imgui.text(f"Record {city} could not be deleted because it is being referenced by a foreign key.")

        if imgui.button(label="Close"):
            imgui.close_current_popup()
            show_popup_delete_error = False
        imgui.end_popup()

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
        response_add_city = requests.post(f"http://{host}:{port}/cities/add-city", json=info_add_city)

    imgui.end()