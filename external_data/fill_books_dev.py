import os

import pandas as pd
import dateutil.parser as parser
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

import flask_restful
from flask_restful import Api
from helpers.api_add_resources import api_add_resources
from helpers.init import app, cache, db, jwt, limiter
from models.author import Author  # noqa
from models.book import Book  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa

api: flask_restful.Api = Api(app)
api_add_resources(api)

host: str = os.environ.get("host")
port: str = os.environ.get("port")
database: str = "dev"
user: str = os.environ.get("user")
password: str = os.environ.get("password")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["BUNDLE_ERRORS"] = True

jwt.init_app(app)
cache.init_app(app)
db.init_app(app)
limiter.init_app(app)

if __name__ == "__main__":
    import psycopg2

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {database}")
        print(f"CREATED DATABASE {database}")
        cur.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {database} already exists")
    with app.app_context():
        con = db.engine.connect()
        trans = con.begin()
        inspector = Inspector.from_engine(db.engine)
        meta = MetaData()
        tables = []
        all_fkeys = []
        for table_name in inspector.get_table_names():
            if table_name == "author":
                continue
            fkeys = []
            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue
                fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))
            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)
        for fkey in all_fkeys:
            con.execute(DropConstraint(fkey))
        for table in tables:
            con.execute(DropTable(table))
        trans.commit()

        db.create_all()

        read_file_path_books = os.path.join(
            "books", "processed_data_editions", "ol_dump_editions_dev.json"
        )
        df_books = pd.read_json(read_file_path_books, orient="records", lines=True)
        print("Filling database")

        for index, book_object in df_books.iterrows():
            author_does_not_exist = False
            for author_id in book_object["authors"]:
                if len(Author.query.filter_by(id=author_id).all()) < 1:
                    author_does_not_exist = True
                    break
            if author_does_not_exist:
                continue
            try:
                premiere_date = parser.parse(book_object["premiere_date"])
            except parser.ParserError:
                print(f"Premiere date is not valid for index {index}")
                premiere_date = None
            db.session.add(
                Book(
                    id=book_object["id"],
                    language=book_object["language"],
                    isbn=book_object["isbn"],
                    title=book_object["title"],
                    authors=book_object["authors"],
                    publishing_house=book_object["publishing_house"],
                    description=book_object["description"],
                    genres=book_object["genres"],
                    picture=book_object["picture"],
                    premiere_date=premiere_date,
                    number_of_pages=book_object["number_of_pages"],
                )
            )
            try:
                db.session.commit()
            except psycopg2.errors.UniqueViolation:
                db.session.rollback()
                print(f"DB SESSION ERROR, probably data duplicates")

        print("Database filled")
