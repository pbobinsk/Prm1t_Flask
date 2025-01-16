import csv

# Wczytanie CSV jako słownika
def csv_to_dict(filename):
    result = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            key = str(row["indeks"])
            result[key] = {"name": row["imie"], "surname": row["nazwisko"]}
    return result

filename = "studenci.csv"
data = csv_to_dict(filename)

