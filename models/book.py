import datetime

from sqlalchemy import ARRAY

from helpers.init import db
from models import author


class Book(db.Model):  # type: ignore[name-defined]
    """The class representing table book in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    language = db.Column("language", db.String(50), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
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
    premiere_date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Float, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion",
        backref="BookOpinion",
        lazy="subquery",
        cascade="all, delete",
    )

    def __init__(
        self,
        isbn: str,
        language: str,
        title: str,
        author_id: int,
        publishing_house: str,
        description: str,
        genres: list,
        picture: str,
        premiere_date: datetime.datetime,
    ) -> None:
        """Initializing an object of the class.
        :param isbn: either isbn-13 or isbn-15
        :param picture: link to the picture
        :param premiere_date: format(YYYY-MM-DD)
        """
        self.isbn = isbn
        self.language = language
        self.title = title
        self.author_id = author_id

        from .author import Author

        author: Author = db.session.query(Author).filter_by(id=author_id).first()
        if author:
            author.released_books_count += 1
            db.session.commit()

        self.publishing_house = publishing_house
        self.description = description
        self.genres = genres
        self.picture = picture
        self.premiere_date = premiere_date

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "language": self.language,
            "isbn": self.isbn,
            "title": self.title,
            "author_id": self.author_id,
            "author_name": author.Author.query.filter_by(id=self.author_id)
            .first()
            .name,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "genres": self.genres,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
            "score": self.score,
            "opinions_count": self.opinions_count,
            "opinions": [opinion.id for opinion in self.opinions],  # type: ignore
        }
