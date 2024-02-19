import datetime

from helpers.init import db


class BookAnnouncement(db.Model):   # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(50), default=0)
    picture = db.Column(db.LargeBinary, default=0)
    premiere_date = db.Column(db.DateTime, nullable=False)

    # TODO bytes? czy napewno?
    def __init__(
        self,
        title: str,
        author: str,
        publishing_house: str,
        description: str,
        category: str,
        picture: bytes,
        premiere_date: datetime.datetime,
    ):
        self.title = title
        self.author = author
        self.publishing_house = publishing_house
        self.description = description
        self.category = category
        self.picture = picture
        self.premiere_date = premiere_date

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "category": self.category,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
        }
