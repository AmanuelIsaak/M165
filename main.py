import pymongo
from prettytable import PrettyTable

# ich wusste nicht genau wie ich die Datenbank exportieren, also habe ich auf der Datei "spiele.pcgame.json" gespeichert
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["spiele"]
collection = db["pcgames"]


# function für daten einfügen
def daten_einfuegen():
    name = input("Name des Spiels eingeben: ")
    jahr = int(input("Wann war das Erscheinungsjahr? "))
    download = int(input("Wie viele Downloads hat " + name + "? "))
    alter = int(input("Was ist die Altersgrenze? "))

    art_list = []

    # für die genre habe ich diese geschrieben, weil man die möglichkeit hat mehrer genres einzugeben. die werden
    # dann schlussendlich mit Kommas getrennt und mit 'x' beendet

    while True:
        art_entry = input("Zu welcher Genre gehört " + name + "? ('x' drücken wenn fertig): ")
        if art_entry.lower() == 'x':
            break
        art_list.append(art_entry)

    bewertung = float(input("Was ist die Bewertung? "))

    data = {
        "name": name,
        "jahr": jahr,
        "download": download,
        "alter": alter,
        "art": art_list,
        "bewertung": bewertung,
    }

    collection.insert_one(data)
    print("Ihre Daten wurden erfolgreich zur Datenbank hinzugefügt!")


# function für die löschung der dokumente
def daten_loeschen():
    print("Diese Aktion wie kann nicht RÜCKGÄNGIG gemacht werden!!!")
    name = input("Name des Spiels: ")
    query = {"name": name}
    result = collection.delete_many(query)
    print(f"{result.deleted_count} Dokument(e) wurden gelöscht!")


# function für namen der daten suchen

def name_suche():
    suche = input("Name suchen: ")
    query = collection.find({"name": {"$regex": suche, "$options": "i"}})

    resultat = list(query)

    count = len(resultat)  # Get the count from the list

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Erscheinungsjahr", "Downloadanzahl", "Genre", "Altergrenze", "Bewertung"]

        for idx, item in enumerate(resultat, start=1):
            name = item.get('name', 'N/A')
            art = item.get('art', 'N/A')
            alter = item.get('alter', 'N/A')
            jahr = item.get('jahr', 'N/A')
            download = item.get('download', 'N/A')
            bewertung = item.get('bewertung', 'N/A')
            table.add_row([idx, name, jahr, download, art, alter, bewertung])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


# function für download fliter
def download_suche():
    niedergste_suche = int(input("Wie viele downloads: "))
    hoechste_suche = int(input("Wie viele downloads: "))

    query = {"download": {"$gte": niedergste_suche, "$lte": hoechste_suche}}
    resultat = collection.find(query)

    count = collection.count_documents(query)

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Downloadanzahl"]

        for idx, item in enumerate(resultat, start=1):
            name = item.get('name', 'N/A')
            download = item.get('download', 'N/A')
            table.add_row([idx, name, download])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


# function für das erscheinungsjahr fliter
def jahr_suche():
    niedrigste_jahr = int(input("Niedrigste Erscheinungsjahr: "))
    hoechste_jahr = int(input("Höchste Erscheinungsjahr: "))

    query = {"jahr": {"$gte": niedrigste_jahr, "$lte": hoechste_jahr}}

    resultat = collection.find(query)
    count = collection.count_documents(query)

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Erscheinungsjahr"]

        for idx, item in enumerate(resultat, start=1):
            name = item.get('name', 'N/A')
            jahr = item.get('jahr', 'N/A')
            table.add_row([idx, name, jahr])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


# function für die alter filter
def alter_suche():
    niedrigste_alter = int(input("Niedrigste Altergrenze: "))
    hoechste_alter = int(input("Höchste Altergrenze: "))

    query = {"alter": {"$gte": niedrigste_alter, "$lte": hoechste_alter}}

    resultat = collection.find(query)
    count = collection.count_documents(query)

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Altergrenze"]

        for idx, item in enumerate(resultat, start=1):
            name = item.get('name', 'N/A')
            alter = item.get('alter', 'N/A')
            table.add_row([idx, name, alter])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


# function für die suche einer genre
def art_suche():
    art = input("Genres des Spiels (,): ")
    genres = [genre.strip() for genre in art.split(",")]

    query = {"art": {"$in": genres}}

    count = collection.count_documents(query)

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Genre"]

        for idx, item in enumerate(collection.find(query), start=1):
            name = item.get('name', 'N/A')
            art = item.get('art', 'N/A')
            table.add_row([idx, name, art])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


# function für bewertung filter
def bewertung_suche():
    niedrigste_bewertung = float(input("Niedrigste Bewertung: "))
    hoechste_bewertung = float(input("Höchste Bewertung: "))

    query = {"bewertung": {"$gte": niedrigste_bewertung, "$lte": hoechste_bewertung}}

    resultat = collection.find(query)
    count = collection.count_documents(query)

    if count > 0:
        print(f"{count} Ergebnis(se) gefunden!")
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Bewertung"]

        for idx, item in enumerate(resultat, start=1):
            name = item.get('name', 'N/A')
            bewertung = item.get('bewertung', 'N/A')
            table.add_row([idx, name, bewertung])

        print(table)
    else:
        print("Keine Ergebnisse gefunden.")


def daten_suchen():
    while True:
        print(" Möglichkeiten für Suche: ")
        print("1. Name")
        print("2. Ausgabejahr")
        print("3. Downloadszahlen")
        print("4. Alterbegrenzung")
        print("5. Art")
        print("6. Bewertung")
        print("7. Zurück")
        option = input("Was möchtest du suchen (1-7)? ")

        if option == "1":
            name_suche()
        elif option == "2":
            jahr_suche()
        elif option == "3":
            download_suche()
        elif option == "4":
            alter_suche()
        elif option == "5":
            art_suche()
        elif option == "6":
            bewertung_suche()
        elif option == "7":
            break
        else:
            print("Ungültige Auswahl!")


# function für aktualisieren
def daten_aktualisieren():
    name = input("Geben Sie Name des Spiels zum Aktualisieren: ")
    update_data = {}

    def eingabe(abfrage, feld, datatype=str):
        neue_wert = input(abfrage)
        if neue_wert:
            update_data[feld] = datatype(neue_wert)

    eingabe("Geben Sie das Erscheinungsjahr (leer lassen damit keine Änderung vorgenommen werden): ", "jahr", int)
    eingabe("Geben Sie das Downloadszahl (leer lassen damit keine Änderung vorgenommen werden): ", "download", int)
    eingabe("Geben Sie das Altergrenze (leer lassen damit keine Änderung vorgenommen werden): ", "alter", int)

    art = input("Geben Sie die Art des Spiels (leer lassen damit keine Änderung vorgenommen werden): ")
    if art:
        update_data["art"] = art.split(",")

    eingabe("Geben Sie die erwünschte Bewertung (leer lassen damit keine Änderung vorgenommen werden): ", "bewertung",
            float)  # float, damit man werte in deziemal eingeben kann
    resultat = collection.update_one({"name": name}, {"$set": update_data})

    if resultat.modified_count > 0:
        print(f"Document with the name '{name}' has been updated.")
    else:
        print(f"Dokument mit der Name '{name}' wurde nicht aktualisiert.")


def main_menu():
    while True:
        print("Hauptmenü:")
        print("1. Daten suchen ")
        print("2. Daten eintragen")
        print("3. Daten löschen")
        print("4. Daten aktualisieren")
        print("5. Abbrechen")

        choice = input("Wählen Sie aus den Optionen (1-5): ")

        if choice == "1":
            daten_suchen()
        elif choice == "2":
            daten_einfuegen()
        elif choice == "3":
            daten_loeschen()
        elif choice == "4":
            daten_aktualisieren()
        elif choice == "5":
            break
        else:
            print("Ungültige Auswahl!")


if __name__ == "__main__":
    main_menu()
