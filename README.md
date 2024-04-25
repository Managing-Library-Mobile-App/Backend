# Backend
Written in Flask

Docstring format (class):
        """

        [Summary]
        
        :param [ParamName]: [ParamDescription]
        """
Docstring format (function):
    """

    [Summary]

    :param [ParamName]: [ParamDescription]
    :raises [ErrorType]: [ErrorDescription]
    :return: [ReturnDescription]
    """

Docstring format (API Endpoints):
    """

    This examples uses FlaskRESTful Resource
    It works also with swag_from, schemas and spec_dict
    ---
    parameters:
    - in: body
      name: passwords
      description: The passwords.
      schema:
        type: object
        required:
          - current_password
          - new_password
        properties:
          current_password:
            type: string
          new_password:
            type: string
    consumes:
    - "application/json"
    produces:
    - "application/json"
    security:
    - APIKeyHeader: ['x-access-token']
    responses:
      200:
        description: A single user item
        schema:
          id: User
          properties:
            username:
              type: string
              description: The name of the user
              default: Steven Wilson
    """

# API Methods

GET - pobieranie danych z api

POST - wrzucanie danych do api

PUT - modyfikacja jakiejś danej np. pola z modelu

PATCH - np. podmiana całego obiektu na nowy

DELETE - usuwanie elementu z api

------------------------------------------------------------

# Available endpoints

------------------------------------------------------------

## address (local): 127.0.0.1:5000 (mobile app uses 10.0.2.2 instead)
## address (remote): differs

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
