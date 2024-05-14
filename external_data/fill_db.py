import argparse
import os

import sys

sys.path.insert(1, os.getcwd())

import pandas as pd

import dateutil.parser as parser
import flask_restful
import psycopg2
from flask_restful import Api
from helpers.api_add_resources import api_add_resources
from helpers.delete_tables import delete_tables
from helpers.init import app, cache, db, jwt, limiter
from models.author import Author  # noqa
from models.book import Book  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa
from test_data.fill_db_script import create_admin_accounts_in_db

api: flask_restful.Api = Api(app)
api_add_resources(api)

arg_parser = argparse.ArgumentParser(description="Description of your script")
arg_parser.add_argument(
    "type_of_db",
    type=str,
    help="Type of db. Currently used: 'prod' or 'dev'",
)
args = arg_parser.parse_args()

host: str = os.environ.get("host")
port: str = os.environ.get("port")
database: str = args.type_of_db
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
    with app.app_context():
        delete_tables(db)

        if database == "prod":
            read_file_path_books = os.path.join(
                "external_data",
                "authors",
                "processed_data_authors",
                "ol_dump_authors_prod.json",
            )
        else:
            read_file_path_books = os.path.join(
                "external_data",
                "authors",
                "processed_data_authors",
                "ol_dump_authors_dev.json",
            )
        df_books = pd.read_json(read_file_path_books, orient="records", lines=True)
        print("Filling database")
        print("Filling Authors")

        for index, author_object in df_books.iterrows():
            db.session.add(
                Author(
                    id=author_object["id"],
                    name=author_object["name"],
                    biography=author_object["biography"],
                    picture=author_object["picture"],
                    website=author_object["website"],
                    birth_date=author_object["birth_date"],
                    death_date=author_object["death_date"],
                )
            )
            db.session.commit()

        print("Authors filled")
        print("Filling Books")

        if database == "prod":
            read_file_path_books = os.path.join(
                "external_data",
                "books",
                "processed_data_editions",
                "ol_dump_editions_prod.json",
            )
        else:
            read_file_path_books = os.path.join(
                "external_data",
                "books",
                "processed_data_editions",
                "ol_dump_editions_dev.json",
            )
        df_books = pd.read_json(read_file_path_books, orient="records", lines=True)

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
                continue

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
            except psycopg2.errors.UniqueViolation as e:
                db.session.rollback()
                print(
                    f"DB SESSION ERROR, probably id or isbn not unique. Error code: {e}"
                )
            except Exception as e:
                db.session.rollback()
                print(f"Unhandled error, probably data duplicates. Error code: {e}")

        print("Books filled")
        print("Filling Admins")

        create_admin_accounts_in_db(db)

        print("Admins filled")
        print("Deleting authors without books")

        all_authors: list[Author] = Author.query.all()
        for author_object in all_authors:
            if len(author_object.released_books) == 0:
                db.session.delete(author_object)
                db.session.commit()

        print("Authors without books deleted")
        print("Database filled")
