from sqlalchemy.orm import backref

from helpers.init import db
from models.book import Book
from models.many_to_many_tables import (
    library_books_bought,
    library_books_favourite,
    library_books_read,
)


class Library(db.Model):  # type: ignore[name-defined]
    """The class representing table library in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    read_books_count = db.Column(db.Integer, default=0)
    favourite_books_count = db.Column(db.Integer, default=0)
    bought_books_count = db.Column(db.Integer, default=0)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    read_books = db.relationship(
        "Book",
        secondary=library_books_read,
        lazy="subquery",
        backref=backref("library_books_read"),
    )
    favourite_books = db.relationship(
        "Book",
        secondary=library_books_favourite,
        lazy="subquery",
        backref=backref("library_books_favourite"),
    )
    bought_books = db.relationship(
        "Book",
        secondary=library_books_bought,
        lazy="subquery",
        backref=backref("library_books_bought"),
    )

    def __init__(
        self, read_books: list, bought_books: list, favourite_books: list, user_id: int
    ) -> None:
        """Initializing an object of the class."""
        self.read_books_count = 0
        self.favourite_books_count = 0
        self.bought_books_count = 0
        self.user_id = user_id
        db.session.add(self)
        for read_book_id in read_books:
            read_book: Book = Book.query.get(read_book_id)
            if read_book:
                self.add_read_book(read_book)
        for bought_book_id in bought_books:
            bought_book: Book = Book.query.get(bought_book_id)
            if bought_book:
                self.add_bought_book(bought_book)
        for favourite_book_id in favourite_books:
            favourite_book: Book = Book.query.get(favourite_book_id)
            if favourite_book:
                self.add_favourite_book(favourite_book)

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "read_books_count": self.read_books_count,
            "read_books": [read_book.id for read_book in self.read_books],  # type: ignore
            "favourite_books_count": self.favourite_books_count,
            "favourite_books": [
                favourite_book.id for favourite_book in self.favourite_books  # type: ignore
            ],
            "bought_books_count": self.bought_books_count,
            "bought_books": [
                bought_book.id for bought_book in self.bought_books  # type: ignore
            ],
        }

    def add_read_book(self, book) -> None:
        self.read_books.append(book)
        self.read_books_count += 1

    def remove_read_book(self, book) -> None:
        self.read_books.remove(book)
        self.read_books_count -= 1

    def add_bought_book(self, book) -> None:
        self.bought_books.append(book)
        self.bought_books_count += 1

    def remove_bought_book(self, book) -> None:
        self.bought_books.remove(book)
        self.bought_books_count -= 1

    def add_favourite_book(self, book) -> None:
        self.favourite_books.append(book)
        self.favourite_books_count += 1

    def remove_favourite_book(self, book) -> None:
        self.favourite_books.remove(book)
        self.favourite_books_count -= 1
