import datetime

from helpers.init import db
from models import user


class Opinion(db.Model):  # type: ignore[name-defined]
    """The class representing table opinion in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    book_id = db.Column(
        db.String, db.ForeignKey("book.id", ondelete="CASCADE"), nullable=False
    )
    stars_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), default="")
    modified_date = db.Column(db.Date, default=datetime.datetime.now)

    __table_args__ = (
        db.UniqueConstraint("user_id", "book_id", name="uq_user_id_book_id"),
    )

    def __init__(
        self, user_id: int, book_id: str, stars_count: int, comment: str
    ) -> None:
        """Initializing an object of the class.
        :param stars_count: x/5, only integer values are allowed
        """
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.stars_count = stars_count

        from .user import User

        user: User = db.session.query(User).filter_by(id=user_id).first()
        if user:
            user.opinions_count += 1
            user.score += 1

        from .book import Book

        book: Book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            score = book.score * book.opinions_count + stars_count
            book.opinions_count += 1
            book.score = score / book.opinions_count
            db.session.commit()

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": user.User.query.filter_by(id=self.user_id).first().username,
            "profile_picture": user.User.query.filter_by(id=self.user_id)
            .first()
            .profile_picture,
            "book_id": self.book_id,
            "stars_count": self.stars_count,
            "comment": self.comment,
            "modified_date": self.modified_date.strftime("%d-%m-%Y"),
        }
