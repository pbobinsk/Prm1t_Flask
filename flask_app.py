
from flask import Flask, request, jsonify
import json
from datetime import datetime

import hashlib

SECRET_SALT = "my_super_secret_salt"

def generate_api_key(user_id):
    user_id_str = str(user_id)  # Zamiana user_id na string
    salted_input = user_id_str + SECRET_SALT
    return hashlib.sha256(salted_input.encode()).hexdigest()

app = Flask(__name__)

user_ids = [101, 102, 103, 104]

api_keys = {str(user_id): generate_api_key(user_id) for user_id in user_ids}

print(api_keys)

@app.route('/')
def index():
    return """<html><body>
              <h1>Witam na Laboratorium 14-tym z PRM1T!</h1>
              <h2>Zapytania do webowych API z Pythona, a więc obsługa zapytań HTTP</h2>
              <br>
              <h2>Zadania w skrócie</h2>
              <ul>
              <li>Z sewisu <a href="https://mapy.radiopolska.pl/">RadioPolska</a> 
              a właściwie jego API (<a href="https://mapy.radiopolska.pl/api">RadioPolska API</a>) 
              pobierz adres strony internetowej programu o identyfikatorze: <br>
              ostatnia cyfra Twojego numeru albumu + 1
              </li>
              <li>
              Prześlij ten adres (url) do mojego API 
              <a href="https://pbobinski.pythonanywhere.com/">Moje API na potrzeby tego laboratorium</a>
              </li>
              </ul>
              <h3>Moje API to <a href="https://pbobinski.pythonanywhere.com/">właśnie ta strona</a></h3>
              <p>Aby uzyskać dostęp do api proszę skorzystać z następujących metod:</p>
              <ul>
              <li><b>get</b> - wymagany argument: user (numer albumu) - zwraca klucz do API w postaci JSON<br>
              ścieżka <code>/get_api_key?user=&lt;numer albumu&gt;</code>
              <li><b>post</b> - wymagane argumenty w JSON: name (imię i nazwisko sudenta), url programu radiowego - zwraca tekst z wynikiem<br>
              ścieżka <code>/post_data</code>, dane w JSON<br>
              w nagłówku zapytania HTTP umieść otrzymany klucz API jako: <code>Authorization</code>
             <li>Jeśli wszystko przebiegnie dobrze, metoda POST zwróci kod 200 i tekst z podziękowaniem.
              </ul>
              </body></html>
              """

@app.route('/get_api_key', methods=['GET'])
def handle_get():
    if request.method == 'GET' and 'user' in request.args:
      user = request.args['user']
      if (user in api_keys):
        return jsonify({'api_key':api_keys[user]})
      else:
        return 'niepoprawny identykikator użytkownika', 400
    else:
      return 'złe zapytanie, metoda lub nazwa argumentu', 400

@app.route('/post_data', methods=['POST'])
def handle_post():
  if request.method == 'POST':
    print(request.json)
    if ('Authorization' not in request.headers):
      return 'brak lub niepoprawny klucz do API', 401
    if (request.headers['Authorization'] not in api_keys.values() ):
      return 'niepoprawny klucz do API', 403
    if ('name' in request.json and 'url' in request.json):
      with open('wyniki.txt','a') as file:
        request.json['date'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        file.write(json.dumps(request.json) + '\n')
      return f'Dziękuję {request.json.get("name")}! Przesłałeś następujący adres URL: {request.json.get("url")}'
    else:
      return 'brak parametrów name, url', 400
  else:
    return 'złe zapytanie, metoda lub argumenty', 400

