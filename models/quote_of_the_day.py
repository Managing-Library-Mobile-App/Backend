import datetime

from helpers.init import db


class QuoteOfTheDay(db.Model):  # type: ignore[name-defined]
    """The class representing table opinion in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    quote = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    date = db.Column(db.Date, default=datetime.datetime.now)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    def __init__(self, quote: str, author: str, category: str, user_id: int) -> None:
        """Initializing an object of the class."""
        self.quote = quote
        self.author = author
        self.category = category
        self.user_id = user_id

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "quote": self.quote,
            "author": self.author,
            "category": self.category,
            "date": self.date.strftime("%d-%m-%Y"),
            "user_id": self.user_id,
        }