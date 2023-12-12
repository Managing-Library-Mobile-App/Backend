from helpers.init import db


class BookAnnouncement(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(50), default=0)
    picture = db.Column(db.LargeBinary, default=0)
    premiere_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<BookAnnouncement %s>" % self._id
