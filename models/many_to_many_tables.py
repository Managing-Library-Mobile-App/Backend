from helpers.init import db

authors_users = db.Table(
    "fans",
    db.Column(
        "author_id",
        db.String,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

authors_released_books = db.Table(
    "released_books",
    db.Column(
        "author_id",
        db.String,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.String,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


library_books_favourite = db.Table(
    "favourite_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.String,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

library_books_bought = db.Table(
    "bought_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.String,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

library_books_read = db.Table(
    "read_books",
    db.Column(
        "library_id",
        db.Integer,
        db.ForeignKey("library.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.String,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
