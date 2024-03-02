from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import authors_users, authors_released_books


class Author(db.Model):  # type: ignore[name-defined]
    __tablename__ = "author"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genres = db.Column(ARRAY(db.String), default=[])
    biography = db.Column(db.String(1000), default="No biography")
    picture = db.Column(db.String(1000), default=0)
    fans_count = db.Column(db.Integer, default=0)
    # TODO pobranie listy fanów? czy wgl potrzebne
    fans = db.relationship(
        "User",
        secondary=authors_users,
        lazy="subquery",
        back_populates="followed_authors",
        cascade="all, delete",
    )
    released_books_count = db.Column(db.Integer, default=0)
    # TODO pobranie listy książek
    released_books = db.relationship(
        "Book",
        secondary=authors_released_books,
        lazy="subquery",
        backref=db.backref("authors_released_books"),
        cascade="all, delete",
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
        for fan_id in fans:
            self.add_fan(fan_id)
        for released_book_id in released_books:
            self.add_released_book(released_book_id)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "biography": self.biography,
            "picture": self.picture,
            "fans_count": self.fans_count,
            "fans": [fan.id for fan in self.fans],  # type: ignore
            "released_books_count": self.released_books_count,
            "released_books": [
                released_book.id for released_book in self.released_books  # type: ignore
            ],
        }

    def add_fan(self, fan_id) -> None:
        from .user import User

        fan = db.session.query(User).filter_by(id=fan_id).first()
        if fan:
            self.fans.append(fan)
            self.fans_count += 1

    def remove_fan(self, fan_id) -> None:
        from .user import User

        fan = db.session.query(User).filter_by(id=fan_id).first()
        if fan:
            self.fans.remove(fan)
            self.fans_count -= 1

    def add_released_book(self, book_id) -> None:
        from .book import Book

        book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.append(book)
            self.released_books_count += 1

    def remove_released_book(self, book_id) -> None:
        from .book import Book

        book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.remove(book)
            self.released_books_count -= 1
