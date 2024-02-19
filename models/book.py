import datetime

from helpers.init import db

opinions = db.Table(
    "opinions",
    db.Column("opinion_id", db.Integer, db.ForeignKey("opinion.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


class Book(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    isbn = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(50), default=0)
    picture = db.Column(db.LargeBinary, default=0)
    premiere_date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion",
        secondary=opinions,
        lazy="subquery",
        backref=db.backref("opinions", lazy=True),
    )
    has_audiobook = db.Column(db.Boolean, default=False)

    # TODO czy napewno bytes?
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
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publishing_house": self.publishing_house,
            "description": self.description,
            "category": self.category,
            "picture": self.picture,
            "premiere_date": self.premiere_date,
            "score": self.score,
            "opinions": self.opinions,
            "has_audiobook": self.has_audiobook,
        }
