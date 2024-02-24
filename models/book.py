import datetime

from sqlalchemy import ARRAY

from helpers.init import db

books_opinions = db.Table(
    "books_opinions",
    db.Column("opinion_id", db.Integer, db.ForeignKey("opinion.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


class Book(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(
        db.Integer,
        db.ForeignKey("author.id"),
        nullable=False,
        unique=False,
    )
    publishing_house = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    genres = db.Column(ARRAY(db.String(50)), default=0)
    picture = db.Column(db.String(1000), default=0)
    premiere_date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion",
        secondary=books_opinions,
        lazy="subquery",
        backref=db.backref("books_opinions", lazy=True),
    )

    def __init__(
        self,
        isbn: str,
        title: str,
        author: int,
        publishing_house: str,
        description: str,
        genres: str,
        picture: str,
        premiere_date: datetime.datetime,
    ) -> None:
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publishing_house = publishing_house
        self.description = description
        self.genres = genres
        self.picture = picture
        self.premiere_date = premiere_date

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "genres": self.genres,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
            "score": self.score,
            "opinions": self.opinions,
            "has_audiobook": self.has_audiobook,
        }
