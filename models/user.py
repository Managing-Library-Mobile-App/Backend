from helpers.init import db
from models.many_to_many_tables import authors_users


class User(db.Model):  # type: ignore[name-defined]
    """The class representing table user in database."""

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    library = db.relationship(
        "Library",
        backref="user",
        lazy="dynamic",
        passive_deletes=True,
        cascade="all, delete",
    )
    score = db.Column(db.Integer, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    opinions = db.relationship(
        "Opinion", backref="UserOpinion", cascade="all, delete", passive_deletes=True
    )
    followed_authors = db.relationship(
        "Author",
        secondary=authors_users,
        lazy="subquery",
        back_populates="fans",
    )
    followed_authors_count = db.Column(db.Integer, default=0)
    profile_picture = db.Column(
        db.String(200), default="https://www.gravatar.com/avatar/?d=mp"
    )
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(
        self, username: str, email: str, password: str, is_admin=False
    ) -> None:
        """Initializing an object of the class.
        :param is_admin: used for authentication
        """
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def as_dict(self) -> dict:
        """Serializing object to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "library": self.library.first().as_dict() if self.library else None,
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
