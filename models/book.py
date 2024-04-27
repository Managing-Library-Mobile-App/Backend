import datetime

from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import authors_released_books


class Book(db.Model):  # type: ignore[name-defined]
    """The class representing table book in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    language = db.Column("language", db.String(50), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    authors = db.relationship(
        "Author",
        secondary=authors_released_books,
        lazy="subquery",
        back_populates="released_books",
    )
    publishing_house = db.Column(db.String(200))
    description = db.Column(db.String(3000), default=0)
    genres = db.Column(ARRAY(db.String(100)), default=[])
    picture = db.Column(
        db.String(200), default="https://demofree.sirv.com/nope-not-here.jpg?w=150"
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
    links = db.Column(ARRAY(db.String(50)), default=[])

    def __init__(
        self,
        isbn: str,
        language: str,
        title: str,
        authors: list[int],
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
        from .author import Author

        author_objects = (
            db.session.query(Author)
            .filter(*[Author.id == author_id for author_id in authors])
            .all()
        )
        if author_objects:
            self.authors = author_objects
            for author_object in author_objects:
                author_object.released_books_count += 1
                db.session.add(author_object)

        self.publishing_house = publishing_house
        self.description = description
        self.genres = genres
        self.picture = picture
        self.premiere_date = premiere_date

        self.links = [
            f"https://www.campusbooks.com/search/{isbn}?buysellrent=buy",
            f"https://www.amazon.com/s?rh=p_66%3A{isbn}",
            f"https://www.google.com/search?tbm=bks&q=isbn:{isbn}",
        ]

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "language": self.language,
            "isbn": self.isbn,
            "title": self.title,
            "authors": [author_object.id for author_object in self.authors],
            "authors_names": [author_object.name for author_object in self.authors],
            "publishing_house": self.publishing_house,
            "description": self.description,
            "genres": self.genres,
            "picture": self.picture,
            "premiere_date": self.premiere_date.strftime("%Y-%m-%d"),
            "score": self.score,
            "opinions_count": self.opinions_count,
            "opinions": [opinion.id for opinion in self.opinions],  # type: ignore
            "links": self.links,
        }
