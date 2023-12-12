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

    def __repr__(self):
        return "<User %s>" % self._id
