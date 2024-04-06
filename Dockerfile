FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
ARG DB_TYPE
ENV DB_TYPE_ENV=$DB_TYPE
CMD python app.py $DB_TYPE_ENV
