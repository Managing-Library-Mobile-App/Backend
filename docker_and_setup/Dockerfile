FROM python:3.11-alpine
WORKDIR /app
COPY .. /app
COPY . /
RUN pip install -r .\docker_and_setup\requirements.txt
CMD ["python", "app.py"]