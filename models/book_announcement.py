import datetime

from sqlalchemy import ARRAY

from helpers.init import db


class BookAnnouncement(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(
        db.Integer,
        db.ForeignKey("author.id"),
        nullable=False,
        unique=False,
    )
    publishing_house = db.Column(db.String(100))
    description = db.Column(db.String(1000), default="No description")
    genres = db.Column(ARRAY(db.String(50)), default=[])
    picture = db.Column(
        db.String(1000), default="https://demofree.sirv.com/nope-not-here.jpg?w=150"
    )
    premiere_date = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        title: str,
        author: id,
        publishing_house: str,
        description: str,
        genres: str,
        picture: str,
        premiere_date: datetime.datetime,
    ) -> None:
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
            "title": self.title,
            "author": self.author,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "genres": self.genres,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
        }
