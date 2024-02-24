from sqlalchemy import ARRAY

from helpers.init import db
from models.book import Book
from models.user import User

authors_users = db.Table(
    "fans",
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

authors_released_books = db.Table(
    "released_books",
    db.Column(
        "author_id",
        db.Integer,
        db.ForeignKey("author.id"),
        primary_key=True,
    ),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


class Author(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genres = db.Column(ARRAY(db.String), nullable=False)
    biography = db.Column(db.String(1000), nullable=False)
    picture = db.Column(db.String(1000), default=0)
    fans_count = db.Column(db.Integer, default=0)
    fans = db.relationship(
        "User",
        secondary=authors_users,
        lazy="subquery",
        backref=db.backref("authors_users", lazy=True),
    )
    released_books_count = db.Column(db.Integer, default=0)
    released_books = db.relationship(
        "Book",
        secondary=authors_released_books,
        lazy="subquery",
        backref=db.backref("authors_released_books", lazy=True),
    )

    def __init__(
        self,
        name: str,
        genres: list[str],
        biography: str,
        picture: str,
        fans: list[int],
        released_books: list[int],
    ) -> None:
        self.name = name
        self.genres = genres
        self.biography = biography
        self.picture = picture
        print(fans, released_books)
        for fan_id in fans:
            self.add_fan(fan_id)
        for released_book_id in released_books:
            self.add_released_book(released_book_id)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "genres": self.genres,
            "biography": self.biography,
            "fans_count": self.fans_count,
            "fans": self.fans,
            "released_books_count": self.released_books_count,
            "released_books": self.released_books,
        }

    def add_fan(self, fan_id) -> None:
        fan = User.query.get(fan_id)
        if fan:
            self.fans.append(fan)
            self.fans_count += 1

    def remove_fan(self, fan_id) -> None:
        fan = User.query.get(fan_id)
        if fan:
            self.fans.remove(fan)
            self.fans_count -= 1

    def add_released_book(self, book_id) -> None:
        book = Book.query.get(book_id)
        if book:
            self.released_books.append(book)
            self.released_books_count += 1

    def remove_released_book(self, book_id) -> None:
        book = Book.query.get(book_id)
        if book:
            self.released_books.remove(book)
            self.released_books_count -= 1
