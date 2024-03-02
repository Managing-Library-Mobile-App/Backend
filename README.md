# Backend
Written in Flask

# API Methods

GET - pobieranie danych z api

POST - wrzucanie danych do api

PUT - modyfikacja jakiejś danej np. pola z modelu

PATCH - np. podmiana całego obiektu na nowy

DELETE - usuwanie elementu z api

------------------------------------------------------------

# Available endpoints

------------------------------------------------------------

## address (local): 127.0.0.1:5000
## address (remote): #TODO

------------------------------------------------------------

Aby korzystać z aplikacji, potrzebne jest konto. Należy je utworzyć.

### {{address}}/api/account/register

#### Authorization: None

#### Method: POST

    Body: raw json
    {
        username: str required
        password: str required
        email: str required
    }
    
    Correct Body example (if account does not exist):
    {
        "username": "Admin-1234"
        "password": "Admin-1234"
        "email": "admin@admin.pl"
    }

------------------------------------------------------------

Po rejestracji trzeba przekierować użytkownika do strony logowania

### {{address}}/api/account/login

#### Authorization: None

#### Method: POST

    Body: raw json
    {
        username: str required
        password: str required
    }
    
    Correct Body example (if account exists):
    {
        "username": "Admin-1234"
        "password": "Admin-1234"
    }

------------------------------------------------------------

Po procedurze logowania należy użyć check_login, by sprawdzić czy osoba ta
nie jest już zalogowana.


### {{address}}/api/account/check_login

#### Authorization: None

#### Method: POST

    Body: raw json
    {
        username: str required
        password: str required
    }
    
    Correct Body example (if account exists):
    {
        "username": "Admin-1234"
        "password": "Admin-1234"
    }

------------------------------------------------------------

Testowy endpoint dostępny dopiero po zalogowaniu

### {{address}}/api/account/protected

#### Authorization: None

#### Method: POST

    Body: None

------------------------------------------------------------
