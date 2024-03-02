import datetime

from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import books_opinions


class Book(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # TODO pobranie autora żeby móc do niego przejść z książki
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )
    publishing_house = db.Column(db.String(100))
    description = db.Column(db.String(1000), default=0)
    genres = db.Column(ARRAY(db.String(50)), default=[])
    picture = db.Column(
        db.String(1000), default="https://demofree.sirv.com/nope-not-here.jpg?w=150"
    )
    premiere_date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    # TODO pobranie listy opinii dla książki
    opinions = db.relationship(
        "Opinion",
        secondary=books_opinions,
        lazy="subquery",
        backref=db.backref("books_opinions"),
        cascade="all, delete",
    )

    def __init__(
        self,
        isbn: str,
        title: str,
        author_id: int,
        publishing_house: str,
        description: str,
        genres: list,
        picture: str,
        premiere_date: datetime.datetime,
    ) -> None:
        self.isbn = isbn
        self.title = title
        self.author_id = author_id

        from .author import Author

        author = db.session.query(Author).filter_by(id=author_id).first()
        if author:
            author.released_books_count += 1
            db.session.commit()

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
            "author_id": self.author_id,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "genres": self.genres,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
            "score": self.score,
            "opinions_count": self.opinions_count,
            "opinions": [opinion.id for opinion in self.opinions],  # type: ignore
        }
