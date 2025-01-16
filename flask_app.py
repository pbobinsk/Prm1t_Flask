
from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

api_keys = {'101':'1234',
          '105':'4321'}



@app.route('/')
def index():
    return """<html><body>
              <h1>Witam na 11-tych ćwiczeniach z PRM1T!</h1>
              <h2>Zapytania do webowego API z Pythona, a więc obsługa zapytań HTTP</h2>
              <h3>Pomoc <a href="https://www.geeksforgeeks.org/get-post-requests-using-python/">np. tu na GeeksForGeeks</a></h3>
              <h3>Adres do API to <a href="https://pbobinski.pythonanywhere.com/">właśnie ta strona</a></h3>

              <p>Aby uzyskać dostęp do api proszę skorzystać z następujących metod:</p>
              <ul>
              <li>get - wymagany argument: grupa (101 lub 105) - zwraca klucz do API w postaci JSON<br>
              ścieżka /get_api_key?grupa=&lt;numer grupy&gt;
              <li>post - wymagane argumenty w JSON: grupa, api_key, name (imię i nazwisko sudenta), lib (nazwa wykorzystanej biblioteki do obslugi http) - zwraca tekst z wynikiem<br>
              ścieżka /post_data, dane w JSON
              </ul>
              <p>Zadanie: Napisz program, który:
              <ul>
              <li>pobierze klucz dla grupy (argument grupa) (metoda GET)
              <li>wyśle za pomocą metody POST dane w postaci JSON zawierające:
              <ul>
              <li>numer grupy (argument grupa)
              <li>klucz do API (argument api_key)
              <li>imię i nazwisko studenta (argument name)
              <li>nazwa biblioteki do obsługi http (argument lib)
              </ul>
              <li>Jeśli wszystko przebiegnie, metoda POST zwróci tekst z podziękowaniem i informacją o przyznanym punkcie
              </body></html>
              """

@app.route('/get_api_key', methods=['GET'])
def handle_get():
    if request.method == 'GET' and 'grupa' in request.args:
      grupa = request.args['grupa']
      if (grupa in api_keys):
        return jsonify({'api_key':api_keys[grupa]})
      else:
        return 'niepoprawny identykikator grupy'
    else:
      return 'złe zapytanie, metoda lub nazwa argumentu'

@app.route('/post_data', methods=['POST'])
def handle_post():
  if request.method == 'POST' and 'grupa' in request.json and 'api_key' in request.json:
    print(request.json)
    if (request.json['grupa'] in api_keys and request.json['api_key'] == api_keys[request.json['grupa']] and 'name' in request.json and 'lib' in request.json):
      with open('wyniki.txt','a') as file:
        request.json['date'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        file.write(json.dumps(request.json) + '\n')
      return f'Dziękuję {request.json.get("name")}! Otrzymasz 1 punkt za użycie biblioteki {request.json.get("lib")} jeśli takowa istnieje'
    else:
      return 'niepoprawny identykator grupy lub klucz do API albo brak parametrów name, lib'
  else:
    return 'złe zapytanie, metoda lub argumenty'

