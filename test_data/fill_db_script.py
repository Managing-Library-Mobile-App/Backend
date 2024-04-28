from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from test_data.authors import authors
from test_data.books import books
from test_data.libraries import libraries
from test_data.new_books import new_books
from test_data.opinions import opinions
from test_data.users import admins, users
from models.author import Author
from models.book import Book
from models.library import Library
from models.opinion import Opinion
from models.user import User


def fill_db(db: SQLAlchemy):
    logger.info("Filling database")

    for author in authors:
        new_author: Author = Author(
            name=author["name"],
            biography=author["biography"],
            picture=author["picture"],
        )
        db.session.add(new_author)
        db.session.commit()

    for book in books:
        db.session.add(
            Book(
                language=book["language"],
                isbn=book["isbn"],
                title=book["title"],
                authors=book["authors"],
                publishing_house=book["publishing_house"],
                description=book["description"],
                genres=book["genres"],
                picture=book["picture"],
                premiere_date=book["premiere_date"],
            )
        )
        db.session.commit()

    for book in new_books:
        db.session.add(
            Book(
                language=book["language"],
                isbn=book["isbn"],
                title=book["title"],
                authors=book["authors"],
                publishing_house=book["publishing_house"],
                description=book["description"],
                genres=book["genres"],
                picture=book["picture"],
                premiere_date=book["premiere_date"],
            )
        )
        db.session.commit()

    for index, user in enumerate(users):
        new_user: User = User(
            username=user["username"],
            password=user["password"],
            email=user["email"],
        )
        db.session.add(new_user)
        db.session.commit()

        new_user_library: Library = Library(
            read_books=libraries[index]["read_books"],
            favourite_books=libraries[index]["favourite_books"],
            bought_books=libraries[index]["bought_books"],
            user_id=new_user.id,
        )
        db.session.add(new_user_library)
        db.session.commit()

    for index, admin in enumerate(admins):
        new_admin: User = User(
            username=admin["username"],
            password=admin["password"],
            email=admin["email"],
            is_admin=admin["is_admin"],
        )
        db.session.add(new_admin)
        db.session.commit()

        new_admin_library: Library = Library(
            read_books=[],
            favourite_books=[],
            bought_books=[],
            user_id=new_admin.id,
        )
        db.session.add(new_admin_library)
        db.session.commit()

    for opinion in opinions:
        new_opinion: Opinion = Opinion(
            user_id=opinion["user_id"],
            book_id=opinion["book_id"],
            stars_count=opinion["stars_count"],
            comment=opinion["comment"],
        )
        db.session.add(new_opinion)
        db.session.commit()

    for index, author in enumerate(authors):
        author_object: Author = Author.query.get(index + 1)
        if author_object:
            for fan in author["fans"]:
                author_object.add_fan(fan)
        db.session.commit()

    logger.info("Database filled")
