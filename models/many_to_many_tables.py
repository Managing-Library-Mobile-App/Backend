from helpers.init import db

authors_users = db.Table(
    "fans",
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

authors_released_books = db.Table(
    "released_books",
    db.Column(
        "author_id",
        db.Integer,
        db.ForeignKey("author.id"),
        primary_key=True,
    ),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)

books_opinions = db.Table(
    "books_opinions",
    db.Column("opinion_id", db.Integer, db.ForeignKey("opinion.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)
