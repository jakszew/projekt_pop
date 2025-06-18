from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim

users:list = []
markers:list = []



def add_user():
    zmienna_nazwa = entry_name.get().strip()

    if not zmienna_nazwa:
        print("Podaj nazwę galerii.")
        return

    user = {"name": zmienna_nazwa}
    users.append(user)

    entry_name.delete(0, END)
    entry_name.focus()
    show_users()

    # przekazujemy nazwę do funkcji
    find_and_mark_gallery(zmienna_nazwa)


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f"{idx+1}. {user['name']}")

def remove_user():
    global markers  # też dodaj tutaj
    i = listbox_lista_obiektow.index(ACTIVE)
    if i < 0 or i >= len(users):
        return

    users.pop(i)

    if i < len(markers):
        markers[i].delete()
        markers.pop(i)

    show_users()

def edit_user():
    i=listbox_lista_obiektow.index(ACTIVE)
    name=users[i]["name"]

    entry_name.insert(0, name)


    button_doda_obiekt.config(text="zapisz", command=lambda: update_user(i))

def update_user(i):
    new_name = entry_name.get()

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
            print(f"Znaleziono lokalizację: {lat}, {lon}")

            marker = map_widget.set_marker(lat, lon, text=query)
            markers.append(marker)

            map_widget.set_position(lat, lon)
            map_widget.set_zoom(14)
        else:
            print("Nie znaleziono lokalizacji dla:", query)

    except Exception as e:
        print("Błąd podczas geolokalizacji:", e)


root = Tk()
root.geometry("1200x760")
root.title('Map Book BK2')


ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista galerii sztuki")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name=Label(ramka_formularz, text="Nazwa galerii: ")
label_name.grid(row=1, column=0, sticky=W)


entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1)


button_doda_obiekt=Button(ramka_formularz, text='Dodaj obiekt', command=add_user)
button_doda_obiekt.grid(row=5, column=0, columnspan=2)


#ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)



root.mainloop()
