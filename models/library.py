from sqlalchemy.orm import backref

from helpers.init import db
from models.book import Book

library_books_favourite = db.Table(
    "favourite_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id"),
        primary_key=True,
    ),
)

library_books_bought = db.Table(
    "bought_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id"),
        primary_key=True,
    ),
)

library_books_read = db.Table(
    "read_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id"),
        primary_key=True,
    ),
)


class Library(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    read_books_count = db.Column(db.Integer, default=0)
    favourite_books_count = db.Column(db.Integer, default=0)
    bought_books_count = db.Column(db.Integer, default=0)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
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
        self.read_books_count = 0
        self.favourite_books_count = 0
        self.bought_books_count = 0
        self.user_id = user_id
        db.session.add(self)
        for read_book_id in read_books:
            book = Book.query.get(read_book_id)
            if book:
                self.add_read_book(book)
        for bought_book_id in bought_books:
            book = Book.query.get(bought_book_id)
            if book:
                self.add_bought_book(book)
        for favourite_book_id in favourite_books:
            book = Book.query.get(favourite_book_id)
            if book:
                self.add_favourite_book(book)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "read_books_count": self.read_books_count,
            "favourite_books_count": self.favourite_books_count,
            "bought_books_count": self.bought_books_count,
            "read_books": self.read_books,
            "favourite_books": self.favourite_books,
            "bought_books": self.bought_books,
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
