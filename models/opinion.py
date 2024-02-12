from helpers.init import db


class Opinion(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    stars_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

    def __init__(self, account_id: int, book_id: int, stars_count: int, comment: str):
        self.account_id = account_id
        self.book_id = book_id
        self.stars_count = stars_count
        self.comment = comment

    def as_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "book_id": self.book_id,
            "stars_count": self.stars_count,
            "comment": self.comment,
        }
