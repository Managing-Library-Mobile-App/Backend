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

# LOCAL SETUP
Go to the project's root directory
To run the app locally, use:
pip install virtualenv
virtualenv venv
pip install -r docker_and_setup/requirements.txt
python app.py

# Database setup

# DOCKER SETUP
To run the app using docker, use:
docker-compose build
docker-compose up

# APP USAGE
Then you can access the api using an address: http://192.168:100.7:5000
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