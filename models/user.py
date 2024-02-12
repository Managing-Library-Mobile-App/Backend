from helpers.init import db


class User(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    opinions_count = db.Column(db.Integer, default=0)
    reviews_count = db.Column(db.Integer, default=0)
    followed_authors_count = db.Column(db.Integer, default=0)
    library_id = db.Column(
        db.Integer, db.ForeignKey("library.id"), nullable=False, unique=True
    )
    profile_picture = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def as_dict(self):
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
