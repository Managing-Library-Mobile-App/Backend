import datetime

from sqlalchemy import ARRAY

from helpers.init import db
from models.many_to_many_tables import authors_released_books


class Book(db.Model):  # type: ignore[name-defined]
    """The class representing table book in database."""

    id = db.Column("id", db.String, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(1000), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.relationship(
        "Author",
        secondary=authors_released_books,
        lazy="subquery",
        back_populates="released_books",
    )
    publishing_house = db.Column(db.String(200))
    description = db.Column(db.String(150000), default=0)
    genres = db.Column(ARRAY(db.String(1000)), default=[])
    picture = db.Column(
        db.String(200), default="https://demofree.sirv.com/nope-not-here.jpg?w=150"
    )
    premiere_date = db.Column(db.Date, default=None)
    score = db.Column(db.Float, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion",
        backref="BookOpinion",
        lazy="subquery",
        cascade="all, delete",
    )
    links = db.Column(ARRAY(db.String(50)), default=[])
    number_of_pages = db.Column(db.Integer)

    def __init__(
        self,
        id: str,
        isbn: str,
        language: str,
        title: str,
        authors: list[str],
        publishing_house: str,
        description: str,
        premiere_date: datetime.datetime = None,
        genres: list = None,
        picture: str = None,
        number_of_pages: int = None,
    ) -> None:
        """Initializing an object of the class.
        :param isbn: either isbn-13 or isbn-15
        :param picture: link to the picture
        :param premiere_date: format(YYYY-MM-DD)
        """
        self.id = id
        self.isbn = isbn
        self.language = language
        self.title = title
        from .author import Author

        author_objects = [
            db.session.query(Author).filter(Author.id == author_id).first()
            for author_id in authors
        ]
        if author_objects:
            self.authors = author_objects
            for author_object in author_objects:
                session = db.create_session({})
                author_object.released_books_count += 1
                author_genres = author_object.genres
                author_genres = set(author_genres)
                for genre in genres:
                    author_genres.add(genre)
                author_object.genres = author_genres
                session.commit()
                session.close()

        self.publishing_house = publishing_house
        self.description = description
        if genres:
            self.genres = genres
        self.picture = picture
        self.premiere_date = premiere_date
        self.number_of_pages = number_of_pages

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
            "premiere_date": self.premiere_date.strftime("%d-%m-%Y"),
            "score": self.score,
            "opinions_count": self.opinions_count,
            "opinions": [opinion.id for opinion in self.opinions],  # type: ignore
            "links": self.links,
            "number_of_pages": self.number_of_pages,
        }
