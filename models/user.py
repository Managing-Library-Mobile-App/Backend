from helpers.init import db


class User(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    library_id = db.Column(
        db.Integer,
        db.ForeignKey("library.id"),
        nullable=False,
        unique=True,
    )
    score = db.Column(db.Integer, default=0, nullable=True)
    opinions_count = db.Column(db.Integer, default=0, nullable=True)
    reviews_count = db.Column(db.Integer, default=0, nullable=True)
    followed_authors_count = db.Column(db.Integer, default=0, nullable=True)
    profile_picture = db.Column(db.LargeBinary, nullable=True)

    def __init__(
        self, username: str, email: str, password: str, library_id: int
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.library_id = library_id

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "score": self.score,
            "opinions_count": self.opinions_count,
            "reviews_count": self.reviews_count,
            "followed_authors_count": self.followed_authors_count,
            "library_id": self.library_id,
            "profile_picture": self.profile_picture,
        }
