from helpers.init import db

favourite_books = db.Table(
    "favourite_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

bought_books = db.Table(
    "bought_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

read_books = db.Table(
    "read_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Library(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    read_books_count = db.Column(db.Integer, default=0, nullable=True)
    favourite_books_count = db.Column(db.Integer, default=0, nullable=True)
    bought_books_count = db.Column(db.Integer, default=0, nullable=True)
    read_books = db.relationship(
        "Book",
        secondary=read_books,
        lazy="subquery",
        backref=db.backref(
            "read_books", lazy=True, cascade="all, delete-orphan", single_parent=True
        ),
    )
    favourite_books = db.relationship(
        "Book",
        secondary=favourite_books,
        lazy="subquery",
        backref=db.backref(
            "favourite_books",
            lazy=True,
            cascade="all, delete-orphan",
            single_parent=True,
        ),
    )
    bought_books = db.relationship(
        "Book",
        secondary=bought_books,
        lazy="subquery",
        backref=db.backref(
            "bought_books", lazy=True, cascade="all, delete-orphan", single_parent=True
        ),
    )

    def __init__(self) -> None:
        pass

    def as_dict(self):
        return {
            "id": self.id,
            "read_books_count": self.read_books_count,
            "favourite_books_count": self.favourite_books_count,
            "bought_books_count": self.bought_books_count,
            "read_books": self.read_books,
            "favourite_books": self.favourite_books,
            "bought_books": self.bought_books,
        }
