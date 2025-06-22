from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim
import requests

users:list = []
markers:list = []
last_selected_gallery_index = None

# --- Funkcja pobierająca współrzędne z Wikipedii ---
def get_coordinates_from_wikipedia(place_name):
    search_url = "https://pl.wikipedia.org/w/api.php"
    params_search = {
        "action": "query",
        "list": "search",
        "srsearch": place_name,
        "format": "json"
    }
    try:
        response = requests.get(search_url, params=params_search)
        response.raise_for_status()
        data = response.json()
        if not data["query"]["search"]:
            return None  # nie znaleziono artykułu

        page_title = data["query"]["search"][0]["title"]

        params_coord = {
            "action": "query",
            "titles": page_title,
            "prop": "coordinates",
            "format": "json"
        }
        coord_response = requests.get(search_url, params=params_coord)
        coord_response.raise_for_status()
        coord_data = coord_response.json()

        pages = coord_data["query"]["pages"]
        for page_id in pages:
            page = pages[page_id]
            if "coordinates" in page:
                lat = page["coordinates"][0]["lat"]
                lon = page["coordinates"][0]["lon"]
                return lat, lon
        return None
    except Exception as e:
        print("Błąd pobierania z Wikipedii:", e)
        return None

# --- Funkcja dodająca galerię ---
def add_user():
    nazwa = entry_name.get().strip()

    if not nazwa:
        print("Podaj nazwę galerii.")
        return

    user = {"name": nazwa, "employees": [], "clients": []}
    users.append(user)

    entry_name.delete(0, END)
    entry_name.focus()
    show_users()
    # przekazujemy nazwę do funkcji, która znajdzie i oznaczy lokalizację
    find_and_mark_gallery(nazwa)

# --- Wyświetlanie listy galerii ---
def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f"{idx+1}. {user['name']}")
    last_selected_gallery_index = None
    clear_employee_list()
    clear_client_list()

# --- Usuwanie galerii ---
def remove_user():
    i = listbox_lista_obiektow.curselection()
    if not i:
        return
    i = i[0]

    user = users.pop(i)
    if "markers" in user:
        for m in user["markers"]:
            m.delete()

    show_users()
# --- Edycja galerii ---
def edit_user():
    i=listbox_lista_obiektow.curselection()
    if not i:
        return
    i=i[0]
    name=users[i]["name"]
    entry_name.delete(0, END)
    entry_name.insert(0, name)
    button_doda_obiekt.config(text="Zapisz", command=lambda: update_user(i))

def update_user(i):
    new_name = entry_name.get().strip()
    if not new_name:
        print("Podaj nazwę galerii sztuki")
        return

    users[i]['name'] = new_name
    entry_name.delete(0, END)
    entry_name.focus()
    button_doda_obiekt.config(text="Dodaj obiekt", command=add_user)
    show_users()

# --- Znajdź i oznacz galerię na mapie ---
def get_coordinates(query):
    coords = get_coordinates_from_wikipedia(query)
    if coords:
        return coords
    try:
        geolocator = Nominatim(user_agent="gallery_map_app")
        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print("Błąd podczas geolokalizacji:", e)
    return None

def find_and_mark_gallery(query):
    coords = get_coordinates(query)
    if coords:
        lat, lon = coords
        marker = map_widget.set_marker(lat, lon, text=query)
        return marker
    return None

# --- Pracownicy ---

def show_employees():
    if last_selected_gallery_index is None:
        return
    listbox_employees.delete(0, END)
    for idx, emp in enumerate(users[last_selected_gallery_index]["employees"]):
        listbox_employees.insert(idx, f"{emp['name']} ({emp['city']})")

def clear_employee_list():
    listbox_employees.delete(0, END)

def add_employee():
    global last_selected_gallery_index
    gallery_index = last_selected_gallery_index
    if gallery_index is None:
        print("Wybierz galerię, do której chcesz dodać pracownika.")
        return

    employee_name = entry_employee_name.get().strip()
    employee_city = entry_employee_city.get().strip()

    if not employee_name or not employee_city:
        print("Podaj nazwę i miasto pracownika.")
        return

    users[gallery_index]["employees"].append({"name": employee_name, "city": employee_city})
    entry_employee_name.delete(0, END)
    entry_employee_city.delete(0, END)
    show_employees()

def remove_employee():
    global last_selected_gallery_index
    gallery_index = last_selected_gallery_index
    selected_employee = listbox_employees.curselection()
    if gallery_index is None or not selected_employee:
        return
    employee_index = selected_employee[0]
    del users[gallery_index]["employees"][employee_index]
    show_employees()

def edit_employee():
    global last_selected_gallery_index
    gallery_index = last_selected_gallery_index
    selected_employee = listbox_employees.curselection()
    if gallery_index is None or not selected_employee:
        return
    employee_index = selected_employee[0]
    current_emp = users[gallery_index]["employees"][employee_index]
    entry_employee_name.delete(0, END)
    entry_employee_name.insert(0, current_emp["name"])
    entry_employee_city.delete(0, END)
    entry_employee_city.insert(0, current_emp["city"])
    button_add_employee.config(text="Zapisz", command=lambda: update_employee(gallery_index, employee_index))
    show_employees()

def update_employee(gallery_index, employee_index):
    new_name = entry_employee_name.get().strip()
    new_city = entry_employee_city.get().strip()
    if new_name and new_city:
        users[gallery_index]["employees"][employee_index] = {"name": new_name, "city": new_city}
        entry_employee_name.delete(0, END)
        entry_employee_city.delete(0, END)
        button_add_employee.config(text="Dodaj pracownika", command=add_employee)
        show_employees()

# --- Klienci ---

def show_clients():
    if last_selected_gallery_index is None:
        return
    listbox_clients.delete(0, END)
    gallery_index = last_selected_gallery_index
    for idx, client in enumerate(users[gallery_index]["clients"]):
        listbox_clients.insert(idx, f"{client['name']} ({client['city']})")

def clear_client_list():
    listbox_clients.delete(0, END)

def add_client():
    if last_selected_gallery_index is None:
        print("Wybierz galerię.")
        return
    gallery_index = last_selected_gallery_index
    client_name = entry_client_name.get().strip()
    client_city = entry_client_city.get().strip()
    if not client_name or not client_city:
        print("Podaj nazwę i miasto klienta.")
        return
    users[gallery_index]["clients"].append({"name": client_name, "city": client_city})
    entry_client_name.delete(0, END)
    entry_client_city.delete(0, END)
    show_clients()

def remove_client():
    if last_selected_gallery_index is None:
        return
    selected_client = listbox_clients.curselection()
    if not selected_client:
        return
    gallery_index = last_selected_gallery_index
    client_index = selected_client[0]
    del users[gallery_index]["clients"][client_index]
    show_clients()

def edit_client():
    if last_selected_gallery_index is None:
        return
    selected_client = listbox_clients.curselection()
    if not selected_client:
        return
    gallery_index = last_selected_gallery_index
    client_index = selected_client[0]
    current_client = users[gallery_index]["clients"][client_index]
    entry_client_name.delete(0, END)
    entry_client_name.insert(0, current_client["name"])
    entry_client_city.delete(0, END)
    entry_client_city.insert(0, current_client["city"])
    button_add_client.config(text="Zapisz", command=lambda: update_client(gallery_index, client_index))

def update_client(gallery_index, client_index):
    new_name = entry_client_name.get().strip()
    new_city = entry_client_city.get().strip()
    if new_name and new_city:
        users[gallery_index]["clients"][client_index] = {"name": new_name, "city": new_city}
        entry_client_name.delete(0, END)
        entry_client_city.delete(0, END)
        show_clients()
        button_add_client.config(text="Dodaj klienta", command=add_client)

# --- Obsługa wyboru galerii ---
def on_gallery_select(event):
    global last_selected_gallery_index
    i = listbox_lista_obiektow.curselection()
    if i:
        last_selected_gallery_index = i[0]
        show_employees()
        show_clients()

# --- Mapy i przełączanie ---
def clear_map_markers():
    # Usuń wszystkie markery z mapy
    for marker in markers:
        marker.delete()
    markers.clear()

    # Usuń markery przypisane do galerii
    for gallery in users:
        if "markers" in gallery:
            for marker in gallery["markers"]:
                marker.delete()
            gallery["markers"] = []

        if "employee_markers" in gallery:
            for marker in gallery["employee_markers"]:
                marker.delete()
            gallery["employee_markers"] = []

        if "client_markers" in gallery:
            for marker in gallery["client_markers"]:
                marker.delete()
            gallery["client_markers"] = []

def show_map_all_galleries():
    clear_map_markers()
    for user in users:
        marker = find_and_mark_gallery(user["name"])
        if marker:
            markers.append(marker)
    if markers:
        lat, lon = markers[0].position
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)

def show_map_employees_gallery():
    # Usuń wszystkie istniejące markery na mapie
    clear_map_markers()

    # Przechowuj nowe markery globalnie, by je potem móc usuwać
    global markers
    markers = []

    for gallery in users:
        # Usuń też stare markery pracowników w galerii
        if "employee_markers" in gallery:
            for m in gallery["employee_markers"]:
                m.delete()
        gallery["employee_markers"] = []

        for emp in gallery["employees"]:
            coords = get_coordinates(emp["city"])
            if not coords:
                coords = get_coordinates(f"{emp['name']} {emp['city']}")
            if coords:
                lat, lon = coords
                marker = map_widget.set_marker(lat, lon, text=f"Pracownik: {emp['name']}")
                gallery["employee_markers"].append(marker)
                markers.append(marker)
            else:
                print(f"Nie znaleziono lokalizacji dla pracownika: {emp['name']} ({emp['city']})")

    if markers:
        lat, lon = markers[0].position
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)

def show_map_clients_gallery():
    clear_map_markers()
    global markers
    markers = []

    for gallery in users:
        if "client_markers" in gallery:
            for m in gallery["client_markers"]:
                m.delete()
        gallery["client_markers"] = []

        for client in gallery["clients"]:
            coords = get_coordinates(client["city"])
            if not coords:
                coords = get_coordinates(f"{client['name']} {client['city']}")
            if coords:
                lat, lon = coords
                marker = map_widget.set_marker(lat, lon, text=f"Klient: {client['name']}")
                gallery["client_markers"].append(marker)
                markers.append(marker)
            else:
                print(f"Nie znaleziono lokalizacji dla klienta: {client['name']} ({client['city']})")

    if markers:
        lat, lon = markers[0].position
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(6)
# --- GUI ---

root = Tk()
root.geometry("1200x760")
root.title('Map Book BK2')

ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, sticky=N+S)
ramka_formularz.grid(row=0, column=1, sticky=N)
ramka_mapa.grid(row=1, column=0, columnspan=2)

# Lista galerii
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista galerii sztuki")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
listbox_lista_obiektow.bind('<<ListboxSelect>>', on_gallery_select)

button_usun_obiekt=Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# Formularz galerii
Label(ramka_formularz, text="Formularz galerii").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Nazwa galerii: ").grid(row=1, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)

button_doda_obiekt = Button(ramka_formularz, text='Dodaj obiekt', command=add_user)
button_doda_obiekt.grid(row=2, column=0, columnspan=2)

# Pracownicy i klienci
Label(ramka_formularz, text="Pracownicy galerii").grid(row=3, column=0, sticky=W)
Label(ramka_formularz, text="Miasto").grid(row=3, column=1, sticky=W)
Label(ramka_formularz, text="Klienci galerii").grid(row=3, column=2, sticky=W)
Label(ramka_formularz, text="Miasto").grid(row=3, column=3, sticky=W)

listbox_employees = Listbox(ramka_formularz, width=30, height=8)
listbox_employees.grid(row=4, column=0, sticky=W)

entry_employee_name = Entry(ramka_formularz, width=20)
entry_employee_name.grid(row=5, column=0, sticky=W)
entry_employee_city = Entry(ramka_formularz, width=20)
entry_employee_city.grid(row=5, column=1, sticky=W)

button_add_employee = Button(ramka_formularz, text='Dodaj pracownika', command=add_employee)
button_add_employee.grid(row=6, column=0)

button_edit_employee = Button(ramka_formularz, text='Edytuj pracownika', command=edit_employee)
button_edit_employee.grid(row=6, column=1)

button_remove_employee = Button(ramka_formularz, text='Usuń pracownika', command=remove_employee)
button_remove_employee.grid(row=7, column=0)

listbox_clients = Listbox(ramka_formularz, width=30, height=8)
listbox_clients.grid(row=4, column=2, sticky=W)

entry_client_name = Entry(ramka_formularz, width=20)
entry_client_name.grid(row=5, column=2, sticky=W)
entry_client_city = Entry(ramka_formularz, width=20)
entry_client_city.grid(row=5, column=3, sticky=W)

button_add_client = Button(ramka_formularz, text='Dodaj klienta', command=add_client)
button_add_client.grid(row=6, column=2)

button_edit_client = Button(ramka_formularz, text='Edytuj klienta', command=edit_client)
button_edit_client.grid(row=6, column=3)

button_remove_client = Button(ramka_formularz, text='Usuń klienta', command=remove_client)
button_remove_client.grid(row=7, column=2)

# Przełącznik map
frame_map_buttons = Frame(root)
frame_map_buttons.grid(row=2, column=0, columnspan=2, sticky=W)

button_show_all_galleries = Button(frame_map_buttons, text="Mapa wszystkich galerii", command=show_map_all_galleries)
button_show_all_galleries.grid(row=0, column=0)

button_show_employees_gallery = Button(frame_map_buttons, text="Mapa pracowników galerii", command=show_map_employees_gallery)
button_show_employees_gallery.grid(row=0, column=2)

button_show_clients_gallery = Button(frame_map_buttons, text="Mapa klientów galerii", command=show_map_clients_gallery)
button_show_clients_gallery.grid(row=0, column=3)

# Mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)


root.mainloop()
