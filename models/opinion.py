from helpers.init import db


class Opinion(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    stars_count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return "<Opinion %s>" % self._id
