from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import authors_released_books, authors_users


class Author(db.Model):  # type: ignore[name-defined]
    """The class representing table author in database."""

    __tablename__ = "author"
    id = db.Column("id", db.String, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    genres = db.Column(ARRAY(db.String), default=[])
    biography = db.Column(db.String(150000), default="No biography")
    picture = db.Column(db.String(200), default=0)
    fans_count = db.Column(db.Integer, default=0)
    fans = db.relationship(
        "User",
        secondary=authors_users,
        lazy="subquery",
        back_populates="followed_authors",
    )
    released_books_count = db.Column(db.Integer, default=0)
    released_books = db.relationship(
        "Book",
        secondary=authors_released_books,
        lazy="subquery",
        back_populates="authors",
        cascade="all, delete",
    )
    birth_date = db.Column(db.String(200))
    death_date = db.Column(db.String(200))
    website = db.Column(db.String(1000))

    def __init__(
        self,
        id: str,
        name: str,
        biography: str,
        picture: str,
        birth_date: str = None,
        death_date: str = None,
        website: str = None,
    ) -> None:
        """Initializing an object of the class.
        :param biography: description of the author
        :param picture: link to the picture
        """
        self.id = id
        self.name = name
        self.biography = biography
        self.picture = picture
        self.birth_date = birth_date
        self.death_date = death_date
        self.website = website

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
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
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "website": self.website,
        }

    def add_fan(self, fan_id) -> None:
        """Add a user to fans' list
        :param fan_id: user id
        """
        from .user import User

        fan: User = db.session.query(User).filter_by(id=fan_id).first()
        if fan:
            self.fans.append(fan)
            self.fans_count += 1
            fan.followed_authors_count += 1

    def remove_fan(self, fan_id) -> None:
        """remove a user from fans' list
        :param fan_id: user id
        """
        from .user import User

        fan: User = db.session.query(User).filter_by(id=fan_id).first()
        if fan:
            self.fans.remove(fan)
            self.fans_count -= 1
            fan.followed_authors_count -= 1

    def add_released_book(self, book_id) -> None:
        """Add a book to released_books' list"""
        from .book import Book

        book: Book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.append(book)
            self.released_books_count += 1

            genres = set()
            for book in self.released_books:
                for genre in book.genres:
                    genres.add(genre)
                self.genres = genres

    def remove_released_book(self, book_id) -> None:
        """Remove a book from released_books' list"""
        from .book import Book

        book: Book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.remove(book)
            self.released_books_count -= 1
            genres = set()
            for book in self.released_books:
                for genre in book.genres:
                    genres.add(genre)
                self.genres = genres
