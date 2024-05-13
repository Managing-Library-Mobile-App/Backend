import os

import pandas as pd
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
            "authors", "processed_data_authors", "ol_dump_authors_dev.json"
        )
        df_books = pd.read_json(read_file_path_books, orient="records", lines=True)
        print(df_books.shape)
        print(df_books)
        print("Filling database")

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

        print("Database filled")
