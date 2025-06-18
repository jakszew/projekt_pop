from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim

users:list = []
markers:list = []
last_selected_gallery_index = None



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
    # przekazujemy nazwę do funkcji
    find_and_mark_gallery(nazwa)


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f"{idx+1}. {user['name']}")
    clear_employee_list()


def remove_user():
    global markers
    i = listbox_lista_obiektow.curselection()
    if not i:
        return
    i = i[0]

    users.pop(i)
    if i < len(markers):
        markers[i].delete()
        markers.pop(i)
    show_users()

def edit_user():
    i=listbox_lista_obiektow.curselection()
    if not i:
        return
    i=i[0]
    name=users[i]["name"]
    entry_name.delete(0, END)
    entry_name.insert(0, name)
    button_doda_obiekt.config(text="zapisz", command=lambda: update_user(i))

def update_user(i):
    new_name = entry_name.get().strip()
    if not new_name:
        print("Podaj nazwe galerii sztuki")
        return

    users[i]['name'] = new_name
    entry_name.delete(0, END)
    entry_name.focus()
    button_doda_obiekt.config(text="Dodaj obiekt", command=add_user)
    show_users()



def find_and_mark_gallery(query):
    global markers  # dodaj tę linijkę na początku funkcji
    try:
        geolocator = Nominatim(user_agent="gallery_map_app")
        location = geolocator.geocode(query)

        if location:
            lat, lon = location.latitude, location.longitude
            marker = map_widget.set_marker(lat, lon, text=query)
            markers.append(marker)
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(14)
        else:
            print("Nie znaleziono lokalizacji dla:", query)

    except Exception as e:
        print("Błąd podczas geolokalizacji:", e)

#pracownicy
def show_employees():
    if last_selected_gallery_index is None:
        return
    listbox_employees.delete(0, END)
    for idx, emp in enumerate(users[last_selected_gallery_index]["employees"]):
        listbox_employees.insert(idx, emp)

def clear_employee_list():
    listbox_employees.delete(0, END)

def add_employee():
    global last_selected_gallery_index
    gallery_index = last_selected_gallery_index
    if gallery_index is None:
        print("Wybierz galerię, do której chcesz dodać pracownika.")
        return

    employee_name = entry_employee_name.get().strip()

    if not employee_name:
        print("Podaj nazwę pracownika.")
        return

    users[gallery_index]["employees"].append(employee_name)
    entry_employee_name.delete(0, END)
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
    current_name = users[gallery_index]["employees"][employee_index]
    entry_employee_name.delete(0, END)
    entry_employee_name.insert(0, current_name)
    button_add_employee.config(text="Zapisz", command=lambda: update_employee(gallery_index, employee_index))
    show_employees()
def update_employee(gallery_index, employee_index):
    new_name = entry_employee_name.get().strip()
    if new_name:
        users[gallery_index]["employees"][employee_index] = new_name
        entry_employee_name.delete(0, END)
        button_add_employee.config(text="Dodaj pracownika", command=add_employee)
        show_employees()

#klienci
def show_clients():
    listbox_clients.delete(0, END)
    if last_selected_gallery_index is None:
        return
    gallery_index = last_selected_gallery_index
    for idx, client in enumerate(users[gallery_index]["clients"]):
        listbox_clients.insert(idx, client)

def add_client():
    if last_selected_gallery_index is None:
        print("Wybierz galerię.")
        return
    gallery_index = last_selected_gallery_index
    client_name = entry_client_name.get().strip()
    if not client_name:
        print("Podaj nazwę klienta.")
        return
    users[gallery_index]["clients"].append(client_name)
    entry_client_name.delete(0, END)
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
    current_name = users[gallery_index]["clients"][client_index]
    entry_client_name.delete(0, END)
    entry_client_name.insert(0, current_name)
    button_add_client.config(text="Zapisz", command=lambda: update_client(gallery_index, client_index))

def update_client(gallery_index, client_index):
    new_name = entry_client_name.get().strip()
    if new_name:
        users[gallery_index]["clients"][client_index] = new_name
        entry_client_name.delete(0, END)
        show_clients()
        button_add_client.config(text="Dodaj klienta", command=add_client)

def on_gallery_select(event):
    global last_selected_gallery_index
    i = listbox_lista_obiektow.curselection()
    if i:
        last_selected_gallery_index = i[0]
        show_employees()
        show_clients()

def on_employee_select(event):
    pass

root = Tk()
root.geometry("1200x760")
root.title('Map Book BK2')


ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista galerii sztuki")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
listbox_lista_obiektow.bind('<<ListboxSelect>>', on_gallery_select)

button_usun_obiekt=Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz_galerii
Label(ramka_formularz, text="Formularz").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Nazwa galerii: ").grid(row=1, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)

button_doda_obiekt = Button(ramka_formularz, text='Dodaj obiekt', command=add_user)
button_doda_obiekt.grid(row=2, column=0, columnspan=2)

#pracownicy
Label(ramka_formularz, text="Pracownicy galerii").grid(row=3, column=0, columnspan=1)
Label(ramka_formularz, text="Klienci galerii").grid(row=3, column=1, columnspan=1)

listbox_employees = Listbox(ramka_formularz, width=40, height=8)
listbox_employees.grid(row=4, column=0)

listbox_clients = Listbox(ramka_formularz, width=40, height=8)
listbox_clients.grid(row=4, column=1)

entry_employee_name = Entry(ramka_formularz)
entry_employee_name.grid(row=5, column=0, sticky=W)

button_add_employee = Button(ramka_formularz, text="Dodaj pracownika", command=add_employee)
button_add_employee.grid(row=5, column=0, sticky=E)

Button(ramka_formularz, text="Usuń pracownika", command=remove_employee).grid(row=6, column=0, sticky=W)
Button(ramka_formularz, text="Edytuj pracownika", command=edit_employee).grid(row=6, column=0, sticky=E)

entry_client_name = Entry(ramka_formularz)
entry_client_name.grid(row=5, column=1, sticky=W)

button_add_client = Button(ramka_formularz, text="Dodaj klienta", command=add_client)
button_add_client.grid(row=5, column=1, sticky=E)

Button(ramka_formularz, text="Usuń klienta", command=remove_client).grid(row=6, column=1, sticky=W)
Button(ramka_formularz, text="Edytuj klienta", command=edit_client).grid(row=6, column=1, sticky=E)

#ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)



root.mainloop()
