FROM python:3.11-alpine
WORKDIR /app
COPY .. /app
COPY . /
RUN pip install -r requirements.txt
CMD ["python", "app.py"]