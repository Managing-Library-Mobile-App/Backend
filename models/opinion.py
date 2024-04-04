from helpers.init import db


class Opinion(db.Model):  # type: ignore[name-defined]
    """The class representing table opinion in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    book_id = db.Column(
        db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"), nullable=False
    )
    stars_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), default="")

    __table_args__ = (
        db.UniqueConstraint("user_id", "book_id", name="uq_user_id_book_id"),
    )

    def __init__(
        self, user_id: int, book_id: int, stars_count: int, comment: str
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
            book.opinions_count += 1
            book.score += stars_count
            db.session.commit()

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "stars_count": self.stars_count,
            "comment": self.comment,
        }
