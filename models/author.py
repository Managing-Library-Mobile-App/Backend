from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import authors_released_books, authors_users


class Author(db.Model):  # type: ignore[name-defined]
    """The class representing table author in database."""

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
        """Initializing an object of the class.
        :param biography: description of the author
        :param picture: link to the picture
        :param fans: list of users who like the author
        :param released_books: list of author's books
        """
        self.name = name
        self.genres = genres
        self.biography = biography
        self.picture = picture
        from .user import User
        for fan_id in fans:
            self.fans.append(db.session.query(User).filter_by(id=fan_id).first())

        from .book import Book
        for book_id in released_books:
            self.released_books.append(
                db.session.query(Book).filter_by(id=book_id).first()
            )
        self.fans_count = len(fans)
        self.released_books_count = len(released_books)

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

    def remove_fan(self, fan_id) -> None:
        """remove a user from fans' list
        :param fan_id: user id
        """
        from .user import User

        fan: User = db.session.query(User).filter_by(id=fan_id).first()
        if fan:
            self.fans.remove(fan)
            self.fans_count -= 1

    def add_released_book(self, book_id) -> None:
        """Add a book to released_books' list"""
        from .book import Book

        book: Book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.append(book)
            self.released_books_count += 1

    def remove_released_book(self, book_id) -> None:
        """Remove a book from released_books' list"""
        from .book import Book

        book: Book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            self.released_books.remove(book)
            self.released_books_count -= 1
