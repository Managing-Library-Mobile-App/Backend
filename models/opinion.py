from helpers.init import db
from models.book import Book
from models.user import User


class Opinion(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    book_id = db.Column(
        db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"), nullable=False
    )
    stars_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), default="")

    __table_args__ = (
        db.UniqueConstraint("account_id", "book_id", name="uq_account_id_book_id"),
    )

    def __init__(
        self, account_id: int, book_id: int, stars_count: int, comment: str
    ) -> None:
        self.account_id = account_id
        self.book_id = book_id
        self.comment = comment
        self.stars_count = stars_count

        user = User.query.filter_by(id=account_id).first()
        user.opinions_count += 1
        user.score += 1
        book = Book.query.filter_by(id=book_id).first()
        book.opinions_count += 1
        book.stars_count += stars_count
        db.session.commit()

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "book_id": self.book_id,
            "stars_count": self.stars_count,
            "comment": self.comment,
        }
