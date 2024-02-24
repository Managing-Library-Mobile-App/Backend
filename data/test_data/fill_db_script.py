from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from data.test_data.admins import admins
from data.test_data.authors import authors
from data.test_data.book_announcements import book_announcements
from data.test_data.books import books
from data.test_data.libraries import libraries
from data.test_data.opinions import opinions
from data.test_data.users import users

from models.admin import Admin
from models.author import Author
from models.book import Book
from models.book_announcement import BookAnnouncement
from models.library import Library
from models.opinion import Opinion
from models.user import User


def fill_db(db: SQLAlchemy):
    logger.info("Filling database")

    for author in authors:
        print(author)
        new_author = Author(
            name=author["name"],
            genres=author["genres"],
            biography=author["biography"],
            picture=author["picture"],
            fans=[],
            released_books=[],
        )
        db.session.add(new_author)
        db.session.commit()

    for book in books:
        new_book = Book(
            isbn=book["isbn"],
            title=book["title"],
            author=book["author"],
            publishing_house=book["publishing_house"],
            description=book["description"],
            genres=book["genres"],
            picture=book["picture"],
            premiere_date=book["premiere_date"],
        )
        db.session.add(new_book)
        db.session.commit()

    for book_announcement in book_announcements:
        new_book_announcement = BookAnnouncement(
            title=book_announcement["title"],
            author=book_announcement["author"],
            publishing_house=book_announcement["publishing_house"],
            description=book_announcement["description"],
            genres=book_announcement["genres"],
            picture=book_announcement["picture"],
            premiere_date=book_announcement["premiere_date"],
        )
        db.session.add(new_book_announcement)
        db.session.commit()

    for admin in admins:
        new_admin = Admin(
            username=admin["username"],
            password=admin["password"],
            email=admin["email"],
        )
        db.session.add(new_admin)
        db.session.commit()

    for index, user in enumerate(users):
        new_user_library = Library(
            read_books=libraries[index]["read_books"],
            favourite_books=libraries[index]["favourite_books"],
            bought_books=libraries[index]["bought_books"],
        )
        # append books to library read_books, favourite_books, bought_books
        db.session.add(new_user_library)
        db.session.commit()

        new_user = User(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            library_id=new_user_library.id,
        )
        db.session.add(new_user)
        db.session.commit()

    for opinion in opinions:
        new_opinion = Opinion(
            account_id=opinion["account_id"],
            book_id=opinion["book_id"],
            stars_count=opinion["stars_count"],
            comment=opinion["comment"],
        )
        db.session.add(new_opinion)
        db.session.commit()

    for index, author in enumerate(authors):
        author_object: Author = Author.query.get(index + 1)
        if author_object:
            for released_book in author["released_books"]:
                author_object.add_released_book(released_book)
            for fan in author["fans"]:
                author_object.add_fan(fan)
        db.session.commit()
