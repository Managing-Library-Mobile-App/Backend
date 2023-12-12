from helpers.init import db


class Admin(db.Model):
    _id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Admin %s>" % self._id
