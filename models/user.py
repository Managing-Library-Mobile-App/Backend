from helpers.init import db
from models.many_to_many_tables import authors_users


class User(db.Model):  # type: ignore[name-defined]
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    library_id = db.relationship(
        "Library",
        backref="library",
        cascade="all, delete",
        passive_deletes=True,
    )
    score = db.Column(db.Integer, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion", backref="opinion", cascade="all, delete", passive_deletes=True
    )
    followed_authors = db.relationship(
        "Author",
        secondary=authors_users,
        lazy="subquery",
        back_populates="fans",
        cascade="all, delete",
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
            "library_id": self.library_id,
            "score": self.score,
            "opinions_count": self.opinions_count,
            "opinions": [opinion.id for opinion in self.opinions],  # type: ignore
            "followed_authors_count": self.followed_authors_count,
            "followed_authors": [
                followed_author.id for followed_author in self.followed_authors  # type: ignore
            ],
            "profile_picture": self.profile_picture,
            "is_admin": self.is_admin,
        }
