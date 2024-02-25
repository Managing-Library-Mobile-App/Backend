from helpers.init import db
from models.many_to_many_tables import authors_users


class User(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    library_id = db.relationship(
        "Library",
        backref="library",
        cascade="all, delete",
        passive_deletes=True,
    )
    score = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion", backref="opinion", cascade="all, delete", passive_deletes=True
    )
    opinions_count = db.Column(db.Integer, default=0)
    followed_authors = db.relationship(
        "Author",
        secondary=authors_users,
        lazy="subquery",
        backref=db.backref("authors_users", lazy=True),
        overlaps="authors_users",
    )
    followed_authors_count = db.Column(db.Integer, default=0)
    profile_picture = db.Column(
        db.String(200), default="https://www.gravatar.com/avatar/?d=mp"
    )
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(
        self, username: str, email: str, password: str, is_admin=False
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

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
