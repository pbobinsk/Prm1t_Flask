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

filename = "studenci_103.csv"
data = csv_to_dict(filename)
filename = "studenci_104.csv"
data |= csv_to_dict(filename)
filename = "studenci_105.csv"
data |= csv_to_dict(filename)
data['1234'] = {"name": "Tester", "surname": "Testowy"}

