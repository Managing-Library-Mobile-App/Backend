from helpers.init import db

fans = db.Table(
    "fans",
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

released_books = db.Table(
    "released_books",
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)


class Author(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    genres = db.Column(db.String(50), nullable=False)
    biography = db.Column(db.String(1000), nullable=False)
    fans_count = db.Column(db.Integer, default=0)
    fans = db.relationship(
        "User",
        secondary=fans,
        lazy="subquery",
        backref=db.backref("fans", lazy=True),
    )
    released_books_count = db.Column(db.Integer, default=0)
    released_books = db.relationship(
        "Book",
        secondary=released_books,
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    def __repr__(self):
        return "<Author %s>" % self._id
