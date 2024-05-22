# LOCAL REQUIREMENTS
Python 3.10
Pip

# CONTAINER REQUIREMENTS
Docker (and Docker Desktop on Windows)

# DOWNLOAD
To download the application, use
clone https://github.com/Managing-Library-Mobile-App/Backend.git

# REQUIRED SECRET FILES
To run the app, two files are required in the static folder: cert.pem and key.pem
They are not in the repository and need to be added manually as they cannot be exposed

# CREATING JSON FILES FOR FILLING DB WITH DATA
python ./external_data/author/txt_authors_to_json prod
python ./external_data/author/txt_authors_to_json dev
python ./external_data/books/txt_books_to_json prod
python ./external_data/books/txt_books_to_json dev

# FILLING DB WITH DATA
python ./external_data/fill_db.py dev
python ./external_data/fill_db.py prod


# LOCAL SETUP
Go to the project's root directory
To run the app locally, use:
pip install virtualenv
virtualenv venv
pip install -r docker_and_setup/requirements.txt
python app.py <type_of_db>

type_of_db= prod or api_tests or e2e_tests, and indicates databases for different purposes

When running locally, if the database is not seen from name db (error: sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not translate host name "db" to address: Nieznany host.
), you have to add the line below to your etc/hosts file:
127.0.0.1 db

Check if your server/database has the same attributes as in the .env file

### ON WINDOWS
# DOCKER SETUP FOR PRODUCTION
To run the app using docker, use:
$env:DB_TYPE="prod"; docker-compose up --build

# DOCKER SETUP FOR DEVELOPMENT
To run the app using docker, use:
$env:DB_TYPE="dev"; docker-compose up --build

# DOCKER SETUP FOR E2E TESTS
To run the app using docker, use:
$env:DB_TYPE="e2e_tests"; docker-compose up --build

# DOCKER SETUP FOR API TESTS
To run the app using docker, use:
$env:DB_TYPE="api_tests"; docker-compose up --build

## ON LINUX USE DB_TYPE=prod

# APP USAGE
You can access the api using an address: http://192.168:100.7:5000
or locally using http://127.0.0.1:5000
or using curl command in the terminal:
curl http://192.168:100.7:5000

# TESTS
To run tests, go to the root of the project and use:
python -m pytest

# FORMATTING COMMANDS

# CHECK FORMAT
flake8 --config=helpers/.flake8

# FORMAT ALL .py FILES
black .

# CHECK STATIC TYPING
mypy --config-file=helpers/mypy.ini .

# FORMAT FILE
black <file_name>

# TEST COVERAGE
pytest --cov-config .coveragerc --cov-report term:skip-covered --cov=.
pytest --cov-config .coveragerc --cov-report html --cov=.

# SORTING IMPORTS
isort . --profile=black