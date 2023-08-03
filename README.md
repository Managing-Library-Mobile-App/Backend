# Backend
Written in Flask

First download the application and go into its directory in a terminal usind for example `cd` command in the terminal.

To run the app locally, use:
pip install -r requirements.txt
python app.py

To run the app using docker, use:
docker build -t app .
docker run app

Then you can access the api using an address: http://192.168:100.7:5000
or locally using http://127.0.0.1:5000
or using curl command in the terminal:
curl http://192.168:100.7:5000




Zadania główne:
# TODO ZROBIĆ WERSJE API: /api/v0.1/..., /api/v1.0/...
# TODO skrypt .sh uruchamiający bazę danych i aplikację
# TODO testy
# TODO uwierzytelnianie (klucz przy każdym zapytaniu po zalogowaniu) auth0?
# TODO sesje (ale to w aplikacji a nie w API powinno być ale ważne, klucz powinien wygasać)
# TODO postgres database?
# TODO pgadmin?
# TODO logger
# TODO https
# TODO instrukcja jak zrobić venv lokalnie
# TODO w readme zawrzeć wymagania np. python 3.10
# TODO marshmallow do mapowania klas???
Zadania dodatkowe (można wykonać na koniec):
# TODO flake8
# TODO dockeryzacja aplikacji z bazką i z volume?
# TODO docker-compose
# TODO opisanie swaggera
# TODO opisanie api
# TODO opisanie bazy danych
# TODO opisanie aplikacji
# TODO opisanie dockera?
# TODO opisanie docker-compose?
# TODO opisanie testów
# TODO opisanie uwierzytelniania
# TODO kubernetes
# TODO postman
# TODO CI/CD (np. Github Actions)
# TODO hosting?
# TODO opisanie w dokumentacji jak uruchomić aplikację w każdy możliwy sposób
# TODO opisanie w dokumentacji jak uruchomić testy
# TODO